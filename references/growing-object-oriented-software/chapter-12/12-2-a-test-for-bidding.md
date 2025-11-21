# 12.2 A Test for Bidding (pp.106-112)

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


---
**Page 107**

4
This method asks the stub auction to check that it has received a bid from
the Sniper that is equal to the last price plus the minimum increment. We
have to do a fraction more work because the XMPP layer constructs a longer
name from the basic identiﬁer, so we deﬁne a constant SNIPER_XMPP_ID which
in practice is sniper@localhost/Auction.
5
We reuse the closing logic from the ﬁrst test, as the Sniper still loses the
auction.
Unrealistic Money
We’re using integers to represent value (imagine that auctions are conducted in
Japanese Yen). In a real system, we would deﬁne a domain type to represent
monetary values, using a ﬁxed decimal implementation. Here, we simplify the
representation to make the example code easier to ﬁt onto a printed page.
Extending the Fake Auction
We have two methods to write in the FakeAuctionServer to support the end-
to-end test: reportPrice() has to send a Price message through the chat;
hasReceivedBid() is a little more complex—it has to check that the auction re-
ceived the right values from the Sniper. Instead of parsing the incoming message,
we construct the expected message and just compare strings. We also pull up the
Matcher clause from the SingleMessageListener to give the FakeAuctionServer
more ﬂexibility in deﬁning what it will accept as a message. Here’s a ﬁrst cut:
public class FakeAuctionServer { […]
  public void reportPrice(int price, int increment, String bidder) 
    throws XMPPException 
  {
    currentChat.sendMessage(
        String.format("SOLVersion: 1.1; Event: PRICE; "
                      + "CurrentPrice: %d; Increment: %d; Bidder: %s;",
                      price, increment, bidder));
  }
  public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
    messageListener.receivesAMessage(is(anything()));
  }
  public void hasReceivedBid(int bid, String sniperId) 
    throws InterruptedException 
  {
    assertThat(currentChat.getParticipant(), equalTo(sniperId));
    messageListener.receivesAMessage(
      equalTo(
        String.format("SOLVersion: 1.1; Command: BID; Price: %d;", bid)));
  }
}
107
A Test for Bidding


---
**Page 108**

public class SingleMessageListener implements MessageListener { […]
  @SuppressWarnings("unchecked")
  public void receivesAMessage(Matcher<? super String> messageMatcher) 
    throws InterruptedException 
  {
    final Message message = messages.poll(5, TimeUnit.SECONDS);
    assertThat("Message", message, is(notNullValue()));
    assertThat(message.getBody(), messageMatcher);
  }
}
Looking again, there’s an imbalance between the two “receives” methods. The
Join method is much more lax than the bid message, in terms of both the contents
of the message and the sender; we will have to remember to come back later and
ﬁx it. We defer a great many decisions when developing incrementally, but
sometimes consistency and symmetry make more sense. We decide to retroﬁt
more detail into hasReceivedJoinRequestFromSniper() while we have the code
cracked open. We also extract the message formats and move them to Main
because we’ll need them to construct raw messages in the Sniper.
public class FakeAuctionServer { […]
  public void hasReceivedJoinRequestFrom(String sniperId) 
    throws InterruptedException 
  {
receivesAMessageMatching(sniperId, equalTo(Main.JOIN_COMMAND_FORMAT));
  }
  public void hasReceivedBid(int bid, String sniperId) 
    throws InterruptedException 
  {
receivesAMessageMatching(sniperId, 
                             equalTo(format(Main.BID_COMMAND_FORMAT, bid)));
  }
  private void receivesAMessageMatching(String sniperId, 
                                        Matcher<? super String> messageMatcher)
    throws InterruptedException 
  {
    messageListener.receivesAMessage(messageMatcher);
    assertThat(currentChat.getParticipant(), equalTo(sniperId));
  }
}
Notice that we check the Sniper’s identiﬁer after we check the contents of the
message. This forces the server to wait until the message has arrived, which means
that it must have accepted a connection and set up currentChat. Otherwise the
test would fail by checking the Sniper’s identiﬁer prematurely.
Chapter 12
Getting Ready to Bid
108


---
**Page 109**

Double-Entry Values
We’re using the same constant to both create a Join message and check its con-
tents. By using the same construct, we’re removing duplication and expressing in
the code a link between the two sides of the system. On the other hand, we’re
making ourselves vulnerable to getting them both wrong and not having a test to
catch the invalid content. In this case, the code is so simple that pretty much any
implementation would do, but the answers become less certain when developing
something more complex, such as a persistence layer. Do we use the same
framework to write and read our values? Can we be sure that it’s not just caching
the results, or that the values are persisted correctly? Should we just write some
straight database queries to be sure?
The critical question is, what do we think we’re testing? Here, we think that the
communication features are more important, that the messages are simple enough
so we can rely on string constants, and that we’d like to be able to ﬁnd code related
to message formats in the IDE. Other developers might come to a different
conclusion and be right for their project.
We adjust the end-to-end tests to match the new API, watch the test fail, and
then add the extra detail to the Sniper to make the test pass.
public class AuctionSniperEndToEndTest {
  @Test public void
sniperMakesAHigherBidButLoses() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding();
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.announceClosed();                  
    application.showsSniperHasLostAuction();   
  }
}
109
A Test for Bidding


---
**Page 110**

public class Main { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new MessageListener() {
          public void processMessage(Chat aChat, Message message) {
            SwingUtilities.invokeLater(new Runnable() {
              public void run() {
                ui.showStatus(MainWindow.STATUS_LOST);
              }
            });
          }
        });
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
}
A Surprise Failure
Finally we write the “checking” method on the ApplicationRunner to give us
our ﬁrst failure. The implementation is simple: we just add another status constant
and copy the existing method.
public class ApplicationRunner { […]
public void hasShownSniperIsBidding() {
    driver.showsSniperStatus(MainWindow.STATUS_BIDDING);
  }
  public void showsSniperHasLostAuction() {
    driver.showsSniperStatus(MainWindow.STATUS_LOST);
  }
}
We’re expecting to see something about a missing label text but instead we
get this:
java.lang.AssertionError: 
Expected: is not null
     got: null
[…]
  at auctionsniper.SingleMessageListener.receivesAMessage()
  at auctionsniper.FakeAuctionServer.hasReceivedJoinRequestFromSniper()
  at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBid()
[…]
and this on the error stream:
Chapter 12
Getting Ready to Bid
110


---
**Page 111**

conflict(409)
  at jivesoftware.smack.SASLAuthentication.bindResourceAndEstablishSession()
  at jivesoftware.smack.SASLAuthentication.authenticate()
  at jivesoftware.smack.XMPPConnection.login()
  at jivesoftware.smack.XMPPConnection.login()
  at auctionsniper.Main.connection()
  at auctionsniper.Main.main()
After some investigation we realize what’s happened. We’ve introduced a second
test which tries to connect using the same account and resource name as the ﬁrst.
The server is conﬁgured, like Southabee’s On-Line, to reject multiple open con-
nections, so the second test fails because the server thinks that the ﬁrst is still
connected. In production, our application would work because we’d stop the
whole process when closing, which would break the connection. Our little com-
promise (of starting the application in a new thread) has caught us out. The Right
Thing to do here is to add a callback to disconnect the client when we close the
window so that the application will clean up after itself:
public class Main { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
[…]
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  private void disconnectWhenUICloses(final XMPPConnection connection) {
    ui.addWindowListener(new WindowAdapter() {
      @Override public void windowClosed(WindowEvent e) {
connection.disconnect();
      }
    });
  }
}
Now we get the failure we expected, because the Sniper has no way to start
bidding.
java.lang.AssertionError: 
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that its label text is "Bidding"
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JLabel (with name "sniper status")
label text was "Lost"
[…]
  at auctionsniper.AuctionSniperDriver.showsSniperStatus()
  at auctionsniper.ApplicationRunner.hasShownSniperIsBidding()
  at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBidButLoses()
111
A Test for Bidding


---
**Page 112**

Outside-In Development
This failure deﬁnes the target for our next coding episode. It tells us, at a high
level, what we’re aiming for—we just have to ﬁll in implementation until it
passes.
Our approach to test-driven development is to start with the outside event that
triggers the behavior we want to implement and work our way into the code an
object at a time, until we reach a visible effect (such as a sent message or log entry)
indicating that we’ve achieved our goal. The end-to-end test shows us the end
points of that process, so we can explore our way through the space in the middle.
In the following sections, we build up the types we need to implement our
Auction Sniper. We’ll take it slowly, strictly by the TDD rules, to show how the
process works. In real projects, we sometimes design a bit further ahead to get
a sense of the bigger picture, but much of the time this is what we actually do.
It produces the right results and forces us to ask the right questions.
Inﬁnite Attention to Detail?
We caught the resource clash because, by luck or insight, our server conﬁguration
matched that of Southabee’s On-Line. We might have used an alternative setting
which allows new connections to kick off existing ones, which would have resulted
in the tests passing but with a confusing conﬂict message from the Smack library
on the error stream. This would have worked ﬁne in development, but with a
risk of Snipers starting to fail in production.
How can we hope to catch all the conﬁguration options in an entire system?
At some level we can’t, and this is at the heart of what professional testers do.
What we can do is push to exercise as much as possible of the system as early as
possible, and to do so repeatedly. We can also help ourselves cope with total
system complexity by keeping the quality of its components high and by constantly
pushing to simplify. If that sounds expensive, consider the cost of ﬁnding and
ﬁxing a transient bug like this one in a busy production system.
The AuctionMessageTranslator
Teasing Out a New Class
Our entry point to the Sniper is where we receive a message from the auction
through the Smack library: it’s the event that triggers the next round of behavior
we want to make work. In practice, this means that we need a class implementing
MessageListener to attach to the Chat. When this class receives a raw message
from the auction, it will translate it into something that represents an auction
event within our code which, eventually, will prompt a Sniper action and a change
in the user interface.
Chapter 12
Getting Ready to Bid
112


