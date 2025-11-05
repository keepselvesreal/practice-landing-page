# Developing a testing strategy (pp.194-213)

---
**Page 194**

194
Developing
a testing strategy
Unit tests represent just one of the types of tests you could and should write. In this
chapter, we’ll discuss how unit testing fits into an organizational testing strategy. As
soon as we start to look at other types of tests, we start asking some really important
questions:
At what level do we want to test various features? (UI, backend, API, unit,
etc.)
How do we decide at which level to test a feature? Do we test it multiple times
on many levels?
Should we have more functional end-to-end tests or more unit tests?
This chapter covers
Testing level pros and cons
Common antipatterns in test levels
The test recipe strategy
Delivery-blocking and non-blocking tests
Delivery vs. discovery pipelines
Test parallelization


---
**Page 195**

195
10.1
Common test types and levels
How can we optimize the speed of tests without sacrificing trust in them?
Who should write each type of test? 
The answers to these questions, and many more, are what I’d call a testing strategy. 
 The first step in our journey is to frame the scope of the testing strategy in terms of
test types. 
10.1
Common test types and levels
Different industries might have different test types and levels. Figure 10.1, which we
first discussed in chapter 7, is a rather generic set of test types that I feel fits 90% of the
organizations I consult with, if not more. The higher the level of the tests, the more
real dependencies they use, which gives us confidence in the overall system’s correct-
ness. The downside is that such tests are slower and flakier.
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
Figure 10.1
Common software test levels 


---
**Page 196**

196
CHAPTER 10
Developing a testing strategy
Nice diagram, but what do we do with it? We use it when we design a framework for
decision making about which test to write. There are several criteria (things that
make our jobs easier or harder) I like to pinpoint; these help me decide which test
type to use.
10.1.1 Criteria for judging a test
When we’re faced with more than two options to choose from, one of the best ways
I’ve found to help me decide is to figure out what my obvious values are for the prob-
lem at hand. These obvious values are the things we can all pretty much agree are use-
ful or should be avoided when making the choice. Table 10.1 lists my obvious values
for tests.
All values are scaled from 1 to 5. As you’ll see, each level in figure 10.1 has pros and
cons in each of these criteria. 
10.1.2 Unit tests and component tests
Unit tests and component tests are the types of tests we’ve been discussing in this book
so far. They both fit under the same category, with the only differentiation being that
component tests might have more functions, classes, or components as part of the
unit of work. In other words, component tests include more “stuff” between the entry
and exit points.
 Here are two test examples to illustrate the difference:
Test A—A unit test of a custom UI button object in memory. You can instantiate
it, click it, and see that it triggers some form of click event. 
Test B—A component test that instantiates a higher-level form component and
includes the button as part of its structure. The test verifies the higher-level
form, with the button playing a small role as part of the higher-level scenario.
Table 10.1
Generic test scorecard
Criterion
Rating scale
Notes
Complexity
1–5
How complicated a test is to write, read, or debug. 
Lower is better. 
Flakiness
1–5
How likely a test is to fail because of things it does 
not control—code from other groups, networks, data-
bases, configuration, and more. Lower is better.
Confidence when passes
1–5
How much confidence is generated in our minds and 
hearts when a test passes. Higher is better.  
Maintainability
1–5
How often the test needs to change, and how easy it 
is to change. Higher is better. 
Execution speed
1–5
How quickly does the test finish? Higher is better. 


---
**Page 197**

197
10.1
Common test types and levels
Both tests are still unit tests, in memory, and we have full control over all the things
being used; there are no dependencies on files, databases, networks, configuration, or
other things we don’t control. Test A is a lower-level unit test, and test B is a compo-
nent test, or a higher-level unit test. 
 The reason this differentiation needs to be made is because I often get asked what
I would call a test with a different level of abstraction. The answer is that whether a test
falls into the unit/component test category is based on the dependencies it does or
doesn’t have, not on the abstraction level it uses. Table 10.2 shows the scorecard for
the unit/component test layer.
10.1.3 Integration tests
Integration tests look almost exactly like regular unit tests, but some of the dependen-
cies are not stubbed out. For example, we might use a real configuration, a real data-
base, a real filesystem, or all three. But to invoke the test, we still instantiate an object
from our production code in memory and invoke an entry point function directly on
that object. Table 10.3 shows the scorecard for integration tests.
Table 10.2
Unit/component test scorecard
Complexity
1/5
These are the least complex of all test types due to the smaller 
scope and the fact that we can control everything in the test.
Flakiness
1/5
These are the least flaky of all test types, since we can control every-
thing in the test. 
Confidence when 
passes
1/5
It feels nice when a unit test passes, but we’re not really confident 
that our application works. We just know that a small piece of it 
does. 
Maintainability
5/5
These are the easiest to maintain out of all test types, since it’s rel-
atively simple to read and to reason about.
Execution speed
5/5
These are the fastest of all test types, since everything runs in mem-
ory without any hard dependencies on files, network, or databases. 
Table 10.3
Integration test scorecard
Complexity
2/5
These tests are slightly or greatly more complex, depending on the 
number of dependencies that we do not fake in the test. 
Flakiness
2–3/5
These tests are slightly or much flakier depending on how many real 
dependencies we use.
Confidence when 
passes
2–3/5
It feels much better when an integration test passes because we are 
verifying that the code uses something we do not control, like a data-
base or a config file. 
Maintainability
3–4/5
These tests are more complex than a unit test because of the depen-
dencies.
Execution speed
3–4/5
These tests are slightly or much slower than a unit test because of 
the dependency on the filesystem, network, database, or threads.


---
**Page 198**

198
CHAPTER 10
Developing a testing strategy
10.1.4 API tests
In previous lower levels of tests, we haven’t needed to deploy the application under
test or make it properly run to test it. At the API test level, we finally need to deploy, at
least in part, the application under test and invoke it through the network. Unlike
unit, component, and integration tests, which can be categorized as in-memory tests,
API tests are out-of-process tests. We are no longer instantiating the unit under test
directly in memory. This means we’re adding a new dependency into the mix: a net-
work, as well as the deployment of some network service. Table 10.4 shows the score-
card for API tests.
10.1.5 E2E/UI isolated tests
At the level of isolated end-to-end (E2E) and user interface (UI) tests, we are testing
our application from the point of view of a user. I use the word isolated to specify that
we are testing only our own application or service, without deploying any dependency
applications or services that our application might need. Such tests fake third-party
authentication mechanisms, the APIs of other applications that are required to be
deployed on the same server, and any code that is not specifically a part of the main
application under test (including apps from the same organization’s other depart-
ments—those would be faked as well). 
 Table 10.5 shows the scorecard for E2E/UI isolated tests.
Table 10.4
API test scorecard
Complexity
3/5
These tests are slightly or greatly more complex, depending on the 
deployment complexity, configuration, and API setup needed. Some-
times we need to include the API schema in the test, which takes 
extra work and thinking.  
Flakiness
3–4/5
The network adds more flakiness to the mix.
Confidence when 
passes
3–4/5
It feels even better when an API test passes. We can trust that others 
can call our API with confidence after deployment. 
Maintainability
2–3/5
The network adds more setup complexity and needs more care when 
changing a test or adding/changing APIs.
Execution speed
2–3/5
The network slows the tests down considerably.
Table 10.5
E2E/UI isolated test scorecard
Complexity
4/5
These tests are much more complex than previous tests, since we are 
dealing with user flows, UI-based changes, and capturing or scraping 
the UI for integration and assertions. Waiting and timeouts abound.
Flakiness
4/5
There are lots of reasons the test may slow down, time out, or not 
work due to the many dependencies involved.
Confidence when 
passes
4/5
It’s a huge relief when this type of test passes. We gain a lot of confi-
dence in our application.


---
**Page 199**

199
10.2
Test-level antipatterns
10.1.6 E2E/UI system tests
At the level of system E2E and UI tests nothing is fake. This is as close to a production
deployment as we can get: all dependency applications and services are real, but they
might be differently configured to allow for our testing scenarios. Table 10.6 shows
the scorecard for E2E/UI system tests.
10.2
Test-level antipatterns
Test-level antipatterns are not technical but organizational in nature. You’ve likely
seen them firsthand. As a consultant, I can tell you that they are very prevalent. 
10.2.1 The end-to-end-only antipattern
A very common strategy that an organization will have is using mostly, if not only, E2E
tests (both isolated and system tests). Figure 10.2 shows what this looks like in the dia-
gram of test levels and types.
 Why is this an antipattern? Tests at this level are very slow, hard to maintain, hard
to debug, and very flaky. These costs remain the same, while the value you get from
each new E2E test diminishes.
DIMINISHING RETURNS FROM E2E TESTS
The first E2E test you write will bring you the most confidence because of how many
other paths of code are included as part of that scenario, and because of the glue—
the code orchestrating the work between your application and other systems—that
gets invoked as part of that test. 
Maintainability
1–2/5
More dependencies add more setup complexity and require more care 
when changing a test or adding or changing workflows. Tests are long 
and usually have multiple steps. 
Execution speed
1–2/5
These tests can be very slow as we navigate user interfaces, some-
times including logins, caching, multipage navigation, etc.
Table 10.6
E2E/UI system test scorecard
Complexity
5/5
These are the most complex tests to set up and write due to the num-
ber of dependencies.
Flakiness
5/5
These tests can fail for any of thousands of different reasons, and 
often for multiple reasons.
Confidence when 
passes
5/5
These tests give us the highest confidence because of all the code 
that gets tested when the tests execute.
Maintainability
1/5
These tests are hard to maintain, due to the many dependencies and 
long workflows.
Execution speed
1/5
These tests are very slow because they use the UI and real depen-
dencies. They can take minutes to hours for a single test.
Table 10.5
E2E/UI isolated test scorecard (continued)


---
**Page 200**

200
CHAPTER 10
Developing a testing strategy
But what about the second E2E test? It will usually be a variation on the first test,
which means it might only bring a small fraction of the same value. Maybe there’s a
difference in a combo box and other UI elements, but all the dependencies, such as
the database and third-party systems, remain the same. 
 The amount of extra confidence you get from the second E2E test is also only a
fraction of the extra confidence you got from the first E2E test. However, the cost
of debugging, changing, reading, and running that test is not a fraction; it is basi-
cally the same as for the previous test. You’re incurring a lot of extra work for a very
small bit of extra confidence, which is why I like to say that E2E tests have quickly
diminishing returns.
 If I want variation on the first test, it would be much more pragmatic to test at a
lower level than the previous test. I already know most, if not all, of the glue between
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
Figure 10.2
End-to-end-only test antipattern


---
**Page 201**

201
10.2
Test-level antipatterns
layers works, from the first test. There’s no need to pay the tax of another E2E test if I
can prove the next scenario at a lower level and pay a much smaller fee for pretty
much the same bit of confidence.
THE BUILD WHISPERER
With E2E tests, not only do we have diminishing returns, we create a new bottleneck
in the organization. Because high-level tests are often flaky, they break for many differ-
ent reasons, some of which are not relevant to the test. You then need special people
in the organization (usually QA leads) to sit down and analyze each of the many
failing tests, and to hunt down the cause and determine if it’s actually a problem or a
minor issue. 
 I call these poor souls build whisperers. When the build is red, which it is most of the
time, build whisperers are the ones who must come in, parse the data, and knowingly
say, after hours of inspection, “Yes, it looks red, but it’s actually green.” 
 Usually, the organization will drive build whisperers into a corner, demanding that
they say the build is green because “We have to get this release out the door.” They are
the gatekeepers of the release, and that is a thankless, stressful, and often manual and
frustrating job. Whisperers usually burn out within a year or two, and they get chewed
up and spit out into the next organization, where they do the same thankless job all
over again. You’ll often see build whisperers when this antipattern of many high-level
E2E tests exists. 
AVOIDING BUILD WHISPERERS
There is a way to resolve this mess, and that’s to create and cultivate robust, automated
test pipelines that can automatically judge whether a build is green or not, even if you
have flaky tests. Netflix has openly blogged about creating their own tool for measur-
ing how a build is doing statistically in the wild, so that it can be automatically
approved for full release deployment (http://mng.bz/BAA1). This is doable, but it
takes time and culture to achieve such a pipeline. I write more about these types of
pipelines in my blog at https://pipelinedriven.org. 
A “THROW IT OVER THE WALL” MENTALITY
Another reason having only E2E tests hurts organizations is that the people in charge
of maintaining and monitoring these tests are people in the QA department. This
means that the organization’s developers might not care about or even know the results
of these builds, and they are not invested in fixing or caring for these tests. They don’t
own them.
 This “throw it over the wall” mentality can cause lots of miscommunication and
quality issues because one part of the organization is not connected to the conse-
quences of its actions, and the other side is suffering the consequences without being
able to control the source of the issue. Is it any wonder that, in many organizations,
developers and QA people don’t get along? The system around them is often
designed to make them mortal enemies instead of collaborators. 


---
**Page 202**

202
CHAPTER 10
Developing a testing strategy
WHEN THIS ANTIPATTERN HAPPENS
These are some reasons why I see this happen:
Separation of duties—Separate QA and development departments with separate
pipelines (automated build jobs and dashboards) exist in many organizations.
When a QA department has its own pipeline, it is likely to write more tests of
the same kind. Also, a QA department tends to write only a specific type of
test—the ones they’re used to and are expected to write (sometimes based on
company policy).
An “if it works, don’t change it” mentality—A group might start with E2E tests and
see that they like the results. They continue to add all their new tests in the
same way, because it’s what they know, and it has proven to be useful. When the
time it takes to run tests gets too long, it’s already too late to change direction
(which relates to the next point).
Sunk-costs fallacy—“We have lots of these types of tests, and if we changed them
or replaced them with lower-level tests, it would mean we’ve wasted all that time
and effort on tests that we are removing.” This is a fallacy, because maintaining,
debugging, and understanding test failures costs a fortune in human time. If
anything, it costs less to delete such tests (keeping only a few basic scenarios)
and get that time back. 
SHOULD YOU AVOID E2E TESTS COMPLETELY?
No, we can’t avoid E2E tests. One of the good things they offer is confidence that the
application works. It’s a completely different level of confidence compared to unit
tests, because they test the integration of the full system, with all of its subsystems
and components, from the point of view of a user. When they pass, the feeling you
get is huge relief that the major scenarios you expect your users to encounter actu-
ally work.
 So don’t avoid them entirely. Instead, I highly recommend minimizing the number
of E2E tests. We’ll talk about what that minimum is in section 10.3.3.
10.2.2 The low-level-only test antipattern
The opposite of having only E2E tests is to have low-level tests only. Unit tests provide
fast feedback, but they don’t provide the amount of confidence needed to fully trust
that your application works as a single integrated unit (see figure 10.3). 
 In this antipattern, the organization’s automated tests are mostly or exclusively low-
level tests, such as unit tests or component tests. There may be hints of integration
tests, but there are no E2E tests in sight.
 The biggest issue with this is that the confidence level you get when these types of
tests pass is simply not enough to feel confident that your application works. That
means people will run the tests and then continue to do manual debugging and test-
ing to get the final sense of confidence needed to release something. Unless what
you’re shipping is a code library that’s meant to be used in the way your unit tests are


---
**Page 203**

203
10.2
Test-level antipatterns
using it, this won’t be enough. Yes, the tests will run quickly, but you’ll still spend lots
of time manually testing and verifying. 
 This antipattern often happens when your developers are only used to writing low-
level tests, if they don’t feel comfortable writing high-level tests, or if they expect the
QA people to write those types of tests.
 Does that mean you should avoid unit tests? Obviously not. But I highly recom-
mend that you have not only unit tests but also higher-level tests. We’ll discuss this rec-
ommendation in section 10.3. 
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
Figure 10.3
Low-level-only test antipattern


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


---
**Page 209**

209
10.4
Managing delivery pipelines
Discovery pipeline—Used for good-to-know tests. This pipeline runs in parallel
with the delivery pipeline, but continuously, and it’s not taken into account as a
release criterion. Since there’s no need to wait for its feedback, tests in this
pipeline can take a long time. If errors are found, they might become new work
items in the next sprints for the team, but releases are not blocked.
Figure 10.6 illustrates the features of these two kinds of pipelines.
The point of the delivery pipeline is to provide a go/no-go check that also deploys our
code if all seems green, perhaps even to production. The point of the discovery pipe-
line is to provide refactoring objectives for the team, such as dealing with code com-
plexity that has become too high. It can also show whether those refactoring efforts
are effective over time. The discovery pipeline does not deploy anything except for
the purpose of running specialized tests or analyzing code and its various KPI metrics.
It ends with numbers on a dashboard. 
 Speed is a big factor in getting teams to be more engaged, and splitting tests into
discovery and delivery pipelines is yet another technique to keep in your arsenal.
10.4.2 Test layer parallelization
Since fast feedback is very important, a common pattern you can and should employ
in many scenarios is to run different test layers in parallel to speed up the pipeline
Auto-triggered
per commit in
source control
Auto-triggered
continuously if
there are changes
Deploy and
report statuses
to dashboards
Report KPIs
to dashboards
Build
Unit tests
API/E2E tests
Security tests
Lint
Code quality
Performance
Load
Delivery
pipeline
Discovery
pipeline
Figure 10.6
Delivery vs. discovery pipelines


---
**Page 210**

210
CHAPTER 10
Developing a testing strategy
feedback, as shown in figure 10.7. You can even use parallel environments that are cre-
ated dynamically and destroyed at the end of the test. 
This approach benefits greatly from having access to dynamic environments. Throw-
ing money at environments and automated parallel tests is almost always much more
effective than throwing money at more people to do more manual tests, or simply
having people wait longer to get feedback because the environment is being used
right now.
 Manual testing is unsustainable because such manual work only increases over
time and becomes more and more frail and error prone. At the same time, simply
waiting longer for pipeline feedback results in a huge waste of time for everyone. The
waiting time, multiplied by the number of people waiting and the number of builds
per day, results in a monthly investment that can be much larger than investing in
dynamic environments and automation. Grab an Excel file and show your manager a
simple formula to get that budget.
 You can parallelize not only stages inside a pipeline; you can go further and run
individual tests in parallel too. For example, if you’re stuck with a large number of
Delivery
pipeline
(parallelized)
Discovery
pipeline
(parallelized)
Auto-triggered
per commit in
source control
Auto-triggered
continuously if
there are
changes
Build
Security tests
Unit tests
API/E2E tests
Wait for all
to ﬁnish
Deploy
Deploy and
report statuses
to dashboards
Report KPIs
to dashboards
Wait for all
to ﬁnish
Auto-triggered
continuously if
there are changes
Code quality
Build
Lint
Performance
Load
Figure 10.7
To speed up delivery, you can run pipelines, and even stages in pipelines, in parallel.


---
**Page 211**

211
Summary
E2E tests, you can break them up into parallel test suites. That shaves a lot of time off
your feedback loop.
Summary
There are multiple levels of tests: unit, component, and integration tests that
run in memory; and API, isolated end-to-end (E2E), and system E2E tests that
run out of process.
Each test can be judged by five criteria: complexity, flakiness, confidence when
it passes, maintainability, and execution speed.
Unit and component tests are best in terms of maintainability, execution speed,
and lack of complexity and flakiness, but they’re worst in terms of the confi-
dence they provide. Integration and API tests are the middle ground in the
trade-off between confidence and the other metrics. E2E tests take the opposite
approach from unit tests: they provide the best confidence but at the expense
of maintainability, speed, complexity, and flakiness.
The end-to-end-only antipattern is when your build consists solely of E2E tests. The
marginal value of each additional E2E test is low, while the maintenance costs
of all tests are the same. You’ll get the most return on your efforts if you have
just a few E2E tests covering the most important functionality.
The low-level-only antipattern is when your build consists solely of unit and compo-
nent tests. Lower-level tests can’t provide enough confidence that your function-
ality as a whole works, and they must be supplemented with higher-level tests.
Disconnected low-level and high-level tests is an antipattern because it’s a strong sign
that your tests are written by two groups of people who don’t communicate
with each other. Such tests often duplicate each other and carry high mainte-
nance costs.
Don’t do nightly builds
It’s best to run your delivery pipeline after every code commit, instead of at a certain
time. Running tests with each code change gives you more granular and faster feed-
back than the crude nightly build that simply accumulates all changes from the pre-
vious day. But if, for some reason, you absolutely have to run your pipeline on a timely
basis, at least run them continuously instead of once a day.
If your delivery pipeline build takes a long time, don’t wait for a magical trigger or
schedule to run it. Imagine, as a developer, needing to wait until tomorrow to know
if you broke something. With tests running continuously, you would still need to wait,
but at least it would only be a couple of hours instead of a full day. Isn’t that more
productive?
Also, don’t just run the build on demand. The feedback loop will be faster if you run
the build automatically as soon as the previous one finishes, assuming there are
code changes since the previous build, of course.


---
**Page 212**

212
CHAPTER 10
Developing a testing strategy
A test recipe is a simple list of 5 to 20 lines of text, detailing which simple scenar-
ios should be tested in an automated fashion and at what level. A test recipe
should give you confidence that, if all outlined tests pass, the feature works
as intended.
Split your build pipeline into delivery and discovery pipelines. The delivery pipe-
line should be used for delivery-blocking tests, which, if they fail, stop delivery
of the code under test. The discovery pipeline is used for good-to-know tests
and runs in parallel with the delivery pipeline.
You can parallelize not just pipelines but also stages inside those pipelines, and
even groups of tests inside stages too.


---
**Page 213**

213
Integrating unit testing
into the organization
As a consultant, I’ve helped several companies, big and small, integrate continuous
delivery processes and various engineering practices, such as test-driven develop-
ment and unit testing, into their organizational culture. Sometimes this has failed,
but those companies that succeeded had several things in common. In any type of
organization, changing people’s habits is more psychological than technical. Peo-
ple don’t like change, and change is usually accompanied with plenty of FUD (fear,
uncertainty, and doubt) to go around. It won’t be a walk in the park for most peo-
ple, as you’ll see in this chapter.
11.1
Steps to becoming an agent of change
If you’re going to be the agent of change in your organization, you should first
accept that role. People will view you as the person responsible (and sometimes
This chapter covers
Becoming an agent of change
Implementing change from the top down or from 
the bottom up
Preparing to answer the tough questions about 
unit testing


