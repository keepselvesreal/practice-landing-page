# 10.2.1 The end-to-end-only antipattern (pp.199-202)

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


