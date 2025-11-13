# 8.1.1 The test is not relevant or conflicts with another test (pp.166-166)

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


