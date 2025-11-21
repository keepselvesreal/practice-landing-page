# 1.3.3 Problems with coverage metrics (pp.12-15)

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


---
**Page 13**

13
Using coverage metrics to measure test suite quality
public void Test()
{
bool result1 = IsStringLong("abc");   
bool result2 = IsStringLong("abcdef");   
}
This test has both code and branch coverage metrics showing 100%. But at the same
time, it is completely useless because it doesn’t verify anything.
But let’s say that you thoroughly verify each outcome of the code under test. Does this,
in combination with the branch coverage metric, provide a reliable mechanism, which
you can use to determine the quality of your test suite? Unfortunately, no. 
Listing 1.3
A test with no assertions always passes.
A story from the trenches
The concept of assertion-free testing might look like a dumb idea, but it does happen
in the wild.
Years ago, I worked on a project where management imposed a strict requirement of
having 100% code coverage for every project under development. This initiative had
noble intentions. It was during the time when unit testing wasn’t as prevalent as it is
today. Few people in the organization practiced it, and even fewer did unit testing
consistently.
A group of developers had gone to a conference where many talks were devoted to
unit testing. After returning, they decided to put their new knowledge into practice.
Upper management supported them, and the great conversion to better programming
techniques began. Internal presentations were given. New tools were installed. And,
more importantly, a new company-wide rule was imposed: all development teams had
to focus on writing tests exclusively until they reached the 100% code coverage mark.
After they reached this goal, any code check-in that lowered the metric had to be
rejected by the build systems.
As you might guess, this didn’t play out well. Crushed by this severe limitation, devel-
opers started to seek ways to game the system. Naturally, many of them came to the
same realization: if you wrap all tests with try/catch blocks and don’t introduce any
assertions in them, those tests are guaranteed to pass. People started to mindlessly
create tests for the sake of meeting the mandatory 100% coverage requirement.
Needless to say, those tests didn’t add any value to the projects. Moreover, they
damaged the projects because of all the effort and time they steered away from pro-
ductive activities, and because of the upkeep costs required to maintain the tests
moving forward.
Eventually, the requirement was lowered to 90% and then to 80%; after some period
of time, it was retracted altogether (for the better!).
Returns true
Returns false


---
**Page 14**

14
CHAPTER 1
The goal of unit testing
NO COVERAGE METRIC CAN TAKE INTO ACCOUNT CODE PATHS IN EXTERNAL LIBRARIES
The second problem with all coverage metrics is that they don’t take into account
code paths that external libraries go through when the system under test calls meth-
ods on them. Let’s take the following example:
public static int Parse(string input)
{
return int.Parse(input);
}
public void Test()
{
int result = Parse("5");
Assert.Equal(5, result);
}
The branch coverage metric shows 100%, and the test verifies all components of the
method’s outcome. It has a single such component anyway—the return value. At the
same time, this test is nowhere near being exhaustive. It doesn’t take into account
the code paths the .NET Framework’s int.Parse method may go through. And
there are quite a number of code paths, even in this simple method, as you can see
in figure 1.6.
The built-in integer type has plenty of branches that are hidden from the test and
that might lead to different results, should you change the method’s input parameter.
Here are just a few possible arguments that can’t be transformed into an integer:
Null value
An empty string
“Not an int”
A string that’s too large
Hidden
part
Start
int.Parse
null
“ ”
“5”
“not an int”
End
Figure 1.6
Hidden code paths of external libraries. Coverage metrics have no way to see how 
many of them there are and how many of them your tests exercise.


---
**Page 15**

15
What makes a successful test suite?
You can fall into numerous edge cases, and there’s no way to see if your tests account
for all of them.
 This is not to say that coverage metrics should take into account code paths in
external libraries (they shouldn’t), but rather to show you that you can’t rely on
those metrics to see how good or bad your unit tests are. Coverage metrics can’t
possibly tell whether your tests are exhaustive; nor can they say if you have enough
tests. 
1.3.4
Aiming at a particular coverage number
At this point, I hope you can see that relying on coverage metrics to determine the
quality of your test suite is not enough. It can also lead to dangerous territory if you
start making a specific coverage number a target, be it 100%, 90%, or even a moder-
ate 70%. The best way to view a coverage metric is as an indicator, not a goal in and
of itself.
 Think of a patient in a hospital. Their high temperature might indicate a fever and
is a helpful observation. But the hospital shouldn’t make the proper temperature of
this patient a goal to target by any means necessary. Otherwise, the hospital might end
up with the quick and “efficient” solution of installing an air conditioner next to the
patient and regulating their temperature by adjusting the amount of cold air flowing
onto their skin. Of course, this approach doesn’t make any sense.
 Likewise, targeting a specific coverage number creates a perverse incentive that
goes against the goal of unit testing. Instead of focusing on testing the things that
matter, people start to seek ways to attain this artificial target. Proper unit testing is dif-
ficult enough already. Imposing a mandatory coverage number only distracts develop-
ers from being mindful about what they test, and makes proper unit testing even
harder to achieve.
TIP
It’s good to have a high level of coverage in core parts of your system.
It’s bad to make this high level a requirement. The difference is subtle but
critical.
Let me repeat myself: coverage metrics are a good negative indicator, but a bad posi-
tive one. Low coverage numbers—say, below 60%—are a certain sign of trouble. They
mean there’s a lot of untested code in your code base. But high numbers don’t mean
anything. Thus, measuring the code coverage should be only a first step on the way to
a quality test suite. 
1.4
What makes a successful test suite?
I’ve spent most of this chapter discussing improper ways to measure the quality of a
test suite: using coverage metrics. What about a proper way? How should you mea-
sure your test suite’s quality? The only reliable way is to evaluate each test in the
suite individually, one by one. Of course, you don’t have to evaluate all of them at


