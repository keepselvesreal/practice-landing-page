# 2.5 Summary (pp.39-41)

---
**Page 39**

39
Summary
and thus can easily bring them to the required state in tests, whereas you don’t have
the same degree of control over the payment gateway. With the payment gateway, you
may need to contact the payment processor organization to set up a special test
account. You might also need to check that account from time to time to manually
clean up all the payment charges left over from the past test executions.
 Since end-to-end tests are the most expensive in terms of maintenance, it’s better
to run them late in the build process, after all the unit and integration tests have
passed. You may possibly even run them only on the build server, not on individual
developers’ machines.
 Keep in mind that even with end-to-end tests, you might not be able to tackle all of
the out-of-process dependencies. There may be no test version of some dependencies,
or it may be impossible to bring those dependencies to the required state automati-
cally. So you may still need to use a test double, reinforcing the fact that there isn’t a
distinct line between integration and end-to-end tests. 
Summary
Throughout this chapter, I’ve refined the definition of a unit test:
– A unit test verifies a single unit of behavior,
– Does it quickly,
– And does it in isolation from other tests.
Another class
Unit test
Payment gateway
End-to-end test
Database
System under test
Integration test
Figure 2.6
End-to-end tests normally include all or almost all out-of-process dependencies 
in the scope. Integration tests check only one or two such dependencies—those that are 
easier to set up automatically, such as the database or the file system.


---
**Page 40**

40
CHAPTER 2
What is a unit test?
The isolation issue is disputed the most. The dispute led to the formation of two
schools of unit testing: the classical (Detroit) school, and the London (mockist)
school. This difference of opinion affects the view of what constitutes a unit and
the treatment of the system under test’s (SUT’s) dependencies.
– The London school states that the units under test should be isolated from
each other. A unit under test is a unit of code, usually a class. All of its depen-
dencies, except immutable dependencies, should be replaced with test dou-
bles in tests.
– The classical school states that the unit tests need to be isolated from each
other, not units. Also, a unit under test is a unit of behavior, not a unit of code.
Thus, only shared dependencies should be replaced with test doubles.
Shared dependencies are dependencies that provide means for tests to affect
each other’s execution flow.
The London school provides the benefits of better granularity, the ease of test-
ing large graphs of interconnected classes, and the ease of finding which func-
tionality contains a bug after a test failure.
The benefits of the London school look appealing at first. However, they intro-
duce several issues. First, the focus on classes under test is misplaced: tests
should verify units of behavior, not units of code. Furthermore, the inability to
unit test a piece of code is a strong sign of a problem with the code design. The
use of test doubles doesn’t fix this problem, but rather only hides it. And finally,
while the ease of determining which functionality contains a bug after a test fail-
ure is helpful, it’s not that big a deal because you often know what caused the
bug anyway—it’s what you edited last.
The biggest issue with the London school of unit testing is the problem of over-
specification—coupling tests to the SUT’s implementation details.
An integration test is a test that doesn’t meet at least one of the criteria for a
unit test. End-to-end tests are a subset of integration tests; they verify the system
from the end user’s point of view. End-to-end tests reach out directly to all or
almost all out-of-process dependencies your application works with.
For a canonical book about the classical style, I recommend Kent Beck’s Test-
Driven Development: By Example. For more on the London style, see Growing Object-
Oriented Software, Guided by Tests, by Steve Freeman and Nat Pryce. For further
reading about working with dependencies, I recommend Dependency Injection:
Principles, Practices, Patterns by Steven van Deursen and Mark Seemann.


---
**Page 41**

41
The anatomy of
a unit test
In this remaining chapter of part 1, I’ll give you a refresher on some basic topics.
I’ll go over the structure of a typical unit test, which is usually represented by the
arrange, act, and assert (AAA) pattern. I’ll also show the unit testing framework of
my choice—xUnit—and explain why I’m using it and not one of its competitors.
 Along the way, we’ll talk about naming unit tests. There are quite a few compet-
ing pieces of advice on this topic, and unfortunately, most of them don’t do a good
enough job improving your unit tests. In this chapter, I describe those less-useful
naming practices and show why they usually aren’t the best choice. Instead of those
practices, I give you an alternative—a simple, easy-to-follow guideline for naming
tests in a way that makes them readable not only to the programmer who wrote
them, but also to any other person familiar with the problem domain.
 Finally, I’ll talk about some features of the framework that help streamline the
process of unit testing. Don’t worry about this information being too specific to C#
This chapter covers
The structure of a unit test
Unit test naming best practices
Working with parameterized tests
Working with fluent assertions


