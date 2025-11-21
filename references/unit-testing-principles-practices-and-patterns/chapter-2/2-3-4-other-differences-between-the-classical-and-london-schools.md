# 2.3.4 Other differences between the classical and London schools (pp.36-37)

---
**Page 36**

36
CHAPTER 2
What is a unit test?
2.3.3
Revealing the precise bug location
If you introduce a bug to a system with London-style tests, it normally causes only tests
whose SUT contains the bug to fail. However, with the classical approach, tests that
target the clients of the malfunctioning class can also fail. This leads to a ripple effect
where a single bug can cause test failures across the whole system. As a result, it
becomes harder to find the root of the issue. You might need to spend some time
debugging the tests to figure it out.
 It’s a valid concern, but I don’t see it as a big problem. If you run your tests regu-
larly (ideally, after each source code change), then you know what caused the bug—
it’s what you edited last, so it’s not that difficult to find the issue. Also, you don’t have
to look at all the failing tests. Fixing one automatically fixes all the others.
 Furthermore, there’s some value in failures cascading all over the test suite. If a
bug leads to a fault in not only one test but a whole lot of them, it shows that the piece
of code you have just broken is of great value—the entire system depends on it. That’s
useful information to keep in mind when working with the code. 
2.3.4
Other differences between the classical and London schools
Two remaining differences between the classical and London schools are
Their approach to system design with test-driven development (TDD)
The issue of over-specification
The London style of unit testing leads to outside-in TDD, where you start from the
higher-level tests that set expectations for the whole system. By using mocks, you spec-
ify which collaborators the system should communicate with to achieve the expected
result. You then work your way through the graph of classes until you implement every
one of them. Mocks make this design process possible because you can focus on one
Test-driven development
Test-driven development is a software development process that relies on tests to
drive the project development. The process consists of three (some authors specify
four) stages, which you repeat for every test case:
1
Write a failing test to indicate which functionality needs to be added and how
it should behave.
2
Write just enough code to make the test pass. At this stage, the code doesn’t
have to be elegant or clean.
3
Refactor the code. Under the protection of the passing test, you can safely
clean up the code to make it more readable and maintainable.
Good sources on this topic are the two books I recommended earlier: Kent Beck’s
Test-Driven Development: By Example, and Growing Object-Oriented Software, Guided
by Tests by Steve Freeman and Nat Pryce.


---
**Page 37**

37
Integration tests in the two schools
class at a time. You can cut off all of the SUT’s collaborators when testing it and thus
postpone implementing those collaborators to a later time.
 The classical school doesn’t provide quite the same guidance since you have to
deal with the real objects in tests. Instead, you normally use the inside-out approach.
In this style, you start from the domain model and then put additional layers on top of
it until the software becomes usable by the end user.
 But the most crucial distinction between the schools is the issue of over-specification:
that is, coupling the tests to the SUT’s implementation details. The London style
tends to produce tests that couple to the implementation more often than the classi-
cal style. And this is the main objection against the ubiquitous use of mocks and the
London style in general.
 There’s much more to the topic of mocking. Starting with chapter 4, I gradually
cover everything related to it. 
2.4
Integration tests in the two schools
The London and classical schools also diverge in their definition of an integration
test. This disagreement flows naturally from the difference in their views on the isola-
tion issue.
 The London school considers any test that uses a real collaborator object an inte-
gration test. Most of the tests written in the classical style would be deemed integra-
tion tests by the London school proponents. For an example, see listing 1.4, in which I
first introduced the two tests covering the customer purchase functionality. That code
is a typical unit test from the classical perspective, but it’s an integration test for a fol-
lower of the London school.
 In this book, I use the classical definitions of both unit and integration testing.
Again, a unit test is an automated test that has the following characteristics:
It verifies a small piece of code,
Does it quickly,
And does it in an isolated manner.
Now that I’ve clarified what the first and third attributes mean, I’ll redefine them
from the point of view of the classical school. A unit test is a test that
Verifies a single unit of behavior,
Does it quickly,
And does it in isolation from other tests.
An integration test, then, is a test that doesn’t meet one of these criteria. For example,
a test that reaches out to a shared dependency—say, a database—can’t run in isolation
from other tests. A change in the database’s state introduced by one test would alter
the outcome of all other tests that rely on the same database if run in parallel. You’d
have to take additional steps to avoid this interference. In particular, you would have
to run such tests sequentially, so that each test would wait its turn to work with the
shared dependency.


