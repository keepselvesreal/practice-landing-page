Line 1: 
Line 2: --- 페이지 63 ---
Line 3: 41
Line 4: The anatomy of
Line 5: a unit test
Line 6: In this remaining chapter of part 1, I’ll give you a refresher on some basic topics.
Line 7: I’ll go over the structure of a typical unit test, which is usually represented by the
Line 8: arrange, act, and assert (AAA) pattern. I’ll also show the unit testing framework of
Line 9: my choice—xUnit—and explain why I’m using it and not one of its competitors.
Line 10:  Along the way, we’ll talk about naming unit tests. There are quite a few compet-
Line 11: ing pieces of advice on this topic, and unfortunately, most of them don’t do a good
Line 12: enough job improving your unit tests. In this chapter, I describe those less-useful
Line 13: naming practices and show why they usually aren’t the best choice. Instead of those
Line 14: practices, I give you an alternative—a simple, easy-to-follow guideline for naming
Line 15: tests in a way that makes them readable not only to the programmer who wrote
Line 16: them, but also to any other person familiar with the problem domain.
Line 17:  Finally, I’ll talk about some features of the framework that help streamline the
Line 18: process of unit testing. Don’t worry about this information being too specific to C#
Line 19: This chapter covers
Line 20: The structure of a unit test
Line 21: Unit test naming best practices
Line 22: Working with parameterized tests
Line 23: Working with fluent assertions
Line 24: 
Line 25: --- 페이지 64 ---
Line 26: 42
Line 27: CHAPTER 3
Line 28: The anatomy of a unit test
Line 29: and .NET; most unit testing frameworks exhibit similar functionality, regardless of
Line 30: the programming language. If you learn one of them, you won’t have problems work-
Line 31: ing with another.
Line 32: 3.1
Line 33: How to structure a unit test
Line 34: This section shows how to structure unit tests using the arrange, act, and assert pat-
Line 35: tern, what pitfalls to avoid, and how to make your tests as readable as possible.
Line 36: 3.1.1
Line 37: Using the AAA pattern
Line 38: The AAA pattern advocates for splitting each test into three parts: arrange, act, and
Line 39: assert. (This pattern is sometimes also called the 3A pattern.) Let’s take a Calculator
Line 40: class with a single method that calculates a sum of two numbers:
Line 41: public class Calculator
Line 42: {
Line 43: public double Sum(double first, double second)
Line 44: {
Line 45: return first + second;
Line 46: }
Line 47: }
Line 48: The following listing shows a test that verifies the class’s behavior. This test follows the
Line 49: AAA pattern.
Line 50: public class CalculatorTests         
Line 51: {
Line 52: [Fact]    
Line 53: public void Sum_of_two_numbers()   
Line 54: {
Line 55: // Arrange
Line 56: double first = 10;
Line 57:    
Line 58: double second = 20;
Line 59:    
Line 60: var calculator = new Calculator();  
Line 61: // Act
Line 62: double result = calculator.Sum(first, second);    
Line 63: // Assert
Line 64: Assert.Equal(30, result);   
Line 65: }
Line 66: }
Line 67: The AAA pattern provides a simple, uniform structure for all tests in the suite. This
Line 68: uniformity is one of the biggest advantages of this pattern: once you get used to it, you
Line 69: can easily read and understand any test. That, in turn, reduces maintenance costs for
Line 70: your entire test suite. The structure is as follows:
Line 71: Listing 3.1
Line 72: A test covering the Sum method in calculator
Line 73: Class-container for a 
Line 74: cohesive set of tests
Line 75: xUnit’s attribute 
Line 76: indicating a test
Line 77: Name of the
Line 78: unit test
Line 79: Arrange 
Line 80: section
Line 81: Act section
Line 82: Assert section
Line 83: 
Line 84: --- 페이지 65 ---
Line 85: 43
Line 86: How to structure a unit test
Line 87: In the arrange section, you bring the system under test (SUT) and its dependen-
Line 88: cies to a desired state.
Line 89: In the act section, you call methods on the SUT, pass the prepared dependen-
Line 90: cies, and capture the output value (if any).
Line 91: In the assert section, you verify the outcome. The outcome may be represented
Line 92: by the return value, the final state of the SUT and its collaborators, or the meth-
Line 93: ods the SUT called on those collaborators.
Line 94: The natural inclination is to start writing a test with the arrange section. After all, it
Line 95: comes before the other two. This approach works well in the vast majority of cases, but
Line 96: starting with the assert section is a viable option too. When you practice Test-Driven
Line 97: Development (TDD)—that is, when you create a failing test before developing a
Line 98: feature—you don’t know enough about the feature’s behavior yet. So, it becomes
Line 99: advantageous to first outline what you expect from the behavior and then figure out
Line 100: how to develop the system to meet this expectation.
Line 101:  Such a technique may look counterintuitive, but it’s how we approach problem
Line 102: solving. We start by thinking about the objective: what a particular behavior should to
Line 103: do for us. The actual solving of the problem comes after that. Writing down the asser-
Line 104: tions before everything else is merely a formalization of this thinking process. But
Line 105: again, this guideline is only applicable when you follow TDD—when you write a test
Line 106: before the production code. If you write the production code before the test, by the
Line 107: time you move on to the test, you already know what to expect from the behavior, so
Line 108: starting with the arrange section is a better option. 
Line 109: 3.1.2
Line 110: Avoid multiple arrange, act, and assert sections
Line 111: Occasionally, you may encounter a test with multiple arrange, act, or assert sections. It
Line 112: usually works as shown in figure 3.1.
Line 113:  When you see multiple act sections separated by assert and, possibly, arrange sec-
Line 114: tions, it means the test verifies multiple units of behavior. And, as we discussed in
Line 115: chapter 2, such a test is no longer a unit test but rather is an integration test. It’s best
Line 116: Given-When-Then pattern
Line 117: You might have heard of the Given-When-Then pattern, which is similar to AAA. This
Line 118: pattern also advocates for breaking the test down into three parts:
Line 119: Given—Corresponds to the arrange section
Line 120: When—Corresponds to the act section
Line 121: Then—Corresponds to the assert section
Line 122: There’s no difference between the two patterns in terms of the test composition. The
Line 123: only distinction is that the Given-When-Then structure is more readable to non-
Line 124: programmers. Thus, Given-When-Then is more suitable for tests that are shared with
Line 125: non-technical people.
Line 126: 
Line 127: --- 페이지 66 ---
Line 128: 44
Line 129: CHAPTER 3
Line 130: The anatomy of a unit test
Line 131: to avoid such a test structure. A single action ensures that your tests remain within the
Line 132: realm of unit testing, which means they are simple, fast, and easy to understand. If you
Line 133: see a test containing a sequence of actions and assertions, refactor it. Extract each act
Line 134: into a test of its own.
Line 135:  It’s sometimes fine to have multiple act sections in integration tests. As you may
Line 136: remember from the previous chapter, integration tests can be slow. One way to speed
Line 137: them up is to group several integration tests together into a single test with multiple
Line 138: acts and assertions. It’s especially helpful when system states naturally flow from one
Line 139: another: that is, when an act simultaneously serves as an arrange for the subsequent act.
Line 140:  But again, this optimization technique is only applicable to integration tests—and
Line 141: not all of them, but rather those that are already slow and that you don’t want to
Line 142: become even slower. There’s no need for such an optimization in unit tests or integra-
Line 143: tion tests that are fast enough. It’s always better to split a multistep unit test into sev-
Line 144: eral tests. 
Line 145: 3.1.3
Line 146: Avoid if statements in tests
Line 147: Similar to multiple occurrences of the arrange, act, and assert sections, you may some-
Line 148: times encounter a unit test with an if statement. This is also an anti-pattern. A test—
Line 149: whether a unit test or an integration test—should be a simple sequence of steps with
Line 150: no branching.
Line 151:  An if statement indicates that the test verifies too many things at once. Such a test,
Line 152: therefore, should be split into several tests. But unlike the situation with multiple AAA
Line 153: Arrange the test
Line 154: Act
Line 155: Assert
Line 156: Act some more
Line 157: Assert again
Line 158: Figure 3.1
Line 159: Multiple arrange, act, and assert sections are a hint that the test verifies 
Line 160: too many things at once. Such a test needs to be split into several tests to fix the 
Line 161: problem.
Line 162: 
Line 163: --- 페이지 67 ---
Line 164: 45
Line 165: How to structure a unit test
Line 166: sections, there’s no exception for integration tests. There are no benefits in branching
Line 167: within a test. You only gain additional maintenance costs: if statements make the tests
Line 168: harder to read and understand. 
Line 169: 3.1.4
Line 170: How large should each section be?
Line 171: A common question people ask when starting out with the AAA pattern is, how large
Line 172: should each section be? And what about the teardown section—the section that cleans
Line 173: up after the test? There are different guidelines regarding the size for each of the test
Line 174: sections.
Line 175: THE ARRANGE SECTION IS THE LARGEST
Line 176: The arrange section is usually the largest of the three. It can be as large as the act and
Line 177: assert sections combined. But if it becomes significantly larger than that, it’s better to
Line 178: extract the arrangements either into private methods within the same test class or to a
Line 179: separate factory class. Two popular patterns can help you reuse the code in the arrange
Line 180: sections: Object Mother and Test Data Builder. 
Line 181: WATCH OUT FOR ACT SECTIONS THAT ARE LARGER THAN A SINGLE LINE
Line 182: The act section is normally just a single line of code. If the act consists of two or more
Line 183: lines, it could indicate a problem with the SUT’s public API.
Line 184:  It’s best to express this point with an example, so let’s take one from chapter 2,
Line 185: which I repeat in the following listing. In this example, the customer makes a pur-
Line 186: chase from a store.
Line 187: [Fact]
Line 188: public void Purchase_succeeds_when_enough_inventory()
Line 189: {
Line 190: // Arrange
Line 191: var store = new Store();
Line 192: store.AddInventory(Product.Shampoo, 10);
Line 193: var customer = new Customer();
Line 194: // Act
Line 195: bool success = customer.Purchase(store, Product.Shampoo, 5);
Line 196: // Assert
Line 197: Assert.True(success);
Line 198: Assert.Equal(5, store.GetInventory(Product.Shampoo));
Line 199: }
Line 200: Notice that the act section in this test is a single method call, which is a sign of a well-
Line 201: designed class’s API. Now compare it to the version in listing 3.3: this act section con-
Line 202: tains two lines. And that’s a sign of a problem with the SUT: it requires the client to
Line 203: remember to make the second method call to finish the purchase and thus lacks
Line 204: encapsulation.
Line 205:  
Line 206: Listing 3.2
Line 207: A single-line act section 
Line 208: 
Line 209: --- 페이지 68 ---
Line 210: 46
Line 211: CHAPTER 3
Line 212: The anatomy of a unit test
Line 213: [Fact]
Line 214: public void Purchase_succeeds_when_enough_inventory()
Line 215: {
Line 216: // Arrange
Line 217: var store = new Store();
Line 218: store.AddInventory(Product.Shampoo, 10);
Line 219: var customer = new Customer();
Line 220: // Act
Line 221: bool success = customer.Purchase(store, Product.Shampoo, 5);
Line 222: store.RemoveInventory(success, Product.Shampoo, 5);
Line 223: // Assert
Line 224: Assert.True(success);
Line 225: Assert.Equal(5, store.GetInventory(Product.Shampoo));
Line 226: }
Line 227: Here’s what you can read from listing 3.3’s act section:
Line 228: In the first line, the customer tries to acquire five units of shampoo from the
Line 229: store.
Line 230: In the second line, the inventory is removed from the store. The removal takes
Line 231: place only if the preceding call to Purchase() returns a success.
Line 232: The issue with the new version is that it requires two method calls to perform a single
Line 233: operation. Note that this is not an issue with the test itself. The test still verifies the
Line 234: same unit of behavior: the process of making a purchase. The issue lies in the API sur-
Line 235: face of the Customer class. It shouldn’t require the client to make an additional
Line 236: method call.
Line 237:  From a business perspective, a successful purchase has two outcomes: the acquisi-
Line 238: tion of a product by the customer and the reduction of the inventory in the store.
Line 239: Both of these outcomes must be achieved together, which means there should be a
Line 240: single public method that does both things. Otherwise, there’s a room for inconsis-
Line 241: tency if the client code calls the first method but not the second, in which case the cus-
Line 242: tomer will acquire the product but its available amount won’t be reduced in the store.
Line 243:  Such an inconsistency is called an invariant violation. The act of protecting your
Line 244: code against potential inconsistencies is called encapsulation. When an inconsistency
Line 245: penetrates into the database, it becomes a big problem: now it’s impossible to reset
Line 246: the state of your application by simply restarting it. You’ll have to deal with the cor-
Line 247: rupted data in the database and, potentially, contact customers and handle the situation
Line 248: on a case-by-case basis. Just imagine what would happen if the application generated
Line 249: confirmation receipts without actually reserving the inventory. It might issue claims
Line 250: to, and even charge for, more inventory than you could feasibly acquire in the near
Line 251: future.
Line 252:  The remedy is to maintain code encapsulation at all times. In the previous exam-
Line 253: ple, the customer should remove the acquired inventory from the store as part of its
Line 254: Listing 3.3
Line 255: A two-line act section 
Line 256: 
Line 257: --- 페이지 69 ---
Line 258: 47
Line 259: How to structure a unit test
Line 260: Purchase method and not rely on the client code to do so. When it comes to main-
Line 261: taining invariants, you should eliminate any potential course of action that could lead
Line 262: to an invariant violation.
Line 263:  This guideline of keeping the act section down to a single line holds true for the
Line 264: vast majority of code that contains business logic, but less so for utility or infrastruc-
Line 265: ture code. Thus, I won’t say “never do it.” Be sure to examine each such case for a
Line 266: potential breach in encapsulation, though. 
Line 267: 3.1.5
Line 268: How many assertions should the assert section hold?
Line 269: Finally, there’s the assert section. You may have heard about the guideline of having
Line 270: one assertion per test. It takes root in the premise discussed in the previous chapter:
Line 271: the premise of targeting the smallest piece of code possible.
Line 272:  As you already know, this premise is incorrect. A unit in unit testing is a unit of
Line 273: behavior, not a unit of code. A single unit of behavior can exhibit multiple outcomes,
Line 274: and it’s fine to evaluate them all in one test.
Line 275:  Having that said, you need to watch out for assertion sections that grow too large:
Line 276: it could be a sign of a missing abstraction in the production code. For example,
Line 277: instead of asserting all properties inside an object returned by the SUT, it may be bet-
Line 278: ter to define proper equality members in the object’s class. You can then compare the
Line 279: object to an expected value using a single assertion. 
Line 280: 3.1.6
Line 281: What about the teardown phase?
Line 282: Some people also distinguish a fourth section, teardown, which comes after arrange, act,
Line 283: and assert. For example, you can use this section to remove any files created by the
Line 284: test, close a database connection, and so on. The teardown is usually represented by a
Line 285: separate method, which is reused across all tests in the class. Thus, I don’t include this
Line 286: phase in the AAA pattern.
Line 287:  Note that most unit tests don’t need teardown. Unit tests don’t talk to out-of-process
Line 288: dependencies and thus don’t leave side effects that need to be disposed of. That’s a
Line 289: realm of integration testing. We’ll talk more about how to properly clean up after inte-
Line 290: gration tests in part 3. 
Line 291: 3.1.7
Line 292: Differentiating the system under test
Line 293: The SUT plays a significant role in tests. It provides an entry point for the behavior
Line 294: you want to invoke in the application. As we discussed in the previous chapter, this
Line 295: behavior can span across as many as several classes or as little as a single method. But
Line 296: there can be only one entry point: one class that triggers that behavior.
Line 297:  Thus it’s important to differentiate the SUT from its dependencies, especially
Line 298: when there are quite a few of them, so that you don’t need to spend too much time
Line 299: figuring out who is who in the test. To do that, always name the SUT in tests sut. The
Line 300: following listing shows how CalculatorTests would look after renaming the Calcu-
Line 301: lator instance.
Line 302: 
Line 303: --- 페이지 70 ---
Line 304: 48
Line 305: CHAPTER 3
Line 306: The anatomy of a unit test
Line 307: public class CalculatorTests
Line 308: {
Line 309: [Fact]
Line 310: public void Sum_of_two_numbers()
Line 311: {
Line 312: // Arrange
Line 313: double first = 10;
Line 314: double second = 20;
Line 315: var sut = new Calculator();    
Line 316: // Act
Line 317: double result = sut.Sum(first, second);
Line 318: // Assert
Line 319: Assert.Equal(30, result);
Line 320: }
Line 321: }
Line 322: 3.1.8
Line 323: Dropping the arrange, act, and assert comments from tests
Line 324: Just as it’s important to set the SUT apart from its dependencies, it’s also important to
Line 325: differentiate the three sections from each other, so that you don’t spend too much
Line 326: time figuring out what section a particular line in the test belongs to. One way to do
Line 327: that is to put // Arrange, // Act, and // Assert comments before the beginning of
Line 328: each section. Another way is to separate the sections with empty lines, as shown next.
Line 329: public class CalculatorTests
Line 330: {
Line 331: [Fact]
Line 332: public void Sum_of_two_numbers()
Line 333: {
Line 334: double first = 10;
Line 335:    
Line 336: double second = 20;
Line 337:   
Line 338: var sut = new Calculator();  
Line 339: double result = sut.Sum(first, second);   
Line 340: Assert.Equal(30, result);   
Line 341: }
Line 342: }
Line 343: Separating sections with empty lines works great in most unit tests. It allows you to
Line 344: keep a balance between brevity and readability. It doesn’t work as well in large tests,
Line 345: though, where you may want to put additional empty lines inside the arrange section
Line 346: to differentiate between configuration stages. This is often the case in integration
Line 347: tests—they frequently contain complicated setup logic. Therefore,
Line 348: Listing 3.4
Line 349: Differentiating the SUT from its dependencies
Line 350: Listing 3.5
Line 351: Calculator with sections separated by empty lines
Line 352: The calculator is 
Line 353: now called sut. 
Line 354: Arrange
Line 355: Act
Line 356: Assert
Line 357: 
Line 358: --- 페이지 71 ---
Line 359: 49
Line 360: Exploring the xUnit testing framework
Line 361: Drop the section comments in tests that follow the AAA pattern and where you
Line 362: can avoid additional empty lines inside the arrange and assert sections.
Line 363: Keep the section comments otherwise. 
Line 364: 3.2
Line 365: Exploring the xUnit testing framework
Line 366: In this section, I give a brief overview of unit testing tools available in .NET, and
Line 367: their features. I’m using xUnit (https://github.com/xunit/xunit) as the unit testing
Line 368: framework (note that you need to install the xunit.runner.visualstudio NuGet
Line 369: package in order to run xUnit tests from Visual Studio). Although this framework
Line 370: works in .NET only, every object-oriented language (Java, C++, JavaScript, and so
Line 371: on) has unit testing frameworks, and all those frameworks look quite similar to each
Line 372: other. If you’ve worked with one of them, you won’t have any issues working with
Line 373: another.
Line 374:  In .NET alone, there are several alternatives to choose from, such as NUnit
Line 375: (https://github.com/nunit/nunit) and the built-in Microsoft MSTest. I personally
Line 376: prefer xUnit for the reasons I’ll describe shortly, but you can also use NUnit; these two
Line 377: frameworks are pretty much on par in terms of functionality. I don’t recommend
Line 378: MSTest, though; it doesn’t provide the same level of flexibility as xUnit and NUnit.
Line 379: And don’t take my word for it—even people inside Microsoft refrain from using
Line 380: MSTest. For example, the ASP.NET Core team uses xUnit.
Line 381:  I prefer xUnit because it’s a cleaner, more concise version of NUnit. For example,
Line 382: you may have noticed that in the tests I’ve brought up so far, there are no framework-
Line 383: related attributes other than [Fact], which marks the method as a unit test so the unit
Line 384: testing framework knows to run it. There are no [TestFixture] attributes; any public
Line 385: class can contain a unit test. There’s also no [SetUp] or [TearDown]. If you need to
Line 386: share configuration logic between tests, you can put it inside the constructor. And if
Line 387: you need to clean something up, you can implement the IDisposable interface, as
Line 388: shown in this listing.
Line 389: public class CalculatorTests : IDisposable
Line 390: {
Line 391: private readonly Calculator _sut;
Line 392: public CalculatorTests()
Line 393:    
Line 394: {
Line 395:    
Line 396: _sut = new Calculator();   
Line 397: }
Line 398:    
Line 399: [Fact]
Line 400: public void Sum_of_two_numbers()
Line 401: {
Line 402: /* ... */
Line 403: }
Line 404: Listing 3.6
Line 405: Arrangement and teardown logic, shared by all tests
Line 406: Called before 
Line 407: each test in 
Line 408: the class
Line 409: 
Line 410: --- 페이지 72 ---
Line 411: 50
Line 412: CHAPTER 3
Line 413: The anatomy of a unit test
Line 414: public void Dispose()   
Line 415: {
Line 416:    
Line 417: _sut.CleanUp();
Line 418:    
Line 419: }
Line 420:    
Line 421: }
Line 422: As you can see, the xUnit authors took significant steps toward simplifying the
Line 423: framework. A lot of notions that previously required additional configuration (like
Line 424: [TestFixture] or [SetUp] attributes) now rely on conventions or built-in language
Line 425: constructs.
Line 426:  I particularly like the [Fact] attribute, specifically because it’s called Fact and not
Line 427: Test. It emphasizes the rule of thumb I mentioned in the previous chapter: each test
Line 428: should tell a story. This story is an individual, atomic scenario or fact about the problem
Line 429: domain, and the passing test is a proof that this scenario or fact holds true. If the test
Line 430: fails, it means either the story is no longer valid and you need to rewrite it, or the sys-
Line 431: tem itself has to be fixed.
Line 432:  I encourage you to adopt this way of thinking when you write unit tests. Your tests
Line 433: shouldn’t be a dull enumeration of what the production code does. Rather, they should
Line 434: provide a higher-level description of the application’s behavior. Ideally, this description
Line 435: should be meaningful not just to programmers but also to business people. 
Line 436: 3.3
Line 437: Reusing test fixtures between tests
Line 438: It’s important to know how and when to reuse code between tests. Reusing code
Line 439: between arrange sections is a good way to shorten and simplify your tests, and this sec-
Line 440: tion shows how to do that properly.
Line 441:  I mentioned earlier that often, fixture arrangements take up too much space. It
Line 442: makes sense to extract these arrangements into separate methods or classes that you
Line 443: then reuse between tests. There are two ways you can perform such reuse, but only
Line 444: one of them is beneficial; the other leads to increased maintenance costs.
Line 445: Test fixture
Line 446: The term test fixture has two common meanings:
Line 447: 1
Line 448: A test fixture is an object the test runs against. This object can be a regular
Line 449: dependency—an argument that is passed to the SUT. It can also be data in
Line 450: the database or a file on the hard disk. Such an object needs to remain in a
Line 451: known, fixed state before each test run, so it produces the same result.
Line 452: Hence the word fixture.
Line 453: 2
Line 454: The other definition comes from the NUnit testing framework. In NUnit, Test-
Line 455: Fixture is an attribute that marks a class containing tests.
Line 456: I use the first definition throughout this book.
Line 457: Called after 
Line 458: each test in 
Line 459: the class
Line 460: 
Line 461: --- 페이지 73 ---
Line 462: 51
Line 463: Reusing test fixtures between tests
Line 464: The first—incorrect—way to reuse test fixtures is to initialize them in the test’s con-
Line 465: structor (or the method marked with a [SetUp] attribute if you are using NUnit), as
Line 466: shown next.
Line 467: public class CustomerTests
Line 468: {
Line 469: private readonly Store _store;       
Line 470: private readonly Customer _sut;
Line 471: public CustomerTests()
Line 472:      
Line 473: {
Line 474:    
Line 475: _store = new Store();
Line 476:    
Line 477: _store.AddInventory(Product.Shampoo, 10);   
Line 478: _sut = new Customer();
Line 479:    
Line 480: }
Line 481:    
Line 482: [Fact]
Line 483: public void Purchase_succeeds_when_enough_inventory()
Line 484: {
Line 485: bool success = _sut.Purchase(_store, Product.Shampoo, 5);
Line 486: Assert.True(success);
Line 487: Assert.Equal(5, _store.GetInventory(Product.Shampoo));
Line 488: }
Line 489: [Fact]
Line 490: public void Purchase_fails_when_not_enough_inventory()
Line 491: {
Line 492: bool success = _sut.Purchase(_store, Product.Shampoo, 15);
Line 493: Assert.False(success);
Line 494: Assert.Equal(10, _store.GetInventory(Product.Shampoo));
Line 495: }
Line 496: }
Line 497: The two tests in listing 3.7 have common configuration logic. In fact, their arrange sec-
Line 498: tions are the same and thus can be fully extracted into CustomerTests’s constructor—
Line 499: which is precisely what I did here. The tests themselves no longer contain arrangements.
Line 500:  With this approach, you can significantly reduce the amount of test code—you can
Line 501: get rid of most or even all test fixture configurations in tests. But this technique has
Line 502: two significant drawbacks:
Line 503: It introduces high coupling between tests.
Line 504: It diminishes test readability.
Line 505: Let’s discuss these drawbacks in more detail.
Line 506: Listing 3.7
Line 507: Extracting the initialization code into the test constructor
Line 508: Common test 
Line 509: fixture
Line 510: Runs before 
Line 511: each test in 
Line 512: the class
Line 513: 
Line 514: --- 페이지 74 ---
Line 515: 52
Line 516: CHAPTER 3
Line 517: The anatomy of a unit test
Line 518: 3.3.1
Line 519: High coupling between tests is an anti-pattern
Line 520: In the new version, shown in listing 3.7, all tests are coupled to each other: a modifica-
Line 521: tion of one test’s arrangement logic will affect all tests in the class. For example, chang-
Line 522: ing this line
Line 523: _store.AddInventory(Product.Shampoo, 10);
Line 524: to this
Line 525: _store.AddInventory(Product.Shampoo, 15);
Line 526: would invalidate the assumption the tests make about the store’s initial state and there-
Line 527: fore would lead to unnecessary test failures.
Line 528:  That’s a violation of an important guideline: a modification of one test should not affect
Line 529: other tests. This guideline is similar to what we discussed in chapter 2—that tests should
Line 530: run in isolation from each other. It’s not the same, though. Here, we are talking about
Line 531: independent modification of tests, not independent execution. Both are important
Line 532: attributes of a well-designed test.
Line 533:  To follow this guideline, you need to avoid introducing shared state in test classes.
Line 534: These two private fields are examples of such a shared state:
Line 535: private readonly Store _store;
Line 536: private readonly Customer _sut;
Line 537: 3.3.2
Line 538: The use of constructors in tests diminishes test readability
Line 539: The other drawback to extracting the arrangement code into the constructor is
Line 540: diminished test readability. You no longer see the full picture just by looking at the
Line 541: test itself. You have to examine different places in the class to understand what the test
Line 542: method does.
Line 543:  Even if there’s not much arrangement logic—say, only instantiation of the fixtures—
Line 544: you are still better off moving it directly to the test method. Otherwise, you’ll wonder
Line 545: if it’s really just instantiation or something else being configured there, too. A self-con-
Line 546: tained test doesn’t leave you with such uncertainties. 
Line 547: 3.3.3
Line 548: A better way to reuse test fixtures
Line 549: The use of the constructor is not the best approach when it comes to reusing test fix-
Line 550: tures. The second way—the beneficial one—is to introduce private factory methods in
Line 551: the test class, as shown in the following listing.
Line 552: public class CustomerTests
Line 553: {
Line 554: [Fact]
Line 555: public void Purchase_succeeds_when_enough_inventory()
Line 556: {
Line 557: Listing 3.8
Line 558: Extracting the common initialization code into private factory methods
Line 559: 
Line 560: --- 페이지 75 ---
Line 561: 53
Line 562: Reusing test fixtures between tests
Line 563: Store store = CreateStoreWithInventory(Product.Shampoo, 10);
Line 564: Customer sut = CreateCustomer();
Line 565: bool success = sut.Purchase(store, Product.Shampoo, 5);
Line 566: Assert.True(success);
Line 567: Assert.Equal(5, store.GetInventory(Product.Shampoo));
Line 568: }
Line 569: [Fact]
Line 570: public void Purchase_fails_when_not_enough_inventory()
Line 571: {
Line 572: Store store = CreateStoreWithInventory(Product.Shampoo, 10);
Line 573: Customer sut = CreateCustomer();
Line 574: bool success = sut.Purchase(store, Product.Shampoo, 15);
Line 575: Assert.False(success);
Line 576: Assert.Equal(10, store.GetInventory(Product.Shampoo));
Line 577: }
Line 578: private Store CreateStoreWithInventory(
Line 579: Product product, int quantity)
Line 580: {
Line 581: Store store = new Store();
Line 582: store.AddInventory(product, quantity);
Line 583: return store;
Line 584: }
Line 585: private static Customer CreateCustomer()
Line 586: {
Line 587: return new Customer();
Line 588: }
Line 589: }
Line 590: By extracting the common initialization code into private factory methods, you can
Line 591: also shorten the test code, but at the same time keep the full context of what’s going
Line 592: on in the tests. Moreover, the private methods don’t couple tests to each other as long
Line 593: as you make them generic enough. That is, allow the tests to specify how they want the
Line 594: fixtures to be created.
Line 595:  Look at this line, for example:
Line 596: Store store = CreateStoreWithInventory(Product.Shampoo, 10);
Line 597: The test explicitly states that it wants the factory method to add 10 units of shampoo
Line 598: to the store. This is both highly readable and reusable. It’s readable because you don’t
Line 599: need to examine the internals of the factory method to understand the attributes of
Line 600: the created store. It’s reusable because you can use this method in other tests, too.
Line 601:  Note that in this particular example, there’s no need to introduce factory meth-
Line 602: ods, as the arrangement logic is quite simple. View it merely as a demonstration.
Line 603: 
Line 604: --- 페이지 76 ---
Line 605: 54
Line 606: CHAPTER 3
Line 607: The anatomy of a unit test
Line 608:  There’s one exception to this rule of reusing test fixtures. You can instantiate a fix-
Line 609: ture in the constructor if it’s used by all or almost all tests. This is often the case for
Line 610: integration tests that work with a database. All such tests require a database connec-
Line 611: tion, which you can initialize once and then reuse everywhere. But even then, it would
Line 612: make more sense to introduce a base class and initialize the database connection in
Line 613: that class’s constructor, not in individual test classes. See the following listing for an
Line 614: example of common initialization code in a base class.
Line 615: public class CustomerTests : IntegrationTests
Line 616: {
Line 617: [Fact]
Line 618: public void Purchase_succeeds_when_enough_inventory()
Line 619: {
Line 620: /* use _database here */
Line 621: }
Line 622: }
Line 623: public abstract class IntegrationTests : IDisposable
Line 624: {
Line 625: protected readonly Database _database;
Line 626: protected IntegrationTests()
Line 627: {
Line 628: _database = new Database();
Line 629: }
Line 630: public void Dispose()
Line 631: {
Line 632: _database.Dispose();
Line 633: }
Line 634: }
Line 635: Notice how CustomerTests remains constructor-less. It gets access to the _database
Line 636: instance by inheriting from the IntegrationTests base class. 
Line 637: 3.4
Line 638: Naming a unit test
Line 639: It’s important to give expressive names to your tests. Proper naming helps you under-
Line 640: stand what the test verifies and how the underlying system behaves.
Line 641:  So, how should you name a unit test? I’ve seen and tried a lot of naming conven-
Line 642: tions over the past decade. One of the most prominent, and probably least helpful, is
Line 643: the following convention:
Line 644: [MethodUnderTest]_[Scenario]_[ExpectedResult]
Line 645: where
Line 646: 
Line 647: MethodUnderTest is the name of the method you are testing.
Line 648: 
Line 649: Scenario is the condition under which you test the method.
Line 650: Listing 3.9
Line 651: Common initialization code in a base class
Line 652: 
Line 653: --- 페이지 77 ---
Line 654: 55
Line 655: Naming a unit test
Line 656: 
Line 657: ExpectedResult is what you expect the method under test to do in the current
Line 658: scenario.
Line 659: It’s unhelpful specifically because it encourages you to focus on implementation
Line 660: details instead of the behavior.
Line 661:  Simple phrases in plain English do a much better job: they are more expressive
Line 662: and don’t box you in a rigid naming structure. With simple phrases, you can describe
Line 663: the system behavior in a way that’s meaningful to a customer or a domain expert. To
Line 664: give you an example of a test titled in plain English, here’s the test from listing 3.5
Line 665: once again:
Line 666: public class CalculatorTests
Line 667: {
Line 668: [Fact]
Line 669: public void Sum_of_two_numbers()
Line 670: {
Line 671: double first = 10;
Line 672: double second = 20;
Line 673: var sut = new Calculator();
Line 674: double result = sut.Sum(first, second);
Line 675: Assert.Equal(30, result);
Line 676: }
Line 677: }
Line 678: How could the test’s name (Sum_of_two_numbers) be rewritten using the [MethodUnder-
Line 679: Test]_[Scenario]_[ExpectedResult] convention? Probably something like this:
Line 680: public void Sum_TwoNumbers_ReturnsSum()
Line 681: The method under test is Sum, the scenario includes two numbers, and the expected
Line 682: result is a sum of those two numbers. The new name looks logical to a programmer’s
Line 683: eye, but does it really help with test readability? Not at all. It’s Greek to an unin-
Line 684: formed person. Think about it: Why does Sum appear twice in the name of the test?
Line 685: And what is this Returns phrasing all about? Where is the sum returned to? You
Line 686: can’t know.
Line 687:  Some might argue that it doesn’t really matter what a non-programmer would
Line 688: think of this name. After all, unit tests are written by programmers for programmers,
Line 689: not domain experts. And programmers are good at deciphering cryptic names—it’s
Line 690: their job!
Line 691:  This is true, but only to a degree. Cryptic names impose a cognitive tax on every-
Line 692: one, programmers or not. They require additional brain capacity to figure out what
Line 693: exactly the test verifies and how it relates to business requirements. This may not seem
Line 694: like much, but the mental burden adds up over time. It slowly but surely increases the
Line 695: maintenance cost for the entire test suite. It’s especially noticeable if you return to the
Line 696: test after you’ve forgotten about the feature’s specifics, or try to understand a test
Line 697: 
Line 698: --- 페이지 78 ---
Line 699: 56
Line 700: CHAPTER 3
Line 701: The anatomy of a unit test
Line 702: written by a colleague. Reading someone else’s code is already difficult enough—any
Line 703: help understanding it is of considerable use.
Line 704:  Here are the two versions again:
Line 705: public void Sum_of_two_numbers()
Line 706: public void Sum_TwoNumbers_ReturnsSum()
Line 707: The initial name written in plain English is much simpler to read. It is a down-to-earth
Line 708: description of the behavior under test.
Line 709: 3.4.1
Line 710: Unit test naming guidelines
Line 711: Adhere to the following guidelines to write expressive, easily readable test names:
Line 712: Don’t follow a rigid naming policy. You simply can’t fit a high-level description of a
Line 713: complex behavior into the narrow box of such a policy. Allow freedom of
Line 714: expression.
Line 715: Name the test as if you were describing the scenario to a non-programmer who is familiar
Line 716: with the problem domain. A domain expert or a business analyst is a good example.
Line 717: Separate words with underscores. Doing so helps improve readability, especially in
Line 718: long names.
Line 719: Notice that I didn’t use underscores when naming the test class, CalculatorTests.
Line 720: Normally, the names of classes are not as long, so they read fine without underscores.
Line 721:  Also notice that although I use the pattern [ClassName]Tests when naming test
Line 722: classes, it doesn’t mean the tests are limited to verifying only that class. Remember, the
Line 723: unit in unit testing is a unit of behavior, not a class. This unit can span across one or sev-
Line 724: eral classes; the actual size is irrelevant. Still, you have to start somewhere. View the
Line 725: class in [ClassName]Tests as just that: an entry point, an API, using which you can
Line 726: verify a unit of behavior. 
Line 727: 3.4.2
Line 728: Example: Renaming a test toward the guidelines
Line 729: Let’s take a test as an example and try to gradually improve its name using the guide-
Line 730: lines I just outlined. In the following listing, you can see a test verifying that a delivery
Line 731: with a past date is invalid. The test’s name is written using the rigid naming policy that
Line 732: doesn’t help with the test readability.
Line 733: [Fact]
Line 734: public void IsDeliveryValid_InvalidDate_ReturnsFalse()
Line 735: {
Line 736: DeliveryService sut = new DeliveryService();
Line 737: DateTime pastDate = DateTime.Now.AddDays(-1);
Line 738: Delivery delivery = new Delivery
Line 739: {
Line 740: Date = pastDate
Line 741: };
Line 742: Listing 3.10
Line 743: A test named using the rigid naming policy
Line 744: 
Line 745: --- 페이지 79 ---
Line 746: 57
Line 747: Naming a unit test
Line 748: bool isValid = sut.IsDeliveryValid(delivery);
Line 749: Assert.False(isValid);
Line 750: }
Line 751: This test checks that DeliveryService properly identifies a delivery with an incorrect
Line 752: date as invalid. How would you rewrite the test’s name in plain English? The following
Line 753: would be a good first try:
Line 754: public void Delivery_with_invalid_date_should_be_considered_invalid()
Line 755: Notice two things in the new version:
Line 756: The name now makes sense to a non-programmer, which means programmers
Line 757: will have an easier time understanding it, too.
Line 758: The name of the SUT’s method—IsDeliveryValid—is no longer part of the
Line 759: test’s name.
Line 760: The second point is a natural consequence of rewriting the test’s name in plain
Line 761: English and thus can be easily overlooked. However, this consequence is important
Line 762: and can be elevated into a guideline of its own.
Line 763: But let’s get back to the example. The new version of the test’s name is a good start,
Line 764: but it can be improved further. What does it mean for a delivery date to be invalid,
Line 765: exactly? From the test in listing 3.10, we can see that an invalid date is any date in
Line 766: the past. This makes sense—you should only be allowed to choose a delivery date
Line 767: in the future.
Line 768:  So let’s be specific and reflect this knowledge in the test’s name:
Line 769: public void Delivery_with_past_date_should_be_considered_invalid()
Line 770: Method under test in the test’s name
Line 771: Don’t include the name of the SUT’s method in the test’s name.
Line 772: Remember, you don’t test code, you test application behavior. Therefore, it doesn’t
Line 773: matter what the name of the method under test is. As I mentioned previously, the
Line 774: SUT is just an entry point: a means to invoke a behavior. You can decide to rename
Line 775: the method under test to, say, IsDeliveryCorrect, and it will have no effect on the
Line 776: SUT’s behavior. On the other hand, if you follow the original naming convention, you’ll
Line 777: have to rename the test. This once again shows that targeting code instead of behav-
Line 778: ior couples tests to that code’s implementation details, which negatively affects the
Line 779: test suite’s maintainability. More on this issue in chapter 5.
Line 780: The only exception to this guideline is when you work on utility code. Such code
Line 781: doesn’t contain business logic—its behavior doesn’t go much beyond simple auxil-
Line 782: iary functionality and thus doesn’t mean anything to business people. It’s fine to use
Line 783: the SUT’s method names there.
Line 784: 
Line 785: --- 페이지 80 ---
Line 786: 58
Line 787: CHAPTER 3
Line 788: The anatomy of a unit test
Line 789: This is better but still not ideal. It’s too verbose. We can get rid of the word consid-
Line 790: ered without any loss of meaning:
Line 791: public void Delivery_with_past_date_should_be_invalid()
Line 792: The wording should be is another common anti-pattern. Earlier in this chapter, I men-
Line 793: tioned that a test is a single, atomic fact about a unit of behavior. There’s no place for
Line 794: a wish or a desire when stating a fact. Name the test accordingly—replace should be
Line 795: with is:
Line 796: public void Delivery_with_past_date_is_invalid()
Line 797: And finally, there’s no need to avoid basic English grammar. Articles help the test read
Line 798: flawlessly. Add the article a to the test’s name:
Line 799: public void Delivery_with_a_past_date_is_invalid()
Line 800: There you go. This final version is a straight-to-the-point statement of a fact, which
Line 801: itself describes one of the aspects of the application behavior under test: in this partic-
Line 802: ular case, the aspect of determining whether a delivery can be done. 
Line 803: 3.5
Line 804: Refactoring to parameterized tests
Line 805: One test usually is not enough to fully describe a unit of behavior. Such a unit normally
Line 806: consists of multiple components, each of which should be captured with its own test. If
Line 807: the behavior is complex enough, the number of tests describing it can grow dramatically
Line 808: and may become unmanageable. Luckily, most unit testing frameworks provide func-
Line 809: tionality that allows you to group similar tests using parameterized tests (see figure 3.2).
Line 810: Behavior N
Line 811: …
Line 812: …
Line 813: …
Line 814: …
Line 815: Behavior 2
Line 816: Behavior 1
Line 817: Can be grouped
Line 818: Fact N
Line 819: Fact 2
Line 820: Fact 1
Line 821: Application
Line 822: Figure 3.2
Line 823: A typical application 
Line 824: exhibits multiple behaviors. The 
Line 825: greater the complexity of the 
Line 826: behavior, the more facts are required 
Line 827: to fully describe it. Each fact is 
Line 828: represented by a test. Similar facts 
Line 829: can be grouped into a single test 
Line 830: method using parameterized tests.
Line 831: 
Line 832: --- 페이지 81 ---
Line 833: 59
Line 834: Refactoring to parameterized tests
Line 835: In this section, I’ll first show each such behavior component described by a separate test
Line 836: and then demonstrate how these tests can be grouped together.
Line 837:  Let’s say that our delivery functionality works in such a way that the soonest
Line 838: allowed delivery date is two days from now. Clearly, the one test we have isn’t enough.
Line 839: In addition to the test that checks for a past delivery date, we’ll also need tests that
Line 840: check for today’s date, tomorrow’s date, and the date after that.
Line 841:  The existing test is called Delivery_with_a_past_date_is_invalid. We could
Line 842: add three more:
Line 843: public void Delivery_for_today_is_invalid()
Line 844: public void Delivery_for_tomorrow_is_invalid()
Line 845: public void The_soonest_delivery_date_is_two_days_from_now()
Line 846: But that would result in four test methods, with the only difference between them
Line 847: being the delivery date.
Line 848:  A better approach is to group these tests into one in order to reduce the amount of
Line 849: test code. xUnit (like most other test frameworks) has a feature called parameterized
Line 850: tests that allows you to do exactly that. The next listing shows how such grouping looks.
Line 851: Each InlineData attribute represents a separate fact about the system; it’s a test case
Line 852: in its own right.
Line 853: public class DeliveryServiceTests
Line 854: {
Line 855: [InlineData(-1, false)]   
Line 856: [InlineData(0, false)]   
Line 857: [InlineData(1, false)]   
Line 858: [InlineData(2, true)]
Line 859:   
Line 860: [Theory]
Line 861: public void Can_detect_an_invalid_delivery_date(
Line 862: int daysFromNow,       
Line 863: bool expected)
Line 864:       
Line 865: {
Line 866: DeliveryService sut = new DeliveryService();
Line 867: DateTime deliveryDate = DateTime.Now
Line 868: .AddDays(daysFromNow);                   
Line 869: Delivery delivery = new Delivery
Line 870: {
Line 871: Date = deliveryDate
Line 872: };
Line 873: bool isValid = sut.IsDeliveryValid(delivery);
Line 874: Assert.Equal(expected, isValid);              
Line 875: }
Line 876: }
Line 877: TIP
Line 878: Notice the use of the [Theory] attribute instead of [Fact]. A theory is a
Line 879: bunch of facts about the behavior.
Line 880: Listing 3.11
Line 881: A test that encompasses several facts
Line 882: The InlineData attribute sends a 
Line 883: set of input values to the test 
Line 884: method. Each line represents a 
Line 885: separate fact about the behavior.
Line 886: Parameters to which the attributes 
Line 887: attach the input values
Line 888: Uses the 
Line 889: parameters
Line 890: 
Line 891: --- 페이지 82 ---
Line 892: 60
Line 893: CHAPTER 3
Line 894: The anatomy of a unit test
Line 895: Each fact is now represented by an [InlineData] line rather than a separate test. I
Line 896: also renamed the test method something more generic: it no longer mentions what
Line 897: constitutes a valid or invalid date.
Line 898:  Using parameterized tests, you can significantly reduce the amount of test code,
Line 899: but this benefit comes at a cost. It’s now hard to figure out what facts the test method
Line 900: represents. And the more parameters there are, the harder it becomes. As a compro-
Line 901: mise, you can extract the positive test case into its own test and benefit from the
Line 902: descriptive naming where it matters the most—in determining what differentiates
Line 903: valid and invalid delivery dates, as shown in the following listing.
Line 904: public class DeliveryServiceTests
Line 905: {
Line 906: [InlineData(-1)]
Line 907: [InlineData(0)]
Line 908: [InlineData(1)]
Line 909: [Theory]
Line 910: public void Detects_an_invalid_delivery_date(int daysFromNow)
Line 911: {
Line 912: /* ... */
Line 913: }
Line 914: [Fact]
Line 915: public void The_soonest_delivery_date_is_two_days_from_now()
Line 916: {
Line 917: /* ... */
Line 918: }
Line 919: }
Line 920: This approach also simplifies the negative test cases, since you can remove the
Line 921: expected Boolean parameter from the test method. And, of course, you can trans-
Line 922: form the positive test method into a parameterized test as well, to test multiple dates.
Line 923:  As you can see, there’s a trade-off between the amount of test code and the read-
Line 924: ability of that code. As a rule of thumb, keep both positive and negative test cases
Line 925: together in a single method only when it’s self-evident from the input parameters
Line 926: which case stands for what. Otherwise, extract the positive test cases. And if the behav-
Line 927: ior is too complicated, don’t use the parameterized tests at all. Represent each nega-
Line 928: tive and positive test case with its own test method.
Line 929: 3.5.1
Line 930: Generating data for parameterized tests
Line 931: There are some caveats in using parameterized tests (at least, in .NET) that you need
Line 932: to be aware of. Notice that in listing 3.11, I used the daysFromNow parameter as an
Line 933: input to the test method. Why not the actual date and time, you might ask? Unfortu-
Line 934: nately, the following code won’t work:
Line 935: [InlineData(DateTime.Now.AddDays(-1), false)]
Line 936: [InlineData(DateTime.Now, false)]
Line 937: Listing 3.12
Line 938: Two tests verifying the positive and negative scenarios
Line 939: 
Line 940: --- 페이지 83 ---
Line 941: 61
Line 942: Refactoring to parameterized tests
Line 943: [InlineData(DateTime.Now.AddDays(1), false)]
Line 944: [InlineData(DateTime.Now.AddDays(2), true)]
Line 945: [Theory]
Line 946: public void Can_detect_an_invalid_delivery_date(
Line 947: DateTime deliveryDate,
Line 948: bool expected)
Line 949: {
Line 950: DeliveryService sut = new DeliveryService();
Line 951: Delivery delivery = new Delivery
Line 952: {
Line 953: Date = deliveryDate
Line 954: };
Line 955: bool isValid = sut.IsDeliveryValid(delivery);
Line 956: Assert.Equal(expected, isValid);
Line 957: }
Line 958: In C#, the content of all attributes is evaluated at compile time. You have to use only
Line 959: those values that the compiler can understand, which are as follows:
Line 960: Constants
Line 961: Literals
Line 962: 
Line 963: typeof() expressions
Line 964: The call to DateTime.Now relies on the .NET runtime and thus is not allowed.
Line 965:  There is a way to overcome this problem. xUnit has another feature that you can
Line 966: use to generate custom data to feed into the test method: [MemberData]. The next list-
Line 967: ing shows how we can rewrite the previous test using this feature.
Line 968: [Theory]
Line 969: [MemberData(nameof(Data))]
Line 970: public void Can_detect_an_invalid_delivery_date(
Line 971: DateTime deliveryDate,
Line 972: bool expected)
Line 973: {
Line 974: /* ... */
Line 975: }
Line 976: public static List<object[]> Data()
Line 977: {
Line 978: return new List<object[]>
Line 979: {
Line 980: new object[] { DateTime.Now.AddDays(-1), false },
Line 981: new object[] { DateTime.Now, false },
Line 982: new object[] { DateTime.Now.AddDays(1), false },
Line 983: new object[] { DateTime.Now.AddDays(2), true }
Line 984: };
Line 985: }
Line 986: Listing 3.13
Line 987: Generating complex data for the parameterized test 
Line 988: 
Line 989: --- 페이지 84 ---
Line 990: 62
Line 991: CHAPTER 3
Line 992: The anatomy of a unit test
Line 993: MemberData accepts the name of a static method that generates a collection of input
Line 994: data (the compiler translates nameof(Data) into a "Data" literal). Each element of
Line 995: the collection is itself a collection that is mapped into the two input parameters:
Line 996: deliveryDate and expected. With this feature, you can overcome the compiler’s
Line 997: restrictions and use parameters of any type in the parameterized tests. 
Line 998: 3.6
Line 999: Using an assertion library to further improve 
Line 1000: test readability
Line 1001: One more thing you can do to improve test readability is to use an assertion library. I
Line 1002: personally prefer Fluent Assertions (https://fluentassertions.com), but .NET has sev-
Line 1003: eral competing libraries in this area.
Line 1004:  The main benefit of using an assertion library is how you can restructure the asser-
Line 1005: tions so that they are more readable. Here’s one of our earlier tests:
Line 1006: [Fact]
Line 1007: public void Sum_of_two_numbers()
Line 1008: {
Line 1009: var sut = new Calculator();
Line 1010: double result = sut.Sum(10, 20);
Line 1011: Assert.Equal(30, result);
Line 1012: }
Line 1013: Now compare it to the following, which uses a fluent assertion:
Line 1014: [Fact]
Line 1015: public void Sum_of_two_numbers()
Line 1016: {
Line 1017: var sut = new Calculator();
Line 1018: double result = sut.Sum(10, 20);
Line 1019: result.Should().Be(30);
Line 1020: }
Line 1021: The assertion from the second test reads as plain English, which is exactly how you
Line 1022: want all your code to read. We as humans prefer to absorb information in the form of
Line 1023: stories. All stories adhere to this specific pattern:
Line 1024: [Subject] [action] [object].
Line 1025: For example,
Line 1026: Bob opened the door.
Line 1027: Here, Bob is a subject, opened is an action, and the door is an object. The same rule
Line 1028: applies to code. result.Should().Be(30) reads better than Assert.Equal(30,
Line 1029: 
Line 1030: --- 페이지 85 ---
Line 1031: 63
Line 1032: Summary
Line 1033: result) precisely because it follows the story pattern. It’s a simple story in which
Line 1034: result is a subject, should be is an action, and 30 is an object.
Line 1035: NOTE
Line 1036: The paradigm of object-oriented programming (OOP) has become a
Line 1037: success partly because of this readability benefit. With OOP, you, too, can
Line 1038: structure the code in a way that reads like a story.
Line 1039: The Fluent Assertions library also provides numerous helper methods to assert against
Line 1040: numbers, strings, collections, dates and times, and much more. The only drawback is
Line 1041: that such a library is an additional dependency you may not want to introduce to your
Line 1042: project (although it’s for development only and won’t be shipped to production). 
Line 1043: Summary
Line 1044: All unit tests should follow the AAA pattern: arrange, act, assert. If a test has mul-
Line 1045: tiple arrange, act, or assert sections, that’s a sign that the test verifies multiple
Line 1046: units of behavior at once. If this test is meant to be a unit test, split it into several
Line 1047: tests—one per each action.
Line 1048: More than one line in the act section is a sign of a problem with the SUT’s API.
Line 1049: It requires the client to remember to always perform these actions together,
Line 1050: which can potentially lead to inconsistencies. Such inconsistencies are called
Line 1051: invariant violations. The act of protecting your code against potential invariant
Line 1052: violations is called encapsulation.
Line 1053: Distinguish the SUT in tests by naming it sut. Differentiate the three test sec-
Line 1054: tions either by putting Arrange, Act, and Assert comments before them or by
Line 1055: introducing empty lines between these sections.
Line 1056: Reuse test fixture initialization code by introducing factory methods, not by
Line 1057: putting this initialization code to the constructor. Such reuse helps maintain a
Line 1058: high degree of decoupling between tests and also provides better readability.
Line 1059: Don’t use a rigid test naming policy. Name each test as if you were describing
Line 1060: the scenario in it to a non-programmer who is familiar with the problem
Line 1061: domain. Separate words in the test name by underscores, and don’t include the
Line 1062: name of the method under test in the test name.
Line 1063: Parameterized tests help reduce the amount of code needed for similar tests.
Line 1064: The drawback is that the test names become less readable as you make them
Line 1065: more generic.
Line 1066: Assertion libraries help you further improve test readability by restructuring the
Line 1067: word order in assertions so that they read like plain English. 
Line 1068: 
Line 1069: --- 페이지 86 ---