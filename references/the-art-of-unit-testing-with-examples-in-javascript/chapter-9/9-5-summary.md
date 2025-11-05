# 9.5 Summary (pp.192-194)

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


---
**Page 193**

193
Summary
Separate assertions from actions. Merging the two shortens the code but makes
it significantly harder to understand.
Try not to use test setups at all (such as beforeEach methods). Introduce helper
methods to simplify the test’s arrange part, and use those helper methods in
each test.


---
**Page 194**

194
Developing
a testing strategy
Unit tests represent just one of the types of tests you could and should write. In this
chapter, we’ll discuss how unit testing fits into an organizational testing strategy. As
soon as we start to look at other types of tests, we start asking some really important
questions:
At what level do we want to test various features? (UI, backend, API, unit,
etc.)
How do we decide at which level to test a feature? Do we test it multiple times
on many levels?
Should we have more functional end-to-end tests or more unit tests?
This chapter covers
Testing level pros and cons
Common antipatterns in test levels
The test recipe strategy
Delivery-blocking and non-blocking tests
Delivery vs. discovery pipelines
Test parallelization


