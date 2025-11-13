# 11.7 Test-Driven Development vs. Test-After Development (pp.231-232)

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


