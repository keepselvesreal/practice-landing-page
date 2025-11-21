# 14.4 The Sniper Acquires Some State (pp.144-146)

---
**Page 144**

Running the end-to-end tests again shows that we’ve ﬁxed the failure that
started this chapter (showing Bidding rather than Winning). Now we have to
make the Sniper win:
java.lang.AssertionError: 
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Won"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Lost"
The Sniper Acquires Some State
We’re about to introduce a step change in the complexity of the Sniper, if only
a small one. When the auction closes, we want the Sniper to announce whether
it has won or lost, which means that it must know whether it was bidding or
winning at the time. This implies that the Sniper will have to maintain some state,
which it hasn’t had to so far.
To get to the functionality we want, we’ll start with the simpler cases where
the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
transitions, before adding the additional step that takes the Sniper to the Won state:
Figure 14.2
A Sniper bids, then loses
Chapter 14
The Sniper Wins the Auction
144


---
**Page 145**

We start by revisiting an existing unit test and adding a new one. These tests
will pass with the current implementation; they’re there to ensure that we don’t
break the behavior when we add further transitions.
This introduces some new jMock syntax, states. The idea is to allow us to
make assertions about the internal state of the object under test. We’ll come back
to this idea in a moment.
public class AuctionSniperTest { […]
  private final States sniperState = context.states("sniper"); 1
  @Test public void
  reportsLostIfAuctionClosesImmediately() { 2
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperLost();
    }});
    sniper.auctionClosed();
  }
  @Test public void
reportsLostIfAuctionClosesWhenBidding() {
    context.checking(new Expectations() {{
      ignoring(auction); 3
      allowing(sniperListener).sniperBidding(); 
                              then(sniperState.is("bidding")); 4
atLeast(1).of(sniperListener).sniperLost(); 
                              when(sniperState.is("bidding")); 5
    }});
    sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 6
    sniper.auctionClosed();
  }
}
1
We want to keep track of the Sniper’s current state, as signaled by the events
it sends out, so we ask context for a placeholder. The default state is null.
2
We keep our original test, but now it will apply where there are no price
updates.
3
The Sniper will call auction but we really don’t care about that in this test,
so we tell the test to ignore this collaborator completely.
4
When the Sniper sends out a bidding event, it’s telling us that it’s in a bidding
state, which we record here. We use the allowing() clause to communicate
that this is a supporting part of the test, not the part we really care about;
see the note below.
5
This is the phrase that matters, the expectation that we want to assert. If the
Sniper isn’t bidding when it makes this call, the test will fail.
145
The Sniper Acquires Some State


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


