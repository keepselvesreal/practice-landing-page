---
created_at: 2025-10-10 00:00:00
links:
   - ./index.md
   - ./concept_tdd.md
   - ./eval_tdd_application_v1.md
---

# 4. TDD 적용 가이드

**TDD 프로세스**:
1. **Red**: 실패하는 테스트 작성
2. **Green**: 최소 구현으로 테스트 통과
3. **Refactor**: 코드 개선

**Outside-in 접근** (GOOS 방식):
- UI 테스트부터 시작 → 도메인으로 내려감
- 사용자 관점에서 시작 → 기술 구현으로 진행

---

## 4.1 Walking Skeleton 구축 (Epic 1)

**목표**: 브라우저부터 데이터베이스까지 전체 흐름을 관통하는 최소 기능 구현

**GOOS 원칙** (Chapter 10-11):
- Walking Skeleton은 "UI → API → Domain → DB" 전체를 의미
- 가장 얇은 기능 조각 (thinnest slice)을 End-to-End로 구현
- 외부에서 내부로 (Outside-in) 진행

**참조**: GOOS p.63-88 "The Walking Skeleton"

---

### 4.1.1 Phase 1: UI Walking Skeleton

**목표**: 사용자가 브라우저에서 주문 폼을 제출하고 성공 메시지를 받는 end-to-end 흐름 구축

**출처**: GOOS Chapter 10-11 (p.63-88)

#### Step 1: 인수 테스트 작성 (UI 레벨)

**GOOS 원칙**: Outside-in 개발 - 사용자 시나리오부터 시작

```python
# tests/integration/end_to_end/test_order_form_ui.py
"""
UI 인수 테스트: 사용자 주문 폼 제출 시나리오
GOOS Chapter 11: First End-to-End Test
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestOrderFormUI:
    """
    브라우저 레벨 인수 테스트

    GOOS: 사용자 관점에서 전체 시스템 동작 검증
    """

    def test_user_can_submit_order_form(self, selenium_driver, live_server):
        """
        인수 테스트: 사용자가 주문 폼을 작성하고 제출할 수 있다

        GOOS: Outside-in, 사용자 시나리오부터 시작
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 주문 폼 작성
        selenium_driver.find_element(By.ID, "customer_email").send_keys("test@example.com")
        selenium_driver.find_element(By.ID, "customer_address").send_keys("123 Main St")
        selenium_driver.find_element(By.ID, "product_price").send_keys("29.99")
        selenium_driver.find_element(By.ID, "submit_order").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 5)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "주문이 완료되었습니다" in success_msg.text


# Pytest Fixtures
@pytest.fixture
def selenium_driver():
    """Selenium WebDriver 설정"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def live_server():
    """테스트용 라이브 서버"""
    return "http://localhost:8000"
```

**핵심 포인트**:
- ✅ **사용자 관점**: 실제 브라우저에서 동작 검증
- ✅ **End-to-End**: UI → API → Domain → DB 전체 흐름
- ✅ **실패 시작**: 이 테스트는 아직 실패 (구현 전)

#### Step 2: UI 컴포넌트 구현 (TDD)

**목표**: 인수 테스트를 통과시키기 위한 최소 UI 구현

```html
<!-- templates/landing.html (주문 폼 추가) -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>화장품 주문 - Walking Skeleton</title>
    <style>
        .hidden { display: none; }
        .success-message { color: green; }
        .error-message { color: red; }
    </style>
</head>
<body>
    <h1>화장품 주문</h1>

    <form id="orderForm">
        <div>
            <label for="customer_email">이메일:</label>
            <input type="email" id="customer_email" required>
        </div>
        <div>
            <label for="customer_address">주소:</label>
            <input type="text" id="customer_address" required>
        </div>
        <div>
            <label for="product_price">가격:</label>
            <input type="number" id="product_price" step="0.01" required>
        </div>
        <button type="submit" id="submit_order">주문하기</button>
    </form>

    <div id="message" class="hidden"></div>

    <script>
    document.getElementById('orderForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            customer_email: document.getElementById('customer_email').value,
            customer_address: document.getElementById('customer_address').value,
            product_price: parseFloat(document.getElementById('product_price').value)
        };

        try {
            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });

            const result = await response.json();
            const messageEl = document.getElementById('message');

            if (response.ok) {
                messageEl.textContent = '주문이 완료되었습니다';
                messageEl.className = 'success-message';
                document.getElementById('orderForm').reset();
            } else {
                messageEl.textContent = result.detail || '주문 실패';
                messageEl.className = 'error-message';
            }
        } catch (error) {
            const messageEl = document.getElementById('message');
            messageEl.textContent = '네트워크 오류';
            messageEl.className = 'error-message';
        }
    });
    </script>
</body>
</html>
```

**TDD 사이클**:
1. ❌ **Red**: 인수 테스트 실패 (폼 요소 없음)
2. ✅ **Green**: HTML 폼 추가로 테스트 통과
3. 🔄 **Refactor**: 스타일 개선 (다음 단계)

#### Step 3: API 엔드포인트 스텁 구현

**목표**: UI 테스트를 통과시키기 위한 최소 API 구현

```python
# config/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path


class OrderRequest(BaseModel):
    """임시 주문 요청 모델 (Walking Skeleton용)"""
    customer_email: str
    customer_address: str
    product_price: float


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/", response_class=HTMLResponse)
    async def landing_page():
        """
        랜딩 페이지 서빙

        Walking Skeleton: 사용자가 실제로 보는 화면
        """
        template_path = Path("templates/landing.html")
        return HTMLResponse(content=template_path.read_text())

    @app.post("/api/orders")
    async def create_order(request: OrderRequest):
        """
        주문 생성 API 스텁

        Walking Skeleton: UI 테스트 통과를 위한 최소 구현
        실제 비즈니스 로직은 아직 없음 (다음 단계에서 추가)
        """
        # TODO: 실제 도메인 로직 구현 (Phase 2)
        return {
            "order_id": 1,  # 하드코딩된 임시 값
            "status": "success"
        }

    @app.get("/health")
    async def health_check():
        """헬스 체크"""
        return {"status": "healthy"}

    return app
```

**TDD 사이클**:
1. ❌ **Red**: 인수 테스트 실패 (`/api/orders` 없음)
2. ✅ **Green**: 스텁 엔드포인트 추가로 테스트 통과
3. 🔄 **Refactor**: 실제 비즈니스 로직 추가 (Phase 2)

**핵심 포인트**:
- ✅ **End-to-End 동작**: 브라우저 → API → 응답 전체 흐름 작동
- ✅ **Walking Skeleton 완성**: UI부터 API까지 최소 기능 구현
- ❌ **비즈니스 로직 없음**: 하드코딩된 응답만 반환 (의도적)

#### Step 4: 테스트 실행 및 검증

**테스트 실행**:
```bash
# 1. 필요 패키지 설치
uv add --dev selenium webdriver-manager

# 2. 인수 테스트 실행
uv run pytest tests/integration/end_to_end/test_order_form_ui.py -v

# 3. 서버 수동 실행 및 브라우저 확인
uv run uvicorn cosmetics_landing.config.main:app --reload
# 브라우저: http://localhost:8000
```

**검증 체크리스트**:
- ✅ 인수 테스트 통과 (`test_user_can_submit_order_form`)
- ✅ 브라우저에서 주문 폼 표시 확인
- ✅ 폼 제출 시 성공 메시지 표시
- ✅ 전체 UI → API 흐름 작동

**Walking Skeleton 완성 확인**:
- ✅ **UI Layer**: HTML 폼 + JavaScript
- ✅ **API Layer**: FastAPI 엔드포인트
- ✅ **End-to-End**: 브라우저 → API 전체 흐름
- ❌ **비즈니스 로직**: 아직 없음 (다음 단계에서 추가)

---

### 4.1.2 Phase 2: API End-to-End 테스트 작성

**목표**: API 레벨에서 주문 생성 흐름 검증

**출처**: Chapter 4, 5 - Use Case 구현

```python
# tests/integration/end_to_end/test_place_order_e2e.py
import pytest
from fastapi.testclient import TestClient

def test_customer_can_place_order(client: TestClient):
    """
    E2E 테스트: 고객이 주문을 생성하고 결제할 수 있다
    (Chapter 4, 5: Walking Skeleton)
    """
    # Given: 주문 요청 데이터
    order_request = {
        "customer_email": "customer@example.com",
        "customer_address": "123 Main St, Manila",
        "product_price": 29.99
    }

    # When: 주문 생성 API 호출
    response = client.post("/api/order", json=order_request)

    # Then: 주문이 성공적으로 생성됨
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["status"] == "success"
```

**핵심**: 실패하는 E2E 테스트부터 시작 → 계층별 구현 → 테스트 통과

### 4.1.3 Phase 3: 도메인 계층 TDD

```python
# tests/unit/domain/test_order.py
import pytest
from decimal import Decimal
from domain.order import Order, Money

def test_creates_new_order_with_pending_status():
    """새 주문은 pending 상태로 생성된다"""
    # Given
    order = Order.create_new(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99"))
    )

    # Then
    assert order.payment_status == "pending"
    assert order.id is None

def test_marks_order_as_paid():
    """주문을 결제 완료 상태로 변경할 수 있다"""
    # Given
    order = Order.create_new(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99"))
    )

    # When
    paid_order = order.mark_as_paid()

    # Then
    assert paid_order.payment_status == "completed"
    assert paid_order.is_paid()
```

**TDD 사이클**:
1. ❌ 실패: `Order` 클래스 없음
2. ✅ 통과: 최소 구현 (dataclass + 메서드)
3. 🔄 리팩토링: 불변성 추가 (`frozen=True`)

### 4.1.4 Phase 4: 애플리케이션 계층 TDD

```python
# tests/unit/application/test_place_order_service.py
import pytest
from unittest.mock import Mock
from decimal import Decimal

from application.service.place_order_service import PlaceOrderService
from application.port.in_.place_order_use_case import PlaceOrderCommand
from domain.order import Order, OrderId, Money

def test_place_order_validates_address():
    """주문 생성 시 주소를 검증한다 (Chapter 4: Business Rule Validation)"""
    # Given: Mock 의존성
    save_order = Mock()
    process_payment = Mock()
    validate_address = Mock()
    validate_address.is_valid.return_value = False  # 잘못된 주소

    service = PlaceOrderService(
        save_order_port=save_order,
        process_payment_port=process_payment,
        validate_address_port=validate_address,
        load_affiliate_port=Mock(),
        save_affiliate_port=Mock()
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="Invalid Address",
        product_price=Decimal("29.99"),
        affiliate_code=None
    )

    # When/Then: 잘못된 주소로 예외 발생
    with pytest.raises(ValueError, match="Invalid address"):
        service.place_order(command)

def test_place_order_processes_payment():
    """주문 생성 시 결제를 처리한다"""
    # Given
    save_order = Mock()
    save_order.save.return_value = OrderId(value=1)

    process_payment = Mock()
    process_payment.process_payment.return_value = PaymentResult(
        success=True,
        transaction_id="txn_123",
        error_message=None
    )

    validate_address = Mock()
    validate_address.is_valid.return_value = True

    service = PlaceOrderService(
        save_order_port=save_order,
        process_payment_port=process_payment,
        validate_address_port=validate_address,
        load_affiliate_port=Mock(),
        save_affiliate_port=Mock()
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Decimal("29.99"),
        affiliate_code=None
    )

    # When
    order_id = service.place_order(command)

    # Then
    assert order_id.value == 1
    process_payment.process_payment.assert_called_once()
```

**Mock 사용 원칙** (Chapter 8):
- **외부 의존성은 Mock 처리**: PayPal, Google Places API
- **도메인 로직은 실제 객체 사용**: `Order`, `Money`

### 4.1.5 Phase 5: 어댑터 계층 통합 테스트

```python
# tests/integration/adapter/test_paypal_adapter.py
import pytest
from adapter.out.payment.paypal_adapter import PayPalAdapter
from domain.order import Order, Money, OrderId

@pytest.mark.integration
def test_paypal_adapter_processes_payment(paypal_sandbox_credentials):
    """PayPal 어댑터가 실제 결제를 처리할 수 있다 (Chapter 8: Third-Party Integration)"""
    # Given
    adapter = PayPalAdapter(
        client_id=paypal_sandbox_credentials["client_id"],
        client_secret=paypal_sandbox_credentials["client_secret"],
        mode="sandbox"
    )

    order = Order(
        id=OrderId(value=1),
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99")),
        affiliate_code=None,
        created_at=datetime.now(),
        payment_status="pending"
    )

    # When
    result = adapter.process_payment(order)

    # Then
    assert result.success
    assert result.transaction_id is not None
```

**통합 테스트 전략** (Chapter 7):
- **단위 테스트**: Mock 사용, 빠른 피드백
- **통합 테스트**: 실제 외부 서비스 (Sandbox), 느리지만 신뢰성 확보

---

## 4.2 Epic 2: 어필리에이트 기능 TDD

### 4.2.1 도메인 계층: Affiliate 엔티티

```python
# tests/unit/domain/test_affiliate.py
from domain.affiliate import Affiliate
from domain.commission import Commission
from domain.order import Money
from decimal import Decimal

def test_affiliate_records_click():
    """어필리에이트 클릭을 기록한다"""
    # Given
    affiliate = Affiliate.create_new(code="INFLUENCER123")

    # When
    updated = affiliate.record_click()

    # Then
    assert updated.total_clicks == 1

def test_affiliate_records_sale_with_commission():
    """판매와 수수료를 함께 기록한다"""
    # Given
    affiliate = Affiliate.create_new(code="INFLUENCER123")
    commission = Money.of(Decimal("5.00"))

    # When
    updated = affiliate.record_sale(commission)

    # Then
    assert updated.total_sales == 1
    assert updated.total_commission.amount == Decimal("5.00")
    assert updated.pending_commission.amount == Decimal("5.00")

def test_commission_calculates_20_percent():
    """수수료는 주문 금액의 20%이다"""
    # Given
    commission = Commission()
    order_amount = Money.of(Decimal("100.00"))

    # When
    result = commission.calculate(order_amount)

    # Then
    assert result.amount == Decimal("20.00")
```

### 4.2.2 애플리케이션 계층: 어필리에이트 추적

```python
# tests/unit/application/test_track_affiliate_service.py
from application.service.track_affiliate_service import TrackAffiliateService
from application.port.in_.track_affiliate_use_case import TrackAffiliateCommand

def test_track_click_increments_counter():
    """클릭 추적 시 카운터가 증가한다"""
    # Given
    load_affiliate = Mock()
    load_affiliate.load_by_code.return_value = Affiliate.create_new("INFLUENCER123")

    save_affiliate = Mock()

    service = TrackAffiliateService(
        load_affiliate_port=load_affiliate,
        save_affiliate_port=save_affiliate
    )

    command = TrackAffiliateCommand(affiliate_code="INFLUENCER123")

    # When
    service.track_click(command)

    # Then
    saved_affiliate = save_affiliate.save.call_args[0][0]
    assert saved_affiliate.total_clicks == 1

def test_place_order_records_affiliate_sale():
    """어필리에이트 코드가 있는 주문은 판매를 기록한다 (Chapter 4: Use Case Composition)"""
    # Given
    affiliate = Affiliate.create_new("INFLUENCER123")

    load_affiliate = Mock()
    load_affiliate.load_by_code.return_value = affiliate

    save_affiliate = Mock()

    service = PlaceOrderService(
        save_order_port=Mock(save=Mock(return_value=OrderId(1))),
        process_payment_port=Mock(process_payment=Mock(return_value=PaymentResult(True, "txn", None))),
        validate_address_port=Mock(is_valid=Mock(return_value=True)),
        load_affiliate_port=load_affiliate,
        save_affiliate_port=save_affiliate
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Decimal("100.00"),
        affiliate_code="INFLUENCER123"
    )

    # When
    service.place_order(command)

    # Then
    saved_affiliate = save_affiliate.save.call_args[0][0]
    assert saved_affiliate.total_sales == 1
    assert saved_affiliate.total_commission.amount == Decimal("20.00")  # 20%
```

---

## 4.3 Epic 3: 고객 문의 기능 TDD

### 4.3.1 애플리케이션 계층: 문의 전송

```python
# tests/unit/application/test_send_inquiry_service.py
from application.service.send_inquiry_service import SendInquiryService
from application.port.in_.send_inquiry_use_case import SendInquiryCommand

def test_sends_inquiry_email():
    """문의 내용을 이메일로 전송한다"""
    # Given
    email_sender = Mock()
    email_sender.send.return_value = True

    service = SendInquiryService(email_sender_port=email_sender)

    command = SendInquiryCommand(
        customer_email="customer@example.com",
        message="When will my order arrive?"
    )

    # When
    result = service.send_inquiry(command)

    # Then
    assert result is True
    email_sender.send.assert_called_once()
    sent_email = email_sender.send.call_args[0][0]
    assert "customer@example.com" in sent_email.from_address
    assert "When will my order arrive?" in sent_email.body
```

### 4.3.2 어댑터 계층: Gmail SMTP

```python
# tests/integration/adapter/test_gmail_smtp_adapter.py
@pytest.mark.integration
def test_gmail_smtp_sends_email(gmail_credentials):
    """Gmail SMTP 어댑터가 실제 이메일을 전송한다 (Chapter 8)"""
    # Given
    adapter = GmailSmtpAdapter(
        smtp_server="smtp.gmail.com",
        port=587,
        username=gmail_credentials["username"],
        password=gmail_credentials["password"]
    )

    email = Email(
        from_address="customer@example.com",
        to_address="support@cosmetics.com",
        subject="Product Inquiry",
        body="When will my order arrive?"
    )

    # When
    result = adapter.send(email)

    # Then
    assert result is True
```

---

## 4.4 TDD 모범 사례 정리

### 4.4.1 Test Data Builder 패턴 활용

```python
# tests/builders.py
class OrderBuilder:
    """주문 테스트 데이터 빌더 (Chapter 22: Test Data Builder)"""

    def __init__(self):
        self.id = None
        self.customer_email = "test@example.com"
        self.customer_address = "123 Main St"
        self.product_price = Money.of(Decimal("29.99"))
        self.affiliate_code = None
        self.created_at = datetime.now()
        self.payment_status = "pending"

    @classmethod
    def an_order(cls):
        return cls()

    def with_id(self, order_id: int):
        self.id = OrderId(value=order_id)
        return self

    def with_affiliate_code(self, code: str):
        self.affiliate_code = code
        return self

    def paid(self):
        self.payment_status = "completed"
        return self

    def build(self) -> Order:
        return Order(
            id=self.id,
            customer_email=self.customer_email,
            customer_address=self.customer_address,
            product_price=self.product_price,
            affiliate_code=self.affiliate_code,
            created_at=self.created_at,
            payment_status=self.payment_status
        )

# 사용 예
def test_paid_order():
    order = OrderBuilder.an_order() \
        .with_id(1) \
        .with_affiliate_code("INFLUENCER123") \
        .paid() \
        .build()

    assert order.is_paid()
```

### 4.4.2 테스트 진단성 향상

```python
# tests/helpers.py
class NamedMoney(Money):
    """자가 설명 Money 값 객체 (Chapter 23: Self-Describing Values)"""

    def __init__(self, amount: Decimal, name: str):
        super().__init__(amount)
        self._name = name

    def __repr__(self):
        return f"{self._name}({self.amount})"

# 사용
STANDARD_PRICE = NamedMoney(Decimal("29.99"), "STANDARD_PRICE")
VIP_DISCOUNT = NamedMoney(Decimal("5.00"), "VIP_DISCOUNT")

def test_calculates_total():
    order = OrderBuilder.an_order() \
        .with_price(STANDARD_PRICE) \
        .build()

    # 실패 시: "Expected STANDARD_PRICE(29.99), got VIP_DISCOUNT(5.00)"
```

### 4.4.3 포트 슬라이싱으로 테스트 단순화

```python
# Chapter 6: 포트 인터페이스 슬라이싱
# ❌ 나쁜 예: 거대한 Repository
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

    @abstractmethod
    def find_by_id(self, id: OrderId) -> Order: pass

    @abstractmethod
    def find_by_email(self, email: str) -> List[Order]: pass

    @abstractmethod
    def find_by_affiliate(self, code: str) -> List[Order]: pass

# ✅ 좋은 예: 슬라이싱된 포트
class SaveOrderPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

class LoadOrderPort(ABC):
    @abstractmethod
    def load_by_id(self, id: OrderId) -> Order: pass

# 테스트에서는 필요한 포트만 Mock
def test_place_order():
    service = PlaceOrderService(
        save_order_port=Mock(),  # SaveOrderPort만 필요
        # ... 다른 포트들
    )
```

### 4.4.4 계층별 테스트 전략

| 계층 | 테스트 타입 | Mock 사용 | 검증 대상 |
|------|------------|-----------|-----------|
| **Domain** | 단위 테스트 | ❌ 없음 | 비즈니스 규칙 |
| **Application** | 단위 테스트 | ✅ 포트 Mock | Use Case 로직 |
| **Adapter (Web)** | 통합 테스트 | ✅ Use Case Mock | HTTP 매핑 |
| **Adapter (Persistence)** | 통합 테스트 | ❌ 실제 DB (TestContainer) | 영속성 로직 |
| **Adapter (External)** | 통합 테스트 | ❌ Sandbox 환경 | 외부 연동 |
| **End-to-End** | 시스템 테스트 | ❌ 실제 환경 (Staging) | 전체 흐름 |
