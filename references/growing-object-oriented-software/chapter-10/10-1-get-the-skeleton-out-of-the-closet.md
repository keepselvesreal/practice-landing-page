# 10.1 Get the Skeleton out of the Closet (pp.83-84)

---
**Page 83**

Chapter 10
The Walking Skeleton
In which we set up our development environment and write our ﬁrst
end-to-end test. We make some infrastructure choices that allow us to
get started, and construct a build. We’re surprised, yet again, at how
much effort this takes.
Get the Skeleton out of the Closet
So now we’ve got an idea of what to build, can we get on with it and write our
ﬁrst unit test?
Not yet.
Our ﬁrst task is to create the “walking skeleton” we described in “First, Test
a Walking Skeleton” (page 32). Again, the point of the walking skeleton is to
help us understand the requirements well enough to propose and validate a broad-
brush system structure. We can always change our minds later, when we learn
more, but it’s important to start with something that maps out the landscape of
our solution. Also, it’s very important to be able to assess the approach we’ve
chosen and to test our decisions so we can make changes with conﬁdence later.
For most projects, developing the walking skeleton takes a surprising amount
of effort. First, because deciding what to do will ﬂush out all sorts of questions
about the application and its place in the world. Second, because the automation
of building, packaging, and deploying into a production-like environment (once
we know what that means) will ﬂush out all sorts of technical and organizational
questions.
Iteration Zero
In most Agile projects, there’s a ﬁrst stage where the team is doing initial analysis,
setting up its physical and technical environments, and otherwise getting started.
The team isn’t adding much visible functionality since almost all the work is infra-
structure, so it might not make sense to count this as a conventional iteration for
scheduling purposes. A common practice is to call this step iteration zero: “iteration”
because the team still needs to time-box its activities and “zero” because it’s before
functional development starts in iteration one. One important task for iteration zero
is to use the walking skeleton to test-drive the initial architecture.
Of course, we start our walking skeleton by writing a test.
83


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


