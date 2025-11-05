# 12.5 Finish the Job (pp.121-123)

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


---
**Page 122**

This page intentionally left blank 


---
**Page 123**

Chapter 13
The Sniper Makes a Bid
In which we extract an AuctionSniper class and tease out its dependen-
cies. We plug our new class into the rest of the application, using an
empty implementation of auction until we’re ready to start sending
commands. We close the loop back to the auction house with an
XMPPAuction class. We continue to carve new types out of the code.
Introducing AuctionSniper
A New Class, with Dependencies
Our application accepts Price events from the auction, but cannot interpret them
yet. We need code that will perform two actions when the currentPrice() method
is called: send a higher bid to the auction and update the status in the user inter-
face. We could extend Main, but that class is looking rather messy—it’s already
doing too many things at once. It feels like this is a good time to introduce
what we should call an “Auction Sniper,” the component at the heart of our
application, so we create an AuctionSniper class. Some of its intended behavior
is currently buried in Main, and a good start would be to extract it into our new
class—although, as we’ll see in a moment, it will take a little effort.
Given that an AuctionSniper should respond to Price events, we decide to
make it implement AuctionEventListener rather than Main. The question is what
to do about the user interface. If we consider moving this method:
public void auctionClosed() {
  SwingUtilities.invokeLater(new Runnable() {
    public void run() {
       ui.showStatus(MainWindow.STATUS_LOST);
    }
  });
}
does it really make sense for an AuctionSniper to know about the implementation
details of the user interface, such as the use of the Swing thread? We’d be at risk
of breaking the “single responsibility” principle again. Surely an AuctionSniper
ought to be concerned with bidding policy and only notify status changes in
its terms?
123


