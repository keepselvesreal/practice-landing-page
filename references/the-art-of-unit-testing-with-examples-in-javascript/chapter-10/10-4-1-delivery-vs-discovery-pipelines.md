# 10.4.1 Delivery vs. discovery pipelines (pp.208-209)

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


