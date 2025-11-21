# 1.4.5 Why do I favor unit tests? (pp.23-24)

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


---
**Page 24**

24
CHAPTER 1
Effective and systematic software testing
developers work. When developers implement a new feature, they write separate units
that will eventually work together to deliver larger functionality. While developing
each unit, it is easy to ensure that it works as expected. Testing small units rigorously
and effectively is much easier than testing a larger piece of functionality.
 Because I am also aware of the disadvantages of unit testing, I think carefully about
how the unit under development will be used by the other units of the system. Enforc-
ing clear contracts and systematically testing them gives me more certainty that things
will work out when they are put together.
 Finally, given the intensity with which I test my code using (simple and cheap)
unit tests, I can use integration and system tests for the parts that really matter. I do
not have to retest all the functionalities again at these levels. I use integration or sys-
tem testing to test specific parts of the code that I believe may cause problems
during integration.
1.4.6
What do I test at the different levels?
I use unit tests for units that are concerned with an algorithm or a single piece of busi-
ness logic of the software system. Most enterprise/business systems are used to trans-
form data. Such business logic is often expressed by using entity classes (for example,
an Invoice class and an Order class) to exchange messages. Business logic often does
not depend on external services, so it can easily be tested and fully controlled through
unit tests. Unit tests give us full control over the input data as well as full observability
in terms of asserting that the behavior is as expected.
NOTE
If a piece of code deals with specific business logic but cannot be
tested via unit tests (for example, the business logic can only be tested with
the full system running), previous design or architectural decisions are proba-
bly preventing you from writing unit tests. How you design your classes has a
significant impact on how easy it is to write unit tests for your code. We discuss
design for testability in chapter 7.
I use integration tests whenever the component under test interacts with an external
component (such as a database or web service). A DAO, whose sole responsibility is to
communicate with a database, is better tested at the integration level: you want to
ensure that communication with the database works, the SQL query returns what you
want it to, and transactions are committed to the database. Again, note that integration
tests are more expensive and harder to set up than unit tests, and I use them only
because they are the only way to test a particular part of the system. Chapter 7 discusses
how having a clear separation between business rules and infrastructure code will help
you test business rules with unit tests and integration code with integration tests.
 As we know already, system tests are very costly (they are difficult to write and slow
to run) and, thus, at the top of the pyramid. It is impossible to retest the entire system
at the system level. Therefore, I have to prioritize what to test at this level, and I per-
form a simple risk analysis to decide. What are the critical parts of the software system


