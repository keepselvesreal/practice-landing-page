# 5.2.0 Introduction [auto-generated] (pp.106-108)

---
**Page 106**

106
CHAPTER 5
Isolation frameworks
Full objects, object hierarchies, and interfaces—Look into the more object-oriented
frameworks, such as substitute.js.
Let’s go back to our Password Verifier and see how we can fake the same types of
dependencies we did in previous chapters, but this time using a framework.
5.2
Faking modules dynamically
For people who are trying to test code with direct dependencies on modules using
require or import, isolation frameworks such as Jest or Sinon present the powerful
ability to fake an entire module dynamically, with very little code. Since we started with
Jest as our test framework, we’ll stick with it for the examples in this chapter.
 Figure 5.1 illustrates a Password Verifier with two dependencies:
A configuration service that helps decide what the logging level is (INFO or ERROR)
A logging service that we call as the exit point of our unit of work, whenever we
verify a password
The arrows represent the flow of behavior through the unit of work. Another way to
think about the arrows is through the terms command and query. We are querying the
configuration service (to get the log level), but we are sending commands to the log-
ger (to log).
The following listing shows a Password Verifier that has a hard dependency on a log-
ger module.
 
Command/query separation
There is a school of design that falls under the ideas of command/query separation. If
you’d like to learn more about these terms, I highly recommend reading Martin Fowler’s
2005 article on the topic, at https://martinfowler.com/bliki/CommandQuerySeparation
.html. This pattern is very beneficial as you navigate your way around different design
ideas, but we won’t be touching on this too much in this book.
Import
Import
Password
Verifier
configuration-service.js
complicated-logger.js
info()
getLogLevel(): string
Figure 5.1
Password Verifier has two dependencies: an incoming one to determine the logging level, and an 
outgoing one to create a log entry.


---
**Page 107**

107
5.2
Faking modules dynamically
const { info, debug } = require("./complicated-logger");
const { getLogLevel } = require("./configuration-service");
const log = (text) => {
  if (getLogLevel() === "info") {
    info(text);
  }
  if (getLogLevel() === "debug") {
    debug(text);
  }
};
const verifyPassword = (input, rules) => {
  const failed = rules
    .map((rule) => rule(input))
    .filter((result) => result === false);
  if (failed.length === 0) {
    log("PASSED");
    return true;
  }
  log("FAIL");
  return false;
};
In this example we’re forced to find a way to do two things:
Simulate (stub) values returned from the configuration service’s getLogLevel
function.
Verify (mock) that the logger module’s info function was called.
Figure 5.2 shows a visual representation of this.
Listing 5.1
Code with hardcoded modular dependencies
verify()
Mock
Stub
Import
Import
Password
Verifier
Test
configuration-service.js
complicated-logger.js
info()
getLogLevel(): string
Assert
Figure 5.2
The test stubs an incoming dependency (the configuration service) and mocks the outgoing 
dependency (the logger).


---
**Page 108**

108
CHAPTER 5
Isolation frameworks
Jest presents us with a few ways to accomplish both simulation and verification, and
one of the cleaner ways it presents is using jest.mock([module name]) at the top of
the spec file, followed by us requiring the fake modules in our tests so that we can con-
figure them.
jest.mock("./complicated-logger");      
jest.mock("./configuration-service");   
const { stringMatching } = expect;
const { verifyPassword } = require("./password-verifier");
const mockLoggerModule = require("./complicated-logger");     
const stubConfigModule = require("./configuration-service");  
describe("password verifier", () => {
  afterEach(jest.resetAllMocks);   
  test('with info log level and no rules, 
          it calls the logger with PASSED', () => {
    stubConfigModule.getLogLevel.mockReturnValue("info");   
    verifyPassword("anything", []);
    expect(mockLoggerModule.info)                      
      .toHaveBeenCalledWith(stringMatching(/PASS/));   
  });
  test('with debug log level and no rules, 
        it calls the logger with PASSED', () => {
    stubConfigModule.getLogLevel.mockReturnValue("debug");   
    verifyPassword("anything", []);
    expect(mockLoggerModule.debug)                     
      .toHaveBeenCalledWith(stringMatching(/PASS/));   
  });
});
By using Jest here, I’ve saved myself a bunch of typing, and the tests still look pretty
readable.
5.2.1
Some things to notice about Jest’s API
Jest uses the word “mock” almost everywhere, whether we’re stubbing things or mock-
ing them, which can be a bit confusing. It’d be great if it had the word “stub” aliased
to “mock” to make things more readable.
 Also, due to the way JavaScript “hoisting” works, the lines faking the modules (via
jest.mock) will need to be at the top of the file. You can read more about this in
Ashutosh Verma’s “Understanding Hoisting in JavaScript” article here: http://mng
.bz/j11r.
Listing 5.2
Faking the module APIs directly with jest.mock()
Faking the modules
Getting the fake 
instances of the 
modules
Telling Jest to reset any fake 
module behavior between tests
Configuring the 
stub to return a 
fake “info” value.
Asserting that the mock 
was called correctly
Changing the 
stub config
Asserting on the mock 
logger as done previously


