# 3.4.1 Unit test naming guidelines (pp.56-56)

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


