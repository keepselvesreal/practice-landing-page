# 26.6 The Limitations of Unit Stress Tests (pp.313-315)

---
**Page 313**

A test will run as fast as possible if successful (Synchroniser’s implementation
is based on Java monitors), and only wait the entire 500 ms for failures. So, most
of the time, the synchronization will not slow down the test suite.
If not using jMock, you can write a utility similar to Synchroniser to synchro-
nize between test and background threads. Alternatively, we describe other
synchronization techniques in Chapter 27.
The Limitations of Unit Stress Tests
Having a separate set of tests for our object’s synchronization behavior helps us
pinpoint where to look for defects if tests fail. It is very difﬁcult to diagnose race
conditions with a debugger, as stepping through code (or even adding print
statements) will alter the thread scheduling that’s causing the clash.3 If a change
causes a stress test to fail but the functional unit tests still pass, at least we know
that the object’s functional logic is correct and we’ve introduced a defect into its
synchronization, or vice versa.
Obviously, stress tests offer only a degree of reassurance that code is thread-safe,
not a guarantee. There may be scheduling differences between different operating
systems (or versions of an operating system) and between different processor
combinations. Further, there may be other processes on a host that affect
scheduling while the tests are running. The best we can do is to run the tests
frequently in a range of environments—locally before committing new code, and
on multiple build servers after commit. This should already be part of the devel-
opment process. We can tune the amount of work and number of threads in the
tests until they are reliable enough at detecting errors—where the meaning of
“enough” is an engineering decision for the team.
To cover our backs, we take a “belt and braces” approach.4 We run unit tests
to check that our objects correctly synchronize concurrent threads and to pin-
point synchronization failures. We run end-to-end tests to check that unit-level
synchronization policies integrate across the entire system. If the concurrency
architecture is not imposed on us by the frameworks we are using, we sometimes
use formal modeling tools, such as the LTSA tool described in [Magee06], to
prove that our concurrency model avoids certain classes of errors. Finally, we
run static analysis tools as part of our automated build process to catch further
errors. There are now some excellent practical examples, such as Findbugs,5 that
can detect synchronization errors in everyday Java code.
3. These are known as “Heisenbugs,” because trying to detect the bug alters it.
4. For American readers, this means “belt and suspenders,” but suspenders are a
signiﬁcantly different garment in British English.
5. http://findbugs.sf.net
313
The Limitations of Unit Stress Tests


---
**Page 314**

In this chapter, we’ve considered unit-level testing of concurrent code. Larger-
scale testing of concurrent behavior is much more complex—the tested code
might be running in multiple, distributed processes; the test setup might not be
able to control the creation of threads with an executor; some of the synchroniza-
tion events might not be easily detectable; and, the system might detect and
swallow errors before they can be reported to a test. We address this level of
testing in the next chapter.
Chapter 26
Unit Testing and Threads
314


---
**Page 315**

Chapter 27
Testing Asynchronous Code
I can spell banana but I never know when to stop.
—Johnny Mercer (songwriter)
Introduction
Some tests must cope with asynchronous behavior—whether they’re end-to-end
tests probing a system from the outside or, as we’ve just seen, unit tests exercising
multithreaded code. These tests trigger some activity within the system to run
concurrently with the test’s thread. The critical difference from “normal” tests,
where there is no concurrency, is that control returns to the test before the tested
activity is complete—returning from the call to the target code does not mean
that it’s ready to be checked.
For example, this test assumes that a Set has ﬁnished adding an element when
the add() method returns. Asserting that set has a size of one veriﬁes that it did
not store duplicate elements.
@Test public void storesUniqueElements() {
  Set set = new HashSet<String>();
  set.add("bananana");
  set.add("bananana");
  assertThat(set.size(), equalTo(1));
}
By contrast, this system test is asynchronous. The holdingOfStock() method
synchronously downloads a stock report by HTTP, but the send() method sends
an asynchronous message to a server that updates its records of stocks held.
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
  assertThat(holdingOfStock("A", tradeDate), equalTo(0));
}
The transmission and processing of a trade message happens concurrently with
the test, so the server might not have received or processed the messages yet
315


