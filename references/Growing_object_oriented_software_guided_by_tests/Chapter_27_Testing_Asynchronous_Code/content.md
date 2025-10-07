Line 1: 
Line 2: --- 페이지 340 ---
Line 3: Chapter 27
Line 4: Testing Asynchronous Code
Line 5: I can spell banana but I never know when to stop.
Line 6: —Johnny Mercer (songwriter)
Line 7: Introduction
Line 8: Some tests must cope with asynchronous behavior—whether they’re end-to-end
Line 9: tests probing a system from the outside or, as we’ve just seen, unit tests exercising
Line 10: multithreaded code. These tests trigger some activity within the system to run
Line 11: concurrently with the test’s thread. The critical difference from “normal” tests,
Line 12: where there is no concurrency, is that control returns to the test before the tested
Line 13: activity is complete—returning from the call to the target code does not mean
Line 14: that it’s ready to be checked.
Line 15: For example, this test assumes that a Set has ﬁnished adding an element when
Line 16: the add() method returns. Asserting that set has a size of one veriﬁes that it did
Line 17: not store duplicate elements.
Line 18: @Test public void storesUniqueElements() {
Line 19:   Set set = new HashSet<String>();
Line 20:   set.add("bananana");
Line 21:   set.add("bananana");
Line 22:   assertThat(set.size(), equalTo(1));
Line 23: }
Line 24: By contrast, this system test is asynchronous. The holdingOfStock() method
Line 25: synchronously downloads a stock report by HTTP, but the send() method sends
Line 26: an asynchronous message to a server that updates its records of stocks held.
Line 27: @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line 28:   Date tradeDate = new Date();
Line 29:   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line 30:   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line 31:   assertThat(holdingOfStock("A", tradeDate), equalTo(0));
Line 32: }
Line 33: The transmission and processing of a trade message happens concurrently with
Line 34: the test, so the server might not have received or processed the messages yet
Line 35: 315
Line 36: 
Line 37: --- 페이지 341 ---
Line 38: when the test makes its assertion. The value of the stock holding that the assertion
Line 39: checks will depend on timings: how long the messages take to reach the server,
Line 40: how long the server takes to update its database, and how long the test takes to
Line 41: run. The test might ﬁre the assertion after both messages have been processed
Line 42: (passing correctly), after one message (failing incorrectly), or before either
Line 43: message (passing, but testing nothing at all).
Line 44: As you can see from this small example, with an asynchronous test we have
Line 45: to be careful about its coordination with the system it’s testing. Otherwise, it can
Line 46: become unreliable, failing intermittently when the system is working or, worse,
Line 47: passing when the system is broken.
Line 48: Current testing frameworks provide little support for dealing with asynchrony.
Line 49: They mostly assume that the tests run in a single thread of control, leaving the
Line 50: programmer to build the scaffolding needed to test concurrent behavior. In this
Line 51: chapter we describe some practices for writing reliable, responsive tests for
Line 52: asynchronous code.
Line 53: Sampling or Listening
Line 54: The fundamental difﬁculty with testing asynchronous code is that a test triggers
Line 55: activity that runs concurrently with the test and therefore cannot immediately
Line 56: check the outcome of the activity. The test will not block until the activity has
Line 57: ﬁnished. If the activity fails, it will not throw an exception back into the test, so
Line 58: the test cannot recognize if the activity is still running or has failed. The test
Line 59: therefore has to wait for the activity to complete successfully and fail if this
Line 60: doesn’t happen within a given timeout period.
Line 61: Wait for Success
Line 62: An asynchronous test must wait for success and use timeouts to detect failure.
Line 63: This implies that every tested activity must have an observable effect: a test
Line 64: must affect the system so that its observable state becomes different. This sounds
Line 65: obvious but it drives how we think about writing asynchronous tests. If an activ-
Line 66: ity has no observable effect, there is nothing the test can wait for, and therefore
Line 67: no way for the test to synchronize with the system it is testing.
Line 68: There are two ways a test can observe the system: by sampling its observable
Line 69: state or by listening for events that it sends out. Of these, sampling is often the
Line 70: only option because many systems don’t send any monitoring events. It’s quite
Line 71: common for a test to include both techniques to interact with different “ends”
Line 72: of its system. For example, the Auction Sniper end-to-end tests sample the user
Line 73: interface for display changes, through the WindowLicker framework, but listen
Line 74: for chat events in the fake auction server.
Line 75: Chapter 27
Line 76: Testing Asynchronous Code
Line 77: 316
Line 78: 
Line 79: --- 페이지 342 ---
Line 80: Beware of Flickering Tests
Line 81: A test can fail intermittently if its timeout is too close to the time the tested behavior
Line 82: normally takes to run, or if it doesn’t synchronize correctly with the system. On a
Line 83: small system, an occasional ﬂickering test might not cause problems—the test will
Line 84: most likely pass during the next build—but it’s risky. As the test suite grows, it be-
Line 85: comes increasingly difﬁcult to get a test run in which none of the ﬂickering tests fail.
Line 86: Flickering tests can mask real defects. If the system itself occasionally fails, the
Line 87: tests that accurately detect those failures will seem to be ﬂickering. If the suite
Line 88: contains unreliable tests, intermittent failures detected by reliable tests can easily
Line 89: be ignored. We need to make sure we understand what the real problem is before
Line 90: we ignore ﬂickering tests.
Line 91: Allowing ﬂickering tests is bad for the team. It breaks the culture of quality where
Line 92: things should “just work,” and even a few ﬂickering tests can make a team stop
Line 93: paying attention to broken builds. It also breaks the habit of feedback. We should
Line 94: be paying attention to why the tests are ﬂickering and whether that means we
Line 95: should improve the design of both the tests and code. Of course, there might be
Line 96: times when we have to compromise and decide to live with a ﬂickering test for the
Line 97: moment, but this should be done reluctantly and include a plan for when it will
Line 98: be ﬁxed.
Line 99: As we saw in the last chapter, synchronizing by simply making each test wait
Line 100: for a ﬁxed time is not practical. The test suite for a system of any size will take
Line 101: too long to run. We know we’ll have to wait for failing tests to time out, but
Line 102: succeeding tests should be able to ﬁnish as soon as there’s a response from
Line 103: the code.
Line 104: Succeed Fast
Line 105: Make asynchronous tests detect success as quickly as possible so that they provide
Line 106: rapid feedback.
Line 107: Of the two observation strategies we outlined in the previous section, listening
Line 108: for events is the quickest. The test thread can block, waiting for an event from
Line 109: the system. It will wake up and check the result as soon as it receives an event.
Line 110: The alternative—sampling—means repeatedly polling the target system for a
Line 111: state change, with a short delay between polls. The frequency of this polling has
Line 112: to be tuned to the system under test, to balance the need for a fast response
Line 113: against the load it imposes on the target system. In the worst case, fast polling
Line 114: might slow the system enough to make the tests unreliable.
Line 115: 317
Line 116: Sampling or Listening
Line 117: 
Line 118: --- 페이지 343 ---
Line 119: Put the Timeout Values in One Place
Line 120: Both observation strategies use a timeout to detect that the system has failed.
Line 121: Again, there’s a balance to be struck between a timeout that’s too short, which will
Line 122: make the tests unreliable, and one that’s too long, which will make failing tests too
Line 123: slow. This balance can be different in different environments, and will change as
Line 124: the system grows over time.
Line 125: When the timeout duration is deﬁned in one place, it’s easy to ﬁnd and change.
Line 126: The team can adjust its value to ﬁnd the right balance between speed and reliability
Line 127: as the system develops.
Line 128: Two Implementations
Line 129: Scattering ad hoc sleeps and timeouts throughout the tests makes them difﬁcult
Line 130: to understand, because it leaves too much implementation detail in the tests
Line 131: themselves. Synchronization and assertion is just the sort of behavior that’s
Line 132: suitable for factoring out into subordinate objects because it usually turns into
Line 133: a bad case of duplication if we don’t. It’s also just the sort of tricky code that we
Line 134: want to get right once and not have to change again.
Line 135: In this section, we’ll show an example implementation of each observation
Line 136: strategy.
Line 137: Capturing Notiﬁcations
Line 138: An event-based assertion waits for an event by blocking on a monitor until it
Line 139: gets notiﬁed or times out. When the monitor is notiﬁed, the test thread wakes
Line 140: up and continues if it ﬁnds that the expected event has arrived, or blocks again.
Line 141: If the test times out, then it raises a failure.
Line 142: NotificationTrace is an example of how to record and test notiﬁcations sent
Line 143: by the system. The setup of the test will arrange for the tested code to call
Line 144: append() when the event happens, for example by plugging in an event listener
Line 145: that will call the method when triggered. In the body of the test, the test thread
Line 146: calls containsNotification() to wait for the expected notiﬁcation or fail if it
Line 147: times out. For example:
Line 148: trace.containsNotification(startsWith("WANTED"));
Line 149: will wait for a notiﬁcation string that starts with WANTED.
Line 150: Within NotificationTrace, incoming notiﬁcations are stored in a list trace,
Line 151: which is protected by a lock traceLock. The class is generic, so we don’t specify
Line 152: the type of these notiﬁcations, except to say that the matchers we pass into
Line 153: containsNotification() must be compatible with that type. The implementation
Line 154: uses Timeout and NotificationStream classes that we’ll describe later.
Line 155: Chapter 27
Line 156: Testing Asynchronous Code
Line 157: 318
Line 158: 
Line 159: --- 페이지 344 ---
Line 160: public class NotificationTrace<T> {
Line 161:   private final Object traceLock = new Object();
Line 162:   private final List<T> trace = new ArrayList<T>(); 1
Line 163:   private long timeoutMs;
Line 164: // constructors and accessors to configure the timeout […]
Line 165:   public void append(T message) { 2
Line 166:     synchronized (traceLock) {
Line 167:       trace.add(message);
Line 168: traceLock.notifyAll();
Line 169:     }
Line 170:   }
Line 171:   public void containsNotification(Matcher<? super T> criteria) 3
Line 172:     throws InterruptedException 
Line 173:   { 
Line 174:     Timeout timeout = new Timeout(timeoutMs); 
Line 175:     synchronized (traceLock) {
Line 176:       NotificationStream<T> stream = new NotificationStream<T>(trace, criteria);
Line 177:       while (! stream.hasMatched()) {
Line 178:         if (timeout.hasTimedOut()) {
Line 179:           throw new AssertionError(failureDescriptionFrom(criteria));
Line 180:         }
Line 181:         timeout.waitOn(traceLock);
Line 182:       }
Line 183:     }
Line 184:   }
Line 185:   private String failureDescriptionFrom(Matcher<? super T> matcher) {  […] 
Line 186:     // Construct a description of why there was no match, 
Line 187:     // including the matcher and all the received messages. 
Line 188: }
Line 189: 1
Line 190: We store notiﬁcations in a list so that they’re available to us for other queries
Line 191: and so that we can include them in a description if the test fails (we don’t
Line 192: show how the description is constructed).
Line 193: 2
Line 194: The append() method, called from a worker thread, appends a new notiﬁca-
Line 195: tion to the trace, and then tells any threads waiting on traceLock to wake
Line 196: up because there’s been a change. This is called by the test infrastructure
Line 197: when triggered by an event in the system.
Line 198: 3
Line 199: The containsNotification() method, called from the test thread, searches
Line 200: through all the notiﬁcations it has received so far. If it ﬁnds a notiﬁcation
Line 201: that matches the given criteria, it returns. Otherwise, it waits until more
Line 202: notiﬁcations arrive and checks again. If it times out while waiting, then it
Line 203: fails the test.
Line 204: The nested NotificationStream class searches the unexamined elements in its
Line 205: list for one that matches the given criteria. It allows the list to grow between calls
Line 206: to hasMatched() and picks up after the last element it looked at.
Line 207: 319
Line 208: Two Implementations
Line 209: 
Line 210: --- 페이지 345 ---
Line 211: private static class NotificationStream<N> {
Line 212:   private final List<N> notifications;
Line 213:   private final Matcher<? super N> criteria;
Line 214:   private int next = 0;
Line 215:   public NotificationStream(List<N> notifications, Matcher<? super N> criteria) {
Line 216:     this.notifications = notifications;
Line 217:     this.criteria = criteria;
Line 218:   }
Line 219:   public boolean hasMatched() {
Line 220:     while (next < notifications.size()) {
Line 221:       if (criteria.matches(notifications.get(next)))
Line 222:         return true;
Line 223:       next++;
Line 224:     }
Line 225:     return false;
Line 226:   }
Line 227: }
Line 228: NotificationTrace is one example of a simple coordination class between test
Line 229: and worker threads. It uses a simple approach, although it does avoid a possible
Line 230: race condition where a background thread delivers a notiﬁcation before the test
Line 231: thread has started waiting. Another implementation, for example, might have
Line 232: containsNotification() only search messages received after the previous call.
Line 233: What is appropriate depends on the context of the test.
Line 234: Polling for Changes
Line 235: A sample-based assertion repeatedly samples some visible effect of the system
Line 236: through a “probe,” waiting for the probe to detect that the system has entered
Line 237: an expected state. There are two aspects to the process of sampling: polling the
Line 238: system and failure reporting, and probing the system for a given state. Separating
Line 239: the two helps us think clearly about the behavior, and different tests can reuse the
Line 240: polling with different probes.
Line 241: Poller is an example of how to poll a system. It repeatedly calls its probe, with
Line 242: a short delay between samples, until the system is ready or the poller times out.
Line 243: The poller drives a probe that actually checks the target system, which we’ve
Line 244: abstracted behind a Probe interface.
Line 245: public interface Probe {
Line 246:   boolean isSatisfied();
Line 247:   void sample();
Line 248:   void describeFailureTo(Description d);
Line 249: }
Line 250: The probe’s sample() method takes a snapshot of the system state that the test
Line 251: is interested in. The isSatisfied() method returns true if that state meets the
Line 252: test’s acceptance criteria. To simplify the poller logic, we allow isSatisfied()
Line 253: to be called before sample().
Line 254: Chapter 27
Line 255: Testing Asynchronous Code
Line 256: 320
Line 257: 
Line 258: --- 페이지 346 ---
Line 259: public class Poller {
Line 260:   private long timeoutMillis;
Line 261:   private long pollDelayMillis;
Line 262: // constructors and accessors to configure the timeout […]
Line 263:   public void check(Probe probe) throws InterruptedException {
Line 264:     Timeout timeout = new Timeout(timeoutMillis);
Line 265:     while (! probe.isSatisfied()) {
Line 266:       if (timeout.hasTimedOut()) {
Line 267:         throw new AssertionError(describeFailureOf(probe));
Line 268:       }
Line 269:       Thread.sleep(pollDelayMillis);
Line 270:       probe.sample();
Line 271:     }
Line 272:   }
Line 273:   private String describeFailureOf(Probe probe) { […] 
Line 274: }
Line 275: This simple implementation delegates synchronization with the system to
Line 276: the probe. A more sophisticated version might implement synchronization in the
Line 277: poller, so it could be shared between probes. The similarity to NotificationTrace
Line 278: is obvious, and we could have pulled out a common abstract structure, but we
Line 279: wanted to keep the designs clear for now.
Line 280: To poll, for example, for the length of a ﬁle, we would write this line in a test:
Line 281: assertEventually(fileLength("data.txt", is(greaterThan(2000))));
Line 282: This wraps up the construction of our sampling code in a more expressive
Line 283: assertion. The helper methods to implement this are:
Line 284: public static void assertEventually(Probe probe) throws InterruptedException {
Line 285:   new Poller(1000L, 100L).check(probe);
Line 286: }
Line 287: public static Probe fileLength(String path, final Matcher<Integer> matcher) {
Line 288:   final File file = new File(path);
Line 289:   return new Probe() {
Line 290:     private long lastFileLength = NOT_SET;
Line 291:     public void sample() { lastFileLength = file.length(); }
Line 292:     public boolean isSatisfied() { 
Line 293:       return lastFileLength != NOT_SET && matcher.matches(lastFileLength);
Line 294:     }
Line 295:     public void describeFailureTo(Description d) {
Line 296:       d.appendText("length was ").appendValue(lastFileLength);
Line 297:     }
Line 298:   };
Line 299: }
Line 300: Separating the act of sampling from checking whether the sample is satisfactory
Line 301: makes the structure of the probe clearer. We can hold on to the sample result to
Line 302: report the unsatisfactory result we found if there’s a failure.
Line 303: 321
Line 304: Two Implementations
Line 305: 
Line 306: --- 페이지 347 ---
Line 307: Timing Out
Line 308: Finally we show the Timeout class that the two example assertion classes use. It
Line 309: packages up time checking and synchronization:
Line 310: public class Timeout {
Line 311:  private final long endTime;
Line 312:   public Timeout(long duration) {
Line 313:     this.endTime = System.currentTimeMillis() + duration;
Line 314:   }
Line 315:   public boolean hasTimedOut() { return timeRemaining() <= 0; }
Line 316:   public void waitOn(Object lock) throws InterruptedException {
Line 317:     long waitTime = timeRemaining();
Line 318:     if (waitTime > 0) lock.wait(waitTime);
Line 319:   }
Line 320:   private long timeRemaining() { return endTime - System.currentTimeMillis(); }
Line 321: }
Line 322: Retroﬁtting a Probe
Line 323: We can now rewrite the test from the introduction. Instead of making an assertion
Line 324: about the current holding of a stock, the test must wait for the holding of the
Line 325: stock to reach the expected level within an acceptable time limit.
Line 326: @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line 327:   Date tradeDate = new Date();
Line 328:   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line 329:   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line 330: assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line 331: }
Line 332: Previously, the holdingOfStock() method returned a value to be compared.
Line 333: Now it returns a Probe that samples the system’s holding and returns if it meets
Line 334: the acceptance criteria deﬁned by a Hamcrest matcher—in this case equalTo(0).
Line 335: Runaway Tests
Line 336: Unfortunately, the new version of the test is still unreliable, even though we’re
Line 337: now sampling for a result. The assertion is waiting for the holding to become
Line 338: zero, which is what we started out with, so it’s possible for the test to pass before
Line 339: the system has even begun processing. This test can run ahead of the system
Line 340: without actually testing anything.
Line 341: Chapter 27
Line 342: Testing Asynchronous Code
Line 343: 322
Line 344: 
Line 345: --- 페이지 348 ---
Line 346: The worst aspect of runaway tests is that they give false positive results, so
Line 347: broken code looks like it’s working. We don’t often review tests that pass, so it’s
Line 348: easy to miss this kind of failure until something breaks down the line. Even more
Line 349: tricky, the code might have worked when we ﬁrst wrote it, as the tests happened
Line 350: to synchronize correctly during development, but now it’s broken and we
Line 351: can’t tell.
Line 352: Beware of Tests That Return the System to the Same State
Line 353: Be careful when an asynchronous test asserts that the system returns to a previous
Line 354: state. Unless it also asserts that the system enters an intermediate state before
Line 355: asserting the initial state, the test will run ahead of the system.
Line 356: To stop the test running ahead of the system, we must add assertions that wait
Line 357: for the system to enter an intermediate state. Here, for example, we make sure
Line 358: that the ﬁrst trade event has been processed before asserting the effect of the
Line 359: second event:
Line 360: @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line 361:   Date tradeDate = new Date();
Line 362:   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line 363: assertEventually(holdingOfStock("A", tradeDate, equalTo(10)));
Line 364:   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line 365:   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line 366: }
Line 367: Similarly, in Chapter 14, we check all the displayed states in the acceptance
Line 368: tests for the Auction Sniper user interface:
Line 369: auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line 370: application.hasShownSniperIsWinning();
Line 371: auction.announceClosed();
Line 372: application.hasShownSniperHasWon();
Line 373: We want to make sure that the sniper has responded to each message before
Line 374: continuing on to the next one.
Line 375: Lost Updates
Line 376: A signiﬁcant difference between tests that sample and those that listen for events
Line 377: is that polling can miss state changes that are later overwritten, Figure 27.1.
Line 378: 323
Line 379: Lost Updates
Line 380: 
Line 381: --- 페이지 349 ---
Line 382: Figure 27.1
Line 383: A test that polls can miss changes in the system
Line 384: under test
Line 385: If the test can record notiﬁcations from the system, it can look through its
Line 386: records to ﬁnd signiﬁcant notiﬁcations.
Line 387: Figure 27.2
Line 388: A test that records notiﬁcations will not lose updates
Line 389: To be reliable, a sampling test must make sure that its system is stable before
Line 390: triggering any further interactions. Sampling tests need to be structured as a series
Line 391: of phases, as shown in Figure 27.3. In each phase, the test sends a stimulus to
Line 392: prompt a change in the observable state of the system, and then waits until that
Line 393: change becomes visible or times out.
Line 394: Figure 27.3
Line 395: Phases of a sampling test
Line 396: Chapter 27
Line 397: Testing Asynchronous Code
Line 398: 324
Line 399: 
Line 400: --- 페이지 350 ---
Line 401: This shows the limits of how precise we can be with a sampling test. All the
Line 402: test can do between “stimulate” and “sample” is wait. We can write more
Line 403: reliable tests by not confusing the different steps in the loop and only triggering
Line 404: further changes once we’ve detected that the system is stable by observing a
Line 405: change in its sampled state.
Line 406: Testing That an Action Has No Effect
Line 407: Asynchronous tests look for changes in a system, so to test that something has
Line 408: not changed takes a little ingenuity. Synchronous tests don’t have this problem
Line 409: because they completely control the execution of the tested code. After invoking
Line 410: the target object, synchronous tests can query its state or check that it hasn’t
Line 411: made any unexpected calls to its neighbors.
Line 412: If an asynchronous test waits for something not to happen, it cannot even be
Line 413: sure that the system has started before it checks the result. For example, if we
Line 414: want to show that trades in another region are not counted in the stock holding,
Line 415: then this test:
Line 416: @Test public void doesNotShowTradesInOtherRegions() {
Line 417:   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line 418: .inTradingRegion(OTHER_REGION));
Line 419:   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line 420: }
Line 421: cannot tell whether the system has correctly ignored the trade or just not received
Line 422: it yet. The most obvious workaround is for the test to wait for a ﬁxed period of
Line 423: time and then check that the unwanted event did not occur. Unfortunately, this
Line 424: makes the test run slowly even when successful, and so breaks our rule of
Line 425: “succeed fast.”
Line 426: Instead, the test should trigger a behavior that is detectable and use that to
Line 427: detect that the system has stabilized. The skill here is in picking a behavior that
Line 428: will not interfere with the test’s assertions and that will complete after the tested
Line 429: behavior. For example, we could add another trade event to the regions example.
Line 430: This shows that the out-of-region event is excluded because its quantity is not
Line 431: included in the total holding.
Line 432: @Test public void doesNotShowTradesInOtherRegions() {
Line 433:   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line 434:                     .inTradingRegion(OTHER_REGION));
Line 435:   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(66)
Line 436:                     .inTradingRegion(SAME_REGION));
Line 437:   assertEventually(holdingOfStock("A", tradeDate, equalTo(66)));
Line 438: }
Line 439: Of course, this test assumes that trade events are processed in sequence, not
Line 440: in parallel, so that the second event cannot overtake the ﬁrst and give a false
Line 441: positive. That’s why such tests are not completely “black box” but have to make
Line 442: assumptions about the structure of the system. This might make these tests
Line 443: 325
Line 444: Testing That an Action Has No Effect
Line 445: 
Line 446: --- 페이지 351 ---
Line 447: brittle—they would misreport if the system changes the assumptions they’ve been
Line 448: built on. One response is to add a test to conﬁrm those expectations—in this
Line 449: case, perhaps a stress test to conﬁrm event processing order and alert the team
Line 450: if circumstances change. That said, there should already be other tests that conﬁrm
Line 451: those assumptions, so it may be enough just to associate these tests, for example
Line 452: by grouping them in the same test package.
Line 453: Distinguish Synchronizations and Assertions
Line 454: We have one mechanism for synchronizing a test with its system and for making
Line 455: assertions about that system—wait for an observable condition and time out if
Line 456: it doesn’t happen. The only difference between the two activities is our interpre-
Line 457: tation of what they mean. As always, we want to make our intentions explicit,
Line 458: but it’s especially important here because there’s a risk that someone may look
Line 459: at the test later and remove what looks like a duplicate assertion, accidentally
Line 460: introducing a race condition.
Line 461: We often adopt a naming scheme to distinguish between synchronizations and
Line 462: assertions. For example, we might have waitUntil() and assertEventually()
Line 463: methods to express the purpose of different checks that share an underlying
Line 464: implementation.
Line 465: Alternatively, we might reserve the term “assert” for synchronous tests and
Line 466: use a different naming conventions in asynchronous tests, as we did in the Auction
Line 467: Sniper example.
Line 468: Externalize Event Sources
Line 469: Some systems trigger their own events internally. The most common example is
Line 470: using a timer to schedule activities. This might include repeated actions that run
Line 471: frequently, such as bundling up emails for forwarding, or follow-up actions that
Line 472: run days or even weeks in the future, such as conﬁrming a delivery date.
Line 473: Hidden timers are very difﬁcult to work with because they make it hard to tell
Line 474: when the system is in a stable state for a test to make its assertions. Waiting for
Line 475: a repeated action to run is too slow to “succeed fast,” to say nothing of an action
Line 476: scheduled a month from now. We also don’t want tests to break unpredictably
Line 477: because of interference from a scheduled activity that’s just kicked in. Trying to
Line 478: test a system by coinciding timers is just too brittle.
Line 479: The only solution is to make the system deterministic by decoupling it from
Line 480: its own scheduling. We can pull event generation out into a shared service that
Line 481: is driven externally. For example, in one project we implemented the system’s
Line 482: scheduler as a web service. System components scheduled activities by making
Line 483: HTTP requests to the scheduler, which triggered activities by making HTTP
Line 484: “postbacks.” In another project, the scheduler published notiﬁcations onto a
Line 485: message bus topic that the components listened to.
Line 486: Chapter 27
Line 487: Testing Asynchronous Code
Line 488: 326
Line 489: 
Line 490: --- 페이지 352 ---
Line 491: With this separation in place, tests can step the system through its behavior
Line 492: by posing as the scheduler and generating events deterministically. Now we can
Line 493: run system tests quickly and reliably. This is a nice example of a testing require-
Line 494: ment leading to a better design. We’ve been forced to abstract out scheduling,
Line 495: which means we won’t have multiple implementations hidden in the system.
Line 496: Usually, introducing such an event infrastructure turns out to be useful for
Line 497: monitoring and administration.
Line 498: There’s a trade-off too, of course. Our tests are no longer exercising the entire
Line 499: system. We’ve prioritized test speed and reliability over ﬁdelity. We compensate
Line 500: by keeping the scheduler’s API as simple as possible and testing it rigorously
Line 501: (another advantage). We would probably also write a few slow tests, running in
Line 502: a separate build, that exercise the whole system together including the real
Line 503: scheduler.
Line 504: 327
Line 505: Externalize Event Sources
Line 506: 
Line 507: --- 페이지 353 ---
Line 508: This page intentionally left blank 