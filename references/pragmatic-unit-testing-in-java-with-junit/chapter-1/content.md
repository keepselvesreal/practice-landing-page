# Building Your First JUnit Test (pp.3-25)

---
**Page 3**

CHAPTER 1
Building Your First JUnit Test
In this chapter, we’ll write a unit test by working through a small example.
You’ll set up your project, add a test class, and see what a test method looks
like. Most importantly, you’ll get JUnit to run your new, passing test.
Reasons to Write a Unit Test
Joe has just completed work on a small feature change, adding several dozen
lines to the system. He’s fairly confident in his change, but it’s been a while
since he’s tried things out in the deployed system. Joe runs the build script,
which packages and deploys the change to the local web server. He pulls up
the application in his browser, navigates to the appropriate screen, enters a
bit of data, clicks submit, and…stack trace!
Joe stares at the screen for a moment, then the code. Aha! Joe notes that he
forgot to initialize a field. He makes the fix, runs the build script again, cranks
up the application, enters data, clicks submit, and…hmm, that’s not the right
amount. Oops. This time, it takes a bit longer to decipher the problem. Joe
fires up his debugger and after a few minutes discovers an off-by-one error
in indexing an array. He once again repeats the cycle of fix, deploy, navigate
the GUI, enter data, and verify results.
Happily, Joe’s third fix attempt has been the charm. But he spent about fifteen
minutes working through the three cycles of code/manual test/fix.
Lucia works differently. Each time she writes a small bit of code, she adds a
unit test that verifies the small change she added to the system. She then
runs all her unit tests, including the new one just written. They run in sec-
onds, so she doesn’t wait long to find out whether or not she can move on.
Because Lucia runs her tests with each small change, she only moves on
when all the tests pass. If her tests fail, she knows she’s created a problem
report erratum  •  discuss


---
**Page 4**

and stops immediately to fix it. The problems she creates are a lot easier to
fix since she’s added only a few lines of code since she last saw all the tests
pass. She avoids piling lots of new code atop her mistakes before discovering
a problem.
Lucia’s tests are part of the system and included in the project’s GitHub
repository. They continue to pay off each time she or anyone else changes
code, alerting the team when someone breaks existing behavior.
Lucia’s tests also save Joe and everyone else on the team significant amounts
of comprehension time on their system. “How does the system handle the
case where the end date isn’t provided?” asks Madhu, the product owner.
Joe’s response, more often than not, is, “I don’t know; let me take a look at
the code.” Sometimes, Joe can answer the question in a minute or two, but
frequently, he ends up digging about for a half hour or more.
Lucia looks at her unit tests and finds one that matches Madhu’s case. She
has an answer within a minute or so.
You’ll follow in Lucia’s footsteps and learn how to write small, focused unit
tests. You’ll start by learning basic JUnit concepts.
Learning JUnit Basics: Your First Testing Challenge
For your first example, you’ll work with a small class named CreditHistory. Its
goal is to return the mean (average) for a number of credit rating objects.
In this book, you’ll probe the many reasons for choosing to write unit tests.
For now, you’ll start with a simple but critical reason: you want to continue
adding behaviors to CreditHistory and want to know the moment you break any
previously coded behaviors.
Initially, you will see screenshots to help guide you through getting started
with JUnit. After this chapter, you will see very few screenshots, and you
won’t need them.
The screenshots demonstrate using JUnit in IntelliJ IDEA. If you’re using
another integrated development environment (IDE), the good news is that
your JUnit test code will look the same whether you use IDEA, Eclipse,
VSCode, or something else. How you set up your project to use JUnit will
differ. The way the JUnit looks and feels will differ from IDE to IDE, though
it will, in general, operate the same and produce the same information.
Chapter 1. Building Your First JUnit Test • 4
report erratum  •  discuss


---
**Page 5**

Here’s the code you need to test:
utj3-credit-history/01/src/main/java/credit/CreditHistory.java
import java.time.LocalDate;
import java.time.Month;
import java.util.*;
public class CreditHistory {
private final List<CreditRating> ratings = new ArrayList<>();
public void add(CreditRating rating) {
ratings.add(rating);
}
public int arithmeticMean() {
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
}
The CreditHistory class collects CreditRating objects through its add method. Its
current primary goal is to provide you with an average (arithmeticMean) of the
scores contained in the credit rating objects.
You implement CreditRating with a Java record declaring a single rating field.
utj3-credit-history/01/src/main/java/credit/CreditRating.java
public record CreditRating(int rating) {}
Your first exercise is small, and you could easily enter it from scratch. Typing
in the code yourself should help you grow your coding skills faster. Still, you
can also choose to download the source for this and all other exercises from
https://pragprog.com/titles/utj3/pragmatic-unit-testing-in-java-with-junit-third-edition/.
Where to Put the Tests
Your project is laid out per the Apache Software Foundation’s standard
directory layout:
1
utj3-credit-history
src/
main/
java/
credit/
CreditHistory.java
CreditRating.java
test/
java/
credit/
1.
https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
report erratum  •  discuss
Learning JUnit Basics: Your First Testing Challenge • 5


---
**Page 6**

Your two production source files for this project are stored in the directory
src/main/java in the package named credit. (IntelliJ IDEA refers to the direc-
tory src/main/java as a Sources Root.)
You’re ready to write a test that describes the behavior in CreditHistory. You’ll
be putting the test in the same package as the production source—credit—but
in the Test Sources Root directory src/test/java.
Your IDE probably provides you with many ways to create a new test class.
In IDEA, you’ll create it by following these steps in the Project explorer:
1.
Select the package src/test/java/credit from the Project or Packages explorer.
2.
Right-click to bring up the context menu.
3.
Select New ▶ Java Class. You will see the New Java Class popup, which
defaults its selection to creating a new class.
4.
Type the classname ACreditHistory (“a credit history”); press enter. IDEA’s
inspections may be unhappy about your test naming convention. You
can reconfigure the inspection,
2 or you can go with the old-school name
CreditHistoryTest.
Running Tests: Testing Nothing at All
When you press enter from the New ▶Java Class menu item, IDEA provides you
with an empty class declaration for ACreditHistory. Your first job is to squeeze
a test method into it:
utj3-credit-history/01/src/test/java/credit/ACreditHistory.java
class ACreditHistory {
@org.junit.jupiter.api.Test
➤
void whatever() {
➤
}
➤
}
To be a bit more specific: Within the body of ACreditHistory, type in the three
lines that start with the @org.junit.jupiter.api.Test annotation.
Lines marked with arrows in code listings represent added lines,
changed lines, or otherwise interesting bits of code.
Type? Yes. It’s better to type code and tests in yourself while learning, rather
than copy/paste them, unless typing isn’t at all your thing. It’ll feel more like
2.
https://langrsoft.com/2024/04/28/your-new-test-naming-convention/
Chapter 1. Building Your First JUnit Test • 6
report erratum  •  discuss


---
**Page 7**

real development, which should help you learn more. It also won’t take as long
as you think. Your IDE offers numerous time-saving shortcuts, such as
intellisense, live templates, and context-sensitive “quick fix.”
Your test is an empty method annotated with the type @org.junit.jupiter.api.Test.
When you tell JUnit to run one or more tests, it will locate all methods
annotated with @Test and run them. It’ll ignore all other methods.
You can run your empty test, which, for now, you’ve given a placeholder name
of whatever. As usual, you have many options for executing tests. You’ll start
by being mousey. Click the little green arrow that appears to the left of the
class declaration, as shown in the following figure. (Chances are good your
IDE has a similar icon.)
Clicking the green arrow pops up a context menu where you can select the
option to run all tests in ACreditHistory, as shown in this figure:
Clicking Run 'ACreditHistory' runs the whatever test. It’s passing, as the figure on
page 8 reveals.
If your test isn’t getting executed, make sure it follows these three guidelines:
• it is annotated with @org.junit.jupiter.api.Test
• it has a void return
• it has no parameters
report erratum  •  discuss
Learning JUnit Basics: Your First Testing Challenge • 7


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


---
**Page 18**

Scannability: Arrange—Act—Assert
With but four lines, your test is already a mass of code demanding close
attention:
utj3-credit-history/06/src/test/java/credit/ACreditHistory.java
@Test
void withOneRatingHasEquivalentMean() {
var creditHistory = new CreditHistory();
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
}
The test has little scannability (as Mike Hill calls it)—the ability to quickly
locate and comprehend code without having to explicitly read it.
3 Someone
wanting a quick understanding must scrutinize each of its four lines from
top to bottom. This is the opposite of scannable, something I call stepwise.
Lines of stepwise code are the opposite of declarative. They’re strongly linked
to earlier steps, and reading one step alone often provides you with no useful
information. Its intertwining of implementation details further compels you
to slow down, lest you miss something.
The four stepwise lines here don’t seem that terrible, but the problem definitely
adds up—imagine thousands of similarly tedious tests.
Every test you write can be broken down into up to three steps. In order:
• Arrange the system so that it’s in a useful state. This set-up step usually
involves creating objects and calling methods or setting data on them.
Your test arranges state by creating a CreditHistory object and adding a
credit rating to it. The first part of your test name, withOneRating, echoes
this state arrangement. Some tests won’t have any arrange needs (for
example, when you’re making a static method call with literal or no
arguments).
• Act upon the system so as to create the behavior you’re trying to test.
Your test acts on the credit history object by calling its arithmeticMean
method.
• Assert (verify) that the system behaves the way you expect. Your test
asserts that the arithmeticMean is calculated correctly.
3.
https://www.geepawhill.org/2020/03/03/readability-and-scannability/.
Chapter 1. Building Your First JUnit Test • 18
report erratum  •  discuss


---
**Page 19**

Some of your tests will be functionally oriented, in which you invoke a method
that returns a value. For these tests, you can often distill the three Arrange-
Act-Assert (AAA) steps to a single line of test code:
assertEquals(42, new Everything().ultimateAnswer());
To make your tests align with at least one aspect of scannable, use blank
lines to break them into AAA chunks:
utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
@Test
void withOneRatingHasEquivalentMean() {
var creditHistory = new CreditHistory();
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
}
Your test code now has some breathing room. AAA has the same effect as
using paragraphs to break up a page of continuous text.
If all of your tests are similarly consistent, both organizationally and visually,
a developer’s eyes can immediately settle on the test part they’re most inter-
ested in. That consistency alone can significantly reduce the time anyone
must otherwise spend reading through any given test.
Test comprehension starts with reading its name. A well-named test summa-
rizes the behavior that the example (the test code itself) demonstrates. You’ll
learn more about improving your test names in Tests as Documentation, on
page 189.
Once you learn the test’s intent through its name, you might next look at the
act step. It will tell you how the test interacts with the system to trigger
the behavior described by the test name.
Then, read the arrange step to see how the system gets into the proper state
to be tested. Or, if you already know (or don’t care) how things are arranged,
focus instead on the assert step to see how the test verifies that the desired
behavior occurred.
Ultimately, only you will know what parts of a test you need to focus on, and
that interest will change from time to time. For example, if you must add a
new behavior related to an existing one, you’ll probably focus heavily on the
arrange of the related test to understand how it sets up state. If you’re instead
report erratum  •  discuss
Increasing Your ROI: Cleaning Up Tests • 19


---
**Page 20**

trying to understand a specific behavior, you’ll want to focus on how its test’s
arrange steps correlate with the expected result expressed in the assert step.
Quickly finding what you need is a key component of increasing your devel-
opment speed, and a large part of succeeding is related to scannability.
Follow Bill Wake’s AAA mnemonic
4 and consistently (visually)
chunk your tests as a valuable means of improving scannability.
Abstraction: Eliminating Boring Details
After chunking both tests using the Arrange—Act—Assert (AAA) pattern, your
tests are more scannable:
utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
@Test
void withOneRatingHasEquivalentMean() {
var creditHistory = new CreditHistory();
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
}
But note that both tests repeat the same uninteresting line of code that creates
a CreditHistory instance:
utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
var creditHistory = new CreditHistory();
That line of code is, of course, necessary for each test to successfully execute,
but you really don’t have to see it in order to understand the tests.
JUnit provides a hook you can use to move common test initialization into a
single place, which at the same time moves it away from the more relevant
test code. The @BeforeEach annotation can mark one or more methods to be
executed before each and every test.
utj3-credit-history/08/src/test/java/credit/ACreditHistory.java
import org.junit.jupiter.api.BeforeEach;
➤
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class ACreditHistory {
CreditHistory creditHistory;
➤
4.
https://xp123.com/3a-arrange-act-assert/
Chapter 1. Building Your First JUnit Test • 20
report erratum  •  discuss


---
**Page 21**

@BeforeEach
➤
void createInstance() {
➤
creditHistory = new CreditHistory();
➤
}
➤
@Test
void withNoCreditRatingsHas0Mean() {
var result = creditHistory.arithmeticMean();
assertEquals(0, result);
}
@Test
void withOneRatingHasEquivalentMean() {
creditHistory.add(new CreditRating(780));
var result = creditHistory.arithmeticMean();
assertEquals(780, result);
}
}
The highlighted lines show a typical use for the @BeforeEach hook. The test declares
a field named creditHistory and then initializes it in the annotated createInstance
method. That allows you to remove the local initializations of creditHistory from
both tests.
Here’s how things happen when JUnit runs these two tests in ACreditHistory:
1.
JUnit creates a new instance of ACreditHistory.
2.
JUnit executes the createInstance method on this instance, which initializes
the creditHistory field.
3.
JUnit executes one of either withNoCreditRatingsHas0Mean or withOneRatingHas-
EquivalentMean, depending on how Java returns the methods declared on a
class. In other words, they don’t run in an order you can depend on.
That’s okay. You want each test to stand completely on its own and not
care about the order in which it’s executed.
4.
JUnit creates a new instance of ACreditHistory.
5.
JUnit executes the createInstance method on this instance.
6.
JUnit executes the other test, the one not already run.
Still fuzzy? Understandable. Put a System.out.println() call in the @BeforeEach hook,
as well as in each of the two tests. Also, create a no-arg constructor and put
a System.out.println() statement in that. Then run your tests; the output should
jibe with the preceding list—you should see six println lines.
report erratum  •  discuss
Increasing Your ROI: Cleaning Up Tests • 21


---
**Page 22**

I just heard you say, “Big deal.” Yep, you have removed a measly line from a
couple of tests, but you have actually introduced more total lines in the
source file.
The remaining tests are now as immediate and scannable as possible. Each
AAA chunk is one line. You can visually scan past boring initialization code
and instead focus on exactly what arrangement is needed to achieve the
desired outcome. You can more quickly correlate the arrange and act steps
and answer the question, “Why does this assertion pass?”
Your tests are highly abstract: They emphasize and document what’s relevant
in each test and de-emphasize necessary but boring details.
Most of your tests can be this concise, with a typical range from one to five
statements. They’ll be easier to write in the first place, easier to understand
(and don’t forget, “write once, read many”), and easier to change when
requirements change. You’ll find additional tips for keeping tests short and
meaningful in Chapter 5, Examining Outcomes with Assertions, on page 99.
Eliminating Clutter and JUnit 5
Your test code may appear to violate longstanding Java conventions. Neither
the class nor the test method signatures declare explicit modifiers. Older
versions of JUnit did require the public modifier. In JUnit 5, classes and
methods should have package-level access.
Omitting the extra keyword goes one more step toward emphasizing the
abstraction of tests by eliminating one more bit of clutter. Your tests move
in the direction of documentation and away from implementation details. They
describe behaviors.
In a similar vein, you can omit the typical access modifier of private for fields.
If you’re worried, don’t be. None of your code will ever call test methods, and
no one will violate their “exposed” fields.
ZOM: Zero and One Done, Now Testing Many
You’ve written a zero-based test (a test for the “zero” case) and a one-based
test so far. It’s time to slam out a many-based test:
utj3-credit-history/09/src/test/java/credit/ACreditHistory.java
@Test
void withMultipleRatingsDividesTotalByCount() {
creditHistory.add(new CreditRating(780));
creditHistory.add(new CreditRating(800));
creditHistory.add(new CreditRating(820));
Chapter 1. Building Your First JUnit Test • 22
report erratum  •  discuss


---
**Page 23**

var result = creditHistory.arithmeticMean();
assertEquals(800, result);
}
You can create this test by copying the one-based test, duplicating a couple
of lines in order to add a total of three credit ratings, and changing the
expected value for the assertion. It should pass. Break it; it should fail. Fix
it again and demonstrate that it passes. It’s possible to do all of that within
a total of about two minutes.
You might wonder if you need all three tests. The one-based test really doesn’t
differ much from the many-based test, and they don’t execute anything differ-
ently with respect to code paths. It’s a debatable point, and ultimately, it’s
up to you.
Prefer deleting tests that don’t add any value in terms of “documenting variant
behaviors.” It was still useful for you to build tests using a zero-one-many
(ZOM) progression, and it really didn’t take any significant additional time to
write all three tests. If you buy that, you should have no qualms about
deleting the one-based test.
Delete it! Doing so allows you to simplify the test name: withMultipleRatingsDivides-
TotalByCount. Here’s your final test class:
utj3-credit-history/10/src/test/java/credit/ACreditHistory.java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.time.LocalDate;
import static org.junit.jupiter.api.Assertions.assertEquals;
class ACreditHistory {
CreditHistory creditHistory;
@BeforeEach
void createInstance() {
creditHistory = new CreditHistory();
}
@Test
void withNoCreditRatingsHas0Mean() {
var result = creditHistory.arithmeticMean();
assertEquals(0, result);
}
@Test
void withRatingsDividesTotalByCount() {
➤
creditHistory.add(new CreditRating(780));
creditHistory.add(new CreditRating(800));
creditHistory.add(new CreditRating(820));
report erratum  •  discuss
ZOM: Zero and One Done, Now Testing Many • 23


---
**Page 24**

var result = creditHistory.arithmeticMean();
assertEquals(800, result);
}
}
Always consider writing a test for each of Zero, One, and Many
(ZOM) cases.
Covering Other Cases: Creating a Test List
Beyond the ZOM cases you’ve covered, you could brainstorm edge cases and
exception-based tests. You’ll explore doing that in later chapters.
As you write tests and continue to re-visit/re-read the code you’re testing,
you’ll think of additional tests you should write. In fact, as you write the code
yourself in the first place—before trying to write tests for it—think about and
note the cases you’ll need for that code.
Add the cases you think of to a test list to remember to write them. Cross
them off as you implement or obviate them. You can do this on paper, in a
notepad file, or even in the test class itself as a series of comments. (Perhaps
in the form of TODO comments, which IDEs like IntelliJ IDEA and Eclipse will
collect in a view as a set of reminders.) Things change, so don’t expend the
effort to code these tests just yet. You can read more on this highly useful
tool in Kent Beck’s seminal book on TDD [Bec02].
Congratulations!…But Don’t Stop Yet
In this chapter, you got past one of the more significant challenges: getting
a first test to pass using JUnit in your IDE. Congrats! Along with that
achievement, you also learned:
• What it takes to write a test that JUnit can accept and run
• How to tell JUnit to run your tests
• How to interpret the test results provided by JUnit
• How to use the ZOM mnemonic to figure out what the next test might be
• How to structure a test using AAA
You’ve been reading about “units” throughout this chapter. Next up, you’ll
learn what a unit is, and you’ll learn a number of tactics for testing some of
the common units that you’ll encounter.
Chapter 1. Building Your First JUnit Test • 24
report erratum  •  discuss


---
**Page 25**

CHAPTER 2
Testing the Building Blocks
In the previous chapter, you took a small piece of code and wrote a few JUnit
tests around it. In the process, you learned how to structure your tests, exe-
cute them, how to interpret results, and what test to write next.
You’ve only scratched the surface of what it means to write tests for code. In
this chapter, you’ll examine several common code constructs and learn how
to test them. These are the topics you’ll cover:
• Testing pure functions
• Testing code with side effects
• How different designs can impact unit tests
• Writing tests for code involving lists
• Writing tests for code that throws exceptions
• Covering boundary conditions with tests
First, however, let’s talk about the word unit in unit test.
Units
A software system is an organized collection of many units. A unit is the
smallest piece of code that accomplishes a specific behavioral goal—a concept.
Here are some examples of concepts:
• Capitalize the first letter of a word
• Move a passenger from the standby list to the boarding list
• Mark a passenger as upgraded
• Calculate the mean credit rating for an individual
• Throw an exception when a user is under 18 years old
report erratum  •  discuss


