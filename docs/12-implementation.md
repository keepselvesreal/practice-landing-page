---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### PostgreSQL 연결
```python
# backend/db.py
import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL")

# 연결 풀 생성 (최소 1, 최대 10 연결)
connection_pool = SimpleConnectionPool(1, 10, DATABASE_URL)

@contextmanager
def get_db_connection():
    """
    연결 풀에서 연결 가져오기 (Context Manager)

    예외 발생 시에도 연결을 안전하게 반환
    """
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)

# 사용 예시
# with get_db_connection() as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM products")
#     # 예외 발생 시에도 자동으로 연결 반환됨
```

---

### updated_at 자동 갱신
```python
# backend/db.py
from datetime import datetime, timezone
from psycopg2 import sql

def execute_update(cursor, table: str, set_clause: dict, where_clause: dict):
    """
    자동으로 updated_at을 추가하는 UPDATE 헬퍼

    SQL 인젝션 방지를 위해 psycopg2.sql.Identifier 사용
    """
    set_clause["updated_at"] = datetime.now(timezone.utc)

    # 테이블명과 컬럼명은 Identifier로 안전하게 처리
    set_parts = sql.SQL(", ").join([
        sql.SQL("{} = %s").format(sql.Identifier(k))
        for k in set_clause.keys()
    ])

    where_parts = sql.SQL(" AND ").join([
        sql.SQL("{} = %s").format(sql.Identifier(k))
        for k in where_clause.keys()
    ])

    query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
        sql.Identifier(table),
        set_parts,
        where_parts
    )

    params = list(set_clause.values()) + list(where_clause.values())
    cursor.execute(query, params)
```

---

### 개인정보 암호화 (Fernet) - 신규
```python
# backend/crypto.py
from cryptography.fernet import Fernet
import os

# 환경변수에서 암호화 키 로드
cipher = Fernet(os.getenv("ENCRYPTION_KEY").encode())

def encrypt(plaintext: str) -> str:
    """평문을 암호화하여 반환"""
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt(ciphertext: str) -> str:
    """암호문을 복호화하여 반환"""
    return cipher.decrypt(ciphertext.encode()).decode()

# 사용 예시
# encrypted_email = encrypt("user@example.com")
# decrypted_email = decrypt(encrypted_email)
```

**암호화 키 생성:**
```python
from cryptography.fernet import Fernet

# 새 암호화 키 생성
key = Fernet.generate_key()
print(key.decode())  # 환경변수에 저장할 키
```

**암호화 대상:**
- `orders.customer_name`
- `orders.customer_email`
- `orders.customer_phone`
- `orders.shipping_address`

---

### Gmail SMTP 이메일 발송 - 신규
```python
# backend/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email: str, subject: str, html_content: str):
    """
    Gmail SMTP로 이메일 발송

    Args:
        to_email: 수신자 이메일
        subject: 제목
        html_content: HTML 본문
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = to_email
    msg["Subject"] = subject

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(
            os.getenv("GMAIL_ADDRESS"),
            os.getenv("GMAIL_APP_PASSWORD")
        )
        server.send_message(msg)

# 사용 예시
# send_email(
#     to_email="customer@example.com",
#     subject="주문 확인",
#     html_content="<h1>주문이 완료되었습니다.</h1>"
# )
```

---

### 어필리에이트 클릭 추적 - 신규
```python
# backend/api/affiliates.py
from fastapi import Response

@app.get("/api/affiliate/track")
def track_affiliate_click(code: str, response: Response):
    """
    어필리에이트 클릭 추적

    - 쿠키에 affiliate_code 저장 (30일 유지)
    - affiliate_stats.click_count 증가
    """
    # 쿠키에 저장
    response.set_cookie(
        key="affiliate_code",
        value=code,
        max_age=30 * 24 * 60 * 60,  # 30일
        httponly=True
    )

    # DB에 클릭 카운트 증가
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE affiliate_stats
            SET click_count = click_count + 1,
                updated_at = NOW()
            WHERE affiliate_code = %s
        """, (code,))
        conn.commit()

    # 메인 페이지로 리다이렉트
    return {"redirect": "/"}
```

**주문 생성 시 커미션 계산:**
```python
# 주문 생성 API에서
affiliate_code = request.cookies.get("affiliate_code")

if affiliate_code:
    # 커미션 계산: (unit_price * quantity) * 0.20
    commission = int((unit_price * quantity) * 0.20)

    # affiliate_stats 업데이트
    cursor.execute("""
        UPDATE affiliate_stats
        SET sale_count = sale_count + 1,
            pending_commission = pending_commission + %s,
            updated_at = NOW()
        WHERE affiliate_code = %s
    """, (commission, affiliate_code))
```

---

### 다국어 처리 (i18n) - 신규
```javascript
// frontend/js/i18n.js
const translations = {
  en: {
    title: "Scout Sunscreen",
    price: "Price",
    shipping: "Shipping",
    total: "Total",
    order_now: "Order Now",
    // ...
  },
  tl: {
    title: "Scout Sunscreen",
    price: "Presyo",
    shipping: "Shipping",
    total: "Kabuuan",
    order_now: "Umorder Na",
    // ...
  }
};

let currentLang = localStorage.getItem("lang") || "en";

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("lang", lang);
  updateUI();
}

function updateUI() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    el.textContent = translations[currentLang][key];
  });
}

// 페이지 로드 시 실행
document.addEventListener("DOMContentLoaded", updateUI);
```

**HTML 사용:**
```html
<h1 data-i18n="title">Scout Sunscreen</h1>
<button onclick="setLanguage('tl')">Tagalog</button>
<button onclick="setLanguage('en')">English</button>
```

---

### 관리자 인증
```python
# backend/api/admin.py
import os
from fastapi import Header, HTTPException

def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
```

---

### CORS 설정
```python
# backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (Firebase Hosting에서의 요청 허용)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Cloud Scheduler 설정 (PayPal 결제 검증 재시도)
```bash
# Cloud Run Job 배포
gcloud run jobs create paypal-retry-job \
  --source=. \
  --command="python,scripts/retry_payments.py" \
  --region=asia-northeast3

# Cloud Scheduler 생성 (5분마다 실행)
gcloud scheduler jobs create http paypal-retry-schedule \
  --location=asia-northeast3 \
  --schedule="*/5 * * * *" \
  --uri="https://asia-northeast3-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/PROJECT_ID/jobs/paypal-retry-job:run" \
  --http-method=POST \
  --oidc-service-account-email=SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com
```

---

### 미반영 요구사항
- REQ-F09~F11, F28: 이메일 자동 발송 (템플릿만 정의, 자동화 로직 구현 필요)
  - 주문 확인 이메일
  - 배송 완료 이메일
  - 재구매 확인 이메일
