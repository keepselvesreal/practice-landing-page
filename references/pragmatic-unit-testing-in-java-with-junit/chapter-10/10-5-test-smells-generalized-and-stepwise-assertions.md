# 10.5 Test Smells: Generalized and Stepwise Assertions (pp.195-197)

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


---
**Page 196**

The following part of the test starts with a statement that appears to be the
act step—a call to search.getMatches():
utj3-refactor-tests/03/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertTrue(matches.size() >= 1);
var match = matches.get(0);
assertEquals("practical joke", match.searchString());
assertEquals("or a vast practical joke, though t",
match.surroundingContext());
The hint that search.getMatches represents the act step is that it’s followed
immediately by four lines of assertion-related code that appears to check the
list of matches returned by search.getMatches(). These lines require stepwise
reading. Here is a quick attempt at paraphrasing them:
• Ensure there’s at least one match
• Get the first match
• Ensure that its search string is “practical joke”
• Ensure that its surrounding context is some longer string
The first statement—assertTrue(matches.size() >= 1—appears to be an unnecessar-
ily generalized assertion. A quick scan of the Melville content (declared in the
arrange step) reveals that the search string "practical joke" appears once and
exactly once in the test.
Most tests should make precise assertions, usually with assertEquals. You are
creating the tests—you can set them up to be precise. To test a one-based
case (search results find a single match), create content with exactly one
match for the given search string and then assert that the one match exists.
In this case, you don’t need to use >=. You could replace that with a precise
comparison: assertEquals(1, matches.size()). But you have an even better resolution.
The test tediously takes four lines to verify what seems to be a single concept:
that the list of matches contains a single match object, initialized with a
specific search string and surrounding context. Java supports declaring an
initialized list, which lets you simplify the test to a single-statement assert:
utj3-refactor-tests/04/src/test/java/util/SearchTest.java
var matches = search.getMatches();
assertEquals(List.of(
new Match("1",
"practical joke",
"or a vast practical joke, though t")),
matches);
Chapter 10. Streamlining Your Tests • 196
report erratum  •  discuss


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


