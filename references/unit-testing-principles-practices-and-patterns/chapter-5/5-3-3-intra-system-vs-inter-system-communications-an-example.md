# 5.3.3 Intra-system vs. inter-system communications: An example (pp.111-114)

---
**Page 111**

111
The relationship between mocks and test fragility
The use of mocks is beneficial when verifying the communication pattern between
your system and external applications. Conversely, using mocks to verify communica-
tions between classes inside your system results in tests that couple to implementation
details and therefore fall short of the resistance-to-refactoring metric.
5.3.3
Intra-system vs. inter-system communications: An example
To illustrate the difference between intra-system and inter-system communications, I’ll
expand on the example with the Customer and Store classes that I used in chapter 2
and earlier in this chapter. Imagine the following business use case:
A customer tries to purchase a product from a store.
If the amount of the product in the store is sufficient, then
– The inventory is removed from the store.
– An email receipt is sent to the customer.
– A confirmation is returned.
Let’s also assume that the application is an API with no user interface.
 In the following listing, the CustomerController class is an application service that
orchestrates the work between domain classes (Customer, Product, Store) and the
external application (EmailGateway, which is a proxy to an SMTP service).
public class CustomerController
{
public bool Purchase(int customerId, int productId, int quantity)
Listing 5.9
Connecting the domain model with external applications
Third-party
system
SMTP service
Implementation detail
Observable behavior (contract)
Observable behavior (contract)
Figure 5.12
Inter-system communications form the observable 
behavior of your application as a whole. Intra-system communications 
are implementation details.


---
**Page 112**

112
CHAPTER 5
Mocks and test fragility
{
Customer customer = _customerRepository.GetById(customerId);
Product product = _productRepository.GetById(productId);
bool isSuccess = customer.Purchase(
_mainStore, product, quantity);
if (isSuccess)
{
_emailGateway.SendReceipt(
customer.Email, product.Name, quantity);
}
return isSuccess;
}
}
Validation of input parameters is omitted for brevity. In the Purchase method, the
customer checks to see if there’s enough inventory in the store and, if so, decreases
the product amount.
 The act of making a purchase is a business use case with both intra-system and
inter-system communications. The inter-system communications are those between
the CustomerController application service and the two external systems: the third-
party application (which is also the client initiating the use case) and the email gate-
way. The intra-system communication is between the Customer and the Store domain
classes (figure 5.13).
 In this example, the call to the SMTP service is a side effect that is visible to the
external world and thus forms the observable behavior of the application as a whole.
Third-party
system
(external
client)
SMTP service
SendReceipt()
Customer
RemoveInventory()
Store
isSuccess
Figure 5.13
The example in listing 5.9 represented using the hexagonal 
architecture. The communications between the hexagons are inter-system 
communications. The communication inside the hexagon is intra-system.


---
**Page 113**

113
The relationship between mocks and test fragility
It also has a direct connection to the client’s goals. The client of the application is the
third-party system. This system’s goal is to make a purchase, and it expects the cus-
tomer to receive a confirmation email as part of the successful outcome.
 The call to the SMTP service is a legitimate reason to do mocking. It doesn’t lead
to test fragility because you want to make sure this type of communication stays in
place even after refactoring. The use of mocks helps you do exactly that.
 The next listing shows an example of a legitimate use of mocks.
[Fact]
public void Successful_purchase()
{
var mock = new Mock<IEmailGateway>();
var sut = new CustomerController(mock.Object);
bool isSuccess = sut.Purchase(
customerId: 1, productId: 2, quantity: 5);
Assert.True(isSuccess);
mock.Verify(
  
x => x.SendReceipt(
  
"customer@email.com", "Shampoo", 5),  
Times.Once);
  
}
Note that the isSuccess flag is also observable by the external client and also needs
verification. This flag doesn’t need mocking, though; a simple value comparison is
enough.
 Let’s now look at a test that mocks the communication between Customer and
Store.
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
var storeMock = new Mock<IStore>();
storeMock
.Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
.Returns(true);
var customer = new Customer();
bool success = customer.Purchase(
storeMock.Object, Product.Shampoo, 5);
Assert.True(success);
storeMock.Verify(
x => x.RemoveInventory(Product.Shampoo, 5),
Times.Once);
}
Listing 5.10
Mocking that doesn’t lead to fragile tests 
Listing 5.11
Mocking that leads to fragile tests 
Verifies that the 
system sent a receipt 
about the purchase


---
**Page 114**

114
CHAPTER 5
Mocks and test fragility
Unlike the communication between CustomerController and the SMTP service, the
RemoveInventory() method call from Customer to Store doesn’t cross the applica-
tion boundary: both the caller and the recipient reside inside the application. Also,
this method is neither an operation nor a state that helps the client achieve its goals.
The client of these two domain classes is CustomerController with the goal of making
a purchase. The only two members that have an immediate connection to this goal are
customer.Purchase() and store.GetInventory(). The Purchase() method initiates
the purchase, and GetInventory() shows the state of the system after the purchase is
completed. The RemoveInventory() method call is an intermediate step on the way to
the client’s goal—an implementation detail. 
5.4
The classical vs. London schools of unit testing, 
revisited
As a reminder from chapter 2 (table 2.1), table 5.2 sums up the differences between
the classical and London schools of unit testing.
In chapter 2, I mentioned that I prefer the classical school of unit testing over the
London school. I hope now you can see why. The London school encourages the use
of mocks for all but immutable dependencies and doesn’t differentiate between intra-
system and inter-system communications. As a result, tests check communications
between classes just as much as they check communications between your application
and external systems.
 This indiscriminate use of mocks is why following the London school often results
in tests that couple to implementation details and thus lack resistance to refactoring.
As you may remember from chapter 4, the metric of resistance to refactoring (unlike
the other three) is mostly a binary choice: a test either has resistance to refactoring or
it doesn’t. Compromising on this metric renders the test nearly worthless.
 The classical school is much better at this issue because it advocates for substitut-
ing only dependencies that are shared between tests, which almost always translates
into out-of-process dependencies such as an SMTP service, a message bus, and so on.
But the classical school is not ideal in its treatment of inter-system communications,
either. This school also encourages excessive use of mocks, albeit not as much as the
London school.
Table 5.2
The differences between the London and classical schools of unit testing
Isolation of
A unit is
Uses test doubles for
London school
Units
A class
All but immutable dependencies
Classical school
Unit tests
A class or a set of classes
Shared dependencies


