# 27.5 Lost Updates (pp.323-325)

---
**Page 323**

The worst aspect of runaway tests is that they give false positive results, so
broken code looks like it’s working. We don’t often review tests that pass, so it’s
easy to miss this kind of failure until something breaks down the line. Even more
tricky, the code might have worked when we ﬁrst wrote it, as the tests happened
to synchronize correctly during development, but now it’s broken and we
can’t tell.
Beware of Tests That Return the System to the Same State
Be careful when an asynchronous test asserts that the system returns to a previous
state. Unless it also asserts that the system enters an intermediate state before
asserting the initial state, the test will run ahead of the system.
To stop the test running ahead of the system, we must add assertions that wait
for the system to enter an intermediate state. Here, for example, we make sure
that the ﬁrst trade event has been processed before asserting the effect of the
second event:
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
assertEventually(holdingOfStock("A", tradeDate, equalTo(10)));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
Similarly, in Chapter 14, we check all the displayed states in the acceptance
tests for the Auction Sniper user interface:
auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
application.hasShownSniperIsWinning();
auction.announceClosed();
application.hasShownSniperHasWon();
We want to make sure that the sniper has responded to each message before
continuing on to the next one.
Lost Updates
A signiﬁcant difference between tests that sample and those that listen for events
is that polling can miss state changes that are later overwritten, Figure 27.1.
323
Lost Updates


---
**Page 324**

Figure 27.1
A test that polls can miss changes in the system
under test
If the test can record notiﬁcations from the system, it can look through its
records to ﬁnd signiﬁcant notiﬁcations.
Figure 27.2
A test that records notiﬁcations will not lose updates
To be reliable, a sampling test must make sure that its system is stable before
triggering any further interactions. Sampling tests need to be structured as a series
of phases, as shown in Figure 27.3. In each phase, the test sends a stimulus to
prompt a change in the observable state of the system, and then waits until that
change becomes visible or times out.
Figure 27.3
Phases of a sampling test
Chapter 27
Testing Asynchronous Code
324


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


