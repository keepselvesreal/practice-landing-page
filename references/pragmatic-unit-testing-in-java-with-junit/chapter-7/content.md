# Executing JUnit Tests (pp.135-147)

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


---
**Page 138**

@Tag("account")
➤
class AnUnfundedAccount {
// ...
@Test
void hasPositiveBalanceAfterInitialDeposit() {
// ...
}
// ...
}
To run the tests in these two tagged classes, you must provide a filter to JUnit.
Your IDE might allow you to do this directly when you run tests. If you’re
using Maven or Gradle, both of these tools provide direct support for specifying
filters. In the worst case, you can run JUnit as a standalone command and
provide the filter at that time.
Visit JUnit’s documentation for running tests for further information
1 on
using tags with Maven, Gradle, or command-line JUnit.
Using Tags in IntelliJ IDEA
With IntelliJ IDEA, you configure how tests are run in the Run/Debug Con-
figurations dialog.
From IDEA’s main menu, access the Run/Debug Configurations dialog by
selecting Run ▶ Edit Configurations. From within the Run/Debug Configura-
tions dialog, add a new configuration by clicking the + button. IDEA provides
a dropdown titled Add New Configuration; select JUnit from its long list of
options.
The dialog defaults to running tests within a single test class; you will need
to change this to tell JUnit to run a tag instead. Within the dialog’s Build and
run section, you should see a dropdown with Class currently selected. Select
instead Tags from this dropdown. In the input field to the right of the drop-
down, type in the text account as the tag to execute. This text should match
the “account” string you specified in your @Tag declarations.
Your dialog should look similar to the figure on page 139.
Specifying utj3-junit as the classpath (-cp) may generate errors.
Ensure you’ve chosen utj3-junit.test.
1.
https://junit.org/junit5/docs/current/user-guide/#running-tests
Chapter 7. Executing JUnit Tests • 138
report erratum  •  discuss


---
**Page 139**

You can now click on Apply and then Run to execute only tests marked with
the “account” tag.
Tag Expressions
IDEA supports tag expressions, which are Boolean expressions that allow
more sophisticated filtering.
In addition to tagging the two account-related test classes, suppose you also
want to run the set of tests related to hot-fixes for discovered defects. You
might have tagged a single test method:
utj3-junit/01/src/test/java/tags/AnInMemoryDatabase.java
import org.junit.jupiter.api.Tag;
➤
import org.junit.jupiter.api.Test;
class AnInMemoryDatabase {
// ...
@Tag("v11.1_defects")
➤
@Test
void objectCopiedWhenAddedToDatabaseFailing() {
// ...
}
// ...
}
report erratum  •  discuss
Creating Arbitrary Test Groups Using Tags • 139


---
**Page 140**

When specifying tags within your run configuration, you can enter the follow-
ing tag expression:
account | v11.1_defects
The | (or) operator indicates that JUnit should run the union of tests tagged
with “account” and tests tagged with “v11_defects.” Specifically, JUnit will
run tests in AnAccount and AnUnfundedAccount, as well as the test named
objectCopiedWhenAddedToDatabaseFailing.
Tag expressions support inverting a filter using the ! (not) operator and running
the intersection of two tags using the & (and) operator. They also allow the
use of parentheses to clarify or force the precedence of the operators.
Overusing Tags
As with anything, heavy use of the tags feature may be a sign that something
else is amiss.
If you find you’ve used more-or-less permanent tag names (like account), try
reorganizing your production and/or test code to eliminate the need for the
tag. You might extract a new package, move classes around, move test
methods to other classes, and so on. Within a single test class, use a @Nested
class to collect a focused set of tests related to a single concept (“withdrawal”).
Temporarily Disabling Tests with @Disabled
Occasionally, you’ll want to keep a specific test from getting executed, usually
because it’s failing. Maybe you don’t have the time to fix it at the moment
and want to focus on getting other tests to pass first—during which time,
other test failures will be a distraction.
You might have other legitimate reasons to avoid running a certain test.
Maybe you’re waiting on an answer from the business about a specific
unit behavior.
You can temporarily comment out tests, of course, but the better answer is
to mark the test methods in question with the @Disabled annotation. JUnit will
bypass executing any such marked test methods. You can similarly mark a
test class as @Disabled, in which case JUnit will run none of its test methods.
Using @Disabled is a better way of bypassing tests because JUnit can remind
you that some tests await your revisit. JUnit can’t remind you if you comment
out tests, in which case your tests may remain forever in limbo. (That’s one
way to break a test’s back.)
Chapter 7. Executing JUnit Tests • 140
report erratum  •  discuss


---
**Page 141**

utj3-junit/01/src/test/java/scratch/AnUnfundedAccount.java
import org.junit.jupiter.api.Disabled;
➤
import org.junit.jupiter.api.Test;
class AnUnfundedAccount {
@Disabled
➤
@Test
void disallowsWithdrawals() {
// ...
}
@Test
void doesNotAccrueInterest() {
// ... uh oh we need to focus on this test
}
}
The informational string provided to the @Disabled annotation is optional. You
should probably use it to describe why you disabled the test unless you’re
going to remove that annotation in the next few minutes or so.
To be honest, few reasons exist to push up a @Disabled test. One legitimate
reason (been there): “Midnight emergency fix resulted in broken tests. Revisit
tomorrow!” In which case, the following reason might suffice:
@Disabled("broken after emergency fix")
Allowing disabled tests in your integrated codebase is otherwise a bad, bad
process smell.
The JUnit test runner you use, whether it’s built into your IDE or your build
automation tool (Gradle or Maven, for example), should make it clear that
some of your tests are disabled. In the following IntelliJ IDEA test runner,
the test disallowsWithdrawals is marked with a grey “no symbol” (⊘) to indicate it
is disabled:
You’ll appreciate the reminder that you’ve left a test in limbo.
Unfortunately, by default, running your tests at the command line with Gradle
only tells you there are disabled tests if at least one test fails. And you only
see that if you scroll upward through the Gradle output.
report erratum  •  discuss
Temporarily Disabling Tests with @Disabled • 141


---
**Page 142**

Gradle is a great way to build and run tests within a continuous build envi-
ronment. But don’t use Gradle for interactive unit testing unless you customize
its output to remind you of disabled tests. Have it fail the test run if any dis-
abled tests exist or show their count as the last line of output.
Disabled tests should not really exist other than on your own machine. Avoid
integrating disabled tests—they usually represent big questions about the
health of your system, such as these: Is the test really needed? Can we just
delete it? What do we currently understand about why we couldn’t immedi-
ately get this to pass?
Exploring More Features
JUnit has grown over its past 20-something years into a fairly large and
sophisticated tool. It’s likely that the features you’ve learned in this chapter
will be enough for your needs for years to come. However, it’s also possible
that one of JUnit’s other features
2 might be useful for your special circum-
stances. Here’s a quick summary:
Abort execution of a test if an assumption is not met (but
don’t count it as failed).
assumptions
Enable or disable tests conditionally. Conditions can ref-
erence the OS, architecture, Java version, value of a system
property/environment variable, or custom-coded predicates.
conditional test
execution
Rather than show the (typically) camel-cased test name
during a test run, show the contents of a string.
display names
Generate more human-readable test names by transform-
ing the test method names. For example, transform
underscores in test names into spaces.
display name
generators
Generate tests at runtime.
dynamic tests
Run tests concurrently to speed up their execution.
parallel execution
Run a test a specified number of times.
repeated tests
Programmatically declare a filtered collection of tests to
execute.
suites
Write a file-dependent test that executes in the context
of a temporary directory.
temp dir context
Fail a test (or lifecycle method) if its execution time
exceeds a specific duration.
timeouts
2.
https://junit.org/junit5/docs/current/user-guide/
Chapter 7. Executing JUnit Tests • 142
report erratum  •  discuss


---
**Page 143**

Summary
In this and the prior two chapters that dig into JUnit, you learned the bulk
of what you’ll need to know about writing assertions, organizing your tests,
and running your tests.
With this solid foundation for JUnit, you can move on to more important
concerns. In the next part of the book, you’ll focus on tests and their relation-
ship to your system’s design. You’ll refactor your code “in the small” because
you have tests that give you the confidence to do so. You’ll touch on larger
design concepts as well, and you’ll also learn how to design your tests to
increase the return on your investment in them.
report erratum  •  discuss
Summary • 143


---
**Page 145**

Part III
Increasing ROI: Unit Testing and Design
Elevate your unit tests beyond mere logic validation.
In this part, learn how to use your tests to maintain
clean code—both "in the small" and "in the large"—
and document your system’s unit capabilities.


---
**Page 147**

CHAPTER 8
Refactoring to Cleaner Code
In Parts I and II, you dug deep into how to write unit tests and take advantage
of JUnit. In this part, you’ll learn to take advantage of unit tests to help shape
the design of your system, as well as document the numerous unit-level
behavioral choices you’ve made. Your ability to keep your system simpler and
your tests clearer can reduce your development costs considerably.
You’ll start by focusing on design “in the small,” addressing the lack of clarity
and excessive complexity that’s commonplace in most systems. You’ll
accomplish this by learning to refactor—making small, frequent edits to the
code you write. Your design improvements will help reduce the cost of change.
In a clear, well-designed system, it might take seconds to locate a point of
change and understand the surrounding code. In a more typically convoluted
system, the navigation and comprehension tasks often require minutes
instead. Once you’ve understood the code well enough to change it, a well-
designed system might accommodate your change readily. In the convoluted
system, weaving in your changes might take hours.
Convoluted systems can increase your maintenance costs by an
order of magnitude or more.
You can, with relative ease, create systems that embody clean code. In brief,
this describes clean code:
• Concise: It imparts the solution without unnecessary code.
• Clear: It can be directly understood.
report erratum  •  discuss


