# 19.2 Detecting the Failure (pp.217-218)

---
**Page 217**

[…] but... 
  it is not table with row with cells 
    <label with text "item-54321">, <label with text "0">, 
    <label with text "0">, <label with text "Failed">
   because 
in row 0: component 1 text was "500"
     in row 1: component 0 text was "item-65432"
It shows that there are two rows in the table: the second is for the other auction,
and the ﬁrst is showing that the current price is 500 when it should have been
ﬂushed to 0. This failure is our marker for what we need to build next.
Detecting the Failure
The failure will actually occur in the AuctionMessageTranslator (last shown in
Chapter 14) which will throw a runtime exception when it tries to parse the
message. The Smack library drops exceptions thrown by MessageHandlers,
so we have to make sure that our handler catches everything. As we write
a unit test for a failure in the translator, we realize that we need to report a
new type of auction event, so we add an auctionFailed() method to the
AuctionEventListener interface.
@Test public void
notifiesAuctionFailedWhenBadMessageReceived() {
  context.checking(new Expectations() {{  
    exactly(1).of(listener).auctionFailed(); 
  }});
  Message message = new Message();
  message.setBody("a bad message");
  translator.processMessage(UNUSED_CHAT, message);
}
This fails with an ArrayIndexOutOfBoundsException when it tries to unpack a
name/value pair from the string. We could be precise about which exceptions to
catch but in practice it doesn’t really matter here: we either parse the message or
we don’t, so to make the test pass we extract the bulk of processMessage() into
a translate() method and wrap a try/catch block around it.
public class AuctionMessageTranslator implements MessageListener {
  public void processMessage(Chat chat, Message message) {
    try {
translate(message.getBody());
    } catch (Exception parseException) {
      listener.auctionFailed();
    }
  }
While we’re here, there’s another failure mode we’d like to check. It’s possible
that a message is well-formed but incomplete: it might be missing one of its ﬁelds
217
Detecting the Failure


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


