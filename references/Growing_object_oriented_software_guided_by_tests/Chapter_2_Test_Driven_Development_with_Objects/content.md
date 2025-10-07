Line 1: 
Line 2: --- 페이지 38 ---
Line 3: Chapter 2
Line 4: Test-Driven Development with
Line 5: Objects
Line 6: Music is the space between the notes.
Line 7: —Claude Debussy
Line 8: A Web of Objects
Line 9: Object-oriented design focuses more on the communication between objects than
Line 10: on the objects themselves. As Alan Kay [Kay98] wrote:
Line 11: The big idea is “messaging” […] The key in making great and growable systems is
Line 12: much more to design how its modules communicate rather than what their internal
Line 13: properties and behaviors should be.
Line 14: An object communicates by messages: It receives messages from other objects
Line 15: and reacts by sending messages to other objects as well as, perhaps, returning a
Line 16: value or exception to the original sender. An object has a method of handling
Line 17: every type of message that it understands and, in most cases, encapsulates some
Line 18: internal state that it uses to coordinate its communication with other objects.
Line 19: An object-oriented system is a web of collaborating objects. A system is built
Line 20: by creating objects and plugging them together so that they can send messages
Line 21: to one another. The behavior of the system is an emergent property of the
Line 22: composition of the objects—the choice of objects and how they are connected
Line 23: (Figure 2.1).
Line 24: This lets us change the behavior of the system by changing the composition of
Line 25: its objects—adding and removing instances, plugging different combinations
Line 26: together—rather than writing procedural code. The code we write to manage
Line 27: this composition is a declarative deﬁnition of the how the web of objects will
Line 28: behave. It’s easier to change the system’s behavior because we can focus on what
Line 29: we want it to do, not how.
Line 30: Values and Objects
Line 31: When designing a system, it’s important to distinguish between values that
Line 32: model unchanging quantities or measurements, and objects that have an identity,
Line 33: might change state over time, and model computational processes. In the
Line 34: 13
Line 35: 
Line 36: --- 페이지 39 ---
Line 37: Figure 2.1
Line 38: A web of objects
Line 39: object-oriented languages that most of us use, the confusion is that both concepts
Line 40: are implemented by the same language construct: classes.
Line 41: Values are immutable instances that model ﬁxed quantities. They have no in-
Line 42: dividual identity, so two value instances are effectively the same if they have the
Line 43: same state. This means that it makes no sense to compare the identity of two
Line 44: values; doing so can cause some subtle bugs—think of the different ways of
Line 45: comparing two copies of new Integer(999). That’s why we’re taught to use
Line 46: string1.equals(string2) in Java rather than string1 == string2.
Line 47: Objects, on the other hand, use mutable state to model their behavior over
Line 48: time. Two objects of the same type have separate identities even if they have ex-
Line 49: actly the same state now, because their states can diverge if they receive different
Line 50: messages in the future.
Line 51: In practice, this means that we split our system into two “worlds”: values,
Line 52: which are treated functionally, and objects, which implement the stateful behavior
Line 53: of the system. In Part III, you’ll see how our coding style varies depending on
Line 54: which world we’re working in.
Line 55: In this book, we will use the term object to refer only to instances with identity,
Line 56: state, and processing—not values. There doesn’t appear to be another accepted
Line 57: term that isn’t overloaded with other meanings (such as entity and process).
Line 58: Follow the Messages
Line 59: We can beneﬁt from this high-level, declarative approach only if our objects are
Line 60: designed to be easily pluggable. In practice, this means that they follow common
Line 61: communication patterns and that the dependencies between them are made ex-
Line 62: plicit. A communication pattern is a set of rules that govern how a group of ob-
Line 63: jects talk to each other: the roles they play, what messages they can send and
Line 64: when, and so on. In languages like Java, we identify object roles with (abstract)
Line 65: interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
Line 66: everything we need to say.
Line 67: Chapter 2
Line 68: Test-Driven Development with Objects
Line 69: 14
Line 70: 
Line 71: --- 페이지 40 ---
Line 72: In our view, the domain model is in these communication patterns, because
Line 73: they are what gives meaning to the universe of possible relationships between
Line 74: the objects. Thinking of a system in terms of its dynamic, communication structure
Line 75: is a signiﬁcant mental shift from the static classiﬁcation that most of us learn
Line 76: when being introduced to objects. The domain model isn’t even obviously visible
Line 77: because the communication patterns are not explicitly represented in the program-
Line 78: ming languages we get to work with. We hope to show, in this book, how tests
Line 79: and mock objects help us see the communication between our objects more
Line 80: clearly.
Line 81: Here’s a small example of how focusing on the communication between objects
Line 82: guides design.
Line 83: In a video game, the objects in play might include: actors, such as the player
Line 84: and the enemies; scenery, which the player ﬂies over; obstacles, which the
Line 85: player can crash into; and effects, such as explosions and smoke. There are also
Line 86: scripts spawning objects behind the scenes as the game progresses.
Line 87: This is a good classiﬁcation of the game objects from the players’ point of view
Line 88: because it supports the decisions they need to make when playing the game—when
Line 89: interacting with the game from outside. This is not, however, a useful classiﬁcation
Line 90: for the implementers of the game. The game engine has to display objects that
Line 91: are visible, tell objects that are animated about the passing of time, detect colli-
Line 92: sions between objects that are physical, and delegate decisions about what to do
Line 93: when physical objects collide to collision resolvers.
Line 94: Figure 2.2
Line 95: Roles and objects in a video game
Line 96: As you can see in Figure 2.2, the two views, one from the game engine and
Line 97: one from the implementation of the in-play objects, are not the same. An Obstacle,
Line 98: for example, is Visible and Physical, while a Script is a Collision Resolver and
Line 99: Animated but not Visible. The objects in the game play different roles depending
Line 100: 15
Line 101: Follow the Messages
Line 102: 
Line 103: --- 페이지 41 ---
Line 104: on what the engine needs from them at the time. This mismatch between static
Line 105: classiﬁcation and dynamic communication means that we’re unlikely to come
Line 106: up with a tidy class hierarchy for the game objects that will also suit the needs
Line 107: of the engine.
Line 108: At best, a class hierarchy represents one dimension of an application, providing
Line 109: a mechanism for sharing implementation details between objects; for example,
Line 110: we might have a base class to implement the common features of frame-based
Line 111: animation. At worst, we’ve seen too many codebases (including our own) that
Line 112: suffer complexity and duplication from using one mechanism to represent multiple
Line 113: concepts.
Line 114: Roles, Responsibilities, Collaborators
Line 115: We try to think about objects in terms of roles, responsibilities, and collaborators,
Line 116: as best described by Wirfs-Brock and McKean in [Wirfs-Brock03]. An object is an
Line 117: implementation of one or more roles; a role is a set of related responsibilities;
Line 118: and a responsibility is an obligation to perform a task or know information. A
Line 119: collaboration is an interaction of objects or roles (or both).
Line 120: Sometimes we step away from the keyboard and use an informal design technique
Line 121: that Wirfs-Brock and McKean describe, called CRC cards (Candidates, Responsi-
Line 122: bilities, Collaborators). The idea is to use low-tech index cards to explore the po-
Line 123: tential object structure of an application, or a part of it. These index cards allow
Line 124: us to experiment with structure without getting stuck in detail or becoming too
Line 125: attached to an early solution.
Line 126: Figure 2.3
Line 127: CRC card for a video game
Line 128: Chapter 2
Line 129: Test-Driven Development with Objects
Line 130: 16
Line 131: 
Line 132: --- 페이지 42 ---
Line 133: Tell, Don’t Ask
Line 134: We have objects sending each other messages, so what do they say? Our experi-
Line 135: ence is that the calling object should describe what it wants in terms of the role
Line 136: that its neighbor plays, and let the called object decide how to make that happen.
Line 137: This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Line 138: Law of Demeter. Objects make their decisions based only on the information
Line 139: they hold internally or that which came with the triggering message; they avoid
Line 140: navigating to other objects to make things happen. Followed consistently, this
Line 141: style produces more ﬂexible code because it’s easy to swap objects that play the
Line 142: same role. The caller sees nothing of their internal structure or the structure of
Line 143: the rest of the system behind the role interface.
Line 144: When we don’t follow the style, we can end up with what’s known as “train
Line 145: wreck” code, where a series of getters is chained together like the carriages in a
Line 146: train. Here’s one case we found on the Internet:
Line 147: ((EditSaveCustomizer) master.getModelisable()
Line 148:   .getDockablePanel()
Line 149:     .getCustomizer())
Line 150:       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line 151: After some head scratching, we realized what this fragment was meant to say:
Line 152: master.allowSavingOfCustomisations();
Line 153: This wraps all that implementation detail up behind a single call. The client of
Line 154: master no longer needs to know anything about the types in the chain. We’ve
Line 155: reduced the risk that a design change might cause ripples in remote parts of the
Line 156: codebase.
Line 157: As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Line 158: Ask.” It forces us to make explicit and so name the interactions between objects,
Line 159: rather than leaving them implicit in the chain of getters. The shorter version
Line 160: above is much clearer about what it’s for, not just how it happens to be
Line 161: implemented.
Line 162: But Sometimes Ask
Line 163: Of course we don’t “tell” everything;1 we “ask” when getting information from
Line 164: values and collections, or when using a factory to create new objects. Occasion-
Line 165: ally, we also ask objects about their state when searching or ﬁltering, but we still
Line 166: want to maintain expressiveness and avoid “train wrecks.”
Line 167: For example (to continue with the metaphor), if we naively wanted to spread
Line 168: reserved seats out across the whole of a train, we might start with something like:
Line 169: 1. Although that’s an interesting exercise to try, to stretch your technique.
Line 170: 17
Line 171: But Sometimes Ask
Line 172: 
Line 173: --- 페이지 43 ---
Line 174: public class Train {
Line 175:   private final List<Carriage> carriages […]
Line 176:   private int percentReservedBarrier = 70;
Line 177:   public void reserveSeats(ReservationRequest request) {
Line 178:     for (Carriage carriage : carriages) {
Line 179:       if (carriage.getSeats().getPercentReserved() < percentReservedBarrier) {
Line 180:         request.reserveSeatsIn(carriage);
Line 181:         return;
Line 182:       }
Line 183:     }
Line 184:     request.cannotFindSeats();
Line 185:   }
Line 186: }
Line 187: We shouldn’t expose the internal structure of Carriage to implement this, not
Line 188: least because there may be different types of carriages within a train. Instead, we
Line 189: should ask the question we really want answered, instead of asking for the
Line 190: information to help us ﬁgure out the answer ourselves:
Line 191: public void reserveSeats(ReservationRequest request) {
Line 192:   for (Carriage carriage : carriages) {
Line 193:     if (carriage.hasSeatsAvailableWithin(percentReservedBarrier)) {
Line 194:       request.reserveSeatsIn(carriage);
Line 195:       return;
Line 196:     }
Line 197:   }
Line 198:   request.cannotFindSeats();
Line 199: } 
Line 200: Adding a query method moves the behavior to the most appropriate object,
Line 201: gives it an explanatory name, and makes it easier to test.
Line 202: We try to be sparing with queries on objects (as opposed to values) because
Line 203: they can allow information to “leak” out of the object, making the system a little
Line 204: bit more rigid. At a minimum, we make a point of writing queries that describe
Line 205: the intention of the calling object, not just the implementation.
Line 206: Unit-Testing the Collaborating Objects
Line 207: We appear to have painted ourselves into a corner. We’re insisting on focused
Line 208: objects that send commands to each other and don’t expose any way to query
Line 209: their state, so it looks like we have nothing available to assert in a unit test. For
Line 210: example, in Figure 2.4, the circled object will send messages to one or more of
Line 211: its three neighbors when invoked. How can we test that it does so correctly
Line 212: without exposing any of its internal state?
Line 213: One option is to replace the target object’s neighbors in a test with substitutes,
Line 214: or mock objects, as in Figure 2.5. We can specify how we expect the target object
Line 215: to communicate with its mock neighbors for a triggering event; we call these
Line 216: speciﬁcations expectations. During the test, the mock objects assert that they
Line 217: Chapter 2
Line 218: Test-Driven Development with Objects
Line 219: 18
Line 220: 
Line 221: --- 페이지 44 ---
Line 222: Figure 2.4
Line 223: Unit-testing an object in isolation
Line 224: Figure 2.5
Line 225: Testing an object with mock objects
Line 226: have been called as expected; they also implement any stubbed behavior needed
Line 227: to make the rest of the test work.
Line 228: With this infrastructure in place, we can change the way we approach TDD.
Line 229: Figure 2.5 implies that we’re just trying to test the target object and that we al-
Line 230: ready know what its neighbors look like. In practice, however, those collaborators
Line 231: don’t need to exist when we’re writing a unit test. We can use the test to help us
Line 232: tease out the supporting roles our object needs, deﬁned as Java interfaces, and
Line 233: ﬁll in real implementations as we develop the rest of the system. We call this in-
Line 234: terface discovery; you’ll see an example when we extract an AuctionEventListener
Line 235: in Chapter 12.
Line 236: Support for TDD with Mock Objects
Line 237: To support this style of test-driven programming, we need to create mock in-
Line 238: stances of the neighboring objects, deﬁne expectations on how they’re called and
Line 239: then check them, and implement any stub behavior we need to get through the
Line 240: test. In practice, the runtime structure of a test with mock objects usually looks
Line 241: like Figure 2.6.
Line 242: 19
Line 243: Support for TDD with Mock Objects
Line 244: 
Line 245: --- 페이지 45 ---
Line 246: Figure 2.6
Line 247: Testing an object with mock objects
Line 248: We use the term mockery2 for the object that holds the context of a test, creates
Line 249: mock objects, and manages expectations and stubbing for the test. We’ll show
Line 250: the practice throughout Part III, so we’ll just touch on the basics here. The
Line 251: essential structure of a test is:
Line 252: •
Line 253: Create any required mock objects.
Line 254: •
Line 255: Create any real objects, including the target object.
Line 256: •
Line 257: Specify how you expect the mock objects to be called by the target object.
Line 258: •
Line 259: Call the triggering method(s) on the target object.
Line 260: •
Line 261: Assert that any resulting values are valid and that all the expected calls have
Line 262: been made.
Line 263: The unit test makes explicit the relationship between the target object and its
Line 264: environment. It creates all the objects in the cluster and makes assertions about
Line 265: the interactions between the target object and its collaborators. We can code this
Line 266: infrastructure by hand or, these days, use one of the multiple mock object
Line 267: frameworks that are available in many languages. The important point, as we
Line 268: stress repeatedly throughout this book, is to make clear the intention of every
Line 269: test, distinguishing between the tested functionality, the supporting infrastructure,
Line 270: and the object structure.
Line 271: 2. This is a pun by Ivan Moore that we adopted in a ﬁt of whimsy.
Line 272: Chapter 2
Line 273: Test-Driven Development with Objects
Line 274: 20