# 5.6 Watch the Test Fail (pp.42-43)

---
**Page 42**

Write the Test That You’d Want to Read
We want each test to be as clear as possible an expression of the behavior to be
performed by the system or object. While writing the test, we ignore the fact that
the test won’t run, or even compile, and just concentrate on its text; we act as
if the supporting code to let us run the test already exists.
When the test reads well, we then build up the infrastructure to support the
test. We know we’ve implemented enough of the supporting code when the test
fails in the way we’d expect, with a clear error message describing what needs
to be done. Only then do we start writing the code to make the test pass. We
look further at making tests readable in Chapter 21.
Watch the Test Fail
We always watch the test fail before writing the code to make it pass, and check
the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
misunderstood something or the code is incomplete, so we ﬁx that. When we get
the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
tion isn’t clear, someone (probably us) will have to struggle when the code breaks
in a few weeks’ time. We adjust the test code and rerun the tests until the error
messages guide us to the problem with the code (Figure 5.2).
Figure 5.2
Improving the diagnostics as part of the TDD cycle
As we write the production code, we keep running the test to see our progress
and to check the error diagnostics as the system is built up behind the test. Where
necessary, we extend or modify the support code to ensure the error messages
are always clear and relevant.
There’s more than one reason for insisting on checking the error messages.
First, it checks our assumptions about the code we’re working on—sometimes
Chapter 5
Maintaining the Test-Driven Cycle
42


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


