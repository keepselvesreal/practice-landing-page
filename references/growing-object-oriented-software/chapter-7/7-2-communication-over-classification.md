# 7.2 Communication over Classification (pp.58-59)

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


---
**Page 59**

Value Types
Before we go further, we want to revisit the distinction we described in “Values
and Objects” (page 13): values are immutable, so they’re simpler and have no
meaningful identity; objects have state, so they have identity and relationships
with each other.
The more code we write, the more we’re convinced that we should deﬁne
types to represent value concepts in the domain, even if they don’t do much. It
helps to create a consistent domain model that is more self-explanatory. If we
create, for example, an Item type in a system, instead of just using String, we can
ﬁnd all the code that’s relevant for a change without having to chase through the
method calls. Speciﬁc types also reduce the risk of confusion—as the Mars Climate
Orbiter disaster showed, feet and metres may both be represented as numbers
but they’re different things.1 Finally, once we have a type to represent a concept,
it usually turns out to be a good place to hang behavior, guiding us towards using
a more object-oriented approach instead of scattering related behavior across
the code.
We use three basic techniques for introducing value types, which we’ve called
(in a ﬁt of alliteration): breaking out, budding off, and bundling up.
Breaking out
When we ﬁnd that the code in an object is becoming complex, that’s often
a sign that it’s implementing multiple concerns and that we can break out
coherent units of behavior into helper types. There’s an example in “Tidying
Up the Translator” (page 135) where we break a class that handles incoming
messages into two parts: one to parse the message string, and one to interpret
the result of the parsing.
Budding off
When we want to mark a new domain concept in the code, we often introduce
a placeholder type that wraps a single ﬁeld, or maybe has no ﬁelds at all. As
the code grows, we ﬁll in more detail in the new type by adding ﬁelds and
methods. With each type that we add, we’re raising the level of abstraction
of the code.
Bundling up
When we notice that a group of values are always used together, we take
that as a suggestion that there’s a missing construct. A ﬁrst step might be to
create a new type with ﬁxed public ﬁelds—just giving the group a name
highlights the missing concept. Later we can migrate behavior to the new
1. In 1999, NASA’s Mars Climate Orbiter burned up in the planet’s atmosphere because,
amongst other problems, the navigation software confused metric with imperial units.
There’s a brief description at http://news.bbc.co.uk/1/hi/sci/tech/514763.stm.
59
Value Types


