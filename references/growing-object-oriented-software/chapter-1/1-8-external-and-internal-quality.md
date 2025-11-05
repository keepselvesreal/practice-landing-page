# 1.8 External and Internal Quality (pp.10-13)

---
**Page 10**

There’s been a lot of discussion in the TDD world over the terminology for
what we’re calling acceptance tests: “functional tests,” “customer tests,” “system
tests.” Worse, our deﬁnitions are often not the same as those used by professional
software testers. The important thing is to be clear about our intentions. We use
“acceptance tests” to help us, with the domain experts, understand and agree on
what we are going to build next. We also use them to make sure that we haven’t
broken any existing features as we continue developing.
Our preferred implementation of the “role” of acceptance testing is to write
end-to-end tests which, as we just noted, should be as end-to-end as possible;
our bias often leads us to use these terms interchangeably although, in some
cases, acceptance tests might not be end-to-end.
We use the term integration tests to refer to the tests that check how some of
our code works with code from outside the team that we can’t change. It might
be a public framework, such as a persistence mapper, or a library from another
team within our organization. The distinction is that integration tests make sure
that any abstractions we build over third-party code work as we expect. In a
small system, such as the one we develop in Part III, acceptance tests might be
enough. In most professional development, however, we’ll want integration tests
to help tease out conﬁguration issues with the external packages, and to give
quicker feedback than the (inevitably) slower acceptance tests.
We won’t write much more about techniques for acceptance and integration
testing, since both depend on the technologies involved and even the culture of
the organization. You’ll see some examples in Part III which we hope give a sense
of the motivation for acceptance tests and show how they ﬁt in the development
cycle. Unit testing techniques, however, are speciﬁc to a style of programming,
and so are common across all systems that take that approach—in our case, are
object-oriented.
External and Internal Quality
There’s another way of looking at what the tests can tell us about a system. We
can make a distinction between external and internal quality: External quality
is how well the system meets the needs of its customers and users (is it functional,
reliable, available, responsive, etc.), and internal quality is how well it meets the
needs of its developers and administrators (is it easy to understand, easy to change,
etc.). Everyone can understand the point of external quality; it’s usually part of
the contract to build. The case for internal quality is equally important but is
often harder to make. Internal quality is what lets us cope with continual and
unanticipated change which, as we saw at the beginning of this chapter, is a fact
of working with software. The point of maintaining internal quality is to allow
us to modify the system’s behavior safely and predictably, because it minimizes
the risk that a change will force major rework.
Chapter 1
What Is the Point of Test-Driven Development?
10


---
**Page 11**

Running end-to-end tests tells us about the external quality of our system, and
writing them tells us something about how well we (the whole team) understand
the domain, but end-to-end tests don’t tell us how well we’ve written the code.
Writing unit tests gives us a lot of feedback about the quality of our code, and
running them tells us that we haven’t broken any classes—but, again, unit tests
don’t give us enough conﬁdence that the system as a whole works. Integration
tests fall somewhere in the middle, as in Figure 1.3.
Figure 1.3
Feedback from tests
Thorough unit testing helps us improve the internal quality because, to be
tested, a unit has to be structured to run outside the system in a test ﬁxture. A
unit test for an object needs to create the object, provide its dependencies, interact
with it, and check that it behaved as expected. So, for a class to be easy to unit-
test, the class must have explicit dependencies that can easily be substituted and
clear responsibilities that can easily be invoked and veriﬁed. In software engineer-
ing terms, that means that the code must be loosely coupled and highly
cohesive—in other words, well-designed.
When we’ve got this wrong—when a class, for example, is tightly coupled to
distant parts of the system, has implicit dependencies, or has too many or unclear
responsibilities—we ﬁnd unit tests difﬁcult to write or understand, so writing a
test ﬁrst gives us valuable, immediate feedback about our design. Like everyone,
we’re tempted not to write tests when our code makes it difﬁcult, but we try to
resist. We use such difﬁculties as an opportunity to investigate why the test is
hard to write and refactor the code to improve its structure. We call this “listening
to the tests,” and we’ll work through some common patterns in Chapter 20.
11
External and Internal Quality


---
**Page 12**

Coupling and Cohesion
Coupling and cohesion are metrics that (roughly) describe how easy it will be to
change the behavior of some code.They were described by Larry Constantine in
[Yourdon79].
Elements are coupled if a change in one forces a change in the other. For example,
if two classes inherit from a common parent, then a change in one class might
require a change in the other. Think of a combo audio system: It’s tightly coupled
because if we want to change from analog to digital radio, we must rebuild the
whole system. If we assemble a system from separates, it would have low coupling
and we could just swap out the receiver. “Loosely” coupled features (i.e., those
with low coupling) are easier to maintain.
An element’s cohesion is a measure of whether its responsibilities form a mean-
ingful unit. For example, a class that parses both dates and URLs is not coherent,
because they’re unrelated concepts.Think of a machine that washes both clothes
and dishes—it’s unlikely to do both well.2 At the other extreme, a class that parses
only the punctuation in a URL is unlikely to be coherent, because it doesn’t repre-
sent a whole concept. To get anything done, the programmer will have to ﬁnd
other parsers for protocol, host, resource, and so on. Features with “high”
coherence are easier to maintain.
2. Actually, there was a combined clothes and dishwasher.The “Thor Automagic” was
manufactured in the 1940s, but the idea hasn’t survived.
Chapter 1
What Is the Point of Test-Driven Development?
12


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


