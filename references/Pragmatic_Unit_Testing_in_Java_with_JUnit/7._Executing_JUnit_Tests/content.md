Line 1: 
Line 2: --- 페이지 153 ---
Line 3: CHAPTER 7
Line 4: Executing JUnit Tests
Line 5: You learned about assertions, test organization, and the JUnit lifecycle of
Line 6: execution earlier in this part of the book.
Line 7: Having all the tests in the world is useless if you never run them. You’ll want
Line 8: to run tests often as you build software on your own machine like you’ve been
Line 9: doing so far. But you’ll also want to run them as part of the process of vetting
Line 10: integrated software before deploying it, perhaps as part of a continuous build
Line 11: process.
Line 12: In this chapter, you’ll learn “when,” “what,” and more of the “how” of running
Line 13: tests:
Line 14: • What set of unit tests you’ll want to run when executing JUnit
Line 15: • Grouping tests using the JUnit @Tag annotation, which allows you to
Line 16: execute arbitrary groups of tests
Line 17: • Temporarily not running your tests using the @Disabled annotation
Line 18: Testing Habits: What Tests to Run
Line 19: Full-fledged Java IDEs (for example, IntelliJ IDEA or Eclipse) have built-in
Line 20: support for JUnit. Out of the box, you can load a project, click on its test
Line 21: directory, and execute tests without having to configure anything. You saw
Line 22: in Chapter 1, Building Your First JUnit Test, on page 3 at least a couple of
Line 23: ways to run JUnit tests from within IntelliJ IDEA. In the following sections,
Line 24: you’ll see how the number of tests you run affects your results.
Line 25: Run All the Tests
Line 26: If your tests are fast (see Fast Tests, on page 66), it’s possible to run thousands
Line 27: of unit tests within a few seconds. When you have fast tests, you can run all
Line 28: report erratum  •  discuss
Line 29: 
Line 30: --- 페이지 154 ---
Line 31: of them with every tiny change. If you broke something elsewhere in the
Line 32: codebase, you’ll know it immediately. Fast tests provide an awe-inspiring
Line 33: power-up.
Line 34: Run as Many Tests as You Can Stand
Line 35: IDEA and other IDEs make it easy to choose the opposite of running every-
Line 36: thing, which is to run only one test at a time. IDEA, for example, provides a
Line 37: small “play” icon button to the left of each test method.
Line 38: Suppose you’re adding a test named issuesSMSAlertOnWithdrawal to the test class
Line 39: AFundedAccount. The problem with running only issuesSMSAlertOnWithdrawal is that
Line 40: it’s surrounded by a number of other tests in AFundedAccount that verify poten-
Line 41: tially related behaviors in the Account production class. As you start changing
Line 42: Account to support the new SMS alert behavior, it’s possible to break these
Line 43: other Account behaviors.
Line 44: You want to know the moment you break other code. In general, the longer you
Line 45: go without feedback that you’ve broken things, the longer it will take you to
Line 46: find and fix things. Piling more code around defective code starts to obscure
Line 47: problems and can also make it harder to fix due to the amount of entanglement.
Line 48: A key value of your unit tests is fast feedback. The only way to get that feed-
Line 49: back, though, is to actually run the darn things.
Line 50: Fortunately, you’re learning to design your tests to be fast. It might not be
Line 51: reasonable to run all your tests because they take more than a few seconds,
Line 52: but it had better be reasonable to run all the tests in, say, AFundedAccount. Your
Line 53: IDE should make it easy to run all tests in a single class. With JUnit, you
Line 54: can also group subsets of related tests using nested classes (see Organizing
Line 55: Related Tests into Nested Classes, on page 126).
Line 56: If running all of a class’s tests takes too long, fix the problem before it gets
Line 57: worse and wastes even more time. The fix might involve some redesign. You
Line 58: might extract some slower, integration-style tests from an otherwise fast
Line 59: test class. Or, you might introduce mock objects (see Chapter 3, Using Test
Line 60: Doubles, on page 53) to transform slow tests into fast tests. Or, more dramat-
Line 61: ically, you might fix the unfortunate dependencies in your production class
Line 62: that foster slow tests.
Line 63: It’s possible for changes in one class to break tests for other classes. Behavior
Line 64: in Account, for example, is verified by tests in AnAccount and AFundedAccount. If all
Line 65: potentially impacted test classes are in the same package, take a step up and
Line 66: Chapter 7. Executing JUnit Tests • 136
Line 67: report erratum  •  discuss
Line 68: 
Line 69: --- 페이지 155 ---
Line 70: run all the tests within that package. If it’s too slow to run all the tests in a
Line 71: package, I have the same blunt advice: fix the problem.
Line 72: Run as many tests as you can stand, as often as you can stand.
Line 73: If you habituate to running one test at a time, you’ll eventually discover defects
Line 74: elsewhere later than you should. About the only time you should run a single
Line 75: test is if you’re struggling to get it to pass and find yourself in debugging mode
Line 76: or using System.out.println statements to trace what’s going on. At that point,
Line 77: running multiple tests will make it difficult to focus on the problematic one.
Line 78: Creating Arbitrary Test Groups Using Tags
Line 79: JUnit 5 lets you mark a test class or a test method with the @Tag annotation.
Line 80: You can use these tags as the basis for running arbitrary sets of tests with
Line 81: JUnit. This is known as filtering your tests.
Line 82: Let’s take a look at an example. When making changes to the Account class,
Line 83: you should run all tests in both AnAccount and AFundedAccount. You could run all
Line 84: the tests in the package containing both these classes, but you can also use
Line 85: tags to be precise about the subset of tests to run.
Line 86: Mark both two classes with the @Tag annotation:
Line 87: utj3-junit/01/src/test/java/tags/AnAccount.java
Line 88: import org.junit.jupiter.api.Tag;
Line 89: ➤
Line 90: import org.junit.jupiter.api.Test;
Line 91: // ...
Line 92: @Tag("account")
Line 93: ➤
Line 94: class AnAccount {
Line 95: // ...
Line 96: @Test
Line 97: void withdrawalReducesAccountBalance() {
Line 98: // ...
Line 99: }
Line 100: // ...
Line 101: }
Line 102: utj3-junit/01/src/test/java/tags/AnUnfundedAccount.java
Line 103: import org.junit.jupiter.api.Tag;
Line 104: ➤
Line 105: import org.junit.jupiter.api.Test;
Line 106: // ...
Line 107: report erratum  •  discuss
Line 108: Creating Arbitrary Test Groups Using Tags • 137
Line 109: 
Line 110: --- 페이지 156 ---
Line 111: @Tag("account")
Line 112: ➤
Line 113: class AnUnfundedAccount {
Line 114: // ...
Line 115: @Test
Line 116: void hasPositiveBalanceAfterInitialDeposit() {
Line 117: // ...
Line 118: }
Line 119: // ...
Line 120: }
Line 121: To run the tests in these two tagged classes, you must provide a filter to JUnit.
Line 122: Your IDE might allow you to do this directly when you run tests. If you’re
Line 123: using Maven or Gradle, both of these tools provide direct support for specifying
Line 124: filters. In the worst case, you can run JUnit as a standalone command and
Line 125: provide the filter at that time.
Line 126: Visit JUnit’s documentation for running tests for further information
Line 127: 1 on
Line 128: using tags with Maven, Gradle, or command-line JUnit.
Line 129: Using Tags in IntelliJ IDEA
Line 130: With IntelliJ IDEA, you configure how tests are run in the Run/Debug Con-
Line 131: figurations dialog.
Line 132: From IDEA’s main menu, access the Run/Debug Configurations dialog by
Line 133: selecting Run ▶ Edit Configurations. From within the Run/Debug Configura-
Line 134: tions dialog, add a new configuration by clicking the + button. IDEA provides
Line 135: a dropdown titled Add New Configuration; select JUnit from its long list of
Line 136: options.
Line 137: The dialog defaults to running tests within a single test class; you will need
Line 138: to change this to tell JUnit to run a tag instead. Within the dialog’s Build and
Line 139: run section, you should see a dropdown with Class currently selected. Select
Line 140: instead Tags from this dropdown. In the input field to the right of the drop-
Line 141: down, type in the text account as the tag to execute. This text should match
Line 142: the “account” string you specified in your @Tag declarations.
Line 143: Your dialog should look similar to the figure on page 139.
Line 144: Specifying utj3-junit as the classpath (-cp) may generate errors.
Line 145: Ensure you’ve chosen utj3-junit.test.
Line 146: 1.
Line 147: https://junit.org/junit5/docs/current/user-guide/#running-tests
Line 148: Chapter 7. Executing JUnit Tests • 138
Line 149: report erratum  •  discuss
Line 150: 
Line 151: --- 페이지 157 ---
Line 152: You can now click on Apply and then Run to execute only tests marked with
Line 153: the “account” tag.
Line 154: Tag Expressions
Line 155: IDEA supports tag expressions, which are Boolean expressions that allow
Line 156: more sophisticated filtering.
Line 157: In addition to tagging the two account-related test classes, suppose you also
Line 158: want to run the set of tests related to hot-fixes for discovered defects. You
Line 159: might have tagged a single test method:
Line 160: utj3-junit/01/src/test/java/tags/AnInMemoryDatabase.java
Line 161: import org.junit.jupiter.api.Tag;
Line 162: ➤
Line 163: import org.junit.jupiter.api.Test;
Line 164: class AnInMemoryDatabase {
Line 165: // ...
Line 166: @Tag("v11.1_defects")
Line 167: ➤
Line 168: @Test
Line 169: void objectCopiedWhenAddedToDatabaseFailing() {
Line 170: // ...
Line 171: }
Line 172: // ...
Line 173: }
Line 174: report erratum  •  discuss
Line 175: Creating Arbitrary Test Groups Using Tags • 139
Line 176: 
Line 177: --- 페이지 158 ---
Line 178: When specifying tags within your run configuration, you can enter the follow-
Line 179: ing tag expression:
Line 180: account | v11.1_defects
Line 181: The | (or) operator indicates that JUnit should run the union of tests tagged
Line 182: with “account” and tests tagged with “v11_defects.” Specifically, JUnit will
Line 183: run tests in AnAccount and AnUnfundedAccount, as well as the test named
Line 184: objectCopiedWhenAddedToDatabaseFailing.
Line 185: Tag expressions support inverting a filter using the ! (not) operator and running
Line 186: the intersection of two tags using the & (and) operator. They also allow the
Line 187: use of parentheses to clarify or force the precedence of the operators.
Line 188: Overusing Tags
Line 189: As with anything, heavy use of the tags feature may be a sign that something
Line 190: else is amiss.
Line 191: If you find you’ve used more-or-less permanent tag names (like account), try
Line 192: reorganizing your production and/or test code to eliminate the need for the
Line 193: tag. You might extract a new package, move classes around, move test
Line 194: methods to other classes, and so on. Within a single test class, use a @Nested
Line 195: class to collect a focused set of tests related to a single concept (“withdrawal”).
Line 196: Temporarily Disabling Tests with @Disabled
Line 197: Occasionally, you’ll want to keep a specific test from getting executed, usually
Line 198: because it’s failing. Maybe you don’t have the time to fix it at the moment
Line 199: and want to focus on getting other tests to pass first—during which time,
Line 200: other test failures will be a distraction.
Line 201: You might have other legitimate reasons to avoid running a certain test.
Line 202: Maybe you’re waiting on an answer from the business about a specific
Line 203: unit behavior.
Line 204: You can temporarily comment out tests, of course, but the better answer is
Line 205: to mark the test methods in question with the @Disabled annotation. JUnit will
Line 206: bypass executing any such marked test methods. You can similarly mark a
Line 207: test class as @Disabled, in which case JUnit will run none of its test methods.
Line 208: Using @Disabled is a better way of bypassing tests because JUnit can remind
Line 209: you that some tests await your revisit. JUnit can’t remind you if you comment
Line 210: out tests, in which case your tests may remain forever in limbo. (That’s one
Line 211: way to break a test’s back.)
Line 212: Chapter 7. Executing JUnit Tests • 140
Line 213: report erratum  •  discuss
Line 214: 
Line 215: --- 페이지 159 ---
Line 216: utj3-junit/01/src/test/java/scratch/AnUnfundedAccount.java
Line 217: import org.junit.jupiter.api.Disabled;
Line 218: ➤
Line 219: import org.junit.jupiter.api.Test;
Line 220: class AnUnfundedAccount {
Line 221: @Disabled
Line 222: ➤
Line 223: @Test
Line 224: void disallowsWithdrawals() {
Line 225: // ...
Line 226: }
Line 227: @Test
Line 228: void doesNotAccrueInterest() {
Line 229: // ... uh oh we need to focus on this test
Line 230: }
Line 231: }
Line 232: The informational string provided to the @Disabled annotation is optional. You
Line 233: should probably use it to describe why you disabled the test unless you’re
Line 234: going to remove that annotation in the next few minutes or so.
Line 235: To be honest, few reasons exist to push up a @Disabled test. One legitimate
Line 236: reason (been there): “Midnight emergency fix resulted in broken tests. Revisit
Line 237: tomorrow!” In which case, the following reason might suffice:
Line 238: @Disabled("broken after emergency fix")
Line 239: Allowing disabled tests in your integrated codebase is otherwise a bad, bad
Line 240: process smell.
Line 241: The JUnit test runner you use, whether it’s built into your IDE or your build
Line 242: automation tool (Gradle or Maven, for example), should make it clear that
Line 243: some of your tests are disabled. In the following IntelliJ IDEA test runner,
Line 244: the test disallowsWithdrawals is marked with a grey “no symbol” (⊘) to indicate it
Line 245: is disabled:
Line 246: You’ll appreciate the reminder that you’ve left a test in limbo.
Line 247: Unfortunately, by default, running your tests at the command line with Gradle
Line 248: only tells you there are disabled tests if at least one test fails. And you only
Line 249: see that if you scroll upward through the Gradle output.
Line 250: report erratum  •  discuss
Line 251: Temporarily Disabling Tests with @Disabled • 141
Line 252: 
Line 253: --- 페이지 160 ---
Line 254: Gradle is a great way to build and run tests within a continuous build envi-
Line 255: ronment. But don’t use Gradle for interactive unit testing unless you customize
Line 256: its output to remind you of disabled tests. Have it fail the test run if any dis-
Line 257: abled tests exist or show their count as the last line of output.
Line 258: Disabled tests should not really exist other than on your own machine. Avoid
Line 259: integrating disabled tests—they usually represent big questions about the
Line 260: health of your system, such as these: Is the test really needed? Can we just
Line 261: delete it? What do we currently understand about why we couldn’t immedi-
Line 262: ately get this to pass?
Line 263: Exploring More Features
Line 264: JUnit has grown over its past 20-something years into a fairly large and
Line 265: sophisticated tool. It’s likely that the features you’ve learned in this chapter
Line 266: will be enough for your needs for years to come. However, it’s also possible
Line 267: that one of JUnit’s other features
Line 268: 2 might be useful for your special circum-
Line 269: stances. Here’s a quick summary:
Line 270: Abort execution of a test if an assumption is not met (but
Line 271: don’t count it as failed).
Line 272: assumptions
Line 273: Enable or disable tests conditionally. Conditions can ref-
Line 274: erence the OS, architecture, Java version, value of a system
Line 275: property/environment variable, or custom-coded predicates.
Line 276: conditional test
Line 277: execution
Line 278: Rather than show the (typically) camel-cased test name
Line 279: during a test run, show the contents of a string.
Line 280: display names
Line 281: Generate more human-readable test names by transform-
Line 282: ing the test method names. For example, transform
Line 283: underscores in test names into spaces.
Line 284: display name
Line 285: generators
Line 286: Generate tests at runtime.
Line 287: dynamic tests
Line 288: Run tests concurrently to speed up their execution.
Line 289: parallel execution
Line 290: Run a test a specified number of times.
Line 291: repeated tests
Line 292: Programmatically declare a filtered collection of tests to
Line 293: execute.
Line 294: suites
Line 295: Write a file-dependent test that executes in the context
Line 296: of a temporary directory.
Line 297: temp dir context
Line 298: Fail a test (or lifecycle method) if its execution time
Line 299: exceeds a specific duration.
Line 300: timeouts
Line 301: 2.
Line 302: https://junit.org/junit5/docs/current/user-guide/
Line 303: Chapter 7. Executing JUnit Tests • 142
Line 304: report erratum  •  discuss
Line 305: 
Line 306: --- 페이지 161 ---
Line 307: Summary
Line 308: In this and the prior two chapters that dig into JUnit, you learned the bulk
Line 309: of what you’ll need to know about writing assertions, organizing your tests,
Line 310: and running your tests.
Line 311: With this solid foundation for JUnit, you can move on to more important
Line 312: concerns. In the next part of the book, you’ll focus on tests and their relation-
Line 313: ship to your system’s design. You’ll refactor your code “in the small” because
Line 314: you have tests that give you the confidence to do so. You’ll touch on larger
Line 315: design concepts as well, and you’ll also learn how to design your tests to
Line 316: increase the return on your investment in them.
Line 317: report erratum  •  discuss
Line 318: Summary • 143