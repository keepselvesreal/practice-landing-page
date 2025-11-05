# Testing Guide from Growing Object-Oriented Software

**작성일**: 2025-11-04
**작성자**: Claude & 태수
**출처**: Growing Object-Oriented Software, Guided by Test (Steve Freeman, Nat Pryce)

이 문서는 GOOS 책의 내용을 바탕으로 소프트웨어 테스팅 범주 체계를 설명합니다.

---

## 목차

- [테스트 명명 규칙](#테스트-명명-규칙-ch-212-pp248-251)
- [테스트 구조화 패턴](#테스트-구조화-패턴-ch-213-pp251-252)
- [테스트 데이터 관리](#테스트-데이터-관리)
  - [Builder 패턴](#builder-패턴-ch-222-pp258-259)
  - [유사 객체 생성](#유사-객체-생성-ch-223-pp259-261)
  - [Factory 패턴](#factory-패턴-ch-225-pp261-262)
- [모킹 전략](#모킹-전략)
  - [Mock 객체의 역할](#mock-객체의-역할-ch-27-pp19-20)
  - [자신이 소유한 타입만 Mock](#자신이-소유한-타입만-mock-ch-8-pp69-71)
- [References](#references)

---

## 테스트 명명 규칙 [Ch 21.2, pp.248-251]

### 핵심 원칙

테스트 이름은 **메서드명이 아닌 기능(feature)을 설명**해야 한다. 테스트 대상 클래스를 암묵적 주어로 하여, 각 테스트 이름이 문장처럼 읽히도록 작성한다.

### 잘못된 예시들

**의미 없는 이름**:
```java
public class TargetObjectTest {
  @Test public void test1() { [...] }
  @Test public void test2() { [...] }
}
```

```python
class TestTargetObject:
    def test_1(self): ...
    def test_2(self): ...
```

**메서드명 반복** (Don't Repeat Yourself 위반):
```java
public class TargetObjectTest {
  @Test public void isReady() { [...] }
  @Test public void choose() { [...] }
  @Test public void choose1() { [...] }
}
```

```python
class TestTargetObject:
    def test_is_ready(self): ...
    def test_choose(self): ...
    def test_choose1(self): ...
```

### TestDox 컨벤션 (권장)

**좋은 예시**:
```java
public class ListTests {
  @Test public void holdsItemsInTheOrderTheyWereAdded() { [...] }
  @Test public void canHoldMultipleReferencesToTheSameItem() { [...] }
  @Test public void throwsAnExceptionWhenRemovingAnItemItDoesntHold() { [...] }
}
```

```python
class TestList:
    def test_holds_items_in_the_order_they_were_added(self): ...
    def test_can_hold_multiple_references_to_the_same_item(self): ...
    def test_throws_an_exception_when_removing_an_item_it_doesnt_hold(self): ...
```

### 명명 스타일 가이드

테스트 이름은 다음을 포함해야 한다:
1. **예상 결과** (expected result)
2. **동작** (action on the object)
3. **동기/시나리오** (motivation for the scenario)

**비교**:
```java
// ❌ 불충분
pollsTheServersMonitoringPort()

// ✅ 명확
notifiesListenersThatServerIsUnavailableWhenCannotConnectToItsMonitoringPort()
```

```python
# ❌ 불충분
def test_polls_the_servers_monitoring_port(self): ...

# ✅ 명확
def test_notifies_listeners_that_server_is_unavailable_when_cannot_connect_to_its_monitoring_port(self): ...
```

### 실용 팁

- **이름 길이**: 리플렉션으로 호출되므로 얼마든지 길어도 됨
- **문서화**: TestDox 도구로 자동 문서 생성 가능
- **작성 순서**: 테스트 이름을 먼저 정하고 본문 작성 OR 작성 후 이름 결정 (둘 다 가능, 단 최종적으로 일관성 유지)

---

## 테스트 구조화 패턴 [Ch 21.3, pp.251-252]

### Canonical Test Structure (표준 테스트 구조)

테스트를 표준 형식으로 작성하면 이해하기 쉽고, expectations와 assertions를 빠르게 찾을 수 있다.

### 4단계 구조

1. **Setup**: 테스트 컨텍스트 준비 (환경 설정)
2. **Execute**: 타겟 코드 호출 (테스트할 동작 실행)
3. **Verify**: 예상 결과 확인 (assertion)
4. **Teardown**: 정리 (다른 테스트 오염 방지)

**다른 버전**: "Arrange, Act, Assert" (AAA) - 일부 단계를 축약

### 예시: 기본 구조

```java
public class StringTemplateTest {
  @Test public void expandsMacrosSurroundedWithBraces() {
    // Setup
    StringTemplate template = new StringTemplate("{a}{b}");
    HashMap<String,Object> macros = new HashMap<String,Object>();
    macros.put("a", "A");
    macros.put("b", "B");

    // Execute
    String expanded = template.expand(macros);

    // Verify
    assertThat(expanded, equalTo("AB"));

    // No Teardown needed
  }
}
```

```python
class TestStringTemplate:
    def test_expands_macros_surrounded_with_braces(self):
        # Setup
        template = StringTemplate("{a}{b}")
        macros = {"a": "A", "b": "B"}

        # Execute
        expanded = template.expand(macros)

        # Verify
        assert expanded == "AB"

        # No Teardown needed
```

### Mock 객체를 사용하는 변형

Expectations를 Execute 전에 선언하고, 실행 후 암묵적으로 검증:

```java
@RunWith(JMock.class)
public class LoggingXMPPFailureReporterTest {
  private final Mockery context = new Mockery() {{  // Setup
    setImposteriser(ClassImposteriser.INSTANCE);
  }};
  final Logger logger = context.mock(Logger.class);
  final LoggingXMPPFailureReporter reporter =
      new LoggingXMPPFailureReporter(logger);

  @Test public void writesMessageTranslationFailureToLog() {
    Exception exception = new Exception("an exception");

    // Expect
    context.checking(new Expectations() {{
      oneOf(logger).severe("expected log message here");
    }});

    // Execute
    reporter.cannotTranslateMessage("auction id", "failed message", exception);

    // Assert (implicitly checks expectations)
  }

  @AfterClass public static void resetLogging() {  // Teardown
    LogManager.getLogManager().reset();
  }
}
```

```python
import unittest
from unittest.mock import Mock

class TestLoggingXMPPFailureReporter(unittest.TestCase):
    def setUp(self):  # Setup
        self.logger = Mock()
        self.reporter = LoggingXMPPFailureReporter(self.logger)

    def test_writes_message_translation_failure_to_log(self):
        exception = Exception("an exception")

        # Execute
        self.reporter.cannot_translate_message(
            "auction id", "failed message", exception
        )

        # Verify (expectations)
        self.logger.severe.assert_called_once_with("expected log message here")

    @classmethod
    def tearDownClass(cls):  # Teardown
        # Reset logging if needed
        pass
```

### 실용 팁

- **테스트 작성 순서**: 테스트 이름 → Execute 코드 → Expectations/Assertions → Setup/Teardown
- **Assertion 개수**: "하나의 일관된 기능"을 표현하는 데 필요한 만큼 (일반적으로 몇 개 이내)
- **표준 형식의 어려움 = 코드 복잡도 신호**: 표준 형식으로 쓰기 어렵다면 코드가 너무 복잡하거나 아이디어가 불명확한 것

---

## 테스트 데이터 관리

### Builder 패턴 [Ch 22.2, pp.258-259]

복잡한 객체 설정이 필요한 경우, Test Data Builder로 인스턴스를 생성한다.

### 문제: Object Mother의 한계

```java
// Object Mother 방식 - 변형마다 새 메서드 필요
Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
```

```python
# Object Mother 방식
order1 = ExampleOrders.new_deerstalker_and_cape_and_swordstick_order()
order2 = ExampleOrders.new_deerstalker_and_boots_order()
```

→ 시간이 지나면 중복 코드 또는 무한한 세밀한 메서드로 지저분해짐

### 해결: Test Data Builder

**Builder 구조**:

```java
public class OrderBuilder {
  // 필드는 안전한 기본값으로 초기화
  private Customer customer = new CustomerBuilder().build();
  private List<OrderLine> lines = new ArrayList<OrderLine>();
  private BigDecimal discountRate = BigDecimal.ZERO;

  // Static factory method (선택사항)
  public static OrderBuilder anOrder() {
    return new OrderBuilder();
  }

  // Chainable methods
  public OrderBuilder withCustomer(Customer customer) {
    this.customer = customer;
    return this;
  }

  public OrderBuilder withOrderLines(OrderLines lines) {
    this.lines = lines;
    return this;
  }

  public OrderBuilder withDiscount(BigDecimal discountRate) {
    this.discountRate = discountRate;
    return this;
  }

  public Order build() {
    Order order = new Order(customer);
    for (OrderLine line : lines) order.addLine(line);
    order.setDiscountRate(discountRate);
    return order;
  }
}
```

```python
from typing import List
from decimal import Decimal

class OrderBuilder:
    def __init__(self):
        # 필드는 안전한 기본값으로 초기화
        self.customer = CustomerBuilder().build()
        self.lines: List[OrderLine] = []
        self.discount_rate = Decimal("0")

    # Static factory method (선택사항)
    @staticmethod
    def an_order():
        return OrderBuilder()

    # Chainable methods
    def with_customer(self, customer):
        self.customer = customer
        return self

    def with_order_lines(self, lines):
        self.lines = lines
        return self

    def with_discount(self, discount_rate):
        self.discount_rate = discount_rate
        return self

    def build(self):
        order = Order(self.customer)
        for line in self.lines:
            order.add_line(line)
        order.set_discount_rate(self.discount_rate)
        return order
```

### 사용 예시

**기본 케이스**:
```java
Order order = new OrderBuilder().build();
```

```python
order = OrderBuilder().build()
```

**특정 값 지정**:
```java
Order order = new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode().build())
      .build())
  .build();
```

```python
order = (OrderBuilder()
    .from_customer(
        CustomerBuilder()
            .with_address(AddressBuilder().with_no_postcode().build())
            .build())
    .build())
```

### Builder의 이점

1. **표현력**: 관련 값만 포함하여 테스트 의도 명확
2. **복원력**: 객체 구조 변경 시 Builder만 수정
3. **가독성**: 메서드 이름이 파라미터 목적 식별
4. **에러 탐지**: 잘못된 값 전달 시 더 명확

**비교**:
```java
// ❌ 목적 불명확
TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");

// ✅ 실수 명확히 드러남
new AddressBuilder()
  .withStreet("221b Baker Street")
  .withStreet2("London")  // 도시가 아닌 street2!
  .withPostCode("NW1 6XE")
  .build();
```

```python
# ❌ 목적 불명확
TestAddresses.new_address("221b Baker Street", "London", "NW1 6XE")

# ✅ 실수 명확히 드러남
(AddressBuilder()
    .with_street("221b Baker Street")
    .with_street2("London")  # 도시가 아닌 street2!
    .with_postcode("NW1 6XE")
    .build())
```

---

### 유사 객체 생성 [Ch 22.3, pp.259-261]

여러 유사한 객체가 필요할 때, Builder를 재사용하여 공통 상태를 공유한다.

**❌ 중복 많은 방식**:
```java
Order orderWithSmallDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.10)
  .build();

Order orderWithLargeDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.25)
  .build();
```

**✅ Builder 재사용**:
```java
OrderBuilder hatAndCape = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1);

Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
```

```python
hat_and_cape = (OrderBuilder()
    .with_line("Deerstalker Hat", 1)
    .with_line("Tweed Cape", 1))

order_with_small_discount = hat_and_cape.with_discount(0.10).build()
order_with_large_discount = hat_and_cape.with_discount(0.25).build()
```

### 주의: 상태 누적 문제

다른 필드를 변경할 때 이전 변경사항이 누적됨:
```java
// ⚠️ orderWithGiftVoucher도 10% 할인 포함!
Order orderWithDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build();
```

**해결책 1: Copy Constructor**:
```java
Order orderWithDiscount = new OrderBuilder(hatAndCape)
  .withDiscount(0.10)
  .build();

Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
  .withGiftVoucher("abc")
  .build();
```

```python
order_with_discount = (OrderBuilder.copy_from(hat_and_cape)
    .with_discount(0.10)
    .build())

order_with_gift_voucher = (OrderBuilder.copy_from(hat_and_cape)
    .with_gift_voucher("abc")
    .build())
```

**해결책 2: but() 메서드**:
```java
Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build();
```

```python
order_with_discount = hat_and_cape.but_().with_discount(0.10).build()
order_with_gift_voucher = hat_and_cape.but_().with_gift_voucher("abc").build()
```

---

### Factory 패턴 [Ch 22.5, pp.261-262]

Factory 메서드로 Builder 생성을 감싸면 도메인 모델을 강조하고 노이즈를 줄일 수 있다.

### 진화 과정

**1단계: 기본 Builder**:
```java
Order order = new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode()))
  .build();
```

**2단계: Factory 메서드 도입**:
```java
Order order =
  anOrder().fromCustomer(
    aCustomer().withAddress(anAddress().withNoPostcode()))
  .build();
```

```python
order = (an_order()
    .from_customer(
        a_customer().with_address(an_address().with_no_postcode()))
    .build())
```

**3단계: 메서드 오버로딩으로 단순화** (Java):
```java
Order order =
  anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
```

```python
# Python은 타입 기반 오버로딩 없으므로 명시적 메서드명 유지
order = (an_order()
    .from_customer(a_customer().with_address(an_address().with_no_postcode()))
    .build())
```

### 도메인 타입 장려

오버로딩은 도메인 타입 도입을 장려:
```java
Address address = anAddress()
    .withStreet("221b Baker Street")
    .withCity("London")
    .with(postCode("NW1", "3RX"))  // 타입 기반 오버로딩
    .build();
```

```python
address = (an_address()
    .with_street("221b Baker Street")
    .with_city("London")
    .with_postcode(postcode("NW1", "3RX"))  # 명시적 메서드
    .build())
```

---

## 모킹 전략

### Mock 객체의 역할 [Ch 2.7, pp.19-20]

Mock 객체는 테스트 대상 객체의 **이웃(neighbors)**을 시뮬레이션한다.

### 기본 구조

```java
// Mockery: mock 객체 생성 및 expectations 관리
Mockery context = new Mockery();

// 테스트 구조:
// 1. Mock 객체 생성
// 2. 실제 객체 생성 (테스트 대상 포함)
// 3. Mock 호출 예상 명시
// 4. 타겟 객체의 트리거 메서드 호출
// 5. 결과 검증 및 예상 호출 확인
```

```python
# Python unittest.mock 사용
from unittest.mock import Mock

# 테스트 구조:
# 1. Mock 객체 생성
mock_neighbor = Mock()

# 2. 실제 객체 생성
target = TargetObject(mock_neighbor)

# 3. 트리거 메서드 호출
target.do_something()

# 4. Mock 호출 검증
mock_neighbor.expected_method.assert_called_once_with(expected_args)
```

### Interface Discovery

Mock을 사용하면 이웃 객체가 존재하지 않아도 테스트 가능:
- 테스트를 통해 필요한 역할(supporting roles)을 발견
- Java interface로 정의
- 시스템 개발 진행하며 실제 구현 추가

---

### 자신이 소유한 타입만 Mock [Ch 8, pp.69-71]

### 원칙: Don't Mock Types You Can't Change

**문제점**:
1. 외부 라이브러리를 완전히 이해하기 어려움 (문서 불완전/부정확, 버그 존재)
2. Mock이 실제 동작과 일치하는지 보장 어려움
3. 라이브러리 업그레이드 시 테스트 유효성 재확인 필요
4. 테스트가 복잡해지고, 설계 피드백에 대응 불가

### 해결: Adapter Layer 작성

```
Application Objects → [Adapter Interfaces] → Adapter Implementation → Third-Party Library
         ↑                     ↑
    Unit Tests            Integration Tests
    (Mock Adapters)       (Real Library)
```

**장점**:
1. 애플리케이션 도메인 용어로 인터페이스 정의
2. Adapter는 얇게 유지 (테스트 어렵고 취약한 코드 최소화)
3. Integration 테스트로 외부 API 이해 검증
4. 낮은 수준의 기술 개념이 도메인 모델로 누출되는 것 방지

### 예외

Mock 외부 라이브러리가 유용한 경우:
- 예외 발생 같은 시뮬레이션 어려운 동작
- 트랜잭션 롤백 같은 호출 시퀀스 테스트

**Value 타입은 Mock 불필요** (직접 사용 또는 도메인별 변환)

### Integration 테스트에서 애플리케이션 객체 Mock

Callback 기반 라이브러리의 경우:
- 외부 라이브러리 → Adapter Callback → Application Callback
- Integration 테스트에서는 **애플리케이션 Callback을 Mock**하여 이벤트 변환 검증

---

## References

**Growing Object-Oriented Software, Guided by Test**
- 저자: Steve Freeman, Nat Pryce
- 출판: Addison-Wesley, 2009
- [목차](../../references/growing-object-oriented-software/toc.md)
- [섹션 매핑](../../references/growing-object-oriented-software/section_mapping.json)
