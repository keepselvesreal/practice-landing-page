# 22.6 Removing Duplication at the Point of Use (pp.262-264)

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


---
**Page 263**

void submitOrderFor(String ... products) {
  OrderBuilder orderBuilder = anOrder()
    .withCustomersReference(nextCustomerReference());
  for (String product : products) {
    orderBuilder = orderBuilder.withLine(product, 1);
  }
  Order order = orderBuilder.build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
This refactoring works ﬁne when there’s a single case but, like the object
mother pattern, does not scale well when we have variation. As we deal with
orders with different contents, amendments, cancellations, and so on, we end up
with this sort of mess:
void submitOrderFor(String ... products) { […]
void submitOrderFor(String product, int count, 
                    String otherProduct, int otherCount) { […]
void submitOrderFor(String product, double discount) { […]
void submitOrderFor(String product, String giftVoucherCode) { […]
We think a bit harder about what varies between tests and what is common,
and realize that a better alternative is to pass the builder through, not its argu-
ments; it’s similar to when we started combining builders. The helper method
can use the builder to add any supporting detail to the order before feeding it
into the system:
@Test public void reportsTotalSalesOfOrderedProducts() {
sendAndProcess(anOrder()
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
sendAndProcess(anOrder()
    .withLine("Deerstalker Hat", 1));
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
void sendAndProcess(OrderBuilder orderDetails) {
  Order order = orderDetails
    .withDefaultCustomersReference(nextCustomerReference())
    .build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
263
Removing Duplication at the Point of Use


---
**Page 264**

Then, Raise the Game
The test code is looking better, but it still reads like a script. We can change its
emphasis to what behavior is expected, rather than how the test is implemented,
by rewording some of the names:
@Test public void reportsTotalSalesOfOrderedProducts() {
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1)
      .withLine("Tweed Cape", 1));
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1));
  TotalSalesReport report = gui.openSalesReport();
  report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
}
@Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
  Customer theCustomer = aCustomer().build();
havingReceived(anOrder().from(theCustomer)
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
havingReceived(anOrderAmendment().from(theCustomer)
    .withLine("Deerstalker Hat", 2));
  TotalSalesReport report = user.openSalesReport();
  report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.containsTotalSalesFor("Tweed Cape", equalTo(1));
}
We started with a test that looked procedural, extracted some of its behavior
into builder objects, and ended up with a declarative description of what the
feature does. We’re nudging the test code towards the sort of language we could
use when discussing the feature with someone else, even someone non-technical;
we push everything else into supporting code.
Communication First
We use test data builders to reduce duplication and make the test code more ex-
pressive. It’s another technique that reﬂects our obsession with the language of
code, driven by the principle that code is there to be read. Combined with factory
methods and test scaffolding, test data builders help us write more literate,
declarative tests that describe the intention of a feature, not just a sequence of
steps to drive it.
Using these techniques, we can even use higher-level tests to communicate di-
rectly with non-technical stakeholders, such as business analysts. If they’re willing
Chapter 22
Constructing Complex Test Data
264


