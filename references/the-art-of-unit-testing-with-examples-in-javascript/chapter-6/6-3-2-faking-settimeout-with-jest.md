# 6.3.2 Faking setTimeout with Jest (pp.139-141)

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


