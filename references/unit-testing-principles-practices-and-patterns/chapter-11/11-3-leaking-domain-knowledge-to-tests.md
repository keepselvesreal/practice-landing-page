# 11.3 Leaking domain knowledge to tests (pp.264-266)

---
**Page 264**

264
CHAPTER 11
Unit testing anti-patterns
Regular,
Preferred
}
This example shows a Customer class. Each customer is created in the Regular status
and then can be promoted to Preferred, at which point they get a 5% discount on
everything.
 How would you test the Promote() method? This method’s side effect is a change
of the _status field, but the field itself is private and thus not available in tests. A
tempting solution would be to make this field public. After all, isn’t the change of sta-
tus the ultimate goal of calling Promote()?
 That would be an anti-pattern, however. Remember, your tests should interact with the
system under test (SUT) exactly the same way as the production code and shouldn’t have any spe-
cial privileges. In listing 11.4, the _status field is hidden from the production code and
thus is not part of the SUT’s observable behavior. Exposing that field would result in
coupling tests to implementation details. How to test Promote(), then?
 What you should do, instead, is look at how the production code uses this class. In
this particular example, the production code doesn’t care about the customer’s status;
otherwise, that field would be public. The only information the production code does
care about is the discount the customer gets after the promotion. And so that’s what
you need to verify in tests. You need to check that
A newly created customer has no discount.
Once the customer is promoted, the discount becomes 5%.
Later, if the production code starts using the customer status field, you’d be able to
couple to that field in tests too, because it would officially become part of the SUT’s
observable behavior.
NOTE
Widening the public API surface for the sake of testability is a bad practice. 
11.3
Leaking domain knowledge to tests
Leaking domain knowledge to tests is another quite common anti-pattern. It usually
takes place in tests that cover complex algorithms. Let’s take the following (admit-
tedly, not that complex) calculation algorithm as an example:
public static class Calculator
{
public static int Add(int value1, int value2)
{
return value1 + value2;
}
}
This listing shows an incorrect way to test it.


---
**Page 265**

265
Leaking domain knowledge to tests
public class CalculatorTests
{
[Fact]
public void Adding_two_numbers()
{
int value1 = 1;
int value2 = 3;
int expected = value1 + value2;      
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
You could also parameterize the test to throw in a couple more test cases at almost no
additional cost.
public class CalculatorTests
{
[Theory]
[InlineData(1, 3)]
[InlineData(11, 33)]
[InlineData(100, 500)]
public void Adding_two_numbers(int value1, int value2)
{
int expected = value1 + value2;    
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
Listings 11.5 and 11.6 look fine at first, but they are, in fact, examples of the anti-pattern:
these tests duplicate the algorithm implementation from the production code. Of
course, it might not seem like a big deal. After all, it’s just one line. But that’s only
because the example is rather simplified. I’ve seen tests that covered complex algo-
rithms and did nothing but reimplement those algorithms in the arrange part. They
were basically a copy-paste from the production code.
 These tests are another example of coupling to implementation details. They score
almost zero on the metric of resistance to refactoring and are worthless as a result.
Such tests don’t have a chance of differentiating legitimate failures from false posi-
tives. Should a change in the algorithm make those tests fail, the team would most
likely just copy the new version of that algorithm to the test without even trying to
Listing 11.5
Leaking algorithm implementation
Listing 11.6
A parameterized version of the same test
The leakage
The leakage


---
**Page 266**

266
CHAPTER 11
Unit testing anti-patterns
identify the root cause (which is understandable, because the tests were a mere dupli-
cation of the algorithm in the first place).
 How to test the algorithm properly, then? Don’t imply any specific implementation when
writing tests. Instead of duplicating the algorithm, hard-code its results into the test, as
shown in the following listing.
public class CalculatorTests
{
[Theory]
[InlineData(1, 3, 4)]
[InlineData(11, 33, 44)]
[InlineData(100, 500, 600)]
public void Adding_two_numbers(int value1, int value2, int expected)
{
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
It can seem counterintuitive at first, but hardcoding the expected result is a good
practice when it comes to unit testing. The important part with the hardcoded values
is to precalculate them using something other than the SUT, ideally with the help of a
domain expert. Of course, that’s only if the algorithm is complex enough (we are all
experts at summing up two numbers). Alternatively, if you refactor a legacy applica-
tion, you can have the legacy code produce those results and then use them as expected
values in tests. 
11.4
Code pollution
The next anti-pattern is code pollution.
DEFINITION
Code pollution is adding production code that’s only needed for
testing.
Code pollution often takes the form of various types of switches. Let’s take a logger as
an example.
public class Logger
{
private readonly bool _isTestEnvironment;
public Logger(bool isTestEnvironment)    
{
_isTestEnvironment = isTestEnvironment;
}
Listing 11.7
Test with no domain knowledge
Listing 11.8
Logger with a Boolean switch 
The switch


