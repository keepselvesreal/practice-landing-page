# 10.11 Test Smell: Implicit Meaning (pp.204-206)

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


