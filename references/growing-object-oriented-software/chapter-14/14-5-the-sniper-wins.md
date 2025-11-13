# 14.5 The Sniper Wins (pp.146-148)

---
**Page 146**

6
This is our ﬁrst test where we need a sequence of events to get the Sniper
into the state we want to test. We just call its methods in order.
Allowances
jMock distinguishes between allowed and expected invocations. An allowing()
clause says that the object might make this call, but it doesn’t have to—unlike an
expectation which will fail the test if the call isn’t made. We make the distinction to
help express what is important in a test (the underlying implementation is actually
the same): expectations are what we want to conﬁrm to have happened; allowances
are supporting infrastructure that helps get the tested objects into the right state,
or they’re side effects we don’t care about. We return to this topic in “Allowances
and Expectations” (page 277) and we describe the API in Appendix A.
Representing Object State
In cases like this, we want to make assertions about an object’s behavior depending
on its state, but we don’t want to break encapsulation by exposing how that state
is implemented. Instead, the test can listen to the notiﬁcation events that the Sniper
provides to tell interested collaborators about its state in their terms. jMock provides
States objects, so that tests can record and make assertions about the state of
an object when something signiﬁcant happens, i.e. when it calls its neighbors; see
Appendix A for the syntax.
This is a “logical” representation of what’s going on inside the object, in this case
the Sniper. It allows the test to describe what it ﬁnds relevant about the Sniper, re-
gardless of how the Sniper is actually implemented. As you’ll see shortly, this sep-
aration will allow us to make radical changes to the implementation of the Sniper
without changing the tests.
The unit test name reportsLostIfAuctionClosesWhenBidding is very similar
to the expectation it enforces:
atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
That’s not an accident. We put a lot of effort into ﬁguring out which abstractions
jMock should support and developing a style that expresses the essential intent
of a unit test.
The Sniper Wins
Finally, we can close the loop and have the Sniper win a bid. The next test
introduces the Won event.
Chapter 14
The Sniper Wins the Auction
146


---
**Page 147**

@Test public void
reportsWonIfAuctionClosesWhenWinning() {
  context.checking(new Expectations() {{
    ignoring(auction);
    allowing(sniperListener).sniperWinning();  then(sniperState.is("winning"));
    atLeast(1).of(sniperListener).sniperWon(); when(sniperState.is("winning"));
  }});
  sniper.currentPrice(123, 45, true);
  sniper.auctionClosed();
}
It has the same structure but represents when the Sniper has won. The test fails
because the Sniper called sniperLost().
unexpected invocation: sniperListener.sniperLost()
expectations:
  allowed, never invoked: 
    auction.<any method>(<any parameters>) was[]; 
  allowed, already invoked 1 time: sniperListener.sniperWinning(); 
                                     then sniper is winning
  expected at least 1 time, never invoked: sniperListener.sniperWon();
                                             when sniper is winning
states:
  sniper is winning
what happened before this:
  sniperListener.sniperWinning()
We add a ﬂag to represent the Sniper’s state, and implement the new
sniperWon() method in the SniperStateDisplayer.
public class AuctionSniper implements AuctionEventListener { […]
private boolean isWinning = false;
  public void auctionClosed() {
if (isWinning) {
      sniperListener.sniperWon();
    } else {
      sniperListener.sniperLost();
    }
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
      sniperListener.sniperWinning();
    } else {
      auction.bid(price + increment);
      sniperListener.sniperBidding();
    }
  }
}
public class SniperStateDisplayer implements SniperListener { […]
  public void sniperWon() {
    showStatus(MainWindow.STATUS_WON);
  }
}
147
The Sniper Wins


---
**Page 148**

Having previously made a fuss about PriceSource, are we being inconsistent
here by using a boolean for isWinning? Our excuse is that we did try an enum
for the Sniper state, but it just looked too complicated. The ﬁeld is private to
AuctionSniper, which is small enough so it’s easy to change later and the code
reads well.
The unit and end-to-end tests all pass now, so we can cross off another item
from the to-do list in Figure 14.3.
Figure 14.3
The Sniper wins
There are more tests we could write—for example, to describe the transitions
from bidding to winning and back again, but we’ll leave those as an exercise for
you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
functionality.
Making Steady Progress
As always, we made steady progress by adding little slices of functionality. First
we made the Sniper show when it’s winning, then when it has won. We used
empty implementations to get us through the compiler when we weren’t ready
to ﬁll in the code, and we stayed focused on the immediate task.
One of the pleasant surprises is that, now the code is growing a little, we’re
starting to see some of our earlier effort pay off as new features just ﬁt into the
existing structure. The next tasks we have to implement will shake this up.
Chapter 14
The Sniper Wins the Auction
148


