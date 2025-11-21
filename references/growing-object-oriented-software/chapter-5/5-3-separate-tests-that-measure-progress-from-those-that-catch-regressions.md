# 5.3 Separate Tests That Measure Progress from Those That Catch Regressions (pp.40-41)

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


---
**Page 41**

Start Testing with the Simplest Success Case
Where do we start when we have to write a new class or feature? It’s tempting
to start with degenerate or failure cases because they’re often easier. That’s a
common interpretation of the XP maxim to do “the simplest thing that could
possibly work” [Beck02], but simple should not be interpreted as simplistic.
Degenerate cases don’t add much to the value of the system and, more important-
ly, don’t give us enough feedback about the validity of our ideas. Incidentally,
we also ﬁnd that focusing on the failure cases at the beginning of a feature is bad
for morale—if we only work on error handling it feels like we’re not achieving
anything.
We prefer to start by testing the simplest success case. Once that’s working,
we’ll have a better idea of the real structure of the solution and can prioritize
between handling any possible failures we noticed along the way and further
success cases. Of course, a feature isn’t complete until it’s robust. This isn’t an
excuse not to bother with failure handling—but we can choose when we want
to implement ﬁrst.
We ﬁnd it useful to keep a notepad or index cards by the keyboard to jot down
failure cases, refactorings, and other technical tasks that need to be addressed.
This allows us to stay focused on the task at hand without dropping detail. The
feature is ﬁnished only when we’ve crossed off everything on the list—either
we’ve done each task or decided that we don’t need to.
Iterations in Space
We’re writing this material around the fortieth anniversary of the ﬁrst Moon landing.
The Moon program was an excellent example of an incremental approach (although
with much larger stakes than we’re used to). In 1967, they proposed a series of
seven missions, each of which would be a step on the way to a landing:
1.
Unmanned Command/Service Module (CSM) test
2.
Unmanned Lunar Module (LM) test
3.
Manned CSM in low Earth orbit
4.
Manned CSM and LM in low Earth orbit
5.
Manned CSM and LM in an elliptical Earth orbit with an apogee of 4600 mi
(7400 km)
6.
Manned CSM and LM in lunar orbit
7.
Manned lunar landing
At least in software, we can develop incrementally without building a new rocket
each time.
41
Start Testing with the Simplest Success Case


