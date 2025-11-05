---
version: 1
created_date: 25-11-04
note: Outside-In TDD 기반 단계별 구현 계획
---

# 단계별 구현 계획

> **전제**: Outside-In TDD 방법론으로 개발
> **순서**: 1-b → 1-a → 2 → 3

---

## 1-b단계: 주문 조회 API

### 1.1 기능 범위

**목표**: 주문번호를 입력하면 주문 정보를 조회할 수 있다

**구현 범위**:
- GET `/orders/{order_number}` API
- 주문 정보 응답 (구매자 정보, 주문 상태, 금액 등)
- 404 에러 처리 (주문번호 없을 시)
- 주문 조회 페이지 (`/order-check`)

**제외 사항**:
- 실제 주문 생성 (Mock 데이터로 테스트)
- PayPal 통합
- 배송/환불 정보 (추후 단계에서 추가)

---

### 1.2 TDD 시나리오

#### E2E 테스트 (최상위)
```python
def test_user_can_check_order_by_order_number():
    """
    사용자가 주문번호를 입력하면 주문 정보를 조회할 수 있다

    Given: 결제 완료된 주문이 존재함
    When: GET /orders/ORD-12345678 요청
    Then: 200 응답, 주문 정보 반환 (구매자 정보, 주문 상태, 금액)
    """
```

#### API 레벨 테스트
```python
def test_get_order_returns_order_info():
    """GET /orders/{order_number} → 200, 주문 정보 포함"""

def test_get_order_not_found():
    """존재하지 않는 주문번호 → 404"""

def test_order_response_format():
    """응답 형식 검증 (필수 필드 포함 여부)"""
```

#### 서비스 레벨 테스트
```python
def test_get_order_service_queries_db():
    """get_order_service()가 DB를 조회하는지 검증 (Mock 사용)"""

def test_get_order_service_raises_not_found():
    """주문이 없으면 OrderNotFound 예외 발생"""
```

#### Repository/DB 레벨 테스트
```python
def test_query_order_by_number():
    """DB에서 주문번호로 조회 성공"""

def test_query_order_returns_none_when_not_found():
    """주문번호 없으면 None 반환"""
```

---

### 1.3 API 명세

#### GET `/orders/{order_number}`

**요청**:
```
GET /orders/ORD-12345678
```

**성공 응답** (200):
```json
{
  "order_number": "ORD-12345678",
  "customer_name": "홍길동",
  "customer_email": "hong@example.com",
  "customer_phone": "01012345678",
  "shipping_address": "서울시 강남구 테헤란로 123",
  "product_name": "조선미녀 맑은쌀 선크림 50ml",
  "quantity": 2,
  "unit_price": 57500,
  "total_amount": 115000,
  "order_status": "PAID",
  "created_at": "2025-11-04T10:30:00"
}
```

**실패 응답** (404):
```json
{
  "error": "주문을 찾을 수 없습니다",
  "code": "ORDER_NOT_FOUND"
}
```

---

### 1.4 DB 스키마 (필요 테이블)

이 단계에서는 `products`와 `orders` 테이블만 필요:

```sql
-- 테스트용 초기 데이터
INSERT INTO products (id, name, price, stock)
VALUES (1, '조선미녀 맑은쌀 선크림 50ml', 57500, 10);

INSERT INTO orders (
  order_number, customer_name, customer_email, customer_phone,
  shipping_address, product_id, quantity, unit_price, total_amount,
  order_status
) VALUES (
  'ORD-12345678', '홍길동', 'hong@example.com', '01012345678',
  '서울시 강남구 테헤란로 123', 1, 2, 57500, 115000, 'PAID'
);
```

---

### 1.5 구현 체크리스트

#### 준비
- [ ] `scouting/` 디렉토리 생성
- [ ] `pyproject.toml` 작성 (FastAPI, pytest 등)
- [ ] `database.db` 초기화 스크립트 작성
- [ ] 테스트용 데이터 삽입

#### 개발 (Outside-In 순서)
- [ ] **E2E 테스트 작성** (실패 확인)
- [ ] FastAPI 앱 생성 (`main.py`)
- [ ] GET `/orders/{order_number}` 엔드포인트 추가 (빈 응답)
- [ ] **API 테스트 작성** (응답 형식 검증)
- [ ] Service 레이어 추가 (Mock으로 Repository 대체)
- [ ] **Service 테스트 작성**
- [ ] Repository 레이어 추가 (실제 DB 조회)
- [ ] **Repository 테스트 작성**
- [ ] Mock 제거하고 **통합 테스트 실행**
- [ ] 404 에러 처리 추가
- [ ] 주문 조회 페이지 HTML 작성
- [ ] JavaScript로 API 호출 연결

#### 검증
- [ ] 모든 테스트 통과 (`pytest -v`)
- [ ] 브라우저에서 수동 테스트
- [ ] 존재하는 주문번호 조회 → 정보 표시 확인
- [ ] 존재하지 않는 주문번호 → 에러 메시지 확인

---

## 1-a단계: 주문 생성 + PayPal 결제

### 2.1 기능 범위

**목표**: 사용자가 상품을 주문하고 PayPal로 결제 완료 시, 주문번호를 받는다

**구현 범위**:
- POST `/orders` API (주문 생성)
- POST `/orders/{order_id}/verify-payment` API (결제 검증)
- PayPal Order API 통합
- 결제 완료 후 재고 차감
- 입력 검증 (이메일, 전화번호, 수량 등)
- PayPal 타임아웃 처리 (`VERIFICATION_PENDING` 상태)
- 메인 랜딩페이지 (`/`)

**제외 사항**:
- 배송 정보 (2단계)
- 환불 기능 (3단계)

---

### 2.2 TDD 시나리오

#### E2E 테스트
```python
def test_user_orders_and_completes_paypal_payment():
    """
    사용자가 상품 1개를 주문하고 PayPal로 결제 완료 시,
    주문 번호를 받는다

    Given: 재고 10개인 상품
    When:
      1. POST /orders → order_number, paypal_order_id 받음
      2. (사용자가 PayPal에서 결제 완료 - 테스트에서는 Mock)
      3. POST /orders/{id}/verify-payment → PAID 상태 확인
    Then:
      - order_status = PAID
      - 재고 9개 (결제 완료 후 차감)
      - 주문번호로 조회 가능
    """
```

#### API 레벨 테스트
```python
def test_create_order_returns_order_number():
    """POST /orders → 201, order_number 반환"""

def test_create_order_validates_input():
    """잘못된 이메일 형식 → 400"""

def test_create_order_checks_stock():
    """재고 부족 → 409"""

def test_verify_payment_updates_status():
    """POST /orders/{id}/verify-payment → order_status PAID"""

def test_verify_payment_deducts_stock():
    """결제 검증 성공 시 재고 차감"""

def test_paypal_timeout_sets_verification_pending():
    """PayPal 타임아웃 → VERIFICATION_PENDING"""
```

#### 서비스 레벨 테스트
```python
def test_generate_order_number_format():
    """주문번호 형식: ORD-XXXXXXXX"""

def test_create_order_does_not_deduct_stock():
    """주문 생성 시 재고 차감 안 함"""

def test_verify_payment_calls_paypal_api():
    """verify_payment()가 PayPal API 호출하는지 검증"""

def test_deduct_stock_after_payment():
    """결제 완료 시 재고 차감 로직"""
```

---

### 2.3 API 명세

#### POST `/orders`

**요청**:
```json
{
  "customer_name": "홍길동",
  "customer_email": "hong@example.com",
  "customer_phone": "01012345678",
  "shipping_address": "서울시 강남구 테헤란로 123",
  "product_id": 1,
  "quantity": 2
}
```

**성공 응답** (201):
```json
{
  "order_number": "ORD-A1B2C3D4",
  "order_id": 123,
  "paypal_order_id": "7RY12345678901234",
  "total_amount": 115000,
  "order_status": "PAYMENT_PENDING"
}
```

**재고 부족** (409):
```json
{
  "error": "재고가 부족합니다",
  "code": "STOCK_INSUFFICIENT",
  "details": {
    "requested": 15,
    "available": 10
  }
}
```

**검증 오류** (400):
```json
{
  "error": "입력값이 유효하지 않습니다",
  "code": "VALIDATION_ERROR",
  "details": {
    "customer_email": "이메일 형식이 올바르지 않습니다"
  }
}
```

---

#### POST `/orders/{order_id}/verify-payment`

**요청**:
```json
{
  "paypal_order_id": "7RY12345678901234"
}
```

**성공 응답** (200):
```json
{
  "order_number": "ORD-A1B2C3D4",
  "order_status": "PAID",
  "paypal_transaction_id": "1234567890ABCDEF"
}
```

**타임아웃** (200, but VERIFICATION_PENDING):
```json
{
  "order_number": "ORD-A1B2C3D4",
  "order_status": "VERIFICATION_PENDING",
  "message": "결제 확인 중입니다. 잠시 후 다시 확인해주세요."
}
```

---

### 2.4 PayPal 통합 플로우

```
1. 사용자가 주문 정보 입력
   ↓
2. POST /orders 호출
   → 백엔드: PayPal Create Order API 호출
   → 응답: paypal_order_id
   ↓
3. 프론트엔드: PayPal JS SDK로 결제 창 표시
   ↓
4. 사용자가 PayPal에서 결제 완료
   ↓
5. POST /orders/{id}/verify-payment 호출
   → 백엔드: PayPal Capture Order API 호출
   → 성공 시: order_status = PAID, 재고 차감
   → 타임아웃 시: order_status = VERIFICATION_PENDING
```

**PayPal Sandbox 설정**:
```python
# .env
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com
```

---

### 2.5 재고 차감 로직

```python
def verify_payment_and_deduct_stock(order_id: int, paypal_order_id: str):
    """
    결제 검증 후 재고 차감
    """
    # 1. PayPal API로 결제 완료 확인
    try:
        paypal_response = capture_paypal_order(paypal_order_id)
    except PayPalTimeout:
        # 타임아웃 → VERIFICATION_PENDING
        execute_update(
            cursor, "orders",
            {"order_status": "VERIFICATION_PENDING"},
            {"id": order_id}
        )
        return {"status": "VERIFICATION_PENDING"}

    # 2. 결제 완료 확인
    if paypal_response['status'] != 'COMPLETED':
        execute_update(
            cursor, "orders",
            {"order_status": "PAYMENT_FAILED"},
            {"id": order_id}
        )
        return {"status": "PAYMENT_FAILED"}

    # 3. 트랜잭션으로 주문 상태 업데이트 + 재고 차감
    with db.transaction():
        # 주문 상태 업데이트
        execute_update(
            cursor, "orders",
            {
                "order_status": "PAID",
                "paypal_transaction_id": paypal_response['transaction_id']
            },
            {"id": order_id}
        )

        # 재고 차감
        cursor.execute("""
            UPDATE products
            SET stock = stock - ?
            WHERE id = (SELECT product_id FROM orders WHERE id = ?)
        """, (quantity, order_id))

        # 재고 음수 체크
        cursor.execute("""
            SELECT stock FROM products
            WHERE id = (SELECT product_id FROM orders WHERE id = ?)
        """, (order_id,))

        if cursor.fetchone()['stock'] < 0:
            raise InsufficientStock

    return {"status": "PAID"}
```

---

### 2.6 에러 처리

| 시나리오 | 처리 방법 |
|---------|---------|
| 재고 부족 (주문 생성 시) | 409, 현재 재고 수량 반환 |
| 입력 검증 실패 | 400, 필드별 에러 메시지 |
| PayPal API 타임아웃 | `VERIFICATION_PENDING`, 배치 작업으로 재시도 |
| PayPal 결제 실패 | `PAYMENT_FAILED`, 사용자에게 재시도 안내 |
| 재고 부족 (결제 검증 시) | 드물지만 가능. 환불 처리 + 안내 |

---

### 2.7 구현 체크리스트

#### 준비
- [ ] PayPal Sandbox 계정 생성
- [ ] Client ID/Secret 발급
- [ ] `.env`에 PayPal 키 설정

#### 개발 (Outside-In)
- [ ] **E2E 테스트 작성** (주문 생성 → 결제 → 재고 차감)
- [ ] POST `/orders` 엔드포인트 추가
- [ ] 입력 검증 로직 (`validators.py`)
- [ ] **검증 테스트 작성**
- [ ] PayPal Create Order API 통합
- [ ] **PayPal 통합 테스트 작성** (Mock)
- [ ] POST `/orders/{id}/verify-payment` 엔드포인트
- [ ] PayPal Capture Order API 통합
- [ ] 재고 차감 로직 (트랜잭션)
- [ ] **재고 차감 테스트 작성**
- [ ] 타임아웃 처리 로직
- [ ] **타임아웃 테스트 작성**
- [ ] 메인 랜딩페이지 HTML 작성
- [ ] PayPal JS SDK 통합
- [ ] 배치 작업 스크립트 (`retry_payments.py`)
- [ ] cron 설정

#### 검증
- [ ] 모든 테스트 통과
- [ ] PayPal Sandbox에서 실제 결제 테스트
- [ ] 재고 차감 확인 (DB 조회)
- [ ] 타임아웃 시나리오 테스트 (네트워크 끊기)
- [ ] 배치 작업 수동 실행 확인

---

## 2단계: 배송 추적

### 3.1 기능 범위

**목표**: 관리자가 배송 상태를 변경하고, 사용자가 배송 상태를 조회할 수 있다

**구현 범위**:
- `shipments` 테이블 생성
- 결제 완료 시 자동 shipment 생성 (`PREPARING`)
- GET `/orders/{order_number}` 응답에 배송 정보 추가
- PATCH `/admin/shipments/{shipment_id}` API (배송 상태 변경)
- 관리자 페이지 (`/admin/shipments`)

---

### 3.2 TDD 시나리오

#### E2E 테스트
```python
def test_admin_can_update_shipping_status():
    """
    관리자가 배송 상태를 변경할 수 있다

    Given: 결제 완료된 주문 (shipment PREPARING)
    When: PATCH /admin/shipments/{id} with status=SHIPPED
    Then: 배송 상태가 SHIPPED로 변경, shipped_at 기록
    """

def test_user_can_see_shipping_status():
    """
    사용자가 주문 조회 시 배송 상태를 볼 수 있다

    Given: 배송 중인 주문
    When: GET /orders/{order_number}
    Then: shipping_status=SHIPPED 포함
    """
```

---

### 3.3 API 명세

#### PATCH `/admin/shipments/{shipment_id}`

**요청 헤더**:
```
X-Admin-Key: secret-key-12345
```

**요청 바디**:
```json
{
  "shipping_status": "SHIPPED",
  "tracking_number": "1234567890",
  "courier": "CJ대한통운"
}
```

**성공 응답** (200):
```json
{
  "shipment_id": 1,
  "order_number": "ORD-A1B2C3D4",
  "shipping_status": "SHIPPED",
  "shipped_at": "2025-11-04T15:30:00"
}
```

**인증 실패** (401):
```json
{
  "error": "인증에 실패했습니다",
  "code": "UNAUTHORIZED"
}
```

---

### 3.4 관리자 페이지

**기능**:
- 주문 목록 표시 (PAID 상태만)
- 각 주문의 현재 배송 상태 표시
- 배송 상태 변경 버튼 (PREPARING → SHIPPED → DELIVERED)
- 송장번호, 택배사 입력 필드
- API 키 입력 (localStorage 저장)

---

### 3.5 구현 체크리스트

- [ ] `shipments` 테이블 생성
- [ ] 결제 완료 시 shipment 자동 생성 로직 추가
- [ ] PATCH `/admin/shipments/{id}` 엔드포인트
- [ ] 관리자 인증 미들웨어
- [ ] GET `/orders/{order_number}` 응답에 배송 정보 추가
- [ ] 관리자 페이지 HTML
- [ ] 모든 테스트 통과
- [ ] 수동 테스트 (배송 상태 변경 → 사용자 조회)

---

## 3단계: 환불 시스템

### 4.1 기능 범위

**목표**: 사용자가 환불 요청하고, 관리자가 승인하면 PayPal 환불이 처리된다

**구현 범위**:
- `refunds` 테이블 생성
- POST `/orders/{order_id}/refund` API (환불 요청)
- POST `/admin/refunds/{refund_id}/approve` API (환불 승인)
- POST `/admin/shipments/{shipment_id}/confirm-return` API (반송 확인)
- 배송 상태별 재고 복구 로직
- PayPal Refund API 통합
- 관리자 페이지 (`/admin/refunds`)
- 주문 조회 페이지에 환불 요청 버튼 추가

---

### 4.2 TDD 시나리오

#### E2E 테스트
```python
def test_user_requests_refund_and_admin_approves():
    """
    사용자가 환불 요청하고 관리자가 승인하면,
    PayPal 환불이 처리되고 재고가 복구된다

    Given: 결제 완료된 주문 (배송 PREPARING)
    When:
      1. POST /orders/{id}/refund (환불 요청)
      2. POST /admin/refunds/{id}/approve (관리자 승인)
    Then:
      - order_status = REFUNDED
      - refund_status = COMPLETED
      - 재고 복구 (PREPARING 상태라서 즉시)
      - PayPal에 환불 요청됨
    """

def test_delivered_order_refund_requires_return():
    """
    배송 완료 주문은 물품 반송 확인 후 재고 복구

    Given: 배송 완료된 주문
    When:
      1. 환불 요청 → 승인
      2. POST /admin/shipments/{id}/confirm-return (반송 확인)
    Then:
      - 재고 복구는 2단계에서만 실행
    """
```

---

### 4.3 API 명세

#### POST `/orders/{order_id}/refund`

**요청**:
```json
{
  "refund_reason": "상품이 손상되어 도착했습니다"
}
```

**성공 응답** (201):
```json
{
  "refund_id": 1,
  "order_number": "ORD-A1B2C3D4",
  "refund_status": "PENDING"
}
```

---

#### POST `/admin/refunds/{refund_id}/approve`

**요청 헤더**:
```
X-Admin-Key: secret-key-12345
```

**성공 응답** (200):
```json
{
  "refund_id": 1,
  "order_number": "ORD-A1B2C3D4",
  "refund_status": "COMPLETED",
  "paypal_refund_id": "REFUND123456",
  "stock_restored": true
}
```

---

#### POST `/admin/shipments/{shipment_id}/confirm-return`

**요청 헤더**:
```
X-Admin-Key: secret-key-12345
```

**성공 응답** (200):
```json
{
  "shipment_id": 1,
  "returned_at": "2025-11-05T10:00:00",
  "stock_restored": true
}
```

---

### 4.4 배송 상태별 재고 복구 로직

```python
def approve_refund(refund_id: int):
    """환불 승인 처리"""
    refund = get_refund(refund_id)
    order = get_order(refund.order_id)
    shipment = get_shipment(order.id)

    # 1. PayPal 환불 처리
    paypal_refund_id = process_paypal_refund(
        order.paypal_transaction_id,
        refund.refund_amount
    )

    # 2. 환불 상태 업데이트
    execute_update(
        cursor, "refunds",
        {
            "refund_status": "COMPLETED",
            "paypal_refund_id": paypal_refund_id
        },
        {"id": refund_id}
    )

    # 3. 주문 상태 업데이트
    execute_update(
        cursor, "orders",
        {"order_status": "REFUNDED"},
        {"id": order.id}
    )

    # 4. 배송 상태별 재고 복구
    if shipment.shipping_status in ["PREPARING", "SHIPPED"]:
        # 즉시 재고 복구
        restore_stock(order.product_id, order.quantity)
        return {"stock_restored": True}

    elif shipment.shipping_status == "DELIVERED":
        # 물품 반송 확인 후 복구 (별도 API 호출 필요)
        return {
            "stock_restored": False,
            "message": "물품 반송 확인 후 재고가 복구됩니다"
        }
```

---

### 4.5 PayPal 환불 통합

```python
import requests

def process_paypal_refund(transaction_id: str, amount: int):
    """PayPal Refund API 호출"""
    access_token = get_paypal_access_token()

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/payments/captures/{transaction_id}/refund",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": {
                "value": f"{amount / 100:.2f}",  # 센타보 → 페소
                "currency_code": "PHP"
            }
        }
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        raise PayPalRefundFailed(response.json())
```

---

### 4.6 관리자 페이지

**환불 관리 페이지** (`/admin/refunds`):
- 환불 요청 목록 표시 (PENDING 상태)
- 주문번호, 고객명, 환불 사유 표시
- 환불 승인 버튼 (confirm 후 처리)
- 배송 상태 표시 (DELIVERED면 "반송 확인 필요")

**배송 관리 페이지** (기존에 추가):
- 환불된 주문 중 DELIVERED 상태인 것 표시
- "반송 확인" 버튼 추가

---

### 4.7 구현 체크리스트

- [ ] `refunds` 테이블 생성
- [ ] `shipments.returned_at` 컬럼 추가
- [ ] POST `/orders/{id}/refund` 엔드포인트
- [ ] POST `/admin/refunds/{id}/approve` 엔드포인트
- [ ] POST `/admin/shipments/{id}/confirm-return` 엔드포인트
- [ ] PayPal Refund API 통합
- [ ] 배송 상태별 재고 복구 로직
- [ ] 주문 조회 페이지에 환불 요청 버튼 추가
- [ ] 관리자 환불 페이지 HTML
- [ ] 모든 테스트 통과
- [ ] PayPal Sandbox에서 환불 테스트
- [ ] 재고 복구 확인 (배송 상태별)

---

## 부록 A. 상태 전이 다이어그램

### 주문 상태 (order_status)
```
PAYMENT_PENDING
  ↓ (PayPal 결제 완료)
PAID
  ↓ (결제 검증 타임아웃)
VERIFICATION_PENDING → (재시도 성공) → PAID
  ↓ (재시도 실패)
PAYMENT_FAILED

PAID → (취소) → CANCELLED
PAID → (환불 완료) → REFUNDED
```

### 배송 상태 (shipping_status)
```
PREPARING (결제 완료 시 자동 생성)
  ↓ (관리자가 송장 입력 + 상태 변경)
SHIPPED
  ↓ (관리자가 배송 완료 처리)
DELIVERED
```

### 환불 상태 (refund_status)
```
PENDING (사용자 환불 요청)
  ↓ (관리자 승인)
COMPLETED
  ↓ (PayPal API 실패)
FAILED
```

---

## 부록 B. 에러 코드 전체 목록

| 코드 | HTTP | 설명 |
|-----|------|-----|
| `ORDER_NOT_FOUND` | 404 | 주문번호 없음 |
| `STOCK_INSUFFICIENT` | 409 | 재고 부족 |
| `VALIDATION_ERROR` | 400 | 입력 검증 실패 |
| `UNAUTHORIZED` | 401 | 관리자 인증 실패 |
| `PAYMENT_FAILED` | 400 | PayPal 결제 실패 |
| `REFUND_NOT_ALLOWED` | 400 | 환불 불가 상태 |
| `PAYPAL_TIMEOUT` | 500 | PayPal API 타임아웃 |
| `INTERNAL_ERROR` | 500 | 서버 내부 오류 |

---

## 부록 C. 배치 작업 (PayPal 검증 재시도)

**스크립트**: `scripts/retry_payments.py`

```python
import sqlite3
from datetime import datetime, timedelta
import os

def retry_pending_verifications():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 30분 이상 VERIFICATION_PENDING인 주문만 처리
    cursor.execute("""
        SELECT id, paypal_order_id, product_id, quantity
        FROM orders
        WHERE order_status = 'VERIFICATION_PENDING'
        AND created_at < ?
    """, (datetime.now() - timedelta(minutes=30),))

    for order_id, paypal_order_id, product_id, quantity in cursor.fetchall():
        try:
            # PayPal API로 결제 상태 확인
            result = verify_paypal_payment(paypal_order_id)

            if result['status'] == 'COMPLETED':
                # 트랜잭션으로 상태 업데이트 + 재고 차감
                with conn:
                    execute_update(cursor, "orders",
                        {
                            "order_status": "PAID",
                            "paypal_transaction_id": result['transaction_id']
                        },
                        {"id": order_id})

                    cursor.execute(
                        "UPDATE products SET stock = stock - ? WHERE id = ?",
                        (quantity, product_id)
                    )

                print(f"Order {order_id} verified and stock deducted")

            else:
                # 결제 실패
                execute_update(cursor, "orders",
                    {"order_status": "PAYMENT_FAILED"},
                    {"id": order_id})

                print(f"Order {order_id} marked as PAYMENT_FAILED")

        except Exception as e:
            print(f"Order {order_id} verification error: {e}")
            # 3회 재시도 후에도 실패하면 관리자 알림 필요

    conn.close()

if __name__ == "__main__":
    retry_pending_verifications()
```

**cron 설정**:
```bash
# crontab -e
*/5 * * * * cd /home/nadle/para/projects/practice-landing-page/scouting && uv run python scripts/retry_payments.py >> logs/retry_payments.log 2>&1
```

---

## 다음 단계

1. `OUTSIDE-IN-TDD-GUIDE.md` 읽고 TDD 학습
2. 1-b단계부터 시작
3. 각 단계마다 Red-Green-Refactor 사이클 준수
4. 모든 테스트가 통과한 후 다음 단계로 진행
