# 1.4.2 Integration testing (pp.20-21)

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


---
**Page 21**

21
The testing pyramid, and where we should focus
only responsibility is to interact with this external component (think of Data Access
Object [DAO] classes). These DAOs may contain complicated SQL code. Thus, a tes-
ter feels the need to test the SQL queries. The tester does not want to test the entire
system, only the integration between the DAO class and the database. The tester also
does not want to test the DAO class in complete isolation. After all, the best way to
know whether a SQL query works is to submit it to the database and see what the
database returns.
 This is an example of an integration test. Integration testing aims to test multiple
components of a system together, focusing on the interactions between them instead
of testing the system as a whole (see figure 1.6). Are they communicating correctly?
What happens if component A sends message X to component B? Do they still present
correct behavior?
Integration testing focuses on two parts: our component and the external component.
Writing such a test is less complicated than writing a test that goes through the entire
system and includes components we do not care about.
 Compared to unit testing, integration tests are more difficult to write. In the exam-
ple, setting up a database for the test requires effort. Tests that involve databases gen-
erally need to use an isolated instance of the database just for testing purposes, update
the database schema, put the database into a state expected by the test by adding or
removing rows, and clean everything afterward. The same effort is involved in other
types of integration tests: web services, file reads and writes, and so on. We will discuss
writing integration tests effectively in chapter 9. 
1.4.3
System testing
To get a more realistic view of the software and thus perform more realistic tests, we
should run the entire software system with all its databases, frontend apps, and other
components. When we test the system in its entirety, instead of testing small parts of
the system in isolation, we are doing system testing (see figure 1.7). We do not care
how the system works from the inside; we do not care if it was developed in Java or
Class
A
Class
B
Class
C
Depends
DB
C
sume
on
s
Integration testing exercises the
integration between a component
of your system and some external
component (e.g., a database).
CTest
Figure 1.6
Integration testing. Our goal is 
to test whether our component integrates 
well with an external component.


