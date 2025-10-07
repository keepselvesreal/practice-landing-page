# Chapter 18: 세부 사항 채우기 (Filling In the Details)

## 압축 내용
정지 가격(stop price) 기능을 추가하여 무한 입찰을 방지하고, 새로운 "Losing" 상태를 도입하며, Item 도메인 타입을 생성하여 입찰 정책을 명확히 표현함으로써 애플리케이션의 실용성과 도메인 모델의 명확성을 동시에 향상시킨다.

## 핵심 내용

### 핵심 개념들

1. **정지 가격 (Stop Price)** - 상세 내용 섹션 1.1, 1.2 참조
   - 입찰 상한선을 설정하여 무한 입찰 방지
   - 실제 배포 가능한 애플리케이션으로 발전시키는 핵심 기능
   - 사용자가 경매에서 지불할 최대 금액 제어

2. **Losing 상태** - 상세 내용 섹션 1.3, 2.1, 2.5 참조
   - 정지 가격에 도달하여 더 이상 입찰할 수 없지만 경매가 아직 종료되지 않은 상태
   - Lost 상태와 구분되어 사용자에게 최종 가격 정보 제공
   - 상태 기계(state machine)에 새로운 전이(transition) 추가

3. **Item 도메인 타입** - 상세 내용 섹션 2.3, 3.3 참조
   - 문자열 대신 명시적인 도메인 타입 사용
   - 아이템 식별자(identifier)와 정지 가격(stopPrice)을 캡슐화
   - 입찰 정책 관련 로직을 응집시킬 수 있는 플레이스홀더

4. **애자일 개발의 우선순위 변화** - 상세 내용 섹션 1.1 참조
   - 초기: 컨셉 증명(proof of concept)
   - 중기: 배포 가능한 기능 구현
   - 후기: 다양한 사용자 지원을 위한 옵션 제공

5. **테스트 주도 개발 (TDD)과 모델링 기법 통합** - 상세 내용 섹션 3.2 참조
   - 상태 전이 다이어그램을 활용한 설계
   - 다이어그램의 전이를 테스트로 직접 매핑
   - 모든 가능성을 커버하는 테스트 작성

### 핵심 개념 간 관계

```
정지 가격 도입
    ↓
Losing 상태 필요성
    ↓
상태 기계 확장 (Figure 18.1)
    ↓
Item 도메인 타입 생성
    ↓
입찰 정책 명확화
    ↓
유연한 도메인 모델
```

**관계 설명:**
- **정지 가격**이 도입되면서 **Losing 상태**가 필요해졌고, 이는 기존 상태 기계를 확장시킴
- 정지 가격과 아이템 식별자를 함께 전달하기 위해 **Item 도메인 타입**을 생성
- Item 타입은 입찰 정책(bidding policy)을 명확히 표현하고 관련 로직을 응집시키는 역할
- 명시적인 도메인 타입 사용으로 코드의 의도가 명확해지고 유연성 증가

## 상세 내용

### 화제 목차

1. **더 유용한 애플리케이션으로 발전**
   1.1 애자일 개발과 우선순위의 동적 변화
   1.2 정지 가격의 필요성
   1.3 Losing 상태 도입

2. **정지 가격 기능 구현**
   2.1 첫 번째 실패 테스트 작성
   2.2 UI에 정지 가격 입력 필드 추가
   2.3 정지 가격을 AuctionSniper까지 전달
   2.4 Item 클래스 생성
   2.5 AuctionSniper가 정지 가격 준수하도록 구현

3. **관찰과 교훈**
   3.1 점진적 UI 개발
   3.2 다른 모델링 기법과 TDD의 통합
   3.3 도메인 타입이 문자열보다 나은 이유

---

### 1. 더 유용한 애플리케이션으로 발전

#### 1.1 애자일 개발과 우선순위의 동적 변화

**참조:** content.md 라인 10-25

**설명:**
초기 기능은 잠재 고객을 유치하기 위해 애플리케이션의 외관과 스나이핑 기능을 보여주는 데 집중했다. 그러나 입찰 상한선이 없어 배포하기에는 위험한 상태였다.

애자일 개발 기법의 특징은 스폰서의 요구사항 변화에 대응할 수 있는 유연성이다:
- **초기 단계**: 컨셉 증명으로 충분한 지원 확보
- **중기 단계**: 배포 준비를 위한 충분한 기능 구현
- **후기 단계**: 더 넓은 사용자층을 지원하는 옵션 제공

이는 고정 설계 접근법(사전 승인 필요)과도 다르고, 코드 앤 픽스 접근법(초기 성공하지만 변화에 취약)과도 다른 방식이다.

**핵심 개념:** 애자일 개발의 우선순위 변화

---

#### 1.2 정지 가격의 필요성

**참조:** content.md 라인 26-28

**이전 화제와의 관계:** 1.1에서 설명한 "배포 준비를 위한 충분한 기능 구현" 단계에 해당하는 기능

**설명:**
최근 금융 위기 이후 가장 시급한 작업은 아이템 입찰에 대한 상한선, 즉 "정지 가격(stop price)"을 설정하는 기능이다. 이 기능이 없으면 입찰이 무한정 증가하여 막대한 비용이 발생할 수 있다.

**핵심 개념:** 정지 가격

---

#### 1.3 Losing 상태 도입

**참조:** content.md 라인 29-43

**이전 화제와의 관계:** 1.2의 정지 가격 도입으로 인해 필요해진 새로운 상태

**설명:**
정지 가격 도입으로 Sniper가 경매 종료 전에 losing 상태에 있을 수 있게 되었다.

단순히 정지 가격에 도달하면 Lost로 표시할 수도 있지만, 사용자는 자신이 드롭아웃한 후 경매가 종료되었을 때 최종 가격을 알고 싶어한다. 따라서 이를 추가 상태로 모델링한다.

**상태 전이:**
Sniper가 정지 가격에서 입찰가를 초과당하면, 절대 이길 수 없으므로 경매가 종료될 때까지 기다리면서 다른 입찰자들의 새로운(더 높은) 가격 업데이트를 수락한다.

**Figure 18.1 (상태 기계 다이어그램):**
- Figure 9.3을 확장하여 새로운 전이를 포함
- Losing 상태가 추가됨

**핵심 개념:** Losing 상태

---

### 2. 정지 가격 기능 구현

#### 2.1 첫 번째 실패 테스트 작성

**참조:** content.md 라인 44-104

**이전 화제와의 관계:** 1.3의 새로운 상태를 검증하는 end-to-end 테스트

**설명:**
새로운 기능을 설명하는 end-to-end 테스트를 작성한다. 이 시나리오는 Sniper가 아이템에 입찰하지만 정지 가격에 도달하여 패배하고, 다른 입찰자들이 경매가 종료될 때까지 계속 입찰하는 상황을 보여준다.

**테스트 코드 (Java → Python 변환):**

```java
// Java 원본 (라인 50-63)
@Test public void sniperLosesAnAuctionWhenThePriceIsTooHigh() throws Exception {
  auction.startSellingItem();
  application.startBiddingWithStopPrice(auction, 1100);  // 정지 가격 1100 설정
  auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  auction.reportPrice(1000, 98, "other bidder");
  application.hasShownSniperIsBidding(auction, 1000, 1098);
  auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
  auction.reportPrice(1197, 10, "third party");  // 정지 가격 초과
  application.hasShownSniperIsLosing(auction, 1197, 1098);  // Losing 상태
  auction.reportPrice(1207, 10, "fourth party");
  application.hasShownSniperIsLosing(auction, 1207, 1098);  // 계속 Losing
  auction.announceClosed();
  application.showsSniperHasLostAuction(auction, 1207, 1098);
}
```

```python
# Python 버전
def test_sniper_loses_an_auction_when_the_price_is_too_high(self):
    """정지 가격 초과 시 Sniper가 경매에서 패배하는 시나리오"""
    self.auction.start_selling_item()
    self.application.start_bidding_with_stop_price(self.auction, 1100)  # 정지 가격 1100
    self.auction.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)
    self.auction.report_price(1000, 98, "other bidder")
    self.application.has_shown_sniper_is_bidding(self.auction, 1000, 1098)
    self.auction.has_received_bid(1098, ApplicationRunner.SNIPER_XMPP_ID)
    self.auction.report_price(1197, 10, "third party")  # 정지 가격 초과
    self.application.has_shown_sniper_is_losing(self.auction, 1197, 1098)  # Losing 상태
    self.auction.report_price(1207, 10, "fourth party")
    self.application.has_shown_sniper_is_losing(self.auction, 1207, 1098)  # 계속 Losing
    self.auction.announce_closed()
    self.application.shows_sniper_has_lost_auction(self.auction, 1207, 1098)
```

**새로운 메서드 구현 (라인 69-97):**

1. **AuctionSniperDriver.startBiddingFor()** - 정지 가격을 UI에 입력

```java
// Java 원본 (라인 73-80)
public class AuctionSniperDriver extends JFrameDriver {
  public void startBiddingFor(String itemId, int stopPrice) {
    textField(NEW_ITEM_ID_NAME).replaceAllText(itemId);
    textField(NEW_ITEM_STOP_PRICE_NAME).replaceAllText(String.valueOf(stopPrice));
    bidButton().click();
  }
  // [...]
}
```

```python
# Python 버전
class AuctionSniperDriver(JFrameDriver):
    def start_bidding_for(self, item_id: str, stop_price: int):
        """아이템 ID와 정지 가격을 입력하고 입찰 시작"""
        self.text_field(NEW_ITEM_ID_NAME).replace_all_text(item_id)
        self.text_field(NEW_ITEM_STOP_PRICE_NAME).replace_all_text(str(stop_price))
        self.bid_button().click()
```

2. **SniperState enum에 LOSING 추가** (라인 89-92)

```java
// Java 원본
public enum SniperState {
  LOSING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  }, // [...]
}
```

```python
# Python 버전
from enum import Enum

class SniperState(Enum):
    LOSING = "losing"
    LOST = "lost"
    WINNING = "winning"
    BIDDING = "bidding"
    JOINING = "joining"
    WON = "won"

    def when_auction_closed(self):
        """경매 종료 시 다음 상태 반환"""
        if self == SniperState.LOSING:
            return SniperState.LOST
        # 다른 상태들의 전이 로직...
```

3. **SnipersTableModel에 표시 텍스트 추가** (라인 95-97)

```java
// Java 원본
private final static String[] STATUS_TEXT = {
  "Joining", "Bidding", "Winning", "Losing", "Lost", "Won"
};
```

```python
# Python 버전
STATUS_TEXT = ["Joining", "Bidding", "Winning", "Losing", "Lost", "Won"]
```

**테스트 실패 메시지 (라인 98-103):**
정지 가격 필드가 없다는 메시지 출력.

**핵심 개념:** 정지 가격, Losing 상태

---

#### 2.2 UI에 정지 가격 입력 필드 추가

**참조:** content.md 라인 105-129

**이전 화제와의 관계:** 2.1의 실패 테스트를 통과시키기 위한 첫 단계

**설명:**
Figure 16.2의 현재 디자인은 아이템 식별자 필드만 있지만, 상단 바에 정지 가격을 받는 필드를 쉽게 추가할 수 있다.

**구현:**
JFormattedTextField를 추가하여 정수 값만 받도록 제한하고, 몇 개의 레이블을 추가한다.

**Figure 18.2:** 정지 가격 필드가 있는 Sniper 상단 바

**예상되는 테스트 실패 (라인 119-129):**
Sniper가 계속 입찰하므로 losing 상태가 아니라는 메시지 출력.

```
[...] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
   it is not table with row with cells
     <label with text "item-54321">, <label with text "1098">,
     <label with text "1197">, <label with text "Losing">
    because
in row 0: component 1 text was "1197"
```

**핵심 개념:** 정지 가격

---

#### 2.3 정지 가격을 AuctionSniper까지 전달

**참조:** content.md 라인 130-189

**이전 화제와의 관계:** 2.2에서 UI에 입력된 정지 가격을 실제로 활용하기 위한 전달 과정

**설명:**
정지 가격을 UI에서 AuctionSniper까지 전달하여 입찰을 제한해야 한다. 체인은 MainWindow가 UserRequestListener에 통지하면서 시작한다.

**기존 메서드:**
```java
void joinAuction(String itemId);
```

**두 가지 접근법:**
1. stopPrice 인자를 추가하여 호출 체인 전체에 전달
2. 사용자의 "정책(policy)"을 나타내는 구조 생성 (선택된 접근법)

**설명:**
사용자 인터페이스는 Sniper의 아이템 입찰에 대한 "정책" 설명을 구성한다:
- 초기: 아이템 식별자만 포함 ("이 아이템에 입찰")
- 현재: 정지 가격 추가 ("이 아이템에 이 금액까지 입찰")

이 구조를 명시적으로 만들기 위해 Item 클래스를 생성한다.

**핵심 개념:** Item 도메인 타입

---

#### 2.4 Item 클래스 생성

**참조:** content.md 라인 148-210

**이전 화제와의 관계:** 2.3의 정책 구조를 명시적으로 표현하기 위한 도메인 타입

**설명:**
식별자와 정지 가격을 public 불변 필드로 가지는 간단한 값 객체로 시작한다. 나중에 동작(behavior)을 추가할 수 있다.

**Item 클래스 코드 (라인 151-159):**

```java
// Java 원본
public class Item {
  public final String identifier;
  public final int stopPrice;

  public Item(String identifier, int stopPrice) {
    this.identifier = identifier;
    this.stopPrice = stopPrice;
  }
  // also equals(), hashCode(), toString()
}
```

```python
# Python 버전
from dataclasses import dataclass

@dataclass(frozen=True)
class Item:
    """경매 아이템을 나타내는 값 객체

    Attributes:
        identifier: 아이템 식별자
        stop_price: 입찰 정지 가격 (상한선)
    """
    identifier: str
    stop_price: int

    def __post_init__(self):
        """유효성 검증"""
        if not self.identifier:
            raise ValueError("Identifier cannot be empty")
        if self.stop_price <= 0:
            raise ValueError("Stop price must be positive")
```

**"Budding Off" 기법:**
"Value Types" (59페이지)에서 설명한 budding off의 예시. 개념을 식별하기 위한 플레이스홀더 타입으로, 코드가 성장하면서 관련 기능을 추가할 장소를 제공한다.

**UserRequestListener 업데이트 (라인 164-167):**

```java
// Java 원본
public interface UserRequestListener extends EventListener {
  void joinAuction(Item item);
}
```

```python
# Python 버전
from abc import ABC, abstractmethod

class UserRequestListener(ABC):
    """사용자 요청을 처리하는 리스너 인터페이스"""

    @abstractmethod
    def join_auction(self, item: Item):
        """경매 참여 요청 처리"""
        pass
```

**MainWindowTest 수정 (라인 174-186):**

```java
// Java 원본
@Test public void
makesUserRequestWhenJoinButtonClicked() {
  final ValueMatcherProbe<Item> itemProbe =
    new ValueMatcherProbe<Item>(equalTo(new Item("an item-id", 789)), "item request");
  mainWindow.addUserRequestListener(
      new UserRequestListener() {
        public void joinAuction(Item item) {
          itemProbe.setReceivedValue(item);
        }
      });
  driver.startBiddingFor("an item-id", 789);
  driver.check(itemProbe);
}
```

```python
# Python 버전
def test_makes_user_request_when_join_button_clicked(self):
    """Join 버튼 클릭 시 사용자 요청 생성 확인"""
    item_probe = ValueMatcherProbe(
        equals(Item("an item-id", 789)),
        "item request"
    )

    class TestListener(UserRequestListener):
        def join_auction(self, item: Item):
            item_probe.set_received_value(item)

    self.main_window.add_user_request_listener(TestListener())
    self.driver.start_bidding_for("an item-id", 789)
    self.driver.check(item_probe)
```

**언어의 변화:**
이전 버전의 테스트에서 프로브 변수는 `buttonProbe`였으나 (UI 구조 설명), 이제는 `itemProbe`로 변경되어 MainWindow와 이웃 간의 협업을 설명한다.

**MainWindow 구현 (라인 192-202):**

```java
// Java 원본
joinAuctionButton.addActionListener(new ActionListener() {
  public void actionPerformed(ActionEvent e) {
    userRequests.announce().joinAuction(new Item(itemId(), stopPrice()));
  }

  private String itemId() {
    return itemIdField.getText();
  }

  private int stopPrice() {
    return ((Number)stopPriceField.getValue()).intValue();
  }
});
```

```python
# Python 버전
def _on_join_auction_clicked(self, event):
    """Join 버튼 클릭 이벤트 핸들러"""
    item = Item(self._item_id(), self._stop_price())
    self.user_requests.announce().join_auction(item)

def _item_id(self) -> str:
    """아이템 ID 필드에서 텍스트 가져오기"""
    return self.item_id_field.get_text()

def _stop_price(self) -> int:
    """정지 가격 필드에서 값 가져오기"""
    return int(self.stop_price_field.get_value())
```

**결과 (라인 203-210):**
Item을 SniperLauncher로 푸시하고, 이는 다시 AuctionHouse와 AuctionSniper 같은 의존 타입으로 푸시된다. 컴파일 오류를 수정하고 모든 테스트를 통과시킨다 (아직 구현하지 않은 end-to-end 테스트 제외).

도메인의 또 다른 개념을 명시적으로 만들었다. 아이템 식별자는 사용자가 경매에 입찰하는 방식의 한 부분일 뿐이다. 이제 코드는 입찰 선택에 대한 결정이 정확히 어디서 이루어지는지 알려줄 수 있어, 메서드 호출 체인을 따라가며 어떤 문자열이 관련 있는지 확인할 필요가 없다.

**핵심 개념:** Item 도메인 타입

---

#### 2.5 AuctionSniper가 정지 가격 준수하도록 구현

**참조:** content.md 라인 211-286

**이전 화제와의 관계:** 2.4에서 전달된 정지 가격을 실제로 활용하여 입찰 제한

**설명:**
작업을 완료하기 위한 마지막 단계는 AuctionSniper가 전달받은 정지 가격을 준수하도록 만드는 것이다. 실제로 Figure 18.1에 그려진 각 새로운 상태 전이에 대한 단위 테스트를 작성하여 모든 것을 커버했는지 확인할 수 있다.

**첫 번째 테스트 (라인 218-236):**

```java
// Java 원본
@Test public void
doesNotBidAndReportsLosingIfSubsequentPriceIsAboveStopPrice() {
  allowingSniperBidding();
  context.checking(new Expectations() {{
    int bid = 123 + 45;
    allowing(auction).bid(bid);
    atLeast(1).of(sniperListener).sniperStateChanged(
                    new SniperSnapshot(ITEM_ID, 2345, bid, LOSING));
                                        when(sniperState.is("bidding"));
  }});
  sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);
  sniper.currentPrice(2345, 25, PriceSource.FromOtherBidder);  // 정지 가격 1234 초과
}

private void allowingSniperBidding() {
  context.checking(new Expectations() {{
    allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
                                              then(sniperState.is("bidding"));
  }});
}
```

```python
# Python 버전
def test_does_not_bid_and_reports_losing_if_subsequent_price_is_above_stop_price(self):
    """후속 가격이 정지 가격 초과 시 입찰하지 않고 Losing 상태 보고"""
    self.allowing_sniper_bidding()

    bid = 123 + 45
    self.context.checking(Expectations()
        .allowing(self.auction).bid(bid)
        .at_least(1).of(self.sniper_listener).sniper_state_changed(
            SniperSnapshot(ITEM_ID, 2345, bid, SniperState.LOSING)
        ).when(self.sniper_state.is_("bidding"))
    )

    self.sniper.current_price(123, 45, PriceSource.FROM_OTHER_BIDDER)
    self.sniper.current_price(2345, 25, PriceSource.FROM_OTHER_BIDDER)  # 정지 가격 초과

def allowing_sniper_bidding(self):
    """Sniper가 입찰 상태가 되도록 허용하는 테스트 설정"""
    self.context.checking(Expectations()
        .allowing(self.sniper_listener).sniper_state_changed(
            with_(a_sniper_that_is(SniperState.BIDDING))
        ).then(self.sniper_state.is_("bidding"))
    )
```

**테스트 설정과 단언 구분 (라인 243-249):**
`allowing` 절을 사용하여 테스트 설정(AuctionSniper를 올바른 상태로 만들기)과 중요한 테스트 단언(AuctionSniper가 이제 losing 상태임)을 구분한다. 이런 표현력에 대해 매우 까다롭게 다루는 이유는, 시간이 지나도 테스트가 의미 있고 유용하게 유지되는 유일한 방법이기 때문이다. Chapter 21과 24에서 자세히 다룬다.

**다른 유사한 테스트들 (라인 251-254):**
- `doesNotBidAndReportsLosingIfFirstPriceIsAboveStopPrice()`
- `reportsLostIfAuctionClosesWhenLosing()`
- `continuesToBeLosingOnceStopPriceHasBeenReached()`
- `doesNotBidAndReportsLosingIfPriceAfterWinningIsAboveStopPrice()`

**AuctionSniper 구현 (라인 257-282):**

```java
// Java 원본
public class AuctionSniper { // [...]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    switch(priceSource) {
    case FromSniper:
      snapshot = snapshot.winning(price);
      break;
    case FromOtherBidder:
      int bid = price + increment;
      if (item.allowsBid(bid)) {  // 정지 가격 확인
        auction.bid(bid);
        snapshot = snapshot.bidding(price, bid);
      } else {
        snapshot = snapshot.losing(price);  // 정지 가격 초과
      }
      break;
    }
    notifyChange();
  } // [...]
}

public class SniperSnapshot { // [...]
  public SniperSnapshot losing(int newLastPrice) {
    return new SniperSnapshot(itemId, newLastPrice, lastBid, LOSING);
  } // [...]
}

public class Item { // [...]
  public boolean allowsBid(int bid) {
    return bid <= stopPrice;
  } // [...]
}
```

```python
# Python 버전
class AuctionSniper:
    def current_price(self, price: int, increment: int, price_source: PriceSource):
        """현재 가격 업데이트 및 입찰 결정"""
        if price_source == PriceSource.FROM_SNIPER:
            self.snapshot = self.snapshot.winning(price)
        elif price_source == PriceSource.FROM_OTHER_BIDDER:
            bid = price + increment
            if self.item.allows_bid(bid):  # 정지 가격 확인
                self.auction.bid(bid)
                self.snapshot = self.snapshot.bidding(price, bid)
            else:
                self.snapshot = self.snapshot.losing(price)  # 정지 가격 초과

        self._notify_change()

class SniperSnapshot:
    def losing(self, new_last_price: int) -> 'SniperSnapshot':
        """Losing 상태의 새로운 스냅샷 생성"""
        return SniperSnapshot(
            self.item_id,
            new_last_price,
            self.last_bid,
            SniperState.LOSING
        )

class Item:
    def allows_bid(self, bid: int) -> bool:
        """주어진 입찰가가 정지 가격 이하인지 확인"""
        return bid <= self.stop_price
```

**결과 (라인 283-286):**
End-to-end 테스트가 통과하고 기능을 목록에서 완료 표시할 수 있다.

**Figure 18.3:** Sniper가 정지 가격에서 입찰을 멈추는 화면

**핵심 개념:** 정지 가격, Losing 상태, Item 도메인 타입

---

### 3. 관찰과 교훈

#### 3.1 점진적 UI 개발

**참조:** content.md 라인 291-301

**이전 화제와의 관계:** 2.2에서의 UI 변경이 늦은 단계에서 이루어진 것에 대한 반성

**설명:**
개발 후기 단계에 사용자 인터페이스에 중요한 변경을 가하는 것처럼 보인다. 이를 미리 예상했어야 하지 않을까?

이는 애자일 사용자 경험 커뮤니티에서 활발히 논의되는 주제이며, 답은 "상황에 따라 다르지만, 생각보다 더 많은 유연성을 가질 수 있다"이다.

**간단한 애플리케이션의 경우:**
처음부터 사용자 인터페이스를 더 자세히 계획하여 사용 가능하고 일관성 있게 만드는 것이 합리적이다.

**그러나:**
변화하는 요구사항에 대응할 수 있다는 점을 강조하고 싶었다. 특히 테스트와 코드를 유연하게 구조화하면 부담이 아니라 자산이 된다.

**현실:**
요구사항은 변경될 것이며, 특히 애플리케이션을 프로덕션에 배포한 후에는 더욱 그렇다. 따라서 대응할 수 있어야 한다.

**핵심 개념:** 애자일 개발의 우선순위 변화

---

#### 3.2 다른 모델링 기법과 TDD의 통합

**참조:** content.md 라인 302-324

**이전 화제와의 관계:** 1.3과 2.1에서 사용한 상태 전이 다이어그램의 가치 재확인

**설명:**
일부 TDD 프레젠테이션은 TDD가 모든 이전 소프트웨어 설계 기법을 대체한다고 제안하는 것처럼 보인다. 그러나 TDD는 가능한 한 폭넓은 경험에서 얻은 기술과 판단력에 기반할 때 가장 잘 작동한다고 생각한다. 이는 오래된 기법과 형식을 활용하는 것을 포함한다.

**상태 전이 다이어그램의 가치:**
- 다른 관점을 제공하는 예
- 도메인의 핵심 개념에 대한 유효한 상태와 전이를 파악하지 못한 팀을 자주 목격
- 이 간단한 형식을 적용하면 코드 전체에 흩어진 행동 조각들의 난장판을 정리할 수 있음
- 상태 전이 다이어그램은 테스트에 직접 매핑되므로 모든 가능성을 커버했음을 보여줄 수 있음

**핵심:**
트릭은 다른 모델링 기법을 지원과 안내를 위해 이해하고 사용하는 것이지, 그 자체를 목적으로 삼지 않는 것이다. (그것이 처음에 나쁜 평판을 얻은 방식이다.)

**TDD 중 불확실할 때:**
때로는 뒤로 물러나서 인덱스 카드를 펼치거나, 상호작용을 스케치하는 것이 방향을 되찾는 데 도움이 될 수 있다.

**핵심 개념:** TDD와 모델링 기법 통합

---

#### 3.3 도메인 타입이 문자열보다 나은 이유

**참조:** content.md 라인 325-346

**이전 화제와의 관계:** 2.4에서 생성한 Item 타입이 왜 더 일찍 도입되었어야 했는지에 대한 반성

**Alan Perlis의 인용 (라인 326-329):**
> "문자열은 가혹한 데이터 구조이며, 전달되는 곳마다 프로세스가 많이 중복된다. 정보를 숨기기에 완벽한 수단이다."

**반성:**
되돌아보면, Item 타입을 훨씬 더 일찍, 아마도 Chapter 16에서 UserRequestListener를 추출할 때 만들었어야 했다. Sniper가 입찰하는 대상을 나타내기 위해 String을 사용하는 대신 말이다.

**만약 그랬다면:**
- 정지 가격을 기존 Item 클래스에 추가할 수 있었음
- 정의상 필요한 곳에 전달되었을 것임
- 테이블을 item identifier가 아니라 Item으로 인덱싱하고 싶다는 것을 더 일찍 알아차렸을 것임
- 단일 경매에서 여러 정책을 시도할 가능성을 열 수 있었음

**명확히:**
증명되지 않은 필요성을 위해 더 추측적으로 설계했어야 한다는 말이 아니다. 오히려 도메인을 명확하게 표현하는 수고를 들이면, 더 많은 옵션을 갖게 된다는 것이다.

**일반 원칙:**
String뿐만 아니라 다른 내장 타입(컬렉션 포함)도 래핑하는 도메인 타입을 정의하는 것이 더 나은 경우가 많다. 우리가 해야 할 일은 자신의 조언을 적용하는 것을 기억하는 것뿐이다. 보다시피, 때로는 우리도 잊는다.

**핵심 개념:** Item 도메인 타입
