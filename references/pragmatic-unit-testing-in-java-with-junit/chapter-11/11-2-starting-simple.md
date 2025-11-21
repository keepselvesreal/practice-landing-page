# 11.2 Starting Simple (pp.212-213)

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


