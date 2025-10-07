Line 1: 
Line 2: --- 페이지 240 ---
Line 3: Chapter 19
Line 4: Handling Failure
Line 5: In which we address the reality of programming in an imperfect world,
Line 6: and add failure reporting. We add a new auction event that reports
Line 7: failure. We attach a new event listener that will turn off the Sniper if
Line 8: it fails. We also write a message to a log and write a unit test that mocks
Line 9: a class, for which we’re very sorry.
Line 10: To avoid trying your patience any further, we close our example here.
Line 11: So far, we’ve been prepared to assume that everything just works. This might be
Line 12: reasonable if the application is not supposed to last—perhaps it’s acceptable if
Line 13: it just crashes and we restart it or, as in this case, we’ve been mainly concerned
Line 14: with demonstrating and exploring the domain. Now it’s time to start being explicit
Line 15: about how we deal with failures.
Line 16: What If It Doesn’t Work?
Line 17: Our product people are concerned that Southabee’s On-Line has a reputation
Line 18: for occasionally failing and sending incorrectly structured messages, so they want
Line 19: us to show that we can cope. It turns out that the system we talk to is actually
Line 20: an aggregator for multiple auction feeds, so the failure of an individual auction
Line 21: does not imply that the whole system is unsafe. Our policy will be that when we
Line 22: receive a message that we cannot interpret, we will mark that auction as Failed
Line 23: and ignore any further updates, since it means we can no longer be sure what’s
Line 24: happening. Once an auction has failed, we make no attempt to recover.1
Line 25: In practice, reporting a message failure means that we ﬂush the price and bid
Line 26: values, and show the status as Failed for the offending item. We also record the
Line 27: event somewhere so that we can deal with it later. We could make the display
Line 28: of the failure more obvious, for example by coloring the row, but we’ll keep this
Line 29: version simple and leave any extras as an exercise for the reader.
Line 30: The end-to-end test shows that a working Sniper receives a bad message, dis-
Line 31: plays and records the failure, and then ignores further updates from this auction:
Line 32: 1. We admit that it’s unlikely that an auction site that regularly garbles its messages
Line 33: will survive for long, but it’s a simple example to work through. We also doubt that
Line 34: any serious bidder will be happy to let their bid lie hanging, not knowing whether
Line 35: they’ve bought something or lost to a rival. On the other hand, we’ve seen less plau-
Line 36: sible systems succeed in the world, propped up by an army of special handling, so
Line 37: perhaps you can let us get away with this one.
Line 38: 215
Line 39: 
Line 40: --- 페이지 241 ---
Line 41: @Test public void
Line 42: sniperReportsInvalidAuctionMessageAndStopsRespondingToEvents()
Line 43:     throws Exception 
Line 44: {
Line 45:   String brokenMessage = "a broken message";
Line 46:   auction.startSellingItem();
Line 47:   auction2.startSellingItem();
Line 48:   application.startBiddingIn(auction, auction2);
Line 49:   auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 50:   auction.reportPrice(500, 20, "other bidder");
Line 51:   auction.hasReceivedBid(520, ApplicationRunner.SNIPER_XMPP_ID);
Line 52:   auction.sendInvalidMessageContaining(brokenMessage);
Line 53:   application.showsSniperHasFailed(auction);
Line 54:   auction.reportPrice(520, 21, "other bidder");
Line 55: waitForAnotherAuctionEvent();
Line 56:   application.reportsInvalidMessage(auction, brokenMessage);
Line 57:   application.showsSniperHasFailed(auction);
Line 58: }
Line 59: private void waitForAnotherAuctionEvent() throws Exception {
Line 60:   auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 61:   auction2.reportPrice(600, 6, "other bidder");
Line 62:   application.hasShownSniperIsBidding(auction2, 600, 606);
Line 63: }
Line 64: where sendInvalidMessageContaining() sends the given invalid string via a chat
Line 65: to the Sniper, and showsSniperHasFailed() checks that the status for the item is
Line 66: Failed and that the price values have been zeroed. We park the implementation
Line 67: of reportsInvalidMessage() for the moment; we’ll come back to it later in this
Line 68: chapter.
Line 69: Testing That Something Doesn’t Happen
Line 70: You’ll have noticed the waitForAnotherAuctionEvent() method which forces an
Line 71: unrelated Sniper event and then waits for it to work through the system. Without
Line 72: this call, it would be possible for the ﬁnal showSniperHasFailed() check to pass
Line 73: incorrectly because it would pick up the previous Sniper state—before the system
Line 74: has had time to process the relevant price event. The additional event holds back
Line 75: the test just long enough to make sure that the system has caught up. See
Line 76: Chapter 27 for more on testing with asynchrony.
Line 77: To get this test to fail appropriately, we add a FAILED value to the SniperState
Line 78: enumeration, with an associated text mapping in SnipersTabelModel. The
Line 79: test fails:
Line 80: Chapter 19
Line 81: Handling Failure
Line 82: 216
Line 83: 
Line 84: --- 페이지 242 ---
Line 85: […] but... 
Line 86:   it is not table with row with cells 
Line 87:     <label with text "item-54321">, <label with text "0">, 
Line 88:     <label with text "0">, <label with text "Failed">
Line 89:    because 
Line 90: in row 0: component 1 text was "500"
Line 91:      in row 1: component 0 text was "item-65432"
Line 92: It shows that there are two rows in the table: the second is for the other auction,
Line 93: and the ﬁrst is showing that the current price is 500 when it should have been
Line 94: ﬂushed to 0. This failure is our marker for what we need to build next.
Line 95: Detecting the Failure
Line 96: The failure will actually occur in the AuctionMessageTranslator (last shown in
Line 97: Chapter 14) which will throw a runtime exception when it tries to parse the
Line 98: message. The Smack library drops exceptions thrown by MessageHandlers,
Line 99: so we have to make sure that our handler catches everything. As we write
Line 100: a unit test for a failure in the translator, we realize that we need to report a
Line 101: new type of auction event, so we add an auctionFailed() method to the
Line 102: AuctionEventListener interface.
Line 103: @Test public void
Line 104: notifiesAuctionFailedWhenBadMessageReceived() {
Line 105:   context.checking(new Expectations() {{  
Line 106:     exactly(1).of(listener).auctionFailed(); 
Line 107:   }});
Line 108:   Message message = new Message();
Line 109:   message.setBody("a bad message");
Line 110:   translator.processMessage(UNUSED_CHAT, message);
Line 111: }
Line 112: This fails with an ArrayIndexOutOfBoundsException when it tries to unpack a
Line 113: name/value pair from the string. We could be precise about which exceptions to
Line 114: catch but in practice it doesn’t really matter here: we either parse the message or
Line 115: we don’t, so to make the test pass we extract the bulk of processMessage() into
Line 116: a translate() method and wrap a try/catch block around it.
Line 117: public class AuctionMessageTranslator implements MessageListener {
Line 118:   public void processMessage(Chat chat, Message message) {
Line 119:     try {
Line 120: translate(message.getBody());
Line 121:     } catch (Exception parseException) {
Line 122:       listener.auctionFailed();
Line 123:     }
Line 124:   }
Line 125: While we’re here, there’s another failure mode we’d like to check. It’s possible
Line 126: that a message is well-formed but incomplete: it might be missing one of its ﬁelds
Line 127: 217
Line 128: Detecting the Failure
Line 129: 
Line 130: --- 페이지 243 ---
Line 131: such as the event type or current price. We write a couple of tests to conﬁrm that
Line 132: we can catch these, for example:
Line 133: @Test public void
Line 134: notifiesAuctionFailedWhenEventTypeMissing() {
Line 135:   context.checking(new Expectations() {{  
Line 136:     exactly(1).of(listener).auctionFailed(); 
Line 137:   }});
Line 138:   Message message = new Message();
Line 139:   message.setBody("SOLVersion: 1.1; CurrentPrice: 234; Increment: 5; Bidder: "
Line 140:                   + SNIPER_ID + ";");
Line 141:   translator.processMessage(UNUSED_CHAT, message);
Line 142: }
Line 143: Our ﬁx is to throw an exception whenever we try to get a value that has not
Line 144: been set, and we deﬁne MissingValueException for this purpose.
Line 145: public static class AuctionEvent { […]
Line 146:   private String get(String name) throws MissingValueException {
Line 147:     String value = values.get(name);
Line 148: if (null == value) {
Line 149:       throw new MissingValueException(name);
Line 150:     }
Line 151:     return value;
Line 152:   }
Line 153: }
Line 154: Displaying the Failure
Line 155: We added an auctionFailed() method to AuctionEventListener while unit-
Line 156: testing AuctionMessageTranslator. This triggers a compiler warning in
Line 157: AuctionSniper, so we added an empty implementation to keep going. Now
Line 158: it’s time to make it work, which turns out to be easy. We write some tests in
Line 159: AuctionSniperTest for the new state transitions, for example:
Line 160: @Test public void
Line 161: reportsFailedIfAuctionFailsWhenBidding() {
Line 162:   ignoringAuction();
Line 163:   allowingSniperBidding();
Line 164:   expectSniperToFailWhenItIs("bidding");
Line 165:   sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 
Line 166:   sniper.auctionFailed(); 
Line 167: }
Line 168: private void expectSniperToFailWhenItIs(final String state) {
Line 169:   context.checking(new Expectations() {{
Line 170:     atLeast(1).of(sniperListener).sniperStateChanged(
Line 171:         new SniperSnapshot(ITEM_ID, 00, 0, SniperState.FAILED)); 
Line 172:                                     when(sniperState.is(state));
Line 173:   }});
Line 174: }
Line 175: Chapter 19
Line 176: Handling Failure
Line 177: 218
Line 178: 
Line 179: --- 페이지 244 ---
Line 180: We’ve added a couple more helper methods: ignoringAuction() says that we
Line 181: don’t care what happens to auction, allowing events to pass through so we can
Line 182: get to the failure; and, expectSniperToFailWhenItIs() describes what a failure
Line 183: should look like, including the previous state of the Sniper.
Line 184: All we have to do is add a failed() transition to SniperSnapshot and use it
Line 185: in the new method.
Line 186: public class AuctionSniper implements AuctionEventListener {
Line 187:   public void auctionFailed() {
Line 188:     snapshot = snapshot.failed();
Line 189:     listeners.announce().sniperStateChanged(snapshot);
Line 190:   } […]
Line 191: public class SniperSnapshot {
Line 192:   public SniperSnapshot failed() {
Line 193:     return new SniperSnapshot(itemId, 0, 0, SniperState.FAILED);
Line 194:   } […]
Line 195: This displays the failure, as we can see in Figure 19.1.
Line 196: Figure 19.1
Line 197: The Sniper shows a failed auction
Line 198: The end-to-end test, however, still fails. The synchronization hook we added
Line 199: reveals that we haven’t disconnected the Sniper from receiving further events
Line 200: from the auction.
Line 201: Disconnecting the Sniper
Line 202: We turn off a Sniper by removing its AuctionMessageTranslator from its Chat’s
Line 203: set of MessageListeners. We can do this safely while processing a message because
Line 204: Chat stores its listeners in a thread-safe “copy on write” collection. One obvious
Line 205: place to do this is within processMessage() in AuctionMessageTranslator, which
Line 206: receives the Chat as an argument, but we have two doubts about this. First, as
Line 207: we pointed out in Chapter 12, constructing a real Chat is painful. Most of the
Line 208: mocking frameworks support creating a mock class, but it makes us uncomfort-
Line 209: able because then we’re deﬁning a relationship with an implementation, not a
Line 210: role—we’re being too precise about our dependencies. Second, we might be as-
Line 211: signing too many responsibilities to AuctionMessageTranslator; it would have
Line 212: to translate the message and decide what to do when it fails.
Line 213: 219
Line 214: Disconnecting the Sniper
Line 215: 
Line 216: --- 페이지 245 ---
Line 217: Our alternative approach is to attach another object to the translator that im-
Line 218: plements this disconnection policy, using the infrastructure we already have for
Line 219: notifying AuctionEventListeners.
Line 220: public final class XMPPAuction implements Auction {
Line 221:   public XMPPAuction(XMPPConnection connection, String auctionJID) {
Line 222:     AuctionMessageTranslator translator = translatorFor(connection);
Line 223:     this.chat = connection.getChatManager().createChat(auctionJID, translator);
Line 224:     addAuctionEventListener(chatDisconnectorFor(translator));
Line 225:   }
Line 226:   private AuctionMessageTranslator translatorFor(XMPPConnection connection) {
Line 227:     return new AuctionMessageTranslator(connection.getUser(), 
Line 228:                                         auctionEventListeners.announce());
Line 229:   }
Line 230: z
Line 231:   private AuctionEventListener 
Line 232: chatDisconnectorFor(final AuctionMessageTranslator translator) {
Line 233:     return new AuctionEventListener() {
Line 234:       public void auctionFailed() { 
Line 235: chat.removeMessageListener(translator);
Line 236:       }
Line 237:       public void auctionClosed(// empty method
Line 238:       public void currentPrice( // empty method
Line 239:     };
Line 240:   } […]
Line 241: The end-to-end test, as far as it goes, passes.
Line 242: The Composition Shell Game
Line 243: The issue in this design episode is not the fundamental complexity of the feature,
Line 244: which is constant, but how we divide it up. The design we chose (attaching a dis-
Line 245: connection listener) could be argued to be more complicated than its alternative
Line 246: (detaching the chat within the translator). It certainly takes more lines of code, but
Line 247: that’s not the only metric. Instead, we’re emphasizing the “single responsibility”
Line 248: principle, which means each object does just one thing well and the system behavior
Line 249: comes from how we assemble those objects.
Line 250: Sometimes this feels as if the behavior we’re looking for is always somewhere else
Line 251: (as Gertrude Stein said, “There is no there there”), which can be frustrating for
Line 252: developers not used to the style. Our experience, on the other hand, is that focused
Line 253: responsibilities make the code more maintainable because we don’t have to cut
Line 254: through unrelated functionality to get to the piece we need. See Chapter 6 for a
Line 255: longer discussion.
Line 256: Chapter 19
Line 257: Handling Failure
Line 258: 220
Line 259: 
Line 260: --- 페이지 246 ---
Line 261: Recording the Failure
Line 262: Now we want to return to the end-to-end test and the reportsInvalidMessage()
Line 263: method that we parked. Our requirement is that the Sniper application must log
Line 264: a message about these failures so that the user’s organization can recover the
Line 265: situation. This means that our test should look for a log ﬁle and check its contents.
Line 266: Filling In the Test
Line 267: We implement the missing check and ﬂush the log before each test, delegating
Line 268: the management of the log ﬁle to an AuctionLogDriver class which uses the
Line 269: Apache Commons IO library. It also cheats slightly by resetting the log manager
Line 270: (we’re not really supposed to be in the same address space), since deleting the
Line 271: log ﬁle can confuse a cached logger.
Line 272: public class ApplicationRunner { […]
Line 273: private AuctionLogDriver logDriver = new AuctionLogDriver();
Line 274:   public void reportsInvalidMessage(FakeAuctionServer auction, String message)
Line 275:     throws IOException 
Line 276:   {
Line 277: logDriver.hasEntry(containsString(message));
Line 278:   }
Line 279:   public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
Line 280:     startSniper();
Line 281:     openBiddingFor(auction, stopPrice);
Line 282:   }  
Line 283:   private startSniper() {
Line 284: logDriver.clearLog()
Line 285:     Thread thread = new Thread("Test Application") {
Line 286:       @Override public void run() { // Start the application […]
Line 287:   }
Line 288: }
Line 289: public class AuctionLogDriver {
Line 290:   public static final String LOG_FILE_NAME = "auction-sniper.log";
Line 291:   private final File logFile = new File(LOG_FILE_NAME);
Line 292:   public void hasEntry(Matcher<String> matcher) throws IOException  {
Line 293:     assertThat(FileUtils.readFileToString(logFile), matcher); 
Line 294:   }
Line 295:   public void clearLog() {
Line 296:     logFile.delete();
Line 297:     LogManager.getLogManager().reset(); 
Line 298:   }
Line 299: }
Line 300: This new check only reassures us that we’ve fed a message through the system
Line 301: and into some kind of log record—it tells us that the pieces ﬁt together. We’ll
Line 302: write a more thorough test of the contents of a log record later. The end-to-end
Line 303: test now fails because, of course, there’s no log ﬁle to read.
Line 304: 221
Line 305: Recording the Failure
Line 306: 
Line 307: --- 페이지 247 ---
Line 308: Failure Reporting in the Translator
Line 309: Once again, the ﬁrst change is in the AuctionMessageTranslator. We’d like
Line 310: the record to include the auction identiﬁer, the received message, and
Line 311: the thrown exception. The “single responsibility” principle suggests that the
Line 312: AuctionMessageTranslator should not be responsible for deciding how to report
Line 313: the event, so we invent a new collaborator to handle this task. We call it
Line 314: XMPPFailureReporter:
Line 315: public interface XMPPFailureReporter {
Line 316:   void cannotTranslateMessage(String auctionId, String failedMessage, 
Line 317:                               Exception exception);
Line 318: }
Line 319: We amend our existing failure tests, wrapping up message creation and common
Line 320: expectations in helper methods, for example:
Line 321: @Test public void
Line 322: notifiesAuctionFailedWhenBadMessageReceived() {
Line 323:   String badMessage = "a bad message";
Line 324: expectFailureWithMessage(badMessage);
Line 325:   translator.processMessage(UNUSED_CHAT, message(badMessage));
Line 326: }
Line 327: private Message message(String body) {
Line 328:   Message message = new Message();
Line 329:   message.setBody(body);
Line 330:   return message;
Line 331: }
Line 332: private void expectFailureWithMessage(final String badMessage) {
Line 333:   context.checking(new Expectations() {{  
Line 334:     oneOf(listener).auctionFailed(); 
Line 335: oneOf(failureReporter).cannotTranslateMessage(
Line 336:                              with(SNIPER_ID), with(badMessage),
Line 337:                              with(any(Exception.class)));
Line 338:   }});
Line 339: }
Line 340: The new reporter is a dependency for the translator, so we feed it in through
Line 341: the constructor and call it just before notifying any listeners. We know that
Line 342: message.getBody() will not throw an exception, it’s just a simple bean, so we
Line 343: can leave it outside the catch block.
Line 344: public class AuctionMessageTranslator implements MessageListener {
Line 345:   public void processMessage(Chat chat, Message message) {
Line 346:     String messageBody = message.getBody();
Line 347:     try {
Line 348:       translate(messageBody);
Line 349:     } catch (RuntimeException exception) {
Line 350: failureReporter.cannotTranslateMessage(sniperId, messageBody, exception);
Line 351:       listener.auctionFailed();
Line 352:     }
Line 353:   }  […]
Line 354: The unit test passes.
Line 355: Chapter 19
Line 356: Handling Failure
Line 357: 222
Line 358: 
Line 359: --- 페이지 248 ---
Line 360: Generating the Log Message
Line 361: The next stage is to implement the XMPPFailureReporter with something that
Line 362: generates a log ﬁle. This is where we actually check the format and contents of
Line 363: a log entry. We start a class LoggingXMPPFailureReporter and decide to use Java’s
Line 364: built-in logging framework. We could make the tests for this new class write and
Line 365: read from a real ﬁle. Instead, we decide that ﬁle access is sufﬁciently covered by
Line 366: the end-to-end test we’ve just set up, so we’ll run everything in memory to
Line 367: reduce the test’s dependencies. We’re conﬁdent we can take this shortcut, because
Line 368: the example is so simple; for more complex behavior we would write some
Line 369: integration tests.
Line 370: The Java logging framework has no interfaces, so we have to be more concrete
Line 371: than we’d like. Exceptionally, we decide to use a class-based mock to override
Line 372: the relevant method in Logger; in jMock we turn on class-based mocking
Line 373: with the setImposteriser() call. The AfterClass annotation tells JUnit to call
Line 374: resetLogging() after all the tests have run to ﬂush any changes we might have
Line 375: made to the logging environment.
Line 376: @RunWith(JMock.class)
Line 377: public class LoggingXMPPFailureReporterTest {
Line 378:   private final Mockery context = new Mockery() {{
Line 379: setImposteriser(ClassImposteriser.INSTANCE);
Line 380:   }};
Line 381:   final Logger logger = context.mock(Logger.class);
Line 382:   final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
Line 383: @AfterClass
Line 384:   public static void resetLogging() {
Line 385:     LogManager.getLogManager().reset();
Line 386:   }
Line 387:   @Test public void
Line 388: writesMessageTranslationFailureToLog() {
Line 389:     context.checking(new Expectations() {{
Line 390:       oneOf(logger).severe("<auction id> "
Line 391:                          + "Could not translate message \"bad message\" "
Line 392:                          + "because \"java.lang.Exception: bad\"");
Line 393:     }});
Line 394:     reporter.cannotTranslateMessage("auction id", "bad message", new Exception("bad"));
Line 395:   }
Line 396: }
Line 397: We pass this test with an implementation that just calls the logger with a string
Line 398: formatted from the inputs to cannotTranslateMessage().
Line 399: Breaking Our Own Rules?
Line 400: We already wrote that we don’t like to mock classes, and we go on about it further
Line 401: in Chapter 20. So, how come we’re doing it here?
Line 402: 223
Line 403: Recording the Failure
Line 404: 
Line 405: --- 페이지 249 ---
Line 406: What we care about in this test is the rendering of the values into a failure message
Line 407: with a severity level. The class is very limited, just a shim above the logging layer,
Line 408: so we don’t think it’s worth introducing another level of indirection to deﬁne the
Line 409: logging role. As we wrote before, we also don’t think it worth running against a real
Line 410: ﬁle since that introduces dependencies (and, even worse, asynchrony) not really
Line 411: relevant to the functionality we’re developing. We also believe that, as part of the
Line 412: Java runtime, the logging API is unlikely to change.
Line 413: So, just this once, as a special favor, setting no precedents, making no promises,
Line 414: we mock the Logger class. There are a couple more points worth making before we
Line 415: move on. First, we would not do this for a class that is internal to our code, because
Line 416: then we would be able write an interface to describe the role it’s playing. Second,
Line 417: if the LoggingXMPPFailureReporter were to grow in complexity, we would probably
Line 418: ﬁnd ourselves discovering a supporting message formatter class that could be
Line 419: tested directly.
Line 420: Closing the Loop
Line 421: Now we have the pieces in place to make the whole end-to-end test pass. We
Line 422: plug an instance of the LoggingXMPPFailureReporter into the XMPPAuctionHouse
Line 423: so that, via its XMPPAuctions, every AuctionMessageTranslator is constructed
Line 424: with the reporter. We also move the constant that deﬁnes the log ﬁle name there
Line 425: from AuctionLogDriver, and deﬁne a new XMPPAuctionException to gather up
Line 426: any failures within the package.
Line 427: public class XMPPAuctionHouse implements AuctionHouse {
Line 428:   public XMPPAuctionHouse(XMPPConnection connection) 
Line 429:     throws XMPPAuctionException 
Line 430:   {
Line 431:     this.connection = connection;
Line 432: this.failureReporter = new LoggingXMPPFailureReporter(makeLogger());
Line 433:   }
Line 434:   public Auction auctionFor(String itemId) {
Line 435:     return new XMPPAuction(connection, auctionId(itemId, connection), failureReporter);
Line 436:   } 
Line 437:   private Logger makeLogger() throws XMPPAuctionException {
Line 438:     Logger logger = Logger.getLogger(LOGGER_NAME);
Line 439:     logger.setUseParentHandlers(false);
Line 440:     logger.addHandler(simpleFileHandler());
Line 441:     return logger;
Line 442:   }
Line 443:   private FileHandler simpleFileHandler() throws XMPPAuctionException {
Line 444:     try {
Line 445:       FileHandler handler = new FileHandler(LOG_FILE_NAME);
Line 446:       handler.setFormatter(new SimpleFormatter());
Line 447:       return handler;
Line 448:     } catch (Exception e) {
Line 449:       throw new XMPPAuctionException("Could not create logger FileHandler " 
Line 450:                                    + getFullPath(LOG_FILE_NAME), e);
Line 451:     }
Line 452:   } […]
Line 453: Chapter 19
Line 454: Handling Failure
Line 455: 224
Line 456: 
Line 457: --- 페이지 250 ---
Line 458: The end-to-end test passes completely and we can cross another item off our
Line 459: list: Figure 19.2.
Line 460: Figure 19.2
Line 461: The Sniper reports failed messages from an auction
Line 462: Observations
Line 463: “Inverse Salami” Development
Line 464: We hope that by now you’re getting a sense of the rhythm of incrementally
Line 465: growing software, adding functionality in thin but coherent slices. For each new
Line 466: feature, write some tests that show what it should do, work through each of
Line 467: those tests changing just enough code to make it pass, restructure the code as
Line 468: needed either to open up space for new functionality or to reveal new
Line 469: concepts—then ship it. We discuss how this ﬁts into the larger development picture
Line 470: in Chapter 5. In static languages, such as Java and C#, we can often use the
Line 471: compiler to help us navigate the chain of implementation dependencies: change
Line 472: the code to accept the new triggering event, see what breaks, ﬁx that breakage,
Line 473: see what that change breaks in turn, and repeat the process until the
Line 474: functionality works.
Line 475: The skill is in learning how to divide requirements up into incremental slices,
Line 476: always having something working, always adding just one more feature. The
Line 477: process should feel relentless—it just keeps moving. To make this work, we have
Line 478: to understand how to change the code incrementally and, critically, keep the
Line 479: code well structured so that we can take it wherever we need to go (and we
Line 480: don’t know where that is yet). This is why the refactoring part of a test-driven
Line 481: 225
Line 482: Observations
Line 483: 
Line 484: --- 페이지 251 ---
Line 485: development cycle is so critical—we always get into trouble when we don’t keep
Line 486: up that side of the bargain.
Line 487: Small Methods to Express Intent
Line 488: We have a habit of writing helper methods to wrap up small amounts of code—for
Line 489: two reasons. First, this reduces the amount of syntactic noise in the calling code
Line 490: that languages like Java force upon us. For example, when we disconnect
Line 491: the Sniper, the translatorFor() method means we don’t have to type
Line 492: "AuctionMessageTranslator" twice in the same line. Second, this gives a mean-
Line 493: ingful name to a structure that would not otherwise be obvious. For example,
Line 494: chatDisconnectorFor() describes what its anonymous class does and is less
Line 495: intrusive than deﬁning a named inner class.
Line 496: Our aim is to do what we can to make each level of code as readable and self-
Line 497: explanatory as possible, repeating the process all the way down until we actually
Line 498: have to use a Java construct.
Line 499: Logging Is Also a Feature
Line 500: We deﬁned XMPPFailureReporter to package up failure reporting for the
Line 501: AuctionMessageTranslator. Many teams would regard this as overdesign and
Line 502: just write the log message in place. We think this would weaken the design by
Line 503: mixing levels (message translation and logging) in the same code.
Line 504: We’ve seen many systems where logging has been added ad hoc by developers
Line 505: wherever they ﬁnd a need. However, production logging is an external interface
Line 506: that should be driven by the requirements of those who will depend on it, not
Line 507: by the structure of the current implementation. We ﬁnd that when we take the
Line 508: trouble to describe runtime reporting in the caller’s terms, as we did with
Line 509: the XMPPFailureReporter, we end up with more useful logs. We also ﬁnd that
Line 510: we end up with the logging infrastructure clearly isolated, rather than scattered
Line 511: throughout the code, which makes it easier to work with.
Line 512: This topic is such a bugbear (for Steve at least) that we devote a whole section
Line 513: to it in Chapter 20.
Line 514: Chapter 19
Line 515: Handling Failure
Line 516: 226