# 5.2.1 Some things to notice about Jest’s API (pp.108-109)

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


---
**Page 109**

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
 


