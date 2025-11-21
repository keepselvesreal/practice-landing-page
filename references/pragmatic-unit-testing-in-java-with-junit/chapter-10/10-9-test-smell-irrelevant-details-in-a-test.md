# 10.9 Test Smell: Irrelevant Details in a Test (pp.202-203)

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


