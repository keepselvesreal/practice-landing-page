# 4.1.2 The second pillar: Resistance to refactoring (pp.69-71)

---
**Page 69**

69
Diving into the four pillars of a good unit test
 Note that it’s not only the amount of code that matters, but also its complexity and
domain significance. Code that represents complex business logic is more important
than boilerplate code—bugs in business-critical functionality are the most damaging.
 On the other hand, it’s rarely worthwhile to test trivial code. Such code is short and
doesn’t contain a substantial amount of business logic. Tests that cover trivial code
don’t have much of a chance of finding a regression error, because there’s not a lot of
room for a mistake. An example of trivial code is a single-line property like this:
public class User
{
public string Name { get; set; }
}
Furthermore, in addition to your code, the code you didn’t write also counts: for
example, libraries, frameworks, and any external systems used in the project. That
code influences the working of your software almost as much as your own code. For
the best protection, the test must include those libraries, frameworks, and external sys-
tems in the testing scope, in order to check that the assumptions your software makes
about these dependencies are correct.
TIP
To maximize the metric of protection against regressions, the test needs
to aim at exercising as much code as possible. 
4.1.2
The second pillar: Resistance to refactoring
The second attribute of a good unit test is resistance to refactoring—the degree to which
a test can sustain a refactoring of the underlying application code without turning red
(failing).
DEFINITION
Refactoring means changing existing code without modifying its
observable behavior. The intention is usually to improve the code’s nonfunc-
tional characteristics: increase readability and reduce complexity. Some exam-
ples of refactoring are renaming a method and extracting a piece of code into
a new class.
Picture this situation. You developed a new feature, and everything works great. The
feature itself is doing its job, and all the tests are passing. Now you decide to clean up
the code. You do some refactoring here, a little bit of modification there, and every-
thing looks even better than before. Except one thing—the tests are failing. You look
more closely to see exactly what you broke with the refactoring, but it turns out that
you didn’t break anything. The feature works perfectly, just as before. The problem is
that the tests are written in such a way that they turn red with any modification of the
underlying code. And they do that regardless of whether you actually break the func-
tionality itself.
 This situation is called a false positive. A false positive is a false alarm. It’s a result
indicating that the test fails, although in reality, the functionality it covers works as


---
**Page 70**

70
CHAPTER 4
The four pillars of a good unit test
intended. Such false positives usually take place when you refactor the code—when
you modify the implementation but keep the observable behavior intact. Hence the
name for this attribute of a good unit test: resistance to refactoring.
 To evaluate how well a test scores on the metric of resisting to refactoring, you
need to look at how many false positives the test generates. The fewer, the better.
 Why so much attention on false positives? Because they can have a devastating
effect on your entire test suite. As you may recall from chapter 1, the goal of unit test-
ing is to enable sustainable project growth. The mechanism by which the tests enable
sustainable growth is that they allow you to add new features and conduct regular
refactorings without introducing regressions. There are two specific benefits here:
Tests provide an early warning when you break existing functionality. Thanks to such
early warnings, you can fix an issue long before the faulty code is deployed to
production, where dealing with it would require a significantly larger amount
of effort.
You become confident that your code changes won’t lead to regressions. Without such
confidence, you will be much more hesitant to refactor and much more likely
to leave the code base to deteriorate.
False positives interfere with both of these benefits:
If tests fail with no good reason, they dilute your ability and willingness to react
to problems in code. Over time, you get accustomed to such failures and stop
paying as much attention. After a while, you start ignoring legitimate failures,
too, allowing them to slip into production.
On the other hand, when false positives are frequent, you slowly lose trust in the
test suite. You no longer perceive it as a reliable safety net—the perception is
diminished by false alarms. This lack of trust leads to fewer refactorings,
because you try to reduce code changes to a minimum in order to avoid regres-
sions.
A story from the trenches
I once worked on a project with a rich history. The project wasn’t too old, maybe two
or three years; but during that period of time, management significantly shifted the
direction they wanted to go with the project, and development changed direction
accordingly. During this change, a problem emerged: the code base accumulated
large chunks of leftover code that no one dared to delete or refactor. The company
no longer needed the features that code provided, but some parts of it were used in
new functionality, so it was impossible to get rid of the old code completely.
The project had good test coverage. But every time someone tried to refactor the old
features and separate the bits that were still in use from everything else, the tests
failed. And not just the old tests—they had been disabled long ago—but the new
tests, too. Some of the failures were legitimate, but most were not—they were false
positives.


---
**Page 71**

71
Diving into the four pillars of a good unit test
This story is typical of most projects with brittle tests. First, developers take test failures
at face value and deal with them accordingly. After a while, people get tired of tests
crying “wolf” all the time and start to ignore them more and more. Eventually, there
comes a moment when a bunch of real bugs are released to production because devel-
opers ignored the failures along with all the false positives.
 You don’t want to react to such a situation by ceasing all refactorings, though. The
correct response is to re-evaluate the test suite and start reducing its brittleness. I
cover this topic in chapter 7. 
4.1.3
What causes false positives?
So, what causes false positives? And how can you avoid them?
 The number of false positives a test produces is directly related to the way the test
is structured. The more the test is coupled to the implementation details of the system
under test (SUT), the more false alarms it generates. The only way to reduce the
chance of getting a false positive is to decouple the test from those implementation
details. You need to make sure the test verifies the end result the SUT delivers: its
observable behavior, not the steps it takes to do that. Tests should approach SUT veri-
fication from the end user’s point of view and check only the outcome meaningful to
that end user. Everything else must be disregarded (more on this topic in chapter 5).
 The best way to structure a test is to make it tell a story about the problem domain.
Should such a test fail, that failure would mean there’s a disconnect between the story
and the actual application behavior. It’s the only type of test failure that benefits you—
such failures are always on point and help you quickly understand what went wrong.
All other failures are just noise that steer your attention away from things that matter.
 Take a look at the following example. In it, the MessageRenderer class generates
an HTML representation of a message containing a header, a body, and a footer.
public class Message
{
public string Header { get; set; }
public string Body { get; set; }
public string Footer { get; set; }
}
At first, the developers tried to deal with the test failures. However, since the vast
majority of them were false alarms, the situation got to the point where the develop-
ers ignored such failures and disabled the failing tests. The prevailing attitude was,
“If it’s because of that old chunk of code, just disable the test; we’ll look at it later.”
Everything worked fine for a while—until a major bug slipped into production. One of
the tests correctly identified the bug, but no one listened; the test was disabled along
with all the others. After that accident, the developers stopped touching the old code
entirely.
Listing 4.1
Generating an HTML representation of a message


