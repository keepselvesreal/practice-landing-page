# 7.2.3 The test is out of date due to a change in functionality (pp.152-152)

---
**Page 152**

152
CHAPTER 7
Trustworthy tests
is now passing, you’re done. You’ve now seen the test passing when it should and fail-
ing when it should. Commit the code and move on.
 If the test is still failing, it might have another bug. Repeat the whole process again
until you verify that the test fails and passes when it should. If the test is still failing, you
might have come across a real bug in production code. In which case, good for you!
HOW TO AVOID BUGGY TESTS IN THE FUTURE
One of the best ways I know to detect and prevent buggy tests is to write your code in a
test-driven manner. I explained a bit about this technique in chapter 1 of this book. I
also practice this technique in real life.
 Test-driven development (TDD) allows us to see both states of a test: both that it
fails when it should (that’s the initial state we start in) and that it passes when it should
(when the production code under test is written to make the test pass). If the test con-
tinues to fail, we’ve found a bug in the production code. If the test starts out passing,
we have a bug in the test. 
 Another great way to reduce the likelihood of bugs in tests is to remove logic from
them. More on this in section 7.3.
7.2.3
The test is out of date due to a change in functionality
A test can fail if it’s no longer compatible with the current feature that’s being tested.
Say you have a login feature, and in an earlier version, you needed to provide a user-
name and a password to log in. In the new version, a two-factor authentication scheme
replaced the old login. The existing test will start failing because it’s not providing the
right parameters to the login functions.
WHAT CAN YOU DO NOW?
You now have two options:
Adapt the test to the new functionality.
Write a new test for the new functionality, and remove the old test because it has
now become irrelevant.
AVOIDING OR PREVENTING THIS IN THE FUTURE
Things change. I don’t think it’s possible to not have out-of-date tests at some point in
time. We’ll deal with change in the next chapter, relating to the maintainability of
tests and how well tests can handle changes in the application. 
7.2.4
The test conflicts with another test
Let’s say you have two tests: one of them is failing and one is passing. Let’s also say they
cannot pass together. You’ll usually only see the failing test, because the passing one is,
well, passing.
 For instance, a test may fail because it suddenly conflicts with a new behavior. On
the other hand, a conflicting test may expect a new behavior but doesn’t find it. The
simplest example is when the first test verifies that calling a function with two parame-
ters produces “3,” whereas the second test expects the same function to produce “4.”


