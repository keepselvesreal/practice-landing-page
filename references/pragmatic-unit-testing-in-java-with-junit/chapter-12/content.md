# Adopting Team Practices (pp.235-245)

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


---
**Page 237**

Here’s a short, incomplete list of unit test practices to standardize on:
• Which tests developers should run prior to check-in
• How to name test classes and test methods
• Whether to use JUnit’s assertions or an assertion library like AssertJ
• Whether to use AAA or not
• Which mock tool to prefer
• Whether to prohibit console output on test runs (please do)
• How to identify and discourage slow tests in the unit test suite
Your team should quickly adopt and adhere to most of these standards. Some
will require continual vigilance, such as eliminating all console output from
a test run. You might be able to automate solutions to ensure people comply;
otherwise, you might find yourself continually pestering folks. You might also
find that some standards just aren’t worth the effort.
Increasing Quality with Post Facto Reviews
To ensure everyone adheres to standards, your team must exert collective
peer pressure through some form of code review. Your team’s investment in
code and unit tests is too expensive to allow individuals to do anything they
want to the codebase.
Many teams require pull requests (PRs)—a feature most closely associated
with GitHub. A developer submits a pull request for a chunk of work deemed
ready for integration into the main branch. GitHub notifies the rest of the
team, who reviews and comments on changes made. Reviewers approve a
request by pulling (merging) it into the main branch.
The PR process has become a preferred standard in many organizations.
While it appears efficient, the PR process is the least effective of the review
mechanisms. That’s because it is the least agile—it attempts to streamline
reviews by minimizing face-to-face human interaction.
1
You might initiate review sessions where unit test producers solicit feedback
from others on the team. Such post facto reviews can range from informal
code walkthroughs to fairly formal processes like Fagan inspections, which
are designed to streamline and standardize the review.
2
When using Fagan inspections, the person creating the document—the thing
to be reviewed (usually code)—is responsible for soliciting reviewers, much
as when doing PRs. A meeting is typically held a couple of days later, which
1.
https://medium.com/pragmatic-programmers/prs-shift-left-please-part-one-b0f8bb79ef2b
2.
http://en.wikipedia.org/wiki/Fagan_inspection
report erratum  •  discuss
Getting on the Same Page with Your Team • 237


---
**Page 238**

allows time for reviewers to take a look at the changes. Prior to the meeting,
reviewers make note of defects and categorize them based on severity.
The inspection meeting is designed to go fast. Only the most severe problems
are described, and discussions are constrained to clarifications only.
Expressly prohibited during the meeting is “solutioning” any problem.
The document producer takes away the list of all problems (including ones
that aren’t severe) and fixes them as appropriate. A follow-up meeting to dis-
cuss the resolution can be held if needed.
Fagan inspections seem similar to PRs in that both are designed to be
streamlined. But they also involve face-to-face communication, which can
help eliminate misunderstandings. The opportunity to interact also helps a
team refine what’s truly important to focus on when doing reviews.
The PR process, Fagan inspections, and things like code walkthroughs are
all post facto—they occur after the code in question was produced. For that
reason, they all suffer from a few challenges.
First, reviewers aren’t usually familiar with the intimate details of the code
product being reviewed. The best reviews—the ones that find problems before
you ship them—come from people with a deep understanding of the code.
The reality in most shops prevents this sort of time investment on the part
of the reviewers—they’re too busy working on their own thing.
As a result, post facto reviews find fewer defects than we’d like. Reviewers can
discover many surface-level defects and style violations. But they often miss
deeper-seated defects related to things you might only think of when you
are deeply immersed in the challenge at hand. Such problems are often
harder to fix after the fact, as they can be deeply intertwined with the existing
solution.
Second, if there are serious problems, after-the-fact reviews come too late.
Once the code is built and seemingly ready, teams are usually under too
much pressure to ship it—by their peers, managers, and even themselves.
They’re not about to step back and significantly rework code that’s purport-
edly already working. As a result, the team takes on problematic software
that will cost them even more to maintain down the road.
In short, post facto reviews are too late and probably barely worth the time
investment they require. Put another way, doing the work, reviewing it,
reworking it, and re-reviewing it is an inefficient process.
Chapter 12. Adopting Team Practices • 238
report erratum  •  discuss


---
**Page 239**

Active Review via Pair Programming
A good review process would let a team review and reject a poor design before
anyone tries to implement it. In the 1990s, much of software development
was driven with design-up-front processes. A team typically invested 30 per-
cent or more of a project producing speculative designs. Development work
did not start until these designs were complete. The designs, based on
exhaustively detailed requirements, were captured as heavy documents with
copious diagrams and models. It worked…for a small number of situations.
Heavy up-front design doesn’t work for most of us because it holds up poorly
to that ever-present thing called change. Also, no matter the amount of up-
front investment, speculative designs are often inadequate or flat-out wrong.
The intent of pair programming, or pairing, is to increase quality. To pair, two
programmers work together side-by-side (or face-to-face remotely) to develop
a two-heads-are-better-than-one solution. Pairing is an active form of
review—its participants review each other’s ideas and code as they code and
fix any problems before moving on. Pair members help each other adhere to
standards and practices like unit testing.
Few practices have drawn as much controversy in the software development
world, however. The thought of working with other developers closely
throughout the day sends many screaming for the exits. Even when practiced
well, pairing incurs a number of overhead costs. It’s also still possible for a
pair to produce a solution that the rest of the team finds problematic.
Don’t dismiss pairing out of hand, however. When done well, even active resisters
can become converts, perhaps due to the increase in quality. Some find its
highly interactive, collaborative aspect gratifying. The PragPub article “Pair
Programming Benefits”
3 describes some potentials for its ROI. Another article,
“Pair Programming in a Flash,”
4 lays out ground rules for successful pairing
and points out a few pitfalls to avoid.
Pair swapping can be valuable. Before a task is considered complete, a new
person replaces one of the starting pair’s developers. This third party provides
the perspective of someone not intimately involved in creating the current
solution. They can help correct clarity and other issues not seen by the original
pair. Recognize that to some extent, though, the process has reverted to work-
review-rework—the new party is identifying and helping fix problems that
might not have existed had they arrived sooner.
3.
https://langrsoft.com/ftp/pragpub-2011-07.pdf
4.
https://langrsoft.com/ftp/pragpub-2011-06.pdf
report erratum  •  discuss
Getting on the Same Page with Your Team • 239


---
**Page 240**

Active Review via Mob Programming
Maybe the answer is to have the whole team actively review everything related
to delivering a feature—the design, tests, code, and anything else required—as
that same team builds it all. This is the idea behind the nearly 15-year-old
practice known as mob programming or ensemble programming.
While its name might suggest chaos, proper mob programming requires the
team to work together in a structured manner in the same virtual or physical
space. It’s not “throw everyone in a room and see what happens.”
When mob programming, one person acts as a driver whose job is to listen
to the rest of the mob—the navigators—and translate their direction into code.
Physically and in person, this means that the driver is the only one typing at
a keyboard; the rest of the mob watches on a shared monitor.
After a short period of time— maybe a handful of minutes—the driver yields
control to another mob member. A driver with a brilliant idea must relinquish
their seat to step the next driver through their thinking.
These two simple rules maximize engagement and minimize domination and
fear. Without structure, a mob usually devolves. A senior team member speeds
off to their desired solution while the rest of the team watches confused and
helpless from the back seat. But with short rotations and a driver who must
follow direction, it becomes difficult for anyone to dominate.
The driver role is a short-lived experience, which can make it less intimidating,
as can the fact that they’re not responsible for knowing what to do. A good
driver ramps up their listening and translating skills. They might start
knowing nothing about a language, requiring detailed direction on its syntax
(“type public static void main, then parentheses, then String[])”). It’s rough at first,
but most drivers quickly improve to the point where they can readily translate
higher-level instruction (“write a method that filters the customer list down
to active customers only”) into code.
Mob programming seems to send fewer folks screaming for the exits than
pairing. That’s possibly because pairing demands continual attention and
forces considerable intimacy between you and each of your teammates. Some
pairs will just never click. In a mob, you’re not “on point” for the entire
development session, unlike when you’re working in a pair.
Mob sessions can be highly effective. Mob programming eliminates a lot of
the cost of splitting the work amongst sub-teams, whether they are pairs or
individuals. Not only can you eliminate review sessions (everyone’s there!),
but ceremonies like standup meetings, iteration planning, and pull requests
Chapter 12. Adopting Team Practices • 240
report erratum  •  discuss


---
**Page 241**

disappear or are greatly simplified. Since everyone is in the room, you find
the problems sooner, you derive a better design that everyone can live with,
you converge on a team coding standard, you have all the expertise available
to use right now, and you write all the tests you need to write.
Most importantly (to me at least), mob sessions are usually a lot of fun, and
I often feel like we got a lot more done.
If you choose to practice either mob or pair programming, you’ll still end up
with some individual work product. Make sure you use a post facto review
process for this work.
Practicing Continuous Integration
“It works on my machine!” cries Joe. “Must be something wrong on yours,”
he says to Lucia.
Hearken to the call of the wild developer, heard ofttimes in olde shops that
weren’t practicing continuous integration (CI). With CI, all developers frequently
integrate their changes with the centralized repository (commonly in GitHub).
A tool known as a CI server monitors the repository. When the repository is
updated, the CI server triggers a new build and runs one or more sets of tests
prior to completion. The first of those test suites to execute is typically your
team’s unit tests.
CI demands a solid suite of fast unit tests.
CI servers can be hosted internally or available in the cloud. The most common
tools are Jenkins, GitHub Actions, and GitLab CI. Some alternative solutions
include Azure DevOps, CircleCI, and TeamCity.
5 Some of the tools are free,
some are licensed, and some are software as a service (SaaS).
The CI build’s tests verify that the integrated codebase works as expected. If
a developer pushes and any CI tests fail, the build fails and the team is notified
of the problem. The unit tests running in CI thus establish a centralized,
authoritative standard.
Broken CI tests indicate a system that cannot be deployed. Resolve
them before doing anything else.
5.
https://blog.jetbrains.com/teamcity/2023/07/best-ci-tools/
report erratum  •  discuss
Practicing Continuous Integration • 241


---
**Page 242**

Tools like Git can be configured to abort commit/push attempts
when unit tests fail locally.
CI is a foundation for practicing continuous deployment (CD), wherein each
successful build triggers a deployment to production. Amazon
6 and Netflix
7
are companies that deploy to production thousands of times daily using CD.
Conflicts and Merges
If two or more separate developers separately make changes to the same
codebase, it’s possible for their combined changes to break the system (even
though the individual contributions worked prior to integration). In order for
CI to work, each developer wishing to push must first pull the latest code
from the central repository. They run their fantastic unit test suite to ensure
nothing is broken and then push up what now becomes the latest version of
the system. If they don’t have a fantastic unit test suite, they must carefully
review the combined code first. (Corollary: folks without a fantastic unit test
suite or some other comprehensive test suite are not usually practicing CI.)
A healthy team that’s created a trustworthy test suite integrates frequently.
Some teams who practice TDD push up every TDD cycle, in other words, as often
as every few minutes. Once they get a new behavior working and clean up the
code, they integrate that new increment. This “continuous” aspect of CI helps
make it work and be successful. Feedback comes sooner and in smaller incre-
ments. It’s easier and faster to find and fix problems in such small increments.
In contrast, developers on less advanced teams defer integrating their changes
until a feature is complete. They typically make their changes on code
branches across the course of a day, a few days, and sometimes a few weeks.
The amount of new code that must subsequently be integrated can be consid-
erable, thus significantly likely to conflict with existing code.
Developers can spend hours, even days, managing a meticulous manual
merge process to integrate a long-lived branch. The correct technical term for
such a nightmare is “merge hell.” The duration of the nightmare often
increases proportionally with the age of the branch.
Better communication and division of labor can help minimize code conflicts
and merge hell. But consider also mob programming (see Active Review via
Mob Programming, on page 240).
6.
https://www.zdnet.com/article/how-amazon-handles-a-new-software-deployment-every-second/
7.
https://www.theserverside.com/feature/How-Netflix-built-tooling-for-multi-cloud-deployment
Chapter 12. Adopting Team Practices • 242
report erratum  •  discuss


---
**Page 243**

An Integration Process Checklist
Here’s a summary of your steps as a developer for practicing continuous
integration:
1.
Pull from your central repo to get your local codebase up to date.
2.
Change the code, running unit tests as you go.
3.
Pull from the repo to integrate any new changes from teammates.
4.
Manually review the incoming changes as appropriate.
5.
Run your tests to ensure that the integrated code works.
6.
Push your changes to the central repository.
Don’t advance to the next step if any of your tests are failing.
A CI process fosters healthy peer pressure against costly code. Developers
quickly habituate themselves to running their unit tests before check-in so
as not to waste their teammates’ time by causing the CI build process to fail.
A CI server is a minimum for building a modern development team.
Summary
You and your team must be on the same page when it comes to unit testing.
If it’s new to your team, it’ll take time to adopt and ingrain as a beneficial
habit. If it’s an existing practice, your team practices might need improvement.
In this chapter, you learned about establishing team-level standards for unit
testing from both implementation and process perspectives. You also learned
about the active review mechanisms that help ensure test quality—specifically,
mob and pair programming. Finally, you discovered the key role that CI plays
in unit testing.
Last up: times are changing rapidly. AI has dramatically made its way into
the software development arena. Unlike previous attempts (anyone remember
Prolog and 4GLs?), AI has made a ubiquitous impact not just in software
development but in day-to-day life for many of us. AI’s improvements are
accelerating and there’s little chance of its disappearance.
Yes, unit testing is quite relevant in the age of AI. Read on to discover how.
report erratum  •  discuss
Summary • 243


---
**Page 245**

CHAPTER 13
Keeping AI Honest with Unit Tests
You’ve learned a number of benefits you can gain from writing unit tests:
fewer defects, of course, but also trustworthy documentation, the ability to
keep your code clean through refactoring, and a dramatic increase in confi-
dence for shipping the system.
AI can generate code, creating increasingly dramatic implications for the
software development industry and you. Yet, unit testing can and will provide
tremendous value in your software development efforts. In this chapter, you’ll
take an approach involving AI generation of both production code and unit
tests. You’ll discover why unit tests remain essential, and you’ll learn how to
incorporate them into a workflow that will give you the confidence to ship.
AI Isn’t Going Away
By the time you read this chapter, the capabilities of artificial intelligence (AI)
will have advanced, perhaps significantly, from when I wrote it (January
2024). At some future point, very possibly within the span of your career,
most (not all) software will be generated by AI.
You will still need to tell your AI assistant what to do.
Today, AI-generated code has limitations. It’s of dubious quality, for one—very
stepwise and highly concrete. Maybe when AI evolves to a point where the
code always works as expected, its quality won’t matter because, at that point,
you might never have to read or write another word of code again. But today,
AI-generated code may contain defects. ChatGPT, for example, perpetually
admits that fact:
ChatGPT can make mistakes. Consider checking important information.
I’ve seen failures often occur when an LLM (Large Language Model) adds a
new feature to an existing body of code, for example. You’ll explore how to
report erratum  •  discuss


