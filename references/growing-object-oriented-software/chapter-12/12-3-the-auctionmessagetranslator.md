# 12.3 The AuctionMessageTranslator (pp.112-118)

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


---
**Page 113**

We already have such a class in Main—it’s anonymous and its responsibilities
aren’t very obvious:
new MessageListener() {
  public void processMessage(Chat aChat, Message message) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
This code implicitly accepts a Close message (the only kind of message we
have so far) and implements the Sniper’s response. We’d like to make this situation
explicit before we add more features. We start by promoting the anonymous
class to a top-level class in its own right, which means it needs a name. From our
description in the paragraph above, we pick up the word “translate” and call it
an AuctionMessageTranslator, because it will translate messages from the auction.
The catch is that the current anonymous class picks up the ui ﬁeld from Main.
We’ll have to attach something to our newly promoted class so that it can respond
to a message. The most obvious thing to do is pass it the MainWindow but we’re
unhappy about creating a dependency on a user interface component. That would
make it hard to unit-test, because we’d have to query the state of a component
that’s running in the Swing event thread.
More signiﬁcantly, such a dependency would break the “single responsibility”
principle which says that unpacking raw messages from the auction is quite
enough for one class to do, without also having to know how to present the
Sniper status. As we wrote in “Designing for Maintainability” (page 47), we
want to maintain a separation of concerns.
Given these constraints, we decide that our new AuctionMessageTranslator
will delegate the handling of an interpreted event to a collaborator, which we will
represent with an AuctionEventListener interface; we can pass an object that
implements it into the translator on construction. We don’t yet know what’s in
this interface and we haven’t yet begun to think about its implementation. Our
immediate concern is to get the message translation to work; the rest can wait.
So far the design looks like Figure 12.1 (types that belong to external frameworks,
such as Chat, are shaded):
Figure 12.1
The AuctionMessageTranslator
113
The AuctionMessageTranslator


---
**Page 114**

The First Unit Test
We start with the simpler event type. As we’ve seen, a Close event has no
values—it’s a simple trigger. When the translator receives one, we want it to call
its listener appropriately.
As this is our ﬁrst unit test, we’ll build it up very slowly to show the process
(later, we will move faster). We start with the test method name. JUnit picks up
test methods by reﬂection, so we can make their names as long and descriptive
as we like because we never have to include them in code. The ﬁrst test says that
the translator will tell anything that’s listening that the auction has closed when
it receives a raw Close message.
package test.auctionsniper;
public class AuctionMessageTranslatorTest {
  @Test public void
notifiesAuctionClosedWhenCloseMessageReceived() {
// nothing yet
  }
}
Put Tests in a Different Package
We’ve adopted a habit of putting tests in a different package from the code they’re
exercising.We want to make sure we’re driving the code through its public interfaces,
like any other client, rather than opening up a package-scoped back door for testing.
We also ﬁnd that, as the application and test code grows, separate packages make
navigation in modern IDEs easier.
The next step is to add the action that will trigger the behavior we want to
test—in this case, sending a Close message. We already know what this will look
like since it’s a call to the Smack MessageListener interface.
public class AuctionMessageTranslatorTest {
  public static final Chat UNUSED_CHAT = null;
private final AuctionMessageTranslator translator = 
                                              new AuctionMessageTranslator();
  @Test public void
notfiesAuctionClosedWhenCloseMessageReceived() {
Message message = new Message();
    message.setBody("SOLVersion: 1.1; Event: CLOSE;");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
Chapter 12
Getting Ready to Bid
114


---
**Page 115**

Use null When an Argument Doesn’t Matter
UNUSED_CHAT is a meaningful name for a constant that is deﬁned as null.We pass
it into processMessage() instead of a real Chat object because the Chat class is
difﬁcult to instantiate—its constructor is package-scoped and we’d have to ﬁll in a
chain of dependencies to create one. As it happens, we don’t need one anyway
for the current functionality, so we just pass in a null value to satisfy the compiler
but use a named constant to make clear its signiﬁcance.
To be clear, this null is not a null object [Woolf98] which may be called and will
do nothing in response. This null is just a placeholder and will fail if called during
the test.
We generate a skeleton implementation from the MessageListener interface.
package auctionsniper;
public class AuctionMessageTranslator implements MessageListener {
  public void processMessage(Chat chat, Message message) {
// TODO Fill in here
  }
}
Next, we want a check that shows whether the translation has taken
place—which should fail since we haven’t implemented anything yet. We’ve al-
ready decided that we want our translator to notify its listener when the Close
event occurs, so we’ll describe that expected behavior in our test.
@RunWith(JMock.class) 
public class AuctionMessageTranslatorTest {
  private final Mockery context = new Mockery();
  private final AuctionEventListener listener = 
                              context.mock(AuctionEventListener.class); 
  private final AuctionMessageTranslator translator = 
                                        new AuctionMessageTranslator();
  @Test public void
notfiesAuctionClosedWhenCloseMessageReceived() {
    context.checking(new Expectations() {{
oneOf(listener).auctionClosed();
    }});
    Message message = new Message();
    message.setBody("SOLVersion: 1.1; Event: CLOSE;");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
115
The AuctionMessageTranslator


---
**Page 116**

This is more or less the kind of unit test we described at the end of Chapter 2,
so we won’t go over its structure again here except to emphasize the highlighted
expectation line. This is the most signiﬁcant line in the test, our declaration of
what matters about the translator’s effect on its environment. It says that when
we send an appropriate message to the translator, we expect it to call the listener’s
auctionClosed() method exactly once.
We get a failure that shows that we haven’t implemented the behavior we need:
not all expectations were satisfied
expectations:
  ! expected once, never invoked: auctionEventListener.auctionClosed()
what happened before this: nothing!
  at org.jmock.Mockery.assertIsSatisfied(Mockery.java:199)
  […]
  at org.junit.internal.runners.JUnit4ClassRunner.run()
The critical phrase is this one:
expected once, never invoked: auctionEventListener.auctionClosed()
which tells us that we haven’t called the listener as we should have.
We need to do two things to make the test pass. First, we need to connect the
translator and listener so that they can communicate. We decide to pass the lis-
tener into the translator’s constructor; it’s simple and ensures that the translator
is always set up correctly with a listener—the Java type system won’t let us forget.
The test setup looks like this:
public class AuctionMessageTranslatorTest {
  private final Mockery context = new Mockery();
  private final AuctionEventListener listener = 
                                     context.mock(AuctionEventListener.class);
  private final AuctionMessageTranslator translator = 
                                       new AuctionMessageTranslator(listener);
The second thing we need to do is call the auctionClosed() method. Actually,
that’s all we need to do to make this test pass, since we haven’t deﬁned any other
behavior.
public void processMessage(Chat chat, Message message) {
    listener.auctionClosed();
  }
The test passes. This might feel like cheating since we haven’t actually unpacked
a message. What we have done is ﬁgured out where the pieces are and got them
into a test harness—and locked down one piece of functionality that should
continue to work as we add more features.
Chapter 12
Getting Ready to Bid
116


---
**Page 117**

Simpliﬁed Test Setup
You might have noticed that all the ﬁelds in the test class are final. As we described
in Chapter 3, JUnit creates a new instance of the test class for each test method,
so the ﬁelds are recreated for each test method. We exploit this by declaring as
many ﬁelds as possible as final and initializing them during construction, which
ﬂushes out any circular dependencies. Steve likes to think of this visually as creating
a lattice of objects that acts a frame to support the test.
Sometimes, as you’ll see later in this example, we can’t lock everything down and
have to attach a dependency directly, but most of the time we can. Any exceptions
will attract our attention and highlight a possible dependency loop. NUnit, on the
other hand, reuses the same instance of the test class, so in that case we’d have
to renew any supporting test values and objects explicitly.
Closing the User Interface Loop
Now we have the beginnings of our new component, we can retroﬁt it into
the Sniper to make sure we don’t drift too far from working code. Previously,
Main updated the Sniper user interface, so now we make it implement
AuctionEventListener and move the functionality to the new auctionClosed()
method.
public class Main implements AuctionEventListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
new AuctionMessageTranslator(this));
    chat.sendMessage(JOIN_COMMAND_FORMAT);
    notToBeGCd = chat; 
  }
  public void auctionClosed() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
The structure now looks like Figure 12.2.
117
The AuctionMessageTranslator


---
**Page 118**

Figure 12.2
Introducing the AuctionMessageTranslator
What Have We Achieved?
In this baby step, we’ve extracted a single feature of our application into a separate
class, which means the functionality now has a name and can be unit-tested.
We’ve also made Main a little simpler, now that it’s no longer concerned with
interpreting the text of messages from the auction. This is not yet a big deal but
we will show, as the Sniper application grows, how this approach helps us keep
code clean and ﬂexible, with clear responsibilities and relationships between its
components.
Unpacking a Price Message
Introducing Message Event Types
We’re about to introduce a second auction message type, the current price update.
The Sniper needs to distinguish between the two, so we take another look at the
message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
simple—just a single line with a few name/value pairs. Here are examples for
the formats again:
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Event: CLOSE;
At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
types, but we’re not clear enough about the behavior to justify any meaningful
structure, so we back off the idea. We decide to start with a simplistic solution
and adapt from there.
The Second Test
The introduction of a different Price event in our second test will force us to
parse the incoming message. This test has the same structure as the ﬁrst one but
gets a different input string and expects us to call a different method on the lis-
tener. A Price message includes details of the last bid, which we need to unpack
and pass to the listener, so we include them in the signature of the new method
currentPrice(). Here’s the test:
@Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Chapter 12
Getting Ready to Bid
118


