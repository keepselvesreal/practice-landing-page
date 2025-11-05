# 8.1.2 Changes in the production code’s API (pp.166-169)

---
**Page 166**

166
CHAPTER 8
Maintainability
Which test failures force us to change the test?
When do we choose to change a test even if we are not forced to?
This chapter presents a series of practices related to maintainability that you can use
when doing test reviews.
8.1
Changes forced by failing tests
A failing test is usually the first sign of potential trouble for maintainability. Of course,
we could have found a real bug in production code, but when that’s not the case, what
other reasons do tests have to fail? I’ll refer to genuine failures as true failures, and fail-
ures that happen for reasons other than finding a bug in the underlying production
code as false failures.
 If we wanted to measure test maintainability, we could start by measuring the num-
ber of false test failures, and the reason for each failure, over time. We already dis-
cussed one such reason in chapter 7: when a test contains a bug. Let’s now discuss
other possible reasons for false failures. 
8.1.1
The test is not relevant or conflicts with another test
A conflict may arise when the production code introduces a new feature that’s in
direct conflict with one or more existing tests. Instead of the test discovering a bug, it
may discover conflicting or new requirements. There might also be a passing test that
targets the new expectation for how the production code should work. 
 Either the existing failing test is no longer relevant, or the new requirement is
wrong. Assuming that the requirement is correct, you can probably go ahead and
delete the no-longer-relevant test.
 Note that there’s a common exception to the “remove the test” rule: when you’re
working with feature toggles. We’ll touch on feature toggles in chapter 10 when we dis-
cuss testing strategies.
8.1.2
Changes in the production code’s API
A test can fail if the production code under test changes so that a function or object
being tested now needs to be used differently, even though it may still have the same
functionality. Such false failures fall in the bucket of “let’s avoid this as much as possible.”
 Consider the PasswordVerifier class in listing 8.1, which requires two constructor
parameters: 
An array of rules (each is a function that takes an input and returns a Boolean)
An ILogger interface
export class PasswordVerifier {
    ...
    constructor(rules: ((input) => boolean)[], logger: ILogger) {
        this._rules = rules;
Listing 8.1
A Password Verifier with two constructor parameters


---
**Page 167**

167
8.1
Changes forced by failing tests
        this._logger = logger;
    }
    ...
}
We could write a couple of tests like the following.
describe("password verifier 1", () => {
  it("passes with zero rules", () => {
    const verifier = new PasswordVerifier([], { info: jest.fn() });   
    const result = verifier.verify("any input");
    expect(result).toBe(true);
  });
  it("fails with single failing rule", () => {
    const failingRule = (input) => false;
    const verifier = 
      new PasswordVerifier([failingRule], { info: jest.fn() });       
    const result = verifier.verify("any input");
    expect(result).toBe(false);
  });
});
If we look at these tests from a maintainability point of view, there are several potential
changes we will likely need to make in the future. 
CODE USUALLY LIVES FOR A LONG TIME
Consider that the code you’re writing will live in the codebase for at least 4–6 years
and sometimes a decade. Over that time, what is the likelihood that the design of
PasswordVerifier will change? Even simple things, like the constructor accepting
more parameters, or the parameter types changing, become more likely over a longer
timeframe. 
 Let’s list a few changes that could happen to our Password Verifier in the future:
We may add or remove a parameter in the constructor for PasswordVerifier.
One of the parameters for PasswordVerifier may change to a different type.
The number of ILogger functions or their signatures may change over time.
The usage pattern changes so we don’t need to instantiate a new Password-
Verifier, but just use the functions in it directly.
If any of these things happen, how many tests would we need to change? Right now
we’d need to change all the tests that instantiate PasswordVerifier. Could we prevent
the need for some of these changes? 
 Let’s pretend the future is here and our fears have come true—someone changed
the production code’s API. Let’s say the constructor signature has changed to use
IComplicatedLogger instead of ILogger, as follows.
Listing 8.2
Tests without factory functions
Test using
the code’s
existing API


---
**Page 168**

168
CHAPTER 8
Maintainability
export class PasswordVerifier2 {
  private _rules: ((input: string) => boolean)[];
  private _logger: IComplicatedLogger;
  constructor(rules: ((input) => boolean)[], 
      logger: IComplicatedLogger) {
    this._rules = rules;
    this._logger = logger;
  }
...
}
As it stands, we would have to change any test that directly instantiates PasswordVerifier. 
FACTORY FUNCTIONS DECOUPLE CREATION OF OBJECT UNDER TEST
A simple way to avoid this pain in the future is to decouple or abstract away the creation
of the code under test so that the changes to the constructor only need to be dealt with
in a centralized location. A function whose sole purpose is to create and preconfigure
an instance of an object is usually called a factory function or method. A more advanced
version of this (which we won’t cover here) is the Object Mother pattern.
 Factory functions can help us mitigate this issue. The next two listings show how we
could have initially written the tests before the signature change, and how we could
easily adapt to the signature change in that case. In listing 8.4, the creation of Password-
Verifier has been extracted into its own centralized factory function. I’ve done the
same for the fakeLogger—it’s now also created using its own separate factory func-
tion. If any of the changes we listed before happens in the future, we’ll only need to
change our factory functions; the tests will usually not need to be touched. 
describe("password verifier 1", () => {
  const makeFakeLogger = () => {
    return { info: jest.fn() };    
  };
  const makePasswordVerifier = (
    rules: ((input) => boolean)[],
    fakeLogger: ILogger = makeFakeLogger()) => {
      return new PasswordVerifier(rules, fakeLogger);    
  };
  it("passes with zero rules", () => {
    const verifier = makePasswordVerifier([]);  
    const result = verifier.verify("any input");
    expect(result).toBe(true);
  });
Listing 8.3
A breaking change in a constructor
Listing 8.4
Refactoring to factory functions
A centralized point for 
creating a fakeLogger
A centralized point 
for creating a 
PasswordVerifier
Using the factory 
function to create 
PasswordVerifier


---
**Page 169**

169
8.1
Changes forced by failing tests
In the following listing, I’ve refactored the tests based on the signature change. Notice
that the change doesn’t involve changing the tests, but only the factory functions.
That’s the type of manageable change I can live with in a real project.
describe("password verifier (ctor change)", () => {
  const makeFakeLogger = () => {
    return Substitute.for<IComplicatedLogger>();
  };
  const makePasswordVerifier = (
    rules: ((input) => boolean)[],
    fakeLogger: IComplicatedLogger = makeFakeLogger()) => {
    return new PasswordVerifier2(rules, fakeLogger);
  };
  // the tests remain the same
});
8.1.3
Changes in other tests
A lack of test isolation is a huge cause of test blockage—I’ve seen this while consulting
and working on unit tests. The basic concept you should keep in mind is that a test
should always run in its own little world, isolated from other tests even if they verify
the same functionality.
When tests aren’t isolated well, they can step on each other’s toes, making you regret
deciding to try unit testing and promising yourself never again. I’ve seen this happen.
Developers don’t bother looking for problems in the tests, so when there’s a problem,
Listing 8.5
Refactoring factory methods to fit a new signature
The test that cried “fail”
One project I was involved in had unit tests behaving strangely, and they got even
stranger as time went on. A test would fail and then suddenly pass for a couple of
days straight. A day later, it would fail, seemingly randomly, and other times it would
pass even if code was changed to remove or change its behavior. It got to the point
where developers would tell each other, “Ah, it’s OK. If it sometimes passes, that
means it passes.”
Properly investigated, it turned out that the test was calling out a different (and flaky)
test as part of its code, and when the other test failed, it would break the first test.
It took us three days to untangle the mess, after spending a month trying various
workarounds for the situation. When we finally had the test working correctly, we dis-
covered that we had a bunch of real bugs in our code that we were ignoring because
the test had its own bugs and issues. The story of the boy who cried wolf holds true
even in development.


