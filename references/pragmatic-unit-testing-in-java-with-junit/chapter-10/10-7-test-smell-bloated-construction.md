# 10.7 Test Smell: Bloated Construction (pp.199-200)

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


