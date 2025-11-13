# 7.6 Refactor Interfaces Too (pp.63-64)

---
**Page 63**

Identify Relationships with Interfaces
We use Java interfaces more liberally than some other developers. This reﬂects
our emphasis on the relationships between objects, as deﬁned by their communi-
cation protocols. We use interfaces to name the roles that objects can play and
to describe the messages they’ll accept.
We also prefer interfaces to be as narrow as possible, even though that means
we need more of them. The fewer methods there are on an interface, the more
obvious is its role in the calling object. We don’t have to worry which other
methods are relevant to a particular call and which were included for convenience.
Narrow interfaces are also easier to write adapters and decorators for; there’s
less to implement, so it’s easier to write objects that compose together well.
“Pulling” interfaces into existence, as we described in “Budding Off,” helps
us keep them as narrow as possible. Driving an interface from its client avoids
leaking excess information about its implementers, which minimizes any implicit
coupling between objects and so keeps the code malleable.
Impl Classes Are Meaningless
Sometimes we see code with classes named by adding “Impl” to the single interface
they implement. This is better than leaving the class name unchanged and
preﬁxing an “I” to the interface, but not by much. A name like BookingImpl is dupli-
cation; it says exactly the same as implements Booking, which is a “code smell.”
We would not be happy with such obvious duplication elsewhere in our code,
so we ought to refactor it away.
It might just be a naming problem. There’s always something speciﬁc about an
implementation that can be included in the class name: it might use a bounded
collection, communicate over HTTP, use a database for persistence, and so on.
A bridging class is even easier to name, since it will belong in one domain but
implement interfaces in another.
If there really isn’t a good implementation name, it might mean that the interface
is poorly named or designed. Perhaps it’s unfocused because it has too many re-
sponsibilities; or it’s named after its implementation rather than its role in the client;
or it’s a value, not an object—this discrepancy sometimes turns up when writing
unit tests, see “Don’t Mock Values” (page 237).
Refactor Interfaces Too
Once we have interfaces for protocols, we can start to pay attention to similarities
and differences. In a reasonably large codebase, we often start to ﬁnd interfaces
that look similar. This means we should look at whether they represent a single
concept and should be merged. Extracting common roles makes the design more
63
Refactor Interfaces Too


---
**Page 64**

malleable because more components will be “plug-compatible,” so we can work
at a higher level of abstraction. For the developer, there’s a secondary advantage
that there will be fewer concepts that cost time to understand.
Alternatively, if similar interfaces turn out to represent different concepts, we
can make a point of making them distinct, so that the compiler can ensure that
we only combine objects correctly. A decision to separate similar-looking inter-
faces is a good time to reconsider their naming. It’s likely that there’s a more
appropriate name for at least one of them.
Finally, another time to consider refactoring interfaces is when we start imple-
menting them. For example, if we ﬁnd that the structure of an implementing class
is unclear, perhaps it has too many responsibilities which might be a hint that
the interface is unfocused too and should be split up.
Compose Objects to Describe System Behavior
TDD at the unit level guides us to decompose our system into value types and
loosely coupled computational objects. The tests give us a good understanding
of how each object behaves and how it can be combined with others. We then
use lower-level objects as the building blocks of more capable objects; this is the
web of objects we described in Chapter 2.
In jMock, for example, we assemble a description of the expected calls for a
test in a context object called a Mockery. During a test run, the Mockery will pass
calls made to any of its mocked objects to its Expectations, each of which will
attempt to match the call. If an Expectation matches, that part of the test suc-
ceeds. If none matches, then each Expectation reports its disagreement and the
test fails. At runtime, the assembled objects look like Figure 7.1:
Figure 7.1
jMock Expectations are assembled from many objects
The advantage of this approach is that we end up with a ﬂexible application
structure built from relatively little code. It’s particularly suitable where the code
has to support many related scenarios. For each scenario, we provide a different
Chapter 7
Achieving Object-Oriented Design
64


