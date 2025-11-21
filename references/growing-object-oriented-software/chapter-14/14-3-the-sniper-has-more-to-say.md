# 14.3 The Sniper Has More to Say (pp.143-144)

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


---
**Page 144**

Running the end-to-end tests again shows that we’ve ﬁxed the failure that
started this chapter (showing Bidding rather than Winning). Now we have to
make the Sniper win:
java.lang.AssertionError: 
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Won"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Lost"
The Sniper Acquires Some State
We’re about to introduce a step change in the complexity of the Sniper, if only
a small one. When the auction closes, we want the Sniper to announce whether
it has won or lost, which means that it must know whether it was bidding or
winning at the time. This implies that the Sniper will have to maintain some state,
which it hasn’t had to so far.
To get to the functionality we want, we’ll start with the simpler cases where
the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
transitions, before adding the additional step that takes the Sniper to the Won state:
Figure 14.2
A Sniper bids, then loses
Chapter 14
The Sniper Wins the Auction
144


