# 2장: Inverting Dependencies - 추출된 정보

## 압축 내용
Single Responsibility Principle과 Dependency Inversion Principle을 적용하여 도메인 코드가 외부 의존성을 갖지 않도록 의존성을 역전시키면, 계층형 아키텍처의 문제를 해결하고 Clean Architecture 또는 Hexagonal Architecture를 구축할 수 있다.

## 핵심 내용

### 핵심 개념
- **Single Responsibility Principle (SRP)**: "한 가지만 하라"가 아니라 "변경의 이유가 하나만 있어야 한다"는 원칙
- **Dependency Inversion Principle (DIP)**: 코드베이스 내 모든 의존성의 방향을 역전시킬 수 있는 원칙
- **Clean Architecture**: 비즈니스 규칙이 프레임워크, 데이터베이스, UI 기술로부터 독립적이고 테스트 가능한 아키텍처
- **Hexagonal Architecture (Ports and Adapters)**: 애플리케이션 코어를 중심으로 포트와 어댑터로 외부 시스템과 상호작용하는 구체적인 구조

### 핵심 개념 설명

**Single Responsibility Principle**은 흔히 "한 가지만 하고 올바르게 하라"로 오해되지만, 실제 정의는 "변경의 이유가 하나만 있어야 한다"는 것이다. 컴포넌트의 의존성은 각각 변경의 이유가 되며, 직접 또는 전이적 의존성을 통해 전파된다. 시간이 지나면서 컴포넌트가 더 많은 변경 이유를 축적하면 코드베이스가 변경하기 어렵고 비용이 많이 들게 된다. (페이지 17-18, 줄 8-43)

**Dependency Inversion Principle**은 이름 그대로 코드베이스 내 모든 의존성의 방향을 역전시킬 수 있다는 원칙이다(단, 양쪽 코드를 제어할 때만 가능). Domain 계층에 repository interface를 생성하고 persistence 계층에서 이를 구현하면, persistence 계층이 domain 계층에 의존하도록 역전시킬 수 있다. 이를 통해 도메인 로직을 persistence 코드에 대한 억압적인 의존성으로부터 해방시킨다. (페이지 19-20, 줄 66-99)

**Clean Architecture**는 Robert C. Martin이 정립한 개념으로, 비즈니스 규칙이 설계상 테스트 가능하고 프레임워크, 데이터베이스, UI 기술, 외부 애플리케이션으로부터 독립적인 아키텍처다. 도메인 코드는 외부 지향 의존성을 가져서는 안 되며, DIP를 통해 모든 의존성이 도메인 코드를 향하도록 한다. 동심원 계층 구조에서 Dependency Rule은 모든 의존성이 내부를 향해야 한다고 명시한다. 핵심에는 도메인 엔티티가 있고 그 주변에 use case(single responsibility를 가진 세분화된 service)가 있으며, 외부 계층은 persistence, UI, 서드파티 어댑터를 제공한다. (페이지 20-21, 줄 100-128)

**Hexagonal Architecture**는 Alistair Cockburn이 제안한 개념으로 Clean Architecture 원칙을 구체적 형태로 구현한다. 애플리케이션 코어를 육각형(이름의 유래지만 의미 없음)으로 표현하며, 외부 의존성 없이 모든 의존성이 중심을 향한다. 코어 외부에는 다양한 어댑터(web, external systems, database)가 있으며, 좌측 어댑터는 애플리케이션을 구동(driving)하고 우측 어댑터는 애플리케이션에 의해 구동(driven)된다. 애플리케이션 코어는 특정 포트를 제공하며, driving adapter의 포트는 코어의 use case가 구현하는 interface이고, driven adapter의 포트는 어댑터가 구현하는 interface다. "Ports and Adapters" 아키텍처라고도 불린다. (페이지 22-24, 줄 152-192)

### 핵심 개념 간 관계

**SRP**는 변경 이유의 최소화를 목표로 하며, **DIP**는 이를 달성하는 기술적 수단이다. DIP를 적용하여 domain 계층으로의 의존성 방향을 역전시키면 domain 코드의 변경 이유가 줄어든다.

**Clean Architecture**는 SRP와 DIP를 전체 아키텍처 수준에서 적용한 추상적 개념이며, **Hexagonal Architecture**는 이를 포트와 어댑터라는 구체적 구조로 실현한다. 두 아키텍처 모두 도메인 코드를 중심에 두고 외부 의존성을 제거하며, 각 계층에서 별도의 엔티티 모델을 유지하여 프레임워크 특정 문제로부터 도메인을 분리한다.

DIP를 통한 의존성 역전은 Clean/Hexagonal Architecture의 핵심 기능이며, persistence 계층과 domain 계층 간 분리를 가능하게 한다. 이는 도메인 코드가 프레임워크나 UI/persistence 문제를 고려하지 않고 비즈니스 규칙에 집중할 수 있도록 하며, 유지보수성을 향상시킨다.

## 상세 핵심 내용

### 중요 개념

- **Single Responsibility Principle (SRP)**
- **Dependency Inversion Principle (DIP)**
- **Clean Architecture**
- **Hexagonal Architecture (Ports and Adapters)**
- **변경의 이유 (Reason to Change)**
- **의존성 전파 (Dependency Propagation)**
- **Dependency Rule**
- **Use Cases (Fine-grained Services)**
- **Driving vs. Driven Adapters**
- **Ports**
- **계층 간 엔티티 모델 분리**
- **Domain-Driven Design (DDD) 자유도**

### 중요 개념 설명

**Single Responsibility Principle (SRP)**의 일반적 해석은 "한 가지만 하고 올바르게 하라"이지만, 실제 정의는 "변경의 이유가 하나만 있어야 한다"이다. "책임(responsibility)"은 "변경의 이유(reason to change)"로 번역되어야 하며, "Single Reason to Change Principle"로 이름 짓는 것이 더 적절하다. 한 가지만 할 수도 있지만, 더 중요한 부분은 변경의 이유가 하나만 있다는 것이다. (페이지 17, 줄 8-22)

**변경의 이유**는 아키텍처에서 중요한 의미를 갖는다. 컴포넌트가 변경의 이유가 하나만 있다면, 다른 이유로 소프트웨어를 변경할 때 이 컴포넌트를 전혀 걱정할 필요가 없으며 예상대로 작동할 것을 안다. 하지만 변경의 이유가 컴포넌트의 의존성을 통해 다른 컴포넌트로 전파되기 매우 쉽다. (페이지 17-18, 줄 23-27)

**의존성 전파**는 그림 6에서 보여주듯이 직접 또는 전이적 의존성(dashed arrows)을 통해 발생한다. 컴포넌트 E는 의존성이 전혀 없어 E의 기능이 변경될 때만 변경 이유가 있지만, 컴포넌트 A는 많은 다른 컴포넌트에 의존하여 그 컴포넌트들이 변경될 때 변경될 수 있다. 많은 코드베이스가 시간이 지남에 따라 변경하기 어렵고 비용이 많이 드는 이유는 SRP 위반 때문이며, 컴포넌트가 더 많은 변경 이유를 축적하고 한 컴포넌트 변경이 다른 컴포넌트를 실패하게 만든다. (페이지 18, 줄 34-43)

**SRP 위반 사례**: 10년 된 코드베이스를 인수한 프로젝트에서, 한 영역의 변경이 다른 영역에 부작용을 일으켰다. 중앙 컴포넌트의 작은 변경이 필요한 더 저렴하고 사용자 친화적인 솔루션을 제안했지만, 클라이언트는 과거 그 컴포넌트 변경이 항상 다른 것을 망가뜨렸기 때문에 부작용을 두려워하여 더 비싸고 불편한 솔루션을 선택했다. 이는 잘못 설계된 소프트웨어 수정에 클라이언트가 추가 비용을 지불하도록 훈련시킨 사례다. (페이지 18, 줄 44-61)

**Dependency Inversion Principle (DIP)**는 이름이 의미하는 그대로 코드베이스 내 모든 의존성의 방향을 역전(invert)시킬 수 있다는 원칙이다(단, 의존성 양쪽 코드를 제어할 때만 가능하며, 서드파티 라이브러리 의존성은 역전할 수 없다). 계층형 아키텍처에서 교차 계층 의존성은 항상 아래로 향하며, 상위 계층이 하위 계층보다 더 많은 변경 이유를 가진다. Domain 계층이 persistence 계층에 의존하므로 persistence의 변경이 domain 변경을 요구할 수 있지만, domain 코드는 애플리케이션에서 가장 중요하므로 persistence 변경 시 변경되어서는 안 된다. (페이지 19, 줄 66-74)

**DIP 적용 과정**: 1장 그림 2의 구조에서 시작하여, domain 계층의 service가 persistence 계층의 엔티티와 repository를 사용한다. 먼저 엔티티를 domain 계층으로 올리는데(도메인 객체를 표현하고 domain 코드가 이 엔티티의 상태 변경을 중심으로 하기 때문), 이는 양 계층 간 순환 의존성을 만든다. DIP를 적용하여 domain 계층에 repository interface를 생성하고 persistence 계층의 실제 repository가 이를 구현하도록 하면, 의존성이 역전되어 persistence 계층이 domain 계층에 의존하게 된다(그림 7). 이를 통해 도메인 로직을 persistence 코드에 대한 억압적인 의존성으로부터 해방시킨다. (페이지 19-20, 줄 75-99)

**Clean Architecture**는 Robert C. Martin의 동명 책에서 정립한 개념으로, 비즈니스 규칙이 설계상 테스트 가능하고 프레임워크, 데이터베이스, UI 기술, 외부 애플리케이션/인터페이스로부터 독립적인 아키텍처다. 도메인 코드는 외부 지향 의존성(outward facing dependencies)을 가져서는 안 되며, DIP를 통해 모든 의존성이 도메인 코드를 향하도록 한다. (페이지 20-21, 줄 100-106)

**Clean Architecture 구조**: 그림 8에서 보여주듯이 계층이 동심원으로 감싸져 있으며, 주요 규칙인 **Dependency Rule**은 계층 간 모든 의존성이 내부를 향해야 한다고 명시한다. 핵심에는 주변 use case가 접근하는 도메인 엔티티가 있다. Use case는 이전에 service라 불렀던 것이지만, single responsibility(즉, 변경의 이유가 하나)를 갖도록 더 세분화되어 broad service 문제를 해결한다. 이 핵심 주변에는 비즈니스 규칙을 지원하는 애플리케이션의 다른 컴포넌트(persistence 제공, UI 제공, 서드파티 어댑터)가 있다. (페이지 21, 줄 107-123)

**Domain-Driven Design (DDD) 자유도**: Domain 코드가 어떤 persistence나 UI 프레임워크를 사용하는지 모르므로, 그 프레임워크에 특정한 코드를 포함할 수 없고 비즈니스 규칙에 집중한다. 도메인 코드를 모델링할 모든 자유가 있으며, 예를 들어 가장 순수한 형태의 DDD를 적용할 수 있다. Persistence나 UI 특정 문제를 고려하지 않아도 되므로 훨씬 쉽다. (페이지 21, 줄 124-128)

**계층 간 엔티티 모델 분리**: Clean Architecture는 비용이 든다. Domain 계층이 persistence, UI 같은 외부 계층으로부터 완전히 분리되므로, 각 계층에서 애플리케이션 엔티티의 모델을 유지해야 한다. ORM 프레임워크는 데이터베이스 구조와 객체 필드-데이터베이스 컬럼 매핑을 설명하는 메타데이터를 포함하는 특정 엔티티 클래스를 기대한다. Domain 계층이 persistence 계층을 모르므로, 동일한 엔티티 클래스를 사용할 수 없어 양쪽 계층에 생성해야 하며, domain 계층이 persistence 계층과 데이터를 주고받을 때 양쪽 표현 간 변환(translation)이 필요하다. Domain 계층과 다른 외부 계층 간에도 동일한 변환이 적용된다. (페이지 22, 줄 129-142)

하지만 이는 좋은 것이다! 이 분리(decoupling)가 바로 domain 코드를 프레임워크 특정 문제로부터 해방시키기 위해 달성하려던 것이다. 예를 들어 Java Persistence API(Java 세계의 표준 ORM-API)는 ORM 관리 엔티티가 인자 없는 기본 생성자를 가져야 하는데, domain model에서는 이를 피하고 싶을 수 있다. 8장 "Mapping Between Boundaries"에서 domain과 persistence 계층 간 결합을 수용하는 "no-mapping" 전략을 포함한 다양한 매핑 전략을 다룬다. (페이지 22, 줄 143-148)

**Hexagonal Architecture**는 Alistair Cockburn이 제안한 개념으로 상당 기간 존재했으며, Robert C. Martin이 Clean Architecture에서 더 일반적 용어로 설명한 것과 동일한 원칙을 적용한다. 애플리케이션 코어가 육각형으로 표현되어 이름이 붙었지만, 육각형 모양은 의미가 없어 팔각형을 그려 "Octagonal Architecture"라 불러도 된다. 전설에 따르면, 애플리케이션이 다른 시스템이나 어댑터에 연결되는 4개 이상의 면을 가질 수 있음을 보여주기 위해 일반적인 직사각형 대신 육각형이 사용되었다. (페이지 22-23, 줄 152-168)

**Hexagonal Architecture 구조**: 육각형 내부에는 도메인 엔티티와 그것을 사용하는 use case가 있다. 육각형은 외부 의존성이 없어 Martin의 Clean Architecture의 Dependency Rule이 적용되며, 모든 의존성이 중심을 향한다. 육각형 외부에는 애플리케이션과 상호작용하는 다양한 어댑터(web browser와 상호작용하는 web adapter, 외부 시스템과 상호작용하는 adapter, 데이터베이스와 상호작용하는 adapter)가 있다. (페이지 23, 줄 169-174)

**Driving vs. Driven Adapters**: 좌측 어댑터는 애플리케이션을 구동(drive)하는 어댑터(애플리케이션 코어를 호출하기 때문)이고, 우측 어댑터는 애플리케이션에 의해 구동(driven)되는 어댑터(애플리케이션 코어에 의해 호출되기 때문)다. (페이지 23, 줄 175-177)

**Ports**: 애플리케이션 코어와 어댑터 간 통신을 위해 애플리케이션 코어는 특정 포트를 제공한다. Driving adapter의 포트는 코어의 use case 클래스 중 하나가 구현하고 어댑터가 호출하는 interface다. Driven adapter의 포트는 어댑터가 구현하고 코어가 호출하는 interface다. 이 중심 개념 때문에 "Ports and Adapters" 아키텍처라고도 불린다. (페이지 23, 줄 178-183)

**Hexagonal Architecture의 계층 구조**: Clean Architecture처럼 Hexagonal Architecture도 계층으로 구성할 수 있다. 최외부 계층은 애플리케이션과 다른 시스템 간 변환을 하는 어댑터로 구성된다. 다음으로 포트와 use case 구현을 결합하여 애플리케이션 계층(application layer)을 형성하는데, 이들이 애플리케이션의 인터페이스를 정의하기 때문이다. 마지막 계층은 도메인 엔티티를 포함한다. (페이지 23-24, 줄 184-192)

### 중요 개념 간 관계

**SRP**는 변경 이유의 최소화를 목표로 하며, 컴포넌트의 의존성이 각각 변경의 이유가 되므로 의존성 관리가 SRP 준수의 핵심이다. **의존성 전파**는 직접 및 전이적 의존성을 통해 변경 이유를 확산시켜 SRP 위반을 야기한다.

**DIP**는 SRP를 달성하는 기술적 수단으로, 의존성 방향을 역전시켜 domain 코드의 변경 이유를 줄인다. 계층형 아키텍처에서 상위 계층이 하위 계층보다 더 많은 변경 이유를 가지는 문제를 DIP로 해결하여 persistence 계층이 domain 계층에 의존하도록 만든다.

**Clean Architecture**는 SRP와 DIP를 전체 아키텍처 수준에서 적용한 추상적 개념이다. **Dependency Rule**은 모든 의존성이 내부를 향하도록 강제하며, 이는 DIP의 확장이다. **Use Cases**는 SRP를 준수하여 single responsibility를 가지도록 세분화되며, broad service 문제를 해결한다.

**Hexagonal Architecture**는 Clean Architecture 원칙을 **Ports and Adapters**라는 구체적 구조로 실현한다. **Driving/Driven Adapters**는 의존성 방향을 명확히 하며, driving adapter는 코어를 호출하고 driven adapter는 코어에 의해 호출된다. **Ports**는 DIP를 구현하는 구체적 메커니즘으로, interface를 통해 의존성을 역전시킨다.

**계층 간 엔티티 모델 분리**는 Clean/Hexagonal Architecture의 비용이지만, domain 코드를 프레임워크 특정 문제(ORM 메타데이터, 기본 생성자 등)로부터 해방시켜 **DDD 자유도**를 제공한다. 이 분리는 domain 코드가 비즈니스 규칙에 집중하도록 하며, persistence와 UI 코드는 각자의 문제에 최적화될 수 있다.

DIP를 통한 의존성 역전 → Dependency Rule 준수 → Use Cases의 SRP 준수 → Ports를 통한 Adapters 분리 → 계층 간 엔티티 모델 분리 → DDD 자유도 확보 → 유지보수성 향상이라는 연쇄적 관계를 형성한다.

## 상세 내용

### 1. 서론: 계층형 아키텍처의 대안 제시

이전 화제와의 관계: 1장에서 계층형 아키텍처의 문제점을 다루었으므로, 이 장에서는 대안적 접근 방식을 논의한다.

1장의 계층형 아키텍처 비판 후, 대안적 접근을 기대하는 것이 당연하다. 먼저 SOLID 원칙 중 두 가지를 논의한 후, 이를 적용하여 계층형 아키텍처의 문제를 해결하는 "Clean" 또는 "Hexagonal" 아키텍처를 생성한다. (페이지 17, 줄 3-7)

**참조**: 페이지 17, 줄 3-7

### 2. Single Responsibility Principle (SRP)

이전 화제와의 관계: 대안 아키텍처를 논의하기 전 기반이 되는 첫 번째 SOLID 원칙을 설명한다.

#### 2.1 일반적 오해

소프트웨어 개발 분야의 모든 사람이 Single Responsibility Principle (SRP)을 알거나 안다고 가정한다. 이 원칙의 일반적 해석은 "한 가지만 하고, 올바르게 하라(A component should do only one thing, and do it right)"다. 이는 좋은 조언이지만 SRP의 실제 의도는 아니다. (페이지 17, 줄 8-13)

"한 가지만 하라"는 single responsibility의 가장 명백한 해석이므로 SRP가 자주 이렇게 해석되는 것은 당연하다. SRP의 이름이 오해의 소지가 있다고 관찰할 수 있다. (페이지 17, 줄 14-16)

**참조**: 페이지 17, 줄 8-16

#### 2.2 실제 정의

SRP의 실제 정의는 "변경의 이유가 하나만 있어야 한다(A component should have only one reason to change)"이다. "책임(responsibility)"은 "한 가지만 하라" 대신 "변경의 이유(reason to change)"로 번역되어야 한다. "Single Reason to Change Principle"로 이름을 바꾸는 것이 좋을 것이다. (페이지 17, 줄 17-20)

컴포넌트가 변경의 이유가 하나만 있다면, 한 가지만 하게 될 수 있지만, 더 중요한 부분은 이 변경의 이유가 하나만 있다는 것이다. (페이지 17, 줄 21-22)

**참조**: 페이지 17, 줄 17-22

#### 2.3 아키텍처에 대한 의미

아키텍처에 이것이 무엇을 의미하는가? 컴포넌트가 변경의 이유가 하나만 있다면, 다른 이유로 소프트웨어를 변경할 때 이 컴포넌트를 전혀 걱정할 필요가 없으며, 예상대로 작동할 것을 알 수 있다. (페이지 17, 줄 23-25)

슬프게도, 변경의 이유가 컴포넌트의 의존성을 통해 다른 컴포넌트로 전파되기 매우 쉽다(그림 6 참조). (페이지 17-18, 줄 26-27)

**참조**: 페이지 17-18, 줄 23-27

#### 2.4 의존성과 변경의 이유

그림 6에서 컴포넌트 A는 많은 다른 컴포넌트에 의존하고(직접 또는 전이적으로) 컴포넌트 E는 의존성이 전혀 없다. 컴포넌트 E를 변경하는 유일한 이유는 E의 기능이 새로운 요구사항으로 인해 변경되어야 할 때다. 하지만 컴포넌트 A는 의존하는 다른 컴포넌트들이 변경될 때 변경되어야 할 수 있다. (페이지 18, 줄 34-40)

많은 코드베이스가 시간이 지남에 따라 변경하기 어렵고 - 따라서 더 비용이 많이 들어 - 이유는 SRP가 위반되기 때문이다. 시간이 지나면서 컴포넌트가 더 많은 변경 이유를 축적한다. 많은 변경 이유를 축적한 후, 한 컴포넌트를 변경하는 것이 다른 컴포넌트를 실패하게 만들 수 있다. (페이지 18, 줄 41-43)

**참조**: 페이지 18, 줄 34-43

#### 2.5 부작용에 대한 이야기 (A Tale about Side Effects)

이전 화제와의 관계: SRP 위반의 실제 사례를 구체적으로 보여준다.

저자의 팀이 다른 소프트웨어 회사가 구축한 10년 된 코드베이스를 인수한 프로젝트가 있었다. 클라이언트가 미래의 유지보수와 개발을 더 낫고 덜 비싸게 만들기 위해 개발팀을 교체하기로 결정했다. (페이지 18, 줄 44-47)

예상대로 코드가 실제로 무엇을 하는지 이해하기 쉽지 않았고, 코드베이스의 한 영역에서 한 변경이 다른 영역에 부작용을 일으키는 경우가 많았다. 하지만 철저한 테스트, 자동화 테스트 추가, 많은 리팩터링을 통해 관리했다. (페이지 18, 줄 48-50)

코드베이스를 성공적으로 유지하고 확장한 일정 시간 후, 클라이언트가 소프트웨어 사용자에게 매우 어색하게 보이는 방식으로 구현될 새 기능을 요청했다. 저자는 전체 변경이 더 적어 더 저렴하게 구현할 수 있는 더 사용자 친화적인 방식을 제안했다. 하지만 특정 매우 중앙의 컴포넌트에 작은 변경이 필요했다. (페이지 18, 줄 51-55)

클라이언트는 거절하고 더 어색하고 비싼 솔루션을 주문했다. 이유를 물었을 때, 과거에 이전 개발팀이 그 컴포넌트의 변경이 항상 다른 것을 망가뜨렸기 때문에 부작용을 두려워한다고 말했다. (페이지 18, 줄 56-58)

슬프게도, 이는 잘못 설계된 소프트웨어를 수정하는 데 클라이언트가 추가 비용을 지불하도록 훈련시킬 수 있는 방법의 예다. 다행히 대부분의 클라이언트는 이 게임에 동참하지 않으므로, 좋은 소프트웨어를 구축하려고 노력하자. (페이지 18, 줄 59-61)

**참조**: 페이지 18, 줄 44-61

### 3. Dependency Inversion Principle (DIP)

이전 화제와의 관계: SRP가 변경 이유 최소화의 목표라면, DIP는 이를 달성하는 기술적 수단이다.

#### 3.1 계층형 아키텍처의 의존성 문제

계층형 아키텍처에서 교차 계층 의존성은 항상 다음 계층으로 아래쪽을 향한다. 높은 수준에서 Single Responsibility Principle을 적용하면, 상위 계층이 하위 계층보다 더 많은 변경 이유를 가진다는 것을 알 수 있다. (페이지 19, 줄 66-69)

따라서 domain 계층의 persistence 계층에 대한 의존성 때문에, persistence 계층의 각 변경이 잠재적으로 domain 계층의 변경을 요구한다. 하지만 domain 코드는 애플리케이션에서 가장 중요한 코드다! Persistence 코드에서 무언가 변경될 때 이를 변경해야 하는 것을 원하지 않는다! (페이지 19, 줄 70-73)

그렇다면 어떻게 이 의존성을 제거할 수 있을까? Dependency Inversion Principle이 답을 제공한다. (페이지 19, 줄 74-75)

**참조**: 페이지 19, 줄 66-75

#### 3.2 DIP의 정의

SRP와 달리 Dependency Inversion Principle (DIP)은 이름이 시사하는 것을 의미한다: 코드베이스 내 모든 의존성의 방향을 역전(invert)시킬 수 있다. (페이지 19, 줄 76-77)

(주석: 실제로는 의존성 양쪽의 코드를 제어할 때만 의존성을 역전시킬 수 있다. 서드파티 라이브러리에 대한 의존성이 있다면, 그 라이브러리의 코드를 제어하지 못하므로 역전시킬 수 없다.) (페이지 19, 줄 89-90)

**참조**: 페이지 19, 줄 76-77, 89-90

#### 3.3 DIP 적용 과정

어떻게 작동하는가? Domain과 persistence 코드 간 의존성을 역전시켜 persistence 코드가 domain 코드에 의존하도록 하고, domain 코드의 변경 이유 수를 줄여보자. (페이지 19, 줄 78-80)

1장 "What's Wrong with Layers?"의 그림 2와 같은 구조에서 시작한다. Domain 계층에 persistence 계층의 엔티티와 repository를 사용하는 service가 있다. (페이지 19, 줄 81-82)

무엇보다도 먼저, 엔티티를 domain 계층으로 올리고 싶다. 왜냐하면 이들이 도메인 객체를 표현하고 domain 코드가 이 엔티티의 상태를 변경하는 것을 중심으로 돌아가기 때문이다. (페이지 19, 줄 83-84)

하지만 이제 persistence 계층의 repository가 엔티티에 의존하는데 엔티티가 이제 domain 계층에 있으므로 양 계층 간 순환 의존성(circular dependency)이 생긴다. 여기서 DIP를 적용한다. Domain 계층에 repository를 위한 interface를 생성하고 persistence 계층의 실제 repository가 이를 구현하도록 한다. 결과는 그림 7과 같다. (페이지 19-20, 줄 85-88)

**참조**: 페이지 19-20, 줄 78-90

#### 3.4 DIP의 효과

이 트릭으로 도메인 로직을 persistence 코드에 대한 억압적인 의존성으로부터 해방시켰다. 이것이 다음 섹션에서 논의할 두 아키텍처 스타일의 핵심 기능이다. (페이지 20, 줄 97-99)

**참조**: 페이지 20, 줄 97-99

### 4. Clean Architecture

이전 화제와의 관계: DIP 적용 방법을 설명한 후, 이를 전체 아키텍처 수준에서 적용한 Clean Architecture를 소개한다.

#### 4.1 Clean Architecture의 정의

Robert C. Martin은 동명의 책에서 "Clean Architecture"라는 용어를 확립했다. 그의 의견에 따르면 clean architecture에서 비즈니스 규칙은 설계상 테스트 가능하고 프레임워크, 데이터베이스, UI 기술 및 기타 외부 애플리케이션이나 인터페이스로부터 독립적이다. (페이지 20, 줄 100-103)

이는 도메인 코드가 외부 지향 의존성(outward facing dependencies)을 가져서는 안 된다는 것을 의미한다. 대신 Dependency Inversion Principle의 도움으로 모든 의존성이 도메인 코드를 향하도록 한다. (페이지 20-21, 줄 104-105)

그림 8은 이러한 아키텍처가 추상적 수준에서 어떻게 보일 수 있는지 보여준다. (페이지 21, 줄 106)

**참조**: 페이지 20-21, 줄 100-106

#### 4.2 Clean Architecture의 구조

이 아키텍처의 계층은 동심원으로 서로를 감싸고 있다. 이러한 아키텍처의 주요 규칙은 Dependency Rule로, 이 계층들 간 모든 의존성이 내부를 향해야 한다고 명시한다. (페이지 21, 줄 114-116)

아키텍처의 핵심에는 주변 use case가 접근하는 도메인 엔티티가 있다. Use case는 이전에 service라고 불렀던 것이지만, single responsibility(즉, 변경의 이유가 하나)를 갖도록 더 세분화(fine-grained)되어 앞서 논의한 broad service 문제를 피한다. (페이지 21, 줄 117-120)

이 핵심 주변에는 비즈니스 규칙을 지원하는 애플리케이션의 다른 모든 컴포넌트를 찾을 수 있다. 이 지원은 예를 들어 persistence 제공이나 사용자 인터페이스 제공을 의미할 수 있다. 또한 외부 계층은 다른 서드파티 컴포넌트에 대한 어댑터를 제공할 수 있다. (페이지 21, 줄 121-123)

**참조**: 페이지 21, 줄 114-123

#### 4.3 Domain 코드의 자유도

Domain 코드가 어떤 persistence나 UI 프레임워크를 사용하는지 모르므로, 그 프레임워크에 특정한 코드를 포함할 수 없고 비즈니스 규칙에 집중할 것이다. 도메인 코드를 모델링할 모든 자유가 있다. 예를 들어 가장 순수한 형태로 Domain-Driven Design (DDD)를 적용할 수 있다. Persistence나 UI 특정 문제를 고려하지 않아도 되므로 훨씬 쉽다. (페이지 21, 줄 124-128)

**참조**: 페이지 21, 줄 124-128

#### 4.4 Clean Architecture의 비용

예상할 수 있듯이, Clean Architecture는 비용이 든다. Domain 계층이 persistence와 UI 같은 외부 계층으로부터 완전히 분리되므로, 각 계층에서 애플리케이션 엔티티의 모델을 유지해야 한다. (페이지 21-22, 줄 129-131)

예를 들어, persistence 계층에서 ORM(Object-Relational Mapping) 프레임워크를 사용한다고 가정하자. ORM 프레임워크는 일반적으로 데이터베이스 구조와 객체 필드-데이터베이스 컬럼 매핑을 설명하는 메타데이터를 포함하는 특정 엔티티 클래스를 기대한다. Domain 계층이 persistence 계층을 모르므로, domain 계층에서 동일한 엔티티 클래스를 사용할 수 없어 양쪽 계층에 생성해야 한다. 이는 domain 계층이 persistence 계층과 데이터를 주고받을 때 양쪽 표현 간 변환(translation)을 해야 함을 의미한다. Domain 계층과 다른 외부 계층 간에도 동일한 변환이 적용된다. (페이지 22, 줄 136-142)

**참조**: 페이지 21-22, 줄 129-142

#### 4.5 분리의 가치

하지만 이는 좋은 것이다! 이 분리(decoupling)가 바로 domain 코드를 프레임워크 특정 문제로부터 해방시키기 위해 달성하려던 것이다. 예를 들어 Java Persistence API(Java 세계의 표준 ORM-API)는 ORM 관리 엔티티가 인자 없는 기본 생성자를 가져야 하는데, domain model에서는 이를 피하고 싶을 수 있다. 8장 "Mapping Between Boundaries"에서 domain과 persistence 계층 간 결합을 그냥 수용하는 "no-mapping" 전략을 포함한 다양한 매핑 전략을 다룰 것이다. (페이지 22, 줄 143-148)

Robert C. Martin의 Clean Architecture가 다소 추상적이므로, 한 단계 더 자세히 들어가 clean architecture 원칙에 더 구체적인 형태를 제공하는 "Hexagonal Architecture"를 보자. (페이지 22, 줄 149-151)

**참조**: 페이지 22, 줄 143-151

### 5. Hexagonal Architecture

이전 화제와의 관계: Clean Architecture가 추상적 개념이라면, Hexagonal Architecture는 이를 구체적 구조로 구현한 것이다.

#### 5.1 Hexagonal Architecture의 기원

"Hexagonal Architecture"라는 용어는 Alistair Cockburn에서 유래했으며 상당 기간 존재했다. Robert C. Martin이 Clean Architecture에서 더 일반적 용어로 설명한 것과 동일한 원칙을 적용한다. (페이지 22-23, 줄 152-155)

(주석: "Hexagonal Architecture"라는 용어의 주요 출처는 Alistair Cockburn의 웹사이트 https://alistair.cockburn.us/hexagonal-architecture/의 글인 것 같다.) (페이지 23, 줄 156-157)

**참조**: 페이지 22-23, 줄 152-157

#### 5.2 Hexagonal Architecture의 구조

그림 9는 hexagonal architecture가 어떻게 보일 수 있는지 보여준다. 애플리케이션 코어는 육각형으로 표현되어 이 아키텍처 스타일에 이름을 준다. 육각형 모양은 의미가 없으므로, 팔각형을 그려 "Octagonal Architecture"라고 불러도 된다. 전설에 따르면, 육각형은 애플리케이션이 다른 시스템이나 어댑터에 연결되는 4개 이상의 면을 가질 수 있음을 보여주기 위해 일반적인 직사각형 대신 사용되었다. (페이지 23, 줄 164-168)

육각형 내부에는 도메인 엔티티와 그것을 사용하는 use case를 찾을 수 있다. 육각형은 외부 의존성이 없어 Martin의 Clean Architecture의 Dependency Rule이 적용된다. 대신 모든 의존성이 중심을 향한다. (페이지 23, 줄 169-171)

육각형 외부에는 애플리케이션과 상호작용하는 다양한 어댑터를 찾을 수 있다. Web browser와 상호작용하는 web adapter, 외부 시스템과 상호작용하는 어댑터들, 데이터베이스와 상호작용하는 어댑터가 있을 수 있다. (페이지 23, 줄 172-174)

**참조**: 페이지 23, 줄 164-174

#### 5.3 Driving vs. Driven Adapters

좌측의 어댑터는 애플리케이션을 구동(drive)하는 어댑터다(애플리케이션 코어를 호출하기 때문). 우측의 어댑터는 애플리케이션에 의해 구동(driven)되는 어댑터다(애플리케이션 코어에 의해 호출되기 때문). (페이지 23, 줄 175-177)

**참조**: 페이지 23, 줄 175-177

#### 5.4 Ports

애플리케이션 코어와 어댑터 간 통신을 허용하기 위해, 애플리케이션 코어는 특정 포트를 제공한다. Driving adapter의 경우, 그러한 포트는 코어의 use case 클래스 중 하나가 구현하고 어댑터가 호출하는 interface일 수 있다. Driven adapter의 경우, 어댑터가 구현하고 코어가 호출하는 interface일 수 있다. (페이지 23, 줄 178-181)

이 중심 개념 때문에 이 아키텍처 스타일은 "Ports and Adapters" 아키텍처라고도 알려져 있다. (페이지 23, 줄 182-183)

**참조**: 페이지 23, 줄 178-183

#### 5.5 Hexagonal Architecture의 계층화

Clean Architecture처럼, 이 Hexagonal Architecture를 계층으로 구성할 수 있다. 최외부 계층은 애플리케이션과 다른 시스템 간 변환을 하는 어댑터로 구성된다. 다음으로 포트와 use case 구현을 결합하여 애플리케이션 계층(application layer)을 형성할 수 있는데, 이들이 애플리케이션의 인터페이스를 정의하기 때문이다. 마지막 계층은 도메인 엔티티를 포함한다. (페이지 23-24, 줄 184-191)

다음 장에서 이러한 아키텍처를 코드로 구성하는 방법을 논의할 것이다. (페이지 24, 줄 192)

**참조**: 페이지 23-24, 줄 184-192

### 6. 결론: 유지보수 가능한 소프트웨어 구축에 어떻게 도움이 되는가?

이전 화제와의 관계: SRP, DIP, Clean Architecture, Hexagonal Architecture의 논의를 종합하여 유지보수성 향상이라는 최종 목표와 연결한다.

Clean Architecture, Hexagonal Architecture 또는 Ports and Adapters Architecture라고 부르든 - 도메인 코드가 외부에 대한 의존성을 갖지 않도록 의존성을 역전시킴으로써, 도메인 로직을 모든 persistence와 UI 특정 문제로부터 분리하고 코드베이스 전체에서 변경 이유의 수를 줄일 수 있다. 그리고 변경 이유가 적다는 것은 더 나은 유지보수성을 의미한다. (페이지 24, 줄 193-198)

Domain 코드는 비즈니스 문제에 가장 적합하게 모델링될 자유가 있고, persistence와 UI 코드는 persistence와 UI 문제에 가장 적합하게 모델링될 자유가 있다. (페이지 24, 줄 199-200)

이 책의 나머지 부분에서 Hexagonal architecture 스타일을 웹 애플리케이션에 적용할 것이다. 애플리케이션의 패키지 구조를 생성하고 dependency injection의 역할을 논의하는 것부터 시작할 것이다. (페이지 24, 줄 201-202)

**참조**: 페이지 24, 줄 193-202
