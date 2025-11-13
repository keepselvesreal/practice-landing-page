# 6.1.5 Spies (pp.144-145)

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


---
**Page 145**

145
An introduction to mocking frameworks
 Spies are used in very specific contexts, such as when it is much easier to use the
real implementation than a mock but you still want to assert how the method under
test interacts with the dependency. Spies are less common in the wild. 
6.2
An introduction to mocking frameworks
Mocking frameworks are available for virtually all programming languages. While they
may differ in their APIs, the underlying idea is the same. Here, I will use Mockito
(https://site.mockito.org), one of the most popular stubbing and mocking libraries
for Java. Mockito offers a simple API, enabling developers to set up stubs and define
expectations in mock objects with just a few lines of code. (Mockito is an extensive
framework, and we cover only part of it in this chapter. To learn more, take a look at
its documentation.)
 Mockito is so simple that knowing the following three methods is often enough:

mock(<class>)—Creates a mock object/stub of a given class. The class can be
specified by <ClassName>.class.

when(<mock>.<method>).thenReturn(<value>)—A chain of method calls that
defines the (stubbed) behavior of the method. In this case <value> is returned.
For example, to make the all method of an issuedInvoices mock return a list
of invoices, we write when(issuedInvoices.all()).thenReturn(someList-
Here).

verify(<mock>).<method>—Asserts that the interactions with the mock object
happened in the expected way. For example, if we want to ensure that the
method all of an issuedInvoices mock was invoked, we use verify(issued-
Invoices).all().
Let’s dive into concrete examples to illustrate Mockito’s main features and show you
how developers use mocking frameworks in practice. If you are already familiar with
Mockito, you can skip this section.
6.2.1
Stubbing dependencies
Let’s learn how to use Mockito and set up stubs with a practical example. Suppose we
have the following requirement:
The program must return all the issued invoices with values smaller than 100.
The collection of invoices can be found in our database. The class Issued-
Invoices already contains a method that retrieves all the invoices.
The code in listing 6.1 is a possible implementation of this requirement. Note that
IssuedInvoices is a class responsible for retrieving all the invoices from a real data-
base (for example, MySQL). For now, suppose it has a method all() (not shown) that
returns all the invoices in the database. The class sends SQL queries to the database
and returns invoices. You can check the (naive) implementation in the book’s code
repository.


