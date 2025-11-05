# 1.3.1 Understanding the code coverage metric (pp.9-10)

---
**Page 9**

9
Using coverage metrics to measure test suite quality
There are different types of coverage metrics, and they’re often used to assess the
quality of a test suite. The common belief is that the higher the coverage number,
the better.
 Unfortunately, it’s not that simple, and coverage metrics, while providing valuable
feedback, can’t be used to effectively measure the quality of a test suite. It’s the same
situation as with the ability to unit test the code: coverage metrics are a good negative
indicator but a bad positive one.
 If a metric shows that there’s too little coverage in your code base—say, only 10%—
that’s a good indication that you are not testing enough. But the reverse isn’t true:
even 100% coverage isn’t a guarantee that you have a good-quality test suite. A test
suite that provides high coverage can still be of poor quality.
 I already touched on why this is so—you can’t just throw random tests at your
project with the hope those tests will improve the situation. But let’s discuss this
problem in detail with respect to the code coverage metric.
1.3.1
Understanding the code coverage metric
The first and most-used coverage metric is code coverage, also known as test coverage; see
figure 1.3. This metric shows the ratio of the number of code lines executed by at least
one test and the total number of lines in the production code base.
Let’s see an example to better understand how this works. Listing 1.1 shows an
IsStringLong method and a test that covers it. The method determines whether a
string provided to it as an input parameter is long (here, the definition of long is any
string with the length greater than five characters). The test exercises the method
using "abc" and checks that this string is not considered long.
public static bool IsStringLong(string input)
{
           
if (input.Length > 5)          
return true;
    
return false;
           
}
          
Listing 1.1
A sample method partially covered by a test
Code coverage (test coverage) =
Total number of lines
Lines of code executed
Figure 1.3
The code coverage (test coverage) metric is 
calculated as the ratio between the number of code lines 
executed by the test suite and the total number of lines in 
the production code base.
Covered 
by the 
test
Not
covered
by the
test


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


