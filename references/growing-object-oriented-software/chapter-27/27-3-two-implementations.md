# 27.3 Two Implementations (pp.318-322)

---
**Page 318**

Put the Timeout Values in One Place
Both observation strategies use a timeout to detect that the system has failed.
Again, there’s a balance to be struck between a timeout that’s too short, which will
make the tests unreliable, and one that’s too long, which will make failing tests too
slow. This balance can be different in different environments, and will change as
the system grows over time.
When the timeout duration is deﬁned in one place, it’s easy to ﬁnd and change.
The team can adjust its value to ﬁnd the right balance between speed and reliability
as the system develops.
Two Implementations
Scattering ad hoc sleeps and timeouts throughout the tests makes them difﬁcult
to understand, because it leaves too much implementation detail in the tests
themselves. Synchronization and assertion is just the sort of behavior that’s
suitable for factoring out into subordinate objects because it usually turns into
a bad case of duplication if we don’t. It’s also just the sort of tricky code that we
want to get right once and not have to change again.
In this section, we’ll show an example implementation of each observation
strategy.
Capturing Notiﬁcations
An event-based assertion waits for an event by blocking on a monitor until it
gets notiﬁed or times out. When the monitor is notiﬁed, the test thread wakes
up and continues if it ﬁnds that the expected event has arrived, or blocks again.
If the test times out, then it raises a failure.
NotificationTrace is an example of how to record and test notiﬁcations sent
by the system. The setup of the test will arrange for the tested code to call
append() when the event happens, for example by plugging in an event listener
that will call the method when triggered. In the body of the test, the test thread
calls containsNotification() to wait for the expected notiﬁcation or fail if it
times out. For example:
trace.containsNotification(startsWith("WANTED"));
will wait for a notiﬁcation string that starts with WANTED.
Within NotificationTrace, incoming notiﬁcations are stored in a list trace,
which is protected by a lock traceLock. The class is generic, so we don’t specify
the type of these notiﬁcations, except to say that the matchers we pass into
containsNotification() must be compatible with that type. The implementation
uses Timeout and NotificationStream classes that we’ll describe later.
Chapter 27
Testing Asynchronous Code
318


---
**Page 319**

public class NotificationTrace<T> {
  private final Object traceLock = new Object();
  private final List<T> trace = new ArrayList<T>(); 1
  private long timeoutMs;
// constructors and accessors to configure the timeout […]
  public void append(T message) { 2
    synchronized (traceLock) {
      trace.add(message);
traceLock.notifyAll();
    }
  }
  public void containsNotification(Matcher<? super T> criteria) 3
    throws InterruptedException 
  { 
    Timeout timeout = new Timeout(timeoutMs); 
    synchronized (traceLock) {
      NotificationStream<T> stream = new NotificationStream<T>(trace, criteria);
      while (! stream.hasMatched()) {
        if (timeout.hasTimedOut()) {
          throw new AssertionError(failureDescriptionFrom(criteria));
        }
        timeout.waitOn(traceLock);
      }
    }
  }
  private String failureDescriptionFrom(Matcher<? super T> matcher) {  […] 
    // Construct a description of why there was no match, 
    // including the matcher and all the received messages. 
}
1
We store notiﬁcations in a list so that they’re available to us for other queries
and so that we can include them in a description if the test fails (we don’t
show how the description is constructed).
2
The append() method, called from a worker thread, appends a new notiﬁca-
tion to the trace, and then tells any threads waiting on traceLock to wake
up because there’s been a change. This is called by the test infrastructure
when triggered by an event in the system.
3
The containsNotification() method, called from the test thread, searches
through all the notiﬁcations it has received so far. If it ﬁnds a notiﬁcation
that matches the given criteria, it returns. Otherwise, it waits until more
notiﬁcations arrive and checks again. If it times out while waiting, then it
fails the test.
The nested NotificationStream class searches the unexamined elements in its
list for one that matches the given criteria. It allows the list to grow between calls
to hasMatched() and picks up after the last element it looked at.
319
Two Implementations


---
**Page 320**

private static class NotificationStream<N> {
  private final List<N> notifications;
  private final Matcher<? super N> criteria;
  private int next = 0;
  public NotificationStream(List<N> notifications, Matcher<? super N> criteria) {
    this.notifications = notifications;
    this.criteria = criteria;
  }
  public boolean hasMatched() {
    while (next < notifications.size()) {
      if (criteria.matches(notifications.get(next)))
        return true;
      next++;
    }
    return false;
  }
}
NotificationTrace is one example of a simple coordination class between test
and worker threads. It uses a simple approach, although it does avoid a possible
race condition where a background thread delivers a notiﬁcation before the test
thread has started waiting. Another implementation, for example, might have
containsNotification() only search messages received after the previous call.
What is appropriate depends on the context of the test.
Polling for Changes
A sample-based assertion repeatedly samples some visible effect of the system
through a “probe,” waiting for the probe to detect that the system has entered
an expected state. There are two aspects to the process of sampling: polling the
system and failure reporting, and probing the system for a given state. Separating
the two helps us think clearly about the behavior, and different tests can reuse the
polling with different probes.
Poller is an example of how to poll a system. It repeatedly calls its probe, with
a short delay between samples, until the system is ready or the poller times out.
The poller drives a probe that actually checks the target system, which we’ve
abstracted behind a Probe interface.
public interface Probe {
  boolean isSatisfied();
  void sample();
  void describeFailureTo(Description d);
}
The probe’s sample() method takes a snapshot of the system state that the test
is interested in. The isSatisfied() method returns true if that state meets the
test’s acceptance criteria. To simplify the poller logic, we allow isSatisfied()
to be called before sample().
Chapter 27
Testing Asynchronous Code
320


---
**Page 321**

public class Poller {
  private long timeoutMillis;
  private long pollDelayMillis;
// constructors and accessors to configure the timeout […]
  public void check(Probe probe) throws InterruptedException {
    Timeout timeout = new Timeout(timeoutMillis);
    while (! probe.isSatisfied()) {
      if (timeout.hasTimedOut()) {
        throw new AssertionError(describeFailureOf(probe));
      }
      Thread.sleep(pollDelayMillis);
      probe.sample();
    }
  }
  private String describeFailureOf(Probe probe) { […] 
}
This simple implementation delegates synchronization with the system to
the probe. A more sophisticated version might implement synchronization in the
poller, so it could be shared between probes. The similarity to NotificationTrace
is obvious, and we could have pulled out a common abstract structure, but we
wanted to keep the designs clear for now.
To poll, for example, for the length of a ﬁle, we would write this line in a test:
assertEventually(fileLength("data.txt", is(greaterThan(2000))));
This wraps up the construction of our sampling code in a more expressive
assertion. The helper methods to implement this are:
public static void assertEventually(Probe probe) throws InterruptedException {
  new Poller(1000L, 100L).check(probe);
}
public static Probe fileLength(String path, final Matcher<Integer> matcher) {
  final File file = new File(path);
  return new Probe() {
    private long lastFileLength = NOT_SET;
    public void sample() { lastFileLength = file.length(); }
    public boolean isSatisfied() { 
      return lastFileLength != NOT_SET && matcher.matches(lastFileLength);
    }
    public void describeFailureTo(Description d) {
      d.appendText("length was ").appendValue(lastFileLength);
    }
  };
}
Separating the act of sampling from checking whether the sample is satisfactory
makes the structure of the probe clearer. We can hold on to the sample result to
report the unsatisfactory result we found if there’s a failure.
321
Two Implementations


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


