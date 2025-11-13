# 10.2 Our Very First Test (pp.84-86)

---
**Page 84**

Our Very First Test
The walking skeleton must cover all the components of our Auction Sniper system:
the user interface, the sniping component, and the communication with an auction
server. The thinnest slice we can imagine testing, the ﬁrst item on our to-do list,
is that the Auction Sniper can join an auction and then wait for it to close. This
slice is so minimal that we’re not even concerned with sending a bid; we just
want to know that the two sides can communicate and that we can test the system
from outside (through the client’s GUI and by injecting events as if from the ex-
ternal auction server). Once that’s working, we have a solid base on which to
build the rest of the features that the clients want.
We like to start by writing a test as if its implementation already exists, and
then ﬁlling in whatever is needed to make it work—what Abelson and Sussman
call “programming by wishful thinking” [Abelson96]. Working backwards from
the test helps us focus on what we want the system to do, instead of getting
caught up in the complexity of how we will make it work. So, ﬁrst we code up
a test to describe our intentions as clearly as we can, given the expressive limits
of a programming language. Then we build the infrastructure to support the way
we want to test the system, instead of writing the tests to ﬁt in with an existing
infrastructure. This usually takes a large part of our initial effort because there
is so much to get ready. With this infrastructure in place, we can implement the
feature and make the test pass.
An outline of the test we want is:
1.
When an auction is selling an item,
2.
And an Auction Sniper has started to bid in that auction,
3.
Then the auction will receive a Join request from the Auction Sniper.
4.
When an auction announces that it is Closed,
5.
Then the Auction Sniper will show that it lost the auction.
This describes one transition in the state machine (see Figure 10.1).
We need to translate this into something executable. We use JUnit as our test
framework since it’s familiar and widely supported. We also need mechanisms
to control the application and the auction that the application is talking to.
Southabee’s On-Line test services are not freely available. We have to book
ahead and pay for each test session, which is not practical if we want to run tests
all the time. We’ll need a fake auction service that we can control from our
tests to behave like the real thing—or at least like we think the real thing behaves
until we get a chance to test against it for real. This fake auction, or stub, will
be as simple as we can make it. It will connect to an XMPP message broker,
receive commands from the Sniper to be checked by the test, and allow the test
to send back events. We’re not trying to reimplement all of Southabee’s On-Line,
just enough of it to support test scenarios.
Chapter 10
The Walking Skeleton
84


---
**Page 85**

Figure 10.1
A Sniper joins, then loses
Controlling the Sniper application is more complicated. We want our skeleton
test to exercise our application as close to end-to-end as possible, to show that
the main() method initializes the application correctly and that the components
really work together. This means that we should start by working through the
publicly visible features of the application (in this case, its user interface) instead
of directly invoking its domain objects. We also want our test to be clear about
what is being checked, written in terms of the relationship between a Sniper and
its auction, so we’ll hide all the messy code for manipulating Swing in an
ApplicationRunner class. We’ll start by writing the test as if all the code it needs
exists and will ﬁll in the implementations afterwards.
public class AuctionSniperEndToEndTest {
  private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");
  private final ApplicationRunner application = new ApplicationRunner();
  @Test public void sniperJoinsAuctionUntilAuctionCloses() throws Exception {
    auction.startSellingItem();                 // Step 1
    application.startBiddingIn(auction);        // Step 2
    auction.hasReceivedJoinRequestFromSniper(); // Step 3
    auction.announceClosed();                   // Step 4
    application.showsSniperHasLostAuction();    // Step 5
  }
// Additional cleanup
  @After public void stopAuction() {
    auction.stop();
  }
  @After public void stopApplication() {
    application.stop();
  }
}
85
Our Very First Test


---
**Page 86**

We’ve adopted certain naming conventions for the methods of the helper ob-
jects. If a method triggers an event to drive the test, its name will be a command,
such as startBiddingIn(). If a method asserts that something should have hap-
pened, its name will be descriptive;1 for example, showsSniperHasLostAuction()
will throw an exception if the application is not showing the auction status as
lost. JUnit will call the two stop() methods after the test has run, to clean up
the runtime environment.
In writing the test, one of the assumptions we’ve made is that a
FakeAuctionServer is tied to a given item. This matches the structure of our
intended architecture, where Southabee’s On-Line hosts multiple auctions, each
selling a single item.
One Domain at a Time
The language of this test is concerned with auctions and Snipers; there’s nothing
about messaging layers or components in the user interface—that’s all incidental
detail here. Keeping the language consistent helps us understand what’s signiﬁcant
in this test, with a nice side effect of protecting us when the implementation inevitably
changes.
Some Initial Choices
Now we have to make the test pass, which will require a lot of preparation. We
need to ﬁnd or write four components: an XMPP message broker, a stub auction
that can communicate over XMPP, a GUI testing framework, and a test har-
ness that can cope with our multithreaded, asynchronous architecture. We also
have to get the project under version control with an automated build/deploy/test
process. Compared to unit-testing a single class, there is a lot to do—but it’s es-
sential. Even at this high level, the exercise of writing tests drives the development
of the system. Working through our ﬁrst end-to-end test will force some of the
structural decisions we need to make, such as packaging and deployment.
First the package selection, we will need an XMPP message broker to let the
application talk to our stub auction house. After some investigation, we decide
on an open source implementation called Openﬁre and its associated client library
Smack. We also need a high-level test framework that can work with Swing
and Smack, both of which are multithreaded and event-driven. Luckily for us,
there are several frameworks for testing Swing applications and the way that
they deal with Swing’s multithreaded, event-driven architecture also works well
with XMPP messaging. We pick WindowLicker which is open source and supports
1. For the grammatically pedantic, the names of methods that trigger events are in the
imperative mood whereas the names of assertions are in the indicative mood.
Chapter 10
The Walking Skeleton
86


