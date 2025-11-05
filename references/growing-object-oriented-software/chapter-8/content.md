# Chapter 8: Building on Third-Party Code (pp.69-75)

---
**Page 69**

Chapter 8
Building on Third-Party Code
Programming today is all about doing science on the parts you have
to work with.
—Gerald Jay Sussman
Introduction
We’ve shown how we pull a system’s design into existence: discovering what our
objects need and writing interfaces and further objects to meet those needs. This
process works well for new functionality. At some point, however, our design
will come up against a need that is best met by third-party code: standard APIs,
open source libraries, or vendor products. The critical point about third-party
code is that we don’t control it, so we cannot use our process to guide its design.
Instead, we must focus on the integration between our design and the
external code.
In integration, we have an abstraction to implement, discovered while we de-
veloped the rest of the feature. With the third-party API pushing back at our
design, we must ﬁnd the best balance between elegance and practical use of
someone else’s ideas. We must check that we are using the third-party API cor-
rectly, and adjust our abstraction to ﬁt if we ﬁnd that our assumptions are
incorrect.
Only Mock Types That You Own
Don’t Mock Types You Can’t Change
When we use third-party code we often do not have a deep understanding of
how it works. Even if we have the source available, we rarely have time to read
it thoroughly enough to explore all its quirks. We can read its documentation,
which is often incomplete or incorrect. The software may also have bugs that we
will need to work around. So, although we know how we want our abstraction
to behave, we don’t know if it really does so until we test it in combination with
the third-party code.
We also prefer not to change third-party code, even when we have the sources.
It’s usually too much trouble to apply private patches every time there’s a new
version. If we can’t change an API, then we can’t respond to any design feedback
we get from writing unit tests that touch it. Whatever alarm bells the unit tests
69


---
**Page 70**

might be ringing about the awkwardness of an external API, we have to live with
it as it stands.
This means that providing mock implementations of third-party types is of
limited use when unit-testing the objects that call them. We ﬁnd that tests that
mock external libraries often need to be complex to get the code into the right
state for the functionality we need to exercise. The mess in such tests is telling
us that the design isn’t right but, instead of ﬁxing the problem by improving the
code, we have to carry the extra complexity in both code and test.
A second risk is that we have to be sure that the behavior we stub or mock
matches what the external library will actually do. How difﬁcult this is depends
on the quality of the library—whether it’s speciﬁed (and implemented) well
enough for us to be certain that our unit tests are valid. Even if we get it right
once, we have to make sure that the tests remain valid when we upgrade the
libraries.
Write an Adapter Layer
If we don’t want to mock an external API, how can we test the code that drives
it? We will have used TDD to design interfaces for the services our objects
need—which will be deﬁned in terms of our objects’ domain, not the external
library.
We write a layer of adapter objects (as described in [Gamma94]) that uses the
third-party API to implement these interfaces, as in Figure 8.1. We keep this
layer as thin as possible, to minimize the amount of potentially brittle and hard-
to-test code. We test these adapters with focused integration tests to conﬁrm our
understanding of how the third-party API works. There will be relatively few
integration tests compared to the number of unit tests, so they should not get in
the way of the build even if they’re not as fast as the in-memory unit tests.
Figure 8.1
Mockable adapters to third-party objects
Following this approach consistently produces a set of interfaces that deﬁne
the relationship between our application and the rest of the world in our
application’s terms and discourages low-level technical concepts from leaking
Chapter 8
Building on Third-Party Code
70


---
**Page 71**

into the application domain model. In Chapter 25, we discuss a common example
where abstractions in the application’s domain model are implemented using a
persistence API.
There are some exceptions where mocking third-party libraries can be helpful.
We might use mocks to simulate behavior that is hard to trigger with the real
library, such as throwing exceptions. Similarly, we might use mocks to test a se-
quence of calls, for example making sure that a transaction is rolled back if there’s
a failure. There should not be many tests like this in a test suite.
This pattern does not apply to value types because, of course, we don’t need
to mock them. We still, however, have to make design decisions about how
much to use third-party value types in our code. They might be so fundamental
that we just use them directly. Often, however, we want to follow the same
principles of isolation as for third-party services, and translate between value
types appropriate to the application domain and to the external domain.
Mock Application Objects in Integration Tests
As described above, adapter objects are passive, reacting to calls from our code.
Sometimes, adapter objects must call back to objects from the application. Event-
based libraries, for example, usually expect the client to provide a callback object
to be notiﬁed when an event happens. In this case, the application code will give
the adapter its own event callback (deﬁned in terms of the application domain).
The adapter will then pass an adapter callback to the external library to receive
external events and translate them for the application callback.
In these cases, we do use mock objects when testing objects that integrate with
third-party code—but only to mock the callback interfaces deﬁned in the appli-
cation, to verify that the adapter translates events between domains correctly
(Figure 8.2).
Multithreading adds more complication to integration tests. For example,
third-party libraries may start background threads to deliver events to the appli-
cation code, so synchronization is a vital aspect of the design effort of adapter
layers; we discuss this further in Chapter 26.
Figure 8.2
Using mock objects in integration tests
71
Mock Application Objects in Integration Tests


---
**Page 72**

This page intentionally left blank 


---
**Page 73**

Part III
A Worked Example
One of our goals in writing this book was to convey the whole
experience of test-driven software development. We want to
show how the techniques ﬁt together over a larger scale than
the examples usually presented in books. We make a point of
including external components, in this case Swing and messaging
infrastructure, since the stress points of this kind of approach
are usually at the boundaries between code that we own and
code that we have to work with. The application that we build
includes such complexities as event-based design, multiple
threads, and distribution.
Another goal was to tell a realistic story, so we include
episodes where we have to backtrack on decisions that turn out
to be wrong. This happens in any software development that
we’ve seen. Even the best people misunderstand requirements
and technologies or, sometimes, just miss the point. A resilient
process allows for mistakes and includes techniques for discov-
ering and recovering from errors as early as possible. After all,
the only alternative is to leave the problems in the code where,
generally, they will cause more expensive damage later.
Finally, we wanted to emphasize our culture of very incremen-
tal development. Experienced teams can learn to make substan-
tial changes to their code in small, safe steps. To those not used
to it, incremental change can feel as if it takes too long. But
we’ve been burned too often by large restructurings that lose
their way and end up taking longer—unpredictably so. By
keeping the system always clean and always working, we can
focus on just the immediate change at hand (instead of having
to maintain a mental model of all the code at once), and merging
changes back in is never a crisis.
On formatting
Some of the code and output layout in this example looks a bit odd.
We’ve had to trim and wrap the long lines to make them ﬁt on the
printed page. In our development environments we use a longer line
length, which (we think) makes for more readable layout of the code.
==STARTINDEX
id/ch09-d21e17/pageno/73
==ENDINDEX


---
**Page 74**

This page intentionally left blank 


---
**Page 75**

Chapter 9
Commissioning an Auction
Sniper
To Begin at the Beginning
In which we are commissioned to build an application that automati-
cally bids in auctions. We sketch out how it should work and what
the major components should be. We put together a rough plan for the
incremental steps in which we will grow the application.
We’re a development team for Markup and Gouge, a company that buys antiques
on the professional market to sell to clients “with the best possible taste.” Markup
and Gouge has been following the industry and now does a lot of its buying on-
line, largely from Southabee’s, a venerable auction house that is keen to grow
online. The trouble is that our buyers are spending a lot of their time manually
checking the state of an auction to decide whether or not to bid, and even missed
a couple of attractive items because they could not respond quickly enough.
After intense discussion, the management decides to commission an Auction
Sniper, an application that watches online auctions and automatically bids
slightly higher whenever the price changes, until it reaches a stop-price or the
auction closes. The buyers are keen to have this new application and some of
them agree to help us clarify what to build.
We start by talking through their ideas with the buyers’ group and ﬁnd that,
to avoid confusion, we need to agree on some basic terms:
•
Item is something that can be identiﬁed and bought.
•
Bidder is a person or organization that is interested in buying an item.
•
Bid is a statement that a bidder will pay a given price for an item.
•
Current price is the current highest bid for the item.
•
Stop price is the most a bidder is prepared to pay for an item.
•
Auction is a process for managing bids for an item.
•
Auction house is an institution that hosts auctions.
75


