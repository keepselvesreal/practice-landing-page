# 1.6 Increasing Your ROI: Cleaning Up Tests (pp.17-22)

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


