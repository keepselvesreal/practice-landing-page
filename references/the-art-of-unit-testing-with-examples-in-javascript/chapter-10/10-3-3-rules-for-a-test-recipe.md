# 10.3.3 Rules for a test recipe (pp.207-208)

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


---
**Page 208**

208
CHAPTER 10
Developing a testing strategy
Pragmatic—Don’t feel the need to write tests at all levels for a given feature.
Some features or user stories might only require unit tests. Others, only API or
E2E tests. The basic idea is that, if all the scenarios in the recipe pass, you
should feel confidence, regardless of what level they are tested at. If that’s not
the case, move the scenarios around to different levels until you feel more con-
fident, without sacrificing too much speed or maintenance burden.
By following these rules, you’ll get the benefit of fast feedback, because most of your
tests will be low level, while not sacrificing confidence because the few most important
scenarios are still covered by high-level tests. The test recipe approach also allows you
to avoid most of the repetition between tests by positioning scenario variations at lev-
els lower than the main scenario. Finally, if QA people are involved in writing test rec-
ipes too, you’ll form a new communication channel between people within your
organization, which helps improve mutual understanding of your software project.
10.4
Managing delivery pipelines
What about performance tests? Security tests? Load tests? What about lots of other
tests that might take ages to run? Where and when should we run them? Which layer
are they? Should they be part of our automated pipeline?
 Lots of organizations run those tests as part of the integration automated pipeline
that runs for each release or pull request. However, this causes huge delays in feed-
back, and the feedback is often “failed,” even though the failure is not essential for a
release to go out for these types of tests.
 We can divide these types of tests into two main groups:
Delivery-blocking tests—These are tests that provide a go or no-go for the change
that is about to be released and deployed. Unit, E2E, system, and security tests
all fall into this category. Their feedback is binary: they either pass and
announce that the change didn’t introduce any bugs, or they fail and indicate
that the code needs to be fixed before it’s released.
Good-to-know tests—These are tests created for the purpose of discovery and con-
tinuous monitoring of key performance indicator (KPI) metrics. Examples
include code analysis and complexity scanning, high-load performance testing,
and other long-running nonfunctional tests that provide nonbinary feedback. If
these tests fail, we might add new work items to our next sprints, but we would
still be OK releasing our software.
10.4.1 Delivery vs. discovery pipelines
We don’t want our good-to-know tests to take valuable feedback time from our deliv-
ery process, so we’ll also have two types of pipelines:
Delivery pipeline—Used for delivery-blocking tests. When the pipeline is green,
we should be confident that we can automatically release the code to produc-
tion. Tests in this pipeline should provide relatively fast feedback.


