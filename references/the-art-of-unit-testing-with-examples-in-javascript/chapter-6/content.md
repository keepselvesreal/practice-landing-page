# Unit testing asynchronous code (pp.121-149)

---
**Page 121**

121
Unit testing
asynchronous code
When we’re dealing with regular synchronous code, waiting for actions to finish is
implicit. We don’t worry about it, and we don’t really think about it too much. When
dealing with asynchronous code, however, waiting for actions to finish becomes an
explicit activity that is under our control. Asynchronicity makes code, and the tests
for that code, potentially trickier because we have to be explicit about waiting for
actions to complete.
 Let’s start with a simple fetching example to illustrate the issue.
 
 
This chapter covers
Async, done(), and awaits
Integration and unit test levels for async
The Extract Entry Point pattern
The Extract Adapter pattern
Stubbing, advancing, and resetting timers


---
**Page 122**

122
CHAPTER 6
Unit testing asynchronous code
6.1
Dealing with async data fetching
Let’s say we have a module that checks whether our website at example.com is alive. It
does this by fetching the context from the main URL and checking for a specific
word, “illustrative,” to determine if the website is up. We’ll look at two different and
very simple implementations of this functionality. The first uses a callback mecha-
nism, and the second uses an async/await mechanism.
 Figure 6.1 illustrates their entry and exit points for our purposes. Note that the
callback arrow is pointed differently, to make it more obvious that it’s a different type
of exit point.
The initial code is shown in the following listing. We’re using node-fetch to get the
URL’s content.
//Callback version
const fetch = require("node-fetch");
const isWebsiteAliveWithCallback = (callback) => {
  const website = "http://example.com";
  fetch(website)
    .then((response) => {
      if (!response.ok) {
        //how can we simulate this network issue?
        throw Error(response.statusText);      
      }
      return response;
    })
    .then((response) => response.text())
    .then((text) => {
      if (text.includes("illustrative")) {
        callback({ success: true, status: "ok" });
      } else {
        //how can we test this path?
Listing 6.1
IsWebsiteAlive() callback and await versions
Callback version
Async/await version
Website
checkup
isWebsiteAlive()
Return
value/error
isWebsiteAlive(callback)
Callback
Website
checkup
Figure 6.1
IsWebsiteAlive() callback vs. the async/await version
Throwing a custom 
error to handle 
problems in our code


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


---
**Page 132**

132
CHAPTER 6
Unit testing asynchronous code
Before
After
Entry point
Exit point
Unit of work
Dependency
Logic
processing
Inject adapter
Entry point
Exit point
Adapter
Dependency
Figure 6.6
Extracting a dependency and wrapping it with an adapter helps us simplify that 
dependency and replace it with a fake in tests.
Before
After
Entry point
Exit point
website-verifier
node-fetch
Logic
Logic
Inject/import
network-adapter
website-verifier
network-adapter
fetchUrlText(url)
async
isWebsiteAlive()
async
node-fetch
Figure 6.7
Wrapping the node-fetch module with our own network-adapter module helps us expose only 
the functionality our application needs, expressed in the language most suitable for the problem at hand.


---
**Page 133**

133
6.2
Making our code unit-test friendly
The following listing shows what the network-adapter module looks like.
const fetch = require("node-fetch");
const fetchUrlText = async (url) => {
  const resp = await fetch(url);
  if (resp.ok) {
    const text = await resp.text();
    return { ok: true, text: text };
  }
  return { ok: false, text: resp.statusText };
};   
Note that the network-adapter module is the only module in the project that imports
node-fetch. If that dependency changes at some point in the future, this increases
the chances that only the current file would need to change. We’ve also simplified the
function both by name and by functionality. We’re hiding the need to fetch the status
and the text from the URL, and we’re abstracting them both under a single easier-to-
use function.
 Now we get to choose how to use the adapter. First, we can use it in the modular
style. Then we’ll use a functional approach and an object-oriented one with a strongly
typed interface.
MODULAR ADAPTER
The following listing shows a modular use of network-adapter by our initial isWebsite-
Alive() function.
const network = require("./network-adapter");
const isWebsiteAlive = async () => {
  try {
    const result = await network.fetchUrlText("http://example.com");
    if (!result.ok) {
      throw result.text;
    }
Interface segregation principle
The term interface segregation principle was coined by Robert Martin. Imagine a data-
base dependency with dozens of functions hidden behind an adapter whose interface
might only contain a couple of functions with custom names and parameters. The
adapter serves to hide the complexity and simplify both the consumer’s code and the
tests that simulate it. For more information on interface segregation, see the Wikipe-
dia article about it: https://en.wikipedia.org/wiki/Interface_segregation_principle.
Listing 6.9
The network-adapter code
Listing 6.10
isWebsiteAlive() using the network-adapter module


---
**Page 134**

134
CHAPTER 6
Unit testing asynchronous code
    const text = result.text;
    return processFetchSuccess(text);
  } catch (err) {
    throw processFetchFail(err);
  }
};
In this version, we are directly importing the network-adapter module, which we’ll
fake in our tests later on. 
 The unit tests for this module are shown in the following listing. Because we’re
using a modular design, we can fake the module using jest.mock() in our tests. We’ll
also inject the module in later examples, don’t worry.
jest.mock("./network-adapter");    
const stubSyncNetwork = require("./network-adapter");   
const webverifier = require("./website-verifier");
describe("unit test website verifier", () => {
  beforeEach(jest.resetAllMocks);              
  test("with good content, returns true", async () => {
    stubSyncNetwork.fetchUrlText.mockReturnValue({     
      ok: true,
      text: "illustrative",
    });
    const result = await webverifier.isWebsiteAlive();    
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
  });
  test("with bad content, returns false", async () => {
    stubSyncNetwork.fetchUrlText.mockReturnValue({
      ok: true,
      text: "<span>hello world</span>",
    });
    const result = await webverifier.isWebsiteAlive();    
    expect(result.success).toBe(false);
    expect(result.status).toBe("missing text");
  });
Notice that we are using async/await again, because we are back to using the original
entry point we started with at the beginning of the chapter. But just because we’re
using await doesn’t mean our tests are running asynchronously. Our test code, and
the production code it invokes, actually runs linearly, with an async-friendly signature.
We’ll need to use async/await for the functional and object-oriented designs as well,
because the entry point requires it.
 I’ve named our fake network stubSyncNetwork to make the synchronous nature of
the test clearer. Otherwise, it’s hard to tell just by looking at the test whether the code
it invokes runs linearly or asynchronously.
Listing 6.11
Faking network-adapter with jest.mock
Faking the network-adapter module
Importing the 
fake module
Resetting all the stubs to avoid 
any potential issues in other tests
Simulating a 
return value from 
the stub module
Using 
await in 
our tests


---
**Page 135**

135
6.2
Making our code unit-test friendly
FUNCTIONAL ADAPTER
In the functional design pattern, the design of the network-adapter module stays the
same, but we enable its injection into our website-verifier differently. As you can
see in the next listing, we add a new parameter to our entry point.
const isWebsiteAlive = async (network) => {
  const result = await network.fetchUrlText("http://example.com");
  if (result.ok) {
    const text = result.text;
    return onFetchSuccess(text);
  }
  return onFetchError(result.text);
};
In this version, we’re expecting the network-adapter module to be injected through
a common parameter to our function. In a functional design, we can use higher-order
functions and currying to configure a pre-injected function with our own network
dependency. In our tests, we can simply send in a fake network via this parameter. As
far as the design of the injection goes, almost nothing else has changed from previous
samples, other than the fact that we don’t import the network-adapter module any-
more. Reducing the amount of imports and requires can help maintainability in the
long run. 
 Our tests are simpler in the following listing, with less boilerplate code.
const webverifier = require("./website-verifier");
const makeStubNetworkWithResult = (fakeResult) => {   
  return {
    fetchUrlText: () => {
      return fakeResult;
    },
  };
};
describe("unit test website verifier", () => {
  test("with good content, returns true", async () => {
    const stubSyncNetwork = makeStubNetworkWithResult({
      ok: true,
      text: "illustrative",
    });
    const result = await webverifier.isWebsiteAlive(stubSyncNetwork);   
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
  });
  test("with bad content, returns false", async () => {
    const stubSyncNetwork = makeStubNetworkWithResult({
Listing 6.12
A functional injection design for isWebsiteAlive() 
Listing 6.13
Unit test with functional injection of network-adapter
A new helper function 
to create a custom 
object that matches 
the important parts of 
the network-adapter’s 
interface
Injecting the
custom object


---
**Page 136**

136
CHAPTER 6
Unit testing asynchronous code
      ok: true,
      text: "unexpected content",
    });
    const result = await webverifier.isWebsiteAlive(stubSyncNetwork);   
    expect(result.success).toBe(false);
    expect(result.status).toBe("missing text");
  });
  …   
Notice that we don’t need a lot of the boilerplate at the top of the file, as we did in the
modular design. We don’t need to fake the module indirectly (via jest.mock), we
don’t need to re-import it for our tests (via require), and we don’t need to reset Jest’s
state using jest.resetAllMocks. All we need to do is call our new makeStubNetwork-
WithResult helper function from each test to generate a new fake network adapter,
and then inject the fake network by sending it as a parameter to our entry point.
OBJECT-ORIENTED, INTERFACE-BASED ADAPTER
We’ve taken a look at the modular and functional designs. Let’s now turn our atten-
tion to the object-oriented side of the equation. In the object-oriented paradigm, we
can take the parameter injection we’ve done before and promote it into a constructor
injection pattern. We’ll start with the network adapter and its interfaces (public API
and results signature) in the following listing.
export interface INetworkAdapter {
  fetchUrlText(url: string): Promise<NetworkAdapterFetchResults>;
}
export interface NetworkAdapterFetchResults {
  ok: boolean;
  text: string;
}
ch6-async/6-fetch-adapter-interface-oo/network-adapter.ts
    
export class NetworkAdapter implements INetworkAdapter {
  async fetchUrlText(url: string): 
        Promise<NetworkAdapterFetchResults> {
    const resp = await fetch(url);
    if (resp.ok) {
      const text = await resp.text();
      return Promise.resolve({ ok: true, text: text });
    }
    return Promise.reject({ ok: false, text: resp.statusText });
  }
}
In the next listing, we create a WebsiteVerifier class that has a constructor that
receives an INetworkAdapter parameter.
 
Listing 6.14
NetworkAdapter and its interfaces
Injecting the
custom object


---
**Page 137**

137
6.2
Making our code unit-test friendly
export interface WebsiteAliveResult {
  success: boolean;
  status: string;
}
export class WebsiteVerifier {
  constructor(private network: INetworkAdapter) {}
  isWebsiteAlive = async (): Promise<WebsiteAliveResult> => {
    let netResult: NetworkAdapterFetchResults;
    try {
    netResult = await this.network.fetchUrlText("http://example.com");
      if (!netResult.ok) {
        throw netResult.text;
      }
      const text = netResult.text;
      return this.processNetSuccess(text);
    } catch (err) {
      throw this.processNetFail(err);
    }
  };
  processNetSuccess = (text): WebsiteAliveResult => {
    const included = text.includes("illustrative");
    if (included) {
      return { success: true, status: "ok" };
    }
    return { success: false, status: "missing text" };
  };
  processNetFail = (err): WebsiteAliveResult => {
    return { success: false, status: err };
  };
}
The unit tests for this class can instantiate a fake network adapter and inject it through
a constructor. In the following listing, we’ll use substitute.js to create a fake object that
fits the new interface.
const makeStubNetworkWithResult = (    
  fakeResult: NetworkAdapterFetchResults
): INetworkAdapter => {
  const stubNetwork = Substitute.for<INetworkAdapter>();   
  stubNetwork.fetchUrlText(Arg.any()) 
    .returns(Promise.resolve(fakeResult));   
  return stubNetwork;
};
Listing 6.15
WebsiteVerifier class with constructor injection
Listing 6.16
Unit tests for the object-oriented WebsiteVerifier
Helper function to simulate 
the network adapter
Generating the 
fake object
Making the fake 
object return what 
the test requires


---
**Page 138**

138
CHAPTER 6
Unit testing asynchronous code
describe("unit test website verifier", () => {
  test("with good content, returns true", async () => {
    const stubSyncNetwork = makeStubNetworkWithResult({
      ok: true,
      text: "illustrative",
    });
    const webVerifier = new WebsiteVerifier(stubSyncNetwork);
    const result = await webVerifier.isWebsiteAlive();
    expect(result.success).toBe(true);
    expect(result.status).toBe("ok");
  });
  test("with bad content, returns false", async () => {
    const stubSyncNetwork = makeStubNetworkWithResult({
      ok: true,
      text: "unexpected content",
    });
    const webVerifier = new WebsiteVerifier(stubSyncNetwork);
    const result = await webVerifier.isWebsiteAlive();
    expect(result.success).toBe(false);
    expect(result.status).toBe("missing text");
  });    
This type of Inversion of Control (IOC) and Dependency Injection (DI) works well. In
the object-oriented world, constructor injection with interfaces is very common and
can, in many instances, provide a valid and maintainable solution for separating your
dependencies from your logic. 
6.3
Dealing with timers
Timers, such as setTimeout, represent a very JavaScript-specific problem. They are
part of the domain and are used, for better or worse, in many pieces of code. Instead
of extracting adapters and entry points, sometimes it’s just as useful to disable these
functions and work around them. We’ll look at two patterns for getting around timers:
Directly monkey-patching the function
Using Jest and other frameworks to disable and control them
6.3.1
Stubbing timers out with monkey-patching
Monkey-patching is a way for a program to extend or modify supporting system soft-
ware locally (affecting only the running instance of the program). Programming lan-
guages and runtimes such as JavaScript, Ruby, and Python can accommodate monkey-
patching pretty easily. It’s much more difficult to do with more strongly typed and
compile-time languages such as C# and Java. I discuss monkey-patching in more detail
in the appendix.
 Here’s one way to do it in JavaScript. We’ll start with the following piece of code
that uses the setTimeout method.


---
**Page 139**

139
6.3
Dealing with timers
const calculate1 = (x, y, resultCallback) => {
  setTimeout(() => { resultCallback(x + y); },
    5000);
};
We can monkey-patch the setTimeout function to be synchronous by literally setting
that function’s prototype in memory, as follows.
const Samples = require("./timing-samples");
describe("monkey patching ", () => {
  let originalTimeOut;
  beforeEach(() => (originalTimeOut = setTimeout));    
  afterEach(() => (setTimeout = originalTimeOut));    
  test("calculate1", () => {
    setTimeout = (callback, ms) => callback();    
    Samples.calculate1(1, 2, (result) => {
        expect(result).toBe(3);
    });
  });
});
Since everything is synchronous, we don’t need to use done() to wait for a callback
invocation. We are replacing setTimeout with a purely synchronous implementation
that invokes the received callback immediately.
 The only downside to this approach is that it requires a bunch of boilerplate code
and is generally more error prone, since we need to remember to clean up correctly.
Let’s look at what frameworks like Jest provide us with to handle these situations.
6.3.2
Faking setTimeout with Jest
Jest provides us with three major functions for handling most types of timers in
JavaScript:

jest.useFakeTimers—Stubs out all the various timer functions, such as
setTimetout

jest.resetAllTimers—Resets all fake timers to the real ones

jest.advanceTimersToNextTimer—Triggers any fake timer so that any callbacks
are triggered
Together, these functions take care of most of the boilerplate code for us.
 Here’s the same test we just did in listing 6.18, this time using Jest’s helper functions.
 
 
Listing 6.17
Code with setTimeout we’d like to monkey-patch 
Listing 6.18
A simple monkey-patching pattern
Saving the 
original 
setTimeout
Restoring the 
original setTimeout
Monkey-patching 
the setTimeout


---
**Page 140**

140
CHAPTER 6
Unit testing asynchronous code
describe("calculate1 - with jest", () => {
  beforeEach(jest.clearAllTimers);
  beforeEach(jest.useFakeTimers);
  test("fake timeout with callback", () => {
    Samples.calculate1(1, 2, (result) => {
      expect(result).toBe(3);
    });
    jest.advanceTimersToNextTimer();
  });
});
Notice that, once again, we don’t need to call done(), since everything is synchronous.
At the same time, we have to use advanceTimersToNextTimer because, without it, our
fake setTimeout would be stuck forever. advanceTimersToNextTimer is also useful for
scenarios such as when the module being tested schedules a setTimeout whose call-
back schedules another setTimeout recursively (meaning the scheduling never
stops). In these scenarios, it’s useful to be able to run forward in time, step by step. 
 With advanceTimersToNextTimer, you could potentially advance all timers by a
specified number of steps to simulate the passage of steps that will trigger the next
timer callback waiting in line.
 The same pattern also works well with setInterval, as shown next.
const calculate4 = (getInputsFn, resultFn) => {
  setInterval(() => {
    const { x, y } = getInputsFn();
    resultFn(x + y);
  }, 1000);
};
In this case, our function takes in two callbacks as parameters: one to provide the
inputs to calculate, and the other to call back with the calculation result. It uses set-
Interval to continuously get more inputs and calculate their results.
 The following listing shows a test that will advance our timer, trigger the interval
twice, and expect the same result from both invocations.
describe("calculate with intervals", () => {
  beforeEach(jest.clearAllTimers);
  beforeEach(jest.useFakeTimers);
  test("calculate, incr input/output, calculates correctly", () => {
    let xInput = 1;
    let yInput = 2;
    const inputFn = () => ({ x: xInput++, y: yInput++ });      
Listing 6.19
Faking setTimeout with Jest
Listing 6.20
A function that uses setInterval
Listing 6.21
Advancing fake timers in a unit test
Incrementing a
variable to verify the
number of callbacks


---
**Page 141**

141
6.4
Dealing with common events
    const results = [];
    Samples.calculate4(inputFn, (result) => results.push(result));
    jest.advanceTimersToNextTimer();   
    jest.advanceTimersToNextTimer();   
    expect(results[0]).toBe(3);
    expect(results[1]).toBe(5);
  });
});
In this example, we verify that the new values are being calculated and stored cor-
rectly. Notice that we could have written the same test with only a single invocation
and a single expect, and we would have gotten close to the same amount of confi-
dence that this more elaborate test provides, but I like to put in additional validation
when I need more confidence. 
6.4
Dealing with common events
I can’t talk about async unit testing and not discuss the basic events flow. Hopefully
the topic of async unit testing now seems relatively straightforward, but I want to go
over the events part explicitly.
6.4.1
Dealing with event emitters
To make sure we’re all on the same page, here’s a clear and concise definition of event
emitters from DigitalOcean’s “Using Event Emitters in Node.js” tutorial (http://mng
.bz/844z):
Event emitters are objects in Node.js that trigger an event by sending a message to signal
that an action was completed. JavaScript developers can write code that listens to events
from an event emitter, allowing them to execute functions every time those events are
triggered. In this context, events are composed of an identifying string and any data that
needs to be passed to the listeners.
Consider the Adder class in the following listing, which emits an event every time it
adds something.
const EventEmitter = require("events");
class Adder extends EventEmitter {
  constructor() {
    super();
  }
  add(x, y) {
    const result = x + y;
    this.emit("added", result);
    return result;
Listing 6.22
A simple event-emitter-based Adder
Invoking 
setInterval twice


---
**Page 142**

142
CHAPTER 6
Unit testing asynchronous code
  }
}
The simplest way to write a unit test that verifies that the event is emitted is to liter-
ally subscribe to the event in our test and verify that it triggers when we call the add
function.
describe("events based module", () => {
  describe("add", () => {
    it("generates addition event when called", (done) => {
      const adder = new Adder();
      adder.on("added", (result) => {
        expect(result).toBe(3);
        done();
      });
      adder.add(1, 2);
    });
  });
});
By using done(), we are verifying that the event actually was emitted. If we didn’t use
done(), and the event wasn’t emitted, our test would pass because the subscribed code
never executed. By adding expect(x).toBe(y), we are also verifying the values sent in
the event parameters, as well as implicitly testing that the event was triggered. 
6.4.2
Dealing with click events
What about those pesky UI events, such as click? How can we test that we have bound
them correctly via our scripts? Consider the simple web page and associated logic in
listings 6.24 and 6.25.
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File to Be Tested</title>
    <script src="index-helper.js"></script>
</head>
<body>
    <div>
        <div>A simple button</div>
        <Button data-testid="myButton" id="myButton">Click Me</Button>
        <div data-testid="myResult" id="myResult">Waiting...</div>
    </div>
</body>
</html> 
Listing 6.23
Testing an event emitter by subscribing to it
Listing 6.24
A simple web page with JavaScript click functionality


---
**Page 143**

143
6.4
Dealing with common events
window.addEventListener("load", () => {
  document
    .getElementById("myButton")
    .addEventListener("click", onMyButtonClick);
  const resultDiv = document.getElementById("myResult");
  resultDiv.innerText = "Document Loaded";
});
function onMyButtonClick() {
  const resultDiv = document.getElementById("myResult");
  resultDiv.innerText = "Clicked!";
}
We have a very simple piece of logic that makes sure our button sets a special message
when clicked. How can we test this?
 Here’s an antipattern: we could subscribe to the click event in our tests and make
sure it is triggered, but this would provide no value to us. What we care about is that
the click has actually done something useful, other than triggering. 
 Here’s a better way: we can trigger the click event and make sure it has changed
the correct value inside the page—this will provide real value. Figure 6.8 shows this.
The following listing shows what our test might look like.
/**
 * @jest-environment jsdom    
 */
//(the above is required for window events)
const fs = require("fs");
const path = require("path");
require("./index-helper.js");
Listing 6.25
The logic for the web page in JavaScript
Listing 6.26
Triggering a click event, and testing an element’s text
Trigger
event
document.load()
Trigger
event
click()
Verify text
in page element
Web page
Figure 6.8
Click as an entry point, 
and element as an exit point
Applying the browser-simulating 
jsdom environment just for this file 


---
**Page 144**

144
CHAPTER 6
Unit testing asynchronous code
const loadHtml = (fileRelativePath) => {
  const filePath = path.join(__dirname, "index.html");
  const innerHTML = fs.readFileSync(filePath);
  document.documentElement.innerHTML = innerHTML;
};
const loadHtmlAndGetUIElements = () => {
  loadHtml("index.html");
  const button = document.getElementById("myButton");
  const resultDiv = document.getElementById("myResult");
  return { window, button, resultDiv };
};
describe("index helper", () => {
  test("vanilla button click triggers change in result div", () => {
    const { window, button, resultDiv } = loadHtmlAndGetUIElements();
    window.dispatchEvent(new Event("load"));    
    button.click();   
    expect(resultDiv.innerText).toBe("Clicked!");   
  });
});   
In this example, I’ve extracted two utility methods, loadHtml and loadHtmlAndGetUI-
Elements, so that I can write cleaner, more readable tests, and so I’ll have fewer issues
changing my tests if UI item locations or IDs change in the future.
 In the test itself, we’re simulating the document.load event, so that our custom
script under test can start running and then triggering the click, as if the user had
clicked the button. Finally, the test verifies that an element in our document has
actually changed, which means our code successfully subscribed to the event and
did its work.
 Notice that we don’t actually care about the underlying logic inside the index
helper file. We just rely on observed state changes in the UI, which acts as our final
exit point. This allows less coupling in our tests, so that if our code under test changes,
we are less likely to need to change the test, unless the observable (publicly notice-
able) functionality has truly changed.
6.5
Bringing in the DOM testing library
Our test has a lot of boilerplate code, mostly for finding elements and verifying their
contents. I recommend looking into the open source DOM Testing Library written by
Kent C. Dodds (https://github.com/kentcdodds/dom-testing-library-with-anything).
This library has variants applicable to most frontend JavaScript frameworks today,
such as React, Angular, and Vue.js. We’ll be using the vanilla version of it named DOM
Testing Library. 
 What I like about this library is that it aims to allow us to write tests closer to the
point of view of the user interacting with our web page. Instead of using IDs for ele-
ments, we query by element text; firing events is a bit cleaner; and querying and
Simulating the 
document.load event
Triggering
the click
Verifying that an element 
in our document has 
actually changed


---
**Page 145**

145
Summary
waiting for elements to appear or disappear is cleaner and hidden under syntactic
sugar. It’s quite useful once you use it in multiple tests. 
 Here’s what our test looks like with this library.
const { fireEvent, findByText, getByText }  
    = require("@testing-library/dom");      
const loadHtml = (fileRelativePath) => {
  const filePath = path.join(__dirname, "index.html");
  const innerHTML = fs.readFileSync(filePath);
  document.documentElement.innerHTML = innerHTML;
  return document.documentElement;        
};
const loadHtmlAndGetUIElements = () => {
  const docElem = loadHtml("index.html");
  const button = getByText(docElem, "click me", { exact: false });
  return { window, docElem, button };
};
describe("index helper", () => {
  test("dom test lib button click triggers change in page", () => {
    const { window, docElem, button } = loadHtmlAndGetUIElements();
    fireEvent.load(window);        
    fireEvent.click(button);       
    //wait until true or timeout in 1 sec
    expect(findByText(docElem,"clicked", { exact: false })).toBeTruthy();  
  });
});
Notice how the library allows us to use the regular text of the page items to get the
items, instead of their IDs or test IDs. This is part of the way the library pushes us to
work so things feel more natural and from the user’s point of view. To make the test
more sustainable over time, we’re using the exact: false flag so that we don’t have to
worry about uppercasing issues or missing letters at the start or end of strings. This
removes the need to change the test for small text changes that are less important.
Summary
Testing asynchronous code directly results in flaky tests that take a long time to
execute. To fix these issues, you can take two approaches: extract an entry point
or extract an adapter.
Extracting an entry point is when you extract the pure logic into separate func-
tions and treat those functions as entry points for your tests. The extracted
entry point can either accept a callback as an argument or return a value. Prefer
return values over callbacks for simplicity.
Listing 6.27
Using the DOM Testing Library in a simple test
Importing some of the 
library APIs to be used
Library APIs require 
the document element 
as the basis for most 
of the work.
Using the library’s fireEvent API 
to simplify event dispatching
This query will wait until the item is
found or will timeout within 1 second.


---
**Page 146**

146
CHAPTER 6
Unit testing asynchronous code
Extracting an adapter involves extracting a dependency that is inherently asyn-
chronous and abstracting it away so that you can replace it with something that
is synchronous. The adapter may be of different types:
– Modular—When you stub the whole module (file) and replace specific func-
tions in it.
– Functional—When you inject a function or value into the system under test.
You can replace the injected value with a stub in tests.
– Object-oriented—When you use an interface in the production code and cre-
ate a stub that implements that interface in the test code.
Timers (such as setTimeout and setInterval) can be replaced either directly
with monkey-patching or by using Jest or another framework to disable and
control them.
Events are best tested by verifying the end result they produce—changes in the
HTML document the user can see. You can do this either directly or by using
libraries such as the DOM Testing Library. 


---
**Page 147**

Part 3
The test code
This part covers techniques for managing and organizing unit tests and for
ensuring that the quality of unit tests in real-world projects is high.
 Chapter 7 covers test trustworthiness. It explains how to write tests that will
reliably report the presence or absence of bugs. We’ll also look at the differences
between true and false test failures.
 In chapter 8, we’ll look at the main pillar of good unit tests—maintainability—
and we’ll explore techniques to support it. For tests to be useful in the long run,
they shouldn’t require much effort to maintain; otherwise, they will inevitably
become abandoned.


---
**Page 148**



---
**Page 149**

149
Trustworthy tests
No matter how you organize your tests, or how many you have, they’re worth very
little if you can’t trust them, maintain them, or read them. The tests that you write
should have three properties that together make them good:
Trustworthiness—Developers will want to run trustworthy tests, and they’ll
accept the test results with confidence. Trustworthy tests don’t have bugs,
and they test the right things. 
Maintainability—Unmaintainable tests are nightmares because they can ruin
project schedules, or they may be sidelined when the project is put on a
more aggressive schedule. Developers will simply stop maintaining and fix-
ing tests that take too long to change or that need to change often on very
minor production code changes.
Readability—This refers not only to being able to read a test but also figuring
out the problem if the test seems to be wrong. Without readability, the other
This chapter covers
How to know you trust a test
Detecting untrustworthy failing tests
Detecting untrustworthy passing tests
Dealing with flaky tests


