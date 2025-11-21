# 1.4.3 System testing (pp.21-23)

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


---
**Page 22**

22
CHAPTER 1
Effective and systematic software testing
Ruby, or whether it uses a relational database. We only care that, given input X, the
system will provide output Y.
The obvious advantage of system testing is how realistic the tests are. Our final customers
will not run the identifyExtremes() method in isolation. Rather, they will visit a web
page, submit a form, and see the results. System tests exercise the system in that pre-
cise manner. The more realistic the tests are (that is, when the tests perform actions
similar to the final user), the more confident we can be about the whole system.
 System testing does, however, have its downsides:
System tests are often slow compared to unit tests. Imagine everything a system
test has to do, including starting and running the entire system with all its com-
ponents. The test also has to interact with the real application, and actions may
take a few seconds. Imagine a test that starts a container with a web application
and another container with a database. It then submits an HTTP request to a
web service exposed by this web app. This web service retrieves data from the
database and writes a JSON response to the test. This obviously takes more time
than running a simple unit test, which has virtually no dependencies.
System tests are also harder to write. Some of the components (such as data-
bases) may require a complex setup before they can be used in a testing sce-
nario. Think of connecting, authenticating, and making sure the database has
all the data required by that test case. Additional code is required just to auto-
mate the tests.
System tests are more prone to flakiness. A flaky test presents erratic behavior: if
you run it, it may pass or fail for the same configuration. Flaky tests are an
important problem for software development teams, and we discuss this issue in
chapter 10. Imagine a system test that exercises a web app. After the tester clicks
a button, the HTTP POST request to the web app takes half a second longer
Class
Class
Class
Depends
System
test
DB
C
mes
onsu
When system testing, you
want to exercise the entire
system together, including
all of its classes, dependencies,
database , web services, and
s
whatever other components it
may have.
Controller
Web
ser
e
vic
The entire software system
Request
Response
Figure 1.7
System testing. Our goal is to test the entire system and its components.


---
**Page 23**

23
The testing pyramid, and where we should focus
than usual (due to small variations we often do not control in real-life scenar-
ios). The test does not expect this and thus fails. The test is executed again, the
web app takes the usual time to respond, and the test passes. Many uncertain-
ties in a system test can lead to unexpected behavior. 
1.4.4
When to use each test level
With a clear understanding of the different test levels and their benefits, we have to
decide whether to invest more in unit testing or system testing and determine which
components should be tested via unit testing and which components should be tested
via system testing. A wrong decision may have a considerable impact on the system’s
quality: a wrong level may cost too many resources and may not find sufficient bugs.
As you may have guessed, the best answer here is, “It depends.”
 Some developers—including me—favor unit testing over other test levels. This
does not mean such developers do not do integration or system testing; but whenever
possible, they push testing toward the unit test level. A pyramid is often used to illus-
trate this idea, as shown in figure 1.8. The size of the slice in the pyramid represents
the relative number of tests to carry out at each test level.
Unit testing is at the bottom of the pyramid and has the largest area. This means
developers who follow this scheme favor unit testing (that is, write more unit tests).
Climbing up in the diagram, the next level is integration testing. The area is smaller,
indicating that, in practice, these developers write fewer integration tests than unit
tests. Given the extra effort that integration tests require, the developers write tests
only for the integrations they need. The diagram shows that these developers favor
system tests less than integration tests and have even fewer manual tests. 
1.4.5
Why do I favor unit tests?
As I said, I tend to favor unit testing. I appreciate the advantages that unit tests give
me. They are easy to write, they are fast, I can write them intertwined with production
code, and so on. I also believe that unit testing fits very well with the way software
Unit tests
Integration tests
System tests
Manual
More real
More complex
All business rules
should be tested here.
Exploratory tests
Complex integrations
with external services
Tests the main/risky
ﬂow of the app
Figure 1.8
My version of the testing pyramid. The closer a test is to the 
top, the more real and complex the test becomes. At the right part you see 
what I test at each test level.


