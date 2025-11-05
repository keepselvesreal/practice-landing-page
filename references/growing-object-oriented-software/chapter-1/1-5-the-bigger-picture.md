# 1.5 The Bigger Picture (pp.7-8)

---
**Page 7**

Refactoring.Think Local, Act Local
Refactoring means changing the internal structure of an existing body of code
without changing its behavior.The point is to improve the code so that it’s a better
representation of the features it implements, making it more maintainable.
Refactoring is a disciplined technique where the programmer applies a series of
transformations (or “refactorings”) that do not change the code’s behavior. Each
refactoring is small enough to be easy to understand and “safe”; for example, a
programmer might pull a block of code into a helper method to make the original
method shorter and easier to understand. The programmer makes sure that the
system is still working after each refactoring step, minimizing the risk of getting
stranded by a change; in test-driven code, we can do that by running the tests.
Refactoring is a “microtechnique” that is driven by ﬁnding small-scale im-
provements. Our experience is that, applied rigorously and consistently, its many
small steps can lead to signiﬁcant structural improvements. Refactoring is not the
same activity as redesign, where the programmers take a conscious decision to
change a large-scale structure. That said, having taken a redesign decision, a
team can use refactoring techniques to get to the new design incrementally
and safely.
You’ll see quite a lot of refactoring in our example in Part III. The standard text on
the concept is Fowler’s [Fowler99].
The Bigger Picture
It is tempting to start the TDD process by writing unit tests for classes in the
application. This is better than having no tests at all and can catch those basic
programming errors that we all know but ﬁnd so hard to avoid: fencepost errors,
incorrect boolean expressions, and the like. But a project with only unit tests is
missing out on critical beneﬁts of the TDD process. We’ve seen projects with
high-quality, well unit-tested code that turned out not to be called from anywhere,
or that could not be integrated with the rest of the system and had to be rewritten.
How do we know where to start writing code? More importantly, how do we
know when to stop writing code? The golden rule tells us what we need to do:
Write a failing test.
When we’re implementing a feature, we start by writing an acceptance test,
which exercises the functionality we want to build. While it’s failing, an acceptance
test demonstrates that the system does not yet implement that feature; when it
passes, we’re done. When working on a feature, we use its acceptance test to
guide us as to whether we actually need the code we’re about to write—we only
write code that’s directly relevant. Underneath the acceptance test, we follow the
unit level test/implement/refactor cycle to develop the feature; the whole cycle
looks like Figure 1.2.
7
The Bigger Picture


---
**Page 8**

Figure 1.2
Inner and outer feedback loops in TDD
The outer test loop is a measure of demonstrable progress, and the growing
suite of tests protects us against regression failures when we change the system.
Acceptance tests often take a while to make pass, certainly more than one check-in
episode, so we usually distinguish between acceptance tests we’re working on
(which are not yet included in the build) and acceptance tests for the features
that have been ﬁnished (which are included in the build and must always pass).
The inner loop supports the developers. The unit tests help us maintain the
quality of the code and should pass soon after they’ve been written. Failing unit
tests should never be committed to the source repository.
Testing End-to-End
Wherever possible, an acceptance test should exercise the system end-to-end
without directly calling its internal code. An end-to-end test interacts with the
system only from the outside: through its user interface, by sending messages as
if from third-party systems, by invoking its web services, by parsing reports, and
so on. As we discuss in Chapter 10, the whole behavior of the system includes
its interaction with its external environment. This is often the riskiest and most
difﬁcult aspect; we ignore it at our peril. We try to avoid acceptance tests that
just exercise the internal objects of the system, unless we really need the speed-up
and already have a stable set of end-to-end tests to provide cover.
The Importance of End-to-End Testing: A Horror Story
Nat was once brought onto a project that had been using TDD since its inception.
The team had been writing acceptance tests to capture requirements and show
progress to their customer representatives. They had been writing unit tests for
the classes of the system, and the internals were clean and easy to change.They
had been making great progress, and the customer representatives had signed
off all the implemented features on the basis of the passing acceptance tests.
Chapter 1
What Is the Point of Test-Driven Development?
8


