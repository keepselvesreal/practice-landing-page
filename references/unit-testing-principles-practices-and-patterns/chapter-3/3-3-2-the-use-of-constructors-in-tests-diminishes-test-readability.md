# 3.3.2 The use of constructors in tests diminishes test readability (pp.52-52)

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


