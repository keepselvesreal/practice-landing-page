Line 1: 
Line 2: --- 페이지 199 ---
Line 3: Chapter 10. Organization Of Tests
Line 4: Good order is the foundation of all good things.
Line 5: — Edmund Burke
Line 6: Rules are mostly made to be broken and are too often for the lazy to hide behind.
Line 7: — Douglas MacArthur
Line 8: When the number of your tests grows, the way they are written and stored becomes more and more
Line 9: important. This section discusses some decisions relating to various "organizational" aspects of your
Line 10: tests. Even though parts of this section do not contribute directly to your testing abilities, it will surely
Line 11: make you aware of the broader context for your tests. This is because writing a single class is just the
Line 12: beginning: sooner or later your test suite will become huge, and then it will really matter how it is
Line 13: organized.
Line 14: How your tests are organized is something that will affect not only your work but also
Line 15: that of your teammates. Before you deviate from the most common paths (for example by
Line 16: changing project layout to something non-standard), please make sure that your colleagues
Line 17: also think it is a good idea!
Line 18: 10.1. Package for Test Classes
Line 19:  We have already discussed where source code and test code should be kept. The general consensus
Line 20: is that they should reside in different directories: src/main/java for production code and src/test/
Line 21: java for test code. Such a separation is respected by all currently used tools, and helps us to steer
Line 22: clear of the peril of releasing production code with which some test classes have come to be mingled.
Line 23: Agreeing on the separate directories does not end the discussion. Another question is about the
Line 24: packages used for test classes.
Line 25: Basically, there are two possible options:
Line 26: 1. test classes should use the same packages that are used by the production code being tested (e.g. a
Line 27: test for a my.project.User class should also be kept in a my.project package),
Line 28: 2. test classes should use different packages - usually prefixed or suffixed with tests, e.g.
Line 29: my.project.tests.
Line 30: Why does this matter? To be perfectly frank, usually it does not matter so much. Having tests in the
Line 31: same package gives you the following:
Line 32: • there is no need to import some classes (e.g. the SUT class) into your tests, making your imports list
Line 33: shorter,
Line 34: • it is possible to test some cumbersome cases by relaxing the access modifiers of some methods to
Line 35: "default" (see Section 8.5 and Section 8.7).
Line 36: On the other hand, keeping test classes in different packages results in the following:
Line 37: • you can not use the "default" access modifier to test private methods …however, you can still use a
Line 38: protected access modifier.
Line 39: 184
Line 40: 
Line 41: --- 페이지 200 ---
Line 42: Chapter 10. Organization Of Tests
Line 43: • it is very clear which classes belong to production code and which to test code; while it is usually
Line 44: not a problem for test classes (as they are pre/suffixed with Test), it might be important for various
Line 45: utility classes of test code.
Line 46: I must say that almost all the projects I’m aware of use the first option, that is they tend to put test
Line 47: classes in the same packages as the production code. Different packages are used for integration and
Line 48: end-to-end tests. And this is how I would encourage you to structure your packages as well.
Line 49: 10.2. Name Your Tests Consistently
Line 50: The naming schema of test classes and test methods can make a real difference. If consistent and
Line 51: well thought out, it will help you go to the right place in your code - exactly where you want to be.
Line 52: If chaotic, with no obvious patterns, it will slow down your development by forcing you to browse
Line 53: through your codebase class by class instead of jumping instantly to this one important place. Another
Line 54: important thing about naming is that it helps us to understand the role and purpose of each test. This
Line 55: is very important when adding new tests or when looking to identify the reason for a particular test
Line 56: failure.
Line 57: In this section we will take a look at two main factors which impact on how hassle-free or problematic
Line 58: your experience of working with test code is likely to be: names of test classes and names of test
Line 59: methods. Additionally we will also consider naming schemas for test-doubles.
Line 60: 10.2.1. Test Class Names
Line 61: The most popular pattern for naming test classes is to append a Test suffix to the name of the
Line 62: class being tested. This results in test classes like UserDAOTest, PasswordValidatorTest and
Line 63: BankAccountTest, which test production classes named UserDAO, PasswordValidator and
Line 64: BankAccount respectively. The benefits of this pattern are the following:
Line 65: • it is dead simple,
Line 66: • it is honored by a number of tools which streamline the process of configuring the testing plugins
Line 67: of build tools (e.g. Maven, Gradle), as classes with the Test suffix are recognized by default as test
Line 68: classes,
Line 69: • allow you to move quickly between test and production code with your IDE (so, for example, you
Line 70: can jump from BankAccount to BankAccountTest with one keyboard shortcut),
Line 71: • there is a one-to-one mapping between production class and test class, so you know that all tests of
Line 72: the given class are in this one place, and, vice-versa, that this test class contains nothing but tests for
Line 73: a single class,
Line 74: • it is commonly used (so everyone feels at home when your code follows this schema).
Line 75: There are not many counterproposals for test class naming schemes1. The overwhelming majority of
Line 76: code that I have seen follows the simple schema presented above. And there are not many reasons, if
Line 77: any, for you not to follow it as well. I follow this pattern 99% of the time (and would encourage you
Line 78: to do the same), but there are also some cases where I renounce it. Two of them are described below.
Line 79: 1One that I am aware of, derived from the BDD approach, makes the test class name part of a "when" element of a BDD
Line 80: convention - see http://www.slideshare.net/wakaleo/junit-kung-fu-getting-more-out-of-your-unit-tests
Line 81: 185
Line 82: 
Line 83: --- 페이지 201 ---
Line 84: Chapter 10. Organization Of Tests
Line 85: Splitting Up Long Test Classes
Line 86: When a test class starts to grow beyond the "safety limit" I have established for myself, I start to
Line 87: wonder whether splitting it up would not perhaps be a good idea. A common scenario, when I do split
Line 88: a test class up, is that there is a lot of arguments checking and numerous tests for expected exceptions.
Line 89: I usually move these tests to a separate class and use a different suffix - WrongValuesTest - to
Line 90: distinguish it. In the case of an exemplary MyClass, I would end up with the following test classes:
Line 91: 1. MyClassTest - all tests that puts the "valid" behaviour of the class through its paces. This test class
Line 92: shows the right way to use MyClass.
Line 93: 2. MyClassWrongValuesTest - all tests that put the SUT through its paces and fail (fast!) with an
Line 94: expected exception. This test class shows what happens when MyClass is used in an incorrect way.
Line 95: The second test class - MyClassWrongValuesTest - is usually much simpler (but sometimes longer)
Line 96: than MyClassTest. Often it will contain some data providers, whose role is to provide various illegal
Line 97: values for different test methods. Test doubles are rarely required there (except, maybe, for dummies);
Line 98: this is because no methods are really called on them, as arguments checking is usually the first thing
Line 99: you do.
Line 100: The necessity of splitting up a test class might by indicative that what you should really be
Line 101: splitting up is the class being tested itself! If it cannot be tested with one test class, maybe
Line 102: it is too big - maybe it has too much responsibility? If so, then fix this problem, and the test
Line 103: class will automatically shrink to an appropriate length.
Line 104: Test Class Per Feature
Line 105: Another way to go with test class naming is to base their name not only on a tested class, but also on a
Line 106: tested feature. The following story illustrates the usability of such an approach.
Line 107: One day I was asked to introduce a change to a certain legacy code class called DataProvider. This
Line 108: class was responsible for some computations and offered some methods which returned the mean
Line 109: values of some calculated numbers. The then current implementation was to return null if some
Line 110: data required for calculations was missing. At some point our client introduced a new monitoring
Line 111: tool, which was consuming data returned by the DataProvider class in order to draw some charts.
Line 112: It transpired that this new tool did not like null values at all, so a change was requested – so that it
Line 113: would return zeros instead of null values.
Line 114: I took a look at the existing code, and found no tests for the class. It was not possible to test the
Line 115: class thoroughly (because it would have taken too much time), so I decided to only introduce tests
Line 116: which would cover the functionality in question. Because I did not intend to test the whole class,
Line 117: I decided to abandon the ClassNameTest pattern. Instead, I created a new test class and called it
Line 118: DataProviderMeanValuesZerosInsteadOfNullsTest. Even though it went against the norms of my
Line 119: working practice, I felt it was the right thing to do. The test class name indicated clearly that it was
Line 120: meant to test the DataProvider class, the suffix informed people that it was a test class, and the rest
Line 121: served to indicate what part of the class functionality was being tested.
Line 122: If it ever should come about that we decide to cover the whole class with tests (not very
Line 123: likely, though…), then the DataProviderMeanValuesZerosInsteadOfNullsTest will
Line 124: probably be merged into it.
Line 125: 186
Line 126: 
Line 127: --- 페이지 202 ---
Line 128: Chapter 10. Organization Of Tests
Line 129: 10.2.2. Test Method Names
Line 130: JUnit, like all current testing frameworks, give you complete freedom when it comes to naming test
Line 131: methods. This is because identification of test methods is based on annotations and not on method
Line 132: names. With freedom, though, comes a need to make choices, and many different options to choose
Line 133: from. Let’s discuss this issue and see if we can get to choose the best one.
Line 134: Please refer to Section 11.1 for additional discussion about why some naming schemas are
Line 135: more appropriate than others.
Line 136:  Historically, method names were prefixed with the word test - e.g. testConstructor(),
Line 137: testReturnsNonNullArray(), etc. This naming schema was popularized (or rather enforced) by
Line 138: older versions of JUnit, which treated all methods that followed this pattern as test methods and
Line 139: executed them during tests execution (ignoring any methods with different names). And for a long
Line 140: time everyone was happy with it.
Line 141:  However, the limitations of this naming schema started to show up. First of all, it was not obvious
Line 142: what a particular test method was all about, just by looking at its name. It was quite common to find
Line 143: lengthy test methods which, under a common name such as, for example, testUserAdd(), verified
Line 144: many features of a class being tested. This was especially painful when dealing with failed tests, as
Line 145: there was not much one could learn from the information that "testUserAdd() has failed". Such
Line 146: an error message does not inform us about exactly what has failed: i.e. which feature of the class
Line 147: tested is not working properly. Because of this, method names started to grow and contain much more
Line 148: information. For example testConstructor() was split into several more focused test methods with
Line 149: names like testConstructorThrowsExceptionForInvalidArguments().
Line 150:  This was definitely a step in the right direction, but still not quite good enough. Developers at
Line 151: this time were fascinated by the expressiveness of new dynamic languages (e.g. Ruby2) and fluent
Line 152: interfaces3, and this meant they were really irritated by the presence of this obligatory test prefix.
Line 153: Many of us demanded that failed test messages should be readable as proper English sentences (or, at
Line 154: least, be as close to this ideal as possible). The rescue came with a new wave of testing frameworks
Line 155: (TestNG in particular) which used annotations instead of method names patterns to recognize test
Line 156: methods. This made it possible to come up with a more readable naming pattern.
Line 157: This new pattern was based on the idea that the test method name should convey information about
Line 158: the following:
Line 159: • preconditions of the test - the state of the SUT and the environment before the test,
Line 160: • triggering actions - what makes the SUT act in the expected way,
Line 161: • expected results of the test - what should be returned by the SUT, or what state the SUT should be
Line 162: in after the test is finished, or what actions should be performed by the SUT during the test,
Line 163: • optionally, the name or role of the SUT,
Line 164: • in addition, the test prefix was replaced with should, which allows one to create specification-like
Line 165: method names.
Line 166: 2http://ruby-lang.org
Line 167: 3http://en.wikipedia.org/wiki/Fluent_interface
Line 168: 187
Line 169: 
Line 170: --- 페이지 203 ---
Line 171: Chapter 10. Organization Of Tests
Line 172: Of course, it is usually not possible to include a full description of all these kinds of information in
Line 173: the method name itself. What is possible, though, is to include just enough details to convey the main
Line 174: purpose of the test. Also, each of the elements can be omitted, if its presence does not enhance the
Line 175: readability of the test method.
Line 176: Table 10.1 provides some examples of test method names which follow the guidelines described
Line 177: above.
Line 178: Table 10.1. Examples of test method names
Line 179: class name
Line 180: test methods
Line 181: constructorShouldThrowExceptionForNullUser()
Line 182: OrderTest
Line 183: constructorShouldCreateValidOrderForValidUser()
Line 184: shouldNotAcceptDictionaryBasedPasswords()
Line 185: shouldNotAcceptPasswordWithoutDigits()
Line 186: shouldNotAcceptShortPasswords()
Line 187: PasswordValidatorTest
Line 188: shouldAcceptLongComplicatedPassword()
Line 189: shouldAllowToBookTableForOneHourAndMore()
Line 190: shouldDisallowToBookForLessThanHour()
Line 191: shouldAllowToCreateRecurrentReservation()
Line 192: BookingSystemTest
Line 193: shouldAllowToCancelExistingReservation()
Line 194: In the case of the examples presented above, all test method names specify exactly what is expected
Line 195: of the SUT (e.g. shouldNotAccept…(), shouldAllow…()), and under what conditions or with what
Line 196: arguments (e.g. …PasswordsWithoutDigits(), …ExistingReservation()). When a test fails, the
Line 197: first line of the message already furnishes us with enough information to understand what it is that is
Line 198: not working properly.
Line 199: What is attractive about this naming schema is that it leaves some room for customization. Some
Line 200: of the examples presented above do not start with should, but with the constructor prefix, which
Line 201: makes it clearer which part of the SUT is being tested by a particular method.
Line 202: Test method names are of secondary importance compared to their content, but they can
Line 203: push your thinking in the right direction - or, for that matter, the wrong one. The use of
Line 204: the "should" prefix helps (some people would say forces) us to focus on the expected
Line 205: behaviour of the SUT, and leads to "testing behaviour and not methods" (see Section 11.1).
Line 206: Thinking in terms of the responsibilities of the SUT will make you test at the right level of
Line 207: abstraction. This is especially important when coding code-first, because it is then so very
Line 208: easy to test implementation details instead of the behaviour of an external SUT.
Line 209: 10.2.3. Naming of Test-Double Variables
Line 210:   Let us take a look at the variable names we have used so far when working with test doubles. An
Line 211: example is given in the listing below.
Line 212: Listing 10.1. Original variables' names
Line 213: Messenger messenger;
Line 214: 188
Line 215: 
Line 216: --- 페이지 204 ---
Line 217: Chapter 10. Organization Of Tests
Line 218: TemplateEngine templateEngine;
Line 219: MailServer mailServer;
Line 220: The names of variables, as shown in Listing 10.1, inform us about the types of objects (e.g. it is
Line 221: obvious that mailServer is of the MailServer type). However, they do not convey any information
Line 222: concerning the role which these objects play in our tests. One of them is an SUT, another one a test
Line 223: spy, another a stub. Yet this difference is not expressed by the names of the variables in test code, and
Line 224: can only be discovered on closer inspection.
Line 225: Some people suggest giving more intention-revealing names to all variables. For example:
Line 226: Listing 10.2. Intention-revealing names of variables
Line 227: Messenger sut;
Line 228: TemplateEngine stubTemplateEngine;
Line 229: MailServer spyMailServer;
Line 230: This version of the names of the variables gives much more insight into their purpose in test
Line 231: class. A single glance is sufficient to let us know that the real testing is to be done using sut and
Line 232: spyMailServer, while stubTemplateEngineReq is only assisting in this process.
Line 233: Another variation of this idea is to reverse the order and put the type of test double as a suffix, e.g.
Line 234: mailServerSpy, templateEngineStub. This way the information concerning the type of the object is
Line 235: more easily visible – something which some people consider more valuable.
Line 236: It is up to you to decide whether you find this worthwile. With short tests, with a very limited number
Line 237: of DOCs (as they should be), these additional hints, embedded within the variable names, are rather
Line 238: unnecessary. If you have more DOCs and more complex tests than it may help you to understand the
Line 239: tests. On the other hand, short, simple, focused tests are what we should be striving for, so instead of
Line 240: renaming variables, maybe it would be better just to write better tests.
Line 241: Whatever naming scheme you decide to follow, please make sure you feel comfortable
Line 242: with it (and that so do your colleagues).
Line 243: 10.3. Comments in Tests
Line 244: Good code is its own best documentation. As you’re about to add a comment, ask
Line 245: yourself, "How can I improve the code so that this comment isn’t needed?"
Line 246: — Steve McConnell Code Complete (1993)
Line 247: When it comes to comments, the same rules apply as with production code. In general, it is better to
Line 248: have clean code with no comments than perfectly commented-upon spaghetti-code. In general:
Line 249: • do not comment on the obvious,
Line 250: • comment on everything that might surprise your fellow developers (explain why you have chosen
Line 251: such a strange, non-standard way of doing something…),
Line 252: • give information about any important things which cannot be read off directly from the code (e.g.
Line 253: the business purpose of some test).
Line 254: 189
Line 255: 
Line 256: --- 페이지 205 ---
Line 257: Chapter 10. Organization Of Tests
Line 258: If you stick to these simple guidelines, your code will have a minimal number of comments, and only
Line 259: valuable ones at that. The old truth about good code not needing comments is even more true with test
Line 260: code. Here are several reasons why comments in test code are rarely required:
Line 261: • Test code should be (and hopefully is) very simple. It is all about arrange/act/assert – the creation of
Line 262: objects, execution of methods and verification of results. If you keep it simple, then there should be
Line 263: nothing complex which requires comments.
Line 264: • By giving descriptive names to variables, test classes and test methods (see Section 10.2), you
Line 265: ensure that there will be no need to include any comments. All important information can be read
Line 266: off from the code itself.
Line 267: Personally, my test code is almost free of comments. There are only three situations where
Line 268: I (sometimes) put comments in code. First, when adding a test because of a reported bug. In such
Line 269: a case, I usually add a link to the issue on bug tracker, and (optionally) write a short explanation of
Line 270: what the problem was. Sometime, I also add a comment on the reasons for selecting a particular set
Line 271: of test data. This often has something to do with business requirements, and cannot be read from the
Line 272: code. It also happens that some tests of legacy code which use non-standard techniques (like the
Line 273: ones described in Section 8.7) require a comment. Apart from these rare occasions, I do not comment
Line 274: on my test code at all.
Line 275: 10.4. BDD: ‘Given’, ‘When’, ‘Then’
Line 276: BDD is a second-generation, outside–in, pull-based, multiple-stakeholder, multiple-
Line 277: scale, high-automation, agile methodology. It describes a cycle of interactions with
Line 278: well-defined outputs, resulting in the delivery of working, tested software that matters.
Line 279: — Dan North
Line 280: In this section I would like to present a slightly different style of writing unit tests. This style comes
Line 281: from the Behaviour-Driven Development (BDD) approach.
Line 282: Because BDD is more applicable to higher-level tests (i.e. end-to-end tests) than unit testing, I will
Line 283: not explain it in detail. There are numerous good sources on the Internet explaining BDD, and I would
Line 284: encourage you to spend some time reading about it. What I would suggest is that we concentrate on
Line 285: the technical aspects of writing unit tests BDD-style. Before doing this, let me quickly introduce BDD
Line 286: in a few sentences:
Line 287: • BDD was introduced by Dan North in 2003.
Line 288: • BDD is more customer-oriented than TDD, mainly because its primary use is in higher level tests.
Line 289: Some BDD ideas are applicable to unit tests (and with very good results).
Line 290: • BDD pays a great deal of attention to the readability of tests. Many BDD frameworks allow tests to
Line 291: be written in almost natural language.
Line 292: • Some people say that BDD is a "TDD done right" – one more reason to put some effort into
Line 293: learning it.
Line 294: In fact, some elements presented in this book - for example the test methods naming schema in
Line 295: Section 10.2 - are very compatible with what BDD suggests, so we could even say that we have
Line 296: already had a taste of doing things BDD-style. However, most developers link BDD to the famous
Line 297: 190
Line 298: 
Line 299: --- 페이지 206 ---
Line 300: Chapter 10. Organization Of Tests
Line 301: ‘given/when/then’ pattern, which is a trademark of BDD. And that is exactly what I would like to
Line 302: discuss in this section.
Line 303: The idea of given/when/then comes from scenarios4 being written in the following manner:
Line 304: Given some initial context (the givens), When an event occurs, Then ensure some
Line 305: outcomes.
Line 306: — Dan North Introducing BDD (2006)
Line 307: An exemplary scenario written in such a manner could be the following:
Line 308: • Given that a user John is logged in,
Line 309: • When he clicks a profile button,
Line 310: • Then a page profile filled with his data is displayed.
Line 311: 10.4.1. Testing BDD-Style
Line 312:  JUnit does not provide any syntactic sugar to support BDD. The usual way of mimicking the style of
Line 313: BDD is by putting the ‘given/when/then’ words in comments, as shown in Listing 10.35. This code is
Line 314: an equivalent of a test we have already discussed in Section 11.1.
Line 315: Listing 10.3. Testing a BankAccount class - BDD style
Line 316: public class BankAccountBDDTest {
Line 317:     @Test
Line 318:     void shouldBeEmptyAfterCreation() {
Line 319:         // given
Line 320:         // when
Line 321:         BankAccount account = new BankAccount();
Line 322:         // then
Line 323:         int balance = account.getBalance();
Line 324:         assertThat(balance).isEqualTo(0);
Line 325:     }
Line 326:     @Test
Line 327:     void shouldAllowToCreditAccount() {
Line 328:         // given
Line 329:         BankAccount account = new BankAccount();
Line 330:         // when
Line 331:         account.deposit(100);
Line 332:         // then
Line 333:         int balance = account.getBalance();
Line 334:         assertThat(balance).isEqualTo(100);
Line 335:     }
Line 336:     @Test
Line 337:     void shouldAllowToDebitAccount() {
Line 338: 4A BDD scenario is a rough equivalent of requirements and/or test cases
Line 339: 5Some people suggest that adding empty lines instead of given/when/then words is good enough. I agree.
Line 340: 191
Line 341: 
Line 342: --- 페이지 207 ---
Line 343: Chapter 10. Organization Of Tests
Line 344:         // given
Line 345:         BankAccount account = new BankAccount();
Line 346:         // when
Line 347:         account.deposit(100);
Line 348:         account.withdraw(40);
Line 349:         // then
Line 350:         int balance = account.getBalance();
Line 351:         assertThat(balance).isEqualTo(60);
Line 352:     }
Line 353: }
Line 354: Anything shocking in the above listing? I do not think so. It only differs from what we have been
Line 355: discussing so far in respect of a few details:
Line 356: • slightly longer test methods, which contain everything that is required to test a certain story
Line 357: (including setting up of objects),
Line 358: • a clear structure for each of the test methods,
Line 359: • clear separation of action (e.g. account.getBalance()) and assertion (e.g.
Line 360: assertThat(balance).isEqualTo(60)).
Line 361: When it comes to unit tests, there is no such thing as an instance of "pure" BDD. Listing
Line 362: 10.3 shows one possible way to write this test BDD-style, but this is probably not the only
Line 363: valid way to do it.
Line 364: As Listing 10.3 shows, in BDD the structure of the test method is really important. Some
Line 365: test methods are (slightly) longer than necessary, just to satisfy the clear separation
Line 366: between the when and given phases (e.g. there is no need for a balance variable to exist -
Line 367: assertThat(account.getBalance()).isEqualTo(60) would suffice). This approach brings a lot of
Line 368: clarity, and a little bit of redundancy, to every test method.
Line 369: 10.4.2. Mockito BDD-Style
Line 370:  In contrast to JUnit, Mockito facilitates writing tests BDD-style. It provides a BDDMockito
Line 371: class, which allows you to use a given() method in the same way as we have been using the
Line 372: Mockito.when() method up to now (i.e. to set expectations on test doubles). This makes Mockito
Line 373: tests more BDD-like. Listing 10.4 shows this.
Line 374: Listing 10.4. Mockito test - BDD style
Line 375: import static org.mockito.BDDMockito.given; 
Line 376: public class BddMockitoTest {
Line 377:     private static final int ID_USER = 329847;
Line 378:     @Test
Line 379:     void shouldReturnClient() {
Line 380:         // given
Line 381:         User USER = new User();
Line 382:         UserDAO dao = mock(UserDAO.class); 
Line 383:         UserService service = new UserService(dao); 
Line 384: 192
Line 385: 
Line 386: --- 페이지 208 ---
Line 387: Chapter 10. Organization Of Tests
Line 388:         given(dao.getUser(ID_USER)).willReturn(USER); 
Line 389:         // when
Line 390:         User user = service.loadUser(ID_USER);
Line 391:         // then
Line 392:         assertThat(user).isEqualTo(USER);
Line 393:     }
Line 394: }
Line 395: Importing of a given() method of the BDDMockito class.
Line 396: Setting up the SUT (service) and injecting a test double (dao).
Line 397: Use of a given() method helps to keep the BDD given/when/then rhythm. It is equivalent to
Line 398: when(dao.getUser(ID_USER)).thenReturn(USER);, but does not use a when() method,
Line 399: which would be confusing as we are still in the "given" part of the test code.
Line 400: As shown in the listing above, this amounts to a nice piece of syntactic sugar, but nothing
Line 401: groundbreaking. However, it does help to express the rhythm of a BDD test, which is a good thing.
Line 402: 10.5. Reducing Mockito Boilerplate Code
Line 403: If you work with Mockito a lot, you might be interested in cutting down the boilerplate code of test
Line 404: doubles creation. All those instances of myMock = mock(SomeClass.class), which seem to show up
Line 405: in every test method, are really annoying, right? The good news is that Mockito makes it possible to
Line 406: get rid of the boilerplate code. In this section we will take a look at Mockito’s annotations and its one-
Line 407: liner stubbing feature.
Line 408: Consistency is good. Whether you decide to use the features presented in this section or
Line 409: choose not to do so, be consistent about this.
Line 410: Listing 10.5 shows two simple classes which will be used to demonstrate these new Mockito features.
Line 411: Their names - SUT and Collaborator - reveal their purpose clearly, in both cases.
Line 412: Listing 10.5. SUT and Collaborator classes
Line 413: public class Collaborator {
Line 414:     public String doSth() {
Line 415:         return "xyz"; 
Line 416:     }
Line 417: }
Line 418: public class SUT {
Line 419:     private Collaborator collaborator;
Line 420:     public void setCollaborator(Collaborator collaborator) {
Line 421:         this.collaborator = collaborator;
Line 422:     }
Line 423:     public String useCollaborator() {
Line 424:         return collaborator.doSth(); 
Line 425:     }
Line 426: }
Line 427: 193
Line 428: 
Line 429: --- 페이지 209 ---
Line 430: Chapter 10. Organization Of Tests
Line 431: The default value returned by the doSth() method is "xyz",
Line 432: A simple delegating method which is supposed to return what collaborator returns.
Line 433: A typical test for this sort of functionality is shown below. I have decided to use a setUp() method
Line 434: this time, because I believe this is a more common scenario.
Line 435: Listing 10.6. Typical test with a lot of boilerplate code
Line 436: public class BoilerplateCodeTest {
Line 437:     private Collaborator collaborator;
Line 438:     private SUT sut;
Line 439:     @BeforeEach
Line 440:     void setUp() { 
Line 441:         sut = new SUT();
Line 442:         collaborator = Mockito.mock(Collaborator.class);
Line 443:         sut.setCollaborator(collaborator);
Line 444:     }
Line 445:     @Test
Line 446:     void shouldReturnABC() {
Line 447:         when(collaborator.doSth()).thenReturn("abc");
Line 448:         assertThat(sut.useCollaborator()).isEqualTo("abc");
Line 449:     }
Line 450: }
Line 451: This is where the repetitive code occurs – the creation of the SUT, the creation of test doubles
Line 452: and injecting them.
Line 453: The question is whether we can do anything about this.
Line 454: Please bear in mind that under "normal" circumstances, the boilerplate code section is
Line 455: much larger than shown in Listing 10.6. Usually there will be more than one test double
Line 456: in your code. Multiply it by the number of tests which use test doubles and the reason for
Line 457: cutting down the size of all of the set up activities becomes evident.
Line 458: 10.5.1. One-Liner Stubs
Line 459:   The first thing we can do is to make the creation and stubbing of collaborator slightly shorter.
Line 460: Mockito allows for one-line stubbing, which is shown in Listing 10.7.
Line 461: Listing 10.7. Reducing boilerplate code with one-line stubbing
Line 462: public class OneLinerStubbingTest {
Line 463:     private Collaborator collaborator =
Line 464:         when(mock(Collaborator.class).doSth())
Line 465:             .thenReturn("abc").getMock(); 
Line 466:     private SUT sut;
Line 467:     @BeforeEach
Line 468:     void setUp() { 
Line 469:         sut = new SUT();
Line 470:         sut.setCollaborator(collaborator);
Line 471:     }
Line 472: 194
Line 473: 
Line 474: --- 페이지 210 ---
Line 475: Chapter 10. Organization Of Tests
Line 476:     @Test
Line 477:     void shouldReturnABC() {
Line 478:         assertThat(sut.useCollaborator()).isEqualTo("abc");
Line 479:     }
Line 480: }
Line 481: In this line, a test double gets created and stubbed. Note the getMock() method at the end of the
Line 482: invocation chain.
Line 483: No test double creation in setUp() method.
Line 484: This is a nice trick which brings some code reduction. You might consider putting collaborator
Line 485: creation and stubbing in your setUp() method, so that all creation code is in one place.
Line 486: 10.5.2. Mockito Annotations
Line 487:      Now let us move on to the main point of boilerplate code reduction. An example of what can be
Line 488: achieved is shown in Listing 10.8.
Line 489: To make the magic happen, we need imports from two projects - JUnit 5 and Mockito:
Line 490: import org.junit.jupiter.api.extension.ExtendWith;
Line 491: import org.mockito.Mock;
Line 492: import org.mockito.junit.jupiter.MockitoExtension;
Line 493: import org.mockito.InjectMocks;
Line 494: Listing 10.8. Creating & injecting test doubles using annotations
Line 495: @ExtendWith(MockitoExtension.class) 
Line 496: public class InjectMocksTest {
Line 497:     @Mock 
Line 498:     private Collaborator collaborator;
Line 499:     @InjectMocks 
Line 500:     private SUT sut = new SUT();
Line 501:     @Test
Line 502:     void shouldReturnABC() {
Line 503:         when(collaborator.doSth()).thenReturn("abc");
Line 504:         assertThat(sut.useCollaborator()).isEqualTo("abc");
Line 505:     }
Line 506: }
Line 507: This line instructs JUnit to use Mockito extension. This will result in the creation of test doubles
Line 508: for all fields marked with an @Mock annotation.
Line 509: The collaborator, which will be replaced by a test double, is marked with an @Mock annotation.
Line 510: No Mockito.mock(…) required!
Line 511: Another surprise! We asked Mockito to inject our collaborator into sut using @InjectMocks
Line 512: annotation. No need to write sut.setCollaborator(collaborator) anymore!
Line 513: Now, that was interesting. There was no explicit line creating a test double, and yet it behaved as
Line 514: if it had been created in the usual way. No setting of collaborator, and still the execution of the
Line 515: useCollaborator() method does not fail with a NullPointerException! In reality the collaborator
Line 516: 195
Line 517: 
Line 518: --- 페이지 211 ---
Line 519: Chapter 10. Organization Of Tests
Line 520: is injected to the SUT behind the scenes. Mockito does this by matching available test doubles with
Line 521: the SUT’s fields.
Line 522: In (rare) cases where you have more than one collaborator of the same kind, you could
Line 523: use the name attribute of the @Mock annotation to instruct Mockito about which field of the
Line 524: SUT should be replaced with which test double. Please consult the Mockito documentation
Line 525: for details.
Line 526: Even in such simple case as presented in Listing 10.8, the code looks nicer now thanks to @Mock and
Line 527: @InjectMocks annotation. If you use this technique for a whole suite, with many test methods and
Line 528: many test doubles, then the decrease in the number of code lines would be even more visible.
Line 529: You will be even more surprised when you remove the setter (the setCollaborator()
Line 530: method) from the SUT class, and watch the test still work. This is because Mockito does
Line 531: not really execute setters to set fields, but uses a reflection mechanism to modify them
Line 532: directly.
Line 533: Now, let us summarize and discuss what we have just been learning about.
Line 534: In our pursuit of better, cleaner, more readable test code, we have learned about Mockito annotations
Line 535: - @Mock and @InjectMocks. Both can be used to cut down the boilerplate code related to the creation
Line 536: and injection of mocks. By using them, we have:
Line 537: • shortened the setup phase of the test code,
Line 538: • got rid of repetitive, boilerplate test double creation and code setting.
Line 539: Using @Mock and @InjectMocks annotations might have both good and bad effects on the readability
Line 540: of your code. On the one hand, the code becomes more concise, and ceases to be cluttered up with
Line 541: repetitive statements. On the other, with larger tests you can lose track of "what was created where",
Line 542: and achieve the opposite effect – namely, that of diminished readability.
Line 543: Please make sure you read carefully about the annotations presented in this section in the Mockito
Line 544: documentation. There are some gotchas which might take you by surprise if and when you use them.
Line 545: Mockito offers several more annotations similar to the @Mock annotation; however, their
Line 546: use is very limited. Please consult the Mockito documentation to learn about them.
Line 547: Getting rid of static imports
Line 548: Last but not least, if you are being irritated by the need to add static imports of Mockito
Line 549: classes, check Marcin Szpak’s blog post [https://solidsoft.wordpress.com/2015/12/01/using-
Line 550: mockito-without-static-imports-with-java-8/] on how to use default methods of interfaces to
Line 551: avoid worrying about imports.
Line 552: 10.6. Creating Complex Objects
Line 553: Up till now, all the objects we have created for testing purposes have been dead simple. That may
Line 554: have been handy for demonstrating various different issues involved in unit testing, but it has not been
Line 555: 196
Line 556: 
Line 557: --- 페이지 212 ---
Line 558: Chapter 10. Organization Of Tests
Line 559: at all realistic. In this section we take a look at issues relating to the creation of complex objects for
Line 560: test purposes.
Line 561: Writing tests which use rich domain objects can turn out to be tedious work. To test their different
Line 562: functionalities you need to set them with different sets of properties. Unfortunately this results in long
Line 563: and obscure tests, which are hard to understand or maintain. The following features are symptomatic
Line 564: of a weak approach to test fixture creation:
Line 565: • a lot of test fixture code in every test method,
Line 566: • duplicated code - usually because multiple tests require similar (but not identical!) objects,
Line 567: • test abstraction polluted by detailed objects creation parts.
Line 568: A common approach to improving this situation is to create some private methods that will be
Line 569: responsible for the creation of domain objects. Unfortunately, often this does not really cure the
Line 570: illness, but replaces it with another one - an entangled web of small methods calling one another. This
Line 571: might be a real nightmare to understand, debug and maintain.
Line 572: In this section we will learn about two approaches to dealing with domain objects creation. They are
Line 573: not guaranteed to make our tests perfect in this respect, but their use should at least limit the harm
Line 574: done by test fixture setup code.
Line 575: In my "career" as a code reviewer, I have witnessed many tests which have been
Line 576: completely unreadable, owing to the chaotic way in which the domain objects had been
Line 577: created.
Line 578:  For the purposes of our discussion we will be using a simple Employee class. Let us assume that this
Line 579: class is immutable6 - something which, in general, is a good thing. There is no point in showing the
Line 580: code of Employee. For the sake of the ensuing discussion it will suffice to say that it has numerous
Line 581: fields (some being primitives and some objects of the Address, Phone and Position types), and that
Line 582: all its fields are initialized via a constructor (no setters).
Line 583: This time we are not really interested in tests (assertion) as such, but only in that part of them which is
Line 584: responsible for objects creation. An example of Employee objects creation within test code is shown
Line 585: below.
Line 586: Listing 10.9. Utility method to create employees
Line 587: public class EmployeeTest {
Line 588:     private static Phone MOBILE_PHONE = new Phone("123-456-789"); 
Line 589:     private static Phone STATIONARY_PHONE = new Phone("123-456-789");
Line 590:     private static Address HOME_ADDRESS = new Address("any street");
Line 591:     private Employee createEmployee(String name, String surname,
Line 592:                         Position position) {
Line 593:         return new Employee(name, surname, position,
Line 594:             HOME_ADDRESS, MOBILE_PHONE, STATIONARY_PHONE); 
Line 595:     }
Line 596: 6See http://en.wikipedia.org/wiki/Immutable_object
Line 597: 197
Line 598: 
Line 599: --- 페이지 213 ---
Line 600: Chapter 10. Organization Of Tests
Line 601: Some properties of the Employee class, not important to the test cases, are reused between tests.
Line 602: Listing 10.10. Creation of employess
Line 603:     @Test
Line 604:     void ceoCanDoEverything() { 
Line 605:         Calendar cal = Calendar.getInstance();
Line 606:         cal.set(2010, 3, 1);
Line 607:         Date startCeo = cal.getTime();
Line 608:         cal.add(Calendar.DATE, 1);
Line 609:         Date endCeo = cal.getTime();
Line 610:         Position pm = new Position("ceo", startCeo, endCeo);
Line 611:         Employee ceoEmpl = createEmployee("ceoName", "ceoSurname", pm); 
Line 612:         // some methods execution and assertions here
Line 613:     }
Line 614:     @Test
Line 615:     void pmCanDoALot() { 
Line 616:         Calendar cal = Calendar.getInstance();
Line 617:         cal.set(2008, 7, 12);
Line 618:         Date startPm = cal.getTime();
Line 619:         cal.add(Calendar.YEAR, 3);
Line 620:         Date endPm = cal.getTime();
Line 621:         Position pm = new Position("pm", startPm, endPm);
Line 622:         Employee pmEmpl = createEmployee("pmName", "pmSurname", pm); 
Line 623:         // some methods execution and assertions here
Line 624:     }
Line 625: }
Line 626: Both test methods contain similar, yet slightly different, code, responsible for the creation of an
Line 627: employee.
Line 628: Execution of the createEmployee() method.
Line 629: There is nothing special about the code shown above. It is the kind of code that all of us have created
Line 630: more than once. It is not especially nice or readable, but it serves its purpose. A private method
Line 631: createEmployee() facilitates, at least to some extent, the creation of similar objects.
Line 632: The test code shown in Listing 10.10 is aware of the details of the Employee class. There is no
Line 633: reasonable abstraction which would make reading the code easier. All we really want to do in the test
Line 634: methods is create a project manager and a CEO. But it is not possible to do this "just like that" - we
Line 635: need to go deep into some properties of the Employee class to achieve this simple thing. This lowers
Line 636: the readability of the test code.
Line 637: Looking at the code in Listing 10.10, we can predict its future evolution. Probably some more static
Line 638: values will be used (e.g. are start and end dates important? - if not they will end up as static values).
Line 639: During the implementation of more sophisticated test scenarios, it will transpire that some properties
Line 640: of employees, e.g. mobile phone, will become important. Then, new private utility methods will be
Line 641: created, to make it possible to create employees with certain fields set with default or custom values.
Line 642: Private methods will start to call one another (code reuse is good, is it not?) and the code will grow.
Line 643: Very soon, working with it will not be a pleasure anymore.
Line 644: The immutability of objects, which in general is a good thing, makes creating multiple
Line 645: objects of the same kind rather cumbersome. You cannot reuse an object created in one test
Line 646: method (or in some "setup" section) and change some of its properties using setters. If the
Line 647: Employee class had not been immutable, then it would have been easier to reuse it across
Line 648: 198
Line 649: 
Line 650: --- 페이지 214 ---
Line 651: Chapter 10. Organization Of Tests
Line 652: tests. In the ensuing sections we will learn how to make immutability less difficult to work
Line 653: with. 
Line 654: 10.6.1. Mummy Knows Best
Line 655:  It is time to introduce an Object Mother pattern. Basically, this is a Factory pattern7, whose purpose
Line 656: is test fixture creation. Each Object Mother method creates a single aggregate. Object Mother
Line 657: centralizes objects creation and makes tests more readable by providing intention-revealing methods.
Line 658: We can think of Object Mother as a more object-oriented alternative to the private utility methods
Line 659: presented in the previous section. If we were to move the code from both of the test methods shown
Line 660: in Listing 10.10 to a separate class, we could then rewrite the test code, so that it would then look as
Line 661: shown in Listing 10.11.
Line 662: Listing 10.11. Object Mother pattern
Line 663: public class EmployeeObjectMotherTest {
Line 664:     @Test
Line 665:     void ceoCanDoEverything() {
Line 666:         Employee empl = ObjectMotherEmployee.ceoEmployee();
Line 667:         // some methods execution and assertions here
Line 668:     }
Line 669:     @Test
Line 670:     void pmCanDoALot() {
Line 671:         Employee empl = ObjectMotherEmployee.pmEmployee();
Line 672:         // some methods execution and assertions here
Line 673:     }
Line 674: }
Line 675: The above code is much clearer, and does not delve into the implementation details of the Employee
Line 676: class. All this is enclosed within the ObjectMotherEmployee class. This kind of separation of
Line 677: concerns between test code and objects creation code is definitely a good thing.
Line 678: In some implementations, Object Mother goes beyond the standard factory pattern by providing
Line 679: methods which facilitate changing objects during tests. For example, an addAddress() method can
Line 680: be used to simplify the setting of a new employee’s address. It can even work with an immutable
Line 681: Employee class: for example, by copying data from one Employee object into another, via a
Line 682: constructor.
Line 683:  On the downside, let us note that the ObjectMotherEmployee class might soon become quite bloated.
Line 684: Eventually, we may end up with numerous Object Mothers (calling one another), or with an Object
Line 685: Mother with plenty of methods (making it a God Object8) - hard both to understand and to maintain.
Line 686: 10.6.2. Test Data Builder
Line 687:  Another approach we can adopt is to employ a different creational pattern. This one - called Test
Line 688: Data Builder - was also created with test code in mind. It requires some additional coding, but in
Line 689: return it offers a kind of internal DSL - one specializing in objects creation. This opens up some new
Line 690: possibilities.
Line 691: 7See http://www.oodesign.com/factory-pattern.html
Line 692: 8See http://en.wikipedia.org/wiki/God_object
Line 693: 199
Line 694: 
Line 695: --- 페이지 215 ---
Line 696: Chapter 10. Organization Of Tests
Line 697: Let us have a look at the code shown in Listing 10.12. It presents a new class - EmployeeBuilder -
Line 698: which will be used to construct very different objects of the Employee type. Some of its fields and
Line 699: methods have been omitted for the sake of brevity.
Line 700: Listing 10.12. Test Data Builder pattern
Line 701: public class EmployeeBuilder {
Line 702:     private String firstname;
Line 703:     private String lastname;
Line 704:     private Address address;
Line 705:     ... some more fields here
Line 706:     private Position position;
Line 707:     public EmployeeBuilder withFirstname(String firstname) { 
Line 708:         this.firstname = firstname;
Line 709:         return this;
Line 710:     }
Line 711:     public EmployeeBuilder withLastname(String lastname) {
Line 712:         this.lastname = lastname;
Line 713:         return this;
Line 714:     }
Line 715:     public EmployeeBuilder withAddress(Address address) {
Line 716:         this.address = address;
Line 717:         return this;
Line 718:     }
Line 719:     ... some more similar methods here
Line 720:     public EmployeeBuilder withPosition(Position position) {
Line 721:         this.position = position;
Line 722:         return this;
Line 723:     }
Line 724:     public Employee build() {
Line 725:         return new Employee(firstname, lastname,
Line 726:             position, address, mobile, stationary); 
Line 727:     }
Line 728: }
Line 729: Each field of the Employee class is represented by a setter method which returns an instance of
Line 730: EmployeeBuilder. This allows us to chain the methods in any order.
Line 731: The build() method calls a constructor of the Employee class and returns the result of the
Line 732: creation.
Line 733: In addition to EmployeeBuilder, we also need builders for all of the other domain classes that
Line 734: will be used (by composition) by the Employee class. Such builders would be very similar to the
Line 735: EmployeeBuilder class we were discussing earlier. Listing 10.13 provides an example of another
Line 736: builder.
Line 737: Listing 10.13. Test Data Builder used to create Position class
Line 738: public class PositionBuilder {
Line 739: 200
Line 740: 
Line 741: --- 페이지 216 ---
Line 742: Chapter 10. Organization Of Tests
Line 743:     private String title;
Line 744:     private Date from;
Line 745:     private Date to;
Line 746:     public PositionBuilder withTitle(String title) {
Line 747:         this.title = title;
Line 748:         return this;
Line 749:     }
Line 750:     public PositionBuilder start(int year, int month, int day) {
Line 751:         Calendar cal = Calendar.getInstance();
Line 752:         cal.set(year, month, day);
Line 753:         this.from = cal.getTime();
Line 754:         return this;
Line 755:     }
Line 756:     public PositionBuilder end(int year, int month, int day) {
Line 757:         Calendar cal = Calendar.getInstance();
Line 758:         cal.set(year, month, day);
Line 759:         this.to = cal.getTime();
Line 760:         return this;
Line 761:     }
Line 762:     public Position build() {
Line 763:         return new Position(title, from, to);
Line 764:     }
Line 765: }
Line 766: What is interesting in Listing 10.13 are its start() and end() methods. They take integers (year,
Line 767: month, day) as parameters, which, as we shall see in a minute, make them easier to use. By using
Line 768: primitives in the API of this builder, we free up its clients from being involved in the cumbersome
Line 769: process of creating Date objects.
Line 770: Let us now take a look at how two such builders might be used in tests. This is shown in Listing
Line 771: 10.14.
Line 772: Listing 10.14. Test Data Builder pattern used in test code
Line 773: public class EmployeeTestDataBuilderTest {
Line 774:     private EmployeeBuilder anEmployee() { 
Line 775:         return new EmployeeBuilder()
Line 776:             .withFirstname("John").withLastname("Doe")
Line 777:             .withMobile(
Line 778:                 new PhoneBuilder().withNumber("123-456-789").build())
Line 779:             .withStationary(
Line 780:                 new PhoneBuilder().withNumber("456-789-012").build())
Line 781:             .withAddress(
Line 782:                 new AddressBuilder().withStreet("Some Street").build());
Line 783:     }
Line 784:     @Test
Line 785:     void pmCanDoALot() {
Line 786:         Employee pmEmpl = anEmployee() 
Line 787:             .withPosition(
Line 788:                 new PositionBuilder().withTitle("PM") 
Line 789:                     .start(2010, 1, 1).end(2011, 7, 3).build()) 
Line 790: 201
Line 791: 
Line 792: --- 페이지 217 ---
Line 793: Chapter 10. Organization Of Tests
Line 794:             .build();
Line 795:         // some methods execution and assertions here
Line 796:     }
Line 797:     @Test
Line 798:     void ceoCanDoEverything() {
Line 799:         Employee ceoEmpl = anEmployee() 
Line 800:             .withPosition(
Line 801:                 new PositionBuilder().withTitle("CEO") 
Line 802:                     .start(2011, 1, 1).end(2011, 5, 5).build()) 
Line 803:             .build();
Line 804:         // some methods execution and assertions here
Line 805:     }
Line 806: }
Line 807: Here we have a utility method which creates a "typical" employee, that will then be modified
Line 808: further. Please note, this method returns an EmployeeBuilder. Another option would be to
Line 809: move this method to the EmployeeBuilder class (and also make it static).
Line 810: When creating objects, the anEmployee() utility method is used. This allows us to express
Line 811: things like "CEO is an employee but with such and such properties", etc.
Line 812: If objects of other types are required, their builders are created and called.
Line 813: The use made here of the start() and end() methods of PositionBuilder is very simple
Line 814: indeed. There is no need to create objects of the Date type.
Line 815:  I remember when I first saw this pattern in action: it felt very awkward to me. Back then, I found this
Line 816: kind of code hard to read. But that was only a first impression. After some time spent studying this
Line 817: pattern, I discovered that it confers several benefits:
Line 818: • In contrast to private methods with multiple parameters, in the case of Test Data Builders the
Line 819: meaning of each value is very clear. There is no confusion about what the name of a person or
Line 820: street, the title of a song, etc., is. Every value can be easily recognized by the method name it is
Line 821: passed to.
Line 822: • The test code can be read without problems (once you get used to it). It is clear what the properties
Line 823: of each created object are.
Line 824: • Even though the Employee objects are immutable, EmployeeBuilder objects are not. This means
Line 825: we can reuse and modify them.
Line 826: • There is no temptation to create various constructors of the Employee class.
Line 827: • Writing such code is an agreeable experience, because the IDE will prompt you with auto-complete
Line 828: hints. You can also add some syntactic sugar methods (like but() or and() methods) which will
Line 829: improve the readability of the code still further.
Line 830: On the downside, we have to mention that the creation of builders requires some (maybe even
Line 831: significant) coding. However, let us remember that the implementation of each builder is trivial.
Line 832: Several projects - including Jilt9 and Project Lombok10 - facilitate the creation of Test Data
Line 833: Builders. Check them out!
Line 834: 9https://github.com/skinny85/jilt
Line 835: 10https://projectlombok.org/features/Builder
Line 836: 202
Line 837: 
Line 838: --- 페이지 218 ---
Line 839: Chapter 10. Organization Of Tests
Line 840: 10.6.3. Conclusions
Line 841: In this section we have taken a closer look at how more complex objects could be created within test
Line 842: code.
Line 843: First, a "natural", unstructured approach was presented. This approach can be recommended only for
Line 844: very simple domain models. If used for the creation of many different complex objects, then the test
Line 845: code will be very hard to understand and maintain.
Line 846: Then we introduced an Object Mother pattern. It encapsulates objects creation code and provides
Line 847: some intention-revealing methods. Thanks to this the test code itself is free of objects creation code.
Line 848: However, it does not remove the real source of the problem: instead it moves it from the area of
Line 849: test code to that of utility classes. Compared to the first approach, this one requires only a minimal
Line 850: additional amount of coding.
Line 851: The last approach we adopted was that of using Test Data Builders. This gave us a lot of flexibility
Line 852: in creating objects, but at the price of maintaining some additional code (much larger than in the case
Line 853: of Object Mother). I would recommend this approach for complex domain objects.
Line 854: When creating domain objects for your tests starts to get painful, it might mean that they
Line 855: are too complicated.
Line 856: 10.7. Conclusions
Line 857: In this chapter you will have learned some things about the organization of tests. We started with basic
Line 858: matters. First, we compared two options for using packages for test classes. After discussing a naming
Line 859: schema for test classes (ClassNameTest) and test methods (should…()), we also tackled the topic of
Line 860: comments within test code.
Line 861: Things got harder, then. We discussed a slightly different approach to writing tests, called BDD. In
Line 862: fact, BDD is much more than this - it is a different mindset, which pays a great deal of attention to
Line 863: fulfilling customers’ requirements. This topic is huge, but here we have concentrated exclusively on
Line 864: its influence on how unit tests should be written.
Line 865: After this we went on to discuss ways of removing some redundant code from Mockito-powered tests,
Line 866: and took a look at the creation of objects - both of them capable of saving us from writing some lines
Line 867: of code, and of making our tests easier to maintain.
Line 868: These last few points are already steering us in the direction of the maintainability and quality of tests,
Line 869: which is very good, because this is exactly what we will be discussing in the next part of the book.
Line 870: But first let us practise a little!
Line 871: 203
Line 872: 
Line 873: --- 페이지 219 ---
Line 874: Chapter 10. Organization Of Tests
Line 875: 10.8. Exercises
Line 876: In addition to the exercises presented below, do not forget to read some more about Behaviour Driven
Line 877: Development! Many tools and ideas, especially for integration and end-to-end tests, are based on the
Line 878: BDD approach.
Line 879: 10.8.1. Test Fixture Setting
Line 880: Enhance the test from Listing 10.15, so some actions are executed:
Line 881: • before the tests of this class are executed,
Line 882: • after the tests of this class have been executed,
Line 883: • before each test method is executed,
Line 884: • after each test method has been executed.
Line 885: Add some System.out.println() statements (or a logger, if you consider System.out.println()
Line 886: to be lame) to the created method. Execute the test, and observe whether the order of execution is as
Line 887: expected.
Line 888: Listing 10.15. Test fixture setting
Line 889: public class TestFixtureTest {
Line 890:     @Test
Line 891:     void testMethodA() {
Line 892:         System.out.println("method A");
Line 893:     }
Line 894:     @Test
Line 895:     void testMethodB() {
Line 896:         System.out.println("method B");
Line 897:     }
Line 898: }
Line 899: 10.8.2. Test Data Builder
Line 900: The listing below shows the Transaction class. It is a simple POJO with no logic but only getters
Line 901: and setters methods (which have been omitted in the listing to make it shorter).
Line 902: Listing 10.16. Transaction class
Line 903: public class Transaction {
Line 904:     private long id;
Line 905:     private State state; 
Line 906:     private boolean retryAllowed;
Line 907: 204
Line 908: 
Line 909: --- 페이지 220 ---
Line 910: Chapter 10. Organization Of Tests
Line 911:     private String message;
Line 912:     private String billingId;
Line 913:     // getters and setters omitted
Line 914:     ...
Line 915: }
Line 916: There are four possible values of the state field - PROCESSING, OK, CANCELLED, ERROR.
Line 917: Write a test which creates a number of objects of the Transaction class using the Test Data Builder
Line 918: pattern. Compare the result with the "normal" approach of creating objects directly within your test
Line 919: code (using their constructor and setters).
Line 920: 205