# 9.3 Getting There Safely (pp.79-81)

---
**Page 79**

We spend some time working through the documentation and talking to
Southabee’s On-Line support people, and ﬁgure out a state machine that shows
the transitions a Sniper can make. Essentially, a Sniper joins an auction, then
there are some rounds of bidding, until the auction closes, at which point the
Sniper will have won or lost; see Figure 9.3. We’ve left out the stop price for now
to keep things simple; it’ll turn up in Chapter 18.
The XMPP Messages
Southabee’s On-Line has also sent us details of the formats they use within the
XMPP messages. They’re pretty simple, since they only involve a few names and
values, and are serialized in a single line with key/value pairs. Each line starts
with a version number for the protocol itself. The messages look like this:
SOLVersion: 1.1; Command: JOIN; 
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Command: BID; Price: 199;
SOLVersion: 1.1; Event: CLOSE;
Southabee’s On-Line uses login names to identify items for sale, so to bid
for an item with identiﬁer 12793, a client would start a chat with the “user”
auction-12793 at the Southabee’s server. The server can tell who is bidding from
the identity of the caller, assuming the accounts have been set up beforehand.
Getting There Safely
Even a small application like this is too large to write in one go, so we need to
ﬁgure out, roughly, the steps we might take to get there. A critical technique with
incremental development is learning how to slice up the functionality so that it
can be built a little at a time. Each slice should be signiﬁcant and concrete enough
that the team can tell when it’s done, and small enough to be focused on one
concept and achievable quickly. Dividing our work into small, coherent chunks
also helps us manage the development risk. We get regular, concrete feedback
on the progress we’re making, so we can adjust our plan as the team discovers
more about the domain and the technologies.
Our immediate task is to ﬁgure out a series of incremental development steps
for the Sniper application. The ﬁrst is absolutely the smallest feature we can build,
the “walking skeleton” we described in “First, Test a Walking Skeleton”
(page 32). Here, the skeleton will cut a minimum path through Swing, XMPP,
and our application; it’s just enough to show that we can plug these components
together. Each subsequent step adds a single element of complexity to the existing
application, building on the work that’s done before. After some discussion, we
come up with this sequence of features to build:
79
Getting There Safely


---
**Page 80**

Single item: join, lose without bidding
This is our starting case where we put together the core infrastructure; it is
the subject of Chapter 10.
Single item: join, bid, and lose
Add bidding to the basic connectivity.
Single item: join, bid, and win
Distinguish who sent the winning bid.
Show price details
Start to fill out the user interface.
Multiple items
Support bidding for multiple items in the same application.
Add items through the user interface
Implement input via the user interface.
Stop bidding at the stop price
More intelligence in the Sniper algorithm.
Within the list, the buyers have prioritized the user interface over the stop
price, partly because they want to make sure they’ll feel comfortable with the
application and partly because there won’t be an easy way to add multiple items,
each with its own stop price, without a user interface.
Once this is stable, we can work on more complicated scenarios, such as
retrying if a bid failed or using different strategies for bidding. For now,
implementing just these features should keep us busy.
Figure 9.4
The initial plan
Chapter 9
Commissioning an Auction Sniper
80


---
**Page 81**

We don’t know if this is exactly the order of steps we’ll take, but we believe
we need all of this, and we can adjust as we go along. To keep ourselves
focused, we’ve written the plan on an index card, as in Figure 9.4.
This Isn’t Real
By now you may be raising objections about all the practicalities we’ve skipped
over. We saw them too. We’ve taken shortcuts with the process and design to
give you a feel of how a real project works while remaining within the limits of
a book. In particular:
•
This isn’t a realistic architecture: XMPP is neither reliable nor secure, and
so is unsuitable for transactions. Ensuring any of those qualities is outside
our scope. That said, the fundamental techniques that we describe still apply
whatever the underlying architecture may be. (In our defense, we see that
major systems have been built on a protocol as inappropriate as HTTP, so
perhaps we’re not as unrealistic as we fear.)
•
This isn’t Agile Planning: We rushed through the planning of the project
to produce a single to-do list. In a real project, we’d likely have a view of
the whole deliverable (a release plan) before jumping in. There are good
descriptions of how to do agile planning in other books, such as [Shore07]
and [Cohn05].
•
This isn’t realistic usability design: Good user experience design investigates
what the end user is really trying to achieve and uses that to create a con-
sistent experience. The User Experience community has been engaging with
the Agile Development community for some time on how to do this itera-
tively. This project is simple enough that we can draft a vision of what we
want to achieve and work towards it.
81
This Isn’t Real


