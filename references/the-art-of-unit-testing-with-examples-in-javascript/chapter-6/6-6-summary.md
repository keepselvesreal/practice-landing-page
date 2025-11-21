# 6.6 Summary (pp.145-149)

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


