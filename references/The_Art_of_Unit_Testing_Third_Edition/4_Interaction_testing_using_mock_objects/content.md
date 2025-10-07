Line 1: 
Line 2: --- 페이지 111 ---
Line 3: 83
Line 4: Interaction testing
Line 5: using mock objects
Line 6: In the previous chapter, we solved the problem of testing code that depends on
Line 7: other objects to run correctly. We used stubs to make sure that the code under
Line 8: test received all the inputs it needed so that we could test the unit of work in
Line 9: isolation.
Line 10:  So far, you’ve only written tests that work against the first two of the three types
Line 11: of exit points a unit of work can have: returning a value and changing the state of the
Line 12: system (you can read more about these types in chapter 1). In this chapter, we’ll
Line 13: look at how you can test the third type of exit point—a call to a third-party func-
Line 14: tion, module, or object. This is important, because often we’ll have code that
Line 15: depends on things we can’t control. Knowing how to check that type of code is an
Line 16: important skill in the world of unit testing. Basically, we’ll find ways to prove that
Line 17: This chapter covers
Line 18: Defining interaction testing 
Line 19: Reasons to use mock objects
Line 20: Injecting and using mocks
Line 21: Dealing with complicated interfaces
Line 22: Partial mocks
Line 23: 
Line 24: --- 페이지 112 ---
Line 25: 84
Line 26: CHAPTER 4
Line 27: Interaction testing using mock objects
Line 28: our unit of work ends up calling a function that we don’t control and identify what val-
Line 29: ues were sent as arguments. 
Line 30:  The approaches we’ve looked at so far won’t do here, because third-party func-
Line 31: tions usually don’t have specialized APIs that allow us to check if they were called
Line 32: correctly. Instead, they internalize their operations for clarity and maintainability.
Line 33: So, how can you test that your unit of work interacts with third-party functions cor-
Line 34: rectly? You use mocks.
Line 35: 4.1
Line 36: Interaction testing, mocks, and stubs
Line 37: Interaction testing is checking how a unit of work interacts with and sends messages
Line 38: (i.e., calls functions) to a dependency beyond its control. Mock functions or objects
Line 39: are used to assert that a call was made correctly to an external dependency.
Line 40:  Let’s recall the differences between mocks and stubs as we covered them in chap-
Line 41: ter 3. The main difference is in the flow of information: 
Line 42: Mock—Used to break outgoing dependencies. Mocks are fake modules, objects,
Line 43: or functions that we assert were called in our tests. A mock represents an exit
Line 44: point in a unit test. If we don’t assert on it, it’s not used as a mock. 
Line 45: It is normal to have no more than a single mock per test, for maintainability
Line 46: and readability reasons. (We’ll discuss this more in part 3 of this book about
Line 47: writing maintainable tests.)
Line 48: Stub—Used to break incoming dependencies. Stubs are fake modules, objects,
Line 49: or functions that provide fake behavior or data to the code under test. We do
Line 50: not assert against them, and we can have many stubs in a single test. 
Line 51: Stubs represent waypoints, not exit points, because the data or behavior
Line 52: flows into the unit of work. They are points of interaction, but they do not repre-
Line 53: sent an ultimate outcome of the unit of work. Instead, they are an interaction
Line 54: on the way to achieving the end result we care about, so we don’t treat them as
Line 55: exit points.
Line 56: Figure 4.1 shows these two side by side.
Line 57:  Let’s look at a simple example of an exit point to a dependency that we do not con-
Line 58: trol: calling a logger.
Line 59:  
Line 60:  
Line 61:  
Line 62:  
Line 63:  
Line 64:  
Line 65:  
Line 66: 
Line 67: --- 페이지 113 ---
Line 68: 85
Line 69: 4.2
Line 70: Depending on a logger
Line 71: 4.2
Line 72: Depending on a logger
Line 73: Let’s take this Password Verifier function as our starting example, and we’ll assume we
Line 74: have a complicated logger (which is a logger that has more functions and parameters,
Line 75: so the interface may present more of a challenge). One of the requirements of our
Line 76: function is to call the logger when verification has passed or failed, as follows.
Line 77: // impossible to fake with traditional injection techniques
Line 78: const log = require('./complicated-logger');
Line 79: const verifyPassword = (input, rules) => {
Line 80:   const failed = rules
Line 81:     .map(rule => rule(input))
Line 82:     .filter(result => result === false);
Line 83:   if (failed.count === 0) {
Line 84:     // to test with traditional injection techniques
Line 85:     log.info('PASSED');                                      
Line 86:     return true; //                                          
Line 87:   }
Line 88:   //impossible to test with traditional injection techniques
Line 89:   log.info('FAIL'); //                                       
Line 90:   return false; //                                           
Line 91: };
Line 92: const info = (text) => {
Line 93:     console.log(`INFO: ${text}`);
Line 94: };
Line 95: Listing 4.1
Line 96: Depending directly on a complicated logger 
Line 97: Test
Line 98: Entry point
Line 99: Exit point
Line 100: Data
Line 101: or behavior
Line 102: Dependency
Line 103: Unit
Line 104: of
Line 105: work
Line 106: Test
Line 107: Entry point
Line 108: Exit point
Line 109: Dependency
Line 110: Unit
Line 111: of
Line 112: work
Line 113: Outgoing dependency
Line 114: (use mocks)
Line 115: Incoming dependency
Line 116: (use stubs)
Line 117: Figure 4.1
Line 118: On the left, an exit point that is implemented as invoking a dependency. On the right, the dependency 
Line 119: provides indirect input or behavior and is not an exit point.
Line 120: Exit
Line 121: point
Line 122: 
Line 123: --- 페이지 114 ---
Line 124: 86
Line 125: CHAPTER 4
Line 126: Interaction testing using mock objects
Line 127: const debug = (text) => {
Line 128:     console.log(`DEBUG: ${text}`);
Line 129: };
Line 130: Figure 4.2 illustrates this. Our verifyPassword function is the entry point to the unit
Line 131: of work, and we have a total of two exit points: one that returns a value, and another
Line 132: that calls log.info().
Line 133: Unfortunately, we cannot verify that logger was called by using any traditional means,
Line 134: or without using some Jest tricks, which I usually use only if there’s no other choice, as
Line 135: they tend to make tests less readable and harder to maintain (more on that later in
Line 136: this chapter).
Line 137:  Let’s do what we like to do with dependencies: abstract them. There are many ways
Line 138: to create a seam in our code. Remember, seams are places where two pieces of code
Line 139: meet—we can use them to inject fake things. Table 4.1 lists the most common ways to
Line 140: abstract dependencies.
Line 141: Table 4.1
Line 142: Techniques for injecting fakes
Line 143: Style
Line 144: Technique
Line 145: Standard
Line 146: Introduce parameter
Line 147: Functional
Line 148: Use currying
Line 149: Convert to higher-order functions
Line 150: Modular
Line 151: Abstract module dependency
Line 152: Object oriented
Line 153: Inject untyped object
Line 154: Inject interface
Line 155: verifyPassword(input, rules)
Line 156: Return value
Line 157: Password
Line 158: verifier
Line 159: Third-party
Line 160: log.info(text)
Line 161: Figure 4.2
Line 162: The entry point 
Line 163: to the Password Verifier is the 
Line 164: verifyPassword function. One 
Line 165: exit point returns a value, and the 
Line 166: other calls log.info().
Line 167: 
Line 168: --- 페이지 115 ---
Line 169: 87
Line 170: 4.3
Line 171: Standard style: Introduce parameter refactoring
Line 172: 4.3
Line 173: Standard style: Introduce parameter refactoring
Line 174: The most obvious way we can start this journey is by introducing a new parameter into
Line 175: our code under test. 
Line 176: const verifyPassword2 = (input, rules, logger) => {
Line 177:     const failed = rules
Line 178:         .map(rule => rule(input))
Line 179:         .filter(result => result === false);
Line 180:     if (failed.length === 0) {
Line 181:         logger.info('PASSED');
Line 182:         return true;
Line 183:     }
Line 184:     logger.info('FAIL');
Line 185:     return false;
Line 186: };
Line 187: The following listing shows how we could write the simplest of tests for this, using a
Line 188: simple closure mechanism.
Line 189: describe('password verifier with logger', () => {
Line 190:     describe('when all rules pass', () => {
Line 191:         it('calls the logger with PASSED', () => {
Line 192:             let written = '';
Line 193:             const mockLog = {
Line 194:                 info: (text) => {
Line 195:                     written = text;
Line 196:                 }
Line 197:             };
Line 198:             verifyPassword2('anything', [], mockLog);
Line 199:             expect(written).toMatch(/PASSED/);
Line 200:         });
Line 201:     });
Line 202: });
Line 203: Notice first that we are naming the variable mockXXX (mockLog in this example) to
Line 204: denote the fact that we have a mock function or object in the test. I use this naming
Line 205: convention because I want you, as a reader of the test, to know that you should expect
Line 206: an assert (also known as verification) against that mock at the end of the test. This nam-
Line 207: ing approach removes the element of surprise for the reader and makes the test much
Line 208: more predictable. Only use this naming convention for things that are actually mocks. 
Line 209:  Here’s our first mock object:
Line 210: let written = '';
Line 211: const mockLog = {
Line 212: Listing 4.2
Line 213: Mock logger parameter injection
Line 214: Listing 4.3
Line 215: Handwritten mock object
Line 216: 
Line 217: --- 페이지 116 ---
Line 218: 88
Line 219: CHAPTER 4
Line 220: Interaction testing using mock objects
Line 221:     info: (text) => {
Line 222:         written = text;
Line 223:     }
Line 224: };
Line 225: It only has one function, which mimics the signature of the logger’s info function. It
Line 226: then saves the parameter being passed to it (text) so that we can assert that it was
Line 227: called later in the test. If the written variable has the correct text, this proves that our
Line 228: function was called, which means we have proven that the exit point is invoked cor-
Line 229: rectly from our unit of work. 
Line 230:  On the verifyPassword2 side, the refactoring we did is pretty common. It’s pretty
Line 231: much the same as we did in the previous chapter, where we extracted a stub as a
Line 232: dependency. Stubs and mocks are often treated the same way in terms of refactoring
Line 233: and introducing seams in our application’s code.
Line 234:  What did this simple refactoring into a parameter provide us with? 
Line 235: We do not need to explicitly import (via require) the logger in our code
Line 236: under test anymore. That means that if we ever change the real dependency of
Line 237: the logger, the code under test will have one less reason to change. 
Line 238: We now have the ability to inject any logger of our choosing into the code under
Line 239: test, as long as it lives up to the same interface (or at least has the info
Line 240: method). This means that we can provide a mock logger that does our bidding
Line 241: for us: the mock logger helps us verify that it was called correctly. 
Line 242: NOTE
Line 243: The fact that our mock object only mimics a part of the logger’s inter-
Line 244: face (it’s missing the debug function) is a form of duck typing. I discussed this
Line 245: idea in chapter 3: if it walks like a duck, and it talks like a duck, then we can
Line 246: use it as a fake object.
Line 247: 4.4
Line 248: The importance of differentiating between mocks 
Line 249: and stubs
Line 250: Why do I care so much about what we name each thing? If we can’t tell the difference
Line 251: between mocks and stubs, or we don’t name them correctly, we can end up with tests
Line 252: that are testing multiple things and that are less readable and harder to maintain.
Line 253: Naming things correctly helps us avoid these pitfalls. 
Line 254:  Given that a mock represents a requirement from our unit of work (“it calls the
Line 255: logger,” “it sends an email,” etc.) and that a stub represents incoming information or
Line 256: behavior (“the database query returns false,” “this specific configuration throws an
Line 257: error”), we can set a simple rule of thumb: It should be OK to have multiple stubs in a
Line 258: test, but you don’t usually want to have more than a single mock per test, because that
Line 259: would mean you’re testing more than one requirement in a single test.
Line 260:  If we can’t (or won’t) differentiate between things (naming is key to that), we can
Line 261: end up with multiple mocks per test or asserting our stubs, both of which can have neg-
Line 262: ative effects on our tests. Keeping naming consistent gives us the following benefits:
Line 263: 
Line 264: --- 페이지 117 ---
Line 265: 89
Line 266: 4.5
Line 267: Modular-style mocks
Line 268: Readability—Your test name will become much more generic and harder to
Line 269: understand. You want people to be able to read the name of the test and know
Line 270: everything that happens or is tested inside of it, without needing to read the
Line 271: test’s code.
Line 272: Maintainability—You could, without noticing or even caring, assert against stubs
Line 273: if you don’t differentiate between mocks and stubs. This produces little value to
Line 274: you and increases the coupling between your tests and internal production
Line 275: code. Asserting that you queried a database is a good example of this. Instead of
Line 276: testing that a database query returns some value, it would be much better to test
Line 277: that the application’s behavior changes after we change the input from the
Line 278: database. 
Line 279: Trust—If you have multiple mocks (requirements) in a single test, and the first
Line 280: mock verification fails the test, most test frameworks won’t execute the rest of
Line 281: the test (below the failing assert line) because an exception has been thrown.
Line 282: This means that the other mocks aren’t verified, and you won’t get the results
Line 283: from them.
Line 284: To drive the last point home, imagine a doctor who only sees 30% of their patient’s
Line 285: symptoms, but still needs to make a decision—they might make the wrong decision
Line 286: about treatment. If you can’t see where all the bugs are, or that two things are failing
Line 287: instead of just one (because one of them is hidden after the first failure), you’re more
Line 288: likely to fix the wrong thing or to fix it in the wrong place. 
Line 289:  XUnit Test Patterns (Addison-Wesley, 2007), by Gerard Meszaros, calls this situation
Line 290: assertion roulette (http://xunitpatterns.com/Assertion%20Roulette.html). I like this
Line 291: name. It’s quite a gamble. You start commenting out lines of code in your test, and lots
Line 292: of fun ensues (and possibly alcohol).
Line 293: 4.5
Line 294: Modular-style mocks
Line 295: I covered modular dependency injection in the previous chapter, but now we’re going
Line 296: to look at how we can use it to inject mock objects and simulate answers on them.
Line 297: Not everything is a mock
Line 298: It’s unfortunate that people still tend to use the word “mock” for anything that isn’t
Line 299: real, such as “mock database” or “mock service.” Most of the time they really mean
Line 300: they are using a stub. 
Line 301: It’s hard to blame them, though. Frameworks like Mockito, jMock, and most isolation
Line 302: frameworks (I don’t call them mocking frameworks, for the same reasons I’m dis-
Line 303: cussing right now), use the word “mock” to denote both mocks and stubs. 
Line 304: There are newer frameworks, such as Sinon and testdouble in JavaScript, NSubsti-
Line 305: tute and FakeItEasy in .NET, and others, that have helped start a change in the nam-
Line 306: ing conventions. I hope this persists.
Line 307: 
Line 308: --- 페이지 118 ---
Line 309: 90
Line 310: CHAPTER 4
Line 311: Interaction testing using mock objects
Line 312: 4.5.1
Line 313: Example of production code
Line 314: Let’s look at a slightly more complicated example than we saw before. In this scenario,
Line 315: our verifyPassword function depends on two external dependencies: 
Line 316:  A logger 
Line 317:  A configuration service
Line 318: The configuration service provides the logging level that is required. Usually this type
Line 319: of code would be moved into a special logger module, but for the purposes of this
Line 320: book’s examples, I’m putting the logic that calls logger.info and logger.debug
Line 321: directly in the code under test.
Line 322: const { info, debug } = require("./complicated-logger");
Line 323: const { getLogLevel } = require("./configuration-service");
Line 324: const log = (text) => {
Line 325:   if (getLogLevel() === "info") {
Line 326:     info(text);
Line 327:   }
Line 328:   if (getLogLevel() === "debug") {
Line 329:     debug(text);
Line 330:   }
Line 331: };
Line 332: const verifyPassword = (input, rules) => {
Line 333:   const failed = rules
Line 334:     .map((rule) => rule(input))
Line 335:     .filter((result) => result === false);
Line 336:   if (failed.length === 0) {
Line 337:     log("PASSED");   
Line 338:     return true;
Line 339:   }
Line 340:   log("FAIL");       
Line 341:   return false;
Line 342: };
Line 343: module.exports = {
Line 344:   verifyPassword,
Line 345: };
Line 346: Let’s assume that we realized we have a bug when we call the logger. We’ve changed
Line 347: the way we check for failures, and now we call the logger with a PASSED result when
Line 348: the number of failures is positive instead of zero. How can we prove that this bug
Line 349: exists, or that we’ve fixed it, with a unit test?
Line 350:  Our problem here is that we are importing (or requiring) the modules directly in
Line 351: our code. If we want to replace the logger module, we have to either replace the file or
Line 352: perform some other dark magic through Jest’s API. I wouldn’t recommend that usually,
Line 353: Listing 4.4
Line 354: A hard modular dependency 
Line 355: Calling the 
Line 356: logger
Line 357: 
Line 358: --- 페이지 119 ---
Line 359: 91
Line 360: 4.5
Line 361: Modular-style mocks
Line 362: because using these techniques leads to more pain and suffering than is usual when
Line 363: dealing with code. 
Line 364: 4.5.2
Line 365: Refactoring the production code in a modular injection style
Line 366: We can abstract away the module dependencies into their own object and allow the
Line 367: user of our module to replace that object as follows.
Line 368: const originalDependencies = {             
Line 369:     log: require('./complicated-logger'),  
Line 370: };                                         
Line 371: let dependencies = { ...originalDependencies };    
Line 372: const resetDependencies = () => {                
Line 373:     dependencies = { …originalDependencies };    
Line 374: };                                               
Line 375: const injectDependencies = (fakes) => {    
Line 376:     Object.assign(dependencies, fakes);    
Line 377: };                                         
Line 378: const verifyPassword = (input, rules) => {
Line 379:     const failed = rules
Line 380:         .map(rule => rule(input))
Line 381:         .filter(result => result === false);
Line 382:     if (failed.length === 0) {
Line 383:         dependencies.log.info('PASSED');
Line 384:         return true;
Line 385:     }
Line 386:     dependencies.log.info('FAIL');
Line 387:     return false;
Line 388: };
Line 389: module.exports = {
Line 390:     verifyPassword,        
Line 391:     injectDependencies,    
Line 392:     resetDependencies      
Line 393: };
Line 394: There’s more production code here, and it seems more complex, but this allows us to
Line 395: replace dependencies in our tests in a relatively easy manner if we are forced to work
Line 396: in such a modular fashion. 
Line 397:  The originalDependencies variable will always hold the original dependencies, so
Line 398: that we never lose them between tests. dependencies is our layer of indirection. It
Line 399: defaults to the original dependencies, but our tests can direct the code under test to
Line 400: replace that variable with custom dependencies (without knowing anything about the
Line 401: internals of the module). injectDependencies and resetDependencies are the pub-
Line 402: lic API that the module exposes for overriding and resetting the dependencies. 
Line 403: Listing 4.5
Line 404: Refactoring to a modular injection pattern
Line 405: Holding original 
Line 406: dependencies
Line 407: The layer of 
Line 408: indirection
Line 409: A function that resets 
Line 410: the dependencies 
Line 411: A function that overrides 
Line 412: the dependencies
Line 413: Exposing the API to the 
Line 414: users of the module
Line 415: 
Line 416: --- 페이지 120 ---
Line 417: 92
Line 418: CHAPTER 4
Line 419: Interaction testing using mock objects
Line 420: 4.5.3
Line 421: A test example with modular-style injection
Line 422: The following listing shows what a test for modular injection might look like.
Line 423: const {
Line 424:   verifyPassword,
Line 425:   injectDependencies,
Line 426:   resetDependencies,
Line 427: } = require("./password-verifier-injectable");
Line 428: describe("password verifier", () => {
Line 429:   afterEach(resetDependencies);
Line 430:   describe("given logger and passing scenario", () => {
Line 431:     it("calls the logger with PASS", () => {
Line 432:       let logged = "";
Line 433:       const mockLog = { info: (text) => (logged = text) };
Line 434:       injectDependencies({ log: mockLog });
Line 435:       verifyPassword("anything", []);
Line 436:       expect(logged).toMatch(/PASSED/);
Line 437:     });
Line 438:   });
Line 439: });
Line 440: As long as we don’t forget to use the resetDependencies function after each test, we
Line 441: can now inject modules pretty easily for test purposes. The obvious main caveat is that
Line 442: this approach requires each module to expose inject and reset functions that can be
Line 443: used from the outside. This might or might not work with your current design limita-
Line 444: tions, but if it does, you can abstract them both into reusable functions and save your-
Line 445: self a lot of boilerplate code.
Line 446: 4.6
Line 447: Mocks in a functional style 
Line 448: Let’s jump into a few of the functional styles we can use to inject mocks into our code
Line 449: under test.
Line 450: 4.6.1
Line 451: Working with a currying style
Line 452: Let’s implement the currying technique introduced in chapter 3 to perform a more
Line 453: functional-style injection of our logger. In the following listing, we’ll use lodash, a
Line 454: library that facilitates functional programming in JavaScript, to get currying working
Line 455: without too much boilerplate code.
Line 456: const verifyPassword3 = _.curry((rules, logger, input) => {
Line 457:     const failed = rules
Line 458:         .map(rule => rule(input))
Line 459:         .filter(result => result === false);
Line 460: Listing 4.6
Line 461: Testing with modular injection
Line 462: Listing 4.7
Line 463: Applying currying to our function
Line 464: 
Line 465: --- 페이지 121 ---
Line 466: 93
Line 467: 4.6
Line 468: Mocks in a functional style
Line 469:     if (failed.length === 0) {
Line 470:         logger.info('PASSED');
Line 471:         return true;
Line 472:     }
Line 473:     logger.info('FAIL');
Line 474:     return false;
Line 475: });
Line 476: The only change is the call to _.curry on the first line, and closing it off at the end of
Line 477: the code block.
Line 478:  The following listing demonstrates what a test for this type of code might look like.
Line 479: describe("password verifier", () => {
Line 480:   describe("given logger and passing scenario", () => {
Line 481:     it("calls the logger with PASS", () => {
Line 482:       let logged = "";
Line 483:       const mockLog = { info: (text) => (logged = text) };
Line 484:       const injectedVerify = verifyPassword3([], mockLog);
Line 485:       // this partially applied function can be passed around
Line 486:       // to other places in the code
Line 487:       // without needing to inject the logger
Line 488:       injectedVerify("anything");
Line 489:       expect(logged).toMatch(/PASSED/);
Line 490:     });
Line 491:   });
Line 492: });
Line 493: Our test invokes the function with the first two arguments (injecting the rules and
Line 494: logger dependencies, effectively returning a partially applied function), and then
Line 495: invokes the returned function injectedVerify with the final input, thus showing the
Line 496: reader two things:
Line 497: How this function is meant to be used in real life
Line 498: What the dependencies are
Line 499: Other than that, it’s pretty much the same as in the previous test.
Line 500: 4.6.2
Line 501: Working with higher-order functions and not currying
Line 502: Listing 4.9 is another variation on the functional programming design. We’re using a
Line 503: higher-order function, but without currying. You can tell that the following code does
Line 504: not contain currying because we always need to send in all of the parameters as argu-
Line 505: ments to the function for it to be able to work correctly.
Line 506:  
Line 507:  
Line 508:  
Line 509: Listing 4.8
Line 510: Testing a curried function with dependency injection
Line 511: 
Line 512: --- 페이지 122 ---
Line 513: 94
Line 514: CHAPTER 4
Line 515: Interaction testing using mock objects
Line 516: const makeVerifier = (rules, logger) => {
Line 517:     return (input) => {             
Line 518:         const failed = rules
Line 519:             .map(rule => rule(input))
Line 520:             .filter(result => result === false);
Line 521:         if (failed.length === 0) {
Line 522:             logger.info('PASSED');
Line 523:             return true;
Line 524:         }
Line 525:         logger.info('FAIL');
Line 526:         return false;
Line 527:     };
Line 528: };
Line 529: This time I’m explicitly making a factory function that returns a preconfigured verifier
Line 530: function that already contains the rules and logger in its closure’s dependencies. 
Line 531:  Now let’s look at the test for this. The test needs to first call the makeVerifier factory
Line 532: function and then call the function that’s returned by that function (passVerify).
Line 533: describe("higher order factory functions", () => {
Line 534:   describe("password verifier", () => {
Line 535:     test("given logger and passing scenario", () => {
Line 536:       let logged = "";
Line 537:       const mockLog = { info: (text) => (logged = text) };
Line 538:       const passVerify = makeVerifier([], mockLog);      
Line 539:       passVerify("any input");    
Line 540:       expect(logged).toMatch(/PASSED/);
Line 541:     });
Line 542:   });
Line 543: });
Line 544: 4.7
Line 545: Mocks in an object-oriented style
Line 546: Now that we’ve covered some functional and modular styles, let’s look at the object-
Line 547: oriented styles. People coming from an object-oriented background will feel much
Line 548: more comfortable with this type of approach, and people coming from a functional
Line 549: background will hate it. But life is about accepting people’s differences.
Line 550: 4.7.1
Line 551: Refactoring production code for injection
Line 552: Listing 4.11 shows what this type of injection might look like in a class-based design in
Line 553: JavaScript. Classes have constructors, and we use the constructor to force the caller of
Line 554: the class to provide parameters. This is not the only way to accomplish that, but it’s
Line 555: very common and useful in an object-oriented design because it makes the requirement
Line 556: Listing 4.9
Line 557: Injecting a mock in a higher-order function
Line 558: Listing 4.10
Line 559: Testing using a factory function
Line 560: Returning a 
Line 561: preconfigured 
Line 562: verifier
Line 563: Calling the 
Line 564: factory 
Line 565: function
Line 566: Calling the 
Line 567: resulting function
Line 568: 
Line 569: --- 페이지 123 ---
Line 570: 95
Line 571: 4.7
Line 572: Mocks in an object-oriented style
Line 573: of those parameters explicit and practically undeniable in strongly typed languages
Line 574: such as Java or C, and when using TypeScript. We want to make sure whoever uses our
Line 575: code knows what is expected to configure it properly.
Line 576: class PasswordVerifier {
Line 577:   _rules;
Line 578:   _logger;
Line 579:   constructor(rules, logger) {
Line 580:     this._rules = rules;
Line 581:     this._logger = logger;
Line 582:   }
Line 583:   verify(input) {
Line 584:     const failed = this._rules
Line 585:         .map(rule => rule(input))
Line 586:         .filter(result => result === false);
Line 587:     if (failed.length === 0) {
Line 588:       this._logger.info('PASSED');
Line 589:       return true;
Line 590:     }
Line 591:     this._logger.info('FAIL');
Line 592:     return false;
Line 593:   }
Line 594: }
Line 595: This is just a standard class that takes a couple of constructor parameters and then
Line 596: uses them inside the verify function. The following listing shows what a test might
Line 597: look like. 
Line 598: describe("duck typing with function constructor injection", () => {
Line 599:   describe("password verifier", () => {
Line 600:     test("logger&passing scenario,calls logger with PASSED", () => {
Line 601:       let logged = "";
Line 602:       const mockLog = { info: (text) => (logged = text) };
Line 603:       const verifier = new PasswordVerifier([], mockLog);
Line 604:       verifier.verify("any input");
Line 605:       expect(logged).toMatch(/PASSED/);
Line 606:     });
Line 607:   });
Line 608: });   
Line 609: Mock injection is straightforward, much like with stubs, as we saw in the previous
Line 610: chapter. If we were to use properties rather than a constructor, it would mean that
Line 611: the dependencies are optional. With a constructor, we’re explicitly saying they’re not
Line 612: optional.
Line 613: Listing 4.11
Line 614: Class-based constructor injection
Line 615: Listing 4.12
Line 616: Injecting a mock logger as a constructor parameter
Line 617: 
Line 618: --- 페이지 124 ---
Line 619: 96
Line 620: CHAPTER 4
Line 621: Interaction testing using mock objects
Line 622:  In strongly typed languages like Java or C#, it’s common to extract the fake logger
Line 623: as a separate class, like so:
Line 624: class FakeLogger {
Line 625:   logged = "";
Line 626:   info(text) {
Line 627:     this.logged = text;
Line 628:   }
Line 629: }
Line 630: We simply implement the info function in the class, but instead of logging anything,
Line 631: we just save the value being sent as a parameter to the function in a publicly visible
Line 632: variable that we can assert again later in our test.
Line 633:  Notice that I didn’t call the fake object MockLogger or StubLogger but FakeLogger.
Line 634: This is so that I can reuse this class in multiple different tests. In some tests, it might
Line 635: be used as a stub, and in others it might be used as a mock object. I use the word
Line 636: “fake” to denote anything that isn’t real. Another common term for this sort of thing is
Line 637: “test double.” Fake is shorter, so I like it. 
Line 638:  In our tests, we’ll instantiate the class and send it over as a constructor parameter,
Line 639: and then we’ll assert on the logged variable of the class, like so:
Line 640: test("logger + passing scenario, calls logger with PASSED", () => {
Line 641:    let logged = "";
Line 642:    const mockLog = new FakeLogger();
Line 643:    const verifier = new PasswordVerifier([], mockLog);
Line 644:    verifier.verify("any input");
Line 645:    expect(mockLog.logged).toMatch(/PASSED/);
Line 646: });
Line 647: 4.7.2
Line 648: Refactoring production code with interface injection
Line 649: Interfaces play a large role in many object-oriented programs. They are one variation
Line 650: on the idea of polymorphism: allowing one or more objects to be replaced with one
Line 651: another as long as they implement the same interface. In JavaScript and other lan-
Line 652: guages like Ruby, interfaces are not needed, since the language allows for the idea of
Line 653: duck typing without needing to cast an object to a specific interface. I won’t touch
Line 654: here on the pros and cons of duck typing. You should be able to use either technique
Line 655: as you see fit, in the language of your choice. In JavaScript, we can turn to TypeScript
Line 656: to use interfaces. The compiler, or transpiler, we’ll use can help ensure that we are
Line 657: using types based on their signatures correctly.
Line 658:  Listing 4.13 shows three code files: the first describes a new ILogger interface, the
Line 659: second describes a SimpleLogger that implements that interface, and the third is our
Line 660: PasswordVerifier, which uses only the ILogger interface to get a logger instance.
Line 661: PasswordVerifier has no knowledge of the actual type of logger being injected. 
Line 662: 
Line 663: --- 페이지 125 ---
Line 664: 97
Line 665: 4.7
Line 666: Mocks in an object-oriented style
Line 667: export interface ILogger {    
Line 668:     info(text: string);       
Line 669: }                             
Line 670: //this class might have dependencies on files or network
Line 671: class SimpleLogger implements ILogger {   
Line 672:     info(text: string) {
Line 673:     }
Line 674: }
Line 675: export class PasswordVerifier {
Line 676:     private _rules: any[];
Line 677:     private _logger: ILogger;                      
Line 678:     constructor(rules: any[], logger: ILogger) {   
Line 679:         this._rules = rules;
Line 680:         this._logger = logger;                     
Line 681:     }
Line 682:     verify(input: string): boolean {
Line 683:         const failed = this._rules
Line 684:             .map(rule => rule(input))
Line 685:             .filter(result => result === false);
Line 686:         if (failed.length === 0) {
Line 687:             this._logger.info('PASSED');
Line 688:             return true;
Line 689:         }
Line 690:         this._logger.info('FAIL');
Line 691:         return false;
Line 692:     }
Line 693: }
Line 694: Notice that a few things have changed in the production code. I’ve added a new inter-
Line 695: face to the production code, and the existing logger now implements this interface.
Line 696: I’m changing the design to make the logger replaceable. Also, the PasswordVerifier
Line 697: class works with the interface instead of the SimpleLogger class. This allows me to
Line 698: replace the instance of the logger class with a fake one, instead of having a hard
Line 699: dependency on the real logger. 
Line 700:  The following listing shows what a test might look like in a strongly typed language,
Line 701: but with a handwritten fake object that implements the ILogger interface.
Line 702: class FakeLogger implements ILogger {
Line 703:     written: string;
Line 704:     info(text: string) {
Line 705:         this.written = text;
Line 706:     }
Line 707: }
Line 708: Listing 4.13
Line 709: Production code gets an ILogger interface
Line 710: Listing 4.14
Line 711: Injecting a handwritten mock ILogger 
Line 712: A new interface, 
Line 713: which is part of 
Line 714: production code
Line 715: The logger now 
Line 716: implements that 
Line 717: interface.
Line 718: The verifier
Line 719: now uses the
Line 720: interface.
Line 721: 
Line 722: --- 페이지 126 ---
Line 723: 98
Line 724: CHAPTER 4
Line 725: Interaction testing using mock objects
Line 726: describe('password verifier with interfaces', () => {
Line 727:     test('verify, with logger, calls logger', () => {
Line 728:         const mockLog = new FakeLogger();
Line 729:         const verifier = new PasswordVerifier([], mockLog);
Line 730:         verifier.verify('anything');
Line 731:         expect(mockLog.written).toMatch(/PASS/);
Line 732:     });
Line 733: });
Line 734: In this example, I’ve created a handwritten class called FakeLogger. All it does is over-
Line 735: ride the one method in the ILogger interface and save the text parameter for future
Line 736: assertion. We then expose this value as a field in the written class. Once this value is
Line 737: exposed, we can verify that the fake logger was called by checking that field.
Line 738:  I’ve done this manually because I wanted you to see that even in object-oriented
Line 739: land, the patterns repeat themselves. Instead of having a mock function, we now have a
Line 740: mock object, but the code and test work just like the previous examples. 
Line 741: 4.8
Line 742: Dealing with complicated interfaces
Line 743: What happens when the interface is more complicated, such as when it has more than
Line 744: one or two functions in it, or more than one or two parameters in each function?
Line 745: 4.8.1
Line 746: Example of a complicated interface
Line 747: Listing 4.15 is an example of such a complicated interface, and of the production
Line 748: code verifier that uses the complicated logger, injected as an interface. The ICompli-
Line 749: catedLogger interface has four functions, each with one or more parameters. Every
Line 750: function would need to be faked in our tests, and that can lead to complexity and
Line 751: maintainability problems in our code and tests.
Line 752: export interface IComplicatedLogger {   
Line 753:     info(text: string)
Line 754:     debug(text: string, obj: any)
Line 755: Interface naming conventions
Line 756: I’m using the naming convention of prefixing the logger interface with an “I” because
Line 757: it’s going to be used for polymorphic reasons (i.e., I’m using it to abstract a role in
Line 758: the system). This is not always the case for interface naming in TypeScript, such as
Line 759: when we use interfaces to define the structure of a set of parameters (basically using
Line 760: them as strongly typed structures). In that case, naming without an “I” makes sense
Line 761: to me. 
Line 762: For now, think of it like this: If you’re going to implement it more than once, you
Line 763: should prefix it with an “I” to make the expected use of the interface more explicit. 
Line 764: Listing 4.15
Line 765: Working with a more complicated interface (production code)
Line 766: A new interface, which is 
Line 767: part of production code
Line 768: 
Line 769: --- 페이지 127 ---
Line 770: 99
Line 771: 4.8
Line 772: Dealing with complicated interfaces
Line 773:     warn(text: string)
Line 774:     error(text: string, location: string, stacktrace: string)
Line 775: }
Line 776: export class PasswordVerifier2 {
Line 777:     private _rules: any[];
Line 778:     private _logger: IComplicatedLogger;                     
Line 779:     constructor(rules: any[], logger: IComplicatedLogger) {  
Line 780:         this._rules = rules;
Line 781:         this._logger = logger;
Line 782:     }
Line 783: ...
Line 784: }
Line 785: As you can see, the new IComplicatedLogger interface will be part of production
Line 786: code, which will make the logger replaceable. I’m leaving off the implementation of a
Line 787: real logger, because it’s not relevant for our examples. That’s the benefit of abstract-
Line 788: ing away things with an interface: we don’t need to reference them directly. Also
Line 789: notice that the type of parameter expected in the class’s constructor is that of the
Line 790: IComplicatedLogger interface. This allows me to replace the instance of the logger
Line 791: class with a fake one, just like we did before.
Line 792: 4.8.2
Line 793: Writing tests with complicated interfaces
Line 794: Here’s what the test looks like. It has to override each and every interface function,
Line 795: which creates long and annoying boilerplate code.
Line 796: describe("working with long interfaces", () => {
Line 797:   describe("password verifier", () => {
Line 798:     class FakeComplicatedLogger            
Line 799:         implements IComplicatedLogger {    
Line 800:       infoWritten = "";
Line 801:       debugWritten = "";
Line 802:       errorWritten = "";
Line 803:       warnWritten = "";
Line 804:       debug(text: string, obj: any) {
Line 805:         this.debugWritten = text;
Line 806:       }
Line 807:       error(text: string, location: string, stacktrace: string) {
Line 808:         this.errorWritten = text;
Line 809:       }
Line 810:       info(text: string) {
Line 811:         this.infoWritten = text;
Line 812:       }
Line 813:       warn(text: string) {
Line 814:         this.warnWritten = text;
Line 815: Listing 4.16
Line 816: Test code with a complicated logger interface
Line 817: The class now 
Line 818: works with the 
Line 819: new interface.
Line 820: A fake logger class that 
Line 821: implements the new interface
Line 822: 
Line 823: --- 페이지 128 ---
Line 824: 100
Line 825: CHAPTER 4
Line 826: Interaction testing using mock objects
Line 827:       }
Line 828:     }
Line 829:     ...
Line 830:     test("verify passing, with logger, calls logger with PASS", () => {
Line 831:       const mockLog = new FakeComplicatedLogger();
Line 832:       const verifier = new PasswordVerifier2([], mockLog);
Line 833:       verifier.verify("anything");
Line 834:       expect(mockLog.infoWritten).toMatch(/PASSED/);
Line 835:     });
Line 836:     test("A more JS oriented variation on this test", () => {
Line 837:       const mockLog = {} as IComplicatedLogger;
Line 838:       let logged = "";
Line 839:       mockLog.info = (text) => (logged = text);
Line 840:       const verifier = new PasswordVerifier2([], mockLog);
Line 841:       verifier.verify("anything");
Line 842:       expect(logged).toMatch(/PASSED/);
Line 843:     });
Line 844:   });
Line 845: });
Line 846: Here, we’re declaring, again, a fake logger class (FakeComplicatedLogger) that imple-
Line 847: ments the IComplicatedLogger interface. Look at how much boilerplate code we
Line 848: have. This will be especially true if we’re working in strongly typed object-oriented lan-
Line 849: guages such as Java, C#, or C++. There are ways around all this boilerplate code, which
Line 850: we’ll touch on in the next chapter. 
Line 851: 4.8.3
Line 852: Downsides of using complicated interfaces directly
Line 853: There are other downsides to using long, complicated interfaces in our tests:
Line 854: If we’re saving arguments being sent in manually, it’s more cumbersome to ver-
Line 855: ify multiple arguments across multiple methods and calls. 
Line 856: It’s likely that we are depending on third-party interfaces instead of internal
Line 857: ones, and this will end up making our tests more brittle as time goes by. 
Line 858: Even if we are depending on internal interfaces, long interfaces have more rea-
Line 859: sons to change, and now so do our tests. 
Line 860: What does this mean for us? I highly recommend using only fake interfaces that meet
Line 861: both of these conditions:
Line 862: You control the interfaces (they are not made by a third party).
Line 863: They are adapted to the needs of your unit of work or component. 
Line 864: 
Line 865: --- 페이지 129 ---
Line 866: 101
Line 867: 4.9
Line 868: Partial mocks
Line 869: 4.8.4
Line 870: The interface segregation principle
Line 871: The second of the preceding conditions might need a bit of explanation. It relates
Line 872: to the interface segregation principle (ISP; https://en.wikipedia.org/wiki/Interface_
Line 873: segregation_principle). ISP means that if we have an interface that contains more
Line 874: functionality than we require, we should create a small, simpler adapter interface that
Line 875: contains just the functionality we need, preferably with fewer functions, better names,
Line 876: and fewer parameters. 
Line 877:  This will end up making our tests much simpler. By abstracting away the real
Line 878: dependencies, we won’t need to change our tests when the complicated interfaces
Line 879: change—only a single adapter class file somewhere. We’ll see an example of this in
Line 880: chapter 5.
Line 881: 4.9
Line 882: Partial mocks
Line 883: It’s possible, in JavaScript and in most other languages and associated test frameworks,
Line 884: to take over existing objects and functions and “spy” on them. By spying on them, we
Line 885: can later check if they were called, how many times, and with which arguments. 
Line 886:  This essentially can turn parts of a real object into mock functions, while keeping
Line 887: the rest of the object as a real object. This can create more complicated tests that are
Line 888: more brittle, but it can sometimes be a viable option, especially if you’re dealing with
Line 889: legacy code (see chapter 12 for more on legacy code). 
Line 890: 4.9.1
Line 891: A functional example of a partial mock
Line 892: The following listing shows what such a test might look like. We create the real logger,
Line 893: and then we simply override one of its existing real functions using a custom function.
Line 894: describe("password verifier with interfaces", () => {
Line 895:   test("verify, with logger, calls logger", () => {
Line 896:     const testableLog: RealLogger = new RealLogger();   
Line 897:     let logged = "";
Line 898:     testableLog.info = (text) => (logged = text);   
Line 899:     const verifier = new PasswordVerifier([], testableLog);
Line 900:     verifier.verify("any input");
Line 901:     expect(logged).toMatch(/PASSED/);
Line 902:   });
Line 903: });
Line 904: In this test, I’m instantiating a RealLogger, and in the next line I’m replacing one of
Line 905: its existing functions with a fake one. More specifically, I’m using a mock function that
Line 906: allows me to track its latest invocation parameter using a custom variable.
Line 907:  The important part here is that the testableLog variable is a partial mock. That
Line 908: means that at least some of its internal implementation is not fake and might have real
Line 909: dependencies and logic in it.
Line 910: Listing 4.17
Line 911: A partial mock example 
Line 912: Instantiating a 
Line 913: real logger
Line 914: Mocking one of 
Line 915: its functions
Line 916: 
Line 917: --- 페이지 130 ---
Line 918: 102
Line 919: CHAPTER 4
Line 920: Interaction testing using mock objects
Line 921:  Sometimes it makes sense to use partial mocks, especially when you’re working
Line 922: with legacy code and you might need to isolate some existing code from its dependen-
Line 923: cies. I’ll touch more on that in chapter 12.
Line 924: 4.9.2
Line 925: An object-oriented partial mock example
Line 926: One object-oriented version of a partial mock uses inheritance to override functions
Line 927: from real classes so that we can verify they were called. The following listing shows
Line 928: how we can do this using inheritance and overrides in JavaScript.
Line 929: class TestableLogger extends RealLogger {    
Line 930:   logged = "";
Line 931:   info(text) {             
Line 932:     this.logged = text;    
Line 933:   }                        
Line 934:   // the error() and debug() functions
Line 935:   // are still "real"
Line 936: }
Line 937: describe("partial mock with inheritance", () => {
Line 938:   test("verify with logger, calls logger", () => {
Line 939:     const mockLog: TestableLogger = new TestableLogger();
Line 940:     const verifier = new PasswordVerifier([], mockLog);
Line 941:     verifier.verify("any input");
Line 942:     expect(mockLog.logged).toMatch(/PASSED/);
Line 943:   });
Line 944: });
Line 945: I inherit from the real logger class in my tests and then use the inherited class, not the
Line 946: original class, in my tests. This technique is commonly called Extract and Override,
Line 947: and you can find more about this in Michael Feathers’ book Working Effectively with
Line 948: Legacy Code (Pearson, 2004). 
Line 949:  Note that I’ve named the fake logger class “TestableXXX” because it’s a testable
Line 950: version of real production code, containing a mix of fake and real code, and this
Line 951: convention helps me make this explicit for the reader. I also put the class right
Line 952: alongside my tests. My production code doesn’t need to know that this class exists.
Line 953: This Extract and Override style requires that my class in production code allows
Line 954: inheritance and that the function allows overriding. In JavaScript this is less of an
Line 955: issue, but in Java and C# these are explicit design choices that need to be made
Line 956: (although there are frameworks that allow us to circumvent this rule; we’ll discuss
Line 957: them in the next chapter).
Line 958:  In this scenario, we’re inheriting from a class that we’re not testing directly (Real-
Line 959: Logger). We use that class to test another class (PasswordVerifier). However, this
Line 960: technique can be used quite effectively to isolate and stub or mock single functions
Line 961: Listing 4.18
Line 962: An object-oriented partial mock example 
Line 963: Inheriting from 
Line 964: the real logger
Line 965: Overriding one 
Line 966: of its functions
Line 967: 
Line 968: --- 페이지 131 ---
Line 969: 103
Line 970: Summary
Line 971: from classes that you’re directly testing. We’ll touch more on that later in the book
Line 972: when we talk about legacy code and refactoring techniques.
Line 973: Summary
Line 974: Interaction testing is a way to check how a unit of work interacts with its outgoing
Line 975: dependencies: what calls were made and with which parameters. Interaction
Line 976: testing relates to the third type of exit points: a third-party module, object, or
Line 977: system. (The first two types are a return value and a state change.)
Line 978: To do interaction testing, you should use mocks, which are test doubles that replace
Line 979: outgoing dependencies. Stubs replace incoming dependencies. You should ver-
Line 980: ify interactions with mocks in tests, but not with stubs. Unlike with mocks, inter-
Line 981: actions with stubs are implementation details and shouldn't be checked.
Line 982: It’s OK to have multiple stubs in a test, but you don’t usually want to have more
Line 983: than a single mock per test, because that means you’re testing more than one
Line 984: requirement in a single test.
Line 985: Just like with stubs, there are multiple ways to inject a mock into a unit of work:
Line 986: – Standard—By introducing a parameter
Line 987: – Functional—Using a partial application or factory functions
Line 988: – Modular—Abstracting the module dependency
Line 989: – Object-oriented—Using an untyped object (in languages like JavaScript) or a
Line 990: typed interface (in TypeScript)
Line 991: In JavaScript, a complicated interface can be implemented partially, which
Line 992: helps reduce the amount of boilerplate. There’s also the option of using partial
Line 993: mocks, where you inherit from a real class and replace only some of its methods
Line 994: with fakes.
