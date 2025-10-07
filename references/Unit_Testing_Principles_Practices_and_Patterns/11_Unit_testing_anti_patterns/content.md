Line 1: 
Line 2: --- 페이지 281 ---
Line 3: 259
Line 4: Unit testing anti-patterns
Line 5: This chapter is an aggregation of lesser related topics (mostly anti-patterns) that
Line 6: didn’t fit in earlier in the book and are better served on their own. An anti-pattern is
Line 7: a common solution to a recurring problem that looks appropriate on the surface
Line 8: but leads to problems further down the road.
Line 9:  You will learn how to work with time in tests, how to identify and avoid such anti-
Line 10: patterns as unit testing of private methods, code pollution, mocking concrete
Line 11: classes, and more. Most of these topics follow from the first principles described in
Line 12: part 2. Still, they are well worth spelling out explicitly. You’ve probably heard of at
Line 13: least some of these anti-patterns in the past, but this chapter will help you connect
Line 14: the dots, so to speak, and see the foundations they are based on.
Line 15: This chapter covers
Line 16: Unit testing private methods
Line 17: Exposing private state to enable unit testing
Line 18: Leaking domain knowledge to tests
Line 19: Mocking concrete classes
Line 20: 
Line 21: --- 페이지 282 ---
Line 22: 260
Line 23: CHAPTER 11
Line 24: Unit testing anti-patterns
Line 25: 11.1
Line 26: Unit testing private methods
Line 27: When it comes to unit testing, one of the most commonly asked questions is how to
Line 28: test a private method. The short answer is that you shouldn’t do so at all, but there’s
Line 29: quite a bit of nuance to this topic.
Line 30: 11.1.1 Private methods and test fragility
Line 31: Exposing methods that you would otherwise keep private just to enable unit testing
Line 32: violates one of the foundational principles we discussed in chapter 5: testing observ-
Line 33: able behavior only. Exposing private methods leads to coupling tests to implementa-
Line 34: tion details and, ultimately, damaging your tests’ resistance to refactoring—the most
Line 35: important metric of the four. (All four metrics, once again, are protection against
Line 36: regressions, resistance to refactoring, fast feedback, and maintainability.) Instead of
Line 37: testing private methods directly, test them indirectly, as part of the overarching observ-
Line 38: able behavior. 
Line 39: 11.1.2 Private methods and insufficient coverage
Line 40: Sometimes, the private method is too complex, and testing it as part of the observable
Line 41: behavior doesn’t provide sufficient coverage. Assuming the observable behavior
Line 42: already has reasonable test coverage, there can be two issues at play:
Line 43: This is dead code. If the uncovered code isn’t being used, this is likely some extra-
Line 44: neous code left after a refactoring. It’s best to delete this code.
Line 45: There’s a missing abstraction. If the private method is too complex (and thus is
Line 46: hard to test via the class’s public API), it’s an indication of a missing abstraction
Line 47: that should be extracted into a separate class.
Line 48: Let’s illustrate the second issue with an example.
Line 49: public class Order
Line 50: {
Line 51: private Customer _customer;
Line 52: private List<Product> _products;
Line 53: public string GenerateDescription()
Line 54: {
Line 55: return $"Customer name: {_customer.Name}, " +
Line 56: $"total number of products: {_products.Count}, " +
Line 57: $"total price: {GetPrice()}";             
Line 58: }
Line 59: private decimal GetPrice()     
Line 60: {
Line 61: decimal basePrice = /* Calculate based on _products */;
Line 62: decimal discounts = /* Calculate based on _customer */;
Line 63: decimal taxes = /* Calculate based on _products */;
Line 64: Listing 11.1
Line 65: A class with a complex private method
Line 66: The complex private
Line 67: method is used by a
Line 68: much simpler public
Line 69: method.
Line 70: Complex private 
Line 71: method
Line 72: 
Line 73: --- 페이지 283 ---
Line 74: 261
Line 75: Unit testing private methods
Line 76: return basePrice - discounts + taxes;
Line 77: }
Line 78: }
Line 79: The GenerateDescription() method is quite simple: it returns a generic description
Line 80: of the order. But it uses the private GetPrice() method, which is much more com-
Line 81: plex: it contains important business logic and needs to be thoroughly tested. That
Line 82: logic is a missing abstraction. Instead of exposing the GetPrice method, make this
Line 83: abstraction explicit by extracting it into a separate class, as shown in the next listing.
Line 84: public class Order
Line 85: {
Line 86: private Customer _customer;
Line 87: private List<Product> _products;
Line 88: public string GenerateDescription()
Line 89: {
Line 90: var calc = new PriceCalculator();
Line 91: return $"Customer name: {_customer.Name}, " +
Line 92: $"total number of products: {_products.Count}, " +
Line 93: $"total price: {calc.Calculate(_customer, _products)}";
Line 94: }
Line 95: }
Line 96: public class PriceCalculator
Line 97: {
Line 98: public decimal Calculate(Customer customer, List<Product> products)
Line 99: {
Line 100: decimal basePrice = /* Calculate based on products */;
Line 101: decimal discounts = /* Calculate based on customer */;
Line 102: decimal taxes = /* Calculate based on products */;
Line 103: return basePrice - discounts + taxes;
Line 104: }
Line 105: }
Line 106: Now you can test PriceCalculator independently of Order. You can also use the
Line 107: output-based (functional) style of unit testing, because PriceCalculator doesn’t
Line 108: have any hidden inputs or outputs. See chapter 6 for more information about styles
Line 109: of unit testing. 
Line 110: 11.1.3 When testing private methods is acceptable
Line 111: There are exceptions to the rule of never testing private methods. To understand
Line 112: those exceptions, we need to revisit the relationship between the code’s publicity and
Line 113: purpose from chapter 5. Table 11.1 sums up that relationship (you already saw this
Line 114: table in chapter 5; I’m copying it here for convenience).
Line 115: Listing 11.2
Line 116: Extracting the complex private method
Line 117: 
Line 118: --- 페이지 284 ---
Line 119: 262
Line 120: CHAPTER 11
Line 121: Unit testing anti-patterns
Line 122: As you might remember from chapter 5, making the observable behavior public and
Line 123: implementation details private results in a well-designed API. On the other hand,
Line 124: leaking implementation details damages the code’s encapsulation. The intersection of
Line 125: observable behavior and private methods is marked N/A in the table because for a
Line 126: method to become part of observable behavior, it has to be used by the client code,
Line 127: which is impossible if that method is private.
Line 128:  Note that testing private methods isn’t bad in and of itself. It’s only bad because
Line 129: those private methods are a proxy for implementation details. Testing implementa-
Line 130: tion details is what ultimately leads to test brittleness. Having that said, there are rare
Line 131: cases where a method is both private and part of observable behavior (and thus the
Line 132: N/A marking in table 11.1 isn’t entirely correct).
Line 133:  Let’s take a system that manages credit inquiries as an example. New inquiries are
Line 134: bulk-loaded directly into the database once a day. Administrators then review those
Line 135: inquiries one by one and decide whether to approve them. Here’s how the Inquiry
Line 136: class might look in that system.
Line 137: public class Inquiry
Line 138: {
Line 139: public bool IsApproved { get; private set; }
Line 140: public DateTime? TimeApproved { get; private set; }
Line 141: private Inquiry(
Line 142:   
Line 143: bool isApproved, DateTime? timeApproved)  
Line 144: {
Line 145: if (isApproved && !timeApproved.HasValue)
Line 146: throw new Exception();
Line 147: IsApproved = isApproved;
Line 148: TimeApproved = timeApproved;
Line 149: }
Line 150: public void Approve(DateTime now)
Line 151: {
Line 152: if (IsApproved)
Line 153: return;
Line 154: IsApproved = true;
Line 155: TimeApproved = now;
Line 156: }
Line 157: }
Line 158: Table 11.1
Line 159: The relationship between the code’s publicity and purpose
Line 160: Observable behavior
Line 161: Implementation detail
Line 162: Public
Line 163: Good
Line 164: Bad
Line 165: Private
Line 166: N/A
Line 167: Good
Line 168: Listing 11.3
Line 169: A class with a private constructor
Line 170: Private 
Line 171: constructor
Line 172: 
Line 173: --- 페이지 285 ---
Line 174: 263
Line 175: Exposing private state
Line 176: The private constructor is private because the class is restored from the database by an
Line 177: object-relational mapping (ORM) library. That ORM doesn’t need a public construc-
Line 178: tor; it may well work with a private one. At the same time, our system doesn’t need a
Line 179: constructor, either, because it’s not responsible for the creation of those inquiries.
Line 180:  How do you test the Inquiry class given that you can’t instantiate its objects? On
Line 181: the one hand, the approval logic is clearly important and thus should be unit tested.
Line 182: But on the other, making the constructor public would violate the rule of not expos-
Line 183: ing private methods.
Line 184:  Inquiry’s constructor is an example of a method that is both private and part of
Line 185: the observable behavior. This constructor fulfills the contract with the ORM, and the
Line 186: fact that it’s private doesn’t make that contract less important: the ORM wouldn’t be
Line 187: able to restore inquiries from the database without it.
Line 188:  And so, making Inquiry’s constructor public won’t lead to test brittleness in this par-
Line 189: ticular case. In fact, it will arguably bring the class’s API closer to being well-designed.
Line 190: Just make sure the constructor contains all the preconditions required to maintain its
Line 191: encapsulation. In listing 11.3, such a precondition is the requirement to have the
Line 192: approval time in all approved inquiries.
Line 193:  Alternatively, if you prefer to keep the class’s public API surface as small as possi-
Line 194: ble, you can instantiate Inquiry via reflection in tests. Although this looks like a hack,
Line 195: you are just following the ORM, which also uses reflection behind the scenes. 
Line 196: 11.2
Line 197: Exposing private state
Line 198: Another common anti-pattern is exposing private state for the sole purpose of unit
Line 199: testing. The guideline here is the same as with private methods: don’t expose state
Line 200: that you would otherwise keep private—test observable behavior only. Let’s take a
Line 201: look at the following listing.
Line 202: public class Customer
Line 203: {
Line 204: private CustomerStatus _status =   
Line 205: CustomerStatus.Regular;
Line 206:    
Line 207: public void Promote()
Line 208: {
Line 209: _status = CustomerStatus.Preferred;
Line 210: }
Line 211: public decimal GetDiscount()
Line 212: {
Line 213: return _status == CustomerStatus.Preferred ? 0.05m : 0m;
Line 214: }
Line 215: }
Line 216: public enum CustomerStatus
Line 217: {
Line 218: Listing 11.4
Line 219: A class with private state
Line 220: Private 
Line 221: state
Line 222: 
Line 223: --- 페이지 286 ---
Line 224: 264
Line 225: CHAPTER 11
Line 226: Unit testing anti-patterns
Line 227: Regular,
Line 228: Preferred
Line 229: }
Line 230: This example shows a Customer class. Each customer is created in the Regular status
Line 231: and then can be promoted to Preferred, at which point they get a 5% discount on
Line 232: everything.
Line 233:  How would you test the Promote() method? This method’s side effect is a change
Line 234: of the _status field, but the field itself is private and thus not available in tests. A
Line 235: tempting solution would be to make this field public. After all, isn’t the change of sta-
Line 236: tus the ultimate goal of calling Promote()?
Line 237:  That would be an anti-pattern, however. Remember, your tests should interact with the
Line 238: system under test (SUT) exactly the same way as the production code and shouldn’t have any spe-
Line 239: cial privileges. In listing 11.4, the _status field is hidden from the production code and
Line 240: thus is not part of the SUT’s observable behavior. Exposing that field would result in
Line 241: coupling tests to implementation details. How to test Promote(), then?
Line 242:  What you should do, instead, is look at how the production code uses this class. In
Line 243: this particular example, the production code doesn’t care about the customer’s status;
Line 244: otherwise, that field would be public. The only information the production code does
Line 245: care about is the discount the customer gets after the promotion. And so that’s what
Line 246: you need to verify in tests. You need to check that
Line 247: A newly created customer has no discount.
Line 248: Once the customer is promoted, the discount becomes 5%.
Line 249: Later, if the production code starts using the customer status field, you’d be able to
Line 250: couple to that field in tests too, because it would officially become part of the SUT’s
Line 251: observable behavior.
Line 252: NOTE
Line 253: Widening the public API surface for the sake of testability is a bad practice. 
Line 254: 11.3
Line 255: Leaking domain knowledge to tests
Line 256: Leaking domain knowledge to tests is another quite common anti-pattern. It usually
Line 257: takes place in tests that cover complex algorithms. Let’s take the following (admit-
Line 258: tedly, not that complex) calculation algorithm as an example:
Line 259: public static class Calculator
Line 260: {
Line 261: public static int Add(int value1, int value2)
Line 262: {
Line 263: return value1 + value2;
Line 264: }
Line 265: }
Line 266: This listing shows an incorrect way to test it.
Line 267: 
Line 268: --- 페이지 287 ---
Line 269: 265
Line 270: Leaking domain knowledge to tests
Line 271: public class CalculatorTests
Line 272: {
Line 273: [Fact]
Line 274: public void Adding_two_numbers()
Line 275: {
Line 276: int value1 = 1;
Line 277: int value2 = 3;
Line 278: int expected = value1 + value2;      
Line 279: int actual = Calculator.Add(value1, value2);
Line 280: Assert.Equal(expected, actual);
Line 281: }
Line 282: }
Line 283: You could also parameterize the test to throw in a couple more test cases at almost no
Line 284: additional cost.
Line 285: public class CalculatorTests
Line 286: {
Line 287: [Theory]
Line 288: [InlineData(1, 3)]
Line 289: [InlineData(11, 33)]
Line 290: [InlineData(100, 500)]
Line 291: public void Adding_two_numbers(int value1, int value2)
Line 292: {
Line 293: int expected = value1 + value2;    
Line 294: int actual = Calculator.Add(value1, value2);
Line 295: Assert.Equal(expected, actual);
Line 296: }
Line 297: }
Line 298: Listings 11.5 and 11.6 look fine at first, but they are, in fact, examples of the anti-pattern:
Line 299: these tests duplicate the algorithm implementation from the production code. Of
Line 300: course, it might not seem like a big deal. After all, it’s just one line. But that’s only
Line 301: because the example is rather simplified. I’ve seen tests that covered complex algo-
Line 302: rithms and did nothing but reimplement those algorithms in the arrange part. They
Line 303: were basically a copy-paste from the production code.
Line 304:  These tests are another example of coupling to implementation details. They score
Line 305: almost zero on the metric of resistance to refactoring and are worthless as a result.
Line 306: Such tests don’t have a chance of differentiating legitimate failures from false posi-
Line 307: tives. Should a change in the algorithm make those tests fail, the team would most
Line 308: likely just copy the new version of that algorithm to the test without even trying to
Line 309: Listing 11.5
Line 310: Leaking algorithm implementation
Line 311: Listing 11.6
Line 312: A parameterized version of the same test
Line 313: The leakage
Line 314: The leakage
Line 315: 
Line 316: --- 페이지 288 ---
Line 317: 266
Line 318: CHAPTER 11
Line 319: Unit testing anti-patterns
Line 320: identify the root cause (which is understandable, because the tests were a mere dupli-
Line 321: cation of the algorithm in the first place).
Line 322:  How to test the algorithm properly, then? Don’t imply any specific implementation when
Line 323: writing tests. Instead of duplicating the algorithm, hard-code its results into the test, as
Line 324: shown in the following listing.
Line 325: public class CalculatorTests
Line 326: {
Line 327: [Theory]
Line 328: [InlineData(1, 3, 4)]
Line 329: [InlineData(11, 33, 44)]
Line 330: [InlineData(100, 500, 600)]
Line 331: public void Adding_two_numbers(int value1, int value2, int expected)
Line 332: {
Line 333: int actual = Calculator.Add(value1, value2);
Line 334: Assert.Equal(expected, actual);
Line 335: }
Line 336: }
Line 337: It can seem counterintuitive at first, but hardcoding the expected result is a good
Line 338: practice when it comes to unit testing. The important part with the hardcoded values
Line 339: is to precalculate them using something other than the SUT, ideally with the help of a
Line 340: domain expert. Of course, that’s only if the algorithm is complex enough (we are all
Line 341: experts at summing up two numbers). Alternatively, if you refactor a legacy applica-
Line 342: tion, you can have the legacy code produce those results and then use them as expected
Line 343: values in tests. 
Line 344: 11.4
Line 345: Code pollution
Line 346: The next anti-pattern is code pollution.
Line 347: DEFINITION
Line 348: Code pollution is adding production code that’s only needed for
Line 349: testing.
Line 350: Code pollution often takes the form of various types of switches. Let’s take a logger as
Line 351: an example.
Line 352: public class Logger
Line 353: {
Line 354: private readonly bool _isTestEnvironment;
Line 355: public Logger(bool isTestEnvironment)    
Line 356: {
Line 357: _isTestEnvironment = isTestEnvironment;
Line 358: }
Line 359: Listing 11.7
Line 360: Test with no domain knowledge
Line 361: Listing 11.8
Line 362: Logger with a Boolean switch 
Line 363: The switch
Line 364: 
Line 365: --- 페이지 289 ---
Line 366: 267
Line 367: Code pollution
Line 368: public void Log(string text)
Line 369: {
Line 370: if (_isTestEnvironment)     
Line 371: return;
Line 372: /* Log the text */
Line 373: }
Line 374: }
Line 375: public class Controller
Line 376: {
Line 377: public void SomeMethod(Logger logger)
Line 378: {
Line 379: logger.Log("SomeMethod is called");
Line 380: }
Line 381: }
Line 382: In this example, Logger has a constructor parameter that indicates whether the class
Line 383: runs in production. If so, the logger records the message into the file; otherwise, it
Line 384: does nothing. With such a Boolean switch, you can disable the logger during test runs,
Line 385: as shown in the following listing.
Line 386: [Fact]
Line 387: public void Some_test()
Line 388: {
Line 389: var logger = new Logger(true);    
Line 390: var sut = new Controller();
Line 391: sut.SomeMethod(logger);
Line 392: /* assert */
Line 393: }
Line 394: The problem with code pollution is that it mixes up test and production code and
Line 395: thereby increases the maintenance costs of the latter. To avoid this anti-pattern, keep
Line 396: the test code out of the production code base.
Line 397:  In the example with Logger, introduce an ILogger interface and create two imple-
Line 398: mentations of it: a real one for production and a fake one for testing purposes. After
Line 399: that, re-target Controller to accept the interface instead of the concrete class, as
Line 400: shown in the following listing.
Line 401: public interface ILogger
Line 402: {
Line 403: void Log(string text);
Line 404: }
Line 405: Listing 11.9
Line 406: A test using the Boolean switch
Line 407: Listing 11.10
Line 408: A version without the switch
Line 409: The switch
Line 410: Sets the parameter to 
Line 411: true to indicate the 
Line 412: test environment
Line 413: 
Line 414: --- 페이지 290 ---
Line 415: 268
Line 416: CHAPTER 11
Line 417: Unit testing anti-patterns
Line 418: public class Logger : ILogger
Line 419:   
Line 420: {
Line 421:   
Line 422: public void Log(string text)  
Line 423: {
Line 424:   
Line 425: /* Log the text */
Line 426:   
Line 427: }
Line 428:   
Line 429: }
Line 430:   
Line 431: public class FakeLogger : ILogger   
Line 432: {
Line 433:    
Line 434: public void Log(string text)    
Line 435: {
Line 436:    
Line 437: /* Do nothing */
Line 438:    
Line 439: }
Line 440:    
Line 441: }
Line 442:    
Line 443: public class Controller
Line 444: {
Line 445: public void SomeMethod(ILogger logger)
Line 446: {
Line 447: logger.Log("SomeMethod is called");
Line 448: }
Line 449: }
Line 450: Such a separation helps keep the production logger simple because it no longer has
Line 451: to account for different environments. Note that ILogger itself is arguably a form of
Line 452: code pollution: it resides in the production code base but is only needed for testing.
Line 453: So how is the new implementation better?
Line 454:  The kind of pollution ILogger introduces is less damaging and easier to deal
Line 455: with. Unlike the initial Logger implementation, with the new version, you can’t acci-
Line 456: dentally invoke a code path that isn’t intended for production use. You can’t have
Line 457: bugs in interfaces, either, because they are just contracts with no code in them. In
Line 458: contrast to Boolean switches, interfaces don’t introduce additional surface area for
Line 459: potential bugs. 
Line 460: 11.5
Line 461: Mocking concrete classes
Line 462: So far, this book has shown mocking examples using interfaces, but there’s an alterna-
Line 463: tive approach: you can mock concrete classes instead and thus preserve part of the
Line 464: original classes’ functionality, which can be useful at times. This alternative has a sig-
Line 465: nificant drawback, though: it violates the Single Responsibility principle. The next list-
Line 466: ing illustrates this idea.
Line 467: public class StatisticsCalculator
Line 468: {
Line 469: public (double totalWeight, double totalCost) Calculate(
Line 470: int customerId)
Line 471: {
Line 472: List<DeliveryRecord> records = GetDeliveries(customerId);
Line 473: Listing 11.11
Line 474: A class that calculates statistics
Line 475: Belongs in the 
Line 476: production code
Line 477: Belongs in 
Line 478: the test code
Line 479: 
Line 480: --- 페이지 291 ---
Line 481: 269
Line 482: Mocking concrete classes
Line 483: double totalWeight = records.Sum(x => x.Weight);
Line 484: double totalCost = records.Sum(x => x.Cost);
Line 485: return (totalWeight, totalCost);
Line 486: }
Line 487: public List<DeliveryRecord> GetDeliveries(int customerId)
Line 488: {
Line 489: /* Call an out-of-process dependency
Line 490: to get the list of deliveries */
Line 491: }
Line 492: }
Line 493: StatisticsCalculator gathers and calculates customer statistics: the weight and cost
Line 494: of all deliveries sent to a particular customer. The class does the calculation based on
Line 495: the list of deliveries retrieved from an external service (the GetDeliveries method).
Line 496: Let’s also say there’s a controller that uses StatisticsCalculator, as shown in the fol-
Line 497: lowing listing.
Line 498: public class CustomerController
Line 499: {
Line 500: private readonly StatisticsCalculator _calculator;
Line 501: public CustomerController(StatisticsCalculator calculator)
Line 502: {
Line 503: _calculator = calculator;
Line 504: }
Line 505: public string GetStatistics(int customerId)
Line 506: {
Line 507: (double totalWeight, double totalCost) = _calculator
Line 508: .Calculate(customerId);
Line 509: return
Line 510: $"Total weight delivered: {totalWeight}. " +
Line 511: $"Total cost: {totalCost}";
Line 512: }
Line 513: }
Line 514: How would you test this controller? You can’t supply it with a real Statistics-
Line 515: Calculator instance, because that instance refers to an unmanaged out-of-process
Line 516: dependency. The unmanaged dependency has to be substituted with a stub. At the
Line 517: same time, you don’t want to replace StatisticsCalculator entirely, either. This
Line 518: class contains important calculation functionality, which needs to be left intact.
Line 519:  One way to overcome this dilemma is to mock the StatisticsCalculator class
Line 520: and override only the GetDeliveries() method, which can be done by making that
Line 521: method virtual, as shown in the following listing.
Line 522:  
Line 523: Listing 11.12
Line 524: A controller using StatisticsCalculator
Line 525: 
Line 526: --- 페이지 292 ---
Line 527: 270
Line 528: CHAPTER 11
Line 529: Unit testing anti-patterns
Line 530: [Fact]
Line 531: public void Customer_with_no_deliveries()
Line 532: {
Line 533: // Arrange
Line 534: var stub = new Mock<StatisticsCalculator> { CallBase = true };
Line 535: stub.Setup(x => x.GetDeliveries(1))         
Line 536: .Returns(new List<DeliveryRecord>());
Line 537: var sut = new CustomerController(stub.Object);
Line 538: // Act
Line 539: string result = sut.GetStatistics(1);
Line 540: // Assert
Line 541: Assert.Equal("Total weight delivered: 0. Total cost: 0", result);
Line 542: }
Line 543: The CallBase = true setting tells the mock to preserve the base class’s behavior unless
Line 544: it’s explicitly overridden. With this approach, you can substitute only a part of the class
Line 545: while keeping the rest as-is. As I mentioned earlier, this is an anti-pattern.
Line 546: NOTE
Line 547: The necessity to mock a concrete class in order to preserve part of its
Line 548: functionality is a result of violating the Single Responsibility principle.
Line 549: StatisticsCalculator combines two unrelated responsibilities: communicating with
Line 550: the unmanaged dependency and calculating statistics. Look at listing 11.11 again. The
Line 551: Calculate() method is where the domain logic lies. GetDeliveries() just gathers
Line 552: the inputs for that logic. Instead of mocking StatisticsCalculator, split this class in
Line 553: two, as the following listing shows.
Line 554: public class DeliveryGateway : IDeliveryGateway
Line 555: {
Line 556: public List<DeliveryRecord> GetDeliveries(int customerId)
Line 557: {
Line 558: /* Call an out-of-process dependency
Line 559: to get the list of deliveries */
Line 560: }
Line 561: }
Line 562: public class StatisticsCalculator
Line 563: {
Line 564: public (double totalWeight, double totalCost) Calculate(
Line 565: List<DeliveryRecord> records)
Line 566: {
Line 567: double totalWeight = records.Sum(x => x.Weight);
Line 568: double totalCost = records.Sum(x => x.Cost);
Line 569: return (totalWeight, totalCost);
Line 570: }
Line 571: }
Line 572: Listing 11.13
Line 573: Test that mocks the concrete class
Line 574: Listing 11.14
Line 575: Splitting StatisticsCalculator into two classes
Line 576: GetDeliveries() must 
Line 577: be made virtual.
Line 578: 
Line 579: --- 페이지 293 ---
Line 580: 271
Line 581: Working with time
Line 582: The next listing shows the controller after the refactoring.
Line 583: public class CustomerController
Line 584: {
Line 585: private readonly StatisticsCalculator _calculator;
Line 586: private readonly IDeliveryGateway _gateway;
Line 587: public CustomerController(
Line 588: StatisticsCalculator calculator,   
Line 589: IDeliveryGateway gateway)
Line 590:    
Line 591: {
Line 592: _calculator = calculator;
Line 593: _gateway = gateway;
Line 594: }
Line 595: public string GetStatistics(int customerId)
Line 596: {
Line 597: var records = _gateway.GetDeliveries(customerId);
Line 598: (double totalWeight, double totalCost) = _calculator
Line 599: .Calculate(records);
Line 600: return
Line 601: $"Total weight delivered: {totalWeight}. " +
Line 602: $"Total cost: {totalCost}";
Line 603: }
Line 604: }
Line 605: The responsibility of communicating with the unmanaged dependency has transi-
Line 606: tioned to DeliveryGateway. Notice how this gateway is backed by an interface, which
Line 607: you can now use for mocking instead of the concrete class. The code in listing 11.15 is
Line 608: an example of the Humble Object design pattern in action. Refer to chapter 7 to
Line 609: learn more about this pattern. 
Line 610: 11.6
Line 611: Working with time
Line 612: Many application features require access to the current date and time. Testing func-
Line 613: tionality that depends on time can result in false positives, though: the time during
Line 614: the act phase might not be the same as in the assert. There are three options for stabi-
Line 615: lizing this dependency. One of these options is an anti-pattern; and of the other two,
Line 616: one is preferable to the other.
Line 617: 11.6.1 Time as an ambient context
Line 618: The first option is to use the ambient context pattern. You already saw this pattern in
Line 619: chapter 8 in the section about testing loggers. In the context of time, the ambient con-
Line 620: text would be a custom class that you’d use in code instead of the framework’s built-in
Line 621: DateTime.Now, as shown in the next listing.
Line 622:  
Line 623: Listing 11.15
Line 624: Controller after the refactoring
Line 625: Two separate 
Line 626: dependencies
Line 627: 
Line 628: --- 페이지 294 ---
Line 629: 272
Line 630: CHAPTER 11
Line 631: Unit testing anti-patterns
Line 632: public static class DateTimeServer
Line 633: {
Line 634: private static Func<DateTime> _func;
Line 635: public static DateTime Now => _func();
Line 636: public static void Init(Func<DateTime> func)
Line 637: {
Line 638: _func = func;
Line 639: }
Line 640: }
Line 641: DateTimeServer.Init(() => DateTime.Now);     
Line 642: DateTimeServer.Init(() => new DateTime(2020, 1, 1));      
Line 643: Just as with the logger functionality, using an ambient context for time is also an anti-
Line 644: pattern. The ambient context pollutes the production code and makes testing more
Line 645: difficult. Also, the static field introduces a dependency shared between tests, thus tran-
Line 646: sitioning those tests into the sphere of integration testing. 
Line 647: 11.6.2 Time as an explicit dependency
Line 648: A better approach is to inject the time dependency explicitly (instead of referring to it
Line 649: via a static method in an ambient context), either as a service or as a plain value, as
Line 650: shown in the following listing.
Line 651: public interface IDateTimeServer
Line 652: {
Line 653: DateTime Now { get; }
Line 654: }
Line 655: public class DateTimeServer : IDateTimeServer
Line 656: {
Line 657: public DateTime Now => DateTime.Now;
Line 658: }
Line 659: public class InquiryController
Line 660: {
Line 661: private readonly DateTimeServer _dateTimeServer;
Line 662: public InquiryController(
Line 663: DateTimeServer dateTimeServer)    
Line 664: {
Line 665: _dateTimeServer = dateTimeServer;
Line 666: }
Line 667: public void ApproveInquiry(int id)
Line 668: {
Line 669: Inquiry inquiry = GetById(id);
Line 670: Listing 11.16
Line 671: Current date and time as an ambient context
Line 672: Listing 11.17
Line 673: Current date and time as an explicit dependency
Line 674: Initialization code 
Line 675: for production
Line 676: Initialization code 
Line 677: for unit tests
Line 678: Injects time as 
Line 679: a service
Line 680: 
Line 681: --- 페이지 295 ---
Line 682: 273
Line 683: Summary
Line 684: inquiry.Approve(_dateTimeServer.Now);      
Line 685: SaveInquiry(inquiry);
Line 686: }
Line 687: }
Line 688: Of these two options, prefer injecting the time as a value rather than as a service. It’s
Line 689: easier to work with plain values in production code, and it’s also easier to stub those
Line 690: values in tests.
Line 691:  Most likely, you won’t be able to always inject the time as a plain value, because
Line 692: dependency injection frameworks don’t play well with value objects. A good compro-
Line 693: mise is to inject the time as a service at the start of a business operation and then
Line 694: pass it as a value in the remainder of that operation. You can see this approach in
Line 695: listing 11.17: the controller accepts DateTimeServer (the service) but then passes a
Line 696: DateTime value to the Inquiry domain class. 
Line 697: 11.7
Line 698: Conclusion
Line 699: In this chapter, we looked at some of the most prominent real-world unit testing use
Line 700: cases and analyzed them using the four attributes of a good test. I understand that it
Line 701: may be overwhelming to start applying all the ideas and guidelines from this book at
Line 702: once. Also, your situation might not be as clear-cut. I publish reviews of other people’s
Line 703: code and answer questions (related to unit testing and code design in general) on my
Line 704: blog at https://enterprisecraftsmanship.com. You can also submit your own question
Line 705: at https://enterprisecraftsmanship.com/about. You might also be interested in taking
Line 706: my online course, where I show how to build an application from the ground up,
Line 707: applying all the principles described in this book in practice, at https://unittesting-
Line 708: course.com.
Line 709:  You can always catch me on twitter at @vkhorikov, or contact me directly through
Line 710: https://enterprisecraftsmanship.com/about. I look forward to hearing from you!
Line 711: Summary
Line 712: Exposing private methods to enable unit testing leads to coupling tests to
Line 713: implementation and, ultimately, damaging the tests’ resistance to refactoring.
Line 714: Instead of testing private methods directly, test them indirectly as part of the
Line 715: overarching observable behavior.
Line 716: If the private method is too complex to be tested as part of the public API that
Line 717: uses it, that’s an indication of a missing abstraction. Extract this abstraction into
Line 718: a separate class instead of making the private method public.
Line 719: In rare cases, private methods do belong to the class’s observable behavior.
Line 720: Such methods usually implement a non-public contract between the class and
Line 721: an ORM or a factory.
Line 722: Don’t expose state that you would otherwise keep private for the sole purpose
Line 723: of unit testing. Your tests should interact with the system under test exactly the
Line 724: same way as the production code; they shouldn’t have any special privileges.
Line 725: Injects time as 
Line 726: a plain value
Line 727: 
Line 728: --- 페이지 296 ---
Line 729: 274
Line 730: CHAPTER 11
Line 731: Unit testing anti-patterns
Line 732: Don’t imply any specific implementation when writing tests. Verify the produc-
Line 733: tion code from a black-box perspective; avoid leaking domain knowledge to
Line 734: tests (see chapter 4 for more details about black-box and white-box testing).
Line 735: Code pollution is adding production code that’s only needed for testing. It’s an
Line 736: anti-pattern because it mixes up test and production code and increases the
Line 737: maintenance costs of the latter.
Line 738: The necessity to mock a concrete class in order to preserve part of its function-
Line 739: ality is a result of violating the Single Responsibility principle. Separate that
Line 740: class into two classes: one with the domain logic, and the other one communi-
Line 741: cating with the out-of-process dependency.
Line 742: Representing the current time as an ambient context pollutes the production
Line 743: code and makes testing more difficult. Inject time as an explicit dependency—
Line 744: either as a service or as a plain value. Prefer the plain value whenever possible.