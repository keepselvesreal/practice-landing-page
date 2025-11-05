# 6.1.2 Defining the state-based style (pp.121-122)

---
**Page 121**

121
The three styles of unit testing
{
decimal discount = products.Length * 0.01m;
return Math.Min(discount, 0.2m);
}
}
[Fact]
public void Discount_of_two_products()
{
var product1 = new Product("Hand wash");
var product2 = new Product("Shampoo");
var sut = new PriceEngine();
decimal discount = sut.CalculateDiscount(product1, product2);
Assert.Equal(0.02m, discount);
}
PriceEngine multiplies the number of products by 1% and caps the result at 20%.
There’s nothing else to this class. It doesn’t add the products to any internal collec-
tion, nor does it persist them in a database. The only outcome of the Calculate-
Discount() method is the discount it returns: the output value (figure 6.2).
The output-based style of unit testing is also known as functional. This name takes root
in functional programming, a method of programming that emphasizes a preference for
side-effect-free code. We’ll talk more about functional programming and functional
architecture later in this chapter. 
6.1.2
Defining the state-based style
The state-based style is about verifying the state of the system after an operation is com-
plete (figure 6.3). The term state in this style of testing can refer to the state of the
SUT itself, of one of its collaborators, or of an out-of-process dependency, such as
the database or the filesystem.
Output
veriﬁcation
Output
PriceEngine
Input
Product (“Hand wash”)
Product (“Shampoo”)
2% discount
Figure 6.2
PriceEngine represented using input-output notation. Its 
CalculateDiscount() method accepts an array of products and 
calculates a discount.


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


