# Streamlining Your Tests (pp.189-211)

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


---
**Page 193**

Match match = matches.get(0);
assertEquals("practical joke", match.searchString());
assertEquals("or a vast practical joke, though t",
match.surroundingContext());
stream.close();
// negative
URLConnection connection =
new URL("http://bit.ly/15sYPA7").openConnection();
InputStream inputStream = connection.getInputStream();
search = new Search(
inputStream, "smelt", "http://bit.ly/15sYPA7");
search.execute();
assertEquals(0, search.getMatches().size());
stream.close();
} catch (Exception e) {
e.printStackTrace();
fail("exception thrown in test" + e.getMessage());
}
}
}
(Text in pageContent by Herman Melville from Moby Dick.)
Match is only a Java record with the three String fields: searchTitle, searchString,
and surroundingContext.
The test name, testSearch, doesn’t tell you anything useful. A couple of com-
ments don’t add much value either. To fully understand what’s going on,
you’ll have to read the test line by line and try to piece its steps together.
(You won’t see the Search class itself in this chapter since your focus will
solely be on cleaning up the tests for better understanding. Visit the source
distribution if you’re curious about the Search class.)
You decide to refactor testSearch while you work through understanding it,
with the goal of shaping it into one or more clear, expressive tests. You look
for various test smells—nuggets of code that emanate an odor. Odors aren’t
necessarily foul, though they can greatly diminish the readability of your
tests.
Test Smell: Legacy Code Constructs
You’ll be making several passes through the test, each with a different intent.
A quick scan of the test reveals old-school Java and JUnit, evidenced by the
lack of local variable type inferencing and the unnecessary use of public for
the class and test method. One of the best things about the newer versions
of both Java and JUnit is their ability to simplify your code.
report erratum  •  discuss
Test Smell: Legacy Code Constructs • 193


---
**Page 194**

First, make a couple of quick cleanup passes:
1.
Remove public from the test class and test methods. They are clutter.
2.
Replace local variable type names with the var type.
Here’s a snippet:
utj3-refactor-tests/02/src/test/java/util/SearchTest.java
class SearchTest {
➤
@Test
void testSearch() {
➤
try {
var pageContent = "There are certain queer times and occasions "
// ...
var bytes = pageContent.getBytes();
var stream = new ByteArrayInputStream(bytes);
//...
The elimination of a few unnecessary tokens will begin to help you focus more
on what’s relevant.
Test Smell: Unnecessary Test Code
The test testSearch() contains a few assertions, none expecting exceptions
themselves. If the test code throws an exception, a try/catch block catches it,
spews a stack trace onto System.out, and explicitly fails the test.
Unless your test expects an exception to be thrown—because you’ve explicitly
designed it to set the stage for throwing an exception—you can let other
exceptions fly. Don’t worry, JUnit traps any exceptions that explode out of
your test. When JUnit catches an unexpected exception, it marks the test as
an error, and displays the stack trace in its output.
The try/catch block surrounding all the test code adds no value. Remove it.
Modify the signature of testSearch() to indicate that it can throw an IOException:
utj3-refactor-tests/03/src/test/java/util/SearchTest.java
@Test
void testSearch() throws IOException {
var pageContent = "There are certain queer times and occasions "
// ...
var bytes = pageContent.getBytes();
var stream = new ByteArrayInputStream(bytes);
// ...
stream.close();
}
Careful editing helps your tests tell a clear story about system behaviors. And
as long as your tests pass, you can trust that story.
Chapter 10. Streamlining Your Tests • 194
report erratum  •  discuss


---
**Page 195**

Comments represent a failure to let the code tell the story. For now, delete
the two comments in testSearch.
Tests provide trustworthy documentation on the unit behaviors
of your system.
About eight statements into the test method, you notice a not-null assert—an
assertion that verifies that a value is not null:
utj3-refactor-tests/02/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertNotNull(matches);
assertTrue(matches.size() >= 1);
The first line assigns the result of search.getMatches() to the matches local variable. The
second statement asserts that matches is not a null value. The final line verifies
that the size of matches is at least 1.
Checking that a variable isn’t null before dereferencing it is a good thing, right?
In production code, perhaps. In this test, the call to assertNotNull is again clutter.
It adds no value: if matches is actually null, the call to matches.size() generates a
NullPointerException. JUnit traps this exception and errors the test. You’re notified
of the error, and it’s no harder to figure out what the problem is.
Like the try/catch block, calling assertNotNull adds no value. Remove it:
utj3-refactor-tests/03/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertTrue(matches.size() >= 1);
That’s one fewer line of test to wade through!
Test Smells: Generalized and Stepwise Assertions
A well-structured test distills the interaction with the system to three steps:
arranging the data, acting on the system, and asserting on the results (see
Scannability: Arrange—Act—Assert, on page 18). Although the test requires
detailed code to accomplish each of these steps, you can improve understand-
ing by organizing those details into abstractions—code elements that maximize
the essential concepts and hide the unnecessary details.
Good tests provide examples of how clients interact with the
system.
report erratum  •  discuss
Test Smells: Generalized and Stepwise Assertions • 195


---
**Page 196**

The following part of the test starts with a statement that appears to be the
act step—a call to search.getMatches():
utj3-refactor-tests/03/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertTrue(matches.size() >= 1);
var match = matches.get(0);
assertEquals("practical joke", match.searchString());
assertEquals("or a vast practical joke, though t",
match.surroundingContext());
The hint that search.getMatches represents the act step is that it’s followed
immediately by four lines of assertion-related code that appears to check the
list of matches returned by search.getMatches(). These lines require stepwise
reading. Here is a quick attempt at paraphrasing them:
• Ensure there’s at least one match
• Get the first match
• Ensure that its search string is “practical joke”
• Ensure that its surrounding context is some longer string
The first statement—assertTrue(matches.size() >= 1—appears to be an unnecessar-
ily generalized assertion. A quick scan of the Melville content (declared in the
arrange step) reveals that the search string "practical joke" appears once and
exactly once in the test.
Most tests should make precise assertions, usually with assertEquals. You are
creating the tests—you can set them up to be precise. To test a one-based
case (search results find a single match), create content with exactly one
match for the given search string and then assert that the one match exists.
In this case, you don’t need to use >=. You could replace that with a precise
comparison: assertEquals(1, matches.size()). But you have an even better resolution.
The test tediously takes four lines to verify what seems to be a single concept:
that the list of matches contains a single match object, initialized with a
specific search string and surrounding context. Java supports declaring an
initialized list, which lets you simplify the test to a single-statement assert:
utj3-refactor-tests/04/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertEquals(List.of(
new Match("1",
"practical joke",
"or a vast practical joke, though t")),
matches);
Chapter 10. Streamlining Your Tests • 196
report erratum  •  discuss


---
**Page 197**

Anywhere you find two or more lines of stepwise assertion code that asserts
a single concept, distill them to a single, clear statement in the test. Sometimes a
short helper method is all it takes. If you use AssertJ, you can create a custom
matcher that provides a concise assertion.
Amplify abstractions in your test. Hide the implementation specifics elsewhere.
In the second chunk of test code, near the end of the method, you spot
another small opportunity for introducing an abstraction. The final assertion
(highlighted) compares the size of search matches to 0:
utj3-refactor-tests/04/src/test/java/util/SearchTest.java
@Test
void testSearch() throws IOException {
// ...
search.execute();
assertEquals(0, search.getMatches().size());
➤
stream.close();
}
The missing abstraction is the concept of emptiness. Altering the assertion
reduces the extra mental overhead needed to understand the size comparison:
utj3-refactor-tests/05/src/test/java/util/SearchTest.java
search.execute();
assertTrue(search.getMatches().isEmpty());
➤
stream.close();
Every small amount of mental clutter adds up. A system with never-ending
clutter wears you down, much as road noise builds to create further fatigue
on a long car trip.
Test Smell: Missing Abstractions
A well-abstracted test emphasizes everything that’s important to understanding
it and de-emphasizes anything that’s not. Any data used in a test should help
tell its story.
Sometimes, you’re forced to supply data to get code to compile, even though
that data is irrelevant to the test at hand. For example, a method might take
additional arguments that have no impact on the test.
Your test contains some magic literals that aren’t at all clear:
utj3-refactor-tests/05/src/test/java/util/SearchTest.java
var search = new Search(stream, "practical joke", "1");
report erratum  •  discuss
Test Smell: Missing Abstractions • 197


---
**Page 198**

And:
utj3-refactor-tests/05/src/test/java/util/SearchTest.java
assertEquals(List.of(
new Match("1",
"practical joke",
"or a vast practical joke, though t")),
matches);
Perhaps these were magically conjured by a wizard who chose to keep their
meanings arcane.
You’re not sure what the "1" string represents, so you navigate into the con-
structors for Search and Match. You discover that "1" is a search title, a field
whose value appears irrelevant right now.
Including the "1" literal raises unnecessary questions. What does it represent?
How, if at all, is it relevant to the results of the test?
At least one other magic literal exists. The second call to the Search constructor
contains a URL as the title argument:
utj3-refactor-tests/05/src/test/java/util/SearchTest.java
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
var inputStream = connection.getInputStream();
search = new Search(
inputStream, "smelt", "http://bit.ly/15sYPA7");
➤
At first glance, it appears that the URL has a correlation with the URL passed
to the URL constructor two statements earlier. But digging reveals that no real
correlation exists.
Developers waste time when they must dig around to find answers. You’ll
help them by introducing an intention-revealing constant. Replace the con-
fusing URL and the "1" magic literal with the A_TITLE constant, which suggests
a title with any value.
Here’s the latest version of the test, highlighting lines with the new abstraction:
utj3-refactor-tests/06/src/test/java/util/SearchTest.java
class SearchTest {
static final String A_TITLE = "1";
➤
@Test
void testSearch() throws IOException {
var pageContent = "There are certain queer times and occasions "
+ "in this strange mixed affair we call life when a man takes "
+ "this whole universe for a vast practical joke, though "
+ "the wit thereof he but dimly discerns, and more than "
+ "suspects that the joke is at nobody's expense but his own.";
Chapter 10. Streamlining Your Tests • 198
report erratum  •  discuss


---
**Page 199**

var bytes = pageContent.getBytes();
var stream = new ByteArrayInputStream(bytes);
var search = new Search(stream, "practical joke", A_TITLE);
➤
Search.LOGGER.setLevel(Level.OFF);
search.setSurroundingCharacterCount(10);
search.execute();
assertFalse(search.errored());
var matches = search.getMatches();
assertEquals(List.of(
new Match(A_TITLE,
➤
"practical joke",
"or a vast practical joke, though t")),
matches);
stream.close();
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
var inputStream = connection.getInputStream();
search = new Search(
inputStream, "smelt", A_TITLE);
➤
search.execute();
assertTrue(search.getMatches().isEmpty());
stream.close();
}
}
You could have named the constant ANY_TITLE or ARBITRARY_TITLE. Or, you might
have used an empty string, which suggests data that you don’t care about
(though sometimes the distinction between an empty string and a nonempty
string is relevant).
Test Smell: Bloated Construction
The Search class requires you to pass an InputStream on a Search object through
its constructor. Your test builds an InputStream in two places. The first construc-
tion requires three statements:
utj3-refactor-tests/06/src/test/java/util/SearchTest.java
var pageContent = "There are certain queer times and occasions "
+ "in this strange mixed affair we call life when a man takes "
+ "this whole universe for a vast practical joke, though "
+ "the wit thereof he but dimly discerns, and more than "
+ "suspects that the joke is at nobody's expense but his own.";
var bytes = pageContent.getBytes();
var stream = new ByteArrayInputStream(bytes);
The test contains implementation detail specifics involving extracting bytes from
a string and then creating a ByteArrayInputStream. That’s stuff you don’t need to
report erratum  •  discuss
Test Smell: Bloated Construction • 199


---
**Page 200**

see to understand the test, and it represents a missing abstraction. Introduce
a helper method that creates an InputStream on a provided string of text:
utj3-refactor-tests/07/src/test/java/util/SearchTest.java
class SearchTest {
// ...
@Test
void testSearch() throws IOException {
var stream = streamOn("There are certain queer times and occasions "
➤
+ "in this strange mixed affair we call life when a man "
+ "takes this whole universe for a vast practical joke, "
+ "though the wit thereof he but dimly discerns, and more "
+ "than suspects that the joke is at nobody's expense but his own.");
var search = new Search(stream, "practical joke", A_TITLE);
// ...
}
private ByteArrayInputStream streamOn(String text) {
➤
return new ByteArrayInputStream(text.getBytes());
➤
}
➤
}
Morphing arbitrary detail into clear declarations is gradually improving the test.
Test Smell: Multiple Assertions
Your long test appears to represent two distinct cases. The first demonstrates
finding a search result, and the second represents finding no match. The
blank line provides a clear dividing point:
utj3-refactor-tests/07/src/test/java/util/SearchTest.java
@Test
void testSearch() throws IOException {
var stream = streamOn("There are certain queer times and occasions "
// ...
var search = new Search(stream, "practical joke", A_TITLE);
Search.LOGGER.setLevel(Level.OFF);
search.setSurroundingCharacterCount(10);
search.execute();
assertFalse(search.errored());
var matches = search.getMatches();
assertEquals(List.of(
new Match(A_TITLE,
"practical joke",
"or a vast practical joke, though t")),
matches);
stream.close();
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
var inputStream = connection.getInputStream();
Chapter 10. Streamlining Your Tests • 200
report erratum  •  discuss


---
**Page 201**

search = new Search(
inputStream, "smelt", A_TITLE);
search.execute();
assertTrue(search.getMatches().isEmpty());
stream.close();
}
Split the test into two test methods, coming up with a better name for each
(the code won’t compile until both test names are distinct). Also, take a
moment to rename the test class to ASearch.
Verifying only one behavior per test facilitates concise test naming.
The resulting two test methods:
utj3-refactor-tests/08/src/test/java/util/ASearch.java
@Test
void returnsMatchesWithSurroundingContext() throws IOException {
var stream = streamOn("There are certain queer times and occasions "
// ...
var search = new Search(stream, "practical joke", A_TITLE);
Search.LOGGER.setLevel(Level.OFF);
search.setSurroundingCharacterCount(10);
search.execute();
assertFalse(search.errored());
var matches = search.getMatches();
assertEquals(List.of(
new Match(A_TITLE,
"practical joke",
"or a vast practical joke, though t")),
matches);
stream.close(); // delete me
➤
}
@Test
void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
var inputStream = connection.getInputStream();
var search = new Search(inputStream, "smelt", A_TITLE);
➤
search.execute();
assertTrue(search.getMatches().isEmpty());
inputStream.close();
➤
}
The listing shows fixes to two compile failures that occurred when splitting.
First, since the search variable was re-used in the original test, its use in the
second test now needs a type declaration. The var type will suffice.
report erratum  •  discuss
Test Smell: Multiple Assertions • 201


---
**Page 202**

Also, the second test’s last line (which closes the stream) wasn’t compiling.
Amusingly, it turns out that the combined mess of a single test was calling
close twice on stream, and not at all on inputStream. Changing the last line to
inputStream.close() fixed the problem.
You can delete the line that closes stream in the first test. There’s no need to
close a ByteArrayInputStream (least of all in a test). (The other close needs to occur
to avoid connection and resource issues for other tests or for itself if run
multiple times.)
Next, use Java’s try-with-resources feature to ensure that inputStream gets
closed. You can then delete the inputStream.close() statement for good:
utj3-refactor-tests/09/src/test/java/util/ASearch.java
@Test
void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
try (var inputStream = connection.getInputStream()) {
var search = new Search(inputStream, "smelt", A_TITLE);
search.execute();
assertTrue(search.getMatches().isEmpty());
}
}
Test Smell: Irrelevant Details in a Test
Your tests should execute cleanly, showing only a summary with the passing
and failing tests. Don’t allow your test run to be littered with dozens or perhaps
hundreds and more lines of log messages, “expected” exception stack traces,
and System.out.println clutter.
Ensure test execution does not pollute console output.
When your test summary is clean, any new exceptions will stand out like a
sore thumb rather than get lost in a sea of stack traces. You’ll also easily spot
any new console output that you’ve temporarily added.
In the prior section, you split one larger test into two. Now, when you run
your tests, you’ll notice some logging output:
Mar 29, 2024 1:35:50 PM util.Search search
INFO: searching matches for pattern:smelt
Chapter 10. Streamlining Your Tests • 202
report erratum  •  discuss


---
**Page 203**

The first test contains the following line, but the second test does not:
Search.LOGGER.setLevel(Level.OFF);
Suppressing logger output when the second test runs would be as easy as
adding the setLevel call to the second test. But that’s the wrong place for it.
While only a single line, the code needed to suppress logging is a distraction
that adds no meaning to any test. De-emphasize the setLevel call by moving it
to a @BeforeEach method.
utj3-refactor-tests/09/src/test/java/util/ASearch.java
@BeforeEach
void suppressLogging() {
Search.LOGGER.setLevel(Level.OFF);
}
// ...
Looking for further irrelevant details, you ponder the assertion in the first
test that ensures the search has not errored:
utj3-refactor-tests/09/src/test/java/util/ASearch.java
var search = new Search(stream, "practical joke", A_TITLE);
search.setSurroundingCharacterCount(10);
search.execute();
assertFalse(search.errored());
➤
var matches = search.getMatches();
assertEquals(List.of(
// ...
The assertion appears valid—a second postcondition of running a search.
But it hints at a missing test case: if there’s an assertFalse, an assertTrue should
exist. For now, delete the assertion and add it to your “todo” test list (see
Covering Other Cases: Creating a Test List, on page 24). You’ll return to add
a couple of new tests once you’ve streamlined all the test code.
Take care when moving details to @BeforeEach or helper methods. Don’t remove
information from a test that’s essential to understanding it.
Good tests contain all the information needed to understand them.
Poor tests send you on scavenger hunts.
Test Smell: Misleading Organization
Speed up cognition by making the act, arrange, and assert parts of a test (see
Scannability: Arrange—Act—Assert, on page 18) explicit. Arrows in the follow-
ing listing show the blank lines to insert around the act step:
report erratum  •  discuss
Test Smell: Misleading Organization • 203


---
**Page 204**

utj3-refactor-tests/10/src/test/java/util/ASearch.java
@Test
void returnsMatchesWithSurroundingContext() {
var stream = streamOn("There are certain queer times and occasions "
// ...
var search = new Search(stream, "practical joke", A_TITLE);
search.setSurroundingCharacterCount(10);
➤
search.execute();
➤
var matches = search.getMatches();
assertEquals(List.of(
new Match(A_TITLE,
"practical joke",
"or a vast practical joke, though t")),
matches);
}
@Test
void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
var connection =
new URL("http://bit.ly/15sYPA7").openConnection();
try (var inputStream = connection.getInputStream()) {
var search = new Search(inputStream, "smelt", A_TITLE);
➤
search.execute();
➤
assertTrue(search.getMatches().isEmpty());
}
}
You’re getting close. Time for a final pass against the two tests!
Test Smell: Implicit Meaning
The big question every test must clearly answer: why does it expect the result
it does? Developers must be able to correlate any assertions with the arrange
step. Unclear correlation forces developers to wade through code for meaning.
The returnsMatchesWithSurroundingContext test searches for practical joke in a long
string, expecting one match. A patient reader could determine where practical
joke appears and then figure out that ten characters before it and ten charac-
ters after it represent the string:
"or a vast practical joke, though t"
But making developers dig for understanding is rude. Make things explicit
by choosing better test data. Change the input stream to contain a small
amount of text. Then, change the content so that the surrounding context
information doesn’t need to be explicitly counted:
Chapter 10. Streamlining Your Tests • 204
report erratum  •  discuss


---
**Page 205**

utj3-refactor-tests/11/src/test/java/util/ASearch.java
@Test
void returnsMatchesWithSurroundingContext() {
var stream = streamOn("""
➤
rest of text here
➤
1234567890search term1234567890
➤
more rest of text""");
➤
var search = new Search(stream, "search term", A_TITLE);
➤
search.setSurroundingCharacterCount(10);
search.execute();
var matches = search.getMatches();
assertEquals(List.of(
new Match(A_TITLE,
"search term",
➤
"1234567890search term1234567890")),
➤
matches);
}
Now, it’s fairly easy to see why a surrounding character count of 10 produces
the corresponding context results in the Match object.
You have no end of ways to improve the correlation across a test. Meaningful
constants, better variable names, better data, and sometimes even doing
small calculations in the test can help. Use your creativity here!
Diversion: Speeding Up Your Tests
As you incrementally shape the design of your tests, you’ll be distracted by
other opportunities to improve them. You can divert to address those oppor-
tunities, or you can add a reminder to do so.
Let’s use returnsNoMatchesWhenSearchTextNotFound to take a quick detour and speed
up the second test. It works against a live URL’s input stream, making it slow.
Since your first test is a fast unit test that verifies the happy path case, you
want a similarly fast test to cover the unhappy path case. (You might want
to retain the live test for integration testing purposes.)
Initialize the stream field to contain a small bit of arbitrary text. To help make
the test’s circumstance clear, search for "text that ain't gonna match":
utj3-refactor-tests/11/src/test/java/util/ASearch.java
@Test
void returnsNoMatchesWhenSearchTextNotFound() {
➤
var stream = streamOn("text that ain't gonna match");
➤
var search = new Search(stream, "missing search term", A_TITLE);
➤
report erratum  •  discuss
Test Smell: Implicit Meaning • 205


---
**Page 206**

search.execute();
assertTrue(search.getMatches().isEmpty());
}
Your test no longer throws a checked exception. Remove the throws clause
from the test’s signature.
Adding Tests from Your Test List
In Test Smell: Irrelevant Details in a Test, on page 202, you added a couple of
needed tests to your test list. Now that you’ve whittled down your messy initial
test into two sleek, clear tests, you should find it relatively easy to add a
couple of new tests.
First, write a test that demonstrates how a completed search returns false for
the errored() query:
utj3-refactor-tests/11/src/test/java/util/ASearch.java
@Test
void erroredReturnsFalseWhenReadSucceeds() {
var stream = streamOn("");
var search = new Search(stream, "", "");
search.execute();
assertFalse(search.errored());
}
Then, test the case where accessing the input stream throws an exception:
utj3-refactor-tests/11/src/test/java/util/ASearch.java
@Test
public void erroredReturnsTrueWhenUnableToReadStream() {
var stream = createStreamThrowingErrorWhenRead();
var search = new Search(stream, "", "");
search.execute();
assertTrue(search.errored());
}
private InputStream createStreamThrowingErrorWhenRead() {
return new InputStream() {
@Override
public int read() throws IOException { throw new IOException(); }
};
}
Time spent to add the new tests: less than a few minutes each.
Chapter 10. Streamlining Your Tests • 206
report erratum  •  discuss


---
**Page 207**

Summary
You ended up with four sleek, refactored tests. A developer can understand
the goal of each test through its name, which provides a generalized summary
of behavior. They can see how that behavior plays out by reading the example
within the test. Arrange—Act—Assert (AAA) guides them immediately to the
act step so that they can see how the code being verified gets executed. They
can reconcile the asserts against the test name’s description of behavior.
Finally, if needed, they can review the arrange step to understand how it puts
the system in the proper state to be tested.
The tests are scannable. A developer can rapidly find and digest each test
element (name, arrange, act, and assert) they’re interested in. The needed
comprehension can happen in seconds rather than minutes. Remember also
that readily understood tests—descriptions of unit behavior—can save even
hours of time required to understand production code.
Seeking to understand your system through its tests motivates
you to keep them as clean as they should be.
It only takes minutes to clean up tests enough to save extensive future
amounts of comprehension time.
You now have a complete picture of what you must do in the name of design:
refactor your production code for clarity and conciseness, refactor your pro-
duction code to support more flexibility in design, design your system to
support mocking of dependency challenges, and refactor your tests to minimize
maintenance and maximize understanding.
You’re ready to move on to the final part of this book, a smorgasbord of
additional topics related to unit testing.
report erratum  •  discuss
Summary • 207


---
**Page 209**

Part IV
Bigger Topics Around Unit Testing
Writing tests is but a part of a larger experience.
Explore unit testing in various modern and relevant
contexts: test-driven development (TDD), project
teams, and AI-driven development.


---
**Page 211**

CHAPTER 11
Advancing with Test-Driven
Development (TDD)
You’re now armed with what you’ll need to know about straight-up unit
testing in Java. In this part, you’ll learn about three significant topics:
• Using TDD to flip the concept of unit testing from test-after to test-driven
• Considerations for unit testing within a project team
• Using AI tooling to drive development, assisted by unit tests
You’ll start with a meaty example of how to practice TDD.
It’s hard to write unit tests for some code. Such “difficult” code grows partly
from a lack of interest in unit testing. In contrast, the more you consider how
to unit test the code you write, the more you’ll end up with easier-to-test code.
(“Well, duh!” responds our reluctant unit tester Joe.)
With TDD, you think first about the outcome you expect for the code you’re
going to write. Rather than slap out some code and then figure out how to
test it (or even what it should do), you first capture the expected outcome in
a test. You then code the behavior needed to meet that outcome. This reversed
approach might seem bizarre or even impossible, but it’s the core element
in TDD.
With TDD, you wield unit tests as a tool to help you shape and control your
systems. Rather than a haphazard practice where you sometimes write unit
tests after you write code, and sometimes you don’t, describing outcomes and
verifying code through unit tests becomes your central focus.
You will probably find the practice of TDD dramatically different than
anything you’ve experienced in software development. The way you build
report erratum  •  discuss


