Line 1: 
Line 2: --- 페이지 141 ---
Line 3: 119
Line 4: Styles of unit testing
Line 5: Chapter 4 introduced the four attributes of a good unit test: protection against
Line 6: regressions, resistance to refactoring, fast feedback, and maintainability. These attri-
Line 7: butes form a frame of reference that you can use to analyze specific tests and unit
Line 8: testing approaches. We analyzed one such approach in chapter 5: the use of mocks.
Line 9:  In this chapter, I apply the same frame of reference to the topic of unit testing
Line 10: styles. There are three such styles: output-based, state-based, and communication-
Line 11: based testing. Among the three, the output-based style produces tests of the highest
Line 12: quality, state-based testing is the second-best choice, and communication-based
Line 13: testing should be used only occasionally.
Line 14:  Unfortunately, you can’t use the output-based testing style everywhere. It’s only
Line 15: applicable to code written in a purely functional way. But don’t worry; there are
Line 16: techniques that can help you transform more of your tests into the output-based
Line 17: style. For that, you’ll need to use functional programming principles to restructure
Line 18: the underlying code toward a functional architecture.
Line 19: This chapter covers
Line 20: Comparing styles of unit testing
Line 21: The relationship between functional and 
Line 22: hexagonal architectures
Line 23: Transitioning to output-based testing
Line 24: 
Line 25: --- 페이지 142 ---
Line 26: 120
Line 27: CHAPTER 6
Line 28: Styles of unit testing
Line 29:  Note that this chapter doesn’t provide a deep dive into the topic of functional pro-
Line 30: gramming. Still, by the end of this chapter, I hope you’ll have an intuitive understand-
Line 31: ing of how functional programming relates to output-based testing. You’ll also learn
Line 32: how to write more of your tests using the output-based style, as well as the limitations
Line 33: of functional programming and functional architecture.
Line 34: 6.1
Line 35: The three styles of unit testing
Line 36: As I mentioned in the chapter introduction, there are three styles of unit testing:
Line 37: Output-based testing 
Line 38: State-based testing 
Line 39: Communication-based testing
Line 40: You can employ one, two, or even all three styles together in a single test. This sec-
Line 41: tion lays the foundation for the whole chapter by defining (with examples) those
Line 42: three styles of unit testing. You’ll see how they score against each other in the sec-
Line 43: tion after that.
Line 44: 6.1.1
Line 45: Defining the output-based style
Line 46: The first style of unit testing is the output-based style, where you feed an input to the sys-
Line 47: tem under test (SUT) and check the output it produces (figure 6.1). This style of unit
Line 48: testing is only applicable to code that doesn’t change a global or internal state, so the
Line 49: only component to verify is its return value.
Line 50: The following listing shows an example of such code and a test covering it. The Price-
Line 51: Engine class accepts an array of products and calculates a discount.
Line 52: public class PriceEngine
Line 53: {
Line 54: public decimal CalculateDiscount(params Product[] products)
Line 55: Listing 6.1
Line 56: Output-based testing
Line 57: Output
Line 58: Production code
Line 59: Input
Line 60: Output
Line 61: veriﬁcation
Line 62: Figure 6.1
Line 63: In output-based testing, tests verify the output the system 
Line 64: generates. This style of testing assumes there are no side effects and the only 
Line 65: result of the SUT’s work is the value it returns to the caller.
Line 66: 
Line 67: --- 페이지 143 ---
Line 68: 121
Line 69: The three styles of unit testing
Line 70: {
Line 71: decimal discount = products.Length * 0.01m;
Line 72: return Math.Min(discount, 0.2m);
Line 73: }
Line 74: }
Line 75: [Fact]
Line 76: public void Discount_of_two_products()
Line 77: {
Line 78: var product1 = new Product("Hand wash");
Line 79: var product2 = new Product("Shampoo");
Line 80: var sut = new PriceEngine();
Line 81: decimal discount = sut.CalculateDiscount(product1, product2);
Line 82: Assert.Equal(0.02m, discount);
Line 83: }
Line 84: PriceEngine multiplies the number of products by 1% and caps the result at 20%.
Line 85: There’s nothing else to this class. It doesn’t add the products to any internal collec-
Line 86: tion, nor does it persist them in a database. The only outcome of the Calculate-
Line 87: Discount() method is the discount it returns: the output value (figure 6.2).
Line 88: The output-based style of unit testing is also known as functional. This name takes root
Line 89: in functional programming, a method of programming that emphasizes a preference for
Line 90: side-effect-free code. We’ll talk more about functional programming and functional
Line 91: architecture later in this chapter. 
Line 92: 6.1.2
Line 93: Defining the state-based style
Line 94: The state-based style is about verifying the state of the system after an operation is com-
Line 95: plete (figure 6.3). The term state in this style of testing can refer to the state of the
Line 96: SUT itself, of one of its collaborators, or of an out-of-process dependency, such as
Line 97: the database or the filesystem.
Line 98: Output
Line 99: veriﬁcation
Line 100: Output
Line 101: PriceEngine
Line 102: Input
Line 103: Product (“Hand wash”)
Line 104: Product (“Shampoo”)
Line 105: 2% discount
Line 106: Figure 6.2
Line 107: PriceEngine represented using input-output notation. Its 
Line 108: CalculateDiscount() method accepts an array of products and 
Line 109: calculates a discount.
Line 110: 
Line 111: --- 페이지 144 ---
Line 112: 122
Line 113: CHAPTER 6
Line 114: Styles of unit testing
Line 115: Here’s an example of state-based testing. The Order class allows the client to add a
Line 116: new product.
Line 117: public class Order
Line 118: {
Line 119: private readonly List<Product> _products = new List<Product>();
Line 120: public IReadOnlyList<Product> Products => _products.ToList();
Line 121: public void AddProduct(Product product)
Line 122: {
Line 123: _products.Add(product);
Line 124: }
Line 125: }
Line 126: [Fact]
Line 127: public void Adding_a_product_to_an_order()
Line 128: {
Line 129: var product = new Product("Hand wash");
Line 130: var sut = new Order();
Line 131: sut.AddProduct(product);
Line 132: Assert.Equal(1, sut.Products.Count);
Line 133: Assert.Equal(product, sut.Products[0]);
Line 134: }
Line 135: The test verifies the Products collection after the addition is completed. Unlike
Line 136: the example of output-based testing in listing 6.1, the outcome of AddProduct() is the
Line 137: change made to the order’s state. 
Line 138: 6.1.3
Line 139: Defining the communication-based style
Line 140: Finally, the third style of unit testing is communication-based testing. This style uses
Line 141: mocks to verify communications between the system under test and its collaborators
Line 142: (figure 6.4).
Line 143: Listing 6.2
Line 144: State-based testing
Line 145: State
Line 146: veriﬁcation
Line 147: State
Line 148: veriﬁcation
Line 149: Production code
Line 150: Input
Line 151: Figure 6.3
Line 152: In state-based testing, tests verify the final state of the 
Line 153: system after an operation is complete. The dashed circles represent that 
Line 154: final state.
Line 155: 
Line 156: --- 페이지 145 ---
Line 157: 123
Line 158: Comparing the three styles of unit testing
Line 159: The following listing shows an example of communication-based testing.
Line 160: [Fact]
Line 161: public void Sending_a_greetings_email()
Line 162: {
Line 163: var emailGatewayMock = new Mock<IEmailGateway>();
Line 164: var sut = new Controller(emailGatewayMock.Object);
Line 165: sut.GreetUser("user@email.com");
Line 166: emailGatewayMock.Verify(
Line 167: x => x.SendGreetingsEmail("user@email.com"),
Line 168: Times.Once);
Line 169: }
Line 170: 6.2
Line 171: Comparing the three styles of unit testing
Line 172: There’s nothing new about output-based, state-based, and communication-based
Line 173: styles of unit testing. In fact, you already saw all of these styles previously in this book.
Line 174: What’s interesting is comparing them to each other using the four attributes of a good
Line 175: unit test. Here are those attributes again (refer to chapter 4 for more details):
Line 176: Protection against regressions
Line 177: Resistance to refactoring
Line 178: Fast feedback
Line 179: Maintainability
Line 180: In our comparison, let’s look at each of the four separately.
Line 181: Listing 6.3
Line 182: Communication-based testing
Line 183: Styles and schools of unit testing
Line 184: The classical school of unit testing prefers the state-based style over the communication-
Line 185: based one. The London school makes the opposite choice. Both schools use output-
Line 186: based testing. 
Line 187: Collaboration
Line 188: veriﬁcation
Line 189: Mocks
Line 190: Production code
Line 191: Input
Line 192: Figure 6.4
Line 193: In communication-based 
Line 194: testing, tests substitute the SUT’s 
Line 195: collaborators with mocks and verify 
Line 196: that the SUT calls those 
Line 197: collaborators correctly.
Line 198: 
Line 199: --- 페이지 146 ---
Line 200: 124
Line 201: CHAPTER 6
Line 202: Styles of unit testing
Line 203: 6.2.1
Line 204: Comparing the styles using the metrics of protection against 
Line 205: regressions and feedback speed
Line 206: Let’s first compare the three styles in terms of the protection against regressions
Line 207: and feedback speed attributes, as these attributes are the most straightforward in this
Line 208: particular comparison. The metric of protection against regressions doesn’t depend
Line 209: on a particular style of testing. This metric is a product of the following three
Line 210: characteristics:
Line 211: The amount of code that is executed during the test
Line 212: The complexity of that code
Line 213: Its domain significance
Line 214: Generally, you can write a test that exercises as much or as little code as you like; no
Line 215: particular style provides a benefit in this area. The same is true for the code’s com-
Line 216: plexity and domain significance. The only exception is the communication-based
Line 217: style: overusing it can result in shallow tests that verify only a thin slice of code and
Line 218: mock out everything else. Such shallowness is not a definitive feature of communication-
Line 219: based testing, though, but rather is an extreme case of abusing this technique.
Line 220:  There’s little correlation between the styles of testing and the test’s feedback speed.
Line 221: As long as your tests don’t touch out-of-process dependencies and thus stay in the
Line 222: realm of unit testing, all styles produce tests of roughly equal speed of execution.
Line 223: Communication-based testing can be slightly worse because mocks tend to introduce
Line 224: additional latency at runtime. But the difference is negligible, unless you have tens of
Line 225: thousands of such tests. 
Line 226: 6.2.2
Line 227: Comparing the styles using the metric of resistance 
Line 228: to refactoring
Line 229: When it comes to the metric of resistance to refactoring, the situation is different.
Line 230: Resistance to refactoring is the measure of how many false positives (false alarms) tests gen-
Line 231: erate during refactorings. False positives, in turn, are a result of tests coupling to
Line 232: code’s implementation details as opposed to observable behavior.
Line 233:  Output-based testing provides the best protection against false positives because
Line 234: the resulting tests couple only to the method under test. The only way for such tests to
Line 235: couple to implementation details is when the method under test is itself an implemen-
Line 236: tation detail.
Line 237:  State-based testing is usually more prone to false positives. In addition to the
Line 238: method under test, such tests also work with the class’s state. Probabilistically speak-
Line 239: ing, the greater the coupling between the test and the production code, the greater
Line 240: the chance for this test to tie to a leaking implementation detail. State-based tests tie
Line 241: to a larger API surface, and hence the chances of coupling them to implementation
Line 242: details are also higher.
Line 243:  Communication-based testing is the most vulnerable to false alarms. As you may
Line 244: remember from chapter 5, the vast majority of tests that check interactions with test
Line 245: 
Line 246: --- 페이지 147 ---
Line 247: 125
Line 248: Comparing the three styles of unit testing
Line 249: doubles end up being brittle. This is always the case for interactions with stubs—you
Line 250: should never check such interactions. Mocks are fine only when they verify interac-
Line 251: tions that cross the application boundary and only when the side effects of those
Line 252: interactions are visible to the external world. As you can see, using communication-
Line 253: based testing requires extra prudence in order to maintain proper resistance to
Line 254: refactoring.
Line 255:  But just like shallowness, brittleness is not a definitive feature of the communication-
Line 256: based style, either. You can reduce the number of false positives to a minimum by
Line 257: maintaining proper encapsulation and coupling tests to observable behavior only.
Line 258: Admittedly, though, the amount of due diligence varies depending on the style of
Line 259: unit testing. 
Line 260: 6.2.3
Line 261: Comparing the styles using the metric of maintainability
Line 262: Finally, the maintainability metric is highly correlated with the styles of unit testing;
Line 263: but, unlike with resistance to refactoring, there’s not much you can do to mitigate
Line 264: that. Maintainability evaluates the unit tests’ maintenance costs and is defined by the
Line 265: following two characteristics:
Line 266: How hard it is to understand the test, which is a function of the test’s size
Line 267: How hard it is to run the test, which is a function of how many out-of-process
Line 268: dependencies the test works with directly
Line 269: Larger tests are less maintainable because they are harder to grasp or change when
Line 270: needed. Similarly, a test that directly works with one or several out-of-process depen-
Line 271: dencies (such as the database) is less maintainable because you need to spend time
Line 272: keeping those out-of-process dependencies operational: rebooting the database
Line 273: server, resolving network connectivity issues, and so on.
Line 274: MAINTAINABILITY OF OUTPUT-BASED TESTS
Line 275: Compared with the other two types of testing, output-based testing is the most main-
Line 276: tainable. The resulting tests are almost always short and concise and thus are easier to
Line 277: maintain. This benefit of the output-based style stems from the fact that this style boils
Line 278: down to only two things: supplying an input to a method and verifying its output,
Line 279: which you can often do with just a couple lines of code.
Line 280:  Because the underlying code in output-based testing must not change the global
Line 281: or internal state, these tests don’t deal with out-of-process dependencies. Hence,
Line 282: output-based tests are best in terms of both maintainability characteristics. 
Line 283: MAINTAINABILITY OF STATE-BASED TESTS
Line 284: State-based tests are normally less maintainable than output-based ones. This is
Line 285: because state verification often takes up more space than output verification. Here’s
Line 286: another example of state-based testing.
Line 287:  
Line 288:  
Line 289: 
Line 290: --- 페이지 148 ---
Line 291: 126
Line 292: CHAPTER 6
Line 293: Styles of unit testing
Line 294: [Fact]
Line 295: public void Adding_a_comment_to_an_article()
Line 296: {
Line 297: var sut = new Article();
Line 298: var text = "Comment text";
Line 299: var author = "John Doe";
Line 300: var now = new DateTime(2019, 4, 1);
Line 301: sut.AddComment(text, author, now);
Line 302: Assert.Equal(1, sut.Comments.Count);
Line 303:     
Line 304: Assert.Equal(text, sut.Comments[0].Text);
Line 305:     
Line 306: Assert.Equal(author, sut.Comments[0].Author);     
Line 307: Assert.Equal(now, sut.Comments[0].DateCreated);   
Line 308: }
Line 309: This test adds a comment to an article and then checks to see if the comment
Line 310: appears in the article’s list of comments. Although this test is simplified and con-
Line 311: tains just a single comment, its assertion part already spans four lines. State-based
Line 312: tests often need to verify much more data than that and, therefore, can grow in size
Line 313: significantly.
Line 314:  You can mitigate this issue by introducing helper methods that hide most of the
Line 315: code and thus shorten the test (see listing 6.5), but these methods require significant
Line 316: effort to write and maintain. This effort is justified only when those methods are going
Line 317: to be reused across multiple tests, which is rarely the case. I’ll explain more about
Line 318: helper methods in part 3 of this book.
Line 319: [Fact]
Line 320: public void Adding_a_comment_to_an_article()
Line 321: {
Line 322: var sut = new Article();
Line 323: var text = "Comment text";
Line 324: var author = "John Doe";
Line 325: var now = new DateTime(2019, 4, 1);
Line 326: sut.AddComment(text, author, now);
Line 327: sut.ShouldContainNumberOfComments(1)    
Line 328: .WithComment(text, author, now);    
Line 329: }
Line 330: Another way to shorten a state-based test is to define equality members in the class
Line 331: that is being asserted. In listing 6.6, that’s the Comment class. You could turn it into a
Line 332: value object (a class whose instances are compared by value and not by reference), as
Line 333: shown next; this would also simplify the test, especially if you combined it with an
Line 334: assertion library like Fluent Assertions.
Line 335: Listing 6.4
Line 336: State verification that takes up a lot of space
Line 337: Listing 6.5
Line 338: Using helper methods in assertions
Line 339: Verifies the state 
Line 340: of the article
Line 341: Helper 
Line 342: methods
Line 343: 
Line 344: --- 페이지 149 ---
Line 345: 127
Line 346: Comparing the three styles of unit testing
Line 347: [Fact]
Line 348: public void Adding_a_comment_to_an_article()
Line 349: {
Line 350: var sut = new Article();
Line 351: var comment = new Comment(
Line 352: "Comment text",
Line 353: "John Doe",
Line 354: new DateTime(2019, 4, 1));
Line 355: sut.AddComment(comment.Text, comment.Author, comment.DateCreated);
Line 356: sut.Comments.Should().BeEquivalentTo(comment);
Line 357: }
Line 358: This test uses the fact that comments can be compared as whole values, without the
Line 359: need to assert individual properties in them. It also uses the BeEquivalentTo method
Line 360: from Fluent Assertions, which can compare entire collections, thereby removing the
Line 361: need to check the collection size.
Line 362:  This is a powerful technique, but it works only when the class is inherently a value
Line 363: and can be converted into a value object. Otherwise, it leads to code pollution (pollut-
Line 364: ing production code base with code whose sole purpose is to enable or, as in this case,
Line 365: simplify unit testing). We’ll discuss code pollution along with other unit testing anti-
Line 366: patterns in chapter 11.
Line 367:  As you can see, these two techniques—using helper methods and converting
Line 368: classes into value objects—are applicable only occasionally. And even when these tech-
Line 369: niques are applicable, state-based tests still take up more space than output-based tests
Line 370: and thus remain less maintainable. 
Line 371: MAINTAINABILITY OF COMMUNICATION-BASED TESTS
Line 372: Communication-based tests score worse than output-based and state-based tests on
Line 373: the maintainability metric. Communication-based testing requires setting up test dou-
Line 374: bles and interaction assertions, and that takes up a lot of space. Tests become even
Line 375: larger and less maintainable when you have mock chains (mocks or stubs returning
Line 376: other mocks, which also return mocks, and so on, several layers deep). 
Line 377: 6.2.4
Line 378: Comparing the styles: The results
Line 379: Let’s now compare the styles of unit testing using the attributes of a good unit test.
Line 380: Table 6.1 sums up the comparison results. As discussed in section 6.2.1, all three styles
Line 381: score equally with the metrics of protection against regressions and feedback speed;
Line 382: hence, I’m omitting these metrics from the comparison.
Line 383:  Output-based testing shows the best results. This style produces tests that rarely
Line 384: couple to implementation details and thus don’t require much due diligence to main-
Line 385: tain proper resistance to refactoring. Such tests are also the most maintainable due to
Line 386: their conciseness and lack of out-of-process dependencies.
Line 387: Listing 6.6
Line 388: Comment compared by value
Line 389: 
Line 390: --- 페이지 150 ---
Line 391: 128
Line 392: CHAPTER 6
Line 393: Styles of unit testing
Line 394: State-based and communication-based tests are worse on both metrics. These are
Line 395: more likely to couple to a leaking implementation detail, and they also incur higher
Line 396: maintenance costs due to being larger in size.
Line 397:  Always prefer output-based testing over everything else. Unfortunately, it’s easier
Line 398: said than done. This style of unit testing is only applicable to code that is written in a
Line 399: functional way, which is rarely the case for most object-oriented programming lan-
Line 400: guages. Still, there are techniques you can use to transition more of your tests toward
Line 401: the output-based style.
Line 402:  The rest of this chapter shows how to transition from state-based and collaboration-
Line 403: based testing to output-based testing. The transition requires you to make your code
Line 404: more purely functional, which, in turn, enables the use of output-based tests instead
Line 405: of state- or communication-based ones. 
Line 406: 6.3
Line 407: Understanding functional architecture
Line 408: Some groundwork is needed before I can show how to make the transition. In this sec-
Line 409: tion, you’ll see what functional programming and functional architecture are and
Line 410: how the latter relates to the hexagonal architecture. Section 6.4 illustrates the transi-
Line 411: tion using an example.
Line 412:  Note that this isn’t a deep dive into the topic of functional programming, but
Line 413: rather an explanation of the basic principles behind it. These basic principles should
Line 414: be enough to understand the connection between functional programming and out-
Line 415: put-based testing. For a deeper look at functional programming, see Scott Wlaschin’s
Line 416: website and books at https://fsharpforfunandprofit.com/books.
Line 417: 6.3.1
Line 418: What is functional programming?
Line 419: As I mentioned in section 6.1.1, the output-based unit testing style is also known as
Line 420: functional. That’s because it requires the underlying production code to be written in
Line 421: a purely functional way, using functional programming. So, what is functional pro-
Line 422: gramming?
Line 423:  Functional programming is programming with mathematical functions. A mathemati-
Line 424: cal function (also known as pure function) is a function (or method) that doesn’t have
Line 425: any hidden inputs or outputs. All inputs and outputs of a mathematical function must
Line 426: be explicitly expressed in its method signature, which consists of the method’s name,
Line 427: arguments, and return type. A mathematical function produces the same output for a
Line 428: given input regardless of how many times it is called.
Line 429: Table 6.1
Line 430: The three styles of unit testing: The comparisons
Line 431: Output-based
Line 432: State-based
Line 433: Communication-based
Line 434: Due diligence to maintain 
Line 435: resistance to refactoring
Line 436: Low
Line 437: Medium
Line 438: Medium
Line 439: Maintainability costs
Line 440: Low
Line 441: Medium
Line 442: High
Line 443: 
Line 444: --- 페이지 151 ---
Line 445: 129
Line 446: Understanding functional architecture
Line 447:  Let’s take the CalculateDiscount() method from listing 6.1 as an example (I’m
Line 448: copying it here for convenience):
Line 449: public decimal CalculateDiscount(Product[] products)
Line 450: {
Line 451: decimal discount = products.Length * 0.01m;
Line 452: return Math.Min(discount, 0.2m);
Line 453: }
Line 454: This method has one input (a Product array) and one output (the decimal dis-
Line 455: count), both of which are explicitly expressed in the method’s signature. There are
Line 456: no hidden inputs or outputs. This makes CalculateDiscount() a mathematical func-
Line 457: tion (figure 6.5).
Line 458: Methods with no hidden inputs and outputs are called mathematical functions
Line 459: because such methods adhere to the definition of a function in mathematics.
Line 460: DEFINITION
Line 461: In mathematics, a function is a relationship between two sets that
Line 462: for each element in the first set, finds exactly one element in the second set.
Line 463: Figure 6.6 shows how for each input number x, function f(x) = x + 1 finds a corre-
Line 464: sponding number y. Figure 6.7 displays the CalculateDiscount() method using the
Line 465: same notation as in figure 6.6.
Line 466: public         CalculateDiscount
Line 467: decimal
Line 468: (Product[] products)
Line 469: Method signature
Line 470: Output
Line 471: Name
Line 472: Input
Line 473: Figure 6.5
Line 474: CalculateDiscount() has one input (a Product array) and 
Line 475: one output (the decimal discount). Both the input and the output are explicitly 
Line 476: expressed in the method’s signature, which makes CalculateDiscount() 
Line 477: a mathematical function.
Line 478: Y
Line 479: 1
Line 480: 2
Line 481: 3
Line 482: 4
Line 483: 2
Line 484: 3
Line 485: 4
Line 486: 5
Line 487: f(x) = x + 1
Line 488: X
Line 489: Figure 6.6
Line 490: A typical example of a function in 
Line 491: mathematics is f(x) = x + 1. For each input 
Line 492: number x in set X, the function finds a 
Line 493: corresponding number y in set Y.
Line 494: 
Line 495: --- 페이지 152 ---
Line 496: 130
Line 497: CHAPTER 6
Line 498: Styles of unit testing
Line 499: Explicit inputs and outputs make mathematical functions extremely testable because
Line 500: the resulting tests are short, simple, and easy to understand and maintain. Mathe-
Line 501: matical functions are the only type of methods where you can apply output-based
Line 502: testing, which has the best maintainability and the lowest chance of producing a
Line 503: false positive.
Line 504:  On the other hand, hidden inputs and outputs make the code less testable (and
Line 505: less readable, too). Types of such hidden inputs and outputs include the following:
Line 506: Side effects—A side effect is an output that isn’t expressed in the method signature
Line 507: and, therefore, is hidden. An operation creates a side effect when it mutates the
Line 508: state of a class instance, updates a file on the disk, and so on.
Line 509: Exceptions—When a method throws an exception, it creates a path in the pro-
Line 510: gram flow that bypasses the contract established by the method’s signature. The
Line 511: thrown exception can be caught anywhere in the call stack, thus introducing an
Line 512: additional output that the method signature doesn’t convey.
Line 513: A reference to an internal or external state—For example, a method can get the cur-
Line 514: rent date and time using a static property such as DateTime.Now. It can query
Line 515: data from the database, or it can refer to a private mutable field. These are all
Line 516: inputs to the execution flow that aren’t present in the method signature and,
Line 517: therefore, are hidden.
Line 518: A good rule of thumb when determining whether a method is a mathematical func-
Line 519: tion is to see if you can replace a call to that method with its return value without
Line 520: changing the program’s behavior. The ability to replace a method call with the
Line 521: corresponding value is known as referential transparency. Look at the following method,
Line 522: for example:
Line 523: Arrays of products
Line 524: Product(“Soap”)
Line 525: Product(“Hand wash”)
Line 526: Product(“Shampoo”)
Line 527: Product(“Soap”)
Line 528: Product(“Sea salt”)
Line 529: Discounts
Line 530: 0.02
Line 531: 0.01
Line 532: CalculateDiscount()
Line 533: Figure 6.7
Line 534: The CalculateDiscount() method represented using the same 
Line 535: notation as the function f(x) = x + 1. For each input array of products, the 
Line 536: method finds a corresponding discount as an output.
Line 537: 
Line 538: --- 페이지 153 ---
Line 539: 131
Line 540: Understanding functional architecture
Line 541: public int Increment(int x)
Line 542: {
Line 543: return x + 1;
Line 544: }
Line 545: This method is a mathematical function. These two statements are equivalent to
Line 546: each other:
Line 547: int y = Increment(4);
Line 548: int y = 5;
Line 549: On the other hand, the following method is not a mathematical function. You can’t
Line 550: replace it with the return value because that return value doesn’t represent all of the
Line 551: method’s outputs. In this example, the hidden output is the change to field x (a side
Line 552: effect):
Line 553: int x = 0;
Line 554: public int Increment()
Line 555: {
Line 556: x++;
Line 557: return x;
Line 558: }
Line 559: Side effects are the most prevalent type of hidden outputs. The following listing shows
Line 560: an AddComment method that looks like a mathematical function on the surface but
Line 561: actually isn’t one. Figure 6.8 shows the method graphically.
Line 562: public Comment AddComment(string text)
Line 563: {
Line 564: var comment = new Comment(text);
Line 565: _comments.Add(comment);
Line 566:    
Line 567: return comment;
Line 568: }
Line 569: Listing 6.7
Line 570: Modification of an internal state
Line 571: Side effect 
Line 572: Text
Line 573: Comment
Line 574: Side effect
Line 575: Method
Line 576: signature
Line 577: Hidden
Line 578: part
Line 579: f
Line 580: Figure 6.8
Line 581: Method AddComment (shown as f) 
Line 582: has a text input and a Comment output, which 
Line 583: are both expressed in the method signature. The 
Line 584: side effect is an additional hidden output.
Line 585: 
Line 586: --- 페이지 154 ---
Line 587: 132
Line 588: CHAPTER 6
Line 589: Styles of unit testing
Line 590: 6.3.2
Line 591: What is functional architecture?
Line 592: You can’t create an application that doesn’t incur any side effects whatsoever, of
Line 593: course. Such an application would be impractical. After all, side effects are what you
Line 594: create all applications for: updating the user’s information, adding a new order line to
Line 595: the shopping cart, and so on.
Line 596:  The goal of functional programming is not to eliminate side effects altogether but
Line 597: rather to introduce a separation between code that handles business logic and code
Line 598: that incurs side effects. These two responsibilities are complex enough on their own;
Line 599: mixing them together multiplies the complexity and hinders code maintainability in
Line 600: the long run. This is where functional architecture comes into play. It separates busi-
Line 601: ness logic from side effects by pushing those side effects to the edges of a business operation.
Line 602: DEFINITION
Line 603: Functional architecture maximizes the amount of code written in a
Line 604: purely functional (immutable) way, while minimizing code that deals with
Line 605: side effects. Immutable means unchangeable: once an object is created, its
Line 606: state can’t be modified. This is in contrast to a mutable object (changeable
Line 607: object), which can be modified after it is created.
Line 608: The separation between business logic and side effects is done by segregating two
Line 609: types of code:
Line 610: Code that makes a decision—This code doesn’t require side effects and thus can
Line 611: be written using mathematical functions.
Line 612: Code that acts upon that decision—This code converts all the decisions made by
Line 613: the mathematical functions into visible bits, such as changes in the database or
Line 614: messages sent to a bus.
Line 615: The code that makes decisions is often referred to as a functional core (also known as an
Line 616: immutable core). The code that acts upon those decisions is a mutable shell (figure 6.9).
Line 617: Input
Line 618: Decisions
Line 619: Functional core
Line 620: Mutable shell
Line 621: Figure 6.9
Line 622: In functional architecture, 
Line 623: the functional core is implemented using 
Line 624: mathematical functions and makes all 
Line 625: decisions in the application. The mutable 
Line 626: shell provides the functional core with 
Line 627: input data and interprets its decisions by 
Line 628: applying side effects to out-of-process 
Line 629: dependencies such as a database.
Line 630: 
Line 631: --- 페이지 155 ---
Line 632: 133
Line 633: Understanding functional architecture
Line 634: The functional core and the mutable shell cooperate in the following way:
Line 635: The mutable shell gathers all the inputs.
Line 636: The functional core generates decisions.
Line 637: The shell converts the decisions into side effects.
Line 638: To maintain a proper separation between these two layers, you need to make sure the
Line 639: classes representing the decisions contain enough information for the mutable shell
Line 640: to act upon them without additional decision-making. In other words, the mutable
Line 641: shell should be as dumb as possible. The goal is to cover the functional core exten-
Line 642: sively with output-based tests and leave the mutable shell to a much smaller number of
Line 643: integration tests.
Line 644: 6.3.3
Line 645: Comparing functional and hexagonal architectures
Line 646: There are a lot of similarities between functional and hexagonal architectures. Both
Line 647: of them are built around the idea of separation of concerns. The details of that sepa-
Line 648: ration vary, though.
Line 649:  As you may remember from chapter 5, the hexagonal architecture differentiates
Line 650: the domain layer and the application services layer (figure 6.10). The domain layer is
Line 651: accountable for business logic while the application services layer, for communication with
Line 652: Encapsulation and immutability
Line 653: Like encapsulation, functional architecture (in general) and immutability (in particular)
Line 654: serve the same goal as unit testing: enabling sustainable growth of your software
Line 655: project. In fact, there’s a deep connection between the concepts of encapsulation
Line 656: and immutability.
Line 657: As you may remember from chapter 5, encapsulation is the act of protecting your
Line 658: code against inconsistencies. Encapsulation safeguards the class’s internals from
Line 659: corruption by
Line 660: Reducing the API surface area that allows for data modification
Line 661: Putting the remaining APIs under scrutiny
Line 662: Immutability tackles this issue of preserving invariants from another angle. With
Line 663: immutable classes, you don’t need to worry about state corruption because it’s impos-
Line 664: sible to corrupt something that cannot be changed in the first place. As a conse-
Line 665: quence, there’s no need for encapsulation in functional programming. You only need
Line 666: to validate the class’s state once, when you create an instance of it. After that, you
Line 667: can freely pass this instance around. When all your data is immutable, the whole set
Line 668: of issues related to the lack of encapsulation simply vanishes.
Line 669: There’s a great quote from Michael Feathers in that regard:
Line 670: Object-oriented programming makes code understandable by encapsulating mov-
Line 671: ing parts. Functional programming makes code understandable by minimizing
Line 672: moving parts.
Line 673: 
Line 674: --- 페이지 156 ---
Line 675: 134
Line 676: CHAPTER 6
Line 677: Styles of unit testing
Line 678: external applications such as a database or an SMTP service. This is very similar to func-
Line 679: tional architecture, where you introduce the separation of decisions and actions.
Line 680:  Another similarity is the one-way flow of dependencies. In the hexagonal architec-
Line 681: ture, classes inside the domain layer should only depend on each other; they should
Line 682: not depend on classes from the application services layer. Likewise, the immutable
Line 683: core in functional architecture doesn’t depend on the mutable shell. It’s self-sufficient
Line 684: and can work in isolation from the outer layers. This is what makes functional archi-
Line 685: tecture so testable: you can strip the immutable core from the mutable shell entirely
Line 686: and simulate the inputs that the shell provides using simple values.
Line 687:  The difference between the two is in their treatment of side effects. Functional
Line 688: architecture pushes all side effects out of the immutable core to the edges of a busi-
Line 689: ness operation. These edges are handled by the mutable shell. On the other hand, the
Line 690: hexagonal architecture is fine with side effects made by the domain layer, as long as
Line 691: they are limited to that domain layer only. All modifications in hexagonal architecture
Line 692: should be contained within the domain layer and not cross that layer’s boundary. For
Line 693: example, a domain class instance can’t persist something to the database directly, but
Line 694: it can change its own state. An application service will then pick up this change and
Line 695: apply it to the database.
Line 696: NOTE
Line 697: Functional architecture is a subset of the hexagonal architecture. You
Line 698: can view functional architecture as the hexagonal architecture taken to an
Line 699: extreme. 
Line 700: Domain
Line 701: (business logic)
Line 702: Application
Line 703: services
Line 704: Third-party
Line 705: system
Line 706: Message
Line 707: bus
Line 708: SMTP
Line 709: service
Line 710: Figure 6.10
Line 711: Hexagonal architecture is a set of interacting 
Line 712: applications—hexagons. Your application consists of a domain 
Line 713: layer and an application services layer, which correspond to a 
Line 714: functional core and a mutable shell in functional architecture.
Line 715: 
Line 716: --- 페이지 157 ---
Line 717: 135
Line 718: Transitioning to functional architecture and output-based testing
Line 719: 6.4
Line 720: Transitioning to functional architecture and output-
Line 721: based testing
Line 722: In this section, we’ll take a sample application and refactor it toward functional archi-
Line 723: tecture. You’ll see two refactoring stages:
Line 724: Moving from using an out-of-process dependency to using mocks
Line 725: Moving from using mocks to using functional architecture
Line 726: The transition affects test code, too! We’ll refactor state-based and communication-
Line 727: based tests to the output-based style of unit testing. Before starting the refactoring,
Line 728: let’s review the sample project and tests covering it.
Line 729: 6.4.1
Line 730: Introducing an audit system
Line 731: The sample project is an audit system that keeps track of all visitors in an organization.
Line 732: It uses flat text files as underlying storage with the structure shown in figure 6.11. The
Line 733: system appends the visitor’s name and the time of their visit to the end of the most
Line 734: recent file. When the maximum number of entries per file is reached, a new file with
Line 735: an incremented index is created.
Line 736: The following listing shows the initial version of the system.
Line 737: public class AuditManager
Line 738: {
Line 739: private readonly int _maxEntriesPerFile;
Line 740: private readonly string _directoryName;
Line 741: public AuditManager(int maxEntriesPerFile, string directoryName)
Line 742: {
Line 743: _maxEntriesPerFile = maxEntriesPerFile;
Line 744: _directoryName = directoryName;
Line 745: }
Line 746: Listing 6.8
Line 747: Initial implementation of the audit system
Line 748: Jane;
Line 749: Jack;
Line 750: Peter; 2019-04-06T16:30:00
Line 751: 2019-04-06T16:40:00
Line 752: 2019-04-06T17:00:00
Line 753: Mary;
Line 754: 2019-04-06T17:30:00
Line 755: New Person; Time of visit
Line 756: audit_01.txt
Line 757: audit_02.txt
Line 758: Figure 6.11
Line 759: The audit system stores information 
Line 760: about visitors in text files with a specific format. 
Line 761: When the maximum number of entries per file is 
Line 762: reached, the system creates a new file.
Line 763: 
Line 764: --- 페이지 158 ---
Line 765: 136
Line 766: CHAPTER 6
Line 767: Styles of unit testing
Line 768: public void AddRecord(string visitorName, DateTime timeOfVisit)
Line 769: {
Line 770: string[] filePaths = Directory.GetFiles(_directoryName);
Line 771: (int index, string path)[] sorted = SortByIndex(filePaths);
Line 772: string newRecord = visitorName + ';' + timeOfVisit;
Line 773: if (sorted.Length == 0)
Line 774: {
Line 775: string newFile = Path.Combine(_directoryName, "audit_1.txt");
Line 776: File.WriteAllText(newFile, newRecord);
Line 777: return;
Line 778: }
Line 779: (int currentFileIndex, string currentFilePath) = sorted.Last();
Line 780: List<string> lines = File.ReadAllLines(currentFilePath).ToList();
Line 781: if (lines.Count < _maxEntriesPerFile)
Line 782: {
Line 783: lines.Add(newRecord);
Line 784: string newContent = string.Join("\r\n", lines);
Line 785: File.WriteAllText(currentFilePath, newContent);
Line 786: }
Line 787: else
Line 788: {
Line 789: int newIndex = currentFileIndex + 1;
Line 790: string newName = $"audit_{newIndex}.txt";
Line 791: string newFile = Path.Combine(_directoryName, newName);
Line 792: File.WriteAllText(newFile, newRecord);
Line 793: }
Line 794: }
Line 795: }
Line 796: The code might look a bit large, but it’s quite simple. AuditManager is the main class
Line 797: in the application. Its constructor accepts the maximum number of entries per file
Line 798: and the working directory as configuration parameters. The only public method in
Line 799: the class is AddRecord, which does all the work of the audit system:
Line 800: Retrieves a full list of files from the working directory
Line 801: Sorts them by index (all filenames follow the same pattern: audit_{index}.txt
Line 802: [for example, audit_1.txt])
Line 803: If there are no audit files yet, creates a first one with a single record
Line 804: If there are audit files, gets the most recent one and either appends the new
Line 805: record to it or creates a new file, depending on whether the number of entries
Line 806: in that file has reached the limit
Line 807: The AuditManager class is hard to test as-is, because it’s tightly coupled to the file-
Line 808: system. Before the test, you’d need to put files in the right place, and after the test
Line 809: finishes, you’d read those files, check their contents, and clear them out (figure 6.12).
Line 810: 
Line 811: --- 페이지 159 ---
Line 812: 137
Line 813: Transitioning to functional architecture and output-based testing
Line 814: You won’t be able to parallelize such tests—at least, not without additional effort
Line 815: that would significantly increase maintenance costs. The bottleneck is the filesys-
Line 816: tem: it’s a shared dependency through which tests can interfere with each other’s
Line 817: execution flow.
Line 818:  The filesystem also makes the tests slow. Maintainability suffers, too, because you
Line 819: have to make sure the working directory exists and is accessible to tests—both on your
Line 820: local machine and on the build server. Table 6.2 sums up the scoring.
Line 821: By the way, tests working directly with the filesystem don’t fit the definition of a unit
Line 822: test. They don’t comply with the second and the third attributes of a unit test, thereby
Line 823: falling into the category of integration tests (see chapter 2 for more details):
Line 824: A unit test verifies a single unit of behavior,
Line 825: Does it quickly,
Line 826: And does it in isolation from other tests. 
Line 827: 6.4.2
Line 828: Using mocks to decouple tests from the filesystem
Line 829: The usual solution to the problem of tightly coupled tests is to mock the filesystem.
Line 830: You can extract all operations on files into a separate class (IFileSystem) and inject
Line 831: that class into AuditManager via the constructor. The tests will then mock this class
Line 832: and capture the writes the audit system do to the files (figure 6.13).
Line 833:  
Line 834:  
Line 835:  
Line 836: Table 6.2
Line 837: The initial version of the audit system scores badly on two out 
Line 838: of the four attributes of a good test.
Line 839: Initial version
Line 840: Protection against regressions
Line 841: Good
Line 842: Resistance to refactoring
Line 843: Good
Line 844: Fast feedback
Line 845: Bad
Line 846: Maintainability
Line 847: Bad
Line 848: Audit system
Line 849: Filesystem
Line 850: Test
Line 851: input
Line 852: input
Line 853: input
Line 854: output
Line 855: assert
Line 856: Figure 6.12
Line 857: Tests covering the initial version of the audit system would 
Line 858: have to work directly with the filesystem.
Line 859: 
Line 860: --- 페이지 160 ---
Line 861: 138
Line 862: CHAPTER 6
Line 863: Styles of unit testing
Line 864: The following listing shows how the filesystem is injected into AuditManager.
Line 865: public class AuditManager
Line 866: {
Line 867: private readonly int _maxEntriesPerFile;
Line 868: private readonly string _directoryName;
Line 869: private readonly IFileSystem _fileSystem;    
Line 870: public AuditManager(
Line 871: int maxEntriesPerFile,
Line 872: string directoryName,
Line 873: IFileSystem fileSystem)
Line 874: {
Line 875: _maxEntriesPerFile = maxEntriesPerFile;
Line 876: _directoryName = directoryName;
Line 877: _fileSystem = fileSystem;                
Line 878: }
Line 879: }
Line 880: And next is the AddRecord method.
Line 881: public void AddRecord(string visitorName, DateTime timeOfVisit)
Line 882: {
Line 883: string[] filePaths = _fileSystem                                
Line 884: .GetFiles(_directoryName);                                  
Line 885: (int index, string path)[] sorted = SortByIndex(filePaths);
Line 886: string newRecord = visitorName + ';' + timeOfVisit;
Line 887: if (sorted.Length == 0)
Line 888: {
Line 889: string newFile = Path.Combine(_directoryName, "audit_1.txt");
Line 890: _fileSystem.WriteAllText(                                   
Line 891: newFile, newRecord);                                    
Line 892: return;
Line 893: }
Line 894: Listing 6.9
Line 895: Injecting the filesystem explicitly via the constructor
Line 896: Listing 6.10
Line 897: Using the new IFileSystem interface
Line 898: mock
Line 899: stub
Line 900: input
Line 901: Audit system
Line 902: Test
Line 903: Filesystem
Line 904: Figure 6.13
Line 905: Tests can mock the 
Line 906: filesystem and capture the writes 
Line 907: the audit system makes to the files.
Line 908: The new interface 
Line 909: represents the 
Line 910: filesystem.
Line 911: The new
Line 912: interface
Line 913: in action
Line 914: 
Line 915: --- 페이지 161 ---
Line 916: 139
Line 917: Transitioning to functional architecture and output-based testing
Line 918: (int currentFileIndex, string currentFilePath) = sorted.Last();
Line 919: List<string> lines = _fileSystem
Line 920:           
Line 921: .ReadAllLines(currentFilePath);          
Line 922: if (lines.Count < _maxEntriesPerFile)
Line 923: {
Line 924: lines.Add(newRecord);
Line 925: string newContent = string.Join("\r\n", lines);
Line 926: _fileSystem.WriteAllText(
Line 927:         
Line 928: currentFilePath, newContent);        
Line 929: }
Line 930: else
Line 931: {
Line 932: int newIndex = currentFileIndex + 1;
Line 933: string newName = $"audit_{newIndex}.txt";
Line 934: string newFile = Path.Combine(_directoryName, newName);
Line 935: _fileSystem.WriteAllText(                
Line 936: newFile, newRecord);                 
Line 937: }
Line 938: }
Line 939: In listing 6.10, IFileSystem is a new custom interface that encapsulates the work with
Line 940: the filesystem:
Line 941: public interface IFileSystem
Line 942: {
Line 943: string[] GetFiles(string directoryName);
Line 944: void WriteAllText(string filePath, string content);
Line 945: List<string> ReadAllLines(string filePath);
Line 946: }
Line 947: Now that AuditManager is decoupled from the filesystem, the shared dependency is
Line 948: gone, and tests can execute independently from each other. Here’s one such test.
Line 949: [Fact]
Line 950: public void A_new_file_is_created_when_the_current_file_overflows()
Line 951: {
Line 952: var fileSystemMock = new Mock<IFileSystem>();
Line 953: fileSystemMock
Line 954: .Setup(x => x.GetFiles("audits"))
Line 955: .Returns(new string[]
Line 956: {
Line 957: @"audits\audit_1.txt",
Line 958: @"audits\audit_2.txt"
Line 959: });
Line 960: fileSystemMock
Line 961: .Setup(x => x.ReadAllLines(@"audits\audit_2.txt"))
Line 962: .Returns(new List<string>
Line 963: {
Line 964: "Peter; 2019-04-06T16:30:00",
Line 965: "Jane; 2019-04-06T16:40:00",
Line 966: Listing 6.11
Line 967: Checking the audit system’s behavior using a mock
Line 968: The new
Line 969: interface
Line 970: in action
Line 971: 
Line 972: --- 페이지 162 ---
Line 973: 140
Line 974: CHAPTER 6
Line 975: Styles of unit testing
Line 976: "Jack; 2019-04-06T17:00:00"
Line 977: });
Line 978: var sut = new AuditManager(3, "audits", fileSystemMock.Object);
Line 979: sut.AddRecord("Alice", DateTime.Parse("2019-04-06T18:00:00"));
Line 980: fileSystemMock.Verify(x => x.WriteAllText(
Line 981: @"audits\audit_3.txt",
Line 982: "Alice;2019-04-06T18:00:00"));
Line 983: }
Line 984: This test verifies that when the number of entries in the current file reaches the limit
Line 985: (3, in this example), a new file with a single audit entry is created. Note that this is a
Line 986: legitimate use of mocks. The application creates files that are visible to end users
Line 987: (assuming that those users use another program to read the files, be it specialized soft-
Line 988: ware or a simple notepad.exe). Therefore, communications with the filesystem and
Line 989: the side effects of these communications (that is, the changes in files) are part of the
Line 990: application’s observable behavior. As you may remember from chapter 5, that’s the
Line 991: only legitimate use case for mocking.
Line 992:  This alternative implementation is an improvement over the initial version. Since
Line 993: tests no longer access the filesystem, they execute faster. And because you don’t need
Line 994: to look after the filesystem to keep the tests happy, the maintenance costs are also
Line 995: reduced. Protection against regressions and resistance to refactoring didn’t suffer
Line 996: from the refactoring either. Table 6.3 shows the differences between the two versions.
Line 997: We can still do better, though. The test in listing 6.11 contains convoluted setups,
Line 998: which is less than ideal in terms of maintenance costs. Mocking libraries try their best
Line 999: to be helpful, but the resulting tests are still not as readable as those that rely on plain
Line 1000: input and output. 
Line 1001: 6.4.3
Line 1002: Refactoring toward functional architecture
Line 1003: Instead of hiding side effects behind an interface and injecting that interface into
Line 1004: AuditManager, you can move those side effects out of the class entirely. Audit-
Line 1005: Manager is then only responsible for making a decision about what to do with the
Line 1006: files. A new class, Persister, acts on that decision and applies updates to the filesys-
Line 1007: tem (figure 6.14).
Line 1008: Table 6.3
Line 1009: The version with mocks compared to the initial version of the audit system
Line 1010: Initial version
Line 1011: With mocks
Line 1012: Protection against regressions
Line 1013: Good
Line 1014: Good
Line 1015: Resistance to refactoring
Line 1016: Good
Line 1017: Good
Line 1018: Fast feedback
Line 1019: Bad
Line 1020: Good
Line 1021: Maintainability
Line 1022: Bad
Line 1023: Moderate
Line 1024: 
Line 1025: --- 페이지 163 ---
Line 1026: 141
Line 1027: Transitioning to functional architecture and output-based testing
Line 1028: Persister in this scenario acts as a mutable shell, while AuditManager becomes a func-
Line 1029: tional (immutable) core. The following listing shows AuditManager after the refactoring.
Line 1030: public class AuditManager
Line 1031: {
Line 1032: private readonly int _maxEntriesPerFile;
Line 1033: public AuditManager(int maxEntriesPerFile)
Line 1034: {
Line 1035: _maxEntriesPerFile = maxEntriesPerFile;
Line 1036: }
Line 1037: public FileUpdate AddRecord(
Line 1038: FileContent[] files,
Line 1039: string visitorName,
Line 1040: DateTime timeOfVisit)
Line 1041: {
Line 1042: (int index, FileContent file)[] sorted = SortByIndex(files);
Line 1043: string newRecord = visitorName + ';' + timeOfVisit;
Line 1044: if (sorted.Length == 0)
Line 1045: {
Line 1046: return new FileUpdate(
Line 1047:   
Line 1048: "audit_1.txt", newRecord);  
Line 1049: }
Line 1050: (int currentFileIndex, FileContent currentFile) = sorted.Last();
Line 1051: List<string> lines = currentFile.Lines.ToList();
Line 1052: Listing 6.12
Line 1053: The AuditManager class after refactoring
Line 1054: FileContent
Line 1055: FileUpdate
Line 1056: AuditManager
Line 1057: (functional core)
Line 1058: Persister
Line 1059: (mutable shell)
Line 1060: Figure 6.14
Line 1061: Persister and 
Line 1062: AuditManager form the functional 
Line 1063: architecture. Persister gathers files 
Line 1064: and their contents from the working 
Line 1065: directory, feeds them to AuditManager, 
Line 1066: and then converts the return value into 
Line 1067: changes in the filesystem.
Line 1068: Returns an update 
Line 1069: instruction
Line 1070: 
Line 1071: --- 페이지 164 ---
Line 1072: 142
Line 1073: CHAPTER 6
Line 1074: Styles of unit testing
Line 1075: if (lines.Count < _maxEntriesPerFile)
Line 1076: {
Line 1077: lines.Add(newRecord);
Line 1078: string newContent = string.Join("\r\n", lines);
Line 1079: return new FileUpdate(
Line 1080:      
Line 1081: currentFile.FileName, newContent);     
Line 1082: }
Line 1083: else
Line 1084: {
Line 1085: int newIndex = currentFileIndex + 1;
Line 1086: string newName = $"audit_{newIndex}.txt";
Line 1087: return new FileUpdate(
Line 1088:                    
Line 1089: newName, newRecord);                   
Line 1090: }
Line 1091: }
Line 1092: }
Line 1093: Instead of the working directory path, AuditManager now accepts an array of File-
Line 1094: Content. This class includes everything AuditManager needs to know about the filesys-
Line 1095: tem to make a decision:
Line 1096: public class FileContent
Line 1097: {
Line 1098: public readonly string FileName;
Line 1099: public readonly string[] Lines;
Line 1100: public FileContent(string fileName, string[] lines)
Line 1101: {
Line 1102: FileName = fileName;
Line 1103: Lines = lines;
Line 1104: }
Line 1105: }
Line 1106: And, instead of mutating files in the working directory, AuditManager now returns an
Line 1107: instruction for the side effect it would like to perform:
Line 1108: public class FileUpdate
Line 1109: {
Line 1110: public readonly string FileName;
Line 1111: public readonly string NewContent;
Line 1112: public FileUpdate(string fileName, string newContent)
Line 1113: {
Line 1114: FileName = fileName;
Line 1115: NewContent = newContent;
Line 1116: }
Line 1117: }
Line 1118: The following listing shows the Persister class.
Line 1119:  
Line 1120:  
Line 1121: Returns an 
Line 1122: update 
Line 1123: instruction
Line 1124: 
Line 1125: --- 페이지 165 ---
Line 1126: 143
Line 1127: Transitioning to functional architecture and output-based testing
Line 1128: public class Persister
Line 1129: {
Line 1130: public FileContent[] ReadDirectory(string directoryName)
Line 1131: {
Line 1132: return Directory
Line 1133: .GetFiles(directoryName)
Line 1134: .Select(x => new FileContent(
Line 1135: Path.GetFileName(x),
Line 1136: File.ReadAllLines(x)))
Line 1137: .ToArray();
Line 1138: }
Line 1139: public void ApplyUpdate(string directoryName, FileUpdate update)
Line 1140: {
Line 1141: string filePath = Path.Combine(directoryName, update.FileName);
Line 1142: File.WriteAllText(filePath, update.NewContent);
Line 1143: }
Line 1144: }
Line 1145: Notice how trivial this class is. All it does is read content from the working directory
Line 1146: and apply updates it receives from AuditManager back to that working directory. It has
Line 1147: no branching (no if statements); all the complexity resides in the AuditManager
Line 1148: class. This is the separation between business logic and side effects in action.
Line 1149:  To maintain such a separation, you need to keep the interface of FileContent and
Line 1150: FileUpdate as close as possible to that of the framework’s built-in file-interaction com-
Line 1151: mands. All the parsing and preparation should be done in the functional core, so that
Line 1152: the code outside of that core remains trivial. For example, if .NET didn’t contain the
Line 1153: built-in File.ReadAllLines() method, which returns the file content as an array of
Line 1154: lines, and only has File.ReadAllText(), which returns a single string, you’d need to
Line 1155: replace the Lines property in FileContent with a string too and do the parsing in
Line 1156: AuditManager:
Line 1157: public class FileContent
Line 1158: {
Line 1159: public readonly string FileName;
Line 1160: public readonly string Text; // previously, string[] Lines;
Line 1161: }
Line 1162: To glue AuditManager and Persister together, you need another class: an applica-
Line 1163: tion service in the hexagonal architecture taxonomy, as shown in the following listing.
Line 1164: public class ApplicationService
Line 1165: {
Line 1166: private readonly string _directoryName;
Line 1167: private readonly AuditManager _auditManager;
Line 1168: private readonly Persister _persister;
Line 1169: Listing 6.13
Line 1170: The mutable shell acting on AuditManager’s decision
Line 1171: Listing 6.14
Line 1172: Gluing together the functional core and mutable shell 
Line 1173: 
Line 1174: --- 페이지 166 ---
Line 1175: 144
Line 1176: CHAPTER 6
Line 1177: Styles of unit testing
Line 1178: public ApplicationService(
Line 1179: string directoryName, int maxEntriesPerFile)
Line 1180: {
Line 1181: _directoryName = directoryName;
Line 1182: _auditManager = new AuditManager(maxEntriesPerFile);
Line 1183: _persister = new Persister();
Line 1184: }
Line 1185: public void AddRecord(string visitorName, DateTime timeOfVisit)
Line 1186: {
Line 1187: FileContent[] files = _persister.ReadDirectory(_directoryName);
Line 1188: FileUpdate update = _auditManager.AddRecord(
Line 1189: files, visitorName, timeOfVisit);
Line 1190: _persister.ApplyUpdate(_directoryName, update);
Line 1191: }
Line 1192: }
Line 1193: Along with gluing the functional core together with the mutable shell, the application
Line 1194: service also provides an entry point to the system for external clients (figure 6.15).
Line 1195: With this implementation, it becomes easy to check the audit system’s behavior. All
Line 1196: tests now boil down to supplying a hypothetical state of the working directory and ver-
Line 1197: ifying the decision AuditManager makes.
Line 1198: [Fact]
Line 1199: public void A_new_file_is_created_when_the_current_file_overflows()
Line 1200: {
Line 1201: var sut = new AuditManager(3);
Line 1202: var files = new FileContent[]
Line 1203: {
Line 1204: new FileContent("audit_1.txt", new string[0]),
Line 1205: Listing 6.15
Line 1206: The test without mocks
Line 1207: Audit manager
Line 1208: Persister
Line 1209: Persister
Line 1210: Application service
Line 1211: External client
Line 1212: Figure 6.15
Line 1213: ApplicationService glues the functional core (AuditManager) 
Line 1214: and the mutable shell (Persister) together and provides an entry point for external 
Line 1215: clients. In the hexagonal architecture taxonomy, ApplicationService and 
Line 1216: Persister are part of the application services layer, while AuditManager 
Line 1217: belongs to the domain model.
Line 1218: 
Line 1219: --- 페이지 167 ---
Line 1220: 145
Line 1221: Transitioning to functional architecture and output-based testing
Line 1222: new FileContent("audit_2.txt", new string[]
Line 1223: {
Line 1224: "Peter; 2019-04-06T16:30:00",
Line 1225: "Jane; 2019-04-06T16:40:00",
Line 1226: "Jack; 2019-04-06T17:00:00"
Line 1227: })
Line 1228: };
Line 1229: FileUpdate update = sut.AddRecord(
Line 1230: files, "Alice", DateTime.Parse("2019-04-06T18:00:00"));
Line 1231: Assert.Equal("audit_3.txt", update.FileName);
Line 1232: Assert.Equal("Alice;2019-04-06T18:00:00", update.NewContent);
Line 1233: }
Line 1234: This test retains the improvement the test with mocks made over the initial version
Line 1235: (fast feedback) but also further improves on the maintainability metric. There’s no
Line 1236: need for complex mock setups anymore, only plain inputs and outputs, which helps
Line 1237: the test’s readability a lot. Table 6.4 compares the output-based test with the initial ver-
Line 1238: sion and the version with mocks.
Line 1239: Notice that the instructions generated by a functional core are always a value or a set of
Line 1240: values. Two instances of such a value are interchangeable as long as their contents
Line 1241: match. You can take advantage of this fact and improve test readability even further by
Line 1242: turning FileUpdate into a value object. To do that in .NET, you need to either convert
Line 1243: the class into a struct or define custom equality members. That will give you compar-
Line 1244: ison by value, as opposed to the comparison by reference, which is the default behavior
Line 1245: for classes in C#. Comparison by value also allows you to compress the two assertions
Line 1246: from listing 6.15 into one:
Line 1247: Assert.Equal(
Line 1248: new FileUpdate("audit_3.txt", "Alice;2019-04-06T18:00:00"),
Line 1249: update);
Line 1250: Or, using Fluent Assertions,
Line 1251: update.Should().Be(
Line 1252: new FileUpdate("audit_3.txt", "Alice;2019-04-06T18:00:00"));
Line 1253: Table 6.4
Line 1254: The output-based test compared to the previous two versions
Line 1255: Initial version
Line 1256: With mocks
Line 1257: Output-based
Line 1258: Protection against regressions
Line 1259: Good
Line 1260: Good
Line 1261: Good
Line 1262: Resistance to refactoring
Line 1263: Good
Line 1264: Good
Line 1265: Good
Line 1266: Fast feedback
Line 1267: Bad
Line 1268: Good
Line 1269: Good
Line 1270: Maintainability
Line 1271: Bad
Line 1272: Moderate
Line 1273: Good
Line 1274: 
Line 1275: --- 페이지 168 ---
Line 1276: 146
Line 1277: CHAPTER 6
Line 1278: Styles of unit testing
Line 1279: 6.4.4
Line 1280: Looking forward to further developments
Line 1281: Let’s step back for a minute and look at further developments that could be done in
Line 1282: our sample project. The audit system I showed you is quite simple and contains only
Line 1283: three branches:
Line 1284: Creating a new file in case of an empty working directory
Line 1285: Appending a new record to an existing file
Line 1286: Creating another file when the number of entries in the current file exceeds
Line 1287: the limit
Line 1288: Also, there’s only one use case: addition of a new entry to the audit log. What if
Line 1289: there were another use case, such as deleting all mentions of a particular visitor?
Line 1290: And what if the system needed to do validations (say, for the maximum length of the
Line 1291: visitor’s name)?
Line 1292:  Deleting all mentions of a particular visitor could potentially affect several files, so
Line 1293: the new method would need to return multiple file instructions:
Line 1294: public FileUpdate[] DeleteAllMentions(
Line 1295: FileContent[] files, string visitorName)
Line 1296: Furthermore, business people might require that you not keep empty files in the
Line 1297: working directory. If the deleted entry was the last entry in an audit file, you would
Line 1298: need to remove that file altogether. To implement this requirement, you could
Line 1299: rename FileUpdate to FileAction and introduce an additional ActionType enum
Line 1300: field to indicate whether it was an update or a deletion.
Line 1301:  Error handling also becomes simpler and more explicit with functional architec-
Line 1302: ture. You could embed errors into the method’s signature, either in the FileUpdate
Line 1303: class or as a separate component:
Line 1304: public (FileUpdate update, Error error) AddRecord(
Line 1305: FileContent[] files,
Line 1306: string visitorName,
Line 1307: DateTime timeOfVisit)
Line 1308: The application service would then check for this error. If it was there, the service
Line 1309: wouldn’t pass the update instruction to the persister, instead propagating an error
Line 1310: message to the user. 
Line 1311: 6.5
Line 1312: Understanding the drawbacks of functional 
Line 1313: architecture
Line 1314: Unfortunately, functional architecture isn’t always attainable. And even when it is, the
Line 1315: maintainability benefits are often offset by a performance impact and increase in
Line 1316: the size of the code base. In this section, we’ll explore the costs and the trade-offs
Line 1317: attached to functional architecture.
Line 1318: 
Line 1319: --- 페이지 169 ---
Line 1320: 147
Line 1321: Understanding the drawbacks of functional architecture
Line 1322: 6.5.1
Line 1323: Applicability of functional architecture
Line 1324: Functional architecture worked for our audit system because this system could gather
Line 1325: all the inputs up front, before making a decision. Often, though, the execution flow is
Line 1326: less straightforward. You might need to query additional data from an out-of-process
Line 1327: dependency, based on an intermediate result of the decision-making process.
Line 1328:  Here’s an example. Let’s say the audit system needs to check the visitor’s access
Line 1329: level if the number of times they have visited during the last 24 hours exceeds some
Line 1330: threshold. And let’s also assume that all visitors’ access levels are stored in a database.
Line 1331: You can’t pass an IDatabase instance to AuditManager like this:
Line 1332: public FileUpdate AddRecord(
Line 1333: FileContent[] files, string visitorName,
Line 1334: DateTime timeOfVisit, IDatabase database
Line 1335: )
Line 1336: Such an instance would introduce a hidden input to the AddRecord() method. This
Line 1337: method would, therefore, cease to be a mathematical function (figure 6.16), which
Line 1338: means you would no longer be able to apply output-based testing.
Line 1339: There are two solutions in such a situation:
Line 1340: You can gather the visitor’s access level in the application service up front,
Line 1341: along with the directory content.
Line 1342: You can introduce a new method such as IsAccessLevelCheckRequired() in
Line 1343: AuditManager. The application service would call this method before Add-
Line 1344: Record(), and if it returned true, the service would get the access level from
Line 1345: the database and pass it to AddRecord().
Line 1346: Both approaches have drawbacks. The first one concedes performance—it uncondi-
Line 1347: tionally queries the database, even in cases when the access level is not required. But this
Line 1348: approach keeps the separation of business logic and communication with external
Line 1349: Application
Line 1350: service
Line 1351: ReadDirectory
Line 1352: Audit manager
Line 1353: Filesystem
Line 1354: and database
Line 1355: Add
Line 1356: record
Line 1357: ApplyUpdate
Line 1358: Get
Line 1359: access
Line 1360: level
Line 1361: Figure 6.16
Line 1362: A dependency on the database introduces a hidden input to 
Line 1363: AuditManager. Such a class is no longer purely functional, and the whole 
Line 1364: application no longer follows the functional architecture.
Line 1365: 
Line 1366: --- 페이지 170 ---
Line 1367: 148
Line 1368: CHAPTER 6
Line 1369: Styles of unit testing
Line 1370: systems fully intact: all decision-making resides in AuditManager as before. The second
Line 1371: approach concedes a degree of that separation for performance gains: the decision as
Line 1372: to whether to call the database now goes to the application service, not AuditManager.
Line 1373:  Note that, unlike these two options, making the domain model (AuditManager)
Line 1374: depend on the database isn’t a good idea. I’ll explain more about keeping the balance
Line 1375: between performance and separation of concerns in the next two chapters.
Line 1376: NOTE
Line 1377: A class from the functional core should work not with a collaborator,
Line 1378: but with the product of its work, a value. 
Line 1379: 6.5.2
Line 1380: Performance drawbacks
Line 1381: The performance impact on the system as a whole is a common argument against
Line 1382: functional architecture. Note that it’s not the performance of tests that suffers. The
Line 1383: output-based tests we ended up with work as fast as the tests with mocks. It’s that the
Line 1384: system itself now has to do more calls to out-of-process dependencies and becomes
Line 1385: less performant. The initial version of the audit system didn’t read all files from the
Line 1386: working directory, and neither did the version with mocks. But the final version does
Line 1387: in order to comply with the read-decide-act approach.
Line 1388:  The choice between a functional architecture and a more traditional one is a
Line 1389: trade-off between performance and code maintainability (both production and test
Line 1390: code). In some systems where the performance impact is not as noticeable, it’s better
Line 1391: to go with functional architecture for additional gains in maintainability. In others,
Line 1392: you might need to make the opposite choice. There’s no one-size-fits-all solution. 
Line 1393: Collaborators vs. values
Line 1394: You may have noticed that AuditManager’s AddRecord() method has a dependency
Line 1395: that’s not present in its signature: the _maxEntriesPerFile field. The audit man-
Line 1396: ager refers to this field to make a decision to either append an existing audit file or
Line 1397: create a new one.
Line 1398: Although this dependency isn’t present among the method’s arguments, it’s not hid-
Line 1399: den. It can be derived from the class’s constructor signature. And because the _max-
Line 1400: EntriesPerFile field is immutable, it stays the same between the class instantiation
Line 1401: and the call to AddRecord(). In other words, that field is a value.
Line 1402: The situation with the IDatabase dependency is different because it’s a collaborator,
Line 1403: not a value like _maxEntriesPerFile. As you may remember from chapter 2, a col-
Line 1404: laborator is a dependency that is one or the other of the following:
Line 1405: Mutable (allows for modification of its state)
Line 1406: A proxy to data that is not yet in memory (a shared dependency)
Line 1407: The IDatabase instance falls into the second category and, therefore, is a collabo-
Line 1408: rator. It requires an additional call to an out-of-process dependency and thus pre-
Line 1409: cludes the use of output-based testing.
Line 1410: 
Line 1411: --- 페이지 171 ---
Line 1412: 149
Line 1413: Summary
Line 1414: 6.5.3
Line 1415: Increase in the code base size
Line 1416: The same is true for the size of the code base. Functional architecture requires a clear
Line 1417: separation between the functional (immutable) core and the mutable shell. This
Line 1418: necessitates additional coding initially, although it ultimately results in reduced code
Line 1419: complexity and gains in maintainability.
Line 1420:  Not all projects exhibit a high enough degree of complexity to justify such an initial
Line 1421: investment, though. Some code bases aren’t that significant from a business perspec-
Line 1422: tive or are just plain too simple. It doesn’t make sense to use functional architecture
Line 1423: in such projects because the initial investment will never pay off. Always apply func-
Line 1424: tional architecture strategically, taking into account the complexity and importance of
Line 1425: your system.
Line 1426:  Finally, don’t go for purity of the functional approach if that purity comes at too
Line 1427: high a cost. In most projects, you won’t be able to make the domain model fully
Line 1428: immutable and thus can’t rely solely on output-based tests, at least not when using an
Line 1429: OOP language like C# or Java. In most cases, you’ll have a combination of output-
Line 1430: based and state-based styles, with a small mix of communication-based tests, and that’s
Line 1431: fine. The goal of this chapter is not to incite you to transition all your tests toward the
Line 1432: output-based style; the goal is to transition as many of them as reasonably possible.
Line 1433: The difference is subtle but important. 
Line 1434: Summary
Line 1435: Output-based testing is a style of testing where you feed an input to the SUT and
Line 1436: check the output it produces. This style of testing assumes there are no hidden
Line 1437: inputs or outputs, and the only result of the SUT’s work is the value it returns.
Line 1438: State-based testing verifies the state of the system after an operation is completed.
Line 1439: In communication-based testing, you use mocks to verify communications between
Line 1440: the system under test and its collaborators.
Line 1441: The classical school of unit testing prefers the state-based style over the
Line 1442: communication-based one. The London school has the opposite preference.
Line 1443: Both schools use output-based testing.
Line 1444: Output-based testing produces tests of the highest quality. Such tests rarely cou-
Line 1445: ple to implementation details and thus are resistant to refactoring. They are
Line 1446: also small and concise and thus are more maintainable.
Line 1447: State-based testing requires extra prudence to avoid brittleness: you need to
Line 1448: make sure you don’t expose a private state to enable unit testing. Because state-
Line 1449: based tests tend to be larger than output-based tests, they are also less maintain-
Line 1450: able. Maintainability issues can sometimes be mitigated (but not eliminated)
Line 1451: with the use of helper methods and value objects.
Line 1452: Communication-based testing also requires extra prudence to avoid brittle-
Line 1453: ness. You should only verify communications that cross the application bound-
Line 1454: ary and whose side effects are visible to the external world. Maintainability of
Line 1455: 
Line 1456: --- 페이지 172 ---
Line 1457: 150
Line 1458: CHAPTER 6
Line 1459: Styles of unit testing
Line 1460: communication-based tests is worse compared to output-based and state-based
Line 1461: tests. Mocks tend to occupy a lot of space, and that makes tests less readable.
Line 1462: Functional programming is programming with mathematical functions.
Line 1463: A mathematical function is a function (or method) that doesn’t have any hidden
Line 1464: inputs or outputs. Side effects and exceptions are hidden outputs. A reference
Line 1465: to an internal or external state is a hidden input. Mathematical functions are
Line 1466: explicit, which makes them extremely testable.
Line 1467: The goal of functional programming is to introduce a separation between busi-
Line 1468: ness logic and side effects.
Line 1469: Functional architecture helps achieve that separation by pushing side effects
Line 1470: to the edges of a business operation. This approach maximizes the amount of
Line 1471: code written in a purely functional way while minimizing code that deals with
Line 1472: side effects.
Line 1473: Functional architecture divides all code into two categories: functional core
Line 1474: and mutable shell. The functional core makes decisions. The mutable shell supplies
Line 1475: input data to the functional core and converts decisions the core makes into
Line 1476: side effects.
Line 1477: The difference between functional and hexagonal architectures is in their treat-
Line 1478: ment of side effects. Functional architecture pushes all side effects out of the
Line 1479: domain layer. Conversely, hexagonal architecture is fine with side effects made
Line 1480: by the domain layer, as long as they are limited to that domain layer only. Func-
Line 1481: tional architecture is hexagonal architecture taken to an extreme.
Line 1482: The choice between a functional architecture and a more traditional one is a
Line 1483: trade-off between performance and code maintainability. Functional architec-
Line 1484: ture concedes performance for maintainability gains.
Line 1485: Not all code bases are worth converting into functional architecture. Apply
Line 1486: functional architecture strategically. Take into account the complexity and the
Line 1487: importance of your system. In code bases that are simple or not that important,
Line 1488: the initial investment required for functional architecture won’t pay off.