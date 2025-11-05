# 5.0 Introduction [auto-generated] (pp.99-100)

---
**Page 99**

CHAPTER 5
Examining Outcomes with Assertions
You’ve learned the most important features of JUnit in the prior four chapters
of this book, enough to survive but not thrive. Truly succeeding with your
unit testing journey will involve gaining proficiency with your primary tool,
JUnit. In this and the next couple of chapters, you’ll explore JUnit in signifi-
cant detail. First, you’ll focus on JUnit’s means of verification—its assertion
library.
Assertions (or asserts) in JUnit are static method calls that you drop into
your tests. Each assertion is an opportunity to verify that some condition
holds true. If an asserted condition does not hold true, the test stops executing
right there and JUnit reports a test failure.
To abort the test, JUnit throws an exception object of type AssertionFailedError.
If JUnit catches AssertionFailedError, it marks the test as failed. In fact, JUnit
marks any test as failed that throws an exception not caught in the test body.
In order to use the most appropriate assertion for your verification need, you’ll
want to learn about JUnit’s numerous assertion variants.
In examples to this point, you’ve used the two most prevalent assertion forms,
assertTrue and assertEquals. Since you’ll use them for the bulk of your tests, you’ll
first examine these assertion workhorses more deeply. You’ll then move on
to exploring the numerous alternative assertion choices that JUnit provides.
In some cases, the easiest way to assert something won’t be to compare to
an actual result but to instead verify an operation by inverting it. You’ll see
a brief example of how.
You’ll also get an overview of AssertJ, a third-party assertion library that
allows you to write “fluent” assertions. Such assertions can make your tests
considerably easier to read. They can also provide more precise explanations
about why a test is failing.
report erratum  •  discuss


---
**Page 100**

Using the Core Assertion Forms
The bulk of your assertions will use either assertTrue or assertEquals. Let’s review
and refine your knowledge of these two assertion workhorses. Let’s also see
how to keep your tests streamlined by eliminating things that don’t add value.
The Most Basic Assertion Form: assertTrue
The most basic assert form accepts a Boolean expression or reference as an
argument and fails the test if that argument evaluates to false.
org.junit.jupiter.api.Assertions.assertTrue(someBooleanExpression);
Here’s an example demonstrating the use of assertTrue:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void hasPositiveBalanceAfterInitialDeposit() {
var account = new Account("an account name");
account.deposit(50);
Assertions.assertTrue(account.hasPositiveBalance());
}
// ...
Technically, you could use assertTrue for every assertion you had to write. But
an assertTrue failure tells you only that the assertion failed and nothing more.
Look for more precise assertions such as assertEquals, which reports what was
expected vs. what was actually received when it fails. You’ll find test failures
easier to understand and resolve as a result.
Eliminating Clutter
As documents that you’ll spend time reading and re-reading, you’ll want to
streamline your tests. You learned in the first chapter (see Chapter 1, Building
Your First JUnit Test, on page 3) that the public keyword is unnecessary when
declaring both JUnit test classes and test methods. Such additional keywords
and other unnecessary elements represent clutter.
Streamline your tests by eliminating unnecessary clutter.
You’ll be scanning lots of tests to gain a rapid understanding of what your
system does and where your changes must go. Getting rid of clutter makes
it easier to understand tests at a glance.
Chapter 5. Examining Outcomes with Assertions • 100
report erratum  •  discuss


