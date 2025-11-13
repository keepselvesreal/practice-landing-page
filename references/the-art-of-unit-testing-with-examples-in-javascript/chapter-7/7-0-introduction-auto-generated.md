# 7.0 Introduction [auto-generated] (pp.149-150)

---
**Page 149**

149
Trustworthy tests
No matter how you organize your tests, or how many you have, they’re worth very
little if you can’t trust them, maintain them, or read them. The tests that you write
should have three properties that together make them good:
Trustworthiness—Developers will want to run trustworthy tests, and they’ll
accept the test results with confidence. Trustworthy tests don’t have bugs,
and they test the right things. 
Maintainability—Unmaintainable tests are nightmares because they can ruin
project schedules, or they may be sidelined when the project is put on a
more aggressive schedule. Developers will simply stop maintaining and fix-
ing tests that take too long to change or that need to change often on very
minor production code changes.
Readability—This refers not only to being able to read a test but also figuring
out the problem if the test seems to be wrong. Without readability, the other
This chapter covers
How to know you trust a test
Detecting untrustworthy failing tests
Detecting untrustworthy passing tests
Dealing with flaky tests


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


