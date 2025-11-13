# 14.6 Making Steady Progress (pp.148-149)

---
**Page 148**

Having previously made a fuss about PriceSource, are we being inconsistent
here by using a boolean for isWinning? Our excuse is that we did try an enum
for the Sniper state, but it just looked too complicated. The ﬁeld is private to
AuctionSniper, which is small enough so it’s easy to change later and the code
reads well.
The unit and end-to-end tests all pass now, so we can cross off another item
from the to-do list in Figure 14.3.
Figure 14.3
The Sniper wins
There are more tests we could write—for example, to describe the transitions
from bidding to winning and back again, but we’ll leave those as an exercise for
you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
functionality.
Making Steady Progress
As always, we made steady progress by adding little slices of functionality. First
we made the Sniper show when it’s winning, then when it has won. We used
empty implementations to get us through the compiler when we weren’t ready
to ﬁll in the code, and we stayed focused on the immediate task.
One of the pleasant surprises is that, now the code is growing a little, we’re
starting to see some of our earlier effort pay off as new features just ﬁt into the
existing structure. The next tasks we have to implement will shake this up.
Chapter 14
The Sniper Wins the Auction
148


---
**Page 149**

Chapter 15
Towards a Real User Interface
In which we grow the user interface from a label to a table. We achieve
this by adding a feature at a time, instead of taking the risk of replacing
the whole thing in one go. We discover that some of the choices we
made are no longer valid, so we dare to change existing code. We
continue to refactor and sense that a more interesting structure is
starting to appear.
A More Realistic Implementation
What Do We Have to Do Next?
So far, we’ve been making do with a simple label in the user interface. That’s
been effective for helping us clarify the structure of the application and prove
that our ideas work, but the next tasks coming up will need more, and the client
wants to see something that looks closer to Figure 9.1. We will need to show
more price details from the auction and handle multiple items.
The simplest option would be just to add more text into the label, but we think
this is the right time to introduce more structure into the user interface. We de-
ferred putting effort into this part of the application, and we think we should
catch up now to be ready for the more complex requirements we’re about to
implement. We decide to make the obvious choice, given our use of Swing, and
replace the label with a table component. This decision gives us a clear direction
for where our design should go next.
The Swing pattern for using a JTable is to associate it with a TableModel. The
table component queries the model for values to present, and the model notiﬁes
the table when those values change. In our application, the relationships will
look like Figure 15.1.  We call the new class SnipersTableModel because we want
it to support multiple Snipers. It will accept updates from the Snipers and provide
a representation of those values to its JTable.
The question is how to get there from here.
149


