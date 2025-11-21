# 6.5 Summary (pp.170-172)

---
**Page 170**

170
CHAPTER 6
Test doubles and mocks
C It is possible to write completely isolated unit tests by, for example, using
mocks.
D The IssuedInvoices type (a direct dependency of InvoiceFilter)
should be tested using integration tests.
6.3
You are testing a system that triggers advanced events based on complex combi-
nations of external, boolean conditions relating to the weather (outside tem-
perature, amount of rain, wind, and so on). The system has been designed
cleanly and consists of a set of cooperating classes, each of which has a single
responsibility. You use specification-based testing for this logic and test it using
mocks.
Which of the following is a valid test strategy?
A You use mocks to support observing the external conditions.
B You create mock objects to represent each variant you need to test.
C You use mocks to control the external conditions and to observe the event
being triggered.
D You use mocks to control the triggered events.
6.4
Class A depends on a static method in class B. If you want to test class A, which of
the following two actions should you apply to do so properly?
Approach 1: Mock class B to control the behavior of the methods in class B.
Approach 2: Refactor class A, so the outcome of the method of class B is now
used as a parameter.
A Only approach 1
B Neither
C Only approach 2
D Both
6.5
According to the guidelines provided in the book, what types of classes should
you mock, and which should you not mock?
6.6
Now that you know the advantages and disadvantages of test doubles, what are
your thoughts about them? Do you plan to use mocks and stubs, or do you pre-
fer to focus on integration tests?
Summary
Test doubles help us test classes that depend on slow, complex, or external com-
ponents that are hard to control and observe.
There are different types of test doubles. Stubs are doubles that return hard-
coded values whenever methods are called. Mocks are like stubs, but we can
define how we expect a mock to interact with other classes.
Mocking can help us in testing, but it also has disadvantages. The mock may dif-
fer from the real implementation, and that would cause our tests to pass while
the system would fail.


---
**Page 171**

171
Summary
Tests that use mocks are more coupled with the production code than tests
that do not use mocks. When not carefully planned, such coupling can be
problematic.
Production classes should allow for the mock to be injected. One common
approach is to require all dependencies via the constructor.
You do not have to (and should not) mock everything, even when you decide to
go for mocks. Only mock what is necessary.


---
**Page 172**

172
Designing for testability
I usually say that every software system can be tested. However, some systems are more
testable than others. Imagine that for a single test case, we need to set up three differ-
ent web services, create five different files in different folders, and put the database
in a specific state. After all that, we exercise the feature under test and, to assert the
correct behavior, again need to see if the three web services were invoked, the five
files were consumed correctly, and the database is now in a different state. All those
steps are doable. But couldn’t this process be simpler?
 Software systems are sometimes not ready for or designed to be tested. In this
chapter, we discuss some of the main ideas behind systems that have high testability.
Testability is how easy it is to write automated tests for the system, class, or method
under test. In chapter 6, we saw that by allowing dependencies to be injected, we
This chapter covers
Designing testable code at the architectural, 
design, and implementation levels
Understanding the Hexagonal Architecture, 
dependency injection, observability, and 
controllability
Avoiding testability pitfalls


