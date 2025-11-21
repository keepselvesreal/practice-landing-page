# 6.2.4 Simulating exceptions (pp.157-158)

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


