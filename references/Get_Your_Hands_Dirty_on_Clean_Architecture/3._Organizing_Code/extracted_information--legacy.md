# 3장: Organizing Code - 추출된 정보

## 압축 내용
계층별 구조와 기능별 구조의 한계를 극복하기 위해 hexagonal 아키텍처의 구성 요소(adapter, port, domain, application)를 직접 반영하는 표현적 패키지 구조를 사용하면, 코드와 아키텍처 간 간극을 줄이고 의존성 주입을 통해 clean architecture의 의존성 규칙을 준수할 수 있다.

## 핵심 내용

### 핵심 개념
- **계층별 구조(Organizing By Layer)**: web, domain, persistence 계층으로 패키지를 구성하는 전통적 방식
- **기능별 구조(Organizing By Feature)**: account 같은 기능 단위로 패키지를 구성하는 방식
- **아키텍처 표현 구조(Architecturally Expressive Package Structure)**: adapter(in/out), domain, application, port(in/out)를 직접 반영하는 구조
- **의존성 주입(Dependency Injection)**: 중립적 컴포넌트가 모든 계층에 의존하며 객체를 인스턴스화하여 의존성을 주입하는 메커니즘

### 핵심 개념 설명

**계층별 구조**는 web, domain, persistence 각 계층마다 전용 패키지를 두는 방식이다. DIP를 적용하여 domain 패키지의 AccountRepository interface를 persistence 패키지의 AccountRepositoryImpl이 구현하도록 하여 의존성이 domain 코드를 향하도록 한다. 하지만 세 가지 문제점이 있다: (1) 기능적 슬라이스/피처 간 패키지 경계가 없어 UserController, UserService 등이 추가되면 클래스 혼재가 발생한다, (2) AccountService/AccountController가 어떤 유스케이스를 구현하는지 보이지 않아 특정 기능을 찾기 위해 추측해야 한다, (3) hexagonal 아키텍처를 추측할 수는 있지만 어떤 기능이 web adapter에 의해 호출되고 persistence adapter가 제공하는지 한눈에 보이지 않으며 incoming/outgoing port가 코드에 숨겨져 있다. (페이지 25-26, 줄 15-66)

**기능별 구조**는 account 관련 모든 코드를 고수준 패키지 account에 넣고 계층 패키지를 제거한다. 새 기능 그룹마다 새 고수준 패키지를 만들고 package-private visibility로 외부에서 접근하지 말아야 할 클래스를 보호하여 기능 간 원치 않는 의존성을 방지한다. AccountService를 SendMoneyService로 이름 변경하여 책임을 좁히면 클래스 이름만으로 "Send Money" 유스케이스 구현을 볼 수 있으며, 이는 Robert Martin이 "Screaming Architecture"라 부르는 기능의 가시성이다. 하지만 아키텍처 가시성은 더 떨어진다: 어댑터를 식별할 패키지 이름이 없고, incoming/outgoing port가 보이지 않으며, DIP를 적용했지만 package-private visibility로 도메인 코드를 persistence 코드로부터 보호할 수 없다. (페이지 26-27, 줄 67-108)

**아키텍처 표현 구조**는 hexagonal 아키텍처의 주요 요소(entities, use cases, incoming/outgoing ports, incoming/outgoing adapters)를 직접 패키지 구조에 반영한다. 최상위 account 패키지 아래에 adapter(in/web, out/persistence), domain, application, port(in, out) 패키지를 두어 각 아키텍처 요소를 직접 매핑한다. Domain 패키지에는 도메인 모델이, application 패키지에는 SendMoneyService가 있으며, SendMoneyService는 incoming port interface SendMoneyUseCase를 구현하고 outgoing port interfaces LoadAccountPort와 UpdateAccountStatePort를 사용한다. (페이지 27-28, 줄 110-186)

이 구조는 "architecture/code gap" 또는 "model/code gap"과 싸우는 강력한 요소다. 대부분 소프트웨어 프로젝트에서 아키텍처는 코드에 직접 매핑될 수 없는 추상적 개념이며, 시간이 지나면서 패키지 구조가 아키텍처를 반영하지 않으면 코드가 목표 아키텍처에서 점점 더 벗어난다. 표현적 패키지 구조는 아키텍처에 대한 능동적 사고를 촉진하며, 많은 패키지가 있어 현재 작업 중인 코드를 어느 패키지에 넣을지 생각해야 한다. Adapter 패키지의 클래스들은 application 패키지의 port interface를 통해서만 호출되므로 package-private일 수 있어 application 계층에서 adapter 클래스로의 우발적 의존성이 없다. Application과 domain 패키지 내에서는 일부 클래스가 public이어야 한다: port는 adapter가 접근해야 하므로 public, domain 클래스는 service와 adapter가 접근해야 하므로 public, 하지만 service는 incoming port interface 뒤에 숨길 수 있어 public일 필요가 없다. (페이지 28-29, 줄 187-212)

이 구조는 adapter를 자체 패키지로 이동시켜 필요 시 다른 구현으로 쉽게 교체할 수 있고, DDD 개념에 직접 매핑된다. 고수준 패키지 account는 다른 bounded context와 통신하기 위한 전용 진입/출구점(port)을 가진 bounded context이며, domain 패키지 내에서 DDD가 제공하는 모든 도구를 사용하여 도메인 모델을 구축할 수 있다. (페이지 29, 줄 218-232)

**의존성 주입**은 clean architecture의 필수 요구사항인 "application 계층이 incoming/outgoing adapter에 의존성을 갖지 않는다"를 충족하는 메커니즘이다. Incoming adapter(web adapter)는 제어 흐름과 의존성 방향이 같아 쉽다: adapter가 단순히 application 계층의 service를 호출하며, 진입점을 명확히 구분하기 위해 실제 service를 port interface 뒤에 숨길 수 있다. Outgoing adapter(persistence adapter)는 DIP를 사용하여 의존성을 제어 흐름 반대로 역전시킨다. Application 계층에 interface(port)를 생성하고 adapter의 클래스가 이를 구현하면, application 계층이 port interface를 호출하여 adapter 기능을 호출한다. (페이지 29-30, 줄 233-246)

Port interface를 구현하는 실제 객체는 누가 제공하는가? Application 계층에서 port를 수동으로 인스턴스화하고 싶지 않으며(adapter에 대한 의존성 도입을 원하지 않음), 이때 의존성 주입이 사용된다. 모든 계층에 의존성을 가진 중립적 컴포넌트를 도입하여 아키텍처를 구성하는 대부분의 클래스를 인스턴스화한다. 예를 들어 AccountController, SendMoneyService, AccountPersistenceAdapter의 인스턴스를 생성하며, AccountController가 SendMoneyUseCase를 필요로 하면 SendMoneyService 인스턴스를 주입하고(controller는 interface만 알고 실제 클래스를 모름), SendMoneyService 구성 시 AccountPersistenceAdapter 인스턴스를 LoadAccountPort interface 형태로 주입한다(service는 interface 뒤의 실제 클래스를 모름). (페이지 30, 줄 253-268)

### 핵심 개념 간 관계

**계층별 구조**는 기능적 경계 부재, 유스케이스 불가시성, 아키텍처 은폐라는 문제를 가지며, **기능별 구조**는 기능적 경계와 유스케이스 가시성(Screaming Architecture)은 개선하지만 아키텍처 가시성을 더 악화시킨다.

**아키텍처 표현 구조**는 두 접근의 문제를 해결하여 기능별 최상위 패키지(account)로 기능적 경계를 제공하고, 명확한 유스케이스 이름(SendMoneyService)으로 가시성을 확보하며, adapter/port/domain/application 구조로 hexagonal 아키텍처를 직접 반영한다. 이는 architecture/code gap을 줄이고 아키텍처에 대한 능동적 사고를 촉진하며, package-private visibility로 의존성을 통제하고, adapter 교체 용이성과 DDD 개념 매핑을 제공한다.

**의존성 주입**은 아키텍처 표현 구조가 의존성 규칙을 준수하도록 하는 메커니즘이다. Incoming adapter는 자연스럽게 의존성 방향이 올바르지만, outgoing adapter는 DIP를 통해 역전된 의존성을 구현하며, 의존성 주입이 port interface 구현체를 제공하여 application 계층이 adapter에 직접 의존하지 않도록 한다.

계층별 구조의 문제 → 기능별 구조의 부분적 개선 → 아키텍처 표현 구조의 종합적 해결 → 의존성 주입을 통한 의존성 규칙 준수라는 진화 관계를 형성하며, 최종적으로 코드와 아키텍처의 일치, 유지보수성 향상을 달성한다.

## 상세 핵심 내용

### 중요 개념

- **계층별 구조(Organizing By Layer)**
- **기능별 구조(Organizing By Feature)**
- **아키텍처 표현 구조(Architecturally Expressive Package Structure)**
- **의존성 주입(Dependency Injection)**
- **기능적 슬라이스(Functional Slices)**
- **Screaming Architecture**
- **Architecture/Code Gap (Model/Code Gap)**
- **Package-Private Visibility**
- **Incoming/Outgoing Ports**
- **Incoming/Outgoing (Driving/Driven) Adapters**
- **Bounded Context (DDD)**
- **중립적 의존성 주입 컴포넌트**

### 중요 개념 설명

**계층별 구조**는 BuckPal 예제 애플리케이션의 "Send Money" 유스케이스(사용자가 자신의 계좌에서 다른 계좌로 돈을 이체)를 구성하는 첫 번째 접근 방식이다. Web, domain, persistence 각 계층마다 전용 패키지를 두며, 1장에서 논의한 단순 계층의 문제를 피하기 위해 DIP를 적용하여 domain 패키지를 향하는 의존성만 허용한다. Domain 패키지에 AccountRepository interface를 도입하고 persistence 패키지에서 이를 구현하는 방식이다. (페이지 25, 줄 15-47)

**계층별 구조의 문제점**: (1) **기능적 슬라이스** 간 패키지 경계가 없다. 사용자 관리 기능을 추가하면 web 패키지에 UserController, domain 패키지에 UserService, UserRepository, User, persistence 패키지에 UserRepositoryImpl을 추가하게 되며, 추가 구조 없이 클래스들이 혼재되어 애플리케이션의 무관한 기능 간 원치 않는 부작용을 유발할 수 있다. (페이지 26, 줄 53-57)

(2) 애플리케이션이 제공하는 유스케이스를 볼 수 없다. AccountService나 AccountController 클래스가 어떤 유스케이스를 구현하는지 알 수 없으며, 특정 기능을 찾기 위해 어떤 service가 구현하는지 추측하고 그 service 내에서 책임 있는 메서드를 찾아야 한다. (페이지 26, 줄 58-61)

(3) 패키지 구조 내에서 목표 아키텍처를 볼 수 없다. Hexagonal 아키텍처 스타일을 따랐다고 추측하고 web과 persistence 패키지의 클래스를 탐색하여 web/persistence adapter를 찾을 수 있지만, web adapter가 어떤 기능을 호출하고 persistence adapter가 domain 계층에 어떤 기능을 제공하는지 한눈에 볼 수 없다. Incoming/outgoing port가 코드에 숨겨져 있다. (페이지 26, 줄 62-66)

**기능별 구조**는 계층별 구조의 문제를 해결하려는 시도로, account 관련 모든 코드를 고수준 패키지 account에 넣고 계층 패키지를 제거한다. 각 새 기능 그룹은 account 옆에 새 고수준 패키지를 얻으며, 외부에서 접근하지 말아야 할 클래스에 package-private visibility를 사용하여 패키지 경계를 강제할 수 있다. Package 경계와 package-private visibility를 결합하여 기능 간 원치 않는 의존성을 방지할 수 있다. (페이지 26, 줄 67-90)

AccountService를 SendMoneyService로 이름 변경하여 책임을 좁히면(계층별 접근에서도 할 수 있었음), 클래스 이름만으로 "Send Money" 유스케이스를 구현한다는 것을 볼 수 있다. 애플리케이션 기능을 코드에 가시적으로 만드는 것은 Robert Martin이 "**Screaming Architecture**"라 부르는 것으로, 의도를 우리에게 외친다(scream). (페이지 26-27, 줄 91-99)

하지만 기능별 접근은 아키텍처를 계층별 접근보다 덜 가시적으로 만든다. Adapter를 식별할 패키지 이름이 없고, incoming/outgoing port가 여전히 보이지 않는다. 더욱이 domain 코드와 persistence 코드 간 의존성을 역전시켜 SendMoneyService가 AccountRepository interface만 알고 구현은 모르지만, package-private visibility를 사용하여 도메인 코드를 persistence 코드로의 우발적 의존성으로부터 보호할 수 없다. (페이지 27, 줄 100-105)

**아키텍처 표현 구조**: 목표 아키텍처를 한눈에 볼 수 있도록 하려면? 아키텍처 다이어그램(예: 그림 9)의 박스에 손가락을 가리켜 그 박스를 담당하는 코드의 부분을 즉시 알 수 있다면 좋을 것이다. 이를 지원할 만큼 충분히 표현적인 패키지 구조를 만들자. (페이지 27, 줄 106-109)

Hexagonal 아키텍처에서 주요 아키텍처 요소는 entities, use cases, incoming/outgoing ports, incoming/outgoing (또는 "driving"/"driven") adapters다. 이들을 이 아키텍처를 표현하는 패키지 구조에 맞춰보자. (페이지 27, 줄 110-113)

아키텍처의 각 요소를 패키지 중 하나에 직접 매핑할 수 있다. 최상위에는 Account 관련 유스케이스를 구현하는 모듈임을 나타내는 account 패키지가 있다. 다음 수준에는 도메인 모델을 포함하는 domain 패키지가 있다. Application 패키지는 이 도메인 모델 주변의 service 계층을 포함한다. SendMoneyService는 incoming port interface SendMoneyUseCase를 구현하고 outgoing port interfaces LoadAccountPort와 UpdateAccountStatePort를 사용하며, 이들은 persistence adapter가 구현한다. (페이지 28, 줄 176-182)

Adapter 패키지는 application 계층의 incoming port를 호출하는 incoming adapter와 application 계층의 outgoing port를 위한 구현을 제공하는 outgoing adapter를 포함한다. 이 경우 각각 자체 하위 패키지를 가진 web과 persistence adapter로 단순한 웹 애플리케이션을 구축하고 있다. (페이지 28, 줄 183-186)

많은 기술적 소리 나는 패키지가 있지만 혼란스러운가? 사무실 벽에 hexagonal 아키텍처의 고수준 뷰가 걸려 있고 소비하는 서드파티 API의 클라이언트 수정에 대해 동료와 이야기한다고 상상해보자. 논의하는 동안 포스터의 해당 outgoing adapter를 가리켜 서로를 더 잘 이해할 수 있다. 이야기가 끝나면 IDE 앞에 앉아 즉시 클라이언트 작업을 시작할 수 있는데, 이야기한 API 클라이언트의 코드가 adapter/out/<name-of-adapter> 패키지에 있기 때문이다. 혼란스럽기보다는 도움이 되지 않는가? (페이지 28, 줄 188-194)

**Architecture/Code Gap**: 이 패키지 구조는 소위 "architecture/code gap" 또는 "model/code gap"과 싸우는 강력한 요소다. 이 용어는 대부분 소프트웨어 개발 프로젝트에서 아키텍처가 코드에 직접 매핑될 수 없는 추상적 개념일 뿐이라는 사실을 설명한다. 시간이 지나면서 (다른 것들 중에서) 패키지 구조가 아키텍처를 반영하지 않으면, 코드는 보통 목표 아키텍처에서 점점 더 벗어나게 된다. (페이지 28, 줄 195-199)

또한 이 표현적 패키지 구조는 아키텍처에 대한 능동적 사고를 촉진한다. 많은 패키지가 있고 현재 작업 중인 코드를 어느 패키지에 넣을지 생각해야 한다. (페이지 28, 줄 200-202)

**Package-Private Visibility**: 많은 패키지가 패키지 간 접근을 허용하기 위해 모든 것이 public이어야 한다는 의미인가? 적어도 adapter 패키지에는 그렇지 않다. 포함하는 모든 클래스가 package-private일 수 있는데, application 패키지 내에 있는 port interface를 통해서만 외부 세계에서 호출되기 때문이다. 따라서 application 계층에서 adapter 클래스로의 우발적 의존성이 없다. (페이지 28, 줄 203-208)

하지만 application과 domain 패키지 내에서는 일부 클래스가 실제로 public이어야 한다. Port는 설계상 adapter가 접근할 수 있어야 하므로 public이어야 한다. Domain 클래스는 service와 잠재적으로 adapter가 접근할 수 있어야 하므로 public이어야 한다. Service는 incoming port interface 뒤에 숨길 수 있으므로 public일 필요가 없다. (페이지 28-29, 줄 209-212)

**어댑터 교체 용이성**: Adapter 코드를 자체 패키지로 이동시키는 것은 필요가 생기면 한 adapter를 다른 구현으로 매우 쉽게 교체할 수 있다는 추가 이점이 있다. 처음에 어떤 데이터베이스가 최선인지 확신이 없어 단순한 key-value 데이터베이스로 구현을 시작했고, 이제 SQL 데이터베이스로 전환해야 한다고 상상해보자. 새 adapter 패키지에서 모든 관련 outgoing port를 구현하고 이전 패키지를 제거하기만 하면 된다. (페이지 29, 줄 218-222)

**Bounded Context (DDD) 매핑**: 이 패키지 구조의 또 다른 매우 매력적인 장점은 DDD 개념에 직접 매핑된다는 것이다. 이 경우 고수준 패키지 account는 다른 bounded context와 통신하기 위한 전용 진입 및 출구점(port)을 가진 bounded context다. Domain 패키지 내에서 DDD가 제공하는 모든 도구를 사용하여 원하는 도메인 모델을 구축할 수 있다. (페이지 29, 줄 223-226)

모든 구조와 마찬가지로, 소프트웨어 프로젝트 수명 동안 이 패키지 구조를 유지하려면 규율이 필요하다. 또한 패키지 구조가 맞지 않아 architecture/code gap을 넓히고 아키텍처를 반영하지 않는 패키지를 만드는 것 외에 다른 방법을 볼 수 없는 경우도 있을 것이다. 완벽은 없다. 하지만 표현적 패키지 구조로 적어도 코드와 아키텍처 간 간극을 줄일 수 있다. (페이지 29, 줄 227-232)

**의존성 주입의 역할**: 위에서 설명한 패키지 구조는 clean architecture를 향해 먼 길을 가지만, 2장 "Inverting Dependencies"에서 배운 것처럼 그러한 아키텍처의 필수 요구사항은 application 계층이 incoming/outgoing adapter에 대한 의존성을 갖지 않는다는 것이다. (페이지 29, 줄 233-236)

**Incoming Adapter의 의존성**: Web adapter 같은 incoming adapter의 경우 제어 흐름이 adapter와 domain 코드 간 의존성과 같은 방향을 가리키므로 쉽다. Adapter는 단순히 application 계층 내의 service를 호출한다. 애플리케이션으로의 진입점을 명확히 구분하기 위해 실제 service를 port interface 뒤에 숨기고 싶을 수 있다. (페이지 29, 줄 237-240)

**Outgoing Adapter의 의존성**: Persistence adapter 같은 outgoing adapter의 경우 Dependency Inversion Principle을 사용하여 의존성을 제어 흐름의 반대 방향으로 역전시켜야 한다. Application 계층 내에 interface를 생성하고 adapter 내의 클래스가 이를 구현하는 방식을 이미 봤다. Hexagonal 아키텍처에서 이 interface는 port다. 그러면 application 계층이 이 port interface를 호출하여 그림 10에 표시된 것처럼 adapter의 기능을 호출한다. (페이지 29-30, 줄 241-246)

**중립적 의존성 주입 컴포넌트**: 하지만 port interface를 구현하는 실제 객체를 누가 애플리케이션에 제공하는가? Application 계층 내에서 port를 수동으로 인스턴스화하고 싶지 않은데, adapter에 대한 의존성을 도입하고 싶지 않기 때문이다. 여기서 의존성 주입이 등장한다. 모든 계층에 의존성을 가진 중립적 컴포넌트를 도입한다. 이 컴포넌트는 아키텍처를 구성하는 대부분의 클래스를 인스턴스화할 책임이 있다. (페이지 30, 줄 253-258)

위 예제 그림에서 중립적 의존성 주입 컴포넌트는 AccountController, SendMoneyService, AccountPersistenceAdapter 클래스의 인스턴스를 생성할 것이다. AccountController가 SendMoneyUseCase를 필요로 하므로, 의존성 주입은 생성 중에 SendMoneyService 클래스의 인스턴스를 줄 것이다. Controller는 interface만 알면 되므로 실제로 SendMoneyService 인스턴스를 받았다는 것을 모른다. (페이지 30, 줄 259-263)

유사하게, SendMoneyService 인스턴스를 구성할 때 의존성 주입 메커니즘은 LoadAccountPort interface의 모습으로 AccountPersistenceAdapter 클래스의 인스턴스를 주입할 것이다. Service는 interface 뒤의 실제 클래스를 결코 모른다. (페이지 30, 줄 264-266)

9장 "Assembling the Application"에서 Spring framework를 예로 사용하여 애플리케이션 초기화에 대해 더 이야기할 것이다. (페이지 30, 줄 267-268)

### 중요 개념 간 관계

**계층별 구조**는 세 가지 문제(기능적 경계 부재, 유스케이스 불가시성, 아키텍처 은폐)를 가지며, **기능별 구조**는 첫 두 문제(기능적 경계, 유스케이스 가시성)를 개선하지만 세 번째 문제(아키텍처 가시성)를 악화시킨다.

**아키텍처 표현 구조**는 계층별 구조의 DIP 적용을 유지하면서 기능별 구조의 장점(기능별 최상위 패키지, Screaming Architecture)을 통합하고, adapter/port/domain/application 패키지로 아키텍처를 직접 반영하여 세 문제를 모두 해결한다.

**Package-Private Visibility**는 아키텍처 표현 구조에서 의존성 통제의 핵심 메커니즘으로, adapter 패키지는 package-private로 유지하여 application 계층으로부터 보호하고, application/domain 패키지의 port와 domain 클래스는 설계상 public이어야 하지만 service는 port interface 뒤에 숨길 수 있다.

**의존성 주입**은 아키텍처 표현 구조가 의존성 규칙(application 계층이 adapter에 의존하지 않음)을 준수하도록 하는 메커니즘이다. **Incoming Adapter**는 자연스럽게 올바른 의존성 방향을 가지지만, **Outgoing Adapter**는 DIP를 통해 의존성을 역전시키며, **중립적 의존성 주입 컴포넌트**가 port interface 구현체를 인스턴스화하여 주입함으로써 application 계층이 실제 구현 클래스를 알지 못하도록 한다.

**Architecture/Code Gap** 감소는 아키텍처 표현 구조의 주요 효과로, 코드가 목표 아키텍처에서 벗어나는 것을 방지하고 능동적 아키텍처 사고를 촉진한다. 이는 **Bounded Context (DDD) 매핑**과 **어댑터 교체 용이성**으로 연결되어 도메인 모델링 자유도와 기술 스택 유연성을 제공한다.

계층별 구조의 문제 인식 → 기능별 구조의 부분적 개선 → 아키텍처 표현 구조의 종합적 해결 → Package-Private Visibility와 의존성 주입을 통한 의존성 규칙 준수 → Architecture/Code Gap 감소 → DDD 통합과 어댑터 교체 용이성이라는 연쇄적 개선 흐름을 형성하며, 최종적으로 코드와 아키텍처의 일치, 유지보수성 향상을 달성한다.

## 상세 내용

### 1. 서론: 코드로 아키텍처 인식하기

코드를 보는 것만으로 아키텍처를 인식할 수 있다면 좋지 않겠는가? 이 장에서는 코드를 구성하는 다양한 방법을 검토하고 hexagonal 아키텍처를 직접 반영하는 표현적 패키지 구조를 소개할 것이다. (페이지 25, 줄 3-6)

Greenfield 소프트웨어 프로젝트에서 올바르게 만들려고 하는 첫 번째 것은 패키지 구조다. 프로젝트의 나머지 기간 동안 사용할 의도로 멋지게 보이는 구조를 설정한다. 그러다 프로젝트 중에 일이 바빠지고 많은 곳에서 패키지 구조가 구조화되지 않은 코드 혼란을 위한 멋지게 보이는 외관일 뿐이라는 것을 깨닫는다. 한 패키지의 클래스가 가져오면 안 되는 다른 패키지의 클래스를 가져온다. (페이지 25, 줄 7-11)

서문에서 소개한 BuckPal 예제 애플리케이션의 코드를 구조화하는 다양한 옵션을 논의할 것이다. 더 구체적으로, 사용자가 자신의 계좌에서 다른 계좌로 돈을 이체할 수 있는 유스케이스 "Send Money"를 살펴볼 것이다. (페이지 25, 줄 12-14)

**참조**: 페이지 25, 줄 3-14

### 2. 계층별 구성 (Organizing By Layer)

이전 화제와의 관계: 서론에서 코드 구성 방법을 탐색하겠다고 했으므로, 첫 번째 접근 방식을 제시한다.

#### 2.1 계층별 구조

코드를 구성하는 첫 번째 접근은 계층별이다. 코드를 다음과 같이 구성할 수 있다: (페이지 25, 줄 15-16)

```
buckpal
├──domain
|  ├──Account
|  ├──Activity
|  ├──AccountRepository
|  └──AccountService
├──persistence
|  └──AccountRepositoryImpl
└──web
   └──AccountController
```

Web, domain, persistence 각 계층마다 전용 패키지가 있다. 1장 "What's Wrong with Layers?"에서 논의한 것처럼 단순한 계층이 여러 이유로 코드의 최선 구조가 아닐 수 있으므로, 여기서는 이미 Dependency Inversion Principle을 적용하여 domain 패키지의 도메인 코드를 향하는 의존성만 허용했다. Domain 패키지에 AccountRepository interface를 도입하고 persistence 패키지에서 이를 구현하여 이를 수행했다. (페이지 25, 줄 17-47)

**참조**: 페이지 25, 줄 15-47

#### 2.2 세 가지 문제점

하지만 이 패키지 구조가 최적이 아닌 최소 세 가지 이유를 찾을 수 있다. (페이지 25, 줄 48)

**참조**: 페이지 25, 줄 48

#### 2.3 문제 1: 기능적 경계 부재

첫째, 애플리케이션의 기능적 슬라이스(functional slices) 또는 피처(features) 간에 패키지 경계가 없다. 사용자 관리 기능을 추가하면, web 패키지에 UserController, domain 패키지에 UserService, UserRepository, User, persistence 패키지에 UserRepositoryImpl을 추가할 것이다. 추가 구조 없이 이것은 빠르게 클래스들의 혼란이 되어 애플리케이션의 무관한 것으로 추정되는 피처들 간에 원치 않는 부작용을 유발할 수 있다. (페이지 26, 줄 53-57)

**참조**: 페이지 26, 줄 53-57

#### 2.4 문제 2: 유스케이스 불가시성

둘째, 애플리케이션이 제공하는 유스케이스를 볼 수 없다. AccountService나 AccountController 클래스가 어떤 유스케이스를 구현하는지 말할 수 있는가? 특정 기능을 찾고 있다면, 어떤 service가 이를 구현하는지 추측한 다음 그 service 내에서 책임 있는 메서드를 검색해야 한다. (페이지 26, 줄 58-61)

**참조**: 페이지 26, 줄 58-61

#### 2.5 문제 3: 아키텍처 은폐

유사하게, 패키지 구조 내에서 목표 아키텍처를 볼 수 없다. Hexagonal 아키텍처 스타일을 따랐다고 추측한 다음 web과 persistence 패키지의 클래스를 탐색하여 web과 persistence adapter를 찾을 수 있다. 하지만 web adapter가 어떤 기능을 호출하고 persistence adapter가 domain 계층에 어떤 기능을 제공하는지 한눈에 볼 수 없다. Incoming과 outgoing port가 코드에 숨겨져 있다. (페이지 26, 줄 62-66)

**참조**: 페이지 26, 줄 62-66

### 3. 기능별 구성 (Organizing By Feature)

이전 화제와의 관계: 계층별 구조의 문제점을 지적했으므로, 이를 해결하려는 다음 접근 방식을 제시한다.

#### 3.1 기능별 구조

"계층별 구성" 접근의 일부 문제를 해결해보자. 다음 접근은 기능별로 코드를 구성하는 것이다: (페이지 26, 줄 67-69)

```
buckpal
└──account
   ├──Account
   ├──AccountController
   ├──AccountRepository
   ├──AccountRepositoryImpl
   └──SendMoneyService
```

본질적으로 account 관련 모든 코드를 고수준 패키지 account에 넣었다. 계층 패키지도 제거했다. (페이지 26, 줄 84-85)

각 새 기능 그룹은 account 옆에 새 고수준 패키지를 얻을 것이고, 외부에서 접근하면 안 되는 클래스에 package-private visibility를 사용하여 기능 간 패키지 경계를 강제할 수 있다. (페이지 26, 줄 86-88)

Package-private visibility와 결합된 패키지 경계는 기능 간 원치 않는 의존성을 방지할 수 있게 해준다. 체크. (페이지 26, 줄 89-90)

**참조**: 페이지 26, 줄 67-90

#### 3.2 유스케이스 가시성 개선 (Screaming Architecture)

AccountService를 SendMoneyService로 이름을 변경하여 책임을 좁혔다(계층별 접근에서도 할 수 있었음). 이제 클래스 이름만 보고 코드가 "Send Money" 유스케이스를 구현한다는 것을 볼 수 있다. 애플리케이션 기능을 코드에 가시적으로 만드는 것은 Robert Martin이 "Screaming Architecture"라 부르는 것인데, 의도를 우리에게 외치기(screams) 때문이다. 체크. (페이지 26-27, 줄 91-99)

**참조**: 페이지 26-27, 줄 91-99

#### 3.3 아키텍처 가시성 악화

하지만 기능별 접근은 아키텍처를 계층별 접근보다 덜 가시적으로 만든다. Adapter를 식별할 패키지 이름이 없고, incoming과 outgoing port가 여전히 보이지 않는다. 더욱이 domain 코드와 persistence 코드 간 의존성을 역전시켜 SendMoneyService가 AccountRepository interface만 알고 구현은 모르게 했지만, package-private visibility를 사용하여 도메인 코드를 persistence 코드로의 우발적 의존성으로부터 보호할 수 없다. (페이지 27, 줄 100-105)

**참조**: 페이지 27, 줄 100-105

#### 3.4 아키텍처 가시성의 필요성

그렇다면 어떻게 목표 아키텍처를 한눈에 볼 수 있게 만들 수 있을까? 그림 9 같은 아키텍처 다이어그램의 박스에 손가락을 가리켜 그 박스를 담당하는 코드의 부분을 즉시 알 수 있다면 좋을 것이다. 이를 지원할 만큼 충분히 표현적인 패키지 구조를 만들기 위해 한 단계 더 나아가자. (페이지 27, 줄 106-109)

**참조**: 페이지 27, 줄 106-109

### 4. 아키텍처 표현 패키지 구조 (An Architecturally Expressive Package Structure)

이전 화제와의 관계: 기능별 구조가 아키텍처 가시성을 악화시켰으므로, 이를 해결하는 최종 접근 방식을 제시한다.

#### 4.1 Hexagonal 아키텍처 요소

Hexagonal 아키텍처에서 주요 아키텍처 요소로 entities, use cases, incoming/outgoing ports, incoming/outgoing (또는 "driving"/"driven") adapters가 있다. 이들을 이 아키텍처를 표현하는 패키지 구조에 맞춰보자: (페이지 27, 줄 110-113)

```
buckpal
└──account
   ├──adapter
   |  ├──in
   |  |  └──web
   |  |     └──AccountController
   |  ├──out
   |  |  └──persistence
   |  |     ├──AccountPersistenceAdapter
   |  |     └──SpringDataAccountRepository
   ├──domain
   |  ├──Account
   |  └──Activity
   └──application
      └──SendMoneyService
      └──port
         ├──in
         |  └──SendMoneyUseCase
         └──out
            ├──LoadAccountPort
            └──UpdateAccountStatePort
```

**참조**: 페이지 27, 줄 110-171

#### 4.2 패키지 매핑

아키텍처의 각 요소를 패키지 중 하나에 직접 매핑할 수 있다. 최상위에는 다시 account라는 이름의 패키지가 있어 이것이 Account 관련 유스케이스를 구현하는 모듈임을 나타낸다. (페이지 28, 줄 176-178)

다음 수준에는 도메인 모델을 포함하는 domain 패키지가 있다. Application 패키지는 이 도메인 모델 주변의 service 계층을 포함한다. SendMoneyService는 incoming port interface SendMoneyUseCase를 구현하고 outgoing port interfaces LoadAccountPort와 UpdateAccountStatePort를 사용하며, 이들은 persistence adapter가 구현한다. (페이지 28, 줄 179-182)

Adapter 패키지는 application 계층의 incoming port를 호출하는 incoming adapter와 application 계층의 outgoing port를 위한 구현을 제공하는 outgoing adapter를 포함한다. 이 경우 각각 자체 하위 패키지를 가진 web과 persistence adapter로 단순한 웹 애플리케이션을 구축하고 있다. (페이지 28, 줄 183-186)

**참조**: 페이지 28, 줄 176-186

#### 4.3 혼란스러운가, 도움이 되는가?

휴, 많은 기술적 소리 나는 패키지다. 혼란스럽지 않은가? (페이지 28, 줄 187)

사무실 벽에 hexagonal 아키텍처의 고수준 뷰가 걸려 있고 소비하는 서드파티 API의 클라이언트 수정에 대해 동료와 이야기한다고 상상해보자. 논의하는 동안 포스터의 해당 outgoing adapter를 가리켜 서로를 더 잘 이해할 수 있다. 이야기가 끝나면 IDE 앞에 앉아 즉시 클라이언트 작업을 시작할 수 있는데, 이야기한 API 클라이언트의 코드가 adapter/out/<name-of-adapter> 패키지에 있기 때문이다. 혼란스럽기보다는 도움이 되지 않는가? (페이지 28, 줄 188-194)

**참조**: 페이지 28, 줄 187-194

#### 4.4 Architecture/Code Gap과의 싸움

이 패키지 구조는 소위 "architecture/code gap" 또는 "model/code gap"과 싸우는 강력한 요소다. 이 용어는 대부분 소프트웨어 개발 프로젝트에서 아키텍처가 코드에 직접 매핑될 수 없는 추상적 개념일 뿐이라는 사실을 설명한다. 시간이 지나면서 (다른 것들 중에서) 패키지 구조가 아키텍처를 반영하지 않으면, 코드는 보통 목표 아키텍처에서 점점 더 벗어나게 된다. (페이지 28, 줄 195-199)

또한 이 표현적 패키지 구조는 아키텍처에 대한 능동적 사고를 촉진한다. 많은 패키지가 있고 현재 작업 중인 코드를 어느 패키지에 넣을지 생각해야 한다. (페이지 28, 줄 200-202)

**참조**: 페이지 28, 줄 195-202

#### 4.5 Visibility와 접근성

하지만 많은 패키지가 패키지 간 접근을 허용하기 위해 모든 것이 public이어야 한다는 의미인가? (페이지 28, 줄 203-204)

적어도 adapter 패키지에는 그렇지 않다. 포함하는 모든 클래스가 package-private일 수 있는데, application 패키지 내에 있는 port interface를 통해서만 외부 세계에서 호출되기 때문이다. 따라서 application 계층에서 adapter 클래스로의 우발적 의존성이 없다. 체크. (페이지 28, 줄 205-208)

하지만 application과 domain 패키지 내에서는 일부 클래스가 실제로 public이어야 한다. Port는 설계상 adapter가 접근할 수 있어야 하므로 public이어야 한다. Domain 클래스는 service와 잠재적으로 adapter가 접근할 수 있어야 하므로 public이어야 한다. Service는 incoming port interface 뒤에 숨길 수 있으므로 public일 필요가 없다. (페이지 28-29, 줄 209-212)

**참조**: 페이지 28-29, 줄 203-212

#### 4.6 어댑터 교체 용이성

Adapter 코드를 자체 패키지로 이동시키는 것은 필요가 생기면 한 adapter를 다른 구현으로 매우 쉽게 교체할 수 있다는 추가 이점이 있다. 처음에 어떤 데이터베이스가 최선인지 확신이 없어 단순한 key-value 데이터베이스로 구현을 시작했고, 이제 SQL 데이터베이스로 전환해야 한다고 상상해보자. 새 adapter 패키지에서 모든 관련 outgoing port를 구현하고 이전 패키지를 제거하기만 하면 된다. (페이지 29, 줄 218-222)

**참조**: 페이지 29, 줄 218-222

#### 4.7 DDD 개념 매핑

이 패키지 구조의 또 다른 매우 매력적인 장점은 DDD 개념에 직접 매핑된다는 것이다. 이 경우 고수준 패키지 account는 다른 bounded context와 통신하기 위한 전용 진입 및 출구점(port)을 가진 bounded context다. Domain 패키지 내에서 DDD가 제공하는 모든 도구를 사용하여 원하는 도메인 모델을 구축할 수 있다. (페이지 29, 줄 223-226)

**참조**: 페이지 29, 줄 223-226

#### 4.8 유지의 어려움과 현실

모든 구조와 마찬가지로, 소프트웨어 프로젝트 수명 동안 이 패키지 구조를 유지하려면 규율이 필요하다. 또한 패키지 구조가 맞지 않아 architecture/code gap을 넓히고 아키텍처를 반영하지 않는 패키지를 만드는 것 외에 다른 방법을 볼 수 없는 경우도 있을 것이다. (페이지 29, 줄 227-230)

완벽은 없다. 하지만 표현적 패키지 구조로 적어도 코드와 아키텍처 간 간극을 줄일 수 있다. (페이지 29, 줄 231-232)

**참조**: 페이지 29, 줄 227-232

### 5. 의존성 주입의 역할 (The Role of Dependency Injection)

이전 화제와의 관계: 아키텍처 표현 구조를 제시했으므로, 이 구조가 clean architecture의 의존성 규칙을 준수하도록 하는 메커니즘을 설명한다.

#### 5.1 Clean Architecture의 필수 요구사항

위에서 설명한 패키지 구조는 clean architecture를 향해 먼 길을 가지만, 2장 "Inverting Dependencies"에서 배운 것처럼 그러한 아키텍처의 필수 요구사항은 application 계층이 incoming/outgoing adapter에 대한 의존성을 갖지 않는다는 것이다. (페이지 29, 줄 233-236)

**참조**: 페이지 29, 줄 233-236

#### 5.2 Incoming Adapter

Web adapter 같은 incoming adapter의 경우 제어 흐름이 adapter와 domain 코드 간 의존성과 같은 방향을 가리키므로 쉽다. Adapter는 단순히 application 계층 내의 service를 호출한다. 애플리케이션으로의 진입점을 명확히 구분하기 위해 실제 service를 port interface 뒤에 숨기고 싶을 수 있다. (페이지 29, 줄 237-240)

**참조**: 페이지 29, 줄 237-240

#### 5.3 Outgoing Adapter와 DIP

Persistence adapter 같은 outgoing adapter의 경우 Dependency Inversion Principle을 사용하여 의존성을 제어 흐름의 반대 방향으로 역전시켜야 한다. (페이지 29-30, 줄 241-242)

Application 계층 내에 adapter의 클래스가 구현하는 interface를 생성하는 방법을 이미 봤다. Hexagonal 아키텍처에서 이 interface는 port다. 그러면 application 계층이 그림 10에 표시된 것처럼 이 port interface를 호출하여 adapter의 기능을 호출한다. (페이지 30, 줄 243-246)

**참조**: 페이지 29-30, 줄 241-246

#### 5.4 의존성 주입의 필요성

하지만 port interface를 구현하는 실제 객체를 누가 애플리케이션에 제공하는가? Application 계층 내에서 port를 수동으로 인스턴스화하고 싶지 않은데, adapter에 대한 의존성을 도입하고 싶지 않기 때문이다. (페이지 30, 줄 253-255)

여기서 의존성 주입이 등장한다. 모든 계층에 의존성을 가진 중립적 컴포넌트를 도입한다. 이 컴포넌트는 아키텍처를 구성하는 대부분의 클래스를 인스턴스화할 책임이 있다. (페이지 30, 줄 256-258)

**참조**: 페이지 30, 줄 253-258

#### 5.5 의존성 주입 작동 방식

위 예제 그림에서 중립적 의존성 주입 컴포넌트는 AccountController, SendMoneyService, AccountPersistenceAdapter 클래스의 인스턴스를 생성할 것이다. AccountController가 SendMoneyUseCase를 필요로 하므로, 의존성 주입은 생성 중에 SendMoneyService 클래스의 인스턴스를 줄 것이다. Controller는 interface만 알면 되므로 실제로 SendMoneyService 인스턴스를 받았다는 것을 모른다. (페이지 30, 줄 259-263)

유사하게, SendMoneyService 인스턴스를 구성할 때 의존성 주입 메커니즘은 LoadAccountPort interface의 모습으로 AccountPersistenceAdapter 클래스의 인스턴스를 주입할 것이다. Service는 interface 뒤의 실제 클래스를 결코 모른다. (페이지 30, 줄 264-266)

9장 "Assembling the Application"에서 Spring framework를 예로 사용하여 애플리케이션 초기화에 대해 더 이야기할 것이다. (페이지 30, 줄 267-268)

**참조**: 페이지 30, 줄 259-268

### 6. 결론: 유지보수 가능한 소프트웨어 구축에 어떻게 도움이 되는가?

이전 화제와의 관계: 세 가지 패키지 구조와 의존성 주입을 논의했으므로, 이것이 유지보수성에 어떻게 기여하는지 종합한다.

Hexagonal 아키텍처를 위한 패키지 구조를 살펴봤으며, 실제 코드 구조를 목표 아키텍처에 최대한 가깝게 가져간다. 이제 코드에서 아키텍처 요소를 찾는 것은 아키텍처 다이어그램의 특정 박스 이름을 따라 패키지 구조를 탐색하는 문제이며, 커뮤니케이션, 개발, 유지보수에 도움이 된다. (페이지 31, 줄 273-277)

다음 장들에서 이 패키지 구조와 의존성 주입이 application 계층의 유스케이스, web adapter, persistence adapter를 구현하면서 실제 작동하는 것을 볼 것이다. (페이지 31, 줄 278-279)

**참조**: 페이지 31, 줄 273-279
