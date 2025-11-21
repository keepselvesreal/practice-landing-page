# 6.5 Bringing in the DOM testing library (pp.144-145)

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


