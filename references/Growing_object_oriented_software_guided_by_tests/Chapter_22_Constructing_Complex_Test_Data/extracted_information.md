# Growing_object_oriented_software_guided_by_tests_Chapter_22_Constructing_Complex_Test_Data

## 압축 내용

테스트 데이터 빌더 패턴을 사용해 복잡한 테스트 객체 생성을 간소화하고, 팩토리 메서드와 결합하여 테스트 코드를 선언적이고 표현력 있게 만들며, 궁극적으로 비즈니스 의도를 명확히 전달하는 가독성 높은 테스트를 작성하는 방법

## 핵심 내용

### 핵심 개념

1. **테스트에서의 객체 생성 문제** (→ 상세 내용 1)
   - 불변 객체와 엄격한 생성자 사용 시 테스트 코드가 장황해지고 읽기 어려워짐
   - 객체 생성 코드가 테스트 의도를 가리고, 구조 변경 시 많은 테스트가 깨지는 취약성 발생
   - Object Mother 패턴은 변형이 많아질수록 무수한 팩토리 메서드가 필요해 유지보수가 어려움

2. **테스트 데이터 빌더 (Test Data Builder)** (→ 상세 내용 2)
   - 빌더 패턴을 활용해 각 생성자 파라미터를 안전한 기본값으로 초기화한 필드로 관리
   - 체이닝 가능한 메서드로 필요한 값만 오버라이드하고 build() 메서드로 객체 생성
   - 테스트 표현력 향상, 변경에 대한 복원력 증가, 구문 노이즈 감소 효과
   - 메서드 이름으로 파라미터 목적이 명확해져 실수 발견이 쉬워짐

3. **유사 객체 생성 전략** (→ 상세 내용 3)
   - 공통 상태로 하나의 빌더를 초기화하고 차이나는 값만 변경하여 여러 객체 생성
   - 복사 생성자나 but() 메서드로 빌더 상태를 복제하여 의도치 않은 상태 공유 방지
   - 복잡한 설정에서는 함수형 접근으로 각 메서드가 새 빌더 복사본을 반환하도록 구현

4. **빌더 결합 (Combining Builders)** (→ 상세 내용 4)
   - 빌더가 다른 빌더를 직접 인자로 받아 build() 호출을 줄여 코드 간소화
   - 중요 정보(무엇을 생성하는가)에 집중하고 빌더 인프라 코드를 제거
   - 중첩된 객체 구조를 더 읽기 쉽게 표현

5. **팩토리 메서드로 도메인 모델 강조** (→ 상세 내용 5)
   - 빌더 생성을 팩토리 메서드로 감싸 코드를 더욱 압축 (예: anOrder(), aCustomer())
   - 메서드 오버로딩을 활용해 with() 메서드로 통일하여 중복 제거
   - 도메인 타입 도입을 장려하여 코드 표현력과 유지보수성 향상

6. **사용 지점에서의 중복 제거** (→ 상세 내용 6)
   - 테스트에서 반복되는 객체 생성 및 전달 패턴을 헬퍼 메서드로 추출
   - 빌더 자체를 헬퍼 메서드에 전달하여 변형에 유연하게 대응
   - 빌더가 지원 세부사항을 추가하고 시스템에 주입하는 구조로 확장성 확보

7. **선언적 테스트로의 전환** (→ 상세 내용 7)
   - 메서드 이름을 의도 중심으로 변경하여 절차적 스크립트를 선언적 설명으로 전환
   - 테스트가 구현 방법이 아닌 기대 동작을 표현하도록 리팩토링
   - 비기술 이해관계자와도 소통 가능한 수준의 가독성 달성

8. **커뮤니케이션 우선 원칙** (→ 상세 내용 8)
   - 테스트 데이터 빌더와 팩토리 메서드를 결합해 더 문학적이고 선언적인 테스트 작성
   - 코드는 읽히기 위한 것이라는 철학 반영
   - 개발 도구셋 내에서 협업 촉진 및 더 나은 테스트 작성 가능

### 개념 간 관계

```
객체 생성 문제 인식
    ↓
테스트 데이터 빌더 도입 (기본값 + 체이닝)
    ↓
유사 객체 생성 전략 (빌더 재사용 + 복제)
    ↓
빌더 결합 (중첩 빌더 간소화)
    ↓
팩토리 메서드 (도메인 언어 강화)
    ↓
사용 지점 중복 제거 (헬퍼 메서드 + 빌더 전달)
    ↓
선언적 테스트 (의도 중심 네이밍)
    ↓
커뮤니케이션 우선 (가독성 최우선)
```

## 상세 내용

### 목차
1. 테스트에서의 객체 생성 문제와 Object Mother 패턴의 한계
2. 테스트 데이터 빌더 패턴 소개 및 구현
3. 유사한 객체 생성 전략
4. 빌더 결합을 통한 코드 간소화
5. 팩토리 메서드로 도메인 모델 강조
6. 사용 지점에서의 중복 제거
7. 선언적 테스트로의 전환
8. 커뮤니케이션 우선 원칙

---

### 1. 테스트에서의 객체 생성 문제와 Object Mother 패턴의 한계

**참조**: 핵심 개념 1

**출처**: Section "Introduction" (Lines 8-46)

#### 문제 상황

생산 코드에서는 객체를 상대적으로 적은 곳에서 생성하고 필요한 값들이 사용자 입력, 데이터베이스 쿼리, 수신 메시지 등에서 제공되지만, 테스트에서는 매번 모든 생성자 인자를 제공해야 함.

**원본 코드 예시 (Java):**
```java
// Lines 15-24
// 고객 주문 테스트에서 복잡한 객체 생성
@Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
  Order order = new Order(
      new Customer("Sherlock Holmes",
          new Address("221b Baker Street",
                      "London",
                      new PostCode("NW1", "3RX"))));
  order.addLine(new OrderLine("Deerstalker Hat", 1));
  order.addLine(new OrderLine("Tweed Cape", 1));
  // [...] 테스트 로직 계속
}
```

**Python 버전:**
```python
# 테스트에서 복잡한 객체 생성
def test_charges_customer_for_total_cost_of_all_ordered_items():
    # 모든 생성자 인자를 명시적으로 제공해야 함
    order = Order(
        customer=Customer(
            name="Sherlock Holmes",
            address=Address(
                street="221b Baker Street",
                city="London",
                postcode=PostCode(area="NW1", code="3RX")
            )
        )
    )
    order.add_line(OrderLine(product="Deerstalker Hat", quantity=1))
    order.add_line(OrderLine(product="Tweed Cape", quantity=1))
    # [...] 실제 테스트 검증 로직
```

**문제점 (Lines 25-28):**
- 객체 생성 코드가 테스트를 읽기 어렵게 만듦
- 테스트 동작과 관련 없는 정보로 가득 참
- 생성자 인자나 객체 구조 변경 시 많은 테스트가 깨짐 (취약성)

#### Object Mother 패턴의 한계

**참조**: 핵심 개념 1

Object Mother는 테스트용 객체를 생성하는 팩토리 메서드를 가진 클래스 (Lines 28-35).

**원본 코드 예시 (Java):**
```java
// Lines 32
Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
```

**Python 버전:**
```python
# Object Mother 패턴 사용
order = ExampleOrders.new_deerstalker_and_cape_order()
```

**한계점 (Lines 39-45):**
- 테스트 데이터의 작은 변형마다 새로운 팩토리 메서드가 필요함
- 시간이 지나면서 중복 코드로 가득 차거나 무한히 세분화된 메서드로 복잡해짐

**원본 코드 예시 (Java):**
```java
// Lines 41-42
Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
```

**Python 버전:**
```python
# 변형마다 새로운 메서드 필요
order1 = ExampleOrders.new_deerstalker_and_cape_and_swordstick_order()
order2 = ExampleOrders.new_deerstalker_and_boots_order()
# 조합이 늘어날수록 메서드가 폭발적으로 증가
```

---

### 2. 테스트 데이터 빌더 패턴 소개 및 구현

**참조**: 핵심 개념 2

**이전 내용과의 관계**: Object Mother 패턴의 한계를 극복하기 위한 해결책으로 테스트 데이터 빌더 도입

**출처**: Section "Test Data Builders" (Lines 46-117)

#### 빌더 패턴의 기본 구조

복잡한 설정이 필요한 클래스에 대해 각 생성자 파라미터를 위한 필드를 가지며 안전한 값으로 초기화된 테스트 데이터 빌더를 만듦. 체이닝 가능한 public 메서드로 값을 오버라이드하고, 관례적으로 build() 메서드로 최종 객체를 생성함 (Lines 47-52).

**원본 코드 예시 (Java):**
```java
// Lines 55-80
// OrderBuilder 구현
public class OrderBuilder {
  // 각 필드를 안전한 기본값으로 초기화
  private Customer customer = new CustomerBuilder().build();
  private List<OrderLine> lines = new ArrayList<OrderLine>();
  private BigDecimal discountRate = BigDecimal.ZERO;

  // 정적 팩토리 메서드 (선택적 개선)
  public static OrderBuilder anOrder() {
    return new OrderBuilder();
  }

  // 체이닝 가능한 setter 메서드들
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

  // 최종 객체 생성 메서드
  public Order build() {
    Order order = new Order(customer);
    for (OrderLine line : lines) order.addLine(line);
    order.setDiscountRate(discountRate);
    return order;
  }
}
```

**Python 버전:**
```python
from decimal import Decimal
from typing import List

# OrderBuilder 구현
class OrderBuilder:
    def __init__(self):
        # 각 필드를 안전한 기본값으로 초기화
        self.customer = CustomerBuilder().build()
        self.lines: List[OrderLine] = []
        self.discount_rate = Decimal('0')

    # 정적 팩토리 메서드 (클래스 메서드로 구현)
    @classmethod
    def an_order(cls):
        return cls()

    # 체이닝 가능한 setter 메서드들
    def with_customer(self, customer: Customer):
        self.customer = customer
        return self  # 체이닝을 위해 자신을 반환

    def with_order_lines(self, lines: List[OrderLine]):
        self.lines = lines
        return self

    def with_discount(self, discount_rate: Decimal):
        self.discount_rate = discount_rate
        return self

    # 최종 객체 생성 메서드
    def build(self) -> Order:
        order = Order(self.customer)
        for line in self.lines:
            order.add_line(line)
        order.set_discount_rate(self.discount_rate)
        return order
```

#### 빌더 사용 예시

**기본 사용 (Lines 87-89):**

**원본 코드 (Java):**
```java
// 기본 Order 객체가 필요하고 내용이 중요하지 않은 경우
Order order = new OrderBuilder().build();
```

**Python 버전:**
```python
# 기본 Order 객체가 필요하고 내용이 중요하지 않은 경우
order = OrderBuilder().build()
```

**특정 값 지정 (Lines 90-100):**

**원본 코드 (Java):**
```java
// 우편번호가 없는 고객을 위한 Order 생성
new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode().build())
      .build())
  .build();
```

**Python 버전:**
```python
# 우편번호가 없는 고객을 위한 Order 생성
(OrderBuilder()
    .from_customer(
        CustomerBuilder()
            .with_address(AddressBuilder().with_no_postcode().build())
            .build())
    .build())
```

#### 빌더의 장점

**참조**: 핵심 개념 2

**출처**: Lines 101-117

1. **구문 노이즈 감소**: 객체 생성 시 대부분의 문법적 잡음을 감쌈
2. **단순한 기본 케이스**: 기본 경우는 단순하고 특수 경우도 크게 복잡하지 않음
3. **변경에 대한 보호**: 생성자에 인자 추가 시 관련 빌더와 해당 인자가 필요한 테스트만 수정
4. **가독성 향상**: 각 빌더 메서드가 파라미터 목적을 식별해 오류 발견이 쉬움

**가독성 비교 예시 (Lines 109-117):**

**원본 코드 (Java):**
```java
// 실수하기 쉬운 코드 - "London"이 두 번째 주소 라인인지 도시 이름인지 불명확
TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");

// 빌더로 실수가 명확해짐
new AddressBuilder()
  .withStreet("221b Baker Street")
  .withStreet2("London")  // 실수가 명확히 드러남
  .withPostCode("NW1 6XE")
  .build();
```

**Python 버전:**
```python
# 실수하기 쉬운 코드 - 위치 기반 인자로는 의미 파악이 어려움
TestAddresses.new_address("221b Baker Street", "London", "NW1 6XE")

# 빌더로 실수가 명확해짐
(AddressBuilder()
    .with_street("221b Baker Street")
    .with_street2("London")  # 실수가 명확히 드러남
    .with_post_code("NW1 6XE")
    .build())
```

---

### 3. 유사한 객체 생성 전략

**참조**: 핵심 개념 3

**이전 내용과의 관계**: 빌더 패턴의 기본 사용법에서 발전하여 여러 유사 객체를 효율적으로 생성하는 방법 제시

**출처**: Section "Creating Similar Objects" (Lines 118-169)

#### 문제 상황: 중복된 빌더 생성

**출처**: Lines 119-137

유사한 객체를 여러 개 만들 때 각각 새 빌더를 생성하면 중복이 발생하고 차이점을 찾기 어려움.

**원본 코드 (Java):**
```java
// Lines 128-137
// 할인율만 다른 두 주문 - 중복이 많고 차이점 발견이 어려움
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

**Python 버전:**
```python
# 할인율만 다른 두 주문 - 중복이 많고 차이점 발견이 어려움
order_with_small_discount = (OrderBuilder()
    .with_line("Deerstalker Hat", 1)
    .with_line("Tweed Cape", 1)
    .with_discount(0.10)
    .build())

order_with_large_discount = (OrderBuilder()
    .with_line("Deerstalker Hat", 1)
    .with_line("Tweed Cape", 1)
    .with_discount(0.25)
    .build())
```

#### 해결책: 공통 빌더 재사용

**출처**: Lines 138-146

공통 상태로 단일 빌더를 초기화하고 각 객체마다 차이나는 값만 설정 후 build() 호출.

**원본 코드 (Java):**
```java
// Lines 140-144
// 공통 부분을 빌더에 저장하고 차이점만 변경
OrderBuilder hatAndCape = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1);

Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
```

**Python 버전:**
```python
# 공통 부분을 빌더에 저장하고 차이점만 변경
hat_and_cape = (OrderBuilder()
    .with_line("Deerstalker Hat", 1)
    .with_line("Tweed Cape", 1))

order_with_small_discount = hat_and_cape.with_discount(0.10).build()
order_with_large_discount = hat_and_cape.with_discount(0.25).build()
```

#### 주의사항: 의도치 않은 상태 공유

**출처**: Lines 147-153

객체가 다른 필드로 변형될 때 이전 변경 사항이 누적되어 의도치 않은 상태를 만들 수 있음.

**원본 코드 (Java):**
```java
// Lines 151-152
// orderWithGiftVoucher가 10% 할인도 포함하게 됨 (의도치 않음)
Order orderWithDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build();
```

**Python 버전:**
```python
# orderWithGiftVoucher가 10% 할인도 포함하게 됨 (의도치 않음)
order_with_discount = hat_and_cape.with_discount(0.10).build()
order_with_gift_voucher = hat_and_cape.with_gift_voucher("abc").build()
```

#### 해결책: 복사 생성자 또는 복제 메서드

**출처**: Lines 153-166

**방법 1: 복사 생성자 (Lines 154-160)**

**원본 코드 (Java):**
```java
// 복사 생성자를 사용해 빌더 상태 복제
Order orderWithDiscount = new OrderBuilder(hatAndCape)
  .withDiscount(0.10)
  .build();

Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
  .withGiftVoucher("abc")
  .build();
```

**Python 버전:**
```python
# 복사 생성자를 사용해 빌더 상태 복제
order_with_discount = (OrderBuilder(hat_and_cape)
    .with_discount(0.10)
    .build())

order_with_gift_voucher = (OrderBuilder(hat_and_cape)
    .with_gift_voucher("abc")
    .build())

# OrderBuilder에 복사 생성자 추가
class OrderBuilder:
    def __init__(self, other=None):
        if other:
            # 다른 빌더로부터 상태 복사
            self.customer = other.customer
            self.lines = other.lines.copy()
            self.discount_rate = other.discount_rate
        else:
            # 기본 초기화
            self.customer = CustomerBuilder().build()
            self.lines = []
            self.discount_rate = Decimal('0')
```

**방법 2: but() 메서드 (Lines 161-164)**

**원본 코드 (Java):**
```java
// but() 메서드로 현재 상태의 복사본 반환
Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build();
```

**Python 버전:**
```python
# but() 메서드로 현재 상태의 복사본 반환
order_with_discount = hat_and_cape.but_().with_discount(0.10).build()
order_with_gift_voucher = hat_and_cape.but_().with_gift_voucher("abc").build()

# OrderBuilder에 but_() 메서드 추가
class OrderBuilder:
    def but_(self):
        """현재 빌더의 복사본을 반환"""
        new_builder = OrderBuilder()
        new_builder.customer = self.customer
        new_builder.lines = self.lines.copy()
        new_builder.discount_rate = self.discount_rate
        return new_builder
```

**방법 3: 함수형 접근 (Lines 165-166)**

복잡한 설정에서는 각 "with" 메서드가 자신 대신 새 빌더 복사본을 반환하도록 함.

**Python 버전:**
```python
# 함수형 접근 - 각 메서드가 새 복사본 반환
class OrderBuilder:
    def with_discount(self, discount_rate: Decimal):
        # 자신을 수정하지 않고 새 복사본 생성
        new_builder = self.but_()
        new_builder.discount_rate = discount_rate
        return new_builder

    def with_gift_voucher(self, code: str):
        new_builder = self.but_()
        new_builder.gift_voucher_code = code
        return new_builder
```

---

### 4. 빌더 결합을 통한 코드 간소화

**참조**: 핵심 개념 4

**이전 내용과의 관계**: 빌더 재사용 전략에서 더 나아가 중첩된 빌더 구조를 간소화하는 방법 제시

**출처**: Section "Combining Builders" (Lines 172-190)

#### 문제 상황: 빌더 인프라 코드가 지배적

**출처**: Lines 173-184

중첩된 객체 구조를 만들 때 build() 메서드 호출이 많아져 코드가 복잡해짐.

**원본 코드 (Java):**
```java
// Lines 179-184
// 우편번호가 없는 주문 생성 - 빌더 인프라가 지배적
Order orderWithNoPostcode = new OrderBuilder()
  .fromCustomer(
    new CustomerBuilder()
        .withAddress(new AddressBuilder().withNoPostcode().build())
        .build())
    .build();
```

**Python 버전:**
```python
# 우편번호가 없는 주문 생성 - 빌더 인프라가 지배적
order_with_no_postcode = (OrderBuilder()
    .from_customer(
        CustomerBuilder()
            .with_address(AddressBuilder().with_no_postcode().build())
            .build())
    .build())
```

#### 해결책: 빌더를 인자로 전달

**출처**: Lines 173-190

빌더가 생성된 객체 대신 다른 빌더를 인자로 받도록 하여 build() 호출을 제거.

**원본 코드 (Java):**
```java
// Lines 186-190
// 빌더를 직접 전달하여 build() 호출 제거
Order order = new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode()))
  .build();
```

**Python 버전:**
```python
# 빌더를 직접 전달하여 build() 호출 제거
order = (OrderBuilder()
    .from_customer(
        CustomerBuilder()
            .with_address(AddressBuilder().with_no_postcode()))
    .build())

# OrderBuilder의 from_customer 메서드 구현
class OrderBuilder:
    def from_customer(self, customer):
        # customer가 빌더인지 객체인지 확인
        if isinstance(customer, CustomerBuilder):
            self.customer = customer.build()
        else:
            self.customer = customer
        return self

# CustomerBuilder의 with_address 메서드 구현
class CustomerBuilder:
    def with_address(self, address):
        # address가 빌더인지 객체인지 확인
        if isinstance(address, AddressBuilder):
            self.address = address.build()
        else:
            self.address = address
        return self
```

**효과 (Lines 175-177):**
- 무엇을 생성하는가(중요한 정보)에 집중
- 생성 메커니즘(build() 호출)을 제거하여 가독성 향상

---

### 5. 팩토리 메서드로 도메인 모델 강조

**참조**: 핵심 개념 5

**이전 내용과의 관계**: 빌더 결합에서 더 나아가 팩토리 메서드로 코드를 더욱 압축하고 도메인 언어를 강화

**출처**: Section "Emphasizing the Domain Model with Factory Methods" (Lines 191-218)

#### 팩토리 메서드로 노이즈 제거

**출처**: Lines 192-203

빌더 생성을 팩토리 메서드로 감싸 테스트 코드의 노이즈를 더 줄임.

**원본 코드 (Java):**
```java
// Lines 194-196
// 팩토리 메서드 사용 전
Order order =
anOrder().fromCustomer(
aCustomer().withAddress(anAddress().withNoPostcode())).build();
```

**Python 버전:**
```python
# 팩토리 메서드를 사용한 간결한 표현
order = (an_order()
    .from_customer(
        a_customer()
            .with_address(an_address().with_no_postcode()))
    .build())

# 팩토리 메서드 구현
def an_order():
    return OrderBuilder()

def a_customer():
    return CustomerBuilder()

def an_address():
    return AddressBuilder()
```

#### 메서드 오버로딩 활용

**출처**: Lines 197-203

Java의 메서드 오버로딩을 활용해 타입별로 단일 with() 메서드로 통일.

**원본 코드 (Java):**
```java
// Lines 202-203
// 메서드 오버로딩으로 with() 메서드 통일
Order order =
  anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
```

**Python 버전:**
```python
# Python은 메서드 오버로딩을 지원하지 않으므로 타입 체크로 구현
from typing import Union

class OrderBuilder:
    def from_(self, customer: Union['CustomerBuilder', 'Customer']):
        if isinstance(customer, CustomerBuilder):
            self.customer = customer.build()
        else:
            self.customer = customer
        return self

class CustomerBuilder:
    def with_(self, arg: Union['AddressBuilder', 'Address', 'Postcode']):
        # 타입에 따라 적절한 필드 설정
        if isinstance(arg, AddressBuilder):
            self.address = arg.build()
        elif isinstance(arg, Address):
            self.address = arg
        elif isinstance(arg, Postcode):
            self.postcode = arg
        return self

# 사용 예시
order = (an_order()
    .from_(a_customer()
        .with_(an_address().with_no_postcode()))
    .build())
```

#### 명시적 이름이 필요한 경우

**출처**: Lines 204-211

같은 타입의 여러 인자가 있을 때는 명시적 이름 필요 (예: String 타입).

**원본 코드 (Java):**
```java
// Lines 207-211
// Postcode는 오버로딩 가능, String은 명시적 이름 필요
Address aLongerAddress = anAddress()
    .withStreet("221b Baker Street")
    .withCity("London")
    .with(postCode("NW1", "3RX"))
    .build();
```

**Python 버전:**
```python
# 타입이 같으면 명시적 메서드 이름 필요
a_longer_address = (an_address()
    .with_street("221b Baker Street")
    .with_city("London")
    .with_(post_code("NW1", "3RX"))
    .build())

def post_code(area: str, code: str) -> Postcode:
    return Postcode(area, code)
```

#### 도메인 타입 도입 장려

**출처**: Lines 216-218

이 접근법은 도메인 타입 도입을 장려하며, 이는 더 표현력 있고 유지보수하기 쉬운 코드로 이어짐 (Chapter 21 "Domain Types Are Better Than Strings" 참조).

---

### 6. 사용 지점에서의 중복 제거

**참조**: 핵심 개념 6

**이전 내용과의 관계**: 테스트 데이터 빌더를 컨텍스트에서 최대한 활용하기 위한 테스트 구조화 방법

**출처**: Section "Removing Duplication at the Point of Use" (Lines 219-305)

#### 초기 중복 제거 시도

**출처**: Section "First, Remove Duplication" (Lines 226-271)

비동기 주문 처리 시스템 테스트에서 주문 생성, 전송, 추적 패턴이 반복됨.

**원본 코드 (Java):**
```java
// Lines 230-247
// 반복적인 주문 생성 및 처리 패턴
@Test public void reportsTotalSalesOfOrderedProducts() {
  Order order1 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1)
    .withCustomersReference(1234)
    .build();
  requestSender.send(order1);
  progressMonitor.waitForCompletion(order1);

  Order order2 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withCustomersReference(5678)
    .build();
  requestSender.send(order2);
  progressMonitor.waitForCompletion(order2);

  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
```

**Python 버전:**
```python
# 반복적인 주문 생성 및 처리 패턴
def test_reports_total_sales_of_ordered_products():
    order1 = (an_order()
        .with_line("Deerstalker Hat", 1)
        .with_line("Tweed Cape", 1)
        .with_customers_reference(1234)
        .build())
    request_sender.send(order1)
    progress_monitor.wait_for_completion(order1)

    order2 = (an_order()
        .with_line("Deerstalker Hat", 1)
        .with_customers_reference(5678)
        .build())
    request_sender.send(order2)
    progress_monitor.wait_for_completion(order2)

    report = gui.open_sales_report()
    assert report.displayed_total_sales_for("Deerstalker Hat") == 2
    assert report.displayed_total_sales_for("Tweed Cape") == 1
```

**문제 있는 첫 번째 시도 (Lines 249-271):**

헬퍼 메서드로 추출했지만 변형에 대응하기 어려움.

**원본 코드 (Java):**
```java
// Lines 250-256
// 첫 번째 시도 - 단순 헬퍼 메서드
@Test public void reportsTotalSalesOfOrderedProducts() {
  submitOrderFor("Deerstalker Hat", "Tweed Cape");
  submitOrderFor("Deerstalker Hat");

  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}

// Lines 262-271
// 헬퍼 메서드 구현
void submitOrderFor(String ... products) {
  OrderBuilder orderBuilder = anOrder()
    .withCustomersReference(nextCustomerReference());
  for (String product : products) {
    orderBuilder = orderBuilder.withLine(product, 1);
  }
  Order order = orderBuilder.build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
```

**Python 버전:**
```python
# 첫 번째 시도 - 단순 헬퍼 메서드
def test_reports_total_sales_of_ordered_products():
    submit_order_for("Deerstalker Hat", "Tweed Cape")
    submit_order_for("Deerstalker Hat")

    report = gui.open_sales_report()
    assert report.displayed_total_sales_for("Deerstalker Hat") == 2
    assert report.displayed_total_sales_for("Tweed Cape") == 1

# 헬퍼 메서드 구현
def submit_order_for(*products):
    order_builder = an_order().with_customers_reference(next_customer_reference())
    for product in products:
        order_builder = order_builder.with_line(product, 1)
    order = order_builder.build()
    request_sender.send(order)
    progress_monitor.wait_for_completion(order)
```

**확장성 문제 (Lines 272-280):**

변형이 많아지면 Object Mother 패턴과 같은 문제 발생.

**원본 코드 (Java):**
```java
// Lines 276-280
// 변형마다 새로운 메서드 필요 - 확장성 없음
void submitOrderFor(String ... products) { […]
void submitOrderFor(String product, int count,
                    String otherProduct, int otherCount) { […]
void submitOrderFor(String product, double discount) { […]
void submitOrderFor(String product, String giftVoucherCode) { […]
```

**Python 버전:**
```python
# 변형마다 새로운 메서드 필요 - 확장성 없음
def submit_order_for(*products): ...
def submit_order_for_with_counts(product, count, other_product, other_count): ...
def submit_order_for_with_discount(product, discount): ...
def submit_order_for_with_gift_voucher(product, gift_voucher_code): ...
```

#### 개선된 해결책: 빌더를 전달

**출처**: Lines 281-302

빌더 자체를 헬퍼 메서드에 전달하여 변형에 유연하게 대응.

**원본 코드 (Java):**
```java
// Lines 286-295
// 빌더를 전달하는 개선된 접근법
@Test public void reportsTotalSalesOfOrderedProducts() {
  sendAndProcess(anOrder()
      .withLine("Deerstalker Hat", 1)
      .withLine("Tweed Cape", 1));
  sendAndProcess(anOrder()
      .withLine("Deerstalker Hat", 1));

  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}

// Lines 296-302
// 빌더를 받는 헬퍼 메서드
void sendAndProcess(OrderBuilder orderDetails) {
  Order order = orderDetails
    .withDefaultCustomersReference(nextCustomerReference())
    .build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
```

**Python 버전:**
```python
# 빌더를 전달하는 개선된 접근법
def test_reports_total_sales_of_ordered_products():
    send_and_process(an_order()
        .with_line("Deerstalker Hat", 1)
        .with_line("Tweed Cape", 1))
    send_and_process(an_order()
        .with_line("Deerstalker Hat", 1))

    report = gui.open_sales_report()
    assert report.displayed_total_sales_for("Deerstalker Hat") == 2
    assert report.displayed_total_sales_for("Tweed Cape") == 1

# 빌더를 받는 헬퍼 메서드
def send_and_process(order_details: OrderBuilder):
    order = (order_details
        .with_default_customers_reference(next_customer_reference())
        .build())
    request_sender.send(order)
    progress_monitor.wait_for_completion(order)
```

**장점 (Lines 281-285):**
- 변형과 공통 요소를 분리
- 헬퍼 메서드가 지원 세부사항(고객 참조 번호)을 추가
- 확장성 있고 집중된 테스트 코드

---

### 7. 선언적 테스트로의 전환

**참조**: 핵심 개념 7

**이전 내용과의 관계**: 중복 제거에서 더 나아가 테스트 코드의 가독성과 의도 전달을 극대화

**출처**: Section "Then, Raise the Game" (Lines 307-331)

#### 의도 중심의 네이밍

**출처**: Lines 308-320

구현 방법이 아닌 기대 동작에 초점을 맞춰 이름을 변경.

**원본 코드 (Java):**
```java
// Lines 311-320
// 선언적 스타일로 전환
@Test public void reportsTotalSalesOfOrderedProducts() {
  havingReceived(anOrder()
        .withLine("Deerstalker Hat", 1)
        .withLine("Tweed Cape", 1));
  havingReceived(anOrder()
        .withLine("Deerstalker Hat", 1));

  TotalSalesReport report = gui.openSalesReport();
  report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
}
```

**Python 버전:**
```python
# 선언적 스타일로 전환
def test_reports_total_sales_of_ordered_products():
    # "수신했음"이라는 의미로 변경
    having_received(an_order()
        .with_line("Deerstalker Hat", 1)
        .with_line("Tweed Cape", 1))
    having_received(an_order()
        .with_line("Deerstalker Hat", 1))

    report = gui.open_sales_report()
    # "표시한다"는 의미로 변경
    report.displays_total_sales_for("Deerstalker Hat", equal_to(2))
    report.displays_total_sales_for("Tweed Cape", equal_to(1))

def having_received(order_details: OrderBuilder):
    """시스템이 주문을 수신했다는 선언적 표현"""
    order = (order_details
        .with_default_customers_reference(next_customer_reference())
        .build())
    request_sender.send(order)
    progress_monitor.wait_for_completion(order)
```

#### 복잡한 시나리오 표현

**출처**: Lines 321-331

주문 수정과 같은 복잡한 시나리오도 선언적으로 표현 가능.

**원본 코드 (Java):**
```java
// Lines 321-331
// 주문 수정을 고려한 총 판매량 계산 테스트
@Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
  Customer theCustomer = aCustomer().build();
  havingReceived(anOrder().from(theCustomer)
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
  havingReceived(anOrderAmendment().from(theCustomer)
    .withLine("Deerstalker Hat", 2));

  TotalSalesReport report = user.openSalesReport();
  report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.containsTotalSalesFor("Tweed Cape", equalTo(1));
}
```

**Python 버전:**
```python
# 주문 수정을 고려한 총 판매량 계산 테스트
def test_takes_amendments_into_account_when_calculating_total_sales():
    the_customer = a_customer().build()

    # 최초 주문 수신
    having_received(an_order()
        .from_(the_customer)
        .with_line("Deerstalker Hat", 1)
        .with_line("Tweed Cape", 1))

    # 주문 수정 수신
    having_received(an_order_amendment()
        .from_(the_customer)
        .with_line("Deerstalker Hat", 2))

    report = user.open_sales_report()
    report.contains_total_sales_for("Deerstalker Hat", equal_to(2))
    report.contains_total_sales_for("Tweed Cape", equal_to(1))

def an_order_amendment():
    return OrderAmendmentBuilder()
```

#### 변환의 의미

**출처**: Lines 332-336

절차적 테스트에서 시작해 빌더 객체로 동작을 추출하고 선언적 기능 설명으로 완성. 기능을 논의할 때 사용할 수 있는 언어로 테스트 코드를 발전시키며, 나머지는 지원 코드로 이동.

---

### 8. 커뮤니케이션 우선 원칙

**참조**: 핵심 개념 8

**이전 내용과의 관계**: 전체 챕터의 기법들이 궁극적으로 지향하는 목표와 철학 정리

**출처**: Section "Communication First" (Lines 337-360)

#### 코드의 가독성 중심 철학

**출처**: Lines 337-343

테스트 데이터 빌더를 사용해 중복을 줄이고 테스트 코드를 더 표현력 있게 만듦. 코드 언어에 대한 집착을 반영하며, 코드는 읽히기 위한 것이라는 원칙에 기반함. 팩토리 메서드 및 테스트 스캐폴딩과 결합하여 단계의 연속이 아닌 기능의 의도를 설명하는 더 문학적이고 선언적인 테스트 작성 가능.

#### 비기술 이해관계자와의 협업

**출처**: Lines 344-352

이러한 기법을 사용하면 상위 레벨 테스트로 비즈니스 분석가 같은 비기술 이해관계자와 직접 소통 가능. 난해한 구두점을 무시할 의향이 있다면, 테스트를 사용해 기능이 무엇을 해야 하는지, 왜 그래야 하는지 정확히 좁혀갈 수 있음.

**다른 도구와의 비교 (Lines 353-357):**

FIT 같은 도구들은 기술/비기술 팀원 간 협업을 촉진하도록 설계됨. 하지만 LiFT 팀의 사례처럼 개발 도구셋 내에서 많은 것을 달성할 수 있으며, 더 나은 테스트를 작성할 수 있음.

#### 핵심 메시지

테스트 데이터 빌더와 관련 기법들은 단순히 코드 중복을 줄이는 것을 넘어, **커뮤니케이션 도구**로서 테스트 코드의 역할을 강화함. 이는 개발자 간, 그리고 개발자와 비기술 이해관계자 간의 협업을 개선하고, 궁극적으로 더 나은 소프트웨어 품질로 이어짐.

---

## 참고 문헌 및 추가 자료

**출처**: Lines 28-29, 354-355

- **[Schuh01]**: Object Mother 패턴
- **[Gamma94]**: Factory Methods (Design Patterns)
- **[Mugridge05]**: FIT (Framework for Integrated Test)
- **[LIFT]**: LiFT 팀의 협업 사례
- **Chapter 21 참조**: "Domain Types Are Better Than Strings" (page 213)

---

## 챕터의 핵심 인사이트

1. **진화적 접근**: Object Mother → Test Data Builder → Factory Methods → Declarative Tests
2. **레이어별 개선**: 구문 노이즈 제거 → 중복 제거 → 의도 표현 강화 → 협업 도구화
3. **실용주의**: 완벽한 추상화보다 팀 내 효과적인 커뮤니케이션이 우선
4. **도메인 중심**: 기술 세부사항을 숨기고 비즈니스 도메인 언어를 드러냄
5. **지속가능성**: 변경에 강하고 유지보수가 쉬운 테스트 코드 작성

