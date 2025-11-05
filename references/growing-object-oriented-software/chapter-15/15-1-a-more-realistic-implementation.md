# 15.1 A More Realistic Implementation (pp.149-152)

---
**Page 149**

Chapter 15
Towards a Real User Interface
In which we grow the user interface from a label to a table. We achieve
this by adding a feature at a time, instead of taking the risk of replacing
the whole thing in one go. We discover that some of the choices we
made are no longer valid, so we dare to change existing code. We
continue to refactor and sense that a more interesting structure is
starting to appear.
A More Realistic Implementation
What Do We Have to Do Next?
So far, we’ve been making do with a simple label in the user interface. That’s
been effective for helping us clarify the structure of the application and prove
that our ideas work, but the next tasks coming up will need more, and the client
wants to see something that looks closer to Figure 9.1. We will need to show
more price details from the auction and handle multiple items.
The simplest option would be just to add more text into the label, but we think
this is the right time to introduce more structure into the user interface. We de-
ferred putting effort into this part of the application, and we think we should
catch up now to be ready for the more complex requirements we’re about to
implement. We decide to make the obvious choice, given our use of Swing, and
replace the label with a table component. This decision gives us a clear direction
for where our design should go next.
The Swing pattern for using a JTable is to associate it with a TableModel. The
table component queries the model for values to present, and the model notiﬁes
the table when those values change. In our application, the relationships will
look like Figure 15.1.  We call the new class SnipersTableModel because we want
it to support multiple Snipers. It will accept updates from the Snipers and provide
a representation of those values to its JTable.
The question is how to get there from here.
149


---
**Page 150**

Figure 15.1
Swing table model for the AuctionSniper
Replacing JLabel
We want to get the pieces into place with a minimum of change, without tearing
the whole application apart. The smallest step we can think of is to replace the
existing implementation (a JLabel) with a single-cell JTable, from which we can
then grow the additional functionality. We start, of course, with the test, changing
our harness to look for a cell in a table, rather than a label.
public class AuctionSniperDriver extends JFrameDriver { […]
  public void showsSniperStatus(String statusText) {
new JTableDriver(this).hasCell(withLabelText(equalTo(statusText)));
  }
}
This generates a failure message because we don’t yet have a table.
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
contained 0 JTable ()
Chapter 15
Towards a Real User Interface
150


---
**Page 151**

We ﬁx this test by retroﬁtting a minimal JTable implementation. From now
on, we want to speed up our narrative, so we’ll just show the end result. If we
were feeling cautious we would ﬁrst add an empty table, to ﬁx the immediate
failure, and then add its contents. It turns out that we don’t have to change any
existing classes outside MainWindow because it encapsulates the act of updating
the status. Here’s the new code:
public class MainWindow extends JFrame { […]
private final SnipersTableModel snipers = new SnipersTableModel();
  public MainWindow() {
    super(APPLICATION_TITLE);
    setName(MainWindow.MAIN_WINDOW_NAME);
fillContentPane(makeSnipersTable());
    pack();
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true);
  }
  private void fillContentPane(JTable snipersTable) {
    final Container contentPane = getContentPane();
    contentPane.setLayout(new BorderLayout());
    contentPane.add(new JScrollPane(snipersTable), BorderLayout.CENTER);
  }
  private JTable makeSnipersTable() {
    final JTable snipersTable = new JTable(snipers);
    snipersTable.setName(SNIPERS_TABLE_NAME);
    return snipersTable;
  }
  public void showStatusText(String statusText) {
snipers.setStatusText(statusText);
  }
}
public class SnipersTableModel extends AbstractTableModel {
  private String statusText = STATUS_JOINING;
  public int getColumnCount() { return 1; }
  public int getRowCount() { return 1; }
  public Object getValueAt(int rowIndex, int columnIndex) { return statusText; }
  public void setStatusText(String newStatusText) {
    statusText = newStatusText;
    fireTableRowsUpdated(0, 0);
  }
}
151
A More Realistic Implementation


---
**Page 152**

Still Ugly
As you can see, the SnipersTableModel really is a minimal implementation; the
only value that can vary is the statusText. It inherits most of its behavior from
the Swing AbstractTableModel, including the infrastructure for notifying the
JTable of data changes. The result is as ugly as our previous version, except that
now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
on the presentation in a moment.
Figure 15.2
Sniper with a single-cell table
Displaying Price Details
First, a Failing Test
Our next task is to display information about the Sniper’s position in the auction:
item identiﬁer, last auction price, last bid, status. These values come from updates
from the auction and the state held within the application. We need to pass them
through from their source to the table model and then render them in the display.
Of course, we start with the test. Given that this feature should be part of the
basic functionality of the application, not separate from what we already have,
we update our existing acceptance tests—starting with just one test so we don’t
break everything at once. Here’s the new version:
public class AuctionSniperEndToEndTest {
  @Test public void
sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning(1098); // winning bid
    auction.announceClosed();
    application.showsSniperHasWonAuction(1098); // last price
  }
}
Chapter 15
Towards a Real User Interface
152


