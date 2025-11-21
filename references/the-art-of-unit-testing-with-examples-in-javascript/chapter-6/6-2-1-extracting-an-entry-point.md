# 6.2.1 Extracting an entry point (pp.126-131)

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


---
**Page 127**

127
6.2
Making our code unit-test friendly
EXAMPLE OF EXTRACTING A UNIT OF WORK
Let’s apply this pattern to the code from listing 6.1. Figure 6.3 shows the steps we’ll
follow:
b
The before state contains processing logic that is baked into the isWebsite-
Alive() function.
c
We’ll extract any logical code that happens at the edge of the fetch results
and put it in two separate functions: one for handling the success case, and
the other for the error case.
d
We’ll then externalize these two functions so that we can invoke them directly
from unit tests.
The following listing shows the refactored code.
//Entry Point
const isWebsiteAlive = (callback) => {
  fetch("http://example.com")
    .then(throwOnInvalidResponse)
    .then((resp) => resp.text())
    .then((text) => {
      processFetchSuccess(text, callback);
    })
    .catch((err) => {
      processFetchError(err, callback);
    });
};
Listing 6.5
Extracting entry points with callback
Before
Extract logic
Externalize entry points
Callback/async result
Pure logic
processFetchSuccess(vars)
Callback
Call fetch(url)
isWebsiteAlive(callback)Callback
Unit of work
Pure logic
Unit of work
isWebsiteAlive(callback)
Callback
Call
fetch(url)
processFetchSuccess(vars)
processFetchError(vars)
Callback
New
unit of work
Pure logic
processFetchError(vars)
1
2
3
(Unit of work logic testable directly)
(Async decoupled from logic)
(Async coupled with logic)
Figure 6.3
Extracting the success and error-handling logic from isWebsiteAlive() to test that logic 
separately


---
**Page 128**

128
CHAPTER 6
Unit testing asynchronous code
const throwOnInvalidResponse = (resp) => {
  if (!resp.ok) {
    throw Error(resp.statusText);
  }
  return resp;
};
//Entry Point
const processFetchSuccess = (text, callback) => {         
  if (text.includes("illustrative")) {
    callback({ success: true, status: "ok" });
  } else {
    callback({ success: false, status: "missing text" });
  }
};
//Entry Point
const processFetchError = (err, callback) => {            
  callback({ success: false, status: err });
};
As you can see, the original unit we started with now has three entry points instead of
the single one we started with. The new entry points can be used for unit testing, while
the original one can still be used for integration testing, as shown in figure 6.4.
We’d still want an integration test for the original entry point, but not more than one
or two of those. Any other scenario can be simulated using the purely logical entry
points, quickly and painlessly. 
 
New entry 
points (units 
of work)
isWebsiteAlive(callback)
Callback version
Callback
Website
checkup
Before
isWebsiteAlive(callback)
Callback version
Website
checkup
Callback
After
processFetchSuccess(text, callback)
processFetchError(err, callback)
Figure 6.4
New entry points introduced after extracting the two new functions. The new functions can now be 
tested with simpler unit tests instead of the integration tests that were required before the refactoring.


---
**Page 129**

129
6.2
Making our code unit-test friendly
 Now we’re free to write unit tests that invoke the new entry points, like this.
describe("Website alive checking", () => {
  test("content matches, returns true", (done) => {
    samples.processFetchSuccess("illustrative", (err, result) => {  
      expect(err).toBeNull();
      expect(result.success).toBe(true);
      expect(result.status).toBe("ok");
      done();
    });
  });
  test("website content does not match, returns false", (done) => {
    samples.processFetchSuccess("bad content", (err, result) => {   
      expect(err.message).toBe("missing text");
      done();
    });
  });
  test("When fetch fails, returns false", (done) => {
   samples.processFetchError("error text", (err,result) => {        
      expect(err.message).toBe("error text");
      done();
    });
  });
});
Notice that we are invoking the new entry points directly, and we’re able to simulate
various conditions easily. Nothing is asynchronous in these tests, but we still need
the done() function, since the callbacks might not be invoked at all, and we’ll want
to catch that.
 We still need at least one integration test that gives us confidence that the asyn-
chronous orchestration works between our entry points. That’s where the original
integration test can help, but we don’t need to write all our test scenarios as integra-
tion tests anymore (more on this in chapter 10).
EXTRACTING AN ENTRY POINT WITH AWAIT
The same pattern we just applied can work well for standard async/await function
structures. Figure 6.5 illustrates that refactoring.
 By providing the async/await syntax, we can go back to writing code in a linear
fashion, without using callback arguments. The isWebsiteAlive() function starts
looking almost exactly the same as regular synchronous code, only returning values
and throwing errors when needed. 
 Listing 6.7 shows how that looks in our production code.
 
 
 
 
 
Listing 6.6
Unit tests with extracted entry points
Invoking 
the new 
entry 
points


---
**Page 130**

130
CHAPTER 6
Unit testing asynchronous code
//Entry Point
const isWebsiteAlive = async () => {
  try {
    const resp = await fetch("http://example.com");
    throwIfResponseNotOK(resp);
    const text = await resp.text();
    return processFetchContent(text);
  } catch (err) {
    return processFetchError(err);
  }
};
const throwIfResponseNotOK = (resp) => {
  if (!resp.ok) {
    throw resp.statusText;
  }
};
//Entry Point
const processFetchContent = (text) => {
  const included = text.includes("illustrative");
  if (included) {
    return { success: true, status: "ok" };          
  }
  return { success: false, status: "missing text" }; 
};
//Entry Point
const processFetchError = (err) => {
  return { success: false, status: err };            
};
Listing 6.7
The function written with async/await instead of callbacks
Async/await version
Before
Async/await version
After
processFetchSuccess(text)
processFetchError(err)
isWebsiteAlive()
Return
value/error
isWebsiteAlive()
Return
value/error
Website
checkup
Website
checkup
Figure 6.5
Extracting entry points with async/await
Returning a 
value instead 
of calling a 
callback


---
**Page 131**

131
6.2
Making our code unit-test friendly
Notice that, unlike the callback examples, we’re using return or throw to denote suc-
cess or failure. This is a common pattern of writing code using async/await.
 Our tests are simplified as well, as shown in the following listing.
describe("website up check", () => {
  test("on fetch success with good content, returns true", () => {
    const result = samples.processFetchContent("illustrative");
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
  });
  test("on fetch success with bad content, returns false", () => {
    const result = samples.processFetchContent("text not on site");
    expect(result.success).toBe(false);
    expect(result.status).toBe("missing text");
  });
  test("on fetch fail, throws ", () => {
    expect(() => samples.processFetchError("error text"))
      .toThrowError("error text");
  });
});
Again, notice that we don’t need to add any kind of async/await-related keywords or
to be explicit about waiting for execution, because we’ve separated the logical unit of
work from the asynchronous pieces that make our lives more complicated.
6.2.2
The Extract Adapter pattern
The Extract Adapter pattern takes the opposite view from the previous pattern. We
look at the asynchronous piece of code just like we look at any dependency we’ve dis-
cussed in the previous chapters—as something we’d like to replace in our tests to
gain more control. Instead of extracting the logical code into its own set of entry
points, we’ll extract the asynchronous code (our dependency) and abstract it away
under an adapter, which we can later inject, just like any other dependency. Figure 6.6
shows this.
 It’s also common to create a special interface for the adapter that is simplified for
the needs of the consumer of the dependency. Another name for this approach is the
interface segregation principle. In this case, we’ll create a network-adapter module that
hides the real fetching functionality and has its own custom functions, as shown in fig-
ure 6.7.
Listing 6.8
Testing entry points extracted from async/await


