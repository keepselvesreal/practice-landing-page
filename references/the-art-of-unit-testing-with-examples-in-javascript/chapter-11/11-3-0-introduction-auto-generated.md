# 11.3.0 Introduction [auto-generated] (pp.222-223)

---
**Page 222**

222
CHAPTER 11
Integrating unit testing into the organization
Skills—Track that we are slowly removing knowledge barriers inside teams or
across teams
Learning—Acting like we’re a learning organization
QUALITATIVE METRICS
The metrics are mostly quantitative (i.e., they are numbers that can be measured), but
a few are qualitative, in that you ask people how they feel or think about something.
The ones I use are
How confident you are that the tests can and will find bugs in the code if they
arise (from 1 to 5)? Take the average of the responses from the team members
or across multiple teams.
Does the code do what it is supposed to do (from 1 to 5)?
These are surveys you can ask at each retrospective meeting, and they take five min-
utes to answer. 
TREND LINES ARE YOUR FRIEND
For all leading and lagging indicators, you want to see trend lines, not just snapshots of
numbers. Lines over time is how you see if you’re getting better or worse. 
 Don’t fall into the trap of having a nice dashboard with large numbers on it. Num-
bers without context are not good or bad. Trend lines tell you if you’re better this
week than you were last week. 
11.2.7 Realize that there will be hurdles
There are always hurdles. Most will come from within the organizational structure,
and some will be technical. The technical ones are easier to fix, because it’s a matter
of finding the right solution. The organizational ones need care and attention and a
psychological approach.
 It’s important not to surrender to a feeling of temporary failure when an iteration
goes bad, tests go slower than expected, and so on. It’s sometimes hard to get going,
and you’ll need to persist for at least a couple of months to start feeling comfortable
with the new process and to iron out all the kinks. Have management commit to con-
tinuing for at least three months even if things don’t go as planned. It’s important to
get their agreement up front. You don’t want to be running around trying to convince
people in the middle of a stressful first month.
 Also, absorb this short realization, shared by Tim Ottinger on Twitter (@Tottinge):
“If your tests don’t catch all defects, they still make it easier to fix the defects they
didn’t catch. It is a profound truth.”
 Now that we’ve looked at ways of ensuring things go right, let’s look at some things
that can lead to failure.
11.3
Ways to fail
In the preface to this book, I talked about one project I was involved with that failed,
partly because unit testing wasn’t implemented correctly. That’s one way a project can


---
**Page 223**

223
11.3
Ways to fail
fail. I’ll discuss several others here, along with one that cost me that project, and some
things that can be done about them.
11.3.1 Lack of a driving force
In the places where I’ve seen change fail, the lack of a driving force was the most pow-
erful factor in play. Being a consistent driving force of change has its price. It will take
time away from your normal job to teach others, help them, and wage internal politi-
cal wars for change. You need to be willing to surrender time for these tasks, or the
change won’t happen. Bringing in an outside person, as mentioned in section 11.2.4,
will help you in your quest for a consistent driving force.
11.3.2 Lack of political support
If your boss explicitly tells you not to make the change, there isn’t a whole lot you can
do, besides trying to convince management to see what you see. But sometimes the
lack of support is much more subtle than that, and the trick is to realize that you’re
facing opposition. 
 For example, you may be told, “Sure, go ahead and implement those tests. We’re
adding 10% to your time to do this.” Anything below 30% isn’t realistic for beginning
a unit testing effort. This is one way a manager may try to stop a trend—by choking it
out of existence. 
 You need to recognize that you’re facing opposition, but once you know what to
look for, it’s easy to identify. When you tell them that their limitations aren’t realistic,
you’ll be told, “So don’t do it.”
11.3.3 Ad hoc implementations and first impressions
If you’re planning to implement unit testing without prior knowledge of how to write
good unit tests, do yourself one big favor: involve someone who has experience and
follow good practices (such as those outlined in this book). 
 I’ve seen developers jump into the deep water without a proper understanding of
what to do or where to start, and that’s not a good place to be. Not only will it take a
huge amount of time to learn how to make changes that are acceptable for your situa-
tion, but you’ll also lose a lot of credibility along the way for starting out with a bad
implementation. This can lead to the pilot project being shut down.
 If you read this book’s preface, you’ll know that this happened to me. You have
only a couple of months to get things up to speed and convince the higher-ups that
you’re achieving results with experiments. Make that time count, and remove any risks
that you can. If you don’t know how to write good tests, read a book or get a consul-
tant. If you don’t know how to make your code testable, do the same. Don’t waste time
reinventing testing methods.


