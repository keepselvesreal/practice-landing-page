# 1.5 Moving On to a One-Based Test: Something’s Happening! (pp.14-17)

---
**Page 14**

Moving On to a One-Based Test: Something’s Happening!
Your zero-based test saved your bacon. Maybe a one-based test can do the
same? Write a test that adds one and only one credit score:
utj3-credit-history/04/src/test/java/credit/ACreditHistory.java
@Test
void withOneRatingHasEquivalentMean() {
var creditHistory = new CreditHistory();
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
}
You might have quickly put that test in place by duplicating the zero-based
test, adding a line to call creditHistory.add(), and changing the assertion.
Your new test passes. Are you done with it? No. Two critical steps remain:
1.
Ensure you’ve seen it fail.
2.
Clean it up.
Making It Fail
If you’ve never seen a test fail for the right reason, don’t trust it.
The test you just wrote contains an assertion that expects arithmeticMean to
return a specific value. “Failing for right reason” for this example would mean
that arithmeticMean returns some value other than 780 (the expected value).
Perhaps the calculation is incorrect, or perhaps the code never makes the
calculation and returns some initial value.
You want to break your code so that the test fails. When it fails, ensure that
the failure message JUnit provides makes sense. Let’s try that.
Chapter 1. Building Your First JUnit Test • 14
report erratum  •  discuss


---
**Page 15**

utj3-credit-history/05/src/main/java/credit/CreditHistory.java
public void add(CreditRating rating) {
//
ratings.add(rating);
➤
}
public int arithmeticMean() {
if (ratings.isEmpty()) return 0;
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
The best way to break things is to comment out the line of code that adds to
the credit history’s ratings collection. Then, rerun the tests (using your new
keyboard shortcut!). JUnit should now look like the following figure.
The JUnit process output on the right shows an exception stack trace. Behind
the scenes, the code in JUnit’s assertEquals method compares the expected value
with the actual value. If they are the same, JUnit returns control to the test,
allowing it to proceed. If the expected value differs from the actual value, JUnit
throws an AssertionFailedError with some useful information attached to it.
Here’s your test again, with the pertinent assertEquals method call highlighted.
utj3-credit-history/05/src/test/java/credit/ACreditHistory.java
@Test
void withOneRatingHasEquivalentMean() {
var creditHistory = new CreditHistory();
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
➤
}
In other words, the assertion compares 780 against the value of result from
the prior step. The message associated with the stack trace describes the
comparison failure:
Expected :780 Actual :0
report erratum  •  discuss
Moving On to a One-Based Test: Something’s Happening! • 15


---
**Page 16**

If you’d mistakenly swapped the order of the arguments to assertEquals, like
this:
assertEquals(result, 780);
…then JUnit’s error message would be inaccurate and confusing:
Expected :0 Actual :780
Your single-rating test doesn’t expect 0; it expects 780. The 0 is the actual
result emanating from the call to arithmeticMean, not 780.
You did see the test fail due to the assertEquals mismatch, so that’s a good thing.
Had you seen something different, it would be a reason to stop and investi-
gate—something is probably wrong with the test in this case. If the test run
shows an exception emanating from the production code, perhaps something
isn’t set up correctly in the test case. If the test run passes, perhaps your
test isn’t really doing what you think it is. You’d want to carefully re-read
the test to see what you’re missing or misrepresenting.
Deliberately fail your tests to prove they’re really doing something.
Corollary: Don’t trust a test you’ve never seen fail.
It might seem easier to get a new test to fail by changing its assertion. For
example, you might change your assertion to assertEquals(result, 9999), which you
know would always result in a failing test.
But think of your tests as “documents of record” for each logical requirement.
Prefer failing the test by changing the production code so that it no longer
meets the requirement, not by altering the conditions of the test. It can require
just a little more thought, but breaking production code will keep you out of
trouble.
Programmers following the practice of test-driven development (TDD) always
demonstrate test failure first to demonstrate that the code they write is
responsible for making the test pass. See Chapter 11, Advancing with Test-
Driven Development (TDD), on page 211 for more on how TDD practitioners
build a cycle around this discipline.
JUnit’s Exceptions
You can click the link of the first line in the stack trace to navigate precisely
to the point where the exception emanated from the code—the assertEquals call.
Chapter 1. Building Your First JUnit Test • 16
report erratum  •  discuss


---
**Page 17**

(If you want to see the relevant execution path through JUnit’s code itself,
you can also click where JUnit says <6 internal lines>.)
All failed asserts throw an AssertionFailedError exception. JUnit catches this or
any other exception thrown during test execution and adds one to its count
of failing tests.
JUnit’s choice to throw an exception means no more code in the test method
gets executed. Any assertions following the first failing one also do not execute,
a deliberate (and good) choice by its designers: Once your first assertion fails,
all bets are off about the state of things. Executing subsequent assertions
may be pointless.
You generally want your tests focused on a single (unit) behavior, which means,
usually, you need only one assertion anyway. You’ll dig deeper into this idea
later in Test Smell: Multiple Assertions, on page 200.
Your probe to watch the test fail involved commenting out a line of code. You
can now uncomment it and watch your test pass again, which should give
you high confidence that your test properly demonstrates the right piece of
behavior.
No More Screenshots
At this point, you’ve graduated…from screenshots! Now that you’ve seen what
to expect in an IDE, you can move forward with learning about unit tests
through raw Java code, presented au naturel rather than cloaked in screen-
shots. Much sleeker, much sexier.
You’ll want to continue to increase your understanding of your IDE’s imple-
mentation of JUnit. Try clicking on its various buttons and menus to learn
more about its shortcuts and power.
Going forward in this book, you’ll mostly see only the code pertinent to the
current discussion (rather than large listings). Minimizing your need to flip
about through the book to find code listings should help you keep your focus
on the relevant code and discussion at hand.
Increasing Your ROI: Cleaning Up Tests
Always review your tests for opportunities to improve their readability. A few
minutes of cleanup now can save countless developers from far more head-
scratching time down the road.
Review your CreditHistory test. See if you can spot ways to improve things.
report erratum  •  discuss
Increasing Your ROI: Cleaning Up Tests • 17


