# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter10: Enforcing Architecture Boundaries

## 압축 내용
아키텍처 경계 강제는 의존성이 올바른 방향(내부로)을 가리키도록 보장하는 것으로, visibility modifiers(package-private), post-compile checks(ArchUnit), build artifacts(모듈 분리)라는 세 가지 접근 방식을 통해 아키텍처 침식을 방지하고 코드베이스를 유지보수 가능하게 유지한다.

## 핵심 내용

**핵심 개념들:**
- Dependency Rule Enforcement (의존성 규칙 강제)
- Visibility Modifiers (가시성 수정자)
- Post-Compile Checks (컴파일 후 검사)
- Build Artifacts (빌드 아티팩트)

**핵심 개념 설명:**

### Dependency Rule Enforcement (의존성 규칙 강제) → [상세: Boundaries and Dependencies]
- 계층 간 경계를 넘는 모든 의존성은 반드시 내부를 향해야 함 (content.md, 28-32행)
- 잘못된 방향의 의존성(dashed red arrows) 방지가 목적 (content.md, 31-32행)
- 아키텍처 침식(architecture erosion) 방지를 위한 필수 활동 (content.md, 6-10행)
- Domain → Application → Adapters → Configuration 순서로 계층 구성 (content.md, 20-27행)

### Visibility Modifiers (가시성 수정자) → [상세: Visibility Modifiers]
- Java의 package-private 수정자를 활용한 경계 강제 (content.md, 33-47행)
- 패키지를 응집된 "모듈"로 그룹화 (content.md, 43-45행)
- 특정 클래스만 public으로 만들어 모듈 진입점 역할 (content.md, 45-47행)
- 서브패키지 사용 시 한계: Java는 서브패키지를 다른 패키지로 취급 (content.md, 124-129행)

### Post-Compile Checks (컴파일 후 검사) → [상세: Post-Compile Checks]
- public 클래스의 잘못된 의존성은 컴파일러가 방지하지 못함 (content.md, 135-138행)
- ArchUnit 같은 도구를 사용한 런타임 검사 (content.md, 142-145행)
- CI 빌드의 자동화된 테스트로 실행 (content.md, 140-141행)
- DSL 형태로 헥사고날 아키텍처 의존성 규칙 명시 가능 (content.md, 178-231행)

### Build Artifacts (빌드 아티팩트) → [상세: Build Artifacts]
- 각 모듈/계층을 별도 빌드 모듈과 JAR 파일로 분리 (content.md, 256-258행)
- 빌드 스크립트에 허용된 의존성만 명시하여 컴파일 타임에 강제 (content.md, 258-260행)
- 순환 의존성 절대 불허 - 빌드 도구가 무한 루프 방지 (content.md, 307-311행)
- 각 모듈을 격리된 상태로 변경 가능 (content.md, 318-326행)

**핵심 개념 간 관계:**
Dependency Rule Enforcement는 목표이며, Visibility Modifiers, Post-Compile Checks, Build Artifacts는 이를 달성하기 위한 세 가지 점진적 방법이다. Visibility Modifiers가 가장 기본적이지만 제한적이고, Post-Compile Checks는 더 강력하지만 유지보수가 필요하며, Build Artifacts는 가장 강력하고 명시적이지만 안정된 아키텍처가 필요하다. 세 방법을 조합하여 사용할 수 있다.

---

## 상세 내용

### 목차
1. Boundaries and Dependencies → [핵심: Dependency Rule Enforcement]
2. Visibility Modifiers → [핵심: Visibility Modifiers]
3. Post-Compile Checks → [핵심: Post-Compile Checks]
4. Build Artifacts → [핵심: Build Artifacts]
5. How Does This Help Me Build Maintainable Software?

### 1. Boundaries and Dependencies → [핵심: Dependency Rule Enforcement]

**아키텍처 경계의 필요성** (content.md, 4-10행):
- 모든 소프트웨어 프로젝트에서 아키텍처는 시간이 지나면서 침식됨
- 계층 간 경계 약화
- 코드 테스트 어려워짐
- 새 기능 구현에 점점 더 많은 시간 소요
- 아키텍처 침식과 싸우기 위한 조치 필요

**아키텍처 계층 구조** (content.md, 12-27행, Figure 27):

```
┌─────────────────────────────────────┐
│     Configuration Layer              │  ← 가장 바깥 계층
│  (Factories, DI mechanism)           │
├─────────────────────────────────────┤
│     Adapters Layer                   │
│  (Web/Persistence Adapters)          │
├─────────────────────────────────────┤
│     Application Layer                │
│  (Use Cases, Services, Ports)        │
├─────────────────────────────────────┤
│     Domain Layer                     │  ← 가장 안쪽 계층
│  (Entities)                          │
└─────────────────────────────────────┘

의존성 방향: 바깥 → 안쪽 (모든 화살표는 도메인을 향함)
```

**계층별 역할** (content.md, 23-27행):
1. **Domain Entities** (가장 안쪽): 도메인 엔티티 포함
2. **Application Layer**:
   - 도메인 엔티티에 접근하여 유스케이스 구현
   - Application services에서 구현
3. **Adapters**:
   - Incoming ports를 통해 서비스 접근
   - Outgoing ports를 통해 서비스로부터 접근됨
4. **Configuration Layer** (가장 바깥):
   - Adapter와 service 객체를 생성하는 팩토리
   - 의존성 주입 메커니즘에 제공

**Dependency Rule** (content.md, 28-32행):
- 각 계층과 그 다음 안쪽/바깥쪽 이웃 사이에 경계 존재
- 계층 경계를 넘는 의존성은 항상 안쪽을 향해야 함
- 잘못된 방향의 의존성(그림의 빨간 점선 화살표) 방지가 목표

### 2. Visibility Modifiers → [핵심: Visibility Modifiers]

이전 화제(Boundaries and Dependencies)에서 경계 강제의 필요성을 확립했으므로, 이제 Java가 제공하는 가장 기본적인 도구인 가시성 수정자를 살펴본다.

**Visibility Modifiers 개요** (content.md, 33-47행):
- Java가 제공하는 경계 강제를 위한 가장 기본 도구
- 대부분의 개발자가 public, protected, private만 알고 package-private(default)는 모름
- Package-private가 중요한 이유:
  - Java 패키지를 응집된 "모듈"로 그룹화
  - 모듈 내 클래스들은 서로 접근 가능
  - 패키지 외부에서는 접근 불가
  - 특정 클래스만 public으로 만들어 모듈 진입점 역할
  - Dependency Rule 위반 위험 감소

**패키지 구조에 가시성 수정자 적용** (content.md, 48-122행):

```
buckpal
└──account
   ├──adapter
   |  ├──in
   |  |  └──web
   |  |     └──o AccountController              (o = package-private)
   |  ├──out
   |  |  └──persistence
   |  |     ├──o AccountPersistenceAdapter     (o = package-private)
   |  |     └──o SpringDataAccountRepository   (o = package-private)
   ├──domain
   |  ├──+ Account                              (+ = public)
   |  └──+ Activity                             (+ = public)
   └──application
      └──o SendMoneyService                     (o = package-private)
      └──port
         ├──in
         |  └──+ SendMoneyUseCase               (+ = public)
         └──out
            ├──+ LoadAccountPort                (+ = public)
            └──+ UpdateAccountStatePort         (+ = public)
```

**Package-private 적용 가능 클래스** (content.md, 111-119행):
1. **Persistence 패키지 클래스들**:
   - 외부에서 접근 불필요
   - Output ports 구현을 통해 접근됨

2. **SendMoneyService**:
   - 같은 이유로 package-private 가능
   - 의존성 주입 메커니즘이 reflection 사용하여 인스턴스화
   - Package-private이어도 인스턴스화 가능

3. **Spring 제약사항**:
   - Classpath scanning 방식에서만 작동
   - 다른 방식은 직접 인스턴스 생성 필요 → public 접근 필요

**Public이어야 하는 클래스** (content.md, 120-122행):
- Domain 패키지: 다른 계층에서 접근 가능해야 함
- Application 계층: 웹 및 퍼시스턴스 어댑터에서 접근 가능해야 함

**Package-private의 한계** (content.md, 123-129행):

```java
// 문제 상황
account/
├── persistence/          // 패키지
│   └── adapter/          // 서브패키지 (다른 패키지로 취급됨!)
│       └── AccountAdapter.java

// Java는 서브패키지를 다른 패키지로 취급
// persistence 패키지의 package-private 멤버를
// persistence.adapter 서브패키지에서 접근 불가
```

```python
# Python에서는 다른 접근 방식 사용
# account/persistence/__init__.py
class _InternalAdapter:  # 언더스코어로 내부 클래스 표시
    """관례상 private, but 강제되지 않음"""
    pass

# 명시적으로 공개할 것만 __all__에 선언
__all__ = ['PublicAdapter']  # _InternalAdapter는 제외
```

제약사항:
- 소수의 클래스(handful)를 가진 작은 모듈에 적합
- 패키지가 일정 수 이상의 클래스를 포함하면 혼란스러움
- 서브패키지로 구조화하고 싶을 때 문제 발생
- 서브패키지의 멤버는 public이어야 함 → 외부에 노출됨
- 아키텍처가 잘못된 의존성에 취약해짐

### 3. Post-Compile Checks → [핵심: Post-Compile Checks]

Visibility Modifiers의 한계(public 클래스는 보호 불가)를 보완하기 위해 컴파일 이후 단계에서 의존성을 검사하는 방법을 살펴본다.

**Post-Compile Checks의 필요성** (content.md, 134-141행):
- Public 클래스는 컴파일러가 다른 클래스의 사용을 허용
- 의존성 방향이 잘못되어도 컴파일러가 막지 못함
- Dependency Rule 위반 검사를 위한 다른 수단 필요
- 런타임(코드 컴파일 후)에 수행되는 검사 도입
- CI 빌드의 자동화된 테스트에서 실행하는 것이 최선

**ArchUnit 도구** (content.md, 142-145행):
- Java용 의존성 방향 검사 도구
- 의존성이 예상 방향을 가리키는지 검사하는 API 제공
- 위반 발견 시 예외 발생
- JUnit 같은 단위 테스트 프레임워크 기반 테스트로 실행
- 의존성 위반 시 테스트 실패

**기본 의존성 검사 예시** (content.md, 146-177행):

```java
class DependencyRuleTests {

    @Test
    void domainLayerDoesNotDependOnApplicationLayer() {
        // Domain 계층이 Application 계층에 의존하지 않음을 검증
        noClasses()
            .that()
            .resideInAPackage("buckpal.domain..")  // domain 패키지의 클래스가
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage("buckpal.application..")  // application 패키지에 의존하면 안됨
            .check(new ClassFileImporter()
                .importPackages("buckpal.."));  // buckpal 패키지 전체 검사
    }
}
```

```python
# Python 버전 (import-linter 사용)
# .import-linter.ini 설정 파일
"""
[importlinter]
root_package = buckpal

[importlinter:contract:domain-independence]
name = Domain layer does not depend on application layer
type = forbidden
source_modules =
    buckpal.domain
forbidden_modules =
    buckpal.application
"""

# pytest 테스트
def test_domain_layer_independence():
    """Domain 계층이 Application 계층에 의존하지 않음을 검증"""
    from importlinter import cli
    result = cli.lint_imports()
    assert result == 0, "Domain layer should not depend on application layer"
```

**DSL을 통한 헥사고날 아키텍처 검증** (content.md, 178-225행):

```java
class DependencyRuleTests {

    @Test
    void validateRegistrationContextArchitecture() {
        HexagonalArchitecture.boundedContext("account")  // Bounded context 지정

            .withDomainLayer("domain")  // Domain 계층 정의

            .withAdaptersLayer("adapter")  // Adapters 계층 정의
                .incoming("web")           // Incoming adapter
                .outgoing("persistence")   // Outgoing adapter
                .and()

            .withApplicationLayer("application")  // Application 계층 정의
                .services("service")              // Services
                .incomingPorts("port.in")        // Incoming ports
                .outgoingPorts("port.out")       // Outgoing ports
                .and()

            .withConfiguration("configuration")  // Configuration 계층 정의

            .check(new ClassFileImporter()
                .importPackages("buckpal.."));  // 의존성 규칙 자동 검증
    }
}
```

```python
# Python 버전 (구조화된 검증 DSL)
from typing import Protocol
from dataclasses import dataclass

@dataclass
class HexagonalArchitecture:
    """헥사고날 아키텍처 검증 DSL"""
    bounded_context: str

    @classmethod
    def bounded_context(cls, name: str):
        return cls(bounded_context=name)

    def with_domain_layer(self, package: str):
        self.domain_package = package
        return self

    def with_adapters_layer(self, package: str):
        self.adapters_package = package
        return AdaptersConfig(self, package)

    def with_application_layer(self, package: str):
        self.application_package = package
        return ApplicationConfig(self, package)

    def with_configuration(self, package: str):
        self.configuration_package = package
        return self

    def check(self):
        """모든 의존성 규칙 검증"""
        # Dependency Rule 검증 로직
        pass

# 사용 예시
def test_validate_registration_context_architecture():
    (HexagonalArchitecture.bounded_context("account")
        .with_domain_layer("domain")
        .with_adapters_layer("adapter")
            .incoming("web")
            .outgoing("persistence")
            .and_()
        .with_application_layer("application")
            .services("service")
            .incoming_ports("port.in")
            .outgoing_ports("port.out")
            .and_()
        .with_configuration("configuration")
        .check())
```

**DSL 작동 방식** (content.md, 226-231행):
1. Bounded context의 부모 패키지 지정 (단일 bounded context면 전체 애플리케이션)
2. Domain, adapter, application, configuration 계층의 서브패키지 지정
3. check() 호출 시 일련의 검사 실행
4. Dependency Rule에 따라 패키지 의존성이 유효한지 검증
5. GitHub에 DSL 코드 공개³⁰

**Post-Compile Checks의 한계** (content.md, 232-237행):

문제점:
1. **오타 취약성**:
   ```java
   // 패키지명 오타
   .importPackages("buckpa..")  // "buckpal" → "buckpa"
   // → 클래스를 찾지 못하고 의존성 위반도 찾지 못함
   // → 하지만 테스트는 통과 (거짓 양성)
   ```

2. **리팩토링 취약성**:
   - 패키지명 변경 시 테스트가 무용지물이 될 수 있음
   - 클래스를 찾지 못하면 실패하도록 검사 추가로 완화 가능
   - 하지만 여전히 리팩토링에 취약

3. **병렬 유지보수 필요**:
   - Post-compile checks는 항상 코드베이스와 병렬로 유지보수해야 함
   - 코드 변경과 테스트 업데이트 동기화 필요

해결 방향:
- 다음 섹션(Build Artifacts)에서 더 강력한 접근법 소개

### 4. Build Artifacts → [핵심: Build Artifacts]

Post-Compile Checks의 유지보수 부담을 해결하고 더 명시적인 경계 강제를 위해 빌드 수준에서 모듈을 분리하는 방법을 살펴본다.

**Build Artifacts 개념** (content.md, 238-250행):
- 지금까지는 패키지만으로 아키텍처 경계 구분
- 모든 코드가 단일 monolithic build artifact의 일부
- Build artifact: (자동화된) 빌드 프로세스의 결과물
- Java 세계의 인기 빌드 도구: Maven, Gradle
- 단일 빌드 스크립트로 컴파일, 테스트, 패키징하여 JAR 파일 생성

**Dependency Resolution** (content.md, 251-260행):

빌드 도구의 주요 기능:
1. 코드베이스가 의존하는 모든 artifacts 가용성 확인
2. 없으면 artifact repository에서 로드 시도
3. 실패 시 코드 컴파일 전에 빌드 실패

활용 방법:
- 각 모듈/계층마다 별도 빌드 모듈 생성
- 각각 자체 코드베이스와 빌드 artifact(JAR 파일) 생성
- 빌드 스크립트에 아키텍처에서 허용된 의존성만 명시
- 개발자가 부주의하게 잘못된 의존성 생성 불가
  - 클래스가 클래스패스에 없어 컴파일 에러 발생

**빌드 모듈 분리 방식들** (content.md, 261-304행, Figure 28):

**방식 1: 기본 3-모듈 빌드** (왼쪽):
```
Configuration Module
    ↓
Adapters Module (Web + Persistence)
    ↓
Application Module
```
- Configuration이 Adapters 접근, Adapters가 Application 접근
- Configuration은 전이적 의존성으로 Application도 접근 가능
- 문제: Web과 Persistence adapter 간 의존성 방지 불가

**방식 2: Adapter 분리** (두 번째):
```
Configuration Module
    ↓
Web Adapter Module    Persistence Adapter Module
         ↓                      ↓
           Application Module
```
- 각 adapter를 별도 빌드 모듈로 분리
- Web과 Persistence adapter 간 의존성 방지
- Single Responsibility Principle 준수
- 다른 타입의 adapter(예: third party API) 추가 시 격리 유지

**방식 3: API 모듈 분리 (Dependency Inversion)** (세 번째):
```
Configuration Module
    ↓
Web Adapter    Persistence Adapter
    ↓                ↓
         API Module (Port Interfaces)
              ↑
    Application Module (Services + Domain)
```
- Port 인터페이스만 포함하는 별도 "api" 모듈
- Adapter와 Application 모듈이 api 모듈 접근 (역방향 불가)
- API 모듈이 domain entities 접근 불가
  - Port 인터페이스에 entities 사용 불가 (No Mapping 전략 불허)
- Adapter가 entities와 services 직접 접근 불가 → ports를 통해야 함

**방식 4: API 모듈 세분화** (네 번째):
```
Configuration Module
    ↓
Web Adapter           Persistence Adapter
    ↓                        ↓
Incoming Ports Module    Outgoing Ports Module
         ↓                      ↓
           Application Module
```
- API 모듈을 incoming/outgoing ports로 분리
- Adapter가 incoming/outgoing 중 하나만 의존하도록 명확화
- Incoming adapter인지 outgoing adapter인지 명확히 구분

**추가 분리 가능성** (content.md, 295-299행):
```
Services Module    Domain Entities Module
         ↓              ↑
         └──────────────┘
```
- Application 모듈을 services와 domain entities로 분리
- Entities가 services 접근 방지
- 다른 애플리케이션(다른 유스케이스)이 동일 domain entities 재사용 가능
  - Domain build artifact에 의존성 선언만으로 가능

**모듈 분리 전략의 트레이드오프** (content.md, 300-304행):
- 더 세밀하게 자를수록: 의존성 제어 강화
- 더 세밀하게 자를수록: 모듈 간 매핑 필요 증가
  - Chapter 8 "Mapping Between Boundaries"의 매핑 전략 강제

**Build Modules의 장점** (content.md, 305-333행):

**1. 순환 의존성 방지** (content.md, 307-313행):
```
Module A → Module B → Module C → Module A (순환!)
```

빌드 도구의 특성:
- 순환 의존성을 절대 허용하지 않음
- 이유: 순환 내 한 모듈의 변경이 다른 모든 모듈의 변경을 초래
  - Single Responsibility Principle 위반
- 의존성 해결 중 무한 루프에 빠짐
- 빌드 모듈 간 순환 의존성이 없음을 보장

Java 컴파일러와 대조:
- 패키지 간 순환 의존성 전혀 신경 쓰지 않음
- 컴파일러 수준에서는 방지 안 됨

**2. 격리된 코드 변경** (content.md, 318-326행):

시나리오:
```
Application Layer (대규모 리팩토링 중)
    ↑
Adapter Layer (일시적 컴파일 에러)
```

단일 빌드 모듈인 경우:
- IDE가 adapter의 컴파일 에러 수정을 요구
- Application layer 테스트가 adapter 불필요해도 실행 불가
- 전체 빌드 실패 (둘 중 하나라도 컴파일 에러)

별도 빌드 모듈인 경우:
- IDE가 adapter 에러 무시
- Application layer 테스트를 자유롭게 실행 가능
- 각 계층을 독립적으로 빌드 가능

추가 이점:
- 각 모듈을 격리된 상태로 변경 가능
- 각 모듈을 별도 코드 리포지토리로 분리 가능
- 다른 팀이 다른 모듈 유지보수 가능

**3. 명시적 의존성 선언** (content.md, 329-332행):

```gradle
// build.gradle
dependencies {
    implementation project(':application')  // 명시적 의존성 선언
    // implementation project(':domain')    // 추가 전 고려 필요
}
```

```python
# Python setup.py / pyproject.toml
[project]
dependencies = [
    "buckpal-application",  # 명시적 의존성 선언
    # "buckpal-domain",     # 추가 전 고려 필요
]
```

효과:
- 새 의존성 추가가 우연이 아닌 의식적 행위
- 개발자가 접근 불가능한 클래스 필요 시:
  - 의존성이 정말 합리적인지 고려
  - 빌드 스크립트에 추가하기 전 숙고

**4. 비용-효익 분석** (content.md, 333-334행):

비용:
- 빌드 스크립트 유지보수 추가 작업 필요

조건:
- 아키텍처가 어느 정도 안정된 후 분리 권장
- 초기 개발 단계에서는 과도한 부담

효익:
- 명시적 의존성 제어
- 순환 의존성 방지
- 격리된 개발 및 테스트
- 팀 간 모듈 분리 가능

### 5. How Does This Help Me Build Maintainable Software?

앞의 세 가지 경계 강제 방법(Visibility Modifiers, Post-Compile Checks, Build Artifacts)을 종합하여 유지보수 가능한 소프트웨어 구축 방법을 정리한다.

**소프트웨어 아키텍처의 본질** (content.md, 336-338행):
- 아키텍처 요소 간 의존성 관리가 핵심
- 의존성이 "big ball of mud"가 되면 아키텍처도 "big ball of mud"
- 시간이 지나도 아키텍처를 보존하려면 의존성이 올바른 방향을 가리키도록 지속적 관리 필요

**새 코드 작성 또는 기존 코드 리팩토링 시** (content.md, 340-342행):

**패키지 구조 염두**:
```java
account/
├── domain/          // public entities
├── application/     // package-private services
│   └── port/        // public interfaces
└── adapter/
    ├── web/         // package-private adapters
    └── persistence/ // package-private adapters
```

**Package-private 활용**:
- 가능한 한 package-private 가시성 사용
- 패키지 외부에서 접근하지 말아야 할 클래스로의 의존성 방지

**단일 빌드 모듈 내에서 아키텍처 경계 강제** (content.md, 343-345행):

조건:
- Package-private 수정자가 작동하지 않는 경우
  - 패키지 구조가 허용하지 않음
  - 서브패키지 필요

해결책:
- ArchUnit 같은 post-compile 도구 활용
- 런타임에 의존성 규칙 검증
- CI/CD 파이프라인에 통합

**아키텍처가 충분히 안정되었을 때** (content.md, 346-347행):

조건:
- 아키텍처 구조가 자주 변경되지 않음
- 모듈 경계가 명확함

행동:
- 아키텍처 요소를 별도 빌드 모듈로 추출
- 의존성에 대한 명시적 제어 확보

**세 가지 접근법의 조합** (content.md, 348-349행):

```
┌─────────────────────────────────────────────────┐
│ Build Artifacts (가장 강력, 명시적)              │
│   ↓ 보완                                        │
│ Post-Compile Checks (중간 강도, 유지보수 필요)    │
│   ↓ 보완                                        │
│ Visibility Modifiers (기본, 제한적)              │
└─────────────────────────────────────────────────┘
```

**통합 전략**:
1. 기본적으로 package-private 활용
2. 필요 시 ArchUnit으로 보완
3. 안정된 후 빌드 모듈 분리
4. 세 방법 모두 조합 가능

**최종 목표** (content.md, 348-349행):
- 아키텍처 경계 강제
- 시간이 지나도 코드베이스 유지보수 가능성 유지
- 아키텍처 침식 방지
