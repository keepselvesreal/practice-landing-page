# 여러 아이템에 대한 스나이핑

## 압축 내용
단일 아이템 경매 참여 시스템을 다중 아이템 처리 구조로 확장하면서, 연결 관리 코드와 개별 경매 처리 코드를 분리하고, UI를 통한 동적 아이템 추가 기능을 구현하며, 사용자 요청 리스너 개념을 도입하여 UI와 비즈니스 로직 간 책임을 명확히 분리한다.

## 핵심 내용

### 핵심 개념들

1. **연결-경매 분리 (Connection-Auction Separation)** → [상세 내용: 연결과 경매 코드 분리](#연결과-경매-코드-분리)
   - 단일 XMPP 연결을 여러 경매 채팅에서 재사용
   - 연결 수준 코드와 경매 수준 코드의 책임 분리

2. **테이블 모델 확장 (Table Model Extension)** → [상세 내용: 테이블 모델 다중 행 지원](#테이블-모델-다중-행-지원)
   - 단일 행에서 다중 행 지원으로 확장
   - 동적 스나이퍼 추가 및 상태 업데이트 메커니즘

3. **사용자 요청 리스너 (User Request Listener)** → [상세 내용: 사용자 요청 리스너 패턴](#사용자-요청-리스너-패턴)
   - UI 이벤트를 도메인 이벤트로 변환
   - UI와 비즈니스 로직 간 책임 분리

4. **다층 테스팅 전략 (Multi-Level Testing Strategy)** → [상세 내용: 통합 수준 테스트 도입](#통합-수준-테스트-도입)
   - End-to-End 테스트 (시스템 전체)
   - 통합 테스트 (UI + WindowLicker)
   - 단위 테스트 (SnipersTableModel)

### 핵심 개념 간 관계

```
연결-경매 분리
    ↓ (enables)
테이블 모델 확장 ← (requires) → 다중 아이템 테스트
    ↓ (supports)
사용자 요청 리스너
    ↓ (validates through)
다층 테스팅 전략
```

- **연결-경매 분리**는 **테이블 모델 확장**을 가능하게 하며, 각 경매를 독립적으로 관리
- **테이블 모델 확장**은 **다층 테스팅 전략**을 통해 검증되며, 각 레벨에서 서로 다른 관심사 테스트
- **사용자 요청 리스너**는 UI와 비즈니스 로직을 분리하며, **통합 테스트**로 직접 검증 가능

## 상세 내용

### 화제 목차

1. [다중 아이템 테스트 작성](#다중-아이템-테스트-작성)
2. [연결과 경매 코드 분리](#연결과-경매-코드-분리)
3. [테이블 모델 다중 행 지원](#테이블-모델-다중-행-지원)
4. [UI를 통한 아이템 추가](#ui를-통한-아이템-추가)
5. [사용자 요청 리스너 패턴](#사용자-요청-리스너-패턴)
6. [통합 수준 테스트 도입](#통합-수준-테스트-도입)
7. [리팩토링 필요성 인식](#리팩토링-필요성-인식)

---

### 다중 아이템 테스트 작성

**이전 상태와의 관계**: 15장까지는 단일 아이템 경매만 처리. 이제 다중 아이템 동시 처리로 확장

**핵심 개념**: [연결-경매 분리](#핵심-개념들)

기존 테스트는 단일 경매를 암묵적으로 가정했다:

```java
// 원본 코드 (Java) - content.md 29번째 줄
application.hasShownSniperIsBidding(1000, 1098);

// 파이썬 버전
def test_sniper_bidding():
    application.has_shown_sniper_is_bidding(1000, 1098)
```

경매 객체를 명시적으로 전달하도록 수정:

```java
// 원본 코드 (Java) - content.md 32번째 줄
application.hasShownSniperIsBidding(auction, 1000, 1098);

// 파이썬 버전
def test_sniper_bidding_with_auction():
    application.has_shown_sniper_is_bidding(auction, 1000, 1098)
```

ApplicationRunner의 hasShownSniperIsBidding 구현:

```java
// 원본 코드 (Java) - content.md 38-43번째 줄
public void hasShownSniperIsBidding(FakeAuctionServer auction,
                                    int lastPrice, int lastBid)
{
  driver.showsSniperStatus(auction.getItemId(), lastPrice, lastBid,
                           textFor(SniperState.BIDDING));
}

// 파이썬 버전
def has_shown_sniper_is_bidding(self, auction: FakeAuctionServer,
                                last_price: int, last_bid: int) -> None:
    """
    경매에 대한 스나이퍼 입찰 상태를 확인

    Args:
        auction: 가짜 경매 서버 인스턴스
        last_price: 마지막 가격
        last_bid: 마지막 입찰가
    """
    self.driver.shows_sniper_status(
        auction.get_item_id(),
        last_price,
        last_bid,
        text_for(SniperState.BIDDING)
    )
```

**완전한 다중 아이템 테스트**:

```java
// 원본 코드 (Java) - content.md 45-68번째 줄
public class AuctionSniperEndToEndTest {
  private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");
  private final FakeAuctionServer auction2 = new FakeAuctionServer("item-65432");

  @Test public void
  sniperBidsForMultipleItems() throws Exception {
    auction.startSellingItem();
    auction2.startSellingItem();

    application.startBiddingIn(auction, auction2);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);

    auction.reportPrice(1000, 98, "other bidder");
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);

    auction2.reportPrice(500, 21, "other bidder");
    auction2.hasReceivedBid(521, ApplicationRunner.SNIPER_XMPP_ID);

    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    auction2.reportPrice(521, 22, ApplicationRunner.SNIPER_XMPP_ID);

    application.hasShownSniperIsWinning(auction, 1098);
    application.hasShownSniperIsWinning(auction2, 521);

    auction.announceClosed();
    auction2.announceClosed();

    application.showsSniperHasWonAuction(auction, 1098);
    application.showsSniperHasWonAuction(auction2, 521);
  }
}

// 파이썬 버전
class TestAuctionSniperEndToEnd:
    """다중 아이템 경매 End-to-End 테스트"""

    def setup_method(self):
        """각 테스트마다 두 개의 가짜 경매 서버 생성"""
        self.auction = FakeAuctionServer("item-54321")
        self.auction2 = FakeAuctionServer("item-65432")

    def test_sniper_bids_for_multiple_items(self):
        """스나이퍼가 두 개의 아이템에 동시에 입찰하고 승리"""
        # 두 경매 시작
        self.auction.start_selling_item()
        self.auction2.start_selling_item()

        # 두 경매에 입찰 시작
        application.start_bidding_in(self.auction, self.auction2)

        # 두 경매 모두 참여 요청 확인
        self.auction.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)
        self.auction2.has_received_join_request_from(ApplicationRunner.SNIPER_XMPP_ID)

        # 첫 번째 경매 입찰
        self.auction.report_price(1000, 98, "other bidder")
        self.auction.has_received_bid(1098, ApplicationRunner.SNIPER_XMPP_ID)

        # 두 번째 경매 입찰
        self.auction2.report_price(500, 21, "other bidder")
        self.auction2.has_received_bid(521, ApplicationRunner.SNIPER_XMPP_ID)

        # 두 경매 모두 승리 상태 확인
        self.auction.report_price(1098, 97, ApplicationRunner.SNIPER_XMPP_ID)
        self.auction2.report_price(521, 22, ApplicationRunner.SNIPER_XMPP_ID)

        application.has_shown_sniper_is_winning(self.auction, 1098)
        application.has_shown_sniper_is_winning(self.auction2, 521)

        # 두 경매 종료 및 승리 확인
        self.auction.announce_closed()
        self.auction2.announce_closed()

        application.shows_sniper_has_won_auction(self.auction, 1098)
        application.shows_sniper_has_won_auction(self.auction2, 521)
```

**False Positive 방지**: 검증 메서드들을 그룹화하여 동시에 유효한지 확인 (content.md 72-76번째 줄)

---

### 연결과 경매 코드 분리

**이전 상태와의 관계**: [다중 아이템 테스트 작성](#다중-아이템-테스트-작성)에서 테스트 구조 변경 완료

**핵심 개념**: [연결-경매 분리](#핵심-개념들)

ApplicationRunner에서 가변 인자 지원:

```java
// 원본 코드 (Java) - content.md 88-109번째 줄
public class ApplicationRunner {
  public void startBiddingIn(final FakeAuctionServer... auctions) {
    Thread thread = new Thread("Test Application") {
      @Override public void run() {
        try {
          Main.main(arguments(auctions));
        } catch (Throwable e) {
          // 에러 처리
        }
      }
    };
    thread.setDaemon(true);
    thread.start();

    for (FakeAuctionServer auction : auctions) {
      driver.showsSniperStatus(auction.getItemId(), 0, 0, textFor(JOINING));
    }
  }

  protected static String[] arguments(FakeAuctionServer... auctions) {
    String[] arguments = new String[auctions.length + 3];
    arguments[0] = XMPP_HOSTNAME;
    arguments[1] = SNIPER_ID;
    arguments[2] = SNIPER_PASSWORD;
    for (int i = 0; i < auctions.length; i++) {
      arguments[i + 3] = auctions[i].getItemId();
    }
    return arguments;
  }
}

// 파이썬 버전
class ApplicationRunner:
    """테스트용 애플리케이션 실행 관리자"""

    def start_bidding_in(self, *auctions: FakeAuctionServer) -> None:
        """
        여러 경매에서 입찰 시작

        Args:
            *auctions: 가변 개수의 가짜 경매 서버들
        """
        def run_application():
            try:
                Main.main(self._arguments(auctions))
            except Exception as e:
                # 에러 처리
                pass

        # 별도 데몬 스레드에서 애플리케이션 실행
        thread = threading.Thread(target=run_application, name="Test Application", daemon=True)
        thread.start()

        # 각 경매에 대해 JOINING 상태 확인
        for auction in auctions:
            self.driver.shows_sniper_status(
                auction.get_item_id(),
                0,
                0,
                text_for(SniperState.JOINING)
            )

    @staticmethod
    def _arguments(*auctions: FakeAuctionServer) -> list[str]:
        """
        명령줄 인자 생성

        Returns:
            [호스트명, 사용자ID, 비밀번호, item_id1, item_id2, ...]
        """
        args = [XMPP_HOSTNAME, SNIPER_ID, SNIPER_PASSWORD]
        args.extend(auction.get_item_id() for auction in auctions)
        return args
```

Main 클래스의 연결-경매 분리:

```java
// 원본 코드 (Java) - content.md 183-203번째 줄
public class Main {
  public static void main(String... args) throws Exception {
    Main main = new Main();
    XMPPConnection connection =
      connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
    main.disconnectWhenUICloses(connection);
    main.joinAuction(connection, args[ARG_ITEM_ID]);
  }

  private void joinAuction(XMPPConnection connection, String itemId) {
    Chat chat = connection.getChatManager()
                            .createChat(auctionId(itemId, connection), null);
    notToBeGCd.add(chat);  // 가비지 컬렉션 방지

    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(itemId, auction,
                              new SwingThreadSniperListener(snipers))));
    auction.join();
  }
}

// 파이썬 버전
class Main:
    """메인 애플리케이션 클래스"""

    def __init__(self):
        self.not_to_be_gcd = []  # 가비지 컬렉션 방지용 채팅 저장
        self.snipers = SnipersTableModel()
        self.ui = None

    @staticmethod
    def main(*args: str) -> None:
        """
        애플리케이션 진입점

        Args:
            args: [호스트명, 사용자명, 비밀번호, 아이템ID]
        """
        main = Main()

        # 연결 수준: 한 번만 생성
        connection = create_connection(
            args[ARG_HOSTNAME],
            args[ARG_USERNAME],
            args[ARG_PASSWORD]
        )
        main.disconnect_when_ui_closes(connection)

        # 경매 수준: 아이템마다 생성
        main.join_auction(connection, args[ARG_ITEM_ID])

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """
        특정 경매에 참여

        Args:
            connection: 재사용할 XMPP 연결
            item_id: 경매 아이템 ID
        """
        # 개별 경매용 채팅 생성
        chat = connection.get_chat_manager().create_chat(
            auction_id(item_id, connection),
            None
        )
        self.not_to_be_gcd.append(chat)  # 참조 유지

        # 경매 객체 생성 및 리스너 연결
        auction = XMPPAuction(chat)
        chat.add_message_listener(
            AuctionMessageTranslator(
                connection.get_user(),
                AuctionSniper(
                    item_id,
                    auction,
                    SwingThreadSniperListener(self.snipers)
                )
            )
        )

        # 경매 참여
        auction.join()
```

여러 아이템 처리를 위한 루프:

```java
// 원본 코드 (Java) - content.md 205-213번째 줄
public static void main(String... args) throws Exception {
  Main main = new Main();
  XMPPConnection connection =
    connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
  main.disconnectWhenUICloses(connection);

  for (int i = 3; i < args.length; i++) {
    main.joinAuction(connection, args[i]);
  }
}

// 파이썬 버전
@staticmethod
def main(*args: str) -> None:
    """
    다중 아이템 지원 애플리케이션 진입점

    Args:
        args: [호스트명, 사용자명, 비밀번호, 아이템ID1, 아이템ID2, ...]
    """
    main = Main()

    # 한 번만 연결
    connection = create_connection(
        args[ARG_HOSTNAME],
        args[ARG_USERNAME],
        args[ARG_PASSWORD]
    )
    main.disconnect_when_ui_closes(connection)

    # 각 아이템마다 경매 참여
    for item_id in args[3:]:  # 3번 인덱스부터 아이템 ID들
        main.join_auction(connection, item_id)
```

---

### 테이블 모델 다중 행 지원

**이전 상태와의 관계**: [연결과 경매 코드 분리](#연결과-경매-코드-분리)에서 구조 변경 완료

**핵심 개념**: [테이블 모델 확장](#핵심-개념들)

스나이퍼 추가를 위한 새 메서드:

```java
// 원본 코드 (Java) - content.md 237-248번째 줄
private void
joinAuction(XMPPConnection connection, String itemId) throws Exception {
  safelyAddItemToModel(itemId);
  // 나머지 코드...
}

private void safelyAddItemToModel(final String itemId) throws Exception {
  SwingUtilities.invokeAndWait(new Runnable() {
    public void run() {
      snipers.addSniper(SniperSnapshot.joining(itemId));
    }
  });
}

// 파이썬 버전
def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
    """
    경매 참여 (Swing 스레드 안전 버전)

    Args:
        connection: XMPP 연결
        item_id: 아이템 ID
    """
    self._safely_add_item_to_model(item_id)
    # 나머지 코드...

def _safely_add_item_to_model(self, item_id: str) -> None:
    """
    스레드 안전하게 테이블 모델에 아이템 추가

    Args:
        item_id: 추가할 아이템 ID
    """
    def add_to_model():
        self.snipers.add_sniper(SniperSnapshot.joining(item_id))

    # Swing 스레드에서 실행 대기
    SwingUtilities.invoke_and_wait(add_to_model)
```

**스나이퍼 추가 단위 테스트**:

```java
// 원본 코드 (Java) - content.md 253-263번째 줄
@Test public void
notifiesListenersWhenAddingASniper() {
    SniperSnapshot joining = SniperSnapshot.joining("item123");
    context.checking(new Expectations() { {
      one(listener).tableChanged(with(anInsertionAtRow(0)));
    }});

    assertEquals(0, model.getRowCount());
    model.addSniper(joining);
    assertEquals(1, model.getRowCount());
    assertRowMatchesSnapshot(0, joining);
}

// 파이썬 버전 (pytest + unittest.mock)
def test_notifies_listeners_when_adding_sniper():
    """스나이퍼 추가 시 리스너에게 알림"""
    # 준비
    model = SnipersTableModel()
    listener = Mock(spec=TableModelListener)
    model.add_table_model_listener(listener)

    joining = SniperSnapshot.joining("item123")

    # 실행 전 상태 확인
    assert model.get_row_count() == 0

    # 스나이퍼 추가
    model.add_sniper(joining)

    # 검증
    assert model.get_row_count() == 1
    listener.table_changed.assert_called_once()

    # 이벤트가 0번 행 삽입임을 확인
    event = listener.table_changed.call_args[0][0]
    assert event.type == TableModelEvent.INSERT
    assert event.first_row == 0

    # 행 데이터 일치 확인
    assert_row_matches_snapshot(model, 0, joining)
```

**기존 업데이트 테스트 수정**:

```java
// 원본 코드 (Java) - content.md 276-287번째 줄
@Test public void
setsSniperValuesInColumns() {
  SniperSnapshot joining = SniperSnapshot.joining("item id");
  SniperSnapshot bidding = joining.bidding(555, 666);

  context.checking(new Expectations() {{
    allowing(listener).tableChanged(with(anyInsertionEvent()));
    one(listener).tableChanged(with(aChangeInRow(0)));
  }});

  model.addSniper(joining);
  model.sniperStateChanged(bidding);

  assertRowMatchesSnapshot(0, bidding);
}

// 파이썬 버전
def test_sets_sniper_values_in_columns():
    """스나이퍼 상태 변경이 컬럼 값을 설정"""
    # 준비
    model = SnipersTableModel()
    listener = Mock(spec=TableModelListener)
    model.add_table_model_listener(listener)

    joining = SniperSnapshot.joining("item id")
    bidding = joining.bidding(555, 666)

    # 스나이퍼 추가 (삽입 이벤트 발생 - 허용)
    model.add_sniper(joining)

    # 리스너 호출 기록 초기화
    listener.reset_mock()

    # 스나이퍼 상태 변경
    model.sniper_state_changed(bidding)

    # 검증: 0번 행 업데이트 이벤트만 발생
    listener.table_changed.assert_called_once()
    event = listener.table_changed.call_args[0][0]
    assert event.type == TableModelEvent.UPDATE
    assert event.first_row == 0
    assert event.last_row == 0

    # 행 데이터 일치 확인
    assert_row_matches_snapshot(model, 0, bidding)
```

**추가 순서 유지 테스트**:

```java
// 원본 코드 (Java) - content.md 297-306번째 줄
@Test public void
holdsSnipersInAdditionOrder() {
  context.checking(new Expectations() { {
    ignoring(listener);
  }});

  model.addSniper(SniperSnapshot.joining("item 0"));
  model.addSniper(SniperSnapshot.joining("item 1"));

  assertEquals("item 0", cellValue(0, Column.ITEM_IDENTIFIER));
  assertEquals("item 1", cellValue(1, Column.ITEM_IDENTIFIER));
}

// 파이썬 버전
def test_holds_snipers_in_addition_order():
    """스나이퍼들을 추가 순서대로 유지"""
    model = SnipersTableModel()

    # 두 스나이퍼 순서대로 추가
    model.add_sniper(SniperSnapshot.joining("item 0"))
    model.add_sniper(SniperSnapshot.joining("item 1"))

    # 순서 확인
    assert model.get_value_at(0, Column.ITEM_IDENTIFIER) == "item 0"
    assert model.get_value_at(1, Column.ITEM_IDENTIFIER) == "item 1"
```

**SnipersTableModel 구현**:

```java
// 원본 코드 (Java) - content.md 320-332번째 줄
public void sniperStateChanged(SniperSnapshot newSnapshot) {
  int row = rowMatching(newSnapshot);
  snapshots.set(row, newSnapshot);
  fireTableRowsUpdated(row, row);
}

private int rowMatching(SniperSnapshot snapshot) {
  for (int i = 0; i < snapshots.size(); i++) {
    if (newSnapshot.isForSameItemAs(snapshots.get(i))) {
      return i;
    }
  }
  throw new Defect("Cannot find match for " + snapshot);
}

// 파이썬 버전
class SnipersTableModel(AbstractTableModel):
    """다중 스나이퍼를 지원하는 테이블 모델"""

    def __init__(self):
        super().__init__()
        self.snapshots: list[SniperSnapshot] = []

    def sniper_state_changed(self, new_snapshot: SniperSnapshot) -> None:
        """
        스나이퍼 상태 변경 처리

        Args:
            new_snapshot: 새 스나이퍼 스냅샷

        Raises:
            Defect: 일치하는 스나이퍼를 찾을 수 없는 경우
        """
        row = self._row_matching(new_snapshot)
        self.snapshots[row] = new_snapshot
        self.fire_table_rows_updated(row, row)

    def _row_matching(self, snapshot: SniperSnapshot) -> int:
        """
        스냅샷과 일치하는 행 번호 찾기

        Args:
            snapshot: 찾을 스냅샷

        Returns:
            일치하는 행 번호

        Raises:
            Defect: 일치하는 항목이 없을 때
        """
        for i, existing_snapshot in enumerate(self.snapshots):
            if snapshot.is_for_same_item_as(existing_snapshot):
                return i

        raise Defect(f"Cannot find match for {snapshot}")

    def add_sniper(self, snapshot: SniperSnapshot) -> None:
        """
        새 스나이퍼 추가

        Args:
            snapshot: 추가할 스나이퍼 스냅샷
        """
        row = len(self.snapshots)
        self.snapshots.append(snapshot)
        self.fire_table_rows_inserted(row, row)
```

---

### UI를 통한 아이템 추가

**이전 상태와의 관계**: [테이블 모델 다중 행 지원](#테이블-모델-다중-행-지원)에서 데이터 모델 완성

**핵심 개념**: [사용자 요청 리스너](#핵심-개념들)

ApplicationRunner 테스트 구조 변경:

```java
// 원본 코드 (Java) - content.md 379-392번째 줄
public class ApplicationRunner {
  public void startBiddingIn(final FakeAuctionServer... auctions) {
    startSniper();
    for (FakeAuctionServer auction : auctions) {
      final String itemId = auction.getItemId();
      driver.startBiddingFor(itemId);
      driver.showsSniperStatus(itemId, 0, 0, textFor(SniperState.JOINING));
    }
  }

  private void startSniper() {
    // UI만 시작, showsSniperStatus() 호출 제거
  }
}

// 파이썬 버전
class ApplicationRunner:
    """테스트용 애플리케이션 실행자"""

    def start_bidding_in(self, *auctions: FakeAuctionServer) -> None:
        """
        UI를 통해 여러 경매에 입찰 시작

        Args:
            *auctions: 참여할 경매들
        """
        # 1단계: 스나이퍼 애플리케이션만 시작
        self._start_sniper()

        # 2단계: 각 경매를 UI를 통해 추가
        for auction in auctions:
            item_id = auction.get_item_id()

            # UI 입력으로 입찰 시작
            self.driver.start_bidding_for(item_id)

            # JOINING 상태 확인
            self.driver.shows_sniper_status(
                item_id,
                0,
                0,
                text_for(SniperState.JOINING)
            )

    def _start_sniper(self) -> None:
        """스나이퍼 애플리케이션만 시작 (명령줄 인자 없음)"""
        # 이전 코드와 동일하나 showsSniperStatus() 호출 제거
        pass
```

AuctionSniperDriver의 UI 입력 메서드:

```java
// 원본 코드 (Java) - content.md 396-412번째 줄
public class AuctionSniperDriver extends JFrameDriver {
  @SuppressWarnings("unchecked")
  public void startBiddingFor(String itemId) {
    itemIdField().replaceAllText(itemId);
    bidButton().click();
  }

  private JTextFieldDriver itemIdField() {
    JTextFieldDriver newItemId =
      new JTextFieldDriver(this, JTextField.class, named(MainWindow.NEW_ITEM_ID_NAME));
    newItemId.focusWithMouse();
    return newItemId;
  }

  private JButtonDriver bidButton() {
    return new JButtonDriver(this, JButton.class, named(MainWindow.JOIN_BUTTON_NAME));
  }
}

// 파이썬 버전
class AuctionSniperDriver(JFrameDriver):
    """경매 스나이퍼 UI 드라이버"""

    def start_bidding_for(self, item_id: str) -> None:
        """
        UI를 통해 아이템 입찰 시작

        Args:
            item_id: 입찰할 아이템 ID
        """
        # 텍스트 필드에 아이템 ID 입력
        item_field = self._item_id_field()
        item_field.replace_all_text(item_id)

        # Join Auction 버튼 클릭
        bid_btn = self._bid_button()
        bid_btn.click()

    def _item_id_field(self) -> JTextFieldDriver:
        """
        아이템 ID 텍스트 필드 찾기

        Returns:
            텍스트 필드 드라이버
        """
        field = JTextFieldDriver(
            self,
            JTextField,
            named(MainWindow.NEW_ITEM_ID_NAME)
        )
        field.focus_with_mouse()  # 마우스로 포커스
        return field

    def _bid_button(self) -> JButtonDriver:
        """
        Join Auction 버튼 찾기

        Returns:
            버튼 드라이버
        """
        return JButtonDriver(
            self,
            JButton,
            named(MainWindow.JOIN_BUTTON_NAME)
        )
```

MainWindow에 액션 바 추가:

```java
// 원본 코드 (Java) - content.md 429-448번째 줄
public class MainWindow extends JFrame {
  public MainWindow(TableModel snipers) {
    super(APPLICATION_TITLE);
    setName(MainWindow.MAIN_WINDOW_NAME);
    fillContentPane(makeSnipersTable(snipers), makeControls());
  }

  private JPanel makeControls() {
    JPanel controls = new JPanel(new FlowLayout());

    final JTextField itemIdField = new JTextField();
    itemIdField.setColumns(25);
    itemIdField.setName(NEW_ITEM_ID_NAME);
    controls.add(itemIdField);

    JButton joinAuctionButton = new JButton("Join Auction");
    joinAuctionButton.setName(JOIN_BUTTON_NAME);
    controls.add(joinAuctionButton);

    return controls;
  }
}

// 파이썬 버전
class MainWindow(JFrame):
    """메인 윈도우 UI"""

    NEW_ITEM_ID_NAME = "item id"
    JOIN_BUTTON_NAME = "join button"

    def __init__(self, snipers: TableModel):
        """
        메인 윈도우 초기화

        Args:
            snipers: 스나이퍼 테이블 모델
        """
        super().__init__(APPLICATION_TITLE)
        self.set_name(MainWindow.MAIN_WINDOW_NAME)

        # 스나이퍼 테이블과 컨트롤 패널로 구성
        self._fill_content_pane(
            self._make_snipers_table(snipers),
            self._make_controls()
        )

    def _make_controls(self) -> JPanel:
        """
        상단 액션 바 생성 (아이템 ID 입력 + Join 버튼)

        Returns:
            컨트롤 패널
        """
        controls = JPanel(FlowLayout())

        # 아이템 ID 텍스트 필드
        item_id_field = JTextField()
        item_id_field.set_columns(25)  # 25자 너비
        item_id_field.set_name(self.NEW_ITEM_ID_NAME)
        controls.add(item_id_field)

        # Join Auction 버튼
        join_button = JButton("Join Auction")
        join_button.set_name(self.JOIN_BUTTON_NAME)
        controls.add(join_button)

        return controls
```

---

### 사용자 요청 리스너 패턴

**이전 상태와의 관계**: [UI를 통한 아이템 추가](#ui를-통한-아이템-추가)에서 UI 구조 완성

**핵심 개념**: [사용자 요청 리스너](#핵심-개념들)

UserRequestListener 인터페이스 정의:

```java
// 원본 코드 (Java) - content.md 486-488번째 줄
public interface UserRequestListener extends EventListener {
  void joinAuction(String itemId);
}

// 파이썬 버전
from abc import ABC, abstractmethod
from typing import Protocol

class UserRequestListener(Protocol):
    """
    사용자 요청 리스너 인터페이스

    UI 이벤트를 도메인 이벤트로 변환하는 계층
    """

    @abstractmethod
    def join_auction(self, item_id: str) -> None:
        """
        사용자가 경매 참여를 요청

        Args:
            item_id: 참여할 경매 아이템 ID
        """
        pass
```

MainWindow에서 Announcer를 사용한 리스너 관리:

```java
// 원본 코드 (Java) - content.md 536-552번째 줄
public class MainWindow extends JFrame {
  private final Announcer<UserRequestListener> userRequests =
                                     Announcer.to(UserRequestListener.class);

  public void addUserRequestListener(UserRequestListener userRequestListener) {
    userRequests.addListener(userRequestListener);
  }

  private JPanel makeControls(final SnipersTableModel snipers) {
    // ...
    joinAuctionButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        userRequests.announce().joinAuction(itemIdField.getText());
      }
    });
    // ...
  }
}

// 파이썬 버전
class MainWindow(JFrame):
    """메인 윈도우 - UI 이벤트를 도메인 이벤트로 변환"""

    def __init__(self, snipers: TableModel):
        super().__init__(APPLICATION_TITLE)

        # UserRequestListener들을 관리하는 Announcer
        self.user_requests = Announcer(UserRequestListener)

        # UI 구성...

    def add_user_request_listener(self, listener: UserRequestListener) -> None:
        """
        사용자 요청 리스너 등록

        Args:
            listener: 등록할 리스너
        """
        self.user_requests.add_listener(listener)

    def _make_controls(self) -> JPanel:
        """컨트롤 패널 생성"""
        controls = JPanel(FlowLayout())

        item_id_field = JTextField()
        item_id_field.set_columns(25)
        item_id_field.set_name(self.NEW_ITEM_ID_NAME)
        controls.add(item_id_field)

        join_button = JButton("Join Auction")
        join_button.set_name(self.JOIN_BUTTON_NAME)

        # ActionListener → UserRequestListener 변환
        def on_join_clicked(event):
            """Join 버튼 클릭 시 도메인 이벤트 발생"""
            item_id = item_id_field.get_text()
            # 모든 등록된 UserRequestListener에게 알림
            self.user_requests.announce().join_auction(item_id)

        join_button.add_action_listener(on_join_clicked)
        controls.add(join_button)

        return controls
```

Main 클래스에서 UserRequestListener 구현:

```java
// 원본 코드 (Java) - content.md 580-604번째 줄
public class Main {
  public static void main(String... args) throws Exception {
    Main main = new Main();
    XMPPConnection connection =
      connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
    main.disconnectWhenUICloses(connection);
    main.addUserRequestListenerFor(connection);
  }

  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
        snipers.addSniper(SniperSnapshot.joining(itemId));

        Chat chat = connection.getChatManager()
                                 .createChat(auctionId(itemId, connection), null);
        notToBeGCd.add(chat);

        Auction auction = new XMPPAuction(chat);
        chat.addMessageListener(
               new AuctionMessageTranslator(connection.getUser(),
                     new AuctionSniper(itemId, auction,
                                       new SwingThreadSniperListener(snipers))));
        auction.join();
      }
    });
  }
}

// 파이썬 버전
class Main:
    """메인 애플리케이션"""

    @staticmethod
    def main(*args: str) -> None:
        """애플리케이션 진입점"""
        main = Main()

        # XMPP 연결 설정
        connection = create_connection(
            args[ARG_HOSTNAME],
            args[ARG_USERNAME],
            args[ARG_PASSWORD]
        )
        main.disconnect_when_ui_closes(connection)

        # UserRequestListener 등록
        main._add_user_request_listener_for(connection)

    def _add_user_request_listener_for(self, connection: XMPPConnection) -> None:
        """
        UserRequestListener 구현 및 등록

        Args:
            connection: 재사용할 XMPP 연결
        """
        # 익명 클래스 대신 람다 사용
        def handle_join_auction(item_id: str) -> None:
            """
            사용자의 경매 참여 요청 처리

            이 메서드는 Swing 스레드에서 호출됨 (ActionListener → UserRequestListener)
            따라서 safelyAddItemToModel() 래퍼 불필요

            Args:
                item_id: 참여할 경매 아이템 ID
            """
            # 테이블 모델에 스나이퍼 추가 (이미 Swing 스레드)
            self.snipers.add_sniper(SniperSnapshot.joining(item_id))

            # 경매용 채팅 생성
            chat = connection.get_chat_manager().create_chat(
                auction_id(item_id, connection),
                None
            )
            self.not_to_be_gcd.append(chat)

            # 경매 참여
            auction = XMPPAuction(chat)
            chat.add_message_listener(
                AuctionMessageTranslator(
                    connection.get_user(),
                    AuctionSniper(
                        item_id,
                        auction,
                        SwingThreadSniperListener(self.snipers)
                    )
                )
            )
            auction.join()

        # 리스너 등록
        self.ui.add_user_request_listener(
            UserRequestListenerImpl(handle_join_auction)
        )


class UserRequestListenerImpl:
    """UserRequestListener 구현체"""

    def __init__(self, join_handler):
        self._join_handler = join_handler

    def join_auction(self, item_id: str) -> None:
        self._join_handler(item_id)
```

**책임 분리의 핵심**:
- MainWindow: Swing ActionEvent → UserRequestListener 도메인 이벤트 변환
- Main: 도메인 이벤트 처리 (연결, 채팅, 경매 로직)

---

### 통합 수준 테스트 도입

**이전 상태와의 관계**: [사용자 요청 리스너 패턴](#사용자-요청-리스너-패턴)에서 새 개념 도입

**핵심 개념**: [다층 테스팅 전략](#핵심-개념들)

MainWindow 통합 테스트:

```java
// 원본 코드 (Java) - content.md 497-514번째 줄
public class MainWindowTest {
  private final SnipersTableModel tableModel = new SnipersTableModel();
  private final MainWindow mainWindow = new MainWindow(tableModel);
  private final AuctionSniperDriver driver = new AuctionSniperDriver(100);

  @Test public void
  makesUserRequestWhenJoinButtonClicked() {
    final ValueMatcherProbe<String> buttonProbe =
      new ValueMatcherProbe<String>(equalTo("an item-id"), "join request");

    mainWindow.addUserRequestListener(
        new UserRequestListener() {
          public void joinAuction(String itemId) {
            buttonProbe.setReceivedValue(itemId);
          }
        });

    driver.startBiddingFor("an item-id");
    driver.check(buttonProbe);
  }
}

// 파이썬 버전 (pytest + WindowLicker 스타일)
class TestMainWindow:
    """MainWindow 통합 테스트 (Swing 스레딩 고려)"""

    def setup_method(self):
        """각 테스트마다 새 MainWindow 생성"""
        self.table_model = SnipersTableModel()
        self.main_window = MainWindow(self.table_model)
        self.driver = AuctionSniperDriver(timeout=100)

    def test_makes_user_request_when_join_button_clicked(self):
        """
        Join 버튼 클릭 시 UserRequestListener가 올바른 아이템 ID로 호출됨

        통합 테스트인 이유:
        - Swing 스레딩 메커니즘 사용
        - WindowLicker Probe로 비동기 확인
        """
        # Probe: 비동기 값 검증
        button_probe = ValueMatcherProbe(
            matcher=equal_to("an item-id"),
            description="join request"
        )

        # UserRequestListener 구현 (테스트용)
        def on_join_auction(item_id: str) -> None:
            """리스너 호출 시 Probe에 값 설정"""
            button_probe.set_received_value(item_id)

        listener = UserRequestListenerImpl(on_join_auction)
        self.main_window.add_user_request_listener(listener)

        # UI 조작: "an item-id" 입력 후 Join 버튼 클릭
        self.driver.start_bidding_for("an item-id")

        # Probe 검증: Swing 이벤트 완료 대기
        self.driver.check(button_probe)


class ValueMatcherProbe:
    """
    WindowLicker Probe 패턴

    비동기 이벤트 완료를 대기하며 값 검증
    """

    def __init__(self, matcher, description: str):
        self.matcher = matcher
        self.description = description
        self.received_value = None
        self.satisfied = False

    def set_received_value(self, value):
        """값 설정 및 만족 여부 확인"""
        self.received_value = value
        self.satisfied = self.matcher.matches(value)

    def is_satisfied(self) -> bool:
        """Probe가 만족했는지 확인"""
        return self.satisfied

    def describe_failure(self) -> str:
        """실패 메시지"""
        if self.received_value is None:
            return f"{self.description}. Received nothing"
        return f"{self.description}. Got {self.received_value}"
```

**WindowLicker Probe 설명** (content.md 520-525번째 줄):
- Probe: 특정 상태가 될 때까지 반복 확인하는 객체
- driver.check(): Probe가 만족하거나 타임아웃될 때까지 반복 실행
- ValueMatcherProbe: Hamcrest Matcher로 값 비교

**통합 테스트가 필요한 이유** (content.md 565-570번째 줄):
- Swing 스레딩: 단순 단위 테스트로는 비동기 완료 확인 불가
- 실수 방지: 텍스트 필드의 이름(item-id)과 텍스트(item id) 혼동 방지
- End-to-End 테스트보다 빠르고 명확한 피드백

---

### 리팩토링 필요성 인식

**이전 상태와의 관계**: 모든 기능 구현 완료

**핵심 개념**: 기술 부채 관리, 지속 가능한 코드

**"Ship It?" 논의** (content.md 632-648번째 줄):

테스트는 통과했지만 Main 클래스의 설계 문제:
- 여러 책임이 한 곳에 집중 (연결, 채팅, 경매, UI 이벤트 처리)
- End-to-End 테스트로만 검증 가능 → 규모 확장 시 유지보수 어려움
- 단위 테스트 부재 → 내부 품질에 대한 피드백 없음

**프로덕션 배포 조건**:
- 코드가 절대 변경되지 않을 것 (현실적으로 불가능)
- 진짜 긴급 상황 (단순히 서두르는 것은 위기 아님)

**다음 장 예고**:
- Main 클래스 리팩토링
- 책임 분리 및 테스트 가능한 구조로 개선

**핵심 교훈**:
> "작동함(working)"과 "완성됨(finished)"은 다르다.
> 지금 정리하지 않으면 매번 재학습 비용 발생

---

## 참조 정보

- **content.md 라인 정보**: 각 코드 블록과 설명 옆에 표시됨
- **핵심 개념 참조**: `→ [상세 내용: 섹션명](#앵커)` 형식으로 연결
- **이전 화제와의 관계**: 각 섹션 시작 부분에 명시
