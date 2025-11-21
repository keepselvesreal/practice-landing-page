# Maintainability (pp.165-187)

---
**Page 165**

165
Maintainability
Tests can enable us to develop faster, unless they make us go slower due to all the
changes needed. If we can avoid changing existing tests when we change produc-
tion code, we can start to hope that our tests are helping rather than hurting our
bottom line. In this chapter, we’ll focus on the maintainability of tests.
 Unmaintainable tests can ruin project schedules and are often set aside when
the project is put on a more aggressive schedule. Developers will simply stop main-
taining and fixing tests that take too long to change or that need to change often as
the result of very minor production code changes. 
 If maintainability is a measure of how often we are forced to change tests, we’d
like to minimize the number of times that happens. This forces us to ask these
questions if we ever want to get down to the root causes:
When do we notice that a test fails and therefore might require a change?
Why do tests fail?
This chapter covers
Root causes of failing tests
Common avoidable changes to test code
Improving the maintainability of tests that aren’t 
currently failing


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


---
**Page 170**

170
CHAPTER 8
Maintainability
it can take a lot of time to find out what’s wrong. The easiest symptom is what I call
“constrained test order.”
CONSTRAINED TEST ORDER
A constrained test order happens when a test assumes that a previous test executed first, or
did not execute first, because it relies on some shared state that is set up or reset by the
other test. For example, if one test changes a shared variable in memory or some exter-
nal resource like a database, and another test depends on that variable’s value after the
first tests’ execution, we have a dependency between the tests based on order. 
 Couple that with the fact that most test runners don’t (and won’t, and maybe
shouldn’t!) guarantee that tests will run in a specific order. This means that if you ran
all your tests today, and all your tests a week later with a new version of the test runner,
the tests might not run in the same order as before.
 To illustrate the problem, let’s look at a simple scenario. Figure 8.1 shows a Special-
App object that uses a UserCache object. The user cache holds a single instance (a sin-
gleton) that is shared as a caching mechanism for the application, and, incidentally,
also for the tests. Listing 8.6 shows the implementation of SpecialApp, the user cache,
and the IUserDetails interface.
export interface IUserDetails {
  key: string;
  password: string;
}
export interface IUserCache {
  addUser(user: IUserDetails): void;
  getUser(key: string);
  reset(): void;
}
Listing 8.6
A shared user cache and associated interfaces
loginUser(user)
UserCache
Shared instance
SpecialApp
Test
getUser()
addUser()
Figure 8.1
A shared 
UserCache instance


---
**Page 171**

171
8.1
Changes forced by failing tests
export class UserCache implements IUserCache {
  users: object = {};
  addUser(user: IUserDetails): void {
    if (this.users[user.key] !== undefined) {
      throw new Error("user already exists");
    }
    this.users[user.key] = user;
  }
  getUser(key: string) {
    return this.users[key];
  }
  reset(): void {
    this.users = {};
  }
}
let _cache: IUserCache;
export function getUserCache() {
  if (_cache === undefined) {
    _cache = new UserCache();
  }
  return _cache;
} 
The following listing shows the SpecialApp implementation.
export class SpecialApp {
  loginUser(key: string, pass: string): boolean {
    const cache: IUserCache = getUserCache();
    const foundUser: IUserDetails = cache.getUser(key);
    if (foundUser?.password === pass) {
      return true;
    }
    return false;
  }
}
This is a simplistic implementation for this example, so don’t worry about SpecialApp
too much. Let’s look at the tests.
describe("Test Dependence", () => {
  describe("loginUser with loggedInUser", () => {
    test("no user, login fails", () => {
      const app = new SpecialApp();
      const result = app.loginUser("a", "abc");   
      expect(result).toBe(false);                 
    });
Listing 8.7
The SpecialApp implementation
Listing 8.8
Tests that need to run in a specific order
Requires the user 
cache to be empty


---
**Page 172**

172
CHAPTER 8
Maintainability
    test("can only cache each user once", () => {
      getUserCache().addUser({   
        key: "a",
        password: "abc",
      });
      expect(() =>
        getUserCache().addUser({
          key: "a",
          password: "abc",
        })
      ).toThrowError("already exists");
    });
    test("user exists, login succeeds", () => {
      const app = new SpecialApp();
      const result = app.loginUser("a", "abc");    
      expect(result).toBe(true);                   
    });
  });
});
Notice that the first and third tests both rely on the second test. The first test requires
that the second test has not executed yet, because it needs the user cache to be empty.
On the other hand, the third test relies on the second test to fill up the cache with the
expected user. If we run only the third test using Jest’s test.only keyword, the test
would fail:
test.only("user exists, login succeeds", () => {
   const app = new SpecialApp();
   const result = app.loginUser("a", "abc");
   expect(result).toBe(true); 
 });
This antipattern usually happens when we try to reuse parts of tests without extracting
helper functions. We end up expecting a different test to run first, saving us from
doing some of the setup. This works, until it doesn’t.
 We can refactor this in a few steps:
Extract a helper function for adding a user.
Reuse this function for multiple tests.
Reset the user cache between tests.
The following listing shows how we could refactor the tests to avoid this problem.
const addDefaultUser = () =>   
  getUserCache().addUser({
    key: "a",
    password: "abc",
  });
const makeSpecialApp = () => new SpecialApp();    
Listing 8.9
Refactoring tests to remove order dependence
Adds a user 
to the cache
Requires the cache 
to contain the user
Extracted user-
creation helper 
function
Extracted factory 
function


---
**Page 173**

173
8.2
Refactoring to increase maintainability
describe("Test Dependence v2", () => {
  beforeEach(() => getUserCache().reset());      
  describe("user cache", () => {                   
    test("can only add cache use once", () => {
      addDefaultUser();    
      expect(() => addDefaultUser())
        .toThrowError("already exists");
    });
  });
  describe("loginUser with loggedInUser", () => {  
    test("user exists, login succeeds", () => {
      addDefaultUser();    
      const app = makeSpecialApp();
      const result = app.loginUser("a", "abc");
      expect(result).toBe(true);
    });
    test("user missing, login fails", () => {
      const app = makeSpecialApp();
      const result = app.loginUser("a", "abc");
      expect(result).toBe(false);
    });
  });
});
There are several things going on here. First, we extracted two helper functions: a
makeSpecialApp factory function and an addDefaultUser helper function that we can
reuse. Next, we created a very important beforeEach function that resets the user
cache before each test. Whenever I have a shared resource like that, I almost always
have a beforeEach or afterEach function that resets it to its original condition before
or after the test runs.
 The first and the third tests now run in their own little nested describe structure.
They also both use the makeSpecialApp factory function, and one of them is using
addDefaultUser to make sure it does not require any other test to run first. The sec-
ond test also runs in its own nested describe function and reuses the addDefaultUser
function.
8.2
Refactoring to increase maintainability
Up until now, I’ve discussed test failures that force us to make changes. Let’s now dis-
cuss changes that we choose to make, to make tests easier to maintain over time.
8.2.1
Avoid testing private or protected methods
This section applies more to object-oriented languages as well as TypeScript. Private
or protected methods are usually private for a good reason in the developer’s mind.
Sometimes it’s to hide implementation details, so that the implementation can
Resets user cache 
between tests
New nested 
describe 
functions
Calls
reusable
helper
functions


---
**Page 174**

174
CHAPTER 8
Maintainability
change later without changing the observable behavior. It could also be for security-
related or IP-related reasons (obfuscation, for example).
 When you test a private method, you’re testing against a contract internal to the
system. Internal contracts are dynamic, and they can change when you refactor the
system. When they change, your test could fail because some internal work is being
done differently, even though the overall functionality of the system remains the
same. For testing purposes, the public contract (the observable behavior) is all you
need to care about. Testing the functionality of private methods may lead to breaking
tests, even though the observable behavior is correct. 
 Think of it this way: no private method exists in a vacuum. Somewhere down the
line, something has to call it, or it will never get triggered. Usually there’s a public
method that ends up invoking this private one, and if not, there’s always a public
method up the chain of calls that gets invoked. This means that any private method is
always part of a bigger unit of work, or use case in the system, that starts out with a
public API and ends with one of the three end results: return value, state change, or
third-party call (or all three).
 So if you see a private method, find the public use case in the system that will exer-
cise it. If you test only the private method and it works, that doesn’t mean that the rest
of the system is using this private method correctly or handles the results it provides
correctly. You might have a system that works perfectly on the inside, but all that nice
inside stuff is used incorrectly from the public APIs.
 Sometimes, if a private method is worth testing, it might be worth making it public,
static, or at least internal, and defining a public contract against any code that uses it.
In some cases, the design may be cleaner if you put the method in a different class
altogether. We’ll look at those approaches in a moment.
 Does this mean there should eventually be no private methods in the codebase?
No. With test-driven design, you usually write tests against methods that are public,
and those public methods are later refactored into calling smaller, private methods.
All the while, the tests against the public methods continue to pass.
MAKING METHODS PUBLIC
Making a method public isn’t necessarily a bad thing. In a more functional world, it’s
not even an issue. This practice may seem to go against the object-oriented principles
many of us were raised on, but that’s not always the case. 
 Consider that wanting to test a method could mean that the method has a known
behavior or contract against the calling code. By making it public, you’re making this
official. By keeping the method private, you tell all the developers who come after you
that they can change the implementation of the method without worrying about
unknown code that uses it.
EXTRACTING METHODS TO NEW CLASSES OR MODULES
If your method contains a lot of logic that can stand on its own, or it uses specialized
state variables in the class or module that are relevant only to the method in question,
it may be a good idea to extract the method into a new class or its own module with a


---
**Page 175**

175
8.2
Refactoring to increase maintainability
specific role in the system. You can then test that class separately. Michael Feathers’
Working Effectively with Legacy Code (Pearson, 2004) has some good examples of this
technique, and Clean Code by Robert Martin (Pearson, 2008) can help you figure out
when this is a good idea.
MAKING STATELESS PRIVATE METHODS PUBLIC AND STATIC
If your method is completely stateless, some people choose to refactor the method by
making it static (in languages that support this feature). That makes it much more
testable but also states that the method is a sort of utility method that has a known
public contract specified by its name.
8.2.2
Keep tests DRY
Duplication in your unit tests can hurt you, as a developer, just as much as, if not more
than, duplication in production code. That’s because any change in a piece of code
that has duplicates will force you to change all the duplicates as well. When you’re
dealing with tests, there’s more risk of the developer just avoiding this trouble and
deleting or ignoring tests instead of fixing them.
 The DRY (don’t repeat yourself) principle should be in effect in test code just as in
production code. Duplicated code means there’s more code to change when one
aspect you test against changes. Changing a constructor or changing the semantics of
using a class can have a major effect on tests that have a lot of duplicated code.
 As we’ve seen in previous examples in this chapter, using helper functions can help
to reduce duplication in tests. 
WARNING
Removing duplication can also go too far and hurt readability.
We’ll talk about that in the next chapter, on readability.
8.2.3
Avoid setup methods
I’m not a fan of the beforeEach function (also called a setup function) that happens
once before each test and is often used to remove duplication. I much prefer using
helper functions. Setup functions are too easy to abuse. Developers tend to use them
for things they weren’t meant for, and tests become less readable and less maintain-
able as a result. 
 Many developers abuse setup methods in several ways:
Initializing objects in the setup method that are used in only some tests in the file
Having setup code that’s lengthy and hard to understand
Setting up mocks and fake objects within the setup method
Also, setup methods have limitations, which you can get around by using simple
helper methods:
Setup methods can only help when you need to initialize things.
Setup methods aren’t always the best candidates for duplication removal.
Removing duplication isn’t always about creating and initializing new instances


---
**Page 176**

176
CHAPTER 8
Maintainability
of objects. Sometimes it’s about removing duplication in assertion logic or call-
ing out code in a specific way.
Setup methods can’t have parameters or return values.
Setup methods can’t be used as factory methods that return values. They’re run
before the test executes, so they must be more generic in the way they work.
Tests sometimes need to request specific things or call shared code with a
parameter for the specific test (for example, retrieving an object and setting its
property to a specific value).
Setup methods should only contain code that applies to all the tests in the cur-
rent test class, or the method will be harder to read and understand.
I’ve almost entirely stopped using setup methods for the tests I write. Test code should
be nice and clean, just like production code, but if your production code looks horri-
ble, please don’t use that as a crutch to write unreadable tests. Use factory and helper
methods, and make the world a better place for the generation of developers that will
have to maintain your code in 5 or 10 years.
NOTE
We looked at an example of moving from using beforeEach to helper
functions in section 8.2.3 (listing 8.9) and also in chapter 2.
8.2.4
Use parameterized tests to remove duplication
Another great option for replacing setup methods, if all your tests look the same, is
to use parameterized tests. Different test frameworks in different languages support
parameterized tests—if you’re using Jest, you can use the built-in test.each or it.each
functions. 
 Parameterization helps move the setup logic that would otherwise remain dupli-
cated or would reside in the beforeEach block to the test’s arrange section. It also
helps avoid duplication of the assertion logic, as shown in the following listing.
const sum = numbers => {
    if (numbers.length > 0) {
        return parseInt(numbers);
    }
    return 0;
};
describe('sum with regular tests', () => {
    test('sum number 1', () => {
        const result = sum('1');    
        expect(result).toBe(1);     
    });
    test('sum number 2', () => {
        const result = sum('2');    
        expect(result).toBe(2);     
    });
});
Listing 8.10
Parameterized tests with Jest
Duplicated setup 
and assertion logic


---
**Page 177**

177
8.3
Avoid overspecification
describe('sum with parameterized tests', () => {
    test.each([
        ['1', 1],   
        ['2', 2]    
    ])('add ,for %s, returns that number', (input, expected) => {
            const result = sum(input);       
            expect(result).toBe(expected);   
        }
    )
});
In the first describe block, we have two tests that repeat each other with different input
values and expected outputs. In the second describe block, we’re using test.each
to provide an array of arrays, where each subarray lists all the values needed for the
test function.
 Parameterized tests can help reduce a lot of duplication between tests, but we
should be careful to only use this technique in cases where we repeat the exact same
scenario and only change the input and output. 
8.3
Avoid overspecification
An overspecified test is one that contains assumptions about how a specific unit under
test (production code) should implement its internal behavior, instead of only check-
ing that the observable behavior (exit points) is correct. 
 Here are ways unit tests are often overspecified:
A test asserts purely internal state in an object under test.
A test uses multiple mocks.
A test uses stubs as mocks.
A test assumes a specific order or exact string matches when that isn’t required.
Let’s look at some examples of overspecified tests.
8.3.1
Internal behavior overspecification with mocks
A very common antipattern is to verify that an internal function in a class or module is
called, instead of checking the exit point of the unit of work. Here’s a password veri-
fier that calls an internal function, which the test shouldn’t care about.
export class PasswordVerifier4 {
  private _rules: ((input: string) => boolean)[];
  private _logger: IComplicatedLogger;
  constructor(rules: ((input) => boolean)[],
      logger: IComplicatedLogger) {
    this._rules = rules;
    this._logger = logger;
  }
Listing 8.11
Production code that calls a protected function
Test data used
for setup and
assertion
Setup and 
assertion without 
duplication


---
**Page 178**

178
CHAPTER 8
Maintainability
  verify(input: string): boolean {
    const failed = this.findFailedRules(input);   
    if (failed.length === 0) {
      this._logger.info("PASSED");
      return true;
    }
    this._logger.info("FAIL");
    return false;
  }
  protected findFailedRules(input: string) {  
    const failed = this._rules
      .map((rule) => rule(input))
      .filter((result) => result === false);
    return failed;
  }
}
Notice that we’re calling the protected findFailedRules function to get a result from
it, and then doing a calculation on the result. 
 Here’s our test.
describe("verifier 4", () => {
  describe("overspecify protected function call", () => {
    test("checkfailedFules is called", () => {
      const pv4 = new PasswordVerifier4(
        [], Substitute.for<IComplicatedLogger>()
      ); 
      const failedMock = jest.fn(() => []);    
      pv4["findFailedRules"] = failedMock;     
      pv4.verify("abc");
      expect(failedMock).toHaveBeenCalled();    
    });
  });
});
The antipattern here is that we’re proving something that isn’t an exit point. We’re
checking that the code calls some internal function, but what does that really prove?
We’re not checking that the calculation was correct on the result; we’re simply testing
for the sake of testing. 
 If the function is returning a value, usually that’s a strong indication that we
shouldn’t mock that function because the function call itself does not represent the
exit point. The exit point is the value returned from the verify() function. We
shouldn’t care whether the internal function even exists. 
 By verifying against a mock of a protected function that is not an exit point, we are
coupling our test implementation to the internal implementation of the code under
Listing 8.12
An overspecified test verifying a call to a protected function
Call to the 
internal 
function
Internal 
function
Mocking the 
internal function
Verifying the 
internal function 
call. Don’t do this.


---
**Page 179**

179
8.3
Avoid overspecification
test, for no real benefit. When the internal calls change (and they will) we will also
have to change all the tests associated with these calls, and that will not be a positive
experience. You can read more about mocks and their relation to test fragility in
chapter 5 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov (Man-
ning, 2020).
WHAT SHOULD WE DO INSTEAD?
Look for the exit point. The real exit point depends on the type of test we wish to
perform:
Value-based test—For a value-based test, which I would highly recommend you
lean toward when possible, we look for a return value from the called function.
In this case, the verify function returns a value, so it’s the perfect candidate for
a value-based test: pv4.verify("abc").
State-based test—For a state-based test, we look for a sibling function (a function
that exists at the same level of scope as the entry point) or a sibling property
that is affected by calling the verify() function. For example, firstname()
and lastname() could be considered sibling functions. That is where we should
be asserting. In this codebase, nothing is affected by calling verify() that is vis-
ible at the same level, so it is not a good candidate for state-based testing.
Third-party test—For a third-party test, we would have to use a mock, and that
would require us to find out where the fire-and-forget location is inside the
code. The findFailedRules function isn’t that, because it is actually delivering
information back to our verify() function. In this case, there’s no real third-
party dependency that we have to take over.
8.3.2
Exact outputs and ordering overspecification
A common antipattern is when a test overspecifies the order and the structure of a col-
lection of returned values. It’s often easier to specify the whole collection, along with
each of its items, in the assertion, but with this approach, we implicitly take on the
burden of fixing the test when any little detail of the collection changes. Instead of
using a single huge assertion, we should separate different aspects of the verification
into smaller, explicit asserts.
 The following listing shows a verify() function that takes on multiple inputs and
returns a list of result objects.
interface IResult {
  result: boolean;
  input: string;
}
export class PasswordVerifier5 {
  private _rules: ((input: string) => boolean)[];
Listing 8.13
A verifier that returns a list of outputs


---
**Page 180**

180
CHAPTER 8
Maintainability
  constructor(rules: ((input) => boolean)[]) {
    this._rules = rules;
  }
  verify(inputs: string[]): IResult[] {
    const failedResults = 
      inputs.map((input) => this.checkSingleInput(input));
    return failedResults;
  }
  private checkSingleInput(input: string): IResult {
    const failed = this.findFailedRules(input);
    return {
      input,
      result: failed.length === 0,
    };
  }
This verify() function returns an array of IResult objects with an input and result
in each. The following listing shows a test that makes an implicit check on both the
ordering of the results and the structure of each result, as well as checking the value of
the results.
test("overspecify order and schema", () => {
  const pv5 = 
    new PasswordVerifier5([input => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results).toEqual([           
    { input: "a", result: false },    
    { input: "ab", result: false },   
    { input: "abc", result: true },   
    { input: "abcd", result: true },  
  ]);
});
How might this test change in the future? Here are quite a few reasons for it to change:
When the length of the results array changes
When each result object gains or removes a property (even if the test doesn’t
care about those properties)
When the order of the results changes (even if it might not be important for
the current test)
If any of these changes happens in the future, but your test is just focused on checking
the logic of the verifier and the structure of its output, there’s going to be a lot of pain
involved in maintaining this test.
 We can reduce some of that pain by verifying only the parts that matter to us.
Listing 8.14
Overspecifying order and schema of the result 
A single 
huge assert


---
**Page 181**

181
8.3
Avoid overspecification
test("overspecify order but ignore schema", () => {
  const pv5 = 
    new PasswordVerifier5([(input) => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results.length).toBe(4);
  expect(results[0].result).toBe(false);
  expect(results[1].result).toBe(false);
  expect(results[2].result).toBe(true);
  expect(results[3].result).toBe(true);
});
Instead of providing the full expected output, we can simply assert on the values of
specific properties in the output. However, we’re still stuck if the order of the results
changes. If we don’t care about the order, we can simply check if the output contains a
specific result, as follows.
test("ignore order and schema", () => {
  const pv5 = 
    new PasswordVerifier5([(input) => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results.length).toBe(4);
  expect(findResultFor("a")).toBe(false);
  expect(findResultFor("ab")).toBe(false);
  expect(findResultFor("abc")).toBe(true);
  expect(findResultFor("abcd")).toBe(true);
});
Here we are using findResultFor() to find the specific result for a given input. Now
the order of the results can change, or extra values can be added, but our test will only
fail if the calculation of the true or false results changes. 
 Another common antipattern people tend to repeat is to assert against hardcoded
strings in the unit’s return value or properties, when only a specific part of a string is
necessary. Ask yourself, “Can I check if a string contains something rather than equals
something?” Here’s a password verifier that gives us a message describing how many
rules were broken during a verification.
export class PasswordVerifier6 {
  private _rules: ((input: string) => boolean)[];
  private _msg: string = "";
Listing 8.15
Ignoring the schema of the results
Listing 8.16
Ignoring order and schema
Listing 8.17
A verifier that returns a string message


---
**Page 182**

182
CHAPTER 8
Maintainability
  constructor(rules: ((input) => boolean)[]) {
    this._rules = rules;
  }
  getMsg(): string {
    return this._msg;
  }
  verify(inputs: string[]): IResult[] {
    const allResults = 
      inputs.map((input) => this.checkSingleInput(input));
    this.setDescription(allResults);
    return allResults;
  }
  private setDescription(results: IResult[]) {
    const failed = results.filter((res) => !res.result);
    this._msg = `you have ${failed.length} failed rules.`;
  }
The following listing shows two tests that use getMsg(). 
describe("verifier 6", () => {
  test("over specify string", () => {
    const pv5 = 
      new PasswordVerifier6([(input) => input.includes("abc")]);
    pv5.verify(["a", "ab", "abc", "abcd"]);
    const msg = pv5.getMsg();
    expect(msg).toBe("you have 2 failed rules.");   
  });
  //Here's a better way to write this test
  test("more future proof string checking", () => {
    const pv5 = 
      new PasswordVerifier6([(input) => input.includes("abc")]);
    pv5.verify(["a", "ab", "abc", "abcd"]);
    const msg = pv5.getMsg();
    expect(msg).toMatch(/2 failed/);    
  });
});
The first test checks that the string exactly equals another string. This backfires often,
because strings are a form of user interface. We tend to change them slightly and
embellish them over time. For example, do we care that there is a period at the end of
the string? Our test requires us to care, but the meat of the assert is the correct num-
ber being shown (especially since strings change in different computer languages or
cultures, but numbers usually stay the same).
Listing 8.18
Overspecifying a string using equality
Overly specific 
string expectation
A better way to assert 
against a string


---
**Page 183**

183
Summary
 The second test simply looks for the “2 failed” string inside the message. This
makes the test more future-proof: the string might change slightly, but the core mes-
sage remains without forcing us to change the test.
Summary
Tests grow and change with the system under test. If we don’t pay attention to
maintainability, our tests may require so many changes from us that it might not
be worth changing them. We may instead end up deleting them, and throwing
away all the hard work that went into creating them. For tests to be useful in the
long run, they should fail only for reasons we truly care about.
A true failure is when a test fails because it finds a bug in production code. A false
failure is when a test fails for any other reason.
To estimate test maintainability, we can measure the number of false test fail-
ures and the reason for each failure, over time.
A test may falsely fail for multiple reasons: it conflicts with another test (in
which case, you should just remove it); changes in the production code’s API
(this can be mitigated by using factory and helper methods); changes in other
tests (such tests should be decoupled from each other).
Avoid testing private methods. Private methods are implementation details, and
the resulting tests are going to be fragile. Tests should verify observable behavior—
behavior that is relevant for the end user. Sometimes, the need to test a private
method is a sign of a missing abstraction, which means the method should be
made public or even be extracted into a separate class.
Keep tests DRY. Use helper methods to abstract nonessential details of arrange
and assert sections. This will simplify your tests without coupling them to each
other.
Avoid setup methods such as the beforeEach function. Once again, use helper
methods instead. Another option is to parameterize your tests and therefore
move the content of the beforeEach block to the test’s arrange section.
Avoid overspecification. Examples of overspecification are asserting the private
state of the code under test, asserting against calls on stubs, or assuming the
specific order of elements in a result collection or exact string matches when
that isn’t required.


---
**Page 184**



---
**Page 185**

Part 4
Design and process
These final chapters cover the problems you’ll face and the techniques you’ll
need when introducing unit testing to an existing organization or codebase.
 In chapter 9, we’ll talk about test readability. We’ll discuss naming conven-
tions for tests and input values for them. We’ll also cover best practices for test
structuring and writing better assertion messages.
 Chapter 10 explains how to develop a testing strategy. We’ll look at which test
levels you should prefer when testing a new feature, discuss common antipat-
terns in test levels, and talk about the test recipe strategy.
 In chapter 11, we’ll deal with the tough issue of implementing unit testing in
an organization, and we’ll cover techniques that can make your job easier. This
chapter provides answers to some tough questions that are common when first
implementing unit testing.
 In chapter 12, we’ll look at common problems associated with legacy code
and examine some tools for working with it.


---
**Page 186**



---
**Page 187**

187
Readability
Without readability, the tests you write are almost meaningless to whoever reads
them later on. Readability is the connecting thread between the person who wrote
the test and the poor soul who must read it a few months or years later. Tests are
stories you tell the next generation of programmers on a project. They allow a
developer to see exactly what an application is made of and where it started.
 This chapter is all about making sure the developers who come after you will be
able to maintain the production code and the tests that you write. They’ll need to
understand what they’re doing and where they should be doing it.
 There are several facets to readability:
Naming unit tests
Naming variables
Separating asserts from actions
Setting up and tearing down
Let’s go through these one by one.
This chapter covers
Naming conventions for unit tests
Writing readable tests


