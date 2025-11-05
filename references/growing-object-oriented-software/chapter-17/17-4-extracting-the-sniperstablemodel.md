# 17.4 Extracting the SnipersTableModel (pp.197-201)

---
**Page 197**

Implementing XMPPAuctionHouse is straightforward; we transfer there all the
code related to connection, including the generation of the Jabber ID from
the auction item ID. Main is now simpler, with just one import for all the XMPP
code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Figure 17.2.
For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
the test to XMPPAuctionHouseTest.
Our ﬁnal touch is to move the relevant constants from Main where we’d left
them: the message formats to XMPPAuction and the connection identiﬁer format
to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
since we’re narrowing the scope of where these constants are used.
Extracting the SnipersTableModel
Sniper Launcher
Finally, we’d like to do something about the direct reference to the
SnipersTableModel and the related SwingThreadSniperListener—and the awful
notToBeGCd. We think we can get there, but it’ll take a couple of steps.
The ﬁrst step is to turn the anonymous implementation of UserRequestListener
into a proper class so we can understand its dependencies. We decide to call the
new class SniperLauncher, since it will respond to a request to join an auction
by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
to the new class.
public class SniperLauncher implements UserRequestListener {
  private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
  private final AuctionHouse auctionHouse;
  private final SnipersTableModel snipers;
  public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
// set the fields 
  }
  public void joinAuction(String itemId) {
snipers.addSniper(SniperSnapshot.joining(itemId));
      Auction auction = auctionHouse.auctionFor(itemId);
      notToBeGCd.add(auction);
      AuctionSniper sniper = 
        new AuctionSniper(itemId, auction, 
                          new SwingThreadSniperListener(snipers));
      auction.addAuctionEventListener(snipers);
      auction.join();
  }
}
With the SniperLauncher separated out, it becomes even clearer that the
Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
197
Extracting the SnipersTableModel


---
**Page 198**

SnipersTableModel, is clumsy: we tell it about the new Sniper by giving it an
initial SniperSnapshot, and we attach it to both the Sniper and the auction.
There’s also some hidden duplication in that we create an initial SniperSnaphot
both here and in the AuctionSniper constructor.
Stepping back, we ought to simplify this class so that all it does is establish a
new AuctionSniper. It can delegate the process of accepting the new Sniper into
the application to a new role which we’ll call a SniperCollector, implemented
in the SnipersTableModel.
public static class SniperLauncher implements UserRequestListener {
  private final AuctionHouse auctionHouse;
  private final SniperCollector collector;
[…]
  public void joinAuction(String itemId) {
      Auction auction = auctionHouse.auctionFor(itemId);
AuctionSniper sniper = new AuctionSniper(itemId, auction);
      auction.addAuctionEventListener(sniper);
collector.addSniper(sniper);
      auction.join();
  }
}
The one behavior that we want to conﬁrm is that we only join the auction after
everything else is set up. With the code now isolated, we can jMock a States to
check the ordering.
public class SniperLauncherTest {
  private final States auctionState = context.states("auction state")
.startsAs("not joined");
[…]
  @Test public void
addsNewSniperToCollectorAndThenJoinsAuction() {
    final String itemId = "item 123";
    context.checking(new Expectations() {{
      allowing(auctionHouse).auctionFor(itemId); will(returnValue(auction));
      oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId))); 
when(auctionState.is("not joined"));
      oneOf(sniperCollector).addSniper(with(sniperForItem(item))); 
when(auctionState.is("not joined"));
      one(auction).join(); then(auctionState.is("joined"));
    }});
    launcher.joinAuction(itemId);
  }
}
where sniperForItem() returns a Matcher that matches any AuctionSniper
associated with the given item identiﬁer.
We extend SnipersTableModel to fulﬁll its new role: now it accepts
AuctionSnipers rather than SniperSnapshots. To make this work, we have to
convert a Sniper’s listener from a dependency to a notiﬁcation, so that we can
Chapter 17
Teasing Apart Main
198


---
**Page 199**

add a listener after construction. We also change SnipersTableModel to use the
new API and disallow adding SniperSnapshots.
public class SnipersTableModel extends AbstractTableModel 
    implements SniperListener, SniperCollector
{
  private final ArrayList<AuctionSniper> notToBeGCd = […]
  public void addSniper(AuctionSniper sniper) {
    notToBeGCd.add(sniper);
    addSniperSnapshot(sniper.getSnapshot());
    sniper.addSniperListener(new SwingThreadSniperListener(this));
  }
  private void addSniperSnapshot(SniperSnapshot sniperSnapshot) {
    snapshots.add(sniperSnapshot);
    int row = snapshots.size() - 1;
    fireTableRowsInserted(row, row);
   }
}
One change that suggests that we’re heading in the right direction is that the
SwingThreadSniperListener is now packaged up in the Swing part of the code,
not in the generic SniperLauncher.
Sniper Portfolio
As a next step, we realize that we don’t yet have anything that represents all our
sniping activity and that we might call our portfolio. At the moment, the
SnipersTableModel is implicitly responsible for both maintaining a record of
our sniping and displaying that record. It also pulls a Swing implementation detail
into Main.
We want a clearer separation of concerns, so we extract a SniperPortfolio
to maintain our Snipers, which we make our new implementer of
SniperCollector. We push the creation of the SnipersTableModel into MainWindow,
and make it a PortfolioListener so the portfolio can tell it when we add or
remove a Sniper.
public interface PortfolioListener extends EventListener {
  void sniperAdded(AuctionSniper sniper);
}
public class MainWindow extends JFrame {
  private JTable makeSnipersTable(SniperPortfolio portfolio) { 
SnipersTableModel model = new SnipersTableModel();
    portfolio.addPortfolioListener(model);
    JTable snipersTable = new JTable(model); 
    snipersTable.setName(SNIPERS_TABLE_NAME); 
    return snipersTable; 
  }
}
199
Extracting the SnipersTableModel


---
**Page 200**

This makes our top-level code very simple—it just binds together the user
interface and sniper creation through the portfolio:
public class Main {  […]
  private final SniperPortfolio portfolio = new SniperPortfolio();
  public Main() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() {
      public void run() {
        ui = new MainWindow(portfolio);
      }
    });
  }
  private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
    ui.addUserRequestListener(new SniperLauncher(auctionHouse, portfolio));
  }
}
Even better, since SniperPortfolio maintains a list of all the Snipers, we can
ﬁnally get rid of notToBeGCd.
This refactoring takes us to the structure shown in Figure 17.3. We’ve separated
the code into three components: one for the core application, one for XMPP
communication, and one for Swing display. We’ll return to this in a moment.
Figure 17.3
With the SniperPortfolio
Chapter 17
Teasing Apart Main
200


---
**Page 201**

Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Figure 17.4
Adding items through the user interface
Observations
Incremental Architecture
This restructuring of Main is a key moment in the development of the application.
As Figure 17.5 shows, we now have a structure that matches the “ports and
adapters” architecture we described in “Designing for Maintainability” (page 47).
There is core domain code (for example, AuctionSniper) which depends on
bridging code (for example, SnipersTableModel) that drives or responds to
technical code (for example, JTable). We’ve kept the domain code free of any
reference to the external infrastructure. The contents of our auctionsniper
package deﬁne a model of our auction sniping business, using a self-contained
language. The exception is Main, which is our entry point and binds the domain
model and infrastructure together.
What’s important for the purposes of this example, is that we arrived at this
design incrementally, by adding features and repeatedly following heuristics.
Although we rely on our experience to guide our decisions, we reached this
solution almost automatically by just following the code and taking care to keep
it clean.
201
Observations


