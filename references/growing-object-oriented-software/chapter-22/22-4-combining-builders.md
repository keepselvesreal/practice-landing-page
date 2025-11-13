# 22.4 Combining Builders (pp.261-261)

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


