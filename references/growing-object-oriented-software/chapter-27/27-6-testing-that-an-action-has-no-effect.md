# 27.6 Testing That an Action Has No Effect (pp.325-326)

---
**Page 325**

This shows the limits of how precise we can be with a sampling test. All the
test can do between “stimulate” and “sample” is wait. We can write more
reliable tests by not confusing the different steps in the loop and only triggering
further changes once we’ve detected that the system is stable by observing a
change in its sampled state.
Testing That an Action Has No Effect
Asynchronous tests look for changes in a system, so to test that something has
not changed takes a little ingenuity. Synchronous tests don’t have this problem
because they completely control the execution of the tested code. After invoking
the target object, synchronous tests can query its state or check that it hasn’t
made any unexpected calls to its neighbors.
If an asynchronous test waits for something not to happen, it cannot even be
sure that the system has started before it checks the result. For example, if we
want to show that trades in another region are not counted in the stock holding,
then this test:
@Test public void doesNotShowTradesInOtherRegions() {
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
.inTradingRegion(OTHER_REGION));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
cannot tell whether the system has correctly ignored the trade or just not received
it yet. The most obvious workaround is for the test to wait for a ﬁxed period of
time and then check that the unwanted event did not occur. Unfortunately, this
makes the test run slowly even when successful, and so breaks our rule of
“succeed fast.”
Instead, the test should trigger a behavior that is detectable and use that to
detect that the system has stabilized. The skill here is in picking a behavior that
will not interfere with the test’s assertions and that will complete after the tested
behavior. For example, we could add another trade event to the regions example.
This shows that the out-of-region event is excluded because its quantity is not
included in the total holding.
@Test public void doesNotShowTradesInOtherRegions() {
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
                    .inTradingRegion(OTHER_REGION));
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(66)
                    .inTradingRegion(SAME_REGION));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(66)));
}
Of course, this test assumes that trade events are processed in sequence, not
in parallel, so that the second event cannot overtake the ﬁrst and give a false
positive. That’s why such tests are not completely “black box” but have to make
assumptions about the structure of the system. This might make these tests
325
Testing That an Action Has No Effect


---
**Page 326**

brittle—they would misreport if the system changes the assumptions they’ve been
built on. One response is to add a test to conﬁrm those expectations—in this
case, perhaps a stress test to conﬁrm event processing order and alert the team
if circumstances change. That said, there should already be other tests that conﬁrm
those assumptions, so it may be enough just to associate these tests, for example
by grouping them in the same test package.
Distinguish Synchronizations and Assertions
We have one mechanism for synchronizing a test with its system and for making
assertions about that system—wait for an observable condition and time out if
it doesn’t happen. The only difference between the two activities is our interpre-
tation of what they mean. As always, we want to make our intentions explicit,
but it’s especially important here because there’s a risk that someone may look
at the test later and remove what looks like a duplicate assertion, accidentally
introducing a race condition.
We often adopt a naming scheme to distinguish between synchronizations and
assertions. For example, we might have waitUntil() and assertEventually()
methods to express the purpose of different checks that share an underlying
implementation.
Alternatively, we might reserve the term “assert” for synchronous tests and
use a different naming conventions in asynchronous tests, as we did in the Auction
Sniper example.
Externalize Event Sources
Some systems trigger their own events internally. The most common example is
using a timer to schedule activities. This might include repeated actions that run
frequently, such as bundling up emails for forwarding, or follow-up actions that
run days or even weeks in the future, such as conﬁrming a delivery date.
Hidden timers are very difﬁcult to work with because they make it hard to tell
when the system is in a stable state for a test to make its assertions. Waiting for
a repeated action to run is too slow to “succeed fast,” to say nothing of an action
scheduled a month from now. We also don’t want tests to break unpredictably
because of interference from a scheduled activity that’s just kicked in. Trying to
test a system by coinciding timers is just too brittle.
The only solution is to make the system deterministic by decoupling it from
its own scheduling. We can pull event generation out into a shared service that
is driven externally. For example, in one project we implemented the system’s
scheduler as a web service. System components scheduled activities by making
HTTP requests to the scheduler, which triggered activities by making HTTP
“postbacks.” In another project, the scheduler published notiﬁcations onto a
message bus topic that the components listened to.
Chapter 27
Testing Asynchronous Code
326


