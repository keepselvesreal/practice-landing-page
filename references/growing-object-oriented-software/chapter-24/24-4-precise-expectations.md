# 24.4 Precise Expectations (pp.277-284)

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


---
**Page 278**

to the current test. For example, in “Repurposing sniperBidding()” we have a
test that includes:
ignoring(auction);
allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
                                          then(sniperState.is("bidding"));
The ignoring() clause says that, in this test, we don’t care about messages
sent to the auction; they will be covered in other tests. The allowing() clause
matches any call to sniperStateChanged() with a Sniper that is currently bidding,
but doesn’t insist that such a call happens. In this test, we use the allowance to
record what the Sniper has told us about its state. The method aSniperThatIs()
returns a Matcher that checks only the SniperState when given a SniperSnapshot.
In other tests we attach “action” clauses to allowances, so that the call will
return a value or throw an exception. For example, we might have an allowance
that stubs the catalog to return a price that will be returned for use later in
the test:
allowing(catalog).getPriceForItem(item); will(returnValue(74));
The distinction between allowances and expectations isn’t rigid, but we’ve
found that this simple rule helps:
Allow Queries; Expect Commands
Commands are calls that are likely to have side effects, to change the world outside
the target object.When we tell the auditTrail above to record a failure, we expect
that to change the contents of some kind of log. The state of the system will be
different if we call the method a different number of times.
Queries don’t change the world, so they can be called any number of times, includ-
ing none. In our example above, it doesn’t make any difference to the system how
many times we ask the catalog for a price.
The rule helps to decouple the test from the tested object. If the implementation
changes, for example to introduce caching or use a different algorithm, the test
is still valid. On the other hand, if we were writing a test for a cache, we would
want to know exactly how often the query was made.
jMock supports more varied checking of how often a call is made than just
allowing() and oneOf(). The number of times a call is expected is deﬁned by the
“cardinality” clause that starts the expectation. In “The AuctionSniper Bids,”
we saw the example:
atLeast(1).of(sniperListener).sniperBidding();
Chapter 24
Test Flexibility
278


---
**Page 279**

which says that we care that this call is made, but not how many times. There
are other clauses which allow ﬁne-tuning of the number of times a call is expected,
listed in Appendix A.
Ignoring Irrelevant Objects
As you’ve seen, we can simplify a test by “ignoring” collaborators that are not
relevant to the functionality being exercised. jMock will not check any calls to
ignored objects. This keeps the test simple and focused, so we can immediately
see what’s important and changes to one aspect of the code do not break
unrelated tests.
As a convenience, jMock will provide “zero” results for ignored methods that
return a value, depending on the return type:
“Zero” value
Type
false
Boolean
0
Numeric type
"" (an empty string)
String
Empty array
Array
An ignored mock
A type that can be mocked by the Mockery
null
Any other type
The ability to dynamically mock returned types can be a powerful tool for
narrowing the scope of a test. For example, for code that uses the Java Persistence
API (JPA), a test can ignore the EntityManagerFactory. The factory will return
an ignored EntityManager, which will return an ignored EntityTransaction on
which we can ignore commit() or rollback(). With one ignore clause, the test
can focus on the code’s domain behavior by disabling everything to do with
transactions.
Like all “power tools,” ignoring() should be used with care. A chain of ignored
objects might suggest that the functionality ought to be pulled out into a new
collaborator. As programmers, we must also make sure that ignored features are
tested somewhere, and that there are higher-level tests to make sure everything
works together. In practice, we usually introduce ignoring() only when writing
specialized tests after the basics are in place, as for example in “The Sniper
Acquires Some State” (page 144).
279
Precise Expectations


---
**Page 280**

Invocation Order
jMock allows invocations on a mock object to be called in any order; the expec-
tations don’t have to be declared in the same sequence.1 The less we say in the
tests about the order of interactions, the more ﬂexibility we have with the imple-
mentation of the code. We also gain ﬂexibility in how we structure the tests; for
example, we can make test methods more readable by packaging up expectations
in helper methods.
Only Enforce Invocation Order When It Matters
Sometimes the order in which calls are made is signiﬁcant, in which case we add
explicit constraints to the test. Keeping such constraints to a minimum avoids
locking down the production code. It also helps us see whether each case is
necessary—ordered constraints are so uncommon that each use stands out.
jMock has two mechanisms for constraining invocation order: sequences,
which deﬁne an ordered list of invocations, and state machines, which can describe
more sophisticated ordering constraints. Sequences are simpler to understand
than state machines, but their restrictiveness can make tests brittle if used
inappropriately.
Sequences are most useful for conﬁrming that an object sends notiﬁcations to
its neighbors in the right order. For example, we need an AuctionSearcher object
that will search its collection of Auctions to ﬁnd which ones match anything from
a given set of keywords. Whenever it ﬁnds a match, the searcher will notify its
AuctionSearchListener by calling searchMatched() with the matching auction.
The searcher will tell the listener that it’s tried all of its available auctions by
calling searchFinished().
Our ﬁrst attempt at a test looks like this:
public class AuctionSearcherTest { […]
  @Test public void
announcesMatchForOneAuction() {
    final AuctionSearcher auctionSearch = 
                   new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
    context.checking(new Expectations() {{
      oneOf(searchListener).searchMatched(STUB_AUCTION1);
      oneOf(searchListener).searchFinished();
    }});
    auctionSearch.searchFor(KEYWORDS);
  }
}
1. Some early mock frameworks were strictly “record/playback”: the actual calls had
to match the sequence of the expected calls. No frameworks enforce this any more,
but the misconception is still common.
Chapter 24
Test Flexibility
280


---
**Page 281**

where searchListener is a mock AuctionSearchListener, KEYWORDS is a set of
keyword strings, and STUB_AUCTION1 is a stub implementation of Auction that
will match one of the strings in KEYWORDS.
The problem with this test is that there’s nothing to stop searchFinished()
being called before searchMatched(), which doesn’t make sense. We have an in-
terface for AuctionSearchListener, but we haven’t described its protocol. We
can ﬁx this by adding a Sequence to describe the relationship between the calls
to the listener. The test will fail if searchFinished() is called ﬁrst.
@Test public void
announcesMatchForOneAuction() {
    final AuctionSearcher auctionSearch = 
                   new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
  context.checking(new Expectations() {{
Sequence events = context.sequence("events");
    oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
    oneOf(searchListener).searchFinished();             inSequence(events);
  }});
  auctionSearch.searchFor(KEYWORDS);
}
We continue using this sequence as we add more auctions to match:
@Test public void
announcesMatchForTwoAuctions() {
  final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
                   new AuctionSearcher(searchListener, 
                                       asList(STUB_AUCTION1, STUB_AUCTION2));
  context.checking(new Expectations() {{
    Sequence events = context.sequence("events");
    oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
oneOf(searchListener).searchMatched(STUB_AUCTION2); inSequence(events);
    oneOf(searchListener).searchFinished();             inSequence(events);
  }});
  auctionSearch.searchFor(KEYWORDS);
} 
But is this overconstraining the protocol? Do we have to match auctions in
the same order that they’re initialized? Perhaps all we care about is that the right
matches are made before the search is closed. We can relax the ordering constraint
with a States object (which we ﬁrst saw in “The Sniper Acquires Some State”
on page 144).
A States implements an abstract state machine with named states. We can
trigger state transitions by attaching a then() clause to an expectation. We
281
Precise Expectations


---
**Page 282**

can enforce that an invocation only happens when object is (or is not) in a
particular state with a when() clause. We rewrite our test:
@Test public void
announcesMatchForTwoAuctions() {
  final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
                   new AuctionSearcher(searchListener, 
                                       asList(STUB_AUCTION1, STUB_AUCTION2));
  context.checking(new Expectations() {{
States searching = context.states("searching");
    oneOf(searchListener).searchMatched(STUB_AUCTION1); 
when(searching.isNot("finished"));
    oneOf(searchListener).searchMatched(STUB_AUCTION2); 
when(searching.isNot("finished"));
    oneOf(searchListener).searchFinished(); then(searching.is("finished"));
  }});
  auctionSearch.searchFor(KEYWORDS);
} 
When the test opens, searching is in an undeﬁned (default) state. The searcher
can report matches as long as searching is not ﬁnished. When the searcher reports
that it has ﬁnished, the then() clause switches searching to finished, which
blocks any further matches.
States and sequences can be used in combination. For example, if our require-
ments change so that auctions have to be matched in order, we can add a sequence
for just the matches, in addition to the existing searching states. The new
sequence would conﬁrm the order of search results and the existing states would
conﬁrm that the results arrived before the search is ﬁnished. An expectation can
belong to multiple states and sequences, if that’s what the protocol requires. We
rarely need such complexity—it’s most common when responding to external
feeds of events where we don’t own the protocol—and we always take it as a
hint that something should be broken up into smaller, simpler pieces.
When Expectation Order Matters
Actually, the order in which jMock expectations are declared is sometimes signiﬁcant,
but not because they have to shadow the order of invocation. Expectations are
appended to a list, and invocations are matched by searching this list in order. If
there are two expectations that can match an invocation, the one declared ﬁrst will
win. If that ﬁrst expectation is actually an allowance, the second expectation will
never see a match and the test will fail.
Chapter 24
Test Flexibility
282


---
**Page 283**

The Power of jMock States
jMock States has turned out to be a useful construct. We can use it to model
each of the three types of participants in a test: the object being tested, its peers,
and the test itself.
We can represent our understanding of the state of the object being tested, as
in the example above. The test listens for the events the object sends out to its
peers and uses them to trigger state transitions and to reject events that would
break the object’s protocol.
As we wrote in “Representing Object State” (page 146), this is a logical repre-
sentation of the state of the tested object. A States describes what the test ﬁnds
relevant about the object, not its internal structure. We don’t want to constrain
the object’s implementation.
We can represent how a peer changes state as it’s called by the tested object.
For instance, in the example above, we might want to insist that the listener must
be ready before it can receive any results, so the searcher must query its state.
We could add a new States, listenerState:
allowing(searchListener).isReady(); will(returnValue(true));
                                    then(listenerState.is("ready"));
oneOf(searchListener).searchMatched(STUB_AUCTION1); 
                                    when(listenerState.is("ready")); 
Finally, we can represent the state of the test itself. For example, we could
enforce that some interactions are ignored while the test is being set up:
ignoring(auction); when(testState.isNot("running"));
testState.become("running");
oneOf(auction).bidMore(); when(testState.is("running")); 
Even More Liberal Expectations
Finally, jMock has plug-in points to support the deﬁnition of arbitrary expecta-
tions. For example, we could write an expectation to accept any getter method:
allowing(aPeerObject).method(startsWith("get")).withNoArguments();
or to accept a call to one of a set of objects:
oneOf (anyOf(same(o1),same(o2),same(o3))).method("doSomething");
Such expectations move us from a statically typed to a dynamically typed world,
which brings both power and risk. These are our strongest “power tool”
features—sometimes just what we need but always to be used with care. There’s
more detail in the jMock documentation.
283
Precise Expectations


---
**Page 284**

“Guinea Pig” Objects
In the “ports and adapters” architecture we described in “Designing for
Maintainability” (page 47), the adapters map application domain objects onto
the system’s technical infrastructure. Most of the adapter implementations we
see are generic; for example, they often use reﬂection to move values between
domains. We can apply such mappings to any type of object, which means we
can change our domain model without touching the mapping code.
The easiest approach when writing tests for the adapter code is to use types
from the application domain model, but this makes the test brittle because it
binds together the application and adapter domains. It introduces a risk of mis-
leadingly breaking tests when we change the application model, because we
haven’t separated the concerns.
Here’s an example. A system uses an XmlMarshaller to marshal objects to and
from XML so they can be sent across a network. This test exercises XmlMarshaller
by round-tripping an AuctionClosedEvent object: a type that the production
system really does send across the network.
public class XmlMarshallerTest {
  @Test public void 
marshallsAndUnmarshallsSerialisableFields() {
    XMLMarshaller marshaller = new XmlMarshaller();
    AuctionClosedEvent original = new AuctionClosedEventBuilder().build();
    String xml = marshaller.marshall(original);
    AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
    assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
  }
}
Later we decide that our system won’t send an AuctionClosedEvent after all,
so we should be able to delete the class. Our refactoring attempt will fail because
AuctionClosedEvent is still being used by the XmlMarshallerTest. The irrelevant
coupling will force us to rework the test unnecessarily.
There’s a more signiﬁcant (and subtle) problem when we couple tests to domain
types: it’s harder to see when test assumptions have been broken. For example,
our XmlMarshallerTest also checks how the marshaller handles transient and
non-transient ﬁelds. When we wrote the tests, AuctionClosedEvent included both
kind of ﬁelds, so we were exercising all the paths through the marshaller. Later,
we removed the transient ﬁelds from AuctionClosedEvent, which means that we
have tests that are no longer meaningful but do not fail. Nothing is alerting us
that we have tests that have stopped working and that important features are
not being covered.
Chapter 24
Test Flexibility
284


