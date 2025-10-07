Line 1: 
Line 2: --- 페이지 141 ---
Line 3: CHAPTER 6
Line 4: Establishing Organization in JUnit Tests
Line 5: Your JUnit learnings so far include:
Line 6: • How to run JUnit and understand its results
Line 7: • How to group related test methods within a test class
Line 8: • How to group common test initialization into a @BeforeEach method
Line 9: • A deep dive into JUnit assertions (the previous chapter)
Line 10: Generally, you want at least one test class for each production class you
Line 11: develop. In this chapter, you’ll dig into the topic of test organization within a
Line 12: test class. You’ll learn about:
Line 13: • The parts of a test
Line 14: • Initializing and cleaning up using lifecycle methods
Line 15: • Grouping related tests with nested classes
Line 16: • The JUnit test execution lifecycle
Line 17: • Avoiding dependency challenges by never ordering tests
Line 18: • Executing multiple test cases for a single test using parameterized tests
Line 19: The Parts of an Individual Test
Line 20: A handful of chapters ago (see Scannability: Arrange—Act—Assert, on page
Line 21: 18), you learned how AAA provides a great visual mnemonic to help readers
Line 22: quickly understand the core parts of a test.
Line 23: Some developers refer to a “four-phase test,”
Line 24: 1 where each test can be broken
Line 25: into (wait for it) four parts or phases:
Line 26: • Set up state/data in what’s sometimes called a fixture. Think of a fixture
Line 27: as the context in which a test runs—its world, so to speak. The fixture is
Line 28: 1.
Line 29: http://xunitpatterns.com/Four%20Phase%20Test.html
Line 30: report erratum  •  discuss
Line 31: 
Line 32: --- 페이지 142 ---
Line 33: managed for you by JUnit; you’ll learn more about that in this chapter
Line 34: as part of the JUnit test execution lifecycle.
Line 35: • Interact with the system to execute what you want to verify.
Line 36: • Do the verification (assert).
Line 37: • Tear down the fixture—clean up any side effects, if necessary. This typi-
Line 38: cally involves cleaning up resources that a test might have used and that
Line 39: could impact the execution of other tests. In this chapter, you’ll read
Line 40: about doing such clean-up with @AfterEach and @AfterAll JUnit hooks.
Line 41: For every intent and purpose, AAA is the first three parts of a four-part test.
Line 42: Arrange, act, assert ≈ setup, execute, verify.
Line 43: Turns out that the fourth part, “tear down,” is and should be rare in unit
Line 44: tests, in which you seek to avoid (mostly by design) interaction with the things
Line 45: that you must clean up. If you feel AAA cheats you out of that fourth phase,
Line 46: you can add a fourth “A”…for ANNIHILATION! (If the violence disturbs you,
Line 47: just mentally go with “After.” Keep calm and carry on.)
Line 48: Setting Up and Tearing Down Using Lifecycle Methods
Line 49: You learned about @BeforeEach in your first JUnit example (see Chapter 1,
Line 50: Building Your First JUnit Test, on page 3). Let’s take a closer look at this
Line 51: initialization hook, as well as some other useful hooks that JUnit provides.
Line 52: Initializing with @BeforeEach and @BeforeAll
Line 53: In Abstraction: Eliminating Boring Details, on page 20, you learned to use
Line 54: @BeforeEach to put common initialization in one place. Methods annotated
Line 55: with @BeforeEach are executed before each test in scope.
Line 56: JUnit also provides another initialization hook known as @BeforeAll, which you
Line 57: must declare as a static method. Each method annotated with @BeforeAll gets
Line 58: executed once per test class and prior to the execution of anything else
Line 59: within that class. Its primary use is to ensure that slowly executing initializa-
Line 60: tions (for example, anything involving a database) only have to execute once.
Line 61: Otherwise, prefer using @BeforeEach.
Line 62: If you find yourself using @BeforeAll more than once in a blue moon, you may
Line 63: be testing behaviors bigger than units. That may be okay, but it might suggest
Line 64: you have opportunities for reducing the dependencies in your system. See
Line 65: Chapter 3, Using Test Doubles, on page 53 for ideas on how to do that.
Line 66: Chapter 6. Establishing Organization in JUnit Tests • 124
Line 67: report erratum  •  discuss
Line 68: 
Line 69: --- 페이지 143 ---
Line 70: If your test needs demand that you initialize a few things before each test is
Line 71: run, you can declare multiple @BeforeEach methods in the test class’s scope,
Line 72: each with a different name. These don’t run in any useful order, just as test
Line 73: methods do not.
Line 74: Creating additional @BeforeEach methods allows you to use their methods name
Line 75: to describe what’s going on in each initialization. Of course, you can also
Line 76: lump all your initialization into a single @BeforeEach method as long as it’s easy
Line 77: for other developers to understand what’s going on when reading through
Line 78: your lump.
Line 79: You can have multiple (static) @BeforeAll methods in a test class.
Line 80: Using @AfterEach and @AfterAll for Cleanup
Line 81: JUnit bookends the initialization hooks @BeforeEach and @BeforeAll with corre-
Line 82: sponding “teardown” lifecycle methods @AfterEach and @AfterAll. These methods
Line 83: allow you to clean up resources on test completion. Both @AfterEach and
Line 84: @AfterAll are guaranteed to run (as long as the JUnit process itself doesn’t
Line 85: crash), even if any tests throw exceptions.
Line 86: Within @AfterEach, for example, you might close a database connection or delete
Line 87: a file. If you write integration (non-unit) tests in JUnit, these teardown hooks
Line 88: are essential.
Line 89: Most unit tests, however, shouldn’t interact with code that requires clean-up.
Line 90: The typical, hopefully rare case is when multiple tests alter the state of a
Line 91: static field.
Line 92: If you do have a clean-up need, try to redesign your code to eliminate it. Use
Line 93: dependency injection (see Injecting Dependencies into Production Code, on
Line 94: page 56) and/or mock objects (see Chapter 3, Using Test Doubles, on page
Line 95: 53) as appropriate.
Line 96: Even when you do have a legitimate clean-up need, adding code to @AfterEach
Line 97: or @AfterAll is mostly only being nice. Suppose the general assumption is that
Line 98: all tests clean up after themselves—seems like a fair testing standard, yes?
Line 99: The problem is that eventually, someone will forget to properly clean up in
Line 100: another test elsewhere. If your test fails as a result, it may take some real
Line 101: time to figure out which one of possibly thousands of tests is the culprit.
Line 102: Each of your tests is responsible for ensuring it executes in a
Line 103: clean, expected state.
Line 104: report erratum  •  discuss
Line 105: Setting Up and Tearing Down Using Lifecycle Methods • 125
Line 106: 
Line 107: --- 페이지 144 ---
Line 108: You can usually design your code so almost no unit tests require clean-up,
Line 109: but you may still need @AfterEach in a tiny number of places.
Line 110: Organizing Related Tests into Nested Classes
Line 111: As your classes grow by taking on more behaviors, you’ll need more and more
Line 112: tests to describe the new behaviors. Use your test class size as a hint: if you
Line 113: declare several dozen tests in one test source file, chances are good that the
Line 114: class under test is too large. Consider splitting the production class up into
Line 115: two or more classes, which also means you’ll want to split the test methods
Line 116: across at least two or more test classes.
Line 117: You may still end up with a couple dozen test methods in one test class. A
Line 118: larger test class can not only be daunting from a navigational sense, but it
Line 119: can also make it harder to find all tests that relate to each other.
Line 120: To help group related tests, you might consider starting each related test’s
Line 121: name with the same thing. Here are three tests describing how withdrawals
Line 122: work in the Account class:
Line 123: @Test void withdrawalReducesAccountBalance() { /* ... */ }
Line 124: @Test void withdrawalThrowsWhenAmountExceedsBalance() { /* ... */ }
Line 125: @Test void withdrawalNotifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
Line 126: A better solution, however, is to group related tests within a JUnit @Nested
Line 127: class:
Line 128: @Nested
Line 129: class Withdrawal {
Line 130: @Test void reducesAccountBalance() { /* ... */ }
Line 131: @Test void throwsWhenAmountExceedsBalance() { /* ... */ }
Line 132: @Test void notifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
Line 133: }
Line 134: You can create a number of @Nested classes within your test class, similarly
Line 135: grouping all methods within it. The name of the nested class, which describes
Line 136: the common behavior, can be removed from each test name.
Line 137: You can also use @Nested classes to group tests by context—the state estab-
Line 138: lished by the arrange part of a test. For example:
Line 139: class AnAccount
Line 140: @Nested
Line 141: class WithZeroBalance {
Line 142: @Test void doesNotAccrueInterest() { /* ... */ }
Line 143: @Test void throwsOnWithdrawal() { /* ... */ }
Line 144: }
Line 145: Chapter 6. Establishing Organization in JUnit Tests • 126
Line 146: report erratum  •  discuss
Line 147: 
Line 148: --- 페이지 145 ---
Line 149: @Nested
Line 150: class WithPositiveBalance {
Line 151: @BeforeEach void fundAccount() { account.deposit(1000); }
Line 152: @Test void accruesInterest() { /* ... */ }
Line 153: @Test void reducesBalanceOnWithdrawal() { /* ... */ }
Line 154: }
Line 155: }
Line 156: Tests are split between those needing a zero-balance account (WithZeroBalance)
Line 157: and those needing a positive account balance (WithPositiveBalance).
Line 158: Observing the JUnit Lifecycle
Line 159: You’ve learned about using before and after hooks and how to group related
Line 160: tests into nested classes. Using a skeleton test class, let’s take a look at how
Line 161: these JUnit elements are actually involved when you run your tests.
Line 162: AFundedAccount contains six tests. Per its name, all tests can assume that an
Line 163: account exists and has a positive balance. An account object gets created at
Line 164: the field level and subsequently funded within a @BeforeEach method. Here’s
Line 165: the entire AFundedAccount test class, minus all the intricate details of each test.
Line 166: utj3-junit/01/src/test/java/scratch/AFundedAccount.java
Line 167: import org.junit.jupiter.api.*;
Line 168: class AFundedAccount {
Line 169: Account account = new Account("Jeff");
Line 170: AFundedAccount() {
Line 171: // ...
Line 172: }
Line 173: @BeforeEach
Line 174: void fundAccount() {
Line 175: account.deposit(1000);
Line 176: }
Line 177: @BeforeAll
Line 178: static void clearAccountRegistry() {
Line 179: // ...
Line 180: }
Line 181: @Nested
Line 182: class AccruingInterest {
Line 183: @BeforeEach
Line 184: void setInterestRate() {
Line 185: account.setInterestRate(0.027d);
Line 186: }
Line 187: @Test
Line 188: void occursWhenMinimumMet() {
Line 189: // ...
Line 190: }
Line 191: report erratum  •  discuss
Line 192: Organizing Related Tests into Nested Classes • 127
Line 193: 
Line 194: --- 페이지 146 ---
Line 195: @Test
Line 196: void doesNotOccurWhenMinimumNotMet() {
Line 197: // ...
Line 198: }
Line 199: @Test
Line 200: void isReconciledWithMasterAccount() {
Line 201: // ...
Line 202: }
Line 203: }
Line 204: @Nested
Line 205: class Withdrawal {
Line 206: @Test
Line 207: void reducesAccountBalance() {
Line 208: // ...
Line 209: }
Line 210: @Test
Line 211: void throwsWhenAmountExceedsBalance() {
Line 212: // ...
Line 213: }
Line 214: @Test
Line 215: void notifiesIRSWhenAmountExceedsThreshold() {
Line 216: // ...
Line 217: }
Line 218: }
Line 219: }
Line 220: While you could choose to instantiate the account field in a @BeforeEach method,
Line 221: there’s nothing wrong with doing field-level initialization, particularly if
Line 222: there’s not much going on. The field declaration in AFundedAccount initializes
Line 223: an account with some arbitrary name, so it’s not interesting enough to warrant
Line 224: a @BeforeEach method. But if your common initialization is at all interesting or
Line 225: requires a series of statements, you’d definitely want it to occur within a
Line 226: @BeforeEach method.
Line 227: The use of @Nested makes for well organized test results when you run your tests:
Line 228: Chapter 6. Establishing Organization in JUnit Tests • 128
Line 229: report erratum  •  discuss
Line 230: 
Line 231: --- 페이지 147 ---
Line 232: You can clearly see the grouping of related tests, which makes it easier to find
Line 233: what you’re looking for. The visual grouping also makes it easier to spot the glaring
Line 234: absence of necessary tests as well as review their names for consistency—with
Line 235: other tests or with your team’s standards for how tests are named.
Line 236: I instrumented each of the @BeforeEach methods, the @Test methods, and the
Line 237: constructors (implicitly defined in the listing) with System.out statements. Here’s
Line 238: the output when the tests are run:
Line 239: @BeforeAll::clearAccountRegistry
Line 240: AFundedAccount(); Jeff balance = 0
Line 241: Withdrawal
Line 242: @BeforeEach::fundAccount
Line 243: notifiesIRSWhenAmountExceedsThreshold
Line 244: AFundedAccount(); Jeff balance = 0
Line 245: Withdrawal
Line 246: @BeforeEach::fundAccount
Line 247: reducesAccountBalance
Line 248: AFundedAccount(); Jeff balance = 0
Line 249: Withdrawal
Line 250: @BeforeEach::fundAccount
Line 251: throwsWhenAmountExceedsBalance
Line 252: AFundedAccount(); Jeff balance = 0
Line 253: Accruing Interest
Line 254: @BeforeEach::fundAccount
Line 255: @BeforeEach::setInterestRate
Line 256: occursWhenMinimumMet
Line 257: AFundedAccount(); Jeff balance = 0
Line 258: Accruing Interest
Line 259: @BeforeEach::fundAccount
Line 260: @BeforeEach::setInterestRate
Line 261: accruesNoInterestWhenMinimumMet
Line 262: AFundedAccount(); Jeff balance = 0
Line 263: Accruing Interest
Line 264: @BeforeEach::fundAccount
Line 265: @BeforeEach::setInterestRate
Line 266: doesNotOccurWhenMinimumNotMet
Line 267: The static @BeforeAll method executes first.
Line 268: The output shows that a new instance of AFundedAccount is constructed for each
Line 269: test executed. It also shows that the account is, as expected, properly initial-
Line 270: ized with a name and zero balance.
Line 271: Creating a new instance for each test is part of JUnit’s deliberate design. It
Line 272: helps ensure each test is isolated from side effects that other tests might
Line 273: create.
Line 274: report erratum  •  discuss
Line 275: Organizing Related Tests into Nested Classes • 129
Line 276: 
Line 277: --- 페이지 148 ---
Line 278: JUnit creates a new instance of the test class for each test method
Line 279: that runs.
Line 280: The @BeforeEach method fundAccount, declared within the top-level scope of the
Line 281: AFundedAccount class, executes prior to each of all six tests.
Line 282: The @BeforeEach method setInterestRate, declared within the scope of AccruingInterest,
Line 283: executes only prior to each of the three tests defined within that nested class.
Line 284: Avoiding Dependency Despair: Don’t Order Your Tests!
Line 285: JUnit tests don’t run in their declared (top to bottom) order. In fact, they don’t
Line 286: run in any order that you’d easily be able to determine or depend on, such
Line 287: as alphabetically. (They’re likely returned in the order that a call to
Line 288: java.lang.Class.getMethods() returns, which is “not sorted and not in any particular
Line 289: order,” per its Javadoc.)
Line 290: You might be tempted to think you want your tests to run in a specific order:
Line 291: “I’m writing a first test around newly created accounts, which have a zero
Line 292: balance. A second test can add $100 to the account, and I can verify that
Line 293: amount. I can then add a test that runs third, in which I’ll deposit $50 and
Line 294: ensure that the new balance is $150.”
Line 295: While JUnit 5 provides a way to force the ordering of test execution, using it
Line 296: for unit tests is a bad idea. Depending on test order might help you avoid
Line 297: redundantly stepping through common setup in multiple test cases. But it
Line 298: will usually lead you down the path to wasted time. For example, say you’re
Line 299: running tests, and the fourth test fails. Was it because of a real problem in
Line 300: the production code? Or was it because one of the preceding three tests (which
Line 301: one?) left the system in some newly unexpected state?
Line 302: With ordered tests, you’ll also have a harder time understanding any test
Line 303: that’s dependent on other tests. Increasing dependencies is as costly in tests
Line 304: as it is in your production code.
Line 305: Unit tests should verify isolated units of code and not depend on
Line 306: any order of execution.
Line 307: Rather than creating headaches by forcing the order of tests, use @BeforeEach
Line 308: to reduce the duplication of common initialization. You can also extract helper
Line 309: methods to reduce redundancy and amplify your tests’ abstraction level.
Line 310: Chapter 6. Establishing Organization in JUnit Tests • 130
Line 311: report erratum  •  discuss
Line 312: 
Line 313: --- 페이지 149 ---
Line 314: Executing Multiple Data Cases with Parameterized Tests
Line 315: Many of your system’s behaviors will demand several distinct test cases. For
Line 316: example, you’ll often end up with at least three tests as you work through
Line 317: the progression of zero-one-many.
Line 318: Defining separate test methods allows you to explicitly summarize their distinct
Line 319: behaviors in the test names:
Line 320: storesEmptyStringWhenEmpty
Line 321: storesInputStringWhenContainingOneElement
Line 322: storesCommaSeparatedStringWhenContainingManyElements
Line 323: Often, the three test cases will be structured exactly the same—all the state-
Line 324: ments within it are the same, but the input and expected output data differ.
Line 325: You can streamline the redundancies across these tests with things like helper
Line 326: methods and @BeforeEach methods if it bothers you.
Line 327: Sometimes, when you have such redundancy across tests, there’s no interest-
Line 328: ing way to name them distinctly. For example, suppose you have tests for
Line 329: code that converts Arabic numbers into Roman equivalents:
Line 330: utj3-junit/01/src/main/java/util/RomanNumberConverter.java
Line 331: public class RomanNumberConverter {
Line 332: record Digit(int arabic, String roman) {}
Line 333: Digit[] conversions = {
Line 334: new Digit(1000, "M"),
Line 335: new Digit(900, "CM"),
Line 336: new Digit(500, "D"),
Line 337: new Digit(400, "CD"),
Line 338: new Digit(100, "C"),
Line 339: new Digit(90, "XC"),
Line 340: new Digit(50, "L"),
Line 341: new Digit(40, "XL"),
Line 342: new Digit(10, "X"),
Line 343: new Digit(9, "IX"),
Line 344: new Digit(5, "V"),
Line 345: new Digit(4, "IV"),
Line 346: new Digit(1, "I")
Line 347: };
Line 348: public String toRoman(int arabic) {
Line 349: return Arrays.stream(conversions).reduce(
Line 350: new Digit(arabic, ""),
Line 351: (acc, conversion) -> {
Line 352: var digitsRequired = acc.arabic / conversion.arabic;
Line 353: report erratum  •  discuss
Line 354: Executing Multiple Data Cases with Parameterized Tests • 131
Line 355: 
Line 356: --- 페이지 150 ---
Line 357: return new Digit(
Line 358: acc.arabic - digitsRequired * conversion.arabic,
Line 359: acc.roman + conversion.roman.repeat(digitsRequired));
Line 360: }).roman();
Line 361: }
Line 362: }
Line 363: Neither the algorithm nor the behavior changes based on the inputs. Were
Line 364: you to code this as separate JUnit tests, there’d be little useful distinction
Line 365: between the test names:
Line 366: utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
Line 367: import org.junit.jupiter.api.Test;
Line 368: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 369: class ARomanNumberConverter {
Line 370: RomanNumberConverter converter = new RomanNumberConverter();
Line 371: @Test
Line 372: void convertsOne() {
Line 373: assertEquals("I", converter.toRoman(1));
Line 374: }
Line 375: @Test
Line 376: void convertsTwo() {
Line 377: assertEquals("II", converter.toRoman(2));
Line 378: }
Line 379: @Test
Line 380: void convertsThree() {
Line 381: assertEquals("III", converter.toRoman(3));
Line 382: }
Line 383: // ... so wordy!
Line 384: }
Line 385: It’s tedious to create separate tests for each case, and their names add little
Line 386: real value. You could lump them all in a single test method but then the
Line 387: individual cases wouldn’t be isolated from each other.
Line 388: Fortunately, JUnit supports a special form of test known as a parameterized
Line 389: test. You create a parameterized test by annotating your test method with
Line 390: @ParameterizedTest instead of @Test. You must also provide a data source, which
Line 391: is essentially a list of data rows. For each data row, JUnit calls the test method
Line 392: with data from the row as parameters.
Line 393: The parameterized test method for the RomanNumberConverter needs two pieces
Line 394: of information: the Arabic number to be passed to the toRoman method and
Line 395: the expected Roman equivalent to be used in an assertEquals statement. You
Line 396: can use a @CsvSource to provide data rows for the test; each row is a CSV
Line 397: (comma-separated values) string.
Line 398: Chapter 6. Establishing Organization in JUnit Tests • 132
Line 399: report erratum  •  discuss
Line 400: 
Line 401: --- 페이지 151 ---
Line 402: Here’s a parameterized test for the RomanNumberConverter:
Line 403: utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
Line 404: @ParameterizedTest
Line 405: @CsvSource({
Line 406: "1,
Line 407: I",
Line 408: ➤
Line 409: "2,
Line 410: II",
Line 411: "3,
Line 412: III",
Line 413: "10,
Line 414: X",
Line 415: "20,
Line 416: XX",
Line 417: "11,
Line 418: XI",
Line 419: "200,
Line 420: CC",
Line 421: "732,
Line 422: DCCXXXII",
Line 423: "2275, MMCCLXXV",
Line 424: "999,
Line 425: CMXCIX",
Line 426: "444,
Line 427: CDXLIVI", // failure
Line 428: })
Line 429: void convertAll(int arabic, String roman) {
Line 430: ➤
Line 431: assertEquals(roman, converter.toRoman(arabic));
Line 432: }
Line 433: The first data row in the @CsvSource (highlighted) contains the CSV string "1,
Line 434: I".
Line 435: JUnit splits this string on the comma and trims the resulting values. It passes
Line 436: these values—the number 1 and the string "I"—to the convertAll test method
Line 437: (highlighted).
Line 438: JUnit takes the CSV values and uses them, left to right, as arguments to the
Line 439: test method. So when the test method is executed, 1 gets assigned to the int
Line 440: arabic parameter (with JUnit converting the string to an int), and "I" gets assigned
Line 441: to the String roman parameter.
Line 442: Since the above example shows eleven CSV data rows, JUnit will run convertAll
Line 443: eleven times. IntelliJ shows the parameters for each of the eleven cases:
Line 444: Note how JUnit indicates the failing (incorrectly specified) case.
Line 445: The JUnit documentation
Line 446: 2 goes into considerable detail about the various
Line 447: data source mechanisms available.
Line 448: 2.
Line 449: https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-sources
Line 450: report erratum  •  discuss
Line 451: Executing Multiple Data Cases with Parameterized Tests • 133
Line 452: 
Line 453: --- 페이지 152 ---
Line 454: Here’s a quick summary:
Line 455: A single array of values. Useful only if your test takes one
Line 456: parameter (which implies that the expected outcome is the
Line 457: same for every source value)
Line 458: @ValueSource
Line 459: Iterates all the possible enum values, with some options for
Line 460: inclusion/exclusion and regex matching
Line 461: @EnumSource
Line 462: Expects the name of a method, which must return all data
Line 463: rows in a stream
Line 464: @MethodSource
Line 465: Mostly the same thing as @CsvSource, except that you specify
Line 466: a filename containing the CSV rows
Line 467: @CsvFileSource
Line 468: Allows you to create a custom, reusable data source in a
Line 469: class that extends an interface named ArgumentsProvider
Line 470: @ArgumentsSource
Line 471: While parameterized tests in JUnit are sophisticated and flexible beasts,
Line 472: @CsvSource will suit most of your needs. I’ve never needed another data source
Line 473: variant (though I don’t frequently use parameterized tests).
Line 474: In summary, parameterized tests are great when you need to demonstrate
Line 475: data (not behavioral) variants. These are a couple of pervasive needs:
Line 476: • Code that conditionally executes if a parameter is null or an empty string.
Line 477: A parameterized test with two inputs (null and "") lets you avoid test
Line 478: duplication.
Line 479: • Code around border conditions, particularly because such code often
Line 480: breeds defects. For example, for code that conditionally executes if n <= 0,
Line 481: use a parameterized test with the values n - 1 and n.
Line 482: Otherwise, create a new @Test that describes a distinct behavior.
Line 483: Summary
Line 484: On most systems, you’ll end up with many hundreds or thousands of unit
Line 485: tests. You’ll want to keep your maintenance costs low by taking advantage
Line 486: of a few JUnit features, including lifecycle methods, nested classes, and param-
Line 487: eterized tests. These features allow you to reduce redundant code and make
Line 488: it easy to run a related set of tests.
Line 489: Now that you’ve learned how to best organize your tests, in the next chapter,
Line 490: you’ll dig into topics that relate to executing tests using JUnit. You’ll pick up
Line 491: some good habits for deciding how many tests to run (and when to not run
Line 492: tests). You’ll learn how to run subsets of tests as well as how to temporarily
Line 493: disable tests.
Line 494: Chapter 6. Establishing Organization in JUnit Tests • 134
Line 495: report erratum  •  discuss