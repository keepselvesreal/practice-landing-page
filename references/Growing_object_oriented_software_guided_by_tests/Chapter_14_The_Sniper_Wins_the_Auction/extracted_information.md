<!--
생성 시간: 2025-10-05 14:05:06 KST
핵심 내용: Sniper가 경매에서 승리하는 기능을 추가하면서 상태(state) 개념을 도입하고, 테스트를 통해 상태 전이를 검증하는 방법을 학습
상세 내용:
  - 압축 내용 (라인 1-3): 장 개요
  - 핵심 내용 (라인 4-20): 핵심 개념과 관계
  - 상세 내용 (라인 21-끝): 화제별 설명
상태: active
참조: content.md
-->

# 14장: Sniper가 경매에서 승리하다

## 압축 내용
Sniper에 상태(state) 개념을 도입하여 경매 승리 기능을 추가하고, 콜백 리스너를 통해 상태 전이를 테스트하며, 이전 리팩토링이 새 기능 추가에 어떻게 기여하는지 확인하는 과정

## 핵심 내용

### 핵심 개념들
1. **상태 기반 테스트 (State-Based Testing)** - [상세: 테스트에서 상태 표현하기, Sniper의 상태 획득]
2. **가치 타입 (Value Type)** - [상세: 입찰자 정보 처리]
3. **책임 분리 (Separation of Concerns)** - [상세: 입찰자 정보 처리, Sniper의 상태 획득]
4. **jMock States 메커니즘** - [상세: 테스트에서 상태 표현하기]
5. **TDD 점진적 개발** - [상세: 실패하는 테스트 작성, Sniper의 승리, 안정적인 진행]

### 핵심 개념 간 관계

```
TDD 점진적 개발
    │
    ├─→ 실패하는 테스트 작성
    │       │
    │       └─→ 상태 기반 테스트 필요성 도출
    │
    ├─→ 책임 분리를 통한 구현
    │       │
    │       ├─→ 가치 타입(PriceSource) 도입
    │       └─→ 입찰자 정보를 translator에서 처리
    │
    └─→ 상태 기반 테스트 구현
            │
            ├─→ jMock States로 상태 표현
            └─→ 점진적으로 상태 전이 추가
```

**개념 간 관계 설명:**
- **TDD 점진적 개발**이 전체 개발 방식을 주도하며, 실패하는 테스트부터 시작
- **책임 분리** 원칙에 따라 **가치 타입(PriceSource)**을 도입하여 도메인 의미를 명확히 표현
- **상태 기반 테스트**를 위해 **jMock States** 메커니즘을 활용하여 캡슐화를 유지하면서 상태 검증
- 이전 챕터에서의 **책임 분리** 리팩토링이 새로운 기능 추가를 용이하게 만듦

## 상세 내용

### 화제 목차
1. 실패하는 테스트 작성 (First, a Failing Test) - 라인 9-51
2. 입찰자 정보 처리 (Who Knows about Bidders?) - 라인 52-162
3. Sniper의 더 많은 메시지 (The Sniper Has More to Say) - 라인 165-225
4. Sniper의 상태 획득 (The Sniper Acquires Some State) - 라인 226-321
5. Sniper의 승리 (The Sniper Wins) - 라인 322-393
6. 안정적인 진행 (Making Steady Progress) - 라인 397-407

---

### 1. 실패하는 테스트 작성 (First, a Failing Test)
**라인 9-51 | content.md**

**이전 화제와의 관계:** 새로운 장의 시작, 이전 챕터에서 구축한 Sniper가 가격 변동에 입찰하는 기능을 확장

**핵심 개념 참조:**
- [상태 기반 테스트]: 승리 상태 전이를 검증하는 테스트 작성
- [TDD 점진적 개발]: 실패하는 테스트부터 시작

**설명:**

Sniper가 경매에서 승리하는 기능을 추가하기 위해 먼저 End-to-End 테스트를 작성한다. 기존의 `sniperMakesAHigherBidButLoses()` 테스트를 기반으로 다른 결말을 가진 `sniperWinsAnAuctionByBiddingHigher()` 테스트를 추가한다.

새로운 상태 전이는 다음과 같다:
- Joining → Bidding → **Winning** → **Won**

**코드:**

```java
// Java 코드 (라인 22-36)
public class AuctionSniperEndToEndTest {
  // [...]

  @Test public void
  sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);

    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding();

    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);  // Sniper의 가격이 수락됨
    application.hasShownSniperIsWinning();  // 승리 중 상태 확인

    auction.announceClosed();
    application.showsSniperHasWonAuction();  // 최종 승리 확인
  }
}
```

```python
# Python 버전
class AuctionSniperEndToEndTest:
    # [...]

    def test_sniper_wins_an_auction_by_bidding_higher(self):
        """Sniper가 더 높은 입찰로 경매에서 승리하는 시나리오"""
        auction.start_selling_item()
        application.start_bidding_in(auction)
        auction.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)

        auction.report_price(1000, 98, "other bidder")
        application.has_shown_sniper_is_bidding()

        auction.has_received_bid(1098, ApplicationRunner.SNIPER_XMPP_ID)
        auction.report_price(1098, 97, ApplicationRunner.SNIPER_XMPP_ID)  # Sniper의 가격이 수락됨
        application.has_shown_sniper_is_winning()  # 승리 중 상태 확인

        auction.announce_closed()
        application.shows_sniper_has_won_auction()  # 최종 승리 확인
```

**테스트 실패 메시지 (라인 40-50):**

```
java.lang.AssertionError:
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Winning"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Bidding"  # 기대: "Winning", 실제: "Bidding"
```

---

### 2. 입찰자 정보 처리 (Who Knows about Bidders?)
**라인 52-162 | content.md**

**이전 화제와의 관계:** 실패하는 테스트를 통과시키기 위한 구현 시작, 설계 결정이 필요한 시점

**핵심 개념 참조:**
- [가치 타입]: PriceSource enum 도입
- [책임 분리]: translator가 입찰자 정보를 처리하도록 결정
- [TDD 점진적 개발]: 책임 할당 결정 후 테스트 작성

**설명:**

Sniper가 승리 중인지 판단하려면 마지막 가격이 자신의 입찰인지 알아야 한다. 이 로직을 어디에 둘지 설계 결정이 필요하다.

**설계 결정:**
- Sniper가 XMPP 상세 정보를 알 필요 없도록 translator가 입찰자 정보를 처리
- Sniper는 "이 가격이 나로부터 왔는가?"라는 선택지만 필요
- 이를 `PriceSource` enum으로 표현 (FromSniper, FromOtherBidder)

**가치 타입의 이점:**
- boolean 대신 도메인 의미를 명확히 표현
- 코드를 읽을 때마다 해석할 필요 없음

**코드:**

```java
// PriceSource enum 정의 (라인 72-75)
public interface AuctionEventListener extends EventListener {
  enum PriceSource {
    FromSniper, FromOtherBidder;
  };
  // [...]
}
```

```python
# Python 버전
from enum import Enum, auto

class PriceSource(Enum):
    """가격이 어디서 왔는지 표현하는 가치 타입"""
    FROM_SNIPER = auto()
    FROM_OTHER_BIDDER = auto()

class AuctionEventListener:
    """경매 이벤트 리스너 인터페이스"""
    pass
```

```java
// Translator 테스트 - 다른 입찰자의 가격 (라인 83-96)
public class AuctionMessageTranslatorTest {
  // [...]
  private final AuctionMessageTranslator translator =
                    new AuctionMessageTranslator(SNIPER_ID, listener);

  @Test public void
  notifiesBidDetailsWhenCurrentPriceMessageReceivedFromOtherBidder() {
    context.checking(new Expectations() {{
      exactly(1).of(listener).currentPrice(192, 7, PriceSource.FromOtherBidder);
    }});

    Message message = new Message();
    message.setBody(
      "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
    );
    translator.processMessage(UNUSED_CHAT, message);
  }
}
```

```python
# Python 버전
class AuctionMessageTranslatorTest:
    def setup_method(self):
        self.translator = AuctionMessageTranslator(SNIPER_ID, self.listener)

    def test_notifies_bid_details_when_current_price_message_received_from_other_bidder(self):
        """다른 입찰자의 가격 메시지를 받으면 FromOtherBidder로 알림"""
        # Mock 설정
        self.listener.should_receive('current_price').once().with_args(
            192, 7, PriceSource.FROM_OTHER_BIDDER
        )

        message = Message()
        message.set_body(
            "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
        )
        self.translator.process_message(UNUSED_CHAT, message)
```

```java
// Translator 테스트 - Sniper의 가격 (라인 97-107)
@Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceivedFromSniper() {
  context.checking(new Expectations() {{
    exactly(1).of(listener).currentPrice(234, 5, PriceSource.FromSniper);
  }});

  Message message = new Message();
  message.setBody(
    "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: "
    + SNIPER_ID + ";"
  );
  translator.processMessage(UNUSED_CHAT, message);
}
```

```python
# Python 버전
def test_notifies_bid_details_when_current_price_message_received_from_sniper(self):
    """Sniper 자신의 가격 메시지를 받으면 FromSniper로 알림"""
    # Mock 설정
    self.listener.should_receive('current_price').once().with_args(
        234, 5, PriceSource.FROM_SNIPER
    )

    message = Message()
    message.set_body(
        f"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: {SNIPER_ID};"
    )
    self.translator.process_message(UNUSED_CHAT, message)
```

**테스트 실패 메시지 (라인 117-125):**

```
unexpected invocation:
  auctionEventListener.currentPrice(<192>, <7>, <FromOtherBidder>)
expectations:
! expected once, never invoked:
    auctionEventListener.currentPrice(<192>, <7>, <FromSniper>)
      parameter 0 matched: <192>
      parameter 1 matched: <7>
      parameter 2 did not match: <FromSniper>, because was <FromOtherBidder>
what happened before this: nothing!
```

**Translator 구현 (라인 127-143):**

```java
public class AuctionMessageTranslator implements MessageListener {
  // [...]
  private final String sniperId;

  public void processMessage(Chat chat, Message message) {
    // [...]
    } else if (EVENT_TYPE_PRICE.equals(type)) {
      listener.currentPrice(event.currentPrice(),
                            event.increment(),
                            event.isFrom(sniperId));  // sniperId와 비교
    }
  }

  public static class AuctionEvent {
    // [...]

    public PriceSource isFrom(String sniperId) {
      // 입찰자가 sniperId와 같으면 FromSniper, 아니면 FromOtherBidder
      return sniperId.equals(bidder()) ? FromSniper : FromOtherBidder;
    }

    private String bidder() {
      return get("Bidder");
    }
  }
}
```

```python
# Python 버전
class AuctionMessageTranslator:
    """경매 메시지를 번역하는 클래스"""

    def __init__(self, sniper_id: str, listener):
        self.sniper_id = sniper_id
        self.listener = listener

    def process_message(self, chat, message):
        """메시지를 처리하여 리스너에 알림"""
        event = AuctionEvent.from_message(message)
        event_type = event.type()

        # [...]
        if event_type == EVENT_TYPE_PRICE:
            self.listener.current_price(
                event.current_price(),
                event.increment(),
                event.is_from(self.sniper_id)  # sniper_id와 비교
            )

    class AuctionEvent:
        # [...]

        def is_from(self, sniper_id: str) -> PriceSource:
            """입찰자가 sniper인지 확인하여 PriceSource 반환"""
            return (PriceSource.FROM_SNIPER
                    if sniper_id == self.bidder()
                    else PriceSource.FROM_OTHER_BIDDER)

        def bidder(self) -> str:
            """메시지에서 입찰자 정보 추출"""
            return self.get("Bidder")
```

**리팩토링의 효과 (라인 144-147):**
이전 챕터 "Tidying Up the Translator"에서 translator 내 책임을 분리한 덕분에 `AuctionEvent`에 메서드 몇 개만 추가하여 매우 가독성 높은 솔루션을 얻을 수 있었다.

**Main 클래스 수정 (라인 148-159):**

```java
private void joinAuction(XMPPConnection connection, String itemId) {
  // [...]
  Auction auction = new XMPPAuction(chat);
  chat.addMessageListener(
    new AuctionMessageTranslator(
      connection.getUser(),  // XMPP connection에서 올바른 형식의 ID 가져오기
      new AuctionSniper(auction, new SniperStateDisplayer())
    )
  );
  auction.join();
}
```

```python
# Python 버전
def join_auction(self, connection, item_id: str):
    """경매에 참여"""
    # [...]
    auction = XMPPAuction(chat)
    chat.add_message_listener(
        AuctionMessageTranslator(
            connection.get_user(),  # XMPP connection에서 사용자 ID 가져오기
            AuctionSniper(auction, SniperStateDisplayer())
        )
    )
    auction.join()
```

---

### 3. Sniper의 더 많은 메시지 (The Sniper Has More to Say)
**라인 165-225 | content.md**

**이전 화제와의 관계:** Translator가 PriceSource를 제공하도록 수정 완료, 이제 Sniper가 이를 해석하도록 구현

**핵심 개념 참조:**
- [상태 기반 테스트]: Sniper의 승리 중 상태를 검증
- [TDD 점진적 개발]: 단위 테스트부터 시작

**설명:**

End-to-End 테스트는 UI가 "Winning" 상태를 표시해야 한다고 알려준다. 다음 단계는 `AuctionSniper`가 `PriceSource` 매개변수를 해석하도록 수정하는 것이다. 단위 테스트부터 시작한다.

**코드:**

```java
// Sniper 단위 테스트 (라인 170-178)
public class AuctionSniperTest {
  // [...]

  @Test public void
  reportsIsWinningWhenCurrentPriceComesFromSniper() {
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperWinning();  // 승리 중 상태 확인
    }});

    sniper.currentPrice(123, 45, PriceSource.FromSniper);  // Sniper 자신의 가격
  }
}
```

```python
# Python 버전
class AuctionSniperTest:
    # [...]

    def test_reports_is_winning_when_current_price_comes_from_sniper(self):
        """Sniper의 가격이 수락되면 승리 중 상태를 보고"""
        # Mock 설정
        self.sniper_listener.should_receive('sniper_winning').at_least_once()

        self.sniper.current_price(123, 45, PriceSource.FROM_SNIPER)
```

**테스트 실패 메시지 (라인 182-186):**

```
unexpected invocation: auction.bid(<168>)  # 입찰하면 안 되는데 입찰함
expectations:
! expected at least 1 time, never invoked: sniperListener.sniperWinning()
what happened before this: nothing!
```

이 실패는 예상하지 않은 메서드를 포착하는 좋은 예다. auction에 대한 기대를 설정하지 않았으므로, 그 메서드가 호출되면 테스트가 실패한다.

**Sniper 구현 (라인 194-207):**

```java
public class AuctionSniper implements AuctionEventListener {
  // [...]

  public void currentPrice(int price, int increment, PriceSource priceSource) {
    switch (priceSource) {
      case FromSniper:
        // Sniper 자신의 가격이면 승리 중
        sniperListener.sniperWinning();
        break;
      case FromOtherBidder:
        // 다른 입찰자의 가격이면 더 높게 입찰
        auction.bid(price + increment);
        sniperListener.sniperBidding();
        break;
    }
  }
}
```

```python
# Python 버전
class AuctionSniper:
    """경매 입찰을 담당하는 Sniper"""

    def current_price(self, price: int, increment: int, price_source: PriceSource):
        """현재 가격 정보를 처리"""
        if price_source == PriceSource.FROM_SNIPER:
            # Sniper 자신의 가격이면 승리 중
            self.sniper_listener.sniper_winning()
        elif price_source == PriceSource.FROM_OTHER_BIDDER:
            # 다른 입찰자의 가격이면 더 높게 입찰
            self.auction.bid(price + increment)
            self.sniper_listener.sniper_bidding()
```

**새로운 End-to-End 테스트 실패 (라인 212-225):**

```
java.lang.AssertionError:
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Won"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Lost"  # 기대: "Won", 실제: "Lost"
```

"Winning" 상태는 표시되지만 아직 "Won"을 표시하지 못한다.

---

### 4. Sniper의 상태 획득 (The Sniper Acquires Some State)
**라인 226-321 | content.md**

**이전 화제와의 관계:** Sniper가 승리 중 상태를 표시하도록 구현 완료, 이제 최종 승리/패배 결정이 필요

**핵심 개념 참조:**
- [상태 기반 테스트]: Sniper의 내부 상태를 테스트
- [jMock States 메커니즘]: 캡슐화를 유지하면서 상태 검증
- [TDD 점진적 개발]: 단순한 경우부터 복잡한 경우로 점진적 구현

**설명:**

경매가 종료될 때 Sniper가 승리했는지 패배했는지 발표하려면 그 시점의 상태(bidding 또는 winning)를 알아야 한다. 이는 Sniper가 상태를 유지해야 함을 의미한다.

**점진적 접근:**
단순한 경우(Sniper가 패배)부터 시작하여 복잡한 경우(승리)로 진행:
1. 경매가 즉시 종료 → 패배
2. 입찰 중 경매 종료 → 패배
3. 승리 중 경매 종료 → 승리

**jMock States를 사용한 상태 표현:**

jMock의 `States` 객체는 테스트에서 객체의 상태를 기록하고 단언할 수 있게 해준다. 이는 캡슐화를 깨지 않고 논리적인 상태를 표현하는 방법이다.

**코드:**

```java
// 즉시 종료 시 패배 테스트 (라인 248-256)
public class AuctionSniperTest {
  // [...]
  private final States sniperState = context.states("sniper");  // 상태 placeholder

  @Test public void
  reportsLostIfAuctionClosesImmediately() {
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperLost();
    }});

    sniper.auctionClosed();  // 가격 업데이트 없이 즉시 종료
  }
}
```

```python
# Python 버전
class AuctionSniperTest:
    def setup_method(self):
        # jMock States와 유사한 상태 추적 메커니즘
        self.sniper_state = StateTracker("sniper")
        # [...]

    def test_reports_lost_if_auction_closes_immediately(self):
        """가격 업데이트 없이 경매가 즉시 종료되면 패배"""
        # Mock 설정
        self.sniper_listener.should_receive('sniper_lost').at_least_once()

        self.sniper.auction_closed()
```

```java
// 입찰 중 종료 시 패배 테스트 (라인 257-268)
@Test public void
reportsLostIfAuctionClosesWhenBidding() {
  context.checking(new Expectations() {{
    ignoring(auction);  // auction 호출은 무시

    // 입찰 이벤트가 발생하면 상태를 "bidding"으로 기록
    allowing(sniperListener).sniperBidding();
                            then(sniperState.is("bidding"));

    // 패배 이벤트는 "bidding" 상태에서만 발생해야 함
    atLeast(1).of(sniperListener).sniperLost();
                            when(sniperState.is("bidding"));
  }});

  sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);  // 입찰 상태로 전환
  sniper.auctionClosed();  // 종료
}
```

```python
# Python 버전
def test_reports_lost_if_auction_closes_when_bidding(self):
    """입찰 중에 경매가 종료되면 패배"""
    # auction 호출 무시
    self.auction.stub()

    # 입찰 이벤트가 발생하면 상태를 "bidding"으로 기록
    self.sniper_listener.should_receive('sniper_bidding').and_then(
        self.sniper_state.set_to("bidding")
    )

    # 패배 이벤트는 "bidding" 상태에서만 발생해야 함
    self.sniper_listener.should_receive('sniper_lost').at_least_once().when(
        self.sniper_state.is_state("bidding")
    )

    self.sniper.current_price(123, 45, PriceSource.FROM_OTHER_BIDDER)  # 입찰 상태
    self.sniper.auction_closed()  # 종료
```

**jMock States 설명 주석:**

1. **`context.states("sniper")`**: 상태 placeholder 생성 (기본 상태는 null)
2. **`allowing(...).then(state.is("..."))`**: 이벤트 발생 시 상태 기록 (supporting part)
3. **`atLeast(1).of(...).when(state.is("..."))`**: 특정 상태에서 이벤트 발생 검증 (main assertion)
4. **`ignoring(auction)`**: auction의 모든 호출 무시

**Allowances vs Expectations (라인 295-302):**

jMock은 allowed invocation과 expected invocation을 구분한다:
- **`allowing()`**: 호출될 수도, 안 될 수도 있음 (supporting infrastructure)
- **expectation**: 반드시 호출되어야 함 (확인하고자 하는 것)

이 구분은 테스트에서 중요한 것과 부수적인 것을 명확히 표현하는 데 도움이 된다.

**테스트에서 객체 상태 표현 (라인 303-315):**

테스트는 객체의 상태에 따른 행동을 단언하고 싶지만, 캡슐화를 깨고 싶지 않다. 대신 Sniper가 제공하는 알림 이벤트를 통해 상태를 추론한다. jMock의 `States` 객체는 이러한 "논리적" 상태 표현을 가능하게 한다.

이는 구현 방법과 무관하게 테스트가 관련성 있는 것을 표현할 수 있게 해준다. 곧 보겠지만, 이 분리 덕분에 Sniper 구현을 근본적으로 변경해도 테스트는 변경하지 않아도 된다.

---

### 5. Sniper의 승리 (The Sniper Wins)
**라인 322-393 | content.md**

**이전 화제와의 관계:** 패배 케이스 테스트 완료, 이제 승리 케이스 추가

**핵심 개념 참조:**
- [상태 기반 테스트]: 승리 상태 전이 검증
- [TDD 점진적 개발]: 점진적으로 상태 전이 추가

**설명:**

패배 테스트를 통과했으므로, 이제 Sniper가 승리하는 테스트를 추가한다.

**코드:**

```java
// 승리 중 종료 시 승리 테스트 (라인 330-339)
@Test public void
reportsWonIfAuctionClosesWhenWinning() {
  context.checking(new Expectations() {{
    ignoring(auction);

    // 승리 중 이벤트가 발생하면 상태를 "winning"으로 기록
    allowing(sniperListener).sniperWinning();
                            then(sniperState.is("winning"));

    // 승리 이벤트는 "winning" 상태에서만 발생해야 함
    atLeast(1).of(sniperListener).sniperWon();
                            when(sniperState.is("winning"));
  }});

  sniper.currentPrice(123, 45, true);  // 승리 중 상태로 전환
  sniper.auctionClosed();  // 종료
}
```

```python
# Python 버전
def test_reports_won_if_auction_closes_when_winning(self):
    """승리 중에 경매가 종료되면 승리"""
    # auction 호출 무시
    self.auction.stub()

    # 승리 중 이벤트가 발생하면 상태를 "winning"으로 기록
    self.sniper_listener.should_receive('sniper_winning').and_then(
        self.sniper_state.set_to("winning")
    )

    # 승리 이벤트는 "winning" 상태에서만 발생해야 함
    self.sniper_listener.should_receive('sniper_won').at_least_once().when(
        self.sniper_state.is_state("winning")
    )

    self.sniper.current_price(123, 45, PriceSource.FROM_SNIPER)  # 승리 중 상태
    self.sniper.auction_closed()  # 종료
```

**테스트 실패 메시지 (라인 341-353):**

```
unexpected invocation: sniperListener.sniperLost()
expectations:
  allowed, never invoked:
    auction.<any method>(<any parameters>) was[];
  allowed, already invoked 1 time: sniperListener.sniperWinning();
                                     then sniper is winning
  expected at least 1 time, never invoked: sniperListener.sniperWon();
                                             when sniper is winning
states:
  sniper is winning  # 상태는 "winning"인데 sniperLost()가 호출됨
what happened before this:
  sniperListener.sniperWinning()
```

**Sniper 구현 (라인 354-374):**

```java
public class AuctionSniper implements AuctionEventListener {
  // [...]
  private boolean isWinning = false;  // 상태를 나타내는 플래그

  public void auctionClosed() {
    if (isWinning) {
      sniperListener.sniperWon();  // 승리 중이었으면 승리
    } else {
      sniperListener.sniperLost();  // 아니면 패배
    }
  }

  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;  // 상태 업데이트

    if (isWinning) {
      sniperListener.sniperWinning();  // 승리 중 알림
    } else {
      auction.bid(price + increment);  // 입찰
      sniperListener.sniperBidding();  // 입찰 중 알림
    }
  }
}
```

```python
# Python 버전
class AuctionSniper:
    """경매 입찰을 담당하는 Sniper"""

    def __init__(self, auction, sniper_listener):
        self.auction = auction
        self.sniper_listener = sniper_listener
        self.is_winning = False  # 상태를 나타내는 플래그

    def auction_closed(self):
        """경매 종료 처리"""
        if self.is_winning:
            self.sniper_listener.sniper_won()  # 승리 중이었으면 승리
        else:
            self.sniper_listener.sniper_lost()  # 아니면 패배

    def current_price(self, price: int, increment: int, price_source: PriceSource):
        """현재 가격 정보를 처리"""
        self.is_winning = (price_source == PriceSource.FROM_SNIPER)  # 상태 업데이트

        if self.is_winning:
            self.sniper_listener.sniper_winning()  # 승리 중 알림
        else:
            self.auction.bid(price + increment)  # 입찰
            self.sniper_listener.sniper_bidding()  # 입찰 중 알림
```

**SniperStateDisplayer 구현 (라인 375-379):**

```java
public class SniperStateDisplayer implements SniperListener {
  // [...]
  public void sniperWon() {
    showStatus(MainWindow.STATUS_WON);
  }
}
```

```python
# Python 버전
class SniperStateDisplayer:
    """Sniper 상태를 화면에 표시하는 클래스"""

    def sniper_won(self):
        """승리 상태 표시"""
        self.show_status(MainWindow.STATUS_WON)

    def show_status(self, status: str):
        """상태 UI 업데이트"""
        # UI 업데이트 로직
        pass
```

**설계 일관성 논의 (라인 384-388):**

PriceSource에 대해 enum을 강조했는데, `isWinning`에는 boolean을 사용하는 것이 일관성이 없는가?

저자의 변명: enum을 시도했지만 너무 복잡해 보였다. `isWinning` 필드는 `AuctionSniper` 내부에 private이고, 클래스가 충분히 작아서 나중에 변경하기 쉽다. 코드가 잘 읽힌다.

**진행 상황 (라인 389-393):**
단위 테스트와 End-to-End 테스트가 모두 통과하므로 to-do 리스트에서 항목을 지울 수 있다.

더 많은 테스트를 작성할 수 있지만(예: bidding에서 winning으로, 다시 bidding으로 전환), 다음 중요한 기능 변경으로 넘어간다.

---

### 6. 안정적인 진행 (Making Steady Progress)
**라인 397-407 | content.md**

**이전 화제와의 관계:** 전체 장의 작업 완료, 회고 및 정리

**핵심 개념 참조:**
- [TDD 점진적 개발]: 작은 단계로 기능 추가
- [책임 분리]: 이전 리팩토링의 효과

**설명:**

항상 그랬듯이 작은 기능 조각들을 추가하며 안정적으로 진행했다.
1. 먼저 Sniper가 승리 중임을 표시
2. 그 다음 승리를 표시

**개발 프로세스:**
- 컴파일러를 통과시키기 위해 빈 구현 사용
- 즉각적인 작업에 집중

**즐거운 발견:**
코드가 조금씩 성장하면서 이전 노력이 효과를 발휘하기 시작했다. 새로운 기능이 기존 구조에 자연스럽게 맞아떨어졌다. 다음 작업들이 이를 더욱 흔들어 놓을 것이다.

---

## 참조 정보

**원본 파일:** content.md (라인 1-407)

**주요 참조 챕터:**
- Chapter 13 (page 134): 이전 리팩토링 (Tidying Up the Translator)
- "Value Types" (page 59): 가치 타입에 대한 상세 설명
- "Allowances and Expectations" (page 277): jMock의 allowances와 expectations
- Appendix A: jMock States 문법 상세

**코드 참조:**
- Figure 14.1 (라인 13-15): 상태 전이 다이어그램 (Joining → Bidding → Winning → Won)
- Figure 14.2 (라인 233-236): 패배 상태 전이 다이어그램
- Figure 14.3 (라인 389-393): 완료된 to-do 리스트
