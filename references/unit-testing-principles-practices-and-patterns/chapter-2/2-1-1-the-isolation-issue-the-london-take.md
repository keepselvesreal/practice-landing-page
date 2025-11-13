# 2.1.1 The isolation issue: The London take (pp.21-27)

---
**Page 21**

21
The definition of “unit test”
 Let’s start by defining a unit test, with all due caveats and subtleties. This definition
is the key to the difference between the classical and London schools.
2.1
The definition of “unit test”
There are a lot of definitions of a unit test. Stripped of their non-essential bits, the
definitions all have the following three most important attributes. A unit test is an
automated test that
Verifies a small piece of code (also known as a unit),
Does it quickly,
And does it in an isolated manner.
The first two attributes here are pretty non-controversial. There might be some dis-
pute as to what exactly constitutes a fast unit test because it’s a highly subjective mea-
sure. But overall, it’s not that important. If your test suite’s execution time is good
enough for you, it means your tests are quick enough.
 What people have vastly different opinions about is the third attribute. The isola-
tion issue is the root of the differences between the classical and London schools of
unit testing. As you will see in the next section, all other differences between the two
schools flow naturally from this single disagreement on what exactly isolation means. I
prefer the classical style for the reasons I describe in section 2.3.
2.1.1
The isolation issue: The London take
What does it mean to verify a piece of code—a unit—in an isolated manner? The Lon-
don school describes it as isolating the system under test from its collaborators. It
means if a class has a dependency on another class, or several classes, you need to
replace all such dependencies with test doubles. This way, you can focus on the class
under test exclusively by separating its behavior from any external influence.
 
The classical and London schools of unit testing
The classical approach is also referred to as the Detroit and, sometimes, the classi-
cist approach to unit testing. Probably the most canonical book on the classical
school is the one by Kent Beck: Test-Driven Development: By Example (Addison-Wesley
Professional, 2002).
The London style is sometimes referred to as mockist. Although the term mockist is
widespread, people who adhere to this style of unit testing generally don’t like it, so
I call it the London style throughout this book. The most prominent proponents of this
approach are Steve Freeman and Nat Pryce. I recommend their book, Growing Object-
Oriented Software, Guided by Tests (Addison-Wesley Professional, 2009), as a good
source on this subject.


---
**Page 22**

22
CHAPTER 2
What is a unit test?
DEFINITION
A test double is an object that looks and behaves like its release-
intended counterpart but is actually a simplified version that reduces the
complexity and facilitates testing. This term was introduced by Gerard Mesza-
ros in his book, xUnit Test Patterns: Refactoring Test Code (Addison-Wesley, 2007).
The name itself comes from the notion of a stunt double in movies.
Figure 2.1 shows how the isolation is usually achieved. A unit test that would otherwise
verify the system under test along with all its dependencies now can do that separately
from those dependencies.
One benefit of this approach is that if the test fails, you know for sure which part of
the code base is broken: it’s the system under test. There could be no other suspects,
because all of the class’s neighbors are replaced with the test doubles.
 Another benefit is the ability to split the object graph—the web of communicating
classes solving the same problem. This web may become quite complicated: every class
in it may have several immediate dependencies, each of which relies on dependencies
of their own, and so on. Classes may even introduce circular dependencies, where the
chain of dependency eventually comes back to where it started.
Test double 2
Dependency 1
Dependency 2
System under test
System under test
Test double 1
Figure 2.1
Replacing the dependencies 
of the system under test with test 
doubles allows you to focus on verifying 
the system under test exclusively, as 
well as split the otherwise large 
interconnected object graph.


---
**Page 23**

23
The definition of “unit test”
 Trying to test such an interconnected code base is hard without test doubles. Pretty
much the only choice you are left with is re-creating the full object graph in the test,
which might not be a feasible task if the number of classes in it is too high.
 With test doubles, you can put a stop to this. You can substitute the immediate
dependencies of a class; and, by extension, you don’t have to deal with the dependen-
cies of those dependencies, and so on down the recursion path. You are effectively
breaking up the graph—and that can significantly reduce the amount of preparations
you have to do in a unit test.
 And let’s not forget another small but pleasant side benefit of this approach to
unit test isolation: it allows you to introduce a project-wide guideline of testing only
one class at a time, which establishes a simple structure in the whole unit test suite.
You no longer have to think much about how to cover your code base with tests.
Have a class? Create a corresponding class with unit tests! Figure 2.2 shows how it
usually looks.
Let’s now look at some examples. Since the classical style probably looks more familiar
to most people, I’ll show sample tests written in that style first and then rewrite them
using the London approach.
 Let’s say that we operate an online store. There’s just one simple use case in our
sample application: a customer can purchase a product. When there’s enough inven-
tory in the store, the purchase is deemed to be successful, and the amount of the
product in the store is reduced by the purchase’s amount. If there’s not enough prod-
uct, the purchase is not successful, and nothing happens in the store.
 Listing 2.1 shows two tests verifying that a purchase succeeds only when there’s
enough inventory in the store. The tests are written in the classical style and use the
Class 1
Class 2
Class 3
Unit tests
Production code
Class 1 Tests
Class 2 Tests
Class 3 Tests
Figure 2.2
Isolating the class under test from its dependencies helps establish a simple 
test suite structure: one class with tests for each class in the production code.


---
**Page 24**

24
CHAPTER 2
What is a unit test?
typical three-phase sequence: arrange, act, and assert (AAA for short—I talk more
about this sequence in chapter 3).
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
// Arrange
var store = new Store();
store.AddInventory(Product.Shampoo, 10);
var customer = new Customer();
// Act
bool success = customer.Purchase(store, Product.Shampoo, 5);
// Assert
Assert.True(success);
Assert.Equal(5, store.GetInventory(Product.Shampoo));   
}
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
// Arrange
var store = new Store();
store.AddInventory(Product.Shampoo, 10);
var customer = new Customer();
// Act
bool success = customer.Purchase(store, Product.Shampoo, 15);
// Assert
Assert.False(success);
Assert.Equal(10, store.GetInventory(Product.Shampoo));   
}
public enum Product
{
Shampoo,
Book
}
As you can see, the arrange part is where the tests make ready all dependencies and
the system under test. The call to customer.Purchase() is the act phase, where you
exercise the behavior you want to verify. The assert statements are the verification
stage, where you check to see if the behavior led to the expected results.
 During the arrange phase, the tests put together two kinds of objects: the system
under test (SUT) and one collaborator. In this case, Customer is the SUT and Store is
the collaborator. We need the collaborator for two reasons:
Listing 2.1
Tests written using the classical style of unit testing
Reduces the 
product amount in 
the store by five
The product 
amount in the 
store remains 
unchanged.


---
**Page 25**

25
The definition of “unit test”
To get the method under test to compile, because customer.Purchase() requires
a Store instance as an argument
For the assertion phase, since one of the results of customer.Purchase() is a
potential decrease in the product amount in the store 
Product.Shampoo and the numbers 5 and 15 are constants.
DEFINITION
A method under test (MUT) is a method in the SUT called by the
test. The terms MUT and SUT are often used as synonyms, but normally, MUT
refers to a method while SUT refers to the whole class.
This code is an example of the classical style of unit testing: the test doesn’t replace
the collaborator (the Store class) but rather uses a production-ready instance of it.
One of the natural outcomes of this style is that the test now effectively verifies both
Customer and Store, not just Customer. Any bug in the inner workings of Store that
affects Customer will lead to failing these unit tests, even if Customer still works cor-
rectly. The two classes are not isolated from each other in the tests.
 Let’s now modify the example toward the London style. I’ll take the same tests and
replace the Store instances with test doubles—specifically, mocks.
 I use Moq (https://github.com/moq/moq4) as the mocking framework, but you
can find several equally good alternatives, such as NSubstitute (https://github.com/
nsubstitute/NSubstitute). All object-oriented languages have analogous frameworks.
For instance, in the Java world, you can use Mockito, JMock, or EasyMock.
DEFINITION
A mock is a special kind of test double that allows you to examine
interactions between the system under test and its collaborators.
We’ll get back to the topic of mocks, stubs, and the differences between them in later
chapters. For now, the main thing to remember is that mocks are a subset of test dou-
bles. People often use the terms test double and mock as synonyms, but technically, they
are not (more on this in chapter 5):
Test double is an overarching term that describes all kinds of non-production-
ready, fake dependencies in a test.
Mock is just one kind of such dependencies.
The next listing shows how the tests look after isolating Customer from its collabora-
tor, Store.
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
// Arrange
var storeMock = new Mock<IStore>();
storeMock
Listing 2.2
Tests written using the London style of unit testing


---
**Page 26**

26
CHAPTER 2
What is a unit test?
.Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
.Returns(true);
var customer = new Customer();
// Act
bool success = customer.Purchase(
storeMock.Object, Product.Shampoo, 5);
// Assert
Assert.True(success);
storeMock.Verify(
x => x.RemoveInventory(Product.Shampoo, 5),
Times.Once);
}
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
// Arrange
var storeMock = new Mock<IStore>();
storeMock
.Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
.Returns(false);
var customer = new Customer();
// Act
bool success = customer.Purchase(
storeMock.Object, Product.Shampoo, 5);
// Assert
Assert.False(success);
storeMock.Verify(
x => x.RemoveInventory(Product.Shampoo, 5),
Times.Never);
}
Note how different these tests are from those written in the classical style. In the
arrange phase, the tests no longer instantiate a production-ready instance of Store
but instead create a substitution for it, using Moq’s built-in class Mock<T>.
 Furthermore, instead of modifying the state of Store by adding a shampoo inven-
tory to it, we directly tell the mock how to respond to calls to HasEnoughInventory().
The mock reacts to this request the way the tests need, regardless of the actual state of
Store. In fact, the tests no longer use Store—we have introduced an IStore interface
and are mocking that interface instead of the Store class.
 In chapter 8, I write in detail about working with interfaces. For now, just make a
note that interfaces are required for isolating the system under test from its collabora-
tors. (You can also mock a concrete class, but that’s an anti-pattern; I cover this topic
in chapter 11.)


---
**Page 27**

27
The definition of “unit test”
 The assertion phase has changed too, and that’s where the key difference lies. We
still check the output from customer.Purchase as before, but the way we verify that
the customer did the right thing to the store is different. Previously, we did that by
asserting against the store’s state. Now, we examine the interactions between Customer
and Store: the tests check to see if the customer made the correct call on the store.
We do this by passing the method the customer should call on the store (x.Remove-
Inventory) as well as the number of times it should do that. If the purchases succeeds,
the customer should call this method once (Times.Once). If the purchases fails, the
customer shouldn’t call it at all (Times.Never). 
2.1.2
The isolation issue: The classical take
To reiterate, the London style approaches the isolation requirement by segregating the
piece of code under test from its collaborators with the help of test doubles: specifically,
mocks. Interestingly enough, this point of view also affects your standpoint on what con-
stitutes a small piece of code (a unit). Here are all the attributes of a unit test once again:
A unit test verifies a small piece of code (a unit),
Does it quickly,
And does it in an isolated manner.
In addition to the third attribute leaving room for interpretation, there’s some room
in the possible interpretations of the first attribute as well. How small should a small
piece of code be? As you saw from the previous section, if you adopt the position of
isolating every individual class, then it’s natural to accept that the piece of code under
test should also be a single class, or a method inside that class. It can’t be more than
that due to the way you approach the isolation issue. In some cases, you might test a
couple of classes at once; but in general, you’ll always strive to maintain this guideline
of unit testing one class at a time.
 As I mentioned earlier, there’s another way to interpret the isolation attribute—
the classical way. In the classical approach, it’s not the code that needs to be tested in
an isolated manner. Instead, unit tests themselves should be run in isolation from
each other. That way, you can run the tests in parallel, sequentially, and in any order,
whatever fits you best, and they still won’t affect each other’s outcome.
 Isolating tests from each other means it’s fine to exercise several classes at once as
long as they all reside in the memory and don’t reach out to a shared state, through
which the tests can communicate and affect each other’s execution context. Typical
examples of such a shared state are out-of-process dependencies—the database, the
file system, and so on.
 For instance, one test could create a customer in the database as part of its arrange
phase, and another test would delete it as part of its own arrange phase, before the
first test completes executing. If you run these two tests in parallel, the first test will
fail, not because the production code is broken, but rather because of the interfer-
ence from the second test.


