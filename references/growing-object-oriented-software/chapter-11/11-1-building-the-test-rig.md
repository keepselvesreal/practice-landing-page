# 11.1 Building the Test Rig (pp.89-95)

---
**Page 89**

Chapter 11
Passing the First Test
In which we write test infrastructure to drive our non-existent applica-
tion, so that we can make the ﬁrst test fail. We repeatedly fail the test
and ﬁx symptoms, until we have a minimal working application that
passes the ﬁrst test. We step through this very slowly to show how the
process works.
Building the Test Rig
At the start of every test run, our test script starts up the Openﬁre server, creates
accounts for the Sniper and the auction, and then runs the tests. Each test will
start instances of the application and the fake auction, and then test their com-
munication through the server. At ﬁrst, we’ll run everything on the same host.
Later, as the infrastructure stabilizes, we can consider running different compo-
nents on different machines, which will be a better match to the real deployment.
This leaves us with two components to write for the test infrastructure:
ApplicationRunner and FakeAuctionServer.
Setting Up the Openﬁre Server
At the time of writing, we were using version 3.6 of Openﬁre. For these end-to-
end tests, we set up our local server with three user accounts and passwords:
sniper
sniper
auction-item-54321
auction
auction-item-65432
auction
For desktop development, we usually started the server by hand and left it running.
We set it up to not store ofﬂine messages, which meant there was no persistent
state. In the System Manager, we edited the “System Name” property to be
localhost, so the tests would run consistently. Finally, we set the resource policy
to “Never kick,” which will not allow a new resource to log in if there’s a conﬂict.
89


---
**Page 90**

The Application Runner
An ApplicationRunner is an object that wraps up all management and commu-
nicating with the Swing application we’re building. It runs the application as if
from the command line, obtaining and holding a reference to its main window
for querying the state of the GUI and for shutting down the application at the
end of the test.
We don’t have to do much here, because we can rely on WindowLicker to do
the hard work: ﬁnd and control Swing GUI components, synchronize with
Swing’s threads and event queue, and wrap that all up behind a simple API.1
WindowLicker has the concept of a ComponentDriver: an object that can manip-
ulate a feature in a Swing user interface. If a ComponentDriver can’t ﬁnd the
Swing component it refers to, it will time out with an error. For this test, we’re
looking for a label component that shows a given string; if our application doesn’t
produce this label, we’ll get an exception. Here’s the implementation (with the
constants left out for clarity) and some explanation:
public class ApplicationRunner {
  public static final String SNIPER_ID = "sniper";
  public static final String SNIPER_PASSWORD = "sniper";
  private AuctionSniperDriver driver;
  public void startBiddingIn(final FakeAuctionServer auction) {
    Thread thread = new Thread("Test Application") {
      @Override public void run() { 1
        try {
          Main.main(XMPP_HOSTNAME, SNIPER_ID, SNIPER_PASSWORD, auction.getItemId()); 2
        } catch (Exception e) {                                                    
          e.printStackTrace(); 3
        }
      }
    };
    thread.setDaemon(true);
    thread.start();
    driver = new AuctionSniperDriver(1000); 4
    driver.showsSniperStatus(STATUS_JOINING); 5
  }
  public void showsSniperHasLostAuction() {
    driver.showsSniperStatus(STATUS_LOST);  6
  }
  public void stop() {
    if (driver != null) {
      driver.dispose(); 7
    }
  }
}
1. We’re assuming that you know how Swing works; there are many other books that
do a good job of describing it. The essential point here is that it’s an event-driven
framework that creates its own internal threads to dispatch events, so we can’t be
precise about when things will happen.
Chapter 11
Passing the First Test
90


---
**Page 91**

1
We call the application through its main() function to make sure we’ve as-
sembled the pieces correctly. We’re following the convention that the entry
point to the application is a Main class in the top-level package. WindowLicker
can control Swing components if they’re in the same JVM, so we start the
Sniper in a new thread. Ideally, the test would start the Sniper in a new pro-
cess, but that would be much harder to test; we think this is a reasonable
compromise.
2
To keep things simple at this stage, we’ll assume that we’re only bidding for
one item and pass the identiﬁer to main().
3
If main() throws an exception, we just print it out. Whatever test we’re
running will fail and we can look for the stack trace in the output. Later,
we’ll handle exceptions properly.
4
We turn down the timeout period for ﬁnding frames and components. The
default values are longer than we need for a simple application like this one
and will slow down the tests when they fail. We use one second, which is
enough to smooth over minor runtime delays.
5
We wait for the status to change to Joining so we know that the application
has attempted to connect. This assertion says that somewhere in the user
interface there’s a label that describes the Sniper’s state.
6
When the Sniper loses the auction, we expect it to show a Lost status. If this
doesn’t happen, the driver will throw an exception.
7
After the test, we tell the driver to dispose of the window to make sure it
won’t be picked up in another test before being garbage-collected.
The AuctionSniperDriver is simply an extension of a WindowLicker
JFrameDriver specialized for our tests:
public class AuctionSniperDriver extends JFrameDriver {
  public AuctionSniperDriver(int timeoutMillis) {
    super(new GesturePerformer(), 
          JFrameDriver.topLevelFrame(
            named(Main.MAIN_WINDOW_NAME), 
            showingOnScreen()),
            new AWTEventQueueProber(timeoutMillis, 100));
  }
  public void showsSniperStatus(String statusText) {
    new JLabelDriver(
      this, named(Main.SNIPER_STATUS_NAME)).hasText(equalTo(statusText));
  }
}
91
Building the Test Rig


---
**Page 92**

On construction, it attempts to ﬁnd a visible top-level window for the Auction
Sniper within the given timeout. The method showsSniperStatus() looks for the
relevant label in the user interface and conﬁrms that it shows the given status.
If the driver cannot ﬁnd a feature it expects, it will throw an exception and fail
the test.
The Fake Auction
A FakeAuctionServer is a substitute server that allows the test to check how the
Auction Sniper interacts with an auction using XMPP messages. It has three re-
sponsibilities: it must connect to the XMPP broker and accept a request to join
the chat from the Sniper; it must receive chat messages from the Sniper or fail if
no message arrives within some timeout; and, it must allow the test to send
messages back to the Sniper as speciﬁed by Southabee’s On-Line.
Smack (the XMPP client library) is event-driven, so the fake auction has to
register listener objects for it to call back. There are two levels of events: events
about a chat, such as people joining, and events within a chat, such as messages
being received. We need to listen for both.
We’ll start by implementing the startSellingItem() method. First, it connects
to the XMPP broker, using the item identiﬁer to construct the login name; then
it registers a ChatManagerListener. Smack will call this listener with a Chat object
that represents the session when a Sniper connects in. The fake auction holds on
to the chat so it can exchange messages with the Sniper.
Figure 11.1
Smack objects and callbacks
Chapter 11
Passing the First Test
92


---
**Page 93**

So far, we have:
public class FakeAuctionServer {
  public static final String ITEM_ID_AS_LOGIN = "auction-%s"; 
  public static final String AUCTION_RESOURCE = "Auction";
  public static final String XMPP_HOSTNAME = "localhost";
  private static final String AUCTION_PASSWORD = "auction";
  private final String itemId;
  private final XMPPConnection connection;
  private Chat currentChat;
  public FakeAuctionServer(String itemId) {
    this.itemId = itemId;
    this.connection = new XMPPConnection(XMPP_HOSTNAME);
  }
  public void startSellingItem() throws XMPPException {
    connection.connect(); 
    connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
                     AUCTION_PASSWORD, AUCTION_RESOURCE);
    connection.getChatManager().addChatListener(
      new ChatManagerListener() {
        public void chatCreated(Chat chat, boolean createdLocally) {
          currentChat = chat;
        }
      });
  }
  public String getItemId() {
    return itemId;
  }
}
A Minimal Fake Implementation
We want to emphasize again that this fake is a minimal implementation just to
support testing. For example, we use a single instance variable to hold the chat
object. A real auction server would manage multiple chats for all the bidders—but
this is a fake; its only purpose is to support the test, so it only needs one chat.
Next, we have to add a MessageListener to the chat to accept messages from
the Sniper. This means that we need to coordinate between the thread that
runs the test and the Smack thread that feeds messages to the listener—the test
has to wait for messages to arrive and time out if they don’t—so we’ll use a
single-element BlockingQueue from the java.util.concurrent package. Just as
we only have one chat in the test, we expect to process only one message at a
time. To make our intentions clearer, we wrap the queue in a helper class
SingleMessageListener. Here’s the rest of FakeAuctionServer:
93
Building the Test Rig


---
**Page 94**

public class FakeAuctionServer {
private final SingleMessageListener messageListener = new SingleMessageListener();
  public void startSellingItem() throws XMPPException {
    connection.connect(); 
    connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
                     AUCTION_PASSWORD, AUCTION_RESOURCE);
    connection.getChatManager().addChatListener(
      new ChatManagerListener() {
        public void chatCreated(Chat chat, boolean createdLocally) {
          currentChat = chat;
chat.addMessageListener(messageListener);
        }
      });
  }
  public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
    messageListener.receivesAMessage(); 1
  }
  public void announceClosed() throws XMPPException {
    currentChat.sendMessage(new Message()); 2
  }
  public void stop() {
    connection.disconnect(); 3
  }
}
public class SingleMessageListener implements MessageListener {
  private final ArrayBlockingQueue<Message> messages = 
                              new ArrayBlockingQueue<Message>(1);
  public void processMessage(Chat chat, Message message) {
    messages.add(message);
  }
  public void receivesAMessage() throws InterruptedException {
    assertThat("Message", messages.poll(5, SECONDS), is(notNullValue())); 4
  }
}
1
The test needs to know when a Join message has arrived. We just check
whether any message has arrived, since the Sniper will only be sending Join
messages to start with; we’ll ﬁll in more detail as we grow the application.
This implementation will fail if no message is received within 5 seconds.
2
The test needs to be able to simulate the auction announcing when it closes,
which is why we held onto the currentChat when it opened. As with the
Join request, the fake auction just sends an empty message, since this is
the only event we support so far.
3
stop() closes the connection.
Chapter 11
Passing the First Test
94


---
**Page 95**

4
The clause is(notNullValue()) uses the Hamcrest matcher syntax. We de-
scribe Matchers in “Methods” (page 339); for now, it’s enough to know that
this checks that the Listener has received a message within the timeout period.
The Message Broker
There’s one more component to mention which doesn’t involve any coding—the
installation of an XMPP message broker. We set up an instance of Openﬁre on
our local host. The Sniper and fake auction in our end-to-end tests, even though
they’re running in the same process, will communicate through this server. We
also set up logins to match the small number of item identiﬁers that we’ll be using
in our tests.
A Working Compromise
As we wrote before, we are cheating a little at this stage to keep development
moving. We want all the developers to have their own environments so they don’t
interfere with each other when running their tests. For example, we’ve seen teams
make their lives very complicated because they didn’t want to create a database
instance for each developer. In a professional organization, we would also expect
to see at least one test rig that represents the production environment, including
the distribution of processing across a network and a build cycle that uses it to
make sure the system works.
Failing and Passing the Test
We have enough infrastructure in place to run the test and watch it fail. For the
rest of this chapter we’ll add functionality, a tiny slice at a time, until eventually
we make the test pass. When we ﬁrst started using this technique, it felt too fussy:
“Just write the code, we know what to do!” Over time, we realized that it didn’t
take any longer and that our progress was much more predictable. Focusing on
just one aspect at a time helps us to make sure we understand it; as a rule, when
we get something working, it stays working. Where there’s no need to discuss
the solution, many of these steps take hardly any time at all—they take longer
to explain than to implement.
We start by writing a build script for ant. We’ll skip over the details of its
content, since it’s standard practice these days, but the important point is that
we always have a single command that reliably compiles, builds, deploys, and
tests the application, and that we run it repeatedly. We only start coding once
we have an automated build and test working.
At this stage, we’ll describe each step, discussing each test failure in turn. Later
we’ll speed up the pace.
95
Failing and Passing the Test


