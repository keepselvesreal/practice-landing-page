Line 1: 
Line 2: --- 페이지 100 ---
Line 3: Chapter 9
Line 4: Commissioning an Auction
Line 5: Sniper
Line 6: To Begin at the Beginning
Line 7: In which we are commissioned to build an application that automati-
Line 8: cally bids in auctions. We sketch out how it should work and what
Line 9: the major components should be. We put together a rough plan for the
Line 10: incremental steps in which we will grow the application.
Line 11: We’re a development team for Markup and Gouge, a company that buys antiques
Line 12: on the professional market to sell to clients “with the best possible taste.” Markup
Line 13: and Gouge has been following the industry and now does a lot of its buying on-
Line 14: line, largely from Southabee’s, a venerable auction house that is keen to grow
Line 15: online. The trouble is that our buyers are spending a lot of their time manually
Line 16: checking the state of an auction to decide whether or not to bid, and even missed
Line 17: a couple of attractive items because they could not respond quickly enough.
Line 18: After intense discussion, the management decides to commission an Auction
Line 19: Sniper, an application that watches online auctions and automatically bids
Line 20: slightly higher whenever the price changes, until it reaches a stop-price or the
Line 21: auction closes. The buyers are keen to have this new application and some of
Line 22: them agree to help us clarify what to build.
Line 23: We start by talking through their ideas with the buyers’ group and ﬁnd that,
Line 24: to avoid confusion, we need to agree on some basic terms:
Line 25: •
Line 26: Item is something that can be identiﬁed and bought.
Line 27: •
Line 28: Bidder is a person or organization that is interested in buying an item.
Line 29: •
Line 30: Bid is a statement that a bidder will pay a given price for an item.
Line 31: •
Line 32: Current price is the current highest bid for the item.
Line 33: •
Line 34: Stop price is the most a bidder is prepared to pay for an item.
Line 35: •
Line 36: Auction is a process for managing bids for an item.
Line 37: •
Line 38: Auction house is an institution that hosts auctions.
Line 39: 75
Line 40: 
Line 41: --- 페이지 101 ---
Line 42: The discussions generate a long list of requirements, such as being able to bid
Line 43: for related groups of items. There’s no way anyone could deliver everything
Line 44: within a useful time, so we talk through the options and the buyers reluctantly
Line 45: agree that they’d rather get a basic application working ﬁrst. Once that’s in place,
Line 46: we can make it more powerful.
Line 47: It turns out that in the online system there’s an auction for every item, so we
Line 48: decide to use an item’s identiﬁer to refer to its auction. In practice, it also turns
Line 49: out that the Sniper application doesn’t have to concern itself with managing any
Line 50: items we’ve bought, since other systems will handle payment and delivery.
Line 51: We decide to build the Auction Sniper as a Java Swing application. It will run
Line 52: on a desktop and allow the user to bid for multiple items at a time. It will show
Line 53: the identiﬁer, stop price, and the current auction price and status for each item
Line 54: it’s sniping. Buyers will be able to add new items for sniping through the user
Line 55: interface, and the display values will change in response to events arriving from
Line 56: the auction house. The buyers are still working with our usability people, but
Line 57: we’ve agreed a rough version that looks like Figure 9.1.
Line 58: Figure 9.1
Line 59: A ﬁrst user interface
Line 60: This is obviously incomplete and not pretty, but it’s close enough to get us
Line 61: started.
Line 62: While these discussions are taking place, we also talk to the technicians at
Line 63: Southabee’s who support their online services. They send us a document that
Line 64: Chapter 9
Line 65: Commissioning an Auction Sniper
Line 66: 76
Line 67: 
Line 68: --- 페이지 102 ---
Line 69: describes their protocol for bidding in auctions, which uses XMPP (Jabber) for
Line 70: its underlying communication layer. Figure 9.2 shows how it handles multiple
Line 71: bidders sending bids over XMPP to the auction house, our Sniper being one of
Line 72: them. As the auction progresses, Southabee’s will send events to all the connected
Line 73: bidders to tell them when anyone’s bid has raised the current price and when the
Line 74: auction closes.
Line 75: Figure 9.2
Line 76: Southabee’s online auction system
Line 77: XMPP: the eXtensible Messaging and Presence Protocol
Line 78: XMPP is a protocol for streaming XML elements across the network. It was origi-
Line 79: nally designed for, and named after, the Jabber instant messaging system and
Line 80: was renamed to XMPP when submitted to the IETF for approval as an Internet
Line 81: standard. Because it is a generic framework for exchanging XML elements across
Line 82: the network, it can be used for a wide variety of applications that need to exchange
Line 83: structured data in close to real time.
Line 84: XMPP has a decentralized, client/server architecture. There is no central server,
Line 85: in contrast with other chat services such as AOL Instant Messenger or MSN
Line 86: Messenger. Anyone may run an XMPP server that hosts users and lets them
Line 87: communicate among themselves and with users hosted by other XMPP servers
Line 88: on the network.
Line 89: A user can log in to an XMPP server simultaneously from multiple devices or
Line 90: clients, known in XMPP terminology as resources. A user assigns each resource
Line 91: a priority. Unless addressed to a speciﬁc resource, messages sent to the user are
Line 92: delivered to this user’s highest priority resource that is currently logged in.
Line 93: Every user on the network has a unique Jabber ID (usually abbreviated as JID)
Line 94: that is rather like an e-mail address. A JID contains a username and a DNS address
Line 95: of the server where that user resides, separated by an at sign (@, for example,
Line 96: username@example.com), and can optionally be sufﬁxed with a resource name after
Line 97: a forward slash (for example, username@example.com/office).
Line 98: 77
Line 99: To Begin at the Beginning
Line 100: 
Line 101: --- 페이지 103 ---
Line 102: Communicating with an Auction
Line 103: The Auction Protocol
Line 104: The protocol for messages between a bidder and an auction house is simple.
Line 105: Bidders send commands, which can be:
Line 106: Join
Line 107: A bidder joins an auction. The sender of the XMPP message identiﬁes the
Line 108: bidder, and the name of the chat session identiﬁes the item.
Line 109: Bid
Line 110: A bidder sends a bidding price to the auction.
Line 111: Auctions send events, which can be:
Line 112: Price
Line 113: An auction reports the currently accepted price. This event also includes the
Line 114: minimum increment that the next bid must be raised by, and the name of
Line 115: bidder who bid this price. The auction will send this event to a bidder when
Line 116: it joins and to all bidders whenever a new bid has been accepted.
Line 117: Close
Line 118: An auction announces that it has closed. The winner of the last price event
Line 119: has won the auction.
Line 120: Figure 9.3
Line 121: A bidder’s behavior represented as a state machine
Line 122: Chapter 9
Line 123: Commissioning an Auction Sniper
Line 124: 78
Line 125: 
Line 126: --- 페이지 104 ---
Line 127: We spend some time working through the documentation and talking to
Line 128: Southabee’s On-Line support people, and ﬁgure out a state machine that shows
Line 129: the transitions a Sniper can make. Essentially, a Sniper joins an auction, then
Line 130: there are some rounds of bidding, until the auction closes, at which point the
Line 131: Sniper will have won or lost; see Figure 9.3. We’ve left out the stop price for now
Line 132: to keep things simple; it’ll turn up in Chapter 18.
Line 133: The XMPP Messages
Line 134: Southabee’s On-Line has also sent us details of the formats they use within the
Line 135: XMPP messages. They’re pretty simple, since they only involve a few names and
Line 136: values, and are serialized in a single line with key/value pairs. Each line starts
Line 137: with a version number for the protocol itself. The messages look like this:
Line 138: SOLVersion: 1.1; Command: JOIN; 
Line 139: SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line 140: SOLVersion: 1.1; Command: BID; Price: 199;
Line 141: SOLVersion: 1.1; Event: CLOSE;
Line 142: Southabee’s On-Line uses login names to identify items for sale, so to bid
Line 143: for an item with identiﬁer 12793, a client would start a chat with the “user”
Line 144: auction-12793 at the Southabee’s server. The server can tell who is bidding from
Line 145: the identity of the caller, assuming the accounts have been set up beforehand.
Line 146: Getting There Safely
Line 147: Even a small application like this is too large to write in one go, so we need to
Line 148: ﬁgure out, roughly, the steps we might take to get there. A critical technique with
Line 149: incremental development is learning how to slice up the functionality so that it
Line 150: can be built a little at a time. Each slice should be signiﬁcant and concrete enough
Line 151: that the team can tell when it’s done, and small enough to be focused on one
Line 152: concept and achievable quickly. Dividing our work into small, coherent chunks
Line 153: also helps us manage the development risk. We get regular, concrete feedback
Line 154: on the progress we’re making, so we can adjust our plan as the team discovers
Line 155: more about the domain and the technologies.
Line 156: Our immediate task is to ﬁgure out a series of incremental development steps
Line 157: for the Sniper application. The ﬁrst is absolutely the smallest feature we can build,
Line 158: the “walking skeleton” we described in “First, Test a Walking Skeleton”
Line 159: (page 32). Here, the skeleton will cut a minimum path through Swing, XMPP,
Line 160: and our application; it’s just enough to show that we can plug these components
Line 161: together. Each subsequent step adds a single element of complexity to the existing
Line 162: application, building on the work that’s done before. After some discussion, we
Line 163: come up with this sequence of features to build:
Line 164: 79
Line 165: Getting There Safely
Line 166: 
Line 167: --- 페이지 105 ---
Line 168: Single item: join, lose without bidding
Line 169: This is our starting case where we put together the core infrastructure; it is
Line 170: the subject of Chapter 10.
Line 171: Single item: join, bid, and lose
Line 172: Add bidding to the basic connectivity.
Line 173: Single item: join, bid, and win
Line 174: Distinguish who sent the winning bid.
Line 175: Show price details
Line 176: Start to fill out the user interface.
Line 177: Multiple items
Line 178: Support bidding for multiple items in the same application.
Line 179: Add items through the user interface
Line 180: Implement input via the user interface.
Line 181: Stop bidding at the stop price
Line 182: More intelligence in the Sniper algorithm.
Line 183: Within the list, the buyers have prioritized the user interface over the stop
Line 184: price, partly because they want to make sure they’ll feel comfortable with the
Line 185: application and partly because there won’t be an easy way to add multiple items,
Line 186: each with its own stop price, without a user interface.
Line 187: Once this is stable, we can work on more complicated scenarios, such as
Line 188: retrying if a bid failed or using different strategies for bidding. For now,
Line 189: implementing just these features should keep us busy.
Line 190: Figure 9.4
Line 191: The initial plan
Line 192: Chapter 9
Line 193: Commissioning an Auction Sniper
Line 194: 80
Line 195: 
Line 196: --- 페이지 106 ---
Line 197: We don’t know if this is exactly the order of steps we’ll take, but we believe
Line 198: we need all of this, and we can adjust as we go along. To keep ourselves
Line 199: focused, we’ve written the plan on an index card, as in Figure 9.4.
Line 200: This Isn’t Real
Line 201: By now you may be raising objections about all the practicalities we’ve skipped
Line 202: over. We saw them too. We’ve taken shortcuts with the process and design to
Line 203: give you a feel of how a real project works while remaining within the limits of
Line 204: a book. In particular:
Line 205: •
Line 206: This isn’t a realistic architecture: XMPP is neither reliable nor secure, and
Line 207: so is unsuitable for transactions. Ensuring any of those qualities is outside
Line 208: our scope. That said, the fundamental techniques that we describe still apply
Line 209: whatever the underlying architecture may be. (In our defense, we see that
Line 210: major systems have been built on a protocol as inappropriate as HTTP, so
Line 211: perhaps we’re not as unrealistic as we fear.)
Line 212: •
Line 213: This isn’t Agile Planning: We rushed through the planning of the project
Line 214: to produce a single to-do list. In a real project, we’d likely have a view of
Line 215: the whole deliverable (a release plan) before jumping in. There are good
Line 216: descriptions of how to do agile planning in other books, such as [Shore07]
Line 217: and [Cohn05].
Line 218: •
Line 219: This isn’t realistic usability design: Good user experience design investigates
Line 220: what the end user is really trying to achieve and uses that to create a con-
Line 221: sistent experience. The User Experience community has been engaging with
Line 222: the Agile Development community for some time on how to do this itera-
Line 223: tively. This project is simple enough that we can draft a vision of what we
Line 224: want to achieve and work towards it.
Line 225: 81
Line 226: This Isn’t Real
Line 227: 
Line 228: --- 페이지 107 ---
Line 229: This page intentionally left blank 