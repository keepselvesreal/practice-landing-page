# 13.3 Tidying Up the Implementation (pp.131-136)

---
**Page 131**

Figure 13.3
One step forward
Tidying Up the Implementation
Extracting XMPPAuction
Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
tation feels messy. We notice that the activity in joinAuction() crosses multiple
domains: managing chats, sending bids, creating snipers, and so on. We need to
clean up. To start, we notice that we’re sending auction commands from two
different levels, at the top and from within the Auction. Sending commands to
an auction sounds like the sort of thing that our Auction object should do, so it
makes sense to package that up together. We add a new method to the interface,
extend our anonymous implementation, and then extract it to a (temporarily)
nested class—for which we need a name. The distinguishing feature of this imple-
mentation of Auction is that it’s based on the messaging infrastructure, so we
call our new class XMPPAuction.
131
Tidying Up the Implementation


---
**Page 132**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), 
                                             null);
    this.notToBeGCd = chat;
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(new AuctionSniper(auction, this)));
auction.join();
  }
  public static class XMPPAuction implements Auction {
    private final Chat chat;
    public XMPPAuction(Chat chat) {
      this.chat = chat;
    }
    public void bid(int amount) {
      sendMessage(format(BID_COMMAND_FORMAT, amount));
    }
    public void join() {
      sendMessage(JOIN_COMMAND_FORMAT);
    }
    private void sendMessage(final String message) {
      try {
        chat.sendMessage(message);
      } catch (XMPPException e) {
        e.printStackTrace();
      }
    }
  }
}
We’re starting to see a clearer model of the domain. The line auction.join()
expresses our intent more clearly than the previous detailed implementation of
sending a string to a chat. The new design looks like Figure 13.4  and we promote
XMPPAuction to be a top-level class.
We still think joinAuction() is unclear, and we’d like to pull the XMPP-related
detail out of Main, but we’re not ready to do that yet. Another point to keep
in mind.
Chapter 13
The Sniper Makes a Bid
132


---
**Page 133**

Figure 13.4
Closing the loop with an XMPPAuction
Extracting the User Interface
The other activity in Main is implementing the user interface and showing the
current state in response to events from the Sniper. We’re not really happy that
Main implements SniperListener; again, it feels like mixing different responsibil-
ities (starting the application and responding to events). We decide to extract the
SniperListener behavior into a nested helper class, for which the best name we
can ﬁnd is SniperStateDisplayer. This new class is our bridge between two do-
mains: it translates Sniper events into a representation that Swing can display,
which includes dealing with Swing threading. We plug an instance of the new
class into the AuctionSniper.
public class Main { // doesn't implement SniperListener
  private MainWindow ui;
  private void joinAuction(XMPPConnection connection, String itemId) {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), null);
    this.notToBeGCd = chat;
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(auction, new SniperStateDisplayer())));
    auction.join();
  }
[…]
133
Tidying Up the Implementation


---
**Page 134**

  public class SniperStateDisplayer implements SniperListener {
    public void sniperBidding() {
      showStatus(MainWindow.STATUS_BIDDING);
    }
    public void sniperLost() {
      showStatus(MainWindow.STATUS_LOST);
    }
    public void sniperWinning() {
      showStatus(MainWindow.STATUS_WINNING);
    }
    private void showStatus(final String status) {
      SwingUtilities.invokeLater(new Runnable() {
        public void run() { ui.showStatus(status); } 
      });
    }
  }
}
Figure 13.5 shows how we’ve reduced Main so much that it no longer partici-
pates in the running application (for clarity, we’ve left out the WindowAdapter
that closes the connection). It has one job which is to create the various compo-
nents and introduce them to each other. We’ve marked MainWindow as external,
even though it’s one of ours, to represent the Swing framework.
Figure 13.5
Extracting SniperStateDisplayer
Chapter 13
The Sniper Makes a Bid
134


---
**Page 135**

Tidying Up the Translator
Finally, 
we 
fulﬁll 
our 
promise 
to 
ourselves 
and 
return 
to 
the
AuctionMessageTranslator. We start trying to reduce the noise by adding
constants and static imports, with some helper methods to reduce duplication.
Then we realize that much of the code is about manipulating the map of
name/value pairs and is rather procedural. We can do a better job by extracting
an inner class, AuctionEvent, to encapsulate the unpacking of the message con-
tents. We have conﬁdence that we can refactor the class safely because it’s
protected by its unit tests.
public class AuctionMessageTranslator implements MessageListener { 
  private final AuctionEventListener listener;
  public AuctionMessageTranslator(AuctionEventListener listener) {
    this.listener = listener;
  }
  public void processMessage(Chat chat, Message message) { 
AuctionEvent event = AuctionEvent.from(message.getBody());
    String eventType = event.type();
    if ("CLOSE".equals(eventType)) { 
      listener.auctionClosed(); 
    } if ("PRICE".equals(eventType)) { 
      listener.currentPrice(event.currentPrice(), event.increment()); 
    } 
  }
  private static class AuctionEvent {
    private final Map<String, String> fields = new HashMap<String, String>();  
    public String type() { return get("Event"); }
    public int currentPrice() { return getInt("CurrentPrice"); }
    public int increment() { return getInt("Increment"); }
    private int getInt(String fieldName) {
      return Integer.parseInt(get(fieldName));
    }
    private String get(String fieldName) { return fields.get(fieldName); }
    private void addField(String field) {
      String[] pair = field.split(":");
      fields.put(pair[0].trim(), pair[1].trim());
    }
    static AuctionEvent from(String messageBody) {
      AuctionEvent event = new AuctionEvent();
      for (String field : fieldsIn(messageBody)) {
        event.addField(field);
      }
      return event;
    }
    static String[] fieldsIn(String messageBody) {
      return messageBody.split(";");
    }
  }
}
135
Tidying Up the Implementation


---
**Page 136**

This is an example of “breaking out” that we described in “Value Types”
(page 59). It may not be obvious, but AuctionEvent is a value: it’s
immutable and there are no interesting differences between two instances
with the same contents. This refactoring separates the concerns within
AuctionMessageTranslator: the top level deals with events and listeners, and
the inner object deals with parsing strings.
Encapsulate Collections
We’ve developed a habit of packaging up common types, such as collections, in
our own classes, even though Java generics avoid the need to cast objects. We’re
trying to use the language of the problem we’re working on, rather than the language
of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
incidental noise about looking up and parsing values.The second is written in terms
of auction events, so there’s less of a conceptual gap between the domain and
the code.
Our rule of thumb is that we try to limit passing around types with generics (the
types enclosed in angle brackets). Particularly when applied to collections, we view
it as a form of duplication. It’s a hint that there’s a domain concept that should be
extracted into a type.
Defer Decisions
There’s a technique we’ve used a couple of times now, which is to introduce a
null implementation of a method (or even a type) to get us through the next step.
This helps us focus on the immediate task without getting dragged into thinking
about the next signiﬁcant chunk of functionality. The null Auction, for example,
allowed us to plug in a new relationship we’d discovered in a unit test without
getting pulled into messaging issues. That, in turn, meant we could stop and
think about the dependencies between our objects without the pressure of having
a broken compilation.
Keep the Code Compiling
We try to minimize the time when we have code that does not compile by keeping
changes incremental. When we have compilation failures, we can’t be quite sure
where the boundaries of our changes are, since the compiler can’t tell us. This, in
turn, means that we can’t check in to our source repository, which we like to do
often.The more code we have open, the more we have to keep in our heads which,
ironically, usually means we move more slowly. One of the great discoveries of
test-driven development is just how ﬁne-grained our development steps can be.
Chapter 13
The Sniper Makes a Bid
136


