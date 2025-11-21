# 4.2 First, Test a Walking Skeleton (pp.32-33)

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


---
**Page 33**

a dummy server, not the real site. At some point before going live, we would
have had to test against Southabee’s On-Line; the earlier we can do that, the
easier it will be for us to respond to any surprises that turn up.
Whilst building the “walking skeleton,” we concentrate on the structure and
don’t worry too much about cleaning up the test to be beautifully expressive.
The walking skeleton and its supporting infrastructure are there to help us work
out how to start test-driven development. It’s only the ﬁrst step toward a complete
end-to-end acceptance-testing solution. When we write the test for the ﬁrst feature,
then we need to “write the test you want to read” (page 42) to make sure that
it’s a clear expression of the behavior of the system.
The Importance of Early End-to-End Testing
We joined a project that had been running for a couple of years but had never
tested their entire system end-to-end. There were frequent production outages
and deployments often failed. The system was large and complex, reﬂecting the
complicated business transactions it managed.The effort of building an automated,
end-to-end test suite was so large that an entire new team had to be formed to
perform the work. It took them months to build an end-to-end test environment,
and they never managed to get the entire system covered by an end-to-end
test suite.
Because the need for end-to-end testing had not inﬂuenced its design, the system
was difﬁcult to test. For example, the system’s components used internal timers
to schedule activities, some of them days or weeks into the future. This made it
very difﬁcult to write end-to-end tests: It was impractical to run the tests in real-
time but the scheduling could not be inﬂuenced from outside the system. The
developers had to redesign the system itself so that periodic activities were trig-
gered by messages sent from a remote scheduler which could be replaced in the
test environment; see “Externalize Event Sources” (page 326).This was a signiﬁ-
cant architectural change—and it was very risky because it had to be performed
without end-to-end test coverage.
Deciding the Shape of the Walking Skeleton
The development of a “walking skeleton” is the moment when we start to make
choices about the high-level structure of our application. We can’t automate the
build, deploy, and test cycle without some idea of the overall structure. We don’t
need much detail yet, just a broad-brush picture of what major system components
will be needed to support the ﬁrst planned release and how they will communicate.
Our rule of thumb is that we should be able to draw the design for the “walking
skeleton” in a few minutes on a whiteboard.
33
Deciding the Shape of the Walking Skeleton


