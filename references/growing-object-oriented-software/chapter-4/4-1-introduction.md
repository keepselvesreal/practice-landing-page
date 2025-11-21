# 4.1 Introduction (pp.31-32)

---
**Page 31**

Chapter 4
Kick-Starting the Test-Driven
Cycle
We should be taught not to wait for inspiration to start a thing. Action
always generates inspiration. Inspiration seldom generates action.
—Frank Tibolt
Introduction
The TDD process we described in Chapter 1 assumes that we can grow the system
by just slotting the tests for new features into an existing infrastructure. But what
about the very ﬁrst feature, before we have this infrastructure? As an acceptance
test, it must run end-to-end to give us the feedback we need about the system’s
external interfaces, which means we must have implemented a whole automated
build, deploy, and test cycle. This is a lot of work to do before we can even see
our ﬁrst test fail.
Deploying and testing right from the start of a project forces the team to un-
derstand how their system ﬁts into the world. It ﬂushes out the “unknown
unknown” technical and organizational risks so they can be addressed while
there’s still time. Attempting to deploy also helps the team understand who they
need to liaise with, such as system administrators or external vendors, and start
to build those relationships.
Starting with “build, deploy, and test” on a nonexistent system sounds odd,
but we think it’s essential. The risks of leaving it to later are just too high. We
have seen projects canceled after months of development because they could not
reliably deploy their system. We have seen systems discarded because new features
required months of manual regression testing and even then the error rates were
too high. As always, we view feedback as a fundamental tool, and we want to
know as early as possible whether we’re moving in the right direction. Then,
once we have our ﬁrst test in place, subsequent tests will be much quicker to write.
31


---
**Page 32**

First, Test a Walking Skeleton
The quandary in writing and passing the ﬁrst acceptance test is that it’s hard to
build both the tooling and the feature it’s testing at the same time. Changes in
one disrupt any progress made with the other, and tracking down failures is
tricky when the architecture, the tests, and the production code are all moving.
One of the symptoms of an unstable development environment is that there’s no
obvious ﬁrst place to look when something fails.
We can cut through this “ﬁrst-feature paradox” by splitting it into two smaller
problems. First, work out how to build, deploy, and test a “walking skeleton,”
then use that infrastructure to write the acceptance tests for the ﬁrst meaningful
feature. After that, everything will be in place for test-driven development of the
rest of the system.
A “walking skeleton” is an implementation of the thinnest possible slice of
real functionality that we can automatically build, deploy, and test end-to-end
[Cockburn04]. It should include just enough of the automation, the major com-
ponents, and communication mechanisms to allow us to start working on the
ﬁrst feature. We keep the skeleton’s application functionality so simple that it’s
obvious and uninteresting, leaving us free to concentrate on the infrastructure.
For example, for a database-backed web application, a skeleton would show a
ﬂat web page with ﬁelds from the database. In Chapter 10, we’ll show an example
that displays a single value in the user interface and sends just a handshake
message to the server.
It’s also important to realize that the “end” in “end-to-end” refers to the pro-
cess, as well as the system. We want our test to start from scratch, build a deploy-
able system, deploy it into a production-like environment, and then run the tests
through the deployed system. Including the deployment step in the testing process
is critical for two reasons. First, this is the sort of error-prone activity that should
not be done by hand, so we want our scripts to have been thoroughly exercised
by the time we have to deploy for real. One lesson that we’ve learned repeatedly
is that nothing forces us to understand a process better than trying to automate
it. Second, this is often the moment where the development team bumps into the
rest of the organization and has to learn how it operates. If it’s going to take six
weeks and four signatures to set up a database, we want to know now, not
two weeks before delivery.
In practice, of course, real end-to-end testing may be so hard to achieve that
we have to start with infrastructure that implements our current understanding
of what the real system will do and what its environment is. We keep in mind,
however, that this is a stop-gap, a temporary patch until we can ﬁnish the job,
and that unknown risks remain until our tests really run end-to-end. One of the
weaknesses of our Auction Sniper example (Part III) is that the tests run against
Chapter 4
Kick-Starting the Test-Driven Cycle
32


