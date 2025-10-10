---
created_at: 2025-10-10 09:52:28
links:
  - ../landing_page/imple_guide_v3.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_7_Achieving_Object_Oriented_Design/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_10_The_Walking_Skeleton/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_11_Passing_the_First_Test/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_20_Listening_to_the_Tests/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_21_Test_Readability/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_22_Constructing_Complex_Test_Data/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_23_Test_Diagnostics/extracted_information.md
  - ../../references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md
---

# TDD 가이드

## 압축 내용

**TDD는 설계 도구이자 안전망**: 테스트를 먼저 작성하면 더 나은 설계가 자연스럽게 나온다. Red(실패) → Green(통과) → Refactor(개선) 사이클을 반복하며, **UI부터 시작하는 Walking Skeleton**(브라우저 → API → Domain → DB)으로 전체 인프라를 구축한다. Mock을 사용해 외부 의존성을 격리하고, Test Data Builder로 복잡한 테스트 데이터를 간단히 만들며, 정확한 명세(필요한 것만)로 깨지기 쉬운 테스트를 방지한다.

---

## 핵심 내용

### 핵심 개념들

1. **TDD 4단계 사이클**: Fail → Report → Pass → Refactor
2. **Walking Skeleton**: UI부터 DB까지 전체 계층을 관통하는 최소 E2E 기능
3. **Outside-in TDD**: 사용자가 보는 UI부터 시작해 내부로 진행
4. **Mock Objects**: 외부 의존성 격리와 설계 발견
5. **Test Data Builder**: 복잡한 테스트 데이터 생성 패턴
6. **Self-Describing Values**: 실패 메시지를 명확하게 만드는 값 객체
7. **정확한 명세**: Allow Queries, Expect Commands
8. **포트 슬라이싱**: 테스트 단순화를 위한 인터페이스 분리

### 핵심 개념 설명

#### 1. TDD 4단계 사이클
- **Fail**: 실패하는 테스트 작성 (요구사항 명확화)
- **Report**: 명확한 실패 메시지 (문제 진단)
- **Pass**: 최소 구현 (YAGNI)
- **Refactor**: 테스트가 보장하는 안전망에서 개선

#### 2. Walking Skeleton (GOOS Chapter 10-11)

**정의** (GOOS p.63):
> "A Walking Skeleton is an implementation of the **thinnest possible slice of real functionality** that we can automatically build, deploy, and test **end-to-end**."

**핵심 특징**:
- **End-to-End**: UI(브라우저)부터 데이터베이스까지 전체 흐름
- **Thinnest Slice**: 최소한의 기능 ("Hello World" 수준)
- **Automatically Testable**: 자동화된 테스트로 검증 가능

**목적**:
- 빌드/배포/테스트 인프라 조기 구축
- 전체 시스템 통합 검증
- 리스크 조기 발견

**전통적 방식 vs GOOS 방식**:
| 구분 | 전통적 E2E | GOOS Walking Skeleton |
|------|-----------|---------------------|
| **시작점** | API 레벨 | **UI 레벨 (브라우저)** |
| **테스트** | `TestClient.post()` | `selenium.click()` |
| **범위** | HTTP → 로직 → DB | **브라우저 → HTTP → 로직 → DB** |
| **검증** | JSON 응답 | **사용자가 보는 화면** |

**예시**:
```
❌ API 레벨 E2E (전통적):
TestClient → FastAPI → Service → Repository → DB

✅ UI 레벨 Walking Skeleton (GOOS):
Selenium → Browser → HTML → FastAPI → Service → Repository → DB
```

#### 3. Outside-in TDD (GOOS 방식)

**정의**: 사용자 관점(UI)에서 시작해 내부(Domain)로 진행하는 TDD

**진행 순서**:
1. **UI 테스트** (Selenium) → 실패
2. **API 테스트** (TestClient) → 실패
3. **Application 테스트** (Mock) → 실패
4. **Domain 테스트** → 성공
5. **역순으로 통과**: Domain → Application → API → UI

**왜 Outside-in인가?**
- 사용자가 실제로 경험하는 것부터 검증
- 불필요한 기능 방지 (YAGNI)
- 전체 시스템 통합을 조기에 확인

**Inside-out vs Outside-in**:
```
❌ Inside-out (도메인부터):
Domain → Application → API → (UI 나중에 추가)
→ 문제: 사용자가 필요 없는 기능 구현 가능

✅ Outside-in (UI부터):
UI → API → Application → Domain
→ 장점: 사용자 관점에서 필요한 것만 구현
```

#### 4. Mock Objects
- **설계 발견**: Mock 작성이 복잡하다 = 설계 문제의 신호
- **외부 격리**: 외부 서비스(PayPal, Google API)를 Mock으로 대체
- **빠른 피드백**: 실제 외부 호출 없이 빠른 테스트

#### 5. Test Data Builder
```python
OrderBuilder.an_order() \
    .with_affiliate_code("INFLUENCER123") \
    .paid() \
    .build()
```
- 복잡한 객체 생성을 선언적으로 표현
- 기본값 제공 + 필요한 것만 오버라이드
- 테스트 가독성 향상

#### 6. Self-Describing Values
```python
VIP_DISCOUNT = NamedMoney(Decimal("5.00"), "VIP_DISCOUNT")
# 실패 시: "Expected VIP_DISCOUNT(5.00), got STANDARD_PRICE(29.99)"
```
- 값 자체가 의미를 설명
- 실패 메시지가 즉시 문제 파악 가능

#### 7. 정확한 명세
- **Allow Queries**: 조회 메서드는 검증하지 않음
- **Expect Commands**: 명령 메서드만 검증
- **정보 vs 표현**: JSON 구조가 아닌 정보의 의미 검증

#### 8. 포트 슬라이싱
```python
# ❌ 거대한 Repository
class OrderRepository:
    save(), find_by_id(), find_by_email(), ...

# ✅ 슬라이싱된 포트
class SaveOrderPort: save()
class LoadOrderPort: find_by_id()
```
- 테스트에서 필요한 포트만 Mock
- ISP(Interface Segregation Principle) 준수

### 핵심 개념 간 관계

```
Outside-in TDD 흐름
    ↓
UI Walking Skeleton (브라우저 레벨)
    ↓ (실패 → 하위 계층 구현)
API E2E 테스트 (HTTP 레벨)
    ↓
계층별 TDD 적용
    ├── Domain: 비즈니스 규칙 (실제 객체)
    ├── Application: Use Case 로직 (Mock 포트)
    └── Adapter: 외부 통신 (통합 테스트)
        ↓
테스트 품질 향상
    ├── Test Data Builder → 복잡한 데이터 생성
    ├── Self-Describing Values → 진단성 개선
    ├── 정확한 명세 → Brittle Test 방지
    └── 포트 슬라이싱 → 테스트 단순화
```

**핵심 흐름**:
1. **UI Walking Skeleton**으로 브라우저부터 DB까지 전체 인프라 구축
2. **Outside-in** 방식으로 계층별 TDD 사이클 반복 (Mock으로 외부 격리)
3. Test Data Builder로 테스트 가독성 향상
4. Self-Describing Values로 진단성 개선
5. 정확한 명세로 깨지기 쉬운 테스트 방지

**Mock의 역할**:
- **설계 피드백**: Mock이 복잡 → 인터페이스 개선 필요
- **테스트 격리**: 외부 의존성 제거 → 빠른 피드백
- **포트 검증**: 포트 인터페이스가 올바른지 확인

---

## 상세 내용

### 1. Walking Skeleton 구축

#### 1.1 GOOS 방식: UI부터 시작

**GOOS Chapter 10 (p.63-70)**: Walking Skeleton 정의

**핵심 원칙**:
- End-to-End는 "사용자가 보는 화면"부터 시작
- 가장 얇은 기능 조각 구현
- 자동화된 테스트로 검증

**단계별 구현**:

##### Step 1: 브라우저 레벨 테스트 (가장 바깥)

```python
# tests/integration/end_to_end/test_ui_walking_skeleton.py
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_landing_page_loads_in_browser(selenium_driver, live_server):
    """
    브라우저에서 랜딩 페이지가 로드된다

    GOOS Chapter 11: 첫 번째 End-to-End 테스트
    """
    # When: 브라우저로 방문
    selenium_driver.get(f"{live_server}/")

    # Then: 페이지 로드 확인
    assert "Walking Skeleton" in selenium_driver.page_source

def test_landing_page_connects_to_api(selenium_driver, live_server):
    """
    UI → API 전체 흐름 검증
    """
    # Given: 랜딩 페이지 방문
    selenium_driver.get(f"{live_server}/")

    # When: JavaScript가 API 호출 (자동)
    wait = WebDriverWait(selenium_driver, 5)
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "api-status"),
            "healthy"
        )
    )

    # Then: API 상태 표시
    assert selenium_driver.find_element(By.ID, "api-status").text == "healthy"
```

**왜 Selenium인가?**
- 실제 사용자가 보는 화면 검증
- JavaScript 실행 확인
- 브라우저 호환성 검증

##### Step 2: 최소 HTML 구현

```html
<!-- templates/landing.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <title>Walking Skeleton</title>
</head>
<body>
    <h1>Walking Skeleton</h1>
    <p>API Status: <span id="api-status">checking...</span></p>

    <script>
        fetch('/health')
            .then(r => r.json())
            .then(d => {
                document.getElementById('api-status').textContent = d.status;
            });
    </script>
</body>
</html>
```

**핵심**: 스타일 없이 "작동만" 확인

##### Step 3: FastAPI 서빙

```python
# config/main.py
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def landing():
    return HTMLResponse(Path("templates/landing.html").read_text())

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

##### Step 4: API 레벨 E2E (두 번째 계층)

```python
# tests/integration/end_to_end/test_place_order_e2e.py
def test_customer_can_place_order(client: TestClient):
    """API 레벨 E2E 테스트"""
    # Given
    order_request = {
        "customer_email": "customer@example.com",
        "customer_address": "123 Main St",
        "product_price": 29.99
    }

    # When
    response = client.post("/api/order", json=order_request)

    # Then
    assert response.status_code == 200
    assert "order_id" in response.json()
```

**UI 테스트 vs API 테스트**:
| 레벨 | UI 테스트 | API 테스트 |
|------|----------|-----------|
| **도구** | Selenium | TestClient |
| **범위** | 브라우저 → DB | HTTP → DB |
| **속도** | 느림 | 빠름 |
| **목적** | 사용자 경험 | 기능 로직 |
| **개수** | 소수 (핵심 흐름) | 다수 (모든 케이스) |

#### 1.2 계층별 TDD 적용

**도메인 계층**:
```python
# tests/unit/domain/test_order.py
def test_creates_new_order_with_pending_status():
    order = Order.create_new(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99"))
    )
    assert order.payment_status == "pending"
```

**애플리케이션 계층** (Mock 사용):
```python
# tests/unit/application/test_place_order_service.py
def test_place_order_validates_address():
    validate_address = Mock()
    validate_address.is_valid.return_value = False

    service = PlaceOrderService(
        validate_address_port=validate_address,
        # ... 다른 Mock 포트들
    )

    with pytest.raises(ValueError, match="Invalid address"):
        service.place_order(command)
```

**어댑터 계층** (통합 테스트):
```python
# tests/integration/adapter/test_paypal_adapter.py
@pytest.mark.integration
def test_paypal_adapter_processes_payment():
    adapter = PayPalAdapter(
        client_id=TEST_CLIENT_ID,
        mode="sandbox"
    )
    result = adapter.process_payment(order)
    assert result.success
```

---

### 2. Outside-in TDD 실전

#### 2.1 전체 흐름 예시

**시나리오**: "사용자가 주문 폼을 작성하고 제출한다"

##### Phase 1: UI 테스트 (실패)

```python
def test_user_submits_order_form(selenium_driver):
    # Given: 랜딩 페이지 방문
    driver.get("http://localhost:8000")

    # When: 폼 작성 및 제출
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "address").send_keys("123 Main St")
    driver.find_element(By.ID, "submit").click()

    # Then: 성공 메시지 표시
    assert "주문 완료" in driver.find_element(By.CLASS_NAME, "success").text
```

**결과**: ❌ 실패 (폼 없음)

##### Phase 2: HTML 폼 추가 (UI 테스트 통과)

```html
<form id="orderForm">
    <input type="email" id="email" required>
    <input type="text" id="address" required>
    <button id="submit">주문하기</button>
</form>
<div class="success" style="display:none"></div>
```

**결과**: ❌ 여전히 실패 (API 없음)

##### Phase 3: API 테스트 작성 (실패)

```python
def test_order_api_creates_order(client):
    response = client.post("/api/orders", json={
        "customer_email": "test@example.com",
        "customer_address": "123 Main St"
    })
    assert response.status_code == 201
```

**결과**: ❌ 실패 (엔드포인트 없음)

##### Phase 4: 계층별 구현 (Inside-out)

1. **Domain** 구현 → 테스트 통과
2. **Application** 구현 → 테스트 통과
3. **Adapter** 구현 → 테스트 통과
4. **API** 연결 → API 테스트 통과
5. **JavaScript** 연결 → UI 테스트 통과 ✅

**최종 결과**: 모든 계층 테스트 통과!

#### 2.2 Outside-in의 장점

1. **불필요한 기능 방지**: 사용자가 필요한 것만 구현
2. **조기 통합**: 전체 시스템이 함께 작동하는지 확인
3. **리스크 조기 발견**: 인프라 문제를 먼저 발견
4. **명확한 목표**: UI 테스트가 최종 목표 제시

---

### 3. Mock Objects로 설계 개선

#### 3.1 Mock이 주는 설계 피드백

```python
# ❌ 복잡한 Mock: 설계 문제의 신호
def test_order_notifies_customer():
    mock_notifier = Mock()
    mock_notifier.send_email = Mock()
    mock_notifier.format_message = Mock(return_value="...")
    mock_notifier.validate_address = Mock(return_value=True)
    # Mock이 너무 많은 것을 알아야 함 → 인터페이스가 너무 큼

# ✅ 단순한 인터페이스: 더 나은 설계
class OrderNotifier(Protocol):
    def notify_order_placed(self, order: Order) -> None:
        ...

def test_order_notifies_customer():
    mock_notifier = Mock(spec=OrderNotifier)
    order.place()
    mock_notifier.notify_order_placed.assert_called_once_with(order)
```

**설계 개선 신호**:
- Mock 설정이 복잡 → 인터페이스 단순화 필요
- Mock이 너무 많음 → 의존성 과다, SRP 위반
- Mock 검증이 어려움 → 책임 분산 필요

#### 3.2 외부 의존성 격리

```python
# Domain: 실제 객체 사용
def test_commission_calculates_20_percent():
    commission = Commission()  # 실제 객체
    result = commission.calculate(Money.of(Decimal("100.00")))
    assert result.amount == Decimal("20.00")

# Application: 포트 Mock
def test_place_order_processes_payment():
    process_payment = Mock(spec=ProcessPaymentPort)
    process_payment.process_payment.return_value = PaymentResult(True, "txn", None)

    service = PlaceOrderService(process_payment_port=process_payment)
    service.place_order(command)

    process_payment.process_payment.assert_called_once()

# Adapter: 통합 테스트 (실제 외부 서비스)
@pytest.mark.integration
def test_paypal_adapter():
    adapter = PayPalAdapter(mode="sandbox")  # 실제 PayPal Sandbox
    result = adapter.process_payment(order)
    assert result.success
```

---

### 4. Test Data Builder 패턴

#### 4.1 Builder 구현

```python
# tests/builders.py
class OrderBuilder:
    def __init__(self):
        self.id = None
        self.customer_email = "test@example.com"
        self.customer_address = "123 Main St"
        self.product_price = Money.of(Decimal("29.99"))
        self.affiliate_code = None
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
            created_at=datetime.now(),
            payment_status=self.payment_status
        )
```

#### 4.2 Factory Methods로 가독성 향상

```python
# tests/builders.py
def an_order_with_affiliate():
    return OrderBuilder.an_order() \
        .with_affiliate_code("INFLUENCER123")

def a_paid_order():
    return OrderBuilder.an_order() \
        .with_id(1) \
        .paid()

# 사용
def test_affiliate_commission():
    order = an_order_with_affiliate().build()
    # 테스트 의도가 명확함
```

#### 4.3 Builder 조합

```python
class AffiliateBuilder:
    @classmethod
    def an_affiliate(cls):
        return cls()

    def with_code(self, code: str):
        self.code = code
        return self

# 조합 사용
def test_order_with_affiliate():
    affiliate = AffiliateBuilder.an_affiliate() \
        .with_code("INFLUENCER123") \
        .build()

    order = OrderBuilder.an_order() \
        .with_affiliate_code(affiliate.code) \
        .build()
```

---

### 5. 자가 진단 테스트

#### 5.1 Self-Describing Values

```python
# tests/helpers.py
class NamedMoney(Money):
    def __init__(self, amount: Decimal, name: str):
        super().__init__(amount)
        self._name = name

    def __repr__(self):
        return f"{self._name}({self.amount})"

# 상수로 정의
VIP_DISCOUNT = NamedMoney(Decimal("5.00"), "VIP_DISCOUNT")
STANDARD_PRICE = NamedMoney(Decimal("29.99"), "STANDARD_PRICE")

# 사용
def test_applies_discount():
    order = OrderBuilder.an_order() \
        .with_price(STANDARD_PRICE) \
        .with_discount(VIP_DISCOUNT) \
        .build()

    total = order.calculate_total()

    # 실패 시 명확한 메시지:
    # "Expected 24.99, but got 29.99.
    #  Price: STANDARD_PRICE(29.99), Discount: VIP_DISCOUNT(5.00)"
    assert total == Decimal("24.99")
```

#### 5.2 Tracer Objects

```python
# tests/helpers.py
class TracerCustomer:
    """테스트용 최소 Customer 구현"""
    def __init__(self, name: str = "TRACER"):
        self.name = name

    def __repr__(self):
        return f"TracerCustomer('{self.name}')"

# 사용
def test_order_requires_customer():
    order = Order(customer=TracerCustomer("TEST_CUSTOMER"))

    # 실패 시: "TracerCustomer('TEST_CUSTOMER') was used in..."
    # 어디서 어떻게 사용되는지 명확히 알 수 있음
```

#### 5.3 Hamcrest Matchers (선택)

```python
from hamcrest import assert_that, equal_to, has_property

def test_order_total():
    order = OrderBuilder.an_order().build()

    # 명확한 실패 메시지
    assert_that(order.calculate_total(),
                equal_to(Decimal("29.99")),
                "Order total calculation")

    # 속성 검증
    assert_that(order,
                has_property("payment_status", "completed"))
```

---

### 6. 정확한 명세 작성

#### 6.1 Allow Queries, Expect Commands

```python
# ❌ Query를 검증 (불필요)
def test_order_calculation():
    tax_calculator = Mock()
    tax_calculator.calculate_tax.return_value = Decimal("2.00")

    order = Order(tax_calculator=tax_calculator)
    total = order.calculate_total()

    # Query를 검증할 필요 없음
    tax_calculator.calculate_tax.assert_called_once()  # 불필요

# ✅ Command만 검증
def test_order_places_successfully():
    repository = Mock()

    order = Order()
    order.place(repository=repository)

    # Command(상태 변경)만 검증
    repository.save.assert_called_once_with(order)
```

**원칙**:
- **Query** (조회): 부작용 없음 → 검증 불필요
- **Command** (명령): 상태 변경 → 검증 필수

#### 6.2 정보 vs 표현 분리

```python
# ❌ 표현(JSON 구조)에 의존
def test_order_serialization():
    order = create_order()
    json_data = order.to_json()

    # JSON 문자열 구조에 결합됨
    assert json_data == '{"id": 1, "total": "10.00"}'

# ✅ 정보(의미)에 집중
def test_order_serialization():
    order = create_order()
    data = json.loads(order.to_json())

    # 정보의 의미만 검증
    assert data["id"] == order.id
    assert Decimal(data["total"]) == order.total
```

#### 6.3 Guinea Pig Objects

```python
# ❌ 도메인 모델에 결합
def test_repository_saves_order():
    real_order = Order(customer=Customer("John"))  # 복잡
    repository.save(real_order)

# ✅ Guinea Pig Object (테스트 전용)
@dataclass
class GuineaPigOrder:
    id: int
    total: Decimal

def test_repository_saves_order():
    guinea_pig = GuineaPigOrder(id=1, total=Decimal("10.00"))
    repository.save(guinea_pig)

    saved = repository.find_by_id(1)
    assert saved.id == guinea_pig.id
    assert saved.total == guinea_pig.total
```

**목적**: Adapter 테스트를 도메인 모델로부터 분리

---

### 7. 포트 슬라이싱으로 테스트 단순화

#### 7.1 ISP 적용

```python
# ❌ 거대한 인터페이스
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

    @abstractmethod
    def find_by_id(self, id: OrderId) -> Order: pass

    @abstractmethod
    def find_by_email(self, email: str) -> List[Order]: pass

    @abstractmethod
    def find_by_affiliate(self, code: str) -> List[Order]: pass

# ✅ 슬라이싱된 포트
class SaveOrderPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

class LoadOrderPort(ABC):
    @abstractmethod
    def load_by_id(self, id: OrderId) -> Order: pass

class LoadOrdersByAffiliatePort(ABC):
    @abstractmethod
    def load_by_affiliate(self, code: str) -> List[Order]: pass
```

#### 7.2 테스트 단순화

```python
# PlaceOrderService는 SaveOrderPort만 필요
def test_place_order():
    save_order = Mock(spec=SaveOrderPort)
    save_order.save.return_value = OrderId(1)

    service = PlaceOrderService(
        save_order_port=save_order,
        # ... 다른 필요한 포트들
    )

    service.place_order(command)

    save_order.save.assert_called_once()

# GetOrderService는 LoadOrderPort만 필요
def test_get_order():
    load_order = Mock(spec=LoadOrderPort)
    load_order.load_by_id.return_value = Order(...)

    service = GetOrderService(load_order_port=load_order)

    order = service.get_order(OrderId(1))

    assert order is not None
```

**장점**:
- Mock 설정이 단순해짐
- 테스트가 필요한 것만 검증
- 인터페이스 변경 영향 최소화

---

### 8. 계층별 테스트 전략

| 계층 | 테스트 타입 | Mock 사용 | 검증 대상 | 예시 |
|------|------------|-----------|-----------|------|
| **UI** | E2E 테스트 | ❌ 없음 | 사용자 경험 | `test_user_submits_order()` |
| **Domain** | 단위 테스트 | ❌ 없음 | 비즈니스 규칙 | `test_order_marks_as_paid()` |
| **Application** | 단위 테스트 | ✅ 포트 Mock | Use Case 로직 | `test_place_order_validates_address()` |
| **Adapter (Web)** | 통합 테스트 | ✅ Use Case Mock | HTTP 매핑 | `test_order_controller_returns_order_id()` |
| **Adapter (Persistence)** | 통합 테스트 | ❌ 실제 DB (TestContainer) | 영속성 로직 | `test_repository_saves_order()` |
| **Adapter (External)** | 통합 테스트 | ❌ Sandbox 환경 | 외부 연동 | `test_paypal_adapter_processes_payment()` |

#### 8.1 테스트 피라미드

```
    UI E2E (소수)
   /              \
  /  통합 (중간)    \
 /                  \
/    단위 (다수)     \
/____________________\
```

- **단위 테스트**: 빠르고 많이, Mock 활용
- **통합 테스트**: 외부 의존성 실제 연동
- **UI E2E 테스트**: 핵심 사용자 시나리오만

---

### 9. 실전 팁

#### 9.1 테스트 이름 규칙

```python
# ❌ 모호한 이름
def test_order(): ...

# ✅ 명확한 이름 (Given-When-Then)
def test_creates_new_order_with_pending_status(): ...
def test_marks_order_as_paid_when_payment_succeeds(): ...
def test_raises_error_when_address_is_invalid(): ...
```

#### 9.2 AAA 패턴

```python
def test_vip_customer_gets_free_shipping():
    # Arrange (Given)
    customer = CustomerBuilder.a_vip_customer().build()
    order = OrderBuilder.an_order().with_customer(customer).build()

    # Act (When)
    shipping_cost = order.calculate_shipping()

    # Assert (Then)
    assert shipping_cost == Decimal("0")
```

#### 9.3 테스트 하나당 하나의 개념

```python
# ❌ 여러 개념 테스트
def test_order():
    order = create_order()
    assert order.total == Decimal("10.00")
    assert order.status == "pending"
    assert len(order.lines) == 1

# ✅ 개념별로 분리
def test_order_calculates_correct_total():
    order = create_order()
    assert order.total == Decimal("10.00")

def test_new_order_has_pending_status():
    order = create_order()
    assert order.status == "pending"
```

#### 9.4 테스트에서 로직 금지

```python
# ❌ 테스트에 로직
def test_order_total():
    order = create_order()
    expected = Decimal("0")
    for line in order.lines:
        expected += line.price * line.quantity
    assert order.total == expected

# ✅ 명확한 기댓값
def test_order_total():
    order = OrderBuilder.an_order() \
        .with_line("Book", Decimal("10.00"), 2) \
        .build()
    assert order.total == Decimal("20.00")
```

---

## 마무리

TDD는 **설계 도구**이자 **문서**이며 **안전망**이야.

**핵심 요약**:
1. **Walking Skeleton (UI부터)** → 브라우저부터 DB까지 전체 인프라 구축
2. **Outside-in TDD** → 사용자 관점에서 내부로 진행
3. **Mock Objects** → 외부 격리 + 설계 피드백
4. **Test Data Builder** → 복잡한 데이터를 간단히
5. **Self-Describing Values** → 실패 메시지를 명확하게
6. **정확한 명세** → Allow Queries, Expect Commands
7. **포트 슬라이싱** → 테스트 단순화

**TDD 사이클**:
- ❌ Fail: 요구사항 명확화
- 📝 Report: 문제 진단
- ✅ Pass: 최소 구현
- 🔄 Refactor: 안전망에서 개선

**Outside-in 핵심**:
```
UI (사용자가 보는 것)
  ↓
API (HTTP 인터페이스)
  ↓
Application (Use Case 로직)
  ↓
Domain (비즈니스 규칙)
```

이 패턴들을 하나씩 적용하다 보면 자연스럽게 더 나은 설계가 나올 거야. 화이팅! 🚀
