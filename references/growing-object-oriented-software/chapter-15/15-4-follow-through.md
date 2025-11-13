# 15.4 Follow Through (pp.164-168)

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


---
**Page 165**

public enum SniperState {
  JOINING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  },
  BIDDING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  },
  WINNING {
    @Override public SniperState whenAuctionClosed() { return WON; }
  },
  LOST,
  WON;
  public SniperState whenAuctionClosed() {
    throw new Defect("Auction is already closed");
  }
}
We would have preferred to use a ﬁeld to implement whenAuctionClosed(). It
turns out that the compiler cannot handle an enum referring to one of its values
which has not yet been deﬁned, so we have to put up with the syntax noise of
overridden methods.
Not Too Small to Test
At ﬁrst SniperState looked too simple to unit-test—after all, it’s exercised through
the AuctionSniper tests—but we thought we should keep ourselves honest.
Writing the test showed that our simple implementation didn’t handle re-closing an
auction, which shouldn’t happen, so we added an exception. It would be better to
write the code so that this case is impossible, but we can’t see how to do that
right now.
A Defect Exception
In most systems we build, we end up writing a runtime exception called something
like Defect (or perhaps StupidProgrammerMistakeException). We throw this
when the code reaches a condition that could only be caused by a programming
error, rather than a failure in the runtime environment.
165
Follow Through


---
**Page 166**

Trimming the Table Model
We remove the accessor setStatusText() that sets the state display string in
SnipersTableModel, as everything uses sniperStatusChanged() now. While we’re
at it, we move the description string constants for the Sniper state over from
MainWindow.
public class SnipersTableModel extends AbstractTableModel { […]
private final static String[] STATUS_TEXT = { 
    "Joining", "Bidding", "Winning", "Lost", "Won" 
  };
  public Object getValueAt(int rowIndex, int columnIndex) {
    switch (Column.at(columnIndex)) {
    case ITEM_IDENTIFIER:
      return snapshot.itemId;
    case LAST_PRICE:
      return snapshot.lastPrice;
    case LAST_BID:
      return snapshot.lastBid;
    case SNIPER_STATE:
      return textFor(snapshot.state);
    default:
      throw new IllegalArgumentException("No column at" + columnIndex);
    }
  }
  public void sniperStateChanged(SniperSnapshot newSnapshot) {
this.snapshot = newSnapshot;
    fireTableRowsUpdated(0, 0);
  }
  public static String textFor(SniperState state) {
    return STATUS_TEXT[state.ordinal()];
  }
}
The helper method, textFor(), helps with readability, and we also use it to get
hold of the display strings in tests since the constants are no longer accessible
from MainWindow.
Object-Oriented Column
We still have a couple of things to do before we ﬁnish this task. We start by
removing all the old test code that didn’t specify the price details, ﬁlling in the
expected values in the tests as required. The tests still run.
The next change is to replace the switch statement which is noisy, not very
object-oriented, and includes an unnecessary default: clause just to satisfy the
compiler. It’s served its purpose, which was to get us through the previous coding
stage. We add a method to Column that will extract the appropriate ﬁeld:
Chapter 15
Towards a Real User Interface
166


---
**Page 167**

public enum Column {
  ITEM_IDENTIFIER {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.itemId;
    }
  },
  LAST_PRICE {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.lastPrice;
    }
  },
  LAST_BID{
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.lastBid;
    }    
  },
  SNIPER_STATE {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return SnipersTableModel.textFor(snapshot.state);
    }    
  };
abstract public Object valueIn(SniperSnapshot snapshot);
[…]
}
and the code in SnipersTableModel becomes negligible:
public class SnipersTableModel extends AbstractTableModel { […]
  public Object getValueAt(int rowIndex, int columnIndex) {
    return Column.at(columnIndex).valueIn(snapshot);
  }
}
Of course, we write a unit test for Column. It may seem unnecessary now, but
it will protect us when we make changes and forget to keep the column mapping
up to date.
Shortening the Event Path
Finally, we see that we have some forwarding calls that we no longer need.
MainWindow just forwards the update and SniperStateDisplayer has collapsed
to almost nothing.
public class MainWindow extends JFrame { […]
  public void sniperStateChanged(SniperSnapshot snapshot) {
    snipers.sniperStateChanged(snapshot);
  }
}
167
Follow Through


---
**Page 168**

public class SniperStateDisplayer implements SniperListener { […]
  public void sniperStateChanged(final SniperSnapshot snapshot) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() { mainWindow.sniperStateChanged(snapshot); } 
    });
  }
}
SniperStateDisplayer still serves a useful purpose, which is to push updates
onto the Swing event thread, but it no longer does any translation between do-
mains in the code, and the call to MainWindow is unnecessary. We decide to sim-
plify the connections by making SnipersTableModel implement SniperListener.
We change SniperStateDisplayer to be a Decorator and rename it to
SwingThreadSniperListener, and we rewire Main so that the Sniper connects
to the table model rather than the window.
 public class Main { […]
private final SnipersTableModel snipers = new SnipersTableModel();
  private MainWindow ui;
  public Main() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() { 
      public void run() { ui = new MainWindow(snipers); }
    });
  }
  private void joinAuction(XMPPConnection connection, String itemId) {
[…]
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(itemId, auction, 
new SwingThreadSniperListener(snipers))));
    auction.join();
  }
}
The new structure looks like Figure 15.4.
Final Polish
A Test for Column Titles
To make the user interface presentable, we need to ﬁll in the column titles which,
as we saw in Figure 15.3, are still missing. This isn’t difﬁcult, since most of the
implementation is built into Swing’s TableModel. As always, we start with
the acceptance test. We add extra validation to AuctionSniperDriver that will
be called by the method in ApplicationRunner that starts up the Sniper. For good
measure, we throw in a check for the application’s displayed title.
Chapter 15
Towards a Real User Interface
168


