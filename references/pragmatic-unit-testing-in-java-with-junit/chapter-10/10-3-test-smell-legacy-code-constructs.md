# 10.3 Test Smell: Legacy Code Constructs (pp.193-194)

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


