# 17.2 Extracting the Chat (pp.192-195)

---
**Page 192**

We think we should extract some of this behavior from Main, and the XMPP
features look like a good ﬁrst candidate. The use of the Smack should be an
implementation detail that is irrelevant to the rest of the application.
Extracting the Chat
Isolating the Chat
Most 
of 
the 
action 
happens 
in 
the 
implementation 
of
UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
leaved different domain levels, auction sniping and chatting, in this one unit of
code. We’d like to split them up. Here it is again:
public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
    public void joinAuction(String itemId) {
      snipers.addSniper(SniperSnapshot.joining(itemId));
        Chat chat = connection.getChatManager()
                                 .createChat(auctionId(itemId, connection), null);
        notToBeGCd.add(chat); 
        Auction auction = new XMPPAuction(chat);
chat.addMessageListener(
               new AuctionMessageTranslator(connection.getUser(),
                     new AuctionSniper(itemId, auction, 
                           new SwingThreadSniperListener(snipers))));
        auction.join();
      }
    });
  }
}
The object that locks this code into Smack is the chat; we refer to it several times:
to avoid garbage collection, to attach it to the Auction implementation, and to
attach the message listener. If we can gather together the auction- and Sniper-
related code, we can move the chat elsewhere, but that’s tricky while there’s still
a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
rather than a direct link, would give us the ﬂexibility we need. It would also make
sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
(page 52). The result is:
Chapter 17
Teasing Apart Main
192


---
**Page 193**

public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
        Chat chat = connection.[…]
        Announcer<AuctionEventListener> auctionEventListeners = 
            Announcer.to(AuctionEventListener.class);
        chat.addMessageListener(
            new AuctionMessageTranslator(
                connection.getUser(),
auctionEventListeners.announce()));
        notToBeGCd.add(chat);
        Auction auction = new XMPPAuction(chat);
auctionEventListeners.addListener(
           new AuctionSniper(itemId, auction, new SwingThreadSniperListener(snipers)));
        auction.join();
      }
    }
  }
}
This looks worse, but the interesting bit is the last three lines. If you squint, it
looks like everything is described in terms of Auctions and Snipers (there’s still
the Swing thread issue, but we did tell you to squint).
Encapsulating the Chat
From here, we can push everything to do with chat, its setup, and the use of the
Announcer, into XMPPAuction, adding management methods to the Auction inter-
face for its AuctionEventListeners. We’re just showing the end result here, but
we changed the code incrementally so that nothing was broken for more than a
few minutes.
public final class XMPPAuction implements Auction { […]
  private final Announcer<AuctionEventListener> auctionEventListeners = […]
  private final Chat chat;
  public XMPPAuction(XMPPConnection connection, String itemId) {
    chat = connection.getChatManager().createChat(
             auctionId(itemId, connection),
             new AuctionMessageTranslator(connection.getUser(), 
                                          auctionEventListeners.announce()));
  } 
  private static String auctionId(String itemId, XMPPConnection connection) { 
    return String.format(AUCTION_ID_FORMAT, itemId, connection.getServiceName());
  }
}
193
Extracting the Chat


---
**Page 194**

Apart from the garbage collection “wart,” this removes any references to Chat
from Main.
public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
          snipers.addSniper(SniperSnapshot.joining(itemId));
          Auction auction = new XMPPAuction(connection, itemId);
          notToBeGCd.add(auction);
auction.addAuctionEventListener(
                  new AuctionSniper(itemId, auction, 
                                    new SwingThreadSniperListener(snipers)));
auction.join();
      }
    });
  }
}
Figure 17.1
With XMPPAuction extracted
Writing a New Test
We also write a new integration test for the expanded XMPPAuction to show that
it can create a Chat and attach a listener. We use some of our existing end-to-end
test infrastructure, such as FakeAuctionServer, and a CountDownLatch from the
Java concurrency libraries to wait for a response.
Chapter 17
Teasing Apart Main
194


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


