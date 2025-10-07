Line 1: 
Line 2: --- 페이지 17 ---
Line 3: Chapter 1. On Tests and Tools
Line 4: This introductory chapter presents the main categories of test. It will enable us to understand the role
Line 5: of each of them, and also to see the place and purpose of unit tests.
Line 6: Naming Chaos
Line 7: If you start digging into the topic of tests, you will be amazed at how many names show up. Unit
Line 8: tests, integration tests, smoke tests, stress tests, end-to-end tests, exploratory tests, system tests,
Line 9: performance tests, user tests, automated tests, acceptance tests, etc. You may well feel perplexed
Line 10: by the sheer number of them, and by the variety of existing classifications. You will get even more
Line 11: perplexed if you start looking for a definition for each of them. Soon you will come across a good
Line 12: few definitions of the same term that differ substantially1. This terminological chaos makes testing
Line 13: subjects much harder to follow than they should be.
Line 14: In this book I follow what I regard as being the most widely used set of test-related terms. I think, that
Line 15: the chosen names describe their purpose well. I can only hope that they do so for you too.
Line 16: 1.1. An Object-Oriented System
Line 17: We will right away discuss three kinds of tests that are essential for developers: unit tests (which are
Line 18: the main topic of this book), integration tests and end-to-end tests. Because the object-oriented (OO)
Line 19: programming paradigm2 is dominant in the Java world, we will learn what role each of these tests
Line 20: plays in the testing of an OO system. Figure 1.1 presents a very simple abstraction of such a system.
Line 21: (We will get on to the meaning of "workers" and "managers" very soon.)
Line 22: Figure 1.1. An OO system abstraction
Line 23: 1Alas, even though some terms seem to have a well-established meaning, they still often get to be misused.
Line 24: 2See http://en.wikipedia.org/wiki/Object-oriented_programming for more information.
Line 25: 2
Line 26: 
Line 27: --- 페이지 18 ---
Line 28: Chapter 1. On Tests and Tools
Line 29: Yes, that is it! A bunch of circles and arrows. Circles are objects, arrows are messages being passed
Line 30: between them. As you can see, we also have a client in this picture, and his action (his request) has
Line 31: initiated a great deal of activity in our OO system. Why so many objects, and so many messages,
Line 32: out there? Why couldn’t one smart object deal with the client’s request? Well, the inhabitants of
Line 33: an OO world have very limited knowledge, and only a small set of abilities. Each of them has very
Line 34: constrained functionality or, to put it another way, each of them cannot do much on its own. Thus they
Line 35: are forced to cooperate in order to achieve anything useful (from the user’s point of view). This results
Line 36: in the following way of acting:
Line 37: I am only a simple web controller, so I cannot fetch the data from the database for you.
Line 38: But I know a guy – call him UserDAO – that might help. So I will pass your request on
Line 39: to him. Ah! I have just remembered that UserDAO does not understand what an HTTP
Line 40: request is. I will extract the information he needs and pass it on to him. Let us wait now
Line 41: for his answer.
Line 42: — Anonymous Web Controller Anonymous Web Application (circa 2003)
Line 43: That is how it works. In fact, a lot of classes do nothing more than pass on messages, and maybe also
Line 44: transform them in some manner.
Line 45: If you think about it, there are not many workers (that is classes that do a real job) out there. At least,
Line 46: not many workers written by you. Object-relational mapping framework (ORM3)? You surely will
Line 47: not have written one. After all, why should you, when there are so many robust solutions around?
Line 48: Dependency-Injection container (DI4)? Not likely. Logging framework? No. If you think about the
Line 49: amount of real business logic in your application you might be surprised how little there is. Of course,
Line 50: you do have some business logic. That is why your customer placed an order for a new application.
Line 51: But you probably used a lot of ready-to-be-used elements that do a lot of work for you. And that is
Line 52: fine, because code reuse is a fantastic way to build applications fast, allowing you to concentrate
Line 53: exclusively on the custom-designed elements. But if so, then quite probably many of your classes
Line 54: are only tying things together by passing appropriate messages to appropriate collaborators. They
Line 55: coordinate the work of others. We will call such classes managers. Their work is substantially
Line 56: different from what workers do.
Line 57: As you will soon see, this difference has a serious impact on testing.
Line 58: 1.2. Types of Developers' Tests
Line 59: Having the picture of an OO system in mind, we can try to visualize the parts of the system affected
Line 60: by each type of test. This will help us to understand the scope and purpose of each kind of developers’
Line 61: test.
Line 62: But before we proceed, let me introduce two important terms that will be used throughout the book:
Line 63: SUT and DOC. Both were popularized by [meszaros2007] and are used frequently when discussing
Line 64: testing issues.
Line 65: By SUT, or System Under Test, we understand the part of the system being tested. Depending on the
Line 66: type of test, SUT may be of very different granularity – from a single class to a whole application.
Line 67: A DOC, or Depended On Component, is any entity that is required by an SUT to fulfill its duties.
Line 68: 3See http://en.wikipedia.org/wiki/Object-relational_mapping
Line 69: 4See http://en.wikipedia.org/wiki/Dependency_injection
Line 70: 3
Line 71: 
Line 72: --- 페이지 19 ---
Line 73: Chapter 1. On Tests and Tools
Line 74: Usually a DOC is of the same granularity as the SUT, e.g. if the SUT is a class, then it uses other
Line 75: classes, if it is a module, then it collaborates with other modules.
Line 76: I will be using the terms "DOCs" and "collaborators" interchangeably.
Line 77: The following sections will introduce very briefly the various kinds of test. Much more could be said
Line 78: about each of them, but right now let us stick to the picture of the OO system and just try to see which
Line 79: part of it is covered by each kind of test.
Line 80: 1.2.1. Unit Tests
Line 81: Unit tests focus on single classes. They exist to make sure that your code works. They control all
Line 82: aspects of the context in which the class to be tested is executed, by replacing real collaborators with
Line 83: test doubles5. They know nothing about the users of the system they put to the test, and are unaware of
Line 84: layers, external systems and resources. They run incredibly quickly, and are executed frequently.
Line 85: This is shown in Figure 1.2, where only one object is clearly visible and all other elements of the
Line 86: system are greyed out. The single visible element is an SUT - the object to be tested. The greyed out
Line 87: elements symbolize those parts of the system not touched fully by the test, or replaced by various test
Line 88: doubles. Horizontal lines represent borders of layers (e.g. view, services, DAO layers). As the picture
Line 89: shows, a unit test is located inside one layer.
Line 90: Figure 1.2. Scope of a unit test
Line 91: Not every test run with a unit testing framework is a unit test! Make sure that your unit
Line 92: tests conform to the definition presented in Section 2.1!
Line 93: 1.2.2. Integration Tests
Line 94: Integration tests focus on the proper integration of different modules of your code, including - and this
Line 95: is especially valuable - with code over which you have no control. An example might be a connection
Line 96: 5Test doubles are fake replacements of real parts of the system (e.g. classes or modules). This topic will be discussed in detail in
Line 97: Chapter 5, Mocks, Stubs, and Dummies.
Line 98: 4
Line 99: 
Line 100: --- 페이지 20 ---
Line 101: Chapter 1. On Tests and Tools
Line 102: between your business classes and an OSGi container, ORM framework or with a web services
Line 103: framework. Even though the integration tests cover a much wider area of code than unit tests, they
Line 104: still test code as it looks from the developer’s standpoint.
Line 105: Integration tests run much more slowly than unit tests. They usually require some resources (e.g. an
Line 106: application context) to be set up before they can be executed, and their execution involves calling
Line 107: some entities that tend to respond slowly (e.g. databases, file system or web services). In order to
Line 108: verify the results of integration tests, it is often necessary to look into external resources (e.g. issue an
Line 109: SQL query).
Line 110: Figure 1.3. Scope of an integration test
Line 111: As Figure 1.3 shows, integration tests usually extend across a few layers (e.g. when testing whether
Line 112: your services work correctly with a DAO layer). They execute code written by your team, but also
Line 113: code from third-party libraries used by the tested application. As with unit tests, vast areas of the
Line 114: system are either not touched by integration tests or are replaced by test doubles. Integration tests
Line 115: usually do not touch the user interface (the GUI). Because of this, the client (user of the system) is not
Line 116: shown in the picture.
Line 117: 1.2.3. End-to-End Tests
Line 118: End-to-end tests exist to verify that your code works from the client’s point of view. They put the
Line 119: system as a whole to the test, mimicking the way the user would use it. As such they extend across all
Line 120: layers. Test doubles are rarely used in end-to-end tests – the point is to test the real system. End-to-end
Line 121: tests usually require a significant amount of time to execute themselves.
Line 122: 5
Line 123: 
Line 124: --- 페이지 21 ---
Line 125: Chapter 1. On Tests and Tools
Line 126: Figure 1.4. Scope of an end-to-end test
Line 127: Figure 1.4 shows an end-to-end test that puts to the test elements from all layers - from the front end
Line 128: (GUI, web services layer or any other external API of the tested system) to the storage layers (e.g.
Line 129: database storage). End-to-end tests are initiated through a request identical to those issued by real
Line 130: users of the system (e.g. clicks on GUI elements).
Line 131: 1.2.4. Examples
Line 132: Table 1.1. Types of test example
Line 133: type of test
Line 134: test examples
Line 135: unit test
Line 136: • An object of the class FootballPlayer should change its status to fired
Line 137: after receiving a second yellow card.
Line 138: • A constructor of the class Product should throw an
Line 139: IllegalArgumentException (with meaningful message) if the price
Line 140: argument is less than 0.
Line 141: integration
Line 142: test
Line 143: • An invocation of deleteAccount() method of the class UserService with
Line 144: an argument ID of value 1 should result in removal of the account with this ID
Line 145: from the database.
Line 146: • When asked for an item with ID = 5 for a second time, the ItemDAO class
Line 147: should not touch the real database, but fetch the requested item from the cache
Line 148: instead.
Line 149: • ParcelService should communicate with some web service, in order to find
Line 150: the parcel’s details, and send an email with the appropriate error information
Line 151: (using EmailService), if the parcel is not found.
Line 152: 6
Line 153: 
Line 154: --- 페이지 22 ---
Line 155: Chapter 1. On Tests and Tools
Line 156: type of test
Line 157: test examples
Line 158: end-to-end
Line 159: test
Line 160: • A logged on user can add comments to any public picture by clicking on the
Line 161: “add comment” button next to it. Guest users (users not logged on) can see
Line 162: this comment after it is published, but cannot post their own comments.
Line 163: • When a shop owner adds a new product to his shop using an Add Product
Line 164: form, it will be possible to locate this product using a Search Form by
Line 165: entering its name in the search field.
Line 166: • When a user sends his/her geo-location data using a whatCityIsThis web
Line 167: service, the system should respond with a city name.
Line 168: Table 1.2 presents examples of SUTs and DOCs for each type of test. It shows how SUTs and DOCs
Line 169: "grow" when moving from unit tests (smaller), via integration tests (medium), to end-to-end tests
Line 170: (large). The difference in granularity is clearly visible. In the case of unit tests, the SUTs and DOCs
Line 171: are simply classes. Integration tests act at the level of modules or layers. In the case of end-to-end
Line 172: tests, it is the whole application that is tested (making the application itself into an SUT), and other
Line 173: applications are collaborators (DOCs).
Line 174: Table 1.2. Examples of SUT and DOC
Line 175: type of test
Line 176: SUT example
Line 177: DOC example
Line 178: UserService
Line 179: UserDAO
Line 180: Invoice
Line 181: Product
Line 182: unit test
Line 183: Client
Line 184: Account
Line 185: DAO layer (ORM based)
Line 186: Hibernate
Line 187: DAO layer (JDBC based)
Line 188: MySQL 5
Line 189: integration test
Line 190: FullTextIndexer module
Line 191: FileStorage module
Line 192: External web service(s)
Line 193: end-to-end test
Line 194: Whole application
Line 195: LDAP repository
Line 196: 1.2.5. Conclusions
Line 197: All of the types of test presented in the preceding sections are important. From the point of view of a
Line 198: development team, each of them will have its own value. Unit tests help to ensure high-quality code,
Line 199: integration tests verify that different modules are cooperating effectively, while end-to-end tests put
Line 200: the system through its paces in ways that reflect the standpoint of users. Depending on the type of
Line 201: application you are implementing, some of them may be more suitable than others.
Line 202: Another way to think about the various types of test is to place them on an scale. At one end
Line 203: of this scale are unit tests, whose role is just to check whether we are implementing a given
Line 204: system correctly. At the other are end-to-end tests, whose main purpose is to verify that we are
Line 205: implementing the right system. Integration tests lie somewhere between.
Line 206: This book concentrates on unit tests, only to a very limited extent touching on other kinds of test.
Line 207: However, it is very important to be aware of their existence, and not to rely solely on unit tests. Unit
Line 208: tests are the foundation of developers’ tests, but rarely are they sufficient in themselves. Please bear
Line 209: this in mind as you learn about unit tests.
Line 210: 7
Line 211: 
Line 212: --- 페이지 23 ---
Line 213: Chapter 1. On Tests and Tools
Line 214: So which tests should you write for your application? Alas, there is no easy answer to
Line 215: this question. No golden rule exists, which would describe the right proportion of tests of
Line 216: different kinds. It depends to a very high degree on the type of application you are writing.
Line 217: 1.3. Verification and Design
Line 218: The continuum of testing approaches falls between two opposing beliefs. I will introduce both
Line 219: extremities to make the distinction clear.
Line 220: Some people (I will call them verifiers for convenience) want to check that their code works. That
Line 221: is their goal – to make sure it does what it should do. In the case of code that is hard to test, they
Line 222: will resort to any available techniques to be able to test it. They will sacrifice some OO rules if
Line 223: they believe that is what they need to do to achieve their Holy Grail of testability. They will modify
Line 224: method visibility using reflection or use classloading hacks to deal with final classes. In this way they
Line 225: are able to test just about anything, including tons of nightmarish legacy6 code. When accused of
Line 226: using "dirty hacks", they shrug their shoulders, and reply that they "don’t feel dirty if they are already
Line 227: swimming in mud".
Line 228: The other group – let us call them designers – believe that following OO rules is the most important
Line 229: thing, and that it leads to easily testable code. They treat tests as an indicator of code health. Easy-
Line 230: to-write tests denote sound code. Difficulties encountered during test-writing indicate problems in
Line 231: the code, and are treated as a clear sign that the code should be reworked. They tend to write tests
Line 232: using the same techniques as they use for production code, and renounce the use of reflection or
Line 233: classloading hacks. Designers particularly like the TDD approach, which guarantees a certain level of
Line 234: code quality. In the case of legacy code they will tend to refactor (or rather rewrite) it in order to make
Line 235: it more testable.
Line 236: As you can see, the conflict between these two approaches could never be resolved. The proponents
Line 237: hold different views, have different needs and value different things. Both also have some good
Line 238: examples to "prove" their superiority. The following paraphrase of a discussion on StackOverflow7
Line 239: shows the difference between these two worlds:
Line 240: - Reflection is the best way to test private methods.
Line 241: - Yes, you should reflect on your design!
Line 242: — Stack Overflow discussion (paraphrased)
Line 243: This distinction is also visible if you examine the features offered by different testing tools that are
Line 244: available. Some of them (e.g. JMockit and Powermock) are there to test the untestable, by giving you
Line 245: the power to mock static classes, final classes and constructors, or to call private methods. Others
Line 246: avoid using any such hacks. For example JUnit has never introduced any feature that would make
Line 247: testing of private methods easier, even though many have requested such a thing since JUnit’s early
Line 248: days.
Line 249: The terms designer and verificator have been introduced to stress a significant difference
Line 250: in how one may approach testing. However, I know no one who would be 100% a designer
Line 251: or 100% a verificator. We all fall somewhere in between.
Line 252: 6By legacy code I mean any code without tests (i.e. unit tests).
Line 253: 7http://stackoverflow.com
Line 254: 8
Line 255: 
Line 256: --- 페이지 24 ---
Line 257: Chapter 1. On Tests and Tools
Line 258: I’m inclined to position myself closer to designers – I share their concern for good design. This has an
Line 259: obvious impact on the tools and testing techniques I use.
Line 260: 1.4. But Should Developers Test Their
Line 261: Own Code?!
Line 262: Probably you have heard, many times over, that you (a developer) should not test your own code.
Line 263: Many reasons are given in support of this claim, but two of them seem to stand out as being the
Line 264: strongest and most commonly used:
Line 265: • developers lack testing skills,
Line 266: • you should not be your own judge.
Line 267: Let us be clear about this. Both of them are well-reasoned and, without a doubt, both emerged on the
Line 268: basis of the real – and no doubt sad – experiences of many development teams. They should not be
Line 269: dismissed too easily. Yet I am convinced that this "common knowledge" about testing reflects a kind
Line 270: of misunderstanding – or maybe, rather, a general failure to appreciate the multifariousness of the
Line 271: characteristics and purposes of testing.
Line 272: If we are talking about final tests before shipping software to customers, then I believe that in general
Line 273: such tests should be executed by professional testers. I would agree that no developer can click
Line 274: through the GUI and be as aggressive and inquisitive as an experienced tester. But those are not the
Line 275: only tests out there! There are many valuable tests that can, and should, be performed by developers
Line 276: themselves.
Line 277: What is more, some software is not easily testable by anyone other than developers
Line 278: themselves! Think about all those back-end solutions. No GUI, no decent entry points, a
Line 279: (sometimes) strong relation to architectural (hardware) aspects of the environment, etc.
Line 280: Checking software from the customer’s point of view is crucial, but this is only a single piece of a
Line 281: larger puzzle. Before you can do that, a development team must provide you with software. And
Line 282: if they do not perform their own tests – developers’ tests – they will probably furnish you with
Line 283: something of low quality. Developers’ tests increase the quality of the product delivered to the
Line 284: customer, but also that of the codebase, which means a great deal for any development team. This is
Line 285: not something to be disdained. The more trust a development team has (and the more pride it takes!)
Line 286: in its code, the better the results it will achieve. Developers’ tests help a team to gain confidence and
Line 287: proceed further without being hampered by too much self-doubt.
Line 288: Also, catching bugs early on (greatly) reduces cost, and shortens the time of repair. The more bugs
Line 289: you find early on, the less they will cost you. This well-known time-to-cost ratio is shown in Figure
Line 290: 1.5.
Line 291: 9
Line 292: 
Line 293: --- 페이지 25 ---
Line 294: Chapter 1. On Tests and Tools
Line 295: Figure 1.5. The cost of bug fixing
Line 296: Developers’ tests are the first line of defense against bugs. They kill them as soon as they appear. Of
Line 297: course, for the reasons mentioned at the beginning of this section, some bugs will probably make it
Line 298: through. Well, yes, it might just happen! That is why other lines of defense have to be in place, too:
Line 299: i.e. highly skilled, specialized testers. Hopefully they will hunt down all the remaining bugs8.
Line 300: In fact, many companies rely (almost) solely on developers’ tests. Big names – like
Line 301: Facebook or WordPress – adopt a continuous deployment approach, which can be
Line 302: summarized as "if it has passed the automatic tests it goes into production". No human
Line 303: testing involved! So it is possible after all, isn’t it?
Line 304: So, should developers tests their own code? Oh yes, they should!
Line 305: …and if you disagree, please stop reading now.
Line 306: 1.5. Tools Introduction
Line 307: Use the right tool for the job.
Line 308: — Andrew Hunt and David Thomas The Pragmatic Programmer: From Journeyman
Line 309: to Master (1999)
Line 310: This section introduces the tools that I will be using for the writing and execution of tests. It relates
Line 311: to our recent discussion about the different approaches to testing (see Section 1.3). These different
Line 312: approaches are responsible for the existence of many tools covering (almost) identical problem areas.
Line 313: Take, for example, mocking frameworks. Do we really need so many of them? The answer is "yes",
Line 314: and the reason is that each mocking framework is slightly different, and facilitates a slightly different
Line 315: approach to writing test doubles. This is also true for other groups of tools – from test frameworks to
Line 316: IDEs.
Line 317: In general, tools for testing are very simple to use. That is good news, isn’t it? But be warned – there
Line 318: is a catch! This deceptive ease of use leads many developers to assume that they know how to test,
Line 319: just because they can use testing tools – i.e. they are able to write a few lines of JUnit code. This
Line 320: is plainly wrong. Tools can be used mindlessly, or they can be used by a skilled hand. They can
Line 321: 8We will discuss this topic some more in Section A.1.
Line 322: 10
Line 323: 
Line 324: --- 페이지 26 ---
Line 325: Chapter 1. On Tests and Tools
Line 326: dominate you or they can become your obedient servants. The point is to grasp the ‘why’ and the
Line 327: ‘what for’, so that you know when to use (or not use) them.
Line 328: Throughout this book I will be stressing the importance of the ideas embodied in certain tools. If
Line 329: you get a good grasp of those ideas, you will be able to follow them with almost any tool. If you
Line 330: concentrate on tools, you will soon need to relearn all that was dear to you. Ideas are everlasting9, but
Line 331: tools are there only for a short period of time.
Line 332: Let me introduce my friends now. There are a few of them, but we will mostly use just three: JUnit,
Line 333: AssertJ and Mockito. The remainder will only play a secondary role.
Line 334: And what if your choices are different, and you use different tools? It is not a problem.
Line 335: Nowadays tools are very similar. They have evolved along different paths, but have also
Line 336: influenced one another, and have often ended up in the proximity of their competitors,
Line 337: with similar sets of features. Using any modern tools you can achieve similar results
Line 338: and still utilize the techniques presented in this book. The ones I have selected are my
Line 339: personal favourites, and have been chosen with great deliberation. I suspect that some of
Line 340: the techniques presented in the book may be easier to master using them than they would
Line 341: be using any other tools. The only risk for you is that you, too, may end up convinced of
Line 342: their superiority, so that you then add some new toys to your toolbox. This doesn’t sound
Line 343: so bad, does it?
Line 344: Testing Framework: JUnit
Line 345: JUnit (http://junit.org) is an open-source testing framework for Java. It was created by Kent Beck
Line 346: around 1997, and since that time has been, de facto, the standard testing tool for Java developers.
Line 347: It is supported by all IDEs (Eclipse, IntelliJ IDEA), build tools (Maven, Gradle) and by popular
Line 348: frameworks (e.g. Spring). JUnit has a wide community of users, and is supplemented by a range of
Line 349: interesting extension projects. It was built especially for unit testing, but is also widely used for other
Line 350: kinds of test.
Line 351: I used version 5.3.1 of JUnit when writing this book.
Line 352: Mock Library: Mockito
Line 353: Mockito (http://mockito.org) since few years is the mocking framework for the Java world. It was
Line 354: born in Q4 2007 (Szczepan Faber being the proud father) and has quickly matured into a top-quality
Line 355: product. It is being actively developed, has great documentation and a thriving community. It offers
Line 356: complete control over the mocking process, and "lets you write beautiful tests with clean & simple
Line 357: API". + Originally, Mockito was derived from Easymock, but has evolved substantially, and now
Line 358: differs in many respects from its predecessor.
Line 359: I used version 2.23.0 of Mockito when writing this book.
Line 360: Fluent Assertions: AssertJ
Line 361: In order to make tests more readable and easier to maintain, I have used the AssertJ (https://joel-
Line 362: costigliola.github.io/assertj/) version 3.11.1.
Line 363: 9Or rather, they live as long as the paradigm they belong to does.
Line 364: 11
Line 365: 
Line 366: --- 페이지 27 ---
Line 367: Chapter 1. On Tests and Tools
Line 368: Other Tools
Line 369: It would be simplistic to say that everything other than the testing framework and mock library plays a
Line 370: secondary role. If you master writing unit tests, you will find good uses for many more tools. Here are
Line 371: my choices.
Line 372: Code Coverage: Cobertura
Line 373: Among code coverage tools there are a few interesting ones, my personal choice being Cobertura
Line 374: (http://cobertura.sourceforge.net). It works well with all build tools, IDEs, and continuous integration
Line 375: servers.
Line 376: I used version 1.9.4.1 of Cobertura when writing this book.
Line 377: PowerMock - mocking without limits
Line 378: Even though Mockito is the mocking framework used within the book, in some situations it might be
Line 379: worthwhile to take a look at the other options. Powermock (http://code.google.com/p/powermock/)
Line 380: offers some powerful features (i.e. mocking of static methods), which we will use once, just in order
Line 381: to be able to demonstrate and discuss an alternative approach to testing.
Line 382: Mutation Testing: PIT
Line 383: PIT Mutation Testing (http://pitest.org) is "a fast bytecode based mutation testing system for Java that
Line 384: makes it possible to test the effectiveness of your unit tests." It works with Java 5 and JUnit 4.6 (and
Line 385: above).
Line 386: I used version 1.4.3 of PIT when writing this book.
Line 387: Testing Asynchronous Code: Awaitility
Line 388: Awaitility (http://www.awaitility.org/) "is a DSL that allows you to express expectations of an
Line 389: asynchronous system in a concise and easy to read manner.".
Line 390: I used version 1.7.0 of Awaitility when writing this book.
Line 391: Build Tools: Gradle and Maven
Line 392:   Unit tests are usually included within the build process, which means they are run by a build tool. In
Line 393: this book I present how to run tests using Maven (http://maven.org) and Gradle (http://gradle.org).
Line 394: IDEs: IntelliJ IDEA and Eclipse
Line 395: Even though IDE is THE tool in your toolbox, we will not devote a lot of time to it. All we need to
Line 396: know is how to use an IDE to execute unit tests. I decided to discuss it with reference to two very
Line 397: popular IDEs: Eclipse (http://eclipse.org) and IntelliJ IDEA (http://www.jetbrains.com/idea). 
Line 398: 12