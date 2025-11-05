# 10.10 Test Smell: Misleading Organization (pp.203-204)

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


