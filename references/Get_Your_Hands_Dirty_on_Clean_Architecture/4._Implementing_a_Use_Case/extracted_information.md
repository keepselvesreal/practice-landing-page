"""
생성 시간: 2025년 10월 3일 11시 58분 50초
핵심 내용: Hexagonal Architecture에서 Use Case 구현 방법
상세 내용:
    - Domain Model 구현 (Line 12-129): Account 엔티티와 활동 추적 방식
    - Use Case 구조 (Line 130-196): Use Case의 4단계 실행 흐름
    - Input Validation (Line 200-363): 입력 검증을 Input Model에서 처리
    - Constructor 활용 (Line 364-402): 불변 객체 생성과 컴파일 타임 검증
    - Use Case별 Input Model 분리 (Line 403-427): 각 Use Case마다 전용 Input Model 사용
    - Business Rule Validation (Line 428-521): 도메인 상태 기반 비즈니스 규칙 검증
    - Rich vs Anemic Domain Model (Line 522-547): 도메인 모델 구현 스타일 비교
    - Use Case별 Output Model 분리 (Line 548-575): 각 Use Case마다 최소한의 Output 반환
    - Read-Only Use Cases (Line 576-625): 조회 전용 Use Case를 Query Service로 구현
    - 유지보수성 향상 (Line 626-635): Use Case별 모델 분리의 장점
상태: active
참조: N/A (원본 파일)
"""
# # Get_Your_Hands_Dirty_on_Clean_Architecture Chapter4: Implementing a Use Case

# ============================================================
# 압축 내용
# ============================================================

**Hexagonal Architecture의 Use Case는 Input Validation(입력 모델), Business Rule Validation(도메인 엔티티/Use Case), Domain State Manipulation(도메인 엔티티), Output Return(최소한의 출력)의 4단계로 구현되며, 각 Use Case마다 전용 Input/Output 모델을 사용하여 결합도를 낮추고 유지보수성을 높인다.**

[참조: Line 130-196, 200-635]


# ============================================================
# 핵심 내용
# ============================================================

## 핵심 개념

1. **Use Case 4단계 구조** → [상세: Use Case 구조]
2. **Input Validation vs Business Rule Validation 분리** → [상세: Input Validation, Business Rule Validation]
3. **Use Case별 전용 Input/Output 모델** → [상세: Use Case별 Input Model 분리, Use Case별 Output Model 분리]
4. **Domain Model 구현 방식** → [상세: Domain Model 구현, Rich vs Anemic Domain Model]
5. **Constructor 기반 불변성과 검증** → [상세: Constructor 활용]
6. **Query Service 패턴** → [상세: Read-Only Use Cases]

---

## 핵심 개념 설명

### 1. Use Case 4단계 구조 → [상세: Use Case 구조]
Use Case는 (1) Input 받기, (2) 비즈니스 규칙 검증, (3) 모델 상태 조작, (4) Output 반환의 4단계로 실행된다. Input Validation은 Use Case 클래스가 아닌 Input 모델에서 처리하고, Business Rule Validation은 도메인 엔티티나 Use Case에서 처리한다.

[참조: Line 130-196]

### 2. Input Validation vs Business Rule Validation 분리 → [상세: Input Validation, Business Rule Validation]
**Input Validation**은 도메인 모델 상태 접근 없이 선언적으로 검증 가능한 구문적(syntactical) 검증이며, **Business Rule Validation**은 도메인 모델의 현재 상태에 접근이 필요한 의미적(semantical) 검증이다. 예: "송금액 > 0"은 Input Validation, "출금 계좌 잔액 부족 여부"는 Business Rule Validation.

[참조: Line 200-363, 428-521]

### 3. Use Case별 전용 Input/Output 모델 → [상세: Use Case별 Input Model 분리, Use Case별 Output Model 분리]
각 Use Case마다 전용 Input/Output 모델을 사용하면 Use Case 간 결합도가 낮아지고 의도가 명확해진다. 공유 모델은 시간이 지나면서 비대해지고, 한 Use Case의 변경이 다른 Use Case에 영향을 준다.

[참조: Line 403-427, 548-575]

### 4. Domain Model 구현 방식 → [상세: Domain Model 구현, Rich vs Anemic Domain Model]
**Rich Domain Model**은 도메인 로직을 엔티티에 최대한 포함시키고 Use Case는 오케스트레이션만 담당한다. **Anemic Domain Model**은 엔티티가 상태와 getter/setter만 가지고, Use Case가 도메인 로직을 포함한다. 두 방식 모두 Hexagonal Architecture에서 구현 가능하다.

[참조: Line 12-129, 522-547]

### 5. Constructor 기반 불변성과 검증 → [상세: Constructor 활용]
불변(immutable) Input 모델은 생성자에서 모든 필드를 초기화하고 검증한다. Builder 패턴 대신 생성자를 직접 사용하면 필드 추가/삭제 시 컴파일 에러로 모든 호출부를 추적할 수 있어 안전하다.

[참조: Line 364-402]

### 6. Query Service 패턴 → [상세: Read-Only Use Cases]
읽기 전용 작업은 Use Case가 아닌 Query로 구분하여 Query Service로 구현한다. 이는 CQS(Command-Query Separation)와 CQRS(Command-Query Responsibility Segregation) 개념과 잘 맞는다.

[참조: Line 576-625]

---

## 핵심 개념 간의 관계

- **Use Case 4단계 구조**는 **Input Validation vs Business Rule Validation 분리**를 통해 각 단계의 책임을 명확히 한다
- **Use Case별 전용 Input/Output 모델**은 **Use Case 4단계 구조**의 Input/Output 단계를 구체화하고 결합도를 낮춘다
- **Constructor 기반 불변성과 검증**은 **Input Validation**을 안전하고 명확하게 구현하는 방법이다
- **Domain Model 구현 방식**은 **Business Rule Validation**이 엔티티 또는 Use Case 중 어디에 위치할지를 결정한다
- **Query Service 패턴**은 **Use Case 4단계 구조** 중 상태 변경이 없는 읽기 전용 작업을 별도로 분리한 것이다

[참조: Line 130-635]


# ============================================================
# 상세 내용
# ============================================================

### 목차
1. Domain Model 구현
2. Use Case 구조
3. Input Validation
4. Constructor 활용
5. Use Case별 Input Model 분리
6. Business Rule Validation
7. Rich vs Anemic Domain Model
8. Use Case별 Output Model 분리
9. Read-Only Use Cases
10. 유지보수성 향상

## 1. Domain Model 구현 [Line 12-129] → [핵심: Domain Model 구현 방식]

### 화제: Account 엔티티 설계

**Account 엔티티**는 계좌의 현재 스냅샷을 나타낸다. 모든 출금과 입금은 **Activity 엔티티**로 기록된다. 모든 활동을 메모리에 로드하는 것은 비효율적이므로, Account는 최근 며칠/몇 주의 활동만 **ActivityWindow** 값 객체에 보관한다.

```java
// Java 코드 (Line 18-112)
package buckpal.domain;

public class Account {
    private AccountId id;  // 계좌 ID
    private Money baselineBalance;  // 기준 잔액 (ActivityWindow 이전 시점의 잔액)
    private ActivityWindow activityWindow;  // 최근 활동 목록

    // 생성자와 getter 생략

    // 현재 잔액 계산: 기준 잔액 + 활동 윈도우의 잔액 변화
    public Money calculateBalance() {
        return Money.add(
            this.baselineBalance,
            this.activityWindow.calculateBalance(this.id));
    }

    // 출금 메서드: 비즈니스 규칙 검증 후 활동 추가
    public boolean withdraw(Money money, AccountId targetAccountId) {
        if (!mayWithdraw(money)) {  // 비즈니스 규칙: 출금 가능 여부 확인
            return false;
        }

        // 출금 활동 생성 및 추가
        Activity withdrawal = new Activity(
            this.id,  // 소유 계좌 ID
            this.id,  // 출발 계좌 ID
            targetAccountId,  // 도착 계좌 ID
            LocalDateTime.now(),  // 시간
            money);  // 금액
        this.activityWindow.addActivity(withdrawal);
        return true;
    }

    // 출금 가능 여부 검증 (비즈니스 규칙)
    private boolean mayWithdraw(Money money) {
        return Money.add(
            this.calculateBalance(),  // 현재 잔액
            money.negate())  // 출금액의 음수
            .isPositive();  // 결과가 양수인지 확인 (잔액 부족 방지)
    }

    // 입금 메서드: 활동 추가
    public boolean deposit(Money money, AccountId sourceAccountId) {
        Activity deposit = new Activity(
            this.id,  // 소유 계좌 ID
            sourceAccountId,  // 출발 계좌 ID
            this.id,  // 도착 계좌 ID
            LocalDateTime.now(),  // 시간
            money);  // 금액
        this.activityWindow.addActivity(deposit);
        return true;
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Account:
    id: AccountId
    baseline_balance: Money  # 기준 잔액 (ActivityWindow 이전 시점의 잔액)
    activity_window: ActivityWindow  # 최근 활동 목록

    def calculate_balance(self) -> Money:
        """현재 잔액 계산: 기준 잔액 + 활동 윈도우의 잔액 변화"""
        return Money.add(
            self.baseline_balance,
            self.activity_window.calculate_balance(self.id))

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        """출금 메서드: 비즈니스 규칙 검증 후 활동 추가"""
        if not self._may_withdraw(money):  # 비즈니스 규칙: 출금 가능 여부 확인
            return False

        # 출금 활동 생성 및 추가
        withdrawal = Activity(
            owner_account_id=self.id,  # 소유 계좌 ID
            source_account_id=self.id,  # 출발 계좌 ID
            target_account_id=target_account_id,  # 도착 계좌 ID
            timestamp=datetime.now(),  # 시간
            money=money)  # 금액
        self.activity_window.add_activity(withdrawal)
        return True

    def _may_withdraw(self, money: Money) -> bool:
        """출금 가능 여부 검증 (비즈니스 규칙)"""
        return Money.add(
            self.calculate_balance(),  # 현재 잔액
            money.negate()  # 출금액의 음수
        ).is_positive()  # 결과가 양수인지 확인 (잔액 부족 방지)

    def deposit(self, money: Money, source_account_id: AccountId) -> bool:
        """입금 메서드: 활동 추가"""
        deposit_activity = Activity(
            owner_account_id=self.id,  # 소유 계좌 ID
            source_account_id=source_account_id,  # 출발 계좌 ID
            target_account_id=self.id,  # 도착 계좌 ID
            timestamp=datetime.now(),  # 시간
            money=money)  # 금액
        self.activity_window.add_activity(deposit_activity)
        return True
```

**핵심 포인트**:
- `baselineBalance`: ActivityWindow 이전 시점의 계좌 잔액
- 현재 잔액 = baselineBalance + activityWindow의 잔액 변화
- 출금/입금은 새로운 Activity를 activityWindow에 추가
- 비즈니스 규칙("계좌 초과 출금 불가")은 `mayWithdraw()` 메서드에서 검증

[참조: Line 12-129] → [핵심: Domain Model 구현 방식]

---

## 2. Use Case 구조 [Line 130-196] → [핵심: Use Case 4단계 구조]

### 이전 화제와의 관계
Domain Model(Account 엔티티)을 구현했으니, 이제 이를 활용하는 Use Case를 구현한다.

### 화제: Use Case의 4단계 실행 흐름

Use Case는 다음 4단계를 따른다:

1. **Input 받기**: Incoming Adapter로부터 입력을 받는다
2. **비즈니스 규칙 검증**: 도메인 로직에 집중, 입력 검증은 별도 처리
3. **모델 상태 조작**: 도메인 객체의 상태를 변경하고 Persistence Adapter를 통해 저장
4. **Output 반환**: Outgoing Adapter의 반환값을 Output 객체로 변환하여 반환

**"Send Money" Use Case 예시**:

```java
// Java 코드 (Line 159-188)
package buckpal.application.service;

@RequiredArgsConstructor  // Lombok: final 필드로 생성자 자동 생성
@Transactional  // 트랜잭션 관리
public class SendMoneyService implements SendMoneyUseCase {

    private final LoadAccountPort loadAccountPort;  // Outgoing Port: 계좌 로드
    private final AccountLock accountLock;  // 계좌 잠금 (동시성 제어)
    private final UpdateAccountStatePort updateAccountStatePort;  // Outgoing Port: 계좌 상태 저장

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        // TODO: validate business rules (비즈니스 규칙 검증)
        // TODO: manipulate model state (모델 상태 조작)
        // TODO: return output (출력 반환)
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from abc import ABC, abstractmethod

class SendMoneyService:
    """송금 Use Case 서비스"""

    def __init__(
        self,
        load_account_port: LoadAccountPort,  # Outgoing Port: 계좌 로드
        account_lock: AccountLock,  # 계좌 잠금 (동시성 제어)
        update_account_state_port: UpdateAccountStatePort  # Outgoing Port: 계좌 상태 저장
    ):
        self.load_account_port = load_account_port
        self.account_lock = account_lock
        self.update_account_state_port = update_account_state_port

    def send_money(self, command: SendMoneyCommand) -> bool:
        """송금 실행"""
        # TODO: validate business rules (비즈니스 규칙 검증)
        # TODO: manipulate model state (모델 상태 조작)
        # TODO: return output (출력 반환)
        pass
```

**아키텍처 구조**:
- SendMoneyService는 **Incoming Port** (SendMoneyUseCase)를 구현
- **Outgoing Port** (LoadAccountPort, UpdateAccountStatePort)를 호출하여 영속성 작업 수행
- 각 Use Case마다 별도의 Service 클래스를 만들어 "Broad Service" 문제를 피함

[참조: Line 130-196] → [핵심: Use Case 4단계 구조]

---

## 3. Input Validation [Line 200-363] → [핵심: Input Validation vs Business Rule Validation 분리, Constructor 기반 불변성과 검증]

### 이전 화제와의 관계
Use Case의 4단계 중 첫 번째 단계인 "Input 받기"를 구체적으로 구현한다.

### 화제: Input Validation을 Input Model에서 처리

**Input Validation을 Use Case 클래스가 아닌 Input 모델에서 처리하는 이유**:
1. Use Case는 도메인 로직에 집중해야 함
2. 여러 Adapter가 같은 Use Case를 호출할 수 있으므로, 각 Adapter에서 검증하면 중복 발생
3. Application Layer는 외부로부터 유효하지 않은 입력이 들어오는 것을 막아야 함

**SendMoneyCommand 구현 (Bean Validation 사용)**:

```java
// Java 코드 (Line 274-315)
package buckpal.application.port.in;

@Getter
public class SendMoneyCommand extends SelfValidating<SendMoneyCommand> {

    @NotNull  // Bean Validation 어노테이션: null 불가
    private final AccountId sourceAccountId;  // 출발 계좌 ID

    @NotNull
    private final AccountId targetAccountId;  // 도착 계좌 ID

    @NotNull
    private final Money money;  // 송금액

    public SendMoneyCommand(
        AccountId sourceAccountId,
        AccountId targetAccountId,
        Money money) {
        this.sourceAccountId = sourceAccountId;
        this.targetAccountId = targetAccountId;
        this.money = money;
        requireGreaterThan(money, 0);  // 수동 검증: 송금액 > 0
        this.validateSelf();  // Bean Validation 실행
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)  # frozen=True로 불변성 보장
class SendMoneyCommand:
    """송금 명령 Input Model"""

    source_account_id: AccountId  # 출발 계좌 ID
    target_account_id: AccountId  # 도착 계좌 ID
    money: Money  # 송금액

    def __post_init__(self):
        """생성 후 검증 (Bean Validation 대신 사용)"""
        # None 체크
        if self.source_account_id is None:
            raise ValueError("sourceAccountId must not be null")
        if self.target_account_id is None:
            raise ValueError("targetAccountId must not be null")
        if self.money is None:
            raise ValueError("money must not be null")

        # 송금액 > 0 검증
        if not self.money.is_positive():
            raise ValueError("money must be greater than 0")
```

**SelfValidating 추상 클래스 구현**:

```java
// Java 코드 (Line 328-359)
package shared;

public abstract class SelfValidating<T> {

    private Validator validator;  // Bean Validation의 Validator

    public SelfValidating(){
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    protected void validateSelf() {
        // Bean Validation 실행
        Set<ConstraintViolation<T>> violations = validator.validate((T) this);
        if (!violations.isEmpty()) {
            throw new ConstraintViolationException(violations);  // 검증 실패 시 예외 발생
        }
    }
}
```

```python
# Python 버전
from abc import ABC
from typing import TypeVar, Generic, Set

T = TypeVar('T')

class SelfValidating(ABC, Generic[T]):
    """자가 검증 추상 클래스"""

    def validate_self(self):
        """자가 검증 실행 (Python에서는 __post_init__에서 직접 검증)"""
        # Python에서는 dataclass의 __post_init__를 사용하거나
        # pydantic 같은 라이브러리 활용 가능
        pass
```

**핵심 포인트**:
- SendMoneyCommand의 모든 필드는 `final` (불변)
- 생성자에서 검증하므로, 객체가 생성되면 항상 유효한 상태 보장
- Bean Validation API로 선언적 검증 (`@NotNull`)
- Bean Validation이 표현 못하는 검증은 수동 구현 (`requireGreaterThan`)
- Input 모델이 Use Case 구현으로부터 **Anti-Corruption Layer** 역할 수행

[참조: Line 200-363] → [핵심: Input Validation vs Business Rule Validation 분리, Constructor 기반 불변성과 검증]

---

## 4. Constructor 활용 [Line 364-402] → [핵심: Constructor 기반 불변성과 검증]

### 이전 화제와의 관계
Input Validation에서 생성자를 사용했는데, Builder 패턴 대신 생성자를 직접 사용하는 이유를 설명한다.

### 화제: Constructor vs Builder 패턴

**Builder 패턴의 문제점**:
- 필드 추가/삭제 시 컴파일 에러가 발생하지 않음
- Builder 호출 코드에서 새 필드를 누락해도 컴파일 타임에 감지 못함
- 런타임(테스트)에서야 검증 로직이 오류를 발견

**Constructor 직접 사용의 장점**:
- 필드 추가/삭제 시 컴파일 에러로 모든 호출부를 추적 가능
- IDE가 파라미터 이름 힌트 제공으로 가독성 향상
- 불변 객체의 유효하지 않은 상태 생성을 컴파일 타임에 방지

**예시**:

```java
// Builder 패턴 (Line 378-386)
new SendMoneyCommandBuilder()
    .sourceAccountId(new AccountId(41L))
    .targetAccountId(new AccountId(42L))
    // ... 많은 필드 초기화
    .build();  // 새 필드 추가 시 누락해도 컴파일 에러 없음

// Constructor 직접 사용 (권장)
new SendMoneyCommand(
    new AccountId(41L),  // IDE가 파라미터 이름 힌트 표시
    new AccountId(42L),
    new Money(100));  // 새 필드 추가 시 컴파일 에러로 모든 호출부 수정 강제
```

```python
# Python 버전

# Builder 패턴 (권장하지 않음)
command = (SendMoneyCommandBuilder()
    .source_account_id(AccountId(41))
    .target_account_id(AccountId(42))
    # ... 많은 필드 초기화
    .build())  # 새 필드 추가 시 누락해도 런타임까지 에러 없음

# Constructor 직접 사용 (권장)
command = SendMoneyCommand(
    source_account_id=AccountId(41),  # 키워드 인자로 명확성 확보
    target_account_id=AccountId(42),
    money=Money(100))  # 새 필드 추가 시 호출부에서 누락하면 즉시 에러
```

**결론**: 긴 파라미터 리스트라도 생성자를 직접 사용하면 컴파일러가 안내해준다.

[참조: Line 364-402] → [핵심: Constructor 기반 불변성과 검증]

---

## 5. Use Case별 Input Model 분리 [Line 403-427] → [핵심: Use Case별 전용 Input/Output 모델]

### 이전 화제와의 관계
Constructor를 사용한 Input Model 구현 방법을 배웠으니, 이제 Input Model을 Use Case별로 분리하는 이유를 설명한다.

### 화제: 각 Use Case마다 전용 Input Model 사용

**공유 Input Model의 문제점**:
- "Register Account"와 "Update Account Details" Use Case를 생각해보자
- 둘 다 계좌 정보를 입력받지만, "Update"는 계좌 ID가 필요하고 "Register"는 소유자 ID가 필요
- 공유 모델을 사용하면 각 Use Case에 불필요한 필드에 `null` 허용 필요
- Validation 로직이 Use Case마다 달라져서 Use Case 코드에 검증 로직이 섞임
- "Register"에 계좌 ID가 전달되면 어떻게 처리할지 불명확 (에러? 무시?)

**전용 Input Model의 장점**:
- Use Case의 의도가 명확해짐
- Use Case 간 결합도 낮아짐 (한 Use Case의 변경이 다른 Use Case에 영향 없음)
- 원치 않는 부작용 방지

**단점과 대응**:
- 들어오는 데이터를 각 Use Case의 Input 모델로 매핑해야 함
- 매핑 전략은 8장 "Mapping Between Boundaries"에서 다룸

[참조: Line 403-427] → [핵심: Use Case별 전용 Input/Output 모델]

---

## 6. Business Rule Validation [Line 428-521] → [핵심: Input Validation vs Business Rule Validation 분리, Domain Model 구현 방식]

### 이전 화제와의 관계
Input Validation을 Input 모델에서 처리했으니, 이제 Business Rule Validation을 어디서 처리할지 설명한다.

### 화제: Input Validation vs Business Rule Validation

**구분 기준**:
- **Input Validation**: 도메인 모델 상태 접근 없이 검증 가능 (구문적 검증, Syntactical)
  - 예: "송금액 > 0", "계좌 ID가 null이 아님"
  - 선언적으로 구현 가능 (`@NotNull`)
- **Business Rule Validation**: 도메인 모델의 현재 상태에 접근이 필요 (의미적 검증, Semantical)
  - 예: "출금 계좌가 초과 인출되지 않음", "계좌가 존재함"
  - Use Case의 컨텍스트에서 검증

**Business Rule을 Domain Entity에 구현**:

```java
// Java 코드 (Line 457-477)
package buckpal.domain;

public class Account {

    // ...

    public boolean withdraw(Money money, AccountId targetAccountId) {
        if (!mayWithdraw(money)) {  // 비즈니스 규칙: 초과 인출 방지
            return false;
        }
        // ...
    }
}
```

```python
# Python 버전
class Account:

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        """출금: 비즈니스 규칙 검증 후 실행"""
        if not self._may_withdraw(money):  # 비즈니스 규칙: 초과 인출 방지
            return False
        # ...
```

**장점**: 비즈니스 규칙이 해당 규칙을 요구하는 비즈니스 로직 바로 옆에 위치하여 찾기 쉽고 이해하기 쉬움

**Business Rule을 Use Case에 구현**:

```java
// Java 코드 (Line 484-509)
package buckpal.application.service;

@RequiredArgsConstructor
@Transactional
public class SendMoneyService implements SendMoneyUseCase {

    // ...

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        requireAccountExists(command.getSourceAccountId());  // 비즈니스 규칙: 계좌 존재 여부
        requireAccountExists(command.getTargetAccountId());
        // ...
    }
}
```

```python
# Python 버전
class SendMoneyService:

    def send_money(self, command: SendMoneyCommand) -> bool:
        """송금 실행"""
        self._require_account_exists(command.source_account_id)  # 비즈니스 규칙: 계좌 존재 여부
        self._require_account_exists(command.target_account_id)
        # ...
```

**사용 시점**: 도메인 엔티티에 규칙을 넣기 어려운 경우 (예: 엔티티 로드 전에 검증 필요)

**처리 방법**: 검증 메서드를 호출하고, 실패 시 전용 예외를 던져 Adapter가 사용자에게 에러 메시지 표시

[참조: Line 428-521] → [핵심: Input Validation vs Business Rule Validation 분리, Domain Model 구현 방식]

---

## 7. Rich vs Anemic Domain Model [Line 522-547] → [핵심: Domain Model 구현 방식]

### 이전 화제와의 관계
Business Rule Validation을 Domain Entity 또는 Use Case에 구현할 수 있다고 했는데, 이는 Domain Model 스타일에 따라 달라진다.

### 화제: Rich Domain Model vs Anemic Domain Model

**Rich Domain Model (DDD 철학)**:
- 도메인 로직을 최대한 엔티티에 포함
- 엔티티는 상태 변경 메서드를 제공하고, 비즈니스 규칙에 따라 유효한 변경만 허용
- Use Case는 도메인 모델의 진입점 역할
  - 사용자 의도를 도메인 엔티티 메서드 호출로 변환
  - 대부분의 비즈니스 규칙은 엔티티에 위치
- **"Send Money" Use Case 예시**: 출발/도착 계좌를 로드 → `withdraw()`, `deposit()` 호출 → 데이터베이스에 저장

**Anemic Domain Model**:
- 엔티티는 매우 얇음 (상태와 getter/setter만 보유)
- 도메인 로직이 없음
- 도메인 로직은 Use Case 클래스에 구현
  - 비즈니스 규칙 검증, 엔티티 상태 변경, Outgoing Port를 통한 저장 모두 Use Case가 담당
  - "풍부함(richness)"이 엔티티가 아닌 Use Case에 있음

**결론**: 두 스타일 모두 Hexagonal Architecture에서 구현 가능. 필요에 맞는 스타일을 선택하면 됨.

[참조: Line 522-547] → [핵심: Domain Model 구현 방식]

---

## 8. Use Case별 Output Model 분리 [Line 548-575] → [핵심: Use Case별 전용 Input/Output 모델]

### 이전 화제와의 관계
Input Model을 Use Case별로 분리했듯이, Output Model도 Use Case별로 분리해야 한다.

### 화제: Use Case별 최소한의 Output 반환

**원칙**: Output은 호출자가 실제로 필요한 데이터만 포함해야 함

**"Send Money" Use Case 예시**:
- 반환값: `boolean` (성공 여부만 반환)
- 최소한이고 명확한 반환값

**안티패턴**: 전체 Account 엔티티를 반환
- "계좌의 새 잔액이 필요할 수도 있지 않을까?"
- 하지만 호출자가 정말 필요한가?
- 필요하다면 전용 Use Case를 만들어야 하지 않을까?

**질문을 던져야 함**:
- Use Case가 이 데이터를 반환해야 하는가?
- 호출자가 정말 필요한가?
- 전용 Use Case를 만들어야 하지 않는가?

**원칙**: 의심스러우면 최소한만 반환

**공유 Output Model의 문제점**:
- Use Case 간 결합도 증가
- 한 Use Case가 Output에 새 필드를 추가하면, 다른 Use Case도 처리해야 함 (불필요해도)
- 공유 모델은 시간이 지나면서 비대해짐
- **Single Responsibility Principle**: 모델을 분리하면 Use Case 간 결합도 낮아짐

**Domain Entity를 Output으로 사용하지 말 것**:
- Domain Entity가 변경되는 이유를 최소화해야 함
- 단, 11장 "Taking Shortcuts Consciously"에서 예외적인 경우 다룸

[참조: Line 548-575] → [핵심: Use Case별 전용 Input/Output 모델]

---

## 9. Read-Only Use Cases [Line 576-625] → [핵심: Query Service 패턴]

### 이전 화제와의 관계
지금까지 상태를 변경하는 Use Case를 다뤘는데, 이제 읽기 전용 Use Case를 어떻게 구현할지 설명한다.

### 화제: Query Service로 읽기 전용 작업 구현

**예시**: UI가 계좌 잔액을 표시해야 함

**질문**: 전용 Use Case를 만들어야 하는가?

**답변**:
- UI 관점에서는 "View Account Balance" Use Case
- Application Core 관점에서는 단순 데이터 조회 (Query)
- 프로젝트 컨텍스트에서 Use Case로 간주되면 Use Case로 구현
- 그렇지 않으면 Query로 구분

**Query Service 구현**:

```java
// Java 코드 (Line 595-616)
package buckpal.application.service;

@RequiredArgsConstructor
class GetAccountBalanceService implements GetAccountBalanceQuery {

    private final LoadAccountPort loadAccountPort;  // Outgoing Port: 계좌 로드

    @Override
    public Money getAccountBalance(AccountId accountId) {
        return loadAccountPort.loadAccount(accountId, LocalDateTime.now())
            .calculateBalance();  // 계좌 로드 후 잔액 계산하여 반환
    }
}
```

```python
# Python 버전
class GetAccountBalanceService:
    """계좌 잔액 조회 Query Service"""

    def __init__(self, load_account_port: LoadAccountPort):
        self.load_account_port = load_account_port

    def get_account_balance(self, account_id: AccountId) -> Money:
        """계좌 잔액 조회"""
        account = self.load_account_port.load_account(
            account_id,
            datetime.now())
        return account.calculate_balance()  # 계좌 로드 후 잔액 계산하여 반환
```

**특징**:
- Use Case Service처럼 동작
- **Incoming Port** (GetAccountBalanceQuery) 구현
- **Outgoing Port** (LoadAccountPort) 호출하여 데이터 로드
- 코드베이스에서 읽기 전용 Query와 상태 변경 Command가 명확히 구분
- **CQS** (Command-Query Separation), **CQRS** (Command-Query Responsibility Segregation)와 잘 맞음

**단축키**: 서비스가 Query를 Outgoing Port로 전달만 한다면, 클라이언트가 Outgoing Port를 직접 호출하게 할 수도 있음 (11장 "Taking Shortcuts Consciously"에서 다룸)

[참조: Line 576-625] → [핵심: Query Service 패턴]

---

## 10. 유지보수성 향상 [Line 626-635] → [핵심: Use Case별 전용 Input/Output 모델]

### 이전 화제와의 관계
모든 구현 방법을 다뤘으니, 마지막으로 이러한 접근법이 유지보수성에 어떤 영향을 주는지 설명한다.

### 화제: Use Case별 모델 분리의 장점

**아키텍처의 이점**:
- 도메인 로직을 원하는 대로 구현 가능 (Rich/Anemic Domain Model 선택 자유)
- Use Case별 Input/Output 모델 분리로 원치 않는 부작용 방지

**비용**:
- 각 Use Case마다 별도 모델 필요
- 모델과 엔티티 간 매핑 작업 필요

**장점**:
1. **명확한 이해**: Use Case별 모델로 Use Case의 의도가 명확해짐
2. **장기 유지보수**: 명확함이 장기적으로 유지보수를 쉽게 만듦
3. **병렬 작업**: 여러 개발자가 서로 다른 Use Case를 동시에 작업 가능 (상호 간섭 없음)

**Input Validation과 결합**:
- 엄격한 입력 검증 + Use Case별 Input/Output 모델 = 유지보수 가능한 코드베이스

[참조: Line 626-635] → [핵심: Use Case별 전용 Input/Output 모델]
