# Growing_object_oriented_software_guided_by_tests_Chapter_24_Test_Flexibility

## 압축 내용

테스트의 유연성은 정확히 필요한 것만 명시하고 불필요한 세부사항을 피함으로써 달성되며, 이를 통해 테스트가 깨지지 않으면서도 프로덕션 코드의 변경과 리팩토링을 가능하게 한다.

---

## 핵심 내용

### 1. 테스트 취약성(Test Brittleness)의 원인 [→ 상세 내용 1]
- **정의**: 테스트가 관련 없는 코드 변경으로 인해 쉽게 깨지는 현상
- **원인**:
  - 시스템의 무관한 부분과 너무 강하게 결합됨
  - 대상 코드의 예상 동작을 과도하게 명시함 (overspecify)
  - 여러 테스트가 동일한 프로덕션 코드 동작을 중복해서 검증함

### 2. 정밀한 명세 원칙(Specify Precisely) [→ 상세 내용 2]
- **핵심 규칙**: "일어나야 할 일을 정확히 명시하되, 그 이상은 명시하지 말라"
- **이점**:
  - 테스트가 무엇을 검증하는지 명확해짐
  - 무관한 차원에서의 코드 변경이 테스트를 깨뜨리지 않음
  - 테스트의 가독성과 탄력성이 비례 관계를 형성함

### 3. 정보 vs 표현(Information vs Representation) [→ 상세 내용 3]
- **원칙**: 테스트는 정보의 내용에 기반하여 작성되어야 하며, 정보의 표현 방식에 의존해서는 안 됨
- **기법**:
  - 의미 있는 값을 상수로 정의 (예: `NO_CUSTOMER_FOUND`)
  - 복잡한 구조는 Test Data Builder로 숨김
- **효과**: 시스템 다른 부분의 구현 변경으로부터 테스트를 보호함

### 4. 정밀한 단언문(Precise Assertions) [→ 상세 내용 4]
- **원칙**: 테스트 시나리오와 관련된 것만 단언함
- **기법**:
  - 테스트 입력으로부터 도출되지 않은 값은 단언하지 않음
  - 다른 테스트에서 다루는 동작은 재검증하지 않음
  - Hamcrest matcher 활용으로 표현력 높이기
- **예시**:
  - 값 자체보다는 관계 검증 (`largerThan`)
  - 문자열 포맷이 아닌 포함 여부 검증 (`containsString`)

### 5. 정밀한 기대값(Precise Expectations) [→ 상세 내용 5]
- **Mock 객체 테스트**: 테스트 대상 객체와 이웃 간의 관련된 상호작용 세부사항만 명시
- **파라미터 매칭**: 필요한 값만 정확히 검증하고 나머지는 무시
- **유연성**: 불필요한 제약을 피하여 구현 변경에 대응

### 6. Allowance vs Expectation [→ 상세 내용 6]
- **Allowance**: 매칭될 수도, 되지 않을 수도 있음 (유연한 stub)
- **Expectation**: 반드시 충족되어야 함 (엄격한 검증)
- **규칙**: "Query는 Allow, Command는 Expect"
  - Query: 세상을 변경하지 않음, 몇 번이든 호출 가능
  - Command: 부작용이 있음, 호출 횟수가 중요함

### 7. 무관한 객체 무시하기(Ignoring Irrelevant Objects) [→ 상세 내용 7]
- **목적**: 테스트를 단순하고 집중되게 유지
- **기법**: jMock의 `ignoring()` 절 사용
- **자동 반환값**: 무시된 메서드에 대해 타입별 "제로" 값 반환
- **주의사항**: 무시된 기능도 어딘가에서는 테스트되어야 함

### 8. 호출 순서(Invocation Order) [→ 상세 내용 8]
- **기본 원칙**: 순서가 중요할 때만 강제하라
- **Sequence**: 순서가 있는 호출 목록 정의
- **States**: 더 복잡한 순서 제약 표현 가능
- **유연성**: 최소한의 제약으로 구현 자유도 보장

### 9. jMock States의 활용 [→ 상세 내용 9]
- **세 가지 참여자 모델링**:
  - 테스트 대상 객체의 논리적 상태
  - 피어 객체의 상태 변화
  - 테스트 자체의 상태
- **장점**: 객체의 프로토콜을 구현이 아닌 논리적으로 표현

### 10. Guinea Pig 객체 [→ 상세 내용 10]
- **문제**: 어댑터 테스트가 도메인 모델 타입에 결합되면 취약해짐
- **해결책**: 테스트 전용 "기니피그" 타입 사용
- **이점**:
  - 테스트가 대표하는 기능이 명확해짐
  - 도메인 모델 변경으로부터 독립적
  - Self-Describing Value로 가독성 향상

---

## 상세 내용

### 목차
1. 테스트 취약성의 원인과 영향
2. 정밀한 명세의 중요성
3. 정보 vs 표현: null 사례 연구
4. 정밀한 단언문: 값 타입과 문자열
5. 정밀한 기대값과 파라미터 매칭
6. Allowance와 Expectation의 구분
7. 무관한 객체 무시하기
8. 호출 순서 제약하기
9. jMock States의 강력함
10. Guinea Pig 객체 패턴

---

### 1. 테스트 취약성의 원인과 영향

[섹션: Introduction, 페이지 298, 라인 11-33]

#### 테스트 취약성의 정의
시스템과 테스트 스위트가 성장함에 따라, 테스트가 신중하게 작성되지 않으면 유지보수 부담이 된다. **취약한 테스트(brittle tests)**는 개발 속도를 늦추고 리팩토링을 억제한다.

#### 테스트 취약성의 일반적인 원인

```java
// 1. 무관한 부분과의 과도한 결합
// 문제: 테스트가 시스템의 먼 부분 변경으로 실패함
@Test
public void processOrder() {
    // CustomerBase, PaymentGateway, EmailService 등
    // 많은 의존성이 직접 사용됨
    Order order = new Order(realCustomerBase, realPaymentGateway, realEmailService);
    order.process();
    // 어느 하나라도 변경되면 이 테스트가 깨짐
}

// 개선: 필요한 것만 stub
@Test
public void processOrder() {
    allowing(customerBase).findCustomer(anyString());
        will(returnValue(KNOWN_CUSTOMER));
    // 주문 처리 로직만 집중해서 테스트
}
```

```python
# Python 버전
# 1. 무관한 부분과의 과도한 결합
# 문제
def test_process_order(self):
    # 실제 의존성들이 모두 필요함
    order = Order(
        real_customer_base,
        real_payment_gateway,
        real_email_service
    )
    order.process()
    # 의존성 중 하나라도 변경되면 테스트가 깨짐

# 개선
def test_process_order(self):
    customer_base = Mock()
    customer_base.find_customer.return_value = KNOWN_CUSTOMER
    # 주문 처리 로직만 집중해서 테스트
    order = Order(customer_base, mock_payment, mock_email)
    order.process()
```

```java
// 2. 예상 동작의 과도한 명세
// 문제: 필요 이상으로 세부사항을 검증
@Test
public void sendsNotification() {
    oneOf(emailService).send(
        with("user@example.com"),           // 구체적 이메일
        with("Order Processed"),             // 구체적 제목
        with(containsString("Your order")),  // 구체적 내용
        with(equal(EmailFormat.HTML)),       // 구체적 포맷
        with(equal(Priority.NORMAL))         // 구체적 우선순위
    );
    // 이 중 하나만 변경되어도 테스트가 깨짐
}

// 개선: 본질만 검증
@Test
public void sendsNotification() {
    oneOf(emailService).send(
        with(any(String.class)),             // 이메일 주소는 어떤 것이든
        with(any(String.class)),             // 제목은 어떤 것이든
        with(containsString("Your order")),  // 핵심 정보만 검증
        with(any(EmailFormat.class)),        // 포맷은 무관
        with(any(Priority.class))            // 우선순위는 무관
    );
}
```

```python
# Python 버전
# 2. 예상 동작의 과도한 명세
# 문제
def test_sends_notification(self):
    email_service.send.assert_called_once_with(
        to="user@example.com",           # 구체적 이메일
        subject="Order Processed",       # 구체적 제목
        body=mock.ANY,
        format=EmailFormat.HTML,         # 구체적 포맷
        priority=Priority.NORMAL         # 구체적 우선순위
    )
    # 세부사항 변경 시 테스트 실패

# 개선
def test_sends_notification(self):
    # 본질만 검증
    email_service.send.assert_called_once()
    call_args = email_service.send.call_args
    assert "Your order" in call_args.kwargs['body']
    # 나머지는 검증하지 않음
```

```java
// 3. 중복된 테스트
// 문제: 여러 테스트가 같은 동작을 검증
@Test
public void calculatesTotal_singleItem() {
    cart.add(ITEM_A);
    assertEquals(10.0, cart.getTotal());  // 총액 계산 검증
}

@Test
public void calculatesTotal_multipleItems() {
    cart.add(ITEM_A);
    cart.add(ITEM_B);
    assertEquals(25.0, cart.getTotal());  // 총액 계산 또 검증
}

@Test
public void appliesDiscount() {
    cart.add(ITEM_A);
    cart.applyDiscount(0.1);
    assertEquals(9.0, cart.getTotal());   // 총액 계산 또 검증
}

// 개선: 각 테스트가 고유한 측면을 검증
@Test
public void sumsItemPrices() {
    cart.add(ITEM_A);
    cart.add(ITEM_B);
    assertEquals(25.0, cart.getTotal());  // 합계 계산만 검증
}

@Test
public void appliesDiscountToTotal() {
    cart.setTotal(100.0);  // 총액 계산은 검증하지 않음
    cart.applyDiscount(0.1);
    assertEquals(90.0, cart.getTotal());  // 할인 적용만 검증
}
```

```python
# Python 버전
# 3. 중복된 테스트
# 문제
def test_calculates_total_single_item(self):
    cart.add(ITEM_A)
    assert cart.get_total() == 10.0  # 총액 계산 검증

def test_calculates_total_multiple_items(self):
    cart.add(ITEM_A)
    cart.add(ITEM_B)
    assert cart.get_total() == 25.0  # 총액 계산 또 검증

def test_applies_discount(self):
    cart.add(ITEM_A)
    cart.apply_discount(0.1)
    assert cart.get_total() == 9.0   # 총액 계산 또 검증

# 개선
def test_sums_item_prices(self):
    cart.add(ITEM_A)
    cart.add(ITEM_B)
    assert cart.get_total() == 25.0  # 합계만 검증

def test_applies_discount_to_total(self):
    cart.set_total(100.0)  # 총액 계산은 건너뜀
    cart.apply_discount(0.1)
    assert cart.get_total() == 90.0  # 할인만 검증
```

#### 설계와의 관계

[라인 28-33]

테스트 취약성은 테스트 작성 방법뿐만 아니라 시스템 설계와도 관련이 있다. 객체가 많은 의존성을 가지거나 의존성이 숨겨져 있으면 환경에서 분리하기 어렵고, 시스템의 먼 부분이 변경될 때 테스트가 실패한다. 따라서 **테스트 취약성을 설계 품질에 대한 귀중한 피드백 소스로 활용**할 수 있다.

[관련 핵심 개념: 2. 정밀한 명세 원칙]

---

### 2. 정밀한 명세의 중요성

[섹션: Specify Precisely What Should Happen and No More, 페이지 299, 라인 42-48]

#### 핵심 규칙

```java
// 전체 챕터를 하나의 규칙으로 요약
// "일어나야 할 일을 정확히 명시하되, 그 이상은 명시하지 말라"
// (Specify Precisely What Should Happen and No More)

// 나쁜 예: 너무 많이 명시
@Test
public void processesPayment() {
    context.checking(new Expectations() {{
        // 불필요한 세부사항까지 모두 명시
        oneOf(logger).log("Starting payment");
        oneOf(validator).validate(payment);
        oneOf(gateway).connect("https://payment.example.com");
        oneOf(gateway).authenticate(API_KEY);
        oneOf(gateway).process(payment);
        oneOf(gateway).disconnect();
        oneOf(logger).log("Payment completed");
        oneOf(emailService).send(confirmation);
    }});

    paymentProcessor.process(payment);
}

// 좋은 예: 핵심만 명시
@Test
public void processesPayment() {
    context.checking(new Expectations() {{
        // 관련된 핵심 상호작용만 명시
        oneOf(gateway).process(payment);
        oneOf(emailService).send(with(confirmationFor(payment)));

        // 나머지는 무시하거나 허용
        ignoring(logger);
        allowing(gateway).connect(with(any(String.class)));
        allowing(gateway).authenticate(with(any(String.class)));
    }});

    paymentProcessor.process(payment);
}
```

```python
# Python 버전
# 나쁜 예: 너무 많이 명시
def test_processes_payment(self):
    # 불필요한 세부사항까지 모두 명시
    logger.log.assert_any_call("Starting payment")
    validator.validate.assert_called_once_with(payment)
    gateway.connect.assert_called_once_with("https://payment.example.com")
    gateway.authenticate.assert_called_once_with(API_KEY)
    gateway.process.assert_called_once_with(payment)
    gateway.disconnect.assert_called_once()
    logger.log.assert_any_call("Payment completed")
    email_service.send.assert_called_once_with(confirmation)

    payment_processor.process(payment)

# 좋은 예: 핵심만 명시
def test_processes_payment(self):
    # 핵심 상호작용만 검증
    payment_processor.process(payment)

    gateway.process.assert_called_once_with(payment)
    email_service.send.assert_called_once()

    # 확인 이메일이 올바른 지불 정보를 포함하는지만 검증
    sent_confirmation = email_service.send.call_args[0][0]
    assert sent_confirmation.payment_id == payment.id
```

#### JUnit, Hamcrest, jMock의 역할

이들 도구는 대상 코드로부터 정확히 원하는 것만 명시할 수 있게 해준다. 더 정확할수록:
- 코드가 무관한 차원에서 유연하게 변경될 수 있음
- 테스트가 깨지는 오류를 줄일 수 있음
- 무엇이 중요하고 중요하지 않은지 명확함

#### 가독성과 탄력성의 선순환

[라인 34-37]

테스트 가독성과 탄력성 사이에는 선순환 관계가 있다. 집중되고, 깔끔한 설정을 가지며, 중복이 최소화된 테스트는 이름 짓기가 쉽고 목적이 명확하다.

[관련 핵심 개념: 3. 정보 vs 표현, 4. 정밀한 단언문, 5. 정밀한 기대값]

---

### 3. 정보 vs 표현: null 사례 연구

[섹션: Test for Information, Not Representation, 페이지 299-300, 라인 49-108]

#### 문제 상황: null의 두 가지 문제점

```java
// 원래 인터페이스 (라인 60-64)
public interface CustomerBase {
    // Returns null if no customer found
    Customer findCustomerWithEmailAddress(String emailAddress);
    // [...]
}

// 테스트에서의 null 사용 (라인 68-69)
allowing(customerBase).findCustomerWithEmailAddress(theAddress);
    will(returnValue(null));
```

```python
# Python 버전
# 원래 인터페이스
class CustomerBase(Protocol):
    def find_customer_with_email_address(self, email_address: str) -> Optional[Customer]:
        """Returns None if no customer found"""
        ...

# 테스트에서의 null 사용
customer_base = Mock()
customer_base.find_customer_with_email_address.return_value = None
```

[라인 70-72]

**문제점**:
1. **가독성**: null이 여기서 무엇을 의미하는지, 언제 적절한지 기억해야 함 - 테스트가 자명하지 않음
2. **유지보수 비용**: 표현이 변경되면 모든 테스트를 수정해야 함

#### 설계 개선: Maybe 타입 도입

[라인 73-90]

```java
// 개선된 인터페이스 (라인 83-90)
public interface CustomerBase {
    Maybe<Customer> findCustomerWithEmailAddress(String emailAddress);
}

public abstract class Maybe<T> implements Iterable<T> {
    abstract boolean hasResult();
    public static Maybe<T> just(T oneValue) { /* ... */ }
    public static Maybe<T> nothing() { /* ... */ }
}
```

```python
# Python 버전
from typing import Generic, TypeVar, Iterator

T = TypeVar('T')

class Maybe(Generic[T]):
    """최대 하나의 결과를 담는 반복 가능한 컬렉션"""

    def has_result(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def just(value: T) -> 'Maybe[T]':
        return Just(value)

    @staticmethod
    def nothing() -> 'Maybe[T]':
        return Nothing()

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError

class Just(Maybe[T]):
    def __init__(self, value: T):
        self._value = value

    def has_result(self) -> bool:
        return True

    def __iter__(self) -> Iterator[T]:
        yield self._value

class Nothing(Maybe[T]):
    def has_result(self) -> bool:
        return False

    def __iter__(self) -> Iterator[T]:
        return iter([])

# 개선된 인터페이스
class CustomerBase(Protocol):
    def find_customer_with_email_address(self, email_address: str) -> Maybe[Customer]:
        ...
```

[라인 91-94]

**문제 발생**: null을 반환하는 기존 테스트들은 여전히 유효한 타입이므로 컴파일러가 경고할 수 없다. 모든 테스트가 실패하는 것을 지켜보고 하나씩 새 설계로 변경해야 한다.

#### 해결책: 의미 있는 상수 사용

[라인 95-101]

```java
// 개선 전 (라인 98)
public static final Customer NO_CUSTOMER_FOUND = null;

// 개선 후 (라인 100)
public static final Maybe<Customer> NO_CUSTOMER_FOUND = Maybe.nothing();

// 테스트 코드는 변경 불필요
allowing(customerBase).findCustomerWithEmailAddress(theAddress);
    will(returnValue(NO_CUSTOMER_FOUND));
```

```python
# Python 버전
# 개선 전
NO_CUSTOMER_FOUND = None

# 개선 후
NO_CUSTOMER_FOUND: Maybe[Customer] = Maybe.nothing()

# 테스트 코드는 변경 불필요
customer_base.find_customer_with_email_address.return_value = NO_CUSTOMER_FOUND
```

#### 핵심 원칙

[라인 102-108]

테스트는 **객체 간 전달되는 정보의 내용**으로 작성되어야 하며, **정보가 표현되는 방식**으로 작성되어서는 안 된다. 이렇게 하면:
1. 테스트가 더 자명해짐
2. 시스템의 다른 곳에서 제어되는 구현 변경으로부터 보호됨

**권장사항**:
- `NO_CUSTOMER_FOUND` 같은 중요한 값은 상수로 한 곳에 정의
- 더 복잡한 구조는 Test Data Builder로 숨김 (Chapter 22 참조)
- Chapter 12의 `UNUSED_CHAT` 예시 참조

[관련 핵심 개념: 4. 정밀한 단언문, 10. Guinea Pig 객체]

---

### 4. 정밀한 단언문: 값 타입과 문자열

[섹션: Precise Assertions, 페이지 300-301, 라인 109-168]

#### 핵심 원칙

[라인 110-116]

- 테스트 시나리오와 관련된 것만 단언
- 테스트 입력으로부터 도출되지 않은 값은 단언하지 말 것
- 다른 테스트에서 다루는 동작은 재검증하지 말 것

**이점**:
- 각 메서드가 대상 코드 동작의 고유한 측면을 검증
- 무관한 결과에 의존하지 않아 견고함
- 중복이 적음

#### 구조화된 값 타입 검증

[라인 128-134]

```java
// 나쁜 예: 전체 객체 비교
assertEquals(expectedInstrument, actualInstrument);

// 좋은 예: 관련 속성만 검증 (라인 133)
assertEquals("strike price", 92, instrument.getStrikePrice());
// 전체 instrument를 비교하지 않음
```

```python
# Python 버전
# 나쁜 예: 전체 객체 비교
assert actual_instrument == expected_instrument

# 좋은 예: 관련 속성만 검증
assert instrument.strike_price == 92, "strike price"
# 전체 instrument를 비교하지 않음
```

#### Hamcrest Matcher 활용

[라인 135-141]

```java
// 관계 검증 (라인 138)
assertThat(instrument.getTransactionId(),
           largerThan(PREVIOUS_TRANSACTION_ID));
// 실제 값이 아니라 이전 값보다 큰지만 검증
// 새 식별자가 이전 것보다 크다는 것만 중요
```

```python
# Python 버전
from hamcrest import assert_that, greater_than

# 관계 검증
assert_that(instrument.transaction_id,
            greater_than(PREVIOUS_TRANSACTION_ID))
# 실제 값이 아니라 관계만 검증
```

#### 문자열 단언의 정밀성

[라인 142-158]

```java
// 문제: 전체 문자열 검증
assertEquals("ERROR: Strike price 92 for instrument FGD.430 is expired at 2024-01-15 14:23:45",
             failureMessage);
// 포맷, 공백, 타임스탬프 변경 시 테스트 실패

// 해결책: 핵심 정보만 검증 (라인 152-155)
assertThat(failureMessage,
           allOf(containsString("strikePrice=92"),
                 containsString("id=FGD.430"),
                 containsString("is expired")));
// 이 문자열들이 어딘가에 포함되기만 하면 됨
```

```python
# Python 버전
# 문제: 전체 문자열 검증
assert failure_message == "ERROR: Strike price 92 for instrument FGD.430 is expired at 2024-01-15 14:23:45"
# 포맷 변경 시 테스트 실패

# 해결책: 핵심 정보만 검증
assert "strikePrice=92" in failure_message
assert "id=FGD.430" in failure_message
assert "is expired" in failure_message
# 문자열들이 포함되기만 하면 됨
```

#### 중간 구조 객체의 필요성 인식

[라인 159-164]

텍스트 문자열에 대한 정밀한 단언을 작성하려는 노력은 종종 **중간 구조 객체가 빠져있음**을 시사한다.

```java
// 개선: InstrumentFailure 구조화된 값 객체 도입
public class InstrumentFailure {
    private final String instrumentId;
    private final double strikePrice;
    private final FailureReason reason;
    // ...
}

// 대부분의 코드는 InstrumentFailure로 작성
InstrumentFailure failure = new InstrumentFailure("FGD.430", 92, EXPIRED);

// 문자열 변환은 마지막 순간에만
String message = failure.toString();

// 문자열 변환은 별도로 격리되어 테스트
@Test
public void formatsFailureMessage() {
    InstrumentFailure failure = new InstrumentFailure("FGD.430", 92, EXPIRED);
    assertThat(failure.toString(),
               containsString("strikePrice=92"));
}
```

```python
# Python 버전
from dataclasses import dataclass
from enum import Enum

class FailureReason(Enum):
    EXPIRED = "expired"
    INVALID = "invalid"

@dataclass
class InstrumentFailure:
    """금융 상품 실패를 나타내는 구조화된 값 객체"""
    instrument_id: str
    strike_price: float
    reason: FailureReason

    def __str__(self) -> str:
        return f"Instrument {self.instrument_id} with strikePrice={self.strike_price} is {self.reason.value}"

# 대부분의 코드는 InstrumentFailure로 작성
failure = InstrumentFailure("FGD.430", 92, FailureReason.EXPIRED)

# 문자열 변환은 마지막 순간에만
message = str(failure)

# 문자열 변환은 별도로 격리되어 테스트
def test_formats_failure_message(self):
    failure = InstrumentFailure("FGD.430", 92, FailureReason.EXPIRED)
    assert "strikePrice=92" in str(failure)
```

[관련 핵심 개념: 5. 정밀한 기대값]

---

### 5. 정밀한 기대값과 파라미터 매칭

[섹션: Precise Expectations, 페이지 302, 라인 170-180]

#### 개념 확장

[라인 171-180]

단언에 대한 정밀성 개념을 **기대값(expectations)**으로 확장할 수 있다. 각 mock 객체 테스트는 테스트 대상 객체와 이웃 간의 **관련된 상호작용 세부사항만** 명시해야 한다.

결합된 단위 테스트들은 객체가 시스템의 나머지 부분과 통신하기 위한 **프로토콜을 설명**한다.

jMock은 이러한 객체 간 통신을 가능한 한 정확하게 명시하도록 많은 지원을 내장했다.

#### 정밀한 파라미터 매칭

[섹션: Precise Parameter Matching, 페이지 302, 라인 181-197]

[라인 182-186]

```java
// Chapter 21 예시 (라인 184-185)
// 특정 클래스가 아닌 어떤 RuntimeException이든 허용
oneOf(listener).handleFailure(with(any(RuntimeException.class)));

// Chapter 16 예시 (라인 187)
oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
```

```python
# Python 버전
from unittest.mock import Mock, ANY

# 어떤 RuntimeException이든 허용
listener.handle_failure.assert_called_once_with(ANY)

# 특정 itemId를 가진 sniper만 검증
auction.add_auction_event_listener.assert_called_once()
sniper = auction.add_auction_event_listener.call_args[0][0]
assert sniper.item_id == item_id
# 나머지 상태(현재 입찰가, 최종 가격 등)는 검증하지 않음
```

[라인 188-191]

`sniperForItem()` 메서드는 AuctionSniper가 주어졌을 때 **item 식별자만 확인**하는 Matcher를 반환한다. 이 테스트는 sniper의 다른 상태(현재 입찰가, 최종 가격 등)는 신경 쓰지 않으므로, 그 값들을 확인하여 테스트를 더 취약하게 만들지 않는다.

#### 입력 문자열에 대한 정밀한 기대값

[라인 192-197]

```java
// 문자열 파라미터에도 동일한 정밀성 적용
oneOf(auditTrail).recordFailure(
    with(allOf(containsString("strikePrice=92"),
               containsString("id=FGD.430"),
               containsString("is expired"))));
```

```python
# Python 버전
from unittest.mock import call

# 문자열 파라미터에도 정밀성 적용
audit_trail.record_failure.assert_called_once()
failure_msg = audit_trail.record_failure.call_args[0][0]
assert "strikePrice=92" in failure_msg
assert "id=FGD.430" in failure_msg
assert "is expired" in failure_msg
```

[관련 핵심 개념: 6. Allowance vs Expectation]

---

### 6. Allowance와 Expectation의 구분

[섹션: Allowances and Expectations, 페이지 302-304, 라인 198-254]

#### 기본 개념

[라인 199-204]

- **Expectation**: 테스트 중에 반드시 충족되어야 함
- **Allowance**: 매칭될 수도, 되지 않을 수도 있음

**구분의 목적**: 특정 테스트에서 무엇이 중요한지 강조하기 위함. 기대값은 테스트하는 프로토콜에 필수적인 상호작용을 설명한다.

#### Allowance의 용도

[라인 205-222]

```java
// Chapter 13 예시 (라인 212-216)
ignoring(auction);  // 이 테스트에서는 auction 메시지 무관

allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
    then(sniperState.is("bidding"));
// sniperStateChanged 호출이 매칭될 수 있지만 필수는 아님
```

```python
# Python 버전
# auction은 무시 (다른 테스트에서 다룸)
auction = Mock()

# sniper 리스너는 호출될 수도 있음
sniper_listener = Mock()
# BIDDING 상태인 sniper로 호출되면 상태 기록
def record_state(snapshot):
    if snapshot.state == BIDDING:
        sniper_state.become("bidding")

sniper_listener.sniper_state_changed.side_effect = record_state
```

**Allowance 용도**:
1. **Stub으로 값 주입**: 객체를 올바른 상태로 만들기 위해 값을 제공
2. **무관한 상호작용 무시**: 현재 테스트와 관련 없는 상호작용 무시

[라인 223-227]

```java
// Action 절을 allowance에 연결하여 값 반환
allowing(catalog).getPriceForItem(item);
    will(returnValue(74));
// 테스트 후반부에 사용할 가격 반환
```

```python
# Python 버전
catalog = Mock()
catalog.get_price_for_item.return_value = 74
# 테스트 후반부에 사용할 가격 반환
```

#### Allow Queries; Expect Commands

[라인 228-241]

**Command** [라인 231-234]:
- 부작용이 있고 대상 객체 밖의 세상을 변경할 가능성이 있는 호출
- 예: `auditTrail.recordFailure()` - 로그 내용 변경
- 호출 횟수가 다르면 시스템 상태가 달라짐
- **→ Expect 사용**

```java
// Command는 expect
oneOf(auditTrail).recordFailure(failureMessage);
// 정확히 한 번 호출되어야 함
```

```python
# Python 버전
# Command는 expect
audit_trail.record_failure.assert_called_once_with(failure_message)
```

**Query** [라인 235-237]:
- 세상을 변경하지 않음
- 몇 번이든 호출 가능 (0번 포함)
- 예: `catalog.getPriceForItem()` - 몇 번을 물어봐도 시스템에 차이 없음
- **→ Allow 사용**

```java
// Query는 allow
allowing(catalog).getPriceForItem(item);
    will(returnValue(74));
// 몇 번이든 호출 가능
```

```python
# Python 버전
# Query는 allow
catalog.get_price_for_item.return_value = 74
# 호출 횟수 검증 안 함
```

[라인 238-241]

이 규칙은 테스트를 대상 객체로부터 분리하는 데 도움이 된다. 구현이 변경되어도 (예: 캐싱 도입, 다른 알고리즘 사용) 테스트는 여전히 유효하다. 반면, 캐시를 테스트한다면 쿼리가 정확히 몇 번 이루어졌는지 알고 싶을 것이다.

#### Cardinality 절

[라인 242-254]

```java
// Chapter 9 예시 (라인 246)
atLeast(1).of(sniperListener).sniperBidding();
// 호출이 이루어지는 것은 중요하지만 횟수는 중요하지 않음
```

```python
# Python 버전
# 최소 한 번은 호출되어야 함
sniper_listener.sniper_bidding.assert_called()
# assert_called()는 최소 1회 호출 보장
```

**Cardinality 절의 종류** (Appendix A에 전체 목록):
- `oneOf(...)`: 정확히 1번
- `atLeast(n).of(...)`: 최소 n번
- `atMost(n).of(...)`: 최대 n번
- `between(min, max).of(...)`: min~max번
- `allowing(...)`: 0번 이상

[관련 핵심 개념: 7. 무관한 객체 무시하기]

---

### 7. 무관한 객체 무시하기

[섹션: Ignoring Irrelevant Objects, 페이지 304, 라인 255-293]

#### 기본 개념

[라인 256-260]

협력자가 실행 중인 기능과 관련이 없으면 "ignoring"하여 테스트를 단순화할 수 있다. jMock은 무시된 객체에 대한 어떤 호출도 확인하지 않는다.

**이점**:
- 테스트가 단순하고 집중적으로 유지됨
- 무엇이 중요한지 즉시 알 수 있음
- 한 측면의 코드 변경이 무관한 테스트를 깨뜨리지 않음

#### Zero 값 자동 반환

[라인 261-276]

편의를 위해 jMock은 무시된 메서드가 값을 반환할 때 타입에 따라 "제로" 결과를 제공한다:

| 타입 | "Zero" 값 |
|------|----------|
| Boolean | false |
| Numeric type | 0 |
| String | "" (빈 문자열) |
| Array | 빈 배열 |
| Mockery로 mock 가능한 타입 | 무시된 mock |
| 기타 타입 | null |

```java
// 무시된 메서드의 자동 반환값 예시
ignoring(calculator);

// 이후 호출들은 자동으로 제로 값 반환
int result = calculator.add(1, 2);        // 0 반환
boolean valid = calculator.isValid();     // false 반환
String name = calculator.getName();       // "" 반환
double[] values = calculator.getValues(); // 빈 배열 반환
```

```python
# Python 버전 - Mock 설정
from unittest.mock import Mock, MagicMock

calculator = MagicMock()  # MagicMock은 자동으로 기본값 반환

# 이후 호출들은 자동으로 Mock/기본값 반환
result = calculator.add(1, 2)        # Mock 객체 반환
valid = calculator.is_valid()        # Mock 객체 반환
name = calculator.get_name()         # Mock 객체 반환
values = calculator.get_values()     # Mock 객체 반환
```

#### 동적 Mock 반환의 강력함

[라인 277-283]

```java
// JPA 예시
ignoring(entityManagerFactory);
// factory는 무시된 EntityManager를 반환
// EntityManager는 무시된 EntityTransaction을 반환
// EntityTransaction의 commit(), rollback()은 무시됨

// 하나의 ignore 절로 트랜잭션 관련 모든 것을 비활성화
// 테스트는 코드의 도메인 동작에만 집중
```

```python
# Python 버전
from unittest.mock import MagicMock

# JPA 유사 예시
entity_manager_factory = MagicMock()

# factory, manager, transaction 모두 자동으로 Mock 반환
manager = entity_manager_factory.create_entity_manager()
transaction = manager.get_transaction()
transaction.commit()  # 아무것도 확인하지 않음
transaction.rollback()  # 아무것도 확인하지 않음
```

#### 주의사항

[라인 284-291]

모든 "파워 툴"처럼 `ignoring()`은 주의해서 사용해야 한다:

1. **무시된 객체의 연쇄**는 새로운 협력자로 분리되어야 할 기능을 제안할 수 있음
2. **무시된 기능도 어딘가에서는 테스트**되어야 함
3. **고수준 테스트**로 모든 것이 함께 작동하는지 확인해야 함

실제로는 보통 기본 테스트가 완료된 후 특수 테스트를 작성할 때만 `ignoring()`을 도입한다.

[관련 핵심 개념: 8. 호출 순서]

---

### 8. 호출 순서 제약하기

[섹션: Invocation Order, 페이지 305-307, 라인 294-413]

#### 기본 원칙

[라인 296-306]

jMock은 mock 객체에 대한 호출이 **어떤 순서로든** 이루어질 수 있도록 허용한다. 기대값을 선언한 순서와 동일할 필요가 없다.

**Only Enforce Invocation Order When It Matters**

상호작용 순서에 대해 덜 말할수록, 코드 구현에서 더 많은 유연성을 가진다. 테스트 구조화에도 유연성을 얻는다.

```java
// 순서 제약이 없으면 helper 메서드로 기대값 패키징 가능
private void expectValidPayment() {
    oneOf(validator).validate(payment);
}

private void expectSuccessfulProcessing() {
    oneOf(gateway).process(payment);
}

@Test
public void processesValidPayment() {
    // 순서와 무관하게 호출 가능
    expectSuccessfulProcessing();
    expectValidPayment();

    processor.process(payment);
}
```

```python
# Python 버전
def expect_valid_payment(self):
    self.validator.validate.assert_called_once_with(self.payment)

def expect_successful_processing(self):
    self.gateway.process.assert_called_once_with(self.payment)

def test_processes_valid_payment(self):
    # 순서와 무관하게 검증 가능
    self.processor.process(self.payment)

    self.expect_valid_payment()
    self.expect_successful_processing()
```

#### Sequence를 사용한 순서 제약

[라인 307-358]

**문제 상황** [라인 313-331]:

```java
// AuctionSearcher: 경매를 검색하고 매칭되면 알림
// searchMatched() -> 매칭 발견 시 호출
// searchFinished() -> 모든 경매 확인 완료 시 호출

// 첫 시도 (라인 321-330)
@Test public void announcesMatchForOneAuction() {
    final AuctionSearcher auctionSearch =
        new AuctionSearcher(searchListener, asList(STUB_AUCTION1));

    context.checking(new Expectations() {{
        oneOf(searchListener).searchMatched(STUB_AUCTION1);
        oneOf(searchListener).searchFinished();
    }});

    auctionSearch.searchFor(KEYWORDS);
}
```

```python
# Python 버전
def test_announces_match_for_one_auction(self):
    auction_search = AuctionSearcher(
        self.search_listener,
        [STUB_AUCTION1]
    )

    # 문제: searchFinished가 searchMatched보다 먼저 호출될 수 있음
    auction_search.search_for(KEYWORDS)

    self.search_listener.search_matched.assert_called_once_with(STUB_AUCTION1)
    self.search_listener.search_finished.assert_called_once()
```

**문제**: `searchFinished()`가 `searchMatched()`보다 먼저 호출되는 것을 막을 수 없다. 프로토콜을 설명하지 못했다.

**해결책: Sequence 추가** [라인 348-358]:

```java
@Test public void announcesMatchForOneAuction() {
    final AuctionSearcher auctionSearch =
        new AuctionSearcher(searchListener, asList(STUB_AUCTION1));

    context.checking(new Expectations() {{
        Sequence events = context.sequence("events");

        oneOf(searchListener).searchMatched(STUB_AUCTION1);
            inSequence(events);
        oneOf(searchListener).searchFinished();
            inSequence(events);
    }});

    auctionSearch.searchFor(KEYWORDS);
}
```

```python
# Python 버전 - call_args_list로 순서 검증
def test_announces_match_for_one_auction(self):
    auction_search = AuctionSearcher(
        self.search_listener,
        [STUB_AUCTION1]
    )

    auction_search.search_for(KEYWORDS)

    # 호출 순서 검증
    calls = self.search_listener.method_calls
    assert calls[0] == call.search_matched(STUB_AUCTION1)
    assert calls[1] == call.search_finished()
```

**복수 매칭** [라인 360-372]:

```java
@Test public void announcesMatchForTwoAuctions() {
    final AuctionSearcher auctionSearch =
        new AuctionSearcher(searchListener,
                           asList(STUB_AUCTION1, STUB_AUCTION2));

    context.checking(new Expectations() {{
        Sequence events = context.sequence("events");

        oneOf(searchListener).searchMatched(STUB_AUCTION1);
            inSequence(events);
        oneOf(searchListener).searchMatched(STUB_AUCTION2);
            inSequence(events);
        oneOf(searchListener).searchFinished();
            inSequence(events);
    }});

    auctionSearch.searchFor(KEYWORDS);
}
```

```python
# Python 버전
def test_announces_match_for_two_auctions(self):
    auction_search = AuctionSearcher(
        self.search_listener,
        [STUB_AUCTION1, STUB_AUCTION2]
    )

    auction_search.search_for(KEYWORDS)

    # 호출 순서 검증
    calls = self.search_listener.method_calls
    assert calls[0] == call.search_matched(STUB_AUCTION1)
    assert calls[1] == call.search_matched(STUB_AUCTION2)
    assert calls[2] == call.search_finished()
```

#### States를 사용한 유연한 순서 제약

[라인 373-404]

**질문** [라인 373-376]: 경매를 초기화 순서대로 매칭해야 하는가? 검색이 종료되기 전에 올바른 매칭이 이루어지기만 하면 되는 것 아닌가?

**해결책: States 객체** [라인 377-404]:

```java
@Test public void announcesMatchForTwoAuctions() {
    final AuctionSearcher auctionSearch =
        new AuctionSearcher(searchListener,
                           asList(STUB_AUCTION1, STUB_AUCTION2));

    context.checking(new Expectations() {{
        States searching = context.states("searching");

        // 매칭은 finished 상태가 아닐 때만
        oneOf(searchListener).searchMatched(STUB_AUCTION1);
            when(searching.isNot("finished"));
        oneOf(searchListener).searchMatched(STUB_AUCTION2);
            when(searching.isNot("finished"));

        // 완료 시 finished 상태로 전환
        oneOf(searchListener).searchFinished();
            then(searching.is("finished"));
    }});

    auctionSearch.searchFor(KEYWORDS);
}
```

```python
# Python 버전 - 상태 머신 개념
class SearchingStates:
    def __init__(self):
        self.state = "searching"

    def finish(self):
        self.state = "finished"

    def is_finished(self):
        return self.state == "finished"

def test_announces_match_for_two_auctions(self):
    searching = SearchingStates()

    def on_finished():
        searching.finish()

    self.search_listener.search_finished.side_effect = on_finished

    auction_search = AuctionSearcher(
        self.search_listener,
        [STUB_AUCTION1, STUB_AUCTION2]
    )

    auction_search.search_for(KEYWORDS)

    # 매칭은 순서 무관, 완료는 마지막
    assert self.search_listener.search_matched.call_count == 2
    assert searching.is_finished()
```

**동작**:
- 테스트 시작 시 `searching`은 정의되지 않은 (기본) 상태
- `searching`이 finished가 아니면 매칭 보고 가능
- 완료 보고 시 `then()` 절이 `searching`을 finished로 전환
- 이후 추가 매칭이 차단됨

#### States와 Sequences 결합

[라인 405-413]

경매가 순서대로 매칭되어야 한다면, 매칭만을 위한 sequence를 기존 states와 함께 추가할 수 있다. 기대값은 여러 states와 sequences에 속할 수 있다.

실제로는 이런 복잡성이 드물며, 보통 외부 이벤트 피드에 응답할 때 나타난다. 항상 더 작고 단순한 조각으로 분해해야 한다는 힌트로 받아들인다.

[관련 핵심 개념: 9. jMock States의 활용]

---

### 9. jMock States의 강력함

[섹션: The Power of jMock States, 페이지 308, 라인 426-450]

#### States의 다양한 용도

[라인 427-429]

jMock States는 테스트의 세 가지 참여자를 모델링하는 데 사용할 수 있다:
1. 테스트 대상 객체
2. 피어 객체
3. 테스트 자체

#### 1. 테스트 대상 객체의 논리적 상태

[라인 430-437]

```java
// 위 예시의 searching states
// 테스트 대상 객체(AuctionSearcher)의 상태를 표현
States searching = context.states("searching");

// 객체가 보내는 이벤트를 듣고 상태 전환 트리거
oneOf(searchListener).searchFinished();
    then(searching.is("finished"));

// 프로토콜을 위반하는 이벤트 거부
oneOf(searchListener).searchMatched(auction);
    when(searching.isNot("finished"));
```

```python
# Python 버전
class ObjectState:
    """테스트 대상 객체의 논리적 상태"""
    def __init__(self):
        self.state = "initial"

    def transition_to(self, new_state):
        self.state = new_state

    def is_not(self, state):
        return self.state != state

# 사용
object_state = ObjectState()

def on_finished():
    object_state.transition_to("finished")

search_listener.search_finished.side_effect = on_finished
```

**중요**: Chapter 13 "Representing Object State"에서 설명한 것처럼, 이는 테스트 대상 객체의 **논리적 표현**이다. States는 테스트가 객체에 대해 관련 있다고 생각하는 것을 설명하지, 내부 구조를 설명하지 않는다. 객체의 구현을 제약하고 싶지 않다.

#### 2. 피어 객체의 상태 변화

[라인 438-445]

```java
// 피어가 테스트 대상 객체에 의해 호출되면서 상태가 변경됨
States listenerState = context.states("listenerState");

// 리스너가 준비되면 상태 전환
allowing(searchListener).isReady();
    will(returnValue(true));
    then(listenerState.is("ready"));

// 리스너가 준비된 상태에서만 결과 받을 수 있음
oneOf(searchListener).searchMatched(STUB_AUCTION1);
    when(listenerState.is("ready"));
```

```python
# Python 버전
class PeerState:
    """피어 객체의 상태"""
    def __init__(self):
        self.ready = False

    def become_ready(self):
        self.ready = True

peer_state = PeerState()

def on_is_ready():
    peer_state.become_ready()
    return True

search_listener.is_ready.side_effect = on_is_ready

# 사용 시 ready 상태 확인
def on_search_matched(auction):
    assert peer_state.ready, "Listener must be ready"

search_listener.search_matched.side_effect = on_search_matched
```

#### 3. 테스트 자체의 상태

[라인 446-450]

```java
// 테스트가 설정 중일 때 일부 상호작용 무시
States testState = context.states("testState");

ignoring(auction);
    when(testState.isNot("running"));

testState.become("running");

oneOf(auction).bidMore();
    when(testState.is("running"));
```

```python
# Python 버전
class TestState:
    """테스트 자체의 상태"""
    def __init__(self):
        self.phase = "setup"

    def start_running(self):
        self.phase = "running"

    def is_running(self):
        return self.phase == "running"

test_state = TestState()

# 설정 단계에서는 auction 호출 무시
# ...

test_state.start_running()

# 실행 단계에서만 검증
def on_bid_more():
    assert test_state.is_running(), "Test must be running"

auction.bid_more.side_effect = on_bid_more
```

[관련 핵심 개념: 8. 호출 순서, 10. Guinea Pig 객체]

---

### 10. Guinea Pig 객체 패턴

[섹션: "Guinea Pig" Objects, 페이지 309-310, 라인 465-537]

#### 문제 상황

[라인 466-476]

"ports and adapters" 아키텍처에서 어댑터는 애플리케이션 도메인 객체를 시스템의 기술 인프라에 매핑한다. 대부분의 어댑터 구현은 **제네릭**이다 (예: 리플렉션 사용).

어댑터 코드 테스트 시 가장 쉬운 접근은 애플리케이션 도메인 모델의 타입을 사용하는 것이지만, 이는 테스트를 취약하게 만든다:
- 애플리케이션과 어댑터 도메인을 결합시킴
- 관심사를 분리하지 못함
- 애플리케이션 모델 변경 시 테스트가 오도하여 깨짐

#### 나쁜 예: 도메인 타입 사용

[라인 477-490]

```java
// XmlMarshaller 테스트 (라인 481-490)
public class XmlMarshallerTest {
    @Test public void
    marshallsAndUnmarshallsSerialisableFields() {
        XMLMarshaller marshaller = new XmlMarshaller();

        // 문제: 프로덕션 도메인 타입 사용
        AuctionClosedEvent original =
            new AuctionClosedEventBuilder().build();

        String xml = marshaller.marshall(original);
        AuctionClosedEvent unmarshalled =
            marshaller.unmarshall(xml);

        assertThat(unmarshalled,
                   hasSameSerialisableFieldsAs(original));
    }
}
```

```python
# Python 버전 - 나쁜 예
class XmlMarshallerTest(unittest.TestCase):
    def test_marshalls_and_unmarshalls_serialisable_fields(self):
        marshaller = XmlMarshaller()

        # 문제: 프로덕션 도메인 타입 사용
        original = AuctionClosedEventBuilder().build()

        xml = marshaller.marshall(original)
        unmarshalled = marshaller.unmarshall(xml)

        assert_has_same_serialisable_fields(unmarshalled, original)
```

**문제점** [라인 491-503]:

1. **불필요한 결합**: `AuctionClosedEvent`를 삭제하려 해도 테스트가 사용 중이어서 실패
2. **테스트 가정 파괴 감지 못함**:
   - 처음에는 transient와 non-transient 필드 모두 있어서 모든 경로 검증
   - 나중에 transient 필드 제거 → 테스트가 더 이상 의미 없지만 실패하지 않음
   - 중요한 기능이 커버되지 않는 것을 경고하지 못함

#### 좋은 예: Guinea Pig 객체

[라인 509-535]

```java
// 개선된 테스트 (라인 512-530)
public class XmlMarshallerTest {
    // 테스트 전용 helper 클래스
    public static class MarshalledObject {
        private String privateField = "private";
        public final String publicFinalField = "public final";
        public int primitiveField;
        // constructors, accessors for private field, etc.
    }

    public static class WithTransient extends MarshalledObject {
        public transient String transientField = "transient";
    }

    @Test public void
    marshallsAndUnmarshallsSerialisableFields() {
        XMLMarshaller marshaller = new XmlMarshaller();

        // Guinea pig 객체 사용
        WithTransient original = new WithTransient();

        String xml = marshaller.marshall(original);
        AuctionClosedEvent unmarshalled =
            marshaller.unmarshall(xml);

        assertThat(unmarshalled,
                   hasSameSerialisableFieldsAs(original));
    }
}
```

```python
# Python 버전 - 좋은 예
class XmlMarshallerTest(unittest.TestCase):
    # 테스트 전용 helper 클래스
    class MarshalledObject:
        """직렬화 가능한 기본 객체"""
        def __init__(self):
            self._private_field = "private"
            self.public_final_field = "public final"
            self.primitive_field = 0

    class WithTransient(MarshalledObject):
        """transient 필드를 가진 객체"""
        def __init__(self):
            super().__init__()
            # Python은 transient 개념이 없으므로
            # __getstate__/__setstate__로 제어
            self._transient_field = "transient"

        def __getstate__(self):
            state = self.__dict__.copy()
            # transient 필드 제외
            state.pop('_transient_field', None)
            return state

    def test_marshalls_and_unmarshalls_serialisable_fields(self):
        marshaller = XmlMarshaller()

        # Guinea pig 객체 사용
        original = self.WithTransient()

        xml = marshaller.marshall(original)
        unmarshalled = marshaller.unmarshall(xml)

        assert_has_same_serialisable_fields(unmarshalled, original)
```

#### Guinea Pig 패턴의 이점

[라인 531-535]

1. **철저한 검증**: 프로덕션 도메인 모델에 적용하기 전에 XmlMarshaller의 동작을 완전히 검증
2. **가독성 향상**: `WithTransient` 클래스와 필드는 "Self-Describing Value"의 예시
   - 이름이 테스트에서의 역할을 반영
3. **독립성**: 도메인 모델 변경과 무관
4. **명확한 의도**: 각 필드가 테스트에서 검증하는 기능을 명확히 나타냄

[관련 핵심 개념: 3. 정보 vs 표현]

---

## 관계도

```
테스트 취약성 원인 (1)
    ↓ 해결책
정밀한 명세 원칙 (2)
    ↓ 적용
    ├─→ 정보 vs 표현 (3)
    │       └─→ Guinea Pig 객체 (10)
    ├─→ 정밀한 단언문 (4)
    │       ↓
    ├─→ 정밀한 기대값 (5)
    │       ↓
    └─→ Allowance vs Expectation (6)
            ↓
        무관한 객체 무시 (7)
            ↓
        호출 순서 제약 (8)
            ↓
        jMock States 활용 (9)
```

## 주요 교훈

1. **단일 규칙**: "일어나야 할 일을 정확히 명시하되, 그 이상은 명시하지 말라"
2. **정보 우선**: 표현이 아닌 정보로 테스트 작성
3. **Query는 Allow, Command는 Expect**: 부작용 유무로 구분
4. **순서는 필요할 때만**: 최소한의 제약으로 유연성 확보
5. **Guinea Pig 패턴**: 어댑터 테스트는 도메인 모델과 분리
6. **States의 다양한 용도**: 객체, 피어, 테스트 상태 모두 모델링 가능
7. **테스트 취약성은 설계 피드백**: 취약한 테스트는 설계 문제를 시사
