Line 1: 
Line 2: --- 페이지 298 ---
Line 3: Chapter 24
Line 4: Test Flexibility
Line 5: Living plants are flexible and tender;
Line 6: the dead are brittle and dry.
Line 7: […]
Line 8: The rigid and stiff will be broken.
Line 9: The soft and yielding will overcome.
Line 10: —Lao Tzu (c.604—531 B.C.)
Line 11: Introduction
Line 12: As the system and its associated test suite grows, maintaining the tests can become
Line 13: a burden if they have not been written carefully. We’ve described how we can
Line 14: reduce the ongoing cost of tests by making them easy to read and generating
Line 15: helpful diagnostics on failure. We also want to make sure that each test fails
Line 16: only when its relevant code is broken. Otherwise, we end up with brittle
Line 17: tests that slow down development and inhibit refactoring. Common causes of test
Line 18: brittleness include:
Line 19: •
Line 20: The tests are too tightly coupled to unrelated parts of the system or unrelated
Line 21: behavior of the object(s) they’re testing;
Line 22: •
Line 23: The tests overspecify the expected behavior of the target code, constraining
Line 24: it more than necessary; and,
Line 25: •
Line 26: There is duplication when multiple tests exercise the same production code
Line 27: behavior.
Line 28: Test brittleness is not just an attribute of how the tests are written; it’s also
Line 29: related to the design of the system. If an object is difﬁcult to decouple from its
Line 30: environment because it has many dependencies or its dependencies are hidden,
Line 31: its tests will fail when distant parts of the system change. It will be hard to judge
Line 32: the knock-on effects of altering the code. So, we can use test brittleness as a
Line 33: valuable source of feedback about design quality.
Line 34: There’s a virtuous relationship with test readability and resilience. A test that
Line 35: is focused, has clean set-up, and has minimal duplication is easier to name and is
Line 36: more obvious about its purpose. This chapter expands on some of the techniques
Line 37: we discussed in Chapter 21. Actually, the whole chapter can be collapsed into a
Line 38: single rule:
Line 39: 273
Line 40: 
Line 41: --- 페이지 299 ---
Line 42: Specify Precisely What Should Happen and No More
Line 43: JUnit, Hamcrest, and jMock allow us to specify just what we want from the
Line 44: target code (there are equivalents in other languages). The more precise we are,
Line 45: the more the code can ﬂex in other unrelated dimensions without breaking tests
Line 46: misleadingly. Our experience is that the other beneﬁt of keeping tests ﬂexible is
Line 47: that they’re easier for us to understand because they are clearer about what they’re
Line 48: testing—about what is and is not important in the tested code.
Line 49: Test for Information, Not Representation
Line 50: A test might need to pass a value to trigger the behavior it’s supposed to exercise
Line 51: in its target object. The value could either be passed in as a parameter to a method
Line 52: on the object, or returned as a result from a query the object makes on one of
Line 53: its neighbors stubbed by the test. If the test is structured in terms of how the
Line 54: value is represented by other parts of the system, then it has a dependency on
Line 55: those parts and will break when they change.
Line 56: For example, imagine we have a system that uses a CustomerBase to store and
Line 57: ﬁnd information about our customers. One of its features is to look up a Customer
Line 58: given an email address; it returns null if there’s no customer with the given
Line 59: address.
Line 60: public interface CustomerBase {
Line 61: // Returns null if no customer found
Line 62:   Customer findCustomerWithEmailAddress(String emailAddress);
Line 63: […]
Line 64: }
Line 65: When we test the parts of the code that search for customers by email address,
Line 66: we stub CustomerBase as a collaborating object. In some of those tests, no
Line 67: customer will be found so we return null:
Line 68: allowing(customerBase).findCustomerWithEmailAddress(theAddress);
Line 69:                                         will(returnValue(null));
Line 70: There are two problems with this use of null in a test. First, we have to remember
Line 71: what null means here, and when it’s appropriate; the test is not self-explanatory.
Line 72: The second concern is the cost of maintenance.
Line 73: Some time later, we experience a NullPointerException in production and
Line 74: track the source of the null reference down to the CustomerBase. We realize we’ve
Line 75: broken one of our design rules: “Never Pass Null between Objects.” Ashamed,
Line 76: we change the CustomerBase’s search methods to return a Maybe type, which im-
Line 77: plements an iterable collection of at most one result.
Line 78: Chapter 24
Line 79: Test Flexibility
Line 80: 274
Line 81: 
Line 82: --- 페이지 300 ---
Line 83: public interface CustomerBase {
Line 84: Maybe<Customer> findCustomerWithEmailAddress(String emailAddress);
Line 85: }
Line 86: public abstract class Maybe<T> implements Iterable<T> {
Line 87:   abstract boolean hasResult();
Line 88:   public static Maybe<T> just(T oneValue) { …
Line 89:   public static Maybe<T> nothing() { …
Line 90: }
Line 91: We still, however, have the tests that stub CustomerBase to return null, to
Line 92: represent missing customers. The compiler cannot warn us of the mismatch be-
Line 93: cause null is a valid value of type Maybe<Customer> too, so the best we can do
Line 94: is to watch all these tests fail and change each one to the new design.
Line 95: If, instead, we’d given the tests their own representation of “no customer
Line 96: found” as a single well-named constant instead of the literal null, we could have
Line 97: avoided this drudgery. We would have changed one line:
Line 98: public static final Customer NO_CUSTOMER_FOUND = null;
Line 99: to
Line 100: public static final Maybe<Customer> NO_CUSTOMER_FOUND = Maybe.nothing();
Line 101: without changing the tests themselves.
Line 102: Tests should be written in terms of the information passed between objects,
Line 103: not of how that information is represented. Doing so will both make the tests
Line 104: more self-explanatory and shield them from changes in implementation controlled
Line 105: elsewhere in the system. Signiﬁcant values, like NO_CUSTOMER_FOUND, should be
Line 106: deﬁned in one place as a constant. There’s another example in Chapter 12 when
Line 107: we introduce UNUSED_CHAT. For more complex structures, we can hide the details
Line 108: of the representation in test data builders (Chapter 22).
Line 109: Precise Assertions
Line 110: In a test, focus the assertions on just what’s relevant to the scenario being tested.
Line 111: Avoid asserting values that aren’t driven by the test inputs, and avoid reasserting
Line 112: behavior that is covered in other tests.
Line 113: We ﬁnd that these heuristics guide us towards writing tests where each method
Line 114: exercises a unique aspect of the target code’s behavior. This makes the tests more
Line 115: robust because they’re not dependent on unrelated results, and there’s less
Line 116: duplication.
Line 117: Most test assertions are simple checks for equality; for example, we assert the
Line 118: number of rows in a table model in “Extending the Table Model” (page 180).
Line 119: Testing for equality doesn’t scale well as the value being returned becomes more
Line 120: 275
Line 121: Precise Assertions
Line 122: 
Line 123: --- 페이지 301 ---
Line 124: complex. Different test scenarios may make the tested code return results that
Line 125: differ only in speciﬁc attributes, so comparing the entire result each time is
Line 126: misleading and introduces an implicit dependency on the behavior of the whole
Line 127: tested object.
Line 128: There are a couple of ways in which a result can be more complex. First, it
Line 129: can be deﬁned as a structured value type. This is straightforward since we can
Line 130: just reference directly any attributes we want to assert. For example, if we take
Line 131: the ﬁnancial instrument from “Use Structure to Explain” (page 253), we might
Line 132: need to assert only its strike price:
Line 133: assertEquals("strike price", 92, instrument.getStrikePrice());
Line 134: without comparing the whole instrument.
Line 135: We can use Hamcrest matchers to make the assertions more expressive and
Line 136: more ﬁnely tuned. For example, if we want to assert that a transaction identiﬁer
Line 137: is larger than its predecessor, we can write:
Line 138: assertThat(instrument.getTransactionId(), largerThan(PREVIOUS_TRANSACTION_ID));
Line 139: This tells the programmer that the only thing we really care about is that the new
Line 140: identiﬁer is larger than the previous one—its actual value is not important in this
Line 141: test. The assertion also generates a helpful message when it fails.
Line 142: The second source of complexity is implicit, but very common. We often have
Line 143: to make assertions about a text string. Sometimes we know exactly what the text
Line 144: should be, for example when we have the FakeAuctionServer look for speciﬁc
Line 145: messages in “Extending the Fake Auction” (page 107). Sometimes, however,
Line 146: all we need to check is that certain values are included in the text.
Line 147: A frequent example is when generating a failure message. We don’t want all
Line 148: our unit tests to be locked to its current formatting, so that they fail when we
Line 149: add whitespace, and we don’t want to have to do anything clever to cope with
Line 150: timestamps. We just want to know that the critical information is included, so
Line 151: we write:
Line 152: assertThat(failureMessage,
Line 153:            allOf(containsString("strikePrice=92"), 
Line 154:                  containsString("id=FGD.430"), 
Line 155:                  containsString("is expired"))); 
Line 156: which asserts that all these strings occur somewhere in failureMessage. That’s
Line 157: enough reassurance for us, and we can write other tests to check that a message
Line 158: is formatted correctly if we think it’s signiﬁcant.
Line 159: One interesting effect of trying to write precise assertions against text strings
Line 160: is that the effort often suggests that we’re missing an intermediate structure
Line 161: object—in this case perhaps an InstrumentFailure. Most of the code would be
Line 162: written in terms of an InstrumentFailure, a structured value that carries all the
Line 163: relevant ﬁelds. The failure would be converted to a string only at the last possible
Line 164: moment, and that string conversion can be tested in isolation.
Line 165: Chapter 24
Line 166: Test Flexibility
Line 167: 276
Line 168: 
Line 169: --- 페이지 302 ---
Line 170: Precise Expectations
Line 171: We can extend the concept of being precise about assertions to being precise
Line 172: about expectations. Each mock object test should specify just the relevant details
Line 173: of the interactions between the object under test and its neighbors. The combined
Line 174: unit tests for an object describe its protocol for communicating with the rest of
Line 175: the system.
Line 176: We’ve built a lot of support into jMock for specifying this communication
Line 177: between objects as precisely as it should be. The API is designed to produce tests
Line 178: that clearly express how objects relate to each other and that are ﬂexible because
Line 179: they’re not too restrictive. This may require a little more test code than some
Line 180: of the alternatives, but we ﬁnd that the extra rigor keeps the tests clear.
Line 181: Precise Parameter Matching
Line 182: We want to be as precise about the values passed in to a method as we are about
Line 183: the value it returns. For example, in “Assertions and Expectations” (page 254)
Line 184: we showed an expectation where one of the accepted arguments was any type
Line 185: of RuntimeException; the speciﬁc class doesn’t matter. Similarly, in “Extracting
Line 186: the SnipersTableModel” (page 197), we have this expectation:
Line 187: oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
Line 188: The method sniperForItem() returns a Matcher that checks only the item identiﬁer
Line 189: when given an AuctionSniper. This test doesn’t care about anything else in the
Line 190: sniper’s state, such as its current bid or last price, so we don’t make it more
Line 191: brittle by checking those values.
Line 192: The same precision can be applied to expecting input strings. If, for example,
Line 193: we have an auditTrail object to accept the failure message we described
Line 194: above, we can write a precise expectation for that auditing:
Line 195: oneOf(auditTrail).recordFailure(with(allOf(containsString("strikePrice=92"),
Line 196:                                            containsString("id=FGD.430"), 
Line 197:                                            containsString("is expired")))); 
Line 198: Allowances and Expectations
Line 199: We introduced the concept of allowances in “The Sniper Acquires Some State”
Line 200: (page 144). jMock insists that all expectations are met during a test, but al-
Line 201: lowances may be matched or not. The point of the distinction is to highlight
Line 202: what matters in a particular test. Expectations describe the interactions that are
Line 203: essential to the protocol we’re testing: if we send this message to the object, we
Line 204: expect to see it send this other message to this neighbor.
Line 205: Allowances support the interaction we’re testing. We often use them as stubs
Line 206: to feed values into the object, to get the object into the right state for the behavior
Line 207: we want to test. We also use them to ignore other interactions that aren’t relevant
Line 208: 277
Line 209: Precise Expectations
Line 210: 
Line 211: --- 페이지 303 ---
Line 212: to the current test. For example, in “Repurposing sniperBidding()” we have a
Line 213: test that includes:
Line 214: ignoring(auction);
Line 215: allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
Line 216:                                           then(sniperState.is("bidding"));
Line 217: The ignoring() clause says that, in this test, we don’t care about messages
Line 218: sent to the auction; they will be covered in other tests. The allowing() clause
Line 219: matches any call to sniperStateChanged() with a Sniper that is currently bidding,
Line 220: but doesn’t insist that such a call happens. In this test, we use the allowance to
Line 221: record what the Sniper has told us about its state. The method aSniperThatIs()
Line 222: returns a Matcher that checks only the SniperState when given a SniperSnapshot.
Line 223: In other tests we attach “action” clauses to allowances, so that the call will
Line 224: return a value or throw an exception. For example, we might have an allowance
Line 225: that stubs the catalog to return a price that will be returned for use later in
Line 226: the test:
Line 227: allowing(catalog).getPriceForItem(item); will(returnValue(74));
Line 228: The distinction between allowances and expectations isn’t rigid, but we’ve
Line 229: found that this simple rule helps:
Line 230: Allow Queries; Expect Commands
Line 231: Commands are calls that are likely to have side effects, to change the world outside
Line 232: the target object.When we tell the auditTrail above to record a failure, we expect
Line 233: that to change the contents of some kind of log. The state of the system will be
Line 234: different if we call the method a different number of times.
Line 235: Queries don’t change the world, so they can be called any number of times, includ-
Line 236: ing none. In our example above, it doesn’t make any difference to the system how
Line 237: many times we ask the catalog for a price.
Line 238: The rule helps to decouple the test from the tested object. If the implementation
Line 239: changes, for example to introduce caching or use a different algorithm, the test
Line 240: is still valid. On the other hand, if we were writing a test for a cache, we would
Line 241: want to know exactly how often the query was made.
Line 242: jMock supports more varied checking of how often a call is made than just
Line 243: allowing() and oneOf(). The number of times a call is expected is deﬁned by the
Line 244: “cardinality” clause that starts the expectation. In “The AuctionSniper Bids,”
Line 245: we saw the example:
Line 246: atLeast(1).of(sniperListener).sniperBidding();
Line 247: Chapter 24
Line 248: Test Flexibility
Line 249: 278
Line 250: 
Line 251: --- 페이지 304 ---
Line 252: which says that we care that this call is made, but not how many times. There
Line 253: are other clauses which allow ﬁne-tuning of the number of times a call is expected,
Line 254: listed in Appendix A.
Line 255: Ignoring Irrelevant Objects
Line 256: As you’ve seen, we can simplify a test by “ignoring” collaborators that are not
Line 257: relevant to the functionality being exercised. jMock will not check any calls to
Line 258: ignored objects. This keeps the test simple and focused, so we can immediately
Line 259: see what’s important and changes to one aspect of the code do not break
Line 260: unrelated tests.
Line 261: As a convenience, jMock will provide “zero” results for ignored methods that
Line 262: return a value, depending on the return type:
Line 263: “Zero” value
Line 264: Type
Line 265: false
Line 266: Boolean
Line 267: 0
Line 268: Numeric type
Line 269: "" (an empty string)
Line 270: String
Line 271: Empty array
Line 272: Array
Line 273: An ignored mock
Line 274: A type that can be mocked by the Mockery
Line 275: null
Line 276: Any other type
Line 277: The ability to dynamically mock returned types can be a powerful tool for
Line 278: narrowing the scope of a test. For example, for code that uses the Java Persistence
Line 279: API (JPA), a test can ignore the EntityManagerFactory. The factory will return
Line 280: an ignored EntityManager, which will return an ignored EntityTransaction on
Line 281: which we can ignore commit() or rollback(). With one ignore clause, the test
Line 282: can focus on the code’s domain behavior by disabling everything to do with
Line 283: transactions.
Line 284: Like all “power tools,” ignoring() should be used with care. A chain of ignored
Line 285: objects might suggest that the functionality ought to be pulled out into a new
Line 286: collaborator. As programmers, we must also make sure that ignored features are
Line 287: tested somewhere, and that there are higher-level tests to make sure everything
Line 288: works together. In practice, we usually introduce ignoring() only when writing
Line 289: specialized tests after the basics are in place, as for example in “The Sniper
Line 290: Acquires Some State” (page 144).
Line 291: 279
Line 292: Precise Expectations
Line 293: 
Line 294: --- 페이지 305 ---
Line 295: Invocation Order
Line 296: jMock allows invocations on a mock object to be called in any order; the expec-
Line 297: tations don’t have to be declared in the same sequence.1 The less we say in the
Line 298: tests about the order of interactions, the more ﬂexibility we have with the imple-
Line 299: mentation of the code. We also gain ﬂexibility in how we structure the tests; for
Line 300: example, we can make test methods more readable by packaging up expectations
Line 301: in helper methods.
Line 302: Only Enforce Invocation Order When It Matters
Line 303: Sometimes the order in which calls are made is signiﬁcant, in which case we add
Line 304: explicit constraints to the test. Keeping such constraints to a minimum avoids
Line 305: locking down the production code. It also helps us see whether each case is
Line 306: necessary—ordered constraints are so uncommon that each use stands out.
Line 307: jMock has two mechanisms for constraining invocation order: sequences,
Line 308: which deﬁne an ordered list of invocations, and state machines, which can describe
Line 309: more sophisticated ordering constraints. Sequences are simpler to understand
Line 310: than state machines, but their restrictiveness can make tests brittle if used
Line 311: inappropriately.
Line 312: Sequences are most useful for conﬁrming that an object sends notiﬁcations to
Line 313: its neighbors in the right order. For example, we need an AuctionSearcher object
Line 314: that will search its collection of Auctions to ﬁnd which ones match anything from
Line 315: a given set of keywords. Whenever it ﬁnds a match, the searcher will notify its
Line 316: AuctionSearchListener by calling searchMatched() with the matching auction.
Line 317: The searcher will tell the listener that it’s tried all of its available auctions by
Line 318: calling searchFinished().
Line 319: Our ﬁrst attempt at a test looks like this:
Line 320: public class AuctionSearcherTest { […]
Line 321:   @Test public void
Line 322: announcesMatchForOneAuction() {
Line 323:     final AuctionSearcher auctionSearch = 
Line 324:                    new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
Line 325:     context.checking(new Expectations() {{
Line 326:       oneOf(searchListener).searchMatched(STUB_AUCTION1);
Line 327:       oneOf(searchListener).searchFinished();
Line 328:     }});
Line 329:     auctionSearch.searchFor(KEYWORDS);
Line 330:   }
Line 331: }
Line 332: 1. Some early mock frameworks were strictly “record/playback”: the actual calls had
Line 333: to match the sequence of the expected calls. No frameworks enforce this any more,
Line 334: but the misconception is still common.
Line 335: Chapter 24
Line 336: Test Flexibility
Line 337: 280
Line 338: 
Line 339: --- 페이지 306 ---
Line 340: where searchListener is a mock AuctionSearchListener, KEYWORDS is a set of
Line 341: keyword strings, and STUB_AUCTION1 is a stub implementation of Auction that
Line 342: will match one of the strings in KEYWORDS.
Line 343: The problem with this test is that there’s nothing to stop searchFinished()
Line 344: being called before searchMatched(), which doesn’t make sense. We have an in-
Line 345: terface for AuctionSearchListener, but we haven’t described its protocol. We
Line 346: can ﬁx this by adding a Sequence to describe the relationship between the calls
Line 347: to the listener. The test will fail if searchFinished() is called ﬁrst.
Line 348: @Test public void
Line 349: announcesMatchForOneAuction() {
Line 350:     final AuctionSearcher auctionSearch = 
Line 351:                    new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
Line 352:   context.checking(new Expectations() {{
Line 353: Sequence events = context.sequence("events");
Line 354:     oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
Line 355:     oneOf(searchListener).searchFinished();             inSequence(events);
Line 356:   }});
Line 357:   auctionSearch.searchFor(KEYWORDS);
Line 358: }
Line 359: We continue using this sequence as we add more auctions to match:
Line 360: @Test public void
Line 361: announcesMatchForTwoAuctions() {
Line 362:   final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
Line 363:                    new AuctionSearcher(searchListener, 
Line 364:                                        asList(STUB_AUCTION1, STUB_AUCTION2));
Line 365:   context.checking(new Expectations() {{
Line 366:     Sequence events = context.sequence("events");
Line 367:     oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
Line 368: oneOf(searchListener).searchMatched(STUB_AUCTION2); inSequence(events);
Line 369:     oneOf(searchListener).searchFinished();             inSequence(events);
Line 370:   }});
Line 371:   auctionSearch.searchFor(KEYWORDS);
Line 372: } 
Line 373: But is this overconstraining the protocol? Do we have to match auctions in
Line 374: the same order that they’re initialized? Perhaps all we care about is that the right
Line 375: matches are made before the search is closed. We can relax the ordering constraint
Line 376: with a States object (which we ﬁrst saw in “The Sniper Acquires Some State”
Line 377: on page 144).
Line 378: A States implements an abstract state machine with named states. We can
Line 379: trigger state transitions by attaching a then() clause to an expectation. We
Line 380: 281
Line 381: Precise Expectations
Line 382: 
Line 383: --- 페이지 307 ---
Line 384: can enforce that an invocation only happens when object is (or is not) in a
Line 385: particular state with a when() clause. We rewrite our test:
Line 386: @Test public void
Line 387: announcesMatchForTwoAuctions() {
Line 388:   final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
Line 389:                    new AuctionSearcher(searchListener, 
Line 390:                                        asList(STUB_AUCTION1, STUB_AUCTION2));
Line 391:   context.checking(new Expectations() {{
Line 392: States searching = context.states("searching");
Line 393:     oneOf(searchListener).searchMatched(STUB_AUCTION1); 
Line 394: when(searching.isNot("finished"));
Line 395:     oneOf(searchListener).searchMatched(STUB_AUCTION2); 
Line 396: when(searching.isNot("finished"));
Line 397:     oneOf(searchListener).searchFinished(); then(searching.is("finished"));
Line 398:   }});
Line 399:   auctionSearch.searchFor(KEYWORDS);
Line 400: } 
Line 401: When the test opens, searching is in an undeﬁned (default) state. The searcher
Line 402: can report matches as long as searching is not ﬁnished. When the searcher reports
Line 403: that it has ﬁnished, the then() clause switches searching to finished, which
Line 404: blocks any further matches.
Line 405: States and sequences can be used in combination. For example, if our require-
Line 406: ments change so that auctions have to be matched in order, we can add a sequence
Line 407: for just the matches, in addition to the existing searching states. The new
Line 408: sequence would conﬁrm the order of search results and the existing states would
Line 409: conﬁrm that the results arrived before the search is ﬁnished. An expectation can
Line 410: belong to multiple states and sequences, if that’s what the protocol requires. We
Line 411: rarely need such complexity—it’s most common when responding to external
Line 412: feeds of events where we don’t own the protocol—and we always take it as a
Line 413: hint that something should be broken up into smaller, simpler pieces.
Line 414: When Expectation Order Matters
Line 415: Actually, the order in which jMock expectations are declared is sometimes signiﬁcant,
Line 416: but not because they have to shadow the order of invocation. Expectations are
Line 417: appended to a list, and invocations are matched by searching this list in order. If
Line 418: there are two expectations that can match an invocation, the one declared ﬁrst will
Line 419: win. If that ﬁrst expectation is actually an allowance, the second expectation will
Line 420: never see a match and the test will fail.
Line 421: Chapter 24
Line 422: Test Flexibility
Line 423: 282
Line 424: 
Line 425: --- 페이지 308 ---
Line 426: The Power of jMock States
Line 427: jMock States has turned out to be a useful construct. We can use it to model
Line 428: each of the three types of participants in a test: the object being tested, its peers,
Line 429: and the test itself.
Line 430: We can represent our understanding of the state of the object being tested, as
Line 431: in the example above. The test listens for the events the object sends out to its
Line 432: peers and uses them to trigger state transitions and to reject events that would
Line 433: break the object’s protocol.
Line 434: As we wrote in “Representing Object State” (page 146), this is a logical repre-
Line 435: sentation of the state of the tested object. A States describes what the test ﬁnds
Line 436: relevant about the object, not its internal structure. We don’t want to constrain
Line 437: the object’s implementation.
Line 438: We can represent how a peer changes state as it’s called by the tested object.
Line 439: For instance, in the example above, we might want to insist that the listener must
Line 440: be ready before it can receive any results, so the searcher must query its state.
Line 441: We could add a new States, listenerState:
Line 442: allowing(searchListener).isReady(); will(returnValue(true));
Line 443:                                     then(listenerState.is("ready"));
Line 444: oneOf(searchListener).searchMatched(STUB_AUCTION1); 
Line 445:                                     when(listenerState.is("ready")); 
Line 446: Finally, we can represent the state of the test itself. For example, we could
Line 447: enforce that some interactions are ignored while the test is being set up:
Line 448: ignoring(auction); when(testState.isNot("running"));
Line 449: testState.become("running");
Line 450: oneOf(auction).bidMore(); when(testState.is("running")); 
Line 451: Even More Liberal Expectations
Line 452: Finally, jMock has plug-in points to support the deﬁnition of arbitrary expecta-
Line 453: tions. For example, we could write an expectation to accept any getter method:
Line 454: allowing(aPeerObject).method(startsWith("get")).withNoArguments();
Line 455: or to accept a call to one of a set of objects:
Line 456: oneOf (anyOf(same(o1),same(o2),same(o3))).method("doSomething");
Line 457: Such expectations move us from a statically typed to a dynamically typed world,
Line 458: which brings both power and risk. These are our strongest “power tool”
Line 459: features—sometimes just what we need but always to be used with care. There’s
Line 460: more detail in the jMock documentation.
Line 461: 283
Line 462: Precise Expectations
Line 463: 
Line 464: --- 페이지 309 ---
Line 465: “Guinea Pig” Objects
Line 466: In the “ports and adapters” architecture we described in “Designing for
Line 467: Maintainability” (page 47), the adapters map application domain objects onto
Line 468: the system’s technical infrastructure. Most of the adapter implementations we
Line 469: see are generic; for example, they often use reﬂection to move values between
Line 470: domains. We can apply such mappings to any type of object, which means we
Line 471: can change our domain model without touching the mapping code.
Line 472: The easiest approach when writing tests for the adapter code is to use types
Line 473: from the application domain model, but this makes the test brittle because it
Line 474: binds together the application and adapter domains. It introduces a risk of mis-
Line 475: leadingly breaking tests when we change the application model, because we
Line 476: haven’t separated the concerns.
Line 477: Here’s an example. A system uses an XmlMarshaller to marshal objects to and
Line 478: from XML so they can be sent across a network. This test exercises XmlMarshaller
Line 479: by round-tripping an AuctionClosedEvent object: a type that the production
Line 480: system really does send across the network.
Line 481: public class XmlMarshallerTest {
Line 482:   @Test public void 
Line 483: marshallsAndUnmarshallsSerialisableFields() {
Line 484:     XMLMarshaller marshaller = new XmlMarshaller();
Line 485:     AuctionClosedEvent original = new AuctionClosedEventBuilder().build();
Line 486:     String xml = marshaller.marshall(original);
Line 487:     AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
Line 488:     assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
Line 489:   }
Line 490: }
Line 491: Later we decide that our system won’t send an AuctionClosedEvent after all,
Line 492: so we should be able to delete the class. Our refactoring attempt will fail because
Line 493: AuctionClosedEvent is still being used by the XmlMarshallerTest. The irrelevant
Line 494: coupling will force us to rework the test unnecessarily.
Line 495: There’s a more signiﬁcant (and subtle) problem when we couple tests to domain
Line 496: types: it’s harder to see when test assumptions have been broken. For example,
Line 497: our XmlMarshallerTest also checks how the marshaller handles transient and
Line 498: non-transient ﬁelds. When we wrote the tests, AuctionClosedEvent included both
Line 499: kind of ﬁelds, so we were exercising all the paths through the marshaller. Later,
Line 500: we removed the transient ﬁelds from AuctionClosedEvent, which means that we
Line 501: have tests that are no longer meaningful but do not fail. Nothing is alerting us
Line 502: that we have tests that have stopped working and that important features are
Line 503: not being covered.
Line 504: Chapter 24
Line 505: Test Flexibility
Line 506: 284
Line 507: 
Line 508: --- 페이지 310 ---
Line 509: We should test the XmlMarshaller with speciﬁc types that are clear about the
Line 510: features that they represent, unrelated to the real system. For example, we can
Line 511: introduce helper classes in the test:
Line 512: public class XmlMarshallerTest {
Line 513:   public static class MarshalledObject {
Line 514:     private String privateField = "private";
Line 515:     public final String publicFinalField = "public final";
Line 516:     public int primitiveField;
Line 517: // constructors, accessors for private field, etc.
Line 518:   }
Line 519:   public static class WithTransient extends MarshalledObject {
Line 520:     public transient String transientField = "transient";
Line 521:   }  
Line 522:   @Test public void 
Line 523: marshallsAndUnmarshallsSerialisableFields() {
Line 524:     XMLMarshaller marshaller = new XmlMarshaller();
Line 525: WithTransient original = new WithTransient();
Line 526:     String xml = marshaller.marshall(original);
Line 527:     AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
Line 528:     assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
Line 529:   }
Line 530: } 
Line 531: The WithTransient class acts as a “guinea pig,” allowing us to exhaustively
Line 532: exercise the behavior of our XmlMarshaller before we let it loose on our produc-
Line 533: tion domain model. WithTransient also makes our test more readable because
Line 534: the class and its ﬁelds are examples of “Self-Describing Value” (page 269), with
Line 535: names that reﬂect their roles in the test.
Line 536: 285
Line 537: Guinea Pig Objects
Line 538: 
Line 539: --- 페이지 311 ---
Line 540: This page intentionally left blank 