# 26.2 Separating Functionality and Concurrency Policy (pp.302-306)

---
**Page 302**

but the application must synchronize the Smack thread and the Swing thread
to avoid the GUI components being corrupted.
When you must design a system’s concurrency architecture from scratch, you
can use modeling tools to prove your design free of certain classes of synchroniza-
tion errors, such as deadlock, livelock, or starvation. Design tools that help you
model concurrency are becoming increasingly easy to use. The book Concurrency:
State Models & Java Programs [Magee06] is an introduction to concurrent pro-
gramming that stresses a combination of formal modeling and implementation
and describes how to do the formal modeling with the LTSA analysis tool.
Even with a proven design, however, we have to cross the chasm between design
and implementation. We need to ensure that our components conform to the
architectural constraints of the system. Testing can help at this point. Once we’ve
designed how the system will manage concurrency, we can test-drive the objects
that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
performs its synchronization responsibilities, such as locking its state or blocking
and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
that the entire system manages concurrency correctly.
Separating Functionality and Concurrency Policy
Objects that cope with multiple threads mix functional concerns with synchro-
nization concerns, either of which can be the cause of test failures. Tests must
also synchronize with the background threads, so that they don’t make assertions
before the threads have ﬁnished working or leave threads running that might
interfere with later tests. Worse, in the presence of threads, unit tests do not
usually report failures well. Exceptions get thrown on the hidden threads, killing
them unexpectedly and breaking the behavior of the tested object. If a test times
out waiting for background threads to ﬁnish, there’s often no diagnostic other
than a basic timeout message. All this makes unit testing difﬁcult.
Searching for Auctions Concurrently
Let’s look at an example. We will extend our Auction Sniper application to let
the user search for auctions of interest. When the user enters search
keywords, the application will run the search concurrently on all auction houses
that the application can connect to. Each AuctionHouse will return a list of
AuctionDescriptions that contain information about its auctions matching the
search keywords. The application will combine the results it receives from all
AuctionHouses and display a single list of auctions to the user. The user can then
decide which of them to bid for.
The concurrent search is performed by an AuctionSearch object which passes
the search keywords to each AuctionHouse and announces the results they return
Chapter 26
Unit Testing and Threads
302


---
**Page 303**

to an AuctionSearchConsumer. Our tests for the Auction Search are complicated
because an AuctionSearch will spawn multiple threads per search, one for each
AuctionHouse. If it hides those threads behind its API, we will have to implement
the searching and notiﬁcation functionality and the synchronization at the same
time. When a test fails, we will have to work out which of those concerns is at
fault. That’s why we prefer our usual practice of incrementally adding
functionality test by test.
It would be easier to test and implement the AuctionSearch if we could tackle
the functional behavior and the synchronization separately. This would allow
us to test the functional behavior within the test thread. We want to separate the
logic that splits a request into multiple tasks from the technical details of how
those tasks are executed concurrently. So we pass a “task runner” in to the
AuctionSearch, which can then delegate managing tasks to the runner instead of
starting threads itself. In our unit tests we’ll give the AuctionSearch a fake task
runner that calls tasks directly. In the real system, we’ll give it a task runner that
creates threads for tasks.
Introducing an Executor
We need an interface between the AuctionHouse and the task runner. We can use
this one from Java’s standard java.util.concurrent package:
public interface Executor {
  void execute(Runnable command);
}
How should we implement Executor in our unit tests? For testing, we need to
run the tasks in the same thread as the test runner instead of creating new task
threads. We could use jMock to mock Executor and write a custom action to
capture all calls so we can run them later, but that sounds too complicated. The
easiest option is to write a class to implement Executor. We can us it to explicitly
run the tasks on the test thread after the call to the tested object has returned.
jMock includes such a class, called DeterministicExecutor. We use this
executor to write our ﬁrst unit test. It checks that AuctionSearch notiﬁes its
AuctionSearchConsumer whenever an AuctionHouse returns search results and
when the entire search has ﬁnished.
In the test setup, we mock the consumer because we want to show how
it’s notiﬁed by AuctionSearch. We represent auction houses with a simple
StubAuctionHouse that just returns a list of descriptions if it matches keywords,
or an empty list if not (real ones would communicate to auction services over
the Internet). We wrote a custom stub, instead of using a jMock allowance, to
reduce the “noise” in the failure reports; you’ll see how this matters when
we start stress-testing in the next section. We also pass an instance of
DeterministicExecutor to AuctionSearch so that we can run the tasks within
the test thread.
303
Separating Functionality and Concurrency Policy


---
**Page 304**

@RunWith(JMock.class)
public class AuctionSearchTests {
  Mockery context = new JUnit4Mockery();
  final DeterministicExecutor executor = new DeterministicExecutor();
  final StubAuctionHouse houseA = new StubAuctionHouse("houseA");
  final StubAuctionHouse houseB = new StubAuctionHouse("houseB");
  List<AuctionDescription> resultsFromA = asList(auction(houseA, "1"));
  List<AuctionDescription> resultsFromB = asList(auction(houseB, "2"));;
  final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
  final AuctionSearch search = 
                        new AuctionSearch(executor, houses(houseA, houseB), consumer);
  @Test public void 
searchesAllAuctionHouses() throws Exception {
    final Set<String> keywords = set("sheep", "cheese");
    houseA.willReturnSearchResults(keywords, resultsFromA);
    houseB.willReturnSearchResults(keywords, resultsFromB);
    context.checking(new Expectations() {{
      final States searching = context.states("searching");
      oneOf(consumer).auctionSearchFound(resultsFromA); when(searching.isNot("done"));
      oneOf(consumer).auctionSearchFound(resultsFromB); when(searching.isNot("done"));
      oneOf(consumer).auctionSearchFinished();          then(searching.is("done"));
    }});
    search.search(keywords);
executor.runUntilIdle();
  }
}
In the test, we conﬁgure the StubAuctionHouses to return example results when
they’re queried with the given keywords. We specify our expectations that the
consumer will be notiﬁed of the two search results (in any order), and then that
the search has ﬁnished.
When we call search.search(keywords), the AuctionSearch hands a task for
each of its auction houses to the executor. By the time search() returns, the tasks
to run are queued in the executor. Finally, we call executor.runUntilIdle() to
tell the executor to run queued tasks until its queue is empty. The tasks run on
the test thread, so any assertion failures will be caught and reported by JUnit,
and we don’t have to worry about synchronizing the test thread with background
threads.
Implementing AuctionSearch
This implementation of AuctionSearch calls its executor to start a search for
each of its auction houses. It tracks how many searches are unﬁnished in its
runningSearchCount ﬁeld, so that it can notify the consumer when it’s ﬁnished.
Chapter 26
Unit Testing and Threads
304


---
**Page 305**

public class AuctionSearch {
  private final Executor executor;
  private final List<AuctionHouse> auctionHouses;
  private final AuctionSearchConsumer consumer;
private int runningSearchCount = 0;
  public AuctionSearch(Executor executor, 
                       List<AuctionHouse> auctionHouses, 
                       AuctionSearchConsumer consumer) 
  {
    this.executor = executor;
    this.auctionHouses = auctionHouses;
    this.consumer = consumer;
  }
  public void search(Set<String> keywords) {
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
runningSearchCount++;
    executor.execute(new Runnable() {
      public void run() {
        search(auctionHouse, keywords);
      }
    });
  }
  private void search(AuctionHouse auctionHouse, Set<String> keywords) {
    consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
runningSearchCount--;
    if (runningSearchCount == 0) {
      consumer.auctionSearchFinished();
    }
  }
}
Unfortunately, this version is unsafe because it doesn’t synchronize access to
runningSearchCount. Different threads may overwrite each other when they
decrement the ﬁeld. So far, we’ve clariﬁed the core behavior. We’ll drive out this
synchronization issue in the next test. Pulling out the Executor has given us two
advantages. First, it makes development easier as we can unit-test the basic
functionality without getting confused by threading issues. Second, the object’s
API no longer hides its concurrency policy.
Concurrency is a system-wide concern that should be controlled outside the
objects that need to run concurrent tasks. By passing an appropriate Executor
to the constructor, we’re following the “context independence” design principle.
305
Separating Functionality and Concurrency Policy


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


