# 5.7 Develop from the Inputs to the Outputs (pp.43-43)

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


