# 6.2.2 The Extract Adapter pattern (pp.131-138)

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


