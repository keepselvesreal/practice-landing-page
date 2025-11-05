# Scout Landing Page MVP

## 1. 프로젝트 개요

### 목적
- 탐색 목적의 랜딩페이지 개발
- 최소한의 기능으로 빠른 프로토타입 구현
- 실제 개발을 통한 학습 및 고려사항 식별

### 기술 스택
- **프론트엔드**: HTML, CSS, Vanilla JavaScript (필요 시)
- **백엔드**: FastAPI
- **데이터베이스**: SQLite3 (동기 방식)
- **결제**: PayPal Sandbox
- **템플릿**: Static HTML + API 호출 방식
- **패키지 관리**: uv

## 2. 데이터베이스 스키마

### products
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
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
    unit_price REAL NOT NULL,
    total_amount REAL NOT NULL,

    -- PayPal 결제 정보
    paypal_order_id TEXT UNIQUE,
    paypal_transaction_id TEXT,
    payment_status TEXT DEFAULT 'PENDING',

    -- 주문 상태
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
    refund_amount REAL NOT NULL,
    refund_reason TEXT,
    refund_status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

## 3. 상품 정보

- **상품명**: 조선미녀 맑은쌀 선크림 50ml
- **가격**: 575원
- **초기 재고**: 10개
- **주문 수량**: 여러 개 주문 가능, 한 번에 전체 재고 구매 가능

## 4. 주문 상태 플로우

### 주문 상태 (order_status)
- `PAYMENT_PENDING`: 결제 대기
- `PAID`: 결제 완료
- `CANCELLED`: 취소
- `REFUNDED`: 환불 완료

### 결제 상태 (payment_status)
- `PENDING`: 결제 대기
- `COMPLETED`: 결제 완료
- `REFUNDED`: 환불 완료

### 배송 상태 (shipping_status)
- `PREPARING`: 배송 준비 중
- `SHIPPED`: 배송 중
- `DELIVERED`: 배송 완료

### 환불 상태 (refund_status)
- `PENDING`: 환불 대기
- `COMPLETED`: 환불 완료
- `FAILED`: 환불 실패

## 5. 비즈니스 로직

### 재고 관리
- **재고 차감 시점**: 주문 생성 시 (결제 전)
- **재고 복구**: 주문 취소 또는 환불 시 자동 복구
- **동시성 제어**: 트랜잭션 처리로 재고 꼬임 방지
- **재고 부족 시**: 에러 메시지 반환, 주문 불가

### 주문 취소
- **대상**: 결제 완료 후 (`PAID` 상태)
- **처리**:
  1. 주문 상태를 `CANCELLED`로 변경
  2. 재고 자동 복구

### 환불 처리
- **환불 가능 상태**: `PAID` (모든 배송 상태에서 가능)
- **프로세스**:
  1. 사용자가 환불 사유 입력 후 요청
  2. `refunds` 테이블에 레코드 생성 (`PENDING`)
  3. 관리자가 수동으로 승인 (confirm 후 처리)
  4. PayPal API로 환불 처리
  5. 주문 상태 `REFUNDED`, 환불 상태 `COMPLETED`
  6. 재고 자동 복구

### 배송 처리
- **shipment 생성 시점**: 결제 완료 시 자동 생성
- **상태 변경**: 관리자가 수동으로 변경 (`/admin/shipments`)

## 6. 페이지 구성

### 사용자 페이지
1. **메인 랜딩페이지** (`/`)
   - 상품 정보 표시
   - 구매자 정보 입력 폼 (이름, 이메일, 전화번호, 배송지)
   - 수량 선택
   - PayPal 결제 버튼

2. **주문 조회 페이지** (`/order-check`)
   - 주문번호 입력
   - 주문 정보 표시 (구매자 정보, 주문 상품, 수량, 금액)
   - 배송 상태 표시
   - 환불 요청 버튼 (조건부 활성화)
   - 환불 상태 표시

### 관리자 페이지
1. **배송 상태 변경** (`/admin/shipments`)
   - 주문 목록 표시
   - 배송 상태 변경 (PREPARING → SHIPPED → DELIVERED)
   - 송장번호, 택배사 입력
   - 인증 불필요

2. **환불 처리** (`/admin/refunds`)
   - 환불 요청 목록 표시
   - 환불 사유 확인
   - 승인 버튼 (confirm 후 PayPal 환불 처리)
   - 인증 불필요

## 7. UI/UX 정책

### 에러/성공 메시지
- 단순 `alert()` 사용

### 버튼 활성화/비활성화 규칙
- **환불 요청 버튼**:
  - 활성화: `order_status = PAID` AND 환불 미요청
  - 비활성화: 환불 요청 중(`PENDING`) 또는 환불 완료(`COMPLETED`)
  - 비활성화 시 상태 텍스트 표시 ("환불 진행 중", "환불 완료")

### 주문번호 형식
- `ORD-XXXXXXXX` (ORD- 접두사 + 8자리 랜덤 영숫자)

## 8. 프로젝트 구조

```
practice-landing-page/
└── scouting/
    ├── app/
    │   ├── main.py              # FastAPI 앱
    │   ├── models.py            # DB 모델/스키마
    │   ├── database.py          # DB 연결
    │   └── routers/
    │       ├── orders.py        # 주문 API
    │       └── payment.py       # PayPal 결제 API
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── main.js          # 필요 시
    ├── templates/
    │   ├── index.html           # 메인 랜딩페이지
    │   ├── order_check.html     # 주문 조회 페이지
    │   ├── admin_shipments.html # 배송 관리
    │   └── admin_refunds.html   # 환불 관리
    ├── tests/                   # TDD 테스트
    ├── database.db              # SQLite DB (gitignore)
    ├── .env                     # PayPal 키 등 (gitignore)
    ├── pyproject.toml           # uv 설정
    └── README.md
```

## 9. 개발 방법론

### Outside-In TDD
- 모든 핵심 기능은 TDD로 개발
- E2E 테스트부터 시작하여 내부 구현으로 진행
- 테스트 커버리지: API 엔드포인트 + DB 로직

### PayPal 통합
- PayPal Sandbox 환경 사용
- 서버 사이드에서 결제 검증
- Order ID와 Transaction ID 모두 저장
