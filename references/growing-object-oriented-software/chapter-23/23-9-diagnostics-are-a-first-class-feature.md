# 23.9 Diagnostics Are a First-Class Feature (pp.271-273)

---
**Page 271**

Notice that jMock can accept a name when creating a mock object that will
be used in failure reporting. In fact, where there’s more than one mock object of
the same type, jMock insists that they are named to avoid confusion (the default
is to use the class name).
Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
use an empty interface to mark (and name) a domain concept and show how
it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
with methods to describe its behavior.
Explicitly Assert That Expectations Were Satisﬁed
A test that has both expectations and assertions can produce a confusing failure.
In jMock and other mock object frameworks, the expectations are checked after
the body of the test. If, for example, a collaboration doesn’t work properly and
returns a wrong value, an assertion might fail before any expectations are checked.
This would produce a failure report that shows, say, an incorrect calculation result
rather than the missing collaboration that actually caused it.
In a few cases, then, it’s worth calling the assertIsSatisfied() method on
the Mockery before any of the test assertions to get the right failure report:
context.assertIsSatisfied();
assertThat(result, equalTo(expectedResult));
This demonstrates why it is important to “Watch the Test Fail” (page 42). If
you expect the test to fail because an expectation is not satisﬁed but a postcondi-
tion assertion fails instead, you will see that you should add an explicit call to
assert that all expectations have been satisﬁed.
Diagnostics Are a First-Class Feature
Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
TDD cycle: fail, pass, refactor. We’re making good progress and we know what
the failures mean because we’ve just written the test. But nowadays, we try to
follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Chapter 5, because that’s how we know we’ve understood the feature—and
whoever has to change it in a month’s time will also understand it. Figure 23.1
shows again that we need to maintain the quality of the tests, as well as the
production code.
271
Diagnostics Are a First-Class Feature


---
**Page 272**

Figure 23.1
Improve the diagnostics as part of the TDD cycle
Chapter 23
Test Diagnostics
272


---
**Page 273**

Chapter 24
Test Flexibility
Living plants are flexible and tender;
the dead are brittle and dry.
[…]
The rigid and stiff will be broken.
The soft and yielding will overcome.
—Lao Tzu (c.604—531 B.C.)
Introduction
As the system and its associated test suite grows, maintaining the tests can become
a burden if they have not been written carefully. We’ve described how we can
reduce the ongoing cost of tests by making them easy to read and generating
helpful diagnostics on failure. We also want to make sure that each test fails
only when its relevant code is broken. Otherwise, we end up with brittle
tests that slow down development and inhibit refactoring. Common causes of test
brittleness include:
•
The tests are too tightly coupled to unrelated parts of the system or unrelated
behavior of the object(s) they’re testing;
•
The tests overspecify the expected behavior of the target code, constraining
it more than necessary; and,
•
There is duplication when multiple tests exercise the same production code
behavior.
Test brittleness is not just an attribute of how the tests are written; it’s also
related to the design of the system. If an object is difﬁcult to decouple from its
environment because it has many dependencies or its dependencies are hidden,
its tests will fail when distant parts of the system change. It will be hard to judge
the knock-on effects of altering the code. So, we can use test brittleness as a
valuable source of feedback about design quality.
There’s a virtuous relationship with test readability and resilience. A test that
is focused, has clean set-up, and has minimal duplication is easier to name and is
more obvious about its purpose. This chapter expands on some of the techniques
we discussed in Chapter 21. Actually, the whole chapter can be collapsed into a
single rule:
273


