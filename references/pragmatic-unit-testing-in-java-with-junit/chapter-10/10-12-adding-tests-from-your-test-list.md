# 10.12 Adding Tests from Your Test List (pp.206-207)

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


