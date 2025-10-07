# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter 7: Testing Architecture Elements

## 압축 내용
헥사고날 아키텍처의 각 계층(도메인 엔티티, 유스케이스, 어댑터)에 적합한 테스트 전략을 테스트 피라미드 기반으로 제시하며, 단위 테스트, 통합 테스트, 시스템 테스트의 구체적인 적용 방법과 테스트 성공의 기준을 설명한다.

## 핵심 내용
### 핵심 개념
- Test Pyramid (테스트 피라미드)
- Unit Test (단위 테스트)
- Integration Test (통합 테스트)
- System Test (시스템 테스트)
- Mocking (모킹)
- Hexagonal Architecture Testing Strategy (헥사고날 아키텍처 테스트 전략)

### 핵심 개념 설명

**Test Pyramid (테스트 피라미드)**
많은 수의 저렴하고 빠른 단위 테스트를 기반으로, 점차 적은 수의 비용이 높고 느린 통합/시스템 테스트로 구성되는 테스트 전략 메타포. 단위 경계, 아키텍처 경계, 시스템 경계를 넘어가는 테스트일수록 비용이 높아지므로 커버리지를 낮춰야 한다.
참조: 페이지 64-65, 라인 10-23

**Unit Test (단위 테스트)**
단일 클래스를 인스턴스화하고 그 인터페이스를 통해 기능을 테스트하며, 의존성은 모크로 대체한다. 도메인 엔티티와 유스케이스 서비스를 검증하는 데 사용된다.
참조: 페이지 65, 라인 31-34

**Integration Test (통합 테스트)**
여러 유닛의 네트워크를 인스턴스화하고 진입점 클래스의 인터페이스를 통해 데이터를 전송하여 동작을 검증한다. 두 레이어 간 경계를 넘나들며 일부는 모크를 사용할 수 있다. 웹 어댑터와 영속성 어댑터를 테스트하는 데 적합하다.
참조: 페이지 65, 라인 35-38

**System Test (시스템 테스트)**
애플리케이션 전체를 구성하는 모든 객체 네트워크를 시작하고 모든 레이어를 거쳐 특정 유스케이스가 작동하는지 검증한다. 실제 HTTP를 통한 요청 검증과 데이터베이스 상태 확인을 포함한다.
참조: 페이지 65, 라인 39-40

**Mocking (모킹)**
테스트 시 실제 의존성 대신 가짜 객체를 사용하여 특정 동작을 시뮬레이션하는 기법. Mockito 라이브러리를 활용하며, 메서드 호출 여부를 검증할 수 있다.
참조: 페이지 67, 라인 194-196

**Hexagonal Architecture Testing Strategy (헥사고날 아키텍처 테스트 전략)**
도메인 엔티티는 단위 테스트, 유스케이스는 단위 테스트, 어댑터는 통합 테스트로 커버하고, 중요한 사용자 경로는 시스템 테스트로 검증하는 전략. 포트는 명확한 모킹 지점을 제공한다.
참조: 페이지 75, 라인 576-587

### 핵심 개념 간 관계

Test Pyramid는 Hexagonal Architecture Testing Strategy의 기반 원칙이다. Unit Test는 도메인 엔티티와 유스케이스에, Integration Test는 웹/영속성 어댑터에, System Test는 전체 애플리케이션 경로 검증에 각각 적용된다. Mocking은 Unit Test와 Integration Test에서 의존성을 제어하는 핵심 기법으로 사용되며, 헥사고날 아키텍처의 포트는 명확한 모킹 지점을 제공하여 테스트를 용이하게 한다.

## 상세 핵심 내용
### 중요 개념
- Test Pyramid (테스트 피라미드)
- Unit Test (단위 테스트)
- Integration Test (통합 테스트)
- System Test (시스템 테스트)
- Mocking (모킹)
- Hexagonal Architecture Testing Strategy (헥사고날 아키텍처 테스트 전략)
- Domain Entity Testing (도메인 엔티티 테스트)
- Use Case Testing (유스케이스 테스트)
- Web Adapter Testing (웹 어댑터 테스트)
- Persistence Adapter Testing (영속성 어댑터 테스트)
- Given/When/Then Pattern (Given/When/Then 패턴)
- Self-Validating Command (자기 검증 커맨드)
- Real Database Testing (실제 데이터베이스 테스트)
- Domain-Specific Language in Tests (테스트에서의 도메인 특화 언어)
- Test Success Measurement (테스트 성공 측정)
- Line Coverage vs Shipping Confidence (라인 커버리지 vs 배포 신뢰도)

### 중요 개념 설명

**Test Pyramid (테스트 피라미드)**
많은 수의 저렴하고 빠른 단위 테스트를 기반으로, 점차 적은 수의 비용이 높고 느린 통합/시스템 테스트로 구성되는 테스트 전략 메타포. Mike Cohn의 "Succeeding with Agile"(2009)에서 유래했다. 단위 경계, 아키텍처 경계, 시스템 경계를 넘어가는 테스트일수록 구축 비용이 높아지고, 실행 속도가 느려지며, 더 취약해진다(설정 오류로 실패 가능성 증가). 따라서 비용이 높은 테스트일수록 커버리지를 낮춰야 새로운 기능 개발 시간을 확보할 수 있다.
참조: 페이지 64-65, 라인 10-23

**Unit Test (단위 테스트)**
단일 "유닛"(보통 클래스)을 인스턴스화하고 그 인터페이스를 통해 기능을 테스트한다. 의존성이 있는 다른 클래스들은 인스턴스화하지 않고 모크로 대체하여 필요한 동작을 시뮬레이션한다. 설정이 쉽고, 이해하기 쉬우며, 매우 빠르게 실행된다. 도메인 엔티티의 비즈니스 로직을 검증하는 데 가장 적합하며, 도메인 엔티티는 다른 클래스에 대한 의존성이 거의 없기 때문에 다른 테스트 타입이 필요하지 않다.
참조: 페이지 65, 라인 31-34

**Integration Test (통합 테스트)**
여러 유닛의 네트워크를 인스턴스화하고 진입점 클래스의 인터페이스를 통해 데이터를 전송하여 해당 네트워크가 예상대로 작동하는지 검증한다. 두 레이어 간 경계를 넘나들기 때문에 객체 네트워크가 완전하지 않거나 일부 지점에서 모크를 사용해야 한다. 웹 어댑터나 영속성 어댑터처럼 프레임워크에 강하게 바인딩된 컴포넌트를 테스트하는 데 적합하다. 프레임워크와 통합된 상태에서 테스트하므로 매핑, 검증, HTTP 처리 등을 실제로 검증할 수 있다.
참조: 페이지 65, 라인 35-38

**System Test (시스템 테스트)**
애플리케이션 전체를 구성하는 모든 객체 네트워크를 시작하고 모든 레이어를 거쳐 특정 유스케이스가 예상대로 작동하는지 검증한다. API를 통해 실제 HTTP 요청을 보내고 응답과 데이터베이스 상태를 검증한다. 실제 사용자가 애플리케이션을 사용하는 방식을 가장 잘 시뮬레이션하며, 여러 유스케이스를 결합하여 시나리오를 생성할 때 강점을 발휘한다. 가장 중요한 시나리오들이 통과하면 최신 수정사항으로 인해 문제가 발생하지 않았다고 가정하고 배포할 수 있다.
참조: 페이지 65, 라인 39-40

**Mocking (모킹)**
테스트 시 실제 의존성 대신 가짜 객체를 사용하여 필요한 동작을 시뮬레이션하는 기법. Mockito 라이브러리를 활용하여 모크 객체를 생성하고, then() 메서드로 특정 메서드가 호출되었는지 검증할 수 있다. 유스케이스 서비스는 상태가 없기 때문에 상태를 검증할 수 없고, 대신 모크된 의존성과의 상호작용을 검증한다. 그러나 이는 테스트가 코드 구조 변경에 취약해지므로, 가장 중요한 상호작용만 검증하는 것이 좋다.
참조: 페이지 67, 라인 194-196

**Hexagonal Architecture Testing Strategy (헥사고날 아키텍처 테스트 전략)**
도메인 엔티티를 구현할 때는 단위 테스트로 커버하고, 유스케이스를 구현할 때는 단위 테스트로 커버하며, 어댑터를 구현할 때는 통합 테스트로 커버하고, 사용자가 거칠 수 있는 가장 중요한 경로는 시스템 테스트로 커버한다. 헥사고날 아키텍처 스타일은 도메인 로직과 외부 대면 어댑터를 명확하게 분리하여 명확한 테스트 전략을 정의하는 데 도움을 준다. 입력 및 출력 포트는 매우 명확한 모킹 지점을 제공하며, 각 포트가 작고 집중되어 있으면 모킹이 수월해진다.
참조: 페이지 74-75, 라인 564-587

**Domain Entity Testing (도메인 엔티티 테스트)**
아키텍처 중심의 도메인 엔티티를 단위 테스트로 검증한다. Account 엔티티를 특정 상태로 인스턴스화하고 withdraw() 메서드를 호출한 후, 출금이 성공했는지와 예상되는 부수 효과가 발생했는지 검증한다. 설정이 쉽고, 이해하기 쉬우며, 매우 빠르게 실행된다. 도메인 엔티티는 다른 클래스에 대한 의존성이 거의 없으므로 단위 테스트가 가장 적합하다.
참조: 페이지 65-66, 라인 46-107

**Use Case Testing (유스케이스 테스트)**
유스케이스 서비스를 단위 테스트로 검증한다. SendMoneyService의 "Send Money" 유스케이스는 소스 계좌를 잠그고, 출금이 성공하면 타겟 계좌도 잠근 후 입금하고, 양쪽 계좌를 모두 잠금 해제한다. Given/When/Then 패턴을 사용하여 가독성을 높이며, 트랜잭션이 성공했을 때 모든 것이 예상대로 작동하는지 검증한다. 유스케이스 서비스는 상태가 없으므로 모크된 의존성과의 상호작용을 검증하지만, 모든 상호작용을 검증하면 리팩토링 시 테스트 수정이 필요하므로 가장 중요한 것만 검증하는 것이 좋다.
참조: 페이지 66-68, 라인 109-213

**Web Adapter Testing (웹 어댑터 테스트)**
웹 어댑터를 통합 테스트로 검증한다. JSON 형식의 HTTP 입력을 받아 검증하고, 유스케이스가 기대하는 형식으로 매핑한 후 유스케이스에 전달하고, 유스케이스 결과를 다시 JSON으로 매핑하여 HTTP 응답으로 반환하는 전 과정을 테스트한다. @WebMvcTest 어노테이션을 사용하여 Spring이 특정 요청 경로에 응답하고, Java와 JSON 간 매핑하고, HTTP 입력을 검증하는 객체 네트워크를 인스턴스화한다. MockMvc를 사용하여 HTTP 프로토콜을 모킹하지만, JSON에서 커맨드 객체로의 매핑, 검증, 유스케이스 호출, HTTP 응답 상태 검증은 모두 실제로 수행된다.
참조: 페이지 68-69, 라인 214-294

**Persistence Adapter Testing (영속성 어댑터 테스트)**
영속성 어댑터를 통합 테스트로 검증한다. 어댑터 내부 로직뿐만 아니라 데이터베이스로의 매핑도 검증해야 하기 때문이다. @DataJpaTest 어노테이션으로 데이터베이스 접근에 필요한 객체 네트워크를 인스턴스화하고, @Sql로 데이터베이스를 특정 상태로 설정한 후 어댑터 API를 통해 계좌를 로드하고 예상 상태인지 검증한다. 중요한 것은 데이터베이스를 모킹하지 않고 실제로 데이터베이스에 접근한다는 점이며, 이를 통해 SQL 문이나 매핑 오류를 실제로 잡을 수 있다. Testcontainers 같은 라이브러리를 사용하여 실제 프로덕션 데이터베이스와 동일한 환경에서 테스트하는 것이 좋다.
참조: 페이지 69-71, 라인 295-408

**Given/When/Then Pattern (Given/When/Then 패턴)**
Behavior-Driven Development에서 일반적으로 사용되는 테스트 구조 패턴. Given 섹션에서는 소스/타겟 계좌를 생성하고 올바른 상태로 설정하며 입력 커맨드를 생성한다. When 섹션에서는 유스케이스 메서드를 호출한다. Then 섹션에서는 트랜잭션 성공 여부를 확인하고 특정 메서드들이 호출되었는지 검증한다. 테스트 가독성을 크게 향상시킨다.
참조: 페이지 66-67, 라인 186-193

**Self-Validating Command (자기 검증 커맨드)**
커맨드 객체가 생성 시점에 자체적으로 유효성 검증을 수행하는 패턴. SendMoneyCommand를 자기 검증 커맨드로 구축하면 매핑이 구문적으로 유효한 입력을 생성함을 보장할 수 있다. 웹 어댑터 테스트에서 JSON에서 커맨드 객체로의 전체 매핑 경로를 검증할 때 유용하다.
참조: 페이지 69, 라인 282-284

**Real Database Testing (실제 데이터베이스 테스트)**
영속성 어댑터 테스트는 실제 데이터베이스를 사용해야 한다. Spring의 기본 인메모리 데이터베이스는 편리하지만 프로덕션 데이터베이스와 다를 수 있으며, 데이터베이스마다 고유한 SQL 방언을 구현하므로 인메모리 테스트가 성공해도 실제 데이터베이스에서는 실패할 수 있다. Testcontainers를 사용하면 요청 시 Docker 컨테이너에서 데이터베이스를 실행할 수 있으며, 두 개의 다른 데이터베이스 시스템을 관리할 필요가 없어진다.
참조: 페이지 71, 라인 398-408

**Domain-Specific Language in Tests (테스트에서의 도메인 특화 언어)**
시스템 테스트에서 헬퍼 메서드로 못생긴 로직을 숨겨 가독성을 최대화한 도메인 특화 언어를 구성한다. 시스템 테스트는 실제 사용자를 훨씬 잘 시뮬레이션하므로 사용자 관점에서 애플리케이션을 검증하는 데 사용할 수 있다. 적절한 어휘를 갖추면 도메인 전문가(프로그래머가 아닐 수 있음)가 테스트에 대해 추론하고 피드백을 제공할 수 있다. JGiven 같은 Behavior-Driven Development 라이브러리는 테스트를 위한 어휘를 만드는 프레임워크를 제공한다.
참조: 페이지 73, 라인 524-533

**Test Success Measurement (테스트 성공 측정)**
많은 프로젝트 팀이 얼마나 테스트해야 하는지 답하지 못한다. 라인 커버리지는 테스트 성공을 측정하는 나쁜 지표이다. 100% 이외의 목표는 완전히 무의미하며(중요한 부분이 커버되지 않을 수 있음), 100%에서도 모든 버그가 해결되었다고 확신할 수 없다. 테스트 성공은 소프트웨어를 배포할 때 얼마나 편안하게 느끼는지로 측정해야 한다. 테스트를 충분히 신뢰하여 테스트 실행 후 배포할 수 있으면 좋은 것이다. 자주 배포할수록 테스트에 대한 신뢰도가 높아진다. 프로덕션 버그가 발생할 때마다 "왜 테스트가 이 버그를 잡지 못했는가?"라는 질문을 하고, 답을 문서화하고, 해당 버그를 커버하는 테스트를 추가해야 한다.
참조: 페이지 74, 라인 549-562

**Line Coverage vs Shipping Confidence (라인 커버리지 vs 배포 신뢰도)**
라인 커버리지는 나쁜 지표이지만, 테스트 성공 측정을 위한 더 나은 대안은 배포에 대한 신뢰도이다. 테스트를 실행한 후 배포할 만큼 테스트를 신뢰하면 좋은 것이다. 자주 배포할수록 테스트에 대한 신뢰도가 높아진다. 처음 몇 번은 믿음의 도약이 필요하지만, 프로덕션 버그를 수정하고 학습하는 것을 우선순위로 삼으면 올바른 방향으로 나아갈 수 있다. 테스트는 개발 중에 작성되어야 개발 도구가 되며 더 이상 잡일처럼 느껴지지 않는다. 새 필드를 추가할 때마다 테스트를 수정하는 데 한 시간을 소비한다면 뭔가 잘못된 것이며, 테스트가 코드 구조 변경에 너무 취약한 것이다.
참조: 페이지 74, 라인 554-574

### 중요 개념 간 관계

Test Pyramid는 Hexagonal Architecture Testing Strategy의 기반 원칙으로, Unit Test, Integration Test, System Test의 비율과 역할을 정의한다. Domain Entity Testing과 Use Case Testing은 Unit Test를 사용하며, Given/When/Then Pattern과 Mocking을 활용한다. Web Adapter Testing과 Persistence Adapter Testing은 Integration Test를 사용하며, Self-Validating Command와 Real Database Testing 개념이 적용된다. System Test는 Domain-Specific Language in Tests를 통해 가독성을 확보하고 실제 사용자 시나리오를 검증한다. Test Success Measurement는 Line Coverage vs Shipping Confidence 개념을 기반으로 하며, 테스트 전략의 실효성을 평가하는 기준이 된다. 헥사고날 아키텍처의 포트는 명확한 모킹 지점을 제공하여 모든 테스트 계층에서 테스트를 용이하게 하며, 테스트가 아키텍처 결함을 경고하는 카나리아 역할을 수행한다.

## 상세 내용

### 1. 테스트 전략의 필요성 (페이지 64, 라인 4-8)
많은 프로젝트에서 자동화된 테스트는 미스터리다. 모두가 위키에 문서화된 오래된 규칙 때문에 각자의 방식대로 테스트를 작성하지만, 팀의 테스트 전략에 대한 구체적인 질문에는 아무도 답하지 못한다. 이 장은 헥사고날 아키텍처를 위한 테스트 전략을 제공하며, 아키텍처의 각 요소를 커버할 테스트 타입을 논의한다.

### 2. The Test Pyramid (테스트 피라미드) (페이지 64-66, 라인 10-45)

**테스트 피라미드의 기본 개념**
테스트 피라미드는 어떤 타입의 테스트를 몇 개나 목표로 해야 하는지 결정하는 데 도움을 주는 메타포다. 기본 개념은 저렴하게 구축하고, 유지보수하기 쉽고, 빠르게 실행되며, 안정적인 세밀한 테스트(단위 테스트)로 높은 커버리지를 확보해야 한다는 것이다. 단위 테스트는 일반적으로 단일 "유닛"(보통 클래스)이 예상대로 작동하는지 검증한다.

테스트가 여러 유닛을 결합하고 유닛 경계, 아키텍처 경계, 심지어 시스템 경계를 넘어가면 구축 비용이 높아지고, 실행 속도가 느려지며, 더 취약해진다(기능 오류 대신 설정 오류로 실패). 피라미드는 이러한 테스트가 비용이 높아질수록 높은 커버리지를 목표로 하지 말아야 한다고 말한다. 그렇지 않으면 새로운 기능 구축 대신 테스트 구축에 너무 많은 시간을 소비하게 된다.

참조: 페이지 64-65, 라인 10-23

**테스트 피라미드의 레이어 정의**
컨텍스트에 따라 "단위 테스트", "통합 테스트", "시스템 테스트"의 정의가 달라질 수 있다. 이 장에서 사용할 해석은 다음과 같다:

- **Unit Tests (단위 테스트)**: 피라미드의 기반. 단일 클래스를 인스턴스화하고 그 인터페이스를 통해 기능을 테스트한다. 의존성이 있는 다른 클래스들은 인스턴스화하지 않고 모크로 대체하여 테스트 중 필요한 실제 클래스의 동작을 시뮬레이션한다.

- **Integration Tests (통합 테스트)**: 피라미드의 다음 레이어. 여러 유닛의 네트워크를 인스턴스화하고 진입점 클래스의 인터페이스를 통해 데이터를 전송하여 해당 네트워크가 예상대로 작동하는지 검증한다. 두 레이어 간 경계를 넘나들기 때문에 객체 네트워크가 완전하지 않거나 일부 지점에서 모크를 사용해야 한다.

- **System Tests (시스템 테스트)**: 마지막으로, 애플리케이션을 구성하는 전체 객체 네트워크를 시작하고 애플리케이션의 모든 레이어를 거쳐 특정 유스케이스가 예상대로 작동하는지 검증한다.

- **End-to-End Tests (엔드투엔드 테스트)**: 시스템 테스트 위에는 애플리케이션의 UI를 포함하는 엔드투엔드 테스트 레이어가 있을 수 있다. 이 책에서는 백엔드 아키텍처만 다루므로 엔드투엔드 테스트는 고려하지 않는다.

참조: 페이지 65-66, 라인 29-45

### 3. Testing a Domain Entity with Unit Tests (도메인 엔티티 단위 테스트) (페이지 66-67, 라인 46-107)

아키텍처 중심의 도메인 엔티티부터 살펴본다. Chapter 4의 Account 엔티티를 다시 떠올려보자. Account의 상태는 과거 특정 시점의 잔액(기준선 잔액)과 그 이후의 입출금 목록(활동)으로 구성된다.

이제 withdraw() 메서드가 예상대로 작동하는지 검증해보자:

```java
// Java 코드
class AccountTest {

    @Test
    void withdrawalSucceeds() {
        // Given: 특정 상태의 계좌 생성
        AccountId accountId = new AccountId(1L);
        Account account = defaultAccount()
            .withAccountId(accountId)
            .withBaselineBalance(Money.of(555L))
            .withActivityWindow(new ActivityWindow(
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(999L)).build(),
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(1L)).build()))
            .build();

        // When: 출금 실행
        boolean success = account.withdraw(Money.of(555L), new AccountId(99L));

        // Then: 검증
        assertThat(success).isTrue();
        assertThat(account.getActivityWindow().getActivities()).hasSize(3);
        assertThat(account.calculateBalance()).isEqualTo(Money.of(1000L));
    }
}
```

```python
# Python 버전
class AccountTest:

    def test_withdrawal_succeeds(self):
        """출금이 성공하는지 테스트"""
        # Given: 특정 상태의 계좌 생성
        account_id = AccountId(1)
        account = (AccountBuilder()
            .with_account_id(account_id)
            .with_baseline_balance(Money(555))
            .with_activity_window(ActivityWindow([
                ActivityBuilder()
                    .with_target_account(account_id)
                    .with_money(Money(999))
                    .build(),
                ActivityBuilder()
                    .with_target_account(account_id)
                    .with_money(Money(1))
                    .build()
            ]))
            .build())

        # When: 출금 실행
        success = account.withdraw(Money(555), AccountId(99))

        # Then: 검증
        assert success is True
        assert len(account.get_activity_window().get_activities()) == 3
        assert account.calculate_balance() == Money(1000)
```

위 테스트는 특정 상태의 Account를 인스턴스화하고, withdraw() 메서드를 호출한 후, 출금이 성공했는지와 테스트 중인 Account 객체의 상태에 예상되는 부수 효과가 발생했는지 검증하는 순수한 단위 테스트다.

테스트 설정이 쉽고, 이해하기 쉬우며, 매우 빠르게 실행된다. 이보다 간단한 테스트는 없다. 이와 같은 단위 테스트는 도메인 엔티티 내에 인코딩된 비즈니스 규칙을 검증하는 데 가장 적합하다. 도메인 엔티티 동작은 다른 클래스에 대한 의존성이 거의 없으므로 다른 타입의 테스트가 필요하지 않다.

참조: 페이지 66-67, 라인 46-107

### 4. Testing a Use Case with Unit Tests (유스케이스 단위 테스트) (페이지 67-68, 라인 108-213)

레이어를 한 단계 바깥으로 나가면 다음으로 테스트할 아키텍처 요소는 유스케이스다. Chapter 4의 SendMoneyService 테스트를 살펴보자. "Send Money" 유스케이스는 다른 트랜잭션이 그 사이에 잔액을 변경하지 못하도록 소스 계좌를 잠근다. 소스 계좌에서 돈을 성공적으로 출금할 수 있으면 타겟 계좌도 잠그고 그곳에 돈을 입금한다. 마지막으로 양쪽 계좌를 모두 잠금 해제한다.

트랜잭션이 성공할 때 모든 것이 예상대로 작동하는지 검증해보자:

```java
// Java 코드
class SendMoneyServiceTest {

    // 필드 선언 생략

    @Test
    void transactionSucceeds() {

        // Given: 소스/타겟 계좌 생성 및 상태 설정
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

        // Then: 검증
        assertThat(success).isTrue();

        AccountId sourceAccountId = sourceAccount.getId();
        AccountId targetAccountId = targetAccount.getId();

        // 계좌 잠금 및 출금 검증
        then(accountLock).should().lockAccount(eq(sourceAccountId));
        then(sourceAccount).should().withdraw(eq(money), eq(targetAccountId));
        then(accountLock).should().releaseAccount(eq(sourceAccountId));

        // 계좌 잠금 및 입금 검증
        then(accountLock).should().lockAccount(eq(targetAccountId));
        then(targetAccount).should().deposit(eq(money), eq(sourceAccountId));
        then(accountLock).should().releaseAccount(eq(targetAccountId));

        thenAccountsHaveBeenUpdated(sourceAccountId, targetAccountId);
    }

    // 헬퍼 메서드 생략
}
```

```python
# Python 버전 (pytest + unittest.mock 사용)
from unittest.mock import Mock, call
import pytest

class TestSendMoneyService:

    def test_transaction_succeeds(self):
        """트랜잭션이 성공하는지 테스트"""

        # Given: 소스/타겟 계좌 생성 및 상태 설정
        source_account = self._given_source_account()
        target_account = self._given_target_account()

        self._given_withdrawal_will_succeed(source_account)
        self._given_deposit_will_succeed(target_account)

        money = Money(500)

        command = SendMoneyCommand(
            source_account.get_id(),
            target_account.get_id(),
            money
        )

        # When: 송금 실행
        success = self.send_money_service.send_money(command)

        # Then: 검증
        assert success is True

        source_account_id = source_account.get_id()
        target_account_id = target_account.get_id()

        # 계좌 잠금 및 출금 검증
        self.account_lock.lock_account.assert_any_call(source_account_id)
        source_account.withdraw.assert_called_once_with(money, target_account_id)
        self.account_lock.release_account.assert_any_call(source_account_id)

        # 계좌 잠금 및 입금 검증
        self.account_lock.lock_account.assert_any_call(target_account_id)
        target_account.deposit.assert_called_once_with(money, source_account_id)
        self.account_lock.release_account.assert_any_call(target_account_id)

        self._then_accounts_have_been_updated(source_account_id, target_account_id)

    # 헬퍼 메서드들
    def _given_source_account(self):
        """소스 계좌 모크 생성"""
        return Mock()

    def _given_target_account(self):
        """타겟 계좌 모크 생성"""
        return Mock()

    def _given_withdrawal_will_succeed(self, account):
        """출금이 성공하도록 설정"""
        account.withdraw.return_value = True

    def _given_deposit_will_succeed(self, account):
        """입금이 성공하도록 설정"""
        account.deposit.return_value = True

    def _then_accounts_have_been_updated(self, source_id, target_id):
        """계좌가 업데이트되었는지 검증"""
        # 업데이트 검증 로직
        pass
```

테스트를 좀 더 읽기 쉽게 만들기 위해 Behavior-Driven Development에서 일반적으로 사용되는 given/when/then 섹션으로 구조화했다.

"given" 섹션에서는 소스 및 타겟 계좌를 생성하고 given...()으로 시작하는 메서드들로 올바른 상태로 만든다. 또한 유스케이스의 입력으로 사용할 SendMoneyCommand를 생성한다. "when" 섹션에서는 sendMoney() 메서드를 호출하여 유스케이스를 실행한다. "then" 섹션에서는 트랜잭션이 성공했는지 확인하고 소스/타겟 계좌와 계좌 잠금을 담당하는 AccountLock 인스턴스에서 특정 메서드들이 호출되었는지 검증한다.

내부적으로 테스트는 Mockito 라이브러리를 사용하여 given...() 메서드에서 모크 객체를 생성한다. Mockito는 모크 객체에서 특정 메서드가 호출되었는지 검증하는 then() 메서드도 제공한다.

테스트 중인 유스케이스 서비스는 상태가 없으므로 "then" 섹션에서 특정 상태를 검증할 수 없다. 대신 테스트는 서비스가 (모크된) 의존성의 특정 메서드들과 상호작용했는지 검증한다. 이는 테스트가 테스트 중인 코드의 구조 변경에 취약하며 동작만 검증하는 것이 아님을 의미한다. 즉, 테스트 중인 코드를 리팩토링하면 테스트도 수정해야 할 가능성이 높다.

이를 염두에 두고 테스트에서 실제로 검증하고자 하는 상호작용에 대해 신중하게 생각해야 한다. 위 테스트처럼 모든 상호작용을 검증하는 것보다 가장 중요한 것들에 집중하는 것이 좋은 아이디어일 수 있다. 그렇지 않으면 테스트 중인 클래스를 변경할 때마다 테스트를 변경해야 하며, 이는 테스트의 가치를 약화시킨다.

이 테스트는 여전히 단위 테스트지만 의존성과의 상호작용을 테스트하기 때문에 통합 테스트에 가깝다. 하지만 모크를 사용하고 실제 의존성을 관리할 필요가 없기 때문에 완전한 통합 테스트보다 생성 및 유지보수가 쉽다.

참조: 페이지 67-68, 라인 108-213

### 5. Testing a Web Adapter with Integration Tests (웹 어댑터 통합 테스트) (페이지 68-69, 라인 214-294)

또 다른 레이어를 바깥으로 나가면 어댑터에 도달한다. 웹 어댑터 테스트를 논의해보자.

웹 어댑터는 예를 들어 JSON 문자열 형식의 입력을 HTTP를 통해 받고, 검증을 수행하고, 유스케이스가 기대하는 형식으로 입력을 매핑한 후 유스케이스에 전달한다는 점을 기억하자. 그런 다음 유스케이스의 결과를 다시 JSON으로 매핑하여 HTTP 응답을 통해 클라이언트에 반환한다.

웹 어댑터 테스트에서는 이러한 모든 단계가 예상대로 작동하는지 확인하고자 한다:

```java
// Java 코드 (Spring Boot 프레임워크)
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
# Python 버전 (Flask + pytest 사용 예시)
from flask import Flask
from unittest.mock import Mock, patch
import pytest
import json

class TestSendMoneyController:

    @pytest.fixture
    def client(self):
        """Flask 테스트 클라이언트 생성"""
        app = Flask(__name__)
        # 컨트롤러 등록
        from controllers import send_money_controller
        app.register_blueprint(send_money_controller)
        return app.test_client()

    @patch('controllers.send_money_use_case')
    def test_send_money(self, mock_use_case, client):
        """송금 API 테스트"""

        # When: HTTP POST 요청 전송
        response = client.post(
            '/accounts/sendMoney/41/42/500',
            headers={'Content-Type': 'application/json'}
        )

        # Then: HTTP 응답 상태 검증
        assert response.status_code == 200

        # Then: 유스케이스가 올바른 커맨드로 호출되었는지 검증
        expected_command = SendMoneyCommand(
            AccountId(41),
            AccountId(42),
            Money(500)
        )
        mock_use_case.send_money.assert_called_once_with(expected_command)
```

위 테스트는 Spring Boot 프레임워크로 구축된 SendMoneyController라는 웹 컨트롤러를 위한 표준 통합 테스트다. testSendMoney() 메서드에서 입력 객체를 생성하고 웹 컨트롤러에 모크 HTTP 요청을 전송한다. 요청 본문에는 입력 객체가 JSON 문자열로 포함된다.

isOk() 메서드로 HTTP 응답의 상태가 200인지 확인하고, 모크된 유스케이스 클래스가 호출되었는지 검증한다.

웹 어댑터의 대부분의 책임이 이 테스트에 의해 커버된다.

MockMvc 객체로 HTTP 프로토콜을 모킹했기 때문에 실제로 HTTP 프로토콜을 통해 테스트하지는 않는다. 프레임워크가 HTTP로/로부터 모든 것을 올바르게 변환한다고 믿는다. 프레임워크를 테스트할 필요는 없다.

하지만 JSON에서 SendMoneyCommand 객체로 입력을 매핑하는 전체 경로는 커버된다. Chapter 4에서 설명한 대로 SendMoneyCommand 객체를 자기 검증 커맨드로 구축했다면 이 매핑이 유스케이스에 구문적으로 유효한 입력을 생성함을 확인한 것이다. 또한 유스케이스가 실제로 호출되었는지와 HTTP 응답이 예상 상태를 가지는지 검증했다.

그렇다면 이것이 단위 테스트가 아니라 통합 테스트인 이유는 무엇일까? 이 테스트에서 단일 웹 컨트롤러 클래스만 테스트하는 것처럼 보이지만 내부적으로는 훨씬 더 많은 일이 일어난다. @WebMvcTest 어노테이션으로 Spring에게 특정 요청 경로에 응답하고, Java와 JSON 간 매핑하고, HTTP 입력을 검증하는 등의 역할을 하는 전체 객체 네트워크를 인스턴스화하라고 지시한다. 그리고 이 테스트에서 우리는 웹 컨트롤러가 이 네트워크의 일부로서 작동하는지 검증한다.

웹 컨트롤러는 Spring 프레임워크에 강하게 바인딩되어 있으므로 격리된 상태가 아니라 프레임워크에 통합된 상태로 테스트하는 것이 합리적이다. 순수한 단위 테스트로 웹 컨트롤러를 테스트했다면 모든 매핑, 검증, HTTP 관련 커버리지를 잃게 되며, 프로덕션 환경에서 실제로 작동할지 확신할 수 없게 된다. 프로덕션에서는 프레임워크 기계의 톱니바퀴 중 하나일 뿐이기 때문이다.

참조: 페이지 68-69, 라인 214-294

### 6. Testing a Persistence Adapter with Integration Tests (영속성 어댑터 통합 테스트) (페이지 69-71, 라인 295-408)

비슷한 이유로 영속성 어댑터를 단위 테스트가 아니라 통합 테스트로 커버하는 것이 합리적이다. 어댑터 내부의 로직뿐만 아니라 데이터베이스로의 매핑도 검증하고자 하기 때문이다.

Chapter 6에서 구축한 영속성 어댑터를 테스트하고자 한다. 어댑터는 두 개의 메서드를 가지는데, 하나는 데이터베이스에서 Account 엔티티를 로드하고 다른 하나는 새로운 계좌 활동을 데이터베이스에 저장한다:

```java
// Java 코드 (Spring Data JPA)
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
        // When: 계좌 로드
        Account account = adapter.loadAccount(
            new AccountId(1L),
            LocalDateTime.of(2018, 8, 10, 0, 0));

        // Then: 로드된 계좌 상태 검증
        assertThat(account.getActivityWindow().getActivities()).hasSize(2);
        assertThat(account.calculateBalance()).isEqualTo(Money.of(500));
    }

    @Test
    void updatesActivities() {
        // Given: 새로운 활동이 있는 계좌 생성
        Account account = defaultAccount()
            .withBaselineBalance(Money.of(555L))
            .withActivityWindow(new ActivityWindow(
                defaultActivity()
                    .withId(null)
                    .withMoney(Money.of(1L)).build()))
            .build();

        // When: 활동 업데이트
        adapter.updateActivities(account);

        // Then: 활동이 저장되었는지 검증
        assertThat(activityRepository.count()).isEqualTo(1);

        ActivityJpaEntity savedActivity = activityRepository.findAll().get(0);
        assertThat(savedActivity.getAmount()).isEqualTo(1L);
    }

}
```

```python
# Python 버전 (SQLAlchemy + pytest)
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestAccountPersistenceAdapter:

    @pytest.fixture
    def db_session(self):
        """테스트용 데이터베이스 세션 생성"""
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        session = Session()
        # 테이블 생성
        Base.metadata.create_all(engine)
        yield session
        session.close()

    @pytest.fixture
    def adapter(self, db_session):
        """영속성 어댑터 인스턴스 생성"""
        return AccountPersistenceAdapter(db_session)

    @pytest.fixture
    def activity_repository(self, db_session):
        """활동 리포지토리 인스턴스 생성"""
        return ActivityRepository(db_session)

    def test_loads_account(self, adapter, db_session):
        """계좌 로드 테스트"""
        # Given: SQL 스크립트로 데이터베이스 초기화
        self._execute_sql_script(db_session, "AccountPersistenceAdapterTest.sql")

        # When: 계좌 로드
        account = adapter.load_account(
            AccountId(1),
            datetime(2018, 8, 10, 0, 0)
        )

        # Then: 로드된 계좌 상태 검증
        assert len(account.get_activity_window().get_activities()) == 2
        assert account.calculate_balance() == Money(500)

    def test_updates_activities(self, adapter, activity_repository):
        """활동 업데이트 테스트"""
        # Given: 새로운 활동이 있는 계좌 생성
        account = (AccountBuilder()
            .with_baseline_balance(Money(555))
            .with_activity_window(ActivityWindow([
                ActivityBuilder()
                    .with_id(None)
                    .with_money(Money(1))
                    .build()
            ]))
            .build())

        # When: 활동 업데이트
        adapter.update_activities(account)

        # Then: 활동이 저장되었는지 검증
        assert activity_repository.count() == 1

        saved_activity = activity_repository.find_all()[0]
        assert saved_activity.amount == 1

    def _execute_sql_script(self, session, script_path):
        """SQL 스크립트 실행"""
        with open(script_path) as f:
            session.execute(f.read())
        session.commit()
```

@DataJpaTest로 Spring에게 데이터베이스 접근에 필요한 객체 네트워크를 인스턴스화하라고 지시한다. 여기에는 데이터베이스에 연결하는 Spring Data 리포지토리들이 포함된다. 추가로 @Import를 사용하여 특정 객체들을 네트워크에 추가한다. 이러한 객체들은 테스트 중인 어댑터가 도메인 객체를 데이터베이스 객체로 매핑하는 데 필요하다.

loadAccount() 메서드 테스트에서는 SQL 스크립트를 사용하여 데이터베이스를 특정 상태로 만든다. 그런 다음 어댑터 API를 통해 계좌를 로드하고 SQL 스크립트의 데이터베이스 상태를 고려할 때 예상되는 상태를 가지는지 검증한다.

updateActivities() 테스트는 반대 방향으로 진행된다. 새로운 계좌 활동이 있는 Account 객체를 생성하고 어댑터에 전달하여 영속화한다. 그런 다음 ActivityRepository의 API를 통해 활동이 데이터베이스에 저장되었는지 확인한다.

이러한 테스트의 중요한 측면은 데이터베이스를 모킹하지 않는다는 것이다. 테스트가 실제로 데이터베이스에 접근한다. 데이터베이스를 모킹했다면 테스트가 여전히 동일한 코드 라인을 커버하여 동일한 높은 라인 커버리지를 생성하지만, 이러한 높은 커버리지에도 불구하고 SQL 문의 오류나 예상치 못한 매핑 오류로 인해 실제 데이터베이스를 사용하는 환경에서 실패할 가능성이 상당히 높다.

기본적으로 Spring은 테스트 중에 사용할 인메모리 데이터베이스를 시작한다. 아무것도 설정할 필요가 없고 테스트가 바로 작동하므로 매우 실용적이다.

하지만 이 인메모리 데이터베이스는 프로덕션에서 사용하는 데이터베이스가 아닐 가능성이 높으므로, 테스트가 인메모리 데이터베이스에 대해 완벽하게 작동해도 실제 데이터베이스에서는 문제가 발생할 가능성이 여전히 상당하다. 데이터베이스들은 각자의 SQL 방언을 구현하는 것을 좋아하기 때문이다.

이러한 이유로 영속성 어댑터 테스트는 실제 데이터베이스에 대해 실행되어야 한다. Testcontainers 같은 라이브러리는 이와 관련하여 큰 도움이 되며, 요청 시 Docker 컨테이너에서 데이터베이스를 실행한다.

실제 데이터베이스에 대해 실행하면 두 개의 다른 데이터베이스 시스템을 관리할 필요가 없다는 추가 이점이 있다. 테스트 중에 인메모리 데이터베이스를 사용하는 경우 특정 방식으로 구성해야 하거나 각 데이터베이스에 대한 별도 버전의 데이터베이스 마이그레이션 스크립트를 만들어야 할 수 있으며, 이는 전혀 재미있지 않다.

참조: 페이지 69-71, 라인 295-408

### 7. Testing Main Paths with System Tests (시스템 테스트로 주요 경로 테스트) (페이지 71-74, 라인 409-547)

피라미드 꼭대기에는 시스템 테스트가 있다. 시스템 테스트는 전체 애플리케이션을 시작하고 API에 대한 요청을 실행하여 모든 레이어가 조화롭게 작동하는지 검증한다.

"Send Money" 유스케이스를 위한 시스템 테스트에서는 애플리케이션에 HTTP 요청을 전송하고 응답과 계좌의 새로운 잔액을 검증한다:

```java
// Java 코드 (Spring Boot)
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class SendMoneySystemTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    @Sql("SendMoneySystemTest.sql")
    void sendMoney() {

        // Given: 초기 잔액 확인
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

        // Then: 소스 계좌 잔액 검증
        then(sourceAccount().calculateBalance())
            .isEqualTo(initialSourceBalance.minus(transferredAmount()));

        // Then: 타겟 계좌 잔액 검증
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
# Python 버전 (Flask + pytest)
import pytest
from flask import Flask
import requests

class TestSendMoneySystem:

    @pytest.fixture
    def app(self):
        """Flask 애플리케이션 시작"""
        app = create_app()
        return app

    @pytest.fixture
    def client(self, app):
        """테스트 클라이언트 생성"""
        return app.test_client()

    @pytest.fixture
    def db_session(self, app):
        """데이터베이스 세션"""
        with app.app_context():
            db.create_all()
            yield db.session
            db.drop_all()

    def test_send_money(self, client, db_session):
        """송금 시스템 테스트"""
        # Given: SQL 스크립트로 초기 데이터 설정
        self._execute_sql_script(db_session, "SendMoneySystemTest.sql")

        initial_source_balance = self._source_account().calculate_balance()
        initial_target_balance = self._target_account().calculate_balance()

        # When: HTTP POST 요청 전송
        response = self._when_send_money(
            client,
            self._source_account_id(),
            self._target_account_id(),
            self._transferred_amount()
        )

        # Then: 응답 상태 검증
        assert response.status_code == 200

        # Then: 소스 계좌 잔액 검증
        assert (self._source_account().calculate_balance() ==
                initial_source_balance - self._transferred_amount())

        # Then: 타겟 계좌 잔액 검증
        assert (self._target_account().calculate_balance() ==
                initial_target_balance + self._transferred_amount())

    def _when_send_money(self, client, source_id, target_id, amount):
        """송금 요청 전송 헬퍼 메서드"""
        return client.post(
            f'/accounts/sendMoney/{source_id}/{target_id}/{amount}',
            headers={'Content-Type': 'application/json'}
        )

    def _source_account(self):
        """소스 계좌 조회"""
        # 데이터베이스에서 소스 계좌 조회
        pass

    def _target_account(self):
        """타겟 계좌 조회"""
        # 데이터베이스에서 타겟 계좌 조회
        pass

    def _source_account_id(self):
        """소스 계좌 ID 반환"""
        pass

    def _target_account_id(self):
        """타겟 계좌 ID 반환"""
        pass

    def _transferred_amount(self):
        """송금 금액 반환"""
        return Money(500)

    def _execute_sql_script(self, session, script_path):
        """SQL 스크립트 실행"""
        with open(script_path) as f:
            session.execute(f.read())
        session.commit()
```

@SpringBootTest로 Spring에게 애플리케이션을 구성하는 전체 객체 네트워크를 시작하라고 지시한다. 또한 애플리케이션이 무작위 포트에 노출되도록 구성한다.

테스트 메서드에서는 요청을 생성하고 애플리케이션에 전송한 후 응답 상태와 계좌의 새로운 잔액을 확인한다.

요청 전송에 앞서 웹 어댑터 테스트에서 사용한 MockMvc가 아니라 TestRestTemplate을 사용한다. 이는 실제 HTTP를 수행한다는 것을 의미하며, 테스트를 프로덕션 환경에 조금 더 가깝게 만든다.

실제 HTTP를 거치는 것처럼 실제 출력 어댑터도 거친다. 우리의 경우 이것은 애플리케이션을 데이터베이스에 연결하는 영속성 어댑터뿐이다. 다른 시스템과 대화하는 애플리케이션에는 추가 출력 어댑터가 있을 것이다. 시스템 테스트라도 모든 타사 시스템을 가동하는 것이 항상 가능한 것은 아니므로 결국 일부를 모킹할 수 있다. 헥사고날 아키텍처는 몇 개의 출력 포트 인터페이스만 스텁하면 되므로 이를 최대한 쉽게 만든다.

테스트를 최대한 읽기 쉽게 만들기 위해 모든 못생긴 로직을 헬퍼 메서드 내부에 숨겼다는 점에 주목하라. 이제 이러한 메서드들은 사물의 상태를 검증하는 데 사용할 수 있는 도메인 특화 언어를 형성한다.

도메인 특화 언어와 같은 것은 모든 타입의 테스트에서 좋은 아이디어지만, 시스템 테스트에서는 훨씬 더 중요하다. 시스템 테스트는 단위 테스트나 통합 테스트보다 애플리케이션의 실제 사용자를 훨씬 더 잘 시뮬레이션하므로 사용자의 관점에서 애플리케이션을 검증하는 데 사용할 수 있다. 이는 적절한 어휘를 갖추면 훨씬 쉽다. 이 어휘는 또한 사용자를 가장 잘 구현할 수 있고 아마도 프로그래머가 아닐 수 있는 도메인 전문가가 테스트에 대해 추론하고 피드백을 제공할 수 있게 한다. JGiven 같은 behavior-driven development를 위한 전체 라이브러리가 테스트를 위한 어휘를 만드는 프레임워크를 제공한다.

이전 섹션에서 설명한 대로 단위 및 통합 테스트를 만들었다면 시스템 테스트는 동일한 코드의 많은 부분을 커버할 것이다. 추가적인 이점을 제공하기는 할까? 그렇다. 일반적으로 단위 및 통합 테스트와는 다른 타입의 버그를 찾아낸다. 예를 들어 레이어 간의 일부 매핑이 잘못되었을 수 있으며, 이는 단위 및 통합 테스트만으로는 발견하지 못할 것이다.

시스템 테스트는 여러 유스케이스를 결합하여 시나리오를 생성할 때 강점을 가장 잘 발휘한다. 각 시나리오는 사용자가 일반적으로 애플리케이션을 거쳐갈 수 있는 특정 경로를 나타낸다. 가장 중요한 시나리오들이 통과하는 시스템 테스트로 커버되면 최신 수정사항으로 인해 문제가 발생하지 않았다고 가정하고 배포할 준비가 된 것이다.

참조: 페이지 71-74, 라인 409-547

### 8. How Much Testing is Enough? (얼마나 테스트해야 충분한가?) (페이지 74, 라인 548-574)

많은 프로젝트 팀이 답하지 못하는 질문은 얼마나 테스트해야 하는가 하는 것이다. 테스트가 코드 라인의 80%를 커버하면 충분한가? 더 높아야 하는가?

라인 커버리지는 테스트 성공을 측정하는 나쁜 지표다. 100% 이외의 목표는 완전히 무의미하다. 왜냐하면 코드베이스의 중요한 부분이 전혀 커버되지 않을 수 있기 때문이다. 그리고 100%에서도 모든 버그가 해결되었다고 확신할 수 없다.

필자는 테스트 성공을 소프트웨어를 배포할 때 얼마나 편안하게 느끼는지로 측정할 것을 제안한다. 테스트를 실행한 후 배포할 만큼 테스트를 신뢰한다면 좋은 것이다. 자주 배포할수록 테스트에 대한 신뢰도가 높아진다. 1년에 두 번만 배포한다면 아무도 테스트를 신뢰하지 않을 것이다. 테스트가 1년에 두 번만 스스로를 증명하기 때문이다.

이는 처음 몇 번 배포할 때 믿음의 도약이 필요하지만, 프로덕션에서 버그를 수정하고 학습하는 것을 우선순위로 삼으면 올바른 방향으로 나아가고 있는 것이다. 각 프로덕션 버그에 대해 "왜 우리 테스트가 이 버그를 잡지 못했는가?"라는 질문을 하고, 답을 문서화하고, 해당 버그를 커버하는 테스트를 추가해야 한다. 시간이 지남에 따라 이는 배포에 대해 편안하게 느끼게 만들 것이며 문서화는 시간 경과에 따른 개선을 측정하는 지표도 제공할 것이다.

하지만 만들어야 할 테스트를 정의하는 전략으로 시작하는 것이 도움이 된다. 헥사고날 아키텍처를 위한 한 가지 전략은 다음과 같다:

- 도메인 엔티티를 구현하는 동안 단위 테스트로 커버한다
- 유스케이스를 구현하는 동안 단위 테스트로 커버한다
- 어댑터를 구현하는 동안 통합 테스트로 커버한다
- 사용자가 애플리케이션을 거쳐갈 수 있는 가장 중요한 경로를 시스템 테스트로 커버한다

"구현하는 동안"이라는 단어에 주목하라: 테스트가 기능 개발 후가 아니라 개발 중에 수행되면 개발 도구가 되며 더 이상 잡일처럼 느껴지지 않는다.

하지만 새 필드를 추가할 때마다 테스트를 수정하는 데 한 시간을 소비해야 한다면 뭔가 잘못하고 있는 것이다. 아마도 테스트가 테스트 중인 코드의 구조 변경에 너무 취약하며, 이를 개선하는 방법을 살펴봐야 한다. 리팩토링할 때마다 테스트를 수정해야 한다면 테스트는 그 가치를 잃는다.

참조: 페이지 74, 라인 548-574

### 9. How Does This Help Me Build Maintainable Software? (유지보수 가능한 소프트웨어 구축에 어떻게 도움이 되는가?) (페이지 75, 라인 575-591)

헥사고날 아키텍처 스타일은 도메인 로직과 외부 대면 어댑터 사이를 명확하게 분리한다. 이는 중심 도메인 로직을 단위 테스트로, 어댑터를 통합 테스트로 커버하는 명확한 테스트 전략을 정의하는 데 도움을 준다.

입력 및 출력 포트는 테스트에서 매우 명확한 모킹 지점을 제공한다. 각 포트에 대해 모킹할지 실제 구현을 사용할지 결정할 수 있다. 포트가 각각 매우 작고 집중되어 있으면 모킹이 잡일이 아니라 수월해진다. 포트 인터페이스가 제공하는 메서드가 적을수록 테스트에서 어떤 메서드를 모킹해야 하는지에 대한 혼란이 줄어든다.

어떤 것을 모킹하는 것이 너무 부담스럽거나 코드베이스의 특정 부분을 커버하기 위해 어떤 종류의 테스트를 사용해야 하는지 모르겠다면 이는 경고 신호다. 이런 점에서 테스트는 카나리아로서 추가 책임이 있다 - 아키텍처의 결함에 대해 경고하고 유지보수 가능한 코드베이스를 만드는 길로 우리를 되돌려 놓는 것이다.

참조: 페이지 75, 라인 575-591
