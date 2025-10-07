Line 1: 
Line 2: --- 페이지 205 ---
Line 3: CHAPTER 10
Line 4: Streamlining Your Tests
Line 5: You’ve wrapped up a couple of chapters that teach you how to use tests to
Line 6: keep your code clean. Now, it’s time to focus on the tests themselves.
Line 7: Your tests represent a significant investment. They’ll pay off by minimizing
Line 8: defects and allowing you to keep your production system clean through
Line 9: refactoring. But, they also represent a continual cost. You need to continually
Line 10: revisit your tests as your system changes. At times, you’ll want to make
Line 11: sweeping changes and might end up having to fix numerous broken tests as
Line 12: a result.
Line 13: In this chapter, you’ll learn to refactor your tests, much like you would
Line 14: refactor your production system, to maximize understanding and minimize
Line 15: maintenance costs. You’ll accomplish this by learning to identify a series of
Line 16: “smells” in your tests that make it harder to quickly understand them. You’ll
Line 17: work through an example or two of how you can transform each smell into
Line 18: de-odorized code.
Line 19: The deodorization process is quick. In reading through the chapter, you might
Line 20: think it would take a long time to clean a test similar to the example in the
Line 21: chapter. In reality, it’s often well under fifteen minutes of real work once you
Line 22: learn how to spot the problems.
Line 23: Tests as Documentation
Line 24: Your unit tests should provide lasting and trustworthy documentation of the
Line 25: capabilities of the classes you build. Tests provide opportunities to explain
Line 26: things that the code itself can’t do as easily. Well-designed tests can supplant
Line 27: a lot of the comments you might otherwise feel compelled to write.
Line 28: report erratum  •  discuss
Line 29: 
Line 30: --- 페이지 206 ---
Line 31: Documenting Your Tests with Consistent Names
Line 32: The more you combine cases into a single test, the more generic and mean-
Line 33: ingless the test name becomes. A test named matches doesn’t tell anyone squat
Line 34: about what it demonstrates.
Line 35: As you move toward more granular tests, each focused on a distinct behavior,
Line 36: you have the opportunity to impart more meaning in each of your test names.
Line 37: Instead of suggesting what context you’re going to test, you can suggest what
Line 38: happens as a result of invoking some behavior against a certain context.
Line 39: You’re probably thinking, “Real examples, please, Jeff, and not so much bab-
Line 40: ble.” Here you go:
Line 41: cooler, more descriptive name
Line 42: not-so-hot name
Line 43: withdrawalReducesBalanceByWithdrawnAmount
Line 44: makeSingleWithdrawal
Line 45: withdrawalOfMoreThanAvailableFundsGeneratesError
Line 46: attemptToWithdrawTooMuch
Line 47: multipleDepositsIncreaseBalanceBySumOfDeposits
Line 48: multipleDeposits
Line 49: That last test name seems kind of an obvious statement, but that’s because you
Line 50: already understand the ATM domain and the concept of deposits. Often,
Line 51: you’re in unfamiliar territory, where the code and business rules are unfamil-
Line 52: iar. A precise test name can provide you with extremely useful context.
Line 53: You can go too far. Reasonable test names probably consist of up to seven
Line 54: (plus or minus two) words. Longer names quickly become dense sentences
Line 55: that take time to digest. If test names are typically long, your design may be
Line 56: amiss.
Line 57: Seek a consistent form for your test names to reduce the friction that others
Line 58: experience when perusing your tests. Most of the test examples in this book
Line 59: are named to complete a sentence that starts with the test class name. For
Line 60: example:
Line 61: class APortfolio {
Line 62: @Test
Line 63: void increasesSizeWhenPurchasingNewSymbol() {
Line 64: // ...
Line 65: }
Line 66: }
Line 67: Concatenate each test name to the class name: “a portfolio increases size
Line 68: when purchasing a new symbol.”
Line 69: Another possible form:
Line 70: doingSomeOperationGeneratesSomeResult
Line 71: Chapter 10. Streamlining Your Tests • 190
Line 72: report erratum  •  discuss
Line 73: 
Line 74: --- 페이지 207 ---
Line 75: And another:
Line 76: someResultOccursUnderSomeCondition
Line 77: Or you might decide to go with the given-when-then naming pattern, which
Line 78: derives from a process known as behavior-driven development:
Line 79: 1
Line 80: givenSomeContextWhenDoingSomeBehaviorThenSomeResultOccurs
Line 81: Given-when-then test names can be a mouthful, though you can usually drop
Line 82: the givenSomeContext portion without creating too much additional work for
Line 83: your test reader:
Line 84: whenDoingSomeBehaviorThenSomeResultOccurs
Line 85: …which is about the same as doingSomeOperationGeneratesSomeResult.
Line 86: JUnit 5’s support for nested test classes allows you to structure your test
Line 87: class to directly support given-when-then:
Line 88: utj3-refactor-tests/01/src/test/java/portfolio/ANonEmptyPortfolio.java
Line 89: class ANonEmptyPortfolio {
Line 90: Portfolio portfolio = new Portfolio();
Line 91: int initialSize;
Line 92: @BeforeEach
Line 93: void purchaseASymbol() {
Line 94: portfolio.purchase("LSFT", 20);
Line 95: initialSize = portfolio.size();
Line 96: }
Line 97: @Nested
Line 98: class WhenPurchasingAnotherSymbol {
Line 99: @BeforeEach
Line 100: void purchaseAnotherSymbol() {
Line 101: portfolio.purchase("AAPL", 10);
Line 102: }
Line 103: @Test
Line 104: void increasesSize() {
Line 105: assertEquals(initialSize + 1, portfolio.size());
Line 106: }
Line 107: }
Line 108: }
Line 109: Which form you choose isn’t as important as being consistent. Your main
Line 110: goal: create easy-to-read test names that clearly impart meaning.
Line 111: 1.
Line 112: http://en.wikipedia.org/wiki/Behavior-driven_development
Line 113: report erratum  •  discuss
Line 114: Tests as Documentation • 191
Line 115: 
Line 116: --- 페이지 208 ---
Line 117: Keeping Your Tests Meaningful
Line 118: If others (or you yourself) have a tough time understanding what a test is
Line 119: doing, don’t add comments. That’s like adding footnotes to describe poorly
Line 120: written text. Improve the test instead, starting with its name. These are other
Line 121: things you can do:
Line 122: • Improve any local variable names.
Line 123: • Introduce meaningful constants.
Line 124: • Prefer matcher-based assertions (for example, those from AssertJ).
Line 125: • Split larger tests into smaller, more focused tests.
Line 126: • Move test clutter to helper methods and @Before methods.
Line 127: Rework test names and code to tell stories instead of introducing
Line 128: explanatory comments.
Line 129: Searching for an Understanding
Line 130: You’re tasked with enhancing the search capabilities of an application. You
Line 131: know you must change the util.Search class, but you’re not at all familiar with
Line 132: it. You turn to the tests. Well, a test—there’s only one. You roll your eyes in
Line 133: annoyance and then begin struggling to figure out what this test is trying to
Line 134: prove:
Line 135: utj3-refactor-tests/01/src/test/java/util/SearchTest.java
Line 136: public class SearchTest {
Line 137: @Test
Line 138: public void testSearch() {
Line 139: try {
Line 140: String pageContent = "There are certain queer times and occasions "
Line 141: + "in this strange mixed affair we call life when a man takes "
Line 142: + "this whole universe for a vast practical joke, though "
Line 143: + "the wit thereof he but dimly discerns, and more than "
Line 144: + "suspects that the joke is at nobody's expense but his own.";
Line 145: byte[] bytes = pageContent.getBytes();
Line 146: ByteArrayInputStream stream = new ByteArrayInputStream(bytes);
Line 147: // search
Line 148: Search search = new Search(stream, "practical joke", "1");
Line 149: Search.LOGGER.setLevel(Level.OFF);
Line 150: search.setSurroundingCharacterCount(10);
Line 151: search.execute();
Line 152: assertFalse(search.errored());
Line 153: List<Match> matches = search.getMatches();
Line 154: assertNotNull(matches);
Line 155: assertTrue(matches.size() >= 1);
Line 156: Chapter 10. Streamlining Your Tests • 192
Line 157: report erratum  •  discuss
Line 158: 
Line 159: --- 페이지 209 ---
Line 160: Match match = matches.get(0);
Line 161: assertEquals("practical joke", match.searchString());
Line 162: assertEquals("or a vast practical joke, though t",
Line 163: match.surroundingContext());
Line 164: stream.close();
Line 165: // negative
Line 166: URLConnection connection =
Line 167: new URL("http://bit.ly/15sYPA7").openConnection();
Line 168: InputStream inputStream = connection.getInputStream();
Line 169: search = new Search(
Line 170: inputStream, "smelt", "http://bit.ly/15sYPA7");
Line 171: search.execute();
Line 172: assertEquals(0, search.getMatches().size());
Line 173: stream.close();
Line 174: } catch (Exception e) {
Line 175: e.printStackTrace();
Line 176: fail("exception thrown in test" + e.getMessage());
Line 177: }
Line 178: }
Line 179: }
Line 180: (Text in pageContent by Herman Melville from Moby Dick.)
Line 181: Match is only a Java record with the three String fields: searchTitle, searchString,
Line 182: and surroundingContext.
Line 183: The test name, testSearch, doesn’t tell you anything useful. A couple of com-
Line 184: ments don’t add much value either. To fully understand what’s going on,
Line 185: you’ll have to read the test line by line and try to piece its steps together.
Line 186: (You won’t see the Search class itself in this chapter since your focus will
Line 187: solely be on cleaning up the tests for better understanding. Visit the source
Line 188: distribution if you’re curious about the Search class.)
Line 189: You decide to refactor testSearch while you work through understanding it,
Line 190: with the goal of shaping it into one or more clear, expressive tests. You look
Line 191: for various test smells—nuggets of code that emanate an odor. Odors aren’t
Line 192: necessarily foul, though they can greatly diminish the readability of your
Line 193: tests.
Line 194: Test Smell: Legacy Code Constructs
Line 195: You’ll be making several passes through the test, each with a different intent.
Line 196: A quick scan of the test reveals old-school Java and JUnit, evidenced by the
Line 197: lack of local variable type inferencing and the unnecessary use of public for
Line 198: the class and test method. One of the best things about the newer versions
Line 199: of both Java and JUnit is their ability to simplify your code.
Line 200: report erratum  •  discuss
Line 201: Test Smell: Legacy Code Constructs • 193
Line 202: 
Line 203: --- 페이지 210 ---
Line 204: First, make a couple of quick cleanup passes:
Line 205: 1.
Line 206: Remove public from the test class and test methods. They are clutter.
Line 207: 2.
Line 208: Replace local variable type names with the var type.
Line 209: Here’s a snippet:
Line 210: utj3-refactor-tests/02/src/test/java/util/SearchTest.java
Line 211: class SearchTest {
Line 212: ➤
Line 213: @Test
Line 214: void testSearch() {
Line 215: ➤
Line 216: try {
Line 217: var pageContent = "There are certain queer times and occasions "
Line 218: // ...
Line 219: var bytes = pageContent.getBytes();
Line 220: var stream = new ByteArrayInputStream(bytes);
Line 221: //...
Line 222: The elimination of a few unnecessary tokens will begin to help you focus more
Line 223: on what’s relevant.
Line 224: Test Smell: Unnecessary Test Code
Line 225: The test testSearch() contains a few assertions, none expecting exceptions
Line 226: themselves. If the test code throws an exception, a try/catch block catches it,
Line 227: spews a stack trace onto System.out, and explicitly fails the test.
Line 228: Unless your test expects an exception to be thrown—because you’ve explicitly
Line 229: designed it to set the stage for throwing an exception—you can let other
Line 230: exceptions fly. Don’t worry, JUnit traps any exceptions that explode out of
Line 231: your test. When JUnit catches an unexpected exception, it marks the test as
Line 232: an error, and displays the stack trace in its output.
Line 233: The try/catch block surrounding all the test code adds no value. Remove it.
Line 234: Modify the signature of testSearch() to indicate that it can throw an IOException:
Line 235: utj3-refactor-tests/03/src/test/java/util/SearchTest.java
Line 236: @Test
Line 237: void testSearch() throws IOException {
Line 238: var pageContent = "There are certain queer times and occasions "
Line 239: // ...
Line 240: var bytes = pageContent.getBytes();
Line 241: var stream = new ByteArrayInputStream(bytes);
Line 242: // ...
Line 243: stream.close();
Line 244: }
Line 245: Careful editing helps your tests tell a clear story about system behaviors. And
Line 246: as long as your tests pass, you can trust that story.
Line 247: Chapter 10. Streamlining Your Tests • 194
Line 248: report erratum  •  discuss
Line 249: 
Line 250: --- 페이지 211 ---
Line 251: Comments represent a failure to let the code tell the story. For now, delete
Line 252: the two comments in testSearch.
Line 253: Tests provide trustworthy documentation on the unit behaviors
Line 254: of your system.
Line 255: About eight statements into the test method, you notice a not-null assert—an
Line 256: assertion that verifies that a value is not null:
Line 257: utj3-refactor-tests/02/src/test/java/util/SearchTest.java
Line 258: var matches = search.getMatches();
Line 259: assertNotNull(matches);
Line 260: assertTrue(matches.size() >= 1);
Line 261: The first line assigns the result of search.getMatches() to the matches local variable. The
Line 262: second statement asserts that matches is not a null value. The final line verifies
Line 263: that the size of matches is at least 1.
Line 264: Checking that a variable isn’t null before dereferencing it is a good thing, right?
Line 265: In production code, perhaps. In this test, the call to assertNotNull is again clutter.
Line 266: It adds no value: if matches is actually null, the call to matches.size() generates a
Line 267: NullPointerException. JUnit traps this exception and errors the test. You’re notified
Line 268: of the error, and it’s no harder to figure out what the problem is.
Line 269: Like the try/catch block, calling assertNotNull adds no value. Remove it:
Line 270: utj3-refactor-tests/03/src/test/java/util/SearchTest.java
Line 271: var matches = search.getMatches();
Line 272: assertTrue(matches.size() >= 1);
Line 273: That’s one fewer line of test to wade through!
Line 274: Test Smells: Generalized and Stepwise Assertions
Line 275: A well-structured test distills the interaction with the system to three steps:
Line 276: arranging the data, acting on the system, and asserting on the results (see
Line 277: Scannability: Arrange—Act—Assert, on page 18). Although the test requires
Line 278: detailed code to accomplish each of these steps, you can improve understand-
Line 279: ing by organizing those details into abstractions—code elements that maximize
Line 280: the essential concepts and hide the unnecessary details.
Line 281: Good tests provide examples of how clients interact with the
Line 282: system.
Line 283: report erratum  •  discuss
Line 284: Test Smells: Generalized and Stepwise Assertions • 195
Line 285: 
Line 286: --- 페이지 212 ---
Line 287: The following part of the test starts with a statement that appears to be the
Line 288: act step—a call to search.getMatches():
Line 289: utj3-refactor-tests/03/src/test/java/util/SearchTest.java
Line 290: var matches = search.getMatches();
Line 291: assertTrue(matches.size() >= 1);
Line 292: var match = matches.get(0);
Line 293: assertEquals("practical joke", match.searchString());
Line 294: assertEquals("or a vast practical joke, though t",
Line 295: match.surroundingContext());
Line 296: The hint that search.getMatches represents the act step is that it’s followed
Line 297: immediately by four lines of assertion-related code that appears to check the
Line 298: list of matches returned by search.getMatches(). These lines require stepwise
Line 299: reading. Here is a quick attempt at paraphrasing them:
Line 300: • Ensure there’s at least one match
Line 301: • Get the first match
Line 302: • Ensure that its search string is “practical joke”
Line 303: • Ensure that its surrounding context is some longer string
Line 304: The first statement—assertTrue(matches.size() >= 1—appears to be an unnecessar-
Line 305: ily generalized assertion. A quick scan of the Melville content (declared in the
Line 306: arrange step) reveals that the search string "practical joke" appears once and
Line 307: exactly once in the test.
Line 308: Most tests should make precise assertions, usually with assertEquals. You are
Line 309: creating the tests—you can set them up to be precise. To test a one-based
Line 310: case (search results find a single match), create content with exactly one
Line 311: match for the given search string and then assert that the one match exists.
Line 312: In this case, you don’t need to use >=. You could replace that with a precise
Line 313: comparison: assertEquals(1, matches.size()). But you have an even better resolution.
Line 314: The test tediously takes four lines to verify what seems to be a single concept:
Line 315: that the list of matches contains a single match object, initialized with a
Line 316: specific search string and surrounding context. Java supports declaring an
Line 317: initialized list, which lets you simplify the test to a single-statement assert:
Line 318: utj3-refactor-tests/04/src/test/java/util/SearchTest.java
Line 319: var matches = search.getMatches();
Line 320: assertEquals(List.of(
Line 321: new Match("1",
Line 322: "practical joke",
Line 323: "or a vast practical joke, though t")),
Line 324: matches);
Line 325: Chapter 10. Streamlining Your Tests • 196
Line 326: report erratum  •  discuss
Line 327: 
Line 328: --- 페이지 213 ---
Line 329: Anywhere you find two or more lines of stepwise assertion code that asserts
Line 330: a single concept, distill them to a single, clear statement in the test. Sometimes a
Line 331: short helper method is all it takes. If you use AssertJ, you can create a custom
Line 332: matcher that provides a concise assertion.
Line 333: Amplify abstractions in your test. Hide the implementation specifics elsewhere.
Line 334: In the second chunk of test code, near the end of the method, you spot
Line 335: another small opportunity for introducing an abstraction. The final assertion
Line 336: (highlighted) compares the size of search matches to 0:
Line 337: utj3-refactor-tests/04/src/test/java/util/SearchTest.java
Line 338: @Test
Line 339: void testSearch() throws IOException {
Line 340: // ...
Line 341: search.execute();
Line 342: assertEquals(0, search.getMatches().size());
Line 343: ➤
Line 344: stream.close();
Line 345: }
Line 346: The missing abstraction is the concept of emptiness. Altering the assertion
Line 347: reduces the extra mental overhead needed to understand the size comparison:
Line 348: utj3-refactor-tests/05/src/test/java/util/SearchTest.java
Line 349: search.execute();
Line 350: assertTrue(search.getMatches().isEmpty());
Line 351: ➤
Line 352: stream.close();
Line 353: Every small amount of mental clutter adds up. A system with never-ending
Line 354: clutter wears you down, much as road noise builds to create further fatigue
Line 355: on a long car trip.
Line 356: Test Smell: Missing Abstractions
Line 357: A well-abstracted test emphasizes everything that’s important to understanding
Line 358: it and de-emphasizes anything that’s not. Any data used in a test should help
Line 359: tell its story.
Line 360: Sometimes, you’re forced to supply data to get code to compile, even though
Line 361: that data is irrelevant to the test at hand. For example, a method might take
Line 362: additional arguments that have no impact on the test.
Line 363: Your test contains some magic literals that aren’t at all clear:
Line 364: utj3-refactor-tests/05/src/test/java/util/SearchTest.java
Line 365: var search = new Search(stream, "practical joke", "1");
Line 366: report erratum  •  discuss
Line 367: Test Smell: Missing Abstractions • 197
Line 368: 
Line 369: --- 페이지 214 ---
Line 370: And:
Line 371: utj3-refactor-tests/05/src/test/java/util/SearchTest.java
Line 372: assertEquals(List.of(
Line 373: new Match("1",
Line 374: "practical joke",
Line 375: "or a vast practical joke, though t")),
Line 376: matches);
Line 377: Perhaps these were magically conjured by a wizard who chose to keep their
Line 378: meanings arcane.
Line 379: You’re not sure what the "1" string represents, so you navigate into the con-
Line 380: structors for Search and Match. You discover that "1" is a search title, a field
Line 381: whose value appears irrelevant right now.
Line 382: Including the "1" literal raises unnecessary questions. What does it represent?
Line 383: How, if at all, is it relevant to the results of the test?
Line 384: At least one other magic literal exists. The second call to the Search constructor
Line 385: contains a URL as the title argument:
Line 386: utj3-refactor-tests/05/src/test/java/util/SearchTest.java
Line 387: var connection =
Line 388: new URL("http://bit.ly/15sYPA7").openConnection();
Line 389: var inputStream = connection.getInputStream();
Line 390: search = new Search(
Line 391: inputStream, "smelt", "http://bit.ly/15sYPA7");
Line 392: ➤
Line 393: At first glance, it appears that the URL has a correlation with the URL passed
Line 394: to the URL constructor two statements earlier. But digging reveals that no real
Line 395: correlation exists.
Line 396: Developers waste time when they must dig around to find answers. You’ll
Line 397: help them by introducing an intention-revealing constant. Replace the con-
Line 398: fusing URL and the "1" magic literal with the A_TITLE constant, which suggests
Line 399: a title with any value.
Line 400: Here’s the latest version of the test, highlighting lines with the new abstraction:
Line 401: utj3-refactor-tests/06/src/test/java/util/SearchTest.java
Line 402: class SearchTest {
Line 403: static final String A_TITLE = "1";
Line 404: ➤
Line 405: @Test
Line 406: void testSearch() throws IOException {
Line 407: var pageContent = "There are certain queer times and occasions "
Line 408: + "in this strange mixed affair we call life when a man takes "
Line 409: + "this whole universe for a vast practical joke, though "
Line 410: + "the wit thereof he but dimly discerns, and more than "
Line 411: + "suspects that the joke is at nobody's expense but his own.";
Line 412: Chapter 10. Streamlining Your Tests • 198
Line 413: report erratum  •  discuss
Line 414: 
Line 415: --- 페이지 215 ---
Line 416: var bytes = pageContent.getBytes();
Line 417: var stream = new ByteArrayInputStream(bytes);
Line 418: var search = new Search(stream, "practical joke", A_TITLE);
Line 419: ➤
Line 420: Search.LOGGER.setLevel(Level.OFF);
Line 421: search.setSurroundingCharacterCount(10);
Line 422: search.execute();
Line 423: assertFalse(search.errored());
Line 424: var matches = search.getMatches();
Line 425: assertEquals(List.of(
Line 426: new Match(A_TITLE,
Line 427: ➤
Line 428: "practical joke",
Line 429: "or a vast practical joke, though t")),
Line 430: matches);
Line 431: stream.close();
Line 432: var connection =
Line 433: new URL("http://bit.ly/15sYPA7").openConnection();
Line 434: var inputStream = connection.getInputStream();
Line 435: search = new Search(
Line 436: inputStream, "smelt", A_TITLE);
Line 437: ➤
Line 438: search.execute();
Line 439: assertTrue(search.getMatches().isEmpty());
Line 440: stream.close();
Line 441: }
Line 442: }
Line 443: You could have named the constant ANY_TITLE or ARBITRARY_TITLE. Or, you might
Line 444: have used an empty string, which suggests data that you don’t care about
Line 445: (though sometimes the distinction between an empty string and a nonempty
Line 446: string is relevant).
Line 447: Test Smell: Bloated Construction
Line 448: The Search class requires you to pass an InputStream on a Search object through
Line 449: its constructor. Your test builds an InputStream in two places. The first construc-
Line 450: tion requires three statements:
Line 451: utj3-refactor-tests/06/src/test/java/util/SearchTest.java
Line 452: var pageContent = "There are certain queer times and occasions "
Line 453: + "in this strange mixed affair we call life when a man takes "
Line 454: + "this whole universe for a vast practical joke, though "
Line 455: + "the wit thereof he but dimly discerns, and more than "
Line 456: + "suspects that the joke is at nobody's expense but his own.";
Line 457: var bytes = pageContent.getBytes();
Line 458: var stream = new ByteArrayInputStream(bytes);
Line 459: The test contains implementation detail specifics involving extracting bytes from
Line 460: a string and then creating a ByteArrayInputStream. That’s stuff you don’t need to
Line 461: report erratum  •  discuss
Line 462: Test Smell: Bloated Construction • 199
Line 463: 
Line 464: --- 페이지 216 ---
Line 465: see to understand the test, and it represents a missing abstraction. Introduce
Line 466: a helper method that creates an InputStream on a provided string of text:
Line 467: utj3-refactor-tests/07/src/test/java/util/SearchTest.java
Line 468: class SearchTest {
Line 469: // ...
Line 470: @Test
Line 471: void testSearch() throws IOException {
Line 472: var stream = streamOn("There are certain queer times and occasions "
Line 473: ➤
Line 474: + "in this strange mixed affair we call life when a man "
Line 475: + "takes this whole universe for a vast practical joke, "
Line 476: + "though the wit thereof he but dimly discerns, and more "
Line 477: + "than suspects that the joke is at nobody's expense but his own.");
Line 478: var search = new Search(stream, "practical joke", A_TITLE);
Line 479: // ...
Line 480: }
Line 481: private ByteArrayInputStream streamOn(String text) {
Line 482: ➤
Line 483: return new ByteArrayInputStream(text.getBytes());
Line 484: ➤
Line 485: }
Line 486: ➤
Line 487: }
Line 488: Morphing arbitrary detail into clear declarations is gradually improving the test.
Line 489: Test Smell: Multiple Assertions
Line 490: Your long test appears to represent two distinct cases. The first demonstrates
Line 491: finding a search result, and the second represents finding no match. The
Line 492: blank line provides a clear dividing point:
Line 493: utj3-refactor-tests/07/src/test/java/util/SearchTest.java
Line 494: @Test
Line 495: void testSearch() throws IOException {
Line 496: var stream = streamOn("There are certain queer times and occasions "
Line 497: // ...
Line 498: var search = new Search(stream, "practical joke", A_TITLE);
Line 499: Search.LOGGER.setLevel(Level.OFF);
Line 500: search.setSurroundingCharacterCount(10);
Line 501: search.execute();
Line 502: assertFalse(search.errored());
Line 503: var matches = search.getMatches();
Line 504: assertEquals(List.of(
Line 505: new Match(A_TITLE,
Line 506: "practical joke",
Line 507: "or a vast practical joke, though t")),
Line 508: matches);
Line 509: stream.close();
Line 510: var connection =
Line 511: new URL("http://bit.ly/15sYPA7").openConnection();
Line 512: var inputStream = connection.getInputStream();
Line 513: Chapter 10. Streamlining Your Tests • 200
Line 514: report erratum  •  discuss
Line 515: 
Line 516: --- 페이지 217 ---
Line 517: search = new Search(
Line 518: inputStream, "smelt", A_TITLE);
Line 519: search.execute();
Line 520: assertTrue(search.getMatches().isEmpty());
Line 521: stream.close();
Line 522: }
Line 523: Split the test into two test methods, coming up with a better name for each
Line 524: (the code won’t compile until both test names are distinct). Also, take a
Line 525: moment to rename the test class to ASearch.
Line 526: Verifying only one behavior per test facilitates concise test naming.
Line 527: The resulting two test methods:
Line 528: utj3-refactor-tests/08/src/test/java/util/ASearch.java
Line 529: @Test
Line 530: void returnsMatchesWithSurroundingContext() throws IOException {
Line 531: var stream = streamOn("There are certain queer times and occasions "
Line 532: // ...
Line 533: var search = new Search(stream, "practical joke", A_TITLE);
Line 534: Search.LOGGER.setLevel(Level.OFF);
Line 535: search.setSurroundingCharacterCount(10);
Line 536: search.execute();
Line 537: assertFalse(search.errored());
Line 538: var matches = search.getMatches();
Line 539: assertEquals(List.of(
Line 540: new Match(A_TITLE,
Line 541: "practical joke",
Line 542: "or a vast practical joke, though t")),
Line 543: matches);
Line 544: stream.close(); // delete me
Line 545: ➤
Line 546: }
Line 547: @Test
Line 548: void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
Line 549: var connection =
Line 550: new URL("http://bit.ly/15sYPA7").openConnection();
Line 551: var inputStream = connection.getInputStream();
Line 552: var search = new Search(inputStream, "smelt", A_TITLE);
Line 553: ➤
Line 554: search.execute();
Line 555: assertTrue(search.getMatches().isEmpty());
Line 556: inputStream.close();
Line 557: ➤
Line 558: }
Line 559: The listing shows fixes to two compile failures that occurred when splitting.
Line 560: First, since the search variable was re-used in the original test, its use in the
Line 561: second test now needs a type declaration. The var type will suffice.
Line 562: report erratum  •  discuss
Line 563: Test Smell: Multiple Assertions • 201
Line 564: 
Line 565: --- 페이지 218 ---
Line 566: Also, the second test’s last line (which closes the stream) wasn’t compiling.
Line 567: Amusingly, it turns out that the combined mess of a single test was calling
Line 568: close twice on stream, and not at all on inputStream. Changing the last line to
Line 569: inputStream.close() fixed the problem.
Line 570: You can delete the line that closes stream in the first test. There’s no need to
Line 571: close a ByteArrayInputStream (least of all in a test). (The other close needs to occur
Line 572: to avoid connection and resource issues for other tests or for itself if run
Line 573: multiple times.)
Line 574: Next, use Java’s try-with-resources feature to ensure that inputStream gets
Line 575: closed. You can then delete the inputStream.close() statement for good:
Line 576: utj3-refactor-tests/09/src/test/java/util/ASearch.java
Line 577: @Test
Line 578: void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
Line 579: var connection =
Line 580: new URL("http://bit.ly/15sYPA7").openConnection();
Line 581: try (var inputStream = connection.getInputStream()) {
Line 582: var search = new Search(inputStream, "smelt", A_TITLE);
Line 583: search.execute();
Line 584: assertTrue(search.getMatches().isEmpty());
Line 585: }
Line 586: }
Line 587: Test Smell: Irrelevant Details in a Test
Line 588: Your tests should execute cleanly, showing only a summary with the passing
Line 589: and failing tests. Don’t allow your test run to be littered with dozens or perhaps
Line 590: hundreds and more lines of log messages, “expected” exception stack traces,
Line 591: and System.out.println clutter.
Line 592: Ensure test execution does not pollute console output.
Line 593: When your test summary is clean, any new exceptions will stand out like a
Line 594: sore thumb rather than get lost in a sea of stack traces. You’ll also easily spot
Line 595: any new console output that you’ve temporarily added.
Line 596: In the prior section, you split one larger test into two. Now, when you run
Line 597: your tests, you’ll notice some logging output:
Line 598: Mar 29, 2024 1:35:50 PM util.Search search
Line 599: INFO: searching matches for pattern:smelt
Line 600: Chapter 10. Streamlining Your Tests • 202
Line 601: report erratum  •  discuss
Line 602: 
Line 603: --- 페이지 219 ---
Line 604: The first test contains the following line, but the second test does not:
Line 605: Search.LOGGER.setLevel(Level.OFF);
Line 606: Suppressing logger output when the second test runs would be as easy as
Line 607: adding the setLevel call to the second test. But that’s the wrong place for it.
Line 608: While only a single line, the code needed to suppress logging is a distraction
Line 609: that adds no meaning to any test. De-emphasize the setLevel call by moving it
Line 610: to a @BeforeEach method.
Line 611: utj3-refactor-tests/09/src/test/java/util/ASearch.java
Line 612: @BeforeEach
Line 613: void suppressLogging() {
Line 614: Search.LOGGER.setLevel(Level.OFF);
Line 615: }
Line 616: // ...
Line 617: Looking for further irrelevant details, you ponder the assertion in the first
Line 618: test that ensures the search has not errored:
Line 619: utj3-refactor-tests/09/src/test/java/util/ASearch.java
Line 620: var search = new Search(stream, "practical joke", A_TITLE);
Line 621: search.setSurroundingCharacterCount(10);
Line 622: search.execute();
Line 623: assertFalse(search.errored());
Line 624: ➤
Line 625: var matches = search.getMatches();
Line 626: assertEquals(List.of(
Line 627: // ...
Line 628: The assertion appears valid—a second postcondition of running a search.
Line 629: But it hints at a missing test case: if there’s an assertFalse, an assertTrue should
Line 630: exist. For now, delete the assertion and add it to your “todo” test list (see
Line 631: Covering Other Cases: Creating a Test List, on page 24). You’ll return to add
Line 632: a couple of new tests once you’ve streamlined all the test code.
Line 633: Take care when moving details to @BeforeEach or helper methods. Don’t remove
Line 634: information from a test that’s essential to understanding it.
Line 635: Good tests contain all the information needed to understand them.
Line 636: Poor tests send you on scavenger hunts.
Line 637: Test Smell: Misleading Organization
Line 638: Speed up cognition by making the act, arrange, and assert parts of a test (see
Line 639: Scannability: Arrange—Act—Assert, on page 18) explicit. Arrows in the follow-
Line 640: ing listing show the blank lines to insert around the act step:
Line 641: report erratum  •  discuss
Line 642: Test Smell: Misleading Organization • 203
Line 643: 
Line 644: --- 페이지 220 ---
Line 645: utj3-refactor-tests/10/src/test/java/util/ASearch.java
Line 646: @Test
Line 647: void returnsMatchesWithSurroundingContext() {
Line 648: var stream = streamOn("There are certain queer times and occasions "
Line 649: // ...
Line 650: var search = new Search(stream, "practical joke", A_TITLE);
Line 651: search.setSurroundingCharacterCount(10);
Line 652: ➤
Line 653: search.execute();
Line 654: ➤
Line 655: var matches = search.getMatches();
Line 656: assertEquals(List.of(
Line 657: new Match(A_TITLE,
Line 658: "practical joke",
Line 659: "or a vast practical joke, though t")),
Line 660: matches);
Line 661: }
Line 662: @Test
Line 663: void returnsNoMatchesWhenSearchTextNotFound() throws IOException {
Line 664: var connection =
Line 665: new URL("http://bit.ly/15sYPA7").openConnection();
Line 666: try (var inputStream = connection.getInputStream()) {
Line 667: var search = new Search(inputStream, "smelt", A_TITLE);
Line 668: ➤
Line 669: search.execute();
Line 670: ➤
Line 671: assertTrue(search.getMatches().isEmpty());
Line 672: }
Line 673: }
Line 674: You’re getting close. Time for a final pass against the two tests!
Line 675: Test Smell: Implicit Meaning
Line 676: The big question every test must clearly answer: why does it expect the result
Line 677: it does? Developers must be able to correlate any assertions with the arrange
Line 678: step. Unclear correlation forces developers to wade through code for meaning.
Line 679: The returnsMatchesWithSurroundingContext test searches for practical joke in a long
Line 680: string, expecting one match. A patient reader could determine where practical
Line 681: joke appears and then figure out that ten characters before it and ten charac-
Line 682: ters after it represent the string:
Line 683: "or a vast practical joke, though t"
Line 684: But making developers dig for understanding is rude. Make things explicit
Line 685: by choosing better test data. Change the input stream to contain a small
Line 686: amount of text. Then, change the content so that the surrounding context
Line 687: information doesn’t need to be explicitly counted:
Line 688: Chapter 10. Streamlining Your Tests • 204
Line 689: report erratum  •  discuss
Line 690: 
Line 691: --- 페이지 221 ---
Line 692: utj3-refactor-tests/11/src/test/java/util/ASearch.java
Line 693: @Test
Line 694: void returnsMatchesWithSurroundingContext() {
Line 695: var stream = streamOn("""
Line 696: ➤
Line 697: rest of text here
Line 698: ➤
Line 699: 1234567890search term1234567890
Line 700: ➤
Line 701: more rest of text""");
Line 702: ➤
Line 703: var search = new Search(stream, "search term", A_TITLE);
Line 704: ➤
Line 705: search.setSurroundingCharacterCount(10);
Line 706: search.execute();
Line 707: var matches = search.getMatches();
Line 708: assertEquals(List.of(
Line 709: new Match(A_TITLE,
Line 710: "search term",
Line 711: ➤
Line 712: "1234567890search term1234567890")),
Line 713: ➤
Line 714: matches);
Line 715: }
Line 716: Now, it’s fairly easy to see why a surrounding character count of 10 produces
Line 717: the corresponding context results in the Match object.
Line 718: You have no end of ways to improve the correlation across a test. Meaningful
Line 719: constants, better variable names, better data, and sometimes even doing
Line 720: small calculations in the test can help. Use your creativity here!
Line 721: Diversion: Speeding Up Your Tests
Line 722: As you incrementally shape the design of your tests, you’ll be distracted by
Line 723: other opportunities to improve them. You can divert to address those oppor-
Line 724: tunities, or you can add a reminder to do so.
Line 725: Let’s use returnsNoMatchesWhenSearchTextNotFound to take a quick detour and speed
Line 726: up the second test. It works against a live URL’s input stream, making it slow.
Line 727: Since your first test is a fast unit test that verifies the happy path case, you
Line 728: want a similarly fast test to cover the unhappy path case. (You might want
Line 729: to retain the live test for integration testing purposes.)
Line 730: Initialize the stream field to contain a small bit of arbitrary text. To help make
Line 731: the test’s circumstance clear, search for "text that ain't gonna match":
Line 732: utj3-refactor-tests/11/src/test/java/util/ASearch.java
Line 733: @Test
Line 734: void returnsNoMatchesWhenSearchTextNotFound() {
Line 735: ➤
Line 736: var stream = streamOn("text that ain't gonna match");
Line 737: ➤
Line 738: var search = new Search(stream, "missing search term", A_TITLE);
Line 739: ➤
Line 740: report erratum  •  discuss
Line 741: Test Smell: Implicit Meaning • 205
Line 742: 
Line 743: --- 페이지 222 ---
Line 744: search.execute();
Line 745: assertTrue(search.getMatches().isEmpty());
Line 746: }
Line 747: Your test no longer throws a checked exception. Remove the throws clause
Line 748: from the test’s signature.
Line 749: Adding Tests from Your Test List
Line 750: In Test Smell: Irrelevant Details in a Test, on page 202, you added a couple of
Line 751: needed tests to your test list. Now that you’ve whittled down your messy initial
Line 752: test into two sleek, clear tests, you should find it relatively easy to add a
Line 753: couple of new tests.
Line 754: First, write a test that demonstrates how a completed search returns false for
Line 755: the errored() query:
Line 756: utj3-refactor-tests/11/src/test/java/util/ASearch.java
Line 757: @Test
Line 758: void erroredReturnsFalseWhenReadSucceeds() {
Line 759: var stream = streamOn("");
Line 760: var search = new Search(stream, "", "");
Line 761: search.execute();
Line 762: assertFalse(search.errored());
Line 763: }
Line 764: Then, test the case where accessing the input stream throws an exception:
Line 765: utj3-refactor-tests/11/src/test/java/util/ASearch.java
Line 766: @Test
Line 767: public void erroredReturnsTrueWhenUnableToReadStream() {
Line 768: var stream = createStreamThrowingErrorWhenRead();
Line 769: var search = new Search(stream, "", "");
Line 770: search.execute();
Line 771: assertTrue(search.errored());
Line 772: }
Line 773: private InputStream createStreamThrowingErrorWhenRead() {
Line 774: return new InputStream() {
Line 775: @Override
Line 776: public int read() throws IOException { throw new IOException(); }
Line 777: };
Line 778: }
Line 779: Time spent to add the new tests: less than a few minutes each.
Line 780: Chapter 10. Streamlining Your Tests • 206
Line 781: report erratum  •  discuss
Line 782: 
Line 783: --- 페이지 223 ---
Line 784: Summary
Line 785: You ended up with four sleek, refactored tests. A developer can understand
Line 786: the goal of each test through its name, which provides a generalized summary
Line 787: of behavior. They can see how that behavior plays out by reading the example
Line 788: within the test. Arrange—Act—Assert (AAA) guides them immediately to the
Line 789: act step so that they can see how the code being verified gets executed. They
Line 790: can reconcile the asserts against the test name’s description of behavior.
Line 791: Finally, if needed, they can review the arrange step to understand how it puts
Line 792: the system in the proper state to be tested.
Line 793: The tests are scannable. A developer can rapidly find and digest each test
Line 794: element (name, arrange, act, and assert) they’re interested in. The needed
Line 795: comprehension can happen in seconds rather than minutes. Remember also
Line 796: that readily understood tests—descriptions of unit behavior—can save even
Line 797: hours of time required to understand production code.
Line 798: Seeking to understand your system through its tests motivates
Line 799: you to keep them as clean as they should be.
Line 800: It only takes minutes to clean up tests enough to save extensive future
Line 801: amounts of comprehension time.
Line 802: You now have a complete picture of what you must do in the name of design:
Line 803: refactor your production code for clarity and conciseness, refactor your pro-
Line 804: duction code to support more flexibility in design, design your system to
Line 805: support mocking of dependency challenges, and refactor your tests to minimize
Line 806: maintenance and maximize understanding.
Line 807: You’re ready to move on to the final part of this book, a smorgasbord of
Line 808: additional topics related to unit testing.
Line 809: report erratum  •  discuss
Line 810: Summary • 207