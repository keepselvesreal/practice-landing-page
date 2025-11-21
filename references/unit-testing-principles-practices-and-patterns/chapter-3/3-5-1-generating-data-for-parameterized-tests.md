# 3.5.1 Generating data for parameterized tests (pp.60-62)

---
**Page 60**

60
CHAPTER 3
The anatomy of a unit test
Each fact is now represented by an [InlineData] line rather than a separate test. I
also renamed the test method something more generic: it no longer mentions what
constitutes a valid or invalid date.
 Using parameterized tests, you can significantly reduce the amount of test code,
but this benefit comes at a cost. It’s now hard to figure out what facts the test method
represents. And the more parameters there are, the harder it becomes. As a compro-
mise, you can extract the positive test case into its own test and benefit from the
descriptive naming where it matters the most—in determining what differentiates
valid and invalid delivery dates, as shown in the following listing.
public class DeliveryServiceTests
{
[InlineData(-1)]
[InlineData(0)]
[InlineData(1)]
[Theory]
public void Detects_an_invalid_delivery_date(int daysFromNow)
{
/* ... */
}
[Fact]
public void The_soonest_delivery_date_is_two_days_from_now()
{
/* ... */
}
}
This approach also simplifies the negative test cases, since you can remove the
expected Boolean parameter from the test method. And, of course, you can trans-
form the positive test method into a parameterized test as well, to test multiple dates.
 As you can see, there’s a trade-off between the amount of test code and the read-
ability of that code. As a rule of thumb, keep both positive and negative test cases
together in a single method only when it’s self-evident from the input parameters
which case stands for what. Otherwise, extract the positive test cases. And if the behav-
ior is too complicated, don’t use the parameterized tests at all. Represent each nega-
tive and positive test case with its own test method.
3.5.1
Generating data for parameterized tests
There are some caveats in using parameterized tests (at least, in .NET) that you need
to be aware of. Notice that in listing 3.11, I used the daysFromNow parameter as an
input to the test method. Why not the actual date and time, you might ask? Unfortu-
nately, the following code won’t work:
[InlineData(DateTime.Now.AddDays(-1), false)]
[InlineData(DateTime.Now, false)]
Listing 3.12
Two tests verifying the positive and negative scenarios


---
**Page 61**

61
Refactoring to parameterized tests
[InlineData(DateTime.Now.AddDays(1), false)]
[InlineData(DateTime.Now.AddDays(2), true)]
[Theory]
public void Can_detect_an_invalid_delivery_date(
DateTime deliveryDate,
bool expected)
{
DeliveryService sut = new DeliveryService();
Delivery delivery = new Delivery
{
Date = deliveryDate
};
bool isValid = sut.IsDeliveryValid(delivery);
Assert.Equal(expected, isValid);
}
In C#, the content of all attributes is evaluated at compile time. You have to use only
those values that the compiler can understand, which are as follows:
Constants
Literals

typeof() expressions
The call to DateTime.Now relies on the .NET runtime and thus is not allowed.
 There is a way to overcome this problem. xUnit has another feature that you can
use to generate custom data to feed into the test method: [MemberData]. The next list-
ing shows how we can rewrite the previous test using this feature.
[Theory]
[MemberData(nameof(Data))]
public void Can_detect_an_invalid_delivery_date(
DateTime deliveryDate,
bool expected)
{
/* ... */
}
public static List<object[]> Data()
{
return new List<object[]>
{
new object[] { DateTime.Now.AddDays(-1), false },
new object[] { DateTime.Now, false },
new object[] { DateTime.Now.AddDays(1), false },
new object[] { DateTime.Now.AddDays(2), true }
};
}
Listing 3.13
Generating complex data for the parameterized test 


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


