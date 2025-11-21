# 6.1.1 Defining the output-based style (pp.120-121)

---
**Page 120**

120
CHAPTER 6
Styles of unit testing
 Note that this chapter doesn’t provide a deep dive into the topic of functional pro-
gramming. Still, by the end of this chapter, I hope you’ll have an intuitive understand-
ing of how functional programming relates to output-based testing. You’ll also learn
how to write more of your tests using the output-based style, as well as the limitations
of functional programming and functional architecture.
6.1
The three styles of unit testing
As I mentioned in the chapter introduction, there are three styles of unit testing:
Output-based testing 
State-based testing 
Communication-based testing
You can employ one, two, or even all three styles together in a single test. This sec-
tion lays the foundation for the whole chapter by defining (with examples) those
three styles of unit testing. You’ll see how they score against each other in the sec-
tion after that.
6.1.1
Defining the output-based style
The first style of unit testing is the output-based style, where you feed an input to the sys-
tem under test (SUT) and check the output it produces (figure 6.1). This style of unit
testing is only applicable to code that doesn’t change a global or internal state, so the
only component to verify is its return value.
The following listing shows an example of such code and a test covering it. The Price-
Engine class accepts an array of products and calculates a discount.
public class PriceEngine
{
public decimal CalculateDiscount(params Product[] products)
Listing 6.1
Output-based testing
Output
Production code
Input
Output
veriﬁcation
Figure 6.1
In output-based testing, tests verify the output the system 
generates. This style of testing assumes there are no side effects and the only 
result of the SUT’s work is the value it returns to the caller.


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


