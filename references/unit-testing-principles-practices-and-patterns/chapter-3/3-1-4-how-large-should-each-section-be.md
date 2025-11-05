# 3.1.4 How large should each section be? (pp.45-47)

---
**Page 45**

45
How to structure a unit test
sections, there’s no exception for integration tests. There are no benefits in branching
within a test. You only gain additional maintenance costs: if statements make the tests
harder to read and understand. 
3.1.4
How large should each section be?
A common question people ask when starting out with the AAA pattern is, how large
should each section be? And what about the teardown section—the section that cleans
up after the test? There are different guidelines regarding the size for each of the test
sections.
THE ARRANGE SECTION IS THE LARGEST
The arrange section is usually the largest of the three. It can be as large as the act and
assert sections combined. But if it becomes significantly larger than that, it’s better to
extract the arrangements either into private methods within the same test class or to a
separate factory class. Two popular patterns can help you reuse the code in the arrange
sections: Object Mother and Test Data Builder. 
WATCH OUT FOR ACT SECTIONS THAT ARE LARGER THAN A SINGLE LINE
The act section is normally just a single line of code. If the act consists of two or more
lines, it could indicate a problem with the SUT’s public API.
 It’s best to express this point with an example, so let’s take one from chapter 2,
which I repeat in the following listing. In this example, the customer makes a pur-
chase from a store.
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
Notice that the act section in this test is a single method call, which is a sign of a well-
designed class’s API. Now compare it to the version in listing 3.3: this act section con-
tains two lines. And that’s a sign of a problem with the SUT: it requires the client to
remember to make the second method call to finish the purchase and thus lacks
encapsulation.
 
Listing 3.2
A single-line act section 


---
**Page 46**

46
CHAPTER 3
The anatomy of a unit test
[Fact]
public void Purchase_succeeds_when_enough_inventory()
{
// Arrange
var store = new Store();
store.AddInventory(Product.Shampoo, 10);
var customer = new Customer();
// Act
bool success = customer.Purchase(store, Product.Shampoo, 5);
store.RemoveInventory(success, Product.Shampoo, 5);
// Assert
Assert.True(success);
Assert.Equal(5, store.GetInventory(Product.Shampoo));
}
Here’s what you can read from listing 3.3’s act section:
In the first line, the customer tries to acquire five units of shampoo from the
store.
In the second line, the inventory is removed from the store. The removal takes
place only if the preceding call to Purchase() returns a success.
The issue with the new version is that it requires two method calls to perform a single
operation. Note that this is not an issue with the test itself. The test still verifies the
same unit of behavior: the process of making a purchase. The issue lies in the API sur-
face of the Customer class. It shouldn’t require the client to make an additional
method call.
 From a business perspective, a successful purchase has two outcomes: the acquisi-
tion of a product by the customer and the reduction of the inventory in the store.
Both of these outcomes must be achieved together, which means there should be a
single public method that does both things. Otherwise, there’s a room for inconsis-
tency if the client code calls the first method but not the second, in which case the cus-
tomer will acquire the product but its available amount won’t be reduced in the store.
 Such an inconsistency is called an invariant violation. The act of protecting your
code against potential inconsistencies is called encapsulation. When an inconsistency
penetrates into the database, it becomes a big problem: now it’s impossible to reset
the state of your application by simply restarting it. You’ll have to deal with the cor-
rupted data in the database and, potentially, contact customers and handle the situation
on a case-by-case basis. Just imagine what would happen if the application generated
confirmation receipts without actually reserving the inventory. It might issue claims
to, and even charge for, more inventory than you could feasibly acquire in the near
future.
 The remedy is to maintain code encapsulation at all times. In the previous exam-
ple, the customer should remove the acquired inventory from the store as part of its
Listing 3.3
A two-line act section 


---
**Page 47**

47
How to structure a unit test
Purchase method and not rely on the client code to do so. When it comes to main-
taining invariants, you should eliminate any potential course of action that could lead
to an invariant violation.
 This guideline of keeping the act section down to a single line holds true for the
vast majority of code that contains business logic, but less so for utility or infrastruc-
ture code. Thus, I won’t say “never do it.” Be sure to examine each such case for a
potential breach in encapsulation, though. 
3.1.5
How many assertions should the assert section hold?
Finally, there’s the assert section. You may have heard about the guideline of having
one assertion per test. It takes root in the premise discussed in the previous chapter:
the premise of targeting the smallest piece of code possible.
 As you already know, this premise is incorrect. A unit in unit testing is a unit of
behavior, not a unit of code. A single unit of behavior can exhibit multiple outcomes,
and it’s fine to evaluate them all in one test.
 Having that said, you need to watch out for assertion sections that grow too large:
it could be a sign of a missing abstraction in the production code. For example,
instead of asserting all properties inside an object returned by the SUT, it may be bet-
ter to define proper equality members in the object’s class. You can then compare the
object to an expected value using a single assertion. 
3.1.6
What about the teardown phase?
Some people also distinguish a fourth section, teardown, which comes after arrange, act,
and assert. For example, you can use this section to remove any files created by the
test, close a database connection, and so on. The teardown is usually represented by a
separate method, which is reused across all tests in the class. Thus, I don’t include this
phase in the AAA pattern.
 Note that most unit tests don’t need teardown. Unit tests don’t talk to out-of-process
dependencies and thus don’t leave side effects that need to be disposed of. That’s a
realm of integration testing. We’ll talk more about how to properly clean up after inte-
gration tests in part 3. 
3.1.7
Differentiating the system under test
The SUT plays a significant role in tests. It provides an entry point for the behavior
you want to invoke in the application. As we discussed in the previous chapter, this
behavior can span across as many as several classes or as little as a single method. But
there can be only one entry point: one class that triggers that behavior.
 Thus it’s important to differentiate the SUT from its dependencies, especially
when there are quite a few of them, so that you don’t need to spend too much time
figuring out who is who in the test. To do that, always name the SUT in tests sut. The
following listing shows how CalculatorTests would look after renaming the Calcu-
lator instance.


