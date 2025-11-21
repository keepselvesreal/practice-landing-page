# 10.1.3 Integration tests (pp.197-198)

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


