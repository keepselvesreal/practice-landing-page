# 3.5.0 Introduction [auto-generated] (pp.58-60)

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


---
**Page 59**

59
Refactoring to parameterized tests
In this section, I’ll first show each such behavior component described by a separate test
and then demonstrate how these tests can be grouped together.
 Let’s say that our delivery functionality works in such a way that the soonest
allowed delivery date is two days from now. Clearly, the one test we have isn’t enough.
In addition to the test that checks for a past delivery date, we’ll also need tests that
check for today’s date, tomorrow’s date, and the date after that.
 The existing test is called Delivery_with_a_past_date_is_invalid. We could
add three more:
public void Delivery_for_today_is_invalid()
public void Delivery_for_tomorrow_is_invalid()
public void The_soonest_delivery_date_is_two_days_from_now()
But that would result in four test methods, with the only difference between them
being the delivery date.
 A better approach is to group these tests into one in order to reduce the amount of
test code. xUnit (like most other test frameworks) has a feature called parameterized
tests that allows you to do exactly that. The next listing shows how such grouping looks.
Each InlineData attribute represents a separate fact about the system; it’s a test case
in its own right.
public class DeliveryServiceTests
{
[InlineData(-1, false)]   
[InlineData(0, false)]   
[InlineData(1, false)]   
[InlineData(2, true)]
  
[Theory]
public void Can_detect_an_invalid_delivery_date(
int daysFromNow,       
bool expected)
      
{
DeliveryService sut = new DeliveryService();
DateTime deliveryDate = DateTime.Now
.AddDays(daysFromNow);                   
Delivery delivery = new Delivery
{
Date = deliveryDate
};
bool isValid = sut.IsDeliveryValid(delivery);
Assert.Equal(expected, isValid);              
}
}
TIP
Notice the use of the [Theory] attribute instead of [Fact]. A theory is a
bunch of facts about the behavior.
Listing 3.11
A test that encompasses several facts
The InlineData attribute sends a 
set of input values to the test 
method. Each line represents a 
separate fact about the behavior.
Parameters to which the attributes 
attach the input values
Uses the 
parameters


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


