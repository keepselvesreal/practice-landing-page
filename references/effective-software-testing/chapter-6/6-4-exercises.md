# 6.4 Exercises (pp.169-170)

---
**Page 169**

169
Exercises
When mocking, prefer state testing rather than interaction testing. Google says you
should make sure you are asserting a change of state and/or the consequence
of the action under test, rather than the precise interaction that the action has
with the mocked object. Google’s point is similar to what we discussed about
mocks and coupling. Interaction testing tends to be too coupled with the imple-
mentation of the system under test.
While I agree with this point, properly written interaction tests are useful.
They tell you when the interaction changed. This is my rule of thumb: if what
matters in the class I am testing is the interaction between classes, I do interac-
tion testing (my assertions check that the interactions are as expected). When
what matters is the result of processing, I do state testing (my assertions check
the return value or whether the state of the class is as expected).
Avoid over-specified interaction tests. Focus on the relevant arguments and functions.
This is a good suggestion and best practice. Make sure you only mock and stub
what needs to be mocked and stubbed. Only verify the interactions that make
sense for that test. Do not verify every single interaction that happens.
Good interaction testing requires strict guidelines when designing the system under test.
Google engineers tend not to do this. Using mocks properly is challenging even for
senior developers. Focus on training and team education, and help your devel-
oper peers do better interaction testing. 
Exercises
6.1
Mocks, stubs, and fakes. What are they, and how do they differ from each other?
6.2
The following InvoiceFilter class is responsible for returning the invoices for
an amount smaller than 100.0. It uses the IssuedInvoices type, which is
responsible for communication with the database.
public class InvoiceFilter {
  private IssuedInvoices invoices;
  public InvoiceFilter(IssuedInvoices invoices) {
    this.invoices = invoices;
  }
  public List<Invoice> filter() {
    return invoices.all().stream()
        .filter(invoice -> invoice.getValue() < 100.0)
        .collect(toList());
  }
}
Which of the following statements about this class is false?
A Integration testing is the only way to achieve 100% branch coverage.
B Its implementation allows for dependency injection, which enables mocking.


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


