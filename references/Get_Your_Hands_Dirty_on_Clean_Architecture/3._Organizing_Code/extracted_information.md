# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter3: Organizing Code

## 압축 내용
계층별 구조(Organizing By Layer)와 기능별 구조(Organizing By Feature)의 한계를 극복하고, 헥사고날 아키텍처의 구성 요소(adapters, ports, domain, application)를 패키지 구조에 명시적으로 반영하여 아키텍처와 코드 간 격차(architecture/code gap)를 최소화하고, 의존성 주입(Dependency Injection)을 통해 계층 간 의존성을 올바르게 관리하는 표현적 패키지 구조(Architecturally Expressive Package Structure)를 구축한다.

---

## 핵심 내용

### 핵심 개념
1. **계층별 구조의 한계** (Organizing By Layer의 문제점) → [상세: 계층별 구조]
2. **기능별 구조의 한계** (Organizing By Feature의 문제점) → [상세: 기능별 구조]
3. **표현적 패키지 구조** (Architecturally Expressive Package Structure) → [상세: 표현적 패키지 구조]
4. **의존성 주입의 역할** (Role of Dependency Injection) → [상세: 의존성 주입]

### 핵심 개념 설명

#### 1. 계층별 구조의 한계 → [상세: 계층별 구조]
전통적인 계층별 패키지 구조(web, domain, persistence)는 세 가지 주요 문제를 가진다: (1) 기능 간 경계가 없어 관련 없는 기능들이 뒤섞임, (2) 어떤 유스케이스를 제공하는지 코드에서 파악 불가, (3) 헥사고날 아키텍처의 포트와 어댑터가 코드에서 명시적으로 드러나지 않음.

#### 2. 기능별 구조의 한계 → [상세: 기능별 구조]
기능별 패키지 구조(account 패키지에 관련 클래스 모두 배치)는 기능 간 경계를 제공하고 유스케이스를 명확히 하지만, 아키텍처의 가시성은 더 떨어진다. 어댑터를 식별할 패키지명이 없고, incoming/outgoing 포트가 여전히 보이지 않으며, package-private 접근제어로 도메인 코드를 보호할 수 없다.

#### 3. 표현적 패키지 구조 → [상세: 표현적 패키지 구조]
헥사고날 아키텍처의 주요 요소(entities, use cases, ports, adapters)를 패키지 구조에 직접 매핑한다. adapter/{in,out}, domain, application, port/{in,out} 패키지를 통해 아키텍처 다이어그램과 코드를 1:1 대응시켜 architecture/code gap을 줄이고, 어댑터 교체가 용이하며, DDD의 bounded context 개념과도 자연스럽게 연결된다.

#### 4. 의존성 주입의 역할 → [상세: 의존성 주입]
애플리케이션 계층이 어댑터에 의존하지 않도록 중립적인 의존성 주입 컴포넌트가 모든 계층의 인스턴스를 생성하고 주입한다. Incoming adapter는 자연스럽게 애플리케이션을 호출하지만, outgoing adapter는 Dependency Inversion Principle을 통해 의존성 방향을 역전시켜야 한다.

### 핵심 개념 간 관계
계층별 구조와 기능별 구조는 각각 다른 측면에서 한계를 가지며, 이를 모두 해결하기 위해 표현적 패키지 구조가 등장한다. 표현적 패키지 구조는 헥사고날 아키텍처의 모든 요소를 명시적으로 드러내지만, 이를 실현하려면 의존성 주입을 통해 계층 간 의존성을 올바르게 관리해야 한다. 결국 네 가지 개념은 "아키텍처를 코드에 명확히 반영"이라는 하나의 목표를 향한 진화 과정을 보여준다.

---

## 상세 내용

### 목차
1. [계층별 구조 (Organizing By Layer)](#계층별-구조)
2. [기능별 구조 (Organizing By Feature)](#기능별-구조)
3. [표현적 패키지 구조 (Architecturally Expressive Package Structure)](#표현적-패키지-구조)
4. [의존성 주입의 역할 (The Role of Dependency Injection)](#의존성-주입의-역할)

---

### 1. 계층별 구조 (Organizing By Layer) {#계층별-구조}
**[핵심 개념 1: 계층별 구조의 한계]**

**참조: Lines 15-67**

첫 번째 코드 구조화 방식은 계층별 패키지 구조다. web, domain, persistence 계층별로 패키지를 나눈다.

**패키지 구조 예시 (Lines 17-41):**
```
buckpal
├──domain
│  ├──Account
│  ├──Activity
│  ├──AccountRepository
│  └──AccountService
├──persistence
│  └──AccountRepositoryImpl
└──web
   └──AccountController
```

이 구조는 Dependency Inversion Principle을 적용하여 모든 의존성이 domain 패키지를 향하도록 설계되었다. AccountRepository 인터페이스를 domain에 두고 persistence 패키지에서 구현한다 (Lines 42-47).

**세 가지 주요 문제점 (Lines 48-66):**

**문제 1: 기능 간 경계 부재 (Lines 53-57)**
- 기능별 슬라이스나 feature 간 패키지 경계가 없다
- 사용자 관리 기능 추가 시: UserController(web), UserService/UserRepository/User(domain), UserRepositoryImpl(persistence)가 각 계층에 흩어진다
- 추가 구조 없이는 클래스들이 뒤섞여 관련 없는 기능 간 원치 않는 부작용 발생

**문제 2: 유스케이스 가시성 부재 (Lines 58-61)**
- AccountService나 AccountController가 어떤 유스케이스를 구현하는지 알 수 없다
- 특정 기능을 찾으려면 어느 서비스가 구현했는지 추측하고 메서드를 찾아야 한다

**문제 3: 아키텍처 가시성 부재 (Lines 62-66)**
- 헥사고날 아키텍처를 따른다고 추측만 할 수 있다
- web과 persistence 패키지를 탐색해야 어댑터를 찾을 수 있다
- incoming/outgoing 포트가 코드에서 숨겨져 있다
- 웹 어댑터가 호출하는 기능과 persistence 어댑터가 제공하는 기능을 한눈에 파악 불가

---

### 2. 기능별 구조 (Organizing By Feature) {#기능별-구조}
**[이전과의 관계: 계층별 구조의 문제점을 해결하기 위한 시도]**
**[핵심 개념 2: 기능별 구조의 한계]**

**참조: Lines 67-109**

두 번째 방식은 기능별로 코드를 구조화한다.

**패키지 구조 예시 (Lines 70-83):**
```
buckpal
└──account
   ├──Account
   ├──AccountController
   ├──AccountRepository
   ├──AccountRepositoryImpl
   └──SendMoneyService
```

계층별 구조와의 차이점:
- 계정 관련 모든 코드를 account 최상위 패키지에 배치 (Lines 84-85)
- 계층 패키지를 제거
- 각 기능 그룹이 별도의 최상위 패키지를 가짐

**개선된 점 (Lines 86-99):**

1. **기능 간 경계 확립 (Lines 86-90)**
   - package-private 접근제어로 외부에서 접근하면 안 되는 클래스 보호
   - 기능 간 원치 않는 의존성 방지 ✓

2. **유스케이스 가시성 (Lines 91-99)**
   - AccountService를 SendMoneyService로 이름 변경하여 책임 명확화
   - 클래스명만으로 "Send Money" 유스케이스 구현을 알 수 있다
   - Robert Martin의 "Screaming Architecture" - 코드가 의도를 소리친다 ✓

**여전한 문제점 (Lines 100-105):**
- 아키텍처 가시성은 오히려 더 떨어짐
- 어댑터를 식별할 패키지명이 없다
- incoming/outgoing 포트가 여전히 보이지 않는다
- 의존성 역전(SendMoneyService → AccountRepository 인터페이스)을 구현했지만, package-private으로 도메인 코드를 persistence 코드로부터 보호할 수 없다

**해결 과제 (Lines 106-109):**
아키텍처를 한눈에 볼 수 있게 하려면 아키텍처 다이어그램의 박스를 가리키면 어느 코드가 책임지는지 즉시 알 수 있어야 한다.

---

### 3. 표현적 패키지 구조 (Architecturally Expressive Package Structure) {#표현적-패키지-구조}
**[이전과의 관계: 기능별 구조의 아키텍처 가시성 문제를 해결]**
**[핵심 개념 3: 표현적 패키지 구조]**

**참조: Lines 110-232**

헥사고날 아키텍처의 주요 요소(entities, use cases, incoming/outgoing ports, adapters)를 패키지 구조에 직접 매핑한다 (Lines 111-113).

**패키지 구조 (Lines 114-171):**
```
buckpal
└──account
   ├──adapter
   │  ├──in
   │  │  └──web
   │  │     └──AccountController
   │  ├──out
   │  │  └──persistence
   │  │     ├──AccountPersistenceAdapter
   │  │     └──SpringDataAccountRepository
   ├──domain
   │  ├──Account
   │  └──Activity
   └──application
      └──SendMoneyService
      └──port
         ├──in
         │  └──SendMoneyUseCase
         └──out
            ├──LoadAccountPort
            └──UpdateAccountStatePort
```

**구조 설명 (Lines 176-186):**

1. **최상위: account 패키지**
   - Account 관련 유스케이스 구현 모듈을 나타냄 (Lines 176-178)

2. **domain 패키지**
   - 도메인 모델 포함 (Lines 179-180)

3. **application 패키지**
   - 도메인 모델을 감싸는 서비스 계층
   - SendMoneyService가 incoming port인 SendMoneyUseCase 구현
   - outgoing port인 LoadAccountPort와 UpdateAccountStatePort 사용
   - persistence adapter가 이 outgoing port들을 구현 (Lines 180-182)

4. **adapter 패키지**
   - incoming adapters: application 계층의 incoming port 호출
   - outgoing adapters: application 계층의 outgoing port 구현 제공
   - web adapter와 persistence adapter가 각각 하위 패키지 보유 (Lines 183-186)

**장점 1: 아키텍처/코드 격차 해소 (Lines 188-199)**

실제 사용 시나리오 (Lines 188-194):
- 사무실 벽에 헥사고날 아키텍처 다이어그램이 있다
- 동료와 third-party API 클라이언트 수정 논의 시 해당 outgoing adapter를 가리킨다
- 대화 후 IDE에서 `adapter/out/<name-of-adapter>` 패키지로 바로 이동해 작업 시작

Architecture/Code Gap 해결 (Lines 195-199):
- 대부분의 소프트웨어 프로젝트에서 아키텍처는 추상 개념일 뿐 코드에 직접 매핑 불가
- 패키지 구조가 아키텍처를 반영하지 않으면 시간이 지나면서 코드가 목표 아키텍처에서 점점 벗어남
- 표현적 패키지 구조는 이 격차를 줄인다

**장점 2: 능동적 아키텍처 사고 촉진 (Lines 200-202)**
- 많은 패키지로 인해 현재 작업 중인 코드를 어느 패키지에 넣을지 고민하게 됨
- 아키텍처에 대한 능동적 사고를 촉진

**접근 제어와 의존성 관리 (Lines 203-212):**

**Adapter 패키지 (Lines 205-208):**
- 모든 클래스가 package-private일 수 있다
- 외부에서는 application 패키지의 port 인터페이스를 통해서만 호출
- application 계층에서 adapter 클래스로의 우발적 의존성 차단 ✓

**Application과 Domain 패키지 (Lines 209-212):**
- 일부 클래스는 public이어야 함
- Ports: 어댑터가 접근해야 하므로 public
- Domain classes: 서비스와 어댑터가 접근해야 하므로 public
- Services: incoming port 인터페이스 뒤에 숨길 수 있어 public 불필요

**장점 3: 어댑터 교체 용이성 (Lines 218-222)**
- 어댑터 코드가 별도 패키지에 있어 교체 용이
- 예시: key-value DB → SQL DB 전환
  - 새 adapter 패키지에 모든 outgoing port 구현
  - 기존 패키지 제거

**장점 4: DDD 개념과의 직접 매핑 (Lines 223-226)**
- 최상위 패키지(account)가 bounded context
- 다른 bounded context와 통신하는 전용 진입/출구점(ports) 보유
- domain 패키지 내에서 DDD 도구를 활용한 도메인 모델 구축 가능

**유지보수 고려사항 (Lines 227-232):**
- 프로젝트 전체 기간 동안 패키지 구조 유지에는 규율이 필요
- 패키지 구조가 맞지 않는 경우도 있어 architecture/code gap을 벌리는 패키지를 만들 수밖에 없을 때도 있다
- 완벽함은 없지만, 표현적 패키지 구조로 코드와 아키텍처 간 격차를 줄일 수 있다

---

### 4. 의존성 주입의 역할 (The Role of Dependency Injection) {#의존성-주입의-역할}
**[이전과의 관계: 표현적 패키지 구조를 실현하기 위한 필수 메커니즘]**
**[핵심 개념 4: 의존성 주입의 역할]**

**참조: Lines 233-268**

클린 아키텍처의 필수 요구사항: application 계층이 incoming/outgoing adapter에 의존성을 가지면 안 됨 (Lines 234-236).

**Incoming Adapter의 의존성 관리 (Lines 237-240):**
- 제어 흐름과 의존성 방향이 같아 쉽다
- 웹 어댑터가 단순히 application 계층의 서비스 호출
- 진입점을 명확히 하려면 실제 서비스를 port 인터페이스 뒤에 숨길 수 있다

**Outgoing Adapter의 의존성 관리 (Lines 241-246):**
- Dependency Inversion Principle 활용 필요
- 제어 흐름 반대 방향으로 의존성을 역전
- application 계층에 인터페이스 생성, adapter에서 클래스로 구현
- 헥사고날 아키텍처에서 이 인터페이스가 port
- application 계층이 port 인터페이스를 호출하여 adapter 기능 사용 (Figure 10)

**의존성 주입 메커니즘 (Lines 253-266):**

**문제 (Lines 253-255):**
- 누가 port 인터페이스를 구현한 실제 객체를 application에 제공하는가?
- application 계층 내에서 port를 수동으로 인스턴스화하면 adapter 의존성 생김 (원치 않음)

**해결책: 중립 컴포넌트 (Lines 256-258):**
- 모든 계층에 의존성을 가진 중립적 컴포넌트 도입
- 아키텍처를 구성하는 대부분의 클래스를 인스턴스화할 책임

**동작 방식 예시 (Lines 259-266):**

```python
# 의존성 주입 컴포넌트가 생성하는 인스턴스들
# - AccountController
# - SendMoneyService
# - AccountPersistenceAdapter

# 1. AccountController 생성
class AccountController:
    def __init__(self, send_money_use_case: SendMoneyUseCase):
        # 의존성 주입이 SendMoneyService 인스턴스를 주입
        # Controller는 실제로 SendMoneyService를 받지만
        # SendMoneyUseCase 인터페이스만 알면 됨
        self.send_money = send_money_use_case

# 2. SendMoneyService 생성
class SendMoneyService:
    def __init__(self, load_account_port: LoadAccountPort):
        # 의존성 주입이 AccountPersistenceAdapter 인스턴스를 주입
        # Service는 실제 클래스를 모르고 LoadAccountPort 인터페이스만 앎
        self.load_account = load_account_port
```

**Lines 259-262**: 중립 의존성 주입 컴포넌트가 AccountController, SendMoneyService, AccountPersistenceAdapter 인스턴스 생성

**Lines 262-263**: AccountController가 SendMoneyUseCase를 요구하면, 의존성 주입이 생성 시 SendMoneyService 인스턴스를 제공. Controller는 실제로 SendMoneyService 인스턴스를 받았지만 인터페이스만 알면 되므로 모름.

**Lines 264-266**: SendMoneyService 인스턴스 생성 시, 의존성 주입 메커니즘이 AccountPersistenceAdapter 인스턴스를 LoadAccountPort 인터페이스 형태로 주입. Service는 인터페이스 뒤의 실제 클래스를 절대 모름.

**추가 정보 (Lines 267-268):**
Spring 프레임워크를 이용한 애플리케이션 초기화는 Chapter 9 "Assembling the Application"에서 다룸.

---

### 결론: 유지보수 가능한 소프트웨어 구축 지원 방법
**참조: Lines 273-278**

헥사고날 아키텍처를 위한 패키지 구조를 통해 실제 코드 구조를 목표 아키텍처에 최대한 가깝게 만들었다 (Lines 274-275).

**주요 이점:**
- 아키텍처 요소를 코드에서 찾는 것이 패키지 구조를 따라 탐색하는 문제로 단순화됨
- 아키텍처 다이어그램의 박스 이름을 따라 내려가면 됨
- 커뮤니케이션, 개발, 유지보수에 도움 (Lines 276-277)

**다음 단계 (Lines 278-279):**
이후 장들에서 패키지 구조와 의존성 주입을 실제로 활용:
- application 계층의 use case 구현
- web adapter 구현
- persistence adapter 구현
