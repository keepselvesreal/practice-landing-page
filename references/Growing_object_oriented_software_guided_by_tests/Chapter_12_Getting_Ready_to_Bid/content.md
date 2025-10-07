Line 1: 
Line 2: --- 페이지 130 ---
Line 3: Chapter 12
Line 4: Getting Ready to Bid
Line 5: In which we write an end-to-end test so that we can make the Sniper
Line 6: bid in an auction. We start to interpret the messages in the auction
Line 7: protocol and discover some new classes in the process. We write our
Line 8: ﬁrst unit tests and then refactor out a helper class. We describe every
Line 9: last detail of this effort to show what we were thinking at the time.
Line 10: An Introduction to the Market
Line 11: Now, to continue with the skeleton metaphor, we start to ﬂesh out the application.
Line 12: The core behavior of a Sniper is that it makes a higher bid on an item in an auction
Line 13: when there’s a change in price. Going back to our to-do list, we revisit the next
Line 14: couple of items:
Line 15: •
Line 16: Single item: join, bid, and lose. When a price comes in, send a bid raised
Line 17: by the minimum increment deﬁned by the auction. This amount will be
Line 18: included in the price update information.
Line 19: •
Line 20: Single item: join, bid, and win. Distinguish which bidder is currently winning
Line 21: the auction and don’t bid against ourselves.
Line 22: We know there’ll be more coming, but this is a coherent slice of functionality
Line 23: that will allow us to explore the design and show concrete progress.
Line 24: In any distributed system similar to this one there are lots of interesting failure
Line 25: and timing issues, but our application only has to deal with the client side of the
Line 26: protocol. We rely on the underlying XMPP protocol to deal with many common
Line 27: distributed programming problems; in particular, we expect it to ensure that
Line 28: messages between a bidder and an auction arrive in the same order in which they
Line 29: were sent.
Line 30: As we described in Chapter 5, we start the next feature with an acceptance
Line 31: test. We used our ﬁrst test in the previous chapter to help ﬂush out the structure
Line 32: of our application. From now on, we can use acceptance tests to show incremental
Line 33: progress.
Line 34: 105
Line 35: 
Line 36: --- 페이지 131 ---
Line 37: A Test for Bidding
Line 38: Starting with a Test
Line 39: Each acceptance test we write should have just enough new requirements to force
Line 40: a manageable increase in functionality, so we decide that the next one will add
Line 41: some price information. The steps are:
Line 42: 1.
Line 43: Tell the auction to send a price to the Sniper.
Line 44: 2.
Line 45: Check the Sniper has received and responded to the price.
Line 46: 3.
Line 47: Check the auction has received an incremented bid from Sniper.
Line 48: To make this pass, the Sniper will have to distinguish between Price and Close
Line 49: events from the auction, display the current price, and generate a new bid. We’ll
Line 50: also have to extend our stub auction to handle bids. We’ve deferred implementing
Line 51: other functionality that will also be required, such as displaying when the Sniper
Line 52: has won the auction; we’ll get to that later. Here’s the new test:
Line 53: public class AuctionSniperEndToEndTest {
Line 54:   @Test public void
Line 55: sniperMakesAHigherBidButLoses() throws Exception {
Line 56:     auction.startSellingItem();
Line 57:     application.startBiddingIn(auction);
Line 58:     auction.hasReceivedJoinRequestFromSniper(); 1
Line 59:     auction.reportPrice(1000, 98, "other bidder"); 2
Line 60:     application.hasShownSniperIsBidding(); 3
Line 61:     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID); 4
Line 62:     auction.announceClosed(); 5
Line 63:     application.showsSniperHasLostAuction();   
Line 64:   }
Line 65: }
Line 66: We have three new methods to implement as part of this test.
Line 67: 1
Line 68: We have to wait for the stub auction to receive the Join request before con-
Line 69: tinuing with the test. We use this assertion to synchronize the Sniper with
Line 70: the auction.
Line 71: 2
Line 72: This method tells the stub auction to send a message back to the Sniper with
Line 73: the news that at the moment the price of the item is 1000, the increment for
Line 74: the next bid is 98, and the winning bidder is “other bidder.”
Line 75: 3
Line 76: This method asks the ApplicationRunner to check that the Sniper shows that
Line 77: it’s now bidding after it’s received the price update message from the auction.
Line 78: Chapter 12
Line 79: Getting Ready to Bid
Line 80: 106
Line 81: 
Line 82: --- 페이지 132 ---
Line 83: 4
Line 84: This method asks the stub auction to check that it has received a bid from
Line 85: the Sniper that is equal to the last price plus the minimum increment. We
Line 86: have to do a fraction more work because the XMPP layer constructs a longer
Line 87: name from the basic identiﬁer, so we deﬁne a constant SNIPER_XMPP_ID which
Line 88: in practice is sniper@localhost/Auction.
Line 89: 5
Line 90: We reuse the closing logic from the ﬁrst test, as the Sniper still loses the
Line 91: auction.
Line 92: Unrealistic Money
Line 93: We’re using integers to represent value (imagine that auctions are conducted in
Line 94: Japanese Yen). In a real system, we would deﬁne a domain type to represent
Line 95: monetary values, using a ﬁxed decimal implementation. Here, we simplify the
Line 96: representation to make the example code easier to ﬁt onto a printed page.
Line 97: Extending the Fake Auction
Line 98: We have two methods to write in the FakeAuctionServer to support the end-
Line 99: to-end test: reportPrice() has to send a Price message through the chat;
Line 100: hasReceivedBid() is a little more complex—it has to check that the auction re-
Line 101: ceived the right values from the Sniper. Instead of parsing the incoming message,
Line 102: we construct the expected message and just compare strings. We also pull up the
Line 103: Matcher clause from the SingleMessageListener to give the FakeAuctionServer
Line 104: more ﬂexibility in deﬁning what it will accept as a message. Here’s a ﬁrst cut:
Line 105: public class FakeAuctionServer { […]
Line 106:   public void reportPrice(int price, int increment, String bidder) 
Line 107:     throws XMPPException 
Line 108:   {
Line 109:     currentChat.sendMessage(
Line 110:         String.format("SOLVersion: 1.1; Event: PRICE; "
Line 111:                       + "CurrentPrice: %d; Increment: %d; Bidder: %s;",
Line 112:                       price, increment, bidder));
Line 113:   }
Line 114:   public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
Line 115:     messageListener.receivesAMessage(is(anything()));
Line 116:   }
Line 117:   public void hasReceivedBid(int bid, String sniperId) 
Line 118:     throws InterruptedException 
Line 119:   {
Line 120:     assertThat(currentChat.getParticipant(), equalTo(sniperId));
Line 121:     messageListener.receivesAMessage(
Line 122:       equalTo(
Line 123:         String.format("SOLVersion: 1.1; Command: BID; Price: %d;", bid)));
Line 124:   }
Line 125: }
Line 126: 107
Line 127: A Test for Bidding
Line 128: 
Line 129: --- 페이지 133 ---
Line 130: public class SingleMessageListener implements MessageListener { […]
Line 131:   @SuppressWarnings("unchecked")
Line 132:   public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line 133:     throws InterruptedException 
Line 134:   {
Line 135:     final Message message = messages.poll(5, TimeUnit.SECONDS);
Line 136:     assertThat("Message", message, is(notNullValue()));
Line 137:     assertThat(message.getBody(), messageMatcher);
Line 138:   }
Line 139: }
Line 140: Looking again, there’s an imbalance between the two “receives” methods. The
Line 141: Join method is much more lax than the bid message, in terms of both the contents
Line 142: of the message and the sender; we will have to remember to come back later and
Line 143: ﬁx it. We defer a great many decisions when developing incrementally, but
Line 144: sometimes consistency and symmetry make more sense. We decide to retroﬁt
Line 145: more detail into hasReceivedJoinRequestFromSniper() while we have the code
Line 146: cracked open. We also extract the message formats and move them to Main
Line 147: because we’ll need them to construct raw messages in the Sniper.
Line 148: public class FakeAuctionServer { […]
Line 149:   public void hasReceivedJoinRequestFrom(String sniperId) 
Line 150:     throws InterruptedException 
Line 151:   {
Line 152: receivesAMessageMatching(sniperId, equalTo(Main.JOIN_COMMAND_FORMAT));
Line 153:   }
Line 154:   public void hasReceivedBid(int bid, String sniperId) 
Line 155:     throws InterruptedException 
Line 156:   {
Line 157: receivesAMessageMatching(sniperId, 
Line 158:                              equalTo(format(Main.BID_COMMAND_FORMAT, bid)));
Line 159:   }
Line 160:   private void receivesAMessageMatching(String sniperId, 
Line 161:                                         Matcher<? super String> messageMatcher)
Line 162:     throws InterruptedException 
Line 163:   {
Line 164:     messageListener.receivesAMessage(messageMatcher);
Line 165:     assertThat(currentChat.getParticipant(), equalTo(sniperId));
Line 166:   }
Line 167: }
Line 168: Notice that we check the Sniper’s identiﬁer after we check the contents of the
Line 169: message. This forces the server to wait until the message has arrived, which means
Line 170: that it must have accepted a connection and set up currentChat. Otherwise the
Line 171: test would fail by checking the Sniper’s identiﬁer prematurely.
Line 172: Chapter 12
Line 173: Getting Ready to Bid
Line 174: 108
Line 175: 
Line 176: --- 페이지 134 ---
Line 177: Double-Entry Values
Line 178: We’re using the same constant to both create a Join message and check its con-
Line 179: tents. By using the same construct, we’re removing duplication and expressing in
Line 180: the code a link between the two sides of the system. On the other hand, we’re
Line 181: making ourselves vulnerable to getting them both wrong and not having a test to
Line 182: catch the invalid content. In this case, the code is so simple that pretty much any
Line 183: implementation would do, but the answers become less certain when developing
Line 184: something more complex, such as a persistence layer. Do we use the same
Line 185: framework to write and read our values? Can we be sure that it’s not just caching
Line 186: the results, or that the values are persisted correctly? Should we just write some
Line 187: straight database queries to be sure?
Line 188: The critical question is, what do we think we’re testing? Here, we think that the
Line 189: communication features are more important, that the messages are simple enough
Line 190: so we can rely on string constants, and that we’d like to be able to ﬁnd code related
Line 191: to message formats in the IDE. Other developers might come to a different
Line 192: conclusion and be right for their project.
Line 193: We adjust the end-to-end tests to match the new API, watch the test fail, and
Line 194: then add the extra detail to the Sniper to make the test pass.
Line 195: public class AuctionSniperEndToEndTest {
Line 196:   @Test public void
Line 197: sniperMakesAHigherBidButLoses() throws Exception {
Line 198:     auction.startSellingItem();
Line 199:     application.startBiddingIn(auction);
Line 200: auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 201:     auction.reportPrice(1000, 98, "other bidder");
Line 202:     application.hasShownSniperIsBidding();
Line 203:     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line 204:     auction.announceClosed();                  
Line 205:     application.showsSniperHasLostAuction();   
Line 206:   }
Line 207: }
Line 208: 109
Line 209: A Test for Bidding
Line 210: 
Line 211: --- 페이지 135 ---
Line 212: public class Main { […]
Line 213:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 214:     throws XMPPException 
Line 215:   {
Line 216:     Chat chat = connection.getChatManager().createChat(
Line 217:         auctionId(itemId, connection), 
Line 218:         new MessageListener() {
Line 219:           public void processMessage(Chat aChat, Message message) {
Line 220:             SwingUtilities.invokeLater(new Runnable() {
Line 221:               public void run() {
Line 222:                 ui.showStatus(MainWindow.STATUS_LOST);
Line 223:               }
Line 224:             });
Line 225:           }
Line 226:         });
Line 227:     this.notToBeGCd = chat;
Line 228:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 229:   }
Line 230: }
Line 231: A Surprise Failure
Line 232: Finally we write the “checking” method on the ApplicationRunner to give us
Line 233: our ﬁrst failure. The implementation is simple: we just add another status constant
Line 234: and copy the existing method.
Line 235: public class ApplicationRunner { […]
Line 236: public void hasShownSniperIsBidding() {
Line 237:     driver.showsSniperStatus(MainWindow.STATUS_BIDDING);
Line 238:   }
Line 239:   public void showsSniperHasLostAuction() {
Line 240:     driver.showsSniperStatus(MainWindow.STATUS_LOST);
Line 241:   }
Line 242: }
Line 243: We’re expecting to see something about a missing label text but instead we
Line 244: get this:
Line 245: java.lang.AssertionError: 
Line 246: Expected: is not null
Line 247:      got: null
Line 248: […]
Line 249:   at auctionsniper.SingleMessageListener.receivesAMessage()
Line 250:   at auctionsniper.FakeAuctionServer.hasReceivedJoinRequestFromSniper()
Line 251:   at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBid()
Line 252: […]
Line 253: and this on the error stream:
Line 254: Chapter 12
Line 255: Getting Ready to Bid
Line 256: 110
Line 257: 
Line 258: --- 페이지 136 ---
Line 259: conflict(409)
Line 260:   at jivesoftware.smack.SASLAuthentication.bindResourceAndEstablishSession()
Line 261:   at jivesoftware.smack.SASLAuthentication.authenticate()
Line 262:   at jivesoftware.smack.XMPPConnection.login()
Line 263:   at jivesoftware.smack.XMPPConnection.login()
Line 264:   at auctionsniper.Main.connection()
Line 265:   at auctionsniper.Main.main()
Line 266: After some investigation we realize what’s happened. We’ve introduced a second
Line 267: test which tries to connect using the same account and resource name as the ﬁrst.
Line 268: The server is conﬁgured, like Southabee’s On-Line, to reject multiple open con-
Line 269: nections, so the second test fails because the server thinks that the ﬁrst is still
Line 270: connected. In production, our application would work because we’d stop the
Line 271: whole process when closing, which would break the connection. Our little com-
Line 272: promise (of starting the application in a new thread) has caught us out. The Right
Line 273: Thing to do here is to add a callback to disconnect the client when we close the
Line 274: window so that the application will clean up after itself:
Line 275: public class Main { […]
Line 276:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 277:     throws XMPPException 
Line 278:   {
Line 279: disconnectWhenUICloses(connection);
Line 280:     Chat chat = connection.getChatManager().createChat(
Line 281: […]
Line 282:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 283:   }
Line 284:   private void disconnectWhenUICloses(final XMPPConnection connection) {
Line 285:     ui.addWindowListener(new WindowAdapter() {
Line 286:       @Override public void windowClosed(WindowEvent e) {
Line 287: connection.disconnect();
Line 288:       }
Line 289:     });
Line 290:   }
Line 291: }
Line 292: Now we get the failure we expected, because the Sniper has no way to start
Line 293: bidding.
Line 294: java.lang.AssertionError: 
Line 295: Tried to look for...
Line 296:     exactly 1 JLabel (with name "sniper status")
Line 297:     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 298:     in all top level windows
Line 299: and check that its label text is "Bidding"
Line 300: but...
Line 301:     all top level windows
Line 302:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 303:     contained 1 JLabel (with name "sniper status")
Line 304: label text was "Lost"
Line 305: […]
Line 306:   at auctionsniper.AuctionSniperDriver.showsSniperStatus()
Line 307:   at auctionsniper.ApplicationRunner.hasShownSniperIsBidding()
Line 308:   at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBidButLoses()
Line 309: 111
Line 310: A Test for Bidding
Line 311: 
Line 312: --- 페이지 137 ---
Line 313: Outside-In Development
Line 314: This failure deﬁnes the target for our next coding episode. It tells us, at a high
Line 315: level, what we’re aiming for—we just have to ﬁll in implementation until it
Line 316: passes.
Line 317: Our approach to test-driven development is to start with the outside event that
Line 318: triggers the behavior we want to implement and work our way into the code an
Line 319: object at a time, until we reach a visible effect (such as a sent message or log entry)
Line 320: indicating that we’ve achieved our goal. The end-to-end test shows us the end
Line 321: points of that process, so we can explore our way through the space in the middle.
Line 322: In the following sections, we build up the types we need to implement our
Line 323: Auction Sniper. We’ll take it slowly, strictly by the TDD rules, to show how the
Line 324: process works. In real projects, we sometimes design a bit further ahead to get
Line 325: a sense of the bigger picture, but much of the time this is what we actually do.
Line 326: It produces the right results and forces us to ask the right questions.
Line 327: Inﬁnite Attention to Detail?
Line 328: We caught the resource clash because, by luck or insight, our server conﬁguration
Line 329: matched that of Southabee’s On-Line. We might have used an alternative setting
Line 330: which allows new connections to kick off existing ones, which would have resulted
Line 331: in the tests passing but with a confusing conﬂict message from the Smack library
Line 332: on the error stream. This would have worked ﬁne in development, but with a
Line 333: risk of Snipers starting to fail in production.
Line 334: How can we hope to catch all the conﬁguration options in an entire system?
Line 335: At some level we can’t, and this is at the heart of what professional testers do.
Line 336: What we can do is push to exercise as much as possible of the system as early as
Line 337: possible, and to do so repeatedly. We can also help ourselves cope with total
Line 338: system complexity by keeping the quality of its components high and by constantly
Line 339: pushing to simplify. If that sounds expensive, consider the cost of ﬁnding and
Line 340: ﬁxing a transient bug like this one in a busy production system.
Line 341: The AuctionMessageTranslator
Line 342: Teasing Out a New Class
Line 343: Our entry point to the Sniper is where we receive a message from the auction
Line 344: through the Smack library: it’s the event that triggers the next round of behavior
Line 345: we want to make work. In practice, this means that we need a class implementing
Line 346: MessageListener to attach to the Chat. When this class receives a raw message
Line 347: from the auction, it will translate it into something that represents an auction
Line 348: event within our code which, eventually, will prompt a Sniper action and a change
Line 349: in the user interface.
Line 350: Chapter 12
Line 351: Getting Ready to Bid
Line 352: 112
Line 353: 
Line 354: --- 페이지 138 ---
Line 355: We already have such a class in Main—it’s anonymous and its responsibilities
Line 356: aren’t very obvious:
Line 357: new MessageListener() {
Line 358:   public void processMessage(Chat aChat, Message message) {
Line 359:     SwingUtilities.invokeLater(new Runnable() {
Line 360:       public void run() {
Line 361:         ui.showStatus(MainWindow.STATUS_LOST);
Line 362:       }
Line 363:     });
Line 364:   }
Line 365: }
Line 366: This code implicitly accepts a Close message (the only kind of message we
Line 367: have so far) and implements the Sniper’s response. We’d like to make this situation
Line 368: explicit before we add more features. We start by promoting the anonymous
Line 369: class to a top-level class in its own right, which means it needs a name. From our
Line 370: description in the paragraph above, we pick up the word “translate” and call it
Line 371: an AuctionMessageTranslator, because it will translate messages from the auction.
Line 372: The catch is that the current anonymous class picks up the ui ﬁeld from Main.
Line 373: We’ll have to attach something to our newly promoted class so that it can respond
Line 374: to a message. The most obvious thing to do is pass it the MainWindow but we’re
Line 375: unhappy about creating a dependency on a user interface component. That would
Line 376: make it hard to unit-test, because we’d have to query the state of a component
Line 377: that’s running in the Swing event thread.
Line 378: More signiﬁcantly, such a dependency would break the “single responsibility”
Line 379: principle which says that unpacking raw messages from the auction is quite
Line 380: enough for one class to do, without also having to know how to present the
Line 381: Sniper status. As we wrote in “Designing for Maintainability” (page 47), we
Line 382: want to maintain a separation of concerns.
Line 383: Given these constraints, we decide that our new AuctionMessageTranslator
Line 384: will delegate the handling of an interpreted event to a collaborator, which we will
Line 385: represent with an AuctionEventListener interface; we can pass an object that
Line 386: implements it into the translator on construction. We don’t yet know what’s in
Line 387: this interface and we haven’t yet begun to think about its implementation. Our
Line 388: immediate concern is to get the message translation to work; the rest can wait.
Line 389: So far the design looks like Figure 12.1 (types that belong to external frameworks,
Line 390: such as Chat, are shaded):
Line 391: Figure 12.1
Line 392: The AuctionMessageTranslator
Line 393: 113
Line 394: The AuctionMessageTranslator
Line 395: 
Line 396: --- 페이지 139 ---
Line 397: The First Unit Test
Line 398: We start with the simpler event type. As we’ve seen, a Close event has no
Line 399: values—it’s a simple trigger. When the translator receives one, we want it to call
Line 400: its listener appropriately.
Line 401: As this is our ﬁrst unit test, we’ll build it up very slowly to show the process
Line 402: (later, we will move faster). We start with the test method name. JUnit picks up
Line 403: test methods by reﬂection, so we can make their names as long and descriptive
Line 404: as we like because we never have to include them in code. The ﬁrst test says that
Line 405: the translator will tell anything that’s listening that the auction has closed when
Line 406: it receives a raw Close message.
Line 407: package test.auctionsniper;
Line 408: public class AuctionMessageTranslatorTest {
Line 409:   @Test public void
Line 410: notifiesAuctionClosedWhenCloseMessageReceived() {
Line 411: // nothing yet
Line 412:   }
Line 413: }
Line 414: Put Tests in a Different Package
Line 415: We’ve adopted a habit of putting tests in a different package from the code they’re
Line 416: exercising.We want to make sure we’re driving the code through its public interfaces,
Line 417: like any other client, rather than opening up a package-scoped back door for testing.
Line 418: We also ﬁnd that, as the application and test code grows, separate packages make
Line 419: navigation in modern IDEs easier.
Line 420: The next step is to add the action that will trigger the behavior we want to
Line 421: test—in this case, sending a Close message. We already know what this will look
Line 422: like since it’s a call to the Smack MessageListener interface.
Line 423: public class AuctionMessageTranslatorTest {
Line 424:   public static final Chat UNUSED_CHAT = null;
Line 425: private final AuctionMessageTranslator translator = 
Line 426:                                               new AuctionMessageTranslator();
Line 427:   @Test public void
Line 428: notfiesAuctionClosedWhenCloseMessageReceived() {
Line 429: Message message = new Message();
Line 430:     message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line 431:     translator.processMessage(UNUSED_CHAT, message);
Line 432:   }
Line 433: }
Line 434: Chapter 12
Line 435: Getting Ready to Bid
Line 436: 114
Line 437: 
Line 438: --- 페이지 140 ---
Line 439: Use null When an Argument Doesn’t Matter
Line 440: UNUSED_CHAT is a meaningful name for a constant that is deﬁned as null.We pass
Line 441: it into processMessage() instead of a real Chat object because the Chat class is
Line 442: difﬁcult to instantiate—its constructor is package-scoped and we’d have to ﬁll in a
Line 443: chain of dependencies to create one. As it happens, we don’t need one anyway
Line 444: for the current functionality, so we just pass in a null value to satisfy the compiler
Line 445: but use a named constant to make clear its signiﬁcance.
Line 446: To be clear, this null is not a null object [Woolf98] which may be called and will
Line 447: do nothing in response. This null is just a placeholder and will fail if called during
Line 448: the test.
Line 449: We generate a skeleton implementation from the MessageListener interface.
Line 450: package auctionsniper;
Line 451: public class AuctionMessageTranslator implements MessageListener {
Line 452:   public void processMessage(Chat chat, Message message) {
Line 453: // TODO Fill in here
Line 454:   }
Line 455: }
Line 456: Next, we want a check that shows whether the translation has taken
Line 457: place—which should fail since we haven’t implemented anything yet. We’ve al-
Line 458: ready decided that we want our translator to notify its listener when the Close
Line 459: event occurs, so we’ll describe that expected behavior in our test.
Line 460: @RunWith(JMock.class) 
Line 461: public class AuctionMessageTranslatorTest {
Line 462:   private final Mockery context = new Mockery();
Line 463:   private final AuctionEventListener listener = 
Line 464:                               context.mock(AuctionEventListener.class); 
Line 465:   private final AuctionMessageTranslator translator = 
Line 466:                                         new AuctionMessageTranslator();
Line 467:   @Test public void
Line 468: notfiesAuctionClosedWhenCloseMessageReceived() {
Line 469:     context.checking(new Expectations() {{
Line 470: oneOf(listener).auctionClosed();
Line 471:     }});
Line 472:     Message message = new Message();
Line 473:     message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line 474:     translator.processMessage(UNUSED_CHAT, message);
Line 475:   }
Line 476: }
Line 477: 115
Line 478: The AuctionMessageTranslator
Line 479: 
Line 480: --- 페이지 141 ---
Line 481: This is more or less the kind of unit test we described at the end of Chapter 2,
Line 482: so we won’t go over its structure again here except to emphasize the highlighted
Line 483: expectation line. This is the most signiﬁcant line in the test, our declaration of
Line 484: what matters about the translator’s effect on its environment. It says that when
Line 485: we send an appropriate message to the translator, we expect it to call the listener’s
Line 486: auctionClosed() method exactly once.
Line 487: We get a failure that shows that we haven’t implemented the behavior we need:
Line 488: not all expectations were satisfied
Line 489: expectations:
Line 490:   ! expected once, never invoked: auctionEventListener.auctionClosed()
Line 491: what happened before this: nothing!
Line 492:   at org.jmock.Mockery.assertIsSatisfied(Mockery.java:199)
Line 493:   […]
Line 494:   at org.junit.internal.runners.JUnit4ClassRunner.run()
Line 495: The critical phrase is this one:
Line 496: expected once, never invoked: auctionEventListener.auctionClosed()
Line 497: which tells us that we haven’t called the listener as we should have.
Line 498: We need to do two things to make the test pass. First, we need to connect the
Line 499: translator and listener so that they can communicate. We decide to pass the lis-
Line 500: tener into the translator’s constructor; it’s simple and ensures that the translator
Line 501: is always set up correctly with a listener—the Java type system won’t let us forget.
Line 502: The test setup looks like this:
Line 503: public class AuctionMessageTranslatorTest {
Line 504:   private final Mockery context = new Mockery();
Line 505:   private final AuctionEventListener listener = 
Line 506:                                      context.mock(AuctionEventListener.class);
Line 507:   private final AuctionMessageTranslator translator = 
Line 508:                                        new AuctionMessageTranslator(listener);
Line 509: The second thing we need to do is call the auctionClosed() method. Actually,
Line 510: that’s all we need to do to make this test pass, since we haven’t deﬁned any other
Line 511: behavior.
Line 512: public void processMessage(Chat chat, Message message) {
Line 513:     listener.auctionClosed();
Line 514:   }
Line 515: The test passes. This might feel like cheating since we haven’t actually unpacked
Line 516: a message. What we have done is ﬁgured out where the pieces are and got them
Line 517: into a test harness—and locked down one piece of functionality that should
Line 518: continue to work as we add more features.
Line 519: Chapter 12
Line 520: Getting Ready to Bid
Line 521: 116
Line 522: 
Line 523: --- 페이지 142 ---
Line 524: Simpliﬁed Test Setup
Line 525: You might have noticed that all the ﬁelds in the test class are final. As we described
Line 526: in Chapter 3, JUnit creates a new instance of the test class for each test method,
Line 527: so the ﬁelds are recreated for each test method. We exploit this by declaring as
Line 528: many ﬁelds as possible as final and initializing them during construction, which
Line 529: ﬂushes out any circular dependencies. Steve likes to think of this visually as creating
Line 530: a lattice of objects that acts a frame to support the test.
Line 531: Sometimes, as you’ll see later in this example, we can’t lock everything down and
Line 532: have to attach a dependency directly, but most of the time we can. Any exceptions
Line 533: will attract our attention and highlight a possible dependency loop. NUnit, on the
Line 534: other hand, reuses the same instance of the test class, so in that case we’d have
Line 535: to renew any supporting test values and objects explicitly.
Line 536: Closing the User Interface Loop
Line 537: Now we have the beginnings of our new component, we can retroﬁt it into
Line 538: the Sniper to make sure we don’t drift too far from working code. Previously,
Line 539: Main updated the Sniper user interface, so now we make it implement
Line 540: AuctionEventListener and move the functionality to the new auctionClosed()
Line 541: method.
Line 542: public class Main implements AuctionEventListener { […]
Line 543:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 544:     throws XMPPException 
Line 545:   {
Line 546:     disconnectWhenUICloses(connection);
Line 547:     Chat chat = connection.getChatManager().createChat(
Line 548:         auctionId(itemId, connection), 
Line 549: new AuctionMessageTranslator(this));
Line 550:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 551:     notToBeGCd = chat; 
Line 552:   }
Line 553:   public void auctionClosed() {
Line 554:     SwingUtilities.invokeLater(new Runnable() {
Line 555:       public void run() {
Line 556:         ui.showStatus(MainWindow.STATUS_LOST);
Line 557:       }
Line 558:     });
Line 559:   }
Line 560: }
Line 561: The structure now looks like Figure 12.2.
Line 562: 117
Line 563: The AuctionMessageTranslator
Line 564: 
Line 565: --- 페이지 143 ---
Line 566: Figure 12.2
Line 567: Introducing the AuctionMessageTranslator
Line 568: What Have We Achieved?
Line 569: In this baby step, we’ve extracted a single feature of our application into a separate
Line 570: class, which means the functionality now has a name and can be unit-tested.
Line 571: We’ve also made Main a little simpler, now that it’s no longer concerned with
Line 572: interpreting the text of messages from the auction. This is not yet a big deal but
Line 573: we will show, as the Sniper application grows, how this approach helps us keep
Line 574: code clean and ﬂexible, with clear responsibilities and relationships between its
Line 575: components.
Line 576: Unpacking a Price Message
Line 577: Introducing Message Event Types
Line 578: We’re about to introduce a second auction message type, the current price update.
Line 579: The Sniper needs to distinguish between the two, so we take another look at the
Line 580: message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
Line 581: simple—just a single line with a few name/value pairs. Here are examples for
Line 582: the formats again:
Line 583: SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line 584: SOLVersion: 1.1; Event: CLOSE;
Line 585: At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
Line 586: types, but we’re not clear enough about the behavior to justify any meaningful
Line 587: structure, so we back off the idea. We decide to start with a simplistic solution
Line 588: and adapt from there.
Line 589: The Second Test
Line 590: The introduction of a different Price event in our second test will force us to
Line 591: parse the incoming message. This test has the same structure as the ﬁrst one but
Line 592: gets a different input string and expects us to call a different method on the lis-
Line 593: tener. A Price message includes details of the last bid, which we need to unpack
Line 594: and pass to the listener, so we include them in the signature of the new method
Line 595: currentPrice(). Here’s the test:
Line 596: @Test public void
Line 597: notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Line 598: Chapter 12
Line 599: Getting Ready to Bid
Line 600: 118
Line 601: 
Line 602: --- 페이지 144 ---
Line 603:   context.checking(new Expectations() {{
Line 604: exactly(1).of(listener).currentPrice(192, 7);
Line 605:   }});
Line 606:   Message message = new Message();
Line 607:     message.setBody(
Line 608: "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
Line 609:                    );
Line 610:   translator.processMessage(UNUSED_CHAT, message);
Line 611: }
Line 612: To get through the compiler, we add a method to the listener; this takes just
Line 613: a keystroke in the IDE:1
Line 614: public interface AuctionEventListener {
Line 615:   void auctionClosed();
Line 616: void currentPrice(int price, int increment);
Line 617: }
Line 618: The test fails.
Line 619: unexpected invocation: auctionEventListener.auctionClosed()
Line 620: expectations:
Line 621:   ! expected once, never invoked: auctionEventListener.currentPrice(<192>, <7>)
Line 622: what happened before this: nothing!
Line 623: […]
Line 624:   at $Proxy6.auctionClosed()
Line 625:   at auctionsniper.AuctionMessageTranslator.processMessage()
Line 626:   at AuctionMessageTranslatorTest.translatesPriceMessagesAsAuctionPriceEvents()
Line 627: […]
Line 628:   at JUnit4ClassRunner.run(JUnit4ClassRunner.java:42)
Line 629: This time the critical phrase is:
Line 630: unexpected invocation: auctionEventListener.auctionClosed()
Line 631: which means that the code called the wrong method, auctionClosed(), during
Line 632: the test. The Mockery isn’t expecting this call so it fails immediately, showing us
Line 633: in the stack trace the line that triggered the failure (you can see the workings of
Line 634: the Mockery in the line $Proxy6.auctionClosed() which is the runtime substitute
Line 635: for a real AuctionEventListener). Here, the place where the code failed is obvious,
Line 636: so we can just ﬁx it.
Line 637: Our ﬁrst version is rough, but it passes the test.
Line 638: 1. Modern development environments, such as Eclipse and IDEA, will ﬁll in a missing
Line 639: method on request. This means that we can write the call we’d like to make and ask
Line 640: the tool to ﬁll in the declaration for us.
Line 641: 119
Line 642: Unpacking a Price Message
Line 643: 
Line 644: --- 페이지 145 ---
Line 645: public class AuctionMessageTranslator implements MessageListener {
Line 646:   private final AuctionEventListener listener;
Line 647:   public AuctionMessageTranslator(AuctionEventListener listener) {
Line 648:     this.listener = listener;
Line 649:   }
Line 650:   public void processMessage(Chat chat, Message message) {
Line 651:     HashMap<String, String> event = unpackEventFrom(message);
Line 652:     String type = event.get("Event");
Line 653:     if ("CLOSE".equals(type)) {
Line 654:       listener.auctionClosed();
Line 655:     } else if ("PRICE".equals(type)) {
Line 656:       listener.currentPrice(Integer.parseInt(event.get("CurrentPrice")), 
Line 657:                             Integer.parseInt(event.get("Increment")));
Line 658:     }
Line 659:   }
Line 660:   private HashMap<String, String> unpackEventFrom(Message message) {
Line 661:     HashMap<String, String> event = new HashMap<String, String>();  
Line 662:     for (String element : message.getBody().split(";")) {
Line 663:       String[] pair = element.split(":");
Line 664:       event.put(pair[0].trim(), pair[1].trim());
Line 665:     }
Line 666:     return event;
Line 667:   }
Line 668: }
Line 669: This implementation breaks the message body into a set of key/value pairs,
Line 670: which it interprets as an auction event so it can notify the AuctionEventListener.
Line 671: We also have to ﬁx the FakeAuctionServer to send a real Close event rather than
Line 672: the current empty message, otherwise the end-to-end tests will fail incorrectly.
Line 673: public void announceClosed() throws XMPPException {
Line 674: currentChat.sendMessage("SOLVersion: 1.1; Event: CLOSE;");
Line 675: }
Line 676: Running our end-to-end test again reminds us that we’re still working on the
Line 677: bidding feature. The test shows that the Sniper status label still displays Joining
Line 678: rather than Bidding.
Line 679: Discovering Further Work
Line 680: This code passes the unit test, but there’s something missing. It assumes that the
Line 681: message is correctly structured and has the right version. Given that the message
Line 682: will be coming from an outside system, this feels risky, so we need to add some
Line 683: error handling. We don’t want to break the ﬂow of getting features to work, so
Line 684: we add error handling to the to-do list to come back to it later (Figure 12.3).
Line 685: Chapter 12
Line 686: Getting Ready to Bid
Line 687: 120
Line 688: 
Line 689: --- 페이지 146 ---
Line 690: Figure 12.3
Line 691: Added tasks for handling errors
Line 692: We’re also concerned that the translator is not as clear as it could be about
Line 693: what it’s doing, with its parsing and the dispatching activities mixed together.
Line 694: We make a note to address this class as soon as we’ve passed the acceptance
Line 695: test, which isn’t far off.
Line 696: Finish the Job
Line 697: Most of the work in this chapter has been trying to decide what we want to say
Line 698: and how to say it: we write a high-level end-to-end test to describe what the
Line 699: Sniper should implement; we write long unit test names to tell us what a class
Line 700: does; we extract new classes to tease apart ﬁne-grained aspects of the functional-
Line 701: ity; and we write lots of little methods to keep each layer of code at a consistent
Line 702: level of abstraction. But ﬁrst, we write a rough implementation to prove that we
Line 703: know how to make the code do what’s required and then we refactor—which
Line 704: we’ll do in the next chapter.
Line 705: We cannot emphasize strongly enough that “ﬁrst-cut” code is not ﬁnished. It’s
Line 706: good enough to sort out our ideas and make sure we have everything in place,
Line 707: but it’s unlikely to express its intentions cleanly. That will make it a drag on
Line 708: productivity as it’s read repeatedly over the lifetime of the code. It’s like carpentry
Line 709: without sanding—eventually someone ends up with a nasty splinter.
Line 710: 121
Line 711: Finish the Job
Line 712: 
Line 713: --- 페이지 147 ---
Line 714: This page intentionally left blank 