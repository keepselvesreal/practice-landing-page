# 6.2.3 Capturing arguments (pp.153-157)

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


---
**Page 154**

154
CHAPTER 6
Test doubles and mocks
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
      String customer = invoice.getCustomer();
      int value = invoice.getValue();
      String sapId = generateId(invoice);
      SapInvoice sapInvoice =
        new SapInvoice(customer, value, sapId);   
      sap.send(sapInvoice);   
    }
  }
  private String generateId(Invoice invoice) {   
    String date = LocalDate.now().format(
      ➥ DateTimeFormatter.ofPattern("MMddyyyy"));
    String customer = invoice.getCustomer();
    return date +
      (customer.length()>=2 ? customer.substring(0,2) : "X");   
  }
}
When it comes to testing, we know that we should stub the InvoiceFilter class. We
can also mock the SAP class and ensure that the send() method was called, as shown
next.
@Test
void sendSapInvoiceToSap() {
  Invoice mauricio = new Invoice("Mauricio", 20);
  List<Invoice> invoices = Arrays.asList(mauricio);
  when(filter.lowValueInvoices()).thenReturn(invoices);  
  sender.sendLowValuedInvoices();
  verify(sap).send(any(SapInvoice.class));   
}
Listing 6.11
Test for the new implementation of SAPInvoiceSender
The constructor 
is the same as 
before.
Instantiates the 
new SAPInvoice 
object
Sends the new 
entity to SAP
Generates the 
required ID as in 
the requirements
Returns the 
date plus the 
customer’s 
code
Again, we stub 
InvoiceFilter.
Asserts that SAP received a SapInvoice. 
But which SapInvoice? Any. That is not 
good. We want to be more specific.


---
**Page 155**

155
An introduction to mocking frameworks
This test ensures that the send method of the SAP is called. But how do we assert that
the generated SapInvoice is the correct one? For example, how do we ensure that the
generated ID is correct?
 One idea could be to extract the logic of converting an Invoice to a SapInvoice,
as shown in listing 6.12. The convert() method receives an invoice, generates the
new id, and returns a SapInvoice. A simple class like this could be tested via unit tests
without any stubs or mocks. We can instantiate different Invoices, call the convert
method, and assert that the returned SapInvoice is correct. I leave that as an exercise
for you.
public class InvoiceToSapInvoiceConverter {
  public SapInvoice convert(Invoice invoice) {   
    String customer = invoice.getCustomer();
    int value = invoice.getValue();
    String sapId = generateId(invoice);
    SapInvoice sapInvoice = new SapInvoice(customer, value, sapId);
    return sapInvoice;
  }
  private String generateId(Invoice invoice) {   
    String date = LocalDate.now()
      .format(DateTimeFormatter.ofPattern("MMddyyyy"));
    String customer = invoice.getCustomer();
    return date +
      (customer.length()>=2 ? customer.substring(0,2) : "X");
  }
}
In chapter 10, we further discuss refactorings you can apply to your code to facilitate
testing. I strongly recommend doing so. But for the sake of argument, let’s suppose
this is not a possibility. How can we get the SapInvoice object generated in the cur-
rent implementation of SAPInvoiceSender and assert it? This is our chance to use
another of Mockito’s features: the argument captor.
 Mockito allows us to get the specific objects passed to its mocks. We then ask the
SAP mock to give us the SapInvoice passed to it during the execution of the method,
to make assertions on it (see listing 6.13). Instead of using any(SAPInvoice.class),
we pass an instance of an ArgumentCaptor. We then capture its value, which in this
case is an instance of SapInvoice. We make traditional assertions on the contents of
this object.
 
 
 
Listing 6.12
Class that converts from Invoice to SapInvoice
This method is straightforward. 
It does not depend on any 
complex classes, so we can 
write unit tests for it as we 
have done previously.
The same generateId 
method we saw 
before


---
**Page 156**

156
CHAPTER 6
Test doubles and mocks
@ParameterizedTest
@CsvSource({   
    "Mauricio,Ma",
    "M,X"}
)
void sendToSapWithTheGeneratedId(String customer, String customerCode) {
  Invoice mauricio = new Invoice(customer, 20);
  List<Invoice> invoices = Arrays.asList(mauricio);
  when(filter.lowValueInvoices()).thenReturn(invoices);
  sender.sendLowValuedInvoices();
  ArgumentCaptor<SapInvoice> captor =
    ArgumentCaptor.forClass(SapInvoice.class);   
  verify(sap).send(captor.capture());    
  SapInvoice generatedSapInvoice = captor.getValue();  
  String date = LocalDate.now().format(DateTimeFormatter.
    ofPattern("MMddyyyy"));
  assertThat(generatedSapInvoice)
    .isEqualTo(new SapInvoice(customer, 20, date + customerCode));   
}
Note that we have at least two different test cases to ensure that the generated ID is
correct: one where the customer’s name is longer than two characters and another
where it is shorter than two characters. Given that the structure of the test method
would be the same for both methods, I decided to use a parameterized test. I also used
the CsvSource to pass the different test cases to the test method. The CSV source
enables us to pass the inputs via comma-separated values. I usually go for CSV sources
whenever the inputs are simple and easily written, as in this case.
 Interestingly, although my first option is always to try to refactor the code so I can
write simple unit tests, I use argument captors often. In practice, it is common to have
such classes, where most of what you do is coordinate the data flow between different
components, and objects that need to be asserted may be created on the fly by the
method but not returned to the caller.
NOTE
There is another test I find fundamental in the sendToSapWithThe-
GeneratedId method: we are missing proper boundary testing. The length of
the customer’s name (two) is a boundary, so I would test with a customer name
that is precisely of length two. Again, we are discussing mocks, but when it
comes to designing test cases, all the techniques we have discussed apply. 
Listing 6.13
Test using the ArgumentCaptor feature of Mockito
Passes the two test cases. The test 
method is executed twice: once for 
“Mauricio” and once for “M”.
Instantiates an ArgumentCaptor 
with the type of the object we 
are expecting to capture
Calls the verify method 
and passes the argument 
captor as the parameter 
of the method
The argument
was already
captured.
Now we
extract it.
Uses a traditional assertion, ensuring
that the ID matches what is expected


---
**Page 157**

157
An introduction to mocking frameworks
6.2.4
Simulating exceptions
The developer realizes that SAP’s send method may throw a SapException if a prob-
lem occurs. This leads to a new requirement:
The system should return the list of invoices that failed to be sent to SAP. A
failure should not make the program stop. Instead, the program should try to
send all the invoices, even though some of them may fail.
One easy way to implement this is to try to catch any possible exceptions. If an excep-
tion happens, we store the failed invoice as shown in the following listing.
public List<Invoice> sendLowValuedInvoices() {
  List<Invoice> failedInvoices = new ArrayList<>();
  List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
  for(Invoice invoice : lowValuedInvoices) {
    String customer = invoice.getCustomer();
    int value = invoice.getValue();
    String sapId = generateId(invoice);
    SapInvoice sapInvoice = new SapInvoice(customer, value, sapId);
    try {       
      sap.send(sapInvoice);
    } catch(SAPException e) {
      failedInvoices.add(invoice);
    }
  }
  return failedInvoices;   
}
How do we test this? By now, you probably see that all we need to do is to force our sap
mock to throw an exception for one of the invoices. We should use Mockito’s doThrow()
.when() chain of calls. This is similar to the when() API you already know, but now we
want it to throw an exception (see listing 6.15). Note that we configure the mock to
throw an exception for the frank invoice. Then we assert that the list of failed invoices
returned by the new sendLowValuedInvoices contains that invoice and that SAP
was called for both the mauricio and the frank invoices. Also, because the SAP inter-
face receives a SapInvoice and not an Invoice, we must instantiate three invoices
(Maurício’s, Frank’s, and Steve’s) before asserting that the send method was called.
@Test
void returnFailedInvoices() {
  Invoice mauricio = new Invoice("Mauricio", 20);
  Invoice frank = new Invoice("Frank", 25);
  Invoice steve = new Invoice("Steve", 48);
Listing 6.14
Catching a possible SAPException
Listing 6.15
Mocks that throw exceptions
Catches the possible SAPException. 
If that happens, we store the failed 
invoice in a list.
Returns the 
list of failed 
invoices


