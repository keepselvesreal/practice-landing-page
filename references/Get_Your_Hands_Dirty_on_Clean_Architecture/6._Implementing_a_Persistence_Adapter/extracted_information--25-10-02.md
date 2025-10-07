# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter 6: Implementing a Persistence Adapter
## 압축 내용
영속성 어댑터를 애플리케이션 계층의 플러그인으로 구현하여 의존성을 역전시키고, Interface Segregation Principle을 적용한 좁은 포트 인터페이스를 통해 도메인 코드를 영속성 세부사항으로부터 자유롭게 만드는 방법을 설명한다.

## 핵심 내용
### 핵심 개념
1. **Dependency Inversion (의존성 역전)**
2. **Port and Adapter Pattern (포트와 어댑터 패턴)**
3. **Interface Segregation Principle (인터페이스 분리 원칙)**
4. **Persistence Adapter Responsibilities (영속성 어댑터 책임)**
5. **Domain Model vs Persistence Model Separation (도메인 모델과 영속성 모델 분리)**

### 핵심 개념 설명

#### 1. Dependency Inversion (의존성 역전)
- **설명**: 애플리케이션 서비스가 영속성 계층에 직접 의존하는 대신, 포트 인터페이스를 통해 간접적으로 접근
- **목적**: 도메인 코드를 영속성 문제로부터 분리하여 진화 가능하게 함
- **효과**: 영속성 레이어의 리팩토링이 핵심 도메인 코드 변경을 필연적으로 유발하지 않음
- **참조**: 페이지 52, 라인 5-23

#### 2. Port and Adapter Pattern (포트와 어댑터 패턴)
- **설명**: 영속성 어댑터는 애플리케이션에 의해 호출되는 "driven" 또는 "outgoing" 어댑터
- **구조**: 애플리케이션 서비스 → 포트 인터페이스 → 영속성 어댑터 → 데이터베이스
- **이점**: 포트 계약만 준수하면 영속성 어댑터를 자유롭게 수정 가능
- **참조**: 페이지 52, 라인 10-31

#### 3. Interface Segregation Principle (인터페이스 분리 원칙)
- **설명**: 넓은 인터페이스를 특정 인터페이스로 분리하여 클라이언트가 필요한 메서드만 알도록 함
- **문제점**: 단일 레포지토리 인터페이스는 불필요한 의존성과 모킹의 복잡성 초래
- **해결책**: "메서드 하나당 포트 하나" 접근으로 명확성과 테스트 용이성 향상
- **참조**: 페이지 54, 라인 67-101

#### 4. Persistence Adapter Responsibilities (영속성 어댑터 책임)
- **단계**:
  1. 입력 받기
  2. 입력을 데이터베이스 포맷으로 매핑
  3. 데이터베이스에 입력 전송
  4. 데이터베이스 출력을 애플리케이션 포맷으로 매핑
  5. 출력 반환
- **중요**: 입력/출력 모델은 애플리케이션 코어에 위치해야 하며, 영속성 어댑터에 있으면 안 됨
- **참조**: 페이지 53, 라인 32-56

#### 5. Domain Model vs Persistence Model Separation (도메인 모델과 영속성 모델 분리)
- **이유**: JPA는 no-args 생성자 등의 제약을 요구하며, 영속성 관점의 관계 설계가 도메인 모델과 다를 수 있음
- **전략**: 도메인 모델과 영속성 모델 간 양방향 매핑을 통해 풍부한 도메인 모델 유지
- **트레이드오프**: 매핑 노력 vs 도메인 모델의 순수성
- **참조**: 페이지 62, 라인 472-483

### 핵심 개념 간 관계

```
Dependency Inversion
    ↓ (구현 수단)
Port and Adapter Pattern
    ↓ (설계 원칙 적용)
Interface Segregation Principle
    ↓ (세부 구현)
Persistence Adapter Responsibilities
    ↓ (순수성 유지)
Domain Model vs Persistence Model Separation
```

**관계 설명**:
- 의존성 역전을 구현하기 위해 포트와 어댑터 패턴 사용
- 포트 설계 시 인터페이스 분리 원칙을 적용하여 좁은 인터페이스 생성
- 영속성 어댑터는 명확한 책임을 가지며, 입출력 모델을 애플리케이션 코어에 위치시킴
- 도메인 모델과 영속성 모델을 분리하여 도메인의 순수성과 풍부함을 유지

## 상세 핵심 내용
### 중요 개념

1. **Dependency Inversion (의존성 역전)**
2. **Port and Adapter Pattern (포트와 어댑터 패턴)**
3. **Interface Segregation Principle (인터페이스 분리 원칙)**
4. **Persistence Adapter Responsibilities (영속성 어댑터 책임)**
5. **Domain Model vs Persistence Model Separation (도메인 모델과 영속성 모델 분리)**
6. **Port Interface Slicing (포트 인터페이스 분할)**
7. **Persistence Adapter Slicing (영속성 어댑터 분할)**
8. **Bounded Context Separation (바운디드 컨텍스트 분리)**
9. **JPA Entity vs Domain Entity (JPA 엔티티 vs 도메인 엔티티)**
10. **Transaction Management (트랜잭션 관리)**

### 중요 개념 설명

#### 6. Port Interface Slicing (포트 인터페이스 분할)
- **단일 넓은 인터페이스의 문제**:
  - 서비스가 실제로는 하나의 메서드만 사용해도 전체 인터페이스에 의존
  - 불필요한 의존성으로 코드 이해와 테스트가 어려워짐
  - 유닛 테스트에서 어떤 메서드를 모킹해야 할지 파악하기 어려움
- **해결책**:
  - "메서드 하나당 포트 하나" 접근으로 특정 인터페이스 생성
  - 예: `LoadAccountPort`, `UpdateAccountStatePort` 등
  - 포트 이름이 명확하게 목적을 표현
- **효과**:
  - 플러그 앤 플레이 코딩 경험
  - 테스트 시 모킹할 메서드가 명확함
  - 불필요한 짐(baggage) 제거
- **예외**: 응집력이 높고 자주 함께 사용되는 데이터베이스 작업은 하나의 인터페이스로 묶을 수 있음
- **참조**: 페이지 54-55, 라인 67-104

#### 7. Persistence Adapter Slicing (영속성 어댑터 분할)
- **단일 어댑터의 대안**:
  - 모든 영속성 포트를 구현하는 한, 여러 클래스로 분할 가능
  - 영속성이 필요한 도메인 클래스(aggregate)당 하나의 어댑터 생성
- **장점**:
  - 도메인의 경계(seam)를 따라 자동으로 분할됨
  - 일부 포트는 JPA로, 다른 포트는 성능을 위해 plain SQL로 구현 가능
- **유연성**:
  - 도메인 코드는 어떤 클래스가 포트 계약을 충족하는지 신경 쓰지 않음
  - 모든 포트가 구현되기만 하면 영속성 레이어에서 자유롭게 설계 가능
- **바운디드 컨텍스트와의 관계**:
  - 향후 여러 바운디드 컨텍스트 분리 시 좋은 기반 제공
- **참조**: 페이지 55-56, 라인 105-124

#### 8. Bounded Context Separation (바운디드 컨텍스트 분리)
- **구조**:
  - 각 바운디드 컨텍스트가 자체 영속성 어댑터 보유
  - 예: account 컨텍스트, billing 컨텍스트
- **경계 규칙**:
  - account 컨텍스트의 서비스는 billing 컨텍스트의 영속성 어댑터에 접근 불가
  - 반대도 동일하게 적용
- **컨텍스트 간 통신**:
  - 한 컨텍스트가 다른 컨텍스트의 무언가를 필요로 하면 전용 incoming 포트를 통해 접근
- **참조**: 페이지 57, 라인 125-137

#### 9. JPA Entity vs Domain Entity (JPA 엔티티 vs 도메인 엔티티)
- **Domain Entity 특징**:
  - 단순 데이터 클래스가 아님
  - 가능한 한 불변(immutable)
  - 팩토리 메서드로 유효한 상태의 Account 생성
  - 모든 변경 메서드가 검증 수행 (예: 출금 전 잔액 확인)
  - 유효하지 않은 도메인 모델 생성 불가
- **JPA Entity 특징**:
  - @Entity, @Table 등 JPA 어노테이션 사용
  - 데이터베이스 테이블 구조 반영
  - 단순 데이터 저장 목적
- **분리 이유**:
  - JPA가 no-args 생성자 등의 제약 요구
  - 영속성 관점의 @ManyToOne 관계가 도메인 모델에서는 반대 방향이 더 적합할 수 있음
  - 풍부한 도메인 모델을 타협 없이 만들기 위함
- **트레이드오프**:
  - 매핑 노력 vs 순수한 도메인 모델
  - "no mapping" 전략도 유효할 수 있음 (8장에서 논의)
- **참조**: 페이지 58-62, 라인 147-483

#### 10. Transaction Management (트랜잭션 관리)
- **트랜잭션 범위**:
  - 특정 유스케이스 내의 모든 쓰기 작업을 포괄
  - 하나의 작업이 실패하면 모든 작업을 함께 롤백
- **책임 위치**:
  - 영속성 어댑터는 같은 유스케이스의 다른 데이터베이스 작업을 알 수 없음
  - 따라서 트랜잭션 시작/종료 시점을 결정할 수 없음
  - 영속성 어댑터 호출을 조율하는 서비스에 책임 위임
- **구현 방법 (Java & Spring)**:
  - 애플리케이션 서비스 클래스에 `@Transactional` 어노테이션 추가
  - Spring이 모든 public 메서드를 트랜잭션으로 래핑
- **대안**:
  - AspectJ 등의 AOP 사용하여 트랜잭션 경계를 코드베이스에 위빙
  - 서비스를 순수하게 유지 가능
- **참조**: 페이지 63, 라인 488-511

### 중요 개념 간 관계

```
Dependency Inversion (의존성 역전)
    ↓
Port and Adapter Pattern (포트와 어댑터 패턴)
    ↓
    ├─→ Port Interface Slicing (포트 인터페이스 분할)
    │   └─→ Interface Segregation Principle (인터페이스 분리 원칙)
    │
    └─→ Persistence Adapter Slicing (영속성 어댑터 분할)
        └─→ Bounded Context Separation (바운디드 컨텍스트 분리)

Persistence Adapter Responsibilities (영속성 어댑터 책임)
    ↓
    ├─→ Domain Model vs Persistence Model Separation
    │   └─→ JPA Entity vs Domain Entity
    │
    └─→ Transaction Management (트랜잭션 관리)
```

**상세 관계 설명**:

1. **의존성 역전 → 포트와 어댑터 패턴**: 의존성 역전 원칙을 실현하기 위한 구체적 패턴

2. **포트와 어댑터 패턴의 두 가지 측면**:
   - **포트 측면**: Interface Segregation Principle을 적용하여 좁은 포트 인터페이스로 분할
   - **어댑터 측면**: 도메인 경계나 기술적 필요에 따라 여러 어댑터로 분할 가능

3. **어댑터 분할 → 바운디드 컨텍스트**: 어댑터를 aggregate 단위로 분할하면 향후 바운디드 컨텍스트 분리의 좋은 기반 제공

4. **영속성 어댑터 책임의 두 가지 중요 결과**:
   - **모델 분리**: 도메인 모델과 영속성 모델을 분리하여 각각의 관심사에 집중
   - **트랜잭션 관리**: 영속성 어댑터는 개별 작업만 수행하고, 트랜잭션 경계는 서비스 레이어에서 관리

5. **모델 분리의 실제 구현**: JPA 엔티티와 도메인 엔티티를 분리하여 JPA의 제약으로부터 도메인 모델 보호

## 상세 내용

### 1. 의존성 역전 (Dependency Inversion)

**전통적인 계층 아키텍처의 문제점** (참조: 페이지 52, 라인 5-8)
- 전통적인 계층 아키텍처는 "데이터베이스 주도 설계"를 지원
- 모든 것이 영속성 계층에 의존하는 구조
- 1장에서 이 문제를 지적했음

**해결책: 영속성 레이어를 플러그인으로** (참조: 페이지 52, 라인 7-12)
- 영속성 계층 대신 "영속성 어댑터" 사용
- 영속성 어댑터가 애플리케이션 서비스에 영속성 기능 제공
- Dependency Inversion Principle을 적용하여 의존성 역전

**의존성 역전의 구조** (참조: 페이지 52, 라인 13-23)
```
Application Core
    ↓ (포트 인터페이스 호출)
Port Interfaces (애플리케이션 코어에 위치)
    ↑ (구현)
Persistence Adapter (외부 레이어)
    ↓
Database
```

- 애플리케이션 서비스가 포트 인터페이스 호출
- 포트는 영속성 어댑터 클래스에 의해 구현됨
- 어댑터가 실제 영속성 작업 수행 및 데이터베이스 통신

**간접 레이어의 목적** (참조: 페이지 52, 라인 19-23)
- 도메인 코드를 영속성 문제를 고려하지 않고 진화시킬 수 있음
- 영속성 레이어에 대한 코드 의존성이 없음
- 영속성 코드의 리팩토링이 반드시 코어의 코드 변경을 유발하지 않음

**런타임 vs 컴파일타임 의존성** (참조: 페이지 53, 라인 28-31)
- 런타임에는 여전히 애플리케이션 코어에서 영속성 어댑터로의 의존성 존재
- 영속성 레이어에 버그를 도입하면 애플리케이션 코어 기능이 깨질 수 있음
- 하지만 포트 계약이 충족되는 한, 영속성 어댑터에서 자유롭게 작업 가능

### 2. 영속성 어댑터의 책임 (Responsibilities of a Persistence Adapter)

**5단계 프로세스** (참조: 페이지 53, 라인 32-38)

1. **입력 받기 (Take input)**
   - 포트 인터페이스를 통해 입력 받음
   - 입력 모델은 도메인 엔티티이거나 특정 데이터베이스 작업 전용 객체

2. **입력을 데이터베이스 포맷으로 매핑 (Map input into database format)**
   - Java 프로젝트에서는 JPA를 일반적으로 사용
   - 입력을 데이터베이스 테이블 구조를 반영하는 JPA 엔티티 객체로 매핑
   - 상황에 따라 매핑이 많은 작업일 수 있음 (8장에서 매핑 없는 전략 논의)

3. **데이터베이스에 입력 전송 (Send input to the database)**
   - JPA 또는 다른 OR 매핑 프레임워크 사용
   - 또는 plain SQL 문으로 매핑하여 전송
   - 또는 데이터를 파일로 직렬화하여 저장

4. **데이터베이스 출력을 애플리케이션 포맷으로 매핑 (Map database output into application format)**
   - 데이터베이스 쿼리 수행 및 결과 수신
   - 포트가 기대하는 출력 모델로 매핑

5. **출력 반환 (Return output)**
   - 애플리케이션 코어로 결과 반환

**중요한 원칙** (참조: 페이지 53, 라인 50-56)
- 입력 모델과 출력 모델은 **애플리케이션 코어**에 위치해야 함
- 영속성 어댑터 자체에 있으면 안 됨
- 이를 통해 영속성 어댑터의 변경이 코어에 영향을 주지 않음

**전통적인 영속성 레이어와의 차이** (참조: 페이지 53, 라인 57-62)
- 입출력 모델의 위치를 제외하면 책임은 전통적인 영속성 레이어와 크게 다르지 않음
- 하지만 이 구현 방식은 필연적으로 몇 가지 질문을 제기함
- 전통적인 방식에 너무 익숙해서 생각하지 않던 질문들

### 3. 포트 인터페이스 분할 (Slicing Port Interfaces)

**문제: 단일 넓은 레포지토리 인터페이스** (참조: 페이지 54, 라인 67-76)

전통적인 접근 방식:
```java
// 단일 넓은 인터페이스
interface AccountRepository {
    Account findById(Long id);
    void save(Account account);
    void delete(Account account);
    List<Account> findAll();
    List<Account> findByOwner(String owner);
    // ... 더 많은 메서드들
}
```

```python
# Python 버전
from abc import ABC, abstractmethod
from typing import List, Optional

class AccountRepository(ABC):
    """단일 넓은 레포지토리 인터페이스"""

    @abstractmethod
    def find_by_id(self, id: int) -> Optional['Account']:
        pass

    @abstractmethod
    def save(self, account: 'Account') -> None:
        pass

    @abstractmethod
    def delete(self, account: 'Account') -> None:
        pass

    @abstractmethod
    def find_all(self) -> List['Account']:
        pass

    @abstractmethod
    def find_by_owner(self, owner: str) -> List['Account']:
        pass
```

문제점:
- 특정 엔티티에 대한 모든 데이터베이스 작업을 하나의 인터페이스에 집중
- 각 서비스가 단 하나의 메서드만 사용해도 전체 인터페이스에 의존
- 불필요한 의존성 발생

**불필요한 의존성의 문제** (참조: 페이지 54, 라인 77-83)
- 컨텍스트에서 필요하지 않은 메서드에 대한 의존성은 코드를 이해하고 테스트하기 어렵게 만듦
- 유닛 테스트 작성 시:
  - `RegisterAccountService`를 테스트하려면 어떤 메서드를 모킹해야 할까?
  - 먼저 서비스가 실제로 호출하는 메서드를 찾아야 함
  - 인터페이스의 일부만 모킹하면 다른 문제 발생 가능
  - 다음 사람이 전체 인터페이스가 모킹되었을 것으로 기대하고 에러 발생
  - 다시 조사 필요

**Martin C. Robert의 조언** (참조: 페이지 54, 라인 84-86)
> "Depending on something that carries baggage that you don't need can cause you troubles that you didn't expect."
> (필요하지 않은 짐을 가진 무언가에 의존하는 것은 예상하지 못한 문제를 일으킬 수 있다.)

**해결책: Interface Segregation Principle** (참조: 페이지 54-55, 라인 87-101)

원칙:
- 넓은 인터페이스는 특정 인터페이스로 분리되어야 함
- 클라이언트는 필요한 메서드만 알아야 함

적용 결과:
```java
// 좁은 포트 인터페이스들
interface LoadAccountPort {
    Account loadAccount(AccountId accountId, LocalDateTime baselineDate);
}

interface UpdateAccountStatePort {
    void updateActivities(Account account);
}
```

```python
# Python 버전
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class LoadAccountPort(ABC):
    """계정 로드 포트"""

    @abstractmethod
    def load_account(
        self,
        account_id: 'AccountId',
        baseline_date: datetime
    ) -> 'Account':
        """
        특정 시점의 계정 정보를 로드한다.

        Args:
            account_id: 계정 ID
            baseline_date: 기준 시점

        Returns:
            Account: 로드된 계정 엔티티
        """
        pass


class UpdateAccountStatePort(ABC):
    """계정 상태 업데이트 포트"""

    @abstractmethod
    def update_activities(self, account: 'Account') -> None:
        """
        계정의 활동 내역을 업데이트한다.

        Args:
            account: 업데이트할 계정 엔티티
        """
        pass
```

장점:
- 각 서비스가 실제로 필요한 메서드에만 의존
- 포트 이름이 명확하게 목적을 표현
- 테스트에서 어떤 메서드를 모킹할지 고민할 필요 없음 (대부분 메서드가 하나)

**플러그 앤 플레이 경험** (참조: 페이지 55, 라인 100-101)
- 좁은 포트를 사용하면 코딩이 플러그 앤 플레이 경험이 됨
- 서비스 작업 시 필요한 포트만 "플러그인"
- 짐(baggage)을 들고 다닐 필요 없음

**예외 사항** (참조: 페이지 55, 라인 102-104)
- "메서드 하나당 포트 하나" 접근이 모든 상황에 적용되지는 않음
- 응집력이 높고 자주 함께 사용되는 데이터베이스 작업 그룹은 하나의 인터페이스로 묶을 수 있음

### 4. 영속성 어댑터 분할 (Slicing Persistence Adapters)

**단일 어댑터의 대안** (참조: 페이지 55-56, 라인 105-108)
- 모든 영속성 포트를 구현하는 단일 영속성 어댑터 클래스를 봤음
- 하지만 둘 이상의 클래스를 만드는 것을 금지하는 규칙은 없음
- 모든 영속성 포트가 구현되기만 하면 됨

**Aggregate당 하나의 어댑터** (참조: 페이지 56, 라인 109-117)

```java
// Account Aggregate를 위한 어댑터
@Component
class AccountPersistenceAdapter implements
    LoadAccountPort,
    UpdateAccountStatePort {
    // Account 관련 영속성 작업
}

// Billing Aggregate를 위한 어댑터
@Component
class BillingPersistenceAdapter implements
    LoadBillingPort,
    SaveBillingPort {
    // Billing 관련 영속성 작업
}
```

```python
# Python 버전
from typing import Protocol

class AccountPersistenceAdapter:
    """Account Aggregate를 위한 영속성 어댑터"""

    def __init__(
        self,
        account_repository: 'AccountRepository',
        activity_repository: 'ActivityRepository'
    ):
        self.account_repository = account_repository
        self.activity_repository = activity_repository

    def load_account(
        self,
        account_id: 'AccountId',
        baseline_date: datetime
    ) -> 'Account':
        """LoadAccountPort 구현"""
        # Account 로딩 로직
        pass

    def update_activities(self, account: 'Account') -> None:
        """UpdateAccountStatePort 구현"""
        # Activity 업데이트 로직
        pass


class BillingPersistenceAdapter:
    """Billing Aggregate를 위한 영속성 어댑터"""

    def __init__(self, billing_repository: 'BillingRepository'):
        self.billing_repository = billing_repository

    def load_billing(self, billing_id: 'BillingId') -> 'Billing':
        """LoadBillingPort 구현"""
        pass

    def save_billing(self, billing: 'Billing') -> None:
        """SaveBillingPort 구현"""
        pass
```

장점:
- 영속성 어댑터가 지원하는 도메인의 경계(seam)를 따라 자동으로 분할됨

**기술별 분할** (참조: 페이지 56, 라인 118-121)
- 일부 포트는 JPA로 구현
- 다른 포트는 성능을 위해 plain SQL로 구현
- JPA 어댑터와 plain SQL 어댑터를 각각 생성
- 각각이 영속성 포트의 하위 집합 구현

**유연성** (참조: 페이지 56, 라인 122-124)
- 도메인 코드는 어떤 클래스가 포트 계약을 충족하는지 신경 쓰지 않음
- 모든 포트가 구현되기만 하면 영속성 레이어에서 자유롭게 작업 가능

**바운디드 컨텍스트와의 관계** (참조: 페이지 56-57, 라인 125-137)

향후 바운디드 컨텍스트 분리 시나리오:
- 시간이 지나 billing 관련 유스케이스를 위한 바운디드 컨텍스트 식별
- 각 바운디드 컨텍스트가 자체 영속성 어댑터 보유

```
Account Context              Billing Context
    ↓                            ↓
Account Persistence          Billing Persistence
Adapter                      Adapter
    ↓                            ↓
Account Database            Billing Database
```

경계 규칙:
- account 컨텍스트의 서비스는 billing 컨텍스트의 영속성 어댑터에 접근 불가
- 반대도 동일
- 한 컨텍스트가 다른 컨텍스트의 무언가를 필요로 하면 전용 incoming 포트를 통해 접근

### 5. Spring Data JPA 예제

#### 5.1 Domain Entity: Account

**Account 엔티티 골격** (참조: 페이지 58, 라인 147-208)

```java
package buckpal.domain;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Account {

    @Getter private final AccountId id;
    @Getter private final ActivityWindow activityWindow;
    private final Money baselineBalance;

    // ID 없이 Account 생성 (신규)
    public static Account withoutId(
        Money baselineBalance,
        ActivityWindow activityWindow) {
        return new Account(null, baselineBalance, activityWindow);
    }

    // ID와 함께 Account 생성 (기존)
    public static Account withId(
        AccountId accountId,
        Money baselineBalance,
        ActivityWindow activityWindow) {
        return new Account(accountId, baselineBalance, activityWindow);
    }

    // 잔액 계산
    public Money calculateBalance() {
        // ...
    }

    // 출금 (검증 포함)
    public boolean withdraw(Money money, AccountId targetAccountId) {
        // ...
    }

    // 입금 (검증 포함)
    public boolean deposit(Money money, AccountId sourceAccountId) {
        // ...
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from typing import Optional
from enum import Enum

@dataclass(frozen=True)
class AccountId:
    """계정 ID 값 객체"""
    value: int


@dataclass(frozen=True)
class Money:
    """금액 값 객체"""
    amount: int

    def add(self, other: 'Money') -> 'Money':
        return Money(self.amount + other.amount)

    def subtract(self, other: 'Money') -> 'Money':
        return Money(self.amount - other.amount)

    def is_positive(self) -> bool:
        return self.amount > 0

    def is_negative(self) -> bool:
        return self.amount < 0


class Account:
    """계정 도메인 엔티티 - 불변성과 유효성을 강조"""

    def __init__(
        self,
        id: Optional[AccountId],
        baseline_balance: Money,
        activity_window: 'ActivityWindow'
    ):
        # private 생성자 - 팩토리 메서드를 통해서만 생성
        self._id = id
        self._baseline_balance = baseline_balance
        self._activity_window = activity_window

    @property
    def id(self) -> Optional[AccountId]:
        return self._id

    @property
    def activity_window(self) -> 'ActivityWindow':
        return self._activity_window

    @staticmethod
    def without_id(
        baseline_balance: Money,
        activity_window: 'ActivityWindow'
    ) -> 'Account':
        """ID 없이 Account 생성 (신규 계정)"""
        return Account(None, baseline_balance, activity_window)

    @staticmethod
    def with_id(
        account_id: AccountId,
        baseline_balance: Money,
        activity_window: 'ActivityWindow'
    ) -> 'Account':
        """ID와 함께 Account 생성 (기존 계정)"""
        return Account(account_id, baseline_balance, activity_window)

    def calculate_balance(self) -> Money:
        """현재 잔액 계산"""
        # baseline_balance + activity_window의 모든 활동 합계
        return self._baseline_balance
        # 실제로는 activity_window의 활동들을 합산

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        """
        출금 (검증 포함)

        Args:
            money: 출금할 금액
            target_account_id: 대상 계정 ID

        Returns:
            bool: 출금 성공 여부
        """
        # 잔액 확인 등의 검증
        if not self._can_withdraw(money):
            return False

        # 출금 활동 추가
        # ...
        return True

    def deposit(self, money: Money, source_account_id: AccountId) -> bool:
        """
        입금 (검증 포함)

        Args:
            money: 입금할 금액
            source_account_id: 출처 계정 ID

        Returns:
            bool: 입금 성공 여부
        """
        # 입금 활동 추가
        # ...
        return True

    def _can_withdraw(self, money: Money) -> bool:
        """출금 가능 여부 확인 (내부 검증)"""
        return self.calculate_balance().subtract(money).is_positive()
```

**Account의 특징** (참조: 페이지 58-59, 라인 209-212)
- 단순한 getter/setter 데이터 클래스가 아님
- 가능한 한 불변(immutable)
- 유효한 상태의 Account를 생성하는 팩토리 메서드만 제공
- 모든 변경 메서드가 검증 수행 (예: 출금 전 잔액 확인)
- 유효하지 않은 도메인 모델을 생성할 수 없음

#### 5.2 JPA Entities

**AccountJpaEntity** (참조: 페이지 59, 라인 219-243)

```java
package buckpal.adapter.persistence;

@Entity
@Table(name = "account")
@Data
@AllArgsConstructor
@NoArgsConstructor
class AccountJpaEntity {

    @Id
    @GeneratedValue
    private Long id;
}
```

```python
# Python 버전 (SQLAlchemy 사용)
from sqlalchemy import Column, Integer, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccountJpaEntity(Base):
    """계정 JPA 엔티티 - 데이터베이스 테이블 매핑"""

    __tablename__ = 'account'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    def __init__(self, id: Optional[int] = None):
        self.id = id
```

**ActivityJpaEntity** (참조: 페이지 59, 라인 244-279)

```java
package buckpal.adapter.persistence;

@Entity
@Table(name = "activity")
@Data
@AllArgsConstructor
@NoArgsConstructor
class ActivityJpaEntity {

    @Id
    @GeneratedValue
    private Long id;

    @Column private LocalDateTime timestamp;
    @Column private Long ownerAccountId;
    @Column private Long sourceAccountId;
    @Column private Long targetAccountId;
    @Column private Long amount;
}
```

```python
# Python 버전 (SQLAlchemy 사용)
from datetime import datetime
from typing import Optional

class ActivityJpaEntity(Base):
    """활동 JPA 엔티티 - 데이터베이스 테이블 매핑"""

    __tablename__ = 'activity'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    owner_account_id = Column(BigInteger, nullable=False)
    source_account_id = Column(BigInteger, nullable=False)
    target_account_id = Column(BigInteger, nullable=False)
    amount = Column(BigInteger, nullable=False)

    def __init__(
        self,
        id: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        owner_account_id: Optional[int] = None,
        source_account_id: Optional[int] = None,
        target_account_id: Optional[int] = None,
        amount: Optional[int] = None
    ):
        self.id = id
        self.timestamp = timestamp
        self.owner_account_id = owner_account_id
        self.source_account_id = source_account_id
        self.target_account_id = target_account_id
        self.amount = amount
```

**JPA Entity 설계 결정** (참조: 페이지 59-60, 라인 280-290)
- Account의 상태는 현 단계에서는 id만 포함
- 나중에 user ID 등의 필드 추가 가능
- ActivityJpaEntity가 더 흥미로움 - 특정 계정에 대한 모든 활동 포함
- ActivityJpaEntity와 AccountJpaEntity를 JPA의 @ManyToOne 또는 @OneToMany로 연결할 수 있음
- 하지만 데이터베이스 쿼리에 부작용을 추가하므로 생략
- 현 단계에서는 JPA보다 더 간단한 OR 매퍼를 사용하는 것이 더 쉬울 수 있음
- 하지만 향후 필요할 것으로 생각하여 JPA 사용

#### 5.3 Spring Data Repositories

**Repository 인터페이스** (참조: 페이지 60, 라인 291-344)

```java
// AccountRepository - 기본 CRUD만 제공
interface AccountRepository extends JpaRepository<AccountJpaEntity, Long> {
}

// ActivityRepository - 커스텀 쿼리 포함
interface ActivityRepository extends JpaRepository<ActivityJpaEntity, Long> {

    // 특정 시점 이후의 활동 조회
    @Query("select a from ActivityJpaEntity a " +
           "where a.ownerAccountId = :ownerAccountId " +
           "and a.timestamp >= :since")
    List<ActivityJpaEntity> findByOwnerSince(
        @Param("ownerAccountId") Long ownerAccountId,
        @Param("since") LocalDateTime since);

    // 특정 시점까지의 입금 잔액
    @Query("select sum(a.amount) from ActivityJpaEntity a " +
           "where a.targetAccountId = :accountId " +
           "and a.ownerAccountId = :accountId " +
           "and a.timestamp < :until")
    Long getDepositBalanceUntil(
        @Param("accountId") Long accountId,
        @Param("until") LocalDateTime until);

    // 특정 시점까지의 출금 잔액
    @Query("select sum(a.amount) from ActivityJpaEntity a " +
           "where a.sourceAccountId = :accountId " +
           "and a.ownerAccountId = :accountId " +
           "and a.timestamp < :until")
    Long getWithdrawalBalanceUntil(
        @Param("accountId") Long accountId,
        @Param("until") LocalDateTime until);
}
```

```python
# Python 버전 (SQLAlchemy 사용)
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

class AccountRepository:
    """Account JPA 레포지토리 - 기본 CRUD"""

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: int) -> Optional[AccountJpaEntity]:
        """ID로 계정 조회"""
        return self.session.query(AccountJpaEntity).filter(
            AccountJpaEntity.id == id
        ).first()

    def save(self, account: AccountJpaEntity) -> AccountJpaEntity:
        """계정 저장"""
        self.session.add(account)
        self.session.commit()
        return account


class ActivityRepository:
    """Activity JPA 레포지토리 - 커스텀 쿼리 포함"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, activity: ActivityJpaEntity) -> ActivityJpaEntity:
        """활동 저장"""
        self.session.add(activity)
        self.session.commit()
        return activity

    def find_by_owner_since(
        self,
        owner_account_id: int,
        since: datetime
    ) -> List[ActivityJpaEntity]:
        """특정 시점 이후의 활동 조회"""
        return self.session.query(ActivityJpaEntity).filter(
            ActivityJpaEntity.owner_account_id == owner_account_id,
            ActivityJpaEntity.timestamp >= since
        ).all()

    def get_deposit_balance_until(
        self,
        account_id: int,
        until: datetime
    ) -> int:
        """특정 시점까지의 입금 잔액 계산"""
        result = self.session.query(
            func.sum(ActivityJpaEntity.amount)
        ).filter(
            ActivityJpaEntity.target_account_id == account_id,
            ActivityJpaEntity.owner_account_id == account_id,
            ActivityJpaEntity.timestamp < until
        ).scalar()

        return result if result is not None else 0

    def get_withdrawal_balance_until(
        self,
        account_id: int,
        until: datetime
    ) -> int:
        """특정 시점까지의 출금 잔액 계산"""
        result = self.session.query(
            func.sum(ActivityJpaEntity.amount)
        ).filter(
            ActivityJpaEntity.source_account_id == account_id,
            ActivityJpaEntity.owner_account_id == account_id,
            ActivityJpaEntity.timestamp < until
        ).scalar()

        return result if result is not None else 0
```

**Spring Data의 역할** (참조: 페이지 60, 라인 345-346)
- Spring Boot가 자동으로 레포지토리 발견
- Spring Data가 마법을 부려 실제로 데이터베이스와 통신하는 구현 제공

#### 5.4 Persistence Adapter 구현

**AccountPersistenceAdapter** (참조: 페이지 61-62, 라인 356-461)

```java
@RequiredArgsConstructor
@Component
class AccountPersistenceAdapter implements
    LoadAccountPort,
    UpdateAccountStatePort {

    private final AccountRepository accountRepository;
    private final ActivityRepository activityRepository;
    private final AccountMapper accountMapper;

    @Override
    public Account loadAccount(
        AccountId accountId,
        LocalDateTime baselineDate) {

        // 1. Account 로드
        AccountJpaEntity account =
            accountRepository.findById(accountId.getValue())
                .orElseThrow(EntityNotFoundException::new);

        // 2. 특정 시점 이후의 활동 로드
        List<ActivityJpaEntity> activities =
            activityRepository.findByOwnerSince(
                accountId.getValue(),
                baselineDate);

        // 3. 특정 시점까지의 출금 잔액 계산
        Long withdrawalBalance = orZero(activityRepository
            .getWithdrawalBalanceUntil(
                accountId.getValue(),
                baselineDate));

        // 4. 특정 시점까지의 입금 잔액 계산
        Long depositBalance = orZero(activityRepository
            .getDepositBalanceUntil(
                accountId.getValue(),
                baselineDate));

        // 5. 도메인 엔티티로 매핑하여 반환
        return accountMapper.mapToDomainEntity(
            account,
            activities,
            withdrawalBalance,
            depositBalance);
    }

    private Long orZero(Long value){
        return value == null ? 0L : value;
    }

    @Override
    public void updateActivities(Account account) {
        // 새로운 활동만 저장 (ID가 없는 활동)
        for (Activity activity : account.getActivityWindow().getActivities()) {
            if (activity.getId() == null) {
                activityRepository.save(accountMapper.mapToJpaEntity(activity));
            }
        }
    }
}
```

```python
# Python 버전
from typing import Optional
from datetime import datetime

class AccountPersistenceAdapter:
    """
    계정 영속성 어댑터
    - LoadAccountPort와 UpdateAccountStatePort 구현
    """

    def __init__(
        self,
        account_repository: AccountRepository,
        activity_repository: ActivityRepository,
        account_mapper: 'AccountMapper'
    ):
        self.account_repository = account_repository
        self.activity_repository = activity_repository
        self.account_mapper = account_mapper

    def load_account(
        self,
        account_id: AccountId,
        baseline_date: datetime
    ) -> Account:
        """
        LoadAccountPort 구현: 계정 로드

        Args:
            account_id: 로드할 계정 ID
            baseline_date: 기준 날짜

        Returns:
            Account: 로드된 도메인 엔티티

        Raises:
            EntityNotFoundException: 계정을 찾을 수 없는 경우
        """
        # 1. Account JPA 엔티티 로드
        account = self.account_repository.find_by_id(account_id.value)
        if account is None:
            raise EntityNotFoundException(f"Account {account_id.value} not found")

        # 2. 특정 시점 이후의 활동 로드
        activities = self.activity_repository.find_by_owner_since(
            account_id.value,
            baseline_date
        )

        # 3. 특정 시점까지의 출금 잔액 계산
        withdrawal_balance = self._or_zero(
            self.activity_repository.get_withdrawal_balance_until(
                account_id.value,
                baseline_date
            )
        )

        # 4. 특정 시점까지의 입금 잔액 계산
        deposit_balance = self._or_zero(
            self.activity_repository.get_deposit_balance_until(
                account_id.value,
                baseline_date
            )
        )

        # 5. JPA 엔티티를 도메인 엔티티로 매핑하여 반환
        return self.account_mapper.map_to_domain_entity(
            account,
            activities,
            withdrawal_balance,
            deposit_balance
        )

    def _or_zero(self, value: Optional[int]) -> int:
        """None을 0으로 변환"""
        return value if value is not None else 0

    def update_activities(self, account: Account) -> None:
        """
        UpdateAccountStatePort 구현: 계정 활동 업데이트

        Args:
            account: 업데이트할 계정 도메인 엔티티
        """
        # 새로운 활동만 저장 (ID가 없는 활동)
        for activity in account.activity_window.activities:
            if activity.id is None:
                # 도메인 엔티티를 JPA 엔티티로 매핑하여 저장
                jpa_entity = self.account_mapper.map_to_jpa_entity(activity)
                self.activity_repository.save(jpa_entity)


class EntityNotFoundException(Exception):
    """엔티티를 찾을 수 없을 때 발생하는 예외"""
    pass
```

**영속성 어댑터의 동작** (참조: 페이지 62, 라인 462-471)

두 개의 포트 구현:
1. **LoadAccountPort**: 계정 로드
2. **UpdateAccountStatePort**: 계정 상태 업데이트

계정 로드 프로세스:
1. AccountRepository에서 계정 로드
2. ActivityRepository를 통해 특정 시간 윈도우의 활동 로드
3. 활동 윈도우 시작 전 계정 잔액 계산 (유효한 Account 도메인 엔티티 생성에 필요)
4. 모든 출금과 입금의 합계를 데이터베이스에서 가져옴
5. 모든 데이터를 Account 도메인 엔티티로 매핑하여 호출자에게 반환

계정 상태 업데이트 프로세스:
1. Account 엔티티의 모든 활동을 반복
2. ID가 있는지 확인
3. ID가 없으면 새로운 활동이므로 ActivityRepository를 통해 저장

**도메인 모델과 데이터베이스 모델 간 매핑** (참조: 페이지 62, 라인 472-483)

질문: 왜 양방향 매핑을 해야 할까?
- JPA 어노테이션을 Account와 Activity 클래스로 옮겨서 직접 데이터베이스에 저장하면 안 될까?

"no mapping" 전략:
- 유효한 선택일 수 있음 (8장에서 매핑 전략 논의)
- 하지만 JPA가 도메인 모델에서 타협을 강요함

JPA의 제약 예시:
- JPA는 엔티티가 no-args 생성자를 가질 것을 요구
- 영속성 레이어에서는 성능 관점에서 @ManyToOne 관계가 적합할 수 있음
- 하지만 도메인 모델에서는 항상 데이터의 일부만 로드하므로 반대 방향 관계가 더 적합할 수 있음

결론:
- 기본 영속성에 타협 없는 풍부한 도메인 모델을 만들고 싶다면 도메인 모델과 영속성 모델 간 매핑 필요

### 6. 데이터베이스 트랜잭션 (Database Transactions)

**트랜잭션의 필요성** (참조: 페이지 63, 라인 488-492)
- 트랜잭션은 특정 유스케이스 내에서 수행되는 모든 쓰기 작업을 포괄해야 함
- 하나의 작업이 실패하면 모든 작업을 함께 롤백할 수 있어야 함

**트랜잭션 경계의 위치** (참조: 페이지 63, 라인 493-495)
- 영속성 어댑터는 같은 유스케이스의 다른 데이터베이스 작업을 알 수 없음
- 따라서 트랜잭션을 언제 열고 닫을지 결정할 수 없음
- 영속성 어댑터 호출을 조율하는 서비스에 이 책임을 위임해야 함

**Java & Spring에서의 구현** (참조: 페이지 63, 라인 496-508)

```java
package buckpal.application.service;

@Transactional  // 모든 public 메서드를 트랜잭션으로 래핑
public class SendMoneyService implements SendMoneyUseCase {
    ...
}
```

```python
# Python 버전 (SQLAlchemy + 데코레이터 사용)
from functools import wraps
from sqlalchemy.orm import Session

def transactional(func):
    """트랜잭션 데코레이터"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            raise
    return wrapper


class SendMoneyService:
    """송금 서비스 - 트랜잭션 관리"""

    def __init__(self, session: Session):
        self.session = session

    @transactional
    def send_money(self, command: 'SendMoneyCommand') -> bool:
        """
        송금 유스케이스 - 트랜잭션으로 래핑됨

        Args:
            command: 송금 커맨드

        Returns:
            bool: 송금 성공 여부
        """
        # 여러 영속성 어댑터 호출이 하나의 트랜잭션으로 묶임
        # ...
        pass
```

**대안: AspectJ를 사용한 AOP** (참조: 페이지 63, 라인 509-511)
- 서비스를 순수하게 유지하고 싶다면 (어노테이션으로 더럽히지 않으려면)
- AspectJ 등의 AOP 사용
- 트랜잭션 경계를 코드베이스에 위빙(weaving)

```python
# Python 버전 (Aspect-Oriented Programming 스타일)
from typing import Callable, Any

class TransactionAspect:
    """트랜잭션 관리를 위한 Aspect"""

    def __init__(self, session: Session):
        self.session = session

    def around_service_method(
        self,
        method: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        서비스 메서드 실행 전후에 트랜잭션 처리

        Args:
            method: 실행할 메서드
            *args: 메서드 인자
            **kwargs: 메서드 키워드 인자

        Returns:
            메서드 실행 결과
        """
        try:
            result = method(*args, **kwargs)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            raise


# 순수한 서비스 클래스 (트랜잭션 어노테이션 없음)
class PureSendMoneyService:
    """순수한 송금 서비스 - 트랜잭션 로직 분리"""

    def send_money(self, command: 'SendMoneyCommand') -> bool:
        """순수한 비즈니스 로직만 포함"""
        # ...
        pass
```

### 7. 유지보수 가능한 소프트웨어 구축에 도움이 되는 이유

**핵심 이점** (참조: 페이지 63, 라인 512-517)

1. **도메인 코드의 자유**:
   - 영속성 어댑터가 도메인 코드의 플러그인으로 작동
   - 도메인 코드를 영속성 세부사항으로부터 해방
   - 풍부한 도메인 모델 구축 가능

2. **유연성**:
   - 좁은 포트 인터페이스 사용
   - 한 포트는 이 방식으로, 다른 포트는 다른 방식으로 구현 가능
   - 심지어 다른 영속성 기술 사용 가능
   - 애플리케이션이 알아차리지 못함

3. **교체 가능성**:
   - 포트 계약만 준수하면 전체 영속성 레이어 교체 가능
   - 도메인 코드에 영향 없음

**아키텍처의 본질**:
```
유연성 = 좁은 인터페이스 + 의존성 역전 + 명확한 경계

도메인의 순수성 = 풍부한 도메인 모델 + 영속성 세부사항 분리

유지보수성 = 유연성 + 도메인의 순수성 + 교체 가능성
```
