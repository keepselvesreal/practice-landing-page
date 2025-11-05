# 11.5 Increment 3: Factoring Out Redundancies (pp.224-226)

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


