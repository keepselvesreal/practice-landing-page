<!--
생성 시간: 2025-10-03 10:46:45 KST
핵심 내용: Hexagonal Architecture에서 Use Case 구현 방법
상세 내용:
    - Domain Model 구현 (17-112라인): Account 엔티티와 도메인 모델 설계
    - Use Case 단계 정의 (130-153라인): Use Case의 4단계 프로세스
    - SendMoneyService 구현 (158-189라인): Use Case 서비스 클래스 구조
    - Input Validation (200-363라인): 입력 검증 방법과 Bean Validation
    - Constructor의 중요성 (364-402라인): 불변성과 컴파일타임 안전성
    - 서로 다른 Input Model (403-427라인): Use Case별 전용 입력 모델
    - Business Rule Validation (428-521라인): 비즈니스 규칙 검증 방법
    - Rich vs Anemic Domain Model (522-547라인): 도메인 모델 스타일 비교
    - Output Model (548-575라인): Use Case별 출력 모델
    - Read-Only Use Cases (576-625라인): 조회 전용 Use Case 처리
    - 유지보수성 (626-635라인): 아키텍처의 장기적 이점
상태: active
참조: 없음
-->

# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter 4: Implementing a Use Case

## 1. 압축 내용

**Use Case 구현은 입력 검증(Input Validation), 비즈니스 규칙 검증(Business Rule Validation), 도메인 모델 상태 조작(Model State Manipulation), 출력 반환(Output Return)의 4단계로 이루어지며, 각 Use Case마다 전용 입력/출력 모델을 사용하여 결합도를 낮추고 유지보수성을 향상시킨다.**

---

## 2. 핵심 내용

### 핵심 개념

1. **Use Case의 4단계 프로세스**
2. **Input Validation vs Business Rule Validation**
3. **Use Case별 전용 Input/Output Model**
4. **Rich vs Anemic Domain Model**
5. **불변 객체(Immutable Object)와 생성자 검증**

### 각 핵심 개념 설명

#### 1. Use Case의 4단계 프로세스
- **Take Input**: 들어오는 어댑터로부터 입력 수신
- **Validate Business Rules**: 비즈니스 규칙 검증
- **Manipulate Model State**: 도메인 모델 상태 변경
- **Return Output**: 출력 반환

Use Case는 도메인 로직에 집중하며, 입력 검증은 별도의 레이어에서 처리한다.

#### 2. Input Validation vs Business Rule Validation
- **Input Validation**: 현재 도메인 모델 상태에 접근하지 않고 수행 가능 (구문적 검증, Syntactical Validation)
- **Business Rule Validation**: 현재 도메인 모델 상태에 접근 필요 (의미적 검증, Semantical Validation)

Input Validation은 Use Case 외부(Input Model)에서, Business Rule Validation은 Use Case 내부 또는 Domain Entity에서 처리한다.

#### 3. Use Case별 전용 Input/Output Model
각 Use Case는 전용 Input/Output 모델을 가져야 한다. 이를 통해:
- Use Case 간 결합도 감소
- 명확한 Use Case 이해
- 의도하지 않은 부작용 방지
- 병렬 개발 가능

#### 4. Rich vs Anemic Domain Model
- **Rich Domain Model**: 도메인 로직을 엔티티 내부에 구현. Use Case는 엔티티 메서드 호출을 오케스트레이션
- **Anemic Domain Model**: 엔티티는 상태만 보유. Use Case가 도메인 로직 구현

둘 다 Hexagonal Architecture에서 구현 가능하며, 컨텍스트에 맞게 선택한다.

#### 5. 불변 객체와 생성자 검증
- 불변 필드(final)를 사용하여 객체 생성 후 상태 변경 방지
- 생성자에서 검증을 수행하여 유효하지 않은 객체 생성 차단
- Builder 패턴보다 긴 생성자가 컴파일타임 안전성 제공

### 핵심 개념 간 관계

Use Case의 4단계 프로세스는 Input Validation과 Business Rule Validation을 명확히 분리한다. Input Validation은 Use Case별 전용 Input Model에서 불변 객체와 생성자 검증을 통해 수행되며, Business Rule Validation은 Rich/Anemic Domain Model 선택에 따라 엔티티 또는 Use Case에서 수행된다. 최종적으로 Use Case별 전용 Output Model을 반환하여 결합도를 낮춘다.

---

## 3. 상세 내용

### 3.1 Domain Model 구현 (섹션: Implementing the Domain Model, 12-121라인)

**이전 화제와의 관계**: 이 장의 시작점으로, Use Case를 구현하기 위한 도메인 모델을 먼저 설계한다.

**📌 핵심 개념: Domain Entity 설계**

**다뤄지는 내용**:
- Account 엔티티 설계
- Activity와 ActivityWindow 개념
- Baseline Balance를 이용한 효율적 잔액 계산
- Withdraw/Deposit 비즈니스 로직

**Java 코드** (참조: 17-112라인):

```java
package buckpal.domain;

public class Account {
    private AccountId id;
    private Money baselineBalance;  // 활동 윈도우 시작 전 잔액
    private ActivityWindow activityWindow;  // 최근 활동 윈도우

    // constructors and getters omitted

    // 현재 잔액 계산: 기준선 잔액 + 활동 윈도우 내 활동들의 잔액
    public Money calculateBalance() {
        return Money.add(
            this.baselineBalance,
            this.activityWindow.calculateBalance(this.id));
    }

    // 출금 메서드: 비즈니스 규칙 검증 포함
    public boolean withdraw(Money money, AccountId targetAccountId) {
        if (!mayWithdraw(money)) {  // 출금 가능 여부 검증
            return false;
        }

        // 새로운 출금 활동 생성
        Activity withdrawal = new Activity(
            this.id,        // 계좌 ID
            this.id,        // 출처 계좌 ID
            targetAccountId,  // 대상 계좌 ID
            LocalDateTime.now(),
            money);
        this.activityWindow.addActivity(withdrawal);
        return true;
    }

    // 출금 가능 여부 검증: 잔액이 양수인지 확인
    private boolean mayWithdraw(Money money) {
        return Money.add(
            this.calculateBalance(),
            money.negate())  // 음수로 변환
            .isPositive();
    }

    // 입금 메서드
    public boolean deposit(Money money, AccountId sourceAccountId) {
        Activity deposit = new Activity(
            this.id,        // 계좌 ID
            sourceAccountId,  // 출처 계좌 ID
            this.id,        // 대상 계좌 ID
            LocalDateTime.now(),
            money);
        this.activityWindow.addActivity(deposit);
        return true;
    }
}
```

**Python 버전**:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Account:
    id: 'AccountId'
    baseline_balance: 'Money'  # 활동 윈도우 시작 전 잔액
    activity_window: 'ActivityWindow'  # 최근 활동 윈도우

    def calculate_balance(self) -> 'Money':
        """현재 잔액 계산: 기준선 잔액 + 활동 윈도우 내 활동들의 잔액"""
        return Money.add(
            self.baseline_balance,
            self.activity_window.calculate_balance(self.id)
        )

    def withdraw(self, money: 'Money', target_account_id: 'AccountId') -> bool:
        """출금 메서드: 비즈니스 규칙 검증 포함"""
        if not self._may_withdraw(money):  # 출금 가능 여부 검증
            return False

        # 새로운 출금 활동 생성
        withdrawal = Activity(
            account_id=self.id,
            source_account_id=self.id,
            target_account_id=target_account_id,
            timestamp=datetime.now(),
            money=money
        )
        self.activity_window.add_activity(withdrawal)
        return True

    def _may_withdraw(self, money: 'Money') -> bool:
        """출금 가능 여부 검증: 잔액이 양수인지 확인"""
        return Money.add(
            self.calculate_balance(),
            money.negate()  # 음수로 변환
        ).is_positive()

    def deposit(self, money: 'Money', source_account_id: 'AccountId') -> bool:
        """입금 메서드"""
        deposit = Activity(
            account_id=self.id,
            source_account_id=source_account_id,
            target_account_id=self.id,
            timestamp=datetime.now(),
            money=money
        )
        self.activity_window.add_activity(deposit)
        return True
```

**설명** (참조: 113-121라인):
- Account 엔티티는 실제 계좌의 현재 스냅샷을 제공
- 모든 활동을 메모리에 로드하는 것은 비효율적이므로 최근 며칠/주의 활동만 ActivityWindow에 저장
- baselineBalance는 ActivityWindow의 첫 활동 직전 계좌 잔액
- 총 잔액 = baselineBalance + ActivityWindow의 모든 활동 잔액

---

### 3.2 Use Case 단계 정의 (섹션: A Use Case in a Nutshell, 130-153라인)

**이전 화제와의 관계**: 도메인 모델을 정의한 후, 이를 활용하는 Use Case의 구조를 정의한다.

**📌 핵심 개념: Use Case의 4단계 프로세스**

**다뤄지는 내용** (참조: 131-148라인):
1. **Take Input**: 들어오는 어댑터로부터 입력 수신
2. **Validate Business Rules**: 비즈니스 규칙 검증 (도메인 엔티티와 책임 공유)
3. **Manipulate Model State**: 입력을 기반으로 모델 상태 조작
4. **Return Output**: 출력 객체로 변환하여 반환

**설명**:
- Input Validation은 Use Case 외부에서 수행 (도메인 로직 오염 방지)
- Business Rule Validation은 Use Case와 Domain Entity가 공유
- Use Case는 도메인 객체의 상태를 변경하고 Persistence Adapter에 전달
- 반환값은 Outgoing Adapter의 결과를 Output 객체로 변환

---

### 3.3 SendMoneyService 구현 (섹션: A Use Case in a Nutshell, 153-195라인)

**이전 화제와의 관계**: Use Case의 단계를 정의한 후, 실제 구현 예제를 제시한다.

**다뤄지는 내용**:
- 각 Use Case마다 별도의 서비스 클래스 생성 (Broad Service 문제 회피)
- Incoming Port 인터페이스 구현
- Outgoing Port 인터페이스 호출

**Java 코드** (참조: 158-189라인):

```java
package buckpal.application.service;

@RequiredArgsConstructor  // Lombok: final 필드에 대한 생성자 자동 생성
@Transactional  // 트랜잭션 관리
public class SendMoneyService implements SendMoneyUseCase {

    // Outgoing Ports
    private final LoadAccountPort loadAccountPort;  // 계좌 로드 포트
    private final AccountLock accountLock;  // 계좌 잠금
    private final UpdateAccountStatePort updateAccountStatePort;  // 계좌 상태 업데이트 포트

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        // TODO: validate business rules
        // TODO: manipulate model state
        // TODO: return output
    }
}
```

**Python 버전**:

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Incoming Port Interface
class SendMoneyUseCase(ABC):
    @abstractmethod
    def send_money(self, command: 'SendMoneyCommand') -> bool:
        pass

# Use Case Implementation
@dataclass
class SendMoneyService(SendMoneyUseCase):
    """송금 Use Case 서비스"""
    # Outgoing Ports
    load_account_port: 'LoadAccountPort'  # 계좌 로드 포트
    account_lock: 'AccountLock'  # 계좌 잠금
    update_account_state_port: 'UpdateAccountStatePort'  # 계좌 상태 업데이트 포트

    def send_money(self, command: 'SendMoneyCommand') -> bool:
        # TODO: validate business rules
        # TODO: manipulate model state
        # TODO: return output
        pass
```

**설명** (참조: 189-195라인):
- SendMoneyService는 Incoming Port인 SendMoneyUseCase 인터페이스 구현
- LoadAccountPort를 호출하여 계좌 로드
- UpdateAccountStatePort를 호출하여 업데이트된 계좌 상태를 DB에 저장
- Figure 11은 서비스, Use Case, 도메인 모델, Outgoing Port 간 관계를 보여줌

---

### 3.4 Input Validation (섹션: Validating Input, 200-363라인)

**이전 화제와의 관계**: Use Case 구현 구조를 정의한 후, 입력 검증 방법을 다룬다.

**📌 핵심 개념: Input Validation과 Anti-Corruption Layer**

**다뤄지는 내용**:
- Input Validation은 Application Layer의 책임
- Input Model(Command 객체)에서 검증 수행
- Bean Validation API를 활용한 선언적 검증
- SelfValidating 추상 클래스를 통한 검증 자동화

**Java 코드 - 수동 검증** (참조: 214-254라인):

```java
package buckpal.application.port.in;

@Getter
public class SendMoneyCommand {

    private final AccountId sourceAccountId;  // 출처 계좌 ID
    private final AccountId targetAccountId;  // 대상 계좌 ID
    private final Money money;  // 송금액

    public SendMoneyCommand(
        AccountId sourceAccountId,
        AccountId targetAccountId,
        Money money) {
        this.sourceAccountId = sourceAccountId;
        this.targetAccountId = targetAccountId;
        this.money = money;
        requireNonNull(sourceAccountId);  // null 검증
        requireNonNull(targetAccountId);  // null 검증
        requireNonNull(money);  // null 검증
        requireGreaterThan(money, 0);  // 양수 검증
    }
}
```

**Python 버전**:

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # 불변 객체
class SendMoneyCommand:
    """송금 커맨드 - Input Model"""
    source_account_id: 'AccountId'  # 출처 계좌 ID
    target_account_id: 'AccountId'  # 대상 계좌 ID
    money: 'Money'  # 송금액

    def __post_init__(self):
        """생성자 검증"""
        if self.source_account_id is None:
            raise ValueError("sourceAccountId must not be None")
        if self.target_account_id is None:
            raise ValueError("targetAccountId must not be None")
        if self.money is None:
            raise ValueError("money must not be None")
        if not self.money > 0:
            raise ValueError("money must be greater than 0")
```

**Java 코드 - Bean Validation** (참조: 273-315라인):

```java
package buckpal.application.port.in;

@Getter
public class SendMoneyCommand extends SelfValidating<SendMoneyCommand> {

    @NotNull  // Bean Validation 어노테이션
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
        requireGreaterThan(money, 0);  // Bean Validation으로 표현 불가한 검증
        this.validateSelf();  // 검증 실행
    }
}
```

**Python 버전 - Pydantic 사용**:

```python
from pydantic import BaseModel, Field, field_validator

class SendMoneyCommand(BaseModel):
    """송금 커맨드 - Bean Validation 스타일"""
    source_account_id: AccountId = Field(..., description="출처 계좌 ID")
    target_account_id: AccountId = Field(..., description="대상 계좌 ID")
    money: Money = Field(..., description="송금액")

    @field_validator('money')
    def money_must_be_positive(cls, v):
        """금액은 0보다 커야 함"""
        if not v > 0:
            raise ValueError('money must be greater than 0')
        return v

    class Config:
        frozen = True  # 불변 객체
```

**SelfValidating 구현** (참조: 327-359라인):

```java
package shared;

public abstract class SelfValidating<T> {

    private Validator validator;  // Bean Validation Validator

    public SelfValidating(){
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    protected void validateSelf() {
        Set<ConstraintViolation<T>> violations = validator.validate((T) this);
        if (!violations.isEmpty()) {
            throw new ConstraintViolationException(violations);  // 검증 실패 시 예외
        }
    }
}
```

**Python 버전**:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Set

T = TypeVar('T')

class SelfValidating(ABC, Generic[T]):
    """자체 검증 추상 클래스"""

    def __init__(self):
        self.validator = self._create_validator()

    def _create_validator(self):
        """Validator 생성 (Bean Validation 스타일)"""
        # Python에서는 Pydantic 등을 사용
        pass

    def validate_self(self):
        """자체 검증 실행"""
        violations = self.validator.validate(self)
        if violations:
            raise ConstraintViolationException(violations)
```

**설명** (참조: 360-363라인):
- Input Model에서 검증을 수행하여 Use Case 구현을 오염시키지 않음
- Anti-Corruption Layer 역할: 잘못된 입력을 호출자에게 되돌림
- Use Case는 유효한 입력만 받아 도메인 로직에 집중

---

### 3.5 Constructor의 중요성 (섹션: The Power of Constructors, 364-402라인)

**이전 화제와의 관계**: Input Validation을 생성자에서 수행하는 이유를 심화하여 설명한다.

**📌 핵심 개념: 불변성과 컴파일타임 안전성**

**다뤄지는 내용**:
- 불변 필드(final)를 사용한 객체 안전성
- Builder 패턴 vs 긴 생성자
- 컴파일타임 에러를 통한 안전성 확보

**Builder 패턴 예제** (참조: 377-386라인):

```java
new SendMoneyCommandBuilder()
    .sourceAccountId(new AccountId(41L))
    .targetAccountId(new AccountId(42L))
    // ... initialize many other fields
    .build();
```

**Python 버전**:

```python
SendMoneyCommandBuilder() \
    .source_account_id(AccountId(41)) \
    .target_account_id(AccountId(42)) \
    .build()  # 필드 누락 시 런타임 에러만 발생
```

**설명** (참조: 389-402라인):
- Builder 패턴은 편리하지만, 필드 추가 시 컴파일러가 누락을 감지하지 못함
- 생성자를 직접 사용하면 필드 추가/제거 시 컴파일 에러로 즉시 감지
- IDE의 파라미터 힌트 기능으로 긴 파라미터 리스트도 가독성 확보
- "컴파일러가 가이드하도록 하자"

---

### 3.6 서로 다른 Input Model (섹션: Different Input Models for Different Use Cases, 403-427라인)

**이전 화제와의 관계**: Input Model의 중요성을 강조한 후, Use Case별 전용 모델의 필요성을 설명한다.

**📌 핵심 개념: Use Case별 전용 Input Model**

**다뤄지는 내용**:
- Use Case 간 Input Model 공유의 문제점
- Null 허용으로 인한 검증 복잡성
- 전용 Input Model의 장점

**예제 시나리오** (참조: 404-423라인):
- "Register Account" Use Case: Owner ID 필요, Account ID 불필요
- "Update Account Details" Use Case: Account ID 필요, Owner ID 불필요
- 공유 모델 사용 시 각 필드에 null 허용 필요
- 검증 로직이 Use Case 내부로 침투

**설명** (참조: 424-427라인):
- 전용 Input Model은 Use Case를 명확하게 만듦
- Use Case 간 결합도 감소, 의도하지 않은 부작용 방지
- 단점: 들어오는 데이터를 서로 다른 Input Model로 매핑 필요
- 8장 "Mapping Between Boundaries"에서 매핑 전략 논의

---

### 3.7 Business Rule Validation (섹션: Validating Business Rules, 428-521라인)

**이전 화제와의 관계**: Input Validation과 대비하여 Business Rule Validation의 차이와 구현 방법을 설명한다.

**📌 핵심 개념: Input Validation vs Business Rule Validation**

**다뤄지는 내용**:
- Input Validation과 Business Rule의 구분
- 도메인 엔티티에서의 비즈니스 규칙 검증
- Use Case에서의 비즈니스 규칙 검증

**구분 기준** (참조: 432-448라인):
- **Input Validation**: 현재 도메인 모델 상태에 접근하지 않음 (구문적 검증)
- **Business Rule Validation**: 현재 도메인 모델 상태에 접근 필요 (의미적 검증)

**예제**:
- "출처 계좌가 초과 인출되면 안 된다" → Business Rule (계좌 상태 확인 필요)
- "송금액은 0보다 커야 한다" → Input Validation (상태 확인 불필요)

**도메인 엔티티에서 검증** (참조: 456-481라인):

```java
package buckpal.domain;

public class Account {
    // ...

    public boolean withdraw(Money money, AccountId targetAccountId) {
        if (!mayWithdraw(money)) {  // 비즈니스 규칙 검증
            return false;
        }
        // ...
    }
}
```

**Python 버전**:

```python
class Account:
    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        """출금 메서드"""
        if not self._may_withdraw(money):  # 비즈니스 규칙 검증
            return False
        # ...
```

**Use Case에서 검증** (참조: 483-513라인):

```java
package buckpal.application.service;

@RequiredArgsConstructor
@Transactional
public class SendMoneyService implements SendMoneyUseCase {
    // ...

    @Override
    public boolean sendMoney(SendMoneyCommand command) {
        requireAccountExists(command.getSourceAccountId());  // 계좌 존재 여부 검증
        requireAccountExists(command.getTargetAccountId());
        ...
    }
}
```

**Python 버전**:

```python
class SendMoneyService(SendMoneyUseCase):
    def send_money(self, command: SendMoneyCommand) -> bool:
        self._require_account_exists(command.source_account_id)  # 계좌 존재 여부 검증
        self._require_account_exists(command.target_account_id)
        # ...
```

**설명** (참조: 517-521라인):
- 계좌 존재 여부 검증은 DB 조회 필요
- 복잡한 비즈니스 규칙이 도메인 모델 로드를 요구할 경우, 도메인 엔티티에 구현
- "출처 계좌가 초과 인출되면 안 된다" 규칙은 Account 엔티티에 구현

---

### 3.8 Rich vs Anemic Domain Model (섹션: Rich vs. Anemic Domain Model, 522-547라인)

**이전 화제와의 관계**: Business Rule Validation의 위치가 도메인 모델 스타일에 따라 달라지므로, 두 가지 스타일을 비교한다.

**📌 핵심 개념: Rich vs Anemic Domain Model**

**다뤄지는 내용**:
- Rich Domain Model의 특징과 Use Case 역할
- Anemic Domain Model의 특징과 Use Case 역할
- 아키텍처 스타일과의 관계

**Rich Domain Model** (참조: 529-538라인):
- 도메인 로직을 엔티티 내부에 최대한 구현
- 엔티티는 비즈니스 규칙에 따라 유효한 상태 변경만 허용하는 메서드 제공
- Use Case는 사용자 의도를 도메인 엔티티 메서드 호출로 변환 (오케스트레이션)
- 비즈니스 규칙 대부분이 엔티티에 위치
- 예: Account 엔티티의 withdraw(), deposit() 메서드

**Anemic Domain Model** (참조: 539-545라인):
- 엔티티는 상태만 보유 (getter/setter만 제공)
- 엔티티에는 도메인 로직 없음
- Use Case가 비즈니스 규칙 검증, 상태 변경, Outgoing Port 호출 담당
- "풍부함(richness)"이 Use Case에 위치

**설명** (참조: 546-547라인):
- 두 스타일 모두 이 책의 아키텍처 접근법으로 구현 가능
- 컨텍스트에 맞는 스타일 선택

---

### 3.9 Output Model (섹션: Different Output Models for Different Use Cases, 548-575라인)

**이전 화제와의 관계**: Input Model과 마찬가지로 Output Model도 Use Case별로 전용화해야 함을 설명한다.

**다뤄지는 내용**:
- Use Case별 전용 Output Model의 필요성
- 최소한의 데이터 반환
- Domain Entity를 Output Model로 사용하지 않는 이유

**예제** (참조: 558-566라인):
- "Send Money" Use Case는 boolean 반환 (최소한이고 구체적)
- 전체 Account 객체 반환은 과도한 데이터 노출
- 새로운 잔액이 필요하면 전용 Use Case 생성 고려

**설명** (참조: 567-575라인):
- Use Case 간 동일 Output Model 공유는 결합도 증가
- 한 Use Case의 필드 추가가 다른 Use Case에 영향
- 공유 모델은 장기적으로 비대해짐 (tumorous growth)
- Single Responsibility Principle 적용: 모델 분리로 결합도 감소
- Domain Entity를 Output Model로 사용하면 엔티티 변경 이유 증가
- 11장 "Taking Shortcuts Consciously"에서 예외 논의

---

### 3.10 Read-Only Use Cases (섹션: What About Read-Only Use Cases?, 576-625라인)

**이전 화제와의 관계**: 상태 변경 Use Case를 다룬 후, 조회 전용 Use Case 처리 방법을 설명한다.

**다뤄지는 내용**:
- Read-Only Operation을 Query로 처리
- Query Service 구현
- CQS/CQRS와의 연관성
- 단축 방법

**Query Service 예제** (참조: 594-616라인):

```java
package buckpal.application.service;

@RequiredArgsConstructor
class GetAccountBalanceService implements GetAccountBalanceQuery {

    private final LoadAccountPort loadAccountPort;  // Outgoing Port

    @Override
    public Money getAccountBalance(AccountId accountId) {
        return loadAccountPort.loadAccount(accountId, LocalDateTime.now())
            .calculateBalance();  // 계좌 잔액 계산
    }
}
```

**Python 버전**:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GetAccountBalanceService(GetAccountBalanceQuery):
    """계좌 잔액 조회 Query Service"""
    load_account_port: LoadAccountPort  # Outgoing Port

    def get_account_balance(self, account_id: AccountId) -> Money:
        """계좌 잔액 조회"""
        return self.load_account_port.load_account(
            account_id,
            datetime.now()
        ).calculate_balance()
```

**설명** (참조: 617-625라인):
- Query Service는 Use Case Service와 유사하게 동작
- Incoming Port (GetAccountBalanceQuery) 구현
- Outgoing Port (LoadAccountPort) 호출
- Read-Only 쿼리를 변경 Use Case(Command)와 명확히 구분
- CQS(Command-Query Separation), CQRS와 잘 어울림
- 레이어 간 동일 모델 사용 시 클라이언트가 Outgoing Port 직접 호출 가능 (단축)
- 11장에서 단축 방법 논의

---

### 3.11 유지보수성 (섹션: How Does This Help Me Build Maintainable Software?, 626-635라인)

**이전 화제와의 관계**: 전체 Use Case 구현 방법을 설명한 후, 이 접근법의 장기적 이점을 정리한다.

**다뤄지는 내용**:
- Use Case별 전용 Input/Output Model의 장점
- 명확한 Use Case 이해
- 병렬 개발 가능성
- 엄격한 Input Validation의 효과

**설명** (참조: 626-635라인):
- 아키텍처는 도메인 로직 구현의 자유를 허용
- Use Case별 독립적 Input/Output 모델은 의도하지 않은 부작용 방지
- Use Case 간 모델 공유보다 작업량이 많지만 장기적 유지보수성 향상
- 명확한 Use Case 이해로 유지보수 용이
- 여러 개발자가 서로 다른 Use Case를 병렬로 작업 가능
- 엄격한 Input Validation과 Use Case별 전용 모델이 유지보수 가능한 코드베이스로 이어짐
