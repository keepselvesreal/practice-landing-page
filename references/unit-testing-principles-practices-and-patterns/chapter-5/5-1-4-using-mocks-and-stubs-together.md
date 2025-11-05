# 5.1.4 Using mocks and stubs together (pp.97-97)

---
**Page 97**

97
Differentiating mocks from stubs
ject: not all uses of mocks lead to test fragility, but a lot of them do. You’ll see why later
in this chapter. 
5.1.4
Using mocks and stubs together
Sometimes you need to create a test double that exhibits the properties of both a
mock and a stub. For example, here’s a test from chapter 2 that I used to illustrate the
London style of unit testing.
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
var storeMock = new Mock<IStore>();
storeMock
    
.Setup(x => x.HasEnoughInventory(    
Product.Shampoo, 5))
    
.Returns(false);
    
var sut = new Customer();
bool success = sut.Purchase(
storeMock.Object, Product.Shampoo, 5);
Assert.False(success);
storeMock.Verify(
   
x => x.RemoveInventory(Product.Shampoo, 5),  
Times.Never);
   
}
This test uses storeMock for two purposes: it returns a canned answer and verifies a
method call made by the SUT. Notice, though, that these are two different methods:
the test sets up the answer from HasEnoughInventory() but then verifies the call to
RemoveInventory(). Thus, the rule of not asserting interactions with stubs is not vio-
lated here.
 When a test double is both a mock and a stub, it’s still called a mock, not a stub.
That’s mostly the case because we need to pick one name, but also because being a
mock is a more important fact than being a stub. 
5.1.5
How mocks and stubs relate to commands and queries
The notions of mocks and stubs tie to the command query separation (CQS) princi-
ple. The CQS principle states that every method should be either a command or a
query, but not both. As shown in figure 5.3, commands are methods that produce side
effects and don’t return any value (return void). Examples of side effects include
mutating an object’s state, changing a file in the file system, and so on. Queries are the
opposite of that—they are side-effect free and return a value.
 To follow this principle, be sure that if a method produces a side effect, that
method’s return type is void. And if the method returns a value, it must stay side-effect
Listing 5.4
storeMock: both a mock and a stub
Sets up a 
canned 
answer
Examines a call 
from the SUT


