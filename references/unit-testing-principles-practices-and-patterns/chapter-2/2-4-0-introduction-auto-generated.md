# 2.4.0 Introduction [auto-generated] (pp.37-38)

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


---
**Page 38**

38
CHAPTER 2
What is a unit test?
 Similarly, an outreach to an out-of-process dependency makes the test slow. A call
to a database adds hundreds of milliseconds, potentially up to a second, of additional
execution time. Milliseconds might not seem like a big deal at first, but when your test
suite grows large enough, every second counts.
 In theory, you could write a slow test that works with in-memory objects only, but
it’s not that easy to do. Communication between objects inside the same memory
space is much less expensive than between separate processes. Even if the test works
with hundreds of in-memory objects, the communication with them will still execute
faster than a call to a database.
 Finally, a test is an integration test when it verifies two or more units of behavior.
This is often a result of trying to optimize the test suite’s execution speed. When you
have two slow tests that follow similar steps but verify different units of behavior, it
might make sense to merge them into one: one test checking two similar things runs
faster than two more-granular tests. But then again, the two original tests would have
been integration tests already (due to them being slow), so this characteristic usually
isn’t decisive.
 An integration test can also verify how two or more modules developed by separate
teams work together. This also falls into the third bucket of tests that verify multiple
units of behavior at once. But again, because such an integration normally requires an
out-of-process dependency, the test will fail to meet all three criteria, not just one.
 Integration testing plays a significant part in contributing to software quality by
verifying the system as a whole. I write about integration testing in detail in part 3.
2.4.1
End-to-end tests are a subset of integration tests
In short, an integration test is a test that verifies that your code works in integration with
shared dependencies, out-of-process dependencies, or code developed by other teams
in the organization. There’s also a separate notion of an end-to-end test. End-to-end
tests are a subset of integration tests. They, too, check to see how your code works with
out-of-process dependencies. The difference between an end-to-end test and an inte-
gration test is that end-to-end tests usually include more of such dependencies.
 The line is blurred at times, but in general, an integration test works with only one
or two out-of-process dependencies. On the other hand, an end-to-end test works with
all out-of-process dependencies, or with the vast majority of them. Hence the name
end-to-end, which means the test verifies the system from the end user’s point of view,
including all the external applications this system integrates with (see figure 2.6).
 People also use such terms as UI tests (UI stands for user interface), GUI tests (GUI is
graphical user interface), and functional tests. The terminology is ill-defined, but in gen-
eral, these terms are all synonyms.
 Let’s say your application works with three out-of-process dependencies: a data-
base, the file system, and a payment gateway. A typical integration test would include
only the database and file system in scope and use a test double to replace the pay-
ment gateway. That’s because you have full control over the database and file system,


