# 6.1.1 An initial attempt with an integration test (pp.123-124)

---
**Page 123**

123
6.1
Dealing with async data fetching
        callback({ success: false, status: "text missing" });
      }
    })
    .catch((err) => {
      //how can we test this exit point?
      callback({ success: false, status: err });
    });
};
// Await version
const isWebsiteAliveWithAsyncAwait = async () => {
  try {
    const resp = await fetch("http://example.com");
    if (!resp.ok) {
      //how can we simulate a non ok response?
      throw resp.statusText;                     
    }
    const text = await resp.text();
    const included = text.includes("illustrative");
    if (included) {
      return { success: true, status: "ok" };
    }
    // how can we simulate different website content?
    throw "text missing";
  } catch (err) {
    return { success: false, status: err };  
  }
};
NOTE
In the preceding code, I’m assuming you know how promises work in
JavaScript. If you need more information, I recommend reading the Mozilla
documentation on promises at http://mng.bz/W11a.
In this example, we are converting any errors from connectivity failures or missing
text on the web page to either a callback or a return value to denote a failure to the
user of our function. 
6.1.1
An initial attempt with an integration test
Since everything is hardcoded in listing 6.1, how would you test this? Your initial reac-
tion might involve writing an integration test. The following listing shows how we
could write an integration test for the callback version.
test("NETWORK REQUIRED (callback): correct content, true", (done) => {
  samples.isWebsiteAliveWithCallback((result) => {
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
    done();
  });
});
Listing 6.2
An initial integration test
Throwing a custom 
error to handle 
problems in our code
Wrapping the error 
into a response


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


