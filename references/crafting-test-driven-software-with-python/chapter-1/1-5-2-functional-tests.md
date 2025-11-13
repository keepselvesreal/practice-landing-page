# 1.5.2 Functional tests (pp.25-26)

---
**Page 25**

Getting Started with Software Testing
Chapter 1
[ 25 ]
Functional tests
Integration tests can be very diverse. As you start integrating more and more components,
you move toward a higher level of abstraction, and in the end, you move so far from the
underlying components that people feel the need to distinguish those kinds of tests as they
offer different benefits, complexities, and execution times.
That's why the naming of functional tests, end-to-end tests, system tests, acceptance tests,
and so on all takes place.
Overall, those are all forms of integration tests; what changes are their goal and purpose:
Functional tests tend to verify that we are exposing to our users the feature we
actually intended. They don't care about intermediate results or side-effects; they
just verify that the end result for the user is the one the specifications described,
thus they are always black-box tests.
End-to-End (E2E) tests are a specific kind of functional test that involves the
vertical integration of components. The most common E2E tests are where
technologies such as Selenium are involved in accessing a real application
instance through a web browser.
System tests are very similar to functional tests themselves, but instead of testing
a single feature, they usually test a whole journey of the user across the system.
So they usually simulate real usage patterns of the user to verify that the system
as a whole behaves as expected.
Acceptance tests are a kind of functional test that is meant to confirm that the
implementation of the feature does behave as expected. They usually express the
primary usage flow of the feature, leaving less common flows for other
integration tests, and are frequently provided by the specifications themselves to
help the developer confirm that they implemented what was expected.
But those are not the only kinds of integration that people refer to; new types are
continuously defined in the effort to distinguish the goals of tests and responsibilities.
Component tests, contract tests, and many others are kinds of tests whose goal is to verify
integration between different pieces of the software at different layers. Overall, you
shouldn't be ashamed of asking your colleagues what they mean exactly when they use
those names, because you will notice each one of them will value different properties of
those tests when classifying them into the different categories.
The general distinction to keep in mind when distinguishing between integration tests and
functional tests is that unit and integration tests aim to test the implementation, while
functional tests aim to test the behavior.


---
**Page 26**

Getting Started with Software Testing
Chapter 1
[ 26 ]
How you do that can easily involve the same exact technologies and it's just a matter of
different goals. Properly covering the behavior of your software with the right kind of tests
can be the difference between buggy software and reliable software. That's why there has
been a long debate about how to structure test suites, leading to the testing pyramid and
the testing trophy as the most widespread models of test distribution.
Understanding the testing pyramid and
trophy
Given the need to provide different kinds of tests – unit, integration, and E2E as each one of
them has different benefits and costs, the next immediate question is how do we get the
right balance?
Each kind of test comes with a benefit and a cost, so it's a matter of finding where we get
the best return on investment:
E2E tests verify the real experience of what the user faces. They are, in theory, the
most realistic kind of tests and can detect problems such as incompatibilities with
specific platforms (for example, browsers) and exercise our system as a whole.
But when something goes wrong, it is hard to spot where the problem lies. They
are very slow and tend to be flaky (failing for reasons unrelated to our software,
such as network conditions).
Integration tests usually provide a reasonable guarantee that the software is
doing what it is expected to do and are fairly robust to internal implementation
changes, requiring less frequent refactoring when the internals of the software
change. But they can still get very slow if your system involves writes to database
services, the rendering of page templates, routing HTTP requests, and generally
slow parts. And when something goes wrong, we might have to go through tens
of layers before being able to spot where the problem is.
Unit tests can be very fast (especially when talking of solitary units) and provide
very pinpointed information about where problems are. But they can't always 
guarantee that the software as a whole does what it's expected to do and can
make changing implementation details expensive because a change to internals
that don't impact the software behavior might require changing tens of unit tests.
Each of them has its own pros and cons, and the development community has long argued
how to get the right balance.
The two primary models that have emerged are the testing pyramid and the testing trophy,
named after their shapes.


