---
created_at: 2025-10-11
links:
  in:
    - ./index.md                    # 인덱스가 이 가이드를 참조
    - ./eval_tdd_application_v1.md  # 평가 문서가 이 가이드를 참조
  out:
    - ./concept_tdd.md              # TDD 기본 개념
    - ./concept_tdd_part2.md        # Learning Test, Contract Test 패턴
    - ./concept_tdd_best_practices.md  # TDD 모범 사례
---

# TDD 적용 가이드 (v4)

---

## 압축 내용

**Outside-in TDD로 UI→Domain→DB 전체를 관통하는 Walking Skeleton을 먼저 구축하고, Learning Test로 외부 API 계약을 학습한 뒤, Contract Test로 Fake↔Real 일치를 보장하면서 각 Epic을 인수 테스트부터 시작해 계층별로 구현한다.**

---

## 핵심 내용

### TDD 프로세스

**Red-Green-Refactor 사이클**:
1. **Red**: 실패하는 테스트 작성
2. **Green**: 최소 구현으로 테스트 통과
3. **Refactor**: 코드 개선

**참고**: [concept_tdd.md - TDD 기본 개념](./concept_tdd.md)

---

### Outside-in 접근 (GOOS 방식)

**사용자 관점에서 기술 구현으로 진행**:

```
인수 테스트(E2E) 작성
  ↓
UI/API 계층 스텁 구현
  ↓
애플리케이션 계층 테스트 작성
  ↓
도메인 계층 테스트 작성
  ↓
어댑터 계층 테스트 작성
  ↓
인수 테스트 통과
```

**핵심 원칙**:
- **UI 테스트부터 시작** → 도메인으로 내려감
- **사용자 시나리오 우선** → 기술 구현은 나중
- **전체 흐름 검증** → 각 계층은 부분 검증

**참고**: [concept_tdd.md - Outside-in TDD](./concept_tdd.md#outside-in-tdd)

---

### Walking Skeleton 구축

**목표**: 브라우저부터 데이터베이스까지 전체 흐름을 관통하는 최소 기능 구현

**GOOS 원칙** (Chapter 10-11):
- Walking Skeleton은 "UI → API → Domain → DB" 전체를 의미
- 가장 얇은 기능 조각 (thinnest slice)을 End-to-End로 구현
- 외부에서 내부로 (Outside-in) 진행

**구성 요소**:
1. **UI Layer**: HTML 폼 + JavaScript
2. **API Layer**: FastAPI 엔드포인트 스텁
3. **E2E 테스트**: 브라우저 → API 전체 흐름 검증
4. **비즈니스 로직**: 아직 없음 (다음 단계에서 추가)

---

### Learning Test 패턴

**목적**: 외부 API(PayPal, Google Geocoding)의 실제 동작과 응답 구조 학습

**핵심 가치**:
- 외부 API 계약(request/response) 구조 학습
- 에러 처리 방식 이해
- Real Adapter 구현 근거 마련
- `@pytest.mark.learning` 마커로 분류

**참고**: [concept_tdd_part2.md - Learning Test 패턴](./concept_tdd_part2.md#learning-test-패턴)

---

### Contract Test 패턴

**목적**: Fake 어댑터가 Real 어댑터와 동일한 계약을 준수하는지 검증

**핵심 가치**:
- Fake↔Real 동일 계약 보장
- 포트 인터페이스 구현 검증
- 타입 안전성 확보

**참고**: [concept_tdd_part2.md - Contract Test 패턴](./concept_tdd_part2.md#contract-test-패턴)

---

### 계층별 테스트 전략

| 계층 | 테스트 타입 | 마커 | Mock 사용 | 검증 대상 |
|------|------------|------|-----------|-----------|
| **Domain** | 단위 테스트 | - | ❌ 없음 | 비즈니스 규칙 |
| **Application** | 단위 테스트 | - | ✅ 포트 Mock | Use Case 로직 |
| **Adapter (Learning)** | Learning Test | `@pytest.mark.learning` | ❌ 실제 API | API 계약 학습 |
| **Adapter (Contract)** | Contract Test | - | ❌ 없음 | Fake↔Real 계약 일치 |
| **Adapter (Integration)** | 통합 테스트 | `@pytest.mark.integration` | ❌ Sandbox/Fake | 외부 연동 |
| **End-to-End** | E2E 테스트 | `@pytest.mark.e2e` | ❌ 실제 환경 | 전체 흐름 |

**테스트 실행 명령어**:

```bash
# 전체 테스트 실행
uv run pytest

# 마커별 실행
uv run pytest -m learning      # Learning Test만
uv run pytest -m integration   # Integration Test만
uv run pytest -m e2e           # E2E Test만

# 빠른 단위 테스트만 실행 (외부 의존성 제외)
uv run pytest -m "not (learning or integration or e2e)"
```

**참고**: [concept_tdd_best_practices.md - 계층별 테스트 전략](./concept_tdd_best_practices.md#계층별-테스트-전략)

---

## 상세 내용

### 테스트 인프라 설정 (Phase 0)

**목표**: 전체 테스트 실행 환경과 공통 픽스처 구성

**출처**: 실제 구현에서 도출된 테스트 인프라 패턴

#### Step 1: conftest.py 구성

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
from cosmetics_landing.domain.affiliate import Affiliate
from cosmetics_landing.adapter.out.persistence.in_memory_affiliate_adapter import InMemoryAffiliateAdapter

# .env 파일 로드
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


@pytest.fixture
def client():
    """
    FastAPI 테스트 클라이언트

    E2E 테스트용 애플리케이션 인스턴스
    어필리에이트 데이터 사전 생성 포함
    """
    app = create_app()

    # E2E 테스트용 어필리에이트 미리 생성
    affiliate_adapter = InMemoryAffiliateAdapter()
    affiliate_adapter.save(Affiliate.create_new("INFLUENCER123"))
    affiliate_adapter.save(Affiliate.create_new("PARTNER999"))

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


@pytest.fixture
def fake_smtp_server():
    """테스트용 Fake SMTP 서버"""
    from tests.fakes.fake_smtp_server import FakeSMTPServer

    server = FakeSMTPServer(host="localhost", port=2525)
    server.start()
    yield server
    server.stop()


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
- ✅ **어필리에이트 사전 생성**: E2E 테스트용 데이터 미리 준비
- ✅ **fake_smtp_server**: 이메일 전송 테스트용 Fake SMTP 서버

---

### Epic 1: Walking Skeleton 구축

**목표**: 브라우저부터 데이터베이스까지 전체 흐름을 관통하는 최소 기능 구현

**GOOS 원칙** (Chapter 10-11):
- Walking Skeleton은 "UI → API → Domain → DB" 전체를 의미
- 가장 얇은 기능 조각 (thinnest slice)을 End-to-End로 구현
- 외부에서 내부로 (Outside-in) 진행

**참조**: GOOS p.63-88 "The Walking Skeleton"

---

#### Phase 1: UI Walking Skeleton

**목표**: 사용자가 브라우저에서 주문 폼을 제출하고 성공 메시지를 받는 end-to-end 흐름 구축

**출처**: GOOS Chapter 10-11 (p.63-88)

##### Step 1: 인수 테스트 작성 (UI 레벨)

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

##### Step 2: UI 컴포넌트 구현 (TDD)

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
        <div>
            <label for="affiliate_code">어필리에이트 코드 (선택):</label>
            <input type="text" id="affiliate_code">
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
            product_price: parseFloat(document.getElementById('customer_price').value),
            affiliate_code: document.getElementById('affiliate_code').value || null
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

##### Step 3: API 엔드포인트 스텁 구현

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
    affiliate_code: str | None = None


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

##### Step 4: 테스트 실행 및 검증

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

#### Phase 2: Learning Test를 통한 외부 API 계약 학습

**목표**: 외부 API(PayPal, Google Geocoding)의 실제 동작과 응답 구조 학습

**출처**: GOOS Chapter 22 "Maintaining the TDD Cycle" - Learning Tests

**개념**: [concept_tdd_part2.md - Learning Test 패턴](./concept_tdd_part2.md#learning-test-패턴) 참조

##### Step 1: PayPal Sandbox API 계약 학습

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

##### Step 2: Google Geocoding API 계약 학습

*(유사한 패턴으로 작성, 생략)*

##### Step 3: Google Places Adapter 통합 테스트

**목표**: 실제 Google Places API와의 통합 검증

```python
# tests/integration/adapter/test_google_places_adapter.py
"""
Google Places Adapter Integration Test
"""
import pytest
import os

from cosmetics_landing.adapter.out.address_validation.google_places_adapter import GooglePlacesAdapter
from cosmetics_landing.application.port.out.address_validator import ValidateAddressPort


@pytest.fixture
def google_api_key():
    """Google API 키 픽스처"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        pytest.skip("Google Places API key not configured")
    return api_key


@pytest.mark.integration
class TestGooglePlacesAdapterIntegration:
    """Google Places 어댑터 통합 테스트"""

    def test_validates_real_address_successfully(self, google_api_key):
        """실제 주소 검증 성공"""
        # Given
        adapter = GooglePlacesAdapter(api_key=google_api_key)
        valid_address = "서울특별시 강남구 테헤란로 427"

        # When
        result = adapter.is_valid(valid_address)

        # Then
        assert result is True

    def test_validates_with_rooftop_accuracy(self, google_api_key):
        """ROOFTOP 정확도 모드로 검증"""
        # Given
        adapter = GooglePlacesAdapter(
            api_key=google_api_key,
            accuracy_mode="ROOFTOP"
        )
        precise_address = "서울특별시 강남구 테헤란로 427"

        # When
        result = adapter.is_valid(precise_address)

        # Then
        assert result is True

    def test_validates_korean_address(self, google_api_key):
        """한글 주소 검증"""
        # Given
        adapter = GooglePlacesAdapter(api_key=google_api_key)
        korean_address = "서울 강남구 역삼동 123"

        # When
        result = adapter.is_valid(korean_address)

        # Then
        assert result is True

    def test_handles_invalid_api_key_gracefully(self):
        """잘못된 API 키 처리"""
        # Given
        adapter = GooglePlacesAdapter(api_key="INVALID_KEY")
        address = "123 Main St"

        # When/Then: 예외 발생 대신 False 반환
        result = adapter.is_valid(address)
        assert result is False

    def test_handles_network_failure_gracefully(self, google_api_key, monkeypatch):
        """네트워크 실패 처리"""
        # Given
        adapter = GooglePlacesAdapter(api_key=google_api_key)

        # When: 네트워크 오류 시뮬레이션
        def mock_api_call(*args, **kwargs):
            raise ConnectionError("Network error")

        monkeypatch.setattr(adapter, "_call_api", mock_api_call)

        # Then: 예외 발생 대신 False 반환
        result = adapter.is_valid("123 Main St")
        assert result is False
```

**검증 체크리스트**:
- ✅ PayPal API 응답 구조 파악 (payment.id, payment.state, payment.links)
- ✅ Google API 응답 구조 파악 (status, results, formatted_address, geometry)
- ✅ Google Places 통합 검증 (ROOFTOP 정확도, 한글 주소, 에러 처리)
- ✅ 에러 케이스 학습 (잘못된 credentials, 네트워크 오류, 잘못된 입력)

---

#### Phase 3: Fake 어댑터 Contract Test

**목표**: Fake 어댑터가 Real 어댑터와 동일한 계약을 준수하는지 검증

**출처**: GOOS Chapter 22 "Learning Tests" - Contract Testing

**개념**: [concept_tdd_part2.md - Contract Test 패턴](./concept_tdd_part2.md#contract-test-패턴) 참조

##### Step 1: Fake Payment Adapter Contract Test

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

#### Phase 4: API End-to-End 테스트 작성 (확장)

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

#### Phase 5: 도메인 계층 TDD (확장)

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

#### Phase 6: 애플리케이션 계층 TDD (헬퍼 패턴)

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

#### Phase 7: 어댑터 계층 통합 테스트 (포트 준수 검증)

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

#### Phase 8: SQLAlchemy Order Adapter 통합 테스트

**목표**: 데이터베이스 영속성 계층 검증

**테스트 파일**: `test_sqlalchemy_order_adapter.py`

**핵심 테스트**:
- CRUD 작업 (저장, 조회, 업데이트)
- 어필리에이트 코드 조회
- 도메인 ↔ ORM 매핑 검증
- Value Object 보존 (Money, OrderId)

```python
# tests/integration/adapter/test_sqlalchemy_order_adapter.py
"""
SQLAlchemy Order Adapter Integration Test
데이터베이스 영속성 계층 검증
"""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cosmetics_landing.adapter.out.persistence.sqlalchemy_order_adapter import SQLAlchemyOrderAdapter
from cosmetics_landing.adapter.out.persistence.sqlalchemy_models import Base
from cosmetics_landing.domain.order import Order, Money


@pytest.fixture(scope="function")
def db_session():
    """테스트용 In-Memory DB 세션"""
    # In-Memory SQLite 사용
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture
def order_adapter(db_session):
    """SQLAlchemy Order Adapter 픽스처"""
    return SQLAlchemyOrderAdapter(session=db_session)


class TestSQLAlchemyOrderAdapterCRUD:
    """CRUD 작업 테스트"""

    def test_saves_order_successfully(self, order_adapter):
        """주문을 데이터베이스에 저장한다"""
        # Given
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        # When
        order_id = order_adapter.save(order)

        # Then
        assert order_id is not None
        assert order_id.value > 0

    def test_loads_saved_order(self, order_adapter):
        """저장된 주문을 조회한다"""
        # Given: 주문 저장
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )
        order_id = order_adapter.save(order)

        # When: 조회
        loaded_order = order_adapter.load(order_id)

        # Then: 동일한 값 검증
        assert loaded_order.customer_email == "test@example.com"
        assert loaded_order.customer_address == "123 Main St"
        assert loaded_order.product_price.amount == Decimal("29.99")

    def test_updates_order_status(self, order_adapter):
        """주문 상태를 업데이트한다"""
        # Given: 주문 저장
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )
        order_id = order_adapter.save(order)

        # When: 결제 완료로 변경
        paid_order = order.mark_as_paid()
        order_adapter.save(paid_order)

        # Then: 변경된 상태 확인
        loaded_order = order_adapter.load(order_id)
        assert loaded_order.payment_status == "completed"


class TestSQLAlchemyOrderAdapterAffiliateTracking:
    """어필리에이트 코드 조회 테스트"""

    def test_loads_order_by_affiliate_code(self, order_adapter):
        """어필리에이트 코드로 주문을 조회한다"""
        # Given: 어필리에이트 주문 저장
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("100.00")),
            affiliate_code="INFLUENCER123"
        )
        order_adapter.save(order)

        # When: 어필리에이트 코드로 조회
        orders = order_adapter.load_by_affiliate_code("INFLUENCER123")

        # Then
        assert len(orders) == 1
        assert orders[0].affiliate_code == "INFLUENCER123"


class TestSQLAlchemyOrderAdapterValueObjectMapping:
    """Value Object 매핑 검증"""

    def test_preserves_money_value_object(self, order_adapter):
        """Money 값 객체가 보존된다"""
        # Given
        original_money = Money.of(Decimal("29.99"))
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=original_money
        )

        # When: 저장 후 조회
        order_id = order_adapter.save(order)
        loaded_order = order_adapter.load(order_id)

        # Then: Money 타입 보존
        assert isinstance(loaded_order.product_price, Money)
        assert loaded_order.product_price.amount == Decimal("29.99")

    def test_preserves_order_id_value_object(self, order_adapter):
        """OrderId 값 객체가 보존된다"""
        # Given
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        # When: 저장
        order_id = order_adapter.save(order)

        # Then: OrderId 타입 보존
        from cosmetics_landing.domain.order import OrderId
        assert isinstance(order_id, OrderId)
        assert order_id.value > 0
```

**핵심 포인트**:
- ✅ **In-Memory DB**: SQLite In-Memory로 빠른 테스트
- ✅ **CRUD 검증**: 저장, 조회, 업데이트 전체 흐름
- ✅ **어필리에이트 조회**: 코드별 주문 조회 기능
- ✅ **Value Object 보존**: Money, OrderId 타입 보존 검증

---

### Epic 2: 어필리에이트 기능 TDD

**목표**: 어필리에이트 추적 및 커미션 계산 기능 구현

**GOOS 원칙**: Epic 1과 동일하게 Outside-in 접근 - **인수 테스트부터 시작**

---

#### Phase 1: 어필리에이트 인수 테스트 작성

**목표**: 사용자 관점에서 어필리에이트 전체 여정 검증

**출처**: GOOS Chapter 4-5 - 모든 기능은 인수 테스트로 시작

```python
# tests/integration/end_to_end/test_affiliate_tracking_e2e.py
"""
Epic 2 인수 테스트: 어필리에이트 추적 전체 흐름
GOOS 4-5장: Outside-in, 사용자 관점 시나리오
"""
import pytest
from fastapi import status


@pytest.mark.e2e
class TestAffiliateTrackingE2E:
    """어필리에이트 추적 E2E 테스트"""

    def test_affiliate_earns_commission_on_sale(self, client):
        """
        인수 테스트: 어필리에이트 링크로 유입된 고객이 주문하면 커미션이 기록된다

        사용자 여정:
        1. 인플루언서가 어필리에이트 링크 공유 (예: ?ref=INFLUENCER123)
        2. 고객이 해당 링크로 랜딩 페이지 방문 → 클릭 카운트 증가
        3. 고객이 주문 완료 → 어필리에이트 판매 및 커미션 기록
        4. 어필리에이트 대시보드에서 실적 확인
        """
        # Given: 어필리에이트 링크로 방문 (클릭 추적)
        response = client.get("/?ref=INFLUENCER123")
        assert response.status_code == status.HTTP_200_OK

        # When: 고객이 주문
        order_request = {
            "customer_email": "customer@example.com",
            "customer_address": "123 Main St, Seoul",
            "product_price": 100.00,
            "affiliate_code": "INFLUENCER123"
        }
        order_response = client.post("/api/orders", json=order_request)
        assert order_response.status_code == status.HTTP_201_CREATED

        # Then: 어필리에이트 실적 확인
        stats_response = client.get("/api/affiliates/INFLUENCER123/stats")
        assert stats_response.status_code == status.HTTP_200_OK

        stats = stats_response.json()
        assert stats["total_clicks"] == 1
        assert stats["total_sales"] == 1
        assert stats["total_commission"] == 20.00  # 100 * 20%
        assert stats["pending_commission"] == 20.00

    def test_multiple_sales_accumulate_commission(self, client):
        """여러 판매 시 커미션이 누적된다"""
        # Given: 어필리에이트 링크로 방문
        client.get("/?ref=PARTNER999")

        # When: 두 번의 주문
        order1 = {
            "customer_email": "customer1@example.com",
            "customer_address": "Address 1",
            "product_price": 50.00,
            "affiliate_code": "PARTNER999"
        }
        order2 = {
            "customer_email": "customer2@example.com",
            "customer_address": "Address 2",
            "product_price": 150.00,
            "affiliate_code": "PARTNER999"
        }

        client.post("/api/orders", json=order1)
        client.post("/api/orders", json=order2)

        # Then: 커미션 누적 확인
        stats_response = client.get("/api/affiliates/PARTNER999/stats")
        stats = stats_response.json()

        assert stats["total_sales"] == 2
        assert stats["total_commission"] == 40.00  # (50 + 150) * 20%
```

**핵심 포인트**:
- ✅ **Outside-in 흐름**: 인수 테스트로 시작 (GOOS 4-5장)
- ✅ **사용자 여정**: 클릭 → 주문 → 커미션 기록 전체 흐름
- ✅ **비즈니스 규칙 검증**: 20% 커미션 계산, 누적 기록

---

#### Phase 2: 도메인 계층 TDD

**목표**: Affiliate 엔티티 + Commission 값 객체 구현

```python
# tests/unit/domain/test_affiliate.py
"""Affiliate 도메인 엔티티 테스트"""
import pytest
from decimal import Decimal

from cosmetics_landing.domain.affiliate import Affiliate
from cosmetics_landing.domain.commission import Commission
from cosmetics_landing.domain.order import Money


class TestAffiliate:
    """Affiliate 엔티티 테스트"""

    def test_affiliate_records_click(self):
        """어필리에이트 클릭을 기록한다"""
        # Given
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        # When
        updated = affiliate.record_click()

        # Then
        assert updated.total_clicks == 1
        # 원본 불변성 확인
        assert affiliate.total_clicks == 0

    def test_affiliate_records_sale_with_commission(self):
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

    def test_multiple_sales_accumulate(self):
        """여러 판매가 누적된다"""
        # Given
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        # When
        affiliate = affiliate.record_sale(Money.of(Decimal("10.00")))
        affiliate = affiliate.record_sale(Money.of(Decimal("15.00")))

        # Then
        assert affiliate.total_sales == 2
        assert affiliate.total_commission.amount == Decimal("25.00")


class TestCommission:
    """Commission 값 객체 테스트"""

    def test_commission_calculates_20_percent(self):
        """수수료는 주문 금액의 20%이다"""
        # Given
        commission = Commission()
        order_amount = Money.of(Decimal("100.00"))

        # When
        result = commission.calculate(order_amount)

        # Then
        assert result.amount == Decimal("20.00")

    def test_commission_rounds_to_two_decimals(self):
        """수수료는 소수점 둘째 자리까지 반올림한다"""
        # Given
        commission = Commission()
        order_amount = Money.of(Decimal("33.33"))

        # When
        result = commission.calculate(order_amount)

        # Then
        assert result.amount == Decimal("6.67")  # 33.33 * 0.2 = 6.666 → 6.67
```

**핵심 포인트**:
- ✅ **불변성 검증**: `record_click()`, `record_sale()` 후 원본 불변
- ✅ **비즈니스 규칙**: 20% 커미션 계산, 소수점 처리

---

#### Phase 3: 애플리케이션 계층 TDD (명시적 협력 검증)

**목표**: PlaceOrderService에 어필리에이트 추적 로직 추가

**개선**: Mock 내부 파고들기 대신 **명시적 협력 검증** 및 **커스텀 매처** 활용

```python
# tests/unit/application/test_place_order_with_affiliate.py
"""
Place Order Service - 어필리에이트 통합 테스트
Chapter 4: Use Case Composition
"""
import pytest
from unittest.mock import Mock
from decimal import Decimal

from cosmetics_landing.application.service.place_order_service import PlaceOrderService
from cosmetics_landing.application.port.in_.place_order_use_case import PlaceOrderCommand
from cosmetics_landing.application.port.out.payment_gateway import PaymentResult
from cosmetics_landing.domain.affiliate import Affiliate
from cosmetics_landing.domain.order import OrderId, Money


# 테스트 헬퍼: 도메인 검증 로직 캡슐화 (GOOS 24장)
def assert_affiliate_has_sales(affiliate: Affiliate, expected_sales: int, expected_commission: Decimal):
    """
    어필리에이트 판매 및 커미션 검증

    의도 기반 단언 (GOOS 24장: 의도에 대한 정밀하지만 유연한 검증)
    """
    assert affiliate.total_sales == expected_sales, \
        f"Expected {expected_sales} sales, but got {affiliate.total_sales}"
    assert affiliate.total_commission.amount == expected_commission, \
        f"Expected commission {expected_commission}, but got {affiliate.total_commission.amount}"


class TestPlaceOrderWithAffiliate:
    """어필리에이트 코드가 포함된 주문 테스트"""

    def test_place_order_records_affiliate_sale(self):
        """
        어필리에이트 코드가 있는 주문은 판매를 기록한다

        GOOS 7장: 협력 프로토콜 명시적 검증
        """
        # Given
        affiliate = Affiliate.create_new("INFLUENCER123")

        load_affiliate = Mock()
        load_affiliate.load_by_code.return_value = affiliate

        save_affiliate = Mock()

        save_order = Mock()
        save_order.save.return_value = OrderId(1)

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True, transaction_id="txn_123", error_message=None
        )

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        service = PlaceOrderService(
            save_order_port=save_order,
            process_payment_port=process_payment,
            validate_address_port=validate_address,
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

        # Then: 협력 프로토콜 명시적 검증 (GOOS 7장)
        load_affiliate.load_by_code.assert_called_once_with("INFLUENCER123")
        save_affiliate.save.assert_called_once()

        # 저장된 어필리에이트 상태 검증 (커스텀 매처 활용)
        saved_affiliate = save_affiliate.save.call_args[0][0]
        assert_affiliate_has_sales(
            saved_affiliate,
            expected_sales=1,
            expected_commission=Decimal("20.00")  # 100 * 20%
        )

    def test_place_order_without_affiliate_code(self):
        """어필리에이트 코드 없는 주문은 추적하지 않는다"""
        # Given
        load_affiliate = Mock()
        save_affiliate = Mock()

        save_order = Mock()
        save_order.save.return_value = OrderId(1)

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True, transaction_id="txn_123", error_message=None
        )

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        service = PlaceOrderService(
            save_order_port=save_order,
            process_payment_port=process_payment,
            validate_address_port=validate_address,
            load_affiliate_port=load_affiliate,
            save_affiliate_port=save_affiliate
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("50.00"),
            affiliate_code=None  # 코드 없음
        )

        # When
        service.place_order(command)

        # Then: 어필리에이트 포트 호출 안 됨
        load_affiliate.load_by_code.assert_not_called()
        save_affiliate.save.assert_not_called()
```

**개선 포인트**:
- ✅ **명시적 협력 검증**: `assert_called_once_with()` 사용
- ✅ **커스텀 매처**: `assert_affiliate_has_sales()` 헬퍼로 의도 명확화
- ✅ **실패 메시지**: 단언 실패 시 명확한 메시지 제공 (GOOS 23장)

**참고**: [concept_tdd_best_practices.md - Mock 사용 원칙](./concept_tdd_best_practices.md#mock-사용-원칙-goos-7-8장)

---

#### 설계 피드백: 다중 Mock 의존성 검토

**현재 테스트의 문제점** (GOOS 20장):
- `PlaceOrderService` 테스트가 **5개 Mock**에 의존 → 설계 냄새 신호
- "테스트를 짜기 어렵다면 설계를 재검토하라"

**리팩터링 방향**:

```python
# 개선 전: PlaceOrderService가 너무 많은 책임 보유
class PlaceOrderService:
    def place_order(self, command):
        # 1. 주소 검증
        # 2. 주문 생성
        # 3. 결제 처리
        # 4. 어필리에이트 추적
        # 5. 주문 저장
        pass  # 5개 포트에 의존


# 개선 후: 역할 분리
class CommissionCalculator:
    """수수료 계산 전용 서비스 (단일 책임)"""
    def calculate(self, order_amount: Money) -> Money:
        return Money.of(order_amount.amount * Decimal("0.20"))


class AffiliateTracker:
    """어필리에이트 추적 전용 서비스"""
    def __init__(
        self,
        load_affiliate_port: LoadAffiliatePort,
        save_affiliate_port: SaveAffiliatePort,
        commission_calculator: CommissionCalculator
    ):
        self._load_affiliate = load_affiliate_port
        self._save_affiliate = save_affiliate_port
        self._calculator = commission_calculator

    def track_sale(self, affiliate_code: str, order_amount: Money):
        """판매 추적 및 커미션 계산"""
        affiliate = self._load_affiliate.load_by_code(affiliate_code)
        commission = self._calculator.calculate(order_amount)
        updated = affiliate.record_sale(commission)
        self._save_affiliate.save(updated)


class PlaceOrderService:
    """주문 생성 서비스 (책임 축소)"""
    def __init__(
        self,
        save_order_port: SaveOrderPort,
        process_payment_port: ProcessPaymentPort,
        validate_address_port: ValidateAddressPort,
        affiliate_tracker: Optional[AffiliateTracker] = None
    ):
        # Mock 개수 감소: 3개 포트 + 1개 도메인 서비스
        self._save_order = save_order_port
        self._process_payment = process_payment_port
        self._validate_address = validate_address_port
        self._affiliate_tracker = affiliate_tracker

    def place_order(self, command: PlaceOrderCommand) -> OrderId:
        # 주소 검증
        if not self._validate_address.is_valid(command.customer_address):
            raise InvalidAddressError(...)

        # 주문 생성 및 저장
        order = Order.create_new(...)
        order_id = self._save_order.save(order)

        # 결제 처리
        result = self._process_payment.process_payment(order)
        if not result.success:
            raise PaymentFailedError(...)

        # 어필리에이트 추적 (옵션)
        if command.affiliate_code and self._affiliate_tracker:
            self._affiliate_tracker.track_sale(
                command.affiliate_code,
                order.product_price
            )

        return order_id
```

**테스트 개선 효과**:
- Mock 개수 감소 (5개 → 3개)
- `CommissionCalculator` 테스트는 독립적으로 작성
- `AffiliateTracker` 테스트도 분리 (재사용 가능)
- 단일 책임 원칙 준수

---

### Epic 3: 고객 문의 기능 TDD

**목표**: 랜딩 페이지에서 고객 문의를 받아 이메일로 전송

**GOOS 원칙**: Epic 1, 2와 동일하게 **인수 테스트부터 시작**

---

#### Phase 1: 고객 문의 인수 테스트 작성

**목표**: 사용자 관점에서 문의 전체 여정 검증

**출처**: GOOS Chapter 4-5 - 기능 수준 인수 테스트

**2가지 접근**: UI E2E (Selenium) + API E2E (TestClient) 분리

##### 접근 1: UI E2E 테스트 (Selenium)

```python
# tests/integration/end_to_end/test_customer_inquiry_e2e.py
"""
Epic 3 인수 테스트: 고객 문의 전체 흐름
GOOS 4-5장: 사용자 관점 E2E 검증
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.e2e
class TestCustomerInquiryE2E:
    """고객 문의 UI E2E 테스트"""

    def test_customer_can_send_inquiry_from_landing_page(
        self, selenium_driver, live_server, fake_smtp_server
    ):
        """
        인수 테스트: 고객이 랜딩 페이지에서 문의를 보내고 확인 메시지를 받는다

        사용자 여정:
        1. 랜딩 페이지 방문
        2. 문의 폼 작성 및 제출
        3. 성공 메시지 표시
        4. 지원팀이 이메일 수신 확인
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 문의 폼 작성 및 제출
        selenium_driver.find_element(By.ID, "inquiry_email").send_keys("customer@example.com")
        selenium_driver.find_element(By.ID, "inquiry_message").send_keys("When will my order arrive?")
        selenium_driver.find_element(By.ID, "submit_inquiry").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inquiry-success"))
        )
        assert "문의가 접수되었습니다" in success_msg.text

        # And: 지원팀이 이메일 수신 (Fake SMTP 확인)
        received_emails = fake_smtp_server.get_received_emails()
        assert len(received_emails) == 1
        assert received_emails[0]["from"] == "customer@example.com"
        assert "When will my order arrive?" in received_emails[0]["body"]

    def test_inquiry_form_validates_email(self, selenium_driver, live_server):
        """잘못된 이메일 형식은 거부된다"""
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 잘못된 이메일로 제출
        selenium_driver.find_element(By.ID, "inquiry_email").send_keys("invalid-email")
        selenium_driver.find_element(By.ID, "inquiry_message").send_keys("Test message")
        selenium_driver.find_element(By.ID, "submit_inquiry").click()

        # Then: 에러 메시지 표시
        wait = WebDriverWait(selenium_driver, 5)
        error_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inquiry-error"))
        )
        assert "유효한 이메일" in error_msg.text
```

##### 접근 2: API E2E 테스트 (TestClient)

```python
# tests/integration/end_to_end/test_customer_inquiry_api.py
"""
Epic 3 API 인수 테스트: 고객 문의 API 흐름
API 레벨에서 독립적으로 검증
"""
import pytest
from fastapi import status


@pytest.mark.e2e
class TestCustomerInquiryAPI:
    """고객 문의 API E2E 테스트"""

    def test_customer_can_submit_inquiry_via_api(self, client, fake_smtp_server):
        """
        API 인수 테스트: 고객이 API를 통해 문의를 전송할 수 있다

        Given: 유효한 문의 데이터
        When: 문의 전송 API 호출
        Then: 성공 응답 + 이메일 전송됨
        """
        # Given
        inquiry_data = {
            "customer_email": "customer@example.com",
            "message": "When will my order arrive?"
        }

        # When
        response = client.post("/api/inquiries", json=inquiry_data)

        # Then: API 성공 응답
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "success"

        # And: 이메일 전송 확인
        received_emails = fake_smtp_server.get_received_emails()
        assert len(received_emails) == 1
        assert received_emails[0]["from"] == "customer@example.com"

    def test_rejects_invalid_email(self, client):
        """잘못된 이메일은 거부된다"""
        # Given
        invalid_data = {
            "customer_email": "invalid-email",
            "message": "Test message"
        }

        # When
        response = client.post("/api/inquiries", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
```

**핵심 포인트**:
- ✅ **UI + API 분리**: UI 테스트는 브라우저, API 테스트는 TestClient
- ✅ **독립적 검증**: 각 계층을 독립적으로 테스트 가능
- ✅ **Fake SMTP 사용**: 통제 가능한 테스트 환경 (GOOS 8장)
- ✅ **입력 검증**: 이메일 형식 검증 포함

---

#### Phase 2: 애플리케이션 계층 TDD (자기 설명적 진단)

**목표**: SendInquiryService 구현

**개선**: 자기 설명적 진단 및 도메인 헬퍼 활용 (GOOS 23-24장)

```python
# tests/unit/application/test_send_inquiry_service.py
"""
Send Inquiry Service 단위 테스트
"""
import pytest
from unittest.mock import Mock

from cosmetics_landing.application.service.send_inquiry_service import SendInquiryService
from cosmetics_landing.application.port.in_.send_inquiry_use_case import SendInquiryCommand


# 테스트 상수 (GOOS 23장: 자기 설명적 값)
CUSTOMER_EMAIL = "customer@example.com"
SUPPORT_EMAIL = "support@cosmetics.com"
SAMPLE_INQUIRY_MESSAGE = "When will my order arrive?"


# 테스트 헬퍼 (helpers.py)
def assert_inquiry_sent_successfully(result: bool):
    """
    문의 전송 성공 검증

    실패 시 명확한 메시지 제공 (GOOS 23장)
    """
    assert result is True, "Inquiry email should be sent successfully"


def assert_email_sent_with(
    mock_sender,
    from_email: str,
    to_email: str,
    containing: str
):
    """
    이메일 전송 내용 검증

    GOOS 24장: 유연한 단언 - 중요한 부분만 검증
    """
    mock_sender.send.assert_called_once()
    sent_email = mock_sender.send.call_args[0][0]

    assert sent_email.from_address == from_email, \
        f"Expected from={from_email}, got {sent_email.from_address}"
    assert sent_email.to_address == to_email, \
        f"Expected to={to_email}, got {sent_email.to_address}"
    assert containing in sent_email.body, \
        f"Email body should contain '{containing}'"


class TestSendInquiryService:
    """SendInquiryService 테스트"""

    def test_sends_inquiry_email_to_support(self):
        """
        문의 내용을 고객 이메일에서 지원팀으로 전송한다

        Given: 고객이 문의 메시지 작성
        When: 문의 전송 서비스 호출
        Then: 지원팀에게 이메일 전송됨
        """
        # Given
        email_sender = Mock()
        email_sender.send.return_value = True

        service = SendInquiryService(email_sender_port=email_sender)

        command = SendInquiryCommand(
            customer_email=CUSTOMER_EMAIL,
            message=SAMPLE_INQUIRY_MESSAGE
        )

        # When
        result = service.send_inquiry(command)

        # Then: 자기 설명적 검증
        assert_inquiry_sent_successfully(result)
        assert_email_sent_with(
            email_sender,
            from_email=CUSTOMER_EMAIL,
            to_email=SUPPORT_EMAIL,
            containing=SAMPLE_INQUIRY_MESSAGE
        )

    def test_handles_email_send_failure(self):
        """이메일 전송 실패 시 False 반환"""
        # Given
        email_sender = Mock()
        email_sender.send.return_value = False  # 전송 실패

        service = SendInquiryService(email_sender_port=email_sender)

        command = SendInquiryCommand(
            customer_email=CUSTOMER_EMAIL,
            message="Test message"
        )

        # When
        result = service.send_inquiry(command)

        # Then
        assert result is False, "Should return False on send failure"
```

**개선 포인트**:
- ✅ **명명된 상수**: `CUSTOMER_EMAIL`, `SUPPORT_EMAIL` (자기 설명적)
- ✅ **커스텀 헬퍼**: `assert_inquiry_sent_successfully()`, `assert_email_sent_with()`
- ✅ **실패 메시지**: 단언 실패 시 명확한 메시지 제공

**참고**: [concept_tdd_best_practices.md - 자기 설명적 테스트](./concept_tdd_best_practices.md#자기-설명적-테스트-goos-23-24장)

---

#### Phase 3: 어댑터 계층 통합 테스트 (Fake SMTP 전략)

**목표**: Gmail SMTP 어댑터 테스트

**개선**: 실계정 의존 대신 **Fake SMTP + 계약 테스트** 전략 (GOOS 8장)

```python
# tests/integration/adapter/test_gmail_smtp_adapter.py
"""
Gmail SMTP Adapter Integration Test
GOOS 8장: 어댑터 테스트는 얇고 통제 가능하게
"""
import pytest
from unittest import mock

from cosmetics_landing.adapter.out.email.gmail_smtp_adapter import GmailSmtpAdapter
from cosmetics_landing.domain.email import Email


# 전략 1: Fake SMTP 서버 사용 (로컬 개발)
class TestGmailAdapterWithFakeSMTP:
    """Fake SMTP를 사용한 빠른 피드백 테스트"""

    def test_gmail_adapter_sends_email_via_fake_smtp(self, fake_smtp_server):
        """
        Gmail 어댑터가 SMTP 프로토콜로 이메일을 전송한다

        빠른 피드백, CI 친화적
        """
        # Given
        adapter = GmailSmtpAdapter(
            smtp_server="localhost",
            port=2525,
            username="test",
            password="test"
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
        assert len(fake_smtp_server.received_emails) == 1

        received = fake_smtp_server.received_emails[0]
        assert received["from"] == "customer@example.com"
        assert received["to"] == "support@cosmetics.com"
        assert "When will my order arrive?" in received["body"]


# 전략 2: 계약 테스트 (CI 환경)
class TestGmailAdapterSMTPContract:
    """Gmail 어댑터가 SMTP 프로토콜 계약을 준수한다"""

    def test_gmail_adapter_follows_smtp_protocol(self):
        """
        SMTP 프로토콜 계약 검증

        Mock SMTP 응답 시뮬레이션
        """
        with mock.patch("smtplib.SMTP") as mock_smtp:
            # SMTP 서버 응답 시뮬레이션
            mock_instance = mock_smtp.return_value
            mock_instance.sendmail.return_value = {}

            adapter = GmailSmtpAdapter(
                smtp_server="smtp.gmail.com",
                port=587,
                username="test@example.com",
                password="test_password"
            )

            email = Email(
                from_address="customer@example.com",
                to_address="support@cosmetics.com",
                subject="Test",
                body="Test message"
            )

            result = adapter.send(email)

            # Then: SMTP 프로토콜 계약 검증
            assert result is True
            mock_instance.starttls.assert_called_once()
            mock_instance.login.assert_called_once_with("test@example.com", "test_password")
            mock_instance.sendmail.assert_called_once()

    def test_handles_smtp_authentication_failure(self):
        """SMTP 인증 실패 시 적절히 처리"""
        with mock.patch("smtplib.SMTP") as mock_smtp:
            mock_instance = mock_smtp.return_value
            mock_instance.login.side_effect = Exception("Authentication failed")

            adapter = GmailSmtpAdapter(
                smtp_server="smtp.gmail.com",
                port=587,
                username="invalid",
                password="invalid"
            )

            email = Email(
                from_address="customer@example.com",
                to_address="support@cosmetics.com",
                subject="Test",
                body="Test"
            )

            # When: 예외를 잡아서 False 반환해야 함
            result = adapter.send(email)

            # Then
            assert result is False


# 전략 3: 수동 검증 (실제 Gmail Sandbox, 자동화 제외)
@pytest.mark.manual
@pytest.mark.slow
class TestGmailAdapterRealIntegration:
    """
    실제 Gmail SMTP 통합 검증

    수동 실행만, CI에서는 제외
    실행: pytest -m manual
    """

    def test_sends_email_to_real_gmail_sandbox(self):
        """실제 Gmail Sandbox 계정으로 이메일 전송"""
        # 실제 Gmail 샌드박스 계정 사용
        # 수동으로만 실행, CI 파이프라인에서는 제외
        pass
```

**개선 포인트**:
- ✅ **Fake SMTP**: 빠르고 통제 가능한 로컬 테스트
- ✅ **계약 테스트**: Mock으로 SMTP 프로토콜 준수 검증
- ✅ **수동 검증**: 실제 Gmail은 `@pytest.mark.manual`로 분리
- ✅ **CI 친화적**: 자동화 테스트는 Fake/Mock만 사용

---

## 참고 문서

### TDD 개념
- [concept_tdd.md](./concept_tdd.md): TDD 기본 개념, Outside-in 접근
- [concept_tdd_part2.md](./concept_tdd_part2.md): Learning Test, Contract Test 패턴

### TDD 모범 사례
- [concept_tdd_best_practices.md](./concept_tdd_best_practices.md): 테스트 명명, 자기 설명적 테스트, Mock 사용 원칙, 계층별 전략

### 평가 문서
- [eval_tdd_application_v1.md](./eval_tdd_application_v1.md): TDD 적용 평가

---

## GOOS 원칙 준수 체크리스트

- ✅ **Outside-in**: 모든 Epic이 인수 테스트로 시작
- ✅ **Learning Test**: 외부 API 계약 학습 후 구현
- ✅ **Contract Test**: Fake↔Real 동일 계약 보장
- ✅ **명시적 협력**: Mock 내부 대신 프로토콜 검증
- ✅ **자기 설명적 진단**: 커스텀 헬퍼, 명명된 상수 활용
- ✅ **설계 피드백**: 테스트 어려움 → 역할 분리 리팩터링
- ✅ **통제 가능한 테스트**: Fake SMTP, 계약 테스트로 CI 안정성 확보
