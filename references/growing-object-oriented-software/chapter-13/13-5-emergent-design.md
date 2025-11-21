# 13.5 Emergent Design (pp.137-139)

---
**Page 137**

Emergent Design
What we hope is becoming clear from this chapter is how we’re growing a design
from what looks like an unpromising start. We alternate, more or less, between
adding features and reﬂecting on—and cleaning up—the code that results. The
cleaning up stage is essential, since without it we would end up with an unmain-
tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
what to do, conﬁdent that we will take the time when we’re ready. In the mean-
time, we keep our code as clean as possible, moving in small increments and using
techniques such as null implementation to minimize the time when it’s broken.
Figure 13.5 shows that we’re building up a layer around our core implementa-
tion that “protects” it from its external dependencies. We think this is just good
practice, but what’s interesting is that we’re getting there incrementally, by
looking for features in classes that either go together or don’t. Of course we’re
inﬂuenced by our experience of working on similar codebases, but we’re trying
hard to follow what the code is telling us instead of imposing our preconceptions.
Sometimes, when we do this, we ﬁnd that the domain takes us in the most
surprising directions.
137
Emergent Design


---
**Page 138**

This page intentionally left blank 


---
**Page 139**

Chapter 14
The Sniper Wins the Auction
In which we add another feature to our Sniper and let it win an auction.
We introduce the concept of state to the Sniper which we test by listen-
ing to its callbacks. We ﬁnd that even this early, one of our refactorings
has paid off.
First, a Failing Test
We have a Sniper that can respond to price changes by bidding more, but it
doesn’t yet know when it’s successful. Our next feature on the to-do list is to
win an auction. This involves an extra state transition, as you can see in
Figure 14.1:
Figure 14.1
A sniper bids, then wins
To represent this, we add an end-to-end test based on sniperMakesAHigherBid-
ButLoses() with a different conclusion—sniperWinsAnAuctionByBiddingHigher().
Here’s the test, with the new features highlighted:
139


