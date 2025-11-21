# 22.1 Introduction (pp.257-258)

---
**Page 257**

Chapter 22
Constructing Complex Test
Data
Many attempts to communicate are nulliﬁed by saying too much.
—Robert Greenleaf
Introduction
If we are strict about our use of constructors and immutable value objects, con-
structing objects in tests can be a chore. In production code, we construct such
objects in relatively few places and all the required values are available to hand
from, for example, user input, a database query, or a received message. In tests,
however, we have to provide all the constructor arguments every time we want
to create an object:
@Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
  Order order = new Order(
      new Customer("Sherlock Holmes",
          new Address("221b Baker Street", 
                      "London", 
                      new PostCode("NW1", "3RX"))));
  order.addLine(new OrderLine("Deerstalker Hat", 1));
  order.addLine(new OrderLine("Tweed Cape", 1));
[…]
}
The code to create all these objects makes the tests hard to read, ﬁlling them
with information that doesn’t contribute to the behavior being tested. It also
makes tests brittle, as changes to the constructor arguments or the structure of
the objects will break many tests. The object mother pattern [Schuh01] is one
attempt to avoid this problem. An object mother is a class that contains a number
of factory methods [Gamma94] that create objects for use in tests. For example,
we could write an object mother for orders:
Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
An object mother makes tests more readable by packaging up the code that
creates new object structures and giving it a name. It also helps with maintenance
since its features can be reused between tests. On the other hand, the object
257


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


