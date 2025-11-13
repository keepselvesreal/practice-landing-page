# Examining Outcomes with Assertions (pp.99-123)

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


---
**Page 101**

Asserts pervade JUnit tests. Rather than explicitly scope each assert call with
the class name (Assertion), use a static import:
import static org.junit.jupiter.api.Assertions.assertTrue;
The result is a de-cluttered, more concise assertion statement:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void hasPositiveBalanceAfterInitialDeposit() {
var account = new Account("an account name");
account.deposit(50);
assertTrue(account.hasPositiveBalance());
➤
}
Generalized Assertions
Here’s another example of assertTrue which explains how a result relates to
some expected outcome:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void depositIncreasesBalance() {
var account = new Account("an account name");
var initialBalance = account.getBalance();
account.deposit(100);
assertTrue(account.getBalance() > initialBalance);
}
A test name—depositIncreasesBalance—is a general statement about the behavior
you want the test to demonstrate. Its assertion—assertTrue(balance > initialBalance)—
corresponds to the test name, ensuring that the balance has increased as an
outcome of the deposit operation. The test does not explicitly verify by how
much the balance increased. As a result, you might describe its assert
statement as a generalized assertion.
Eliminating More Clutter
The preceding examples depend on the existence of an initialized Account
instance. You can create an Account in a @BeforeEach method (see Initializing
with @BeforeEach and @BeforeAll, on page 124 for more information) and store
a reference to it as a field on the test class:
utj3-junit/02/src/test/java/scratch/AnAccount.java
class AnAccount {
Account account;
report erratum  •  discuss
Using the Core Assertion Forms • 101


---
**Page 102**

@BeforeEach
void createAccount() {
account = new Account("an account name");
}
@Test
void hasPositiveBalanceAfterInitialDeposit() {
account.deposit(50);
assertTrue(account.hasPositiveBalance());
}
// ...
}
JUnit creates a new instance of the test class for each test (see Observing
the JUnit Lifecycle, on page 127 for further explanation). That means you
can also safely initialize fields at their point of declaration:
utj3-junit/03/src/test/java/scratch/AnAccount.java
class AnAccount {
Account account = new Account("an account name");
@Test
void hasPositiveBalanceAfterInitialDeposit() {
// ...
}
// ...
}
Use assertEquals for Explicit Comparisons
Your test names should be generalizations of behavior, but each test should
present a specific example with a specific result. If the test makes a deposit,
you know what the new balance amount should be. In most cases, you should
be explicit with your assertion and verify the actual new balance.
The assertion assertEquals compares an expected answer to the actual answer,
allowing you to explicitly verify an outcome’s value. It’s overloaded so that
you can appropriately compare all primitive types, wrapper types, and object
references. (To compare two arrays, use assertArrayEquals instead.) Most of your
assertions should probably be assertEquals.
Here’s the deposit example again, asserting by how much the balance
increased:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void depositIncreasesBalanceByAmountDeposited() {
account.deposit(50);
Chapter 5. Examining Outcomes with Assertions • 102
report erratum  •  discuss


---
**Page 103**

account.deposit(100);
assertEquals(150, account.getBalance());
}
You design the example for each test, and you know the expected outcome.
Encode it in the test with assertEquals.
Assertion Messages: Redundant Messages for Assertions
Most verifications are self-explanatory, at least in terms of the code bits they’re
trying to verify. Sometimes, it’s helpful to have a bit of “why” or additional context
to explain an assertion. “Just why does this test expect the total to be 42?”
Most JUnit assert forms support an optional final argument named message.
The message argument allows you to supply a nice verbose explanation of the
rationale behind the assertion:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void balanceRepresentsTotalOfDeposits() {
account.deposit(50);
account.deposit(51);
var balance = account.getBalance();
assertEquals(101, balance, "account balance must be total of deposits");
}
The assertion message displays when the test fails:
account balance must be total of deposits ==> expected: <101> but was: <102>
If you prefer lots of explanatory comments, you might get some mileage out
of assertion messages. However, this is the better route:
• Test only one behavior at a time
• Make your test names more descriptive
In fact, if you demonstrate only one behavior per test, you’ll usually only need
a single assertion. The name of the test will then naturally describe the reason
for that one assertion. No assertion failure message is needed.
Well-written tests document themselves.
Elements like explanatory constants, helper methods, and intention-revealing
variable names go a long way toward making tests accessible and to the point.
The existence of comments and assertion messages in unit tests is a smell
report erratum  •  discuss
Assertion Messages: Redundant Messages for Assertions • 103


---
**Page 104**

that usually indicates stinky test design. In Chapter 10, Streamlining Your
Tests, on page 189, you’ll step through an example of test clean-up.
In well-written tests, the assertion message becomes redundant clutter, just
one more thing to have to wade through and maintain.
Improved test failure messages can provide a small benefit since figuring out
the meaning or implication of an assertion failure can be frustrating. Rather
than use assertion failure messages, however, take a look at AssertJ, which
provides fluent assertions that generate more detailed failure messages.
1
Assertion messages can also provide value when you employ parameterized
tests, which are a JUnit mechanism for running the same test with a bunch
of different data. See Executing Multiple Data Cases with Parameterized Tests,
on page 131.
Other Common JUnit Assertion Forms
While assertEquals and assertTrue would cover almost all the assertions you’ll
need to write, you’ll want to learn about the other forms that JUnit supports.
Choosing the best assertion for the job will keep your tests concise and clear.
In this section, you’ll be introduced to the majority of JUnit’s other assertion
forms, including assertFalse, assertNotEquals, assertSame, assertNotSame, assertNull, and
assertNotNull. You’ll also get an experience-based opinion on the value and best
uses for each variant.
assertFalse
Nobody doesn’t dislike double negatives (or triple negatives, so says my editor).
To help you say things “straight up” in your tests, JUnit provides some inverse
assertions. Here’s assertFalse—the opposite of assertTrue—in action:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void doesNotHavePositiveBalanceWhenAccountCreated() {
assertFalse(account.hasPositiveBalance());
}
You can code the equivalent by using assertTrue if you’re in a contrary mood:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void doesNotHavePositiveBalanceWhenAccountCreated() {
assertTrue(!account.hasPositiveBalance());
}
1.
https://assertj.github.io/doc/
Chapter 5. Examining Outcomes with Assertions • 104
report erratum  •  discuss


---
**Page 105**

Paraphrased, it reads awkwardly: “assert true…not account has positive balance”
and represents the kind of logic that trips many of us up. Keep the double
negatives out of your tests. Use assertFalse when it’s easier to read than assertTrue.
assertNotEquals
Appropriate use of assertNotEquals is much rarer. If you know what the answer
should be, use assertEquals to say that. Use of assertNotEquals otherwise may
represent making what you might call a weak assertion—one that doesn’t
fully verify a result.
Some sensible cases for using assertNotEquals:
• You really don’t have a way of knowing what the answer should be.
• You’ve explained (in another test, perhaps) what an actual answer might
be, and with this test, you want to emphasize that it can’t possibly be
some other specified value.
• It would require too much data detail to explicitly assert against the
actual result.
Let’s try an example. For any card game (for example, poker), you must
shuffle the deck of playing cards prior to dealing any cards from it. Here’s a
starter implementation of a Deck class, showing that shuffling occurs in its
constructor:
utj3-junit/01/src/main/java/cards/Deck.java
public class Deck {
private LinkedList<Card> cards;
public Deck() {
cards = newDeck();
Collections.shuffle(cards);
➤
}
static LinkedList<Card> newDeck() {
var cards = new LinkedList<Card>();
for (var i = 1; i <= 13; i++) {
cards.add(new Card(i, "C"));
cards.add(new Card(i, "D"));
cards.add(new Card(i, "H"));
cards.add(new Card(i, "S"));
}
return cards;
}
public Card deal() {
return cards.removeFirst();
}
report erratum  •  discuss
Other Common JUnit Assertion Forms • 105


---
**Page 106**

List<Card> remaining() {
return cards;
}
}
You want to verify that the shuffling did actually occur:
utj3-junit/01/src/test/java/cards/ADeck.java
public class ADeck {
Deck deck = new Deck();
// ... other Deck tests here ...
@Test
void hasBeenShuffled() {
var cards = deck.remaining();
assertNotEquals(Deck.newDeck(), cards);
}
}
You might be thinking, “Hey, that looks like a weak assertion!” It is, in a way—
you do not know whether or not the deck has been properly shuffled. But
that’s not the job of the Deck class. The Deck class here invokes a shuffle rather
than implementing it, using a method from the Java API. You can trust that
Collections.shuffle() randomizes the order of a collection appropriately, though
you might need a better random shuffler if you’re a casino.
Since you can trust the Java API, you don’t need to prove the quality of its shuf-
fle. But your unit test does need to verify that the cards were actually shuffled.
You can do this in a number of somewhat complex ways, such as by using test
doubles (see Chapter 3, Using Test Doubles, on page 53) or injecting a seeded
random number generator to use for shuffling.
Ensuring that the order of cards in an instantiated Deck is not equal to the
cards returned by Deck.newDeck() is sufficient and simple. It demonstrates that
some operation occurred to change the order. (Note that this weak assertion
also has a slim possibility of failing in the one case where it shuffles to the
deck’s starting order. Highly unlikely in your lifetime. Run the test again if
you chance upon that serendipitous moment.)
Yes, someone could replace the call to Collections.shuffle() with shoddy shuffle
code—for example, something that moved one card from the front to the back
of the deck. But don’t worry—no one would do that.
Unit tests don’t exist to protect you from willful destructiveness. A determined
saboteur can break your system without breaking any tests.
Chapter 5. Examining Outcomes with Assertions • 106
report erratum  •  discuss


---
**Page 107**

Avoid weak assertions like assertNotEquals unless you have no choice
or they emphasize what you really want your test to say.
assertSame
Also infrequently used, assertSame verifies that two references point to the same
object in memory.
Your challenge: minimize the use of memory in a scheduling application where
there might need to be many millions of Time objects. (This example is based
on “Working with Design Patterns: Flyweight.”)
2 Most of these Times will be on
the quarter hour (11:15, 14:30, 10:15) because that’s how we usually like to
schedule things. Some small subset will be at odd times, like 3:10 or 4:20,
because some people do odd things at odd times, dude.
The idea of the flyweight pattern is to have a single object pool, which allows
for multiple interested parties to share objects that have the same values.
(This works great for immutable objects, not so great otherwise.) Your appli-
cation can reduce its memory footprint significantly as a result.
Here are the two production classes involved:
utj3-junit/01/src/main/java/time/Time.java
import static java.lang.String.format;
public record Time(byte hour, byte minute) {
static String key(byte hour, byte minute) {
return format("%d:%d", hour, minute);
}
@Override
public String toString() {
return key(hour, minute);
}
}
utj3-junit/01/src/main/java/time/TimePool.java
import java.util.HashMap;
import java.util.Map;
public class TimePool {
private static Map<String, Time> times = new HashMap<>();
static void reset() {
times.clear();
}
2.
https://www.developer.com/design/working-with-design-patterns-flyweight/
report erratum  •  discuss
Other Common JUnit Assertion Forms • 107


---
**Page 108**

public static Time get(byte hour, byte minute) {
return times.computeIfAbsent(Time.key(hour, minute),
k -> new Time(hour, minute));
}
}
Here are a couple of tests:
utj3-junit/01/src/test/java/time/ATimePool.java
public class ATimePool {
@BeforeEach
void resetPool() {
TimePool.reset();
}
@Test
void getReturnsTimeInstance() {
byte four = 4;
byte twenty = 20;
assertEquals(new Time(four, twenty), TimePool.get(four, twenty));
}
@Test
void getWithSameValuesReturnsSharedInstance() {
byte ten = 10;
byte five = 5;
var firstRetrieved = TimePool.get(ten, five);
var secondRetrieved = TimePool.get(ten, five);
assertSame(firstRetrieved, secondRetrieved);
➤
}
}
The highlighted line in the second test demonstrates the use of assertSame. The
arrange step calls the get method on the TimePool to retrieve a first Time object,
then makes the same call a second time in the act step. The assert step verifies
that the two Time objects are one and the same.
assertNotSame
assertNotSame verifies that two references point to different objects in memory.
You might use assertNotSame to verify that an object “persisted” in memory—in
a hash map, for example—is a different instance than the one stored. Other-
wise, changes to the “live” object would also alter the persisted object. Here’s
some code to demonstrate:
utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
package persistence;
import org.junit.jupiter.api.Test;
Chapter 5. Examining Outcomes with Assertions • 108
report erratum  •  discuss


---
**Page 109**

import static org.junit.jupiter.api.Assertions.*;
class AnInMemoryDatabase {
@Test
void objectCopiedWhenAddedToDatabase() {
var db = new InMemoryDatabase();
var customer = new Customer("1", "Smelt, Inc.");
db.add(customer);
var retrieved = db.data.get("1");
assertNotSame(retrieved, customer);
}
}
The test creates an InMemoryDatabase and adds a customer via the database’s
add method.
utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
import java.util.HashMap;
import java.util.Map;
public class InMemoryDatabase {
Map<String, Customer> data = new HashMap<>();
public void add(Customer customer) {
data.put(customer.id(), new Customer(customer));
➤
}
}
In the add method in the production code, the highlighted line shows the use
of a copy constructor on the Customer record to ensure that a new instance is
added to the HashMap named data.
Without making that copy—with this line instead as the implementation for
the add method:
utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
data.put(customer.id(), customer);
…the test fails.
One way to think about unit tests is they add protections—and corresponding
explanations—for the little things that are important but not necessarily
obvious, like the need for creating a copy in this example.
Unit tests not only safeguard but also describe the thousands of
choices in your system.
report erratum  •  discuss
Other Common JUnit Assertion Forms • 109


---
**Page 110**

assertNull
assertNull is equivalent to doing assertEquals(null, someValue).
The InMemoryDatabase class needs a public way for clients to retrieve customers
by their id. Here’s an implementation of a get method:
utj3-junit/01/src/main/java/persistence/InMemoryDatabase.java
public class InMemoryDatabase {
Map<String, Customer> data = new HashMap<>();
// ...
public Customer get(String id) {
return data.getOrDefault(id, null);
}
}
How many tests do you need to cover that method? The word “Or” in getOrDefault
is a solid hint that you’ll want at least two. In this listing, the first test is the
“happy path” case where a Customer is successfully retrieved:
utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
InMemoryDatabase db = new InMemoryDatabase();
@Test
void returnsCustomerCorrespondingToId() {
var customer = new Customer("42", "Mr Creosote");
db.add(customer);
var retrieved = db.get("42");
assertEquals(customer, retrieved);
}
@Test
void returnsNotNullForNonexistentKey() {
assertNull(db.get("42"));
➤
}
The second test demonstrates the use of assertNull: if you attempt to retrieve
anything (42 in this case) from a newly created db (into which nothing has
been inserted), it should return null.
assertNotNull
assertNotNull is the opposite of assertNull, naturally. It’s used to assert that a ref-
erence points to something, not nothing.
Like assertNotEquals, many uses of assertNotNull are dubious.
Some folks new to JUnit introduce assertNotNull checks for references to newly
instantiated objects:
Chapter 5. Examining Outcomes with Assertions • 110
report erratum  •  discuss


---
**Page 111**

utj3-junit/01/src/test/java/persistence/AnInMemoryDatabase.java
@Test
void returnsCustomerCorrespondingToId() {
var customer = new Customer("42", "Mr Creosote");
assertNotNull(customer); // bogus! this can't fail
➤
db.add(customer);
var retrieved = db.get("42");
assertEquals(customer, retrieved);
}
However, that assertNotNull can never fail. The only way that the customer variable,
initialized in the first line of the test, can ever end up null is if the Customer
constructor throws an exception. If an exception is thrown, the next line of
code—the assertNotNull statement—is never executed. If no exception is thrown,
the customer reference will point to a (non-null) object, so the assertNotNull will
never fail if it does get executed. Don’t do that.
assertNotNull is only useful when you need to demonstrate that a reference
points to a value and you don’t care at all what that value is. Otherwise—if
you can determine the expected value—assertNotNull is a weak assertion. You’d
be better off using assertEquals to compare the reference to its actual value.
You’ll know when, on rare occasions, you should reach for assertNotNull. Other-
wise…don’t do that.
An Added Assortment of Asserts
But wait—there’s more!
The org.junit.jupiter.api.Assertions class in JUnit provides a few more assertions
that are not described here. Without perusing the users’s guide or the volu-
minous Javadoc for the class, you wouldn’t know these assertions existed.
Here they are with brief descriptions of what they do.
asserts that two lists or streams of strings match; can involve
regular expressions and "fast forwarding"
assertLinesMatch
asserts that all supplied executables do not throw exception
assertAll
asserts that the actual value is an instance of the expected type
assertInstanceOf
asserts that the provided Iterable references are deeply equal
assertIterableEquals
asserts that an executable completes execution within a speci-
fied duration
assertTimeout
like assertTimeout, but runs the executable in a separate thread
assertTimeout
Preemptively
report erratum  •  discuss
Other Common JUnit Assertion Forms • 111


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


---
**Page 119**

Here’s what an AssertJ assertion looks like when applied to the common need
of comparing one object to another—isEqualTo is analogous to assertEquals in JUnit:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(name).isEqualTo("my big fat acct");
So far, so simple. To note:
• You can take advantage of autocomplete to flesh out the assertion.
• The assertion reads like an English sentence, left to right.
AssertJ provides numerous inversions of positively stated assertions. Thus,
the converse of isEqualTo is isNotEqualTo:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(name).isNotEqualTo("plunderings");
A few more examples follow. Most of them speak for themselves, and that’s
part of the point.
You can use chaining to specify multiple expected outcomes in a single
statement. The following assertion passes if the name references a string that
both starts with "my" and ends with "acct":
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(name)
.startsWith("my")
.endsWith("acct");
A type-checking example:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(name).isInstanceOf(String.class);
Using regular expressions:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(name).containsPattern(
compile("\\s+(big fat|small)\\s+"));
AssertJ contains numerous tests around lists:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
@Test
public void simpleListTests() {
var names = List.of("Moe", "Larry", "Curly");
assertThat(names).contains("Curly");
assertThat(names).contains("Curly", "Moe");
assertThat(names).anyMatch(name -> name.endsWith("y"));
assertThat(names).allMatch(name -> name.length() < 6);
}
report erratum  •  discuss
Third-Party Assertion Libraries • 119


---
**Page 120**

The third list assertion passes if any one or more of the elements in the list
ends with the substring "y". (The strings "Larry" or "Curly" here make it pass.)
The fourth assertion passes if all of the elements in the list have a length less
than 6. (They do.)
(Caveat: The preceding asserts that verify only part of a string might be con-
sidered weak assertions. You likely need to verify more.)
AssertJ’s failing fluent assertions provide far more useful failure messages
than what JUnit might give you. Here’s a failing assertion for the list of names:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
assertThat(names).allMatch(name -> name.length() < 5);
… and here’s the failure message generated by AssertJ:
Expecting all elements of:
["Moe", "Larry", "Curly"]
to match given predicate but these elements did not:
["Larry", "Curly"]
Knowing exactly why the assert failed should speed up your fix.
AssertJ allows you to express your assertions in the most concise manner
possible, particularly as things get more complex. Occasionally, your tests will
need to extract specific data from results in order to effectively assert against
it. With JUnit, doing so might require one or more lines of code before you
can write the assertion. With AssertJ, you might be able to directly express
your needs in a single statement.
The Power of Fluency
Let’s look at a small example that still demonstrates some of AssertJ’s power.
The example uses two classes:
• a Flight class that declares a segment field of type Segment
• a Segment class containing the fields origin, destination, and distance
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
record Segment(String origin, String destination, int distance) {
boolean includes(String airport) {
return origin.equals(airport) || destination.equals(airport);
}
}
record Flight(Segment segment, LocalDateTime dateTime) {
Flight(String origin, String destination,
int distance, LocalDateTime dateTime) {
Chapter 5. Examining Outcomes with Assertions • 120
report erratum  •  discuss


---
**Page 121**

this(new Segment(origin, destination, distance), dateTime);
}
boolean includes(String airport) {
return segment.includes(airport);
}
}
The following AssertJ assertion compares against a list of Flight objects stored
in the variable flights:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
@Test
void filterAndExtract() {
// ...
assertThat(flights)
.filteredOn(flight -> flight.includes("DEN"))
.extracting("segment.distance", Integer.class)
.allMatch(distance -> distance < 1700);
}
The call to filteredOn returns a subset of flights involving the flight code "DEN".
The call to extracting applies an AssertJ property reference ("segment.distance") to
each "DEN" flight. The reference tells AssertJ to first retrieve the segment object
from a flight, then retrieve the distance value from that segment as an Integer.
Yes, you could manually code an equivalent to the AssertJ solution, but the
resulting code would lose the declarative nature that AssertJ can provide.
Your test would require more effort to both write and read. In contrast,
AssertJ’s support for method chaining creates a fluent sentence that you can
read as a single concept.
Regardless of whether you choose to adopt AssertJ or another third-party
assertions library, streamline your tests so they read as concise documenta-
tion. A well-designed assertion step minimizes stepwise reading.
Eliminating Non-Tests
Assertions are what make a test an automated test. Omitting assertions from
your tests would render them pointless. And yet, some developers do exactly
that in order to meet code coverage mandates easily. Another common ruse
is to write tests that exercise a large amount of code, then assert something
simple—for example, that a method’s return value is not null.
Such non-tests provide almost zero value at a significant cost in time and
effort. Worse, they carry an increasingly negative return on investment: you
must expend time on non-tests when they fail or error, when they appear in
report erratum  •  discuss
Eliminating Non-Tests • 121


---
**Page 122**

search results (“is that a real test we need to update or do we not need to
worry about it?”), and when you must update them to keep them running
(for example, when a method signature gets changed).
Eliminate tests that verify nothing.
Summary
You’ve learned numerous assertion forms in this chapter. You also learned
about AssertJ, an alternate assertions library.
Initially, you’ll survive if you predominantly use assertEquals for most assertions,
along with an occasional assertTrue or assertFalse. You’ll want to move to the next
level quickly, however, and learn to use the most concise and expressive
assertion for the situation at hand.
Armed with a solid understanding of how to write assertions, you’ll next dig
into the organization of test classes so that you can most effectively run and
maintain related groups of tests.
Chapter 5. Examining Outcomes with Assertions • 122
report erratum  •  discuss


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


