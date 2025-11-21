# 10.4.2 Test layer parallelization (pp.209-211)

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


