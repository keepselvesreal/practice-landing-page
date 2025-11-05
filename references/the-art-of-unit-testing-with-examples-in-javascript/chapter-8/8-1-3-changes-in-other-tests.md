# 8.1.3 Changes in other tests (pp.169-173)

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


