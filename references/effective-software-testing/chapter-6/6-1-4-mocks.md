# 6.1.4 Mocks (pp.144-144)

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


