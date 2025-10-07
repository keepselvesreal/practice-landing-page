
--- 페이지 111 ---
83
Interaction testing
using mock objects
In the previous chapter, we solved the problem of testing code that depends on
other objects to run correctly. We used stubs to make sure that the code under
test received all the inputs it needed so that we could test the unit of work in
isolation.
 So far, you’ve only written tests that work against the first two of the three types
of exit points a unit of work can have: returning a value and changing the state of the
system (you can read more about these types in chapter 1). In this chapter, we’ll
look at how you can test the third type of exit point—a call to a third-party func-
tion, module, or object. This is important, because often we’ll have code that
depends on things we can’t control. Knowing how to check that type of code is an
important skill in the world of unit testing. Basically, we’ll find ways to prove that
This chapter covers
Defining interaction testing 
Reasons to use mock objects
Injecting and using mocks
Dealing with complicated interfaces
Partial mocks

--- 페이지 112 ---
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
 
 
 
 
 
 
 

--- 페이지 113 ---
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

--- 페이지 114 ---
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

--- 페이지 115 ---
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

--- 페이지 116 ---
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

--- 페이지 117 ---
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

--- 페이지 118 ---
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

--- 페이지 119 ---
91
4.5
Modular-style mocks
because using these techniques leads to more pain and suffering than is usual when
dealing with code. 
4.5.2
Refactoring the production code in a modular injection style
We can abstract away the module dependencies into their own object and allow the
user of our module to replace that object as follows.
const originalDependencies = {             
    log: require('./complicated-logger'),  
};                                         
let dependencies = { ...originalDependencies };    
const resetDependencies = () => {                
    dependencies = { …originalDependencies };    
};                                               
const injectDependencies = (fakes) => {    
    Object.assign(dependencies, fakes);    
};                                         
const verifyPassword = (input, rules) => {
    const failed = rules
        .map(rule => rule(input))
        .filter(result => result === false);
    if (failed.length === 0) {
        dependencies.log.info('PASSED');
        return true;
    }
    dependencies.log.info('FAIL');
    return false;
};
module.exports = {
    verifyPassword,        
    injectDependencies,    
    resetDependencies      
};
There’s more production code here, and it seems more complex, but this allows us to
replace dependencies in our tests in a relatively easy manner if we are forced to work
in such a modular fashion. 
 The originalDependencies variable will always hold the original dependencies, so
that we never lose them between tests. dependencies is our layer of indirection. It
defaults to the original dependencies, but our tests can direct the code under test to
replace that variable with custom dependencies (without knowing anything about the
internals of the module). injectDependencies and resetDependencies are the pub-
lic API that the module exposes for overriding and resetting the dependencies. 
Listing 4.5
Refactoring to a modular injection pattern
Holding original 
dependencies
The layer of 
indirection
A function that resets 
the dependencies 
A function that overrides 
the dependencies
Exposing the API to the 
users of the module

--- 페이지 120 ---
92
CHAPTER 4
Interaction testing using mock objects
4.5.3
A test example with modular-style injection
The following listing shows what a test for modular injection might look like.
const {
  verifyPassword,
  injectDependencies,
  resetDependencies,
} = require("./password-verifier-injectable");
describe("password verifier", () => {
  afterEach(resetDependencies);
  describe("given logger and passing scenario", () => {
    it("calls the logger with PASS", () => {
      let logged = "";
      const mockLog = { info: (text) => (logged = text) };
      injectDependencies({ log: mockLog });
      verifyPassword("anything", []);
      expect(logged).toMatch(/PASSED/);
    });
  });
});
As long as we don’t forget to use the resetDependencies function after each test, we
can now inject modules pretty easily for test purposes. The obvious main caveat is that
this approach requires each module to expose inject and reset functions that can be
used from the outside. This might or might not work with your current design limita-
tions, but if it does, you can abstract them both into reusable functions and save your-
self a lot of boilerplate code.
4.6
Mocks in a functional style 
Let’s jump into a few of the functional styles we can use to inject mocks into our code
under test.
4.6.1
Working with a currying style
Let’s implement the currying technique introduced in chapter 3 to perform a more
functional-style injection of our logger. In the following listing, we’ll use lodash, a
library that facilitates functional programming in JavaScript, to get currying working
without too much boilerplate code.
const verifyPassword3 = _.curry((rules, logger, input) => {
    const failed = rules
        .map(rule => rule(input))
        .filter(result => result === false);
Listing 4.6
Testing with modular injection
Listing 4.7
Applying currying to our function

--- 페이지 121 ---
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

--- 페이지 122 ---
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

--- 페이지 123 ---
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

--- 페이지 124 ---
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

--- 페이지 125 ---
97
4.7
Mocks in an object-oriented style
export interface ILogger {    
    info(text: string);       
}                             
//this class might have dependencies on files or network
class SimpleLogger implements ILogger {   
    info(text: string) {
    }
}
export class PasswordVerifier {
    private _rules: any[];
    private _logger: ILogger;                      
    constructor(rules: any[], logger: ILogger) {   
        this._rules = rules;
        this._logger = logger;                     
    }
    verify(input: string): boolean {
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
Notice that a few things have changed in the production code. I’ve added a new inter-
face to the production code, and the existing logger now implements this interface.
I’m changing the design to make the logger replaceable. Also, the PasswordVerifier
class works with the interface instead of the SimpleLogger class. This allows me to
replace the instance of the logger class with a fake one, instead of having a hard
dependency on the real logger. 
 The following listing shows what a test might look like in a strongly typed language,
but with a handwritten fake object that implements the ILogger interface.
class FakeLogger implements ILogger {
    written: string;
    info(text: string) {
        this.written = text;
    }
}
Listing 4.13
Production code gets an ILogger interface
Listing 4.14
Injecting a handwritten mock ILogger 
A new interface, 
which is part of 
production code
The logger now 
implements that 
interface.
The verifier
now uses the
interface.

--- 페이지 126 ---
98
CHAPTER 4
Interaction testing using mock objects
describe('password verifier with interfaces', () => {
    test('verify, with logger, calls logger', () => {
        const mockLog = new FakeLogger();
        const verifier = new PasswordVerifier([], mockLog);
        verifier.verify('anything');
        expect(mockLog.written).toMatch(/PASS/);
    });
});
In this example, I’ve created a handwritten class called FakeLogger. All it does is over-
ride the one method in the ILogger interface and save the text parameter for future
assertion. We then expose this value as a field in the written class. Once this value is
exposed, we can verify that the fake logger was called by checking that field.
 I’ve done this manually because I wanted you to see that even in object-oriented
land, the patterns repeat themselves. Instead of having a mock function, we now have a
mock object, but the code and test work just like the previous examples. 
4.8
Dealing with complicated interfaces
What happens when the interface is more complicated, such as when it has more than
one or two functions in it, or more than one or two parameters in each function?
4.8.1
Example of a complicated interface
Listing 4.15 is an example of such a complicated interface, and of the production
code verifier that uses the complicated logger, injected as an interface. The ICompli-
catedLogger interface has four functions, each with one or more parameters. Every
function would need to be faked in our tests, and that can lead to complexity and
maintainability problems in our code and tests.
export interface IComplicatedLogger {   
    info(text: string)
    debug(text: string, obj: any)
Interface naming conventions
I’m using the naming convention of prefixing the logger interface with an “I” because
it’s going to be used for polymorphic reasons (i.e., I’m using it to abstract a role in
the system). This is not always the case for interface naming in TypeScript, such as
when we use interfaces to define the structure of a set of parameters (basically using
them as strongly typed structures). In that case, naming without an “I” makes sense
to me. 
For now, think of it like this: If you’re going to implement it more than once, you
should prefix it with an “I” to make the expected use of the interface more explicit. 
Listing 4.15
Working with a more complicated interface (production code)
A new interface, which is 
part of production code

--- 페이지 127 ---
99
4.8
Dealing with complicated interfaces
    warn(text: string)
    error(text: string, location: string, stacktrace: string)
}
export class PasswordVerifier2 {
    private _rules: any[];
    private _logger: IComplicatedLogger;                     
    constructor(rules: any[], logger: IComplicatedLogger) {  
        this._rules = rules;
        this._logger = logger;
    }
...
}
As you can see, the new IComplicatedLogger interface will be part of production
code, which will make the logger replaceable. I’m leaving off the implementation of a
real logger, because it’s not relevant for our examples. That’s the benefit of abstract-
ing away things with an interface: we don’t need to reference them directly. Also
notice that the type of parameter expected in the class’s constructor is that of the
IComplicatedLogger interface. This allows me to replace the instance of the logger
class with a fake one, just like we did before.
4.8.2
Writing tests with complicated interfaces
Here’s what the test looks like. It has to override each and every interface function,
which creates long and annoying boilerplate code.
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    class FakeComplicatedLogger            
        implements IComplicatedLogger {    
      infoWritten = "";
      debugWritten = "";
      errorWritten = "";
      warnWritten = "";
      debug(text: string, obj: any) {
        this.debugWritten = text;
      }
      error(text: string, location: string, stacktrace: string) {
        this.errorWritten = text;
      }
      info(text: string) {
        this.infoWritten = text;
      }
      warn(text: string) {
        this.warnWritten = text;
Listing 4.16
Test code with a complicated logger interface
The class now 
works with the 
new interface.
A fake logger class that 
implements the new interface

--- 페이지 128 ---
100
CHAPTER 4
Interaction testing using mock objects
      }
    }
    ...
    test("verify passing, with logger, calls logger with PASS", () => {
      const mockLog = new FakeComplicatedLogger();
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.infoWritten).toMatch(/PASSED/);
    });
    test("A more JS oriented variation on this test", () => {
      const mockLog = {} as IComplicatedLogger;
      let logged = "";
      mockLog.info = (text) => (logged = text);
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(logged).toMatch(/PASSED/);
    });
  });
});
Here, we’re declaring, again, a fake logger class (FakeComplicatedLogger) that imple-
ments the IComplicatedLogger interface. Look at how much boilerplate code we
have. This will be especially true if we’re working in strongly typed object-oriented lan-
guages such as Java, C#, or C++. There are ways around all this boilerplate code, which
we’ll touch on in the next chapter. 
4.8.3
Downsides of using complicated interfaces directly
There are other downsides to using long, complicated interfaces in our tests:
If we’re saving arguments being sent in manually, it’s more cumbersome to ver-
ify multiple arguments across multiple methods and calls. 
It’s likely that we are depending on third-party interfaces instead of internal
ones, and this will end up making our tests more brittle as time goes by. 
Even if we are depending on internal interfaces, long interfaces have more rea-
sons to change, and now so do our tests. 
What does this mean for us? I highly recommend using only fake interfaces that meet
both of these conditions:
You control the interfaces (they are not made by a third party).
They are adapted to the needs of your unit of work or component. 

--- 페이지 129 ---
101
4.9
Partial mocks
4.8.4
The interface segregation principle
The second of the preceding conditions might need a bit of explanation. It relates
to the interface segregation principle (ISP; https://en.wikipedia.org/wiki/Interface_
segregation_principle). ISP means that if we have an interface that contains more
functionality than we require, we should create a small, simpler adapter interface that
contains just the functionality we need, preferably with fewer functions, better names,
and fewer parameters. 
 This will end up making our tests much simpler. By abstracting away the real
dependencies, we won’t need to change our tests when the complicated interfaces
change—only a single adapter class file somewhere. We’ll see an example of this in
chapter 5.
4.9
Partial mocks
It’s possible, in JavaScript and in most other languages and associated test frameworks,
to take over existing objects and functions and “spy” on them. By spying on them, we
can later check if they were called, how many times, and with which arguments. 
 This essentially can turn parts of a real object into mock functions, while keeping
the rest of the object as a real object. This can create more complicated tests that are
more brittle, but it can sometimes be a viable option, especially if you’re dealing with
legacy code (see chapter 12 for more on legacy code). 
4.9.1
A functional example of a partial mock
The following listing shows what such a test might look like. We create the real logger,
and then we simply override one of its existing real functions using a custom function.
describe("password verifier with interfaces", () => {
  test("verify, with logger, calls logger", () => {
    const testableLog: RealLogger = new RealLogger();   
    let logged = "";
    testableLog.info = (text) => (logged = text);   
    const verifier = new PasswordVerifier([], testableLog);
    verifier.verify("any input");
    expect(logged).toMatch(/PASSED/);
  });
});
In this test, I’m instantiating a RealLogger, and in the next line I’m replacing one of
its existing functions with a fake one. More specifically, I’m using a mock function that
allows me to track its latest invocation parameter using a custom variable.
 The important part here is that the testableLog variable is a partial mock. That
means that at least some of its internal implementation is not fake and might have real
dependencies and logic in it.
Listing 4.17
A partial mock example 
Instantiating a 
real logger
Mocking one of 
its functions

--- 페이지 130 ---
102
CHAPTER 4
Interaction testing using mock objects
 Sometimes it makes sense to use partial mocks, especially when you’re working
with legacy code and you might need to isolate some existing code from its dependen-
cies. I’ll touch more on that in chapter 12.
4.9.2
An object-oriented partial mock example
One object-oriented version of a partial mock uses inheritance to override functions
from real classes so that we can verify they were called. The following listing shows
how we can do this using inheritance and overrides in JavaScript.
class TestableLogger extends RealLogger {    
  logged = "";
  info(text) {             
    this.logged = text;    
  }                        
  // the error() and debug() functions
  // are still "real"
}
describe("partial mock with inheritance", () => {
  test("verify with logger, calls logger", () => {
    const mockLog: TestableLogger = new TestableLogger();
    const verifier = new PasswordVerifier([], mockLog);
    verifier.verify("any input");
    expect(mockLog.logged).toMatch(/PASSED/);
  });
});
I inherit from the real logger class in my tests and then use the inherited class, not the
original class, in my tests. This technique is commonly called Extract and Override,
and you can find more about this in Michael Feathers’ book Working Effectively with
Legacy Code (Pearson, 2004). 
 Note that I’ve named the fake logger class “TestableXXX” because it’s a testable
version of real production code, containing a mix of fake and real code, and this
convention helps me make this explicit for the reader. I also put the class right
alongside my tests. My production code doesn’t need to know that this class exists.
This Extract and Override style requires that my class in production code allows
inheritance and that the function allows overriding. In JavaScript this is less of an
issue, but in Java and C# these are explicit design choices that need to be made
(although there are frameworks that allow us to circumvent this rule; we’ll discuss
them in the next chapter).
 In this scenario, we’re inheriting from a class that we’re not testing directly (Real-
Logger). We use that class to test another class (PasswordVerifier). However, this
technique can be used quite effectively to isolate and stub or mock single functions
Listing 4.18
An object-oriented partial mock example 
Inheriting from 
the real logger
Overriding one 
of its functions

--- 페이지 131 ---
103
Summary
from classes that you’re directly testing. We’ll touch more on that later in the book
when we talk about legacy code and refactoring techniques.
Summary
Interaction testing is a way to check how a unit of work interacts with its outgoing
dependencies: what calls were made and with which parameters. Interaction
testing relates to the third type of exit points: a third-party module, object, or
system. (The first two types are a return value and a state change.)
To do interaction testing, you should use mocks, which are test doubles that replace
outgoing dependencies. Stubs replace incoming dependencies. You should ver-
ify interactions with mocks in tests, but not with stubs. Unlike with mocks, inter-
actions with stubs are implementation details and shouldn't be checked.
It’s OK to have multiple stubs in a test, but you don’t usually want to have more
than a single mock per test, because that means you’re testing more than one
requirement in a single test.
Just like with stubs, there are multiple ways to inject a mock into a unit of work:
– Standard—By introducing a parameter
– Functional—Using a partial application or factory functions
– Modular—Abstracting the module dependency
– Object-oriented—Using an untyped object (in languages like JavaScript) or a
typed interface (in TypeScript)
In JavaScript, a complicated interface can be implemented partially, which
helps reduce the amount of boilerplate. There’s also the option of using partial
mocks, where you inherit from a real class and replace only some of its methods
with fakes.
