# 11.6 Increment 4: Introducing a Test Double (pp.226-231)

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


