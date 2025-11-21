# 27.2 Sampling or Listening (pp.316-318)

---
**Page 316**

when the test makes its assertion. The value of the stock holding that the assertion
checks will depend on timings: how long the messages take to reach the server,
how long the server takes to update its database, and how long the test takes to
run. The test might ﬁre the assertion after both messages have been processed
(passing correctly), after one message (failing incorrectly), or before either
message (passing, but testing nothing at all).
As you can see from this small example, with an asynchronous test we have
to be careful about its coordination with the system it’s testing. Otherwise, it can
become unreliable, failing intermittently when the system is working or, worse,
passing when the system is broken.
Current testing frameworks provide little support for dealing with asynchrony.
They mostly assume that the tests run in a single thread of control, leaving the
programmer to build the scaffolding needed to test concurrent behavior. In this
chapter we describe some practices for writing reliable, responsive tests for
asynchronous code.
Sampling or Listening
The fundamental difﬁculty with testing asynchronous code is that a test triggers
activity that runs concurrently with the test and therefore cannot immediately
check the outcome of the activity. The test will not block until the activity has
ﬁnished. If the activity fails, it will not throw an exception back into the test, so
the test cannot recognize if the activity is still running or has failed. The test
therefore has to wait for the activity to complete successfully and fail if this
doesn’t happen within a given timeout period.
Wait for Success
An asynchronous test must wait for success and use timeouts to detect failure.
This implies that every tested activity must have an observable effect: a test
must affect the system so that its observable state becomes different. This sounds
obvious but it drives how we think about writing asynchronous tests. If an activ-
ity has no observable effect, there is nothing the test can wait for, and therefore
no way for the test to synchronize with the system it is testing.
There are two ways a test can observe the system: by sampling its observable
state or by listening for events that it sends out. Of these, sampling is often the
only option because many systems don’t send any monitoring events. It’s quite
common for a test to include both techniques to interact with different “ends”
of its system. For example, the Auction Sniper end-to-end tests sample the user
interface for display changes, through the WindowLicker framework, but listen
for chat events in the fake auction server.
Chapter 27
Testing Asynchronous Code
316


---
**Page 317**

Beware of Flickering Tests
A test can fail intermittently if its timeout is too close to the time the tested behavior
normally takes to run, or if it doesn’t synchronize correctly with the system. On a
small system, an occasional ﬂickering test might not cause problems—the test will
most likely pass during the next build—but it’s risky. As the test suite grows, it be-
comes increasingly difﬁcult to get a test run in which none of the ﬂickering tests fail.
Flickering tests can mask real defects. If the system itself occasionally fails, the
tests that accurately detect those failures will seem to be ﬂickering. If the suite
contains unreliable tests, intermittent failures detected by reliable tests can easily
be ignored. We need to make sure we understand what the real problem is before
we ignore ﬂickering tests.
Allowing ﬂickering tests is bad for the team. It breaks the culture of quality where
things should “just work,” and even a few ﬂickering tests can make a team stop
paying attention to broken builds. It also breaks the habit of feedback. We should
be paying attention to why the tests are ﬂickering and whether that means we
should improve the design of both the tests and code. Of course, there might be
times when we have to compromise and decide to live with a ﬂickering test for the
moment, but this should be done reluctantly and include a plan for when it will
be ﬁxed.
As we saw in the last chapter, synchronizing by simply making each test wait
for a ﬁxed time is not practical. The test suite for a system of any size will take
too long to run. We know we’ll have to wait for failing tests to time out, but
succeeding tests should be able to ﬁnish as soon as there’s a response from
the code.
Succeed Fast
Make asynchronous tests detect success as quickly as possible so that they provide
rapid feedback.
Of the two observation strategies we outlined in the previous section, listening
for events is the quickest. The test thread can block, waiting for an event from
the system. It will wake up and check the result as soon as it receives an event.
The alternative—sampling—means repeatedly polling the target system for a
state change, with a short delay between polls. The frequency of this polling has
to be tuned to the system under test, to balance the need for a fast response
against the load it imposes on the target system. In the worst case, fast polling
might slow the system enough to make the tests unreliable.
317
Sampling or Listening


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


