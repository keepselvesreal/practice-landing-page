# 6.2.2 Mocks and expectations (pp.150-153)

---
**Page 150**

150
CHAPTER 6
Test doubles and mocks
6.2.2
Mocks and expectations
Next, let’s discuss mocks. Suppose our current system has a new requirement:
All low-valued invoices should be sent to our SAP system (a software that man-
ages business operations). SAP offers a sendInvoice web service that receives
invoices.
You know you probably want to test the new class without depending on a real full-
blown SAP web service. So, the SAPInvoiceSender class (which contains the main
logic of the feature) receives, via its constructor, a class that communicates with SAP.
For simplicity, suppose there is a SAP interface. The SAPInvoiceSender’s main method,
sendLowValuedInvoices, gets all the low-valued invoices using the InvoiceFilter
class discussed in the previous section and then passes the resulting invoices to SAP.
public interface SAP {   
  void send(Invoice invoice);
}
public class SAPInvoiceSender {
  private final InvoiceFilter filter;  
  private final SAP sap;               
  public SAPInvoiceSender(InvoiceFilter filter, SAP sap) {  
    this.filter = filter;
    this.sap = sap;
  }
  public void sendLowValuedInvoices() {  
    List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
    for(Invoice invoice : lowValuedInvoices) {
      sap.send(invoice);
    }
  }
}
Let’s test the SAPInvoiceSender class (see listing 6.6 for the implementation of the
test suite). For this test, we stub the InvoiceFilter class. For SAPInvoiceSender,
InvoiceFilter is a class that returns a list of invoices. It is not the goal of the current
test to test InvoiceFilter, so we should stub this class to facilitate testing the method
we do want to test. The stub returns a list of low-valued invoices.
 The main purpose of this test is to ensure that every low-valued invoice is sent to
SAP. How can we assert that this is happening without having the real SAP? It is sim-
ple: we ensure that the call to SAP’s send() method happened. How do we do that?
 Mockito, behind the scenes, records all the interactions with its mocks. This means
if we mock the SAP interface and pass it to the class under test, at the end of the test,
Listing 6.5
SAPInvoiceSender class
This interface encapsulates the communication 
with SAP. Note that it does not matter how the 
concrete implementation will work.
We have fields for both the 
required dependencies.
The two
dependencies
are required
by the
constructor
of the class.
The logic of the method is straightforward. 
We first get the low-value invoices from 
the InvoiceFilter. Then we pass each of 
them to SAP.


---
**Page 151**

151
An introduction to mocking frameworks
all we need to do is ask the mock whether the method is called. For that, we use
Mockito’s verify assertion (listing 6.6). Note the syntax: we repeat the method we
expect to be called. We can even pass the specific parameters we expect. In the case of
this test method, we expect the send method to be called for both the mauricio and
frank invoices.
public class SAPInvoiceSenderTest {
  private InvoiceFilter filter = mock(InvoiceFilter.class);   
  private SAP sap = mock(SAP.class);                          
  private SAPInvoiceSender sender =
    new SAPInvoiceSender(filter, sap);  
  @Test
  void sendToSap() {
    Invoice mauricio = new Invoice("Mauricio", 20);
    Invoice frank = new Invoice("Frank", 99);
    List<Invoice> invoices = Arrays.asList(mauricio, frank);
    when(filter.lowValueInvoices()).thenReturn(invoices);   
    sender.sendLowValuedInvoices();   
    verify(sap).send(mauricio);   
    verify(sap).send(frank);      
  }
}
Again, note how we define the expectations of the mock object. We know exactly how
the InvoiceFilter class should interact with the mock. When the test is executed,
Mockito checks whether these expectations were met and fails the test if they were not.
 If you want to see Mockito in action, comment out the call to sap.send() in the
sendLowValuedInvoices method to see the test fail. Mockito will say something like
what you see in listing 6.7. Mockito expected the send method to be called to the
“mauricio” invoice, but it was not. Mockito even complements the message and says
that it did not see any interactions with this mock. This is an extra tip to help you
debug the failing test.
Wanted but not invoked:
sap.send(        
    Invoice{customer='Mauricio', value=20}
);
Actually, there were zero interactions with this mock.
Listing 6.6
Tests for the SAPInvoiceSender class
Listing 6.7
Mockito’s verify-failing message
Instantiates all the mocks as fields. Nothing
changes in terms of behavior. JUnit instantiates
a new class before running each of the test
methods. This is a matter of taste, but I usually
like to have my mocks as fields, so I do not need
to instantiate them in every test method.
Passes the
mock and the
stub to the
class under
test
Sets up the 
InvoiceFilter stub. 
It will return two 
invoices whenever 
lowValueInvoices() 
is called.
Calls the
method
under test,
knowing
that these
two invoices
will be sent
to SAP
Ensures that the send method 
was called for both invoices
send() was not invoked 
for this invoice!


---
**Page 152**

152
CHAPTER 6
Test doubles and mocks
This example illustrates the main difference between stubbing and mocking. Stub-
bing means returning hard-coded values for a given method call. Mocking means
not only defining what methods do but also explicitly defining the interactions with
the mock.
 Mockito enables us to define even more specific expectations. For example, look
at the following expectations.
verify(sap, times(2)).send(any(Invoice.class));   
verify(sap, times(1)).send(mauricio);    
verify(sap, times(1)).send(frank);   
These expectations are more restrictive than the earlier ones. We now expect the SAP
mock to have its send method invoked precisely two times (for any given Invoice).
We then expect the send method to be called once for the mauricio invoice and once
for the frank invoice.
 Let’s write one more test so you become more familiar with Mockito. Let’s exercise
the case where there are no low-valued invoices. The code is basically the same as in
the previous test, but we make our stub return an empty list when the lowValue-
Invoices() method of InvoiceFilter is called. We then expect no interactions with
the SAP mock. That can be accomplished through the Mockito.never() and
Mockito.any() methods in combination with verify().
@Test
void noLowValueInvoices() {
  List<Invoice> invoices = emptyList();
  when(filter.lowValueInvoices()).thenReturn(invoices);   
  sender.sendLowValuedInvoices();
  verify(sap, never()).send(any(Invoice.class));   
}
You may wonder why I did not put this new SAP sending functionality in the existing
InvoiceFilter class. The lowValueInvoices method would then be both a command
and a query. Mixing both concepts in a single method is not a good idea, as it may
confuse developers who call this method. An advantage of separating commands from
queries is that, from a mocking perspective, you know what to do. You should stub the
queries, as you now know that queries return values and do not change the object’s
Listing 6.8
More Mockito expectations
Listing 6.9
Test for when there are no low-value invoices
Verifies that the send method was
called precisely twice for any invoice
Verifies that the send method 
was called precisely once for 
the “mauricio” invoice
Verifies that the send method was called
precisely once for the “frank” invoice
This time, the 
stub will return 
an empty list.
The important part of this 
test is the assertion. We 
ensure that the send() 
method was not invoked 
for any invoice.


---
**Page 153**

153
An introduction to mocking frameworks
state; and you should mock commands, as you know they change the world outside
the object under test.
NOTE
If you want to learn more, search for “command-query separation”
(CQS) or read Fowler’s wiki entry on CQS (2005). As you get used to testing
and writing tests, you will see that the better the code, the easier it is to test it.
In chapter 7, we will discuss code decisions you can make in your production
code to facilitate testing.
To learn more about the differences between mocks and stubs, see the article “Mocks
Aren’t Stubs,” by Martin Fowler (2007). 
6.2.3
Capturing arguments
Imagine a tiny change in the requirements of sending the invoice to the SAP feature:
Instead of receiving the Invoice entity directly, SAP now requires the data to
be sent in a different format. SAP requires the customer’s name, the value of
the invoice, and a generated ID.
The ID should have the following format: <date><customer code>.
The date should always be in the “MMddyyyy” format: <month><day><year
with 4 digits>.
The customer code should be the first two characters of the customer’s
first name. If the customer’s name has fewer than two characters, it should
be “X”.
Implementation-wise, we change the SAP interface to receive a new SapInvoice entity.
This entity has three fields: customer, value, and id. We then modify the SAPInvoice-
Sender so for each low-value invoice, it creates a new SapInvoice entity with the cor-
rect id and sends it to SAP. The next listing contains the new implementation.
public class SapInvoice {      
  private final String customer;
  private final int value;
  private final String id;
  public SapInvoice(String customer, int value, String id) {
    // constructor
  }
  // getters
}
public interface SAP {   
  void send(SapInvoice invoice);
}
Listing 6.10
Changing the SAP-related classes to support the new required format
A new entity to 
represent the 
new format
SAP receives this 
new SapInvoice 
entity.


