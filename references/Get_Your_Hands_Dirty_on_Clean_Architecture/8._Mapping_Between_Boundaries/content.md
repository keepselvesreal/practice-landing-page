Line 1: 
Line 2: --- 페이지 76 ---
Line 3: 8. Mapping Between Boundaries
Line 4: In the previous chapters, we’ve discussed the web, application, domain and persistence layers and
Line 5: what each of those layers contributes to implementing a use case.
Line 6: We have, however, barely touched the dreaded and omnipresent topic of mapping between the
Line 7: models of each layer. I bet you’ve had a discussion at some point about whether to use the same
Line 8: model in two layers in order to avoid implementing a mapper.
Line 9: The argument might have gone something like this:
Line 10: Pro-Mapping Developer:
Line 11: > If we don’t map between layers, we have to use the same model in both layers which means that
Line 12: the layers will be tightly coupled!
Line 13: Contra-Mapping Developer:
Line 14: > But if we do map between layers, we produce a lot of boilerplate code which is overkill for many
Line 15: use cases, since they’re only doing CRUD and have the same model across layers anyways!
Line 16: As is often the case in discussions like this, there’s truth to both sides of the argument. Let’s discuss
Line 17: some mapping strategies with their pros and cons and see if we can help those developers make a
Line 18: decision.
Line 19: The “No Mapping” Strategy
Line 20: The first strategy is actually not mapping at all.
Line 21: Figure 22 - If the port interfaces use the domain model as input and output model we don’t need to map between
Line 22: layers.
Line 23: Figure 22 shows the components that are relevant for the “Send Money” use case from our BuckPal
Line 24: example application.
Line 25: In the web layer, the web controller calls the SendMoneyUseCase interface to execute the use case.
Line 26: This interface takes a Account object as argument. This means that both the web and application
Line 27: layer need access to the Account class - both are using the same model.
Line 28: 
Line 29: --- 페이지 77 ---
Line 30: 8. Mapping Between Boundaries
Line 31: 71
Line 32: On the other side of the application we have the same relationship between the persistence and
Line 33: application layer.
Line 34: Since all layers use the same model, we don’t need to implement a mapping between them.
Line 35: But what are the consequences of this design?
Line 36: The web and persistence layers may have special requirements to their models. If our web layer
Line 37: exposes its model via REST, for instance, the model classes might need some annotations that define
Line 38: how to serialize certain fields into JSON. The same is true for the persistence layer if we’re using an
Line 39: ORM framework, which might require some annotations that define the database mapping.
Line 40: In the example, all of those special requirements have to be dealt with in the Account domain model
Line 41: class even though the domain and application layers are not interested in them. This violates the
Line 42: Single Responsibility Principle since the Account class has to be changed for reasons of the web,
Line 43: application, and persistence layer.
Line 44: Aside from the technical requirements, each layer might require certain custom fields on the Account
Line 45: class. This might lead to a fragmented domain model with certain fields only relevant in one layer.
Line 46: Does this mean, though, that we should never, ever implement a “no mapping” strategy? Certainly
Line 47: not.
Line 48: Even though it might feel dirty, a “no mapping” strategy can be perfectly valid.
Line 49: Consider a simple CRUD use case. Do we really need to map the same fields from the web model
Line 50: into the domain model and from the domain model into the persistence model? I’d say we don’t.
Line 51: And what about those JSON or ORM annotations on the domain model? Do they really bother us?
Line 52: Even if we have to change an annotation or two in the domain model if something changes in the
Line 53: persistence layer, so what?
Line 54: As long as all layers need exactly the same information in exactly the same structure, a “no mapping”
Line 55: strategy is a perfectly valid option.
Line 56: As soon as we’re dealing with web or persistence issues in the application or domain layer (aside
Line 57: from annotations, perhaps), however, we should move to another mapping strategy.
Line 58: There is a lesson for the two developers from the introduction here: even though we have decided
Line 59: on a certain mapping strategy in the past, we can change it later.
Line 60: In my experience, many use cases start their life as simple CRUD use cases. Later, they might grow
Line 61: into a full-fledged business use case with a rich behavior and validations which justify a more
Line 62: expensive mapping strategy. Or they might forever keep their CRUD status, in which case we’re
Line 63: glad that we haven’t invested into a different mapping strategy.
Line 64: The “Two-Way” Mapping Strategy
Line 65: A mapping strategy where each layer has its own model is what I call the “Two-Way” mapping
Line 66: strategy outlined in Figure 23.
Line 67: 
Line 68: --- 페이지 78 ---
Line 69: 8. Mapping Between Boundaries
Line 70: 72
Line 71: Figure 23 - With each adapter having its own model, the adapters are responsible to map their model into the domain
Line 72: model and back.
Line 73: Each layer has its own model, which may have a structure that is completely different from the
Line 74: domain model.
Line 75: The web layer maps the web model into the input model that is expected by the incoming ports. It
Line 76: also maps domain objects returned by the incoming ports back into the web model.
Line 77: The persistence layer is responsible for a similar mapping between the domain model, which is used
Line 78: by the outgoing ports, and the persistence model.
Line 79: Both layers map in two directions, hence the name “Two-Way” mapping.
Line 80: With each layer having its own model, each layer can modify its own model without affecting
Line 81: the other layers (as long as the contents are unchanged). The web model can have a structure that
Line 82: allows for optimal presentation of the data. The domain model can have a structure that best allows
Line 83: for implementing the use cases. And the persistence model can have the structure needed by an
Line 84: OR-Mapper for persisting objects to a database.
Line 85: This mapping strategy also leads to a clean domain model that is not dirtied by web or persistence
Line 86: concerns. It does not contain JSON or ORM mapping annotations. The Single Responsibility Principle
Line 87: is satisfied.
Line 88: Another bonus of “Two-Way” mapping is that, after the “No Mapping” strategy, it’s the conception-
Line 89: ally simplest mapping strategy. The mapping responsibilities are clear: the outer layers / adapters
Line 90: map into the model of the inner layers and back. The inner layers only know their own model and
Line 91: can concentrate on the domain logic instead of mapping.
Line 92: As every mapping strategy, the “Two-Way” mapping also has its drawbacks.
Line 93: First of all, it usually ends up in a lot of boilerplate code. Even if we use one of the many mapping
Line 94: frameworks out there to reduce the amount of code, implementing the mapping between models
Line 95: usually takes up a good portion of our time. This is partly due to the fact that debugging mapping
Line 96: logic is a pain - especially when using a mapping framework that hides its inner workings behind a
Line 97: layer of generic code and reflection.
Line 98: Another drawback is that the domain model is used to communicate across layer boundaries. The
Line 99: incoming ports and outgoing ports use domain objects as input parameters and return values. This
Line 100: makes them vulnerable to changes that are triggered by the needs of the outer layers whereas it’s
Line 101: desirable for the domain model only to evolve due to the needs of the domain logic.
Line 102: 
Line 103: --- 페이지 79 ---
Line 104: 8. Mapping Between Boundaries
Line 105: 73
Line 106: Just like the “No Mapping” strategy, the “Two-Way” mapping strategy is not a silver bullet. In many
Line 107: projects, however, this kind of mapping is considered a holy law that we have to comply with
Line 108: throughout the whole codebase, even for the simplest CRUD use cases. This unnecessarily slows
Line 109: down development.
Line 110: No mapping strategy should be considered an iron law. Instead, we should decide for each use case.
Line 111: The “Full” Mapping Strategy
Line 112: Another mapping strategy is what I call the “Full” mapping strategy sketched in Figure 24.
Line 113: Figure 24 - With each operation requiring its own model, the web adapter and application layer each map their model
Line 114: into the model expected by the operation they want to execute.
Line 115: This mapping strategy introduces a separate input and output model per operation. Instead of
Line 116: using the domain model to communicate across layer boundaries, we use a model specific to each
Line 117: operation, like the SendMoneyCommand, which acts as an input model to the SendMoneyUseCase port
Line 118: in the figure. We can call those models “commands”, “requests”, or similar.
Line 119: The web layer is responsible for mapping its input into the command object of the application layer.
Line 120: Such a command makes the interface to the application layer very explicit, with little room for
Line 121: interpretation. Each use case has its own command with its own fields and validations. There’s no
Line 122: guessing involved as to which fields should be filled and which fields should better be left empty
Line 123: since they would otherwise trigger a validation we don’t want for our current use case.
Line 124: The application layer is then responsible for mapping the command object into whatever it needs
Line 125: to modify the domain model according to the use case.
Line 126: Naturally, mapping from the one layer into many different commands requires even more mapping
Line 127: code than mapping between a single web model and domain model. This mapping, however, is
Line 128: significantly easier to implement and maintain than a mapping that has to handle the needs of
Line 129: many use cases instead of only one.
Line 130: I don’t advocate this mapping strategy as a global pattern. It plays out its advantages best between
Line 131: the web layer (or any other incoming adapter) and the application layer to clearly demarcate the
Line 132: state-modifying use cases of the application. I would not use it between application and persistence
Line 133: layer due to the mapping overhead.
Line 134: 
Line 135: --- 페이지 80 ---
Line 136: 8. Mapping Between Boundaries
Line 137: 74
Line 138: Also, in some cases, I would restrict this kind of mapping to the input model of operations and simply
Line 139: use a domain object as the output model. The SendMoneyUseCase might then return an Account object
Line 140: with the updated balance, for instance.
Line 141: This shows that the mapping strategies can and should be mixed. No mapping strategy needs to be
Line 142: a global rule across all layers.
Line 143: The “One-Way” Mapping Strategy
Line 144: There is yet another mapping strategy with another set of pros and cons: the “One-Way” strategy
Line 145: sketched in Figure 25.
Line 146: Figure 25 - With the domain model and the adapter models implementing the same “state” interface, each layer only
Line 147: needs to map objects it receives from other layers - one way.
Line 148: In this strategy, the models in all layers implement the same interface that encapsulates the state of
Line 149: the domain model by providing getter methods on the relevant attributes.
Line 150: The domain model itself can implement a rich behavior, which we can access from our services
Line 151: within the application layer. If we want to pass a domain object to the outer layers, we can do so
Line 152: without mapping, since the domain object implements the state interface expected by the incoming
Line 153: and outgoing ports.
Line 154: The outer layers can then decide if they can work with the interface or if they need to map it into their
Line 155: own model. They cannot inadvertently modify the state of the domain object since the modifying
Line 156: behavior is not exposed by the state interface.
Line 157: Objects we pass from an outer layer into the application layer also implement this state interface.
Line 158: The application layer then has to map it into the real domain model in order to get access to its
Line 159: behavior. This mapping plays well with the DDD concept of a factory. A factory in terms of DDD
Line 160: is responsible for reconstituting a domain object from a certain state, which is exactly what we’re
Line 161: doing²⁷.
Line 162: ²⁷Domain Driven Design by Eric Evans, Addison-Wesley, 2004, p. 158
Line 163: 
Line 164: --- 페이지 81 ---
Line 165: 8. Mapping Between Boundaries
Line 166: 75
Line 167: The mapping responsibility is clear: if a layer receives an object from another layer, we map it into
Line 168: something the layer can work with. Thus, each layer only maps one way, making this the “One-Way”
Line 169: mapping strategy.
Line 170: With the mapping distributed across layers, however, this strategy is conceptionally more difficult
Line 171: than the other strategies.
Line 172: This strategy plays out its strength best if the if the models across the layers are similar. For read-
Line 173: only operations, for instance, the web layer then might not need to map into its own model at all,
Line 174: since the state interface provides all the information it needs.
Line 175: When to use which Mapping Strategy?
Line 176: This is the million-dollar question, isn’t it?
Line 177: The answer is the usual, dissatisfying, “it depends”.
Line 178: Since each mapping strategy has different advantages and disadvantages we should resist the urge
Line 179: to define a single strategy as a hard-and-fast global rule for the whole codebase. This goes against
Line 180: our instincts, as it feels untidy to mix patterns within the same codebase. But knowingly choosing a
Line 181: pattern that is not the best pattern for a certain job, just to serve our sense of tidiness, is irresponsible,
Line 182: plain and simple.
Line 183: Also, as software evolves over time, the strategy that was the best for the job yesterday might not
Line 184: still be the best for the job today. Instead of starting with a fixed mapping strategy and keep it over
Line 185: time - no matter what - we might start with a simple strategy that allows us to quickly evolve the
Line 186: code and later move to a more complex one that helps us to better decouple the layers.
Line 187: In order to decide which strategy to use when, we need to agree upon a set of guidelines within
Line 188: the team. These guidelines should answer the question which mapping strategy should be the first
Line 189: choice in which situation. They should also answer why they are first choice so that we’re able to
Line 190: evaluate if those reasons still apply after some time.
Line 191: We might for example define different mapping guidelines to modifying use cases than we do to
Line 192: queries. Also, we might want to use different mapping strategies between the web and application
Line 193: layer and between the application and persistence layer.
Line 194: Guidelines for these situations might look like this:
Line 195: If we’re working on a modifying use case, the “full mapping” strategy is the first choice between the
Line 196: web and application layer, in order to decouple the use cases from one another. This gives us clear
Line 197: per-use-case validation rules and we don’t have to deal with fields we don’t need in a certain use
Line 198: case.
Line 199: If we’re working on a modifying use case, the “no mapping” strategy is the first choice between the
Line 200: application and persistence layer in order to be able to quickly evolve the code without mapping
Line 201: overhead. As soon as we have to deal with persistence issues in the application layer, however, we
Line 202: move to a “two-way” mapping strategy to keep persistence issues in the persistence layer.
Line 203: 
Line 204: --- 페이지 82 ---
Line 205: 8. Mapping Between Boundaries
Line 206: 76
Line 207: If we’re working on a query, the “no mapping” strategy is the first choice between the web and
Line 208: application layer and between the application and persistence layer in order to be able to quickly
Line 209: evolve the code without mapping overhead. As soon as we have to deal with web or persistence
Line 210: issues in the application layer, however, we move to a “two-way” mapping strategy between the
Line 211: web and application layer or the application layer and persistence layer, respectively.
Line 212: In order to successfully apply guidelines like these, they must be present in the minds of the
Line 213: developers. So, the guidelines should be discussed and revised continuously as a team effort.
Line 214: How Does This Help Me Build Maintainable Software?
Line 215: With incoming and outgoing ports acting as gatekeepers between the layers of our application, they
Line 216: define how the layers communicate with each other and thus if and how we map between layers.
Line 217: With narrow ports in place for each use case, we can choose different mapping strategies for different
Line 218: use cases, and even evolve them over time without affecting other use cases, thus selecting the best
Line 219: strategy for a certain situation at a certain time.
Line 220: This selection of mapping strategies per situation certainly is harder and requires more communi-
Line 221: cation than simply using the same mapping strategy for all situations, but it will reward the team
Line 222: with a codebase that does just what it needs to do and is easier to maintain, as long as the mapping
Line 223: guidelines are known.