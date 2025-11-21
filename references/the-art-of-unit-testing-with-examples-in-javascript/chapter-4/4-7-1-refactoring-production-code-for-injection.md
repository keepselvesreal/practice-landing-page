# 4.7.1 Refactoring production code for injection (pp.94-96)

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


---
**Page 95**

95
4.7
Mocks in an object-oriented style
of those parameters explicit and practically undeniable in strongly typed languages
such as Java or C, and when using TypeScript. We want to make sure whoever uses our
code knows what is expected to configure it properly.
class PasswordVerifier {
  _rules;
  _logger;
  constructor(rules, logger) {
    this._rules = rules;
    this._logger = logger;
  }
  verify(input) {
    const failed = this._rules
        .map(rule => rule(input))
        .filter(result => result === false);
    if (failed.length === 0) {
      this._logger.info('PASSED');
      return true;
    }
    this._logger.info('FAIL');
    return false;
  }
}
This is just a standard class that takes a couple of constructor parameters and then
uses them inside the verify function. The following listing shows what a test might
look like. 
describe("duck typing with function constructor injection", () => {
  describe("password verifier", () => {
    test("logger&passing scenario,calls logger with PASSED", () => {
      let logged = "";
      const mockLog = { info: (text) => (logged = text) };
      const verifier = new PasswordVerifier([], mockLog);
      verifier.verify("any input");
      expect(logged).toMatch(/PASSED/);
    });
  });
});   
Mock injection is straightforward, much like with stubs, as we saw in the previous
chapter. If we were to use properties rather than a constructor, it would mean that
the dependencies are optional. With a constructor, we’re explicitly saying they’re not
optional.
Listing 4.11
Class-based constructor injection
Listing 4.12
Injecting a mock logger as a constructor parameter


---
**Page 96**

96
CHAPTER 4
Interaction testing using mock objects
 In strongly typed languages like Java or C#, it’s common to extract the fake logger
as a separate class, like so:
class FakeLogger {
  logged = "";
  info(text) {
    this.logged = text;
  }
}
We simply implement the info function in the class, but instead of logging anything,
we just save the value being sent as a parameter to the function in a publicly visible
variable that we can assert again later in our test.
 Notice that I didn’t call the fake object MockLogger or StubLogger but FakeLogger.
This is so that I can reuse this class in multiple different tests. In some tests, it might
be used as a stub, and in others it might be used as a mock object. I use the word
“fake” to denote anything that isn’t real. Another common term for this sort of thing is
“test double.” Fake is shorter, so I like it. 
 In our tests, we’ll instantiate the class and send it over as a constructor parameter,
and then we’ll assert on the logged variable of the class, like so:
test("logger + passing scenario, calls logger with PASSED", () => {
   let logged = "";
   const mockLog = new FakeLogger();
   const verifier = new PasswordVerifier([], mockLog);
   verifier.verify("any input");
   expect(mockLog.logged).toMatch(/PASSED/);
});
4.7.2
Refactoring production code with interface injection
Interfaces play a large role in many object-oriented programs. They are one variation
on the idea of polymorphism: allowing one or more objects to be replaced with one
another as long as they implement the same interface. In JavaScript and other lan-
guages like Ruby, interfaces are not needed, since the language allows for the idea of
duck typing without needing to cast an object to a specific interface. I won’t touch
here on the pros and cons of duck typing. You should be able to use either technique
as you see fit, in the language of your choice. In JavaScript, we can turn to TypeScript
to use interfaces. The compiler, or transpiler, we’ll use can help ensure that we are
using types based on their signatures correctly.
 Listing 4.13 shows three code files: the first describes a new ILogger interface, the
second describes a SimpleLogger that implements that interface, and the third is our
PasswordVerifier, which uses only the ILogger interface to get a logger instance.
PasswordVerifier has no knowledge of the actual type of logger being injected. 


