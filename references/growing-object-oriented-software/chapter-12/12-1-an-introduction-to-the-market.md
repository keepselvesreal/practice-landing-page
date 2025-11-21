# 12.1 An Introduction to the Market (pp.105-106)

---
**Page 105**

Chapter 12
Getting Ready to Bid
In which we write an end-to-end test so that we can make the Sniper
bid in an auction. We start to interpret the messages in the auction
protocol and discover some new classes in the process. We write our
ﬁrst unit tests and then refactor out a helper class. We describe every
last detail of this effort to show what we were thinking at the time.
An Introduction to the Market
Now, to continue with the skeleton metaphor, we start to ﬂesh out the application.
The core behavior of a Sniper is that it makes a higher bid on an item in an auction
when there’s a change in price. Going back to our to-do list, we revisit the next
couple of items:
•
Single item: join, bid, and lose. When a price comes in, send a bid raised
by the minimum increment deﬁned by the auction. This amount will be
included in the price update information.
•
Single item: join, bid, and win. Distinguish which bidder is currently winning
the auction and don’t bid against ourselves.
We know there’ll be more coming, but this is a coherent slice of functionality
that will allow us to explore the design and show concrete progress.
In any distributed system similar to this one there are lots of interesting failure
and timing issues, but our application only has to deal with the client side of the
protocol. We rely on the underlying XMPP protocol to deal with many common
distributed programming problems; in particular, we expect it to ensure that
messages between a bidder and an auction arrive in the same order in which they
were sent.
As we described in Chapter 5, we start the next feature with an acceptance
test. We used our ﬁrst test in the previous chapter to help ﬂush out the structure
of our application. From now on, we can use acceptance tests to show incremental
progress.
105


---
**Page 106**

A Test for Bidding
Starting with a Test
Each acceptance test we write should have just enough new requirements to force
a manageable increase in functionality, so we decide that the next one will add
some price information. The steps are:
1.
Tell the auction to send a price to the Sniper.
2.
Check the Sniper has received and responded to the price.
3.
Check the auction has received an incremented bid from Sniper.
To make this pass, the Sniper will have to distinguish between Price and Close
events from the auction, display the current price, and generate a new bid. We’ll
also have to extend our stub auction to handle bids. We’ve deferred implementing
other functionality that will also be required, such as displaying when the Sniper
has won the auction; we’ll get to that later. Here’s the new test:
public class AuctionSniperEndToEndTest {
  @Test public void
sniperMakesAHigherBidButLoses() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFromSniper(); 1
    auction.reportPrice(1000, 98, "other bidder"); 2
    application.hasShownSniperIsBidding(); 3
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID); 4
    auction.announceClosed(); 5
    application.showsSniperHasLostAuction();   
  }
}
We have three new methods to implement as part of this test.
1
We have to wait for the stub auction to receive the Join request before con-
tinuing with the test. We use this assertion to synchronize the Sniper with
the auction.
2
This method tells the stub auction to send a message back to the Sniper with
the news that at the moment the price of the item is 1000, the increment for
the next bid is 98, and the winning bidder is “other bidder.”
3
This method asks the ApplicationRunner to check that the Sniper shows that
it’s now bidding after it’s received the price update message from the auction.
Chapter 12
Getting Ready to Bid
106


