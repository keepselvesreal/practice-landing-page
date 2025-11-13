# 26.4 Stress-Testing Passive Objects (pp.311-312)

---
**Page 311**

Stress-Testing Passive Objects
AuctionSearch actively starts multiple threads by calling out to its executor.
Most objects that are concerned with threading, however, don’t start threads
themselves but have multiple threads “pass through” them and alter their state.
Servlets, for example, are required to support multiple threads touching the same
instance. In such cases, an object must synchronize access to any state that might
cause a race condition.
To stress-test the synchronization of a passive object, the test must start its
own threads to call the object. When all the threads have ﬁnished, the state of
the object should be the same as if those calls had happened in sequence. For
example, AtomicBigCounter below does not synchronize access to its count vari-
able. It works when called from a single thread but can lose updates when called
from multiple threads:
public class AtomicBigCounter {
  private BigInteger count = BigInteger.ZERO;
  public BigInteger count() { return count; }
  public void inc() { count = count.add(BigInteger.ONE); }
}
We can show this failure by calling inc() from multiple threads enough times
to give us a good chance of causing the race condition and losing an update.
When this happens, the ﬁnal result of count() will be less than the number of
times we’ve called inc().
We could spin up multiple threads directly in our test, but the mess of detail
for launching and synchronizing threads would get in the way of understanding
the intent. The threading concerns are a good candidate for extracting into a
subordinate object, MultiThreadedStressTester, which we use to call the counter’s
inc() method:
public class AtomicBigCounterTests { […]
  final AtomicBigCounter counter = new AtomicBigCounter();
  @Test public void
canIncrementCounterFromMultipleThreadsSimultaneously() throws InterruptedException {
    MultithreadedStressTester stressTester = new MultithreadedStressTester(25000);
    stressTester.stress(new Runnable() {
      public void run() {
        counter.inc();
      }
    });
    stressTester.shutdown();
    assertThat("final count", counter.count(), 
               equalTo(BigInteger.valueOf(stressTester.totalActionCount())));
  }
}
311
Stress-Testing Passive Objects


---
**Page 312**

The test fails, showing the race condition in AtomicBigCounter:
java.lang.AssertionError: final count
Expected: <50000>
     got: <36933>
We pass the test by making the inc() and count() methods synchronized.
Synchronizing the Test Thread with Background Threads
When writing a test for code that starts threads, the test cannot conﬁrm the code’s
behavior until it has synchronized its thread with any threads the code has
started. For example, in AuctionSearchStressTests we make the test thread wait
until all the task threads launched by AuctionSearch have been completed. Syn-
chronizing with background threads can be challenging, especially if the tested
object does not delegate to an executor to run concurrent tasks.
The easiest way to ensure that threads have ﬁnished is for the test to sleep long
enough for them all to run to completion. For example:
private void waitForSearchToFinish() throws InterruptedException {
  Thread.sleep(250);
}
This works for occasional use—a sub-second delay in a few tests won’t be
noticeable—but it doesn’t scale. As the number of tests with delays grows, the
total delay adds up and the test suite slows down so much that running it becomes
a distraction. We must be able to run all the unit tests so quickly as to not even
think about whether we should. The other problem with ﬁxed sleeps is that our
choice of delay has to apply across all the environments where the tests run. A
delay suitable for an underpowered machine will slow the tests everywhere else,
and introducing a new environment may force another round of tuning.
An alternative, as we saw in AuctionSearchStressTests, is to use jMock’s
Synchroniser. It provides support for synchronizing between test and background
threads, based on whether a state machine has entered or left a given state:
synchroniser.waitUntil(searching.is("finished"));
synchroniser.waitUntil(searching.isNot("in progress"));
These methods will block forever for a failing test, where the state machine never
meets the speciﬁed criteria, so they should be used with a timeout added to the
test declaration:
@Test(timeout=500)
This tells the test runnner to force a failure if the test overruns the timeout period.
Chapter 26
Unit Testing and Threads
312


