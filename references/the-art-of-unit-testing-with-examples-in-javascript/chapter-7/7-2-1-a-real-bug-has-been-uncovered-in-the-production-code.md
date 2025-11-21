# 7.2.1 A real bug has been uncovered in the production code (pp.151-151)

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


