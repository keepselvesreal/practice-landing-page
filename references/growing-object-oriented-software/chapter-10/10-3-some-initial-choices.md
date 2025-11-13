# 10.3 Some Initial Choices (pp.86-89)

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


---
**Page 87**

the asynchronous approach that we need in our tests. When assembled, the
infrastructure will look like Figure 10.2:
Figure 10.2
The end-to-end test rig
End-to-End Testing
End-to-end testing for event-based systems, such as our Sniper, has to cope with
asynchrony. The tests run in parallel with the application and do not know pre-
cisely when the application is or isn’t ready. This is unlike unit testing, where a
test drives an object directly in the same thread and so can make direct assertions
about its state and behavior.
An end-to-end test can’t peek inside the target application, so it must wait to
detect some visible effect, such as a user interface change or an entry in a log.
The usual technique is to poll for the effect and fail if it doesn’t happen within
a given time limit. There’s a further complexity in that the target application has
to stabilize after the triggering event long enough for the test to catch the result.
An asynchronous test waiting for a value that just ﬂashes on the screen will be
too unreliable for an automated build, so a common technique is to control the
application and step through the scenario. At each stage, the test waits for an
assertion to pass, then sends an event to wake the application for the next step.
See Chapter 14 for a full discussion of testing asynchronous behavior.
All this makes end-to-end testing slower and more brittle (perhaps the test
network is just busy today), so failures might need interpretation. We’ve heard
of teams where timing-related tests have to fail several times in a row before
they’re reported. This is unlike unit tests which must all pass every time.
In our case, both Swing and the messaging infrastructure are asynchronous,
so using WindowLicker (which polls for values) to drive the Sniper covers the
natural asynchrony of our end-to-end testing.
87
Some Initial Choices


---
**Page 88**

Ready to Start
You might have noticed that we skipped over one point: this ﬁrst test is not really
end-to-end. It doesn’t include the real auction service because that is not easily
available. An important part of the test-driven development skills is judging where
to set the boundaries of what to test and how to eventually cover everything. In
this case, we have to start with a fake auction service based on the documentation
from Southabee’s On-Line. The documentation might or might not be correct,
so we will record that as a known risk in the project plan and schedule time to
test against the real server as soon as we have enough functionality to complete
a meaningful transaction—even if we end up buying a hideous (but cheap) pair
of candlesticks in a real auction. The sooner we ﬁnd a discrepancy, the less code
we will have based on that misunderstanding and the more time to ﬁx it.
We’d better get on with it.
Chapter 10
The Walking Skeleton
88


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


