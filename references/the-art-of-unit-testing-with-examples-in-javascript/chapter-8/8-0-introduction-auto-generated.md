# 8.0 Introduction [auto-generated] (pp.165-166)

---
**Page 165**

165
Maintainability
Tests can enable us to develop faster, unless they make us go slower due to all the
changes needed. If we can avoid changing existing tests when we change produc-
tion code, we can start to hope that our tests are helping rather than hurting our
bottom line. In this chapter, we’ll focus on the maintainability of tests.
 Unmaintainable tests can ruin project schedules and are often set aside when
the project is put on a more aggressive schedule. Developers will simply stop main-
taining and fixing tests that take too long to change or that need to change often as
the result of very minor production code changes. 
 If maintainability is a measure of how often we are forced to change tests, we’d
like to minimize the number of times that happens. This forces us to ask these
questions if we ever want to get down to the root causes:
When do we notice that a test fails and therefore might require a change?
Why do tests fail?
This chapter covers
Root causes of failing tests
Common avoidable changes to test code
Improving the maintainability of tests that aren’t 
currently failing


---
**Page 166**

166
CHAPTER 8
Maintainability
Which test failures force us to change the test?
When do we choose to change a test even if we are not forced to?
This chapter presents a series of practices related to maintainability that you can use
when doing test reviews.
8.1
Changes forced by failing tests
A failing test is usually the first sign of potential trouble for maintainability. Of course,
we could have found a real bug in production code, but when that’s not the case, what
other reasons do tests have to fail? I’ll refer to genuine failures as true failures, and fail-
ures that happen for reasons other than finding a bug in the underlying production
code as false failures.
 If we wanted to measure test maintainability, we could start by measuring the num-
ber of false test failures, and the reason for each failure, over time. We already dis-
cussed one such reason in chapter 7: when a test contains a bug. Let’s now discuss
other possible reasons for false failures. 
8.1.1
The test is not relevant or conflicts with another test
A conflict may arise when the production code introduces a new feature that’s in
direct conflict with one or more existing tests. Instead of the test discovering a bug, it
may discover conflicting or new requirements. There might also be a passing test that
targets the new expectation for how the production code should work. 
 Either the existing failing test is no longer relevant, or the new requirement is
wrong. Assuming that the requirement is correct, you can probably go ahead and
delete the no-longer-relevant test.
 Note that there’s a common exception to the “remove the test” rule: when you’re
working with feature toggles. We’ll touch on feature toggles in chapter 10 when we dis-
cuss testing strategies.
8.1.2
Changes in the production code’s API
A test can fail if the production code under test changes so that a function or object
being tested now needs to be used differently, even though it may still have the same
functionality. Such false failures fall in the bucket of “let’s avoid this as much as possible.”
 Consider the PasswordVerifier class in listing 8.1, which requires two constructor
parameters: 
An array of rules (each is a function that takes an input and returns a Boolean)
An ILogger interface
export class PasswordVerifier {
    ...
    constructor(rules: ((input) => boolean)[], logger: ILogger) {
        this._rules = rules;
Listing 8.1
A Password Verifier with two constructor parameters


