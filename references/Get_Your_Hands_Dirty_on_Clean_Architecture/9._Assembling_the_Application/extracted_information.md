# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter9: Assembling the Application

## 압축 내용
애플리케이션 조립은 의존성 주입을 통해 use case, adapter, domain 객체를 인스턴스화하고 연결하며, 의존성 규칙을 준수하면서 configuration component가 중립적 위치에서 모든 계층에 접근하여 작동하는 애플리케이션을 구성하는 과정이다.

## 핵심 내용

**핵심 개념들:**
- Configuration Component (설정 컴포넌트)
- Dependency Injection (의존성 주입)
- Assembly Approaches (조립 방식)

**핵심 개념 설명:**

### Configuration Component (설정 컴포넌트) → [상세: Why Even Care About Assembly?, Figure 26]
- 아키텍처에 중립적이며 모든 클래스에 대한 의존성을 가지는 컴포넌트 (content.md, 23-24행)
- Clean Architecture의 가장 바깥 원에 위치하여 모든 내부 계층에 접근 가능 (content.md, 30-32행)
- 웹 어댑터, 유스케이스, 퍼시스턴스 어댑터 인스턴스를 생성하고 연결 (content.md, 35-41행)
- Single Responsibility Principle을 위반하지만 나머지 애플리케이션을 깨끗하게 유지하기 위해 필요 (content.md, 46-49행)

### Dependency Injection (의존성 주입) → [상세: Why Even Care About Assembly?]
- 의존성이 올바른 방향(내부로)을 가리키도록 유지하는 메커니즘 (content.md, 5-7행, 11-13행)
- 유스케이스가 퍼시스턴스 어댑터를 직접 인스턴스화하면 잘못된 방향의 의존성 생성 (content.md, 14-15행)
- Outgoing port interface를 통해 유스케이스는 인터페이스만 알고 런타임에 구현체 제공받음 (content.md, 16-17행)
- 테스트 시 mock 객체 주입으로 단위 테스트 용이성 향상 (content.md, 18-20행)

### Assembly Approaches (조립 방식) → [상세: Assembling via Plain Code, Assembling via Spring's Classpath Scanning, Assembling via Spring's Java Config]
세 가지 주요 조립 방식:
1. **Plain Code** - 프레임워크 없이 직접 코드로 조립 (content.md, 54-110행)
2. **Classpath Scanning** - Spring의 `@Component` 어노테이션 기반 자동 스캔 (content.md, 122-230행)
3. **Java Config** - Spring의 `@Configuration`과 `@Bean`을 이용한 명시적 설정 (content.md, 231-317행)

**핵심 개념 간 관계:**
Configuration Component는 Dependency Injection을 구현하기 위한 컨테이너 역할을 하며, Assembly Approaches는 이 Configuration Component를 구현하는 구체적인 방법론들이다. Plain Code에서 Spring Java Config로 갈수록 더 세밀한 제어와 모듈화가 가능해지며, Dependency Rule 준수와 테스트 용이성이 향상된다.

---

## 상세 내용

### 목차
1. Why Even Care About Assembly? → [핵심: Configuration Component, Dependency Injection]
2. Assembling via Plain Code → [핵심: Assembly Approaches]
3. Assembling via Spring's Classpath Scanning → [핵심: Assembly Approaches]
4. Assembling via Spring's Java Config → [핵심: Assembly Approaches]
5. How Does This Help Me Build Maintainable Software?

### 1. Why Even Care About Assembly? → [핵심: Configuration Component, Dependency Injection]

**의존성 방향의 중요성** (content.md, 10-22행):
- 모든 의존성은 내부(도메인 코드)를 향해야 함
- 유스케이스가 퍼시스턴스 어댑터를 직접 인스턴스화하면 잘못된 의존성 방향
- Outgoing port interface를 통해 런타임에 구현체 제공
- 생성자를 통한 객체 전달로 테스트 시 mock 사용 가능

```java
// 잘못된 방식 - 유스케이스가 어댑터를 직접 인스턴스화
class SendMoneyUseCase {
    public void sendMoney() {
        // 의존성이 잘못된 방향(외부로)을 가리킴
        AccountPersistenceAdapter adapter = new AccountPersistenceAdapter();
    }
}

// 올바른 방식 - 인터페이스를 통한 의존성 주입
class SendMoneyUseCase {
    private final LoadAccountPort loadAccountPort;

    // 생성자를 통해 구현체 주입받음
    public SendMoneyUseCase(LoadAccountPort loadAccountPort) {
        this.loadAccountPort = loadAccountPort;
    }
}
```

```python
# Python 버전
# 잘못된 방식
class SendMoneyUseCase:
    def send_money(self):
        # 직접 어댑터 인스턴스화
        adapter = AccountPersistenceAdapter()

# 올바른 방식
class SendMoneyUseCase:
    def __init__(self, load_account_port: LoadAccountPort):
        # 인터페이스를 통한 의존성 주입
        self.load_account_port = load_account_port
```

**Configuration Component의 역할** (content.md, 23-49행):
- 중립적 위치에서 모든 계층의 클래스에 접근 가능 (Figure 26 참조)
- Clean Architecture의 가장 바깥 원에 위치
- 책임사항:
  - 웹 어댑터 인스턴스 생성
  - HTTP 요청을 웹 어댑터로 라우팅
  - 유스케이스 인스턴스 생성
  - 웹 어댑터에 유스케이스 인스턴스 제공
  - 퍼시스턴스 어댑터 인스턴스 생성
  - 유스케이스에 퍼시스턴스 어댑터 인스턴스 제공
  - 퍼시스턴스 어댑터의 데이터베이스 접근 보장
- 설정 파일이나 커맨드라인 파라미터에 접근하여 컴포넌트에 전달
- Single Responsibility Principle 위반이지만 나머지 애플리케이션을 깨끗하게 유지하기 위해 필요

### 2. Assembling via Plain Code → [핵심: Assembly Approaches]

이전 화제(Why Even Care About Assembly?)에서 Configuration Component의 필요성을 확립했으므로, 이제 가장 기본적인 구현 방법인 Plain Code 방식을 살펴본다.

**기본 구현 방식** (content.md, 54-97행):

```java
package copyeditor.configuration;

class Application {
    public static void main(String[] args) {
        // 1. 리포지토리 인스턴스 생성
        AccountRepository accountRepository = new AccountRepository();
        ActivityRepository activityRepository = new ActivityRepository();

        // 2. 퍼시스턴스 어댑터 생성 및 리포지토리 주입
        AccountPersistenceAdapter accountPersistenceAdapter =
            new AccountPersistenceAdapter(accountRepository, activityRepository);

        // 3. 유스케이스 생성 및 어댑터 주입 (port로서)
        SendMoneyUseCase sendMoneyUseCase =
            new SendMoneyUseService(
                accountPersistenceAdapter,  // LoadAccountPort로 사용
                accountPersistenceAdapter); // UpdateAccountStatePort로 사용

        // 4. 웹 컨트롤러 생성 및 유스케이스 주입
        SendMoneyController sendMoneyController =
            new SendMoneyController(sendMoneyUseCase);

        // 5. HTTP 요청 처리 시작
        startProcessingWebRequests(sendMoneyController);
    }
}
```

```python
# Python 버전
class Application:
    @staticmethod
    def main(args):
        # 1. 리포지토리 인스턴스 생성
        account_repository = AccountRepository()
        activity_repository = ActivityRepository()

        # 2. 퍼시스턴스 어댑터 생성 및 리포지토리 주입
        account_persistence_adapter = AccountPersistenceAdapter(
            account_repository,
            activity_repository
        )

        # 3. 유스케이스 생성 및 어댑터 주입 (port로서)
        send_money_use_case = SendMoneyUseService(
            account_persistence_adapter,  # LoadAccountPort로 사용
            account_persistence_adapter   # UpdateAccountStatePort로 사용
        )

        # 4. 웹 컨트롤러 생성 및 유스케이스 주입
        send_money_controller = SendMoneyController(send_money_use_case)

        # 5. HTTP 요청 처리 시작
        start_processing_web_requests(send_money_controller)
```

**Plain Code 방식의 단점** (content.md, 103-121행):
1. **코드 양 증가**: 단일 컨트롤러, 유스케이스, 어댑터만으로도 많은 코드 필요
   - 엔터프라이즈 애플리케이션에서는 관리 불가능한 수준으로 증가
2. **가시성 문제**: 모든 클래스가 public이어야 함
   - 패키지 외부에서 인스턴스화하기 때문
   - Java가 유스케이스와 퍼시스턴스 어댑터 간 직접 접근을 방지하지 못함
   - package-private 가시성 사용 불가

**해결책 제시** (content.md, 118-121행):
- Dependency injection 프레임워크 사용
- Spring 프레임워크가 Java 세계에서 가장 인기
- 웹 및 데이터베이스 지원 포함
- startProcessingWebRequests() 같은 로직 직접 구현 불필요

### 3. Assembling via Spring's Classpath Scanning → [핵심: Assembly Approaches]

Plain Code 방식의 단점을 해결하기 위해 Spring의 가장 편리한 방식인 Classpath Scanning을 살펴본다.

**Classpath Scanning 개념** (content.md, 122-134행):
- Spring이 클래스패스의 모든 클래스를 탐색
- `@Component` 어노테이션이 붙은 클래스 검색
- 각 클래스로부터 객체(bean) 생성
- 필요한 필드를 인자로 받는 생성자 필요

**구현 예시** (content.md, 135-175행):

```java
@Component  // Spring이 이 클래스를 자동으로 감지
@RequiredArgsConstructor  // Lombok이 final 필드로 생성자 자동 생성
class AccountPersistenceAdapter implements
    LoadAccountPort,
    UpdateAccountStatePort {

    // final 필드들 - 생성자로 주입됨
    private final AccountRepository accountRepository;
    private final ActivityRepository activityRepository;
    private final AccountMapper accountMapper;

    @Override
    public Account loadAccount(AccountId accountId, LocalDateTime baselineDate) {
        // 구현...
    }

    @Override
    public void updateActivities(Account account) {
        // 구현...
    }
}
```

```python
# Python 버전 (dataclass 사용)
from dataclasses import dataclass

@dataclass  # Python에서 자동 생성자 생성
class AccountPersistenceAdapter:
    """Spring의 @Component + @RequiredArgsConstructor와 유사"""
    account_repository: AccountRepository
    activity_repository: ActivityRepository
    account_mapper: AccountMapper

    def load_account(self, account_id: AccountId, baseline_date: datetime) -> Account:
        # 구현...
        pass

    def update_activities(self, account: Account):
        # 구현...
        pass
```

**커스텀 Stereotype 어노테이션** (content.md, 185-208행):

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component  // Spring이 감지하도록 메타-어노테이션
public @interface PersistenceAdapter {
    @AliasFor(annotation = Component.class)
    String value() default "";
}

// 사용 예시
@PersistenceAdapter  // @Component 대신 사용
class AccountPersistenceAdapter implements LoadAccountPort {
    // 아키텍처를 더 명확하게 표현
}
```

```python
# Python 버전 (데코레이터 사용)
from typing import Type
from functools import wraps

def persistence_adapter(cls: Type) -> Type:
    """
    PersistenceAdapter 마커 데코레이터
    아키텍처를 명확하게 표현
    """
    cls._is_persistence_adapter = True
    return cls

# 사용 예시
@persistence_adapter
class AccountPersistenceAdapter:
    """아키텍처를 명확하게 표현하는 어댑터"""
    pass
```

**Classpath Scanning의 장단점** (content.md, 183-230행):

장점:
- 매우 편리한 조립 방식
- `@Component` 어노테이션만 추가하고 올바른 생성자 제공
- 빠른 개발 가능

단점:
1. **침습적(Invasive)**: 프레임워크 특정 어노테이션 필요
   - Clean Architecture 순수주의자들은 금지사항으로 봄
   - 일반 애플리케이션 개발에서는 큰 문제 아님
   - 라이브러리/프레임워크 개발 시에는 문제 (사용자에게 Spring 의존성 강제)

2. **마법 같은 일(Magic) 발생**:
   - 예상치 못한 효과로 문제 발생 시 해결에 오랜 시간 소요
   - 부모 패키지를 가리키고 `@Component` 클래스 탐색
   - 애플리케이션 내 모든 클래스를 파악하기 어려움
   - 원치 않는 클래스가 application context에 포함될 수 있음
   - 해당 클래스가 application context를 악의적으로 조작 가능

### 4. Assembling via Spring's Java Config → [핵심: Assembly Approaches]

Classpath Scanning의 "무분별한(blunt)" 특성을 보완하기 위해 더 세밀한 제어를 제공하는 Java Config 방식을 살펴본다.

**Java Config 개념** (content.md, 231-244행):
- Classpath scanning이 "cudgel(곤봉)"이라면 Java Config는 "scalpel(메스)"
- Plain Code 방식과 유사하지만 덜 지저분하고 프레임워크 제공
- Configuration 클래스를 생성하여 bean 집합을 application context에 추가

**구현 예시** (content.md, 239-281행):

```java
@Configuration  // Spring이 설정 클래스로 인식
@EnableJpaRepositories  // JPA 리포지토리 자동 구현 제공
class PersistenceAdapterConfiguration {

    @Bean  // AccountPersistenceAdapter bean 생성
    AccountPersistenceAdapter accountPersistenceAdapter(
        AccountRepository accountRepository,
        ActivityRepository activityRepository,
        AccountMapper accountMapper) {

        return new AccountPersistenceAdapter(
            accountRepository,
            activityRepository,
            accountMapper);
    }

    @Bean  // AccountMapper bean 생성
    AccountMapper accountMapper() {
        return new AccountMapper();
    }
}
```

```python
# Python 버전 (의존성 주입 컨테이너 패턴)
from typing import Protocol

class PersistenceAdapterConfiguration:
    """퍼시스턴스 계층의 모든 객체를 인스턴스화하는 설정 모듈"""

    def __init__(self, container):
        self.container = container

    def account_persistence_adapter(
        self,
        account_repository: AccountRepository,
        activity_repository: ActivityRepository,
        account_mapper: AccountMapper
    ) -> AccountPersistenceAdapter:
        """AccountPersistenceAdapter bean 생성"""
        return AccountPersistenceAdapter(
            account_repository,
            activity_repository,
            account_mapper
        )

    def account_mapper(self) -> AccountMapper:
        """AccountMapper bean 생성"""
        return AccountMapper()
```

**Repository 객체의 출처** (content.md, 289-300행):
- `@EnableJpaRepositories` 어노테이션에 의해 Spring이 자동 생성
- Spring Boot가 이 어노테이션을 발견하면 Spring Data repository 인터페이스의 구현체 자동 제공
- 메인 애플리케이션 클래스 대신 커스텀 설정 클래스에 어노테이션 배치
  - 퍼시스턴스가 필요 없는 테스트에서도 JPA 리포지토리 활성화 방지
  - "feature annotations"를 별도 설정 "module"로 분리하여 유연성 향상
  - 전체 애플리케이션이 아닌 일부만 시작 가능

**Java Config의 장점** (content.md, 301-312행):
1. **Tightly-scoped Module**:
   - 퍼시스턴스 계층에 필요한 모든 객체를 인스턴스화하는 좁은 범위 모듈
   - classpath scanning으로 자동 감지되지만 어떤 bean이 추가되는지 완전한 제어

2. **유연한 모듈 구성**:
   - 웹 어댑터, 애플리케이션 계층 모듈 등 유사하게 생성 가능
   - 특정 모듈은 포함하고 다른 모듈은 mock으로 대체 가능
   - 테스트에서 높은 유연성 제공
   - 각 모듈을 별도 코드베이스, 패키지, JAR 파일로 분리 가능

3. **프레임워크 독립성**:
   - `@Component` 어노테이션을 코드베이스 전체에 뿌릴 필요 없음
   - 애플리케이션 계층을 Spring(또는 다른 프레임워크) 의존성 없이 깨끗하게 유지

**Java Config의 제약사항** (content.md, 313-317행):
- 설정 클래스가 bean 클래스와 같은 패키지에 없으면 해당 클래스들이 public이어야 함
- 가시성 제한을 위해 패키지를 모듈 경계로 사용하고 각 패키지에 전용 설정 클래스 생성
- 단, 이 방식은 하위 패키지 사용 불가 (10장 "Enforcing Architecture Boundaries"에서 논의)

### 5. How Does This Help Me Build Maintainable Software?

앞의 세 가지 조립 방식(Plain Code, Classpath Scanning, Java Config)을 비교하며 유지보수 가능한 소프트웨어 구축 방법을 정리한다.

**Spring/Spring Boot의 가치** (content.md, 322-328행):
- 개발자 삶을 편하게 만드는 많은 기능 제공
- 주요 기능: 개발자가 제공한 부품(클래스)으로 애플리케이션 조립

**Classpath Scanning의 양면성** (content.md, 326-331행):

편의성:
- 매우 편리한 기능
- Spring에 패키지만 가리키면 찾은 클래스로 애플리케이션 조립
- 빠른 개발 가능
- 애플리케이션 전체를 생각할 필요 없음

문제점 (코드베이스 성장 시):
- 투명성 부족: 어떤 bean이 application context에 로드되는지 불명확
- 테스트에서 application context의 격리된 부분을 쉽게 시작할 수 없음

**전용 Configuration Component의 이점** (content.md, 332-336행):
1. **책임 분리**:
   - 애플리케이션 조립 책임을 전용 컴포넌트에 위임
   - 애플리케이션 코드를 이 책임(변경 이유)에서 해방
   - SOLID의 "S" (Single Responsibility Principle) 준수

2. **높은 응집도 모듈**:
   - 서로 격리되어 시작 가능한 고도로 응집된 모듈
   - 코드베이스 내에서 쉽게 이동 가능
   - 유지보수성 향상

3. **비용-효익 균형**:
   - 추가 시간이 필요: 설정 컴포넌트 유지보수
   - 보상: 모듈화, 테스트 용이성, 코드 이동성
   - "As usual" - 소프트웨어 개발의 일반적인 트레이드오프
