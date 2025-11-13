# 5.4 Expecting Exceptions (pp.112-115)

---
**Page 112**

Expecting Exceptions
In addition to ensuring that the happy path through your code works, you
also need to verify the unhappy cases. For example, you’ll want to write tests
that demonstrate when code can throw exceptions. These tests are necessary
to provide a full understanding of the behaviors to developers who must work
with the code.
The ever-evolving Java language has driven the continual development of
JUnit as well—there are no fewer than four ways to write exception-based
tests in JUnit. You’ll take a look at a couple of these.
Let’s examine a simple case: ensure the Account code throws an InsufficientFunds-
Exception when a client attempts to withdraw more than the available balance.
Newer School: assertThrows
The assertThrows assertion, available in JUnit since version 4.13, should cover
all your needs when writing exception-based tests. Prefer it over the other
mechanisms.
The most useful assertThrows form takes two arguments: the type of the exception
expected to be thrown and an executable object (usually a lambda, but
potentially a method reference). The executable contains the code expected
to throw the exception.
When the assertion gets executed by JUnit, the code in the lambda is run. If
that code throws no exception, the assertion fails. If the code in the lambda
does throw an exception, the test passes if the type of the exception object
matches or is a subclass of the expected exception type.
Here’s assertThrows in action. The lambda argument to assertThrows attempts to
withdraw 100 from a newly created account (that is, one with no money):
utj3-junit/01/src/test/java/scratch/AnAccount.java
import static org.junit.jupiter.api.Assertions.assertThrows;
// ...
@Test
void throwsWhenWithdrawingTooMuch() {
var thrown = assertThrows(InsufficientFundsException.class,
() -> account.withdraw(100));
assertEquals("balance only 0", thrown.getMessage());
}
Calling assertThrows returns the exception object. This test assigns it to the
thrown variable to allow asserting against its message string.
Chapter 5. Examining Outcomes with Assertions • 112
report erratum  •  discuss


---
**Page 113**

Don’t add extraneous code to the lambda. You don’t want a false positive
where the test passes because the wrong line of code threw the expected
exception.
Code in withdraw passes the assertThrows statement by throwing an InsufficientFunds-
Exception when the amount to withdraw exceeds the balance:
utj3-junit/01/src/main/java/scratch/Account.java
void withdraw(int dollars) {
if (balance < dollars) {
throw new InsufficientFundsException("balance only " + balance);
}
balance -= dollars;
}
Old School
Prior to the availability of assertThrows, you had at least three options in JUnit
for expecting exceptions: Using try/catch, annotations, and rules. You may see
some of these solutions if you maintain older systems. Annotations and rules
aren’t supported by JUnit 5, so I won’t cover them here. I’ll show you what
they look like, though, so you can understand what you’re seeing.
Here’s an example of the annotations-based mechanism:
@Test(expected=InsufficientFundsException.class)
public void throwsWhenWithdrawingTooMuch() {
account.withdraw(100);
}
If you see expected= as an argument to the @Test annotation, visit the JUnit 4
documentation on @Test for further explanation.
3
Here’s what the use of the rules-based mechanism (added in JUnit 4.7) might
look like:
public class SimpleExpectedExceptionTest {
@Rule
public ExpectedException thrown= ExpectedException.none();
@Test
public void throwsException() {
thrown.expect(NullPointerException.class);
thrown.expectMessage("happened");
// ... code that throws the exception
}
// ...
3.
https://junit.org/junit4/javadoc/4.12/org/junit/Test.html
report erratum  •  discuss
Expecting Exceptions • 113


---
**Page 114**

If you see an ExpectedException instantiated and annotated with @Rule, visit JUnit
4’s documentation for ExpectedException for further explanation.
4
If it’s not obvious, “old school” is pejorative. (I’m allowed to say it, though,
‘cause I’m old.) Don’t use these old constructs if you can help it.
Use of try/catch
JUnit’s first releases supported only “roll-your-own” mechanisms for exception
handling, based on the use of Java’s try/catch construct. Here’s the comparable
Account code for expecting an InsufficientFundsException:
@Test
void throwsWhenWithdrawingTooMuch() {
try {
account.withdraw(100);
➤
fail();
} catch (InsufficientFundsException expected) {
assertEquals("balance only 0", expected.getMessage());
}
}
When JUnit executes code within a try block that does throw an exception,
control is transferred to the appropriate catch block and executed. In the
example, since the code indeed throws an InsufficientFundsException, control
transfers to the assertEquals statement in the catch block, which verifies the
exception object’s message contents.
You can deliberately fail the test by commenting out the withdrawal operation
in Account’s withdraw method. Do that to see firsthand what JUnit tells you.
If the call to withdraw does not throw an exception, the next line executes. When
using the try/catch mechanism, the last line in the try block should be a call to
org.junit.Assert.fail(). As you might guess, JUnit’s fail method throws an Assertion-
FailedError so as to abort and fail the test.
The try/catch idiom represents the rare case where it might be okay to have
an empty catch block—perhaps you don’t care about the contents of the
exception. Naming the exception variable expected helps reinforce to the reader
that we expect an exception to be thrown and caught.
Think about other things that you might want a test to assert after an
exception has been thrown. Examine any important post-conditions that
must hold true. For example, it might be of value to assert that the account
balance didn’t change after the failed withdrawal attempt.
4.
https://junit.org/junit4/javadoc/4.12/org/junit/rules/ExpectedException.html
Chapter 5. Examining Outcomes with Assertions • 114
report erratum  •  discuss


---
**Page 115**

You might occasionally see the try/catch mechanism used in older code. If so, you
can leave it alone (you now know how it works), or you can streamline your test
by replacing it with assertThrows.
Assert That Nothing Happened: assertDoesNotThrow
As with a lot of other assertion forms, JUnit provides a converse to assertThrows—
specifically, the ‘assertDoesNotThrow‘ method. In its simplest form, it takes an
executable object (a lambda or method reference). If the invocation of code in
the executable doesn’t throw anything, the assertion passes; otherwise, it fails.
Every once in a while, you’ll think you might want to use assertDoesNotThrow…the
only problem is, it really doesn’t assert anything about what the executed
code does do. Try finding a way to test that elusive “something.”
You might find assertDoesNotThrow useful as the catch-all in a series of tests.
Suppose you have a validator that throws an exception in a couple of cases
and otherwise does nothing:
utj3-junit/01/src/test/java/scratch/ANameValidator.java
class NameValidationException extends RuntimeException {}
class NameValidator {
long commaCount(String s) {
return s.chars().filter(ch -> ch == ',').count();
}
void validate(String name) {
if (name.isEmpty() ||
commaCount(name) > 1)
throw new NameValidationException();
}
}
You need two tests to demonstrate that validate throws an exception for each
of the two negative cases:
utj3-junit/01/src/test/java/scratch/ANameValidator.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertThrows;
class ANameValidator {
NameValidator validator = new NameValidator();
@Test
void throwsWhenNameIsEmpty() {
assertThrows(NameValidationException.class, () ->
validator.validate(""));
}
report erratum  •  discuss
Assert That Nothing Happened: assertDoesNotThrow • 115


