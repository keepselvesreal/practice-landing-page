# 24.2 Test for Information, Not Representation (pp.274-275)

---
**Page 274**

Specify Precisely What Should Happen and No More
JUnit, Hamcrest, and jMock allow us to specify just what we want from the
target code (there are equivalents in other languages). The more precise we are,
the more the code can ﬂex in other unrelated dimensions without breaking tests
misleadingly. Our experience is that the other beneﬁt of keeping tests ﬂexible is
that they’re easier for us to understand because they are clearer about what they’re
testing—about what is and is not important in the tested code.
Test for Information, Not Representation
A test might need to pass a value to trigger the behavior it’s supposed to exercise
in its target object. The value could either be passed in as a parameter to a method
on the object, or returned as a result from a query the object makes on one of
its neighbors stubbed by the test. If the test is structured in terms of how the
value is represented by other parts of the system, then it has a dependency on
those parts and will break when they change.
For example, imagine we have a system that uses a CustomerBase to store and
ﬁnd information about our customers. One of its features is to look up a Customer
given an email address; it returns null if there’s no customer with the given
address.
public interface CustomerBase {
// Returns null if no customer found
  Customer findCustomerWithEmailAddress(String emailAddress);
[…]
}
When we test the parts of the code that search for customers by email address,
we stub CustomerBase as a collaborating object. In some of those tests, no
customer will be found so we return null:
allowing(customerBase).findCustomerWithEmailAddress(theAddress);
                                        will(returnValue(null));
There are two problems with this use of null in a test. First, we have to remember
what null means here, and when it’s appropriate; the test is not self-explanatory.
The second concern is the cost of maintenance.
Some time later, we experience a NullPointerException in production and
track the source of the null reference down to the CustomerBase. We realize we’ve
broken one of our design rules: “Never Pass Null between Objects.” Ashamed,
we change the CustomerBase’s search methods to return a Maybe type, which im-
plements an iterable collection of at most one result.
Chapter 24
Test Flexibility
274


---
**Page 275**

public interface CustomerBase {
Maybe<Customer> findCustomerWithEmailAddress(String emailAddress);
}
public abstract class Maybe<T> implements Iterable<T> {
  abstract boolean hasResult();
  public static Maybe<T> just(T oneValue) { …
  public static Maybe<T> nothing() { …
}
We still, however, have the tests that stub CustomerBase to return null, to
represent missing customers. The compiler cannot warn us of the mismatch be-
cause null is a valid value of type Maybe<Customer> too, so the best we can do
is to watch all these tests fail and change each one to the new design.
If, instead, we’d given the tests their own representation of “no customer
found” as a single well-named constant instead of the literal null, we could have
avoided this drudgery. We would have changed one line:
public static final Customer NO_CUSTOMER_FOUND = null;
to
public static final Maybe<Customer> NO_CUSTOMER_FOUND = Maybe.nothing();
without changing the tests themselves.
Tests should be written in terms of the information passed between objects,
not of how that information is represented. Doing so will both make the tests
more self-explanatory and shield them from changes in implementation controlled
elsewhere in the system. Signiﬁcant values, like NO_CUSTOMER_FOUND, should be
deﬁned in one place as a constant. There’s another example in Chapter 12 when
we introduce UNUSED_CHAT. For more complex structures, we can hide the details
of the representation in test data builders (Chapter 22).
Precise Assertions
In a test, focus the assertions on just what’s relevant to the scenario being tested.
Avoid asserting values that aren’t driven by the test inputs, and avoid reasserting
behavior that is covered in other tests.
We ﬁnd that these heuristics guide us towards writing tests where each method
exercises a unique aspect of the target code’s behavior. This makes the tests more
robust because they’re not dependent on unrelated results, and there’s less
duplication.
Most test assertions are simple checks for equality; for example, we assert the
number of rows in a table model in “Extending the Table Model” (page 180).
Testing for equality doesn’t scale well as the value being returned becomes more
275
Precise Assertions


