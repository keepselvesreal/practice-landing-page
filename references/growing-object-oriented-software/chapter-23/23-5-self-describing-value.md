# 23.5 Self-Describing Value (pp.269-270)

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


---
**Page 270**

Obviously Canned Value
Sometimes, the values being checked can’t easily explain themselves. There’s not
enough information in a char or int, for example. One option is to use improb-
able values that will be obviously different from the values we would expect in
production. For an int, for example, we might use a negative value (if that doesn’t
break the code) or Integer.MAX_VALUE (if it’s wildly out of range). Similarly, the
original version of startDate in the previous example was an obviously canned
value because nothing in the system dated back to 1970.
When a team develops conventions for common values, it can ensure that they
stand out. The INVALID_ID at the end of the last chapter was three digits long;
that would be very obviously wrong if real system identiﬁers were ﬁve digits
and up.
Tracer Object
Sometimes we just want to check that an object is passed around by the code
under test and routed to the appropriate collaborator. We can create a tracer
object, a type of Obviously Canned Value, to represent this value. A tracer object
is a dummy object that has no supported behavior of its own, except to describe
its role when something fails. For example, this test:
@RunWith(JMock.class)
public class CustomerTest {
  final LineItem item1 = context.mock(LineItem.class, "item1");
  final LineItem item2 = context.mock(LineItem.class, "item2");
  final Billing billing = context.mock(Billing.class);
  @Test public void
requestsInvoiceForPurchasedItems() {
    context.checking(new Expectations() {{
      oneOf(billing).add(item1);
      oneOf(billing).add(item2);
    }});
    customer.purchase(item1, item2);
    customer.requestInvoice(billing);
  }
}
might generate a failure report like this:
not all expectations were satisfied
expectations:
  expected once, already invoked 1 time: billing.add(<item1>)
  ! expected once, never invoked: billing.add(<item2>>)
what happened before this:
  billing.add(<item1>)
Chapter 23
Test Diagnostics
270


