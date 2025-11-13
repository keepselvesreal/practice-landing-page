# 1.3 Writing a First Real Test (pp.8-11)

---
**Page 8**

The built-in JUnit test runner appears at the bottom of the IDE. Its left-hand
panel shows a summary of all the tests executed. Your summary shows that
you ran the whatever test within ACreditHistory, that it succeeded (because it has
a green check mark), and that it took 12 milliseconds to execute.
The test runner’s right-hand panel shows different information depending on
what’s selected in the left-hand panel. By default, it tells you how many tests
passed out of the number that were executed (yours: “1 of 1”). It also provides
you with information captured as part of the JUnit process execution. (In this
screenshot, the IDE is configured to use Gradle to execute the test via the
build task, which also executes the tests.)
You now know something fundamental about how JUnit behaves: an empty
test passes. More specifically and more usefully, a test whose method execu-
tion completes—without having encountered any failure points or throwing
any exceptions—is a passing test.
Writing a First Real Test
An empty test isn’t of much use. Let’s devise a good first test.
You could start with a meaty test that adds a few credit scores, asks for the
average, and then ascertains whether or not you got the right answer. This
happy path test case—in contrast with negative or error-based tests—is not
the only test you’d want to write, though. You have some other cases to con-
sider for verifying arithmeticMean:
Chapter 1. Building Your First JUnit Test • 8
report erratum  •  discuss


---
**Page 9**

• What happens if you add only one credit rating?
• What happens if you don’t add any credit ratings?
• Are there any exceptional cases—conditions under which a problem could
occur? How does the code behave under these conditions?
Starting with a happy path test is one choice; you have other options. One is
to start with the simplest test possible, move on to incrementally more complex
tests, and finally to exceptional cases. Another option is to start with the
exceptional cases first, then cover happy path cases in complexity order.
Other ordering schemes are, of course, possible.
When writing unit tests for code you’ve already written, ultimately, the order
really doesn’t matter. But if you follow a consistent approach, you’ll be less
likely to miss something. Throughout this book, the progression you’ll prefer
will be to start with the simplest case, then move on to incrementally more
complex happy path cases, and then to exception-based tests.
The Simplest Possible Case
The simplest case often involves zero or some concept of nothing. Calcu-
lating the arithmetic mean involves creating a credit history with nothing
added to it. You think that an empty credit history should return an average
of zero.
Update ACreditHistory with the following code, which replaces the whatever test
with a new one:
utj3-credit-history/02/src/test/java/credit/ACreditHistory.java
import org.junit.jupiter.api.Test;
Line 1
import static org.junit.jupiter.api.Assertions.assertEquals;
-
-
class ACreditHistory {
-
@Test
5
void withNoCreditRatingsHas0Mean() {
-
var creditHistory = new CreditHistory();
-
var result = creditHistory.arithmeticMean();
-
assertEquals(0, result);
-
}
10
}
-
Let’s step through the updated lines in ACreditHistory.java.
Each of your tests will call one or more assertion methods to verify your
assumptions about the system. That’ll add up to piles of lines of assertions.
Since these assertions are static methods, add a static import at 2 so that
you don’t have to constantly qualify your assertion calls.
report erratum  •  discuss
Writing a First Real Test • 9


---
**Page 10**

Line 2: You simplify your test declaration by introducing an import statement
for the @Test annotation.
The test name whatever wasn’t much of a winner, so supply a new one at line
6. As with all tests you write, strive for a test name that summarizes what
the test verifies. Here’s a wacky idea: have the test name complete a sentence
about the behavior it describes.
A Credit History…with no credit ratings…has a 0 mean
Your test describes a credit history object in a certain context—it has no
credit ratings. You expect something to hold true about that credit history in
that context: it has a zero mean. Your test name is a concise representation
of that context and expected outcome:
ACreditHistory ... withNoCreditRatingsHas0Mean() { }
Was that a snort? No, you don’t have to follow this test class naming conven-
tion, but it’s as valid as any other. You’ll read about alternative naming
schemes at Documenting Your Tests with Consistent Names, on page 190.
On to the body of the code—where the work gets done. Your test first creates a
CreditHistory instance (line 7). This new object allows your test to run from a clean
slate, keeping it isolated from the effects of other tests. JUnit helps reinforce
such isolation by creating a new instance of the test class—ACreditHistory—for
each test it executes.
Your test next (at line 8) interacts with the CreditHistory test instance to exercise
the behavior that you want to verify. Here, you call its arithmeticMean method
and capture the return value in result.
Your test finally (at line 9) asserts that the expected (desired) result of 0
matches the actual result captured.
Your call to assertEquals uses JUnit’s bread-and-butter assertion method, which
compares a result with what you expect. The majority of your tests will use
assertEquals. The rest will use one of many other assert forms that you’ll learn
in Chapter 5, Examining Outcomes with Assertions, on page 99.
An assertEquals method call passes if its two arguments match each other. It
fails if the two arguments do not match. The test method as a whole fails if
it encounters any assertion failures.
The hard part about learning assertEquals is remembering the correct order of
its arguments. The value your test expects comes first; the actual value
Chapter 1. Building Your First JUnit Test • 10
report erratum  •  discuss


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


