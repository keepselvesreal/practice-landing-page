# 27.4 Runaway Tests (pp.322-323)

---
**Page 322**

Timing Out
Finally we show the Timeout class that the two example assertion classes use. It
packages up time checking and synchronization:
public class Timeout {
 private final long endTime;
  public Timeout(long duration) {
    this.endTime = System.currentTimeMillis() + duration;
  }
  public boolean hasTimedOut() { return timeRemaining() <= 0; }
  public void waitOn(Object lock) throws InterruptedException {
    long waitTime = timeRemaining();
    if (waitTime > 0) lock.wait(waitTime);
  }
  private long timeRemaining() { return endTime - System.currentTimeMillis(); }
}
Retroﬁtting a Probe
We can now rewrite the test from the introduction. Instead of making an assertion
about the current holding of a stock, the test must wait for the holding of the
stock to reach the expected level within an acceptable time limit.
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
Previously, the holdingOfStock() method returned a value to be compared.
Now it returns a Probe that samples the system’s holding and returns if it meets
the acceptance criteria deﬁned by a Hamcrest matcher—in this case equalTo(0).
Runaway Tests
Unfortunately, the new version of the test is still unreliable, even though we’re
now sampling for a result. The assertion is waiting for the holding to become
zero, which is what we started out with, so it’s possible for the test to pass before
the system has even begun processing. This test can run ahead of the system
without actually testing anything.
Chapter 27
Testing Asynchronous Code
322


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


