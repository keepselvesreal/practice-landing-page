# 4.5.0 Introduction [auto-generated] (pp.89-90)

---
**Page 89**

89
4.5
Modular-style mocks
Readability—Your test name will become much more generic and harder to
understand. You want people to be able to read the name of the test and know
everything that happens or is tested inside of it, without needing to read the
test’s code.
Maintainability—You could, without noticing or even caring, assert against stubs
if you don’t differentiate between mocks and stubs. This produces little value to
you and increases the coupling between your tests and internal production
code. Asserting that you queried a database is a good example of this. Instead of
testing that a database query returns some value, it would be much better to test
that the application’s behavior changes after we change the input from the
database. 
Trust—If you have multiple mocks (requirements) in a single test, and the first
mock verification fails the test, most test frameworks won’t execute the rest of
the test (below the failing assert line) because an exception has been thrown.
This means that the other mocks aren’t verified, and you won’t get the results
from them.
To drive the last point home, imagine a doctor who only sees 30% of their patient’s
symptoms, but still needs to make a decision—they might make the wrong decision
about treatment. If you can’t see where all the bugs are, or that two things are failing
instead of just one (because one of them is hidden after the first failure), you’re more
likely to fix the wrong thing or to fix it in the wrong place. 
 XUnit Test Patterns (Addison-Wesley, 2007), by Gerard Meszaros, calls this situation
assertion roulette (http://xunitpatterns.com/Assertion%20Roulette.html). I like this
name. It’s quite a gamble. You start commenting out lines of code in your test, and lots
of fun ensues (and possibly alcohol).
4.5
Modular-style mocks
I covered modular dependency injection in the previous chapter, but now we’re going
to look at how we can use it to inject mock objects and simulate answers on them.
Not everything is a mock
It’s unfortunate that people still tend to use the word “mock” for anything that isn’t
real, such as “mock database” or “mock service.” Most of the time they really mean
they are using a stub. 
It’s hard to blame them, though. Frameworks like Mockito, jMock, and most isolation
frameworks (I don’t call them mocking frameworks, for the same reasons I’m dis-
cussing right now), use the word “mock” to denote both mocks and stubs. 
There are newer frameworks, such as Sinon and testdouble in JavaScript, NSubsti-
tute and FakeItEasy in .NET, and others, that have helped start a change in the nam-
ing conventions. I hope this persists.


---
**Page 90**

90
CHAPTER 4
Interaction testing using mock objects
4.5.1
Example of production code
Let’s look at a slightly more complicated example than we saw before. In this scenario,
our verifyPassword function depends on two external dependencies: 
 A logger 
 A configuration service
The configuration service provides the logging level that is required. Usually this type
of code would be moved into a special logger module, but for the purposes of this
book’s examples, I’m putting the logic that calls logger.info and logger.debug
directly in the code under test.
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
module.exports = {
  verifyPassword,
};
Let’s assume that we realized we have a bug when we call the logger. We’ve changed
the way we check for failures, and now we call the logger with a PASSED result when
the number of failures is positive instead of zero. How can we prove that this bug
exists, or that we’ve fixed it, with a unit test?
 Our problem here is that we are importing (or requiring) the modules directly in
our code. If we want to replace the logger module, we have to either replace the file or
perform some other dark magic through Jest’s API. I wouldn’t recommend that usually,
Listing 4.4
A hard modular dependency 
Calling the 
logger


