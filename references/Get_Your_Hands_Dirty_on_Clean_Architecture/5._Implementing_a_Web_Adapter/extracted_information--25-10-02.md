# Get_Your_Hands_Dirty_on_Clean_Architecture Chapter 5: Implementing a Web Adapter

## 압축 내용
웹 어댑터는 HTTP 요청을 애플리케이션 코어의 유스케이스 호출로 변환하는 인커밍 어댑터로, 의존성 역전을 통해 애플리케이션 레이어와 분리되며, 좁은 책임 범위를 가진 여러 개의 작은 컨트롤러로 슬라이싱하여 구현해야 유지보수성이 향상된다.

## 핵심 내용
### 핵심 개념
1. Web Adapter (인커밍 어댑터)
2. Dependency Inversion (의존성 역전)
3. Incoming Port (인커밍 포트)
4. Controller Slicing (컨트롤러 슬라이싱)
5. Web Adapter Responsibilities (웹 어댑터 책임)

### 핵심 개념 설명

**1. Web Adapter (인커밍 어댑터)**
- 외부 HTTP 요청을 받아 애플리케이션 코어의 유스케이스 호출로 변환하는 드라이빙 어댑터
- 제어 흐름이 컨트롤러(웹 어댑터)에서 서비스(애플리케이션 레이어)로 진행됨
- 참조: 페이지 45, 라인 13-15

**2. Dependency Inversion (의존성 역전)**
- 웹 어댑터와 애플리케이션 레이어 사이에 포트 인터페이스를 두어 의존성 방향을 제어
- 포트는 외부 세계가 애플리케이션 코어와 상호작용할 수 있는 명세(specification)를 제공
- 참조: 페이지 45-46, 라인 18-28

**3. Incoming Port (인커밍 포트)**
- 애플리케이션 레이어가 제공하는 특정 포트를 통해 웹 어댑터가 통신
- 서비스가 이 포트를 구현하고 웹 어댑터가 포트를 호출
- 인터랙티브 앱의 경우 아웃고잉 포트도 필요할 수 있음 (웹소켓 등)
- 참조: 페이지 45-46, 라인 16-41

**4. Controller Slicing (컨트롤러 슬라이싱)**
- 단일 거대 컨트롤러 대신, 각 오퍼레이션마다 별도의 좁은 범위의 컨트롤러를 생성
- 각 컨트롤러는 자체 모델을 가지며, 불필요한 공유를 최소화
- 참조: 페이지 48-51, 라인 92-268

**5. Web Adapter Responsibilities (웹 어댑터 책임)**
- HTTP 요청을 Java/Python 객체로 매핑
- 인가(authorization) 체크 수행
- 입력 검증(validation)
- 유스케이스 입력 모델로 변환
- 유스케이스 호출
- 유스케이스 출력을 HTTP로 매핑
- HTTP 응답 반환
- 참조: 페이지 47, 라인 51-58

### 핵심 개념 간 관계

```
Web Adapter (Incoming Adapter)
    ↓ (통신)
Incoming Port (Interface)
    ↓ (구현)
Application Service (Use Case)
```

- **Dependency Inversion**을 통해 Web Adapter는 Incoming Port에만 의존하고, 구체적인 구현에는 의존하지 않음
- **Controller Slicing**은 Web Adapter의 구현 전략으로, 각 유스케이스마다 별도의 컨트롤러 생성
- **Web Adapter Responsibilities**는 각 컨트롤러가 수행해야 할 7단계 작업을 정의
- Incoming Port는 외부와의 명확한 경계를 제공하며, 이를 통해 HTTP 상세가 애플리케이션 레이어로 누출되지 않음

## 상세 핵심 내용
### 중요 개념
1. Web Adapter (인커밍 어댑터)
2. Dependency Inversion (의존성 역전)
3. Incoming Port (인커밍 포트)
4. Outgoing Port (아웃고잉 포트)
5. Web Adapter Responsibilities (웹 어댑터 책임)
6. Controller Slicing (컨트롤러 슬라이싱)
7. Single Controller Anti-pattern (단일 컨트롤러 안티패턴)
8. Model Sharing (모델 공유 문제)
9. Naming Convention (네이밍 컨벤션)
10. HTTP Boundary (HTTP 경계)

### 중요 개념 설명

**1. Web Adapter (인커밍 어댑터)**
- "Driving" 또는 "Incoming" 어댑터로 불림
- 외부 요청을 받아 애플리케이션 코어에게 무엇을 해야 할지 지시
- 제어 흐름: 웹 어댑터의 컨트롤러 → 애플리케이션 레이어의 서비스
- 참조: 페이지 45, 라인 13-15

**2. Dependency Inversion (의존성 역전)**
- 제어 흐름은 왼쪽(웹 어댑터)에서 오른쪽(유스케이스)으로 가지만, 포트 인터페이스를 통해 의존성 방향 제어
- 포트가 없으면 웹 어댑터가 유스케이스를 직접 호출할 수 있지만, 포트를 둠으로써 외부 세계와의 상호작용 지점을 명확히 정의
- 유지보수 엔지니어에게 귀중한 정보 제공
- 참조: 페이지 45-46, 라인 18-32

**3. Incoming Port (인커밍 포트)**
- 애플리케이션 레이어가 제공하는 특정 포트
- 서비스가 이 포트를 구현하고 웹 어댑터가 호출
- 외부 세계가 애플리케이션 코어와 상호작용할 수 있는 명세(specification)
- 참조: 페이지 45-46, 라인 16-32

**4. Outgoing Port (아웃고잉 포트)**
- 실시간 데이터를 웹소켓을 통해 브라우저로 전송하는 등, 애플리케이션이 웹 어댑터를 능동적으로 알려야 하는 경우 필요
- 웹 어댑터가 구현하고 애플리케이션 코어가 호출
- 동일한 어댑터가 인커밍과 아웃고잉 어댑터를 동시에 할 수 있음
- 참조: 페이지 46, 라인 33-41

**5. Web Adapter Responsibilities (웹 어댑터 책임)**
- 7단계 책임:
  1. HTTP 요청을 Java 객체로 매핑
  2. 인증/인가 체크 수행
  3. 입력 검증
  4. 유스케이스 입력 모델로 변환
  5. 유스케이스 호출
  6. 유스케이스 출력을 HTTP로 매핑
  7. HTTP 응답 반환
- 에러 발생 시 예외를 메시지로 변환하여 호출자에게 반환
- 참조: 페이지 47-48, 라인 51-77

**6. Controller Slicing (컨트롤러 슬라이싱)**
- 각 오퍼레이션마다 별도의 컨트롤러 생성 (가능한 한 많은 작은 컨트롤러)
- 각 컨트롤러는 가능한 한 좁은 웹 어댑터 슬라이스를 구현
- 다른 컨트롤러와 최소한의 공유
- 같은 패키지 계층에 배치하여 소속감 표현
- 참조: 페이지 48-51, 라인 92-268

**7. Single Controller Anti-pattern (단일 컨트롤러 안티패턴)**
- 모든 오퍼레이션을 단일 컨트롤러에 모으는 방식의 문제점:
  - 클래스당 코드 라인이 많아짐 (200라인도 50라인보다 이해하기 어려움)
  - 테스트 코드도 많아지고 복잡해짐
  - 데이터 구조 재사용 장려 (AccountResource 같은 버킷 클래스)
  - 병렬 작업 시 머지 충돌 발생
- 참조: 페이지 48-50, 라인 102-206

**8. Model Sharing (모델 공유 문제)**
- 여러 오퍼레이션이 AccountResource 같은 모델 클래스를 공유
- "모든 것을 담는 버킷" 역할을 하게 됨
- 예: create 오퍼레이션에는 id 필드가 필요 없는데 혼란 야기
- 일대다 관계(Account-User)에서 포함 여부 결정이 복잡해짐
- 참조: 페이지 49-50, 라인 192-206

**9. Naming Convention (네이밍 컨벤션)**
- 메서드와 클래스 이름을 유스케이스에 최대한 가깝게 작성
- 예: CreateAccount 대신 RegisterAccount (등록이라는 도메인 개념 반영)
- Create..., Update..., Delete... 같은 일반적인 이름보다 도메인 특화 이름 선호
- 참조: 페이지 50-51, 라인 257-266

**10. HTTP Boundary (HTTP 경계)**
- HTTP와 관련된 모든 것은 애플리케이션 레이어로 누출되어서는 안 됨
- 애플리케이션 코어가 HTTP를 알게 되면, HTTP를 사용하지 않는 다른 인커밍 어댑터로 동일한 도메인 로직을 수행할 수 없게 됨
- 좋은 아키텍처는 옵션을 열어둠
- 도메인과 애플리케이션 레이어를 먼저 개발하면 이 경계가 자연스럽게 생김
- 참조: 페이지 48, 라인 84-91

### 중요 개념 간 관계

```
외부 HTTP 요청
    ↓
Web Adapter (Controller)
    ├─ HTTP → Java/Python 객체 매핑
    ├─ 인증/인가 체크
    ├─ 입력 검증
    ├─ 유스케이스 입력 모델 변환
    ↓
Incoming Port (Interface)
    ↓
Application Service (Use Case 구현)
    ↓
도메인 로직 수행
    ↓
결과 반환
    ↓
Web Adapter
    ├─ 출력 → HTTP 변환
    └─ HTTP 응답 반환
```

**Controller Slicing 전략:**
- Single Controller (안티패턴): 모든 Account 오퍼레이션을 AccountController 하나에 모음
  - 문제: 코드 많음, 테스트 복잡, 모델 공유, 머지 충돌
- Multiple Narrow Controllers (권장): SendMoneyController, CreateAccountController 등
  - 장점: 코드 적음, 테스트 간단, 모델 독립, 병렬 작업 용이

**Dependency Inversion 효과:**
- Port 있음: Web Adapter → Incoming Port ← Application Service
  - 의존성 제어, 명확한 경계, 유지보수 정보 제공
- Port 없음: Web Adapter → Application Service (직접 호출)
  - 단순하지만 경계 불명확 (11장에서 다루는 shortcut)

**HTTP Boundary 유지:**
- HTTP 상세를 애플리케이션 레이어에서 완전히 격리
- 다른 인커밍 어댑터(CLI, 메시징 등)로 쉽게 교체 가능
- 도메인 로직의 재사용성 극대화

## 상세 내용

### 1. 의존성 역전 (Dependency Inversion)

**아키텍처 요소**
웹 어댑터와 관련된 아키텍처 요소들을 확대한 뷰를 제공한다. 웹 어댑터 자체와 애플리케이션 코어와 상호작용하는 포트들이 포함된다.
참조: 페이지 45, 라인 9-12

**인커밍 어댑터의 특성**
웹 어댑터는 "드라이빙(driving)" 또는 "인커밍(incoming)" 어댑터이다. 외부로부터 요청을 받아 애플리케이션 코어로 변환하여, 무엇을 해야 할지 지시한다. 제어 흐름은 웹 어댑터의 컨트롤러에서 애플리케이션 레이어의 서비스로 진행된다.
참조: 페이지 45, 라인 13-15

**포트를 통한 통신**
애플리케이션 레이어는 웹 어댑터가 통신할 수 있는 특정 포트를 제공한다. 서비스들이 이 포트를 구현하고, 웹 어댑터가 이 포트를 호출할 수 있다.
참조: 페이지 45, 라인 16-17

**의존성 역전 원리 적용**
자세히 보면, 이것이 바로 의존성 역전 원리(Dependency Inversion Principle)가 작동하는 모습이다. 제어 흐름이 왼쪽에서 오른쪽으로 가기 때문에, 웹 어댑터가 유스케이스를 직접 호출하도록 할 수도 있다.
참조: 페이지 45-46, 라인 18-20

**포트의 필요성**
그렇다면 왜 어댑터와 유스케이스 사이에 또 다른 간접 레이어를 추가하는가? 그 이유는 포트가 외부 세계가 애플리케이션 코어와 상호작용할 수 있는 지점들의 명세(specification)이기 때문이다. 포트가 있으면, 어떤 외부 세계와의 통신이 일어나는지 정확히 알 수 있으며, 이는 레거시 코드베이스를 작업하는 모든 유지보수 엔지니어에게 귀중한 정보이다.
참조: 페이지 46, 라인 26-30

**Shortcut 논의**
그렇긴 하지만, 11장 "의식적으로 지름길 택하기(Taking Shortcuts Consciously)"에서 논의할 지름길 중 하나는 인커밍 포트를 제거하고 애플리케이션 서비스를 직접 호출하는 것이다.
참조: 페이지 46, 라인 31-32

**아웃고잉 포트의 필요성**
그러나 한 가지 질문이 남는데, 이는 고도로 인터랙티브한 애플리케이션에 관련된 것이다. 웹소켓을 통해 실시간 데이터를 사용자 브라우저로 보내는 애플리케이션을 상상해보자. 애플리케이션 코어가 이 실시간 데이터를 웹 어댑터로 어떻게 보내고, 웹 어댑터는 다시 사용자 브라우저로 보낼까?

이 시나리오에서는 반드시 포트가 필요하다. 이 포트는 웹 어댑터가 구현해야 하고 애플리케이션 코어가 호출해야 한다.

기술적으로 말하면, 이는 아웃고잉 포트이며 웹 어댑터를 인커밍과 아웃고잉 어댑터로 만든다. 하지만 동일한 어댑터가 동시에 둘 다일 수 없다는 이유는 없다.
참조: 페이지 46, 라인 33-41

**본 장의 가정**
이 장의 나머지 부분에서는 웹 어댑터가 인커밍 어댑터만이라고 가정할 것이다. 이것이 가장 일반적인 경우이기 때문이다.
참조: 페이지 46-47, 라인 46-47

### 2. 웹 어댑터의 책임 (Responsibilities of a Web Adapter)

**책임의 범위**
웹 어댑터는 실제로 무엇을 하는가? BuckPal 애플리케이션을 위한 REST API를 제공한다고 하자. 웹 어댑터의 책임은 어디서 시작하고 어디서 끝나는가?
참조: 페이지 47, 라인 48-50

**웹 어댑터가 수행하는 7가지 작업**
웹 어댑터는 일반적으로 다음 작업들을 수행한다:

1. HTTP 요청을 Java 객체로 매핑
2. 인가(authorization) 체크 수행
3. 입력 검증(validation)
4. 유스케이스의 입력 모델로 입력 매핑
5. 유스케이스 호출
6. 유스케이스의 출력을 HTTP로 매핑
7. HTTP 응답 반환

참조: 페이지 47, 라인 51-58

**HTTP 요청 처리**
우선, 웹 어댑터는 특정 URL 경로, HTTP 메서드, 콘텐츠 타입 등의 기준과 일치하는 HTTP 요청을 수신해야 한다. 일치하는 HTTP 요청의 파라미터와 콘텐츠는 작업할 수 있는 객체로 역직렬화되어야 한다.
참조: 페이지 47, 라인 59-61

**인증과 인가**
일반적으로 웹 어댑터는 인증(authentication)과 인가(authorization) 체크를 수행하고, 실패하면 에러를 반환한다.
참조: 페이지 47, 라인 62-63

**입력 검증**
들어오는 객체의 상태는 검증될 수 있다. 하지만 유스케이스의 입력 모델의 책임으로 입력 검증을 이미 논의하지 않았나? 맞다. 유스케이스의 입력 모델은 유스케이스의 컨텍스트에서 유효한 입력만 허용해야 한다. 하지만 여기서는 웹 어댑터의 입력 모델에 대해 이야기하고 있다. 이것은 유스케이스의 입력 모델과 완전히 다른 구조와 의미를 가질 수 있으므로, 다른 검증을 수행해야 할 수도 있다.

웹 어댑터에서 유스케이스에서 이미 수행한 것과 동일한 검증을 구현하라고 주장하는 것은 아니다. 대신, 웹 어댑터의 입력 모델을 유스케이스의 입력 모델로 변환할 수 있는지 검증해야 한다. 이 변환을 방해하는 모든 것이 검증 에러이다.
참조: 페이지 47, 라인 64-72

**유스케이스 호출과 출력 변환**
이것이 웹 어댑터의 다음 책임으로 이어진다: 변환된 입력 모델로 특정 유스케이스를 호출한다. 그런 다음 어댑터는 유스케이스의 출력을 가져와 HTTP 응답으로 직렬화하여 호출자에게 다시 전송한다.
참조: 페이지 47, 라인 73-75

**에러 처리**
과정 중에 무언가 잘못되어 예외가 발생하면, 웹 어댑터는 에러를 호출자에게 다시 보낼 메시지로 변환해야 한다.
참조: 페이지 47, 라인 76-77

**책임의 의미**
웹 어댑터의 어깨에 많은 책임이 실려 있다. 하지만 이것들은 애플리케이션 레이어가 관심을 가져서는 안 되는 책임들이기도 하다. HTTP와 관련된 모든 것은 애플리케이션 레이어로 누출되어서는 안 된다. 애플리케이션 코어가 외부에서 HTTP를 다루고 있다는 것을 알게 되면, HTTP를 사용하지 않는 다른 인커밍 어댑터에서 동일한 도메인 로직을 수행할 수 있는 옵션을 본질적으로 잃게 된다. 좋은 아키텍처에서는 옵션을 열어두고 싶다.
참조: 페이지 47-48, 라인 78-87

**경계의 자연스러운 형성**
웹 어댑터와 애플리케이션 레이어 사이의 이 경계는 웹 레이어 대신 도메인과 애플리케이션 레이어로 개발을 시작하면 자연스럽게 생긴다는 점을 주목하라. 특정 인커밍 어댑터를 생각하지 않고 유스케이스를 먼저 구현하면, 경계를 흐리게 만들 유혹을 받지 않는다.
참조: 페이지 48, 라인 88-91

### 3. 컨트롤러 슬라이싱 (Slicing Controllers)

**컨트롤러의 역할**
대부분의 웹 프레임워크(Java 세계의 Spring MVC 같은)에서는 위에서 논의한 책임들을 수행하는 컨트롤러 클래스를 만든다. 그렇다면 애플리케이션으로 향하는 모든 요청에 응답하는 단일 컨트롤러를 만드는가? 그럴 필요는 없다. 웹 어댑터는 확실히 하나 이상의 클래스로 구성될 수 있다.
참조: 페이지 48, 라인 92-96

**패키지 구성**
그러나 이 클래스들을 같은 패키지 계층에 두어 함께 속한다는 것을 표시해야 한다. 3장 "코드 조직화"에서 논의한 대로이다.
참조: 페이지 48, 라인 97-98

**컨트롤러 수**
그렇다면 몇 개의 컨트롤러를 만드는가? 나는 너무 적은 것보다는 너무 많은 것을 만들어야 한다고 말한다. 각 컨트롤러가 가능한 한 좁은 웹 어댑터의 슬라이스를 구현하도록 하고, 다른 컨트롤러와 가능한 한 적게 공유하도록 해야 한다.
참조: 페이지 48, 라인 99-101

**단일 컨트롤러 접근 방식 (안티패턴)**
BuckPal 애플리케이션 내의 계정(account) 엔티티에 대한 오퍼레이션들을 예로 들어보자. 인기 있는 접근 방식은 계정과 관련된 모든 오퍼레이션에 대한 요청을 수용하는 단일 AccountController를 만드는 것이다.

REST API를 제공하는 Spring 컨트롤러는 다음 코드 스니펫처럼 보일 수 있다.
참조: 페이지 48, 라인 102-104

```java
// Java 버전
package buckpal.adapter.web;

@RestController
@RequiredArgsConstructor
class AccountController {

    private final GetAccountBalanceQuery getAccountBalanceQuery;
    private final ListAccountsQuery listAccountsQuery;
    private final LoadAccountQuery loadAccountQuery;

    private final SendMoneyUseCase sendMoneyUseCase;
    private final CreateAccountUseCase createAccountUseCase;

    @GetMapping("/accounts")
    List<AccountResource> listAccounts(){
        ...
    }

    @GetMapping("/accounts/id")
    AccountResource getAccount(@PathVariable("accountId") Long accountId){
        ...
    }

    @GetMapping("/accounts/{id}/balance")
    long getAccountBalance(@PathVariable("accountId") Long accountId){
        ...
    }

    @PostMapping("/accounts")
    AccountResource createAccount(@RequestBody AccountResource account){
        ...
    }

    @PostMapping("/accounts/send/{sourceAccountId}/{targetAccountId}/{amount}")
    void sendMoney(
        @PathVariable("sourceAccountId") Long sourceAccountId,
        @PathVariable("targetAccountId") Long targetAccountId,
        @PathVariable("amount") Long amount) {
        ...
    }
}
```
참조: 페이지 48-49, 라인 105-182

```python
# Python 버전 (FastAPI 사용)
from fastapi import APIRouter, Path, Body
from typing import List

# 컨트롤러 라우터 생성
router = APIRouter()

class AccountController:
    """계정 관련 모든 오퍼레이션을 처리하는 단일 컨트롤러 (안티패턴)"""

    def __init__(
        self,
        get_account_balance_query,
        list_accounts_query,
        load_account_query,
        send_money_use_case,
        create_account_use_case
    ):
        self.get_account_balance_query = get_account_balance_query
        self.list_accounts_query = list_accounts_query
        self.load_account_query = load_account_query
        self.send_money_use_case = send_money_use_case
        self.create_account_use_case = create_account_use_case

    @router.get("/accounts")
    def list_accounts(self) -> List[dict]:
        """계정 목록 조회"""
        # ...
        pass

    @router.get("/accounts/{account_id}")
    def get_account(self, account_id: int = Path(...)) -> dict:
        """특정 계정 조회"""
        # ...
        pass

    @router.get("/accounts/{account_id}/balance")
    def get_account_balance(self, account_id: int = Path(...)) -> int:
        """계정 잔액 조회"""
        # ...
        pass

    @router.post("/accounts")
    def create_account(self, account: dict = Body(...)) -> dict:
        """계정 생성"""
        # ...
        pass

    @router.post("/accounts/send/{source_account_id}/{target_account_id}/{amount}")
    def send_money(
        self,
        source_account_id: int = Path(...),
        target_account_id: int = Path(...),
        amount: int = Path(...)
    ) -> None:
        """송금"""
        # ...
        pass
```

**단일 컨트롤러의 문제점**
계정 리소스에 관한 모든 것이 단일 클래스에 있어서 좋아 보인다. 하지만 이 접근 방식의 단점들을 논의해보자.

첫째, 클래스당 코드가 적을수록 좋다. 나는 가장 큰 클래스가 30,000 라인의 코드를 가진 레거시 프로젝트에서 작업한 적이 있다. 그것은 재미없다. 컨트롤러가 수년에 걸쳐 200 라인의 코드만 축적하더라도, 메서드로 깔끔하게 분리되어 있더라도 50 라인보다는 파악하기 어렵다.

동일한 주장이 테스트 코드에도 유효하다. 컨트롤러 자체에 많은 코드가 있으면, 많은 테스트 코드가 있을 것이다. 그리고 종종 테스트 코드는 프로덕션 코드보다 파악하기 더 어렵다. 더 추상적인 경향이 있기 때문이다. 또한 특정 프로덕션 코드에 대한 테스트를 찾기 쉽게 만들고 싶은데, 이는 작은 클래스에서 더 쉽다.
참조: 페이지 49, 라인 185-191

**모델 공유의 문제**
그러나 똑같이 중요한 것은, 모든 오퍼레이션을 단일 컨트롤러 클래스에 넣는 것이 데이터 구조의 재사용을 장려한다는 것이다. 위의 코드 예제에서 많은 오퍼레이션이 AccountResource 모델 클래스를 공유한다. 이것은 오퍼레이션 중 하나에서 필요한 모든 것의 버킷 역할을 한다. AccountResource는 아마도 id 필드를 가지고 있을 것이다. 이것은 create 오퍼레이션에서는 필요하지 않으며 여기서 혼란을 야기할 것이다. Account가 User 객체와 일대다 관계를 가진다고 상상해보자. 책을 생성하거나 업데이트할 때 그 User 객체를 포함하는가? list 오퍼레이션에서 사용자들이 반환되는가? 이것은 쉬운 예제이지만, 평균 이상의 프로젝트에서는 언젠가 이런 질문들을 하게 될 것이다.
참조: 페이지 49-50, 라인 192-206

**별도 컨트롤러 접근 방식 (권장)**
그래서 나는 각 오퍼레이션마다 별도의 컨트롤러를, 잠재적으로 별도의 패키지에 만드는 접근 방식을 주장한다. 또한 메서드와 클래스의 이름을 유스케이스에 최대한 가깝게 지어야 한다:
참조: 페이지 50, 라인 207-208

```java
// Java 버전
package buckpal.adapter.web;

@RestController
@RequiredArgsConstructor
public class SendMoneyController {

    private final SendMoneyUseCase sendMoneyUseCase;

    @PostMapping(path = "/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}")
    void sendMoney(
        @PathVariable("sourceAccountId") Long sourceAccountId,
        @PathVariable("targetAccountId") Long targetAccountId,
        @PathVariable("amount") Long amount) {

        SendMoneyCommand command = new SendMoneyCommand(
            new AccountId(sourceAccountId),
            new AccountId(targetAccountId),
            Money.of(amount));

        sendMoneyUseCase.sendMoney(command);
    }

}
```
참조: 페이지 50, 라인 209-250

```python
# Python 버전 (FastAPI 사용)
from fastapi import APIRouter, Path

# 송금 전용 라우터 생성
router = APIRouter()

class SendMoneyController:
    """송금 유스케이스만 처리하는 좁은 범위의 컨트롤러"""

    def __init__(self, send_money_use_case):
        """
        Args:
            send_money_use_case: 송금 유스케이스 인터페이스
        """
        self.send_money_use_case = send_money_use_case

    @router.post("/accounts/sendMoney/{source_account_id}/{target_account_id}/{amount}")
    def send_money(
        self,
        source_account_id: int = Path(..., description="출금 계정 ID"),
        target_account_id: int = Path(..., description="입금 계정 ID"),
        amount: int = Path(..., description="송금 금액")
    ) -> None:
        """
        송금 요청을 처리

        Args:
            source_account_id: 출금할 계정 ID
            target_account_id: 입금받을 계정 ID
            amount: 송금할 금액
        """
        # HTTP 요청 파라미터를 유스케이스 커맨드 객체로 변환
        command = SendMoneyCommand(
            source_account_id=AccountId(source_account_id),
            target_account_id=AccountId(target_account_id),
            money=Money.of(amount)
        )

        # 유스케이스 실행
        self.send_money_use_case.send_money(command)
```

**전용 모델 클래스**
또한 각 컨트롤러는 CreateAccountResource나 UpdateAccountResource 같은 자체 모델을 가질 수 있거나, 위의 예제처럼 프리미티브를 입력으로 사용할 수 있다. 이런 특화된 모델 클래스들은 컨트롤러의 패키지에 private으로 만들어 다른 곳에서 실수로 재사용되지 않도록 할 수 있다. 컨트롤러들은 여전히 모델을 공유할 수 있지만, 다른 패키지의 공유 클래스를 사용하면 더 많이 생각하게 되고, 필드의 절반이 필요 없다는 것을 알게 되어 결국 자체 모델을 만들 수도 있다.
참조: 페이지 50, 라인 251-256

**네이밍에 대한 고민**
또한 컨트롤러와 서비스의 이름에 대해 깊이 생각해야 한다. 예를 들어 CreateAccount 대신 RegisterAccount가 더 나은 이름이 아닐까? BuckPal 애플리케이션에서 계정을 만드는 유일한 방법은 사용자가 등록하는 것이다. 그래서 의미를 더 잘 전달하기 위해 클래스 이름에 "register"라는 단어를 사용한다. 일반적인 Create..., Update..., Delete...가 유스케이스를 충분히 설명하는 경우도 분명 있지만, 실제로 사용하기 전에 두 번 생각해볼 필요가 있다.
참조: 페이지 50-51, 라인 257-266

**병렬 작업의 이점**
이 슬라이싱 스타일의 또 다른 장점은 다른 오퍼레이션에 대한 병렬 작업을 쉽게 만든다는 것이다. 두 개발자가 다른 오퍼레이션을 작업하면 머지 충돌이 발생하지 않을 것이다.
참조: 페이지 51, 라인 267-268

### 4. 이것이 유지보수 가능한 소프트웨어 구축에 어떻게 도움이 되는가? (How Does This Help Me Build Maintainable Software?)

**웹 어댑터의 본질**
애플리케이션에 웹 어댑터를 구축할 때, HTTP를 애플리케이션의 유스케이스에 대한 메서드 호출로 변환하고 결과를 다시 HTTP로 변환하는 어댑터를 구축하고 있다는 것을 염두에 두어야 하며, 도메인 로직은 수행하지 않는다.
참조: 페이지 51, 라인 270-272

**HTTP 격리**
반면에 애플리케이션 레이어는 HTTP를 수행해서는 안 되므로, HTTP 상세 사항이 누출되지 않도록 확실히 해야 한다. 이것이 필요가 생길 경우 웹 어댑터를 다른 어댑터로 교체할 수 있게 만든다.
참조: 페이지 51, 라인 273-274

**컨트롤러 슬라이싱의 이점**
웹 컨트롤러를 슬라이싱할 때, 모델을 공유하지 않는 많은 작은 클래스를 만드는 것을 두려워해서는 안 된다. 그것들은 파악하기 쉽고, 테스트하기 쉬우며, 병렬 작업을 지원한다. 처음에 이렇게 세밀한 컨트롤러를 설정하는 것은 더 많은 작업이지만, 유지보수 중에는 그만한 가치가 있을 것이다.
참조: 페이지 51, 라인 275-277
