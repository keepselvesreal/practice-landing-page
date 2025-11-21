# 4.1 Interaction testing, mocks, and stubs (pp.84-85)

---
**Page 84**

84
CHAPTER 4
Interaction testing using mock objects
our unit of work ends up calling a function that we don’t control and identify what val-
ues were sent as arguments. 
 The approaches we’ve looked at so far won’t do here, because third-party func-
tions usually don’t have specialized APIs that allow us to check if they were called
correctly. Instead, they internalize their operations for clarity and maintainability.
So, how can you test that your unit of work interacts with third-party functions cor-
rectly? You use mocks.
4.1
Interaction testing, mocks, and stubs
Interaction testing is checking how a unit of work interacts with and sends messages
(i.e., calls functions) to a dependency beyond its control. Mock functions or objects
are used to assert that a call was made correctly to an external dependency.
 Let’s recall the differences between mocks and stubs as we covered them in chap-
ter 3. The main difference is in the flow of information: 
Mock—Used to break outgoing dependencies. Mocks are fake modules, objects,
or functions that we assert were called in our tests. A mock represents an exit
point in a unit test. If we don’t assert on it, it’s not used as a mock. 
It is normal to have no more than a single mock per test, for maintainability
and readability reasons. (We’ll discuss this more in part 3 of this book about
writing maintainable tests.)
Stub—Used to break incoming dependencies. Stubs are fake modules, objects,
or functions that provide fake behavior or data to the code under test. We do
not assert against them, and we can have many stubs in a single test. 
Stubs represent waypoints, not exit points, because the data or behavior
flows into the unit of work. They are points of interaction, but they do not repre-
sent an ultimate outcome of the unit of work. Instead, they are an interaction
on the way to achieving the end result we care about, so we don’t treat them as
exit points.
Figure 4.1 shows these two side by side.
 Let’s look at a simple example of an exit point to a dependency that we do not con-
trol: calling a logger.
 
 
 
 
 
 
 


---
**Page 85**

85
4.2
Depending on a logger
4.2
Depending on a logger
Let’s take this Password Verifier function as our starting example, and we’ll assume we
have a complicated logger (which is a logger that has more functions and parameters,
so the interface may present more of a challenge). One of the requirements of our
function is to call the logger when verification has passed or failed, as follows.
// impossible to fake with traditional injection techniques
const log = require('./complicated-logger');
const verifyPassword = (input, rules) => {
  const failed = rules
    .map(rule => rule(input))
    .filter(result => result === false);
  if (failed.count === 0) {
    // to test with traditional injection techniques
    log.info('PASSED');                                      
    return true; //                                          
  }
  //impossible to test with traditional injection techniques
  log.info('FAIL'); //                                       
  return false; //                                           
};
const info = (text) => {
    console.log(`INFO: ${text}`);
};
Listing 4.1
Depending directly on a complicated logger 
Test
Entry point
Exit point
Data
or behavior
Dependency
Unit
of
work
Test
Entry point
Exit point
Dependency
Unit
of
work
Outgoing dependency
(use mocks)
Incoming dependency
(use stubs)
Figure 4.1
On the left, an exit point that is implemented as invoking a dependency. On the right, the dependency 
provides indirect input or behavior and is not an exit point.
Exit
point


