# 22.5 Emphasizing the Domain Model with Factory Methods (pp.261-262)

---
**Page 261**

Combining Builders
Where a test data builder for an object uses other “built” objects, we can pass
in those builders as arguments rather than their objects. This will simplify the
test code by removing the build() methods. The result is easier to read because
it emphasizes the important information—what is being built—rather than the
mechanics of building it. For example, this code builds an order with no postcode,
but it’s dominated by the builder infrastructure:
Order orderWithNoPostcode = new OrderBuilder()
  .fromCustomer(
    new CustomerBuilder()
        .withAddress(new AddressBuilder().withNoPostcode().build())
        .build())
    .build();
We can remove much of the noise by passing around builders:
Order order = new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode())))
  .build();
Emphasizing the Domain Model with Factory Methods
We can further reduce the noise in the test code by wrapping up the construction
of the builders in factory methods:
Order order = 
anOrder().fromCustomer(
aCustomer().withAddress(anAddress().withNoPostcode())).build();
As we compress the test code, the duplication in the builders becomes more
obtrusive; we have the name of the constructed type in both the “with” and
“builder” methods. We can take advantage of Java’s method overloading by
collapsing this to a single with() method, letting the Java type system ﬁgure out
which ﬁeld to update:
Order order = 
  anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
Obviously, this will only work with one argument of each type. For example,
if we introduce a Postcode, we can use overloading, whereas the rest of the builder
methods must have explicit names because they use String:
Address aLongerAddress = anAddress()
    .withStreet("221b Baker Street")
    .withCity("London")
    .with(postCode("NW1", "3RX"))
    .build();
261
Emphasizing the Domain Model with Factory Methods


---
**Page 262**

This should encourage us to introduce domain types, which, as we wrote in
“Domain Types Are Better Than Strings” (page 213), leads to more expressive
and maintainable code.
Removing Duplication at the Point of Use
We’ve made the process of assembling complex objects for tests simpler and more
expressive by using test data builders. Now, let’s look at how we can structure
our tests to make the best use of these builders in context. We often ﬁnd ourselves
writing tests with similar code to create supporting objects and pass them to the
code under test, so we want to clean up this duplication. We’ve found that some
refactorings are better than others; here’s an example.
First, Remove Duplication
We have a system that processes orders asynchronously. The test feeds orders
into the system, tracks their progress on a monitor, and then looks for them in
a user interface. We’ve packaged up all the infrastructure so the test looks like this:
@Test public void reportsTotalSalesOfOrderedProducts() {
  Order order1 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1)
    .withCustomersReference(1234)
    .build();
  requestSender.send(order1);
  progressMonitor.waitForCompletion(order1);
  Order order2 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withCustomersReference(5678)
    .build();
  requestSender.send(order2);
  progressMonitor.waitForCompletion(order2);
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
There’s an obvious duplication in the way the orders are created, sent, and
tracked. Our ﬁrst thought might be to pull that into a helper method:
@Test public void reportsTotalSalesOfOrderedProducts() {
submitOrderFor("Deerstalker Hat", "Tweed Cape");
submitOrderFor("Deerstalker Hat");
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
Chapter 22
Constructing Complex Test Data
262


