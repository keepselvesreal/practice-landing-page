# 10.1.2 Unit tests and component tests (pp.196-197)

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


