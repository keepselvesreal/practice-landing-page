# 10.1.6 E2E/UI system tests (pp.199-199)

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


