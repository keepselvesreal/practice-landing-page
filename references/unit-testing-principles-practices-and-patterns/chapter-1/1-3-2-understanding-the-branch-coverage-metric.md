# 1.3.2 Understanding the branch coverage metric (pp.10-12)

---
**Page 10**

10
CHAPTER 1
The goal of unit testing
public void Test()
{
bool result = IsStringLong("abc");
Assert.Equal(false, result);
}
It’s easy to calculate the code coverage here. The total number of lines in the method
is five (curly braces count, too). The number of lines executed by the test is four—the
test goes through all the code lines except for the return true; statement. This gives
us 4/5 = 0.8 = 80% code coverage.
 Now, what if I refactor the method and inline the unnecessary if statement, like this?
public static bool IsStringLong(string input)
{
return input.Length > 5;
}
public void Test()
{
bool result = IsStringLong("abc");
Assert.Equal(false, result);
}
Does the code coverage number change? Yes, it does. Because the test now exercises
all three lines of code (the return statement plus two curly braces), the code coverage
increases to 100%.
 But did I improve the test suite with this refactoring? Of course not. I just shuffled the
code inside the method. The test still verifies the same number of possible outcomes.
 This simple example shows how easy it is to game the coverage numbers. The more
compact your code is, the better the test coverage metric becomes, because it only
accounts for the raw line numbers. At the same time, squashing more code into less
space doesn’t (and shouldn’t) change the value of the test suite or the maintainability
of the underlying code base. 
1.3.2
Understanding the branch coverage metric
Another coverage metric is called branch coverage. Branch coverage provides more pre-
cise results than code coverage because it helps cope with code coverage’s shortcom-
ings. Instead of using the raw number of code lines, this metric focuses on control
structures, such as if and switch statements. It shows how many of such control struc-
tures are traversed by at least one test in the suite, as shown in figure 1.4.
Branch coverage = Total number of branches
Branches traversed
Figure 1.4
The branch metric is calculated as the ratio of the 
number of code branches exercised by the test suite and the 
total number of branches in the production code base.


---
**Page 11**

11
Using coverage metrics to measure test suite quality
To calculate the branch coverage metric, you need to sum up all possible branches in
your code base and see how many of them are visited by tests. Let’s take our previous
example again:
public static bool IsStringLong(string input)
{
return input.Length > 5;
}
public void Test()
{
bool result = IsStringLong("abc");
Assert.Equal(false, result);
}
There are two branches in the IsStringLong method: one for the situation when the
length of the string argument is greater than five characters, and the other one when
it’s not. The test covers only one of these branches, so the branch coverage metric is
1/2 = 0.5 = 50%. And it doesn’t matter how we represent the code under test—
whether we use an if statement as before or use the shorter notation. The branch cov-
erage metric only accounts for the number of branches; it doesn’t take into consider-
ation how many lines of code it took to implement those branches.
 Figure 1.5 shows a helpful way to visualize this metric. You can represent all pos-
sible paths the code under test can take as a graph and see how many of them have
been traversed. IsStringLong has two such paths, and the test exercises only one
of them.
Start
Length <= 5
End
Length > 5
Figure 1.5
The method IsStringLong represented as a graph of possible 
code paths. Test covers only one of the two code paths, thus providing 50% 
branch coverage.


---
**Page 12**

12
CHAPTER 1
The goal of unit testing
1.3.3
Problems with coverage metrics
Although the branch coverage metric yields better results than code coverage, you still
can’t rely on either of them to determine the quality of your test suite, for two reasons:
You can’t guarantee that the test verifies all the possible outcomes of the system
under test.
No coverage metric can take into account code paths in external libraries.
Let’s look more closely at each of these reasons.
YOU CAN’T GUARANTEE THAT THE TEST VERIFIES ALL THE POSSIBLE OUTCOMES
For the code paths to be actually tested and not just exercised, your unit tests must
have appropriate assertions. In other words, you need to check that the outcome the
system under test produces is the exact outcome you expect it to produce. Moreover,
this outcome may have several components; and for the coverage metrics to be mean-
ingful, you need to verify all of them.
 The next listing shows another version of the IsStringLong method. It records the
last result into a public WasLastStringLong property.
public static bool WasLastStringLong { get; private set; }
public static bool IsStringLong(string input)
{
bool result = input.Length > 5;
WasLastStringLong = result;         
return result;
     
}
public void Test()
{
bool result = IsStringLong("abc");
Assert.Equal(false, result);   
}
The IsStringLong method now has two outcomes: an explicit one, which is encoded
by the return value; and an implicit one, which is the new value of the property. And
in spite of not verifying the second, implicit outcome, the coverage metrics would still
show the same results: 100% for the code coverage and 50% for the branch coverage.
As you can see, the coverage metrics don’t guarantee that the underlying code is
tested, only that it has been executed at some point.
 An extreme version of this situation with partially tested outcomes is assertion-free
testing, which is when you write tests that don’t have any assertion statements in them
whatsoever. Here’s an example of assertion-free testing.
 
 
Listing 1.2
Version of IsStringLong that records the last result
First 
outcome
Second 
outcome
The test verifies only 
the second outcome.


