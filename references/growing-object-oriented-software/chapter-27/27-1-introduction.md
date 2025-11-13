# 27.1 Introduction (pp.315-316)

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


