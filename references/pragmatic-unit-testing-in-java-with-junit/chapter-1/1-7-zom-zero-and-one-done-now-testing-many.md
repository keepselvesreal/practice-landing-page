# 1.7 ZOM: Zero and One Done, Now Testing Many (pp.22-24)

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


