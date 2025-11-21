# 6.4.1 Dealing with event emitters (pp.141-142)

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


