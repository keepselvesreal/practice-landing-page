# 6.1.0 Introduction [auto-generated] (pp.122-123)

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


