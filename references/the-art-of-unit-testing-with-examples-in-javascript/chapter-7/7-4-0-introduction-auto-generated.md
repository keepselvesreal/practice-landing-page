# 7.4.0 Introduction [auto-generated] (pp.156-157)

---
**Page 156**

156
CHAPTER 7
Trustworthy tests
 This is an all-around bad test. It’s better to separate this into two or three tests,
each with its own scenario and name. This would allow us to use hardcoded inputs
and assertions and to remove any loops and if/else logic from the code. Anything
more complex causes the following problems:
The test is harder to read and understand.
The test is hard to recreate. For example, imagine a multithreaded test or a test
with random numbers that suddenly fails.
The test is more likely to have a bug or to verify the wrong thing.
Naming the test may be harder because it does multiple things.
Generally, monster tests replace original simpler tests, and that makes it harder to find
bugs in the production code. If you must create a monster test, it should be added as a
new test and not be a replacement for existing tests. Also, it should reside in a project
or folder explicitly titled to hold tests other than unit tests. I call these “integration
tests” or “complex tests” and try to keep their number to an acceptable minimum.
7.3.3
Even more logic
Logic can be found not only in tests but also in test helper methods, handwritten
fakes, and test utility classes. Remember, every piece of logic you add in these places
makes the code that much harder to read and increases the chances of a bug in a util-
ity method that your tests use. 
 If you find that you need to have complicated logic in your test suite for some rea-
son (though that’s generally something I do with integration tests, not unit tests), at
least make sure you have a couple of tests against the logic of your utility methods in
the test project. This will save you many tears down the road.
7.4
Smelling a false sense of trust in passing tests
We’ve now covered failed tests as a means of detecting tests we shouldn’t trust. What
about all those quiet, green tests we have lying all over the place? Should we trust
them? What about a test that we need to do a code review for, before it’s pushed into a
main branch? What should we look for?
 Let’s use the term “false-trust” to describe trusting a test that you really shouldn’t,
but you don’t know it yet. Being able to review tests and find possible false-trust issues
has immense value because, not only can you fix those tests yourself, you’re affecting
the trust of everyone else who’s ever going to read or run those tests. Here are some
reasons I reduce my trust in tests, even if they are passing:
The test contains no asserts.
I can’t understand the test.
Unit tests are mixed with flaky integration tests.
The test verifies multiple concerns or exit points.
The test keeps changing.


---
**Page 157**

157
7.4
Smelling a false sense of trust in passing tests
7.4.1
Tests that don’t assert anything
We all agree that a test that doesn’t actually verify that something is true or false is less
than helpful, right? Less than helpful because it also costs in maintenance time, refac-
toring, and reading time, and sometimes unnecessary noise if it needs changing due
to API changes in production code. 
 If you see a test with no asserts, consider that there may be hidden asserts in a func-
tion call. This causes a readability problem if the function is not named to explain
this. Sometimes people also write a test that exercises a piece of code simply to make
sure that the code does not throw an exception. This does have some value, and if
that’s the test you choose to write, make sure that the name of the test indicates this
with a term such as “does not throw.” To be even more specific, many test APIs support
the ability to specify that something does not throw an exception. This is how you can
do this in Jest:
expect(() => someFunction()).not.toThrow(error)
If you do have such tests, make sure there’s a very small number of them. I don’t rec-
ommend it as a standard, but only for really special cases.
 Sometimes people simply forget to write an assert due to lack of experience. Con-
sider adding the missing assert or removing the test if it brings no value. People may
also actively write tests to achieve some imagined test coverage goal set by manage-
ment. Those tests usually serve no real value except to get management off people’s
backs so they can do real work.
TIP
Code coverage shouldn’t ever be a goal on its own. It doesn’t mean
“code quality.” In fact, it often causes developers to write meaningless tests
that will cost even more time to maintain. Instead, measure “escaped bugs,”
“time to fix,” and other metrics that we’ll discuss in chapter 11.
7.4.2
Not understanding the tests
This is a huge issue, and I’ll deal with it in depth in chapter 9. There are several possi-
ble issues:
Tests with bad names
Tests that are too long or have convoluted code
Tests containing confusing variable names
Tests containing hidden logic or assumptions that cannot be understood easily
Test results that are inconclusive (neither failed nor passed)
Test messages that don’t provide enough information
If you don’t understand the test that’s failing or passing, you don’t know if you should
be worried or not.


