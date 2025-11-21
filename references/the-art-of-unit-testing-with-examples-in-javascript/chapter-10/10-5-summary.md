# 10.5 Summary (pp.211-213)

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


