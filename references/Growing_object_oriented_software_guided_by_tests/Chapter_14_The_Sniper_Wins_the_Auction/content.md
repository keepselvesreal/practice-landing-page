Line 1: 
Line 2: --- 페이지 164 ---
Line 3: Chapter 14
Line 4: The Sniper Wins the Auction
Line 5: In which we add another feature to our Sniper and let it win an auction.
Line 6: We introduce the concept of state to the Sniper which we test by listen-
Line 7: ing to its callbacks. We ﬁnd that even this early, one of our refactorings
Line 8: has paid off.
Line 9: First, a Failing Test
Line 10: We have a Sniper that can respond to price changes by bidding more, but it
Line 11: doesn’t yet know when it’s successful. Our next feature on the to-do list is to
Line 12: win an auction. This involves an extra state transition, as you can see in
Line 13: Figure 14.1:
Line 14: Figure 14.1
Line 15: A sniper bids, then wins
Line 16: To represent this, we add an end-to-end test based on sniperMakesAHigherBid-
Line 17: ButLoses() with a different conclusion—sniperWinsAnAuctionByBiddingHigher().
Line 18: Here’s the test, with the new features highlighted:
Line 19: 139
Line 20: 
Line 21: --- 페이지 165 ---
Line 22: public class AuctionSniperEndToEndTest { […]
Line 23:   @Test public void
Line 24: sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line 25:     auction.startSellingItem();
Line 26:     application.startBiddingIn(auction);
Line 27:     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line 28:     auction.reportPrice(1000, 98, "other bidder");
Line 29:     application.hasShownSniperIsBidding();
Line 30:     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line 31: auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line 32:     application.hasShownSniperIsWinning();
Line 33:     auction.announceClosed();
Line 34:     application.showsSniperHasWonAuction();
Line 35:   }
Line 36: }
Line 37: In our test infrastructure we add the two methods to check that the user interface
Line 38: shows the two new states to the ApplicationRunner.
Line 39: This generates a new failure message:
Line 40: java.lang.AssertionError: 
Line 41: Tried to look for...
Line 42:   exactly 1 JLabel (with name "sniper status")
Line 43:   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 44:   in all top level windows
Line 45: and check that its label text is "Winning"
Line 46: but...
Line 47:   all top level windows
Line 48:   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 49:   contained 1 JLabel (with name "sniper status")
Line 50: label text was "Bidding"
Line 51: Now we know where we’re going, we can implement the feature.
Line 52: Who Knows about Bidders?
Line 53: The application knows that the Sniper is winning if it’s the bidder for the last
Line 54: price that the auction accepted. We have to decide where to put that logic.
Line 55: Looking again at Figure 13.5 on page 134, one choice would be that the translator
Line 56: could pass the bidder through to the Sniper and let the Sniper decide. That would
Line 57: mean that the Sniper would have to know something about how bidders are
Line 58: identiﬁed by the auction, with a risk of pulling in XMPP details that we’ve been
Line 59: careful to keep separate. To decide whether it’s winning, the only thing the Sniper
Line 60: needs to know when a price arrives is, did this price come from me? This is a
Line 61: Chapter 14
Line 62: The Sniper Wins the Auction
Line 63: 140
Line 64: 
Line 65: --- 페이지 166 ---
Line 66: choice, not an identiﬁer, so we’ll represent it with an enumeration PriceSource
Line 67: which we include in AuctionEventListener.1
Line 68: Incidentally, PriceSource is an example of a value type. We want code that
Line 69: describes the domain of Sniping—not, say, a boolean which we would have to
Line 70: interpret every time we read it; there’s more discussion in “Value Types”
Line 71: (page 59).
Line 72: public interface AuctionEventListener extends EventListener {
Line 73: enum PriceSource {
Line 74:     FromSniper, FromOtherBidder;
Line 75:   };
Line 76: […]
Line 77: We take the view that determining whether this is our price or not is part of
Line 78: the translator’s role. We extend currentPrice() with a new parameter and
Line 79: change the translator’s unit tests; note that we change the name of the existing
Line 80: test to include the extra feature. We also take the opportunity to pass the Sniper
Line 81: identiﬁer to the translator in SNIPER_ID. This ties the setup of the translator to
Line 82: the input message in the second test.
Line 83: public class AuctionMessageTranslatorTest { […]
Line 84:   private final AuctionMessageTranslator translator = 
Line 85:                     new AuctionMessageTranslator(SNIPER_ID, listener);
Line 86:   @Test public void
Line 87:   notifiesBidDetailsWhenCurrentPriceMessageReceivedFromOtherBidder() {
Line 88:     context.checking(new Expectations() {{
Line 89:       exactly(1).of(listener).currentPrice(192, 7, PriceSource.FromOtherBidder);
Line 90:     }});
Line 91:     Message message = new Message();
Line 92:     message.setBody(
Line 93: "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
Line 94:                    );
Line 95:     translator.processMessage(UNUSED_CHAT, message);
Line 96:   }
Line 97:   @Test public void
Line 98: notifiesBidDetailsWhenCurrentPriceMessageReceivedFromSniper() {
Line 99:     context.checking(new Expectations() {{
Line 100:       exactly(1).of(listener).currentPrice(234, 5, PriceSource.FromSniper);
Line 101:     }});
Line 102:     Message message = new Message();
Line 103:     message.setBody(
Line 104: "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: " 
Line 105:       + SNIPER_ID + ";");
Line 106:     translator.processMessage(UNUSED_CHAT, message);
Line 107:   }
Line 108: }
Line 109: 1. Some developers we know have an allergic reaction to nested types. In Java, we use
Line 110: them as a form of ﬁne-grained scoping. In this case, PriceSource is always used
Line 111: together with AuctionEventListener, so it makes sense to bind the two together.
Line 112: 141
Line 113: Who Knows about Bidders?
Line 114: 
Line 115: --- 페이지 167 ---
Line 116: The new test fails:
Line 117: unexpected invocation: 
Line 118:   auctionEventListener.currentPrice(<192>, <7>, <FromOtherBidder>)
Line 119: expectations:
Line 120: ! expected once, never invoked: 
Line 121:     auctionEventListener.currentPrice(<192>, <7>, <FromSniper>)
Line 122:       parameter 0 matched: <192>
Line 123:       parameter 1 matched: <7>
Line 124:       parameter 2 did not match: <FromSniper>, because was <FromOtherBidder>
Line 125: what happened before this: nothing!
Line 126: The ﬁx is to compare the Sniper identiﬁer to the bidder from the event message.
Line 127: public class AuctionMessageTranslator implements MessageListener {  […]
Line 128: private final String sniperId;
Line 129:   public void processMessage(Chat chat, Message message) {
Line 130: […]
Line 131:     } else if (EVENT_TYPE_PRICE.equals(type)) {
Line 132:       listener.currentPrice(event.currentPrice(), 
Line 133:                             event.increment(), 
Line 134: event.isFrom(sniperId));
Line 135:     }
Line 136:   }
Line 137:   public static class AuctionEvent { […]
Line 138: public PriceSource isFrom(String sniperId) {
Line 139:       return sniperId.equals(bidder()) ? FromSniper : FromOtherBidder;
Line 140:     }
Line 141:     private String bidder() { return get("Bidder"); }
Line 142:   }
Line 143: }
Line 144: The work we did in “Tidying Up the Translator” (page 135) to separate the
Line 145: different responsibilities within the translator has paid off here. All we had to
Line 146: do was add a couple of extra methods to AuctionEvent to get a very readable
Line 147: solution.
Line 148: Finally, to get all the code through the compiler, we ﬁx joinAuction() in Main
Line 149: to pass in the new constructor parameter for the translator. We can get a correctly
Line 150: structured identiﬁer from connection.
Line 151: private void joinAuction(XMPPConnection connection, String itemId) {
Line 152: […]
Line 153:   Auction auction = new XMPPAuction(chat);
Line 154:   chat.addMessageListener(
Line 155:       new AuctionMessageTranslator(
Line 156: connection.getUser(), 
Line 157:              new AuctionSniper(auction, new SniperStateDisplayer())));
Line 158:   auction.join();
Line 159: }
Line 160: Chapter 14
Line 161: The Sniper Wins the Auction
Line 162: 142
Line 163: 
Line 164: --- 페이지 168 ---
Line 165: The Sniper Has More to Say
Line 166: Our immediate end-to-end test failure tells us that we should make the user inter-
Line 167: face show when the Sniper is winning. Our next implementation step is to follow
Line 168: through by ﬁxing the AuctionSniper to interpret the isFromSniper parameter
Line 169: we’ve just added. Once again we start with a unit test.
Line 170: public class AuctionSniperTest { […]
Line 171:   @Test public void
Line 172: reportsIsWinningWhenCurrentPriceComesFromSniper() {
Line 173:     context.checking(new Expectations() {{
Line 174:       atLeast(1).of(sniperListener).sniperWinning();
Line 175:     }});
Line 176:     sniper.currentPrice(123, 45, PriceSource.FromSniper);
Line 177:   }
Line 178: }
Line 179: To get through the compiler, we add the new sniperWinning() method to
Line 180: SniperListener which, in turn, means that we add an empty implementation
Line 181: to SniperStateDisplayer.
Line 182: The test fails:
Line 183: unexpected invocation: auction.bid(<168>)
Line 184: expectations:
Line 185: ! expected at least 1 time, never invoked: sniperListener.sniperWinning()
Line 186: what happened before this: nothing!
Line 187: This failure is a nice example of trapping a method that we didn’t expect. We set
Line 188: no expectations on the auction, so calls to any of its methods will fail the test.
Line 189: If you compare this test to bidsHigherAndReportsBiddingWhenNewPriceArrives()
Line 190: in “The AuctionSniper Bids” (page 126) you’ll also see that we drop the price
Line 191: and increment variables and just feed in numbers. That’s because, in this test,
Line 192: there’s no calculation to do, so we don’t need to reference them in an expectation.
Line 193: They’re just details to get us to the interesting behavior.
Line 194: The ﬁx is straightforward:
Line 195: public class AuctionSniper implements AuctionEventListener { […]
Line 196:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 197: switch (priceSource) {
Line 198:     case FromSniper:
Line 199:       sniperListener.sniperWinning();
Line 200:       break;
Line 201:     case FromOtherBidder:
Line 202:       auction.bid(price + increment); 
Line 203:       sniperListener.sniperBidding();
Line 204:       break;
Line 205:     }
Line 206:   } 
Line 207: }
Line 208: 143
Line 209: The Sniper Has More to Say
Line 210: 
Line 211: --- 페이지 169 ---
Line 212: Running the end-to-end tests again shows that we’ve ﬁxed the failure that
Line 213: started this chapter (showing Bidding rather than Winning). Now we have to
Line 214: make the Sniper win:
Line 215: java.lang.AssertionError: 
Line 216: Tried to look for...
Line 217:   exactly 1 JLabel (with name "sniper status")
Line 218:   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 219:   in all top level windows
Line 220: and check that its label text is "Won"
Line 221: but...
Line 222:   all top level windows
Line 223:   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 224:   contained 1 JLabel (with name "sniper status")
Line 225: label text was "Lost"
Line 226: The Sniper Acquires Some State
Line 227: We’re about to introduce a step change in the complexity of the Sniper, if only
Line 228: a small one. When the auction closes, we want the Sniper to announce whether
Line 229: it has won or lost, which means that it must know whether it was bidding or
Line 230: winning at the time. This implies that the Sniper will have to maintain some state,
Line 231: which it hasn’t had to so far.
Line 232: To get to the functionality we want, we’ll start with the simpler cases where
Line 233: the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
Line 234: transitions, before adding the additional step that takes the Sniper to the Won state:
Line 235: Figure 14.2
Line 236: A Sniper bids, then loses
Line 237: Chapter 14
Line 238: The Sniper Wins the Auction
Line 239: 144
Line 240: 
Line 241: --- 페이지 170 ---
Line 242: We start by revisiting an existing unit test and adding a new one. These tests
Line 243: will pass with the current implementation; they’re there to ensure that we don’t
Line 244: break the behavior when we add further transitions.
Line 245: This introduces some new jMock syntax, states. The idea is to allow us to
Line 246: make assertions about the internal state of the object under test. We’ll come back
Line 247: to this idea in a moment.
Line 248: public class AuctionSniperTest { […]
Line 249:   private final States sniperState = context.states("sniper"); 1
Line 250:   @Test public void
Line 251:   reportsLostIfAuctionClosesImmediately() { 2
Line 252:     context.checking(new Expectations() {{
Line 253:       atLeast(1).of(sniperListener).sniperLost();
Line 254:     }});
Line 255:     sniper.auctionClosed();
Line 256:   }
Line 257:   @Test public void
Line 258: reportsLostIfAuctionClosesWhenBidding() {
Line 259:     context.checking(new Expectations() {{
Line 260:       ignoring(auction); 3
Line 261:       allowing(sniperListener).sniperBidding(); 
Line 262:                               then(sniperState.is("bidding")); 4
Line 263: atLeast(1).of(sniperListener).sniperLost(); 
Line 264:                               when(sniperState.is("bidding")); 5
Line 265:     }});
Line 266:     sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 6
Line 267:     sniper.auctionClosed();
Line 268:   }
Line 269: }
Line 270: 1
Line 271: We want to keep track of the Sniper’s current state, as signaled by the events
Line 272: it sends out, so we ask context for a placeholder. The default state is null.
Line 273: 2
Line 274: We keep our original test, but now it will apply where there are no price
Line 275: updates.
Line 276: 3
Line 277: The Sniper will call auction but we really don’t care about that in this test,
Line 278: so we tell the test to ignore this collaborator completely.
Line 279: 4
Line 280: When the Sniper sends out a bidding event, it’s telling us that it’s in a bidding
Line 281: state, which we record here. We use the allowing() clause to communicate
Line 282: that this is a supporting part of the test, not the part we really care about;
Line 283: see the note below.
Line 284: 5
Line 285: This is the phrase that matters, the expectation that we want to assert. If the
Line 286: Sniper isn’t bidding when it makes this call, the test will fail.
Line 287: 145
Line 288: The Sniper Acquires Some State
Line 289: 
Line 290: --- 페이지 171 ---
Line 291: 6
Line 292: This is our ﬁrst test where we need a sequence of events to get the Sniper
Line 293: into the state we want to test. We just call its methods in order.
Line 294: Allowances
Line 295: jMock distinguishes between allowed and expected invocations. An allowing()
Line 296: clause says that the object might make this call, but it doesn’t have to—unlike an
Line 297: expectation which will fail the test if the call isn’t made. We make the distinction to
Line 298: help express what is important in a test (the underlying implementation is actually
Line 299: the same): expectations are what we want to conﬁrm to have happened; allowances
Line 300: are supporting infrastructure that helps get the tested objects into the right state,
Line 301: or they’re side effects we don’t care about. We return to this topic in “Allowances
Line 302: and Expectations” (page 277) and we describe the API in Appendix A.
Line 303: Representing Object State
Line 304: In cases like this, we want to make assertions about an object’s behavior depending
Line 305: on its state, but we don’t want to break encapsulation by exposing how that state
Line 306: is implemented. Instead, the test can listen to the notiﬁcation events that the Sniper
Line 307: provides to tell interested collaborators about its state in their terms. jMock provides
Line 308: States objects, so that tests can record and make assertions about the state of
Line 309: an object when something signiﬁcant happens, i.e. when it calls its neighbors; see
Line 310: Appendix A for the syntax.
Line 311: This is a “logical” representation of what’s going on inside the object, in this case
Line 312: the Sniper. It allows the test to describe what it ﬁnds relevant about the Sniper, re-
Line 313: gardless of how the Sniper is actually implemented. As you’ll see shortly, this sep-
Line 314: aration will allow us to make radical changes to the implementation of the Sniper
Line 315: without changing the tests.
Line 316: The unit test name reportsLostIfAuctionClosesWhenBidding is very similar
Line 317: to the expectation it enforces:
Line 318: atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
Line 319: That’s not an accident. We put a lot of effort into ﬁguring out which abstractions
Line 320: jMock should support and developing a style that expresses the essential intent
Line 321: of a unit test.
Line 322: The Sniper Wins
Line 323: Finally, we can close the loop and have the Sniper win a bid. The next test
Line 324: introduces the Won event.
Line 325: Chapter 14
Line 326: The Sniper Wins the Auction
Line 327: 146
Line 328: 
Line 329: --- 페이지 172 ---
Line 330: @Test public void
Line 331: reportsWonIfAuctionClosesWhenWinning() {
Line 332:   context.checking(new Expectations() {{
Line 333:     ignoring(auction);
Line 334:     allowing(sniperListener).sniperWinning();  then(sniperState.is("winning"));
Line 335:     atLeast(1).of(sniperListener).sniperWon(); when(sniperState.is("winning"));
Line 336:   }});
Line 337:   sniper.currentPrice(123, 45, true);
Line 338:   sniper.auctionClosed();
Line 339: }
Line 340: It has the same structure but represents when the Sniper has won. The test fails
Line 341: because the Sniper called sniperLost().
Line 342: unexpected invocation: sniperListener.sniperLost()
Line 343: expectations:
Line 344:   allowed, never invoked: 
Line 345:     auction.<any method>(<any parameters>) was[]; 
Line 346:   allowed, already invoked 1 time: sniperListener.sniperWinning(); 
Line 347:                                      then sniper is winning
Line 348:   expected at least 1 time, never invoked: sniperListener.sniperWon();
Line 349:                                              when sniper is winning
Line 350: states:
Line 351:   sniper is winning
Line 352: what happened before this:
Line 353:   sniperListener.sniperWinning()
Line 354: We add a ﬂag to represent the Sniper’s state, and implement the new
Line 355: sniperWon() method in the SniperStateDisplayer.
Line 356: public class AuctionSniper implements AuctionEventListener { […]
Line 357: private boolean isWinning = false;
Line 358:   public void auctionClosed() {
Line 359: if (isWinning) {
Line 360:       sniperListener.sniperWon();
Line 361:     } else {
Line 362:       sniperListener.sniperLost();
Line 363:     }
Line 364:   }
Line 365:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 366: isWinning = priceSource == PriceSource.FromSniper;
Line 367:     if (isWinning) {
Line 368:       sniperListener.sniperWinning();
Line 369:     } else {
Line 370:       auction.bid(price + increment);
Line 371:       sniperListener.sniperBidding();
Line 372:     }
Line 373:   }
Line 374: }
Line 375: public class SniperStateDisplayer implements SniperListener { […]
Line 376:   public void sniperWon() {
Line 377:     showStatus(MainWindow.STATUS_WON);
Line 378:   }
Line 379: }
Line 380: 147
Line 381: The Sniper Wins
Line 382: 
Line 383: --- 페이지 173 ---
Line 384: Having previously made a fuss about PriceSource, are we being inconsistent
Line 385: here by using a boolean for isWinning? Our excuse is that we did try an enum
Line 386: for the Sniper state, but it just looked too complicated. The ﬁeld is private to
Line 387: AuctionSniper, which is small enough so it’s easy to change later and the code
Line 388: reads well.
Line 389: The unit and end-to-end tests all pass now, so we can cross off another item
Line 390: from the to-do list in Figure 14.3.
Line 391: Figure 14.3
Line 392: The Sniper wins
Line 393: There are more tests we could write—for example, to describe the transitions
Line 394: from bidding to winning and back again, but we’ll leave those as an exercise for
Line 395: you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
Line 396: functionality.
Line 397: Making Steady Progress
Line 398: As always, we made steady progress by adding little slices of functionality. First
Line 399: we made the Sniper show when it’s winning, then when it has won. We used
Line 400: empty implementations to get us through the compiler when we weren’t ready
Line 401: to ﬁll in the code, and we stayed focused on the immediate task.
Line 402: One of the pleasant surprises is that, now the code is growing a little, we’re
Line 403: starting to see some of our earlier effort pay off as new features just ﬁt into the
Line 404: existing structure. The next tasks we have to implement will shake this up.
Line 405: Chapter 14
Line 406: The Sniper Wins the Auction
Line 407: 148