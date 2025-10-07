
--- 페이지 132 ---
104
Isolation frameworks
In the previous chapters, we looked at writing mocks and stubs manually and saw
the challenges involved, especially when the interface we’d like to fake requires us
to create long, error prone, repetitive code. We kept having to declare custom vari-
ables, create custom functions, or inherit from classes that use those variables and
basically make things a bit more complicated than they need to be (most of the
time).
 In this chapter, we’ll look at some elegant solutions to these problems in the
form of an isolation framework—a reusable library that can create and configure fake
objects at run time. These objects are referred to as dynamic stubs and dynamic mocks.
 I call them isolation frameworks because they allow you to isolate the unit of
work from its dependencies. You’ll find that many resources will refer to them as
“mocking frameworks,” but I try to avoid that because they can be used for both
This chapter covers
Defining isolation frameworks and how they help
Two main flavors of frameworks
Faking modules with Jest
Faking functions with Jest 
Object-oriented fakes with substitute.js

--- 페이지 133 ---
105
5.1
Defining isolation frameworks
mocks and stubs. In this chapter, we’ll take a look at a few of the JavaScript frameworks
available and how we can use them in modular, functional, and object-oriented
designs. You’ll see how you can use such frameworks to test various things and to cre-
ate stubs, mocks, and other interesting things.
 But the specific frameworks I’ll present here aren’t the point. While using them,
you’ll see the values that their APIs promote in your tests (readability, maintainability,
robust and long-lasting tests, and more), and you’ll find out what makes an isolation
framework good and, alternatively, what can make it a drawback for your tests.
5.1
Defining isolation frameworks
I’ll start with a basic definition that may sound a bit bland, but it needs to be generic
in order to include the various isolation frameworks out there: 
An isolation framework is a set of programmable APIs that allow the dynamic creation,
configuration, and verification of mocks and stubs, either in object or function form.
When using an isolation framework, these tasks are often simpler, quicker, and produce
shorter code than hand-coded mocks and stubs.
Isolation frameworks, when used properly, can save developers from the need to write
repetitive code to assert or simulate object interactions, and if applied in the right
places, they can help make tests last many years without requiring a developer to come
back and fix them after every little production code change. If they’re applied badly,
they can cause confusion and full-on abuse of these frameworks, to the point where
we either can’t read or can’t trust our own tests, so be wary. I’ll discuss some dos and
don’ts in part 3 of this book.
5.1.1
Choosing a flavor: Loose vs. typed 
Because JavaScript supports multiple paradigms of programming design, we can split
the frameworks in our world into two main flavors:
Loose JavaScript isolation frameworks—These are vanilla JavaScript-friendly loose-
typed isolation frameworks (such as Jest and Sinon). These frameworks usually
also lend themselves better to more functional styles of code because they
require less ceremony and boilerplate code to do their work.
Typed JavaScript isolation frameworks—These are more object-oriented and Type-
Script-friendly isolation frameworks (such as substitute.js). They’re very useful
when dealing with whole classes and interfaces.
Which flavor you end up choosing to use in your project will depend on a few things,
like taste, style, and readability, but the main question to start with is, what type of
dependencies will you mostly need to fake?
Module dependencies (imports, requires)—Jest and other loosely typed frameworks
should work well.
Functional (single and higher-order functions, simple parameters and values)—Jest and
other loosely typed frameworks should work well.

--- 페이지 134 ---
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

--- 페이지 135 ---
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

--- 페이지 136 ---
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

--- 페이지 137 ---
109
5.3
Functional dynamic mocks and stubs
 Also note that Jest has many other APIs and abilities, and its worth exploring them
if you’re interested in using it. Head over to https://jestjs.io/ to get the full picture—
it’s beyond the scope of this book, which is mostly about patterns, not tools.
 A few other frameworks, among them Sinon (https://sinonjs.org), also support
faking modules. Sinon is quite pleasant to work with, as far as isolation frameworks go,
but like many other frameworks in the JavaScript world, and much like Jest, it contains
too many ways of accomplishing the same task, and that can often be confusing. Still,
faking modules by hand can be quite annoying without these frameworks.
5.2.2
Consider abstracting away direct dependencies
The good news about the jest.mock API, and others like it, is that it meets a very real
need for developers who are stuck trying to test modules that have baked-in depen-
dencies that are not easily changeable (i.e., code they cannot control). This issue is
very prevalent in legacy code situations, which I’ll discuss in chapter 12.
 The bad news about the jest.mock API is that it also allows us to mock the code
that we do control and that might have benefited from abstracting away the real
dependencies behind simpler, shorter, internal APIs. This approach, also known as
onion architecture or hexagonal architecture or ports and adapters, is very useful for the long-
term maintainability of our code. You can read more about this type of architecture in
Alistair Cockburn’s article, “Hexagonal Architecture,” at https://alistair.cockburn.us/
hexagonal-architecture/.
 Why are direct dependencies potentially problematic? By using those APIs directly,
we’re also forced into faking the module APIs directly in our tests instead of their
abstractions. We’re gluing the design of those direct APIs to the implementation of
the tests, which means that if (or really, when) those APIs change, we’ll also need to
change many of our tests. 
 Here’s a quick example. Imagine your code depends on a well-known JavaScript
logging framework (such as Winston) and depends on it directly in hundreds or
thousands of places in the code. Then imagine that Winston releases a breaking
upgrade. Lots of pain will ensue, which could have been addressed much earlier,
before things got out of hand. One simple way to accomplish this would be with a
simple abstraction to a single adapter file, which is the only one holding a reference
to that logger. That abstraction can expose a simpler, internal logging API that we
do control, so we can prevent large-scale breakage across our code. I’ll return to this
subject in chapter 12.
5.3
Functional dynamic mocks and stubs
We covered modular dependencies, so let’s turn to faking simple functions. We’ve
done that plenty of times in the previous chapters, but we’ve always done it by hand.
That works great for stubs, but for mocks it gets annoying fast.
 The following listing shows the manual approach we used before.
 

--- 페이지 138 ---
110
CHAPTER 5
Isolation frameworks
test("given logger and passing scenario", () => {
  let logged = "";                            
  const mockLog = { info: (text) => (logged = text) };   
  const passVerify = makeVerifier([], mockLog);
  passVerify("any input");
  expect(logged).toMatch(/PASSED/);   
});
It works—we’re able to verify that the logger function was called, but that’s a lot of work
that can become very repetitive. Enter isolation frameworks like Jest. jest.fn() is the
simplest way to get rid of such code. The following listing shows how we can use it.
test('given logger and passing scenario', () => {
  const mockLog = { info: jest.fn() };
  const verify = makeVerifier([], mockLog);
  verify('any input');
  expect(mockLog.info)
    .toHaveBeenCalledWith(stringMatching(/PASS/));
});
Compare this code with the previous example. It’s subtle, but it saves plenty of time.
Here we’re using jest.fn() to get back a function that is automatically tracked by
Jest, so that we can query it later using Jest’s API via toHaveBeenCalledWith(). It’s
small and cute, and it works well any time you need to track calls to a specific function.
The stringMatching function is an example of a matcher. A matcher is usually defined
as a utility function that can assert on the value of a parameter being sent into a func-
tion. The Jest docs use the term a bit more liberally, but you can find the full list of
matchers in the Jest documentation at https://jestjs.io/docs/en/expect. 
 To summarize, jest.fn() works well for single-function-based mocks and stubs.
Let’s move on to a more object-oriented challenge.
5.4
Object-oriented dynamic mocks and stubs
As we’ve just seen, jest.fn() is an example of a single-function faking utility func-
tion. It works well in a functional world, but it breaks down a bit when we try to use it
on full-blown API interfaces or classes that contain multiple functions. 
5.4.1
Using a loosely typed framework
I mentioned before that there are two categories of isolation frameworks. To start, we’ll
use the first (loosely typed, function-friendly) kind. The following listing is an example
of trying to tackle the IComplicatedLogger we looked at in the previous chapter. 
Listing 5.3
Manually mocking a function to verify it was called
Listing 5.4
Using jest.fn() for simple function mocks
Declaring a custom variable 
to hold the value passed in
Saving the 
passed-in value 
to that variable
Asserting on the 
value of the variable

--- 페이지 139 ---
111
5.4
Object-oriented dynamic mocks and stubs
export interface IComplicatedLogger {
    info(text: string, method: string)
    debug(text: string, method: string)
    warn(text: string, method: string)
    error(text: string, method: string)
}
Creating a handwritten stub or mock for this interface may be very time consuming,
because you’d need to remember the parameters on a per-method basis, as the next
listing shows.
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    class FakeLogger implements IComplicatedLogger {
      debugText = "";
      debugMethod = "";
      errorText = "";
      errorMethod = "";
      infoText = "";
      infoMethod = "";
      warnText = "";
      warnMethod = "";
      debug(text: string, method: string) {
        this.debugText = text;
        this.debugMethod = method;
      }
      error(text: string, method: string) {
        this.errorText = text;
        this.errorMethod = method;
      }
      ...
    }
    test("verify, w logger & passing, calls logger with PASS", () => {
      const mockLog = new FakeLogger();
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.infoText).toMatch(/PASSED/);
    });
  });
});
What a mess. Not only is this handwritten fake time consuming and cumbersome to
write, what happens if you want it to return a specific value somewhere in the test, or
Listing 5.5
The IComplicatedLogger interface
Listing 5.6
Handwritten stubs creating lots of boilerplate code

--- 페이지 140 ---
112
CHAPTER 5
Isolation frameworks
simulate an error from a function call on the logger? We can do it, but the code gets
ugly fast.
 Using an isolation framework, the code for doing this becomes trivial, more read-
able, and much shorter. Let’s use jest.fn() for the same task and see where we end up.
import stringMatching = jasmine.stringMatching;
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    test("verify, w logger & passing, calls logger with PASS", () => {
      const mockLog: IComplicatedLogger = {    
        info: jest.fn(),                       
        warn: jest.fn(),                       
        debug: jest.fn(),                      
        error: jest.fn(),                      
      };
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.info)
        .toHaveBeenCalledWith(stringMatching(/PASS/));
    });
  });
});
Not too shabby. Here we simply outline our own object and attach a jest.fn() func-
tion to each of the functions in the interface. This saves a lot of typing, but it has one
important caveat: whenever the interface changes (a function is added, for example),
we’ll have to go back to the code that defines this object and add that function. With
plain JavaScript, this would be less of an issue, but it can still create some complica-
tions if the code under test uses a function we didn’t define in the test. 
 In any case, it might be wise to push the creation of such a fake object into a fac-
tory helper method, so that the creation only exists in a single place.
5.4.2
Switching to a type-friendly framework
Let’s switch to the second category of frameworks and try substitute.js (www.npmjs
.com/package/@fluffy-spoon/substitute). We have to choose one, and I like the C#
version of this framework a lot and used it in the previous edition of this book. 
 With substitute.js (and the assumption of working with TypeScript), we can write
code like the following.
import { Substitute, Arg } from "@fluffy-spoon/substitute";
describe("working with long interfaces", () => {
  describe("password verifier", () => {
Listing 5.7
Mocking individual interface functions with jest.fn()
Listing 5.8
Using substitute.js to fake a full interface
Setting up the 
mock using Jest

--- 페이지 141 ---
113
5.4
Object-oriented dynamic mocks and stubs
    test("verify, w logger & passing, calls logger w PASS", () => {
      const mockLog = Substitute.for<IComplicatedLogger>();   
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      mockLog.received().info(                 
        Arg.is((x) => x.includes("PASSED")),   
        "verify"                               
      );
    });
  });
});
In the preceding listing, we generate the fake object, which absolves us of caring
about any functions other than the one we’re testing against, even if the object’s signa-
ture changes in the future. We then use .received() as our verification mechanism,
as well as another argument matcher, Arg.is, this time from substitute.js’s API, which
works just like string matches from Jasmine. The added benefit here is that if new
functions are added to the object’s signature, we will be less likely to need to change
the test, and there’s no need to add those functions to any tests that use the same
object signature.  
OK, that was mocks. What about stubs?
Isolation frameworks and the Arrange-Act-Assert pattern
Notice that the way you use the isolation framework matches nicely with the Arrange-
Act-Assert structure, which we discussed in chapter 1. You start by arranging a fake
object, you act on the thing you’re testing, and then you assert on something at the
end of the test. 
It wasn’t always this easy, though. In the olden days (around 2006), most of the open
source isolation frameworks didn’t support the idea of Arrange-Act-Assert and instead
used a concept called Record-Replay (we’re talking about Java and C#). Record-
Replay was a nasty mechanism where you’d have to tell the isolation API that its fake
object was in record mode, and then you’d have to call the methods on that object
as you expected them to be called from production code. Then you’d have to tell the
isolation API to switch into replay mode, and only then could you send your fake object
into the heart of your production code. An example can be seen on the Baeldung site
at www.baeldung.com/easymock.
Compared to today’s ability to write tests that use the far more readable Arrange-Act-
Assert model, this tragedy cost many developers millions of combined hours in pains-
taking test reading to figure out exactly where tests failed.
If you have the first edition of this book, you can see an example of Record-Replay
when I showed Rhino Mocks (which initially had the same design).
Generating 
the fake 
object
Verifying the 
fake object 
was called

--- 페이지 142 ---
114
CHAPTER 5
Isolation frameworks
5.5
Stubbing behavior dynamically
Jest has a very simple API for simulating return values for modular and functional
dependencies: mockReturnValue() and mockReturnValueOnce().
test("fake same return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValue("abc");
  //value remains the same
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
});
test("fake multiple return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValueOnce("a")
    .mockReturnValueOnce("b")
    .mockReturnValueOnce("c");
  //value remains the same
  expect(stubFunc()).toBe("a");
  expect(stubFunc()).toBe("b");
  expect(stubFunc()).toBe("c");
  expect(stubFunc()).toBe(undefined);
});
Notice that, in the first test, we’re setting a permanent return value for the duration of
the test. This is my preferred method of writing tests if I can use it, because it makes
the tests simple to read and maintain. If we do need to simulate multiple values, we
can use mockReturnValueOnce. 
 If you need to simulate an error or do anything more complicated, you can use
mockImplementation() and mockImplementationOnce():
yourStub.mockImplementation(() => {
  throw new Error();
});
5.5.1
An object-oriented example with a mock and a stub
Let’s add another ingredient into our Password Verifier equation. 
Let’s say that the Password Verifier is not active during a special maintenance
window, when software is being updated. 
When a maintenance window is active, calling verify() on the verifier will
cause it to call logger.info() with “under maintenance.” 
Otherwise it will call logger.info() with a “passed” or “failed” result. 
Listing 5.9
Stubbing a value from a fake function with jest.fn() 

--- 페이지 143 ---
115
5.5
Stubbing behavior dynamically
For this purpose (and for the purpose of showing an object-oriented design decision),
we’ll introduce a MaintenanceWindow interface that will be injected into the construc-
tor of our Password Verifier, as illustrated in figure 5.3.
The following listing shows the code for the Password Verifier using the new dependency.
export class PasswordVerifier3 {
  private _rules: any[];
  private _logger: IComplicatedLogger;
  private _maintenanceWindow: MaintenanceWindow;
  constructor(
    rules: any[],
    logger: IComplicatedLogger,
    maintenanceWindow: MaintenanceWindow
  ) {
    this._rules = rules;
    this._logger = logger;
    this._maintenanceWindow = maintenanceWindow;
  }
  verify(input: string): boolean {
    if (this._maintenanceWindow.isUnderMaintenance()) {
      this._logger.info("Under Maintenance", "verify");
      return false;
    }
    const failed = this._rules
      .map((rule) => rule(input))
      .filter((result) => result === false);
    if (failed.length === 0) {
      this._logger.info("PASSED", "verify");
      return true;
    }
Listing 5.10
Password Verifier with a MaintenanceWindow dependency
verify()
Password
Verifier
MaintenanceWindow
Logger
info()
isUnderMaintenance(): bool
Figure 5.3
Using the MaintenanceWindow interface

--- 페이지 144 ---
116
CHAPTER 5
Isolation frameworks
    this._logger.info("FAIL", "verify");
    return false;
  }
}
The MaintenanceWindow interface is injected as a constructor parameter (i.e., using
constructor injection), and it’s used to determine where to execute or not execute the
password verification and send the proper message to the logger.
5.5.2
Stubs and mocks with substitute.js
Now we’ll use substitute.js instead of Jest to create a stub of the MaintenanceWindow
interface and a mock of the IComplicatedLogger interface. Figure 5.4 illustrates this.
Creating stubs and mocks with substitute.js works the same way: we use the Substi-
tute.for<T> function. We can configure stubs with the .returns function and verify
mocks with the .received function. Both of these are part of the fake object that is
returned from Substitute.for<T>(). 
 Here’s what stub creation and configuration looks like:
const stubMaintWindow = Substitute.for<MaintenanceWindow>();
stubMaintWindow.isUnderMaintenance().returns(true);
Mock creation and verification looks like this:
const mockLog = Substitute.for<IComplicatedLogger>();
. . .
/// later down in the end of the test…
mockLog.received().info("Under Maintenance", "verify");
verify()
Password
Verifier
MaintenanceWindow
Logger
info()
isUnderMaintenance(): bool
Stub
Mock
Test
Figure 5.4
A MaintenanceWindow dependency

--- 페이지 145 ---
117
5.6
Advantages and traps of isolation frameworks
The following listing shows the full code for a couple of tests that use a mock and a stub.
import { Substitute } from "@fluffy-spoon/substitute";
const makeVerifierWithNoRules = (log, maint) =>
  new PasswordVerifier3([], log, maint);
describe("working with substitute part 2", () => {
  test("verify, during maintanance, calls logger", () => {
    const stubMaintWindow = Substitute.for<MaintenanceWindow>();
    stubMaintWindow.isUnderMaintenance().returns(true);
    const mockLog = Substitute.for<IComplicatedLogger>();
    const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
    verifier.verify("anything");
    mockLog.received().info("Under Maintenance", "verify");
  });
  test("verify, outside maintanance, calls logger", () => {
    const stubMaintWindow = Substitute.for<MaintenanceWindow>();
    stubMaintWindow.isUnderMaintenance().returns(false);
    const mockLog = Substitute.for<IComplicatedLogger>();
    const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
    verifier.verify("anything");
    mockLog.received().info("PASSED", "verify");
  });
});
We can successfully and relatively easily simulate values in our tests with dynamically
created objects. I encourage you to research the flavor of an isolation framework
you’d like to use. I’ve only used substitute.js as an example in this book. It’s not the
only framework out there.
 This test requires no handwritten fakes, but notice that it’s already starting to take
a toll on the readability for the test reader. Functional designs are usually much slim-
mer than this. In an object-oriented setting, sometimes this is a necessary evil. How-
ever, we could easily refactor the creation of various helpers, mocks, and stubs to
helper functions as we refactor our code, so that the test can be simpler and shorter to
read. More on that in part 3 of this book.
5.6
Advantages and traps of isolation frameworks
Based on what we’ve covered in this chapter, we’ve seen distinct advantages to using
isolation frameworks:
Easier modular faking—Module dependencies can be hard to get around without
some boilerplate code, which isolation frameworks help us eliminate. This point
Listing 5.11
Testing Password Verifier with substitute.js

--- 페이지 146 ---
118
CHAPTER 5
Isolation frameworks
can also be counted as a negative, as explained earlier, because it encourages us
to have code strongly coupled to third-party implementations.
Easier simulation of values or errors—Writing mocks manually can be difficult
across a complicated interface. Frameworks help a lot.
Easier fake creation—Isolation frameworks can be used to create both mocks and
stubs more easily. 
Although there are many advantages to using isolation frameworks, there are also pos-
sible dangers. Let’s now talk about a few things to watch out for.
5.6.1
You don’t need mock objects most of the time
The biggest trap that isolation frameworks lead you into is making it easy to fake any-
thing, and encouraging you to think you need mock objects in the first place. I’m not
saying you won’t need stubs, but mock objects shouldn’t be the standard operating
procedure for most unit tests. Remember that a unit of work can have three different
types of exit points: return values, state change, and calling a third-party dependency.
Only one of these types can benefit from a mock object in your test. The others don’t.
 I find that, in my own tests, mock objects are present in perhaps 2%–5% of my tests.
The rest of the tests are usually return-value or state-based tests. For functional designs,
the number of mock objects should be near zero, except for some corner cases.
 If you find yourself defining a test and verifying that an object or function was
called, think carefully whether you can prove the same functionality without a mock
object, but instead by verifying a return value or a change in the behavior of the over-
all unit of work from the outside (for example, verifying that a function throws an
exception when it didn’t before). Chapter 6 of Unit Testing Principles, Practices, and Pat-
terns by Vladimir Khorikov (Manning, 2020) contains a detailed description of how to
refactor interaction-based tests into simpler, more reliable tests that check a return
value instead.
5.6.2
Unreadable test code
Using a mock in a test makes the test a little less readable, but still readable enough
that an outsider can look at it and understand what’s going on. Having many mocks,
or many expectations, in a single test can ruin the readability of the test so it’s hard to
maintain, or even to understand what’s being tested.
 If you find that your test becomes unreadable or hard to follow, consider removing
some mocks or some mock expectations, or separating the test into several smaller
tests that are more readable.
5.6.3
Verifying the wrong things
Mock objects allow you to verify that methods were called on your interfaces or that
functions were called, but that doesn’t necessarily mean that you’re testing the right
thing. A lot of people new to tests end up verifying things just because they can, not
because it makes sense. Examples may include the following:

--- 페이지 147 ---
119
Summary
Verifying that an internal function calls another internal function (not an
exit point).
Verifying that a stub was called (an incoming dependency should not be veri-
fied; it’s the overspecification antipattern, as we’ll discuss in section 5.6.5).
Verifying that something was called simply because someone told you to write a
test, and you’re not sure what should really be tested. (This is a good time to
verify that you’re understanding the requirements correctly.)
5.6.4
Having more than one mock per test
It’s considered good practice to test only one concern per test. Testing more than one
concern can lead to confusion and problems maintaining the test. Having two mocks
in a test is the same as testing several end results of the same unit of work (multiple
exit points).
 For each exit point, consider writing a separate test, as it could be considered a
separate requirement. Chances are that your test names will also become more focused
and readable when you only test one concern. If you can’t name your test because it
does too many things and the name becomes very generic (e.g., “XWorksOK”), it’s time
to separate it into more than one test.
5.6.5
Overspecifying the tests
If your test has too many expectations (x.received().X(), x.received().Y(), and so
on), it may become very fragile, breaking on the slightest of production code changes,
even though the overall functionality still works. Testing interactions is a double-
edged sword: test them too much, and you start to lose sight of the big picture—the
overall functionality; test them too little, and you’ll miss the important interactions
between units of work. 
 Here are some ways to balance this effect:
Use stubs instead of mocks when you can—If more than 5% of your tests use mock
objects, you might be overdoing it. Stubs can be everywhere. Mocks, not so
much. You only need to test one scenario at a time. The more mocks you
have, the more verifications will take place at the end of the test, but usually
only one will be the important one. The rest will be noise against the current
test scenario.
Avoid using stubs as mocks if possible—Use a stub only for faking simulated values
into the unit of work under test or to throw exceptions. Don’t verify that meth-
ods were called on stubs.
Summary
Isolation, or mocking, frameworks allow you to dynamically create, configure,
and verify mocks and stubs, either in object or function form. Isolation frame-
works save a lot of time compared to handwritten fakes, especially in modular
dependency situations.

--- 페이지 148 ---
120
CHAPTER 5
Isolation frameworks
There are two flavors of isolation frameworks: loosely typed (such as Jest and
Sinon) and strongly typed (such as substitute.js). Loosely typed frameworks
require less boilerplate and are good for functional-style code; strongly typed
frameworks are useful when dealing with classes and interfaces.
Isolation frameworks can replace whole modules, but try to abstract away direct
dependencies and fake those abstractions instead. This will help you reduce the
amount of refactoring needed when the module’s API changes.
It's important to lean toward return-value or state-based testing as opposed to
interaction testing whenever you can, so that your tests assume as little as possi-
ble about internal implementation details.
Mocks should be used only when there’s no other way to test the implementa-
tion, because they eventually lead to tests that are harder to maintain if you’re
not careful.
Choose the way you work with isolation frameworks based on the codebase you
are working on. In legacy projects, you may need to fake whole modules, as it
might be the only way to add tests to such projects. In greenfield projects, try to
introduce proper abstractions on top of third-party modules. It’s all about pick-
ing the right tool for the job, so be sure to look at the big picture when consid-
ering how to approach a specific problem in testing.
