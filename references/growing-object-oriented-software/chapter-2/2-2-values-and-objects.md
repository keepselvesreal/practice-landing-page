# 2.2 Values and Objects (pp.13-14)

---
**Page 13**

Chapter 2
Test-Driven Development with
Objects
Music is the space between the notes.
—Claude Debussy
A Web of Objects
Object-oriented design focuses more on the communication between objects than
on the objects themselves. As Alan Kay [Kay98] wrote:
The big idea is “messaging” […] The key in making great and growable systems is
much more to design how its modules communicate rather than what their internal
properties and behaviors should be.
An object communicates by messages: It receives messages from other objects
and reacts by sending messages to other objects as well as, perhaps, returning a
value or exception to the original sender. An object has a method of handling
every type of message that it understands and, in most cases, encapsulates some
internal state that it uses to coordinate its communication with other objects.
An object-oriented system is a web of collaborating objects. A system is built
by creating objects and plugging them together so that they can send messages
to one another. The behavior of the system is an emergent property of the
composition of the objects—the choice of objects and how they are connected
(Figure 2.1).
This lets us change the behavior of the system by changing the composition of
its objects—adding and removing instances, plugging different combinations
together—rather than writing procedural code. The code we write to manage
this composition is a declarative deﬁnition of the how the web of objects will
behave. It’s easier to change the system’s behavior because we can focus on what
we want it to do, not how.
Values and Objects
When designing a system, it’s important to distinguish between values that
model unchanging quantities or measurements, and objects that have an identity,
might change state over time, and model computational processes. In the
13


---
**Page 14**

Figure 2.1
A web of objects
object-oriented languages that most of us use, the confusion is that both concepts
are implemented by the same language construct: classes.
Values are immutable instances that model ﬁxed quantities. They have no in-
dividual identity, so two value instances are effectively the same if they have the
same state. This means that it makes no sense to compare the identity of two
values; doing so can cause some subtle bugs—think of the different ways of
comparing two copies of new Integer(999). That’s why we’re taught to use
string1.equals(string2) in Java rather than string1 == string2.
Objects, on the other hand, use mutable state to model their behavior over
time. Two objects of the same type have separate identities even if they have ex-
actly the same state now, because their states can diverge if they receive different
messages in the future.
In practice, this means that we split our system into two “worlds”: values,
which are treated functionally, and objects, which implement the stateful behavior
of the system. In Part III, you’ll see how our coding style varies depending on
which world we’re working in.
In this book, we will use the term object to refer only to instances with identity,
state, and processing—not values. There doesn’t appear to be another accepted
term that isn’t overloaded with other meanings (such as entity and process).
Follow the Messages
We can beneﬁt from this high-level, declarative approach only if our objects are
designed to be easily pluggable. In practice, this means that they follow common
communication patterns and that the dependencies between them are made ex-
plicit. A communication pattern is a set of rules that govern how a group of ob-
jects talk to each other: the roles they play, what messages they can send and
when, and so on. In languages like Java, we identify object roles with (abstract)
interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
everything we need to say.
Chapter 2
Test-Driven Development with Objects
14


