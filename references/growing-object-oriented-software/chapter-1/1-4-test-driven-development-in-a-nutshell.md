# 1.4 Test-Driven Development in a Nutshell (pp.6-7)

---
**Page 6**

Test-Driven Development in a Nutshell
The cycle at the heart of TDD is: write a test; write some code to get it working;
refactor the code to be as simple an implementation of the tested features as
possible. Repeat.
Figure 1.1
The fundamental TDD cycle
As we develop the system, we use TDD to give us feedback on the quality of
both its implementation (“Does it work?”) and design (“Is it well structured?”).
Developing test-ﬁrst, we ﬁnd we beneﬁt twice from the effort. Writing tests:
•
makes us clarify the acceptance criteria for the next piece of work—we
have to ask ourselves how we can tell when we’re done (design);
•
encourages us to write loosely coupled components, so they can easily be
tested in isolation and, at higher levels, combined together (design);
•
adds an executable description of what the code does (design); and,
•
adds to a complete regression suite (implementation);
whereas running tests:
•
detects errors while the context is fresh in our mind (implementation); and,
•
lets us know when we’ve done enough, discouraging “gold plating” and
unnecessary features (design).
This feedback cycle can be summed up by the Golden Rule of TDD:
The Golden Rule of Test-Driven Development
Never write new functionality without a failing test.
Chapter 1
What Is the Point of Test-Driven Development?
6


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


