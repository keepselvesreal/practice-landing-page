# 26.5 Synchronizing the Test Thread with Background Threads (pp.312-313)

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


