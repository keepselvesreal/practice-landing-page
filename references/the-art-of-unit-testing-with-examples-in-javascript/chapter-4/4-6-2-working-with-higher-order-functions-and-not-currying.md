# 4.6.2 Working with higher-order functions and not currying (pp.93-94)

---
**Page 93**

93
4.6
Mocks in a functional style
    if (failed.length === 0) {
        logger.info('PASSED');
        return true;
    }
    logger.info('FAIL');
    return false;
});
The only change is the call to _.curry on the first line, and closing it off at the end of
the code block.
 The following listing demonstrates what a test for this type of code might look like.
describe("password verifier", () => {
  describe("given logger and passing scenario", () => {
    it("calls the logger with PASS", () => {
      let logged = "";
      const mockLog = { info: (text) => (logged = text) };
      const injectedVerify = verifyPassword3([], mockLog);
      // this partially applied function can be passed around
      // to other places in the code
      // without needing to inject the logger
      injectedVerify("anything");
      expect(logged).toMatch(/PASSED/);
    });
  });
});
Our test invokes the function with the first two arguments (injecting the rules and
logger dependencies, effectively returning a partially applied function), and then
invokes the returned function injectedVerify with the final input, thus showing the
reader two things:
How this function is meant to be used in real life
What the dependencies are
Other than that, it’s pretty much the same as in the previous test.
4.6.2
Working with higher-order functions and not currying
Listing 4.9 is another variation on the functional programming design. We’re using a
higher-order function, but without currying. You can tell that the following code does
not contain currying because we always need to send in all of the parameters as argu-
ments to the function for it to be able to work correctly.
 
 
 
Listing 4.8
Testing a curried function with dependency injection


---
**Page 94**

94
CHAPTER 4
Interaction testing using mock objects
const makeVerifier = (rules, logger) => {
    return (input) => {             
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
};
This time I’m explicitly making a factory function that returns a preconfigured verifier
function that already contains the rules and logger in its closure’s dependencies. 
 Now let’s look at the test for this. The test needs to first call the makeVerifier factory
function and then call the function that’s returned by that function (passVerify).
describe("higher order factory functions", () => {
  describe("password verifier", () => {
    test("given logger and passing scenario", () => {
      let logged = "";
      const mockLog = { info: (text) => (logged = text) };
      const passVerify = makeVerifier([], mockLog);      
      passVerify("any input");    
      expect(logged).toMatch(/PASSED/);
    });
  });
});
4.7
Mocks in an object-oriented style
Now that we’ve covered some functional and modular styles, let’s look at the object-
oriented styles. People coming from an object-oriented background will feel much
more comfortable with this type of approach, and people coming from a functional
background will hate it. But life is about accepting people’s differences.
4.7.1
Refactoring production code for injection
Listing 4.11 shows what this type of injection might look like in a class-based design in
JavaScript. Classes have constructors, and we use the constructor to force the caller of
the class to provide parameters. This is not the only way to accomplish that, but it’s
very common and useful in an object-oriented design because it makes the requirement
Listing 4.9
Injecting a mock in a higher-order function
Listing 4.10
Testing using a factory function
Returning a 
preconfigured 
verifier
Calling the 
factory 
function
Calling the 
resulting function


