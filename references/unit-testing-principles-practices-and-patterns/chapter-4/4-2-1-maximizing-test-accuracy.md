# 4.2.1 Maximizing test accuracy (pp.76-78)

---
**Page 76**

76
CHAPTER 4
The four pillars of a good unit test
how a message is displayed in the browser. Failures of such a test are always on point:
they communicate a change in the application behavior that can affect the customer
and thus should be brought to the developer’s attention. This test will produce few, if
any, false positives.
 Why few and not none at all? Because there could still be changes in Message-
Renderer that would break the test. For example, you could introduce a new parame-
ter in the Render() method, causing a compilation error. And technically, such an
error counts as a false positive, too. After all, the test isn’t failing because of a change
in the application’s behavior.
 But this kind of false positive is easy to fix. Just follow the compiler and add a new
parameter to all tests that invoke the Render() method. The worse false positives are
those that don’t lead to compilation errors. Such false positives are the hardest to deal
with—they seem as though they point to a legitimate bug and require much more
time to investigate.
4.2
The intrinsic connection between the first 
two attributes
As I mentioned earlier, there’s an intrinsic connection between the first two pillars of
a good unit test—protection against regressions and resistance to refactoring. They both con-
tribute to the accuracy of the test suite, though from opposite perspectives. These two
attributes also tend to influence the project differently over time: while it’s important
to have good protection against regressions very soon after the project’s initiation, the
need for resistance to refactoring is not immediate.
 In this section, I talk about
Maximizing test accuracy
The importance of false positives and false negatives
4.2.1
Maximizing test accuracy
Let’s step back for a second and look at the broader picture with regard to test results.
When it comes to code correctness and test results, there are four possible outcomes,
as shown in figure 4.3. The test can either pass or fail (the rows of the table). And the
functionality itself can be either correct or broken (the table’s columns).
 The situation when the test passes and the underlying functionality works as
intended is a correct inference: the test correctly inferred the state of the system (there
are no bugs in it). Another term for this combination of working functionality and a
passing test is true negative.
 Similarly, when the functionality is broken and the test fails, it’s also a correct infer-
ence. That’s because you expect to see the test fail when the functionality is not work-
ing properly. That’s the whole point of unit testing. The corresponding term for this
situation is true positive.
 But when the test doesn’t catch an error, that’s a problem. This is the upper-right
quadrant, a false negative. And this is what the first attribute of a good test—protection


---
**Page 77**

77
The intrinsic connection between the first two attributes
against regressions—helps you avoid. Tests with a good protection against regressions
help you to minimize the number of false negatives—type II errors.
 On the other hand, there’s a symmetric situation when the functionality is correct
but the test still shows a failure. This is a false positive, a false alarm. And this is what the
second attribute—resistance to refactoring—helps you with.
 All these terms (false positive, type I error and so on) have roots in statistics, but can
also be applied to analyzing a test suite. The best way to wrap your head around them
is to think of a flu test. A flu test is positive when the person taking the test has the flu.
The term positive is a bit confusing because there’s nothing positive about having the
flu. But the test doesn’t evaluate the situation as a whole. In the context of testing,
positive means that some set of conditions is now true. Those are the conditions the
creators of the test have set it to react to. In this particular example, it’s the presence
of the flu. Conversely, the lack of flu renders the flu test negative.
 Now, when you evaluate how accurate the flu test is, you bring up terms such as
false positive or false negative. The probability of false positives and false negatives tells
you how good the flu test is: the lower that probability, the more accurate the test.
 This accuracy is what the first two pillars of a good unit test are all about. Protection
against regressions and resistance to refactoring aim at maximizing the accuracy of the test
suite. The accuracy metric itself consists of two components:
How good the test is at indicating the presence of bugs (lack of false negatives,
the sphere of protection against regressions)
How good the test is at indicating the absence of bugs (lack of false positives,
the sphere of resistance to refactoring)
Another way to think of false positives and false negatives is in terms of signal-to-noise
ratio. As you can see from the formula in figure 4.4, there are two ways to improve test
Table of error types
Type II error
(false negative)
Correct inference
(true positives)
Type I error
(false positive)
Correct inference
(true negatives)
Resistance to
refactoring
Test
result
Test fails
Test passes
Correct
Functionality is
Broken
Protection
against
regressions
Figure 4.3
The relationship between protection against regressions and resistance to 
refactoring. Protection against regressions guards against false negatives (type II errors). 
Resistance to refactoring minimizes the number of false positives (type I errors).


---
**Page 78**

78
CHAPTER 4
The four pillars of a good unit test
accuracy. The first is to increase the numerator, signal: that is, make the test better at
finding regressions. The second is to reduce the denominator, noise: make the test bet-
ter at not raising false alarms.
 Both are critically important. There’s no use for a test that isn’t capable of finding
any bugs, even if it doesn’t raise false alarms. Similarly, the test’s accuracy goes to zero
when it generates a lot of noise, even if it’s capable of finding all the bugs in code.
These findings are simply lost in the sea of irrelevant information. 
4.2.2
The importance of false positives and false negatives: 
The dynamics
In the short term, false positives are not as bad as false negatives. In the beginning of a
project, receiving a wrong warning is not that big a deal as opposed to not being
warned at all and running the risk of a bug slipping into production. But as the proj-
ect grows, false positives start to have an increasingly large effect on the test suite
(figure 4.5).
Test accuracy =
Noise (number of false alarms raised)
Signal (number of bugs found)
Figure 4.4
A test is accurate insofar as it generates a 
strong signal (is capable of finding bugs) with as little 
noise (false alarms) as possible.
Eﬀect on the
test suite
Project duration
False negatives
False positives
Figure 4.5
False positives (false alarms) don’t have as much of a 
negative effect in the beginning. But they become increasingly 
important as the project grows—as important as false negatives 
(unnoticed bugs).


