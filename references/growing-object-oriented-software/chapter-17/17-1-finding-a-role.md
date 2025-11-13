# 17.1 Finding a Role (pp.191-192)

---
**Page 191**

Chapter 17
Teasing Apart Main
In which we slice up our application, shufﬂing behavior around to
isolate the XMPP and user interface code from the sniping logic. We
achieve this incrementally, changing one concept at a time without
breaking the whole application. We ﬁnally put a stake through the
heart of notToBeGCd.
Finding a Role
We’ve convinced ourselves that we need to do some surgery on Main, but what
do we want our improved Main to do?
For programs that are more than trivial, we like to think of our top-level class
as a “matchmaker,” ﬁnding components and introducing them to each other.
Once that job is done it drops into the background and waits for the application to
ﬁnish. On a larger scale, this what the current generation of application containers
do, except that the relationships are often encoded in XML.
In its current form, Main acts as a matchmaker but it’s also implementing some
of the components, which means it has too many responsibilities. One clue is to
look at its imports:
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import javax.swing.SwingUtilities;
import org.jivesoftware.smack.Chat;
import org.jivesoftware.smack.XMPPConnection;
import org.jivesoftware.smack.XMPPException;
import auctionsniper.ui.MainWindow;
import auctionsniper.ui.SnipersTableModel;
import auctionsniper.AuctionMessageTranslator;
import auctionsniper.XMPPAuction;
We’re importing code from three unrelated packages, plus the auctionsniper
package itself. In fact, we have a package loop in that the top-level and
UI packages depend on each other. Java, unlike some other languages, tolerates
package loops, but they’re not something we should be pleased with.
191


---
**Page 192**

We think we should extract some of this behavior from Main, and the XMPP
features look like a good ﬁrst candidate. The use of the Smack should be an
implementation detail that is irrelevant to the rest of the application.
Extracting the Chat
Isolating the Chat
Most 
of 
the 
action 
happens 
in 
the 
implementation 
of
UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
leaved different domain levels, auction sniping and chatting, in this one unit of
code. We’d like to split them up. Here it is again:
public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
    public void joinAuction(String itemId) {
      snipers.addSniper(SniperSnapshot.joining(itemId));
        Chat chat = connection.getChatManager()
                                 .createChat(auctionId(itemId, connection), null);
        notToBeGCd.add(chat); 
        Auction auction = new XMPPAuction(chat);
chat.addMessageListener(
               new AuctionMessageTranslator(connection.getUser(),
                     new AuctionSniper(itemId, auction, 
                           new SwingThreadSniperListener(snipers))));
        auction.join();
      }
    });
  }
}
The object that locks this code into Smack is the chat; we refer to it several times:
to avoid garbage collection, to attach it to the Auction implementation, and to
attach the message listener. If we can gather together the auction- and Sniper-
related code, we can move the chat elsewhere, but that’s tricky while there’s still
a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
rather than a direct link, would give us the ﬂexibility we need. It would also make
sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
(page 52). The result is:
Chapter 17
Teasing Apart Main
192


