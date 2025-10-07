Line 1: 
Line 2: --- 페이지 174 ---
Line 3: Chapter 15
Line 4: Towards a Real User Interface
Line 5: In which we grow the user interface from a label to a table. We achieve
Line 6: this by adding a feature at a time, instead of taking the risk of replacing
Line 7: the whole thing in one go. We discover that some of the choices we
Line 8: made are no longer valid, so we dare to change existing code. We
Line 9: continue to refactor and sense that a more interesting structure is
Line 10: starting to appear.
Line 11: A More Realistic Implementation
Line 12: What Do We Have to Do Next?
Line 13: So far, we’ve been making do with a simple label in the user interface. That’s
Line 14: been effective for helping us clarify the structure of the application and prove
Line 15: that our ideas work, but the next tasks coming up will need more, and the client
Line 16: wants to see something that looks closer to Figure 9.1. We will need to show
Line 17: more price details from the auction and handle multiple items.
Line 18: The simplest option would be just to add more text into the label, but we think
Line 19: this is the right time to introduce more structure into the user interface. We de-
Line 20: ferred putting effort into this part of the application, and we think we should
Line 21: catch up now to be ready for the more complex requirements we’re about to
Line 22: implement. We decide to make the obvious choice, given our use of Swing, and
Line 23: replace the label with a table component. This decision gives us a clear direction
Line 24: for where our design should go next.
Line 25: The Swing pattern for using a JTable is to associate it with a TableModel. The
Line 26: table component queries the model for values to present, and the model notiﬁes
Line 27: the table when those values change. In our application, the relationships will
Line 28: look like Figure 15.1.  We call the new class SnipersTableModel because we want
Line 29: it to support multiple Snipers. It will accept updates from the Snipers and provide
Line 30: a representation of those values to its JTable.
Line 31: The question is how to get there from here.
Line 32: 149
Line 33: 
Line 34: --- 페이지 175 ---
Line 35: Figure 15.1
Line 36: Swing table model for the AuctionSniper
Line 37: Replacing JLabel
Line 38: We want to get the pieces into place with a minimum of change, without tearing
Line 39: the whole application apart. The smallest step we can think of is to replace the
Line 40: existing implementation (a JLabel) with a single-cell JTable, from which we can
Line 41: then grow the additional functionality. We start, of course, with the test, changing
Line 42: our harness to look for a cell in a table, rather than a label.
Line 43: public class AuctionSniperDriver extends JFrameDriver { […]
Line 44:   public void showsSniperStatus(String statusText) {
Line 45: new JTableDriver(this).hasCell(withLabelText(equalTo(statusText)));
Line 46:   }
Line 47: }
Line 48: This generates a failure message because we don’t yet have a table.
Line 49: […] but...
Line 50:     all top level windows
Line 51:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 52: contained 0 JTable ()
Line 53: Chapter 15
Line 54: Towards a Real User Interface
Line 55: 150
Line 56: 
Line 57: --- 페이지 176 ---
Line 58: We ﬁx this test by retroﬁtting a minimal JTable implementation. From now
Line 59: on, we want to speed up our narrative, so we’ll just show the end result. If we
Line 60: were feeling cautious we would ﬁrst add an empty table, to ﬁx the immediate
Line 61: failure, and then add its contents. It turns out that we don’t have to change any
Line 62: existing classes outside MainWindow because it encapsulates the act of updating
Line 63: the status. Here’s the new code:
Line 64: public class MainWindow extends JFrame { […]
Line 65: private final SnipersTableModel snipers = new SnipersTableModel();
Line 66:   public MainWindow() {
Line 67:     super(APPLICATION_TITLE);
Line 68:     setName(MainWindow.MAIN_WINDOW_NAME);
Line 69: fillContentPane(makeSnipersTable());
Line 70:     pack();
Line 71:     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line 72:     setVisible(true);
Line 73:   }
Line 74:   private void fillContentPane(JTable snipersTable) {
Line 75:     final Container contentPane = getContentPane();
Line 76:     contentPane.setLayout(new BorderLayout());
Line 77:     contentPane.add(new JScrollPane(snipersTable), BorderLayout.CENTER);
Line 78:   }
Line 79:   private JTable makeSnipersTable() {
Line 80:     final JTable snipersTable = new JTable(snipers);
Line 81:     snipersTable.setName(SNIPERS_TABLE_NAME);
Line 82:     return snipersTable;
Line 83:   }
Line 84:   public void showStatusText(String statusText) {
Line 85: snipers.setStatusText(statusText);
Line 86:   }
Line 87: }
Line 88: public class SnipersTableModel extends AbstractTableModel {
Line 89:   private String statusText = STATUS_JOINING;
Line 90:   public int getColumnCount() { return 1; }
Line 91:   public int getRowCount() { return 1; }
Line 92:   public Object getValueAt(int rowIndex, int columnIndex) { return statusText; }
Line 93:   public void setStatusText(String newStatusText) {
Line 94:     statusText = newStatusText;
Line 95:     fireTableRowsUpdated(0, 0);
Line 96:   }
Line 97: }
Line 98: 151
Line 99: A More Realistic Implementation
Line 100: 
Line 101: --- 페이지 177 ---
Line 102: Still Ugly
Line 103: As you can see, the SnipersTableModel really is a minimal implementation; the
Line 104: only value that can vary is the statusText. It inherits most of its behavior from
Line 105: the Swing AbstractTableModel, including the infrastructure for notifying the
Line 106: JTable of data changes. The result is as ugly as our previous version, except that
Line 107: now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
Line 108: on the presentation in a moment.
Line 109: Figure 15.2
Line 110: Sniper with a single-cell table
Line 111: Displaying Price Details
Line 112: First, a Failing Test
Line 113: Our next task is to display information about the Sniper’s position in the auction:
Line 114: item identiﬁer, last auction price, last bid, status. These values come from updates
Line 115: from the auction and the state held within the application. We need to pass them
Line 116: through from their source to the table model and then render them in the display.
Line 117: Of course, we start with the test. Given that this feature should be part of the
Line 118: basic functionality of the application, not separate from what we already have,
Line 119: we update our existing acceptance tests—starting with just one test so we don’t
Line 120: break everything at once. Here’s the new version:
Line 121: public class AuctionSniperEndToEndTest {
Line 122:   @Test public void
Line 123: sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line 124:     auction.startSellingItem();
Line 125:     application.startBiddingIn(auction);
Line 126:     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 127:     auction.reportPrice(1000, 98, "other bidder");
Line 128:     application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
Line 129:     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line 130:     auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line 131:     application.hasShownSniperIsWinning(1098); // winning bid
Line 132:     auction.announceClosed();
Line 133:     application.showsSniperHasWonAuction(1098); // last price
Line 134:   }
Line 135: }
Line 136: Chapter 15
Line 137: Towards a Real User Interface
Line 138: 152
Line 139: 
Line 140: --- 페이지 178 ---
Line 141: public class ApplicationRunner {
Line 142: private String itemId;
Line 143:   public void startBiddingIn(final FakeAuctionServer auction) {
Line 144: itemId = auction.getItemId();
Line 145: […]
Line 146:   }
Line 147: […]
Line 148:   public void hasShownSniperIsBidding(int lastPrice, int lastBid) {
Line 149:     driver.showsSniperStatus(itemId, lastPrice, lastBid, 
Line 150:                              MainWindow.STATUS_BIDDING);
Line 151:   }
Line 152:   public void hasShownSniperIsWinning(int winningBid) {
Line 153:     driver.showsSniperStatus(itemId, winningBid, winningBid, 
Line 154:                              MainWindow.STATUS_WINNING);
Line 155:   }
Line 156:   public void showsSniperHasWonAuction(int lastPrice) {
Line 157:     driver.showsSniperStatus(itemId, lastPrice, lastPrice, 
Line 158:                              MainWindow.STATUS_WON);
Line 159:   }
Line 160: }
Line 161: public class AuctionSniperDriver extends JFrameDriver {
Line 162: […]
Line 163:   public void showsSniperStatus(String itemId, int lastPrice, int lastBid, 
Line 164:                                 String statusText)
Line 165:   {
Line 166:     JTableDriver table = new JTableDriver(this);
Line 167:     table.hasRow(
Line 168:       matching(withLabelText(itemId), withLabelText(valueOf(lastPrice)), 
Line 169:                withLabelText(valueOf(lastBid)), withLabelText(statusText)));
Line 170:   }
Line 171: }
Line 172: We need the item identiﬁer so the test can look for it in the row, so we make
Line 173: the ApplicationRunner hold on it when connecting to an auction. We extend the
Line 174: AuctionSniperDriver to look for a table row that shows the item identiﬁer, last
Line 175: price, last bid, and sniper status.
Line 176: The test fails because the row has no details, only the status text:
Line 177: […] but...
Line 178:     all top level windows
Line 179:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 180:     contained 1 JTable ()
Line 181:  it is not with row with cells 
Line 182:    <label with text "item-54321">, <label with text "1000">, 
Line 183:    <label with text "1098">, <label with text "Bidding">
Line 184: because 
Line 185:       in row 0: component 0 text was "Bidding"
Line 186: 153
Line 187: Displaying Price Details
Line 188: 
Line 189: --- 페이지 179 ---
Line 190: Sending the State out of the Sniper
Line 191: With an acceptance test to show us where we want to get to, we can ﬁll in the
Line 192: steps along the way. As usual, we work “outside-in,” from the event that triggers
Line 193: the behavior; in this case it’s a price update from Southabee’s On-Line.
Line 194: Following along the sequence of method calls, we don’t have to change
Line 195: AuctionMessageTranslator, so we start by looking at AuctionSniper and its
Line 196: unit tests.
Line 197: AuctionSniper notiﬁes changes in its state to neighbors that implement the
Line 198: SniperListener interface which, as you might remember, has four callback
Line 199: methods, one for each state of the Sniper. Now we also need to pass in the current
Line 200: state of the Sniper when we notify a listener. We could add the same set of argu-
Line 201: ments to each method, but that would be duplication; so, we introduce a value
Line 202: type to carry the Sniper’s state. This is an example of “bundling up” that we
Line 203: described in “Value Types” (page 59). Here’s a ﬁrst cut:
Line 204: public class SniperState {
Line 205:   public final String itemId;
Line 206:   public final int lastPrice;
Line 207:   public final int lastBid;
Line 208:   public SniperState(String itemId, int lastPrice, int lastBid) {
Line 209:     this.itemId = itemId;
Line 210:     this.lastPrice = lastPrice;
Line 211:     this.lastBid = lastBid;
Line 212:   }
Line 213: }
Line 214: To save effort, we use the reﬂective builders from the Apache commons.lang
Line 215: library to implement equals(), hashCode(), and toString() in the new class. We
Line 216: could argue that we’re being premature with these features, but in practice we’ll
Line 217: need them in a moment when we write our unit tests.
Line 218: Public Final Fields
Line 219: We’ve adopted a habit of using public ﬁnal ﬁelds in value types, at least while we’re
Line 220: in the process of sorting out what the type should do. It makes it obvious that the
Line 221: value is immutable and reduces the overhead of maintaining getters when the class
Line 222: isn’t yet stable. Our ambition, which we might not achieve, is to replace all ﬁeld
Line 223: access with meaningful action methods on the type. We’ll see how that pans out.
Line 224: We don’t want to break all the tests at once, so we start with an easy one. In
Line 225: this test there’s no history, all we have to do in the Sniper is construct a
Line 226: SniperState from information available at the time and pass it to the listener.
Line 227: Chapter 15
Line 228: Towards a Real User Interface
Line 229: 154
Line 230: 
Line 231: --- 페이지 180 ---
Line 232: public class AuctionSniperTest { […]
Line 233:   @Test public void
Line 234: bidsHigherAndReportsBiddingWhenNewPriceArrives() {
Line 235:     final int price = 1001;
Line 236:     final int increment = 25;
Line 237:     final int bid = price + increment;
Line 238:     context.checking(new Expectations() {{
Line 239:       one(auction).bid(bid);
Line 240:       atLeast(1).of(sniperListener).sniperBidding(
Line 241: new SniperState(ITEM_ID, price, bid));
Line 242:     }});
Line 243:     sniper.currentPrice(price, increment, PriceSource.FromOtherBidder);
Line 244:   }
Line 245: }
Line 246: Then we make the test pass:
Line 247: public class AuctionSniper implements AuctionEventListener { […]
Line 248:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 249:     isWinning = priceSource == PriceSource.FromSniper;
Line 250:     if (isWinning) {
Line 251:       sniperListener.sniperWinning();
Line 252:     } else {
Line 253: int bid = price + increment;
Line 254:       auction.bid(bid);
Line 255:       sniperListener.sniperBidding(new SniperState(itemId, price, bid));
Line 256:     }
Line 257:   }
Line 258: }
Line 259: To get the code to compile, we also add the state argument to the
Line 260: sniperBidding() method in 
Line 261: SniperStateDisplayer, which implements
Line 262: SniperListener, but don’t yet do anything with it.
Line 263: The one signiﬁcant change is that the Sniper needs access to the item identiﬁer
Line 264: so it can construct a SniperState. Given that the Sniper doesn’t need this value
Line 265: for any other reason, we could have kept it in the SniperStateDisplayer and
Line 266: added it in when an event passes through, but we think it’s reasonable that the
Line 267: Sniper has access to this information. We decide to pass the identiﬁer into the
Line 268: AuctionSniper constructor; it’s available at the time, and we don’t want to get
Line 269: it from the Auction object which may have its own form of identiﬁer for an item.
Line 270: We have one other test that refers to the sniperBidding() method, but only
Line 271: as an “allowance.” We use a matcher that says that, since it’s only supporting
Line 272: the interesting part of the test, we don’t care about the contents of the state object.
Line 273: allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Line 274: Showing a Bidding Sniper
Line 275: We’ll take larger steps for the next task—presenting the state in the user
Line 276: interface—as there are some new moving parts, including a new unit test. The
Line 277: 155
Line 278: Displaying Price Details
Line 279: 
Line 280: --- 페이지 181 ---
Line 281: ﬁrst version of the code will be clumsier than we would like but, as you’ll soon
Line 282: see, there’ll be interesting opportunities for cleaning up.
Line 283: Our very ﬁrst step is to pass the new state parameter, which we’ve been ignor-
Line 284: ing, through MainWindow to a new method in SnipersTableModel. While we’re at
Line 285: it, we notice that just passing events through MainWindow isn’t adding much value,
Line 286: so we make a note to deal with that later.
Line 287: public class SniperStateDisplayer implements SniperListener { […]
Line 288:   public void sniperBidding(final SniperState state) {
Line 289:     SwingUtilities.invokeLater(new Runnable() {
Line 290:       public void run() { 
Line 291: ui.sniperStatusChanged(state, MainWindow.STATUS_BIDDING);
Line 292:       } 
Line 293:     });
Line 294:   }
Line 295: }
Line 296: public class MainWindow extends JFrame { […]
Line 297:   public void sniperStatusChanged(SniperState sniperState, String statusText) {
Line 298:     snipers.sniperStatusChanged(sniperState, statusText);
Line 299:   }
Line 300: }
Line 301: To get the new values visible on screen, we need to ﬁx SnipersTableModel so
Line 302: that it makes them available to its JTable, starting with a unit test. We take a
Line 303: small design leap by introducing a Java enum to represent the columns in the
Line 304: table—it’s more meaningful than just using integers.
Line 305: public enum Column {
Line 306:   ITEM_IDENTIFIER,
Line 307:   LAST_PRICE,
Line 308:   LAST_BID,
Line 309:   SNIPER_STATUS;
Line 310:   public static Column at(int offset) { return values()[offset]; }
Line 311: }
Line 312: The table model needs to do two things when its state changes: hold onto the
Line 313: new values and notify the table that they’ve changed. Here’s the test:
Line 314: @RunWith(JMock.class)
Line 315: public class SnipersTableModelTest {
Line 316:   private final Mockery context = new Mockery();
Line 317:   private TableModelListener listener = context.mock(TableModelListener.class);
Line 318:   private final SnipersTableModel model = new SnipersTableModel();
Line 319:   @Before public void attachModelListener() {  1
Line 320:     model.addTableModelListener(listener);
Line 321:   }
Line 322:   @Test public void
Line 323: hasEnoughColumns() {  2
Line 324:     assertThat(model.getColumnCount(), equalTo(Column.values().length));
Line 325:   }
Line 326: Chapter 15
Line 327: Towards a Real User Interface
Line 328: 156
Line 329: 
Line 330: --- 페이지 182 ---
Line 331:   @Test public void
Line 332: setsSniperValuesInColumns() {
Line 333:     context.checking(new Expectations() {{
Line 334:       one(listener).tableChanged(with(aRowChangedEvent()));  3
Line 335:     }});
Line 336:     model.sniperStatusChanged(new SniperState("item id", 555, 666),  4
Line 337:                               MainWindow.STATUS_BIDDING);
Line 338:     assertColumnEquals(Column.ITEM_IDENTIFIER, "item id"); 5
Line 339:     assertColumnEquals(Column.LAST_PRICE, 555);
Line 340:     assertColumnEquals(Column.LAST_BID, 666);
Line 341:     assertColumnEquals(Column.SNIPER_STATUS, MainWindow.STATUS_BIDDING);
Line 342:   }
Line 343:   private void assertColumnEquals(Column column, Object expected) {
Line 344:     final int rowIndex = 0;
Line 345:     final int columnIndex = column.ordinal();
Line 346:     assertEquals(expected, model.getValueAt(rowIndex, columnIndex);
Line 347:   }
Line 348:   private Matcher<TableModelEvent> aRowChangedEvent() { 6
Line 349:     return samePropertyValuesAs(new TableModelEvent(model, 0));
Line 350:   }
Line 351: }
Line 352: 1
Line 353: We attach a mock implementation of TableModelListener to the model. This
Line 354: is one of the few occasions where we break our rule “Only Mock Types That
Line 355: You Own” (page 69) because the table model design ﬁts our design approach
Line 356: so well.
Line 357: 2
Line 358: We add a ﬁrst test to make sure we’re rendering the right number of columns.
Line 359: Later, we’ll do something about the column titles.
Line 360: 3
Line 361: This expectation checks that we notify any attached JTable that the contents
Line 362: have changed.
Line 363: 4
Line 364: This is the event that triggers the behavior we want to test.
Line 365: 5
Line 366: We assert that the table model returns the right values in the right columns.
Line 367: We hard-code the row number because we’re still assuming that there is
Line 368: only one.
Line 369: 6
Line 370: There’s no speciﬁc equals() method on TableModelEvent, so we use a
Line 371: matcher that will reﬂectively compare the property values of any event it re-
Line 372: ceives against an expected example. Again, we hard-code the row number.
Line 373: After the usual red/green cycle, we end up with an implementation that looks
Line 374: like this:
Line 375: 157
Line 376: Displaying Price Details
Line 377: 
Line 378: --- 페이지 183 ---
Line 379: public class SnipersTableModel extends AbstractTableModel {
Line 380:   private final static SniperState STARTING_UP = new SniperState("", 0, 0);
Line 381:   private String statusText = MainWindow.STATUS_JOINING;
Line 382:   private SniperState sniperState = STARTING_UP; 1
Line 383: […]
Line 384:   public int getColumnCount() { 2
Line 385:     return Column.values().length; 
Line 386:   }
Line 387:   public int getRowCount() {
Line 388:     return 1;
Line 389:   }
Line 390:   public Object getValueAt(int rowIndex, int columnIndex) { 3
Line 391:     switch (Column.at(columnIndex)) {
Line 392:     case ITEM_IDENTIFIER:
Line 393:       return sniperState.itemId;
Line 394:     case LAST_PRICE:
Line 395:       return sniperState.lastPrice;
Line 396:     case LAST_BID:
Line 397:       return sniperState.lastBid;
Line 398:     case SNIPER_STATUS:
Line 399:       return statusText;
Line 400:     default:
Line 401:       throw new IllegalArgumentException("No column at " + columnIndex);
Line 402:     }
Line 403:   }
Line 404:   public void sniperStatusChanged(SniperState newSniperState, 4
Line 405:                                   String newStatusText) 
Line 406:   { 
Line 407:     sniperState = newSniperState;
Line 408:     statusText = newStatusText;
Line 409:     fireTableRowsUpdated(0, 0);
Line 410:   }
Line 411: }
Line 412: 1
Line 413: We provide an initial SniperState with “empty” values so that the table
Line 414: model will work before the Sniper has connected.
Line 415: 2
Line 416: For the dimensions, we just return the numbers of values in Column or a
Line 417: hard-coded row count.
Line 418: 3
Line 419: This method unpacks the value to return depending on the column that is
Line 420: speciﬁed. The advantage of using an enum is that the compiler will help with
Line 421: missing branches in the switch statement (although it still insists on a default
Line 422: case). We’re not keen on using switch, as it’s not object-oriented, so we’ll
Line 423: keep an eye on this too.
Line 424: 4
Line 425: The Sniper-speciﬁc method. It sets the ﬁelds and then triggers its clients to
Line 426: update.
Line 427: If we run our acceptance test again, we ﬁnd we’ve made some progress. It’s
Line 428: gone past the Bidding check and now fails because the last price column, “B”,
Line 429: has not yet been updated. Interestingly, the status column shows Winning correctly,
Line 430: because that code is still working.
Line 431: Chapter 15
Line 432: Towards a Real User Interface
Line 433: 158
Line 434: 
Line 435: --- 페이지 184 ---
Line 436: […] but...
Line 437:     all top level windows
Line 438:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 439:     contained 1 JTable ()
Line 440:  it is not with row with cells 
Line 441:    <label with text "item-54321">, <label with text "1098">, 
Line 442:    <label with text "1098">, <label with text "Winning">
Line 443: because 
Line 444:       in row 0: component 1 text was "1000"
Line 445: and the proof is in Figure 15.3.
Line 446: Figure 15.3
Line 447: Sniper showing a row of detail
Line 448: Simplifying Sniper Events
Line 449: Listening to the Mood Music
Line 450: We have one kind of Sniper event, Bidding, that we can handle all the way
Line 451: through our application. Now we have to do the same thing to Winning, Lost,
Line 452: and Won.
Line 453: Frankly, that’s just dull. There’s too much repetitive work needed to make the
Line 454: other cases work—setting them up in the Sniper and passing them through
Line 455: the layers. Something’s wrong with the design. We toss this one around for a
Line 456: while and eventually notice that we would have a subtle duplication in our code
Line 457: if we just carried on. We would be splitting the transmission of the Sniper state
Line 458: into two mechanisms: the choice of listener method and the state object. That’s
Line 459: one mechanism too many.
Line 460: We realize that we could collapse our events into one notiﬁcation that includes
Line 461: the prices and the Sniper status. Of course we’re transmitting the same information
Line 462: whichever mechanism we choose—but, looking at the chain of methods calls,
Line 463: it would be simpler to have just one method and pass everything through in
Line 464: SniperState.
Line 465: Having made this choice, can we do it cleanly without ripping up the
Line 466: metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
Line 467: We want to start by creating a type to represent the Sniper’s status (winning,
Line 468: losing, etc.) in the auction, but the terms “status” and “state” are too close to
Line 469: distinguish easily. We kick around some vocabulary and eventually decide that
Line 470: a better term for what we now call SniperState would be SniperSnapshot: a
Line 471: description of the Sniper’s relationship with the auction at this moment in time.
Line 472: This frees up the name SniperState to describe whether the Sniper is winning,
Line 473: losing, and so on, which matches the terminology of the state machine we drew
Line 474: 159
Line 475: Simplifying Sniper Events
Line 476: 
Line 477: --- 페이지 185 ---
Line 478: in Figure 9.3 on page 78. Renaming the SniperState takes a moment, and we
Line 479: change the value in Column from SNIPER_STATUS to SNIPER_STATE.
Line 480: 20/20 Hindsight
Line 481: We’ve just gone through not one but two of those forehead-slapping moments that
Line 482: make us wonder why we didn’t see it the ﬁrst time around. Surely, if we’d spent
Line 483: more time on the design, we wouldn’t have to change it now? Sometimes that’s
Line 484: true. Our experience, however, is that nothing shakes out a design like trying to
Line 485: implement it, and between us we know just a handful of people who are smart
Line 486: enough to get their designs always right. Our coping mechanism is to get into the
Line 487: critical areas of the code early and to allow ourselves to change our collective mind
Line 488: when we could do better. We rely on our skills, on taking small steps, and on the
Line 489: tests to protect us when we make changes.
Line 490: Repurposing sniperBidding()
Line 491: Our ﬁrst step is to take the method that does most of what we want,
Line 492: sniperBidding(), and rework it to ﬁt our new scheme. We create an enum that
Line 493: takes the SniperState name we’ve just freed up and add it to SniperSnapshot;
Line 494: we take the sniperState ﬁeld out of the method arguments; and, ﬁnally, we re-
Line 495: name the method to sniperStateChanged() to match its intended new role. We
Line 496: push the changes through to get the following code:
Line 497: public enum SniperState {
Line 498:   JOINING,
Line 499:   BIDDING,
Line 500:   WINNING,
Line 501:   LOST,
Line 502:   WON;
Line 503: }
Line 504: public class AuctionSniper implements AuctionEventListener { […]
Line 505:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 506:     isWinning = priceSource == PriceSource.FromSniper;
Line 507:     if (isWinning) {
Line 508:       sniperListener.sniperWinning();
Line 509:     } else {
Line 510:       final int bid = price + increment;
Line 511:       auction.bid(bid);
Line 512:       sniperListener.sniperStateChanged(
Line 513:         new SniperSnapshot(itemId, price, bid, SniperState.BIDDING));
Line 514:     }
Line 515:   }
Line 516: }
Line 517: Chapter 15
Line 518: Towards a Real User Interface
Line 519: 160
Line 520: 
Line 521: --- 페이지 186 ---
Line 522: In the table model, we use simple indexing to translate the enum into displayable
Line 523: text.
Line 524: public class SnipersTableModel extends AbstractTableModel { […]
Line 525: private static String[] STATUS_TEXT = { MainWindow.STATUS_JOINING, 
Line 526:                                           MainWindow.STATUS_BIDDING };
Line 527:   public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line 528:     this.snapshot = newSnapshot;
Line 529:     this.state = STATUS_TEXT[newSnapshot.state.ordinal()];
Line 530:     fireTableRowsUpdated(0, 0);
Line 531:   }
Line 532: }
Line 533: We make some minor changes to the test code, to get it through the compiler,
Line 534: plus one more interesting adjustment. You might remember that we wrote an
Line 535: expectation clause that ignored the details of the SniperState:
Line 536: allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Line 537: We can no longer rely on the choice of method to distinguish between different
Line 538: events, so we have to dig into the new SniperSnapshot object to make sure we’re
Line 539: matching the right one. We rewrite the expectation with a custom matcher that
Line 540: checks just the state:
Line 541: public class AuctionSniperTest {
Line 542: […]
Line 543:   context.checking(new Expectations() {{
Line 544:     ignoring(auction);
Line 545:     allowing(sniperListener).sniperStateChanged(
Line 546:                                with(aSniperThatIs(BIDDING))); 
Line 547:                                                 then(sniperState.is("bidding"));
Line 548:     atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
Line 549:   }});
Line 550: […]
Line 551:   private Matcher<SniperSnapshot> aSniperThatIs(final SniperState state) {
Line 552:     return new FeatureMatcher<SniperSnapshot, SniperState>(
Line 553:              equalTo(state), "sniper that is ", "was") 
Line 554:     {
Line 555:       @Override
Line 556:       protected SniperState featureValueOf(SniperSnapshot actual) {
Line 557:         return actual.state;
Line 558:       }
Line 559:     };
Line 560:   }
Line 561: }
Line 562: 161
Line 563: Simplifying Sniper Events
Line 564: 
Line 565: --- 페이지 187 ---
Line 566: Lightweight Extensions to jMock
Line 567: We added a small helper method aSniperThatIs() to package up our specializa-
Line 568: tion of FeatureMatcher behind a descriptive name. You’ll see that the method
Line 569: name is intended to make the expectation code read well (or as well as we can
Line 570: manage in Java).We did the same earlier in the chapter with aRowChangedEvent().
Line 571: As we discussed in “Different Levels of Language” on page 51, we’re effectively
Line 572: writing extensions to a language that’s embedded in Java. jMock was designed to
Line 573: be extensible in this way, so that programmers can plug in features described in
Line 574: terms of the code they’re testing.You could think of these little helper methods as
Line 575: creating new nouns in jMock’s expectation language.
Line 576: Filling In the Numbers
Line 577: Now we’re in a position to feed the missing price to the user interface, which
Line 578: means changing the listener call from sniperWinning() to sniperStateChanged()
Line 579: so that the listener will receive the value in a SniperSnapshot. We start by
Line 580: changing the test to expect the different listener call, and to trigger the event by
Line 581: calling currentPrice() twice: once to force the Sniper to bid, and again to tell
Line 582: the Sniper that it’s winning.
Line 583: public class AuctionSniperTest { […]
Line 584:   @Test public void
Line 585: reportsIsWinningWhenCurrentPriceComesFromSniper() {
Line 586:     context.checking(new Expectations() {{
Line 587:       ignoring(auction);
Line 588:       allowing(sniperListener).sniperStateChanged(
Line 589:                                  with(aSniperThatIs(BIDDING))); 
Line 590:                                                then(sniperState.is("bidding"));
Line 591: atLeast(1).of(sniperListener).sniperStateChanged(
Line 592:                                new SniperSnapshot(ITEM_ID, 135, 135, WINNING)); 
Line 593:                                                when(sniperState.is("bidding"));
Line 594:     }});
Line 595: sniper.currentPrice(123, 12, PriceSource.FromOtherBidder);
Line 596:     sniper.currentPrice(135, 45, PriceSource.FromSniper);
Line 597:   }
Line 598: }
Line 599: We change AuctionSniper to retain its most recent values by holding on to the
Line 600: last snapshot. We also add some helper methods to SniperSnapshot, and ﬁnd
Line 601: that our implementation starts to simplify.
Line 602: Chapter 15
Line 603: Towards a Real User Interface
Line 604: 162
Line 605: 
Line 606: --- 페이지 188 ---
Line 607: public class AuctionSniper implements AuctionEventListener { […]
Line 608: private SniperSnapshot snapshot;
Line 609:   public AuctionSniper(String itemId, Auction auction, SniperListener sniperListener)
Line 610:   {
Line 611:     this.auction = auction;
Line 612:     this.sniperListener = sniperListener;
Line 613: this.snapshot = SniperSnapshot.joining(itemId);
Line 614:   }
Line 615:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 616:     isWinning = priceSource == PriceSource.FromSniper;
Line 617:     if (isWinning) {
Line 618: snapshot = snapshot.winning(price);
Line 619:     } else {
Line 620:       final int bid = price + increment;
Line 621:       auction.bid(bid);
Line 622: snapshot = snapshot.bidding(price, bid);
Line 623:     }
Line 624: sniperListener.sniperStateChanged(snapshot);
Line 625:   }
Line 626: }
Line 627: public class SniperSnapshot { […]
Line 628:   public SniperSnapshot bidding(int newLastPrice, int newLastBid) {
Line 629:     return new SniperSnapshot(itemId, newLastPrice, newLastBid, SniperState.BIDDING);
Line 630:   }
Line 631:   public SniperSnapshot winning(int newLastPrice) {
Line 632:     return new SniperSnapshot(itemId, newLastPrice, lastBid, SniperState.WINNING);
Line 633:   }
Line 634:   public static SniperSnapshot joining(String itemId) {
Line 635:     return new SniperSnapshot(itemId, 0, 0, SniperState.JOINING);
Line 636:   }
Line 637: }
Line 638: Nearly a State Machine
Line 639: We’ve added some constructor methods to SniperSnapshot that provide a clean
Line 640: mechanism for moving between snapshot states. It’s not a full state machine, in
Line 641: that we don’t enforce only “legal” transitions, but it’s a hint, and it nicely packages
Line 642: up the getting and setting of ﬁelds.
Line 643: We remove sniperWinning() from SniperListener and its implementations,
Line 644: and add a value for winning to SnipersTableModel.STATUS_TEXT.
Line 645: Now, the end-to-end test passes.
Line 646: 163
Line 647: Simplifying Sniper Events
Line 648: 
Line 649: --- 페이지 189 ---
Line 650: Follow Through
Line 651: Converting Won and Lost
Line 652: This works, but we still have two notiﬁcation methods in SniperListener left to
Line 653: convert before we can say we’re done: sniperWon() and sniperLost(). Again,
Line 654: we replace these with sniperStateChanged() and add two new values to
Line 655: SniperState.
Line 656: Plugging these changes in, we ﬁnd that the code simpliﬁes further. We drop
Line 657: the isWinning ﬁeld from the Sniper and move some decision-making into
Line 658: SniperSnapshot, which will know whether the Sniper is winning or losing,
Line 659: and SniperState.
Line 660: public class AuctionSniper implements AuctionEventListener { […]
Line 661:   public void auctionClosed() {
Line 662: snapshot = snapshot.closed();
Line 663:     notifyChange();
Line 664:   }
Line 665:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 666: switch(priceSource) {
Line 667:     case FromSniper:
Line 668:       snapshot = snapshot.winning(price); 
Line 669:       break;
Line 670: case FromOtherBidder:
Line 671:       int bid = price + increment;
Line 672:       auction.bid(bid);
Line 673:       snapshot = snapshot.bidding(price, bid); 
Line 674:       break;
Line 675:     }
Line 676: notifyChange();
Line 677:   }
Line 678:   private void notifyChange() {
Line 679:     sniperListener.sniperStateChanged(snapshot);
Line 680:   }
Line 681: }
Line 682: We note, with smug satisfaction, that AuctionSniper no longer refers to
Line 683: SniperState; it’s hidden in SniperSnapshot.
Line 684: public class SniperSnapshot { […]
Line 685:   public SniperSnapshot closed() {
Line 686:     return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
Line 687:   }
Line 688: }
Line 689: Chapter 15
Line 690: Towards a Real User Interface
Line 691: 164
Line 692: 
Line 693: --- 페이지 190 ---
Line 694: public enum SniperState {
Line 695:   JOINING {
Line 696:     @Override public SniperState whenAuctionClosed() { return LOST; }
Line 697:   },
Line 698:   BIDDING {
Line 699:     @Override public SniperState whenAuctionClosed() { return LOST; }
Line 700:   },
Line 701:   WINNING {
Line 702:     @Override public SniperState whenAuctionClosed() { return WON; }
Line 703:   },
Line 704:   LOST,
Line 705:   WON;
Line 706:   public SniperState whenAuctionClosed() {
Line 707:     throw new Defect("Auction is already closed");
Line 708:   }
Line 709: }
Line 710: We would have preferred to use a ﬁeld to implement whenAuctionClosed(). It
Line 711: turns out that the compiler cannot handle an enum referring to one of its values
Line 712: which has not yet been deﬁned, so we have to put up with the syntax noise of
Line 713: overridden methods.
Line 714: Not Too Small to Test
Line 715: At ﬁrst SniperState looked too simple to unit-test—after all, it’s exercised through
Line 716: the AuctionSniper tests—but we thought we should keep ourselves honest.
Line 717: Writing the test showed that our simple implementation didn’t handle re-closing an
Line 718: auction, which shouldn’t happen, so we added an exception. It would be better to
Line 719: write the code so that this case is impossible, but we can’t see how to do that
Line 720: right now.
Line 721: A Defect Exception
Line 722: In most systems we build, we end up writing a runtime exception called something
Line 723: like Defect (or perhaps StupidProgrammerMistakeException). We throw this
Line 724: when the code reaches a condition that could only be caused by a programming
Line 725: error, rather than a failure in the runtime environment.
Line 726: 165
Line 727: Follow Through
Line 728: 
Line 729: --- 페이지 191 ---
Line 730: Trimming the Table Model
Line 731: We remove the accessor setStatusText() that sets the state display string in
Line 732: SnipersTableModel, as everything uses sniperStatusChanged() now. While we’re
Line 733: at it, we move the description string constants for the Sniper state over from
Line 734: MainWindow.
Line 735: public class SnipersTableModel extends AbstractTableModel { […]
Line 736: private final static String[] STATUS_TEXT = { 
Line 737:     "Joining", "Bidding", "Winning", "Lost", "Won" 
Line 738:   };
Line 739:   public Object getValueAt(int rowIndex, int columnIndex) {
Line 740:     switch (Column.at(columnIndex)) {
Line 741:     case ITEM_IDENTIFIER:
Line 742:       return snapshot.itemId;
Line 743:     case LAST_PRICE:
Line 744:       return snapshot.lastPrice;
Line 745:     case LAST_BID:
Line 746:       return snapshot.lastBid;
Line 747:     case SNIPER_STATE:
Line 748:       return textFor(snapshot.state);
Line 749:     default:
Line 750:       throw new IllegalArgumentException("No column at" + columnIndex);
Line 751:     }
Line 752:   }
Line 753:   public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line 754: this.snapshot = newSnapshot;
Line 755:     fireTableRowsUpdated(0, 0);
Line 756:   }
Line 757:   public static String textFor(SniperState state) {
Line 758:     return STATUS_TEXT[state.ordinal()];
Line 759:   }
Line 760: }
Line 761: The helper method, textFor(), helps with readability, and we also use it to get
Line 762: hold of the display strings in tests since the constants are no longer accessible
Line 763: from MainWindow.
Line 764: Object-Oriented Column
Line 765: We still have a couple of things to do before we ﬁnish this task. We start by
Line 766: removing all the old test code that didn’t specify the price details, ﬁlling in the
Line 767: expected values in the tests as required. The tests still run.
Line 768: The next change is to replace the switch statement which is noisy, not very
Line 769: object-oriented, and includes an unnecessary default: clause just to satisfy the
Line 770: compiler. It’s served its purpose, which was to get us through the previous coding
Line 771: stage. We add a method to Column that will extract the appropriate ﬁeld:
Line 772: Chapter 15
Line 773: Towards a Real User Interface
Line 774: 166
Line 775: 
Line 776: --- 페이지 192 ---
Line 777: public enum Column {
Line 778:   ITEM_IDENTIFIER {
Line 779:     @Override public Object valueIn(SniperSnapshot snapshot) {
Line 780:       return snapshot.itemId;
Line 781:     }
Line 782:   },
Line 783:   LAST_PRICE {
Line 784:     @Override public Object valueIn(SniperSnapshot snapshot) {
Line 785:       return snapshot.lastPrice;
Line 786:     }
Line 787:   },
Line 788:   LAST_BID{
Line 789:     @Override public Object valueIn(SniperSnapshot snapshot) {
Line 790:       return snapshot.lastBid;
Line 791:     }    
Line 792:   },
Line 793:   SNIPER_STATE {
Line 794:     @Override public Object valueIn(SniperSnapshot snapshot) {
Line 795:       return SnipersTableModel.textFor(snapshot.state);
Line 796:     }    
Line 797:   };
Line 798: abstract public Object valueIn(SniperSnapshot snapshot);
Line 799: […]
Line 800: }
Line 801: and the code in SnipersTableModel becomes negligible:
Line 802: public class SnipersTableModel extends AbstractTableModel { […]
Line 803:   public Object getValueAt(int rowIndex, int columnIndex) {
Line 804:     return Column.at(columnIndex).valueIn(snapshot);
Line 805:   }
Line 806: }
Line 807: Of course, we write a unit test for Column. It may seem unnecessary now, but
Line 808: it will protect us when we make changes and forget to keep the column mapping
Line 809: up to date.
Line 810: Shortening the Event Path
Line 811: Finally, we see that we have some forwarding calls that we no longer need.
Line 812: MainWindow just forwards the update and SniperStateDisplayer has collapsed
Line 813: to almost nothing.
Line 814: public class MainWindow extends JFrame { […]
Line 815:   public void sniperStateChanged(SniperSnapshot snapshot) {
Line 816:     snipers.sniperStateChanged(snapshot);
Line 817:   }
Line 818: }
Line 819: 167
Line 820: Follow Through
Line 821: 
Line 822: --- 페이지 193 ---
Line 823: public class SniperStateDisplayer implements SniperListener { […]
Line 824:   public void sniperStateChanged(final SniperSnapshot snapshot) {
Line 825:     SwingUtilities.invokeLater(new Runnable() {
Line 826:       public void run() { mainWindow.sniperStateChanged(snapshot); } 
Line 827:     });
Line 828:   }
Line 829: }
Line 830: SniperStateDisplayer still serves a useful purpose, which is to push updates
Line 831: onto the Swing event thread, but it no longer does any translation between do-
Line 832: mains in the code, and the call to MainWindow is unnecessary. We decide to sim-
Line 833: plify the connections by making SnipersTableModel implement SniperListener.
Line 834: We change SniperStateDisplayer to be a Decorator and rename it to
Line 835: SwingThreadSniperListener, and we rewire Main so that the Sniper connects
Line 836: to the table model rather than the window.
Line 837:  public class Main { […]
Line 838: private final SnipersTableModel snipers = new SnipersTableModel();
Line 839:   private MainWindow ui;
Line 840:   public Main() throws Exception {
Line 841:     SwingUtilities.invokeAndWait(new Runnable() { 
Line 842:       public void run() { ui = new MainWindow(snipers); }
Line 843:     });
Line 844:   }
Line 845:   private void joinAuction(XMPPConnection connection, String itemId) {
Line 846: […]
Line 847:     Auction auction = new XMPPAuction(chat);
Line 848:     chat.addMessageListener(
Line 849:         new AuctionMessageTranslator(
Line 850:             connection.getUser(),
Line 851:             new AuctionSniper(itemId, auction, 
Line 852: new SwingThreadSniperListener(snipers))));
Line 853:     auction.join();
Line 854:   }
Line 855: }
Line 856: The new structure looks like Figure 15.4.
Line 857: Final Polish
Line 858: A Test for Column Titles
Line 859: To make the user interface presentable, we need to ﬁll in the column titles which,
Line 860: as we saw in Figure 15.3, are still missing. This isn’t difﬁcult, since most of the
Line 861: implementation is built into Swing’s TableModel. As always, we start with
Line 862: the acceptance test. We add extra validation to AuctionSniperDriver that will
Line 863: be called by the method in ApplicationRunner that starts up the Sniper. For good
Line 864: measure, we throw in a check for the application’s displayed title.
Line 865: Chapter 15
Line 866: Towards a Real User Interface
Line 867: 168
Line 868: 
Line 869: --- 페이지 194 ---
Line 870: Figure 15.4
Line 871: TableModel as a SniperListener
Line 872: public class ApplicationRunner { […]
Line 873:   public void startBiddingIn(final FakeAuctionServer auction) {
Line 874:     itemId = auction.getItemId();
Line 875:     Thread thread = new Thread("Test Application") {
Line 876: […]
Line 877:     };
Line 878:     thread.setDaemon(true);
Line 879:     thread.start();
Line 880:     driver = new AuctionSniperDriver(1000);
Line 881: driver.hasTitle(MainWindow.APPLICATION_TITLE);
Line 882: driver.hasColumnTitles();
Line 883:     driver.showsSniperStatus(JOINING.itemId, JOINING.lastPrice, 
Line 884:                              JOINING.lastBid, textFor(SniperState.JOINING));
Line 885:   }
Line 886: }
Line 887: public class AuctionSniperDriver extends JFrameDriver { […]
Line 888:   public void hasColumnTitles() {
Line 889:     JTableHeaderDriver headers = new JTableHeaderDriver(this, JTableHeader.class);
Line 890:     headers.hasHeaders(matching(withLabelText("Item"), withLabelText("Last Price"),
Line 891:                                 withLabelText("Last Bid"), withLabelText("State")));
Line 892:   }
Line 893: }
Line 894: The test fails:
Line 895: 169
Line 896: Final Polish
Line 897: 
Line 898: --- 페이지 195 ---
Line 899: java.lang.AssertionError: 
Line 900: Tried to look for...
Line 901:     exactly 1 JTableHeader ()
Line 902:     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 903:     in all top level windows
Line 904: and check that it is with headers with cells 
Line 905:   <label  with text "Item">, <label with text "Last Price">, 
Line 906:     <label with text "Last Bid">, <label with text "State">
Line 907: but...
Line 908:     all top level windows
Line 909:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 910:     contained 1 JTableHeader ()
Line 911:    it is not with headers with cells 
Line 912:      <label with text "Item">, <label with text "Last Price">, 
Line 913:        <label with text "Last Bid">, <label with text "State">
Line 914: because component 0 text was "A"
Line 915: Implementing the TableModel
Line 916: Swing allows a JTable to query its TableModel for the column headers, which is
Line 917: the mechanism we’ve chosen to use. We already have Column to represent the
Line 918: columns, so we extend this enum by adding a ﬁeld for the header text which we
Line 919: reference in SnipersTableModel.
Line 920: public enum Column {
Line 921:   ITEM_IDENTIFIER("Item") { […]
Line 922:   LAST_PRICE("Last Price") { […]
Line 923:   LAST_BID("Last Bid") { […]
Line 924:   SNIPER_STATE("State") { […]
Line 925: public final String name;
Line 926:   private Column(String name) {
Line 927: this.name = name;
Line 928:   }
Line 929: }
Line 930: public class SnipersTableModel extends AbstractTableModel implements SniperListener
Line 931: { […]
Line 932:   @Override public String getColumnName(int column) {
Line 933:     return Column.at(column).name;
Line 934:   }
Line 935: }
Line 936: All we really need to check in the unit test for SniperTablesModel is the link
Line 937: between a Column value and a column name, but it’s so simple to iterate that we
Line 938: check them all:
Line 939: public class SnipersTableModelTest { […]
Line 940:   @Test public void
Line 941: setsUpColumnHeadings() {
Line 942:     for (Column column: Column.values()) {
Line 943:       assertEquals(column.name, model.getColumnName(column.ordinal()));
Line 944:     }
Line 945:   }
Line 946: }
Line 947: Chapter 15
Line 948: Towards a Real User Interface
Line 949: 170
Line 950: 
Line 951: --- 페이지 196 ---
Line 952: The acceptance test passes, and we can see the result in Figure 15.5.
Line 953: Figure 15.5
Line 954: Sniper with column headers
Line 955: Enough for Now
Line 956: There’s more we should do, such as set up borders and text alignment, to tune
Line 957: the user interface. We might do that by associating CellRenderers with each
Line 958: Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
Line 959: as an exercise for the reader, since they don’t add any more insight into our
Line 960: development process.
Line 961: In the meantime, we can cross off one more task from our to-do list:
Line 962: Figure 15.6.
Line 963: Figure 15.6
Line 964: The Sniper shows price information
Line 965: Observations
Line 966: Single Responsibilities
Line 967: SnipersTableModel has one responsibility: to represent the state of our bidding
Line 968: in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
Line 969: 171
Line 970: Observations
Line 971: 
Line 972: --- 페이지 197 ---
Line 973: But’s” (page 51). We’ve seen too much user interface code that is brittle because
Line 974: it has business logic mixed in. In this case, we could also have made the model
Line 975: responsible for deciding whether to bid (“because that would be simpler”), but
Line 976: that would make it harder to respond when either the user interface or the bidding
Line 977: policy change. It would be harder to even ﬁnd the bidding policy, which is why
Line 978: we isolated it in AuctionSniper.
Line 979: Keyhole Surgery for Software
Line 980: In this chapter we repeatedly used the practice of adding little slices of behavior
Line 981: all the way through the system: replace a label with a table, get that working;
Line 982: show the Sniper bidding, get that working; add the other values, get that
Line 983: working. In all of these cases, we’ve ﬁgured out where we want to get to (always
Line 984: allowing that we might discover a better alternative along the way), but we want
Line 985: to avoid ripping the application apart to get there. Once we start a major rework,
Line 986: we can’t stop until it’s ﬁnished, we can’t check in without branching, and merging
Line 987: with rest of the team is harder. There’s a reason that surgeons prefer keyhole
Line 988: surgery to opening up a patient—it’s less invasive and cheaper.
Line 989: Programmer Hyper-Sensitivity
Line 990: We have a well-developed sense of the value of our own time. We keep an eye
Line 991: out for activities that don’t seem to be making the best of our (doubtless signiﬁ-
Line 992: cant) talents, such as boiler-plate copying and adapting code: if we had the right
Line 993: abstraction, we wouldn’t have to bother. Sometimes this just has to be done, es-
Line 994: pecially when working with existing code—but there are fewer excuses when it’s
Line 995: our own. Deciding when to change the design requires a good sense for trade-
Line 996: offs, which implies both sensitivity and technical maturity: “I’m about to repeat
Line 997: this code with minor variations, that seems dull and wasteful” as against “This
Line 998: may not be the right time to rework this, I don’t understand it yet.”
Line 999: We don’t have a simple, reproducible technique here; it requires skill and ex-
Line 1000: perience. Developers should have a habit of reﬂecting on their activity, on the
Line 1001: best way to invest their time for the rest of a coding session. This might mean
Line 1002: carrying on exactly as before, but at least they’ll have thought about it.
Line 1003: Celebrate Changing Your Mind
Line 1004: When the facts change, I change my mind. What do you do, sir?
Line 1005: —John Maynard Keynes
Line 1006: During this chapter, we renamed several features in the code. In many develop-
Line 1007: ment cultures, this is viewed as a sign of weakness, as an inability to do a proper
Line 1008: job. Instead, we think this is an essential part of our development process. Just
Line 1009: Chapter 15
Line 1010: Towards a Real User Interface
Line 1011: 172
Line 1012: 
Line 1013: --- 페이지 198 ---
Line 1014: as we learn more about what the structure should be by using the code we’ve
Line 1015: written, we learn more about the names we’ve chosen when we work with them.
Line 1016: We see how the type and method names ﬁt together and whether the concepts
Line 1017: are clear, which stimulates the discovery of new ideas. If the name of a feature
Line 1018: isn’t right, the only smart thing to do is change it and avoid countless hours of
Line 1019: confusion for all who will read the code later.
Line 1020: This Isn’t the Only Solution
Line 1021: Examples in books, such as this one, tend to read as if there was an inevitability
Line 1022: about the solution. That’s partly because we put effort into making the narrative
Line 1023: ﬂow, but it’s also because presenting one solution tends to drive others out of
Line 1024: the reader’s consciousness. There are other variations we could have considered,
Line 1025: some of which might even resurface as the example develops.
Line 1026: For example, we could argue that AuctionSniper doesn’t need to know whether
Line 1027: it’s won or lost the auction—just whether it should bid or not. At present, the
Line 1028: only part of the application that cares about winning is the user interface, and
Line 1029: it would certainly simplify the AuctionSniper and SniperSnapshot if we moved
Line 1030: that decision away from them. We won’t do that now, because we don’t yet
Line 1031: know if it’s the right choice, but we ﬁnd that kicking around design options
Line 1032: sometimes leads to much better solutions.
Line 1033: 173
Line 1034: Observations
Line 1035: 
Line 1036: --- 페이지 199 ---
Line 1037: This page intentionally left blank 