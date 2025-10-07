Line 1: 
Line 2: --- 페이지 25 ---
Line 3: 3. Organizing Code
Line 4: Wouldn’t it be nice to recognize the architecture just by looking at the code?
Line 5: In this chapter, we’ll examine different ways of organizing code and introduce an expressive package
Line 6: structure that directly reflects a hexagonal architecture.
Line 7: In greenfield software projects, the first thing we try to get right is the package structure. We set up
Line 8: a nice-looking structure that we intend to use for the rest of project. Then, during the project, things
Line 9: become hectic and we realize that in many places the package structure is just a nice-looking facade
Line 10: for an unstructured mess of code. Classes in one package import classes from other packages that
Line 11: should not be imported.
Line 12: We’ll discuss different options for structuring the code of the BuckPal example application that was
Line 13: introduced in the preface. More specifically, we’ll look at the use case “Send Money” with which a
Line 14: user can transfer money from his account to another.
Line 15: Organizing By Layer
Line 16: The first approach to organizing our code is by layer. We might organize the code like this:
Line 17: 1
Line 18: buckpal
Line 19: 2
Line 20: ├──domain
Line 21: 3
Line 22: |
Line 23: ├──Account
Line 24: 4
Line 25: |
Line 26: ├──Activity
Line 27: 5
Line 28: |
Line 29: ├──AccountRepository
Line 30: 6
Line 31: |
Line 32: └──AccountService
Line 33: 7
Line 34: ├──persistence
Line 35: 8
Line 36: |
Line 37: └──AccountRepositoryImpl
Line 38: 9
Line 39: └──web
Line 40: 10
Line 41: └──AccountController
Line 42: For each of our layers web, domain and persistence we have a dedicated package. As discussed
Line 43: in chapter 1 “What’s Wrong with Layers?”, simple layers may not be the best structure for our
Line 44: code for several reasons, so we have already applied the Dependency Inversion Principle here, only
Line 45: allowing dependencies toward the domain code in the domain package. We did this by introducing
Line 46: the AccountRepository interface in the domain package and implementing it in the persistence
Line 47: package.
Line 48: However, we can find at least three reasons why this package structure is suboptimal.
Line 49: 
Line 50: --- 페이지 26 ---
Line 51: 3. Organizing Code
Line 52: 20
Line 53: First, we have no package boundary between functional slices or features of our application. If we
Line 54: add a feature for managing users, we’ll add an UserController to the web package, a UserService,
Line 55: UserRepository, and User to the domain package and an UserRepositoryImpl to the persistence
Line 56: package. Without further structure, this might quickly become a mess of classes leading to unwanted
Line 57: side effects between supposedly unrelated features of the application.
Line 58: Second, we can’t see which use cases our application provides. Can you tell what use cases the
Line 59: AccountService or AccountController classes implement? If we’re looking for a certain feature, we
Line 60: have to guess which service implements it and then search for the responsible method within that
Line 61: service.
Line 62: Similarly, we can’t see our target architecture within the package structure. We can guess that
Line 63: we have followed the Hexagonal architecture style and then browse the classes in the web and
Line 64: persistence packages to find the web and persistence adapters. But we can’t see at a glance which
Line 65: functionality is called by the web adapter and which functionality the persistence adapter provides
Line 66: for the domain layer. The incoming and outgoing ports are hidden in the code.
Line 67: Organizing By Feature
Line 68: Let’s try to address some of the issues of the “organize by layer” approach.
Line 69: The next approach is to organize our code by feature:
Line 70: 1
Line 71: buckpal
Line 72: 2
Line 73: └──account
Line 74: 3
Line 75: ├──Account
Line 76: 4
Line 77: ├──AccountController
Line 78: 5
Line 79: ├──AccountRepository
Line 80: 6
Line 81: ├──AccountRepositoryImpl
Line 82: 7
Line 83: └──SendMoneyService
Line 84: In essence, we have put all the code related to accounts into the high-level package account. We
Line 85: have also removed the layer packages.
Line 86: Each new group of features will get a new high-level package next to account and we can enforce
Line 87: package boundaries between the features by using package-private visibility for the classes that
Line 88: should not be accessed from the outside.
Line 89: The package boundaries, combined with package-private visibility, enable us to avoid unwanted
Line 90: dependencies between features. Check.
Line 91: We have also renamed AccountService to SendMoneyService to narrow its responsibility (we
Line 92: actually could have done that in the package-by-layer approach, too). We can now see that the code
Line 93: implements the use case “Send Money” just by looking at the class names. Making the application’s
Line 94: 
Line 95: --- 페이지 27 ---
Line 96: 3. Organizing Code
Line 97: 21
Line 98: functionality visible in the code is what Robert Martin calls a “Screaming Architecture”, because it
Line 99: screams its intention at us¹⁵. Check.
Line 100: However, the package-by-feature approach makes our architecture even less visible than the
Line 101: package-by-layer approach. We have no package names to identify our adapters, and we still
Line 102: don’t see the incoming and outgoing ports. What’s more, even though we have inverted the
Line 103: dependencies between domain code and persistence code so that SendMoneyService only knows the
Line 104: AccountRepository interface and not its implementation, we cannot use package-private visibility
Line 105: to protect the domain code from accidental dependencies to persistence code.
Line 106: So, how can we make our target architecture visible at a glance? It would be nice if we could point
Line 107: a finger at a box in an architecture diagram like figure 9 and instantly know which part of the code
Line 108: is responsible for that box.
Line 109: Let’s take one more step to create a package structure that is expressive enough to support this.
Line 110: An Architecturally Expressive Package Structure
Line 111: In a hexagonal architecture we have entities, use cases, incoming and outgoing ports and incoming
Line 112: and outgoing (or “driving” and “driven”) adapters as our main architecture elements. Let’s fit them
Line 113: into a package structure that expresses this architecture:
Line 114: 1
Line 115: buckpal
Line 116: 2
Line 117: └──account
Line 118: 3
Line 119: ├──adapter
Line 120: 4
Line 121: |
Line 122: ├──in
Line 123: 5
Line 124: |
Line 125: |
Line 126: └──web
Line 127: 6
Line 128: |
Line 129: |
Line 130: └──AccountController
Line 131: 7
Line 132: |
Line 133: ├──out
Line 134: 8
Line 135: |
Line 136: |
Line 137: └──persistence
Line 138: 9
Line 139: |
Line 140: |
Line 141: ├──AccountPersistenceAdapter
Line 142: 10
Line 143: |
Line 144: |
Line 145: └──SpringDataAccountRepository
Line 146: 11
Line 147: ├──domain
Line 148: 12
Line 149: |
Line 150: ├──Account
Line 151: 13
Line 152: |
Line 153: └──Activity
Line 154: 14
Line 155: └──application
Line 156: 15
Line 157: └──SendMoneyService
Line 158: 16
Line 159: └──port
Line 160: 17
Line 161: ├──in
Line 162: 18
Line 163: |
Line 164: └──SendMoneyUseCase
Line 165: 19
Line 166: └──out
Line 167: 20
Line 168: ├──LoadAccountPort
Line 169: 21
Line 170: └──UpdateAccountStatePort
Line 171: ¹⁵Clean Architecture by Robert C. Martin, Prentice Hall, 2017, Chapter 21
Line 172: 
Line 173: --- 페이지 28 ---
Line 174: 3. Organizing Code
Line 175: 22
Line 176: Each element of the architecture can directly be mapped to one of the packages. On the highest level,
Line 177: we again have a package named account, indicating that this is the module implementing the use
Line 178: cases around an Account.
Line 179: On the next level, we have the domain package containing our domain model. The application
Line 180: package contains a service layer around this domain model. The SendMoneyService implements the
Line 181: incoming port interface SendMoneyUseCase and uses the outgoing port interfaces LoadAccountPort
Line 182: and UpdateAccountStatePort, which are implemented by the persistence adapter.
Line 183: The adapter package contains the incoming adapters that call the application layers’ incoming ports
Line 184: and the outgoing adapters that provide implementations for the application layers’ outgoing ports.
Line 185: In our case, we’re building a simple web application with the adapters web and persistence, each
Line 186: having its own sub-package.
Line 187: Phew, that’s a lot of technical-sounding packages. Isn’t that confusing?
Line 188: Imagine we have a high-level view of our hexagonal architecture hanging at the office wall and
Line 189: we’re talking to a colleague about modifying a client to a third-party API we’re consuming. While
Line 190: discussing, we can point at the corresponding outgoing adapter on the poster to better understand
Line 191: each other. Then, when we’re finished talking, we sit down in front of our IDE and can start working
Line 192: on the client right away, because the code of the API client we have talked about can be found in
Line 193: the adapter/out/<name-of-adapter> package.
Line 194: Rather helpful instead of confusing, don’t you think?
Line 195: This package structure is a powerful element in the fight against the so-called “architecture/code gap”
Line 196: or “model/code gap”¹⁶. These terms describe the fact that in most software development projects the
Line 197: architecture is only an abstract concept that cannot be directly mapped to the code. With time, if
Line 198: the package structure (among other things) does not reflect the architecture, the code will usually
Line 199: deviate more and more from the target architecture.
Line 200: Also, this expressive package structure promotes active thinking about the architecture. We have
Line 201: many packages and have to think about into which package to put the code we’re currently working
Line 202: on.
Line 203: But don’t so many packages mean that everything has to be public in order to allow access across
Line 204: packages?
Line 205: For the adapter packages, at least, this is not true. All classes they contain may be package private
Line 206: since they are not called by the outside world except over port interfaces, which live within the
Line 207: application package. So, no accidental dependencies from the application layer to the adapter
Line 208: classes. Check.
Line 209: Within the application and domain packages, however, some classes indeed have to be public. The
Line 210: ports must be public because they must be accessible to the adapters by design. The domain classes
Line 211: must be public to be accessible by the services and, potentially, by the adapters. The services don’t
Line 212: need to be public, because they can be hidden behind the incoming port interfaces.
Line 213: ¹⁶Just Enough Architecture by George Fairbanks, Marshall & Brainerd, 2010, page 167
Line 214: 
Line 215: --- 페이지 29 ---
Line 216: 3. Organizing Code
Line 217: 23
Line 218: Moving the adapter code to their own packages has the added benefit that we can very easily
Line 219: replace one adapter with another implementation, should the need arise. Imagine we have started
Line 220: implementing against a simple key-value database, because we weren’t sure about which database
Line 221: would be best in the end, and now we need to switch to an SQL database. We simply implement all
Line 222: relevant outgoing ports in a new adapter package and then remove the old package.
Line 223: Another very appealing advantage of this package structure is that it directly maps to DDD concepts.
Line 224: The high-level package, account, in our case, is a bounded context which has dedicated entry and
Line 225: exit points (the ports) to communicate with other bounded contexts. Within the domain package, we
Line 226: can build any domain model we want, using all the tools DDD provides us.
Line 227: As with every structure, it takes discipline to maintain this package structure over the lifetime of a
Line 228: software project. Also, there will be cases when the package structure just does not fit and we see
Line 229: no other way than to widen the architecture/code gap and create a package that does not reflect the
Line 230: architecture.
Line 231: There is no perfection. But with an expressive package structure, we can at least reduce the the gap
Line 232: between code and architecture.
Line 233: The Role of Dependency Injection
Line 234: The package structure described above goes a long way towards a clean architecture, but an essential
Line 235: requirement of such an architecture is that the application layer does not have dependencies to the
Line 236: incoming and outgoing adapters, as we have learned in chapter 2 “Inverting Dependencies”.
Line 237: For incoming adapters, like our web adapter, this is easy, since the control flow points in the same
Line 238: direction as the dependency between adapter and domain code. The adapter simply calls the service
Line 239: within the application layer. In order to clearly demarcate the entry points to our application, we
Line 240: might want to hide the actual services between port interfaces nonetheless.
Line 241: For outgoing adapters, like our persistence adapter, we have to make use of the Dependency Inversion
Line 242: Principle to turn the dependency against the direction of the control flow.
Line 243: We have already seen how that works. We create an interface within the application layer that is
Line 244: implemented by a class within the adapter. Within our hexagonal architecture, this interface is a
Line 245: port. The application layer then calls this port interface to call the functionality of the adapter as
Line 246: shown in figure 10.
Line 247: 
Line 248: --- 페이지 30 ---
Line 249: 3. Organizing Code
Line 250: 24
Line 251: Figure 10 - The web controller calls an incoming port, which is implemented by a service. The service calls an outgoing
Line 252: port, which is implemented by an adapter.
Line 253: But who provides the application with the actual objects that implement the port interfaces? We
Line 254: don’t want to instantiate the ports manually within the application layer, because we don’t want to
Line 255: introduce a dependency to an adapter.
Line 256: This is where dependency injection comes into play. We introduce a neutral component that has a
Line 257: dependency to all layers. This component is responsible for instantiating most of the classes that
Line 258: make up our architecture.
Line 259: In the example figure above, the neutral dependency injection component would create instances
Line 260: of the AccountController, SendMoneyService, and AccountPersistenceAdapter classes. Since the
Line 261: AccountController requires a SendMoneyUseCase, the dependency injection will give it an instance
Line 262: of the SendMoneyService class during construction. The controller doesn’t know that it actually got
Line 263: a SendMoneyService instance since it only needs to know the interface.
Line 264: Similarly, when constructing the SendMoneyService instance, the dependency injection mechanism
Line 265: will inject an instance of the AccountPersistenceAdapter class, in the guise of the LoadAccountPort
Line 266: interface. The service never knows the actual class behind the interface.
Line 267: We’ll talk more about initializing an application using the Spring framework as an example in
Line 268: chapter 9 “Assembling the Application”.
Line 269: 
Line 270: --- 페이지 31 ---
Line 271: 3. Organizing Code
Line 272: 25
Line 273: How Does This Help Me Build Maintainable Software?
Line 274: We have looked at a package structure for a hexagonal architecture that takes the actual code
Line 275: structure as close to the target architecture as possible. Finding an element of the architecture in
Line 276: the code is now a matter of navigating down the package structure along the names of certain boxes
Line 277: in an architecture diagram, helping in communication, development and maintenance.
Line 278: In the following chapters, we’ll see this package structure and dependency injection in action as
Line 279: we’re going to implement a use case in the application layer, a web adapter and a persistence adapter.