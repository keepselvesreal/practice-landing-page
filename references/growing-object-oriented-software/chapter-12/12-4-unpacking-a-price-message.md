# 12.4 Unpacking a Price Message (pp.118-121)

---
**Page 118**

Figure 12.2
Introducing the AuctionMessageTranslator
What Have We Achieved?
In this baby step, we’ve extracted a single feature of our application into a separate
class, which means the functionality now has a name and can be unit-tested.
We’ve also made Main a little simpler, now that it’s no longer concerned with
interpreting the text of messages from the auction. This is not yet a big deal but
we will show, as the Sniper application grows, how this approach helps us keep
code clean and ﬂexible, with clear responsibilities and relationships between its
components.
Unpacking a Price Message
Introducing Message Event Types
We’re about to introduce a second auction message type, the current price update.
The Sniper needs to distinguish between the two, so we take another look at the
message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
simple—just a single line with a few name/value pairs. Here are examples for
the formats again:
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Event: CLOSE;
At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
types, but we’re not clear enough about the behavior to justify any meaningful
structure, so we back off the idea. We decide to start with a simplistic solution
and adapt from there.
The Second Test
The introduction of a different Price event in our second test will force us to
parse the incoming message. This test has the same structure as the ﬁrst one but
gets a different input string and expects us to call a different method on the lis-
tener. A Price message includes details of the last bid, which we need to unpack
and pass to the listener, so we include them in the signature of the new method
currentPrice(). Here’s the test:
@Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Chapter 12
Getting Ready to Bid
118


---
**Page 119**

  context.checking(new Expectations() {{
exactly(1).of(listener).currentPrice(192, 7);
  }});
  Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
                   );
  translator.processMessage(UNUSED_CHAT, message);
}
To get through the compiler, we add a method to the listener; this takes just
a keystroke in the IDE:1
public interface AuctionEventListener {
  void auctionClosed();
void currentPrice(int price, int increment);
}
The test fails.
unexpected invocation: auctionEventListener.auctionClosed()
expectations:
  ! expected once, never invoked: auctionEventListener.currentPrice(<192>, <7>)
what happened before this: nothing!
[…]
  at $Proxy6.auctionClosed()
  at auctionsniper.AuctionMessageTranslator.processMessage()
  at AuctionMessageTranslatorTest.translatesPriceMessagesAsAuctionPriceEvents()
[…]
  at JUnit4ClassRunner.run(JUnit4ClassRunner.java:42)
This time the critical phrase is:
unexpected invocation: auctionEventListener.auctionClosed()
which means that the code called the wrong method, auctionClosed(), during
the test. The Mockery isn’t expecting this call so it fails immediately, showing us
in the stack trace the line that triggered the failure (you can see the workings of
the Mockery in the line $Proxy6.auctionClosed() which is the runtime substitute
for a real AuctionEventListener). Here, the place where the code failed is obvious,
so we can just ﬁx it.
Our ﬁrst version is rough, but it passes the test.
1. Modern development environments, such as Eclipse and IDEA, will ﬁll in a missing
method on request. This means that we can write the call we’d like to make and ask
the tool to ﬁll in the declaration for us.
119
Unpacking a Price Message


---
**Page 120**

public class AuctionMessageTranslator implements MessageListener {
  private final AuctionEventListener listener;
  public AuctionMessageTranslator(AuctionEventListener listener) {
    this.listener = listener;
  }
  public void processMessage(Chat chat, Message message) {
    HashMap<String, String> event = unpackEventFrom(message);
    String type = event.get("Event");
    if ("CLOSE".equals(type)) {
      listener.auctionClosed();
    } else if ("PRICE".equals(type)) {
      listener.currentPrice(Integer.parseInt(event.get("CurrentPrice")), 
                            Integer.parseInt(event.get("Increment")));
    }
  }
  private HashMap<String, String> unpackEventFrom(Message message) {
    HashMap<String, String> event = new HashMap<String, String>();  
    for (String element : message.getBody().split(";")) {
      String[] pair = element.split(":");
      event.put(pair[0].trim(), pair[1].trim());
    }
    return event;
  }
}
This implementation breaks the message body into a set of key/value pairs,
which it interprets as an auction event so it can notify the AuctionEventListener.
We also have to ﬁx the FakeAuctionServer to send a real Close event rather than
the current empty message, otherwise the end-to-end tests will fail incorrectly.
public void announceClosed() throws XMPPException {
currentChat.sendMessage("SOLVersion: 1.1; Event: CLOSE;");
}
Running our end-to-end test again reminds us that we’re still working on the
bidding feature. The test shows that the Sniper status label still displays Joining
rather than Bidding.
Discovering Further Work
This code passes the unit test, but there’s something missing. It assumes that the
message is correctly structured and has the right version. Given that the message
will be coming from an outside system, this feels risky, so we need to add some
error handling. We don’t want to break the ﬂow of getting features to work, so
we add error handling to the to-do list to come back to it later (Figure 12.3).
Chapter 12
Getting Ready to Bid
120


---
**Page 121**

Figure 12.3
Added tasks for handling errors
We’re also concerned that the translator is not as clear as it could be about
what it’s doing, with its parsing and the dispatching activities mixed together.
We make a note to address this class as soon as we’ve passed the acceptance
test, which isn’t far off.
Finish the Job
Most of the work in this chapter has been trying to decide what we want to say
and how to say it: we write a high-level end-to-end test to describe what the
Sniper should implement; we write long unit test names to tell us what a class
does; we extract new classes to tease apart ﬁne-grained aspects of the functional-
ity; and we write lots of little methods to keep each layer of code at a consistent
level of abstraction. But ﬁrst, we write a rough implementation to prove that we
know how to make the code do what’s required and then we refactor—which
we’ll do in the next chapter.
We cannot emphasize strongly enough that “ﬁrst-cut” code is not ﬁnished. It’s
good enough to sort out our ideas and make sure we have everything in place,
but it’s unlikely to express its intentions cleanly. That will make it a drag on
productivity as it’s read repeatedly over the lifetime of the code. It’s like carpentry
without sanding—eventually someone ends up with a nasty splinter.
121
Finish the Job


