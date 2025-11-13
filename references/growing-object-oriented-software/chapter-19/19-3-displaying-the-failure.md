# 19.3 Displaying the Failure (pp.218-219)

---
**Page 218**

such as the event type or current price. We write a couple of tests to conﬁrm that
we can catch these, for example:
@Test public void
notifiesAuctionFailedWhenEventTypeMissing() {
  context.checking(new Expectations() {{  
    exactly(1).of(listener).auctionFailed(); 
  }});
  Message message = new Message();
  message.setBody("SOLVersion: 1.1; CurrentPrice: 234; Increment: 5; Bidder: "
                  + SNIPER_ID + ";");
  translator.processMessage(UNUSED_CHAT, message);
}
Our ﬁx is to throw an exception whenever we try to get a value that has not
been set, and we deﬁne MissingValueException for this purpose.
public static class AuctionEvent { […]
  private String get(String name) throws MissingValueException {
    String value = values.get(name);
if (null == value) {
      throw new MissingValueException(name);
    }
    return value;
  }
}
Displaying the Failure
We added an auctionFailed() method to AuctionEventListener while unit-
testing AuctionMessageTranslator. This triggers a compiler warning in
AuctionSniper, so we added an empty implementation to keep going. Now
it’s time to make it work, which turns out to be easy. We write some tests in
AuctionSniperTest for the new state transitions, for example:
@Test public void
reportsFailedIfAuctionFailsWhenBidding() {
  ignoringAuction();
  allowingSniperBidding();
  expectSniperToFailWhenItIs("bidding");
  sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 
  sniper.auctionFailed(); 
}
private void expectSniperToFailWhenItIs(final String state) {
  context.checking(new Expectations() {{
    atLeast(1).of(sniperListener).sniperStateChanged(
        new SniperSnapshot(ITEM_ID, 00, 0, SniperState.FAILED)); 
                                    when(sniperState.is(state));
  }});
}
Chapter 19
Handling Failure
218


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


