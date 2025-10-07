Line 1: 
Line 2: --- 페이지 243 ---
Line 3: 215
Line 4: Writing larger tests
Line 5: Most of the code we tested in previous chapters could be tested via unit tests. When
Line 6: that was not possible because, say, the class depended on something else, we used
Line 7: stubs and mocks to replace the dependency, and we still wrote a unit test. As I said
Line 8: when we discussed the testing pyramid in chapter 1, I favor unit tests as much as
Line 9: possible when testing business rules.
Line 10:  But not everything in our systems can (or should) be tested via unit tests. Writ-
Line 11: ing unit tests for some pieces of code is a waste of time. Forcing yourself to write
Line 12: unit tests for them would result in test suites that are not good enough to find bugs,
Line 13: are hard to write, or are flaky and break when you make small changes in the code.
Line 14:  This chapter discusses how to identify which parts of the system should be tested
Line 15: with integration or system tests. Then I will illustrate how I write these tests for three
Line 16: common situations: (1) components (or sets of classes) that should be exercised
Line 17: together, because otherwise, the test suite would be too weak; (2) components that
Line 18: communicate with external infrastructure, such as classes that communicate with
Line 19: databases and are full of SQL queries; and (3) the entire system, end to end.
Line 20: This chapter covers
Line 21: Deciding when to write a larger test
Line 22: Engineering reliable integration and system tests
Line 23: 
Line 24: --- 페이지 244 ---
Line 25: 216
Line 26: CHAPTER 9
Line 27: Writing larger tests
Line 28: 9.1
Line 29: When to use larger tests
Line 30: I see two situations where you should use a larger test:
Line 31: You have exercised each class individually, but the overall behavior is composed
Line 32: of many classes, and you want to see them work together. Think of a set of
Line 33: classes that calculates the final cost of a shopping cart. You have unit-tested the
Line 34: class responsible for business rule 1 and the class responsible for business rule 2.
Line 35: But you still want to see the final cost of the shopping cart after all the rules
Line 36: have been applied to it.
Line 37: The class you want to test is a component in a larger plug-and-play architecture.
Line 38: One of the main advantages of object-oriented design is that we can encapsu-
Line 39: late and abstract repetitive complexity, so the user only has to implement what
Line 40: matters. Think of a plugin for your favorite IDE (in my case, IntelliJ). You can
Line 41: develop the logic of the plugin, but many actions will only happen when IntelliJ
Line 42: calls the plugin and passes parameters to it.
Line 43: The following sections show examples of both cases and will help you generalize
Line 44: them.
Line 45: 9.1.1
Line 46: Testing larger components
Line 47: As always, let’s use a concrete example. Suppose we have the following requirement:
Line 48: Given a shopping cart with items, quantities, and respective unit prices, the
Line 49: final price of the cart is calculated as follows:
Line 50: The final price of each item is calculated by multiplying its unit price by
Line 51: the quantity.
Line 52: The delivery costs are the following. For shopping carts with
Line 53: – 1 to 3 elements (inclusive), we charge 5 dollars extra.
Line 54: – 4 to 10 elements (inclusive), we charge 12.5 dollars extra.
Line 55: – More than 10 elements, we charge 20 dollars extra.
Line 56: If there is an electronic item in the cart, we charge 7.5 dollars extra.
Line 57: NOTE
Line 58: The business rule related to delivery costs is not realistic. As a devel-
Line 59: oper, when you notice such inconsistencies, you should talk to the stake-
Line 60: holder, product owner, or whomever is sponsoring that feature. I am keeping
Line 61: this business rule simple for the sake of the example.
Line 62: Before I begin coding, I think about how to approach the problem. I see how the
Line 63: final price is calculated and that a list of rules is applied to the shopping cart. My
Line 64: experience with software design and design for testability tells me that each rule
Line 65: should be in its own class—putting everything in a single class would result in a large
Line 66: class, which would require lots of tests. We prefer small classes that require only a
Line 67: handful of tests.
Line 68: 
Line 69: --- 페이지 245 ---
Line 70: 217
Line 71: When to use larger tests
Line 72:  Suppose the ShoppingCart and Item classes already exist in our code base. They are
Line 73: simple entities. ShoppingCart holds a list of Items. An Item is composed of a name, a
Line 74: quantity, a price per unit, and a type indicating whether this item is a piece of electronics.
Line 75:  Let’s define the contract that all the prices have in common. Listing 9.1 shows the
Line 76: PriceRule interface that all the price rules will follow. It receives a ShoppingCart and
Line 77: returns the value that should be aggregated to the final price of the shopping cart.
Line 78: Aggregating all the price rules will be the responsibility of another class, which we will
Line 79: code later.
Line 80: public interface PriceRule {
Line 81:     double priceToAggregate(ShoppingCart cart);
Line 82: }
Line 83: We begin with the DeliveryPrice price rule. It is straightforward, as its value depends
Line 84: solely on the number of items in the cart.
Line 85: public class DeliveryPrice implements PriceRule {
Line 86:   @Override
Line 87:   public double priceToAggregate(ShoppingCart cart) {
Line 88:     int totalItems = cart.numberOfItems();      
Line 89:     if(totalItems == 0)   
Line 90:       return 0;
Line 91:     if(totalItems >= 1 && totalItems <= 3)
Line 92:       return 5;
Line 93:     if(totalItems >= 4 && totalItems <= 10)
Line 94:       return 12.5;
Line 95:     return 20.0;
Line 96:   }
Line 97: }
Line 98: NOTE
Line 99: I am using double to represent prices for illustration purposes, but as
Line 100: discussed before, that would be a poor choice in real life. You may prefer to
Line 101: use BigDecimal or represent prices using integers or longs.
Line 102: With the implementation ready, let’s test it as we have learned: with unit testing. The
Line 103: class is so small and localized that it makes sense to exercise it via unit testing. We will
Line 104: apply specification-based and, more importantly, boundary testing (discussed in chap-
Line 105: ter 2). The requirements contain clear boundaries, and these boundaries are continu-
Line 106: ous (1 to 3 items, 4 to 10 items, more than 10 items). This means we can test each
Line 107: rule’s on and off points:
Line 108: 0 items
Line 109: 1 item
Line 110: Listing 9.1
Line 111: PriceRule interface
Line 112: Listing 9.2
Line 113: Implementation of DeliveryPrice
Line 114: Gets the number of items 
Line 115: in the cart. The delivery 
Line 116: price is based on this.
Line 117: These if statements based 
Line 118: on the requirements are 
Line 119: enough to return the 
Line 120: price.
Line 121: 
Line 122: --- 페이지 246 ---
Line 123: 218
Line 124: CHAPTER 9
Line 125: Writing larger tests
Line 126: 3 items
Line 127: 4 items
Line 128: 10 items
Line 129: More than 10 items (with 11 being the off point)
Line 130: NOTE
Line 131: Notice the “0 items” handler: the requirements do not mention that
Line 132: case. But I was thinking of the class’s pre-conditions and decided that if the
Line 133: cart has no items, the price should return 0. This corner case deserves a test.
Line 134: We use a parameterized test and comma-separated values (CSV) source to implement
Line 135: the JUnit test.
Line 136: public class DeliveryPriceTest {
Line 137:   @ParameterizedTest
Line 138:   @CsvSource({    
Line 139:     "0,0",
Line 140:     "1,5",
Line 141:     "3,5",
Line 142:     "4,12.5",
Line 143:     "10,12.5",
Line 144:     "11,20"})
Line 145:   void deliveryIsAccordingToTheNumberOfItems(int noOfItems,
Line 146:     ➥ double expectedDeliveryPrice) {
Line 147:     ShoppingCart cart = new ShoppingCart();   
Line 148:     for(int i = 0; i < noOfItems; i++) {
Line 149:       cart.add(new Item(ItemType.OTHER, "ANY", 1, 1));
Line 150:     }
Line 151:     double price = new DeliveryPrice().priceToAggregate(cart);  
Line 152:     assertThat(price).isEqualTo(expectedDeliveryPrice);  
Line 153:   }
Line 154: }
Line 155: Listing 9.3
Line 156: Tests for DeliveryPrice
Line 157: Refactoring to achieve 100% code coverage
Line 158: This example illustrates why you cannot blindly use code coverage. If you generate
Line 159: the report, you will see that the tool does not report 100% branch coverage! In fact,
Line 160: only three of the five conditions are fully exercised: totalItems >= 1 and total-
Line 161: Items >= 4 are not.
Line 162: Why? Let’s take the first case as an example. We have lots of tests where the num-
Line 163: ber of items is greater than 1, so the true branch of this condition is exercised. But
Line 164: how can we exercise the false branch? We would need a number of items less than
Line 165: 1. We have a test where the number of items is zero, but the test never reaches that
Line 166: Exercises the six boundaries. 
Line 167: The first value is the number 
Line 168: of items in the cart; the 
Line 169: second is the expected 
Line 170: delivery price.
Line 171: Creates a shopping cart and 
Line 172: adds the specified number 
Line 173: of items to it. The type, 
Line 174: name, quantity, and unit 
Line 175: price do not matter.
Line 176: Calls the
Line 177: DeliveryPrice
Line 178: rule …
Line 179: … and asserts 
Line 180: its output.
Line 181: 
Line 182: --- 페이지 247 ---
Line 183: 219
Line 184: When to use larger tests
Line 185: Next, we implement ExtraChargeForElectronics. The implementation is also
Line 186: straightforward, as all we need to do is check whether the cart contains any electron-
Line 187: ics. If so, we add the extra charge.
Line 188: public class ExtraChargeForElectronics implements PriceRule {
Line 189:   @Override
Line 190:   public double priceToAggregate(ShoppingCart cart) {
Line 191:     List<Item> items = cart.getItems();
Line 192:     boolean hasAnElectronicDevice = items
Line 193:       .stream()
Line 194:       .anyMatch(it -> it.getType() == ItemType.ELECTRONIC);   
Line 195:     if(hasAnElectronicDevice)   
Line 196:       return 7.50;
Line 197:     return 0;   
Line 198:   }
Line 199: }
Line 200: We have three cases to exercise: no electronics in the cart, one or more electronics in
Line 201: the cart, and an empty cart. Let’s implement them in three test methods. First, the fol-
Line 202: lowing test exercises the “one or more electronics” case. We can use parameterized
Line 203: tests to try this.
Line 204:  
Line 205:  
Line 206: condition because an early return happens in totalItems == 0. Pragmatically
Line 207: speaking, we have covered all the branches, but the tool cannot see it.
Line 208: One idea is to rewrite the code so this is not a problem. In the following code, the
Line 209: implementation is basically the same, but the sequence of if statements is written
Line 210: such that the tool can report 100% branch coverage:
Line 211: public double priceToAggregate(ShoppingCart cart) {
Line 212:   int totalItems = cart.numberOfItems();
Line 213:   if(totalItems == 0)
Line 214:     return 0;
Line 215:   if(totalItems <= 3)   
Line 216:     return 5;
Line 217:   if(totalItems <= 10)   
Line 218:     return 12.5;
Line 219:   return 20.0;
Line 220: }
Line 221: Listing 9.4
Line 222: ExtraChargeForElectronics implementation
Line 223: We do not need to check totalItems >= 1, 
Line 224: as that is the only thing that can happen if 
Line 225: we reach this if statement.
Line 226: Same here: no 
Line 227: need to check 
Line 228: totalItems >= 4
Line 229: Looks for any item
Line 230: whose type is equal to
Line 231: ELECTRONIC
Line 232: If there is at least one 
Line 233: such item, we return 
Line 234: the extra charge.
Line 235: Otherwise, we do not 
Line 236: add an extra charge.
Line 237: 
Line 238: --- 페이지 248 ---
Line 239: 220
Line 240: CHAPTER 9
Line 241: Writing larger tests
Line 242: public class ExtraChargeForElectronicsTest {
Line 243:   @ParameterizedTest
Line 244:   @CsvSource({"1", "2"})    
Line 245:   void chargeTheExtraPriceIfThereIsAnyElectronicInTheCart(
Line 246:     ➥ int numberOfElectronics) {
Line 247:     ShoppingCart cart = new ShoppingCart();
Line 248:     for(int i = 0; i < numberOfElectronics; i++) {      
Line 249:       cart.add(new Item(ItemType.ELECTRONIC, "ANY ELECTRONIC", 1, 1));
Line 250:     }
Line 251:     double price = new ExtraChargeForElectronics().priceToAggregate(cart);
Line 252:     assertThat(price).isEqualTo(7.50);  
Line 253:   }
Line 254: }
Line 255: We then test that no extra charges are added when there are no electronics in the cart
Line 256: (see listing 9.6).
Line 257: NOTE
Line 258: If you read chapter 5, you may wonder if we should write a property-
Line 259: based test in this case. The implementation is straightforward, and the num-
Line 260: ber of electronic items does not significantly affect how the algorithm works,
Line 261: so I am fine with example-based testing here.
Line 262: @Test
Line 263: void noExtraChargesIfNoElectronics() {
Line 264:   ShoppingCart cart = new ShoppingCart();  
Line 265:   cart.add(new Item(ItemType.OTHER, "BOOK", 1, 1));
Line 266:   cart.add(new Item(ItemType.OTHER, "CD", 1, 1));
Line 267:   cart.add(new Item(ItemType.OTHER, "BABY TOY", 1, 1));
Line 268:   double price = new ExtraChargeForElectronics().priceToAggregate(cart);
Line 269:   assertThat(price).isEqualTo(0);    
Line 270: }
Line 271: Finally, we test the case where there are no items in the shopping cart.
Line 272: @Test
Line 273: void noItems() {
Line 274:   ShoppingCart cart = new ShoppingCart();
Line 275: Listing 9.5
Line 276: Testing the extra charge for electronics
Line 277: Listing 9.6
Line 278: Testing for no extra charge for electronics
Line 279: Listing 9.7
Line 280: No items in the shopping cart, so no electronics charge
Line 281: The parameterized test will run a test with one electronic item in the cart and 
Line 282: another test with two electronic items in the cart. We want to ensure that having 
Line 283: multiple electronics in the cart does not incur incorrect extra charges.
Line 284: A simple loop that adds 
Line 285: the specified number of 
Line 286: electronics. We could 
Line 287: also have added a non-
Line 288: electronic item. Would 
Line 289: that make the test 
Line 290: stronger?
Line 291: Asserts that the extra 
Line 292: electronics price is charged
Line 293: Creates a cart with 
Line 294: random items, all 
Line 295: non-electronic
Line 296: Asserts that nothing 
Line 297: is charged
Line 298: 
Line 299: --- 페이지 249 ---
Line 300: 221
Line 301: When to use larger tests
Line 302:   double price = new ExtraChargeForElectronics().priceToAggregate(cart);
Line 303:   assertThat(price).isEqualTo(0);     
Line 304: }
Line 305: The final rule to implement is PriceOfItems, which navigates the list of items and cal-
Line 306: culates the unit price times the quantity of each item. I do not show the code and the
Line 307: test, to save space; they are available in the book’s code repository.
Line 308:  Let’s go to the class that aggregates all the price rules and calculates the final price.
Line 309: The FinalPriceCalculator class receives a list of PriceRules in its constructor. Its
Line 310: calculate method receives a ShoppingCart, passes it to all the price rules, and
Line 311: returns the aggregated price.
Line 312: public class FinalPriceCalculator {
Line 313:   private final List<PriceRule> rules;
Line 314:   public FinalPriceCalculator(List<PriceRule> rules) {  
Line 315:     this.rules = rules;
Line 316:   }
Line 317:   public double calculate(ShoppingCart cart) {
Line 318:     double finalPrice = 0;
Line 319:     for (PriceRule rule : rules) {   
Line 320:       finalPrice += rule.priceToAggregate(cart);
Line 321:     }
Line 322:     return finalPrice;     
Line 323:   }
Line 324: }
Line 325: We can easily unit-test this class: all we need to do is stub a set of PriceRules. Listing 9.9
Line 326: creates three price rule stubs. Each returns a different value, including 0, as 0 may
Line 327: happen. We then create a very simple shopping cart—its items do not matter, because
Line 328: we are mocking the price rules.
Line 329: public class FinalPriceCalculatorTest {
Line 330:   @Test
Line 331:   void callAllPriceRules() {
Line 332:     PriceRule rule1 = mock(PriceRule.class);      
Line 333:     PriceRule rule2 = mock(PriceRule.class);
Line 334:     PriceRule rule3 = mock(PriceRule.class);
Line 335:     ShoppingCart cart = new ShoppingCart();   
Line 336:     cart.add(new Item(ItemType.OTHER, "ITEM", 1, 1));
Line 337: Listing 9.8
Line 338: FinalPriceCalculator that runs all the PriceRules
Line 339: Listing 9.9
Line 340: Testing FinalPriceCalculator
Line 341: The shopping cart is empty, 
Line 342: so nothing is charged.
Line 343: Receives a list of 
Line 344: price rules in the 
Line 345: constructor. This 
Line 346: class is flexible and 
Line 347: can receive any 
Line 348: combination of 
Line 349: price rules.
Line 350: For each price rule, 
Line 351: gets the price to add 
Line 352: to the final price
Line 353: Returns the final 
Line 354: aggregated price
Line 355: Creates three 
Line 356: different stubs 
Line 357: of price rules
Line 358: Creates a 
Line 359: simple cart
Line 360: 
Line 361: --- 페이지 250 ---
Line 362: 222
Line 363: CHAPTER 9
Line 364: Writing larger tests
Line 365:     when(rule1.priceToAggregate(cart)).thenReturn(1.0);   
Line 366:     when(rule2.priceToAggregate(cart)).thenReturn(0.0);
Line 367:     when(rule3.priceToAggregate(cart)).thenReturn(2.0);
Line 368:     List<PriceRule> rules = Arrays.asList(rule1, rule2, rule3);   
Line 369:     FinalPriceCalculator calculator = new FinalPriceCalculator(rules);
Line 370:     double price = calculator.calculate(cart);
Line 371:     assertThat(price).isEqualTo(3);  
Line 372:   }
Line 373: }
Line 374: If this is what you envisioned when I posed the requirements, you understand my way
Line 375: of thinking about design and testing. But you may be thinking that even though we
Line 376: tested each of the price rules individually, and we tested the price calculator with
Line 377: stubbed rules, we don’t know if these pieces will work when we plug them together.
Line 378:  This is a valid skeptical thought. Why not write more tests? Because our tests
Line 379: already cover all the requirements. Structurally, we have covered everything. In these
Line 380: cases, I suggest writing a larger test that exercises all the classes together. In this case,
Line 381: the larger test will exercise FinalPriceCalculator together with all the PriceRules.
Line 382: First, let’s create a factory class in the production code that is responsible for instanti-
Line 383: ating the calculator with all its dependencies.
Line 384: public class FinalPriceCalculatorFactory {
Line 385:   public FinalPriceCalculator build() {
Line 386:     List<PriceRule> priceRules = Arrays.asList(   
Line 387:         new PriceOfItems(),
Line 388:         new ExtraChargeForElectronics(),
Line 389:         new DeliveryPrice());
Line 390:     return new FinalPriceCalculator(priceRules);
Line 391:   }
Line 392: }
Line 393: Now all we need to do is to use the factory to build up a real FinalPriceCalculator
Line 394: and then give it some inputs. To get started, let’s write a test with a shopping cart that
Line 395: has four items (the delivery price is 12.5) and an electronic item (the final price will
Line 396: include the extra charge).
Line 397: public class FinalPriceCalculatorLargerTest {
Line 398:   private final FinalPriceCalculator calculator =
Line 399:   ➥  new FinalPriceCalculatorFactory().build();   
Line 400: Listing 9.10
Line 401: FinalPriceCalculatorFactory 
Line 402: Listing 9.11
Line 403: A larger test for FinalPriceCalculator
Line 404: Makes the stubs 
Line 405: return different values, 
Line 406: given the cart
Line 407: Passes the
Line 408: stubs to the
Line 409: calculator
Line 410: and runs it
Line 411: Given the values we set for 
Line 412: the stubs, we expect a 
Line 413: final value of 3.
Line 414: Passes the list of 
Line 415: PriceRules manually. 
Line 416: You can use dependency 
Line 417: injection frameworks to 
Line 418: do this.
Line 419: Uses a real 
Line 420: FinalPriceCalculator with 
Line 421: all the real PriceRules
Line 422: 
Line 423: --- 페이지 251 ---
Line 424: 223
Line 425: When to use larger tests
Line 426:   @Test
Line 427:   void appliesAllRules() {
Line 428:     ShoppingCart cart = new ShoppingCart();  
Line 429:     cart.add(new Item(ItemType.ELECTRONIC, "PS5", 1, 299));
Line 430:     cart.add(new Item(ItemType.OTHER, "BOOK", 1, 29));
Line 431:     cart.add(new Item(ItemType.OTHER, "CD", 2, 12));
Line 432:     cart.add(new Item(ItemType.OTHER, "CHOCOLATE", 3, 1.50));
Line 433:     double price = calculator.calculate(cart);
Line 434:     double expectedPrice =
Line 435:         299 + 29 + 12 * 2 + 1.50 * 3 +   
Line 436:         7.50 +   
Line 437:         12.5;  
Line 438:     assertThat(price)
Line 439:       .isEqualTo(expectedPrice);  
Line 440:   }
Line 441: }
Line 442: In terms of test code, this is no different from writing a unit test. In fact, based on the
Line 443: definition I gave in chapter 1, I do not consider this an integration test, as it does not
Line 444: go beyond the system’s boundaries. This is a larger test that exercises many units.
Line 445:  From a testing perspective, we can apply specification-based, boundary, and struc-
Line 446: tural testing the same way. The difference is that the granularity may be coarser. When
Line 447: testing the DeliveryPrice unit, we only had to think about the rules related to deliv-
Line 448: ery. Now that we are testing all the behavior together (the calculator plus the price
Line 449: rules), the number of combinations is larger.
Line 450: Specification-based testing in larger tests
Line 451: Let’s look at how I would apply specification-based testing here. I would consider
Line 452: each price rule a category to exercise individually, analogous to the input values of
Line 453: the methods we test in isolation. Therefore, my categories would be price per item,
Line 454: delivery, and electronics extra charge, each with its own partitions. The item itself can
Line 455: also vary. The categories and partitions are as follows:
Line 456: Shopping cart:
Line 457: a
Line 458: Empty cart
Line 459: b
Line 460: 1 element
Line 461: c
Line 462: Many elements
Line 463: Each individual item:
Line 464: a
Line 465: Single quantity
Line 466: b
Line 467: More than one
Line 468: c
Line 469: Unit price times quantity, rounded
Line 470: d
Line 471: Unit price times quantity, not rounded
Line 472: Builds up a 
Line 473: shopping cart
Line 474: The prices of 
Line 475: the items
Line 476: Includes an 
Line 477: electronic
Line 478: Delivery
Line 479: price
Line 480: Asserts that the 
Line 481: final value matches 
Line 482: the shopping cart
Line 483: 
Line 484: --- 페이지 252 ---
Line 485: 224
Line 486: CHAPTER 9
Line 487: Writing larger tests
Line 488: This example shows how much more work it is to test sets of classes together. I use this
Line 489: approach when I see value in it, such as for debugging a problem that happens in pro-
Line 490: duction. However, I use these tests in addition to unit tests. I also do not re-test every-
Line 491: thing. I prefer to use these large component tests as an excuse to try the component
Line 492: with real-world inputs. 
Line 493: 9.1.2
Line 494: Testing larger components that go beyond our code base
Line 495: In the previous example, the large test gives us confidence about the overall behavior
Line 496: of the component, but we could still test each unit individually. In some cases, how-
Line 497: ever, we cannot write tests for units in isolation. Or rather, we can write tests, but doing
Line 498: so would not make sense. Let’s look at examples of two small open source projects I
Line 499: coded.
Line 500: TESTING THE CK TOOL
Line 501: The first example is a project called CK (https://github.com/mauricioaniche/ck),
Line 502: available on my GitHub page. CK is a tool that calculates code metrics for Java code.
Line 503: To do so, it relies on Eclipse JDT (www.eclipse.org/jdt/), a library that is part of the
Line 504: Eclipse IDE. Among its many functionalities, JDT enables us to build abstract syntax
Line 505: trees (ASTs) of Java code. CK builds ASTs using JDT and then visits these trees and cal-
Line 506: culates the different metrics.
Line 507:  As you can imagine, CK is highly dependent on how JDT does things. Given an
Line 508: AST, JDT offers clients a way to visit the tree. Clients need to create a class that inherits
Line 509: from ASTVisitor. (Visitor is a popular design pattern for navigating complex data
Line 510: structures.) CK then implements many of these AST visitors, one for each metric.
Line 511:  One of the metrics that CK implements is coupling between objects (CBO). The
Line 512: metric counts the number of other classes the class under analysis depends on.
Line 513: Imagine the fictitious class A in the following listing. This class declares a field of
Line 514: type B and instantiates class C. CK detects the dependency on B and C and returns 2
Line 515: as the CBO.
Line 516:  
Line 517: (continued)
Line 518: Delivery price:
Line 519: a
Line 520: 1 to 3 items
Line 521: b
Line 522: 4 to 10 items
Line 523: c
Line 524: More than 10 items
Line 525: Electronics:
Line 526: a
Line 527: Has an electronic item
Line 528: b
Line 529: No electronic items
Line 530: I would then combine the partitions that make sense, engineer the different test
Line 531: cases, and write them as automated JUnit tests. I will leave that as an exercise for
Line 532: you.
Line 533: 
Line 534: --- 페이지 253 ---
Line 535: 225
Line 536: When to use larger tests
Line 537: class A {
Line 538:   private B b;
Line 539:   public void action() {
Line 540:     new C().method();
Line 541:   }
Line 542: }
Line 543: In listing 9.13, I show a simplified implementation of the CBO metric (you can see the
Line 544: full code on my GitHub). The implementation looks at any declared or used type in
Line 545: the class and adds it to a set. Later, it returns the number of types in the set. Note all
Line 546: the visit methods: they are called by the JDT whenever there is, for example, a
Line 547: method invocation or a field declaration.
Line 548: public class CBO implements CKASTVisitor {   
Line 549:   private Set<String> coupling = new HashSet<String>();  
Line 550:   @Override
Line 551:   public void visit(MethodInvocation node) {      
Line 552:     IMethodBinding binding = node.resolveMethodBinding();
Line 553:     if(binding!=null)
Line 554:       coupleTo(binding.getDeclaringClass());
Line 555:   }
Line 556:   @Override
Line 557:   public void visit(FieldDeclaration node) {  
Line 558:     coupleTo(node.getType());
Line 559:   }
Line 560:   // this continues for all the possible places where a type can appear...
Line 561:   private void coupleTo(Type type) {
Line 562:     // some complex code here to extract the name of the type.
Line 563:     String fullyQualifiedName = ...;
Line 564:     addToSet(fullyQualifiedName);   
Line 565:   }
Line 566:   private void addToSet(String name) {
Line 567:     this.coupling.add(name);
Line 568:   }
Line 569: }
Line 570: How can we write a unit test for the CBO class? The CBO class offers many visit
Line 571: methods called by the JDT once the JDT builds the AST out of real Java code. We could
Line 572: Listing 9.12
Line 573: Fictitious class A that depends on B and C
Line 574: Listing 9.13
Line 575: CBO implementation in CK
Line 576: I created my own interface, instead of using 
Line 577: JDT’s ASTVisitor, but it is the same thing.
Line 578: Declares a set 
Line 579: to keep all the 
Line 580: unique types 
Line 581: this class uses
Line 582: If there is a method 
Line 583: invocation, gets the 
Line 584: type of the class of 
Line 585: the invoked method
Line 586: If there is a field 
Line 587: declaration, gets the 
Line 588: type of the field
Line 589: Adds the full 
Line 590: name of the 
Line 591: type to the set
Line 592: 
Line 593: --- 페이지 254 ---
Line 594: 226
Line 595: CHAPTER 9
Line 596: Writing larger tests
Line 597: try to mock all the types that these visit methods receive, such as MethodInvocation
Line 598: and FieldDeclaration, and then make a sequence of calls to these methods. But in
Line 599: my opinion, that would be too far from what will happen when we run JDT for real.
Line 600:  I do not see a way to unit-test this class without starting up JDT, asking JDT to build
Line 601: an AST out of a small but real Java class, using CBO to visit the generated AST, and
Line 602: comparing the result. So, I used real integration testing in this case.
Line 603:  The test class in listing 9.14 runs CK (which runs JDT) in a specific directory. This
Line 604: directory contains fake Java classes that I created for the sole purpose of the tests. In
Line 605: the code, it is the cbo directory. I have one directory per metric. Because running JDT
Line 606: takes a few seconds, I run it once for the entire test class (see the @BeforeAll
Line 607: method). The test method then asks for the report of a specific class. In the case of
Line 608: the countDifferentDependencies test, I am interested in the coupling of the fake
Line 609: Coupling1 class. I then assert that its coupling is 6.
Line 610: public class CBOTest extends BaseTest {   
Line 611:   @BeforeAll
Line 612:   public void setUp() {
Line 613:     report = run(fixturesDir() + "/cbo");   
Line 614:   }
Line 615:   @Test
Line 616:   public void countDifferentDependencies() {
Line 617:     CKClassResult result = report.get("cbo.Coupling1");   
Line 618:     assertEquals(6, result.getCbo());   
Line 619:   }
Line 620: }
Line 621: To help you better understand why the CBO is 6, listing 9.15 shows the Coupling1
Line 622: class. This code makes no sense, but it is enough for us to count dependencies. This
Line 623: class uses classes A, B, C, D, C2, and CouplingHelper: that makes six dependencies.
Line 624: public class Coupling1 {
Line 625:   private B b;      
Line 626:   public D m1() {     
Line 627:     A a = new A();   
Line 628:     C[] x = new C[10];   
Line 629:     CouplingHelper h = new CouplingHelper();    
Line 630:     C2 c2 = h.m1();   
Line 631:     return d;
Line 632:   }
Line 633: }
Line 634: Listing 9.14
Line 635: CBOTest 
Line 636: Listing 9.15
Line 637: Coupling1 fixture
Line 638: The BaseTest class provides 
Line 639: basic functionality for all 
Line 640: the test classes.
Line 641: Runs JDT on all code in the cbo 
Line 642: directory. This directory contains 
Line 643: Java code I created solely for 
Line 644: testing purposes.
Line 645: CK returns a report, 
Line 646: which we use to get the 
Line 647: results of a specific Java 
Line 648: class we created for this 
Line 649: test (see listing 9.15).
Line 650: We expect this class to be
Line 651: coupled with six classes.
Line 652: B
Line 653: D
Line 654: A
Line 655: C
Line 656: CouplingHelper
Line 657: C2
Line 658: 
Line 659: --- 페이지 255 ---
Line 660: 227
Line 661: When to use larger tests
Line 662: The CBOTest class contains many other test methods, each exercising a different case.
Line 663: For example, it tests whether CK can count a dependency even though the depen-
Line 664: dency’s code is not available (imagine that class A in the example is not in the direc-
Line 665: tory). It also tests whether it counts interfaces and inherited classes, types in method
Line 666: parameters, and so on.
Line 667:  It was challenging to come up with good test cases here; and it was not easy to
Line 668: apply specification-based testing, because the input could be virtually any Java class.
Line 669: You may face similar challenges when implementing classes for a plug-and-play archi-
Line 670: tecture. This is a good example of a specific context where we need to learn more
Line 671: about how to test. Testing compilers, which is a related problem, is also a significant
Line 672: area of research. 
Line 673: TESTING THE ANDY TOOL
Line 674: Another example where I could not write isolated unit tests involved a tool my teaching
Line 675: assistants and I wrote to assess the test suites that our students engineered. The tool,
Line 676: named Andy (https://github.com/cse1110/andy), compiles the test code provided by a
Line 677: student, runs all the provided JUnit tests, calculates code coverage, runs some static
Line 678: analysis, and checks whether the test suite is strong enough to kill mutant versions of the
Line 679: code under test. Andy then gives a grade and a detailed description of its assessment.
Line 680:  Each step is implemented in its own class. For example, CompilationStep is
Line 681: responsible for compiling the student’s code, RunJUnitTestsStep is responsible for
Line 682: executing all the unit tests in the student’s submission, and RunMetaTestsStep checks
Line 683: whether the test suite kills all the manually engineered mutants we expect it to kill.
Line 684: Figure 9.1 illustrates Andy’s overall flow.
Line 685:  If we were to unit-test everything, we would need a unit test for the compilation
Line 686: step, another for the step that runs JUnit, and so on. But how could we exercise the
Line 687: “run JUnit” step without compiling the code first? It is not possible.
Line 688: Student’s
Line 689: test
Line 690: (“submission”)
Line 691: Program to
Line 692: test
Line 693: (“exercise”)
Line 694: Student
Line 695: Tests
Line 696: Engineers
Line 697: test cases
Line 698: Submits
Line 699: Andy
Line 700: Compiles
Line 701: the code
Line 702: Runs tests
Line 703: Calculates
Line 704: coverage
Line 705: Runs meta
Line 706: tests
Line 707: Generates a ﬁnal
Line 708: assessment
Line 709: Final grade: 78/100
Line 710: Coverage: 85/100
Line 711: Meta tests: 2/3
Line 712: Meta test 1: Killed
Line 713: Meta test 2: Survived
Line 714: …
Line 715: Prints the assessment
Line 716: Figure 9.1
Line 717: Simplified flow of Andy
Line 718: 
Line 719: --- 페이지 256 ---
Line 720: 228
Line 721: CHAPTER 9
Line 722: Writing larger tests
Line 723: We decided to use larger tests. For example, the tests that exercise RunMetaTestsStep
Line 724: run the entire engine we developed. Thus our test provides a real Java file that simulates
Line 725: the student’s submission and another Java file that contains the class under test. Andy
Line 726: gets these files, compiles them, runs the JUnit tests, and finally runs the meta tests.
Line 727:  Listing 9.16 shows one of the tests in the test suite. The run() method, which is
Line 728: implemented in the IntegrationTestBase test base so all the test classes can use it,
Line 729: runs the entire Andy engine. The parameters are real Java files: 
Line 730: 
Line 731: NumberUtilsAddLibrary.java, which contains the code of the class under test 
Line 732: 
Line 733: NumberUtilsAddOfficialSolution.java, which contains a possible solution
Line 734: submitted by the student (in this case, the official solution of this exercise)
Line 735: 
Line 736: NumberUtilsAddConfiguration.java, a configuration class that should be pro-
Line 737: vided by the teacher
Line 738: The run() method returns a Result class: an entity containing all the results of each
Line 739: step. Because this test case focuses on the meta tests, the assertions also focus on them.
Line 740: In this test method, we expect Andy to run four meta tests—AppliesMultipleCarries-
Line 741: Wrongly, DoesNotApplyCarryAtAll, DoesNotApplyLastCarry, and DoesNotCheck-
Line 742: NumbersOutOfRange—and we expect them all to pass.
Line 743: public class MetaTestsTest extends IntegrationTestBase {
Line 744:   @Test
Line 745:   void allMetaTestsPassing() {
Line 746:     Result result =
Line 747:       run(         
Line 748:       "NumberUtilsAddLibrary.java",
Line 749:       "NumberUtilsAddOfficialSolution.java",
Line 750:       "NumberUtilsAddConfiguration.java");
Line 751:     assertThat(result.getMetaTests().getTotalTests())
Line 752:       .isEqualTo(4);  
Line 753:     assertThat(result.getMetaTests().getPassedMetaTests())
Line 754:       .isEqualTo(4);
Line 755:     assertThat(result.getMetaTests())
Line 756:       .has(passedMetaTest("AppliesMultipleCarriesWrongly"))
Line 757:       .has(passedMetaTest("DoesNotApplyCarryAtAll"))
Line 758:       .has(passedMetaTest("DoesNotApplyLastCarry"))
Line 759:       .has(passedMetaTest("DoesNotCheckNumbersOutOfRange"));
Line 760:   }
Line 761: }
Line 762: NOTE
Line 763: You may be curious about the passedMetaTest method in this test
Line 764: method. AssertJ enables us to extend its set of assertions, and we created one
Line 765: specifically for meta tests. I will show how to do this in chapter 10.
Line 766: These two examples illustrate situations where unit-testing a class in isolation does not
Line 767: make sense. In general, my advice is to use unit testing as much as possible, because—as
Line 768: Listing 9.16
Line 769: Integration test for the MetaTests step
Line 770: Runs the full 
Line 771: Andy engine
Line 772: Asserts that
Line 773: the meta tests
Line 774: step executed
Line 775: as expected
Line 776: 
Line 777: --- 페이지 257 ---
Line 778: 229
Line 779: Database and SQL testing
Line 780: I have said many times before—unit tests are cheap and easy to write. But do not be
Line 781: afraid to write larger tests whenever you believe they will give you more confidence. 
Line 782: 9.2
Line 783: Database and SQL testing
Line 784: In many of the examples in this book, a Data Access Object (DAO) class is responsible
Line 785: for retrieving or persisting information in the database. Whenever these classes
Line 786: appear, we quickly stub or mock them out of our way. However, at some point, you
Line 787: need to test these classes. These DAOs often perform complex SQL queries, and they
Line 788: encapsulate a lot of business knowledge, requiring testers to spend some energy mak-
Line 789: ing sure they produce the expected outcomes. The following sections examine what
Line 790: to test in a SQL query, how to write automated test cases for such queries, and the
Line 791: challenges and best practices involved.
Line 792: 9.2.1
Line 793: What to test in a SQL query
Line 794: SQL is a robust language and contains many different functions we can use. Let’s sim-
Line 795: plify and look at queries as a composition of predicates. Here are some examples:
Line 796: 
Line 797: SELECT * FROM INVOICE WHERE VALUE < 50
Line 798: 
Line 799: SELECT * FROM INVOICE I JOIN CUSTOMER C ON I.CUSTOMER_ID = C.ID WHERE
Line 800: C.COUNTRY = 'NL'
Line 801: 
Line 802: SELECT * FROM INVOICE WHERE VALUE > 50 AND VALUE < 200
Line 803: In these examples, value < 50, i.customer_id = c.id, c.country = 'NL', and value >
Line 804: 50 and value < 200 are the predicates that compose the different queries. As a tester, a
Line 805: possible criterion is to exercise the predicates and check whether the SQL query
Line 806: returns the expected results when predicates are evaluated to different results.
Line 807:  Virtually all the testing techniques we have discussed in this book can be applied
Line 808: here:
Line 809: Specification-based testing—SQL queries emerge out of a requirement. A tester can
Line 810: analyze the requirements and derive equivalent partitions that need to be tested.
Line 811: Boundary analysis—Such programs have boundaries. Because we expect bound-
Line 812: aries to be places with a high bug probability, exercising them is important.
Line 813: Structural testing—SQL queries contain predicates, and a tester can use the
Line 814: SQL’s structure to derive test cases.
Line 815: Here, we focus on structural testing. If we look at the third SQL example and try to
Line 816: make an analogy with what we have discussed about structural testing, we see that the
Line 817: SQL query contains a single branch composed of two predicates (value > 50 and
Line 818: value < 200). This means there are four possible combinations of results in these two
Line 819: predicates: (true, true), (true, false), (false, true), and (false, false). We
Line 820: can aim at either of the following:
Line 821: Branch coverage—In this case, two tests (one that makes the overall decision eval-
Line 822: uate to true and one that makes it evaluate to false) would be enough to
Line 823: achieve 100% branch coverage.
Line 824: 
Line 825: --- 페이지 258 ---
Line 826: 230
Line 827: CHAPTER 9
Line 828: Writing larger tests
Line 829: Condition + branch coverage—In this case, three tests would be enough to achieve
Line 830: 100% condition + branch coverage: for example, T1 = 150, T2 = 40, T3 = 250.
Line 831: In “A practical guide to SQL white-box testing,” a 2006 paper by Tuya, Suárez-Cabal,
Line 832: and De La Riva, the authors suggest five guidelines for designing SQL tests:
Line 833: Adopting modified condition/decision coverage (MC/DC) for SQL conditions—Deci-
Line 834: sions happen at three places in a SQL query: join, where, and having condi-
Line 835: tions. We can use criteria like MC/DC to fully exercise the query’s predicates. If
Line 836: you do not remember how MC/DC coverage works, revisit chapter 3.
Line 837: Adapting MC/DC for tackling nulls—Because databases have a special way of han-
Line 838: dling/returning nulls, any (coverage) criteria should be adapted to three-valued
Line 839: logic (true, false, null). In other words, consider the possibility of values being
Line 840: null in your query.
Line 841: Category-partitioning selected data—SQL can be considered a declarative specifica-
Line 842: tion for which we can define partitions to be tested. Directly from Tuya et al.’s
Line 843: paper, we define the following:
Line 844: – Rows that are retrieved—We include a test state to force the query to not select
Line 845: any row.
Line 846: – Rows that are merged—The presence of unwanted duplicate rows in the output
Line 847: is a common failure in some queries. We include a test state in which identi-
Line 848: cal rows are selected.
Line 849: – Rows that are grouped—For each of the group-by columns, we design test states
Line 850: to obtain at least two different groups at the output, such that the value used
Line 851: for the grouping is the same and all the others are different.
Line 852: – Rows that are selected in a subquery—For each subquery, we include test states
Line 853: that return zero or more rows, with at least one null and two different values
Line 854: in the selected column.
Line 855: – Values that participate in aggregate functions—For each aggregate function
Line 856: (excluding count), we include at least one test state in which the function
Line 857: computes two equal values and another that is different.
Line 858: – Other expressions—We also design test states for expressions involving the like
Line 859: predicate, date management, string management, data type conversions, or
Line 860: other functions using category partitioning and boundary checking.
Line 861: Checking the outputs—We should check not only the input domain but also the
Line 862: output domain. SQL queries may return null or empty values in specific col-
Line 863: umns, which may make the rest of the program break.
Line 864: Checking the database constraints—Databases have constraints. We should make
Line 865: sure the database enforces these constraints.
Line 866: As you can see, many things can go wrong in a SQL query. It is part of the tester’s job
Line 867: to make sure that does not happen. 
Line 868: 
Line 869: --- 페이지 259 ---
Line 870: 231
Line 871: Database and SQL testing
Line 872: 9.2.2
Line 873: Writing automated tests for SQL queries
Line 874: We can use JUnit to write SQL tests. All we need to do is (1) establish a connection
Line 875: with the database, (2) make sure the database is in the right initial state, (3) execute
Line 876: the SQL query, and (4) check the output.
Line 877:  Consider the following scenario:
Line 878: We have an Invoice table composed of a name (varchar, length 100) and a value
Line 879: (double).
Line 880: We have an InvoiceDao class that uses an API to communicate with the data-
Line 881: base. The precise API does not matter.
Line 882: This DAO performs three actions: save() persists an invoice in the database,
Line 883: all() returns all invoices in the database, and allWithAtLeast() returns all
Line 884: invoices with at least a specified value. Specifically,
Line 885: – save() runs INSERT INTO invoice (name, value) VALUES (?,?).
Line 886: – all() runs SELECT * FROM invoice.
Line 887: – allWithAtLeast() runs SELECT * FROM invoice WHERE value >= ?.
Line 888: A simple JDBC implementation of such a class is shown in listings 9.17, 9.18, and 9.19.
Line 889: import java.sql.*;
Line 890: import java.util.ArrayList;
Line 891: import java.util.List;
Line 892: public class InvoiceDao {
Line 893:   private final Connection connection;  
Line 894:   public InvoiceDao(Connection connection) {
Line 895:     this.connection = connection;
Line 896:   }
Line 897:   public List<Invoice> all() {
Line 898:     try {
Line 899:       PreparedStatement ps = connection.prepareStatement(
Line 900:         ➥ "select * from invoice");   
Line 901:       ResultSet rs = ps.executeQuery();
Line 902:       List<Invoice> allInvoices = new ArrayList<>();
Line 903:       while (rs.next()) {                                 
Line 904:         allInvoices.add(new Invoice(rs.getString("name"),
Line 905:         ➥ rs.getInt("value")));
Line 906:       }
Line 907:       return allInvoices;
Line 908:     } catch(Exception e) {   
Line 909:       throw new RuntimeException(e);
Line 910:     }
Line 911:   }
Line 912: Listing 9.17
Line 913: Simple JDBC implementation of InvoiceDao, part 1
Line 914: The DAO holds 
Line 915: a connection to 
Line 916: the database.
Line 917: Prepares and 
Line 918: executes the 
Line 919: SQL query
Line 920: Loops through the 
Line 921: results, creating a 
Line 922: new Invoice entity 
Line 923: for each of them
Line 924: The JDBC API throws checked 
Line 925: exceptions. To simplify, we convert 
Line 926: them to unchecked exceptions.
Line 927: 
Line 928: --- 페이지 260 ---
Line 929: 232
Line 930: CHAPTER 9
Line 931: Writing larger tests
Line 932: public List<Invoice> allWithAtLeast(int value) {  
Line 933:     try {
Line 934:       PreparedStatement ps = connection.prepareStatement(
Line 935:         ➥ "select * from invoice where value >= ?");
Line 936:       ps.setInt(1, value);
Line 937:       ResultSet rs = ps.executeQuery();
Line 938:       List<Invoice> allInvoices = new ArrayList<>();
Line 939:       while (rs.next()) {
Line 940:         allInvoices.add(
Line 941:           new Invoice(rs.getString("name"), rs.getInt("value"))
Line 942:         );
Line 943:       }
Line 944:       return allInvoices;
Line 945:     } catch (Exception e) {
Line 946:       throw new RuntimeException(e);
Line 947:     }
Line 948:   }
Line 949: public void save(Invoice inv) {
Line 950:     try {
Line 951:       PreparedStatement ps = connection.prepareStatement(
Line 952:         "insert into invoice (name, value) values (?,?)");  
Line 953:       ps.setString(1, inv.customer);
Line 954:       ps.setInt(2, inv.value);
Line 955:       ps.execute();
Line 956:       connection.commit();
Line 957:     } catch(Exception e) {
Line 958:       throw new RuntimeException(e);
Line 959:     }
Line 960:   }
Line 961: }
Line 962: NOTE
Line 963: This implementation is a naive way to access a database. In more com-
Line 964: plex projects, you should use a professional production-ready database API
Line 965: such as jOOQ, Hibernate, or Spring Data.
Line 966: Let’s test the InvoiceDao class. Remember, we want to apply the same ideas we have
Line 967: seen so far. The difference is that we have a database in the loop. Let’s start with
Line 968: all(). This method sends a SELECT * FROM invoice to the database and gets back the
Line 969: result. But for this query to return something, we must first insert some invoices into
Line 970: the database. The InvoiceDao class also provides the save() method, which sends an
Line 971: INSERT query. This is enough for our first test.
Line 972: Listing 9.18
Line 973: Simple JDBC implementation of InvoiceDao, part 2
Line 974: Listing 9.19
Line 975: Simple JDBC implementation of InvoiceDao, part 3
Line 976: The same thing 
Line 977: happens here: we 
Line 978: prepare the SQL 
Line 979: query, execute it, 
Line 980: and then create one 
Line 981: Invoice entity for 
Line 982: each row.
Line 983: Prepares 
Line 984: the INSERT 
Line 985: statement and 
Line 986: executes it
Line 987: 
Line 988: --- 페이지 261 ---
Line 989: 233
Line 990: Database and SQL testing
Line 991: public class InvoiceDaoIntegrationTest {
Line 992:   private Connection connection;   
Line 993:   private InvoiceDao dao;          
Line 994:   @Test
Line 995:   void save() {
Line 996:    Invoice inv1 = new Invoice("Mauricio", 10);   
Line 997:    Invoice inv2 = new Invoice("Frank", 11);
Line 998:    dao.save(inv1);   
Line 999:    List<Invoice> afterSaving = dao.all();    
Line 1000:    assertThat(afterSaving).containsExactlyInAnyOrder(inv1);
Line 1001:    dao.save(inv2);    
Line 1002:    List<Invoice> afterSavingAgain = dao.all();
Line 1003:    assertThat(afterSavingAgain)
Line 1004:      .containsExactlyInAnyOrder(inv1, inv2);
Line 1005:   }
Line 1006: }
Line 1007: This test method creates two invoices (inv1, inv2), persists the first one using the
Line 1008: save() method, retrieves the invoices from the database, and asserts that it returns
Line 1009: one invoice. Then it persists another invoice, retrieves the invoices from the database
Line 1010: again, and asserts that now it returns two invoices. The test method ensures the cor-
Line 1011: rect behavior of both the save() and all() methods. The containsExactlyInAny-
Line 1012: Order assertion from AssertJ ensures that the list contains the precise invoices that we
Line 1013: pass to it, in any order. For that to happen, the Invoice class needs a proper imple-
Line 1014: mentation of the equals() method.
Line 1015:  In terms of testing, our implementation is correct. However, given the database, we
Line 1016: have some extra concerns. First, we should not forget that the database persists the
Line 1017: data permanently. Suppose we start with an empty database. The first time we run the
Line 1018: test, it will persist two invoices in the database. The second time we run the test, it will
Line 1019: persist two new invoices, totaling four invoices. This will make our test fail, as it
Line 1020: expects the database to have one and two invoices, respectively.
Line 1021:  This was never a problem in our previous unit tests: every object we created lived in
Line 1022: memory, and they disappeared after the test method was done. When testing with a
Line 1023: real database, we must ensure a clean state:
Line 1024: Before the test runs, we open the database connection, clean the database, and
Line 1025: (optionally) put it in the state we need it to be in before executing the SQL
Line 1026: query under test.
Line 1027: After the test runs, we close the database connection.
Line 1028: This is a perfect fit for JUnit’s @BeforeEach and @AfterEach, as shown in the following
Line 1029: listing.
Line 1030: Listing 9.20
Line 1031: First step of our SQL test
Line 1032: This test requires a connection to 
Line 1033: the database and an invoice DAO.
Line 1034: Creates a set 
Line 1035: of invoices
Line 1036: Persists the
Line 1037: first one
Line 1038: Gets all invoices from the database 
Line 1039: and ensures that the database only 
Line 1040: contains the invoice we inserted
Line 1041: Inserts another 
Line 1042: invoice and ensures 
Line 1043: that the database 
Line 1044: contains both of 
Line 1045: them
Line 1046: 
Line 1047: --- 페이지 262 ---
Line 1048: 234
Line 1049: CHAPTER 9
Line 1050: Writing larger tests
Line 1051: public class InvoiceDaoIntegrationTest {
Line 1052:   private Connection connection;
Line 1053:   private InvoiceDao dao;
Line 1054:   @BeforeEach
Line 1055:   void openConnectionAndCleanup() throws SQLException {
Line 1056:     connection = DriverManager.getConnection("jdbc:hsqldb:mem:book");   
Line 1057:     PreparedStatement preparedStatement = connection.prepareStatement(
Line 1058:       ➥ "create table if not exists invoice (name varchar(100),
Line 1059:       ➥ value double)");   
Line 1060:     preparedStatement.execute();
Line 1061:     connection.commit();
Line 1062:     connection.prepareStatement("truncate table invoice").execute();  
Line 1063:     dao = new InvoiceDao(connection);  
Line 1064:   }
Line 1065:   @AfterEach
Line 1066:   void close() throws SQLException {
Line 1067:     connection.close();   
Line 1068:   }
Line 1069:   @Test
Line 1070:   void save() {   
Line 1071:     // ...
Line 1072:   }
Line 1073: }
Line 1074: The openConnectionAndCleanup() method is annotated as @BeforeEach, which
Line 1075: means JUnit will run the cleanup before every test method. Right now, its implemen-
Line 1076: tation is simplistic: it sends a truncate table query to the database.
Line 1077: NOTE
Line 1078: In larger systems, you may prefer to use a framework to help you han-
Line 1079: dle the database. I suggest Flyway (https://flywaydb.org) or Liquibase (https://
Line 1080: www.liquibase.org). In addition to supporting you in evolving your database
Line 1081: schema, these frameworks contain helper methods that help clean up the
Line 1082: database and make sure it contains the right schema (that is, all tables, con-
Line 1083: straints, and indexes are there).
Line 1084: We also open the connection to the database manually, using JDBC’s most rudimen-
Line 1085: tary API call, getConnection. (In a real software system, you would probably ask
Line 1086: Hibernate or Spring Data for an active database connection.) Finally, we close the
Line 1087: connection in the close() method (which happens after every test method).
Line 1088:  Let’s now test the other method: allWithAtLeast(). This method is more interest-
Line 1089: ing, as the SQL query contains a predicate, where value >= ?. This means we have
Line 1090: Listing 9.21
Line 1091: Setting up and tearing down the database
Line 1092: Opens a connection to the database.
Line 1093: For simplicity, I am using HSQLDB, an
Line 1094: in-memory database. In real systems,
Line 1095: you may want to connect to the same
Line 1096: type of database you use in
Line 1097: production.
Line 1098: Ensures that the database has the right tables and schema. 
Line 1099: In this example, we create the invoice table. You may need 
Line 1100: something fancier than that in real applications.
Line 1101: Truncates the table to
Line 1102: ensure that no data from
Line 1103: previous tests is in the
Line 1104: database. Again, you may
Line 1105: need something fancier
Line 1106: in more complex
Line 1107: applications.
Line 1108: Creates
Line 1109: the DAO
Line 1110: Closes the connection. You 
Line 1111: may decide to close the 
Line 1112: connection only at the end of 
Line 1113: the entire test suite. In that 
Line 1114: case, you can use JUnit’s 
Line 1115: @BeforeAll and @AfterAll.
Line 1116: The test
Line 1117: we wrote
Line 1118: 
Line 1119: --- 페이지 263 ---
Line 1120: 235
Line 1121: Database and SQL testing
Line 1122: different scenarios to exercise. Here we can use all of our knowledge about boundary
Line 1123: testing and think of on and off points, as we did in chapter 2.
Line 1124:  Figure 9.2 shows the boundary analysis. The on point is the point on the boundary.
Line 1125: In this case, it is whatever concrete number we pass in the SQL query. The off point
Line 1126: is the nearest point to the on point that flips the condition. In this case, that is what-
Line 1127: ever concrete number we pass in the SQL query minus one, since it makes the con-
Line 1128: dition false.
Line 1129: The following listing shows the JUnit test. Note that we add an in point to the test
Line 1130: suite. Although it isn’t needed, it is cheap to do and makes the test more readable:
Line 1131: @Test
Line 1132: void atLeast() {
Line 1133:   int value = 50;
Line 1134:   Invoice inv1 = new Invoice("Mauricio", value - 1);   
Line 1135:   Invoice inv2 = new Invoice("Arie", value);           
Line 1136:   Invoice inv3 = new Invoice("Frank", value + 1);      
Line 1137:   dao.save(inv1);    
Line 1138:   dao.save(inv2);
Line 1139:   dao.save(inv3);
Line 1140:   List<Invoice> afterSaving = dao.allWithAtLeast(value);
Line 1141:   assertThat(afterSaving)
Line 1142:     .containsExactlyInAnyOrder(inv2, inv3);    
Line 1143: }
Line 1144: The strategy we use to derive the test case is very similar to what we have seen previ-
Line 1145: ously. We exercise the on and off points and then ensure that the result is correct.
Line 1146: Given where value >= ?, where we concretely replace ? with 50 (see the value variable
Line 1147: and the inv2 variable), we have 50 as on point and 49 as off point (value - 1 in inv1).
Line 1148: Listing 9.22
Line 1149: Integration test for the atLeast method
Line 1150: where value >= ?
Line 1151: On point:
Line 1152: Oﬀpoint:
Line 1153: ?
Line 1154: ? – 1
Line 1155: The on point is the number
Line 1156: in the boundary. In this case,
Line 1157: it’s whatever number we
Line 1158: pass in the SQL.
Line 1159: The off point ﬂips the result of the on point. In
Line 1160: this case, it should make the expression false: e.g.,
Line 1161: whatever number we pass in the SQL minus
Line 1162: makes
Line 1163: 1
Line 1164: the expression false.
Line 1165: Figure 9.2
Line 1166: On and off points 
Line 1167: for the allWithAtLeast() 
Line 1168: SQL query
Line 1169: The on point of the value 
Line 1170: >= x boundary is x. The off 
Line 1171: point is x - 1. A random in 
Line 1172: point can be x + 1.
Line 1173: Persists them all 
Line 1174: in the database
Line 1175: We expect the method to 
Line 1176: return only inv2 and inv3.
Line 1177: 
Line 1178: --- 페이지 264 ---
Line 1179: 236
Line 1180: CHAPTER 9
Line 1181: Writing larger tests
Line 1182: In addition, we test a single in point. While doing so is not necessary, as we discussed
Line 1183: in the boundary testing section in chapter 2, one more test case is cheap and makes
Line 1184: the test strategy more comprehensible.
Line 1185: NOTE
Line 1186: Your tests should run against a test database—a database set up exclu-
Line 1187: sively for your tests. Needless to say, you do not want to run your tests against
Line 1188: the production database. 
Line 1189: 9.2.3
Line 1190: Setting up infrastructure for SQL tests
Line 1191: In our example, it was simple to open a connection, reset the database state, and so
Line 1192: on, but that may become more complicated (or lengthy) when your database schema
Line 1193: is complicated. Invest in test infrastructure to facilitate your SQL testing and make
Line 1194: sure that when a developer wants to write an integration test, they do not need to set
Line 1195: up connections manually or handle transactions. This should be a given from the test
Line 1196: suite class.
Line 1197:  A strategy I often apply is to create a base class for my integration tests: say, SQL-
Line 1198: IntegrationTestBase. This base class handles all the magic, such as creating a con-
Line 1199: nection, cleaning up the database, and closing the connection. Then the test class,
Line 1200: such as InvoiceDaoTest, which would extend SQLIntegrationTestBase, focuses only
Line 1201: on testing the SQL queries. JUnit allows you to put BeforeEach and AfterEach in base
Line 1202: classes, and those are executed as if they were in the child test class.
Line 1203:  Another advantage of having all the database logic in the test base class is that
Line 1204: future changes will only need to be made in one place. Listing 9.23 shows an imple-
Line 1205: mentation example. Note how the InvoiceDaoIntegrationTest code focuses primar-
Line 1206: ily on tests.
Line 1207: public class SqlIntegrationTestBase {
Line 1208:   private Connection connection;
Line 1209:   protected InvoiceDao dao;     
Line 1210:   @BeforeEach   
Line 1211:   void openConnectionAndCleanup() throws SQLException {
Line 1212:     // ...
Line 1213:   }
Line 1214:   @AfterEach    
Line 1215:   void close() throws SQLException {
Line 1216:     // ...
Line 1217:   }
Line 1218: }
Line 1219: public class InvoiceDaoIntegrationTest extends SqlIntegrationTestBase {  
Line 1220: Listing 9.23
Line 1221: Base class that handles the database-related logic
Line 1222: Makes the InvoiceDao 
Line 1223: protected so we can access 
Line 1224: it from the child classes
Line 1225: The methods
Line 1226: are the same
Line 1227: as before.
Line 1228: InvoiceDaoTest now extends
Line 1229: SqlIntegrationTestBase.
Line 1230: 
Line 1231: --- 페이지 265 ---
Line 1232: 237
Line 1233: Database and SQL testing
Line 1234:   @Test
Line 1235:   void save() {      
Line 1236:     // ...
Line 1237:   }
Line 1238:   @Test
Line 1239:   void atLeast() {   
Line 1240:     // ...
Line 1241:   }
Line 1242: }
Line 1243: I will not provide a complete code example, because it changes from project to proj-
Line 1244: ect. Instead, the following sections list what I do in such an integration test base class.
Line 1245: OPENING THE DATABASE CONNECTION
Line 1246: This means opening a JDBC connection, a Hibernate connection, or the connection
Line 1247: of whatever persistence framework you use. In some cases, you may be able to open a
Line 1248: single connection per test suite instead of one per test method. In this case, you may
Line 1249: want to declare it as static and use JUnit’s BeforeAll to open and AfterAll to close it. 
Line 1250: OPENING AND COMMITTING THE TRANSACTION
Line 1251: In more complex database operations, it is common to make them all happen
Line 1252: within a transaction scope. In some systems, your framework handles this automati-
Line 1253: cally (think of Spring and its @Transactional annotations). In other systems, devel-
Line 1254: opers do it by hand, calling something that begins the transaction and later something
Line 1255: that commits it.
Line 1256:  You should decide on how to handle transactions in your test. A common approach
Line 1257: is to open the transaction and, at the end of the test method, commit the transaction.
Line 1258: Some people never commit the transaction, but roll it back once the test is over.
Line 1259: Because this is an integration test, I suggest committing the transaction for each test
Line 1260: method (and not for the entire test class, as we did for the connection). 
Line 1261: RESETTING THE STATE OF THE DATABASE
Line 1262: You want all your tests to start with a clean database state. This means ensuring the
Line 1263: correct database schema and having no unexpected data in the tables. The simplest
Line 1264: way to do this is to truncate every table at the beginning of each test method. If you
Line 1265: have many tables, you truncate them all. You can do this by hand (and manually add
Line 1266: one truncate instruction per table in the code) or use a smarter framework that does
Line 1267: it automatically.
Line 1268:  Some developers prefer to truncate the tables before the test method, and others
Line 1269: after. In the former case, you are sure the database is clean before running the test. In
Line 1270: the latter, you ensure that everything is clean afterward, which helps ensure that it will
Line 1271: be clean the next time you run it. I prefer to avoid confusion and truncate before the
Line 1272: test method. 
Line 1273: The test class focuses on 
Line 1274: the tests themselves, as the 
Line 1275: database infrastructure is 
Line 1276: handled by the base class.
Line 1277: 
Line 1278: --- 페이지 266 ---
Line 1279: 238
Line 1280: CHAPTER 9
Line 1281: Writing larger tests
Line 1282: HELPER METHODS THAT REDUCE THE AMOUNT OF CODE IN THE TESTS
Line 1283: SQL integration test methods can be long. You may need to create many entities
Line 1284: and perform more complex assertions. If code can be reused by many other tests, I
Line 1285: extract it to a method and move it to the base class. The test classes now all inherit
Line 1286: this utility method and can use it. Object builders, frequent assertions, and specific
Line 1287: database operations that are often reused are good candidates to become methods
Line 1288: in the base class. 
Line 1289: 9.2.4
Line 1290: Best practices
Line 1291: Let’s close this section with some final tips on writing tests for SQL queries.
Line 1292: USE TEST DATA BUILDERS
Line 1293: Creating invoices in our earlier example was a simple task. The entity was small and
Line 1294: contained only two properties. However, entities in real-world systems are much more
Line 1295: complex and may require more work to be instantiated. You do not want to write 15
Line 1296: lines of code and pass 20 parameters to create a simple invoice object. Instead, use
Line 1297: helper classes that instantiate test objects for you. These test data builders, as they are
Line 1298: known, help you quickly build the data structures you need. I will show how to imple-
Line 1299: ment test data builders in chapter 10. 
Line 1300: USE GOOD AND REUSABLE ASSERTION APIS
Line 1301: Asserting was easy in the example, thanks to AssertJ. However, many SQL queries
Line 1302: return lists of objects, and AssertJ provides several methods to assert them in many dif-
Line 1303: ferent ways. If a specific assertion is required by many test methods, do not be afraid
Line 1304: to create a utility method that encapsulates this complex assertion. As I discussed, put-
Line 1305: ting it in the base test class is my usual way to go. 
Line 1306: MINIMIZE THE REQUIRED DATA
Line 1307: Make sure the input data is minimized. You do not want to have to load hundreds of
Line 1308: thousands of elements to exercise your SQL query. If your test only requires data in
Line 1309: two tables, only insert data in these two tables. If your test requires no more than 10
Line 1310: rows in that table, only insert 10 rows. 
Line 1311: TAKE THE SCHEMA EVOLUTION INTO CONSIDERATION
Line 1312: In real software systems, database schemas evolve quickly. Make sure your test suite is
Line 1313: resilient toward these changes. In other words, database evolution should not break
Line 1314: the existing test suite. Of course, you cannot (and you probably do not want to)
Line 1315: decouple your code completely from the database. But if you are writing a test and
Line 1316: notice that a future change may break it, consider reducing the number of points that
Line 1317: will require change. Also, if the database changes, you must propagate the change to
Line 1318: the test database. If you are using a framework to help you with migration (like Flyway
Line 1319: or Liquibase), you can ask the framework to perform the migrations. 
Line 1320: 
Line 1321: --- 페이지 267 ---
Line 1322: 239
Line 1323: System tests
Line 1324: CONSIDER (OR DON’T) AN IN-MEMORY DATABASE
Line 1325: You should decide whether your tests will communicate with a real database (the same
Line 1326: type of database as in your production environment) or a simpler database (such as
Line 1327: an in-memory database). As always, both sides have advantages and disadvantages.
Line 1328: Using the same database as in production makes your tests more realistic: your tests
Line 1329: will exercise the same SQL engine that will be exercised in production. On the other
Line 1330: hand, running full-blown MySQL is much more expensive, computationally speaking,
Line 1331: than a simple in-memory database. All in all, I favor using real databases when I am
Line 1332: writing SQL integration tests. 
Line 1333: 9.3
Line 1334: System tests
Line 1335: At some point, your classes, business rules, persistence layers, and so on are combined
Line 1336: to form, for example, a web application. Let’s think about how a web application tradi-
Line 1337: tionally works. Users visit a web page (that is, their browser makes a request to the
Line 1338: server, and the server processes the request and returns a response that the browser
Line 1339: shows) and interact with the elements on the page. These interactions often trigger
Line 1340: other requests and responses. Considering a pet clinic application: a user goes to the
Line 1341: web page that lists all the scheduled appointments for today, clicks the New Appoint-
Line 1342: ment button, fills out the name of their pet and its owner, and selects an available time
Line 1343: slot. The web page then takes the user back to the Appointments page, which now
Line 1344: shows the newly added appointment.
Line 1345:  If this pet clinic web application was developed using test-driven approaches and
Line 1346: everything we discussed in the previous chapters of this book, the developer already
Line 1347: wrote (systematic) unit tests for each unit in the software. For example, the Appointment
Line 1348: class already has unit tests of its own.
Line 1349:  In this section, we discuss what to test in a web application and what tools we can
Line 1350: use to automatically open the browser and interact with the web page. We also discuss
Line 1351: some best practices for writing system tests.
Line 1352: NOTE
Line 1353: Although I use a web application as an example of how to write a sys-
Line 1354: tem test, the ideas in this section apply to any other type of software system.
Line 1355: 9.3.1
Line 1356: An introduction to Selenium
Line 1357: Before diving into the best practices, let’s get familiar with the mechanics of writing such
Line 1358: tests. For that, we will rely on Selenium. The Selenium framework (www.selenium.dev)
Line 1359: is a well-known tool that supports developers in testing web applications. Selenium
Line 1360: can connect to any browser and control it. Then, through the Selenium API, we can
Line 1361: give commands such as “open this URL,” “find this HTML element in the page and
Line 1362: get its inner text,” and “click that button.” We will use commands like these to test our
Line 1363: web applications.
Line 1364:  We use the Spring PetClinic web application (https://projects.spring.io/spring
Line 1365: -petclinic) as an example throughout this section. If you are a Java web developer,
Line 1366: you are probably familiar with Spring Boot. For those who are not, Spring Boot is
Line 1367: 
Line 1368: --- 페이지 268 ---
Line 1369: 240
Line 1370: CHAPTER 9
Line 1371: Writing larger tests
Line 1372: the state-of-the-art framework for web development in Java. Spring PetClinic is a sim-
Line 1373: ple web application that illustrates how powerful and easy to use Spring Boot is. Its
Line 1374: code base contains the two lines required for you to download (via Git) and run (via
Line 1375: Maven) the web application. Once you do, you should be able to visit your local-
Line 1376: host:8080 and see the web application, shown in figures 9.3 and 9.4.
Line 1377: Figure 9.3
Line 1378: First screenshot of the Spring PetClinic application
Line 1379: Figure 9.4
Line 1380: Second screenshot of the Spring PetClinic application
Line 1381: 
Line 1382: --- 페이지 269 ---
Line 1383: 241
Line 1384: System tests
Line 1385: Before discussing testing techniques and best practices, let’s get started with Sele-
Line 1386: nium. The Selenium API is intuitive and easy to use. The following listing shows our
Line 1387: first test.
Line 1388: public class FirstSeleniumTest {
Line 1389:   @Test
Line 1390:   void firstSeleniumTest() {
Line 1391:     WebDriver browser = new SafariDriver();   
Line 1392:     browser.get("http:/ /localhost:8080");   
Line 1393:     WebElement welcomeHeader = browser.findElement(By.tagName("h2"));   
Line 1394:     assertThat(welcomeHeader.getText())
Line 1395:       .isEqualTo("Welcome");  
Line 1396:     browser.close();   
Line 1397:   }
Line 1398: }
Line 1399: Let’s go line by line:
Line 1400: 1
Line 1401: The first line, WebDriver browser = new SafariDriver(), instantiates a Safari
Line 1402: browser. WebDriver is the abstraction that all other browsers implement. If you
Line 1403: would like to try a different browser, you can use new FirefoxBrowser() or new
Line 1404: ChromeBrowser() instead. I am using Safari for two reasons:
Line 1405: a
Line 1406: I am a Mac user, and Safari is often my browser of choice.
Line 1407: b
Line 1408: Other browsers, such as Chrome, may require you to download an external
Line 1409: application that enables Safari to communicate with it. In the case of Chrome,
Line 1410: you need to download ChromeDriver (https://chromedriver.chromium.org/
Line 1411: downloads).
Line 1412: 2
Line 1413: With an instantiated browser, we visit a URL by means of browser.get("url");.
Line 1414: Whatever URL we pass, the browser will visit. Remember that Selenium is not
Line 1415: simulating the browser: it is using the real browser.
Line 1416: 3
Line 1417: The test visits the home page of the Spring PetClinic web app (figure 9.3). This
Line 1418: website is very simple and shows a brief message (“Welcome”) and a cute pic-
Line 1419: ture of a dog and a cat. To ensure that we can extract data from the page we are
Line 1420: visiting, let’s ensure that the “Welcome” message is on the screen. To do that,
Line 1421: we first must locate the element that contains the message. Knowledge of
Line 1422: HTML and DOM is required here.
Line 1423: If you inspect the HTML of the Spring PetClinic, you see that the message is
Line 1424: within an h2 tag. Later, we discuss the best ways to locate elements on the page;
Line 1425: but for now, we locate the only h2 element. To do so, we use Selenium’s find-
Line 1426: Element() function, which receives a strategy that Selenium will use to find the
Line 1427: Listing 9.24
Line 1428: Our first Selenium test
Line 1429: Selects a driver. The 
Line 1430: driver indicates which 
Line 1431: browser to use.
Line 1432: Visits a page at 
Line 1433: the given URL
Line 1434: Finds an HTML
Line 1435: element in the page
Line 1436: Asserts that the 
Line 1437: page contains 
Line 1438: what we want
Line 1439: Closes the browser and 
Line 1440: the selenium session
Line 1441: 
Line 1442: --- 페이지 270 ---
Line 1443: 242
Line 1444: CHAPTER 9
Line 1445: Writing larger tests
Line 1446: element. We can find elements by their names, IDs, CSS classes, and tag name.
Line 1447: By.tagName("h2") returns a WebElement, an abstraction representing an ele-
Line 1448: ment on the web page.
Line 1449: 4
Line 1450: We extract some properties of this element: in particular, the text inside the h2
Line 1451: tag. For that, we call the getText() method. Because we expect it to return
Line 1452: “Welcome”, we write an assertion the same way we are used to. Remember, this
Line 1453: is an automated test. If the web element does not contain “Welcome”, the test
Line 1454: will fail.
Line 1455: 5
Line 1456: We close the browser. This is an important step, as it disconnects Selenium
Line 1457: from the browser. It is always a good practice to close any resources you use in
Line 1458: your tests.
Line 1459: If you run the test, you should see Safari (or your browser of choice) open, be auto-
Line 1460: matically controlled by Selenium, and then close. This will get more exciting when we
Line 1461: start to fill out forms. 
Line 1462: 9.3.2
Line 1463: Designing page objects
Line 1464: For web applications and system testing, we do not want to exercise just one unit of
Line 1465: the system but the entire system. We want to do what we called system testing in chap-
Line 1466: ter 1. What should we test in a web application, with all the components working
Line 1467: together and an infinite number of different paths to test?
Line 1468:  Following what we discussed in the testing pyramid, all the units of the web appli-
Line 1469: cation are at this point (we hope) already tested at the unit or integration level. The
Line 1470: entities in the Spring PetClinic, such as Owner or Pet, have been unit-tested, and all
Line 1471: the queries that may exist in DAOs have also been tested via integration tests similar to
Line 1472: what we just did.
Line 1473:  But if everything has already been tested, what is left for us to test? We can test the
Line 1474: different user journeys via web testing. Here is Fowler’s definition of a user journey test
Line 1475: (2003): “User-journey tests are a form of business-facing test, designed to simulate a
Line 1476: typical user’s journey through the system. Such a test will typically cover a user’s entire
Line 1477: interaction with the system to achieve some goal. They act as one path in a use case.”
Line 1478:  Think of possible user journeys in the Spring PetClinic application. One possible
Line 1479: journey is the user trying to find owners. Other possible journeys include the user
Line 1480: adding a new owner, adding a pet to the owner, or adding a log entry of the pet after
Line 1481: the pet visits the veterinarian.
Line 1482:  Let’s test one journey: the find owners journey. We will code this test using a Page
Line 1483: Object pattern. Page objects (POs) help us write more maintainable and readable web
Line 1484: tests. The idea of the Page Object pattern is to define a class that encapsulates all the
Line 1485: (Selenium) logic involved in manipulating one page.
Line 1486:  For example, if the application has a List of Owners page that shows all the owners,
Line 1487: we will create a ListOfOwnersPage class that will know how to handle it (such as
Line 1488: extracting the names of the owners from the HTML). If the application has an Add
Line 1489: Owner page, we will create an AddOwnerPage class that will know how to handle it
Line 1490: 
Line 1491: --- 페이지 271 ---
Line 1492: 243
Line 1493: System tests
Line 1494: (such as filling out the form with the name of the new owner and clicking the button
Line 1495: that saves it). Later, we will put all these POs together in a JUnit test, simulate the
Line 1496: whole journey, and assert that it went as expected.
Line 1497:  When I write Selenium web tests, I prefer to start by designing my POs. Let’s begin
Line 1498: by modeling the first page of this journey: the Find Owners page. This page is shown
Line 1499: in figure 9.5, and the page can be accessed by clicking the Find Owners link in the menu.
Line 1500: This page primarily contains one interesting thing to be modeled: the “find owners”
Line 1501: functionality. For that to work, we need to fill in the Last Name input field and click
Line 1502: the Find Owners button. Let’s start with that.
Line 1503: public class FindOwnersPage extends PetClinicPageObject {
Line 1504:   public FindOwnersPage(WebDriver driver) {  
Line 1505:     super(driver);
Line 1506:   }
Line 1507:   public ListOfOwnersPage findOwners(String ownerLastName) {   
Line 1508:     driver.findElement(By.id("lastName")).sendKeys(ownerLastName);   
Line 1509:     WebElement findOwnerButton = driver
Line 1510:       .findElement(By.id("search-owner-form"))
Line 1511:       .findElement(By.tagName("button"));
Line 1512:     findOwnerButton.click();   
Line 1513:     ListOfOwnersPage listOfOwnersPage = new ListOfOwnersPage(driver);  
Line 1514:     listOfOwnersPage.isReady();   
Line 1515:     return listOfOwnersPage;
Line 1516:   }
Line 1517: }
Line 1518: Listing 9.25
Line 1519: FindOwners page object
Line 1520: We need to type the name of the owner in
Line 1521: this HTML ﬁeld and press the Find Owner
Line 1522: button for the search to happen.
Line 1523: Figure 9.5
Line 1524: The Find Owners page
Line 1525: The constructor of all our POs receives the Selenium 
Line 1526: driver. The PO needs it to manipulate the web page.
Line 1527: This method is
Line 1528: responsible for
Line 1529: finding an owner
Line 1530: on this page based
Line 1531: on their last name.
Line 1532: Finds the HTML element
Line 1533: whose ID is lastName and
Line 1534: types the last name of the
Line 1535: owner we are looking for.
Line 1536: Clicks the
Line 1537: Find Owner
Line 1538: button. We
Line 1539: find it on
Line 1540: the page by
Line 1541: its ID.
Line 1542: Takes us to another page.
Line 1543: To represent that, we
Line 1544: make the PO return the
Line 1545: new page, also as a PO.
Line 1546: Waits for the 
Line 1547: page to be 
Line 1548: ready before 
Line 1549: returning it
Line 1550: 
Line 1551: --- 페이지 272 ---
Line 1552: 244
Line 1553: CHAPTER 9
Line 1554: Writing larger tests
Line 1555: Let’s look at this code line by line:
Line 1556: 1
Line 1557: The newly created class FindOwnersPage represents the Find Owners page. It
Line 1558: inherits from another class, PetClinicPageObject, which will serve as a com-
Line 1559: mon abstraction for our POs. I show its source code later.
Line 1560: 2
Line 1561: Our POs always have a constructor that receives a WebDriver. Everything we do
Line 1562: with Selenium starts with the WebDriver class, which we will instantiate later
Line 1563: from a JUnit test method.
Line 1564: 3
Line 1565: Methods in this PO represent actions we can take with the page we are model-
Line 1566: ing. The first action we modeled is findOwners(), which fills the Last Name
Line 1567: input with the value passed to the ownerLastName string parameter.
Line 1568: 4
Line 1569: The implementation of the method is straightforward. We first locate the
Line 1570: HTML input element. By inspecting the Spring PetClinic web page, we see that
Line 1571: the field has an ID. Elements with IDs are usually easy to find, as IDs are unique
Line 1572: in the page. With the element in hand, we use the sendKeys() function to fill in
Line 1573: the input with ownerLastName. Selenium’s API is fluent, so we can chain the
Line 1574: method calls: findElement(…).sendKeys(…).
Line 1575: 5
Line 1576: We search for the Find Owner button. When inspecting the page, we see that
Line 1577: this button does not have a specific ID. This means we need to find another way
Line 1578: to locate it on the HTML page. My first instinct is to see if this button’s HTML
Line 1579: form has an ID. It does: search-owner-form. We can locate the form and then
Line 1580: locate a button inside it (as this form has one button).
Line 1581: Note how we chain calls for the findElement method. Remember that
Line 1582: HTML elements may have other HTML elements inside them. Therefore, the
Line 1583: first findElement() returns the form, and the second findElement searches
Line 1584: only the elements inside the element returned by the first findElement. With
Line 1585: the button available to us, we call the click() method, which clicks the button.
Line 1586: The form is now submitted.
Line 1587: 6
Line 1588: The website takes us to another page that shows the list of owners with the
Line 1589: searched last name. This is no longer the Find Owners page, so we should now
Line 1590: use another PO to represent the current page. That is why we make the find-
Line 1591: Owners() method return a ListOfOwnersPage: one page takes you to another
Line 1592: page.
Line 1593: 7
Line 1594: Before we return the newly instantiated ListOfOwnersPage, we call an isReady()
Line 1595: method. This method waits for the Owners page to be ready. Remember that
Line 1596: this is a web application, so requests and responses may take some time. If we
Line 1597: try to look for an element from the page, but the element is not there yet, the
Line 1598: test will fail. Selenium has a set of APIs that enable us to wait for such things,
Line 1599: which we will see soon.
Line 1600: We still have more POs to model before writing the test for the entire journey. Let’s
Line 1601: model the Owners page, shown in figure 9.6. This page contains a table in which each
Line 1602: row represents one owner.
Line 1603: 
Line 1604: --- 페이지 273 ---
Line 1605: 245
Line 1606: System tests
Line 1607: Our ListOfOwnersPage PO models a single action that will be very important for our
Line 1608: test later: getting the list of owners in this table. The following listing shows the source
Line 1609: code.
Line 1610: public class ListOfOwnersPage extends PetClinicPageObject {
Line 1611:   public ListOfOwnersPage(WebDriver driver) {    
Line 1612:     super(driver);
Line 1613:   }
Line 1614:   @Override
Line 1615:   public void isReady() {   
Line 1616:     WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
Line 1617:     wait.until(
Line 1618:       ExpectedConditions.visibilityOfElementLocated(
Line 1619:       By.id("owners")));    
Line 1620:   }
Line 1621:   public List<OwnerInfo> all() {
Line 1622:     List<OwnerInfo> owners = new ArrayList<>();    
Line 1623:     WebElement table = driver.findElement(By.id("owners"));   
Line 1624:     List<WebElement> rows = table.findElement(By.tagName(
Line 1625:       ➥ "tbody")).findElements(By.tagName("tr"));
Line 1626:     for (WebElement row : rows) {    
Line 1627:       List<WebElement> columns = row.findElements(By.tagName("td"));  
Line 1628:       String name = columns.get(0).getText().trim();   
Line 1629:       String address = columns.get(1).getText().trim();
Line 1630:       String city = columns.get(2).getText().trim();
Line 1631:       String telephone = columns.get(3).getText().trim();
Line 1632:       String pets = columns.get(4).getText().trim();
Line 1633: Listing 9.26
Line 1634: ListOfOwners PO
Line 1635: We need to get the list of
Line 1636: owners from this HTML table.
Line 1637: Figure 9.6
Line 1638: The Owners page
Line 1639: As we know, all POs receive the 
Line 1640: WebDriver in the constructor.
Line 1641: The isReady method lets us know whether the 
Line 1642: page is ready in the browser so we can start 
Line 1643: manipulating it. This is important, as some 
Line 1644: pages take more time than others to load.
Line 1645: The Owners page is considered ready when the list of 
Line 1646: owners is loaded. We find the table with owners by its 
Line 1647: ID. We wait up to three seconds for that to happen.
Line 1648: Creates
Line 1649: a list to
Line 1650: hold all the
Line 1651: owners. For
Line 1652: that, we
Line 1653: create an
Line 1654: OwnerInfo
Line 1655: class.
Line 1656: Gets the HTML table 
Line 1657: and all its rows. The 
Line 1658: table’s ID is owners, 
Line 1659: which makes it easy 
Line 1660: to find.
Line 1661: For each row in 
Line 1662: the table …
Line 1663: … gets the 
Line 1664: HTML row
Line 1665: Gets the value of each 
Line 1666: HTML cell. The first 
Line 1667: column contains the 
Line 1668: name, the second the 
Line 1669: address, and so on.
Line 1670: 
Line 1671: --- 페이지 274 ---
Line 1672: 246
Line 1673: CHAPTER 9
Line 1674: Writing larger tests
Line 1675:       OwnerInfo ownerInfo = new OwnerInfo(
Line 1676:         ➥ name, address, city, telephone, pets);    
Line 1677:       owners.add(ownerInfo);
Line 1678:     }
Line 1679:     return owners;   
Line 1680:   }
Line 1681: }
Line 1682: Let’s walk through this code:
Line 1683: 1
Line 1684: Our class is a PO, so it extends from PetClinicPageObject, which forces the
Line 1685: class to have a constructor that receives a WebDriver. We still have not seen the
Line 1686: PetClinicPageObject code, but we will soon.
Line 1687: 2
Line 1688: The isReady() method (which you can see by the @Override annotation is also
Line 1689: defined in the base class) knows when this page is loaded. How do we do this?
Line 1690: The simplest way is to wait a few seconds for a specific element to appear on the
Line 1691: page. In this case, we wait for the element with ID “owners” (the table with all
Line 1692: the owners) to be on the page. We tell WebDriverWait to wait up to three sec-
Line 1693: onds for the owners element to be visible. If the element is not there after three
Line 1694: seconds, the method throws an exception. Why three seconds? That was a
Line 1695: guess; in practice, you have to find the number that best fits your test.
Line 1696: 3
Line 1697: We return to our main action: the all() method. The objective is to extract the
Line 1698: names of all the owners. Because this is an HTML table, we know that each row
Line 1699: is in a tr element. The table has a header, which we want to ignore. So, we
Line 1700: locate #owners > tbody > tr or, in other words, all trs inside tbody that are
Line 1701: inside the owners element. We do this using nested findElement() and find-
Line 1702: Elements() calls. Note the difference between the two methods: one returns a
Line 1703: single element, the other multiple elements (useful in this case, as we know
Line 1704: there are many trs to be returned).
Line 1705: 4
Line 1706: With the list of rows ready, we iterate over each element. We know that trs are
Line 1707: composed of tds. We find all tds inside the current tr and extract the text
Line 1708: inside each td, one by one. We know the first cell contains the name, the sec-
Line 1709: ond cell contains the address, and so on. We then build an object to hold this
Line 1710: information: the OwnerInfo class. This is a simple class with getters only. We also
Line 1711: trim() the string to get rid of any whitespaces in the HTML.
Line 1712: 5
Line 1713: We return the list of owners in the table.
Line 1714: Now, searching for an owner with their surname takes us to the next page, where we
Line 1715: can extract the list of owners. Figure 9.7 illustrates the two POs we have implemented
Line 1716: so far and which pages of the web application they model.
Line 1717:  We are only missing two things. First and foremost, to search for an owner, the
Line 1718: owner must be in the application. How do we add a new owner? We use the Add
Line 1719: Owner page. So, we need to model one more PO. Second we need a way to visit these
Line 1720: pages for the first time.
Line 1721: Once all the information 
Line 1722: is collected from the 
Line 1723: HTML, we build an 
Line 1724: OwnerInfo class.
Line 1725: Returns a list of 
Line 1726: OwnerInfos. This object 
Line 1727: knows nothing about 
Line 1728: the HTML page.
Line 1729: 
Line 1730: --- 페이지 275 ---
Line 1731: 247
Line 1732: System tests
Line 1733: NOTE
Line 1734: Much more work is required to write a test for a single journey than we
Line 1735: are used to when doing unit tests. System tests are naturally more expensive
Line 1736: to create. But I also want you to recognize that adding a new test becomes eas-
Line 1737: ier once you have an initial structure with POs. The high cost comes now,
Line 1738: when building this initial infrastructure.
Line 1739: Let’s start with adding an owner. The next listing shows the AddOwnerPage PO.
Line 1740: public class AddOwnerPage extends PetClinicPageObject {
Line 1741:   public AddOwnerPage(WebDriver driver) {   
Line 1742:     super(driver);
Line 1743:   }
Line 1744:   @Override
Line 1745:   public void isReady() {
Line 1746:     WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
Line 1747:     wait.until(
Line 1748:       ExpectedConditions.visibilityOfElementLocated(
Line 1749:       By.id("add-owner-form")));     
Line 1750:   }
Line 1751:   public OwnerInformationPage add(AddOwnerInfo ownerToBeAdded) {
Line 1752:     driver.findElement(By.id("firstName"))
Line 1753:       .sendKeys(ownerToBeAdded.getFirstName());   
Line 1754:     driver.findElement(By.id("lastName"))
Line 1755:       .sendKeys(ownerToBeAdded.getLastName());
Line 1756:     driver.findElement(By.id("address"))
Line 1757:       .sendKeys(ownerToBeAdded.getAddress());
Line 1758:     driver.findElement(By.id("city"))
Line 1759:       .sendKeys(ownerToBeAdded.getCity());
Line 1760:     driver.findElement(By.id("telephone"))
Line 1761:       .sendKeys(ownerToBeAdded.getTelephone());
Line 1762: Listing 9.27
Line 1763: .AddOwnerPage page object
Line 1764: /findOwners
Line 1765: owners?lastName=x
Line 1766: FindOwnersPage
Line 1767: (Java object)
Line 1768: ow er
Line 1769: n
Line 1770: s()
Line 1771: …
Line 1772: ListOfOwnersPage
Line 1773: (Java object)
Line 1774: all()
Line 1775: …
Line 1776: Web pages
Line 1777: Page objects
Line 1778: Each page object represents one web page. It contains elegant
Line 1779: methods that know how to manipulate the page. Test methods
Line 1780: use these page objects to test the web application.
Line 1781: Figure 9.7
Line 1782: An illustration 
Line 1783: of web pages and their 
Line 1784: respective POs
Line 1785: Again, the PO 
Line 1786: receives the 
Line 1787: WebDriver.
Line 1788: The HTML page is 
Line 1789: ready when the 
Line 1790: form appears on 
Line 1791: the screen.
Line 1792: Fills out all the HTML form 
Line 1793: elements with the data 
Line 1794: provided in AddOwnerInfo, 
Line 1795: a class created for that 
Line 1796: purpose. We find the form 
Line 1797: elements by their IDs.
Line 1798: 
Line 1799: --- 페이지 276 ---
Line 1800: 248
Line 1801: CHAPTER 9
Line 1802: Writing larger tests
Line 1803:     driver.findElement(By.id("add-owner-form"))
Line 1804:         .findElement(By.tagName("button"))
Line 1805:         .click();     
Line 1806:     OwnerInformationPage ownerInformationPage =
Line 1807:       new OwnerInformationPage(driver);  
Line 1808:     ownerInformationPage.isReady();
Line 1809:     return ownerInformationPage;
Line 1810:   }
Line 1811: }
Line 1812: The implementation should not be a surprise. The isReady() method waits for the
Line 1813: form to be ready. The add() method, which is the relevant method here, finds the
Line 1814: input elements (which all have specific IDs, making our lives much easier), fills them
Line 1815: in, finds the Add Owner button, and returns the PO that represents the page we go to
Line 1816: after adding an owner: OwnerInformationPage. I do not show its code, to save space,
Line 1817: but it is a PO much like the others we have seen.
Line 1818:  Finally, all we need is a way to visit the pages. I usually have a visit() method in
Line 1819: my POs to take me directly to that page. Let’s add a visit() method to the POs we
Line 1820: need to visit: the Find Owner page and the Add Owner page.
Line 1821: // FindOwnersPage
Line 1822: public void visit() {
Line 1823:   visit("/owners/find");
Line 1824: }
Line 1825: // AddOwnersPage
Line 1826: public void visit() {
Line 1827:   visit("/owners/new");
Line 1828: }
Line 1829: Note that these visit() methods call another visit method in the superclass.
Line 1830:  Now it is time to show the PO base class. This is where we put common behavior
Line 1831: that all our POs have. Base classes like these support and simplify the development of
Line 1832: our tests.
Line 1833: public abstract class PetClinicPageObject {
Line 1834:   protected final WebDriver driver;   
Line 1835:   public PetClinicPageObject(WebDriver driver) {
Line 1836:     this.driver = driver;
Line 1837:   }
Line 1838:   public void visit() {     
Line 1839:     throw new RuntimeException("This page does not have a visit link");
Line 1840:   }
Line 1841: Listing 9.28
Line 1842: Adding visit() methods to all the POs
Line 1843: Listing 9.29
Line 1844: Initial code of the PO base class
Line 1845: Clicks the 
Line 1846: Add button
Line 1847: When an owner is added, the web 
Line 1848: application redirects us to the Owner 
Line 1849: Information page. The method then 
Line 1850: returns the PO of the class we are 
Line 1851: redirected to.
Line 1852: The base class keeps 
Line 1853: the reference to the 
Line 1854: WebDriver.
Line 1855: The visit method 
Line 1856: should be overridden 
Line 1857: by the child classes.
Line 1858: 
Line 1859: --- 페이지 277 ---
Line 1860: 249
Line 1861: System tests
Line 1862:   protected void visit(String url) {       
Line 1863:     driver.get("http:/ /localhost:8080" + url);  
Line 1864:     isReady();
Line 1865:   }
Line 1866:   public abstract void isReady();    
Line 1867: }
Line 1868: You can make this PO base class as complex as you need. In more involved apps, the
Line 1869: base class is more complex and full of helper methods. For now, we have a constructor
Line 1870: that receives WebDriver (forcing all POs to have the same constructor), a visit()
Line 1871: method that can be overridden by child POs, a helper visit() method that com-
Line 1872: pletes the URL with the localhost URL, and an abstract isReady() method that forces
Line 1873: all POs to implement this functionality.
Line 1874:  We now have enough POs to model our first journey. The following listing shows a
Line 1875: JUnit test.
Line 1876: public class FindOwnersFlowTest {
Line 1877:   protected static WebDriver driver = new SafariDriver();   
Line 1878:   private FindOwnersPage page = new FindOwnersPage(driver);   
Line 1879:   @AfterAll
Line 1880:   static void close() {   
Line 1881:     driver.close();
Line 1882:   }
Line 1883:   @Test
Line 1884:   void findOwnersBasedOnTheirLastNames() {
Line 1885:     AddOwnerInfo owner1 = new AddOwnerInfo(
Line 1886:       ➥ "John", "Doe", "some address", "some city", "11111");   
Line 1887:     AddOwnerInfo owner2 = new AddOwnerInfo(
Line 1888:       ➥ "Jane", "Doe", "some address", "some city", "11111");
Line 1889:     AddOwnerInfo owner3 = new AddOwnerInfo(
Line 1890:       ➥ "Sally", "Smith", "some address", "some city", "11111");
Line 1891:     addOwners(owner1, owner2, owner3);
Line 1892:     page.visit();   
Line 1893:     ListOfOwnersPage listPage = page.findOwners("Doe");  
Line 1894:     List<OwnerInfo> all = listPage.all();
Line 1895:     assertThat(all).hasSize(2).
Line 1896:         containsExactlyInAnyOrder(
Line 1897:         owner1.toOwnerInfo(), owner2.toOwnerInfo());  
Line 1898:   }
Line 1899: Listing 9.30
Line 1900: Our first journey: find owners
Line 1901: Provides a helper 
Line 1902: method for the base 
Line 1903: classes to help them 
Line 1904: visit the page
Line 1905: The hard-coded URL can come 
Line 1906: from a configuration file.
Line 1907: All POs are forced to implement an isReady 
Line 1908: method. Making methods abstract is a nice 
Line 1909: way to force all POs to implement their 
Line 1910: minimum required behavior.
Line 1911: Creates a concrete WebDriver, the SafariDriver.
Line 1912: Later, we will make this more flexible so our
Line 1913: tests can run in multiple browsers.
Line 1914: Creates the 
Line 1915: FindOwners PO, 
Line 1916: where the test 
Line 1917: should start
Line 1918: When the test suite is done, we 
Line 1919: close the Selenium driver. This 
Line 1920: method is also a good candidate 
Line 1921: to move to a base class.
Line 1922: Creates a bunch of owners to
Line 1923: be added. We need owners
Line 1924: before testing the listing page.
Line 1925: Visits the Find 
Line 1926: Owners page
Line 1927: Looks for all 
Line 1928: owners with Doe 
Line 1929: as their surname
Line 1930: Asserts that we find 
Line 1931: John and Jane from 
Line 1932: the Doe family
Line 1933: 
Line 1934: --- 페이지 278 ---
Line 1935: 250
Line 1936: CHAPTER 9
Line 1937: Writing larger tests
Line 1938:   private void addOwners(AddOwnerInfo... owners) {   
Line 1939:     AddOwnerPage addOwnerPage = new AddOwnerPage(driver);
Line 1940:     for (AddOwnerInfo owner : owners) {
Line 1941:       addOwnerPage.visit();
Line 1942:       addOwnerPage.add(owner);
Line 1943:     }
Line 1944:   }
Line 1945: }
Line 1946: Let’s walk through this code:
Line 1947: 1
Line 1948: At the top of the class, we create a static instance of SafariDriver, which we
Line 1949: enclose in the @AfterAll method. To save some time (opening and closing the
Line 1950: browser for every test), we only need one instance of WebDriver for all the tests
Line 1951: in this class. For now, this means our test has the Safari browser hard-coded.
Line 1952: Later we will discuss how to make it more flexible so you can run your test suite
Line 1953: in multiple browsers.
Line 1954: 2
Line 1955: The findOwnersBasedOnTheirLastNames() method contains our journey. We
Line 1956: create two fake AddOwnerInfos: two owners that will be added to the applica-
Line 1957: tion. For each owner, we visit the Add Owner page, fill in the information, and
Line 1958: save. (I created an addOwners() private helper method to increase the readabil-
Line 1959: ity of the main test method.)
Line 1960: 3
Line 1961: We visit the Owners page and get all the owners in the list. We expect both
Line 1962: newly added owners to be there, so we assert that the list contains two items and
Line 1963: they are the two owners we created.
Line 1964: 4
Line 1965: AddOwnerInfo, the data structure used by AddOwnerPage, is different from Owner-
Line 1966: Info, the data structure returned by the ListOfOwnersPage page. In one, a
Line 1967: name is the first name and last name together, and in the other, the first name
Line 1968: and last name are separate. We could use a single data structure for both or
Line 1969: design them separately. I chose to design them separately, so I needed to con-
Line 1970: vert from one to another. So, I implemented toOwnerInfo() in the AddOwner-
Line 1971: Info class. It is a simple method, as you see in the next listing.
Line 1972: public OwnerInfo toOwnerInfo() {
Line 1973:   return new OwnerInfo(firstName + " " + lastName, address, city, telephone, "");
Line 1974: }
Line 1975: Now, when we run the test, it looks almost like magic: the browser opens, the names of
Line 1976: the owners are typed in the page, buttons are clicked, pages change, the browser
Line 1977: closes, and JUnit shows us that the test passed. We are finished with our first web Sele-
Line 1978: nium test.
Line 1979: NOTE
Line 1980: A good exercise for you is to write tests for other application journeys.
Line 1981: This will require the development of more POs!
Line 1982: Listing 9.31
Line 1983: toOwnerInfo converter method
Line 1984: The addOwners 
Line 1985: helper method 
Line 1986: adds an owner 
Line 1987: via the Add 
Line 1988: Owner page.
Line 1989: 
Line 1990: --- 페이지 279 ---
Line 1991: 251
Line 1992: System tests
Line 1993: If you run the test again, it will fail. The list of owners will return four people instead
Line 1994: of two, as the test expects—we are running our entire web application, and data is per-
Line 1995: sisted in the database. We need to make sure we can reset the web application when-
Line 1996: ever we run a test, and we discuss that in the next section. 
Line 1997: 9.3.3
Line 1998: Patterns and best practices
Line 1999: You probably noticed that the amount of code required to get our first system test
Line 2000: working was much greater than in previous chapters. In this section, I introduce some
Line 2001: patterns and best practices that will help you write maintainable web tests. These pat-
Line 2002: terns come from my own experience after writing many such tests. Together with
Line 2003: Guerra and Gerosa, I proposed some of these patterns at the PLoP conference in
Line 2004: 2014.
Line 2005: PROVIDE A WAY TO SET THE SYSTEM TO THE STATE THAT THE WEB TEST REQUIRES
Line 2006: To ensure that the Find Owners journey worked properly, we needed some owners in
Line 2007: the database. We added them by repeatedly navigating to the Add Owner page, filling
Line 2008: in the form, and saving it. This strategy works fine in simple cases. However, imagine a
Line 2009: more complicated scenario where your test requires 10 different entities in the data-
Line 2010: base. Visiting 10 different web pages in a specific order is too much work (and also
Line 2011: slow, since the test would take a considerable amount of time to visit all the pages).
Line 2012:  In such cases, I suggest creating all the required data before running the test. But
Line 2013: how do you do that if the web application runs standalone and has its own database?
Line 2014: You can provide web services (say, REST web services) that are easily accessible by the
Line 2015: test. This way, whenever you need some data in the application, you can get it through
Line 2016: simple requests. Imagine that instead of visiting the pages, we call the API. From the
Line 2017: test side, we implement classes that abstract away all the complexity of calling a
Line 2018: remote web service. The following listing shows how the previous test would look if it
Line 2019: consumed a web service.
Line 2020: @Test
Line 2021: void findOwnersBasedOnTheirLastNames() {
Line 2022:   AddOwnerInfo owner1 = new AddOwnerInfo(
Line 2023:     ➥ "John", "Doe", "some address", "some city", "11111");
Line 2024:   AddOwnerInfo owner2 = new AddOwnerInfo(
Line 2025:     ➥ "Jane", "Doe", "some address", "some city", "11111");
Line 2026:   AddOwnerInfo owner3 = new AddOwnerInfo(
Line 2027:     ➥ "Sally", "Smith", "some address", "some city", "11111");
Line 2028:   OwnersAPI api = new OwnersAPI();  
Line 2029:   api.add(owner1);
Line 2030:   api.add(owner2);
Line 2031:   api.add(owner3);
Line 2032:   page.visit();
Line 2033:   ListOfOwnersPage listPage = page.findOwners("Doe");
Line 2034:   List<OwnerInfo> all = listPage.all();
Line 2035: Listing 9.32
Line 2036: Our test if we had a web service to add owners
Line 2037: Calls the API. We no longer need to visit 
Line 2038: the Add Owner page. The OwnersAPI 
Line 2039: class hides the complexity of calling 
Line 2040: a web service.
Line 2041: 
Line 2042: --- 페이지 280 ---
Line 2043: 252
Line 2044: CHAPTER 9
Line 2045: Writing larger tests
Line 2046:   assertThat(all).hasSize(2).
Line 2047:       containsExactlyInAnyOrder(owner1.toOwnerInfo(), owner2.toOwnerInfo());
Line 2048: }
Line 2049: Creating simple REST web services is easy today, given the full support of the web
Line 2050: frameworks. In Spring MVC (or Ruby, or Django, or Asp.Net Core), you can write one
Line 2051: in a couple of lines. The same thing happens from the client side. Calling a REST web
Line 2052: service is simple, and you don’t have to write much code.
Line 2053:  You may be thinking of security issues. What if you do not want the web services in
Line 2054: production? If they are only for testing purposes, your software should hide the API
Line 2055: when in production and allow the API only in the testing environment.
Line 2056:  Moreover, do not be afraid to write different functionalities for these APIs, if doing
Line 2057: so makes the testing process easier. If your web page needs a combination of Products,
Line 2058: Invoices, Baskets, and Items, perhaps you can devise a web service solely to help the
Line 2059: test build up complex data. 
Line 2060: MAKE SURE EACH TEST ALWAYS RUNS IN A CLEAN ENVIRONMENT
Line 2061: Similar to what we did earlier when testing SQL queries, we must make sure our tests
Line 2062: always run in a clean version of the web application. Otherwise, the test may fail for
Line 2063: reasons other than a bug. This means databases (and any other dependencies) must
Line 2064: only contain the bare minimum amount of data for the test to start.
Line 2065:  We can reset the web application the same way we provide data to it: via web ser-
Line 2066: vices. The application could provide an easy backdoor that resets it. It goes without
Line 2067: saying that such a web service should never be deployed in production.
Line 2068:  Resetting the web application often means resetting the database. You can imple-
Line 2069: ment that in many different ways, such as truncating all the tables or dropping and re-
Line 2070: creating them.
Line 2071: WARNING
Line 2072: Be very careful. The reset backdoor is nice for tests, but if it is
Line 2073: deployed into production, chaos may result. If you use this solution, make
Line 2074: sure it is only available in the test environment!
Line 2075: GIVE MEANINGFUL NAMES TO YOUR HTML ELEMENTS
Line 2076: Locating elements is a vital part of a web test, and we do that by, for example,
Line 2077: searching for their name, class, tag, or XPath. In one of our examples, we first
Line 2078: searched for the form the element was in and then found the element by its tag. But
Line 2079: user interfaces change frequently during the life of a website. That is why web test
Line 2080: suites are often highly unstable. We do not want a change in the presentation of a
Line 2081: web page (such as moving a button from the left menu to the right menu) to break
Line 2082: the test.
Line 2083:  Therefore, I suggest assigning proper (unique) names and IDs to elements that
Line 2084: will play a role in the test. Even if the element does not need an ID, giving it one will
Line 2085: simplify the test and make sure the test will not break if the presentation of the ele-
Line 2086: ment changes.
Line 2087: 
Line 2088: --- 페이지 281 ---
Line 2089: 253
Line 2090: System tests
Line 2091:  If for some reason an element has a very unstable ID (perhaps it is dynamically
Line 2092: generated), we need to create any specific property for the testing. HTML5 allows us
Line 2093: to create extra attributes on HTML tags, like the following example.
Line 2094: <input type="text"
Line 2095: id="customer_\${i}"
Line 2096: name="customer"
Line 2097: data-selenium="customer-name" />    
Line 2098: If you think this extra property may be a problem in the production environment,
Line 2099: remove it during deployment. There are many tools that manipulate HTML pages
Line 2100: before deploying them (minification is an example).
Line 2101: NOTE
Line 2102: Before applying this pattern to the project, you may want to talk to
Line 2103: your team’s frontend lead. 
Line 2104: VISIT EVERY STEP OF A JOURNEY ONLY WHEN THAT JOURNEY IS UNDER TEST
Line 2105: Unlike unit testing, building up scenarios on a system test can be complicated. We saw
Line 2106: that some journeys may require the test to navigate through many different pages
Line 2107: before getting to the page it wants to test.
Line 2108:  Imagine a specific page A that requires the test to visit pages B, C, D, E, and F
Line 2109: before it can finally get to A and test it. A test for that page is shown here.
Line 2110: @Test
Line 2111: void longest() {
Line 2112:   BPage b = new BPage();    
Line 2113:   b.action1(..);
Line 2114:   b.action2(..);
Line 2115:   CPage c = new CPage();   
Line 2116:   c.action1(..);
Line 2117:   DPage d = new DPage();   
Line 2118:   d.action1(..);
Line 2119:   d.action2(..);
Line 2120:   EPage e = new EPage();
Line 2121:   e.action1(..);
Line 2122:   FPage e = new FPage();
Line 2123:   f.action1(..);
Line 2124:   // finally!!
Line 2125:   APage a = new APage();
Line 2126:   a.action1();
Line 2127:   assertThat(a.confirmationAppears()).isTrue();
Line 2128: }
Line 2129: Listing 9.33
Line 2130: HTML element with a property that makes it easy to find
Line 2131: Listing 9.34
Line 2132: A very long test that calls many POs
Line 2133: It is easy to find the HTML element 
Line 2134: that has a data-selenium attribute 
Line 2135: with customer-name as its value.
Line 2136: Calls the 
Line 2137: first PO
Line 2138: Calls a 
Line 2139: second PO
Line 2140: Calls a third 
Line 2141: PO, and so on
Line 2142: 
Line 2143: --- 페이지 282 ---
Line 2144: 254
Line 2145: CHAPTER 9
Line 2146: Writing larger tests
Line 2147: Note how long and complex the test is. We discussed a similar problem, and our
Line 2148: solution was to provide a web service that enabled us to skip many of the page visits.
Line 2149: But if visiting all these pages is part of the journey under test, the test should visit
Line 2150: each one. If one or two of these steps are not part of the journey, you can use the
Line 2151: web services. 
Line 2152: ASSERTIONS SHOULD USE DATA THAT COMES FROM THE POS
Line 2153: In the Find Owners test, our assertions focused on checking whether all the owners
Line 2154: were on the list. In the code, the FindOwnersPage PO provided an all() method that
Line 2155: returned the owners. The test code was only responsible for the assertion. This is a
Line 2156: good practice. Whenever your tests require information from the page for the asser-
Line 2157: tion, the PO provides this information. Your JUnit test should not locate HTML ele-
Line 2158: ments by itself. However, the assertions stay in the JUnit test code. 
Line 2159: PASS IMPORTANT CONFIGURATIONS TO THE TEST SUITE
Line 2160: The example test suite has some hard-coded details, such as the local URL of the
Line 2161: application (right now, it is localhost:8080) and the browser to run the tests (currently
Line 2162: Safari). However, you may need to change these configurations dynamically. For
Line 2163: example, your continuous integration may need to run the web app on a different
Line 2164: port, or you may want to run your test suite on Chrome.
Line 2165:  There are many different ways to pass configuration to Java tests, but I usually opt
Line 2166: for the simplest approach: everything that is a configuration is provided by a method
Line 2167: in  my PageObject base class. For example, a String baseUrl() method returns the
Line 2168: base URL of the application, and a WebDriver browser() method returns the con-
Line 2169: crete instance of WebDriver. These methods then read from a configuration file or an
Line 2170: environment variable, as those are easy to pass via build scripts. 
Line 2171: RUN YOUR TESTS IN MULTIPLE BROWSERS
Line 2172: You should run your tests in multiple browsers to be sure everything works every-
Line 2173: where. But I don’t do this on my machine, because it takes too much time. Instead, my
Line 2174: continuous integration (CI) tool has a multiple-stage process that runs the web test
Line 2175: suite multiple times, each time passing a different browser. If configuring such a CI is
Line 2176: an issue, consider using a service such as SauceLabs (https://saucelabs.com), which
Line 2177: automates this process for you. 
Line 2178: 9.4
Line 2179: Final notes on larger tests
Line 2180: I close this chapter with some points I have not yet mentioned regarding larger tests.
Line 2181: 9.4.1
Line 2182: How do all the testing techniques fit?
Line 2183: In the early chapters of this book, our goal was to explore techniques that would help
Line 2184: you engineer test cases systematically. In this chapter, we discuss a more orthogonal
Line 2185: topic: how large should our tests be? I have shown you examples of larger component
Line 2186: tests, integration tests, and system tests. But regardless of the test level, engineering
Line 2187: good test cases should still be the focus.
Line 2188: 
Line 2189: --- 페이지 283 ---
Line 2190: 255
Line 2191: Final notes on larger tests
Line 2192:  When you write a larger test, use the requirement and its boundaries, the structure
Line 2193: of the code, and the properties it should uphold to engineer good test cases. The chal-
Line 2194: lenge is that an entire component has a much larger requirement and a much larger
Line 2195: code base, which means many more tests to engineer.
Line 2196:  I follow this rule of thumb: exercise everything at the unit level (you can easily
Line 2197: cover entire requirements and structures at the unit level), and exercise the most
Line 2198: important behavior in larger tests (so you have more confidence that the program will
Line 2199: work when the pieces are put together). It may help to reread about the testing pyra-
Line 2200: mid in section 1.4 in chapter 1.
Line 2201: 9.4.2
Line 2202: Perform cost/benefit analysis
Line 2203: One of the testing mantras is that a good test is cheap to write but can capture import-
Line 2204: ant bugs. Unit tests are cheap to write, so we do not have to think much about cost.
Line 2205:  Larger tests may not be cheap to write, run, or maintain. I have seen integration
Line 2206: test suites that take hours to run—and cases where developers spend hours writing a
Line 2207: single integration test.
Line 2208:  Therefore, it is fundamental to perform a simple cost/benefit analysis. Questions
Line 2209: like “How much will it cost me to write this test?” “How much will it cost to run?”
Line 2210: “What is the benefit of this test? What bugs will it catch?” and “Is this functionality
Line 2211: already covered by unit tests? If so, do I need to cover it via integration tests, too?” may
Line 2212: help you understand whether this is a fundamental test.
Line 2213:  The answer will be “yes” in many cases. The benefits outweigh the costs, so you
Line 2214: should write the test. If the cost is too high, consider simplifying your test. Can you
Line 2215: stub parts of the test without losing too much? Can you write a more focused test that
Line 2216: exercises a smaller part of the system? As always, there is no single good answer or
Line 2217: golden rule to follow. 
Line 2218: 9.4.3
Line 2219: Be careful with methods that are covered but not tested
Line 2220: Larger tests exercise more classes, methods, and behaviors together. In addition to all
Line 2221: the trade-offs discussed in this chapter, with larger tests, the chances of covering a
Line 2222: method but not testing it are much higher.
Line 2223:  Vera-Pérez and colleagues (2019) coined the term pseudo-tested methods. These
Line 2224: methods are tested, but if we replace their entire implementation with a simple
Line 2225: return null, tests still pass. And believe it or not, Vera-Pérez and colleagues show that
Line 2226: pseudo-tested methods happen in the wild, even in important open source projects.
Line 2227: This is another reason I defend both unit tests and larger tests, used together to
Line 2228: ensure that everything works. 
Line 2229: 9.4.4
Line 2230: Proper code infrastructure is key
Line 2231: Integration and system tests both require a decent infrastructure behind the scenes.
Line 2232: Without it, we may spend too much time setting up the environment or asserting that
Line 2233: behavior was as expected. My key advice here is to invest in test infrastructure. Your
Line 2234: 
Line 2235: --- 페이지 284 ---
Line 2236: 256
Line 2237: CHAPTER 9
Line 2238: Writing larger tests
Line 2239: infrastructure should help developers set up the environment, clean up the environ-
Line 2240: ment, retrieve complex data, assert complex data, and perform whatever other com-
Line 2241: plex tasks are required to write tests. 
Line 2242: 9.4.5
Line 2243: DSLs and tools for stakeholders to write tests
Line 2244: In this chapter, we wrote the system tests ourselves with lots of Java code. At this level,
Line 2245: it is also common to see more automation. Some tools, such as the Robot framework
Line 2246: (https://robotframework.org) and Cucumber (https://cucumber.io), even allow you
Line 2247: to write tests in language that is almost completely natural. These tools make a lot of
Line 2248: sense if you want others to write tests, too, such as (non-technical) stakeholders. 
Line 2249: 9.4.6
Line 2250: Testing other types of web systems
Line 2251: The higher we go in levels of testing, such as web testing, the more we start to think
Line 2252: about the frameworks and environment our application runs in. Our web application
Line 2253: is responsive; how do we test for that? If we use Angular or React, how do we test it?
Line 2254: Or, if we use a non-relational database like Mongo, how do we test it?
Line 2255:  Testing these specific technologies is far beyond the scope of this book. My sugges-
Line 2256: tion is that you visit those communities and explore their state-of-the-art tools and
Line 2257: bodies of knowledge. All the test case engineering techniques you learn in this book
Line 2258: will apply to your software, regardless of the technology.
Line 2259: SYSTEM TESTS IN SOFTWARE OTHER THAN WEB APPLICATIONS
Line 2260: I used web applications to exemplify system tests because I have a lot of experience
Line 2261: with them. But the idea of system testing can be applied to any type of software you
Line 2262: develop. If your software is a library or framework, your system tests will exercise the
Line 2263: entire library as the clients would. If your software is a mobile application, your system
Line 2264: tests will exercise the mobile app as the clients would.
Line 2265:  The best practices I discussed still apply. Engineering system tests will be harder
Line 2266: than engineering unit tests, and you may need some infrastructure code (like the POs
Line 2267: we created) to make you more productive. There are probably also specific best prac-
Line 2268: tices for your type of software—be sure to do some research. 
Line 2269: Exercises
Line 2270: 9.1
Line 2271: Which of the following recommendations should you follow to keep a web
Line 2272: application testable? Select all that apply.
Line 2273: A Use TypeScript instead of JavaScript.
Line 2274: B Make sure the HTML elements can be found easily from the tests.
Line 2275: C Make sure requests to web servers are performed asynchronously.
Line 2276: D Avoid inline JavaScript in an HTML page.
Line 2277: 9.2
Line 2278: Which of the following statements is true about end-to-end/system testing?
Line 2279: A End-to-end testing cannot be automated for web applications and there-
Line 2280: fore has to be performed manually.
Line 2281: 
Line 2282: --- 페이지 285 ---
Line 2283: 257
Line 2284: Summary
Line 2285: B In web testing, end-to-end testing is more important than unit testing.
Line 2286: C End-to-end testing can be used to verify whether the frontend and back-
Line 2287: end work together well.
Line 2288: D End-to-end tests are, like unit tests, not very realistic.
Line 2289: 9.3
Line 2290: Which of the following is true about page objects?
Line 2291: A POs abstract the HTML page to facilitate the engineering of end-to-end
Line 2292: tests.
Line 2293: B POs cannot be used in highly complex web applications.
Line 2294: C By introducing a PO, we no longer need libraries like Selenium.
Line 2295: D POs usually make the test code more complex.
Line 2296: 9.4
Line 2297: Which of the following are important recommendations for developers who are
Line 2298: engineering integration and system test suites? Choose all that apply.
Line 2299: A What can be tested via unit testing should be tested via unit testing. Use
Line 2300: integration and system tests for bugs that can only be caught at that level.
Line 2301: B It is fundamental for developers to have a solid infrastructure to write
Line 2302: such tests, as otherwise, they would feel unproductive.
Line 2303: C If something is already covered via unit testing, you should not cover it
Line 2304: (again) via integration testing.
Line 2305: D Too many integration tests may mean your application is badly designed.
Line 2306: Focus on unit tests.
Line 2307: 9.5
Line 2308: Which of the following can cause web tests to be flaky (that is, sometimes pass,
Line 2309: sometimes fail)? Choose all that apply.
Line 2310: A AJAX requests that take longer than expected
Line 2311: B The use of LESS and SASS instead of pure CSS
Line 2312: C The database of the web app under test is not being cleaned up after every
Line 2313: test run
Line 2314: D Some components of the web app were unavailable at the time
Line 2315: Summary
Line 2316: Developers benefit from writing larger tests, ranging from testing entire compo-
Line 2317: nents together, to integrating with external parties, to entire systems.
Line 2318: Engineering larger tests is more challenging than writing unit tests, because the
Line 2319: component under test is probably much bigger and more complex than a sin-
Line 2320: gle unit of the system.
Line 2321: All the test case engineering techniques we have discussed—specification-based
Line 2322: testing, boundary testing, structural testing, and property-based testing—apply
Line 2323: to larger tests.
Line 2324: Investing in a good test infrastructure for large tests is a requirement. Without
Line 2325: it, you will spend too much time writing a single test case.