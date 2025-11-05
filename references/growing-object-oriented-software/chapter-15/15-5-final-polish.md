# 15.5 Final Polish (pp.168-171)

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


---
**Page 169**

Figure 15.4
TableModel as a SniperListener
public class ApplicationRunner { […]
  public void startBiddingIn(final FakeAuctionServer auction) {
    itemId = auction.getItemId();
    Thread thread = new Thread("Test Application") {
[…]
    };
    thread.setDaemon(true);
    thread.start();
    driver = new AuctionSniperDriver(1000);
driver.hasTitle(MainWindow.APPLICATION_TITLE);
driver.hasColumnTitles();
    driver.showsSniperStatus(JOINING.itemId, JOINING.lastPrice, 
                             JOINING.lastBid, textFor(SniperState.JOINING));
  }
}
public class AuctionSniperDriver extends JFrameDriver { […]
  public void hasColumnTitles() {
    JTableHeaderDriver headers = new JTableHeaderDriver(this, JTableHeader.class);
    headers.hasHeaders(matching(withLabelText("Item"), withLabelText("Last Price"),
                                withLabelText("Last Bid"), withLabelText("State")));
  }
}
The test fails:
169
Final Polish


---
**Page 170**

java.lang.AssertionError: 
Tried to look for...
    exactly 1 JTableHeader ()
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that it is with headers with cells 
  <label  with text "Item">, <label with text "Last Price">, 
    <label with text "Last Bid">, <label with text "State">
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTableHeader ()
   it is not with headers with cells 
     <label with text "Item">, <label with text "Last Price">, 
       <label with text "Last Bid">, <label with text "State">
because component 0 text was "A"
Implementing the TableModel
Swing allows a JTable to query its TableModel for the column headers, which is
the mechanism we’ve chosen to use. We already have Column to represent the
columns, so we extend this enum by adding a ﬁeld for the header text which we
reference in SnipersTableModel.
public enum Column {
  ITEM_IDENTIFIER("Item") { […]
  LAST_PRICE("Last Price") { […]
  LAST_BID("Last Bid") { […]
  SNIPER_STATE("State") { […]
public final String name;
  private Column(String name) {
this.name = name;
  }
}
public class SnipersTableModel extends AbstractTableModel implements SniperListener
{ […]
  @Override public String getColumnName(int column) {
    return Column.at(column).name;
  }
}
All we really need to check in the unit test for SniperTablesModel is the link
between a Column value and a column name, but it’s so simple to iterate that we
check them all:
public class SnipersTableModelTest { […]
  @Test public void
setsUpColumnHeadings() {
    for (Column column: Column.values()) {
      assertEquals(column.name, model.getColumnName(column.ordinal()));
    }
  }
}
Chapter 15
Towards a Real User Interface
170


---
**Page 171**

The acceptance test passes, and we can see the result in Figure 15.5.
Figure 15.5
Sniper with column headers
Enough for Now
There’s more we should do, such as set up borders and text alignment, to tune
the user interface. We might do that by associating CellRenderers with each
Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
as an exercise for the reader, since they don’t add any more insight into our
development process.
In the meantime, we can cross off one more task from our to-do list:
Figure 15.6.
Figure 15.6
The Sniper shows price information
Observations
Single Responsibilities
SnipersTableModel has one responsibility: to represent the state of our bidding
in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
171
Observations


