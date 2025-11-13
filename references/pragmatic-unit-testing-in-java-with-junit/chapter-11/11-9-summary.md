# 11.9 Summary (pp.233-235)

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


