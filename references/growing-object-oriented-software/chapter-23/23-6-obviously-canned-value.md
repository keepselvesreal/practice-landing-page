# 23.6 Obviously Canned Value (pp.270-270)

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


