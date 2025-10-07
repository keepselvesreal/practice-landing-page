# 2장: 채팅 애플리케이션과 테스트 더블 - 추출된 정보

## 핵심 내용
- 테스트 더블의 개념과 의존성 분리
- TDD로 채팅 애플리케이션 개발
- 더미(Dummy), 스텁(Stub), 스파이(Spy), 목(Mock), 페이크(Fake) 객체 활용
- 의존성 주입을 통한 테스트 더블 관리
- 승인 테스트에서의 테스트 더블 사용

## 상세 핵심 내용

### 테스트 더블의 목적
- **의존성 분리**: 컴포넌트 간 의존성을 끊어 격리된 테스트 환경 구축
- **빠른 테스트**: 외부 의존성 없이 빠른 테스트 실행
- **일관된 테스트**: 외부 상태에 영향받지 않는 안정적 테스트
- **동작 시뮬레이션**: 다른 컴포넌트의 상태에 의존하는 동작 시뮬레이션

### 테스트 더블의 종류
- **더미(Dummy)**: 아무것도 하지 않는 객체, 단순히 매개변수 전달용
- **스텁(Stub)**: 미리 준비된 답변을 제공하는 객체
- **스파이(Spy)**: 호출 방법과 인자를 기록하는 객체
- **목(Mock)**: 동작을 검증하고 예상된 방식으로 사용되었는지 확인
- **페이크(Fake)**: 실제 의존성을 충분히 모방하는 단순화된 구현

### TDD 접근법
- **탑다운 vs 바텀업**: 상위레벨 테스트부터 vs 단위 테스트부터
- **승인 테스트 우선**: "달성하고자 하는 것"을 먼저 정의
- **TODO 리스트**: Kent Beck이 제안한 할 일 목록 관리
- **점진적 개발**: 테스트 실패 → 최소 구현 → 리팩터링

## 상세 내용

### 채팅 애플리케이션 승인 테스트
```python
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("John Doe")
        user2 = ChatClient("Harry Potter")
        user1.send_message("Hello World")
        messages = user2.fetch_messages()
        assert messages == ["John Doe: Hello World"]
```

### 더미 객체 사용 예제
```python
class _DummyConnection:
    def broadcast(*args, **kwargs):
        pass

# unittest.mock 사용
class TestChatClient(unittest.TestCase):
    def test_send_message(self):
        client = ChatClient("User 1")
        client.connection = unittest.mock.Mock()
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
```

### 스텁 객체 구현
```python
class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        with unittest.mock.patch.object(Connection, "connect"):
            c = Connection(("localhost", 9090))
        with unittest.mock.patch.object(c, "get_messages", return_value=[]):
            c.broadcast("some message")
            assert c.get_messages()[-1] == "some message"
```

### 스파이를 이용한 동작 검증
```python
def test_client_connection(self):
    client = ChatClient("User 1")
    connection_spy = unittest.mock.MagicMock()
    with unittest.mock.patch.object(client, "_get_connection",
                                   return_value=connection_spy):
        client.send_message("Hello World")
    connection_spy.broadcast.assert_called_with("User 1: Hello World")
```

### 페이크 서버 구현
```python
class FakeServer:
    def __init__(self):
        self.last_command = None
        self.last_args = None
        self.messages = []

    def send(self, data):
        callid, command, args, kwargs = data
        self.last_command = command
        self.last_args = args

    def recv(self, *args, **kwargs):
        if self.last_command == "dummy":
            return "#RETURN", None
        elif self.last_command == "create":
            return "#RETURN", ("fakeid", tuple())
        elif self.last_command == "append":
            self.messages.append(self.last_args[0])
            return "#RETURN", None
        # ... 더 많은 명령어 처리
```

### 의존성 주입 구현
```python
class ChatClient:
    def __init__(self, nickname, connection_provider=Connection):
        self.nickname = nickname
        self._connection = None
        self._connection_provider = connection_provider
        self._last_msg_idx = 0

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._connection_provider(("localhost", 9090))
        return self._connection
```

### Pinject 프레임워크 사용
```python
import pinject

class ChatClient:
    def __init__(self, connection):
        print(self, "GOT", connection)

class Connection:
    pass

injector = pinject.new_object_graph()
cli = injector.provide(ChatClient)

# 페이크 바인딩
class FakedBindingSpec(pinject.BindingSpec):
    def provide_connection(self):
        return FakeConnection()

faked_injector = pinject.new_object_graph(binding_specs=[FakedBindingSpec()])
```

## 주요 화제

### 1. 테스트 더블 기초
- 테스트 더블의 필요성과 목적
- 실제 컴포넌트 대신 사용하는 가짜 객체
- 빠르고 일관된 테스트 환경 구축
- unittest.mock 모듈의 활용

### 2. TDD 개발 프로세스
- 승인 테스트부터 시작하는 탑다운 접근
- 실패하는 테스트 작성 → 최소 구현 → 리팩터링
- TODO 리스트를 통한 작업 관리
- 테스트가 설계를 이끄는 개발 방식

### 3. 채팅 애플리케이션 구현
- ChatClient와 Connection 클래스 설계
- multiprocessing.managers.SyncManager 활용
- 메시지 브로드캐스트와 수신 기능
- 서버-클라이언트 아키텍처

### 4. 각 테스트 더블의 활용
- 더미: 인자 전달용 빈 객체
- 스텁: 미리 정의된 응답 제공
- 스파이: 호출 추적 및 검증
- 목: 동작 검증과 어설션
- 페이크: 실제 서비스의 단순화된 구현

### 5. 의존성 주입 패턴
- 생성자 주입(Constructor Injection)
- mock.patch 대신 명시적 의존성 제공
- 코드의 유연성과 테스트 용이성 향상
- 의존성 주입 프레임워크(Pinject) 활용

### 6. 승인 테스트와 테스트 더블
- 승인 테스트에서는 테스트 더블 사용 최소화
- 실제 사용 환경에 가까운 테스트
- 페이크는 승인 테스트에서도 사용 가능
- 시스템 테스트로 실제 서비스 검증 필요

## 부차 화제

### 1. Python 기술 요구사항
- Python 3.7 이상 권장
- unittest.mock 모듈 표준 라이브러리
- multiprocessing.managers 활용
- GitHub: PacktPublishing/Crafting-Test-Driven-Software-with-Python

### 2. unittest.mock 모듈 활용
- Mock 객체의 다양한 용도
- patch.object를 통한 런타임 교체
- return_value로 스텁 동작 구현
- assert_called_with로 호출 검증

### 3. 네트워킹과 멀티프로세싱
- SyncManager를 이용한 프로세스 간 통신
- 네트워크 연결 시뮬레이션
- 프로토콜 레벨에서의 페이크 구현
- pickle 기반 통신 채널 교체

### 4. 테스트 조직화
- 단위 테스트 vs 통합 테스트 vs 승인 테스트
- 각 레벨에서의 테스트 더블 사용법
- 테스트 스위트의 계층적 구조
- 빠른 피드백과 신뢰성의 균형

### 5. 의존성 주입 프레임워크
- Pinject의 자동 의존성 해결
- BindingSpec을 통한 커스텀 바인딩
- 싱글톤 vs 프로토타입 스코프
- Google의 의존성 주입 경험

### 6. 실제 적용 고려사항
- 페이크 구현의 복잡성
- 역공학을 통한 프로토콜 이해
- 인메모리 데이터베이스 등 기존 페이크 활용
- 테스트 더블과 실제 구현 간 동기화

### 7. 코드 품질과 유지보수
- mock.patch 사용 최소화
- 명시적이고 읽기 쉬운 테스트 코드
- 의존성 주입을 통한 유연한 설계
- 테스트 더블이 설계에 미치는 영향