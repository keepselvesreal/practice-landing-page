# 6.1.4 Challenges with integration tests (pp.125-125)

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


