# 6.3.5 What do others say about mocking? (pp.168-169)

---
**Page 168**

168
CHAPTER 6
Test doubles and mocks
 Creating abstractions on top of dependencies that you do not own, as a way to gain
more control, is a common technique among developers. (The idea of only mocking
types you own was suggested by Freeman et al. in the paper that introduced the con-
cept of mock objects [2004] and by Mockito.) Doing so increases the overall complex-
ity of the system and requires maintaining another abstraction. But does the ease in
testing the system that we get from adding the abstraction compensate for the cost of
the increased complexity? Often, the answer is yes: it does pay off. 
6.3.5
What do others say about mocking?
As I said, some developers favor mocking, and others do not. Software Engineering at Goo-
gle, edited by Winters, Manshreck, and Wright (2020), has an entire chapter dedicated
to test doubles. Here’s what I understood from it, along with my own point of view:
Using test doubles requires the system to be designed for testability. Indeed, as we saw, if
you use mocks, you need to make sure the class under test can receive the mock.
Building test doubles faithful to the real implementation is challenging. Test doubles must
be as faithful as possible. If your mocks do not offer the same contracts and expec-
tations of the production class, your tests may all pass, but the software system
will fail in production. Whenever you are mocking, make sure your mocks faith-
fully represent the class you are mocking.
Prefer realism over isolation. When possible, opt for the real implementation instead of
fakes, stubs, or mocks. I fully agree with this. Although I did my best to convince
you about the usefulness of mocking (that was the point of this chapter), real-
ism always wins over isolation. I am pragmatic about it, though. If it is getting
too hard to test with the real dependency, I mock it.
The following are trade-offs to consider when deciding whether to use a test
double:
– The execution time of the real implementation—I also take the execution time of
the dependency into account when deciding to mock or not. I usually mock
slow dependencies.
– How much non-determinism we would get from using the real implementation—
While I did not discuss non-deterministic behavior, dependencies that pres-
ent such behavior may be good candidates for mocking.
When using the real implementation is not possible or too costly, prefer fakes over mocks. I
do not fully agree with this recommendation. In my opinion, you either use the
real implementation or mock it. A fake implementation may end up having the
same problems as a mock. How do you ensure that the fake implementation has
the same behavior as the real implementation? I rarely use fakes.
Excessive mocking can be dangerous, as tests become unclear (hard to comprehend), brittle
(may break too often), and less effective (reduced ability to detect faults). I agree. If you
are mocking too much or the class under test forces you to mock too much,
that may be a sign that the production class is poorly designed.


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


