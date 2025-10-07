# 입찰 준비하기 (Getting Ready to Bid)

## 압축 내용
엔드투엔드 테스트로 입찰 기능을 구현하며, 옥션 프로토콜 메시지 해석을 통해 새로운 클래스를 발견하고, 첫 단위 테스트 작성 후 헬퍼 클래스로 리팩토링하는 Outside-In 개발 과정을 보여준다.

## 핵심 내용

### 핵심 개념

1. **Outside-In 개발 방법론** (상세 내용: Outside-In Development 섹션 참조)
   - 외부 이벤트에서 시작하여 안쪽으로 코드 구현
   - 엔드투엔드 테스트가 개발의 끝점을 정의
   - 한 번에 한 객체씩 작업하며 가시적 효과까지 구현

2. **AuctionMessageTranslator 클래스** (상세 내용: The AuctionMessageTranslator 섹션 참조)
   - 옥션 메시지를 도메인 이벤트로 변환하는 책임
   - MessageListener 구현 및 AuctionEventListener에 위임
   - 단일 책임 원칙(Single Responsibility Principle) 적용

3. **Fake 객체를 이용한 동기화** (상세 내용: A Test for Bidding, Extending the Fake Auction 섹션 참조)
   - FakeAuctionServer로 비동기 통신 테스트
   - hasReceivedJoinRequestFrom()으로 테스트 동기화
   - 메시지 수신 확인을 통한 타이밍 이슈 해결

4. **Double-Entry Values 패턴** (상세 내용: Double-Entry Values 섹션 참조)
   - 메시지 생성과 검증에 동일한 상수 사용
   - 중복 제거 vs 테스트 신뢰성 사이 트레이드오프
   - 통신 기능 테스트에 초점, 간단한 메시지는 상수로 처리

5. **점진적 테스트 작성** (상세 내용: The First Unit Test 섹션 참조)
   - 테스트 메서드 이름부터 시작
   - 트리거 액션 추가
   - 기대 동작 명세(expectation)
   - 최소 구현으로 통과 후 기능 추가

### 핵심 개념 간 관계

- **Outside-In 개발**이 전체 개발 방법론을 제공하며, **AuctionMessageTranslator**는 이 방법론을 적용한 구체적 사례
- **점진적 테스트 작성**은 Outside-In 개발의 구현 기법으로, 각 단계마다 작은 단위 테스트를 작성
- **Fake 객체**는 비동기 시스템에서 Outside-In 개발을 가능하게 하는 테스트 인프라
- **Double-Entry Values**는 테스트 작성 시 실용적 균형점을 제시
- **AuctionMessageTranslator**는 **단일 책임 원칙**을 적용하여 메시지 해석과 UI 업데이트를 분리

## 상세 내용

### 화제 목차

1. [시장 소개 (An Introduction to the Market)](#1-시장-소개)
2. [입찰 테스트 (A Test for Bidding)](#2-입찰-테스트)
3. [Fake 옥션 확장 (Extending the Fake Auction)](#3-fake-옥션-확장)
4. [이중 입력 값 (Double-Entry Values)](#4-이중-입력-값)
5. [예상치 못한 실패 (A Surprise Failure)](#5-예상치-못한-실패)
6. [Outside-In 개발 (Outside-In Development)](#6-outside-in-개발)
7. [AuctionMessageTranslator](#7-auctionmessagetranslator)
8. [첫 번째 단위 테스트 (The First Unit Test)](#8-첫-번째-단위-테스트)
9. [사용자 인터페이스 루프 닫기 (Closing the User Interface Loop)](#9-사용자-인터페이스-루프-닫기)
10. [가격 메시지 언팩 (Unpacking a Price Message)](#10-가격-메시지-언팩)
11. [작업 완료 (Finish the Job)](#11-작업-완료)

---

### 1. 시장 소개
**참조**: content.md 10-34행

**설명**:
- 이전 화제(Ch 11): Walking Skeleton 구축 완료
- Sniper의 핵심 동작 정의: 가격 변경 시 더 높은 입찰
- 다음 구현 항목 선정: 입찰 및 패배, 입찰 및 승리
- 분산 시스템의 실패/타이밍 이슈는 XMPP 프로토콜에 위임
- 핵심 개념 연결: **Outside-In 개발**의 시작점 설정

```python
# 구현할 기능 목록 (원문: 15-21행)
"""
• 단일 아이템: 참가, 입찰, 패배
  - 가격 수신 시 옥션의 최소 증가분만큼 높은 입찰 전송
  - 최소 증가분은 가격 업데이트 정보에 포함

• 단일 아이템: 참가, 입찰, 승리
  - 현재 입찰자가 누구인지 구분
  - 자기 자신에게 입찰하지 않도록 처리
"""
```

---

### 2. 입찰 테스트
**참조**: content.md 37-97행

**설명**:
- 이전 화제와의 관계: 시장 소개에서 정의한 기능을 테스트로 구체화
- 인수 테스트 작성: 가격 정보를 포함한 다음 단계 기능
- 핵심 개념 연결: **점진적 테스트 작성**의 시작
- Fake 객체로 3단계 검증: 가격 전송 → Sniper 수신/응답 → 옥션의 입찰 수신

**테스트 단계** (원문: 42-47행):
```python
# 1. 옥션에 가격을 Sniper에게 전송하도록 지시
# 2. Sniper가 가격을 수신하고 응답했는지 확인
# 3. 옥션이 Sniper로부터 증가된 입찰을 받았는지 확인
```

**엔드투엔드 테스트 코드** (원문: 53-65행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionSniperEndToEndTest:
    def test_sniper_makes_a_higher_bid_but_loses(self):
        """Sniper가 더 높은 입찰을 하지만 패배"""
        auction.start_selling_item()
        application.start_bidding_in(auction)

        # 1. Join 요청 수신 대기로 동기화
        auction.has_received_join_request_from_sniper()

        # 2. 가격 정보 전송 (현재가: 1000, 증가분: 98, 입찰자: "other bidder")
        auction.report_price(1000, 98, "other bidder")

        # 3. Sniper가 입찰 중 상태 표시 확인
        application.has_shown_sniper_is_bidding()

        # 4. 옥션이 올바른 입찰(1098 = 1000 + 98) 수신 확인
        auction.has_received_bid(1098, ApplicationRunner.SNIPER_XMPP_ID)

        # 5. 옥션 종료 및 패배 상태 확인
        auction.announce_closed()
        application.shows_sniper_has_lost_auction()
```

**핵심 포인트** (원문: 67-91행):
- 주석 1: `hasReceivedJoinRequestFromSniper()` - Sniper와 옥션 동기화 (핵심 개념: **Fake 객체를 이용한 동기화**)
- 주석 2: `reportPrice()` - 가격, 증가분, 입찰자 정보 전송
- 주석 3: `hasShownSniperIsBidding()` - 입찰 중 상태 UI 확인
- 주석 4: `hasReceivedBid()` - SNIPER_XMPP_ID로 올바른 입찰 확인
- 주석 5: 기존 종료 로직 재사용

**화폐 단순화** (원문: 92-96행):
```python
# 실제 시스템에서는 도메인 타입으로 화폐 표현 필요 (고정 소수점)
# 예제에서는 정수 사용 (일본 엔화 가정)
# 이유: 인쇄 페이지에 코드를 쉽게 맞추기 위함
```

---

### 3. Fake 옥션 확장
**참조**: content.md 98-175행

**설명**:
- 이전 화제와의 관계: 입찰 테스트를 지원하기 위한 인프라 구축
- 핵심 개념 연결: **Fake 객체를 이용한 동기화** 구현
- `reportPrice()`: 가격 메시지 전송
- `hasReceivedBid()`: 입찰 메시지 수신 확인
- 메시지 파싱 대신 예상 메시지 구성 후 문자열 비교

**첫 번째 구현** (원문: 105-125행, 자바 → 파이썬):
```python
# 원본: 자바
class FakeAuctionServer:
    def report_price(self, price: int, increment: int, bidder: str):
        """가격 정보를 Sniper에게 전송"""
        message = (f"SOLVersion: 1.1; Event: PRICE; "
                  f"CurrentPrice: {price}; Increment: {increment}; Bidder: {bidder};")
        self.current_chat.send_message(message)

    def has_received_join_request_from_sniper(self):
        """Join 요청 수신 확인 - 모든 메시지 허용"""
        self.message_listener.receives_a_message(is_anything())

    def has_received_bid(self, bid: int, sniper_id: str):
        """입찰 수신 확인 - sniper_id와 정확한 입찰가 검증"""
        assert self.current_chat.get_participant() == sniper_id
        expected_message = f"SOLVersion: 1.1; Command: BID; Price: {bid};"
        self.message_listener.receives_a_message(equals_to(expected_message))
```

**SingleMessageListener 수정** (원문: 130-139행, 자바 → 파이썬):
```python
# 원본: 자바
class SingleMessageListener:
    """메시지 수신 대기 및 검증"""

    def receives_a_message(self, message_matcher):
        """메시지 매처로 메시지 검증"""
        # 5초 대기 후 메시지 폴링
        message = self.messages.poll(5, TimeUnit.SECONDS)
        assert message is not None, "Message should not be null"
        assert message_matcher.matches(message.get_body())
```

**대칭성을 위한 리팩토링** (원문: 140-171행):
- Join 메시지 검증이 너무 느슨함 → 입찰 메시지와 일관성 유지
- 메시지 포맷을 Main으로 이동 (재사용)
- 핵심 개념 연결: **점진적 테스트 작성**에서 일관성 유지의 중요성

**개선된 구현** (원문: 148-167행, 자바 → 파이썬):
```python
# 원본: 자바
class FakeAuctionServer:
    def has_received_join_request_from(self, sniper_id: str):
        """Join 요청 수신 확인 - 더 엄격한 검증"""
        self._receives_a_message_matching(sniper_id,
                                         equals_to(Main.JOIN_COMMAND_FORMAT))

    def has_received_bid(self, bid: int, sniper_id: str):
        """입찰 수신 확인"""
        expected_message = Main.BID_COMMAND_FORMAT.format(bid)
        self._receives_a_message_matching(sniper_id, equals_to(expected_message))

    def _receives_a_message_matching(self, sniper_id: str, message_matcher):
        """메시지 매칭 및 발신자 확인 - 순서가 중요!"""
        # 1. 메시지 내용 확인 (current_chat 설정 대기)
        self.message_listener.receives_a_message(message_matcher)
        # 2. 발신자 확인 (메시지 도착 후)
        assert self.current_chat.get_participant() == sniper_id
```

**타이밍 이슈 해결** (원문: 168-171행):
```python
# 메시지 확인을 sniper_id 확인보다 먼저 수행
# 이유: 메시지가 도착할 때까지 대기하여 current_chat 설정 보장
# 순서를 바꾸면 current_chat이 None일 수 있어 테스트 실패
```

---

### 4. 이중 입력 값
**참조**: content.md 177-209행

**설명**:
- 이전 화제와의 관계: Fake 옥션에서 사용한 상수 재사용의 타당성 논의
- 핵심 개념: **Double-Entry Values 패턴**
- 동일 상수로 메시지 생성과 검증 → 중복 제거, 코드에서 링크 표현
- 트레이드오프: 둘 다 틀릴 경우 테스트가 잡지 못할 위험

**핵심 질문** (원문: 188-192행):
```python
"""
무엇을 테스트하고 있는가?
- 통신 기능이 더 중요
- 메시지가 충분히 단순하여 문자열 상수에 의존 가능
- IDE에서 메시지 포맷 관련 코드 찾기 용이

다른 개발자는 다른 결론을 내릴 수 있으며,
그들의 프로젝트에서는 그것이 옳을 수 있음
"""
```

**테스트 업데이트** (원문: 195-207행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionSniperEndToEndTest:
    def test_sniper_makes_a_higher_bid_but_loses(self):
        auction.start_selling_item()
        application.start_bidding_in(auction)

        # 새 API에 맞춰 조정
        auction.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)
        auction.report_price(1000, 98, "other bidder")
        application.has_shown_sniper_is_bidding()
        auction.has_received_bid(1098, ApplicationRunner.SNIPER_XMPP_ID)
        auction.announce_closed()
        application.shows_sniper_has_lost_auction()
```

**Main 클래스 수정** (원문: 212-230행, 자바 → 파이썬):
```python
# 원본: 자바
class Main:
    def join_auction(self, connection, item_id):
        """옥션 참가"""
        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            # 메시지 리스너: 모든 메시지를 Lost로 처리 (임시)
            lambda a_chat, message: SwingUtilities.invoke_later(
                lambda: self.ui.show_status(MainWindow.STATUS_LOST)
            )
        )
        self.not_to_be_gcd = chat  # GC 방지
        chat.send_message(JOIN_COMMAND_FORMAT)  # 상수 사용
```

---

### 5. 예상치 못한 실패
**참조**: content.md 231-311행

**설명**:
- 이전 화제와의 관계: 테스트 실행 중 예상치 못한 실패 발견
- XMPP 서버 리소스 충돌: 동일 계정으로 다중 연결 시도
- 근본 원인: 첫 번째 테스트의 연결이 닫히지 않음
- 핵심 개념 연결: **Outside-In 개발**의 실전 문제 해결

**에러 메시지** (원문: 245-265행):
```python
# 예상한 실패
"""
java.lang.AssertionError:
Expected: is not null
     got: null
  at SingleMessageListener.receivesAMessage()
  at FakeAuctionServer.hasReceivedJoinRequestFromSniper()
"""

# 에러 스트림의 실제 원인
"""
conflict(409)
  at jivesoftware.smack.SASLAuthentication.bindResourceAndEstablishSession()
  at jivesoftware.smack.XMPPConnection.login()
  at auctionsniper.Main.connection()
  at auctionsniper.Main.main()
"""
```

**문제 분석** (원문: 266-273행):
```python
"""
두 번째 테스트가 첫 번째와 동일한 계정/리소스로 연결 시도
서버 설정: 다중 연결 거부 (Southabee's On-Line과 동일)
두 번째 테스트 실패: 서버가 첫 번째 연결을 여전히 활성으로 인식
프로덕션에서는 정상 작동: 프로세스 종료 시 연결 자동 해제
타협안(새 스레드에서 애플리케이션 시작)의 부작용 발견
"""
```

**해결책** (원문: 275-291행, 자바 → 파이썬):
```python
# 원본: 자바
class Main:
    def join_auction(self, connection, item_id):
        # UI 종료 시 연결 해제 콜백 추가
        self._disconnect_when_ui_closes(connection)

        chat = connection.get_chat_manager().create_chat(...)
        chat.send_message(JOIN_COMMAND_FORMAT)

    def _disconnect_when_ui_closes(self, connection):
        """UI 윈도우 종료 시 XMPP 연결 해제"""
        class DisconnectAdapter(WindowAdapter):
            def window_closed(self, e):
                connection.disconnect()

        self.ui.add_window_listener(DisconnectAdapter())
```

**예상된 실패로 전환** (원문: 292-309행):
```python
# 이제 Sniper가 입찰을 시작할 방법이 없어서 실패
"""
java.lang.AssertionError:
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
and check that its label text is "Bidding"
but...
label text was "Lost"
  at AuctionSniperDriver.showsSniperStatus()
  at ApplicationRunner.hasShownSniperIsBidding()
"""
```

---

### 6. Outside-In 개발
**참조**: content.md 313-340행

**설명**:
- 이전 화제와의 관계: 실패를 통해 다음 구현 목표 정의
- 핵심 개념: **Outside-In 개발 방법론**
- 외부 이벤트에서 시작하여 가시적 효과까지 객체 단위로 탐색
- 엔드투엔드 테스트가 끝점 정의, 중간 공간 탐색

**개발 접근법** (원문: 317-326행):
```python
"""
Outside-In 개발 과정:
1. 외부 이벤트(트리거) 식별
2. 코드 안쪽으로 한 번째 한 객체씩 작업
3. 가시적 효과(메시지 전송, 로그 엔트리)까지 도달
4. 엔드투엔드 테스트로 끝점 확인
5. 중간 공간을 탐색하며 구현

실전에서는 때때로 더 앞서 설계하지만,
대부분의 경우 이 방식이 올바른 결과와 질문을 이끌어냄
"""
```

**무한한 주의력?** (원문: 327-340행):
```python
"""
리소스 충돌 감지: 운 또는 통찰로 서버 설정이 프로덕션과 일치
대안 설정: 새 연결이 기존 연결 종료 → 테스트는 통과하지만 에러 메시지
개발 환경에서는 작동, 프로덕션에서 Sniper 실패 위험

모든 설정 옵션을 어떻게 잡을 수 있나?
- 일정 수준에서는 불가능 (전문 테스터의 영역)
- 가능한 한 많은 시스템을 조기에, 반복적으로 실행
- 컴포넌트 품질을 높게 유지하고 지속적으로 단순화
- 비용 대비: 프로덕션 시스템에서 이런 간헐적 버그 찾고 고치는 비용
"""
```

---

### 7. AuctionMessageTranslator
**참조**: content.md 341-395행

**설명**:
- 이전 화제와의 관계: Outside-In 개발의 진입점 구현
- 핵심 개념: **AuctionMessageTranslator 클래스**
- MessageListener 구현 → 옥션 메시지를 도메인 이벤트로 변환
- 단일 책임 원칙 적용: 메시지 해석만 담당, UI 업데이트는 위임

**새 클래스 발견** (원문: 343-349행):
```python
"""
진입점: Smack 라이브러리를 통한 옥션 메시지 수신
필요: MessageListener를 Chat에 부착
역할:
  1. 옥션의 원시 메시지 수신
  2. 코드 내 옥션 이벤트로 변환
  3. Sniper 액션 및 UI 변경 유도
"""
```

**익명 클래스 분석** (원문: 355-365행, 자바 → 파이썬):
```python
# 원본: 자바 - Main의 익명 MessageListener
class AnonymousMessageListener:
    """현재는 암묵적으로 Close 메시지만 처리"""

    def process_message(self, a_chat, message):
        # Swing 이벤트 스레드에서 UI 업데이트
        SwingUtilities.invoke_later(
            lambda: self.ui.show_status(MainWindow.STATUS_LOST)
        )
```

**설계 결정** (원문: 366-389행):
```python
"""
익명 클래스를 AuctionMessageTranslator로 승격
이유: 책임을 명확히 하고 기능 추가 전 구조화

문제: 익명 클래스가 Main의 ui 필드 사용
해결책 고려:
  1. MainWindow 전달 → 거부
     - UI 컴포넌트 의존성 생성
     - 단위 테스트 어려움 (Swing 이벤트 스레드)

  2. AuctionEventListener 인터페이스 도입 → 채택
     - 단일 책임 원칙 준수
     - 메시지 언팩과 Sniper 상태 표시 분리
     - 관심사의 분리 (Separation of Concerns)

AuctionEventListener:
  - 생성자로 전달
  - 인터페이스는 아직 미정의 (필요할 때 정의)
  - 구현은 나중에 (메시지 변환이 우선)
"""
```

**초기 설계** (원문: 389-393행):
```python
# Figure 12.1: The AuctionMessageTranslator
"""
[Chat] → [AuctionMessageTranslator] → [AuctionEventListener]
       (MessageListener 구현)      (인터페이스)

외부 프레임워크(Chat)는 음영 처리
"""
```

---

### 8. 첫 번째 단위 테스트
**참조**: content.md 397-522행

**설명**:
- 이전 화제와의 관계: AuctionMessageTranslator 설계를 테스트로 검증
- 핵심 개념: **점진적 테스트 작성**
- Close 이벤트부터 시작 (간단한 트리거)
- 테스트 메서드 이름 → 액션 → 기대 동작 순으로 작성

**테스트 메서드 이름** (원문: 401-413행, 자바 → 파이썬):
```python
# 원본: 자바
# 패키지: test.auctionsniper (별도 패키지 사용)
class AuctionMessageTranslatorTest:
    def test_notifies_auction_closed_when_close_message_received(self):
        """Close 메시지 수신 시 옥션 종료 통지"""
        # 아직 구현 없음
```

**별도 패키지 사용** (원문: 414-419행):
```python
"""
테스트를 별도 패키지에 배치하는 습관
이유:
  1. 공개 인터페이스를 통한 테스트 (다른 클라이언트처럼)
  2. 패키지 스코프 백도어 방지
  3. IDE에서 네비게이션 용이 (애플리케이션/테스트 코드 분리)
"""
```

**트리거 액션 추가** (원문: 420-433행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslatorTest:
    # Chat은 생성하기 어려워 null 사용
    UNUSED_CHAT = None  # 의미 있는 이름의 null 상수

    def setUp(self):
        self.translator = AuctionMessageTranslator()

    def test_notifies_auction_closed_when_close_message_received(self):
        message = Message()
        message.set_body("SOLVersion: 1.1; Event: CLOSE;")

        # MessageListener 인터페이스 호출
        self.translator.process_message(self.UNUSED_CHAT, message)
```

**null 사용 가이드** (원문: 439-448행):
```python
"""
null을 의미 있게 사용:
- UNUSED_CHAT: null의 의미 있는 이름
- 이유: Chat 객체 생성이 어려움 (패키지 스코프 생성자, 의존성 체인)
- 현재 기능에서는 불필요하므로 null 전달
- 명명된 상수로 의미 명확화

주의: Null Object 패턴 [Woolf98]과 다름
- Null Object: 호출 가능, 아무것도 안 함
- 이 null: 플레이스홀더, 호출 시 실패
"""
```

**스켈레톤 구현** (원문: 449-455행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslator(MessageListener):
    """MessageListener 인터페이스 구현"""

    def process_message(self, chat, message):
        # TODO: 여기를 채우세요
        pass
```

**기대 동작 명세** (원문: 456-476행, 자바 → 파이썬):
```python
# 원본: 자바
# JMock 사용
class AuctionMessageTranslatorTest:
    def setUp(self):
        self.mockery = Mockery()
        # Mock 객체 생성
        self.listener = self.mockery.mock(AuctionEventListener)
        self.translator = AuctionMessageTranslator()

    def test_notifies_auction_closed_when_close_message_received(self):
        # 기대 동작 정의 - 가장 중요한 라인!
        self.mockery.checking(Expectations() {{
            one_of(self.listener).auction_closed()  # 정확히 1회 호출
        }})

        message = Message()
        message.set_body("SOLVersion: 1.1; Event: CLOSE;")
        self.translator.process_message(self.UNUSED_CHAT, message)
```

**테스트 실패** (원문: 487-497행):
```python
# 예상된 실패
"""
not all expectations were satisfied
expectations:
  ! expected once, never invoked: auctionEventListener.auctionClosed()
what happened before this: nothing!
  at org.jmock.Mockery.assertIsSatisfied(Mockery.java:199)
  at org.junit.internal.runners.JUnit4ClassRunner.run()

핵심 문구:
"expected once, never invoked: auctionEventListener.auctionClosed()"
→ 리스너를 호출하지 않음
"""
```

**구현 1: 리스너 연결** (원문: 498-508행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslatorTest:
    def setUp(self):
        self.mockery = Mockery()
        self.listener = self.mockery.mock(AuctionEventListener)
        # 생성자에 리스너 전달 (타입 시스템으로 보장)
        self.translator = AuctionMessageTranslator(self.listener)
```

**구현 2: 메서드 호출** (원문: 509-518행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslator:
    def process_message(self, chat, message):
        # 현재는 무조건 auction_closed() 호출
        self.listener.auction_closed()

# 테스트 통과!
# 메시지 언팩은 아직 안 했지만:
# 1. 컴포넌트 배치 완료
# 2. 테스트 하네스에 통합
# 3. 하나의 기능 잠금 (기능 추가 시에도 작동 보장)
```

**단순화된 테스트 설정** (원문: 524-535행):
```python
"""
모든 테스트 필드를 final로 선언
이유:
  1. JUnit이 각 테스트 메서드마다 새 인스턴스 생성
  2. 필드가 매번 재생성됨
  3. final 선언으로 순환 의존성 제거
  4. 객체 격자(lattice) 구조로 테스트 프레임 지원

예외: 직접 의존성 부착 필요한 경우 (나중에 예제)
대부분 가능: 순환 루프를 강조하여 주의 환기

NUnit: 동일 인스턴스 재사용 → 명시적 갱신 필요
"""
```

---

### 9. 사용자 인터페이스 루프 닫기
**참조**: content.md 536-575행

**설명**:
- 이전 화제와의 관계: 단위 테스트한 컴포넌트를 실제 Sniper에 통합
- Main이 AuctionEventListener 구현
- 익명 클래스를 AuctionMessageTranslator로 교체
- 핵심 개념 연결: **Outside-In 개발**의 통합 단계

**Main 리팩토링** (원문: 537-560행, 자바 → 파이썬):
```python
# 원본: 자바
class Main(AuctionEventListener):
    """이제 AuctionEventListener 인터페이스 구현"""

    def join_auction(self, connection, item_id):
        self._disconnect_when_ui_closes(connection)

        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            # 익명 클래스 → AuctionMessageTranslator로 교체
            AuctionMessageTranslator(self)  # self를 리스너로 전달
        )
        chat.send_message(JOIN_COMMAND_FORMAT)
        self.not_to_be_gcd = chat  # GC 방지

    def auction_closed(self):
        """AuctionEventListener 인터페이스 구현"""
        # 이전 익명 클래스의 기능을 메서드로 이동
        SwingUtilities.invoke_later(
            lambda: self.ui.show_status(MainWindow.STATUS_LOST)
        )
```

**구조 변화** (원문: 561-567행):
```python
# Figure 12.2: Introducing the AuctionMessageTranslator
"""
구조:
[Chat] → [AuctionMessageTranslator] → [Main]
       (MessageListener)            (AuctionEventListener)
                                           ↓
                                      [MainWindow]

Main이 AuctionEventListener 구현
→ UI 업데이트 책임 분리
"""
```

**성과 분석** (원문: 568-575행):
```python
"""
작은 단계에서 달성한 것:
1. 기능을 별도 클래스로 추출
   - 기능에 이름 부여 (AuctionMessageTranslator)
   - 단위 테스트 가능

2. Main 단순화
   - 옥션 메시지 해석 관심 제거
   - 명확한 책임과 관계

아직은 큰 차이 없지만,
애플리케이션이 성장하면서 이 접근법이
코드를 깨끗하고 유연하게 유지하는 데 도움
"""
```

---

### 10. 가격 메시지 언팩
**참조**: content.md 576-688행

**설명**:
- 이전 화제와의 관계: 두 번째 메시지 타입 추가로 메시지 해석 강제
- 메시지 타입 구분: PRICE vs CLOSE
- 핵심 개념 연결: **점진적 테스트 작성**으로 기능 확장

**메시지 포맷 분석** (원문: 578-588행):
```python
# 원문: 581-584행
"""
옥션 메시지 포맷 (Southabee's On-Line):
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Event: CLOSE;

초기 시도: 객체 지향적 타입 모델링
문제: 행위가 명확하지 않아 의미 있는 구조 정당화 불가
결정: 단순한 해법으로 시작, 필요 시 적응
"""
```

**두 번째 테스트** (원문: 590-611행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslatorTest:
    def test_notifies_bid_details_when_current_price_message_received(self):
        """현재 가격 메시지 수신 시 입찰 세부정보 통지"""

        # 기대 동작: currentPrice(192, 7) 정확히 1회 호출
        self.mockery.checking(Expectations() {{
            exactly(1).of(self.listener).current_price(192, 7)
        }})

        message = Message()
        # PRICE 이벤트 메시지
        message.set_body(
            "SOLVersion: 1.1; Event: PRICE; "
            "CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
        )

        self.translator.process_message(self.UNUSED_CHAT, message)
```

**인터페이스 확장** (원문: 612-617행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionEventListener:
    """옥션 이벤트 리스너 인터페이스"""

    def auction_closed(self):
        """옥션 종료"""
        pass

    def current_price(self, price: int, increment: int):
        """현재 가격 및 증가분"""
        pass
```

**테스트 실패 분석** (원문: 618-636행):
```python
# 예상 실패
"""
unexpected invocation: auctionEventListener.auctionClosed()
expectations:
  ! expected once, never invoked: auctionEventListener.currentPrice(<192>, <7>)
what happened before this: nothing!
  at $Proxy6.auctionClosed()
  at auctionsniper.AuctionMessageTranslator.processMessage()
  at AuctionMessageTranslatorTest.translatesPriceMessagesAsAuctionPriceEvents()

핵심 문구:
"unexpected invocation: auctionEventListener.auctionClosed()"
→ 잘못된 메서드(auctionClosed) 호출

스택 트레이스:
- $Proxy6.auctionClosed(): Mockery의 런타임 대리 객체
- processMessage()에서 실패 → 명확하므로 수정
"""
```

**초기 구현** (원문: 637-668행, 자바 → 파이썬):
```python
# 원본: 자바
class AuctionMessageTranslator(MessageListener):
    def __init__(self, listener: AuctionEventListener):
        self.listener = listener

    def process_message(self, chat, message):
        """메시지 처리 - 이벤트 타입에 따라 분기"""
        event = self._unpack_event_from(message)
        event_type = event.get("Event")

        if event_type == "CLOSE":
            self.listener.auction_closed()
        elif event_type == "PRICE":
            # 문자열을 정수로 변환하여 전달
            price = int(event.get("CurrentPrice"))
            increment = int(event.get("Increment"))
            self.listener.current_price(price, increment)

    def _unpack_event_from(self, message) -> dict:
        """메시지 본문을 key/value 쌍으로 파싱"""
        event = {}
        for element in message.get_body().split(";"):
            pair = element.split(":")
            if len(pair) == 2:
                key = pair[0].strip()
                value = pair[1].strip()
                event[key] = value
        return event
```

**FakeAuctionServer 수정** (원문: 671-675행, 자바 → 파이썬):
```python
# 원본: 자바
class FakeAuctionServer:
    def announce_closed(self):
        """실제 Close 이벤트 전송 (빈 메시지 아님)"""
        self.current_chat.send_message("SOLVersion: 1.1; Event: CLOSE;")
```

**추가 작업 발견** (원문: 679-695행):
```python
"""
코드가 단위 테스트를 통과하지만 누락된 것:
1. 메시지 구조 검증 부재
2. 버전 확인 누락
3. 외부 시스템 메시지 → 에러 처리 필요

작업 흐름 유지:
- 기능 구현 흐름을 깨지 않기 위해
- To-Do 리스트에 에러 처리 추가 (나중에 처리)

코드 품질 우려:
- 파싱과 디스패칭이 혼재
- 명확성 부족
- 인수 테스트 통과 후 리팩토링 예정 (곧!)
"""

# Figure 12.3: Added tasks for handling errors
"""
To-Do 리스트 업데이트:
- 메시지 버전 확인
- 메시지 구조 검증
- 에러 처리
"""
```

---

### 11. 작업 완료
**참조**: content.md 696-714행

**설명**:
- 이전 화제와의 관계: 전체 장을 마무리하며 개발 철학 강조
- 핵심: 첫 번째 구현은 완성이 아님
- 리팩토링의 중요성: 의도를 명확히 표현

**작업 내용 요약** (원문: 697-703행):
```python
"""
이 장에서 한 작업:
1. 무엇을 말할지 결정 (what to say)
2. 어떻게 말할지 결정 (how to say it)

구체적:
- 엔드투엔드 테스트: Sniper 구현 내용 기술
- 긴 단위 테스트 이름: 클래스 역할 설명
- 새 클래스 추출: 기능의 세밀한 측면 분리
- 많은 작은 메서드: 각 코드 레이어를 일관된 추상화 수준으로 유지

과정:
1. 거친 구현으로 증명 (요구사항 구현 방법 확인)
2. 리팩토링 (다음 장에서)
"""
```

**미완성 코드의 위험** (원문: 704-709행):
```python
"""
"첫 번째 구현" 코드는 완성이 아님!

목적:
- 아이디어 정리
- 모든 것이 제자리에 있는지 확인

문제:
- 의도를 명확히 표현하지 못함
- 반복적으로 읽히는 코드의 생산성 저하
- 코드 수명 동안 부담

비유:
- 샌딩(sanding) 없는 목공
- 결국 누군가 큰 가시에 찔림
"""
```