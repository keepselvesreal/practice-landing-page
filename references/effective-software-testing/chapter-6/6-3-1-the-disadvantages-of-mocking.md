# 6.3.1 The disadvantages of mocking (pp.159-160)

---
**Page 159**

159
Mocks in the real world
 When should we mock? When is it best not to mock? What other best practices
should I follow? I tackle those questions next.
6.3.1
The disadvantages of mocking
I have been talking a lot about the advantages of mocks. However, as I hinted before, a
common (and heated) discussion among practitioners is whether to use mocks. Let’s
look at possible disadvantages.
 Some developers strongly believe that using mocks may lead to test suites that test the
mock, not the code. That can happen. When you use mocks, you are naturally making your
test less realistic. In production, your code will use the concrete implementation of the
class you mocked during the test. Something may go wrong in the way the classes com-
municate in production, for example, and you may miss it because you mocked them.
 Consider a class A that depends on class B. Suppose class B offers a method sum()
that always returns positive numbers (that is, the post-condition of sum()). When test-
ing class A, the developer decides to mock B. Everything seems to work. Months later, a
developer changes the post-conditions of B’s sum(): now it also returns negative num-
bers. In a common development workflow, a developer would apply these changes in
B and update B’s tests to reflect the change. It is easy to forget to check whether A han-
dles this new post-condition well. Even worse, A’s test suite will still pass! A mocks B,
and the mock does not know that B changed. In large-scale software, it can be easy to
lose control of your mocks in the sense that mocks may not represent the real contract
of the class.
 For mock objects to work well on a large scale, developers must design careful
(and hopefully stable) contracts. If contracts are well designed and stable, you do not
need to be afraid of mocks. And although we use the example of a contract break as a
disadvantage of mocks, it is part of the coder’s job to find the dependencies of the
contract change and check that the new contract is covered, mocks or not.
 Another disadvantage is that tests that use mocks are naturally more coupled with
the code they test than tests that do not use mocks. Think of all the tests we have writ-
ten without mocks. They call a method, and they assert the output. They do not know
anything about the actual implementation of the method. Now, think of all the tests
we wrote in this chapter. The test methods know some things about the production
code. The tests we wrote for SAPInvoiceSender know that the class uses Invoice-
Filter’s lowValueInvoices method and that SAP’s send method must be called for all
the invoices. This is a lot of information about the class under test.
 What is the problem with the test knowing so much? It may be harder to change. If
the developer changes how the SAPInvoiceSender class does its job and, say, stops
using the InvoiceFilter class or uses the same filter differently, the developer may
also have to change the tests. The mocks and their expectations may be completely
different.
 Therefore, although mocks simplify our tests, they increase the coupling between
the test and the production code, which may force us to change the test whenever we


---
**Page 160**

160
CHAPTER 6
Test doubles and mocks
change the production code. Spadini and colleagues, including me, observed this
through empirical studies in open source systems (2019). Can you avoid such coupling?
Not really, but at least now you are aware of it.
 Interestingly, developers consider this coupling a major drawback of mocks. But I
appreciate that my tests break when I change how a class interacts with other classes.
The broken tests make me reflect on the changes I am making. Of course, my tests do
not break as a result of every minor change I make in my production code. I also do
not use mocks in every situation. I believe that when mocks are properly used, the
coupling with the production code is not a big deal.
6.3.2
What to mock and what not to mock
Mocks and stubs are useful tools for simplifying the process of writing unit tests.
However, mocking too much might also be a problem. A test that uses the real depen-
dencies is more real than a test that uses doubles and, consequently, is more prone
to find real bugs. Therefore, we do not want to mock a dependency that should not
be mocked. Imagine you are testing class A, which depends on class B. How do we
know whether we should mock or stub B or whether it is better to use the real, con-
crete implementation?
 Pragmatically, developers often mock or stub the following types of dependencies:
Dependencies that are too slow—If the dependency is too slow for any reason, it
might be a good idea to simulate it. We do not want slow test suites. Therefore,
I mock classes that deal with databases or web services. Note that I still do inte-
gration tests to ensure that these classes work properly, but I use mocks for all
the other classes that depend on these slow classes.
Dependencies that communicate with external infrastructure—If the dependency talks
to (external) infrastructure, it may be too slow or too complex to set up the
required infrastructure. So, I apply the same principle: whenever testing a class
that depends on a class that handles external infrastructure, I mock the depen-
dency (as we mocked the IssuedInvoices class when testing the Invoice-
Filter class). I then write integration tests for these classes.
Mocking as a design technique
Whenever I say that mocks increase coupling with production code, I am talking about
using mocks from a testing perspective: not using mocks as a way to design the code,
but in the sense of “This is the code we have: let’s test it.” In this case, mocks are
naturally coupled with the code under test, and changes in the code will impact
the mocks.
If you are using mocks as a design technique (as explained in Freeman and Pryce’s
2009 book), you should look at it from a different angle. You want your mocks to be
coupled with the code under test because you care about how the code does its job.
If the code changes, you want your mocks to change. 


