# 18.3 Observations (pp.212-215)

---
**Page 212**

Figure 18.3
The Sniper stops bidding at the stop price
Observations
User Interfaces, Incrementally
It looks like we’re making signiﬁcant changes again to the user interface at a late
stage in our development. Shouldn’t we have seen this coming? This is an active
topic for discussion in the Agile User Experience community and, as always, the
answer is “it depends, but you have more ﬂexibility than you might think.”
In truth, for a simple application like this it would make sense to work out the
user interface in more detail at the start, to make sure it’s usable and coherent.
That said, we also wanted to make a point that we can respond to changing
needs, especially if we structure our tests and code so that they’re ﬂexible, not a
dead weight. We all know that requirements will change, especially once we put
our application into production, so we should be able to respond.
Other Modeling Techniques Still Work
Some presentations of TDD appear to suggest that it supersedes all previous
software design techniques. We think TDD works best when it’s based on skill
and judgment acquired from as wide an experience as possible—which includes
taking advantage of older techniques and formats (we hope we’re not being too
controversial here).
State transition diagrams are one example of taking another view. We regularly
come across teams that have never quite ﬁgured out what the valid states and
transitions are for key concepts in their domain, and applying this simple
Chapter 18
Filling In the Details
212


---
**Page 213**

formalism often means we can clean up a lucky-dip of snippets of behavior
scattered across the code. What’s nice about state transitions diagrams is that
they map directly onto tests, so we can show that we’ve covered all the
possibilities.
The trick is to understand and use other modeling techniques for support and
guidance, not as an end in themselves—which is how they got a bad name in the
ﬁrst place. When we’re doing TDD and we’re uncertain what to do, sometimes
stepping back and opening a pack of index cards, or sketching out the interactions,
can help us regain direction.
Domain Types Are Better Than Strings
The string is a stark data structure and everywhere it is passed there
is much duplication of process. It is a perfect vehicle for hiding
information.
—Alan Perlis
Looking back, we wish we’d created the Item type earlier, probably when we
extracted UserRequestListener, instead of just using a String to represent the
thing a Sniper bids for. Had we done so, we could have added the stop price to
the existing Item class, and it would have been delivered, by deﬁnition, to where
it was needed.
We might also have noticed sooner that we do not want to index our table on
item identiﬁer but on an Item, which would open up the possibility of trying
multiple policies in a single auction. We’re not saying that we should have de-
signed more speculatively for a need that hasn’t been proved. Rather, when we
take the trouble to express the domain clearly, we often ﬁnd that we have more
options.
It’s often better to deﬁne domain types to wrap not only Strings but other
built-in types too, including collections. All we have to do is remember to apply
our own advice. As you see, sometimes we forget.
213
Observations


---
**Page 214**

This page intentionally left blank 


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


