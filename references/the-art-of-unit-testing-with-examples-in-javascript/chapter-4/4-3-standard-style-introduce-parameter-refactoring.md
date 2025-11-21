# 4.3 Standard style: Introduce parameter refactoring (pp.87-88)

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


---
**Page 88**

88
CHAPTER 4
Interaction testing using mock objects
    info: (text) => {
        written = text;
    }
};
It only has one function, which mimics the signature of the logger’s info function. It
then saves the parameter being passed to it (text) so that we can assert that it was
called later in the test. If the written variable has the correct text, this proves that our
function was called, which means we have proven that the exit point is invoked cor-
rectly from our unit of work. 
 On the verifyPassword2 side, the refactoring we did is pretty common. It’s pretty
much the same as we did in the previous chapter, where we extracted a stub as a
dependency. Stubs and mocks are often treated the same way in terms of refactoring
and introducing seams in our application’s code.
 What did this simple refactoring into a parameter provide us with? 
We do not need to explicitly import (via require) the logger in our code
under test anymore. That means that if we ever change the real dependency of
the logger, the code under test will have one less reason to change. 
We now have the ability to inject any logger of our choosing into the code under
test, as long as it lives up to the same interface (or at least has the info
method). This means that we can provide a mock logger that does our bidding
for us: the mock logger helps us verify that it was called correctly. 
NOTE
The fact that our mock object only mimics a part of the logger’s inter-
face (it’s missing the debug function) is a form of duck typing. I discussed this
idea in chapter 3: if it walks like a duck, and it talks like a duck, then we can
use it as a fake object.
4.4
The importance of differentiating between mocks 
and stubs
Why do I care so much about what we name each thing? If we can’t tell the difference
between mocks and stubs, or we don’t name them correctly, we can end up with tests
that are testing multiple things and that are less readable and harder to maintain.
Naming things correctly helps us avoid these pitfalls. 
 Given that a mock represents a requirement from our unit of work (“it calls the
logger,” “it sends an email,” etc.) and that a stub represents incoming information or
behavior (“the database query returns false,” “this specific configuration throws an
error”), we can set a simple rule of thumb: It should be OK to have multiple stubs in a
test, but you don’t usually want to have more than a single mock per test, because that
would mean you’re testing more than one requirement in a single test.
 If we can’t (or won’t) differentiate between things (naming is key to that), we can
end up with multiple mocks per test or asserting our stubs, both of which can have neg-
ative effects on our tests. Keeping naming consistent gives us the following benefits:


