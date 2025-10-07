Line 1: 
Line 2: --- 페이지 216 ---
Line 3: Chapter 17
Line 4: Teasing Apart Main
Line 5: In which we slice up our application, shufﬂing behavior around to
Line 6: isolate the XMPP and user interface code from the sniping logic. We
Line 7: achieve this incrementally, changing one concept at a time without
Line 8: breaking the whole application. We ﬁnally put a stake through the
Line 9: heart of notToBeGCd.
Line 10: Finding a Role
Line 11: We’ve convinced ourselves that we need to do some surgery on Main, but what
Line 12: do we want our improved Main to do?
Line 13: For programs that are more than trivial, we like to think of our top-level class
Line 14: as a “matchmaker,” ﬁnding components and introducing them to each other.
Line 15: Once that job is done it drops into the background and waits for the application to
Line 16: ﬁnish. On a larger scale, this what the current generation of application containers
Line 17: do, except that the relationships are often encoded in XML.
Line 18: In its current form, Main acts as a matchmaker but it’s also implementing some
Line 19: of the components, which means it has too many responsibilities. One clue is to
Line 20: look at its imports:
Line 21: import java.awt.event.WindowAdapter;
Line 22: import java.awt.event.WindowEvent;
Line 23: import java.util.ArrayList;
Line 24: import javax.swing.SwingUtilities;
Line 25: import org.jivesoftware.smack.Chat;
Line 26: import org.jivesoftware.smack.XMPPConnection;
Line 27: import org.jivesoftware.smack.XMPPException;
Line 28: import auctionsniper.ui.MainWindow;
Line 29: import auctionsniper.ui.SnipersTableModel;
Line 30: import auctionsniper.AuctionMessageTranslator;
Line 31: import auctionsniper.XMPPAuction;
Line 32: We’re importing code from three unrelated packages, plus the auctionsniper
Line 33: package itself. In fact, we have a package loop in that the top-level and
Line 34: UI packages depend on each other. Java, unlike some other languages, tolerates
Line 35: package loops, but they’re not something we should be pleased with.
Line 36: 191
Line 37: 
Line 38: --- 페이지 217 ---
Line 39: We think we should extract some of this behavior from Main, and the XMPP
Line 40: features look like a good ﬁrst candidate. The use of the Smack should be an
Line 41: implementation detail that is irrelevant to the rest of the application.
Line 42: Extracting the Chat
Line 43: Isolating the Chat
Line 44: Most 
Line 45: of 
Line 46: the 
Line 47: action 
Line 48: happens 
Line 49: in 
Line 50: the 
Line 51: implementation 
Line 52: of
Line 53: UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
Line 54: leaved different domain levels, auction sniping and chatting, in this one unit of
Line 55: code. We’d like to split them up. Here it is again:
Line 56: public class Main { […]
Line 57:   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line 58:     ui.addUserRequestListener(new UserRequestListener() {
Line 59:     public void joinAuction(String itemId) {
Line 60:       snipers.addSniper(SniperSnapshot.joining(itemId));
Line 61:         Chat chat = connection.getChatManager()
Line 62:                                  .createChat(auctionId(itemId, connection), null);
Line 63:         notToBeGCd.add(chat); 
Line 64:         Auction auction = new XMPPAuction(chat);
Line 65: chat.addMessageListener(
Line 66:                new AuctionMessageTranslator(connection.getUser(),
Line 67:                      new AuctionSniper(itemId, auction, 
Line 68:                            new SwingThreadSniperListener(snipers))));
Line 69:         auction.join();
Line 70:       }
Line 71:     });
Line 72:   }
Line 73: }
Line 74: The object that locks this code into Smack is the chat; we refer to it several times:
Line 75: to avoid garbage collection, to attach it to the Auction implementation, and to
Line 76: attach the message listener. If we can gather together the auction- and Sniper-
Line 77: related code, we can move the chat elsewhere, but that’s tricky while there’s still
Line 78: a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Line 79: Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
Line 80: as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
Line 81: rather than a direct link, would give us the ﬂexibility we need. It would also make
Line 82: sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
Line 83: (page 52). The result is:
Line 84: Chapter 17
Line 85: Teasing Apart Main
Line 86: 192
Line 87: 
Line 88: --- 페이지 218 ---
Line 89: public class Main { […]
Line 90:   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line 91:     ui.addUserRequestListener(new UserRequestListener() {
Line 92:       public void joinAuction(String itemId) {
Line 93:         Chat chat = connection.[…]
Line 94:         Announcer<AuctionEventListener> auctionEventListeners = 
Line 95:             Announcer.to(AuctionEventListener.class);
Line 96:         chat.addMessageListener(
Line 97:             new AuctionMessageTranslator(
Line 98:                 connection.getUser(),
Line 99: auctionEventListeners.announce()));
Line 100:         notToBeGCd.add(chat);
Line 101:         Auction auction = new XMPPAuction(chat);
Line 102: auctionEventListeners.addListener(
Line 103:            new AuctionSniper(itemId, auction, new SwingThreadSniperListener(snipers)));
Line 104:         auction.join();
Line 105:       }
Line 106:     }
Line 107:   }
Line 108: }
Line 109: This looks worse, but the interesting bit is the last three lines. If you squint, it
Line 110: looks like everything is described in terms of Auctions and Snipers (there’s still
Line 111: the Swing thread issue, but we did tell you to squint).
Line 112: Encapsulating the Chat
Line 113: From here, we can push everything to do with chat, its setup, and the use of the
Line 114: Announcer, into XMPPAuction, adding management methods to the Auction inter-
Line 115: face for its AuctionEventListeners. We’re just showing the end result here, but
Line 116: we changed the code incrementally so that nothing was broken for more than a
Line 117: few minutes.
Line 118: public final class XMPPAuction implements Auction { […]
Line 119:   private final Announcer<AuctionEventListener> auctionEventListeners = […]
Line 120:   private final Chat chat;
Line 121:   public XMPPAuction(XMPPConnection connection, String itemId) {
Line 122:     chat = connection.getChatManager().createChat(
Line 123:              auctionId(itemId, connection),
Line 124:              new AuctionMessageTranslator(connection.getUser(), 
Line 125:                                           auctionEventListeners.announce()));
Line 126:   } 
Line 127:   private static String auctionId(String itemId, XMPPConnection connection) { 
Line 128:     return String.format(AUCTION_ID_FORMAT, itemId, connection.getServiceName());
Line 129:   }
Line 130: }
Line 131: 193
Line 132: Extracting the Chat
Line 133: 
Line 134: --- 페이지 219 ---
Line 135: Apart from the garbage collection “wart,” this removes any references to Chat
Line 136: from Main.
Line 137: public class Main { […]
Line 138:   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line 139:     ui.addUserRequestListener(new UserRequestListener() {
Line 140:       public void joinAuction(String itemId) {
Line 141:           snipers.addSniper(SniperSnapshot.joining(itemId));
Line 142:           Auction auction = new XMPPAuction(connection, itemId);
Line 143:           notToBeGCd.add(auction);
Line 144: auction.addAuctionEventListener(
Line 145:                   new AuctionSniper(itemId, auction, 
Line 146:                                     new SwingThreadSniperListener(snipers)));
Line 147: auction.join();
Line 148:       }
Line 149:     });
Line 150:   }
Line 151: }
Line 152: Figure 17.1
Line 153: With XMPPAuction extracted
Line 154: Writing a New Test
Line 155: We also write a new integration test for the expanded XMPPAuction to show that
Line 156: it can create a Chat and attach a listener. We use some of our existing end-to-end
Line 157: test infrastructure, such as FakeAuctionServer, and a CountDownLatch from the
Line 158: Java concurrency libraries to wait for a response.
Line 159: Chapter 17
Line 160: Teasing Apart Main
Line 161: 194
Line 162: 
Line 163: --- 페이지 220 ---
Line 164: @Test public void
Line 165: receivesEventsFromAuctionServerAfterJoining() throws Exception {
Line 166:   CountDownLatch auctionWasClosed = new CountDownLatch(1);
Line 167:   Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
Line 168:   auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
Line 169:   auction.join();
Line 170:   server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 171:   server.announceClosed();
Line 172:   assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS)); 
Line 173: } 
Line 174: private AuctionEventListener 
Line 175: auctionClosedListener(final CountDownLatch auctionWasClosed) {
Line 176:   return new AuctionEventListener() {
Line 177:     public void auctionClosed() { auctionWasClosed.countDown(); }
Line 178:     public void currentPrice(int price, int increment, PriceSource priceSource) { 
Line 179: // not implemented
Line 180:     }
Line 181:   };
Line 182: }
Line 183: Looking over the result, we can see that it makes sense for XMPPAuction to en-
Line 184: capsulate a Chat as now it hides everything to do with communicating between
Line 185: a request listener and an auction service, including translating the messages. We
Line 186: can also see that the AuctionMessageTranslator is internal to this encapsulation,
Line 187: the Sniper doesn’t need to see it. So, to recognize our new structure, we move
Line 188: XMPPAuction and AuctionMessageTranslator into a new auctionsniper.xmpp
Line 189: package, and the tests into equivalent xmpp test packages.
Line 190: Compromising on a Constructor
Line 191: We have one doubt about this implementation: the constructor includes some real
Line 192: behavior. Our experience is that busy constructors enforce assumptions that one
Line 193: day we will want to break, especially when testing, so we prefer to keep them very
Line 194: simple—just setting the ﬁelds. For now, we convince ourselves that this is “veneer”
Line 195: code, a bridge to an external library, that can only be integration-tested because
Line 196: the Smack classes have just the kind of complicated constructors we try to avoid.
Line 197: Extracting the Connection
Line 198: The next thing to remove from Main is direct references to the XMPPConnection.
Line 199: We can wrap these up in a factory class that will create an instance of an Auction
Line 200: for a given item, so it will have a method like
Line 201: Auction auction = <factory>.auctionFor(item id);
Line 202: 195
Line 203: Extracting the Connection
Line 204: 
Line 205: --- 페이지 221 ---
Line 206: We struggle for a while over what to call this new type, since it should have a
Line 207: name that reﬂects the language of auctions. In the end, we decide that the concept
Line 208: that arranges auctions is an “auction house,” so that’s what we call our new type:
Line 209: public interface AuctionHouse {
Line 210:   Auction auctionFor(String itemId);
Line 211: }
Line 212: The end result of this refactoring is:
Line 213: public class Main { […]
Line 214:   public static void main(String... args) throws Exception {
Line 215:     Main main = new Main();
Line 216: XMPPAuctionHouse auctionHouse = 
Line 217:       XMPPAuctionHouse.connect(
Line 218:         args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line 219:     main.disconnectWhenUICloses(auctionHouse);
Line 220:     main.addUserRequestListenerFor(auctionHouse);
Line 221:   }
Line 222:   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
Line 223:     ui.addUserRequestListener(new UserRequestListener() {
Line 224:       public void joinAuction(String itemId) {
Line 225:         snipers.addSniper(SniperSnapshot.joining(itemId));
Line 226: Auction auction = auctionHouse.auctionFor(itemId);
Line 227:         notToBeGCd.add(auction);
Line 228: […]
Line 229:       }
Line 230:     }
Line 231:   }
Line 232: }
Line 233: Figure 17.2
Line 234: With XMPPAuctionHouse extracted
Line 235: Chapter 17
Line 236: Teasing Apart Main
Line 237: 196
Line 238: 
Line 239: --- 페이지 222 ---
Line 240: Implementing XMPPAuctionHouse is straightforward; we transfer there all the
Line 241: code related to connection, including the generation of the Jabber ID from
Line 242: the auction item ID. Main is now simpler, with just one import for all the XMPP
Line 243: code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Line 244: Figure 17.2.
Line 245: For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
Line 246: XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
Line 247: the test to XMPPAuctionHouseTest.
Line 248: Our ﬁnal touch is to move the relevant constants from Main where we’d left
Line 249: them: the message formats to XMPPAuction and the connection identiﬁer format
Line 250: to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
Line 251: since we’re narrowing the scope of where these constants are used.
Line 252: Extracting the SnipersTableModel
Line 253: Sniper Launcher
Line 254: Finally, we’d like to do something about the direct reference to the
Line 255: SnipersTableModel and the related SwingThreadSniperListener—and the awful
Line 256: notToBeGCd. We think we can get there, but it’ll take a couple of steps.
Line 257: The ﬁrst step is to turn the anonymous implementation of UserRequestListener
Line 258: into a proper class so we can understand its dependencies. We decide to call the
Line 259: new class SniperLauncher, since it will respond to a request to join an auction
Line 260: by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
Line 261: to the new class.
Line 262: public class SniperLauncher implements UserRequestListener {
Line 263:   private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
Line 264:   private final AuctionHouse auctionHouse;
Line 265:   private final SnipersTableModel snipers;
Line 266:   public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
Line 267: // set the fields 
Line 268:   }
Line 269:   public void joinAuction(String itemId) {
Line 270: snipers.addSniper(SniperSnapshot.joining(itemId));
Line 271:       Auction auction = auctionHouse.auctionFor(itemId);
Line 272:       notToBeGCd.add(auction);
Line 273:       AuctionSniper sniper = 
Line 274:         new AuctionSniper(itemId, auction, 
Line 275:                           new SwingThreadSniperListener(snipers));
Line 276:       auction.addAuctionEventListener(snipers);
Line 277:       auction.join();
Line 278:   }
Line 279: }
Line 280: With the SniperLauncher separated out, it becomes even clearer that the
Line 281: Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
Line 282: 197
Line 283: Extracting the SnipersTableModel
Line 284: 
Line 285: --- 페이지 223 ---
Line 286: SnipersTableModel, is clumsy: we tell it about the new Sniper by giving it an
Line 287: initial SniperSnapshot, and we attach it to both the Sniper and the auction.
Line 288: There’s also some hidden duplication in that we create an initial SniperSnaphot
Line 289: both here and in the AuctionSniper constructor.
Line 290: Stepping back, we ought to simplify this class so that all it does is establish a
Line 291: new AuctionSniper. It can delegate the process of accepting the new Sniper into
Line 292: the application to a new role which we’ll call a SniperCollector, implemented
Line 293: in the SnipersTableModel.
Line 294: public static class SniperLauncher implements UserRequestListener {
Line 295:   private final AuctionHouse auctionHouse;
Line 296:   private final SniperCollector collector;
Line 297: […]
Line 298:   public void joinAuction(String itemId) {
Line 299:       Auction auction = auctionHouse.auctionFor(itemId);
Line 300: AuctionSniper sniper = new AuctionSniper(itemId, auction);
Line 301:       auction.addAuctionEventListener(sniper);
Line 302: collector.addSniper(sniper);
Line 303:       auction.join();
Line 304:   }
Line 305: }
Line 306: The one behavior that we want to conﬁrm is that we only join the auction after
Line 307: everything else is set up. With the code now isolated, we can jMock a States to
Line 308: check the ordering.
Line 309: public class SniperLauncherTest {
Line 310:   private final States auctionState = context.states("auction state")
Line 311: .startsAs("not joined");
Line 312: […]
Line 313:   @Test public void
Line 314: addsNewSniperToCollectorAndThenJoinsAuction() {
Line 315:     final String itemId = "item 123";
Line 316:     context.checking(new Expectations() {{
Line 317:       allowing(auctionHouse).auctionFor(itemId); will(returnValue(auction));
Line 318:       oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId))); 
Line 319: when(auctionState.is("not joined"));
Line 320:       oneOf(sniperCollector).addSniper(with(sniperForItem(item))); 
Line 321: when(auctionState.is("not joined"));
Line 322:       one(auction).join(); then(auctionState.is("joined"));
Line 323:     }});
Line 324:     launcher.joinAuction(itemId);
Line 325:   }
Line 326: }
Line 327: where sniperForItem() returns a Matcher that matches any AuctionSniper
Line 328: associated with the given item identiﬁer.
Line 329: We extend SnipersTableModel to fulﬁll its new role: now it accepts
Line 330: AuctionSnipers rather than SniperSnapshots. To make this work, we have to
Line 331: convert a Sniper’s listener from a dependency to a notiﬁcation, so that we can
Line 332: Chapter 17
Line 333: Teasing Apart Main
Line 334: 198
Line 335: 
Line 336: --- 페이지 224 ---
Line 337: add a listener after construction. We also change SnipersTableModel to use the
Line 338: new API and disallow adding SniperSnapshots.
Line 339: public class SnipersTableModel extends AbstractTableModel 
Line 340:     implements SniperListener, SniperCollector
Line 341: {
Line 342:   private final ArrayList<AuctionSniper> notToBeGCd = […]
Line 343:   public void addSniper(AuctionSniper sniper) {
Line 344:     notToBeGCd.add(sniper);
Line 345:     addSniperSnapshot(sniper.getSnapshot());
Line 346:     sniper.addSniperListener(new SwingThreadSniperListener(this));
Line 347:   }
Line 348:   private void addSniperSnapshot(SniperSnapshot sniperSnapshot) {
Line 349:     snapshots.add(sniperSnapshot);
Line 350:     int row = snapshots.size() - 1;
Line 351:     fireTableRowsInserted(row, row);
Line 352:    }
Line 353: }
Line 354: One change that suggests that we’re heading in the right direction is that the
Line 355: SwingThreadSniperListener is now packaged up in the Swing part of the code,
Line 356: not in the generic SniperLauncher.
Line 357: Sniper Portfolio
Line 358: As a next step, we realize that we don’t yet have anything that represents all our
Line 359: sniping activity and that we might call our portfolio. At the moment, the
Line 360: SnipersTableModel is implicitly responsible for both maintaining a record of
Line 361: our sniping and displaying that record. It also pulls a Swing implementation detail
Line 362: into Main.
Line 363: We want a clearer separation of concerns, so we extract a SniperPortfolio
Line 364: to maintain our Snipers, which we make our new implementer of
Line 365: SniperCollector. We push the creation of the SnipersTableModel into MainWindow,
Line 366: and make it a PortfolioListener so the portfolio can tell it when we add or
Line 367: remove a Sniper.
Line 368: public interface PortfolioListener extends EventListener {
Line 369:   void sniperAdded(AuctionSniper sniper);
Line 370: }
Line 371: public class MainWindow extends JFrame {
Line 372:   private JTable makeSnipersTable(SniperPortfolio portfolio) { 
Line 373: SnipersTableModel model = new SnipersTableModel();
Line 374:     portfolio.addPortfolioListener(model);
Line 375:     JTable snipersTable = new JTable(model); 
Line 376:     snipersTable.setName(SNIPERS_TABLE_NAME); 
Line 377:     return snipersTable; 
Line 378:   }
Line 379: }
Line 380: 199
Line 381: Extracting the SnipersTableModel
Line 382: 
Line 383: --- 페이지 225 ---
Line 384: This makes our top-level code very simple—it just binds together the user
Line 385: interface and sniper creation through the portfolio:
Line 386: public class Main {  […]
Line 387:   private final SniperPortfolio portfolio = new SniperPortfolio();
Line 388:   public Main() throws Exception {
Line 389:     SwingUtilities.invokeAndWait(new Runnable() {
Line 390:       public void run() {
Line 391:         ui = new MainWindow(portfolio);
Line 392:       }
Line 393:     });
Line 394:   }
Line 395:   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
Line 396:     ui.addUserRequestListener(new SniperLauncher(auctionHouse, portfolio));
Line 397:   }
Line 398: }
Line 399: Even better, since SniperPortfolio maintains a list of all the Snipers, we can
Line 400: ﬁnally get rid of notToBeGCd.
Line 401: This refactoring takes us to the structure shown in Figure 17.3. We’ve separated
Line 402: the code into three components: one for the core application, one for XMPP
Line 403: communication, and one for Swing display. We’ll return to this in a moment.
Line 404: Figure 17.3
Line 405: With the SniperPortfolio
Line 406: Chapter 17
Line 407: Teasing Apart Main
Line 408: 200
Line 409: 
Line 410: --- 페이지 226 ---
Line 411: Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Line 412: Figure 17.4
Line 413: Adding items through the user interface
Line 414: Observations
Line 415: Incremental Architecture
Line 416: This restructuring of Main is a key moment in the development of the application.
Line 417: As Figure 17.5 shows, we now have a structure that matches the “ports and
Line 418: adapters” architecture we described in “Designing for Maintainability” (page 47).
Line 419: There is core domain code (for example, AuctionSniper) which depends on
Line 420: bridging code (for example, SnipersTableModel) that drives or responds to
Line 421: technical code (for example, JTable). We’ve kept the domain code free of any
Line 422: reference to the external infrastructure. The contents of our auctionsniper
Line 423: package deﬁne a model of our auction sniping business, using a self-contained
Line 424: language. The exception is Main, which is our entry point and binds the domain
Line 425: model and infrastructure together.
Line 426: What’s important for the purposes of this example, is that we arrived at this
Line 427: design incrementally, by adding features and repeatedly following heuristics.
Line 428: Although we rely on our experience to guide our decisions, we reached this
Line 429: solution almost automatically by just following the code and taking care to keep
Line 430: it clean.
Line 431: 201
Line 432: Observations
Line 433: 
Line 434: --- 페이지 227 ---
Line 435: Figure 17.5
Line 436: The application now has a “ports and adapters”
Line 437: architecture
Line 438: Three-Point Contact
Line 439: We wrote this refactoring up in detail because we wanted to make some points
Line 440: along the way and to show that we can do signiﬁcant refactorings incrementally.
Line 441: When we’re not sure what to do next or how to get there from here, one way of
Line 442: coping is to scale down the individual changes we make, as Kent Beck showed
Line 443: in [Beck02]. By repeatedly ﬁxing local problems in the code, we ﬁnd we can ex-
Line 444: plore the design safely, never straying more than a few minutes from working
Line 445: code. Usually this is enough to lead us towards a better design, and we can always
Line 446: backtrack and take another path if it doesn’t work out.
Line 447: One way to think of this is the rock climbing rule of “three-point contact.”
Line 448: Trained climbers only move one limb at a time (a hand or a foot), to minimize
Line 449: the risk of falling off. Each move is minimal and safe, but combining enough of
Line 450: them will get you to the top of the route.
Line 451: In “elapsed time,” this refactoring didn’t take much longer than the time you
Line 452: spent reading it, which we think is a good return for the clearer separation of
Line 453: concerns. With experience, we’ve learned to recognize fault lines in code so we
Line 454: can often take a more direct route.
Line 455: Chapter 17
Line 456: Teasing Apart Main
Line 457: 202
Line 458: 
Line 459: --- 페이지 228 ---
Line 460: Dynamic as Well as Static Design
Line 461: We did encounter one small bump whilst working on the code for this chapter.
Line 462: Steve was extracting the SniperPortfolio and got stuck trying to ensure that the
Line 463: sniperAdded() method was called within the Swing thread. Eventually he remem-
Line 464: bered that the event is triggered by a button click anyway, so he was already
Line 465: covered.
Line 466: What we learn from this (apart from the need for pairing while writing book
Line 467: examples) is that we should consider more than one view when refactoring code.
Line 468: Refactoring is, after all, a design activity, which means we still need all the skills
Line 469: we were taught—except that now we need them all the time rather than periodi-
Line 470: cally. Refactoring is so focused on static structure (classes and interfaces) that
Line 471: it’s easy to lose sight of an application’s dynamic structure (instances and threads).
Line 472: Sometimes we just need to step back and draw out, say, an interaction diagram
Line 473: like Figure 17.6:
Line 474: Figure 17.6
Line 475: An Interaction Diagram
Line 476: An Alternative Fix to notToBeGCd
Line 477: Our chosen ﬁx relies on the SniperPortfolio holding onto the reference. That’s
Line 478: likely to be the case in practice, but if it ever changes we will get transient failures
Line 479: that are hard to track down. We’re relying on a side effect of the application to
Line 480: ﬁx an issue in the XMPP code.
Line 481: An alternative would be to say that it’s a Smack problem, so our XMPP layer
Line 482: should deal with it. We could make the XMPPAuctionHouse hang on to the
Line 483: XMPPAuctions it creates, in which case we’d to have to add a lifecycle listener of
Line 484: some sort to tell us when we’re ﬁnished with an Auction and can release it. There
Line 485: is no obvious choice here; we just have to look at the circumstances and exercise
Line 486: some judgment.
Line 487: 203
Line 488: Observations
Line 489: 
Line 490: --- 페이지 229 ---
Line 491: This page intentionally left blank 