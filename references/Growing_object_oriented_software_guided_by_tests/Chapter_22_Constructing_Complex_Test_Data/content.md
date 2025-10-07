Line 1: 
Line 2: --- 페이지 282 ---
Line 3: Chapter 22
Line 4: Constructing Complex Test
Line 5: Data
Line 6: Many attempts to communicate are nulliﬁed by saying too much.
Line 7: —Robert Greenleaf
Line 8: Introduction
Line 9: If we are strict about our use of constructors and immutable value objects, con-
Line 10: structing objects in tests can be a chore. In production code, we construct such
Line 11: objects in relatively few places and all the required values are available to hand
Line 12: from, for example, user input, a database query, or a received message. In tests,
Line 13: however, we have to provide all the constructor arguments every time we want
Line 14: to create an object:
Line 15: @Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
Line 16:   Order order = new Order(
Line 17:       new Customer("Sherlock Holmes",
Line 18:           new Address("221b Baker Street", 
Line 19:                       "London", 
Line 20:                       new PostCode("NW1", "3RX"))));
Line 21:   order.addLine(new OrderLine("Deerstalker Hat", 1));
Line 22:   order.addLine(new OrderLine("Tweed Cape", 1));
Line 23: […]
Line 24: }
Line 25: The code to create all these objects makes the tests hard to read, ﬁlling them
Line 26: with information that doesn’t contribute to the behavior being tested. It also
Line 27: makes tests brittle, as changes to the constructor arguments or the structure of
Line 28: the objects will break many tests. The object mother pattern [Schuh01] is one
Line 29: attempt to avoid this problem. An object mother is a class that contains a number
Line 30: of factory methods [Gamma94] that create objects for use in tests. For example,
Line 31: we could write an object mother for orders:
Line 32: Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
Line 33: An object mother makes tests more readable by packaging up the code that
Line 34: creates new object structures and giving it a name. It also helps with maintenance
Line 35: since its features can be reused between tests. On the other hand, the object
Line 36: 257
Line 37: 
Line 38: --- 페이지 283 ---
Line 39: mother pattern does not cope well with variation in the test data—every minor
Line 40: difference requires a new factory method:
Line 41: Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Line 42: Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
Line 43: […]
Line 44: Over time, an object mother may itself become too messy to support, either
Line 45: full of duplicated code or refactored into an inﬁnity of ﬁne-grained methods.
Line 46: Test Data Builders
Line 47: Another solution is to use the builder pattern to build instances in tests, most
Line 48: often for values. For a class that requires complex setup, we create a test data
Line 49: builder that has a ﬁeld for each constructor parameter, initialized to a safe value.
Line 50: The builder has “chainable” public methods for overwriting the values in its
Line 51: ﬁelds and, by convention, a build() method that is called last to create a new
Line 52: instance of the target object from the ﬁeld values.1 An optional reﬁnement is to
Line 53: add a static factory method for the builder itself so that it’s clearer in the test
Line 54: what is being built. For example, a builder for Order objects might look like:
Line 55: public class OrderBuilder {
Line 56:   private Customer customer = new CustomerBuilder().build();
Line 57:   private List<OrderLine> lines = new ArrayList<OrderLine>();
Line 58:   private BigDecimal discountRate = BigDecimal.ZERO;
Line 59:   public static OrderBuilder anOrder() {
Line 60:     return new OrderBuilder();
Line 61:   }
Line 62:   public OrderBuilder withCustomer(Customer customer) {
Line 63:     this.customer = customer;
Line 64:     return this;
Line 65:   }
Line 66:   public OrderBuilder withOrderLines(OrderLines lines) {
Line 67:     this.lines = lines;
Line 68:     return this;
Line 69:   }
Line 70:   public OrderBuilder withDiscount(BigDecimal discountRate) {
Line 71:     this.discountRate = discountRate;
Line 72:     return this;
Line 73:   }
Line 74:   public Order build() {
Line 75:     Order order = new Order(customer);
Line 76:     for (OrderLine line : lines) order.addLine(line);
Line 77:       order.setDiscountRate(discountRate);
Line 78:     }
Line 79:   }
Line 80: }
Line 81: 1. This pattern is essentially the same as a Smalltalk cascade.
Line 82: Chapter 22
Line 83: Constructing Complex Test Data
Line 84: 258
Line 85: 
Line 86: --- 페이지 284 ---
Line 87: Tests that just need an Order object and are not concerned with its contents
Line 88: can create one in a single line:
Line 89: Order order = new OrderBuilder().build();
Line 90: Tests that need particular values within an object can specify just those values
Line 91: that are relevant and use defaults for the rest. This makes the test more expressive
Line 92: because it includes only the values that are relevant to the expected results.
Line 93: For example, if a test needed an Order for a Customer with no postcode, we
Line 94: would write:
Line 95: new OrderBuilder()
Line 96:   .fromCustomer(
Line 97:      new CustomerBuilder()
Line 98:       .withAddress(new AddressBuilder().withNoPostcode().build())
Line 99:       .build())
Line 100:   .build();
Line 101: We ﬁnd that test data builders help keep tests expressive and resilient to change.
Line 102: First, they wrap up most of the syntax noise when creating new objects. Second,
Line 103: they make the default case simple, and special cases not much more complicated.
Line 104: Third, they protect the test against changes in the structure of its objects. If we
Line 105: add an argument to a constructor, then all we have to change is the relevant
Line 106: builder and those tests that drove the need for the new argument.
Line 107: A ﬁnal beneﬁt is that we can write test code that’s easier to read and spot errors,
Line 108: because each builder method identiﬁes the purpose of its parameter. For example,
Line 109: in this code it’s not obvious that “London” has been passed in as the second
Line 110: street line rather than the city name:
Line 111: TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");
Line 112: A test data builder makes the mistake more obvious:
Line 113: new AddressBuilder()
Line 114:   .withStreet("221b Baker Street")
Line 115:   .withStreet2("London")
Line 116:   .withPostCode("NW1 6XE")
Line 117:   .build();
Line 118: Creating Similar Objects
Line 119: We can use builders when we need to create multiple similar objects. The most
Line 120: obvious approach is to create a new builder for each new object, but this leads
Line 121: to duplication and makes the test code harder to work with. For example, these
Line 122: two orders are identical apart from the discount. If we didn’t highlight the
Line 123: difference, it would be difﬁcult to ﬁnd:
Line 124: 259
Line 125: Creating Similar Objects
Line 126: 
Line 127: --- 페이지 285 ---
Line 128: Order orderWithSmallDiscount = new OrderBuilder()
Line 129:   .withLine("Deerstalker Hat", 1)
Line 130:   .withLine("Tweed Cape", 1)
Line 131:   .withDiscount(0.10)
Line 132:   .build();
Line 133: Order orderWithLargeDiscount = new OrderBuilder()
Line 134:   .withLine("Deerstalker Hat", 1)
Line 135:   .withLine("Tweed Cape", 1)
Line 136:   .withDiscount(0.25)
Line 137:   .build(); 
Line 138: Instead, we can initialize a single builder with the common state and then, for
Line 139: each object to be built, deﬁne the differing values and call its build() method:
Line 140: OrderBuilder hatAndCape = new OrderBuilder()
Line 141:   .withLine("Deerstalker Hat", 1)
Line 142:   .withLine("Tweed Cape", 1);
Line 143: Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Line 144: Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
Line 145: This produces a more focused test with less code. We can name the builder
Line 146: after the features that are common, and the domain objects after their differences.
Line 147: This technique works best if the objects differ by the same ﬁelds. If the objects
Line 148: vary by different ﬁelds, each build() will pick up the changes from the previous
Line 149: uses. For example, it’s not obvious in this code that orderWithGiftVoucher will
Line 150: carry the 10% discount as well as a gift voucher:
Line 151: Order orderWithDiscount = hatAndCape.withDiscount(0.10).build(); 
Line 152: Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build(); 
Line 153: To avoid this problem, we could add a copy constructor or a method that
Line 154: duplicates the state from another builder:
Line 155: Order orderWithDiscount = new OrderBuilder(hatAndCape)
Line 156:   .withDiscount(0.10)
Line 157:   .build();
Line 158: Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
Line 159:   .withGiftVoucher("abc")
Line 160:   .build();
Line 161: Alternatively, we could add a factory method that returns a copy of the builder
Line 162: with its current state:
Line 163: Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Line 164: Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build(); 
Line 165: For complex setups, the safest option is to make the “with” methods functional
Line 166: and have each one return a new copy of the builder instead of itself.
Line 167: Chapter 22
Line 168: Constructing Complex Test Data
Line 169: 260
Line 170: 
Line 171: --- 페이지 286 ---
Line 172: Combining Builders
Line 173: Where a test data builder for an object uses other “built” objects, we can pass
Line 174: in those builders as arguments rather than their objects. This will simplify the
Line 175: test code by removing the build() methods. The result is easier to read because
Line 176: it emphasizes the important information—what is being built—rather than the
Line 177: mechanics of building it. For example, this code builds an order with no postcode,
Line 178: but it’s dominated by the builder infrastructure:
Line 179: Order orderWithNoPostcode = new OrderBuilder()
Line 180:   .fromCustomer(
Line 181:     new CustomerBuilder()
Line 182:         .withAddress(new AddressBuilder().withNoPostcode().build())
Line 183:         .build())
Line 184:     .build();
Line 185: We can remove much of the noise by passing around builders:
Line 186: Order order = new OrderBuilder()
Line 187:   .fromCustomer(
Line 188:      new CustomerBuilder()
Line 189:       .withAddress(new AddressBuilder().withNoPostcode())))
Line 190:   .build();
Line 191: Emphasizing the Domain Model with Factory Methods
Line 192: We can further reduce the noise in the test code by wrapping up the construction
Line 193: of the builders in factory methods:
Line 194: Order order = 
Line 195: anOrder().fromCustomer(
Line 196: aCustomer().withAddress(anAddress().withNoPostcode())).build();
Line 197: As we compress the test code, the duplication in the builders becomes more
Line 198: obtrusive; we have the name of the constructed type in both the “with” and
Line 199: “builder” methods. We can take advantage of Java’s method overloading by
Line 200: collapsing this to a single with() method, letting the Java type system ﬁgure out
Line 201: which ﬁeld to update:
Line 202: Order order = 
Line 203:   anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
Line 204: Obviously, this will only work with one argument of each type. For example,
Line 205: if we introduce a Postcode, we can use overloading, whereas the rest of the builder
Line 206: methods must have explicit names because they use String:
Line 207: Address aLongerAddress = anAddress()
Line 208:     .withStreet("221b Baker Street")
Line 209:     .withCity("London")
Line 210:     .with(postCode("NW1", "3RX"))
Line 211:     .build();
Line 212: 261
Line 213: Emphasizing the Domain Model with Factory Methods
Line 214: 
Line 215: --- 페이지 287 ---
Line 216: This should encourage us to introduce domain types, which, as we wrote in
Line 217: “Domain Types Are Better Than Strings” (page 213), leads to more expressive
Line 218: and maintainable code.
Line 219: Removing Duplication at the Point of Use
Line 220: We’ve made the process of assembling complex objects for tests simpler and more
Line 221: expressive by using test data builders. Now, let’s look at how we can structure
Line 222: our tests to make the best use of these builders in context. We often ﬁnd ourselves
Line 223: writing tests with similar code to create supporting objects and pass them to the
Line 224: code under test, so we want to clean up this duplication. We’ve found that some
Line 225: refactorings are better than others; here’s an example.
Line 226: First, Remove Duplication
Line 227: We have a system that processes orders asynchronously. The test feeds orders
Line 228: into the system, tracks their progress on a monitor, and then looks for them in
Line 229: a user interface. We’ve packaged up all the infrastructure so the test looks like this:
Line 230: @Test public void reportsTotalSalesOfOrderedProducts() {
Line 231:   Order order1 = anOrder()
Line 232:     .withLine("Deerstalker Hat", 1)
Line 233:     .withLine("Tweed Cape", 1)
Line 234:     .withCustomersReference(1234)
Line 235:     .build();
Line 236:   requestSender.send(order1);
Line 237:   progressMonitor.waitForCompletion(order1);
Line 238:   Order order2 = anOrder()
Line 239:     .withLine("Deerstalker Hat", 1)
Line 240:     .withCustomersReference(5678)
Line 241:     .build();
Line 242:   requestSender.send(order2);
Line 243:   progressMonitor.waitForCompletion(order2);
Line 244:   TotalSalesReport report = gui.openSalesReport();
Line 245:   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line 246:   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line 247: }
Line 248: There’s an obvious duplication in the way the orders are created, sent, and
Line 249: tracked. Our ﬁrst thought might be to pull that into a helper method:
Line 250: @Test public void reportsTotalSalesOfOrderedProducts() {
Line 251: submitOrderFor("Deerstalker Hat", "Tweed Cape");
Line 252: submitOrderFor("Deerstalker Hat");
Line 253:   TotalSalesReport report = gui.openSalesReport();
Line 254:   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line 255:   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line 256: }
Line 257: Chapter 22
Line 258: Constructing Complex Test Data
Line 259: 262
Line 260: 
Line 261: --- 페이지 288 ---
Line 262: void submitOrderFor(String ... products) {
Line 263:   OrderBuilder orderBuilder = anOrder()
Line 264:     .withCustomersReference(nextCustomerReference());
Line 265:   for (String product : products) {
Line 266:     orderBuilder = orderBuilder.withLine(product, 1);
Line 267:   }
Line 268:   Order order = orderBuilder.build();
Line 269:   requestSender.send(order);
Line 270:   progressMonitor.waitForCompletion(order);
Line 271: }
Line 272: This refactoring works ﬁne when there’s a single case but, like the object
Line 273: mother pattern, does not scale well when we have variation. As we deal with
Line 274: orders with different contents, amendments, cancellations, and so on, we end up
Line 275: with this sort of mess:
Line 276: void submitOrderFor(String ... products) { […]
Line 277: void submitOrderFor(String product, int count, 
Line 278:                     String otherProduct, int otherCount) { […]
Line 279: void submitOrderFor(String product, double discount) { […]
Line 280: void submitOrderFor(String product, String giftVoucherCode) { […]
Line 281: We think a bit harder about what varies between tests and what is common,
Line 282: and realize that a better alternative is to pass the builder through, not its argu-
Line 283: ments; it’s similar to when we started combining builders. The helper method
Line 284: can use the builder to add any supporting detail to the order before feeding it
Line 285: into the system:
Line 286: @Test public void reportsTotalSalesOfOrderedProducts() {
Line 287: sendAndProcess(anOrder()
Line 288:     .withLine("Deerstalker Hat", 1)
Line 289:     .withLine("Tweed Cape", 1));
Line 290: sendAndProcess(anOrder()
Line 291:     .withLine("Deerstalker Hat", 1));
Line 292:   TotalSalesReport report = gui.openSalesReport();
Line 293:   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line 294:   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line 295: }
Line 296: void sendAndProcess(OrderBuilder orderDetails) {
Line 297:   Order order = orderDetails
Line 298:     .withDefaultCustomersReference(nextCustomerReference())
Line 299:     .build();
Line 300:   requestSender.send(order);
Line 301:   progressMonitor.waitForCompletion(order);
Line 302: }
Line 303: 263
Line 304: Removing Duplication at the Point of Use
Line 305: 
Line 306: --- 페이지 289 ---
Line 307: Then, Raise the Game
Line 308: The test code is looking better, but it still reads like a script. We can change its
Line 309: emphasis to what behavior is expected, rather than how the test is implemented,
Line 310: by rewording some of the names:
Line 311: @Test public void reportsTotalSalesOfOrderedProducts() {
Line 312: havingReceived(anOrder()
Line 313:       .withLine("Deerstalker Hat", 1)
Line 314:       .withLine("Tweed Cape", 1));
Line 315: havingReceived(anOrder()
Line 316:       .withLine("Deerstalker Hat", 1));
Line 317:   TotalSalesReport report = gui.openSalesReport();
Line 318:   report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
Line 319:   report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
Line 320: }
Line 321: @Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
Line 322:   Customer theCustomer = aCustomer().build();
Line 323: havingReceived(anOrder().from(theCustomer)
Line 324:     .withLine("Deerstalker Hat", 1)
Line 325:     .withLine("Tweed Cape", 1));
Line 326: havingReceived(anOrderAmendment().from(theCustomer)
Line 327:     .withLine("Deerstalker Hat", 2));
Line 328:   TotalSalesReport report = user.openSalesReport();
Line 329:   report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
Line 330:   report.containsTotalSalesFor("Tweed Cape", equalTo(1));
Line 331: }
Line 332: We started with a test that looked procedural, extracted some of its behavior
Line 333: into builder objects, and ended up with a declarative description of what the
Line 334: feature does. We’re nudging the test code towards the sort of language we could
Line 335: use when discussing the feature with someone else, even someone non-technical;
Line 336: we push everything else into supporting code.
Line 337: Communication First
Line 338: We use test data builders to reduce duplication and make the test code more ex-
Line 339: pressive. It’s another technique that reﬂects our obsession with the language of
Line 340: code, driven by the principle that code is there to be read. Combined with factory
Line 341: methods and test scaffolding, test data builders help us write more literate,
Line 342: declarative tests that describe the intention of a feature, not just a sequence of
Line 343: steps to drive it.
Line 344: Using these techniques, we can even use higher-level tests to communicate di-
Line 345: rectly with non-technical stakeholders, such as business analysts. If they’re willing
Line 346: Chapter 22
Line 347: Constructing Complex Test Data
Line 348: 264
Line 349: 
Line 350: --- 페이지 290 ---
Line 351: to ignore the obscure punctuation, we can use the tests to help us narrow down
Line 352: exactly what a feature should do, and why.
Line 353: There are other tools that are designed to foster collaboration across the
Line 354: technical and non-technical members in a team, such as FIT [Mugridge05]. We’ve
Line 355: found, as have others such as the LiFT team [LIFT], that we can achieve much
Line 356: of this while staying within our development toolset—and, of course, we can
Line 357: write better tests for ourselves.
Line 358: 265
Line 359: Communication First
Line 360: 
Line 361: --- 페이지 291 ---
Line 362: This page intentionally left blank 