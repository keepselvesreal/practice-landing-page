# 12.2 Getting on the Same Page with Your Team (pp.236-241)

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


