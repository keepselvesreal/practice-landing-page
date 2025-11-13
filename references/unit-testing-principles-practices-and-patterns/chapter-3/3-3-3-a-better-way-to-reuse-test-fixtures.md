# 3.3.3 A better way to reuse test fixtures (pp.52-54)

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


---
**Page 53**

53
Reusing test fixtures between tests
Store store = CreateStoreWithInventory(Product.Shampoo, 10);
Customer sut = CreateCustomer();
bool success = sut.Purchase(store, Product.Shampoo, 5);
Assert.True(success);
Assert.Equal(5, store.GetInventory(Product.Shampoo));
}
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
Store store = CreateStoreWithInventory(Product.Shampoo, 10);
Customer sut = CreateCustomer();
bool success = sut.Purchase(store, Product.Shampoo, 15);
Assert.False(success);
Assert.Equal(10, store.GetInventory(Product.Shampoo));
}
private Store CreateStoreWithInventory(
Product product, int quantity)
{
Store store = new Store();
store.AddInventory(product, quantity);
return store;
}
private static Customer CreateCustomer()
{
return new Customer();
}
}
By extracting the common initialization code into private factory methods, you can
also shorten the test code, but at the same time keep the full context of what’s going
on in the tests. Moreover, the private methods don’t couple tests to each other as long
as you make them generic enough. That is, allow the tests to specify how they want the
fixtures to be created.
 Look at this line, for example:
Store store = CreateStoreWithInventory(Product.Shampoo, 10);
The test explicitly states that it wants the factory method to add 10 units of shampoo
to the store. This is both highly readable and reusable. It’s readable because you don’t
need to examine the internals of the factory method to understand the attributes of
the created store. It’s reusable because you can use this method in other tests, too.
 Note that in this particular example, there’s no need to introduce factory meth-
ods, as the arrangement logic is quite simple. View it merely as a demonstration.


---
**Page 54**

54
CHAPTER 3
The anatomy of a unit test
 There’s one exception to this rule of reusing test fixtures. You can instantiate a fix-
ture in the constructor if it’s used by all or almost all tests. This is often the case for
integration tests that work with a database. All such tests require a database connec-
tion, which you can initialize once and then reuse everywhere. But even then, it would
make more sense to introduce a base class and initialize the database connection in
that class’s constructor, not in individual test classes. See the following listing for an
example of common initialization code in a base class.
public class CustomerTests : IntegrationTests
{
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
/* use _database here */
}
}
public abstract class IntegrationTests : IDisposable
{
protected readonly Database _database;
protected IntegrationTests()
{
_database = new Database();
}
public void Dispose()
{
_database.Dispose();
}
}
Notice how CustomerTests remains constructor-less. It gets access to the _database
instance by inheriting from the IntegrationTests base class. 
3.4
Naming a unit test
It’s important to give expressive names to your tests. Proper naming helps you under-
stand what the test verifies and how the underlying system behaves.
 So, how should you name a unit test? I’ve seen and tried a lot of naming conven-
tions over the past decade. One of the most prominent, and probably least helpful, is
the following convention:
[MethodUnderTest]_[Scenario]_[ExpectedResult]
where

MethodUnderTest is the name of the method you are testing.

Scenario is the condition under which you test the method.
Listing 3.9
Common initialization code in a base class


