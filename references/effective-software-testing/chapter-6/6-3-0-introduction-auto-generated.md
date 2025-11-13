# 6.3.0 Introduction [auto-generated] (pp.158-159)

---
**Page 158**

158
CHAPTER 6
Test doubles and mocks
  List<Invoice> invoices = Arrays.asList(mauricio, frank, steve);
  when(filter.lowValueInvoices()).thenReturn(invoices);
  String date = LocalDate.now()
    .format(DateTimeFormatter.ofPattern("MMddyyyy"));
  SapInvoice franksInvoice = new SapInvoice("Frank", 25, date + "Fr");
  doThrow(new SAPException())
    .when(sap).send(franksInvoice);  
  List<Invoice> failedInvoices = sender.sendLowValuedInvoices();   
  assertThat(failedInvoices).containsExactly(frank);               
  SapInvoice mauriciosInvoice =
    new SapInvoice("Mauricio", 20, date + "Ma");
  verify(sap).send(mauriciosInvoice);           
  SapInvoice stevesInvoice =
    new SapInvoice("Steve", 48, date + "St");
  verify(sap).send(stevesInvoice);              
}
NOTE
Creating SapInvoices is becoming a pain, given that we always need
to get the current date, put it in the MMddyyyy format, and concatenate it
with the first two letters of the customer’s name. You may want to extract all
this logic to a helper method or a helper class. Helper methods are wide-
spread in test code. Remember, test code is as important as production
code. All the best practices you follow when implementing your production
code should be applied to your test code, too. We will discuss test code qual-
ity in chapter 10.
Configuring mocks to throw exceptions enables us to test how our systems would
behave in unexpected scenarios. This is perfect for many software systems that inter-
act with external systems, which may not behave as expected. Think of a web service
that is not available for a second: would your application behave correctly if this hap-
pened? How would you test the program behavior without using mocks or stubs? How
would you force the web service API to throw you an exception? Doing so would be
harder than telling the mock to throw an exception.
 The requirement says one more thing: “A failure should not make the program
stop; rather, the program should try to send all the invoices, even though some of
them may fail.” We also tested that in our test method. We ensured that steve’s
invoice—the one after frank’s invoice, which throws the exception—is sent to SAP. 
6.3
Mocks in the real world
Now that you know how to write mocks and stubs and how you can write powerful tests
with them, it is time to discuss best practices. As you can imagine, some developers are
big fans of mocking. Others believe mocks should not be used. It is a fact that mocks
make your tests less real.
Configures the mock to throw an exception 
when it receives Frank’s invoice. Note the call to 
doThrow().when(): this is the first time we use it.
Gets the returned list of failed
invoices and ensures that it
only has Frank’s invoice
Asserts that we tried to 
send both Maurício’s 
and Steve’s invoices


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


