Line 1: 
Line 2: --- 페이지 117 ---
Line 3: CHAPTER 5
Line 4: Examining Outcomes with Assertions
Line 5: You’ve learned the most important features of JUnit in the prior four chapters
Line 6: of this book, enough to survive but not thrive. Truly succeeding with your
Line 7: unit testing journey will involve gaining proficiency with your primary tool,
Line 8: JUnit. In this and the next couple of chapters, you’ll explore JUnit in signifi-
Line 9: cant detail. First, you’ll focus on JUnit’s means of verification—its assertion
Line 10: library.
Line 11: Assertions (or asserts) in JUnit are static method calls that you drop into
Line 12: your tests. Each assertion is an opportunity to verify that some condition
Line 13: holds true. If an asserted condition does not hold true, the test stops executing
Line 14: right there and JUnit reports a test failure.
Line 15: To abort the test, JUnit throws an exception object of type AssertionFailedError.
Line 16: If JUnit catches AssertionFailedError, it marks the test as failed. In fact, JUnit
Line 17: marks any test as failed that throws an exception not caught in the test body.
Line 18: In order to use the most appropriate assertion for your verification need, you’ll
Line 19: want to learn about JUnit’s numerous assertion variants.
Line 20: In examples to this point, you’ve used the two most prevalent assertion forms,
Line 21: assertTrue and assertEquals. Since you’ll use them for the bulk of your tests, you’ll
Line 22: first examine these assertion workhorses more deeply. You’ll then move on
Line 23: to exploring the numerous alternative assertion choices that JUnit provides.
Line 24: In some cases, the easiest way to assert something won’t be to compare to
Line 25: an actual result but to instead verify an operation by inverting it. You’ll see
Line 26: a brief example of how.
Line 27: You’ll also get an overview of AssertJ, a third-party assertion library that
Line 28: allows you to write “fluent” assertions. Such assertions can make your tests
Line 29: considerably easier to read. They can also provide more precise explanations
Line 30: about why a test is failing.
Line 31: report erratum  •  discuss
Line 32: 
Line 33: --- 페이지 118 ---
Line 34: Using the Core Assertion Forms
Line 35: The bulk of your assertions will use either assertTrue or assertEquals. Let’s review
Line 36: and refine your knowledge of these two assertion workhorses. Let’s also see
Line 37: how to keep your tests streamlined by eliminating things that don’t add value.
Line 38: The Most Basic Assertion Form: assertTrue
Line 39: The most basic assert form accepts a Boolean expression or reference as an
Line 40: argument and fails the test if that argument evaluates to false.
Line 41: org.junit.jupiter.api.Assertions.assertTrue(someBooleanExpression);
Line 42: Here’s an example demonstrating the use of assertTrue:
Line 43: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 44: @Test
Line 45: void hasPositiveBalanceAfterInitialDeposit() {
Line 46: var account = new Account("an account name");
Line 47: account.deposit(50);
Line 48: Assertions.assertTrue(account.hasPositiveBalance());
Line 49: }
Line 50: // ...
Line 51: Technically, you could use assertTrue for every assertion you had to write. But
Line 52: an assertTrue failure tells you only that the assertion failed and nothing more.
Line 53: Look for more precise assertions such as assertEquals, which reports what was
Line 54: expected vs. what was actually received when it fails. You’ll find test failures
Line 55: easier to understand and resolve as a result.
Line 56: Eliminating Clutter
Line 57: As documents that you’ll spend time reading and re-reading, you’ll want to
Line 58: streamline your tests. You learned in the first chapter (see Chapter 1, Building
Line 59: Your First JUnit Test, on page 3) that the public keyword is unnecessary when
Line 60: declaring both JUnit test classes and test methods. Such additional keywords
Line 61: and other unnecessary elements represent clutter.
Line 62: Streamline your tests by eliminating unnecessary clutter.
Line 63: You’ll be scanning lots of tests to gain a rapid understanding of what your
Line 64: system does and where your changes must go. Getting rid of clutter makes
Line 65: it easier to understand tests at a glance.
Line 66: Chapter 5. Examining Outcomes with Assertions • 100
Line 67: report erratum  •  discuss
Line 68: 
Line 69: --- 페이지 119 ---
Line 70: Asserts pervade JUnit tests. Rather than explicitly scope each assert call with
Line 71: the class name (Assertion), use a static import:
Line 72: import static org.junit.jupiter.api.Assertions.assertTrue;
Line 73: The result is a de-cluttered, more concise assertion statement:
Line 74: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 75: @Test
Line 76: void hasPositiveBalanceAfterInitialDeposit() {
Line 77: var account = new Account("an account name");
Line 78: account.deposit(50);
Line 79: assertTrue(account.hasPositiveBalance());
Line 80: ➤
Line 81: }
Line 82: Generalized Assertions
Line 83: Here’s another example of assertTrue which explains how a result relates to
Line 84: some expected outcome:
Line 85: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 86: @Test
Line 87: void depositIncreasesBalance() {
Line 88: var account = new Account("an account name");
Line 89: var initialBalance = account.getBalance();
Line 90: account.deposit(100);
Line 91: assertTrue(account.getBalance() > initialBalance);
Line 92: }
Line 93: A test name—depositIncreasesBalance—is a general statement about the behavior
Line 94: you want the test to demonstrate. Its assertion—assertTrue(balance > initialBalance)—
Line 95: corresponds to the test name, ensuring that the balance has increased as an
Line 96: outcome of the deposit operation. The test does not explicitly verify by how
Line 97: much the balance increased. As a result, you might describe its assert
Line 98: statement as a generalized assertion.
Line 99: Eliminating More Clutter
Line 100: The preceding examples depend on the existence of an initialized Account
Line 101: instance. You can create an Account in a @BeforeEach method (see Initializing
Line 102: with @BeforeEach and @BeforeAll, on page 124 for more information) and store
Line 103: a reference to it as a field on the test class:
Line 104: utj3-junit/02/src/test/java/scratch/AnAccount.java
Line 105: class AnAccount {
Line 106: Account account;
Line 107: report erratum  •  discuss
Line 108: Using the Core Assertion Forms • 101
Line 109: 
Line 110: --- 페이지 120 ---
Line 111: @BeforeEach
Line 112: void createAccount() {
Line 113: account = new Account("an account name");
Line 114: }
Line 115: @Test
Line 116: void hasPositiveBalanceAfterInitialDeposit() {
Line 117: account.deposit(50);
Line 118: assertTrue(account.hasPositiveBalance());
Line 119: }
Line 120: // ...
Line 121: }
Line 122: JUnit creates a new instance of the test class for each test (see Observing
Line 123: the JUnit Lifecycle, on page 127 for further explanation). That means you
Line 124: can also safely initialize fields at their point of declaration:
Line 125: utj3-junit/03/src/test/java/scratch/AnAccount.java
Line 126: class AnAccount {
Line 127: Account account = new Account("an account name");
Line 128: @Test
Line 129: void hasPositiveBalanceAfterInitialDeposit() {
Line 130: // ...
Line 131: }
Line 132: // ...
Line 133: }
Line 134: Use assertEquals for Explicit Comparisons
Line 135: Your test names should be generalizations of behavior, but each test should
Line 136: present a specific example with a specific result. If the test makes a deposit,
Line 137: you know what the new balance amount should be. In most cases, you should
Line 138: be explicit with your assertion and verify the actual new balance.
Line 139: The assertion assertEquals compares an expected answer to the actual answer,
Line 140: allowing you to explicitly verify an outcome’s value. It’s overloaded so that
Line 141: you can appropriately compare all primitive types, wrapper types, and object
Line 142: references. (To compare two arrays, use assertArrayEquals instead.) Most of your
Line 143: assertions should probably be assertEquals.
Line 144: Here’s the deposit example again, asserting by how much the balance
Line 145: increased:
Line 146: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 147: @Test
Line 148: void depositIncreasesBalanceByAmountDeposited() {
Line 149: account.deposit(50);
Line 150: Chapter 5. Examining Outcomes with Assertions • 102
Line 151: report erratum  •  discuss
Line 152: 
Line 153: --- 페이지 121 ---
Line 154: account.deposit(100);
Line 155: assertEquals(150, account.getBalance());
Line 156: }
Line 157: You design the example for each test, and you know the expected outcome.
Line 158: Encode it in the test with assertEquals.
Line 159: Assertion Messages: Redundant Messages for Assertions
Line 160: Most verifications are self-explanatory, at least in terms of the code bits they’re
Line 161: trying to verify. Sometimes, it’s helpful to have a bit of “why” or additional context
Line 162: to explain an assertion. “Just why does this test expect the total to be 42?”
Line 163: Most JUnit assert forms support an optional final argument named message.
Line 164: The message argument allows you to supply a nice verbose explanation of the
Line 165: rationale behind the assertion:
Line 166: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 167: @Test
Line 168: void balanceRepresentsTotalOfDeposits() {
Line 169: account.deposit(50);
Line 170: account.deposit(51);
Line 171: var balance = account.getBalance();
Line 172: assertEquals(101, balance, "account balance must be total of deposits");
Line 173: }
Line 174: The assertion message displays when the test fails:
Line 175: account balance must be total of deposits ==> expected: <101> but was: <102>
Line 176: If you prefer lots of explanatory comments, you might get some mileage out
Line 177: of assertion messages. However, this is the better route:
Line 178: • Test only one behavior at a time
Line 179: • Make your test names more descriptive
Line 180: In fact, if you demonstrate only one behavior per test, you’ll usually only need
Line 181: a single assertion. The name of the test will then naturally describe the reason
Line 182: for that one assertion. No assertion failure message is needed.
Line 183: Well-written tests document themselves.
Line 184: Elements like explanatory constants, helper methods, and intention-revealing
Line 185: variable names go a long way toward making tests accessible and to the point.
Line 186: The existence of comments and assertion messages in unit tests is a smell
Line 187: report erratum  •  discuss
Line 188: Assertion Messages: Redundant Messages for Assertions • 103
Line 189: 
Line 190: --- 페이지 122 ---
Line 191: that usually indicates stinky test design. In Chapter 10, Streamlining Your
Line 192: Tests, on page 189, you’ll step through an example of test clean-up.
Line 193: In well-written tests, the assertion message becomes redundant clutter, just
Line 194: one more thing to have to wade through and maintain.
Line 195: Improved test failure messages can provide a small benefit since figuring out
Line 196: the meaning or implication of an assertion failure can be frustrating. Rather
Line 197: than use assertion failure messages, however, take a look at AssertJ, which
Line 198: provides fluent assertions that generate more detailed failure messages.
Line 199: 1
Line 200: Assertion messages can also provide value when you employ parameterized
Line 201: tests, which are a JUnit mechanism for running the same test with a bunch
Line 202: of different data. See Executing Multiple Data Cases with Parameterized Tests,
Line 203: on page 131.
Line 204: Other Common JUnit Assertion Forms
Line 205: While assertEquals and assertTrue would cover almost all the assertions you’ll
Line 206: need to write, you’ll want to learn about the other forms that JUnit supports.
Line 207: Choosing the best assertion for the job will keep your tests concise and clear.
Line 208: In this section, you’ll be introduced to the majority of JUnit’s other assertion
Line 209: forms, including assertFalse, assertNotEquals, assertSame, assertNotSame, assertNull, and
Line 210: assertNotNull. You’ll also get an experience-based opinion on the value and best
Line 211: uses for each variant.
Line 212: assertFalse
Line 213: Nobody doesn’t dislike double negatives (or triple negatives, so says my editor).
Line 214: To help you say things “straight up” in your tests, JUnit provides some inverse
Line 215: assertions. Here’s assertFalse—the opposite of assertTrue—in action:
Line 216: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 217: @Test
Line 218: void doesNotHavePositiveBalanceWhenAccountCreated() {
Line 219: assertFalse(account.hasPositiveBalance());
Line 220: }
Line 221: You can code the equivalent by using assertTrue if you’re in a contrary mood:
Line 222: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 223: @Test
Line 224: void doesNotHavePositiveBalanceWhenAccountCreated() {
Line 225: assertTrue(!account.hasPositiveBalance());
Line 226: }
Line 227: 1.
Line 228: https://assertj.github.io/doc/
Line 229: Chapter 5. Examining Outcomes with Assertions • 104
Line 230: report erratum  •  discuss
Line 231: 
Line 232: --- 페이지 123 ---
Line 233: Paraphrased, it reads awkwardly: “assert true…not account has positive balance”
Line 234: and represents the kind of logic that trips many of us up. Keep the double
Line 235: negatives out of your tests. Use assertFalse when it’s easier to read than assertTrue.
Line 236: assertNotEquals
Line 237: Appropriate use of assertNotEquals is much rarer. If you know what the answer
Line 238: should be, use assertEquals to say that. Use of assertNotEquals otherwise may
Line 239: represent making what you might call a weak assertion—one that doesn’t
Line 240: fully verify a result.
Line 241: Some sensible cases for using assertNotEquals:
Line 242: • You really don’t have a way of knowing what the answer should be.
Line 243: • You’ve explained (in another test, perhaps) what an actual answer might
Line 244: be, and with this test, you want to emphasize that it can’t possibly be
Line 245: some other specified value.
Line 246: • It would require too much data detail to explicitly assert against the
Line 247: actual result.
Line 248: Let’s try an example. For any card game (for example, poker), you must
Line 249: shuffle the deck of playing cards prior to dealing any cards from it. Here’s a
Line 250: starter implementation of a Deck class, showing that shuffling occurs in its
Line 251: constructor:
Line 252: utj3-junit/01/src/main/java/cards/Deck.java
Line 253: public class Deck {
Line 254: private LinkedList<Card> cards;
Line 255: public Deck() {
Line 256: cards = newDeck();
Line 257: Collections.shuffle(cards);
Line 258: ➤
Line 259: }
Line 260: static LinkedList<Card> newDeck() {
Line 261: var cards = new LinkedList<Card>();
Line 262: for (var i = 1; i <= 13; i++) {
Line 263: cards.add(new Card(i, "C"));
Line 264: cards.add(new Card(i, "D"));
Line 265: cards.add(new Card(i, "H"));
Line 266: cards.add(new Card(i, "S"));
Line 267: }
Line 268: return cards;
Line 269: }
Line 270: public Card deal() {
Line 271: return cards.removeFirst();
Line 272: }
Line 273: report erratum  •  discuss
Line 274: Other Common JUnit Assertion Forms • 105
Line 275: 
Line 276: --- 페이지 124 ---
Line 277: List<Card> remaining() {
Line 278: return cards;
Line 279: }
Line 280: }
Line 281: You want to verify that the shuffling did actually occur:
Line 282: utj3-junit/01/src/test/java/cards/ADeck.java
Line 283: public class ADeck {
Line 284: Deck deck = new Deck();
Line 285: // ... other Deck tests here ...
Line 286: @Test
Line 287: void hasBeenShuffled() {
Line 288: var cards = deck.remaining();
Line 289: assertNotEquals(Deck.newDeck(), cards);
Line 290: }
Line 291: }
Line 292: You might be thinking, “Hey, that looks like a weak assertion!” It is, in a way—
Line 293: you do not know whether or not the deck has been properly shuffled. But
Line 294: that’s not the job of the Deck class. The Deck class here invokes a shuffle rather
Line 295: than implementing it, using a method from the Java API. You can trust that
Line 296: Collections.shuffle() randomizes the order of a collection appropriately, though
Line 297: you might need a better random shuffler if you’re a casino.
Line 298: Since you can trust the Java API, you don’t need to prove the quality of its shuf-
Line 299: fle. But your unit test does need to verify that the cards were actually shuffled.
Line 300: You can do this in a number of somewhat complex ways, such as by using test
Line 301: doubles (see Chapter 3, Using Test Doubles, on page 53) or injecting a seeded
Line 302: random number generator to use for shuffling.
Line 303: Ensuring that the order of cards in an instantiated Deck is not equal to the
Line 304: cards returned by Deck.newDeck() is sufficient and simple. It demonstrates that
Line 305: some operation occurred to change the order. (Note that this weak assertion
Line 306: also has a slim possibility of failing in the one case where it shuffles to the
Line 307: deck’s starting order. Highly unlikely in your lifetime. Run the test again if
Line 308: you chance upon that serendipitous moment.)
Line 309: Yes, someone could replace the call to Collections.shuffle() with shoddy shuffle
Line 310: code—for example, something that moved one card from the front to the back
Line 311: of the deck. But don’t worry—no one would do that.
Line 312: Unit tests don’t exist to protect you from willful destructiveness. A determined
Line 313: saboteur can break your system without breaking any tests.
Line 314: Chapter 5. Examining Outcomes with Assertions • 106
Line 315: report erratum  •  discuss
Line 316: 
Line 317: --- 페이지 125 ---
Line 318: Avoid weak assertions like assertNotEquals unless you have no choice
Line 319: or they emphasize what you really want your test to say.
Line 320: assertSame
Line 321: Also infrequently used, assertSame verifies that two references point to the same
Line 322: object in memory.
Line 323: Your challenge: minimize the use of memory in a scheduling application where
Line 324: there might need to be many millions of Time objects. (This example is based
Line 325: on “Working with Design Patterns: Flyweight.”)
Line 326: 2 Most of these Times will be on
Line 327: the quarter hour (11:15, 14:30, 10:15) because that’s how we usually like to
Line 328: schedule things. Some small subset will be at odd times, like 3:10 or 4:20,
Line 329: because some people do odd things at odd times, dude.
Line 330: The idea of the flyweight pattern is to have a single object pool, which allows
Line 331: for multiple interested parties to share objects that have the same values.
Line 332: (This works great for immutable objects, not so great otherwise.) Your appli-
Line 333: cation can reduce its memory footprint significantly as a result.
Line 334: Here are the two production classes involved:
Line 335: utj3-junit/01/src/main/java/time/Time.java
Line 336: import static java.lang.String.format;
Line 337: public record Time(byte hour, byte minute) {
Line 338: static String key(byte hour, byte minute) {
Line 339: return format("%d:%d", hour, minute);
Line 340: }
Line 341: @Override
Line 342: public String toString() {
Line 343: return key(hour, minute);
Line 344: }
Line 345: }
Line 346: utj3-junit/01/src/main/java/time/TimePool.java
Line 347: import java.util.HashMap;
Line 348: import java.util.Map;
Line 349: public class TimePool {
Line 350: private static Map<String, Time> times = new HashMap<>();
Line 351: static void reset() {
Line 352: times.clear();
Line 353: }
Line 354: 2.
Line 355: https://www.developer.com/design/working-with-design-patterns-flyweight/
Line 356: report erratum  •  discuss
Line 357: Other Common JUnit Assertion Forms • 107
Line 358: 
Line 359: --- 페이지 126 ---
Line 360: public static Time get(byte hour, byte minute) {
Line 361: return times.computeIfAbsent(Time.key(hour, minute),
Line 362: k -> new Time(hour, minute));
Line 363: }
Line 364: }
Line 365: Here are a couple of tests:
Line 366: utj3-junit/01/src/test/java/time/ATimePool.java
Line 367: public class ATimePool {
Line 368: @BeforeEach
Line 369: void resetPool() {
Line 370: TimePool.reset();
Line 371: }
Line 372: @Test
Line 373: void getReturnsTimeInstance() {
Line 374: byte four = 4;
Line 375: byte twenty = 20;
Line 376: assertEquals(new Time(four, twenty), TimePool.get(four, twenty));
Line 377: }
Line 378: @Test
Line 379: void getWithSameValuesReturnsSharedInstance() {
Line 380: byte ten = 10;
Line 381: byte five = 5;
Line 382: var firstRetrieved = TimePool.get(ten, five);
Line 383: var secondRetrieved = TimePool.get(ten, five);
Line 384: assertSame(firstRetrieved, secondRetrieved);
Line 385: ➤
Line 386: }
Line 387: }
Line 388: The highlighted line in the second test demonstrates the use of assertSame. The
Line 389: arrange step calls the get method on the TimePool to retrieve a first Time object,
Line 390: then makes the same call a second time in the act step. The assert step verifies
Line 391: that the two Time objects are one and the same.
Line 392: assertNotSame
Line 393: assertNotSame verifies that two references point to different objects in memory.
Line 394: You might use assertNotSame to verify that an object “persisted” in memory—in
Line 395: a hash map, for example—is a different instance than the one stored. Other-
Line 396: wise, changes to the “live” object would also alter the persisted object. Here’s
Line 397: some code to demonstrate:
Line 398: utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
Line 399: package persistence;
Line 400: import org.junit.jupiter.api.Test;
Line 401: Chapter 5. Examining Outcomes with Assertions • 108
Line 402: report erratum  •  discuss
Line 403: 
Line 404: --- 페이지 127 ---
Line 405: import static org.junit.jupiter.api.Assertions.*;
Line 406: class AnInMemoryDatabase {
Line 407: @Test
Line 408: void objectCopiedWhenAddedToDatabase() {
Line 409: var db = new InMemoryDatabase();
Line 410: var customer = new Customer("1", "Smelt, Inc.");
Line 411: db.add(customer);
Line 412: var retrieved = db.data.get("1");
Line 413: assertNotSame(retrieved, customer);
Line 414: }
Line 415: }
Line 416: The test creates an InMemoryDatabase and adds a customer via the database’s
Line 417: add method.
Line 418: utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
Line 419: import java.util.HashMap;
Line 420: import java.util.Map;
Line 421: public class InMemoryDatabase {
Line 422: Map<String, Customer> data = new HashMap<>();
Line 423: public void add(Customer customer) {
Line 424: data.put(customer.id(), new Customer(customer));
Line 425: ➤
Line 426: }
Line 427: }
Line 428: In the add method in the production code, the highlighted line shows the use
Line 429: of a copy constructor on the Customer record to ensure that a new instance is
Line 430: added to the HashMap named data.
Line 431: Without making that copy—with this line instead as the implementation for
Line 432: the add method:
Line 433: utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
Line 434: data.put(customer.id(), customer);
Line 435: …the test fails.
Line 436: One way to think about unit tests is they add protections—and corresponding
Line 437: explanations—for the little things that are important but not necessarily
Line 438: obvious, like the need for creating a copy in this example.
Line 439: Unit tests not only safeguard but also describe the thousands of
Line 440: choices in your system.
Line 441: report erratum  •  discuss
Line 442: Other Common JUnit Assertion Forms • 109
Line 443: 
Line 444: --- 페이지 128 ---
Line 445: assertNull
Line 446: assertNull is equivalent to doing assertEquals(null, someValue).
Line 447: The InMemoryDatabase class needs a public way for clients to retrieve customers
Line 448: by their id. Here’s an implementation of a get method:
Line 449: utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
Line 450: public class InMemoryDatabase {
Line 451: Map<String, Customer> data = new HashMap<>();
Line 452: // ...
Line 453: public Customer get(String id) {
Line 454: return data.getOrDefault(id, null);
Line 455: }
Line 456: }
Line 457: How many tests do you need to cover that method? The word “Or” in getOrDefault
Line 458: is a solid hint that you’ll want at least two. In this listing, the first test is the
Line 459: “happy path” case where a Customer is successfully retrieved:
Line 460: utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
Line 461: InMemoryDatabase db = new InMemoryDatabase();
Line 462: @Test
Line 463: void returnsCustomerCorrespondingToId() {
Line 464: var customer = new Customer("42", "Mr Creosote");
Line 465: db.add(customer);
Line 466: var retrieved = db.get("42");
Line 467: assertEquals(customer, retrieved);
Line 468: }
Line 469: @Test
Line 470: void returnsNotNullForNonexistentKey() {
Line 471: assertNull(db.get("42"));
Line 472: ➤
Line 473: }
Line 474: The second test demonstrates the use of assertNull: if you attempt to retrieve
Line 475: anything (42 in this case) from a newly created db (into which nothing has
Line 476: been inserted), it should return null.
Line 477: assertNotNull
Line 478: assertNotNull is the opposite of assertNull, naturally. It’s used to assert that a ref-
Line 479: erence points to something, not nothing.
Line 480: Like assertNotEquals, many uses of assertNotNull are dubious.
Line 481: Some folks new to JUnit introduce assertNotNull checks for references to newly
Line 482: instantiated objects:
Line 483: Chapter 5. Examining Outcomes with Assertions • 110
Line 484: report erratum  •  discuss
Line 485: 
Line 486: --- 페이지 129 ---
Line 487: utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
Line 488: @Test
Line 489: void returnsCustomerCorrespondingToId() {
Line 490: var customer = new Customer("42", "Mr Creosote");
Line 491: assertNotNull(customer); // bogus! this can't fail
Line 492: ➤
Line 493: db.add(customer);
Line 494: var retrieved = db.get("42");
Line 495: assertEquals(customer, retrieved);
Line 496: }
Line 497: However, that assertNotNull can never fail. The only way that the customer variable,
Line 498: initialized in the first line of the test, can ever end up null is if the Customer
Line 499: constructor throws an exception. If an exception is thrown, the next line of
Line 500: code—the assertNotNull statement—is never executed. If no exception is thrown,
Line 501: the customer reference will point to a (non-null) object, so the assertNotNull will
Line 502: never fail if it does get executed. Don’t do that.
Line 503: assertNotNull is only useful when you need to demonstrate that a reference
Line 504: points to a value and you don’t care at all what that value is. Otherwise—if
Line 505: you can determine the expected value—assertNotNull is a weak assertion. You’d
Line 506: be better off using assertEquals to compare the reference to its actual value.
Line 507: You’ll know when, on rare occasions, you should reach for assertNotNull. Other-
Line 508: wise…don’t do that.
Line 509: An Added Assortment of Asserts
Line 510: But wait—there’s more!
Line 511: The org.junit.jupiter.api.Assertions class in JUnit provides a few more assertions
Line 512: that are not described here. Without perusing the users’s guide or the volu-
Line 513: minous Javadoc for the class, you wouldn’t know these assertions existed.
Line 514: Here they are with brief descriptions of what they do.
Line 515: asserts that two lists or streams of strings match; can involve
Line 516: regular expressions and "fast forwarding"
Line 517: assertLinesMatch
Line 518: asserts that all supplied executables do not throw exception
Line 519: assertAll
Line 520: asserts that the actual value is an instance of the expected type
Line 521: assertInstanceOf
Line 522: asserts that the provided Iterable references are deeply equal
Line 523: assertIterableEquals
Line 524: asserts that an executable completes execution within a speci-
Line 525: fied duration
Line 526: assertTimeout
Line 527: like assertTimeout, but runs the executable in a separate thread
Line 528: assertTimeout
Line 529: Preemptively
Line 530: report erratum  •  discuss
Line 531: Other Common JUnit Assertion Forms • 111
Line 532: 
Line 533: --- 페이지 130 ---
Line 534: Expecting Exceptions
Line 535: In addition to ensuring that the happy path through your code works, you
Line 536: also need to verify the unhappy cases. For example, you’ll want to write tests
Line 537: that demonstrate when code can throw exceptions. These tests are necessary
Line 538: to provide a full understanding of the behaviors to developers who must work
Line 539: with the code.
Line 540: The ever-evolving Java language has driven the continual development of
Line 541: JUnit as well—there are no fewer than four ways to write exception-based
Line 542: tests in JUnit. You’ll take a look at a couple of these.
Line 543: Let’s examine a simple case: ensure the Account code throws an InsufficientFunds-
Line 544: Exception when a client attempts to withdraw more than the available balance.
Line 545: Newer School: assertThrows
Line 546: The assertThrows assertion, available in JUnit since version 4.13, should cover
Line 547: all your needs when writing exception-based tests. Prefer it over the other
Line 548: mechanisms.
Line 549: The most useful assertThrows form takes two arguments: the type of the exception
Line 550: expected to be thrown and an executable object (usually a lambda, but
Line 551: potentially a method reference). The executable contains the code expected
Line 552: to throw the exception.
Line 553: When the assertion gets executed by JUnit, the code in the lambda is run. If
Line 554: that code throws no exception, the assertion fails. If the code in the lambda
Line 555: does throw an exception, the test passes if the type of the exception object
Line 556: matches or is a subclass of the expected exception type.
Line 557: Here’s assertThrows in action. The lambda argument to assertThrows attempts to
Line 558: withdraw 100 from a newly created account (that is, one with no money):
Line 559: utj3-junit/01/src/test/java/scratch/AnAccount.java
Line 560: import static org.junit.jupiter.api.Assertions.assertThrows;
Line 561: // ...
Line 562: @Test
Line 563: void throwsWhenWithdrawingTooMuch() {
Line 564: var thrown = assertThrows(InsufficientFundsException.class,
Line 565: () -> account.withdraw(100));
Line 566: assertEquals("balance only 0", thrown.getMessage());
Line 567: }
Line 568: Calling assertThrows returns the exception object. This test assigns it to the
Line 569: thrown variable to allow asserting against its message string.
Line 570: Chapter 5. Examining Outcomes with Assertions • 112
Line 571: report erratum  •  discuss
Line 572: 
Line 573: --- 페이지 131 ---
Line 574: Don’t add extraneous code to the lambda. You don’t want a false positive
Line 575: where the test passes because the wrong line of code threw the expected
Line 576: exception.
Line 577: Code in withdraw passes the assertThrows statement by throwing an InsufficientFunds-
Line 578: Exception when the amount to withdraw exceeds the balance:
Line 579: utj3-junit/01/src/main/java/scratch/Account.java
Line 580: void withdraw(int dollars) {
Line 581: if (balance < dollars) {
Line 582: throw new InsufficientFundsException("balance only " + balance);
Line 583: }
Line 584: balance -= dollars;
Line 585: }
Line 586: Old School
Line 587: Prior to the availability of assertThrows, you had at least three options in JUnit
Line 588: for expecting exceptions: Using try/catch, annotations, and rules. You may see
Line 589: some of these solutions if you maintain older systems. Annotations and rules
Line 590: aren’t supported by JUnit 5, so I won’t cover them here. I’ll show you what
Line 591: they look like, though, so you can understand what you’re seeing.
Line 592: Here’s an example of the annotations-based mechanism:
Line 593: @Test(expected=InsufficientFundsException.class)
Line 594: public void throwsWhenWithdrawingTooMuch() {
Line 595: account.withdraw(100);
Line 596: }
Line 597: If you see expected= as an argument to the @Test annotation, visit the JUnit 4
Line 598: documentation on @Test for further explanation.
Line 599: 3
Line 600: Here’s what the use of the rules-based mechanism (added in JUnit 4.7) might
Line 601: look like:
Line 602: public class SimpleExpectedExceptionTest {
Line 603: @Rule
Line 604: public ExpectedException thrown= ExpectedException.none();
Line 605: @Test
Line 606: public void throwsException() {
Line 607: thrown.expect(NullPointerException.class);
Line 608: thrown.expectMessage("happened");
Line 609: // ... code that throws the exception
Line 610: }
Line 611: // ...
Line 612: 3.
Line 613: https://junit.org/junit4/javadoc/4.12/org/junit/Test.html
Line 614: report erratum  •  discuss
Line 615: Expecting Exceptions • 113
Line 616: 
Line 617: --- 페이지 132 ---
Line 618: If you see an ExpectedException instantiated and annotated with @Rule, visit JUnit
Line 619: 4’s documentation for ExpectedException for further explanation.
Line 620: 4
Line 621: If it’s not obvious, “old school” is pejorative. (I’m allowed to say it, though,
Line 622: ‘cause I’m old.) Don’t use these old constructs if you can help it.
Line 623: Use of try/catch
Line 624: JUnit’s first releases supported only “roll-your-own” mechanisms for exception
Line 625: handling, based on the use of Java’s try/catch construct. Here’s the comparable
Line 626: Account code for expecting an InsufficientFundsException:
Line 627: @Test
Line 628: void throwsWhenWithdrawingTooMuch() {
Line 629: try {
Line 630: account.withdraw(100);
Line 631: ➤
Line 632: fail();
Line 633: } catch (InsufficientFundsException expected) {
Line 634: assertEquals("balance only 0", expected.getMessage());
Line 635: }
Line 636: }
Line 637: When JUnit executes code within a try block that does throw an exception,
Line 638: control is transferred to the appropriate catch block and executed. In the
Line 639: example, since the code indeed throws an InsufficientFundsException, control
Line 640: transfers to the assertEquals statement in the catch block, which verifies the
Line 641: exception object’s message contents.
Line 642: You can deliberately fail the test by commenting out the withdrawal operation
Line 643: in Account’s withdraw method. Do that to see firsthand what JUnit tells you.
Line 644: If the call to withdraw does not throw an exception, the next line executes. When
Line 645: using the try/catch mechanism, the last line in the try block should be a call to
Line 646: org.junit.Assert.fail(). As you might guess, JUnit’s fail method throws an Assertion-
Line 647: FailedError so as to abort and fail the test.
Line 648: The try/catch idiom represents the rare case where it might be okay to have
Line 649: an empty catch block—perhaps you don’t care about the contents of the
Line 650: exception. Naming the exception variable expected helps reinforce to the reader
Line 651: that we expect an exception to be thrown and caught.
Line 652: Think about other things that you might want a test to assert after an
Line 653: exception has been thrown. Examine any important post-conditions that
Line 654: must hold true. For example, it might be of value to assert that the account
Line 655: balance didn’t change after the failed withdrawal attempt.
Line 656: 4.
Line 657: https://junit.org/junit4/javadoc/4.12/org/junit/rules/ExpectedException.html
Line 658: Chapter 5. Examining Outcomes with Assertions • 114
Line 659: report erratum  •  discuss
Line 660: 
Line 661: --- 페이지 133 ---
Line 662: You might occasionally see the try/catch mechanism used in older code. If so, you
Line 663: can leave it alone (you now know how it works), or you can streamline your test
Line 664: by replacing it with assertThrows.
Line 665: Assert That Nothing Happened: assertDoesNotThrow
Line 666: As with a lot of other assertion forms, JUnit provides a converse to assertThrows—
Line 667: specifically, the ‘assertDoesNotThrow‘ method. In its simplest form, it takes an
Line 668: executable object (a lambda or method reference). If the invocation of code in
Line 669: the executable doesn’t throw anything, the assertion passes; otherwise, it fails.
Line 670: Every once in a while, you’ll think you might want to use assertDoesNotThrow…the
Line 671: only problem is, it really doesn’t assert anything about what the executed
Line 672: code does do. Try finding a way to test that elusive “something.”
Line 673: You might find assertDoesNotThrow useful as the catch-all in a series of tests.
Line 674: Suppose you have a validator that throws an exception in a couple of cases
Line 675: and otherwise does nothing:
Line 676: utj3-junit/01/src/test/java/scratch/ANameValidator.java
Line 677: class NameValidationException extends RuntimeException {}
Line 678: class NameValidator {
Line 679: long commaCount(String s) {
Line 680: return s.chars().filter(ch -> ch == ',').count();
Line 681: }
Line 682: void validate(String name) {
Line 683: if (name.isEmpty() ||
Line 684: commaCount(name) > 1)
Line 685: throw new NameValidationException();
Line 686: }
Line 687: }
Line 688: You need two tests to demonstrate that validate throws an exception for each
Line 689: of the two negative cases:
Line 690: utj3-junit/01/src/test/java/scratch/ANameValidator.java
Line 691: import org.junit.jupiter.api.Test;
Line 692: import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
Line 693: import static org.junit.jupiter.api.Assertions.assertThrows;
Line 694: class ANameValidator {
Line 695: NameValidator validator = new NameValidator();
Line 696: @Test
Line 697: void throwsWhenNameIsEmpty() {
Line 698: assertThrows(NameValidationException.class, () ->
Line 699: validator.validate(""));
Line 700: }
Line 701: report erratum  •  discuss
Line 702: Assert That Nothing Happened: assertDoesNotThrow • 115
Line 703: 
Line 704: --- 페이지 134 ---
Line 705: @Test
Line 706: void throwsWhenNameContainsMultipleCommas() {
Line 707: assertThrows(NameValidationException.class, () ->
Line 708: validator.validate("Langr, Jeffrey,J."));
Line 709: }
Line 710: }
Line 711: …and one test with assertDoesNotThrow to show nothing happens otherwise:
Line 712: utj3-junit/01/src/test/java/scratch/ANameValidator.java
Line 713: @Test
Line 714: void doesNotThrowWhenNoErrorsExist() {
Line 715: assertDoesNotThrow(() ->
Line 716: validator.validate("Langr, Jeffrey J."));
Line 717: }
Line 718: Use assertDoesNotThrow if you must, but maybe explore a different design first.
Line 719: For the example here, changing the validator to expose a Boolean method
Line 720: would do the trick.
Line 721: Exceptions Schmexceptions, Who Needs ‘em?
Line 722: Most tests you write will be more carefree, happy path tests where exceptions
Line 723: are highly unlikely to be thrown. But Java acts as a bit of a buzzkill, insisting
Line 724: that you acknowledge any checked exception types.
Line 725: Don’t clutter your tests with try/catch blocks to deal with checked exceptions.
Line 726: Instead, let those exceptions loose! The test can just throw them:
Line 727: utj3-junit/01/src/test/java/scratch/SomeAssertExamples.java
Line 728: @Test
Line 729: void readsFromTestFile() throws IOException {
Line 730: ➤
Line 731: var writer = new BufferedWriter(new FileWriter("test.txt"));
Line 732: writer.write("test data");
Line 733: writer.close();
Line 734: // ...
Line 735: }
Line 736: You’re designing these positive tests so you know they won’t throw an
Line 737: exception except under truly exceptional conditions. Even if an exception does
Line 738: get thrown unexpectedly, JUnit will trap it for you and report the test as an
Line 739: error instead of a failure.
Line 740: Alternate Assertion Approaches
Line 741: Most of the assertions in your tests will be straight-up comparisons of
Line 742: expected outcomes to actual outcomes: is the average credit history 780?
Line 743: Sometimes, however, direct comparisons aren’t the most effective way to
Line 744: describe the expected outcome.
Line 745: Chapter 5. Examining Outcomes with Assertions • 116
Line 746: report erratum  •  discuss
Line 747: 
Line 748: --- 페이지 135 ---
Line 749: For example, suppose you’ve coded the method fastHalf that uses bit shifting
Line 750: to perform integer division by two. The code is trivial, as are some core tests:
Line 751: utj3-junit/01/src/main/java/util/MathUtils.java
Line 752: public class MathUtils {
Line 753: static long fastHalf(long number) {
Line 754: return number >> 1;
Line 755: }
Line 756: }
Line 757: utj3-junit/01/src/test/java/util/SomeMathUtils.java
Line 758: import org.junit.jupiter.api.Test;
Line 759: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 760: import static util.MathUtils.fastHalf;
Line 761: public class SomeMathUtils {
Line 762: @Nested
Line 763: class FastHalf {
Line 764: @Test
Line 765: void isZeroWhenZero() {
Line 766: assertEquals(0, fastHalf(0));
Line 767: }
Line 768: @Test
Line 769: void roundsDownToZeroWhenOne() {
Line 770: assertEquals(0, fastHalf(1));
Line 771: }
Line 772: @Test
Line 773: void dividesEvenlyWhenEven() {
Line 774: assertEquals(11, fastHalf(22));
Line 775: }
Line 776: @Test
Line 777: void roundsDownWhenOdd() {
Line 778: assertEquals(10, fastHalf(21));
Line 779: }
Line 780: @Test
Line 781: void handlesNegativeNumbers() {
Line 782: assertEquals(-2, fastHalf(-4));
Line 783: }
Line 784: You might want another test to verify the utility works with very large numbers:
Line 785: utj3-junit/01/src/test/java/util/SomeMathUtils.java
Line 786: @Test
Line 787: void handlesLargeNumbers() {
Line 788: var number = 489_935_889_934_389_890L;
Line 789: assertEquals(244_967_944_967_194_945L, fastHalf(number));
Line 790: }
Line 791: But, oh, that’s ugly, and it’s hard for a test reader to quickly verify.
Line 792: report erratum  •  discuss
Line 793: Alternate Assertion Approaches • 117
Line 794: 
Line 795: --- 페이지 136 ---
Line 796: You’ve demonstrated that fast half works for 0, 1, many, and negative number
Line 797: cases. For very large numbers, rather than show many-digit barfages in the
Line 798: test, you can write an assertion that emphasizes the inverse mathematical
Line 799: relationship between input and output:
Line 800: utj3-junit/01/src/test/java/util/SomeMathUtils.java
Line 801: @Test
Line 802: void handlesLargeNumbers() {
Line 803: var number = 489_935_889_934_389_890L;
Line 804: assertEquals(number, fastHalf(number) * 2);
Line 805: }
Line 806: Mathematical computations represent the canonical examples for verifying
Line 807: via inverse relationships: you can verify division by using multiplication,
Line 808: addition by using subtraction, square roots by squares, and so on. Other
Line 809: domains where you can verify using inverse operations include cryptography,
Line 810: accounting, physics, computer graphics, finance, and data compression.
Line 811: Cross-checking via inversion ensures that everything adds up and balances,
Line 812: much like the general ledger in a double-entry bookkeeping system. It’s not
Line 813: a technique you should reach for often, but it can occasionally help make
Line 814: your tests considerably more expressive. You might find particular value in
Line 815: inversion when your test demands voluminous amounts of data.
Line 816: Be careful with the code you use for verification! If both the actual routine
Line 817: and the assertion share the same code (perhaps a common utility class you
Line 818: wrote), they could share a common defect.
Line 819: Third-Party Assertion Libraries
Line 820: JUnit provides all the assertions you’ll need, but it’s worth taking a look at
Line 821: the third-party assertion libraries available—AssertJ, Hamcrest, Truth, and
Line 822: more. These libraries primarily seek to improve upon the expressiveness of
Line 823: assertions, which can help streamline and simplify your tests.
Line 824: Let’s take a very quick look at AssertJ, a popular choice, to see a little bit of
Line 825: its power. AssertJ offers fluent assertions, which are designed to help tests
Line 826: flow better and read more naturally. A half-dozen simple examples should
Line 827: get the idea across quickly. Each of the examples assumes the following
Line 828: declaration:
Line 829: String name = "my big fat acct";
Line 830: The core AssertJ form reverses JUnit order. You specify the actual value first
Line 831: as an argument to an assertThat method that all assertions use. You then make
Line 832: a chained call to one of many methods that complete or continue the assertion.
Line 833: Chapter 5. Examining Outcomes with Assertions • 118
Line 834: report erratum  •  discuss
Line 835: 
Line 836: --- 페이지 137 ---
Line 837: Here’s what an AssertJ assertion looks like when applied to the common need
Line 838: of comparing one object to another—isEqualTo is analogous to assertEquals in JUnit:
Line 839: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 840: assertThat(name).isEqualTo("my big fat acct");
Line 841: So far, so simple. To note:
Line 842: • You can take advantage of autocomplete to flesh out the assertion.
Line 843: • The assertion reads like an English sentence, left to right.
Line 844: AssertJ provides numerous inversions of positively stated assertions. Thus,
Line 845: the converse of isEqualTo is isNotEqualTo:
Line 846: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 847: assertThat(name).isNotEqualTo("plunderings");
Line 848: A few more examples follow. Most of them speak for themselves, and that’s
Line 849: part of the point.
Line 850: You can use chaining to specify multiple expected outcomes in a single
Line 851: statement. The following assertion passes if the name references a string that
Line 852: both starts with "my" and ends with "acct":
Line 853: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 854: assertThat(name)
Line 855: .startsWith("my")
Line 856: .endsWith("acct");
Line 857: A type-checking example:
Line 858: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 859: assertThat(name).isInstanceOf(String.class);
Line 860: Using regular expressions:
Line 861: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 862: assertThat(name).containsPattern(
Line 863: compile("\\s+(big fat|small)\\s+"));
Line 864: AssertJ contains numerous tests around lists:
Line 865: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 866: @Test
Line 867: public void simpleListTests() {
Line 868: var names = List.of("Moe", "Larry", "Curly");
Line 869: assertThat(names).contains("Curly");
Line 870: assertThat(names).contains("Curly", "Moe");
Line 871: assertThat(names).anyMatch(name -> name.endsWith("y"));
Line 872: assertThat(names).allMatch(name -> name.length() < 6);
Line 873: }
Line 874: report erratum  •  discuss
Line 875: Third-Party Assertion Libraries • 119
Line 876: 
Line 877: --- 페이지 138 ---
Line 878: The third list assertion passes if any one or more of the elements in the list
Line 879: ends with the substring "y". (The strings "Larry" or "Curly" here make it pass.)
Line 880: The fourth assertion passes if all of the elements in the list have a length less
Line 881: than 6. (They do.)
Line 882: (Caveat: The preceding asserts that verify only part of a string might be con-
Line 883: sidered weak assertions. You likely need to verify more.)
Line 884: AssertJ’s failing fluent assertions provide far more useful failure messages
Line 885: than what JUnit might give you. Here’s a failing assertion for the list of names:
Line 886: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 887: assertThat(names).allMatch(name -> name.length() < 5);
Line 888: … and here’s the failure message generated by AssertJ:
Line 889: Expecting all elements of:
Line 890: ["Moe", "Larry", "Curly"]
Line 891: to match given predicate but these elements did not:
Line 892: ["Larry", "Curly"]
Line 893: Knowing exactly why the assert failed should speed up your fix.
Line 894: AssertJ allows you to express your assertions in the most concise manner
Line 895: possible, particularly as things get more complex. Occasionally, your tests will
Line 896: need to extract specific data from results in order to effectively assert against
Line 897: it. With JUnit, doing so might require one or more lines of code before you
Line 898: can write the assertion. With AssertJ, you might be able to directly express
Line 899: your needs in a single statement.
Line 900: The Power of Fluency
Line 901: Let’s look at a small example that still demonstrates some of AssertJ’s power.
Line 902: The example uses two classes:
Line 903: • a Flight class that declares a segment field of type Segment
Line 904: • a Segment class containing the fields origin, destination, and distance
Line 905: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 906: record Segment(String origin, String destination, int distance) {
Line 907: boolean includes(String airport) {
Line 908: return origin.equals(airport) || destination.equals(airport);
Line 909: }
Line 910: }
Line 911: record Flight(Segment segment, LocalDateTime dateTime) {
Line 912: Flight(String origin, String destination,
Line 913: int distance, LocalDateTime dateTime) {
Line 914: Chapter 5. Examining Outcomes with Assertions • 120
Line 915: report erratum  •  discuss
Line 916: 
Line 917: --- 페이지 139 ---
Line 918: this(new Segment(origin, destination, distance), dateTime);
Line 919: }
Line 920: boolean includes(String airport) {
Line 921: return segment.includes(airport);
Line 922: }
Line 923: }
Line 924: The following AssertJ assertion compares against a list of Flight objects stored
Line 925: in the variable flights:
Line 926: utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
Line 927: @Test
Line 928: void filterAndExtract() {
Line 929: // ...
Line 930: assertThat(flights)
Line 931: .filteredOn(flight -> flight.includes("DEN"))
Line 932: .extracting("segment.distance", Integer.class)
Line 933: .allMatch(distance -> distance < 1700);
Line 934: }
Line 935: The call to filteredOn returns a subset of flights involving the flight code "DEN".
Line 936: The call to extracting applies an AssertJ property reference ("segment.distance") to
Line 937: each "DEN" flight. The reference tells AssertJ to first retrieve the segment object
Line 938: from a flight, then retrieve the distance value from that segment as an Integer.
Line 939: Yes, you could manually code an equivalent to the AssertJ solution, but the
Line 940: resulting code would lose the declarative nature that AssertJ can provide.
Line 941: Your test would require more effort to both write and read. In contrast,
Line 942: AssertJ’s support for method chaining creates a fluent sentence that you can
Line 943: read as a single concept.
Line 944: Regardless of whether you choose to adopt AssertJ or another third-party
Line 945: assertions library, streamline your tests so they read as concise documenta-
Line 946: tion. A well-designed assertion step minimizes stepwise reading.
Line 947: Eliminating Non-Tests
Line 948: Assertions are what make a test an automated test. Omitting assertions from
Line 949: your tests would render them pointless. And yet, some developers do exactly
Line 950: that in order to meet code coverage mandates easily. Another common ruse
Line 951: is to write tests that exercise a large amount of code, then assert something
Line 952: simple—for example, that a method’s return value is not null.
Line 953: Such non-tests provide almost zero value at a significant cost in time and
Line 954: effort. Worse, they carry an increasingly negative return on investment: you
Line 955: must expend time on non-tests when they fail or error, when they appear in
Line 956: report erratum  •  discuss
Line 957: Eliminating Non-Tests • 121
Line 958: 
Line 959: --- 페이지 140 ---
Line 960: search results (“is that a real test we need to update or do we not need to
Line 961: worry about it?”), and when you must update them to keep them running
Line 962: (for example, when a method signature gets changed).
Line 963: Eliminate tests that verify nothing.
Line 964: Summary
Line 965: You’ve learned numerous assertion forms in this chapter. You also learned
Line 966: about AssertJ, an alternate assertions library.
Line 967: Initially, you’ll survive if you predominantly use assertEquals for most assertions,
Line 968: along with an occasional assertTrue or assertFalse. You’ll want to move to the next
Line 969: level quickly, however, and learn to use the most concise and expressive
Line 970: assertion for the situation at hand.
Line 971: Armed with a solid understanding of how to write assertions, you’ll next dig
Line 972: into the organization of test classes so that you can most effectively run and
Line 973: maintain related groups of tests.
Line 974: Chapter 5. Examining Outcomes with Assertions • 122
Line 975: report erratum  •  discuss