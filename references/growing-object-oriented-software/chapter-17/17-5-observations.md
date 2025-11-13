# 17.5 Observations (pp.201-205)

---
**Page 201**

Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Figure 17.4
Adding items through the user interface
Observations
Incremental Architecture
This restructuring of Main is a key moment in the development of the application.
As Figure 17.5 shows, we now have a structure that matches the “ports and
adapters” architecture we described in “Designing for Maintainability” (page 47).
There is core domain code (for example, AuctionSniper) which depends on
bridging code (for example, SnipersTableModel) that drives or responds to
technical code (for example, JTable). We’ve kept the domain code free of any
reference to the external infrastructure. The contents of our auctionsniper
package deﬁne a model of our auction sniping business, using a self-contained
language. The exception is Main, which is our entry point and binds the domain
model and infrastructure together.
What’s important for the purposes of this example, is that we arrived at this
design incrementally, by adding features and repeatedly following heuristics.
Although we rely on our experience to guide our decisions, we reached this
solution almost automatically by just following the code and taking care to keep
it clean.
201
Observations


---
**Page 202**

Figure 17.5
The application now has a “ports and adapters”
architecture
Three-Point Contact
We wrote this refactoring up in detail because we wanted to make some points
along the way and to show that we can do signiﬁcant refactorings incrementally.
When we’re not sure what to do next or how to get there from here, one way of
coping is to scale down the individual changes we make, as Kent Beck showed
in [Beck02]. By repeatedly ﬁxing local problems in the code, we ﬁnd we can ex-
plore the design safely, never straying more than a few minutes from working
code. Usually this is enough to lead us towards a better design, and we can always
backtrack and take another path if it doesn’t work out.
One way to think of this is the rock climbing rule of “three-point contact.”
Trained climbers only move one limb at a time (a hand or a foot), to minimize
the risk of falling off. Each move is minimal and safe, but combining enough of
them will get you to the top of the route.
In “elapsed time,” this refactoring didn’t take much longer than the time you
spent reading it, which we think is a good return for the clearer separation of
concerns. With experience, we’ve learned to recognize fault lines in code so we
can often take a more direct route.
Chapter 17
Teasing Apart Main
202


---
**Page 203**

Dynamic as Well as Static Design
We did encounter one small bump whilst working on the code for this chapter.
Steve was extracting the SniperPortfolio and got stuck trying to ensure that the
sniperAdded() method was called within the Swing thread. Eventually he remem-
bered that the event is triggered by a button click anyway, so he was already
covered.
What we learn from this (apart from the need for pairing while writing book
examples) is that we should consider more than one view when refactoring code.
Refactoring is, after all, a design activity, which means we still need all the skills
we were taught—except that now we need them all the time rather than periodi-
cally. Refactoring is so focused on static structure (classes and interfaces) that
it’s easy to lose sight of an application’s dynamic structure (instances and threads).
Sometimes we just need to step back and draw out, say, an interaction diagram
like Figure 17.6:
Figure 17.6
An Interaction Diagram
An Alternative Fix to notToBeGCd
Our chosen ﬁx relies on the SniperPortfolio holding onto the reference. That’s
likely to be the case in practice, but if it ever changes we will get transient failures
that are hard to track down. We’re relying on a side effect of the application to
ﬁx an issue in the XMPP code.
An alternative would be to say that it’s a Smack problem, so our XMPP layer
should deal with it. We could make the XMPPAuctionHouse hang on to the
XMPPAuctions it creates, in which case we’d to have to add a lifecycle listener of
some sort to tell us when we’re ﬁnished with an Auction and can release it. There
is no obvious choice here; we just have to look at the circumstances and exercise
some judgment.
203
Observations


---
**Page 204**

This page intentionally left blank 


---
**Page 205**

Chapter 18
Filling In the Details
In which we introduce a stop price so we don’t bid inﬁnitely, which
means we can now be losing an auction that hasn’t yet closed. We add
a new ﬁeld to the user interface and push it through to the Sniper. We
realize we should have created an Item type much earlier.
A More Useful Application
So far the functionality has been prioritized to attract potential customers by
giving them a sense of what the application will look like. We can show items
being added and some features of sniping. It’s not a very useful application be-
cause, amongst other things, there’s no upper limit for bidding on an item—it
could be very expensive to deploy.
This is a common pattern when using Agile Development techniques to work
on a new project. The team is ﬂexible enough to respond to how the needs of
the sponsors change over time: at the beginning, the emphasis might be on
proving the concept to attract enough support to continue; later, the emphasis
might be on implementing enough functionality to be ready to deploy; later still,
the emphasis might change to providing more options to support a wider range
of users.
This dynamic is very different from both a ﬁxed design approach, where the
structure of the development has to be approved before work can begin, and a
code-and-ﬁx approach, where the system might be initially successful but not
resilient enough to adapt to its changing role.
Stop When We’ve Had Enough
Our next most pressing task (especially after recent crises in the ﬁnancial markets)
is to be able to set an upper limit, the “stop price,” for our bid for an item.
Introducing a Losing State
With the introduction of a stop price, it’s possible for a Sniper to be losing before
the auction has closed. We could implement this by just marking the Sniper as
Lost when it hits its stop price, but the users want to know the ﬁnal price when
the auction has ﬁnished after they’ve dropped out, so we model this as an extra
state. Once a Sniper has been outbid at its stop price, it will never be able to win,
205


