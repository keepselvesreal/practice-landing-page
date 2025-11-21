# 6.1.3 Defining the communication-based style (pp.122-123)

---
**Page 122**

122
CHAPTER 6
Styles of unit testing
Here’s an example of state-based testing. The Order class allows the client to add a
new product.
public class Order
{
private readonly List<Product> _products = new List<Product>();
public IReadOnlyList<Product> Products => _products.ToList();
public void AddProduct(Product product)
{
_products.Add(product);
}
}
[Fact]
public void Adding_a_product_to_an_order()
{
var product = new Product("Hand wash");
var sut = new Order();
sut.AddProduct(product);
Assert.Equal(1, sut.Products.Count);
Assert.Equal(product, sut.Products[0]);
}
The test verifies the Products collection after the addition is completed. Unlike
the example of output-based testing in listing 6.1, the outcome of AddProduct() is the
change made to the order’s state. 
6.1.3
Defining the communication-based style
Finally, the third style of unit testing is communication-based testing. This style uses
mocks to verify communications between the system under test and its collaborators
(figure 6.4).
Listing 6.2
State-based testing
State
veriﬁcation
State
veriﬁcation
Production code
Input
Figure 6.3
In state-based testing, tests verify the final state of the 
system after an operation is complete. The dashed circles represent that 
final state.


---
**Page 123**

123
Comparing the three styles of unit testing
The following listing shows an example of communication-based testing.
[Fact]
public void Sending_a_greetings_email()
{
var emailGatewayMock = new Mock<IEmailGateway>();
var sut = new Controller(emailGatewayMock.Object);
sut.GreetUser("user@email.com");
emailGatewayMock.Verify(
x => x.SendGreetingsEmail("user@email.com"),
Times.Once);
}
6.2
Comparing the three styles of unit testing
There’s nothing new about output-based, state-based, and communication-based
styles of unit testing. In fact, you already saw all of these styles previously in this book.
What’s interesting is comparing them to each other using the four attributes of a good
unit test. Here are those attributes again (refer to chapter 4 for more details):
Protection against regressions
Resistance to refactoring
Fast feedback
Maintainability
In our comparison, let’s look at each of the four separately.
Listing 6.3
Communication-based testing
Styles and schools of unit testing
The classical school of unit testing prefers the state-based style over the communication-
based one. The London school makes the opposite choice. Both schools use output-
based testing. 
Collaboration
veriﬁcation
Mocks
Production code
Input
Figure 6.4
In communication-based 
testing, tests substitute the SUT’s 
collaborators with mocks and verify 
that the SUT calls those 
collaborators correctly.


