Line 1: 
Line 2: --- 페이지 89 ---
Line 3: 61
Line 4: Breaking dependencies
Line 5: with stubs
Line 6: In the previous chapter, you wrote your first unit test using Jest, and we looked
Line 7: more at the maintainability of the test itself. The scenario was pretty simple, and
Line 8: more importantly, it was completely self-contained. The Password Verifier had no
Line 9: reliance on outside modules, and we could focus on its functionality without worry-
Line 10: ing about other things that might interfere with it. 
Line 11:  In that chapter, we used the first two types of exit points for our examples:
Line 12: return value exit points and state-based exit points. In this chapter, we’ll talk about
Line 13: the final type—calling a third party. This chapter will also present a new require-
Line 14: ment—having your code rely on time. We’ll look at two different approaches to
Line 15: handling it—refactoring our code and monkey-patching it without refactoring.
Line 16:  The reliance on outside modules or functions can and will make it harder to
Line 17: write a test and to make the test repeatable, and it can also cause tests to be flaky.
Line 18: This chapter covers
Line 19: Types of dependencies—mocks, stubs, and more
Line 20: Reasons to use stubs
Line 21: Functional injection techniques
Line 22: Modular injection techniques
Line 23: Object-oriented injection techniques
Line 24: 
Line 25: --- 페이지 90 ---
Line 26: 62
Line 27: CHAPTER 3
Line 28: Breaking dependencies with stubs
Line 29: We call the external things that we rely on in our code dependencies. I’ll define them
Line 30: more thoroughly later in the chapter. These dependencies could include things like
Line 31: time, async execution, using the filesystem, or using the network, or they could simply
Line 32: involve using something that is very difficult to configure or that may be time consum-
Line 33: ing to execute.
Line 34: 3.1
Line 35: Types of dependencies
Line 36: In my experience, there are two main types of dependencies that our unit of work
Line 37: can use:
Line 38: Outgoing dependencies—Dependencies that represent an exit point of our unit of
Line 39: work, such as calling a logger, saving something to a database, sending an email,
Line 40: notifying an API or a webhook that something has happened, etc. Notice these
Line 41: are all verbs: “calling,” “sending,” and “notifying.” They are flowing outward from
Line 42: the unit of work in a sort of fire-and-forget scenario. Each represents an exit
Line 43: point, or the end of a specific logical flow in a unit of work.
Line 44: Incoming dependencies—Dependencies that are not exit points. These do not rep-
Line 45: resent a requirement on the eventual behavior of the unit of work. They are
Line 46: merely there to provide test-specific specialized data or behavior to the unit of
Line 47: work, such as a database query’s result, the contents of a file on the filesystem, a
Line 48: network response, etc. Notice that these are all passive pieces of data that flow
Line 49: inward to the unit of work as the result of a previous operation. 
Line 50: Figure 3.1 shows these side by side.
Line 51: Test
Line 52: Entry point
Line 53: Exit point
Line 54: Data
Line 55: or behavior
Line 56: Dependency
Line 57: Unit
Line 58: of
Line 59: work
Line 60: Test
Line 61: Entry point
Line 62: Exit point
Line 63: Dependency
Line 64: Unit
Line 65: of
Line 66: work
Line 67: Outgoing dependency
Line 68: Incoming dependency
Line 69: Figure 3.1
Line 70: On the left, an exit point is implemented as invoking a dependency. On the right, the dependency 
Line 71: provides indirect input or behavior and is not an exit point.
Line 72: 
Line 73: --- 페이지 91 ---
Line 74: 63
Line 75: 3.1
Line 76: Types of dependencies
Line 77: Some dependencies can be both incoming and outgoing—in some tests they will rep-
Line 78: resent exit points, and in other tests they will be used to simulate data coming into the
Line 79: application. These shouldn’t be very common, but they do exist, such as an external
Line 80: API that returns a success/fail response for an outgoing message.
Line 81:  With these types of dependencies in mind, let’s look at how the book xUnit Test Pat-
Line 82: terns defines the various patterns for things that look like other things in tests.
Line 83: Table 3.1 lists my thoughts about some patterns from the book’s website at http://
Line 84: mng.bz/n1WK.
Line 85: Here’s another way to think about this for the rest of this book:
Line 86: Stubs break incoming dependencies (indirect inputs). Stubs are fake modules,
Line 87: objects, or functions that provide fake behavior or data into the code under test.
Line 88: We do not assert against them. We can have many stubs in a single test.
Line 89: Mocks break outgoing dependencies (indirect outputs or exit points). Mocks
Line 90: are fake modules, objects, or functions that we assert were called in our tests. A
Line 91: mock represents an exit point in a unit test. Because of this, it is recommended
Line 92: that you have no more than a single mock per test.
Line 93: Unfortunately, in many shops you’ll hear the word “mock” thrown around as a catch-
Line 94: all term for both stubs and mocks. Phrases like “we’ll mock this out” or “we have a
Line 95: mock database” can really create confusion. There is a huge difference between stubs
Line 96: Table 3.1
Line 97: Clarifying terminology around stubs and mocks
Line 98: Category
Line 99: Pattern
Line 100: Purpose
Line 101: Uses
Line 102: Test double
Line 103: Generic name for stubs and 
Line 104: mocks
Line 105: I also use the term fake.
Line 106: Stub
Line 107: Dummy object
Line 108: Used to specify the values to 
Line 109: be used in tests when the only 
Line 110: usage is as irrelevant argu-
Line 111: ments of SUT method calls
Line 112: Send as a parameter to the 
Line 113: entry point or as the arrange 
Line 114: part of the AAA pattern.
Line 115: Test stub
Line 116: Used to verify logic inde-
Line 117: pendently when it depends on 
Line 118: indirect inputs from other soft-
Line 119: ware components
Line 120: Inject as a dependency, and 
Line 121: configure it to return specific 
Line 122: values or behavior into the SUT.
Line 123: Mock
Line 124: Test spy
Line 125: Used to verify logic inde-
Line 126: pendently when it has indirect 
Line 127: outputs to other software com-
Line 128: ponents
Line 129: Override a single function on a 
Line 130: real object, and verify that the 
Line 131: fake function was called as 
Line 132: expected.
Line 133: Mock object
Line 134: Used to verify logic inde-
Line 135: pendently when it depends on 
Line 136: indirect outputs to other soft-
Line 137: ware components
Line 138: Inject the fake as a depen-
Line 139: dency into the SUT, and verify 
Line 140: that the fake was called as 
Line 141: expected.
Line 142: 
Line 143: --- 페이지 92 ---
Line 144: 64
Line 145: CHAPTER 3
Line 146: Breaking dependencies with stubs
Line 147: and mocks (one should really only be used once in a test), and we should use the right
Line 148: terms to ensure it’s clear what the other person is referring to. 
Line 149:  When in doubt, use the term “test double” or “fake.” Often, a single fake depen-
Line 150: dency can be used as a stub in one test, and it can be used as a mock in another test.
Line 151: We’ll see an example of this later on. 
Line 152: This might seem like a whole lot of information at once. I’ll dive deep into these defi-
Line 153: nitions throughout this chapter. Let’s take a small bite and start with stubs.
Line 154: 3.2
Line 155: Reasons to use stubs
Line 156: What if we’re faced with the task of testing a piece of code like the following?
Line 157: const moment = require('moment');
Line 158: const SUNDAY = 0, SATURDAY = 6;
Line 159: const verifyPassword = (input, rules) => {
Line 160:     const dayOfWeek = moment().day();
Line 161:     if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
Line 162:         throw Error("It's the weekend!");
Line 163:     }
Line 164:     //more code goes here...
Line 165:     //return list of errors found..
Line 166:     return [];
Line 167: };
Line 168: Our password verifier has a new dependency: it can’t work on weekends. Go figure. Spe-
Line 169: cifically, the module has a direct dependency on moment.js, which is a very common
Line 170: date/time wrapper for JavaScript. Working with dates directly in JavaScript is not a pleas-
Line 171: ant experience, so we can assume many shops out there have something like this. 
Line 172: XUnit test patterns and naming things
Line 173: xUnit Test Patterns: Refactoring Test Code by Gerard Meszaros (Addison-Wesley,
Line 174: 2007) is a classic pattern reference book for unit testing. It defines patterns for
Line 175: things you fake in your tests in at least five ways. Once you’ve gotten a feel for the
Line 176: three types I mention here, I encourage you to take a look at the extra details that
Line 177: book provides. 
Line 178: Note that xUnit Test Patterns has a definition for the word “fake”: “Replace a compo-
Line 179: nent that the system under test (SUT) depends on with a much lighter-weight imple-
Line 180: mentation.” For example, you might use an in-memory database instead of a full-
Line 181: fledged production instance. 
Line 182: I still consider this type of test double a “stub,” and I use the word “fake” to call out
Line 183: anything that isn’t real, much like the term “test double,” but “fake” is shorter and
Line 184: easier on the tongue.
Line 185: Listing 3.1
Line 186: verifyPassword using time
Line 187: 
Line 188: --- 페이지 93 ---
Line 189: 65
Line 190: 3.2
Line 191: Reasons to use stubs
Line 192:  How does this direct use of a time-related library affect our unit tests? The unfor-
Line 193: tunate issue here is that this direct dependency forces our tests, given no direct way
Line 194: to affect date and time inside our application under test, to take into account the
Line 195: correct date and time. The following listing shows an unfortunate test that only runs
Line 196: on weekends.
Line 197: const moment = require('moment');
Line 198: const {verifyPassword} = require("./password-verifier-time00");
Line 199: const SUNDAY = 0, SATURDAY = 6, MONDAY = 2;
Line 200: describe('verifier', () => {
Line 201:     const TODAY = moment().day();
Line 202:     //test is always executed, but might not do anything
Line 203:     test('on weekends, throws exceptions', () => {
Line 204:         if ([SATURDAY, SUNDAY].includes(TODAY)) {    
Line 205:             expect(()=> verifyPassword('anything',[]))
Line 206:                 .toThrow("It's the weekend!");
Line 207:         }
Line 208:     });
Line 209:     //test is not even executed on week days
Line 210:     if ([SATURDAY, SUNDAY].includes(TODAY)) {       
Line 211:         test('on a weekend, throws an error', () => {
Line 212:             expect(()=> verifyPassword('anything', []))
Line 213:                 .toThrow("It's the weekend!");
Line 214:         });
Line 215:     }
Line 216: });
Line 217: The preceding listing includes two variations on the same test. One checks for the cur-
Line 218: rent date inside the test, and the other has the check outside the test, which means the
Line 219: test never even executes unless it’s the weekend. This is bad. 
Line 220:  Let’s revisit one of the good test qualities mentioned in chapter 1, consistency:
Line 221: Every time I run a test, it is the same exact test that I ran before. The values being used
Line 222: do not change. The asserts do not change. If no code has changed (in test or produc-
Line 223: tion code), then the test should provide the exact same result as previous runs.
Line 224:  The second test sometimes doesn’t even run. That’s a good enough reason to use a
Line 225: fake to break the dependency right there. Furthermore, we can’t simulate a weekend
Line 226: or a weekday, which gives us more than enough incentive to redesign the code under
Line 227: test so it’s a bit more injectable for dependencies.
Line 228:  But wait, there’s more. Tests that use time can often be flaky. They only fail
Line 229: sometimes, without anything but the time changing. This test is a prime candidate
Line 230: for this behavior, because we’ll only get feedback on one of its two states when we
Line 231: run it locally. If you want to know how it behaves on a weekend, just wait a couple of
Line 232: days. Ugh.
Line 233: Listing 3.2
Line 234: Initial unit tests for verifyPassword
Line 235: Checking the 
Line 236: date inside 
Line 237: the test
Line 238: Checking the 
Line 239: date outside 
Line 240: the test
Line 241: 
Line 242: --- 페이지 94 ---
Line 243: 66
Line 244: CHAPTER 3
Line 245: Breaking dependencies with stubs
Line 246:  Tests might become flaky due to edge cases that affect variables that are not under
Line 247: our control in the test. Common examples are network issues during end-to-end testing,
Line 248: database connectivity issues, or various server issues. When this happens, it’s easy to
Line 249: dismiss the test failure by saying “just run it again” or “It’s OK. It’s just [insert variabil-
Line 250: ity issue here].”
Line 251: 3.3
Line 252: Generally accepted design approaches to stubbing
Line 253: In the next few sections, we’ll discuss several common forms of injecting stubs into
Line 254: our units of work. First, we’ll discuss basic parameterization as a first step, then we’ll
Line 255: jump into the following approaches:
Line 256: Functional approaches
Line 257: – Function as parameter
Line 258: – Partial application (currying)
Line 259: – Factory functions 
Line 260: – Constructor functions 
Line 261: Modular approach
Line 262: – Module injection
Line 263: Object-oriented approaches
Line 264: – Class constructor injection
Line 265: – Object as parameter (aka duck typing)
Line 266: – Common interface as parameter (for this we’ll use TypeScript)
Line 267: We’ll tackle each of these by starting with the simple case of controlling time in our
Line 268: tests.
Line 269: 3.3.1
Line 270: Stubbing out time with parameter injection
Line 271: I can think of at least two good reasons to control time based on what we’ve covered
Line 272: so far:
Line 273: To remove the variability from our tests
Line 274: To easily simulate any time-related scenario we’d like to test our code with
Line 275: Here’s the simplest refactoring I can think of that makes things a bit more repeatable.
Line 276: Let’s add a currentDay parameter to our function to specify the current date. This will
Line 277: remove the need to use the moment.js module in our function, and it will put that
Line 278: responsibility on the caller of the function. That way, in our tests, we can determine
Line 279: the time in a hardcoded manner and make the test and the function repeatable and
Line 280: consistent. The following listing shows an example of such a refactoring.
Line 281: const verifyPassword2 = (input, rules, currentDay) => {
Line 282:     if ([SATURDAY, SUNDAY].includes(currentDay)) {
Line 283:         throw Error("It's the weekend!");
Line 284: Listing 3.3
Line 285: verifyPassword with a currentDay parameter
Line 286: 
Line 287: --- 페이지 95 ---
Line 288: 67
Line 289: 3.3
Line 290: Generally accepted design approaches to stubbing
Line 291:     }
Line 292:     //more code goes here...
Line 293:     //return list of errors found..
Line 294:     return [];
Line 295: };
Line 296: const SUNDAY = 0, SATURDAY = 6, MONDAY = 1;
Line 297: describe('verifier2 - dummy object', () => {
Line 298:     test('on weekends, throws exceptions', () => {
Line 299:         expect(() => verifyPassword2('anything',[],SUNDAY ))
Line 300:             .toThrow("It's the weekend!");
Line 301:     });
Line 302: });
Line 303: By adding the currentDay parameter, we’re essentially giving control over time to the
Line 304: caller of the function (our test). What we’re injecting is formally called a “dummy”—
Line 305: it’s just a piece of data with no behavior—but we can call it a “stub” from now on. 
Line 306:  This is approach is a form of Dependency Inversion. It seems the term “Inversion of
Line 307: Control” first came up in Johnson and Foote’s paper “Designing Reusable Classes,”
Line 308: published by the Journal of Object-Oriented Programming in 1988. The term “Dependency
Line 309: Inversion” is also one of the SOLID patterns described by Robert C. Martin in 2000, in
Line 310: his “Design Principles and Design Patterns” paper. I’ll talk more about higher-level
Line 311: design considerations in chapter 8. 
Line 312:  Adding this parameter is a simple refactoring, but it’s quite effective. It provides a
Line 313: couple of nice benefits other than consistency in the test:
Line 314: We can now easily simulate any day we want.
Line 315: The code under test is not responsible for managing time imports, so it has one
Line 316: less reason to change if we ever use a different time library.
Line 317: We’re doing “dependency injection” of time into our unit of work. We’ve changed the
Line 318: design of the entry point to use a day value as a parameter. The function is now “pure”
Line 319: by functional programming standards in that it has no side effects. Pure functions
Line 320: have built-in injections of all of their dependencies, which is one of the reasons you’ll
Line 321: find functional programming designs are typically much easier to test.
Line 322:  It might feel weird to call the currentDay parameter a stub if it’s just a day integer
Line 323: value, but based on the definitions from xUnit Test Patterns, we can say that this is a
Line 324: “dummy” value, and as far as I’m concerned, it falls into the “stub” category. It does
Line 325: not have to be complex in order to be a stub. It just has to be under our control. It’s a
Line 326: stub because we are using it to simulate some input or behavior being passed into the
Line 327: unit under test. Figure 3.2 shows this visually.
Line 328: 
Line 329: --- 페이지 96 ---
Line 330: 68
Line 331: CHAPTER 3
Line 332: Breaking dependencies with stubs
Line 333: 3.3.2
Line 334: Dependencies, injections, and control
Line 335: Table 3.2 recaps some important terms we’ve discussed and are about to use through-
Line 336: out the rest of the chapter.
Line 337: Table 3.2
Line 338: Terminology used in this chapter
Line 339: Dependencies
Line 340: The things that make our testing lives and code maintainability difficult, since we can-
Line 341: not control them from our tests. Examples include time, the filesystem, the network, 
Line 342: random values, and more.
Line 343: Control
Line 344: The ability to instruct a dependency how to behave. Whoever is creating the dependen-
Line 345: cies is said to be in control of them, since they have the ability to configure them 
Line 346: before they are used in the code under test. 
Line 347: In listing 3.1, our test does not have control over time because the module under test 
Line 348: has control over it. The module has chosen to always use the current date and time. This 
Line 349: forces the test to do the exact same thing, and thus we lose consistency in our tests. 
Line 350: In listing 3.3, we have gained access to the dependency by inverting the control over it 
Line 351: via the currentDay parameter. Now the test has control over the time and can decide 
Line 352: to use a hardcoded time. The module under test has to use the time provided, which 
Line 353: makes things much easier for our test.
Line 354: Inversion of 
Line 355: control
Line 356: Designing the code to remove the responsibility of creating the dependency internally, 
Line 357: and externalizing it instead. Listing 3.3 shows one way of doing this with parameter 
Line 358: injection.
Line 359: Dependency 
Line 360: injection
Line 361: The act of sending a dependency through the design interface to be used internally by a 
Line 362: piece of code. The place where you inject the dependency is the injection point. In our 
Line 363: case, we are using a parameter injection point. Another word for this place where we 
Line 364: can inject things is a seam.
Line 365: Seam
Line 366: Pronounced “s-ee-m,” and coined by Michael Feathers in his book Working Effectively 
Line 367: with Legacy Code (Pearson, 2004).
Line 368: Seams are where two pieces of software meet and something else can be injected. 
Line 369: They are a place where you can alter behavior in your program without editing in that 
Line 370: place. Examples include parameters, functions, module loaders, function rewriting, 
Line 371: and, in the object-oriented world, class interfaces, public virtual methods, and more.
Line 372: verify(input, rules, dayStub)
Line 373: Return value
Line 374: Test
Line 375: Stub
Line 376: Time
Line 377: Figure 3.2
Line 378: Injecting a stub 
Line 379: for a time dependency
Line 380: 
Line 381: --- 페이지 97 ---
Line 382: 69
Line 383: 3.4
Line 384: Functional injection techniques
Line 385: Seams in production code play an important role in the maintainability and readabil-
Line 386: ity of unit tests. The easier it is to change and inject behavior or custom data into the
Line 387: code under test, the easier it will be to write, read, and later on maintain the test as
Line 388: the production code changes. I’ll talk more about some patterns and antipatterns
Line 389: related to designing code in chapter 8.
Line 390: 3.4
Line 391: Functional injection techniques
Line 392: At this point, we might not be happy with our design choice. Adding a parameter did
Line 393: solve the dependency issue at the function level, but now every caller will need to
Line 394: know how to handle dates in some way. It feels a bit too chatty. 
Line 395:  JavaScript enables two major styles of programming—functional and object-
Line 396: oriented—so I’ll show approaches in both styles when it makes sense, and you can
Line 397: pick and choose what works best in your situation.
Line 398:  There isn’t a single way to design something. Functional programming proponents
Line 399: will argue for the simplicity, clarity, and provability of the functional style, but it does
Line 400: come with a learning curve. For that reason alone, it is wise to learn both approaches
Line 401: so that you can apply whichever works best for the team you’re working with. Some
Line 402: teams will lean more toward object-oriented designs because they feel more comfort-
Line 403: able with that. Others will lean towards functional designs. I’d argue that the patterns
Line 404: remain largely the same; we just translate them to different styles. 
Line 405: 3.4.1
Line 406: Injecting a function
Line 407: The following listing shows a different refactoring for the same problem: instead of a
Line 408: data object, we’re expecting a function as the parameter. That function returns the
Line 409: date object.
Line 410: const verifyPassword3 = (input, rules, getDayFn) => {
Line 411:     const dayOfWeek = getDayFn();
Line 412:     if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
Line 413:         throw Error("It's the weekend!");
Line 414:     }
Line 415:     //more code goes here...
Line 416:     //return list of errors found..
Line 417:     return [];
Line 418: };
Line 419: The associated test is shown in the following listing.
Line 420: describe('verifier3 - dummy function', () => {
Line 421:     test('on weekends, throws exceptions', () => {
Line 422:         const alwaysSunday = () => SUNDAY;
Line 423:         expect(()=> verifyPassword3('anything',[], alwaysSunday))
Line 424:             .toThrow("It's the weekend!");
Line 425:     });
Line 426: Listing 3.4
Line 427: Dependency injection with a function
Line 428: Listing 3.5
Line 429: Testing with function injection
Line 430: 
Line 431: --- 페이지 98 ---
Line 432: 70
Line 433: CHAPTER 3
Line 434: Breaking dependencies with stubs
Line 435: There’s very little difference from the previous test, but using a function as a parame-
Line 436: ter is a valid way to do injection. In other scenarios, it’s also a great way to enable spe-
Line 437: cial behavior, such as simulating special cases or exceptions in your code under test.
Line 438: 3.4.2
Line 439: Dependency injection via partial application
Line 440: Factory functions or methods (a subcategory of “higher-order functions”) are func-
Line 441: tions that return other functions, preconfigured with some context. In our case, the
Line 442: context can be the list of rules and the current day function. We then get back a new
Line 443: function that we can trigger with only a string input, and it will use the rules and get-
Line 444: Day() function configured in its creation. 
Line 445:  The code in the following listing essentially turns the factory function into the
Line 446: arrange part of the test, and calls the returned function into the act part. Quite lovely.
Line 447: const SUNDAY = 0, . . . FRIDAY=5, SATURDAY = 6;
Line 448: const makeVerifier = (rules, dayOfWeekFn) => {
Line 449:     return function (input) {
Line 450:         if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
Line 451:             throw new Error("It's the weekend!");
Line 452:         }
Line 453:         //more code goes here..
Line 454:     };
Line 455: };
Line 456: describe('verifier', () => {
Line 457:     test('factory method: on weekends, throws exceptions', () => {
Line 458:         const alwaysSunday = () => SUNDAY;
Line 459:         const verifyPassword = makeVerifier([], alwaysSunday);
Line 460:         expect(() => verifyPassword('anything'))
Line 461:             .toThrow("It's the weekend!");
Line 462:     });
Line 463: 3.5
Line 464: Modular injection techniques
Line 465: JavaScript also allows for the idea of modules, which we import or require. How can we
Line 466: handle the idea of dependency injection when faced with a direct import of a depen-
Line 467: dency in our code under test, such as in the code from listing 3.1, shown again here?
Line 468: const moment = require('moment');
Line 469: const SUNDAY = 0; const SATURDAY = 6;
Line 470: const verifyPassword = (input, rules) => {
Line 471:     const dayOfWeek = moment().day();
Line 472:     if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
Line 473:         throw Error("It's the weekend!");
Line 474:     }
Line 475: Listing 3.6
Line 476: Using a higher-order factory function
Line 477: 
Line 478: --- 페이지 99 ---
Line 479: 71
Line 480: 3.5
Line 481: Modular injection techniques
Line 482:     // more code goes here...
Line 483:     // return list of errors found..
Line 484:     return [];
Line 485: };
Line 486: How can we overcome this direct dependency that’s happening? The answer is, we
Line 487: can’t. We’ll have to write the code differently to allow for the replacement of that
Line 488: dependency later on. We’ll have to create a seam through which we can replace our
Line 489: dependencies. Here’s one such example.
Line 490: const originalDependencies = {    
Line 491:     moment: require(‘moment’),    
Line 492: };                                
Line 493: let dependencies = { ...originalDependencies };     
Line 494: const inject = (fakes) => {          
Line 495:     Object.assign(dependencies, fakes);
Line 496:     return function reset() {                    
Line 497:         dependencies = { ...originalDependencies };
Line 498:     }
Line 499: };
Line 500: const SUNDAY = 0; const SATURDAY = 6;
Line 501: const verifyPassword = (input, rules) => {
Line 502:     const dayOfWeek = dependencies.moment().day();
Line 503:     if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
Line 504:         throw Error("It's the weekend!");
Line 505:     }
Line 506:     // more code goes here...
Line 507:     // return list of errors found..
Line 508:     return [];
Line 509: };
Line 510: module.exports = {
Line 511:     SATURDAY,
Line 512:     verifyPassword,
Line 513:     inject
Line 514: };
Line 515: What’s going on here? Three new things have been introduced:
Line 516: First, we have replaced our direct dependency on moment.js with an object:
Line 517: originalDependencies. It contains that module import as part of its
Line 518: implementation. 
Line 519: Next, we have added yet another object into the mix: dependencies. This
Line 520: object, by default, takes on all of the real dependencies that the original-
Line 521: Dependencies object contains. 
Line 522: Listing 3.7
Line 523: Abstracting the required dependencies
Line 524: Wrapping moment.js 
Line 525: with an intermediary 
Line 526: object
Line 527: The object containing 
Line 528: the current dependency, 
Line 529: either real or fake
Line 530: A function that replaces the real 
Line 531: dependency with a fake one
Line 532: A function that resets 
Line 533: the dependency back 
Line 534: to the real one
Line 535: 
Line 536: --- 페이지 100 ---
Line 537: 72
Line 538: CHAPTER 3
Line 539: Breaking dependencies with stubs
Line 540: Finally, the inject function, which we’re also exposing as part of our own mod-
Line 541: ule, allows whoever is importing our module (both production code and tests)
Line 542: to override our real dependencies with custom dependencies (fakes). 
Line 543: When you invoke inject, it returns a reset function that reapplies the origi-
Line 544: nal dependencies onto the current dependencies variable, thus resetting any
Line 545: fakes currently being used. 
Line 546: Here’s how you can use the inject and reset functions in a test.
Line 547: const { inject, verifyPassword, SATURDAY } = require('./password-verifier-
Line 548: time00-modular');
Line 549: const injectDate = (newDay) => {  
Line 550:     const reset = inject({       
Line 551:         moment: function () {
Line 552:             //we're faking the moment.js module's API here.
Line 553:             return {
Line 554:                 day: () => newDay
Line 555:             }
Line 556:         }
Line 557:     });
Line 558:     return reset;
Line 559: };
Line 560: describe('verifyPassword', () => {
Line 561:     describe('when its the weekend', () => {
Line 562:         it('throws an error', () => {
Line 563:             const reset = injectDate(SATURDAY);   
Line 564:             expect(() => verifyPassword('any input'))
Line 565:                 .toThrow("It's the weekend!");
Line 566:             reset();   
Line 567:         });
Line 568:     });
Line 569: });
Line 570: Let’s break down what’s going on here:
Line 571: 1
Line 572: The injectDate function is just a helper function meant to reduce the boiler-
Line 573: plate code in our test. It always builds the fake structure of the moment.js API,
Line 574: and it sets its getDay function to return the newDay parameter.
Line 575: 2
Line 576: The injectDate function calls inject with the new fake moment.js API. This
Line 577: applies the fake dependency in our unit of work to the one we have sent in as a
Line 578: parameter. 
Line 579: 3
Line 580: Our test calls the inject function with a custom, fake day.
Line 581: 4
Line 582: At the end of the test, we call the reset function, which resets the unit of work’s
Line 583: module dependencies to the original ones. 
Line 584: Listing 3.8
Line 585: Injecting a fake module with inject()
Line 586: A helper function
Line 587: Injecting a fake API 
Line 588: instead of moment.js
Line 589: Providing a 
Line 590: fake day
Line 591: Resetting the 
Line 592: dependency
Line 593: 
Line 594: --- 페이지 101 ---
Line 595: 73
Line 596: 3.6
Line 597: Moving toward objects with constructor functions
Line 598: Once you’ve done this a couple of times, it starts making sense. But it has some caveats
Line 599: as well. On the pro side, it definitely takes care of the dependency issue in our tests,
Line 600: and it’s relatively easy to use. As for the cons, there is one huge downside as far as I can
Line 601: see. Using this method to fake our modular dependencies forces our tests to be
Line 602: closely tied to the API signature of the dependencies we are faking. If these are third-
Line 603: party dependencies, such as moment.js, loggers, or anything else that we do not fully
Line 604: control, our tests will become very brittle when the time comes (as it always does) to
Line 605: upgrade or replace the dependencies with something that has a different API. This
Line 606: doesn’t hurt much if it’s just a test or two, but we’ll usually have hundreds or thou-
Line 607: sands of tests that have to fake several common dependencies, and that sometimes
Line 608: means changing and fixing hundreds of files when replacing a logger with a breaking
Line 609: API change, for example. 
Line 610:  I have two possible ways to prevent such a situation:
Line 611: Never import a third-party dependency that you don’t control directly in your
Line 612: code. Always use an interim abstraction that you do control. The Ports and
Line 613: Adapters architecture is a good example of such an idea (other names for this
Line 614: architecture are Hexagonal architecture and Onion architecture). With such
Line 615: an architecture, faking these internal APIs should present less risk, because
Line 616: we can control their rate of change, thus making our tests less brittle. (We can
Line 617: refactor them internally without our tests caring, even if the outside world
Line 618: changes.)
Line 619: Avoid using module injection, and instead use one of the other ways mentioned
Line 620: in this book for dependency injection: function parameters, currying, and, as
Line 621: mentioned in the next section, constructors and interfaces. Between these, you
Line 622: should have plenty of choices instead of importing things directly. 
Line 623: 3.6
Line 624: Moving toward objects with constructor functions
Line 625: Constructor functions are a slightly more object-oriented JavaScript-ish way of achiev-
Line 626: ing the same result as a factory function, but they return something akin to an object
Line 627: with methods we can trigger. We then use the keyword new to call this function and get
Line 628: back that special object. 
Line 629:  Here’s what the same code and tests look like with this design choice.
Line 630: const Verifier = function(rules, dayOfWeekFn)
Line 631: {
Line 632:     this.verify = function (input) {
Line 633:         if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
Line 634:             throw new Error("It's the weekend!");
Line 635:         }
Line 636:         //more code goes here..
Line 637:     };
Line 638: };
Line 639: Listing 3.9
Line 640: Using a constructor function
Line 641: 
Line 642: --- 페이지 102 ---
Line 643: 74
Line 644: CHAPTER 3
Line 645: Breaking dependencies with stubs
Line 646: const {Verifier} = require("./password-verifier-time01");
Line 647: test('constructor function: on weekends, throws exception', () => {
Line 648:     const alwaysSunday = () => SUNDAY;
Line 649:     const verifier = new Verifier([], alwaysSunday);
Line 650:     expect(() => verifier.verify('anything'))
Line 651:         .toThrow("It's the weekend!");
Line 652: });
Line 653: You might look at this and ask, “Why move toward objects?” The answer really depends
Line 654: on the context of your current project, its stack, your team’s knowledge of functional
Line 655: programming and object-oriented background, and many other non-technical fac-
Line 656: tors. It’s good to have this tool in your toolbox so you can use it when it makes sense to
Line 657: you. Keep this in the back of your mind as you read the next few sections.
Line 658: 3.7
Line 659: Object-oriented injection techniques
Line 660: If a more object-oriented style is what you’re leaning toward, or if you’re working in
Line 661: an object-oriented language such as C# or Java, here are a few common patterns that
Line 662: are widely used in the object-oriented world for dependency injection.
Line 663: 3.7.1
Line 664: Constructor injection
Line 665: Constructor injection is how I would describe a design in which we can inject dependen-
Line 666: cies through the constructor of a class. In the JavaScript world, Angular is the best-
Line 667: known web frontend framework that uses this design for injecting “services,” which is
Line 668: just a code word for “dependencies” in Angular-speak. This is a viable design in many
Line 669: other situations. 
Line 670:  Having a stateful class is not without benefits. It can remove repetition from clients
Line 671: that only need to configure our class once and can then reuse the configured class
Line 672: multiple times. 
Line 673:  If we had chosen to create a stateful version of Password Verifier, and we wanted
Line 674: to inject the date function through constructor injection, it might look like the fol-
Line 675: lowing design. 
Line 676: class PasswordVerifier {
Line 677:     constructor(rules, dayOfWeekFn) {
Line 678:         this.rules = rules;
Line 679:         this.dayOfWeek = dayOfWeekFn;
Line 680:     }
Line 681:     verify(input) {
Line 682:         if ([SATURDAY, SUNDAY].includes(this.dayOfWeek())) {
Line 683:             throw new Error("It's the weekend!");
Line 684:         }
Line 685:         const errors = [];
Line 686:         //more code goes here..
Line 687: Listing 3.10
Line 688: Constructor injection design
Line 689: 
Line 690: --- 페이지 103 ---
Line 691: 75
Line 692: 3.7
Line 693: Object-oriented injection techniques
Line 694:         return errors;
Line 695:     };
Line 696: }
Line 697: test('class constructor: on weekends, throws exception', () => {
Line 698:     const alwaysSunday = () => SUNDAY;
Line 699:     const verifier = new PasswordVerifier([], alwaysSunday);
Line 700:     expect(() => verifier.verify('anything'))
Line 701:         .toThrow("It's the weekend!");
Line 702: });
Line 703: This looks and feels a lot like the constructor function design in section 3.6. This is a
Line 704: more class-oriented design that many people will feel more comfortable with, coming
Line 705: from an object-oriented background. It also is more verbose. You’ll see that we get
Line 706: more and more verbose the more object-oriented we make things. It’s part of the
Line 707: object-oriented game. This is partly why people are choosing functional styles more
Line 708: and more—they are much more concise.
Line 709:  Let’s talk a bit about the maintainability of the tests. If I wrote a second test with
Line 710: this class, I’d extract the creation of the class via the constructor to a nice little factory
Line 711: function that returns an instance of the class under test, so that if (i.e., “when”) the
Line 712: constructor signature changes and breaks many tests at once, I only have to fix a single
Line 713: place to get all the tests working again, as you can see in the following listing.
Line 714: describe('refactored with constructor', () => {
Line 715:     const makeVerifier = (rules, dayFn) => {
Line 716:         return new PasswordVerifier(rules, dayFn);
Line 717:     };
Line 718:     test('class constructor: on weekends, throws exceptions', () => {
Line 719:         const alwaysSunday = () => SUNDAY;
Line 720:         const verifier = makeVerifier([],alwaysSunday);
Line 721:         expect(() => verifier.verify('anything'))
Line 722:             .toThrow("It's the weekend!");
Line 723:     });
Line 724:     test('class constructor: on weekdays, with no rules, passes', () => { 
Line 725:         const alwaysMonday = () => MONDAY;
Line 726:         const verifier = makeVerifier([],alwaysMonday);
Line 727:         const result = verifier.verify('anything');
Line 728:         expect(result.length).toBe(0);
Line 729:     });
Line 730: });
Line 731: Notice that this is not the same as the factory function design in section 3.4.2. This fac-
Line 732: tory function resides in our tests; the other was in our production code. This one is for
Line 733: Listing 3.11
Line 734: Adding a helper factory function to our tests
Line 735: 
Line 736: --- 페이지 104 ---
Line 737: 76
Line 738: CHAPTER 3
Line 739: Breaking dependencies with stubs
Line 740: test maintainability, and it can work with object-oriented and functional production
Line 741: code because it hides how the function or object is being created or configured. It’s
Line 742: an abstraction layer in our tests, so we can push the dependency on how a function or
Line 743: object is created or configured into a single place in our tests.
Line 744: 3.7.2
Line 745: Injecting an object instead of a function
Line 746: Right now, our class constructor takes in a function as the second parameter:
Line 747: constructor(rules, dayOfWeekFn) {
Line 748:     this.rules = rules;
Line 749:     this.dayOfWeek = dayOfWeekFn;
Line 750: }
Line 751: Let’s go one step up in our object-oriented design and use an object instead of a func-
Line 752: tion as our parameter. This requires us to do a bit of legwork: refactor the code.
Line 753:  First, we’ll create a new file called time-provider.js, which will contain our real
Line 754: object that has a dependency on moment.js. The object will be designed to have a sin-
Line 755: gle function called getDay():
Line 756: import moment from "moment";
Line 757: const RealTimeProvider = () =>  {
Line 758:     this.getDay = () => moment().day()
Line 759: };
Line 760: Next, we’ll change the parameter usage to use an object with a function:
Line 761: const SUNDAY = 0, MONDAY = 1, SATURDAY = 6;
Line 762: class PasswordVerifier {
Line 763:     constructor(rules, timeProvider) {
Line 764:         this.rules = rules;
Line 765:         this.timeProvider = timeProvider;
Line 766:     }
Line 767:     verify(input) {
Line 768:         if ([SATURDAY, SUNDAY].includes(this.timeProvider.getDay())) {
Line 769:             throw new Error("It's the weekend!");
Line 770:         }
Line 771:     ...
Line 772: }
Line 773: Finally, let’s give whoever needs an instance of our PasswordVerifier the ability to
Line 774: get it preconfigured with the real time provider by default. We’ll do this with a new
Line 775: passwordVerifierFactory function that any production code that needs a verifier
Line 776: instance will need to use:
Line 777: const passwordVerifierFactory = (rules) => {
Line 778:     return new PasswordVerifier(new RealTimeProvider())
Line 779: };
Line 780: 
Line 781: --- 페이지 105 ---
Line 782: 77
Line 783: 3.7
Line 784: Object-oriented injection techniques
Line 785: The following listing shows the entire piece of new code.
Line 786: import moment from "moment";
Line 787: const RealTimeProvider = () =>  {
Line 788:     this.getDay = () => moment().day()
Line 789: };
Line 790: const SUNDAY = 0, MONDAY=1, SATURDAY = 6;
Line 791: class PasswordVerifier {
Line 792:     constructor(rules, timeProvider) {
Line 793:         this.rules = rules;
Line 794:         this.timeProvider = timeProvider;
Line 795:     }
Line 796:     verify(input) {
Line 797:         if ([SATURDAY, SUNDAY].includes(this.timeProvider.getDay())) {
Line 798:             throw new Error("It's the weekend!");
Line 799:         }
Line 800:         const errors = [];
Line 801:         //more code goes here..
Line 802:         return errors;
Line 803:     };
Line 804: }
Line 805: const passwordVerifierFactory = (rules) => {
Line 806:     return new PasswordVerifier(new RealTimeProvider())
Line 807: };
Line 808: IoC containers and dependency injection
Line 809: There are many other ways to glue PasswordVerifier and TimeProvider together.
Line 810: I’ve just chosen manual injection to keep things simple. Many frameworks today are
Line 811: able to configure the injection of dependencies into objects under test, so that we
Line 812: can define how an object is to be constructed. Angular is one such framework. 
Line 813: If you’re using libraries like Spring in Java or Autofac or StructureMap in C#, you can
Line 814: easily configure the construction of objects with constructor injection without needing
Line 815: to create specialized functions. Commonly, these features are called Inversion of
Line 816: Control (IoC) containers or Dependency Injection (DI) containers. I’m not using them
Line 817: in this book to avoid unneeded details. You don’t need them to create great tests. 
Line 818: In fact, I don’t normally use IoC containers in tests. I’ll almost always use custom
Line 819: factory functions to inject dependencies. I find that makes my tests easier to read
Line 820: and reason about. 
Line 821: Even for tests covering Angular code, we don’t have to go through Angular’s DI frame-
Line 822: work to inject a dependency into an object in memory; we can call that object’s con-
Line 823: structor directly and send in fake stuff. As long as we do that in a factory function,
Line 824: we’re not sacrificing maintainability, and we’re also not adding extra code to tests
Line 825: unless it’s essential to the tests.
Line 826: Listing 3.12
Line 827: Injecting an object
Line 828: 
Line 829: --- 페이지 106 ---
Line 830: 78
Line 831: CHAPTER 3
Line 832: Breaking dependencies with stubs
Line 833: How can we handle this type of design in our tests, where we need to inject a fake
Line 834: object, instead of a fake function? We’ll do this manually at first, so you can see that
Line 835: it’s not a big deal. Later, we’ll let frameworks help us, but you’ll see that sometimes
Line 836: hand-coding fake objects can actually make your test more readable than using a
Line 837: framework, such as Jasmine, Jest, or Sinon (we’ll cover those in chapter 5).
Line 838:  First, in our test file, we’ll create a new fake object that has the same function sig-
Line 839: nature as our real time provider, but it will be controllable by our tests. In this case,
Line 840: we’ll just use a constructor pattern:
Line 841: function FakeTimeProvider(fakeDay) {
Line 842:     this.getDay = function () {
Line 843:         return fakeDay;
Line 844:     }
Line 845: }
Line 846: NOTE
Line 847: If you are working in a more object-oriented style, you might choose to
Line 848: create a simple class that inherits from a common interface. We’ll cover that a
Line 849: bit later in the chapter.
Line 850: Next, we’ll construct the FakeTimeProvider in our tests and inject it into the verifier
Line 851: under test:
Line 852: describe('verifier', () => {
Line 853:     test('on weekends, throws exception', () => {
Line 854:         const verifier = 
Line 855:              new PasswordVerifier([], new FakeTimeProvider(SUNDAY));
Line 856:         expect(()=> verifier.verify('anything'))
Line 857:             .toThrow("It's the weekend!");
Line 858:     });
Line 859: Here’s what the full test file looks like.
Line 860: function FakeTimeProvider(fakeDay) {
Line 861:     this.getDay = function () {
Line 862:         return fakeDay;
Line 863:     }
Line 864: }
Line 865: describe('verifier', () => {
Line 866:     test('class constructor: on weekends, throws exception', () => {
Line 867:         const verifier = 
Line 868:             new PasswordVerifier([], new FakeTimeProvider(SUNDAY));
Line 869:         expect(() => verifier.verify('anything'))
Line 870:             .toThrow("It's the weekend!");
Line 871:     });
Line 872: }); 
Line 873: Listing 3.13
Line 874: Creating a handwritten stub object
Line 875: 
Line 876: --- 페이지 107 ---
Line 877: 79
Line 878: 3.7
Line 879: Object-oriented injection techniques
Line 880: This code works because JavaScript, by default, is a very permissive language. Much
Line 881: like Ruby or Python, you can get away with duck typing things. Duck typing refers to the
Line 882: idea that if it walks like a duck and it talks like a duck, we’ll treat it like a duck. In this
Line 883: case, the real object and fake object both implement the same function, even though
Line 884: they are completely different objects. We can simply send one in place of the other,
Line 885: and the production code should be OK with this.
Line 886:  Of course, we’ll only know that this is OK and that we didn’t make any mistakes or
Line 887: miss anything regarding the function signatures at run time. If we want a bit more
Line 888: confidence, we can try it in a more type-safe manner.
Line 889: 3.7.3
Line 890: Extracting a common interface
Line 891: We can take things one step further, and, if we’re using TypeScript or a strongly typed
Line 892: language such as Java or C#, start using interfaces to denote the roles that our depen-
Line 893: dencies play. We can create a contract of sorts that both real objects and fake objects
Line 894: will have to abide by at the compiler level.
Line 895:  First, we’ll define our new interface (notice that this is now TypeScript code):
Line 896: export interface TimeProviderInterface {
Line 897:     getDay(): number;
Line 898: }
Line 899: Second, we’ll define a real time provider that implements our interface in our pro-
Line 900: duction code like this:
Line 901: import * as moment from "moment";
Line 902: import {TimeProviderInterface} from "./time-provider-interface";
Line 903: export class RealTimeProvider implements TimeProviderInterface {
Line 904:     getDay(): number {
Line 905:         return moment().day();
Line 906:     }
Line 907: }
Line 908: Third, we’ll update the constructor of our PasswordVerifier to take a dependency of
Line 909: our new TimeProviderInterface type, instead of having a parameter type of Real-
Line 910: TimeProvider. We’re abstracting away the role of a time provider and declaring that
Line 911: we don’t care what object is being passed, as long as it answers to this role’s interface:
Line 912: export class PasswordVerifier {
Line 913:     private _timeProvider: TimeProviderInterface;
Line 914:     constructor(rules: any[], timeProvider: TimeProviderInterface) {
Line 915:         this._timeProvider = timeProvider;
Line 916:     }
Line 917:     verify(input: string):string[] {
Line 918:         const isWeekened = [SUNDAY, SATURDAY]
Line 919:             .filter(x => x === this._timeProvider.getDay())
Line 920:             .length > 0;
Line 921: 
Line 922: --- 페이지 108 ---
Line 923: 80
Line 924: CHAPTER 3
Line 925: Breaking dependencies with stubs
Line 926:         if (isWeekened) {
Line 927:             throw new Error("It's the weekend!")
Line 928:         }
Line 929:          // more logic goes here
Line 930:         return [];
Line 931:     }
Line 932: }
Line 933: Now that we have an interface that defines what a “duck” looks like, we can implement
Line 934: a duck of our own in our tests. It’s going to look a lot like the previous test’s code, but
Line 935: it will have one strong difference: it will be compiler checked to ensure the correct-
Line 936: ness of the method signatures.
Line 937:  Here’s what our fake time provider looks like in our test file:
Line 938: class FakeTimeProvider implements TimeProviderInterface {
Line 939:     fakeDay: number;
Line 940:     getDay(): number {
Line 941:         return this.fakeDay;
Line 942:     }
Line 943: }
Line 944: And here’s our test:
Line 945: describe('password verifier with interfaces', () => {
Line 946:     test('on weekends, throws exceptions', () => {
Line 947:         const stubTimeProvider = new FakeTimeProvider();
Line 948:         stubTimeProvider.fakeDay = SUNDAY;
Line 949:         const verifier = new PasswordVerifier([], stubTimeProvider);
Line 950:         expect(() => verifier.verify('anything'))
Line 951:             .toThrow("It's the weekend!");
Line 952:     });
Line 953: });
Line 954: The following listing shows all the code together.
Line 955: export interface TimeProviderInterface {  getDay(): number;  }
Line 956:  
Line 957: export class RealTimeProvider implements TimeProviderInterface {
Line 958:     getDay(): number {
Line 959:         return moment().day();
Line 960:     }
Line 961: }
Line 962: export class PasswordVerifier {
Line 963:     private _timeProvider: TimeProviderInterface;
Line 964:     constructor(rules: any[], timeProvider: TimeProviderInterface) {
Line 965:         this._timeProvider = timeProvider;
Line 966:     }
Line 967: Listing 3.14
Line 968: Extracting a common interface in production code
Line 969: 
Line 970: --- 페이지 109 ---
Line 971: 81
Line 972: Summary
Line 973:     verify(input: string):string[] {
Line 974:         const isWeekend = [SUNDAY, SATURDAY]
Line 975:             .filter(x => x === this._timeProvider.getDay())
Line 976:             .length>0;
Line 977:         if (isWeekend) {
Line 978:             throw new Error("It's the weekend!")
Line 979:         }
Line 980:         return [];
Line 981:     }
Line 982: }
Line 983: class FakeTimeProvider implements TimeProviderInterface{
Line 984:     fakeDay: number;
Line 985:     getDay(): number {
Line 986:         return this.fakeDay;
Line 987:     }
Line 988: }
Line 989: describe('password verifier with interfaces', () => {
Line 990:     test('on weekends, throws exceptions', () => {
Line 991:         const stubTimeProvider = new FakeTimeProvider();
Line 992:         stubTimeProvider.fakeDay = SUNDAY;
Line 993:         const verifier = new PasswordVerifier([], stubTimeProvider);
Line 994:         expect(() => verifier.verify('anything'))
Line 995:             .toThrow("It's the weekend!");
Line 996:     });
Line 997: });
Line 998: We’ve now made a full transition from a purely functional design into a strongly
Line 999: typed, object-oriented design. Which is best for your team and your project? There’s
Line 1000: no single answer. I’ll talk more about design in chapter 8. Here, I mainly wanted to
Line 1001: show that whatever design you end up choosing, the pattern of injection remains
Line 1002: largely the same. It is just enabled with different vocabulary or language features.
Line 1003:  It’s the ability to inject that enables us to simulate things that would be practically
Line 1004: impossible to test in real life. That’s where the idea of stubs shines the most. We can
Line 1005: tell our stubs to return fake values or even to simulate exceptions in our code, to see
Line 1006: how it handles errors arising from dependencies. Injection makes this possible. Injec-
Line 1007: tion has also made our tests more repeatable, consistent, and trustworthy, and I’ll talk
Line 1008: about trustworthiness in the third part of this book. In the next chapter, we’ll look at
Line 1009: mock objects and see how they differ from stubs.
Line 1010: Summary
Line 1011: Test double is an overarching term that describes all kinds of non-production-
Line 1012: ready, fake dependencies in tests. There are five variations on test doubles that
Line 1013: can be grouped into just two types: mocks and stubs. 
Line 1014: Mocks help emulate and examine outgoing dependencies: dependencies that repre-
Line 1015: sent an exit point of our unit of work. The system under test (SUT) calls outgoing
Line 1016: 
Line 1017: --- 페이지 110 ---
Line 1018: 82
Line 1019: CHAPTER 3
Line 1020: Breaking dependencies with stubs
Line 1021: dependencies to change the state of those dependencies. Stubs help emulate
Line 1022: incoming dependencies: the SUT makes calls to such dependencies to get input data.
Line 1023: Stubs help replace an unreliable dependency with a fake, reliable one and thus
Line 1024: avoid test flakiness.
Line 1025: There are multiple ways to inject a stub into a unit of work:
Line 1026: – Function as parameter—Injecting a function instead of a plain value.
Line 1027: – Partial application (currying) and factory functions—Creating a function that
Line 1028: returns another function with some of the context baked in. This context
Line 1029: may include the dependency you replaced with a stub.
Line 1030: – Module injection—Replacing a module with a fake one with the same API.
Line 1031: This approach is fragile. You may need a lot of refactoring if the module you
Line 1032: are faking changes its API in the future.
Line 1033: – Constructor function—This is mostly the same as partial application.
Line 1034: – Class constructor injection—This is a common object-oriented technique where
Line 1035: you inject a dependency via a constructor.
Line 1036: – Object as parameter (aka duck typing)—In JavaScript, you can inject any depen-
Line 1037: dency in place of the required one as long as that dependency implements
Line 1038: the same functions.
Line 1039: – Common interface as parameter—This is the same as object as parameter, but it
Line 1040: involves a check during compile time. For this approach, you need a strongly
Line 1041: typed language like TypeScript.
