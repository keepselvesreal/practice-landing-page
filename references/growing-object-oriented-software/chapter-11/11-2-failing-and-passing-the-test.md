# 11.2 Failing and Passing the Test (pp.95-102)

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


---
**Page 96**

First User Interface
Test Failure
The test can’t ﬁnd a user interface component with the name "Auction Sniper
Main".
java.lang.AssertionError: 
Tried to look for...
    exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
but...
    all top level windows
contained 0 JFrame (with name "Auction Sniper Main" and showing on screen)
[…]
  at auctionsniper.ApplicationRunner.stop()
  at auctionsniper.AuctionSniperEndToEndTest.stopApplication()
[…]
WindowLicker is verbose in its error reporting, trying to make failures easy
to understand. In this case, we couldn’t even ﬁnd the top-level frame so JUnit
failed before even starting the test. The stack trace comes from the @After method
that stops the application.
Implementation
We need a top-level window for our application. We write a MainWindow class in
the auctionsniper.ui package that extends Swing’s JFrame, and call it from
main(). All it will do is create a window with the right name.
public class Main {
  private MainWindow ui;
  public Main() throws Exception {
startUserInterface()
  }
  public static void main(String... args) throws Exception {
    Main main = new Main();
  }
  private void startUserInterface() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() {
      public void run() {
        ui = new MainWindow();
      }
    });
  }
}
Chapter 11
Passing the First Test
96


---
**Page 97**

public class MainWindow extends JFrame {
  public MainWindow() {
    super("Auction Sniper");
    setName(MAIN_WINDOW_NAME);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true);
  }
}
Unfortunately, this is a little messy because Swing requires us to create the
user interface on its event dispatch thread. We’ve further complicated the imple-
mentation so we can hang on to the main window object in our code. It’s not
strictly necessary here but we thought we’d get it over with.
Notes
The user interface in Figure 11.2 really is minimal. It does not look like much
but it conﬁrms that we can start up an application window and connect to it.
Our test still fails, but we’ve moved on a step. Now we know that our harness
is working, which is one less thing to worry about as we move on to more
interesting functionality.
Figure 11.2
Just a top-level window
Showing the Sniper State
Test Failure
The test ﬁnds a top-level window, but no display of the current state of the Sniper.
To start with, the Sniper should show Joining while waiting for the auction to
respond.
java.lang.AssertionError: 
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that its label text is "Joining"
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
contained 0 JLabel (with name "sniper status")
  at com.objogate.wl.AWTEventQueueProber.check()
[…]
  at AuctionSniperDriver.showsSniperStatus()
  at ApplicationRunner.startBiddingIn()
  at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
[…]
97
Failing and Passing the Test


---
**Page 98**

Implementation
We add a label representing the Sniper’s state to MainWindow.
public class MainWindow extends JFrame {
  public static final String SNIPER_STATUS_NAME = "sniper status";
  private final JLabel sniperStatus = createLabel(STATUS_JOINING);
  public MainWindow() {
    super("Auction Sniper");
    setName(MAIN_WINDOW_NAME);
add(sniperStatus);
    pack();
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true);
  }
  private static JLabel createLabel(String initialText) {
    JLabel result = new JLabel(initialText);
    result.setName(SNIPER_STATUS_NAME);
    result.setBorder(new LineBorder(Color.BLACK));
    return result;
  }
}
Notes
Another minimal change, but now we can show some content in our application,
as in Figure 11.3.
Figure 11.3
Showing Joining status
Connecting to the Auction
Test Failure
Our user interface is working, but the auction does not receive a Join request
from the Sniper.
java.lang.AssertionError: 
Expected: is not null
got: null
  at org.junit.Assert.assertThat()
  at SingleMessageListener.receivesAMessage()
  at FakeAuctionServer.hasReceivedJoinRequestFromSniper()
  at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
[…]
Chapter 11
Passing the First Test
98


---
**Page 99**

This failure message is a bit cryptic, but the names in the stack trace tell us
what’s wrong.
Implementation
We write a simplistic implementation to get us past this failure. It connects to
the chat in Main and sends an empty message. We create a null MessageListener
to allow us to create a Chat for sending the empty initial message, since we don’t
yet care about receiving messages.
public class Main {
  private static final int ARG_HOSTNAME = 0;
  private static final int ARG_USERNAME = 1;
  private static final int ARG_PASSWORD = 2;
  private static final int ARG_ITEM_ID  = 3;
  public static final String AUCTION_RESOURCE = "Auction";
  public static final String ITEM_ID_AS_LOGIN = "auction-%s";
  public static final String AUCTION_ID_FORMAT = 
                               ITEM_ID_AS_LOGIN + "@%s/" + AUCTION_RESOURCE;
[…]
  public static void main(String... args) throws Exception {
    Main main = new Main();
    XMPPConnection connection = connectTo(args[ARG_HOSTNAME], 
                                          args[ARG_USERNAME], 
                                          args[ARG_PASSWORD]);
    Chat chat = connection.getChatManager().createChat(
        auctionId(args[ARG_ITEM_ID], connection), 
        new MessageListener() {
          public void processMessage(Chat aChat, Message message) {
// nothing yet
          }
        });
    chat.sendMessage(new Message());
  }
  private static XMPPConnection 
connectTo(String hostname, String username, String password) 
      throws XMPPException
  {
    XMPPConnection connection = new XMPPConnection(hostname);
    connection.connect();
    connection.login(username, password, AUCTION_RESOURCE);
    return connection;
  }
  private static String auctionId(String itemId, XMPPConnection connection) {
    return String.format(AUCTION_ID_FORMAT, itemId, 
                         connection.getServiceName()); 
  }
[…]
}
99
Failing and Passing the Test


---
**Page 100**

Notes
This shows that we can establish a connection from the Sniper to the auction,
which means we had to sort out details such as interpreting the item and user
credentials from the command-line arguments and using the Smack library. We’re
leaving the message contents until later because we only have one message type,
so sending an empty value is enough to prove the connection.
This implementation may seem gratuitously naive—after all, we should be able
to design a structure for something as simple as this, but we’ve often found it
worth writing a small amount of ugly code and seeing how it falls out. It helps
us to test our ideas before we’ve gone too far, and sometimes the results can be
surprising. The important point is to make sure we don’t leave it ugly.
We make a point of keeping the connection code out of the Swing
invokeAndWait() call that creates the MainWindow, because we want the user
interface to settle before we try anything more complicated.
Receiving a Response from the Auction
Test Failure
With a connection established, the Sniper should receive and display the Lost
response from the auction. It doesn’t yet:
java.lang.AssertionError: 
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that its label text is "Lost"
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JLabel (with name "sniper status")
label text was "Joining"
[…]
  at AuctionSniperDriver.showsSniperStatus()
  at ApplicationRunner.showsSniperHasLostAuction()
  at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
[…]
Implementation
We need to attach the user interface to the chat so it can receive the response
from the auction, so we create a connection and pass it to Main to create the Chat
object. joinAuction() creates a MessageListener that sets the status label, using
an invokeLater() call to avoid blocking the Smack library. As with the Join
message, we don’t bother with the contents of the incoming message since there’s
only one possible response the auction can send at the moment. While we’re at
it, we rename connect() to connection() to make the code read better.
Chapter 11
Passing the First Test
100


---
**Page 101**

public class Main {
  @SuppressWarnings("unused") private Chat notToBeGCd;
[…]
  public static void main(String... args) throws Exception {
    Main main = new Main();
main.joinAuction(
      connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
      args[ARG_ITEM_ID]);
  }
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException
  {
    final Chat chat = connection.getChatManager().createChat(
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
    chat.sendMessage(new Message());
  }
Why the Chat Field?
You’ll notice that we’ve assigned the chat that we create to the ﬁeld notToBeGCd
in Main. This is to make sure that the chat is not garbage-collected by the Java
runtime. There’s a note at the top of the ChatManager documentation that says:
The chat manager keeps track of references to all current chats. It will not
hold any references in memory on its own so it is necessary to keep a
reference to the chat object itself.
If the chat is garbage-collected, the Smack runtime will hand the message to a
new Chat which it will create for the purpose. In an interactive application, we would
listen for and show these new chats, but our needs are different, so we add this
quirk to stop it from happening.
We made this reference clumsy on purpose—to highlight in the code why we’re
doing it.We also know that we’re likely to come up with a better solution in a while.
We implement the display method in the user interface and, ﬁnally, the whole
test passes.
101
Failing and Passing the Test


---
**Page 102**

public class MainWindow extends JFrame {
[…]
  public void showStatus(String status) {
sniperStatus.setText(status);
  }
}
Notes
Figure 11.4 is visible conﬁrmation that the code works.
Figure 11.4
Showing Lost status
It may not look like much, but it conﬁrms that a Sniper can establish a
connection with an auction, accept a response, and display the result.
The Necessary Minimum
In one of his school reports, Steve was noted as “a ﬁne judge of the necessary
minimum.” It seems he’s found his calling in writing software since this is a
critical skill during iteration zero.
What we hope you’ve seen in this chapter is the degree of focus that’s required
to put together your ﬁrst walking skeleton. The point is to design and validate
the initial structure of the end-to-end system—where end-to-end includes deploy-
ment to a working environment—to prove that our choices of packages, libraries,
and tooling will actually work. A sense of urgency will help the team to strip the
functionality down to the absolute minimum sufﬁcient to test their assumptions.
That’s why we didn’t put any content in our Sniper messages; it would be a di-
version from making sure that the communication and event handling work. We
didn’t sweat too hard over the detailed code design, partly because there isn’t
much but mainly because we’re just getting the pieces in place; that effort will
come soon enough.
Of course, all you see in this chapter are edited highlights. We’ve left out many
diversions and discussions as we ﬁgured out which pieces to use and how to make
them work, trawling through product documentation and discussion lists. We’ve
also left out some of our discussions about what this project is for. Iteration zero
usually brings up project chartering issues as the team looks for criteria to guide
its decisions, so the project’s sponsors should expect to ﬁeld some deep questions
about its purpose.
Chapter 11
Passing the First Test
102


