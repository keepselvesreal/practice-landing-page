# Growing_object_oriented_software_guided_by_tests_Chapter_23_Test_Diagnostics

## 압축 내용

테스트 실패 시 원인을 빠르게 진단할 수 있도록 명확하고 정보가 풍부한 실패 메시지를 설계하여, 디버거 없이도 문제를 즉시 파악하고 수정할 수 있는 자기 진단적(self-diagnostic) 테스트를 작성하는 방법

## 핵심 내용

### 1. 실패를 위한 설계 (Design to Fail) [→ 상세내용 1]
- **테스트의 진정한 목적**: 통과가 아니라 오류를 감지하고 보고하는 것
- **진단 불가능한 테스트의 위험**: 디버거를 열어야 하는 상황은 테스트가 요구사항을 명확히 표현하지 못했다는 신호
- **"debug hell" 방지**: 진단 불가능한 상황에서 테스트를 삭제하고 안전망을 잃는 최악의 시나리오 회피

### 2. 작고 집중된 테스트 (Small, Focused, Well-Named Tests) [→ 상세내용 2]
- **테스트 크기와 진단성의 관계**: 테스트가 작을수록 이름만으로도 무엇이 잘못되었는지 파악 가능
- **가독성 있는 이름**: Chapter 21의 원칙과 연결되어 정적 가독성과 런타임 진단성 모두 향상

### 3. 설명적 단언 메시지 (Explanatory Assertion Messages) [→ 상세내용 3]
- **JUnit의 메시지 파라미터 활용**: 단언 실패 시 표시될 메시지를 첫 번째 파라미터로 제공
- **증상 vs 원인**: 메시지가 단순 값의 차이(증상)가 아닌 검증하는 속성의 의미(원인)를 설명해야 함
- **실전 예시**: `assertEquals("outstanding balance", 16301, customer.getOutstandingBalance())`

### 4. Matcher를 통한 세부사항 강조 (Highlight Detail with Matchers) [→ 상세내용 4]
- **Hamcrest Matcher의 진단 능력**: `assertThat()`과 함께 사용 시 불일치한 값에 대한 상세한 설명 제공
- **구조화된 실패 보고**: 어떤 값들이 관련되어 있고 정확히 무엇이 다른지 명확히 표시

### 5. 자기 설명적 값 (Self-Describing Value) [→ 상세내용 5]
- **값 자체에 의미 포함**: 단언에 설명을 추가하는 대신, 값 자체가 역할을 설명하도록 설계
- **참조 타입 활용**: `toString()` 메서드를 오버라이드하여 값의 의미를 표현
- **도메인 타입의 중요성**: Chapter 20에서 다룬 "Domain Types Are Better Than Strings"와 연결

**핵심 개념 간의 관계**:
- 개념 1(실패를 위한 설계)은 전체 장의 철학적 기반을 제공
- 개념 2-6은 이 철학을 실현하기 위한 구체적 기법들
- 개념 2(작은 테스트)는 가장 기본적인 접근
- 개념 3-4(메시지와 Matcher)는 단언 수준의 개선
- 개념 5-7(자기 설명적 값)은 테스트 데이터 수준의 개선
- 개념 8(명시적 기대치 확인)은 Mock 프레임워크 사용 시의 특수 상황
- 개념 9(진단은 일급 기능)는 전체 프로세스에 진단을 통합하는 메타 수준의 원칙

### 6. 명백하게 인위적인 값 (Obviously Canned Value) [→ 상세내용 6]
- **자기 설명이 어려운 기본 타입 처리**: char, int 등에서 명백히 비정상적인 값 사용
- **팀 규칙**: 공통 값에 대한 규칙을 수립하여 일관성 유지 (예: `INVALID_ID`가 3자리인데 실제 ID는 5자리 이상)

### 7. 추적 객체 (Tracer Object) [→ 상세내용 7]
- **객체 전달 경로 추적**: 코드가 객체를 올바른 협력자에게 전달하는지 확인
- **최소 기능 더미 객체**: 실패 시 자신의 역할을 설명하는 기능만 가진 객체
- **설계 도구로서의 활용**: TDD 초기에 빈 인터페이스로 도메인 개념을 표시하고 협력 관계 정의

### 8. 명시적 기대치 충족 단언 (Explicitly Assert That Expectations Were Satisfied) [→ 상세내용 8]
- **혼란스러운 실패 보고 문제**: 기대치와 단언을 모두 가진 테스트에서 잘못된 실패 메시지 표시
- **순서 제어**: `context.assertIsSatisfied()`를 단언 전에 명시적으로 호출
- **"Watch the Test Fail"과의 연결**: 테스트가 예상과 다른 이유로 실패하면 명시적 호출 추가 필요

### 9. 진단은 일급 기능 (Diagnostics Are a First-Class Feature) [→ 상세내용 9]
- **4단계 TDD 사이클**: fail → **report** → pass → refactor (Chapter 5에서 소개)
- **테스트 품질 유지**: 프로덕션 코드뿐 아니라 테스트 코드의 품질도 유지해야 함
- **장기적 이해**: 한 달 후 코드를 변경할 사람도 이해할 수 있도록 진단 품질 확보

## 상세 내용

### 목차
1. 실패를 위한 설계 (Design to Fail)
2. 작고 집중된 테스트 (Small, Focused, Well-Named Tests)
3. 설명적 단언 메시지 (Explanatory Assertion Messages)
4. Matcher를 통한 세부사항 강조 (Highlight Detail with Matchers)
5. 자기 설명적 값 (Self-Describing Value)
6. 명백하게 인위적인 값 (Obviously Canned Value)
7. 추적 객체 (Tracer Object)
8. 명시적 기대치 충족 단언 (Explicitly Assert That Expectations Were Satisfied)
9. 진단은 일급 기능 (Diagnostics Are a First-Class Feature)

---

### 1. 실패를 위한 설계 (Design to Fail) [→ 핵심개념 1]

**위치**: 292페이지, 7-20행

**이전 맥락**: 이 장은 Chapter 21(테스트의 정적 가독성)에서 이어지며, 런타임에서 테스트가 제공해야 하는 정보에 초점을 맞춤

#### 테스트의 진정한 목적

테스트의 목적은 **통과하는 것이 아니라 실패하는 것**입니다. 우리는 프로덕션 코드가 테스트를 통과하길 원하지만, 동시에 존재하는 모든 오류를 테스트가 감지하고 보고하길 원합니다. "실패하는" 테스트는 실제로는 설계된 목적을 성공적으로 수행한 것입니다.

```python
# 실패의 가치를 보여주는 예시
def test_unexpected_relationship_detection():
    """
    작업 중이던 영역과 무관한 곳에서의 예상치 못한 테스트 실패도 가치가 있습니다.
    이는 우리가 눈치채지 못했던 코드 내의 암시적 관계를 드러냅니다.
    """
    # 예: A 모듈을 수정했는데 B 모듈의 테스트가 실패
    # → A와 B 사이에 숨겨진 의존성이 존재함을 발견
    pass
```

#### 진단 불가능한 실패의 위험

**위치**: 292페이지, 14-20행

피해야 할 상황은 **발생한 테스트 실패를 진단할 수 없는 경우**입니다. 디버거를 열고 테스트된 코드를 단계별로 실행하며 불일치 지점을 찾아야 하는 것은 최악입니다.

```python
# 나쁜 예: 진단 불가능한 테스트
def test_customer_data_bad():
    customer = order.get_customer()
    assert customer.account_id == "573242"
    assert customer.outstanding_balance == 16301
    # 실패 시: AssertionError만 발생, 어떤 값이 문제인지 불명확
    # → 디버거를 열어야 함 ("debug hell")
```

이는 최소한 우리의 테스트가 요구사항을 아직 충분히 명확하게 표현하지 못했음을 시사합니다. 최악의 경우, 우리는 마감 기한은 있지만 수정에 얼마나 걸릴지 모르는 "debug hell"에 빠질 수 있습니다. 이 시점에서 테스트를 그냥 삭제하고 싶은 유혹이 클 것이고, 그러면 안전망을 잃게 됩니다.

#### Stay Close to Home (집 가까이에 머물기)

**위치**: 292페이지, 21-27행

소스 코드 저장소와 자주 동기화하세요—몇 분마다라도. 그래야 테스트가 예상치 못하게 실패해도 최근 변경사항을 되돌리고 다른 접근을 시도하는 데 큰 비용이 들지 않습니다.

```bash
# 자주 커밋하는 습관
git commit -m "Add validation for account ID"  # 작은 변경사항
# 테스트 실패 발생
git revert HEAD  # 쉽게 되돌리기
# 다른 접근 시도
```

이 조언의 다른 의미는 코드를 버리고 다시 시작하는 것을 너무 주저하지 말라는 것입니다. 때로는 계속 파고드는 것보다 롤백하고 깨끗한 정신으로 다시 시작하는 것이 더 빠릅니다.

---

### 2. 작고 집중된 테스트 (Small, Focused, Well-Named Tests) [→ 핵심개념 2]

**위치**: 293페이지, 37-40행

**이전 토픽과의 관계**: 진단 가능한 테스트를 만들기 위한 가장 기본적이고 쉬운 첫 번째 방법

진단성을 개선하는 가장 쉬운 방법은 **각 테스트를 작고 집중적으로 유지하고 가독성 있는 이름을 부여**하는 것입니다(Chapter 21에서 설명).

```python
# 좋은 예: 작고 집중된 테스트
def test_customer_account_id_matches_order():
    """고객 계정 ID가 주문의 것과 일치해야 함"""
    customer = order.get_customer()
    assert customer.account_id == "573242"

def test_customer_outstanding_balance_calculated_correctly():
    """고객 미결제 잔액이 올바르게 계산되어야 함"""
    customer = order.get_customer()
    assert customer.outstanding_balance == 16301

# 나쁜 예: 크고 여러 것을 검증하는 테스트
def test_customer_data():
    """고객 데이터 테스트"""  # 이름이 모호함
    customer = order.get_customer()
    assert customer.account_id == "573242"
    assert customer.outstanding_balance == 16301
    assert customer.email == "test@example.com"
    assert customer.is_active == True
    # 실패 시 어떤 검증이 실패했는지 이름만으로는 알 수 없음
```

테스트가 작으면 이름이 무엇이 잘못되었는지에 대해 대부분을 알려줄 것입니다.

---

### 3. 설명적 단언 메시지 (Explanatory Assertion Messages) [→ 핵심개념 3]

**위치**: 293페이지, 41-57행

**이전 토픽과의 관계**: 작은 테스트만으로 충분하지 않을 때, 단언 수준에서 정보를 추가하는 방법

#### JUnit의 메시지 파라미터

JUnit의 단언 메서드들은 모두 **첫 번째 파라미터로 실패 시 표시할 메시지**를 받는 버전이 있습니다. 우리가 본 바로는 이 기능이 단언 실패를 더 유용하게 만드는 데 충분히 활용되지 않고 있습니다.

#### 문제 사례: 메시지 없는 단언

```java
// 원본 Java 코드
Customer customer = order.getCustomer();
assertEquals("573242", customer.getAccountId());
assertEquals(16301, customer.getOutstandingBalance());
```

```python
# Python 버전
customer = order.get_customer()
assert customer.account_id == "573242"
assert customer.outstanding_balance == 16301
```

이 테스트가 실패하면 보고서는 어떤 단언이 실패했는지 명확하지 않습니다:

```
ComparisonFailure: expected:<[16301]> but was:<[16103]>
```

메시지는 **증상**(잔액이 16103임)을 설명할 뿐 **원인**(미결제 잔액 계산이 잘못됨)을 설명하지 않습니다.

#### 해결책: 설명적 메시지 추가

```java
// 원본 Java 코드
assertEquals("account id", "573242", customer.getAccountId());
assertEquals("outstanding balance", 16301, customer.getOutstandingBalance());
```

```python
# Python 버전 (pytest 사용)
customer = order.get_customer()
assert customer.account_id == "573242", "account id"
assert customer.outstanding_balance == 16301, "outstanding balance"

# 또는 더 명확한 메시지
assert customer.outstanding_balance == 16301, \
    f"outstanding balance: expected 16301 but was {customer.outstanding_balance}"
```

이제 즉시 요점을 알 수 있습니다:

```
ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
```

---

### 4. Matcher를 통한 세부사항 강조 (Highlight Detail with Matchers) [→ 핵심개념 4]

**위치**: 293페이지, 58-69행

**이전 토픽과의 관계**: 단순한 메시지 추가를 넘어서, 구조화된 방식으로 진단 정보를 제공하는 방법

개발자는 **Hamcrest matcher와 함께 `assertThat()`을 사용**하여 또 다른 수준의 진단 세부사항을 제공할 수 있습니다.

#### Matcher API의 진단 기능

Matcher API는 불일치한 값을 설명하는 지원을 포함하여, 정확히 무엇이 다른지 이해하는 데 도움을 줍니다.

```java
// 원본 Java 코드 (252페이지의 instrument strike price 단언)
// 실패 보고서:
// Expected: a collection containing instrument at price a value greater than <81>
//      but: price was <50>, price was <72>, price was <31>
```

```python
# Python 버전 (PyHamcrest 사용)
from hamcrest import assert_that, has_item, greater_than

# 테스트 코드
instruments = get_instruments_from_market()
assert_that(
    instruments,
    has_item(instrument_with_price(greater_than(81)))
)

# 실패 시 출력:
# Expected: a collection containing instrument at price a value greater than <81>
#      but: price was <50>, price was <72>, price was <31>
```

이는 **어떤 값들이 관련되어 있는지** 정확히 보여줍니다. 단순히 "일치하지 않음"이 아니라, 어떤 가격들이 확인되었고 왜 조건을 만족하지 못했는지 명확합니다.

```python
# 더 복잡한 예시: 커스텀 matcher
from hamcrest.core.base_matcher import BaseMatcher

class HasValidEmail(BaseMatcher):
    """이메일 유효성을 검증하는 커스텀 matcher"""

    def _matches(self, customer):
        return '@' in customer.email and '.' in customer.email

    def describe_to(self, description):
        description.append_text('customer with valid email format')

    def describe_mismatch(self, customer, mismatch_description):
        mismatch_description.append_text(f'email was "{customer.email}"')

# 사용
assert_that(customer, HasValidEmail())

# 실패 시:
# Expected: customer with valid email format
#      but: email was "invalid-email"
```

---

### 5. 자기 설명적 값 (Self-Describing Value) [→ 핵심개념 5]

**위치**: 294페이지, 72-108행

**이전 토픽과의 관계**: 단언에 설명을 추가하는 대신, 값 자체를 개선하는 더 근본적인 접근

단언에 세부사항을 추가하는 대신 **단언의 값에 세부사항을 내장**할 수 있습니다.

#### 철학: 주석은 코드 개선의 힌트

코드에 주석이 필요하다는 것은 코드 자체를 개선해야 한다는 힌트라는 개념과 같은 정신으로 볼 수 있습니다. 단언에 세부사항을 추가해야 한다면, 그것은 실패를 더 명확하게 만들 수 있다는 힌트일 수 있습니다.

#### 예시 1: 문자열 값을 자기 설명적으로 만들기

```java
// 원본 Java 코드 - 개선 전
Customer customer = order.getCustomer();
assertEquals("573242", customer.getAccountId());
// 실패: ComparisonFailure: expected:<[573242]> but was:<[id not set]>
```

```java
// 원본 Java 코드 - 개선 후
// 테스트 Customer의 account ID를 자기 설명적 값으로 설정
assertEquals("a customer account id", customer.getAccountId());
// 실패: ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
```

```python
# Python 버전
# 개선 전
customer = order.get_customer()
assert customer.account_id == "573242"
# 실패: AssertionError: assert 'id not set' == '573242'

# 개선 후
assert customer.account_id == "a customer account id"
# 실패: AssertionError: assert 'id not set' == 'a customer account id'
#       'id not set'이 무엇을 의미하는지 명확함
```

이제 설명적 메시지를 추가할 필요가 없습니다. **값 자체가 자신의 역할을 설명**하기 때문입니다.

#### 예시 2: 참조 타입에 의미 부여하기

**위치**: 294페이지, 83-103행

```java
// 원본 Java 코드 - 문제 상황
Date startDate = new Date(1000);
Date endDate = new Date(2000);

// 실패 메시지는 날짜가 틀렸다고 하지만 어디서 온 값인지 설명하지 않음:
// java.lang.AssertionError: payment date
// Expected: <Thu Jan 01 01:00:01 GMT 1970>
//      got: <Thu Jan 01 01:00:02 GMT 1970>
```

```java
// 원본 Java 코드 - 해결책: toString() 강제
Date startDate = namedDate(1000, "startDate");
Date endDate = namedDate(2000, "endDate");

Date namedDate(long timeValue, final String name) {
    return new Date(timeValue) {
        public String toString() {
            return name;
        }
    };
}

// 개선된 실패 메시지:
// java.lang.AssertionError: payment date
// Expected: <startDate>
//      got: <endDate>
```

```python
# Python 버전
from datetime import datetime

# 문제 상황
start_date = datetime.fromtimestamp(1.0)
end_date = datetime.fromtimestamp(2.0)

# 실패 시: 1970-01-01 01:00:01과 1970-01-01 01:00:02의 의미가 불명확

# 해결책 1: 커스텀 클래스
class NamedDate(datetime):
    """의미 있는 이름을 가진 날짜"""
    def __new__(cls, timestamp, name):
        instance = super().__new__(cls, timestamp)
        instance._name = name
        return instance

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

start_date = NamedDate(datetime.fromtimestamp(1.0), "startDate")
end_date = NamedDate(datetime.fromtimestamp(2.0), "endDate")

# 실패 시:
# AssertionError: payment date
# Expected: <startDate>
#      got: <endDate>

# 해결책 2: 래퍼 클래스 (더 명시적)
class DateWrapper:
    """날짜를 감싸서 이름을 부여"""
    def __init__(self, date_value, name):
        self.value = date_value
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, DateWrapper):
            return self.value == other.value
        return self.value == other

start_date = DateWrapper(datetime.fromtimestamp(1.0), "startDate")
end_date = DateWrapper(datetime.fromtimestamp(2.0), "endDate")
```

이는 잘못된 필드를 결제 날짜에 할당했음을 명확히 보여줍니다.

#### 도메인 타입과의 연결

**위치**: 294페이지, 104-106행 (각주)

이것은 **도메인 타입을 정의**하여 언어의 기본 타입을 숨기는 또 다른 동기입니다. Chapter 20의 "Domain Types Are Better Than Strings"(213페이지)에서 논의했듯이, 이런 유용한 동작을 매달 곳을 제공합니다.

```python
# 도메인 타입 예시
class AccountId:
    """계정 ID 도메인 타입"""
    def __init__(self, value, description="account id"):
        self.value = value
        self.description = description

    def __eq__(self, other):
        if isinstance(other, AccountId):
            return self.value == other.value
        return self.value == other

    def __repr__(self):
        return f"{self.description}: {self.value}"

class Balance:
    """잔액 도메인 타입"""
    def __init__(self, amount, description="balance"):
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"{self.description}: ${self.amount}"

# 사용
customer = Customer(
    account_id=AccountId("573242", "customer account id"),
    balance=Balance(16301, "outstanding balance")
)

# 실패 시 자동으로 의미 있는 메시지
# Expected: customer account id: 573242
#      but: customer account id: id not set
```

---

### 6. 명백하게 인위적인 값 (Obviously Canned Value) [→ 핵심개념 6]

**위치**: 295페이지, 111-122행

**이전 토픽과의 관계**: 자기 설명이 어려운 기본 타입(char, int)에서도 진단성을 확보하는 방법

#### 기본 타입의 한계

때때로 검증되는 값들이 쉽게 자기 설명을 할 수 없습니다. 예를 들어 `char`나 `int`에는 충분한 정보가 없습니다.

#### 해결책: 비현실적인 값 사용

한 가지 옵션은 **프로덕션에서 예상되는 값과 명백히 다른 비현실적인 값**을 사용하는 것입니다.

```python
# int에 대한 명백하게 인위적인 값
class TestConstants:
    """테스트용 명백하게 인위적인 값들"""

    # 음수가 불가능한 경우
    INVALID_QUANTITY = -1
    INVALID_PRICE = -999

    # 범위를 크게 벗어난 경우
    INVALID_ID = 999999999  # Integer.MAX_VALUE와 유사

    # 명백히 비정상적인 날짜
    EPOCH_DATE = 0  # 1970년 (시스템에 그렇게 오래된 것이 없을 때)

# 사용 예시
def test_order_with_invalid_id():
    """잘못된 ID로 주문 생성 시 실패해야 함"""
    order = Order(id=TestConstants.INVALID_ID)
    assert not order.is_valid()

    # 실패 시: ID가 999999999로 명백히 비정상적임

# 실제 예시: 이전 장의 INVALID_ID
INVALID_ID = -1  # 실제 시스템 ID가 5자리 이상일 때, 3자리는 명백히 잘못됨
```

#### 팀 규칙의 중요성

**위치**: 295페이지, 119-122행

팀이 공통 값에 대한 **규칙을 개발**하면 이러한 값들이 두드러지도록 보장할 수 있습니다. 이전 장 마지막의 `INVALID_ID`는 3자리 길이였습니다. 실제 시스템 식별자가 5자리 이상이라면 이것은 매우 명백히 잘못된 것입니다.

```python
# 팀 규칙 예시
class TestConventions:
    """팀 전체가 따르는 테스트 규칙"""

    # ID 규칙: 실제는 5자리 이상, 테스트는 3자리 이하
    INVALID_CUSTOMER_ID = -1
    INVALID_ORDER_ID = -2
    INVALID_PRODUCT_ID = -3

    # 금액 규칙: 명백히 비현실적인 큰 숫자
    HUGE_AMOUNT = 999999999

    # 문자열 규칙: 역할을 명시하는 명명
    PLACEHOLDER_EMAIL = "test@invalid-domain.test"
    PLACEHOLDER_NAME = "TEST_USER_NAME"

    # 날짜 규칙: 시스템 시작 이전
    BEFORE_SYSTEM_START = datetime(1970, 1, 1)

# 문서화
"""
팀 테스트 규칙:
- ID는 실제 시스템에서 5자리 이상이므로, 테스트용 무효 ID는 음수 사용
- 금액은 현실적으로 10만 이하이므로, 테스트용 큰 값은 999999999 사용
- 이메일은 'test@'로 시작하고 '.test'로 끝남
"""
```

---

### 7. 추적 객체 (Tracer Object) [→ 핵심개념 7]

**위치**: 295-296페이지, 123-163행

**이전 토픽과의 관계**: 명백하게 인위적인 값의 특수한 형태로, 객체의 전달 경로를 추적

#### 추적 객체의 목적

때때로 우리는 단지 객체가 테스트 대상 코드에 의해 전달되고 적절한 협력자로 라우팅되는지만 확인하고 싶을 때가 있습니다.

#### 정의

**추적 객체(Tracer Object)**는 명백하게 인위적인 값의 한 유형으로, 자신의 지원 동작은 없지만 **무언가 실패할 때 자신의 역할을 설명**하는 더미 객체입니다.

#### 예시: jMock을 사용한 추적 객체

```java
// 원본 Java 코드
@RunWith(JMock.class)
public class CustomerTest {
  final LineItem item1 = context.mock(LineItem.class, "item1");
  final LineItem item2 = context.mock(LineItem.class, "item2");
  final Billing billing = context.mock(Billing.class);

  @Test public void
  requestsInvoiceForPurchasedItems() {
    context.checking(new Expectations() {{
      oneOf(billing).add(item1);
      oneOf(billing).add(item2);
    }});

    customer.purchase(item1, item2);
    customer.requestInvoice(billing);
  }
}
```

```python
# Python 버전 (unittest.mock 사용)
import unittest
from unittest.mock import Mock, call

class CustomerTest(unittest.TestCase):
    def setUp(self):
        # 추적 객체 생성: 이름을 부여하여 실패 시 역할 식별
        self.item1 = Mock(spec=LineItem, name="item1")
        self.item2 = Mock(spec=LineItem, name="item2")
        self.billing = Mock(spec=Billing)

    def test_requests_invoice_for_purchased_items(self):
        """구매한 항목들에 대한 송장을 요청해야 함"""
        customer = Customer()

        # 행동
        customer.purchase(self.item1, self.item2)
        customer.request_invoice(self.billing)

        # 검증: billing.add()가 각 항목에 대해 호출되었는지
        self.billing.add.assert_has_calls([
            call(self.item1),
            call(self.item2)
        ])

# Python 버전 (pytest-mock 사용 - 더 간결)
def test_requests_invoice_for_purchased_items(mocker):
    """구매한 항목들에 대한 송장을 요청해야 함"""
    # 추적 객체 생성
    item1 = mocker.Mock(spec=LineItem, name="item1")
    item2 = mocker.Mock(spec=LineItem, name="item2")
    billing = mocker.Mock(spec=Billing)

    customer = Customer()
    customer.purchase(item1, item2)
    customer.request_invoice(billing)

    # 검증
    assert billing.add.call_args_list == [
        mocker.call(item1),
        mocker.call(item2)
    ]
```

#### 실패 보고서

**위치**: 296페이지, 144-151행

```
not all expectations were satisfied
expectations:
  expected once, already invoked 1 time: billing.add(<item1>)
  ! expected once, never invoked: billing.add(<item2>)
what happened before this:
  billing.add(<item1>)
```

jMock은 mock 객체 생성 시 **이름을 받을 수 있으며** 이는 실패 보고에 사용됩니다. 실제로 같은 타입의 mock 객체가 둘 이상 있으면 jMock은 혼란을 피하기 위해 이름을 부여하도록 강제합니다(기본값은 클래스 이름 사용).

```python
# Python에서 명시적 이름 부여의 중요성
def test_multiple_mocks_without_names():
    """이름 없는 여러 mock - 혼란스러운 실패 메시지"""
    item1 = Mock(spec=LineItem)  # 이름 없음
    item2 = Mock(spec=LineItem)  # 이름 없음
    # 실패 시: <Mock id='...'> vs <Mock id='...'>
    # 어떤 mock이 문제인지 구분 어려움

def test_multiple_mocks_with_names():
    """이름 있는 여러 mock - 명확한 실패 메시지"""
    item1 = Mock(spec=LineItem, name="item1")  # 명확한 이름
    item2 = Mock(spec=LineItem, name="item2")  # 명확한 이름
    # 실패 시: <Mock name='item1'> vs <Mock name='item2'>
    # 정확히 어떤 mock이 문제인지 명확함
```

#### 설계 도구로서의 활용

**위치**: 296페이지, 160-163행

추적 객체는 클래스를 TDD할 때 유용한 설계 도구가 될 수 있습니다. 때때로 우리는 도메인 개념을 표시(하고 이름 붙이기)하고 협력에서 어떻게 사용되는지 보여주기 위해 **빈 인터페이스**를 사용합니다. 나중에 코드를 키워가면서 인터페이스를 동작을 설명하는 메서드로 채웁니다.

```python
# 초기: 빈 인터페이스로 도메인 개념 표시
class PaymentMethod:
    """결제 방법 - TDD 초기 단계"""
    pass

class CreditCard(PaymentMethod):
    """신용카드 결제"""
    pass

class BankTransfer(PaymentMethod):
    """계좌 이체 결제"""
    pass

# 테스트: 추적 객체로 협력 관계 정의
def test_order_accepts_payment_method():
    """주문이 결제 방법을 받아들여야 함"""
    payment = Mock(spec=PaymentMethod, name="payment_method")
    order = Order()

    order.set_payment_method(payment)

    assert order.payment_method is payment

# 나중: 인터페이스에 동작 추가
class PaymentMethod:
    """결제 방법"""
    def authorize(self, amount: Decimal) -> bool:
        """결제 승인"""
        raise NotImplementedError

    def charge(self, amount: Decimal) -> Transaction:
        """결제 실행"""
        raise NotImplementedError

    def refund(self, transaction: Transaction) -> bool:
        """환불 처리"""
        raise NotImplementedError

# 진화한 테스트
def test_order_charges_payment_method():
    """주문이 결제 방법으로 결제를 실행해야 함"""
    payment = Mock(spec=PaymentMethod, name="credit_card")
    payment.authorize.return_value = True
    payment.charge.return_value = Transaction(id="TXN123")

    order = Order(total=Decimal("100.00"))
    order.set_payment_method(payment)
    result = order.process_payment()

    payment.authorize.assert_called_once_with(Decimal("100.00"))
    payment.charge.assert_called_once_with(Decimal("100.00"))
    assert result.transaction_id == "TXN123"
```

---

### 8. 명시적 기대치 충족 단언 (Explicitly Assert That Expectations Were Satisfied) [→ 핵심개념 8]

**위치**: 296페이지, 164-178행

**이전 토픽과의 관계**: Mock 프레임워크 사용 시 발생할 수 있는 혼란스러운 실패 보고를 해결하는 방법

#### 문제: 혼란스러운 실패 보고

기대치(expectations)와 단언(assertions)을 모두 가진 테스트는 혼란스러운 실패를 만들 수 있습니다.

jMock과 다른 mock 객체 프레임워크에서 **기대치는 테스트 본문 후에 확인**됩니다. 예를 들어 협력이 제대로 작동하지 않아 잘못된 값을 반환하면, 기대치가 확인되기 전에 단언이 실패할 수 있습니다.

```python
# 문제 상황
def test_calculate_total_with_discount(mocker):
    """할인이 적용된 총액 계산"""
    calculator = mocker.Mock()
    calculator.apply_discount.return_value = Decimal("90.00")  # 실제로는 다른 값 반환

    order = Order(calculator=calculator)
    order.add_item(Item(price=Decimal("100.00")))

    # 행동
    total = order.calculate_total(discount_code="SAVE10")

    # 문제: 이 단언이 먼저 실패
    assert total == Decimal("90.00")
    # 실제로는 apply_discount가 호출되지 않았는데
    # 단언 실패만 보고되어 협력 문제를 놓침

    # 기대치는 테스트 후에 확인 (unittest 프레임워크에 의해)
    calculator.apply_discount.assert_called_once()
```

이는 실제 원인인 누락된 협력이 아니라 잘못된 계산 결과를 보여주는 실패 보고를 만듭니다.

#### 해결책: 명시적 기대치 확인

```java
// 원본 Java 코드
context.assertIsSatisfied();
assertThat(result, equalTo(expectedResult));
```

```python
# Python 버전
def test_calculate_total_with_discount_explicit(mocker):
    """할인이 적용된 총액 계산 - 명시적 기대치 확인"""
    calculator = mocker.Mock()
    calculator.apply_discount.return_value = Decimal("90.00")

    order = Order(calculator=calculator)
    order.add_item(Item(price=Decimal("100.00")))

    # 행동
    total = order.calculate_total(discount_code="SAVE10")

    # 해결책: 기대치를 먼저 명시적으로 확인
    calculator.apply_discount.assert_called_once_with(
        Decimal("100.00"), "SAVE10"
    )
    # 이제 협력 문제를 먼저 발견

    # 그 다음 결과 확인
    assert total == Decimal("90.00")

# 더 나은 구조: 명확한 단계 분리
def test_order_calculation_with_clear_phases(mocker):
    """명확한 단계 분리로 협력과 결과를 각각 확인"""
    # Setup
    calculator = mocker.Mock()
    calculator.apply_discount.return_value = Decimal("90.00")
    order = Order(calculator=calculator)
    order.add_item(Item(price=Decimal("100.00")))

    # Exercise
    total = order.calculate_total(discount_code="SAVE10")

    # Verify - 단계 1: 협력 확인
    calculator.apply_discount.assert_called_once_with(
        Decimal("100.00"), "SAVE10"
    )

    # Verify - 단계 2: 결과 확인
    assert total == Decimal("90.00"), \
        f"Expected total of 90.00 but got {total}"
```

#### "Watch the Test Fail"과의 연결

**위치**: 296페이지, 175-178행

이는 "Watch the Test Fail"(42페이지)이 중요한 이유를 보여줍니다. 테스트가 기대치가 충족되지 않아 실패할 것으로 예상했는데 대신 사후조건 단언이 실패하면, 모든 기대치가 충족되었음을 단언하는 명시적 호출을 추가해야 한다는 것을 알게 됩니다.

```python
# "Watch the Test Fail" 예시
def test_development_process():
    """TDD 프로세스에서 테스트 실패를 관찰하는 것의 중요성"""

    # 1. 테스트 작성 - 기대치가 충족되지 않을 것으로 예상
    def test_first_attempt(mocker):
        billing = mocker.Mock()
        customer = Customer()

        customer.request_invoice(billing)

        # 예상: billing.add()가 호출되지 않아 실패
        billing.add.assert_called()

        result = customer.get_invoice_total()
        assert result == 100

    # 실제 실패: result 단언에서 실패 (0 != 100)
    # 이는 협력 문제가 아니라 계산 문제처럼 보임

    # 2. 수정 - 명시적 기대치 확인 추가
    def test_corrected(mocker):
        billing = mocker.Mock()
        customer = Customer()

        customer.request_invoice(billing)

        # 먼저 협력 확인
        billing.add.assert_called()  # 이제 올바른 실패 보고

        # 그 다음 결과 확인
        result = customer.get_invoice_total()
        assert result == 100
```

---

### 9. 진단은 일급 기능 (Diagnostics Are a First-Class Feature) [→ 핵심개념 9]

**위치**: 297페이지, 179-196행

**이전 토픽과의 관계**: 모든 개별 기법들을 전체 TDD 프로세스에 통합하는 메타 수준의 원칙

#### 3단계에서 4단계 TDD 사이클로

**위치**: 297페이지, 179-185행

모든 사람들처럼 우리도 단순한 3단계 TDD 사이클(fail → pass → refactor)에 휩쓸리기 쉽습니다. 좋은 진전을 이루고 있고 방금 테스트를 작성했기 때문에 실패의 의미를 알고 있습니다.

하지만 요즘 우리는 Chapter 5에서 설명한 **4단계 TDD 사이클**(fail → **report** → pass → refactor)을 따르려고 노력합니다. 그것이 우리가 기능을 이해했다는 것을 아는 방법이고, 한 달 후 이것을 변경해야 하는 사람도 이해할 것이기 때문입니다.

```python
# 3단계 TDD 사이클 (기본)
def three_step_tdd():
    """기본 TDD 사이클"""

    # 1. FAIL: 테스트 작성
    def test_customer_discount():
        customer = Customer(loyalty_points=100)
        assert customer.get_discount() == 0.1

    # 2. PASS: 최소한의 구현
    class Customer:
        def get_discount(self):
            return 0.1

    # 3. REFACTOR: 리팩토링
    class Customer:
        def get_discount(self):
            if self.loyalty_points >= 100:
                return 0.1
            return 0.0

# 4단계 TDD 사이클 (개선됨)
def four_step_tdd():
    """진단이 포함된 TDD 사이클"""

    # 1. FAIL: 테스트 작성
    def test_customer_discount():
        customer = Customer(loyalty_points=100)
        assert customer.get_discount() == 0.1

    # 2. REPORT: 실패 메시지 개선
    def test_customer_discount_improved():
        customer = Customer(loyalty_points=100)
        discount = customer.get_discount()
        assert discount == 0.1, \
            f"Customer with {customer.loyalty_points} loyalty points " \
            f"should get 10% discount, but got {discount*100}%"
        # 실패 시 명확한 메시지:
        # "Customer with 100 loyalty points should get 10% discount, but got 0%"

    # 3. PASS: 구현
    class Customer:
        def __init__(self, loyalty_points=0):
            self.loyalty_points = loyalty_points

        def get_discount(self):
            if self.loyalty_points >= 100:
                return 0.1
            return 0.0

    # 4. REFACTOR: 리팩토링
    class Customer:
        DISCOUNT_THRESHOLD = 100
        DISCOUNT_RATE = 0.1

        def __init__(self, loyalty_points=0):
            self.loyalty_points = loyalty_points

        def get_discount(self):
            if self.loyalty_points >= self.DISCOUNT_THRESHOLD:
                return self.DISCOUNT_RATE
            return 0.0

# 더 나은 진단을 위한 도메인 타입 활용
def advanced_diagnostics():
    """도메인 타입으로 자기 설명적 테스트 만들기"""

    class LoyaltyPoints:
        def __init__(self, points):
            self.points = points

        def __repr__(self):
            return f"LoyaltyPoints({self.points})"

    class Discount:
        def __init__(self, rate):
            self.rate = rate

        def __repr__(self):
            return f"Discount({self.rate*100}%)"

        def __eq__(self, other):
            if isinstance(other, Discount):
                return abs(self.rate - other.rate) < 0.0001
            return False

    class Customer:
        def __init__(self, loyalty_points: LoyaltyPoints):
            self.loyalty_points = loyalty_points

        def get_discount(self) -> Discount:
            if self.loyalty_points.points >= 100:
                return Discount(0.1)
            return Discount(0.0)

    # 테스트: 값 자체가 의미를 설명
    def test_customer_discount_with_domain_types():
        customer = Customer(LoyaltyPoints(100))
        expected = Discount(0.1)
        actual = customer.get_discount()

        assert actual == expected
        # 실패 시: "Discount(0%) != Discount(10%)"
        # 명확하고 도메인 언어로 표현됨
```

#### 테스트 품질 유지의 중요성

**위치**: 297페이지, 185-188행

Figure 23.1은 프로덕션 코드뿐만 아니라 **테스트의 품질도 유지해야** 한다는 것을 다시 보여줍니다.

```python
# 테스트 품질 유지 체크리스트
class TestQualityChecklist:
    """테스트 품질을 유지하기 위한 체크리스트"""

    def check_test_quality(self, test_code):
        """테스트 품질 확인"""
        checks = {
            'small_and_focused': self._is_small_and_focused(test_code),
            'well_named': self._has_clear_name(test_code),
            'clear_failure_messages': self._has_clear_messages(test_code),
            'self_describing_values': self._uses_domain_types(test_code),
            'explicit_expectations': self._checks_expectations_first(test_code),
        }
        return all(checks.values()), checks

    def _is_small_and_focused(self, test_code):
        """테스트가 작고 집중되어 있는가?"""
        # 하나의 개념만 테스트하는가?
        # 너무 많은 단언을 포함하지 않는가?
        pass

    def _has_clear_name(self, test_code):
        """명확한 이름을 가지고 있는가?"""
        # 테스트 이름이 무엇을 검증하는지 명확한가?
        # 실패 시 이름만으로도 문제를 짐작할 수 있는가?
        pass

    def _has_clear_messages(self, test_code):
        """명확한 실패 메시지를 제공하는가?"""
        # 단언에 설명적 메시지가 있는가?
        # Matcher를 사용하여 세부사항을 제공하는가?
        pass

    def _uses_domain_types(self, test_code):
        """자기 설명적인 값을 사용하는가?"""
        # 도메인 타입을 사용하는가?
        # 값이 자신의 역할을 설명하는가?
        pass

    def _checks_expectations_first(self, test_code):
        """기대치를 먼저 확인하는가?"""
        # Mock을 사용할 때 순서가 올바른가?
        pass

# 실전 적용
def test_with_quality_in_mind():
    """품질을 염두에 둔 테스트 작성"""

    # ✅ Small and Focused
    def test_customer_discount_for_gold_tier():
        """골드 등급 고객은 10% 할인을 받아야 함"""
        # 하나의 개념만 테스트
        pass

    # ✅ Well-Named
    # 위의 함수 이름이 정확히 무엇을 테스트하는지 설명

    # ✅ Clear Failure Messages
    def test_with_messages():
        customer = Customer(tier="gold")
        discount = customer.get_discount()
        assert discount.rate == 0.1, \
            f"Gold tier customer should get 10% discount, got {discount}"

    # ✅ Self-Describing Values
    gold_tier = CustomerTier("gold", "Gold Membership")
    # 값 자체가 "Gold Membership"으로 자신을 설명

    # ✅ Explicit Expectations
    def test_with_mocks(mocker):
        notification = mocker.Mock()
        customer = Customer()
        customer.upgrade_tier(notification)

        # 먼저 협력 확인
        notification.send.assert_called_once()
        # 그 다음 결과 확인
        assert customer.tier == "gold"
```

#### 장기적 관점

진단 품질은 다음을 보장합니다:
1. **현재**: 방금 작성한 테스트를 이해함
2. **단기**: 오늘 작업 중 다른 테스트 실패 시 빠른 진단
3. **장기**: 한 달 후 코드를 수정할 사람도 실패 원인을 즉시 파악

```python
# 시간의 흐름에 따른 테스트 가치
class TestLifecycle:
    """테스트의 생애주기에 걸친 가치"""

    def immediate_value(self):
        """즉각적 가치: 방금 작성한 테스트"""
        # - 요구사항을 명확히 이해했는지 확인
        # - 구현 가이드 제공
        pass

    def short_term_value(self):
        """단기 가치: 오늘의 개발 작업"""
        # - 리팩토링 시 안전망
        # - 다른 영역 수정 시 영향 감지
        pass

    def long_term_value(self):
        """장기 가치: 몇 주/몇 달 후"""
        # - 실행 가능한 문서화
        # - 새로운 팀원의 이해 도움
        # - 유지보수 비용 절감
        pass

# 좋은 진단은 모든 단계에서 가치 제공
def test_long_term_maintainability():
    """장기 유지보수를 고려한 테스트"""
    # 6개월 후 이 테스트를 보는 개발자를 생각하며 작성

    # 명확한 컨텍스트
    premium_customer = Customer(
        tier=CustomerTier("premium", "Premium Membership"),
        purchase_history=PurchaseHistory(total=Decimal("1000.00"))
    )

    # 명확한 행동
    discount = premium_customer.calculate_loyalty_discount()

    # 명확한 검증
    assert discount == Discount(0.15), \
        "Premium customers with $1000+ purchase history " \
        "should receive 15% loyalty discount"

    # 이 테스트가 실패하면 읽는 사람은 즉시 이해할 수 있음:
    # - 누가: Premium 고객
    # - 무엇을: $1000 이상 구매 이력
    # - 왜: 15% 충성 할인을 받아야 함
```

#### 4단계 TDD 사이클 다이어그램

**위치**: 297페이지, Figure 23.1

```
┌─────────────────────────────────────────────────────────┐
│                  4-Step TDD Cycle                        │
│                                                          │
│  ┌──────┐    ┌────────┐    ┌──────┐    ┌──────────┐   │
│  │ FAIL │ -> │ REPORT │ -> │ PASS │ -> │ REFACTOR │   │
│  └──────┘    └────────┘    └──────┘    └──────────┘   │
│      ↑                                        │          │
│      └────────────────────────────────────────┘          │
│                                                          │
│  각 단계의 품질 유지:                                       │
│  - FAIL: 올바른 이유로 실패하는가?                          │
│  - REPORT: 실패 메시지가 명확한가?                         │
│  - PASS: 최소한의 올바른 구현인가?                         │
│  - REFACTOR: 코드와 테스트 모두 개선되었는가?               │
└─────────────────────────────────────────────────────────┘
```

```python
# 4단계 사이클 실전 예시
class FourStepTDDInPractice:
    """4단계 TDD 사이클 실전 적용"""

    def step_1_fail(self):
        """1단계: 실패하는 테스트 작성"""
        def test_premium_shipping_cost():
            order = Order(shipping_method="premium")
            cost = order.calculate_shipping_cost()
            assert cost == Decimal("0.00")

        # 실행: AttributeError (calculate_shipping_cost 미구현)
        # ✓ 올바른 이유로 실패

    def step_2_report(self):
        """2단계: 진단 개선"""
        def test_premium_shipping_cost():
            """프리미엄 회원은 무료 배송을 받아야 함"""
            order = Order(
                items=[Item(name="Product A", price=Decimal("100.00"))],
                customer=Customer(tier="premium"),
                shipping_method=ShippingMethod("express")
            )

            cost = order.calculate_shipping_cost()

            assert cost == Decimal("0.00"), \
                f"Premium customers should have free shipping, " \
                f"but got ${cost}"

        # 이제 실패 메시지가 명확함:
        # "Premium customers should have free shipping, but got $15.00"

    def step_3_pass(self):
        """3단계: 구현"""
        class Order:
            def calculate_shipping_cost(self):
                if self.customer.tier == "premium":
                    return Decimal("0.00")
                return self.shipping_method.base_cost

        # 테스트 통과

    def step_4_refactor(self):
        """4단계: 리팩토링 (코드와 테스트 모두)"""
        # 프로덕션 코드 리팩토링
        class Order:
            def calculate_shipping_cost(self):
                if self._is_free_shipping_eligible():
                    return Decimal("0.00")
                return self._calculate_standard_shipping()

            def _is_free_shipping_eligible(self):
                return self.customer.is_premium()

        # 테스트 리팩토링
        def test_premium_customer_gets_free_shipping(self):
            """프리미엄 고객은 무료 배송"""
            order = self._create_order_for_premium_customer()
            assert_free_shipping(order)

        def _create_order_for_premium_customer(self):
            return Order(
                customer=Customer(tier=CustomerTier.PREMIUM),
                shipping_method=ShippingMethod.EXPRESS
            )

        def assert_free_shipping(order):
            cost = order.calculate_shipping_cost()
            assert cost == Decimal("0.00"), \
                "Expected free shipping for premium customer"
```

---

## 전체 요약

이 장은 **테스트 진단의 중요성**과 구체적인 구현 기법들을 다룹니다:

1. **철학적 기반**: 테스트의 목적은 실패를 통한 오류 발견이며, 진단 불가능한 실패는 피해야 함
2. **기본 원칙**: 작고 집중된 테스트와 명확한 이름
3. **단언 수준**: 설명적 메시지와 Hamcrest Matcher 활용
4. **데이터 수준**: 자기 설명적 값, 명백하게 인위적인 값, 추적 객체
5. **Mock 특수 상황**: 명시적 기대치 확인
6. **프로세스 통합**: 4단계 TDD 사이클 (fail → report → pass → refactor)

모든 기법의 목표는 **디버거 없이도 테스트 실패 원인을 즉시 파악**할 수 있는 자기 진단적 테스트를 만드는 것입니다.
