# 15.3 Simplifying Sniper Events (pp.159-164)

---
**Page 159**

[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
 it is not with row with cells 
   <label with text "item-54321">, <label with text "1098">, 
   <label with text "1098">, <label with text "Winning">
because 
      in row 0: component 1 text was "1000"
and the proof is in Figure 15.3.
Figure 15.3
Sniper showing a row of detail
Simplifying Sniper Events
Listening to the Mood Music
We have one kind of Sniper event, Bidding, that we can handle all the way
through our application. Now we have to do the same thing to Winning, Lost,
and Won.
Frankly, that’s just dull. There’s too much repetitive work needed to make the
other cases work—setting them up in the Sniper and passing them through
the layers. Something’s wrong with the design. We toss this one around for a
while and eventually notice that we would have a subtle duplication in our code
if we just carried on. We would be splitting the transmission of the Sniper state
into two mechanisms: the choice of listener method and the state object. That’s
one mechanism too many.
We realize that we could collapse our events into one notiﬁcation that includes
the prices and the Sniper status. Of course we’re transmitting the same information
whichever mechanism we choose—but, looking at the chain of methods calls,
it would be simpler to have just one method and pass everything through in
SniperState.
Having made this choice, can we do it cleanly without ripping up the
metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
We want to start by creating a type to represent the Sniper’s status (winning,
losing, etc.) in the auction, but the terms “status” and “state” are too close to
distinguish easily. We kick around some vocabulary and eventually decide that
a better term for what we now call SniperState would be SniperSnapshot: a
description of the Sniper’s relationship with the auction at this moment in time.
This frees up the name SniperState to describe whether the Sniper is winning,
losing, and so on, which matches the terminology of the state machine we drew
159
Simplifying Sniper Events


---
**Page 160**

in Figure 9.3 on page 78. Renaming the SniperState takes a moment, and we
change the value in Column from SNIPER_STATUS to SNIPER_STATE.
20/20 Hindsight
We’ve just gone through not one but two of those forehead-slapping moments that
make us wonder why we didn’t see it the ﬁrst time around. Surely, if we’d spent
more time on the design, we wouldn’t have to change it now? Sometimes that’s
true. Our experience, however, is that nothing shakes out a design like trying to
implement it, and between us we know just a handful of people who are smart
enough to get their designs always right. Our coping mechanism is to get into the
critical areas of the code early and to allow ourselves to change our collective mind
when we could do better. We rely on our skills, on taking small steps, and on the
tests to protect us when we make changes.
Repurposing sniperBidding()
Our ﬁrst step is to take the method that does most of what we want,
sniperBidding(), and rework it to ﬁt our new scheme. We create an enum that
takes the SniperState name we’ve just freed up and add it to SniperSnapshot;
we take the sniperState ﬁeld out of the method arguments; and, ﬁnally, we re-
name the method to sniperStateChanged() to match its intended new role. We
push the changes through to get the following code:
public enum SniperState {
  JOINING,
  BIDDING,
  WINNING,
  LOST,
  WON;
}
public class AuctionSniper implements AuctionEventListener { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
      sniperListener.sniperWinning();
    } else {
      final int bid = price + increment;
      auction.bid(bid);
      sniperListener.sniperStateChanged(
        new SniperSnapshot(itemId, price, bid, SniperState.BIDDING));
    }
  }
}
Chapter 15
Towards a Real User Interface
160


---
**Page 161**

In the table model, we use simple indexing to translate the enum into displayable
text.
public class SnipersTableModel extends AbstractTableModel { […]
private static String[] STATUS_TEXT = { MainWindow.STATUS_JOINING, 
                                          MainWindow.STATUS_BIDDING };
  public void sniperStateChanged(SniperSnapshot newSnapshot) {
    this.snapshot = newSnapshot;
    this.state = STATUS_TEXT[newSnapshot.state.ordinal()];
    fireTableRowsUpdated(0, 0);
  }
}
We make some minor changes to the test code, to get it through the compiler,
plus one more interesting adjustment. You might remember that we wrote an
expectation clause that ignored the details of the SniperState:
allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
We can no longer rely on the choice of method to distinguish between different
events, so we have to dig into the new SniperSnapshot object to make sure we’re
matching the right one. We rewrite the expectation with a custom matcher that
checks just the state:
public class AuctionSniperTest {
[…]
  context.checking(new Expectations() {{
    ignoring(auction);
    allowing(sniperListener).sniperStateChanged(
                               with(aSniperThatIs(BIDDING))); 
                                                then(sniperState.is("bidding"));
    atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
  }});
[…]
  private Matcher<SniperSnapshot> aSniperThatIs(final SniperState state) {
    return new FeatureMatcher<SniperSnapshot, SniperState>(
             equalTo(state), "sniper that is ", "was") 
    {
      @Override
      protected SniperState featureValueOf(SniperSnapshot actual) {
        return actual.state;
      }
    };
  }
}
161
Simplifying Sniper Events


---
**Page 162**

Lightweight Extensions to jMock
We added a small helper method aSniperThatIs() to package up our specializa-
tion of FeatureMatcher behind a descriptive name. You’ll see that the method
name is intended to make the expectation code read well (or as well as we can
manage in Java).We did the same earlier in the chapter with aRowChangedEvent().
As we discussed in “Different Levels of Language” on page 51, we’re effectively
writing extensions to a language that’s embedded in Java. jMock was designed to
be extensible in this way, so that programmers can plug in features described in
terms of the code they’re testing.You could think of these little helper methods as
creating new nouns in jMock’s expectation language.
Filling In the Numbers
Now we’re in a position to feed the missing price to the user interface, which
means changing the listener call from sniperWinning() to sniperStateChanged()
so that the listener will receive the value in a SniperSnapshot. We start by
changing the test to expect the different listener call, and to trigger the event by
calling currentPrice() twice: once to force the Sniper to bid, and again to tell
the Sniper that it’s winning.
public class AuctionSniperTest { […]
  @Test public void
reportsIsWinningWhenCurrentPriceComesFromSniper() {
    context.checking(new Expectations() {{
      ignoring(auction);
      allowing(sniperListener).sniperStateChanged(
                                 with(aSniperThatIs(BIDDING))); 
                                               then(sniperState.is("bidding"));
atLeast(1).of(sniperListener).sniperStateChanged(
                               new SniperSnapshot(ITEM_ID, 135, 135, WINNING)); 
                                               when(sniperState.is("bidding"));
    }});
sniper.currentPrice(123, 12, PriceSource.FromOtherBidder);
    sniper.currentPrice(135, 45, PriceSource.FromSniper);
  }
}
We change AuctionSniper to retain its most recent values by holding on to the
last snapshot. We also add some helper methods to SniperSnapshot, and ﬁnd
that our implementation starts to simplify.
Chapter 15
Towards a Real User Interface
162


---
**Page 163**

public class AuctionSniper implements AuctionEventListener { […]
private SniperSnapshot snapshot;
  public AuctionSniper(String itemId, Auction auction, SniperListener sniperListener)
  {
    this.auction = auction;
    this.sniperListener = sniperListener;
this.snapshot = SniperSnapshot.joining(itemId);
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
snapshot = snapshot.winning(price);
    } else {
      final int bid = price + increment;
      auction.bid(bid);
snapshot = snapshot.bidding(price, bid);
    }
sniperListener.sniperStateChanged(snapshot);
  }
}
public class SniperSnapshot { […]
  public SniperSnapshot bidding(int newLastPrice, int newLastBid) {
    return new SniperSnapshot(itemId, newLastPrice, newLastBid, SniperState.BIDDING);
  }
  public SniperSnapshot winning(int newLastPrice) {
    return new SniperSnapshot(itemId, newLastPrice, lastBid, SniperState.WINNING);
  }
  public static SniperSnapshot joining(String itemId) {
    return new SniperSnapshot(itemId, 0, 0, SniperState.JOINING);
  }
}
Nearly a State Machine
We’ve added some constructor methods to SniperSnapshot that provide a clean
mechanism for moving between snapshot states. It’s not a full state machine, in
that we don’t enforce only “legal” transitions, but it’s a hint, and it nicely packages
up the getting and setting of ﬁelds.
We remove sniperWinning() from SniperListener and its implementations,
and add a value for winning to SnipersTableModel.STATUS_TEXT.
Now, the end-to-end test passes.
163
Simplifying Sniper Events


---
**Page 164**

Follow Through
Converting Won and Lost
This works, but we still have two notiﬁcation methods in SniperListener left to
convert before we can say we’re done: sniperWon() and sniperLost(). Again,
we replace these with sniperStateChanged() and add two new values to
SniperState.
Plugging these changes in, we ﬁnd that the code simpliﬁes further. We drop
the isWinning ﬁeld from the Sniper and move some decision-making into
SniperSnapshot, which will know whether the Sniper is winning or losing,
and SniperState.
public class AuctionSniper implements AuctionEventListener { […]
  public void auctionClosed() {
snapshot = snapshot.closed();
    notifyChange();
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
switch(priceSource) {
    case FromSniper:
      snapshot = snapshot.winning(price); 
      break;
case FromOtherBidder:
      int bid = price + increment;
      auction.bid(bid);
      snapshot = snapshot.bidding(price, bid); 
      break;
    }
notifyChange();
  }
  private void notifyChange() {
    sniperListener.sniperStateChanged(snapshot);
  }
}
We note, with smug satisfaction, that AuctionSniper no longer refers to
SniperState; it’s hidden in SniperSnapshot.
public class SniperSnapshot { […]
  public SniperSnapshot closed() {
    return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
  }
}
Chapter 15
Towards a Real User Interface
164


