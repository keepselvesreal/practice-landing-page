# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter5: Implementing a Web Adapter

## 압축 내용

웹 어댑터는 의존성 역전 원칙을 활용하여 HTTP 요청을 애플리케이션 코어의 유스케이스 호출로 변환하고, HTTP 관련 책임(요청/응답 매핑, 인증/인가, 입력 검증)을 애플리케이션 계층과 분리하며, 컨트롤러를 유스케이스별로 세분화하여 유지보수성과 병렬 작업을 개선한다.

## 핵심 내용

### 핵심 개념들
- **의존성 역전 원칙(Dependency Inversion Principle)** → 상세 내용: 의존성 역전 섹션
- **웹 어댑터의 책임(Web Adapter Responsibilities)** → 상세 내용: 웹 어댑터의 책임 섹션
- **컨트롤러 슬라이싱(Controller Slicing)** → 상세 내용: 컨트롤러 슬라이싱 섹션

### 핵심 개념 설명

**의존성 역전 원칙** (참조: 페이지 45-47, 라인 8-47)
- 웹 어댑터는 incoming(driving) 어댑터로서 외부 요청을 애플리케이션 코어로 전달
- 포트(port) 인터페이스를 통해 애플리케이션 서비스와 통신하여 외부와의 상호작용 지점을 명확히 정의
- 양방향 통신이 필요한 경우(예: 웹소켓) outgoing 포트를 사용하여 의존성 방향 유지
- 관계: **웹 어댑터의 책임**을 수행하기 위한 아키텍처 원칙

**웹 어댑터의 책임** (참조: 페이지 47-48, 라인 48-91)
- 7가지 핵심 책임: HTTP 요청 매핑, 인증/인가, 입력 검증, 유스케이스 입력 모델 변환, 유스케이스 호출, 출력 HTTP 매핑, HTTP 응답 반환
- HTTP 관련 세부사항은 애플리케이션 계층으로 누출되지 않아야 함
- 도메인 계층과 애플리케이션 계층부터 개발 시작 시 자연스러운 경계 형성
- 관계: **의존성 역전 원칙**을 구현하며, **컨트롤러 슬라이싱**으로 구체화됨

**컨트롤러 슬라이싱** (참조: 페이지 48-51, 라인 92-277)
- 단일 큰 컨트롤러보다 유스케이스별 작은 컨트롤러 선호
- 각 컨트롤러는 전용 모델을 사용하여 불필요한 데이터 구조 공유 방지
- 유스케이스를 반영한 명확한 네이밍(예: CreateAccount 대신 RegisterAccount)
- 병렬 작업 용이 및 머지 충돌 감소
- 관계: **웹 어댑터의 책임**을 실제 코드로 구현하는 방법론

### 핵심 개념 간 관계

**의존성 역전 원칙**은 웹 어댑터 아키텍처의 기반이 되며, 이를 통해 **웹 어댑터의 책임**이 명확하게 정의됩니다. 이러한 책임들은 **컨트롤러 슬라이싱** 기법을 통해 실제 구현으로 구체화되며, 세 개념이 함께 작동하여 유지보수 가능하고 테스트 가능한 웹 계층을 구성합니다.

## 상세 내용

### 목차
1. [의존성 역전](#1-의존성-역전)
2. [웹 어댑터의 책임](#2-웹-어댑터의-책임)
3. [컨트롤러 슬라이싱](#3-컨트롤러-슬라이싱)
4. [유지보수 가능한 소프트웨어 구축 방법](#4-유지보수-가능한-소프트웨어-구축-방법)

---

### 1. 의존성 역전
(참조: 페이지 45-47, 라인 8-47)
→ 핵심 개념: **의존성 역전 원칙**

#### 웹 어댑터의 역할과 제어 흐름

오늘날 대부분의 애플리케이션은 웹 브라우저를 통한 UI 또는 다른 시스템이 호출할 수 있는 HTTP API 형태의 웹 인터페이스를 가집니다. 대상 아키텍처에서 외부 세계와의 모든 통신은 어댑터를 통해 이루어집니다.

웹 어댑터는 "driving" 또는 "incoming" 어댑터입니다. 외부에서 요청을 받아 애플리케이션 코어를 호출하는 형태로 변환하여 무엇을 할지 지시합니다. 제어 흐름은 웹 어댑터의 컨트롤러에서 애플리케이션 계층의 서비스로 진행됩니다.

애플리케이션 계층은 웹 어댑터가 통신할 수 있는 특정 포트를 제공합니다. 서비스가 이러한 포트를 구현하고, 웹 어댑터는 이러한 포트를 호출할 수 있습니다.

#### 포트의 필요성

제어 흐름이 왼쪽에서 오른쪽으로 진행되므로, 웹 어댑터가 유스케이스를 직접 호출하도록 할 수도 있습니다. 그렇다면 왜 어댑터와 유스케이스 사이에 또 다른 간접 계층을 추가할까요?

포트는 외부 세계가 애플리케이션 코어와 상호작용할 수 있는 지점의 명세입니다. 포트가 있으면 외부 세계와 어떤 통신이 발생하는지 정확히 알 수 있으며, 이는 레거시 코드베이스를 유지보수하는 엔지니어에게 귀중한 정보입니다.

11장 "의식적으로 지름길 택하기"에서는 incoming 포트를 생략하고 애플리케이션 서비스를 직접 호출하는 것을 하나의 지름길로 다룹니다.

#### 양방향 어댑터: 웹소켓 시나리오
(참조: 페이지 46-47, 라인 33-47)

고도로 상호작용적인 애플리케이션의 경우를 상상해봅시다. 웹소켓을 통해 사용자의 브라우저로 실시간 데이터를 전송하는 애플리케이션이 있다면, 애플리케이션 코어가 이 실시간 데이터를 웹 어댑터로 보내고, 웹 어댑터가 다시 사용자의 브라우저로 보내는 방법은 무엇일까요?

이 시나리오에서는 반드시 포트가 필요합니다. 이 포트는 웹 어댑터에 의해 구현되고 애플리케이션 코어에 의해 호출되어야 합니다.

기술적으로 이것은 outgoing 포트가 되며, 웹 어댑터를 incoming 및 outgoing 어댑터로 만듭니다. 하지만 동일한 어댑터가 동시에 둘 다일 수 없는 이유는 없습니다.

이 장의 나머지 부분에서는 가장 일반적인 경우이므로 웹 어댑터가 incoming 어댑터만 된다고 가정합니다.

---

### 2. 웹 어댑터의 책임
(참조: 페이지 47-48, 라인 48-91)
→ 핵심 개념: **웹 어댑터의 책임**
→ 이전 화제와의 관계: **의존성 역전**에서 정의한 웹 어댑터의 아키텍처적 역할을 구체적인 책임 목록으로 상세화

#### 웹 어댑터의 7가지 책임

BuckPal 애플리케이션에 REST API를 제공한다고 가정할 때, 웹 어댑터의 책임은 어디서 시작하고 어디서 끝날까요?

웹 어댑터는 일반적으로 다음 작업을 수행합니다:

1. **HTTP 요청을 Java 객체로 매핑**
2. **인가 검사 수행**
3. **입력 검증**
4. **입력을 유스케이스의 입력 모델로 매핑**
5. **유스케이스 호출**
6. **유스케이스의 출력을 HTTP로 다시 매핑**
7. **HTTP 응답 반환**

#### 각 책임의 상세 설명

**1. HTTP 요청 매핑**
웹 어댑터는 특정 URL 경로, HTTP 메서드, 콘텐츠 타입과 같은 특정 기준과 일치하는 HTTP 요청을 수신해야 합니다. 일치하는 HTTP 요청의 매개변수와 콘텐츠는 작업할 수 있는 객체로 역직렬화되어야 합니다.

**2-3. 인증/인가 및 입력 검증**
일반적으로 웹 어댑터는 인증 및 인가 검사를 수행하고 실패하면 오류를 반환합니다.

들어오는 객체의 상태를 검증할 수 있습니다. 유스케이스의 입력 모델에 대한 입력 검증을 이미 논의하지 않았나요? 그렇습니다. 유스케이스의 입력 모델은 유스케이스의 맥락에서 유효한 입력만 허용해야 합니다. 하지만 여기서는 웹 어댑터의 입력 모델에 대해 이야기하고 있습니다. 이것은 유스케이스의 입력 모델과 완전히 다른 구조와 의미를 가질 수 있으므로 다른 검증을 수행해야 할 수 있습니다.

유스케이스의 입력 모델에서 이미 수행한 것과 동일한 검증을 웹 어댑터에서 구현하는 것을 지지하지 않습니다. 대신, 웹 어댑터의 입력 모델을 유스케이스의 입력 모델로 변환할 수 있는지 검증해야 합니다. 이 변환을 방해하는 모든 것이 검증 오류입니다.

**4-5. 유스케이스 입력 모델 변환 및 호출**
변환된 입력 모델로 특정 유스케이스를 호출합니다.

**6-7. 출력 매핑 및 응답 반환**
어댑터는 유스케이스의 출력을 받아 호출자에게 다시 보내지는 HTTP 응답으로 직렬화합니다.

도중에 무언가 잘못되어 예외가 발생하면, 웹 어댑터는 오류를 호출자에게 다시 보내지는 메시지로 변환해야 합니다.

#### HTTP와 애플리케이션 계층의 분리
(참조: 페이지 48, 라인 78-91)

웹 어댑터에 많은 책임이 있지만, 애플리케이션 계층이 걱정하지 말아야 할 책임이기도 합니다. HTTP와 관련된 모든 것은 애플리케이션 계층으로 누출되어서는 안 됩니다. 애플리케이션 코어가 외부에서 HTTP를 다루고 있다는 것을 알면, 본질적으로 HTTP를 사용하지 않는 다른 incoming 어댑터에서 동일한 도메인 로직을 수행할 수 있는 옵션을 잃게 됩니다. 좋은 아키텍처에서는 옵션을 열어두고 싶습니다.

이 웹 어댑터와 애플리케이션 계층 사이의 경계는 웹 계층 대신 도메인 및 애플리케이션 계층부터 개발을 시작하면 자연스럽게 형성됩니다. 특정 incoming 어댑터를 생각하지 않고 유스케이스를 먼저 구현하면 경계를 흐리려는 유혹을 받지 않습니다.

---

### 3. 컨트롤러 슬라이싱
(참조: 페이지 48-51, 라인 92-268)
→ 핵심 개념: **컨트롤러 슬라이싱**
→ 이전 화제와의 관계: **웹 어댑터의 책임**을 실제 코드로 구현할 때의 구조화 방법론

#### 컨트롤러 구조 설계

Java의 Spring MVC와 같은 대부분의 웹 프레임워크에서는 위에서 논의한 책임을 수행하는 컨트롤러 클래스를 만듭니다. 애플리케이션으로 향하는 모든 요청에 응답하는 단일 컨트롤러를 구축해야 할까요? 그럴 필요는 없습니다. 웹 어댑터는 확실히 하나 이상의 클래스로 구성될 수 있습니다.

그러나 3장 "코드 구성"에서 논의한 것처럼 이러한 클래스들을 동일한 패키지 계층 구조에 배치하여 함께 속한다는 것을 표시해야 합니다.

얼마나 많은 컨트롤러를 구축해야 할까요? 너무 적은 것보다 너무 많은 것을 구축해야 한다고 말합니다. 각 컨트롤러가 가능한 한 좁은 웹 어댑터의 슬라이스를 구현하고 다른 컨트롤러와 가능한 한 적게 공유하도록 해야 합니다.

#### 안티 패턴: 단일 거대 컨트롤러
(참조: 페이지 48-50, 라인 102-206)

BuckPal 애플리케이션 내의 계정 엔티티에 대한 작업을 예로 들어봅시다. 인기 있는 접근 방식은 계정과 관련된 모든 작업에 대한 요청을 수락하는 단일 AccountController를 만드는 것입니다.

REST API를 제공하는 Spring 컨트롤러는 다음 코드 스니펫과 같을 수 있습니다:

```java
// 참조: 페이지 48-50, 라인 105-182
package buckpal.adapter.web;

@RestController
@RequiredArgsConstructor
class AccountController {

    // 여러 유스케이스를 위한 의존성들
    private final GetAccountBalanceQuery getAccountBalanceQuery;
    private final ListAccountsQuery listAccountsQuery;
    private final LoadAccountQuery loadAccountQuery;

    private final SendMoneyUseCase sendMoneyUseCase;
    private final CreateAccountUseCase createAccountUseCase;

    // 계정 목록 조회
    @GetMapping("/accounts")
    List<AccountResource> listAccounts(){
        // 구현...
    }

    // 특정 계정 조회
    @GetMapping("/accounts/id")
    AccountResource getAccount(@PathVariable("accountId") Long accountId){
        // 구현...
    }

    // 계정 잔액 조회
    @GetMapping("/accounts/{id}/balance")
    long getAccountBalance(@PathVariable("accountId") Long accountId){
        // 구현...
    }

    // 계정 생성
    @PostMapping("/accounts")
    AccountResource createAccount(@RequestBody AccountResource account){
        // 구현...
    }

    // 송금 실행
    @PostMapping("/accounts/send/{sourceAccountId}/{targetAccountId}/{amount}")
    void sendMoney(
        @PathVariable("sourceAccountId") Long sourceAccountId,
        @PathVariable("targetAccountId") Long targetAccountId,
        @PathVariable("amount") Long amount) {
        // 구현...
    }
}
```

```python
# Python 버전 (Flask 예시)
from flask import Blueprint, request, jsonify

# 참조: 페이지 48-50, 라인 105-182
account_controller = Blueprint('account', __name__)

class AccountController:
    def __init__(self, get_balance_query, list_accounts_query,
                 load_account_query, send_money_use_case, create_account_use_case):
        # 여러 유스케이스를 위한 의존성들
        self.get_balance_query = get_balance_query
        self.list_accounts_query = list_accounts_query
        self.load_account_query = load_account_query
        self.send_money_use_case = send_money_use_case
        self.create_account_use_case = create_account_use_case

    # 계정 목록 조회
    @account_controller.route('/accounts', methods=['GET'])
    def list_accounts(self):
        # 구현...
        pass

    # 특정 계정 조회
    @account_controller.route('/accounts/<int:account_id>', methods=['GET'])
    def get_account(self, account_id):
        # 구현...
        pass

    # 계정 잔액 조회
    @account_controller.route('/accounts/<int:account_id>/balance', methods=['GET'])
    def get_account_balance(self, account_id):
        # 구현...
        pass

    # 계정 생성
    @account_controller.route('/accounts', methods=['POST'])
    def create_account(self):
        account = request.json
        # 구현...
        pass

    # 송금 실행
    @account_controller.route('/accounts/send/<int:source_id>/<int:target_id>/<int:amount>',
                             methods=['POST'])
    def send_money(self, source_id, target_id, amount):
        # 구현...
        pass
```

#### 단일 컨트롤러의 단점
(참조: 페이지 49-50, 라인 183-206)

계정 리소스에 관한 모든 것이 단일 클래스에 있어 좋게 느껴집니다. 하지만 이 접근 방식의 단점을 논의해봅시다.

**1. 코드 크기 문제**
클래스당 코드가 적은 것이 좋습니다. 30,000줄의 코드를 가진 가장 큰 클래스가 있는 레거시 프로젝트에서 일한 적이 있습니다. 그것은 재미가 없습니다. 컨트롤러가 수년에 걸쳐 200줄의 코드만 축적하더라도 50줄보다 파악하기 어렵습니다. 메서드로 깔끔하게 분리되어 있더라도 마찬가지입니다.

**2. 테스트 코드 복잡성**
동일한 논거가 테스트 코드에도 유효합니다. 컨트롤러 자체에 많은 코드가 있으면 테스트 코드도 많을 것입니다. 그리고 종종 테스트 코드는 프로덕션 코드보다 파악하기 더 어렵습니다. 더 추상적인 경향이 있기 때문입니다. 또한 특정 프로덕션 코드에 대한 테스트를 쉽게 찾을 수 있기를 원하며, 이는 작은 클래스에서 더 쉽습니다.

**3. 데이터 구조 재사용의 문제**
마찬가지로 중요한 것은, 모든 작업을 단일 컨트롤러 클래스에 넣으면 데이터 구조의 재사용을 장려한다는 것입니다. 위 코드 예제에서 많은 작업이 AccountResource 모델 클래스를 공유합니다. 이것은 모든 작업에 필요한 모든 것을 위한 버킷 역할을 합니다. AccountResource는 아마도 id 필드를 가질 것입니다. 이것은 생성 작업에서는 필요하지 않으며 여기서 혼란을 일으킬 것입니다.

Account가 User 객체와 일대다 관계를 가진다고 상상해보십시오. 책을 생성하거나 업데이트할 때 이러한 User 객체를 포함할까요? 사용자가 목록 작업에 의해 반환될까요? 이것은 쉬운 예이지만, 일반적인 크기 이상의 프로젝트에서는 어느 시점에서 이러한 질문을 할 것입니다.

#### 권장 패턴: 유스케이스별 컨트롤러
(참조: 페이지 50-51, 라인 207-268)

따라서 각 작업에 대해 별도의 컨트롤러를 만드는 접근 방식을 지지합니다. 잠재적으로 별도의 패키지에 있을 수 있습니다. 또한 유스케이스에 가능한 한 가깝게 메서드와 클래스의 이름을 지정해야 합니다:

```java
// 참조: 페이지 50, 라인 209-250
package buckpal.adapter.web;

@RestController
@RequiredArgsConstructor
public class SendMoneyController {

    // 단일 유스케이스만 의존
    private final SendMoneyUseCase sendMoneyUseCase;

    // 송금 작업만 처리
    @PostMapping(path = "/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}")
    void sendMoney(
        @PathVariable("sourceAccountId") Long sourceAccountId,
        @PathVariable("targetAccountId") Long targetAccountId,
        @PathVariable("amount") Long amount) {

        // 유스케이스 입력 모델 생성
        SendMoneyCommand command = new SendMoneyCommand(
            new AccountId(sourceAccountId),
            new AccountId(targetAccountId),
            Money.of(amount));

        // 유스케이스 호출
        sendMoneyUseCase.sendMoney(command);
    }
}
```

```python
# Python 버전 (Flask 예시)
from flask import Blueprint, request, jsonify

# 참조: 페이지 50, 라인 209-250
send_money_controller = Blueprint('send_money', __name__)

class SendMoneyController:
    def __init__(self, send_money_use_case):
        # 단일 유스케이스만 의존
        self.send_money_use_case = send_money_use_case

    # 송금 작업만 처리
    @send_money_controller.route('/accounts/sendMoney/<int:source_id>/<int:target_id>/<int:amount>',
                                 methods=['POST'])
    def send_money(self, source_id, target_id, amount):
        # 유스케이스 입력 모델 생성
        command = SendMoneyCommand(
            account_id=AccountId(source_id),
            target_account_id=AccountId(target_id),
            money=Money.of(amount)
        )

        # 유스케이스 호출
        self.send_money_use_case.send_money(command)

        return jsonify({"status": "success"}), 200
```

#### 세분화된 컨트롤러의 이점
(참조: 페이지 50-51, 라인 251-268)

**1. 전용 모델 사용**
각 컨트롤러는 CreateAccountResource 또는 UpdateAccountResource와 같은 자체 모델을 가질 수 있거나 위 예제처럼 프리미티브를 입력으로 사용할 수 있습니다. 이러한 특수 모델 클래스는 컨트롤러의 패키지에 private일 수도 있으므로 실수로 다른 곳에서 재사용되지 않을 수 있습니다.

컨트롤러는 여전히 모델을 공유할 수 있지만, 다른 패키지의 공유 클래스를 사용하면 더 많이 생각하게 되고 아마도 필드의 절반이 필요하지 않다는 것을 알게 되어 결국 우리 자신의 것을 만들게 됩니다.

**2. 명확한 네이밍**
컨트롤러와 서비스의 이름을 신중하게 생각해야 합니다. 예를 들어 CreateAccount 대신 RegisterAccount가 더 나은 이름이 아닐까요? BuckPal 애플리케이션에서 계정을 만드는 유일한 방법은 사용자가 등록하는 것입니다. 따라서 의미를 더 잘 전달하기 위해 클래스 이름에 "register"라는 단어를 사용합니다. 일반적인 용의자 Create..., Update..., Delete...가 유스케이스를 충분히 설명하는 경우도 있지만, 실제로 사용하기 전에 두 번 생각해야 할 수 있습니다.

**3. 병렬 작업 용이성**
이 슬라이싱 스타일의 또 다른 이점은 서로 다른 작업에 대한 병렬 작업을 쉽게 만든다는 것입니다. 두 개발자가 서로 다른 작업에 작업하면 머지 충돌이 발생하지 않습니다.

---

### 4. 유지보수 가능한 소프트웨어 구축 방법
(참조: 페이지 51, 라인 269-277)
→ 이전 화제와의 관계: 앞서 다룬 **의존성 역전**, **웹 어댑터의 책임**, **컨트롤러 슬라이싱** 개념들을 종합하여 실무 적용 원칙 제시

#### 핵심 원칙

**웹 어댑터의 본질 이해**
애플리케이션에 웹 어댑터를 구축할 때, HTTP를 애플리케이션의 유스케이스에 대한 메서드 호출로 변환하고 결과를 다시 HTTP로 변환하는 어댑터를 구축하고 있으며 도메인 로직을 수행하지 않는다는 것을 명심해야 합니다.

**계층 분리의 중요성**
반면에 애플리케이션 계층은 HTTP를 수행하지 말아야 하므로 HTTP 세부 사항이 누출되지 않도록 해야 합니다. 이렇게 하면 필요가 발생할 경우 웹 어댑터를 다른 어댑터로 교체할 수 있습니다.

**세분화된 컨트롤러의 가치**
웹 컨트롤러를 슬라이싱할 때 모델을 공유하지 않는 많은 작은 클래스를 구축하는 것을 두려워해서는 안 됩니다. 그것들은 파악하기 쉽고, 테스트하기 쉽고, 병렬 작업을 지원합니다. 이러한 세분화된 컨트롤러를 설정하는 데 처음에는 더 많은 작업이 필요하지만 유지보수 중에 그만한 가치가 있을 것입니다.
