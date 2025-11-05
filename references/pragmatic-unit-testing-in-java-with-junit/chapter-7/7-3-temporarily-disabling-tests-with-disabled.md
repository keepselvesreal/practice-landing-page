# 7.3 Temporarily Disabling Tests with @Disabled (pp.140-142)

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


