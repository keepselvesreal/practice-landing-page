# 5.2 Start Each Feature with an Acceptance Test (pp.39-40)

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


---
**Page 40**

Figure 5.1
Each TDD cycle starts with a failing acceptance test
us focused on implementing the limited set of features they describe, improving
our chances of delivering them. More subtly, starting with tests makes us look
at the system from the users’ point of view, understanding what they need it to
do rather than speculating about features from the implementers’ point of view.
Unit tests, on the other hand, exercise objects, or small clusters of objects, in
isolation. They’re important to help us design classes and give us conﬁdence that
they work, but they don’t say anything about whether they work together with
the rest of the system. Acceptance tests both test the integration of unit-tested
objects and push the project forwards.
Separate Tests That Measure Progress from Those That
Catch Regressions
When we write acceptance tests to describe a new feature, we expect them to fail
until that feature has been implemented; new acceptance tests describe work yet
to be done. The activity of turning acceptance tests from red to green gives the
team a measure of the progress it’s making. A regular cycle of passing acceptance
tests is the engine that drives the nested project feedback loops we described in
“Feedback Is the Fundamental Tool” (page 4). Once passing, the acceptance tests
now represent completed features and should not fail again. A failure means that
there’s been a regression, that we’ve broken our existing code.
We organize our test suites to reﬂect the different roles that the tests fulﬁll.
Unit and integration tests support the development team, should run quickly,
and should always pass. Acceptance tests for completed features catch
regressions and should always pass, although they might take longer to run.
New acceptance tests represent work in progress and will not pass until a feature
is ready.
If requirements change, we must move any affected acceptance tests out of the
regression suite back into the in-progress suite, edit them to reﬂect the new
requirements, and change the system to make them pass again.
Chapter 5
Maintaining the Test-Driven Cycle
40


