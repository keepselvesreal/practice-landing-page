Line 1: 
Line 2: --- 페이지 114 ---
Line 3: Chapter 11
Line 4: Passing the First Test
Line 5: In which we write test infrastructure to drive our non-existent applica-
Line 6: tion, so that we can make the ﬁrst test fail. We repeatedly fail the test
Line 7: and ﬁx symptoms, until we have a minimal working application that
Line 8: passes the ﬁrst test. We step through this very slowly to show how the
Line 9: process works.
Line 10: Building the Test Rig
Line 11: At the start of every test run, our test script starts up the Openﬁre server, creates
Line 12: accounts for the Sniper and the auction, and then runs the tests. Each test will
Line 13: start instances of the application and the fake auction, and then test their com-
Line 14: munication through the server. At ﬁrst, we’ll run everything on the same host.
Line 15: Later, as the infrastructure stabilizes, we can consider running different compo-
Line 16: nents on different machines, which will be a better match to the real deployment.
Line 17: This leaves us with two components to write for the test infrastructure:
Line 18: ApplicationRunner and FakeAuctionServer.
Line 19: Setting Up the Openﬁre Server
Line 20: At the time of writing, we were using version 3.6 of Openﬁre. For these end-to-
Line 21: end tests, we set up our local server with three user accounts and passwords:
Line 22: sniper
Line 23: sniper
Line 24: auction-item-54321
Line 25: auction
Line 26: auction-item-65432
Line 27: auction
Line 28: For desktop development, we usually started the server by hand and left it running.
Line 29: We set it up to not store ofﬂine messages, which meant there was no persistent
Line 30: state. In the System Manager, we edited the “System Name” property to be
Line 31: localhost, so the tests would run consistently. Finally, we set the resource policy
Line 32: to “Never kick,” which will not allow a new resource to log in if there’s a conﬂict.
Line 33: 89
Line 34: 
Line 35: --- 페이지 115 ---
Line 36: The Application Runner
Line 37: An ApplicationRunner is an object that wraps up all management and commu-
Line 38: nicating with the Swing application we’re building. It runs the application as if
Line 39: from the command line, obtaining and holding a reference to its main window
Line 40: for querying the state of the GUI and for shutting down the application at the
Line 41: end of the test.
Line 42: We don’t have to do much here, because we can rely on WindowLicker to do
Line 43: the hard work: ﬁnd and control Swing GUI components, synchronize with
Line 44: Swing’s threads and event queue, and wrap that all up behind a simple API.1
Line 45: WindowLicker has the concept of a ComponentDriver: an object that can manip-
Line 46: ulate a feature in a Swing user interface. If a ComponentDriver can’t ﬁnd the
Line 47: Swing component it refers to, it will time out with an error. For this test, we’re
Line 48: looking for a label component that shows a given string; if our application doesn’t
Line 49: produce this label, we’ll get an exception. Here’s the implementation (with the
Line 50: constants left out for clarity) and some explanation:
Line 51: public class ApplicationRunner {
Line 52:   public static final String SNIPER_ID = "sniper";
Line 53:   public static final String SNIPER_PASSWORD = "sniper";
Line 54:   private AuctionSniperDriver driver;
Line 55:   public void startBiddingIn(final FakeAuctionServer auction) {
Line 56:     Thread thread = new Thread("Test Application") {
Line 57:       @Override public void run() { 1
Line 58:         try {
Line 59:           Main.main(XMPP_HOSTNAME, SNIPER_ID, SNIPER_PASSWORD, auction.getItemId()); 2
Line 60:         } catch (Exception e) {                                                    
Line 61:           e.printStackTrace(); 3
Line 62:         }
Line 63:       }
Line 64:     };
Line 65:     thread.setDaemon(true);
Line 66:     thread.start();
Line 67:     driver = new AuctionSniperDriver(1000); 4
Line 68:     driver.showsSniperStatus(STATUS_JOINING); 5
Line 69:   }
Line 70:   public void showsSniperHasLostAuction() {
Line 71:     driver.showsSniperStatus(STATUS_LOST);  6
Line 72:   }
Line 73:   public void stop() {
Line 74:     if (driver != null) {
Line 75:       driver.dispose(); 7
Line 76:     }
Line 77:   }
Line 78: }
Line 79: 1. We’re assuming that you know how Swing works; there are many other books that
Line 80: do a good job of describing it. The essential point here is that it’s an event-driven
Line 81: framework that creates its own internal threads to dispatch events, so we can’t be
Line 82: precise about when things will happen.
Line 83: Chapter 11
Line 84: Passing the First Test
Line 85: 90
Line 86: 
Line 87: --- 페이지 116 ---
Line 88: 1
Line 89: We call the application through its main() function to make sure we’ve as-
Line 90: sembled the pieces correctly. We’re following the convention that the entry
Line 91: point to the application is a Main class in the top-level package. WindowLicker
Line 92: can control Swing components if they’re in the same JVM, so we start the
Line 93: Sniper in a new thread. Ideally, the test would start the Sniper in a new pro-
Line 94: cess, but that would be much harder to test; we think this is a reasonable
Line 95: compromise.
Line 96: 2
Line 97: To keep things simple at this stage, we’ll assume that we’re only bidding for
Line 98: one item and pass the identiﬁer to main().
Line 99: 3
Line 100: If main() throws an exception, we just print it out. Whatever test we’re
Line 101: running will fail and we can look for the stack trace in the output. Later,
Line 102: we’ll handle exceptions properly.
Line 103: 4
Line 104: We turn down the timeout period for ﬁnding frames and components. The
Line 105: default values are longer than we need for a simple application like this one
Line 106: and will slow down the tests when they fail. We use one second, which is
Line 107: enough to smooth over minor runtime delays.
Line 108: 5
Line 109: We wait for the status to change to Joining so we know that the application
Line 110: has attempted to connect. This assertion says that somewhere in the user
Line 111: interface there’s a label that describes the Sniper’s state.
Line 112: 6
Line 113: When the Sniper loses the auction, we expect it to show a Lost status. If this
Line 114: doesn’t happen, the driver will throw an exception.
Line 115: 7
Line 116: After the test, we tell the driver to dispose of the window to make sure it
Line 117: won’t be picked up in another test before being garbage-collected.
Line 118: The AuctionSniperDriver is simply an extension of a WindowLicker
Line 119: JFrameDriver specialized for our tests:
Line 120: public class AuctionSniperDriver extends JFrameDriver {
Line 121:   public AuctionSniperDriver(int timeoutMillis) {
Line 122:     super(new GesturePerformer(), 
Line 123:           JFrameDriver.topLevelFrame(
Line 124:             named(Main.MAIN_WINDOW_NAME), 
Line 125:             showingOnScreen()),
Line 126:             new AWTEventQueueProber(timeoutMillis, 100));
Line 127:   }
Line 128:   public void showsSniperStatus(String statusText) {
Line 129:     new JLabelDriver(
Line 130:       this, named(Main.SNIPER_STATUS_NAME)).hasText(equalTo(statusText));
Line 131:   }
Line 132: }
Line 133: 91
Line 134: Building the Test Rig
Line 135: 
Line 136: --- 페이지 117 ---
Line 137: On construction, it attempts to ﬁnd a visible top-level window for the Auction
Line 138: Sniper within the given timeout. The method showsSniperStatus() looks for the
Line 139: relevant label in the user interface and conﬁrms that it shows the given status.
Line 140: If the driver cannot ﬁnd a feature it expects, it will throw an exception and fail
Line 141: the test.
Line 142: The Fake Auction
Line 143: A FakeAuctionServer is a substitute server that allows the test to check how the
Line 144: Auction Sniper interacts with an auction using XMPP messages. It has three re-
Line 145: sponsibilities: it must connect to the XMPP broker and accept a request to join
Line 146: the chat from the Sniper; it must receive chat messages from the Sniper or fail if
Line 147: no message arrives within some timeout; and, it must allow the test to send
Line 148: messages back to the Sniper as speciﬁed by Southabee’s On-Line.
Line 149: Smack (the XMPP client library) is event-driven, so the fake auction has to
Line 150: register listener objects for it to call back. There are two levels of events: events
Line 151: about a chat, such as people joining, and events within a chat, such as messages
Line 152: being received. We need to listen for both.
Line 153: We’ll start by implementing the startSellingItem() method. First, it connects
Line 154: to the XMPP broker, using the item identiﬁer to construct the login name; then
Line 155: it registers a ChatManagerListener. Smack will call this listener with a Chat object
Line 156: that represents the session when a Sniper connects in. The fake auction holds on
Line 157: to the chat so it can exchange messages with the Sniper.
Line 158: Figure 11.1
Line 159: Smack objects and callbacks
Line 160: Chapter 11
Line 161: Passing the First Test
Line 162: 92
Line 163: 
Line 164: --- 페이지 118 ---
Line 165: So far, we have:
Line 166: public class FakeAuctionServer {
Line 167:   public static final String ITEM_ID_AS_LOGIN = "auction-%s"; 
Line 168:   public static final String AUCTION_RESOURCE = "Auction";
Line 169:   public static final String XMPP_HOSTNAME = "localhost";
Line 170:   private static final String AUCTION_PASSWORD = "auction";
Line 171:   private final String itemId;
Line 172:   private final XMPPConnection connection;
Line 173:   private Chat currentChat;
Line 174:   public FakeAuctionServer(String itemId) {
Line 175:     this.itemId = itemId;
Line 176:     this.connection = new XMPPConnection(XMPP_HOSTNAME);
Line 177:   }
Line 178:   public void startSellingItem() throws XMPPException {
Line 179:     connection.connect(); 
Line 180:     connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
Line 181:                      AUCTION_PASSWORD, AUCTION_RESOURCE);
Line 182:     connection.getChatManager().addChatListener(
Line 183:       new ChatManagerListener() {
Line 184:         public void chatCreated(Chat chat, boolean createdLocally) {
Line 185:           currentChat = chat;
Line 186:         }
Line 187:       });
Line 188:   }
Line 189:   public String getItemId() {
Line 190:     return itemId;
Line 191:   }
Line 192: }
Line 193: A Minimal Fake Implementation
Line 194: We want to emphasize again that this fake is a minimal implementation just to
Line 195: support testing. For example, we use a single instance variable to hold the chat
Line 196: object. A real auction server would manage multiple chats for all the bidders—but
Line 197: this is a fake; its only purpose is to support the test, so it only needs one chat.
Line 198: Next, we have to add a MessageListener to the chat to accept messages from
Line 199: the Sniper. This means that we need to coordinate between the thread that
Line 200: runs the test and the Smack thread that feeds messages to the listener—the test
Line 201: has to wait for messages to arrive and time out if they don’t—so we’ll use a
Line 202: single-element BlockingQueue from the java.util.concurrent package. Just as
Line 203: we only have one chat in the test, we expect to process only one message at a
Line 204: time. To make our intentions clearer, we wrap the queue in a helper class
Line 205: SingleMessageListener. Here’s the rest of FakeAuctionServer:
Line 206: 93
Line 207: Building the Test Rig
Line 208: 
Line 209: --- 페이지 119 ---
Line 210: public class FakeAuctionServer {
Line 211: private final SingleMessageListener messageListener = new SingleMessageListener();
Line 212:   public void startSellingItem() throws XMPPException {
Line 213:     connection.connect(); 
Line 214:     connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
Line 215:                      AUCTION_PASSWORD, AUCTION_RESOURCE);
Line 216:     connection.getChatManager().addChatListener(
Line 217:       new ChatManagerListener() {
Line 218:         public void chatCreated(Chat chat, boolean createdLocally) {
Line 219:           currentChat = chat;
Line 220: chat.addMessageListener(messageListener);
Line 221:         }
Line 222:       });
Line 223:   }
Line 224:   public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
Line 225:     messageListener.receivesAMessage(); 1
Line 226:   }
Line 227:   public void announceClosed() throws XMPPException {
Line 228:     currentChat.sendMessage(new Message()); 2
Line 229:   }
Line 230:   public void stop() {
Line 231:     connection.disconnect(); 3
Line 232:   }
Line 233: }
Line 234: public class SingleMessageListener implements MessageListener {
Line 235:   private final ArrayBlockingQueue<Message> messages = 
Line 236:                               new ArrayBlockingQueue<Message>(1);
Line 237:   public void processMessage(Chat chat, Message message) {
Line 238:     messages.add(message);
Line 239:   }
Line 240:   public void receivesAMessage() throws InterruptedException {
Line 241:     assertThat("Message", messages.poll(5, SECONDS), is(notNullValue())); 4
Line 242:   }
Line 243: }
Line 244: 1
Line 245: The test needs to know when a Join message has arrived. We just check
Line 246: whether any message has arrived, since the Sniper will only be sending Join
Line 247: messages to start with; we’ll ﬁll in more detail as we grow the application.
Line 248: This implementation will fail if no message is received within 5 seconds.
Line 249: 2
Line 250: The test needs to be able to simulate the auction announcing when it closes,
Line 251: which is why we held onto the currentChat when it opened. As with the
Line 252: Join request, the fake auction just sends an empty message, since this is
Line 253: the only event we support so far.
Line 254: 3
Line 255: stop() closes the connection.
Line 256: Chapter 11
Line 257: Passing the First Test
Line 258: 94
Line 259: 
Line 260: --- 페이지 120 ---
Line 261: 4
Line 262: The clause is(notNullValue()) uses the Hamcrest matcher syntax. We de-
Line 263: scribe Matchers in “Methods” (page 339); for now, it’s enough to know that
Line 264: this checks that the Listener has received a message within the timeout period.
Line 265: The Message Broker
Line 266: There’s one more component to mention which doesn’t involve any coding—the
Line 267: installation of an XMPP message broker. We set up an instance of Openﬁre on
Line 268: our local host. The Sniper and fake auction in our end-to-end tests, even though
Line 269: they’re running in the same process, will communicate through this server. We
Line 270: also set up logins to match the small number of item identiﬁers that we’ll be using
Line 271: in our tests.
Line 272: A Working Compromise
Line 273: As we wrote before, we are cheating a little at this stage to keep development
Line 274: moving. We want all the developers to have their own environments so they don’t
Line 275: interfere with each other when running their tests. For example, we’ve seen teams
Line 276: make their lives very complicated because they didn’t want to create a database
Line 277: instance for each developer. In a professional organization, we would also expect
Line 278: to see at least one test rig that represents the production environment, including
Line 279: the distribution of processing across a network and a build cycle that uses it to
Line 280: make sure the system works.
Line 281: Failing and Passing the Test
Line 282: We have enough infrastructure in place to run the test and watch it fail. For the
Line 283: rest of this chapter we’ll add functionality, a tiny slice at a time, until eventually
Line 284: we make the test pass. When we ﬁrst started using this technique, it felt too fussy:
Line 285: “Just write the code, we know what to do!” Over time, we realized that it didn’t
Line 286: take any longer and that our progress was much more predictable. Focusing on
Line 287: just one aspect at a time helps us to make sure we understand it; as a rule, when
Line 288: we get something working, it stays working. Where there’s no need to discuss
Line 289: the solution, many of these steps take hardly any time at all—they take longer
Line 290: to explain than to implement.
Line 291: We start by writing a build script for ant. We’ll skip over the details of its
Line 292: content, since it’s standard practice these days, but the important point is that
Line 293: we always have a single command that reliably compiles, builds, deploys, and
Line 294: tests the application, and that we run it repeatedly. We only start coding once
Line 295: we have an automated build and test working.
Line 296: At this stage, we’ll describe each step, discussing each test failure in turn. Later
Line 297: we’ll speed up the pace.
Line 298: 95
Line 299: Failing and Passing the Test
Line 300: 
Line 301: --- 페이지 121 ---
Line 302: First User Interface
Line 303: Test Failure
Line 304: The test can’t ﬁnd a user interface component with the name "Auction Sniper
Line 305: Main".
Line 306: java.lang.AssertionError: 
Line 307: Tried to look for...
Line 308:     exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 309:     in all top level windows
Line 310: but...
Line 311:     all top level windows
Line 312: contained 0 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 313: […]
Line 314:   at auctionsniper.ApplicationRunner.stop()
Line 315:   at auctionsniper.AuctionSniperEndToEndTest.stopApplication()
Line 316: […]
Line 317: WindowLicker is verbose in its error reporting, trying to make failures easy
Line 318: to understand. In this case, we couldn’t even ﬁnd the top-level frame so JUnit
Line 319: failed before even starting the test. The stack trace comes from the @After method
Line 320: that stops the application.
Line 321: Implementation
Line 322: We need a top-level window for our application. We write a MainWindow class in
Line 323: the auctionsniper.ui package that extends Swing’s JFrame, and call it from
Line 324: main(). All it will do is create a window with the right name.
Line 325: public class Main {
Line 326:   private MainWindow ui;
Line 327:   public Main() throws Exception {
Line 328: startUserInterface()
Line 329:   }
Line 330:   public static void main(String... args) throws Exception {
Line 331:     Main main = new Main();
Line 332:   }
Line 333:   private void startUserInterface() throws Exception {
Line 334:     SwingUtilities.invokeAndWait(new Runnable() {
Line 335:       public void run() {
Line 336:         ui = new MainWindow();
Line 337:       }
Line 338:     });
Line 339:   }
Line 340: }
Line 341: Chapter 11
Line 342: Passing the First Test
Line 343: 96
Line 344: 
Line 345: --- 페이지 122 ---
Line 346: public class MainWindow extends JFrame {
Line 347:   public MainWindow() {
Line 348:     super("Auction Sniper");
Line 349:     setName(MAIN_WINDOW_NAME);
Line 350:     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line 351:     setVisible(true);
Line 352:   }
Line 353: }
Line 354: Unfortunately, this is a little messy because Swing requires us to create the
Line 355: user interface on its event dispatch thread. We’ve further complicated the imple-
Line 356: mentation so we can hang on to the main window object in our code. It’s not
Line 357: strictly necessary here but we thought we’d get it over with.
Line 358: Notes
Line 359: The user interface in Figure 11.2 really is minimal. It does not look like much
Line 360: but it conﬁrms that we can start up an application window and connect to it.
Line 361: Our test still fails, but we’ve moved on a step. Now we know that our harness
Line 362: is working, which is one less thing to worry about as we move on to more
Line 363: interesting functionality.
Line 364: Figure 11.2
Line 365: Just a top-level window
Line 366: Showing the Sniper State
Line 367: Test Failure
Line 368: The test ﬁnds a top-level window, but no display of the current state of the Sniper.
Line 369: To start with, the Sniper should show Joining while waiting for the auction to
Line 370: respond.
Line 371: java.lang.AssertionError: 
Line 372: Tried to look for...
Line 373:     exactly 1 JLabel (with name "sniper status")
Line 374:     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 375:     in all top level windows
Line 376: and check that its label text is "Joining"
Line 377: but...
Line 378:     all top level windows
Line 379:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 380: contained 0 JLabel (with name "sniper status")
Line 381:   at com.objogate.wl.AWTEventQueueProber.check()
Line 382: […]
Line 383:   at AuctionSniperDriver.showsSniperStatus()
Line 384:   at ApplicationRunner.startBiddingIn()
Line 385:   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line 386: […]
Line 387: 97
Line 388: Failing and Passing the Test
Line 389: 
Line 390: --- 페이지 123 ---
Line 391: Implementation
Line 392: We add a label representing the Sniper’s state to MainWindow.
Line 393: public class MainWindow extends JFrame {
Line 394:   public static final String SNIPER_STATUS_NAME = "sniper status";
Line 395:   private final JLabel sniperStatus = createLabel(STATUS_JOINING);
Line 396:   public MainWindow() {
Line 397:     super("Auction Sniper");
Line 398:     setName(MAIN_WINDOW_NAME);
Line 399: add(sniperStatus);
Line 400:     pack();
Line 401:     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line 402:     setVisible(true);
Line 403:   }
Line 404:   private static JLabel createLabel(String initialText) {
Line 405:     JLabel result = new JLabel(initialText);
Line 406:     result.setName(SNIPER_STATUS_NAME);
Line 407:     result.setBorder(new LineBorder(Color.BLACK));
Line 408:     return result;
Line 409:   }
Line 410: }
Line 411: Notes
Line 412: Another minimal change, but now we can show some content in our application,
Line 413: as in Figure 11.3.
Line 414: Figure 11.3
Line 415: Showing Joining status
Line 416: Connecting to the Auction
Line 417: Test Failure
Line 418: Our user interface is working, but the auction does not receive a Join request
Line 419: from the Sniper.
Line 420: java.lang.AssertionError: 
Line 421: Expected: is not null
Line 422: got: null
Line 423:   at org.junit.Assert.assertThat()
Line 424:   at SingleMessageListener.receivesAMessage()
Line 425:   at FakeAuctionServer.hasReceivedJoinRequestFromSniper()
Line 426:   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line 427: […]
Line 428: Chapter 11
Line 429: Passing the First Test
Line 430: 98
Line 431: 
Line 432: --- 페이지 124 ---
Line 433: This failure message is a bit cryptic, but the names in the stack trace tell us
Line 434: what’s wrong.
Line 435: Implementation
Line 436: We write a simplistic implementation to get us past this failure. It connects to
Line 437: the chat in Main and sends an empty message. We create a null MessageListener
Line 438: to allow us to create a Chat for sending the empty initial message, since we don’t
Line 439: yet care about receiving messages.
Line 440: public class Main {
Line 441:   private static final int ARG_HOSTNAME = 0;
Line 442:   private static final int ARG_USERNAME = 1;
Line 443:   private static final int ARG_PASSWORD = 2;
Line 444:   private static final int ARG_ITEM_ID  = 3;
Line 445:   public static final String AUCTION_RESOURCE = "Auction";
Line 446:   public static final String ITEM_ID_AS_LOGIN = "auction-%s";
Line 447:   public static final String AUCTION_ID_FORMAT = 
Line 448:                                ITEM_ID_AS_LOGIN + "@%s/" + AUCTION_RESOURCE;
Line 449: […]
Line 450:   public static void main(String... args) throws Exception {
Line 451:     Main main = new Main();
Line 452:     XMPPConnection connection = connectTo(args[ARG_HOSTNAME], 
Line 453:                                           args[ARG_USERNAME], 
Line 454:                                           args[ARG_PASSWORD]);
Line 455:     Chat chat = connection.getChatManager().createChat(
Line 456:         auctionId(args[ARG_ITEM_ID], connection), 
Line 457:         new MessageListener() {
Line 458:           public void processMessage(Chat aChat, Message message) {
Line 459: // nothing yet
Line 460:           }
Line 461:         });
Line 462:     chat.sendMessage(new Message());
Line 463:   }
Line 464:   private static XMPPConnection 
Line 465: connectTo(String hostname, String username, String password) 
Line 466:       throws XMPPException
Line 467:   {
Line 468:     XMPPConnection connection = new XMPPConnection(hostname);
Line 469:     connection.connect();
Line 470:     connection.login(username, password, AUCTION_RESOURCE);
Line 471:     return connection;
Line 472:   }
Line 473:   private static String auctionId(String itemId, XMPPConnection connection) {
Line 474:     return String.format(AUCTION_ID_FORMAT, itemId, 
Line 475:                          connection.getServiceName()); 
Line 476:   }
Line 477: […]
Line 478: }
Line 479: 99
Line 480: Failing and Passing the Test
Line 481: 
Line 482: --- 페이지 125 ---
Line 483: Notes
Line 484: This shows that we can establish a connection from the Sniper to the auction,
Line 485: which means we had to sort out details such as interpreting the item and user
Line 486: credentials from the command-line arguments and using the Smack library. We’re
Line 487: leaving the message contents until later because we only have one message type,
Line 488: so sending an empty value is enough to prove the connection.
Line 489: This implementation may seem gratuitously naive—after all, we should be able
Line 490: to design a structure for something as simple as this, but we’ve often found it
Line 491: worth writing a small amount of ugly code and seeing how it falls out. It helps
Line 492: us to test our ideas before we’ve gone too far, and sometimes the results can be
Line 493: surprising. The important point is to make sure we don’t leave it ugly.
Line 494: We make a point of keeping the connection code out of the Swing
Line 495: invokeAndWait() call that creates the MainWindow, because we want the user
Line 496: interface to settle before we try anything more complicated.
Line 497: Receiving a Response from the Auction
Line 498: Test Failure
Line 499: With a connection established, the Sniper should receive and display the Lost
Line 500: response from the auction. It doesn’t yet:
Line 501: java.lang.AssertionError: 
Line 502: Tried to look for...
Line 503:     exactly 1 JLabel (with name "sniper status")
Line 504:     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 505:     in all top level windows
Line 506: and check that its label text is "Lost"
Line 507: but...
Line 508:     all top level windows
Line 509:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 510:     contained 1 JLabel (with name "sniper status")
Line 511: label text was "Joining"
Line 512: […]
Line 513:   at AuctionSniperDriver.showsSniperStatus()
Line 514:   at ApplicationRunner.showsSniperHasLostAuction()
Line 515:   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line 516: […]
Line 517: Implementation
Line 518: We need to attach the user interface to the chat so it can receive the response
Line 519: from the auction, so we create a connection and pass it to Main to create the Chat
Line 520: object. joinAuction() creates a MessageListener that sets the status label, using
Line 521: an invokeLater() call to avoid blocking the Smack library. As with the Join
Line 522: message, we don’t bother with the contents of the incoming message since there’s
Line 523: only one possible response the auction can send at the moment. While we’re at
Line 524: it, we rename connect() to connection() to make the code read better.
Line 525: Chapter 11
Line 526: Passing the First Test
Line 527: 100
Line 528: 
Line 529: --- 페이지 126 ---
Line 530: public class Main {
Line 531:   @SuppressWarnings("unused") private Chat notToBeGCd;
Line 532: […]
Line 533:   public static void main(String... args) throws Exception {
Line 534:     Main main = new Main();
Line 535: main.joinAuction(
Line 536:       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
Line 537:       args[ARG_ITEM_ID]);
Line 538:   }
Line 539:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 540:     throws XMPPException
Line 541:   {
Line 542:     final Chat chat = connection.getChatManager().createChat(
Line 543:         auctionId(itemId, connection), 
Line 544:         new MessageListener() {
Line 545:           public void processMessage(Chat aChat, Message message) {
Line 546: SwingUtilities.invokeLater(new Runnable() {
Line 547:               public void run() {
Line 548:                 ui.showStatus(MainWindow.STATUS_LOST);
Line 549:               }
Line 550:             });
Line 551:           }
Line 552:         });
Line 553:     this.notToBeGCd = chat;
Line 554:     chat.sendMessage(new Message());
Line 555:   }
Line 556: Why the Chat Field?
Line 557: You’ll notice that we’ve assigned the chat that we create to the ﬁeld notToBeGCd
Line 558: in Main. This is to make sure that the chat is not garbage-collected by the Java
Line 559: runtime. There’s a note at the top of the ChatManager documentation that says:
Line 560: The chat manager keeps track of references to all current chats. It will not
Line 561: hold any references in memory on its own so it is necessary to keep a
Line 562: reference to the chat object itself.
Line 563: If the chat is garbage-collected, the Smack runtime will hand the message to a
Line 564: new Chat which it will create for the purpose. In an interactive application, we would
Line 565: listen for and show these new chats, but our needs are different, so we add this
Line 566: quirk to stop it from happening.
Line 567: We made this reference clumsy on purpose—to highlight in the code why we’re
Line 568: doing it.We also know that we’re likely to come up with a better solution in a while.
Line 569: We implement the display method in the user interface and, ﬁnally, the whole
Line 570: test passes.
Line 571: 101
Line 572: Failing and Passing the Test
Line 573: 
Line 574: --- 페이지 127 ---
Line 575: public class MainWindow extends JFrame {
Line 576: […]
Line 577:   public void showStatus(String status) {
Line 578: sniperStatus.setText(status);
Line 579:   }
Line 580: }
Line 581: Notes
Line 582: Figure 11.4 is visible conﬁrmation that the code works.
Line 583: Figure 11.4
Line 584: Showing Lost status
Line 585: It may not look like much, but it conﬁrms that a Sniper can establish a
Line 586: connection with an auction, accept a response, and display the result.
Line 587: The Necessary Minimum
Line 588: In one of his school reports, Steve was noted as “a ﬁne judge of the necessary
Line 589: minimum.” It seems he’s found his calling in writing software since this is a
Line 590: critical skill during iteration zero.
Line 591: What we hope you’ve seen in this chapter is the degree of focus that’s required
Line 592: to put together your ﬁrst walking skeleton. The point is to design and validate
Line 593: the initial structure of the end-to-end system—where end-to-end includes deploy-
Line 594: ment to a working environment—to prove that our choices of packages, libraries,
Line 595: and tooling will actually work. A sense of urgency will help the team to strip the
Line 596: functionality down to the absolute minimum sufﬁcient to test their assumptions.
Line 597: That’s why we didn’t put any content in our Sniper messages; it would be a di-
Line 598: version from making sure that the communication and event handling work. We
Line 599: didn’t sweat too hard over the detailed code design, partly because there isn’t
Line 600: much but mainly because we’re just getting the pieces in place; that effort will
Line 601: come soon enough.
Line 602: Of course, all you see in this chapter are edited highlights. We’ve left out many
Line 603: diversions and discussions as we ﬁgured out which pieces to use and how to make
Line 604: them work, trawling through product documentation and discussion lists. We’ve
Line 605: also left out some of our discussions about what this project is for. Iteration zero
Line 606: usually brings up project chartering issues as the team looks for criteria to guide
Line 607: its decisions, so the project’s sponsors should expect to ﬁeld some deep questions
Line 608: about its purpose.
Line 609: Chapter 11
Line 610: Passing the First Test
Line 611: 102
Line 612: 
Line 613: --- 페이지 128 ---
Line 614: We have something visible we can present as a sign of progress, so we can
Line 615: cross off the ﬁrst item on our list, as in Figure 11.5.
Line 616: Figure 11.5
Line 617: First item done
Line 618: The next step is to start building out real functionality.
Line 619: 103
Line 620: The Necessary Minimum
Line 621: 
Line 622: --- 페이지 129 ---
Line 623: This page intentionally left blank 