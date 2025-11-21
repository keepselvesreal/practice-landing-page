# 6.0 Introduction [auto-generated] (pp.141-143)

---
**Page 141**

141
Test doubles and mocks
Until now, we have been testing classes and methods that were isolated from each
other. We passed the inputs to a single method call and asserted its output. Or,
when a class was involved, we set up the state of the class, called the method under
test, and asserted that the class was in the expected state.
 But some classes depend on other classes to do their job. Exercising (or testing)
many classes together may be desirable. We often break down complex behavior into
multiple classes to improve maintainability, each with a small part of the business
logic. We still want to ensure, however, that the whole thing works together; we will
discuss this in chapter 9. This chapter focuses on testing that unit in an isolated fash-
ion without caring too much about its dependencies. But why would we want that?
 The answer is simple: because exercising the class under test together with its
concrete dependencies might be too slow, too hard, or too much work. As an exam-
ple, consider an application that handles invoices. This system has a class called
This chapter covers
Using stubs, fakes, and mocks to simplify testing
Understanding what to mock, when to mock, and 
when not to mock
How to mock the unmockable


---
**Page 142**

142
CHAPTER 6
Test doubles and mocks
IssuedInvoices, which handles the database and contains lots of SQL queries. Other
parts of the system (such as the InvoiceGenerationService class, which generates
new invoices) depend on this IssuedInvoices class to persist the generated invoice in
the database. This means that whenever we test InvoiceGenerationService, this class
will consequently call IssuedInvoices, which will then communicate with a database.
 In other words, the InvoiceGenerationService class indirectly depends on the
database that stores the issued invoices. This means testing the InvoiceGeneration-
Service requires setting up a database, making sure it contains all the right data, and
so on. That is clearly much more work than writing tests that do not require a data-
base. Figure 6.1 shows a more generic illustration of this problem. How do we test a
class that depends on many other classes, some of which may involve databases and
other complicated things?
But when systematically testing the InvoiceGenerationService class, maybe we do
not want to test whether the SQL query in the IssuedInvoices class is correct. We
only want to ensure that, for example, the invoice is generated correctly or contains
all the right values. Testing whether the SQL query works will be the responsibility of
the IssuedInvoicesTest test suite, not InvoiceGenerationServiceTest. We will
write integration tests for SQL queries in chapter 9.
 We must figure out how to test a class that depends on another class without using
that dependency. This is where test doubles come in handy. We create an object to
mimic the behavior of component B (“it looks like B, but it is not B”). Within the test,
we have full control over what this fake component B does, so we can make it behave
as B would in the context of this test and thus cut the dependency on the real object.
 In the previous example, suppose A is a plain Java class that depends on Issued-
Invoices to retrieve values from a database. We can implement a fake IssuedInvoices
that returns a hard-coded list of values rather than retrieving them from an external
database. This means we can control the environment around A so we can check how
A behaves without dealing with complex dependencies. I show examples of how this
works later in the chapter.
etc.
B
DB
A
C
How do we write tests for A without
depending on B, C, and all their
transitive dependencies?
Figure 6.1
A simple illustration of the 
challenges we face when testing a class 
that depends on many other classes


---
**Page 143**

143
Dummies, fakes, stubs, spies, and mocks
 Using objects that simulate the behavior of other objects has the following
advantages:
We have more control. We can easily tell these fake objects what to do. If we want a
method to throw an exception, we tell the mock method to throw it. There is
no need for complicated setups to force the dependency to throw the excep-
tion. Think of how hard it is to force a class to throw an exception or return a
fake date. This effort is close to zero when we simulate the dependencies with
mock objects.
Simulations are faster. Imagine a dependency that communicates with a web ser-
vice or a database. A method in one of these classes might take a few seconds to
process. On the other hand, if we simulate the dependency, it will no longer
need to communicate with a database or web service and wait for a response.
The simulation will return what it was configured to return, and it will cost
nothing in terms of time.
When used as a design technique, mocks enable developers to reflect on how
classes should interact with each other, what their contracts should be, and the con-
ceptual boundaries. Therefore, mocks can be used to make testing easier and
support developers in designing code.
NOTE
While some of the schools of thought in testing prefer to see mocks as
a design technique, in this book, I talk about stubs and mocks mostly from a
testing perspective, as our goal is to use mocks to ease our lives when looking
for bugs. If you are interested in mocking as a design technique, I strongly
recommend Freeman and Pryce’s 2009 book, which is the canonical refer-
ence for the subject.
I sorted mocks into the unit testing section of my testing flow (go back to figure 1.4 in
chapter 1) because our goal is to focus on a single unit without caring much about the
other units of the system. Note, however, that we still care about the contracts of the
dependencies, as our simulations must follow and do the same things that the simu-
lated class promises.
6.1
Dummies, fakes, stubs, spies, and mocks
Before we dive into how to simulate objects, let’s first discuss the different types of sim-
ulations we can create. Meszaros, in his book (2007), defines five different types:
dummy objects, fake objects, stubs, spies, and mocks. Each makes sense in a specific
situation.
6.1.1
Dummy objects
Dummy objects are passed to the class under test but never used. This is common in
business applications where you need to fill a long list of parameters, but the test exer-
cises only a few of them. Think of a unit test for a Customer class. Maybe this class
depends on several other classes like Address, Email, and so on. Maybe a specific test


