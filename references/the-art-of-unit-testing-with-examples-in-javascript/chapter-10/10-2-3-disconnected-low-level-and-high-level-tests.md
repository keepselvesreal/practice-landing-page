# 10.2.3 Disconnected low-level and high-level tests (pp.204-205)

---
**Page 204**

204
CHAPTER 10
Developing a testing strategy
10.2.3 Disconnected low-level and high-level tests
This pattern might seem healthy at first, but it really isn’t. It might look a bit like fig-
ure 10.4.
Yes, you want to have both low-level tests (for speed) and high-level tests (for confi-
dence). But when you see something like this in an organization, you will likely
encounter one or more of these anti-behaviors:
Many of the tests repeat in multiple levels.
The people who write the low-level tests are not the same people who write the
high-level tests. This means they don’t care about each other’s test results, and
Most speed
• Easier to maintain
• Easier to write
• Faster feedback loop
Most conﬁdence
• Harder to maintain
• Harder to write
• Slower feedback loop
Conﬁdence
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Scenario
1
Scenario
1.1
Scenario
1.2
Scenario
1.3
Scenario
1.4
Scenario
1.5
Scenario
1
Scenario
1.6
Scenario
1.2
Scenario
1.10
Scenario
1.4
Scenario
1.5
Scenario
1.9
Figure 10.4
Disconnected low-level and high-level tests


---
**Page 205**

205
10.3
Test recipes as a strategy
they’ll likely have different pipelines execute the different test types. When one
pipeline is red, the other group might not even know nor care that those tests
are failing.
We suffer the worst of both worlds: at the top level, we suffer from the long test
times, difficult maintainability, build whisperers, and flakiness; at the bottom
level, we suffer from lack of confidence. And because there is often a lack of
communication, we don’t get the speed benefit of the low-level tests because
they repeat at the top anyway. We also don’t get the top-level confidence
because of how flaky such a large number of tests is. 
This pattern often happens when we have separate test and a development organiza-
tions with different goals and metrics, as well as different jobs and pipelines, permis-
sions, and even code repositories. The larger the company, the more likely this is to
happen. 
10.3
Test recipes as a strategy
My proposed strategy to achieve balance in the types of tests used by the organization
is to use test recipes. The idea is to have an informal plan for how a particular feature is
going to be tested. This plan should include not only the main scenario (also known
as the happy path), but also all its significant variations (also known as edge cases), as
shown in figure 10.5. A well-outlined test recipe gives a clear picture of what test level
is appropriate for each scenario.
10.3.1 How to write a test recipe
It’s best to have at least two people create a test recipe—hopefully one with a devel-
oper’s point of view and one with a tester’s point of view. If there is no test depart-
ment, two developers, or a developer with a senior developer will suffice. Mapping
each scenario to a specific level in the test hierarchy can be a highly subjective task, so
two pairs of eyes will help keep each other’s implicit assumptions in check.
 The recipes themselves can be stored as extra text in a TODO list or as part of the
feature story on the tracking board for the task. You don’t need a separate tool for
planning tests. 
 The best time to create a test recipe is just before you start working on the feature.
This way, the test recipe becomes part of the definition of “done” for the feature,
meaning the feature is not complete until the full test recipe is passing.
 Of course, a recipe can change as time goes by. The team can add or remove sce-
narios from it. A recipe is not a rigid artifact but a continuous work in progress, just
like everything else in software development.
 A test recipe represents the list of scenarios that will give its creators “pretty good
confidence” that the feature works. As a rule of thumb, I like to have a 1 to 5 or 1 to 10
ratio between levels of tests. For any high-level, E2E test, I might have 5 tests at a lower
level. Or, if you think bottom-up, say you have 100 unit tests. You usually won’t need to
have more than 10 integration tests and 1 E2E test. 


