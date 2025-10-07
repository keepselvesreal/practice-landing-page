Line 1: 
Line 2: --- 페이지 17 ---
Line 3: 2. Inverting Dependencies
Line 4: After the rant about layered architecture in the previous chapter, you’re right to expect this chapter
Line 5: to discuss an alternative approach. We’ll start by discussing two of the SOLID¹¹ principles and then
Line 6: apply them to create a “Clean” or “Hexagonal” architecture that addresses the problems of a layered
Line 7: architecture.
Line 8: The Single Responsibility Principle
Line 9: Everyone in software development probably knows the Single Responsibility Principle (SRP) or at
Line 10: least assumes to know it.
Line 11: A common interpretation of this principle is this:
Line 12: A component should do only one thing, and do it right.
Line 13: That’s good advice, but not the actual intent of the SRP.
Line 14: “Doing only one thing” is actually the most obvious interpretation of a single responsibility, so it’s
Line 15: no wonder that the SRP is frequently interpreted like this. Let’s just observe that the name of the
Line 16: SRP is misleading.
Line 17: Here’s the actual definition of the SRP:
Line 18: A component should have only one reason to change.
Line 19: As we see, “responsibility” should actually be translated to “reason to change” instead of “do only
Line 20: one thing”. Perhaps we should rename the SRP to “Single Reason to Change Principle”.
Line 21: If a component has only one reason to change, it might end up doing only one thing, but the more
Line 22: important part is that it has only this one reason to change.
Line 23: What does that mean for our architecture?
Line 24: If a component has only one reason to change, we don’t have to worry about this component at all
Line 25: if we change the software for any other reason, because we know that it will still work as expected.
Line 26: Sadly, it’s very easy for a reason to change to propagate through code via the dependencies of a
Line 27: component to other components (see figure 6).
Line 28: ¹¹Single Responsibility Principle, Open-Closed Principle, Liskov Substitution Principle, Interface Segregation Principle, Dependency
Line 29: Inversion Principle. You can read more about these Principles in Clean Architecture by Robert C. Martin or on Wikipedia.
Line 30: 
Line 31: --- 페이지 18 ---
Line 32: 2. Inverting Dependencies
Line 33: 12
Line 34: Figure 6 - Each dependency of a component is a possible reason to change this component, even if it is only a transitive
Line 35: dependency (dashed arrows).
Line 36: In the figure above, component A depends on many other components (either directly or transitively)
Line 37: while component E has no dependencies at all.
Line 38: The only reason to change component E is when the functionality of E must change due to some
Line 39: new requirement. Component A, however, possibly might have to change when any of the other
Line 40: components change, because it depends on them.
Line 41: Many codebases grow harder - and thus more expensive - to change over time because the SRP is
Line 42: violated. Over time, components collect more and more reasons to change. After having collected
Line 43: many reasons to change, changing one component might cause another component to fail.
Line 44: A Tale about Side Effects
Line 45: I once was part of a project where my team inherited a ten-year-old codebase built by another
Line 46: software shop. The client had decided to replace the development team to make maintenance and
Line 47: development better and less expensive in the future.
Line 48: As was to be expected, it was not easy to gain an understanding of what the code actually did, and
Line 49: changes we did in one area of the codebase often had side effects in other areas. But we managed -
Line 50: by testing exhaustively, adding automated tests and refactoring a lot.
Line 51: After some time of successfully maintaining and extending the codebase, the client requested a new
Line 52: feature to be implemented in a way that struck me as very awkward for the users of the software.
Line 53: So I proposed to do it in a more user-friendly way that was even less expensive to implement since
Line 54: it needed fewer overall changes. It needed a small change in a certain very central component,
Line 55: however.
Line 56: The client declined and ordered the more awkward and expensive solution. When I asked for the
Line 57: reason, they said that they were afraid of side effects because changes in that one component by the
Line 58: previous development team have always broken something else in the past.
Line 59: Sadly, this is an example of how you can train your client to pay extra for modifying badly
Line 60: architected software. Luckily, most clients will not play along with this game, so let’s try to build
Line 61: good software instead.
Line 62: 
Line 63: --- 페이지 19 ---
Line 64: 2. Inverting Dependencies
Line 65: 13
Line 66: The Dependency Inversion Principle
Line 67: In our layered architecture, the cross-layer dependencies always point downward to the next layer.
Line 68: When we apply the Single Responsibility Principle on a high level, we notice that the upper layers
Line 69: have more reasons to change than the lower layers.
Line 70: Thus, due to the domain layer’s dependency to the persistence layer, each change in the persistence
Line 71: layer potentially requires a change in the domain layer. But the domain code is the most important
Line 72: code in our application! We don’t want to have to change it when something changes in the
Line 73: persistence code!
Line 74: So, how can we get rid of this dependency?
Line 75: The Dependency Inversion Principle provides the answer.
Line 76: In contrast to the SRP, the Dependency Inversion Principle (DIP) means what the name suggests:
Line 77: We can turn around (invert) the direction of any dependency within our codebase¹²
Line 78: How does that work? Let’s try to invert the dependency between our domain and persistence code
Line 79: so that the persistence code depends on the domain code, reducing the number of reasons to change
Line 80: for the domain code.
Line 81: We start with a structure like in figure 2 from chapter 1 “What’s Wrong with Layers?”. We have a
Line 82: service in the domain layer that works with entities and repositories from the persistence layer.
Line 83: First of all, we want to pull up the entities into the domain layer because they represent our domain
Line 84: objects and our domain code pretty much revolves around changing state in those entities.
Line 85: But now, we’d have a circular dependency between both layers since the repository from the
Line 86: persistence layer depends on the entity, which is now in the domain layer. This is where we apply
Line 87: the DIP. We create an interface for the repository in the domain layer and let the actual repository
Line 88: in the persistence layer implement it. The result is something like in figure 7.
Line 89: ¹²Actually, we can only invert dependencies when we have control over the code on both sides of the dependency. If we have a dependency
Line 90: to a third-party library, we cannot invert it, since we don’t control the code of that library.
Line 91: 
Line 92: --- 페이지 20 ---
Line 93: 2. Inverting Dependencies
Line 94: 14
Line 95: Figure 7 - By introducing an interface in the domain layer, we can invert the dependency so that the persistence layer
Line 96: depends on the domain layer.
Line 97: With this trick, we have liberated our domain logic from the oppressive dependency to the
Line 98: persistence code. This is a core feature of the two architecture styles we’re going to discuss in the
Line 99: upcoming sections.
Line 100: Clean Architecture
Line 101: Robert C. Martin cemented the term “Clean Architecture” in his book with the same name¹³. In
Line 102: a clean architecture, in his opinion, the business rules are testable by design and independent of
Line 103: frameworks, databases, UI technologies and other external applications or interfaces.
Line 104: That means that the domain code must not have any outward facing dependencies. Instead, with
Line 105: the help of the Dependency Inversion Principle, all dependencies point toward the domain code.
Line 106: Figure 8 shows how such an architecture might look on an abstract level.
Line 107: ¹³Clean Architecture by Robert C. Martin, Prentice Hall, 2017, Chapter 22
Line 108: 
Line 109: --- 페이지 21 ---
Line 110: 2. Inverting Dependencies
Line 111: 15
Line 112: Figure 8 - In a Clean Architecture, all dependencies point inward toward the domain logic. Source: Clean Architecture
Line 113: by Robert C. Martin.
Line 114: The layers in this architecture are wrapped around each other in concentric circles. The main rule
Line 115: in such an architecture is the Dependency Rule, which states that all dependencies between those
Line 116: layers must point inward.
Line 117: The core of the architecture contains the domain entities which are accessed by the surrounding use
Line 118: cases. The use cases are what we have called services earlier, but are more fine-grained to have a
Line 119: single responsibility (i.e. a single reason to change), thus avoiding the problem of broad services we
Line 120: have discussed earlier.
Line 121: Around this core we can find all the other components of our application that support the business
Line 122: rules. This support can mean providing persistence or providing a user interface, for example. Also,
Line 123: the outer layers may provide adapters to any other third-party component.
Line 124: Since the domain code knows nothing about which persistence or UI framework is used, it cannot
Line 125: contain any code specific to those frameworks and will concentrate on the business rules. We have all
Line 126: the freedom we can wish for to model the domain code. We could for example apply Domain-Driven
Line 127: Design (DDD) in it’s purest form. Not having to think about persistence or UI specific problems
Line 128: makes that so much easier.
Line 129: As we might expect, a Clean Architecture comes at a cost. Since the domain layer is completely
Line 130: decoupled from the outer layers like persistence and UI, we have to maintain a model of our
Line 131: 
Line 132: --- 페이지 22 ---
Line 133: 2. Inverting Dependencies
Line 134: 16
Line 135: application’s entities in each of the layers.
Line 136: Let’s assume, for instance, that we’re using an object-relational mapping (ORM) framework in our
Line 137: persistence layer. An ORM framework usually expects specific entity classes that contain metadata
Line 138: describing the database structure and the mapping of object fields to database columns. Since the
Line 139: domain layer doesn’t know the persistence layer, we cannot use the same entity classes in the
Line 140: domain layer and have to create them in both layers. That means we have to translate between
Line 141: both representations when the domain layer sends and receives data to and from the persistence
Line 142: layer. The same translation applies between the domain layer and other outer layers.
Line 143: But that’s a good thing! This decoupling is exactly what we wanted to achieve to free the domain
Line 144: code from framework-specific problems. The Java Persistence API (the standard ORM-API in the
Line 145: Java world), for instance, requires the ORM-managed entities to have a default constructor without
Line 146: arguments that we might want to avoid in our domain model. In chapter 8 “Mapping Between
Line 147: Boundaries”, we’ll talk about different mapping strategies, including a “no-mapping” strategy that
Line 148: just accepts the coupling between the domain and persistence layers.
Line 149: Since the Clean Architecture by Robert C. Martin is somewhat abstract, let’s go a level of detail
Line 150: deeper and look at a “Hexagonal Architecture”, which gives the clean architecture principles a more
Line 151: concrete shape.
Line 152: Hexagonal Architecture
Line 153: The term “Hexagonal Architecture” stems from Alistair Cockburn and has been around for quite
Line 154: some time¹⁴. It applies the same principles that Robert C. Martin later described in more general
Line 155: terms in his Clean Architecture.
Line 156: ¹⁴The primary source for the term “Hexagonal Architecture” seems to be an article on Alistair Cockburn’s website at
Line 157: https://alistair.cockburn.us/hexagonal-architecture/.
Line 158: 
Line 159: --- 페이지 23 ---
Line 160: 2. Inverting Dependencies
Line 161: 17
Line 162: Figure 9 - A hexagonal architecture is also called a “Ports and Adapters” architecture, since the application core
Line 163: provides specific ports for each adapter to interact with.
Line 164: Figure 9 shows what a hexagonal architecture might look like. The application core is represented
Line 165: as a hexagon, giving this architecture style it’s name. The hexagon shape has no meaning, however,
Line 166: so we might just as well draw an octagon and call it “Octagonal Architecture”. According to legend,
Line 167: the hexagon was simply used instead of the common rectangle to show that an application can have
Line 168: more than 4 sides connecting it to other systems or adapters.
Line 169: Within the hexagon, we find our domain entities and the use cases that work with them. Note
Line 170: that the hexagon has no outgoing dependencies, so that the Dependency Rule from Martin’s Clean
Line 171: Architecture holds true. Instead, all dependencies point towards the center.
Line 172: Outside of the hexagon, we find various adapters that interact with the application. There might be
Line 173: a web adapter that interacts with a web browser, some adapters interacting with external systems
Line 174: and an adapter that interacts with a database.
Line 175: The adapters on the left side are adapters that drive our application (because they call our application
Line 176: core) while the adapters on the right side are driven by our application (because they are called by
Line 177: our application core).
Line 178: To allow communication between the application core and the adapters, the application core
Line 179: provides specific ports. For driving adapters, such a port might be an interface that is implemented
Line 180: by one of the use case classes in the core and called by the adapter. For a driven adapter, it might be
Line 181: an interface that is implemented by the adapter and called by the core.
Line 182: Due to its central concepts this architecture style is also known as a “Ports and Adapters”
Line 183: architecture.
Line 184: Just like the Clean Architecture, we can organize this Hexagonal Architecture into layers. The
Line 185: outermost layer consists of the adapters that translate between the application and other systems.
Line 186: 
Line 187: --- 페이지 24 ---
Line 188: 2. Inverting Dependencies
Line 189: 18
Line 190: Next, we can combine the ports and use case implementations to form the application layer, because
Line 191: they define the interface of our application. The final layer contains the domain entities.
Line 192: In the next chapter, we’ll discuss a way to organize such an architecture in code.
Line 193: How Does This Help Me Build Maintainable Software?
Line 194: Name it Clean Architecture, Hexagonal Architecture or Ports and Adapters Architecture - by
Line 195: inverting our dependencies so that the domain code has no dependencies to the outside we can
Line 196: decouple our domain logic from all those persistence and UI specific problems and reduce the
Line 197: number of reasons to change throughout the codebase. And less reasons to change means better
Line 198: maintainability.
Line 199: The domain code is free to be modelled as best fits the business problems while the persistence and
Line 200: UI code are free to be modelled as best fits the persistence and UI problems.
Line 201: In the rest of this book, we’ll apply the Hexagonal architecture style to a web application. We’ll start
Line 202: by creating the package structure of our application and discussing the role of dependency injection.