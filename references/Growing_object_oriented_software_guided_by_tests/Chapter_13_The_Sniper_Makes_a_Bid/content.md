Line 1: 
Line 2: --- 페이지 148 ---
Line 3: Chapter 13
Line 4: The Sniper Makes a Bid
Line 5: In which we extract an AuctionSniper class and tease out its dependen-
Line 6: cies. We plug our new class into the rest of the application, using an
Line 7: empty implementation of auction until we’re ready to start sending
Line 8: commands. We close the loop back to the auction house with an
Line 9: XMPPAuction class. We continue to carve new types out of the code.
Line 10: Introducing AuctionSniper
Line 11: A New Class, with Dependencies
Line 12: Our application accepts Price events from the auction, but cannot interpret them
Line 13: yet. We need code that will perform two actions when the currentPrice() method
Line 14: is called: send a higher bid to the auction and update the status in the user inter-
Line 15: face. We could extend Main, but that class is looking rather messy—it’s already
Line 16: doing too many things at once. It feels like this is a good time to introduce
Line 17: what we should call an “Auction Sniper,” the component at the heart of our
Line 18: application, so we create an AuctionSniper class. Some of its intended behavior
Line 19: is currently buried in Main, and a good start would be to extract it into our new
Line 20: class—although, as we’ll see in a moment, it will take a little effort.
Line 21: Given that an AuctionSniper should respond to Price events, we decide to
Line 22: make it implement AuctionEventListener rather than Main. The question is what
Line 23: to do about the user interface. If we consider moving this method:
Line 24: public void auctionClosed() {
Line 25:   SwingUtilities.invokeLater(new Runnable() {
Line 26:     public void run() {
Line 27:        ui.showStatus(MainWindow.STATUS_LOST);
Line 28:     }
Line 29:   });
Line 30: }
Line 31: does it really make sense for an AuctionSniper to know about the implementation
Line 32: details of the user interface, such as the use of the Swing thread? We’d be at risk
Line 33: of breaking the “single responsibility” principle again. Surely an AuctionSniper
Line 34: ought to be concerned with bidding policy and only notify status changes in
Line 35: its terms?
Line 36: 123
Line 37: 
Line 38: --- 페이지 149 ---
Line 39: Our solution is to insulate the AuctionSniper by introducing a new relationship:
Line 40: it will notify a SniperListener of changes in its status. The interface and the ﬁrst
Line 41: unit test look like this:
Line 42: public interface SniperListener extends EventListener {
Line 43:   void sniperLost();
Line 44: }
Line 45: @RunWith(JMock.class)
Line 46: public class AuctionSniperTest {
Line 47:   private final Mockery context = new Mockery();
Line 48:   private final SniperListener sniperListener = 
Line 49:                                       context.mock(SniperListener.class);
Line 50:   private final AuctionSniper sniper = new AuctionSniper(sniperListener);
Line 51:   @Test public void
Line 52: reportsLostWhenAuctionCloses() {
Line 53:     context.checking(new Expectations() {{
Line 54:       one(sniperListener).sniperLost();
Line 55:     }});
Line 56:     sniper.auctionClosed();
Line 57:   }
Line 58: }
Line 59: which says that Sniper should report that it has lost if it receives a Close event
Line 60: from the auction.
Line 61: The failure report says:
Line 62: not all expectations were satisfied
Line 63: expectations:
Line 64: ! expected exactly 1 time, never invoked: SniperListener.sniperLost();
Line 65: which we can make pass with a simple implementation:
Line 66: public class AuctionSniper implements AuctionEventListener {
Line 67:   private final SniperListener sniperListener;
Line 68:   public AuctionSniper(SniperListener sniperListener) {
Line 69:     this.sniperListener = sniperListener;
Line 70:   }
Line 71: public void auctionClosed() {
Line 72:     sniperListener.sniperLost();
Line 73:   }
Line 74:   public void currentPrice(int price, int increment) {
Line 75: // TODO Auto-generated method stub
Line 76:   }
Line 77: }
Line 78: Finally, we retroﬁt the new AuctionSniper by having Main implement
Line 79: SniperListener.
Line 80: Chapter 13
Line 81: The Sniper Makes a Bid
Line 82: 124
Line 83: 
Line 84: --- 페이지 150 ---
Line 85: public class Main implements SniperListener { […]
Line 86:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 87:     throws XMPPException 
Line 88:   {
Line 89:     disconnectWhenUICloses(connection);
Line 90:     Chat chat = connection.getChatManager().createChat(
Line 91:         auctionId(itemId, connection), 
Line 92:         new AuctionMessageTranslator(new AuctionSniper(this)));
Line 93:     this.notToBeGCd = chat;
Line 94:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 95:   }
Line 96:   public void sniperLost() {
Line 97:     SwingUtilities.invokeLater(new Runnable() {
Line 98:       public void run() {
Line 99:         ui.showStatus(MainWindow.STATUS_LOST);
Line 100:       }
Line 101:     });
Line 102:   }
Line 103: }
Line 104: Our working end-to-end test still passes and our broken one still fails at the
Line 105: same place, so we haven’t made things worse. The new structure looks like
Line 106: Figure 13.1.
Line 107: Figure 13.1
Line 108: Plugging in the AuctionSniper
Line 109: Focus, Focus, Focus
Line 110: Once again, we’ve noticed complexity in a class and used that to tease out a new
Line 111: concept from our initial skeleton implementation. Now we have a Sniper to re-
Line 112: spond to events from the translator. As you’ll see shortly, this is a better structure
Line 113: for expressing what the code does and for unit testing. We also think that the
Line 114: sniperLost() method is clearer than its previous incarnation, auctionClosed(),
Line 115: since there’s now a closer match between its name and what it does—that is,
Line 116: reports a lost auction.
Line 117: Isn’t this wasteful ﬁddling, gold-plating the code while time slips by? Obviously
Line 118: we don’t think so, especially when we’re sorting out our ideas this early in the
Line 119: project. There are teams that overdo their design effort, but our experience is
Line 120: that most teams spend too little time clarifying the code and pay for it in mainte-
Line 121: nance overhead. As we’ve shown a couple of times now, the “single responsibil-
Line 122: ity” principle is a very effective heuristic for breaking up complexity, and
Line 123: 125
Line 124: Introducing AuctionSniper
Line 125: 
Line 126: --- 페이지 151 ---
Line 127: developers shouldn’t be shy about creating new types. We think Main still does
Line 128: too much, but we’re not yet sure how best to break it up. We decide to push on
Line 129: and see where the code takes us.
Line 130: Sending a Bid
Line 131: An Auction Interface
Line 132: The next step is to have the Sniper send a bid to the auction, so who should the
Line 133: Sniper talk to? Extending the SniperListener feels wrong because that relationship
Line 134: is about tracking what’s happening in the Sniper, not about making external
Line 135: commitments. In the terms deﬁned in “Object Peer Stereotypes” (page 52),
Line 136: SniperListener is a notiﬁcation, not a dependency.
Line 137: After the usual discussion, we decide to introduce a new collaborator, an
Line 138: Auction. Auction and SniperListener represent two different domains in the
Line 139: application: Auction is about ﬁnancial transactions, it accepts bids for items in
Line 140: the market; and SniperListener is about feedback to the application, it reports
Line 141: changes to the current state of the Sniper. The Auction is a dependency, for a
Line 142: Sniper cannot function without one, whereas the SniperListener, as we
Line 143: discussed above, is not. Introducing the new interface makes the design look like
Line 144: Figure 13.2.
Line 145: Figure 13.2
Line 146: Introducing Auction
Line 147: The AuctionSniper Bids
Line 148: Now we’re ready to start bidding. The ﬁrst step is to implement the response to
Line 149: a Price event, so we start by adding a new unit test for the AuctionSniper. It
Line 150: says that the Sniper, when it receives a Price update, sends an incremented bid
Line 151: to the auction. It also notiﬁes its listener that it’s now bidding, so we add a
Line 152: sniperBidding() method. We’re making an implicit assumption that the Auction
Line 153: knows which bidder the Sniper represents, so the Sniper does not have to pass
Line 154: in that information with the bid.
Line 155: Chapter 13
Line 156: The Sniper Makes a Bid
Line 157: 126
Line 158: 
Line 159: --- 페이지 152 ---
Line 160: public class AuctionSniperTest {
Line 161: private final Auction auction = context.mock(Auction.class);
Line 162:   private final AuctionSniper sniper = 
Line 163:                     new AuctionSniper(auction, sniperListener);
Line 164: […]
Line 165:   @Test public void
Line 166: bidsHigherAndReportsBiddingWhenNewPriceArrives() {
Line 167:     final int price = 1001;
Line 168:     final int increment = 25;
Line 169:     context.checking(new Expectations() {{
Line 170:       one(auction).bid(price + increment);
Line 171:       atLeast(1).of(sniperListener).sniperBidding();
Line 172:     }});
Line 173:     sniper.currentPrice(price, increment);
Line 174:   }
Line 175: }
Line 176: The failure report is:
Line 177: not all expectations were satisfied
Line 178: expectations:
Line 179:   ! expected once, never invoked: auction.bid(<1026>)
Line 180:   ! expected at least 1 time, never invoked: sniperListener.sniperBidding()
Line 181: what happened before this: nothing!
Line 182: When writing the test, we realized that we don’t actually care if the Sniper
Line 183: notiﬁes the listener more than once that it’s bidding; it’s just a status update,
Line 184: so we use an atLeast(1) clause for the listener’s expectation. On the other hand,
Line 185: we do care that we send a bid exactly once, so we use a one() clause for its ex-
Line 186: pectation. In practice, of course, we’ll probably only call the listener once, but
Line 187: this loosening of the conditions in the test expresses our intent about the two
Line 188: relationships. The test says that the listener is a more forgiving collaborator, in
Line 189: terms of how it’s called, than the Auction. We also retroﬁt the atLeast(1) clause
Line 190: to the other test method.
Line 191: How Should We Describe Expected Values?
Line 192: We’ve speciﬁed the expected bid value by adding the price and increment.There
Line 193: are different opinions about whether test values should just be literals with “obvious”
Line 194: values, or expressed in terms of the calculation they represent. Writing out the
Line 195: calculation may make the test more readable but risks reimplementing the target
Line 196: code in the test, and in some cases the calculation will be too complicated to repro-
Line 197: duce. Here, we decide that the calculation is so trivial that we can just write it into
Line 198: the test.
Line 199: 127
Line 200: Sending a Bid
Line 201: 
Line 202: --- 페이지 153 ---
Line 203: jMock Expectations Don’t Need to Be Matched in Order
Line 204: This is our ﬁrst test with more than one expectation, so we’ll point out that the order
Line 205: in which expectations are declared does not have to match the order in which the
Line 206: methods are called in the code. If the calling order does matter, the expectations
Line 207: should include a sequence clause, which is described in Appendix A.
Line 208: The implementation to make the test pass is simple.
Line 209: public interface Auction {
Line 210:   void bid(int amount);
Line 211: }
Line 212: public class AuctionSniper implements AuctionEventListener {  […]
Line 213:   private final SniperListener sniperListener;
Line 214: private final Auction auction;
Line 215:   public AuctionSniper(Auction auction, SniperListener sniperListener) {
Line 216: this.auction = auction;
Line 217:     this.sniperListener = sniperListener;
Line 218:   }
Line 219:   public void currentPrice(int price, int increment) {
Line 220:     auction.bid(price + increment);
Line 221:     sniperListener.sniperBidding();
Line 222:   }
Line 223: }
Line 224: Successfully Bidding with the AuctionSniper
Line 225: Now we have to fold our new AuctionSniper back into the application. The easy
Line 226: part is displaying the bidding status, the (slightly) harder part is sending the bid
Line 227: back to the auction. Our ﬁrst job is to get the code through the compiler. We
Line 228: implement the new sniperBidding() method on Main and, to avoid having
Line 229: code that doesn’t compile for too long, we pass the AuctionSniper a null
Line 230: implementation of Auction.
Line 231: Chapter 13
Line 232: The Sniper Makes a Bid
Line 233: 128
Line 234: 
Line 235: --- 페이지 154 ---
Line 236: public class Main implements SniperListener { […]
Line 237:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 238:     throws XMPPException 
Line 239:   {
Line 240: Auction nullAuction = new Auction() {
Line 241:       public void bid(int amount) {}
Line 242:     };
Line 243:     disconnectWhenUICloses(connection);
Line 244:     Chat chat = connection.getChatManager().createChat(
Line 245:         auctionId(itemId, connection), 
Line 246:         new AuctionMessageTranslator(new AuctionSniper(nullAuction, this)));
Line 247:     this.notToBeGCd = chat;
Line 248:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 249:   }
Line 250:   public void sniperBidding() {
Line 251:     SwingUtilities.invokeLater(new Runnable() {
Line 252:       public void run() {
Line 253:         ui.showStatus(MainWindow.STATUS_BIDDING);
Line 254:       }
Line 255:     });
Line 256:   }
Line 257: }
Line 258: So, what goes in the Auction implementation? It needs access to the chat so it
Line 259: can send a bid message. To create the chat we need a translator, the translator
Line 260: needs a Sniper, and the Sniper needs an auction. We have a dependency loop
Line 261: which we need to break.
Line 262: Looking again at our design, there are a couple of places we could intervene,
Line 263: but it turns out that the ChatManager API is misleading. It does not require a
Line 264: MessageListener to create a Chat, even though the createChat() methods imply
Line 265: that it does. In our terms, the MessageListener is a notiﬁcation; we can pass in
Line 266: null when we create the Chat and add a MessageListener later.
Line 267: Expressing Intent in API
Line 268: We were only able to discover that we could pass null as a MessageListener
Line 269: because we have the source code to the Smack library. This isn’t clear from the
Line 270: API because, presumably, the authors wanted to enforce the right behavior and
Line 271: it’s not clear why anyone would want a Chat without a listener. An alternative would
Line 272: have been to provide equivalent creation methods that don’t take a listener, but
Line 273: that would lead to API bloat. There isn’t an obvious best approach here, except to
Line 274: note that including well-structured source code with the distribution makes libraries
Line 275: much easier to work with.
Line 276: 129
Line 277: Sending a Bid
Line 278: 
Line 279: --- 페이지 155 ---
Line 280: Now we can restructure our connection code and use the Chat to send back
Line 281: a bid.
Line 282: public class Main implements SniperListener { […]
Line 283:   private void joinAuction(XMPPConnection connection, String itemId) 
Line 284:     throws XMPPException 
Line 285:   {
Line 286:     disconnectWhenUICloses(connection);
Line 287:     final Chat chat = 
Line 288:       connection.getChatManager().createChat(auctionId(itemId, connection), null);
Line 289:     this.notToBeGCd = chat;
Line 290:     Auction auction = new Auction() {
Line 291:       public void bid(int amount) {
Line 292:         try {
Line 293:           chat.sendMessage(String.format(BID_COMMAND_FORMAT, amount));
Line 294:         } catch (XMPPException e) {
Line 295:           e.printStackTrace();
Line 296:         }
Line 297:       }
Line 298:     };
Line 299:     chat.addMessageListener(
Line 300:            new AuctionMessageTranslator(new AuctionSniper(auction, this)));
Line 301:     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line 302:   }
Line 303: }
Line 304: Null Implementation
Line 305: A null implementation is similar to a null object [Woolf98]: both are implementations
Line 306: that respond to a protocol by not doing anything—but the intention is different. A
Line 307: null object is usually one implementation amongst many, introduced to reduce
Line 308: complexity in the code that calls the protocol. We deﬁne a null implementation as
Line 309: a temporary empty implementation, introduced to allow the programmer to make
Line 310: progress by deferring effort and intended to be replaced.
Line 311: The End-to-End Tests Pass
Line 312: Now the end-to-end tests pass: the Sniper can lose without making a bid, and
Line 313: lose after making a bid. We can cross off another item on the to-do list, but that
Line 314: includes just catching and printing the XMPPException. Normally, we regard this
Line 315: as a very bad practice but we wanted to see the tests pass and get some structure
Line 316: into the code—and we know that the end-to-end tests will fail anyway if there’s
Line 317: a problem sending a message. To make sure we don’t forget, we add another
Line 318: to-do item to ﬁnd a better solution, Figure 13.3.
Line 319: Chapter 13
Line 320: The Sniper Makes a Bid
Line 321: 130
Line 322: 
Line 323: --- 페이지 156 ---
Line 324: Figure 13.3
Line 325: One step forward
Line 326: Tidying Up the Implementation
Line 327: Extracting XMPPAuction
Line 328: Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
Line 329: tation feels messy. We notice that the activity in joinAuction() crosses multiple
Line 330: domains: managing chats, sending bids, creating snipers, and so on. We need to
Line 331: clean up. To start, we notice that we’re sending auction commands from two
Line 332: different levels, at the top and from within the Auction. Sending commands to
Line 333: an auction sounds like the sort of thing that our Auction object should do, so it
Line 334: makes sense to package that up together. We add a new method to the interface,
Line 335: extend our anonymous implementation, and then extract it to a (temporarily)
Line 336: nested class—for which we need a name. The distinguishing feature of this imple-
Line 337: mentation of Auction is that it’s based on the messaging infrastructure, so we
Line 338: call our new class XMPPAuction.
Line 339: 131
Line 340: Tidying Up the Implementation
Line 341: 
Line 342: --- 페이지 157 ---
Line 343: public class Main implements SniperListener { […]
Line 344:   private void joinAuction(XMPPConnection connection, String itemId) {
Line 345:     disconnectWhenUICloses(connection);
Line 346:     final Chat chat = 
Line 347:       connection.getChatManager().createChat(auctionId(itemId, connection), 
Line 348:                                              null);
Line 349:     this.notToBeGCd = chat;
Line 350:     Auction auction = new XMPPAuction(chat);
Line 351:     chat.addMessageListener(
Line 352:         new AuctionMessageTranslator(new AuctionSniper(auction, this)));
Line 353: auction.join();
Line 354:   }
Line 355:   public static class XMPPAuction implements Auction {
Line 356:     private final Chat chat;
Line 357:     public XMPPAuction(Chat chat) {
Line 358:       this.chat = chat;
Line 359:     }
Line 360:     public void bid(int amount) {
Line 361:       sendMessage(format(BID_COMMAND_FORMAT, amount));
Line 362:     }
Line 363:     public void join() {
Line 364:       sendMessage(JOIN_COMMAND_FORMAT);
Line 365:     }
Line 366:     private void sendMessage(final String message) {
Line 367:       try {
Line 368:         chat.sendMessage(message);
Line 369:       } catch (XMPPException e) {
Line 370:         e.printStackTrace();
Line 371:       }
Line 372:     }
Line 373:   }
Line 374: }
Line 375: We’re starting to see a clearer model of the domain. The line auction.join()
Line 376: expresses our intent more clearly than the previous detailed implementation of
Line 377: sending a string to a chat. The new design looks like Figure 13.4  and we promote
Line 378: XMPPAuction to be a top-level class.
Line 379: We still think joinAuction() is unclear, and we’d like to pull the XMPP-related
Line 380: detail out of Main, but we’re not ready to do that yet. Another point to keep
Line 381: in mind.
Line 382: Chapter 13
Line 383: The Sniper Makes a Bid
Line 384: 132
Line 385: 
Line 386: --- 페이지 158 ---
Line 387: Figure 13.4
Line 388: Closing the loop with an XMPPAuction
Line 389: Extracting the User Interface
Line 390: The other activity in Main is implementing the user interface and showing the
Line 391: current state in response to events from the Sniper. We’re not really happy that
Line 392: Main implements SniperListener; again, it feels like mixing different responsibil-
Line 393: ities (starting the application and responding to events). We decide to extract the
Line 394: SniperListener behavior into a nested helper class, for which the best name we
Line 395: can ﬁnd is SniperStateDisplayer. This new class is our bridge between two do-
Line 396: mains: it translates Sniper events into a representation that Swing can display,
Line 397: which includes dealing with Swing threading. We plug an instance of the new
Line 398: class into the AuctionSniper.
Line 399: public class Main { // doesn't implement SniperListener
Line 400:   private MainWindow ui;
Line 401:   private void joinAuction(XMPPConnection connection, String itemId) {
Line 402:     disconnectWhenUICloses(connection);
Line 403:     final Chat chat = 
Line 404:       connection.getChatManager().createChat(auctionId(itemId, connection), null);
Line 405:     this.notToBeGCd = chat;
Line 406:     Auction auction = new XMPPAuction(chat);
Line 407:     chat.addMessageListener(
Line 408:         new AuctionMessageTranslator(
Line 409:             connection.getUser(),
Line 410:             new AuctionSniper(auction, new SniperStateDisplayer())));
Line 411:     auction.join();
Line 412:   }
Line 413: […]
Line 414: 133
Line 415: Tidying Up the Implementation
Line 416: 
Line 417: --- 페이지 159 ---
Line 418:   public class SniperStateDisplayer implements SniperListener {
Line 419:     public void sniperBidding() {
Line 420:       showStatus(MainWindow.STATUS_BIDDING);
Line 421:     }
Line 422:     public void sniperLost() {
Line 423:       showStatus(MainWindow.STATUS_LOST);
Line 424:     }
Line 425:     public void sniperWinning() {
Line 426:       showStatus(MainWindow.STATUS_WINNING);
Line 427:     }
Line 428:     private void showStatus(final String status) {
Line 429:       SwingUtilities.invokeLater(new Runnable() {
Line 430:         public void run() { ui.showStatus(status); } 
Line 431:       });
Line 432:     }
Line 433:   }
Line 434: }
Line 435: Figure 13.5 shows how we’ve reduced Main so much that it no longer partici-
Line 436: pates in the running application (for clarity, we’ve left out the WindowAdapter
Line 437: that closes the connection). It has one job which is to create the various compo-
Line 438: nents and introduce them to each other. We’ve marked MainWindow as external,
Line 439: even though it’s one of ours, to represent the Swing framework.
Line 440: Figure 13.5
Line 441: Extracting SniperStateDisplayer
Line 442: Chapter 13
Line 443: The Sniper Makes a Bid
Line 444: 134
Line 445: 
Line 446: --- 페이지 160 ---
Line 447: Tidying Up the Translator
Line 448: Finally, 
Line 449: we 
Line 450: fulﬁll 
Line 451: our 
Line 452: promise 
Line 453: to 
Line 454: ourselves 
Line 455: and 
Line 456: return 
Line 457: to 
Line 458: the
Line 459: AuctionMessageTranslator. We start trying to reduce the noise by adding
Line 460: constants and static imports, with some helper methods to reduce duplication.
Line 461: Then we realize that much of the code is about manipulating the map of
Line 462: name/value pairs and is rather procedural. We can do a better job by extracting
Line 463: an inner class, AuctionEvent, to encapsulate the unpacking of the message con-
Line 464: tents. We have conﬁdence that we can refactor the class safely because it’s
Line 465: protected by its unit tests.
Line 466: public class AuctionMessageTranslator implements MessageListener { 
Line 467:   private final AuctionEventListener listener;
Line 468:   public AuctionMessageTranslator(AuctionEventListener listener) {
Line 469:     this.listener = listener;
Line 470:   }
Line 471:   public void processMessage(Chat chat, Message message) { 
Line 472: AuctionEvent event = AuctionEvent.from(message.getBody());
Line 473:     String eventType = event.type();
Line 474:     if ("CLOSE".equals(eventType)) { 
Line 475:       listener.auctionClosed(); 
Line 476:     } if ("PRICE".equals(eventType)) { 
Line 477:       listener.currentPrice(event.currentPrice(), event.increment()); 
Line 478:     } 
Line 479:   }
Line 480:   private static class AuctionEvent {
Line 481:     private final Map<String, String> fields = new HashMap<String, String>();  
Line 482:     public String type() { return get("Event"); }
Line 483:     public int currentPrice() { return getInt("CurrentPrice"); }
Line 484:     public int increment() { return getInt("Increment"); }
Line 485:     private int getInt(String fieldName) {
Line 486:       return Integer.parseInt(get(fieldName));
Line 487:     }
Line 488:     private String get(String fieldName) { return fields.get(fieldName); }
Line 489:     private void addField(String field) {
Line 490:       String[] pair = field.split(":");
Line 491:       fields.put(pair[0].trim(), pair[1].trim());
Line 492:     }
Line 493:     static AuctionEvent from(String messageBody) {
Line 494:       AuctionEvent event = new AuctionEvent();
Line 495:       for (String field : fieldsIn(messageBody)) {
Line 496:         event.addField(field);
Line 497:       }
Line 498:       return event;
Line 499:     }
Line 500:     static String[] fieldsIn(String messageBody) {
Line 501:       return messageBody.split(";");
Line 502:     }
Line 503:   }
Line 504: }
Line 505: 135
Line 506: Tidying Up the Implementation
Line 507: 
Line 508: --- 페이지 161 ---
Line 509: This is an example of “breaking out” that we described in “Value Types”
Line 510: (page 59). It may not be obvious, but AuctionEvent is a value: it’s
Line 511: immutable and there are no interesting differences between two instances
Line 512: with the same contents. This refactoring separates the concerns within
Line 513: AuctionMessageTranslator: the top level deals with events and listeners, and
Line 514: the inner object deals with parsing strings.
Line 515: Encapsulate Collections
Line 516: We’ve developed a habit of packaging up common types, such as collections, in
Line 517: our own classes, even though Java generics avoid the need to cast objects. We’re
Line 518: trying to use the language of the problem we’re working on, rather than the language
Line 519: of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
Line 520: incidental noise about looking up and parsing values.The second is written in terms
Line 521: of auction events, so there’s less of a conceptual gap between the domain and
Line 522: the code.
Line 523: Our rule of thumb is that we try to limit passing around types with generics (the
Line 524: types enclosed in angle brackets). Particularly when applied to collections, we view
Line 525: it as a form of duplication. It’s a hint that there’s a domain concept that should be
Line 526: extracted into a type.
Line 527: Defer Decisions
Line 528: There’s a technique we’ve used a couple of times now, which is to introduce a
Line 529: null implementation of a method (or even a type) to get us through the next step.
Line 530: This helps us focus on the immediate task without getting dragged into thinking
Line 531: about the next signiﬁcant chunk of functionality. The null Auction, for example,
Line 532: allowed us to plug in a new relationship we’d discovered in a unit test without
Line 533: getting pulled into messaging issues. That, in turn, meant we could stop and
Line 534: think about the dependencies between our objects without the pressure of having
Line 535: a broken compilation.
Line 536: Keep the Code Compiling
Line 537: We try to minimize the time when we have code that does not compile by keeping
Line 538: changes incremental. When we have compilation failures, we can’t be quite sure
Line 539: where the boundaries of our changes are, since the compiler can’t tell us. This, in
Line 540: turn, means that we can’t check in to our source repository, which we like to do
Line 541: often.The more code we have open, the more we have to keep in our heads which,
Line 542: ironically, usually means we move more slowly. One of the great discoveries of
Line 543: test-driven development is just how ﬁne-grained our development steps can be.
Line 544: Chapter 13
Line 545: The Sniper Makes a Bid
Line 546: 136
Line 547: 
Line 548: --- 페이지 162 ---
Line 549: Emergent Design
Line 550: What we hope is becoming clear from this chapter is how we’re growing a design
Line 551: from what looks like an unpromising start. We alternate, more or less, between
Line 552: adding features and reﬂecting on—and cleaning up—the code that results. The
Line 553: cleaning up stage is essential, since without it we would end up with an unmain-
Line 554: tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
Line 555: what to do, conﬁdent that we will take the time when we’re ready. In the mean-
Line 556: time, we keep our code as clean as possible, moving in small increments and using
Line 557: techniques such as null implementation to minimize the time when it’s broken.
Line 558: Figure 13.5 shows that we’re building up a layer around our core implementa-
Line 559: tion that “protects” it from its external dependencies. We think this is just good
Line 560: practice, but what’s interesting is that we’re getting there incrementally, by
Line 561: looking for features in classes that either go together or don’t. Of course we’re
Line 562: inﬂuenced by our experience of working on similar codebases, but we’re trying
Line 563: hard to follow what the code is telling us instead of imposing our preconceptions.
Line 564: Sometimes, when we do this, we ﬁnd that the domain takes us in the most
Line 565: surprising directions.
Line 566: 137
Line 567: Emergent Design
Line 568: 
Line 569: --- 페이지 163 ---
Line 570: This page intentionally left blank 