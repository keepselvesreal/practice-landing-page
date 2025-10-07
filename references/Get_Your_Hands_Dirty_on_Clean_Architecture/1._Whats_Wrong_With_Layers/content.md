Line 1: 
Line 2: --- 페이지 10 ---
Line 3: 1. What’s Wrong With Layers?
Line 4: Chances are that you have developed a layered (web) application in the past. You might even be
Line 5: doing it in your current project right now (actually, I am).
Line 6: Thinking in layers has been drilled into us in computer science classes, tutorials and best practices.
Line 7: It has even been taught in books⁸.
Line 8: Figure 1 - A conventional web application architecture consists of a web layer, a domain layer, and a persistence layer.
Line 9: Figure 1 shows a high-level view of the very common three-layer architecture. We have a web layer
Line 10: that receives requests and routes them to a service in the domain or “business” layer. The service
Line 11: does some business magic and calls components from the persistence layer to query for or modify
Line 12: the current state of our domain entities.
Line 13: You know what? Layers are a solid architecture pattern! If we get them right, we’re able to build
Line 14: domain logic that is independent of the web and persistence layers. We can switch the web or
Line 15: persistence technologies without affecting our domain logic if we feel like it. We can add new
Line 16: features without affecting existing features.
Line 17: With a good layered architecture we’re keeping our options open and are able to quickly adapt
Line 18: to changing requirements and external factors. And if we believe Uncle Bob, this is exactly what
Line 19: architecture is all about⁹.
Line 20: So, what’s wrong with layers?
Line 21: In my experience a layered architecture has too many open flanks that allow bad habits to creep in
Line 22: and make the software increasingly harder to change over time. In the following sections, I’ll tell
Line 23: you why.
Line 24: ⁸Software Architecture Patterns by Mark Richards, O’Reilly, 2015
Line 25: ⁹Clean Architecture by Robert C. Martin, Prentice Hall, 2017, Chapter 15
Line 26: 
Line 27: --- 페이지 11 ---
Line 28: 1. What’s Wrong With Layers?
Line 29: 5
Line 30: It Promotes Database-Driven Design
Line 31: By its very definition, the foundation of a conventional layered architecture is the database.
Line 32: The web layer depends on the domain layer which in turn depends on the persistence layer and thus
Line 33: the database.
Line 34: Everything builds on top of the persistence layer. This is problematic due to several reasons.
Line 35: Let’s take a step back and think about what we’re trying to achieve with almost any application
Line 36: we’re building. We’re typically trying to create a model of the rules or “policies” that govern the
Line 37: business in order to make it easier for the users to interact with them.
Line 38: We’re primarily trying to model behavior, and not state. Yes, state is an important part of any
Line 39: application, but the behavior is what changes the state and thus drives the business!
Line 40: So why are we making the database the foundation of our architecture and not the domain logic?
Line 41: Think back to the last use cases you have implemented in any application. Have you started with
Line 42: implementing the domain logic or the persistence layer? Most likely, you have thought about what
Line 43: the database structure would look like and only then moved on to implementing the domain logic
Line 44: on top it.
Line 45: This makes sense in a conventional layered architecture, since we’re going with the natural flow
Line 46: of dependencies. But it makes absolutely no sense from a business point of view! We should build
Line 47: the domain logic before doing anything else! Only then can we find out if we have understood it
Line 48: correctly. And only once we know we’re building the right domain logic should we move on to build
Line 49: a persistence and web layer around it.
Line 50: A driving force in such a database-centric architecture is the use of object-relational mapping (ORM)
Line 51: frameworks. Don’t get me wrong, I love those frameworks and I’m working with JPA and Hibernate
Line 52: on a daily basis.
Line 53: But if we combine an ORM framework with a layered architecture, we’re easily tempted to mix
Line 54: business rules with persistence aspects.
Line 55: 
Line 56: --- 페이지 12 ---
Line 57: 1. What’s Wrong With Layers?
Line 58: 6
Line 59: Figure 2 - Using the database entities in the domain layer leads to strong coupling with the persistence layer.
Line 60: Usually, we have ORM-managed entities as part of the persistence layer as shown in figure 2. Since
Line 61: layers may access the layers below them, the domain layer is allowed to access those entities. And
Line 62: if it’s allowed to use them, they will be used.
Line 63: This creates a strong coupling between the persistence layer and the domain layer. Our services use
Line 64: the persistence model as their business model and not only have to deal with the domain logic, but
Line 65: also with eager vs. lazy loading, database transactions, flushing caches and similar housekeeping
Line 66: tasks.
Line 67: The persistence code is virtually fused into the domain code and thus it’s hard to change one without
Line 68: the other. That’s the opposite of being flexible and keeping options open, which should be the goal
Line 69: of our architecture.
Line 70: It’s Prone to Shortcuts
Line 71: In a conventional layered architecture, the only global rule is that from a certain layer, we can only
Line 72: access components in the same layer or a layer below.
Line 73: There may be other rules that a development team has agreed upon and some of them might even
Line 74: be enforced by tooling, but the layered architecture style itself does not impose those rules on us.
Line 75: So, if we need access to a certain component in a layer above ours, we can just push the component
Line 76: down a layer and we’re allowed to access it. Problem solved.
Line 77: Doing this once may be OK. But doing it once opens the door for doing it a second time. And if
Line 78: someone else was allowed to do it, so am I, right?
Line 79: I’m not saying that as developers, we take such shortcuts lightly. But if there is an option to do
Line 80: something, someone will do it, especially in combination with a looming deadline. And if something
Line 81: has been done before, the threshold for someone to do it again will lower drastically. This is a
Line 82: psychological effect called the “Broken Windows Theory” - more on this in chapter 11 “Taking
Line 83: Shortcuts Consciously”.
Line 84: 
Line 85: --- 페이지 13 ---
Line 86: 1. What’s Wrong With Layers?
Line 87: 7
Line 88: Figure 3 - Since we may access everything in the persistence layer, it tends to grow fat over time.
Line 89: Over years of development and maintenance of a software project, the persistence layer may very
Line 90: well end up like in figure 3.
Line 91: The persistence layer (or in more generic terms: the bottom-most layer) will grow fat as we push
Line 92: components down through the layers. Perfect candidates for this are helper or utility components
Line 93: since they don’t seem to belong to any specific layer.
Line 94: So, if we want to disable the “shortcut mode” for our architecture, layers are not the best option, at
Line 95: least not without enforcing some kind of additional architecture rules. And with “enforce” I don’t
Line 96: mean a senior developer doing code reviews but rules that make the build fail when they’re broken.
Line 97: It Grows Hard to Test
Line 98: A common evolution within a layered architecture is that layers are being skipped. We access the
Line 99: persistence layer directly from the web layer, since we’re only manipulating a single field of an
Line 100: entity and for that we need not bother the domain layer, right?
Line 101: 
Line 102: --- 페이지 14 ---
Line 103: 1. What’s Wrong With Layers?
Line 104: 8
Line 105: Figure 4 - Skipping the domain layer tends to scatter domain logic across the codebase.
Line 106: Again, this feels OK the first couple of times, but it has two drawbacks if it happens often (and it
Line 107: will, once someone has done the first step).
Line 108: First, we’re implementing domain logic in the web layer, even if it’s only manipulating a single field.
Line 109: What if the use case expands in the future? We’re most likely going to add more domain logic to the
Line 110: web layer, mixing responsibilities and spreading essential domain logic all over the application.
Line 111: Second, in the tests of our web layer, we not only have to mock away the domain layer, but also
Line 112: the persistence layer. This adds complexity to the unit test. And a complex test setup is the first step
Line 113: towards no tests at all because we don’t have time for them.
Line 114: As the web component grows over time, it may accumulate a lot of dependencies to different
Line 115: persistence components, adding to the test’s complexity. At some point, it takes more time for us to
Line 116: understand and mock away the dependencies than to actually write test code.
Line 117: It Hides the Use Cases
Line 118: As developers, we like to create new code that implements shiny new use cases. But we usually
Line 119: spend much more time changing existing code than we do creating new code. This is not only true
Line 120: for those dreaded legacy projects in which we’re working on a decades-old codebase but also for a
Line 121: hot new greenfield project after the initial use cases have been implemented.
Line 122: Since we’re so often searching for the right place to add or change functionality, our architecture
Line 123: should help us to quickly navigate the codebase. How is a layered architecture holding up in this
Line 124: regard?
Line 125: As already discussed above, in a layered architecture it easily happens that domain logic is scattered
Line 126: throughout the layers. It may exist in the web layer if we’re skipping the domain logic for an “easy”
Line 127: use case. And it may exist in the persistence layer if we have pushed a certain component down so
Line 128: 
Line 129: --- 페이지 15 ---
Line 130: 1. What’s Wrong With Layers?
Line 131: 9
Line 132: it can be accessed from both the domain and the persistence layer. This already makes finding the
Line 133: right spot to add new functionality hard.
Line 134: But there’s more. A layered architecture does not impose rules on the “width” of domain services.
Line 135: Over time, this often leads to very broad services that serve multiple use cases (see figure 5).
Line 136: Figure 5 - “Broad” services make it hard to find a certain use case within the codebase.
Line 137: A broad service has many dependencies to the persistence layer and many components in the web
Line 138: layer depend on it. This not only makes the service hard to test, but also makes it hard for us to find
Line 139: the service responsible for the use case we want to work on.
Line 140: How much easier would it be if we had highly-specialized narrow domain services that each serve a
Line 141: single use case? Instead of searching for the user registration use case in the UserService, we would
Line 142: just open up the RegisterUserService and start working.
Line 143: It Makes Parallel Work Difficult
Line 144: Management usually expects us to be done with building the software they sponsor at a certain date.
Line 145: Actually, they even expect us to be done within a certain budget as well, but let’s not complicate
Line 146: things here.
Line 147: Aside from the fact that I have never seen “done” software in my career as a software developer, to
Line 148: be done by a certain date usually implies that we have to work in parallel.
Line 149: Probably you know this famous conclusion from “The Mythical Man-Month”, even if you haven’t
Line 150: read the book:
Line 151: Adding manpower to a late software project makes it later¹⁰
Line 152: ¹⁰The Mythical Man-Month: Essays on Software Engineering by Frederick P. Brooks, Jr., Addison-Wesley, 1995
Line 153: 
Line 154: --- 페이지 16 ---
Line 155: 1. What’s Wrong With Layers?
Line 156: 10
Line 157: This also holds true, to a degree, to software projects that are not (yet) late. You cannot expect a
Line 158: large group of 50 developers to be 5 times as fast as a smaller team of 10 developers in every context.
Line 159: If they’re working on a very large application where they can split up in sub teams and work on
Line 160: separate parts of the software, it may work, but in most contexts they would stand on each other’s
Line 161: feet.
Line 162: But at a healthy scale, we can certainly expect to be faster with more people on the project. And
Line 163: management is right to expect that of us.
Line 164: To meet this expectation, our architecture must support parallel work. This is not easy. And a layered
Line 165: architecture doesn’t really help us here.
Line 166: Imagine we’re adding a new use case to our application. We have three developers available. One
Line 167: can add the needed features to the web layer, one to the domain layer and the third to the persistence
Line 168: layer, right?
Line 169: Well, it usually doesn’t work that way in a layered architecture. Since everything builds on top of
Line 170: the persistence layer, the persistence layer must be developed first. Then comes the domain layer
Line 171: and finally the web layer. So only one developer can work on the feature at the same time!
Line 172: Ah, but the developers can define interfaces first, you say, and then each developer can work against
Line 173: these interfaces without having to wait for the actual implementation. Sure, this is possible, but only
Line 174: if we’re not doing Database-Driven Design as discussed above, where our persistence logic is so
Line 175: mixed up with our domain logic that we just cannot work on each aspect separately.
Line 176: If we have broad services in our codebase, it may even be hard to work on different features in
Line 177: parallel. Working on different use cases will cause the same service to be edited in parallel which
Line 178: leads to merge conflicts and potentially regressions.
Line 179: How Does This Help Me Build Maintainable Software?
Line 180: If you have built layered architectures in the past, you can probably relate to some of the
Line 181: disadvantages discussed in this chapter, and you could maybe even add some more.
Line 182: If done correctly, and if some additional rules are imposed on it, a layered architecture can be very
Line 183: maintainable and make changing or adding to the codebase a breeze.
Line 184: However, the discussion shows that a layered architecture allows many things to go wrong. Without
Line 185: a very strict self discipline it’s prone to degrade and become less maintainable over time. And this
Line 186: self discipline usually becomes a little less strict each time a manager draws a new deadline around
Line 187: the development team.
Line 188: Keeping the traps of a layered architecture in mind will help us the next time we argue against taking
Line 189: a shortcut and for building a more maintainable solution instead - be it in a layered architecture or
Line 190: a different architecture style.