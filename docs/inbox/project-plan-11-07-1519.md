---
version: 3
created_date: 25-11-07
note: synthesis.md 피드백 및 실제 MVP 배포 목적으로 전면 수정
---

## 0. 개발 시작 전 준비사항

### 개발 도구 설치

#### 필수 도구
```bash
# Python 3.11+ 설치 확인
python --version  # 3.11 이상이어야 함

# uv 설치 (의존성 관리)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# Docker Desktop 설치 (로컬 PostgreSQL용)
# https://www.docker.com/products/docker-desktop/
docker --version
docker-compose --version

# Firebase CLI 설치
npm install -g firebase-tools
firebase --version

# gcloud CLI 설치
# https://cloud.google.com/sdk/docs/install
gcloud --version
```

---

### 외부 서비스 계정 생성 및 설정

#### 1. PayPal Developer Account

**계정 생성:**
1. https://developer.paypal.com 접속
2. "Log in to Dashboard" → 계정 생성 또는 로그인

---

**A. 개발/테스트용: Sandbox 앱 생성**

1. "Apps & Credentials" → "Sandbox" 탭 선택
2. "Create App" 버튼 클릭
3. App Name 입력 (예: "Scout Landing Page Sandbox")
4. App Type: "Merchant" 선택
5. "Create App" 클릭

**발급받을 정보:**
- `PAYPAL_CLIENT_ID_SANDBOX`: Client ID (Sandbox)
- `PAYPAL_CLIENT_SECRET_SANDBOX`: Secret (Show 클릭 후 복사)
- API Base URL: `https://api-m.sandbox.paypal.com`

**Sandbox 테스트 계정:**
- "Sandbox" → "Accounts"에서 테스트용 buyer/seller 계정 확인
- 테스트 결제 시 사용

---

**B. 운영용: Production 앱 생성**

1. "Apps & Credentials" → "Live" 탭 선택
2. "Create App" 버튼 클릭
3. App Name 입력 (예: "Scout Landing Page Production")
4. App Type: "Merchant" 선택
5. "Create App" 클릭
6. **PayPal 검토 대기**: Production 앱은 PayPal 승인 필요 (수일 소요 가능)

**발급받을 정보:**
- `PAYPAL_CLIENT_ID_PROD`: Client ID (Live)
- `PAYPAL_CLIENT_SECRET_PROD`: Secret (Show 클릭 후 복사)
- API Base URL: `https://api-m.paypal.com`

**⚠️ 주의사항:**
- Production 앱은 실제 결제 처리
- PayPal 비즈니스 계정 필요
- 수수료 및 정산 정책 확인 필요

---

#### 2. Google Cloud Platform

**프로젝트 생성:**
1. https://console.cloud.google.com 접속
2. "프로젝트 선택" → "새 프로젝트"
3. 프로젝트 이름 입력 (예: "scout-landing-page")
4. 프로젝트 ID 기록 (예: `scout-landing-page-123456`)

**필수 API 활성화:**
```bash
# gcloud CLI로 API 활성화
gcloud config set project PROJECT_ID

gcloud services enable \
  sqladmin.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com
```

또는 콘솔에서:
- Cloud SQL Admin API
- Cloud Run API
- Secret Manager API
- Cloud Scheduler API
- (Phase 4) Places API

**서비스 계정 생성:**
1. IAM & Admin → Service Accounts
2. "Create Service Account"
3. 이름: `scout-api-service-account`
4. 역할 부여:
   - Cloud Run Admin
   - Cloud SQL Client
   - Secret Manager Secret Accessor
   - Cloud Scheduler Admin

**JSON 키 다운로드:**
1. 생성된 서비스 계정 클릭
2. "Keys" 탭 → "Add Key" → "Create new key"
3. JSON 선택 → "Create"
4. 다운로드된 JSON 파일 안전하게 보관
5. 이 파일 내용을 GitHub Secrets의 `GCP_SA_KEY`에 등록

**발급받을 정보:**
- 프로젝트 ID
- 서비스 계정 이메일
- JSON 키 파일

---

#### 3. Firebase

**프로젝트 생성 및 GCP 연동:**
1. https://console.firebase.google.com 접속
2. "프로젝트 추가"
3. 기존 GCP 프로젝트 선택 (위에서 생성한 scout-landing-page)
4. Google Analytics 설정 (선택사항, 일단 비활성화 가능)

**Hosting 활성화:**
1. Firebase Console → "Hosting" 메뉴
2. "시작하기" 클릭
3. 안내에 따라 진행 (로컬 설정은 나중에)

**Firebase CLI 로그인:**
```bash
firebase login
firebase projects:list  # 프로젝트 확인
```

**Firebase 초기화 (프로젝트 디렉토리에서):**
```bash
cd practice-landing-page
firebase init hosting

# 설정:
# - Public directory: frontend
# - Configure as single-page app: No
# - Set up automatic builds: No (GitHub Actions 사용)
```

**Service Account 생성 (GitHub Actions용):**
1. Firebase Console → 프로젝트 설정 (톱니바퀴 아이콘)
2. "서비스 계정" 탭
3. "새 비공개 키 생성" 클릭
4. JSON 파일 다운로드
5. 이 파일 내용을 GitHub Secrets의 `FIREBASE_SERVICE_ACCOUNT`에 등록

**발급받을 정보:**
- Firebase 프로젝트 ID
- Hosting URL (예: `https://scout-landing-page.web.app`)
- Service Account JSON

---

#### 4. GitHub Repository Secrets

**설정 위치:**
Repository → Settings → Secrets and variables → Actions → "New repository secret"

**등록할 Secrets:**
1. `GCP_SA_KEY`
   - GCP 서비스 계정 JSON 키 전체 내용

2. `FIREBASE_SERVICE_ACCOUNT`
   - Firebase 서비스 계정 JSON 키 전체 내용

---

### 준비사항 체크리스트

#### 개발 도구
- [ ] Python 3.11+ 설치 완료
- [ ] uv 설치 및 버전 확인
- [ ] Docker Desktop 설치 및 실행 확인
- [ ] Firebase CLI 설치 및 로그인
- [ ] gcloud CLI 설치 및 로그인

#### PayPal
- [ ] PayPal Developer 계정 생성
- [ ] Sandbox 앱 생성
- [ ] Client ID 및 Secret 발급 완료
- [ ] Sandbox 테스트 계정 확인

#### GCP
- [ ] GCP 프로젝트 생성
- [ ] 프로젝트 ID 기록
- [ ] 필수 API 활성화 (Cloud SQL, Cloud Run, Secret Manager, Scheduler)
- [ ] 서비스 계정 생성 및 역할 부여
- [ ] JSON 키 다운로드

#### Firebase
- [ ] Firebase 프로젝트 생성 (GCP 연동)
- [ ] Hosting 활성화
- [ ] Firebase CLI 로그인
- [ ] `firebase init hosting` 완료
- [ ] Service Account JSON 다운로드

#### GitHub
- [ ] `GCP_SA_KEY` Secrets 등록
- [ ] `FIREBASE_SERVICE_ACCOUNT` Secrets 등록

---

## 1. 프로젝트 개요

### 목적
- 실제 운영용 전자상거래 랜딩페이지 개발
- 단계적 구현으로 전자상거래 풀 플로우 구현
- Outside-In TDD 방법론 적용

### 배포 전략
**개발/테스트 환경:**
- PayPal Sandbox API 사용
- 로컬 개발: Docker PostgreSQL
- 스테이징: Cloud Run + Cloud SQL (개발용 인스턴스)

**운영 환경:**
- PayPal Production API 사용 (실제 결제 처리)
- Firebase Hosting (프론트엔드)
- Cloud Run (백엔드 API)
- Cloud SQL (프로덕션 데이터베이스)

### 기술 스택

#### Frontend
- HTML5, Vanilla JavaScript
- CSS
- Firebase Hosting (배포)

#### Backend
- **FastAPI** (웹 프레임워크)
- **PostgreSQL** (데이터베이스)
- **Cloud SQL** (관리형 PostgreSQL)
- **Cloud Run** (배포 환경)
- **Python 3.11+**

#### 테스트
- **pytest** (테스트 프레임워크)
- **pytest-cov** (커버리지)
- **pytest-playwright** (E2E 테스트)

#### 개발 도구
- **uv** (의존성 관리 - pip 대체)
- **ruff** (linter + formatter)
- **mypy** (타입 체커)
- **email-validator** (이메일 검증)
- **pyproject.toml** (통합 설정)
- **Docker** (로컬 PostgreSQL)

#### CI/CD
- **GitHub Actions** (테스트 + 배포)
- Firebase CLI
- gcloud CLI

#### 외부 서비스
- PayPal Sandbox (결제 - Phase 3)
- Google Places API (주소 - Phase 4)

---

## 2. 데이터베이스 스키마

### products
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,              -- 센타보(centavo) 단위 (페소 × 100)
    stock INTEGER NOT NULL DEFAULT 10
);
```

### orders
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
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

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(id),
    CHECK (total_amount = unit_price * quantity)
);

-- 인덱스
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_paypal_order_id ON orders(paypal_order_id);
CREATE INDEX idx_orders_status ON orders(order_status);
```

### shipments
```sql
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL,

    -- 배송 정보
    shipping_status TEXT DEFAULT 'PREPARING',

    tracking_number TEXT,
    courier TEXT,

    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    returned_at TIMESTAMP WITH TIME ZONE,              -- 환불 시 물품 반송 확인

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### refunds
```sql
CREATE TABLE refunds (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    paypal_refund_id TEXT,
    refund_amount INTEGER NOT NULL,     -- 센타보 단위
    refund_reason TEXT,
    refund_status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

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

2. **백그라운드 재시도** (Cloud Scheduler, 5분마다 실행):
   - 성공 시: `PAID` + 재고 차감
   - 실패 시: `PAYMENT_FAILED`

3. **3회 재시도 실패 시**:
   - 관리자 대시보드에 "수동 확인 필요" 플래그
   - 관리자가 PayPal 대시보드에서 직접 확인 후 처리

### 결제 중복 방지 (Idempotency)
- `paypal_order_id`를 UNIQUE 제약으로 중복 방지
- 재시도 전 DB 조회로 이미 처리된 주문 확인
- 동일 PayPal Order ID로 재요청 시 기존 주문 정보 반환

---

## 7. 데이터 검증 규칙

### 입력 검증 (필수)
```python
customer_name:
  - 2자 이상, 50자 이하

customer_email:
  - email-validator 라이브러리 사용
  - RFC 5322 표준 검증

  from email_validator import validate_email, EmailNotValidError
  try:
      validate_email(customer_email)
  except EmailNotValidError:
      raise ValidationError("이메일 형식이 올바르지 않습니다")

customer_phone:
  - 필리핀 형식: 09XX-XXX-XXXX (11자리) 또는 +63 9XX XXX XXXX
  - 정규식: ^(09\d{9}|\+639\d{9})$
  - 09로 시작: 총 11자리, +639로 시작: 총 12자리

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
   - 환불 요청 목록 표시 (주문번호, 환불 사유, 배송 상태 포함)
   - 환불 사유 확인
   - 승인 버튼 (confirm 후 PayPal 환불 처리)
   - **물품 반송 확인 버튼** (`DELIVERED` 상태 환불 시만 표시)
     - API: `POST /admin/shipments/{order_id}/return-confirm`
     - 반송 확인 시: `shipments.returned_at` 기록 → 재고 자동 복구
     - UI: 배송 상태가 `DELIVERED`이고 환불 승인된 경우에만 활성화
   - **인증**: API 키 (헤더: `X-Admin-Key`)

### API 엔드포인트

#### 사용자 API
```
POST   /api/orders                      # 주문 생성
GET    /api/orders/{order_number}       # 주문 조회
POST   /api/refunds                     # 환불 요청
POST   /api/payment/verify              # PayPal 결제 검증
```

#### 관리자 API (X-Admin-Key 헤더 필수)
```
GET    /admin/orders                             # 주문 목록 조회
PATCH  /admin/shipments/{order_id}              # 배송 상태 변경
GET    /admin/refunds                           # 환불 요청 목록
POST   /admin/refunds/{refund_id}/approve       # 환불 승인
POST   /admin/shipments/{order_id}/return-confirm  # 반송 확인
```

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
- 충돌 시 최대 3회 재시도

---

## 10. 프로젝트 구조

```
practice-landing-page/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── models.py            # Pydantic 모델/스키마
│   ├── db.py                # PostgreSQL 연결 + 연결 풀
│   ├── validators.py        # 입력 검증
│   ├── api/
│   │   ├── __init__.py
│   │   ├── orders.py        # 주문 API
│   │   ├── payment.py       # PayPal 결제 API
│   │   ├── admin.py         # 관리자 API
│   │   └── refunds.py       # 환불 API
│   └── db/
│       ├── __init__.py
│       └── connection.py    # DB 연결 관리
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── index.html           # 메인 랜딩페이지
│       ├── order_check.html     # 주문 조회 페이지
│       ├── admin_shipments.html # 배송 관리
│       └── admin_refunds.html   # 환불 관리
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest 설정
│   ├── data/
│   │   └── sample_purchases.json
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── factories.py     # 테스트 데이터 팩토리
│   │   └── helpers.py       # 테스트 헬퍼 함수
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_order_flow.py    # E2E 테스트
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_orders.py        # 주문 API 통합 테스트
│   │   ├── test_payment.py       # 결제 통합 테스트
│   │   └── test_refunds.py       # 환불 통합 테스트
│   └── unit/
│       ├── __init__.py
│       ├── test_validators.py    # 단위 테스트
│       └── test_models.py
├── docs/
│   ├── project-plan.md          # 본 문서
│   ├── inbox/
│   └── reviews/                 # AI 리뷰 기록
├── records/
│   ├── notes/                   # 개발 노트
│   └── sources/                 # 참고 자료
├── references/                  # 테스팅 관련 책
│   ├── growing-object-oriented-software/
│   ├── effective-software-testing/
│   └── ...
├── scripts/
│   ├── init_db.py               # DB 초기화
│   └── retry_payments.py        # PayPal 검증 재시도 (Cloud Run Job)
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions 배포
├── .env                         # 로컬 환경변수 (gitignore)
├── .firebaserc                  # Firebase 프로젝트 설정
├── firebase.json                # Firebase Hosting 설정
├── docker-compose.yml           # 로컬 PostgreSQL
├── pyproject.toml               # uv 설정
├── uv.lock
├── CLAUDE.md                    # Claude Code 프로젝트 설정
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

### 관리자 인증
```python
# app/routers/admin.py
import os
from fastapi import Header, HTTPException

def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
```

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

## 13. 환경 변수

### 로컬 개발 환경 (.env - gitignore)
```bash
# Database
DATABASE_URL=postgresql://dev:dev@localhost:5432/scout

# PayPal (Sandbox)
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com

# Admin
ADMIN_API_KEY=local-dev-key

# CORS (Firebase Hosting emulator)
ALLOWED_ORIGINS=http://localhost:5000
```

---

### 스테이징/테스트 환경 (GCP Secret Manager)
```bash
# Secret Manager에 시크릿 생성
gcloud secrets create staging-db-url --data-file=-
gcloud secrets create staging-paypal-client-id --data-file=-
gcloud secrets create staging-paypal-secret --data-file=-
gcloud secrets create staging-admin-api-key --data-file=-

# Cloud Run 배포 시 시크릿 참조 (Sandbox API 사용)
gcloud run deploy scout-api-staging \
  --set-secrets="DATABASE_URL=staging-db-url:latest,
                 PAYPAL_CLIENT_ID=staging-paypal-client-id:latest,
                 PAYPAL_CLIENT_SECRET=staging-paypal-secret:latest,
                 ADMIN_API_KEY=staging-admin-api-key:latest" \
  --set-env-vars="ALLOWED_ORIGINS=https://staging-project.web.app,
                  PAYPAL_API_BASE=https://api-m.sandbox.paypal.com"
```

**⚠️ 주의**: 스테이징 환경도 PayPal Sandbox API 사용

---

### 운영 환경 (GCP Secret Manager)
```bash
# Secret Manager에 시크릿 생성
gcloud secrets create prod-db-url --data-file=-
gcloud secrets create prod-paypal-client-id --data-file=-
gcloud secrets create prod-paypal-secret --data-file=-
gcloud secrets create prod-admin-api-key --data-file=-

# Cloud Run 배포 시 시크릿 참조 (Production API 사용)
gcloud run deploy scout-api \
  --set-secrets="DATABASE_URL=prod-db-url:latest,
                 PAYPAL_CLIENT_ID=prod-paypal-client-id:latest,
                 PAYPAL_CLIENT_SECRET=prod-paypal-secret:latest,
                 ADMIN_API_KEY=prod-admin-api-key:latest" \
  --set-env-vars="ALLOWED_ORIGINS=https://your-project.web.app,
                  PAYPAL_API_BASE=https://api-m.paypal.com"
```

**⚠️ 중요**:
- 운영 환경은 **PayPal Production API** 사용 (`https://api-m.paypal.com`)
- 실제 결제 처리되므로 배포 전 충분한 테스트 필요
- Production Client ID/Secret은 PayPal 승인 완료 후 사용 가능

---

## 14. 로컬 개발 환경 설정

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: scout
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 로컬 개발 시작
```bash
# 1. PostgreSQL 시작
docker-compose up -d

# 2. 의존성 설치
uv sync

# 3. 데이터베이스 초기화
uv run python scripts/init_db.py

# 4. Backend 개발 서버 실행
uv run uvicorn backend.main:app --reload --port 8000

# 5. Frontend 개발 서버 실행 (별도 터미널)
firebase emulators:start --only hosting

# 6. 테스트 실행
uv run pytest

# 7. 커버리지 확인
uv run pytest --cov=backend --cov-report=html
```

### Firebase 설정
```json
// firebase.json
{
  "hosting": {
    "public": "frontend",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "/api/**",
        "run": {
          "serviceId": "scout-api",
          "region": "asia-northeast3"
        }
      }
    ]
  }
}
```

```json
// .firebaserc
{
  "projects": {
    "default": "your-project-id"
  }
}
```

---

## 15. 배포 설정

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run and Firebase

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest --cov=backend

      - name: Run linter
        run: uv run ruff check .

      - name: Run type checker
        run: uv run mypy backend

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Authenticate to GCP
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1

      - name: Deploy Backend to Cloud Run
        run: |
          gcloud run deploy scout-api \
            --source=./backend \
            --region=asia-northeast3 \
            --platform=managed \
            --allow-unauthenticated \
            --set-secrets="DATABASE_URL=prod-db-url:latest,
                           PAYPAL_CLIENT_ID=paypal-client-id:latest,
                           PAYPAL_CLIENT_SECRET=paypal-secret:latest,
                           ADMIN_API_KEY=admin-api-key:latest" \
            --set-env-vars="ALLOWED_ORIGINS=https://your-project.web.app,
                            PAYPAL_API_BASE=https://api-m.paypal.com"

      - name: Deploy Frontend to Firebase Hosting
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: ${{ secrets.GITHUB_TOKEN }}
          firebaseServiceAccount: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
          channelId: live
          projectId: your-project-id
```

### Cloud SQL 연결 설정
```bash
# Cloud SQL 인스턴스 생성
gcloud sql instances create scout-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-northeast3

# 데이터베이스 생성
gcloud sql databases create scout --instance=scout-db

# 사용자 생성
gcloud sql users create scout-user \
  --instance=scout-db \
  --password=SECURE_PASSWORD

# Cloud Run에서 Cloud SQL 접근 권한 부여
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

### 배포 순서

**중요**: Firebase Hosting의 rewrites 설정이 Cloud Run URL을 참조하므로, **Backend를 먼저 배포**해야 합니다.

#### 1. 인프라 준비
```bash
# Cloud SQL 생성 (위 명령어 참조)
gcloud sql instances create scout-db ...

# 데이터베이스 초기화
uv run python scripts/init_db.py
```

#### 2. Secret Manager 시크릿 등록
```bash
# 환경에 맞는 시크릿 등록 (로컬/스테이징/운영)
gcloud secrets create prod-db-url ...
gcloud secrets create prod-paypal-client-id ...
# (섹션 13 참조)
```

#### 3. Backend Cloud Run 배포 (먼저!)
```bash
gcloud run deploy scout-api \
  --source=./backend \
  --region=asia-northeast3 \
  --set-secrets=... \
  --set-env-vars=...

# ✅ 배포 완료 후 Cloud Run URL 확인
# 예: https://scout-api-xxxxx-an.a.run.app
```

#### 4. Cloud Scheduler 설정
```bash
gcloud scheduler jobs create http paypal-retry-schedule ...
# (섹션 12 참조)
```

#### 5. Firebase Hosting 배포
```bash
# firebase.json에서 Backend URL 확인 후
firebase deploy --only hosting
```

#### 배포 순서 요약
1. Cloud SQL → 2. Secret Manager → 3. **Backend (먼저)** → 4. Scheduler → 5. Frontend

---

### 배포 전 체크리스트

#### 인프라 및 서비스 준비
- [ ] GCP 프로젝트 생성 완료
- [ ] Firebase 프로젝트 생성 및 GCP 연동
- [ ] Firebase Hosting 활성화
- [ ] Cloud SQL 인스턴스 생성 및 DATABASE_URL 확인
- [ ] GCP Secret Manager에 환경별 시크릿 등록 (개발/스테이징/운영)
- [ ] 서비스 계정 생성 및 권한 부여
- [ ] GitHub Secrets에 GCP_SA_KEY 및 FIREBASE_SERVICE_ACCOUNT 등록

#### PayPal 설정
- [ ] PayPal Sandbox 계정 및 앱 생성 (개발/테스트용)
- [ ] **PayPal Production 앱 생성 및 PayPal 승인 완료** (운영 배포 시)
- [ ] 운영 환경 시크릿이 Production API 사용하는지 확인
  - `PAYPAL_API_BASE=https://api-m.paypal.com`
  - Production Client ID/Secret 사용

#### 배포 설정
- [ ] firebase.json에서 Cloud Run 서비스 ID 확인
- [ ] ALLOWED_ORIGINS에 Firebase Hosting 도메인 설정
- [ ] **Backend 먼저 배포 후 Cloud Run URL 확인**
- [ ] Cloud Scheduler 설정 (PayPal 재시도)

#### 테스트
- [ ] 로컬에서 전체 테스트 통과 확인
- [ ] E2E 테스트 시나리오 작성 및 통과
- [ ] 스테이징 환경에서 충분한 테스트 완료 (운영 배포 전)

---

## 변경 사항 요약 (v2 → v3)

### 인프라 변경
1. ✅ SQLite → **PostgreSQL (Cloud SQL)** (프로덕션 준비)
2. ✅ Frontend/Backend 분리 → **Firebase Hosting + Cloud Run**
3. ✅ Cloud Storage 제거 → **Cloud SQL 자동 백업**
4. ✅ crontab → **Cloud Scheduler + Cloud Run Job**

### 기술 스택 추가
5. ✅ email-validator 라이브러리 (RFC 5322 검증)
6. ✅ Docker Compose (로컬 PostgreSQL)
7. ✅ GitHub Actions (CI/CD 통합)
8. ✅ PostgreSQL 연결 풀

### 스키마 개선
9. ✅ `AUTOINCREMENT` → `SERIAL`
10. ✅ `TIMESTAMP` → `TIMESTAMP WITH TIME ZONE`
11. ✅ CHECK 제약 추가 (`total_amount` 검증)
12. ✅ 인덱스 추가 (조회 성능 최적화)

### 문서 보완
13. ✅ API 엔드포인트 명세 추가
14. ✅ 로컬 개발 환경 설정 섹션
15. ✅ 배포 설정 및 체크리스트
16. ✅ 환경 변수 관리 전략 (Secret Manager)
17. ✅ CORS 설정
18. ✅ 결제 idempotency 처리

---

## 다음 단계

1. 로컬 개발 환경 설정 (Docker PostgreSQL)
4. 1-b단계 첫 테스트 작성 시작
