# 9.1 To Begin at the Beginning (pp.75-78)

---
**Page 75**

Chapter 9
Commissioning an Auction
Sniper
To Begin at the Beginning
In which we are commissioned to build an application that automati-
cally bids in auctions. We sketch out how it should work and what
the major components should be. We put together a rough plan for the
incremental steps in which we will grow the application.
We’re a development team for Markup and Gouge, a company that buys antiques
on the professional market to sell to clients “with the best possible taste.” Markup
and Gouge has been following the industry and now does a lot of its buying on-
line, largely from Southabee’s, a venerable auction house that is keen to grow
online. The trouble is that our buyers are spending a lot of their time manually
checking the state of an auction to decide whether or not to bid, and even missed
a couple of attractive items because they could not respond quickly enough.
After intense discussion, the management decides to commission an Auction
Sniper, an application that watches online auctions and automatically bids
slightly higher whenever the price changes, until it reaches a stop-price or the
auction closes. The buyers are keen to have this new application and some of
them agree to help us clarify what to build.
We start by talking through their ideas with the buyers’ group and ﬁnd that,
to avoid confusion, we need to agree on some basic terms:
•
Item is something that can be identiﬁed and bought.
•
Bidder is a person or organization that is interested in buying an item.
•
Bid is a statement that a bidder will pay a given price for an item.
•
Current price is the current highest bid for the item.
•
Stop price is the most a bidder is prepared to pay for an item.
•
Auction is a process for managing bids for an item.
•
Auction house is an institution that hosts auctions.
75


---
**Page 76**

The discussions generate a long list of requirements, such as being able to bid
for related groups of items. There’s no way anyone could deliver everything
within a useful time, so we talk through the options and the buyers reluctantly
agree that they’d rather get a basic application working ﬁrst. Once that’s in place,
we can make it more powerful.
It turns out that in the online system there’s an auction for every item, so we
decide to use an item’s identiﬁer to refer to its auction. In practice, it also turns
out that the Sniper application doesn’t have to concern itself with managing any
items we’ve bought, since other systems will handle payment and delivery.
We decide to build the Auction Sniper as a Java Swing application. It will run
on a desktop and allow the user to bid for multiple items at a time. It will show
the identiﬁer, stop price, and the current auction price and status for each item
it’s sniping. Buyers will be able to add new items for sniping through the user
interface, and the display values will change in response to events arriving from
the auction house. The buyers are still working with our usability people, but
we’ve agreed a rough version that looks like Figure 9.1.
Figure 9.1
A ﬁrst user interface
This is obviously incomplete and not pretty, but it’s close enough to get us
started.
While these discussions are taking place, we also talk to the technicians at
Southabee’s who support their online services. They send us a document that
Chapter 9
Commissioning an Auction Sniper
76


---
**Page 77**

describes their protocol for bidding in auctions, which uses XMPP (Jabber) for
its underlying communication layer. Figure 9.2 shows how it handles multiple
bidders sending bids over XMPP to the auction house, our Sniper being one of
them. As the auction progresses, Southabee’s will send events to all the connected
bidders to tell them when anyone’s bid has raised the current price and when the
auction closes.
Figure 9.2
Southabee’s online auction system
XMPP: the eXtensible Messaging and Presence Protocol
XMPP is a protocol for streaming XML elements across the network. It was origi-
nally designed for, and named after, the Jabber instant messaging system and
was renamed to XMPP when submitted to the IETF for approval as an Internet
standard. Because it is a generic framework for exchanging XML elements across
the network, it can be used for a wide variety of applications that need to exchange
structured data in close to real time.
XMPP has a decentralized, client/server architecture. There is no central server,
in contrast with other chat services such as AOL Instant Messenger or MSN
Messenger. Anyone may run an XMPP server that hosts users and lets them
communicate among themselves and with users hosted by other XMPP servers
on the network.
A user can log in to an XMPP server simultaneously from multiple devices or
clients, known in XMPP terminology as resources. A user assigns each resource
a priority. Unless addressed to a speciﬁc resource, messages sent to the user are
delivered to this user’s highest priority resource that is currently logged in.
Every user on the network has a unique Jabber ID (usually abbreviated as JID)
that is rather like an e-mail address. A JID contains a username and a DNS address
of the server where that user resides, separated by an at sign (@, for example,
username@example.com), and can optionally be sufﬁxed with a resource name after
a forward slash (for example, username@example.com/office).
77
To Begin at the Beginning


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


