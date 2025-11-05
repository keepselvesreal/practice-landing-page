# 7.4 Where Do Objects Come From? (pp.60-63)

---
**Page 60**

type, which might eventually allow us to hide its ﬁelds behind a clean
interface, satisfying the “composite simpler than the sum of its parts” rule.
We ﬁnd that the discovery of value types is usually motivated by trying to
follow our design principles, rather than by responding to code stresses when
writing tests.
Where Do Objects Come From?
The categories for discovering object types are similar (which is why we shoe-
horned them into these names), except that the design guidance we get from
writing unit tests tends to be more important. As we wrote in “External and
Internal Quality” (page 10), we use the effort of unit testing to maintain the
code’s internal quality. There are more examples of the inﬂuence of testing on
design in Chapter 20.
Breaking Out: Splitting a Large Object into a Group of
Collaborating Objects
When starting a new area of code, we might temporarily suspend our design
judgment and just write code without attempting to impose much structure. This
allows us to gain some experience in the area and test our understanding of any
external APIs we’re developing against. After a short while, we’ll ﬁnd our code
becoming too complex to understand and will want to clean it up. We can start
pulling out cohesive units of functionality into smaller collaborating objects,
which we can then unit-test independently. Splitting out a new object also forces
us to look at the dependencies of the code we’re pulling out.
We have two concerns about deferring cleanup. The ﬁrst is how long we should
wait before doing something. Under time pressure, it’s tempting to leave the un-
structured code as is and move on to the next thing (“after all, it works and it’s
just one class…”). We’ve seen too much code where the intention wasn’t clear
and the cost of cleanup kicked in when the team could least afford it. The second
concern is that occasionally it’s better to treat this code as a spike—once we
know what to do, just roll it back and reimplement cleanly. Code isn’t sacred
just because it exists, and the second time won’t take as long.
The Tests Say…
Break up an object if it becomes too large to test easily, or if its test failures become
difﬁcult to interpret. Then unit-test the new parts separately.
Chapter 7
Achieving Object-Oriented Design
60


---
**Page 61**

Looking Ahead…
In Chapter 12, when extracting an AuctionMessageTranslator, we avoid including
its interaction with MainWindow because that would give it too many responsibilities.
Looking at the behavior of the new class, we identify a missing dependency,
AuctionEventListener, which we deﬁne while writing the unit tests.We repackage
the existing code in Main to provide an implementation for the new interface.
AuctionMessageTranslator satisﬁes both our design heuristics: it introduces a
separation of concerns by splitting message translation from auction display, and
it abstracts message-handling code into a new domain-speciﬁc concept.
Budding Off: Deﬁning a New Service That an Object Needs and
Adding a New Object to Provide It
When the code is more stable and has some degree of structure, we often discover
new types by “pulling” them into existence. We might be adding behavior to an
object and ﬁnd that, following our design principles, some new feature doesn’t
belong inside it.
Our response is to create an interface to deﬁne the service that the object needs
from the object’s point of view. We write tests for the new behavior as if the
service already exists, using mock objects to help describe the relationship between
the target object and its new collaborator; this is how we introduced the
AuctionEventListener we mentioned in the previous section.
The development cycle goes like this. When implementing an object, we discover
that it needs a service to be provided by another object. We give the new service
a name and mock it out in the client object’s unit tests, to clarify the relationship
between the two. Then we write an object to provide that service and, in doing
so, discover what services that object needs. We follow this chain (or perhaps a
directed graph) of collaborator relationships until we connect up to existing ob-
jects, either our own or from a third-party API. This is how we implement
“Develop from the Inputs to the Outputs” (page 43).
We think of this as “on-demand” design: we “pull” interfaces and their imple-
mentations into existence from the needs of the client, rather than “pushing” out
the features that we think a class should provide.
The Tests Say…
When writing a test, we ask ourselves, “If this worked, who would know?” If the
right answer to that question is not in the target object, it’s probably time to introduce
a new collaborator.
61
Where Do Objects Come From?


---
**Page 62**

Looking Ahead…
In Chapter 13, we introduce an Auction interface. The concept of making a bid
would have been an additional responsibility for AuctionSniper, so we introduce
a new service for bidding—just an interface without any implementation.We write a
new test to show the relationship between AuctionSniper and Auction. Then we
write a concrete implementation of Auction—initially as an anonymous class in
Main, later as XMPPAuction.
Bundling Up: Hiding Related Objects into a Containing Object
This is the application of the “composite simpler than the sum of its parts” rule
(page 53). When we have a cluster of related objects that work together, we can
package them up in a containing object. The new object hides the complexity in
an abstraction that allows us to program at a higher level.
The process of making an implicit concept concrete has some other nice effects.
First, we have to give it a name which helps us understand the domain a little
better. Second, we can scope dependencies more clearly, since we can see the
boundaries of the concept. Third, we can be more precise with our unit testing.
We can test the new composite object directly, and use a mock implementation
to simplify the tests for code from which it was extracted (since, of course, we
added an interface for the role the new object plays).
The Tests Say…
When the test for an object becomes too complicated to set up—when there are
too many moving parts to get the code into the relevant state—consider bundling
up some of the collaborating objects. There’s an example in “Bloated Constructor”
(page 238).
Looking Ahead…
In Chapter 17, we introduce XMPPAuctionHouse to package up everything to do with
the messaging infrastructure, and SniperLauncher for constructing and attaching a
Sniper. Once extracted, the references to Swing behavior in SniperLauncher
stand out as inappropriate, so we introduce SniperCollector to decouple the
domains.
Chapter 7
Achieving Object-Oriented Design
62


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


