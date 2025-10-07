Line 1: 
Line 2: --- 페이지 152 ---
Line 3: Chapter 8. Points of Controversy
Line 4: Discussion is an exchange of knowledge; an argument an exchange of ignorance.
Line 5: — Robert Quillen
Line 6: There are many topics related to writing tests that are still up for debate within the developer
Line 7: community. In this section we will discuss some of these. Sometimes a definite answer will be given,
Line 8: sometimes a variety of options will be presented – for you, dear reader, to decide about.
Line 9: 8.1. Access Modifiers
Line 10: In the code shown throughout the book, I follow unwritten standards of the Java world relating to the
Line 11: use of access modifiers. In particular, I used the private keyword for almost every instance variable.
Line 12: There is nothing wrong with this approach; however, some people may find it unnecessary.
Line 13: The point here is that while with production code we tend to be obsessed with encapsulation and
Line 14: information hiding, this is not the case with test classes. They are almost never used by other classes
Line 15: 1, which means that the fact that some field or method is marked with private does not really make
Line 16: code any better. Hence, if you are in the habit of marking everything with the private keyword, then
Line 17: by all means go ahead and adopt this approach with test code as well. On the other hand, if you think
Line 18: that by omitting private you are going to gain some readability in respect of your test code, then do
Line 19: get rid of it. (And don’t let any zealots intimidate you into doing otherwise!)
Line 20: 8.2. Random Values in Tests
Line 21: Up till now we created all the values used in our tests by hand. But this isn’t the only option: we can
Line 22: ask the computer to (randomly) generate them for us. There are a few aspects of using such random
Line 23: values in tests, so let us have a closer look at this topic.
Line 24: Before we start discussing code, however, let me just say that there are many ways to generate random
Line 25: values, including:
Line 26: • custom "utility methods",
Line 27: • using specialized libraries like Java Faker [https://github.com/DiUS/java-faker] or libraries of
Line 28: general use like Apache Commons Lang library2 (which provides a RandomStringUtils utility
Line 29: class),
Line 30: • using frameworks for property-based testing like jqwik [https://jqwik.net/specialized] or junit-
Line 31: quickcheck [https://github.com/pholser/junit-quickcheck].
Line 32: 8.2.1. Random Object Properties
Line 33: Let us assume that an SUT (of the UserToPersonConverter class) can translate an object of the
Line 34: User class into objects of the Person class by turning the user’s name and surname into a person’s
Line 35: nickname. The implementation of the SUT is shown below:
Line 36: 1This is not 100% true, as sometimes we use inheritance, so some test classes inherit the fields and methods of a base class.
Line 37: 2http://commons.apache.org/lang/
Line 38: 137
Line 39: 
Line 40: --- 페이지 153 ---
Line 41: Chapter 8. Points of Controversy
Line 42: Listing 8.1. The UserToPersonConverter class
Line 43: public class UserToPersonConverter {
Line 44:     public static Person convert(User user) {
Line 45:         return new Person(user.getName() + " " + user.getSurname());
Line 46:     }
Line 47: }
Line 48: A test of this class can take advantage of random values. Such an attempt is shown in Listing 8.2.
Line 49: Listing 8.2. Test of the UserToPersonConverter class
Line 50: public class UserToPersonConverterTest {
Line 51:     @Test
Line 52:     void shouldConvertUserNamesIntoPersonNick() {
Line 53:         String name = RandomStringUtils.randomAlphabetic(8);
Line 54:         String surname = RandomStringUtils.randomAlphabetic(12);
Line 55:         User user = new User(name, surname);
Line 56:         Person person = UserToPersonConverter.convert(user);
Line 57:         assertThat(person.getNick())
Line 58:             .isEqualTo(name + " " + surname);
Line 59:     }
Line 60: }
Line 61: As far as I understand the idea behind the implementation shown in Listing 8.2, random values are to
Line 62: be used because they (supposedly) highlight the robustness of a given test. It is as if the test were to
Line 63: shout "Hey look, every time I execute the test it uses a different user’s name and still passes! Amazing,
Line 64: isn’t it?".
Line 65: But obviously, why stop at one random value, when we can easily have thousands of them? It seems
Line 66: natural to move forward, combining randomly generated values with parameterized tests.
Line 67: Listing 8.3. Creation of multiple random test cases
Line 68: import com.github.javafaker.Faker;
Line 69: import org.junit.jupiter.params.ParameterizedTest;
Line 70: import org.junit.jupiter.params.provider.Arguments;
Line 71: import org.junit.jupiter.params.provider.MethodSource;
Line 72: import java.util.stream.Stream;
Line 73: public class UserToPersonConverterDataProvidersTest {
Line 74:     private static Stream<Arguments> getRandomNames() {
Line 75:         return Stream.generate(() -> {
Line 76:             return Arguments.of(
Line 77:                     faker.name().firstName(), 
Line 78:                     faker.name().lastName()
Line 79:             );
Line 80:         }).limit(100); 
Line 81:     }
Line 82: 138
Line 83: 
Line 84: --- 페이지 154 ---
Line 85: Chapter 8. Points of Controversy
Line 86:     @ParameterizedTest
Line 87:     @MethodSource(value = "getRandomNames")
Line 88:     void shouldConvertUserNamesIntoPersonNick(
Line 89:         String name, String surname) {
Line 90:         User user = new User(name, surname);
Line 91:         Person person = UserToPersonConverter.convert(user);
Line 92:         assertThat(person.getNick())
Line 93:             .isEqualTo(name + " " + surname);
Line 94:     }
Line 95: }
Line 96: This time we use Java Faker library to generate values.
Line 97: The test method will be executed 100 times with different values.
Line 98: Even if the test in Listing 8.3 looks much more serious than the previous one, it is not really much
Line 99: stronger. It only tricks us into thinking that UserToPersonConverter has now been thoroughly tested.
Line 100: Unfortunately it hasn’t been.
Line 101: Let us take another look at the implementation of the UserToPersonConverter class (shown in
Line 102: Listing 8.1). Has it been tested more effectively, just because we have passed 100 various names? I do
Line 103: not think so. The probability that tests 2 to 100 will reveal some bugs not discovered by the first test
Line 104: is minimal. The diversity of test parameters is very limited, and so is the value added by each of the
Line 105: tests. It would not increase, even if we were to up the number of randomly generated values from 100
Line 106: to 1000.
Line 107: When it comes to testing, I would rather prioritize the quality of test cases over the quantity. A good
Line 108: quality test case can expose some holes within the production code. I suggest thinking carefully about
Line 109: the possible scenarios (as discussed in Section 7.1) and then making a deliberate choice of some
Line 110: values. My test of the UserToPersonConverter class would definitely contain cases of names and
Line 111: surnames of varied length (including empty strings), with varied capitalization. I might even use some
Line 112: randomness to avoid putting so many names directly in the test code; however, I would make sure
Line 113: that some borderline cases (e.g. empty or extremely long strings) are verified. The variety of my test
Line 114: parameters would definitely be far greater than that generated by the data provider in Listing 8.3.
Line 115: 139
Line 116: 
Line 117: --- 페이지 155 ---
Line 118: Chapter 8. Points of Controversy
Line 119: Property-based testing
Line 120: So far, I haven’t been enthusiastic about the introduction of random values into tests. Still,
Line 121: they are valuable - or even indispensable - in some kind of tests. By way of example, let me
Line 122: mention that the test suites of Apache Lucene3 contain a lot of randomly generated test cases,
Line 123: which allowed them to report an important Java 7 bug4.
Line 124: Property-based tests capture characteristics, or "properties", of the output of
Line 125: code that should be true given arbitrary inputs that meet certain criteria.
Line 126: — junit-quickcheck documentation
Line 127: The idea of property-based testing is to generate a vast number of random input values and
Line 128: verify whether expected properties hold for these generated use cases. This makes perfect
Line 129: sense for algorithm verification, when you know exactly what constraints you expect your
Line 130: results to be subject to. As I don’t find much need to use tests of this kind in my programming
Line 131: tasks, I would suggest that you scan the documentation of junit-quickech [https://github.com/
Line 132: pholser/junit-quickcheck] and jqwik [http://jqwik.net] projects to see what the valid use cases
Line 133: for such an approach are.
Line 134: 8.2.2. The Gotchas
Line 135: As you will have observed for yourself, generating multiple tests with random values does not
Line 136: automatically make the test suite stronger. Instead, it can complicate your tests and give rise to a
Line 137: number of issues. However, if randomness is really appropriate within the context of your testing
Line 138: domain, then at least try to do it right.
Line 139: Let us discuss now issues relating to the use of random values in your tests.
Line 140: The aformentioned libraries - e.g. jqwik and junit-quickcheck - provide solutions for some
Line 141: of the issues described below. 
Line 142: Table 8.1. Issues with the random values of parameters
Line 143: (possible) issue
Line 144: comment
Line 145: Why should I test with
Line 146: nonsensical values (e.g.
Line 147: "(*&KLNHF_98234" passed as
Line 148: String name parameter)?
Line 149: You should not. "Random" does not have to mean "any". Take
Line 150: control over how parameters values are generated, e.g. use
Line 151: RandomStringUtils.randomAlphabetic() method from the
Line 152: Apache Commons Lang library or name().firstName() from
Line 153: Java Faker in cases of the name parameter.
Line 154: I do not have control over random
Line 155: values, so how can I guarantee
Line 156: that some values (e.g. boundary
Line 157: values) will always be checked?
Line 158: Do not rely solely on random values! Apart from random
Line 159: values, you also have to make sure boundary values (and any
Line 160: other values which are important to your code) are being used.
Line 161: Probably you need two sources of parameters - one controlled by
Line 162: you, and one random.
Line 163: 3http://lucene.apache.org
Line 164: 4See http://blog.thetaphi.de/2011/07/real-story-behind-java-7-ga-bugs.html
Line 165: 140
Line 166: 
Line 167: --- 페이지 156 ---
Line 168: Chapter 8. Points of Controversy
Line 169: (possible) issue
Line 170: comment
Line 171: Hard to repeat. How can I repeat
Line 172: something which is random?
Line 173: Repeatability is an important thing. If you do not have it, then
Line 174: you might know there is a bug in your code, but you will not be
Line 175: able to nail it down - which will surely cost you a few gray hairs.
Line 176: However, it is possible to repeat your tests, even when random
Line 177: values are being used.
Line 178: First of all, XML files created by JUnit during the execution of
Line 179: tests contain comprehensive information on parameters passed to
Line 180: test methods, so you can see what values were used there. You
Line 181: can also control the way the random values are generated by
Line 182: choosing the seed, remembering it (e.g. by writing to some test
Line 183: report), and using it later to repeat the testsa.
Line 184: "Flickering tests" - every
Line 185: execution of the test suite could
Line 186: end with a different result.
Line 187: Every time the test fails, add the values which made it fail to
Line 188: your test. And of course, make it pass with these values.
Line 189: Weird error messages.
Line 190: Using random test values can result in obscure failure messages.
Line 191: For example, you can learn that the test failed because of some
Line 192: issue with user "IkldlDFg yw,cKxH.zDIF". This might be
Line 193: very confusing, especially if the test case has nothing to do
Line 194: with the user’s name. I would suggest using much simpler
Line 195: values, which reveal the intention much better - e.g. "ANY_NAME
Line 196: ANY_SURNAME" would be much more clear.
Line 197: aIf you are interested in details, please refer to Jaroslav Tulach’s article at http://wiki.apidesign.org/wiki/RandomizedTest
Line 198: 8.3. Is Set-up the Right Thing for You?
Line 199: We already know now that it is essential to make sure that we test a "fresh" SUT and collaborators
Line 200: before putting them through their paces with our test methods. However, this raises the question how
Line 201: this has been achieved. And this is where some issues arise.
Line 202: As we already know, JUnit creates a new instance of a test class before each of its methods is
Line 203: executed. This allows us to create the SUT and collaborators in different places. Firstly, we could
Line 204: create the SUT and collaborators along with their declaration as instance members. Secondly, we
Line 205: could create objects within test methods. Thirdly, we could create objects within the specialized set-
Line 206: up methods. Last but not least, we could combine all of these options. Let us take a closer look at
Line 207: these alternatives.
Line 208: In some cases, it is possible to create the SUT and collaborators as instance fields.
Line 209: Listing 8.4. Creation along with declaration
Line 210: public class DeclarationTest {
Line 211:     Collaborator collaborator = mock(Collaborator.class);
Line 212:     OtherCollaborator otherCollaborator = mock(OtherCollaborator.class);
Line 213:     SUT sut = new SUT(collaborator, otherCollaborator);
Line 214:     @Test
Line 215:     void testA() {
Line 216: 141
Line 217: 
Line 218: --- 페이지 157 ---
Line 219: Chapter 8. Points of Controversy
Line 220:         // ...
Line 221:     }
Line 222:     @Test
Line 223:     void testB() {
Line 224:         // ...
Line 225:     }
Line 226: }
Line 227: This works fine for "smaller" tests, in which there are not many collaborators and the test fixture is
Line 228: relatively simple. For the creation of more complex objects this technique is less feasible.
Line 229: Experience tells me that every time I start with instance members, I willneed to switch to the set-up
Line 230: method at some point. So I use the set-up method as my default approach knowing I will end up there
Line 231: anyway.
Line 232: In addition to that, it happens that the SUT and/or some of its collaborators need some additional care
Line 233: with regard to a specific test scenario. If so, this additional configuration happens in the test method.
Line 234: (This was the case of FootballTeam class we encountered in Section 4.3: for each test scenario we
Line 235: had to create the SUT with different properties, so the only logical solution was to move this creation
Line 236: phase into the test methods.)
Line 237: To sum it all up, my test classes often adopt this structure:
Line 238: Listing 8.5. SetUp method & additional configuration within test method
Line 239: public class SetUpTest {
Line 240:     private Collaborator collaborator;
Line 241:     private OtherCollaborator otherCollaborator;
Line 242:     private SUT sut;
Line 243:     @BeforeEach
Line 244:     void setUp() { 
Line 245:         collaborator = mock(Collaborator.class);
Line 246:         otherCollaborator = mock(OtherCollaborator.class);
Line 247:         sut = new SUT(collaborator, otherCollaborator);
Line 248:         // more configuration of SUT and collaborators here
Line 249:     }
Line 250:     @Test
Line 251:     void testA() {
Line 252:         // assertions
Line 253:     }
Line 254:     @Test
Line 255:     void testB() {
Line 256:         sut.someConfigurationMethod(); 
Line 257:         // assertions
Line 258:     }
Line 259: }
Line 260: This is where creation of the SUT and collaborators happens…
Line 261: 142
Line 262: 
Line 263: --- 페이지 158 ---
Line 264: Chapter 8. Points of Controversy
Line 265: …well, not entirely, as some objects need to be configured in a specific way for some test cases.
Line 266:  As usual, there is a trade-off we have to take when deciding where to put our test-fixture code. An
Line 267: obvious disadvantage of this approach is that test fixture creation happens now in two places, so to
Line 268: understand the exact scenarios one needs to look into the test method and the set-up method.
Line 269: I would say there are a few factors in play here:
Line 270: The DRY principle. 
Line 271: If the DRY principle is very dear to you, you will probably use the set-up
Line 272: methods approach. After you have got used to the fact that some of the test logic is also included
Line 273: within set-up methods, you will have no problems reading your tests.
Line 274: The readability of tests. 
Line 275: On the other hand, if you are into BDD then you will, instead, appreciate
Line 276: your tests being self-contained (and you will put most of the test fixture code directly into test
Line 277: methods).
Line 278: Consistency. 
Line 279: If you like your codebase to be written in the same way throughout, you will probably
Line 280: want to follow one approach in all your tests. If this is not the most important factor, then you will
Line 281: probably do what I did when writing tests for this book: use the set-up approach for test classes with
Line 282: multiple test methods (and multiple collaborators), but put the test-fixture creation within test methods
Line 283: in cases of shorter tests.
Line 284: Complexity. 
Line 285: Sometimes the complexity of the test case will make the decision for you. For more
Line 286: complex tests you will end up with a mixture of the above techniques, so be prepared for that!
Line 287: 8.4. How Many Assertions per Test
Line 288: Method?
Line 289: Chuck Norris can unit test an entire application with a single assert.
Line 290: — Wisdom of the Internet ;)
Line 291: The idea of having only One Assertion Per Test Method (I will use the acronym OAPTM for this
Line 292: from here on) is quite popular among developers. Some of its popularity may be attributed to the
Line 293: misuse of multi-assertion test methods, which tend to grow into many lines of code (in the hands of
Line 294: inexperienced or incompetent developers). It has also been discussed on popular forums and promoted
Line 295: by a number of prominent TDD and testing proponents, including Dave Astel and Roy Osherove.
Line 296: All of the code examples presented so far in this book make it quite obvious that I myself do not
Line 297: subscribe to this idea and do not follow it. And even though I understand and share some of the
Line 298: motivations behind it, I will try to persuade you not to subscribe to it either – at least, not in its
Line 299: dogmatic version.
Line 300: 8.4.1. Code Example
Line 301: Let us take a look at an example, to make sure we understand the problem in hand. I will use an
Line 302: example taken from the "One Assertion per Test" post by Dave Astels5. It relates to the problem of
Line 303: 5See http://www.artima.com/weblogs/viewpost.jsp?thread=35578
Line 304: 143
Line 305: 
Line 306: --- 페이지 159 ---
Line 307: Chapter 8. Points of Controversy
Line 308: parsing some information passed as a String argument and creating a reasonable domain class out of
Line 309: it. In Listing 8.6 I use original test method names.
Line 310: Since the original test uses the assertEquals() assertion of JUnit I have decided to also
Line 311: use it in my code.
Line 312: Listing 8.6. Address parsing – one assert per test method
Line 313: public class AddressParsingOneAssertTest {
Line 314:     private Address anAddress
Line 315:         = new Address("ADDR1$CITY IL 60563$COUNTRY"); 
Line 316:     @Test
Line 317:     void testAddr1() { 
Line 318:         assertEquals("ADDR1",  anAddress.getAddr1());
Line 319:     }
Line 320:     @Test
Line 321:     void testCsp() { 
Line 322:         assertEquals("CITY IL 60563",  anAddress.getCsp());
Line 323:     }
Line 324:     @Test
Line 325:     void testCountry() { 
Line 326:         assertEquals("COUNTRY",  anAddress.getCountry());
Line 327:     }
Line 328: }
Line 329: setting the test fixture for every test method,
Line 330: each test method contains only one assert.
Line 331: As you can see, OAPTM makes us use many very focused, tiny, often just one-line test methods. To
Line 332: get a broader understanding of "what address parsing looks like", you need to scan at least a few of
Line 333: them. What you get in return is that if a constructor of the Address class does not work properly, you
Line 334: will know all about it - i.e. the failing test cases will tell you exactly what works and what doesn’t.
Line 335: A counterpart test – i.e. a test which uses several assertions per test method – is shown in Listing 8.7.
Line 336: Listing 8.7. Address parsing – several assertions per test method
Line 337: public class AddressParsingManyAsserts {
Line 338:     @Test
Line 339:     void testAddressParsing() { 
Line 340:         Address anAddress = new Address("ADDR1$CITY IL 60563$COUNTRY");
Line 341:         assertEquals("ADDR1",  anAddress.getAddr1()); 
Line 342:         assertEquals("CITY IL 60563",  anAddress.getCsp());
Line 343:         assertEquals("COUNTRY",  anAddress.getCountry());
Line 344:     }
Line 345: }
Line 346: Only one test method - with three assertions.
Line 347: 144
Line 348: 
Line 349: --- 페이지 160 ---
Line 350: Chapter 8. Points of Controversy
Line 351: All three assertions gathered in one place.
Line 352: This time the number of test methods is significantly smaller, but they themselves are slightly larger
Line 353: (though still reasonably short). It is very easy to understand what "address parsing" means, since
Line 354: all parsing assertions are grouped together. On the downside, though, it might happen that any bugs
Line 355: introduced into the Address class constructor only reveal themselves gradually – one by one, in
Line 356: consecutive runs of the AddressParsingManyAssertsTest test class.
Line 357: One important thing to notice is that even though in the second version of the test there is more
Line 358: than one assert per test method, each test method tests only one thing - the ability of the Address
Line 359: constructor to parse addresses properly.
Line 360: Custom Matcher
Line 361:  And BTW. A custom matcher-based solution would be even better. For example:
Line 362: assertThat(anAddress)
Line 363:         .hasCountry("COUNTRY")
Line 364:         .hasCsp("CITY IL 60563")
Line 365:         .hasAddr1("ADDR1")
Line 366: 8.4.2. Pros and Cons
Line 367: Allow me now to take up the commonly cited reasons for following the OAPTM rule (as put forward
Line 368: by its proponents) and comment on them as they relate to the code present in the Listing 8.6 and
Line 369: Listing 8.7.
Line 370: Table 8.2. Arguments for using only one assert per test
Line 371: argument
Line 372: comment
Line 373: Using more than one assertion per test
Line 374: method leads to testing more than one
Line 375: thing - which violates the SRP.
Line 376: Use of many assertions per test method may potentially
Line 377: lead to testing too much, this is true. However, it does not
Line 378: have to be so. The question is, what granularity of this 'one
Line 379: thing' you are testing makes you feel comfortable. For me,
Line 380: testing the ability of Address class constructor to parse
Line 381: address passed as a String, is just the right size of a thing
Line 382: (of a functionality) to be tested in single test method.
Line 383: Tests written this way are easier to
Line 384: maintain (thanks to smaller, focused
Line 385: methods).
Line 386: This is a very subjective statement. The number of test
Line 387: methods created with OAPTM rule can be really high.
Line 388: Maintaining them might be a nightmare, especially that you
Line 389: need to browse through many of them to get a clear picture
Line 390: of tested functionality.
Line 391: When a test fails it is dead simply to
Line 392: deduce what went wrong.
Line 393: If you write good test with many asserts you can achieve the
Line 394: same effect. Current IDEs are capable of telling you exactly
Line 395: which assertion failed, so I do not see any gain from using
Line 396: OAPTM in this aspect.
Line 397: If more than one asserts are about to
Line 398: fail, they will - in case of multiple
Line 399: This is true, but I believe this threat to be of more
Line 400: theoretical rather than practical significance. From my
Line 401: 145
Line 402: 
Line 403: --- 페이지 161 ---
Line 404: Chapter 8. Points of Controversy
Line 405: argument
Line 406: comment
Line 407: asserts per test, only the first one will
Line 408: fail, so you need to rerun your tests to
Line 409: see the next one failing.
Line 410: experience, the situations where one assertion failure
Line 411: "hides" other failures, are more than rare - in fact I cannot
Line 412: recall it ever happening to me. I shield myself from such an
Line 413: effect writing assertions one by one and following the TDD
Line 414: rhythm.
Line 415: It is easier to create intention-revealing
Line 416: method names for one-assertion tests.
Line 417: Maybe so, but as proved by original code on Listing
Line 418: 8.6, it is still pretty easy to come with lousy names (e.g.
Line 419: testCsp()) even if using one assert per test! I am confident
Line 420: that finding good intention-revealing names for many-
Line 421: assertions is possible, and that OATPM does not have any
Line 422: advantages here.
Line 423: 8.4.3. Conclusions
Line 424: Even as a firm believer in small, focused, easy-to-understand methods, I think that OAPTM goes too
Line 425: far, and does more harm than good. It results in too many lines of code being scattered amongst a
Line 426: multitude of tiny methods – something which is much harder to understand and maintain. It saves me
Line 427: from one problem (having too many assertions per test method), only to inflict on me another (having
Line 428: too many test methods).
Line 429: No. Sorry, OAPTM! I can judge on my own when a test method is getting too large, without needing
Line 430: to follow such dogmatic rules. And as long as I stick to the TDD approach, I will rarely, if ever, be
Line 431: stricken by the downside of the multiple asserts approach. My test methods are very concise and
Line 432: readable, and I can easily find intention-revealing names for them. My IDE will guide me straight to
Line 433: the fallen assertion every time a test fails.
Line 434: My advice would be not to take the "one assert per test" recommendation too literally. Get clear about
Line 435: the reasons behind it, but follow another, similar rule, which says that each test method should
Line 436: concentrate on a single feature of the SUT. Sometimes numerous assertions will be required to
Line 437: test a certain feature, sometimes one will suffice. But in my opinion, the number of assertions should
Line 438: not be your main concern. What really matters is the scope of the SUT features covered by each test
Line 439: method.
Line 440: The only thing that would get me writing so many tiny test methods would be if I was
Line 441: being paid by LOCs. :)
Line 442: 146
Line 443: 
Line 444: --- 페이지 162 ---
Line 445: Chapter 8. Points of Controversy
Line 446: Soft Assertions
Line 447: Continuing the discussion from the previous sections, let us learn now about soft assertions.
Line 448: The idea behind them is the following: Let us not stop the execution of test after the first failed
Line 449: assertion. We should better execute them all and report all failures together. Both AssertJ and
Line 450: JUnit provide methods that are quite easy to use, and the IDEs print reasonable output giving
Line 451: you a good understanding of which asserts have failed and for what reasons.
Line 452: And since you are probably curious what these soft assertions look like, let us see one possible
Line 453: example with AssertJ SoftAssertions class:
Line 454: Listing 8.8. Soft Assertions - pseudocode example
Line 455: // this is a pseudocode for illustration purposes only
Line 456: // refer to AssertJ documentation for details
Line 457: import org.assertj.core.api.SoftAssertions;
Line 458: SoftAssertions.assertSoftly(softly -> { 
Line 459:          softly.assertThat(something).someAssertHere();
Line 460:          softly.assertThat(something).anotherAssert();
Line 461:          softly.assertThat(something).yetAnotherAssert();
Line 462: });
Line 463: each of the assertions within the code block will be executed no matter the failures of
Line 464: previously executed ones
Line 465: Hmm… I can clearly see the value of such approach for long-running integration or end-
Line 466: to-end tests when the execution of the test is so costly (in terms of time) that you really,
Line 467: really want to learn as much about the tested scenario as possible. So, in the case of a long
Line 468: (Webdriver) test, which ends with bunch of asserts, I think it might make sense to write them
Line 469: using soft assertions.
Line 470: But for unit tests? Oh no, I don’t see a need for them. Are you waiting long for execution and
Line 471: would like to learn about all failures at once? Not very likely. And since each of your test
Line 472: methods focuses on a "single feature of the SUT", there is no broader spectrum of failures you
Line 473: would also like to learn about in one test.
Line 474: And I also see a potential downside. I think that using soft assertions might lead you in the
Line 475: wrong direction: it might encourage you to verify much more then required, or to verify
Line 476: different things "because you can".
Line 477: Have soft assertions in your toolbox then (they will come in handy one day!), but don’t put
Line 478: them in your unit tests.
Line 479: 8.5. Private Methods Testing
Line 480: Everyone agrees that we should test publicly available methods. They provide the functionality used
Line 481: by clients, so it would be unreasonable to leave them untested. However, when it comes to testing
Line 482: private methods, two different voices can be heard. Let us hear them.
Line 483: 147
Line 484: 
Line 485: --- 페이지 163 ---
Line 486: Chapter 8. Points of Controversy
Line 487: 8.5.1. Verification vs. Design - Revisited
Line 488:  Some people say this is something you simply should not do. They point out that it is a bad idea
Line 489: to make assumptions about the internal implementation of an object: all we should care about is
Line 490: its public API. They will point to the weak design of a class as the culprit, and will tend to fix it in
Line 491: order to have a more testable solution. They perceive private methods, which cry out to be tested,
Line 492: as being indicative of hidden classes, which should be extracted and tested properly via their public
Line 493: API6. A practical argument against testing private methods is that they are prone to alteration during
Line 494: refactorings, so their tests are endangered.
Line 495:  Others will have no such objections. They say we should test everything that might possibly break
Line 496: (see Section 11.5), no matter if it be a publicly available part of a class or not. They want to have their
Line 497: code covered with tests, and do not feel inclined to perform complicated refactorings or redesigns of
Line 498: code that seems "good enough".
Line 499: If you are experiencing a sense of déjà vu right now, then rest assured - you are not in an
Line 500: altered matrix7. No - it is a perfectly reliable indicator of your brain’s working as it should!
Line 501: We were indeed discussing two similar points of view in Section 1.3.
Line 502: 8.5.2. Options We Have
Line 503: So, what to do, when faced with such a dilemma? Several things.
Line 504: The first thing you could, and probably should, do, is to avoid such a situation. How? By following
Line 505: the TDD approach. Think about how private methods come to life when you code test first. The
Line 506: answer is, that they are created during the refactoring phase, which means their content is fully
Line 507: covered by tests (assuming that you really follow the TDD rules, and write code only when there
Line 508: is a failing test). In such cases there is no problem of an "untested private method which should
Line 509: somehow be tested", because such methods simply do not exist.
Line 510: Alas, this is not the ultimate answer to our problem! It is the right answer when writing software from
Line 511: scratch, but will not help you when working with legacy code. What is more irritating is that when
Line 512: faced with legacy code, we often run up against the "chicken and egg" dilemma:
Line 513: • a class requires a refactoring, but you cannot perform this, because you lack the tests to tell you
Line 514: whether or not it will break things along the way,
Line 515: • tests should be written for the class, but this is not easily achieved without it having been refactored
Line 516: first.
Line 517: And so we have a closed circle. Definitely, then, we will have to explore further options to find a way
Line 518: out of this situation.
Line 519: Another approach you can take, even with the most vicious legacy code, is to refactor a little, test
Line 520: a little, and then refactor again, and test, and refactor, etc. moving in baby steps. You will probably
Line 521: need to start with integration tests (which are sometimes easier to write for legacy applications, which
Line 522: consists of many tightly coupled classes and external resources like databases) and then gradually
Line 523: 6As extreme programmers put it, "you should listen to your code" and follow its advices.
Line 524: 7http://en.wikipedia.org/wiki/Deja_vu
Line 525: 148
Line 526: 
Line 527: --- 페이지 164 ---
Line 528: Chapter 8. Points of Controversy
Line 529: make your tests more focused. Step by step… This is a tedious task, and by no means a short one.
Line 530: The benefit is that you end up with a loosely coupled, testable application. However, it is a potentially
Line 531: dangerous approach and, given the complexity of the code and its legacy nature, will not guarantee
Line 532: success.
Line 533: Because of the difficulties involved with this, some people opt to take the "easy" path. They use
Line 534: techniques (and/or tools) which will allow them to test private methods as they are, without any
Line 535: additional work on the code structure (or with only a minimal amount of this).
Line 536: To sum things up, let us make the following observations:
Line 537: • No one wants to promote private methods testing - but some of us believe that sometimes this is the
Line 538: only way.
Line 539: • Some developers demand that their code be tested and 100% object-oriented, while others believe
Line 540: that testing is enough and do not struggle to achieve clean design.
Line 541: • When writing new code, we are conveniently positioned to write it so that it is fully tested via its
Line 542: public API. TDD might help to achieve this.
Line 543: • When working with legacy code we compromise on private method testing. Since the code plays
Line 544: unfair, we also forget about fair-play.
Line 545: 8.5.3. Private Methods Testing - Techniques
Line 546: Keeping in mind all the arguments against private methods testing, we should at least be prepared
Line 547: to test them. Sometimes it might just save our lives! Now we shall discuss the two most popular
Line 548: techniques for testing private methods. We will use the following class to demonstrate them:
Line 549: Listing 8.9. Class with a private method
Line 550: public class SomeClass {
Line 551:     private boolean privateMethod(Long param) { 
Line 552:         return true;
Line 553:     }
Line 554: }
Line 555: This is the method we would like to test.
Line 556: Reflection
Line 557:   This technique uses a Method class from the java.lang.reflect package8, which allows one to
Line 558: gather information on methods, but also to tweak them – e.g. introducing changes to their access
Line 559: modifiers. An application of this class in test code is shown in Listing 8.10.
Line 560: Listing 8.10. Testing private methods using reflection
Line 561: import java.lang.reflect.InvocationTargetException;
Line 562: import java.lang.reflect.Method;
Line 563: 8See http://docs.oracle.com/javase/7/docs/api/java/lang/reflect/package-summary.html
Line 564: 149
Line 565: 
Line 566: --- 페이지 165 ---
Line 567: Chapter 8. Points of Controversy
Line 568: public class PrivateMethodReflectionTest {
Line 569:     @Test
Line 570:     void testingPrivateMethodWithReflection()
Line 571:             throws NoSuchMethodException, InvocationTargetException,
Line 572:             IllegalAccessException {
Line 573:         SomeClass sut = new SomeClass(); 
Line 574:         Class[] parameterTypes = new Class[1];
Line 575:         parameterTypes[0] = java.lang.Long.class;
Line 576:         Method m = sut.getClass()
Line 577:             .getDeclaredMethod("privateMethod", parameterTypes); 
Line 578:         m.setAccessible(true); 
Line 579:         Object[] parameters = new Object[1];
Line 580:         parameters[0] = 5569L;
Line 581:         Boolean result = (Boolean) m.invoke(sut, parameters); 
Line 582:         assertThat(result).isTrue(); 
Line 583:     }
Line 584: }
Line 585: The SUT only contains a single private method, which is to be tested.
Line 586: Reflection is employed to set privateMethod() as accessible.
Line 587: invoke() returns Object, so we need to cast it to the expected type.
Line 588: Asserting that privateMethod() works as expected.
Line 589:   Obviously, this is not the sort of code we should be writing everyday! It is ugly, it uses magic
Line 590: (disguised as reflection), and it will break if you refactor privateMethod() to anything else. We
Line 591: could dispose of some of its weaknesses using a tool that will hide all this nasty code behind some
Line 592: nice API. This can be done, for example, using ReflectionUtils class of JUnit5.
Line 593: Listing 8.11. Testing private methods using ReflectionUtils class
Line 594: import org.junit.platform.commons.util.ReflectionUtils;
Line 595: import java.lang.reflect.Method;
Line 596: public class PrivateMethodReflectionUtilsTest {
Line 597:     @Test
Line 598:     void testingPrivateMethodWithReflection()
Line 599:             throws Exception {
Line 600:         SomeClass sut = new SomeClass();
Line 601:         Method privateMethod = sut.getClass()
Line 602:                 .getDeclaredMethod("privateMethod", Long.class);
Line 603:         ReflectionUtils.makeAccessible(privateMethod);
Line 604:         assertThat((boolean) privateMethod.invoke(sut, 2348973L)) 
Line 605:                 .isTrue();
Line 606:     }
Line 607: }
Line 608: As before invoke() returns Object, so we need to cast it to the expected type.
Line 609: 150
Line 610: 
Line 611: --- 페이지 166 ---
Line 612: Chapter 8. Points of Controversy
Line 613: Even though this code looks much nicer than that of the previous attempt, it still cannot be refactored
Line 614: safely. Calling methods using their name (String) as the parameter is not a healthy approach.
Line 615: One more thing to note is that neither the approach involving direct use of reflection, nor that which
Line 616: makes use of ReflectionUtils class, require us to modify the production code. This is a good thing.
Line 617: Access Modifiers
Line 618: Another option we have is to weaken the access modifier of a private method – something which
Line 619: will make it more easily accessible by test code. However, we do not usually want to make such a
Line 620: method public. Adding new methods to the API of a class, just because we want to test it, would be
Line 621: too much. Fortunately, we can achieve our goal by relaxing the access modifier just a little. This is
Line 622: shown in Listing 8.12.
Line 623: Listing 8.12. Testing private methods by relaxing access modifiers
Line 624: public class SomeClass {
Line 625:     boolean privateMethod(Long param) { 
Line 626:             return true;
Line 627:     }
Line 628: }
Line 629: public class PrivateMethodAccessModifierTest {
Line 630:     @Test
Line 631:     void testingPrivateMethodWithReflection() {
Line 632:         SomeClass sut = new SomeClass();
Line 633:         assertThat(sut.privateMethod(9238423L)).isTrue(); 
Line 634:     }
Line 635: }
Line 636: privateMethod() is no longer private - it has a "default" access modifier,
Line 637: which means it can be called directly from classes within the same package.
Line 638: This solution requires a serious change in the production code, which might not be possible. On the
Line 639: other hand, the test code is "normal" - that is, free from any unexpected constructs. It is also immune
Line 640: to name changes of tested methods, as refactoring tools will easily update the new method name
Line 641: within the test code.
Line 642: 8.5.4. Conclusions
Line 643: When writing the section on private methods testing, I must confess I was in two minds as to whether
Line 644: I should describe this at all. One part of me argued that it is evil and anti-OO, and that I should not
Line 645: include it in a book that sets out to promote good practice, and that puts a lot of pressure on one
Line 646: with respect to the quality of one’s code. The other part of me argued that I should have faith in my
Line 647: readers. My role will be to present and describe the different options so that you, dear reader, can
Line 648: decide by yourself which way to go. So it looks as though, in the end, this second part of me must
Line 649: have prevailed!
Line 650: I have tried very hard to discourage you from testing private methods. I still think that with good
Line 651: design, you will never need to test them directly. However, I do think that sometimes (very rarely, but
Line 652: 151
Line 653: 
Line 654: --- 페이지 167 ---
Line 655: Chapter 8. Points of Controversy
Line 656: still…) you might need to use the techniques described in this section. This is why I have decided to
Line 657: include them in the book.
Line 658: 8.6. Lambdas
Line 659: Java 8 brought us a powerful gift in the form of lambda expressions and streams. And, as it usually
Line 660: happens with new powers, learning how to wield them so we don’t shoot ourselves in the foot requires
Line 661: some time. And I could bet that every developer who started using lambdas abused the concept by
Line 662: putting too much complex functionality into them "just because we can" (well, it certainly happened
Line 663: to me!).
Line 664: This foreword to the section devoted to the testing of lambdas is justified, as most problems with
Line 665: writing tests for code which uses lambdas stem from the fact that sometimes the lambda expressions
Line 666: are too complex. If you think about it, you will discover that when it comes to testing, at the
Line 667: conceptual level lambdas do not differ much from private methods. If they are simple enough and
Line 668: contain only a limited amount of logic, you shouldn’t waste your time testing them directly. All you
Line 669: have to do is to test the outcomes of public methods that use the lambda expressions.
Line 670: This approach would work nicely for simple methods such as this one:
Line 671: public static List<String> someMethod(List<String> input) {
Line 672:   return input.stream()
Line 673:     .map(s -> someSimpleOperationHere(s))
Line 674:     .collect(Collectors.toList());
Line 675: }
Line 676: All we have to do in such a simple case is to prepare the input and expected output data (both
Line 677: collections of strings) and verify that once we call someMethod() with the given input we get the
Line 678: expected output.
Line 679: If the lambda expression is more complex, this technique might be insufficient. What we can do is
Line 680: extract the lambda and use method reference instead. The testing of this method should be a simpler
Line 681: task then, because we don’t need to deal with stream pipelines.
Line 682: This basically means we should refactor this method:
Line 683: public static List<String> someMethod(List<String> input) {
Line 684:   return input.stream()
Line 685:     .map(() -> complexOperationsHere())
Line 686:     .collect(Collectors.toList());
Line 687: }
Line 688: into this:
Line 689: public static List<String> someMethod(List<String> input) {
Line 690:   return input.stream()
Line 691:     .map(MyClass::complexLambda)
Line 692:     .collect(Collectors.toList());
Line 693: }
Line 694: static String complexLambda(String s) {
Line 695:     ....
Line 696: }
Line 697: 152
Line 698: 
Line 699: --- 페이지 168 ---
Line 700: Chapter 8. Points of Controversy
Line 701: Then, we can test the complexLambda() method, which is usually much simpler as we do not have to
Line 702: worry about stream pipelines (often much more complicated than in the example presented).
Line 703: The two techniques presented in this section should be sufficient for the vast majority of lambda-
Line 704: powered methods. If you still struggle with testing of any such method, then it might be the case there
Line 705: is too much complex logic involved.
Line 706: Methods which use lambda expression often take various collections as input arguments
Line 707: and often return collections. But since you already know how to test collections (see
Line 708: Section 7.10), this shouldn’t be a problem.
Line 709: 8.7. New Operator
Line 710: A seam is a place where you can alter behavior in your program without editing in that
Line 711: place.
Line 712: — Michael Feathers Working Effectively With Legacy Code (2004)
Line 713: When introducing test doubles (in Chapter 5, Mocks, Stubs, and Dummies), we assumed that the
Line 714: collaborators of the SUT could be replaced easily. This is the case if they are "injected" into the SUT
Line 715: - as constructor parameters, method parameters or using setters. However, this is not always the case.
Line 716: This section explains what can be done if there is no straightforward way of replacing the SUT’s
Line 717: collaborators.
Line 718: Listing 8.13 presents some very simple code. The myMethod() method of the MySut class creates
Line 719: another object (of the MyCollaborator class) using the new operator. Then it uses this newly created
Line 720: object (calls its methods, uses values it returns, etc.).
Line 721: Listing 8.13. Typical use of the Java new operator within the method body
Line 722: public class MySut {
Line 723:     public void myMethod() {
Line 724:         MyCollaborator collaborator = new MyCollaborator();
Line 725:         // some behaviour worth testing here which uses collaborator 
Line 726:     }
Line 727: }
Line 728: We assume this code can not be tested using state testing (there are no returned values or state
Line 729: changes) and we need to use interaction testing.
Line 730: The code in Listing 8.13 is perfectly valid Java code and, frankly, not complicated either. However,
Line 731: testing interactions between the SUT and its collaborator requires some additional effort. A test
Line 732: skeleton for such a method would look as shown below:
Line 733: Listing 8.14. Testing new - a test skeleton
Line 734: public class MySutTest {
Line 735:     @Test
Line 736:     void testMyMethod() {
Line 737: 153
Line 738: 
Line 739: --- 페이지 169 ---
Line 740: Chapter 8. Points of Controversy
Line 741:         MySut sut = new MySut(); 
Line 742:         MyCollaborator collaborator = mock(MyCollaborator.class); 
Line 743:         // make sut use collaborator 
Line 744:         // set expectations regarding collaborator's behaviour
Line 745:         // execute sut's method(s)
Line 746:         // verify results and/or collaborator's behaviour
Line 747:     }
Line 748: }
Line 749: Creation of the SUT.
Line 750: Creation of a test double for the SUT’s collaborator.
Line 751: "Make sut use collaborator" - but how?!
Line 752: When writing a test for the MySut class, we very quickly encounter a problem. There is no direct
Line 753: way to force sut to use a test double of the MyCollaborator class. This means that we cannot easily
Line 754: control the SUT’s environment. One option we have is to forget about testing in isolation, and test
Line 755: both classes (MySut and MyCollaborator) together. While this might work out pretty well in the short
Line 756: run (see the discussion in Section 5.5), it makes it hard to test all of the scenarios we should test. We
Line 757: don’t need to relive the whole debate about this: isolation in tests is usually worth fighting for, so let
Line 758: us fight for it!
Line 759: Even though myMethod() uses the new operator to create its collaborator,
Line 760: the discussion in this section also covers other similar situations. In
Line 761: particular, if myMethod() had used a factory pattern (e.g. MyCollaborator
Line 762: collaborator = MyFactory.getCollaborator(…)), instead of the new
Line 763: operator, or had used a lookup service (e.g. MyCollaborator collaborator =
Line 764: LookupService.findCollaborator(…)), that would have caused exactly the same
Line 765: problem when testing. The solutions discussed in the following sections would also apply
Line 766: to these similar scenarios. 
Line 767: Now that we understand the problem, let us discuss possible solutions to it. Each of them has its own
Line 768: pros and cons, which will be discussed in the sections below. But before we take a closer look at them,
Line 769: let us get clear about exactly what kind of a dilemma we are faced with here.
Line 770:   As was stated in Section 1.3, tools for testing can be divided into two types. Some of them only deal
Line 771: with verification, while others are more concerned with design. Mockito belongs to the second group:
Line 772: it works perfectly with well-written, loosely coupled code, but refuses to test code that is tightly-
Line 773: coupled. The problem we are facing right now – the use of either the new operator or static methods -
Line 774: is precisely a representation of what happens when the code is not loosely coupled. The ties between
Line 775: objects (in this case between sut and collaborator) are so tight that it is hard to loosen them for
Line 776: testing purposes.
Line 777: Having read this, one might well expect the solutions called for to come from using both types of tool.
Line 778: And this is exactly the case. Either we can use a tool that allows us to test tightly coupled code, or we
Line 779: will find it necessary to introduce some changes to the original code (hopefully making it better), and
Line 780: then use a tool from the second group.
Line 781: 8.7.1. PowerMock to the Rescue
Line 782: I will start this section in an unusual way - with a disclaimer:
Line 783: 154
Line 784: 
Line 785: --- 페이지 170 ---
Line 786: Chapter 8. Points of Controversy
Line 787: As discussed previously, I’m not a big fun of such tools, so we won’t spend much time here.
Line 788: But I decided to at least mention this alternative, so that when cornered by legacy code you
Line 789: might look for PowerMock’s help!
Line 790: But you need to be aware of two things.
Line 791: First of all, the creators of PowerMock themselves understand that this tool gives developers
Line 792: an unhealthy power:
Line 793: PowerMock is mainly intended for people with expert knowledge in unit
Line 794: testing. Putting it in the hands of junior developers may cause more harm than
Line 795: good.
Line 796: — PowerMock documentation
Line 797: Second, at the time of writing PowerMock does not work with JUnit5! Please consult the
Line 798: project’s documentation [https://github.com/powermock/powermock/wiki] to learn about any
Line 799: changes in that matter.
Line 800: Now, let us continue as if nothing happened. :)
Line 801: PowerMock acts as a kind of wrapper around different mocking frameworks. It enhances their
Line 802: functionality with some new features. It can simply ignore the nuisance that the new operator is and
Line 803: create a test double as if it were no issue at all.
Line 804: Listing 8.15 presents a test class which uses PowerMock. It does not differ substantially from what we
Line 805: have encountered so far, but it does use some annotations and classes which we have not come across
Line 806: until now.
Line 807: This is a JUnit4 test!
Line 808: Listing 8.15. Using PowerMock to test the new operator
Line 809: import org.powermock.api.mockito.PowerMockito; 
Line 810: import org.powermock.core.classloader.annotations.PrepareForTest;
Line 811: import org.powermock.modules.junit4.PowerMockRunner;
Line 812: @PrepareForTest(MySut.class) 
Line 813: @RunWith(PowerMockRunner.class) 
Line 814: public class MySutTest {
Line 815:     @Test
Line 816:     void testMyMethod() throws Exception {
Line 817:         MySut sut = new MySut();
Line 818:         MyCollaborator collaborator = mock(MyCollaborator.class); 
Line 819:         PowerMockito.whenNew(MyCollaborator.class).
Line 820:             withNoArguments().thenReturn(collaborator); 
Line 821:         // normal test using Mockito's syntax
Line 822:         // e.g. Mockito.when(collaborator.someMethod()).thenReturn(...) 
Line 823:     }
Line 824: 155
Line 825: 
Line 826: --- 페이지 171 ---
Line 827: Chapter 8. Points of Controversy
Line 828: }
Line 829: Required imports.
Line 830: In this case, the @PrepareForTest annotation informs PowerMock that the MySut class will
Line 831: create a new instance of some other class. In general, this is how PowerMock learns, about
Line 832: which classes it should perform some bytecode manipulation on.
Line 833: A special runner is used so PowerMock can be used within JUnit4 tests.
Line 834: The test double is created as usual - with the static mock() method of Mockito.
Line 835: This is where the magic happens: whenever a new object of the MyCollaborator class gets
Line 836: created, our test double object (collaborator) will be used instead. Two of PowerMock’s
Line 837: methods - whenNew() and withNoArguments() - are used to control the execution of a no-
Line 838: arguments constructor of the MyCollaborator class.
Line 839: There is nothing special in the test method itself - we can use normal Mockito syntax to verify
Line 840: the behaviour, to stub or to spy.
Line 841: And that is it. Except for some annotations required in order to use PowerMock and JUnit4 together,
Line 842: there is not much new here: only that in some places the PowerMockito class is used instead of the
Line 843: Mockito class. Apart from this, the code looks very similar to what we have come across so far.
Line 844: Let us conclude by summing up what this example has showed us:
Line 845: • there are tools (i.e. PowerMock) capable of dealing with the new operator, static method calls, and
Line 846: other language constructs, which are commonly recognized as being "untestable",
Line 847: • it is possible to test classes like the MySut class without changing (refactoring or redesigning) them
Line 848: at all,
Line 849: • tests written with PowerMock do not differ much from what we have become used to.
Line 850: After seeing what PowerMock can do for us, we should answer one question, which is surely shouting
Line 851: in our heads: "Why bother with anything else if I can do it so easily using PowerMock?!"
Line 852: There is a serious reason for avoiding using such tools. It is all about the quality of your code - in
Line 853: particular, about its maintainability. By using PowerMock as shown in Listing 8.15, you reproduce
Line 854: in your test code the tight-coupling which exists in the production code. Now, every time you change
Line 855: your production code, your tests will fail. By including implementation details in your tests (as
Line 856: PowerMock requires you to do) you have created an additional force which will make it harder to
Line 857: introduce changes to your production code. This is not good.
Line 858: Additionally, PowerMock lets you get away with suboptimal design. For example, a class can have
Line 859: way too much responsibility and still be capable of being tested with PowerMock. Testing it with
Line 860: other tools would be very cumbersome, but with PowerMock you will not feel the pain. In short, using
Line 861: PowerMock deprives you of valuable feedback about the quality of your code, which other tools will
Line 862: give you.
Line 863: However, there are situations where having PowerMock in your toolbox is a real blessing.
Line 864: That is why I have decided to present this tool, even though I myself do not use it on a
Line 865: daily basis.
Line 866: 8.7.2. Redesign and Inject
Line 867: Now we will be going in a direction quite opposite to that which we went in with PowerMock:
Line 868: we shall be working on the production code, to make it more testable. After this goal has been
Line 869: 156
Line 870: 
Line 871: --- 페이지 172 ---
Line 872: Chapter 8. Points of Controversy
Line 873: accomplished, we will be able to use a common Mockito approach, without using any reflection or
Line 874: class loading tricks.
Line 875: Basically, there are two ways in which a collaborator object can be easily replaced with a test double.
Line 876: First, we need to create a new field in the MySut class of the MyCollaborator type, and then:
Line 877: • either pass an object of the MyCollaborator class as the constructor’s argument, or via a setter
Line 878: method,
Line 879: • or redesign myMethod() so it takes an object of the MyCollaborator class as one of it arguments.
Line 880: No matter which option we choose, writing test code will then be a piece of cake. Listing 8.16 shows a
Line 881: refactored MySut class (with a constructor-injected collaborator), and Listing 8.17 shows a test written
Line 882: for this class.
Line 883: Listing 8.16. MySut class with constructor-injected collaborator
Line 884: public class MySut {
Line 885:     private final MyCollaborator collab; 
Line 886:     public MySut(MyCollaborator collab) { 
Line 887:         this.collab = collab;
Line 888:     }
Line 889:     public void myMethod() {
Line 890:         // some behaviour worth testing here which uses collaborator 
Line 891:     }
Line 892: }
Line 893: An object of the MyCollaborator class is provided by MySut's clients when they create objects
Line 894: of the MySut class.
Line 895: No new operator is used within myMethod(). The collaborator object has been created outside
Line 896: of the MySut class and passed as a constructor parameter.
Line 897: The myMethod() method does not deal with the creation of collaborators anymore. It uses a +collab+
Line 898: object of the MyCollaborator class, which is already available when myMethod() is executed.
Line 899: Listing 8.17. Testing of the redesigned MySut class
Line 900: public class MySutTest {
Line 901:     @Test
Line 902:     void testMyMethod() {
Line 903:         MyCollaborator collaborator = mock(MyCollaborator.class);
Line 904:         MySut sut = new MySut(collaborator); 
Line 905:         // usual Mockito interactions testing with stubs & mocks
Line 906:     }
Line 907: }
Line 908: The updated constructor of the MySut class allows for straightforward injection of
Line 909: a +collaborator+ test double.
Line 910: The test in Listing 8.17 holds no surprises for us. Replacing the collaborator of sut is simply a matter
Line 911: of passing the appropriate test double to its constructor.
Line 912: 157
Line 913: 
Line 914: --- 페이지 173 ---
Line 915: Chapter 8. Points of Controversy
Line 916: As this example demonstrates, a complicated case can be turned into something far simpler (from a
Line 917: testing point of view) by the redesign of the SUT. If it is possible to replace the cumbersome creation
Line 918: of objects (involving either the new operator or static factory methods) with a dependency injection,
Line 919: then testing becomes a trivial task.
Line 920: Even so, there are some downsides – or, at least, some issues we should be aware of:
Line 921: • production code gets altered to meet the requirements of the tests themselves (isn’t this a case of the
Line 922: tail wagging the dog?),
Line 923: • such a redesign breaks existing clients (it truly is a redesign, not a refactoring),
Line 924: • you need to write some additional code.
Line 925: On the "plus" side, there are two important things:
Line 926: • the design of production code is improved (myMethod() can take care of its business task, and need
Line 927: not occupy itself with objects creation),
Line 928: • tests are very simple to write (which also means they are easy to understand and maintain).
Line 929: After we have discussed all of the possible options, some conclusions will be drawn, but even now, I
Line 930: would like to encourage you to use this technique, because it addresses the real cause of the pain, not
Line 931: merely its symptoms. By redesigning your production code you make it better, and you get testability
Line 932: as a side effect.
Line 933: 8.7.3. Refactor and Subclass
Line 934: In some cases the redesign discussed in the previous section is not feasible. For example, it might be
Line 935: the case that we cannot afford to break a client that uses the old API. In such a case, we need to find
Line 936: another way to make the class more testable. This can be done by a certain refactoring.
Line 937: The pattern presented in this section is known by many names. [meszaros2007] calls this
Line 938: pattern a Test-Specific Subclass, while [feathers2004] uses the name subclass and override.
Line 939: The next listing shows a slightly changed version of the original MySut class.
Line 940: Listing 8.18. Refactored version of the MySut class
Line 941: public class MyRefactoredSut {
Line 942:     void myMethod() {
Line 943:         MyCollaborator collaborator = createCollaborator(); 
Line 944:         // some behaviour worth testing here which uses collaborator
Line 945:     }
Line 946:     // method extracted to facilitate testing 
Line 947:     MyCollaborator createCollaborator() { 
Line 948:         return new MyCollaborator();
Line 949:     }
Line 950: }
Line 951: 158
Line 952: 
Line 953: --- 페이지 174 ---
Line 954: Chapter 8. Points of Controversy
Line 955: Instead of invoking the new operator directly we call a newly created createCollaborator()
Line 956: method.
Line 957: I strongly recommend adding a short comment to the extracted method, so it is clear that it has
Line 958: been created for the purpose of conducting unit tests.
Line 959: The extracted method has a default access modifier, …and not very impressive content.
Line 960: As for the access modifier of the extracted createCollaborator() method, we can choose between
Line 961: making it protected or using default access protection (so-called "package-private"). This has some
Line 962: impact on our test classes. If we keep them in the same package as the production code, then the
Line 963: default access will be good enough. If they reside in different packages, then we will need to make the
Line 964: access less restrictive (protected). Some information on the organization of test packages is given in
Line 965: Section 10.1.
Line 966: The change introduced to the original class is minimal. All we did is a simple "extract method"
Line 967: refactoring. At first it might seem useless, but in fact it opens up a new testing possibility. Listing 8.19
Line 968: shows a test which takes advantage of this minor refactoring.
Line 969: Listing 8.19. Test of the refactored version of the MySut class
Line 970: public class MySutRefactoredTest {
Line 971:     private MyCollaborator collaborator;
Line 972:     class MyRefactoredSutSubclassed extends MyRefactoredSut { 
Line 973:         @Override
Line 974:         protected MyCollaborator createCollaborator() { 
Line 975:             return collaborator;
Line 976:         }
Line 977:     }
Line 978:     @Test
Line 979:     void testMyMethod() {
Line 980:         MyRefactoredSut sut = new MyRefactoredSutSubclassed(); 
Line 981:         collaborator = mock(MyCollaborator.class); 
Line 982:         when(collaborator.someMethod()).thenReturn(true);
Line 983:         assertThat(sut.myMethod()).isTrue();
Line 984:     }
Line 985: }
Line 986: A new class is introduced - a subclass of the original class (the one we intend to test). An object
Line 987: of this newly introduced class - MyRefactoredSutSubclassed - will be tested.
Line 988: The new class overrides the createCollaborator() method. The new implementation returns a
Line 989: test double of the MyCollaborator class.
Line 990: There is no need to inject collaborator to sut - this is done by a myMethod() of SUT’s parent
Line 991: class (see Listing 8.18).
Line 992: This simple technique, as presented in this section, can be really handy. Let us conclude by now
Line 993: listing some of its pros and cons:
Line 994: • It does not break the clients (the SUT’s API has not been changed) and it lets you write tests at the
Line 995: same time.
Line 996: • Changes are limited to the SUT class.
Line 997: 159
Line 998: 
Line 999: --- 페이지 175 ---
Line 1000: Chapter 8. Points of Controversy
Line 1001: • The design of production code is somewhat worse than it was before the refactoring. The newly
Line 1002: introduced method is awkward, and poses a potential encapsulation issue. (I must remark that I
Line 1003: have never seen any harm being done because of this slight reduction in the SUT’s integrity.)
Line 1004: • The SUT’s myMethod() still creates collaborators (instead of focusing on its business tasks), which
Line 1005: means its design has not been improved.
Line 1006: • Some people feel bad about testing a subclass instead of a real SUT. Personally, I would be very
Line 1007: happy to test the real thing, but just having a test of a strictly controlled subclass has proved more
Line 1008: than adequate for my purposes.
Line 1009: 8.7.4. Partial Mocking
Line 1010: The technique demonstrated in this section is very similar to the previously presented subclass and
Line 1011: override technique. The difference lies in the implementation, which requires less coding and relies on
Line 1012: some Mockito features.
Line 1013: The first step is almost identical to the one previously discussed. You must extract a method which
Line 1014: will deal solely with the creation of a new object. Listing 8.20 shows this.
Line 1015: Listing 8.20. Refactored version of the MySut class
Line 1016: public class MyPartialSut {
Line 1017:     public boolean myMethod() {
Line 1018:         MyCollaborator collaborator = createCollaborator();
Line 1019:         // some behaviour worth testing here which uses collaborator
Line 1020:     }
Line 1021:     // method extracted to facilitate testing
Line 1022:     MyCollaborator createCollaborator() { 
Line 1023:         return new MyCollaborator();
Line 1024:     }
Line 1025: }
Line 1026: Extracted method - identical as previously.
Line 1027:  So far, nothing new here. The difference is only visible when it comes to the tests class. But before
Line 1028: we inspect any new code, we need to learn something new about Mockito. Mockito allows us to spy
Line 1029: on real objects. That means we can decide which methods of a real object are invoked, and which are
Line 1030: being intercepted (and stubbed). The Javadocs of the spy() method explains this in the following
Line 1031: way: "Creates a spy of the real object. The spy calls real methods unless they are stubbed."
Line 1032:  This feature is deployed in Listing 8.21, which illustrates the use of a partial mocking technique.
Line 1033: Additionally, it presents a new static Mockito method - doReturn(). We use
Line 1034: doReturn(collaborator).when(sut).createCollaborator();
Line 1035: instead of
Line 1036: when(collaborator.someMethod()).thenReturn(true);
Line 1037: to avoid execution of the real method (someMethod()), because:
Line 1038: • the real method might throw some exceptions,
Line 1039: 160
Line 1040: 
Line 1041: --- 페이지 176 ---
Line 1042: Chapter 8. Points of Controversy
Line 1043: • if we are to verify it, then the number of invocations would grow.
Line 1044: Listing 8.21. Partial mocking test of the refactored MySut class
Line 1045: public class MySutPartialTest {
Line 1046:     @Test
Line 1047:     void testMyMethod() {
Line 1048:         MyPartialSut sut = spy(new MyPartialSut()); 
Line 1049:         MyCollaborator collaborator = mock(MyCollaborator.class);
Line 1050:         doReturn(collaborator).when(sut).createCollaborator(); 
Line 1051:         // normal Mockito stubbing/test spying test
Line 1052:     }
Line 1053: }
Line 1054: Surprise! The SUT has not been created using the new operator. Instead, another static method
Line 1055: of Mockito has been used.
Line 1056: Another unusual situation. We request that our SUT returns some canned values for a given
Line 1057: method invocation.
Line 1058: As was mentioned before, when created with the spy() method sut behaves like a normal object
Line 1059: of its class, until some of its methods are stubbed. In the case of our example, all the SUT’s
Line 1060: methods, except for createCollaborator(), would be executed as if sut had been created
Line 1061: with the new keyword. However, this one method - createCollaborator() - is different. When
Line 1062: createCollaborator() is executed, it is intercepted by Mockito, which returns some canned values
Line 1063: without touching the real sut object at all.
Line 1064: Well, this is confusing! Our SUT is performing two roles here: first of all, it is being tested (which is
Line 1065: not shown in the above listing, for reasons of brevity), and secondly, it is being used as a test stub, to
Line 1066: provide some canned values.
Line 1067: Partial mocking using the spy() method has its quirks. Make sure you read the Mockito
Line 1068: documentation before using it!
Line 1069: As for pros and cons, this technique is very similar to the one discussed previously, with the following
Line 1070: differences:
Line 1071: • There is no need to create a subclass. This is done "under the hood" by Mockito.
Line 1072: • The test code is more concise.
Line 1073: • The SUT is even more confusing than before …are we testing the real thing, or some strange
Line 1074: artifact created by Mockito?
Line 1075: In conclusion, we may say that this technique is very similar to the one discussed previously (Section
Line 1076: 8.7.3). The idea is the same: introduce changes to the SUT, and replace a part of it with some canned
Line 1077: behaviour. With the previously presented technique, this was done by hand. In this section, we have
Line 1078: learned how to do it with Mockito. There is no semantic difference between these two approaches.
Line 1079: Some people feel that the first technique is better (probably because they have visible control over the
Line 1080: subclassing of the SUT), while others will argue that the use of a framework makes things simpler by
Line 1081: automating things which were done by hand. It is really hard to choose a winner here.
Line 1082: 161
Line 1083: 
Line 1084: --- 페이지 177 ---
Line 1085: Chapter 8. Points of Controversy
Line 1086: The thing to remember is that this technique allows for the testing of some cumbersome code, but
Line 1087: does not make this code any better. If your aim is to verify things, this might be enough for you.
Line 1088: If you want cleaner code, you should rather think about redesigning your classes, as discussed
Line 1089: previously.
Line 1090: 8.7.5. Conclusions
Line 1091: In this section, we have discussed various options for testing code which uses the new operator to
Line 1092: create collaborators. Four different approaches have been discussed. Each of them had some pros and
Line 1093: cons, which have been discussed in the sections above. Table 8.3 summarizes the salient features of
Line 1094: each of the options on offer.
Line 1095: Table 8.3. Comparison of new operator testing approaches
Line 1096: PowerMock
Line 1097: redesign
Line 1098: refactor &
Line 1099: subclass
Line 1100: partial mocking
Line 1101: required SUT
Line 1102: change
Line 1103: no change
Line 1104: API change,
Line 1105: DI introduced
Line 1106: (breaking clients)
Line 1107: refactoring -
Line 1108: method extracted
Line 1109: refactoring -
Line 1110: method extracted
Line 1111: SUT’s design
Line 1112: no change
Line 1113: improved -
Line 1114: business logic
Line 1115: separated from
Line 1116: collaborators
Line 1117: creation
Line 1118: slightly worse than
Line 1119: before (method
Line 1120: extracted to
Line 1121: facilitate testing)
Line 1122: slightly worse than
Line 1123: before (method
Line 1124: extracted to
Line 1125: facilitate testing)
Line 1126: test code
Line 1127: different than usual simple
Line 1128: complicated,
Line 1129: testing subclass of
Line 1130: SUT
Line 1131: complicated, SUT
Line 1132: is tested and also
Line 1133: stubbed
Line 1134: amount of work
Line 1135: minimal
Line 1136: might be
Line 1137: significant
Line 1138: medium
Line 1139: medium (but less
Line 1140: than Refactor &
Line 1141: Subclass)
Line 1142: SUT is a final
Line 1143: class
Line 1144: not a problem
Line 1145: not a problem
Line 1146: can not use this
Line 1147: technique
Line 1148: can not use this
Line 1149: technique
Line 1150: • The PowerMock option is especially attractive when working with legacy code, which is
Line 1151: something we cannot modify (or are too scared to modify…). Its selling point is its ability to test
Line 1152: nasty code without any struggle.
Line 1153: • Redesign is probably the right way to go, but it requires more work than other techniques, and
Line 1154: breaks clients (because of API change). Its main benefit is improved design of production code.
Line 1155: • Both Refactor & Subclass and Partial Mocking offer similar benefits: the ability to test classes
Line 1156: without API change. However, they require some effort, cannot be used with final classes, and do
Line 1157: not make production code better (they rather make it slightly worse).
Line 1158: To conclude, I would strongly recommend that you always aim at making the design better, thus
Line 1159: leaving PowerMock as a tool of "last resort" – one that may save your life when battling with
Line 1160: especially vicious legacy code.
Line 1161: 162
Line 1162: 
Line 1163: --- 페이지 178 ---
Line 1164: Chapter 8. Points of Controversy
Line 1165: 8.8. Capturing Arguments to Collaborators
Line 1166:  Sometimes there is a need to verify whether arguments passed to collaborators are exactly as they
Line 1167: should be. This might be tricky, especially if they are created within the SUT’s method. In this section
Line 1168: we will discuss possible solutions which allow us to test such code.
Line 1169: First, let us meet the classes which will be used to demonstrate this issue. There are three of them:
Line 1170: • PIM - which represents a Personal Information Manager9. This is the SUT.
Line 1171: • Calendar - a collaborator of PIM.
Line 1172: • Meeting - argument to Calendar's method call.
Line 1173: All three types are shown in the listings below:
Line 1174: Listing 8.22. Calendar interface
Line 1175: public interface Calendar {
Line 1176:     public void addEvent(Event event);
Line 1177: }
Line 1178: Listing 8.23. Meeting class
Line 1179: public class Meeting implements Event {
Line 1180:     private final Date startDate;
Line 1181:     private final Date endDate;
Line 1182:     public Meeting(Date startDate, Date endDate) {
Line 1183:         this.startDate = new Date(startDate.getTime());
Line 1184:         this.endDate = new Date(endDate.getTime());
Line 1185:     }
Line 1186:     public Date getStartDate() {
Line 1187:         return startDate;
Line 1188:     }
Line 1189:     public Date getEndDate() {
Line 1190:         return endDate;
Line 1191:     }
Line 1192: }
Line 1193: Listing 8.24. PIM - the SUT
Line 1194: public class PIM {
Line 1195:     private final static int MILLIS_IN_MINUTE = 60 * 1000;
Line 1196:     private Calendar calendar;
Line 1197: 9http://en.wikipedia.org/wiki/Personal_information_manager
Line 1198: 163
Line 1199: 
Line 1200: --- 페이지 179 ---
Line 1201: Chapter 8. Points of Controversy
Line 1202:     public PIM(Calendar calendar) { 
Line 1203:         this.calendar = calendar;
Line 1204:     }
Line 1205:     public void addMeeting(Date startDate, int durationInMinutes) { 
Line 1206:         Date endDate = new Date(startDate.getTime()
Line 1207:                 + MILLIS_IN_MINUTE * durationInMinutes);
Line 1208:         Meeting meeting = new Meeting(startDate, endDate);
Line 1209:         calendar.addEvent(meeting);
Line 1210:     }
Line 1211: }
Line 1212: The collaborator is passed as a constructor argument - there will be no problem with injecting its
Line 1213: test double into the SUT within the test code.
Line 1214: A new object of the Meeting type is created, and is then used as a parameter to the
Line 1215: collaborator’s addEvent() method.
Line 1216: The problem we face when testing the PIM class is the following: how to make sure that the
Line 1217: addMeeting() method constructs a proper Meeting object? We need to somehow intercept the
Line 1218: parameter passed to calendar.addEvent(). There are two ways we can do it.
Line 1219: The problem with addMeeting() method testing comes from its poor design. It is
Line 1220: responsible for too many things - it deals with the creation of the Meeting object, and
Line 1221: interacts with the calendar collaborator. If we were to split its functionality and, for
Line 1222: example, introduce another collaborator responsible for the creation of proper Meeting
Line 1223: objects, than there would be no issue with testing arguments of the addEvent() method!
Line 1224: 8.8.1. Identical Objects
Line 1225: How about creating an object of Meeting class identical to the one which we expected would be
Line 1226: created by the addMeeting() method of SUT? Then we can verify whether the addEvent() method
Line 1227: of the calendar test double has been called with an identical Meeting object. Sounds good, so let us
Line 1228: try it!
Line 1229: Listing 8.25. Creating objects identical to expected arguments
Line 1230: public class PIMTest {
Line 1231:     private static final int ONE_HOUR = 60;
Line 1232:     private static final Date START_DATE = new Date();
Line 1233:     private static final int MILLIS_IN_MINUTE = 1000 * 60;
Line 1234:     private static final Date END_DATE = new Date(START_DATE.getTime()
Line 1235:         + ONE_HOUR * MILLIS_IN_MINUTE);
Line 1236:     @Test
Line 1237:     void shouldAddNewEventToCalendar() {
Line 1238:         Calendar calendar = mock(Calendar.class);
Line 1239:         PIM pim = new PIM(calendar);
Line 1240:         Meeting expectedMeeting = new Meeting(START_DATE, END_DATE); 
Line 1241:         pim.addMeeting(START_DATE, ONE_HOUR); 
Line 1242:         verify(calendar).addEvent(expectedMeeting); 
Line 1243:     }
Line 1244: }
Line 1245: 164
Line 1246: 
Line 1247: --- 페이지 180 ---
Line 1248: Chapter 8. Points of Controversy
Line 1249: An object of the Meeting class is created, identical to the one which we expect to be created by
Line 1250: SUT’s addMeeting() method.
Line 1251: Execution of the method of the SUT being tested.
Line 1252: Verification of whether the calendar.addEvent() method has been called with exactly the
Line 1253: same Meeting object.
Line 1254:  Looks good? Yes, but unfortunately it does not work. The test fails with the following failure
Line 1255: message (stack trace lines have been omitted for greater readability):
Line 1256: Listing 8.26. The test fails - objects are not identical
Line 1257: Argument(s) are different! Wanted:
Line 1258: calendar.addEvent(
Line 1259:     com.practicalunittesting.Meeting@1242b11
Line 1260: );
Line 1261: Actual invocation has different arguments:
Line 1262: calendar.addEvent(
Line 1263:     com.practicalunittesting.Meeting@1878144
Line 1264: );
Line 1265: Hmm, strange! I could have sworn that the addMeeting() method constructs a proper Meeting
Line 1266: object… And in fact it does! The problem lies elsewhere. The Meeting class does not override the
Line 1267: equals() method, so the objects’ equality is verified by reference, and thus fails. We can fix it by
Line 1268: adding appropriate methods10 to the Meeting class. Below you can see an implementation of the
Line 1269: equals() method generated by IntelliJ IDEA:
Line 1270: Listing 8.27. Implementation of the equals() method
Line 1271: @Override
Line 1272: public boolean equals(Object o) {
Line 1273:     if (this == o) return true;
Line 1274:     if (o == null || getClass() != o.getClass()) return false;
Line 1275:     Meeting meeting = (Meeting) o;
Line 1276:     if (endDate != null ? !endDate.equals(meeting.endDate)
Line 1277:         : meeting.endDate != null) return false;
Line 1278:     if (startDate != null ? !startDate.equals(meeting.startDate)
Line 1279:         : meeting.startDate != null) return false;
Line 1280:     return true;
Line 1281: }
Line 1282: @Override
Line 1283: public int hashCode() { ... } 
Line 1284: The hashCode() method implementation is not important right now, but remember: it should
Line 1285: also be overridden!
Line 1286: Now, if we rerun the test, it passes. Good, we have the first solution to the problem of verifying
Line 1287: whether the arguments passed to the collaborator are as expected.
Line 1288: However, this is not an ideal solution. On the plus side, we may say that:
Line 1289: 10Remember, if you override equals() you should also override hashCode()!
Line 1290: 165
Line 1291: 
Line 1292: --- 페이지 181 ---
Line 1293: Chapter 8. Points of Controversy
Line 1294: • it works!
Line 1295: • it is quite straightforward and easy to understand.
Line 1296: Unfortunately, there are more things to say on the minus side:
Line 1297: • A domain object in question might not have the equals() method implemented.
Line 1298: • In worse cases, a domain object’s equals() might already be implemented, and might behave
Line 1299: differently than as required by our test.
Line 1300: • The verification is "total" - it checks everything that our equals() method checks. This might lead
Line 1301: to overspecified tests.
Line 1302: • There is no direct assertion on the properties of the collaborator’s method argument.
Line 1303: Because of these downsides, we need to find some better solution.
Line 1304: 8.8.2. ArgumentCaptor
Line 1305:  Listing 8.28 shows another approach to writing a test for arguments of the collaborator’s method. It
Line 1306: uses the Mockito ArgumentCaptor class.
Line 1307: Listing 8.28. Capturing Arguments using ArgumentCaptor class
Line 1308: public class PIMTest {
Line 1309:     private static final int ONE_HOUR = 60;
Line 1310:     private static final Date START_DATE = new Date();
Line 1311:     private static final int MILLIS_IN_MINUTE = 1000 * 60;
Line 1312:     private static final Date END_DATE = new Date(START_DATE.getTime()
Line 1313:         + ONE_HOUR * MILLIS_IN_MINUTE);
Line 1314:     @Test
Line 1315:     void shouldAddNewEventToCalendar() {
Line 1316:         Calendar calendar = mock(Calendar.class);
Line 1317:         PIM pim = new PIM(calendar);
Line 1318:         ArgumentCaptor<Meeting> argument
Line 1319:             = ArgumentCaptor.forClass(Meeting.class); 
Line 1320:         pim.addMeeting(START_DATE, ONE_HOUR);
Line 1321:         verify(calendar).addEvent(argument.capture()); 
Line 1322:         Meeting meeting = argument.getValue(); 
Line 1323:         assertThat(meeting.getStartDate()).isEqualTo(START_DATE); 
Line 1324:         assertThat(meeting.getEndDate()).isEqualTo(END_DATE); 
Line 1325:     }
Line 1326: }
Line 1327: An object of the ArgumentCaptor class is created, which will gather information on arguments
Line 1328: of the type Meeting.
Line 1329: The addEvent() method’s having been called is verified, and Mockito is instructed to capture
Line 1330: arguments of this method call.
Line 1331: 166
Line 1332: 
Line 1333: --- 페이지 182 ---
Line 1334: Chapter 8. Points of Controversy
Line 1335: The actual argument to the addEvent() method is extracted from the ArgumentCaptor object.
Line 1336: Classic assertions are used to verify that the right object has been passed as an argument to the
Line 1337: addEvent() method.
Line 1338: As shown in Listing 8.28, we can use ArgumentCaptor to verify arguments passed to collaborators.
Line 1339: This solution has some positive features:
Line 1340: • it does not rely on the equals() method of the domain object (in our case, of the Meeting class),
Line 1341: • it can be used to test arbitrary properties of arguments,
Line 1342: • regular assertions are used to specify our expectations concerning the arguments.
Line 1343: In general, Mockito does a good job of facilitating the task of verifying a collaborator’s arguments.
Line 1344: However, as the Mockito documentation warns, having to use ArgumentCaptor might be indicative
Line 1345: that the code is not well-designed:
Line 1346: Over reliance on capturing arguments would be a code smell in my opinion as most
Line 1347: well abstracted code should not need to do this. However for testing legacy code and
Line 1348: interactions with outside systems ArgumentCaptors can be very useful.
Line 1349: — Mockito Documentation
Line 1350: 8.8.3. Hamcrest Matchers
Line 1351: ArgumentCaptor looks kind of heavy, so you might be interested to know that there is another
Line 1352: way. We can use Hamcrest matchers (see Section 7.7.1) to achieve a similar effect. The next
Line 1353: listing presents a test method which is functionally equivalent to the test code which used the
Line 1354: ArgumentCaptor class:
Line 1355: Listing 8.29. Capturing Arguments using Hamcrest Matchers
Line 1356: import static org.mockito.ArgumentMatchers.argThat;
Line 1357:     @Test
Line 1358:     void shouldAddNewEventToCalendarLambda() {
Line 1359:         Calendar calendar = mock(Calendar.class);
Line 1360:         PIM pim = new PIM(calendar);
Line 1361:         pim.addMeeting(START_DATE, ONE_HOUR);
Line 1362:         verify(calendar).addEvent(argThat(event ->
Line 1363:             event.getStartDate().equals(START_DATE) &&
Line 1364:             event.getEndDate().equals(END_DATE)
Line 1365:         ));
Line 1366:     }
Line 1367: As you can see, the code is shorter, and there is one significant difference: the assertions part is now
Line 1368: included within the verify() method call.
Line 1369: What we have lost (compared to ArgumentCaptor version) is the clarity of the failure message. If the
Line 1370: argument check fails, we will be surprised with a rather cryptic piece of information:
Line 1371: Argument(s) are different! Wanted:
Line 1372: calendar.addEvent(
Line 1373: 167
Line 1374: 
Line 1375: --- 페이지 183 ---
Line 1376: Chapter 8. Points of Controversy
Line 1377:     <P i m test$$ lambda$ 2 6 7/ 2 1 0 0 5 7 2 3 2 7>
Line 1378: );
Line 1379: Actual invocation has different arguments:
Line 1380: calendar.addEvent(
Line 1381:     Meeting{startDate=Fri Nov 09 15:18:38 CET 2018,
Line 1382:         endDate=Fri Nov 09 16:18:38 CET 2018}
Line 1383: );
Line 1384: Taking this nuisance into account, I would rather use the ArgumentCaptor approach.
Line 1385: 8.9. Files & Databases
Line 1386: At some point in the book, I quoted Michael Feathers who declared in 2005 that:
Line 1387: A test is not a unit test if […] It talks to the database […] It touches the file system.
Line 1388: I’ve lived by these words for a very long time. But things have changed over time. The filesystems
Line 1389: now are reliable and blazingly fast. The databases are lightweight and also many times faster than a
Line 1390: decade ago. Things look different now than they did in 2005. No wonder then that many have started
Line 1391: to question these rules.
Line 1392: Well, me too. I feel no shame to read the test data from a file (like we did in Section 7.11.2). And if
Line 1393: I work on a class which uses SuperCsv11 parser to read data from a CSV file, then I do not mock it
Line 1394: but I put few files with test data in the src/test/resources folder and I still call my tests unit tests.
Line 1395: And they run blazingly fast. And if they fail it is not because of the file system failures, but because I
Line 1396: messed up the business logic.
Line 1397: In other words, my private definition of a unit tests now also includes some simple file system
Line 1398: operations.
Line 1399: As for the databases, I’m more conservative here. I work a lot with the Spring framework which
Line 1400: provides a nice support for integration tests, so I don’t need my unit tests to deal with any database-
Line 1401: related operations. Still, if I wrote a different kind of code, which worked with database directly, then
Line 1402: who knows - maybe I would enhance my definition of unit tests and used an in-memory database to
Line 1403: verify some properties of my code.
Line 1404: The moral from this section is the following. Rules are great. There is a wisdom buried in them.
Line 1405: But they are not carved in stone, and as long as you keep the spirit of the law then, in my humble
Line 1406: opinion, you are doing OK. So, keep your unit tests blazingly fast and reliable, and independent
Line 1407: of each other, and repeatable, and focused on single classes. This is what really matters. And if you
Line 1408: succeed at this, then I don’t ask questions whether you touch the file system or not.
Line 1409: 8.10. Conclusions
Line 1410: The issues discussed in this chapter are nothing short of real-life problems. You will encounter them
Line 1411: mostly when working with legacy code, but also when making decisions about how to design the
Line 1412: application you are working on right now. And you will have to make your choices. In this section
Line 1413: we have discussed some important dilemmas, in the hope that when the time comes, you will have
Line 1414: enough knowledge to choose the right solution to the problem you are faced with. Maybe you will
Line 1415: 11http://super-csv.github.io/super-csv/
Line 1416: 168
Line 1417: 
Line 1418: --- 페이지 184 ---
Line 1419: Chapter 8. Points of Controversy
Line 1420: redesign your application and avoid the problem of private methods testing, or maybe you will use
Line 1421: the sort of brute-force techniques that will enable you to do that. This depends on the context of the
Line 1422: problem in hand, and on your own personal experience and preferences.
Line 1423: 169
Line 1424: 
Line 1425: --- 페이지 185 ---
Line 1426: Chapter 8. Points of Controversy
Line 1427: 8.11. Exercises
Line 1428: Let us recap what we have learned in this chapter by doing some exercises.
Line 1429: 8.11.1. Property Based Testing
Line 1430: You have already encountered the reverse() method (see Section 7.13.1), which - surprise, surprise!
Line 1431: - was reversing String arguments. Implement it and verify its correctness using the property based
Line 1432: testing technique (see Property-based testing). Use whichever dedicated library you find the most
Line 1433: appealing.
Line 1434: 8.11.2. Testing Legacy Code
Line 1435: So that you can fully understand the obstacles involved in testing legacy code, please write tests
Line 1436: for the code presented below. Try to repeat this exercise using the different techniques described
Line 1437: in Section 8.7 and Section 8.8. Make sure that you follow the "redesign" approach at least once,
Line 1438: changing the code so it is easily testable using standard techniques.
Line 1439: Listing 8.30. Sending emails is not hard, is it?
Line 1440: public class MailClient {
Line 1441:     public void sendEmail(String address, String title, String body) {
Line 1442:         Email email = new Email(address, title, body); 
Line 1443:         EmailServer.sendEmail(email); 
Line 1444:     }
Line 1445: }
Line 1446: Email has no functionality apart from keeping all this data.
Line 1447: sendEmail() is a static method.
Line 1448: Please note that static methods can be tested with the same approaches as the new operator, which
Line 1449: was discussed in Section 8.7.
Line 1450: 170