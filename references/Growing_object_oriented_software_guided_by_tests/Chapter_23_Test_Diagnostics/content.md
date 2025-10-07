Line 1: 
Line 2: --- 페이지 292 ---
Line 3: Chapter 23
Line 4: Test Diagnostics
Line 5: Mistakes are the portals of discovery.
Line 6: —James Joyce
Line 7: Design to Fail
Line 8: The point of a test is not to pass but to fail. We want the production code to
Line 9: pass its tests, but we also want the tests to detect and report any errors that
Line 10: do exist. A “failing” test has actually succeeded at the job it was designed to do.
Line 11: Even unexpected test failures, in an area unrelated to where we are working, can
Line 12: be valuable because they reveal implicit relationships in the code that we hadn’t
Line 13: noticed.
Line 14: One situation we want to avoid, however, is when we can’t diagnose a test
Line 15: failure that has happened. The last thing we should have to do is crack open the
Line 16: debugger and step through the tested code to ﬁnd the point of disagreement. At
Line 17: a minimum, it suggests that our tests don’t yet express our requirements clearly
Line 18: enough. In the worst case, we can ﬁnd ourselves in “debug hell,” with deadlines
Line 19: to meet but no idea of how long a ﬁx will take. At this point, the temptation will
Line 20: be high to just delete the test—and lose our safety net.
Line 21: Stay Close to Home
Line 22: Synchronize frequently with the source code repository—up to every few minutes—
Line 23: so that if a test fails unexpectedly it won’t cost much to revert your recent changes
Line 24: and try another approach.
Line 25: The other implication of this tip is not to be too inhibited about dropping code and
Line 26: trying again. Sometimes it’s quicker to roll back and restart with a clear head than
Line 27: to keep digging.
Line 28: We’ve learned the hard way to make tests fail informatively. If a failing test
Line 29: clearly explains what has failed and why, we can quickly diagnose and correct
Line 30: the code. Then, we can get on with the next task.
Line 31: Chapter 21 addressed the static readability of tests. This chapter describes
Line 32: some practices that we ﬁnd helpful to make sure the tests give us the information
Line 33: we need at runtime.
Line 34: 267
Line 35: 
Line 36: --- 페이지 293 ---
Line 37: Small, Focused, Well-Named Tests
Line 38: The easiest way to improve diagnostics is to keep each test small and focused
Line 39: and give tests readable names, as described in Chapter 21. If a test is small, its
Line 40: name should tell us most of what we need to know about what has gone wrong.
Line 41: Explanatory Assertion Messages
Line 42: JUnit’s assertion methods all have a version in which the ﬁrst parameter is a
Line 43: message to display when the assertion fails. From what we’ve seen, this feature
Line 44: is not used as often as it should be to make assertion failures more helpful.
Line 45: For example, when this test fails:
Line 46: Customer customer  = order.getCustomer();
Line 47: assertEquals("573242", customer.getAccountId());
Line 48: assertEquals(16301, customer.getOutstandingBalance());
Line 49: the report does not make it obvious which of the assertions has failed:
Line 50: ComparisonFailure: expected:<[16301]> but was:<[16103]>
Line 51: The message is describing the symptom (the balance is 16103) rather than the
Line 52: cause (the outstanding balance calculation is wrong).
Line 53: If we add a message to identify the value being asserted:
Line 54: assertEquals("account id", "573242", customer.getAccountId());
Line 55: assertEquals("outstanding balance", 16301, customer.getOustandingBalance());
Line 56: we can immediately see what the point is:
Line 57: ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
Line 58: Highlight Detail with Matchers
Line 59: Developers can provide another level of diagnostic detail by using assertThat()
Line 60: with Hamcrest matchers. The Matcher API includes support for describing the
Line 61: value that mismatched, to help with understanding exactly what is different. For
Line 62: example, the instrument strike price assertion on page 252 generates this failure
Line 63: report:
Line 64: Expected: a collection containing instrument at price a value greater than <81>
Line 65:      but: price was <50>, price was <72>, price was <31>
Line 66: which shows exactly which values are relevant.
Line 67: Chapter 23
Line 68: Test Diagnostics
Line 69: 268
Line 70: 
Line 71: --- 페이지 294 ---
Line 72: Self-Describing Value
Line 73: An alternative to adding detail to the assertion is to build the detail into values
Line 74: in the assertion. We can take this in the same spirit as the idea that comments
Line 75: are a hint that the code needs to be improved: if we have to add detail to an
Line 76: assertion, maybe that’s a hint that we could make the failure more obvious.
Line 77: In the customer example above, we could improve the failure message by setting
Line 78: the account identiﬁer in the test Customer to the self-describing value "a customer
Line 79: account id":
Line 80: ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
Line 81: Now we don’t need to add an explanatory message, because the value itself
Line 82: explains its role.
Line 83: We might be able to do more when we’re working with reference types. For
Line 84: example, in a test that has this setup:
Line 85: Date startDate = new Date(1000);
Line 86: Date endDate = new Date(2000);
Line 87: the failure message reports that a payment date is wrong but doesn’t describe
Line 88: where the wrong value might have come from:
Line 89: java.lang.AssertionError: payment date
Line 90: Expected: <Thu Jan 01 01:00:01 GMT 1970>
Line 91:      got: <Thu Jan 01 01:00:02 GMT 1970>
Line 92: What we really want to know is the meaning of these dates. If we force the
Line 93: display string:
Line 94: Date startDate = namedDate(1000, "startDate");
Line 95: Date endDate = namedDate(2000, "endDate");
Line 96: Date namedDate(long timeValue, final String name) {
Line 97:     return new Date(timeValue) { public String toString() { return name; } };
Line 98: }
Line 99: we get a message that describes the role that each date plays:
Line 100: java.lang.AssertionError: payment date
Line 101: Expected: <startDate>
Line 102:      got: <endDate>
Line 103: which makes it clear that we’ve assigned the wrong ﬁeld to the payment date.1
Line 104: 1. This is yet another motivation for deﬁning more domain types to hide the basic types
Line 105: in the language. As we discussed in “Domain Types Are Better Than Strings”
Line 106: (page 213), it gives us somewhere to hang useful behavior like this.
Line 107: 269
Line 108: Self-Describing Value
Line 109: 
Line 110: --- 페이지 295 ---
Line 111: Obviously Canned Value
Line 112: Sometimes, the values being checked can’t easily explain themselves. There’s not
Line 113: enough information in a char or int, for example. One option is to use improb-
Line 114: able values that will be obviously different from the values we would expect in
Line 115: production. For an int, for example, we might use a negative value (if that doesn’t
Line 116: break the code) or Integer.MAX_VALUE (if it’s wildly out of range). Similarly, the
Line 117: original version of startDate in the previous example was an obviously canned
Line 118: value because nothing in the system dated back to 1970.
Line 119: When a team develops conventions for common values, it can ensure that they
Line 120: stand out. The INVALID_ID at the end of the last chapter was three digits long;
Line 121: that would be very obviously wrong if real system identiﬁers were ﬁve digits
Line 122: and up.
Line 123: Tracer Object
Line 124: Sometimes we just want to check that an object is passed around by the code
Line 125: under test and routed to the appropriate collaborator. We can create a tracer
Line 126: object, a type of Obviously Canned Value, to represent this value. A tracer object
Line 127: is a dummy object that has no supported behavior of its own, except to describe
Line 128: its role when something fails. For example, this test:
Line 129: @RunWith(JMock.class)
Line 130: public class CustomerTest {
Line 131:   final LineItem item1 = context.mock(LineItem.class, "item1");
Line 132:   final LineItem item2 = context.mock(LineItem.class, "item2");
Line 133:   final Billing billing = context.mock(Billing.class);
Line 134:   @Test public void
Line 135: requestsInvoiceForPurchasedItems() {
Line 136:     context.checking(new Expectations() {{
Line 137:       oneOf(billing).add(item1);
Line 138:       oneOf(billing).add(item2);
Line 139:     }});
Line 140:     customer.purchase(item1, item2);
Line 141:     customer.requestInvoice(billing);
Line 142:   }
Line 143: }
Line 144: might generate a failure report like this:
Line 145: not all expectations were satisfied
Line 146: expectations:
Line 147:   expected once, already invoked 1 time: billing.add(<item1>)
Line 148:   ! expected once, never invoked: billing.add(<item2>>)
Line 149: what happened before this:
Line 150:   billing.add(<item1>)
Line 151: Chapter 23
Line 152: Test Diagnostics
Line 153: 270
Line 154: 
Line 155: --- 페이지 296 ---
Line 156: Notice that jMock can accept a name when creating a mock object that will
Line 157: be used in failure reporting. In fact, where there’s more than one mock object of
Line 158: the same type, jMock insists that they are named to avoid confusion (the default
Line 159: is to use the class name).
Line 160: Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
Line 161: use an empty interface to mark (and name) a domain concept and show how
Line 162: it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
Line 163: with methods to describe its behavior.
Line 164: Explicitly Assert That Expectations Were Satisﬁed
Line 165: A test that has both expectations and assertions can produce a confusing failure.
Line 166: In jMock and other mock object frameworks, the expectations are checked after
Line 167: the body of the test. If, for example, a collaboration doesn’t work properly and
Line 168: returns a wrong value, an assertion might fail before any expectations are checked.
Line 169: This would produce a failure report that shows, say, an incorrect calculation result
Line 170: rather than the missing collaboration that actually caused it.
Line 171: In a few cases, then, it’s worth calling the assertIsSatisfied() method on
Line 172: the Mockery before any of the test assertions to get the right failure report:
Line 173: context.assertIsSatisfied();
Line 174: assertThat(result, equalTo(expectedResult));
Line 175: This demonstrates why it is important to “Watch the Test Fail” (page 42). If
Line 176: you expect the test to fail because an expectation is not satisﬁed but a postcondi-
Line 177: tion assertion fails instead, you will see that you should add an explicit call to
Line 178: assert that all expectations have been satisﬁed.
Line 179: Diagnostics Are a First-Class Feature
Line 180: Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
Line 181: TDD cycle: fail, pass, refactor. We’re making good progress and we know what
Line 182: the failures mean because we’ve just written the test. But nowadays, we try to
Line 183: follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Line 184: Chapter 5, because that’s how we know we’ve understood the feature—and
Line 185: whoever has to change it in a month’s time will also understand it. Figure 23.1
Line 186: shows again that we need to maintain the quality of the tests, as well as the
Line 187: production code.
Line 188: 271
Line 189: Diagnostics Are a First-Class Feature
Line 190: 
Line 191: --- 페이지 297 ---
Line 192: Figure 23.1
Line 193: Improve the diagnostics as part of the TDD cycle
Line 194: Chapter 23
Line 195: Test Diagnostics
Line 196: 272