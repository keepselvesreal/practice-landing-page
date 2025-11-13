# 24.3 Precise Assertions (pp.275-277)

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


---
**Page 276**

complex. Different test scenarios may make the tested code return results that
differ only in speciﬁc attributes, so comparing the entire result each time is
misleading and introduces an implicit dependency on the behavior of the whole
tested object.
There are a couple of ways in which a result can be more complex. First, it
can be deﬁned as a structured value type. This is straightforward since we can
just reference directly any attributes we want to assert. For example, if we take
the ﬁnancial instrument from “Use Structure to Explain” (page 253), we might
need to assert only its strike price:
assertEquals("strike price", 92, instrument.getStrikePrice());
without comparing the whole instrument.
We can use Hamcrest matchers to make the assertions more expressive and
more ﬁnely tuned. For example, if we want to assert that a transaction identiﬁer
is larger than its predecessor, we can write:
assertThat(instrument.getTransactionId(), largerThan(PREVIOUS_TRANSACTION_ID));
This tells the programmer that the only thing we really care about is that the new
identiﬁer is larger than the previous one—its actual value is not important in this
test. The assertion also generates a helpful message when it fails.
The second source of complexity is implicit, but very common. We often have
to make assertions about a text string. Sometimes we know exactly what the text
should be, for example when we have the FakeAuctionServer look for speciﬁc
messages in “Extending the Fake Auction” (page 107). Sometimes, however,
all we need to check is that certain values are included in the text.
A frequent example is when generating a failure message. We don’t want all
our unit tests to be locked to its current formatting, so that they fail when we
add whitespace, and we don’t want to have to do anything clever to cope with
timestamps. We just want to know that the critical information is included, so
we write:
assertThat(failureMessage,
           allOf(containsString("strikePrice=92"), 
                 containsString("id=FGD.430"), 
                 containsString("is expired"))); 
which asserts that all these strings occur somewhere in failureMessage. That’s
enough reassurance for us, and we can write other tests to check that a message
is formatted correctly if we think it’s signiﬁcant.
One interesting effect of trying to write precise assertions against text strings
is that the effort often suggests that we’re missing an intermediate structure
object—in this case perhaps an InstrumentFailure. Most of the code would be
written in terms of an InstrumentFailure, a structured value that carries all the
relevant ﬁelds. The failure would be converted to a string only at the last possible
moment, and that string conversion can be tested in isolation.
Chapter 24
Test Flexibility
276


---
**Page 277**

Precise Expectations
We can extend the concept of being precise about assertions to being precise
about expectations. Each mock object test should specify just the relevant details
of the interactions between the object under test and its neighbors. The combined
unit tests for an object describe its protocol for communicating with the rest of
the system.
We’ve built a lot of support into jMock for specifying this communication
between objects as precisely as it should be. The API is designed to produce tests
that clearly express how objects relate to each other and that are ﬂexible because
they’re not too restrictive. This may require a little more test code than some
of the alternatives, but we ﬁnd that the extra rigor keeps the tests clear.
Precise Parameter Matching
We want to be as precise about the values passed in to a method as we are about
the value it returns. For example, in “Assertions and Expectations” (page 254)
we showed an expectation where one of the accepted arguments was any type
of RuntimeException; the speciﬁc class doesn’t matter. Similarly, in “Extracting
the SnipersTableModel” (page 197), we have this expectation:
oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
The method sniperForItem() returns a Matcher that checks only the item identiﬁer
when given an AuctionSniper. This test doesn’t care about anything else in the
sniper’s state, such as its current bid or last price, so we don’t make it more
brittle by checking those values.
The same precision can be applied to expecting input strings. If, for example,
we have an auditTrail object to accept the failure message we described
above, we can write a precise expectation for that auditing:
oneOf(auditTrail).recordFailure(with(allOf(containsString("strikePrice=92"),
                                           containsString("id=FGD.430"), 
                                           containsString("is expired")))); 
Allowances and Expectations
We introduced the concept of allowances in “The Sniper Acquires Some State”
(page 144). jMock insists that all expectations are met during a test, but al-
lowances may be matched or not. The point of the distinction is to highlight
what matters in a particular test. Expectations describe the interactions that are
essential to the protocol we’re testing: if we send this message to the object, we
expect to see it send this other message to this neighbor.
Allowances support the interaction we’re testing. We often use them as stubs
to feed values into the object, to get the object into the right state for the behavior
we want to test. We also use them to ignore other interactions that aren’t relevant
277
Precise Expectations


