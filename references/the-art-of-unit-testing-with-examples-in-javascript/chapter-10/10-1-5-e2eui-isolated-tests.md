# 10.1.5 E2E/UI isolated tests (pp.198-199)

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


