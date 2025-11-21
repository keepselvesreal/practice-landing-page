# 14.1 First, a Failing Test (pp.139-140)

---
**Page 139**

Chapter 14
The Sniper Wins the Auction
In which we add another feature to our Sniper and let it win an auction.
We introduce the concept of state to the Sniper which we test by listen-
ing to its callbacks. We ﬁnd that even this early, one of our refactorings
has paid off.
First, a Failing Test
We have a Sniper that can respond to price changes by bidding more, but it
doesn’t yet know when it’s successful. Our next feature on the to-do list is to
win an auction. This involves an extra state transition, as you can see in
Figure 14.1:
Figure 14.1
A sniper bids, then wins
To represent this, we add an end-to-end test based on sniperMakesAHigherBid-
ButLoses() with a different conclusion—sniperWinsAnAuctionByBiddingHigher().
Here’s the test, with the new features highlighted:
139


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


