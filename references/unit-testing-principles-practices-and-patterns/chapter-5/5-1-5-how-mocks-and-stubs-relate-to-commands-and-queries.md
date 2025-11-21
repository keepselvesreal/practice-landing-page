# 5.1.5 How mocks and stubs relate to commands and queries (pp.97-99)

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


---
**Page 98**

98
CHAPTER 5
Mocks and test fragility
free. In other words, asking a question should not change the answer. Code that main-
tains such a clear separation becomes easier to read. You can tell what a method does
just by looking at its signature, without diving into its implementation details.
 Of course, it’s not always possible to follow the CQS principle. There are always
methods for which it makes sense to both incur a side effect and return a value. A clas-
sical example is stack.Pop(). This method both removes a top element from the
stack and returns it to the caller. Still, it’s a good idea to adhere to the CQS principle
whenever you can.
 Test doubles that substitute commands become mocks. Similarly, test doubles that
substitute queries are stubs. Look at the two tests from listings 5.1 and 5.2 again (I’m
showing their relevant parts here):
var mock = new Mock<IEmailGateway>();
mock.Verify(x => x.SendGreetingsEmail("user@email.com"));
var stub = new Mock<IDatabase>();
stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
SendGreetingsEmail() is a command whose side effect is sending an email. The test
double that substitutes this command is a mock. On the other hand, GetNumberOf-
Users() is a query that returns a value and doesn’t mutate the database state. The cor-
responding test double is a stub. 
 
Methods
Commands
Incur side effects
No return value
Mocks
Queries
Side-effect free
Returns a value
Stubs
Figure 5.3
In the command query 
separation (CQS) principle, commands 
correspond to mocks, while queries are 
consistent with stubs.


---
**Page 99**

99
Observable behavior vs. implementation details
5.2
Observable behavior vs. implementation details
Section 5.1 showed what a mock is. The next step on the way to explaining the con-
nection between mocks and test fragility is diving into what causes such fragility.
 As you might remember from chapter 4, test fragility corresponds to the second
attribute of a good unit test: resistance to refactoring. (As a reminder, the four attri-
butes are protection against regressions, resistance to refactoring, fast feedback, and
maintainability.) The metric of resistance to refactoring is the most important
because whether a unit test possesses this metric is mostly a binary choice. Thus, it’s
good to max out this metric to the extent that the test still remains in the realm of unit
testing and doesn’t transition to the category of end-to-end testing. The latter, despite
being the best at resistance to refactoring, is generally much harder to maintain.
 In chapter 4, you also saw that the main reason tests deliver false positives (and thus
fail at resistance to refactoring) is because they couple to the code’s implementation
details. The only way to avoid such coupling is to verify the end result the code produces
(its observable behavior) and distance tests from implementation details as much as pos-
sible. In other words, tests must focus on the whats, not the hows. So, what exactly is an
implementation detail, and how is it different from an observable behavior?
5.2.1
Observable behavior is not the same as a public API
All production code can be categorized along two dimensions:
Public API vs. private API (where API means application programming interface)
Observable behavior vs. implementation details 
The categories in these dimensions don’t overlap. A method can’t belong to both a pub-
lic and a private API; it’s either one or the other. Similarly, the code is either an internal
implementation detail or part of the system’s observable behavior, but not both.
 Most programming languages provide a simple mechanism to differentiate between
the code base’s public and private APIs. For example, in C#, you can mark any mem-
ber in a class with the private keyword, and that member will be hidden from the cli-
ent code, becoming part of the class’s private API. The same is true for classes: you can
easily make them private by using the private or internal keyword.
 The distinction between observable behavior and internal implementation details
is more nuanced. For a piece of code to be part of the system’s observable behavior, it
has to do one of the following things:
Expose an operation that helps the client achieve one of its goals. An operation is
a method that performs a calculation or incurs a side effect or both.
Expose a state that helps the client achieve one of its goals. State is the current
condition of the system.
Any code that does neither of these two things is an implementation detail.
 Notice that whether the code is observable behavior depends on who its client is
and what the goals of that client are. In order to be a part of observable behavior, the


