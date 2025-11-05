# 13.1 Introducing AuctionSniper (pp.123-126)

---
**Page 123**

Chapter 13
The Sniper Makes a Bid
In which we extract an AuctionSniper class and tease out its dependen-
cies. We plug our new class into the rest of the application, using an
empty implementation of auction until we’re ready to start sending
commands. We close the loop back to the auction house with an
XMPPAuction class. We continue to carve new types out of the code.
Introducing AuctionSniper
A New Class, with Dependencies
Our application accepts Price events from the auction, but cannot interpret them
yet. We need code that will perform two actions when the currentPrice() method
is called: send a higher bid to the auction and update the status in the user inter-
face. We could extend Main, but that class is looking rather messy—it’s already
doing too many things at once. It feels like this is a good time to introduce
what we should call an “Auction Sniper,” the component at the heart of our
application, so we create an AuctionSniper class. Some of its intended behavior
is currently buried in Main, and a good start would be to extract it into our new
class—although, as we’ll see in a moment, it will take a little effort.
Given that an AuctionSniper should respond to Price events, we decide to
make it implement AuctionEventListener rather than Main. The question is what
to do about the user interface. If we consider moving this method:
public void auctionClosed() {
  SwingUtilities.invokeLater(new Runnable() {
    public void run() {
       ui.showStatus(MainWindow.STATUS_LOST);
    }
  });
}
does it really make sense for an AuctionSniper to know about the implementation
details of the user interface, such as the use of the Swing thread? We’d be at risk
of breaking the “single responsibility” principle again. Surely an AuctionSniper
ought to be concerned with bidding policy and only notify status changes in
its terms?
123


---
**Page 124**

Our solution is to insulate the AuctionSniper by introducing a new relationship:
it will notify a SniperListener of changes in its status. The interface and the ﬁrst
unit test look like this:
public interface SniperListener extends EventListener {
  void sniperLost();
}
@RunWith(JMock.class)
public class AuctionSniperTest {
  private final Mockery context = new Mockery();
  private final SniperListener sniperListener = 
                                      context.mock(SniperListener.class);
  private final AuctionSniper sniper = new AuctionSniper(sniperListener);
  @Test public void
reportsLostWhenAuctionCloses() {
    context.checking(new Expectations() {{
      one(sniperListener).sniperLost();
    }});
    sniper.auctionClosed();
  }
}
which says that Sniper should report that it has lost if it receives a Close event
from the auction.
The failure report says:
not all expectations were satisfied
expectations:
! expected exactly 1 time, never invoked: SniperListener.sniperLost();
which we can make pass with a simple implementation:
public class AuctionSniper implements AuctionEventListener {
  private final SniperListener sniperListener;
  public AuctionSniper(SniperListener sniperListener) {
    this.sniperListener = sniperListener;
  }
public void auctionClosed() {
    sniperListener.sniperLost();
  }
  public void currentPrice(int price, int increment) {
// TODO Auto-generated method stub
  }
}
Finally, we retroﬁt the new AuctionSniper by having Main implement
SniperListener.
Chapter 13
The Sniper Makes a Bid
124


---
**Page 125**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new AuctionMessageTranslator(new AuctionSniper(this)));
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  public void sniperLost() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
Our working end-to-end test still passes and our broken one still fails at the
same place, so we haven’t made things worse. The new structure looks like
Figure 13.1.
Figure 13.1
Plugging in the AuctionSniper
Focus, Focus, Focus
Once again, we’ve noticed complexity in a class and used that to tease out a new
concept from our initial skeleton implementation. Now we have a Sniper to re-
spond to events from the translator. As you’ll see shortly, this is a better structure
for expressing what the code does and for unit testing. We also think that the
sniperLost() method is clearer than its previous incarnation, auctionClosed(),
since there’s now a closer match between its name and what it does—that is,
reports a lost auction.
Isn’t this wasteful ﬁddling, gold-plating the code while time slips by? Obviously
we don’t think so, especially when we’re sorting out our ideas this early in the
project. There are teams that overdo their design effort, but our experience is
that most teams spend too little time clarifying the code and pay for it in mainte-
nance overhead. As we’ve shown a couple of times now, the “single responsibil-
ity” principle is a very effective heuristic for breaking up complexity, and
125
Introducing AuctionSniper


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


