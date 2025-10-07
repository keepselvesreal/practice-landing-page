Line 1: 
Line 2: --- 페이지 132 ---
Line 3: 104
Line 4: Isolation frameworks
Line 5: In the previous chapters, we looked at writing mocks and stubs manually and saw
Line 6: the challenges involved, especially when the interface we’d like to fake requires us
Line 7: to create long, error prone, repetitive code. We kept having to declare custom vari-
Line 8: ables, create custom functions, or inherit from classes that use those variables and
Line 9: basically make things a bit more complicated than they need to be (most of the
Line 10: time).
Line 11:  In this chapter, we’ll look at some elegant solutions to these problems in the
Line 12: form of an isolation framework—a reusable library that can create and configure fake
Line 13: objects at run time. These objects are referred to as dynamic stubs and dynamic mocks.
Line 14:  I call them isolation frameworks because they allow you to isolate the unit of
Line 15: work from its dependencies. You’ll find that many resources will refer to them as
Line 16: “mocking frameworks,” but I try to avoid that because they can be used for both
Line 17: This chapter covers
Line 18: Defining isolation frameworks and how they help
Line 19: Two main flavors of frameworks
Line 20: Faking modules with Jest
Line 21: Faking functions with Jest 
Line 22: Object-oriented fakes with substitute.js
Line 23: 
Line 24: --- 페이지 133 ---
Line 25: 105
Line 26: 5.1
Line 27: Defining isolation frameworks
Line 28: mocks and stubs. In this chapter, we’ll take a look at a few of the JavaScript frameworks
Line 29: available and how we can use them in modular, functional, and object-oriented
Line 30: designs. You’ll see how you can use such frameworks to test various things and to cre-
Line 31: ate stubs, mocks, and other interesting things.
Line 32:  But the specific frameworks I’ll present here aren’t the point. While using them,
Line 33: you’ll see the values that their APIs promote in your tests (readability, maintainability,
Line 34: robust and long-lasting tests, and more), and you’ll find out what makes an isolation
Line 35: framework good and, alternatively, what can make it a drawback for your tests.
Line 36: 5.1
Line 37: Defining isolation frameworks
Line 38: I’ll start with a basic definition that may sound a bit bland, but it needs to be generic
Line 39: in order to include the various isolation frameworks out there: 
Line 40: An isolation framework is a set of programmable APIs that allow the dynamic creation,
Line 41: configuration, and verification of mocks and stubs, either in object or function form.
Line 42: When using an isolation framework, these tasks are often simpler, quicker, and produce
Line 43: shorter code than hand-coded mocks and stubs.
Line 44: Isolation frameworks, when used properly, can save developers from the need to write
Line 45: repetitive code to assert or simulate object interactions, and if applied in the right
Line 46: places, they can help make tests last many years without requiring a developer to come
Line 47: back and fix them after every little production code change. If they’re applied badly,
Line 48: they can cause confusion and full-on abuse of these frameworks, to the point where
Line 49: we either can’t read or can’t trust our own tests, so be wary. I’ll discuss some dos and
Line 50: don’ts in part 3 of this book.
Line 51: 5.1.1
Line 52: Choosing a flavor: Loose vs. typed 
Line 53: Because JavaScript supports multiple paradigms of programming design, we can split
Line 54: the frameworks in our world into two main flavors:
Line 55: Loose JavaScript isolation frameworks—These are vanilla JavaScript-friendly loose-
Line 56: typed isolation frameworks (such as Jest and Sinon). These frameworks usually
Line 57: also lend themselves better to more functional styles of code because they
Line 58: require less ceremony and boilerplate code to do their work.
Line 59: Typed JavaScript isolation frameworks—These are more object-oriented and Type-
Line 60: Script-friendly isolation frameworks (such as substitute.js). They’re very useful
Line 61: when dealing with whole classes and interfaces.
Line 62: Which flavor you end up choosing to use in your project will depend on a few things,
Line 63: like taste, style, and readability, but the main question to start with is, what type of
Line 64: dependencies will you mostly need to fake?
Line 65: Module dependencies (imports, requires)—Jest and other loosely typed frameworks
Line 66: should work well.
Line 67: Functional (single and higher-order functions, simple parameters and values)—Jest and
Line 68: other loosely typed frameworks should work well.
Line 69: 
Line 70: --- 페이지 134 ---
Line 71: 106
Line 72: CHAPTER 5
Line 73: Isolation frameworks
Line 74: Full objects, object hierarchies, and interfaces—Look into the more object-oriented
Line 75: frameworks, such as substitute.js.
Line 76: Let’s go back to our Password Verifier and see how we can fake the same types of
Line 77: dependencies we did in previous chapters, but this time using a framework.
Line 78: 5.2
Line 79: Faking modules dynamically
Line 80: For people who are trying to test code with direct dependencies on modules using
Line 81: require or import, isolation frameworks such as Jest or Sinon present the powerful
Line 82: ability to fake an entire module dynamically, with very little code. Since we started with
Line 83: Jest as our test framework, we’ll stick with it for the examples in this chapter.
Line 84:  Figure 5.1 illustrates a Password Verifier with two dependencies:
Line 85: A configuration service that helps decide what the logging level is (INFO or ERROR)
Line 86: A logging service that we call as the exit point of our unit of work, whenever we
Line 87: verify a password
Line 88: The arrows represent the flow of behavior through the unit of work. Another way to
Line 89: think about the arrows is through the terms command and query. We are querying the
Line 90: configuration service (to get the log level), but we are sending commands to the log-
Line 91: ger (to log).
Line 92: The following listing shows a Password Verifier that has a hard dependency on a log-
Line 93: ger module.
Line 94:  
Line 95: Command/query separation
Line 96: There is a school of design that falls under the ideas of command/query separation. If
Line 97: you’d like to learn more about these terms, I highly recommend reading Martin Fowler’s
Line 98: 2005 article on the topic, at https://martinfowler.com/bliki/CommandQuerySeparation
Line 99: .html. This pattern is very beneficial as you navigate your way around different design
Line 100: ideas, but we won’t be touching on this too much in this book.
Line 101: Import
Line 102: Import
Line 103: Password
Line 104: Verifier
Line 105: configuration-service.js
Line 106: complicated-logger.js
Line 107: info()
Line 108: getLogLevel(): string
Line 109: Figure 5.1
Line 110: Password Verifier has two dependencies: an incoming one to determine the logging level, and an 
Line 111: outgoing one to create a log entry.
Line 112: 
Line 113: --- 페이지 135 ---
Line 114: 107
Line 115: 5.2
Line 116: Faking modules dynamically
Line 117: const { info, debug } = require("./complicated-logger");
Line 118: const { getLogLevel } = require("./configuration-service");
Line 119: const log = (text) => {
Line 120:   if (getLogLevel() === "info") {
Line 121:     info(text);
Line 122:   }
Line 123:   if (getLogLevel() === "debug") {
Line 124:     debug(text);
Line 125:   }
Line 126: };
Line 127: const verifyPassword = (input, rules) => {
Line 128:   const failed = rules
Line 129:     .map((rule) => rule(input))
Line 130:     .filter((result) => result === false);
Line 131:   if (failed.length === 0) {
Line 132:     log("PASSED");
Line 133:     return true;
Line 134:   }
Line 135:   log("FAIL");
Line 136:   return false;
Line 137: };
Line 138: In this example we’re forced to find a way to do two things:
Line 139: Simulate (stub) values returned from the configuration service’s getLogLevel
Line 140: function.
Line 141: Verify (mock) that the logger module’s info function was called.
Line 142: Figure 5.2 shows a visual representation of this.
Line 143: Listing 5.1
Line 144: Code with hardcoded modular dependencies
Line 145: verify()
Line 146: Mock
Line 147: Stub
Line 148: Import
Line 149: Import
Line 150: Password
Line 151: Verifier
Line 152: Test
Line 153: configuration-service.js
Line 154: complicated-logger.js
Line 155: info()
Line 156: getLogLevel(): string
Line 157: Assert
Line 158: Figure 5.2
Line 159: The test stubs an incoming dependency (the configuration service) and mocks the outgoing 
Line 160: dependency (the logger).
Line 161: 
Line 162: --- 페이지 136 ---
Line 163: 108
Line 164: CHAPTER 5
Line 165: Isolation frameworks
Line 166: Jest presents us with a few ways to accomplish both simulation and verification, and
Line 167: one of the cleaner ways it presents is using jest.mock([module name]) at the top of
Line 168: the spec file, followed by us requiring the fake modules in our tests so that we can con-
Line 169: figure them.
Line 170: jest.mock("./complicated-logger");      
Line 171: jest.mock("./configuration-service");   
Line 172: const { stringMatching } = expect;
Line 173: const { verifyPassword } = require("./password-verifier");
Line 174: const mockLoggerModule = require("./complicated-logger");     
Line 175: const stubConfigModule = require("./configuration-service");  
Line 176: describe("password verifier", () => {
Line 177:   afterEach(jest.resetAllMocks);   
Line 178:   test('with info log level and no rules, 
Line 179:           it calls the logger with PASSED', () => {
Line 180:     stubConfigModule.getLogLevel.mockReturnValue("info");   
Line 181:     verifyPassword("anything", []);
Line 182:     expect(mockLoggerModule.info)                      
Line 183:       .toHaveBeenCalledWith(stringMatching(/PASS/));   
Line 184:   });
Line 185:   test('with debug log level and no rules, 
Line 186:         it calls the logger with PASSED', () => {
Line 187:     stubConfigModule.getLogLevel.mockReturnValue("debug");   
Line 188:     verifyPassword("anything", []);
Line 189:     expect(mockLoggerModule.debug)                     
Line 190:       .toHaveBeenCalledWith(stringMatching(/PASS/));   
Line 191:   });
Line 192: });
Line 193: By using Jest here, I’ve saved myself a bunch of typing, and the tests still look pretty
Line 194: readable.
Line 195: 5.2.1
Line 196: Some things to notice about Jest’s API
Line 197: Jest uses the word “mock” almost everywhere, whether we’re stubbing things or mock-
Line 198: ing them, which can be a bit confusing. It’d be great if it had the word “stub” aliased
Line 199: to “mock” to make things more readable.
Line 200:  Also, due to the way JavaScript “hoisting” works, the lines faking the modules (via
Line 201: jest.mock) will need to be at the top of the file. You can read more about this in
Line 202: Ashutosh Verma’s “Understanding Hoisting in JavaScript” article here: http://mng
Line 203: .bz/j11r.
Line 204: Listing 5.2
Line 205: Faking the module APIs directly with jest.mock()
Line 206: Faking the modules
Line 207: Getting the fake 
Line 208: instances of the 
Line 209: modules
Line 210: Telling Jest to reset any fake 
Line 211: module behavior between tests
Line 212: Configuring the 
Line 213: stub to return a 
Line 214: fake “info” value.
Line 215: Asserting that the mock 
Line 216: was called correctly
Line 217: Changing the 
Line 218: stub config
Line 219: Asserting on the mock 
Line 220: logger as done previously
Line 221: 
Line 222: --- 페이지 137 ---
Line 223: 109
Line 224: 5.3
Line 225: Functional dynamic mocks and stubs
Line 226:  Also note that Jest has many other APIs and abilities, and its worth exploring them
Line 227: if you’re interested in using it. Head over to https://jestjs.io/ to get the full picture—
Line 228: it’s beyond the scope of this book, which is mostly about patterns, not tools.
Line 229:  A few other frameworks, among them Sinon (https://sinonjs.org), also support
Line 230: faking modules. Sinon is quite pleasant to work with, as far as isolation frameworks go,
Line 231: but like many other frameworks in the JavaScript world, and much like Jest, it contains
Line 232: too many ways of accomplishing the same task, and that can often be confusing. Still,
Line 233: faking modules by hand can be quite annoying without these frameworks.
Line 234: 5.2.2
Line 235: Consider abstracting away direct dependencies
Line 236: The good news about the jest.mock API, and others like it, is that it meets a very real
Line 237: need for developers who are stuck trying to test modules that have baked-in depen-
Line 238: dencies that are not easily changeable (i.e., code they cannot control). This issue is
Line 239: very prevalent in legacy code situations, which I’ll discuss in chapter 12.
Line 240:  The bad news about the jest.mock API is that it also allows us to mock the code
Line 241: that we do control and that might have benefited from abstracting away the real
Line 242: dependencies behind simpler, shorter, internal APIs. This approach, also known as
Line 243: onion architecture or hexagonal architecture or ports and adapters, is very useful for the long-
Line 244: term maintainability of our code. You can read more about this type of architecture in
Line 245: Alistair Cockburn’s article, “Hexagonal Architecture,” at https://alistair.cockburn.us/
Line 246: hexagonal-architecture/.
Line 247:  Why are direct dependencies potentially problematic? By using those APIs directly,
Line 248: we’re also forced into faking the module APIs directly in our tests instead of their
Line 249: abstractions. We’re gluing the design of those direct APIs to the implementation of
Line 250: the tests, which means that if (or really, when) those APIs change, we’ll also need to
Line 251: change many of our tests. 
Line 252:  Here’s a quick example. Imagine your code depends on a well-known JavaScript
Line 253: logging framework (such as Winston) and depends on it directly in hundreds or
Line 254: thousands of places in the code. Then imagine that Winston releases a breaking
Line 255: upgrade. Lots of pain will ensue, which could have been addressed much earlier,
Line 256: before things got out of hand. One simple way to accomplish this would be with a
Line 257: simple abstraction to a single adapter file, which is the only one holding a reference
Line 258: to that logger. That abstraction can expose a simpler, internal logging API that we
Line 259: do control, so we can prevent large-scale breakage across our code. I’ll return to this
Line 260: subject in chapter 12.
Line 261: 5.3
Line 262: Functional dynamic mocks and stubs
Line 263: We covered modular dependencies, so let’s turn to faking simple functions. We’ve
Line 264: done that plenty of times in the previous chapters, but we’ve always done it by hand.
Line 265: That works great for stubs, but for mocks it gets annoying fast.
Line 266:  The following listing shows the manual approach we used before.
Line 267:  
Line 268: 
Line 269: --- 페이지 138 ---
Line 270: 110
Line 271: CHAPTER 5
Line 272: Isolation frameworks
Line 273: test("given logger and passing scenario", () => {
Line 274:   let logged = "";                            
Line 275:   const mockLog = { info: (text) => (logged = text) };   
Line 276:   const passVerify = makeVerifier([], mockLog);
Line 277:   passVerify("any input");
Line 278:   expect(logged).toMatch(/PASSED/);   
Line 279: });
Line 280: It works—we’re able to verify that the logger function was called, but that’s a lot of work
Line 281: that can become very repetitive. Enter isolation frameworks like Jest. jest.fn() is the
Line 282: simplest way to get rid of such code. The following listing shows how we can use it.
Line 283: test('given logger and passing scenario', () => {
Line 284:   const mockLog = { info: jest.fn() };
Line 285:   const verify = makeVerifier([], mockLog);
Line 286:   verify('any input');
Line 287:   expect(mockLog.info)
Line 288:     .toHaveBeenCalledWith(stringMatching(/PASS/));
Line 289: });
Line 290: Compare this code with the previous example. It’s subtle, but it saves plenty of time.
Line 291: Here we’re using jest.fn() to get back a function that is automatically tracked by
Line 292: Jest, so that we can query it later using Jest’s API via toHaveBeenCalledWith(). It’s
Line 293: small and cute, and it works well any time you need to track calls to a specific function.
Line 294: The stringMatching function is an example of a matcher. A matcher is usually defined
Line 295: as a utility function that can assert on the value of a parameter being sent into a func-
Line 296: tion. The Jest docs use the term a bit more liberally, but you can find the full list of
Line 297: matchers in the Jest documentation at https://jestjs.io/docs/en/expect. 
Line 298:  To summarize, jest.fn() works well for single-function-based mocks and stubs.
Line 299: Let’s move on to a more object-oriented challenge.
Line 300: 5.4
Line 301: Object-oriented dynamic mocks and stubs
Line 302: As we’ve just seen, jest.fn() is an example of a single-function faking utility func-
Line 303: tion. It works well in a functional world, but it breaks down a bit when we try to use it
Line 304: on full-blown API interfaces or classes that contain multiple functions. 
Line 305: 5.4.1
Line 306: Using a loosely typed framework
Line 307: I mentioned before that there are two categories of isolation frameworks. To start, we’ll
Line 308: use the first (loosely typed, function-friendly) kind. The following listing is an example
Line 309: of trying to tackle the IComplicatedLogger we looked at in the previous chapter. 
Line 310: Listing 5.3
Line 311: Manually mocking a function to verify it was called
Line 312: Listing 5.4
Line 313: Using jest.fn() for simple function mocks
Line 314: Declaring a custom variable 
Line 315: to hold the value passed in
Line 316: Saving the 
Line 317: passed-in value 
Line 318: to that variable
Line 319: Asserting on the 
Line 320: value of the variable
Line 321: 
Line 322: --- 페이지 139 ---
Line 323: 111
Line 324: 5.4
Line 325: Object-oriented dynamic mocks and stubs
Line 326: export interface IComplicatedLogger {
Line 327:     info(text: string, method: string)
Line 328:     debug(text: string, method: string)
Line 329:     warn(text: string, method: string)
Line 330:     error(text: string, method: string)
Line 331: }
Line 332: Creating a handwritten stub or mock for this interface may be very time consuming,
Line 333: because you’d need to remember the parameters on a per-method basis, as the next
Line 334: listing shows.
Line 335: describe("working with long interfaces", () => {
Line 336:   describe("password verifier", () => {
Line 337:     class FakeLogger implements IComplicatedLogger {
Line 338:       debugText = "";
Line 339:       debugMethod = "";
Line 340:       errorText = "";
Line 341:       errorMethod = "";
Line 342:       infoText = "";
Line 343:       infoMethod = "";
Line 344:       warnText = "";
Line 345:       warnMethod = "";
Line 346:       debug(text: string, method: string) {
Line 347:         this.debugText = text;
Line 348:         this.debugMethod = method;
Line 349:       }
Line 350:       error(text: string, method: string) {
Line 351:         this.errorText = text;
Line 352:         this.errorMethod = method;
Line 353:       }
Line 354:       ...
Line 355:     }
Line 356:     test("verify, w logger & passing, calls logger with PASS", () => {
Line 357:       const mockLog = new FakeLogger();
Line 358:       const verifier = new PasswordVerifier2([], mockLog);
Line 359:       verifier.verify("anything");
Line 360:       expect(mockLog.infoText).toMatch(/PASSED/);
Line 361:     });
Line 362:   });
Line 363: });
Line 364: What a mess. Not only is this handwritten fake time consuming and cumbersome to
Line 365: write, what happens if you want it to return a specific value somewhere in the test, or
Line 366: Listing 5.5
Line 367: The IComplicatedLogger interface
Line 368: Listing 5.6
Line 369: Handwritten stubs creating lots of boilerplate code
Line 370: 
Line 371: --- 페이지 140 ---
Line 372: 112
Line 373: CHAPTER 5
Line 374: Isolation frameworks
Line 375: simulate an error from a function call on the logger? We can do it, but the code gets
Line 376: ugly fast.
Line 377:  Using an isolation framework, the code for doing this becomes trivial, more read-
Line 378: able, and much shorter. Let’s use jest.fn() for the same task and see where we end up.
Line 379: import stringMatching = jasmine.stringMatching;
Line 380: describe("working with long interfaces", () => {
Line 381:   describe("password verifier", () => {
Line 382:     test("verify, w logger & passing, calls logger with PASS", () => {
Line 383:       const mockLog: IComplicatedLogger = {    
Line 384:         info: jest.fn(),                       
Line 385:         warn: jest.fn(),                       
Line 386:         debug: jest.fn(),                      
Line 387:         error: jest.fn(),                      
Line 388:       };
Line 389:       const verifier = new PasswordVerifier2([], mockLog);
Line 390:       verifier.verify("anything");
Line 391:       expect(mockLog.info)
Line 392:         .toHaveBeenCalledWith(stringMatching(/PASS/));
Line 393:     });
Line 394:   });
Line 395: });
Line 396: Not too shabby. Here we simply outline our own object and attach a jest.fn() func-
Line 397: tion to each of the functions in the interface. This saves a lot of typing, but it has one
Line 398: important caveat: whenever the interface changes (a function is added, for example),
Line 399: we’ll have to go back to the code that defines this object and add that function. With
Line 400: plain JavaScript, this would be less of an issue, but it can still create some complica-
Line 401: tions if the code under test uses a function we didn’t define in the test. 
Line 402:  In any case, it might be wise to push the creation of such a fake object into a fac-
Line 403: tory helper method, so that the creation only exists in a single place.
Line 404: 5.4.2
Line 405: Switching to a type-friendly framework
Line 406: Let’s switch to the second category of frameworks and try substitute.js (www.npmjs
Line 407: .com/package/@fluffy-spoon/substitute). We have to choose one, and I like the C#
Line 408: version of this framework a lot and used it in the previous edition of this book. 
Line 409:  With substitute.js (and the assumption of working with TypeScript), we can write
Line 410: code like the following.
Line 411: import { Substitute, Arg } from "@fluffy-spoon/substitute";
Line 412: describe("working with long interfaces", () => {
Line 413:   describe("password verifier", () => {
Line 414: Listing 5.7
Line 415: Mocking individual interface functions with jest.fn()
Line 416: Listing 5.8
Line 417: Using substitute.js to fake a full interface
Line 418: Setting up the 
Line 419: mock using Jest
Line 420: 
Line 421: --- 페이지 141 ---
Line 422: 113
Line 423: 5.4
Line 424: Object-oriented dynamic mocks and stubs
Line 425:     test("verify, w logger & passing, calls logger w PASS", () => {
Line 426:       const mockLog = Substitute.for<IComplicatedLogger>();   
Line 427:       const verifier = new PasswordVerifier2([], mockLog);
Line 428:       verifier.verify("anything");
Line 429:       mockLog.received().info(                 
Line 430:         Arg.is((x) => x.includes("PASSED")),   
Line 431:         "verify"                               
Line 432:       );
Line 433:     });
Line 434:   });
Line 435: });
Line 436: In the preceding listing, we generate the fake object, which absolves us of caring
Line 437: about any functions other than the one we’re testing against, even if the object’s signa-
Line 438: ture changes in the future. We then use .received() as our verification mechanism,
Line 439: as well as another argument matcher, Arg.is, this time from substitute.js’s API, which
Line 440: works just like string matches from Jasmine. The added benefit here is that if new
Line 441: functions are added to the object’s signature, we will be less likely to need to change
Line 442: the test, and there’s no need to add those functions to any tests that use the same
Line 443: object signature.  
Line 444: OK, that was mocks. What about stubs?
Line 445: Isolation frameworks and the Arrange-Act-Assert pattern
Line 446: Notice that the way you use the isolation framework matches nicely with the Arrange-
Line 447: Act-Assert structure, which we discussed in chapter 1. You start by arranging a fake
Line 448: object, you act on the thing you’re testing, and then you assert on something at the
Line 449: end of the test. 
Line 450: It wasn’t always this easy, though. In the olden days (around 2006), most of the open
Line 451: source isolation frameworks didn’t support the idea of Arrange-Act-Assert and instead
Line 452: used a concept called Record-Replay (we’re talking about Java and C#). Record-
Line 453: Replay was a nasty mechanism where you’d have to tell the isolation API that its fake
Line 454: object was in record mode, and then you’d have to call the methods on that object
Line 455: as you expected them to be called from production code. Then you’d have to tell the
Line 456: isolation API to switch into replay mode, and only then could you send your fake object
Line 457: into the heart of your production code. An example can be seen on the Baeldung site
Line 458: at www.baeldung.com/easymock.
Line 459: Compared to today’s ability to write tests that use the far more readable Arrange-Act-
Line 460: Assert model, this tragedy cost many developers millions of combined hours in pains-
Line 461: taking test reading to figure out exactly where tests failed.
Line 462: If you have the first edition of this book, you can see an example of Record-Replay
Line 463: when I showed Rhino Mocks (which initially had the same design).
Line 464: Generating 
Line 465: the fake 
Line 466: object
Line 467: Verifying the 
Line 468: fake object 
Line 469: was called
Line 470: 
Line 471: --- 페이지 142 ---
Line 472: 114
Line 473: CHAPTER 5
Line 474: Isolation frameworks
Line 475: 5.5
Line 476: Stubbing behavior dynamically
Line 477: Jest has a very simple API for simulating return values for modular and functional
Line 478: dependencies: mockReturnValue() and mockReturnValueOnce().
Line 479: test("fake same return values", () => {
Line 480:   const stubFunc = jest.fn()
Line 481:     .mockReturnValue("abc");
Line 482:   //value remains the same
Line 483:   expect(stubFunc()).toBe("abc");
Line 484:   expect(stubFunc()).toBe("abc");
Line 485:   expect(stubFunc()).toBe("abc");
Line 486: });
Line 487: test("fake multiple return values", () => {
Line 488:   const stubFunc = jest.fn()
Line 489:     .mockReturnValueOnce("a")
Line 490:     .mockReturnValueOnce("b")
Line 491:     .mockReturnValueOnce("c");
Line 492:   //value remains the same
Line 493:   expect(stubFunc()).toBe("a");
Line 494:   expect(stubFunc()).toBe("b");
Line 495:   expect(stubFunc()).toBe("c");
Line 496:   expect(stubFunc()).toBe(undefined);
Line 497: });
Line 498: Notice that, in the first test, we’re setting a permanent return value for the duration of
Line 499: the test. This is my preferred method of writing tests if I can use it, because it makes
Line 500: the tests simple to read and maintain. If we do need to simulate multiple values, we
Line 501: can use mockReturnValueOnce. 
Line 502:  If you need to simulate an error or do anything more complicated, you can use
Line 503: mockImplementation() and mockImplementationOnce():
Line 504: yourStub.mockImplementation(() => {
Line 505:   throw new Error();
Line 506: });
Line 507: 5.5.1
Line 508: An object-oriented example with a mock and a stub
Line 509: Let’s add another ingredient into our Password Verifier equation. 
Line 510: Let’s say that the Password Verifier is not active during a special maintenance
Line 511: window, when software is being updated. 
Line 512: When a maintenance window is active, calling verify() on the verifier will
Line 513: cause it to call logger.info() with “under maintenance.” 
Line 514: Otherwise it will call logger.info() with a “passed” or “failed” result. 
Line 515: Listing 5.9
Line 516: Stubbing a value from a fake function with jest.fn() 
Line 517: 
Line 518: --- 페이지 143 ---
Line 519: 115
Line 520: 5.5
Line 521: Stubbing behavior dynamically
Line 522: For this purpose (and for the purpose of showing an object-oriented design decision),
Line 523: we’ll introduce a MaintenanceWindow interface that will be injected into the construc-
Line 524: tor of our Password Verifier, as illustrated in figure 5.3.
Line 525: The following listing shows the code for the Password Verifier using the new dependency.
Line 526: export class PasswordVerifier3 {
Line 527:   private _rules: any[];
Line 528:   private _logger: IComplicatedLogger;
Line 529:   private _maintenanceWindow: MaintenanceWindow;
Line 530:   constructor(
Line 531:     rules: any[],
Line 532:     logger: IComplicatedLogger,
Line 533:     maintenanceWindow: MaintenanceWindow
Line 534:   ) {
Line 535:     this._rules = rules;
Line 536:     this._logger = logger;
Line 537:     this._maintenanceWindow = maintenanceWindow;
Line 538:   }
Line 539:   verify(input: string): boolean {
Line 540:     if (this._maintenanceWindow.isUnderMaintenance()) {
Line 541:       this._logger.info("Under Maintenance", "verify");
Line 542:       return false;
Line 543:     }
Line 544:     const failed = this._rules
Line 545:       .map((rule) => rule(input))
Line 546:       .filter((result) => result === false);
Line 547:     if (failed.length === 0) {
Line 548:       this._logger.info("PASSED", "verify");
Line 549:       return true;
Line 550:     }
Line 551: Listing 5.10
Line 552: Password Verifier with a MaintenanceWindow dependency
Line 553: verify()
Line 554: Password
Line 555: Verifier
Line 556: MaintenanceWindow
Line 557: Logger
Line 558: info()
Line 559: isUnderMaintenance(): bool
Line 560: Figure 5.3
Line 561: Using the MaintenanceWindow interface
Line 562: 
Line 563: --- 페이지 144 ---
Line 564: 116
Line 565: CHAPTER 5
Line 566: Isolation frameworks
Line 567:     this._logger.info("FAIL", "verify");
Line 568:     return false;
Line 569:   }
Line 570: }
Line 571: The MaintenanceWindow interface is injected as a constructor parameter (i.e., using
Line 572: constructor injection), and it’s used to determine where to execute or not execute the
Line 573: password verification and send the proper message to the logger.
Line 574: 5.5.2
Line 575: Stubs and mocks with substitute.js
Line 576: Now we’ll use substitute.js instead of Jest to create a stub of the MaintenanceWindow
Line 577: interface and a mock of the IComplicatedLogger interface. Figure 5.4 illustrates this.
Line 578: Creating stubs and mocks with substitute.js works the same way: we use the Substi-
Line 579: tute.for<T> function. We can configure stubs with the .returns function and verify
Line 580: mocks with the .received function. Both of these are part of the fake object that is
Line 581: returned from Substitute.for<T>(). 
Line 582:  Here’s what stub creation and configuration looks like:
Line 583: const stubMaintWindow = Substitute.for<MaintenanceWindow>();
Line 584: stubMaintWindow.isUnderMaintenance().returns(true);
Line 585: Mock creation and verification looks like this:
Line 586: const mockLog = Substitute.for<IComplicatedLogger>();
Line 587: . . .
Line 588: /// later down in the end of the test…
Line 589: mockLog.received().info("Under Maintenance", "verify");
Line 590: verify()
Line 591: Password
Line 592: Verifier
Line 593: MaintenanceWindow
Line 594: Logger
Line 595: info()
Line 596: isUnderMaintenance(): bool
Line 597: Stub
Line 598: Mock
Line 599: Test
Line 600: Figure 5.4
Line 601: A MaintenanceWindow dependency
Line 602: 
Line 603: --- 페이지 145 ---
Line 604: 117
Line 605: 5.6
Line 606: Advantages and traps of isolation frameworks
Line 607: The following listing shows the full code for a couple of tests that use a mock and a stub.
Line 608: import { Substitute } from "@fluffy-spoon/substitute";
Line 609: const makeVerifierWithNoRules = (log, maint) =>
Line 610:   new PasswordVerifier3([], log, maint);
Line 611: describe("working with substitute part 2", () => {
Line 612:   test("verify, during maintanance, calls logger", () => {
Line 613:     const stubMaintWindow = Substitute.for<MaintenanceWindow>();
Line 614:     stubMaintWindow.isUnderMaintenance().returns(true);
Line 615:     const mockLog = Substitute.for<IComplicatedLogger>();
Line 616:     const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
Line 617:     verifier.verify("anything");
Line 618:     mockLog.received().info("Under Maintenance", "verify");
Line 619:   });
Line 620:   test("verify, outside maintanance, calls logger", () => {
Line 621:     const stubMaintWindow = Substitute.for<MaintenanceWindow>();
Line 622:     stubMaintWindow.isUnderMaintenance().returns(false);
Line 623:     const mockLog = Substitute.for<IComplicatedLogger>();
Line 624:     const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
Line 625:     verifier.verify("anything");
Line 626:     mockLog.received().info("PASSED", "verify");
Line 627:   });
Line 628: });
Line 629: We can successfully and relatively easily simulate values in our tests with dynamically
Line 630: created objects. I encourage you to research the flavor of an isolation framework
Line 631: you’d like to use. I’ve only used substitute.js as an example in this book. It’s not the
Line 632: only framework out there.
Line 633:  This test requires no handwritten fakes, but notice that it’s already starting to take
Line 634: a toll on the readability for the test reader. Functional designs are usually much slim-
Line 635: mer than this. In an object-oriented setting, sometimes this is a necessary evil. How-
Line 636: ever, we could easily refactor the creation of various helpers, mocks, and stubs to
Line 637: helper functions as we refactor our code, so that the test can be simpler and shorter to
Line 638: read. More on that in part 3 of this book.
Line 639: 5.6
Line 640: Advantages and traps of isolation frameworks
Line 641: Based on what we’ve covered in this chapter, we’ve seen distinct advantages to using
Line 642: isolation frameworks:
Line 643: Easier modular faking—Module dependencies can be hard to get around without
Line 644: some boilerplate code, which isolation frameworks help us eliminate. This point
Line 645: Listing 5.11
Line 646: Testing Password Verifier with substitute.js
Line 647: 
Line 648: --- 페이지 146 ---
Line 649: 118
Line 650: CHAPTER 5
Line 651: Isolation frameworks
Line 652: can also be counted as a negative, as explained earlier, because it encourages us
Line 653: to have code strongly coupled to third-party implementations.
Line 654: Easier simulation of values or errors—Writing mocks manually can be difficult
Line 655: across a complicated interface. Frameworks help a lot.
Line 656: Easier fake creation—Isolation frameworks can be used to create both mocks and
Line 657: stubs more easily. 
Line 658: Although there are many advantages to using isolation frameworks, there are also pos-
Line 659: sible dangers. Let’s now talk about a few things to watch out for.
Line 660: 5.6.1
Line 661: You don’t need mock objects most of the time
Line 662: The biggest trap that isolation frameworks lead you into is making it easy to fake any-
Line 663: thing, and encouraging you to think you need mock objects in the first place. I’m not
Line 664: saying you won’t need stubs, but mock objects shouldn’t be the standard operating
Line 665: procedure for most unit tests. Remember that a unit of work can have three different
Line 666: types of exit points: return values, state change, and calling a third-party dependency.
Line 667: Only one of these types can benefit from a mock object in your test. The others don’t.
Line 668:  I find that, in my own tests, mock objects are present in perhaps 2%–5% of my tests.
Line 669: The rest of the tests are usually return-value or state-based tests. For functional designs,
Line 670: the number of mock objects should be near zero, except for some corner cases.
Line 671:  If you find yourself defining a test and verifying that an object or function was
Line 672: called, think carefully whether you can prove the same functionality without a mock
Line 673: object, but instead by verifying a return value or a change in the behavior of the over-
Line 674: all unit of work from the outside (for example, verifying that a function throws an
Line 675: exception when it didn’t before). Chapter 6 of Unit Testing Principles, Practices, and Pat-
Line 676: terns by Vladimir Khorikov (Manning, 2020) contains a detailed description of how to
Line 677: refactor interaction-based tests into simpler, more reliable tests that check a return
Line 678: value instead.
Line 679: 5.6.2
Line 680: Unreadable test code
Line 681: Using a mock in a test makes the test a little less readable, but still readable enough
Line 682: that an outsider can look at it and understand what’s going on. Having many mocks,
Line 683: or many expectations, in a single test can ruin the readability of the test so it’s hard to
Line 684: maintain, or even to understand what’s being tested.
Line 685:  If you find that your test becomes unreadable or hard to follow, consider removing
Line 686: some mocks or some mock expectations, or separating the test into several smaller
Line 687: tests that are more readable.
Line 688: 5.6.3
Line 689: Verifying the wrong things
Line 690: Mock objects allow you to verify that methods were called on your interfaces or that
Line 691: functions were called, but that doesn’t necessarily mean that you’re testing the right
Line 692: thing. A lot of people new to tests end up verifying things just because they can, not
Line 693: because it makes sense. Examples may include the following:
Line 694: 
Line 695: --- 페이지 147 ---
Line 696: 119
Line 697: Summary
Line 698: Verifying that an internal function calls another internal function (not an
Line 699: exit point).
Line 700: Verifying that a stub was called (an incoming dependency should not be veri-
Line 701: fied; it’s the overspecification antipattern, as we’ll discuss in section 5.6.5).
Line 702: Verifying that something was called simply because someone told you to write a
Line 703: test, and you’re not sure what should really be tested. (This is a good time to
Line 704: verify that you’re understanding the requirements correctly.)
Line 705: 5.6.4
Line 706: Having more than one mock per test
Line 707: It’s considered good practice to test only one concern per test. Testing more than one
Line 708: concern can lead to confusion and problems maintaining the test. Having two mocks
Line 709: in a test is the same as testing several end results of the same unit of work (multiple
Line 710: exit points).
Line 711:  For each exit point, consider writing a separate test, as it could be considered a
Line 712: separate requirement. Chances are that your test names will also become more focused
Line 713: and readable when you only test one concern. If you can’t name your test because it
Line 714: does too many things and the name becomes very generic (e.g., “XWorksOK”), it’s time
Line 715: to separate it into more than one test.
Line 716: 5.6.5
Line 717: Overspecifying the tests
Line 718: If your test has too many expectations (x.received().X(), x.received().Y(), and so
Line 719: on), it may become very fragile, breaking on the slightest of production code changes,
Line 720: even though the overall functionality still works. Testing interactions is a double-
Line 721: edged sword: test them too much, and you start to lose sight of the big picture—the
Line 722: overall functionality; test them too little, and you’ll miss the important interactions
Line 723: between units of work. 
Line 724:  Here are some ways to balance this effect:
Line 725: Use stubs instead of mocks when you can—If more than 5% of your tests use mock
Line 726: objects, you might be overdoing it. Stubs can be everywhere. Mocks, not so
Line 727: much. You only need to test one scenario at a time. The more mocks you
Line 728: have, the more verifications will take place at the end of the test, but usually
Line 729: only one will be the important one. The rest will be noise against the current
Line 730: test scenario.
Line 731: Avoid using stubs as mocks if possible—Use a stub only for faking simulated values
Line 732: into the unit of work under test or to throw exceptions. Don’t verify that meth-
Line 733: ods were called on stubs.
Line 734: Summary
Line 735: Isolation, or mocking, frameworks allow you to dynamically create, configure,
Line 736: and verify mocks and stubs, either in object or function form. Isolation frame-
Line 737: works save a lot of time compared to handwritten fakes, especially in modular
Line 738: dependency situations.
Line 739: 
Line 740: --- 페이지 148 ---
Line 741: 120
Line 742: CHAPTER 5
Line 743: Isolation frameworks
Line 744: There are two flavors of isolation frameworks: loosely typed (such as Jest and
Line 745: Sinon) and strongly typed (such as substitute.js). Loosely typed frameworks
Line 746: require less boilerplate and are good for functional-style code; strongly typed
Line 747: frameworks are useful when dealing with classes and interfaces.
Line 748: Isolation frameworks can replace whole modules, but try to abstract away direct
Line 749: dependencies and fake those abstractions instead. This will help you reduce the
Line 750: amount of refactoring needed when the module’s API changes.
Line 751: It's important to lean toward return-value or state-based testing as opposed to
Line 752: interaction testing whenever you can, so that your tests assume as little as possi-
Line 753: ble about internal implementation details.
Line 754: Mocks should be used only when there’s no other way to test the implementa-
Line 755: tion, because they eventually lead to tests that are harder to maintain if you’re
Line 756: not careful.
Line 757: Choose the way you work with isolation frameworks based on the codebase you
Line 758: are working on. In legacy projects, you may need to fake whole modules, as it
Line 759: might be the only way to add tests to such projects. In greenfield projects, try to
Line 760: introduce proper abstractions on top of third-party modules. It’s all about pick-
Line 761: ing the right tool for the job, so be sure to look at the big picture when consid-
Line 762: ering how to approach a specific problem in testing.
