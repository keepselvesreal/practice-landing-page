# 5.6 Alternate Assertion Approaches (pp.116-118)

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


---
**Page 117**

For example, suppose you’ve coded the method fastHalf that uses bit shifting
to perform integer division by two. The code is trivial, as are some core tests:
utj3-junit/01/src/main/java/util/MathUtils.java
public class MathUtils {
static long fastHalf(long number) {
return number >> 1;
}
}
utj3-junit/01/src/test/java/util/SomeMathUtils.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static util.MathUtils.fastHalf;
public class SomeMathUtils {
@Nested
class FastHalf {
@Test
void isZeroWhenZero() {
assertEquals(0, fastHalf(0));
}
@Test
void roundsDownToZeroWhenOne() {
assertEquals(0, fastHalf(1));
}
@Test
void dividesEvenlyWhenEven() {
assertEquals(11, fastHalf(22));
}
@Test
void roundsDownWhenOdd() {
assertEquals(10, fastHalf(21));
}
@Test
void handlesNegativeNumbers() {
assertEquals(-2, fastHalf(-4));
}
You might want another test to verify the utility works with very large numbers:
utj3-junit/01/src/test/java/util/SomeMathUtils.java
@Test
void handlesLargeNumbers() {
var number = 489_935_889_934_389_890L;
assertEquals(244_967_944_967_194_945L, fastHalf(number));
}
But, oh, that’s ugly, and it’s hard for a test reader to quickly verify.
report erratum  •  discuss
Alternate Assertion Approaches • 117


---
**Page 118**

You’ve demonstrated that fast half works for 0, 1, many, and negative number
cases. For very large numbers, rather than show many-digit barfages in the
test, you can write an assertion that emphasizes the inverse mathematical
relationship between input and output:
utj3-junit/01/src/test/java/util/SomeMathUtils.java
@Test
void handlesLargeNumbers() {
var number = 489_935_889_934_389_890L;
assertEquals(number, fastHalf(number) * 2);
}
Mathematical computations represent the canonical examples for verifying
via inverse relationships: you can verify division by using multiplication,
addition by using subtraction, square roots by squares, and so on. Other
domains where you can verify using inverse operations include cryptography,
accounting, physics, computer graphics, finance, and data compression.
Cross-checking via inversion ensures that everything adds up and balances,
much like the general ledger in a double-entry bookkeeping system. It’s not
a technique you should reach for often, but it can occasionally help make
your tests considerably more expressive. You might find particular value in
inversion when your test demands voluminous amounts of data.
Be careful with the code you use for verification! If both the actual routine
and the assertion share the same code (perhaps a common utility class you
wrote), they could share a common defect.
Third-Party Assertion Libraries
JUnit provides all the assertions you’ll need, but it’s worth taking a look at
the third-party assertion libraries available—AssertJ, Hamcrest, Truth, and
more. These libraries primarily seek to improve upon the expressiveness of
assertions, which can help streamline and simplify your tests.
Let’s take a very quick look at AssertJ, a popular choice, to see a little bit of
its power. AssertJ offers fluent assertions, which are designed to help tests
flow better and read more naturally. A half-dozen simple examples should
get the idea across quickly. Each of the examples assumes the following
declaration:
String name = "my big fat acct";
The core AssertJ form reverses JUnit order. You specify the actual value first
as an argument to an assertThat method that all assertions use. You then make
a chained call to one of many methods that complete or continue the assertion.
Chapter 5. Examining Outcomes with Assertions • 118
report erratum  •  discuss


