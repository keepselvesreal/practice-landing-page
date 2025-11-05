# 11.8 The Rhythm of TDD (pp.232-233)

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


