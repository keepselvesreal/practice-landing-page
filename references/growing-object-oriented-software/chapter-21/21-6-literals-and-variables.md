# 21.6 Literals and Variables (pp.255-257)

---
**Page 255**

too much detail, which makes them difﬁcult to read and brittle when things
change; we discuss what this might mean in “Too Many Expectations” (page 242).
For the expectations and assertions we write, we try to keep them as narrowly
deﬁned as possible. For example, in the “instrument with price” assertion above,
we check only the strike price and ignore the rest of the values as irrelevant in
that test. In other cases, we’re not interested in all of the arguments to a method,
so we ignore them in the expectation. In Chapter 19, we deﬁne an expectation
that says that we care about the Sniper identiﬁer and message, but that any
RuntimeException object will do for the third argument:
oneOf(failureReporter).cannotTranslateMessage(
                         with(SNIPER_ID), with(badMessage),
                         with(any(RuntimeException.class)));
If you learned about pre- and postconditions in college, this is when that training
will come in useful.
Finally, a word of caution on assertFalse(). The combination of the failure
message and negation makes it easy to read this as meaning that the two dates
should not be different:
assertFalse("end date", first.endDate().equals(second.endDate()));
We could use assertTrue() and add a “!” to the result but, again, the single
character is easy to miss. That’s why we prefer to use matchers to make the code
more explicit:
assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
which also has the advantage of showing the actual date received in the failure
report:
java.lang.AssertionError: end date
Expected: not <Thu Jan 01 02:34:38 GMT 1970>
     but: was <Thu Jan 01 02:34:38 GMT 1970>
Literals and Variables
One last point. As we wrote in the introduction to this chapter, test code tends
to be more concrete than production code, which means it has more literal values.
Literal values without explanation can be difﬁcult to understand because the
programmer has to interpret whether a particular value is signiﬁcant (e.g. just
outside the allowed range) or just an arbitrary placeholder to trace behavior (e.g.
should be doubled and passed on to a peer). A literal value does not describe its
role, although there are some techniques for doing so that we will show in
Chapter 23
One solution is to allocate literal values to variables and constants with names
that describe their function. For example, in Chapter 12 we declared
255
Literals and Variables


---
**Page 256**

public static final Chat UNUSED_CHAT = null;
to show that we were using null to represent an argument that was unused in
the target code. We weren’t expecting the code to receive null in production,
but it turns out that we don’t care and it makes testing easier. Similarly, a team
might develop conventions for naming common values, such as:
public final static INVALID_ID = 666;
We name variables to show the roles these values or objects play in the test and
their relationships to the target object.
Chapter 21
Test Readability
256


---
**Page 257**

Chapter 22
Constructing Complex Test
Data
Many attempts to communicate are nulliﬁed by saying too much.
—Robert Greenleaf
Introduction
If we are strict about our use of constructors and immutable value objects, con-
structing objects in tests can be a chore. In production code, we construct such
objects in relatively few places and all the required values are available to hand
from, for example, user input, a database query, or a received message. In tests,
however, we have to provide all the constructor arguments every time we want
to create an object:
@Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
  Order order = new Order(
      new Customer("Sherlock Holmes",
          new Address("221b Baker Street", 
                      "London", 
                      new PostCode("NW1", "3RX"))));
  order.addLine(new OrderLine("Deerstalker Hat", 1));
  order.addLine(new OrderLine("Tweed Cape", 1));
[…]
}
The code to create all these objects makes the tests hard to read, ﬁlling them
with information that doesn’t contribute to the behavior being tested. It also
makes tests brittle, as changes to the constructor arguments or the structure of
the objects will break many tests. The object mother pattern [Schuh01] is one
attempt to avoid this problem. An object mother is a class that contains a number
of factory methods [Gamma94] that create objects for use in tests. For example,
we could write an object mother for orders:
Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
An object mother makes tests more readable by packaging up the code that
creates new object structures and giving it a name. It also helps with maintenance
since its features can be reused between tests. On the other hand, the object
257


