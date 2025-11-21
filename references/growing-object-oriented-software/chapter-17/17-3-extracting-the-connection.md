# 17.3 Extracting the Connection (pp.195-197)

---
**Page 195**

@Test public void
receivesEventsFromAuctionServerAfterJoining() throws Exception {
  CountDownLatch auctionWasClosed = new CountDownLatch(1);
  Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
  auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
  auction.join();
  server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  server.announceClosed();
  assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS)); 
} 
private AuctionEventListener 
auctionClosedListener(final CountDownLatch auctionWasClosed) {
  return new AuctionEventListener() {
    public void auctionClosed() { auctionWasClosed.countDown(); }
    public void currentPrice(int price, int increment, PriceSource priceSource) { 
// not implemented
    }
  };
}
Looking over the result, we can see that it makes sense for XMPPAuction to en-
capsulate a Chat as now it hides everything to do with communicating between
a request listener and an auction service, including translating the messages. We
can also see that the AuctionMessageTranslator is internal to this encapsulation,
the Sniper doesn’t need to see it. So, to recognize our new structure, we move
XMPPAuction and AuctionMessageTranslator into a new auctionsniper.xmpp
package, and the tests into equivalent xmpp test packages.
Compromising on a Constructor
We have one doubt about this implementation: the constructor includes some real
behavior. Our experience is that busy constructors enforce assumptions that one
day we will want to break, especially when testing, so we prefer to keep them very
simple—just setting the ﬁelds. For now, we convince ourselves that this is “veneer”
code, a bridge to an external library, that can only be integration-tested because
the Smack classes have just the kind of complicated constructors we try to avoid.
Extracting the Connection
The next thing to remove from Main is direct references to the XMPPConnection.
We can wrap these up in a factory class that will create an instance of an Auction
for a given item, so it will have a method like
Auction auction = <factory>.auctionFor(item id);
195
Extracting the Connection


---
**Page 196**

We struggle for a while over what to call this new type, since it should have a
name that reﬂects the language of auctions. In the end, we decide that the concept
that arranges auctions is an “auction house,” so that’s what we call our new type:
public interface AuctionHouse {
  Auction auctionFor(String itemId);
}
The end result of this refactoring is:
public class Main { […]
  public static void main(String... args) throws Exception {
    Main main = new Main();
XMPPAuctionHouse auctionHouse = 
      XMPPAuctionHouse.connect(
        args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
    main.disconnectWhenUICloses(auctionHouse);
    main.addUserRequestListenerFor(auctionHouse);
  }
  private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
        snipers.addSniper(SniperSnapshot.joining(itemId));
Auction auction = auctionHouse.auctionFor(itemId);
        notToBeGCd.add(auction);
[…]
      }
    }
  }
}
Figure 17.2
With XMPPAuctionHouse extracted
Chapter 17
Teasing Apart Main
196


---
**Page 197**

Implementing XMPPAuctionHouse is straightforward; we transfer there all the
code related to connection, including the generation of the Jabber ID from
the auction item ID. Main is now simpler, with just one import for all the XMPP
code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Figure 17.2.
For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
the test to XMPPAuctionHouseTest.
Our ﬁnal touch is to move the relevant constants from Main where we’d left
them: the message formats to XMPPAuction and the connection identiﬁer format
to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
since we’re narrowing the scope of where these constants are used.
Extracting the SnipersTableModel
Sniper Launcher
Finally, we’d like to do something about the direct reference to the
SnipersTableModel and the related SwingThreadSniperListener—and the awful
notToBeGCd. We think we can get there, but it’ll take a couple of steps.
The ﬁrst step is to turn the anonymous implementation of UserRequestListener
into a proper class so we can understand its dependencies. We decide to call the
new class SniperLauncher, since it will respond to a request to join an auction
by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
to the new class.
public class SniperLauncher implements UserRequestListener {
  private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
  private final AuctionHouse auctionHouse;
  private final SnipersTableModel snipers;
  public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
// set the fields 
  }
  public void joinAuction(String itemId) {
snipers.addSniper(SniperSnapshot.joining(itemId));
      Auction auction = auctionHouse.auctionFor(itemId);
      notToBeGCd.add(auction);
      AuctionSniper sniper = 
        new AuctionSniper(itemId, auction, 
                          new SwingThreadSniperListener(snipers));
      auction.addAuctionEventListener(snipers);
      auction.join();
  }
}
With the SniperLauncher separated out, it becomes even clearer that the
Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
197
Extracting the SnipersTableModel


