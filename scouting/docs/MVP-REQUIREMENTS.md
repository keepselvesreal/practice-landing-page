---
version: 2
created_date: 25-11-04
note: synthesis.md의 비판적 피드백을 반영하여 전면 수정
---

# Scout Landing Page MVP

## 1. 프로젝트 개요

### 목적
- 탐색 목적의 랜딩페이지 개발
- 단계적 구현으로 전자상거래 풀 플로우 경험
- Outside-In TDD 방법론 학습 및 실습

### 기술 스택
- **프론트엔드**: HTML, CSS, Vanilla JavaScript
- **백엔드**: FastAPI
- **데이터베이스**: SQLite3 (동기 방식)
- **결제**: PayPal Sandbox
- **템플릿**: Static HTML + API 호출
- **패키지 관리**: uv
- **테스트**: pytest, pytest-mock

---

## 2. 데이터베이스 스키마

### products
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,              -- 센타보(centavo) 단위 (페소 × 100)
    stock INTEGER NOT NULL DEFAULT 10
);
```

### orders
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,  -- ORD-XXXXXXXX (8자리 랜덤)

    -- 구매자 정보
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    shipping_address TEXT NOT NULL,

    -- 주문 정보
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price INTEGER NOT NULL,        -- 센타보 단위
    total_amount INTEGER NOT NULL,      -- 센타보 단위

    -- PayPal 결제 정보
    paypal_order_id TEXT UNIQUE,
    paypal_transaction_id TEXT,

    -- 주문 상태 (단일 상태로 통합)
    order_status TEXT DEFAULT 'PAYMENT_PENDING',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### shipments
```sql
CREATE TABLE shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE NOT NULL,

    -- 배송 정보
    shipping_status TEXT DEFAULT 'PREPARING',

    tracking_number TEXT,
    courier TEXT,

    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    returned_at TIMESTAMP,              -- 환불 시 물품 반송 확인

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### refunds
```sql
CREATE TABLE refunds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    paypal_refund_id TEXT,
    refund_amount INTEGER NOT NULL,     -- 센타보 단위
    refund_reason TEXT,
    refund_status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

---

## 3. 상품 정보

- **상품명**: 조선미녀 맑은쌀 선크림 50ml
- **가격**: 575 페소 (DB 저장: 57500 센타보)
- **초기 재고**: 10개
- **주문 수량**: 여러 개 주문 가능, 한 번에 전체 재고 구매 가능

---

## 4. 상태 관리

### 주문 상태 (order_status) - 단일 상태로 통합
- `PAYMENT_PENDING`: 결제 대기 (주문 생성 직후)
- `VERIFICATION_PENDING`: 결제 검증 중 (PayPal API 타임아웃 시)
- `PAID`: 결제 완료 (재고 차감됨)
- `PAYMENT_FAILED`: 결제 실패
- `CANCELLED`: 주문 취소
- `REFUNDED`: 환불 완료

### 배송 상태 (shipping_status)
- `PREPARING`: 배송 준비 중
- `SHIPPED`: 배송 중
- `DELIVERED`: 배송 완료

### 환불 상태 (refund_status)
- `PENDING`: 환불 대기
- `COMPLETED`: 환불 완료
- `FAILED`: 환불 실패

---

## 5. 비즈니스 로직

### 재고 관리
- **재고 차감 시점**: **결제 완료 시** (`PAID` 상태 전환 시)
- **재고 복구 조건**:
  - 주문 취소: 즉시 복구
  - 환불 시 (배송 상태별):
    - `PREPARING`, `SHIPPED`: 환불 승인 시 즉시 복구
    - `DELIVERED`: **물품 반송 확인 후** 복구 (`returned_at` 기록 후)
- **동시성 제어**: 트랜잭션 처리로 재고 꼬임 방지
- **재고 부족 시**: `409 Conflict` 반환, 현재 재고 수량 포함

### 주문 취소
- **대상**: 결제 완료 후 (`PAID` 상태), 배송 전 (`PREPARING`)
- **처리**:
  1. 주문 상태를 `CANCELLED`로 변경
  2. 재고 자동 복구

### 환불 처리
- **환불 가능 상태**: `PAID` (모든 배송 상태에서 가능)
- **프로세스**:
  1. 사용자가 환불 사유 입력 후 요청
  2. `refunds` 테이블에 레코드 생성 (`PENDING`)
  3. 관리자가 환불 승인
  4. PayPal API로 환불 처리
  5. 주문 상태 `REFUNDED`, 환불 상태 `COMPLETED`
  6. 배송 상태별 재고 복구:
     - `PREPARING`, `SHIPPED`: 즉시 복구
     - `DELIVERED`: 물품 반송 확인 후 복구

### 배송 처리
- **shipment 생성 시점**: 결제 완료 시 자동 생성
- **상태 변경**: 관리자가 수동으로 변경 (`/admin/shipments`)

---

## 6. 에러 처리 정책

### HTTP 상태 코드
```
200: 성공
201: 생성 성공 (주문 생성)
400: 입력 오류 (이메일 형식, 수량 등)
401: 인증 실패 (관리자 API)
404: 리소스 없음 (주문번호 조회 실패)
409: 재고 부족
500: 서버 오류
```

### 에러 응답 형식
```json
{
  "error": "재고가 부족합니다",
  "code": "STOCK_INSUFFICIENT",
  "details": {
    "requested": 5,
    "available": 3
  }
}
```

### PayPal API 타임아웃 처리
1. **타임아웃 발생 시**:
   - `order_status` → `VERIFICATION_PENDING`
   - 재고는 차감하지 않음
   - 사용자에게: "결제 확인 중입니다. 주문번호: ORD-XXX"

2. **백그라운드 재시도** (배치 작업, 5분마다 실행):
   - 성공 시: `PAID` + 재고 차감
   - 실패 시: `PAYMENT_FAILED`

3. **3회 재시도 실패 시**:
   - 관리자 대시보드에 "수동 확인 필요" 플래그
   - 관리자가 PayPal 대시보드에서 직접 확인 후 처리

---

## 7. 데이터 검증 규칙

### 입력 검증 (필수)
```python
customer_name:
  - 2자 이상, 50자 이하

customer_email:
  - 이메일 형식 검증 (정규식: ^[^@]+@[^@]+\.[^@]+$)

customer_phone:
  - 숫자만 허용
  - 10-11자리

quantity:
  - 1 이상
  - 재고 이하

shipping_address:
  - 10자 이상
```

### 검증 실패 시
```json
{
  "error": "입력값이 유효하지 않습니다",
  "code": "VALIDATION_ERROR",
  "details": {
    "customer_email": "이메일 형식이 올바르지 않습니다",
    "quantity": "수량은 1 이상이어야 합니다"
  }
}
```

---

## 8. 페이지 구성

### 사용자 페이지
1. **메인 랜딩페이지** (`/`)
   - 상품 정보 표시
   - 구매자 정보 입력 폼 (이름, 이메일, 전화번호, 배송지)
   - 수량 선택
   - PayPal 결제 버튼

2. **주문 조회 페이지** (`/order-check`)
   - 주문번호 입력
   - 주문 정보 표시 (구매자 정보, 주문 상품, 수량, 금액)
   - 배송 상태 표시 (2단계 이후)
   - 환불 요청 버튼 (3단계 이후, 조건부 활성화)
   - 환불 상태 표시 (3단계 이후)

### 관리자 페이지
1. **배송 상태 변경** (`/admin/shipments`)
   - 주문 목록 표시
   - 배송 상태 변경 (PREPARING → SHIPPED → DELIVERED)
   - 송장번호, 택배사 입력
   - **인증**: API 키 (헤더: `X-Admin-Key`)

2. **환불 처리** (`/admin/refunds`)
   - 환불 요청 목록 표시
   - 환불 사유 확인
   - 승인 버튼 (confirm 후 PayPal 환불 처리)
   - 물품 반송 확인 버튼 (`DELIVERED` 상태 환불 시)
   - **인증**: API 키 (헤더: `X-Admin-Key`)

---

## 9. UI/UX 정책

### 에러/성공 메시지
- 인라인 메시지 영역 사용
- 성공: 초록색 배경 (`#4CAF50`)
- 에러: 빨간색 배경 (`#f44336`)
- 3-5초 후 자동 사라짐 (선택 사항)

```html
<div id="message" class="message success" style="display:none;">
  주문이 생성되었습니다. 주문번호: ORD-12345678
</div>
```

### 버튼 활성화/비활성화 규칙
- **환불 요청 버튼**:
  - 활성화: `order_status = PAID` AND 환불 미요청
  - 비활성화: 환불 요청 중(`PENDING`) 또는 환불 완료(`COMPLETED`)
  - 비활성화 시 상태 텍스트 표시 ("환불 진행 중", "환불 완료")

### 주문번호 형식
- `ORD-XXXXXXXX` (ORD- 접두사 + 8자리 랜덤 영숫자, 대문자)

---

## 10. 프로젝트 구조

```
practice-landing-page/
└── scouting/
    ├── app/
    │   ├── main.py              # FastAPI 앱
    │   ├── models.py            # DB 모델/스키마
    │   ├── database.py          # DB 연결 + execute_update 헬퍼
    │   ├── validators.py        # 입력 검증
    │   └── routers/
    │       ├── orders.py        # 주문 API
    │       ├── payment.py       # PayPal 결제 API
    │       ├── admin.py         # 관리자 API
    │       └── refunds.py       # 환불 API
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── main.js
    ├── templates/
    │   ├── index.html           # 메인 랜딩페이지
    │   ├── order_check.html     # 주문 조회 페이지
    │   ├── admin_shipments.html # 배송 관리
    │   └── admin_refunds.html   # 환불 관리
    ├── tests/
    │   ├── test_orders.py       # 주문 테스트
    │   ├── test_payment.py      # 결제 테스트
    │   └── test_refunds.py      # 환불 테스트
    ├── scripts/
    │   └── retry_payments.py    # PayPal 검증 재시도 배치
    ├── database.db              # SQLite DB (gitignore)
    ├── .env                     # PayPal 키, ADMIN_API_KEY (gitignore)
    ├── pyproject.toml           # uv 설정
    └── README.md
```

---

## 11. 개발 방법론

### Outside-In TDD
- 모든 핵심 기능은 TDD로 개발
- E2E 테스트부터 시작하여 내부 구현으로 진행
- Red-Green-Refactor 사이클 준수

### 단계별 구현 순서
1. **1-b단계**: 주문 조회 API (Mock 데이터)
2. **1-a단계**: 주문 생성 + PayPal 결제 + 재고 차감
3. **2단계**: 배송 추적 시스템
4. **3단계**: 환불 시스템

자세한 내용은 `IMPLEMENTATION-PLAN.md` 참조

---

## 12. 기술적 구현 세부사항

### updated_at 자동 갱신
```python
# database.py
from datetime import datetime

def execute_update(cursor, table: str, set_clause: dict, where_clause: dict):
    """
    자동으로 updated_at을 추가하는 UPDATE 헬퍼
    """
    set_clause["updated_at"] = datetime.now()

    set_parts = ", ".join([f"{k}=?" for k in set_clause.keys()])
    where_parts = " AND ".join([f"{k}=?" for k in where_clause.keys()])

    sql = f"UPDATE {table} SET {set_parts} WHERE {where_parts}"
    params = list(set_clause.values()) + list(where_clause.values())

    cursor.execute(sql, params)
```

### 관리자 인증
```python
# .env
ADMIN_API_KEY=your-secret-key-here

# app/routers/admin.py
from fastapi import Header, HTTPException

def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
```

### PayPal 결제 검증 재시도 (배치 작업)
```bash
# crontab -e
*/5 * * * * cd /path/to/scouting && uv run python scripts/retry_payments.py
```

---

## 13. 환경 변수

```bash
# .env
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com
ADMIN_API_KEY=secret-key-12345
```

---

## 변경 사항 요약 (v1 → v2)

### 치명적 문제 수정
1. ✅ 재고 차감 시점: 주문 생성 시 → **결제 완료 시**
2. ✅ 환불 시 재고 복구: 무조건 복구 → **배송 상태별 조건 적용**
3. ✅ 금액 타입: `REAL` → **`INTEGER` (센타보 단위)**
4. ✅ 관리자 인증: 불필요 → **API 키 인증**
5. ✅ `updated_at`: 자동 갱신 미지원 → **헬퍼 함수로 명시적 갱신**

### 구조적 개선
6. ✅ MVP 범위: 한 번에 전체 → **단계적 구현 (1-b → 1-a → 2 → 3)**
7. ✅ 에러 처리: 미정의 → **HTTP 코드 + PayPal 타임아웃 전략 추가**
8. ✅ 상태 관리: 이중 상태 → **단일 `order_status`로 통합**
9. ✅ 데이터 검증: 없음 → **필수 검증 규칙 추가**
10. ✅ UI 피드백: `alert()` → **인라인 메시지**
11. ✅ TDD 시작점: 불명확 → **1-b부터 시작 (조회 → 생성 순서)**

---

## 다음 단계

1. `IMPLEMENTATION-PLAN.md` 읽기
2. `OUTSIDE-IN-TDD-GUIDE.md`로 TDD 학습
3. 1-b단계 첫 테스트 작성 시작
