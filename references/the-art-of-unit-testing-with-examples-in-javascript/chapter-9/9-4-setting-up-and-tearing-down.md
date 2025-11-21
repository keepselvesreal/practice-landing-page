# 9.4 Setting up and tearing down (pp.191-192)

---
**Page 191**

191
9.4
Setting up and tearing down
 It’s also much easier to debug the second example than the first one, if you wanted
to focus on the result value after the call. Don’t skimp on this small tip. The people
after you will whisper a small thank you when your test doesn’t make them feel stupid
for not understanding it.
9.4
Setting up and tearing down
Setup and teardown methods in unit tests can be abused to the point where the tests
or the setup and teardown methods are unreadable. The situation is usually worse in
the setup method than in the teardown method.
 The following listing shows one possible abuse that is very common: using the
setup (or beforeEach function) for setting up mocks or stubs.
describe("password verifier", () => {
  let mockLog;
  beforeEach(() => {
    mockLog = Substitute.for<IComplicatedLogger>();  
  });
  test("verify, with logger & passing, calls logger with PASS",() => {
    const verifier = new PasswordVerifier2([], mockLog);  
    verifier.verify("anything");
    mockLog.received().info(                              
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
}); 
If you set up mocks and stubs in a setup method, that means they don’t get set up in
the actual test. That, in turn, means that whoever is reading your test may not even
realize that there are mock objects in use, or what the test expects from them.
 The test in listing 9.6 uses the mockLog variable, which is initialized in the
beforeEach function (a setup method). Imagine you have dozens or more of these
tests in the file. The setup function is at the beginning of the file, and you are stuck
reading a test way down in the file. You come across the mockLog variable and you
have to start asking questions such as, “Where is this initialized? How will it behave
in the test?” and more. 
 Another problem that can arise if multiple mocks and stubs are used in various
tests in the same file is that the setup function becomes a dumping group for all the
various states used by your tests. It becomes a big mess, a soup of many parameters,
some used by one test and others used somewhere else. It becomes difficult to manage
and understand such a setup. 
 It’s much more readable to initialize mock objects directly in the test, with all their
expectations. The following listing is an example of initializing the mock in each test. 
Listing 9.6
Using a setup (beforeEach) function for mock setup
Setting up 
a mock
Using the
mock


---
**Page 192**

192
CHAPTER 9
Readability
describe("password verifier", () => {
  test("verify, with logger & passing,calls logger with PASS",() => {
    const mockLog = Substitute.for<IComplicatedLogger>();   
    const verifier = new PasswordVerifier2([], mockLog);
    verifier.verify("anything");
    mockLog.received().info(
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
When I look at this test, everything is clear as day. I can see when the mock is created,
its behavior, and anything else I need to know. 
 If you’re worried about maintainability, you can refactor the creation of the mock
into a helper function that each test would call. That way, you’re avoiding the generic
setup function and are instead calling the same helper function from multiple tests.
As the following listing shows, you keep the readability and gain more maintainability.
describe("password verifier", () => {
  test("verify, with logger & passing,calls logger with PASS",() => {
    const mockLog = makeMockLogger();        
    const verifier = new PasswordVerifier2([], mockLog);
    verifier.verify("anything");
    mockLog.received().info(
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
And yes, if you follow this logic, you can see that I’m perfectly OK with you not having
any setup functions in your tests. I’ve often written full test suites that don’t have a
setup function, instead calling helper methods from each test, for the sake of main-
tainability. The tests were still readable and maintainable.
Summary
When naming a test, include the name of the unit of work under test, the cur-
rent test scenario, and the expected behavior of the unit of work.
Don’t leave magic values in your tests. Either wrap them in variables with mean-
ingful names, or put the description into the value itself, if it’s a string.
Listing 9.7
Avoiding a setup function
Listing 9.8
Using a helper function
Initializing 
the mock 
in the test 
Using a helper 
function to 
initialize the 
mock


