# 14.2 Who Knows about Bidders? (pp.140-143)

---
**Page 140**

public class AuctionSniperEndToEndTest { […]
  @Test public void
sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding();
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning();
    auction.announceClosed();
    application.showsSniperHasWonAuction();
  }
}
In our test infrastructure we add the two methods to check that the user interface
shows the two new states to the ApplicationRunner.
This generates a new failure message:
java.lang.AssertionError: 
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Winning"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Bidding"
Now we know where we’re going, we can implement the feature.
Who Knows about Bidders?
The application knows that the Sniper is winning if it’s the bidder for the last
price that the auction accepted. We have to decide where to put that logic.
Looking again at Figure 13.5 on page 134, one choice would be that the translator
could pass the bidder through to the Sniper and let the Sniper decide. That would
mean that the Sniper would have to know something about how bidders are
identiﬁed by the auction, with a risk of pulling in XMPP details that we’ve been
careful to keep separate. To decide whether it’s winning, the only thing the Sniper
needs to know when a price arrives is, did this price come from me? This is a
Chapter 14
The Sniper Wins the Auction
140


---
**Page 141**

choice, not an identiﬁer, so we’ll represent it with an enumeration PriceSource
which we include in AuctionEventListener.1
Incidentally, PriceSource is an example of a value type. We want code that
describes the domain of Sniping—not, say, a boolean which we would have to
interpret every time we read it; there’s more discussion in “Value Types”
(page 59).
public interface AuctionEventListener extends EventListener {
enum PriceSource {
    FromSniper, FromOtherBidder;
  };
[…]
We take the view that determining whether this is our price or not is part of
the translator’s role. We extend currentPrice() with a new parameter and
change the translator’s unit tests; note that we change the name of the existing
test to include the extra feature. We also take the opportunity to pass the Sniper
identiﬁer to the translator in SNIPER_ID. This ties the setup of the translator to
the input message in the second test.
public class AuctionMessageTranslatorTest { […]
  private final AuctionMessageTranslator translator = 
                    new AuctionMessageTranslator(SNIPER_ID, listener);
  @Test public void
  notifiesBidDetailsWhenCurrentPriceMessageReceivedFromOtherBidder() {
    context.checking(new Expectations() {{
      exactly(1).of(listener).currentPrice(192, 7, PriceSource.FromOtherBidder);
    }});
    Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
                   );
    translator.processMessage(UNUSED_CHAT, message);
  }
  @Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceivedFromSniper() {
    context.checking(new Expectations() {{
      exactly(1).of(listener).currentPrice(234, 5, PriceSource.FromSniper);
    }});
    Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: " 
      + SNIPER_ID + ";");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
1. Some developers we know have an allergic reaction to nested types. In Java, we use
them as a form of ﬁne-grained scoping. In this case, PriceSource is always used
together with AuctionEventListener, so it makes sense to bind the two together.
141
Who Knows about Bidders?


---
**Page 142**

The new test fails:
unexpected invocation: 
  auctionEventListener.currentPrice(<192>, <7>, <FromOtherBidder>)
expectations:
! expected once, never invoked: 
    auctionEventListener.currentPrice(<192>, <7>, <FromSniper>)
      parameter 0 matched: <192>
      parameter 1 matched: <7>
      parameter 2 did not match: <FromSniper>, because was <FromOtherBidder>
what happened before this: nothing!
The ﬁx is to compare the Sniper identiﬁer to the bidder from the event message.
public class AuctionMessageTranslator implements MessageListener {  […]
private final String sniperId;
  public void processMessage(Chat chat, Message message) {
[…]
    } else if (EVENT_TYPE_PRICE.equals(type)) {
      listener.currentPrice(event.currentPrice(), 
                            event.increment(), 
event.isFrom(sniperId));
    }
  }
  public static class AuctionEvent { […]
public PriceSource isFrom(String sniperId) {
      return sniperId.equals(bidder()) ? FromSniper : FromOtherBidder;
    }
    private String bidder() { return get("Bidder"); }
  }
}
The work we did in “Tidying Up the Translator” (page 135) to separate the
different responsibilities within the translator has paid off here. All we had to
do was add a couple of extra methods to AuctionEvent to get a very readable
solution.
Finally, to get all the code through the compiler, we ﬁx joinAuction() in Main
to pass in the new constructor parameter for the translator. We can get a correctly
structured identiﬁer from connection.
private void joinAuction(XMPPConnection connection, String itemId) {
[…]
  Auction auction = new XMPPAuction(chat);
  chat.addMessageListener(
      new AuctionMessageTranslator(
connection.getUser(), 
             new AuctionSniper(auction, new SniperStateDisplayer())));
  auction.join();
}
Chapter 14
The Sniper Wins the Auction
142


---
**Page 143**

The Sniper Has More to Say
Our immediate end-to-end test failure tells us that we should make the user inter-
face show when the Sniper is winning. Our next implementation step is to follow
through by ﬁxing the AuctionSniper to interpret the isFromSniper parameter
we’ve just added. Once again we start with a unit test.
public class AuctionSniperTest { […]
  @Test public void
reportsIsWinningWhenCurrentPriceComesFromSniper() {
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperWinning();
    }});
    sniper.currentPrice(123, 45, PriceSource.FromSniper);
  }
}
To get through the compiler, we add the new sniperWinning() method to
SniperListener which, in turn, means that we add an empty implementation
to SniperStateDisplayer.
The test fails:
unexpected invocation: auction.bid(<168>)
expectations:
! expected at least 1 time, never invoked: sniperListener.sniperWinning()
what happened before this: nothing!
This failure is a nice example of trapping a method that we didn’t expect. We set
no expectations on the auction, so calls to any of its methods will fail the test.
If you compare this test to bidsHigherAndReportsBiddingWhenNewPriceArrives()
in “The AuctionSniper Bids” (page 126) you’ll also see that we drop the price
and increment variables and just feed in numbers. That’s because, in this test,
there’s no calculation to do, so we don’t need to reference them in an expectation.
They’re just details to get us to the interesting behavior.
The ﬁx is straightforward:
public class AuctionSniper implements AuctionEventListener { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
switch (priceSource) {
    case FromSniper:
      sniperListener.sniperWinning();
      break;
    case FromOtherBidder:
      auction.bid(price + increment); 
      sniperListener.sniperBidding();
      break;
    }
  } 
}
143
The Sniper Has More to Say


