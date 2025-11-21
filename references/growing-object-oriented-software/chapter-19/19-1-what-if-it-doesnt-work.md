# 19.1 What If It Doesn't Work? (pp.215-217)

---
**Page 215**

Chapter 19
Handling Failure
In which we address the reality of programming in an imperfect world,
and add failure reporting. We add a new auction event that reports
failure. We attach a new event listener that will turn off the Sniper if
it fails. We also write a message to a log and write a unit test that mocks
a class, for which we’re very sorry.
To avoid trying your patience any further, we close our example here.
So far, we’ve been prepared to assume that everything just works. This might be
reasonable if the application is not supposed to last—perhaps it’s acceptable if
it just crashes and we restart it or, as in this case, we’ve been mainly concerned
with demonstrating and exploring the domain. Now it’s time to start being explicit
about how we deal with failures.
What If It Doesn’t Work?
Our product people are concerned that Southabee’s On-Line has a reputation
for occasionally failing and sending incorrectly structured messages, so they want
us to show that we can cope. It turns out that the system we talk to is actually
an aggregator for multiple auction feeds, so the failure of an individual auction
does not imply that the whole system is unsafe. Our policy will be that when we
receive a message that we cannot interpret, we will mark that auction as Failed
and ignore any further updates, since it means we can no longer be sure what’s
happening. Once an auction has failed, we make no attempt to recover.1
In practice, reporting a message failure means that we ﬂush the price and bid
values, and show the status as Failed for the offending item. We also record the
event somewhere so that we can deal with it later. We could make the display
of the failure more obvious, for example by coloring the row, but we’ll keep this
version simple and leave any extras as an exercise for the reader.
The end-to-end test shows that a working Sniper receives a bad message, dis-
plays and records the failure, and then ignores further updates from this auction:
1. We admit that it’s unlikely that an auction site that regularly garbles its messages
will survive for long, but it’s a simple example to work through. We also doubt that
any serious bidder will be happy to let their bid lie hanging, not knowing whether
they’ve bought something or lost to a rival. On the other hand, we’ve seen less plau-
sible systems succeed in the world, propped up by an army of special handling, so
perhaps you can let us get away with this one.
215


---
**Page 216**

@Test public void
sniperReportsInvalidAuctionMessageAndStopsRespondingToEvents()
    throws Exception 
{
  String brokenMessage = "a broken message";
  auction.startSellingItem();
  auction2.startSellingItem();
  application.startBiddingIn(auction, auction2);
  auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  auction.reportPrice(500, 20, "other bidder");
  auction.hasReceivedBid(520, ApplicationRunner.SNIPER_XMPP_ID);
  auction.sendInvalidMessageContaining(brokenMessage);
  application.showsSniperHasFailed(auction);
  auction.reportPrice(520, 21, "other bidder");
waitForAnotherAuctionEvent();
  application.reportsInvalidMessage(auction, brokenMessage);
  application.showsSniperHasFailed(auction);
}
private void waitForAnotherAuctionEvent() throws Exception {
  auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  auction2.reportPrice(600, 6, "other bidder");
  application.hasShownSniperIsBidding(auction2, 600, 606);
}
where sendInvalidMessageContaining() sends the given invalid string via a chat
to the Sniper, and showsSniperHasFailed() checks that the status for the item is
Failed and that the price values have been zeroed. We park the implementation
of reportsInvalidMessage() for the moment; we’ll come back to it later in this
chapter.
Testing That Something Doesn’t Happen
You’ll have noticed the waitForAnotherAuctionEvent() method which forces an
unrelated Sniper event and then waits for it to work through the system. Without
this call, it would be possible for the ﬁnal showSniperHasFailed() check to pass
incorrectly because it would pick up the previous Sniper state—before the system
has had time to process the relevant price event. The additional event holds back
the test just long enough to make sure that the system has caught up. See
Chapter 27 for more on testing with asynchrony.
To get this test to fail appropriately, we add a FAILED value to the SniperState
enumeration, with an associated text mapping in SnipersTabelModel. The
test fails:
Chapter 19
Handling Failure
216


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


