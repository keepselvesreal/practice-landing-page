# 13.2 Sending a Bid (pp.126-131)

---
**Page 126**

developers shouldn’t be shy about creating new types. We think Main still does
too much, but we’re not yet sure how best to break it up. We decide to push on
and see where the code takes us.
Sending a Bid
An Auction Interface
The next step is to have the Sniper send a bid to the auction, so who should the
Sniper talk to? Extending the SniperListener feels wrong because that relationship
is about tracking what’s happening in the Sniper, not about making external
commitments. In the terms deﬁned in “Object Peer Stereotypes” (page 52),
SniperListener is a notiﬁcation, not a dependency.
After the usual discussion, we decide to introduce a new collaborator, an
Auction. Auction and SniperListener represent two different domains in the
application: Auction is about ﬁnancial transactions, it accepts bids for items in
the market; and SniperListener is about feedback to the application, it reports
changes to the current state of the Sniper. The Auction is a dependency, for a
Sniper cannot function without one, whereas the SniperListener, as we
discussed above, is not. Introducing the new interface makes the design look like
Figure 13.2.
Figure 13.2
Introducing Auction
The AuctionSniper Bids
Now we’re ready to start bidding. The ﬁrst step is to implement the response to
a Price event, so we start by adding a new unit test for the AuctionSniper. It
says that the Sniper, when it receives a Price update, sends an incremented bid
to the auction. It also notiﬁes its listener that it’s now bidding, so we add a
sniperBidding() method. We’re making an implicit assumption that the Auction
knows which bidder the Sniper represents, so the Sniper does not have to pass
in that information with the bid.
Chapter 13
The Sniper Makes a Bid
126


---
**Page 127**

public class AuctionSniperTest {
private final Auction auction = context.mock(Auction.class);
  private final AuctionSniper sniper = 
                    new AuctionSniper(auction, sniperListener);
[…]
  @Test public void
bidsHigherAndReportsBiddingWhenNewPriceArrives() {
    final int price = 1001;
    final int increment = 25;
    context.checking(new Expectations() {{
      one(auction).bid(price + increment);
      atLeast(1).of(sniperListener).sniperBidding();
    }});
    sniper.currentPrice(price, increment);
  }
}
The failure report is:
not all expectations were satisfied
expectations:
  ! expected once, never invoked: auction.bid(<1026>)
  ! expected at least 1 time, never invoked: sniperListener.sniperBidding()
what happened before this: nothing!
When writing the test, we realized that we don’t actually care if the Sniper
notiﬁes the listener more than once that it’s bidding; it’s just a status update,
so we use an atLeast(1) clause for the listener’s expectation. On the other hand,
we do care that we send a bid exactly once, so we use a one() clause for its ex-
pectation. In practice, of course, we’ll probably only call the listener once, but
this loosening of the conditions in the test expresses our intent about the two
relationships. The test says that the listener is a more forgiving collaborator, in
terms of how it’s called, than the Auction. We also retroﬁt the atLeast(1) clause
to the other test method.
How Should We Describe Expected Values?
We’ve speciﬁed the expected bid value by adding the price and increment.There
are different opinions about whether test values should just be literals with “obvious”
values, or expressed in terms of the calculation they represent. Writing out the
calculation may make the test more readable but risks reimplementing the target
code in the test, and in some cases the calculation will be too complicated to repro-
duce. Here, we decide that the calculation is so trivial that we can just write it into
the test.
127
Sending a Bid


---
**Page 128**

jMock Expectations Don’t Need to Be Matched in Order
This is our ﬁrst test with more than one expectation, so we’ll point out that the order
in which expectations are declared does not have to match the order in which the
methods are called in the code. If the calling order does matter, the expectations
should include a sequence clause, which is described in Appendix A.
The implementation to make the test pass is simple.
public interface Auction {
  void bid(int amount);
}
public class AuctionSniper implements AuctionEventListener {  […]
  private final SniperListener sniperListener;
private final Auction auction;
  public AuctionSniper(Auction auction, SniperListener sniperListener) {
this.auction = auction;
    this.sniperListener = sniperListener;
  }
  public void currentPrice(int price, int increment) {
    auction.bid(price + increment);
    sniperListener.sniperBidding();
  }
}
Successfully Bidding with the AuctionSniper
Now we have to fold our new AuctionSniper back into the application. The easy
part is displaying the bidding status, the (slightly) harder part is sending the bid
back to the auction. Our ﬁrst job is to get the code through the compiler. We
implement the new sniperBidding() method on Main and, to avoid having
code that doesn’t compile for too long, we pass the AuctionSniper a null
implementation of Auction.
Chapter 13
The Sniper Makes a Bid
128


---
**Page 129**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
Auction nullAuction = new Auction() {
      public void bid(int amount) {}
    };
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new AuctionMessageTranslator(new AuctionSniper(nullAuction, this)));
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  public void sniperBidding() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_BIDDING);
      }
    });
  }
}
So, what goes in the Auction implementation? It needs access to the chat so it
can send a bid message. To create the chat we need a translator, the translator
needs a Sniper, and the Sniper needs an auction. We have a dependency loop
which we need to break.
Looking again at our design, there are a couple of places we could intervene,
but it turns out that the ChatManager API is misleading. It does not require a
MessageListener to create a Chat, even though the createChat() methods imply
that it does. In our terms, the MessageListener is a notiﬁcation; we can pass in
null when we create the Chat and add a MessageListener later.
Expressing Intent in API
We were only able to discover that we could pass null as a MessageListener
because we have the source code to the Smack library. This isn’t clear from the
API because, presumably, the authors wanted to enforce the right behavior and
it’s not clear why anyone would want a Chat without a listener. An alternative would
have been to provide equivalent creation methods that don’t take a listener, but
that would lead to API bloat. There isn’t an obvious best approach here, except to
note that including well-structured source code with the distribution makes libraries
much easier to work with.
129
Sending a Bid


---
**Page 130**

Now we can restructure our connection code and use the Chat to send back
a bid.
public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), null);
    this.notToBeGCd = chat;
    Auction auction = new Auction() {
      public void bid(int amount) {
        try {
          chat.sendMessage(String.format(BID_COMMAND_FORMAT, amount));
        } catch (XMPPException e) {
          e.printStackTrace();
        }
      }
    };
    chat.addMessageListener(
           new AuctionMessageTranslator(new AuctionSniper(auction, this)));
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
}
Null Implementation
A null implementation is similar to a null object [Woolf98]: both are implementations
that respond to a protocol by not doing anything—but the intention is different. A
null object is usually one implementation amongst many, introduced to reduce
complexity in the code that calls the protocol. We deﬁne a null implementation as
a temporary empty implementation, introduced to allow the programmer to make
progress by deferring effort and intended to be replaced.
The End-to-End Tests Pass
Now the end-to-end tests pass: the Sniper can lose without making a bid, and
lose after making a bid. We can cross off another item on the to-do list, but that
includes just catching and printing the XMPPException. Normally, we regard this
as a very bad practice but we wanted to see the tests pass and get some structure
into the code—and we know that the end-to-end tests will fail anyway if there’s
a problem sending a message. To make sure we don’t forget, we add another
to-do item to ﬁnd a better solution, Figure 13.3.
Chapter 13
The Sniper Makes a Bid
130


---
**Page 131**

Figure 13.3
One step forward
Tidying Up the Implementation
Extracting XMPPAuction
Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
tation feels messy. We notice that the activity in joinAuction() crosses multiple
domains: managing chats, sending bids, creating snipers, and so on. We need to
clean up. To start, we notice that we’re sending auction commands from two
different levels, at the top and from within the Auction. Sending commands to
an auction sounds like the sort of thing that our Auction object should do, so it
makes sense to package that up together. We add a new method to the interface,
extend our anonymous implementation, and then extract it to a (temporarily)
nested class—for which we need a name. The distinguishing feature of this imple-
mentation of Auction is that it’s based on the messaging infrastructure, so we
call our new class XMPPAuction.
131
Tidying Up the Implementation


