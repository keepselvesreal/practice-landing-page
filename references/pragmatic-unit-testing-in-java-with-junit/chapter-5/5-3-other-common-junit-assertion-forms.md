# 5.3 Other Common JUnit Assertion Forms (pp.104-112)

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


