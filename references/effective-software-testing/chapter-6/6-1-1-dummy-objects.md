# 6.1.1 Dummy objects (pp.143-144)

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


---
**Page 144**

144
CHAPTER 6
Test doubles and mocks
case A wants to exercise a behavior, and this behavior does not care which Address
this Customer has. In this case, a tester can set up a dummy Address object and pass it
to the Customer class. 
6.1.2
Fake objects
Fake objects have real working implementations of the class they simulate. However, they
usually do the same task in a much simpler way. Imagine a fake database class that uses an
array list instead of a real database. This fake object is simpler to control than the real
database. A common example in real life is to use a simpler database during testing.
 In the Java world, developers like to use HSQLDB (HyperSQL database, http://
hsqldb.org), an in-memory database that is much faster and easier to set up in the test
code than a real database. We will talk more about in-memory databases when we dis-
cuss integration testing in chapter 9. 
6.1.3
Stubs
Stubs provide hard-coded answers to the calls performed during the test. Unlike fake
objects, stubs do not have a working implementation. If the code calls a stubbed
method getAllInvoices, the stub will return a hard-coded list of invoices.
 Stubs are the most popular type of simulation. In most cases, all you need from a
dependency is for it to return a value so the method under test can continue its execu-
tion. If we were testing a method that depends on this getAllInvoices method, we
could stub it to return an empty list, then return a list with one element, then return a
list with many elements, and so on. This would enable us to assert how the method
under test would work for lists of various lengths being returned from the database. 
6.1.4
Mocks
Mock objects act like stubs in the sense that you can configure how they reply if a
method is called: for example, to return a list of invoices when getAllInvoices is
called. However, mocks go beyond that. They save all the interactions and allow you to
make assertions afterward. For example, maybe we only want the getAllInvoices
method to be called once. If the method is called twice by the class under test, this is a
bug, and the test should fail. At the end of our test, we can write an assertion along the
lines of “verify that getAllInvoices was called just once.”
 Mocking frameworks let you assert all sorts of interactions, such as “the method
was never called with this specific parameter” or “the method was called twice with
parameter A and once with parameter B.” Mocks are also popular in industry since
they can provide insight into how classes interact. 
6.1.5
Spies
As the name suggests, spies spy on a dependency. They wrap themselves around the
real object and observe its behavior. Strictly speaking, we are not simulating the object
but rather recording all the interactions with the underlying object we are spying on.


