# 3.4.0 Introduction [auto-generated] (pp.54-56)

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


---
**Page 55**

55
Naming a unit test

ExpectedResult is what you expect the method under test to do in the current
scenario.
It’s unhelpful specifically because it encourages you to focus on implementation
details instead of the behavior.
 Simple phrases in plain English do a much better job: they are more expressive
and don’t box you in a rigid naming structure. With simple phrases, you can describe
the system behavior in a way that’s meaningful to a customer or a domain expert. To
give you an example of a test titled in plain English, here’s the test from listing 3.5
once again:
public class CalculatorTests
{
[Fact]
public void Sum_of_two_numbers()
{
double first = 10;
double second = 20;
var sut = new Calculator();
double result = sut.Sum(first, second);
Assert.Equal(30, result);
}
}
How could the test’s name (Sum_of_two_numbers) be rewritten using the [MethodUnder-
Test]_[Scenario]_[ExpectedResult] convention? Probably something like this:
public void Sum_TwoNumbers_ReturnsSum()
The method under test is Sum, the scenario includes two numbers, and the expected
result is a sum of those two numbers. The new name looks logical to a programmer’s
eye, but does it really help with test readability? Not at all. It’s Greek to an unin-
formed person. Think about it: Why does Sum appear twice in the name of the test?
And what is this Returns phrasing all about? Where is the sum returned to? You
can’t know.
 Some might argue that it doesn’t really matter what a non-programmer would
think of this name. After all, unit tests are written by programmers for programmers,
not domain experts. And programmers are good at deciphering cryptic names—it’s
their job!
 This is true, but only to a degree. Cryptic names impose a cognitive tax on every-
one, programmers or not. They require additional brain capacity to figure out what
exactly the test verifies and how it relates to business requirements. This may not seem
like much, but the mental burden adds up over time. It slowly but surely increases the
maintenance cost for the entire test suite. It’s especially noticeable if you return to the
test after you’ve forgotten about the feature’s specifics, or try to understand a test


---
**Page 56**

56
CHAPTER 3
The anatomy of a unit test
written by a colleague. Reading someone else’s code is already difficult enough—any
help understanding it is of considerable use.
 Here are the two versions again:
public void Sum_of_two_numbers()
public void Sum_TwoNumbers_ReturnsSum()
The initial name written in plain English is much simpler to read. It is a down-to-earth
description of the behavior under test.
3.4.1
Unit test naming guidelines
Adhere to the following guidelines to write expressive, easily readable test names:
Don’t follow a rigid naming policy. You simply can’t fit a high-level description of a
complex behavior into the narrow box of such a policy. Allow freedom of
expression.
Name the test as if you were describing the scenario to a non-programmer who is familiar
with the problem domain. A domain expert or a business analyst is a good example.
Separate words with underscores. Doing so helps improve readability, especially in
long names.
Notice that I didn’t use underscores when naming the test class, CalculatorTests.
Normally, the names of classes are not as long, so they read fine without underscores.
 Also notice that although I use the pattern [ClassName]Tests when naming test
classes, it doesn’t mean the tests are limited to verifying only that class. Remember, the
unit in unit testing is a unit of behavior, not a class. This unit can span across one or sev-
eral classes; the actual size is irrelevant. Still, you have to start somewhere. View the
class in [ClassName]Tests as just that: an entry point, an API, using which you can
verify a unit of behavior. 
3.4.2
Example: Renaming a test toward the guidelines
Let’s take a test as an example and try to gradually improve its name using the guide-
lines I just outlined. In the following listing, you can see a test verifying that a delivery
with a past date is invalid. The test’s name is written using the rigid naming policy that
doesn’t help with the test readability.
[Fact]
public void IsDeliveryValid_InvalidDate_ReturnsFalse()
{
DeliveryService sut = new DeliveryService();
DateTime pastDate = DateTime.Now.AddDays(-1);
Delivery delivery = new Delivery
{
Date = pastDate
};
Listing 3.10
A test named using the rigid naming policy


