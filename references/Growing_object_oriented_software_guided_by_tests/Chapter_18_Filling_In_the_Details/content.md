Line 1: 
Line 2: --- 페이지 230 ---
Line 3: Chapter 18
Line 4: Filling In the Details
Line 5: In which we introduce a stop price so we don’t bid inﬁnitely, which
Line 6: means we can now be losing an auction that hasn’t yet closed. We add
Line 7: a new ﬁeld to the user interface and push it through to the Sniper. We
Line 8: realize we should have created an Item type much earlier.
Line 9: A More Useful Application
Line 10: So far the functionality has been prioritized to attract potential customers by
Line 11: giving them a sense of what the application will look like. We can show items
Line 12: being added and some features of sniping. It’s not a very useful application be-
Line 13: cause, amongst other things, there’s no upper limit for bidding on an item—it
Line 14: could be very expensive to deploy.
Line 15: This is a common pattern when using Agile Development techniques to work
Line 16: on a new project. The team is ﬂexible enough to respond to how the needs of
Line 17: the sponsors change over time: at the beginning, the emphasis might be on
Line 18: proving the concept to attract enough support to continue; later, the emphasis
Line 19: might be on implementing enough functionality to be ready to deploy; later still,
Line 20: the emphasis might change to providing more options to support a wider range
Line 21: of users.
Line 22: This dynamic is very different from both a ﬁxed design approach, where the
Line 23: structure of the development has to be approved before work can begin, and a
Line 24: code-and-ﬁx approach, where the system might be initially successful but not
Line 25: resilient enough to adapt to its changing role.
Line 26: Stop When We’ve Had Enough
Line 27: Our next most pressing task (especially after recent crises in the ﬁnancial markets)
Line 28: is to be able to set an upper limit, the “stop price,” for our bid for an item.
Line 29: Introducing a Losing State
Line 30: With the introduction of a stop price, it’s possible for a Sniper to be losing before
Line 31: the auction has closed. We could implement this by just marking the Sniper as
Line 32: Lost when it hits its stop price, but the users want to know the ﬁnal price when
Line 33: the auction has ﬁnished after they’ve dropped out, so we model this as an extra
Line 34: state. Once a Sniper has been outbid at its stop price, it will never be able to win,
Line 35: 205
Line 36: 
Line 37: --- 페이지 231 ---
Line 38: so the only option left is to wait for the auction to close, accepting updates of
Line 39: any new (higher) prices from other bidders.
Line 40: We adapt the state machine we drew in Figure 9.3 to include the new
Line 41: transitions. The result is Figure 18.1.
Line 42: Figure 18.1
Line 43: A bidder may now be losing
Line 44: The First Failing Test
Line 45: Of course we start with a failing test. We won’t go through all the cases here,
Line 46: but this example will take us through the essentials. First, we write an end-to-
Line 47: end test to describe the new feature. It shows a scenario where our Sniper bids
Line 48: for an item but loses because it bumps into its stop price, and other bidders
Line 49: continue until the auction closes.
Line 50: @Test public void sniperLosesAnAuctionWhenThePriceIsTooHigh() throws Exception {
Line 51:   auction.startSellingItem();
Line 52: application.startBiddingWithStopPrice(auction, 1100);
Line 53:   auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID); 
Line 54:   auction.reportPrice(1000, 98, "other bidder"); 
Line 55:   application.hasShownSniperIsBidding(auction, 1000, 1098);
Line 56:   auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line 57:   auction.reportPrice(1197, 10, "third party");
Line 58: application.hasShownSniperIsLosing(auction, 1197, 1098);
Line 59:   auction.reportPrice(1207, 10, "fourth party");
Line 60: application.hasShownSniperIsLosing(auction, 1207, 1098);
Line 61:   auction.announceClosed();
Line 62:   application.showsSniperHasLostAuction(auction, 1207, 1098); 
Line 63: }
Line 64: Chapter 18
Line 65: Filling In the Details
Line 66: 206
Line 67: 
Line 68: --- 페이지 232 ---
Line 69: This test introduces two new methods into our test infrastructure, which we
Line 70: need to ﬁll in to get through the compiler. First, startBiddingWithStopPrice()
Line 71: passes the new stop price value through the ApplicationRunner to the
Line 72: AuctionSniperDriver.
Line 73: public class AuctionSniperDriver extends JFrameDriver {
Line 74:   public void startBiddingFor(String itemId, int stopPrice) {
Line 75:     textField(NEW_ITEM_ID_NAME).replaceAllText(itemId); 
Line 76: textField(NEW_ITEM_STOP_PRICE_NAME).replaceAllText(String.valueOf(stopPrice));
Line 77:     bidButton().click(); 
Line 78:   }
Line 79: […]
Line 80: }
Line 81: This implies that we need a new input ﬁeld in the user interface for the stop price,
Line 82: so we create a constant to identify it in MainWindow (we’ll ﬁll in the component
Line 83: itself soon). We also need to support our existing tests which do not have a stop
Line 84: price, so we change them to use Integer.MAX_VALUE to represent no stop price
Line 85: at all.
Line 86: The other new method in ApplicationRunner is hasShownSniperIsLosing(),
Line 87: which is the same as the other checking methods, except that it uses a new Losing
Line 88: value in SniperState:
Line 89: public enum SniperState {
Line 90: LOSING {
Line 91:     @Override public SniperState whenAuctionClosed() { return LOST; }
Line 92:   }, […]
Line 93: and, to complete the loop, we add a value to the display text in
Line 94: SnipersTableModel:
Line 95: private final static String[] STATUS_TEXT = {
Line 96:   "Joining", "Bidding", "Winning", "Losing", "Lost", "Won" 
Line 97: };
Line 98: The failure message says that we have no stop price ﬁeld:
Line 99: […] but...
Line 100:   all top level windows
Line 101:   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 102: contained 0 JTextField (with name "stop price")
Line 103: Now we have a failing end-to-end test that describes our intentions for the
Line 104: feature, so we can implement it.
Line 105: Typing In the Stop Price
Line 106: To make any progress, we must add a component to the user interface that will
Line 107: accept a stop price. Our current design, which we saw in Figure 16.2, has only
Line 108: a ﬁeld for the item identiﬁer but we can easily adjust it to take a stop price in the
Line 109: top bar.
Line 110: 207
Line 111: Stop When We’ve Had Enough
Line 112: 
Line 113: --- 페이지 233 ---
Line 114: For our implementation, we will add a JFormattedTextField for the stop price
Line 115: that is constrained to accept only integer values, and a couple of labels. The new
Line 116: top bar looks like Figure 18.2.
Line 117: Figure 18.2
Line 118: The Sniper with a stop price ﬁeld in its bar
Line 119: We get the test failure we expect, which is that the Sniper is not losing because
Line 120: it continues to bid:
Line 121: […] but...
Line 122:     all top level windows
Line 123:     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line 124:     contained 1 JTable ()
Line 125:    it is not table with row with cells 
Line 126:      <label with text "item-54321">, <label with text "1098">, 
Line 127:      <label with text "1197">, <label with text "Losing">
Line 128:     because 
Line 129: in row 0: component 1 text was "1197"
Line 130: Propagating the Stop Price
Line 131: To make this feature work, we need to pass the stop price from the user interface
Line 132: to the AuctionSniper, which can then use it to limit further bidding. The chain
Line 133: starts when MainWindow notiﬁes its UserRequestListener using:
Line 134: void joinAuction(String itemId);
Line 135: The obvious thing to do is to add a stopPrice argument to this method and to
Line 136: the rest of the chain of calls, until it reaches the AuctionSniper class. We want
Line 137: to make a point here, so we’ll force a slightly different approach to propagating
Line 138: the new value.
Line 139: Another way to look at it is that the user interface constructs a description of
Line 140: the user’s “policy” for the Sniper’s bidding on an item. So far this has only in-
Line 141: cluded the item’s identiﬁer (“bid on this item”), but now we’re adding a stop
Line 142: price (“bid up to this amount on this item”) so there’s more structure.
Line 143: Chapter 18
Line 144: Filling In the Details
Line 145: 208
Line 146: 
Line 147: --- 페이지 234 ---
Line 148: We want to make this structure explicit, so we create a new class, Item. We
Line 149: start with a simple value that just carries the identiﬁer and stop price as public
Line 150: immutable ﬁelds; we can move behavior into it later.
Line 151: public class Item {
Line 152:   public final String identifier;
Line 153:   public final int stopPrice;
Line 154:   public Item(String identifier, int stopPrice) { 
Line 155:     this.identifier = identifier;
Line 156:     this.stopPrice = stopPrice; 
Line 157:   }
Line 158: // also equals(), hashCode(), toString()
Line 159: } 
Line 160: Introducing the Item class is an example of budding off that we described in
Line 161: “Value Types” (page 59). It’s a placeholder type that we use to identify a concept
Line 162: and that gives us somewhere to attach relevant new features as the code grows.
Line 163: We push Item into the code and see what breaks, starting with
Line 164: UserRequestListener:
Line 165: public interface UserRequestListener extends EventListener {
Line 166:   void joinAuction(Item item);
Line 167: }
Line 168: First we ﬁx MainWindowTest, the integration test we wrote for the Swing imple-
Line 169: mentation in Chapter 16. The language is already beginning to shift. In the pre-
Line 170: vious version of this test, the probe variable was called buttonProbe, which
Line 171: describes the structure of the user interface. That doesn’t make sense any more,
Line 172: so we’ve renamed it itemProbe, which describes a collaboration between
Line 173: MainWindow and its neighbors.
Line 174: @Test public void 
Line 175: makesUserRequestWhenJoinButtonClicked() { 
Line 176:   final ValueMatcherProbe<Item> itemProbe = 
Line 177:     new ValueMatcherProbe<Item>(equalTo(new Item("an item-id", 789)), "item request");
Line 178:   mainWindow.addUserRequestListener( 
Line 179:       new UserRequestListener() { 
Line 180:         public void joinAuction(Item item) { 
Line 181: itemProbe.setReceivedValue(item); 
Line 182:         } 
Line 183:       }); 
Line 184:   driver.startBiddingFor("an item-id", 789);
Line 185:   driver.check(itemProbe); 
Line 186: }
Line 187: We make this test pass by extracting the stop price value within MainWindow.
Line 188: 209
Line 189: Stop When We’ve Had Enough
Line 190: 
Line 191: --- 페이지 235 ---
Line 192: joinAuctionButton.addActionListener(new ActionListener() { 
Line 193:   public void actionPerformed(ActionEvent e) { 
Line 194:     userRequests.announce().joinAuction(new Item(itemId(), stopPrice())); 
Line 195:   } 
Line 196:   private String itemId() {
Line 197:     return itemIdField.getText();
Line 198:   }
Line 199:   private int stopPrice() { 
Line 200:     return ((Number)stopPriceField.getValue()).intValue(); 
Line 201:   } 
Line 202: });
Line 203: This pushes Item into SniperLauncher which, in turn, pushes it through to its
Line 204: dependent types such as AuctionHouse and AuctionSniper. We ﬁx the compilation
Line 205: errors and make all the tests pass again—except for the outstanding end-to-end
Line 206: test which we have yet to implement.
Line 207: We’ve now made explicit another concept in the domain. We realize that an
Line 208: item’s identiﬁer is only one part of how a user bids in an auction. Now the code
Line 209: can tell us exactly where decisions are made about bidding choices, so we don’t
Line 210: have to follow a chain of method calls to see which strings are relevant.
Line 211: Restraining the AuctionSniper
Line 212: The last step to ﬁnish the task is to make the AuctionSniper observe the stop
Line 213: price we’ve just passed to it and stop bidding. In practice, we can ensure that
Line 214: we’ve covered everything by writing unit tests for each of the new state transitions
Line 215: drawn in Figure 18.1. Our ﬁrst test triggers the Sniper to start bidding and then
Line 216: announces a bid outside its limit—the stop price is set to 1234. We’ve also
Line 217: extracted a common expectation into a helper method.1
Line 218: @Test public void
Line 219: doesNotBidAndReportsLosingIfSubsequentPriceIsAboveStopPrice() {
Line 220:   allowingSniperBidding();
Line 221:   context.checking(new Expectations() {{
Line 222:     int bid = 123 + 45;
Line 223:     allowing(auction).bid(bid);
Line 224:     atLeast(1).of(sniperListener).sniperStateChanged(
Line 225:                     new SniperSnapshot(ITEM_ID, 2345, bid, LOSING)); 
Line 226:                                         when(sniperState.is("bidding"));
Line 227:   }});
Line 228:   sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);
Line 229:   sniper.currentPrice(2345, 25, PriceSource.FromOtherBidder);
Line 230: }
Line 231: private void allowingSniperBidding() {
Line 232:   context.checking(new Expectations() {{ 
Line 233:     allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
Line 234:                                               then(sniperState.is("bidding"));
Line 235:   }});
Line 236: } 
Line 237: 1. jMock allows checking() to be called multiple times within a test.
Line 238: Chapter 18
Line 239: Filling In the Details
Line 240: 210
Line 241: 
Line 242: --- 페이지 236 ---
Line 243: Distinguishing between Test Setup and Assertions
Line 244: Once again we’re using the allowing clause to distinguish between the test setup
Line 245: (getting the AuctionSniper into the right state) and the signiﬁcant test assertion
Line 246: (that the AuctionSniper is now losing). We’re very picky about this kind of
Line 247: expressiveness because we’ve found it’s the only way for the tests to remain
Line 248: meaningful, and therefore useful, over time.We return to this at length in Chapter 21
Line 249: and Chapter 24.
Line 250: The other tests are similar:
Line 251: doesNotBidAndReportsLosingIfFirstPriceIsAboveStopPrice()
Line 252: reportsLostIfAuctionClosesWhenLosing()
Line 253: continuesToBeLosingOnceStopPriceHasBeenReached()
Line 254: doesNotBidAndReportsLosingIfPriceAfterWinningIsAboveStopPrice()
Line 255: We change AuctionSniper, with supporting features in SniperSnapshot and
Line 256: Item, to make the test pass:
Line 257: public class AuctionSniper { […]
Line 258:   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line 259:     switch(priceSource) {
Line 260:     case FromSniper:
Line 261:       snapshot = snapshot.winning(price); 
Line 262:       break;
Line 263:     case FromOtherBidder:
Line 264:       int bid = price + increment;
Line 265:       if (item.allowsBid(bid)) {
Line 266:         auction.bid(bid);
Line 267:         snapshot = snapshot.bidding(price, bid);
Line 268: } else {
Line 269:         snapshot = snapshot.losing(price);
Line 270:       }
Line 271:       break;
Line 272:     }
Line 273:     notifyChange();
Line 274:   } […]
Line 275: public class SniperSnapshot { […]
Line 276:   public SniperSnapshot losing(int newLastPrice) {
Line 277:     return new SniperSnapshot(itemId, newLastPrice, lastBid, LOSING);
Line 278:   } […]
Line 279: public class Item { […]
Line 280:   public boolean allowsBid(int bid) {
Line 281:     return bid <= stopPrice;
Line 282:   } […]
Line 283: The end-to-end tests pass and we can cross the feature off our list, Figure 18.3.
Line 284: 211
Line 285: Stop When We’ve Had Enough
Line 286: 
Line 287: --- 페이지 237 ---
Line 288: Figure 18.3
Line 289: The Sniper stops bidding at the stop price
Line 290: Observations
Line 291: User Interfaces, Incrementally
Line 292: It looks like we’re making signiﬁcant changes again to the user interface at a late
Line 293: stage in our development. Shouldn’t we have seen this coming? This is an active
Line 294: topic for discussion in the Agile User Experience community and, as always, the
Line 295: answer is “it depends, but you have more ﬂexibility than you might think.”
Line 296: In truth, for a simple application like this it would make sense to work out the
Line 297: user interface in more detail at the start, to make sure it’s usable and coherent.
Line 298: That said, we also wanted to make a point that we can respond to changing
Line 299: needs, especially if we structure our tests and code so that they’re ﬂexible, not a
Line 300: dead weight. We all know that requirements will change, especially once we put
Line 301: our application into production, so we should be able to respond.
Line 302: Other Modeling Techniques Still Work
Line 303: Some presentations of TDD appear to suggest that it supersedes all previous
Line 304: software design techniques. We think TDD works best when it’s based on skill
Line 305: and judgment acquired from as wide an experience as possible—which includes
Line 306: taking advantage of older techniques and formats (we hope we’re not being too
Line 307: controversial here).
Line 308: State transition diagrams are one example of taking another view. We regularly
Line 309: come across teams that have never quite ﬁgured out what the valid states and
Line 310: transitions are for key concepts in their domain, and applying this simple
Line 311: Chapter 18
Line 312: Filling In the Details
Line 313: 212
Line 314: 
Line 315: --- 페이지 238 ---
Line 316: formalism often means we can clean up a lucky-dip of snippets of behavior
Line 317: scattered across the code. What’s nice about state transitions diagrams is that
Line 318: they map directly onto tests, so we can show that we’ve covered all the
Line 319: possibilities.
Line 320: The trick is to understand and use other modeling techniques for support and
Line 321: guidance, not as an end in themselves—which is how they got a bad name in the
Line 322: ﬁrst place. When we’re doing TDD and we’re uncertain what to do, sometimes
Line 323: stepping back and opening a pack of index cards, or sketching out the interactions,
Line 324: can help us regain direction.
Line 325: Domain Types Are Better Than Strings
Line 326: The string is a stark data structure and everywhere it is passed there
Line 327: is much duplication of process. It is a perfect vehicle for hiding
Line 328: information.
Line 329: —Alan Perlis
Line 330: Looking back, we wish we’d created the Item type earlier, probably when we
Line 331: extracted UserRequestListener, instead of just using a String to represent the
Line 332: thing a Sniper bids for. Had we done so, we could have added the stop price to
Line 333: the existing Item class, and it would have been delivered, by deﬁnition, to where
Line 334: it was needed.
Line 335: We might also have noticed sooner that we do not want to index our table on
Line 336: item identiﬁer but on an Item, which would open up the possibility of trying
Line 337: multiple policies in a single auction. We’re not saying that we should have de-
Line 338: signed more speculatively for a need that hasn’t been proved. Rather, when we
Line 339: take the trouble to express the domain clearly, we often ﬁnd that we have more
Line 340: options.
Line 341: It’s often better to deﬁne domain types to wrap not only Strings but other
Line 342: built-in types too, including collections. All we have to do is remember to apply
Line 343: our own advice. As you see, sometimes we forget.
Line 344: 213
Line 345: Observations
Line 346: 
Line 347: --- 페이지 239 ---
Line 348: This page intentionally left blank 