# 9.2 Communicating with an Auction (pp.78-79)

---
**Page 78**

Communicating with an Auction
The Auction Protocol
The protocol for messages between a bidder and an auction house is simple.
Bidders send commands, which can be:
Join
A bidder joins an auction. The sender of the XMPP message identiﬁes the
bidder, and the name of the chat session identiﬁes the item.
Bid
A bidder sends a bidding price to the auction.
Auctions send events, which can be:
Price
An auction reports the currently accepted price. This event also includes the
minimum increment that the next bid must be raised by, and the name of
bidder who bid this price. The auction will send this event to a bidder when
it joins and to all bidders whenever a new bid has been accepted.
Close
An auction announces that it has closed. The winner of the last price event
has won the auction.
Figure 9.3
A bidder’s behavior represented as a state machine
Chapter 9
Commissioning an Auction Sniper
78


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


