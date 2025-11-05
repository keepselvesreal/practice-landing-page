# 7.2.0 Introduction [auto-generated] (pp.150-151)

---
**Page 150**

150
CHAPTER 7
Trustworthy tests
two pillars fall pretty quickly. Maintaining tests becomes harder, and you can’t
trust them anymore because you don’t understand them.
This chapter and the next two present a series of practices related to each of these pil-
lars that you can use when doing test reviews. Together, the three pillars ensure your
time is well used. Drop one of them, and you run the risk of wasting everyone’s time.
 Trust is the first of the three pillars that I like to evaluate good unit tests on, so it’s
fitting that we start with it. If we don’t trust the tests, what’s the point in running
them? What’s the point in fixing them or fixing the code if they fail? What’s the point
of maintaining them? 
7.1
How to know you trust a test
What does “trust” mean for a software developer in the context of a test? Perhaps it’s
easier to explain based on what we do or don’t do when a test fails or passes. 
 You might not trust a test if
It fails and you’re not worried (you believe it’s a false positive).
You feel like it’s fine to ignore the results of this test, either because it passes
every once in a while or because you feel it’s not relevant or buggy. 
It passes and you are worried (you believe it’s a false negative).
You still feel the need to manually debug or test the software “just in case.”
You might trust the test if
The test fails and you’re genuinely worried that something broke. You don’t
move on, assuming the test is wrong.
The test passes and you feel relaxed, not feeling the need to test or debug
manually.
In the next few sections, we’ll look at test failures as a way to identify untrustworthy tests,
and we’ll look at passing tests’ code and see how to detect untrustworthy test code.
Finally, we’ll cover a few generic practices that can enhance trustworthiness in tests.
7.2
Why tests fail
Ideally, your tests (any tests, not just unit tests) should only be failing for a good reason.
That good reason is, of course, that a real bug was uncovered in the underlying pro-
duction code. 
 Unfortunately, tests can fail for a multitude of reasons. We can assume that a test
failing for any reason other than that one good reason should trigger an “untrust-
worthy” warning, but not all tests fail the same way, and recognizing the reasons tests
may fail can help us build a roadmap for what we’d like to do in each case.
 Here are some reasons that tests fail:
A real bug has been uncovered in the production code
A buggy test gives a false failure
The test is out of date due to a change in functionality


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


