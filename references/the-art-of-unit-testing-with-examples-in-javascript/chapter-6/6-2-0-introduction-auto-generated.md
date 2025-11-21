# 6.2.0 Introduction [auto-generated] (pp.125-126)

---
**Page 125**

125
6.2
Making our code unit-test friendly
Having asynchronous code that allows us to use the async/await syntax turns our test
into almost a run-of-the-mill value-based test. The entry point is also the exit point, as
we saw in figure 6.1. 
 Even though the call is simplified, the call is still asynchronous underneath,
which is why I still call this an integration test. What are the caveats for this type of
test? Let’s discuss.
6.1.4
Challenges with integration tests
The tests we’ve just written aren’t horrible as far as integration tests go. They’re rela-
tively short and readable, but they still suffer from what any integration test suffers from:
Lengthy run time—Compared to unit tests, integration tests are orders of magni-
tude slower, sometimes taking seconds or even minutes.
Flaky—Integration tests can present inconsistent results (different timings
based on where they run, inconsistent failures or successes, etc.)
Tests possibly irrelevant code and environment conditions—Integration tests test mul-
tiple pieces of code that might be unrelated to what we care about. (In our case,
it’s the node-fetch library, network conditions, firewall, external website func-
tionality, etc.)
Longer investigations—When an integration test fails, it requires more time for
investigation and debugging because there are many possible reasons for a failure.
Simulation is harder—It is harder than it needs to be to simulate a negative test
with an integration test (simulating wrong website content, website down, net-
work down, etc.)
Harder to trust results—We might believe the failure of an integration test is due
to an external issue when in fact it’s a bug in our code. I’ll talk about trust more
in the next chapter.
Does all this mean you shouldn’t write integration tests? No, I believe you should abso-
lutely have integration tests, but you don’t need to have that many of them to get
enough confidence in your code. Whatever integration tests don’t cover should be
covered by lower-level tests, such as unit, API, or component tests. I’ll discuss this strat-
egy at length in chapter 10, which focuses on testing strategies.
6.2
Making our code unit-test friendly
How can we test the code with a unit test? I’ll show you some patterns that I use to
make the code more unit testable (i.e., to more easily inject or avoid dependencies,
and to check exit points): 
Extract Entry Point pattern—Extracting the parts of the production code that are
pure logic into their own functions, and treating those functions as entry points
for our tests
Extract Adapter pattern—Extracting the thing that is inherently asynchronous and
abstracting it away so that we can replace it with something that is synchronous


---
**Page 126**

126
CHAPTER 6
Unit testing asynchronous code
6.2.1
Extracting an entry point
In this pattern, we take a specific unit of async work and split it into two pieces:
The async part (which stays intact).
The callbacks that are invoked when the async execution finishes. These are
extracted as new functions, which eventually become entry points for a purely
logical unit of work that we can invoke with pure unit tests.
Figure 6.2 depicts this idea: In the before diagram, we have a single unit of work that
contains asynchronous code mixed with logic that processes the async results inter-
nally and returns a result via a callback or promise mechanism. In step 1, we extract
the logic into its own function (or functions) that contains only the results of the
async work as inputs. In step 2, we externalize those functions so that we can use them
as entry points for our unit tests.
This provides us with the important ability to test the logical processing of the async
callbacks (and to simulate inputs easily). At the same time, we can choose to write a
higher-level integration test against the original unit of work to gain confidence that
the async orchestration works correctly as well. 
 If we do integration tests only for all our scenarios, we would end up in a world of
many long-running and flaky tests. In the new world, we’re able to have most of our
tests be fast and consistent, and to have a small layer of integration tests on top to
make sure all the orchestration works in between. This way we don’t sacrifice speed
and maintainability for confidence.
Before
Step 1
Step 2
Callback/async result
Logic
processing
Entry point
Callback
Async code
Entry point
Callback/async result
Unit of work
Logic
processing
Unit of work
Entry point
Callback/async result
Async
code
Logic
processing
Callback
Figure 6.2
Extracting the internal processing logic into a separate unit of work helps simplify the tests, because 
we are able to verify the new unit of work synchronously and without involving external dependencies.


