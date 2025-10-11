---
created_at: 2025-10-10 20:55:47
links:
   - ./index.md
   - ./concept_tdd.md
   - ./concept_tdd_part2.md
   - ./eval_tdd_application_v1.md
---

# 4. TDD 적용 가이드 (v2)

**TDD 프로세스**:
1. **Red**: 실패하는 테스트 작성
2. **Green**: 최소 구현으로 테스트 통과
3. **Refactor**: 코드 개선

**Outside-in 접근** (GOOS 방식):
- UI 테스트부터 시작 → 도메인으로 내려감
- 사용자 관점에서 시작 → 기술 구현으로 진행

---

## 4.0 테스트 인프라 설정 (Phase 0)

**목표**: 전체 테스트 실행 환경과 공통 픽스처 구성

**출처**: 실제 구현에서 도출된 테스트 인프라 패턴

### Step 1: conftest.py 구성

```python
# tests/conftest.py
"""
Pytest Configuration
"""
import pytest
import os
import threading
import time
from pathlib import Path
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from selenium import webdriver
import uvicorn

from cosmetics_landing.config.main import create_app

# .env 파일 로드
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


@pytest.fixture
def client():
    """
    FastAPI 테스트 클라이언트

    E2E 테스트용 애플리케이션 인스턴스
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def valid_order_data():
    """유효한 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99
    }


@pytest.fixture
def order_with_affiliate():
    """어필리에이트 코드가 포함된 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99,
        "affiliate_code": "INFLUENCER123"
    }


@pytest.fixture(scope="session")
def live_server():
    """
    실제 서버를 백그라운드에서 실행하는 픽스처

    Selenium 테스트용 라이브 서버
    포트 충돌 방지를 위해 사용 가능한 포트 자동 탐색
    """
    import socket

    # 사용 가능한 포트 찾기
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    port = find_free_port()

    # 서버를 별도 스레드에서 실행
    server_thread = threading.Thread(
        target=uvicorn.run,
        args=(create_app(),),
        kwargs={
            "host": "127.0.0.1",
            "port": port,
            "log_level": "error"
        },
        daemon=True
    )
    server_thread.start()

    # 서버 시작 대기
    time.sleep(3)

    yield f"http://localhost:{port}"

    # 종료는 daemon 스레드이므로 자동으로 처리됨


@pytest.fixture
def selenium_driver():
    """
    Selenium WebDriver 설정

    Headless Chrome 브라우저 사용
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # 암묵적 대기 시간

    yield driver

    driver.quit()


# pytest marker 설정
def pytest_configure(config):
    """pytest 마커 설정"""
    config.addinivalue_line(
        "markers", "learning: 외부 API 계약 검증을 위한 Learning Test"
    )
    config.addinivalue_line(
        "markers", "integration: 실제 외부 서비스를 사용하는 통합 테스트"
    )
    config.addinivalue_line(
        "markers", "e2e: UI + API 전체 흐름을 검증하는 End-to-End 테스트"
    )
```

**핵심 포인트**:
- ✅ **live_server 픽스처**: 포트 자동 탐색으로 충돌 방지
- ✅ **테스트 마커**: `learning`, `integration`, `e2e` 마커로 테스트 분류
- ✅ **공통 픽스처**: 테스트 데이터 재사용

### Step 2: 테스트 실행 명령어

```bash
# 전체 테스트 실행
uv run pytest

# 마커별 실행
uv run pytest -m learning      # Learning Test만
uv run pytest -m integration   # Integration Test만
uv run pytest -m e2e           # E2E Test만

# 빠른 단위 테스트만 실행 (Learning, Integration, E2E 제외)
uv run pytest -m "not (learning or integration or e2e)"

# 특정 파일 실행
uv run pytest tests/unit/domain/test_order.py -v
```

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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.e2e
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
        selenium_driver.find_element(By.ID, "customer_address").send_keys("123 Main St, Manila, Philippines")
        selenium_driver.find_element(By.ID, "product_price").send_keys("29.99")
        selenium_driver.find_element(By.ID, "submit_order").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "주문이 완료되었습니다" in success_msg.text

    def test_user_can_submit_order_with_affiliate_code(self, selenium_driver, live_server):
        """
        인수 테스트: 사용자가 어필리에이트 코드와 함께 주문할 수 있다

        Epic 2: 어필리에이트 통합 시나리오
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 어필리에이트 코드를 포함한 주문 폼 작성
        selenium_driver.find_element(By.ID, "customer_email").send_keys("customer@example.com")
        selenium_driver.find_element(By.ID, "customer_address").send_keys("Seoul, Korea")
        selenium_driver.find_element(By.ID, "product_price").send_keys("150.00")
        selenium_driver.find_element(By.ID, "affiliate_code").send_keys("INFLUENCER123")
        selenium_driver.find_element(By.ID, "submit_order").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "주문이 완료되었습니다" in success_msg.text

    def test_landing_page_displays_order_form(self, selenium_driver, live_server):
        """
        랜딩 페이지에 주문 폼이 표시된다

        기본 UI 요소 검증 (스모크 테스트)
        """
        # Given & When: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # Then: 주문 폼 요소들이 표시됨
        assert selenium_driver.find_element(By.ID, "customer_email").is_displayed()
        assert selenium_driver.find_element(By.ID, "customer_address").is_displayed()
        assert selenium_driver.find_element(By.ID, "product_price").is_displayed()
        assert selenium_driver.find_element(By.ID, "affiliate_code").is_displayed()
        assert selenium_driver.find_element(By.ID, "submit_order").is_displayed()
```

**핵심 포인트**:
- ✅ **사용자 관점**: 실제 브라우저에서 동작 검증
- ✅ **End-to-End**: UI → API → Domain → DB 전체 흐름
- ✅ **실패 시작**: 이 테스트는 아직 실패 (구현 전)
- ✅ **@pytest.mark.e2e**: 마커로 E2E 테스트 분류

#### Step 2-4: UI 구현 및 검증

*(v1과 동일하므로 생략)*

---

### 4.1.2 Phase 2: Learning Test를 통한 외부 API 계약 학습

**목표**: 외부 API(PayPal, Google Geocoding)의 실제 동작과 응답 구조 학습

**출처**: GOOS Chapter 22 "Maintaining the TDD Cycle" - Learning Tests

**개념**: [concept_tdd_part2.md - Learning Test 패턴](./concept_tdd_part2.md#learning-test-패턴) 참조

#### Step 1: PayPal Sandbox API 계약 학습

```python
# tests/learning/test_paypal_contract.py
"""
PayPal API Contract Learning Test
Chapter 22: "Maintaining the TDD Cycle"

목적:
1. 실제 PayPal Sandbox API 동작 확인
2. API 계약(request/response) 구조 학습
3. 에러 처리 방식 이해
4. Mock 및 실제 어댑터 구현 근거 마련

실행:
    pytest tests/learning/test_paypal_contract.py -v -m learning
"""
import pytest
import os
from decimal import Decimal

try:
    import paypalrestsdk
except ImportError:
    pytest.skip("paypalrestsdk not installed", allow_module_level=True)


@pytest.fixture(scope="module")
def paypal_config():
    """PayPal Sandbox 설정"""
    client_id = os.getenv("PAYPAL_SANDBOX_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_SANDBOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("PayPal credentials not configured in .env")

    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": client_id,
        "client_secret": client_secret
    })

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "mode": "sandbox"
    }


@pytest.mark.learning
class TestPayPalPaymentCreation:
    """PayPal 결제 생성 API 계약 학습"""

    def test_payment_creation_returns_payment_id(self, paypal_config):
        """
        학습 목표: 결제 생성 시 payment_id를 반환한다

        API 계약 검증:
        - 성공 시 payment.create() == True
        - payment.id가 "PAYID-"로 시작
        - payment.state == "created"
        """
        # Given: 최소 결제 정보
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "10.00", "currency": "USD"},
                "description": "Learning test payment"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",
                "cancel_url": "http://localhost:8000/payment/cancel"
            }
        })

        # When: 결제 생성
        result = payment.create()

        # Then: 성공 응답 검증
        assert result is True, f"Payment failed: {payment.error}"
        assert payment.id is not None
        assert payment.id.startswith("PAYID-")
        assert payment.state == "created"

        print(f"\n✅ Payment created: {payment.id}")
```

**핵심 포인트**:
- ✅ **Learning Test**: 외부 API 계약을 학습하고 검증
- ✅ **@pytest.mark.learning**: 마커로 Learning Test 분류
- ✅ **실제 API 호출**: Sandbox 환경에서 실제 동작 확인
- ✅ **문서화**: API 응답 구조와 에러 패턴 명시

#### Step 2: Google Geocoding API 계약 학습

*(유사한 패턴으로 작성, 생략)*

**검증 체크리스트**:
- ✅ PayPal API 응답 구조 파악 (payment.id, payment.state, payment.links)
- ✅ Google API 응답 구조 파악 (status, results, formatted_address, geometry)
- ✅ 에러 케이스 학습 (잘못된 credentials, 네트워크 오류, 잘못된 입력)

---

### 4.1.3 Phase 3: Fake 어댑터 Contract Test

**목표**: Fake 어댑터가 Real 어댑터와 동일한 계약을 준수하는지 검증

**출처**: GOOS Chapter 22 "Learning Tests" - Contract Testing

**개념**: [concept_tdd_part2.md - Contract Test 패턴](./concept_tdd_part2.md#contract-test-패턴) 참조

#### Step 1: Fake Payment Adapter Contract Test

```python
# tests/unit/adapter/test_fake_payment_contract.py
"""
Fake Payment Adapter Contract Test
Chapter 22: "Learning Tests" - Verify Fake implements same contract as Real

목적:
- FakePaymentGateway가 PayPalAdapter와 동일한 계약 준수 확인
- 포트 인터페이스(ProcessPaymentPort) 구현 검증
- 동일한 입출력 타입과 동작 보장
"""
import pytest
from decimal import Decimal
from datetime import datetime

from cosmetics_landing.adapter.out.payment.fake_payment_adapter import FakePaymentAdapter
from cosmetics_landing.adapter.out.payment.paypal_adapter import PayPalAdapter
from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort, PaymentResult
from cosmetics_landing.domain.order import Order, OrderId, Money


class TestFakePaymentAdapterContract:
    """FakePaymentAdapter 계약 검증"""

    def test_implements_process_payment_port(self):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        fake_gateway = FakePaymentAdapter()

        assert isinstance(fake_gateway, ProcessPaymentPort)

    def test_same_interface_as_paypal_adapter(self, sample_order):
        """PayPalAdapter와 동일한 인터페이스"""
        fake_gateway = FakePaymentAdapter()

        # 두 어댑터 모두 동일한 포트 구현
        assert isinstance(fake_gateway, ProcessPaymentPort)

        # 동일한 입출력 타입
        result = fake_gateway.process_payment(sample_order)
        assert isinstance(result, PaymentResult)


class TestFakePaymentAdapterBehavior:
    """FakePaymentAdapter 동작 검증 (Real과 다를 수 있는 부분)"""

    def test_fake_allows_success_mode_toggle(self, sample_order):
        """Fake는 성공/실패 모드 전환 가능 (테스트 편의성)"""
        # 성공 모드
        fake_gateway = FakePaymentAdapter(always_succeed=True)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is True

        # 실패 모드
        fake_gateway = FakePaymentAdapter(always_succeed=False)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is False
```

**핵심 포인트**:
- ✅ **Contract Test**: Fake와 Real이 동일한 포트 인터페이스 구현 검증
- ✅ **테스트 편의성**: Fake는 성공/실패 모드 전환, 예측 가능한 ID 생성
- ✅ **타입 안전성**: 입출력 타입이 동일함을 명시적으로 검증

---

### 4.1.4 Phase 4: API End-to-End 테스트 작성 (확장)

**목표**: API 레벨에서 주문 생성 흐름 검증 + 입력 검증 강화

**출처**: Chapter 4, 5 - Use Case 구현

```python
# tests/integration/end_to_end/test_place_order_e2e.py
"""
Place Order E2E Test
Chapter 4, 5: Walking Skeleton 전체 흐름 검증
"""
import pytest
from fastapi import status


class TestPlaceOrderE2E:
    """주문 생성 E2E 테스트"""

    def test_customer_can_place_order_successfully(self, client, valid_order_data):
        """
        고객이 주문을 생성하고 결제할 수 있다

        Given: 유효한 주문 정보
        When: 주문 생성 API 호출
        Then: 주문이 성공적으로 생성됨
        """
        # When
        response = client.post("/api/orders", json=valid_order_data)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "order_id" in data
        assert data["order_id"] > 0
        assert data["status"] == "success"

    # 입력 검증 테스트 (추가)
    def test_rejects_invalid_email(self, client, valid_order_data):
        """잘못된 이메일은 거부된다"""
        invalid_data = {**valid_order_data, "customer_email": "invalid-email"}
        response = client.post("/api/orders", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rejects_short_address(self, client, valid_order_data):
        """너무 짧은 주소는 거부된다"""
        invalid_data = {**valid_order_data, "customer_address": "abc"}
        response = client.post("/api/orders", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rejects_invalid_address_pattern(self, client, valid_order_data):
        """
        유효하지 않은 주소 패턴은 거부된다

        Business Rule: FakeAddressValidator가 "invalid" 패턴 거부
        """
        invalid_data = {**valid_order_data, "customer_address": "This is an invalid address"}
        response = client.post("/api/orders", json=invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "address" in response.json()["detail"].lower()

    def test_rejects_negative_price(self, client, valid_order_data):
        """음수 가격은 거부된다"""
        invalid_data = {**valid_order_data, "product_price": -10.00}
        response = client.post("/api/orders", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_multiple_orders_get_unique_ids(self, client, valid_order_data):
        """여러 주문이 고유한 ID를 받는다"""
        response1 = client.post("/api/orders", json=valid_order_data)
        response2 = client.post("/api/orders", json=valid_order_data)

        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED

        order_id1 = response1.json()["order_id"]
        order_id2 = response2.json()["order_id"]
        assert order_id1 != order_id2


class TestHealthEndpoints:
    """헬스 체크 엔드포인트 테스트"""

    def test_root_endpoint(self, client):
        """루트 엔드포인트가 응답한다"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "running"

    def test_health_endpoint(self, client):
        """헬스 체크 엔드포인트가 응답한다"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"
```

**핵심 포인트**:
- ✅ **입력 검증 강화**: 엣지 케이스 테스트 (음수, 빈 문자열, 잘못된 형식)
- ✅ **비즈니스 규칙 검증**: FakeAddressValidator의 "invalid" 패턴 거부
- ✅ **인프라 엔드포인트**: 헬스 체크 엔드포인트 테스트 추가

---

### 4.1.5 Phase 5: 도메인 계층 TDD (확장)

**목표**: Money 값 객체 + Order 엔티티 테스트

```python
# tests/unit/domain/test_order.py
"""Order 엔티티 단위 테스트"""
import pytest
from decimal import Decimal
from datetime import datetime

from cosmetics_landing.domain.order import Order, Money, OrderId


class TestMoney:
    """Money 값 객체 테스트"""

    def test_creates_money_with_valid_amount(self):
        """유효한 금액으로 Money 생성"""
        money = Money.of(Decimal("29.99"))
        assert money.amount == Decimal("29.99")

    def test_rejects_negative_amount(self):
        """음수 금액은 거부"""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Money(amount=Decimal("-10.00"))

    def test_money_is_immutable(self):
        """Money는 불변 객체"""
        money = Money.of(Decimal("10.00"))
        with pytest.raises(Exception):  # dataclass frozen
            money.amount = Decimal("20.00")


class TestOrder:
    """Order 엔티티 테스트"""

    def test_creates_new_order_with_pending_status(self):
        """새 주문은 pending 상태로 생성"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St, Manila",
            product_price=Money.of(Decimal("29.99"))
        )

        assert order.payment_status == "pending"
        assert order.id is None
        assert isinstance(order.created_at, datetime)

    def test_marks_order_as_paid(self):
        """주문을 결제 완료 상태로 변경"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        paid_order = order.mark_as_paid()

        assert paid_order.payment_status == "completed"
        assert paid_order.is_paid()
        # 원본은 변경되지 않음 (불변성)
        assert order.payment_status == "pending"

    def test_marks_order_as_failed(self):
        """주문을 결제 실패 상태로 변경"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        failed_order = order.mark_as_failed()

        assert failed_order.payment_status == "failed"
        assert not failed_order.is_paid()
```

**핵심 포인트**:
- ✅ **Money 값 객체 테스트**: 불변성, 음수 검증 추가
- ✅ **mark_as_failed() 메서드**: 결제 실패 상태 처리 추가

---

### 4.1.6 Phase 6: 애플리케이션 계층 TDD (헬퍼 패턴)

**목표**: PlaceOrderService 테스트 + 테스트 헬퍼 패턴 적용

```python
# tests/unit/application/test_place_order_service.py
"""
Place Order Service 단위 테스트
Chapter 4 & Chapter 8: Mock을 사용한 Use Case 테스트
"""
import pytest
from unittest.mock import Mock
from decimal import Decimal

from cosmetics_landing.application.service.place_order_service import PlaceOrderService
from cosmetics_landing.application.port.in_.place_order_use_case import PlaceOrderCommand
from cosmetics_landing.application.port.out.payment_gateway import PaymentResult
from cosmetics_landing.application.exceptions import PaymentFailedError, InvalidAddressError
from cosmetics_landing.domain.order import OrderId


class TestPlaceOrderService:
    """PlaceOrderService 테스트"""

    def create_service(
        self,
        save_order=None,
        process_payment=None,
        validate_address=None
    ):
        """
        테스트용 서비스 생성 헬퍼

        테스트 설정 단순화를 위한 헬퍼 메서드
        """
        return PlaceOrderService(
            save_order_port=save_order or Mock(),
            process_payment_port=process_payment or Mock(),
            validate_address_port=validate_address or Mock()
        )

    def test_validates_address(self):
        """주문 생성 시 주소 검증"""
        # Given: 잘못된 주소
        validate_address = Mock()
        validate_address.is_valid.return_value = False

        service = self.create_service(validate_address=validate_address)
        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="Invalid Address",
            product_price=Decimal("29.99")
        )

        # When/Then: 예외 발생
        with pytest.raises(InvalidAddressError):
            service.place_order(command)

        validate_address.is_valid.assert_called_once_with("Invalid Address")

    def test_saves_order_before_payment(self):
        """결제 전에 주문을 저장"""
        # Given
        save_order = Mock()
        save_order.save.return_value = OrderId(value=1)

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True, transaction_id="txn_123", error_message=None
        )

        service = self.create_service(
            save_order=save_order,
            validate_address=validate_address,
            process_payment=process_payment
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("29.99")
        )

        # When
        service.place_order(command)

        # Then: save가 2번 호출됨 (결제 전, 결제 후)
        assert save_order.save.call_count == 2
```

**핵심 포인트**:
- ✅ **테스트 헬퍼 메서드**: `create_service()` 헬퍼로 테스트 설정 단순화
- ✅ **저장 호출 검증**: `save.call_count == 2` (결제 전/후 저장 확인)

---

### 4.1.7 Phase 7: 어댑터 계층 통합 테스트 (포트 준수 검증)

**목표**: 실제 어댑터가 포트 인터페이스를 준수하는지 명시적으로 검증

```python
# tests/integration/adapter/test_paypal_adapter.py
"""PayPal Adapter Integration Test"""
import pytest
import os
from decimal import Decimal

from cosmetics_landing.adapter.out.payment.paypal_adapter import PayPalAdapter
from cosmetics_landing.domain.order import Order, OrderId, Money


@pytest.mark.integration
class TestPayPalAdapterIntegration:
    """PayPal 어댑터 통합 테스트"""

    def test_processes_payment_successfully(self, paypal_adapter, sample_order):
        """실제 PayPal Sandbox로 결제 처리 성공"""
        result = paypal_adapter.process_payment(sample_order)

        assert result.success is True
        assert result.transaction_id is not None
        assert result.transaction_id.startswith("PAYID-")
        assert result.error_message is None

    def test_handles_network_issues_gracefully(self, sample_order):
        """네트워크 문제 시 적절히 처리"""
        # Given: 잘못된 credentials
        bad_adapter = PayPalAdapter(
            client_id="INVALID",
            client_secret="INVALID",
            mode="sandbox"
        )

        # When: PaymentResult로 변환해야 함 (예외 발생 금지)
        result = bad_adapter.process_payment(sample_order)

        # Then
        assert result.success is False
        assert result.transaction_id is None
        assert result.error_message is not None


@pytest.mark.integration
class TestPayPalAdapterPortCompliance:
    """PayPal 어댑터의 포트 인터페이스 준수 검증"""

    def test_implements_process_payment_port(self, paypal_adapter):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort

        assert isinstance(paypal_adapter, ProcessPaymentPort)

    def test_returns_payment_result_type(self, paypal_adapter, sample_order):
        """PaymentResult 타입 반환 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import PaymentResult

        result = paypal_adapter.process_payment(sample_order)

        assert isinstance(result, PaymentResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'transaction_id')
        assert hasattr(result, 'error_message')
```

**핵심 포인트**:
- ✅ **에러 처리 검증**: 네트워크 오류 시 PaymentResult로 변환 (예외 발생 금지)
- ✅ **포트 준수 검증**: 별도 테스트 클래스로 인터페이스 구현 명시적 검증

---

## 4.2 TDD 모범 사례 정리

### 4.2.1 Test Data Builder 패턴 + 서비스 헬퍼

```python
# tests/unit/application/test_place_order_service.py
class TestPlaceOrderService:
    def create_service(
        self,
        save_order=None,
        process_payment=None,
        validate_address=None
    ):
        """테스트용 서비스 생성 헬퍼"""
        return PlaceOrderService(
            save_order_port=save_order or Mock(),
            process_payment_port=process_payment or Mock(),
            validate_address_port=validate_address or Mock()
        )
```

### 4.2.2 계층별 테스트 전략 (마커 포함)

| 계층 | 테스트 타입 | 마커 | Mock 사용 | 검증 대상 |
|------|------------|------|-----------|-----------|
| **Domain** | 단위 테스트 | - | ❌ 없음 | 비즈니스 규칙 |
| **Application** | 단위 테스트 | - | ✅ 포트 Mock | Use Case 로직 |
| **Adapter (Learning)** | Learning Test | `@pytest.mark.learning` | ❌ 실제 API | API 계약 학습 |
| **Adapter (Contract)** | Contract Test | - | ❌ 없음 | Fake↔Real 계약 일치 |
| **Adapter (Integration)** | 통합 테스트 | `@pytest.mark.integration` | ❌ Sandbox 환경 | 외부 연동 |
| **End-to-End** | E2E 테스트 | `@pytest.mark.e2e` | ❌ 실제 환경 | 전체 흐름 |

**테스트 실행 명령어**:
```bash
pytest -m learning      # Learning Test만 실행
pytest -m integration   # Integration Test만 실행
pytest -m e2e           # E2E Test만 실행
pytest -m "not (learning or integration)"  # 빠른 단위 테스트만
```

---

## 참조 문서

- [TDD 핵심 개념](./concept_tdd.md)
- [TDD 고급 패턴 (Learning Test, Contract Test)](./concept_tdd_part2.md)
- [TDD 적용 평가 v1](./eval_tdd_application_v1.md)
