# 22.3 Creating Similar Objects (pp.259-261)

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


---
**Page 260**

Order orderWithSmallDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.10)
  .build();
Order orderWithLargeDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.25)
  .build(); 
Instead, we can initialize a single builder with the common state and then, for
each object to be built, deﬁne the differing values and call its build() method:
OrderBuilder hatAndCape = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1);
Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
This produces a more focused test with less code. We can name the builder
after the features that are common, and the domain objects after their differences.
This technique works best if the objects differ by the same ﬁelds. If the objects
vary by different ﬁelds, each build() will pick up the changes from the previous
uses. For example, it’s not obvious in this code that orderWithGiftVoucher will
carry the 10% discount as well as a gift voucher:
Order orderWithDiscount = hatAndCape.withDiscount(0.10).build(); 
Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build(); 
To avoid this problem, we could add a copy constructor or a method that
duplicates the state from another builder:
Order orderWithDiscount = new OrderBuilder(hatAndCape)
  .withDiscount(0.10)
  .build();
Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
  .withGiftVoucher("abc")
  .build();
Alternatively, we could add a factory method that returns a copy of the builder
with its current state:
Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build(); 
For complex setups, the safest option is to make the “with” methods functional
and have each one return a new copy of the builder instead of itself.
Chapter 22
Constructing Complex Test Data
260


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


