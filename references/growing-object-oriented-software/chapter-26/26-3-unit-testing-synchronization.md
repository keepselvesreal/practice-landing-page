# 26.3 Unit-Testing Synchronization (pp.306-311)

---
**Page 306**

The application can now easily adapt the object to the application’s threading
policy without changing its implementation. For example, we could introduce a
thread pool should we need to limit the number of active threads.
Unit-Testing Synchronization
Separating the functional and synchronization concerns has let us test-drive the
functional behavior of our AuctionSearch in isolation. Now it’s time to test-drive
the synchronization. We will do this by writing stress-tests that run multiple
threads through the AuctionSearch implementation to cause synchronization
errors. Without precise control over the thread scheduler, we can’t guarantee
that our tests will ﬁnd synchronization errors. The best we can do is run the same
code enough times on enough threads to give our tests a reasonable likelihood
of detecting the errors.
One approach to designing stress tests is to think about the aspects of an ob-
ject’s observable behavior that are independent of the number of threads calling
into the object. These are the object’s observable invariants with respect to con-
currency.1 By focusing on these invariants, we can tune the number of threads
in a test without having to change its assertions. This gives us a process for
writing stress tests:
•
Specify one of the object’s observable invariants with respect to concurrency;
•
Write a stress test for the invariant that exercises the object multiple times
from multiple threads;
•
Watch the test fail, and tune the stress test until it reliably fails on every
test run; and,
•
Make the test pass by adding synchronization.
We’ll demonstrate this with an example.
Safety First
In this chapter we have made the unit tests of functional behavior pass before we
covered stress testing at the unit level because that allowed us to explain each
technique on its own. In practice, however, we often write both a unit test for func-
tionality and a stress test of the synchronization before writing any code, make
sure they both fail, then make them both pass.This helps us avoid checking in code
that passes its tests but contains concurrency errors.
1. This differs from the use of invariants in “design by contract” and formal methods
of modeling concurrency. These deﬁne invariants over the object’s state.
Chapter 26
Unit Testing and Threads
306


---
**Page 307**

A Stress Test for AuctionSearch
One invariant of our AuctionSearch is that it notiﬁes the consumer just once
when the search has ﬁnished, no matter how many AuctionHouses it searches—that
is, no matter how many threads its starts.
We can use jMock to write a stress test for this invariant. We don’t always use
jMock for stress tests because expectation failures interfere with the threads of
the object under test. On the other hand, jMock reports the actual sequence
of calls to its mock objects when there is a failure, which helps diagnose defects.
It also provides convenient facilities for synchronizing between the test thread
and the threads being tested.
In AuctionSearchStressTests, we set up AuctionSearch with a thread-pool
executor that will run tasks in background threads, and a list of auction houses
stubbed to match on the given keywords. jMock is not thread-safe by default,
so we set up the Mockery with a Synchroniser, an implementation of its threading
policy that allows us to call mocked objects from different threads. To make
tuning the test easier, we deﬁne constants at the top for the “degree of stress”
we’ll apply during the run.
@RunWith(JMock.class)
public class AuctionSearchStressTests {
  private static final int NUMBER_OF_AUCTION_HOUSES = 4; 
  private static final int NUMBER_OF_SEARCHES = 8;
  private static final Set<String> KEYWORDS = setOf("sheep", "cheese");
  final Synchroniser synchroniser = new Synchroniser();
  final Mockery context = new JUnit4Mockery() {{
    setThreadingPolicy(synchroniser);
  }};
  final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
  final States searching = context.states("searching");
  final ExecutorService executor = Executors.newCachedThreadPool();
  final AuctionSearch search = new AuctionSearch(executor, auctionHouses(), consumer); 
[…]
  private List<AuctionHouse> auctionHouses() {
    ArrayList<AuctionHouse> auctionHouses = new ArrayList<AuctionHouse>();
    for (int i = 0; i < NUMBER_OF_AUCTION_HOUSES; i++) {
      auctionHouses.add(stubbedAuctionHouse(i));
    }
    return auctionHouses;
  }
  private AuctionHouse stubbedAuctionHouse(final int id) {
    StubAuctionHouse house = new StubAuctionHouse("house" + id);
    house.willReturnSearchResults(
        KEYWORDS, asList(new AuctionDescription(house, "id" + id, "description")));
    return house;
  } 
307
Unit-Testing Synchronization


---
**Page 308**

  @Test(timeout=500) public void 
onlyOneAuctionSearchFinishedNotificationPerSearch() throws Exception {
    context.checking(new Expectations() {{ 
      ignoring (consumer).auctionSearchFound(with(anyResults()));
    }});
    for (int i = 0; i < NUMBER_OF_SEARCHES; i++) { 
      completeASearch();
    }
  }
  private void completeASearch() throws InterruptedException {
    searching.startsAs("in progress");
    context.checking(new Expectations() {{
      exactly(1).of(consumer).auctionSearchFinished(); then(searching.is("done"));
    }});
    search.search(KEYWORDS);
synchroniser.waitUntil(searching.is("done")); 
  }
  @After
  public void cleanUp() throws InterruptedException {
executor.shutdown();
executor.awaitTermination(1, SECONDS);
  }
}
In the test method onlyOneAuctionSearchFinishedNotificationPerSearch(),
we run a complete search NUMBER_OF_SEARCHES times, to increase the likelihood
of ﬁnding any race conditions. It ﬁnishes each search by asking synchroniser
to wait until it’s collected all the background threads the executor has
launched, or until it’s timed out. Synchroniser provides a method that will
safely wait until a state machine is (or is not) in a given state. The test ignores
auctionSearchFound() notiﬁcations, since here we’re only interested in making
sure that the searches ﬁnish cleanly. Finally, we shut down executor in the test
teardown.
It’s important to watch a stress test fail. It’s too easy to write a test that passes
even though the tested object has a synchronization hole. So, we “test the test”
by making it fail before we’ve synchronized the code, and checking that we get
the failure report we expected. If we don’t, then we might need to raise the
numbers of threads or iterations per thread until we can trust the test to reveal
the error.2 Then we add the synchronization to make the test pass. Here’s our
test failure:
2. Of course, the stress parameters may differ between environments, such as develop-
ment vs. build. We can’t follow that through here, except to note that it needs
addressing.
Chapter 26
Unit Testing and Threads
308


---
**Page 309**

java.lang.AssertionError: unexpected invocation: consumer.auctionSearchFinished()
expectations:
  allowed, already invoked 5 times: consumer.auctionSearchFound(ANYTHING)
  expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
                                                           then searching is done
  expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
                                                           then searching is done
states:
  searching is done
what happened before this:
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
  consumer.auctionSearchFinished()
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
  consumer.auctionSearchFinished()
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
This says that AuctionSearch has called auctionFinished() once too often.
Fixing the Race Condition (Twice)
We haven’t synchronized access to runningSearchCount. If we use an
AtomicInteger from the Java concurrency libraries instead of a plain int, the
threads should be able to decrement it without interfering with each other.
public class AuctionSearch { […]
private final AtomicInteger runningSearchCount = new AtomicInteger();
  public void search(Set<String> keywords) {
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
runningSearchCount.incrementAndGet();
    executor.execute(new Runnable() {
      public void run() { search(auctionHouse, keywords); }
    });
  }
  private void search(AuctionHouse auctionHouse, Set<String> keywords) {
    consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
    if (runningSearchCount.decrementAndGet() == 0) {
      consumer.auctionSearchFinished();
    }
  }
}
309
Unit-Testing Synchronization


---
**Page 310**

We try this and, in spite of our use of an AtomicInteger, our test still fails! We
haven’t got our synchronization right after all.
We look again at the failure and see that now the AuctionSearch is
reporting that the search has ﬁnished more than once per search. Previously,
the unsafe concurrent access to runningSearchCount resulted in fewer
auctionSearchFinshed() notiﬁcations than expected, because AuctionSearch
was losing updates to the ﬁeld. Something else must be wrong.
As an eagle-eyed reader, you’ll have noticed a race condition in the way
AuctionSearch increments and decrements runningSearchCount. It increments
the count before starting a task thread. Once the main thread has started creating
task threads, the thread scheduler can preëmpt it and start running whatever task
threads are ready—while the main thread still has search tasks left to create. If
all these started task threads complete before the scheduler resumes the main
thread, they will decrement the count to 0 and the last one will send an
auctionSearchFinshed() notiﬁcation. When the main thread ﬁnally resumes, it
will continue by starting its remaining searches, which will eventually trigger
another notiﬁcation.
This sort of error shows why we need to write stress tests, to make sure that
we see them fail, and to understand the failure messages—it’s also a good moti-
vation for us to write comprehensible failure reports. This example also highlights
the beneﬁts of splitting tests of “raw” functionality from threaded tests. With the
single-threaded version stable, we know we can concentrate on looking for race
conditions in the stress tests.
We ﬁx the code by setting runningSearchCount to the expected number of
searches before starting any threads:
public class AuctionSearch { […]
  public void search(Set<String> keywords) {
runningSearchCount.set(auctionHouses.size());
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
// no longer increments the count here
    executor.execute(new Runnable() {
      public void run() { search(auctionHouse, keywords); }
    });
  }
}
Chapter 26
Unit Testing and Threads
310


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


