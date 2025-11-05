# 11.4 Increment 2: Generalizing the Implementation (pp.221-224)

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


