# 6.1.3 Integration testing of async/await (pp.124-125)

---
**Page 124**

124
CHAPTER 6
Unit testing asynchronous code
To test a function whose exit point is a callback function, we pass it our own callback
function in which we can
Check the correctness of the passed-in values
Tell the test runner to stop waiting through whatever mechanism is given to us
by the test framework (in this case, that’s the done() function)
6.1.2
Waiting for the act
Because we’re using callbacks as exit points, our test has to explicitly wait until the par-
allel execution completes. That parallel execution could be on the JavaScript event
loop or it could be in a separate thread, or even in a separate process if you’re using
another language.
 In the Arrange-Act-Assert pattern, the act part is the thing we need to wait out.
Most test frameworks will allow us to do so with special helper functions. In this case,
we can use the optional done callback that Jest provides to signal that the test needs to
wait until we explicitly call done(). If done() isn’t called, our test will time out and fail
after the default 5 seconds (which is configurable, of course).
 Jest has other means for testing asynchronous code, a couple of which we’ll cover
later in the chapter.
6.1.3
Integration testing of async/await
What about the async/await version? We could technically write a test that looks almost
exactly like the previous one, since async/await is just syntactic sugar over promises.
test("NETWORK REQUIRED (await): correct content, true", (done) => {
  samples.isWebsiteAliveWithAsyncAwait().then((result) => {
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
    done();
  });
});
However, a test that uses callbacks such as done() and then() is much less readable
than one using the Arrange-Act-Assert pattern. The good news is there’s no need to
complicate our lives by forcing ourselves to use callbacks. We can use the await syntax
in our test as well. This will force us to put the async keyword in front of the test func-
tion, but, overall, our test becomes simpler and more readable, as you can see here.
test("NETWORK REQUIRED2 (await): correct content, true", async () => {
  const result = await samples.isWebsiteAliveWithAsyncAwait();
  expect(result.success).toBe(true);
  expect(result.status).toBe("ok");
});
Listing 6.3
Integration test with callbacks and .then()
Listing 6.4
Integration test with async/await


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


