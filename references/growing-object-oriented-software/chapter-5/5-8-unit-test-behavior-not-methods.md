# 5.8 Unit-Test Behavior, Not Methods (pp.43-44)

---
**Page 43**

we’re wrong. Second, more subtly, we ﬁnd that our emphasis on (or, perhaps,
mania for) expressing our intentions is fundamental for developing reliable,
maintainable systems—and for us that includes tests and failure messages. Taking
the trouble to generate a useful diagnostic helps us clarify what the test, and
therefore the code, is supposed to do. We look at error diagnostics and how to
improve them in Chapter 23.
Develop from the Inputs to the Outputs
We start developing a feature by considering the events coming into the system
that will trigger the new behavior. The end-to-end tests for the feature will simu-
late these events arriving. At the boundaries of our system, we will need to write
one or more objects to handle these events. As we do so, we discover that these
objects need supporting services from the rest of the system to perform their re-
sponsibilities. We write more objects to implement these services, and discover
what services these new objects need in turn.
In this way, we work our way through the system: from the objects that receive
external events, through the intermediate layers, to the central domain model,
and then on to other boundary objects that generate an externally visible response.
That might mean accepting some text and a mouse click and looking for a record
in a database, or receiving a message in a queue and looking for a ﬁle on a server.
It’s tempting to start by unit-testing new domain model objects and then trying
to hook them into the rest of the application. It seems easier at the start—we feel
we’re making rapid progress working on the domain model when we don’t have
to make it ﬁt into anything—but we’re more likely to get bitten by integration
problems later. We’ll have wasted time building unnecessary or incorrect func-
tionality, because we weren’t receiving the right kind of feedback when we were
working on it.
Unit-Test Behavior, Not Methods
We’ve learned the hard way that just writing lots of tests, even when it produces
high test coverage, does not guarantee a codebase that’s easy to work with. Many
developers who adopt TDD ﬁnd their early tests hard to understand when they
revisit them later, and one common mistake is thinking about testing methods.
A test called testBidAccepted() tells us what it does, but not what it’s for.
We do better when we focus on the features that the object under test should
provide, each of which may require collaboration with its neighbors and calling
more than one of its methods. We need to know how to use the class to achieve
a goal, not how to exercise all the paths through its code.
43
Unit-Test Behavior, Not Methods


---
**Page 44**

The Importance of Describing Behavior, Not API Features
Nat used to run a company that produced online advertising and branded content
for clients sponsoring sports teams. One of his clients sponsored a Formula One
racing team. Nat wrote a fun little game that simulated Formula One race strategies
for the client to put on the team’s website. It took him two weeks to write, from
initial idea to ﬁnal deliverable, and once he handed it over to the client he forgot
all about it.
It turned out, however, that the throw-away game was by far the most popular
content on the team’s website. For the next F1 season, the client wanted to capi-
talize on its success. They wanted the game to model the track of each Grand
Prix, to accommodate the latest F1 rules, to have a better model of car physics,
to simulate dynamic weather, overtaking, spin-outs, and more.
Nat had written the original version test-ﬁrst, so he expected it to be easy to
change. However, going back to the code, he found the tests very hard to under-
stand. He had written a test for each method of each object but couldn’t understand
from those tests how each object was meant to behave—what the responsibilities
of the object were and how the different methods of the object worked together.
It helps to choose test names that describe how the object behaves in the
scenario being tested. We look at this in more detail in “Test Names Describe
Features” (page 248).
Listen to the Tests
When writing unit and integration tests, we stay alert for areas of the code that
are difﬁcult to test. When we ﬁnd a feature that’s difﬁcult to test, we don’t just
ask ourselves how to test it, but also why is it difﬁcult to test.
Our experience is that, when code is difﬁcult to test, the most likely cause is
that our design needs improving. The same structure that makes the code difﬁcult
to test now will make it difﬁcult to change in the future. By the time that future
comes around, a change will be more difﬁcult still because we’ll have forgotten
what we were thinking when we wrote the code. For a successful system, it might
even be a completely different team that will have to live with the consequences
of our decisions.
Our response is to regard the process of writing tests as a valuable early
warning of potential maintenance problems and to use those hints to ﬁx a problem
while it’s still fresh. As Figure 5.3 shows, if we’re ﬁnding it hard to write the next
failing test, we look again at the design of the production code and often refactor
it before moving on.
Chapter 5
Maintaining the Test-Driven Cycle
44


