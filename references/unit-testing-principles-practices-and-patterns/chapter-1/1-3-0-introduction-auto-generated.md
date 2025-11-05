# 1.3.0 Introduction [auto-generated] (pp.8-9)

---
**Page 8**

8
CHAPTER 1
The goal of unit testing
Remember, not all tests are created equal. Some of them are valuable and contribute a lot
to overall software quality. Others don’t. They raise false alarms, don’t help you catch
regression errors, and are slow and difficult to maintain. It’s easy to fall into the trap
of writing unit tests for the sake of unit testing without a clear picture of whether it
helps the project.
 You can’t achieve the goal of unit testing by just throwing more tests at the project.
You need to consider both the test’s value and its upkeep cost. The cost component is
determined by the amount of time spent on various activities:
Refactoring the test when you refactor the underlying code
Running the test on each code change
Dealing with false alarms raised by the test
Spending time reading the test when you’re trying to understand how the
underlying code behaves
It’s easy to create tests whose net value is close to zero or even is negative due to high
maintenance costs. To enable sustainable project growth, you have to exclusively
focus on high-quality tests—those are the only type of tests that are worth keeping in
the test suite.
It’s crucial to learn how to differentiate between good and bad unit tests. I cover this
topic in chapter 4. 
1.3
Using coverage metrics to measure test suite quality
In this section, I talk about the two most popular coverage metrics—code coverage
and branch coverage—how to calculate them, how they’re used, and problems with
them. I’ll show why it’s detrimental for programmers to aim at a particular coverage
number and why you can’t just rely on coverage metrics to determine the quality of
your test suite.
DEFINITION
A coverage metric shows how much source code a test suite exe-
cutes, from none to 100%.
Production code vs. test code 
People often think production code and test code are different. Tests are assumed
to be an addition to production code and have no cost of ownership. By extension,
people often believe that the more tests, the better. This isn’t the case. Code is a
liability, not an asset. The more code you introduce, the more you extend the surface
area for potential bugs in your software, and the higher the project’s upkeep cost. It’s
always better to solve problems with as little code as possible.
Tests are code, too. You should view them as the part of your code base that aims at
solving a particular problem: ensuring the application’s correctness. Unit tests, just
like any other code, are also vulnerable to bugs and require maintenance.


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


