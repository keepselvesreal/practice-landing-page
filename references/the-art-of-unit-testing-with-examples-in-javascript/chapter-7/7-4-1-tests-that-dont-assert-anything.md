# 7.4.1 Tests that don’t assert anything (pp.157-157)

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


