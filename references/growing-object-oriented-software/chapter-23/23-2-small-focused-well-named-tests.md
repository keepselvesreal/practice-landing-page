# 23.2 Small, Focused, Well-Named Tests (pp.268-268)

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


