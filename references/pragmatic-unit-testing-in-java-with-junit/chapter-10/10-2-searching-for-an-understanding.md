# 10.2 Searching for an Understanding (pp.192-193)

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


