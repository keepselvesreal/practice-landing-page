# 13.4 Defer Decisions (pp.136-137)

---
**Page 136**

This is an example of “breaking out” that we described in “Value Types”
(page 59). It may not be obvious, but AuctionEvent is a value: it’s
immutable and there are no interesting differences between two instances
with the same contents. This refactoring separates the concerns within
AuctionMessageTranslator: the top level deals with events and listeners, and
the inner object deals with parsing strings.
Encapsulate Collections
We’ve developed a habit of packaging up common types, such as collections, in
our own classes, even though Java generics avoid the need to cast objects. We’re
trying to use the language of the problem we’re working on, rather than the language
of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
incidental noise about looking up and parsing values.The second is written in terms
of auction events, so there’s less of a conceptual gap between the domain and
the code.
Our rule of thumb is that we try to limit passing around types with generics (the
types enclosed in angle brackets). Particularly when applied to collections, we view
it as a form of duplication. It’s a hint that there’s a domain concept that should be
extracted into a type.
Defer Decisions
There’s a technique we’ve used a couple of times now, which is to introduce a
null implementation of a method (or even a type) to get us through the next step.
This helps us focus on the immediate task without getting dragged into thinking
about the next signiﬁcant chunk of functionality. The null Auction, for example,
allowed us to plug in a new relationship we’d discovered in a unit test without
getting pulled into messaging issues. That, in turn, meant we could stop and
think about the dependencies between our objects without the pressure of having
a broken compilation.
Keep the Code Compiling
We try to minimize the time when we have code that does not compile by keeping
changes incremental. When we have compilation failures, we can’t be quite sure
where the boundaries of our changes are, since the compiler can’t tell us. This, in
turn, means that we can’t check in to our source repository, which we like to do
often.The more code we have open, the more we have to keep in our heads which,
ironically, usually means we move more slowly. One of the great discoveries of
test-driven development is just how ﬁne-grained our development steps can be.
Chapter 13
The Sniper Makes a Bid
136


---
**Page 137**

Emergent Design
What we hope is becoming clear from this chapter is how we’re growing a design
from what looks like an unpromising start. We alternate, more or less, between
adding features and reﬂecting on—and cleaning up—the code that results. The
cleaning up stage is essential, since without it we would end up with an unmain-
tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
what to do, conﬁdent that we will take the time when we’re ready. In the mean-
time, we keep our code as clean as possible, moving in small increments and using
techniques such as null implementation to minimize the time when it’s broken.
Figure 13.5 shows that we’re building up a layer around our core implementa-
tion that “protects” it from its external dependencies. We think this is just good
practice, but what’s interesting is that we’re getting there incrementally, by
looking for features in classes that either go together or don’t. Of course we’re
inﬂuenced by our experience of working on similar codebases, but we’re trying
hard to follow what the code is telling us instead of imposing our preconceptions.
Sometimes, when we do this, we ﬁnd that the domain takes us in the most
surprising directions.
137
Emergent Design


