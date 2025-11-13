# 7.1 Testing Habits: What Tests to Run (pp.135-137)

---
**Page 135**

CHAPTER 7
Executing JUnit Tests
You learned about assertions, test organization, and the JUnit lifecycle of
execution earlier in this part of the book.
Having all the tests in the world is useless if you never run them. You’ll want
to run tests often as you build software on your own machine like you’ve been
doing so far. But you’ll also want to run them as part of the process of vetting
integrated software before deploying it, perhaps as part of a continuous build
process.
In this chapter, you’ll learn “when,” “what,” and more of the “how” of running
tests:
• What set of unit tests you’ll want to run when executing JUnit
• Grouping tests using the JUnit @Tag annotation, which allows you to
execute arbitrary groups of tests
• Temporarily not running your tests using the @Disabled annotation
Testing Habits: What Tests to Run
Full-fledged Java IDEs (for example, IntelliJ IDEA or Eclipse) have built-in
support for JUnit. Out of the box, you can load a project, click on its test
directory, and execute tests without having to configure anything. You saw
in Chapter 1, Building Your First JUnit Test, on page 3 at least a couple of
ways to run JUnit tests from within IntelliJ IDEA. In the following sections,
you’ll see how the number of tests you run affects your results.
Run All the Tests
If your tests are fast (see Fast Tests, on page 66), it’s possible to run thousands
of unit tests within a few seconds. When you have fast tests, you can run all
report erratum  •  discuss


---
**Page 136**

of them with every tiny change. If you broke something elsewhere in the
codebase, you’ll know it immediately. Fast tests provide an awe-inspiring
power-up.
Run as Many Tests as You Can Stand
IDEA and other IDEs make it easy to choose the opposite of running every-
thing, which is to run only one test at a time. IDEA, for example, provides a
small “play” icon button to the left of each test method.
Suppose you’re adding a test named issuesSMSAlertOnWithdrawal to the test class
AFundedAccount. The problem with running only issuesSMSAlertOnWithdrawal is that
it’s surrounded by a number of other tests in AFundedAccount that verify poten-
tially related behaviors in the Account production class. As you start changing
Account to support the new SMS alert behavior, it’s possible to break these
other Account behaviors.
You want to know the moment you break other code. In general, the longer you
go without feedback that you’ve broken things, the longer it will take you to
find and fix things. Piling more code around defective code starts to obscure
problems and can also make it harder to fix due to the amount of entanglement.
A key value of your unit tests is fast feedback. The only way to get that feed-
back, though, is to actually run the darn things.
Fortunately, you’re learning to design your tests to be fast. It might not be
reasonable to run all your tests because they take more than a few seconds,
but it had better be reasonable to run all the tests in, say, AFundedAccount. Your
IDE should make it easy to run all tests in a single class. With JUnit, you
can also group subsets of related tests using nested classes (see Organizing
Related Tests into Nested Classes, on page 126).
If running all of a class’s tests takes too long, fix the problem before it gets
worse and wastes even more time. The fix might involve some redesign. You
might extract some slower, integration-style tests from an otherwise fast
test class. Or, you might introduce mock objects (see Chapter 3, Using Test
Doubles, on page 53) to transform slow tests into fast tests. Or, more dramat-
ically, you might fix the unfortunate dependencies in your production class
that foster slow tests.
It’s possible for changes in one class to break tests for other classes. Behavior
in Account, for example, is verified by tests in AnAccount and AFundedAccount. If all
potentially impacted test classes are in the same package, take a step up and
Chapter 7. Executing JUnit Tests • 136
report erratum  •  discuss


---
**Page 137**

run all the tests within that package. If it’s too slow to run all the tests in a
package, I have the same blunt advice: fix the problem.
Run as many tests as you can stand, as often as you can stand.
If you habituate to running one test at a time, you’ll eventually discover defects
elsewhere later than you should. About the only time you should run a single
test is if you’re struggling to get it to pass and find yourself in debugging mode
or using System.out.println statements to trace what’s going on. At that point,
running multiple tests will make it difficult to focus on the problematic one.
Creating Arbitrary Test Groups Using Tags
JUnit 5 lets you mark a test class or a test method with the @Tag annotation.
You can use these tags as the basis for running arbitrary sets of tests with
JUnit. This is known as filtering your tests.
Let’s take a look at an example. When making changes to the Account class,
you should run all tests in both AnAccount and AFundedAccount. You could run all
the tests in the package containing both these classes, but you can also use
tags to be precise about the subset of tests to run.
Mark both two classes with the @Tag annotation:
utj3-junit/01/src/test/java/tags/AnAccount.java
import org.junit.jupiter.api.Tag;
➤
import org.junit.jupiter.api.Test;
// ...
@Tag("account")
➤
class AnAccount {
// ...
@Test
void withdrawalReducesAccountBalance() {
// ...
}
// ...
}
utj3-junit/01/src/test/java/tags/AnUnfundedAccount.java
import org.junit.jupiter.api.Tag;
➤
import org.junit.jupiter.api.Test;
// ...
report erratum  •  discuss
Creating Arbitrary Test Groups Using Tags • 137


