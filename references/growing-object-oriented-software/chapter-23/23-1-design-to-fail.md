# 23.1 Design to Fail (pp.267-268)

---
**Page 267**

Chapter 23
Test Diagnostics
Mistakes are the portals of discovery.
—James Joyce
Design to Fail
The point of a test is not to pass but to fail. We want the production code to
pass its tests, but we also want the tests to detect and report any errors that
do exist. A “failing” test has actually succeeded at the job it was designed to do.
Even unexpected test failures, in an area unrelated to where we are working, can
be valuable because they reveal implicit relationships in the code that we hadn’t
noticed.
One situation we want to avoid, however, is when we can’t diagnose a test
failure that has happened. The last thing we should have to do is crack open the
debugger and step through the tested code to ﬁnd the point of disagreement. At
a minimum, it suggests that our tests don’t yet express our requirements clearly
enough. In the worst case, we can ﬁnd ourselves in “debug hell,” with deadlines
to meet but no idea of how long a ﬁx will take. At this point, the temptation will
be high to just delete the test—and lose our safety net.
Stay Close to Home
Synchronize frequently with the source code repository—up to every few minutes—
so that if a test fails unexpectedly it won’t cost much to revert your recent changes
and try another approach.
The other implication of this tip is not to be too inhibited about dropping code and
trying again. Sometimes it’s quicker to roll back and restart with a clear head than
to keep digging.
We’ve learned the hard way to make tests fail informatively. If a failing test
clearly explains what has failed and why, we can quickly diagnose and correct
the code. Then, we can get on with the next task.
Chapter 21 addressed the static readability of tests. This chapter describes
some practices that we ﬁnd helpful to make sure the tests give us the information
we need at runtime.
267


---
**Page 268**

Small, Focused, Well-Named Tests
The easiest way to improve diagnostics is to keep each test small and focused
and give tests readable names, as described in Chapter 21. If a test is small, its
name should tell us most of what we need to know about what has gone wrong.
Explanatory Assertion Messages
JUnit’s assertion methods all have a version in which the ﬁrst parameter is a
message to display when the assertion fails. From what we’ve seen, this feature
is not used as often as it should be to make assertion failures more helpful.
For example, when this test fails:
Customer customer  = order.getCustomer();
assertEquals("573242", customer.getAccountId());
assertEquals(16301, customer.getOutstandingBalance());
the report does not make it obvious which of the assertions has failed:
ComparisonFailure: expected:<[16301]> but was:<[16103]>
The message is describing the symptom (the balance is 16103) rather than the
cause (the outstanding balance calculation is wrong).
If we add a message to identify the value being asserted:
assertEquals("account id", "573242", customer.getAccountId());
assertEquals("outstanding balance", 16301, customer.getOustandingBalance());
we can immediately see what the point is:
ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
Highlight Detail with Matchers
Developers can provide another level of diagnostic detail by using assertThat()
with Hamcrest matchers. The Matcher API includes support for describing the
value that mismatched, to help with understanding exactly what is different. For
example, the instrument strike price assertion on page 252 generates this failure
report:
Expected: a collection containing instrument at price a value greater than <81>
     but: price was <50>, price was <72>, price was <31>
which shows exactly which values are relevant.
Chapter 23
Test Diagnostics
268


