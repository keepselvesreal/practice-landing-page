# 7.6 Summary (pp.164-165)

---
**Page 164**

164
CHAPTER 7
Trustworthy tests
On this last point, controlling external dependencies can be difficult or impossible
when using external systems managed by other companies. When that’s true, it’s
worth considering these options:
Remove some of the higher-level tests if some low-level tests already cover those
scenarios.
Convert some of the higher-level tests to a set of lower-level tests.
If you’re writing new tests, consider a pipeline-friendly testing strategy with test
recipes (such as the one I’ll explain in chapter 10).
Summary
If you don’t trust a test when it’s failing, you might ignore a real bug, and if you
don’t trust a test when it’s passing, you’ll end up doing lots of manual debug-
ging and testing. Both of these outcomes are supposed to be reduced by having
good tests, but if we don’t reduce them, and we spend all this time writing tests
that we don’t trust, what’s the point in writing them in the first place? 
Tests might fail for multiple reasons: a real bug found in production code, a bug
in the test resulting in a false failure, a test being out of date due to a change in
functionality, a test conflicting with another test, or test flakiness. Only the first
reason is a valid one. All the others tell us the test shouldn’t be trusted.
Avoid complexity in tests, such as creating dynamic expected values or duplicat-
ing logic from the underlying production code. Such complexity increases the
chances of introducing bugs in tests and the time it takes to understand them.
If a test doesn’t have any asserts, you can’t understand what's it’s doing, it runs
alongside flaky tests (even if this test itself isn’t flaky), it verifies multiple exit
points, or it keeps changing, it can’t be fully trusted.
Flaky tests are tests that fail unpredictably. The higher the level of the test, the
more real dependencies it uses, which gives us confidence in the overall sys-
tem’s correctness but results in more flakiness. To better identify flaky tests, put
them in a special category or folder that can be run separately.
To reduce test flakiness, either fix the tests, convert flaky higher-level tests into
less flaky lower-level ones, or delete them.


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


