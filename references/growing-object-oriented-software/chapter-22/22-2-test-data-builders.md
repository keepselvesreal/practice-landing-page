# 22.2 Test Data Builders (pp.258-259)

---
**Page 258**

mother pattern does not cope well with variation in the test data—every minor
difference requires a new factory method:
Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
[…]
Over time, an object mother may itself become too messy to support, either
full of duplicated code or refactored into an inﬁnity of ﬁne-grained methods.
Test Data Builders
Another solution is to use the builder pattern to build instances in tests, most
often for values. For a class that requires complex setup, we create a test data
builder that has a ﬁeld for each constructor parameter, initialized to a safe value.
The builder has “chainable” public methods for overwriting the values in its
ﬁelds and, by convention, a build() method that is called last to create a new
instance of the target object from the ﬁeld values.1 An optional reﬁnement is to
add a static factory method for the builder itself so that it’s clearer in the test
what is being built. For example, a builder for Order objects might look like:
public class OrderBuilder {
  private Customer customer = new CustomerBuilder().build();
  private List<OrderLine> lines = new ArrayList<OrderLine>();
  private BigDecimal discountRate = BigDecimal.ZERO;
  public static OrderBuilder anOrder() {
    return new OrderBuilder();
  }
  public OrderBuilder withCustomer(Customer customer) {
    this.customer = customer;
    return this;
  }
  public OrderBuilder withOrderLines(OrderLines lines) {
    this.lines = lines;
    return this;
  }
  public OrderBuilder withDiscount(BigDecimal discountRate) {
    this.discountRate = discountRate;
    return this;
  }
  public Order build() {
    Order order = new Order(customer);
    for (OrderLine line : lines) order.addLine(line);
      order.setDiscountRate(discountRate);
    }
  }
}
1. This pattern is essentially the same as a Smalltalk cascade.
Chapter 22
Constructing Complex Test Data
258


---
**Page 259**

Tests that just need an Order object and are not concerned with its contents
can create one in a single line:
Order order = new OrderBuilder().build();
Tests that need particular values within an object can specify just those values
that are relevant and use defaults for the rest. This makes the test more expressive
because it includes only the values that are relevant to the expected results.
For example, if a test needed an Order for a Customer with no postcode, we
would write:
new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode().build())
      .build())
  .build();
We ﬁnd that test data builders help keep tests expressive and resilient to change.
First, they wrap up most of the syntax noise when creating new objects. Second,
they make the default case simple, and special cases not much more complicated.
Third, they protect the test against changes in the structure of its objects. If we
add an argument to a constructor, then all we have to change is the relevant
builder and those tests that drove the need for the new argument.
A ﬁnal beneﬁt is that we can write test code that’s easier to read and spot errors,
because each builder method identiﬁes the purpose of its parameter. For example,
in this code it’s not obvious that “London” has been passed in as the second
street line rather than the city name:
TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");
A test data builder makes the mistake more obvious:
new AddressBuilder()
  .withStreet("221b Baker Street")
  .withStreet2("London")
  .withPostCode("NW1 6XE")
  .build();
Creating Similar Objects
We can use builders when we need to create multiple similar objects. The most
obvious approach is to create a new builder for each new object, but this leads
to duplication and makes the test code harder to work with. For example, these
two orders are identical apart from the discount. If we didn’t highlight the
difference, it would be difﬁcult to ﬁnd:
259
Creating Similar Objects


