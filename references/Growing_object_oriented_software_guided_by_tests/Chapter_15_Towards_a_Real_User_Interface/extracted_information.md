# 실제 사용자 인터페이스로 나아가기

## 압축 내용
단순한 레이블에서 테이블로 UI를 점진적으로 발전시키면서, 기존 설계 결정을 과감히 변경하고 더 흥미로운 구조를 발견해가는 과정을 다룬다.

## 핵심 내용

### 핵심 개념

1. **점진적 UI 개선** (상세 내용: 화제 1-3)
   - 전체를 한 번에 교체하는 대신 한 번에 하나씩 기능을 추가하여 리스크를 줄임
   - JLabel을 JTable로 교체하는 최소 단계부터 시작

2. **이벤트 단순화** (상세 내용: 화제 4-5)
   - 여러 콜백 메서드를 단일 알림으로 통합
   - SniperState와 SniperSnapshot의 명확한 역할 분리

3. **객체지향적 리팩토링** (상세 내용: 화제 6-7)
   - switch 문을 다형성으로 대체
   - 열거형에 동작 추가하여 더 객체지향적인 코드 작성

4. **설계 변경의 수용** (상세 내용: 화제 8)
   - 구현을 통해 설계 개선점 발견
   - 리네이밍을 통한 명확성 향상

### 핵심 개념 간 관계

- **점진적 UI 개선**은 **이벤트 단순화**의 필요성을 발견하게 함
- **이벤트 단순화**는 **객체지향적 리팩토링**의 기회를 제공
- **설계 변경의 수용**은 모든 과정에서 지속적으로 적용되는 철학

## 상세 내용

### 화제 목차

1. 현실적인 구현 - JLabel을 JTable로 교체 (174-177쪽)
2. 가격 세부사항 표시 - 스니퍼 상태를 테이블로 전달 (177-183쪽)
3. 스니퍼 이벤트 단순화 - 여러 콜백을 하나로 통합 (184-189쪽)
4. 후속 작업 - Won과 Lost 상태 변환 (189-190쪽)
5. 테이블 모델 다듬기 - 불필요한 코드 제거 (191쪽)
6. 객체지향적 컬럼 - switch 문을 다형성으로 대체 (191-192쪽)
7. 이벤트 경로 단축 - 불필요한 전달 호출 제거 (192-193쪽)
8. 마지막 손질 - 컬럼 타이틀 테스트 및 구현 (193-196쪽)

---

### 화제 1: 현실적인 구현 - JLabel을 JTable로 교체
**참조**: content.md 11-101쪽

#### 이전 화제와의 관계
새로운 장의 시작으로, 이전까지의 단순한 레이블 기반 UI를 테이블 기반으로 전환하기 시작

#### 설명
단순한 JLabel을 단일 셀 JTable로 교체하는 최소한의 변경부터 시작. 전체 애플리케이션을 한 번에 뜯어고치지 않고 점진적으로 개선.

#### 주요 코드

```java
// 참조: content.md 43-47쪽
// 테스트 코드 - 레이블 대신 테이블 셀 찾기
public class AuctionSniperDriver extends JFrameDriver {
    public void showsSniperStatus(String statusText) {
        new JTableDriver(this).hasCell(withLabelText(equalTo(statusText)));
    }
}
```

**Python 버전**:
```python
# 테스트 드라이버 - 레이블 대신 테이블 셀 찾기
class AuctionSniperDriver(JFrameDriver):
    def shows_sniper_status(self, status_text):
        """상태 텍스트를 테이블 셀에서 확인"""
        JTableDriver(self).has_cell(with_label_text(equal_to(status_text)))
```

```java
// 참조: content.md 64-97쪽
// MainWindow - 테이블 구조로 변경
public class MainWindow extends JFrame {
    private final SnipersTableModel snipers = new SnipersTableModel();

    public MainWindow() {
        super(APPLICATION_TITLE);
        setName(MainWindow.MAIN_WINDOW_NAME);
        fillContentPane(makeSnipersTable());  // 테이블로 콘텐츠 채우기
        pack();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    private void fillContentPane(JTable snipersTable) {
        final Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout());
        contentPane.add(new JScrollPane(snipersTable), BorderLayout.CENTER);
    }

    private JTable makeSnipersTable() {
        final JTable snipersTable = new JTable(snipers);
        snipersTable.setName(SNIPERS_TABLE_NAME);
        return snipersTable;
    }

    public void showStatusText(String statusText) {
        snipers.setStatusText(statusText);
    }
}

// SnipersTableModel - 최소 구현
public class SnipersTableModel extends AbstractTableModel {
    private String statusText = STATUS_JOINING;

    public int getColumnCount() { return 1; }
    public int getRowCount() { return 1; }
    public Object getValueAt(int rowIndex, int columnIndex) { return statusText; }

    public void setStatusText(String newStatusText) {
        statusText = newStatusText;
        fireTableRowsUpdated(0, 0);  // 테이블 업데이트 알림
    }
}
```

**Python 버전**:
```python
from javax.swing import JFrame, JTable, JScrollPane, BorderLayout
from javax.swing.table import AbstractTableModel

# MainWindow - 테이블 구조로 변경
class MainWindow(JFrame):
    def __init__(self):
        super().__init__(APPLICATION_TITLE)
        self.snipers = SnipersTableModel()

        self.set_name(MAIN_WINDOW_NAME)
        self._fill_content_pane(self._make_snipers_table())
        self.pack()
        self.set_default_close_operation(JFrame.EXIT_ON_CLOSE)
        self.set_visible(True)

    def _fill_content_pane(self, snipers_table):
        """테이블로 콘텐츠 영역 채우기"""
        content_pane = self.get_content_pane()
        content_pane.set_layout(BorderLayout())
        content_pane.add(JScrollPane(snipers_table), BorderLayout.CENTER)

    def _make_snipers_table(self):
        """스니퍼 테이블 생성"""
        snipers_table = JTable(self.snipers)
        snipers_table.set_name(SNIPERS_TABLE_NAME)
        return snipers_table

    def show_status_text(self, status_text):
        """상태 텍스트 표시"""
        self.snipers.set_status_text(status_text)

# SnipersTableModel - 최소 구현
class SnipersTableModel(AbstractTableModel):
    def __init__(self):
        super().__init__()
        self.status_text = STATUS_JOINING

    def get_column_count(self):
        return 1

    def get_row_count(self):
        return 1

    def get_value_at(self, row_index, column_index):
        """지정된 셀의 값 반환"""
        return self.status_text

    def set_status_text(self, new_status_text):
        """상태 텍스트 설정 및 테이블 업데이트"""
        self.status_text = new_status_text
        self.fire_table_rows_updated(0, 0)  # 테이블 업데이트 알림
```

---

### 화제 2: 가격 세부사항 표시 - 스니퍼 상태를 테이블로 전달
**참조**: content.md 111-189쪽
**핵심 개념**: 점진적 UI 개선

#### 이전 화제와의 관계
화제 1에서 구축한 기본 테이블 구조 위에 실제 데이터(아이템 ID, 가격, 입찰가, 상태)를 표시하는 기능 추가

#### 설명
스니퍼의 위치 정보(아이템 ID, 마지막 경매 가격, 마지막 입찰가, 상태)를 테이블에 표시. SniperState 값 타입을 도입하여 스니퍼 상태를 전달.

#### 주요 코드

```java
// 참조: content.md 121-135쪽
// 승인 테스트 - 가격 세부사항 검증
public class AuctionSniperEndToEndTest {
    @Test public void
    sniperWinsAnAuctionByBiddingHigher() throws Exception {
        auction.startSellingItem();
        application.startBiddingIn(auction);
        auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);

        auction.reportPrice(1000, 98, "other bidder");
        application.hasShownSniperIsBidding(1000, 1098); // 마지막 가격, 마지막 입찰가

        auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
        auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
        application.hasShownSniperIsWinning(1098); // 승리 입찰가

        auction.announceClosed();
        application.showsSniperHasWonAuction(1098); // 마지막 가격
    }
}
```

**Python 버전**:
```python
# 승인 테스트 - 가격 세부사항 검증
class AuctionSniperEndToEndTest:
    def test_sniper_wins_auction_by_bidding_higher(self):
        """스니퍼가 더 높은 입찰로 경매를 이기는 시나리오"""
        self.auction.start_selling_item()
        self.application.start_bidding_in(self.auction)
        self.auction.has_received_join_request_from(SNIPER_XMPP_ID)

        # 다른 입찰자가 1000에 입찰
        self.auction.report_price(1000, 98, "other bidder")
        self.application.has_shown_sniper_is_bidding(1000, 1098)  # 마지막 가격, 마지막 입찰가

        # 스니퍼가 1098에 입찰
        self.auction.has_received_bid(1098, SNIPER_XMPP_ID)
        self.auction.report_price(1098, 97, SNIPER_XMPP_ID)
        self.application.has_shown_sniper_is_winning(1098)  # 승리 입찰가

        # 경매 종료
        self.auction.announce_closed()
        self.application.shows_sniper_has_won_auction(1098)  # 마지막 가격
```

```java
// 참조: content.md 161-171쪽
// 테스트 드라이버 - 테이블 행 검증
public class AuctionSniperDriver extends JFrameDriver {
    public void showsSniperStatus(String itemId, int lastPrice, int lastBid,
                                  String statusText)
    {
        JTableDriver table = new JTableDriver(this);
        table.hasRow(
            matching(withLabelText(itemId), withLabelText(valueOf(lastPrice)),
                     withLabelText(valueOf(lastBid)), withLabelText(statusText)));
    }
}
```

**Python 버전**:
```python
# 테스트 드라이버 - 테이블 행 검증
class AuctionSniperDriver(JFrameDriver):
    def shows_sniper_status(self, item_id, last_price, last_bid, status_text):
        """스니퍼 상태를 테이블 행에서 검증"""
        table = JTableDriver(self)
        table.has_row(
            matching(
                with_label_text(item_id),
                with_label_text(str(last_price)),
                with_label_text(str(last_bid)),
                with_label_text(status_text)
            )
        )
```

```java
// 참조: content.md 204-213쪽
// SniperState 값 타입 도입
public class SniperState {
    public final String itemId;
    public final int lastPrice;
    public final int lastBid;

    public SniperState(String itemId, int lastPrice, int lastBid) {
        this.itemId = itemId;
        this.lastPrice = lastPrice;
        this.lastBid = lastBid;
    }
    // Apache commons.lang의 반사적 빌더로 equals(), hashCode(), toString() 구현
}
```

**Python 버전**:
```python
from dataclasses import dataclass

# SniperState 값 타입 도입
@dataclass(frozen=True)
class SniperState:
    """스니퍼 상태를 담는 불변 값 타입

    Attributes:
        item_id: 아이템 식별자
        last_price: 마지막 경매 가격
        last_bid: 마지막 입찰가
    """
    item_id: str
    last_price: int
    last_bid: int

    # dataclass가 자동으로 __eq__, __hash__, __repr__ 생성
```

```java
// 참조: content.md 232-258쪽
// AuctionSniper - SniperState 생성 및 전달
public class AuctionSniper implements AuctionEventListener {
    private final String itemId;

    public void currentPrice(int price, int increment, PriceSource priceSource) {
        isWinning = priceSource == PriceSource.FromSniper;
        if (isWinning) {
            sniperListener.sniperWinning();
        } else {
            int bid = price + increment;
            auction.bid(bid);
            sniperListener.sniperBidding(new SniperState(itemId, price, bid));
        }
    }
}
```

**Python 버전**:
```python
# AuctionSniper - SniperState 생성 및 전달
class AuctionSniper(AuctionEventListener):
    def __init__(self, item_id, auction, sniper_listener):
        self.item_id = item_id
        self.auction = auction
        self.sniper_listener = sniper_listener
        self.is_winning = False

    def current_price(self, price, increment, price_source):
        """현재 가격 업데이트 처리"""
        self.is_winning = (price_source == PriceSource.FROM_SNIPER)

        if self.is_winning:
            self.sniper_listener.sniper_winning()
        else:
            bid = price + increment
            self.auction.bid(bid)
            # SniperState 생성하여 리스너에 전달
            self.sniper_listener.sniper_bidding(
                SniperState(self.item_id, price, bid)
            )
```

```java
// 참조: content.md 305-351쪽
// Column 열거형 도입
public enum Column {
    ITEM_IDENTIFIER,
    LAST_PRICE,
    LAST_BID,
    SNIPER_STATUS;

    public static Column at(int offset) { return values()[offset]; }
}

// SnipersTableModel 테스트
@RunWith(JMock.class)
public class SnipersTableModelTest {
    private final Mockery context = new Mockery();
    private TableModelListener listener = context.mock(TableModelListener.class);
    private final SnipersTableModel model = new SnipersTableModel();

    @Before public void attachModelListener() {  // 1. 모델 리스너 연결
        model.addTableModelListener(listener);
    }

    @Test public void
    hasEnoughColumns() {  // 2. 컬럼 수 검증
        assertThat(model.getColumnCount(), equalTo(Column.values().length));
    }

    @Test public void
    setsSniperValuesInColumns() {
        context.checking(new Expectations() {{
            one(listener).tableChanged(with(aRowChangedEvent()));  // 3. 변경 알림 검증
        }});

        model.sniperStatusChanged(new SniperState("item id", 555, 666),  // 4. 이벤트 트리거
                                  MainWindow.STATUS_BIDDING);

        assertColumnEquals(Column.ITEM_IDENTIFIER, "item id");  // 5. 값 검증
        assertColumnEquals(Column.LAST_PRICE, 555);
        assertColumnEquals(Column.LAST_BID, 666);
        assertColumnEquals(Column.SNIPER_STATUS, MainWindow.STATUS_BIDDING);
    }

    private void assertColumnEquals(Column column, Object expected) {
        final int rowIndex = 0;
        final int columnIndex = column.ordinal();
        assertEquals(expected, model.getValueAt(rowIndex, columnIndex));
    }

    private Matcher<TableModelEvent> aRowChangedEvent() {  // 6. 이벤트 매처
        return samePropertyValuesAs(new TableModelEvent(model, 0));
    }
}
```

**Python 버전**:
```python
from enum import Enum, auto
from unittest.mock import Mock
import pytest

# Column 열거형 도입
class Column(Enum):
    """테이블 컬럼 정의"""
    ITEM_IDENTIFIER = auto()
    LAST_PRICE = auto()
    LAST_BID = auto()
    SNIPER_STATUS = auto()

    @classmethod
    def at(cls, offset):
        """인덱스로 컬럼 가져오기"""
        return list(cls)[offset]

# SnipersTableModel 테스트
class TestSnipersTableModel:
    def setup_method(self):
        """각 테스트 전 초기화"""
        self.listener = Mock()  # Mock 리스너
        self.model = SnipersTableModel()
        self.model.add_table_model_listener(self.listener)  # 1. 모델 리스너 연결

    def test_has_enough_columns(self):
        """2. 컬럼 수 검증"""
        assert self.model.get_column_count() == len(Column)

    def test_sets_sniper_values_in_columns(self):
        """스니퍼 값이 컬럼에 올바르게 설정되는지 검증"""
        # 4. 이벤트 트리거
        self.model.sniper_status_changed(
            SniperState("item id", 555, 666),
            STATUS_BIDDING
        )

        # 3. 변경 알림 검증
        self.listener.table_changed.assert_called_once()

        # 5. 값 검증
        self._assert_column_equals(Column.ITEM_IDENTIFIER, "item id")
        self._assert_column_equals(Column.LAST_PRICE, 555)
        self._assert_column_equals(Column.LAST_BID, 666)
        self._assert_column_equals(Column.SNIPER_STATUS, STATUS_BIDDING)

    def _assert_column_equals(self, column, expected):
        """지정된 컬럼의 값이 예상과 일치하는지 확인"""
        row_index = 0
        column_index = list(Column).index(column)
        actual = self.model.get_value_at(row_index, column_index)
        assert actual == expected
```

```java
// 참조: content.md 379-411쪽
// SnipersTableModel 구현
public class SnipersTableModel extends AbstractTableModel {
    private final static SniperState STARTING_UP = new SniperState("", 0, 0);  // 1. 초기 상태
    private String statusText = MainWindow.STATUS_JOINING;
    private SniperState sniperState = STARTING_UP;

    public int getColumnCount() {  // 2. 컬럼 수 반환
        return Column.values().length;
    }

    public int getRowCount() {
        return 1;
    }

    public Object getValueAt(int rowIndex, int columnIndex) {  // 3. 셀 값 반환
        switch (Column.at(columnIndex)) {
        case ITEM_IDENTIFIER:
            return sniperState.itemId;
        case LAST_PRICE:
            return sniperState.lastPrice;
        case LAST_BID:
            return sniperState.lastBid;
        case SNIPER_STATUS:
            return statusText;
        default:
            throw new IllegalArgumentException("No column at " + columnIndex);
        }
    }

    public void sniperStatusChanged(SniperState newSniperState,  // 4. 상태 변경
                                    String newStatusText)
    {
        sniperState = newSniperState;
        statusText = newStatusText;
        fireTableRowsUpdated(0, 0);
    }
}
```

**Python 버전**:
```python
from javax.swing.table import AbstractTableModel

# SnipersTableModel 구현
class SnipersTableModel(AbstractTableModel):
    # 1. 초기 상태
    STARTING_UP = SniperState("", 0, 0)

    def __init__(self):
        super().__init__()
        self.status_text = STATUS_JOINING
        self.sniper_state = self.STARTING_UP

    def get_column_count(self):
        """2. 컬럼 수 반환"""
        return len(Column)

    def get_row_count(self):
        return 1

    def get_value_at(self, row_index, column_index):
        """3. 셀 값 반환 - 컬럼별 분기"""
        column = Column.at(column_index)

        if column == Column.ITEM_IDENTIFIER:
            return self.sniper_state.item_id
        elif column == Column.LAST_PRICE:
            return self.sniper_state.last_price
        elif column == Column.LAST_BID:
            return self.sniper_state.last_bid
        elif column == Column.SNIPER_STATUS:
            return self.status_text
        else:
            raise ValueError(f"No column at {column_index}")

    def sniper_status_changed(self, new_sniper_state, new_status_text):
        """4. 상태 변경 및 테이블 업데이트"""
        self.sniper_state = new_sniper_state
        self.status_text = new_status_text
        self.fire_table_rows_updated(0, 0)
```

---

### 화제 3: 스니퍼 이벤트 단순화 - 여러 콜백을 하나로 통합
**참조**: content.md 448-565쪽
**핵심 개념**: 이벤트 단순화

#### 이전 화제와의 관계
화제 2에서 Bidding 이벤트를 구현한 후, Winning, Lost, Won 등 다른 이벤트도 같은 방식으로 구현해야 하는 반복 작업 발견. 이를 해결하기 위해 이벤트 메커니즘 자체를 단순화

#### 설명
4개의 콜백 메서드(sniperBidding, sniperWinning, sniperLost, sniperWon)를 하나의 sniperStateChanged()로 통합. SniperState를 SniperSnapshot으로 리네이밍하여 용어 명확화.

#### 주요 코드

```java
// 참조: content.md 497-516쪽
// SniperState 열거형 도입 (상태를 나타냄)
public enum SniperState {
    JOINING,
    BIDDING,
    WINNING,
    LOST,
    WON;
}

// AuctionSniper - 통합된 이벤트 사용
public class AuctionSniper implements AuctionEventListener {
    public void currentPrice(int price, int increment, PriceSource priceSource) {
        isWinning = priceSource == PriceSource.FromSniper;
        if (isWinning) {
            sniperListener.sniperWinning();
        } else {
            final int bid = price + increment;
            auction.bid(bid);
            sniperListener.sniperStateChanged(
                new SniperSnapshot(itemId, price, bid, SniperState.BIDDING));
        }
    }
}
```

**Python 버전**:
```python
from enum import Enum, auto

# SniperState 열거형 도입 (상태를 나타냄)
class SniperState(Enum):
    """스니퍼의 경매 내 상태"""
    JOINING = auto()    # 경매 참여 중
    BIDDING = auto()    # 입찰 중
    WINNING = auto()    # 승리 중
    LOST = auto()       # 패배
    WON = auto()        # 승리

# AuctionSniper - 통합된 이벤트 사용
class AuctionSniper(AuctionEventListener):
    def current_price(self, price, increment, price_source):
        """현재 가격 업데이트 처리"""
        self.is_winning = (price_source == PriceSource.FROM_SNIPER)

        if self.is_winning:
            self.sniper_listener.sniper_winning()
        else:
            bid = price + increment
            self.auction.bid(bid)
            # 통합된 이벤트로 상태 전달
            self.sniper_listener.sniper_state_changed(
                SniperSnapshot(self.item_id, price, bid, SniperState.BIDDING)
            )
```

```java
// 참조: content.md 524-532쪽
// SnipersTableModel - 상태 텍스트 배열로 변환
public class SnipersTableModel extends AbstractTableModel {
    private static String[] STATUS_TEXT = { MainWindow.STATUS_JOINING,
                                            MainWindow.STATUS_BIDDING };

    public void sniperStateChanged(SniperSnapshot newSnapshot) {
        this.snapshot = newSnapshot;
        this.state = STATUS_TEXT[newSnapshot.state.ordinal()];
        fireTableRowsUpdated(0, 0);
    }
}
```

**Python 버전**:
```python
# SnipersTableModel - 상태 텍스트 배열로 변환
class SnipersTableModel(AbstractTableModel):
    STATUS_TEXT = [STATUS_JOINING, STATUS_BIDDING]

    def sniper_state_changed(self, new_snapshot):
        """스니퍼 상태 변경 처리"""
        self.snapshot = new_snapshot
        # 열거형 순서로 상태 텍스트 인덱싱
        self.state = self.STATUS_TEXT[new_snapshot.state.value - 1]
        self.fire_table_rows_updated(0, 0)
```

```java
// 참조: content.md 541-561쪽
// 커스텀 매처 - 상태만 검증
public class AuctionSniperTest {
    context.checking(new Expectations() {{
        ignoring(auction);
        allowing(sniperListener).sniperStateChanged(
                                   with(aSniperThatIs(BIDDING)));
                                                then(sniperState.is("bidding"));
        atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
    }});

    private Matcher<SniperSnapshot> aSniperThatIs(final SniperState state) {
        return new FeatureMatcher<SniperSnapshot, SniperState>(
                 equalTo(state), "sniper that is ", "was")
        {
            @Override
            protected SniperState featureValueOf(SniperSnapshot actual) {
                return actual.state;
            }
        };
    }
}
```

**Python 버전**:
```python
from unittest.mock import Mock, ANY
from hamcrest import equal_to, has_property

# 커스텀 매처 - 상태만 검증
class TestAuctionSniper:
    def test_sniper_bidding(self):
        """스니퍼 입찰 상태 테스트"""
        # 매처를 사용한 기대값 설정
        self.sniper_listener.sniper_state_changed = Mock()

        # ... 테스트 실행 ...

        # 상태만 검증하는 커스텀 매처
        self.sniper_listener.sniper_state_changed.assert_called_with(
            self._a_sniper_that_is(SniperState.BIDDING)
        )

    def _a_sniper_that_is(self, state):
        """특정 상태를 가진 스니퍼 매처"""
        return has_property('state', equal_to(state))
```

```java
// 참조: content.md 583-601쪽
// Winning 상태로 변환
public class AuctionSniperTest {
    @Test public void
    reportsIsWinningWhenCurrentPriceComesFromSniper() {
        context.checking(new Expectations() {{
            ignoring(auction);
            allowing(sniperListener).sniperStateChanged(
                                       with(aSniperThatIs(BIDDING)));
                                                   then(sniperState.is("bidding"));
            atLeast(1).of(sniperListener).sniperStateChanged(
                                   new SniperSnapshot(ITEM_ID, 135, 135, WINNING));
                                                   when(sniperState.is("bidding"));
        }});

        sniper.currentPrice(123, 12, PriceSource.FromOtherBidder);
        sniper.currentPrice(135, 45, PriceSource.FromSniper);
    }
}
```

**Python 버전**:
```python
# Winning 상태로 변환 테스트
class TestAuctionSniper:
    def test_reports_is_winning_when_current_price_comes_from_sniper(self):
        """스니퍼가 현재 가격을 제시했을 때 승리 상태 보고"""
        # 기대값 설정
        calls = []
        def track_calls(snapshot):
            calls.append(snapshot)

        self.sniper_listener.sniper_state_changed = track_calls

        # 먼저 다른 입찰자의 가격으로 입찰 상태로 전환
        self.sniper.current_price(123, 12, PriceSource.FROM_OTHER_BIDDER)
        assert calls[-1].state == SniperState.BIDDING

        # 스니퍼의 가격으로 승리 상태로 전환
        self.sniper.current_price(135, 45, PriceSource.FROM_SNIPER)
        expected = SniperSnapshot(ITEM_ID, 135, 135, SniperState.WINNING)
        assert calls[-1] == expected
```

```java
// 참조: content.md 607-637쪽
// SniperSnapshot - 헬퍼 메서드 추가
public class AuctionSniper implements AuctionEventListener {
    private SniperSnapshot snapshot;

    public AuctionSniper(String itemId, Auction auction, SniperListener sniperListener)
    {
        this.auction = auction;
        this.sniperListener = sniperListener;
        this.snapshot = SniperSnapshot.joining(itemId);
    }

    public void currentPrice(int price, int increment, PriceSource priceSource) {
        isWinning = priceSource == PriceSource.FromSniper;
        if (isWinning) {
            snapshot = snapshot.winning(price);
        } else {
            final int bid = price + increment;
            auction.bid(bid);
            snapshot = snapshot.bidding(price, bid);
        }
        sniperListener.sniperStateChanged(snapshot);
    }
}

public class SniperSnapshot {
    public SniperSnapshot bidding(int newLastPrice, int newLastBid) {
        return new SniperSnapshot(itemId, newLastPrice, newLastBid, SniperState.BIDDING);
    }

    public SniperSnapshot winning(int newLastPrice) {
        return new SniperSnapshot(itemId, newLastPrice, lastBid, SniperState.WINNING);
    }

    public static SniperSnapshot joining(String itemId) {
        return new SniperSnapshot(itemId, 0, 0, SniperState.JOINING);
    }
}
```

**Python 버전**:
```python
from dataclasses import dataclass, replace

# SniperSnapshot - 헬퍼 메서드 추가
@dataclass(frozen=True)
class SniperSnapshot:
    """스니퍼의 특정 시점 스냅샷"""
    item_id: str
    last_price: int
    last_bid: int
    state: SniperState

    def bidding(self, new_last_price, new_last_bid):
        """입찰 중 상태의 새 스냅샷 생성"""
        return SniperSnapshot(
            self.item_id,
            new_last_price,
            new_last_bid,
            SniperState.BIDDING
        )

    def winning(self, new_last_price):
        """승리 중 상태의 새 스냅샷 생성"""
        return SniperSnapshot(
            self.item_id,
            new_last_price,
            self.last_bid,  # 입찰가는 유지
            SniperState.WINNING
        )

    @classmethod
    def joining(cls, item_id):
        """참여 중 상태의 초기 스냅샷 생성"""
        return cls(item_id, 0, 0, SniperState.JOINING)

# AuctionSniper에서 사용
class AuctionSniper(AuctionEventListener):
    def __init__(self, item_id, auction, sniper_listener):
        self.auction = auction
        self.sniper_listener = sniper_listener
        self.snapshot = SniperSnapshot.joining(item_id)  # 초기 스냅샷

    def current_price(self, price, increment, price_source):
        """현재 가격 업데이트 처리"""
        is_winning = (price_source == PriceSource.FROM_SNIPER)

        if is_winning:
            self.snapshot = self.snapshot.winning(price)
        else:
            bid = price + increment
            self.auction.bid(bid)
            self.snapshot = self.snapshot.bidding(price, bid)

        # 통합된 이벤트로 스냅샷 전달
        self.sniper_listener.sniper_state_changed(self.snapshot)
```

---

### 화제 4: 후속 작업 - Won과 Lost 상태 변환
**참조**: content.md 650-728쪽
**핵심 개념**: 이벤트 단순화, 객체지향적 리팩토링

#### 이전 화제와의 관계
화제 3에서 Bidding과 Winning을 sniperStateChanged()로 통합한 것과 동일한 방식으로 Won과 Lost도 변환

#### 설명
sniperWon()과 sniperLost()를 sniperStateChanged()로 변환. isWinning 필드 제거하고 의사결정 로직을 SniperSnapshot과 SniperState로 이동.

#### 주요 코드

```java
// 참조: content.md 660-681쪽
// AuctionSniper - 간소화된 구조
public class AuctionSniper implements AuctionEventListener {
    public void auctionClosed() {
        snapshot = snapshot.closed();
        notifyChange();
    }

    public void currentPrice(int price, int increment, PriceSource priceSource) {
        switch(priceSource) {
        case FromSniper:
            snapshot = snapshot.winning(price);
            break;
        case FromOtherBidder:
            int bid = price + increment;
            auction.bid(bid);
            snapshot = snapshot.bidding(price, bid);
            break;
        }
        notifyChange();
    }

    private void notifyChange() {
        sniperListener.sniperStateChanged(snapshot);
    }
}
```

**Python 버전**:
```python
# AuctionSniper - 간소화된 구조
class AuctionSniper(AuctionEventListener):
    def auction_closed(self):
        """경매 종료 처리"""
        self.snapshot = self.snapshot.closed()
        self._notify_change()

    def current_price(self, price, increment, price_source):
        """현재 가격 업데이트 처리 - switch 문 대신 if-elif 사용"""
        if price_source == PriceSource.FROM_SNIPER:
            self.snapshot = self.snapshot.winning(price)
        elif price_source == PriceSource.FROM_OTHER_BIDDER:
            bid = price + increment
            self.auction.bid(bid)
            self.snapshot = self.snapshot.bidding(price, bid)

        self._notify_change()

    def _notify_change(self):
        """변경 사항을 리스너에 알림"""
        self.sniper_listener.sniper_state_changed(self.snapshot)
```

```java
// 참조: content.md 684-709쪽
// SniperSnapshot과 SniperState - 의사결정 로직 이동
public class SniperSnapshot {
    public SniperSnapshot closed() {
        return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
    }
}

public enum SniperState {
    JOINING {
        @Override public SniperState whenAuctionClosed() { return LOST; }
    },
    BIDDING {
        @Override public SniperState whenAuctionClosed() { return LOST; }
    },
    WINNING {
        @Override public SniperState whenAuctionClosed() { return WON; }
    },
    LOST,
    WON;

    public SniperState whenAuctionClosed() {
        throw new Defect("Auction is already closed");
    }
}
```

**Python 버전**:
```python
from enum import Enum

class DefectException(Exception):
    """프로그래밍 오류로 인한 예외"""
    pass

# SniperState - 의사결정 로직 포함
class SniperState(Enum):
    """스니퍼의 경매 내 상태 및 상태 전이 로직"""
    JOINING = "joining"
    BIDDING = "bidding"
    WINNING = "winning"
    LOST = "lost"
    WON = "won"

    def when_auction_closed(self):
        """경매 종료 시 최종 상태 결정"""
        if self == SniperState.JOINING:
            return SniperState.LOST
        elif self == SniperState.BIDDING:
            return SniperState.LOST
        elif self == SniperState.WINNING:
            return SniperState.WON
        else:
            # LOST나 WON에서 다시 종료되면 프로그래밍 오류
            raise DefectException("Auction is already closed")

# SniperSnapshot에서 사용
@dataclass(frozen=True)
class SniperSnapshot:
    item_id: str
    last_price: int
    last_bid: int
    state: SniperState

    def closed(self):
        """경매 종료 상태의 새 스냅샷 생성"""
        return SniperSnapshot(
            self.item_id,
            self.last_price,
            self.last_bid,
            self.state.when_auction_closed()  # 상태에게 최종 상태 결정 위임
        )
```

---

### 화제 5: 테이블 모델 다듬기 - 불필요한 코드 제거
**참조**: content.md 730-764쪽
**핵심 개념**: 객체지향적 리팩토링

#### 이전 화제와의 관계
화제 4에서 모든 이벤트를 sniperStateChanged()로 통합한 후, 이제 불필요해진 코드 정리

#### 설명
setStatusText() 접근자 제거. 상태 표시 문자열 상수를 MainWindow에서 SnipersTableModel로 이동.

#### 주요 코드

```java
// 참조: content.md 735-760쪽
// SnipersTableModel - 상수 이동 및 헬퍼 메서드
public class SnipersTableModel extends AbstractTableModel {
    private final static String[] STATUS_TEXT = {
        "Joining", "Bidding", "Winning", "Lost", "Won"
    };

    public Object getValueAt(int rowIndex, int columnIndex) {
        switch (Column.at(columnIndex)) {
        case ITEM_IDENTIFIER:
            return snapshot.itemId;
        case LAST_PRICE:
            return snapshot.lastPrice;
        case LAST_BID:
            return snapshot.lastBid;
        case SNIPER_STATE:
            return textFor(snapshot.state);
        default:
            throw new IllegalArgumentException("No column at" + columnIndex);
        }
    }

    public void sniperStateChanged(SniperSnapshot newSnapshot) {
        this.snapshot = newSnapshot;
        fireTableRowsUpdated(0, 0);
    }

    public static String textFor(SniperState state) {
        return STATUS_TEXT[state.ordinal()];
    }
}
```

**Python 버전**:
```python
# SnipersTableModel - 상수 이동 및 헬퍼 메서드
class SnipersTableModel(AbstractTableModel):
    STATUS_TEXT = [
        "Joining", "Bidding", "Winning", "Lost", "Won"
    ]

    def get_value_at(self, row_index, column_index):
        """셀 값 반환"""
        column = Column.at(column_index)

        if column == Column.ITEM_IDENTIFIER:
            return self.snapshot.item_id
        elif column == Column.LAST_PRICE:
            return self.snapshot.last_price
        elif column == Column.LAST_BID:
            return self.snapshot.last_bid
        elif column == Column.SNIPER_STATE:
            return self.text_for(self.snapshot.state)
        else:
            raise ValueError(f"No column at {column_index}")

    def sniper_state_changed(self, new_snapshot):
        """스니퍼 상태 변경 처리"""
        self.snapshot = new_snapshot
        self.fire_table_rows_updated(0, 0)

    @staticmethod
    def text_for(state):
        """상태를 표시 텍스트로 변환"""
        return SnipersTableModel.STATUS_TEXT[state.value - 1]
```

---

### 화제 6: 객체지향적 컬럼 - switch 문을 다형성으로 대체
**참조**: content.md 764-810쪽
**핵심 개념**: 객체지향적 리팩토링

#### 이전 화제와의 관계
화제 5에서 테이블 모델을 정리한 후, switch 문을 더 객체지향적인 방식으로 대체

#### 설명
switch 문을 Column 열거형의 추상 메서드로 대체하여 더 객체지향적이고 간결한 코드 작성.

#### 주요 코드

```java
// 참조: content.md 777-806쪽
// Column - 추상 메서드로 각 컬럼의 값 추출
public enum Column {
    ITEM_IDENTIFIER {
        @Override public Object valueIn(SniperSnapshot snapshot) {
            return snapshot.itemId;
        }
    },
    LAST_PRICE {
        @Override public Object valueIn(SniperSnapshot snapshot) {
            return snapshot.lastPrice;
        }
    },
    LAST_BID{
        @Override public Object valueIn(SniperSnapshot snapshot) {
            return snapshot.lastBid;
        }
    },
    SNIPER_STATE {
        @Override public Object valueIn(SniperSnapshot snapshot) {
            return SnipersTableModel.textFor(snapshot.state);
        }
    };

    abstract public Object valueIn(SniperSnapshot snapshot);
}

// SnipersTableModel - 간결해진 구현
public class SnipersTableModel extends AbstractTableModel {
    public Object getValueAt(int rowIndex, int columnIndex) {
        return Column.at(columnIndex).valueIn(snapshot);
    }
}
```

**Python 버전**:
```python
from enum import Enum
from abc import ABC, abstractmethod

# Column - 추상 메서드로 각 컬럼의 값 추출
class Column(Enum):
    """테이블 컬럼과 값 추출 로직"""

    class _ColumnType(ABC):
        @abstractmethod
        def value_in(self, snapshot):
            """스냅샷에서 컬럼 값 추출"""
            pass

    class _ItemIdentifier(_ColumnType):
        def value_in(self, snapshot):
            return snapshot.item_id

    class _LastPrice(_ColumnType):
        def value_in(self, snapshot):
            return snapshot.last_price

    class _LastBid(_ColumnType):
        def value_in(self, snapshot):
            return snapshot.last_bid

    class _SniperState(_ColumnType):
        def value_in(self, snapshot):
            return SnipersTableModel.text_for(snapshot.state)

    ITEM_IDENTIFIER = _ItemIdentifier()
    LAST_PRICE = _LastPrice()
    LAST_BID = _LastBid()
    SNIPER_STATE = _SniperState()

    @classmethod
    def at(cls, offset):
        """인덱스로 컬럼 가져오기"""
        return list(cls)[offset].value

# SnipersTableModel - 간결해진 구현
class SnipersTableModel(AbstractTableModel):
    def get_value_at(self, row_index, column_index):
        """셀 값 반환 - Column에 위임"""
        return Column.at(column_index).value_in(self.snapshot)
```

---

### 화제 7: 이벤트 경로 단축 - 불필요한 전달 호출 제거
**참조**: content.md 810-857쪽
**핵심 개념**: 객체지향적 리팩토링

#### 이전 화제와의 관계
화제 6에서 Column을 정리한 후, 이제 전체 이벤트 전달 경로를 단순화

#### 설명
MainWindow와 SniperStateDisplayer의 단순 전달 호출을 제거. SnipersTableModel이 직접 SniperListener를 구현하도록 변경. SniperStateDisplayer를 Decorator로 변경하고 SwingThreadSniperListener로 리네이밍.

#### 주요 코드

```java
// 참조: content.md 814-829쪽
// 변경 전 - 불필요한 전달 호출
public class MainWindow extends JFrame {
    public void sniperStateChanged(SniperSnapshot snapshot) {
        snipers.sniperStateChanged(snapshot);  // 단순 전달
    }
}

public class SniperStateDisplayer implements SniperListener {
    public void sniperStateChanged(final SniperSnapshot snapshot) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() { mainWindow.sniperStateChanged(snapshot); }  // 단순 전달
        });
    }
}
```

**Python 버전**:
```python
# 변경 전 - 불필요한 전달 호출
class MainWindow(JFrame):
    def sniper_state_changed(self, snapshot):
        """단순 전달만 수행"""
        self.snipers.sniper_state_changed(snapshot)

class SniperStateDisplayer(SniperListener):
    def sniper_state_changed(self, snapshot):
        """Swing 스레드로 전달"""
        def update():
            self.main_window.sniper_state_changed(snapshot)

        SwingUtilities.invoke_later(update)
```

```java
// 참조: content.md 837-856쪽
// 변경 후 - 직접 연결
public class Main {
    private final SnipersTableModel snipers = new SnipersTableModel();
    private MainWindow ui;

    public Main() throws Exception {
        SwingUtilities.invokeAndWait(new Runnable() {
            public void run() { ui = new MainWindow(snipers); }
        });
    }

    private void joinAuction(XMPPConnection connection, String itemId) {
        Auction auction = new XMPPAuction(chat);
        chat.addMessageListener(
            new AuctionMessageTranslator(
                connection.getUser(),
                new AuctionSniper(itemId, auction,
                    new SwingThreadSniperListener(snipers))));  // 직접 연결
        auction.join();
    }
}
```

**Python 버전**:
```python
# 변경 후 - 직접 연결
class Main:
    def __init__(self):
        self.snipers = SnipersTableModel()

        def create_ui():
            self.ui = MainWindow(self.snipers)

        SwingUtilities.invoke_and_wait(create_ui)

    def join_auction(self, connection, item_id):
        """경매 참여 - 테이블 모델에 직접 연결"""
        auction = XMPPAuction(chat)

        # 직접 테이블 모델을 리스너로 사용 (Swing 스레드 래퍼로 감쌈)
        chat.add_message_listener(
            AuctionMessageTranslator(
                connection.get_user(),
                AuctionSniper(
                    item_id,
                    auction,
                    SwingThreadSniperListener(self.snipers)  # 직접 연결
                )
            )
        )
        auction.join()
```

---

### 화제 8: 마지막 손질 - 컬럼 타이틀 테스트 및 구현
**참조**: content.md 857-965쪽
**핵심 개념**: 점진적 UI 개선

#### 이전 화제와의 관계
화제 7에서 이벤트 경로를 정리한 후, UI의 마지막 디테일인 컬럼 타이틀 추가

#### 설명
테이블의 컬럼 타이틀을 추가하여 UI를 완성. Column 열거형에 타이틀 필드 추가하고 SnipersTableModel에서 참조.

#### 주요 코드

```java
// 참조: content.md 872-893쪽
// 승인 테스트 - 컬럼 타이틀 검증
public class ApplicationRunner {
    public void startBiddingIn(final FakeAuctionServer auction) {
        itemId = auction.getItemId();
        Thread thread = new Thread("Test Application") { /* ... */ };
        thread.setDaemon(true);
        thread.start();
        driver = new AuctionSniperDriver(1000);
        driver.hasTitle(MainWindow.APPLICATION_TITLE);
        driver.hasColumnTitles();  // 컬럼 타이틀 검증
        driver.showsSniperStatus(JOINING.itemId, JOINING.lastPrice,
                                 JOINING.lastBid, textFor(SniperState.JOINING));
    }
}

public class AuctionSniperDriver extends JFrameDriver {
    public void hasColumnTitles() {
        JTableHeaderDriver headers = new JTableHeaderDriver(this, JTableHeader.class);
        headers.hasHeaders(matching(withLabelText("Item"), withLabelText("Last Price"),
                                    withLabelText("Last Bid"), withLabelText("State")));
    }
}
```

**Python 버전**:
```python
# 승인 테스트 - 컬럼 타이틀 검증
class ApplicationRunner:
    def start_bidding_in(self, auction):
        """경매 참여 시작 및 UI 검증"""
        self.item_id = auction.get_item_id()

        # 애플리케이션 스레드 시작
        thread = Thread(target=self._run_application, daemon=True)
        thread.start()

        self.driver = AuctionSniperDriver(1000)
        self.driver.has_title(APPLICATION_TITLE)
        self.driver.has_column_titles()  # 컬럼 타이틀 검증
        self.driver.shows_sniper_status(
            JOINING.item_id,
            JOINING.last_price,
            JOINING.last_bid,
            text_for(SniperState.JOINING)
        )

class AuctionSniperDriver(JFrameDriver):
    def has_column_titles(self):
        """컬럼 타이틀 존재 확인"""
        headers = JTableHeaderDriver(self, JTableHeader)
        headers.has_headers(
            matching(
                with_label_text("Item"),
                with_label_text("Last Price"),
                with_label_text("Last Bid"),
                with_label_text("State")
            )
        )
```

```java
// 참조: content.md 920-935쪽
// Column - 타이틀 필드 추가
public enum Column {
    ITEM_IDENTIFIER("Item") { /* ... */ },
    LAST_PRICE("Last Price") { /* ... */ },
    LAST_BID("Last Bid") { /* ... */ },
    SNIPER_STATE("State") { /* ... */ };

    public final String name;

    private Column(String name) {
        this.name = name;
    }
}

// SnipersTableModel - 컬럼 이름 반환
public class SnipersTableModel extends AbstractTableModel implements SniperListener {
    @Override public String getColumnName(int column) {
        return Column.at(column).name;
    }
}
```

**Python 버전**:
```python
# Column - 타이틀 필드 추가
class Column(Enum):
    """테이블 컬럼과 타이틀"""

    class _ColumnType(ABC):
        def __init__(self, name):
            self.name = name

        @abstractmethod
        def value_in(self, snapshot):
            pass

    class _ItemIdentifier(_ColumnType):
        def __init__(self):
            super().__init__("Item")

        def value_in(self, snapshot):
            return snapshot.item_id

    class _LastPrice(_ColumnType):
        def __init__(self):
            super().__init__("Last Price")

        def value_in(self, snapshot):
            return snapshot.last_price

    class _LastBid(_ColumnType):
        def __init__(self):
            super().__init__("Last Bid")

        def value_in(self, snapshot):
            return snapshot.last_bid

    class _SniperState(_ColumnType):
        def __init__(self):
            super().__init__("State")

        def value_in(self, snapshot):
            return SnipersTableModel.text_for(snapshot.state)

    ITEM_IDENTIFIER = _ItemIdentifier()
    LAST_PRICE = _LastPrice()
    LAST_BID = _LastBid()
    SNIPER_STATE = _SniperState()

    @classmethod
    def at(cls, offset):
        return list(cls)[offset].value

# SnipersTableModel - 컬럼 이름 반환
class SnipersTableModel(AbstractTableModel, SniperListener):
    def get_column_name(self, column):
        """컬럼 타이틀 반환"""
        return Column.at(column).name
```

```java
// 참조: content.md 939-946쪽
// 단위 테스트 - 모든 컬럼 타이틀 검증
public class SnipersTableModelTest {
    @Test public void
    setsUpColumnHeadings() {
        for (Column column: Column.values()) {
            assertEquals(column.name, model.getColumnName(column.ordinal()));
        }
    }
}
```

**Python 버전**:
```python
# 단위 테스트 - 모든 컬럼 타이틀 검증
class TestSnipersTableModel:
    def test_sets_up_column_headings(self):
        """모든 컬럼의 타이틀이 올바르게 설정되는지 검증"""
        for i, column in enumerate(Column):
            expected_name = column.value.name
            actual_name = self.model.get_column_name(i)
            assert actual_name == expected_name
```
