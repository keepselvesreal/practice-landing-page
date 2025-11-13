# Advancing with Test-Driven Development (TDD) (pp.211-235)

---
**Page 211**

CHAPTER 11
Advancing with Test-Driven
Development (TDD)
You’re now armed with what you’ll need to know about straight-up unit
testing in Java. In this part, you’ll learn about three significant topics:
• Using TDD to flip the concept of unit testing from test-after to test-driven
• Considerations for unit testing within a project team
• Using AI tooling to drive development, assisted by unit tests
You’ll start with a meaty example of how to practice TDD.
It’s hard to write unit tests for some code. Such “difficult” code grows partly
from a lack of interest in unit testing. In contrast, the more you consider how
to unit test the code you write, the more you’ll end up with easier-to-test code.
(“Well, duh!” responds our reluctant unit tester Joe.)
With TDD, you think first about the outcome you expect for the code you’re
going to write. Rather than slap out some code and then figure out how to
test it (or even what it should do), you first capture the expected outcome in
a test. You then code the behavior needed to meet that outcome. This reversed
approach might seem bizarre or even impossible, but it’s the core element
in TDD.
With TDD, you wield unit tests as a tool to help you shape and control your
systems. Rather than a haphazard practice where you sometimes write unit
tests after you write code, and sometimes you don’t, describing outcomes and
verifying code through unit tests becomes your central focus.
You will probably find the practice of TDD dramatically different than
anything you’ve experienced in software development. The way you build
report erratum  •  discuss


---
**Page 212**

code and the shape that your code takes on will change considerably. You
may well find TDD highly gratifying and ultimately liberating, strangely
enough.
In this chapter, you’ll test drive a small solution using TDD, unit by unit, and
talk about the nuanced changes to the approach that TDD brings.
The Primary Benefit of TDD
With plain ol’ after-the-fact unit testing, the obvious, most significant benefit
you gain is increased confidence that the code you wrote works as expected—at
least to the coverage that your unit tests provide. With TDD, you gain that
same benefit and many more.
Systems degrade primarily because we don’t strive often or hard enough to
keep the code clean. We’re good at quickly adding code into our systems, but
on the first pass, it’s more often not-so-great code than good code. We don’t
spend a lot of effort cleaning up that initially costly code for many reasons.
Joe chimes in with his list:
• “We need to move on to the next task. We don’t have time to gild the code.”
• “I think the code reads just fine the way it is. I wrote it, I understand it.
I can add some comments to the code if you think it’s not clear.”
• “We can refactor the code when we need to make further changes in that
area.”
• “It works. Why mess with a good thing? If it ain’t broke, don’t fix it. It’s
too easy to break something else when refactoring code.”
Thanks, Joe, for that list of common rationalizations for letting code degrade.
With TDD, your fear about changing code can evaporate. Indeed, refactoring is
a risky activity, and we’ve all made plenty of mistakes when making seemingly
innocuous changes. But if you’re following TDD well, you’re writing unit tests
for virtually all cases you implement in the system. Those unit tests give you
the freedom you need to continually improve the code.
Starting Simple
TDD is a three-part cycle:
1.
Write a test that fails.
2.
Get the test to pass.
3.
Clean up any code added or changed in the prior two steps.
Chapter 11. Advancing with Test-Driven Development (TDD) • 212
report erratum  •  discuss


---
**Page 213**

The first step of the cycle tells you to write a test describing the behavior you
want to build into the system. Seek to write a test representing the smallest
possible—but useful—increment to the code that already exists.
For your exercise, you’ll test-drive a small portfolio manager. Your require-
ments will be revealed to you incrementally as well, in batches, by your
product owner Madhu. Imagine that each requirements batch was not previ-
ously considered. Your job is to deliver a solution for each incremental need
to production.
You want to ensure that you can continue to accommodate new batches of
requirements indefinitely. To meet that ongoing demand, your focus after
getting each new test to pass—as part of the clean-up step in TDD—will be
to distill the solution to employ the simplest possible design. You will seek
maximally concise, clear, and cohesive code.
Each new TDD cycle starts with choosing the next behavior to implement.
For the smoothest progression through building a solution, you’ll seek a
behavior that produces the smallest possible increment from the current
solution.
In other words, you’re trying to ensure each TDD cycle represents a tiny little
step that requires only a tiny bit of new code or changed code.
You’ll step through four increments of code. You’ll be able to deliver each
increment to production.
Increment 1: Deferring Complexity
For your first requirements batch, you’re tasked with delivering very simple
rudiments of a portfolio.
You’ll be able to make purchases for the portfolio. For now, a purchase involves
a stock symbol, such as SONO (Sonos) or AAPL (Apple), and a number of
shares purchased for that symbol.
But your solution won’t need to track the actual symbols or shares of each.
Madhu tells you that all it needs to answer are the following two things:
• Whether or not it is empty. A portfolio is empty if no purchases have been
made and not empty otherwise.
• How many unique symbols have been purchased—the portfolio’s size. If
you purchase AAPL once, you have one unique symbol. If you purchase
AAPL a second time, you still have only the one unique symbol. If you
purchase AAPL and then purchase SONO, you have two unique symbols.
report erratum  •  discuss
Increment 1: Deferring Complexity • 213


---
**Page 214**

The ZOM progression (see ZOM: Zero and One Done, Now Testing Many, on
page 22) is a great place to start when practicing TDD. You’ll employ it fre-
quently as you try to derive the next-smallest increment.
You want to start with the absolute simplest requirement. Between the two
concerns—emptiness and size—emptiness seems simplest. Your first test is
a zero-based verification: the portfolio is empty when created (in other words,
no purchases have been made).
utj3-tdd/01/src/test/java/app/APortfolio.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;
public class APortfolio {
@Test
void isEmptyWhenCreated() {
var portfolio = new Portfolio();
assertTrue(portfolio.isEmpty());
}
}
In order to compile and run the test, you’ll need to supply an implementation
for the Portfolio class. You also want a test that fails (more on that as you go).
Returning false from isEmpty will cause the call to assertTrue to fail:
utj3-tdd/01/src/main/java/app/Portfolio.java
public class Portfolio {
public boolean isEmpty() {
return false;
}
}
Now, you can run JUnit. You expect a failure and receive it:
Expected :true
Actual
:false
All is well.
Avoid costly, poor assumptions with TDD. Ensure each new test
fails before you write the code to make it pass.
You seek the simplest code that will get the test to pass in order to avoid
adding code until you have a test that demands its existence:
Chapter 11. Advancing with Test-Driven Development (TDD) • 214
report erratum  •  discuss


---
**Page 215**

utj3-tdd/02/src/main/java/app/Portfolio.java
public boolean isEmpty() {
return true;
}
As far as the cleanup step in the TDD cycle is concerned, that four-line
solution is expressed about as concisely and clearly as it can get. Time to
move on.
If you’re using a capable source repository such as Git, now is the time to
commit your code. Committing each new bit of behavior as you do TDD makes
it easy to back up and change direction as needed.
You’ve written a test for a Boolean method that demonstrates when it returns
true. A second test, demonstrating the conditions that produce a false return, is
required. Creating a non-empty portfolio requires test code that makes a
purchase:
utj3-tdd/03/src/test/java/app/APortfolio.java
@Test
void isNotEmptyAfterPurchase() {
var portfolio = new Portfolio();
portfolio.purchase("AAPL", 1);
assertFalse(portfolio.isEmpty());
}
To appease the compiler, provide a purchase method:
utj3-tdd/03/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
}
Run all of your Portfolio tests and ensure that (only) the newest one fails.
To get your tests passing, you could consider storing the symbol and shares
in some sort of data structure, such as a HashMap. And that’s probably your
natural inclination as a developer. But it’s a lot more than you need at this
current moment. It speculates a need to be able to return the symbol and
shares, a need that does not exist.
Your goal is to meet requirements and deliver. Yes, you probably will need to
retain the symbol and shares in the portfolio. But TDD tells you to wait until
that need exists. For now, your goal is to get the test passing in as straight-
forward and non-speculative a manner as possible.
report erratum  •  discuss
Increment 1: Deferring Complexity • 215


---
**Page 216**

If you need to retain a Boolean state, a Boolean field will unsurprisingly do
the trick. On a purchase, update the Boolean to reflect that the portfolio is
no longer empty.
utj3-tdd/04/src/main/java/app/Portfolio.java
public class Portfolio {
private boolean isEmpty = true;
➤
public boolean isEmpty() {
return isEmpty;
➤
}
public void purchase(String symbol, int shares) {
isEmpty = false;
➤
}
}
Your tests need love, too. They are no longer concise; both the tests you’ve
written so far initialize a Portfolio object—a necessary thing to do, but not an
interesting thing to do in the sense that it adds any meaning to either test.
You can do the common initialization in a @BeforeEach method.
utj3-tdd/05/src/test/java/app/APortfolio.java
public class APortfolio {
Portfolio portfolio;
@BeforeEach
➤
void create() {
➤
portfolio = new Portfolio();
➤
}
➤
@Test
void isEmptyWhenCreated() {
assertTrue(portfolio.isEmpty());
}
@Test
void isNotEmptyAfterPurchase() {
portfolio.purchase("AAPL", 1);
assertFalse(portfolio.isEmpty());
}
}
For now, you’ve exhausted the Boolean. Two states/two behaviors/two tests.
A Boolean won’t support “many.”
Go ahead and commit your code at this point. Going forward, you won’t get
any more reminders. Every time you get a test to pass and spend a bit of
effort cleaning up the result, do a commit. You’ll appreciate being able to
revert to the previous increment of code.
Chapter 11. Advancing with Test-Driven Development (TDD) • 216
report erratum  •  discuss


---
**Page 217**

The next of the two features to tackle for this batch is the notion of the port-
folio’s size, and…yes, you’re right, a zero-based test.
utj3-tdd/06/src/test/java/app/APortfolio.java
@Test
void hasSize0WhenCreated() {
assertEquals(0, portfolio.size());
}
To get this to compile but not pass the tests, return -1 from size. After observing
the failure, hard-code a 0 to make it pass:
utj3-tdd/07/src/main/java/app/Portfolio.java
public int size() {
return 0;
}
Hard-coding seems silly, but it is in keeping with the test-code-and-refactor
rhythm of the TDD cycle. Your goal is to produce the simplest possible
implementation for the latest test. More specifically, you want to only solve
the current set of problems. By doing so, you avoid overengineering and pre-
mature speculation. Both will cost you in the long run.
You are learning to design for current need so that you can more easily take
on new, never-before-considered requirements that you could never have
predicted (or designed for).
Next test—make one purchase and have a portfolio with size one:
utj3-tdd/08/src/test/java/app/APortfolio.java
@Test
void hasSize1OnPurchase() {
portfolio.purchase("AAPL", 1);
assertEquals(1, portfolio.size());
}
Think for just a moment. Can you solve this problem given the current “data
structure” (a Boolean)? Of course you can:
utj3-tdd/09/src/main/java/app/Portfolio.java
public int size() {
return isEmpty ? 0 : 1;
}
Maybe a Boolean’s two states can support more than you think.
It’s possible that you’re thinking at this very moment that TDD might be too
pedantic to be useful. Hang in there. You’re starting to use your brain to think
differently about how to solve software problems. Specifically, you’re focusing
report erratum  •  discuss
Increment 1: Deferring Complexity • 217


---
**Page 218**

on what it means to find the next-smallest increment, probably something
you’ve not done before.
One key benefit you might or might not have noticed: each of these increments
is something you could get passing in no more than a couple minutes and in
seconds-less-than-100 in many cases (unless you’re a terrible typist, and
that’s okay too).
Ready for some real computing? The next test demands more than a two-state
solution can support:
utj3-tdd/10/src/test/java/app/APortfolio.java
@Test
void incrementsSizeWithEachPurchaseDifferentSymbol() {
portfolio.purchase("AAPL", 1);
portfolio.purchase("SONO", 1);
assertEquals(2, portfolio.size());
}
Your portfolio needs to track more than 0 and 1 values; it must be able to
answer 2, and 3, and to infinity…and beyond. The two-state Boolean solution
has reached its predictable end and must yield to the (short-to-live) future.
Introduce an int field named size, initialized to 0 and incremented on each
purchase:
utj3-tdd/11/src/main/java/app/Portfolio.java
public class Portfolio {
private boolean isEmpty = true;
private int size = 0;
➤
public boolean isEmpty() {
return isEmpty;
}
public void purchase(String symbol, int shares) {
isEmpty = false;
size++;
➤
}
public int size() {
return size;
➤
}
}
Note that you don’t evict the Boolean-related code just yet. It can watch and
continue to support current needs as progress, in the form of slightly more
generalized code supporting new behavior, gets built next door.
Chapter 11. Advancing with Test-Driven Development (TDD) • 218
report erratum  •  discuss


---
**Page 219**

Once you demonstrate that the generalization to an int works, you can take
advantage of a refactoring step to purge all the old, limited behaviors:
utj3-tdd/12/src/main/java/app/Portfolio.java
public class Portfolio {
private int size = 0;
public boolean isEmpty() {
return size == 0;
}
public void purchase(String symbol, int shares) {
size++;
}
public int size() {
return size;
}
}
Little pieces of code come and support a new initiative. Little pieces leave to
ensure a clean, easy-to-navigate code neighborhood.
Maybe you’re thinking, “this seems like a roundabout way to get to three lines
of code.” Two things are important to remember, however:
• You’ve created a handful of tests along with your solution. These tests
will continue to provide protection.
• You’re adopting a new mentality where someone could yell, “stop building!”
at any time, and you’d be okay with that. With TDD, you constantly have
the confidence to support releasing the system.
You’ve supported Zero, One, Many cases for the portfolio’s size. Now, it’s time
to think about the interesting cases. Hearken back to the description of the
requirements for this batch. One of them indicated that if you purchased
Apple stock and then purchased more of Apple stock, you still only had one
stock symbol and thus a portfolio size of one:
utj3-tdd/13/src/test/java/app/APortfolio.java
@Test
void doesNotIncrementSizeWithPurchaseSameSymbol() {
portfolio.purchase("AAPL", 1);
portfolio.purchase("AAPL", 1);
assertEquals(1, portfolio.size());
}
“Now is it time for the HashMap?” you might ask.
report erratum  •  discuss
Increment 1: Deferring Complexity • 219


---
**Page 220**

Not quite yet. Maybe half a hash map: A hash map is a collection of unique
keys, each that maps to some value. You might remember from second grade
that a collection of unique keys is known as a set.
Probably the easiest way to count the number of unique values is to throw
them into a set and ask for its size.
You introduced “real computing” a few moments back in the form of incre-
menting an integer. Now, you’ll get to use a “real data structure” in the form
of a Java set object.
“Pedantic again?” you might ask. Maybe. “Why not just use a HashMap?”
Because it’s more complex than what you need right now.
utj3-tdd/14/src/main/java/app/Portfolio.java
public class Portfolio {
private int size = 0;
private Set symbols = new HashSet<String>();
➤
public boolean isEmpty() {
return symbols.isEmpty();
➤
}
public void purchase(String symbol, int shares) {
size++;
symbols.add(symbol);
➤
}
public int size() {
return symbols.size();
➤
}
}
After verifying your updated solution, remove references to the size int:
utj3-tdd/15/src/main/java/app/Portfolio.java
public class Portfolio {
private Set symbols = new HashSet<String>();
public boolean isEmpty() {
return symbols.isEmpty();
}
public void purchase(String symbol, int shares) {
symbols.add(symbol);
}
public int size() {
return symbols.size();
}
}
Chapter 11. Advancing with Test-Driven Development (TDD) • 220
report erratum  •  discuss


---
**Page 221**

And…ship it! You’ve built support for tracking the size and emptiness of the
portfolio. It has no extraneous, speculative moving parts and is as simple a
solution as you could ask for. It’s fully tested with six simple unit tests.
Increment 2: Generalizing the Implementation
Madhu’s second batch of requirements for you is a batch of one: track the
number of shares owned for a given symbol. A happy path test case:
utj3-tdd/16/src/test/java/app/APortfolio.java
@Test
void returnsSharesGivenSymbol() {
portfolio.purchase("AAPL", 42);
assertEquals(42, portfolio.sharesOf("AAPL"));
}
The tests to any point in time represent the set of assumptions you make.
Currently, you are assuming there will only ever be a single purchase. As
such, you can track the shares purchased using a single discrete field:
utj3-tdd/17/src/main/java/app/Portfolio.java
public class Portfolio {
private Set symbols = new HashSet<String>();
private int shares;
➤
// ...
public void purchase(String symbol, int shares) {
symbols.add(symbol);
this.shares = shares;
➤
}
public int sharesOf(String symbol) {
➤
return shares;
➤
}
➤
}
You know that using a single field won’t hold up to multiple purchases that
are for differing symbols. That tells you that the next test you write—involve
multiple purchases—will most certainly fail, keeping you in the TDD cycle:
utj3-tdd/18/src/test/java/app/APortfolio.java
@Test
void separatesSharesBySymbol() {
portfolio.purchase("SONO", 42);
portfolio.purchase("AAPL", 1);
assertEquals(42, portfolio.sharesOf("SONO"));
}
report erratum  •  discuss
Increment 2: Generalizing the Implementation • 221


---
**Page 222**

“It’s time, right?” you ask. Why yes, you can finally introduce the HashMap…if
you must. There are other ways of solving the problem, but for now, the
HashMap is the most direct.
utj3-tdd/19/src/main/java/app/Portfolio.java
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
public class Portfolio {
private Map<String, Integer> purchases = new HashMap<>();
➤
private Set symbols = new HashSet<String>();
private int shares;
public boolean isEmpty() {
return purchases.isEmpty();
➤
}
public void purchase(String symbol, int shares) {
symbols.add(symbol);
this.shares = shares;
purchases.put(symbol, shares);
➤
}
public int size() {
return purchases.size();
➤
}
public int sharesOf(String symbol) {
return purchases.get(symbol);
➤
}
}
With your vaunted key-value data structure and supporting code in place,
you can make a pass that eliminates the use of both symbols and shares fields:
utj3-tdd/20/src/main/java/app/Portfolio.java
import java.util.HashMap;
import java.util.Map;
public class Portfolio {
private Map<String, Integer> purchases = new HashMap<>();
public boolean isEmpty() {
return purchases.isEmpty();
}
public void purchase(String symbol, int shares) {
purchases.put(symbol, shares);
}
public int size() {
return purchases.size();
}
Chapter 11. Advancing with Test-Driven Development (TDD) • 222
report erratum  •  discuss


---
**Page 223**

public int sharesOf(String symbol) {
return purchases.get(symbol);
}
}
Oops! You forgot about the zero-based test. Good habits take a while to
ingrain, and it’s still possible to temporarily forget even once ingrained.
utj3-tdd/21/src/test/java/app/APortfolio.java
@Test
void returns0SharesForSymbolNotPurchased() {
assertEquals(0, portfolio.sharesOf("SONO"));
}
The failing test requires a single line of production code, a guard clause in
the sharesOf method:
utj3-tdd/22/src/main/java/app/Portfolio.java
public int sharesOf(String symbol) {
if (!purchases.containsKey(symbol)) return 0;
➤
return purchases.get(symbol);
}
With a quick refactoring pass and a bit of Java knowledge, you can simplify
the two lines into one:
utj3-tdd/23/src/main/java/app/Portfolio.java
public int sharesOf(String symbol) {
return purchases.getOrDefault(symbol, 0);
➤
}
Next up—making sure that the portfolio returns the total number of shares
across all purchases of the same symbol:
utj3-tdd/23/src/test/java/app/APortfolio.java
@Test
void accumulatesSharesOfSameSymbolPurchase() {
portfolio.purchase("SONO", 42);
portfolio.purchase("SONO", 100);
assertEquals(142, portfolio.sharesOf("SONO"));
}
A small modification on an existing line of code is all you need:
utj3-tdd/24/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
purchases.put(symbol, sharesOf(symbol + shares)); // OOPS!
➤
}
report erratum  •  discuss
Increment 2: Generalizing the Implementation • 223


---
**Page 224**

Except, oops. That’s not quite the right implementation. A real mistake (by
me), and the tests quickly caught it. The fix involves moving the parentheses:
utj3-tdd/25/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
purchases.put(symbol, sharesOf(symbol) + shares);
➤
}
Increment 3: Factoring Out Redundancies
Your next challenge: support selling shares of a stock. There’s not much point
in buying stocks in the first place if you can’t sell them.
Madhu discusses the requirements with you:
• Reduce shares of a holding when selling stocks.
• Throw an exception on attempts to sell more shares of a symbol than
what is held.
Joe says, “okay,” then pauses a moment and asks, “what happens if you sell
all the shares of a stock? The portfolio’s size—its count of unique symbols
held—should come down by one, right?”
Madhu says, “Yes, a good thought, and let’s make sure we test for that.”
You both nod to Madhu and then turn to the monitor to code the first test:
utj3-tdd/26/src/test/java/app/APortfolio.java
@Test
void reducesSharesOnSell() {
portfolio.purchase("AAPL", 100);
portfolio.sell("AAPL", 25);
assertEquals(75, portfolio.sharesOf("AAPL"));
}
The implementation of the new sell method looks exactly like the purchase
method, with the exception of the minus sign:
utj3-tdd/26/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
purchases.put(symbol, sharesOf(symbol) + shares);
}
public void sell(String symbol, int shares) {
➤
purchases.put(symbol, sharesOf(symbol) - shares);
➤
}
➤
Both methods are heavy on implementation specifics and not abstractions.
You can extract the commonality to a shared method named updateShares:
Chapter 11. Advancing with Test-Driven Development (TDD) • 224
report erratum  •  discuss


---
**Page 225**

utj3-tdd/27/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
updateShares(symbol, shares);
➤
}
public void sell(String symbol, int shares) {
updateShares(symbol, -shares);
➤
}
private void updateShares(String symbol, int shares) {
➤
purchases.put(symbol, sharesOf(symbol) + shares);
}
Without the safety control that TDD provides, you would be less likely to
make small improvements to the codebase. It’s part of the reason why
most codebases steadily degrade over time with lots of crud building up
everywhere—poorly expressed code, redundant code, overly complex solutions,
and so on. The typical developer has little confidence to properly edit their
code once they get their “first draft” working.
TDD enables safe refactoring of virtually all of your code.
A second test, for the exceptional case:
utj3-tdd/28/src/test/java/app/APortfolio.java
@Test
void throwsWhenSellingMoreSharesThanHeld() {
portfolio.purchase("AAPL", 10);
assertThrows(InvalidTransactionException.class, () ->
portfolio.sell("AAPL", 10 + 1));
}
The guard clause that gets it to pass:
utj3-tdd/28/src/main/java/app/Portfolio.java
public void sell(String symbol, int shares) {
if (sharesOf(symbol) < shares)
➤
throw new InvalidTransactionException();
➤
updateShares(symbol, -shares);
}
You look at the implementation in sell, thinking it needs improvement. The
first two lines smack of implementation specifics (even though there aren’t a
whole lot of other ways to implement that logic). It doesn’t have the immediacy
that the other line in sell has. You extract it to its own method:
report erratum  •  discuss
Increment 3: Factoring Out Redundancies • 225


---
**Page 226**

utj3-tdd/29/src/main/java/app/Portfolio.java
public void sell(String symbol, int shares) {
abortOnOversell(symbol, shares);
➤
updateShares(symbol, -shares);
}
private void abortOnOversell(String symbol, int shares) {
➤
if (sharesOf(symbol) < shares)
➤
throw new InvalidTransactionException();
➤
}
➤
Time to move on to the special case: when all shares of a stock are sold,
ensure that the size of the portfolio reduces:
utj3-tdd/30/src/test/java/app/APortfolio.java
@Test
void reducesSizeWhenLiquidatingSymbol() {
portfolio.purchase("AAPL", 50);
portfolio.sell("AAPL", 50);
assertEquals(0, portfolio.size());
}
The test fails, as expected. Your solution:
utj3-tdd/30/src/main/java/app/Portfolio.java
public void sell(String symbol, int shares) {
abortOnOversell(symbol, shares);
updateShares(symbol, -shares);
removeSymbolIfSoldOut(symbol);
➤
}
private void removeSymbolIfSoldOut(String symbol) {
➤
if (sharesOf(symbol) == 0)
purchases.remove(symbol);
}
Increment 4: Introducing a Test Double
For the final increment, Madhu tells you that you’ll need to capture and save
a timestamp for each purchase or sale. He indicates that later requirements
will need this information. These are the current requirements:
• Provide details about the last transaction (purchase or sale) made,
including the timestamp.
• Produce a list of all transactions, ordered reverse-chronologically.
Chapter 11. Advancing with Test-Driven Development (TDD) • 226
report erratum  •  discuss


---
**Page 227**

You choose to start with the requirement for the last transaction. Before you
forget, you drop a zero-based test in place:
utj3-tdd/31/src/test/java/app/APortfolio.java
@Test
void returnsNullWhenNoPreviousTransactionMade() {
assertNull(portfolio.lastTransaction());
}
The next test, a one-based test for the last transaction, will require you to be
able to verify the timestamp of when the transaction was created. Time is an
ever-changing quantity. If production code captures the instant in time when
a transaction occurs, how can a test know what timestamp to expect?
Your solution uses a test double (see Chapter 3, Using Test Doubles, on page
53) that the Java class java.time.Clock provides for just this purpose. You use
the static method fixed on the Clock class, providing it a java.time.Instant object.
The clock object acts like a real-world broken clock, fixed to one point in time.
Every subsequent time inquiry will return the test instant you gave it.
After creating a Clock object with a fixed instant, the test injects it into the
portfolio via a setter:
utj3-tdd/31/src/test/java/app/APortfolio.java
@Nested
class LastTransaction {
Instant now = Instant.now();
@BeforeEach
void injectFixedClock() {
Clock clock = Clock.fixed(now, ZoneId.systemDefault());
portfolio.setClock(clock);
}
@Test
void returnsLastTransactionAfterPurchase() {
portfolio.purchase("SONO", 20);
assertEquals(portfolio.lastTransaction(),
new Transaction("SONO", 20, BUY, now));
}
}
The Portfolio class initializes its clock field to a working (production) clock. When
run in production, the clock returns the actual instant in time. When run in
the context of a unit test, the production clock gets overwritten with the
injected “broken” clock. Portfolio code doesn’t know or care about which context
it’s executing in.
report erratum  •  discuss
Increment 4: Introducing a Test Double • 227


---
**Page 228**

The following listing introduces both the clock as well as the ability to track
a “last transaction” object:
utj3-tdd/31/src/main/java/app/Portfolio.java
import java.time.Clock;
import static app.TransactionType.BUY;
import static java.lang.Math.abs;
// ...
public class Portfolio {
private Transaction lastTransaction;
➤
private Clock clock = Clock.systemUTC();
➤
// ...
public void purchase(String symbol, int shares) {
updateShares(symbol, shares);
}
private void updateShares(String symbol, int shares) {
lastTransaction =
➤
new Transaction(symbol, abs(shares), BUY, clock.instant());
➤
purchases.put(symbol, sharesOf(symbol) + shares);
}
// ...
public void setClock(Clock clock) {
this.clock = clock;
}
public Transaction lastTransaction() {
➤
return lastTransaction;
➤
}
➤
}
Here are declarations for the supporting types TransactionType and Transaction:
utj3-tdd/31/src/main/java/app/TransactionType.java
public enum TransactionType {
BUY, SELL;
}
utj3-tdd/31/src/main/java/app/Transaction.java
import java.time.Instant;
public record Transaction(
String symbol, int shares, TransactionType type, Instant now) {}
In the prior increment, you factored out the redundancy between the sell and
purchase methods, creating a new method, updateShares. It was the better design
choice for at least a couple of reasons:
• It increased the abstraction level and, thus, the understandability of the code.
• It increased the conciseness of the solution, reducing future costs to
understand both sell and update.
Chapter 11. Advancing with Test-Driven Development (TDD) • 228
report erratum  •  discuss


---
**Page 229**

Here, the shared method allowed you to isolate the creation of the Transaction
to a single method.
You add a second test so that the transaction type gets set appropriately for
sell transactions:
utj3-tdd/32/src/test/java/app/APortfolio.java
@Test
void returnsLastTransactionAfterSale() {
portfolio.purchase("SONO", 200);
portfolio.sell("SONO", 40);
assertEquals(portfolio.lastTransaction(),
new Transaction("SONO", 40, SELL, now));
}
utj3-tdd/32/src/main/java/app/Portfolio.java
public void purchase(String symbol, int shares) {
updateShares(symbol, shares, BUY);
➤
}
public void sell(String symbol, int shares) {
abortOnOversell(symbol, shares);
updateShares(symbol, -shares, SELL);
➤
removeSymbolIfSoldOut(symbol);
}
private void updateShares(String symbol, int shares, TransactionType type) {
➤
lastTransaction =
new Transaction(symbol, abs(shares), type, clock.instant());
➤
purchases.put(symbol, sharesOf(symbol) + shares);
}
Moving on to the transaction history requirement:
utj3-tdd/33/src/test/java/app/APortfolio.java
@Nested
class TransactionHistory {
Instant now = Instant.now();
@BeforeEach
void injectFixedClock() {
Clock clock = Clock.fixed(now, ZoneId.systemDefault());
portfolio.setClock(clock);
}
@Test
void returnsEmptyListWhenNoTransactionsMade() {
assertTrue(portfolio.transactions().isEmpty());
}
report erratum  •  discuss
Increment 4: Introducing a Test Double • 229


---
**Page 230**

@Test
void returnsListOfTransactionsReverseChronologically() {
portfolio.purchase("A", 1);
portfolio.purchase("B", 2);
portfolio.purchase("C", 3);
assertEquals(portfolio.transactions(), List.of(
new Transaction("C", 3, BUY, now),
new Transaction("B", 2, BUY, now),
new Transaction("A", 1, BUY, now)
));
}
}
Although two tests are shown here to simplify the presentation in this book,
ensure you incrementally write each and develop the solution for each sepa-
rately. Writing multiple tests at a time is improper TDD practice.
The implementation:
utj3-tdd/33/src/main/java/app/Portfolio.java
import java.time.Clock;
import java.util.LinkedList;
import java.util.List;
// ...
public class Portfolio {
private Transaction lastTransaction;
➤
private LinkedList transactions = new LinkedList();
➤
// ...
private void updateShares(String symbol,
int shares,
TransactionType type) {
lastTransaction =
new Transaction(symbol, abs(shares), type, clock.instant());
transactions.addFirst(lastTransaction);
➤
purchases.put(symbol, sharesOf(symbol) + shares);
}
public Transaction lastTransaction() {
return lastTransaction;
}
public List<Transaction> transactions() {
➤
return transactions;
➤
}
➤
// ...
}
You no longer need the field lastTransaction, as you can extract the most recent
transaction from the transaction list. You’ll want to change both the updateShares
and lastTransaction methods. Ensure you remove the field afterward.
Chapter 11. Advancing with Test-Driven Development (TDD) • 230
report erratum  •  discuss


---
**Page 231**

utj3-tdd/34/src/main/java/app/Portfolio.java
private void updateShares(String symbol,
int shares,
TransactionType type) {
var transaction =
➤
new Transaction(symbol, abs(shares), type, clock.instant());
transactions.addFirst(transaction);
➤
purchases.put(symbol, sharesOf(symbol) + shares);
}
public Transaction lastTransaction() {
return transactions.peekFirst();
➤
}
You might consider the solution design at this point to be flawed. It uses two
distinct data structures to manage information that could be represented
with one. If you consider the list of transactions as the “document of record,”
all inquiries regarding the portfolio can be calculated from it. The information
captured in the purchases HashMap is essentially an optimized calculation.
The dual data structure implementation is a recipe for later disaster, partic-
ularly as the solution increases in complexity. If new behaviors are added,
it’s possible that an oversight will lead to inconsistent data representations
in each data structure.
The better solution would be to eliminate the hash map, replacing all inquiries
of it with operations on the history stream instead. If you’re curious what this
looks like, visit versions 35 and 36 in the source distribution.
Test-Driven Development vs. Test-After Development
TDD centers on the simple cycle of test-code-refactor. “Significantly reduced
defects” would seem to be the key benefit of practicing TDD, but it can accrue
some even more valuable benefits. Most of them derive from describing every
desired, incremental outcome before coding it into the system.
By definition, TDD gives you near-complete unit test coverage, which in turn
gives you the following significant benefits:
• High confidence that the unit behaviors are correct
• The ability to continuously retain a high-quality design
• The ability to incorporate new changes safely and without fear
• Clear, trustworthy documentation on all intended behaviors
Your cost of change can reduce dramatically as a result.
report erratum  •  discuss
Test-Driven Development vs. Test-After Development • 231


---
**Page 232**

You’ve been learning test-after development (TAD, as in “a tad too late”) in
this book. With TAD, testing is an afterthought—as in, “I thought about
writing some unit tests after I developed my stellar code but decided not to.”
You could absolutely achieve full coverage with TAD. There’s no mechanical
reason why you couldn’t write TAD tests that cover every behavior in your
system. The reality, though, is that almost no one ever does.
TAD can be harder than TDD. Determining all the behavioral intents of previ-
ously written code can be tough, even if it was written within the last hour.
It seems simpler, in contrast, to first capture the desired outcome with a test.
Writing tests for code with private dependencies and myriad entanglements
is also tough. It seems simpler to shape code to align with the needs of a test
instead of the other way around.
Here’s a short list of reasons we don’t write enough tests when doing TAD:
1.
We run out of time and are told to move on to the next thing. “We just
need to ship.”
2.
Because it’s often hard, we sometimes give up, particularly if we’re told
to move on.
3.
We think our code doesn’t stink. “I just wrote this, it looks great.”
4.
We avoid it because unit testing isn’t as much fun as writing the produc-
tion code.
5.
Someone else told us we had to do it, which can be another discourage-
ment for some of us.
Re-read How Much Coverage Is Enough?, on page 77 if you think there’s little
difference between 75% and 100% coverage. Minimally, remember that 75%
coverage means that a quarter of the code in your system remains at risk.
The Rhythm of TDD
TDD cycles are short. Without all the chatter accompanying this chapter’s
example, each test-code-refactor cycle takes maybe a few minutes. Increments
of code written or changed at each step in the cycle are likewise small.
Once you’ve established a short-cycle rhythm with TDD, it becomes obvious
when you’re heading down a rathole. Set a regular time limit of about ten
minutes. If you haven’t received any positive feedback (passing tests) in the
last ten minutes, discard what you were working on and try again, taking
Chapter 11. Advancing with Test-Driven Development (TDD) • 232
report erratum  •  discuss


---
**Page 233**

even smaller steps. If you were committing after introducing (and cleaning)
each new increment, reverting to the prior increment will be a trivial operation.
Yes, you heard right—throw away costly code. Treat each cycle of TDD as a
time-boxed experiment whose test is the hypothesis. If the experiment is going
awry, restarting the experiment and shrinking the scope of assumptions
(taking smaller steps) can help you pinpoint where things went wrong. The
fresh take can often help you derive a better solution in less time than you
would have wasted on the mess you were making.
Summary
In this chapter, you toured the practice of TDD, which takes all the concepts
you’ve learned about unit testing and puts them into a simple disciplined
cycle: write a test, get it to pass, ensure the code is clean, and repeat.
Adopting TDD may change the way you think about design.
Next, you’ll learn about some topics relevant to unit testing as part of a
development team.
report erratum  •  discuss
Summary • 233


---
**Page 235**

CHAPTER 12
Adopting Team Practices
You last learned about TDD, a concept you can employ on your own. When you
work in a team environment, shifting to TDD represents an effective way to
take your unit testing practice to the next, more disciplined level. In this
chapter, you’ll learn a few other considerations for doing unit testing within
a team environment.
If you’re like most of us, you’re working on a project with other team members.
You want to be on the same page with them when it comes to unit testing.
In this chapter, you’ll learn about working agreements that your team must
hash out to avoid wasting time on endless debates and code thrashing. Topics
include test standards, code/test review, and continuous integration.
Coming up to Speed
Incorporating a new practice like unit testing requires continual vigilance.
Even if you enjoy writing unit tests and are good about covering the new code
you write, you’ll sometimes face an uphill battle within your team. They might
not be as vigilant, and they’re probably producing code at a rate that far
outpaces your ability to test it. You might also face a team that insists on
tossing all safeguards, tests included, in order to meet a critical deadline.
“Unit testing isn’t free,” says Joe, “We’ve gotta deliver in two weeks. We’re way
behind and just need to slam out code.”
Lucia responds to Joe, “The worst possible time to throw away unit tests is
while in crunch mode. Squeezing lots of coding into a short time will guarantee
a mess. It’ll take longer to know if everything still works and to fix the defects
that arise…and there’ll be a lot more of those. One way or another, we’ll pay
dearly if we dispense with quality for short-term gains.
report erratum  •  discuss


