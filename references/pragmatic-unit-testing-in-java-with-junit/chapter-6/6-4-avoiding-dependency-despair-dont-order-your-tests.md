# 6.4 Avoiding Dependency Despair: Don’t Order Your Tests! (pp.130-131)

---
**Page 130**

JUnit creates a new instance of the test class for each test method
that runs.
The @BeforeEach method fundAccount, declared within the top-level scope of the
AFundedAccount class, executes prior to each of all six tests.
The @BeforeEach method setInterestRate, declared within the scope of AccruingInterest,
executes only prior to each of the three tests defined within that nested class.
Avoiding Dependency Despair: Don’t Order Your Tests!
JUnit tests don’t run in their declared (top to bottom) order. In fact, they don’t
run in any order that you’d easily be able to determine or depend on, such
as alphabetically. (They’re likely returned in the order that a call to
java.lang.Class.getMethods() returns, which is “not sorted and not in any particular
order,” per its Javadoc.)
You might be tempted to think you want your tests to run in a specific order:
“I’m writing a first test around newly created accounts, which have a zero
balance. A second test can add $100 to the account, and I can verify that
amount. I can then add a test that runs third, in which I’ll deposit $50 and
ensure that the new balance is $150.”
While JUnit 5 provides a way to force the ordering of test execution, using it
for unit tests is a bad idea. Depending on test order might help you avoid
redundantly stepping through common setup in multiple test cases. But it
will usually lead you down the path to wasted time. For example, say you’re
running tests, and the fourth test fails. Was it because of a real problem in
the production code? Or was it because one of the preceding three tests (which
one?) left the system in some newly unexpected state?
With ordered tests, you’ll also have a harder time understanding any test
that’s dependent on other tests. Increasing dependencies is as costly in tests
as it is in your production code.
Unit tests should verify isolated units of code and not depend on
any order of execution.
Rather than creating headaches by forcing the order of tests, use @BeforeEach
to reduce the duplication of common initialization. You can also extract helper
methods to reduce redundancy and amplify your tests’ abstraction level.
Chapter 6. Establishing Organization in JUnit Tests • 130
report erratum  •  discuss


---
**Page 131**

Executing Multiple Data Cases with Parameterized Tests
Many of your system’s behaviors will demand several distinct test cases. For
example, you’ll often end up with at least three tests as you work through
the progression of zero-one-many.
Defining separate test methods allows you to explicitly summarize their distinct
behaviors in the test names:
storesEmptyStringWhenEmpty
storesInputStringWhenContainingOneElement
storesCommaSeparatedStringWhenContainingManyElements
Often, the three test cases will be structured exactly the same—all the state-
ments within it are the same, but the input and expected output data differ.
You can streamline the redundancies across these tests with things like helper
methods and @BeforeEach methods if it bothers you.
Sometimes, when you have such redundancy across tests, there’s no interest-
ing way to name them distinctly. For example, suppose you have tests for
code that converts Arabic numbers into Roman equivalents:
utj3-junit/01/src/main/java/util/RomanNumberConverter.java
public class RomanNumberConverter {
record Digit(int arabic, String roman) {}
Digit[] conversions = {
new Digit(1000, "M"),
new Digit(900, "CM"),
new Digit(500, "D"),
new Digit(400, "CD"),
new Digit(100, "C"),
new Digit(90, "XC"),
new Digit(50, "L"),
new Digit(40, "XL"),
new Digit(10, "X"),
new Digit(9, "IX"),
new Digit(5, "V"),
new Digit(4, "IV"),
new Digit(1, "I")
};
public String toRoman(int arabic) {
return Arrays.stream(conversions).reduce(
new Digit(arabic, ""),
(acc, conversion) -> {
var digitsRequired = acc.arabic / conversion.arabic;
report erratum  •  discuss
Executing Multiple Data Cases with Parameterized Tests • 131


