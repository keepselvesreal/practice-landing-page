# 24.1 Introduction (pp.273-274)

---
**Page 273**

Chapter 24
Test Flexibility
Living plants are flexible and tender;
the dead are brittle and dry.
[…]
The rigid and stiff will be broken.
The soft and yielding will overcome.
—Lao Tzu (c.604—531 B.C.)
Introduction
As the system and its associated test suite grows, maintaining the tests can become
a burden if they have not been written carefully. We’ve described how we can
reduce the ongoing cost of tests by making them easy to read and generating
helpful diagnostics on failure. We also want to make sure that each test fails
only when its relevant code is broken. Otherwise, we end up with brittle
tests that slow down development and inhibit refactoring. Common causes of test
brittleness include:
•
The tests are too tightly coupled to unrelated parts of the system or unrelated
behavior of the object(s) they’re testing;
•
The tests overspecify the expected behavior of the target code, constraining
it more than necessary; and,
•
There is duplication when multiple tests exercise the same production code
behavior.
Test brittleness is not just an attribute of how the tests are written; it’s also
related to the design of the system. If an object is difﬁcult to decouple from its
environment because it has many dependencies or its dependencies are hidden,
its tests will fail when distant parts of the system change. It will be hard to judge
the knock-on effects of altering the code. So, we can use test brittleness as a
valuable source of feedback about design quality.
There’s a virtuous relationship with test readability and resilience. A test that
is focused, has clean set-up, and has minimal duplication is easier to name and is
more obvious about its purpose. This chapter expands on some of the techniques
we discussed in Chapter 21. Actually, the whole chapter can be collapsed into a
single rule:
273


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


