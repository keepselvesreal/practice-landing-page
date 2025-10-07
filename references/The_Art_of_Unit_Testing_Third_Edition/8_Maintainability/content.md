Line 1: 
Line 2: --- 페이지 193 ---
Line 3: 165
Line 4: Maintainability
Line 5: Tests can enable us to develop faster, unless they make us go slower due to all the
Line 6: changes needed. If we can avoid changing existing tests when we change produc-
Line 7: tion code, we can start to hope that our tests are helping rather than hurting our
Line 8: bottom line. In this chapter, we’ll focus on the maintainability of tests.
Line 9:  Unmaintainable tests can ruin project schedules and are often set aside when
Line 10: the project is put on a more aggressive schedule. Developers will simply stop main-
Line 11: taining and fixing tests that take too long to change or that need to change often as
Line 12: the result of very minor production code changes. 
Line 13:  If maintainability is a measure of how often we are forced to change tests, we’d
Line 14: like to minimize the number of times that happens. This forces us to ask these
Line 15: questions if we ever want to get down to the root causes:
Line 16: When do we notice that a test fails and therefore might require a change?
Line 17: Why do tests fail?
Line 18: This chapter covers
Line 19: Root causes of failing tests
Line 20: Common avoidable changes to test code
Line 21: Improving the maintainability of tests that aren’t 
Line 22: currently failing
Line 23: 
Line 24: --- 페이지 194 ---
Line 25: 166
Line 26: CHAPTER 8
Line 27: Maintainability
Line 28: Which test failures force us to change the test?
Line 29: When do we choose to change a test even if we are not forced to?
Line 30: This chapter presents a series of practices related to maintainability that you can use
Line 31: when doing test reviews.
Line 32: 8.1
Line 33: Changes forced by failing tests
Line 34: A failing test is usually the first sign of potential trouble for maintainability. Of course,
Line 35: we could have found a real bug in production code, but when that’s not the case, what
Line 36: other reasons do tests have to fail? I’ll refer to genuine failures as true failures, and fail-
Line 37: ures that happen for reasons other than finding a bug in the underlying production
Line 38: code as false failures.
Line 39:  If we wanted to measure test maintainability, we could start by measuring the num-
Line 40: ber of false test failures, and the reason for each failure, over time. We already dis-
Line 41: cussed one such reason in chapter 7: when a test contains a bug. Let’s now discuss
Line 42: other possible reasons for false failures. 
Line 43: 8.1.1
Line 44: The test is not relevant or conflicts with another test
Line 45: A conflict may arise when the production code introduces a new feature that’s in
Line 46: direct conflict with one or more existing tests. Instead of the test discovering a bug, it
Line 47: may discover conflicting or new requirements. There might also be a passing test that
Line 48: targets the new expectation for how the production code should work. 
Line 49:  Either the existing failing test is no longer relevant, or the new requirement is
Line 50: wrong. Assuming that the requirement is correct, you can probably go ahead and
Line 51: delete the no-longer-relevant test.
Line 52:  Note that there’s a common exception to the “remove the test” rule: when you’re
Line 53: working with feature toggles. We’ll touch on feature toggles in chapter 10 when we dis-
Line 54: cuss testing strategies.
Line 55: 8.1.2
Line 56: Changes in the production code’s API
Line 57: A test can fail if the production code under test changes so that a function or object
Line 58: being tested now needs to be used differently, even though it may still have the same
Line 59: functionality. Such false failures fall in the bucket of “let’s avoid this as much as possible.”
Line 60:  Consider the PasswordVerifier class in listing 8.1, which requires two constructor
Line 61: parameters: 
Line 62: An array of rules (each is a function that takes an input and returns a Boolean)
Line 63: An ILogger interface
Line 64: export class PasswordVerifier {
Line 65:     ...
Line 66:     constructor(rules: ((input) => boolean)[], logger: ILogger) {
Line 67:         this._rules = rules;
Line 68: Listing 8.1
Line 69: A Password Verifier with two constructor parameters
Line 70: 
Line 71: --- 페이지 195 ---
Line 72: 167
Line 73: 8.1
Line 74: Changes forced by failing tests
Line 75:         this._logger = logger;
Line 76:     }
Line 77:     ...
Line 78: }
Line 79: We could write a couple of tests like the following.
Line 80: describe("password verifier 1", () => {
Line 81:   it("passes with zero rules", () => {
Line 82:     const verifier = new PasswordVerifier([], { info: jest.fn() });   
Line 83:     const result = verifier.verify("any input");
Line 84:     expect(result).toBe(true);
Line 85:   });
Line 86:   it("fails with single failing rule", () => {
Line 87:     const failingRule = (input) => false;
Line 88:     const verifier = 
Line 89:       new PasswordVerifier([failingRule], { info: jest.fn() });       
Line 90:     const result = verifier.verify("any input");
Line 91:     expect(result).toBe(false);
Line 92:   });
Line 93: });
Line 94: If we look at these tests from a maintainability point of view, there are several potential
Line 95: changes we will likely need to make in the future. 
Line 96: CODE USUALLY LIVES FOR A LONG TIME
Line 97: Consider that the code you’re writing will live in the codebase for at least 4–6 years
Line 98: and sometimes a decade. Over that time, what is the likelihood that the design of
Line 99: PasswordVerifier will change? Even simple things, like the constructor accepting
Line 100: more parameters, or the parameter types changing, become more likely over a longer
Line 101: timeframe. 
Line 102:  Let’s list a few changes that could happen to our Password Verifier in the future:
Line 103: We may add or remove a parameter in the constructor for PasswordVerifier.
Line 104: One of the parameters for PasswordVerifier may change to a different type.
Line 105: The number of ILogger functions or their signatures may change over time.
Line 106: The usage pattern changes so we don’t need to instantiate a new Password-
Line 107: Verifier, but just use the functions in it directly.
Line 108: If any of these things happen, how many tests would we need to change? Right now
Line 109: we’d need to change all the tests that instantiate PasswordVerifier. Could we prevent
Line 110: the need for some of these changes? 
Line 111:  Let’s pretend the future is here and our fears have come true—someone changed
Line 112: the production code’s API. Let’s say the constructor signature has changed to use
Line 113: IComplicatedLogger instead of ILogger, as follows.
Line 114: Listing 8.2
Line 115: Tests without factory functions
Line 116: Test using
Line 117: the code’s
Line 118: existing API
Line 119: 
Line 120: --- 페이지 196 ---
Line 121: 168
Line 122: CHAPTER 8
Line 123: Maintainability
Line 124: export class PasswordVerifier2 {
Line 125:   private _rules: ((input: string) => boolean)[];
Line 126:   private _logger: IComplicatedLogger;
Line 127:   constructor(rules: ((input) => boolean)[], 
Line 128:       logger: IComplicatedLogger) {
Line 129:     this._rules = rules;
Line 130:     this._logger = logger;
Line 131:   }
Line 132: ...
Line 133: }
Line 134: As it stands, we would have to change any test that directly instantiates PasswordVerifier. 
Line 135: FACTORY FUNCTIONS DECOUPLE CREATION OF OBJECT UNDER TEST
Line 136: A simple way to avoid this pain in the future is to decouple or abstract away the creation
Line 137: of the code under test so that the changes to the constructor only need to be dealt with
Line 138: in a centralized location. A function whose sole purpose is to create and preconfigure
Line 139: an instance of an object is usually called a factory function or method. A more advanced
Line 140: version of this (which we won’t cover here) is the Object Mother pattern.
Line 141:  Factory functions can help us mitigate this issue. The next two listings show how we
Line 142: could have initially written the tests before the signature change, and how we could
Line 143: easily adapt to the signature change in that case. In listing 8.4, the creation of Password-
Line 144: Verifier has been extracted into its own centralized factory function. I’ve done the
Line 145: same for the fakeLogger—it’s now also created using its own separate factory func-
Line 146: tion. If any of the changes we listed before happens in the future, we’ll only need to
Line 147: change our factory functions; the tests will usually not need to be touched. 
Line 148: describe("password verifier 1", () => {
Line 149:   const makeFakeLogger = () => {
Line 150:     return { info: jest.fn() };    
Line 151:   };
Line 152:   const makePasswordVerifier = (
Line 153:     rules: ((input) => boolean)[],
Line 154:     fakeLogger: ILogger = makeFakeLogger()) => {
Line 155:       return new PasswordVerifier(rules, fakeLogger);    
Line 156:   };
Line 157:   it("passes with zero rules", () => {
Line 158:     const verifier = makePasswordVerifier([]);  
Line 159:     const result = verifier.verify("any input");
Line 160:     expect(result).toBe(true);
Line 161:   });
Line 162: Listing 8.3
Line 163: A breaking change in a constructor
Line 164: Listing 8.4
Line 165: Refactoring to factory functions
Line 166: A centralized point for 
Line 167: creating a fakeLogger
Line 168: A centralized point 
Line 169: for creating a 
Line 170: PasswordVerifier
Line 171: Using the factory 
Line 172: function to create 
Line 173: PasswordVerifier
Line 174: 
Line 175: --- 페이지 197 ---
Line 176: 169
Line 177: 8.1
Line 178: Changes forced by failing tests
Line 179: In the following listing, I’ve refactored the tests based on the signature change. Notice
Line 180: that the change doesn’t involve changing the tests, but only the factory functions.
Line 181: That’s the type of manageable change I can live with in a real project.
Line 182: describe("password verifier (ctor change)", () => {
Line 183:   const makeFakeLogger = () => {
Line 184:     return Substitute.for<IComplicatedLogger>();
Line 185:   };
Line 186:   const makePasswordVerifier = (
Line 187:     rules: ((input) => boolean)[],
Line 188:     fakeLogger: IComplicatedLogger = makeFakeLogger()) => {
Line 189:     return new PasswordVerifier2(rules, fakeLogger);
Line 190:   };
Line 191:   // the tests remain the same
Line 192: });
Line 193: 8.1.3
Line 194: Changes in other tests
Line 195: A lack of test isolation is a huge cause of test blockage—I’ve seen this while consulting
Line 196: and working on unit tests. The basic concept you should keep in mind is that a test
Line 197: should always run in its own little world, isolated from other tests even if they verify
Line 198: the same functionality.
Line 199: When tests aren’t isolated well, they can step on each other’s toes, making you regret
Line 200: deciding to try unit testing and promising yourself never again. I’ve seen this happen.
Line 201: Developers don’t bother looking for problems in the tests, so when there’s a problem,
Line 202: Listing 8.5
Line 203: Refactoring factory methods to fit a new signature
Line 204: The test that cried “fail”
Line 205: One project I was involved in had unit tests behaving strangely, and they got even
Line 206: stranger as time went on. A test would fail and then suddenly pass for a couple of
Line 207: days straight. A day later, it would fail, seemingly randomly, and other times it would
Line 208: pass even if code was changed to remove or change its behavior. It got to the point
Line 209: where developers would tell each other, “Ah, it’s OK. If it sometimes passes, that
Line 210: means it passes.”
Line 211: Properly investigated, it turned out that the test was calling out a different (and flaky)
Line 212: test as part of its code, and when the other test failed, it would break the first test.
Line 213: It took us three days to untangle the mess, after spending a month trying various
Line 214: workarounds for the situation. When we finally had the test working correctly, we dis-
Line 215: covered that we had a bunch of real bugs in our code that we were ignoring because
Line 216: the test had its own bugs and issues. The story of the boy who cried wolf holds true
Line 217: even in development.
Line 218: 
Line 219: --- 페이지 198 ---
Line 220: 170
Line 221: CHAPTER 8
Line 222: Maintainability
Line 223: it can take a lot of time to find out what’s wrong. The easiest symptom is what I call
Line 224: “constrained test order.”
Line 225: CONSTRAINED TEST ORDER
Line 226: A constrained test order happens when a test assumes that a previous test executed first, or
Line 227: did not execute first, because it relies on some shared state that is set up or reset by the
Line 228: other test. For example, if one test changes a shared variable in memory or some exter-
Line 229: nal resource like a database, and another test depends on that variable’s value after the
Line 230: first tests’ execution, we have a dependency between the tests based on order. 
Line 231:  Couple that with the fact that most test runners don’t (and won’t, and maybe
Line 232: shouldn’t!) guarantee that tests will run in a specific order. This means that if you ran
Line 233: all your tests today, and all your tests a week later with a new version of the test runner,
Line 234: the tests might not run in the same order as before.
Line 235:  To illustrate the problem, let’s look at a simple scenario. Figure 8.1 shows a Special-
Line 236: App object that uses a UserCache object. The user cache holds a single instance (a sin-
Line 237: gleton) that is shared as a caching mechanism for the application, and, incidentally,
Line 238: also for the tests. Listing 8.6 shows the implementation of SpecialApp, the user cache,
Line 239: and the IUserDetails interface.
Line 240: export interface IUserDetails {
Line 241:   key: string;
Line 242:   password: string;
Line 243: }
Line 244: export interface IUserCache {
Line 245:   addUser(user: IUserDetails): void;
Line 246:   getUser(key: string);
Line 247:   reset(): void;
Line 248: }
Line 249: Listing 8.6
Line 250: A shared user cache and associated interfaces
Line 251: loginUser(user)
Line 252: UserCache
Line 253: Shared instance
Line 254: SpecialApp
Line 255: Test
Line 256: getUser()
Line 257: addUser()
Line 258: Figure 8.1
Line 259: A shared 
Line 260: UserCache instance
Line 261: 
Line 262: --- 페이지 199 ---
Line 263: 171
Line 264: 8.1
Line 265: Changes forced by failing tests
Line 266: export class UserCache implements IUserCache {
Line 267:   users: object = {};
Line 268:   addUser(user: IUserDetails): void {
Line 269:     if (this.users[user.key] !== undefined) {
Line 270:       throw new Error("user already exists");
Line 271:     }
Line 272:     this.users[user.key] = user;
Line 273:   }
Line 274:   getUser(key: string) {
Line 275:     return this.users[key];
Line 276:   }
Line 277:   reset(): void {
Line 278:     this.users = {};
Line 279:   }
Line 280: }
Line 281: let _cache: IUserCache;
Line 282: export function getUserCache() {
Line 283:   if (_cache === undefined) {
Line 284:     _cache = new UserCache();
Line 285:   }
Line 286:   return _cache;
Line 287: } 
Line 288: The following listing shows the SpecialApp implementation.
Line 289: export class SpecialApp {
Line 290:   loginUser(key: string, pass: string): boolean {
Line 291:     const cache: IUserCache = getUserCache();
Line 292:     const foundUser: IUserDetails = cache.getUser(key);
Line 293:     if (foundUser?.password === pass) {
Line 294:       return true;
Line 295:     }
Line 296:     return false;
Line 297:   }
Line 298: }
Line 299: This is a simplistic implementation for this example, so don’t worry about SpecialApp
Line 300: too much. Let’s look at the tests.
Line 301: describe("Test Dependence", () => {
Line 302:   describe("loginUser with loggedInUser", () => {
Line 303:     test("no user, login fails", () => {
Line 304:       const app = new SpecialApp();
Line 305:       const result = app.loginUser("a", "abc");   
Line 306:       expect(result).toBe(false);                 
Line 307:     });
Line 308: Listing 8.7
Line 309: The SpecialApp implementation
Line 310: Listing 8.8
Line 311: Tests that need to run in a specific order
Line 312: Requires the user 
Line 313: cache to be empty
Line 314: 
Line 315: --- 페이지 200 ---
Line 316: 172
Line 317: CHAPTER 8
Line 318: Maintainability
Line 319:     test("can only cache each user once", () => {
Line 320:       getUserCache().addUser({   
Line 321:         key: "a",
Line 322:         password: "abc",
Line 323:       });
Line 324:       expect(() =>
Line 325:         getUserCache().addUser({
Line 326:           key: "a",
Line 327:           password: "abc",
Line 328:         })
Line 329:       ).toThrowError("already exists");
Line 330:     });
Line 331:     test("user exists, login succeeds", () => {
Line 332:       const app = new SpecialApp();
Line 333:       const result = app.loginUser("a", "abc");    
Line 334:       expect(result).toBe(true);                   
Line 335:     });
Line 336:   });
Line 337: });
Line 338: Notice that the first and third tests both rely on the second test. The first test requires
Line 339: that the second test has not executed yet, because it needs the user cache to be empty.
Line 340: On the other hand, the third test relies on the second test to fill up the cache with the
Line 341: expected user. If we run only the third test using Jest’s test.only keyword, the test
Line 342: would fail:
Line 343: test.only("user exists, login succeeds", () => {
Line 344:    const app = new SpecialApp();
Line 345:    const result = app.loginUser("a", "abc");
Line 346:    expect(result).toBe(true); 
Line 347:  });
Line 348: This antipattern usually happens when we try to reuse parts of tests without extracting
Line 349: helper functions. We end up expecting a different test to run first, saving us from
Line 350: doing some of the setup. This works, until it doesn’t.
Line 351:  We can refactor this in a few steps:
Line 352: Extract a helper function for adding a user.
Line 353: Reuse this function for multiple tests.
Line 354: Reset the user cache between tests.
Line 355: The following listing shows how we could refactor the tests to avoid this problem.
Line 356: const addDefaultUser = () =>   
Line 357:   getUserCache().addUser({
Line 358:     key: "a",
Line 359:     password: "abc",
Line 360:   });
Line 361: const makeSpecialApp = () => new SpecialApp();    
Line 362: Listing 8.9
Line 363: Refactoring tests to remove order dependence
Line 364: Adds a user 
Line 365: to the cache
Line 366: Requires the cache 
Line 367: to contain the user
Line 368: Extracted user-
Line 369: creation helper 
Line 370: function
Line 371: Extracted factory 
Line 372: function
Line 373: 
Line 374: --- 페이지 201 ---
Line 375: 173
Line 376: 8.2
Line 377: Refactoring to increase maintainability
Line 378: describe("Test Dependence v2", () => {
Line 379:   beforeEach(() => getUserCache().reset());      
Line 380:   describe("user cache", () => {                   
Line 381:     test("can only add cache use once", () => {
Line 382:       addDefaultUser();    
Line 383:       expect(() => addDefaultUser())
Line 384:         .toThrowError("already exists");
Line 385:     });
Line 386:   });
Line 387:   describe("loginUser with loggedInUser", () => {  
Line 388:     test("user exists, login succeeds", () => {
Line 389:       addDefaultUser();    
Line 390:       const app = makeSpecialApp();
Line 391:       const result = app.loginUser("a", "abc");
Line 392:       expect(result).toBe(true);
Line 393:     });
Line 394:     test("user missing, login fails", () => {
Line 395:       const app = makeSpecialApp();
Line 396:       const result = app.loginUser("a", "abc");
Line 397:       expect(result).toBe(false);
Line 398:     });
Line 399:   });
Line 400: });
Line 401: There are several things going on here. First, we extracted two helper functions: a
Line 402: makeSpecialApp factory function and an addDefaultUser helper function that we can
Line 403: reuse. Next, we created a very important beforeEach function that resets the user
Line 404: cache before each test. Whenever I have a shared resource like that, I almost always
Line 405: have a beforeEach or afterEach function that resets it to its original condition before
Line 406: or after the test runs.
Line 407:  The first and the third tests now run in their own little nested describe structure.
Line 408: They also both use the makeSpecialApp factory function, and one of them is using
Line 409: addDefaultUser to make sure it does not require any other test to run first. The sec-
Line 410: ond test also runs in its own nested describe function and reuses the addDefaultUser
Line 411: function.
Line 412: 8.2
Line 413: Refactoring to increase maintainability
Line 414: Up until now, I’ve discussed test failures that force us to make changes. Let’s now dis-
Line 415: cuss changes that we choose to make, to make tests easier to maintain over time.
Line 416: 8.2.1
Line 417: Avoid testing private or protected methods
Line 418: This section applies more to object-oriented languages as well as TypeScript. Private
Line 419: or protected methods are usually private for a good reason in the developer’s mind.
Line 420: Sometimes it’s to hide implementation details, so that the implementation can
Line 421: Resets user cache 
Line 422: between tests
Line 423: New nested 
Line 424: describe 
Line 425: functions
Line 426: Calls
Line 427: reusable
Line 428: helper
Line 429: functions
Line 430: 
Line 431: --- 페이지 202 ---
Line 432: 174
Line 433: CHAPTER 8
Line 434: Maintainability
Line 435: change later without changing the observable behavior. It could also be for security-
Line 436: related or IP-related reasons (obfuscation, for example).
Line 437:  When you test a private method, you’re testing against a contract internal to the
Line 438: system. Internal contracts are dynamic, and they can change when you refactor the
Line 439: system. When they change, your test could fail because some internal work is being
Line 440: done differently, even though the overall functionality of the system remains the
Line 441: same. For testing purposes, the public contract (the observable behavior) is all you
Line 442: need to care about. Testing the functionality of private methods may lead to breaking
Line 443: tests, even though the observable behavior is correct. 
Line 444:  Think of it this way: no private method exists in a vacuum. Somewhere down the
Line 445: line, something has to call it, or it will never get triggered. Usually there’s a public
Line 446: method that ends up invoking this private one, and if not, there’s always a public
Line 447: method up the chain of calls that gets invoked. This means that any private method is
Line 448: always part of a bigger unit of work, or use case in the system, that starts out with a
Line 449: public API and ends with one of the three end results: return value, state change, or
Line 450: third-party call (or all three).
Line 451:  So if you see a private method, find the public use case in the system that will exer-
Line 452: cise it. If you test only the private method and it works, that doesn’t mean that the rest
Line 453: of the system is using this private method correctly or handles the results it provides
Line 454: correctly. You might have a system that works perfectly on the inside, but all that nice
Line 455: inside stuff is used incorrectly from the public APIs.
Line 456:  Sometimes, if a private method is worth testing, it might be worth making it public,
Line 457: static, or at least internal, and defining a public contract against any code that uses it.
Line 458: In some cases, the design may be cleaner if you put the method in a different class
Line 459: altogether. We’ll look at those approaches in a moment.
Line 460:  Does this mean there should eventually be no private methods in the codebase?
Line 461: No. With test-driven design, you usually write tests against methods that are public,
Line 462: and those public methods are later refactored into calling smaller, private methods.
Line 463: All the while, the tests against the public methods continue to pass.
Line 464: MAKING METHODS PUBLIC
Line 465: Making a method public isn’t necessarily a bad thing. In a more functional world, it’s
Line 466: not even an issue. This practice may seem to go against the object-oriented principles
Line 467: many of us were raised on, but that’s not always the case. 
Line 468:  Consider that wanting to test a method could mean that the method has a known
Line 469: behavior or contract against the calling code. By making it public, you’re making this
Line 470: official. By keeping the method private, you tell all the developers who come after you
Line 471: that they can change the implementation of the method without worrying about
Line 472: unknown code that uses it.
Line 473: EXTRACTING METHODS TO NEW CLASSES OR MODULES
Line 474: If your method contains a lot of logic that can stand on its own, or it uses specialized
Line 475: state variables in the class or module that are relevant only to the method in question,
Line 476: it may be a good idea to extract the method into a new class or its own module with a
Line 477: 
Line 478: --- 페이지 203 ---
Line 479: 175
Line 480: 8.2
Line 481: Refactoring to increase maintainability
Line 482: specific role in the system. You can then test that class separately. Michael Feathers’
Line 483: Working Effectively with Legacy Code (Pearson, 2004) has some good examples of this
Line 484: technique, and Clean Code by Robert Martin (Pearson, 2008) can help you figure out
Line 485: when this is a good idea.
Line 486: MAKING STATELESS PRIVATE METHODS PUBLIC AND STATIC
Line 487: If your method is completely stateless, some people choose to refactor the method by
Line 488: making it static (in languages that support this feature). That makes it much more
Line 489: testable but also states that the method is a sort of utility method that has a known
Line 490: public contract specified by its name.
Line 491: 8.2.2
Line 492: Keep tests DRY
Line 493: Duplication in your unit tests can hurt you, as a developer, just as much as, if not more
Line 494: than, duplication in production code. That’s because any change in a piece of code
Line 495: that has duplicates will force you to change all the duplicates as well. When you’re
Line 496: dealing with tests, there’s more risk of the developer just avoiding this trouble and
Line 497: deleting or ignoring tests instead of fixing them.
Line 498:  The DRY (don’t repeat yourself) principle should be in effect in test code just as in
Line 499: production code. Duplicated code means there’s more code to change when one
Line 500: aspect you test against changes. Changing a constructor or changing the semantics of
Line 501: using a class can have a major effect on tests that have a lot of duplicated code.
Line 502:  As we’ve seen in previous examples in this chapter, using helper functions can help
Line 503: to reduce duplication in tests. 
Line 504: WARNING
Line 505: Removing duplication can also go too far and hurt readability.
Line 506: We’ll talk about that in the next chapter, on readability.
Line 507: 8.2.3
Line 508: Avoid setup methods
Line 509: I’m not a fan of the beforeEach function (also called a setup function) that happens
Line 510: once before each test and is often used to remove duplication. I much prefer using
Line 511: helper functions. Setup functions are too easy to abuse. Developers tend to use them
Line 512: for things they weren’t meant for, and tests become less readable and less maintain-
Line 513: able as a result. 
Line 514:  Many developers abuse setup methods in several ways:
Line 515: Initializing objects in the setup method that are used in only some tests in the file
Line 516: Having setup code that’s lengthy and hard to understand
Line 517: Setting up mocks and fake objects within the setup method
Line 518: Also, setup methods have limitations, which you can get around by using simple
Line 519: helper methods:
Line 520: Setup methods can only help when you need to initialize things.
Line 521: Setup methods aren’t always the best candidates for duplication removal.
Line 522: Removing duplication isn’t always about creating and initializing new instances
Line 523: 
Line 524: --- 페이지 204 ---
Line 525: 176
Line 526: CHAPTER 8
Line 527: Maintainability
Line 528: of objects. Sometimes it’s about removing duplication in assertion logic or call-
Line 529: ing out code in a specific way.
Line 530: Setup methods can’t have parameters or return values.
Line 531: Setup methods can’t be used as factory methods that return values. They’re run
Line 532: before the test executes, so they must be more generic in the way they work.
Line 533: Tests sometimes need to request specific things or call shared code with a
Line 534: parameter for the specific test (for example, retrieving an object and setting its
Line 535: property to a specific value).
Line 536: Setup methods should only contain code that applies to all the tests in the cur-
Line 537: rent test class, or the method will be harder to read and understand.
Line 538: I’ve almost entirely stopped using setup methods for the tests I write. Test code should
Line 539: be nice and clean, just like production code, but if your production code looks horri-
Line 540: ble, please don’t use that as a crutch to write unreadable tests. Use factory and helper
Line 541: methods, and make the world a better place for the generation of developers that will
Line 542: have to maintain your code in 5 or 10 years.
Line 543: NOTE
Line 544: We looked at an example of moving from using beforeEach to helper
Line 545: functions in section 8.2.3 (listing 8.9) and also in chapter 2.
Line 546: 8.2.4
Line 547: Use parameterized tests to remove duplication
Line 548: Another great option for replacing setup methods, if all your tests look the same, is
Line 549: to use parameterized tests. Different test frameworks in different languages support
Line 550: parameterized tests—if you’re using Jest, you can use the built-in test.each or it.each
Line 551: functions. 
Line 552:  Parameterization helps move the setup logic that would otherwise remain dupli-
Line 553: cated or would reside in the beforeEach block to the test’s arrange section. It also
Line 554: helps avoid duplication of the assertion logic, as shown in the following listing.
Line 555: const sum = numbers => {
Line 556:     if (numbers.length > 0) {
Line 557:         return parseInt(numbers);
Line 558:     }
Line 559:     return 0;
Line 560: };
Line 561: describe('sum with regular tests', () => {
Line 562:     test('sum number 1', () => {
Line 563:         const result = sum('1');    
Line 564:         expect(result).toBe(1);     
Line 565:     });
Line 566:     test('sum number 2', () => {
Line 567:         const result = sum('2');    
Line 568:         expect(result).toBe(2);     
Line 569:     });
Line 570: });
Line 571: Listing 8.10
Line 572: Parameterized tests with Jest
Line 573: Duplicated setup 
Line 574: and assertion logic
Line 575: 
Line 576: --- 페이지 205 ---
Line 577: 177
Line 578: 8.3
Line 579: Avoid overspecification
Line 580: describe('sum with parameterized tests', () => {
Line 581:     test.each([
Line 582:         ['1', 1],   
Line 583:         ['2', 2]    
Line 584:     ])('add ,for %s, returns that number', (input, expected) => {
Line 585:             const result = sum(input);       
Line 586:             expect(result).toBe(expected);   
Line 587:         }
Line 588:     )
Line 589: });
Line 590: In the first describe block, we have two tests that repeat each other with different input
Line 591: values and expected outputs. In the second describe block, we’re using test.each
Line 592: to provide an array of arrays, where each subarray lists all the values needed for the
Line 593: test function.
Line 594:  Parameterized tests can help reduce a lot of duplication between tests, but we
Line 595: should be careful to only use this technique in cases where we repeat the exact same
Line 596: scenario and only change the input and output. 
Line 597: 8.3
Line 598: Avoid overspecification
Line 599: An overspecified test is one that contains assumptions about how a specific unit under
Line 600: test (production code) should implement its internal behavior, instead of only check-
Line 601: ing that the observable behavior (exit points) is correct. 
Line 602:  Here are ways unit tests are often overspecified:
Line 603: A test asserts purely internal state in an object under test.
Line 604: A test uses multiple mocks.
Line 605: A test uses stubs as mocks.
Line 606: A test assumes a specific order or exact string matches when that isn’t required.
Line 607: Let’s look at some examples of overspecified tests.
Line 608: 8.3.1
Line 609: Internal behavior overspecification with mocks
Line 610: A very common antipattern is to verify that an internal function in a class or module is
Line 611: called, instead of checking the exit point of the unit of work. Here’s a password veri-
Line 612: fier that calls an internal function, which the test shouldn’t care about.
Line 613: export class PasswordVerifier4 {
Line 614:   private _rules: ((input: string) => boolean)[];
Line 615:   private _logger: IComplicatedLogger;
Line 616:   constructor(rules: ((input) => boolean)[],
Line 617:       logger: IComplicatedLogger) {
Line 618:     this._rules = rules;
Line 619:     this._logger = logger;
Line 620:   }
Line 621: Listing 8.11
Line 622: Production code that calls a protected function
Line 623: Test data used
Line 624: for setup and
Line 625: assertion
Line 626: Setup and 
Line 627: assertion without 
Line 628: duplication
Line 629: 
Line 630: --- 페이지 206 ---
Line 631: 178
Line 632: CHAPTER 8
Line 633: Maintainability
Line 634:   verify(input: string): boolean {
Line 635:     const failed = this.findFailedRules(input);   
Line 636:     if (failed.length === 0) {
Line 637:       this._logger.info("PASSED");
Line 638:       return true;
Line 639:     }
Line 640:     this._logger.info("FAIL");
Line 641:     return false;
Line 642:   }
Line 643:   protected findFailedRules(input: string) {  
Line 644:     const failed = this._rules
Line 645:       .map((rule) => rule(input))
Line 646:       .filter((result) => result === false);
Line 647:     return failed;
Line 648:   }
Line 649: }
Line 650: Notice that we’re calling the protected findFailedRules function to get a result from
Line 651: it, and then doing a calculation on the result. 
Line 652:  Here’s our test.
Line 653: describe("verifier 4", () => {
Line 654:   describe("overspecify protected function call", () => {
Line 655:     test("checkfailedFules is called", () => {
Line 656:       const pv4 = new PasswordVerifier4(
Line 657:         [], Substitute.for<IComplicatedLogger>()
Line 658:       ); 
Line 659:       const failedMock = jest.fn(() => []);    
Line 660:       pv4["findFailedRules"] = failedMock;     
Line 661:       pv4.verify("abc");
Line 662:       expect(failedMock).toHaveBeenCalled();    
Line 663:     });
Line 664:   });
Line 665: });
Line 666: The antipattern here is that we’re proving something that isn’t an exit point. We’re
Line 667: checking that the code calls some internal function, but what does that really prove?
Line 668: We’re not checking that the calculation was correct on the result; we’re simply testing
Line 669: for the sake of testing. 
Line 670:  If the function is returning a value, usually that’s a strong indication that we
Line 671: shouldn’t mock that function because the function call itself does not represent the
Line 672: exit point. The exit point is the value returned from the verify() function. We
Line 673: shouldn’t care whether the internal function even exists. 
Line 674:  By verifying against a mock of a protected function that is not an exit point, we are
Line 675: coupling our test implementation to the internal implementation of the code under
Line 676: Listing 8.12
Line 677: An overspecified test verifying a call to a protected function
Line 678: Call to the 
Line 679: internal 
Line 680: function
Line 681: Internal 
Line 682: function
Line 683: Mocking the 
Line 684: internal function
Line 685: Verifying the 
Line 686: internal function 
Line 687: call. Don’t do this.
Line 688: 
Line 689: --- 페이지 207 ---
Line 690: 179
Line 691: 8.3
Line 692: Avoid overspecification
Line 693: test, for no real benefit. When the internal calls change (and they will) we will also
Line 694: have to change all the tests associated with these calls, and that will not be a positive
Line 695: experience. You can read more about mocks and their relation to test fragility in
Line 696: chapter 5 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov (Man-
Line 697: ning, 2020).
Line 698: WHAT SHOULD WE DO INSTEAD?
Line 699: Look for the exit point. The real exit point depends on the type of test we wish to
Line 700: perform:
Line 701: Value-based test—For a value-based test, which I would highly recommend you
Line 702: lean toward when possible, we look for a return value from the called function.
Line 703: In this case, the verify function returns a value, so it’s the perfect candidate for
Line 704: a value-based test: pv4.verify("abc").
Line 705: State-based test—For a state-based test, we look for a sibling function (a function
Line 706: that exists at the same level of scope as the entry point) or a sibling property
Line 707: that is affected by calling the verify() function. For example, firstname()
Line 708: and lastname() could be considered sibling functions. That is where we should
Line 709: be asserting. In this codebase, nothing is affected by calling verify() that is vis-
Line 710: ible at the same level, so it is not a good candidate for state-based testing.
Line 711: Third-party test—For a third-party test, we would have to use a mock, and that
Line 712: would require us to find out where the fire-and-forget location is inside the
Line 713: code. The findFailedRules function isn’t that, because it is actually delivering
Line 714: information back to our verify() function. In this case, there’s no real third-
Line 715: party dependency that we have to take over.
Line 716: 8.3.2
Line 717: Exact outputs and ordering overspecification
Line 718: A common antipattern is when a test overspecifies the order and the structure of a col-
Line 719: lection of returned values. It’s often easier to specify the whole collection, along with
Line 720: each of its items, in the assertion, but with this approach, we implicitly take on the
Line 721: burden of fixing the test when any little detail of the collection changes. Instead of
Line 722: using a single huge assertion, we should separate different aspects of the verification
Line 723: into smaller, explicit asserts.
Line 724:  The following listing shows a verify() function that takes on multiple inputs and
Line 725: returns a list of result objects.
Line 726: interface IResult {
Line 727:   result: boolean;
Line 728:   input: string;
Line 729: }
Line 730: export class PasswordVerifier5 {
Line 731:   private _rules: ((input: string) => boolean)[];
Line 732: Listing 8.13
Line 733: A verifier that returns a list of outputs
Line 734: 
Line 735: --- 페이지 208 ---
Line 736: 180
Line 737: CHAPTER 8
Line 738: Maintainability
Line 739:   constructor(rules: ((input) => boolean)[]) {
Line 740:     this._rules = rules;
Line 741:   }
Line 742:   verify(inputs: string[]): IResult[] {
Line 743:     const failedResults = 
Line 744:       inputs.map((input) => this.checkSingleInput(input));
Line 745:     return failedResults;
Line 746:   }
Line 747:   private checkSingleInput(input: string): IResult {
Line 748:     const failed = this.findFailedRules(input);
Line 749:     return {
Line 750:       input,
Line 751:       result: failed.length === 0,
Line 752:     };
Line 753:   }
Line 754: This verify() function returns an array of IResult objects with an input and result
Line 755: in each. The following listing shows a test that makes an implicit check on both the
Line 756: ordering of the results and the structure of each result, as well as checking the value of
Line 757: the results.
Line 758: test("overspecify order and schema", () => {
Line 759:   const pv5 = 
Line 760:     new PasswordVerifier5([input => input.includes("abc")]);
Line 761:   const results = pv5.verify(["a", "ab", "abc", "abcd"]);
Line 762:   expect(results).toEqual([           
Line 763:     { input: "a", result: false },    
Line 764:     { input: "ab", result: false },   
Line 765:     { input: "abc", result: true },   
Line 766:     { input: "abcd", result: true },  
Line 767:   ]);
Line 768: });
Line 769: How might this test change in the future? Here are quite a few reasons for it to change:
Line 770: When the length of the results array changes
Line 771: When each result object gains or removes a property (even if the test doesn’t
Line 772: care about those properties)
Line 773: When the order of the results changes (even if it might not be important for
Line 774: the current test)
Line 775: If any of these changes happens in the future, but your test is just focused on checking
Line 776: the logic of the verifier and the structure of its output, there’s going to be a lot of pain
Line 777: involved in maintaining this test.
Line 778:  We can reduce some of that pain by verifying only the parts that matter to us.
Line 779: Listing 8.14
Line 780: Overspecifying order and schema of the result 
Line 781: A single 
Line 782: huge assert
Line 783: 
Line 784: --- 페이지 209 ---
Line 785: 181
Line 786: 8.3
Line 787: Avoid overspecification
Line 788: test("overspecify order but ignore schema", () => {
Line 789:   const pv5 = 
Line 790:     new PasswordVerifier5([(input) => input.includes("abc")]);
Line 791:   const results = pv5.verify(["a", "ab", "abc", "abcd"]);
Line 792:   expect(results.length).toBe(4);
Line 793:   expect(results[0].result).toBe(false);
Line 794:   expect(results[1].result).toBe(false);
Line 795:   expect(results[2].result).toBe(true);
Line 796:   expect(results[3].result).toBe(true);
Line 797: });
Line 798: Instead of providing the full expected output, we can simply assert on the values of
Line 799: specific properties in the output. However, we’re still stuck if the order of the results
Line 800: changes. If we don’t care about the order, we can simply check if the output contains a
Line 801: specific result, as follows.
Line 802: test("ignore order and schema", () => {
Line 803:   const pv5 = 
Line 804:     new PasswordVerifier5([(input) => input.includes("abc")]);
Line 805:   const results = pv5.verify(["a", "ab", "abc", "abcd"]);
Line 806:   expect(results.length).toBe(4);
Line 807:   expect(findResultFor("a")).toBe(false);
Line 808:   expect(findResultFor("ab")).toBe(false);
Line 809:   expect(findResultFor("abc")).toBe(true);
Line 810:   expect(findResultFor("abcd")).toBe(true);
Line 811: });
Line 812: Here we are using findResultFor() to find the specific result for a given input. Now
Line 813: the order of the results can change, or extra values can be added, but our test will only
Line 814: fail if the calculation of the true or false results changes. 
Line 815:  Another common antipattern people tend to repeat is to assert against hardcoded
Line 816: strings in the unit’s return value or properties, when only a specific part of a string is
Line 817: necessary. Ask yourself, “Can I check if a string contains something rather than equals
Line 818: something?” Here’s a password verifier that gives us a message describing how many
Line 819: rules were broken during a verification.
Line 820: export class PasswordVerifier6 {
Line 821:   private _rules: ((input: string) => boolean)[];
Line 822:   private _msg: string = "";
Line 823: Listing 8.15
Line 824: Ignoring the schema of the results
Line 825: Listing 8.16
Line 826: Ignoring order and schema
Line 827: Listing 8.17
Line 828: A verifier that returns a string message
Line 829: 
Line 830: --- 페이지 210 ---
Line 831: 182
Line 832: CHAPTER 8
Line 833: Maintainability
Line 834:   constructor(rules: ((input) => boolean)[]) {
Line 835:     this._rules = rules;
Line 836:   }
Line 837:   getMsg(): string {
Line 838:     return this._msg;
Line 839:   }
Line 840:   verify(inputs: string[]): IResult[] {
Line 841:     const allResults = 
Line 842:       inputs.map((input) => this.checkSingleInput(input));
Line 843:     this.setDescription(allResults);
Line 844:     return allResults;
Line 845:   }
Line 846:   private setDescription(results: IResult[]) {
Line 847:     const failed = results.filter((res) => !res.result);
Line 848:     this._msg = `you have ${failed.length} failed rules.`;
Line 849:   }
Line 850: The following listing shows two tests that use getMsg(). 
Line 851: describe("verifier 6", () => {
Line 852:   test("over specify string", () => {
Line 853:     const pv5 = 
Line 854:       new PasswordVerifier6([(input) => input.includes("abc")]);
Line 855:     pv5.verify(["a", "ab", "abc", "abcd"]);
Line 856:     const msg = pv5.getMsg();
Line 857:     expect(msg).toBe("you have 2 failed rules.");   
Line 858:   });
Line 859:   //Here's a better way to write this test
Line 860:   test("more future proof string checking", () => {
Line 861:     const pv5 = 
Line 862:       new PasswordVerifier6([(input) => input.includes("abc")]);
Line 863:     pv5.verify(["a", "ab", "abc", "abcd"]);
Line 864:     const msg = pv5.getMsg();
Line 865:     expect(msg).toMatch(/2 failed/);    
Line 866:   });
Line 867: });
Line 868: The first test checks that the string exactly equals another string. This backfires often,
Line 869: because strings are a form of user interface. We tend to change them slightly and
Line 870: embellish them over time. For example, do we care that there is a period at the end of
Line 871: the string? Our test requires us to care, but the meat of the assert is the correct num-
Line 872: ber being shown (especially since strings change in different computer languages or
Line 873: cultures, but numbers usually stay the same).
Line 874: Listing 8.18
Line 875: Overspecifying a string using equality
Line 876: Overly specific 
Line 877: string expectation
Line 878: A better way to assert 
Line 879: against a string
Line 880: 
Line 881: --- 페이지 211 ---
Line 882: 183
Line 883: Summary
Line 884:  The second test simply looks for the “2 failed” string inside the message. This
Line 885: makes the test more future-proof: the string might change slightly, but the core mes-
Line 886: sage remains without forcing us to change the test.
Line 887: Summary
Line 888: Tests grow and change with the system under test. If we don’t pay attention to
Line 889: maintainability, our tests may require so many changes from us that it might not
Line 890: be worth changing them. We may instead end up deleting them, and throwing
Line 891: away all the hard work that went into creating them. For tests to be useful in the
Line 892: long run, they should fail only for reasons we truly care about.
Line 893: A true failure is when a test fails because it finds a bug in production code. A false
Line 894: failure is when a test fails for any other reason.
Line 895: To estimate test maintainability, we can measure the number of false test fail-
Line 896: ures and the reason for each failure, over time.
Line 897: A test may falsely fail for multiple reasons: it conflicts with another test (in
Line 898: which case, you should just remove it); changes in the production code’s API
Line 899: (this can be mitigated by using factory and helper methods); changes in other
Line 900: tests (such tests should be decoupled from each other).
Line 901: Avoid testing private methods. Private methods are implementation details, and
Line 902: the resulting tests are going to be fragile. Tests should verify observable behavior—
Line 903: behavior that is relevant for the end user. Sometimes, the need to test a private
Line 904: method is a sign of a missing abstraction, which means the method should be
Line 905: made public or even be extracted into a separate class.
Line 906: Keep tests DRY. Use helper methods to abstract nonessential details of arrange
Line 907: and assert sections. This will simplify your tests without coupling them to each
Line 908: other.
Line 909: Avoid setup methods such as the beforeEach function. Once again, use helper
Line 910: methods instead. Another option is to parameterize your tests and therefore
Line 911: move the content of the beforeEach block to the test’s arrange section.
Line 912: Avoid overspecification. Examples of overspecification are asserting the private
Line 913: state of the code under test, asserting against calls on stubs, or assuming the
Line 914: specific order of elements in a result collection or exact string matches when
Line 915: that isn’t required.
Line 916: 
Line 917: --- 페이지 212 ---
