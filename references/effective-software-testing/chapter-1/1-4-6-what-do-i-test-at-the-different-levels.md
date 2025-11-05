# 1.4.6 What do I test at the different levels? (pp.24-25)

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


---
**Page 25**

25
The testing pyramid, and where we should focus
under test? In other words, what parts of the system would be significantly affected by
a bug? These are the areas where I do some system testing.
 Remember the pesticide paradox: a single technique usually is not enough to iden-
tify all the bugs. Let me give you a real-world example from one of my previous proj-
ects. In developing an e-learning platform, one of our most important functionalities
was payment. The worst type of bug would prevent users from buying our product.
Therefore, we were rigorous in testing all the code related to payment. We used unit
tests for business rules related to what the user bought being converted into the right
product, access and permissions, and so on. Integration with the two payment gate-
ways we supported was tested via integration testing: the integration tests made real
HTTP calls to a sandbox web service provided by the payment gateways, and we tested
different types of users buying products with various credit cards. Finally, our system
tests represented the entire user journey in buying our product. These tests started a
Firefox browser, clicked HTML elements, submitted forms, and checked that the right
product was available after confirming payment.
 Figure 1.8 also includes manual testing. I’ve said that every test should be auto-
mated, but I see some value in manual testing when these tests focus on exploration
and validation. As a developer, it is nice to use and explore the software system you are
building from time to time, both for real and via a test script. Open the browser or the
app, and play with it—you may gain better insight into what else to test. 
1.4.7
What if you disagree with the testing pyramid?
Many people disagree about the idea of a testing pyramid and whether we should
favor unit testing. These developers argue for the testing trophy: a thinner bottom level
with unit tests, a bigger middle slice with integration tests, and a thinner top with sys-
tem tests. Clearly, these developers see the most value in writing integration tests.
 While I disagree, I see their point. In many software systems, most of the complex-
ity is in integrating components. Think of a highly distributed microservices architec-
ture: in such a scenario, the developer may feel more comfortable if the automated
tests make actual calls to other microservices instead of relying on stubs or mocks that
simulate them. Why write unit tests for something you have to test anyway via integra-
tion tests?
 In this particular case, as someone who favors unit testing, I would prefer to tackle
the microservices testing problem by first writing lots and lots of unit tests in each micro-
service to ensure that they all behaved correctly, investing heavily in contract design to
ensure that the microservices had clear pre- and post-conditions. Then, I would use
many integration tests to ensure that communication worked as expected and that the
normal variations in the distributed system did not break the system—yes, lots of them,
because their benefits would outweigh their costs in this scenario. I might even invest in
some smart (maybe AI-driven) tests to explore corner cases I could not see.
 Another common case I see in favor of integration testing rather than unit test-
ing involves database-centric information systems: that is, systems where the main


