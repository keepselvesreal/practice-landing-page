# 11.3 Increment 1: Deferring Complexity (pp.213-221)

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


