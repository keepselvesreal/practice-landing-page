# 8.3 Mock Application Objects in Integration Tests (pp.71-75)

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


