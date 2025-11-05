# 19.4 Disconnecting the Sniper (pp.219-221)

---
**Page 219**

We’ve added a couple more helper methods: ignoringAuction() says that we
don’t care what happens to auction, allowing events to pass through so we can
get to the failure; and, expectSniperToFailWhenItIs() describes what a failure
should look like, including the previous state of the Sniper.
All we have to do is add a failed() transition to SniperSnapshot and use it
in the new method.
public class AuctionSniper implements AuctionEventListener {
  public void auctionFailed() {
    snapshot = snapshot.failed();
    listeners.announce().sniperStateChanged(snapshot);
  } […]
public class SniperSnapshot {
  public SniperSnapshot failed() {
    return new SniperSnapshot(itemId, 0, 0, SniperState.FAILED);
  } […]
This displays the failure, as we can see in Figure 19.1.
Figure 19.1
The Sniper shows a failed auction
The end-to-end test, however, still fails. The synchronization hook we added
reveals that we haven’t disconnected the Sniper from receiving further events
from the auction.
Disconnecting the Sniper
We turn off a Sniper by removing its AuctionMessageTranslator from its Chat’s
set of MessageListeners. We can do this safely while processing a message because
Chat stores its listeners in a thread-safe “copy on write” collection. One obvious
place to do this is within processMessage() in AuctionMessageTranslator, which
receives the Chat as an argument, but we have two doubts about this. First, as
we pointed out in Chapter 12, constructing a real Chat is painful. Most of the
mocking frameworks support creating a mock class, but it makes us uncomfort-
able because then we’re deﬁning a relationship with an implementation, not a
role—we’re being too precise about our dependencies. Second, we might be as-
signing too many responsibilities to AuctionMessageTranslator; it would have
to translate the message and decide what to do when it fails.
219
Disconnecting the Sniper


---
**Page 220**

Our alternative approach is to attach another object to the translator that im-
plements this disconnection policy, using the infrastructure we already have for
notifying AuctionEventListeners.
public final class XMPPAuction implements Auction {
  public XMPPAuction(XMPPConnection connection, String auctionJID) {
    AuctionMessageTranslator translator = translatorFor(connection);
    this.chat = connection.getChatManager().createChat(auctionJID, translator);
    addAuctionEventListener(chatDisconnectorFor(translator));
  }
  private AuctionMessageTranslator translatorFor(XMPPConnection connection) {
    return new AuctionMessageTranslator(connection.getUser(), 
                                        auctionEventListeners.announce());
  }
z
  private AuctionEventListener 
chatDisconnectorFor(final AuctionMessageTranslator translator) {
    return new AuctionEventListener() {
      public void auctionFailed() { 
chat.removeMessageListener(translator);
      }
      public void auctionClosed(// empty method
      public void currentPrice( // empty method
    };
  } […]
The end-to-end test, as far as it goes, passes.
The Composition Shell Game
The issue in this design episode is not the fundamental complexity of the feature,
which is constant, but how we divide it up. The design we chose (attaching a dis-
connection listener) could be argued to be more complicated than its alternative
(detaching the chat within the translator). It certainly takes more lines of code, but
that’s not the only metric. Instead, we’re emphasizing the “single responsibility”
principle, which means each object does just one thing well and the system behavior
comes from how we assemble those objects.
Sometimes this feels as if the behavior we’re looking for is always somewhere else
(as Gertrude Stein said, “There is no there there”), which can be frustrating for
developers not used to the style. Our experience, on the other hand, is that focused
responsibilities make the code more maintainable because we don’t have to cut
through unrelated functionality to get to the piece we need. See Chapter 6 for a
longer discussion.
Chapter 19
Handling Failure
220


---
**Page 221**

Recording the Failure
Now we want to return to the end-to-end test and the reportsInvalidMessage()
method that we parked. Our requirement is that the Sniper application must log
a message about these failures so that the user’s organization can recover the
situation. This means that our test should look for a log ﬁle and check its contents.
Filling In the Test
We implement the missing check and ﬂush the log before each test, delegating
the management of the log ﬁle to an AuctionLogDriver class which uses the
Apache Commons IO library. It also cheats slightly by resetting the log manager
(we’re not really supposed to be in the same address space), since deleting the
log ﬁle can confuse a cached logger.
public class ApplicationRunner { […]
private AuctionLogDriver logDriver = new AuctionLogDriver();
  public void reportsInvalidMessage(FakeAuctionServer auction, String message)
    throws IOException 
  {
logDriver.hasEntry(containsString(message));
  }
  public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
    startSniper();
    openBiddingFor(auction, stopPrice);
  }  
  private startSniper() {
logDriver.clearLog()
    Thread thread = new Thread("Test Application") {
      @Override public void run() { // Start the application […]
  }
}
public class AuctionLogDriver {
  public static final String LOG_FILE_NAME = "auction-sniper.log";
  private final File logFile = new File(LOG_FILE_NAME);
  public void hasEntry(Matcher<String> matcher) throws IOException  {
    assertThat(FileUtils.readFileToString(logFile), matcher); 
  }
  public void clearLog() {
    logFile.delete();
    LogManager.getLogManager().reset(); 
  }
}
This new check only reassures us that we’ve fed a message through the system
and into some kind of log record—it tells us that the pieces ﬁt together. We’ll
write a more thorough test of the contents of a log record later. The end-to-end
test now fails because, of course, there’s no log ﬁle to read.
221
Recording the Failure


