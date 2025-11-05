# 3.4.2 Example: Renaming a test toward the guidelines (pp.56-58)

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


---
**Page 57**

57
Naming a unit test
bool isValid = sut.IsDeliveryValid(delivery);
Assert.False(isValid);
}
This test checks that DeliveryService properly identifies a delivery with an incorrect
date as invalid. How would you rewrite the test’s name in plain English? The following
would be a good first try:
public void Delivery_with_invalid_date_should_be_considered_invalid()
Notice two things in the new version:
The name now makes sense to a non-programmer, which means programmers
will have an easier time understanding it, too.
The name of the SUT’s method—IsDeliveryValid—is no longer part of the
test’s name.
The second point is a natural consequence of rewriting the test’s name in plain
English and thus can be easily overlooked. However, this consequence is important
and can be elevated into a guideline of its own.
But let’s get back to the example. The new version of the test’s name is a good start,
but it can be improved further. What does it mean for a delivery date to be invalid,
exactly? From the test in listing 3.10, we can see that an invalid date is any date in
the past. This makes sense—you should only be allowed to choose a delivery date
in the future.
 So let’s be specific and reflect this knowledge in the test’s name:
public void Delivery_with_past_date_should_be_considered_invalid()
Method under test in the test’s name
Don’t include the name of the SUT’s method in the test’s name.
Remember, you don’t test code, you test application behavior. Therefore, it doesn’t
matter what the name of the method under test is. As I mentioned previously, the
SUT is just an entry point: a means to invoke a behavior. You can decide to rename
the method under test to, say, IsDeliveryCorrect, and it will have no effect on the
SUT’s behavior. On the other hand, if you follow the original naming convention, you’ll
have to rename the test. This once again shows that targeting code instead of behav-
ior couples tests to that code’s implementation details, which negatively affects the
test suite’s maintainability. More on this issue in chapter 5.
The only exception to this guideline is when you work on utility code. Such code
doesn’t contain business logic—its behavior doesn’t go much beyond simple auxil-
iary functionality and thus doesn’t mean anything to business people. It’s fine to use
the SUT’s method names there.


---
**Page 58**

58
CHAPTER 3
The anatomy of a unit test
This is better but still not ideal. It’s too verbose. We can get rid of the word consid-
ered without any loss of meaning:
public void Delivery_with_past_date_should_be_invalid()
The wording should be is another common anti-pattern. Earlier in this chapter, I men-
tioned that a test is a single, atomic fact about a unit of behavior. There’s no place for
a wish or a desire when stating a fact. Name the test accordingly—replace should be
with is:
public void Delivery_with_past_date_is_invalid()
And finally, there’s no need to avoid basic English grammar. Articles help the test read
flawlessly. Add the article a to the test’s name:
public void Delivery_with_a_past_date_is_invalid()
There you go. This final version is a straight-to-the-point statement of a fact, which
itself describes one of the aspects of the application behavior under test: in this partic-
ular case, the aspect of determining whether a delivery can be done. 
3.5
Refactoring to parameterized tests
One test usually is not enough to fully describe a unit of behavior. Such a unit normally
consists of multiple components, each of which should be captured with its own test. If
the behavior is complex enough, the number of tests describing it can grow dramatically
and may become unmanageable. Luckily, most unit testing frameworks provide func-
tionality that allows you to group similar tests using parameterized tests (see figure 3.2).
Behavior N
…
…
…
…
Behavior 2
Behavior 1
Can be grouped
Fact N
Fact 2
Fact 1
Application
Figure 3.2
A typical application 
exhibits multiple behaviors. The 
greater the complexity of the 
behavior, the more facts are required 
to fully describe it. Each fact is 
represented by a test. Similar facts 
can be grouped into a single test 
method using parameterized tests.


