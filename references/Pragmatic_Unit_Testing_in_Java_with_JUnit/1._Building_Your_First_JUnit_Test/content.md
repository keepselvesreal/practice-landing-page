Line 1: 
Line 2: --- 페이지 24 ---
Line 3: CHAPTER 1
Line 4: Building Your First JUnit Test
Line 5: In this chapter, we’ll write a unit test by working through a small example.
Line 6: You’ll set up your project, add a test class, and see what a test method looks
Line 7: like. Most importantly, you’ll get JUnit to run your new, passing test.
Line 8: Reasons to Write a Unit Test
Line 9: Joe has just completed work on a small feature change, adding several dozen
Line 10: lines to the system. He’s fairly confident in his change, but it’s been a while
Line 11: since he’s tried things out in the deployed system. Joe runs the build script,
Line 12: which packages and deploys the change to the local web server. He pulls up
Line 13: the application in his browser, navigates to the appropriate screen, enters a
Line 14: bit of data, clicks submit, and…stack trace!
Line 15: Joe stares at the screen for a moment, then the code. Aha! Joe notes that he
Line 16: forgot to initialize a field. He makes the fix, runs the build script again, cranks
Line 17: up the application, enters data, clicks submit, and…hmm, that’s not the right
Line 18: amount. Oops. This time, it takes a bit longer to decipher the problem. Joe
Line 19: fires up his debugger and after a few minutes discovers an off-by-one error
Line 20: in indexing an array. He once again repeats the cycle of fix, deploy, navigate
Line 21: the GUI, enter data, and verify results.
Line 22: Happily, Joe’s third fix attempt has been the charm. But he spent about fifteen
Line 23: minutes working through the three cycles of code/manual test/fix.
Line 24: Lucia works differently. Each time she writes a small bit of code, she adds a
Line 25: unit test that verifies the small change she added to the system. She then
Line 26: runs all her unit tests, including the new one just written. They run in sec-
Line 27: onds, so she doesn’t wait long to find out whether or not she can move on.
Line 28: Because Lucia runs her tests with each small change, she only moves on
Line 29: when all the tests pass. If her tests fail, she knows she’s created a problem
Line 30: report erratum  •  discuss
Line 31: 
Line 32: --- 페이지 25 ---
Line 33: and stops immediately to fix it. The problems she creates are a lot easier to
Line 34: fix since she’s added only a few lines of code since she last saw all the tests
Line 35: pass. She avoids piling lots of new code atop her mistakes before discovering
Line 36: a problem.
Line 37: Lucia’s tests are part of the system and included in the project’s GitHub
Line 38: repository. They continue to pay off each time she or anyone else changes
Line 39: code, alerting the team when someone breaks existing behavior.
Line 40: Lucia’s tests also save Joe and everyone else on the team significant amounts
Line 41: of comprehension time on their system. “How does the system handle the
Line 42: case where the end date isn’t provided?” asks Madhu, the product owner.
Line 43: Joe’s response, more often than not, is, “I don’t know; let me take a look at
Line 44: the code.” Sometimes, Joe can answer the question in a minute or two, but
Line 45: frequently, he ends up digging about for a half hour or more.
Line 46: Lucia looks at her unit tests and finds one that matches Madhu’s case. She
Line 47: has an answer within a minute or so.
Line 48: You’ll follow in Lucia’s footsteps and learn how to write small, focused unit
Line 49: tests. You’ll start by learning basic JUnit concepts.
Line 50: Learning JUnit Basics: Your First Testing Challenge
Line 51: For your first example, you’ll work with a small class named CreditHistory. Its
Line 52: goal is to return the mean (average) for a number of credit rating objects.
Line 53: In this book, you’ll probe the many reasons for choosing to write unit tests.
Line 54: For now, you’ll start with a simple but critical reason: you want to continue
Line 55: adding behaviors to CreditHistory and want to know the moment you break any
Line 56: previously coded behaviors.
Line 57: Initially, you will see screenshots to help guide you through getting started
Line 58: with JUnit. After this chapter, you will see very few screenshots, and you
Line 59: won’t need them.
Line 60: The screenshots demonstrate using JUnit in IntelliJ IDEA. If you’re using
Line 61: another integrated development environment (IDE), the good news is that
Line 62: your JUnit test code will look the same whether you use IDEA, Eclipse,
Line 63: VSCode, or something else. How you set up your project to use JUnit will
Line 64: differ. The way the JUnit looks and feels will differ from IDE to IDE, though
Line 65: it will, in general, operate the same and produce the same information.
Line 66: Chapter 1. Building Your First JUnit Test • 4
Line 67: report erratum  •  discuss
Line 68: 
Line 69: --- 페이지 26 ---
Line 70: Here’s the code you need to test:
Line 71: utj3-credit-history/01/src/main/java/credit/CreditHistory.java
Line 72: import java.time.LocalDate;
Line 73: import java.time.Month;
Line 74: import java.util.*;
Line 75: public class CreditHistory {
Line 76: private final List<CreditRating> ratings = new ArrayList<>();
Line 77: public void add(CreditRating rating) {
Line 78: ratings.add(rating);
Line 79: }
Line 80: public int arithmeticMean() {
Line 81: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 82: return total / ratings.size();
Line 83: }
Line 84: }
Line 85: The CreditHistory class collects CreditRating objects through its add method. Its
Line 86: current primary goal is to provide you with an average (arithmeticMean) of the
Line 87: scores contained in the credit rating objects.
Line 88: You implement CreditRating with a Java record declaring a single rating field.
Line 89: utj3-credit-history/01/src/main/java/credit/CreditRating.java
Line 90: public record CreditRating(int rating) {}
Line 91: Your first exercise is small, and you could easily enter it from scratch. Typing
Line 92: in the code yourself should help you grow your coding skills faster. Still, you
Line 93: can also choose to download the source for this and all other exercises from
Line 94: https://pragprog.com/titles/utj3/pragmatic-unit-testing-in-java-with-junit-third-edition/.
Line 95: Where to Put the Tests
Line 96: Your project is laid out per the Apache Software Foundation’s standard
Line 97: directory layout:
Line 98: 1
Line 99: utj3-credit-history
Line 100: src/
Line 101: main/
Line 102: java/
Line 103: credit/
Line 104: CreditHistory.java
Line 105: CreditRating.java
Line 106: test/
Line 107: java/
Line 108: credit/
Line 109: 1.
Line 110: https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
Line 111: report erratum  •  discuss
Line 112: Learning JUnit Basics: Your First Testing Challenge • 5
Line 113: 
Line 114: --- 페이지 27 ---
Line 115: Your two production source files for this project are stored in the directory
Line 116: src/main/java in the package named credit. (IntelliJ IDEA refers to the direc-
Line 117: tory src/main/java as a Sources Root.)
Line 118: You’re ready to write a test that describes the behavior in CreditHistory. You’ll
Line 119: be putting the test in the same package as the production source—credit—but
Line 120: in the Test Sources Root directory src/test/java.
Line 121: Your IDE probably provides you with many ways to create a new test class.
Line 122: In IDEA, you’ll create it by following these steps in the Project explorer:
Line 123: 1.
Line 124: Select the package src/test/java/credit from the Project or Packages explorer.
Line 125: 2.
Line 126: Right-click to bring up the context menu.
Line 127: 3.
Line 128: Select New ▶ Java Class. You will see the New Java Class popup, which
Line 129: defaults its selection to creating a new class.
Line 130: 4.
Line 131: Type the classname ACreditHistory (“a credit history”); press enter. IDEA’s
Line 132: inspections may be unhappy about your test naming convention. You
Line 133: can reconfigure the inspection,
Line 134: 2 or you can go with the old-school name
Line 135: CreditHistoryTest.
Line 136: Running Tests: Testing Nothing at All
Line 137: When you press enter from the New ▶Java Class menu item, IDEA provides you
Line 138: with an empty class declaration for ACreditHistory. Your first job is to squeeze
Line 139: a test method into it:
Line 140: utj3-credit-history/01/src/test/java/credit/ACreditHistory.java
Line 141: class ACreditHistory {
Line 142: @org.junit.jupiter.api.Test
Line 143: ➤
Line 144: void whatever() {
Line 145: ➤
Line 146: }
Line 147: ➤
Line 148: }
Line 149: To be a bit more specific: Within the body of ACreditHistory, type in the three
Line 150: lines that start with the @org.junit.jupiter.api.Test annotation.
Line 151: Lines marked with arrows in code listings represent added lines,
Line 152: changed lines, or otherwise interesting bits of code.
Line 153: Type? Yes. It’s better to type code and tests in yourself while learning, rather
Line 154: than copy/paste them, unless typing isn’t at all your thing. It’ll feel more like
Line 155: 2.
Line 156: https://langrsoft.com/2024/04/28/your-new-test-naming-convention/
Line 157: Chapter 1. Building Your First JUnit Test • 6
Line 158: report erratum  •  discuss
Line 159: 
Line 160: --- 페이지 28 ---
Line 161: real development, which should help you learn more. It also won’t take as long
Line 162: as you think. Your IDE offers numerous time-saving shortcuts, such as
Line 163: intellisense, live templates, and context-sensitive “quick fix.”
Line 164: Your test is an empty method annotated with the type @org.junit.jupiter.api.Test.
Line 165: When you tell JUnit to run one or more tests, it will locate all methods
Line 166: annotated with @Test and run them. It’ll ignore all other methods.
Line 167: You can run your empty test, which, for now, you’ve given a placeholder name
Line 168: of whatever. As usual, you have many options for executing tests. You’ll start
Line 169: by being mousey. Click the little green arrow that appears to the left of the
Line 170: class declaration, as shown in the following figure. (Chances are good your
Line 171: IDE has a similar icon.)
Line 172: Clicking the green arrow pops up a context menu where you can select the
Line 173: option to run all tests in ACreditHistory, as shown in this figure:
Line 174: Clicking Run 'ACreditHistory' runs the whatever test. It’s passing, as the figure on
Line 175: page 8 reveals.
Line 176: If your test isn’t getting executed, make sure it follows these three guidelines:
Line 177: • it is annotated with @org.junit.jupiter.api.Test
Line 178: • it has a void return
Line 179: • it has no parameters
Line 180: report erratum  •  discuss
Line 181: Learning JUnit Basics: Your First Testing Challenge • 7
Line 182: 
Line 183: --- 페이지 29 ---
Line 184: The built-in JUnit test runner appears at the bottom of the IDE. Its left-hand
Line 185: panel shows a summary of all the tests executed. Your summary shows that
Line 186: you ran the whatever test within ACreditHistory, that it succeeded (because it has
Line 187: a green check mark), and that it took 12 milliseconds to execute.
Line 188: The test runner’s right-hand panel shows different information depending on
Line 189: what’s selected in the left-hand panel. By default, it tells you how many tests
Line 190: passed out of the number that were executed (yours: “1 of 1”). It also provides
Line 191: you with information captured as part of the JUnit process execution. (In this
Line 192: screenshot, the IDE is configured to use Gradle to execute the test via the
Line 193: build task, which also executes the tests.)
Line 194: You now know something fundamental about how JUnit behaves: an empty
Line 195: test passes. More specifically and more usefully, a test whose method execu-
Line 196: tion completes—without having encountered any failure points or throwing
Line 197: any exceptions—is a passing test.
Line 198: Writing a First Real Test
Line 199: An empty test isn’t of much use. Let’s devise a good first test.
Line 200: You could start with a meaty test that adds a few credit scores, asks for the
Line 201: average, and then ascertains whether or not you got the right answer. This
Line 202: happy path test case—in contrast with negative or error-based tests—is not
Line 203: the only test you’d want to write, though. You have some other cases to con-
Line 204: sider for verifying arithmeticMean:
Line 205: Chapter 1. Building Your First JUnit Test • 8
Line 206: report erratum  •  discuss
Line 207: 
Line 208: --- 페이지 30 ---
Line 209: • What happens if you add only one credit rating?
Line 210: • What happens if you don’t add any credit ratings?
Line 211: • Are there any exceptional cases—conditions under which a problem could
Line 212: occur? How does the code behave under these conditions?
Line 213: Starting with a happy path test is one choice; you have other options. One is
Line 214: to start with the simplest test possible, move on to incrementally more complex
Line 215: tests, and finally to exceptional cases. Another option is to start with the
Line 216: exceptional cases first, then cover happy path cases in complexity order.
Line 217: Other ordering schemes are, of course, possible.
Line 218: When writing unit tests for code you’ve already written, ultimately, the order
Line 219: really doesn’t matter. But if you follow a consistent approach, you’ll be less
Line 220: likely to miss something. Throughout this book, the progression you’ll prefer
Line 221: will be to start with the simplest case, then move on to incrementally more
Line 222: complex happy path cases, and then to exception-based tests.
Line 223: The Simplest Possible Case
Line 224: The simplest case often involves zero or some concept of nothing. Calcu-
Line 225: lating the arithmetic mean involves creating a credit history with nothing
Line 226: added to it. You think that an empty credit history should return an average
Line 227: of zero.
Line 228: Update ACreditHistory with the following code, which replaces the whatever test
Line 229: with a new one:
Line 230: utj3-credit-history/02/src/test/java/credit/ACreditHistory.java
Line 231: import org.junit.jupiter.api.Test;
Line 232: Line 1
Line 233: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 234: -
Line 235: -
Line 236: class ACreditHistory {
Line 237: -
Line 238: @Test
Line 239: 5
Line 240: void withNoCreditRatingsHas0Mean() {
Line 241: -
Line 242: var creditHistory = new CreditHistory();
Line 243: -
Line 244: var result = creditHistory.arithmeticMean();
Line 245: -
Line 246: assertEquals(0, result);
Line 247: -
Line 248: }
Line 249: 10
Line 250: }
Line 251: -
Line 252: Let’s step through the updated lines in ACreditHistory.java.
Line 253: Each of your tests will call one or more assertion methods to verify your
Line 254: assumptions about the system. That’ll add up to piles of lines of assertions.
Line 255: Since these assertions are static methods, add a static import at 2 so that
Line 256: you don’t have to constantly qualify your assertion calls.
Line 257: report erratum  •  discuss
Line 258: Writing a First Real Test • 9
Line 259: 
Line 260: --- 페이지 31 ---
Line 261: Line 2: You simplify your test declaration by introducing an import statement
Line 262: for the @Test annotation.
Line 263: The test name whatever wasn’t much of a winner, so supply a new one at line
Line 264: 6. As with all tests you write, strive for a test name that summarizes what
Line 265: the test verifies. Here’s a wacky idea: have the test name complete a sentence
Line 266: about the behavior it describes.
Line 267: A Credit History…with no credit ratings…has a 0 mean
Line 268: Your test describes a credit history object in a certain context—it has no
Line 269: credit ratings. You expect something to hold true about that credit history in
Line 270: that context: it has a zero mean. Your test name is a concise representation
Line 271: of that context and expected outcome:
Line 272: ACreditHistory ... withNoCreditRatingsHas0Mean() { }
Line 273: Was that a snort? No, you don’t have to follow this test class naming conven-
Line 274: tion, but it’s as valid as any other. You’ll read about alternative naming
Line 275: schemes at Documenting Your Tests with Consistent Names, on page 190.
Line 276: On to the body of the code—where the work gets done. Your test first creates a
Line 277: CreditHistory instance (line 7). This new object allows your test to run from a clean
Line 278: slate, keeping it isolated from the effects of other tests. JUnit helps reinforce
Line 279: such isolation by creating a new instance of the test class—ACreditHistory—for
Line 280: each test it executes.
Line 281: Your test next (at line 8) interacts with the CreditHistory test instance to exercise
Line 282: the behavior that you want to verify. Here, you call its arithmeticMean method
Line 283: and capture the return value in result.
Line 284: Your test finally (at line 9) asserts that the expected (desired) result of 0
Line 285: matches the actual result captured.
Line 286: Your call to assertEquals uses JUnit’s bread-and-butter assertion method, which
Line 287: compares a result with what you expect. The majority of your tests will use
Line 288: assertEquals. The rest will use one of many other assert forms that you’ll learn
Line 289: in Chapter 5, Examining Outcomes with Assertions, on page 99.
Line 290: An assertEquals method call passes if its two arguments match each other. It
Line 291: fails if the two arguments do not match. The test method as a whole fails if
Line 292: it encounters any assertion failures.
Line 293: The hard part about learning assertEquals is remembering the correct order of
Line 294: its arguments. The value your test expects comes first; the actual value
Line 295: Chapter 1. Building Your First JUnit Test • 10
Line 296: report erratum  •  discuss
Line 297: 
Line 298: --- 페이지 32 ---
Line 299: returned by the system you’re testing second. The signature for assertEquals
Line 300: makes the order clear. If you ever forget, use your IDE to show it to you:
Line 301: public static void assertEquals(int expected, int actual)
Line 302: When you run your test, you’ll see why the order for expected and actual
Line 303: arguments matters. You’ll do that in the forthcoming section, Making It Fail,
Line 304: on page 14. Stick around!
Line 305: Dealing with Failure
Line 306: You previously learned to click on the little JUnit run icon next to the class
Line 307: declaration to execute all its tests. But you’re going to be running tests quite
Line 308: often—potentially hundreds of times per day, and mousing about is a much
Line 309: slower, labor-intensive process. It behooves you to be more efficient. Repetitive
Line 310: stress injuries are real and unpleasant.
Line 311: Any good IDE will show you the appropriate keyboard shortcut when you
Line 312: hover over a button. Hovering over the JUnit “run” button reveals Ctrl-Shift-R
Line 313: as the appropriate shortcut in my IDE. Hover over yours. Write down the
Line 314: shortcut it provides. Press it and run your tests. Press it again. And again.
Line 315: And remember it. And from here on out, for the thousands of times you will
Line 316: ultimately need to run your tests, use the keyboard. You’ll go faster, and your
Line 317: tendons will thank you.
Line 318: Your test is failing. Your JUnit execution should look similar to the following
Line 319: figure.
Line 320: report erratum  •  discuss
Line 321: Dealing with Failure • 11
Line 322: 
Line 323: --- 페이지 33 ---
Line 324: This information-rich view contains several pieces of information about your
Line 325: test’s failing execution:
Line 326: 1.
Line 327: The JUnit panel to the left, which gives you a hierarchical listing of the
Line 328: tests executed, marks both the test class name ACreditHistory and the test
Line 329: method name withNoCreditRatingsHas0Mean with a yellow x. You can click on
Line 330: that test method name to focus on its execution details.
Line 331: 2.
Line 332: The JUnit panel to the right gets to the point with a statistical summary:
Line 333: Tests failed: 1 of 1 test That is, JUnit executed one test, and that sole test
Line 334: failed.
Line 335: 3.
Line 336: Below that redundantly phrased summary, JUnit shows the gory execution
Line 337: details for the test. The failure left behind an exception stack trace that
Line 338: tells you the test barfed before even reaching its assertion statement.
Line 339: 4.
Line 340: The stack trace screams at you in red text—the favored color of items
Line 341: designed to alert, like errors, stop signs, and poisoned lipstick. You have
Line 342: a divide-by-zero problem. The stack trace is linked to appropriate lines
Line 343: in the source, which allows you to quickly navigate to the offending code:
Line 344: public int arithmeticMean() {
Line 345: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 346: return total / ratings.size(); // oops!
Line 347: }
Line 348: Your test added no credit ratings to the CreditHistory. As a result, ratings.size()
Line 349: returns a 0, and Java throws an ArithmeticException as its way of telling you it
Line 350: wants nothing to do with that sort of division. Oops!
Line 351: Your exception-throwing test reveals another useful JUnit nugget: if code
Line 352: executed in a test run throws an exception that’s not caught, that counts as
Line 353: a failing test.
Line 354: Fixing the Problem
Line 355: The unit test did its job: it notified you of a problem. Earlier, you decided that
Line 356: it’s possible someone could call arithmeticMean before any credit ratings are
Line 357: added. You also decided that you don’t want the code to throw an exception
Line 358: in that case; you instead want it to return a 0. The unit test captures and
Line 359: documents your choice.
Line 360: Your unit test will continue to protect you from future regressions, letting
Line 361: you know anytime the behavior of arithmeticMean changes.
Line 362: To get the failing test to pass—to fix your problem—add a guard clause to the
Line 363: arithmeticMean method in CreditHistory:
Line 364: Chapter 1. Building Your First JUnit Test • 12
Line 365: report erratum  •  discuss
Line 366: 
Line 367: --- 페이지 34 ---
Line 368: utj3-credit-history/03/src/main/java/credit/CreditHistory.java
Line 369: public int arithmeticMean() {
Line 370: if (ratings.isEmpty()) return 0;
Line 371: ➤
Line 372: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 373: return total / ratings.size();
Line 374: }
Line 375: Run the tests again to see if your change did the trick. This time, kick them
Line 376: off by using the Project view (usually the upper-left-most tool window in IDEA
Line 377: and other IDEs). Drill down from the project at its top level until you can
Line 378: select the test/java directory, as shown in this figure:
Line 379: A right-click brings up a near-freakishly large context menu:
Line 380: Select the option Run ’All Tests’. JUnit will execute all the tests within
Line 381: src/test/java. Success! Here’s the passing test (as shown in the figure on page
Line 382: 14), where everything is a glorious green and devoid of stack trace statements.
Line 383: Looks good, right? Feels good, right? Go ahead and hit that Ctrl-Shift-R
Line 384: keystroke (or its equivalent on your machine) to run the test again. Bask in
Line 385: the glory.
Line 386: report erratum  •  discuss
Line 387: Dealing with Failure • 13
Line 388: 
Line 389: --- 페이지 35 ---
Line 390: Moving On to a One-Based Test: Something’s Happening!
Line 391: Your zero-based test saved your bacon. Maybe a one-based test can do the
Line 392: same? Write a test that adds one and only one credit score:
Line 393: utj3-credit-history/04/src/test/java/credit/ACreditHistory.java
Line 394: @Test
Line 395: void withOneRatingHasEquivalentMean() {
Line 396: var creditHistory = new CreditHistory();
Line 397: creditHistory.add(new CreditRating(780));
Line 398: var result = creditHistory.arithmeticMean();
Line 399: assertEquals(780, result);
Line 400: }
Line 401: You might have quickly put that test in place by duplicating the zero-based
Line 402: test, adding a line to call creditHistory.add(), and changing the assertion.
Line 403: Your new test passes. Are you done with it? No. Two critical steps remain:
Line 404: 1.
Line 405: Ensure you’ve seen it fail.
Line 406: 2.
Line 407: Clean it up.
Line 408: Making It Fail
Line 409: If you’ve never seen a test fail for the right reason, don’t trust it.
Line 410: The test you just wrote contains an assertion that expects arithmeticMean to
Line 411: return a specific value. “Failing for right reason” for this example would mean
Line 412: that arithmeticMean returns some value other than 780 (the expected value).
Line 413: Perhaps the calculation is incorrect, or perhaps the code never makes the
Line 414: calculation and returns some initial value.
Line 415: You want to break your code so that the test fails. When it fails, ensure that
Line 416: the failure message JUnit provides makes sense. Let’s try that.
Line 417: Chapter 1. Building Your First JUnit Test • 14
Line 418: report erratum  •  discuss
Line 419: 
Line 420: --- 페이지 36 ---
Line 421: utj3-credit-history/05/src/main/java/credit/CreditHistory.java
Line 422: public void add(CreditRating rating) {
Line 423: //
Line 424: ratings.add(rating);
Line 425: ➤
Line 426: }
Line 427: public int arithmeticMean() {
Line 428: if (ratings.isEmpty()) return 0;
Line 429: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 430: return total / ratings.size();
Line 431: }
Line 432: The best way to break things is to comment out the line of code that adds to
Line 433: the credit history’s ratings collection. Then, rerun the tests (using your new
Line 434: keyboard shortcut!). JUnit should now look like the following figure.
Line 435: The JUnit process output on the right shows an exception stack trace. Behind
Line 436: the scenes, the code in JUnit’s assertEquals method compares the expected value
Line 437: with the actual value. If they are the same, JUnit returns control to the test,
Line 438: allowing it to proceed. If the expected value differs from the actual value, JUnit
Line 439: throws an AssertionFailedError with some useful information attached to it.
Line 440: Here’s your test again, with the pertinent assertEquals method call highlighted.
Line 441: utj3-credit-history/05/src/test/java/credit/ACreditHistory.java
Line 442: @Test
Line 443: void withOneRatingHasEquivalentMean() {
Line 444: var creditHistory = new CreditHistory();
Line 445: creditHistory.add(new CreditRating(780));
Line 446: var result = creditHistory.arithmeticMean();
Line 447: assertEquals(780, result);
Line 448: ➤
Line 449: }
Line 450: In other words, the assertion compares 780 against the value of result from
Line 451: the prior step. The message associated with the stack trace describes the
Line 452: comparison failure:
Line 453: Expected :780 Actual :0
Line 454: report erratum  •  discuss
Line 455: Moving On to a One-Based Test: Something’s Happening! • 15
Line 456: 
Line 457: --- 페이지 37 ---
Line 458: If you’d mistakenly swapped the order of the arguments to assertEquals, like
Line 459: this:
Line 460: assertEquals(result, 780);
Line 461: …then JUnit’s error message would be inaccurate and confusing:
Line 462: Expected :0 Actual :780
Line 463: Your single-rating test doesn’t expect 0; it expects 780. The 0 is the actual
Line 464: result emanating from the call to arithmeticMean, not 780.
Line 465: You did see the test fail due to the assertEquals mismatch, so that’s a good thing.
Line 466: Had you seen something different, it would be a reason to stop and investi-
Line 467: gate—something is probably wrong with the test in this case. If the test run
Line 468: shows an exception emanating from the production code, perhaps something
Line 469: isn’t set up correctly in the test case. If the test run passes, perhaps your
Line 470: test isn’t really doing what you think it is. You’d want to carefully re-read
Line 471: the test to see what you’re missing or misrepresenting.
Line 472: Deliberately fail your tests to prove they’re really doing something.
Line 473: Corollary: Don’t trust a test you’ve never seen fail.
Line 474: It might seem easier to get a new test to fail by changing its assertion. For
Line 475: example, you might change your assertion to assertEquals(result, 9999), which you
Line 476: know would always result in a failing test.
Line 477: But think of your tests as “documents of record” for each logical requirement.
Line 478: Prefer failing the test by changing the production code so that it no longer
Line 479: meets the requirement, not by altering the conditions of the test. It can require
Line 480: just a little more thought, but breaking production code will keep you out of
Line 481: trouble.
Line 482: Programmers following the practice of test-driven development (TDD) always
Line 483: demonstrate test failure first to demonstrate that the code they write is
Line 484: responsible for making the test pass. See Chapter 11, Advancing with Test-
Line 485: Driven Development (TDD), on page 211 for more on how TDD practitioners
Line 486: build a cycle around this discipline.
Line 487: JUnit’s Exceptions
Line 488: You can click the link of the first line in the stack trace to navigate precisely
Line 489: to the point where the exception emanated from the code—the assertEquals call.
Line 490: Chapter 1. Building Your First JUnit Test • 16
Line 491: report erratum  •  discuss
Line 492: 
Line 493: --- 페이지 38 ---
Line 494: (If you want to see the relevant execution path through JUnit’s code itself,
Line 495: you can also click where JUnit says <6 internal lines>.)
Line 496: All failed asserts throw an AssertionFailedError exception. JUnit catches this or
Line 497: any other exception thrown during test execution and adds one to its count
Line 498: of failing tests.
Line 499: JUnit’s choice to throw an exception means no more code in the test method
Line 500: gets executed. Any assertions following the first failing one also do not execute,
Line 501: a deliberate (and good) choice by its designers: Once your first assertion fails,
Line 502: all bets are off about the state of things. Executing subsequent assertions
Line 503: may be pointless.
Line 504: You generally want your tests focused on a single (unit) behavior, which means,
Line 505: usually, you need only one assertion anyway. You’ll dig deeper into this idea
Line 506: later in Test Smell: Multiple Assertions, on page 200.
Line 507: Your probe to watch the test fail involved commenting out a line of code. You
Line 508: can now uncomment it and watch your test pass again, which should give
Line 509: you high confidence that your test properly demonstrates the right piece of
Line 510: behavior.
Line 511: No More Screenshots
Line 512: At this point, you’ve graduated…from screenshots! Now that you’ve seen what
Line 513: to expect in an IDE, you can move forward with learning about unit tests
Line 514: through raw Java code, presented au naturel rather than cloaked in screen-
Line 515: shots. Much sleeker, much sexier.
Line 516: You’ll want to continue to increase your understanding of your IDE’s imple-
Line 517: mentation of JUnit. Try clicking on its various buttons and menus to learn
Line 518: more about its shortcuts and power.
Line 519: Going forward in this book, you’ll mostly see only the code pertinent to the
Line 520: current discussion (rather than large listings). Minimizing your need to flip
Line 521: about through the book to find code listings should help you keep your focus
Line 522: on the relevant code and discussion at hand.
Line 523: Increasing Your ROI: Cleaning Up Tests
Line 524: Always review your tests for opportunities to improve their readability. A few
Line 525: minutes of cleanup now can save countless developers from far more head-
Line 526: scratching time down the road.
Line 527: Review your CreditHistory test. See if you can spot ways to improve things.
Line 528: report erratum  •  discuss
Line 529: Increasing Your ROI: Cleaning Up Tests • 17
Line 530: 
Line 531: --- 페이지 39 ---
Line 532: Scannability: Arrange—Act—Assert
Line 533: With but four lines, your test is already a mass of code demanding close
Line 534: attention:
Line 535: utj3-credit-history/06/src/test/java/credit/ACreditHistory.java
Line 536: @Test
Line 537: void withOneRatingHasEquivalentMean() {
Line 538: var creditHistory = new CreditHistory();
Line 539: creditHistory.add(new CreditRating(780));
Line 540: var result = creditHistory.arithmeticMean();
Line 541: assertEquals(780, result);
Line 542: }
Line 543: The test has little scannability (as Mike Hill calls it)—the ability to quickly
Line 544: locate and comprehend code without having to explicitly read it.
Line 545: 3 Someone
Line 546: wanting a quick understanding must scrutinize each of its four lines from
Line 547: top to bottom. This is the opposite of scannable, something I call stepwise.
Line 548: Lines of stepwise code are the opposite of declarative. They’re strongly linked
Line 549: to earlier steps, and reading one step alone often provides you with no useful
Line 550: information. Its intertwining of implementation details further compels you
Line 551: to slow down, lest you miss something.
Line 552: The four stepwise lines here don’t seem that terrible, but the problem definitely
Line 553: adds up—imagine thousands of similarly tedious tests.
Line 554: Every test you write can be broken down into up to three steps. In order:
Line 555: • Arrange the system so that it’s in a useful state. This set-up step usually
Line 556: involves creating objects and calling methods or setting data on them.
Line 557: Your test arranges state by creating a CreditHistory object and adding a
Line 558: credit rating to it. The first part of your test name, withOneRating, echoes
Line 559: this state arrangement. Some tests won’t have any arrange needs (for
Line 560: example, when you’re making a static method call with literal or no
Line 561: arguments).
Line 562: • Act upon the system so as to create the behavior you’re trying to test.
Line 563: Your test acts on the credit history object by calling its arithmeticMean
Line 564: method.
Line 565: • Assert (verify) that the system behaves the way you expect. Your test
Line 566: asserts that the arithmeticMean is calculated correctly.
Line 567: 3.
Line 568: https://www.geepawhill.org/2020/03/03/readability-and-scannability/.
Line 569: Chapter 1. Building Your First JUnit Test • 18
Line 570: report erratum  •  discuss
Line 571: 
Line 572: --- 페이지 40 ---
Line 573: Some of your tests will be functionally oriented, in which you invoke a method
Line 574: that returns a value. For these tests, you can often distill the three Arrange-
Line 575: Act-Assert (AAA) steps to a single line of test code:
Line 576: assertEquals(42, new Everything().ultimateAnswer());
Line 577: To make your tests align with at least one aspect of scannable, use blank
Line 578: lines to break them into AAA chunks:
Line 579: utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
Line 580: @Test
Line 581: void withOneRatingHasEquivalentMean() {
Line 582: var creditHistory = new CreditHistory();
Line 583: creditHistory.add(new CreditRating(780));
Line 584: var result = creditHistory.arithmeticMean();
Line 585: assertEquals(780, result);
Line 586: }
Line 587: Your test code now has some breathing room. AAA has the same effect as
Line 588: using paragraphs to break up a page of continuous text.
Line 589: If all of your tests are similarly consistent, both organizationally and visually,
Line 590: a developer’s eyes can immediately settle on the test part they’re most inter-
Line 591: ested in. That consistency alone can significantly reduce the time anyone
Line 592: must otherwise spend reading through any given test.
Line 593: Test comprehension starts with reading its name. A well-named test summa-
Line 594: rizes the behavior that the example (the test code itself) demonstrates. You’ll
Line 595: learn more about improving your test names in Tests as Documentation, on
Line 596: page 189.
Line 597: Once you learn the test’s intent through its name, you might next look at the
Line 598: act step. It will tell you how the test interacts with the system to trigger
Line 599: the behavior described by the test name.
Line 600: Then, read the arrange step to see how the system gets into the proper state
Line 601: to be tested. Or, if you already know (or don’t care) how things are arranged,
Line 602: focus instead on the assert step to see how the test verifies that the desired
Line 603: behavior occurred.
Line 604: Ultimately, only you will know what parts of a test you need to focus on, and
Line 605: that interest will change from time to time. For example, if you must add a
Line 606: new behavior related to an existing one, you’ll probably focus heavily on the
Line 607: arrange of the related test to understand how it sets up state. If you’re instead
Line 608: report erratum  •  discuss
Line 609: Increasing Your ROI: Cleaning Up Tests • 19
Line 610: 
Line 611: --- 페이지 41 ---
Line 612: trying to understand a specific behavior, you’ll want to focus on how its test’s
Line 613: arrange steps correlate with the expected result expressed in the assert step.
Line 614: Quickly finding what you need is a key component of increasing your devel-
Line 615: opment speed, and a large part of succeeding is related to scannability.
Line 616: Follow Bill Wake’s AAA mnemonic
Line 617: 4 and consistently (visually)
Line 618: chunk your tests as a valuable means of improving scannability.
Line 619: Abstraction: Eliminating Boring Details
Line 620: After chunking both tests using the Arrange—Act—Assert (AAA) pattern, your
Line 621: tests are more scannable:
Line 622: utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
Line 623: @Test
Line 624: void withOneRatingHasEquivalentMean() {
Line 625: var creditHistory = new CreditHistory();
Line 626: creditHistory.add(new CreditRating(780));
Line 627: var result = creditHistory.arithmeticMean();
Line 628: assertEquals(780, result);
Line 629: }
Line 630: But note that both tests repeat the same uninteresting line of code that creates
Line 631: a CreditHistory instance:
Line 632: utj3-credit-history/07/src/test/java/credit/ACreditHistory.java
Line 633: var creditHistory = new CreditHistory();
Line 634: That line of code is, of course, necessary for each test to successfully execute,
Line 635: but you really don’t have to see it in order to understand the tests.
Line 636: JUnit provides a hook you can use to move common test initialization into a
Line 637: single place, which at the same time moves it away from the more relevant
Line 638: test code. The @BeforeEach annotation can mark one or more methods to be
Line 639: executed before each and every test.
Line 640: utj3-credit-history/08/src/test/java/credit/ACreditHistory.java
Line 641: import org.junit.jupiter.api.BeforeEach;
Line 642: ➤
Line 643: import org.junit.jupiter.api.Test;
Line 644: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 645: class ACreditHistory {
Line 646: CreditHistory creditHistory;
Line 647: ➤
Line 648: 4.
Line 649: https://xp123.com/3a-arrange-act-assert/
Line 650: Chapter 1. Building Your First JUnit Test • 20
Line 651: report erratum  •  discuss
Line 652: 
Line 653: --- 페이지 42 ---
Line 654: @BeforeEach
Line 655: ➤
Line 656: void createInstance() {
Line 657: ➤
Line 658: creditHistory = new CreditHistory();
Line 659: ➤
Line 660: }
Line 661: ➤
Line 662: @Test
Line 663: void withNoCreditRatingsHas0Mean() {
Line 664: var result = creditHistory.arithmeticMean();
Line 665: assertEquals(0, result);
Line 666: }
Line 667: @Test
Line 668: void withOneRatingHasEquivalentMean() {
Line 669: creditHistory.add(new CreditRating(780));
Line 670: var result = creditHistory.arithmeticMean();
Line 671: assertEquals(780, result);
Line 672: }
Line 673: }
Line 674: The highlighted lines show a typical use for the @BeforeEach hook. The test declares
Line 675: a field named creditHistory and then initializes it in the annotated createInstance
Line 676: method. That allows you to remove the local initializations of creditHistory from
Line 677: both tests.
Line 678: Here’s how things happen when JUnit runs these two tests in ACreditHistory:
Line 679: 1.
Line 680: JUnit creates a new instance of ACreditHistory.
Line 681: 2.
Line 682: JUnit executes the createInstance method on this instance, which initializes
Line 683: the creditHistory field.
Line 684: 3.
Line 685: JUnit executes one of either withNoCreditRatingsHas0Mean or withOneRatingHas-
Line 686: EquivalentMean, depending on how Java returns the methods declared on a
Line 687: class. In other words, they don’t run in an order you can depend on.
Line 688: That’s okay. You want each test to stand completely on its own and not
Line 689: care about the order in which it’s executed.
Line 690: 4.
Line 691: JUnit creates a new instance of ACreditHistory.
Line 692: 5.
Line 693: JUnit executes the createInstance method on this instance.
Line 694: 6.
Line 695: JUnit executes the other test, the one not already run.
Line 696: Still fuzzy? Understandable. Put a System.out.println() call in the @BeforeEach hook,
Line 697: as well as in each of the two tests. Also, create a no-arg constructor and put
Line 698: a System.out.println() statement in that. Then run your tests; the output should
Line 699: jibe with the preceding list—you should see six println lines.
Line 700: report erratum  •  discuss
Line 701: Increasing Your ROI: Cleaning Up Tests • 21
Line 702: 
Line 703: --- 페이지 43 ---
Line 704: I just heard you say, “Big deal.” Yep, you have removed a measly line from a
Line 705: couple of tests, but you have actually introduced more total lines in the
Line 706: source file.
Line 707: The remaining tests are now as immediate and scannable as possible. Each
Line 708: AAA chunk is one line. You can visually scan past boring initialization code
Line 709: and instead focus on exactly what arrangement is needed to achieve the
Line 710: desired outcome. You can more quickly correlate the arrange and act steps
Line 711: and answer the question, “Why does this assertion pass?”
Line 712: Your tests are highly abstract: They emphasize and document what’s relevant
Line 713: in each test and de-emphasize necessary but boring details.
Line 714: Most of your tests can be this concise, with a typical range from one to five
Line 715: statements. They’ll be easier to write in the first place, easier to understand
Line 716: (and don’t forget, “write once, read many”), and easier to change when
Line 717: requirements change. You’ll find additional tips for keeping tests short and
Line 718: meaningful in Chapter 5, Examining Outcomes with Assertions, on page 99.
Line 719: Eliminating Clutter and JUnit 5
Line 720: Your test code may appear to violate longstanding Java conventions. Neither
Line 721: the class nor the test method signatures declare explicit modifiers. Older
Line 722: versions of JUnit did require the public modifier. In JUnit 5, classes and
Line 723: methods should have package-level access.
Line 724: Omitting the extra keyword goes one more step toward emphasizing the
Line 725: abstraction of tests by eliminating one more bit of clutter. Your tests move
Line 726: in the direction of documentation and away from implementation details. They
Line 727: describe behaviors.
Line 728: In a similar vein, you can omit the typical access modifier of private for fields.
Line 729: If you’re worried, don’t be. None of your code will ever call test methods, and
Line 730: no one will violate their “exposed” fields.
Line 731: ZOM: Zero and One Done, Now Testing Many
Line 732: You’ve written a zero-based test (a test for the “zero” case) and a one-based
Line 733: test so far. It’s time to slam out a many-based test:
Line 734: utj3-credit-history/09/src/test/java/credit/ACreditHistory.java
Line 735: @Test
Line 736: void withMultipleRatingsDividesTotalByCount() {
Line 737: creditHistory.add(new CreditRating(780));
Line 738: creditHistory.add(new CreditRating(800));
Line 739: creditHistory.add(new CreditRating(820));
Line 740: Chapter 1. Building Your First JUnit Test • 22
Line 741: report erratum  •  discuss
Line 742: 
Line 743: --- 페이지 44 ---
Line 744: var result = creditHistory.arithmeticMean();
Line 745: assertEquals(800, result);
Line 746: }
Line 747: You can create this test by copying the one-based test, duplicating a couple
Line 748: of lines in order to add a total of three credit ratings, and changing the
Line 749: expected value for the assertion. It should pass. Break it; it should fail. Fix
Line 750: it again and demonstrate that it passes. It’s possible to do all of that within
Line 751: a total of about two minutes.
Line 752: You might wonder if you need all three tests. The one-based test really doesn’t
Line 753: differ much from the many-based test, and they don’t execute anything differ-
Line 754: ently with respect to code paths. It’s a debatable point, and ultimately, it’s
Line 755: up to you.
Line 756: Prefer deleting tests that don’t add any value in terms of “documenting variant
Line 757: behaviors.” It was still useful for you to build tests using a zero-one-many
Line 758: (ZOM) progression, and it really didn’t take any significant additional time to
Line 759: write all three tests. If you buy that, you should have no qualms about
Line 760: deleting the one-based test.
Line 761: Delete it! Doing so allows you to simplify the test name: withMultipleRatingsDivides-
Line 762: TotalByCount. Here’s your final test class:
Line 763: utj3-credit-history/10/src/test/java/credit/ACreditHistory.java
Line 764: import org.junit.jupiter.api.BeforeEach;
Line 765: import org.junit.jupiter.api.Test;
Line 766: import java.time.LocalDate;
Line 767: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 768: class ACreditHistory {
Line 769: CreditHistory creditHistory;
Line 770: @BeforeEach
Line 771: void createInstance() {
Line 772: creditHistory = new CreditHistory();
Line 773: }
Line 774: @Test
Line 775: void withNoCreditRatingsHas0Mean() {
Line 776: var result = creditHistory.arithmeticMean();
Line 777: assertEquals(0, result);
Line 778: }
Line 779: @Test
Line 780: void withRatingsDividesTotalByCount() {
Line 781: ➤
Line 782: creditHistory.add(new CreditRating(780));
Line 783: creditHistory.add(new CreditRating(800));
Line 784: creditHistory.add(new CreditRating(820));
Line 785: report erratum  •  discuss
Line 786: ZOM: Zero and One Done, Now Testing Many • 23
Line 787: 
Line 788: --- 페이지 45 ---
Line 789: var result = creditHistory.arithmeticMean();
Line 790: assertEquals(800, result);
Line 791: }
Line 792: }
Line 793: Always consider writing a test for each of Zero, One, and Many
Line 794: (ZOM) cases.
Line 795: Covering Other Cases: Creating a Test List
Line 796: Beyond the ZOM cases you’ve covered, you could brainstorm edge cases and
Line 797: exception-based tests. You’ll explore doing that in later chapters.
Line 798: As you write tests and continue to re-visit/re-read the code you’re testing,
Line 799: you’ll think of additional tests you should write. In fact, as you write the code
Line 800: yourself in the first place—before trying to write tests for it—think about and
Line 801: note the cases you’ll need for that code.
Line 802: Add the cases you think of to a test list to remember to write them. Cross
Line 803: them off as you implement or obviate them. You can do this on paper, in a
Line 804: notepad file, or even in the test class itself as a series of comments. (Perhaps
Line 805: in the form of TODO comments, which IDEs like IntelliJ IDEA and Eclipse will
Line 806: collect in a view as a set of reminders.) Things change, so don’t expend the
Line 807: effort to code these tests just yet. You can read more on this highly useful
Line 808: tool in Kent Beck’s seminal book on TDD [Bec02].
Line 809: Congratulations!…But Don’t Stop Yet
Line 810: In this chapter, you got past one of the more significant challenges: getting
Line 811: a first test to pass using JUnit in your IDE. Congrats! Along with that
Line 812: achievement, you also learned:
Line 813: • What it takes to write a test that JUnit can accept and run
Line 814: • How to tell JUnit to run your tests
Line 815: • How to interpret the test results provided by JUnit
Line 816: • How to use the ZOM mnemonic to figure out what the next test might be
Line 817: • How to structure a test using AAA
Line 818: You’ve been reading about “units” throughout this chapter. Next up, you’ll
Line 819: learn what a unit is, and you’ll learn a number of tactics for testing some of
Line 820: the common units that you’ll encounter.
Line 821: Chapter 1. Building Your First JUnit Test • 24
Line 822: report erratum  •  discuss