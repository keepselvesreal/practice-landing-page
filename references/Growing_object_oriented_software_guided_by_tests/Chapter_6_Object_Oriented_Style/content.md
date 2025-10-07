Line 1: 
Line 2: --- 페이지 72 ---
Line 3: Chapter 6
Line 4: Object-Oriented Style
Line 5: Always design a thing by considering it in its next larger
Line 6: context—a chair in a room, a room in a house, a house in an
Line 7: environment, an environment in a city plan.
Line 8: —Eliel Saarinen
Line 9: Introduction
Line 10: So far in Part II, we’ve talked about how to get started with the development
Line 11: process and how to keep going. Now we want to take a more detailed look at
Line 12: our design goals and our use of TDD, and in particular mock objects, to guide
Line 13: the structure of our code.
Line 14: We value code that is easy to maintain over code that is easy to write.1 Imple-
Line 15: menting a feature in the most direct way can damage the maintainability of the
Line 16: system, for example by making the code difﬁcult to understand or by introducing
Line 17: hidden dependencies between components. Balancing immediate and longer-term
Line 18: concerns is often tricky, but we’ve seen too many teams that can no longer deliver
Line 19: because their system is too brittle.
Line 20: In this chapter, we want to show something of what we’re trying to achieve
Line 21: when we design software, and how that looks in an object-oriented language;
Line 22: this is the “opinionated” part of our approach to software. In the next chapter,
Line 23: we’ll look at the mechanics of how to guide code in this direction with TDD.
Line 24: Designing for Maintainability
Line 25: Following the process we described in Chapter 5, we grow our systems a slice of
Line 26: functionality at a time. As the code scales up, the only way we can continue to
Line 27: understand and maintain it is by structuring the functionality into objects, objects
Line 28: into packages,2 packages into programs, and programs into systems. We use two
Line 29: principal heuristics to guide this structuring:
Line 30: 1. As the Agile Manifesto might have put it.
Line 31: 2. We’re being vague about the meaning of “package” here since we want it to include
Line 32: concepts such as modules, libraries, and namespaces, which tend to be confounded
Line 33: in the Java world—but you know what we mean.
Line 34: 47
Line 35: 
Line 36: --- 페이지 73 ---
Line 37: Separation of concerns
Line 38: When we have to change the behavior of a system, we want to change as
Line 39: little code as possible. If all the relevant changes are in one area of code, we
Line 40: don’t have to hunt around the system to get the job done. Because we cannot
Line 41: predict when we will have to change any particular part of the system, we
Line 42: gather together code that will change for the same reason. For example, code
Line 43: to unpack messages from an Internet standard protocol will not change for
Line 44: the same reasons as business code that interprets those messages, so we
Line 45: partition the two concepts into different packages.
Line 46: Higher levels of abstraction
Line 47: The only way for humans to deal with complexity is to avoid it, by working
Line 48: at higher levels of abstraction. We can get more done if we program by
Line 49: combining components of useful functionality rather than manipulating
Line 50: variables and control ﬂow; that’s why most people order food from a menu
Line 51: in terms of dishes, rather than detail the recipes used to create them.
Line 52: Applied consistently, these two forces will push the structure of an appli-
Line 53: cation towards something like Cockburn’s “ports and adapters” architecture
Line 54: [Cockburn08], in which the code for the business domain is isolated from its
Line 55: dependencies on technical infrastructure, such as databases and user interfaces.
Line 56: We don’t want technical concepts to leak into the application model, so we write
Line 57: interfaces to describe its relationships with the outside world in its terminology
Line 58: (Cockburn’s ports). Then we write bridges between the application core and each
Line 59: technical domain (Cockburn’s adapters). This is related to what Eric Evans calls
Line 60: an “anticorruption layer” [Evans03].
Line 61: The bridges implement the interfaces deﬁned by the application model and
Line 62: map between application-level and technical-level objects (Figure 6.1). For exam-
Line 63: ple, a bridge might map an order book object to SQL statements so that orders
Line 64: are persisted in a database. To do so, it might query values from the application
Line 65: object or use an object-relational tool like Hibernate3 to pull values out of objects
Line 66: using Java reﬂection. We’ll show an example of refactoring to this architecture
Line 67: in Chapter 17.
Line 68: The next question is how to ﬁnd the facets in the behavior where the interfaces
Line 69: should be, so that we can divide up the code cleanly. We have some second-level
Line 70: heuristics to help us think about that.
Line 71: 3. http://www.hibernate.org
Line 72: Chapter 6
Line 73: Object-Oriented Style
Line 74: 48
Line 75: 
Line 76: --- 페이지 74 ---
Line 77: Figure 6.1
Line 78: An application’s core domain model is mapped onto
Line 79: technical infrastructure
Line 80: Encapsulation and Information Hiding
Line 81: We want to be careful with the distinction between “encapsulation” and “information
Line 82: hiding.” The terms are often used interchangeably but actually refer to two separate,
Line 83: and largely orthogonal, qualities:
Line 84: Encapsulation
Line 85: Ensures that the behavior of an object can only be affected through its API.
Line 86: It lets us control how much a change to one object will impact other parts of
Line 87: the system by ensuring that there are no unexpected dependencies between
Line 88: unrelated components.
Line 89: Information hiding
Line 90: Conceals how an object implements its functionality behind the abstraction
Line 91: of its API. It lets us work with higher abstractions by ignoring lower-level details
Line 92: that are unrelated to the task at hand.
Line 93: We’re most aware of encapsulation when we haven’t got it. When working with
Line 94: badly encapsulated code, we spend too much time tracing what the potential
Line 95: effects of a change might be, looking at where objects are created, what common
Line 96: data they hold, and where their contents are referenced. The topic has inspired
Line 97: two books that we know of, [Feathers04] and [Demeyer03].
Line 98: 49
Line 99: Designing for Maintainability
Line 100: 
Line 101: --- 페이지 75 ---
Line 102: Many object-oriented languages support encapsulation by providing control over
Line 103: the visibility of an object’s features to other objects, but that’s not enough. Objects
Line 104: can break encapsulation by sharing references to mutable objects, an effect known
Line 105: as aliasing. Aliasing is essential for conventional object- oriented systems (other-
Line 106: wise no two objects would be able to communicate), but accidental aliasing can
Line 107: couple unrelated parts of a system so it behaves mysteriously and is inﬂexible to
Line 108: change.
Line 109: We follow standard practices to maintain encapsulation when coding: deﬁne
Line 110: immutable value types, avoid global variables and singletons, copy collections
Line 111: and mutable values when passing them between objects, and so on. We have
Line 112: more about information hiding later in this chapter.
Line 113: Internals vs. Peers
Line 114: As we organize our system, we must decide what is inside and outside each object,
Line 115: so that the object provides a coherent abstraction with a clear API. Much of the
Line 116: point of an object, as we discussed above, is to encapsulate access to its internals
Line 117: through its API and to hide these details from the rest of the system. An object
Line 118: communicates with other objects in the system by sending and receiving messages,
Line 119: as in Figure 6.2; the objects it communicates with directly are its peers.
Line 120: Figure 6.2
Line 121: Objects communicate by sending and receiving messages
Line 122: This decision matters because it affects how easy an object is to use, and so
Line 123: contributes to the internal quality of the system. If we expose too much of an
Line 124: object’s internals through its API, its clients will end up doing some of its work.
Line 125: We’ll have distributed behavior across too many objects (they’ll be coupled to-
Line 126: gether), increasing the cost of maintenance because any changes will now ripple
Line 127: across the code. This is the effect of the “train wreck” example on page 17:
Line 128: Chapter 6
Line 129: Object-Oriented Style
Line 130: 50
Line 131: 
Line 132: --- 페이지 76 ---
Line 133: ((EditSaveCustomizer) master.getModelisable()
Line 134:   .getDockablePanel()
Line 135:     .getCustomizer())
Line 136:       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line 137: Every getter in this example exposes a structural detail. If we wanted to change,
Line 138: say, the way customizations on the master are enabled, we’d have to change all
Line 139: the intermediate relationships.
Line 140: Different Levels of Language
Line 141: As you’ll see in Part III, we often write helper methods to make code more readable.
Line 142: We’re not afraid of adding very small methods if they clarify the meaning of the
Line 143: feature they represent. We name these methods to make the calling code read
Line 144: as naturally as possible; we don’t have to conform to external conventions since
Line 145: these methods are only there to support other code. For example, in Chapter 15
Line 146: we have a line in a test that reads:
Line 147: allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
Line 148: We’ll explain what this means at the time. What’s relevant here is that
Line 149: aSniperThatIs() is a local method that constructs a value to be passed to the
Line 150: with() method, and that its name is intended to describe its intent in this context.
Line 151: In effect, we’re constructing a very small embedded language that deﬁnes, in this
Line 152: case, a part of a test.
Line 153: As well as distinguishing between value and object types (page 13), we ﬁnd that
Line 154: we tend towards different programming styles at different levels in the code.
Line 155: Loosely speaking, we use the message-passing style we’ve just described between
Line 156: objects, but we tend to use a more functional style within an object, building up
Line 157: behavior from methods and values that have no side effects.
Line 158: Features without side effects mean that we can assemble our code from smaller
Line 159: components, minimizing the amount of risky shared state. Writing large-scale
Line 160: functional programs is a topic for a different book, but we ﬁnd that a little
Line 161: immutability within the implementation of a class leads to much safer code and
Line 162: that, if we do a good job, the code reads well too.
Line 163: So how do we choose the right features for an object?
Line 164: No And’s, Or’s, or But’s
Line 165: Every object should have a single, clearly deﬁned responsibility; this is the “single
Line 166: responsibility” principle [Martin02]. When we’re adding behavior to a system,
Line 167: this principle helps us decide whether to extend an existing object or create a
Line 168: new service for an object to call.
Line 169: 51
Line 170: No And’s, Or’s, or But’s
Line 171: 
Line 172: --- 페이지 77 ---
Line 173: Our heuristic is that we should be able to describe what an object does without
Line 174: using any conjunctions (“and,” “or”). If we ﬁnd ourselves adding clauses to the
Line 175: description, then the object probably should be broken up into collaborating
Line 176: objects, usually one for each clause.
Line 177: This principle also applies when we’re combining objects into new abstractions.
Line 178: If we’re packaging up behavior implemented across several objects into a single
Line 179: construct, we should be able to describe its responsibility clearly; there are some
Line 180: related ideas below in the “Composite Simpler Than the Sum of Its Parts” and
Line 181: “Context Independence” sections.
Line 182: Object Peer Stereotypes
Line 183: We have objects with single responsibilities, communicating with their peers
Line 184: through messages in clean APIs, but what do they say to each other?
Line 185: We categorize an object’s peers (loosely) into three types of relationship. An
Line 186: object might have:
Line 187: Dependencies
Line 188: Services that the object requires from its peers so it can perform its responsi-
Line 189: bilities. The object cannot function without these services. It should not be
Line 190: possible to create the object without them. For example, a graphics package
Line 191: will need something like a screen or canvas to draw on—it doesn’t make
Line 192: sense without one.
Line 193: Notiﬁcations
Line 194: Peers that need to be kept up to date with the object’s activity. The object
Line 195: will notify interested peers whenever it changes state or performs a signiﬁcant
Line 196: action. Notiﬁcations are “ﬁre and forget”; the object neither knows nor cares
Line 197: which peers are listening. Notiﬁcations are so useful because they decouple
Line 198: objects from each other. For example, in a user interface system, a button
Line 199: component promises to notify any registered listeners when it’s clicked, but
Line 200: does not know what those listeners will do. Similarly, the listeners expect to
Line 201: be called but know nothing of the way the user interface dispatches its events.
Line 202: Adjustments
Line 203: Peers that adjust the object’s behavior to the wider needs of the system. This
Line 204: includes policy objects that make decisions on the object’s behalf (the Strat-
Line 205: egy pattern in [Gamma94]) and component parts of the object if it’s a com-
Line 206: posite. For example, a Swing JTable will ask a TableCellRenderer to draw
Line 207: a cell’s value, perhaps as RGB (Red, Green, Blue) values for a color. If we
Line 208: change the renderer, the table will change its presentation, now displaying
Line 209: the HSB (Hue, Saturation, Brightness) values.
Line 210: Chapter 6
Line 211: Object-Oriented Style
Line 212: 52
Line 213: 
Line 214: --- 페이지 78 ---
Line 215: These stereotypes are only heuristics to help us think about the design, not
Line 216: hard rules, so we don’t obsess about ﬁnding just the right classiﬁcation of an
Line 217: object’s peers. What matters most is the context in which the collaborating objects
Line 218: are used. For example, in one application an auditing log could be a dependency,
Line 219: because auditing is a legal requirement for the business and no object should be
Line 220: created without an audit trail. Elsewhere, it could be a notiﬁcation, because
Line 221: auditing is a user choice and objects will function perfectly well without it.
Line 222: Another way to look at it is that notiﬁcations are one-way: A notiﬁcation lis-
Line 223: tener may not return a value, call back the caller, or throw an exception, since
Line 224: there may be other listeners further down the chain. A dependency or adjustment,
Line 225: on the other hand, may do any of these, since there’s a direct relationship.
Line 226: “New or new not. There is no try.”4
Line 227: We try to make sure that we always create a valid object. For dependencies, this
Line 228: means that we pass them in through the constructor. They’re required, so there’s
Line 229: no point in creating an instance of an object until its dependencies are available,
Line 230: and using the constructor enforces this constraint in the object’s deﬁnition.
Line 231: Partially creating an object and then ﬁnishing it off by setting properties is brittle
Line 232: because the programmer has to remember to set all the dependencies.When the
Line 233: object changes to add new dependencies, the existing client code will still compile
Line 234: even though it no longer constructs a valid instance. At best this will cause a
Line 235: NullPointerException, at worst it will fail misleadingly.
Line 236: Notiﬁcations and adjustments can be passed to the constructor as a convenience.
Line 237: Alternatively, they can be initialized to safe defaults and overwritten later (note
Line 238: that there is no safe default for a dependency). Adjustments can be initialized to
Line 239: common values, and notiﬁcations to a null object [Woolf98] or an empty collection.
Line 240: We then add methods to allow callers to change these default values, and add or
Line 241: remove listeners.
Line 242: Composite Simpler Than the Sum of Its Parts
Line 243: All objects in a system, except for primitive types built into the language, are
Line 244: composed of other objects. When composing objects into a new type, we want
Line 245: the new type to exhibit simpler behavior than all of its component parts considered
Line 246: together. The composite object’s API must hide the existence of its component
Line 247: parts and the interactions between them, and expose a simpler abstraction to its
Line 248: peers. Think of a mechanical clock: It has two or three hands for output and one
Line 249: pull-out wheel for input but packages up dozens of moving parts.
Line 250: 4. Attributed to Yoda.
Line 251: 53
Line 252: Composite Simpler Than the Sum of Its Parts
Line 253: 
Line 254: --- 페이지 79 ---
Line 255: In software, a user interface component for editing money values might have
Line 256: two subcomponents: one for the amount and one for the currency. For the
Line 257: component to be useful, its API should manage both values together, otherwise
Line 258: the client code could just control it subcomponents directly.
Line 259: moneyEditor.getAmountField().setText(String.valueOf(money.amount());
Line 260: moneyEditor.getCurrencyField().setText(money.currencyCode());
Line 261: The “Tell, Don’t Ask” convention can start to hide an object’s structure from
Line 262: its clients but is not a strong enough rule by itself. For example, we could replace
Line 263: the getters in the ﬁrst version with setters:
Line 264: moneyEditor.setAmountField(money.amount());
Line 265: moneyEditor.setCurrencyField(money.currencyCode());
Line 266: This still exposes the internal structure of the component, which its client still
Line 267: has to manage explicitly.
Line 268: We can make the API much simpler by hiding within the component everything
Line 269: about the way money values are displayed and edited, which in turn simpliﬁes
Line 270: the client code:
Line 271: moneyEditor.setValue(money);
Line 272: This suggests a rule of thumb:
Line 273: Composite Simpler Than the Sum of Its Parts
Line 274: The API of a composite object should not be more complicated than that of any of
Line 275: its components.
Line 276: Composite objects can, of course, be used as components in larger-scale, more
Line 277: sophisticated composite objects. As we grow the code, the “composite simpler
Line 278: than the sum of its parts” rule contributes to raising the level of abstraction.
Line 279: Context Independence
Line 280: While the “composite simpler than the sum of its parts” rule helps us decide
Line 281: whether an object hides enough information, the “context independence” rule
Line 282: helps us decide whether an object hides too much or hides the wrong information.
Line 283: A system is easier to change if its objects are context-independent; that is, if
Line 284: each object has no built-in knowledge about the system in which it executes. This
Line 285: allows us to take units of behavior (objects) and apply them in new situations.
Line 286: To be context-independent, whatever an object needs to know about the larger
Line 287: environment it’s running in must be passed in. Those relationships might be
Line 288: Chapter 6
Line 289: Object-Oriented Style
Line 290: 54
Line 291: 
Line 292: --- 페이지 80 ---
Line 293: “permanent” (passed in on construction) or “transient” (passed in to the method
Line 294: that needs them).
Line 295: In this “paternalistic” approach, each object is told just enough to do its job
Line 296: and wrapped up in an abstraction that matches its vocabulary. Eventually, the
Line 297: chain of objects reaches a process boundary, which is where the system will ﬁnd
Line 298: external details such as host names, ports, and user interface events.
Line 299: One Domain Vocabulary
Line 300: A class that uses terms from multiple domains might be violating context
Line 301: independence, unless it’s part of a bridging layer.
Line 302: The effect of the “context independence” rule on a system of objects is to make
Line 303: their relationships explicit, deﬁned separately from the objects themselves. First,
Line 304: this simpliﬁes the objects, since they don’t need to manage their own relationships.
Line 305: Second, this simpliﬁes managing the relationships, since objects at the same
Line 306: scale are often created and composed together in the same places, usually in
Line 307: mapping-layer factory objects.
Line 308: Context independence guides us towards coherent objects that can be applied
Line 309: in different contexts, and towards systems that we can change by reconﬁguring
Line 310: how their objects are composed.
Line 311: Hiding the Right Information
Line 312: Encapsulation is almost always a good thing to do, but sometimes information
Line 313: can be hidden in the wrong place. This makes the code difﬁcult to understand,
Line 314: to integrate, or to build behavior from by composing objects. The best defense
Line 315: is to be clear about the difference between the two concepts when discussing a
Line 316: design. For example, we might say:
Line 317: •
Line 318: “Encapsulate the data structure for the cache in the CachingAuctionLoader
Line 319: class.”
Line 320: •
Line 321: “Encapsulate the name of the application’s log ﬁle in the PricingPolicy
Line 322: class.”
Line 323: These sound reasonable until we recast them in terms of information hiding:
Line 324: •
Line 325: “Hide the data structure used for the cache in the CachingAuctionLoader
Line 326: class.”
Line 327: •
Line 328: “Hide the name of the application’s log ﬁle in the PricingPolicy class.”
Line 329: 55
Line 330: Hiding the Right Information
Line 331: 
Line 332: --- 페이지 81 ---
Line 333: Context independence tells us that we have no business hiding details of the
Line 334: log ﬁle in the PricingPolicy class—they’re concepts from different levels in
Line 335: the “Russian doll” structure of nested domains. If the log ﬁle name is necessary,
Line 336: it should be packaged up and passed in from a level that understands external
Line 337: conﬁguration.
Line 338: An Opinionated View
Line 339: We’ve taken the time to describe what we think of as “good” object-oriented
Line 340: design because it underlies our approach to development and we ﬁnd that it helps
Line 341: us write code that we can easily grow and adapt to meet the changing needs of
Line 342: its users. Now we want to show how our approach to test-driven development
Line 343: supports these principles.
Line 344: Chapter 6
Line 345: Object-Oriented Style
Line 346: 56