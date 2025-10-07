Line 1: 
Line 2: --- 페이지 42 ---
Line 3: 20
Line 4: What is a unit test?
Line 5: As mentioned in chapter 1, there are a surprising number of nuances in the defini-
Line 6: tion of a unit test. Those nuances are more important than you might think—so
Line 7: much so that the differences in interpreting them have led to two distinct views on
Line 8: how to approach unit testing.
Line 9:  These views are known as the classical and the London schools of unit testing.
Line 10: The classical school is called “classical” because it’s how everyone originally
Line 11: approached unit testing and test-driven development. The London school takes
Line 12: root in the programming community in London. The discussion in this chapter
Line 13: about the differences between the classical and London styles lays the foundation
Line 14: for chapter 5, where I cover the topic of mocks and test fragility in detail.
Line 15: This chapter covers
Line 16: What a unit test is
Line 17: The differences between shared, private, 
Line 18: and volatile dependencies
Line 19: The two schools of unit testing: classical 
Line 20: and London
Line 21: The differences between unit, integration, 
Line 22: and end-to-end tests
Line 23: 
Line 24: --- 페이지 43 ---
Line 25: 21
Line 26: The definition of “unit test”
Line 27:  Let’s start by defining a unit test, with all due caveats and subtleties. This definition
Line 28: is the key to the difference between the classical and London schools.
Line 29: 2.1
Line 30: The definition of “unit test”
Line 31: There are a lot of definitions of a unit test. Stripped of their non-essential bits, the
Line 32: definitions all have the following three most important attributes. A unit test is an
Line 33: automated test that
Line 34: Verifies a small piece of code (also known as a unit),
Line 35: Does it quickly,
Line 36: And does it in an isolated manner.
Line 37: The first two attributes here are pretty non-controversial. There might be some dis-
Line 38: pute as to what exactly constitutes a fast unit test because it’s a highly subjective mea-
Line 39: sure. But overall, it’s not that important. If your test suite’s execution time is good
Line 40: enough for you, it means your tests are quick enough.
Line 41:  What people have vastly different opinions about is the third attribute. The isola-
Line 42: tion issue is the root of the differences between the classical and London schools of
Line 43: unit testing. As you will see in the next section, all other differences between the two
Line 44: schools flow naturally from this single disagreement on what exactly isolation means. I
Line 45: prefer the classical style for the reasons I describe in section 2.3.
Line 46: 2.1.1
Line 47: The isolation issue: The London take
Line 48: What does it mean to verify a piece of code—a unit—in an isolated manner? The Lon-
Line 49: don school describes it as isolating the system under test from its collaborators. It
Line 50: means if a class has a dependency on another class, or several classes, you need to
Line 51: replace all such dependencies with test doubles. This way, you can focus on the class
Line 52: under test exclusively by separating its behavior from any external influence.
Line 53:  
Line 54: The classical and London schools of unit testing
Line 55: The classical approach is also referred to as the Detroit and, sometimes, the classi-
Line 56: cist approach to unit testing. Probably the most canonical book on the classical
Line 57: school is the one by Kent Beck: Test-Driven Development: By Example (Addison-Wesley
Line 58: Professional, 2002).
Line 59: The London style is sometimes referred to as mockist. Although the term mockist is
Line 60: widespread, people who adhere to this style of unit testing generally don’t like it, so
Line 61: I call it the London style throughout this book. The most prominent proponents of this
Line 62: approach are Steve Freeman and Nat Pryce. I recommend their book, Growing Object-
Line 63: Oriented Software, Guided by Tests (Addison-Wesley Professional, 2009), as a good
Line 64: source on this subject.
Line 65: 
Line 66: --- 페이지 44 ---
Line 67: 22
Line 68: CHAPTER 2
Line 69: What is a unit test?
Line 70: DEFINITION
Line 71: A test double is an object that looks and behaves like its release-
Line 72: intended counterpart but is actually a simplified version that reduces the
Line 73: complexity and facilitates testing. This term was introduced by Gerard Mesza-
Line 74: ros in his book, xUnit Test Patterns: Refactoring Test Code (Addison-Wesley, 2007).
Line 75: The name itself comes from the notion of a stunt double in movies.
Line 76: Figure 2.1 shows how the isolation is usually achieved. A unit test that would otherwise
Line 77: verify the system under test along with all its dependencies now can do that separately
Line 78: from those dependencies.
Line 79: One benefit of this approach is that if the test fails, you know for sure which part of
Line 80: the code base is broken: it’s the system under test. There could be no other suspects,
Line 81: because all of the class’s neighbors are replaced with the test doubles.
Line 82:  Another benefit is the ability to split the object graph—the web of communicating
Line 83: classes solving the same problem. This web may become quite complicated: every class
Line 84: in it may have several immediate dependencies, each of which relies on dependencies
Line 85: of their own, and so on. Classes may even introduce circular dependencies, where the
Line 86: chain of dependency eventually comes back to where it started.
Line 87: Test double 2
Line 88: Dependency 1
Line 89: Dependency 2
Line 90: System under test
Line 91: System under test
Line 92: Test double 1
Line 93: Figure 2.1
Line 94: Replacing the dependencies 
Line 95: of the system under test with test 
Line 96: doubles allows you to focus on verifying 
Line 97: the system under test exclusively, as 
Line 98: well as split the otherwise large 
Line 99: interconnected object graph.
Line 100: 
Line 101: --- 페이지 45 ---
Line 102: 23
Line 103: The definition of “unit test”
Line 104:  Trying to test such an interconnected code base is hard without test doubles. Pretty
Line 105: much the only choice you are left with is re-creating the full object graph in the test,
Line 106: which might not be a feasible task if the number of classes in it is too high.
Line 107:  With test doubles, you can put a stop to this. You can substitute the immediate
Line 108: dependencies of a class; and, by extension, you don’t have to deal with the dependen-
Line 109: cies of those dependencies, and so on down the recursion path. You are effectively
Line 110: breaking up the graph—and that can significantly reduce the amount of preparations
Line 111: you have to do in a unit test.
Line 112:  And let’s not forget another small but pleasant side benefit of this approach to
Line 113: unit test isolation: it allows you to introduce a project-wide guideline of testing only
Line 114: one class at a time, which establishes a simple structure in the whole unit test suite.
Line 115: You no longer have to think much about how to cover your code base with tests.
Line 116: Have a class? Create a corresponding class with unit tests! Figure 2.2 shows how it
Line 117: usually looks.
Line 118: Let’s now look at some examples. Since the classical style probably looks more familiar
Line 119: to most people, I’ll show sample tests written in that style first and then rewrite them
Line 120: using the London approach.
Line 121:  Let’s say that we operate an online store. There’s just one simple use case in our
Line 122: sample application: a customer can purchase a product. When there’s enough inven-
Line 123: tory in the store, the purchase is deemed to be successful, and the amount of the
Line 124: product in the store is reduced by the purchase’s amount. If there’s not enough prod-
Line 125: uct, the purchase is not successful, and nothing happens in the store.
Line 126:  Listing 2.1 shows two tests verifying that a purchase succeeds only when there’s
Line 127: enough inventory in the store. The tests are written in the classical style and use the
Line 128: Class 1
Line 129: Class 2
Line 130: Class 3
Line 131: Unit tests
Line 132: Production code
Line 133: Class 1 Tests
Line 134: Class 2 Tests
Line 135: Class 3 Tests
Line 136: Figure 2.2
Line 137: Isolating the class under test from its dependencies helps establish a simple 
Line 138: test suite structure: one class with tests for each class in the production code.
Line 139: 
Line 140: --- 페이지 46 ---
Line 141: 24
Line 142: CHAPTER 2
Line 143: What is a unit test?
Line 144: typical three-phase sequence: arrange, act, and assert (AAA for short—I talk more
Line 145: about this sequence in chapter 3).
Line 146: [Fact]
Line 147: public void Purchase_succeeds_when_enough_inventory()
Line 148: {
Line 149: // Arrange
Line 150: var store = new Store();
Line 151: store.AddInventory(Product.Shampoo, 10);
Line 152: var customer = new Customer();
Line 153: // Act
Line 154: bool success = customer.Purchase(store, Product.Shampoo, 5);
Line 155: // Assert
Line 156: Assert.True(success);
Line 157: Assert.Equal(5, store.GetInventory(Product.Shampoo));   
Line 158: }
Line 159: [Fact]
Line 160: public void Purchase_fails_when_not_enough_inventory()
Line 161: {
Line 162: // Arrange
Line 163: var store = new Store();
Line 164: store.AddInventory(Product.Shampoo, 10);
Line 165: var customer = new Customer();
Line 166: // Act
Line 167: bool success = customer.Purchase(store, Product.Shampoo, 15);
Line 168: // Assert
Line 169: Assert.False(success);
Line 170: Assert.Equal(10, store.GetInventory(Product.Shampoo));   
Line 171: }
Line 172: public enum Product
Line 173: {
Line 174: Shampoo,
Line 175: Book
Line 176: }
Line 177: As you can see, the arrange part is where the tests make ready all dependencies and
Line 178: the system under test. The call to customer.Purchase() is the act phase, where you
Line 179: exercise the behavior you want to verify. The assert statements are the verification
Line 180: stage, where you check to see if the behavior led to the expected results.
Line 181:  During the arrange phase, the tests put together two kinds of objects: the system
Line 182: under test (SUT) and one collaborator. In this case, Customer is the SUT and Store is
Line 183: the collaborator. We need the collaborator for two reasons:
Line 184: Listing 2.1
Line 185: Tests written using the classical style of unit testing
Line 186: Reduces the 
Line 187: product amount in 
Line 188: the store by five
Line 189: The product 
Line 190: amount in the 
Line 191: store remains 
Line 192: unchanged.
Line 193: 
Line 194: --- 페이지 47 ---
Line 195: 25
Line 196: The definition of “unit test”
Line 197: To get the method under test to compile, because customer.Purchase() requires
Line 198: a Store instance as an argument
Line 199: For the assertion phase, since one of the results of customer.Purchase() is a
Line 200: potential decrease in the product amount in the store 
Line 201: Product.Shampoo and the numbers 5 and 15 are constants.
Line 202: DEFINITION
Line 203: A method under test (MUT) is a method in the SUT called by the
Line 204: test. The terms MUT and SUT are often used as synonyms, but normally, MUT
Line 205: refers to a method while SUT refers to the whole class.
Line 206: This code is an example of the classical style of unit testing: the test doesn’t replace
Line 207: the collaborator (the Store class) but rather uses a production-ready instance of it.
Line 208: One of the natural outcomes of this style is that the test now effectively verifies both
Line 209: Customer and Store, not just Customer. Any bug in the inner workings of Store that
Line 210: affects Customer will lead to failing these unit tests, even if Customer still works cor-
Line 211: rectly. The two classes are not isolated from each other in the tests.
Line 212:  Let’s now modify the example toward the London style. I’ll take the same tests and
Line 213: replace the Store instances with test doubles—specifically, mocks.
Line 214:  I use Moq (https://github.com/moq/moq4) as the mocking framework, but you
Line 215: can find several equally good alternatives, such as NSubstitute (https://github.com/
Line 216: nsubstitute/NSubstitute). All object-oriented languages have analogous frameworks.
Line 217: For instance, in the Java world, you can use Mockito, JMock, or EasyMock.
Line 218: DEFINITION
Line 219: A mock is a special kind of test double that allows you to examine
Line 220: interactions between the system under test and its collaborators.
Line 221: We’ll get back to the topic of mocks, stubs, and the differences between them in later
Line 222: chapters. For now, the main thing to remember is that mocks are a subset of test dou-
Line 223: bles. People often use the terms test double and mock as synonyms, but technically, they
Line 224: are not (more on this in chapter 5):
Line 225: Test double is an overarching term that describes all kinds of non-production-
Line 226: ready, fake dependencies in a test.
Line 227: Mock is just one kind of such dependencies.
Line 228: The next listing shows how the tests look after isolating Customer from its collabora-
Line 229: tor, Store.
Line 230: [Fact]
Line 231: public void Purchase_succeeds_when_enough_inventory()
Line 232: {
Line 233: // Arrange
Line 234: var storeMock = new Mock<IStore>();
Line 235: storeMock
Line 236: Listing 2.2
Line 237: Tests written using the London style of unit testing
Line 238: 
Line 239: --- 페이지 48 ---
Line 240: 26
Line 241: CHAPTER 2
Line 242: What is a unit test?
Line 243: .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
Line 244: .Returns(true);
Line 245: var customer = new Customer();
Line 246: // Act
Line 247: bool success = customer.Purchase(
Line 248: storeMock.Object, Product.Shampoo, 5);
Line 249: // Assert
Line 250: Assert.True(success);
Line 251: storeMock.Verify(
Line 252: x => x.RemoveInventory(Product.Shampoo, 5),
Line 253: Times.Once);
Line 254: }
Line 255: [Fact]
Line 256: public void Purchase_fails_when_not_enough_inventory()
Line 257: {
Line 258: // Arrange
Line 259: var storeMock = new Mock<IStore>();
Line 260: storeMock
Line 261: .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
Line 262: .Returns(false);
Line 263: var customer = new Customer();
Line 264: // Act
Line 265: bool success = customer.Purchase(
Line 266: storeMock.Object, Product.Shampoo, 5);
Line 267: // Assert
Line 268: Assert.False(success);
Line 269: storeMock.Verify(
Line 270: x => x.RemoveInventory(Product.Shampoo, 5),
Line 271: Times.Never);
Line 272: }
Line 273: Note how different these tests are from those written in the classical style. In the
Line 274: arrange phase, the tests no longer instantiate a production-ready instance of Store
Line 275: but instead create a substitution for it, using Moq’s built-in class Mock<T>.
Line 276:  Furthermore, instead of modifying the state of Store by adding a shampoo inven-
Line 277: tory to it, we directly tell the mock how to respond to calls to HasEnoughInventory().
Line 278: The mock reacts to this request the way the tests need, regardless of the actual state of
Line 279: Store. In fact, the tests no longer use Store—we have introduced an IStore interface
Line 280: and are mocking that interface instead of the Store class.
Line 281:  In chapter 8, I write in detail about working with interfaces. For now, just make a
Line 282: note that interfaces are required for isolating the system under test from its collabora-
Line 283: tors. (You can also mock a concrete class, but that’s an anti-pattern; I cover this topic
Line 284: in chapter 11.)
Line 285: 
Line 286: --- 페이지 49 ---
Line 287: 27
Line 288: The definition of “unit test”
Line 289:  The assertion phase has changed too, and that’s where the key difference lies. We
Line 290: still check the output from customer.Purchase as before, but the way we verify that
Line 291: the customer did the right thing to the store is different. Previously, we did that by
Line 292: asserting against the store’s state. Now, we examine the interactions between Customer
Line 293: and Store: the tests check to see if the customer made the correct call on the store.
Line 294: We do this by passing the method the customer should call on the store (x.Remove-
Line 295: Inventory) as well as the number of times it should do that. If the purchases succeeds,
Line 296: the customer should call this method once (Times.Once). If the purchases fails, the
Line 297: customer shouldn’t call it at all (Times.Never). 
Line 298: 2.1.2
Line 299: The isolation issue: The classical take
Line 300: To reiterate, the London style approaches the isolation requirement by segregating the
Line 301: piece of code under test from its collaborators with the help of test doubles: specifically,
Line 302: mocks. Interestingly enough, this point of view also affects your standpoint on what con-
Line 303: stitutes a small piece of code (a unit). Here are all the attributes of a unit test once again:
Line 304: A unit test verifies a small piece of code (a unit),
Line 305: Does it quickly,
Line 306: And does it in an isolated manner.
Line 307: In addition to the third attribute leaving room for interpretation, there’s some room
Line 308: in the possible interpretations of the first attribute as well. How small should a small
Line 309: piece of code be? As you saw from the previous section, if you adopt the position of
Line 310: isolating every individual class, then it’s natural to accept that the piece of code under
Line 311: test should also be a single class, or a method inside that class. It can’t be more than
Line 312: that due to the way you approach the isolation issue. In some cases, you might test a
Line 313: couple of classes at once; but in general, you’ll always strive to maintain this guideline
Line 314: of unit testing one class at a time.
Line 315:  As I mentioned earlier, there’s another way to interpret the isolation attribute—
Line 316: the classical way. In the classical approach, it’s not the code that needs to be tested in
Line 317: an isolated manner. Instead, unit tests themselves should be run in isolation from
Line 318: each other. That way, you can run the tests in parallel, sequentially, and in any order,
Line 319: whatever fits you best, and they still won’t affect each other’s outcome.
Line 320:  Isolating tests from each other means it’s fine to exercise several classes at once as
Line 321: long as they all reside in the memory and don’t reach out to a shared state, through
Line 322: which the tests can communicate and affect each other’s execution context. Typical
Line 323: examples of such a shared state are out-of-process dependencies—the database, the
Line 324: file system, and so on.
Line 325:  For instance, one test could create a customer in the database as part of its arrange
Line 326: phase, and another test would delete it as part of its own arrange phase, before the
Line 327: first test completes executing. If you run these two tests in parallel, the first test will
Line 328: fail, not because the production code is broken, but rather because of the interfer-
Line 329: ence from the second test.
Line 330: 
Line 331: --- 페이지 50 ---
Line 332: 28
Line 333: CHAPTER 2
Line 334: What is a unit test?
Line 335: This take on the isolation issue entails a much more modest view on the use of mocks
Line 336: and other test doubles. You can still use them, but you normally do that for only those
Line 337: dependencies that introduce a shared state between tests. Figure 2.3 shows how it looks.
Line 338:  Note that shared dependencies are shared between unit tests, not between classes
Line 339: under test (units). In that sense, a singleton dependency is not shared as long as you
Line 340: are able to create a new instance of it in each test. While there’s only one instance of a
Line 341: Shared, private, and out-of-process dependencies 
Line 342: A shared dependency is a dependency that is shared between tests and provides
Line 343: means for those tests to affect each other’s outcome. A typical example of shared
Line 344: dependencies is a static mutable field. A change to such a field is visible across all
Line 345: unit tests running within the same process. A database is another typical example of
Line 346: a shared dependency.
Line 347: A private dependency is a dependency that is not shared.
Line 348: An out-of-process dependency is a dependency that runs outside the application’s
Line 349: execution process; it’s a proxy to data that is not yet in the memory. An out-of-process
Line 350: dependency corresponds to a shared dependency in the vast majority of cases, but
Line 351: not always. For example, a database is both out-of-process and shared. But if you
Line 352: launch that database in a Docker container before each test run, that would make
Line 353: this dependency out-of-process but not shared, since tests no longer work with the
Line 354: same instance of it. Similarly, a read-only database is also out-of-process but not
Line 355: shared, even if it’s reused by tests. Tests can’t mutate data in such a database and
Line 356: thus can’t affect each other’s outcome.
Line 357: Private dependency; keep
Line 358: Shared dependency; replace
Line 359: File system
Line 360: System under test
Line 361: Database
Line 362: Test
Line 363: Shared dependency; replace
Line 364: Another class
Line 365: Figure 2.3
Line 366: Isolating unit tests from each other entails isolating the class under test 
Line 367: from shared dependencies only. Private dependencies can be kept intact.
Line 368: 
Line 369: --- 페이지 51 ---
Line 370: 29
Line 371: The definition of “unit test”
Line 372: singleton in the production code, tests may very well not follow this pattern and not
Line 373: reuse that singleton. Thus, such a dependency would be private.
Line 374:  For example, there’s normally only one instance of a configuration class, which is
Line 375: reused across all production code. But if it’s injected into the SUT the way all other
Line 376: dependencies are, say, via a constructor, you can create a new instance of it in each
Line 377: test; you don’t have to maintain a single instance throughout the test suite. You can’t
Line 378: create a new file system or a database, however; they must be either shared between
Line 379: tests or substituted away with test doubles.
Line 380: Another reason for substituting shared dependencies is to increase the test execution
Line 381: speed. Shared dependencies almost always reside outside the execution process, while
Line 382: private dependencies usually don’t cross that boundary. Because of that, calls to
Line 383: shared dependencies, such as a database or the file system, take more time than calls
Line 384: to private dependencies. And since the necessity to run quickly is the second attribute
Line 385: of the unit test definition, such calls push the tests with shared dependencies out of
Line 386: the realm of unit testing and into the area of integration testing. I talk more about
Line 387: integration testing later in this chapter.
Line 388:  This alternative view of isolation also leads to a different take on what constitutes a
Line 389: unit (a small piece of code). A unit doesn’t necessarily have to be limited to a class.
Line 390: Shared vs. volatile dependencies 
Line 391: Another term has a similar, yet not identical, meaning: volatile dependency. I recom-
Line 392: mend Dependency Injection: Principles, Practices, Patterns by Steven van Deursen and
Line 393: Mark Seemann (Manning Publications, 2018) as a go-to book on the topic of depen-
Line 394: dency management.
Line 395: A volatile dependency is a dependency that exhibits one of the following properties:
Line 396: It introduces a requirement to set up and configure a runtime environment in
Line 397: addition to what is installed on a developer’s machine by default. Databases
Line 398: and API services are good examples here. They require additional setup and
Line 399: are not installed on machines in your organization by default.
Line 400: It contains nondeterministic behavior. An example would be a random num-
Line 401: ber generator or a class returning the current date and time. These depen-
Line 402: dencies are non-deterministic because they provide different results on each
Line 403: invocation.
Line 404: As you can see, there’s an overlap between the notions of shared and volatile depen-
Line 405: dencies. For example, a dependency on the database is both shared and volatile. But
Line 406: that’s not the case for the file system. The file system is not volatile because it is
Line 407: installed on every developer’s machine and it behaves deterministically in the vast
Line 408: majority of cases. Still, the file system introduces a means by which the unit tests
Line 409: can interfere with each other’s execution context; hence it is shared. Likewise, a ran-
Line 410: dom number generator is volatile, but because you can supply a separate instance
Line 411: of it to each test, it isn’t shared.
Line 412: 
Line 413: --- 페이지 52 ---
Line 414: 30
Line 415: CHAPTER 2
Line 416: What is a unit test?
Line 417: You can just as well unit test a group of classes, as long as none of them is a shared
Line 418: dependency. 
Line 419: 2.2
Line 420: The classical and London schools of unit testing
Line 421: As you can see, the root of the differences between the London and classical schools is
Line 422: the isolation attribute. The London school views it as isolation of the system under test
Line 423: from its collaborators, whereas the classical school views it as isolation of unit tests
Line 424: themselves from each other.
Line 425:  This seemingly minor difference has led to a vast disagreement about how to
Line 426: approach unit testing, which, as you already know, produced the two schools of thought.
Line 427: Overall, the disagreement between the schools spans three major topics:
Line 428: The isolation requirement
Line 429: What constitutes a piece of code under test (a unit)
Line 430: Handling dependencies
Line 431: Table 2.1 sums it all up.
Line 432: 2.2.1
Line 433: How the classical and London schools handle dependencies
Line 434: Note that despite the ubiquitous use of test doubles, the London school still allows
Line 435: for using some dependencies in tests as-is. The litmus test here is whether a depen-
Line 436: dency is mutable. It’s fine not to substitute objects that don’t ever change—
Line 437: immutable objects.
Line 438:  And you saw in the earlier examples that, when I refactored the tests toward the
Line 439: London style, I didn’t replace the Product instances with mocks but rather used
Line 440: the real objects, as shown in the following code (repeated from listing 2.2 for your
Line 441: convenience):
Line 442: [Fact]
Line 443: public void Purchase_fails_when_not_enough_inventory()
Line 444: {
Line 445: // Arrange
Line 446: var storeMock = new Mock<IStore>();
Line 447: storeMock
Line 448: .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
Line 449: .Returns(false);
Line 450: var customer = new Customer();
Line 451: Table 2.1
Line 452: The differences between the London and classical schools of unit testing, summed up by the
Line 453: approach to isolation, the size of a unit, and the use of test doubles
Line 454: Isolation of
Line 455: A unit is
Line 456: Uses test doubles for
Line 457: London school
Line 458: Units
Line 459: A class
Line 460: All but immutable dependencies
Line 461: Classical school
Line 462: Unit tests
Line 463: A class or a set of classes
Line 464: Shared dependencies
Line 465: 
Line 466: --- 페이지 53 ---
Line 467: 31
Line 468: The classical and London schools of unit testing
Line 469: // Act
Line 470: bool success = customer.Purchase(storeMock.Object, Product.Shampoo, 5);
Line 471: // Assert
Line 472: Assert.False(success);
Line 473: storeMock.Verify(
Line 474: x => x.RemoveInventory(Product.Shampoo, 5),
Line 475: Times.Never);
Line 476: }
Line 477: Of the two dependencies of Customer, only Store contains an internal state that can
Line 478: change over time. The Product instances are immutable (Product itself is a C#
Line 479: enum). Hence I substituted the Store instance only.
Line 480:  It makes sense, if you think about it. You wouldn’t use a test double for the 5
Line 481: number in the previous test either, would you? That’s because it is also immutable—
Line 482: you can’t possibly modify this number. Note that I’m not talking about a variable
Line 483: containing the number, but rather the number itself. In the statement Remove-
Line 484: Inventory(Product.Shampoo, 5), we don’t even use a variable; 5 is declared right
Line 485: away. The same is true for Product.Shampoo.
Line 486:  Such immutable objects are called value objects or values. Their main trait is that
Line 487: they have no individual identity; they are identified solely by their content. As a corol-
Line 488: lary, if two such objects have the same content, it doesn’t matter which of them you’re
Line 489: working with: these instances are interchangeable. For example, if you’ve got two 5
Line 490: integers, you can use them in place of one another. The same is true for the products
Line 491: in our case: you can reuse a single Product.Shampoo instance or declare several of
Line 492: them—it won’t make any difference. These instances will have the same content and
Line 493: thus can be used interchangeably.
Line 494:  Note that the concept of a value object is language-agnostic and doesn’t require a
Line 495: particular programming language or framework. You can read more about value
Line 496: objects in my article “Entity vs. Value Object: The ultimate list of differences” at
Line 497: http://mng.bz/KE9O.
Line 498:  Figure 2.4 shows the categorization of dependencies and how both schools of unit
Line 499: testing treat them. A dependency can be either shared or private. A private dependency, in
Line 500: turn, can be either mutable or immutable. In the latter case, it is called a value object. For
Line 501: example, a database is a shared dependency—its internal state is shared across all
Line 502: automated tests (that don’t replace it with a test double). A Store instance is a private
Line 503: dependency that is mutable. And a Product instance (or an instance of a number 5,
Line 504: for that matter) is an example of a private dependency that is immutable—a value
Line 505: object. All shared dependencies are mutable, but for a mutable dependency to be
Line 506: shared, it has to be reused by tests.
Line 507:  
Line 508:  
Line 509:  
Line 510:  
Line 511: 
Line 512: --- 페이지 54 ---
Line 513: 32
Line 514: CHAPTER 2
Line 515: What is a unit test?
Line 516: I’m repeating table 2.1 with the differences between the schools for your convenience.
Line 517: Isolation of
Line 518: A unit is
Line 519: Uses test doubles for
Line 520: London school
Line 521: Units
Line 522: A class
Line 523: All but immutable dependencies
Line 524: Classical school
Line 525: Unit tests
Line 526: A class or a set of classes
Line 527: Shared dependencies
Line 528: Collaborator vs. dependency
Line 529: A collaborator is a dependency that is either shared or mutable. For example, a class
Line 530: providing access to the database is a collaborator since the database is a shared
Line 531: dependency. Store is a collaborator too, because its state can change over time.
Line 532: Product and number 5 are also dependencies, but they’re not collaborators. They’re
Line 533: values or value objects.
Line 534: A typical class may work with dependencies of both types: collaborators and values.
Line 535: Look at this method call:
Line 536: customer.Purchase(store, Product.Shampoo, 5)
Line 537: Here we have three dependencies. One of them (store) is a collaborator, and the
Line 538: other two (Product.Shampoo, 5) are not.
Line 539: Private
Line 540: Value object
Line 541: Mutable
Line 542: Collaborator,
Line 543: replaced in the
Line 544: London school
Line 545: Replaced in the
Line 546: classic school
Line 547: Shared
Line 548: Dependency
Line 549: Figure 2.4
Line 550: The hierarchy of dependencies. The classical school advocates for 
Line 551: replacing shared dependencies with test doubles. The London school advocates for the 
Line 552: replacement of private dependencies as well, as long as they are mutable.
Line 553: 
Line 554: --- 페이지 55 ---
Line 555: 33
Line 556: The classical and London schools of unit testing
Line 557: And let me reiterate one point about the types of dependencies. Not all out-of-process
Line 558: dependencies fall into the category of shared dependencies. A shared dependency
Line 559: almost always resides outside the application’s process, but the opposite isn’t true (see
Line 560: figure 2.5). In order for an out-of-process dependency to be shared, it has to provide
Line 561: means for unit tests to communicate with each other. The communication is done
Line 562: through modifications of the dependency’s internal state. In that sense, an immutable
Line 563: out-of-process dependency doesn’t provide such a means. The tests simply can’t mod-
Line 564: ify anything in it and thus can’t interfere with each other’s execution context.
Line 565: For example, if there’s an API somewhere that returns a catalog of all products the orga-
Line 566: nization sells, this isn’t a shared dependency as long as the API doesn’t expose the
Line 567: functionality to change the catalog. It’s true that such a dependency is volatile and sits
Line 568: outside the application’s boundary, but since the tests can’t affect the data it returns, it
Line 569: isn’t shared. This doesn’t mean you have to include such a dependency in the testing
Line 570: scope. In most cases, you still need to replace it with a test double to keep the test fast.
Line 571: But if the out-of-process dependency is quick enough and the connection to it is stable,
Line 572: you can make a good case for using it as-is in the tests.
Line 573:  Having that said, in this book, I use the terms shared dependency and out-of-process
Line 574: dependency interchangeably unless I explicitly state otherwise. In real-world projects,
Line 575: you rarely have a shared dependency that isn’t out-of-process. If a dependency is in-
Line 576: process, you can easily supply a separate instance of it to each test; there’s no need to
Line 577: share it between tests. Similarly, you normally don’t encounter an out-of-process
Line 578: Shared
Line 579: dependencies
Line 580: Out-of-process
Line 581: dependencies
Line 582: Singleton
Line 583: Database
Line 584: Read-only API service
Line 585: Figure 2.5
Line 586: The relation between shared and out-of-process dependencies. An example of a 
Line 587: dependency that is shared but not out-of-process is a singleton (an instance that is reused by 
Line 588: all tests) or a static field in a class. A database is shared and out-of-process—it resides outside 
Line 589: the main process and is mutable. A read-only API is out-of-process but not shared, since tests 
Line 590: can’t modify it and thus can’t affect each other’s execution flow.
Line 591: 
Line 592: --- 페이지 56 ---
Line 593: 34
Line 594: CHAPTER 2
Line 595: What is a unit test?
Line 596: dependency that’s not shared. Most such dependencies are mutable and thus can be
Line 597: modified by tests.
Line 598:  With this foundation of definitions, let’s contrast the two schools on their merits. 
Line 599: 2.3
Line 600: Contrasting the classical and London schools 
Line 601: of unit testing
Line 602: To reiterate, the main difference between the classical and London schools is in how
Line 603: they treat the isolation issue in the definition of a unit test. This, in turn, spills over to
Line 604: the treatment of a unit—the thing that should be put under test—and the approach
Line 605: to handling dependencies.
Line 606:  As I mentioned previously, I prefer the classical school of unit testing. It tends to
Line 607: produce tests of higher quality and thus is better suited for achieving the ultimate goal
Line 608: of unit testing, which is the sustainable growth of your project. The reason is fragility:
Line 609: tests that use mocks tend to be more brittle than classical tests (more on this in chap-
Line 610: ter 5). For now, let’s take the main selling points of the London school and evaluate
Line 611: them one by one.
Line 612:  The London school’s approach provides the following benefits:
Line 613: Better granularity. The tests are fine-grained and check only one class at a time.
Line 614: It’s easier to unit test a larger graph of interconnected classes. Since all collaborators
Line 615: are replaced by test doubles, you don’t need to worry about them at the time of
Line 616: writing the test.
Line 617: If a test fails, you know for sure which functionality has failed. Without the class’s
Line 618: collaborators, there could be no suspects other than the class under test itself.
Line 619: Of course, there may still be situations where the system under test uses a
Line 620: value object and it’s the change in this value object that makes the test fail.
Line 621: But these cases aren’t that frequent because all other dependencies are elimi-
Line 622: nated in tests.
Line 623: 2.3.1
Line 624: Unit testing one class at a time
Line 625: The point about better granularity relates to the discussion about what constitutes a
Line 626: unit in unit testing. The London school considers a class as such a unit. Coming from
Line 627: an object-oriented programming background, developers usually regard classes as the
Line 628: atomic building blocks that lie at the foundation of every code base. This naturally
Line 629: leads to treating classes as the atomic units to be verified in tests, too. This tendency is
Line 630: understandable but misleading.
Line 631: TIP
Line 632: Tests shouldn’t verify units of code. Rather, they should verify units of
Line 633: behavior: something that is meaningful for the problem domain and, ideally,
Line 634: something that a business person can recognize as useful. The number of
Line 635: classes it takes to implement such a unit of behavior is irrelevant. The unit
Line 636: could span across multiple classes or only one class, or even take up just a
Line 637: tiny method.
Line 638: 
Line 639: --- 페이지 57 ---
Line 640: 35
Line 641: Contrasting the classical and London schools of unit testing
Line 642: And so, aiming at better code granularity isn’t helpful. As long as the test checks a sin-
Line 643: gle unit of behavior, it’s a good test. Targeting something less than that can in fact
Line 644: damage your unit tests, as it becomes harder to understand exactly what these tests
Line 645: verify. A test should tell a story about the problem your code helps to solve, and this story should
Line 646: be cohesive and meaningful to a non-programmer.
Line 647:  For instance, this is an example of a cohesive story:
Line 648: When I call my dog, he comes right to me.
Line 649: Now compare it to the following:
Line 650: When I call my dog, he moves his front left leg first, then the front right 
Line 651: leg, his head turns, the tail start wagging...
Line 652: The second story makes much less sense. What’s the purpose of all those movements?
Line 653: Is the dog coming to me? Or is he running away? You can’t tell. This is what your tests
Line 654: start to look like when you target individual classes (the dog’s legs, head, and tail)
Line 655: instead of the actual behavior (the dog coming to his master). I talk more about this
Line 656: topic of observable behavior and how to differentiate it from internal implementation
Line 657: details in chapter 5. 
Line 658: 2.3.2
Line 659: Unit testing a large graph of interconnected classes
Line 660: The use of mocks in place of real collaborators can make it easier to test a class—
Line 661: especially when there’s a complicated dependency graph, where the class under test
Line 662: has dependencies, each of which relies on dependencies of its own, and so on, several
Line 663: layers deep. With test doubles, you can substitute the class’s immediate dependencies
Line 664: and thus break up the graph, which can significantly reduce the amount of prepara-
Line 665: tion you have to do in a unit test. If you follow the classical school, you have to re-create
Line 666: the full object graph (with the exception of shared dependencies) just for the sake of
Line 667: setting up the system under test, which can be a lot of work.
Line 668:  Although this is all true, this line of reasoning focuses on the wrong problem.
Line 669: Instead of finding ways to test a large, complicated graph of interconnected classes,
Line 670: you should focus on not having such a graph of classes in the first place. More often
Line 671: than not, a large class graph is a result of a code design problem.
Line 672:  It’s actually a good thing that the tests point out this problem. As we discussed in
Line 673: chapter 1, the ability to unit test a piece of code is a good negative indicator—it pre-
Line 674: dicts poor code quality with a relatively high precision. If you see that to unit test a
Line 675: class, you need to extend the test’s arrange phase beyond all reasonable limits, it’s a
Line 676: certain sign of trouble. The use of mocks only hides this problem; it doesn’t tackle the
Line 677: root cause. I talk about how to fix the underlying code design problem in part 2. 
Line 678:  
Line 679: 
Line 680: --- 페이지 58 ---
Line 681: 36
Line 682: CHAPTER 2
Line 683: What is a unit test?
Line 684: 2.3.3
Line 685: Revealing the precise bug location
Line 686: If you introduce a bug to a system with London-style tests, it normally causes only tests
Line 687: whose SUT contains the bug to fail. However, with the classical approach, tests that
Line 688: target the clients of the malfunctioning class can also fail. This leads to a ripple effect
Line 689: where a single bug can cause test failures across the whole system. As a result, it
Line 690: becomes harder to find the root of the issue. You might need to spend some time
Line 691: debugging the tests to figure it out.
Line 692:  It’s a valid concern, but I don’t see it as a big problem. If you run your tests regu-
Line 693: larly (ideally, after each source code change), then you know what caused the bug—
Line 694: it’s what you edited last, so it’s not that difficult to find the issue. Also, you don’t have
Line 695: to look at all the failing tests. Fixing one automatically fixes all the others.
Line 696:  Furthermore, there’s some value in failures cascading all over the test suite. If a
Line 697: bug leads to a fault in not only one test but a whole lot of them, it shows that the piece
Line 698: of code you have just broken is of great value—the entire system depends on it. That’s
Line 699: useful information to keep in mind when working with the code. 
Line 700: 2.3.4
Line 701: Other differences between the classical and London schools
Line 702: Two remaining differences between the classical and London schools are
Line 703: Their approach to system design with test-driven development (TDD)
Line 704: The issue of over-specification
Line 705: The London style of unit testing leads to outside-in TDD, where you start from the
Line 706: higher-level tests that set expectations for the whole system. By using mocks, you spec-
Line 707: ify which collaborators the system should communicate with to achieve the expected
Line 708: result. You then work your way through the graph of classes until you implement every
Line 709: one of them. Mocks make this design process possible because you can focus on one
Line 710: Test-driven development
Line 711: Test-driven development is a software development process that relies on tests to
Line 712: drive the project development. The process consists of three (some authors specify
Line 713: four) stages, which you repeat for every test case:
Line 714: 1
Line 715: Write a failing test to indicate which functionality needs to be added and how
Line 716: it should behave.
Line 717: 2
Line 718: Write just enough code to make the test pass. At this stage, the code doesn’t
Line 719: have to be elegant or clean.
Line 720: 3
Line 721: Refactor the code. Under the protection of the passing test, you can safely
Line 722: clean up the code to make it more readable and maintainable.
Line 723: Good sources on this topic are the two books I recommended earlier: Kent Beck’s
Line 724: Test-Driven Development: By Example, and Growing Object-Oriented Software, Guided
Line 725: by Tests by Steve Freeman and Nat Pryce.
Line 726: 
Line 727: --- 페이지 59 ---
Line 728: 37
Line 729: Integration tests in the two schools
Line 730: class at a time. You can cut off all of the SUT’s collaborators when testing it and thus
Line 731: postpone implementing those collaborators to a later time.
Line 732:  The classical school doesn’t provide quite the same guidance since you have to
Line 733: deal with the real objects in tests. Instead, you normally use the inside-out approach.
Line 734: In this style, you start from the domain model and then put additional layers on top of
Line 735: it until the software becomes usable by the end user.
Line 736:  But the most crucial distinction between the schools is the issue of over-specification:
Line 737: that is, coupling the tests to the SUT’s implementation details. The London style
Line 738: tends to produce tests that couple to the implementation more often than the classi-
Line 739: cal style. And this is the main objection against the ubiquitous use of mocks and the
Line 740: London style in general.
Line 741:  There’s much more to the topic of mocking. Starting with chapter 4, I gradually
Line 742: cover everything related to it. 
Line 743: 2.4
Line 744: Integration tests in the two schools
Line 745: The London and classical schools also diverge in their definition of an integration
Line 746: test. This disagreement flows naturally from the difference in their views on the isola-
Line 747: tion issue.
Line 748:  The London school considers any test that uses a real collaborator object an inte-
Line 749: gration test. Most of the tests written in the classical style would be deemed integra-
Line 750: tion tests by the London school proponents. For an example, see listing 1.4, in which I
Line 751: first introduced the two tests covering the customer purchase functionality. That code
Line 752: is a typical unit test from the classical perspective, but it’s an integration test for a fol-
Line 753: lower of the London school.
Line 754:  In this book, I use the classical definitions of both unit and integration testing.
Line 755: Again, a unit test is an automated test that has the following characteristics:
Line 756: It verifies a small piece of code,
Line 757: Does it quickly,
Line 758: And does it in an isolated manner.
Line 759: Now that I’ve clarified what the first and third attributes mean, I’ll redefine them
Line 760: from the point of view of the classical school. A unit test is a test that
Line 761: Verifies a single unit of behavior,
Line 762: Does it quickly,
Line 763: And does it in isolation from other tests.
Line 764: An integration test, then, is a test that doesn’t meet one of these criteria. For example,
Line 765: a test that reaches out to a shared dependency—say, a database—can’t run in isolation
Line 766: from other tests. A change in the database’s state introduced by one test would alter
Line 767: the outcome of all other tests that rely on the same database if run in parallel. You’d
Line 768: have to take additional steps to avoid this interference. In particular, you would have
Line 769: to run such tests sequentially, so that each test would wait its turn to work with the
Line 770: shared dependency.
Line 771: 
Line 772: --- 페이지 60 ---
Line 773: 38
Line 774: CHAPTER 2
Line 775: What is a unit test?
Line 776:  Similarly, an outreach to an out-of-process dependency makes the test slow. A call
Line 777: to a database adds hundreds of milliseconds, potentially up to a second, of additional
Line 778: execution time. Milliseconds might not seem like a big deal at first, but when your test
Line 779: suite grows large enough, every second counts.
Line 780:  In theory, you could write a slow test that works with in-memory objects only, but
Line 781: it’s not that easy to do. Communication between objects inside the same memory
Line 782: space is much less expensive than between separate processes. Even if the test works
Line 783: with hundreds of in-memory objects, the communication with them will still execute
Line 784: faster than a call to a database.
Line 785:  Finally, a test is an integration test when it verifies two or more units of behavior.
Line 786: This is often a result of trying to optimize the test suite’s execution speed. When you
Line 787: have two slow tests that follow similar steps but verify different units of behavior, it
Line 788: might make sense to merge them into one: one test checking two similar things runs
Line 789: faster than two more-granular tests. But then again, the two original tests would have
Line 790: been integration tests already (due to them being slow), so this characteristic usually
Line 791: isn’t decisive.
Line 792:  An integration test can also verify how two or more modules developed by separate
Line 793: teams work together. This also falls into the third bucket of tests that verify multiple
Line 794: units of behavior at once. But again, because such an integration normally requires an
Line 795: out-of-process dependency, the test will fail to meet all three criteria, not just one.
Line 796:  Integration testing plays a significant part in contributing to software quality by
Line 797: verifying the system as a whole. I write about integration testing in detail in part 3.
Line 798: 2.4.1
Line 799: End-to-end tests are a subset of integration tests
Line 800: In short, an integration test is a test that verifies that your code works in integration with
Line 801: shared dependencies, out-of-process dependencies, or code developed by other teams
Line 802: in the organization. There’s also a separate notion of an end-to-end test. End-to-end
Line 803: tests are a subset of integration tests. They, too, check to see how your code works with
Line 804: out-of-process dependencies. The difference between an end-to-end test and an inte-
Line 805: gration test is that end-to-end tests usually include more of such dependencies.
Line 806:  The line is blurred at times, but in general, an integration test works with only one
Line 807: or two out-of-process dependencies. On the other hand, an end-to-end test works with
Line 808: all out-of-process dependencies, or with the vast majority of them. Hence the name
Line 809: end-to-end, which means the test verifies the system from the end user’s point of view,
Line 810: including all the external applications this system integrates with (see figure 2.6).
Line 811:  People also use such terms as UI tests (UI stands for user interface), GUI tests (GUI is
Line 812: graphical user interface), and functional tests. The terminology is ill-defined, but in gen-
Line 813: eral, these terms are all synonyms.
Line 814:  Let’s say your application works with three out-of-process dependencies: a data-
Line 815: base, the file system, and a payment gateway. A typical integration test would include
Line 816: only the database and file system in scope and use a test double to replace the pay-
Line 817: ment gateway. That’s because you have full control over the database and file system,
Line 818: 
Line 819: --- 페이지 61 ---
Line 820: 39
Line 821: Summary
Line 822: and thus can easily bring them to the required state in tests, whereas you don’t have
Line 823: the same degree of control over the payment gateway. With the payment gateway, you
Line 824: may need to contact the payment processor organization to set up a special test
Line 825: account. You might also need to check that account from time to time to manually
Line 826: clean up all the payment charges left over from the past test executions.
Line 827:  Since end-to-end tests are the most expensive in terms of maintenance, it’s better
Line 828: to run them late in the build process, after all the unit and integration tests have
Line 829: passed. You may possibly even run them only on the build server, not on individual
Line 830: developers’ machines.
Line 831:  Keep in mind that even with end-to-end tests, you might not be able to tackle all of
Line 832: the out-of-process dependencies. There may be no test version of some dependencies,
Line 833: or it may be impossible to bring those dependencies to the required state automati-
Line 834: cally. So you may still need to use a test double, reinforcing the fact that there isn’t a
Line 835: distinct line between integration and end-to-end tests. 
Line 836: Summary
Line 837: Throughout this chapter, I’ve refined the definition of a unit test:
Line 838: – A unit test verifies a single unit of behavior,
Line 839: – Does it quickly,
Line 840: – And does it in isolation from other tests.
Line 841: Another class
Line 842: Unit test
Line 843: Payment gateway
Line 844: End-to-end test
Line 845: Database
Line 846: System under test
Line 847: Integration test
Line 848: Figure 2.6
Line 849: End-to-end tests normally include all or almost all out-of-process dependencies 
Line 850: in the scope. Integration tests check only one or two such dependencies—those that are 
Line 851: easier to set up automatically, such as the database or the file system.
Line 852: 
Line 853: --- 페이지 62 ---
Line 854: 40
Line 855: CHAPTER 2
Line 856: What is a unit test?
Line 857: The isolation issue is disputed the most. The dispute led to the formation of two
Line 858: schools of unit testing: the classical (Detroit) school, and the London (mockist)
Line 859: school. This difference of opinion affects the view of what constitutes a unit and
Line 860: the treatment of the system under test’s (SUT’s) dependencies.
Line 861: – The London school states that the units under test should be isolated from
Line 862: each other. A unit under test is a unit of code, usually a class. All of its depen-
Line 863: dencies, except immutable dependencies, should be replaced with test dou-
Line 864: bles in tests.
Line 865: – The classical school states that the unit tests need to be isolated from each
Line 866: other, not units. Also, a unit under test is a unit of behavior, not a unit of code.
Line 867: Thus, only shared dependencies should be replaced with test doubles.
Line 868: Shared dependencies are dependencies that provide means for tests to affect
Line 869: each other’s execution flow.
Line 870: The London school provides the benefits of better granularity, the ease of test-
Line 871: ing large graphs of interconnected classes, and the ease of finding which func-
Line 872: tionality contains a bug after a test failure.
Line 873: The benefits of the London school look appealing at first. However, they intro-
Line 874: duce several issues. First, the focus on classes under test is misplaced: tests
Line 875: should verify units of behavior, not units of code. Furthermore, the inability to
Line 876: unit test a piece of code is a strong sign of a problem with the code design. The
Line 877: use of test doubles doesn’t fix this problem, but rather only hides it. And finally,
Line 878: while the ease of determining which functionality contains a bug after a test fail-
Line 879: ure is helpful, it’s not that big a deal because you often know what caused the
Line 880: bug anyway—it’s what you edited last.
Line 881: The biggest issue with the London school of unit testing is the problem of over-
Line 882: specification—coupling tests to the SUT’s implementation details.
Line 883: An integration test is a test that doesn’t meet at least one of the criteria for a
Line 884: unit test. End-to-end tests are a subset of integration tests; they verify the system
Line 885: from the end user’s point of view. End-to-end tests reach out directly to all or
Line 886: almost all out-of-process dependencies your application works with.
Line 887: For a canonical book about the classical style, I recommend Kent Beck’s Test-
Line 888: Driven Development: By Example. For more on the London style, see Growing Object-
Line 889: Oriented Software, Guided by Tests, by Steve Freeman and Nat Pryce. For further
Line 890: reading about working with dependencies, I recommend Dependency Injection:
Line 891: Principles, Practices, Patterns by Steven van Deursen and Mark Seemann.