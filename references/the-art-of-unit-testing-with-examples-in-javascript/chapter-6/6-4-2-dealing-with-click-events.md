# 6.4.2 Dealing with click events (pp.142-144)

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


