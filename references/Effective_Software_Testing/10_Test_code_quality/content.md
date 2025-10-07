Line 1: 
Line 2: --- 페이지 286 ---
Line 3: 258
Line 4: Test code quality
Line 5: You have probably noticed that once test infected, the number of JUnit tests a soft-
Line 6: ware development team writes and maintains can become significant. In practice,
Line 7: test code bases grow quickly. Moreover, we have observed that Lehman’s law of evo-
Line 8: lution, “Code tends to rot, unless one actively works against it” (1980), also applies
Line 9: to test code. A 2018 literature review by Garousi and Küçük shows that our body of
Line 10: knowledge about things that can go wrong with test code is already comprehensive.
Line 11:  As with production code, we must put extra effort into writing high-quality test code
Line 12: bases so they can be maintained and developed sustainably. In this chapter, I discuss two
Line 13: opposite perspectives of writing test code. First, we examine what constitutes good
Line 14: and maintainable test code, and best practices that can help you keep complexity
Line 15: under control. Then we look at what constitutes problematic test code. We focus on
Line 16: key test smells that hinder test code comprehension and evolution.
Line 17:  I have discussed some of this material informally in previous chapters. This
Line 18: chapter consolidates that knowledge.
Line 19: This chapter covers
Line 20: Principles and best practices of good and 
Line 21: maintainable test code
Line 22: Avoiding test smells that hinder the 
Line 23: comprehension and evolution of test code
Line 24: 
Line 25: --- 페이지 287 ---
Line 26: 259
Line 27: Principles of maintainable test code
Line 28: 10.1
Line 29: Principles of maintainable test code
Line 30: What does good test code look like? There is a great deal of literature about test code
Line 31: quality, which I rely on in this section. Much of what I say here can be found in the
Line 32: works of Langr, Hunt, and Thomas (2015); Meszaros (2007); and Beck (2019)—as
Line 33: always, with my own twist.
Line 34: 10.1.1
Line 35: Tests should be fast
Line 36: Tests are a developer’s safety net. Whenever we perform maintenance or evolution in
Line 37: source code, we use the feedback from the test suite to understand whether the system
Line 38: is working as expected. The faster we get feedback from the test code, the better.
Line 39: Slower test suites force us to run the tests less often, making them less effective. There-
Line 40: fore, good tests are fast. There is no hard line that separates slow from fast tests. You
Line 41: should apply common sense.
Line 42:  If you are facing a slow test, consider the following:
Line 43: Using mocks or stubs to replace slower components that are part of the test
Line 44: Redesigning the production code so slower pieces of code can be tested sepa-
Line 45: rately from fast pieces of code
Line 46: Moving slower tests to a different test suite that you can run less often
Line 47: Sometimes you cannot avoid slow tests. Think of SQL tests: they are much slower than
Line 48: unit tests, but there is not much you can do about it. I separate slow tests from fast
Line 49: ones: this way, I can run my fast tests all the time and the slow tests when I modify the
Line 50: production code that has a slow test tied to it. I also run the slow tests before commit-
Line 51: ting my code and in continuous integration. 
Line 52: 10.1.2
Line 53: Tests should be cohesive, independent, and isolated
Line 54: Tests should be as cohesive, independent, and isolated as possible. Ideally, a single test
Line 55: method should test a single functionality or behavior of the system. Fat tests (or, as the
Line 56: test smells community calls them, eager tests) exercise multiple functionalities and are
Line 57: often complex in terms of implementation. Complex test code reduces our ability to
Line 58: understand what is being tested at a glance and makes future maintenance more diffi-
Line 59: cult. If you face such a test, break it into multiple smaller tests. Simpler and shorter
Line 60: tests are better.
Line 61:  Moreover, tests should not depend on other tests to succeed. The test result should
Line 62: be the same whether the test is executed in isolation or together with the rest of the
Line 63: test suite. It is not uncommon to see cases where test B only works if test A is executed
Line 64: first. This is often the case when test B relies on the work of test A to set up the envi-
Line 65: ronment for it. Such tests become highly unreliable.
Line 66:  If you have a test that is somewhat dependent on another test, refactor the test
Line 67: suite so each test is responsible for setting up the whole environment it needs.
Line 68: Another tip that helps make tests independent is to make sure your tests clean up
Line 69: their messes: for example, by deleting any files they created on the disk and cleaning
Line 70: 
Line 71: --- 페이지 288 ---
Line 72: 260
Line 73: CHAPTER 10
Line 74: Test code quality
Line 75: up values they inserted into a database. This will force tests to set up things themselves
Line 76: and not rely on data that was already there. 
Line 77: 10.1.3
Line 78: Tests should have a reason to exist
Line 79: You want tests that either help you find bugs or help you document behavior. You do
Line 80: not want tests that, for example, increase code coverage. If a test does not have a good
Line 81: reason to exist, it should not exist. Remember that you must maintain all your tests.
Line 82: The perfect test suite is one that can detect all the bugs with the minimum number of
Line 83: tests. While having such a perfect test suite is impossible, making sure you do not have
Line 84: useless tests is a good start. 
Line 85: 10.1.4
Line 86: Tests should be repeatable and not flaky
Line 87: A repeatable test gives the same result no matter how many times it is executed. Devel-
Line 88: opers lose their trust in tests that present flaky behavior (sometimes pass and some-
Line 89: times fail, without any changes in the system or test code).
Line 90:  Flaky tests hurt the productivity of software development teams. It is hard to know
Line 91: whether a flaky test is failing because the behavior is buggy or because it is flaky. Little
Line 92: by little, flaky tests can make us lose confidence in our test suites. Such lack of confi-
Line 93: dence may lead us to deploy our systems even though the tests fail (they may be bro-
Line 94: ken because of flakiness, not because the system is misbehaving).
Line 95:  The prevalence and impact of flaky tests in the software development world have
Line 96: increased over time (or, at least, we talk more about them now). Companies like
Line 97: Google and Facebook have publicly talked about problems caused by flaky tests.
Line 98:  A test can become flaky for many reasons:
Line 99: Because it depends on external or shared resources—If a test depends on a database,
Line 100: many things can cause flakiness. For example, the database may not be available
Line 101: at the moment the test is executed, it may contain data that the test does not
Line 102: expect, or two developers may be running the test suite at the same time and
Line 103: sharing the same database, causing one to break the test of the other.
Line 104: Due to improper time-outs—This is a common reason in web testing. Suppose a test
Line 105: has to wait for something to happen in the system: for example, a request com-
Line 106: ing back from a web service, which is then displayed in an HTML element. If
Line 107: the web application is slower than normal, the test may fail because it did not
Line 108: wait long enough.
Line 109: Because of a hidden interaction between different test methods—Test A somehow influ-
Line 110: ences the result of test B, possibly causing it to fail.
Line 111: The work of Luo et al. (2014) also shed light on the causes of flaky tests. After analyz-
Line 112: ing 201 flaky tests in open source systems, the authors noticed the following:
Line 113: Async wait, concurrency, and test order dependency are the three most com-
Line 114: mon causes of flakiness.
Line 115: Most flaky tests are flaky from the time they are written.
Line 116: 
Line 117: --- 페이지 289 ---
Line 118: 261
Line 119: Principles of maintainable test code
Line 120: Flaky tests are rarely due to the platform-specifics (they do not fail because of
Line 121: different operating systems).
Line 122: Flakiness is often due to dependencies on external resources and can be fixed
Line 123: by cleaning the shared state between test runs.
Line 124: Detecting the cause of a flaky test is challenging. Software engineering researchers
Line 125: have proposed automated tools to detect flaky tests. If you are curious about such
Line 126: tools and the current state of the art, I suggest that you read the following:
Line 127: The work of Bell et al. (2018), who proposed DeFlaker, a tool that monitors the
Line 128: coverage of the latest code changes and marks a test as flaky if any new failing
Line 129: test did not exercise any of the changed code.
Line 130: The work of Lam et al. (2019), who proposed iDFlakies, a tool that executes
Line 131: tests in random order, looking for flakiness.
Line 132: Because these tools are not fully ready, it is up to us to find the flaky tests and fix them.
Line 133: Meszaros has made a decision table that may help you with that task. You can find it in
Line 134: his book (2007) or on his website (http://xunitpatterns.com/Erratic%20Test.html). 
Line 135: 10.1.5
Line 136: Tests should have strong assertions
Line 137: Tests exist to assert that the exercised code behaved as expected. Writing good asser-
Line 138: tions is therefore key to a good test. An extreme example of a test with bad assertions
Line 139: is one with no assertions. This seems strange, but believe it or not, it happens—not
Line 140: because we do not know what we are doing, but because writing a good assertion can
Line 141: be tricky. In cases where observing the outcome of behavior is not easily achievable, I
Line 142: suggest refactoring the class or method under test to increase its observability. Revisit
Line 143: chapter 7 if you need tips for how to do so.
Line 144:  Assertions should be as strong as possible. You want your tests to fully validate the
Line 145: behavior and break if there is any slight change in the output. Imagine that a method
Line 146: calculateFinalPrice() in a ShoppingCart class changes two properties: finalPrice
Line 147: and the taxPaid. If your tests only ensure the value of the finalPrice property, a bug
Line 148: may happen in the way taxPaid is set, and your tests will not notice it. Make sure you
Line 149: are asserting everything that needs to be asserted. 
Line 150: 10.1.6
Line 151: Tests should break if the behavior changes
Line 152: Tests let you know that you broke the expected behavior. If you break the behavior
Line 153: and the test suite is still green, something is wrong with your tests. That may hap-
Line 154: pen because of weak assertions (which we have discussed) or because the method is
Line 155: covered but not tested (this happens, as discussed in chapter 9). Also recall that I
Line 156: mentioned the work of Vera-Pérez and colleagues (2019) and the existence of
Line 157: pseudo-tested methods.
Line 158:  Whenever you write a test, make sure it will break if the behavior changes. The
Line 159: TDD cycle allows developers to always see the test breaking. That happens because
Line 160: the behavior is not yet implemented, but I like the idea of “let’s see if the test breaks
Line 161: 
Line 162: --- 페이지 290 ---
Line 163: 262
Line 164: CHAPTER 10
Line 165: Test code quality
Line 166: if the behavior does not exist or is incorrect.” I am not afraid of purposefully intro-
Line 167: ducing a bug in the code, running the tests, and seeing them red (and then revert-
Line 168: ing the bug). 
Line 169: 10.1.7
Line 170: Tests should have a single and clear reason to fail
Line 171: We love tests that fail. They indicate problems in our code, usually long before the
Line 172: code is deployed. But the test failure is the first step toward understanding and fixing
Line 173: the bug. Your test code should help you understand what caused the bug.
Line 174:  There are many ways you can do that. If your test follows the earlier principles, the
Line 175: test is cohesive and exercises only one (hopefully small) behavior of the software sys-
Line 176: tem. Give your test a name that indicates its intention and the behavior it exercises.
Line 177: Make sure anyone can understand the input values passed to the method under test.
Line 178: If the input values are complex, use good variable names that explain what they are
Line 179: about and code comments in natural language. Finally, make sure the assertions are
Line 180: clear, and explain why a value is expected. 
Line 181: 10.1.8
Line 182: Tests should be easy to write
Line 183: There should be no friction when it comes to writing tests. If it is hard to do so (per-
Line 184: haps writing an integration test requires you to set up the database, create complex
Line 185: objects one by one, and so on), it is too easy for you to give up and not do it.
Line 186:  Writing unit tests tends to be easy most of the time, but it may get complicated
Line 187: when the class under test requires too much setup or depends on too many other
Line 188: classes. Integration and system tests also require each test to set up and tear down the
Line 189: (external) infrastructure.
Line 190:  Make sure tests are always easy to write. Give developers all the tools to do that. If
Line 191: tests require a database to be set up, provide developers with an API that requires one
Line 192: or two method calls and voilà—the database is ready for tests.
Line 193:  Investing time in writing good test infrastructure is fundamental and pays off in
Line 194: the long term. Remember the test base classes we created to facilitate SQL integra-
Line 195: tion tests and all the POs we created to facilitate web testing in chapter 9? This is the
Line 196: type of infrastructure I am talking about. After the test infrastructure was in place,
Line 197: the rest was easy. 
Line 198: 10.1.9
Line 199: Tests should be easy to read
Line 200: I touched on this point when I said that tests should have a clear reason to fail. I will
Line 201: reinforce it now. Your test code base will grow significantly. But you probably will not
Line 202: read it until there is a bug or you add another test to the suite.
Line 203:  It is well known that developers spend more time reading than writing code. There-
Line 204: fore, saving reading time will make you more productive. All the things you know about
Line 205: code readability and use in your production code apply to test code, as well. Do not be
Line 206: afraid to invest some time in refactoring it. The next developer will thank you.
Line 207: 
Line 208: --- 페이지 291 ---
Line 209: 263
Line 210: Principles of maintainable test code
Line 211:  I follow two practices when making my tests readable: make sure all the informa-
Line 212: tion (especially the inputs and assertions) is clear enough, and use test data builders
Line 213: whenever I build complex data structures.
Line 214:  Let’s illustrate these two ideas with an example. The following listing shows an
Line 215: Invoice class.
Line 216: public class Invoice {
Line 217:   private final double value;
Line 218:   private final String country;
Line 219:   private final CustomerType customerType;
Line 220:   public Invoice(double value, String country, CustomerType customerType) {
Line 221:     this.value = value;
Line 222:     this.country = country;
Line 223:     this.customerType = customerType;
Line 224:   }
Line 225:   public double calculate() { 
Line 226:     double ratio = 0.1;
Line 227:     // some business rule here to calculate the ratio
Line 228:     // depending on the value, company/person, country ...
Line 229:     return value * ratio;
Line 230:   }
Line 231: }
Line 232: Not-very-clear test code for the calculate() method could look like the next listing.
Line 233: @Test
Line 234: void test1() {
Line 235:   Invoice invoice = new Invoice(new BigDecimal("2500"), "NL",
Line 236:   ➥ CustomerType.COMPANY);
Line 237:   double v = invoice.calculate();
Line 238:   assertThat(v).isEqualTo(250);
Line 239: }
Line 240: At first glance, it may be hard to understand what all the information in the code
Line 241: means. It may require some extra effort to see what this invoice looks like. Imagine an
Line 242: entity class from a real enterprise system: an Invoice class may have dozens of attri-
Line 243: butes. The name of the test and the name of the cryptic variable v do not clearly
Line 244: explain what they mean. It is also not clear if the choice of “NL” as a country or
Line 245: “COMPANY” as a customer type makes any difference for the test or whether they are
Line 246: random values.
Line 247: Listing 10.1
Line 248: Invoice class
Line 249: Listing 10.2
Line 250: A not-very-clear test for an invoice
Line 251: The method we will soon test. 
Line 252: Imagine business rule here.
Line 253: 
Line 254: --- 페이지 292 ---
Line 255: 264
Line 256: CHAPTER 10
Line 257: Test code quality
Line 258:  A better version of this test method could be as follows.
Line 259: @Test
Line 260: void taxesForCompanies() {
Line 261:   Invoice invoice = new InvoiceBuilder()
Line 262:       .asCompany()
Line 263:       .withCountry("NL")
Line 264:       .withAValueOf(2500.0)
Line 265:       .build(); 
Line 266:   double calculatedValue = invoice.calculate(); 
Line 267:   assertThat(calculatedValue) 
Line 268:     .isEqualTo(250.0); // 2500 * 0.1 = 250
Line 269: }
Line 270: First, the name of the test method—taxesForCompanies—clearly expresses what
Line 271: behavior the method is exercising. This is a best practice: name your test method after
Line 272: what it tests. Why? Because a good method name may save developers from having to
Line 273: read the method’s body to understand what is being tested. In practice, it is common
Line 274: to skim the test suite, looking for a specific test or learning more about that class.
Line 275: Meaningful test names help. Some developers would argue for an even more detailed
Line 276: method name, such as taxesForCompanyAreTaxRateMultipliedByAmount. A devel-
Line 277: oper skimming the test suite can understand even the business rule.
Line 278:  Many of the methods we tested in previous chapters, while complex, had a single
Line 279: responsibility: for example, substringsBetween in chapter 2, or leftPad in chapter 3.
Line 280: We even created single parameterized tests with a generic name. We did not need a set
Line 281: of test methods with nice names, as the name of the method under test said it all. But
Line 282: in enterprise systems, where we have business-like methods such as calculateTaxes
Line 283: or calculateFinalPrice, each test method (or partition) covers a different business
Line 284: rule. Those can be expressed in the name of that test method.
Line 285:  Next, using InvoiceBuilder (the implementation of which I show shortly)
Line 286: clearly expresses what this invoice is about: it is an invoice for a company (as clearly
Line 287: stated by the asCompany() method), “NL” is the country of that invoice, and the
Line 288: invoice has a value of 2500. The result of the behavior goes to a variable whose name
Line 289: says it all (calculatedValue). The assertion contains a comment that explains
Line 290: where the 250 comes from.
Line 291:  InvoiceBuilder is an example of an implementation of a test data builder (as defined
Line 292: by Pryce [2007]). The builder helps us create test scenarios by providing a clear and
Line 293: expressive API. The use of fluent interfaces (such as asCompany().withAValueOf()…) is
Line 294: also a common implementation choice. In terms of its implementation, Invoice-
Line 295: Builder is a Java class. The trick that allows methods to be chained is to return the
Line 296: class in the methods (methods return this), as shown in the following listing.
Line 297:  
Line 298: Listing 10.3
Line 299: A more readable version of the test
Line 300: The Invoice object is 
Line 301: now built through a 
Line 302: fluent builder.
Line 303: The variable that holds the 
Line 304: result has a better name.
Line 305: The assertion has a comment to 
Line 306: explain where the 250 comes from.
Line 307: 
Line 308: --- 페이지 293 ---
Line 309: 265
Line 310: Principles of maintainable test code
Line 311: public class InvoiceBuilder {
Line 312:   private String country = "NL"; 
Line 313:   private CustomerType customerType = CustomerType.PERSON;
Line 314:   private double value = 500;
Line 315:   public InvoiceBuilder withCountry(String country) { 
Line 316:     this.country = country;
Line 317:     return this;
Line 318:   }
Line 319:   public InvoiceBuilder asCompany() {
Line 320:     this.customerType = CustomerType.COMPANY;
Line 321:     return this;
Line 322:   }
Line 323:   public InvoiceBuilder withAValueOf(double value) {
Line 324:     this.value = value;
Line 325:     return this;
Line 326:   }
Line 327:   public Invoice build() { 
Line 328:     return new Invoice(value, country, customerType);
Line 329:   }
Line 330: }
Line 331: You should feel free to customize your builders. A common trick is to make the builder
Line 332: build a common version of the class without requiring the call to all the setup methods.
Line 333: You can then, in one line, build a complex invoice, as you see in the next listing.
Line 334: var invoice = new InvoiceBuilder().build();
Line 335: In such a case, the build method (without any setup) will always build an invoice for a
Line 336: person with a value of 500.0 and “NL” as the country (see the initialized values in
Line 337: InvoiceBuilder).
Line 338:  Other developers may write shortcut methods that build other common fixtures
Line 339: for the class. In listing 10.6, the anyCompany() method returns an Invoice that belongs
Line 340: to a company (and the default value for the other fields). The fromTheUS() method
Line 341: builds an Invoice for someone in the U.S.
Line 342: public Invoice anyCompany() {
Line 343:   return new Invoice(value, country, CustomerType.COMPANY);
Line 344: }
Line 345: Listing 10.4
Line 346: Invoice test data builder
Line 347: Listing 10.5
Line 348: Building an invoice with a single line
Line 349: Listing 10.6
Line 350: Other helper methods in the builder
Line 351: The builder contains predefined values allowing 
Line 352: the user to only set the values they need to 
Line 353: customize for the current test.
Line 354: The builder contains 
Line 355: many methods that 
Line 356: let the test change a 
Line 357: specific value (such 
Line 358: as the country).
Line 359: Once the required Invoice 
Line 360: is set up, the builder builds 
Line 361: an instance of it.
Line 362: 
Line 363: --- 페이지 294 ---
Line 364: 266
Line 365: CHAPTER 10
Line 366: Test code quality
Line 367: public Invoice fromTheUS() {
Line 368:   return new Invoice(value, "US", customerType);
Line 369: }
Line 370: Building complex test data is such a recurrent task that frameworks are available to
Line 371: help, such as Java Faker (https://github.com/DiUS/java-faker) for the Java world and
Line 372: factory_bot (https://github.com/thoughtbot/factory_bot) for Ruby. I am sure you
Line 373: can find one for your programming language.
Line 374:  Finally, you may have noticed the comment near the assertion: 2500 * 0.1 = 250.
Line 375: Some developers would suggest that the need for this comment indicates the code
Line 376: requires improvement. To remove the comment, we can introduce explanatory vari-
Line 377: ables: in listing 10.7, we use the invoiceValue and tax variables in the assertion. It is
Line 378: up to you and your team members to agree on the best approach for you.
Line 379: @Test
Line 380: void taxesForCompanyAreTaxRateMultipliedByAmount() {
Line 381:   double invoiceValue = 2500.0; 
Line 382:   double tax = 0.1;
Line 383:   Invoice invoice = new InvoiceBuilder()
Line 384:       .asCompany()
Line 385:       .withCountry("NL")
Line 386:       .withAValueOf(invoiceValue) 
Line 387:       .build();
Line 388:   double calculatedValue = invoice.calculate();
Line 389:   assertThat(calculatedValue)
Line 390:     .isEqualTo(invoiceValue * tax); 
Line 391: }
Line 392: To sum up, introducing test data builders, using variable names to explain the mean-
Line 393: ing of information, having clear assertions, and adding comments where code is not
Line 394: expressive enough will help developers better comprehend the test code. 
Line 395: 10.1.10 Tests should be easy to change and evolve
Line 396: Although we like to think that we always design stable classes with single responsibili-
Line 397: ties that are closed for modification but open for extension (see Martin [2014] for
Line 398: more about the Open Closed Principle), in practice, that does not always happen.
Line 399: Your production code will change, and that will force your tests to change as well.
Line 400:  Therefore, your task when implementing test code is to ensure that changing it
Line 401: will not be too painful. I do not think it is possible to make it completely painless, but
Line 402: you can reduce the number of points that will require changes. For example, if you
Line 403: see the same snippet of code in 10 different test methods, consider extracting it. If a
Line 404: Listing 10.7
Line 405: Making the test more readable via explanatory variables
Line 406: Declares the 
Line 407: invoiceValue and 
Line 408: tax variables
Line 409: Uses the variable instead 
Line 410: of the hard-coded value
Line 411: The assertion uses the 
Line 412: explanatory variables instead 
Line 413: of hard-coded numbers.
Line 414: 
Line 415: --- 페이지 295 ---
Line 416: 267
Line 417: Test smells
Line 418: change happens and you are forced to change that code snippet, you now only have
Line 419: to change it in 1 place rather than 10.
Line 420:  Your tests are coupled to the production code in one way or another. That is a fact.
Line 421: The more your tests know about how the production code works, the harder it is to
Line 422: change them. As we discussed in chapter 6, a clear disadvantage of using mocks is the
Line 423: significant coupling with the production code. Determining how much your tests
Line 424: need to know about the production code to test it properly is a significant challenge. 
Line 425: 10.2
Line 426: Test smells
Line 427: In the previous sections, we discussed some best practices for writing good test code.
Line 428: Now let’s discuss test smells. The term code smell indicates symptoms that may indicate
Line 429: deeper problems in the system’s source code. Some well-known examples are Long
Line 430: Method, Long Class, and God Class. Several research papers show that code smells hin-
Line 431: der the comprehensibility and maintainability of software systems (such as the work by
Line 432: Khomh and colleagues [2009]).
Line 433:  While the term has long been applied to production code, our community has
Line 434: been developing catalogs of smells that are specific to test code. Research has also
Line 435: shown that test smells are prevalent in real life and, unsurprisingly, often hurt the
Line 436: maintenance and comprehensibility of the test suite (Spadini et al., 2020).
Line 437:  The following sections examine several well-known test smells. A more compre-
Line 438: hensive list can be found in xUnit Test Patterns by Meszaros (2007). I also recommend
Line 439: reading the foundational paper on test smells by Deursen and colleagues (2001).
Line 440: 10.2.1
Line 441: Excessive duplication
Line 442: It is not surprising that code duplication can happen in test code since it is widespread
Line 443: in production code. Tests are often similar in structure, as you may have noticed in
Line 444: several of the code examples in this book. We even used parameterized tests to reduce
Line 445: duplication. A less attentive developer may end up writing duplicate code (copy-pasting
Line 446: often happens in real life, as Treude, Zaidman, and I observed in an empirical study
Line 447: [2021]) instead of putting some effort into implementing a better solution.
Line 448:  Duplicated code can reduce the productivity of software developers. If we need to
Line 449: change a duplicated piece of code, we must apply the same change in all the places
Line 450: where the code is duplicated. In practice, it is easy to forget one of these places and end
Line 451: up with problematic test code. Duplicating code may also hinder the ability to evolve the
Line 452: test suite, as mentioned earlier. If the production code changes, you do not want to have
Line 453: to change too much test code. Isolating duplicated code reduces this pain.
Line 454:  I advise you to refactor your test code often. Extracting duplicate code to private
Line 455: methods or external classes is often a good, quick, cheap solution to the problem. But
Line 456: being pragmatic is key: a little duplication may not harm you, and you should use your
Line 457: experience to judge when refactoring is needed. 
Line 458: 
Line 459: --- 페이지 296 ---
Line 460: 268
Line 461: CHAPTER 10
Line 462: Test code quality
Line 463: 10.2.2
Line 464: Unclear assertions
Line 465: Assertions are the first thing a developer looks at when a test fails. A good assertion
Line 466: clearly reveals its reason for failure, is legible, and is as specific as possible. The test smell
Line 467: emerges when it is hard to understand the assertions or the reason for their failure.
Line 468:  There are several reasons for this smell to happen. Some features or business rules are
Line 469: so complex that they require a complex set of assertions to ensure their behavior. In
Line 470: these situations, we end up writing complex assert instructions that are not easy to under-
Line 471: stand. To help with such cases, I recommend writing customized assert instructions that
Line 472: abstract away part of the complexity of the assertion code, and writing code comments
Line 473: that explain quickly and in natural language what those assertions are about. The latter
Line 474: mainly applies when the assertions are not self-explanatory. Do not be afraid to write a
Line 475: comment in your code if it will help future developers understand what is going on.
Line 476:  Interestingly, a common best practice in the test best practice literature is the “one
Line 477: assertion per method” strategy. The idea is that a test with a single assertion can only
Line 478: focus on a single behavior, and it is easier for developers to understand if the assertion
Line 479: fails. I strongly disagree with this rule. If my test is cohesive enough and focuses on a
Line 480: single feature, the assertions should ensure that the entire behavior is as expected.
Line 481: This may mean asserting that many fields were updated and have a new value. It may
Line 482: also mean asserting that the mock interacted with other dependencies properly.
Line 483: There are many cases in which using multiple assertions in a single test is useful. Forc-
Line 484: ing developers to have a single assertion per test method is extreme—but your tests
Line 485: also should not have useless assertions.
Line 486:  Frameworks often offer the possibility of doing soft assertions: assertions that do
Line 487: not stop the test if they fail but are reported only at the very end of the test execu-
Line 488: tion (which is still considered a failed test). For example, AssertJ offers this ability
Line 489: (http://mng.bz/aDeo).
Line 490:  Finally, even if you know what to assert for, picking the right assertion method pro-
Line 491: vided by whatever test framework you are using can make a difference. Using the
Line 492: wrong or not ideal assert instruction may lead to imprecise assertion error messages. I
Line 493: strongly suggest using AssertJ and its extensive collection of assertions. 
Line 494: 10.2.3
Line 495: Bad handling of complex or external resources
Line 496: Understanding test code that uses external resources can be difficult. The test should
Line 497: ensure that the resource is readily available and prepared for it. The test should also
Line 498: clean up its mess afterward.
Line 499:  A common smell is to be optimistic about the external resource. Resource optimism
Line 500: happens when a test assumes that a necessary resource (such as a database) is readily
Line 501: available at the start of its execution. The problem is that when the resource is not avail-
Line 502: able, the test fails, often without a clear message that explains the reason. This can con-
Line 503: fuse developers, who may think a new bug has been introduced in the system.
Line 504:  To avoid such resource optimism, a test should not assume that the resource is
Line 505: already in the correct state. The test should be responsible for setting up the state
Line 506: 
Line 507: --- 페이지 297 ---
Line 508: 269
Line 509: Test smells
Line 510: itself. This can mean the test is responsible for populating a database, writing the
Line 511: required files to the disk, or starting up a Tomcat server. This setup may require com-
Line 512: plex code, and you should also make your best effort to abstract away such complexity
Line 513: by, for example, moving such code to other classes (like DatabaseInitialization or
Line 514: TomcatLoader) and allowing the test code to focus on the test cases.
Line 515:  Another common test smell happens when the test assumes that the resource is
Line 516: available all the time. Imagine a test method that interacts with a web service, which
Line 517: may be down for reasons we do not control. To avoid this test smell, you have two
Line 518: options: avoid depending on external resources by using stubs and mocks or, if the
Line 519: test cannot avoid using the external dependency, make the test suite robust enough.
Line 520: For example, make your test suite skip that test when the resource is unavailable, and
Line 521: provide an alert explaining why that was the case. This may seem counterintuitive, but
Line 522: remember that developers trust their test suites. Having a single test fail for the wrong
Line 523: reasons can make you lose confidence in the entire test suite.
Line 524:  From a readability perspective, it should be easy to understand all the (external)
Line 525: resources required and used by the test. Imagine that a test requires a test file in some
Line 526: directory. If the file is not there, the test fails. A first-time developer may have difficulty
Line 527: understanding this prerequisite. Avoid having such mystery guests in your test suite.
Line 528: The test code should be explicit about all its external dependencies.  
Line 529: 10.2.4
Line 530: Fixtures that are too general
Line 531: A fixture is the set of input values used to exercise the component under test. As you
Line 532: may have noticed, fixtures are the stars of the test method, as they derive naturally
Line 533: from the test cases we engineer using any of the techniques we have discussed.
Line 534:  When testing more complex components, you may need to build several different
Line 535: fixtures: one for each partition you want to exercise. These fixtures can then become
Line 536: complex. And to make the situation worse, while tests are different from each other,
Line 537: their fixtures may intersect. Given this possible intersection among the different fix-
Line 538: tures, as well as the difficulty with building complex entities and fixtures, you may
Line 539: decide to declare a large fixture that works for many different tests. Each test would
Line 540: then use a small part of this large fixture.
Line 541:  While this approach may work, and the tests may correctly implement the test
Line 542: cases, they quickly become hard to maintain. Once a test fails, you will find yourself
Line 543: with a large fixture that may not be completely relevant for that particular failing test.
Line 544: You then must manually filter out parts of the fixture that are not exercised by the fail-
Line 545: ing test. That is an unnecessary cost.
Line 546:  Making sure the fixture of a test is as specific and cohesive as possible helps you com-
Line 547: prehend the essence of a test (which is, again, highly relevant when the test starts to fail).
Line 548: Build patterns (focusing on building test data) can help you avoid generic fixtures. More
Line 549: specifically, the Test Data Builder pattern we discussed is often used in the test code of
Line 550: enterprise applications. Such applications often deal with creating complex sets of inter-
Line 551: related business entities, which can easily lead developers to write general fixtures. 
Line 552: 
Line 553: --- 페이지 298 ---
Line 554: 270
Line 555: CHAPTER 10
Line 556: Test code quality
Line 557: 10.2.5
Line 558: Sensitive assertions
Line 559: Good assertions are fundamental in test cases. A bad assertion may result in a test not
Line 560: failing when it should. However, a bad assertion may also cause a test to fail when it
Line 561: should not. Engineering a good assertion statement is challenging—even more so when
Line 562: components produce fragile outputs (outputs that change often). Test code should be
Line 563: as resilient as possible to the implementation details of the component under test.
Line 564: Assertions also should not be oversensitive to internal changes.
Line 565:  In the tool we use to assess students’ submissions (https://github.com/cse1110/
Line 566: andy), we have a class responsible for transforming the assessment results into a message
Line 567: (string) that we show in our cloud-based IDE. The following listing shows the output for
Line 568: one of our exercises.
Line 569: --- Compilation 
Line 570: Success
Line 571: --- JUnit execution 
Line 572: 7/7 passed
Line 573: --- JaCoCo coverage 
Line 574: Line coverage: 13/13
Line 575: Instruction coverage: 46/46
Line 576: Branch coverage: 12/12 
Line 577: --- Mutation testing     
Line 578: 10/10 killed
Line 579: --- Code checks 
Line 580: No code checks to be assessed
Line 581: --- Meta tests 
Line 582: 13/13 passed
Line 583: Meta test: always finds clumps (weight: 1) PASSED
Line 584: Meta test: always returns zero (weight: 1) PASSED
Line 585: Meta test: checks in pairs (weight: 1) PASSED
Line 586: Meta test: does not support more than two per clump (weight: 1) PASSED
Line 587: Meta test: does not support multiple clumps (weight: 1) PASSED
Line 588: Meta test: no empty check (weight: 1) PASSED
Line 589: Meta test: no null check (weight: 1) PASSED
Line 590: Meta test: only checks first two elements (weight: 1) PASSED
Line 591: Meta test: only checks last two elements (weight: 1) PASSED
Line 592: Meta test: skips elements after clump (weight: 1) PASSED
Line 593: Meta test: skips first element (weight: 1) PASSED
Line 594: Meta test: skips last element (weight: 1) PASSED
Line 595: Meta test: wrong result for one element (weight: 1) PASSED 
Line 596: --- Assessment
Line 597: Branch coverage: 12/12 (overall weight=0.10)
Line 598: Mutation coverage: 10/10 (overall weight=0.10)
Line 599: Listing 10.8
Line 600: An example of the output of our tool
Line 601: The result of the compilation
Line 602: How many tests passed
Line 603: Coverage information
Line 604: Mutation testing 
Line 605: information
Line 606: Static code checks (in this 
Line 607: case, none were executed)
Line 608: The student’s final grade
Line 609: The student’s 
Line 610: final grade
Line 611: 
Line 612: --- 페이지 299 ---
Line 613: 271
Line 614: Test smells
Line 615: Code checks: 0/0 (overall weight=0.00)
Line 616: Meta tests: 13/13 (overall weight=0.80)
Line 617: Final grade: 100/100
Line 618: If we write tests without thinking too much, we end up writing lots of assertions that
Line 619: check whether some string is in the output. And given that we will write many test
Line 620: cases for many different outputs, our test suite will end up with lots of statements like
Line 621: “assert output contains Final grade: 100/100”.
Line 622:  Note how sensitive this assertion is. If we change the message slightly, the tests will all
Line 623: break. Making assertions that are less sensitive to small changes is usually a good idea.
Line 624:  In this situation, we have no other option than to assert that the string matches
Line 625: what we have. To sort this out, we decided to create our own set of assertions for each
Line 626: part of the message we need to assert. These assertions enable us to decouple our test
Line 627: code from the strings themselves. And if the message changes in the future, all we will
Line 628: need to do is change our assertion.
Line 629:  In listing 10.9, the reportCompilationError test method ensures that we show the
Line 630: proper message to the student when they submit a solution that does not compile. We
Line 631: create a Result object (representing the final assessment of the student solution) with
Line 632: a compilation error. We then call the method under test and get back the generated
Line 633: string message.
Line 634: @Test
Line 635: void reportCompilationError() {
Line 636:   Result result = new ResultTestDataBuilder()
Line 637:     .withCompilationFail(
Line 638:       new CompilationErrorInfo(
Line 639:         ➥ "Library.java", 10, "some compilation error"),
Line 640:       new CompilationErrorInfo(
Line 641:         ➥ "Library.java", 11, "some other compilation error")
Line 642:   ).build(); 
Line 643:   writer.write(ctx, result); 
Line 644:   String output = generatedResult();
Line 645:   assertThat(output) 
Line 646:     .has(noFinalGrade())
Line 647:     .has(not(compilationSuccess()))
Line 648:     .has(compilationFailure())
Line 649:     .has(compilationErrorOnLine(10))
Line 650:     .has(compilationErrorOnLine(11))
Line 651:     .has(compilationErrorType("some compilation error"))
Line 652:     .has(compilationErrorType("some other compilation error"));
Line 653: }
Line 654: Listing 10.9
Line 655: A test that uses our own assertions
Line 656: Creates a 
Line 657: Result in 
Line 658: which we tell 
Line 659: the student 
Line 660: that there is a 
Line 661: compilation 
Line 662: error in their 
Line 663: solution
Line 664: Calls the method 
Line 665: under test and gets 
Line 666: the generated message
Line 667: Asserts that the message is as we expect. 
Line 668: Note, however, our set of assertions: 
Line 669: noFinalGrade, compilationSuccess, and 
Line 670: so on. They decouple our test from the 
Line 671: concrete string.
Line 672: 
Line 673: --- 페이지 300 ---
Line 674: 272
Line 675: CHAPTER 10
Line 676: Test code quality
Line 677: The trick happens in the assertions. Note the many assertions we created: noFinal-
Line 678: Grade() ensures that the final grade is not displayed, compilationErrorOnLine(10)
Line 679: ensures that we tell the student there is a compilation error on line 10, and so on. To
Line 680: create these assertions, we use AssertJ’s extension capabilities. All we need to do is cre-
Line 681: ate a method that returns AssertJ’s Condition<?> class. The generic type should be
Line 682: the same as the type of the object on which we are performing the assertion. In this
Line 683: case, the output variable is a string, so we need to create a Condition<String>.
Line 684:  The implementation of the compilationErrorOnLine assertion is shown in listing
Line 685: 10.10. If a compilation error happens, we print "- line <number>: <error message>".
Line 686: This assertion then looks for "- line <number>" in the string.
Line 687: public static Condition<String> compilationErrorOnLine(int lineNumber) { 
Line 688:   return new Condition<>() {
Line 689:     @Override
Line 690:     public boolean matches(String value) {
Line 691:       return value.contains("- line " + lineNumber); 
Line 692:     }
Line 693:   };
Line 694: }
Line 695: Back to the big picture: make sure your assertions are not too sensitive, or your tests
Line 696: may break for no good reason. 
Line 697: Exercises
Line 698: 10.1
Line 699: Jeanette hears that two tests are behaving strangely. Both of them pass when
Line 700: executed in isolation, but they fail when executed together.
Line 701: Which one of the following is not the cause of this problem?
Line 702: A The tests depend on the same external resources.
Line 703: B The execution order of the tests matters.
Line 704: C Both tests are very slow.
Line 705: D They do not perform a cleanup operation after execution.
Line 706: 10.2
Line 707: Look at the following test code. What is the most likely test code smell that this
Line 708: piece of code presents?
Line 709: @Test
Line 710: void test1() {
Line 711:   // web service that communicates with the bank
Line 712:   BankWebService bank = new BankWebService();
Line 713:   User user = new User("d.bergkamp", "nl123");
Line 714:   bank.authenticate(user);
Line 715:   Thread.sleep(5000); // sleep for 5 seconds
Line 716:   double balance = bank.getBalance();
Line 717:   Thread.sleep(2000);
Line 718: Listing 10.10
Line 719: compilationErrorOnLine assertion
Line 720: Makes the method
Line 721: static, so we can
Line 722: statically import it
Line 723: in the test class
Line 724: Checks whether value contains
Line 725: the string we are looking for
Line 726: 
Line 727: --- 페이지 301 ---
Line 728: 273
Line 729: Exercises
Line 730:   Payment bill = new Payment();
Line 731:   bill.setOrigin(user);
Line 732:   bill.setValue(150.0);
Line 733:   bill.setDescription("Energy bill");
Line 734:   bill.setCode("YHG45LT");
Line 735:   bank.pay(bill);
Line 736:   Thread.sleep(5000);
Line 737:   double newBalance = bank.getBalance();
Line 738:   Thread.sleep(2000);
Line 739:   // new balance should be previous balance - 150
Line 740:   Assertions.assertEquals(newBalance, balance - 150);
Line 741: }
Line 742: A Flaky test
Line 743: B Test code duplication
Line 744: C Obscure test
Line 745: D Long method
Line 746: 10.3
Line 747: RepoDriller is a project that extracts information from Git repositories. Its inte-
Line 748: gration tests use a lot of real Git repositories (that are created solely for the
Line 749: test), each with a different characteristic: one repository contains a merge com-
Line 750: mit, another contains a revert operation, and so on.
Line 751: Its tests look like this:
Line 752: @Test
Line 753: public void test01() {
Line 754:   // arrange: specific repo
Line 755:   String path = "test-repos/git-4";
Line 756:   // act
Line 757:   TestVisitor visitor = new TestVisitor();
Line 758:   new RepositoryMining()
Line 759:     .in(GitRepository.singleProject(path))
Line 760:     .through(Commits.all())
Line 761:     .process(visitor)
Line 762:     .mine();
Line 763:   // assert
Line 764:   Assert.assertEquals(3, visitor.getVisitedHashes().size());
Line 765:   Assert.assertTrue(visitor.getVisitedHashes().get(2).equals("b8c2"));
Line 766:   Assert.assertTrue(visitor.getVisitedHashes().get(1).equals("375d"));
Line 767:   Assert.assertTrue(visitor.getVisitedHashes().get(0).equals("a1b6"));
Line 768: }
Line 769: Which test smell might this piece of code suffer from?
Line 770: A Condition logic in the test
Line 771: B General fixture
Line 772: 
Line 773: --- 페이지 302 ---
Line 774: 274
Line 775: CHAPTER 10
Line 776: Test code quality
Line 777: C Flaky test
Line 778: D Mystery guest
Line 779: 10.4
Line 780: In the following code, we show an actual test from Apache Commons Lang, a
Line 781: very popular open source Java library. This test focuses on the static random()
Line 782: method, which is responsible for generating random characters. An interesting
Line 783: detail in this test is the comment Will fail randomly about 1 in 1000 times.
Line 784: /**
Line 785:  * Test homogeneity of random strings generated --
Line 786:  * i.e., test that characters show up with expected frequencies
Line 787:  * in generated strings.  Will fail randomly about 1 in 1000 times.
Line 788:  * Repeated failures indicate a problem.
Line 789:  */
Line 790: @Test
Line 791: public void testRandomStringUtilsHomog() {
Line 792:   final String set = "abc";
Line 793:   final char[] chars = set.toCharArray();
Line 794:   String gen = "";
Line 795:   final int[] counts = {0, 0, 0};
Line 796:   final int[] expected = {200, 200, 200};
Line 797:   for (int i = 0; i < 100; i++) {
Line 798:     gen = RandomStringUtils.random(6,chars);
Line 799:     for (int j = 0; j < 6; j++) {
Line 800:       switch (gen.charAt(j)) {
Line 801:         case 'a': {counts[0]++; break;}
Line 802:         case 'b': {counts[1]++; break;}
Line 803:         case 'c': {counts[2]++; break;}
Line 804:         default: {fail("generated character not in set");}
Line 805:       }
Line 806:     }
Line 807:   }
Line 808:   // Perform chi-square test with df = 3-1 = 2, testing at .001 level
Line 809:   assertTrue("test homogeneity -- will fail about 1 in 1000 times",
Line 810:     chiSquare(expected,counts) < 13.82);
Line 811: }
Line 812: Which one of the following statements is incorrect about the test?
Line 813: A The test is flaky because of the randomness that exists in generating
Line 814: characters.
Line 815: B The test checks for invalidly generated characters and also checks that
Line 816: characters are picked in the same proportion.
Line 817: C The method being static has nothing to do with its flakiness.
Line 818: D To avoid flakiness, a developer should have mocked the random() function.
Line 819: 10.5
Line 820: A developer observes that two tests pass when executed in isolation but fail
Line 821: when executed together.
Line 822: Which of the following is the least likely fix for this problem (also known as
Line 823: Test Run War)?
Line 824: 
Line 825: --- 페이지 303 ---
Line 826: 275
Line 827: Summary
Line 828: A Make each test runner a specific sandbox.
Line 829: B Use fresh fixtures in every test.
Line 830: C Remove and isolate duplicated test code.
Line 831: D Clean up the state during teardown.
Line 832: Summary
Line 833: Writing good test code is as challenging as writing good production code. We
Line 834: should ensure that our test code is easy to maintain and evolve.
Line 835: We desire many things in a test method. Tests should be fast, cohesive, and
Line 836: repeatable; they should fail for a reason and contain strong assertions; they
Line 837: should be easy to read, write, and evolve; and they should be loosely coupled
Line 838: with the production code.
Line 839: Many things can hinder the maintainability of test methods: too much duplica-
Line 840: tion, too many bad assertions, bad handling of complex (external) resources, too
Line 841: many general fixtures, too many sensitive assertions, and flakiness. You should
Line 842: avoid these.