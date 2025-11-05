# 7.5 Identify Relationships with Interfaces (pp.63-63)

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


