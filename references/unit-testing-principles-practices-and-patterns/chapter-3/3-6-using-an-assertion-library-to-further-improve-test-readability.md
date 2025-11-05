# 3.6 Using an assertion library to further improve test readability (pp.62-63)

---
**Page 62**

62
CHAPTER 3
The anatomy of a unit test
MemberData accepts the name of a static method that generates a collection of input
data (the compiler translates nameof(Data) into a "Data" literal). Each element of
the collection is itself a collection that is mapped into the two input parameters:
deliveryDate and expected. With this feature, you can overcome the compiler’s
restrictions and use parameters of any type in the parameterized tests. 
3.6
Using an assertion library to further improve 
test readability
One more thing you can do to improve test readability is to use an assertion library. I
personally prefer Fluent Assertions (https://fluentassertions.com), but .NET has sev-
eral competing libraries in this area.
 The main benefit of using an assertion library is how you can restructure the asser-
tions so that they are more readable. Here’s one of our earlier tests:
[Fact]
public void Sum_of_two_numbers()
{
var sut = new Calculator();
double result = sut.Sum(10, 20);
Assert.Equal(30, result);
}
Now compare it to the following, which uses a fluent assertion:
[Fact]
public void Sum_of_two_numbers()
{
var sut = new Calculator();
double result = sut.Sum(10, 20);
result.Should().Be(30);
}
The assertion from the second test reads as plain English, which is exactly how you
want all your code to read. We as humans prefer to absorb information in the form of
stories. All stories adhere to this specific pattern:
[Subject] [action] [object].
For example,
Bob opened the door.
Here, Bob is a subject, opened is an action, and the door is an object. The same rule
applies to code. result.Should().Be(30) reads better than Assert.Equal(30,


---
**Page 63**

63
Summary
result) precisely because it follows the story pattern. It’s a simple story in which
result is a subject, should be is an action, and 30 is an object.
NOTE
The paradigm of object-oriented programming (OOP) has become a
success partly because of this readability benefit. With OOP, you, too, can
structure the code in a way that reads like a story.
The Fluent Assertions library also provides numerous helper methods to assert against
numbers, strings, collections, dates and times, and much more. The only drawback is
that such a library is an additional dependency you may not want to introduce to your
project (although it’s for development only and won’t be shipped to production). 
Summary
All unit tests should follow the AAA pattern: arrange, act, assert. If a test has mul-
tiple arrange, act, or assert sections, that’s a sign that the test verifies multiple
units of behavior at once. If this test is meant to be a unit test, split it into several
tests—one per each action.
More than one line in the act section is a sign of a problem with the SUT’s API.
It requires the client to remember to always perform these actions together,
which can potentially lead to inconsistencies. Such inconsistencies are called
invariant violations. The act of protecting your code against potential invariant
violations is called encapsulation.
Distinguish the SUT in tests by naming it sut. Differentiate the three test sec-
tions either by putting Arrange, Act, and Assert comments before them or by
introducing empty lines between these sections.
Reuse test fixture initialization code by introducing factory methods, not by
putting this initialization code to the constructor. Such reuse helps maintain a
high degree of decoupling between tests and also provides better readability.
Don’t use a rigid test naming policy. Name each test as if you were describing
the scenario in it to a non-programmer who is familiar with the problem
domain. Separate words in the test name by underscores, and don’t include the
name of the method under test in the test name.
Parameterized tests help reduce the amount of code needed for similar tests.
The drawback is that the test names become less readable as you make them
more generic.
Assertion libraries help you further improve test readability by restructuring the
word order in assertions so that they read like plain English. 


