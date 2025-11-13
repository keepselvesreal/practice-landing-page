# 6.0 Introduction [auto-generated] (pp.121-122)

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


