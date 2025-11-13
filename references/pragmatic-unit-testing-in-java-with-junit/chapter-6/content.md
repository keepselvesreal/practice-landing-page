# Establishing Organization in JUnit Tests (pp.123-135)

---
**Page 123**

CHAPTER 6
Establishing Organization in JUnit Tests
Your JUnit learnings so far include:
• How to run JUnit and understand its results
• How to group related test methods within a test class
• How to group common test initialization into a @BeforeEach method
• A deep dive into JUnit assertions (the previous chapter)
Generally, you want at least one test class for each production class you
develop. In this chapter, you’ll dig into the topic of test organization within a
test class. You’ll learn about:
• The parts of a test
• Initializing and cleaning up using lifecycle methods
• Grouping related tests with nested classes
• The JUnit test execution lifecycle
• Avoiding dependency challenges by never ordering tests
• Executing multiple test cases for a single test using parameterized tests
The Parts of an Individual Test
A handful of chapters ago (see Scannability: Arrange—Act—Assert, on page
18), you learned how AAA provides a great visual mnemonic to help readers
quickly understand the core parts of a test.
Some developers refer to a “four-phase test,”
1 where each test can be broken
into (wait for it) four parts or phases:
• Set up state/data in what’s sometimes called a fixture. Think of a fixture
as the context in which a test runs—its world, so to speak. The fixture is
1.
http://xunitpatterns.com/Four%20Phase%20Test.html
report erratum  •  discuss


---
**Page 124**

managed for you by JUnit; you’ll learn more about that in this chapter
as part of the JUnit test execution lifecycle.
• Interact with the system to execute what you want to verify.
• Do the verification (assert).
• Tear down the fixture—clean up any side effects, if necessary. This typi-
cally involves cleaning up resources that a test might have used and that
could impact the execution of other tests. In this chapter, you’ll read
about doing such clean-up with @AfterEach and @AfterAll JUnit hooks.
For every intent and purpose, AAA is the first three parts of a four-part test.
Arrange, act, assert ≈ setup, execute, verify.
Turns out that the fourth part, “tear down,” is and should be rare in unit
tests, in which you seek to avoid (mostly by design) interaction with the things
that you must clean up. If you feel AAA cheats you out of that fourth phase,
you can add a fourth “A”…for ANNIHILATION! (If the violence disturbs you,
just mentally go with “After.” Keep calm and carry on.)
Setting Up and Tearing Down Using Lifecycle Methods
You learned about @BeforeEach in your first JUnit example (see Chapter 1,
Building Your First JUnit Test, on page 3). Let’s take a closer look at this
initialization hook, as well as some other useful hooks that JUnit provides.
Initializing with @BeforeEach and @BeforeAll
In Abstraction: Eliminating Boring Details, on page 20, you learned to use
@BeforeEach to put common initialization in one place. Methods annotated
with @BeforeEach are executed before each test in scope.
JUnit also provides another initialization hook known as @BeforeAll, which you
must declare as a static method. Each method annotated with @BeforeAll gets
executed once per test class and prior to the execution of anything else
within that class. Its primary use is to ensure that slowly executing initializa-
tions (for example, anything involving a database) only have to execute once.
Otherwise, prefer using @BeforeEach.
If you find yourself using @BeforeAll more than once in a blue moon, you may
be testing behaviors bigger than units. That may be okay, but it might suggest
you have opportunities for reducing the dependencies in your system. See
Chapter 3, Using Test Doubles, on page 53 for ideas on how to do that.
Chapter 6. Establishing Organization in JUnit Tests • 124
report erratum  •  discuss


---
**Page 125**

If your test needs demand that you initialize a few things before each test is
run, you can declare multiple @BeforeEach methods in the test class’s scope,
each with a different name. These don’t run in any useful order, just as test
methods do not.
Creating additional @BeforeEach methods allows you to use their methods name
to describe what’s going on in each initialization. Of course, you can also
lump all your initialization into a single @BeforeEach method as long as it’s easy
for other developers to understand what’s going on when reading through
your lump.
You can have multiple (static) @BeforeAll methods in a test class.
Using @AfterEach and @AfterAll for Cleanup
JUnit bookends the initialization hooks @BeforeEach and @BeforeAll with corre-
sponding “teardown” lifecycle methods @AfterEach and @AfterAll. These methods
allow you to clean up resources on test completion. Both @AfterEach and
@AfterAll are guaranteed to run (as long as the JUnit process itself doesn’t
crash), even if any tests throw exceptions.
Within @AfterEach, for example, you might close a database connection or delete
a file. If you write integration (non-unit) tests in JUnit, these teardown hooks
are essential.
Most unit tests, however, shouldn’t interact with code that requires clean-up.
The typical, hopefully rare case is when multiple tests alter the state of a
static field.
If you do have a clean-up need, try to redesign your code to eliminate it. Use
dependency injection (see Injecting Dependencies into Production Code, on
page 56) and/or mock objects (see Chapter 3, Using Test Doubles, on page
53) as appropriate.
Even when you do have a legitimate clean-up need, adding code to @AfterEach
or @AfterAll is mostly only being nice. Suppose the general assumption is that
all tests clean up after themselves—seems like a fair testing standard, yes?
The problem is that eventually, someone will forget to properly clean up in
another test elsewhere. If your test fails as a result, it may take some real
time to figure out which one of possibly thousands of tests is the culprit.
Each of your tests is responsible for ensuring it executes in a
clean, expected state.
report erratum  •  discuss
Setting Up and Tearing Down Using Lifecycle Methods • 125


---
**Page 126**

You can usually design your code so almost no unit tests require clean-up,
but you may still need @AfterEach in a tiny number of places.
Organizing Related Tests into Nested Classes
As your classes grow by taking on more behaviors, you’ll need more and more
tests to describe the new behaviors. Use your test class size as a hint: if you
declare several dozen tests in one test source file, chances are good that the
class under test is too large. Consider splitting the production class up into
two or more classes, which also means you’ll want to split the test methods
across at least two or more test classes.
You may still end up with a couple dozen test methods in one test class. A
larger test class can not only be daunting from a navigational sense, but it
can also make it harder to find all tests that relate to each other.
To help group related tests, you might consider starting each related test’s
name with the same thing. Here are three tests describing how withdrawals
work in the Account class:
@Test void withdrawalReducesAccountBalance() { /* ... */ }
@Test void withdrawalThrowsWhenAmountExceedsBalance() { /* ... */ }
@Test void withdrawalNotifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
A better solution, however, is to group related tests within a JUnit @Nested
class:
@Nested
class Withdrawal {
@Test void reducesAccountBalance() { /* ... */ }
@Test void throwsWhenAmountExceedsBalance() { /* ... */ }
@Test void notifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
}
You can create a number of @Nested classes within your test class, similarly
grouping all methods within it. The name of the nested class, which describes
the common behavior, can be removed from each test name.
You can also use @Nested classes to group tests by context—the state estab-
lished by the arrange part of a test. For example:
class AnAccount
@Nested
class WithZeroBalance {
@Test void doesNotAccrueInterest() { /* ... */ }
@Test void throwsOnWithdrawal() { /* ... */ }
}
Chapter 6. Establishing Organization in JUnit Tests • 126
report erratum  •  discuss


---
**Page 127**

@Nested
class WithPositiveBalance {
@BeforeEach void fundAccount() { account.deposit(1000); }
@Test void accruesInterest() { /* ... */ }
@Test void reducesBalanceOnWithdrawal() { /* ... */ }
}
}
Tests are split between those needing a zero-balance account (WithZeroBalance)
and those needing a positive account balance (WithPositiveBalance).
Observing the JUnit Lifecycle
You’ve learned about using before and after hooks and how to group related
tests into nested classes. Using a skeleton test class, let’s take a look at how
these JUnit elements are actually involved when you run your tests.
AFundedAccount contains six tests. Per its name, all tests can assume that an
account exists and has a positive balance. An account object gets created at
the field level and subsequently funded within a @BeforeEach method. Here’s
the entire AFundedAccount test class, minus all the intricate details of each test.
utj3-junit/01/src/test/java/scratch/AFundedAccount.java
import org.junit.jupiter.api.*;
class AFundedAccount {
Account account = new Account("Jeff");
AFundedAccount() {
// ...
}
@BeforeEach
void fundAccount() {
account.deposit(1000);
}
@BeforeAll
static void clearAccountRegistry() {
// ...
}
@Nested
class AccruingInterest {
@BeforeEach
void setInterestRate() {
account.setInterestRate(0.027d);
}
@Test
void occursWhenMinimumMet() {
// ...
}
report erratum  •  discuss
Organizing Related Tests into Nested Classes • 127


---
**Page 128**

@Test
void doesNotOccurWhenMinimumNotMet() {
// ...
}
@Test
void isReconciledWithMasterAccount() {
// ...
}
}
@Nested
class Withdrawal {
@Test
void reducesAccountBalance() {
// ...
}
@Test
void throwsWhenAmountExceedsBalance() {
// ...
}
@Test
void notifiesIRSWhenAmountExceedsThreshold() {
// ...
}
}
}
While you could choose to instantiate the account field in a @BeforeEach method,
there’s nothing wrong with doing field-level initialization, particularly if
there’s not much going on. The field declaration in AFundedAccount initializes
an account with some arbitrary name, so it’s not interesting enough to warrant
a @BeforeEach method. But if your common initialization is at all interesting or
requires a series of statements, you’d definitely want it to occur within a
@BeforeEach method.
The use of @Nested makes for well organized test results when you run your tests:
Chapter 6. Establishing Organization in JUnit Tests • 128
report erratum  •  discuss


---
**Page 129**

You can clearly see the grouping of related tests, which makes it easier to find
what you’re looking for. The visual grouping also makes it easier to spot the glaring
absence of necessary tests as well as review their names for consistency—with
other tests or with your team’s standards for how tests are named.
I instrumented each of the @BeforeEach methods, the @Test methods, and the
constructors (implicitly defined in the listing) with System.out statements. Here’s
the output when the tests are run:
@BeforeAll::clearAccountRegistry
AFundedAccount(); Jeff balance = 0
Withdrawal
@BeforeEach::fundAccount
notifiesIRSWhenAmountExceedsThreshold
AFundedAccount(); Jeff balance = 0
Withdrawal
@BeforeEach::fundAccount
reducesAccountBalance
AFundedAccount(); Jeff balance = 0
Withdrawal
@BeforeEach::fundAccount
throwsWhenAmountExceedsBalance
AFundedAccount(); Jeff balance = 0
Accruing Interest
@BeforeEach::fundAccount
@BeforeEach::setInterestRate
occursWhenMinimumMet
AFundedAccount(); Jeff balance = 0
Accruing Interest
@BeforeEach::fundAccount
@BeforeEach::setInterestRate
accruesNoInterestWhenMinimumMet
AFundedAccount(); Jeff balance = 0
Accruing Interest
@BeforeEach::fundAccount
@BeforeEach::setInterestRate
doesNotOccurWhenMinimumNotMet
The static @BeforeAll method executes first.
The output shows that a new instance of AFundedAccount is constructed for each
test executed. It also shows that the account is, as expected, properly initial-
ized with a name and zero balance.
Creating a new instance for each test is part of JUnit’s deliberate design. It
helps ensure each test is isolated from side effects that other tests might
create.
report erratum  •  discuss
Organizing Related Tests into Nested Classes • 129


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


---
**Page 132**

return new Digit(
acc.arabic - digitsRequired * conversion.arabic,
acc.roman + conversion.roman.repeat(digitsRequired));
}).roman();
}
}
Neither the algorithm nor the behavior changes based on the inputs. Were
you to code this as separate JUnit tests, there’d be little useful distinction
between the test names:
utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class ARomanNumberConverter {
RomanNumberConverter converter = new RomanNumberConverter();
@Test
void convertsOne() {
assertEquals("I", converter.toRoman(1));
}
@Test
void convertsTwo() {
assertEquals("II", converter.toRoman(2));
}
@Test
void convertsThree() {
assertEquals("III", converter.toRoman(3));
}
// ... so wordy!
}
It’s tedious to create separate tests for each case, and their names add little
real value. You could lump them all in a single test method but then the
individual cases wouldn’t be isolated from each other.
Fortunately, JUnit supports a special form of test known as a parameterized
test. You create a parameterized test by annotating your test method with
@ParameterizedTest instead of @Test. You must also provide a data source, which
is essentially a list of data rows. For each data row, JUnit calls the test method
with data from the row as parameters.
The parameterized test method for the RomanNumberConverter needs two pieces
of information: the Arabic number to be passed to the toRoman method and
the expected Roman equivalent to be used in an assertEquals statement. You
can use a @CsvSource to provide data rows for the test; each row is a CSV
(comma-separated values) string.
Chapter 6. Establishing Organization in JUnit Tests • 132
report erratum  •  discuss


---
**Page 133**

Here’s a parameterized test for the RomanNumberConverter:
utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
@ParameterizedTest
@CsvSource({
"1,
I",
➤
"2,
II",
"3,
III",
"10,
X",
"20,
XX",
"11,
XI",
"200,
CC",
"732,
DCCXXXII",
"2275, MMCCLXXV",
"999,
CMXCIX",
"444,
CDXLIVI", // failure
})
void convertAll(int arabic, String roman) {
➤
assertEquals(roman, converter.toRoman(arabic));
}
The first data row in the @CsvSource (highlighted) contains the CSV string "1,
I".
JUnit splits this string on the comma and trims the resulting values. It passes
these values—the number 1 and the string "I"—to the convertAll test method
(highlighted).
JUnit takes the CSV values and uses them, left to right, as arguments to the
test method. So when the test method is executed, 1 gets assigned to the int
arabic parameter (with JUnit converting the string to an int), and "I" gets assigned
to the String roman parameter.
Since the above example shows eleven CSV data rows, JUnit will run convertAll
eleven times. IntelliJ shows the parameters for each of the eleven cases:
Note how JUnit indicates the failing (incorrectly specified) case.
The JUnit documentation
2 goes into considerable detail about the various
data source mechanisms available.
2.
https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-sources
report erratum  •  discuss
Executing Multiple Data Cases with Parameterized Tests • 133


---
**Page 134**

Here’s a quick summary:
A single array of values. Useful only if your test takes one
parameter (which implies that the expected outcome is the
same for every source value)
@ValueSource
Iterates all the possible enum values, with some options for
inclusion/exclusion and regex matching
@EnumSource
Expects the name of a method, which must return all data
rows in a stream
@MethodSource
Mostly the same thing as @CsvSource, except that you specify
a filename containing the CSV rows
@CsvFileSource
Allows you to create a custom, reusable data source in a
class that extends an interface named ArgumentsProvider
@ArgumentsSource
While parameterized tests in JUnit are sophisticated and flexible beasts,
@CsvSource will suit most of your needs. I’ve never needed another data source
variant (though I don’t frequently use parameterized tests).
In summary, parameterized tests are great when you need to demonstrate
data (not behavioral) variants. These are a couple of pervasive needs:
• Code that conditionally executes if a parameter is null or an empty string.
A parameterized test with two inputs (null and "") lets you avoid test
duplication.
• Code around border conditions, particularly because such code often
breeds defects. For example, for code that conditionally executes if n <= 0,
use a parameterized test with the values n - 1 and n.
Otherwise, create a new @Test that describes a distinct behavior.
Summary
On most systems, you’ll end up with many hundreds or thousands of unit
tests. You’ll want to keep your maintenance costs low by taking advantage
of a few JUnit features, including lifecycle methods, nested classes, and param-
eterized tests. These features allow you to reduce redundant code and make
it easy to run a related set of tests.
Now that you’ve learned how to best organize your tests, in the next chapter,
you’ll dig into topics that relate to executing tests using JUnit. You’ll pick up
some good habits for deciding how many tests to run (and when to not run
tests). You’ll learn how to run subsets of tests as well as how to temporarily
disable tests.
Chapter 6. Establishing Organization in JUnit Tests • 134
report erratum  •  discuss


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


