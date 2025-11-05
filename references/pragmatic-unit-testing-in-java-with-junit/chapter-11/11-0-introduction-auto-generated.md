# 11.0 Introduction [auto-generated] (pp.211-212)

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


