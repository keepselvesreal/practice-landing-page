# Get_Your_Hands_Dirty_on_Clean_Architecture

## 압축 내용

Hexagonal Architecture는 Use Case 4단계 구조와 전용 Input/Output 모델로 도메인 로직을 구현하고(4장), 웹 어댑터가 HTTP를 유스케이스 호출로 변환하며(5장), 영속성 어댑터가 의존성 역전을 통해 도메인을 영속성 세부사항으로부터 분리하고(6장), 테스트 피라미드에 따라 각 계층을 적절한 테스트 유형으로 커버하며(7장), Configuration Component가 의존성 주입을 통해 모든 객체를 조립하고(9장), visibility modifiers, post-compile checks, build artifacts를 통해 아키텍처 경계를 강제한다(10장).

## 핵심 내용

### 핵심 개념들
- **Use Case 구현 패턴** → 상세 내용: 4장
- **Adapter 패턴 (Web/Persistence)** → 상세 내용: 5장, 6장
- **계층별 테스트 전략** → 상세 내용: 7장
- **의존성 주입과 조립** → 상세 내용: 9장
- **아키텍처 경계 강제** → 상세 내용: 10장

### 핵심 개념 설명

**Use Case 구현 패턴** (참조: 4장)
Use Case는 Input Validation(입력 모델), Business Rule Validation(도메인 엔티티/Use Case), Domain State Manipulation(도메인 엔티티), Output Return(최소한의 출력)의 4단계로 구현되며, 각 Use Case마다 전용 Input/Output 모델을 사용하여 결합도를 낮추고 유지보수성을 높인다. Constructor 기반 불변성과 검증을 통해 안전한 객체 생성을 보장하며, Query Service 패턴으로 읽기 전용 작업을 분리한다.

**Adapter 패턴 (Web/Persistence)** (참조: 5장, 6장)
웹 어댑터는 HTTP 요청을 유스케이스 호출로 변환하고 HTTP 관련 책임(요청/응답 매핑, 인증/인가, 입력 검증)을 애플리케이션 계층과 분리하며, 컨트롤러를 유스케이스별로 세분화한다. 영속성 어댑터는 의존성 역전 원칙을 통해 애플리케이션 코어의 플러그인으로 구현되며, 인터페이스 분리 원칙에 따라 좁은 포트 인터페이스를 제공하고, 도메인 모델과 데이터베이스 모델 간 매핑을 담당하여 도메인 로직을 영속성 세부사항으로부터 독립시킨다.

**계층별 테스트 전략** (참조: 7장)
테스트 피라미드에 따라 도메인 엔티티는 단위 테스트로 비즈니스 규칙을 검증하고, 유스케이스는 모킹을 활용한 단위 테스트로 오케스트레이션을 검증하며, 어댑터는 프레임워크와 통합된 통합 테스트로 매핑과 통합을 검증하고, 핵심 시나리오는 시스템 테스트로 전체 계층의 협력을 검증한다. 테스트 성공은 라인 커버리지가 아닌 배포에 대한 자신감으로 측정하며, 프로덕션 버그로부터 지속적으로 학습한다.

**의존성 주입과 조립** (참조: 9장)
Configuration Component는 아키텍처에 중립적이며 모든 클래스에 대한 의존성을 가지는 컴포넌트로, 의존성 주입을 통해 use case, adapter, domain 객체를 인스턴스화하고 연결한다. Plain Code, Classpath Scanning, Java Config의 세 가지 조립 방식이 있으며, Java Config는 프레임워크 독립성과 유연한 모듈 구성을 제공하면서도 명시적 제어가 가능하다.

**아키텍처 경계 강제** (참조: 10장)
의존성이 올바른 방향(내부로)을 가리키도록 보장하기 위해 세 가지 접근 방식을 사용한다. Visibility modifiers(package-private)는 패키지 수준에서 기본적인 경계를 제공하고, Post-compile checks(ArchUnit)는 public 클래스의 잘못된 의존성을 런타임에 검증하며, Build artifacts(모듈 분리)는 빌드 수준에서 의존성을 명시적으로 제어하고 순환 의존성을 방지한다.

### 핵심 개념 간 관계

**Use Case 구현 패턴**은 Hexagonal Architecture의 중심이며, **Adapter 패턴**은 이 Use Case를 외부 세계(웹, 데이터베이스)와 연결한다. **의존성 주입과 조립**은 Use Case와 Adapter를 런타임에 연결하여 의존성 역전을 실현하고, **아키텍처 경계 강제**는 이러한 의존성이 올바른 방향을 유지하도록 보장한다. **계층별 테스트 전략**은 각 계층(도메인, Use Case, Adapter)의 특성에 맞는 테스트 방법을 제공하여 전체 아키텍처의 품질을 검증한다. 이 다섯 개념이 함께 작동하여 유지보수 가능하고 테스트 가능한 Hexagonal Architecture를 구성한다.

---

# 4. Implementing a Use Case

## 압축 내용

Hexagonal Architecture의 Use Case는 Input Validation(입력 모델), Business Rule Validation(도메인 엔티티/Use Case), Domain State Manipulation(도메인 엔티티), Output Return(최소한의 출력)의 4단계로 구현되며, 각 Use Case마다 전용 Input/Output 모델을 사용하여 결합도를 낮추고 유지보수성을 높인다.

## 핵심 내용

### 핵심 개념들
- **Use Case 4단계 구조** → 상세 내용: Use Case 구조
- **Input Validation vs Business Rule Validation 분리** → 상세 내용: Input Validation, Business Rule Validation
- **Use Case별 전용 Input/Output 모델** → 상세 내용: Use Case별 Input Model 분리, Use Case별 Output Model 분리
- **Domain Model 구현 방식** → 상세 내용: Domain Model 구현, Rich vs Anemic Domain Model
- **Constructor 기반 불변성과 검증** → 상세 내용: Constructor 활용
- **Query Service 패턴** → 상세 내용: Read-Only Use Cases

### 핵심 개념 설명

**Use Case 4단계 구조** (참조: Line 130-196)
Use Case는 (1) Input 받기, (2) 비즈니스 규칙 검증, (3) 모델 상태 조작, (4) Output 반환의 4단계로 실행된다. Input Validation은 Use Case 클래스가 아닌 Input 모델에서 처리하고, Business Rule Validation은 도메인 엔티티나 Use Case에서 처리한다.

**Input Validation vs Business Rule Validation 분리** (참조: Line 200-363, 428-521)
Input Validation은 도메인 모델 상태 접근 없이 선언적으로 검증 가능한 구문적(syntactical) 검증이며, Business Rule Validation은 도메인 모델의 현재 상태에 접근이 필요한 의미적(semantical) 검증이다. 예: "송금액 > 0"은 Input Validation, "출금 계좌 잔액 부족 여부"는 Business Rule Validation.

**Use Case별 전용 Input/Output 모델** (참조: Line 403-427, 548-575)
각 Use Case마다 전용 Input/Output 모델을 사용하면 Use Case 간 결합도가 낮아지고 의도가 명확해진다. 공유 모델은 시간이 지나면서 비대해지고, 한 Use Case의 변경이 다른 Use Case에 영향을 준다.

**Domain Model 구현 방식** (참조: Line 12-129, 522-547)
Rich Domain Model은 도메인 로직을 엔티티에 최대한 포함시키고 Use Case는 오케스트레이션만 담당한다. Anemic Domain Model은 엔티티가 상태와 getter/setter만 가지고, Use Case가 도메인 로직을 포함한다. 두 방식 모두 Hexagonal Architecture에서 구현 가능하다.

**Constructor 기반 불변성과 검증** (참조: Line 364-402)
불변(immutable) Input 모델은 생성자에서 모든 필드를 초기화하고 검증한다. Builder 패턴 대신 생성자를 직접 사용하면 필드 추가/삭제 시 컴파일 에러로 모든 호출부를 추적할 수 있어 안전하다.

**Query Service 패턴** (참조: Line 576-625)
읽기 전용 작업은 Use Case가 아닌 Query로 구분하여 Query Service로 구현한다. 이는 CQS(Command-Query Separation)와 CQRS(Command-Query Responsibility Segregation) 개념과 잘 맞는다.

### 핵심 개념 간 관계

**Use Case 4단계 구조**는 **Input Validation vs Business Rule Validation 분리**를 통해 각 단계의 책임을 명확히 한다. **Use Case별 전용 Input/Output 모델**은 **Use Case 4단계 구조**의 Input/Output 단계를 구체화하고 결합도를 낮춘다. **Constructor 기반 불변성과 검증**은 **Input Validation**을 안전하고 명확하게 구현하는 방법이다. **Domain Model 구현 방식**은 **Business Rule Validation**이 엔티티 또는 Use Case 중 어디에 위치할지를 결정한다. **Query Service 패턴**은 **Use Case 4단계 구조** 중 상태 변경이 없는 읽기 전용 작업을 별도로 분리한 것이다.

## 상세 내용

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

---

# 5. Implementing a Web Adapter

## 압축 내용

웹 어댑터는 의존성 역전 원칙을 활용하여 HTTP 요청을 애플리케이션 코어의 유스케이스 호출로 변환하고, HTTP 관련 책임(요청/응답 매핑, 인증/인가, 입력 검증)을 애플리케이션 계층과 분리하며, 컨트롤러를 유스케이스별로 세분화하여 유지보수성과 병렬 작업을 개선한다.

## 핵심 내용

### 핵심 개념들
- **의존성 역전 원칙(Dependency Inversion Principle)** → 상세 내용: 의존성 역전 섹션
- **웹 어댑터의 책임(Web Adapter Responsibilities)** → 상세 내용: 웹 어댑터의 책임 섹션
- **컨트롤러 슬라이싱(Controller Slicing)** → 상세 내용: 컨트롤러 슬라이싱 섹션

### 핵심 개념 설명

**의존성 역전 원칙** (참조: 페이지 45-47, 라인 8-47)
웹 어댑터는 incoming(driving) 어댑터로서 외부 요청을 애플리케이션 코어로 전달하며, 포트(port) 인터페이스를 통해 애플리케이션 서비스와 통신하여 외부와의 상호작용 지점을 명확히 정의한다. 양방향 통신이 필요한 경우(예: 웹소켓) outgoing 포트를 사용하여 의존성 방향을 유지한다.

**웹 어댑터의 책임** (참조: 페이지 47-48, 라인 48-91)
7가지 핵심 책임: HTTP 요청 매핑, 인증/인가, 입력 검증, 유스케이스 입력 모델 변환, 유스케이스 호출, 출력 HTTP 매핑, HTTP 응답 반환. HTTP 관련 세부사항은 애플리케이션 계층으로 누출되지 않아야 하며, 도메인 계층과 애플리케이션 계층부터 개발 시작 시 자연스러운 경계가 형성된다.

**컨트롤러 슬라이싱** (참조: 페이지 48-51, 라인 92-277)
단일 큰 컨트롤러보다 유스케이스별 작은 컨트롤러를 선호하며, 각 컨트롤러는 전용 모델을 사용하여 불필요한 데이터 구조 공유를 방지한다. 유스케이스를 반영한 명확한 네이밍(예: CreateAccount 대신 RegisterAccount)을 사용하고, 병렬 작업이 용이하며 머지 충돌을 감소시킨다.

### 핵심 개념 간 관계

**의존성 역전 원칙**은 웹 어댑터 아키텍처의 기반이 되며, 이를 통해 **웹 어댑터의 책임**이 명확하게 정의된다. 이러한 책임들은 **컨트롤러 슬라이싱** 기법을 통해 실제 구현으로 구체화되며, 세 개념이 함께 작동하여 유지보수 가능하고 테스트 가능한 웹 계층을 구성한다.

## 상세 내용

### 목차
1. 의존성 역전
2. 웹 어댑터의 책임
3. 컨트롤러 슬라이싱
4. 유지보수 가능한 소프트웨어 구축 방법

---

# 6. Implementing a Persistence Adapter

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
영속성 어댑터는 애플리케이션 서비스에 영속성 기능을 제공하는 "driven" 또는 "outgoing" 어댑터이며, 애플리케이션 서비스는 포트 인터페이스를 통해 영속성 기능에 접근한다. 포트는 애플리케이션 서비스와 영속성 코드 사이의 간접 계층으로 작동하여 도메인 코드를 영속성 세부사항으로부터 독립시키며, 포트 계약이 충족되는 한 영속성 어댑터 내부를 자유롭게 변경할 수 있다.

**포트 인터페이스 슬라이싱** (참조: 페이지 54-55, 라인 67-104)
인터페이스 분리 원칙(Interface Segregation Principle)을 적용하여 넓은 인터페이스를 특화된 인터페이스로 분할한다. 각 서비스는 실제로 필요한 메서드만 의존하여 불필요한 의존성을 제거하고, "메서드 하나당 포트 하나" 접근 방식으로 플러그 앤 플레이 경험을 제공하며, 테스트 시 어떤 메서드를 모킹할지 명확해진다.

**영속성 어댑터 슬라이싱** (참조: 페이지 55-57, 라인 105-137)
단일 영속성 어댑터 클래스 대신 여러 어댑터 클래스를 생성할 수 있으며, 도메인 클래스(또는 DDD의 애그리게이트)별로 하나의 영속성 어댑터를 구현한다. JPA와 플레인 SQL을 혼합 사용하는 등 기술별로 어댑터를 분리할 수 있고, Bounded Context별로 전용 영속성 어댑터를 두어 명확한 경계를 형성한다.

**도메인 모델과 영속성 모델 간 매핑** (참조: 페이지 58-62, 라인 147-483)
도메인 엔티티(Account)와 JPA 엔티티(AccountJpaEntity, ActivityJpaEntity) 간 분리를 통해 도메인 모델은 불변성과 유효성 검증을 통해 풍부한 비즈니스 로직을 포함하고, JPA 엔티티는 데이터베이스 테이블 구조를 반영한다. 매핑을 통해 JPA의 제약(no-args constructor 등)으로부터 도메인 모델을 보호한다.

### 핵심 개념 간 관계

**의존성 역전**은 영속성 어댑터 아키텍처의 기반 원칙이며, **포트 인터페이스 슬라이싱**은 이를 효과적으로 구현하기 위한 설계 기법이다. **영속성 어댑터 슬라이싱**은 물리적인 구현 단위를 정의하며, **도메인 모델과 영속성 모델 간 매핑**은 이 모든 것을 실제 코드로 구체화한다. 네 개념이 함께 작동하여 유지보수 가능하고 테스트 가능한 영속성 계층을 구성한다.

## 상세 내용

### 목차
1. 의존성 역전
2. 영속성 어댑터의 책임
3. 포트 인터페이스 슬라이싱
4. 영속성 어댑터 슬라이싱
5. Spring Data JPA 예제
6. 데이터베이스 트랜잭션 처리
7. 유지보수 가능한 소프트웨어 구축 방법

---

# 7. Testing Architecture Elements

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
세분화된 저비용 테스트(단위 테스트)를 높은 커버리지로 작성하고, 고비용 테스트는 낮은 커버리지로 작성한다. 계층별 정의: 단위 테스트(단일 클래스), 통합 테스트(여러 유닛의 네트워크), 시스템 테스트(전체 애플리케이션). 비용 요소: 구축 비용, 유지보수 비용, 실행 속도, 안정성.

**단위 테스트** (참조: 페이지 65-68, 라인 46-213)
단일 클래스를 인스턴스화하고 인터페이스를 통해 기능을 검증하며, 의존성은 실제 클래스 대신 모킹으로 대체한다. 도메인 엔티티는 비즈니스 규칙 검증에 최적이고 빠르고 간단하며, 유스케이스는 Mockito를 활용하여 상호작용을 검증하지만 구조 변경에 취약할 수 있다.

**통합 테스트** (참조: 페이지 68-71, 라인 214-408)
여러 유닛의 네트워크를 인스턴스화하고 진입 클래스의 인터페이스를 통해 데이터를 전송하며, 두 계층 간 경계를 넘나들고 일부는 모킹한다. 웹 어댑터는 Spring의 @WebMvcTest를 사용하여 JSON 매핑과 HTTP 응답을 검증하고, 영속성 어댑터는 Spring의 @DataJpaTest를 사용하여 실제 데이터베이스(Testcontainers 권장)를 사용한다.

**시스템 테스트** (참조: 페이지 71-74, 라인 409-547)
전체 애플리케이션을 시작하고 API를 통해 요청을 실행하여 모든 계층이 함께 작동하는지 검증한다. Spring의 @SpringBootTest를 사용하고 실제 HTTP 프로토콜을 사용하며, 여러 유스케이스를 조합하여 사용자 시나리오를 생성한다. 도메인 특화 언어(DSL) 사용으로 가독성을 향상하고 도메인 전문가의 피드백을 가능하게 한다.

**테스트 전략과 측정** (참조: 페이지 74-75, 라인 548-591)
라인 커버리지는 나쁜 지표이며, 배포에 대한 자신감으로 테스트 성공을 측정한다. 프로덕션 버그에 대해 "왜 테스트가 이 버그를 잡지 못했는가?" 질문하고 문서화하며, 구현 중 테스트 작성으로 개발 도구화하고 사후 작성 시 잡무화를 방지한다. 리팩터링마다 테스트 수정이 필요하면 테스트 설계에 문제가 있다.

### 핵심 개념 간 관계

**테스트 피라미드**는 전체 테스트 전략의 메타 원칙으로, **단위 테스트**, **통합 테스트**, **시스템 테스트**의 비율과 목적을 정의한다. Hexagonal Architecture의 각 요소는 특성에 맞는 테스트 유형으로 커버되며(도메인 엔티티와 유스케이스는 단위 테스트, 어댑터는 통합 테스트, 주요 시나리오는 시스템 테스트), 이 모든 것은 **테스트 전략과 측정** 원칙 하에서 배포 자신감이라는 실무적 목표를 달성한다.

## 상세 내용

### 목차
1. 테스트 피라미드
2. 단위 테스트로 도메인 엔티티 테스트
3. 단위 테스트로 유스케이스 테스트
4. 통합 테스트로 웹 어댑터 테스트
5. 통합 테스트로 영속성 어댑터 테스트
6. 시스템 테스트로 주요 경로 테스트
7. 얼마나 많은 테스트가 충분한가
8. 유지보수 가능한 소프트웨어 구축 방법

---

# 9. Assembling the Application

## 압축 내용

애플리케이션 조립은 의존성 주입을 통해 use case, adapter, domain 객체를 인스턴스화하고 연결하며, 의존성 규칙을 준수하면서 configuration component가 중립적 위치에서 모든 계층에 접근하여 작동하는 애플리케이션을 구성하는 과정이다.

## 핵심 내용

### 핵심 개념들
- **Configuration Component (설정 컴포넌트)** → 상세 내용: Why Even Care About Assembly?, Figure 26
- **Dependency Injection (의존성 주입)** → 상세 내용: Why Even Care About Assembly?
- **Assembly Approaches (조립 방식)** → 상세 내용: Assembling via Plain Code, Assembling via Spring's Classpath Scanning, Assembling via Spring's Java Config

### 핵심 개념 설명

**Configuration Component** (참조: content.md, 23-49행)
아키텍처에 중립적이며 모든 클래스에 대한 의존성을 가지는 컴포넌트로, Clean Architecture의 가장 바깥 원에 위치하여 모든 내부 계층에 접근할 수 있다. 웹 어댑터, 유스케이스, 퍼시스턴스 어댑터 인스턴스를 생성하고 연결하며, Single Responsibility Principle을 위반하지만 나머지 애플리케이션을 깨끗하게 유지하기 위해 필요하다.

**Dependency Injection** (참조: content.md, 5-20행)
의존성이 올바른 방향(내부로)을 가리키도록 유지하는 메커니즘이다. 유스케이스가 퍼시스턴스 어댑터를 직접 인스턴스화하면 잘못된 방향의 의존성이 생성되므로, Outgoing port interface를 통해 유스케이스는 인터페이스만 알고 런타임에 구현체를 제공받는다. 테스트 시 mock 객체 주입으로 단위 테스트 용이성이 향상된다.

**Assembly Approaches** (참조: content.md, 54-317행)
세 가지 주요 조립 방식이 있다: (1) Plain Code - 프레임워크 없이 직접 코드로 조립하지만 코드 양이 많고 가시성 문제가 있다, (2) Classpath Scanning - Spring의 @Component 어노테이션 기반 자동 스캔으로 매우 편리하지만 투명성이 부족하고 마법 같은 일이 발생할 수 있다, (3) Java Config - Spring의 @Configuration과 @Bean을 이용한 명시적 설정으로 프레임워크 독립성과 유연한 모듈 구성을 제공하면서도 세밀한 제어가 가능하다.

### 핵심 개념 간 관계

**Configuration Component**는 **Dependency Injection**을 구현하기 위한 컨테이너 역할을 하며, **Assembly Approaches**는 이 Configuration Component를 구현하는 구체적인 방법론들이다. Plain Code에서 Spring Java Config로 갈수록 더 세밀한 제어와 모듈화가 가능해지며, Dependency Rule 준수와 테스트 용이성이 향상된다.

## 상세 내용

### 목차
1. Why Even Care About Assembly?
2. Assembling via Plain Code
3. Assembling via Spring's Classpath Scanning
4. Assembling via Spring's Java Config
5. How Does This Help Me Build Maintainable Software?

---

# 10. Enforcing Architecture Boundaries

## 압축 내용

아키텍처 경계 강제는 의존성이 올바른 방향(내부로)을 가리키도록 보장하는 것으로, visibility modifiers(package-private), post-compile checks(ArchUnit), build artifacts(모듈 분리)라는 세 가지 접근 방식을 통해 아키텍처 침식을 방지하고 코드베이스를 유지보수 가능하게 유지한다.

## 핵심 내용

### 핵심 개념들
- **Dependency Rule Enforcement (의존성 규칙 강제)** → 상세 내용: Boundaries and Dependencies
- **Visibility Modifiers (가시성 수정자)** → 상세 내용: Visibility Modifiers
- **Post-Compile Checks (컴파일 후 검사)** → 상세 내용: Post-Compile Checks
- **Build Artifacts (빌드 아티팩트)** → 상세 내용: Build Artifacts

### 핵심 개념 설명

**Dependency Rule Enforcement** (참조: content.md, 28-32행)
계층 간 경계를 넘는 모든 의존성은 반드시 내부를 향해야 하며, 잘못된 방향의 의존성(dashed red arrows) 방지가 목적이다. 아키텍처 침식(architecture erosion) 방지를 위한 필수 활동으로, Domain → Application → Adapters → Configuration 순서로 계층이 구성된다.

**Visibility Modifiers** (참조: content.md, 33-129행)
Java의 package-private 수정자를 활용하여 패키지를 응집된 "모듈"로 그룹화하고, 특정 클래스만 public으로 만들어 모듈 진입점 역할을 하게 한다. 하지만 서브패키지 사용 시 한계가 있으며, Java는 서브패키지를 다른 패키지로 취급하므로 package-private 멤버에 접근할 수 없다.

**Post-Compile Checks** (참조: content.md, 135-237행)
public 클래스의 잘못된 의존성은 컴파일러가 방지하지 못하므로, ArchUnit 같은 도구를 사용하여 런타임에 검사하고 CI 빌드의 자동화된 테스트로 실행한다. DSL 형태로 헥사고날 아키텍처 의존성 규칙을 명시할 수 있지만, 오타와 리팩토링에 취약하며 항상 코드베이스와 병렬로 유지보수해야 한다.

**Build Artifacts** (참조: content.md, 256-334행)
각 모듈/계층을 별도 빌드 모듈과 JAR 파일로 분리하고, 빌드 스크립트에 허용된 의존성만 명시하여 컴파일 타임에 강제한다. 순환 의존성을 절대 불허하며 빌드 도구가 무한 루프를 방지하고, 각 모듈을 격리된 상태로 변경할 수 있으며, 의존성 추가가 의식적 행위가 된다.

### 핵심 개념 간 관계

**Dependency Rule Enforcement**는 목표이며, **Visibility Modifiers**, **Post-Compile Checks**, **Build Artifacts**는 이를 달성하기 위한 세 가지 점진적 방법이다. Visibility Modifiers가 가장 기본적이지만 제한적이고, Post-Compile Checks는 더 강력하지만 유지보수가 필요하며, Build Artifacts는 가장 강력하고 명시적이지만 안정된 아키텍처가 필요하다. 세 방법을 조합하여 사용할 수 있다.

## 상세 내용

### 목차
1. Boundaries and Dependencies
2. Visibility Modifiers
3. Post-Compile Checks
4. Build Artifacts
5. How Does This Help Me Build Maintainable Software?
