Line 1: 
Line 2: --- 페이지 82 ---
Line 3: Chapter 7
Line 4: Achieving Object-Oriented
Line 5: Design
Line 6: In matters of style, swim with the current; in matters of principle, stand
Line 7: like a rock.
Line 8: —Thomas Jefferson
Line 9: How Writing a Test First Helps the Design
Line 10: The design principles we outlined in the previous chapter apply to ﬁnding the
Line 11: right boundaries for an object so that it plays well with its neighbors—a caller
Line 12: wants to know what an object does and what it depends on, but not how it
Line 13: works. We also want an object to represent a coherent unit that makes sense in
Line 14: its larger environment. A system built from such components will have the
Line 15: ﬂexibility to reconﬁgure and adapt as requirements change.
Line 16: There are three aspects of TDD that help us achieve this scoping. First, starting
Line 17: with a test means that we have to describe what we want to achieve before we
Line 18: consider how. This focus helps us maintain the right level of abstraction for the
Line 19: target object. If the intention of the unit test is unclear then we’re probably
Line 20: mixing up concepts and not ready to start coding. It also helps us with information
Line 21: hiding as we have to decide what needs to be visible from outside the object.
Line 22: Second, to keep unit tests understandable (and, so, maintainable), we have to
Line 23: limit their scope. We’ve seen unit tests that are dozens of lines long, burying the
Line 24: point of the test somewhere in its setup. Such tests tell us that the component
Line 25: they’re testing is too large and needs breaking up into smaller components. The
Line 26: resulting composite object should have a clearer separation of concerns as we
Line 27: tease out its implicit structure, and we can write simpler tests for the extracted
Line 28: objects.
Line 29: Third, to construct an object for a unit test, we have to pass its dependencies
Line 30: to it, which means that we have to know what they are. This encourages context
Line 31: independence, since we have to be able to set up the target object’s environment
Line 32: before we can unit-test it—a unit test is just another context. We’ll notice that
Line 33: an object with implicit (or just too many) dependencies is painful to prepare for
Line 34: testing—and make a point of cleaning it up.
Line 35: In this chapter, we describe how we use an incremental, test-driven approach
Line 36: to nudge our code towards the design principles we described in the previous
Line 37: chapter.
Line 38: 57
Line 39: 
Line 40: --- 페이지 83 ---
Line 41: Communication over Classiﬁcation
Line 42: As we wrote in Chapter 2, we view a running system as a web of communicating
Line 43: objects, so we focus our design effort on how the objects collaborate to deliver
Line 44: the functionality we need. Obviously, we want to achieve a well-designed class
Line 45: structure, but we think the communication patterns between objects are more
Line 46: important.
Line 47: In languages such as Java, we can use interfaces to deﬁne the available messages
Line 48: between objects, but we also need to deﬁne their patterns of communication—their
Line 49: communication protocols. We do what we can with naming and convention, but
Line 50: there’s nothing in the language to describe relationships between interfaces or
Line 51: methods within an interface, which leaves a signiﬁcant part of the design implicit.
Line 52: Interface and Protocol
Line 53: Steve heard this useful distinction in a conference talk: an interface describes
Line 54: whether two components will ﬁt together, while a protocol describes whether they
Line 55: will work together.
Line 56: We use TDD with mock objects as a technique to make these communication
Line 57: protocols visible, both as a tool for discovering them during development and
Line 58: as a description when revisiting the code. For example, the unit test towards the
Line 59: end of Chapter 3 tells us that, given a certain input message, the translator
Line 60: should call listener.auctionClosed() exactly once—and nothing else. Although
Line 61: the listener interface has other methods, this test says that its protocol requires
Line 62: that auctionClosed() should be called on its own.
Line 63: @Test public void
Line 64: notifiesAuctionClosedWhenCloseMessageReceived() {
Line 65:   Message message = new Message();
Line 66:   message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line 67:   context.checking(new Expectations() {{ 
Line 68:     oneOf(listener).auctionClosed(); 
Line 69:   }});
Line 70:   translator.processMessage(UNUSED_CHAT, message); 
Line 71: }
Line 72: TDD with mock objects also encourages information hiding. We should mock
Line 73: an object’s peers—its dependencies, notiﬁcations, and adjustments we categorized
Line 74: on page 52—but not its internals. Tests that highlight an object’s neighbors help
Line 75: us to see whether they are peers, or should instead be internal to the target object.
Line 76: A test that is clumsy or unclear might be a hint that we’ve exposed too much
Line 77: implementation, and that we should rebalance the responsibilities between the
Line 78: object and its neighbors.
Line 79: Chapter 7
Line 80: Achieving Object-Oriented Design
Line 81: 58
Line 82: 
Line 83: --- 페이지 84 ---
Line 84: Value Types
Line 85: Before we go further, we want to revisit the distinction we described in “Values
Line 86: and Objects” (page 13): values are immutable, so they’re simpler and have no
Line 87: meaningful identity; objects have state, so they have identity and relationships
Line 88: with each other.
Line 89: The more code we write, the more we’re convinced that we should deﬁne
Line 90: types to represent value concepts in the domain, even if they don’t do much. It
Line 91: helps to create a consistent domain model that is more self-explanatory. If we
Line 92: create, for example, an Item type in a system, instead of just using String, we can
Line 93: ﬁnd all the code that’s relevant for a change without having to chase through the
Line 94: method calls. Speciﬁc types also reduce the risk of confusion—as the Mars Climate
Line 95: Orbiter disaster showed, feet and metres may both be represented as numbers
Line 96: but they’re different things.1 Finally, once we have a type to represent a concept,
Line 97: it usually turns out to be a good place to hang behavior, guiding us towards using
Line 98: a more object-oriented approach instead of scattering related behavior across
Line 99: the code.
Line 100: We use three basic techniques for introducing value types, which we’ve called
Line 101: (in a ﬁt of alliteration): breaking out, budding off, and bundling up.
Line 102: Breaking out
Line 103: When we ﬁnd that the code in an object is becoming complex, that’s often
Line 104: a sign that it’s implementing multiple concerns and that we can break out
Line 105: coherent units of behavior into helper types. There’s an example in “Tidying
Line 106: Up the Translator” (page 135) where we break a class that handles incoming
Line 107: messages into two parts: one to parse the message string, and one to interpret
Line 108: the result of the parsing.
Line 109: Budding off
Line 110: When we want to mark a new domain concept in the code, we often introduce
Line 111: a placeholder type that wraps a single ﬁeld, or maybe has no ﬁelds at all. As
Line 112: the code grows, we ﬁll in more detail in the new type by adding ﬁelds and
Line 113: methods. With each type that we add, we’re raising the level of abstraction
Line 114: of the code.
Line 115: Bundling up
Line 116: When we notice that a group of values are always used together, we take
Line 117: that as a suggestion that there’s a missing construct. A ﬁrst step might be to
Line 118: create a new type with ﬁxed public ﬁelds—just giving the group a name
Line 119: highlights the missing concept. Later we can migrate behavior to the new
Line 120: 1. In 1999, NASA’s Mars Climate Orbiter burned up in the planet’s atmosphere because,
Line 121: amongst other problems, the navigation software confused metric with imperial units.
Line 122: There’s a brief description at http://news.bbc.co.uk/1/hi/sci/tech/514763.stm.
Line 123: 59
Line 124: Value Types
Line 125: 
Line 126: --- 페이지 85 ---
Line 127: type, which might eventually allow us to hide its ﬁelds behind a clean
Line 128: interface, satisfying the “composite simpler than the sum of its parts” rule.
Line 129: We ﬁnd that the discovery of value types is usually motivated by trying to
Line 130: follow our design principles, rather than by responding to code stresses when
Line 131: writing tests.
Line 132: Where Do Objects Come From?
Line 133: The categories for discovering object types are similar (which is why we shoe-
Line 134: horned them into these names), except that the design guidance we get from
Line 135: writing unit tests tends to be more important. As we wrote in “External and
Line 136: Internal Quality” (page 10), we use the effort of unit testing to maintain the
Line 137: code’s internal quality. There are more examples of the inﬂuence of testing on
Line 138: design in Chapter 20.
Line 139: Breaking Out: Splitting a Large Object into a Group of
Line 140: Collaborating Objects
Line 141: When starting a new area of code, we might temporarily suspend our design
Line 142: judgment and just write code without attempting to impose much structure. This
Line 143: allows us to gain some experience in the area and test our understanding of any
Line 144: external APIs we’re developing against. After a short while, we’ll ﬁnd our code
Line 145: becoming too complex to understand and will want to clean it up. We can start
Line 146: pulling out cohesive units of functionality into smaller collaborating objects,
Line 147: which we can then unit-test independently. Splitting out a new object also forces
Line 148: us to look at the dependencies of the code we’re pulling out.
Line 149: We have two concerns about deferring cleanup. The ﬁrst is how long we should
Line 150: wait before doing something. Under time pressure, it’s tempting to leave the un-
Line 151: structured code as is and move on to the next thing (“after all, it works and it’s
Line 152: just one class…”). We’ve seen too much code where the intention wasn’t clear
Line 153: and the cost of cleanup kicked in when the team could least afford it. The second
Line 154: concern is that occasionally it’s better to treat this code as a spike—once we
Line 155: know what to do, just roll it back and reimplement cleanly. Code isn’t sacred
Line 156: just because it exists, and the second time won’t take as long.
Line 157: The Tests Say…
Line 158: Break up an object if it becomes too large to test easily, or if its test failures become
Line 159: difﬁcult to interpret. Then unit-test the new parts separately.
Line 160: Chapter 7
Line 161: Achieving Object-Oriented Design
Line 162: 60
Line 163: 
Line 164: --- 페이지 86 ---
Line 165: Looking Ahead…
Line 166: In Chapter 12, when extracting an AuctionMessageTranslator, we avoid including
Line 167: its interaction with MainWindow because that would give it too many responsibilities.
Line 168: Looking at the behavior of the new class, we identify a missing dependency,
Line 169: AuctionEventListener, which we deﬁne while writing the unit tests.We repackage
Line 170: the existing code in Main to provide an implementation for the new interface.
Line 171: AuctionMessageTranslator satisﬁes both our design heuristics: it introduces a
Line 172: separation of concerns by splitting message translation from auction display, and
Line 173: it abstracts message-handling code into a new domain-speciﬁc concept.
Line 174: Budding Off: Deﬁning a New Service That an Object Needs and
Line 175: Adding a New Object to Provide It
Line 176: When the code is more stable and has some degree of structure, we often discover
Line 177: new types by “pulling” them into existence. We might be adding behavior to an
Line 178: object and ﬁnd that, following our design principles, some new feature doesn’t
Line 179: belong inside it.
Line 180: Our response is to create an interface to deﬁne the service that the object needs
Line 181: from the object’s point of view. We write tests for the new behavior as if the
Line 182: service already exists, using mock objects to help describe the relationship between
Line 183: the target object and its new collaborator; this is how we introduced the
Line 184: AuctionEventListener we mentioned in the previous section.
Line 185: The development cycle goes like this. When implementing an object, we discover
Line 186: that it needs a service to be provided by another object. We give the new service
Line 187: a name and mock it out in the client object’s unit tests, to clarify the relationship
Line 188: between the two. Then we write an object to provide that service and, in doing
Line 189: so, discover what services that object needs. We follow this chain (or perhaps a
Line 190: directed graph) of collaborator relationships until we connect up to existing ob-
Line 191: jects, either our own or from a third-party API. This is how we implement
Line 192: “Develop from the Inputs to the Outputs” (page 43).
Line 193: We think of this as “on-demand” design: we “pull” interfaces and their imple-
Line 194: mentations into existence from the needs of the client, rather than “pushing” out
Line 195: the features that we think a class should provide.
Line 196: The Tests Say…
Line 197: When writing a test, we ask ourselves, “If this worked, who would know?” If the
Line 198: right answer to that question is not in the target object, it’s probably time to introduce
Line 199: a new collaborator.
Line 200: 61
Line 201: Where Do Objects Come From?
Line 202: 
Line 203: --- 페이지 87 ---
Line 204: Looking Ahead…
Line 205: In Chapter 13, we introduce an Auction interface. The concept of making a bid
Line 206: would have been an additional responsibility for AuctionSniper, so we introduce
Line 207: a new service for bidding—just an interface without any implementation.We write a
Line 208: new test to show the relationship between AuctionSniper and Auction. Then we
Line 209: write a concrete implementation of Auction—initially as an anonymous class in
Line 210: Main, later as XMPPAuction.
Line 211: Bundling Up: Hiding Related Objects into a Containing Object
Line 212: This is the application of the “composite simpler than the sum of its parts” rule
Line 213: (page 53). When we have a cluster of related objects that work together, we can
Line 214: package them up in a containing object. The new object hides the complexity in
Line 215: an abstraction that allows us to program at a higher level.
Line 216: The process of making an implicit concept concrete has some other nice effects.
Line 217: First, we have to give it a name which helps us understand the domain a little
Line 218: better. Second, we can scope dependencies more clearly, since we can see the
Line 219: boundaries of the concept. Third, we can be more precise with our unit testing.
Line 220: We can test the new composite object directly, and use a mock implementation
Line 221: to simplify the tests for code from which it was extracted (since, of course, we
Line 222: added an interface for the role the new object plays).
Line 223: The Tests Say…
Line 224: When the test for an object becomes too complicated to set up—when there are
Line 225: too many moving parts to get the code into the relevant state—consider bundling
Line 226: up some of the collaborating objects. There’s an example in “Bloated Constructor”
Line 227: (page 238).
Line 228: Looking Ahead…
Line 229: In Chapter 17, we introduce XMPPAuctionHouse to package up everything to do with
Line 230: the messaging infrastructure, and SniperLauncher for constructing and attaching a
Line 231: Sniper. Once extracted, the references to Swing behavior in SniperLauncher
Line 232: stand out as inappropriate, so we introduce SniperCollector to decouple the
Line 233: domains.
Line 234: Chapter 7
Line 235: Achieving Object-Oriented Design
Line 236: 62
Line 237: 
Line 238: --- 페이지 88 ---
Line 239: Identify Relationships with Interfaces
Line 240: We use Java interfaces more liberally than some other developers. This reﬂects
Line 241: our emphasis on the relationships between objects, as deﬁned by their communi-
Line 242: cation protocols. We use interfaces to name the roles that objects can play and
Line 243: to describe the messages they’ll accept.
Line 244: We also prefer interfaces to be as narrow as possible, even though that means
Line 245: we need more of them. The fewer methods there are on an interface, the more
Line 246: obvious is its role in the calling object. We don’t have to worry which other
Line 247: methods are relevant to a particular call and which were included for convenience.
Line 248: Narrow interfaces are also easier to write adapters and decorators for; there’s
Line 249: less to implement, so it’s easier to write objects that compose together well.
Line 250: “Pulling” interfaces into existence, as we described in “Budding Off,” helps
Line 251: us keep them as narrow as possible. Driving an interface from its client avoids
Line 252: leaking excess information about its implementers, which minimizes any implicit
Line 253: coupling between objects and so keeps the code malleable.
Line 254: Impl Classes Are Meaningless
Line 255: Sometimes we see code with classes named by adding “Impl” to the single interface
Line 256: they implement. This is better than leaving the class name unchanged and
Line 257: preﬁxing an “I” to the interface, but not by much. A name like BookingImpl is dupli-
Line 258: cation; it says exactly the same as implements Booking, which is a “code smell.”
Line 259: We would not be happy with such obvious duplication elsewhere in our code,
Line 260: so we ought to refactor it away.
Line 261: It might just be a naming problem. There’s always something speciﬁc about an
Line 262: implementation that can be included in the class name: it might use a bounded
Line 263: collection, communicate over HTTP, use a database for persistence, and so on.
Line 264: A bridging class is even easier to name, since it will belong in one domain but
Line 265: implement interfaces in another.
Line 266: If there really isn’t a good implementation name, it might mean that the interface
Line 267: is poorly named or designed. Perhaps it’s unfocused because it has too many re-
Line 268: sponsibilities; or it’s named after its implementation rather than its role in the client;
Line 269: or it’s a value, not an object—this discrepancy sometimes turns up when writing
Line 270: unit tests, see “Don’t Mock Values” (page 237).
Line 271: Refactor Interfaces Too
Line 272: Once we have interfaces for protocols, we can start to pay attention to similarities
Line 273: and differences. In a reasonably large codebase, we often start to ﬁnd interfaces
Line 274: that look similar. This means we should look at whether they represent a single
Line 275: concept and should be merged. Extracting common roles makes the design more
Line 276: 63
Line 277: Refactor Interfaces Too
Line 278: 
Line 279: --- 페이지 89 ---
Line 280: malleable because more components will be “plug-compatible,” so we can work
Line 281: at a higher level of abstraction. For the developer, there’s a secondary advantage
Line 282: that there will be fewer concepts that cost time to understand.
Line 283: Alternatively, if similar interfaces turn out to represent different concepts, we
Line 284: can make a point of making them distinct, so that the compiler can ensure that
Line 285: we only combine objects correctly. A decision to separate similar-looking inter-
Line 286: faces is a good time to reconsider their naming. It’s likely that there’s a more
Line 287: appropriate name for at least one of them.
Line 288: Finally, another time to consider refactoring interfaces is when we start imple-
Line 289: menting them. For example, if we ﬁnd that the structure of an implementing class
Line 290: is unclear, perhaps it has too many responsibilities which might be a hint that
Line 291: the interface is unfocused too and should be split up.
Line 292: Compose Objects to Describe System Behavior
Line 293: TDD at the unit level guides us to decompose our system into value types and
Line 294: loosely coupled computational objects. The tests give us a good understanding
Line 295: of how each object behaves and how it can be combined with others. We then
Line 296: use lower-level objects as the building blocks of more capable objects; this is the
Line 297: web of objects we described in Chapter 2.
Line 298: In jMock, for example, we assemble a description of the expected calls for a
Line 299: test in a context object called a Mockery. During a test run, the Mockery will pass
Line 300: calls made to any of its mocked objects to its Expectations, each of which will
Line 301: attempt to match the call. If an Expectation matches, that part of the test suc-
Line 302: ceeds. If none matches, then each Expectation reports its disagreement and the
Line 303: test fails. At runtime, the assembled objects look like Figure 7.1:
Line 304: Figure 7.1
Line 305: jMock Expectations are assembled from many objects
Line 306: The advantage of this approach is that we end up with a ﬂexible application
Line 307: structure built from relatively little code. It’s particularly suitable where the code
Line 308: has to support many related scenarios. For each scenario, we provide a different
Line 309: Chapter 7
Line 310: Achieving Object-Oriented Design
Line 311: 64
Line 312: 
Line 313: --- 페이지 90 ---
Line 314: assembly of components to build, in effect, a subsystem to plug into the rest of
Line 315: the application. Such designs are also easy to extend—just write a new plug-
Line 316: compatible component and add it in; you’ll see us write several new Hamcrest
Line 317: matchers in Part III.
Line 318: For example, to have jMock check that a method example.doSomething() is
Line 319: called exactly once with an argument of type String, we set up our test context
Line 320: like this:
Line 321: InvocationExpectation expectation = new InvocationExpectation();
Line 322: expectation.setParametersMatcher(
Line 323:   new AllParametersMatcher(Arrays.asList(new IsInstanceOf(String.class)));
Line 324: expectation.setCardinality(new Cardinality(1, 1));
Line 325: expectation.setMethodMatcher(new MethodNameMatcher("doSomething"));
Line 326: expectation.setObjectMatcher(new IsSame<Example>(example));
Line 327: context.addExpectation(expectation);
Line 328: Building Up to Higher-Level Programming
Line 329: You have probably spotted a difﬁculty with the code fragment above: it doesn’t
Line 330: explain very well what the expectation is testing. Conceptually, assembling a
Line 331: web of objects is straightforward. Unfortunately, the mainstream languages we
Line 332: usually work with bury the information we care about (objects and their relation-
Line 333: ships) in a morass of keywords, setters, punctuation, and the like. Just assigning
Line 334: and linking objects, as in this example, doesn’t help us understand the behavior
Line 335: of the system we’re assembling—it doesn’t express our intent.2
Line 336: Our response is to organize the code into two layers: an implementation layer
Line 337: which is the graph of objects, its behavior is the combined result of how its objects
Line 338: respond to events; and, a declarative layer which builds up the objects in the
Line 339: implementation layer, using small “sugar” methods and syntax to describe
Line 340: the purpose of each fragment. The declarative layer describes what the code will
Line 341: do, while the implementation layer describes how the code does it. The declarative
Line 342: layer is, in effect, a small domain-speciﬁc language embedded (in this case)
Line 343: in Java.3
Line 344: The different purposes of the two layers mean that we use a different coding
Line 345: style for each. For the implementation layer we stick to the conventional object-
Line 346: oriented style guidelines we described in the previous chapter. We’re more ﬂexible
Line 347: for the declarative layer—we might even use “train wreck” chaining of method
Line 348: calls or static methods to help get the point across.
Line 349: A good example is jMock itself. We can rewrite the example from the previous
Line 350: section as:
Line 351: 2. Nor does the common alternative of moving the object construction into a separate
Line 352: XML ﬁle.
Line 353: 3. This became clear to us when working on jMock. We wrote up our experiences in
Line 354: [Freeman06].
Line 355: 65
Line 356: Building Up to Higher-Level Programming
Line 357: 
Line 358: --- 페이지 91 ---
Line 359: context.checking(new Expectations() {{
Line 360:     oneOf(example).doSomething(with(any(String.class)));
Line 361: }});
Line 362: The Expectations object is a Builder [Gamma94] that constructs expectations.
Line 363: It deﬁnes “sugar” methods that construct the assembly of expectations and
Line 364: matchers and load it into the Mockery, as shown in Figure 7.2.
Line 365: Figure 7.2
Line 366: A syntax-layer constructs the interpreter
Line 367: Most of the time, such a declarative layer emerges from continual “merciless”
Line 368: refactoring. We start by writing code that directly composes objects and keep
Line 369: factoring out duplication. We also add helper methods to push the syntax noise
Line 370: out of the main body of the code and to add explanation. Taking care to notice
Line 371: when an area of code is not clear, we add or move structure until it is; this is
Line 372: very easy to do in a modern refactoring IDE. Eventually, we ﬁnd we have our
Line 373: two-layer structure. Occasionally, we start from the declarative code we’d like
Line 374: to have and work down to ﬁll in its implementation, as we do with the ﬁrst
Line 375: end-to-end test in Chapter 10.
Line 376: Our purpose, in the end, is to achieve more with less code. We aspire to raise
Line 377: ourselves from programming in terms of control ﬂow and data manipulation, to
Line 378: composing programs from smaller programs—where objects form the smallest
Line 379: unit of behavior. None of this is new—it’s the same concept as programming
Line 380: Unix by composing utilities with pipes [Kernighan76],4 or building up layers of
Line 381: language in Lisp [Graham93]—but we still don’t see it in the ﬁeld as often as we
Line 382: would like.
Line 383: 4. Kernighan and Plauger attribute the idea of pipes to Douglas McIlroy, who wrote a
Line 384: memo in 1964 suggesting the metaphor of data passing through a segmented garden
Line 385: hose. It’s currently available at http://plan9.bell-labs.com/who/dmr/mdmpipe.pdf.
Line 386: Chapter 7
Line 387: Achieving Object-Oriented Design
Line 388: 66
Line 389: 
Line 390: --- 페이지 92 ---
Line 391: And What about Classes?
Line 392: One last point. Unusually for a book on object-oriented software, we haven’t
Line 393: said much about classes and inheritance. It should be obvious by now that we’ve
Line 394: been pushing the application domain into the gaps between the objects, the
Line 395: communication protocols. We emphasize interfaces more than classes because
Line 396: that’s what other objects see: an object’s type is deﬁned by the roles it plays.
Line 397: We view classes for objects as an “implementation detail”—a way of imple-
Line 398: menting types, not the types themselves. We discover object class hierarchies by
Line 399: factoring out common behavior, but prefer to refactor to delegation if possible
Line 400: since we ﬁnd that it makes our code more ﬂexible and easier to understand.5
Line 401: Value types, on the other hand, are less likely to use delegation since they don’t
Line 402: have peers.
Line 403: There’s plenty of good advice on how to work with classes in, for example,
Line 404: [Fowler99], [Kerievsky04], and [Evans03].
Line 405: 5. The design forces, of course, are different in languages that support multiple
Line 406: inheritance well, such as Eiffel [Meyer91].
Line 407: 67
Line 408: And What about Classes?
Line 409: 
Line 410: --- 페이지 93 ---
Line 411: This page intentionally left blank 