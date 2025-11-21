# 6.1.2 Waiting for the act (pp.124-124)

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


