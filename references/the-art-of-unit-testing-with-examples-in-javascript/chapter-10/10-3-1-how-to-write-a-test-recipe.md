# 10.3.1 How to write a test recipe (pp.205-207)

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


---
**Page 206**

206
CHAPTER 10
Developing a testing strategy
Don’t treat test recipes as something formal, though. A test recipe is not a binding
commitment or a list of test cases in a test-planning piece of software. Don’t use it as a
public report, a user story, or any other kind of promise to a stakeholder. At its core, a
recipe is a simple list of 5 to 20 lines of text detailing simple scenarios to be tested in
an automated fashion and at what level. The list can be changed, added to, or sub-
tracted from. Consider it a comment. I usually like to just put it right in the user story
or feature in Jira or whatever program I’m using.
 Here’s an example of what one might look like:
User profile feature testing recipe
E2E – Login, go to profile screen, update email, log out, log in with new 
email, verify profile screen updated
API – Call UpdateProfile API with more complicated data
Conﬁdence
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Happy
scenario
1
Feature 1
Feature 2
Great ROI on this test
Scenario
variation
1.1
Scenario
variation
1.2
Scenario
variation
2.1
Scenario
variation
2.1.2
Scenario
variation
2.1.1
Scenario
variation
1.1.2
Scenario
variation
1.1.1
Scenario
variation
2.1.2
Scenario
variation
2.1.1
Figure 10.5
A test recipe is a test plan, outlining at which level a particular feature should be tested. 


---
**Page 207**

207
10.3
Test recipes as a strategy
Unit test – Check profile update logic with bad email
Unit test – Profile update logic with same email
Unit test – Profile serialization/deserialization
10.3.2 When do I write and use a test recipe?
Just before you start coding a feature or a user story, sit down with another person and
try to come up with various scenarios to be tested. Discuss at which level that scenario
should be best tested. This meeting will usually be no longer than 5 to 15 minutes,
and after it, coding begins, including the writing of the tests. (If you’re doing TDD,
you’ll start with the tests.)
 In organizations where there are automation or QA roles, the developer will write
the lower-level tests, and the QA will focus on writing the higher-level tests, while cod-
ing of the feature is taking place. Both people are working at the same time. One does
not wait for the other to finish their work before starting to write their tests.
 If you are working with feature toggles, they should also be checked as part of the
tests, so that if a feature is off, its tests will not run.
10.3.3 Rules for a test recipe
There are several rules to follow when writing a test recipe:
Faster—Prefer writing tests at lower levels, unless a high-level test is the only way
for you to gain confidence that the feature works.
Confidence—The recipe is done when you can tell yourself, “If all these tests
passed, I’ll feel pretty good about this feature working.” If you can’t say that,
write more scenarios that will allow you to say that.
Revise—Feel free to add or remove tests from the list as you code. Just make
sure you notify the other person you worked with on the recipe.
Just in time—Write this recipe just before starting to code, when you know who
is going to code it.
Pair—Don’t write it alone if you can help it. People think in different ways, and
it’s important to talk through the scenarios and learn from each other about
testing ideas and mindset.
Don’t repeat yourself from other features—If this scenario is already covered by an
existing test (perhaps an E2E test from a previous feature), there is no need to
repeat this scenario at that level.
Don’t repeat yourself from other layers—Try not to repeat the same scenario at multi-
ple levels. If you’re checking a successful login at the E2E level, lower-level tests
should only check variations of that scenario (logging in with different provid-
ers, unsuccessful login results, etc.). 
More, faster—A good rule of thumb is to end up with a ratio of at least one to
five between levels (for one E2E test, you might end up with five or more lower-
level tests).


