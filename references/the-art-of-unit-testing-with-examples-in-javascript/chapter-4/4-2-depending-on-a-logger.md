# 4.2 Depending on a logger (pp.85-87)

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


---
**Page 86**

86
CHAPTER 4
Interaction testing using mock objects
const debug = (text) => {
    console.log(`DEBUG: ${text}`);
};
Figure 4.2 illustrates this. Our verifyPassword function is the entry point to the unit
of work, and we have a total of two exit points: one that returns a value, and another
that calls log.info().
Unfortunately, we cannot verify that logger was called by using any traditional means,
or without using some Jest tricks, which I usually use only if there’s no other choice, as
they tend to make tests less readable and harder to maintain (more on that later in
this chapter).
 Let’s do what we like to do with dependencies: abstract them. There are many ways
to create a seam in our code. Remember, seams are places where two pieces of code
meet—we can use them to inject fake things. Table 4.1 lists the most common ways to
abstract dependencies.
Table 4.1
Techniques for injecting fakes
Style
Technique
Standard
Introduce parameter
Functional
Use currying
Convert to higher-order functions
Modular
Abstract module dependency
Object oriented
Inject untyped object
Inject interface
verifyPassword(input, rules)
Return value
Password
verifier
Third-party
log.info(text)
Figure 4.2
The entry point 
to the Password Verifier is the 
verifyPassword function. One 
exit point returns a value, and the 
other calls log.info().


---
**Page 87**

87
4.3
Standard style: Introduce parameter refactoring
4.3
Standard style: Introduce parameter refactoring
The most obvious way we can start this journey is by introducing a new parameter into
our code under test. 
const verifyPassword2 = (input, rules, logger) => {
    const failed = rules
        .map(rule => rule(input))
        .filter(result => result === false);
    if (failed.length === 0) {
        logger.info('PASSED');
        return true;
    }
    logger.info('FAIL');
    return false;
};
The following listing shows how we could write the simplest of tests for this, using a
simple closure mechanism.
describe('password verifier with logger', () => {
    describe('when all rules pass', () => {
        it('calls the logger with PASSED', () => {
            let written = '';
            const mockLog = {
                info: (text) => {
                    written = text;
                }
            };
            verifyPassword2('anything', [], mockLog);
            expect(written).toMatch(/PASSED/);
        });
    });
});
Notice first that we are naming the variable mockXXX (mockLog in this example) to
denote the fact that we have a mock function or object in the test. I use this naming
convention because I want you, as a reader of the test, to know that you should expect
an assert (also known as verification) against that mock at the end of the test. This nam-
ing approach removes the element of surprise for the reader and makes the test much
more predictable. Only use this naming convention for things that are actually mocks. 
 Here’s our first mock object:
let written = '';
const mockLog = {
Listing 4.2
Mock logger parameter injection
Listing 4.3
Handwritten mock object


