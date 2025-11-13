# 3.1.3 Avoid if statements in tests (pp.44-45)

---
**Page 44**

44
CHAPTER 3
The anatomy of a unit test
to avoid such a test structure. A single action ensures that your tests remain within the
realm of unit testing, which means they are simple, fast, and easy to understand. If you
see a test containing a sequence of actions and assertions, refactor it. Extract each act
into a test of its own.
 It’s sometimes fine to have multiple act sections in integration tests. As you may
remember from the previous chapter, integration tests can be slow. One way to speed
them up is to group several integration tests together into a single test with multiple
acts and assertions. It’s especially helpful when system states naturally flow from one
another: that is, when an act simultaneously serves as an arrange for the subsequent act.
 But again, this optimization technique is only applicable to integration tests—and
not all of them, but rather those that are already slow and that you don’t want to
become even slower. There’s no need for such an optimization in unit tests or integra-
tion tests that are fast enough. It’s always better to split a multistep unit test into sev-
eral tests. 
3.1.3
Avoid if statements in tests
Similar to multiple occurrences of the arrange, act, and assert sections, you may some-
times encounter a unit test with an if statement. This is also an anti-pattern. A test—
whether a unit test or an integration test—should be a simple sequence of steps with
no branching.
 An if statement indicates that the test verifies too many things at once. Such a test,
therefore, should be split into several tests. But unlike the situation with multiple AAA
Arrange the test
Act
Assert
Act some more
Assert again
Figure 3.1
Multiple arrange, act, and assert sections are a hint that the test verifies 
too many things at once. Such a test needs to be split into several tests to fix the 
problem.


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


