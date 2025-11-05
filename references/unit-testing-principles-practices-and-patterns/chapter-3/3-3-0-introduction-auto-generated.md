# 3.3.0 Introduction [auto-generated] (pp.50-52)

---
**Page 50**

50
CHAPTER 3
The anatomy of a unit test
public void Dispose()   
{
   
_sut.CleanUp();
   
}
   
}
As you can see, the xUnit authors took significant steps toward simplifying the
framework. A lot of notions that previously required additional configuration (like
[TestFixture] or [SetUp] attributes) now rely on conventions or built-in language
constructs.
 I particularly like the [Fact] attribute, specifically because it’s called Fact and not
Test. It emphasizes the rule of thumb I mentioned in the previous chapter: each test
should tell a story. This story is an individual, atomic scenario or fact about the problem
domain, and the passing test is a proof that this scenario or fact holds true. If the test
fails, it means either the story is no longer valid and you need to rewrite it, or the sys-
tem itself has to be fixed.
 I encourage you to adopt this way of thinking when you write unit tests. Your tests
shouldn’t be a dull enumeration of what the production code does. Rather, they should
provide a higher-level description of the application’s behavior. Ideally, this description
should be meaningful not just to programmers but also to business people. 
3.3
Reusing test fixtures between tests
It’s important to know how and when to reuse code between tests. Reusing code
between arrange sections is a good way to shorten and simplify your tests, and this sec-
tion shows how to do that properly.
 I mentioned earlier that often, fixture arrangements take up too much space. It
makes sense to extract these arrangements into separate methods or classes that you
then reuse between tests. There are two ways you can perform such reuse, but only
one of them is beneficial; the other leads to increased maintenance costs.
Test fixture
The term test fixture has two common meanings:
1
A test fixture is an object the test runs against. This object can be a regular
dependency—an argument that is passed to the SUT. It can also be data in
the database or a file on the hard disk. Such an object needs to remain in a
known, fixed state before each test run, so it produces the same result.
Hence the word fixture.
2
The other definition comes from the NUnit testing framework. In NUnit, Test-
Fixture is an attribute that marks a class containing tests.
I use the first definition throughout this book.
Called after 
each test in 
the class


---
**Page 51**

51
Reusing test fixtures between tests
The first—incorrect—way to reuse test fixtures is to initialize them in the test’s con-
structor (or the method marked with a [SetUp] attribute if you are using NUnit), as
shown next.
public class CustomerTests
{
private readonly Store _store;       
private readonly Customer _sut;
public CustomerTests()
     
{
   
_store = new Store();
   
_store.AddInventory(Product.Shampoo, 10);   
_sut = new Customer();
   
}
   
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
bool success = _sut.Purchase(_store, Product.Shampoo, 5);
Assert.True(success);
Assert.Equal(5, _store.GetInventory(Product.Shampoo));
}
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
bool success = _sut.Purchase(_store, Product.Shampoo, 15);
Assert.False(success);
Assert.Equal(10, _store.GetInventory(Product.Shampoo));
}
}
The two tests in listing 3.7 have common configuration logic. In fact, their arrange sec-
tions are the same and thus can be fully extracted into CustomerTests’s constructor—
which is precisely what I did here. The tests themselves no longer contain arrangements.
 With this approach, you can significantly reduce the amount of test code—you can
get rid of most or even all test fixture configurations in tests. But this technique has
two significant drawbacks:
It introduces high coupling between tests.
It diminishes test readability.
Let’s discuss these drawbacks in more detail.
Listing 3.7
Extracting the initialization code into the test constructor
Common test 
fixture
Runs before 
each test in 
the class


---
**Page 52**

52
CHAPTER 3
The anatomy of a unit test
3.3.1
High coupling between tests is an anti-pattern
In the new version, shown in listing 3.7, all tests are coupled to each other: a modifica-
tion of one test’s arrangement logic will affect all tests in the class. For example, chang-
ing this line
_store.AddInventory(Product.Shampoo, 10);
to this
_store.AddInventory(Product.Shampoo, 15);
would invalidate the assumption the tests make about the store’s initial state and there-
fore would lead to unnecessary test failures.
 That’s a violation of an important guideline: a modification of one test should not affect
other tests. This guideline is similar to what we discussed in chapter 2—that tests should
run in isolation from each other. It’s not the same, though. Here, we are talking about
independent modification of tests, not independent execution. Both are important
attributes of a well-designed test.
 To follow this guideline, you need to avoid introducing shared state in test classes.
These two private fields are examples of such a shared state:
private readonly Store _store;
private readonly Customer _sut;
3.3.2
The use of constructors in tests diminishes test readability
The other drawback to extracting the arrangement code into the constructor is
diminished test readability. You no longer see the full picture just by looking at the
test itself. You have to examine different places in the class to understand what the test
method does.
 Even if there’s not much arrangement logic—say, only instantiation of the fixtures—
you are still better off moving it directly to the test method. Otherwise, you’ll wonder
if it’s really just instantiation or something else being configured there, too. A self-con-
tained test doesn’t leave you with such uncertainties. 
3.3.3
A better way to reuse test fixtures
The use of the constructor is not the best approach when it comes to reusing test fix-
tures. The second way—the beneficial one—is to introduce private factory methods in
the test class, as shown in the following listing.
public class CustomerTests
{
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
Listing 3.8
Extracting the common initialization code into private factory methods


