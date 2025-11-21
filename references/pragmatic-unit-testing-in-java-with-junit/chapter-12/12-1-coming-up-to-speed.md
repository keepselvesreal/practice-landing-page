# 12.1 Coming up to Speed (pp.235-236)

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


---
**Page 236**

“Slapping out code with no tests only speeds us up for a very short period of
time—maybe a couple of days or so. Invariably, we’ll hit ugly defects requiring
long debugging sessions. Maybe the worst of it is that we’ll create chunks of
legacy code that’ll cost us forever. Sorry Joe, tossing unit tests isn’t worth it.”
Not much will allow you to escape last-minute crunches unscathed, no matter
how good you are at development. Once you’re there, all you can do is nego-
tiate or work excessive hours. But if you insist on quality controls from day
one, it won’t happen nearly as often.
Unit testing is a part of those quality controls. Let’s look at how to ensure
that it becomes a habit within your team.
Getting on the Same Page with Your Team
Approaches to unit testing can vary dramatically from developer to developer.
Some insist on TDD. Others resist unit testing at all costs, producing only
tests they feel forced to write. Some prefer lumping multiple cases into a
single test method. Some favor slower integration tests. Some will disagree
with other recommendations you’ve learned from this book.
Your team must get on the same page, whether it’s regarding unit testing
standards or how you review code in the first place. Long debates or continual
back-and-forth without resolution are wastes of everyone’s time. You’ll never
agree on everything, but you can quickly discover what you do agree on and
increase consensus over time.
Your team can establish initial working agreements as part of team char-
tering activities. Liftoff [LN17] is a great guide for facilitating effective
chartering sessions.
Establishing Standards
You’ll want to derive some standards around unit testing. Start minimally.
Answer two questions:
• What code (and test) related elements are wasting our time?
• What simple standards can we quickly agree on?
Run a sub-hour discussion that results in a short list of standards, or better,
in a code example that clearly embodies the standards. Over time, ensure
that standards stay relevant and followed. Reference them when violated,
review them when disagreement arises, and revise them as needed.
Chapter 12. Adopting Team Practices • 236
report erratum  •  discuss


