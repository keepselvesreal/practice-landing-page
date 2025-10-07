Line 1: 
Line 2: --- 페이지 108 ---
Line 3: Chapter 10
Line 4: The Walking Skeleton
Line 5: In which we set up our development environment and write our ﬁrst
Line 6: end-to-end test. We make some infrastructure choices that allow us to
Line 7: get started, and construct a build. We’re surprised, yet again, at how
Line 8: much effort this takes.
Line 9: Get the Skeleton out of the Closet
Line 10: So now we’ve got an idea of what to build, can we get on with it and write our
Line 11: ﬁrst unit test?
Line 12: Not yet.
Line 13: Our ﬁrst task is to create the “walking skeleton” we described in “First, Test
Line 14: a Walking Skeleton” (page 32). Again, the point of the walking skeleton is to
Line 15: help us understand the requirements well enough to propose and validate a broad-
Line 16: brush system structure. We can always change our minds later, when we learn
Line 17: more, but it’s important to start with something that maps out the landscape of
Line 18: our solution. Also, it’s very important to be able to assess the approach we’ve
Line 19: chosen and to test our decisions so we can make changes with conﬁdence later.
Line 20: For most projects, developing the walking skeleton takes a surprising amount
Line 21: of effort. First, because deciding what to do will ﬂush out all sorts of questions
Line 22: about the application and its place in the world. Second, because the automation
Line 23: of building, packaging, and deploying into a production-like environment (once
Line 24: we know what that means) will ﬂush out all sorts of technical and organizational
Line 25: questions.
Line 26: Iteration Zero
Line 27: In most Agile projects, there’s a ﬁrst stage where the team is doing initial analysis,
Line 28: setting up its physical and technical environments, and otherwise getting started.
Line 29: The team isn’t adding much visible functionality since almost all the work is infra-
Line 30: structure, so it might not make sense to count this as a conventional iteration for
Line 31: scheduling purposes. A common practice is to call this step iteration zero: “iteration”
Line 32: because the team still needs to time-box its activities and “zero” because it’s before
Line 33: functional development starts in iteration one. One important task for iteration zero
Line 34: is to use the walking skeleton to test-drive the initial architecture.
Line 35: Of course, we start our walking skeleton by writing a test.
Line 36: 83
Line 37: 
Line 38: --- 페이지 109 ---
Line 39: Our Very First Test
Line 40: The walking skeleton must cover all the components of our Auction Sniper system:
Line 41: the user interface, the sniping component, and the communication with an auction
Line 42: server. The thinnest slice we can imagine testing, the ﬁrst item on our to-do list,
Line 43: is that the Auction Sniper can join an auction and then wait for it to close. This
Line 44: slice is so minimal that we’re not even concerned with sending a bid; we just
Line 45: want to know that the two sides can communicate and that we can test the system
Line 46: from outside (through the client’s GUI and by injecting events as if from the ex-
Line 47: ternal auction server). Once that’s working, we have a solid base on which to
Line 48: build the rest of the features that the clients want.
Line 49: We like to start by writing a test as if its implementation already exists, and
Line 50: then ﬁlling in whatever is needed to make it work—what Abelson and Sussman
Line 51: call “programming by wishful thinking” [Abelson96]. Working backwards from
Line 52: the test helps us focus on what we want the system to do, instead of getting
Line 53: caught up in the complexity of how we will make it work. So, ﬁrst we code up
Line 54: a test to describe our intentions as clearly as we can, given the expressive limits
Line 55: of a programming language. Then we build the infrastructure to support the way
Line 56: we want to test the system, instead of writing the tests to ﬁt in with an existing
Line 57: infrastructure. This usually takes a large part of our initial effort because there
Line 58: is so much to get ready. With this infrastructure in place, we can implement the
Line 59: feature and make the test pass.
Line 60: An outline of the test we want is:
Line 61: 1.
Line 62: When an auction is selling an item,
Line 63: 2.
Line 64: And an Auction Sniper has started to bid in that auction,
Line 65: 3.
Line 66: Then the auction will receive a Join request from the Auction Sniper.
Line 67: 4.
Line 68: When an auction announces that it is Closed,
Line 69: 5.
Line 70: Then the Auction Sniper will show that it lost the auction.
Line 71: This describes one transition in the state machine (see Figure 10.1).
Line 72: We need to translate this into something executable. We use JUnit as our test
Line 73: framework since it’s familiar and widely supported. We also need mechanisms
Line 74: to control the application and the auction that the application is talking to.
Line 75: Southabee’s On-Line test services are not freely available. We have to book
Line 76: ahead and pay for each test session, which is not practical if we want to run tests
Line 77: all the time. We’ll need a fake auction service that we can control from our
Line 78: tests to behave like the real thing—or at least like we think the real thing behaves
Line 79: until we get a chance to test against it for real. This fake auction, or stub, will
Line 80: be as simple as we can make it. It will connect to an XMPP message broker,
Line 81: receive commands from the Sniper to be checked by the test, and allow the test
Line 82: to send back events. We’re not trying to reimplement all of Southabee’s On-Line,
Line 83: just enough of it to support test scenarios.
Line 84: Chapter 10
Line 85: The Walking Skeleton
Line 86: 84
Line 87: 
Line 88: --- 페이지 110 ---
Line 89: Figure 10.1
Line 90: A Sniper joins, then loses
Line 91: Controlling the Sniper application is more complicated. We want our skeleton
Line 92: test to exercise our application as close to end-to-end as possible, to show that
Line 93: the main() method initializes the application correctly and that the components
Line 94: really work together. This means that we should start by working through the
Line 95: publicly visible features of the application (in this case, its user interface) instead
Line 96: of directly invoking its domain objects. We also want our test to be clear about
Line 97: what is being checked, written in terms of the relationship between a Sniper and
Line 98: its auction, so we’ll hide all the messy code for manipulating Swing in an
Line 99: ApplicationRunner class. We’ll start by writing the test as if all the code it needs
Line 100: exists and will ﬁll in the implementations afterwards.
Line 101: public class AuctionSniperEndToEndTest {
Line 102:   private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");
Line 103:   private final ApplicationRunner application = new ApplicationRunner();
Line 104:   @Test public void sniperJoinsAuctionUntilAuctionCloses() throws Exception {
Line 105:     auction.startSellingItem();                 // Step 1
Line 106:     application.startBiddingIn(auction);        // Step 2
Line 107:     auction.hasReceivedJoinRequestFromSniper(); // Step 3
Line 108:     auction.announceClosed();                   // Step 4
Line 109:     application.showsSniperHasLostAuction();    // Step 5
Line 110:   }
Line 111: // Additional cleanup
Line 112:   @After public void stopAuction() {
Line 113:     auction.stop();
Line 114:   }
Line 115:   @After public void stopApplication() {
Line 116:     application.stop();
Line 117:   }
Line 118: }
Line 119: 85
Line 120: Our Very First Test
Line 121: 
Line 122: --- 페이지 111 ---
Line 123: We’ve adopted certain naming conventions for the methods of the helper ob-
Line 124: jects. If a method triggers an event to drive the test, its name will be a command,
Line 125: such as startBiddingIn(). If a method asserts that something should have hap-
Line 126: pened, its name will be descriptive;1 for example, showsSniperHasLostAuction()
Line 127: will throw an exception if the application is not showing the auction status as
Line 128: lost. JUnit will call the two stop() methods after the test has run, to clean up
Line 129: the runtime environment.
Line 130: In writing the test, one of the assumptions we’ve made is that a
Line 131: FakeAuctionServer is tied to a given item. This matches the structure of our
Line 132: intended architecture, where Southabee’s On-Line hosts multiple auctions, each
Line 133: selling a single item.
Line 134: One Domain at a Time
Line 135: The language of this test is concerned with auctions and Snipers; there’s nothing
Line 136: about messaging layers or components in the user interface—that’s all incidental
Line 137: detail here. Keeping the language consistent helps us understand what’s signiﬁcant
Line 138: in this test, with a nice side effect of protecting us when the implementation inevitably
Line 139: changes.
Line 140: Some Initial Choices
Line 141: Now we have to make the test pass, which will require a lot of preparation. We
Line 142: need to ﬁnd or write four components: an XMPP message broker, a stub auction
Line 143: that can communicate over XMPP, a GUI testing framework, and a test har-
Line 144: ness that can cope with our multithreaded, asynchronous architecture. We also
Line 145: have to get the project under version control with an automated build/deploy/test
Line 146: process. Compared to unit-testing a single class, there is a lot to do—but it’s es-
Line 147: sential. Even at this high level, the exercise of writing tests drives the development
Line 148: of the system. Working through our ﬁrst end-to-end test will force some of the
Line 149: structural decisions we need to make, such as packaging and deployment.
Line 150: First the package selection, we will need an XMPP message broker to let the
Line 151: application talk to our stub auction house. After some investigation, we decide
Line 152: on an open source implementation called Openﬁre and its associated client library
Line 153: Smack. We also need a high-level test framework that can work with Swing
Line 154: and Smack, both of which are multithreaded and event-driven. Luckily for us,
Line 155: there are several frameworks for testing Swing applications and the way that
Line 156: they deal with Swing’s multithreaded, event-driven architecture also works well
Line 157: with XMPP messaging. We pick WindowLicker which is open source and supports
Line 158: 1. For the grammatically pedantic, the names of methods that trigger events are in the
Line 159: imperative mood whereas the names of assertions are in the indicative mood.
Line 160: Chapter 10
Line 161: The Walking Skeleton
Line 162: 86
Line 163: 
Line 164: --- 페이지 112 ---
Line 165: the asynchronous approach that we need in our tests. When assembled, the
Line 166: infrastructure will look like Figure 10.2:
Line 167: Figure 10.2
Line 168: The end-to-end test rig
Line 169: End-to-End Testing
Line 170: End-to-end testing for event-based systems, such as our Sniper, has to cope with
Line 171: asynchrony. The tests run in parallel with the application and do not know pre-
Line 172: cisely when the application is or isn’t ready. This is unlike unit testing, where a
Line 173: test drives an object directly in the same thread and so can make direct assertions
Line 174: about its state and behavior.
Line 175: An end-to-end test can’t peek inside the target application, so it must wait to
Line 176: detect some visible effect, such as a user interface change or an entry in a log.
Line 177: The usual technique is to poll for the effect and fail if it doesn’t happen within
Line 178: a given time limit. There’s a further complexity in that the target application has
Line 179: to stabilize after the triggering event long enough for the test to catch the result.
Line 180: An asynchronous test waiting for a value that just ﬂashes on the screen will be
Line 181: too unreliable for an automated build, so a common technique is to control the
Line 182: application and step through the scenario. At each stage, the test waits for an
Line 183: assertion to pass, then sends an event to wake the application for the next step.
Line 184: See Chapter 14 for a full discussion of testing asynchronous behavior.
Line 185: All this makes end-to-end testing slower and more brittle (perhaps the test
Line 186: network is just busy today), so failures might need interpretation. We’ve heard
Line 187: of teams where timing-related tests have to fail several times in a row before
Line 188: they’re reported. This is unlike unit tests which must all pass every time.
Line 189: In our case, both Swing and the messaging infrastructure are asynchronous,
Line 190: so using WindowLicker (which polls for values) to drive the Sniper covers the
Line 191: natural asynchrony of our end-to-end testing.
Line 192: 87
Line 193: Some Initial Choices
Line 194: 
Line 195: --- 페이지 113 ---
Line 196: Ready to Start
Line 197: You might have noticed that we skipped over one point: this ﬁrst test is not really
Line 198: end-to-end. It doesn’t include the real auction service because that is not easily
Line 199: available. An important part of the test-driven development skills is judging where
Line 200: to set the boundaries of what to test and how to eventually cover everything. In
Line 201: this case, we have to start with a fake auction service based on the documentation
Line 202: from Southabee’s On-Line. The documentation might or might not be correct,
Line 203: so we will record that as a known risk in the project plan and schedule time to
Line 204: test against the real server as soon as we have enough functionality to complete
Line 205: a meaningful transaction—even if we end up buying a hideous (but cheap) pair
Line 206: of candlesticks in a real auction. The sooner we ﬁnd a discrepancy, the less code
Line 207: we will have based on that misunderstanding and the more time to ﬁx it.
Line 208: We’d better get on with it.
Line 209: Chapter 10
Line 210: The Walking Skeleton
Line 211: 88