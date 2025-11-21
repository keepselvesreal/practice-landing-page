# 7.1 How Writing a Test First Helps the Design (pp.57-58)

---
**Page 57**

Chapter 7
Achieving Object-Oriented
Design
In matters of style, swim with the current; in matters of principle, stand
like a rock.
—Thomas Jefferson
How Writing a Test First Helps the Design
The design principles we outlined in the previous chapter apply to ﬁnding the
right boundaries for an object so that it plays well with its neighbors—a caller
wants to know what an object does and what it depends on, but not how it
works. We also want an object to represent a coherent unit that makes sense in
its larger environment. A system built from such components will have the
ﬂexibility to reconﬁgure and adapt as requirements change.
There are three aspects of TDD that help us achieve this scoping. First, starting
with a test means that we have to describe what we want to achieve before we
consider how. This focus helps us maintain the right level of abstraction for the
target object. If the intention of the unit test is unclear then we’re probably
mixing up concepts and not ready to start coding. It also helps us with information
hiding as we have to decide what needs to be visible from outside the object.
Second, to keep unit tests understandable (and, so, maintainable), we have to
limit their scope. We’ve seen unit tests that are dozens of lines long, burying the
point of the test somewhere in its setup. Such tests tell us that the component
they’re testing is too large and needs breaking up into smaller components. The
resulting composite object should have a clearer separation of concerns as we
tease out its implicit structure, and we can write simpler tests for the extracted
objects.
Third, to construct an object for a unit test, we have to pass its dependencies
to it, which means that we have to know what they are. This encourages context
independence, since we have to be able to set up the target object’s environment
before we can unit-test it—a unit test is just another context. We’ll notice that
an object with implicit (or just too many) dependencies is painful to prepare for
testing—and make a point of cleaning it up.
In this chapter, we describe how we use an incremental, test-driven approach
to nudge our code towards the design principles we described in the previous
chapter.
57


---
**Page 58**

Communication over Classiﬁcation
As we wrote in Chapter 2, we view a running system as a web of communicating
objects, so we focus our design effort on how the objects collaborate to deliver
the functionality we need. Obviously, we want to achieve a well-designed class
structure, but we think the communication patterns between objects are more
important.
In languages such as Java, we can use interfaces to deﬁne the available messages
between objects, but we also need to deﬁne their patterns of communication—their
communication protocols. We do what we can with naming and convention, but
there’s nothing in the language to describe relationships between interfaces or
methods within an interface, which leaves a signiﬁcant part of the design implicit.
Interface and Protocol
Steve heard this useful distinction in a conference talk: an interface describes
whether two components will ﬁt together, while a protocol describes whether they
will work together.
We use TDD with mock objects as a technique to make these communication
protocols visible, both as a tool for discovering them during development and
as a description when revisiting the code. For example, the unit test towards the
end of Chapter 3 tells us that, given a certain input message, the translator
should call listener.auctionClosed() exactly once—and nothing else. Although
the listener interface has other methods, this test says that its protocol requires
that auctionClosed() should be called on its own.
@Test public void
notifiesAuctionClosedWhenCloseMessageReceived() {
  Message message = new Message();
  message.setBody("SOLVersion: 1.1; Event: CLOSE;");
  context.checking(new Expectations() {{ 
    oneOf(listener).auctionClosed(); 
  }});
  translator.processMessage(UNUSED_CHAT, message); 
}
TDD with mock objects also encourages information hiding. We should mock
an object’s peers—its dependencies, notiﬁcations, and adjustments we categorized
on page 52—but not its internals. Tests that highlight an object’s neighbors help
us to see whether they are peers, or should instead be internal to the target object.
A test that is clumsy or unclear might be a hint that we’ve exposed too much
implementation, and that we should rebalance the responsibilities between the
object and its neighbors.
Chapter 7
Achieving Object-Oriented Design
58


