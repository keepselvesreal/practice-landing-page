# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter 7: Testing Architecture Elements

## 압축 내용

테스트 피라미드에 따라 도메인 엔티티는 단위 테스트로, 유스케이스는 모킹을 활용한 단위 테스트로, 어댑터는 프레임워크와 통합된 통합 테스트로, 핵심 시나리오는 시스템 테스트로 커버하며, 테스트 성공은 배포에 대한 자신감으로 측정하고 프로덕션 버그로부터 지속적으로 학습한다.

## 핵심 내용

### 핵심 개념들
- **테스트 피라미드(Test Pyramid)** → 상세 내용: 테스트 피라미드 섹션
- **단위 테스트(Unit Tests)** → 상세 내용: 도메인 엔티티 테스트, 유스케이스 테스트 섹션
- **통합 테스트(Integration Tests)** → 상세 내용: 웹 어댑터 테스트, 영속성 어댑터 테스트 섹션
- **시스템 테스트(System Tests)** → 상세 내용: 시스템 테스트 섹션
- **테스트 전략과 측정(Testing Strategy)** → 상세 내용: 충분한 테스트 섹션

### 핵심 개념 설명

**테스트 피라미드** (참조: 페이지 64-65, 라인 9-45)
- 세분화된 저비용 테스트(단위 테스트)를 높은 커버리지로 작성하고, 고비용 테스트는 낮은 커버리지로 작성
- 계층별 정의: 단위 테스트(단일 클래스), 통합 테스트(여러 유닛의 네트워크), 시스템 테스트(전체 애플리케이션)
- 비용 요소: 구축 비용, 유지보수 비용, 실행 속도, 안정성
- 관계: **단위 테스트**, **통합 테스트**, **시스템 테스트**의 비율과 목적을 정의하는 메타 원칙

**단위 테스트** (참조: 페이지 65-68, 라인 46-213)
- 단일 클래스를 인스턴스화하고 인터페이스를 통해 기능 검증
- 의존성은 실제 클래스 대신 모킹으로 대체
- 도메인 엔티티: 비즈니스 규칙 검증에 최적, 빠르고 간단
- 유스케이스: Mockito 활용, 상호작용 검증, 구조 변경에 취약할 수 있음
- 관계: **테스트 피라미드**의 기반이며, **통합 테스트**보다 우선 적용

**통합 테스트** (참조: 페이지 68-71, 라인 214-408)
- 여러 유닛의 네트워크를 인스턴스화하고 진입 클래스의 인터페이스를 통해 데이터 전송
- 두 계층 간 경계를 넘나들며, 일부는 모킹
- 웹 어댑터: Spring의 @WebMvcTest, JSON 매핑, HTTP 응답 검증
- 영속성 어댑터: Spring의 @DataJpaTest, 실제 데이터베이스 사용, Testcontainers 권장
- 관계: **단위 테스트**보다 비용이 높지만 프레임워크 통합을 검증하며, **시스템 테스트**의 기반

**시스템 테스트** (참조: 페이지 71-74, 라인 409-547)
- 전체 애플리케이션을 시작하고 API를 통해 요청을 실행하여 모든 계층이 함께 작동하는지 검증
- Spring의 @SpringBootTest, 실제 HTTP 프로토콜 사용
- 여러 유스케이스를 조합하여 사용자 시나리오 생성
- 도메인 특화 언어(DSL) 사용으로 가독성 향상 및 도메인 전문가의 피드백 가능
- 관계: **통합 테스트**로 잡지 못하는 계층 간 매핑 오류 등을 발견하며, 배포 자신감 제공

**테스트 전략과 측정** (참조: 페이지 74-75, 라인 548-591)
- 라인 커버리지는 나쁜 지표, 배포에 대한 자신감으로 테스트 성공 측정
- 프로덕션 버그에 대해 "왜 테스트가 이 버그를 잡지 못했는가?" 질문하고 문서화
- 구현 중 테스트 작성으로 개발 도구화, 사후 작성 시 잡무화
- 리팩터링마다 테스트 수정 필요하면 테스트 설계 문제
- 관계: **테스트 피라미드**, **단위 테스트**, **통합 테스트**, **시스템 테스트**를 실무에 적용하는 지침

### 핵심 개념 간 관계

**테스트 피라미드**는 전체 테스트 전략의 메타 원칙으로, **단위 테스트**, **통합 테스트**, **시스템 테스트**의 비율과 목적을 정의합니다. Hexagonal Architecture의 각 요소는 특성에 맞는 테스트 유형으로 커버되며(도메인 엔티티와 유스케이스는 단위 테스트, 어댑터는 통합 테스트, 주요 시나리오는 시스템 테스트), 이 모든 것은 **테스트 전략과 측정** 원칙 하에서 배포 자신감이라는 실무적 목표를 달성합니다.

## 상세 내용

### 목차
1. [테스트 피라미드](#1-테스트-피라미드)
2. [단위 테스트로 도메인 엔티티 테스트](#2-단위-테스트로-도메인-엔티티-테스트)
3. [단위 테스트로 유스케이스 테스트](#3-단위-테스트로-유스케이스-테스트)
4. [통합 테스트로 웹 어댑터 테스트](#4-통합-테스트로-웹-어댑터-테스트)
5. [통합 테스트로 영속성 어댑터 테스트](#5-통합-테스트로-영속성-어댑터-테스트)
6. [시스템 테스트로 주요 경로 테스트](#6-시스템-테스트로-주요-경로-테스트)
7. [얼마나 많은 테스트가 충분한가](#7-얼마나-많은-테스트가-충분한가)
8. [유지보수 가능한 소프트웨어 구축 방법](#8-유지보수-가능한-소프트웨어-구축-방법)

---

### 1. 테스트 피라미드
(참조: 페이지 64-65, 라인 9-45)
→ 핵심 개념: **테스트 피라미드**

#### 테스트 전략의 부재

많은 프로젝트에서 자동화된 테스트는 미스터리입니다. 모든 사람이 위키에 문서화된 일부 낡은 규칙에 의해 요구되기 때문에 적합하다고 생각하는 대로 테스트를 작성하지만, 팀의 테스트 전략에 대한 구체적인 질문에는 아무도 답할 수 없습니다.

이 장은 hexagonal architecture에 대한 테스트 전략을 제공합니다. 아키텍처의 각 요소에 대해 이를 커버하기 위한 테스트 유형을 논의하겠습니다.

#### 테스트 피라미드의 기본 원칙

테스트 피라미드를 따라 테스트에 대한 논의를 시작해봅시다. 이는 얼마나 많은 어떤 유형의 테스트를 목표로 해야 하는지 결정하는 데 도움이 되는 은유입니다.

기본 명제는 구축하기 저렴하고, 유지보수하기 쉽고, 빠르게 실행되고, 안정적인 세분화된 테스트를 높은 커버리지로 가져야 한다는 것입니다. 이것이 단일 "유닛"(보통 클래스)이 예상대로 작동하는지 검증하는 단위 테스트입니다.

테스트가 여러 유닛을 결합하고 유닛 경계, 아키텍처 경계, 심지어 시스템 경계를 넘나들면 구축 비용이 더 많이 들고, 실행 속도가 느려지고, 더 취약해지는(기능 오류 대신 일부 구성 오류로 인해 실패) 경향이 있습니다. 피라미드는 이러한 테스트가 비용이 높아질수록 이러한 테스트의 높은 커버리지를 목표로 하지 말아야 한다고 말합니다. 그렇지 않으면 새로운 기능 대신 테스트를 구축하는 데 너무 많은 시간을 소비하게 됩니다.

#### 테스트 유형의 정의

맥락에 따라 테스트 피라미드는 종종 다른 계층으로 표시됩니다. hexagonal architecture를 테스트하기 위해 논의하기로 선택한 계층을 살펴봅시다. "단위 테스트", "통합 테스트", "시스템 테스트"의 정의는 맥락에 따라 다릅니다. 한 프로젝트에서는 다른 프로젝트와 다른 의미일 수 있습니다. 다음은 이 장에서 사용할 이러한 용어의 해석입니다.

**단위 테스트(Unit Tests)**
피라미드의 기반입니다. 단위 테스트는 일반적으로 단일 클래스를 인스턴스화하고 인터페이스를 통해 기능을 테스트합니다. 테스트 대상 클래스가 다른 클래스에 대한 의존성을 가지고 있으면 해당 다른 클래스는 인스턴스화되지 않고 테스트 중에 필요한 대로 실제 클래스의 동작을 시뮬레이션하는 모킹으로 대체됩니다.

**통합 테스트(Integration Tests)**
피라미드의 다음 계층을 형성합니다. 이러한 테스트는 여러 유닛의 네트워크를 인스턴스화하고 진입 클래스의 인터페이스를 통해 일부 데이터를 보내 이 네트워크가 예상대로 작동하는지 검증합니다. 우리의 해석에서 통합 테스트는 두 계층 간의 경계를 넘나들므로 객체의 네트워크가 완전하지 않거나 어느 시점에서 모킹에 대해 작동해야 합니다.

**시스템 테스트(System Tests)**
마지막으로 애플리케이션을 구성하는 전체 객체 네트워크를 가동하고 특정 유스케이스가 애플리케이션의 모든 계층을 통해 예상대로 작동하는지 검증합니다.

**End-to-End 테스트**
시스템 테스트 위에는 애플리케이션의 UI를 포함하는 end-to-end 테스트 계층이 있을 수 있습니다. 이 책에서는 백엔드 아키텍처만 논의하므로 end-to-end 테스트는 고려하지 않겠습니다.

이제 일부 테스트 유형을 정의했으므로 hexagonal architecture의 각 계층에 가장 적합한 테스트 유형을 살펴봅시다.

---

### 2. 단위 테스트로 도메인 엔티티 테스트
(참조: 페이지 65-66, 라인 46-107)
→ 핵심 개념: **단위 테스트**
→ 이전 화제와의 관계: **테스트 피라미드**의 기반 계층을 도메인 엔티티에 적용

#### Account 엔티티 테스트

아키텍처 중심의 도메인 엔티티를 살펴보는 것으로 시작합니다. 4장 "유스케이스 구현"의 Account 엔티티를 상기해봅시다. Account의 상태는 과거 특정 시점의 잔액(baseline balance)과 그 이후의 입출금 목록(activities)으로 구성됩니다.

이제 withdraw() 메서드가 예상대로 작동하는지 검증하려고 합니다:

```java
// 참조: 페이지 65-66, 라인 52-100
class AccountTest {

    @Test
    void withdrawalSucceeds() {
        // Given: 초기 상태 설정
        AccountId accountId = new AccountId(1L);
        Account account = defaultAccount()
            .withAccountId(accountId)
            .withBaselineBalance(Money.of(555L))  // 기준 잔액: 555
            .withActivityWindow(new ActivityWindow(
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(999L)).build(),  // 입금: 999
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(1L)).build()))   // 입금: 1
            .build();

        // When: 출금 실행
        boolean success = account.withdraw(Money.of(555L), new AccountId(99L));

        // Then: 결과 검증
        assertThat(success).isTrue();                                      // 출금 성공
        assertThat(account.getActivityWindow().getActivities()).hasSize(3); // 활동 3개
        assertThat(account.calculateBalance()).isEqualTo(Money.of(1000L)); // 잔액 1000
    }
}
```

```python
# Python 버전
import pytest

# 참조: 페이지 65-66, 라인 52-100
class TestAccount:

    def test_withdrawal_succeeds(self):
        """출금이 성공적으로 처리되는지 검증"""
        # Given: 초기 상태 설정
        account_id = AccountId(1)
        account = (AccountBuilder()
            .with_account_id(account_id)
            .with_baseline_balance(Money(555))  # 기준 잔액: 555
            .with_activity_window(ActivityWindow([
                ActivityBuilder()
                    .with_target_account(account_id)
                    .with_money(Money(999))      # 입금: 999
                    .build(),
                ActivityBuilder()
                    .with_target_account(account_id)
                    .with_money(Money(1))        # 입금: 1
                    .build()
            ]))
            .build())

        # When: 출금 실행
        success = account.withdraw(Money(555), AccountId(99))

        # Then: 결과 검증
        assert success is True                                    # 출금 성공
        assert len(account.activity_window.activities) == 3       # 활동 3개
        assert account.calculate_balance() == Money(1000)         # 잔액 1000
```

#### 단위 테스트의 특징

위 테스트는 특정 상태의 Account를 인스턴스화하고, withdraw() 메서드를 호출하고, 출금이 성공했는지와 테스트 대상 Account 객체의 상태에 예상된 부작용이 있었는지 검증하는 순수한 단위 테스트입니다.

테스트는 설정하기 매우 쉽고, 이해하기 쉽고, 매우 빠르게 실행됩니다. 테스트가 이보다 훨씬 간단하지 않습니다. 이와 같은 단위 테스트는 도메인 엔티티 내에 인코딩된 비즈니스 규칙을 검증하는 데 가장 좋은 선택입니다. 도메인 엔티티 동작은 다른 클래스에 대한 의존성이 거의 없거나 전혀 없기 때문에 다른 유형의 테스트가 필요하지 않습니다.

---

### 3. 단위 테스트로 유스케이스 테스트
(참조: 페이지 66-68, 라인 108-213)
→ 핵심 개념: **단위 테스트**
→ 이전 화제와의 관계: **도메인 엔티티 테스트**에서 한 계층 외부로 이동하여 유스케이스 계층에 단위 테스트 적용

#### SendMoneyService 테스트

한 계층 외부로 나가 테스트할 다음 아키텍처 요소는 유스케이스입니다. 4장 "유스케이스 구현"에서 논의한 SendMoneyService의 테스트를 살펴봅시다. "Send Money" 유스케이스는 다른 트랜잭션이 그 사이에 잔액을 변경할 수 없도록 소스 Account를 잠급니다. 소스 계정에서 돈을 성공적으로 출금할 수 있으면 대상 계정도 잠그고 거기에 돈을 입금합니다. 마지막으로 두 계정을 다시 잠금 해제합니다.

트랜잭션이 성공할 때 모든 것이 예상대로 작동하는지 검증하려고 합니다:

```java
// 참조: 페이지 66-67, 라인 115-185
class SendMoneyServiceTest {

    // 필드 선언 생략

    @Test
    void transactionSucceeds() {

        // Given: 초기 상태 설정
        Account sourceAccount = givenSourceAccount();
        Account targetAccount = givenTargetAccount();

        givenWithdrawalWillSucceed(sourceAccount);
        givenDepositWillSucceed(targetAccount);

        Money money = Money.of(500L);

        SendMoneyCommand command = new SendMoneyCommand(
            sourceAccount.getId(),
            targetAccount.getId(),
            money);

        // When: 송금 실행
        boolean success = sendMoneyService.sendMoney(command);

        // Then: 성공 여부 검증
        assertThat(success).isTrue();

        AccountId sourceAccountId = sourceAccount.getId();
        AccountId targetAccountId = targetAccount.getId();

        // 소스 계정 처리 순서 검증
        then(accountLock).should().lockAccount(eq(sourceAccountId));        // 1. 잠금
        then(sourceAccount).should().withdraw(eq(money), eq(targetAccountId)); // 2. 출금
        then(accountLock).should().releaseAccount(eq(sourceAccountId));     // 3. 해제

        // 대상 계정 처리 순서 검증
        then(accountLock).should().lockAccount(eq(targetAccountId));        // 4. 잠금
        then(targetAccount).should().deposit(eq(money), eq(sourceAccountId)); // 5. 입금
        then(accountLock).should().releaseAccount(eq(targetAccountId));     // 6. 해제

        // 계정 업데이트 검증
        thenAccountsHaveBeenUpdated(sourceAccountId, targetAccountId);
    }

    // 헬퍼 메서드 생략
}
```

```python
# Python 버전
from unittest.mock import Mock, call
import pytest

# 참조: 페이지 66-67, 라인 115-185
class TestSendMoneyService:

    def test_transaction_succeeds(self):
        """트랜잭션이 성공적으로 처리되는지 검증"""
        # Given: 초기 상태 설정
        source_account = self._given_source_account()
        target_account = self._given_target_account()

        self._given_withdrawal_will_succeed(source_account)
        self._given_deposit_will_succeed(target_account)

        money = Money(500)

        command = SendMoneyCommand(
            source_account.id,
            target_account.id,
            money
        )

        # When: 송금 실행
        success = self.send_money_service.send_money(command)

        # Then: 성공 여부 검증
        assert success is True

        source_account_id = source_account.id
        target_account_id = target_account.id

        # 소스 계정 처리 순서 검증
        assert self.account_lock.lock_account.called_with(source_account_id)      # 1. 잠금
        assert source_account.withdraw.called_with(money, target_account_id)      # 2. 출금
        assert self.account_lock.release_account.called_with(source_account_id)   # 3. 해제

        # 대상 계정 처리 순서 검증
        assert self.account_lock.lock_account.called_with(target_account_id)      # 4. 잠금
        assert target_account.deposit.called_with(money, source_account_id)       # 5. 입금
        assert self.account_lock.release_account.called_with(target_account_id)   # 6. 해제

        # 계정 업데이트 검증
        self._then_accounts_have_been_updated(source_account_id, target_account_id)

    # 헬퍼 메서드 생략
```

#### BDD 스타일의 테스트 구조

테스트를 좀 더 읽기 쉽게 만들기 위해 Behavior-Driven Development에서 일반적으로 사용되는 given/when/then 섹션으로 구조화되어 있습니다.

"given" 섹션에서 소스 및 대상 Account를 생성하고 이름이 given...()으로 시작하는 일부 메서드로 올바른 상태로 만듭니다. 또한 유스케이스에 대한 입력 역할을 할 SendMoneyCommand를 생성합니다. "when" 섹션에서는 단순히 sendMoney() 메서드를 호출하여 유스케이스를 호출합니다. "then" 섹션은 트랜잭션이 성공했는지 확인하고 소스 및 대상 Account와 계정 잠금 및 잠금 해제를 담당하는 AccountLock 인스턴스에서 특정 메서드가 호출되었는지 검증합니다.

#### Mockito를 활용한 모킹

내부적으로 테스트는 Mockito 라이브러리를 사용하여 given...() 메서드에서 모킹 객체를 만듭니다. Mockito는 모킹 객체에서 특정 메서드가 호출되었는지 검증하기 위한 then() 메서드도 제공합니다.

#### 단위 테스트의 한계와 주의사항

테스트 대상 서비스가 상태가 없기 때문에 "then" 섹션에서 특정 상태를 검증할 수 없습니다. 대신 테스트는 서비스가 (모킹된) 의존성의 특정 메서드와 상호작용했는지 검증합니다. 이는 테스트가 테스트 대상 코드의 구조 변경에 취약하고 동작뿐만 아니라는 것을 의미합니다. 결과적으로 테스트 대상 코드가 리팩터링되면 테스트를 수정해야 할 가능성이 더 높습니다.

이를 염두에 두고 테스트에서 실제로 검증하려는 상호작용에 대해 열심히 생각해야 합니다. 위 테스트에서처럼 모든 상호작용을 검증하는 것이 좋은 생각이 아닐 수 있습니다. 대신 가장 중요한 것에 집중해야 합니다. 그렇지 않으면 테스트 대상 클래스의 모든 단일 변경과 함께 테스트를 변경해야 하므로 테스트의 가치가 훼손됩니다.

이 테스트는 여전히 단위 테스트이지만, 의존성과의 상호작용을 테스트하고 있기 때문에 통합 테스트에 가깝습니다. 그러나 모킹으로 작업하고 있고 실제 의존성을 관리할 필요가 없기 때문에 본격적인 통합 테스트보다 생성하고 유지하기가 더 쉽습니다.

---

### 4. 통합 테스트로 웹 어댑터 테스트
(참조: 페이지 68-69, 라인 214-294)
→ 핵심 개념: **통합 테스트**
→ 이전 화제와의 관계: **유스케이스 테스트**에서 한 계층 외부로 이동하여 어댑터 계층에 통합 테스트 적용

#### 웹 어댑터의 책임

또 다른 계층 외부로 이동하면 어댑터에 도착합니다. 웹 어댑터 테스트에 대해 논의해봅시다.

웹 어댑터가 예를 들어 JSON 문자열 형식의 입력을 HTTP를 통해 받고, 그것에 대해 일부 검증을 수행하고, 유스케이스가 예상하는 형식으로 입력을 매핑한 다음 해당 유스케이스로 전달한다는 것을 상기하십시오. 그런 다음 유스케이스의 결과를 받아 JSON으로 직렬화하고 HTTP 응답을 통해 호출자에게 다시 보냅니다.

#### 웹 어댑터 통합 테스트

웹 어댑터 테스트에서 이 모든 단계가 예상대로 작동하는지 확인하려고 합니다:

```java
// 참조: 페이지 68-69, 라인 221-270
@WebMvcTest(controllers = SendMoneyController.class)
class SendMoneyControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SendMoneyUseCase sendMoneyUseCase;

    @Test
    void testSendMoney() throws Exception {

        // When: HTTP 요청 전송
        mockMvc.perform(
            post("/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}",
                41L, 42L, 500)
            .header("Content-Type", "application/json"))
            .andExpect(status().isOk());

        // Then: 유스케이스 호출 검증
        then(sendMoneyUseCase).should()
            .sendMoney(eq(new SendMoneyCommand(
                new AccountId(41L),
                new AccountId(42L),
                Money.of(500L))));
    }
}
```

```python
# Python 버전 (Flask 테스트 예시)
from flask import Flask
from unittest.mock import Mock, patch
import pytest

# 참조: 페이지 68-69, 라인 221-270
class TestSendMoneyController:

    @pytest.fixture
    def client(self):
        """테스트 클라이언트 설정"""
        app = Flask(__name__)
        # 컨트롤러 등록
        app.register_blueprint(send_money_controller)
        return app.test_client()

    def test_send_money(self, client):
        """송금 API가 올바르게 작동하는지 검증"""
        # Given: 유스케이스 모킹
        with patch('controllers.send_money_use_case') as mock_use_case:

            # When: HTTP 요청 전송
            response = client.post(
                '/accounts/sendMoney/41/42/500',
                headers={'Content-Type': 'application/json'}
            )

            # Then: HTTP 응답 검증
            assert response.status_code == 200

            # Then: 유스케이스 호출 검증
            mock_use_case.send_money.assert_called_once_with(
                SendMoneyCommand(
                    AccountId(41),
                    AccountId(42),
                    Money(500)
                )
            )
```

#### Spring Boot 통합 테스트의 특징

위 테스트는 Spring Boot 프레임워크로 구축된 SendMoneyController라는 웹 컨트롤러에 대한 표준 통합 테스트입니다. testSendMoney() 메서드에서 입력 객체를 생성한 다음 모킹 HTTP 요청을 웹 컨트롤러로 보냅니다. 요청 본문에는 JSON 문자열로 입력 객체가 포함되어 있습니다.

isOk() 메서드로 HTTP 응답의 상태가 200인지 검증하고 모킹된 유스케이스 클래스가 호출되었는지 검증합니다.

#### 웹 어댑터의 책임 커버리지

대부분의 웹 어댑터 책임이 이 테스트에 의해 커버됩니다.

MockMvc 객체로 HTTP를 모킹했기 때문에 실제로 HTTP 프로토콜을 통해 테스트하는 것은 아닙니다. 프레임워크가 모든 것을 HTTP로 또는 HTTP에서 제대로 변환한다고 신뢰합니다. 프레임워크를 테스트할 필요는 없습니다.

그러나 JSON에서 SendMoneyCommand 객체로 입력을 매핑하는 전체 경로가 커버됩니다. 4장 "유스케이스 구현"에서 설명한 대로 SendMoneyCommand 객체를 자체 검증 명령으로 구축했다면 이 매핑이 유스케이스에 대한 구문적으로 유효한 입력을 생성하는지까지 확인한 것입니다. 또한 유스케이스가 실제로 호출되고 HTTP 응답이 예상 상태를 가지고 있는지 검증했습니다.

#### 통합 테스트인 이유

그렇다면 왜 이것이 단위 테스트가 아니라 통합 테스트일까요? 이 테스트에서 단일 웹 컨트롤러 클래스만 테스트하는 것처럼 보이지만, 내부적으로 훨씬 더 많은 일이 일어나고 있습니다. @WebMvcTest 주석으로 Spring에게 특정 요청 경로에 응답하고, Java와 JSON 간에 매핑하고, HTTP 입력을 검증하는 등을 담당하는 전체 객체 네트워크를 인스턴스화하도록 지시합니다. 그리고 이 테스트에서 웹 컨트롤러가 이 네트워크의 일부로 작동하는지 검증하고 있습니다.

웹 컨트롤러는 Spring 프레임워크에 강하게 바인딩되어 있으므로 격리된 상태로 테스트하는 대신 이 프레임워크에 통합하여 테스트하는 것이 합리적입니다. 웹 컨트롤러를 순수한 단위 테스트로 테스트했다면 모든 매핑, 검증 및 HTTP 관련 사항의 커버리지를 잃게 되고, 프로덕션에서 실제로 작동하는지 확신할 수 없었을 것입니다. 프로덕션에서는 프레임워크 기계의 톱니바퀴일 뿐이기 때문입니다.

---

### 5. 통합 테스트로 영속성 어댑터 테스트
(참조: 페이지 69-71, 라인 295-408)
→ 핵심 개념: **통합 테스트**
→ 이전 화제와의 관계: **웹 어댑터 테스트**와 동일한 통합 테스트 접근을 영속성 어댑터에 적용

#### 영속성 어댑터 통합 테스트의 필요성

비슷한 이유로 단위 테스트 대신 통합 테스트로 영속성 어댑터를 커버하는 것이 합리적입니다. 어댑터 내의 로직뿐만 아니라 데이터베이스로의 매핑도 검증하고 싶기 때문입니다.

#### AccountPersistenceAdapter 테스트

6장 "영속성 어댑터 구현"에서 구축한 영속성 어댑터를 테스트하려고 합니다. 어댑터에는 데이터베이스에서 Account 엔티티를 로드하는 메서드와 새로운 계정 활동을 데이터베이스에 저장하는 메서드가 있습니다:

```java
// 참조: 페이지 70-71, 라인 306-380
@DataJpaTest
@Import({AccountPersistenceAdapter.class, AccountMapper.class})
class AccountPersistenceAdapterTest {

    @Autowired
    private AccountPersistenceAdapter adapterUnderTest;

    @Autowired
    private ActivityRepository activityRepository;

    @Test
    @Sql("AccountPersistenceAdapterTest.sql")
    void loadsAccount() {
        // When: 계정 로드
        Account account = adapter.loadAccount(
            new AccountId(1L),
            LocalDateTime.of(2018, 8, 10, 0, 0));

        // Then: 로드된 상태 검증
        assertThat(account.getActivityWindow().getActivities()).hasSize(2);
        assertThat(account.calculateBalance()).isEqualTo(Money.of(500));
    }

    @Test
    void updatesActivities() {
        // Given: 새 활동이 있는 계정 생성
        Account account = defaultAccount()
            .withBaselineBalance(Money.of(555L))
            .withActivityWindow(new ActivityWindow(
                defaultActivity()
                    .withId(null)  // 새 활동 (ID 없음)
                    .withMoney(Money.of(1L)).build()))
            .build();

        // When: 활동 저장
        adapter.updateActivities(account);

        // Then: 데이터베이스 검증
        assertThat(activityRepository.count()).isEqualTo(1);

        ActivityJpaEntity savedActivity = activityRepository.findAll().get(0);
        assertThat(savedActivity.getAmount()).isEqualTo(1L);
    }
}
```

```python
# Python 버전 (SQLAlchemy 테스트 예시)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 참조: 페이지 70-71, 라인 306-380
class TestAccountPersistenceAdapter:

    @pytest.fixture
    def setup_database(self):
        """테스트용 인메모리 데이터베이스 설정"""
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # 테스트 데이터 로드
        self._load_test_data(session)

        yield session
        session.close()

    def test_loads_account(self, setup_database):
        """계정 로드가 올바르게 작동하는지 검증"""
        session = setup_database
        adapter = AccountPersistenceAdapter(session)

        # When: 계정 로드
        account = adapter.load_account(
            AccountId(1),
            datetime(2018, 8, 10, 0, 0)
        )

        # Then: 로드된 상태 검증
        assert len(account.activity_window.activities) == 2
        assert account.calculate_balance() == Money(500)

    def test_updates_activities(self, setup_database):
        """활동 업데이트가 올바르게 작동하는지 검증"""
        session = setup_database
        adapter = AccountPersistenceAdapter(session)

        # Given: 새 활동이 있는 계정 생성
        account = (AccountBuilder()
            .with_baseline_balance(Money(555))
            .with_activity_window(ActivityWindow([
                ActivityBuilder()
                    .with_id(None)  # 새 활동 (ID 없음)
                    .with_money(Money(1))
                    .build()
            ]))
            .build())

        # When: 활동 저장
        adapter.update_activities(account)

        # Then: 데이터베이스 검증
        activities = session.query(ActivityJpaEntity).all()
        assert len(activities) == 1
        assert activities[0].amount == 1
```

#### Spring Boot의 데이터베이스 테스트 지원

@DataJpaTest로 Spring에게 데이터베이스 액세스에 필요한 객체 네트워크를 인스턴스화하도록 지시합니다. 여기에는 데이터베이스에 연결하는 Spring Data 리포지토리가 포함됩니다. 테스트 대상 어댑터가 필요로 하는 특정 객체가 해당 네트워크에 추가되도록 일부 추가 @Import를 추가합니다. 예를 들어 들어오는 도메인 객체를 데이터베이스 객체로 매핑하기 위해 어댑터가 필요로 하는 객체들입니다.

loadAccount() 메서드에 대한 테스트에서 SQL 스크립트를 사용하여 데이터베이스를 특정 상태로 만듭니다. 그런 다음 단순히 어댑터 API를 통해 계정을 로드하고 SQL 스크립트의 데이터베이스 상태를 고려할 때 예상되는 상태를 가지고 있는지 검증합니다.

updateActivities() 테스트는 반대 방향으로 진행됩니다. 새로운 계정 활동이 있는 Account 객체를 생성하고 지속되도록 어댑터로 전달합니다. 그런 다음 ActivityRepository의 API를 통해 활동이 데이터베이스에 저장되었는지 확인합니다.

#### 실제 데이터베이스의 중요성

이러한 테스트의 중요한 측면은 데이터베이스를 모킹하지 않는다는 것입니다. 테스트가 실제로 데이터베이스를 사용합니다. 데이터베이스를 모킹했다면 테스트는 여전히 동일한 코드 라인을 커버하여 동일한 높은 코드 라인 커버리지를 생성했을 것입니다. 그러나 이 높은 커버리지에도 불구하고 SQL 문의 오류 또는 데이터베이스 테이블과 Java 객체 간의 예상치 못한 매핑 오류로 인해 실제 데이터베이스가 있는 설정에서 테스트가 실패할 가능성이 여전히 상당히 높습니다.

기본적으로 Spring은 테스트 중에 사용할 인메모리 데이터베이스를 가동합니다. 아무것도 구성할 필요가 없고 테스트가 즉시 작동하기 때문에 매우 실용적입니다.

#### Testcontainers를 통한 프로덕션 데이터베이스 테스트

그러나 이 인메모리 데이터베이스는 프로덕션에서 사용하는 데이터베이스가 아닐 가능성이 높으므로 테스트가 인메모리 데이터베이스에 대해 완벽하게 작동했더라도 실제 데이터베이스에서 문제가 발생할 가능성이 여전히 상당합니다. 예를 들어 데이터베이스는 자체 SQL 버전을 구현하는 것을 좋아합니다.

이러한 이유로 영속성 어댑터 테스트는 실제 데이터베이스에 대해 실행되어야 합니다. Testcontainers와 같은 라이브러리는 이와 관련하여 큰 도움이 되며 필요에 따라 데이터베이스가 있는 Docker 컨테이너를 가동합니다.

실제 데이터베이스에 대해 실행하면 두 개의 다른 데이터베이스 시스템을 관리할 필요가 없다는 추가 이점이 있습니다. 테스트 중에 인메모리 데이터베이스를 사용하는 경우 특정 방식으로 구성하거나 각 데이터베이스에 대해 별도 버전의 데이터베이스 마이그레이션 스크립트를 만들어야 할 수 있으며, 이는 전혀 재미있지 않습니다.

---

### 6. 시스템 테스트로 주요 경로 테스트
(참조: 페이지 71-74, 라인 409-547)
→ 핵심 개념: **시스템 테스트**
→ 이전 화제와의 관계: **통합 테스트**에서 더 나아가 전체 애플리케이션을 커버하는 최상위 테스트

#### 시스템 테스트의 개념

피라미드 맨 위에는 시스템 테스트가 있습니다. 시스템 테스트는 전체 애플리케이션을 시작하고 API에 대해 요청을 실행하여 모든 계층이 함께 작동하는지 검증합니다.

#### "Send Money" 유스케이스 시스템 테스트

"Send Money" 유스케이스에 대한 시스템 테스트에서 애플리케이션에 HTTP 요청을 보내고 응답과 계정의 새 잔액을 검증합니다:

```java
// 참조: 페이지 72-73, 라인 419-510
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class SendMoneySystemTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    @Sql("SendMoneySystemTest.sql")
    void sendMoney() {

        // Given: 초기 잔액 저장
        Money initialSourceBalance = sourceAccount().calculateBalance();
        Money initialTargetBalance = targetAccount().calculateBalance();

        // When: HTTP 요청 전송
        ResponseEntity response = whenSendMoney(
            sourceAccountId(),
            targetAccountId(),
            transferredAmount());

        // Then: 응답 상태 검증
        then(response.getStatusCode())
            .isEqualTo(HttpStatus.OK);

        // Then: 소스 계정 잔액 검증
        then(sourceAccount().calculateBalance())
            .isEqualTo(initialSourceBalance.minus(transferredAmount()));

        // Then: 대상 계정 잔액 검증
        then(targetAccount().calculateBalance())
            .isEqualTo(initialTargetBalance.plus(transferredAmount()));
    }

    private ResponseEntity whenSendMoney(
        AccountId sourceAccountId,
        AccountId targetAccountId,
        Money amount) {

        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");
        HttpEntity<Void> request = new HttpEntity<>(null, headers);

        return restTemplate.exchange(
            "/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}",
            HttpMethod.POST,
            request,
            Object.class,
            sourceAccountId.getValue(),
            targetAccountId.getValue(),
            amount.getAmount());
    }

    // 헬퍼 메서드 생략
}
```

```python
# Python 버전 (Flask 테스트 예시)
import pytest
from flask import Flask

# 참조: 페이지 72-73, 라인 419-510
class TestSendMoneySystem:

    @pytest.fixture
    def app(self):
        """전체 애플리케이션 설정"""
        app = create_app()
        app.config['TESTING'] = True
        return app

    @pytest.fixture
    def client(self, app):
        """테스트 클라이언트"""
        return app.test_client()

    def test_send_money(self, client, setup_test_data):
        """송금 시나리오 전체 흐름 검증"""
        # Given: 초기 잔액 저장
        initial_source_balance = self._source_account().calculate_balance()
        initial_target_balance = self._target_account().calculate_balance()

        # When: HTTP 요청 전송
        response = self._when_send_money(
            client,
            self._source_account_id(),
            self._target_account_id(),
            self._transferred_amount()
        )

        # Then: 응답 상태 검증
        assert response.status_code == 200

        # Then: 소스 계정 잔액 검증
        assert self._source_account().calculate_balance() == \
            initial_source_balance - self._transferred_amount()

        # Then: 대상 계정 잔액 검증
        assert self._target_account().calculate_balance() == \
            initial_target_balance + self._transferred_amount()

    def _when_send_money(self, client, source_id, target_id, amount):
        """송금 HTTP 요청 전송"""
        return client.post(
            f'/accounts/sendMoney/{source_id}/{target_id}/{amount}',
            headers={'Content-Type': 'application/json'}
        )

    # 헬퍼 메서드 생략
```

#### 시스템 테스트의 특징

@SpringBootTest로 Spring에게 애플리케이션을 구성하는 전체 객체 네트워크를 시작하도록 지시합니다. 또한 애플리케이션이 랜덤 포트에 노출되도록 구성합니다.

테스트 메서드에서 단순히 요청을 생성하고, 애플리케이션에 보내고, 응답 상태와 계정의 새 잔액을 확인합니다.

요청을 보내기 위해 TestRestTemplate을 사용하고 있으며, 웹 어댑터 테스트에서 사용한 MockMvc는 사용하지 않습니다. 이는 실제 HTTP를 수행하고 있음을 의미하며 테스트를 프로덕션 환경에 조금 더 가깝게 만듭니다.

#### 실제 출력 어댑터 사용

실제 HTTP를 통과하는 것처럼 실제 출력 어댑터를 통과합니다. 우리의 경우 이것은 애플리케이션을 데이터베이스에 연결하는 영속성 어댑터일 뿐입니다. 다른 시스템과 통신하는 애플리케이션에서는 추가 출력 어댑터가 있을 것입니다. 시스템 테스트를 위해서라도 모든 제3자 시스템을 가동하고 실행하는 것이 항상 가능한 것은 아니므로 결국 모킹할 수 있습니다. 우리의 hexagonal architecture는 몇 개의 출력 포트 인터페이스만 스텁 아웃하면 되기 때문에 가능한 한 쉽게 만듭니다.

#### 도메인 특화 언어(DSL)의 중요성

테스트를 가능한 한 읽기 쉽게 만들기 위해 많은 노력을 기울였습니다. 모든 못생긴 로직을 헬퍼 메서드 내에 숨겼습니다. 이제 이러한 메서드는 사물의 상태를 검증하는 데 사용할 수 있는 도메인 특화 언어를 형성합니다.

이와 같은 도메인 특화 언어는 모든 유형의 테스트에서 좋은 아이디어이지만 시스템 테스트에서는 훨씬 더 중요합니다. 시스템 테스트는 단위 또는 통합 테스트보다 애플리케이션의 실제 사용자를 훨씬 더 잘 시뮬레이션하므로 사용자의 관점에서 애플리케이션을 검증하는 데 사용할 수 있습니다. 이는 적절한 어휘가 있으면 훨씬 쉽습니다.

이 어휘는 또한 애플리케이션의 사용자를 구현하기에 가장 적합하고 아마도 프로그래머가 아닌 도메인 전문가가 테스트에 대해 추론하고 피드백을 제공할 수 있게 합니다. JGiven과 같은 행동 주도 개발을 위한 전체 라이브러리가 있어 테스트를 위한 어휘를 만드는 프레임워크를 제공합니다.

#### 시스템 테스트의 추가 가치

이전 섹션에서 설명한 대로 단위 및 통합 테스트를 만들었다면 시스템 테스트는 동일한 코드의 많은 부분을 커버할 것입니다. 그들이 추가 이점을 제공하기는 할까요? 그렇습니다. 일반적으로 단위 및 통합 테스트와는 다른 유형의 버그를 발견합니다. 예를 들어 계층 간의 일부 매핑이 잘못되었을 수 있으며, 이는 단위 및 통합 테스트만으로는 알아차리지 못할 것입니다.

#### 시나리오 기반 시스템 테스트

시스템 테스트는 여러 유스케이스를 결합하여 시나리오를 만들 때 강점을 발휘합니다. 각 시나리오는 사용자가 일반적으로 애플리케이션을 통과할 수 있는 특정 경로를 나타냅니다. 가장 중요한 시나리오가 통과하는 시스템 테스트로 커버되면 최신 수정으로 시나리오를 손상시키지 않았다고 가정하고 배포할 준비가 된 것입니다.

---

### 7. 얼마나 많은 테스트가 충분한가
(참조: 페이지 74-75, 라인 548-591)
→ 핵심 개념: **테스트 전략과 측정**
→ 이전 화제와의 관계: 앞서 다룬 모든 테스트 유형들을 실무에 적용하기 위한 전략과 지침

#### 라인 커버리지의 한계

내가 참여한 많은 프로젝트 팀이 답할 수 없는 질문은 얼마나 많은 테스트를 해야 하는가입니다. 우리의 테스트가 코드의 80%를 커버하면 충분할까요? 그보다 높아야 할까요?

라인 커버리지는 테스트 성공을 측정하는 나쁜 지표입니다. 100% 이외의 목표는 완전히 무의미합니다. 코드베이스의 중요한 부분이 전혀 커버되지 않을 수 있기 때문입니다. 그리고 100%에서도 모든 버그가 해결되었다고 확신할 수 없습니다.

#### 배포 자신감으로 측정

소프트웨어 배포에 대해 얼마나 편안하게 느끼는지로 테스트 성공을 측정할 것을 제안합니다. 테스트를 실행한 후 배포할 만큼 테스트를 신뢰한다면 괜찮습니다. 더 자주 배포할수록 테스트를 더 신뢰합니다. 1년에 두 번만 배포한다면 1년에 두 번만 자신을 증명하기 때문에 아무도 테스트를 신뢰하지 않을 것입니다.

#### 프로덕션 버그로부터 학습

처음 몇 번 배포할 때는 믿음의 도약이 필요하지만, 프로덕션의 버그를 수정하고 배우는 것을 우선시하면 올바른 방향으로 가고 있는 것입니다. 각 프로덕션 버그에 대해 "왜 우리의 테스트가 이 버그를 잡지 못했는가?"라는 질문을 하고, 답을 문서화한 다음, 이를 커버하는 테스트를 추가해야 합니다. 시간이 지나면서 이것은 우리가 배포에 편안해지도록 만들 것이고 문서화는 시간 경과에 따른 개선을 측정하는 지표까지 제공할 것입니다.

#### Hexagonal Architecture의 테스트 전략

그러나 만들어야 할 테스트를 정의하는 전략으로 시작하는 것이 도움이 됩니다. hexagonal architecture에 대한 그러한 전략은 다음과 같습니다:

• **도메인 엔티티를 구현하는 동안 단위 테스트로 커버**
• **유스케이스를 구현하는 동안 단위 테스트로 커버**
• **어댑터를 구현하는 동안 통합 테스트로 커버**
• **사용자가 애플리케이션을 통과할 수 있는 가장 중요한 경로를 시스템 테스트로 커버**

#### "구현하는 동안"의 중요성

"구현하는 동안"이라는 단어에 주목하십시오. 테스트가 기능 개발 후가 아니라 개발 중에 수행되면 개발 도구가 되며 더 이상 잡무처럼 느껴지지 않습니다.

#### 테스트 설계의 중요성

그러나 새 필드를 추가할 때마다 테스트를 수정하는 데 한 시간을 소비해야 한다면 우리는 무언가 잘못하고 있는 것입니다. 아마도 우리의 테스트가 테스트 대상 코드의 구조 변경에 너무 취약하며 이를 개선하는 방법을 살펴봐야 합니다. 각 리팩터링에 대해 테스트를 수정해야 한다면 테스트는 가치를 잃게 됩니다.

---

### 8. 유지보수 가능한 소프트웨어 구축 방법
(참조: 페이지 75, 라인 575-591)
→ 이전 화제와의 관계: 앞서 다룬 모든 테스트 개념들을 종합하여 실무 적용 원칙 제시

#### Hexagonal Architecture의 테스트 이점

Hexagonal Architecture 스타일은 도메인 로직과 외부를 향한 어댑터를 깔끔하게 분리합니다. 이는 중앙 도메인 로직을 단위 테스트로, 어댑터를 통합 테스트로 커버하는 명확한 테스트 전략을 정의하는 데 도움이 됩니다.

#### 포트의 모킹 지점 역할

입출력 포트는 테스트에서 매우 명확한 모킹 지점을 제공합니다. 각 포트에 대해 모킹할지 실제 구현을 사용할지 결정할 수 있습니다. 포트가 각각 매우 작고 집중되어 있으면 모킹하는 것이 잡무가 아니라 쉽습니다. 포트 인터페이스가 제공하는 메서드가 적을수록 테스트에서 모킹해야 하는 메서드에 대한 혼란이 줄어듭니다.

#### 테스트가 제공하는 경고 신호

무언가를 모킹하는 것이 너무 부담스럽거나 코드베이스의 특정 부분을 커버하기 위해 어떤 종류의 테스트를 사용해야 하는지 모르겠다면 경고 신호입니다. 이와 관련하여 우리의 테스트는 카나리아로서 추가 책임이 있습니다 - 아키텍처의 결함에 대해 경고하고 유지보수 가능한 코드 베이스를 만드는 경로로 우리를 되돌리는 것입니다.
