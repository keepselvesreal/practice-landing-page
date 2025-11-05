# 1.4.1 Unit testing (pp.19-20)

---
**Page 19**

19
The testing pyramid, and where we should focus
 Verification and validation can walk hand in hand. In this chapter’s example about
the planning poker algorithm, this was what happened when Eleanor imagined all the
developers estimating the same effort. The product owner did not think of this case. A
systematic testing approach can help you identify corner cases that even the product
experts did not envision. 
1.4
The testing pyramid, and where we should focus
Whenever we talk about pragmatic testing, one of the first decisions we need to make
is the level at which to test the code. By a test level, I mean the unit, integration, or system
level. Let’s quickly look at each of them.
1.4.1
Unit testing
In some situations, the tester’s goal is to test a single feature of the software, purpose-
fully ignoring the other units of the system. This is basically what we saw in the plan-
ning poker example. The goal was to test the identifyExtremes() method and
nothing else. Of course, we cared about how this method would interact with the rest
of the system, and that is why we tested its contracts. However, we did not test it
together with the other pieces of the system.
 When we test units in isolation, we are doing unit testing. This test level offers the
following advantages:
Unit tests are fast. A unit test usually takes just a couple of milliseconds to exe-
cute. Fast tests allow us to test huge portions of the system in a small amount of
time. Fast, automated test suites give us constant feedback. This fast safety net
makes us feel more comfortable and confident in performing evolutionary
changes to the software system we are working on.
Unit tests are easy to control. A unit test tests the software by giving certain parame-
ters to a method and then comparing the return value of this method to the
expected result. These input values and the expected result value are easy to
adapt or modify in the test. Again, look at the identifyExtremes() example
and how easy it was to provide different inputs and assert its output.
Unit tests are easy to write. They do not require a complicated setup or additional
work. A single unit is also often cohesive and small, making the tester’s job eas-
ier. Tests become much more complicated when we have databases, frontends,
and web services all together.
As for disadvantages, the following should be considered:
Unit tests lack reality. A software system is rarely composed of a single class. The
large number of classes in a system and their interaction can cause the system to
behave differently in its real application than in the unit tests. Therefore, unit
tests do not perfectly represent the real execution of a software system.
Some types of bugs are not caught. Some types of bugs cannot be caught at the unit
test level; they only happen in the integration of the different components


---
**Page 20**

20
CHAPTER 1
Effective and systematic software testing
(which are not exercised in a pure unit test). Think of a web application that
has a complex UI: you may have tested the backend and the frontend thor-
oughly, but a bug may only reveal itself when the backend and frontend are put
together. Or imagine multithreaded code: everything may work at the unit
level, but bugs may appear once threads are running together.
Interestingly, one of the hardest challenges in unit testing is to define what constitutes
a unit. A unit can be one method or multiple classes. Here is a definition for unit test-
ing that I like, given by Roy Osherove (2009): “A unit test is an automated piece of
code that invokes a unit of work in the system. And a unit of work can span a single
method, a whole class or multiple classes working together to achieve one single logi-
cal purpose that can be verified.”
 For me, unit testing means testing a (small) set of classes that have no dependency
on external systems (such as databases or web services) or anything else I do not fully
control. When I unit-test a set of classes together, the number of classes tends to be
small. This is primarily because testing many classes together may be too difficult, not
because this isn’t a unit test.
 But what if a class I want to test depends on another class that talks to, for example,
a database (figure 1.5)? This is where unit testing becomes more complicated. Here is
a short answer: if I want to test a class, and this class depends on another class that
depends on a database, I will simulate the database class. In other words, I will create a
stub that acts like the original class but is much simpler and easier to use during test-
ing. We will dive into this specific problem in chapter 6, where we discuss mocks. 
1.4.2
Integration testing
Unit tests focus on the smallest parts of the system. However, testing components in
isolation sometimes is not enough. This is especially true when the code under test
goes beyond the system’s borders and uses other (often external) components. Inte-
gration testing is the test level we use to test the integration between our code and
external parties.
 Let’s consider a real-world example. Software systems commonly rely on database
systems. To communicate with the database, developers often create a class whose
Class
A
Class
B
Class
C
Depends
ATest
DB
C
sume
on
s
When unit testing class A, our focus is on testing A,
as isolated as possible from the rest! If A depends
on other classes, we have to decide whether to
simulate them or to make our unit test a bit bigger.
Unit test
Figure 1.5
Unit testing. Our goal is 
to test one unit of the system that is 
as isolated as possible from the rest 
of the system.


