# Chapter 4: Implementing a Use Case - 정보 추출

## 압축 내용
헥사고나 아키텍처에서 유스케이스를 구현하는 방법을 설명하며, 입력 검증은 커맨드 객체에서, 비즈니스 룰은 도메인 엔티티나 유스케이스에서 처리하고, 각 유스케이스마다 전용 입출력 모델을 사용하여 결합도를 낮추고 유지보수성을 높이는 방법을 제시한다.

## 핵심 내용
### 핵심 개념
1. Use Case 구현 단계
2. Input Validation (입력 검증)
3. Business Rule Validation (비즈니스 룰 검증)
4. Domain Entity (도메인 엔티티)
5. Input/Output Model (입출력 모델)

### 핵심 개념 설명

**1. Use Case 구현 단계** (참조: 페이지 34, 라인 131-136)
- 유스케이스는 4단계로 구성: (1) 입력 받기, (2) 비즈니스 룰 검증, (3) 모델 상태 조작, (4) 출력 반환
- 입력 검증은 유스케이스 외부에서 처리하고, 비즈니스 룰 검증은 유스케이스 책임

**2. Input Validation (입력 검증)** (참조: 페이지 36-37, 라인 200-268)
- 입력 검증은 유스케이스가 아닌 입력 모델(Command 객체)의 생성자에서 처리
- 불변(immutable) 객체로 만들어 유효성이 보장된 상태만 존재하도록 함
- Bean Validation API를 활용하여 선언적 검증 가능

**3. Business Rule Validation (비즈니스 룰 검증)** (참조: 페이지 40-42, 라인 429-521)
- 비즈니스 룰은 도메인 모델의 현재 상태에 접근이 필요한 검증
- 도메인 엔티티 내부에 구현하는 것이 최선 (예: 출금 시 잔액 초과 방지)
- 엔티티에 구현이 어려운 경우 유스케이스 코드에서 직접 검증

**4. Domain Entity (도메인 엔티티)** (참조: 페이지 32-34, 라인 13-128)
- Account 엔티티는 계좌의 현재 스냅샷을 표현
- ActivityWindow로 최근 활동만 메모리에 로드하고, baselineBalance로 전체 잔액 계산
- withdraw()와 deposit() 메서드로 비즈니스 로직 캡슐화

**5. Input/Output Model (입출력 모델)** (참조: 페이지 40, 라인 403-427 & 페이지 43, 라인 548-571)
- 각 유스케이스마다 전용 입출력 모델을 사용하여 결합도 감소
- 호출자가 실제로 필요한 데이터만 반환 (최소한의 출력)
- 도메인 엔티티를 입출력 모델로 직접 사용하지 않는 것이 권장됨

### 핵심 개념 간 관계
- **Use Case 구현 단계**는 **Input Validation**과 **Business Rule Validation**을 명확히 구분
- **Input Validation**은 **Input Model (Command)**에서 처리하여 유스케이스 코드를 깨끗하게 유지
- **Business Rule Validation**은 **Domain Entity** 또는 유스케이스에서 처리
- **Domain Entity**는 비즈니스 로직을 캡슐화하며, **Use Case**는 이를 조율(orchestrate)
- **Input/Output Model**은 유스케이스 간 결합도를 낮추고 단일 책임 원칙(SRP)을 지원

## 상세 핵심 내용
### 중요 개념
1. Use Case 구현 단계
2. Input Validation (입력 검증)
3. Business Rule Validation (비즈니스 룰 검증)
4. Domain Entity (도메인 엔티티)
5. Input/Output Model (입출력 모델)
6. Anti-Corruption Layer (부패 방지 층)
7. Constructor Validation (생성자 검증)
8. Rich vs Anemic Domain Model
9. Query Service (쿼리 서비스)
10. Single Responsibility Principle (SRP)

### 중요 개념 설명

**1. Use Case 구현 단계** (참조: 페이지 34, 라인 131-149)
- 4단계: (1) Take input, (2) Validate business rules, (3) Manipulate model state, (4) Return output
- 입력 검증은 도메인 로직이 아니므로 유스케이스 외부에서 처리
- 비즈니스 룰 검증은 도메인 엔티티와 유스케이스가 공유
- 모델 상태 조작 후 persistence adapter를 통해 저장
- 반환값은 outgoing adapter의 응답을 출력 객체로 변환

**2. Input Validation (입력 검증)** (참조: 페이지 36-38, 라인 200-363)
- 어댑터가 아닌 애플리케이션 레이어에서 처리 (여러 어댑터가 호출 가능하므로)
- 입력 모델(SendMoneyCommand)의 생성자에서 검증
- null 체크, 값 범위 체크 등 syntactical validation
- Bean Validation API (@NotNull 등)를 활용하여 선언적 검증
- 유효하지 않으면 생성자에서 예외 발생

**3. Business Rule Validation (비즈니스 룰 검증)** (참조: 페이지 40-42, 라인 429-521)
- 도메인 모델의 현재 상태에 접근이 필요한 검증 (semantical validation)
- 예: "출금 계좌는 초과 인출되면 안 됨" → 현재 잔액 확인 필요
- 입력 검증 예: "송금액은 0보다 커야 함" → 모델 상태 불필요
- 도메인 엔티티 내부에 구현하는 것이 최선 (비즈니스 로직과 함께 위치)
- 엔티티에 불가능한 경우 유스케이스에서 검증 (예: 계좌 존재 여부)

**4. Domain Entity (도메인 엔티티)** (참조: 페이지 32-34, 라인 13-128)
- Account는 계좌의 현재 스냅샷, Activity는 각 거래 기록
- ActivityWindow: 최근 며칠/몇 주간의 활동만 메모리에 로드
- baselineBalance: 활동 창 이전의 잔액 (전체 잔액 = baseline + 활동 창 잔액)
- withdraw()와 deposit()로 출금/입금 비즈니스 로직 캡슐화
- 비즈니스 룰 검증 포함 (mayWithdraw()로 초과 인출 방지)

**5. Input/Output Model (입출력 모델)** (참조: 페이지 40 & 43, 라인 403-427, 548-571)
- 각 유스케이스마다 전용 입출력 모델 사용
- 예: "Register Account"와 "Update Account Details"는 다른 입력 모델 필요
- 공유 모델은 null 허용, 복잡한 검증, 원치 않는 부작용 발생
- 출력도 호출자가 실제 필요한 최소한의 데이터만 반환 (boolean, 특정 필드만)
- 도메인 엔티티를 직접 반환하면 변경 이유가 늘어남 (SRP 위반)

**6. Anti-Corruption Layer (부패 방지 층)** (참조: 페이지 38, 라인 360-363)
- 입력 모델의 검증 로직이 유스케이스 주변에 보호막 역할
- 잘못된 입력을 호출자에게 반환하여 유스케이스 내부를 보호
- 레이어드 아키텍처의 레이어가 아닌, 유스케이스 주변의 얇은 보호 스크린

**7. Constructor Validation (생성자 검증)** (참조: 페이지 38-40, 라인 364-402)
- 불변 객체의 생성자에 모든 검증 로직 집중
- Builder 패턴보다 생성자 직접 사용을 권장 (컴파일러의 도움 받기 위해)
- 필드 추가/제거 시 컴파일 에러로 모든 호출 코드를 추적 가능
- Builder는 필드 누락 시 컴파일 에러 없이 런타임 에러 발생 가능
- IDE의 파라미터 힌트로 긴 파라미터 리스트도 관리 가능

**8. Rich vs Anemic Domain Model** (참조: 페이지 42-43, 라인 522-547)
- **Rich Domain Model (DDD)**: 도메인 로직을 엔티티 내부에 최대한 구현, 상태 변경은 엔티티 메서드를 통해서만, 유스케이스는 엔티티 메서드 조율(orchestrate)
- **Anemic Domain Model**: 엔티티는 필드와 getter/setter만, 도메인 로직은 유스케이스에 구현
- 두 스타일 모두 헥사고나 아키텍처와 호환 가능
- 프로젝트 상황에 맞게 선택

**9. Query Service (쿼리 서비스)** (참조: 페이지 43-44, 라인 576-625)
- 읽기 전용 작업(예: 계좌 잔액 조회)은 유스케이스가 아닌 쿼리로 구분
- GetAccountBalanceQuery 포트를 구현하는 쿼리 서비스 생성
- CQS(Command-Query Separation), CQRS와 잘 어울림
- 쿼리가 단순히 데이터를 전달만 하면 outgoing port를 직접 호출하는 단축 가능

**10. Single Responsibility Principle (SRP)** (참조: 페이지 43, 라인 570-571)
- 각 유스케이스마다 전용 입출력 모델 사용 → SRP 준수
- 공유 모델은 여러 유스케이스의 변경 이유로 인해 비대해짐 (tumor)
- 모델 분리로 유스케이스 간 결합도 감소, 독립적 개발 가능

### 중요 개념 간 관계
- **Use Case 구현 단계**는 **Input Validation**, **Business Rule Validation**, **Domain Entity** 조작, **Output Model** 반환을 포함
- **Input Validation**은 **Anti-Corruption Layer** 역할을 하며, **Constructor Validation**을 통해 구현
- **Business Rule Validation**은 **Domain Entity** (Rich Model) 또는 유스케이스 (Anemic Model)에서 처리
- **Rich vs Anemic Domain Model** 선택은 비즈니스 로직의 위치를 결정
- **Input/Output Model**은 **SRP**를 지원하고 유스케이스 간 결합도 감소
- **Query Service**는 상태 변경 없는 읽기 작업을 유스케이스와 분리 (CQS/CQRS)

## 상세 내용

### 1. 도메인 모델 구현 (Implementing the Domain Model)
(참조: 페이지 32-34, 라인 12-128)

한 계좌에서 다른 계좌로 송금하는 유스케이스를 구현하기 위해, 객체 지향 방식으로 Account 엔티티를 모델링한다. 출금(withdraw)과 입금(deposit)을 허용하는 Account 엔티티를 생성하여, 송신 계좌에서 돈을 빼고 수신 계좌에 넣는다.

```java
// Java 버전
package buckpal.domain;

public class Account {

    private AccountId id;
    private Money baselineBalance;  // 활동 창 이전의 잔액
    private ActivityWindow activityWindow;  // 최근 활동 창

    // constructors and getters omitted

    // 현재 잔액 계산: 베이스라인 + 활동 창의 잔액
    public Money calculateBalance() {
        return Money.add(
            this.baselineBalance,
            this.activityWindow.calculateBalance(this.id));
    }

    // 출금 메서드: 비즈니스 룰 검증 포함
    public boolean withdraw(Money money, AccountId targetAccountId) {

        // 출금 가능 여부 확인 (비즈니스 룰)
        if (!mayWithdraw(money)) {
            return false;
        }

        // 출금 활동 생성
        Activity withdrawal = new Activity(
            this.id,  // 활동 소유 계좌
            this.id,  // 출금 계좌 (source)
            targetAccountId,  // 입금 계좌 (target)
            LocalDateTime.now(),
            money);
        this.activityWindow.addActivity(withdrawal);
        return true;
    }

    // 출금 가능 여부 검증 (비즈니스 룰)
    private boolean mayWithdraw(Money money) {
        return Money.add(
            this.calculateBalance(),
            money.negate())  // 음수로 변환
            .isPositive();  // 결과가 양수인지 확인 (초과 인출 방지)
    }

    // 입금 메서드
    public boolean deposit(Money money, AccountId sourceAccountId) {
        Activity deposit = new Activity(
            this.id,  // 활동 소유 계좌
            sourceAccountId,  // 출금 계좌 (source)
            this.id,  // 입금 계좌 (target)
            LocalDateTime.now(),
            money);
        this.activityWindow.addActivity(deposit);
        return true;
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AccountId:
    value: int

@dataclass
class Money:
    amount: int

    def add(self, other: 'Money') -> 'Money':
        return Money(self.amount + other.amount)

    def negate(self) -> 'Money':
        return Money(-self.amount)

    def is_positive(self) -> bool:
        return self.amount > 0

@dataclass
class Activity:
    """거래 활동 엔티티"""
    owner_account_id: AccountId
    source_account_id: AccountId
    target_account_id: AccountId
    timestamp: datetime
    money: Money

class ActivityWindow:
    """최근 활동 창"""
    def __init__(self):
        self.activities: list[Activity] = []

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)

    def calculate_balance(self, account_id: AccountId) -> Money:
        """활동 창 내 잔액 계산"""
        balance = 0
        for activity in self.activities:
            if activity.target_account_id == account_id:
                balance += activity.money.amount
            if activity.source_account_id == account_id:
                balance -= activity.money.amount
        return Money(balance)

class Account:
    """계좌 엔티티"""

    def __init__(
        self,
        id: AccountId,
        baseline_balance: Money,
        activity_window: ActivityWindow
    ):
        self.id = id
        self.baseline_balance = baseline_balance  # 활동 창 이전 잔액
        self.activity_window = activity_window  # 최근 활동 창

    def calculate_balance(self) -> Money:
        """현재 잔액 계산: 베이스라인 + 활동 창의 잔액"""
        return self.baseline_balance.add(
            self.activity_window.calculate_balance(self.id)
        )

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        """출금 메서드: 비즈니스 룰 검증 포함"""

        # 출금 가능 여부 확인 (비즈니스 룰)
        if not self._may_withdraw(money):
            return False

        # 출금 활동 생성
        withdrawal = Activity(
            owner_account_id=self.id,
            source_account_id=self.id,
            target_account_id=target_account_id,
            timestamp=datetime.now(),
            money=money
        )
        self.activity_window.add_activity(withdrawal)
        return True

    def _may_withdraw(self, money: Money) -> bool:
        """출금 가능 여부 검증 (비즈니스 룰)"""
        # 현재 잔액 - 출금액이 양수인지 확인 (초과 인출 방지)
        return self.calculate_balance().add(money.negate()).is_positive()

    def deposit(self, money: Money, source_account_id: AccountId) -> bool:
        """입금 메서드"""
        deposit = Activity(
            owner_account_id=self.id,
            source_account_id=source_account_id,
            target_account_id=self.id,
            timestamp=datetime.now(),
            money=money
        )
        self.activity_window.add_activity(deposit)
        return True
```

**설명:**
- Account 엔티티는 실제 계좌의 현재 스냅샷을 제공한다.
- 모든 출금과 입금은 Activity 엔티티로 기록된다.
- 모든 활동을 메모리에 로드하는 것은 비효율적이므로, Account는 최근 며칠/몇 주간의 활동만 ActivityWindow에 보관한다.
- 현재 잔액 계산을 위해 baselineBalance 속성을 추가로 가지며, 이는 활동 창의 첫 활동 직전의 잔액을 나타낸다.
- 총 잔액 = baseline balance + 활동 창의 모든 활동 잔액

---

### 2. 유스케이스 개요 (A Use Case in a Nutshell)
(참조: 페이지 34-35, 라인 130-196)

유스케이스는 일반적으로 다음 단계를 따른다:

1. **입력 받기 (Take input)**: incoming adapter로부터 입력 수신
2. **비즈니스 룰 검증 (Validate business rules)**: 도메인 로직 검증
3. **모델 상태 조작 (Manipulate model state)**: 도메인 객체의 상태 변경
4. **출력 반환 (Return output)**: 결과를 출력 객체로 변환하여 반환

입력 검증(input validation)은 유스케이스의 책임이 아니므로 다른 곳에서 처리한다. 유스케이스는 비즈니스 룰 검증에 책임이 있으며, 이는 도메인 엔티티와 공유한다.

비즈니스 룰이 만족되면, 입력을 기반으로 모델의 상태를 조작한다. 일반적으로 도메인 객체의 상태를 변경하고, persistence adapter가 구현한 포트를 통해 새 상태를 저장한다.

마지막 단계는 outgoing adapter의 반환값을 출력 객체로 변환하여 호출한 어댑터에 반환한다.

```java
// Java 버전
package buckpal.application.service;

@RequiredArgsConstructor
@Transactional
public class SendMoneyService implements SendMoneyUseCase {

    // outgoing ports
    private final LoadAccountPort loadAccountPort;
    private final AccountLock accountLock;
    private final UpdateAccountStatePort updateAccountStatePort;

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        // TODO: validate business rules
        // TODO: manipulate model state
        // TODO: return output
    }
}
```

```python
# Python 버전
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Incoming port (use case interface)
class SendMoneyUseCase(ABC):
    @abstractmethod
    def send_money(self, command: 'SendMoneyCommand') -> bool:
        pass

# Outgoing ports
class LoadAccountPort(ABC):
    @abstractmethod
    def load_account(self, account_id: AccountId, timestamp: datetime) -> Account:
        pass

class UpdateAccountStatePort(ABC):
    @abstractmethod
    def update_account(self, account: Account) -> None:
        pass

class AccountLock(ABC):
    @abstractmethod
    def lock(self, account_id: AccountId) -> None:
        pass

    @abstractmethod
    def unlock(self, account_id: AccountId) -> None:
        pass

# Use case implementation (service)
class SendMoneyService(SendMoneyUseCase):
    """송금 유스케이스 서비스"""

    def __init__(
        self,
        load_account_port: LoadAccountPort,
        account_lock: AccountLock,
        update_account_state_port: UpdateAccountStatePort
    ):
        self.load_account_port = load_account_port
        self.account_lock = account_lock
        self.update_account_state_port = update_account_state_port

    def send_money(self, command: 'SendMoneyCommand') -> bool:
        # TODO: validate business rules
        # TODO: manipulate model state
        # TODO: return output
        pass
```

**설명:**
- 서비스는 incoming port 인터페이스 SendMoneyUseCase를 구현한다.
- outgoing port 인터페이스 LoadAccountPort를 호출하여 계좌를 로드한다.
- UpdateAccountStatePort를 통해 업데이트된 계좌 상태를 데이터베이스에 저장한다.
- 각 유스케이스마다 별도의 서비스 클래스를 만들어 broad service 문제를 방지한다.

---

### 3. 입력 검증 (Validating Input)
(참조: 페이지 36-38, 라인 200-363)

입력 검증은 유스케이스 클래스의 책임은 아니지만, 애플리케이션 레이어에 속한다. 호출하는 어댑터가 검증하도록 하면, 모든 어댑터가 제대로 검증하리라 신뢰할 수 없고, 여러 어댑터가 호출할 수 있으므로 각각 구현해야 한다.

애플리케이션 레이어는 입력 검증을 담당해야 한다. 그렇지 않으면 외부에서 유효하지 않은 입력이 들어와 모델 상태를 손상시킬 수 있다.

유스케이스 클래스가 아니라면 어디에? **입력 모델(input model)**이 담당한다. SendMoneyCommand의 생성자에서 검증을 수행한다.

```java
// Java 버전 (수동 검증)
package buckpal.application.port.in;

@Getter
public class SendMoneyCommand {

    private final AccountId sourceAccountId;
    private final AccountId targetAccountId;
    private final Money money;

    public SendMoneyCommand(
        AccountId sourceAccountId,
        AccountId targetAccountId,
        Money money) {
        this.sourceAccountId = sourceAccountId;
        this.targetAccountId = targetAccountId;
        this.money = money;
        requireNonNull(sourceAccountId);  // null 체크
        requireNonNull(targetAccountId);
        requireNonNull(money);
        requireGreaterThan(money, 0);  // 양수 체크
    }
}
```

```python
# Python 버전 (수동 검증)
from dataclasses import dataclass

@dataclass(frozen=True)  # frozen=True로 불변성 보장
class SendMoneyCommand:
    """송금 커맨드 (입력 모델)"""
    source_account_id: AccountId
    target_account_id: AccountId
    money: Money

    def __post_init__(self):
        """생성 후 검증"""
        if self.source_account_id is None:
            raise ValueError("sourceAccountId must not be null")
        if self.target_account_id is None:
            raise ValueError("targetAccountId must not be null")
        if self.money is None:
            raise ValueError("money must not be null")
        if self.money.amount <= 0:
            raise ValueError("money must be greater than 0")
```

필드를 final(불변)로 만들어 객체를 불변(immutable)하게 만든다. 성공적으로 생성되면, 상태가 유효하며 유효하지 않은 상태로 변경될 수 없음을 보장한다.

SendMoneyCommand는 유스케이스 API의 일부이므로 incoming port 패키지에 위치한다. 따라서 검증은 애플리케이션 코어 내부(헥사곤 내부)에 남지만 유스케이스 코드를 오염시키지 않는다.

**Bean Validation API 사용:**

```java
// Java 버전 (Bean Validation)
package buckpal.application.port.in;

@Getter
public class SendMoneyCommand extends SelfValidating<SendMoneyCommand> {

    @NotNull
    private final AccountId sourceAccountId;
    @NotNull
    private final AccountId targetAccountId;
    @NotNull
    private final Money money;

    public SendMoneyCommand(
        AccountId sourceAccountId,
        AccountId targetAccountId,
        Money money) {
        this.sourceAccountId = sourceAccountId;
        this.targetAccountId = targetAccountId;
        this.money = money;
        requireGreaterThan(money, 0);  // 수동 검증
        this.validateSelf();  // Bean Validation 실행
    }
}
```

```python
# Python 버전 (Pydantic 사용)
from pydantic import BaseModel, Field, field_validator

class SendMoneyCommand(BaseModel):
    """송금 커맨드 (Pydantic 검증 사용)"""
    source_account_id: AccountId = Field(..., description="출금 계좌 ID")
    target_account_id: AccountId = Field(..., description="입금 계좌 ID")
    money: Money = Field(..., description="송금액")

    @field_validator('money')
    @classmethod
    def validate_money_positive(cls, v: Money) -> Money:
        if v.amount <= 0:
            raise ValueError('money must be greater than 0')
        return v

    class Config:
        frozen = True  # 불변성
```

**SelfValidating 구현:**

```java
// Java 버전
package shared;

public abstract class SelfValidating<T> {

    private Validator validator;

    public SelfValidating(){
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    protected void validateSelf() {
        Set<ConstraintViolation<T>> violations = validator.validate((T) this);
        if (!violations.isEmpty()) {
            throw new ConstraintViolationException(violations);
        }
    }
}
```

```python
# Python 버전 (Pydantic은 자동 검증 제공)
# Pydantic BaseModel은 자동으로 검증을 수행하므로
# SelfValidating 패턴이 별도로 필요하지 않음

# 만약 수동 검증 베이스 클래스가 필요하다면:
from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')

class SelfValidating(ABC, Generic[T]):
    """자체 검증 베이스 클래스"""

    def validate_self(self) -> None:
        """검증 로직을 서브클래스에서 구현"""
        pass
```

입력 모델에 검증을 위치시킴으로써, 유스케이스 구현 주변에 **부패 방지 층(anti-corruption layer)**을 효과적으로 생성했다. 이는 레이어드 아키텍처의 레이어가 아니라, 유스케이스 주변의 얇은 보호 스크린으로 잘못된 입력을 호출자에게 반환한다.

---

### 4. 생성자의 힘 (The Power of Constructors)
(참조: 페이지 38-40, 라인 364-402)

입력 모델 SendMoneyCommand는 생성자에 많은 책임을 부여한다. 클래스가 불변이므로, 생성자의 인수 목록은 각 속성마다 파라미터를 포함한다. 생성자가 파라미터를 검증하므로, 유효하지 않은 상태의 객체를 생성할 수 없다.

파라미터가 더 많다면? Builder 패턴을 사용하면 더 편리하지 않을까?

```java
// Java 버전 (Builder 패턴 예시)
new SendMoneyCommandBuilder()
    .sourceAccountId(new AccountId(41L))
    .targetAccountId(new AccountId(42L))
    // ... 많은 필드 초기화
    .build();
```

```python
# Python 버전 (Builder 패턴 예시)
SendMoneyCommandBuilder() \
    .source_account_id(AccountId(41)) \
    .target_account_id(AccountId(42)) \
    .build()
```

하지만 새 필드를 추가할 때 문제가 발생한다. 필드를 생성자와 빌더에 추가했지만, 동료나 전화, 이메일로 인해 작업이 중단되고, 빌더를 호출하는 코드에 새 필드를 추가하는 것을 잊어버릴 수 있다.

**컴파일러는 경고를 주지 않는다!** 런타임(유닛 테스트에서)에 검증 로직이 작동하여 에러를 던진다.

생성자를 직접 사용하면, 새 필드가 추가되거나 제거될 때마다 컴파일 에러를 따라가며 코드베이스 전체에 변경을 반영할 수 있다.

긴 파라미터 리스트도 IDE의 파라미터 이름 힌트로 잘 포맷될 수 있다.

**결론: 컴파일러가 우리를 가이드하도록 하자.**

---

### 5. 다른 유스케이스는 다른 입력 모델 (Different Input Models for Different Use Cases)
(참조: 페이지 40, 라인 403-427)

여러 유스케이스에 같은 입력 모델을 사용하고 싶은 유혹이 있다. "Register Account"와 "Update Account Details" 유스케이스를 고려하자. 둘 다 초기에는 거의 같은 입력(계좌 설명 등)이 필요하다.

차이점:
- "Update Account Details"는 업데이트할 계좌의 ID가 필요
- "Register Account"는 소유자의 ID가 필요 (계좌를 할당하기 위해)

같은 입력 모델을 공유하면, "Update Account Details"에 null 계좌 ID를, "Register Account"에 null 소유자 ID를 허용해야 한다.

불변 커맨드 객체의 필드에 null을 허용하는 것은 코드 스멜이다. 더 중요한 것은, 입력 검증을 어떻게 처리할까? 각 유스케이스마다 다른 검증이 필요하므로, 유스케이스 자체에 커스텀 검증 로직을 넣어야 하고, 이는 비즈니스 코드를 입력 검증 관심사로 오염시킨다.

또한, "Register Account" 유스케이스에서 계좌 ID 필드가 실수로 non-null 값을 가지면? 에러를 던질까? 무시할까? 유지보수 엔지니어(미래의 우리 포함)가 코드를 볼 때 묻게 될 질문들이다.

**각 유스케이스마다 전용 입력 모델**을 사용하면 유스케이스가 훨씬 명확해지고, 다른 유스케이스와 분리되어 원치 않는 부작용을 방지한다. 하지만 비용이 있다: 들어오는 데이터를 다른 유스케이스의 다른 입력 모델로 매핑해야 한다. 이 매핑 전략은 8장 "Mapping Between Boundaries"에서 논의한다.

---

### 6. 비즈니스 룰 검증 (Validating Business Rules)
(참조: 페이지 40-42, 라인 428-521)

입력 검증은 유스케이스 로직의 일부가 아니지만, **비즈니스 룰 검증은 확실히 유스케이스의 일부**다. 비즈니스 룰은 애플리케이션의 핵심이며 적절한 주의를 기울여야 한다.

**입력 검증 vs 비즈니스 룰의 구분:**
- **비즈니스 룰 검증**: 도메인 모델의 **현재 상태에 접근**이 필요
- **입력 검증**: 현재 상태 접근 불필요, 선언적으로 구현 가능 (@NotNull 등)

또 다른 표현:
- **입력 검증**: syntactical validation (구문적 검증)
- **비즈니스 룰**: semantical validation (의미적 검증, 유스케이스 맥락에서)

예시:
- **비즈니스 룰**: "출금 계좌는 초과 인출되면 안 됨" → 현재 모델 상태(잔액) 확인 필요
- **입력 검증**: "송금액은 0보다 커야 함" → 모델 접근 불필요

이 구분은 코드베이스 내에서 특정 검증을 배치하고 나중에 쉽게 찾을 수 있도록 돕는다. 검증이 현재 모델 상태 접근이 필요한가?라는 질문에 답하면 된다.

**비즈니스 룰 구현 방법:**

1. **도메인 엔티티에 배치** (최선):

```java
// Java 버전
package buckpal.domain;

public class Account {

    // ...

    public boolean withdraw(Money money, AccountId targetAccountId) {
        // 비즈니스 룰 검증
        if (!mayWithdraw(money)) {
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
        """출금 메서드: 비즈니스 룰 검증 포함"""
        # 비즈니스 룰 검증
        if not self._may_withdraw(money):
            return False
        # ... 출금 처리
```

이 방법은 비즈니스 룰이 그것을 필요로 하는 비즈니스 로직 바로 옆에 위치하므로, 쉽게 찾고 이해할 수 있다.

2. **유스케이스 코드에서 검증** (도메인 엔티티에 불가능한 경우):

```java
// Java 버전
package buckpal.application.service;

@RequiredArgsConstructor
@Transactional
public class SendMoneyService implements SendMoneyUseCase {

    // ...

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        // 비즈니스 룰: 계좌 존재 여부 확인
        requireAccountExists(command.getSourceAccountId());
        requireAccountExists(command.getTargetAccountId());
        // ...
    }
}
```

```python
# Python 버전
class SendMoneyService(SendMoneyUseCase):

    def send_money(self, command: SendMoneyCommand) -> bool:
        # 비즈니스 룰: 계좌 존재 여부 확인
        self._require_account_exists(command.source_account_id)
        self._require_account_exists(command.target_account_id)
        # ...

    def _require_account_exists(self, account_id: AccountId) -> None:
        """계좌 존재 여부 검증"""
        if not self.load_account_port.account_exists(account_id):
            raise AccountNotFoundException(account_id)
```

검증을 수행하는 메서드를 호출하고, 검증 실패 시 전용 예외를 던진다. 사용자와 인터페이스하는 어댑터는 이 예외를 사용자에게 에러 메시지로 표시하거나 적절한 방식으로 처리할 수 있다.

위 예시에서, 검증은 단순히 출금/입금 계좌가 데이터베이스에 실제로 존재하는지 확인한다. 더 복잡한 비즈니스 룰은 데이터베이스에서 도메인 모델을 먼저 로드한 후 상태를 확인해야 할 수 있다. 어차피 도메인 모델을 로드해야 한다면, 비즈니스 룰을 도메인 엔티티 자체에 구현해야 한다.

---

### 7. Rich vs Anemic 도메인 모델 (Rich vs. Anemic Domain Model)
(참조: 페이지 42-43, 라인 522-547)

우리의 아키텍처 스타일은 도메인 모델을 어떻게 구현할지 열려 있다. 이는 축복(우리 맥락에 맞게 할 수 있음)이자 저주(가이드라인이 없음)다.

빈번한 논의: DDD 철학을 따르는 **rich domain model** vs **"anemic" domain model**

**Rich Domain Model:**
- 가능한 많은 도메인 로직을 애플리케이션 핵심의 엔티티 내부에 구현
- 엔티티는 상태를 변경하는 메서드를 제공하며, 비즈니스 룰에 따라 유효한 변경만 허용
- 위의 Account 엔티티가 이 방식을 따름

이 시나리오에서 유스케이스는?
- 유스케이스는 도메인 모델의 **진입점(entry point)** 역할
- 사용자의 의도를 표현하고, 이를 도메인 엔티티의 조율된(orchestrated) 메서드 호출로 변환
- 많은 비즈니스 룰이 유스케이스 구현이 아닌 엔티티에 위치

"Send Money" 유스케이스 서비스는 출금/입금 계좌 엔티티를 로드하고, withdraw()와 deposit() 메서드를 호출하고, 다시 데이터베이스로 보낸다.

**Anemic Domain Model:**
- 엔티티 자체는 매우 얇음
- 일반적으로 상태를 보유하는 필드와 getter/setter 메서드만 제공
- 도메인 로직을 포함하지 않음

이는 도메인 로직이 유스케이스 클래스에 구현됨을 의미한다. 유스케이스는 비즈니스 룰 검증, 엔티티 상태 변경, outgoing port로 전달하여 데이터베이스에 저장하는 책임을 진다. "richness"는 엔티티가 아닌 유스케이스에 포함된다.

**결론:**
두 스타일(및 기타 여러 스타일) 모두 이 책에서 논의하는 아키텍처 접근법으로 구현 가능하다. 필요에 맞는 것을 자유롭게 선택하라.

---

### 8. 다른 유스케이스는 다른 출력 모델 (Different Output Models for Different Use Cases)
(참조: 페이지 43, 라인 548-571)

유스케이스가 작업을 완료하면, 호출자에게 무엇을 반환해야 할까?

입력과 유사하게, **출력도 유스케이스에 가능한 한 구체적**이면 이점이 있다. 출력은 호출자가 실제로 필요한 데이터만 포함해야 한다.

위의 "Send Money" 유스케이스 예시 코드에서, 우리는 boolean을 반환한다. 이는 이 맥락에서 가능한 최소이자 가장 구체적인 값이다.

업데이트된 전체 Account 엔티티를 호출자에게 반환하고 싶을 수도 있다. 아마도 호출자가 계좌의 새 잔액에 관심이 있을까?

하지만 정말로 "Send Money" 유스케이스가 이 데이터를 반환하도록 하고 싶은가? 호출자가 정말 필요한가? 그렇다면, 다른 호출자가 사용할 수 있는 그 데이터에 접근하기 위한 전용 유스케이스를 만들어야 하지 않을까?

이 질문들에 정답은 없다. 하지만 유스케이스를 가능한 한 구체적으로 유지하기 위해 질문을 던져야 한다. **의심스러우면, 가능한 한 적게 반환하라.**

유스케이스 간 같은 출력 모델을 공유하는 것도 그 유스케이스들을 강하게 결합시키는 경향이 있다. 한 유스케이스가 출력 모델에 새 필드가 필요하면, 다른 유스케이스도 그 필드를 처리해야 하며, 그들에게는 무관할 수 있다. 공유 모델은 장기적으로 여러 이유로 종양처럼 비대해진다. 단일 책임 원칙(SRP)을 적용하고 모델을 분리하면 유스케이스 분리에 도움이 된다.

같은 이유로 도메인 엔티티를 출력 모델로 사용하려는 유혹에 저항할 수 있다. 도메인 엔티티가 필요 이상의 이유로 변경되는 것을 원하지 않는다. 하지만 엔티티를 입출력 모델로 사용하는 것에 대해서는 11장 "Taking Shortcuts Consciously"에서 더 다룬다.

---

### 9. 읽기 전용 유스케이스는? (What About Read-Only Use Cases?)
(참조: 페이지 43-44, 라인 576-625)

위에서는 모델의 상태를 수정하는 유스케이스를 구현하는 방법을 논의했다. 읽기 전용 작업은 어떻게 구현할까?

UI가 계좌의 잔액을 표시해야 한다고 가정하자. 이를 위한 특정 유스케이스 구현을 만들까?

이런 읽기 전용 작업을 유스케이스라고 부르는 것은 어색하다. 물론, UI에서 요청된 데이터는 우리가 "View Account Balance"라고 부를 수 있는 특정 유스케이스를 구현하기 위해 필요하다. 이것이 프로젝트 맥락에서 유스케이스로 간주된다면, 다른 것들처럼 구현해야 한다.

그러나 애플리케이션 코어의 관점에서, 이것은 단순한 **데이터에 대한 쿼리**다. 프로젝트 맥락에서 유스케이스로 간주되지 않는다면, 실제 유스케이스와 구분하기 위해 **쿼리로 구현**할 수 있다.

우리 아키텍처 스타일 내에서 이를 수행하는 한 가지 방법은 쿼리를 위한 전용 incoming port를 만들고, "query service"에서 구현하는 것이다:

```java
// Java 버전
package buckpal.application.service;

@RequiredArgsConstructor
class GetAccountBalanceService implements GetAccountBalanceQuery {

    private final LoadAccountPort loadAccountPort;

    @Override
    public Money getAccountBalance(AccountId accountId) {
        return loadAccountPort.loadAccount(accountId, LocalDateTime.now())
            .calculateBalance();
    }
}
```

```python
# Python 버전
from abc import ABC, abstractmethod

# Incoming port (query interface)
class GetAccountBalanceQuery(ABC):
    @abstractmethod
    def get_account_balance(self, account_id: AccountId) -> Money:
        pass

# Query service implementation
class GetAccountBalanceService(GetAccountBalanceQuery):
    """계좌 잔액 조회 쿼리 서비스"""

    def __init__(self, load_account_port: LoadAccountPort):
        self.load_account_port = load_account_port

    def get_account_balance(self, account_id: AccountId) -> Money:
        """계좌 잔액 조회"""
        account = self.load_account_port.load_account(
            account_id,
            datetime.now()
        )
        return account.calculate_balance()
```

쿼리 서비스는 유스케이스 서비스와 똑같이 작동한다. GetAccountBalanceQuery라는 incoming port를 구현하고, LoadAccountPort라는 outgoing port를 호출하여 데이터베이스에서 실제 데이터를 로드한다.

이 방식으로, 읽기 전용 쿼리는 코드베이스에서 수정하는 유스케이스(또는 "commands")와 명확히 구분된다. 이는 **CQS(Command-Query Separation)** 및 **CQRS(Command-Query Responsibility Segregation)** 개념과 잘 어울린다.

위 코드에서, 서비스는 쿼리를 outgoing port로 전달하는 것 외에는 실제 작업을 하지 않는다. 레이어 간 같은 모델을 사용한다면, 클라이언트가 outgoing port를 직접 호출하도록 하는 단축(shortcut)을 취할 수 있다. 이 단축에 대해서는 11장 "Taking Shortcuts Consciously"에서 다룬다.

---

### 10. 이것이 유지보수 가능한 소프트웨어를 만드는 데 어떻게 도움이 되는가? (How Does This Help Me Build Maintainable Software?)
(참조: 페이지 44, 라인 626-635)

우리의 아키텍처는 우리가 적합하다고 생각하는 대로 도메인 로직을 구현할 수 있게 하지만, **유스케이스의 입력과 출력을 독립적으로 모델링**하면 원치 않는 부작용을 피할 수 있다.

예, 유스케이스 간 모델을 공유하는 것보다 더 많은 작업이다. 각 유스케이스마다 별도의 모델을 도입하고, 이 모델과 엔티티 간 매핑을 해야 한다.

하지만 **유스케이스별 모델은 유스케이스에 대한 명확한 이해**를 가능하게 하여, 장기적으로 유지보수가 더 쉬워진다. 또한 여러 개발자가 서로의 발을 밟지 않고 다른 유스케이스를 병렬로 작업할 수 있다.

**엄격한 입력 검증**과 함께, 유스케이스별 입출력 모델은 유지보수 가능한 코드베이스로 가는 긴 길을 간다.
