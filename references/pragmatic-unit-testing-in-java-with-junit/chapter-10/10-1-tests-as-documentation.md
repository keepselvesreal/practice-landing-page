# 10.1 Tests as Documentation (pp.189-192)

---
**Page 189**

CHAPTER 10
Streamlining Your Tests
You’ve wrapped up a couple of chapters that teach you how to use tests to
keep your code clean. Now, it’s time to focus on the tests themselves.
Your tests represent a significant investment. They’ll pay off by minimizing
defects and allowing you to keep your production system clean through
refactoring. But, they also represent a continual cost. You need to continually
revisit your tests as your system changes. At times, you’ll want to make
sweeping changes and might end up having to fix numerous broken tests as
a result.
In this chapter, you’ll learn to refactor your tests, much like you would
refactor your production system, to maximize understanding and minimize
maintenance costs. You’ll accomplish this by learning to identify a series of
“smells” in your tests that make it harder to quickly understand them. You’ll
work through an example or two of how you can transform each smell into
de-odorized code.
The deodorization process is quick. In reading through the chapter, you might
think it would take a long time to clean a test similar to the example in the
chapter. In reality, it’s often well under fifteen minutes of real work once you
learn how to spot the problems.
Tests as Documentation
Your unit tests should provide lasting and trustworthy documentation of the
capabilities of the classes you build. Tests provide opportunities to explain
things that the code itself can’t do as easily. Well-designed tests can supplant
a lot of the comments you might otherwise feel compelled to write.
report erratum  •  discuss


---
**Page 190**

Documenting Your Tests with Consistent Names
The more you combine cases into a single test, the more generic and mean-
ingless the test name becomes. A test named matches doesn’t tell anyone squat
about what it demonstrates.
As you move toward more granular tests, each focused on a distinct behavior,
you have the opportunity to impart more meaning in each of your test names.
Instead of suggesting what context you’re going to test, you can suggest what
happens as a result of invoking some behavior against a certain context.
You’re probably thinking, “Real examples, please, Jeff, and not so much bab-
ble.” Here you go:
cooler, more descriptive name
not-so-hot name
withdrawalReducesBalanceByWithdrawnAmount
makeSingleWithdrawal
withdrawalOfMoreThanAvailableFundsGeneratesError
attemptToWithdrawTooMuch
multipleDepositsIncreaseBalanceBySumOfDeposits
multipleDeposits
That last test name seems kind of an obvious statement, but that’s because you
already understand the ATM domain and the concept of deposits. Often,
you’re in unfamiliar territory, where the code and business rules are unfamil-
iar. A precise test name can provide you with extremely useful context.
You can go too far. Reasonable test names probably consist of up to seven
(plus or minus two) words. Longer names quickly become dense sentences
that take time to digest. If test names are typically long, your design may be
amiss.
Seek a consistent form for your test names to reduce the friction that others
experience when perusing your tests. Most of the test examples in this book
are named to complete a sentence that starts with the test class name. For
example:
class APortfolio {
@Test
void increasesSizeWhenPurchasingNewSymbol() {
// ...
}
}
Concatenate each test name to the class name: “a portfolio increases size
when purchasing a new symbol.”
Another possible form:
doingSomeOperationGeneratesSomeResult
Chapter 10. Streamlining Your Tests • 190
report erratum  •  discuss


---
**Page 191**

And another:
someResultOccursUnderSomeCondition
Or you might decide to go with the given-when-then naming pattern, which
derives from a process known as behavior-driven development:
1
givenSomeContextWhenDoingSomeBehaviorThenSomeResultOccurs
Given-when-then test names can be a mouthful, though you can usually drop
the givenSomeContext portion without creating too much additional work for
your test reader:
whenDoingSomeBehaviorThenSomeResultOccurs
…which is about the same as doingSomeOperationGeneratesSomeResult.
JUnit 5’s support for nested test classes allows you to structure your test
class to directly support given-when-then:
utj3-refactor-tests/01/src/test/java/portfolio/ANonEmptyPortfolio.java
class ANonEmptyPortfolio {
Portfolio portfolio = new Portfolio();
int initialSize;
@BeforeEach
void purchaseASymbol() {
portfolio.purchase("LSFT", 20);
initialSize = portfolio.size();
}
@Nested
class WhenPurchasingAnotherSymbol {
@BeforeEach
void purchaseAnotherSymbol() {
portfolio.purchase("AAPL", 10);
}
@Test
void increasesSize() {
assertEquals(initialSize + 1, portfolio.size());
}
}
}
Which form you choose isn’t as important as being consistent. Your main
goal: create easy-to-read test names that clearly impart meaning.
1.
http://en.wikipedia.org/wiki/Behavior-driven_development
report erratum  •  discuss
Tests as Documentation • 191


---
**Page 192**

Keeping Your Tests Meaningful
If others (or you yourself) have a tough time understanding what a test is
doing, don’t add comments. That’s like adding footnotes to describe poorly
written text. Improve the test instead, starting with its name. These are other
things you can do:
• Improve any local variable names.
• Introduce meaningful constants.
• Prefer matcher-based assertions (for example, those from AssertJ).
• Split larger tests into smaller, more focused tests.
• Move test clutter to helper methods and @Before methods.
Rework test names and code to tell stories instead of introducing
explanatory comments.
Searching for an Understanding
You’re tasked with enhancing the search capabilities of an application. You
know you must change the util.Search class, but you’re not at all familiar with
it. You turn to the tests. Well, a test—there’s only one. You roll your eyes in
annoyance and then begin struggling to figure out what this test is trying to
prove:
utj3-refactor-tests/01/src/test/java/util/SearchTest.java
public class SearchTest {
@Test
public void testSearch() {
try {
String pageContent = "There are certain queer times and occasions "
+ "in this strange mixed affair we call life when a man takes "
+ "this whole universe for a vast practical joke, though "
+ "the wit thereof he but dimly discerns, and more than "
+ "suspects that the joke is at nobody's expense but his own.";
byte[] bytes = pageContent.getBytes();
ByteArrayInputStream stream = new ByteArrayInputStream(bytes);
// search
Search search = new Search(stream, "practical joke", "1");
Search.LOGGER.setLevel(Level.OFF);
search.setSurroundingCharacterCount(10);
search.execute();
assertFalse(search.errored());
List<Match> matches = search.getMatches();
assertNotNull(matches);
assertTrue(matches.size() >= 1);
Chapter 10. Streamlining Your Tests • 192
report erratum  •  discuss


