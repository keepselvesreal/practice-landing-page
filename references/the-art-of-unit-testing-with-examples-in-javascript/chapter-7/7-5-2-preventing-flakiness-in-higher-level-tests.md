# 7.5.2 Preventing flakiness in higher-level tests (pp.163-164)

---
**Page 163**

163
7.5
Dealing with flaky tests
7.5.1
What can you do once you’ve found a flaky test?
It’s important to realize that flaky tests can be costly to an organization. You should
aim to have zero flaky tests as a long-term goal. Here are some ways to reduce the costs
associated with handling flaky tests:
Define—Agree on what “flaky” means to your organization. For example, run
your test suite 10 times without any production code changes, and count all the
tests that were not consistent in their results (i.e., ones that did not fail all 10
times or did not pass all 10 times).
Place any test deemed flaky in a special category or folder of tests that can be
run separately. I recommend removing all flaky tests from the regular delivery
build so they do not create noise, and quarantining them in their own little
pipeline temporarily. Then, go over each of the flaky tests and play my favorite
flaky game, “fix, convert, or kill”:
– Fix—Make the test not flaky by controlling its dependencies, if possible. For
example, if it requires data in the database, insert the data into the database
as part of the test. 
– Convert—Remove flakiness by converting the test into a lower-level test by
removing and controlling one or more of its dependencies. For example,
simulate a network endpoint with a stub instead of using a real one. 
– Kill—Seriously consider whether the value the test brings is enough to con-
tinue to run it and pay the maintenance costs it creates. Sometimes old flaky
tests are better off dead and buried. Sometimes they are already covered by
newer, better tests, and the old tests are pure technical debt that we can get
rid of. Sadly, many engineering managers are reluctant to remove these old
tests because of the sunken cost fallacy—there was so much effort put into
them that it would be a waste to delete them. However, at this point, it might
cost you more to keep the test than to delete it, so I recommend seriously
considering this option for many of your flaky tests. 
7.5.2
Preventing flakiness in higher-level tests
If you’re interested in preventing flakiness in higher-level tests, your best bet is to
make sure that your tests are repeatable on any environment after any deployment.
That could involve the following:
Roll back any changes your tests have made to external shared resources.
Do not depend on other tests changing external state.
Gain some control over external systems and dependencies by ensuring you
have the ability to recreate them at will (do an internet search on “infrastruc-
ture as code”), creating dummies of them that you can control, or creating spe-
cial test accounts on them and pray that they stay safe.


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


