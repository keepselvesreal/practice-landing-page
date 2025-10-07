# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter6: Implementing a Persistence Adapter

## 압축 내용

영속성 어댑터는 의존성 역전 원칙을 통해 애플리케이션 코어의 플러그인으로 구현되며, 인터페이스 분리 원칙에 따라 좁은 포트 인터페이스를 제공하고, 도메인 모델과 데이터베이스 모델 간의 매핑을 담당하여 도메인 로직을 영속성 세부사항으로부터 독립시킨다.

## 핵심 내용

### 핵심 개념들
- **의존성 역전(Dependency Inversion)** → 상세 내용: 의존성 역전 섹션
- **포트 인터페이스 슬라이싱(Slicing Port Interfaces)** → 상세 내용: 포트 인터페이스 슬라이싱 섹션
- **영속성 어댑터 슬라이싱(Slicing Persistence Adapters)** → 상세 내용: 영속성 어댑터 슬라이싱 섹션
- **도메인 모델과 영속성 모델 간 매핑(Domain-Persistence Mapping)** → 상세 내용: Spring Data JPA 예제 섹션

### 핵심 개념 설명

**의존성 역전** (참조: 페이지 52-53, 라인 9-31)
- 영속성 어댑터는 애플리케이션 서비스에 영속성 기능을 제공하는 "driven" 또는 "outgoing" 어댑터
- 애플리케이션 서비스는 포트 인터페이스를 통해 영속성 기능에 접근
- 포트는 애플리케이션 서비스와 영속성 코드 사이의 간접 계층으로 작동하여 도메인 코드를 영속성 세부사항으로부터 독립시킴
- 포트 계약이 충족되는 한 영속성 어댑터 내부를 자유롭게 변경 가능
- 관계: **포트 인터페이스 슬라이싱**과 **영속성 어댑터 슬라이싱**을 가능하게 하는 아키텍처 원칙

**포트 인터페이스 슬라이싱** (참조: 페이지 54-55, 라인 67-104)
- 인터페이스 분리 원칙(Interface Segregation Principle)을 적용하여 넓은 인터페이스를 특화된 인터페이스로 분할
- 각 서비스는 실제로 필요한 메서드만 의존하여 불필요한 의존성 제거
- "메서드 하나당 포트 하나" 접근 방식으로 플러그 앤 플레이 경험 제공
- 테스트 시 어떤 메서드를 모킹할지 명확해짐
- 관계: **의존성 역전**을 구현하며, **영속성 어댑터 슬라이싱**과 함께 유연한 영속성 계층 구성

**영속성 어댑터 슬라이싱** (참조: 페이지 55-57, 라인 105-137)
- 단일 영속성 어댑터 클래스 대신 여러 어댑터 클래스 생성 가능
- 도메인 클래스(또는 DDD의 애그리게이트)별로 하나의 영속성 어댑터 구현
- JPA와 플레인 SQL을 혼합 사용하는 등 기술별로 어댑터 분리 가능
- Bounded Context별로 전용 영속성 어댑터를 두어 명확한 경계 형성
- 관계: **의존성 역전**과 **포트 인터페이스 슬라이싱**을 활용하여 유연한 구조 제공

**도메인 모델과 영속성 모델 간 매핑** (참조: 페이지 58-62, 라인 147-483)
- 도메인 엔티티(Account)와 JPA 엔티티(AccountJpaEntity, ActivityJpaEntity) 간 분리
- 도메인 모델은 불변성과 유효성 검증을 통해 풍부한 비즈니스 로직 포함
- JPA 엔티티는 데이터베이스 테이블 구조 반영
- 매핑을 통해 JPA의 제약(no-args constructor 등)으로부터 도메인 모델 보호
- 관계: **의존성 역전**의 실제 구현으로, 도메인 로직과 영속성 기술의 완전한 분리 달성

### 핵심 개념 간 관계

**의존성 역전**은 영속성 어댑터 아키텍처의 기반 원칙이며, **포트 인터페이스 슬라이싱**은 이를 효과적으로 구현하기 위한 설계 기법입니다. **영속성 어댑터 슬라이싱**은 물리적인 구현 단위를 정의하며, **도메인 모델과 영속성 모델 간 매핑**은 이 모든 것을 실제 코드로 구체화합니다. 네 개념이 함께 작동하여 유지보수 가능하고 테스트 가능한 영속성 계층을 구성합니다.

## 상세 내용

### 목차
1. [의존성 역전](#1-의존성-역전)
2. [영속성 어댑터의 책임](#2-영속성-어댑터의-책임)
3. [포트 인터페이스 슬라이싱](#3-포트-인터페이스-슬라이싱)
4. [영속성 어댑터 슬라이싱](#4-영속성-어댑터-슬라이싱)
5. [Spring Data JPA 예제](#5-spring-data-jpa-예제)
6. [데이터베이스 트랜잭션 처리](#6-데이터베이스-트랜잭션-처리)
7. [유지보수 가능한 소프트웨어 구축 방법](#7-유지보수-가능한-소프트웨어-구축-방법)

---

### 1. 의존성 역전
(참조: 페이지 52-53, 라인 9-31)
→ 핵심 개념: **의존성 역전**

#### 전통적인 계층 아키텍처의 문제점

1장에서 전통적인 계층 아키텍처가 "데이터베이스 중심 설계"를 지원한다고 비판했습니다. 모든 것이 결국 영속성 계층에 의존하기 때문입니다. 이 장에서는 영속성 계층을 애플리케이션 계층의 플러그인으로 만들어 이 의존성을 역전시키는 방법을 살펴봅니다.

#### 영속성 어댑터와 포트

영속성 계층 대신 애플리케이션 서비스에 영속성 기능을 제공하는 영속성 어댑터에 대해 이야기하겠습니다. 의존성 역전 원칙을 적용하여 이를 수행할 수 있습니다.

애플리케이션 서비스는 영속성 기능에 접근하기 위해 포트 인터페이스를 호출합니다. 이러한 포트는 실제 영속성 작업을 수행하고 데이터베이스와 통신하는 책임을 가진 영속성 어댑터 클래스에 의해 구현됩니다.

Hexagonal Architecture 용어로, 영속성 어댑터는 "driven" 또는 "outgoing" 어댑터입니다. 우리의 애플리케이션에 의해 호출되지 그 반대가 아니기 때문입니다.

#### 간접 계층의 목적

포트는 효과적으로 애플리케이션 서비스와 영속성 코드 사이의 간접 계층입니다. 영속성 계층에 대한 코드 의존성 없이, 즉 영속성 문제를 생각할 필요 없이 도메인 코드를 발전시킬 수 있도록 이 간접 계층을 추가하고 있다는 것을 상기시켜 봅시다. 영속성 코드의 리팩터링이 반드시 코어의 코드 변경으로 이어지지는 않습니다.

당연히 런타임에는 애플리케이션 코어에서 영속성 어댑터로의 의존성이 여전히 존재합니다. 예를 들어 영속성 계층의 코드를 수정하고 버그를 도입하면 애플리케이션 코어의 기능이 여전히 손상될 수 있습니다. 하지만 포트의 계약이 충족되는 한 코어에 영향을 주지 않고 영속성 어댑터에서 원하는 대로 자유롭게 작업할 수 있습니다.

---

### 2. 영속성 어댑터의 책임
(참조: 페이지 53, 라인 32-62)
→ 이전 화제와의 관계: **의존성 역전**에서 정의한 영속성 어댑터의 아키텍처적 역할을 구체적인 책임 목록으로 상세화

#### 영속성 어댑터의 5가지 책임

영속성 어댑터가 일반적으로 수행하는 작업을 살펴봅시다:

1. **입력 받기**
2. **입력을 데이터베이스 형식으로 매핑**
3. **데이터베이스로 입력 전송**
4. **데이터베이스 출력을 애플리케이션 형식으로 매핑**
5. **출력 반환**

#### 각 책임의 상세 설명

**1. 입력 받기**
영속성 어댑터는 포트 인터페이스를 통해 입력을 받습니다. 입력 모델은 인터페이스에서 지정한 대로 도메인 엔티티 또는 특정 데이터베이스 작업 전용 객체일 수 있습니다.

**2-3. 데이터베이스 형식으로 매핑 및 전송**
그런 다음 데이터베이스를 수정하거나 쿼리하기 위해 작업할 수 있는 형식으로 입력 모델을 매핑합니다. Java 프로젝트에서는 일반적으로 JPA(Java Persistence API)를 사용하여 데이터베이스와 통신하므로 데이터베이스 테이블의 구조를 반영하는 JPA 엔티티 객체로 입력을 매핑할 수 있습니다. 맥락에 따라 입력 모델을 JPA 엔티티로 매핑하는 것이 많은 작업이 될 수 있으므로 8장 "경계 간 매핑"에서 매핑 없는 전략에 대해 이야기하겠습니다.

JPA 또는 다른 객체 관계 매핑 프레임워크를 사용하는 대신 데이터베이스와 통신하기 위한 다른 기술을 사용할 수 있습니다. 입력 모델을 플레인 SQL 문으로 매핑하여 이러한 문을 데이터베이스로 보내거나 들어오는 데이터를 파일로 직렬화하여 거기서 다시 읽을 수 있습니다.

중요한 부분은 영속성 어댑터의 입력 모델이 영속성 어댑터 자체가 아닌 애플리케이션 코어 내에 있다는 것입니다. 따라서 영속성 어댑터의 변경이 코어에 영향을 미치지 않습니다.

**4-5. 애플리케이션 형식으로 매핑 및 반환**
다음으로 영속성 어댑터는 데이터베이스를 쿼리하고 쿼리 결과를 받습니다.

마지막으로 데이터베이스 응답을 포트가 기대하는 출력 모델로 매핑하고 반환합니다. 다시 말하지만, 출력 모델이 영속성 어댑터가 아닌 애플리케이션 코어 내에 있다는 것이 중요합니다.

#### 전통적인 영속성 계층과의 비교

입력 및 출력 모델이 영속성 어댑터 자체가 아닌 애플리케이션 코어에 있다는 사실을 제외하면, 책임은 전통적인 영속성 계층의 책임과 크게 다르지 않습니다.

그러나 위에서 설명한 대로 영속성 어댑터를 구현하면 전통적인 영속성 계층을 구현할 때는 아마도 묻지 않았을 몇 가지 질문이 불가피하게 제기됩니다. 전통적인 방식에 너무 익숙해서 그것에 대해 생각하지 않기 때문입니다.

---

### 3. 포트 인터페이스 슬라이싱
(참조: 페이지 54-55, 라인 67-104)
→ 핵심 개념: **포트 인터페이스 슬라이싱**
→ 이전 화제와의 관계: **영속성 어댑터의 책임**을 효과적으로 분할하기 위한 인터페이스 설계 기법

#### 단일 넓은 리포지토리의 문제점

서비스를 구현할 때 애플리케이션 코어에서 사용할 수 있는 데이터베이스 작업을 정의하는 포트 인터페이스를 어떻게 슬라이스할지가 떠오릅니다.

일반적인 관행은 특정 엔티티에 대한 모든 데이터베이스 작업을 제공하는 단일 리포지토리 인터페이스를 만드는 것입니다.

데이터베이스 작업에 의존하는 각 서비스는 이 단일 "넓은" 포트 인터페이스에 대한 의존성을 가지며, 인터페이스에서 단일 메서드만 사용하더라도 마찬가지입니다. 이는 코드베이스에 불필요한 의존성이 있다는 것을 의미합니다.

#### 불필요한 의존성의 문제

우리 맥락에서 필요하지 않은 메서드에 대한 의존성은 코드를 이해하고 테스트하기 어렵게 만듭니다. 위 그림의 RegisterAccountService에 대한 단위 테스트를 작성한다고 상상해보십시오. AccountRepository 인터페이스의 어떤 메서드를 모킹해야 할까요? 먼저 서비스가 실제로 호출하는 AccountRepository 메서드를 찾아야 합니다. 인터페이스의 일부만 모킹하면 테스트를 작업하는 다음 사람이 인터페이스가 완전히 모킹되었을 것으로 예상하고 오류에 부딪힐 수 있는 다른 문제가 발생할 수 있습니다. 따라서 그 사람도 다시 조사를 해야 합니다.

Martin C. Robert의 말을 인용하자면:

> 필요하지 않은 것을 가져오는 것에 의존하면 예상하지 못한 문제가 발생할 수 있습니다.

#### 인터페이스 분리 원칙 적용

인터페이스 분리 원칙(Interface Segregation Principle)이 이 문제에 대한 답을 제공합니다. 클라이언트가 필요한 메서드만 알도록 넓은 인터페이스를 특화된 인터페이스로 분할해야 한다고 명시합니다.

outgoing 포트에 이를 적용하면 다음과 같은 결과를 얻을 수 있습니다:

각 서비스는 이제 실제로 필요한 메서드에만 의존합니다. 게다가 포트의 이름은 그것이 무엇에 관한 것인지 명확하게 나타냅니다. 테스트에서 더 이상 어떤 메서드를 모킹해야 할지 생각할 필요가 없습니다. 대부분의 경우 포트당 하나의 메서드만 있기 때문입니다.

#### 플러그 앤 플레이 경험

이와 같은 매우 좁은 포트를 사용하면 코딩이 플러그 앤 플레이 경험이 됩니다. 서비스를 작업할 때 필요한 포트를 "플러그인"하기만 하면 됩니다. 가지고 다닐 짐이 없습니다.

물론 "포트당 하나의 메서드" 접근 방식이 모든 상황에 적용되지 않을 수 있습니다. 매우 응집력 있고 자주 함께 사용되는 데이터베이스 작업 그룹이 있어 단일 인터페이스로 묶고 싶을 수 있습니다.

---

### 4. 영속성 어댑터 슬라이싱
(참조: 페이지 55-57, 라인 105-137)
→ 핵심 개념: **영속성 어댑터 슬라이싱**
→ 이전 화제와의 관계: **포트 인터페이스 슬라이싱**의 물리적 구현으로, 인터페이스 분할을 실제 클래스 구조로 구체화

#### 여러 영속성 어댑터 클래스

위 그림들에서 모든 영속성 포트를 구현하는 단일 영속성 어댑터 클래스를 보았습니다. 그러나 모든 영속성 포트가 구현되는 한, 하나 이상의 클래스를 만드는 것을 금지하는 규칙은 없습니다.

#### 애그리게이트별 영속성 어댑터

예를 들어, 영속성 작업이 필요한 도메인 클래스(또는 DDD 용어로 "애그리게이트")당 하나의 영속성 어댑터를 구현하도록 선택할 수 있습니다.

이렇게 하면 영속성 어댑터가 영속성 기능으로 지원하는 도메인의 이음새를 따라 자동으로 슬라이스됩니다.

#### 기술별 영속성 어댑터

영속성 어댑터를 더 많은 클래스로 분할할 수 있습니다. 예를 들어 JPA 또는 다른 OR-Mapper를 사용하여 몇 가지 영속성 포트를 구현하고 더 나은 성능을 위해 플레인 SQL을 사용하여 다른 일부 포트를 구현하려는 경우입니다. 그런 다음 각각 영속성 포트의 하위 집합을 구현하는 하나의 JPA 어댑터와 하나의 플레인 SQL 어댑터를 만들 수 있습니다.

도메인 코드는 영속성 포트가 정의한 계약을 궁극적으로 어떤 클래스가 충족하는지 신경 쓰지 않는다는 것을 기억하십시오. 모든 포트가 구현되는 한 영속성 계층에서 적합하다고 생각하는 대로 자유롭게 수행할 수 있습니다.

#### Bounded Context와의 관계

"애그리게이트당 하나의 영속성 어댑터" 접근 방식은 향후 여러 Bounded Context에 대한 영속성 요구 사항을 분리하기 위한 좋은 기반이기도 합니다. 시간이 지나면 청구와 관련된 유스케이스를 담당하는 Bounded Context를 식별한다고 가정해봅시다.

각 Bounded Context에는 자체 영속성 어댑터가 있습니다(위에서 설명한 대로 둘 이상일 수도 있음). "bounded context"라는 용어는 경계를 의미하며, 이는 계정 컨텍스트의 서비스가 청구 컨텍스트의 영속성 어댑터에 접근할 수 없으며 그 반대도 마찬가지임을 의미합니다. 한 컨텍스트가 다른 컨텍스트의 무언가를 필요로 하면 전용 incoming 포트를 통해 접근할 수 있습니다.

---

### 5. Spring Data JPA 예제
(참조: 페이지 57-62, 라인 138-483)
→ 핵심 개념: **도메인 모델과 영속성 모델 간 매핑**
→ 이전 화제와의 관계: **영속성 어댑터 슬라이싱**의 구체적 구현 예제로, 실제 코드를 통한 개념 실현

#### Account 도메인 엔티티

위 그림의 AccountPersistenceAdapter를 구현하는 코드 예제를 살펴봅시다. 이 어댑터는 계정을 데이터베이스에 저장하고 로드해야 합니다. 4장 "유스케이스 구현"에서 이미 Account 엔티티를 보았지만 참조용으로 골격을 다시 소개합니다:

```java
// 참조: 페이지 58, 라인 147-208
package buckpal.domain;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Account {

    @Getter private final AccountId id;
    @Getter private final ActivityWindow activityWindow;
    private final Money baselineBalance;

    // ID 없이 새 Account 생성 (신규 계정용)
    public static Account withoutId(
        Money baselineBalance,
        ActivityWindow activityWindow) {
        return new Account(null, baselineBalance, activityWindow);
    }

    // ID와 함께 Account 생성 (기존 계정 로드용)
    public static Account withId(
        AccountId accountId,
        Money baselineBalance,
        ActivityWindow activityWindow) {
        return new Account(accountId, baselineBalance, activityWindow);
    }

    // 현재 잔액 계산
    public Money calculateBalance() {
        // 구현...
    }

    // 출금 처리 및 검증
    public boolean withdraw(Money money, AccountId targetAccountId) {
        // 구현...
    }

    // 입금 처리
    public boolean deposit(Money money, AccountId sourceAccountId) {
        // 구현...
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from typing import Optional

# 참조: 페이지 58, 라인 147-208
@dataclass(frozen=True)  # 불변성 보장
class Account:
    """도메인 엔티티로서 비즈니스 로직과 불변성을 포함"""
    id: Optional['AccountId']
    activity_window: 'ActivityWindow'
    baseline_balance: 'Money'

    @classmethod
    def without_id(cls, baseline_balance: 'Money',
                   activity_window: 'ActivityWindow') -> 'Account':
        """ID 없이 새 Account 생성 (신규 계정용)"""
        return cls(id=None, baseline_balance=baseline_balance,
                  activity_window=activity_window)

    @classmethod
    def with_id(cls, account_id: 'AccountId', baseline_balance: 'Money',
                activity_window: 'ActivityWindow') -> 'Account':
        """ID와 함께 Account 생성 (기존 계정 로드용)"""
        return cls(id=account_id, baseline_balance=baseline_balance,
                  activity_window=activity_window)

    def calculate_balance(self) -> 'Money':
        """현재 잔액 계산"""
        # 구현...
        pass

    def withdraw(self, money: 'Money', target_account_id: 'AccountId') -> bool:
        """출금 처리 및 검증"""
        # 잔액 검증 후 출금
        # 구현...
        pass

    def deposit(self, money: 'Money', source_account_id: 'AccountId') -> bool:
        """입금 처리"""
        # 구현...
        pass
```

Account 클래스는 getter와 setter가 있는 단순한 데이터 클래스가 아니라 가능한 한 불변성을 유지하려고 시도합니다. 유효한 상태의 Account를 생성하는 팩토리 메서드만 제공하고 모든 변경 메서드는 출금 전 계정 잔액 확인과 같은 검증을 수행하므로 유효하지 않은 도메인 모델을 만들 수 없습니다.

#### JPA 엔티티 클래스

데이터베이스와 통신하기 위해 Spring Data JPA를 사용할 것이므로 계정의 데이터베이스 상태를 나타내는 @Entity 주석이 달린 클래스도 필요합니다:

```java
// 참조: 페이지 59, 라인 219-279
package buckpal.adapter.persistence;

// Account 테이블 매핑
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

// Activity 테이블 매핑
@Entity
@Table(name = "activity")
@Data
@AllArgsConstructor
@NoArgsConstructor
class ActivityJpaEntity {
    @Id
    @GeneratedValue
    private Long id;

    @Column private LocalDateTime timestamp;       // 활동 시간
    @Column private Long ownerAccountId;           // 소유 계정 ID
    @Column private Long sourceAccountId;          // 출금 계정 ID
    @Column private Long targetAccountId;          // 입금 계정 ID
    @Column private Long amount;                   // 금액
}
```

```python
# Python 버전 (SQLAlchemy 사용)
from sqlalchemy import Column, Integer, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

# 참조: 페이지 59, 라인 219-279
Base = declarative_base()

# Account 테이블 매핑
class AccountJpaEntity(Base):
    """JPA 엔티티로서 데이터베이스 테이블 구조 반영"""
    __tablename__ = 'account'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

# Activity 테이블 매핑
class ActivityJpaEntity(Base):
    """활동 내역을 저장하는 JPA 엔티티"""
    __tablename__ = 'activity'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)              # 활동 시간
    owner_account_id = Column(BigInteger)     # 소유 계정 ID
    source_account_id = Column(BigInteger)    # 출금 계정 ID
    target_account_id = Column(BigInteger)    # 입금 계정 ID
    amount = Column(BigInteger)               # 금액
```

이 단계에서 계정의 상태는 단지 ID로 구성됩니다. 나중에 사용자 ID와 같은 추가 필드가 추가될 수 있습니다. 더 흥미로운 것은 특정 계정에 대한 모든 활동을 포함하는 ActivityJpaEntity입니다. JPA의 @ManyToOne 또는 @OneToMany 주석을 통해 ActivityJpaEntity를 AccountJpaEntity와 연결하여 그들 사이의 관계를 표시할 수 있었지만, 데이터베이스 쿼리에 부작용을 추가하므로 지금은 이를 생략하기로 했습니다. 사실 이 단계에서는 JPA보다 더 간단한 객체 관계 매퍼를 사용하여 영속성 어댑터를 구현하는 것이 더 쉬울 것이지만, 미래에 필요할 수 있다고 생각하기 때문에 어쨌든 사용합니다.

#### Spring Data 리포지토리

다음으로 Spring Data를 사용하여 기본 CRUD 기능과 데이터베이스에서 특정 활동을 로드하는 사용자 정의 쿼리를 즉시 제공하는 리포지토리 인터페이스를 만듭니다:

```java
// 참조: 페이지 60, 라인 293-344
// Account 리포지토리 - 기본 CRUD 제공
interface AccountRepository extends JpaRepository<AccountJpaEntity, Long> {
}

// Activity 리포지토리 - 기본 CRUD + 사용자 정의 쿼리
interface ActivityRepository extends JpaRepository<ActivityJpaEntity, Long> {

    // 특정 시점 이후의 활동 조회
    @Query("select a from ActivityJpaEntity a " +
           "where a.ownerAccountId = :ownerAccountId " +
           "and a.timestamp >= :since")
    List<ActivityJpaEntity> findByOwnerSince(
        @Param("ownerAccountId") Long ownerAccountId,
        @Param("since") LocalDateTime since);

    // 특정 시점까지의 입금 총액 계산
    @Query("select sum(a.amount) from ActivityJpaEntity a " +
           "where a.targetAccountId = :accountId " +
           "and a.ownerAccountId = :accountId " +
           "and a.timestamp < :until")
    Long getDepositBalanceUntil(
        @Param("accountId") Long accountId,
        @Param("until") LocalDateTime until);

    // 특정 시점까지의 출금 총액 계산
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
# Python 버전 (SQLAlchemy + 리포지토리 패턴)
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

# 참조: 페이지 60, 라인 293-344
class ActivityRepository:
    """Activity 엔티티를 위한 리포지토리"""

    def __init__(self, session: Session):
        self.session = session

    def find_by_owner_since(self, owner_account_id: int,
                           since: datetime) -> List[ActivityJpaEntity]:
        """특정 시점 이후의 활동 조회"""
        return self.session.query(ActivityJpaEntity).filter(
            ActivityJpaEntity.owner_account_id == owner_account_id,
            ActivityJpaEntity.timestamp >= since
        ).all()

    def get_deposit_balance_until(self, account_id: int,
                                  until: datetime) -> int:
        """특정 시점까지의 입금 총액 계산"""
        result = self.session.query(
            func.sum(ActivityJpaEntity.amount)
        ).filter(
            ActivityJpaEntity.target_account_id == account_id,
            ActivityJpaEntity.owner_account_id == account_id,
            ActivityJpaEntity.timestamp < until
        ).scalar()
        return result or 0

    def get_withdrawal_balance_until(self, account_id: int,
                                     until: datetime) -> int:
        """특정 시점까지의 출금 총액 계산"""
        result = self.session.query(
            func.sum(ActivityJpaEntity.amount)
        ).filter(
            ActivityJpaEntity.source_account_id == account_id,
            ActivityJpaEntity.owner_account_id == account_id,
            ActivityJpaEntity.timestamp < until
        ).scalar()
        return result or 0
```

Spring Boot는 이러한 리포지토리를 자동으로 찾고 Spring Data는 실제로 데이터베이스와 통신하는 리포지토리 인터페이스 뒤에 구현을 제공하기 위해 마법을 부립니다.

#### 영속성 어댑터 구현

JPA 엔티티와 리포지토리가 준비되면 애플리케이션에 영속성 기능을 제공하는 영속성 어댑터를 구현할 수 있습니다:

```java
// 참조: 페이지 61-62, 라인 356-461
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

        // 1. Account 엔티티 로드
        AccountJpaEntity account =
            accountRepository.findById(accountId.getValue())
                .orElseThrow(EntityNotFoundException::new);

        // 2. 특정 시점 이후의 활동 로드
        List<ActivityJpaEntity> activities =
            activityRepository.findByOwnerSince(
                accountId.getValue(),
                baselineDate);

        // 3. 기준 시점까지의 출금 총액 계산
        Long withdrawalBalance = orZero(activityRepository
            .getWithdrawalBalanceUntil(
                accountId.getValue(),
                baselineDate));

        // 4. 기준 시점까지의 입금 총액 계산
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
        // 새로운 활동만 저장 (ID가 null인 활동)
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

# 참조: 페이지 61-62, 라인 356-461
class AccountPersistenceAdapter:
    """영속성 기능을 제공하는 어댑터"""

    def __init__(self, account_repository, activity_repository, account_mapper):
        self.account_repository = account_repository
        self.activity_repository = activity_repository
        self.account_mapper = account_mapper

    def load_account(self, account_id: 'AccountId',
                    baseline_date: datetime) -> 'Account':
        """계정을 데이터베이스에서 로드"""

        # 1. Account 엔티티 로드
        account = self.account_repository.find_by_id(account_id.value)
        if not account:
            raise EntityNotFoundException()

        # 2. 특정 시점 이후의 활동 로드
        activities = self.activity_repository.find_by_owner_since(
            account_id.value,
            baseline_date
        )

        # 3. 기준 시점까지의 출금 총액 계산
        withdrawal_balance = self.activity_repository.get_withdrawal_balance_until(
            account_id.value,
            baseline_date
        )

        # 4. 기준 시점까지의 입금 총액 계산
        deposit_balance = self.activity_repository.get_deposit_balance_until(
            account_id.value,
            baseline_date
        )

        # 5. 도메인 엔티티로 매핑하여 반환
        return self.account_mapper.map_to_domain_entity(
            account,
            activities,
            withdrawal_balance,
            deposit_balance
        )

    def update_activities(self, account: 'Account') -> None:
        """계정의 새로운 활동을 저장"""
        # 새로운 활동만 저장 (ID가 None인 활동)
        for activity in account.activity_window.activities:
            if activity.id is None:
                jpa_entity = self.account_mapper.map_to_jpa_entity(activity)
                self.activity_repository.save(jpa_entity)
```

영속성 어댑터는 애플리케이션에 필요한 두 개의 포트인 LoadAccountPort와 UpdateAccountStatePort를 구현합니다.

데이터베이스에서 계정을 로드하기 위해 AccountRepository에서 로드하고 ActivityRepository를 통해 특정 시간 창에 대한 이 계정의 활동을 로드합니다.

유효한 Account 도메인 엔티티를 생성하려면 이 활동 창이 시작되기 전에 계정이 가졌던 잔액도 필요하므로 데이터베이스에서 이 계정의 모든 출금 및 입금 합계를 가져옵니다.

마지막으로 이 모든 데이터를 Account 도메인 엔티티로 매핑하고 호출자에게 반환합니다.

계정의 상태를 업데이트하기 위해 Account 엔티티의 모든 활동을 반복하고 ID가 있는지 확인합니다. ID가 없으면 새로운 활동이므로 ActivityRepository를 통해 지속합니다.

#### 매핑의 필요성

위에서 설명한 시나리오에서 Account 및 Activity 도메인 모델과 AccountJpaEntity 및 ActivityJpaEntity 데이터베이스 모델 사이에 양방향 매핑이 있습니다. 왜 앞뒤로 매핑하는 수고를 할까요? Account 및 Activity 클래스로 JPA 주석을 옮기고 데이터베이스에 엔티티를 직접 저장할 수 없을까요?

이러한 "매핑 없음" 전략은 8장 "경계 간 매핑"에서 매핑 전략에 대해 이야기할 때 보게 될 유효한 선택일 수 있습니다. 그러나 JPA는 도메인 모델에서 타협을 강요합니다. 예를 들어 JPA는 엔티티가 no-args 생성자를 가져야 합니다. 또는 영속성 계층에서 @ManyToOne 관계가 성능 관점에서 의미가 있을 수 있지만 도메인 모델에서는 어쨌든 데이터의 일부만 로드하기 때문에 이 관계가 반대 방향이기를 원할 수 있습니다.

따라서 기본 영속성과 타협 없이 풍부한 도메인 모델을 만들고 싶다면 도메인 모델과 영속성 모델 사이를 매핑해야 합니다.

---

### 6. 데이터베이스 트랜잭션 처리
(참조: 페이지 63, 라인 488-511)
→ 이전 화제와의 관계: **Spring Data JPA 예제**의 실무적 고려사항으로, 트랜잭션 관리 책임 배치

#### 트랜잭션 경계의 위치

아직 데이터베이스 트랜잭션 주제를 다루지 않았습니다. 트랜잭션 경계를 어디에 둘까요?

트랜잭션은 특정 유스케이스 내에서 수행되는 모든 쓰기 작업을 포괄해야 하므로 그 중 하나가 실패하면 모든 작업을 함께 롤백할 수 있습니다.

영속성 어댑터는 어떤 다른 데이터베이스 작업이 동일한 유스케이스의 일부인지 알 수 없으므로 트랜잭션을 언제 열고 닫을지 결정할 수 없습니다. 이 책임을 영속성 어댑터 호출을 조율하는 서비스에 위임해야 합니다.

#### Spring의 @Transactional 사용

Java와 Spring으로 이를 수행하는 가장 쉬운 방법은 애플리케이션 서비스 클래스에 @Transactional 주석을 추가하여 Spring이 모든 public 메서드를 트랜잭션으로 래핑하도록 하는 것입니다:

```java
// 참조: 페이지 63, 라인 498-508
package buckpal.application.service;

@Transactional  // 모든 public 메서드를 트랜잭션으로 래핑
public class SendMoneyService implements SendMoneyUseCase {
    // 구현...
}
```

```python
# Python 버전 (데코레이터 사용)
from contextlib import contextmanager

# 참조: 페이지 63, 라인 498-508
def transactional(func):
    """트랜잭션 데코레이터"""
    def wrapper(*args, **kwargs):
        session = get_session()
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    return wrapper

class SendMoneyService:
    """모든 메서드가 트랜잭션으로 실행됨"""

    @transactional
    def send_money(self, command):
        # 구현...
        pass
```

#### AspectJ를 통한 대안

서비스를 순수하게 유지하고 @Transactional 주석으로 더럽히지 않으려면 AspectJ와 같은 관점 지향 프로그래밍을 사용하여 코드베이스에 트랜잭션 경계를 짜 넣을 수 있습니다.

---

### 7. 유지보수 가능한 소프트웨어 구축 방법
(참조: 페이지 63, 라인 512-517)
→ 이전 화제와의 관계: 앞서 다룬 모든 개념들을 종합하여 실무 적용 원칙 제시

#### 도메인 코드의 자유

도메인 코드의 플러그인 역할을 하는 영속성 어댑터를 구축하면 영속성 세부사항으로부터 도메인 코드를 자유롭게 하여 풍부한 도메인 모델을 구축할 수 있습니다.

#### 포트의 유연성

좁은 포트 인터페이스를 사용하여 하나의 포트를 이런 방식으로 구현하고 다른 포트를 저런 방식으로, 심지어 다른 영속성 기술을 사용하여 구현할 수 있는 유연성을 가지며, 애플리케이션은 이를 알아차리지 못합니다. 포트 계약이 준수되는 한 완전한 영속성 계층도 교체할 수 있습니다.
