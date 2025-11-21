# 1.4 Dealing with Failure (pp.11-14)

---
**Page 11**

returned by the system you’re testing second. The signature for assertEquals
makes the order clear. If you ever forget, use your IDE to show it to you:
public static void assertEquals(int expected, int actual)
When you run your test, you’ll see why the order for expected and actual
arguments matters. You’ll do that in the forthcoming section, Making It Fail,
on page 14. Stick around!
Dealing with Failure
You previously learned to click on the little JUnit run icon next to the class
declaration to execute all its tests. But you’re going to be running tests quite
often—potentially hundreds of times per day, and mousing about is a much
slower, labor-intensive process. It behooves you to be more efficient. Repetitive
stress injuries are real and unpleasant.
Any good IDE will show you the appropriate keyboard shortcut when you
hover over a button. Hovering over the JUnit “run” button reveals Ctrl-Shift-R
as the appropriate shortcut in my IDE. Hover over yours. Write down the
shortcut it provides. Press it and run your tests. Press it again. And again.
And remember it. And from here on out, for the thousands of times you will
ultimately need to run your tests, use the keyboard. You’ll go faster, and your
tendons will thank you.
Your test is failing. Your JUnit execution should look similar to the following
figure.
report erratum  •  discuss
Dealing with Failure • 11


---
**Page 12**

This information-rich view contains several pieces of information about your
test’s failing execution:
1.
The JUnit panel to the left, which gives you a hierarchical listing of the
tests executed, marks both the test class name ACreditHistory and the test
method name withNoCreditRatingsHas0Mean with a yellow x. You can click on
that test method name to focus on its execution details.
2.
The JUnit panel to the right gets to the point with a statistical summary:
Tests failed: 1 of 1 test That is, JUnit executed one test, and that sole test
failed.
3.
Below that redundantly phrased summary, JUnit shows the gory execution
details for the test. The failure left behind an exception stack trace that
tells you the test barfed before even reaching its assertion statement.
4.
The stack trace screams at you in red text—the favored color of items
designed to alert, like errors, stop signs, and poisoned lipstick. You have
a divide-by-zero problem. The stack trace is linked to appropriate lines
in the source, which allows you to quickly navigate to the offending code:
public int arithmeticMean() {
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size(); // oops!
}
Your test added no credit ratings to the CreditHistory. As a result, ratings.size()
returns a 0, and Java throws an ArithmeticException as its way of telling you it
wants nothing to do with that sort of division. Oops!
Your exception-throwing test reveals another useful JUnit nugget: if code
executed in a test run throws an exception that’s not caught, that counts as
a failing test.
Fixing the Problem
The unit test did its job: it notified you of a problem. Earlier, you decided that
it’s possible someone could call arithmeticMean before any credit ratings are
added. You also decided that you don’t want the code to throw an exception
in that case; you instead want it to return a 0. The unit test captures and
documents your choice.
Your unit test will continue to protect you from future regressions, letting
you know anytime the behavior of arithmeticMean changes.
To get the failing test to pass—to fix your problem—add a guard clause to the
arithmeticMean method in CreditHistory:
Chapter 1. Building Your First JUnit Test • 12
report erratum  •  discuss


---
**Page 13**

utj3-credit-history/03/src/main/java/credit/CreditHistory.java
public int arithmeticMean() {
if (ratings.isEmpty()) return 0;
➤
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
Run the tests again to see if your change did the trick. This time, kick them
off by using the Project view (usually the upper-left-most tool window in IDEA
and other IDEs). Drill down from the project at its top level until you can
select the test/java directory, as shown in this figure:
A right-click brings up a near-freakishly large context menu:
Select the option Run ’All Tests’. JUnit will execute all the tests within
src/test/java. Success! Here’s the passing test (as shown in the figure on page
14), where everything is a glorious green and devoid of stack trace statements.
Looks good, right? Feels good, right? Go ahead and hit that Ctrl-Shift-R
keystroke (or its equivalent on your machine) to run the test again. Bask in
the glory.
report erratum  •  discuss
Dealing with Failure • 13


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


