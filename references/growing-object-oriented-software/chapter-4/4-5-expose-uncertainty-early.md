# 4.5 Expose Uncertainty Early (pp.36-39)

---
**Page 36**

We use the automation of building and testing to give us feedback on qualities
of the system, such as how easily we can cut a version and deploy, how well the
design works, and how good the code is. The automated deployment helps us
release frequently to real users, which gives us feedback on how well we have
understood the domain and whether seeing the system in practice has changed
our customer’s priorities.
The great beneﬁt is that we will be able to make changes in response to what-
ever we learn, because writing everything test-ﬁrst means that we will have a
thorough set of regression tests. No tests are perfect, of course, but in practice
we’ve found that a substantial test suite allows us to make major changes safely.
Expose Uncertainty Early
All this effort means that teams are frequently surprised by the time it takes to
get a “walking skeleton” working, considering that it does hardly anything.
That’s because this ﬁrst step involves establishing a lot of infrastructure and
asking (and answering) many awkward questions. The time to implement the
ﬁrst few features will be unpredictable as the team discovers more about its re-
quirements and target environment. For a new team, this will be compounded
by the social stresses of learning how to work together.
Fred Tingey, a colleague, once observed that incremental development can be
disconcerting for teams and management who aren’t used to it because it front-
loads the stress in a project. Projects with late integration start calmly but gener-
ally turn difﬁcult towards the end as the team tries to pull the system together
for the ﬁrst time. Late integration is unpredictable because the team has to
assemble a great many moving parts with limited time and budget to ﬁx any
failures. The result is that experienced stakeholders react badly to the instability
at the start of an incremental project because they expect that the end of the
project will be much worse.
Our experience is that a well-run incremental development runs in the opposite
direction. It starts unsettled but then, after a few features have been implemented
and the project automation has been built up, settles in to a routine. As a project
approaches delivery, the end-game should be a steady production of functionality,
perhaps with a burst of activity before the ﬁrst release. All the mundane but
brittle tasks, such as deployment and upgrades, will have been automated so that
they “just work.” The contrast looks rather like Figure 4.4.
This aspect of test-driven development, like others, may appear counter-
intuitive, but we’ve always found it worth taking enough time to structure and
automate the basics of the system—or at least a ﬁrst cut. Of course, we don’t
want to spend the whole project setting up a perfect “walking skeleton,” so we
limit ourselves to whiteboard-level decisions and reserve the right to change our
mind when we have to. But the most important thing is to have a sense of direction
and a concrete implementation to test our assumptions.
Chapter 4
Kick-Starting the Test-Driven Cycle
36


---
**Page 37**

Figure 4.4
Visible uncertainty in test-ﬁrst and test-later projects
A “walking skeleton” will ﬂush out issues early in the project when there’s
still time, budget, and goodwill to address them.
Brownﬁeld Development
We don’t always have the luxury of building a new system from the ground up.
Many of our projects have started with an existing system that must be extended,
adapted, or replaced. In such cases, we can’t start by building a “walking skeleton”;
we have to work with what already exists, no matter how hostile its structure.
That said, the process of kick-starting TDD of an existing system is not fundamen-
tally different from applying it to a new system—although it may be orders of
magnitude more difﬁcult because of the technical baggage the system already
carries. Michael Feathers has written a whole book on the topic, [Feathers04].
It is risky to start reworking a system when there are no tests to detect regressions.
The safest way to start the TDD process is to automate the build and deploy pro-
cess, and then add end-to-end tests that cover the areas of the code we need to
change. With that protection, we can start to address internal quality issues with
more conﬁdence, refactoring the code and introducing unit tests as we add func-
tionality.
The easiest way to start building an end-to-end test infrastructure is with the sim-
plest path through the system that we can ﬁnd. Like a “walking skeleton,” this lets
us build up some supporting infrastructure before we tackle the harder problems
of testing more complicated functionality.
37
Expose Uncertainty Early


---
**Page 38**

This page intentionally left blank 


---
**Page 39**

Chapter 5
Maintaining the Test-Driven
Cycle
Every day you may make progress. Every step may be fruitful. Yet there
will stretch out before you an ever-lengthening, ever-ascending,
ever-improving path. You know you will never get to the end of the
journey. But this, so far from discouraging, only adds to the joy and
glory of the climb.
—Winston Churchill
Introduction
Once we’ve kick-started the TDD process, we need to keep it running smoothly.
In this chapter we’ll show how a TDD process runs once started. The rest of the
book explores in some detail how we ensure it runs smoothly—how we write
tests as we build the system, how we use tests to get early feedback on internal
and external quality issues, and how we ensure that the tests continue to support
change and do not become an obstacle to further development.
Start Each Feature with an Acceptance Test
As we described in Chapter 1, we start work on a new feature by writing failing
acceptance tests that demonstrate that the system does not yet have the feature
we’re about to write and track our progress towards completion of the
feature (Figure 5.1).
We write the acceptance test using only terminology from the application’s
domain, not from the underlying technologies (such as databases or web servers).
This helps us understand what the system should do, without tying us to any of
our initial assumptions about the implementation or complicating the test with
technological details. This also shields our acceptance test suite from changes to
the system’s technical infrastructure. For example, if a third-party organization
changes the protocol used by their services from FTP and binary ﬁles to web
services and XML, we should not have to rework the tests for the system’s
application logic.
We ﬁnd that writing such a test before coding makes us clarify what we want
to achieve. The precision of expressing requirements in a form that can be auto-
matically checked helps us uncover implicit assumptions. The failing tests keep
39


