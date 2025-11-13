# 18.1 A More Useful Application (pp.205-205)

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


