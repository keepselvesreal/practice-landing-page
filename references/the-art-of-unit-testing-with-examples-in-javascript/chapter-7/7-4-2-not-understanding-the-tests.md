# 7.4.2 Not understanding the tests (pp.157-158)

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


---
**Page 158**

158
CHAPTER 7
Trustworthy tests
7.4.3
Mixing unit tests and flaky integration tests
They say that one rotten apple spoils the bunch. The same is true for flaky tests
mixed in with nonflaky tests. Integration tests are much more likely to be flaky than
unit tests because they have more dependencies. If you find that you have a mix of
integration and unit tests in the same folder or test execution command, you should
be suspicious.
 Humans like to take the path of least resistance, and it’s no different when it comes
to coding. Suppose that a developer runs all the tests and one of them fails—if there’s
a way to blame a missing configuration or a network issue instead of spending time
investigating and fixing a real problem, they will. That’s especially true if they’re under
serious time pressure or they’re overcommitted to delivering things they’re already
late on.
 The easiest thing is to accuse any failing test of being a flaky test. Because flaky and
nonflaky tests are mixed up with each other, that’s a simple thing to do, and it’s a good
way to ignore the issue and work on something more fun. Because of this human fac-
tor, it’s best to remove the option to blame a test for being flaky. What should you do
to prevent this? Aim to have a safe green zone by keeping your integration and unit tests
in separate places.
 A safe green test area should contain only nonflaky, fast tests, where developers
know that they can get the latest code version, they can run all the tests in that name-
space or folder, and the tests should all be green (given no changes to production
code). If some tests in the safe green zone don’t pass, a developer is much more likely
to be concerned.
 An added benefit to this separation is that developers are more likely to run the
unit tests more often, now that the run time is faster without the integration tests. It’s
better to have some feedback than no feedback, right? The automated build pipeline
should take care of running any of the “missing” feedback tests that developers can’t
or won’t run on their local machines.
7.4.4
Testing multiple exit points
An exit point (I’ll also refer to it as a concern) is explained in chapter 1. It’s a single end
result from a unit of work: a return value, a change to system state, or a call to a third-
party object.
 Here’s a simple example of a function that has two exit points, or two concerns. It
both returns a value and triggers a passed-in callback function:
const trigger = (x, y, callback) => {
  callback("I'm triggered");
  return x + y;
};
We could write a test that checks both of these exit points at the same time.
 


