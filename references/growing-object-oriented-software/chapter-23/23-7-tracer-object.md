# 23.7 Tracer Object (pp.270-271)

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


---
**Page 271**

Notice that jMock can accept a name when creating a mock object that will
be used in failure reporting. In fact, where there’s more than one mock object of
the same type, jMock insists that they are named to avoid confusion (the default
is to use the class name).
Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
use an empty interface to mark (and name) a domain concept and show how
it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
with methods to describe its behavior.
Explicitly Assert That Expectations Were Satisﬁed
A test that has both expectations and assertions can produce a confusing failure.
In jMock and other mock object frameworks, the expectations are checked after
the body of the test. If, for example, a collaboration doesn’t work properly and
returns a wrong value, an assertion might fail before any expectations are checked.
This would produce a failure report that shows, say, an incorrect calculation result
rather than the missing collaboration that actually caused it.
In a few cases, then, it’s worth calling the assertIsSatisfied() method on
the Mockery before any of the test assertions to get the right failure report:
context.assertIsSatisfied();
assertThat(result, equalTo(expectedResult));
This demonstrates why it is important to “Watch the Test Fail” (page 42). If
you expect the test to fail because an expectation is not satisﬁed but a postcondi-
tion assertion fails instead, you will see that you should add an explicit call to
assert that all expectations have been satisﬁed.
Diagnostics Are a First-Class Feature
Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
TDD cycle: fail, pass, refactor. We’re making good progress and we know what
the failures mean because we’ve just written the test. But nowadays, we try to
follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Chapter 5, because that’s how we know we’ve understood the feature—and
whoever has to change it in a month’s time will also understand it. Figure 23.1
shows again that we need to maintain the quality of the tests, as well as the
production code.
271
Diagnostics Are a First-Class Feature


