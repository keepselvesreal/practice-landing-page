# 10.4 Test Smell: Unnecessary Test Code (pp.194-195)

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


