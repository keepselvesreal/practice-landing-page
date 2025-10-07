Line 1: 
Line 2: --- 페이지 114 ---
Line 3: 92
Line 4: Mocks and test fragility
Line 5: Chapter 4 introduced a frame of reference that you can use to analyze specific tests
Line 6: and unit testing approaches. In this chapter, you’ll see that frame of reference in
Line 7: action; we’ll use it to dissect the topic of mocks.
Line 8:  The use of mocks in tests is a controversial subject. Some people argue that
Line 9: mocks are a great tool and apply them in most of their tests. Others claim that mocks
Line 10: lead to test fragility and try not to use them at all. As the saying goes, the truth lies
Line 11: somewhere in between. In this chapter, I’ll show that, indeed, mocks often result in
Line 12: fragile tests—tests that lack the metric of resistance to refactoring. But there are still
Line 13: cases where mocking is applicable and even preferable.
Line 14: This chapter covers
Line 15: Differentiating mocks from stubs
Line 16: Defining observable behavior and implementation 
Line 17: details
Line 18: Understanding the relationship between mocks 
Line 19: and test fragility
Line 20: Using mocks without compromising resistance 
Line 21: to refactoring
Line 22: 
Line 23: --- 페이지 115 ---
Line 24: 93
Line 25: Differentiating mocks from stubs
Line 26:  This chapter draws heavily on the discussion about the London versus classical
Line 27: schools of unit testing from chapter 2. In short, the disagreement between the schools
Line 28: stems from their views on the test isolation issue. The London school advocates isolat-
Line 29: ing pieces of code under test from each other and using test doubles for all but
Line 30: immutable dependencies to perform such isolation.
Line 31:  The classical school stands for isolating unit tests themselves so that they can be
Line 32: run in parallel. This school uses test doubles only for dependencies that are shared
Line 33: between tests.
Line 34:  There’s a deep and almost inevitable connection between mocks and test fragility.
Line 35: In the next several sections, I will gradually lay down the foundation for you to see why
Line 36: that connection exists. You will also learn how to use mocks so that they don’t compro-
Line 37: mise a test’s resistance to refactoring.
Line 38: 5.1
Line 39: Differentiating mocks from stubs
Line 40: In chapter 2, I briefly mentioned that a mock is a test double that allows you to exam-
Line 41: ine interactions between the system under test (SUT) and its collaborators. There’s
Line 42: another type of test double: a stub. Let’s take a closer look at what a mock is and how it
Line 43: is different from a stub.
Line 44: 5.1.1
Line 45: The types of test doubles
Line 46: A test double is an overarching term that describes all kinds of non-production-ready,
Line 47: fake dependencies in tests. The term comes from the notion of a stunt double in a
Line 48: movie. The major use of test doubles is to facilitate testing; they are passed to the
Line 49: system under test instead of real dependencies, which could be hard to set up or
Line 50: maintain.
Line 51:  According to Gerard Meszaros, there are five variations of test doubles: dummy,
Line 52: stub, spy, mock, and fake.1 Such a variety can look intimidating, but in reality, they can all
Line 53: be grouped together into just two types: mocks and stubs (figure 5.1).
Line 54: 1 See xUnit Test Patterns: Refactoring Test Code (Addison-Wesley, 2007).
Line 55: Test double
Line 56: Mock
Line 57: (mock, spy)
Line 58: Stub
Line 59: (stub, dummy, fake)
Line 60: Figure 5.1
Line 61: All variations of test 
Line 62: doubles can be categorized into 
Line 63: two types: mocks and stubs.
Line 64: 
Line 65: --- 페이지 116 ---
Line 66: 94
Line 67: CHAPTER 5
Line 68: Mocks and test fragility
Line 69: The difference between these two types boils down to the following:
Line 70: Mocks help to emulate and examine outcoming interactions. These interactions
Line 71: are calls the SUT makes to its dependencies to change their state.
Line 72: Stubs help to emulate incoming interactions. These interactions are calls the
Line 73: SUT makes to its dependencies to get input data (figure 5.2).
Line 74: All other differences between the five variations are insignificant implementation
Line 75: details. For example, spies serve the same role as mocks. The distinction is that spies
Line 76: are written manually, whereas mocks are created with the help of a mocking frame-
Line 77: work. Sometimes people refer to spies as handwritten mocks.
Line 78:  On the other hand, the difference between a stub, a dummy, and a fake is in how
Line 79: intelligent they are. A dummy is a simple, hardcoded value such as a null value or a
Line 80: made-up string. It’s used to satisfy the SUT’s method signature and doesn’t partici-
Line 81: pate in producing the final outcome. A stub is more sophisticated. It’s a fully fledged
Line 82: dependency that you configure to return different values for different scenarios.
Line 83: Finally, a fake is the same as a stub for most purposes. The difference is in the ratio-
Line 84: nale for its creation: a fake is usually implemented to replace a dependency that
Line 85: doesn’t yet exist.
Line 86:  Notice the difference between mocks and stubs (aside from outcoming versus
Line 87: incoming interactions). Mocks help to emulate and examine interactions between the
Line 88: SUT and its dependencies, while stubs only help to emulate those interactions. This is
Line 89: an important distinction. You will see why shortly. 
Line 90: 5.1.2
Line 91: Mock (the tool) vs. mock (the test double)
Line 92: The term mock is overloaded and can mean different things in different circum-
Line 93: stances. I mentioned in chapter 2 that people often use this term to mean any test
Line 94: double, whereas mocks are only a subset of test doubles. But there’s another meaning
Line 95: System under test
Line 96: SMTP server
Line 97: Send an email
Line 98: Retrieve data
Line 99: Database
Line 100: Stub
Line 101: Mock
Line 102: Figure 5.2
Line 103: Sending an email is 
Line 104: an outcoming interaction: an inter-
Line 105: action that results in a side effect 
Line 106: in the SMTP server. A test double 
Line 107: emulating such an interaction is 
Line 108: a mock. Retrieving data from the 
Line 109: database is an incoming inter-
Line 110: action; it doesn’t result in a 
Line 111: side effect. The corresponding 
Line 112: test double is a stub.
Line 113: 
Line 114: --- 페이지 117 ---
Line 115: 95
Line 116: Differentiating mocks from stubs
Line 117: for the term mock. You can refer to the classes from mocking libraries as mocks, too.
Line 118: These classes help you create actual mocks, but they themselves are not mocks per se.
Line 119: The following listing shows an example.
Line 120: [Fact]
Line 121: public void Sending_a_greetings_email()
Line 122: {
Line 123: var mock = new Mock<IEmailGateway>();      
Line 124: var sut = new Controller(mock.Object);
Line 125: sut.GreetUser("user@email.com");
Line 126: mock.Verify(
Line 127:    
Line 128: x => x.SendGreetingsEmail(   
Line 129: "user@email.com"),
Line 130:    
Line 131: Times.Once);
Line 132:    
Line 133: }
Line 134: The test in listing 5.1 uses the Mock class from the mocking library of my choice
Line 135: (Moq). This class is a tool that enables you to create a test double—a mock. In other
Line 136: words, the class Mock (or Mock<IEmailGateway>) is a mock (the tool), while the instance
Line 137: of that class, mock, is a mock (the test double). It’s important not to conflate a mock (the
Line 138: tool) with a mock (the test double) because you can use a mock (the tool) to create
Line 139: both types of test doubles: mocks and stubs.
Line 140:  The test in the following listing also uses the Mock class, but the instance of that
Line 141: class is not a mock, it’s a stub.
Line 142: [Fact]
Line 143: public void Creating_a_report()
Line 144: {
Line 145: var stub = new Mock<IDatabase>();       
Line 146: stub.Setup(x => x.GetNumberOfUsers())     
Line 147: .Returns(10);
Line 148:      
Line 149: var sut = new Controller(stub.Object);
Line 150: Report report = sut.CreateReport();
Line 151: Assert.Equal(10, report.NumberOfUsers);
Line 152: }
Line 153: This test double emulates an incoming interaction—a call that provides the SUT with
Line 154: input data. On the other hand, in the previous example (listing 5.1), the call to Send-
Line 155: GreetingsEmail() is an outcoming interaction. Its sole purpose is to incur a side
Line 156: effect—send an email. 
Line 157: Listing 5.1
Line 158: Using the Mock class from a mocking library to create a mock
Line 159: Listing 5.2
Line 160: Using the Mock class to create a stub
Line 161: Uses a mock (the 
Line 162: tool) to create a mock 
Line 163: (the test double)
Line 164: Examines the call 
Line 165: from the SUT to 
Line 166: the test double
Line 167: Uses a mock 
Line 168: (the tool) to 
Line 169: create a stub
Line 170: Sets up a 
Line 171: canned answer
Line 172: 
Line 173: --- 페이지 118 ---
Line 174: 96
Line 175: CHAPTER 5
Line 176: Mocks and test fragility
Line 177: 5.1.3
Line 178: Don’t assert interactions with stubs
Line 179: As I mentioned in section 5.1.1, mocks help to emulate and examine outcoming interac-
Line 180: tions between the SUT and its dependencies, while stubs only help to emulate incom-
Line 181: ing interactions, not examine them. The difference between the two stems from the
Line 182: guideline of never asserting interactions with stubs. A call from the SUT to a stub is not
Line 183: part of the end result the SUT produces. Such a call is only a means to produce the
Line 184: end result: a stub provides input from which the SUT then generates the output.
Line 185: NOTE
Line 186: Asserting interactions with stubs is a common anti-pattern that leads to
Line 187: fragile tests.
Line 188: As you might remember from chapter 4, the only way to avoid false positives and thus
Line 189: improve resistance to refactoring in tests is to make those tests verify the end result
Line 190: (which, ideally, should be meaningful to a non-programmer), not implementation
Line 191: details. In listing 5.1, the check
Line 192: mock.Verify(x => x.SendGreetingsEmail("user@email.com"))
Line 193: corresponds to an actual outcome, and that outcome is meaningful to a domain
Line 194: expert: sending a greetings email is something business people would want the system
Line 195: to do. At the same time, the call to GetNumberOfUsers() in listing 5.2 is not an out-
Line 196: come at all. It’s an internal implementation detail regarding how the SUT gathers
Line 197: data necessary for the report creation. Therefore, asserting this call would lead to test
Line 198: fragility: it shouldn’t matter how the SUT generates the end result, as long as that
Line 199: result is correct. The following listing shows an example of such a brittle test.
Line 200: [Fact]
Line 201: public void Creating_a_report()
Line 202: {
Line 203: var stub = new Mock<IDatabase>();
Line 204: stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
Line 205: var sut = new Controller(stub.Object);
Line 206: Report report = sut.CreateReport();
Line 207: Assert.Equal(10, report.NumberOfUsers);
Line 208: stub.Verify(
Line 209:    
Line 210: x => x.GetNumberOfUsers(),   
Line 211: Times.Once);
Line 212:    
Line 213: }
Line 214: This practice of verifying things that aren’t part of the end result is also called over-
Line 215: specification. Most commonly, overspecification takes place when examining interac-
Line 216: tions. Checking for interactions with stubs is a flaw that’s quite easy to spot because
Line 217: tests shouldn’t check for any interactions with stubs. Mocks are a more complicated sub-
Line 218: Listing 5.3
Line 219: Asserting an interaction with a stub
Line 220: Asserts the 
Line 221: interaction 
Line 222: with the stub
Line 223: 
Line 224: --- 페이지 119 ---
Line 225: 97
Line 226: Differentiating mocks from stubs
Line 227: ject: not all uses of mocks lead to test fragility, but a lot of them do. You’ll see why later
Line 228: in this chapter. 
Line 229: 5.1.4
Line 230: Using mocks and stubs together
Line 231: Sometimes you need to create a test double that exhibits the properties of both a
Line 232: mock and a stub. For example, here’s a test from chapter 2 that I used to illustrate the
Line 233: London style of unit testing.
Line 234: [Fact]
Line 235: public void Purchase_fails_when_not_enough_inventory()
Line 236: {
Line 237: var storeMock = new Mock<IStore>();
Line 238: storeMock
Line 239:     
Line 240: .Setup(x => x.HasEnoughInventory(    
Line 241: Product.Shampoo, 5))
Line 242:     
Line 243: .Returns(false);
Line 244:     
Line 245: var sut = new Customer();
Line 246: bool success = sut.Purchase(
Line 247: storeMock.Object, Product.Shampoo, 5);
Line 248: Assert.False(success);
Line 249: storeMock.Verify(
Line 250:    
Line 251: x => x.RemoveInventory(Product.Shampoo, 5),  
Line 252: Times.Never);
Line 253:    
Line 254: }
Line 255: This test uses storeMock for two purposes: it returns a canned answer and verifies a
Line 256: method call made by the SUT. Notice, though, that these are two different methods:
Line 257: the test sets up the answer from HasEnoughInventory() but then verifies the call to
Line 258: RemoveInventory(). Thus, the rule of not asserting interactions with stubs is not vio-
Line 259: lated here.
Line 260:  When a test double is both a mock and a stub, it’s still called a mock, not a stub.
Line 261: That’s mostly the case because we need to pick one name, but also because being a
Line 262: mock is a more important fact than being a stub. 
Line 263: 5.1.5
Line 264: How mocks and stubs relate to commands and queries
Line 265: The notions of mocks and stubs tie to the command query separation (CQS) princi-
Line 266: ple. The CQS principle states that every method should be either a command or a
Line 267: query, but not both. As shown in figure 5.3, commands are methods that produce side
Line 268: effects and don’t return any value (return void). Examples of side effects include
Line 269: mutating an object’s state, changing a file in the file system, and so on. Queries are the
Line 270: opposite of that—they are side-effect free and return a value.
Line 271:  To follow this principle, be sure that if a method produces a side effect, that
Line 272: method’s return type is void. And if the method returns a value, it must stay side-effect
Line 273: Listing 5.4
Line 274: storeMock: both a mock and a stub
Line 275: Sets up a 
Line 276: canned 
Line 277: answer
Line 278: Examines a call 
Line 279: from the SUT
Line 280: 
Line 281: --- 페이지 120 ---
Line 282: 98
Line 283: CHAPTER 5
Line 284: Mocks and test fragility
Line 285: free. In other words, asking a question should not change the answer. Code that main-
Line 286: tains such a clear separation becomes easier to read. You can tell what a method does
Line 287: just by looking at its signature, without diving into its implementation details.
Line 288:  Of course, it’s not always possible to follow the CQS principle. There are always
Line 289: methods for which it makes sense to both incur a side effect and return a value. A clas-
Line 290: sical example is stack.Pop(). This method both removes a top element from the
Line 291: stack and returns it to the caller. Still, it’s a good idea to adhere to the CQS principle
Line 292: whenever you can.
Line 293:  Test doubles that substitute commands become mocks. Similarly, test doubles that
Line 294: substitute queries are stubs. Look at the two tests from listings 5.1 and 5.2 again (I’m
Line 295: showing their relevant parts here):
Line 296: var mock = new Mock<IEmailGateway>();
Line 297: mock.Verify(x => x.SendGreetingsEmail("user@email.com"));
Line 298: var stub = new Mock<IDatabase>();
Line 299: stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
Line 300: SendGreetingsEmail() is a command whose side effect is sending an email. The test
Line 301: double that substitutes this command is a mock. On the other hand, GetNumberOf-
Line 302: Users() is a query that returns a value and doesn’t mutate the database state. The cor-
Line 303: responding test double is a stub. 
Line 304:  
Line 305: Methods
Line 306: Commands
Line 307: Incur side effects
Line 308: No return value
Line 309: Mocks
Line 310: Queries
Line 311: Side-effect free
Line 312: Returns a value
Line 313: Stubs
Line 314: Figure 5.3
Line 315: In the command query 
Line 316: separation (CQS) principle, commands 
Line 317: correspond to mocks, while queries are 
Line 318: consistent with stubs.
Line 319: 
Line 320: --- 페이지 121 ---
Line 321: 99
Line 322: Observable behavior vs. implementation details
Line 323: 5.2
Line 324: Observable behavior vs. implementation details
Line 325: Section 5.1 showed what a mock is. The next step on the way to explaining the con-
Line 326: nection between mocks and test fragility is diving into what causes such fragility.
Line 327:  As you might remember from chapter 4, test fragility corresponds to the second
Line 328: attribute of a good unit test: resistance to refactoring. (As a reminder, the four attri-
Line 329: butes are protection against regressions, resistance to refactoring, fast feedback, and
Line 330: maintainability.) The metric of resistance to refactoring is the most important
Line 331: because whether a unit test possesses this metric is mostly a binary choice. Thus, it’s
Line 332: good to max out this metric to the extent that the test still remains in the realm of unit
Line 333: testing and doesn’t transition to the category of end-to-end testing. The latter, despite
Line 334: being the best at resistance to refactoring, is generally much harder to maintain.
Line 335:  In chapter 4, you also saw that the main reason tests deliver false positives (and thus
Line 336: fail at resistance to refactoring) is because they couple to the code’s implementation
Line 337: details. The only way to avoid such coupling is to verify the end result the code produces
Line 338: (its observable behavior) and distance tests from implementation details as much as pos-
Line 339: sible. In other words, tests must focus on the whats, not the hows. So, what exactly is an
Line 340: implementation detail, and how is it different from an observable behavior?
Line 341: 5.2.1
Line 342: Observable behavior is not the same as a public API
Line 343: All production code can be categorized along two dimensions:
Line 344: Public API vs. private API (where API means application programming interface)
Line 345: Observable behavior vs. implementation details 
Line 346: The categories in these dimensions don’t overlap. A method can’t belong to both a pub-
Line 347: lic and a private API; it’s either one or the other. Similarly, the code is either an internal
Line 348: implementation detail or part of the system’s observable behavior, but not both.
Line 349:  Most programming languages provide a simple mechanism to differentiate between
Line 350: the code base’s public and private APIs. For example, in C#, you can mark any mem-
Line 351: ber in a class with the private keyword, and that member will be hidden from the cli-
Line 352: ent code, becoming part of the class’s private API. The same is true for classes: you can
Line 353: easily make them private by using the private or internal keyword.
Line 354:  The distinction between observable behavior and internal implementation details
Line 355: is more nuanced. For a piece of code to be part of the system’s observable behavior, it
Line 356: has to do one of the following things:
Line 357: Expose an operation that helps the client achieve one of its goals. An operation is
Line 358: a method that performs a calculation or incurs a side effect or both.
Line 359: Expose a state that helps the client achieve one of its goals. State is the current
Line 360: condition of the system.
Line 361: Any code that does neither of these two things is an implementation detail.
Line 362:  Notice that whether the code is observable behavior depends on who its client is
Line 363: and what the goals of that client are. In order to be a part of observable behavior, the
Line 364: 
Line 365: --- 페이지 122 ---
Line 366: 100
Line 367: CHAPTER 5
Line 368: Mocks and test fragility
Line 369: code needs to have an immediate connection to at least one such goal. The word client
Line 370: can refer to different things depending on where the code resides. The common
Line 371: examples are client code from the same code base, an external application, or the
Line 372: user interface.
Line 373:  Ideally, the system’s public API surface should coincide with its observable behav-
Line 374: ior, and all its implementation details should be hidden from the eyes of the clients.
Line 375: Such a system has a well-designed API (figure 5.4).
Line 376: Often, though, the system’s public API extends beyond its observable behavior and
Line 377: starts exposing implementation details. Such a system’s implementation details leak to
Line 378: its public API surface (figure 5.5). 
Line 379: 5.2.2
Line 380: Leaking implementation details: An example with an operation
Line 381: Let’s take a look at examples of code whose implementation details leak to the public
Line 382: API. Listing 5.5 shows a User class with a public API that consists of two members: a
Line 383: Name property and a NormalizeName() method. The class also has an invariant: users’
Line 384: names must not exceed 50 characters and should be truncated otherwise.
Line 385: public class User
Line 386: {
Line 387: public string Name { get; set; }
Line 388: Listing 5.5
Line 389: User class with leaking implementation details
Line 390: Observable behavior
Line 391: Public API
Line 392: Private API
Line 393: Implementation detail
Line 394: Figure 5.4
Line 395: In a well-designed API, the 
Line 396: observable behavior coincides with the public 
Line 397: API, while all implementation details are 
Line 398: hidden behind the private API.
Line 399: Observable behavior
Line 400: Public API
Line 401: Private API
Line 402: Leaking implementation detail
Line 403: Figure 5.5
Line 404: A system leaks implementation 
Line 405: details when its public API extends beyond 
Line 406: the observable behavior.
Line 407: 
Line 408: --- 페이지 123 ---
Line 409: 101
Line 410: Observable behavior vs. implementation details
Line 411: public string NormalizeName(string name)
Line 412: {
Line 413: string result = (name ?? "").Trim();
Line 414: if (result.Length > 50)
Line 415: return result.Substring(0, 50);
Line 416: return result;
Line 417: }
Line 418: }
Line 419: public class UserController
Line 420: {
Line 421: public void RenameUser(int userId, string newName)
Line 422: {
Line 423: User user = GetUserFromDatabase(userId);
Line 424: string normalizedName = user.NormalizeName(newName);
Line 425: user.Name = normalizedName;
Line 426: SaveUserToDatabase(user);
Line 427: }
Line 428: }
Line 429: UserController is client code. It uses the User class in its RenameUser method. The
Line 430: goal of this method, as you have probably guessed, is to change a user’s name.
Line 431:  So, why isn’t User’s API well-designed? Look at its members once again: the Name
Line 432: property and the NormalizeName method. Both of them are public. Therefore, in
Line 433: order for the class’s API to be well-designed, these members should be part of the
Line 434: observable behavior. This, in turn, requires them to do one of the following two things
Line 435: (which I’m repeating here for convenience):
Line 436: Expose an operation that helps the client achieve one of its goals.
Line 437: Expose a state that helps the client achieve one of its goals.
Line 438: Only the Name property meets this requirement. It exposes a setter, which is an opera-
Line 439: tion that allows UserController to achieve its goal of changing a user’s name. The
Line 440: NormalizeName method is also an operation, but it doesn’t have an immediate con-
Line 441: nection to the client’s goal. The only reason UserController calls this method is to
Line 442: satisfy the invariant of User. NormalizeName is therefore an implementation detail that
Line 443: leaks to the class’s public API (figure 5.6).
Line 444:  To fix the situation and make the class’s API well-designed, User needs to hide
Line 445: NormalizeName() and call it internally as part of the property’s setter without relying
Line 446: on the client code to do so. Listing 5.6 shows this approach.
Line 447:  
Line 448:  
Line 449: 
Line 450: --- 페이지 124 ---
Line 451: 102
Line 452: CHAPTER 5
Line 453: Mocks and test fragility
Line 454:  
Line 455: public class User
Line 456: {
Line 457: private string _name;
Line 458: public string Name
Line 459: {
Line 460: get => _name;
Line 461: set => _name = NormalizeName(value);
Line 462: }
Line 463: private string NormalizeName(string name)
Line 464: {
Line 465: string result = (name ?? "").Trim();
Line 466: if (result.Length > 50)
Line 467: return result.Substring(0, 50);
Line 468: return result;
Line 469: }
Line 470: }
Line 471: public class UserController
Line 472: {
Line 473: public void RenameUser(int userId, string newName)
Line 474: {
Line 475: User user = GetUserFromDatabase(userId);
Line 476: user.Name = newName;
Line 477: SaveUserToDatabase(user);
Line 478: }
Line 479: }
Line 480: User’s API in listing 5.6 is well-designed: only the observable behavior (the Name prop-
Line 481: erty) is made public, while the implementation details (the NormalizeName method)
Line 482: are hidden behind the private API (figure 5.7).
Line 483:  
Line 484: Listing 5.6
Line 485: A version of User with a well-designed API
Line 486: Observable behavior
Line 487: Public API
Line 488: Normalize
Line 489: name
Line 490: Name
Line 491: Leaking implementation detail
Line 492: Figure 5.6
Line 493: The API of User is not well-
Line 494: designed: it exposes the NormalizeName 
Line 495: method, which is not part of the observable 
Line 496: behavior.
Line 497: 
Line 498: --- 페이지 125 ---
Line 499: 103
Line 500: Observable behavior vs. implementation details
Line 501: NOTE
Line 502: Strictly speaking, Name’s getter should also be made private, because
Line 503: it’s not used by UserController. In reality, though, you almost always want to
Line 504: read back changes you make. Therefore, in a real project, there will certainly be
Line 505: another use case that requires seeing users’ current names via Name’s getter.
Line 506: There’s a good rule of thumb that can help you determine whether a class leaks its
Line 507: implementation details. If the number of operations the client has to invoke on the
Line 508: class to achieve a single goal is greater than one, then that class is likely leaking imple-
Line 509: mentation details. Ideally, any individual goal should be achieved with a single operation. In
Line 510: listing 5.5, for example, UserController has to use two operations from User:
Line 511: string normalizedName = user.NormalizeName(newName);
Line 512: user.Name = normalizedName;
Line 513: After the refactoring, the number of operations has been reduced to one:
Line 514: user.Name = newName;
Line 515: In my experience, this rule of thumb holds true for the vast majority of cases where
Line 516: business logic is involved. There could very well be exceptions, though. Still, be sure
Line 517: to examine each situation where your code violates this rule for a potential leak of
Line 518: implementation details. 
Line 519: 5.2.3
Line 520: Well-designed API and encapsulation
Line 521: Maintaining a well-designed API relates to the notion of encapsulation. As you might
Line 522: recall from chapter 3, encapsulation is the act of protecting your code against inconsis-
Line 523: tencies, also known as invariant violations. An invariant is a condition that should be
Line 524: held true at all times. The User class from the previous example had one such invari-
Line 525: ant: no user could have a name that exceeded 50 characters.
Line 526:  Exposing implementation details goes hand in hand with invariant violations—the
Line 527: former often leads to the latter. Not only did the original version of User leak its
Line 528: implementation details, but it also didn’t maintain proper encapsulation. It allowed
Line 529: the client to bypass the invariant and assign a new name to a user without normalizing
Line 530: that name first.
Line 531: Observable behavior
Line 532: Public API
Line 533: Normalize
Line 534: name
Line 535: Name
Line 536: Private API
Line 537: Implementation detail
Line 538: Figure 5.7
Line 539: User with a well-designed API. 
Line 540: Only the observable behavior is public; the 
Line 541: implementation details are now private.
Line 542: 
Line 543: --- 페이지 126 ---
Line 544: 104
Line 545: CHAPTER 5
Line 546: Mocks and test fragility
Line 547:  Encapsulation is crucial for code base maintainability in the long run. The reason
Line 548: why is complexity. Code complexity is one of the biggest challenges you’ll face in soft-
Line 549: ware development. The more complex the code base becomes, the harder it is to work
Line 550: with, which, in turn, results in slowing down development speed and increasing the
Line 551: number of bugs.
Line 552:  Without encapsulation, you have no practical way to cope with ever-increasing
Line 553: code complexity. When the code’s API doesn’t guide you through what is and what
Line 554: isn’t allowed to be done with that code, you have to keep a lot of information in mind
Line 555: to make sure you don’t introduce inconsistencies with new code changes. This brings
Line 556: an additional mental burden to the process of programming. Remove as much of that
Line 557: burden from yourself as possible. You cannot trust yourself to do the right thing all the
Line 558: time—so, eliminate the very possibility of doing the wrong thing. The best way to do so is to
Line 559: maintain proper encapsulation so that your code base doesn’t even provide an option
Line 560: for you to do anything incorrectly. Encapsulation ultimately serves the same goal as
Line 561: unit testing: it enables sustainable growth of your software project.
Line 562:  There’s a similar principle: tell-don’t-ask. It was coined by Martin Fowler (https://
Line 563: martinfowler.com/bliki/TellDontAsk.html) and stands for bundling data with the
Line 564: functions that operate on that data. You can view this principle as a corollary to the
Line 565: practice of encapsulation. Code encapsulation is a goal, whereas bundling data and
Line 566: functions together, as well as hiding implementation details, are the means to achieve
Line 567: that goal:
Line 568: Hiding implementation details helps you remove the class’s internals from the eyes
Line 569: of its clients, so there’s less risk of corrupting those internals.
Line 570: Bundling data and operations helps to make sure these operations don’t violate
Line 571: the class’s invariants. 
Line 572: 5.2.4
Line 573: Leaking implementation details: An example with state
Line 574: The example shown in listing 5.5 demonstrated an operation (the NormalizeName
Line 575: method) that was an implementation detail leaking to the public API. Let’s also look
Line 576: at an example with state. The following listing contains the MessageRenderer class you
Line 577: saw in chapter 4. It uses a collection of sub-renderers to generate an HTML represen-
Line 578: tation of a message containing a header, a body, and a footer.
Line 579: public class MessageRenderer : IRenderer
Line 580: {
Line 581: public IReadOnlyList<IRenderer> SubRenderers { get; }
Line 582: public MessageRenderer()
Line 583: {
Line 584: SubRenderers = new List<IRenderer>
Line 585: {
Line 586: new HeaderRenderer(),
Line 587: new BodyRenderer(),
Line 588: Listing 5.7
Line 589: State as an implementation detail 
Line 590: 
Line 591: --- 페이지 127 ---
Line 592: 105
Line 593: Observable behavior vs. implementation details
Line 594: new FooterRenderer()
Line 595: };
Line 596: }
Line 597: public string Render(Message message)
Line 598: {
Line 599: return SubRenderers
Line 600: .Select(x => x.Render(message))
Line 601: .Aggregate("", (str1, str2) => str1 + str2);
Line 602: }
Line 603: }
Line 604: The sub-renderers collection is public. But is it part of observable behavior? Assuming
Line 605: that the client’s goal is to render an HTML message, the answer is no. The only class
Line 606: member such a client would need is the Render method itself. Thus SubRenderers is
Line 607: also a leaking implementation detail.
Line 608:  I bring up this example again for a reason. As you may remember, I used it to illus-
Line 609: trate a brittle test. That test was brittle precisely because it was tied to this implementa-
Line 610: tion detail—it checked to see the collection’s composition. The brittleness was fixed by
Line 611: re-targeting the test at the Render method. The new version of the test verified the result-
Line 612: ing message—the only output the client code cared about, the observable behavior.
Line 613:  As you can see, there’s an intrinsic connection between good unit tests and a well-
Line 614: designed API. By making all implementation details private, you leave your tests no
Line 615: choice other than to verify the code’s observable behavior, which automatically
Line 616: improves their resistance to refactoring.
Line 617: TIP
Line 618: Making the API well-designed automatically improves unit tests.
Line 619: Another guideline flows from the definition of a well-designed API: you should expose
Line 620: the absolute minimum number of operations and state. Only code that directly helps
Line 621: clients achieve their goals should be made public. Everything else is implementation
Line 622: details and thus must be hidden behind the private API.
Line 623:  Note that there’s no such problem as leaking observable behavior, which would be
Line 624: symmetric to the problem of leaking implementation details. While you can expose an
Line 625: implementation detail (a method or a class that is not supposed to be used by the cli-
Line 626: ent), you can’t hide an observable behavior. Such a method or class would no longer
Line 627: have an immediate connection to the client goals, because the client wouldn’t be able
Line 628: to directly use it anymore. Thus, by definition, this code would cease to be part of
Line 629: observable behavior. Table 5.1 sums it all up.
Line 630: Table 5.1
Line 631: The relationship between the code’s publicity and purpose. Avoid making implementation
Line 632: details public.
Line 633: Observable behavior
Line 634: Implementation detail
Line 635: Public
Line 636: Good
Line 637: Bad
Line 638: Private
Line 639: N/A
Line 640: Good 
Line 641: 
Line 642: --- 페이지 128 ---
Line 643: 106
Line 644: CHAPTER 5
Line 645: Mocks and test fragility
Line 646: 5.3
Line 647: The relationship between mocks and test fragility
Line 648: The previous sections defined a mock and showed the difference between observable
Line 649: behavior and an implementation detail. In this section, you will learn about hexago-
Line 650: nal architecture, the difference between internal and external communications, and
Line 651: (finally!) the relationship between mocks and test fragility.
Line 652: 5.3.1
Line 653: Defining hexagonal architecture
Line 654: A typical application consists of two layers, domain and application services, as
Line 655: shown in figure 5.8. The domain layer resides in the middle of the diagram because
Line 656: it’s the central part of your application. It contains the business logic: the essential
Line 657: functionality your application is built for. The domain layer and its business logic
Line 658: differentiate this application from others and provide a competitive advantage for
Line 659: the organization.
Line 660: The application services layer sits on top of the domain layer and orchestrates com-
Line 661: munication between that layer and the external world. For example, if your applica-
Line 662: tion is a RESTful API, all requests to this API hit the application services layer first.
Line 663: This layer then coordinates the work between domain classes and out-of-process
Line 664: dependencies. Here’s an example of such coordination for the application service. It
Line 665: does the following:
Line 666: Queries the database and uses the data to materialize a domain class instance
Line 667: Invokes an operation on that instance
Line 668: Saves the results back to the database
Line 669: The combination of the application services layer and the domain layer forms a hexa-
Line 670: gon, which itself represents your application. It can interact with other applications,
Line 671: which are represented with their own hexagons (see figure 5.9). These other applica-
Line 672: tions could be an SMTP service, a third-party system, a message bus, and so on. A set
Line 673: of interacting hexagons makes up a hexagonal architecture.
Line 674:  
Line 675: Domain
Line 676: (business logic)
Line 677: Application
Line 678: services
Line 679: Figure 5.8
Line 680: A typical application consists of a 
Line 681: domain layer and an application services layer. 
Line 682: The domain layer contains the application’s 
Line 683: business logic; application services tie that 
Line 684: logic to business use cases.
Line 685: 
Line 686: --- 페이지 129 ---
Line 687: 107
Line 688: The relationship between mocks and test fragility
Line 689: The term hexagonal architecture was introduced by Alistair Cockburn. Its purpose is to
Line 690: emphasize three important guidelines:
Line 691: The separation of concerns between the domain and application services layers—Business
Line 692: logic is the most important part of the application. Therefore, the domain layer
Line 693: should be accountable only for that business logic and exempted from all other
Line 694: responsibilities. Those responsibilities, such as communicating with external
Line 695: applications and retrieving data from the database, must be attributed to appli-
Line 696: cation services. Conversely, the application services shouldn’t contain any busi-
Line 697: ness logic. Their responsibility is to adapt the domain layer by translating the
Line 698: incoming requests into operations on domain classes and then persisting the
Line 699: results or returning them back to the caller. You can view the domain layer as a
Line 700: collection of the application’s domain knowledge (how-to’s) and the application
Line 701: services layer as a set of business use cases (what-to’s).
Line 702: Communications inside your application—Hexagonal architecture prescribes a
Line 703: one-way flow of dependencies: from the application services layer to the domain
Line 704: layer. Classes inside the domain layer should only depend on each other; they
Line 705: should not depend on classes from the application services layer. This guideline
Line 706: flows from the previous one. The separation of concerns between the applica-
Line 707: tion services layer and the domain layer means that the former knows about the
Line 708: latter, but the opposite is not true. The domain layer should be fully isolated
Line 709: from the external world.
Line 710: Communications between applications—External applications connect to your
Line 711: application through a common interface maintained by the application services
Line 712: layer. No one has a direct access to the domain layer. Each side in a hexagon
Line 713: represents a connection into or out of the application. Note that although a
Line 714: Domain
Line 715: (business logic)
Line 716: Application
Line 717: services
Line 718: Third-party
Line 719: system
Line 720: Message
Line 721: bus
Line 722: SMTP
Line 723: service
Line 724: Figure 5.9
Line 725: A hexagonal 
Line 726: architecture is a set of 
Line 727: interacting applications—
Line 728: hexagons.
Line 729: 
Line 730: --- 페이지 130 ---
Line 731: 108
Line 732: CHAPTER 5
Line 733: Mocks and test fragility
Line 734: hexagon has six sides, it doesn’t mean your application can only connect to six
Line 735: other applications. The number of connections is arbitrary. The point is that
Line 736: there can be many such connections.
Line 737: Each layer of your application exhibits observable behavior and contains its own set of
Line 738: implementation details. For example, observable behavior of the domain layer is the
Line 739: sum of this layer’s operations and state that helps the application service layer achieve
Line 740: at least one of its goals. The principles of a well-designed API have a fractal nature:
Line 741: they apply equally to as much as a whole layer or as little as a single class.
Line 742:  When you make each layer’s API well-designed (that is, hide its implementation
Line 743: details), your tests also start to have a fractal structure; they verify behavior that helps
Line 744: achieve the same goals but at different levels. A test covering an application service
Line 745: checks to see how this service attains an overarching, coarse-grained goal posed by the
Line 746: external client. At the same time, a test working with a domain class verifies a subgoal
Line 747: that is part of that greater goal (figure 5.10).
Line 748: You might remember from previous chapters how I mentioned that you should be
Line 749: able to trace any test back to a particular business requirement. Each test should tell a
Line 750: story that is meaningful to a domain expert, and if it doesn’t, that’s a strong indication
Line 751: that the test couples to implementation details and therefore is brittle. I hope now you
Line 752: can see why.
Line 753:  Observable behavior flows inward from outer layers to the center. The overarching
Line 754: goal posed by the external client gets translated into subgoals achieved by individual
Line 755: Goal
Line 756: (use case)
Line 757: Subgoal
Line 758: Subgoal
Line 759: Test 1
Line 760: Test 2
Line 761: Test 3
Line 762: External client
Line 763: Application service
Line 764: Domain class 1
Line 765: Domain class 2
Line 766: Figure 5.10
Line 767: Tests working with different layers have a fractal nature: they verify the 
Line 768: same behavior at different levels. A test of an application service checks to see how 
Line 769: the overall business use case is executed. A test working with a domain class verifies 
Line 770: an intermediate subgoal on the way to use-case completion.
Line 771: 
Line 772: --- 페이지 131 ---
Line 773: 109
Line 774: The relationship between mocks and test fragility
Line 775: domain classes. Each piece of observable behavior in the domain layer therefore pre-
Line 776: serves the connection to a particular business use case. You can trace this connection
Line 777: recursively from the innermost (domain) layer outward to the application services
Line 778: layer and then to the needs of the external client. This traceability follows from the
Line 779: definition of observable behavior. For a piece of code to be part of observable behav-
Line 780: ior, it needs to help the client achieve one of its goals. For a domain class, the client is
Line 781: an application service; for the application service, it’s the external client itself.
Line 782:  Tests that verify a code base with a well-designed API also have a connection to
Line 783: business requirements because those tests tie to the observable behavior only. A good
Line 784: example is the User and UserController classes from listing 5.6 (I’m repeating the
Line 785: code here for convenience).
Line 786: public class User
Line 787: {
Line 788: private string _name;
Line 789: public string Name
Line 790: {
Line 791: get => _name;
Line 792: set => _name = NormalizeName(value);
Line 793: }
Line 794: private string NormalizeName(string name)
Line 795: {
Line 796: /* Trim name down to 50 characters */
Line 797: }
Line 798: }
Line 799: public class UserController
Line 800: {
Line 801: public void RenameUser(int userId, string newName)
Line 802: {
Line 803: User user = GetUserFromDatabase(userId);
Line 804: user.Name = newName;
Line 805: SaveUserToDatabase(user);
Line 806: }
Line 807: }
Line 808: UserController in this example is an application service. Assuming that the exter-
Line 809: nal client doesn’t have a specific goal of normalizing user names, and all names are
Line 810: normalized solely due to restrictions from the application itself, the NormalizeName
Line 811: method in the User class can’t be traced to the client’s needs. Therefore, it’s an
Line 812: implementation detail and should be made private (we already did that earlier in
Line 813: this chapter). Moreover, tests shouldn’t check this method directly. They should ver-
Line 814: ify it only as part of the class’s observable behavior—the Name property’s setter in
Line 815: this example.
Line 816:  This guideline of always tracing the code base’s public API to business require-
Line 817: ments applies to the vast majority of domain classes and application services but less
Line 818: Listing 5.8
Line 819: A domain class with an application service
Line 820: 
Line 821: --- 페이지 132 ---
Line 822: 110
Line 823: CHAPTER 5
Line 824: Mocks and test fragility
Line 825: so to utility and infrastructure code. The individual problems such code solves are
Line 826: often too low-level and fine-grained and can’t be traced to a specific business use case. 
Line 827: 5.3.2
Line 828: Intra-system vs. inter-system communications
Line 829: There are two types of communications in a typical application: intra-system and inter-
Line 830: system. Intra-system communications are communications between classes inside your
Line 831: application. Inter-system communications are when your application talks to other appli-
Line 832: cations (figure 5.11).
Line 833: NOTE
Line 834: Intra-system communications are implementation details; inter-system
Line 835: communications are not.
Line 836: Intra-system communications are implementation details because the collaborations
Line 837: your domain classes go through in order to perform an operation are not part of their
Line 838: observable behavior. These collaborations don’t have an immediate connection to the
Line 839: client’s goal. Thus, coupling to such collaborations leads to fragile tests.
Line 840:  Inter-system communications are a different matter. Unlike collaborations between
Line 841: classes inside your application, the way your system talks to the external world forms
Line 842: the observable behavior of that system as a whole. It’s part of the contract your appli-
Line 843: cation must hold at all times (figure 5.12).
Line 844:  This attribute of inter-system communications stems from the way separate applica-
Line 845: tions evolve together. One of the main principles of such an evolution is maintaining
Line 846: backward compatibility. Regardless of the refactorings you perform inside your sys-
Line 847: tem, the communication pattern it uses to talk to external applications should always
Line 848: stay in place, so that external applications can understand it. For example, messages
Line 849: your application emits on a bus should preserve their structure, the calls issued to an
Line 850: SMTP service should have the same number and type of parameters, and so on.
Line 851: Third-party
Line 852: system
Line 853: SMTP service
Line 854: Intra-system
Line 855: Inter-system
Line 856: Inter-system
Line 857: Figure 5.11
Line 858: There are two types 
Line 859: of communications: intra-system 
Line 860: (between classes inside the 
Line 861: application) and inter-system 
Line 862: (between applications).
Line 863: 
Line 864: --- 페이지 133 ---
Line 865: 111
Line 866: The relationship between mocks and test fragility
Line 867: The use of mocks is beneficial when verifying the communication pattern between
Line 868: your system and external applications. Conversely, using mocks to verify communica-
Line 869: tions between classes inside your system results in tests that couple to implementation
Line 870: details and therefore fall short of the resistance-to-refactoring metric.
Line 871: 5.3.3
Line 872: Intra-system vs. inter-system communications: An example
Line 873: To illustrate the difference between intra-system and inter-system communications, I’ll
Line 874: expand on the example with the Customer and Store classes that I used in chapter 2
Line 875: and earlier in this chapter. Imagine the following business use case:
Line 876: A customer tries to purchase a product from a store.
Line 877: If the amount of the product in the store is sufficient, then
Line 878: – The inventory is removed from the store.
Line 879: – An email receipt is sent to the customer.
Line 880: – A confirmation is returned.
Line 881: Let’s also assume that the application is an API with no user interface.
Line 882:  In the following listing, the CustomerController class is an application service that
Line 883: orchestrates the work between domain classes (Customer, Product, Store) and the
Line 884: external application (EmailGateway, which is a proxy to an SMTP service).
Line 885: public class CustomerController
Line 886: {
Line 887: public bool Purchase(int customerId, int productId, int quantity)
Line 888: Listing 5.9
Line 889: Connecting the domain model with external applications
Line 890: Third-party
Line 891: system
Line 892: SMTP service
Line 893: Implementation detail
Line 894: Observable behavior (contract)
Line 895: Observable behavior (contract)
Line 896: Figure 5.12
Line 897: Inter-system communications form the observable 
Line 898: behavior of your application as a whole. Intra-system communications 
Line 899: are implementation details.
Line 900: 
Line 901: --- 페이지 134 ---
Line 902: 112
Line 903: CHAPTER 5
Line 904: Mocks and test fragility
Line 905: {
Line 906: Customer customer = _customerRepository.GetById(customerId);
Line 907: Product product = _productRepository.GetById(productId);
Line 908: bool isSuccess = customer.Purchase(
Line 909: _mainStore, product, quantity);
Line 910: if (isSuccess)
Line 911: {
Line 912: _emailGateway.SendReceipt(
Line 913: customer.Email, product.Name, quantity);
Line 914: }
Line 915: return isSuccess;
Line 916: }
Line 917: }
Line 918: Validation of input parameters is omitted for brevity. In the Purchase method, the
Line 919: customer checks to see if there’s enough inventory in the store and, if so, decreases
Line 920: the product amount.
Line 921:  The act of making a purchase is a business use case with both intra-system and
Line 922: inter-system communications. The inter-system communications are those between
Line 923: the CustomerController application service and the two external systems: the third-
Line 924: party application (which is also the client initiating the use case) and the email gate-
Line 925: way. The intra-system communication is between the Customer and the Store domain
Line 926: classes (figure 5.13).
Line 927:  In this example, the call to the SMTP service is a side effect that is visible to the
Line 928: external world and thus forms the observable behavior of the application as a whole.
Line 929: Third-party
Line 930: system
Line 931: (external
Line 932: client)
Line 933: SMTP service
Line 934: SendReceipt()
Line 935: Customer
Line 936: RemoveInventory()
Line 937: Store
Line 938: isSuccess
Line 939: Figure 5.13
Line 940: The example in listing 5.9 represented using the hexagonal 
Line 941: architecture. The communications between the hexagons are inter-system 
Line 942: communications. The communication inside the hexagon is intra-system.
Line 943: 
Line 944: --- 페이지 135 ---
Line 945: 113
Line 946: The relationship between mocks and test fragility
Line 947: It also has a direct connection to the client’s goals. The client of the application is the
Line 948: third-party system. This system’s goal is to make a purchase, and it expects the cus-
Line 949: tomer to receive a confirmation email as part of the successful outcome.
Line 950:  The call to the SMTP service is a legitimate reason to do mocking. It doesn’t lead
Line 951: to test fragility because you want to make sure this type of communication stays in
Line 952: place even after refactoring. The use of mocks helps you do exactly that.
Line 953:  The next listing shows an example of a legitimate use of mocks.
Line 954: [Fact]
Line 955: public void Successful_purchase()
Line 956: {
Line 957: var mock = new Mock<IEmailGateway>();
Line 958: var sut = new CustomerController(mock.Object);
Line 959: bool isSuccess = sut.Purchase(
Line 960: customerId: 1, productId: 2, quantity: 5);
Line 961: Assert.True(isSuccess);
Line 962: mock.Verify(
Line 963:   
Line 964: x => x.SendReceipt(
Line 965:   
Line 966: "customer@email.com", "Shampoo", 5),  
Line 967: Times.Once);
Line 968:   
Line 969: }
Line 970: Note that the isSuccess flag is also observable by the external client and also needs
Line 971: verification. This flag doesn’t need mocking, though; a simple value comparison is
Line 972: enough.
Line 973:  Let’s now look at a test that mocks the communication between Customer and
Line 974: Store.
Line 975: [Fact]
Line 976: public void Purchase_succeeds_when_enough_inventory()
Line 977: {
Line 978: var storeMock = new Mock<IStore>();
Line 979: storeMock
Line 980: .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
Line 981: .Returns(true);
Line 982: var customer = new Customer();
Line 983: bool success = customer.Purchase(
Line 984: storeMock.Object, Product.Shampoo, 5);
Line 985: Assert.True(success);
Line 986: storeMock.Verify(
Line 987: x => x.RemoveInventory(Product.Shampoo, 5),
Line 988: Times.Once);
Line 989: }
Line 990: Listing 5.10
Line 991: Mocking that doesn’t lead to fragile tests 
Line 992: Listing 5.11
Line 993: Mocking that leads to fragile tests 
Line 994: Verifies that the 
Line 995: system sent a receipt 
Line 996: about the purchase
Line 997: 
Line 998: --- 페이지 136 ---
Line 999: 114
Line 1000: CHAPTER 5
Line 1001: Mocks and test fragility
Line 1002: Unlike the communication between CustomerController and the SMTP service, the
Line 1003: RemoveInventory() method call from Customer to Store doesn’t cross the applica-
Line 1004: tion boundary: both the caller and the recipient reside inside the application. Also,
Line 1005: this method is neither an operation nor a state that helps the client achieve its goals.
Line 1006: The client of these two domain classes is CustomerController with the goal of making
Line 1007: a purchase. The only two members that have an immediate connection to this goal are
Line 1008: customer.Purchase() and store.GetInventory(). The Purchase() method initiates
Line 1009: the purchase, and GetInventory() shows the state of the system after the purchase is
Line 1010: completed. The RemoveInventory() method call is an intermediate step on the way to
Line 1011: the client’s goal—an implementation detail. 
Line 1012: 5.4
Line 1013: The classical vs. London schools of unit testing, 
Line 1014: revisited
Line 1015: As a reminder from chapter 2 (table 2.1), table 5.2 sums up the differences between
Line 1016: the classical and London schools of unit testing.
Line 1017: In chapter 2, I mentioned that I prefer the classical school of unit testing over the
Line 1018: London school. I hope now you can see why. The London school encourages the use
Line 1019: of mocks for all but immutable dependencies and doesn’t differentiate between intra-
Line 1020: system and inter-system communications. As a result, tests check communications
Line 1021: between classes just as much as they check communications between your application
Line 1022: and external systems.
Line 1023:  This indiscriminate use of mocks is why following the London school often results
Line 1024: in tests that couple to implementation details and thus lack resistance to refactoring.
Line 1025: As you may remember from chapter 4, the metric of resistance to refactoring (unlike
Line 1026: the other three) is mostly a binary choice: a test either has resistance to refactoring or
Line 1027: it doesn’t. Compromising on this metric renders the test nearly worthless.
Line 1028:  The classical school is much better at this issue because it advocates for substitut-
Line 1029: ing only dependencies that are shared between tests, which almost always translates
Line 1030: into out-of-process dependencies such as an SMTP service, a message bus, and so on.
Line 1031: But the classical school is not ideal in its treatment of inter-system communications,
Line 1032: either. This school also encourages excessive use of mocks, albeit not as much as the
Line 1033: London school.
Line 1034: Table 5.2
Line 1035: The differences between the London and classical schools of unit testing
Line 1036: Isolation of
Line 1037: A unit is
Line 1038: Uses test doubles for
Line 1039: London school
Line 1040: Units
Line 1041: A class
Line 1042: All but immutable dependencies
Line 1043: Classical school
Line 1044: Unit tests
Line 1045: A class or a set of classes
Line 1046: Shared dependencies
Line 1047: 
Line 1048: --- 페이지 137 ---
Line 1049: 115
Line 1050: The classical vs. London schools of unit testing, revisited
Line 1051: 5.4.1
Line 1052: Not all out-of-process dependencies should be mocked out
Line 1053: Before we discuss out-of-process dependencies and mocking, let me give you a quick
Line 1054: refresher on types of dependencies (refer to chapter 2 for more details):
Line 1055: Shared dependency—A dependency shared by tests (not production code)
Line 1056: Out-of-process dependency—A dependency hosted by a process other than the pro-
Line 1057: gram’s execution process (for example, a database, a message bus, or an SMTP
Line 1058: service)
Line 1059: Private dependency—Any dependency that is not shared
Line 1060: The classical school recommends avoiding shared dependencies because they provide
Line 1061: the means for tests to interfere with each other’s execution context and thus prevent
Line 1062: those tests from running in parallel. The ability for tests to run in parallel, sequen-
Line 1063: tially, and in any order is called test isolation.
Line 1064:  If a shared dependency is not out-of-process, then it’s easy to avoid reusing it in
Line 1065: tests by providing a new instance of it on each test run. In cases where the shared
Line 1066: dependency is out-of-process, testing becomes more complicated. You can’t instanti-
Line 1067: ate a new database or provision a new message bus before each test execution; that
Line 1068: would drastically slow down the test suite. The usual approach is to replace such
Line 1069: dependencies with test doubles—mocks and stubs.
Line 1070:  Not all out-of-process dependencies should be mocked out, though. If an out-of-
Line 1071: process dependency is only accessible through your application, then communications with such a
Line 1072: dependency are not part of your system’s observable behavior. An out-of-process dependency
Line 1073: that can’t be observed externally, in effect, acts as part of your application (figure 5.14).
Line 1074:  Remember, the requirement to always preserve the communication pattern
Line 1075: between your application and external systems stems from the necessity to maintain
Line 1076: backward compatibility. You have to maintain the way your application talks to external
Line 1077: Third-party
Line 1078: system
Line 1079: (external
Line 1080: client)
Line 1081: SMTP service
Line 1082: Observable behavior (contract)
Line 1083: Application
Line 1084: database
Line 1085: (accessible
Line 1086: only by the
Line 1087: application)
Line 1088: Implementation details
Line 1089: Figure 5.14
Line 1090: Communications with an out-of-process dependency that can’t be 
Line 1091: observed externally are implementation details. They don’t have to stay in place 
Line 1092: after refactoring and therefore shouldn’t be verified with mocks.
Line 1093: 
Line 1094: --- 페이지 138 ---
Line 1095: 116
Line 1096: CHAPTER 5
Line 1097: Mocks and test fragility
Line 1098: systems. That’s because you can’t change those external systems simultaneously with
Line 1099: your application; they may follow a different deployment cycle, or you might simply
Line 1100: not have control over them.
Line 1101:  But when your application acts as a proxy to an external system, and no client can
Line 1102: access it directly, the backward-compatibility requirement vanishes. Now you can deploy
Line 1103: your application together with this external system, and it won’t affect the clients. The
Line 1104: communication pattern with such a system becomes an implementation detail.
Line 1105:  A good example here is an application database: a database that is used only by
Line 1106: your application. No external system has access to this database. Therefore, you can
Line 1107: modify the communication pattern between your system and the application database
Line 1108: in any way you like, as long as it doesn’t break existing functionality. Because that data-
Line 1109: base is completely hidden from the eyes of the clients, you can even replace it with an
Line 1110: entirely different storage mechanism, and no one will notice.
Line 1111:  The use of mocks for out-of-process dependencies that you have a full control over
Line 1112: also leads to brittle tests. You don’t want your tests to turn red every time you split a
Line 1113: table in the database or modify the type of one of the parameters in a stored proce-
Line 1114: dure. The database and your application must be treated as one system.
Line 1115:  This obviously poses an issue. How would you test the work with such a depen-
Line 1116: dency without compromising the feedback speed, the third attribute of a good unit
Line 1117: test? You’ll see this subject covered in depth in the following two chapters. 
Line 1118: 5.4.2
Line 1119: Using mocks to verify behavior
Line 1120: Mocks are often said to verify behavior. In the vast majority of cases, they don’t. The
Line 1121: way each individual class interacts with neighboring classes in order to achieve some
Line 1122: goal has nothing to do with observable behavior; it’s an implementation detail.
Line 1123:  Verifying communications between classes is akin to trying to derive a person’s
Line 1124: behavior by measuring the signals that neurons in the brain pass among each other.
Line 1125: Such a level of detail is too granular. What matters is the behavior that can be traced
Line 1126: back to the client goals. The client doesn’t care what neurons in your brain light up
Line 1127: when they ask you to help. The only thing that matters is the help itself—provided by
Line 1128: you in a reliable and professional fashion, of course. Mocks have something to do with
Line 1129: behavior only when they verify interactions that cross the application boundary and
Line 1130: only when the side effects of those interactions are visible to the external world. 
Line 1131: Summary
Line 1132: Test double is an overarching term that describes all kinds of non-production-
Line 1133: ready, fake dependencies in tests. There are five variations of test doubles—
Line 1134: dummy, stub, spy, mock, and fake—that can be grouped in just two types: mocks
Line 1135: and stubs. Spies are functionally the same as mocks; dummies and fakes serve
Line 1136: the same role as stubs.
Line 1137: Mocks help emulate and examine outcoming interactions: calls from the SUT to
Line 1138: its dependencies that change the state of those dependencies. Stubs help
Line 1139: 
Line 1140: --- 페이지 139 ---
Line 1141: 117
Line 1142: Summary
Line 1143: emulate incoming interactions: calls the SUT makes to its dependencies to get
Line 1144: input data.
Line 1145: A mock (the tool) is a class from a mocking library that you can use to create a
Line 1146: mock (the test double) or a stub.
Line 1147: Asserting interactions with stubs leads to fragile tests. Such an interaction doesn’t
Line 1148: correspond to the end result; it’s an intermediate step on the way to that result,
Line 1149: an implementation detail.
Line 1150: The command query separation (CQS) principle states that every method
Line 1151: should be either a command or a query but not both. Test doubles that substi-
Line 1152: tute commands are mocks. Test doubles that substitute queries are stubs.
Line 1153: All production code can be categorized along two dimensions: public API ver-
Line 1154: sus private API, and observable behavior versus implementation details. Code
Line 1155: publicity is controlled by access modifiers, such as private, public, and
Line 1156: internal keywords. Code is part of observable behavior when it meets one of
Line 1157: the following requirements (any other code is an implementation detail):
Line 1158: – It exposes an operation that helps the client achieve one of its goals. An oper-
Line 1159: ation is a method that performs a calculation or incurs a side effect.
Line 1160: – It exposes a state that helps the client achieve one of its goals. State is the cur-
Line 1161: rent condition of the system.
Line 1162: Well-designed code is code whose observable behavior coincides with the public
Line 1163: API and whose implementation details are hidden behind the private API. A
Line 1164: code leaks implementation details when its public API extends beyond the
Line 1165: observable behavior.
Line 1166: Encapsulation is the act of protecting your code against invariant violations.
Line 1167: Exposing implementation details often entails a breach in encapsulation
Line 1168: because clients can use implementation details to bypass the code’s invariants.
Line 1169: Hexagonal architecture is a set of interacting applications represented as hexa-
Line 1170: gons. Each hexagon consists of two layers: domain and application services.
Line 1171: Hexagonal architecture emphasizes three important aspects:
Line 1172: – Separation of concerns between the domain and application services layers.
Line 1173: The domain layer should be responsible for the business logic, while the
Line 1174: application services should orchestrate the work between the domain layer
Line 1175: and external applications.
Line 1176: – A one-way flow of dependencies from the application services layer to the
Line 1177: domain layer. Classes inside the domain layer should only depend on each
Line 1178: other; they should not depend on classes from the application services layer.
Line 1179: – External applications connect to your application through a common inter-
Line 1180: face maintained by the application services layer. No one has a direct access
Line 1181: to the domain layer.
Line 1182: Each layer in a hexagon exhibits observable behavior and contains its own set of
Line 1183: implementation details.
Line 1184: 
Line 1185: --- 페이지 140 ---
Line 1186: 118
Line 1187: CHAPTER 5
Line 1188: Mocks and test fragility
Line 1189: There are two types of communications in an application: intra-system and
Line 1190: inter-system. Intra-system communications are communications between classes
Line 1191: inside the application. Inter-system communication is when the application talks
Line 1192: to external applications.
Line 1193: Intra-system communications are implementation details. Inter-system commu-
Line 1194: nications are part of observable behavior, with the exception of external systems
Line 1195: that are accessible only through your application. Interactions with such sys-
Line 1196: tems are implementation details too, because the resulting side effects are not
Line 1197: observed externally.
Line 1198: Using mocks to assert intra-system communications leads to fragile tests. Mock-
Line 1199: ing is legitimate only when it’s used for inter-system communications—commu-
Line 1200: nications that cross the application boundary—and only when the side effects
Line 1201: of those communications are visible to the external world.