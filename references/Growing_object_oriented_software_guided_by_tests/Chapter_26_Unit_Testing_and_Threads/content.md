Line 1: 
Line 2: --- 페이지 326 ---
Line 3: Chapter 26
Line 4: Unit Testing and Threads
Line 5: It is decreed by a merciful Nature that the human brain cannot think
Line 6: of two things simultaneously.
Line 7: —Sir Arthur Conan Doyle
Line 8: Introduction
Line 9: There’s no getting away from it: concurrency complicates matters. It is a challenge
Line 10: when doing test-driven development. Unit tests cannot give you as much
Line 11: conﬁdence in system quality because concurrency and synchronization are system-
Line 12: wide concerns. When writing tests, you have to worry about getting the synchro-
Line 13: nization right within the system and between the test and the system. Test failures
Line 14: are harder to diagnose because exceptions may be swallowed by background
Line 15: threads or tests may just time out with no clear explanation.
Line 16: It’s hard to diagnose and correct synchronization problems in existing code,
Line 17: so it’s worth thinking about the system’s concurrency architecture ahead of
Line 18: time. You don’t need to design it in great detail, just decide on a broad-brush
Line 19: architecture and principles by which the system will cope with concurrency.
Line 20: This design is often prescribed by the frameworks or libraries that an
Line 21: application uses. For example:
Line 22: •
Line 23: Swing dispatches user events on its own thread. If an event handler runs
Line 24: for a long time, the user interface becomes unresponsive because Swing
Line 25: does not process user input while the event handler is running. Event call-
Line 26: backs must spawn “worker” threads to perform long-running tasks, and
Line 27: those worker threads must synchronize with the event dispatch thread to
Line 28: update the user interface.
Line 29: •
Line 30: A servlet container has a pool of threads that receive HTTP requests and
Line 31: pass them to servlets for processing. Many threads can be active in the same
Line 32: servlet instance at once.
Line 33: •
Line 34: Java EE containers manage all the threading in the application. The contain-
Line 35: er guarantees that only one thread will call into a component at a time.
Line 36: Components cannot start their own threads.
Line 37: •
Line 38: The Smack library used by the Auction Sniper application starts a daemon
Line 39: thread to receive XMPP messages. It will deliver messages on a single thread,
Line 40: 301
Line 41: 
Line 42: --- 페이지 327 ---
Line 43: but the application must synchronize the Smack thread and the Swing thread
Line 44: to avoid the GUI components being corrupted.
Line 45: When you must design a system’s concurrency architecture from scratch, you
Line 46: can use modeling tools to prove your design free of certain classes of synchroniza-
Line 47: tion errors, such as deadlock, livelock, or starvation. Design tools that help you
Line 48: model concurrency are becoming increasingly easy to use. The book Concurrency:
Line 49: State Models & Java Programs [Magee06] is an introduction to concurrent pro-
Line 50: gramming that stresses a combination of formal modeling and implementation
Line 51: and describes how to do the formal modeling with the LTSA analysis tool.
Line 52: Even with a proven design, however, we have to cross the chasm between design
Line 53: and implementation. We need to ensure that our components conform to the
Line 54: architectural constraints of the system. Testing can help at this point. Once we’ve
Line 55: designed how the system will manage concurrency, we can test-drive the objects
Line 56: that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
Line 57: performs its synchronization responsibilities, such as locking its state or blocking
Line 58: and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
Line 59: that the entire system manages concurrency correctly.
Line 60: Separating Functionality and Concurrency Policy
Line 61: Objects that cope with multiple threads mix functional concerns with synchro-
Line 62: nization concerns, either of which can be the cause of test failures. Tests must
Line 63: also synchronize with the background threads, so that they don’t make assertions
Line 64: before the threads have ﬁnished working or leave threads running that might
Line 65: interfere with later tests. Worse, in the presence of threads, unit tests do not
Line 66: usually report failures well. Exceptions get thrown on the hidden threads, killing
Line 67: them unexpectedly and breaking the behavior of the tested object. If a test times
Line 68: out waiting for background threads to ﬁnish, there’s often no diagnostic other
Line 69: than a basic timeout message. All this makes unit testing difﬁcult.
Line 70: Searching for Auctions Concurrently
Line 71: Let’s look at an example. We will extend our Auction Sniper application to let
Line 72: the user search for auctions of interest. When the user enters search
Line 73: keywords, the application will run the search concurrently on all auction houses
Line 74: that the application can connect to. Each AuctionHouse will return a list of
Line 75: AuctionDescriptions that contain information about its auctions matching the
Line 76: search keywords. The application will combine the results it receives from all
Line 77: AuctionHouses and display a single list of auctions to the user. The user can then
Line 78: decide which of them to bid for.
Line 79: The concurrent search is performed by an AuctionSearch object which passes
Line 80: the search keywords to each AuctionHouse and announces the results they return
Line 81: Chapter 26
Line 82: Unit Testing and Threads
Line 83: 302
Line 84: 
Line 85: --- 페이지 328 ---
Line 86: to an AuctionSearchConsumer. Our tests for the Auction Search are complicated
Line 87: because an AuctionSearch will spawn multiple threads per search, one for each
Line 88: AuctionHouse. If it hides those threads behind its API, we will have to implement
Line 89: the searching and notiﬁcation functionality and the synchronization at the same
Line 90: time. When a test fails, we will have to work out which of those concerns is at
Line 91: fault. That’s why we prefer our usual practice of incrementally adding
Line 92: functionality test by test.
Line 93: It would be easier to test and implement the AuctionSearch if we could tackle
Line 94: the functional behavior and the synchronization separately. This would allow
Line 95: us to test the functional behavior within the test thread. We want to separate the
Line 96: logic that splits a request into multiple tasks from the technical details of how
Line 97: those tasks are executed concurrently. So we pass a “task runner” in to the
Line 98: AuctionSearch, which can then delegate managing tasks to the runner instead of
Line 99: starting threads itself. In our unit tests we’ll give the AuctionSearch a fake task
Line 100: runner that calls tasks directly. In the real system, we’ll give it a task runner that
Line 101: creates threads for tasks.
Line 102: Introducing an Executor
Line 103: We need an interface between the AuctionHouse and the task runner. We can use
Line 104: this one from Java’s standard java.util.concurrent package:
Line 105: public interface Executor {
Line 106:   void execute(Runnable command);
Line 107: }
Line 108: How should we implement Executor in our unit tests? For testing, we need to
Line 109: run the tasks in the same thread as the test runner instead of creating new task
Line 110: threads. We could use jMock to mock Executor and write a custom action to
Line 111: capture all calls so we can run them later, but that sounds too complicated. The
Line 112: easiest option is to write a class to implement Executor. We can us it to explicitly
Line 113: run the tasks on the test thread after the call to the tested object has returned.
Line 114: jMock includes such a class, called DeterministicExecutor. We use this
Line 115: executor to write our ﬁrst unit test. It checks that AuctionSearch notiﬁes its
Line 116: AuctionSearchConsumer whenever an AuctionHouse returns search results and
Line 117: when the entire search has ﬁnished.
Line 118: In the test setup, we mock the consumer because we want to show how
Line 119: it’s notiﬁed by AuctionSearch. We represent auction houses with a simple
Line 120: StubAuctionHouse that just returns a list of descriptions if it matches keywords,
Line 121: or an empty list if not (real ones would communicate to auction services over
Line 122: the Internet). We wrote a custom stub, instead of using a jMock allowance, to
Line 123: reduce the “noise” in the failure reports; you’ll see how this matters when
Line 124: we start stress-testing in the next section. We also pass an instance of
Line 125: DeterministicExecutor to AuctionSearch so that we can run the tasks within
Line 126: the test thread.
Line 127: 303
Line 128: Separating Functionality and Concurrency Policy
Line 129: 
Line 130: --- 페이지 329 ---
Line 131: @RunWith(JMock.class)
Line 132: public class AuctionSearchTests {
Line 133:   Mockery context = new JUnit4Mockery();
Line 134:   final DeterministicExecutor executor = new DeterministicExecutor();
Line 135:   final StubAuctionHouse houseA = new StubAuctionHouse("houseA");
Line 136:   final StubAuctionHouse houseB = new StubAuctionHouse("houseB");
Line 137:   List<AuctionDescription> resultsFromA = asList(auction(houseA, "1"));
Line 138:   List<AuctionDescription> resultsFromB = asList(auction(houseB, "2"));;
Line 139:   final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
Line 140:   final AuctionSearch search = 
Line 141:                         new AuctionSearch(executor, houses(houseA, houseB), consumer);
Line 142:   @Test public void 
Line 143: searchesAllAuctionHouses() throws Exception {
Line 144:     final Set<String> keywords = set("sheep", "cheese");
Line 145:     houseA.willReturnSearchResults(keywords, resultsFromA);
Line 146:     houseB.willReturnSearchResults(keywords, resultsFromB);
Line 147:     context.checking(new Expectations() {{
Line 148:       final States searching = context.states("searching");
Line 149:       oneOf(consumer).auctionSearchFound(resultsFromA); when(searching.isNot("done"));
Line 150:       oneOf(consumer).auctionSearchFound(resultsFromB); when(searching.isNot("done"));
Line 151:       oneOf(consumer).auctionSearchFinished();          then(searching.is("done"));
Line 152:     }});
Line 153:     search.search(keywords);
Line 154: executor.runUntilIdle();
Line 155:   }
Line 156: }
Line 157: In the test, we conﬁgure the StubAuctionHouses to return example results when
Line 158: they’re queried with the given keywords. We specify our expectations that the
Line 159: consumer will be notiﬁed of the two search results (in any order), and then that
Line 160: the search has ﬁnished.
Line 161: When we call search.search(keywords), the AuctionSearch hands a task for
Line 162: each of its auction houses to the executor. By the time search() returns, the tasks
Line 163: to run are queued in the executor. Finally, we call executor.runUntilIdle() to
Line 164: tell the executor to run queued tasks until its queue is empty. The tasks run on
Line 165: the test thread, so any assertion failures will be caught and reported by JUnit,
Line 166: and we don’t have to worry about synchronizing the test thread with background
Line 167: threads.
Line 168: Implementing AuctionSearch
Line 169: This implementation of AuctionSearch calls its executor to start a search for
Line 170: each of its auction houses. It tracks how many searches are unﬁnished in its
Line 171: runningSearchCount ﬁeld, so that it can notify the consumer when it’s ﬁnished.
Line 172: Chapter 26
Line 173: Unit Testing and Threads
Line 174: 304
Line 175: 
Line 176: --- 페이지 330 ---
Line 177: public class AuctionSearch {
Line 178:   private final Executor executor;
Line 179:   private final List<AuctionHouse> auctionHouses;
Line 180:   private final AuctionSearchConsumer consumer;
Line 181: private int runningSearchCount = 0;
Line 182:   public AuctionSearch(Executor executor, 
Line 183:                        List<AuctionHouse> auctionHouses, 
Line 184:                        AuctionSearchConsumer consumer) 
Line 185:   {
Line 186:     this.executor = executor;
Line 187:     this.auctionHouses = auctionHouses;
Line 188:     this.consumer = consumer;
Line 189:   }
Line 190:   public void search(Set<String> keywords) {
Line 191:     for (AuctionHouse auctionHouse : auctionHouses) {
Line 192:       startSearching(auctionHouse, keywords);
Line 193:     }
Line 194:   }
Line 195:   private void startSearching(final AuctionHouse auctionHouse, 
Line 196:                               final Set<String> keywords) 
Line 197:   {
Line 198: runningSearchCount++;
Line 199:     executor.execute(new Runnable() {
Line 200:       public void run() {
Line 201:         search(auctionHouse, keywords);
Line 202:       }
Line 203:     });
Line 204:   }
Line 205:   private void search(AuctionHouse auctionHouse, Set<String> keywords) {
Line 206:     consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
Line 207: runningSearchCount--;
Line 208:     if (runningSearchCount == 0) {
Line 209:       consumer.auctionSearchFinished();
Line 210:     }
Line 211:   }
Line 212: }
Line 213: Unfortunately, this version is unsafe because it doesn’t synchronize access to
Line 214: runningSearchCount. Different threads may overwrite each other when they
Line 215: decrement the ﬁeld. So far, we’ve clariﬁed the core behavior. We’ll drive out this
Line 216: synchronization issue in the next test. Pulling out the Executor has given us two
Line 217: advantages. First, it makes development easier as we can unit-test the basic
Line 218: functionality without getting confused by threading issues. Second, the object’s
Line 219: API no longer hides its concurrency policy.
Line 220: Concurrency is a system-wide concern that should be controlled outside the
Line 221: objects that need to run concurrent tasks. By passing an appropriate Executor
Line 222: to the constructor, we’re following the “context independence” design principle.
Line 223: 305
Line 224: Separating Functionality and Concurrency Policy
Line 225: 
Line 226: --- 페이지 331 ---
Line 227: The application can now easily adapt the object to the application’s threading
Line 228: policy without changing its implementation. For example, we could introduce a
Line 229: thread pool should we need to limit the number of active threads.
Line 230: Unit-Testing Synchronization
Line 231: Separating the functional and synchronization concerns has let us test-drive the
Line 232: functional behavior of our AuctionSearch in isolation. Now it’s time to test-drive
Line 233: the synchronization. We will do this by writing stress-tests that run multiple
Line 234: threads through the AuctionSearch implementation to cause synchronization
Line 235: errors. Without precise control over the thread scheduler, we can’t guarantee
Line 236: that our tests will ﬁnd synchronization errors. The best we can do is run the same
Line 237: code enough times on enough threads to give our tests a reasonable likelihood
Line 238: of detecting the errors.
Line 239: One approach to designing stress tests is to think about the aspects of an ob-
Line 240: ject’s observable behavior that are independent of the number of threads calling
Line 241: into the object. These are the object’s observable invariants with respect to con-
Line 242: currency.1 By focusing on these invariants, we can tune the number of threads
Line 243: in a test without having to change its assertions. This gives us a process for
Line 244: writing stress tests:
Line 245: •
Line 246: Specify one of the object’s observable invariants with respect to concurrency;
Line 247: •
Line 248: Write a stress test for the invariant that exercises the object multiple times
Line 249: from multiple threads;
Line 250: •
Line 251: Watch the test fail, and tune the stress test until it reliably fails on every
Line 252: test run; and,
Line 253: •
Line 254: Make the test pass by adding synchronization.
Line 255: We’ll demonstrate this with an example.
Line 256: Safety First
Line 257: In this chapter we have made the unit tests of functional behavior pass before we
Line 258: covered stress testing at the unit level because that allowed us to explain each
Line 259: technique on its own. In practice, however, we often write both a unit test for func-
Line 260: tionality and a stress test of the synchronization before writing any code, make
Line 261: sure they both fail, then make them both pass.This helps us avoid checking in code
Line 262: that passes its tests but contains concurrency errors.
Line 263: 1. This differs from the use of invariants in “design by contract” and formal methods
Line 264: of modeling concurrency. These deﬁne invariants over the object’s state.
Line 265: Chapter 26
Line 266: Unit Testing and Threads
Line 267: 306
Line 268: 
Line 269: --- 페이지 332 ---
Line 270: A Stress Test for AuctionSearch
Line 271: One invariant of our AuctionSearch is that it notiﬁes the consumer just once
Line 272: when the search has ﬁnished, no matter how many AuctionHouses it searches—that
Line 273: is, no matter how many threads its starts.
Line 274: We can use jMock to write a stress test for this invariant. We don’t always use
Line 275: jMock for stress tests because expectation failures interfere with the threads of
Line 276: the object under test. On the other hand, jMock reports the actual sequence
Line 277: of calls to its mock objects when there is a failure, which helps diagnose defects.
Line 278: It also provides convenient facilities for synchronizing between the test thread
Line 279: and the threads being tested.
Line 280: In AuctionSearchStressTests, we set up AuctionSearch with a thread-pool
Line 281: executor that will run tasks in background threads, and a list of auction houses
Line 282: stubbed to match on the given keywords. jMock is not thread-safe by default,
Line 283: so we set up the Mockery with a Synchroniser, an implementation of its threading
Line 284: policy that allows us to call mocked objects from different threads. To make
Line 285: tuning the test easier, we deﬁne constants at the top for the “degree of stress”
Line 286: we’ll apply during the run.
Line 287: @RunWith(JMock.class)
Line 288: public class AuctionSearchStressTests {
Line 289:   private static final int NUMBER_OF_AUCTION_HOUSES = 4; 
Line 290:   private static final int NUMBER_OF_SEARCHES = 8;
Line 291:   private static final Set<String> KEYWORDS = setOf("sheep", "cheese");
Line 292:   final Synchroniser synchroniser = new Synchroniser();
Line 293:   final Mockery context = new JUnit4Mockery() {{
Line 294:     setThreadingPolicy(synchroniser);
Line 295:   }};
Line 296:   final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
Line 297:   final States searching = context.states("searching");
Line 298:   final ExecutorService executor = Executors.newCachedThreadPool();
Line 299:   final AuctionSearch search = new AuctionSearch(executor, auctionHouses(), consumer); 
Line 300: […]
Line 301:   private List<AuctionHouse> auctionHouses() {
Line 302:     ArrayList<AuctionHouse> auctionHouses = new ArrayList<AuctionHouse>();
Line 303:     for (int i = 0; i < NUMBER_OF_AUCTION_HOUSES; i++) {
Line 304:       auctionHouses.add(stubbedAuctionHouse(i));
Line 305:     }
Line 306:     return auctionHouses;
Line 307:   }
Line 308:   private AuctionHouse stubbedAuctionHouse(final int id) {
Line 309:     StubAuctionHouse house = new StubAuctionHouse("house" + id);
Line 310:     house.willReturnSearchResults(
Line 311:         KEYWORDS, asList(new AuctionDescription(house, "id" + id, "description")));
Line 312:     return house;
Line 313:   } 
Line 314: 307
Line 315: Unit-Testing Synchronization
Line 316: 
Line 317: --- 페이지 333 ---
Line 318:   @Test(timeout=500) public void 
Line 319: onlyOneAuctionSearchFinishedNotificationPerSearch() throws Exception {
Line 320:     context.checking(new Expectations() {{ 
Line 321:       ignoring (consumer).auctionSearchFound(with(anyResults()));
Line 322:     }});
Line 323:     for (int i = 0; i < NUMBER_OF_SEARCHES; i++) { 
Line 324:       completeASearch();
Line 325:     }
Line 326:   }
Line 327:   private void completeASearch() throws InterruptedException {
Line 328:     searching.startsAs("in progress");
Line 329:     context.checking(new Expectations() {{
Line 330:       exactly(1).of(consumer).auctionSearchFinished(); then(searching.is("done"));
Line 331:     }});
Line 332:     search.search(KEYWORDS);
Line 333: synchroniser.waitUntil(searching.is("done")); 
Line 334:   }
Line 335:   @After
Line 336:   public void cleanUp() throws InterruptedException {
Line 337: executor.shutdown();
Line 338: executor.awaitTermination(1, SECONDS);
Line 339:   }
Line 340: }
Line 341: In the test method onlyOneAuctionSearchFinishedNotificationPerSearch(),
Line 342: we run a complete search NUMBER_OF_SEARCHES times, to increase the likelihood
Line 343: of ﬁnding any race conditions. It ﬁnishes each search by asking synchroniser
Line 344: to wait until it’s collected all the background threads the executor has
Line 345: launched, or until it’s timed out. Synchroniser provides a method that will
Line 346: safely wait until a state machine is (or is not) in a given state. The test ignores
Line 347: auctionSearchFound() notiﬁcations, since here we’re only interested in making
Line 348: sure that the searches ﬁnish cleanly. Finally, we shut down executor in the test
Line 349: teardown.
Line 350: It’s important to watch a stress test fail. It’s too easy to write a test that passes
Line 351: even though the tested object has a synchronization hole. So, we “test the test”
Line 352: by making it fail before we’ve synchronized the code, and checking that we get
Line 353: the failure report we expected. If we don’t, then we might need to raise the
Line 354: numbers of threads or iterations per thread until we can trust the test to reveal
Line 355: the error.2 Then we add the synchronization to make the test pass. Here’s our
Line 356: test failure:
Line 357: 2. Of course, the stress parameters may differ between environments, such as develop-
Line 358: ment vs. build. We can’t follow that through here, except to note that it needs
Line 359: addressing.
Line 360: Chapter 26
Line 361: Unit Testing and Threads
Line 362: 308
Line 363: 
Line 364: --- 페이지 334 ---
Line 365: java.lang.AssertionError: unexpected invocation: consumer.auctionSearchFinished()
Line 366: expectations:
Line 367:   allowed, already invoked 5 times: consumer.auctionSearchFound(ANYTHING)
Line 368:   expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
Line 369:                                                            then searching is done
Line 370:   expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
Line 371:                                                            then searching is done
Line 372: states:
Line 373:   searching is done
Line 374: what happened before this:
Line 375:   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
Line 376:   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line 377:   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line 378:   consumer.auctionSearchFinished()
Line 379:   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
Line 380:   consumer.auctionSearchFinished()
Line 381:   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line 382: This says that AuctionSearch has called auctionFinished() once too often.
Line 383: Fixing the Race Condition (Twice)
Line 384: We haven’t synchronized access to runningSearchCount. If we use an
Line 385: AtomicInteger from the Java concurrency libraries instead of a plain int, the
Line 386: threads should be able to decrement it without interfering with each other.
Line 387: public class AuctionSearch { […]
Line 388: private final AtomicInteger runningSearchCount = new AtomicInteger();
Line 389:   public void search(Set<String> keywords) {
Line 390:     for (AuctionHouse auctionHouse : auctionHouses) {
Line 391:       startSearching(auctionHouse, keywords);
Line 392:     }
Line 393:   }
Line 394:   private void startSearching(final AuctionHouse auctionHouse, 
Line 395:                               final Set<String> keywords) 
Line 396:   {
Line 397: runningSearchCount.incrementAndGet();
Line 398:     executor.execute(new Runnable() {
Line 399:       public void run() { search(auctionHouse, keywords); }
Line 400:     });
Line 401:   }
Line 402:   private void search(AuctionHouse auctionHouse, Set<String> keywords) {
Line 403:     consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
Line 404:     if (runningSearchCount.decrementAndGet() == 0) {
Line 405:       consumer.auctionSearchFinished();
Line 406:     }
Line 407:   }
Line 408: }
Line 409: 309
Line 410: Unit-Testing Synchronization
Line 411: 
Line 412: --- 페이지 335 ---
Line 413: We try this and, in spite of our use of an AtomicInteger, our test still fails! We
Line 414: haven’t got our synchronization right after all.
Line 415: We look again at the failure and see that now the AuctionSearch is
Line 416: reporting that the search has ﬁnished more than once per search. Previously,
Line 417: the unsafe concurrent access to runningSearchCount resulted in fewer
Line 418: auctionSearchFinshed() notiﬁcations than expected, because AuctionSearch
Line 419: was losing updates to the ﬁeld. Something else must be wrong.
Line 420: As an eagle-eyed reader, you’ll have noticed a race condition in the way
Line 421: AuctionSearch increments and decrements runningSearchCount. It increments
Line 422: the count before starting a task thread. Once the main thread has started creating
Line 423: task threads, the thread scheduler can preëmpt it and start running whatever task
Line 424: threads are ready—while the main thread still has search tasks left to create. If
Line 425: all these started task threads complete before the scheduler resumes the main
Line 426: thread, they will decrement the count to 0 and the last one will send an
Line 427: auctionSearchFinshed() notiﬁcation. When the main thread ﬁnally resumes, it
Line 428: will continue by starting its remaining searches, which will eventually trigger
Line 429: another notiﬁcation.
Line 430: This sort of error shows why we need to write stress tests, to make sure that
Line 431: we see them fail, and to understand the failure messages—it’s also a good moti-
Line 432: vation for us to write comprehensible failure reports. This example also highlights
Line 433: the beneﬁts of splitting tests of “raw” functionality from threaded tests. With the
Line 434: single-threaded version stable, we know we can concentrate on looking for race
Line 435: conditions in the stress tests.
Line 436: We ﬁx the code by setting runningSearchCount to the expected number of
Line 437: searches before starting any threads:
Line 438: public class AuctionSearch { […]
Line 439:   public void search(Set<String> keywords) {
Line 440: runningSearchCount.set(auctionHouses.size());
Line 441:     for (AuctionHouse auctionHouse : auctionHouses) {
Line 442:       startSearching(auctionHouse, keywords);
Line 443:     }
Line 444:   }
Line 445:   private void startSearching(final AuctionHouse auctionHouse, 
Line 446:                               final Set<String> keywords) 
Line 447:   {
Line 448: // no longer increments the count here
Line 449:     executor.execute(new Runnable() {
Line 450:       public void run() { search(auctionHouse, keywords); }
Line 451:     });
Line 452:   }
Line 453: }
Line 454: Chapter 26
Line 455: Unit Testing and Threads
Line 456: 310
Line 457: 
Line 458: --- 페이지 336 ---
Line 459: Stress-Testing Passive Objects
Line 460: AuctionSearch actively starts multiple threads by calling out to its executor.
Line 461: Most objects that are concerned with threading, however, don’t start threads
Line 462: themselves but have multiple threads “pass through” them and alter their state.
Line 463: Servlets, for example, are required to support multiple threads touching the same
Line 464: instance. In such cases, an object must synchronize access to any state that might
Line 465: cause a race condition.
Line 466: To stress-test the synchronization of a passive object, the test must start its
Line 467: own threads to call the object. When all the threads have ﬁnished, the state of
Line 468: the object should be the same as if those calls had happened in sequence. For
Line 469: example, AtomicBigCounter below does not synchronize access to its count vari-
Line 470: able. It works when called from a single thread but can lose updates when called
Line 471: from multiple threads:
Line 472: public class AtomicBigCounter {
Line 473:   private BigInteger count = BigInteger.ZERO;
Line 474:   public BigInteger count() { return count; }
Line 475:   public void inc() { count = count.add(BigInteger.ONE); }
Line 476: }
Line 477: We can show this failure by calling inc() from multiple threads enough times
Line 478: to give us a good chance of causing the race condition and losing an update.
Line 479: When this happens, the ﬁnal result of count() will be less than the number of
Line 480: times we’ve called inc().
Line 481: We could spin up multiple threads directly in our test, but the mess of detail
Line 482: for launching and synchronizing threads would get in the way of understanding
Line 483: the intent. The threading concerns are a good candidate for extracting into a
Line 484: subordinate object, MultiThreadedStressTester, which we use to call the counter’s
Line 485: inc() method:
Line 486: public class AtomicBigCounterTests { […]
Line 487:   final AtomicBigCounter counter = new AtomicBigCounter();
Line 488:   @Test public void
Line 489: canIncrementCounterFromMultipleThreadsSimultaneously() throws InterruptedException {
Line 490:     MultithreadedStressTester stressTester = new MultithreadedStressTester(25000);
Line 491:     stressTester.stress(new Runnable() {
Line 492:       public void run() {
Line 493:         counter.inc();
Line 494:       }
Line 495:     });
Line 496:     stressTester.shutdown();
Line 497:     assertThat("final count", counter.count(), 
Line 498:                equalTo(BigInteger.valueOf(stressTester.totalActionCount())));
Line 499:   }
Line 500: }
Line 501: 311
Line 502: Stress-Testing Passive Objects
Line 503: 
Line 504: --- 페이지 337 ---
Line 505: The test fails, showing the race condition in AtomicBigCounter:
Line 506: java.lang.AssertionError: final count
Line 507: Expected: <50000>
Line 508:      got: <36933>
Line 509: We pass the test by making the inc() and count() methods synchronized.
Line 510: Synchronizing the Test Thread with Background Threads
Line 511: When writing a test for code that starts threads, the test cannot conﬁrm the code’s
Line 512: behavior until it has synchronized its thread with any threads the code has
Line 513: started. For example, in AuctionSearchStressTests we make the test thread wait
Line 514: until all the task threads launched by AuctionSearch have been completed. Syn-
Line 515: chronizing with background threads can be challenging, especially if the tested
Line 516: object does not delegate to an executor to run concurrent tasks.
Line 517: The easiest way to ensure that threads have ﬁnished is for the test to sleep long
Line 518: enough for them all to run to completion. For example:
Line 519: private void waitForSearchToFinish() throws InterruptedException {
Line 520:   Thread.sleep(250);
Line 521: }
Line 522: This works for occasional use—a sub-second delay in a few tests won’t be
Line 523: noticeable—but it doesn’t scale. As the number of tests with delays grows, the
Line 524: total delay adds up and the test suite slows down so much that running it becomes
Line 525: a distraction. We must be able to run all the unit tests so quickly as to not even
Line 526: think about whether we should. The other problem with ﬁxed sleeps is that our
Line 527: choice of delay has to apply across all the environments where the tests run. A
Line 528: delay suitable for an underpowered machine will slow the tests everywhere else,
Line 529: and introducing a new environment may force another round of tuning.
Line 530: An alternative, as we saw in AuctionSearchStressTests, is to use jMock’s
Line 531: Synchroniser. It provides support for synchronizing between test and background
Line 532: threads, based on whether a state machine has entered or left a given state:
Line 533: synchroniser.waitUntil(searching.is("finished"));
Line 534: synchroniser.waitUntil(searching.isNot("in progress"));
Line 535: These methods will block forever for a failing test, where the state machine never
Line 536: meets the speciﬁed criteria, so they should be used with a timeout added to the
Line 537: test declaration:
Line 538: @Test(timeout=500)
Line 539: This tells the test runnner to force a failure if the test overruns the timeout period.
Line 540: Chapter 26
Line 541: Unit Testing and Threads
Line 542: 312
Line 543: 
Line 544: --- 페이지 338 ---
Line 545: A test will run as fast as possible if successful (Synchroniser’s implementation
Line 546: is based on Java monitors), and only wait the entire 500 ms for failures. So, most
Line 547: of the time, the synchronization will not slow down the test suite.
Line 548: If not using jMock, you can write a utility similar to Synchroniser to synchro-
Line 549: nize between test and background threads. Alternatively, we describe other
Line 550: synchronization techniques in Chapter 27.
Line 551: The Limitations of Unit Stress Tests
Line 552: Having a separate set of tests for our object’s synchronization behavior helps us
Line 553: pinpoint where to look for defects if tests fail. It is very difﬁcult to diagnose race
Line 554: conditions with a debugger, as stepping through code (or even adding print
Line 555: statements) will alter the thread scheduling that’s causing the clash.3 If a change
Line 556: causes a stress test to fail but the functional unit tests still pass, at least we know
Line 557: that the object’s functional logic is correct and we’ve introduced a defect into its
Line 558: synchronization, or vice versa.
Line 559: Obviously, stress tests offer only a degree of reassurance that code is thread-safe,
Line 560: not a guarantee. There may be scheduling differences between different operating
Line 561: systems (or versions of an operating system) and between different processor
Line 562: combinations. Further, there may be other processes on a host that affect
Line 563: scheduling while the tests are running. The best we can do is to run the tests
Line 564: frequently in a range of environments—locally before committing new code, and
Line 565: on multiple build servers after commit. This should already be part of the devel-
Line 566: opment process. We can tune the amount of work and number of threads in the
Line 567: tests until they are reliable enough at detecting errors—where the meaning of
Line 568: “enough” is an engineering decision for the team.
Line 569: To cover our backs, we take a “belt and braces” approach.4 We run unit tests
Line 570: to check that our objects correctly synchronize concurrent threads and to pin-
Line 571: point synchronization failures. We run end-to-end tests to check that unit-level
Line 572: synchronization policies integrate across the entire system. If the concurrency
Line 573: architecture is not imposed on us by the frameworks we are using, we sometimes
Line 574: use formal modeling tools, such as the LTSA tool described in [Magee06], to
Line 575: prove that our concurrency model avoids certain classes of errors. Finally, we
Line 576: run static analysis tools as part of our automated build process to catch further
Line 577: errors. There are now some excellent practical examples, such as Findbugs,5 that
Line 578: can detect synchronization errors in everyday Java code.
Line 579: 3. These are known as “Heisenbugs,” because trying to detect the bug alters it.
Line 580: 4. For American readers, this means “belt and suspenders,” but suspenders are a
Line 581: signiﬁcantly different garment in British English.
Line 582: 5. http://findbugs.sf.net
Line 583: 313
Line 584: The Limitations of Unit Stress Tests
Line 585: 
Line 586: --- 페이지 339 ---
Line 587: In this chapter, we’ve considered unit-level testing of concurrent code. Larger-
Line 588: scale testing of concurrent behavior is much more complex—the tested code
Line 589: might be running in multiple, distributed processes; the test setup might not be
Line 590: able to control the creation of threads with an executor; some of the synchroniza-
Line 591: tion events might not be easily detectable; and, the system might detect and
Line 592: swallow errors before they can be reported to a test. We address this level of
Line 593: testing in the next chapter.
Line 594: Chapter 26
Line 595: Unit Testing and Threads
Line 596: 314