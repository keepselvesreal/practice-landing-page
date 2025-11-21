# 15.6 Observations (pp.171-175)

---
**Page 171**

The acceptance test passes, and we can see the result in Figure 15.5.
Figure 15.5
Sniper with column headers
Enough for Now
There’s more we should do, such as set up borders and text alignment, to tune
the user interface. We might do that by associating CellRenderers with each
Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
as an exercise for the reader, since they don’t add any more insight into our
development process.
In the meantime, we can cross off one more task from our to-do list:
Figure 15.6.
Figure 15.6
The Sniper shows price information
Observations
Single Responsibilities
SnipersTableModel has one responsibility: to represent the state of our bidding
in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
171
Observations


---
**Page 172**

But’s” (page 51). We’ve seen too much user interface code that is brittle because
it has business logic mixed in. In this case, we could also have made the model
responsible for deciding whether to bid (“because that would be simpler”), but
that would make it harder to respond when either the user interface or the bidding
policy change. It would be harder to even ﬁnd the bidding policy, which is why
we isolated it in AuctionSniper.
Keyhole Surgery for Software
In this chapter we repeatedly used the practice of adding little slices of behavior
all the way through the system: replace a label with a table, get that working;
show the Sniper bidding, get that working; add the other values, get that
working. In all of these cases, we’ve ﬁgured out where we want to get to (always
allowing that we might discover a better alternative along the way), but we want
to avoid ripping the application apart to get there. Once we start a major rework,
we can’t stop until it’s ﬁnished, we can’t check in without branching, and merging
with rest of the team is harder. There’s a reason that surgeons prefer keyhole
surgery to opening up a patient—it’s less invasive and cheaper.
Programmer Hyper-Sensitivity
We have a well-developed sense of the value of our own time. We keep an eye
out for activities that don’t seem to be making the best of our (doubtless signiﬁ-
cant) talents, such as boiler-plate copying and adapting code: if we had the right
abstraction, we wouldn’t have to bother. Sometimes this just has to be done, es-
pecially when working with existing code—but there are fewer excuses when it’s
our own. Deciding when to change the design requires a good sense for trade-
offs, which implies both sensitivity and technical maturity: “I’m about to repeat
this code with minor variations, that seems dull and wasteful” as against “This
may not be the right time to rework this, I don’t understand it yet.”
We don’t have a simple, reproducible technique here; it requires skill and ex-
perience. Developers should have a habit of reﬂecting on their activity, on the
best way to invest their time for the rest of a coding session. This might mean
carrying on exactly as before, but at least they’ll have thought about it.
Celebrate Changing Your Mind
When the facts change, I change my mind. What do you do, sir?
—John Maynard Keynes
During this chapter, we renamed several features in the code. In many develop-
ment cultures, this is viewed as a sign of weakness, as an inability to do a proper
job. Instead, we think this is an essential part of our development process. Just
Chapter 15
Towards a Real User Interface
172


---
**Page 173**

as we learn more about what the structure should be by using the code we’ve
written, we learn more about the names we’ve chosen when we work with them.
We see how the type and method names ﬁt together and whether the concepts
are clear, which stimulates the discovery of new ideas. If the name of a feature
isn’t right, the only smart thing to do is change it and avoid countless hours of
confusion for all who will read the code later.
This Isn’t the Only Solution
Examples in books, such as this one, tend to read as if there was an inevitability
about the solution. That’s partly because we put effort into making the narrative
ﬂow, but it’s also because presenting one solution tends to drive others out of
the reader’s consciousness. There are other variations we could have considered,
some of which might even resurface as the example develops.
For example, we could argue that AuctionSniper doesn’t need to know whether
it’s won or lost the auction—just whether it should bid or not. At present, the
only part of the application that cares about winning is the user interface, and
it would certainly simplify the AuctionSniper and SniperSnapshot if we moved
that decision away from them. We won’t do that now, because we don’t yet
know if it’s the right choice, but we ﬁnd that kicking around design options
sometimes leads to much better solutions.
173
Observations


---
**Page 174**

This page intentionally left blank 


---
**Page 175**

Chapter 16
Sniping for Multiple Items
In which we bid for multiple items, splitting the per-connection code
from the per-auction code. We use the table model we just introduced
to display the additional bids. We extend the user interface to allow
users to add items dynamically. We’re pleased to ﬁnd that we don’t
have to change the tests, just their implementation. We tease out a
“user request listener” concept, which means we can test some features
more directly. We leave the code in a bit of a mess.
Testing for Multiple Items
A Tale of Two Items
The next task on our to-do list is to be able to snipe for multiple items at the
same time. We already have much of the machinery we’ll need in place, since our
user interface is based on a table, so some minor structural changes are all we
need to make this work. Looking ahead in the list, we could combine this change
with adding items through the user interface, but we don’t think we need to do
that yet. Just focusing on this one task means we can clarify the distinction be-
tween those features that belong to the Sniper’s connection to the auction house,
and those that belong to an individual auction. So far we’ve speciﬁed the item
on the command line, but we can extend that to pass multiple items in the
argument list.
As always, we start with a test. We want our new test to show that the appli-
cation can bid for and win two different items, so we start by looking at the tests
we already have. Our current test for a successful bid, in “First, a Failing Test”
(page 152), assumes that the application has only one auction—it’s implicit in
code such as:
application.hasShownSniperIsBidding(1000, 1098);
We prepare for multiple items by passing an auction into each of the
ApplicationRunner calls, so the code now looks like:
application.hasShownSniperIsBidding(auction, 1000, 1098);
Within the ApplicationRunner, we remove the itemId ﬁeld and instead extract
the item identiﬁer from the auction parameters.
175


