Line 1: 
Line 2: --- 페이지 99 ---
Line 3: 11. Taking Shortcuts Consciously
Line 4: In the preface of this book, I cursed the fact that we feel forced to take shortcuts all the time, building
Line 5: up a great heap of technical debt we never have the chance to pay back.
Line 6: To prevent shortcuts, we must be able to identify them. So, the goal of this chapter is to raise
Line 7: awareness of some potential shortcuts and discuss their effects.
Line 8: With this information, we can identify and fix accidental shortcuts. Or, if justified, we can even
Line 9: consciously opt-in to the effects of a shortcut³¹.
Line 10: Why Shortcuts Are Like Broken Windows
Line 11: In 1969, psychologist Philip Zimbardo conducted an experiment to test a theory that later became
Line 12: known as the “Broken Windows Theory”³².
Line 13: He parked one car without license plates in a Bronx neighborhood and another in an allegedly
Line 14: “better” neighborhood in Palo Alto. Then he waited.
Line 15: The car in the Bronx was picked clean of valuable parts within 24 hours and then passersby started
Line 16: to randomly destroy it.
Line 17: The car in Palo Alto was not touched for a week, so Zimbardo smashed a window. From then on,
Line 18: the car had a similar fate to the car in the Bronx and was destroyed in the same short amount of
Line 19: time by people walking by.
Line 20: The people taking part in looting and destroying the cars came from across all social classes and
Line 21: included people who were otherwise law-abiding and well-behaved citizens.
Line 22: This human behavior has become known as the Broken Windows Theory. In my own words:
Line 23: As soon as something looks run-down, damaged, [insert negative adjective here], or
Line 24: generally untended, the human brain feels that it’s OK to make it more run-down,
Line 25: damaged, or [insert negative adjective here].
Line 26: This theory applies to many areas of life:
Line 27: • In a neighborhood where vandalism is common, the threshold to loot or damage an untended
Line 28: car is low.
Line 29: ³¹Imagine this sentence in a book about construction engineering or, even scarier, in a book about avionics! Most of us, however, are
Line 30: not building the software equivalent of a skyscraper or an airplane. And software is soft and can be changed more easily than hardware, so
Line 31: sometimes it’s actually more economic to (consciously!) take a shortcut first and fix it later (or never).
Line 32: ³²https://www.theatlantic.com/ideastour/archive/windows.html
Line 33: 
Line 34: --- 페이지 100 ---
Line 35: 11. Taking Shortcuts Consciously
Line 36: 94
Line 37: • When a car has a broken window, the threshold to damage it further is low, even in a “good”
Line 38: neighborhood.
Line 39: • In an untidy bedroom, the threshold to throw our clothes on the ground instead of putting
Line 40: them into the wardrobe is low.
Line 41: • In a group of people where bullying is common, the threshold to bully just a little more is low.
Line 42: • …
Line 43: Applied to working with code, this means:
Line 44: • When working on a low-quality codebase, the threshold to add more low-quality code is low.
Line 45: • When working on a codebase with a lot of coding violations, the threshold to add another
Line 46: coding violation is low.
Line 47: • When working on a codebase with a lot of shortcuts, the threshold to add another shortcut is
Line 48: low.
Line 49: • …
Line 50: With all this in mind, is it really a surprise that the quality of many so-called “legacy” codebases has
Line 51: eroded so badly over time?
Line 52: The Responsibility of Starting Clean
Line 53: While working with code doesn’t really feel like looting a car, we all are unconsciously subject to the
Line 54: Broken Windows psychology. This makes it important to start a project clean, with as little shortcuts
Line 55: and technical debt as possible. Because, as soon as a shortcut creeps in, it acts as a broken window
Line 56: and attracts more shortcuts.
Line 57: Since a software project often is a very expensive and long-running endeavor, keeping broken
Line 58: windows at bay is a huge responsibility for us as software developers. We may even not be the
Line 59: ones finishing the project and others have to take over. For them, it’s a legacy codebase they don’t
Line 60: have a connection to, yet, lowering the threshold for creating broken windows even further.
Line 61: There are times, however, when we decide a shortcut is the pragmatic thing to do, be it because
Line 62: the part of the code we’re working on is not that important to the project as a whole, or that we’re
Line 63: prototyping, or for economical reasons.
Line 64: We should take great care to document such consciously added shortcuts, for example in the form of
Line 65: Architecture Decision Records (ADRs) as proposed by Michael Nygard in his blog³³. We owe that to
Line 66: our future selves and to our successors. If every member of the team is aware of this documentation,
Line 67: it will even reduce the Broken Windows effect, because the team will know that the shortcuts have
Line 68: been taken consciously and for good reason.
Line 69: The following sections each discuss a pattern that can be considered a shortcut in the hexagonal
Line 70: architecture style presented in this book. We’ll have a look at the effects of the shortcuts and the
Line 71: arguments that speak for and against taking them.
Line 72: ³³http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions
Line 73: 
Line 74: --- 페이지 101 ---
Line 75: 11. Taking Shortcuts Consciously
Line 76: 95
Line 77: Sharing Models between Use Cases
Line 78: In chapter 4 “Implementing a Use Case”, I argued that different use cases should have a different
Line 79: input and output model, meaning that the types of the input parameters and the types of the return
Line 80: values should be different.
Line 81: Figure 29 shows an example where two use cases share the same input model:
Line 82: Figure 29 - Sharing the input or output model between use cases leads to coupling between the use cases.
Line 83: The effect of sharing in this case is that SendMoneyUseCase and RevokeActivityUseCase are coupled
Line 84: to each other. If we change something within the shared SendMoneyCommand class, both use cases are
Line 85: affected. They share a reason to change in terms of the Single Responsibility Principle. The same is
Line 86: true if both use cases share the same output model.
Line 87: Sharing input and output models between use cases is valid if the use cases are functionally bound,
Line 88: i.e. if they share a certain requirement. In this case, we actually want both use cases to be affected if
Line 89: we change a certain detail.
Line 90: If both use cases should be able to evolve separately from each other, however, this is a shortcut. In
Line 91: this case, we should separate the use cases from the start, even if it means to duplicate input and
Line 92: output classes if they look the same at the start.
Line 93: So, when building multiple use cases around a similar concept, it’s worthwhile to regularly ask the
Line 94: question whether the use cases should evolve separately from each other. As soon as the answer
Line 95: becomes a “yes”, it’s time to separate the input and output models.
Line 96: 
Line 97: --- 페이지 102 ---
Line 98: 11. Taking Shortcuts Consciously
Line 99: 96
Line 100: Using Domain Entities as Input or Output Model
Line 101: If we have an Account domain entity and an incoming port SendMoneyUseCase, we might be tempted
Line 102: to use the entity as the input and/or output model of the incoming port, as figure 30 shows:
Line 103: Figure 30 - Using a domain entity as input or output model of a use case couples the domain entity to the use case.
Line 104: The incoming port has a dependency to the domain entity. The consequence of this is that we’ve
Line 105: added another reason for the Account entity to change.
Line 106: Wait, the Account entity doesn’t have a dependency to the SendMoneyUseCase incoming port (it’s the
Line 107: other way around), so how can the incoming port be a reason to change for the entity?
Line 108: Say we need some information about an account in the use case that is not currently available in the
Line 109: Account entity. This information is ultimately not to be stored in the Account entity, however, but
Line 110: in a different domain or bounded context. We’re tempted to add a new field to the Account entity
Line 111: nevertheless, because it’s already available in the use case interface.
Line 112: For simple create or update use cases, a domain entity in the use case interface may be fine, since
Line 113: the entity contains exactly the information we need to persist its state in the database.
Line 114: As soon as a use case is not simply about updating a couple of fields in the database, but instead
Line 115: implements more complex domain logic (potentially delegating part of the domain logic to a rich
Line 116: domain entity), we should use a dedicated input and output model for the use case interface, because
Line 117: we don’t want changes in the use case to propagate to the domain entity.
Line 118: What makes this shortcut dangerous is the fact that many use cases start their lives as a simple create
Line 119: or update use case only to become beasts of complex domain logic over time. This is especially true
Line 120: in an agile environment where we start with a minimum viable product and add complexity on the
Line 121: way forward. So if we used a domain entity as input model at the start, we must find the point in
Line 122: time when to replace it with a dedicated input model that is independent of the domain entity.
Line 123: 
Line 124: --- 페이지 103 ---
Line 125: 11. Taking Shortcuts Consciously
Line 126: 97
Line 127: Skipping Incoming Ports
Line 128: While the outgoing ports are necessary to invert the dependency between the application layer and
Line 129: the outgoing adapters (to make the dependencies point inward), we don’t need the incoming ports for
Line 130: dependency inversion. We could decide to let the incoming adapters access our application services
Line 131: directly, without incoming ports in between, as shown in figure 31.
Line 132: Figure 31 - Without incoming ports, we lose clearly marked entry points to the domain logic.
Line 133: By removing the incoming ports, we have reduced a layer of abstraction between incoming adapters
Line 134: and the application layer. Removing layers of abstraction usually feels rather good.
Line 135: The incoming ports, however, define the entry points into out application core. Once we remove
Line 136: them, we must know more about the internals of our application to find out which service method we
Line 137: can call to implement a certain use case. By maintaining dedicated incoming ports, we can identify
Line 138: the entry points to the application at a glance. This makes it especially easy for new developers to
Line 139: get their bearings in the codebase.
Line 140: Another reason to keep the incoming ports is that they allow us to easily enforce architecture. With
Line 141: the enforcement options from chapter 10 “Enforcing Architecture Boundaries” we can make certain
Line 142: that incoming adapters only call incoming ports and not application services. This makes every
Line 143: entry point into the application layer a very conscious decision. We can no longer accidentally call
Line 144: a service method that was not meant to be called from an incoming adapter.
Line 145: If an application is small enough or only has a single incoming adapter so that we can grasp the
Line 146: whole control flow without the help of incoming ports, we might want to do without incoming
Line 147: ports. However, how often can we say that we know that an application stays small or will only
Line 148: ever have a single incoming adapter over its whole lifetime?
Line 149: Skipping Application Services
Line 150: Aside from the incoming ports, for certain use cases we might want to skip the application layer as
Line 151: a whole, as figure 32 shows:
Line 152: 
Line 153: --- 페이지 104 ---
Line 154: 11. Taking Shortcuts Consciously
Line 155: 98
Line 156: Figure 32 - Without application services, we don’t have a specified location for domain logic.
Line 157: Here, the AccountPersistenceAdapter class within an outgoing adapter directly implements an
Line 158: incoming port and replaces the application service that usually implements an incoming port.
Line 159: It is very tempting to do this for simple CRUD use cases, since in this case an application service
Line 160: usually only forwards a create, update or delete request to the persistence adapter, without adding
Line 161: any domain logic. Instead of forwarding, we can let the persistence adapter implement the use case
Line 162: directly.
Line 163: This, however, requires a shared model between the incoming adapter and the outgoing adapter,
Line 164: which is the Account domain entity in this case, so it usually means that we’re using the domain
Line 165: model as input model as described above.
Line 166: Furthermore, we no longer have a representation of the use case within our application core. If a
Line 167: CRUD use case grows to something more complex over time, it’s tempting to add domain logic
Line 168: directly to the outgoing adapter, since the use case has already been implemented there. This
Line 169: decentralizes the domain logic, making it harder to find and to maintain.
Line 170: In the end, to prevent boilerplate pass-through services, we might choose to skip the application
Line 171: services for simple CRUD use cases after all. Then, however, the team should develop clear guidelines
Line 172: to introduce an application service as soon as the use case is expected to do more than just create,
Line 173: update or delete an entity.
Line 174: How Does This Help Me Build Maintainable Software?
Line 175: There are times when shortcuts make sense from an economic point of view. This chapter provided
Line 176: some insights to the consequences some shortcuts might have to help decide whether to take them
Line 177: or not.
Line 178: The discussion shows that it’s tempting to introduce shortcuts for simple CRUD use cases, since
Line 179: for them, implementing the whole architecture feels like overkill (and the shortcuts don’t feel like
Line 180: shortcuts). Since all applications start small, however, it’s very important for the team to agree upon
Line 181: when a use case grows out of its CRUD state. Only then can the team replace the shortcuts with an
Line 182: architecture that is more maintainable in the long run.
Line 183: 
Line 184: --- 페이지 105 ---
Line 185: 11. Taking Shortcuts Consciously
Line 186: 99
Line 187: Some use cases will never grow out of their CRUD state. For them, it might be more pragmatic to
Line 188: keep the shortcuts in place forever, as they don’t really entail a maintenance overhead.
Line 189: In any case, we should document the architecture and the decisions why we chose a certain shortcut
Line 190: so that we (or our successors) can re-evaluate the decisions in the future.