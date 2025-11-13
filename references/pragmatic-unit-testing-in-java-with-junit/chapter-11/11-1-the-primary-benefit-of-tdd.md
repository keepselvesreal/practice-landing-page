# 11.1 The Primary Benefit of TDD (pp.212-212)

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


