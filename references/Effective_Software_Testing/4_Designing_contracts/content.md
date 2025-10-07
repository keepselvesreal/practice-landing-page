Line 1: 
Line 2: --- 페이지 125 ---
Line 3: 97
Line 4: Designing contracts
Line 5: Imagine a piece of software that handles a very complex financial process. For that
Line 6: big routine to happen, the software system chains calls to several subroutines (or
Line 7: classes) in a complex flow of information: that is, the results of one class are passed
Line 8: to the next class, whose results are again passed to the next class, and so on. As
Line 9: usual, the data comes from different sources, such as databases, external web ser-
Line 10: vices, and users. At some point in the routine, the class TaxCalculator (which han-
Line 11: dles calculating a specific tax) is called. From the requirements of this class, the
Line 12: calculation only makes sense for positive numbers.
Line 13:  We need to think about how we want to model such a restriction. I see three
Line 14: options when facing such a restriction:
Line 15: Ensure that classes never call other classes with invalid inputs. In our exam-
Line 16: ple, any other classes called TaxCalculator will ensure that they will never
Line 17: pass a negative number. While this simplifies the code of the class under
Line 18: This chapter covers
Line 19: Designing pre-conditions, post-conditions, and 
Line 20: invariants
Line 21: Understanding the differences between contracts 
Line 22: and validation
Line 23: 
Line 24: --- 페이지 126 ---
Line 25: 98
Line 26: CHAPTER 4
Line 27: Designing contracts
Line 28: development, since it does not need to deal with the special cases, it adds com-
Line 29: plexity to the caller classes that need to be sure they never make a bad call.
Line 30: Program in a more defensive manner, ensuring that if an invalid input happens,
Line 31: the system halts and returns an error message to the user. This adds a little com-
Line 32: plexity to every class in the system, as they all have to know how to handle
Line 33: invalid inputs. At the same time, it makes the system more resilient. However,
Line 34: coding defensively in an ad hoc manner is not productive. You may end up add-
Line 35: ing unnecessary code, such as restrictions that were already checked.
Line 36: My favorite approach, and the goal of this chapter, is to define clear contracts for
Line 37: each class we develop. These contracts clearly establish what the class requires as
Line 38: pre-conditions, what the class provides as post-conditions, and what invariants
Line 39: always hold for the class. This is a major modeling activity for which the design-by-
Line 40: contract idea will inspire us (originally proposed by Bertrand Meyer).
Line 41: Such contract decisions happen while the developer is implementing the functional-
Line 42: ity. That is why design-by-contract appears on the “testing to guide development” side
Line 43: of the development flow I propose (see figure 1.4).
Line 44: 4.1
Line 45: Pre-conditions and post-conditions
Line 46: Going back to the tax calculation example, we need to reflect on pre-conditions that the
Line 47: method needs to function properly, as well as its post-conditions: what the method guar-
Line 48: antees as outcomes. We already mentioned a pre-condition: the method does not
Line 49: accept negative numbers. A possible post-condition of this method is that it also does
Line 50: not return negative numbers.
Line 51:  Once the method’s pre- and post-conditions are established, it is time to add
Line 52: them to the source code. Doing so can be as simple as an if instruction, as shown in
Line 53: the following listing.
Line 54: public class TaxCalculator {
Line 55:   public double calculateTax(double value) {
Line 56:     if(value < 0) { 
Line 57:       throw new RuntimeException("Value cannot be negative.");
Line 58:     }
Line 59:     double taxValue = 0;
Line 60:     // some complex business rule here...
Line 61:     // final value goes to 'taxValue'
Line 62:     if(taxValue < 0) { 
Line 63:       throw new RuntimeException("Calculated tax value
Line 64:       ➥ cannot be negative.");
Line 65:     }
Line 66: Listing 4.1
Line 67: TaxCalculator with pre- and post-conditions
Line 68: The pre-condition: a 
Line 69: simple if ensuring that 
Line 70: no invalid values pass
Line 71: The post-condition is also 
Line 72: implemented as a simple if. If 
Line 73: something goes wrong, we throw an 
Line 74: exception, alerting the consumer that 
Line 75: the post-condition does not hold.
Line 76: 
Line 77: --- 페이지 127 ---
Line 78: 99
Line 79: Pre-conditions and post-conditions
Line 80:     return taxValue;
Line 81:   }
Line 82: }
Line 83: NOTE
Line 84: You may be wondering what value, the input parameter of the
Line 85: calculateTax method, represents. Also, how is the tax rate set? In real life, the
Line 86: requirements and implementation of a tax calculator would be much more
Line 87: complex—this simple code lets you focus on the technique. Bear with me!
Line 88: Note that the pre- and post-conditions ensure different things. Pre-conditions (in this
Line 89: case, a single pre-condition) ensure that the input values received by a method adhere
Line 90: to what it requires. Post-conditions ensure that the method returns what it promises to
Line 91: other methods.
Line 92:  You may be wondering, “How can I have a value that breaks the post-condition if I
Line 93: am coding the implementation of this method?” In this example, you hope that your
Line 94: implementation will never return a negative number. But in very complex implemen-
Line 95: tations, a bug may slip in! If bugs did not exist, there would be no reason for this
Line 96: book. The post-condition check ensures that if there is a bug in the implementation,
Line 97: the method will throw an exception instead of returning an invalid value. An excep-
Line 98: tion will make your program halt—and halting is often much better than continuing
Line 99: with an incorrect value.
Line 100:  Making your pre- and post-conditions clear in the documentation is also funda-
Line 101: mental and very much recommended. Let’s do that in the next listing.
Line 102: /**
Line 103:  * Calculates the tax according to (some
Line 104:  * explanation here...)
Line 105:  *
Line 106:  * @param value the base value for tax calculation. Value has
Line 107:  *              to be a positive number.
Line 108:  * @return the calculated tax. The tax is always a positive number.
Line 109:  */
Line 110: public double calculateTax(double value) { ... }
Line 111: 4.1.1
Line 112: The assert keyword
Line 113: The Java language offers the keyword assert, which is a native way of writing asser-
Line 114: tions. In the previous example, instead of throwing an exception, we could write
Line 115: assert value >= 0 : "Value cannot be negative.". If value is not greater than or
Line 116: equal to 0, the Java Virtual Machine (JVM) will throw an AssertionError. In the fol-
Line 117: lowing listing, I show a version of the TaxCalculator using asserts.
Line 118: public class TaxCalculator {
Line 119:   public double calculateTax(double value) {
Line 120: Listing 4.2
Line 121: Javadoc of the calculateTax method describing its contract
Line 122: Listing 4.3
Line 123: TaxCalculator with pre- and post-conditions implemented via asserts
Line 124: 
Line 125: --- 페이지 128 ---
Line 126: 100
Line 127: CHAPTER 4
Line 128: Designing contracts
Line 129:     assert value >= 0 : "Value cannot be negative"; 
Line 130:     double taxValue = 0;
Line 131:     // some complex business rule here...
Line 132:     // final value goes to 'taxValue'
Line 133:     assert taxValue >= 0 : "Calculated tax value
Line 134:     ➥ cannot be negative."; 
Line 135:     return taxValue;
Line 136:   }
Line 137: }
Line 138: Deciding whether to use assert instructions or simple if statements that throw
Line 139: exceptions is something to discuss with your team members. I’ll give you my opinion
Line 140: about it later in section 4.5.3.
Line 141:  The assert instruction can be disabled via a parameter to the JVM, so it does not
Line 142: have to be executed at all times. If you disable it in production, for example, the pre-
Line 143: conditions will not be checked while running the system. If you do not have full con-
Line 144: trol of your production environment, you may want to opt for exceptions so you can
Line 145: be sure your pre-conditions will be checked.
Line 146:  An argument against the use of asserts is that they always throw AssertionError,
Line 147: which is a generic error. Sometimes you may want to throw a more specific exception
Line 148: that the caller can handle. For simplicity, I make use of assert in the remainder of
Line 149: this chapter.
Line 150:  Later in this chapter, we differentiate between pre-conditions and validations. This
Line 151: may also be taken into account when deciding between asserts and exceptions. 
Line 152: 4.1.2
Line 153: Strong and weak pre- and post-conditions
Line 154: When defining pre- and post-conditions, an important decision is how weak or strong
Line 155: you want them to be. In the previous example, we handle the pre-condition very
Line 156: strongly: if a negative value comes in, it violates the pre-condition of the method, so
Line 157: we halt the program.
Line 158:  One way to avoid halting the program due to negative numbers would be to
Line 159: weaken the pre-condition. In other words, instead of accepting only values that are
Line 160: greater than zero, the method could accept any value, positive or negative. We could
Line 161: do this by removing the if statement, as shown in the following listing (the developer
Line 162: would have to find a way to take negative numbers into account and handle them).
Line 163: public double calculateTax(double value) {
Line 164:   
Line 165:   // method continues ...
Line 166: }
Line 167: Listing 4.4
Line 168: TaxCalculator with a weaker pre-condition
Line 169: The same pre-condition, 
Line 170: now as an assert 
Line 171: statement
Line 172: The same post-condition, 
Line 173: now as an assert 
Line 174: statement
Line 175: No pre-conditions 
Line 176: check; any value 
Line 177: is valid.
Line 178: 
Line 179: --- 페이지 129 ---
Line 180: 101
Line 181: Pre-conditions and post-conditions
Line 182: Weaker pre-conditions make it easier for other classes to invoke the method. After all,
Line 183: regardless of the value you pass to calculateTax, the program will return something.
Line 184: This is in contrast to the previous version, where a negative number throws an error.
Line 185:  There is no single answer for whether to use weaker or stronger pre-conditions. It
Line 186: depends on the type of system you are developing as well as what you expect from the
Line 187: consumers of the class you are modeling. I prefer stronger conditions, as I believe they
Line 188: reduce the range of mistakes that may happen in the code. However, this means I spend
Line 189: more time encoding these conditions as assertions, so my code becomes more complex.
Line 190: In some cases, you cannot weaken the pre-condition. For the tax calculation, there is
Line 191: no way to accept negative values, and the pre-condition should be strong. Pragmati-
Line 192: cally speaking, another way of handling such a case is to return an error value. For
Line 193: example, if a negative number comes in, the program can return 0 instead of halting,
Line 194: as in the following listing.
Line 195: public double calculateTax(double value) {
Line 196:   // pre-condition check
Line 197:   if(value < 0) { 
Line 198:     return 0;
Line 199:   }
Line 200:   // method continues ...
Line 201: }
Line 202: While this approach simplifies the clients’ lives, they now have to be aware that if they
Line 203: receive a 0, it might be because of invalid input. Perhaps the method could return –1
Line 204: to differentiate from zero taxes. Deciding between a weaker pre-condition or an error
Line 205: value is another decision to make after considering all the possibilities.
Line 206:  For those that know the original theory of design-by-contracts: we do not weaken
Line 207: the pre-condition here to make it easier for clients to handle the outcomes of the
Line 208: method. We decided to return an error code instead of throwing an exception. In the
Line 209: remainder of this chapter, you see that my perspective on contracts is more pragmatic
Line 210: than that in the original design-by-contract paper by Meyer in 1992. What matters to
Line 211: me is reflecting on what classes and methods can and cannot handle and what they
Line 212: should do in case a violation happens. 
Line 213: Can you apply the same reasoning to post-conditions?
Line 214: You may find a reason to return a value instead of throwing an exception. To be hon-
Line 215: est, I cannot recall a single time I’ve done that. In the TaxCalculator example, a
Line 216: negative number would mean there was a bug in the implementation, and you prob-
Line 217: ably do not want someone to pay zero taxes.
Line 218: Listing 4.5
Line 219: TaxCalculator returning an error code instead of an exception
Line 220: If the pre-condition does not hold, 
Line 221: the method returns 0. The client of 
Line 222: this method does not need to worry 
Line 223: about exceptions.
Line 224: 
Line 225: --- 페이지 130 ---
Line 226: 102
Line 227: CHAPTER 4
Line 228: Designing contracts
Line 229: 4.2
Line 230: Invariants
Line 231: We have seen that pre-conditions should hold before a method’s execution, and post-
Line 232: conditions should hold after a method’s execution. Now we move on to conditions
Line 233: that must always hold before and after a method’s execution. These conditions are
Line 234: called invariants. An invariant is thus a condition that holds throughout the entire life-
Line 235: time of an object or a data structure.
Line 236:  Imagine a Basket class that stores the products the user is buying from an online
Line 237: shop. The class offers methods such as add(Product p, int quantity), which adds a
Line 238: product p a quantity number of times, and remove(Product p), which removes the
Line 239: product completely from the cart. Here is a skeleton of the class.
Line 240: public class Basket {
Line 241:   private BigDecimal totalValue = BigDecimal.ZERO; 
Line 242:   private Map<Product, Integer> basket = new HashMap<>();
Line 243:   public void add(Product product, int qtyToAdd) { 
Line 244:     // add the product
Line 245:     // update the total value
Line 246:   }
Line 247:   public void remove(Product product) { 
Line 248:     // remove the product from the basket
Line 249:     // update the total value
Line 250:   }
Line 251: }
Line 252: Before we talk about invariants, let’s focus on the method’s pre- and post-conditions.
Line 253: For the add() method, we can ensure that the product is not null (you cannot add
Line 254: a null product to the cart) and that the quantity is greater than 0 (you cannot buy a
Line 255: product 0 or fewer times). In addition, a clear post-condition is that the product is
Line 256: now in the basket. Listing 4.7 shows the implementation. Note that I am using Java’s
Line 257: assert method to express the pre-condition, which means I must have assertions
Line 258: enabled in my JVM when I run the system. You could also use a simple if statement,
Line 259: as I showed earlier.
Line 260: public void add(Product product, int qtyToAdd) {
Line 261:   assert product != null : "Product is required"; 
Line 262:   assert qtyToAdd > 0 : "Quantity has to be greater than zero"; 
Line 263:   // ...
Line 264:   // add the product in the basket
Line 265:   // update the total value
Line 266:   // ...
Line 267: Listing 4.6
Line 268: The Basket class
Line 269: Listing 4.7
Line 270: Basket's add method with its pre-conditions
Line 271: We use BigDecimal 
Line 272: instead of double to avoid 
Line 273: rounding issues in Java.
Line 274: Adds the product to the 
Line 275: cart and updates the 
Line 276: total value of the cart
Line 277: Removes a product from 
Line 278: the cart and updates its 
Line 279: total value
Line 280: Pre-condition ensuring 
Line 281: that product is not null
Line 282: Pre-condition ensuring
Line 283: that qtyToAdd is
Line 284: greater than 0
Line 285: 
Line 286: --- 페이지 131 ---
Line 287: 103
Line 288: Invariants
Line 289:   assert basket.containsKey(product) :
Line 290:    "Product was not inserted in the basket"; 
Line 291: }
Line 292: You could model other post-conditions here, such as “the new total value should be
Line 293: greater than the previous total value.” Java does not provide an easy way to do that, so
Line 294: we need extra code to keep the old total value, which we use in the post-condition
Line 295: check (see listing 4.8). Interestingly, in languages like Eiffel, doing so would not
Line 296: require an extra variable! Those languages provide old and new values of variables to
Line 297: facilitate the post-condition check.
Line 298: public void add(Product product, int qtyToAdd) {
Line 299:   assert product != null : "Product is required";
Line 300:   assert qtyToAdd > 0 : "Quantity has to be greater than zero";
Line 301:   BigDecimal oldTotalValue = totalValue; 
Line 302:   // add the product in the basket
Line 303:   // update the total value
Line 304:   assert basket.containsKey(product) :
Line 305:     "Product was not inserted in the basket";
Line 306:   assert totalValue.compareTo(oldTotalValue) == 1 :
Line 307:     "Total value should be greater than
Line 308:     ➥ previous total value"; 
Line 309: }
Line 310: NOTE
Line 311: We use the BigDecimal class here instead of a simple double. Big-
Line 312: Decimals are recommended whenever you want to avoid rounding issues that
Line 313: may happen when you use doubles. Check your programming language for
Line 314: how to do that. BigDecimal gives us precision, but it is verbose. In listing 4.8,
Line 315: for example, we have to use the compareTo method to compare two Big-
Line 316: Decimals, which is more complicated than a > b. Another trick is to represent
Line 317: money in cents and use integer or long as the types, but that is beyond the
Line 318: scope of this book.
Line 319: Now for the pre-conditions of the remove() method. The product should not be null;
Line 320: moreover, the product to be removed needs to be in the basket. If the product is not
Line 321: in the basket, how can you remove it? As a post-condition, we can ensure that, after
Line 322: the removal, the product is no longer in the basket. See the implementation of both
Line 323: pre- and post-conditions in the following listing.
Line 324: public void remove(Product product) {
Line 325:   assert product != null : "product can't be null";                   
Line 326:   assert basket.containsKey(product) : "Product must already be in the
Line 327:   ➥ basket";                                                         
Line 328: Listing 4.8
Line 329: Another post-condition for Basket's add method
Line 330: Listing 4.9
Line 331: Pre- and post-conditions for the remove method
Line 332: Post-condition ensuring 
Line 333: that the product was 
Line 334: added to the cart
Line 335: For the post-condition to 
Line 336: happen, we need to save 
Line 337: the old total value.
Line 338: The post-condition ensures 
Line 339: that the total value is 
Line 340: greater than before.
Line 341: Pre-conditions: the product cannot be
Line 342: null, and it must exist in the basket.
Line 343: 
Line 344: --- 페이지 132 ---
Line 345: 104
Line 346: CHAPTER 4
Line 347: Designing contracts
Line 348:   // ...
Line 349:   // remove the product from the basket
Line 350:   // update the total value
Line 351:   // ...
Line 352:   assert !basket.containsKey(product) : "Product is still in the  
Line 353:   ➥ basket";                                                     
Line 354: }
Line 355: We are finished with the pre- and post-conditions. It is time to model the class invari-
Line 356: ants. Regardless of products being added to and removed from the basket, the total
Line 357: value of the basket should never be negative. This is not a pre-condition nor a post-
Line 358: condition: this is an invariant, and the class is responsible for maintaining it. For the
Line 359: implementation, you can use assertions or ifs or whatever your programming lan-
Line 360: guage offers. Whenever a method that manipulates the totalValue field is called, we
Line 361: ensure that totalValue is still a positive number at the end of the method. See the
Line 362: implementation of the invariants in the following listing.
Line 363: public class Basket {
Line 364:   private BigDecimal totalValue = BigDecimal.ZERO;
Line 365:   private Map<Product, Integer> basket = new HashMap<>();
Line 366:   public void add(Product product, int qtyToAdd) {
Line 367:     assert product != null : "Product is required";
Line 368:     assert qtyToAdd > 0 : "Quantity has to be greater than zero";
Line 369:     BigDecimal oldTotalValue = totalValue;
Line 370:     // add the product in the basket
Line 371:     // update the total value
Line 372:     assert basket.containsKey(product) : "Product was not inserted in
Line 373:     ➥ the basket";
Line 374:     assert totalValue.compareTo(oldTotalValue) == 1 : "Total value should
Line 375:     ➥ be greater than previous total value";
Line 376:     assert totalValue.compareTo(BigDecimal.ZERO) >= 0 :
Line 377:       "Total value can't be negative." 
Line 378:   }
Line 379:   public void remove(Product product) {
Line 380:     assert product != null : "product can't be null";
Line 381:     assert basket.containsKey(product) : "Product must already be in the 
Line 382: basket";
Line 383:     ➥ 
Line 384:     // remove the product from the basket
Line 385:     // update the total value
Line 386:     assert !basket.containsKey(product) : "Product is still in the basket";
Line 387:     assert totalValue.compareTo(BigDecimal.ZERO) >= 0 : 
Line 388:       "Total value can't be negative."
Line 389:   }
Line 390: }
Line 391: Listing 4.10
Line 392: Invariants of the Basket class
Line 393: Post-condition: the product
Line 394: is no longer in the basket.
Line 395: The invariant ensures that the total 
Line 396: value is greater than or equal to 0.
Line 397: The same invariant 
Line 398: check for the remove
Line 399: 
Line 400: --- 페이지 133 ---
Line 401: 105
Line 402: Changing contracts, and the Liskov substitution principle
Line 403: Because the invariant checking may happen at the end of all the methods of a class,
Line 404: you may want to reduce duplication and create a method for such checks, such as the
Line 405: invariant() method in listing 4.11. We call invariant() at the end of every public
Line 406: method: after each method does its business (and changes the object’s state), we want
Line 407: to ensure that the invariants hold.
Line 408: public class Basket {
Line 409:   public void add(Product product, int qtyToAdd) {
Line 410:     // ... method here ...
Line 411:     assert invariant() : "Invariant does not hold";
Line 412:   }
Line 413:   public void remove(Product product) {
Line 414:     // ... method here ...
Line 415:     assert invariant() : "Invariant does not hold";
Line 416:   }
Line 417:   private boolean invariant() {
Line 418:     return totalValue.compareTo(BigDecimal.ZERO) >= 0;
Line 419:   }
Line 420: }
Line 421: Note that invariants may not hold, say, in the middle of the method execution. The
Line 422: method may break the invariants for a second, as part of its algorithm. However, the
Line 423: method needs to ensure that, in the end, the invariants hold.
Line 424: NOTE
Line 425: You might be curious about the concrete implementation of the Bas-
Line 426: ket class and how we would test it. We cannot test all possible combinations of
Line 427: method calls (adds and removes, in any order). How would you tackle this?
Line 428: We get to property-based testing in chapter 5. 
Line 429: 4.3
Line 430: Changing contracts, and the Liskov substitution 
Line 431: principle
Line 432: What happens if we change the contract of a class or method? Suppose the calculate-
Line 433: Tax method we discussed earlier needs new pre-conditions. Instead of “value
Line 434: should be greater than or equal to 0,” they are changed to “value should be greater
Line 435: than or equal to 100.” What impact would this change have on the system and our
Line 436: test suites? Or suppose the add method from the previous section, which does not
Line 437: accept null as product, now accepts it. What is the impact of this decision? Do these
Line 438: two changes impact the system in the same way, or does one change have less impact
Line 439: than the other?
Line 440:  In an ideal world, we would not change the contract of a class or method after we
Line 441: define it. In the real world, we are sometimes forced to do so. While there may not be
Line 442: anything we can do to prevent the change, we can understand its impact. If you do not
Line 443: Listing 4.11
Line 444: invariant() method for the invariant check
Line 445: 
Line 446: --- 페이지 134 ---
Line 447: 106
Line 448: CHAPTER 4
Line 449: Designing contracts
Line 450: understand the impact of the change, your system may behave unexpectedly—and
Line 451: this is how contract changes are related to testing and quality.
Line 452:  The easiest way to understand the impact of a change is not to look at the change
Line 453: itself or at the class in which the change is happening, but at all the other classes (or
Line 454: dependencies) that may use the changing class. Figure 4.1 shows the calculateTax()
Line 455: method and  three other (imaginary) classes that use it. When these classes were cre-
Line 456: ated, they knew the pre-conditions of the calculateTax() at that point: “value has to
Line 457: be greater than or equal to 0.” They knew calculateTax() would throw an exception
Line 458: if they passed a negative number. So, these client classes currently ensure that they
Line 459: never pass a negative number to calculateTax().
Line 460: Notice that m1() passes 50 as value, m2() passes 150, and m3 passes a value from a
Line 461: database (after ensuring that the value is greater than 0). Now, suppose we change the
Line 462: pre-condition to value > 100. What will happen to these three dependencies? Nothing
Line 463: will happen to m2(): by pure luck, the new pre-condition holds for the value of 150.
Line 464: However, we cannot say the same for the other two methods: m1() will crash, and m3()
Line 465: will have erratic behavior, as some values from the database may be greater than 100,
Line 466: while others may be smaller than 100. What do we learn here? If we change our pre-
Line 467: conditions to something stronger and more restrictive, such as accepting a smaller set
Line 468: of values (100 to infinity instead of 0 to infinity), we may have a problem with classes
Line 469: that depend on the previously defined contract.
Line 470:  Now, suppose calculateTax() changes its pre-condition to accept negative num-
Line 471: bers as inputs. In this case, the three existing dependencies would not break. The new
Line 472: pre-condition is more relaxed than the previous one: it accepts a larger set of inputs.
Line 473: What do we learn? If we change our pre-conditions to something weaker and less
Line 474: restrictive, we do not break the contracts with the clients of the changing class.
Line 475: Ta
Line 476: tor
Line 477: xCalcula
Line 478: calculateTax(value),
Line 479: value >= 0
Line 480: The
Line 481: method is used by many other classes in the
Line 482: calculateTax()
Line 483: system. The
Line 484: class doesn’t know about them.
Line 485: TaxCalculator
Line 486: Dependency 1
Line 487: m1() {
Line 488: calculateTax(50);
Line 489: }
Line 490: Dependency 2
Line 491: m2() {
Line 492: calculateTax(150);
Line 493: }
Line 494: Dependency 3
Line 495: m3() {
Line 496: t = getFromDB()
Line 497: ensur      0
Line 498: e t >
Line 499: c
Line 500: teTax(t);
Line 501: alcula
Line 502: }
Line 503: Figure 4.1
Line 504: The calculateTax() method and all the classes that possibly depend on it
Line 505: 
Line 506: --- 페이지 135 ---
Line 507: 107
Line 508: Changing contracts, and the Liskov substitution principle
Line 509:  The same type of reasoning can be applied to the post-conditions. There, we
Line 510: observe the inverse relation. The clients know that calculateTax never returns nega-
Line 511: tive numbers. Although this would make no business sense, let’s suppose the method
Line 512: now also returns negative numbers. This is a breaking change: the clients of this class
Line 513: do not expect negative numbers to come back and probably are not ready to handle
Line 514: them. The system may behave erratically, depending on whether the returned tax is
Line 515: negative. We learn that if we change our post-condition to something weaker and less
Line 516: restrictive, our clients may break.
Line 517:  On the other hand, if the post-condition changes to “the returned value is always
Line 518: greater than 100,” the clients will not break. They were already prepared for the
Line 519: returning value to be between 0 and infinity, and the range from 100 to infinity is a
Line 520: subset of the previous domain. We learn that changing post-conditions to something
Line 521: stronger and more restrictive prevents breaking changes in the dependencies.
Line 522: 4.3.1
Line 523: Inheritance and contracts
Line 524: We mostly use Java for the examples in this book, and Java is an object-oriented lan-
Line 525: guage, so I must discuss what happens when we use inheritance. Figure 4.2 shows that
Line 526: the TaxCalculator class has many children (TaxCalculatorBrazil which calculates
Line 527: taxes in Brazil, TaxCalculatorNL, which calculates taxes in the Netherlands, and so
Line 528: on). These child classes all override calculateTax() and change the pre- or post-
Line 529: conditions one way or another. Are these contract changes breaking changes?
Line 530:  We can apply the same reasoning as when we discussed changing contracts. Let’s
Line 531: start by focusing on the client class rather than the child classes. Suppose the client
Line 532: Ta
Line 533: tor
Line 534: xCalcula
Line 535: c
Line 536: teTax(value)
Line 537: alcula
Line 538: v l
Line 539: returns
Line 540: 0
Line 541: a ue >= 0,         >=
Line 542: Client
Line 543: Dep
Line 544: on
Line 545: ends
Line 546: Note how all children changed either the pre- or the post-condition,
Line 547: in comparison to the base class. Are these breaking changes or not?
Line 548: Ta
Line 549: torBrazil
Line 550: xCalcula
Line 551: c
Line 552: eTax(value)
Line 553: alculat
Line 554: v           returns
Line 555: ,inf]
Line 556: alue >= 0,         [-inf
Line 557: Ta
Line 558: torUS
Line 559: xCalcula
Line 560: c
Line 561: teTax(value)
Line 562: alcula
Line 563: v
Line 564: ue >= 100
Line 565: r       >= 0
Line 566: al         ,  eturns
Line 567: TaxCalculatorNL
Line 568: c
Line 569: teTax(value)
Line 570: alcula
Line 571: val       f,inf], returns >= 0
Line 572: ue [-in
Line 573: Figure 4.2
Line 574: A base class and its child classes. The client depends on the base class, which means any of its 
Line 575: children may be used at run time.
Line 576: 
Line 577: --- 페이지 136 ---
Line 578: 108
Line 579: CHAPTER 4
Line 580: Designing contracts
Line 581: class receives a TaxCalculator in its constructor and later uses it in its methods. Due
Line 582: to polymorphism, we know that any of the child classes can also be passed to the cli-
Line 583: ent: for example, we can pass a TaxCalculatorBrazil or a TaxCalculatorUS, and it
Line 584: will be accepted because they are all children of the base class.
Line 585:  Since the client class does not know which tax calculator was given to it, it can only
Line 586: assume that whatever class it received will respect the pre- and post-conditions of the
Line 587: base class (the only class the client knows). In this case, value must be greater than or
Line 588: equal to 0 and should return a value greater than or equal to 0. Let’s explore what will
Line 589: happen if each of the child classes is given to the client class:
Line 590: 
Line 591: TaxCalculatorBrazil has the same pre-conditions as the base class. This means
Line 592: there is no way the client class will observe strange behavior regarding the pre-
Line 593: conditions if it is given TaxCalculatorBrazil. On the other hand, the Tax-
Line 594: CalculatorBrazil class has a post-condition that the returned value is any num-
Line 595: ber. This is bad. The client class expects only values that are greater than or equal
Line 596: to zero; it does not expect negative numbers. So if TaxCalculatorBrazil returns
Line 597: a negative number to the client, this may surprise the client and lead to a failure.
Line 598: 
Line 599: TaxCalculatorUS has the following pre-condition: “value greater than or equal
Line 600: to 100.” This pre-condition is stronger than the pre-condition of the base class
Line 601: (value >= 0), and the client class does not know that. Thus the client may call
Line 602: the tax calculator with a value that is acceptable for the base class but not
Line 603: acceptable for TaxCalculatorUS. We can expect a failure to happen. The post-
Line 604: condition of TaxCalculatorUS is the same as that of the base class, so we do not
Line 605: expect problems there.
Line 606: 
Line 607: TaxCalculatorNL has a different pre-condition from the base class: it accepts
Line 608: any value. In other words, the pre-condition is weaker than that of the base
Line 609: class. So although the client is not aware of this pre-condition, we do not expect
Line 610: failures, as TaxCalculatorNL can handle all of the client’s inputs.
Line 611: If we generalize what we observe in this example, we arrive at the following rules
Line 612: whenever a subclass S (for example, TaxCalculatorBrazil) inherits from a base class
Line 613: B (for example, TaxCalculator):
Line 614: 1
Line 615: The pre-conditions of subclass S should be the same as or weaker (accept more
Line 616: values) than the pre-conditions of base class B.
Line 617: 2
Line 618: The post-conditions of subclass S should be the same as or stronger (return
Line 619: fewer values) than the post-conditions of base class B.
Line 620: This idea that a subclass may be used as a substitution for a base class without
Line 621: breaking the expected behavior of the system is known as the Liskov substitution
Line 622: principle (LSP). This principle was introduced by Barbara Liskov in a 1987 keynote
Line 623: and later refined by her and Jeannette Wing in the famous “A behavioral notion of
Line 624: subtyping” paper (1994). The LSP became even more popular among software
Line 625: developers when Robert Martin popularized the SOLID principles, where the “L”
Line 626: stands for LSP.
Line 627: 
Line 628: --- 페이지 137 ---
Line 629: 109
Line 630: How is design-by-contract related to testing?
Line 631: NOTE
Line 632: A well-known best practice is to avoid inheritance whenever possible
Line 633: (see Effective Java’s item 16, “favor compostion over inheritance”). If you avoid
Line 634: inheritance, you naturally avoid all the problems just discussed. But it is not the
Line 635: goal of this book to discuss best practices in object-oriented design. If you ever
Line 636: need to use inheritance, you now know what to pay attention to. 
Line 637: 4.4
Line 638: How is design-by-contract related to testing?
Line 639: Defining clear pre-conditions, post-conditions, and invariants (and automating them
Line 640: in your code via, for example, assertions) helps developers in many ways. First, asser-
Line 641: tions ensure that bugs are detected early in the production environment. As soon as a
Line 642: contract is violated, the program halts instead of continuing its execution, which is
Line 643: usually a good idea. The error you get from an assertion violation is very specific, and
Line 644: you know precisely what to debug for. This may not be the case without assertions.
Line 645: Imagine a program that performs calculations. The method that does the heavy calcu-
Line 646: lation does not work well with negative numbers. However, instead of defining such a
Line 647: restriction as an explicit pre-condition, the method returns an invalid output if a neg-
Line 648: ative number comes in. This invalid number is then passed to other parts of the sys-
Line 649: tem, which may incur other unexpected behavior. Given that the program does not
Line 650: crash per se, it may be hard for the developer to know that the root cause of the prob-
Line 651: lem was a violation of the pre-condition.
Line 652:  Second, pre-conditions, post-conditions, and invariants provide developers with
Line 653: ideas about what to test. As soon as we see the qty > 0 pre-condition, we know this is
Line 654: something to exercise via unit, integration, or system tests. Therefore, contracts do
Line 655: not replace (unit) testing: they complement it. In chapter 5, you will see how to use
Line 656: such contracts and write test cases that automatically generate random input data,
Line 657: looking for possible violations.
Line 658:  Third, such explicit contracts make the lives of consumers much easier. The class
Line 659: (or server, if you think of it as a client-server application) does its job as long as its meth-
Line 660: ods are used properly by the consumer (or client). If the client uses the server’s meth-
Line 661: ods so that their pre-conditions hold, the server guarantees that the post-conditions will
Line 662: hold after the method call. In other words, the server makes sure the method delivers
Line 663: what it promises. Suppose a method expects only positive numbers (as a pre-condition)
Line 664: and promises to return only positive numbers (as a post-condition). As a client, if you
Line 665: pass a positive number, you are sure the server will return a positive number and never
Line 666: a negative number. The client, therefore, does not need to check if the return is nega-
Line 667: tive, simplifying its code.
Line 668:  I do not see design-by-contract as a testing practice per se. I see it as more of a
Line 669: design technique. That is also why I include it in the development part of the devel-
Line 670: oper testing workflow (figure 1.4).
Line 671: NOTE
Line 672: Another benefit of assertions is that they serve as oracles during fuzz-
Line 673: ing or other intelligent testing. These tools reason about the pre-conditions,
Line 674: post-conditions, and invariants that are clearly expressed in the code and
Line 675: 
Line 676: --- 페이지 138 ---
Line 677: 110
Line 678: CHAPTER 4
Line 679: Designing contracts
Line 680: look for ways to break them. If you want to read more about fuzzing, I suggest
Line 681: The Fuzzing Book (https://fuzzingbook.org). 
Line 682: 4.5
Line 683: Design-by-contract in the real world
Line 684: Let me close this chapter with some pragmatic tips on how to use design-by-contract
Line 685: in practice.
Line 686: 4.5.1
Line 687: Weak or strong pre-conditions?
Line 688: A very important design decision when modeling contracts is whether to use strong or
Line 689: weak contracts. This is a matter of trade-offs.
Line 690:  Consider a method with a weak pre-condition. For example, the method accepts
Line 691: any input value, including null. This method is easy for clients to use for the clients:
Line 692: any call to it will work, and the method will never throw an exception related to a pre-
Line 693: condition being violated (as there are no pre-conditions to be violated). However, this
Line 694: puts an extra burden on the method, as it has to handle any invalid inputs.
Line 695:  On the other hand, consider a strong contract: the method only accepts positive
Line 696: numbers and does not accept null values. The extra burden is now on the side of the
Line 697: client. The client must make sure it does not violate the pre-conditions of the method.
Line 698: This may require extra code.
Line 699:  There is no clear way to go, and the decision should be made considering the
Line 700: whole context. For example, many methods of the Apache Commons library have
Line 701: weak pre-conditions, making it much easier for clients to use the API. Library develop-
Line 702: ers often prefer to design weaker pre-conditions and simplify the clients’ lives. 
Line 703: 4.5.2
Line 704: Input validation, contracts, or both?
Line 705: Developers are aware of how important input validation is. A mistake in the validation
Line 706: may lead to security vulnerabilities. Therefore, developers often handle input valida-
Line 707: tion whenever data comes from the end user.
Line 708:  Consider a web application that stores products for an online store. To add a new
Line 709: product, a user must pass a name, a description, and a value. Before saving the new
Line 710: product to the database, the developer performs checks to ensure that the input val-
Line 711: ues are as expected. Here is the greatly simplified pseudo-code.
Line 712: class ProductController {
Line 713:   // more code here ...
Line 714:   public void add(String productName, String productDescription,
Line 715:    double price) { 
Line 716:     String sanitizedProductName = sanitize(productName); 
Line 717:     String sanitizedProductDescription = sanitize(productDescription); 
Line 718: Listing 4.12
Line 719: Pseudo-code for input validation
Line 720: These parameters come directly from the 
Line 721: end user, and they need to be validated 
Line 722: before being used.
Line 723: We use the made-up sanitize()
Line 724: method to sanitize (remove invalid
Line 725: characters from) the inputs.
Line 726: 
Line 727: --- 페이지 139 ---
Line 728: 111
Line 729: Design-by-contract in the real world
Line 730:     if(!isValidProductName(sanitizedProductName)) { 
Line 731:        errorMessages.add("Invalid product name");
Line 732:     }
Line 733:     if(!isValidProductDescription(sanitizedProductDescription)) { 
Line 734:        errorMessages.add("Invalid product description");
Line 735:     }
Line 736:     if(!isValidPriceRange(price)) { 
Line 737:        errorMessages.add("Invalid price");
Line 738:     }
Line 739:     if(errorMessages.empty()) { 
Line 740:       Product newProduct = new Product(sanitizedProductName,
Line 741:         ➥ productDescription, price);
Line 742:       database.save(newProduct);
Line 743:       redirectTo("productPage", newProduct.getId());
Line 744:     } else { 
Line 745:       redirectTo("addProduct", errorMessages.getErrors());
Line 746:     }
Line 747:   }
Line 748: }
Line 749: Given all this validation before the objects are even created, you may be thinking, “Do
Line 750: I need to model pre-conditions and post-conditions in the classes and methods? I
Line 751: already know the values are valid!” Let me give you a pragmatic perspective.
Line 752:  First, let’s focus on the difference between validation and contracts. Validation
Line 753: ensures that bad or invalid data that may come from users does not infiltrate our sys-
Line 754: tems. For example, if the user types a string in the Quantity field on the Add Product
Line 755: page, we should return a friendly message saying “Quantity should be a numeric
Line 756: value.” This is what validation is about: it validates that the data coming from the user
Line 757: is correct and, if not, returns a message.
Line 758:  On the other hand, contracts ensure that communication between classes happens
Line 759: without a problem. We do not expect problems to occur—the data is already vali-
Line 760: dated. However, if a violation occurs, the program halts, since something unexpected
Line 761: happened. The application also returns an error message to the user. Figure 4.3 illus-
Line 762: trates the difference between validation and code contracts.
Line 763:  Both validation and contracts should happen, as they are different. The question is
Line 764: how to avoid repetition. Maybe the validation and pre-condition are the same, which
Line 765: means either there is code repetition or the check is happening twice.
Line 766:  I tend to be pragmatic. As a rule of thumb, I prefer to avoid repetition. If the input
Line 767: validation already checked for, say, the length of the product description being
Line 768: greater than 10 characters, I don’t re-check it as a pre-condition in the constructor of
Line 769: the Product class. This implies that no instances of Product are instantiated without
Line 770: input validation first. Your architecture must ensure that some zones of the code are
Line 771: safe and that data has been already cleaned up.
Line 772:  On the other hand, if a contract is very important and should never be broken
Line 773: (the impact could be significant), I do not mind using a little repetition and extra
Line 774: Ensures that
Line 775: values are
Line 776: within the
Line 777: expected
Line 778: format,
Line 779: range, and
Line 780: so on
Line 781: Only when the parameters are 
Line 782: valid do we create objects. 
Line 783: Is this a replacement for 
Line 784: design-by-contract?
Line 785: Otherwise, we return 
Line 786: to the Add Product 
Line 787: page and display the 
Line 788: error messages.
Line 789: 
Line 790: --- 페이지 140 ---
Line 791: 112
Line 792: CHAPTER 4
Line 793: Designing contracts
Line 794: computational power to check it at both input-validation time and contract-checking
Line 795: time. Again, consider the context to decide what works best for each situation.
Line 796: NOTE
Line 797: Arie van Deursen offers a clear answer on Stack Overflow about the
Line 798: differences between design-by-contract and validation, and I strongly recom-
Line 799: mend that you check it out: https://stackoverflow.com/a/5452329. 
Line 800: 4.5.3
Line 801: Asserts and exceptions: When to use one or the other
Line 802: Java does not offer a clear mechanism for expressing code contracts. Only a few
Line 803: popular programming languages do, such as F#. The assert keyword in Java is okay,
Line 804: but if you forget to enable it in the runtime, the contracts may not be checked in
Line 805: production. That is why many developers prefer to use (checked or unchecked)
Line 806: exceptions.
Line 807:  Here is my rule of thumb:
Line 808: If I am modeling the contracts of a library or utility class, I favor exceptions, fol-
Line 809: lowing the wisdom of the most popular libraries.
Line 810: If I am modeling business classes and their interactions and I know that the
Line 811: data was cleaned up in previous layers (say, in the controller of a Model-View-
Line 812: Controller [MVC] architecture), I favor assertions. The data was already vali-
Line 813: dated, and I am sure they start their work with valid data. I do not expect pre-
Line 814: conditions or post-conditions to be violated, so I prefer to use the assert
Line 815: instruction. It will throw an AssertionError, which will halt execution. I also
Line 816: ensure that my final user does not see an exception stack trace but instead is
Line 817: shown a more elegant error page.
Line 818: If I am modeling business classes but I am not sure whether the data was already
Line 819: cleaned up, I go for exceptions.
Line 820: Input validation
Line 821: Input
Line 822: data
Line 823: User
Line 824: Bad input values that come from the
Line 825: user do not get to the main classes.
Line 826: Instead, a message is displayed, and
Line 827: the user tries again.
Line 828: If a class makes a bad call to another class, e.g., a pre-condition violation,
Line 829: the program halts, as this should not happen. The user may also be informed
Line 830: about the problem, although commonly with a more generic message.
Line 831: Class B
Line 832: Class A
Line 833: Class C
Line 834: Figure 4.3
Line 835: The difference between validation and code contracts. Each 
Line 836: circle represents one input coming to the system.
Line 837: 
Line 838: --- 페이지 141 ---
Line 839: 113
Line 840: Design-by-contract in the real world
Line 841: When it comes to validation, I tend not to use either assertions or exceptions. I prefer
Line 842: to model validations in more elegant ways. First, you rarely want to stop the validation
Line 843: when the first check fails. Instead, it is more common to show a complete list of errors
Line 844: to the user. Therefore, you need a structure that allows you to build the error message
Line 845: as you go. Second, you may want to model complex validations, which may require
Line 846: lots of code. Having all the validations in a single class or method may lead to code
Line 847: that is very long, highly complex, and hard to reuse.
Line 848:  If you are curious, I suggest the Specification pattern proposed by Eric Evans in his
Line 849: seminal book, Domain-Driven Design (2004). Another nice resource is the article “Use
Line 850: of Assertions” by John Regehr (2014); it discusses the pros and cons of assertions, mis-
Line 851: conceptions, and limitations in a very pragmatic way.
Line 852:  Finally, in this chapter, I used native Java exceptions, such as RuntimeException. In
Line 853: practice, you may prefer to throw more specialized and semantic exceptions, such as
Line 854: NegativeValueException. That helps clients treat business exceptions differently
Line 855: from real one-in-a-million exceptional behavior.
Line 856: NOTE
Line 857: Formal semantics scholars do not favor the use of assertions over
Line 858: exceptions. I should not use the term design-by-contract for the snippets where I
Line 859: use an if statement and throw an exception—that is defensive programming.
Line 860: But, as I said before, I am using the term design-by-contract for the idea of
Line 861: reflecting about contracts and somehow making them explicit in the code. 
Line 862: 4.5.4
Line 863: Exception or soft return values?
Line 864: We saw that a possible way to simplify clients’ lives is to make your method return a
Line 865: “soft value” instead of throwing an exception. Go back to listing 4.5 for an example.
Line 866:  My rule of thumb is the following:
Line 867: If it is behavior that should not happen, and clients would not know what to do
Line 868: with it, I throw an exception. That would be the case with the calculateTax
Line 869: method. If a negative value comes in, that is unexpected behavior, and we
Line 870: should halt the program rather than let it make bad calculations. The monitor-
Line 871: ing systems will catch the exception, and we will debug the case.
Line 872: On the other hand, if I can see a soft return for the client method that would allow
Line 873: the client to keep working, I go for it. Imagine a utility method that trims a string.
Line 874: A pre-condition of this method could be that it does not accept null strings. But
Line 875: returning an empty string in case of a null is a soft return that clients can deal with. 
Line 876: 4.5.5
Line 877: When not to use design-by-contract
Line 878: Understanding when not to use a practice is as important as knowing when to use it.
Line 879: In this case, I may disappoint you, as I cannot see a single good reason not to use the
Line 880: design-by-contract ideas presented in this chapter. The development of object-oriented
Line 881: systems is all about ensuring that objects can communicate and collaborate properly.
Line 882: Experience shows me that making the pre-conditions, post-conditions, and invari-
Line 883: ants explicit in the code is not expensive and does not take a lot of time. Therefore,
Line 884: 
Line 885: --- 페이지 142 ---
Line 886: 114
Line 887: CHAPTER 4
Line 888: Designing contracts
Line 889: I recommend that you consider using this approach. (Note that I am not discussing
Line 890: input validation here, which is fundamental and has to be done whether or not you
Line 891: like design-by-contracts.)
Line 892:  I also want to highlight that design-by-contract does not replace the need for test-
Line 893: ing. Why? Because, to the best of my knowledge and experience, you cannot express all
Line 894: the expected behavior of a piece of code solely with pre-conditions, post-conditions, and
Line 895: invariants. In practice, I suggest that you design contracts to ensure that classes can
Line 896: communicate with each other without fear, and test to ensure that the behavior of the
Line 897: class is correct. 
Line 898: 4.5.6
Line 899: Should we write tests for pre-conditions, post-conditions, 
Line 900: and invariants?
Line 901: In a way, assertions, pre-conditions, post-conditions, and invariant checks test the pro-
Line 902: duction code from the inside. Do we also need to write (unit) tests for them?
Line 903:  To answer this question, let me again discuss the difference between validation and
Line 904: pre-conditions. Validation is what you do to ensure that the data is valid. Pre-conditions
Line 905: explicitly state under what conditions a method can be invoked.
Line 906:  I usually write automated tests for validation. We want to ensure that our validation
Line 907: mechanisms are in place and working as expected. On the other hand, I rarely write
Line 908: tests for assertions. They are naturally covered by tests that focus on other business
Line 909: rules. I suggest reading Arie van Deursen’s answer on Stack Overflow about writing
Line 910: tests for assertions (https://stackoverflow.com/a/6486294/165292).
Line 911: NOTE
Line 912: Some code coverage tools do not handle asserts well. JaCoCo, for
Line 913: example, cannot report full branch coverage in assertions. This is another
Line 914: great example of why you should not use coverage numbers blindly. 
Line 915: 4.5.7
Line 916: Tooling support
Line 917: There is more and more support for pre- and post-condition checks, even in languages
Line 918: like Java. For instance, IntelliJ, a famous Java IDE, offers the @Nullable and @NotNull
Line 919: annotations (http://mng.bz/QWMe). You can annotate your methods, attributes, or
Line 920: return values with them, and IntelliJ will alert you about possible violations. IntelliJ can
Line 921: even transform those annotations into proper assert checks at compile time.
Line 922:  In addition, projects such as Bean Validation (https://beanvalidation.org) enable
Line 923: you to write more complex validations, such as “this string should be an email” or “this
Line 924: integer should be between 1 and 10.” I appreciate such useful tools that help us
Line 925: ensure the quality of our products. The more, the merrier. 
Line 926: Exercises
Line 927: 4.1
Line 928: Which of the following is a valid reason to use assertions in your code?
Line 929: A To verify expressions with side effects
Line 930: B To handle exceptional cases in the program
Line 931: 
Line 932: --- 페이지 143 ---
Line 933: 115
Line 934: Exercises
Line 935: C To conduct user input validation
Line 936: D To make debugging easier
Line 937: 4.2
Line 938: Consider the following squareAt method:
Line 939: public Square squareAt(int x, int y){
Line 940:    assert x >= 0;
Line 941:    assert x < board.length;
Line 942:    assert y >= 0;
Line 943:    assert y < board[x].length;
Line 944:    assert board != null;
Line 945:    Square result = board[x][y];
Line 946:    assert result != null;
Line 947:    return result;
Line 948: }
Line 949: Suppose we remove the last assertion (assert result != null), which states
Line 950: that the result can never be null. Are the existing pre-conditions of the
Line 951: squareAt method enough to ensure the property of the removed assertion?
Line 952: What can we add to the class (other than the just-removed post-condition) to
Line 953: guarantee this property?
Line 954: 4.3
Line 955: See the squareAt method in exercise 4.3. Which assertion(s), if any, can be
Line 956: turned into class invariants? Choose all that apply.
Line 957: A
Line 958: x >= 0 and x < board.length
Line 959: B
Line 960: board != null
Line 961: C
Line 962: result != null
Line 963: D
Line 964: y >= 0 and y < board[x].length
Line 965: 4.4
Line 966: You run your application with assertion checking enabled. Unfortunately, it
Line 967: reports an assertion failure, signaling a class invariant violation in one of the
Line 968: libraries your application uses. Assume that your application is following all the
Line 969: pre-conditions established by the library.
Line 970: Which of the following statements best characterizes the situation and corre-
Line 971: sponding action to take?
Line 972: A Since you assume that the contract is correct, the safe action is to run the
Line 973: server with assertion checking disabled.
Line 974: B This indicates an integration fault and requires a redesign that involves
Line 975: the interface that is offered by the library and used by your application.
Line 976: C This indicates a problem in the implementation of that library and
Line 977: requires a fix in the library’s code.
Line 978: D This indicates that you invoked one of the methods of the library in the
Line 979: wrong way and requires a fix in your application.
Line 980: 4.5
Line 981: Can static methods have invariants? Explain your answer.
Line 982: 
Line 983: --- 페이지 144 ---
Line 984: 116
Line 985: CHAPTER 4
Line 986: Designing contracts
Line 987: 4.6
Line 988: A method M belongs to a class C and has a pre-condition P and a post-condition
Line 989: Q. Suppose that a developer creates a class C' that extends C and creates a method
Line 990: M' that overrides M.
Line 991: Which one of the following statements correctly explains the relative strength
Line 992: of the pre- (P') and post-conditions (Q') of the overridden method M'?
Line 993: A
Line 994: P' should be equal to or weaker than P, and Q' should be equal to or
Line 995: stronger than Q.
Line 996: B
Line 997: P' should be equal to or stronger than P, and Q' should be equal to or
Line 998: stronger than Q.
Line 999: C
Line 1000: P' should be equal to or weaker than P, and Q' should be equal to or
Line 1001: weaker than Q.
Line 1002: D
Line 1003: P' should be equal to or stronger than P, and Q' should be equal to or
Line 1004: weaker than Q.
Line 1005: Summary
Line 1006: Contracts ensure that classes can safely communicate with each other without
Line 1007: surprises.
Line 1008: In practice, designing contracts boils down to explicitly defining the pre-
Line 1009: conditions, post-conditions, and invariants of our classes and methods.
Line 1010: Deciding to go for a weaker or a stronger contract is a contextual decision. Both
Line 1011: have advantages and disadvantages.
Line 1012: Design-by-contract does not remove the need for validation. Validation and con-
Line 1013: tract checking are different things with different objectives. Both should be done.
Line 1014: Whenever changing a contract, we need to reflect on the impact of the change.
Line 1015: Some contract changes might be breaking changes.