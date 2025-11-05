# 10.6 Test Smell: Missing Abstractions (pp.197-199)

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


