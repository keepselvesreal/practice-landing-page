---
version: 2
notes: "Google Cloud 플랫폼으로 변경 (Cloud Run, Firebase Hosting, SQLite + Cloud Storage 백업)"
created_date: 2025-10-28 22:19:00
---

## 1. 압축 내용

헥사고날 아키텍처로 구현된 K-뷰티 랜딩페이지 시스템 - 단일 제품 판매, PayPal 결제, 어필리에이트 추적, 이메일 알림 기능 제공

---

## 2. 핵심 내용

**아키텍처 패턴**
- Hexagonal Architecture (Ports & Adapters) 엄격 적용
- 모든 외부 의존성은 포트를 통해 추상화
- 도메인 로직과 인프라 계층 완전 분리

**핵심 컴포넌트**
- **Order Management**: 주문 생성/조회, 재고 관리, 주문 상태 추적
- **Payment Integration**: PayPal 결제 요청 및 Webhook 처리
- **Affiliate Tracking**: 어필리에이트 클릭 추적 및 판매 기록
- **Notification Service**: 주문 확인, 배송 시작, 재판매 알림 이메일 발송

✨(추가) **기술 스택**
- Backend: Python 3.11+, FastAPI, SQLAlchemy
- Frontend: 정적 HTML/CSS/JavaScript
- Database: SQLite (개발/MVP), PostgreSQL (확장 시)
- 호스팅: Cloud Run (백엔드), Firebase Hosting (프론트엔드)
- 외부 API: PayPal REST API, SMTP (Gmail)
- 백업: Google Cloud Storage (SQLite 자동 백업)

---

## 3. 상세 내용

### 📋 목차
- [시스템 구조](#시스템-구조)
- [컴포넌트 상세](#컴포넌트-상세)
- [데이터 설계](#데이터-설계)
- [품질 속성](#품질-속성)
- [배포 아키텍처](#배포-아키텍처)

---

### 시스템 구조

#### 전체 다이어그램

✨(수정)
```
┌─────────────────────────────────────────────────────────────┐
│                    External Systems                          │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Browser  │  │  PayPal  │  │   SMTP   │  │  Admin   │   │
│  │ (Customer│  │   API    │  │  Server  │  │   UI     │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        │ HTTP/HTTPS  │ Webhook     │ SMTP        │ HTTP Basic
        │             │             │             │
┌───────▼─────────────▼─────────────▼─────────────▼──────────┐
│                  Inbound Adapters                           │
│  ┌────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐     │
│  │   REST     │ │  PayPal  │ │  Email  │ │  Admin   │     │
│  │ Controller │ │  Webhook │ │ Adapter │ │ Controller│     │
│  └─────┬──────┘ └─────┬────┘ └────┬────┘ └─────┬────┘     │
└────────┼──────────────┼───────────┼────────────┼───────────┘
         │              │           │            │
         │              │           │            │
┌────────▼──────────────▼───────────▼────────────▼───────────┐
│                     Domain Layer                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │                  Use Cases                       │      │
│  │  - CreateOrderUseCase                            │      │
│  │  - ConfirmPaymentUseCase                         │      │
│  │  - UpdateShippingUseCase                         │      │
│  │  - TrackAffiliateClickUseCase                    │      │
│  │  - RecordAffiliateSaleUseCase                    │      │
│  │  - SendNotificationUseCase                       │      │
│  └──────────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │               Domain Entities                    │      │
│  │  - Order, Inventory, AffiliateCode               │      │
│  │  - AffiliateClick, AffiliateSale                 │      │
│  └──────────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │               Output Ports (Interfaces)          │      │
│  │  - SaveOrderPort, LoadOrderPort                  │      │
│  │  - DecreaseInventoryPort, IncreaseInventoryPort  │      │
│  │  - RequestPaymentPort, VerifyWebhookPort         │      │
│  │  - SendEmailPort, RecordClickPort                │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                 Outbound Adapters                           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐             │
│  │    SQL     │ │   PayPal   │ │    SMTP    │             │
│  │ Persistence│ │   Adapter  │ │   Adapter  │             │
│  │  Adapter   │ │            │ │            │             │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘             │
└────────┼──────────────┼──────────────┼─────────────────────┘
         │              │              │
    ┌────▼─────┐   ┌────▼──────┐  ┌───▼─────┐
    │  SQLite  │   │   PayPal  │  │  Gmail  │
    │    DB    │   │    API    │  │  SMTP   │
    └──────────┘   └───────────┘  └─────────┘
```

**런타임 흐름 (주문 생성):**
```
1. Customer → REST Controller (POST /orders)
2. REST Controller → CreateOrderUseCase
3. CreateOrderUseCase → DecreaseInventoryPort
4. DecreaseInventoryPort → SQL Persistence Adapter → SQLite DB
5. CreateOrderUseCase → SaveOrderPort
6. SaveOrderPort → SQL Persistence Adapter → SQLite DB
7. CreateOrderUseCase → RequestPaymentPort
8. RequestPaymentPort → PayPal Adapter → PayPal API
9. CreateOrderUseCase → REST Controller → Customer (결제 URL)
```

**런타임 흐름 (결제 완료):**
```
1. PayPal → PayPal Webhook Controller (POST /webhooks/paypal)
2. Webhook Controller → VerifyWebhookPort (서명 검증)
3. Webhook Controller → ConfirmPaymentUseCase
4. ConfirmPaymentUseCase → LoadOrderPort → SQLite DB
5. ConfirmPaymentUseCase → SaveOrderPort (상태 업데이트)
6. ConfirmPaymentUseCase → RecordAffiliateSaleUseCase
7. RecordAffiliateSaleUseCase → RecordSalePort → SQLite DB
8. ConfirmPaymentUseCase → SendNotificationUseCase
9. SendNotificationUseCase → SendEmailPort → SMTP Adapter → Gmail
```

**의존성 방향:**
```
Inbound Adapters → Use Cases → Domain Entities
                             → Output Ports ← Outbound Adapters
```
- **규칙**: 의존성은 항상 외부에서 내부로 (도메인 레이어는 외부 의존성 없음)
- **순환 의존**: 없음 (포트를 통한 의존성 역전)

---

#### 컴포넌트 목록

| 컴포넌트 | 책임 | 기술 스택 |
|----------|------|-----------|
| **Order Management** | 주문 생성/조회, 재고 관리, 주문 상태 추적 | Python, SQLAlchemy, SQLite |
| **Payment Integration** | PayPal 결제 요청, Webhook 처리, 결제 상태 확인 | Python, PayPal REST API |
| **Affiliate Tracking** | 클릭 추적, 판매 기록, 수수료 계산 | Python, SQLAlchemy |
| **Notification Service** | 주문 확인, 배송 시작, 재판매 알림 이메일 발송 | Python, SMTP (Gmail) |

---

#### 컴포넌트 간 관계

**통신 방식:**
- **동기 통신**: REST API (JSON over HTTP)
- **비동기 통신**:
  - PayPal Webhook (이벤트 기반)
  - 이메일 발송 (백그라운드 작업)
- **프로토콜**: HTTP/HTTPS, SMTP
- **데이터 형식**: JSON (API), HTML (이메일)

**의존성 규칙:**
- Order Management → Payment Integration (결제 요청)
- Order Management → Notification Service (이메일 발송)
- Payment Integration → Order Management (결제 완료 시 주문 확정)
- Affiliate Tracking → Order Management (주문 생성 시 어필리에이트 코드 기록)

**제약 사항:**
- 각 컴포넌트는 자신의 DB 테이블만 소유
- 다른 컴포넌트 데이터 접근은 포트를 통해서만 가능
- 직접 DB 접근 금지 (SQLAlchemy ORM 필수 사용)

---

### 컴포넌트 상세

#### Order Management

**책임 (Responsibility):**
- 주문 생성 및 저장
- 재고 확인 및 차감 (원자적 연산)
- 주문 상태 추적 (PENDING → PAID → SHIPPED → DELIVERED)
- 만료 주문 정리 (10분 경과 미결제 주문)
- 관리자 주문 조회 및 배송 처리

**경계 (Boundary):**

*담당하는 것:*
- 주문 데이터 CRUD
- 재고 수량 관리 (차감, 복구, 조회)
- 주문 상태 전이 로직
- 배송 정보 업데이트

*담당하지 않는 것:*
- 결제 처리 (Payment Integration에 위임)
- 이메일 발송 (Notification Service에 위임)
- 어필리에이트 수수료 계산 (Affiliate Tracking에 위임)

**통신 규칙:**

*제공하는 인터페이스:*
- `POST /orders` - 주문 생성
- `GET /orders/{order_id}` - 주문 조회
- `PATCH /admin/orders/{order_id}/shipping` - 배송 시작 (관리자)
- `PATCH /admin/orders/{order_id}/delivered` - 배송 완료 (관리자)

*사용하는 인터페이스:*
- `RequestPaymentPort` - PayPal 결제 URL 생성
- `SendEmailPort` - 주문 확인 이메일 발송

*데이터 접근:*
- 소유: `orders`, `inventory` 테이블
- 금지: `affiliate_*`, `restock_alerts` 테이블 직접 접근

**핵심 비즈니스 로직:**

1. **재고 원자적 차감 (초과 판매 방지):**
```python
UPDATE inventory
SET reserved_quantity = reserved_quantity + :qty
WHERE product_id = :pid
  AND (quantity - reserved_quantity) >= :qty
RETURNING quantity, reserved_quantity;
```

2. **주문 생성 트랜잭션:**
```python
# 트랜잭션 1: 재고 차감 + 주문 저장
with transaction_manager.begin():
    decrease_inventory_port.decrease_if_available(product_id, quantity)
    save_order_port.save(order)

# PayPal 요청 (트랜잭션 외부)
try:
    payment_url = request_payment_port.request(order)
except PayPalAPIError:
    # 보상 트랜잭션: 재고 복구
    increase_inventory_port.increase(product_id, quantity)
    save_order_port.update_status(order_id, "CANCELLED")
    raise PaymentRequestFailedError()
```

3. **만료 주문 정리 (배치 작업, 5분마다):**
```python
expired_orders = load_order_port.find_expired(minutes=10)
with transaction_manager.begin():
    for order in expired_orders:
        save_order_port.update_status(order.order_id, "EXPIRED")
        increase_inventory_port.increase(order.product_id, order.quantity)
```

---

#### Payment Integration

**책임 (Responsibility):**
- PayPal 결제 URL 생성
- PayPal Webhook 수신 및 서명 검증
- 결제 완료 시 주문 상태 업데이트
- 결제 실패 처리

**경계 (Boundary):**

*담당하는 것:*
- PayPal API 통신
- Webhook 서명 검증
- 결제 상태 확인

*담당하지 않는 것:*
- 주문 데이터 저장 (Order Management에 위임)
- 재고 관리 (Order Management에 위임)
- 이메일 발송 (Notification Service에 위임)

**통신 규칙:**

*제공하는 인터페이스:*
- `POST /webhooks/paypal` - PayPal Webhook 수신

*사용하는 인터페이스:*
- `LoadOrderPort` - 주문 조회
- `SaveOrderPort` - 주문 상태 업데이트
- `IncreaseInventoryPort` - 재고 복구 (실패 시)

*데이터 접근:*
- 소유: 없음 (외부 PayPal API만 사용)
- 읽기: `orders` 테이블 (포트를 통해)

**핵심 비즈니스 로직:**

1. **결제 URL 생성:**
```python
paypal_response = requests.post(
    f"{paypal_base_url}/v2/checkout/orders",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "PHP",
                "value": str(order.total_amount)
            },
            "reference_id": order.order_id
        }],
        "application_context": {
            "return_url": f"{frontend_url}/order/success",
            "cancel_url": f"{frontend_url}/order/cancel"
        }
    }
)

payment_url = next(
    link["href"] for link in paypal_response.json()["links"]
    if link["rel"] == "approve"
)
```

2. **Webhook 서명 검증:**
```python
verification_response = requests.post(
    f"{paypal_base_url}/v1/notifications/verify-webhook-signature",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "transmission_id": headers["paypal-transmission-id"],
        "transmission_sig": headers["paypal-transmission-sig"],
        "webhook_id": os.getenv("PAYPAL_WEBHOOK_ID"),
        "webhook_event": webhook_body
    }
)

if verification_response.json()["verification_status"] != "SUCCESS":
    raise InvalidWebhookSignatureError()
```

---

#### Affiliate Tracking

**책임 (Responsibility):**
- 어필리에이트 클릭 추적 (24시간 중복 방지)
- 판매 기록 생성
- 수수료 계산 (이윤의 20%)
- 인플루언서 성과 대시보드 조회

**경계 (Boundary):**

*담당하는 것:*
- 클릭 추적 데이터 저장
- 판매-어필리에이트 연결
- 수수료 계산 로직

*담당하지 않는 것:*
- 주문 생성 (Order Management에 위임)
- 수수료 지급 처리 (MVP 범위 외)

**통신 규칙:**

*제공하는 인터페이스:*
- `POST /affiliate/click` - 클릭 기록
- `GET /affiliate/stats/{code}` - 성과 조회

*사용하는 인터페이스:*
- `LoadInventoryPort` - 제품 이윤 조회 (수수료 계산용)

*데이터 접근:*
- 소유: `affiliate_codes`, `affiliate_clicks`, `affiliate_sales` 테이블
- 읽기: `inventory.profit_per_unit` (포트를 통해)

**핵심 비즈니스 로직:**

1. **중복 클릭 방지 (24시간 내):**
```python
existing_click = db.query(AffiliateClick).filter(
    AffiliateClick.affiliate_code == code,
    AffiliateClick.visitor_ip == ip,
    AffiliateClick.clicked_at > datetime.utcnow() - timedelta(hours=24)
).first()

if existing_click:
    return  # 중복 클릭 무시
```

2. **수수료 계산 (이윤 기준):**
```python
product = load_inventory_port.get(order.product_id)
commission_amount = (
    product.profit_per_unit * order.quantity * affiliate.commission_rate
)
# 예: ₱500 이윤 × 1개 × 0.20 = ₱100 수수료
```

---

#### Notification Service

**책임 (Responsibility):**
- 주문 확인 이메일 발송 (결제 완료 시)
- 배송 시작 이메일 발송 (운송장 번호 포함)
- 재판매 알림 이메일 발송 (배송 완료 시)
- 재판매 알림 신청 기록

**경계 (Boundary):**

*담당하는 것:*
- 이메일 템플릿 렌더링
- SMTP 발송 처리
- 재판매 알림 신청 데이터 저장

*담당하지 않는 것:*
- 주문 상태 관리 (Order Management에 위임)
- 이메일 발송 트리거 (다른 컴포넌트가 호출)

**통신 규칙:**

*제공하는 인터페이스:*
- `POST /restock-alerts/subscribe` - 재판매 알림 신청

*사용하는 인터페이스:*
- 없음 (다른 컴포넌트가 호출하는 방식)

*데이터 접근:*
- 소유: `restock_alerts`, `email_logs` 테이블

**핵심 비즈니스 로직:**

1. **이메일 템플릿 렌더링:**
```python
def render_template(template_name: str, data: dict) -> str:
    with open(f"templates/{template_name}") as f:
        template = f.read()
    return template.format(**data)

html_body = render_template(
    "order_confirmation.html",
    {
        "customer_name": order.customer_name,
        "order_id": order.order_id,
        "total_amount": f"₱{order.total_amount:,.2f}"
    }
)
```

2. **SMTP 발송:**
```python
msg = MIMEMultipart("alternative")
msg["From"] = "noreply@kbeauty.ph"
msg["To"] = order.email
msg["Subject"] = f"[K-Beauty Store] 주문이 확정되었습니다 #{order.order_id}"
msg.attach(MIMEText(html_body, "html"))

smtp = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
smtp.starttls()
smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
smtp.send_message(msg)
smtp.quit()
```

---

### 데이터 설계

#### 데이터 모델

**컴포넌트별 데이터 소유권:**

**Order Management 테이블:**

```python
# orders 테이블
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(String(36), primary_key=True)  # UUID
    customer_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=False)

    product_id = Column(String(36), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    paypal_order_id = Column(String(100), nullable=True)
    payment_confirmed_at = Column(DateTime, nullable=True)

    tracking_number = Column(String(100), nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    affiliate_code = Column(String(20), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_status_created_at', 'status', 'created_at'),
        Index('idx_email', 'email'),
        Index('idx_affiliate_code', 'affiliate_code'),
    )

# inventory 테이블
class Inventory(Base):
    __tablename__ = 'inventory'

    product_id = Column(String(36), primary_key=True)
    product_name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    profit_per_unit = Column(Float, nullable=False)  # 개당 이윤

    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)

    description = Column(String(1000), nullable=True)
    image_url = Column(String(500), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

**Affiliate Tracking 테이블:**

```python
# affiliate_codes 테이블
class AffiliateCode(Base):
    __tablename__ = 'affiliate_codes'

    code = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    commission_rate = Column(Float, default=0.20)  # 20%
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# affiliate_clicks 테이블
class AffiliateClick(Base):
    __tablename__ = 'affiliate_clicks'

    click_id = Column(String(36), primary_key=True)
    affiliate_code = Column(String(20), nullable=False)
    visitor_ip = Column(String(45), nullable=False)
    user_agent = Column(String(500), nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_affiliate_visitor', 'affiliate_code', 'visitor_ip', 'clicked_at'),
    )

# affiliate_sales 테이블
class AffiliateSale(Base):
    __tablename__ = 'affiliate_sales'

    sale_id = Column(String(36), primary_key=True)
    affiliate_code = Column(String(20), nullable=False)
    order_id = Column(String(36), nullable=False)

    sale_amount = Column(Float, nullable=False)
    commission_amount = Column(Float, nullable=False)
    commission_rate = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_affiliate_created', 'affiliate_code', 'created_at'),
        UniqueConstraint('order_id', name='uq_order_id'),
    )
```

**Notification Service 테이블:**

```python
# restock_alerts 테이블
class RestockAlert(Base):
    __tablename__ = 'restock_alerts'

    alert_id = Column(String(36), primary_key=True)
    email = Column(String(255), nullable=False)
    alert_type = Column(String(50), default='general')
    is_active = Column(Boolean, default=True)
    notified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_email_active', 'email', 'is_active'),
    )

# email_logs 테이블
class EmailLog(Base):
    __tablename__ = 'email_logs'

    log_id = Column(String(36), primary_key=True)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False)  # sent, failed
    error_message = Column(String(500), nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_status_sent_at', 'status', 'sent_at'),
    )
```

**데이터 소유권 원칙:**
- 한 테이블은 한 컴포넌트만 소유
- 다른 컴포넌트는 포트를 통해서만 접근
- 외래 키 사용 최소화 (느슨한 결합)

---

#### 데이터 플로우

**주요 비즈니스 플로우별 데이터 이동:**

**1. 주문 생성 플로우:**
```
Frontend (JSON)
  → CreateOrderUseCase
    → DecreaseInventoryPort
      → UPDATE inventory SET reserved_quantity = reserved_quantity + 1
    → SaveOrderPort
      → INSERT INTO orders
    → RequestPaymentPort
      → PayPal API (POST /v2/checkout/orders)
  → Frontend (payment_url)
```

**2. 결제 완료 플로우:**
```
PayPal Webhook (JSON)
  → VerifyWebhookPort (서명 검증)
  → ConfirmPaymentUseCase
    → LoadOrderPort
      → SELECT * FROM orders WHERE order_id = ?
    → SaveOrderPort
      → UPDATE orders SET status = 'PAID', quantity = quantity - 1
    → RecordAffiliateSaleUseCase
      → LoadInventoryPort (이윤 조회)
      → INSERT INTO affiliate_sales
    → SendNotificationUseCase
      → SendEmailPort (SMTP)
```

**3. 배송 처리 플로우:**
```
Admin API (JSON)
  → UpdateShippingUseCase
    → SaveOrderPort
      → UPDATE orders SET status = 'SHIPPED', tracking_number = ?
    → SendNotificationUseCase
      → SendEmailPort (배송 시작 이메일)

Admin API (배송 완료)
  → UpdateDeliveryUseCase
    → SaveOrderPort
      → UPDATE orders SET status = 'DELIVERED'
    → SendNotificationUseCase
      → SendEmailPort (재판매 알림 이메일)
```

**4. 만료 주문 정리 플로우:**
```
APScheduler (5분마다)
  → CleanupExpiredOrdersUseCase
    → LoadOrderPort
      → SELECT * FROM orders WHERE status = 'PENDING' AND created_at < NOW() - 10 minutes
    → SaveOrderPort
      → UPDATE orders SET status = 'EXPIRED'
    → IncreaseInventoryPort
      → UPDATE inventory SET reserved_quantity = reserved_quantity - ?
```

✨(추가) **SQLite 동시성 제어:**
- WAL (Write-Ahead Logging) 모드 활성화
- IMMEDIATE 트랜잭션 사용
- Busy timeout: 5초 설정
- 소규모 트래픽(~10 req/s)에 충분

✨(추가) **향후 확장 (PostgreSQL 전환 시점):**
- 동시 주문 >20개/초
- 복잡한 분석 쿼리 필요
- 다중 인스턴스 필요 시

**트랜잭션 경계:**
- DB 트랜잭션: 재고 차감 + 주문 저장 (원자성)
- 보상 트랜잭션: PayPal 실패 시 재고 복구
- 비동기 작업: 이메일 발송 (실패해도 롤백 안 함)

---

### 품질 속성

#### 보안 설계

**인증/인가:**
- **관리자 인증**: HTTP Basic Authentication
  - 환경 변수로 credential 관리
  - `secrets.compare_digest()` 사용 (타이밍 공격 방지)
  - HTTPS 필수
- **고객 인증**: 없음 (비회원 구매)
- **향후 확장**: JWT 토큰, OAuth 2.0

```python
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv("ADMIN_USERNAME")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv("ADMIN_PASSWORD")
    )
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)
    return credentials.username
```

**데이터 보호:**
- **전송 계층**: HTTPS/TLS (Cloud Run + Firebase Hosting 자동 SSL)
- **저장 데이터**: 평문 저장 (MVP 단순화)
  - 이메일: 평문 (발송 필요)
  - 전화번호: 평문 (배송 연락)
  - 주소: 평문 (배송지)
- **환경 변수**: Google Secret Manager (암호화 저장)
- **향후 확장**: AES-256 암호화 (개인정보), bcrypt 해싱 (비밀번호)

**API 보안:**
- **Rate Limiting**: slowapi 사용
  - `POST /orders`: 5/분 (스팸 방지)
  - `POST /admin/login`: 3/분 (Brute Force 방지)
  - `POST /restock-alerts/subscribe`: 10/분
- **CORS 정책**: 특정 도메인만 허용
  ```python
  allowed_origins = [
      "https://kbeauty.ph",
      "https://www.kbeauty.ph"
  ]
  ```
- **Input Validation**: Pydantic 자동 검증
  - 타입 체크, 이메일 형식, 필수 필드
  - 특수문자 필터링 (XSS 방지)
  - SQL Injection 방지 (SQLAlchemy ORM)
- **PayPal Webhook 검증**: 서명 확인 필수

---

#### 확장성/성능 전략

✨(추가) **Cloud Run 자동 확장:**
- 최소 인스턴스: 0 (트래픽 없으면 비용 $0)
- 최대 인스턴스: 10
- 동시성: 인스턴스당 80 요청
- Cold Start: 1-3초 (개발 단계 허용)

**캐싱 전략 (향후):**
| 데이터 | 캐싱 방식 | TTL | 이유 |
|--------|---------|-----|------|
| 제품 정보 | Redis | 5분 | 변경 빈도 낮음 |
| 어필리에이트 코드 | Redis | 1시간 | 거의 변경 안 됨 |
| 재고 수량 | ❌ 캐싱 안 함 | - | 실시간 정확성 필수 |
| 주문 정보 | ❌ 캐싱 안 함 | - | 실시간 정확성 필수 |

✨(수정) **성능 목표 (SQLite 기준):**
| 엔드포인트 | 목표 | 측정 방법 |
|-----------|------|----------|
| `GET /products/{id}` | <100ms | DB 조회 |
| `POST /orders` | <500ms | DB + PayPal API |
| `POST /webhooks/paypal` | <300ms | DB + 이메일 비동기 |

**동시 접속자 처리:**
- MVP: 10 req/s (SQLite + Cloud Run 기본)
- 확장 후: 100 req/s (PostgreSQL + 다중 인스턴스)

**DB 쿼리 최적화:**
- **인덱스**: `idx_status_created_at`, `idx_email`, `idx_affiliate_code`
- **N+1 방지**: `joinedload()` 사용
- **Bulk Insert**: `bulk_insert_mappings()` 사용
- **Connection Pool**: pool_size=5, max_overflow=10

**네트워크 최적화:**
- **CDN**: Firebase Hosting (전 세계 엣지 서버)
- **Gzip 압축**: JSON 응답 70% 감소
- **HTTP/2**: Cloud Run + Firebase 자동 지원
- **이미지 최적화**: srcset, lazy loading

**비동기 처리 (향후):**
- 이메일 발송: BackgroundTasks 또는 Celery
- 배치 작업: APScheduler

---

### 배포 아키텍처

#### 인프라 구성

✨(수정) **전체 아키텍처:**
```
Internet
    │
    ├── Firebase Hosting (CDN)
    │   └── Static Files (HTML/CSS/JS)
    │
    └── Google Cloud Platform
        ├── Cloud Run (서버리스)
        │   ├── FastAPI Backend
        │   ├── Order Management
        │   ├── Payment Integration
        │   ├── Affiliate Tracking
        │   └── Notification Service
        ├── Cloud Storage
        │   └── SQLite 백업 (자동 백업)
        └── Secret Manager
            └── 환경 변수 (PayPal, SMTP)

External APIs:
    ├── PayPal API
    └── Gmail SMTP
```

✨(수정) **네트워크 구성:**
- 프론트엔드: `https://kbeauty.ph` (Firebase Hosting)
- 백엔드 API: `https://api.kbeauty.ph` (Cloud Run)
- SSL/TLS: 자동 인증서 (Firebase + Cloud Run)
- DNS: Firebase Hosting 자동 설정

---

#### 환경 구성

✨(수정)
| 환경 | 용도 | 배포 방식 | URL | 특이사항 |
|------|------|-----------|-----|----------|
| Development | 로컬 개발 | 수동 실행 | `localhost:8000` | SQLite 로컬, PayPal Sandbox |
| Production | 실서비스 | Git push (main) → Cloud Run | `api.kbeauty.ph` | SQLite + Cloud Storage 백업, PayPal Live |

✨(수정) **환경 변수 관리:**
- Development: `.env` 파일 (gitignore)
- Production: Google Secret Manager

---

#### 배포 전략

✨(수정) **Cloud Run 자동 배포:**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# DB 마이그레이션
RUN alembic upgrade head

# Cloud Run PORT 환경변수 사용
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

✨(추가) **배포 프로세스:**
```
1. 로컬 테스트 (`pytest tests/`)
2. Git push (main 브랜치)
3. Cloud Build 자동 트리거 → 이미지 빌드
4. Cloud Run 자동 배포 (Zero Downtime)
5. Health Check (`curl https://api.kbeauty.ph/health`)
```

✨(추가) **Firebase Hosting 배포:**
```bash
# firebase.json 설정
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
  }
}

# 배포 명령어
firebase deploy --only hosting
```

✨(수정) **롤백 계획:**
- Cloud Run: 이전 리비전으로 트래픽 전환 (콘솔 클릭)
- Firebase: `firebase hosting:rollback`
- 롤백 시간: <2분

**다운타임 최소화:**
- Cloud Run Zero Downtime Deployment (새 리비전 준비 → 트래픽 전환)
- Health Check (`/health` 200 OK 확인)
- Graceful Shutdown (SIGTERM 처리)

---

#### 모니터링 및 로깅

✨(수정) **Google Cloud Monitoring:**
- Cloud Run 메트릭: 요청 수, 응답 시간, 에러율
- 인스턴스 수, Cold Start 빈도
- 알림: 에러율 >1%, 응답 시간 >1s

✨(수정) **Cloud Logging:**
- 구조화된 로깅 (JSON)
- 로그 레벨: INFO (운영)
- 슬로우 쿼리: >100ms

✨(추가) **비용 모니터링:**
- Budget Alert: $10/월 초과 시 알림
- 예상 비용: $0-5/월 (무료 크레딧 범위)

---

#### 백업 및 복구

✨(수정) **백업 대상:**
- SQLite DB (매일 02:00 자동 → Cloud Storage)
- 환경 변수 (Secret Manager - 자동 버전 관리)
- 코드베이스 (Git Repository)

✨(추가) **자동 백업 설정:**
```python
# Cloud Scheduler + Cloud Functions
def backup_sqlite():
    """매일 SQLite DB를 Cloud Storage에 백업"""
    storage_client = storage.Client()
    bucket = storage_client.bucket('kbeauty-backups')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    blob = bucket.blob(f'sqlite/database_{timestamp}.db')
    blob.upload_from_filename('/app/data/database.db')

    # 30일 이상 백업 자동 삭제
    lifecycle_rule = {
        'action': {'type': 'Delete'},
        'condition': {'age': 30}
    }
    bucket.lifecycle_rules = [lifecycle_rule]
    bucket.patch()
```

✨(수정) **복구 절차:**
```
1. Cloud Storage에서 최신 SQLite 파일 다운로드
2. Cloud Run 재배포 시 백업 파일 포함
3. Health Check 확인
→ 복구 시간: <10분
```

✨(수정) **목표:**
- RTO (Recovery Time Objective): <10분
- RPO (Recovery Point Objective): <24시간

---

## 작성 원칙

1. **컴포넌트 경계 명확화**: 책임과 경계를 명시하여 Epic 분해 기준 제공
2. **기술 결정 근거**: 모든 주요 기술 선택에 대한 이유 명시
3. **데이터 소유권**: 각 컴포넌트가 소유하는 데이터 명확히 정의
4. **확장 가능성**: 초기 설계부터 확장성 고려
5. **보안 우선**: 보안은 설계 단계부터 고려
6. **다이어그램 활용**: 텍스트보다 다이어그램으로 구조 표현
7. **실행 가능성**: 이 문서만으로 구현 시작 가능해야 함
