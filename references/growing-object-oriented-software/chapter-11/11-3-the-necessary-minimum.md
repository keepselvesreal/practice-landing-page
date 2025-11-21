# 11.3 The Necessary Minimum (pp.102-105)

---
**Page 102**

public class MainWindow extends JFrame {
[…]
  public void showStatus(String status) {
sniperStatus.setText(status);
  }
}
Notes
Figure 11.4 is visible conﬁrmation that the code works.
Figure 11.4
Showing Lost status
It may not look like much, but it conﬁrms that a Sniper can establish a
connection with an auction, accept a response, and display the result.
The Necessary Minimum
In one of his school reports, Steve was noted as “a ﬁne judge of the necessary
minimum.” It seems he’s found his calling in writing software since this is a
critical skill during iteration zero.
What we hope you’ve seen in this chapter is the degree of focus that’s required
to put together your ﬁrst walking skeleton. The point is to design and validate
the initial structure of the end-to-end system—where end-to-end includes deploy-
ment to a working environment—to prove that our choices of packages, libraries,
and tooling will actually work. A sense of urgency will help the team to strip the
functionality down to the absolute minimum sufﬁcient to test their assumptions.
That’s why we didn’t put any content in our Sniper messages; it would be a di-
version from making sure that the communication and event handling work. We
didn’t sweat too hard over the detailed code design, partly because there isn’t
much but mainly because we’re just getting the pieces in place; that effort will
come soon enough.
Of course, all you see in this chapter are edited highlights. We’ve left out many
diversions and discussions as we ﬁgured out which pieces to use and how to make
them work, trawling through product documentation and discussion lists. We’ve
also left out some of our discussions about what this project is for. Iteration zero
usually brings up project chartering issues as the team looks for criteria to guide
its decisions, so the project’s sponsors should expect to ﬁeld some deep questions
about its purpose.
Chapter 11
Passing the First Test
102


---
**Page 103**

We have something visible we can present as a sign of progress, so we can
cross off the ﬁrst item on our list, as in Figure 11.5.
Figure 11.5
First item done
The next step is to start building out real functionality.
103
The Necessary Minimum


---
**Page 104**

This page intentionally left blank 


---
**Page 105**

Chapter 12
Getting Ready to Bid
In which we write an end-to-end test so that we can make the Sniper
bid in an auction. We start to interpret the messages in the auction
protocol and discover some new classes in the process. We write our
ﬁrst unit tests and then refactor out a helper class. We describe every
last detail of this effort to show what we were thinking at the time.
An Introduction to the Market
Now, to continue with the skeleton metaphor, we start to ﬂesh out the application.
The core behavior of a Sniper is that it makes a higher bid on an item in an auction
when there’s a change in price. Going back to our to-do list, we revisit the next
couple of items:
•
Single item: join, bid, and lose. When a price comes in, send a bid raised
by the minimum increment deﬁned by the auction. This amount will be
included in the price update information.
•
Single item: join, bid, and win. Distinguish which bidder is currently winning
the auction and don’t bid against ourselves.
We know there’ll be more coming, but this is a coherent slice of functionality
that will allow us to explore the design and show concrete progress.
In any distributed system similar to this one there are lots of interesting failure
and timing issues, but our application only has to deal with the client side of the
protocol. We rely on the underlying XMPP protocol to deal with many common
distributed programming problems; in particular, we expect it to ensure that
messages between a bidder and an auction arrive in the same order in which they
were sent.
As we described in Chapter 5, we start the next feature with an acceptance
test. We used our ﬁrst test in the previous chapter to help ﬂush out the structure
of our application. From now on, we can use acceptance tests to show incremental
progress.
105


