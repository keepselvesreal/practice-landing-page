# 6.3.1 Stubbing timers out with monkey-patching (pp.138-139)

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


