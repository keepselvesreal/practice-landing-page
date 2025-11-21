# 23.4 Highlight Detail with Matchers (pp.268-269)

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


---
**Page 269**

Self-Describing Value
An alternative to adding detail to the assertion is to build the detail into values
in the assertion. We can take this in the same spirit as the idea that comments
are a hint that the code needs to be improved: if we have to add detail to an
assertion, maybe that’s a hint that we could make the failure more obvious.
In the customer example above, we could improve the failure message by setting
the account identiﬁer in the test Customer to the self-describing value "a customer
account id":
ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
Now we don’t need to add an explanatory message, because the value itself
explains its role.
We might be able to do more when we’re working with reference types. For
example, in a test that has this setup:
Date startDate = new Date(1000);
Date endDate = new Date(2000);
the failure message reports that a payment date is wrong but doesn’t describe
where the wrong value might have come from:
java.lang.AssertionError: payment date
Expected: <Thu Jan 01 01:00:01 GMT 1970>
     got: <Thu Jan 01 01:00:02 GMT 1970>
What we really want to know is the meaning of these dates. If we force the
display string:
Date startDate = namedDate(1000, "startDate");
Date endDate = namedDate(2000, "endDate");
Date namedDate(long timeValue, final String name) {
    return new Date(timeValue) { public String toString() { return name; } };
}
we get a message that describes the role that each date plays:
java.lang.AssertionError: payment date
Expected: <startDate>
     got: <endDate>
which makes it clear that we’ve assigned the wrong ﬁeld to the payment date.1
1. This is yet another motivation for deﬁning more domain types to hide the basic types
in the language. As we discussed in “Domain Types Are Better Than Strings”
(page 213), it gives us somewhere to hang useful behavior like this.
269
Self-Describing Value


