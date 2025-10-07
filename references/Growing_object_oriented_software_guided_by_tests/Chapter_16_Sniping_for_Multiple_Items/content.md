Line 1: 
Line 2: --- 페이지 200 ---
Line 3: Chapter 16
Line 4: Sniping for Multiple Items
Line 5: In which we bid for multiple items, splitting the per-connection code
Line 6: from the per-auction code. We use the table model we just introduced
Line 7: to display the additional bids. We extend the user interface to allow
Line 8: users to add items dynamically. We’re pleased to ﬁnd that we don’t
Line 9: have to change the tests, just their implementation. We tease out a
Line 10: “user request listener” concept, which means we can test some features
Line 11: more directly. We leave the code in a bit of a mess.
Line 12: Testing for Multiple Items
Line 13: A Tale of Two Items
Line 14: The next task on our to-do list is to be able to snipe for multiple items at the
Line 15: same time. We already have much of the machinery we’ll need in place, since our
Line 16: user interface is based on a table, so some minor structural changes are all we
Line 17: need to make this work. Looking ahead in the list, we could combine this change
Line 18: with adding items through the user interface, but we don’t think we need to do
Line 19: that yet. Just focusing on this one task means we can clarify the distinction be-
Line 20: tween those features that belong to the Sniper’s connection to the auction house,
Line 21: and those that belong to an individual auction. So far we’ve speciﬁed the item
Line 22: on the command line, but we can extend that to pass multiple items in the
Line 23: argument list.
Line 24: As always, we start with a test. We want our new test to show that the appli-
Line 25: cation can bid for and win two different items, so we start by looking at the tests
Line 26: we already have. Our current test for a successful bid, in “First, a Failing Test”
Line 27: (page 152), assumes that the application has only one auction—it’s implicit in
Line 28: code such as:
Line 29: application.hasShownSniperIsBidding(1000, 1098);
Line 30: We prepare for multiple items by passing an auction into each of the
Line 31: ApplicationRunner calls, so the code now looks like:
Line 32: application.hasShownSniperIsBidding(auction, 1000, 1098);
Line 33: Within the ApplicationRunner, we remove the itemId ﬁeld and instead extract
Line 34: the item identiﬁer from the auction parameters.
Line 35: 175
Line 36: 
Line 37: --- 페이지 201 ---
Line 38: public void hasShownSniperIsBidding(FakeAuctionServer auction, 
Line 39:                                     int lastPrice, int lastBid) 
Line 40: {
Line 41:   driver.showsSniperStatus(auction.getItemId(), lastPrice, lastBid, 
Line 42:                            textFor(SniperState.BIDDING));
Line 43: }
Line 44: The rest is similar, which means we can write a new test:
Line 45: public class AuctionSniperEndToEndTest {
Line 46:   private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");  
Line 47: private final FakeAuctionServer auction2 = new FakeAuctionServer("item-65432");
Line 48:   @Test public void
Line 49: sniperBidsForMultipleItems() throws Exception {
Line 50:     auction.startSellingItem();
Line 51: auction2.startSellingItem();
Line 52:     application.startBiddingIn(auction, auction2);
Line 53:     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 54: auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 55:     auction.reportPrice(1000, 98, "other bidder");
Line 56:     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line 57: auction2.reportPrice(500, 21, "other bidder");
Line 58:     auction2.hasReceivedBid(521, ApplicationRunner.SNIPER_XMPP_ID);
Line 59:     auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);    
Line 60: auction2.reportPrice(521, 22, ApplicationRunner.SNIPER_XMPP_ID);
Line 61:     application.hasShownSniperIsWinning(auction, 1098);
Line 62: application.hasShownSniperIsWinning(auction2, 521);
Line 63:     auction.announceClosed();
Line 64: auction2.announceClosed();
Line 65:     application.showsSniperHasWonAuction(auction, 1098);
Line 66: application.showsSniperHasWonAuction(auction2, 521);
Line 67:   }
Line 68: }
Line 69: Following the protocol convention, we also remember to add a new user,
Line 70: auction-item-65432, to the chat server to represent the new auction.
Line 71: Avoiding False Positives
Line 72: We group the showsSniper methods together instead of pairing them with their
Line 73: associated auction triggers. This is to catch a problem that we found in an earlier
Line 74: version where each checking method would pick up the most recent change—the
Line 75: one we’d just triggered in the previous call. Grouping the checking methods together
Line 76: gives us conﬁdence that they’re both valid at the same time.
Line 77: Chapter 16
Line 78: Sniping for Multiple Items
Line 79: 176
Line 80: 
Line 81: --- 페이지 202 ---
Line 82: The ApplicationRunner
Line 83: The one signiﬁcant change we have to make in the ApplicationRunner is to the
Line 84: startBiddingIn() method. Now it needs to accept a variable number of auctions
Line 85: passed through to the Sniper’s command line. The conversion is a bit messy since
Line 86: we have to unpack the item identiﬁers and append them to the end of the other
Line 87: command-line arguments—this is the best we can do with Java arrays:
Line 88: public class ApplicationRunner { […]s
Line 89:   public void startBiddingIn(final FakeAuctionServer... auctions) {
Line 90:     Thread thread = new Thread("Test Application") {
Line 91:       @Override public void run() {
Line 92:         try {
Line 93:           Main.main(arguments(auctions));
Line 94:         } catch (Throwable e) {
Line 95: […]
Line 96: for (FakeAuctionServer auction : auctions) {
Line 97:       driver.showsSniperStatus(auction.getItemId(), 0, 0, textFor(JOINING));
Line 98: }
Line 99:   }
Line 100:   protected static String[] arguments(FakeAuctionServer... auctions) {
Line 101:     String[] arguments = new String[auctions.length + 3];
Line 102:     arguments[0] = XMPP_HOSTNAME;
Line 103:     arguments[1] = SNIPER_ID;
Line 104:     arguments[2] = SNIPER_PASSWORD;
Line 105:     for (int i = 0; i < auctions.length; i++) {
Line 106:       arguments[i + 3] = auctions[i].getItemId();
Line 107:     }
Line 108:     return arguments;
Line 109:   }
Line 110: }
Line 111: We run the test and watch it fail.
Line 112: java.lang.AssertionError: 
Line 113: Expected: is not null
Line 114:      got: null
Line 115:   at auctionsniper.SingleMessageListener.receivesAMessage()
Line 116: A Diversion, Fixing the Failure Message
Line 117: We ﬁrst saw this cryptic failure message in Chapter 11. It wasn’t so bad then
Line 118: because it could only occur in one place and there wasn’t much code to test
Line 119: anyway. Now it’s more annoying because we have to ﬁnd this method:
Line 120: public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line 121:   throws InterruptedException 
Line 122: {
Line 123:   final Message message = messages.poll(5, TimeUnit.SECONDS);
Line 124:   assertThat(message, is(notNullValue()));
Line 125:   assertThat(message.getBody(), messageMatcher);
Line 126: }
Line 127: 177
Line 128: Testing for Multiple Items
Line 129: 
Line 130: --- 페이지 203 ---
Line 131: and ﬁgure out what we’re missing. We’d like to combine these two assertions and
Line 132: provide a more meaningful failure. We could write a custom matcher for the
Line 133: message body but, given that the structure of Message is not going to change
Line 134: soon, we can use a PropertyMatcher, like this:
Line 135: public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line 136:   throws InterruptedException 
Line 137: {
Line 138:   final Message message = messages.poll(5, TimeUnit.SECONDS);
Line 139:   assertThat(message, hasProperty("body", messageMatcher));
Line 140: }
Line 141: which produces this more helpful failure report:
Line 142: java.lang.AssertionError: 
Line 143: Expected: hasProperty("body", "SOLVersion: 1.1; Command: JOIN;")
Line 144:      got: null
Line 145: With slightly more effort, we could have extended a FeatureMatcher to extract
Line 146: the message body with a nicer failure report. There’s not much difference, expect
Line 147: that it would be statically type-checked. Now back to business.
Line 148: Restructuring Main
Line 149: The test is failing because the Sniper is not sending a Join message for the second
Line 150: auction. We must change Main to interpret the additional arguments. Just to
Line 151: remind you, the current structure of the code is:
Line 152: public class Main {
Line 153:   public Main() throws Exception {
Line 154:     SwingUtilities.invokeAndWait(new Runnable() {
Line 155:       public void run() {
Line 156:         ui = new MainWindow(snipers);
Line 157:       }
Line 158:     });
Line 159:   }
Line 160:   public static void main(String... args) throws Exception {
Line 161:     Main main = new Main();
Line 162:     main.joinAuction(
Line 163:       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
Line 164:       args[ARG_ITEM_ID]);
Line 165:   }
Line 166:   private void joinAuction(XMPPConnection connection, String itemId) {
Line 167:     disconnectWhenUICloses(connection);
Line 168:     Chat chat = connection.getChatManager()
Line 169:                             .createChat(auctionId(itemId, connection), null);
Line 170: […]
Line 171:   }    
Line 172: }
Line 173: Chapter 16
Line 174: Sniping for Multiple Items
Line 175: 178
Line 176: 
Line 177: --- 페이지 204 ---
Line 178: To add multiple items, we need to distinguish between the code that establishes
Line 179: a connection to the auction server and the code that joins an auction. We start
Line 180: by holding on to connection so we can reuse it with multiple chats; the result is
Line 181: not very object-oriented but we want to wait and see how the structure develops.
Line 182: We also change notToBeGCd from a single value to a collection.
Line 183: public class Main {
Line 184:   public static void main(String... args) throws Exception {
Line 185:     Main main = new Main();
Line 186: XMPPConnection connection = 
Line 187:        connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line 188: main.disconnectWhenUICloses(connection);
Line 189:     main.joinAuction(connection, args[ARG_ITEM_ID]);
Line 190:   }
Line 191:   private void joinAuction(XMPPConnection connection, String itemId) {
Line 192:     Chat chat = connection.getChatManager()
Line 193:                             .createChat(auctionId(itemId, connection), null);
Line 194: notToBeGCd.add(chat);
Line 195:     Auction auction = new XMPPAuction(chat);
Line 196:     chat.addMessageListener(
Line 197:         new AuctionMessageTranslator(
Line 198:             connection.getUser(),
Line 199:             new AuctionSniper(itemId, auction, 
Line 200:                               new SwingThreadSniperListener(snipers))));
Line 201:     auction.join();
Line 202:   }
Line 203: }
Line 204: We loop through each of the items that we’ve been given:
Line 205: public static void main(String... args) throws Exception {
Line 206:   Main main = new Main();
Line 207:   XMPPConnection connection = 
Line 208:     connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line 209:   main.disconnectWhenUICloses(connection);
Line 210: for (int i = 3; i < args.length; i++) {
Line 211:     main.joinAuction(connection, args[i]);
Line 212:   }
Line 213: }
Line 214: This is ugly, but it does show us a separation between the code for the single
Line 215: connection and multiple auctions. We have a hunch it’ll be cleaned up before long.
Line 216: The end-to-end test now shows us that display cannot handle the additional
Line 217: item we’ve just fed in. The table model is still hard-coded to support one row,
Line 218: so one of the items will be ignored:
Line 219: […] but...
Line 220:   it is not table with row with cells 
Line 221:     <label with text "item-65432">, <label with text "521">, 
Line 222:     <label with text "521">, <label with text "Winning">
Line 223:   because 
Line 224: in row 0: component 0 text was "item-54321"
Line 225: 179
Line 226: Testing for Multiple Items
Line 227: 
Line 228: --- 페이지 205 ---
Line 229: Incidentally, this result is a nice example of why we needed to be aware of timing
Line 230: in end-to-end tests. This test might fail when looking for auction1 or auction2.
Line 231: The asynchrony of the system means that we can’t tell which will arrive ﬁrst.
Line 232: Extending the Table Model
Line 233: The SnipersTableModel needs to know about multiple items, so we add a new
Line 234: method to tell it when the Sniper joins an auction. We’ll call this method
Line 235: from Main.joinAuction() so we show that context ﬁrst, writing an empty
Line 236: implementation in SnipersTableModel to satisfy the compiler:
Line 237: private void 
Line 238: joinAuction(XMPPConnection connection, String itemId) throws Exception {
Line 239: safelyAddItemToModel(itemId);
Line 240: […]
Line 241: }
Line 242: private void safelyAddItemToModel(final String itemId) throws Exception {
Line 243:   SwingUtilities.invokeAndWait(new Runnable() {
Line 244:     public void run() {
Line 245:       snipers.addSniper(SniperSnapshot.joining(itemId));
Line 246:     }
Line 247:   });
Line 248: }
Line 249: We have to wrap the call in an invokeAndWait() because it’s changing the state
Line 250: of the user interface from outside the Swing thread.
Line 251: The implementation of SnipersTableModel itself is single-threaded, so we can
Line 252: write direct unit tests for it—starting with this one for adding a Sniper:
Line 253: @Test public void
Line 254: notifiesListenersWhenAddingASniper() {
Line 255:     SniperSnapshot joining = SniperSnapshot.joining("item123");
Line 256:     context.checking(new Expectations() { {
Line 257:       one(listener).tableChanged(with(anInsertionAtRow(0)));
Line 258:     }});
Line 259:     assertEquals(0, model.getRowCount());
Line 260:     model.addSniper(joining);
Line 261:     assertEquals(1, model.getRowCount());
Line 262:     assertRowMatchesSnapshot(0, joining);
Line 263: }
Line 264: This is similar to the test for updating the Sniper state that we wrote in
Line 265: “Showing a Bidding Sniper” (page 155), except that we’re calling the new method
Line 266: and matching a different TableModelEvent. We also package up the comparison
Line 267: of the table row values into a helper method assertRowMatchesSnapshot().
Line 268: We make this test pass by replacing the single SniperSnapshot ﬁeld with a
Line 269: collection and triggering the extra table event. These changes break the existing
Line 270: Sniper update test, because there’s no longer a default Sniper, so we ﬁx it:
Line 271: Chapter 16
Line 272: Sniping for Multiple Items
Line 273: 180
Line 274: 
Line 275: --- 페이지 206 ---
Line 276: @Test public void 
Line 277: setsSniperValuesInColumns() { 
Line 278:   SniperSnapshot joining = SniperSnapshot.joining("item id");
Line 279:   SniperSnapshot bidding = joining.bidding(555, 666);
Line 280:   context.checking(new Expectations() {{ 
Line 281: allowing(listener).tableChanged(with(anyInsertionEvent()));
Line 282:     one(listener).tableChanged(with(aChangeInRow(0))); 
Line 283:   }}); 
Line 284: model.addSniper(joining);
Line 285:   model.sniperStateChanged(bidding);
Line 286:   assertRowMatchesSnapshot(0, bidding);
Line 287: }
Line 288: We have to add a Sniper to the model. This triggers an insertion event which
Line 289: isn’t relevant to this test—it’s just supporting infrastructure—so we add an
Line 290: allowing() clause to let the insertion through. The clause uses a more forgiving
Line 291: matcher that checks only the type of the event, not its scope. We also change
Line 292: the matcher for the update event (the one we do care about) to be precise about
Line 293: which row it’s checking.
Line 294: Then we write more unit tests to drive out the rest of the functionality. For
Line 295: these, we’re not interested in the TableModelEvents, so we ignore the listener
Line 296: altogether.
Line 297: @Test public void 
Line 298: holdsSnipersInAdditionOrder() {
Line 299:   context.checking(new Expectations() { {
Line 300:     ignoring(listener);
Line 301:   }});
Line 302:   model.addSniper(SniperSnapshot.joining("item 0"));
Line 303:   model.addSniper(SniperSnapshot.joining("item 1"));
Line 304:   assertEquals("item 0", cellValue(0, Column.ITEM_IDENTIFIER));
Line 305:   assertEquals("item 1", cellValue(1, Column.ITEM_IDENTIFIER));
Line 306: }
Line 307: updatesCorrectRowForSniper() { […]
Line 308: throwsDefectIfNoExistingSniperForAnUpdate() { […]
Line 309: The implementation is obvious. The only point of interest is that we add an
Line 310: isForSameItemAs() method to SniperSnapshot so that it can decide whether it’s
Line 311: referring to the same item, instead of having the table model extract and compare
Line 312: identiﬁers.1 It’s a clearer division of responsibilities, with the advantage that we
Line 313: can change its implementation without changing the table model. We also decide
Line 314: that not ﬁnding a relevant entry is a programming error.
Line 315: 1. This avoids the “feature envy” code smell [Fowler99].
Line 316: 181
Line 317: Testing for Multiple Items
Line 318: 
Line 319: --- 페이지 207 ---
Line 320: public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line 321:   int row = rowMatching(newSnapshot);
Line 322:   snapshots.set(row, newSnapshot);
Line 323:   fireTableRowsUpdated(row, row);
Line 324: }
Line 325: private int rowMatching(SniperSnapshot snapshot) {
Line 326:   for (int i = 0; i < snapshots.size(); i++) {
Line 327:     if (newSnapshot.isForSameItemAs(snapshots.get(i))) {
Line 328:       return i;
Line 329:     }
Line 330:   }
Line 331:   throw new Defect("Cannot find match for " + snapshot);
Line 332: }
Line 333: This makes the current end-to-end test pass—so we can cross off the task from
Line 334: our to-do list, Figure 16.1.
Line 335: Figure 16.1
Line 336: The Sniper handles multiple items
Line 337: The End of Off-by-One Errors?
Line 338: Interacting with the table model requires indexing into a logical grid of cells. We
Line 339: ﬁnd that this is a case where TDD is particularly helpful. Getting indexing right can
Line 340: be tricky, except in the simplest cases, and writing tests ﬁrst clariﬁes the boundary
Line 341: conditions and then checks that our implementation is correct. We’ve both lost too
Line 342: much time in the past searching for indexing bugs buried deep in the code.
Line 343: Chapter 16
Line 344: Sniping for Multiple Items
Line 345: 182
Line 346: 
Line 347: --- 페이지 208 ---
Line 348: Adding Items through the User Interface
Line 349: A Simpler Design
Line 350: The buyers and user interface designers are still working through their ideas, but
Line 351: they have managed to simplify their original design by moving the item entry
Line 352: into a top bar instead of a pop-up dialog. The current version of the design looks
Line 353: like Figure 16.2, so we need to add a text ﬁeld and a button to the display.
Line 354: Figure 16.2
Line 355: The Sniper with input ﬁelds in its bar
Line 356: Making Progress While We Can
Line 357: The design of user interfaces is outside the scope of this book. For a project of any
Line 358: size, a user experience professional will consider all sorts of macro- and micro-
Line 359: details to provide the user with a coherent experience, so one route that some
Line 360: teams take is to try to lock down the interface design before coding. Our experience,
Line 361: and that of others like Jeff Patton, is that we can make development progress whilst
Line 362: the design is being sorted out. We can build to the team’s current understanding
Line 363: of the features and keep our code (and attitude) ﬂexible to respond to design ideas
Line 364: as they ﬁrm up—and perhaps even feed our experience back into the process.
Line 365: Update the Test
Line 366: Looking back at AuctionSniperEndToEndTest, it already expresses everything we
Line 367: want the application to do: it describes how the Sniper connects to one or more
Line 368: auctions and bids. The change is that we want to describe a different implemen-
Line 369: tation of some of that behavior (establishing the connection through the user
Line 370: interface rather than the command line) which happens in the ApplicationRunner.
Line 371: We need a restructuring similar to the one we just made in Main, splitting the
Line 372: connection from the individual auctions. We pull out a startSniper() method
Line 373: that starts up and checks the Sniper, and then start bidding for each auction
Line 374: in turn.
Line 375: 183
Line 376: Adding Items through the User Interface
Line 377: 
Line 378: --- 페이지 209 ---
Line 379: public class ApplicationRunner {
Line 380:   public void startBiddingIn(final FakeAuctionServer... auctions) {
Line 381:     startSniper();
Line 382:     for (FakeAuctionServer auction : auctions) {
Line 383: final String itemId = auction.getItemId();
Line 384:       driver.startBiddingFor(itemId);
Line 385:       driver.showsSniperStatus(itemId, 0, 0, textFor(SniperState.JOINING));
Line 386:     }
Line 387:   }
Line 388:   private void startSniper() {
Line 389: // as before without the call to showsSniperStatus()
Line 390:   }
Line 391: […]
Line 392: }
Line 393: The other change to the test infrastructure is implementing the new method
Line 394: startBiddingFor() in AuctionSniperDriver. This ﬁnds and ﬁlls in the text ﬁeld
Line 395: for the item identiﬁer, then ﬁnds and clicks on the Join Auction button.
Line 396: public class AuctionSniperDriver extends JFrameDriver {
Line 397:   @SuppressWarnings("unchecked")
Line 398:   public void startBiddingFor(String itemId) {
Line 399:     itemIdField().replaceAllText(itemId); 
Line 400:     bidButton().click(); 
Line 401:   }
Line 402:   private JTextFieldDriver itemIdField() {
Line 403:     JTextFieldDriver newItemId = 
Line 404:       new JTextFieldDriver(this, JTextField.class, named(MainWindow.NEW_ITEM_ID_NAME));
Line 405:     newItemId.focusWithMouse();
Line 406:     return newItemId;
Line 407:   }
Line 408:   private JButtonDriver bidButton() {
Line 409:     return new JButtonDriver(this, JButton.class, named(MainWindow.JOIN_BUTTON_NAME));
Line 410:   }
Line 411: […]
Line 412: }
Line 413: Neither of these components exist yet, so the test fails looking for the text ﬁeld.
Line 414: […] but...
Line 415:     all top level windows
Line 416:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 417: contained 0 JTextField (with name "item id")
Line 418: Adding an Action Bar
Line 419: We address this failure by adding a new panel across the top to contain the
Line 420: text ﬁeld for the identiﬁer and the Join Auction button, wrapping up the activity
Line 421: in a makeControls() method to help express our intent. We realize that this code
Line 422: isn’t very exciting, but we want to show its structure now before we add any
Line 423: behavior.
Line 424: Chapter 16
Line 425: Sniping for Multiple Items
Line 426: 184
Line 427: 
Line 428: --- 페이지 210 ---
Line 429: public class MainWindow extends JFrame {
Line 430:   public MainWindow(TableModel snipers) {
Line 431:     super(APPLICATION_TITLE);
Line 432:     setName(MainWindow.MAIN_WINDOW_NAME);
Line 433:     fillContentPane(makeSnipersTable(snipers), makeControls());
Line 434: […]
Line 435:   }
Line 436:   private JPanel makeControls() {
Line 437:     JPanel controls = new JPanel(new FlowLayout());
Line 438:     final JTextField itemIdField = new JTextField();
Line 439:     itemIdField.setColumns(25);
Line 440:     itemIdField.setName(NEW_ITEM_ID_NAME);
Line 441:     controls.add(itemIdField);
Line 442:     JButton joinAuctionButton = new JButton("Join Auction");
Line 443:     joinAuctionButton.setName(JOIN_BUTTON_NAME);
Line 444:     controls.add(joinAuctionButton);
Line 445:     return controls;
Line 446:   }
Line 447: […]
Line 448: }
Line 449: With the action bar in place, our next test fails because we don’t create the
Line 450: identiﬁed rows in the table model.
Line 451: […] but...
Line 452:    all top level windows
Line 453:    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 454:    contained 1 JTable ()
Line 455: it is not with row with cells
Line 456:    <label with text "item-54321">, <label with text "0">, 
Line 457:    <label with text "0">, <label with text "Joining">
Line 458: A Design Moment
Line 459: Now what do we do? To review our position: we have a broken acceptance
Line 460: test pending, we have the user interface structure but no behavior, and the
Line 461: SnipersTableModel still handles only one Sniper at a time. Our goal is that, when
Line 462: we click on the Join Auction button, the application will attempt to join the
Line 463: auction speciﬁed in the item ﬁeld and add a new row to the list of auctions to
Line 464: show that the request is being handled.
Line 465: In practice, this means that we need a Swing ActionListener for the JButton
Line 466: that will use the text from the JTextField as an item identiﬁer for the new session.
Line 467: Its implementation will add a row to the SnipersTableModel and create a new
Line 468: Chat to the Southabee’s On-Line server. The catch is that everything to do with
Line 469: connections is in Main, whereas the button and the text ﬁeld are in MainWindow.
Line 470: This is a distinction we’d like to maintain, since it keeps the responsibilities of
Line 471: the two classes focused.
Line 472: 185
Line 473: Adding Items through the User Interface
Line 474: 
Line 475: --- 페이지 211 ---
Line 476: We stop for a moment to think about the structure of the code, using the CRC
Line 477: cards we mentioned in “Roles, Responsibilities, Collaborators” on page 16 to
Line 478: help us visualize our ideas. After some discussion, we remind ourselves that the
Line 479: job of MainWindow is to manage our UI components and their interactions; it
Line 480: shouldn’t also have to manage concepts such as “connection” or “chat.” When
Line 481: a user interaction implies an action outside the user interface, MainWindow should
Line 482: delegate to a collaborating object.
Line 483: To express this, we decide to add a listener to MainWindow to notify neighboring
Line 484: objects about such requests. We call the new collaborator a UserRequestListener
Line 485: since it will be responsible for handling requests made by the user:
Line 486: public interface UserRequestListener extends EventListener {
Line 487:   void joinAuction(String itemId);
Line 488: }
Line 489: Another Level of Testing
Line 490: We want to write a test for our proposed new behavior, but we can’t just write
Line 491: a simple unit test because of Swing threading. We can’t be sure that the Swing
Line 492: code will have ﬁnished running by the time we check any assertions at the end
Line 493: of the test, so we need something that will wait until the tested code has
Line 494: stabilized—what we usually call an integration test because it’s testing how our
Line 495: code works with a third-party library. We can use WindowLicker for this level
Line 496: of testing as well as for our end-to-end tests. Here’s the new test:
Line 497: public class MainWindowTest {
Line 498:   private final SnipersTableModel tableModel = new SnipersTableModel();
Line 499:   private final MainWindow mainWindow = new MainWindow(tableModel);
Line 500:   private final AuctionSniperDriver driver = new AuctionSniperDriver(100);
Line 501:   @Test public void
Line 502: makesUserRequestWhenJoinButtonClicked() {
Line 503:     final ValueMatcherProbe<String> buttonProbe = 
Line 504:       new ValueMatcherProbe<String>(equalTo("an item-id"), "join request");
Line 505:     mainWindow.addUserRequestListener(
Line 506:         new UserRequestListener() {
Line 507:           public void joinAuction(String itemId) {
Line 508:             buttonProbe.setReceivedValue(itemId);
Line 509:           }
Line 510:         });
Line 511:     driver.startBiddingFor("an item-id");
Line 512:     driver.check(buttonProbe);
Line 513:   }
Line 514: }
Line 515: Chapter 16
Line 516: Sniping for Multiple Items
Line 517: 186
Line 518: 
Line 519: --- 페이지 212 ---
Line 520: WindowLicker Probes
Line 521: In WindowLicker, a probe is an object that checks for a given state. A driver’s
Line 522: check() method repeatedly ﬁres the given probe until it’s satisﬁed or times out. In
Line 523: this test, we use a ValueMatcherProbe, which compares a value against a Ham-
Line 524: crest matcher, to wait for the UserRequestListener’s joinAuction() to be called
Line 525: with the right auction identiﬁer.
Line 526: We create an empty implementation of MainWindow.addUserRequestListener,
Line 527: to get through the compiler, and the test fails:
Line 528: Tried to look for...
Line 529:     join request "an item-id"
Line 530: but...
Line 531:     join request "an item-id". Received nothing
Line 532: To make this test pass, we ﬁll in the request listener infrastructure in MainWindow
Line 533: using Announcer, a utility class that manages collections of listeners.2 We add a
Line 534: Swing ActionListener that extracts the item identiﬁer and announces it to the
Line 535: request listeners. The relevant parts of MainWindow look like this:
Line 536: public class MainWindow extends JFrame {
Line 537:   private final Announcer<UserRequestListener> userRequests = 
Line 538:                                      Announcer.to(UserRequestListener.class); 
Line 539:   public void addUserRequestListener(UserRequestListener userRequestListener) {
Line 540:     userRequests.addListener(userRequestListener); 
Line 541:   } 
Line 542: […]
Line 543:   private JPanel makeControls(final SnipersTableModel snipers) {
Line 544: […]
Line 545:     joinAuctionButton.addActionListener(new ActionListener() {
Line 546:       public void actionPerformed(ActionEvent e) {
Line 547: userRequests.announce().joinAuction(itemIdField.getText());
Line 548:       }
Line 549:     });
Line 550: […]
Line 551:   }
Line 552: }
Line 553: To emphasize the point here, we’ve converted an ActionListener event, which
Line 554: is internal to the user interface framework, to a UserRequestListener event,
Line 555: which is about users interacting with an auction. These are two separate domains
Line 556: and MainWindow’s job is to translate from one to the other. MainWindow is
Line 557: not concerned with how any implementation of UserRequestListener might
Line 558: work—that would be too much responsibility.
Line 559: 2.
Line 560: Announcer is included in the examples that ship with jMock.
Line 561: 187
Line 562: Adding Items through the User Interface
Line 563: 
Line 564: --- 페이지 213 ---
Line 565: Micro-Hubris
Line 566: In case this level of testing seems like overkill, when we ﬁrst wrote this example
Line 567: we managed to return the text ﬁeld’s name, not its text—one was item-id and the
Line 568: other was item id. This is just the sort of bug that’s easy to let slip through and a
Line 569: nightmare to unpick in end-to-end tests—which is why we like to also write
Line 570: integration-level tests.
Line 571: Implementing the UserRequestListener
Line 572: We return to Main to see where we can plug in our new UserRequestListener.
Line 573: The changes are minor because we did most of the work when we restructured
Line 574: the class earlier in this chapter. We decide to preserve most of the existing
Line 575: code for now (even though it’s not quite the right shape) until we’ve made
Line 576: more progress, so we just inline our previous joinAuction() method into the
Line 577: UserRequestListener’s. We’re also pleased to remove the safelyAddItemToModel()
Line 578: wrapper, since the UserRequestListener will be called on the Swing thread. This
Line 579: is not obvious from the code as it stands; we make a note to address that later.
Line 580: public class Main {
Line 581:   public static void main(String... args) throws Exception {
Line 582:     Main main = new Main();
Line 583:     XMPPConnection connection = 
Line 584:       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line 585:     main.disconnectWhenUICloses(connection);
Line 586: main.addUserRequestListenerFor(connection);
Line 587:   }
Line 588:   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line 589:     ui.addUserRequestListener(new UserRequestListener() {
Line 590:       public void joinAuction(String itemId) {
Line 591: snipers.addSniper(SniperSnapshot.joining(itemId));
Line 592:         Chat chat = connection.getChatManager()
Line 593:                                  .createChat(auctionId(itemId, connection), null);
Line 594:         notToBeGCd.add(chat); 
Line 595:         Auction auction = new XMPPAuction(chat);
Line 596:         chat.addMessageListener(
Line 597:                new AuctionMessageTranslator(connection.getUser(),
Line 598:                      new AuctionSniper(itemId, auction, 
Line 599:                                        new SwingThreadSniperListener(snipers))));
Line 600:         auction.join();
Line 601:       }
Line 602:     });
Line 603:   }
Line 604: }
Line 605: We try our end-to-end tests again and ﬁnd that they pass. Slightly stunned, we
Line 606: break for coffee.
Line 607: Chapter 16
Line 608: Sniping for Multiple Items
Line 609: 188
Line 610: 
Line 611: --- 페이지 214 ---
Line 612: Observations
Line 613: Making Steady Progress
Line 614: We’re starting to see more payback from some of our restructuring work. It was
Line 615: pretty easy to convert the end-to-end test to handle multiple items, and most of
Line 616: the implementation consisted of teasing apart code that was already working.
Line 617: We’ve been careful to keep class responsibilities focused—except for the one
Line 618: place, Main, where we’ve put all our working compromises.
Line 619: We made an effort to stay honest about writing enough tests, which has forced
Line 620: us to consider a couple of edge cases we might otherwise have left. We also intro-
Line 621: duced a new intermediate-level “integration” test to allow us to work out the
Line 622: implementation of the user interface without dragging in the rest of the system.
Line 623: TDD Conﬁdential
Line 624: We don’t write up everything that went into the development of our
Line 625: examples—that would be boring and waste paper—but we think it’s worth a
Line 626: note about what happened with this one. It took us a couple of attempts to get
Line 627: this design pointing in the right direction because we were trying to allocate be-
Line 628: havior to the wrong objects. What kept us honest was that for each attempt to
Line 629: write tests that were focused and made sense, the setup and our assertions kept
Line 630: drifting apart. Once we’d broken through our inadequacies as programmers, the
Line 631: tests became much clearer.
Line 632: Ship It?
Line 633: So now that everything works we can get on with more features, right? Wrong.
Line 634: We don’t believe that “working” is the same thing as “ﬁnished.” We’ve left quite
Line 635: a design mess in Main as we sorted out our ideas, with functionality from various
Line 636: slices of the application all jumbled into one, as in Figure 16.3.  Apart from the
Line 637: confusion this leaves, most of this code is not really testable except through the
Line 638: end-to-end tests. We can get away with that now, while the code is still small,
Line 639: but it will be difﬁcult to sustain as the application grows. More importantly,
Line 640: perhaps, we’re not getting any unit-test feedback about the internal quality of
Line 641: the code.
Line 642: We might put this code into production if we knew the code was never going
Line 643: to change or there was an emergency. We know that the ﬁrst isn’t true, because
Line 644: the application isn’t ﬁnished yet, and being in a hurry is not really a crisis. We
Line 645: know we will be working in this code again soon, so we can either clean up now,
Line 646: while it’s still fresh in our minds, or re-learn it every time we touch it. Given that
Line 647: we’re trying to make an educational point here, you’ve probably guessed
Line 648: what we’ll do next.
Line 649: 189
Line 650: Observations
Line 651: 
Line 652: --- 페이지 215 ---
Line 653: This page intentionally left blank 