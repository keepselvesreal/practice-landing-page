# 10.8 Test Smell: Multiple Assertions (pp.200-202)

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


