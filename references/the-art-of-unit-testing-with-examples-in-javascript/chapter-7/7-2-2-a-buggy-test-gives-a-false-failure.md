# 7.2.2 A buggy test gives a false failure (pp.151-152)

---
**Page 151**

151
7.2
Why tests fail
The test conflicts with another test
The test is flaky
Except for the first point here, all these reasons are the test telling you it should not
be trusted in its current form. Let’s go through them.
7.2.1
A real bug has been uncovered in the production code
The first reason a test will fail is when there is a bug in the production code. That’s
good! That’s why we have tests. Let’s move on to the other reasons tests fail.
7.2.2
A buggy test gives a false failure
A test will fail if the test is buggy. The production code might be correct, but that
doesn’t matter if the test itself has a bug that causes the test to fail. It could be that
you’re asserting on the wrong expected result of an exit point, or that you’re using the
system under test incorrectly. It could be that you’re setting up the context for the test
wrong or that you misunderstand what you were supposed to test. 
 Either way, a buggy test can be quite dangerous, because a bug in a test can also
cause it to pass and leave you unsuspecting of what’s really going on. We’ll talk more
about tests that don’t fail but should later in the chapter.
HOW TO RECOGNIZE A BUGGY TEST
You have a failing test, but you might have already debugged the production code and
couldn’t find any bug there. This is when you should start suspecting the failing test.
There’s no way around it. You’re going to have to slowly debug the test code. 
 Here are some potential causes of false failures:
Asserting on the wrong thing or on the wrong exit point
Injecting a wrong value into the entry point
Invoking the entry point incorrectly
It could also be some other small mistake that happens when you write code at 2 A.M.
(That’s not a sustainable coding strategy, by the way. Stop doing that.)
WHAT DO YOU DO ONCE YOU’VE FOUND A BUGGY TEST?
When you find a buggy test, don’t panic. This might be the millionth time you’ve
found one, so you might be panicking and thinking “our tests suck.” You might also be
right about that. But that doesn’t mean you should panic. Fix the bug, and run the
test to see if it now passes.
 If the test passes, don’t be happy too soon! Go to the production code and place an
obvious bug that should be caught by the newly fixed test. For example, change a
Boolean to always be true. Or false. Then run the test again, and make sure it fails. If
it doesn’t, you might still have a bug in your test. Fix the test until it can find the pro-
duction bug and you can see it fail.
 Once you are sure the test is failing for an obvious production code issue, fix the
production code issue you just made and run the test again. It should pass. If the test


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


