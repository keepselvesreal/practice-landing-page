# 7.2 Creating Arbitrary Test Groups Using Tags (pp.137-140)

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


