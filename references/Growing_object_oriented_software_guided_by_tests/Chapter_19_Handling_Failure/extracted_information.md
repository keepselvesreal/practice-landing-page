# 실패 처리 (Handling Failure)

## 압축 내용

옥션 메시지 파싱 실패를 감지하고, 사용자에게 실패를 표시하며, 해당 옥션으로부터의 이벤트 수신을 중단하고, 실패 정보를 로그 파일에 기록하는 완전한 실패 처리 시스템을 TDD 방식으로 구축한다.

## 핵심 내용

### 핵심 개념

1. **실패 감지 (Failure Detection)**: 잘못된 메시지 수신 시 예외를 포착하고 실패 이벤트를 발생시킴 (→ [상세 내용 2])
2. **실패 표시 (Failure Display)**: UI에 실패 상태를 표시하고 가격 정보를 초기화함 (→ [상세 내용 3])
3. **연결 해제 (Disconnection)**: 실패한 옥션으로부터 더 이상 메시지를 받지 않도록 리스너를 제거함 (→ [상세 내용 4])
4. **실패 기록 (Failure Recording)**: 실패 정보를 로그 파일에 기록하여 나중에 복구할 수 있도록 함 (→ [상세 내용 5, 6, 7])

### 핵심 개념 간 관계

- **실패 감지**는 전체 실패 처리 흐름의 시작점으로, AuctionMessageTranslator에서 예외를 포착하면 auctionFailed() 이벤트를 발생시킴
- **실패 표시**는 실패 감지 이벤트를 받아 AuctionSniper의 상태를 FAILED로 변경하고 UI를 업데이트함
- **연결 해제**는 실패 이벤트 리스너를 통해 실패한 옥션으로부터의 메시지 수신을 중단하여 추가 오류를 방지함
- **실패 기록**은 XMPPFailureReporter를 통해 실패 정보를 로그 파일에 기록하여 운영팀이 상황을 복구할 수 있도록 함
- 모든 개념은 "단일 책임 원칙"에 따라 각각의 역할을 명확히 분리하여 유지보수성을 높임

## 상세 내용

### 화제 목차

1. 실패 시나리오 정의 및 E2E 테스트 작성 (What If It Doesn't Work?, Testing That Something Doesn't Happen)
2. 실패 감지 로직 구현 (Detecting the Failure)
3. 실패 상태 표시 구현 (Displaying the Failure)
4. Sniper 연결 해제 구현 (Disconnecting the Sniper, The Composition Shell Game)
5. 실패 기록 테스트 작성 (Recording the Failure, Filling In the Test)
6. 실패 리포터 구현 (Failure Reporting in the Translator, Generating the Log Message, Breaking Our Own Rules?)
7. 전체 통합 및 관찰 (Closing the Loop, Observations)

---

### 1. 실패 시나리오 정의 및 E2E 테스트 작성

**핵심 개념**: 실패 감지, 실패 표시

#### 요구사항 정의 (섹션: What If It Doesn't Work?, 라인: 16-29)

- Southabee's On-Line 옥션 시스템이 간혹 잘못된 구조의 메시지를 전송하는 문제가 있음
- 해석할 수 없는 메시지를 받으면 해당 옥션을 Failed로 표시하고 추가 업데이트를 무시하는 정책 수립
- 실패 시 가격과 입찰 값을 초기화하고, 상태를 Failed로 표시하며, 이벤트를 기록함

#### E2E 테스트 구현 (섹션: What If It Doesn't Work?, 라인: 30-68)

**참조**: 핵심 개념 - 실패 감지, 실패 표시

```java
// 잘못된 메시지를 받았을 때 Sniper가 실패를 표시하고 추가 이벤트에 응답하지 않음을 테스트
@Test public void
sniperReportsInvalidAuctionMessageAndStopsRespondingToEvents()
    throws Exception
{
  String brokenMessage = "a broken message";

  // 두 개의 옥션을 시작
  auction.startSellingItem();
  auction2.startSellingItem();
  application.startBiddingIn(auction, auction2);

  // 첫 번째 옥션에서 정상적인 입찰 진행
  auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  auction.reportPrice(500, 20, "other bidder");
  auction.hasReceivedBid(520, ApplicationRunner.SNIPER_XMPP_ID);

  // 잘못된 메시지 전송
  auction.sendInvalidMessageContaining(brokenMessage);

  // 실패 상태 표시 확인
  application.showsSniperHasFailed(auction);

  // 추가 가격 이벤트 전송
  auction.reportPrice(520, 21, "other bidder");

  // 동기화를 위한 다른 옥션 이벤트 대기 (비동기 처리 완료 확인)
  waitForAnotherAuctionEvent();

  // 실패 메시지가 로그에 기록되었는지 확인
  application.reportsInvalidMessage(auction, brokenMessage);

  // 실패 상태가 유지되는지 확인 (추가 이벤트에 반응하지 않음)
  application.showsSniperHasFailed(auction);
}

// 비동기 처리 완료를 확인하기 위한 헬퍼 메서드
// 다른 옥션의 이벤트를 강제로 발생시켜 시스템이 이벤트를 처리할 시간을 확보
private void waitForAnotherAuctionEvent() throws Exception {
  auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  auction2.reportPrice(600, 6, "other bidder");
  application.hasShownSniperIsBidding(auction2, 600, 606);
}
```

#### 비동기 테스트 기법 (섹션: Testing That Something Doesn't Happen, 라인: 69-76)

**참조**: 핵심 개념 - 실패 표시

- `waitForAnotherAuctionEvent()` 메서드는 관련 없는 Sniper 이벤트를 강제로 발생시켜 테스트를 지연시킴
- 이 방법 없이는 최종 `showSniperHasFailed()` 체크가 시스템이 관련 가격 이벤트를 처리하기 전의 이전 상태를 확인하여 잘못 통과할 수 있음
- 추가 이벤트가 테스트를 충분히 지연시켜 시스템이 따라잡을 수 있도록 함

#### 초기 테스트 실패 (섹션: Testing That Something Doesn't Happen, 라인: 77-94)

- SniperState 열거형에 FAILED 값을 추가하고 SniperTableModel에 텍스트 매핑 추가
- 테스트 실패 메시지: 가격이 0으로 초기화되어야 하는데 500으로 표시됨

```python
# 파이썬 버전의 E2E 테스트
def test_sniper_reports_invalid_auction_message_and_stops_responding_to_events(self):
    """잘못된 메시지를 받았을 때 Sniper가 실패를 표시하고 추가 이벤트에 응답하지 않음을 테스트"""
    broken_message = "a broken message"

    # 두 개의 옥션을 시작
    self.auction.start_selling_item()
    self.auction2.start_selling_item()
    self.application.start_bidding_in(self.auction, self.auction2)

    # 첫 번째 옥션에서 정상적인 입찰 진행
    self.auction.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)
    self.auction.report_price(500, 20, "other bidder")
    self.auction.has_received_bid(520, ApplicationRunner.SNIPER_XMPP_ID)

    # 잘못된 메시지 전송
    self.auction.send_invalid_message_containing(broken_message)

    # 실패 상태 표시 확인
    self.application.shows_sniper_has_failed(self.auction)

    # 추가 가격 이벤트 전송
    self.auction.report_price(520, 21, "other bidder")

    # 동기화를 위한 다른 옥션 이벤트 대기
    self.wait_for_another_auction_event()

    # 실패 메시지가 로그에 기록되었는지 확인
    self.application.reports_invalid_message(self.auction, broken_message)

    # 실패 상태가 유지되는지 확인
    self.application.shows_sniper_has_failed(self.auction)

def wait_for_another_auction_event(self):
    """비동기 처리 완료를 확인하기 위한 헬퍼 메서드"""
    self.auction2.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)
    self.auction2.report_price(600, 6, "other bidder")
    self.application.has_shown_sniper_is_bidding(self.auction2, 600, 606)
```

---

### 2. 실패 감지 로직 구현

**핵심 개념**: 실패 감지

**이전 화제와의 관계**: E2E 테스트가 실패하는 상황에서 실제 구현을 시작함

#### AuctionEventListener 인터페이스 확장 (섹션: Detecting the Failure, 라인: 95-102)

- AuctionMessageTranslator에서 메시지 파싱 실패 시 런타임 예외가 발생함
- Smack 라이브러리가 MessageHandler에서 발생한 예외를 무시하므로 직접 처리해야 함
- 새로운 옥션 이벤트 타입을 보고하기 위해 AuctionEventListener 인터페이스에 `auctionFailed()` 메서드 추가

#### 단위 테스트 작성 (섹션: Detecting the Failure, 라인: 103-111)

**참조**: 핵심 개념 - 실패 감지

```java
// 잘못된 메시지를 받았을 때 auctionFailed() 이벤트가 발생하는지 테스트
@Test public void
notifiesAuctionFailedWhenBadMessageReceived() {
  // 리스너가 정확히 한 번 auctionFailed()를 호출받을 것으로 기대
  context.checking(new Expectations() {{
    exactly(1).of(listener).auctionFailed();
  }});

  // 잘못된 메시지 생성 및 처리
  Message message = new Message();
  message.setBody("a bad message");
  translator.processMessage(UNUSED_CHAT, message);
}
```

#### 구현: 예외 처리 (섹션: Detecting the Failure, 라인: 112-124)

**참조**: 핵심 개념 - 실패 감지

```java
// AuctionMessageTranslator에 try/catch 블록 추가
public class AuctionMessageTranslator implements MessageListener {
  public void processMessage(Chat chat, Message message) {
    try {
      // 메시지 파싱 로직을 별도 메서드로 추출
      translate(message.getBody());
    } catch (Exception parseException) {
      // 파싱 실패 시 리스너에게 알림
      listener.auctionFailed();
    }
  }
  // ... translate() 메서드 구현
}
```

#### 불완전한 메시지 처리 (섹션: Detecting the Failure, 라인: 125-153)

**참조**: 핵심 개념 - 실패 감지

- 메시지가 잘 구성되었지만 필수 필드(이벤트 타입, 현재 가격 등)가 누락된 경우도 처리해야 함

```java
// 이벤트 타입이 누락된 경우 테스트
@Test public void
notifiesAuctionFailedWhenEventTypeMissing() {
  context.checking(new Expectations() {{
    exactly(1).of(listener).auctionFailed();
  }});

  Message message = new Message();
  // Event 필드가 누락된 메시지
  message.setBody("SOLVersion: 1.1; CurrentPrice: 234; Increment: 5; Bidder: "
                  + SNIPER_ID + ";");
  translator.processMessage(UNUSED_CHAT, message);
}

// MissingValueException을 정의하여 누락된 값에 대한 예외 처리
public static class AuctionEvent {
  // ...
  private String get(String name) throws MissingValueException {
    String value = values.get(name);
    if (null == value) {
      // 값이 없으면 예외 발생
      throw new MissingValueException(name);
    }
    return value;
  }
}
```

```python
# 파이썬 버전의 실패 감지 구현
class AuctionMessageTranslator:
    """옥션 메시지를 이벤트로 변환하는 클래스"""

    def __init__(self, listener):
        """
        Args:
            listener: AuctionEventListener 인터페이스를 구현한 객체
        """
        self.listener = listener

    def process_message(self, chat, message):
        """메시지를 처리하고 파싱 실패 시 auctionFailed() 이벤트 발생

        Args:
            chat: XMPP Chat 객체 (사용되지 않음)
            message: 처리할 메시지 객체
        """
        try:
            # 메시지 파싱 로직 실행
            self._translate(message.get_body())
        except Exception as parse_exception:
            # 파싱 실패 시 리스너에게 알림
            self.listener.auction_failed()

    def _translate(self, message_body):
        """메시지를 파싱하여 이벤트로 변환

        Args:
            message_body: 메시지 본문 문자열

        Raises:
            MissingValueException: 필수 필드가 누락된 경우
            ValueError: 메시지 형식이 잘못된 경우
        """
        auction_event = self._parse_auction_event(message_body)
        # 이벤트 처리 로직...

class MissingValueException(Exception):
    """필수 값이 누락되었을 때 발생하는 예외"""

    def __init__(self, field_name):
        """
        Args:
            field_name: 누락된 필드 이름
        """
        super().__init__(f"Missing required field: {field_name}")
        self.field_name = field_name
```

---

### 3. 실패 상태 표시 구현

**핵심 개념**: 실패 표시

**이전 화제와의 관계**: 실패 감지가 구현되었으므로 이제 UI에 실패를 표시하는 로직을 구현함

#### AuctionSniper 테스트 작성 (섹션: Displaying the Failure, 라인: 154-174)

**참조**: 핵심 개념 - 실패 표시

```java
// 입찰 중에 옥션 실패가 발생했을 때 테스트
@Test public void
reportsFailedIfAuctionFailsWhenBidding() {
  // 옥션 호출 무시 설정
  ignoringAuction();

  // Sniper가 입찰할 수 있도록 허용
  allowingSniperBidding();

  // "bidding" 상태에서 실패할 것으로 예상
  expectSniperToFailWhenItIs("bidding");

  // 가격 이벤트 처리
  sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);

  // 실패 이벤트 처리
  sniper.auctionFailed();
}

// 실패 예상 헬퍼 메서드
private void expectSniperToFailWhenItIs(final String state) {
  context.checking(new Expectations() {{
    // SniperListener가 FAILED 상태의 SniperSnapshot을 받을 것으로 기대
    // 가격과 입찰 값은 0으로 초기화됨
    atLeast(1).of(sniperListener).sniperStateChanged(
        new SniperSnapshot(ITEM_ID, 0, 0, SniperState.FAILED));
    when(sniperState.is(state));  // 이전 상태 확인
  }});
}
```

#### 구현: 실패 상태 전이 (섹션: Displaying the Failure, 라인: 175-195)

**참조**: 핵심 개념 - 실패 표시

```java
// AuctionSniper에 auctionFailed() 메서드 구현
public class AuctionSniper implements AuctionEventListener {
  public void auctionFailed() {
    // 현재 스냅샷을 실패 상태로 전이
    snapshot = snapshot.failed();

    // 리스너들에게 상태 변경 알림
    listeners.announce().sniperStateChanged(snapshot);
  }
  // ...
}

// SniperSnapshot에 failed() 메서드 추가
public class SniperSnapshot {
  // 실패 상태의 새로운 스냅샷 생성
  // 가격과 입찰 값을 0으로 초기화
  public SniperSnapshot failed() {
    return new SniperSnapshot(itemId, 0, 0, SniperState.FAILED);
  }
  // ...
}
```

#### 테스트 결과 (섹션: Displaying the Failure, 라인: 195-200)

- UI에 실패가 표시됨 (Figure 19.1)
- 하지만 E2E 테스트는 여전히 실패: Sniper가 추가 이벤트 수신을 중단하지 않음

```python
# 파이썬 버전의 실패 표시 구현
from enum import Enum
from typing import List, Protocol

class SniperState(Enum):
    """Sniper의 상태를 나타내는 열거형"""
    JOINING = "Joining"
    BIDDING = "Bidding"
    WINNING = "Winning"
    LOSING = "Losing"
    LOST = "Lost"
    WON = "Won"
    FAILED = "Failed"  # 실패 상태 추가

class SniperListener(Protocol):
    """Sniper 상태 변경을 수신하는 리스너 인터페이스"""

    def sniper_state_changed(self, snapshot: 'SniperSnapshot') -> None:
        """Sniper 상태가 변경되었을 때 호출됨"""
        ...

class SniperSnapshot:
    """Sniper의 현재 상태 스냅샷"""

    def __init__(self, item_id: str, last_price: int, last_bid: int, state: SniperState):
        """
        Args:
            item_id: 아이템 ID
            last_price: 마지막 가격
            last_bid: 마지막 입찰 금액
            state: Sniper 상태
        """
        self.item_id = item_id
        self.last_price = last_price
        self.last_bid = last_bid
        self.state = state

    def failed(self) -> 'SniperSnapshot':
        """실패 상태의 새로운 스냅샷 생성

        Returns:
            가격과 입찰 값이 0으로 초기화된 FAILED 상태의 스냅샷
        """
        return SniperSnapshot(self.item_id, 0, 0, SniperState.FAILED)

class AuctionSniper:
    """옥션 입찰을 담당하는 클래스"""

    def __init__(self, item_id: str, auction, listeners: List[SniperListener]):
        """
        Args:
            item_id: 아이템 ID
            auction: Auction 객체
            listeners: SniperListener 리스트
        """
        self.item_id = item_id
        self.auction = auction
        self.listeners = listeners
        self.snapshot = SniperSnapshot(item_id, 0, 0, SniperState.JOINING)

    def auction_failed(self) -> None:
        """옥션 실패 이벤트 처리

        현재 스냅샷을 실패 상태로 전이하고 리스너들에게 알림
        """
        # 현재 스냅샷을 실패 상태로 전이
        self.snapshot = self.snapshot.failed()

        # 모든 리스너들에게 상태 변경 알림
        for listener in self.listeners:
            listener.sniper_state_changed(self.snapshot)
```

---

### 4. Sniper 연결 해제 구현

**핵심 개념**: 연결 해제

**이전 화제와의 관계**: 실패 상태를 표시했지만, Sniper가 여전히 실패한 옥션으로부터 이벤트를 수신하므로 연결을 해제해야 함

#### 설계 고민 (섹션: Disconnecting the Sniper, 라인: 201-213)

**참조**: 핵심 개념 - 연결 해제

- AuctionMessageTranslator의 `processMessage()` 메서드에서 Chat을 통해 리스너를 제거할 수 있음
- 하지만 두 가지 문제점:
  1. 실제 Chat 객체 생성이 어려움 (Chapter 12 참조)
  2. 클래스 기반 Mock 사용 시 구현에 의존하게 됨 (역할이 아닌 구현에 의존)
  3. AuctionMessageTranslator에 너무 많은 책임 부여 (메시지 번역 + 실패 시 처리)

#### 설계 결정: 별도의 리스너 객체 사용 (섹션: Disconnecting the Sniper, 라인: 216-241)

**참조**: 핵심 개념 - 연결 해제

- 대안: Translator에 별도의 객체를 연결하여 연결 해제 정책을 구현
- 기존 AuctionEventListener 인프라를 재사용

```java
// XMPPAuction 클래스에서 연결 해제 리스너 추가
public final class XMPPAuction implements Auction {
  public XMPPAuction(XMPPConnection connection, String auctionJID) {
    // Translator 생성
    AuctionMessageTranslator translator = translatorFor(connection);

    // Chat 생성
    this.chat = connection.getChatManager().createChat(auctionJID, translator);

    // 연결 해제 리스너 추가
    addAuctionEventListener(chatDisconnectorFor(translator));
  }

  private AuctionMessageTranslator translatorFor(XMPPConnection connection) {
    return new AuctionMessageTranslator(
        connection.getUser(),
        auctionEventListeners.announce()
    );
  }

  // 연결 해제 리스너 생성 메서드
  private AuctionEventListener
  chatDisconnectorFor(final AuctionMessageTranslator translator) {
    return new AuctionEventListener() {
      // auctionFailed() 이벤트 발생 시 Chat에서 translator 제거
      public void auctionFailed() {
        chat.removeMessageListener(translator);
      }

      // 다른 이벤트는 무시
      public void auctionClosed() { /* empty method */ }
      public void currentPrice( /* empty method */ )
    };
  }
  // ...
}
```

#### 테스트 결과 (섹션: Disconnecting the Sniper, 라인: 241)

- E2E 테스트 통과 (일부분)

#### 설계 철학: 단일 책임 원칙 (섹션: The Composition Shell Game, 라인: 242-259)

**참조**: 핵심 개념 - 연결 해제

- 이 설계가 대안(Translator 내에서 Chat 분리)보다 더 복잡해 보일 수 있지만 더 나은 이유:
  - 각 객체가 한 가지 일만 잘 수행함 ("단일 책임 원칙")
  - 시스템 동작은 객체들의 조립에서 나옴
- 집중된 책임은 유지보수성을 향상시킴
  - 관련 없는 기능을 뚫고 필요한 부분을 찾을 필요가 없음
- "거기가 없다"는 느낌(Gertrude Stein)이 들 수 있지만, 경험상 집중된 책임이 더 유지보수하기 쉬움

```python
# 파이썬 버전의 연결 해제 구현
from typing import Protocol, List

class MessageListener(Protocol):
    """메시지 리스너 인터페이스"""

    def process_message(self, chat, message) -> None:
        """메시지 처리"""
        ...

class Chat:
    """XMPP Chat 클래스"""

    def __init__(self):
        """메시지 리스너 목록 초기화 (thread-safe copy-on-write 컬렉션)"""
        self._listeners: List[MessageListener] = []

    def add_message_listener(self, listener: MessageListener) -> None:
        """메시지 리스너 추가"""
        # copy-on-write: 새로운 리스트 생성하여 안전하게 추가
        self._listeners = self._listeners + [listener]

    def remove_message_listener(self, listener: MessageListener) -> None:
        """메시지 리스너 제거

        Args:
            listener: 제거할 리스너

        Note:
            copy-on-write 컬렉션이므로 메시지 처리 중에도 안전하게 제거 가능
        """
        # copy-on-write: 새로운 리스트 생성하여 안전하게 제거
        self._listeners = [l for l in self._listeners if l != listener]

class AuctionEventListener(Protocol):
    """옥션 이벤트 리스너 인터페이스"""

    def auction_failed(self) -> None:
        """옥션 실패 이벤트"""
        ...

    def auction_closed(self) -> None:
        """옥션 종료 이벤트"""
        ...

    def current_price(self, price: int, increment: int, source: str) -> None:
        """현재 가격 이벤트"""
        ...

class ChatDisconnector:
    """Chat 연결 해제를 담당하는 리스너 클래스

    auctionFailed() 이벤트 발생 시 Chat에서 translator를 제거하여
    추가 메시지를 받지 않도록 함
    """

    def __init__(self, chat: Chat, translator):
        """
        Args:
            chat: XMPP Chat 객체
            translator: 제거할 AuctionMessageTranslator
        """
        self.chat = chat
        self.translator = translator

    def auction_failed(self) -> None:
        """옥션 실패 시 Chat에서 translator 제거"""
        self.chat.remove_message_listener(self.translator)

    def auction_closed(self) -> None:
        """옥션 종료 이벤트 무시"""
        pass

    def current_price(self, price: int, increment: int, source: str) -> None:
        """현재 가격 이벤트 무시"""
        pass

class XMPPAuction:
    """XMPP 기반 옥션 구현 클래스"""

    def __init__(self, connection, auction_jid: str):
        """
        Args:
            connection: XMPP 연결 객체
            auction_jid: 옥션 Jabber ID
        """
        self.auction_event_listeners = []

        # Translator 생성
        translator = self._translator_for(connection)

        # Chat 생성
        self.chat = connection.get_chat_manager().create_chat(
            auction_jid,
            translator
        )

        # 연결 해제 리스너 추가
        self.add_auction_event_listener(
            ChatDisconnector(self.chat, translator)
        )

    def _translator_for(self, connection):
        """AuctionMessageTranslator 생성

        Args:
            connection: XMPP 연결 객체

        Returns:
            생성된 AuctionMessageTranslator 인스턴스
        """
        return AuctionMessageTranslator(
            connection.get_user(),
            self._create_event_announcer()
        )

    def _create_event_announcer(self):
        """이벤트 발표자 생성 (모든 리스너에게 브로드캐스트)"""
        class EventAnnouncer:
            def __init__(self, listeners):
                self.listeners = listeners

            def auction_failed(self):
                for listener in self.listeners:
                    listener.auction_failed()

            def auction_closed(self):
                for listener in self.listeners:
                    listener.auction_closed()

            def current_price(self, price, increment, source):
                for listener in self.listeners:
                    listener.current_price(price, increment, source)

        return EventAnnouncer(self.auction_event_listeners)

    def add_auction_event_listener(self, listener: AuctionEventListener) -> None:
        """옥션 이벤트 리스너 추가"""
        self.auction_event_listeners.append(listener)
```

---

### 5. 실패 기록 테스트 작성

**핵심 개념**: 실패 기록

**이전 화제와의 관계**: 실패 감지, 표시, 연결 해제가 구현되었으므로 이제 운영팀이 복구할 수 있도록 로그에 기록하는 기능을 추가함

#### 요구사항 (섹션: Recording the Failure, 라인: 260-265)

**참조**: 핵심 개념 - 실패 기록

- Sniper 애플리케이션은 사용자 조직이 상황을 복구할 수 있도록 실패에 대한 메시지를 로그에 기록해야 함
- 테스트는 로그 파일을 찾아 내용을 확인해야 함

#### 테스트 구현 (섹션: Filling In the Test, 라인: 266-306)

**참조**: 핵심 개념 - 실패 기록

```java
// ApplicationRunner 클래스에 로그 검증 추가
public class ApplicationRunner {
  // ...
  private AuctionLogDriver logDriver = new AuctionLogDriver();

  // 로그에 잘못된 메시지가 기록되었는지 확인
  public void reportsInvalidMessage(FakeAuctionServer auction, String message)
    throws IOException
  {
    logDriver.hasEntry(containsString(message));
  }

  public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
    startSniper();
    openBiddingFor(auction, stopPrice);
  }

  // Sniper 시작 전 로그 파일 초기화
  private startSniper() {
    logDriver.clearLog();  // 로그 초기화
    Thread thread = new Thread("Test Application") {
      @Override public void run() {
        // Start the application ...
      }
    };
  }
}

// 로그 파일 관리 클래스
public class AuctionLogDriver {
  public static final String LOG_FILE_NAME = "auction-sniper.log";
  private final File logFile = new File(LOG_FILE_NAME);

  // 로그 파일에 특정 패턴의 항목이 있는지 확인
  public void hasEntry(Matcher<String> matcher) throws IOException {
    // Apache Commons IO 라이브러리 사용
    assertThat(FileUtils.readFileToString(logFile), matcher);
  }

  // 로그 파일 초기화
  public void clearLog() {
    logFile.delete();
    // LogManager 리셋 (캐시된 로거 혼란 방지)
    LogManager.getLogManager().reset();
  }
}
```

#### 테스트의 목적 (섹션: Filling In the Test, 라인: 300-303)

- 이 테스트는 메시지가 시스템을 통해 어떤 로그 레코드로 전달되었는지만 확인함 (조각들이 맞춰졌는지 확인)
- 로그 레코드의 내용에 대한 더 철저한 테스트는 나중에 작성함
- E2E 테스트는 로그 파일이 없어서 실패함

```python
# 파이썬 버전의 로그 테스트 구현
import os
import logging
from pathlib import Path
from typing import Callable

class AuctionLogDriver:
    """로그 파일 관리 및 검증 클래스"""

    LOG_FILE_NAME = "auction-sniper.log"

    def __init__(self):
        """로그 파일 경로 초기화"""
        self.log_file = Path(self.LOG_FILE_NAME)

    def has_entry(self, matcher: Callable[[str], bool]) -> None:
        """로그 파일에 특정 패턴의 항목이 있는지 확인

        Args:
            matcher: 로그 내용을 검증하는 함수 (예: lambda x: "error" in x)

        Raises:
            AssertionError: 로그에 매칭되는 항목이 없는 경우
            FileNotFoundError: 로그 파일이 없는 경우
        """
        if not self.log_file.exists():
            raise FileNotFoundError(f"Log file not found: {self.log_file}")

        log_content = self.log_file.read_text(encoding='utf-8')
        assert matcher(log_content), f"Log content does not match: {log_content}"

    def clear_log(self) -> None:
        """로그 파일 초기화 및 로거 리셋

        Note:
            - 로그 파일을 삭제하면 캐시된 로거가 혼란스러울 수 있으므로
              LogManager를 리셋함 (같은 주소 공간에 있다는 가정)
        """
        # 로그 파일 삭제
        if self.log_file.exists():
            self.log_file.unlink()

        # 로거 리셋 (모든 핸들러 제거)
        logging.shutdown()
        # 루트 로거의 핸들러 제거
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

class ApplicationRunner:
    """애플리케이션 실행 및 테스트 헬퍼 클래스"""

    def __init__(self):
        """로그 드라이버 초기화"""
        self.log_driver = AuctionLogDriver()

    def reports_invalid_message(self, auction, message: str) -> None:
        """로그에 잘못된 메시지가 기록되었는지 확인

        Args:
            auction: FakeAuctionServer 인스턴스
            message: 확인할 메시지 내용
        """
        # 로그에 메시지가 포함되어 있는지 확인
        self.log_driver.has_entry(lambda content: message in content)

    def start_bidding_with_stop_price(self, auction, stop_price: int) -> None:
        """입찰 시작

        Args:
            auction: FakeAuctionServer 인스턴스
            stop_price: 최대 입찰 가격
        """
        self._start_sniper()
        self._open_bidding_for(auction, stop_price)

    def _start_sniper(self) -> None:
        """Sniper 애플리케이션 시작 전 로그 초기화"""
        # 로그 파일 초기화
        self.log_driver.clear_log()

        # 애플리케이션 시작 (별도 스레드)
        # ... 애플리케이션 시작 로직

# 사용 예제
def test_reports_invalid_message():
    """로그 기록 테스트 예제"""
    app_runner = ApplicationRunner()

    # 로그 초기화
    app_runner.log_driver.clear_log()

    # 잘못된 메시지 처리 후 로그 확인
    broken_message = "a broken message"
    # ... 애플리케이션에서 메시지 처리

    # 로그에 잘못된 메시지가 기록되었는지 확인
    app_runner.reports_invalid_message(None, broken_message)
```

---

### 6. 실패 리포터 구현

**핵심 개념**: 실패 기록

**이전 화제와의 관계**: 로그 테스트가 준비되었으므로 이제 실제로 로그를 기록하는 리포터를 구현함

#### XMPPFailureReporter 인터페이스 정의 (섹션: Failure Reporting in the Translator, 라인: 307-318)

**참조**: 핵심 개념 - 실패 기록

- "단일 책임 원칙"에 따라 AuctionMessageTranslator는 이벤트 보고 방법을 결정하지 않아야 함
- 새로운 협력자 XMPPFailureReporter를 발명하여 이 작업 처리

```java
// 실패 리포터 인터페이스
public interface XMPPFailureReporter {
  // 메시지 번역 실패를 보고
  void cannotTranslateMessage(String auctionId, String failedMessage,
                              Exception exception);
}
```

#### 기존 테스트 수정 (섹션: Failure Reporting in the Translator, 라인: 319-339)

**참조**: 핵심 개념 - 실패 기록

```java
// 기존 실패 테스트를 헬퍼 메서드를 사용하도록 수정
@Test public void
notifiesAuctionFailedWhenBadMessageReceived() {
  String badMessage = "a bad message";
  expectFailureWithMessage(badMessage);
  translator.processMessage(UNUSED_CHAT, message(badMessage));
}

// 메시지 생성 헬퍼 메서드
private Message message(String body) {
  Message message = new Message();
  message.setBody(body);
  return message;
}

// 실패 예상 헬퍼 메서드
private void expectFailureWithMessage(final String badMessage) {
  context.checking(new Expectations() {{
    // 리스너가 auctionFailed() 호출받을 것으로 기대
    oneOf(listener).auctionFailed();

    // 실패 리포터가 cannotTranslateMessage() 호출받을 것으로 기대
    oneOf(failureReporter).cannotTranslateMessage(
        with(SNIPER_ID),           // 옥션 ID
        with(badMessage),           // 실패한 메시지
        with(any(Exception.class))  // 발생한 예외
    );
  }});
}
```

#### AuctionMessageTranslator 수정 (섹션: Failure Reporting in the Translator, 라인: 340-354)

**참조**: 핵심 개념 - 실패 기록

```java
// 실패 리포터를 생성자를 통해 주입받고 사용
public class AuctionMessageTranslator implements MessageListener {
  private final String sniperId;
  private final AuctionEventListener listener;
  private final XMPPFailureReporter failureReporter;  // 새로 추가

  public AuctionMessageTranslator(String sniperId,
                                  AuctionEventListener listener,
                                  XMPPFailureReporter failureReporter) {
    this.sniperId = sniperId;
    this.listener = listener;
    this.failureReporter = failureReporter;
  }

  public void processMessage(Chat chat, Message message) {
    String messageBody = message.getBody();  // 예외 발생하지 않음
    try {
      translate(messageBody);
    } catch (RuntimeException exception) {
      // 리스너에게 알리기 전에 실패 리포터 호출
      failureReporter.cannotTranslateMessage(sniperId, messageBody, exception);
      listener.auctionFailed();
    }
  }
  // ...
}
```

#### LoggingXMPPFailureReporter 테스트 작성 (섹션: Generating the Log Message, 라인: 360-396)

**참조**: 핵심 개념 - 실패 기록

- 파일 접근은 E2E 테스트에서 충분히 다루므로, 메모리에서 실행하여 의존성 줄임
- Java 로깅 프레임워크에는 인터페이스가 없으므로 클래스 기반 Mock 사용 (예외적)

```java
@RunWith(JMock.class)
public class LoggingXMPPFailureReporterTest {
  // 클래스 기반 Mock 활성화
  private final Mockery context = new Mockery() {{
    setImposteriser(ClassImposteriser.INSTANCE);
  }};

  // Logger 클래스의 Mock 생성
  final Logger logger = context.mock(Logger.class);
  final LoggingXMPPFailureReporter reporter =
      new LoggingXMPPFailureReporter(logger);

  // 모든 테스트 실행 후 로깅 환경 초기화
  @AfterClass
  public static void resetLogging() {
    LogManager.getLogManager().reset();
  }

  @Test public void
  writesMessageTranslationFailureToLog() {
    context.checking(new Expectations() {{
      // Logger의 severe() 메서드가 특정 형식의 메시지로 호출될 것으로 기대
      oneOf(logger).severe(
          "<auction id> "
          + "Could not translate message \"bad message\" "
          + "because \"java.lang.Exception: bad\""
      );
    }});

    // 실패 메시지 기록
    reporter.cannotTranslateMessage(
        "auction id",
        "bad message",
        new Exception("bad")
    );
  }
}

// 구현: 입력값들로 포맷된 문자열을 로거에 전달
public class LoggingXMPPFailureReporter implements XMPPFailureReporter {
  private final Logger logger;

  public LoggingXMPPFailureReporter(Logger logger) {
    this.logger = logger;
  }

  public void cannotTranslateMessage(String auctionId,
                                    String failedMessage,
                                    Exception exception) {
    logger.severe(String.format(
        "<%s> Could not translate message \"%s\" because \"%s\"",
        auctionId,
        failedMessage,
        exception
    ));
  }
}
```

#### 클래스 Mock 사용 정당화 (섹션: Breaking Our Own Rules?, 라인: 399-419)

**참조**: 핵심 개념 - 실패 기록

- 일반적으로 클래스 Mock을 좋아하지 않지만, 이 경우는 예외:
  1. 테스트하려는 것: 심각도 수준과 함께 실패 메시지 렌더링
  2. 클래스가 매우 제한적: 로깅 레이어 위의 shim일 뿐
  3. 다른 수준의 간접 참조를 도입할 가치가 없음
  4. 실제 파일 사용 시 의존성과 비동기성이 발생하여 기능 개발과 무관함
  5. Java 런타임의 일부로서 로깅 API는 변경될 가능성이 낮음

- 하지만:
  1. 내부 코드의 클래스에는 하지 않음 (인터페이스 작성 가능)
  2. LoggingXMPPFailureReporter가 복잡해지면 메시지 포맷터 클래스를 발견하여 직접 테스트할 것

```python
# 파이썬 버전의 실패 리포터 구현
import logging
from typing import Protocol
from unittest.mock import Mock
import pytest

class XMPPFailureReporter(Protocol):
    """실패 리포터 인터페이스"""

    def cannot_translate_message(self, auction_id: str,
                                 failed_message: str,
                                 exception: Exception) -> None:
        """메시지 번역 실패를 보고

        Args:
            auction_id: 옥션 ID
            failed_message: 번역 실패한 메시지
            exception: 발생한 예외
        """
        ...

class LoggingXMPPFailureReporter:
    """로깅 기반 실패 리포터 구현

    실패 정보를 로거를 통해 심각도 수준과 함께 기록함
    """

    def __init__(self, logger: logging.Logger):
        """
        Args:
            logger: 사용할 Logger 인스턴스
        """
        self.logger = logger

    def cannot_translate_message(self, auction_id: str,
                                 failed_message: str,
                                 exception: Exception) -> None:
        """메시지 번역 실패를 로그에 기록

        Args:
            auction_id: 옥션 ID
            failed_message: 번역 실패한 메시지
            exception: 발생한 예외
        """
        message = (
            f"<{auction_id}> "
            f"Could not translate message \"{failed_message}\" "
            f"because \"{exception.__class__.__name__}: {exception}\""
        )
        self.logger.error(message)

# 테스트 코드
class TestLoggingXMPPFailureReporter:
    """LoggingXMPPFailureReporter 테스트"""

    @pytest.fixture
    def mock_logger(self):
        """Mock Logger 생성"""
        return Mock(spec=logging.Logger)

    @pytest.fixture
    def reporter(self, mock_logger):
        """테스트용 Reporter 생성"""
        return LoggingXMPPFailureReporter(mock_logger)

    def test_writes_message_translation_failure_to_log(self, reporter, mock_logger):
        """메시지 번역 실패가 로그에 기록되는지 테스트"""
        # 테스트 데이터
        auction_id = "auction id"
        bad_message = "bad message"
        exception = Exception("bad")

        # 실행
        reporter.cannot_translate_message(auction_id, bad_message, exception)

        # 검증: Logger의 error() 메서드가 올바른 형식으로 호출되었는지 확인
        expected_message = (
            f"<{auction_id}> "
            f"Could not translate message \"{bad_message}\" "
            f"because \"Exception: {exception}\""
        )
        mock_logger.error.assert_called_once_with(expected_message)

# 사용 예제
def create_failure_reporter() -> LoggingXMPPFailureReporter:
    """프로덕션용 실패 리포터 생성"""
    # 로거 설정
    logger = logging.getLogger("auction-sniper")
    logger.setLevel(logging.ERROR)

    # 파일 핸들러 추가
    handler = logging.FileHandler("auction-sniper.log")
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)

    return LoggingXMPPFailureReporter(logger)
```

---

### 7. 전체 통합 및 관찰

**핵심 개념**: 실패 기록

**이전 화제와의 관계**: 모든 조각이 준비되었으므로 이제 전체 시스템을 통합하여 E2E 테스트를 통과시킴

#### XMPPAuctionHouse 통합 (섹션: Closing the Loop, 라인: 420-456)

**참조**: 핵심 개념 - 실패 기록

```java
// XMPPAuctionHouse에 LoggingXMPPFailureReporter 연결
public class XMPPAuctionHouse implements AuctionHouse {
  private final XMPPConnection connection;
  private final XMPPFailureReporter failureReporter;

  public XMPPAuctionHouse(XMPPConnection connection)
    throws XMPPAuctionException
  {
    this.connection = connection;
    // 로거 생성 및 실패 리포터 초기화
    this.failureReporter = new LoggingXMPPFailureReporter(makeLogger());
  }

  public Auction auctionFor(String itemId) {
    // XMPPAuction 생성 시 failureReporter 전달
    return new XMPPAuction(
        connection,
        auctionId(itemId, connection),
        failureReporter
    );
  }

  // Logger 생성 메서드
  private Logger makeLogger() throws XMPPAuctionException {
    Logger logger = Logger.getLogger(LOGGER_NAME);
    logger.setUseParentHandlers(false);  // 부모 핸들러 사용 안 함
    logger.addHandler(simpleFileHandler());
    return logger;
  }

  // 파일 핸들러 생성
  private FileHandler simpleFileHandler() throws XMPPAuctionException {
    try {
      FileHandler handler = new FileHandler(LOG_FILE_NAME);
      handler.setFormatter(new SimpleFormatter());  // 간단한 포맷터 사용
      return handler;
    } catch (Exception e) {
      throw new XMPPAuctionException(
          "Could not create logger FileHandler " + getFullPath(LOG_FILE_NAME),
          e
      );
    }
  }
  // ...
}
```

#### 테스트 결과 (섹션: Closing the Loop, 라인: 457-461)

- E2E 테스트 완전히 통과
- Figure 19.2: Sniper가 옥션으로부터의 실패 메시지를 보고함

#### 관찰: "역 살라미" 개발 (섹션: "Inverse Salami" Development, 라인: 462-486)

**참조**: 모든 핵심 개념

- 소프트웨어를 점진적으로 성장시키는 리듬: 얇지만 일관된 조각으로 기능 추가
- 각 새 기능에 대해:
  1. 기능이 무엇을 해야 하는지 보여주는 테스트 작성
  2. 각 테스트를 통과하기에 충분한 코드만 변경
  3. 새 기능을 위한 공간을 열거나 새로운 개념을 드러내기 위해 코드 재구조화
  4. 출시
- 정적 언어(Java, C#)에서 컴파일러를 사용하여 구현 의존성 체인 탐색:
  1. 새 트리거 이벤트를 받도록 코드 변경
  2. 무엇이 깨지는지 확인
  3. 그 깨진 부분 수정
  4. 그 변경이 무엇을 깨뜨리는지 확인
  5. 기능이 작동할 때까지 반복
- 핵심 기술: 요구사항을 점진적 조각으로 나누는 방법 학습
  - 항상 무언가 작동하도록 유지
  - 항상 한 가지 기능만 추가
  - 과정은 끊임없이 진행되어야 함

#### 관찰: 의도를 표현하는 작은 메서드 (섹션: Small Methods to Express Intent, 라인: 487-498)

**참조**: 핵심 개념 - 연결 해제

- 작은 양의 코드를 래핑하는 헬퍼 메서드를 작성하는 습관의 두 가지 이유:
  1. Java와 같은 언어가 강제하는 구문적 노이즈 감소
     - 예: `translatorFor()` 메서드로 같은 줄에 "AuctionMessageTranslator"를 두 번 타이핑하지 않음
  2. 명확한 이름을 구조에 부여
     - 예: `chatDisconnectorFor()`가 익명 클래스의 역할을 설명
- 목표: 각 수준의 코드를 가능한 한 읽기 쉽고 자기 설명적으로 만들기
  - Java 구문을 실제로 사용해야 할 때까지 이 과정 반복

#### 관찰: 로깅도 기능이다 (섹션: Logging Is Also a Feature, 라인: 499-513)

**참조**: 핵심 개념 - 실패 기록

- XMPPFailureReporter를 정의하여 AuctionMessageTranslator의 실패 보고를 패키지화
- 많은 팀이 이것을 과도한 설계로 간주하고 그냥 로그 메시지를 제자리에 작성함
- 하지만 이는 같은 코드에서 수준(메시지 번역과 로깅)을 혼합하여 설계를 약화시킴
- 프로덕션 로깅은 외부 인터페이스:
  - 현재 구현 구조가 아닌, 그것에 의존할 사람들의 요구사항에 의해 주도되어야 함
- 호출자의 용어로 런타임 보고를 설명하면:
  - 더 유용한 로그를 얻게 됨
  - 로깅 인프라가 코드 전체에 흩어지지 않고 명확히 격리됨
  - 작업하기 더 쉬워짐

```python
# 파이썬 버전의 전체 통합 코드
import logging
from pathlib import Path
from typing import Optional

class XMPPAuctionException(Exception):
    """XMPP 옥션 관련 예외"""
    pass

class XMPPAuctionHouse:
    """XMPP 기반 옥션 하우스

    모든 XMPPAuction 인스턴스에 대해 공통 실패 리포터를 제공
    """

    LOGGER_NAME = "auction-sniper"
    LOG_FILE_NAME = "auction-sniper.log"

    def __init__(self, connection):
        """
        Args:
            connection: XMPP 연결 객체

        Raises:
            XMPPAuctionException: 로거 초기화 실패 시
        """
        self.connection = connection
        # 로거 생성 및 실패 리포터 초기화
        self.failure_reporter = LoggingXMPPFailureReporter(
            self._make_logger()
        )

    def auction_for(self, item_id: str):
        """특정 아이템에 대한 옥션 생성

        Args:
            item_id: 아이템 ID

        Returns:
            생성된 XMPPAuction 인스턴스
        """
        auction_id = self._auction_id(item_id)
        return XMPPAuction(
            self.connection,
            auction_id,
            self.failure_reporter  # 모든 옥션이 같은 리포터 공유
        )

    def _make_logger(self) -> logging.Logger:
        """Logger 인스턴스 생성 및 설정

        Returns:
            설정된 Logger 인스턴스

        Raises:
            XMPPAuctionException: 로거 초기화 실패 시
        """
        logger = logging.getLogger(self.LOGGER_NAME)
        logger.setLevel(logging.ERROR)

        # 부모 핸들러 사용하지 않음 (중복 로깅 방지)
        logger.propagate = False

        # 파일 핸들러 추가
        logger.addHandler(self._simple_file_handler())

        return logger

    def _simple_file_handler(self) -> logging.FileHandler:
        """파일 핸들러 생성

        Returns:
            설정된 FileHandler 인스턴스

        Raises:
            XMPPAuctionException: 파일 핸들러 생성 실패 시
        """
        try:
            handler = logging.FileHandler(self.LOG_FILE_NAME)
            # 간단한 포맷터 사용
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            return handler
        except Exception as e:
            full_path = Path(self.LOG_FILE_NAME).absolute()
            raise XMPPAuctionException(
                f"Could not create logger FileHandler {full_path}"
            ) from e

    def _auction_id(self, item_id: str) -> str:
        """아이템 ID로부터 옥션 ID 생성

        Args:
            item_id: 아이템 ID

        Returns:
            옥션 Jabber ID
        """
        # 실제 구현은 연결 정보를 사용하여 옥션 JID 생성
        return f"{item_id}@auction.server.com"

class XMPPAuction:
    """XMPP 기반 개별 옥션 인스턴스"""

    def __init__(self, connection, auction_jid: str, failure_reporter):
        """
        Args:
            connection: XMPP 연결 객체
            auction_jid: 옥션 Jabber ID
            failure_reporter: XMPPFailureReporter 인스턴스
        """
        self.auction_event_listeners = []

        # Translator 생성 (실패 리포터 주입)
        translator = AuctionMessageTranslator(
            connection.get_user(),
            self._create_event_announcer(),
            failure_reporter  # 실패 리포터 전달
        )

        # Chat 생성
        self.chat = connection.get_chat_manager().create_chat(
            auction_jid,
            translator
        )

        # 연결 해제 리스너 추가
        self.add_auction_event_listener(
            ChatDisconnector(self.chat, translator)
        )

    def _create_event_announcer(self):
        """이벤트 발표자 생성"""
        # ... 이벤트 발표자 구현
        pass

    def add_auction_event_listener(self, listener) -> None:
        """옥션 이벤트 리스너 추가"""
        self.auction_event_listeners.append(listener)

# 실제 사용 예제
def main():
    """애플리케이션 메인 함수"""
    # XMPP 연결 생성
    connection = create_xmpp_connection()

    try:
        # 옥션 하우스 생성 (로거 자동 초기화)
        auction_house = XMPPAuctionHouse(connection)

        # 특정 아이템에 대한 옥션 생성
        auction = auction_house.auction_for("item-12345")

        # 옥션 사용...

    except XMPPAuctionException as e:
        print(f"Failed to initialize auction house: {e}")
        raise
```

## 요약

이 장은 TDD 방식으로 완전한 실패 처리 시스템을 구축하는 과정을 보여줌:

1. **E2E 테스트로 시작**: 전체 실패 시나리오를 정의하고 테스트 작성
2. **단위 테스트로 구현**: 각 컴포넌트를 독립적으로 테스트하며 구현
3. **단일 책임 원칙 준수**: 각 클래스가 하나의 명확한 역할만 수행
4. **점진적 통합**: 작은 조각들을 점진적으로 통합하여 전체 기능 완성
5. **리팩토링**: 코드를 읽기 쉽고 유지보수하기 쉽게 지속적으로 개선

핵심 교훈:
- 실패 처리도 하나의 기능으로 취급하여 테스트해야 함
- 로깅은 외부 인터페이스로, 구현이 아닌 사용자의 요구사항에 의해 주도되어야 함
- 작은 메서드와 명확한 이름으로 코드의 의도를 표현함
- 점진적 개발 리듬을 유지하며 항상 무언가 작동하도록 유지함
