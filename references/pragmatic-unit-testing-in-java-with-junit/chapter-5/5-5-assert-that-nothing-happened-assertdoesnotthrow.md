# 5.5 Assert That Nothing Happened: assertDoesNotThrow (pp.115-116)

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


---
**Page 116**

@Test
void throwsWhenNameContainsMultipleCommas() {
assertThrows(NameValidationException.class, () ->
validator.validate("Langr, Jeffrey,J."));
}
}
…and one test with assertDoesNotThrow to show nothing happens otherwise:
utj3-junit/01/src/test/java/scratch/ANameValidator.java
@Test
void doesNotThrowWhenNoErrorsExist() {
assertDoesNotThrow(() ->
validator.validate("Langr, Jeffrey J."));
}
Use assertDoesNotThrow if you must, but maybe explore a different design first.
For the example here, changing the validator to expose a Boolean method
would do the trick.
Exceptions Schmexceptions, Who Needs ‘em?
Most tests you write will be more carefree, happy path tests where exceptions
are highly unlikely to be thrown. But Java acts as a bit of a buzzkill, insisting
that you acknowledge any checked exception types.
Don’t clutter your tests with try/catch blocks to deal with checked exceptions.
Instead, let those exceptions loose! The test can just throw them:
utj3-junit/01/src/test/java/scratch/SomeAssertExamples.java
@Test
void readsFromTestFile() throws IOException {
➤
var writer = new BufferedWriter(new FileWriter("test.txt"));
writer.write("test data");
writer.close();
// ...
}
You’re designing these positive tests so you know they won’t throw an
exception except under truly exceptional conditions. Even if an exception does
get thrown unexpectedly, JUnit will trap it for you and report the test as an
error instead of a failure.
Alternate Assertion Approaches
Most of the assertions in your tests will be straight-up comparisons of
expected outcomes to actual outcomes: is the average credit history 780?
Sometimes, however, direct comparisons aren’t the most effective way to
describe the expected outcome.
Chapter 5. Examining Outcomes with Assertions • 116
report erratum  •  discuss


