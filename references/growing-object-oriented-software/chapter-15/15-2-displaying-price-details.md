# 15.2 Displaying Price Details (pp.152-159)

---
**Page 152**

Still Ugly
As you can see, the SnipersTableModel really is a minimal implementation; the
only value that can vary is the statusText. It inherits most of its behavior from
the Swing AbstractTableModel, including the infrastructure for notifying the
JTable of data changes. The result is as ugly as our previous version, except that
now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
on the presentation in a moment.
Figure 15.2
Sniper with a single-cell table
Displaying Price Details
First, a Failing Test
Our next task is to display information about the Sniper’s position in the auction:
item identiﬁer, last auction price, last bid, status. These values come from updates
from the auction and the state held within the application. We need to pass them
through from their source to the table model and then render them in the display.
Of course, we start with the test. Given that this feature should be part of the
basic functionality of the application, not separate from what we already have,
we update our existing acceptance tests—starting with just one test so we don’t
break everything at once. Here’s the new version:
public class AuctionSniperEndToEndTest {
  @Test public void
sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning(1098); // winning bid
    auction.announceClosed();
    application.showsSniperHasWonAuction(1098); // last price
  }
}
Chapter 15
Towards a Real User Interface
152


---
**Page 153**

public class ApplicationRunner {
private String itemId;
  public void startBiddingIn(final FakeAuctionServer auction) {
itemId = auction.getItemId();
[…]
  }
[…]
  public void hasShownSniperIsBidding(int lastPrice, int lastBid) {
    driver.showsSniperStatus(itemId, lastPrice, lastBid, 
                             MainWindow.STATUS_BIDDING);
  }
  public void hasShownSniperIsWinning(int winningBid) {
    driver.showsSniperStatus(itemId, winningBid, winningBid, 
                             MainWindow.STATUS_WINNING);
  }
  public void showsSniperHasWonAuction(int lastPrice) {
    driver.showsSniperStatus(itemId, lastPrice, lastPrice, 
                             MainWindow.STATUS_WON);
  }
}
public class AuctionSniperDriver extends JFrameDriver {
[…]
  public void showsSniperStatus(String itemId, int lastPrice, int lastBid, 
                                String statusText)
  {
    JTableDriver table = new JTableDriver(this);
    table.hasRow(
      matching(withLabelText(itemId), withLabelText(valueOf(lastPrice)), 
               withLabelText(valueOf(lastBid)), withLabelText(statusText)));
  }
}
We need the item identiﬁer so the test can look for it in the row, so we make
the ApplicationRunner hold on it when connecting to an auction. We extend the
AuctionSniperDriver to look for a table row that shows the item identiﬁer, last
price, last bid, and sniper status.
The test fails because the row has no details, only the status text:
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
 it is not with row with cells 
   <label with text "item-54321">, <label with text "1000">, 
   <label with text "1098">, <label with text "Bidding">
because 
      in row 0: component 0 text was "Bidding"
153
Displaying Price Details


---
**Page 154**

Sending the State out of the Sniper
With an acceptance test to show us where we want to get to, we can ﬁll in the
steps along the way. As usual, we work “outside-in,” from the event that triggers
the behavior; in this case it’s a price update from Southabee’s On-Line.
Following along the sequence of method calls, we don’t have to change
AuctionMessageTranslator, so we start by looking at AuctionSniper and its
unit tests.
AuctionSniper notiﬁes changes in its state to neighbors that implement the
SniperListener interface which, as you might remember, has four callback
methods, one for each state of the Sniper. Now we also need to pass in the current
state of the Sniper when we notify a listener. We could add the same set of argu-
ments to each method, but that would be duplication; so, we introduce a value
type to carry the Sniper’s state. This is an example of “bundling up” that we
described in “Value Types” (page 59). Here’s a ﬁrst cut:
public class SniperState {
  public final String itemId;
  public final int lastPrice;
  public final int lastBid;
  public SniperState(String itemId, int lastPrice, int lastBid) {
    this.itemId = itemId;
    this.lastPrice = lastPrice;
    this.lastBid = lastBid;
  }
}
To save effort, we use the reﬂective builders from the Apache commons.lang
library to implement equals(), hashCode(), and toString() in the new class. We
could argue that we’re being premature with these features, but in practice we’ll
need them in a moment when we write our unit tests.
Public Final Fields
We’ve adopted a habit of using public ﬁnal ﬁelds in value types, at least while we’re
in the process of sorting out what the type should do. It makes it obvious that the
value is immutable and reduces the overhead of maintaining getters when the class
isn’t yet stable. Our ambition, which we might not achieve, is to replace all ﬁeld
access with meaningful action methods on the type. We’ll see how that pans out.
We don’t want to break all the tests at once, so we start with an easy one. In
this test there’s no history, all we have to do in the Sniper is construct a
SniperState from information available at the time and pass it to the listener.
Chapter 15
Towards a Real User Interface
154


---
**Page 155**

public class AuctionSniperTest { […]
  @Test public void
bidsHigherAndReportsBiddingWhenNewPriceArrives() {
    final int price = 1001;
    final int increment = 25;
    final int bid = price + increment;
    context.checking(new Expectations() {{
      one(auction).bid(bid);
      atLeast(1).of(sniperListener).sniperBidding(
new SniperState(ITEM_ID, price, bid));
    }});
    sniper.currentPrice(price, increment, PriceSource.FromOtherBidder);
  }
}
Then we make the test pass:
public class AuctionSniper implements AuctionEventListener { […]
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
To get the code to compile, we also add the state argument to the
sniperBidding() method in 
SniperStateDisplayer, which implements
SniperListener, but don’t yet do anything with it.
The one signiﬁcant change is that the Sniper needs access to the item identiﬁer
so it can construct a SniperState. Given that the Sniper doesn’t need this value
for any other reason, we could have kept it in the SniperStateDisplayer and
added it in when an event passes through, but we think it’s reasonable that the
Sniper has access to this information. We decide to pass the identiﬁer into the
AuctionSniper constructor; it’s available at the time, and we don’t want to get
it from the Auction object which may have its own form of identiﬁer for an item.
We have one other test that refers to the sniperBidding() method, but only
as an “allowance.” We use a matcher that says that, since it’s only supporting
the interesting part of the test, we don’t care about the contents of the state object.
allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Showing a Bidding Sniper
We’ll take larger steps for the next task—presenting the state in the user
interface—as there are some new moving parts, including a new unit test. The
155
Displaying Price Details


---
**Page 156**

ﬁrst version of the code will be clumsier than we would like but, as you’ll soon
see, there’ll be interesting opportunities for cleaning up.
Our very ﬁrst step is to pass the new state parameter, which we’ve been ignor-
ing, through MainWindow to a new method in SnipersTableModel. While we’re at
it, we notice that just passing events through MainWindow isn’t adding much value,
so we make a note to deal with that later.
public class SniperStateDisplayer implements SniperListener { […]
  public void sniperBidding(final SniperState state) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() { 
ui.sniperStatusChanged(state, MainWindow.STATUS_BIDDING);
      } 
    });
  }
}
public class MainWindow extends JFrame { […]
  public void sniperStatusChanged(SniperState sniperState, String statusText) {
    snipers.sniperStatusChanged(sniperState, statusText);
  }
}
To get the new values visible on screen, we need to ﬁx SnipersTableModel so
that it makes them available to its JTable, starting with a unit test. We take a
small design leap by introducing a Java enum to represent the columns in the
table—it’s more meaningful than just using integers.
public enum Column {
  ITEM_IDENTIFIER,
  LAST_PRICE,
  LAST_BID,
  SNIPER_STATUS;
  public static Column at(int offset) { return values()[offset]; }
}
The table model needs to do two things when its state changes: hold onto the
new values and notify the table that they’ve changed. Here’s the test:
@RunWith(JMock.class)
public class SnipersTableModelTest {
  private final Mockery context = new Mockery();
  private TableModelListener listener = context.mock(TableModelListener.class);
  private final SnipersTableModel model = new SnipersTableModel();
  @Before public void attachModelListener() {  1
    model.addTableModelListener(listener);
  }
  @Test public void
hasEnoughColumns() {  2
    assertThat(model.getColumnCount(), equalTo(Column.values().length));
  }
Chapter 15
Towards a Real User Interface
156


---
**Page 157**

  @Test public void
setsSniperValuesInColumns() {
    context.checking(new Expectations() {{
      one(listener).tableChanged(with(aRowChangedEvent()));  3
    }});
    model.sniperStatusChanged(new SniperState("item id", 555, 666),  4
                              MainWindow.STATUS_BIDDING);
    assertColumnEquals(Column.ITEM_IDENTIFIER, "item id"); 5
    assertColumnEquals(Column.LAST_PRICE, 555);
    assertColumnEquals(Column.LAST_BID, 666);
    assertColumnEquals(Column.SNIPER_STATUS, MainWindow.STATUS_BIDDING);
  }
  private void assertColumnEquals(Column column, Object expected) {
    final int rowIndex = 0;
    final int columnIndex = column.ordinal();
    assertEquals(expected, model.getValueAt(rowIndex, columnIndex);
  }
  private Matcher<TableModelEvent> aRowChangedEvent() { 6
    return samePropertyValuesAs(new TableModelEvent(model, 0));
  }
}
1
We attach a mock implementation of TableModelListener to the model. This
is one of the few occasions where we break our rule “Only Mock Types That
You Own” (page 69) because the table model design ﬁts our design approach
so well.
2
We add a ﬁrst test to make sure we’re rendering the right number of columns.
Later, we’ll do something about the column titles.
3
This expectation checks that we notify any attached JTable that the contents
have changed.
4
This is the event that triggers the behavior we want to test.
5
We assert that the table model returns the right values in the right columns.
We hard-code the row number because we’re still assuming that there is
only one.
6
There’s no speciﬁc equals() method on TableModelEvent, so we use a
matcher that will reﬂectively compare the property values of any event it re-
ceives against an expected example. Again, we hard-code the row number.
After the usual red/green cycle, we end up with an implementation that looks
like this:
157
Displaying Price Details


---
**Page 158**

public class SnipersTableModel extends AbstractTableModel {
  private final static SniperState STARTING_UP = new SniperState("", 0, 0);
  private String statusText = MainWindow.STATUS_JOINING;
  private SniperState sniperState = STARTING_UP; 1
[…]
  public int getColumnCount() { 2
    return Column.values().length; 
  }
  public int getRowCount() {
    return 1;
  }
  public Object getValueAt(int rowIndex, int columnIndex) { 3
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
  public void sniperStatusChanged(SniperState newSniperState, 4
                                  String newStatusText) 
  { 
    sniperState = newSniperState;
    statusText = newStatusText;
    fireTableRowsUpdated(0, 0);
  }
}
1
We provide an initial SniperState with “empty” values so that the table
model will work before the Sniper has connected.
2
For the dimensions, we just return the numbers of values in Column or a
hard-coded row count.
3
This method unpacks the value to return depending on the column that is
speciﬁed. The advantage of using an enum is that the compiler will help with
missing branches in the switch statement (although it still insists on a default
case). We’re not keen on using switch, as it’s not object-oriented, so we’ll
keep an eye on this too.
4
The Sniper-speciﬁc method. It sets the ﬁelds and then triggers its clients to
update.
If we run our acceptance test again, we ﬁnd we’ve made some progress. It’s
gone past the Bidding check and now fails because the last price column, “B”,
has not yet been updated. Interestingly, the status column shows Winning correctly,
because that code is still working.
Chapter 15
Towards a Real User Interface
158


---
**Page 159**

[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
 it is not with row with cells 
   <label with text "item-54321">, <label with text "1098">, 
   <label with text "1098">, <label with text "Winning">
because 
      in row 0: component 1 text was "1000"
and the proof is in Figure 15.3.
Figure 15.3
Sniper showing a row of detail
Simplifying Sniper Events
Listening to the Mood Music
We have one kind of Sniper event, Bidding, that we can handle all the way
through our application. Now we have to do the same thing to Winning, Lost,
and Won.
Frankly, that’s just dull. There’s too much repetitive work needed to make the
other cases work—setting them up in the Sniper and passing them through
the layers. Something’s wrong with the design. We toss this one around for a
while and eventually notice that we would have a subtle duplication in our code
if we just carried on. We would be splitting the transmission of the Sniper state
into two mechanisms: the choice of listener method and the state object. That’s
one mechanism too many.
We realize that we could collapse our events into one notiﬁcation that includes
the prices and the Sniper status. Of course we’re transmitting the same information
whichever mechanism we choose—but, looking at the chain of methods calls,
it would be simpler to have just one method and pass everything through in
SniperState.
Having made this choice, can we do it cleanly without ripping up the
metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
We want to start by creating a type to represent the Sniper’s status (winning,
losing, etc.) in the auction, but the terms “status” and “state” are too close to
distinguish easily. We kick around some vocabulary and eventually decide that
a better term for what we now call SniperState would be SniperSnapshot: a
description of the Sniper’s relationship with the auction at this moment in time.
This frees up the name SniperState to describe whether the Sniper is winning,
losing, and so on, which matches the terminology of the state machine we drew
159
Simplifying Sniper Events


