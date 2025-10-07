Line 1: 
Line 2: --- 페이지 31 ---
Line 3: 3
Line 4: The basics of unit testing
Line 5: Manual tests suck. You write your code, you run it in the debugger, you hit all the
Line 6: right keys in your app to get things just right, and then you repeat all this the next
Line 7: time you write new code. And you have to remember to check all the other code
Line 8: that might have been affected by the new code. More manual work. Great.
Line 9:  Doing tests and regression testing completely manually, repeating the same
Line 10: actions again and again like a monkey, is error prone and time consuming, and
Line 11: people seem to hate doing that as much as anything can be hated in software devel-
Line 12: opment. These problems are alleviated by tooling and our decision to use it for
Line 13: good, by writing automated tests that save us precious time and debugging pain.
Line 14: Integration and unit testing frameworks help developers write tests more quickly
Line 15: with a set of known APIs, execute those tests automatically, and review the results of
Line 16: This chapter covers
Line 17: Identifying entry points and exit points
Line 18: The definitions of unit test and unit of work
Line 19: The difference between unit testing and 
Line 20: integration testing
Line 21: A simple example of unit testing
Line 22: Understanding test-driven development
Line 23: 
Line 24: --- 페이지 32 ---
Line 25: 4
Line 26: CHAPTER 1
Line 27: The basics of unit testing
Line 28: those tests easily. And they never forget! I’m assuming you’re reading this book
Line 29: because either you feel the same way, or because someone forced you to read it, and
Line 30: that someone feels the same way. Or maybe that someone was forced to force you into
Line 31: reading this book. Doesn’t matter. If you believe repetitive manual testing is awesome,
Line 32: this book will be very difficult to read. The assumption is that you want to learn how to
Line 33: write good unit tests. 
Line 34:  This book also assumes that you know how to write code using JavaScript or Type-
Line 35: Script, using at least ECMAScript 6 (ES6) features, and that you are comfortable with
Line 36: node package manager (npm). Another assumption is that you are familiar with Git
Line 37: source control. If you’ve seen github.com before and you know how to clone a reposi-
Line 38: tory from there, you are good to go.
Line 39:  Although all the book’s code listings are in JavaScript and TypeScript, you don’t
Line 40: have to be a JavaScript programmer to read this book. The previous editions of this
Line 41: book were in C#, and I’ve found that about 80% of the patterns there have transferred
Line 42: over quite easily. You should be able to read this book even if you come from Java,
Line 43: .NET, Python, Ruby, or other languages. The patterns are just patterns. The language
Line 44: is used to demonstrate those patterns, but they are not language-specific.
Line 45: JavaScript vs. TypeScript in this book
Line 46: This book contains both vanilla JavaScript and TypeScript examples throughout. I
Line 47: take full responsibility for creating such a Tower of Babel (no pun intended), but I prom-
Line 48: ise, there’s a good reason: this book is dealing with three programming paradigms in
Line 49: JavaScript: procedural, functional, and object-oriented design. 
Line 50: I use regular JavaScript for the samples dealing with procedural and functional
Line 51: designs. I use TypeScript for the object-oriented examples, because it provides the
Line 52: structure needed to express these ideas. 
Line 53: In previous editions of this book, when I was working in C#, this wasn’t an issue.
Line 54: When moving to JavaScript, which supports these multiple paradigms, using Type-
Line 55: Script makes sense.
Line 56: Why not just use TypeScript for all the paradigms, you ask? Both to show that Type-
Line 57: Script is not needed to write unit tests and that the concepts of unit testing do not
Line 58: depend on one language or another, or on any type of compiler or linter, to work.
Line 59: This means that if you’re into functional programming, some of the examples in this
Line 60: book will make sense, and others will seem like they are overcomplicated or need-
Line 61: lessly verbose. Feel free to focus only on the functional examples.
Line 62: If you’re into object-oriented programming or are coming from a C#/Java background,
Line 63: you’ll find that some of the non-object-oriented examples are simplistic and don’t rep-
Line 64: resent your day-to-day work in your own projects. Fear not, there will be plenty of sec-
Line 65: tions relating to the object-oriented style. 
Line 66: 
Line 67: --- 페이지 33 ---
Line 68: 5
Line 69: 1.2
Line 70: Defining unit testing, step by step
Line 71: 1.1
Line 72: The first step
Line 73: There’s always a first step: the first time you wrote a program, the first time you failed
Line 74: a project, and the first time you succeeded in what you were trying to accomplish. You
Line 75: never forget your first time, and I hope you won’t forget your first tests. 
Line 76:  You may have come across tests in some form. Some of your favorite open source
Line 77: projects come with bundled “test” folders—you have them in your own projects at
Line 78: work. You might have already written a few tests yourself, and you may even remember
Line 79: them as being bad, awkward, slow, or unmaintainable. Even worse, you might have felt
Line 80: they were useless and a waste of time. (Many people sadly do.) Or you may have had a
Line 81: great first experience with unit tests, and you’re reading this book to see what more
Line 82: you might be missing. 
Line 83:  This chapter will analyze the “classic” definition of a unit test and compare it to the
Line 84: concept of integration testing. This distinction is confusing to many, but it’s very
Line 85: important to learn, because, as you’ll learn later in the book, separating unit tests
Line 86: from other types of tests can be crucial to having high confidence in your tests when
Line 87: they fail or pass.
Line 88:  We’ll also discuss the pros and cons of unit testing versus integration testing, and
Line 89: we’ll develop a better definition of what might be a “good” unit test. We’ll finish with a
Line 90: look at test-driven development (TDD), because it’s often associated with unit testing
Line 91: but is a separate skill that I highly recommend giving a chance (it’s not the main topic
Line 92: of this book, though). Throughout this chapter, I’ll also touch on concepts that are
Line 93: explained more thoroughly elsewhere in the book.
Line 94:  First, let’s define what a unit test should be.
Line 95: 1.2
Line 96: Defining unit testing, step by step
Line 97: Unit testing isn’t a new concept in software development. It’s been floating around
Line 98: since the early days of the Smalltalk programming language in the 1970s, and it
Line 99: proves itself time and time again as one of the best ways a developer can improve code
Line 100: quality while gaining a deeper understanding of the functional requirements of a
Line 101: module, class, or function. Kent Beck introduced the concept of unit testing in Small-
Line 102: talk, and it has carried on into many other programming languages, making unit test-
Line 103: ing an extremely useful practice. 
Line 104:  To see what we don’t want to use as our definition of unit testing, let’s look to Wiki-
Line 105: pedia as a starting point. I’ll use its definition with reservations, because, in my opin-
Line 106: ion, there are many important parts missing, but it is largely accepted by many for lack
Line 107: of other good definitions. Our definition will slowly evolve throughout this chapter,
Line 108: with the final definition appearing in section 1.9. 
Line 109: Unit tests are typically automated tests written and run by software developers to ensure
Line 110: that a section of an application (known as the “unit”) meets its design and behaves as
Line 111: intended. In procedural programming, a unit could be an entire module, but it is more
Line 112: commonly an individual function or procedure. In object-oriented programming, a unit
Line 113: 
Line 114: --- 페이지 34 ---
Line 115: 6
Line 116: CHAPTER 1
Line 117: The basics of unit testing
Line 118: is often an entire interface, such as a class, or an individual method (https://en
Line 119: .wikipedia.org/wiki/Unit_testing).
Line 120: The thing you’ll write tests for is the subject, system, or suite under test (SUT).
Line 121: DEFINITION
Line 122: SUT stands for subject, system, or suite under test, and some people
Line 123: like to use CUT (component, class, or code under test). When you test something,
Line 124: you refer to the thing you’re testing as the SUT.
Line 125: Let’s talk about the word “unit” in unit testing. To me, unit stands for a “unit of work”
Line 126: or a “use case” inside the system. A unit of work has a beginning and an end, which I
Line 127: call an entry point and an exit point. A simple example of a unit of work is a function
Line 128: that calculates something and returns a value. However, a function could also use
Line 129: other functions, other modules, and other components in the calculation process,
Line 130: which means the unit of work (from entry point to exit point), could span more than
Line 131: just a function.
Line 132: 1.3
Line 133: Entry points and exit points
Line 134: A unit of work always has an entry point and one or
Line 135: more exit points. Figure 1.1 shows a simple diagram
Line 136: of a unit of work.
Line 137:  A unit of work can be a single function, multiple
Line 138: functions, or even multiple modules or components.
Line 139: But it always has an entry point that we can trigger
Line 140: from the outside (via tests or other production code),
Line 141: and it always ends up doing something useful. If it
Line 142: doesn’t do anything useful, we might as well remove it
Line 143: from our codebase. 
Line 144:  What’s useful? Something publicly noticeable that
Line 145: happens in the code: a return value, a state change,
Line 146: or calling an external party, as shown in figure 1.2.
Line 147: Those noticeable behaviors are what I call exit points. 
Line 148: Unit of work
Line 149: A unit of work is all the actions that take place between the invocation of an entry
Line 150: point up until a noticeable end result through one or more exit points. The entry point
Line 151: is the thing we trigger. Given a publicly visible function, for example
Line 152: The function’s body is all or part of the unit of work. 
Line 153: The function’s declaration and signature are the entry point into the body. 
Line 154: The resulting outputs or behaviors of the function are its exit points.
Line 155: Entry point
Line 156: Exit point
Line 157: Unit
Line 158: of
Line 159: work
Line 160: Exit point
Line 161: Exit point
Line 162: Figure 1.1
Line 163: A unit of work has 
Line 164: entry points and exit points.
Line 165: 
Line 166: --- 페이지 35 ---
Line 167: 7
Line 168: 1.3
Line 169: Entry points and exit points
Line 170: The following listing shows a quick code example of a simple unit of work. 
Line 171: const sum = (numbers) => {
Line 172:   const [a, b] = numbers.split(',');
Line 173:   const result = parseInt(a) + parseInt(b);
Line 174:   return result;
Line 175: };
Line 176: Why “exit point”?
Line 177: Why use the term “exit point” and not something like “behavior”? My thinking is that
Line 178: behaviors can be purely internal, whereas we’re looking for externally visible behav-
Line 179: iors from the caller. That difference might be difficult to distinguish at a glance. Also,
Line 180: “exit point” nicely suggests we are leaving the context of a unit of work and going
Line 181: back to the test context, though behaviors might be a bit more fluid than that. There’s
Line 182: an extensive discussion about types of behavior, including observable behavior, in
Line 183: Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov (Manning, 2020).
Line 184: Refer to that book to learn more about this topic.
Line 185: Listing 1.1
Line 186: A simple function that we’d like to test
Line 187: About the JavaScript version used in this book
Line 188: I’ve chosen to use Node.js 12.8 with plain ES6 JavaScript along with JSDoc-style com-
Line 189: ments. The module system I’ll use is CommonJS, to keep things simple. Perhaps in a
Line 190: future edition I’ll start using ES modules (.mjs files), but for now, and for the rest of this
Line 191: book, CommonJS will do. It doesn’t really matter for the patterns in this book anyway. 
Line 192: You should be able to easily extrapolate the techniques used here for whatever
Line 193: JavaScript stack you’re currently working with, whether you’re using TypeScript, Plain
Line 194: JS, ES modules, backend or frontend, Angular, or React. It shouldn’t matter. 
Line 195: someFunction()
Line 196: Return value
Line 197: or error
Line 198: Unit
Line 199: of
Line 200: work
Line 201: Calling third-party
Line 202: dependency
Line 203: Noticeable
Line 204: state change
Line 205: Figure 1.2
Line 206: Types of exit points
Line 207: 
Line 208: --- 페이지 36 ---
Line 209: 8
Line 210: CHAPTER 1
Line 211: The basics of unit testing
Line 212: This unit of work is completely encompassed in a
Line 213: single function. The function is the entry point,
Line 214: and because its end result returns a value, it also
Line 215: acts as the exit point. We get the end result in the
Line 216: same place we trigger the unit of work, so the entry
Line 217: point is also the exit point.
Line 218:  If we drew this function as a unit of work, it
Line 219: would look something like figure 1.3. I used
Line 220: sum(numbers) as the entry point, not numbers,
Line 221: because the entry point is the function signature.
Line 222: The parameters are the context or input given
Line 223: through the entry point.
Line 224:  The following listing shows a variation on this
Line 225: idea. 
Line 226: let total = 0;
Line 227: const totalSoFar = () => {
Line 228:   return total;
Line 229: };
Line 230: const sum = (numbers) => {
Line 231:   const [a, b] = numbers.split(',');
Line 232:   const result = parseInt(a) + parseInt(b);
Line 233:   total += result;    
Line 234:   return result;
Line 235: };
Line 236: This new version of sum has two exit points. It does two things: 
Line 237: It returns a value.
Line 238: It introduces new functionality: a running total of all the sums. It sets the state
Line 239: of the module in a way that is noticeable (via totalSoFar) from the caller of the
Line 240: entry point.
Line 241: Getting the code for this chapter
Line 242: You can download all the code samples shown in this book from GitHub. You can find
Line 243: the repository at https://github.com/royosherove/aout3-samples. Make sure you
Line 244: have Node 12.8 or higher installed, and run npm install followed by npm run
Line 245: ch[chapter number]. For this chapter, you would run npm run ch1. This will run all
Line 246: the tests for this chapter so you can see their outputs.
Line 247: Listing 1.2
Line 248: A unit of work with entry points and exit points
Line 249: sum(numbers)
Line 250: Return value
Line 251: Unit
Line 252: of
Line 253: work
Line 254: Figure 1.3
Line 255: A function that has the 
Line 256: same entry point as exit point
Line 257: New functionality: 
Line 258: calculating a 
Line 259: running total
Line 260: 
Line 261: --- 페이지 37 ---
Line 262: 9
Line 263: 1.3
Line 264: Entry points and exit points
Line 265: Figure 1.4 shows how I would draw this unit of
Line 266: work. You can think of these two exit points as
Line 267: two different paths, or requirements, from the
Line 268: same unit of work, because they indeed are two
Line 269: different useful things the code is expected to
Line 270: do. This also means I’d be very likely to write
Line 271: two different unit tests here: one for each exit
Line 272: point. Very soon we’ll do exactly that.
Line 273:  What about totalSoFar? Is this also an
Line 274: entry point? Yes, it could be, in a separate test. I
Line 275: could write a test that proves that calling
Line 276: totalSoFar without triggering prior to that
Line 277: call returns 0. That would make it its own little
Line 278: unit of work, which would be perfectly fine.
Line 279: Often one unit of work (such as sum) can be
Line 280: composed of smaller units. 
Line 281:  As you can see, the scope of our tests can change and mutate, but we can still
Line 282: define them with entry points and exit points. Entry points are always where the test
Line 283: triggers the unit of work. You can have multiple entry points into a unit of work, each
Line 284: used by a different set of tests. 
Line 285: A note on design
Line 286: There are two main types of actions: “query” actions and “command” actions. Query
Line 287: actions don’t change stuff; they just return values. Command actions change stuff
Line 288: but don’t return values. 
Line 289: We often combine the two, but there are many cases where separating them might
Line 290: be a better design choice. This book isn’t primarily about design, but I urge you to
Line 291: read more about the concept of command query separation over on Martin Fowler’s
Line 292: website: https://martinfowler.com/bliki/CommandQuerySeparation.html.
Line 293: Exit points signifying requirements and new tests, and vice versa
Line 294: Exit points are end results of a unit of work. For unit tests, I usually write at least one
Line 295: test, with its own readable name, for each exit point. I may then add more tests with
Line 296: variations on the inputs, all using the same entry point, to gain more confidence. 
Line 297: Integration tests, which we’ll discuss later in this chapter and in the book, usually
Line 298: include multiple end results, since it can be impossible to separate code paths at
Line 299: those levels. That’s also one of the reasons integration tests are harder to debug,
Line 300: get up and running, and maintain: they do much more than unit tests, as you’ll
Line 301: soon see. 
Line 302: sum(numbers)
Line 303: Return value
Line 304: Unit
Line 305: of
Line 306: work
Line 307: State change
Line 308: totalSoFar()
Line 309: Figure 1.4
Line 310: A unit of work with two exit 
Line 311: points
Line 312: 
Line 313: --- 페이지 38 ---
Line 314: 10
Line 315: CHAPTER 1
Line 316: The basics of unit testing
Line 317: A third version of our example function is shown in the following listing.
Line 318: let total = 0;
Line 319: const totalSoFar = () => {
Line 320:   return total;
Line 321: };
Line 322: const logger = makeLogger();
Line 323: const sum = (numbers) => {
Line 324:   const [a, b] = numbers.split(',');
Line 325:   logger.info(                               
Line 326:     'this is a very important log output',   
Line 327:     { firstNumWas: a, secondNumWas: b });    
Line 328:   const result = parseInt(a) + parseInt(b);
Line 329:   total += result;
Line 330:   return result;
Line 331: };
Line 332: You can see that there’s a new exit point (or requirement, or end result) in the func-
Line 333: tion. It logs something to an external entity—perhaps to a file, or the console, or a
Line 334: database. We don’t know, and we don’t care. This is the third type of exit point: calling
Line 335: a third party. I also like to refer to it as “calling a dependency.” 
Line 336: DEFINITION
Line 337: A dependency is something we don’t have full control over during
Line 338: a unit test. Or it can be something that trying to control in a test would
Line 339: make our lives miserable. Some examples would include loggers that write
Line 340: to files, things that talk to the network, code that’s controlled by other teams,
Line 341: components that take a long time (calculations, threads, database access),
Line 342: and more. The rule of thumb is that if we can fully and easily control what
Line 343: it’s doing, and it runs in memory, and it’s fast, then it’s not a dependency.
Line 344: There are always exceptions to the rule, but this should get you through
Line 345: 80% of the cases, at least.
Line 346: Figure 1.5 shows how I’d draw this unit of work with all three exit points. At this point
Line 347: we’re still discussing a function-sized unit of work. The entry point is the function call,
Line 348: but now we have three possible paths, or exit points, that do something useful and
Line 349: that the caller can verify publicly.
Line 350:  Here’s where it gets interesting: it’s a good idea to have a separate test for each exit
Line 351: point. This will make the tests more readable and simpler to debug or change without
Line 352: affecting other outcomes.
Line 353:  
Line 354:  
Line 355:  
Line 356: Listing 1.3
Line 357: Adding a logger call to the function
Line 358: A new exit 
Line 359: point
Line 360: 
Line 361: --- 페이지 39 ---
Line 362: 11
Line 363: 1.4
Line 364: Exit point types
Line 365: 1.4
Line 366: Exit point types
Line 367: We’ve seen that we have three different types of end results:
Line 368: The invoked function returns a useful value (not undefined). If this was in a stati-
Line 369: cally typed language such as Java or C#, we’d say it is a public, non-void function.
Line 370: There’s a noticeable change to the state or behavior of the system before and
Line 371: after invocation that can be determined without interrogating private state.
Line 372: There’s a callout to a third-party system over which the test has no control. That
Line 373: third-party system doesn’t return any value, or that value is ignored. (Example:
Line 374: the code calls a third-party logging system that was not written by you, and you
Line 375: don’t control its source code.)
Line 376: Let’s see how the idea of entry and exit points affects the definition of a unit test: A
Line 377: unit test is a piece of code that invokes a unit of work and checks one specific exit point
Line 378: as an end result of that unit of work. If the assumptions about the end result turn out
Line 379: to be wrong, the unit test has failed. A unit test’s scope can span as little as a function
Line 380: or as much as multiple modules or components, depending on how many functions
Line 381: and modules are used between the entry point and the exit point. 
Line 382: XUnit Test Patterns’ definition of entry and exit points
Line 383: Gerard Meszaros’ book XUnit Test Patterns (Addison-Wesley Professional, 2007) dis-
Line 384: cusses the notion of direct inputs and outputs, and indirect inputs and outputs. Direct
Line 385: inputs are what I like to call entry points. Meszaros refers to it as “using the front
Line 386: door” of a component. Indirect outputs in that book are the other two types of exit
Line 387: points I mentioned (state change and calling a third party). 
Line 388: Both versions of these ideas have evolved in parallel, but the idea of a “unit of work”
Line 389: only appears in this book. A unit of work, coupled with entry and exit points, makes
Line 390: much more sense to me than direct and indirect inputs and outputs, but you can con-
Line 391: sider this a stylistic choice about how to teach the concept of test scopes. You can
Line 392: find more about XUnit Test Patterns at xunitpatterns.com. 
Line 393: sum(numbers)
Line 394: Return value
Line 395: Unit
Line 396: of
Line 397: work
Line 398: Call third-party
Line 399: logger
Line 400: State change
Line 401: totalSoFar()
Line 402: Figure 1.5
Line 403: Showing three exit 
Line 404: points from a function
Line 405: 
Line 406: --- 페이지 40 ---
Line 407: 12
Line 408: CHAPTER 1
Line 409: The basics of unit testing
Line 410: 1.5
Line 411: Different exit points, different techniques
Line 412: Why am I spending so much time talking about types of exit points? Because not only
Line 413: is it a great idea to separate the tests for each exit point, but different types of exit
Line 414: points might require different techniques to test successfully:
Line 415: Return-value-based exit points (direct outputs in Meszaros’ XUnit Test Patterns)
Line 416: should be the easiest exit points to test. You trigger an entry point, you get
Line 417: something back, and you check the value you got back.
Line 418: State-based tests (indirect outputs) usually require a little more gymnastics. You
Line 419: call something, and then you do another call to check something else (or you
Line 420: call the previous thing again) to see if everything went according to plan. 
Line 421: In a third-party situation (indirect outputs), we have the most hoops to jump through.
Line 422: We haven’t discussed this yet, but that’s where we’re forced to use things like mock
Line 423: objects to replace the external system with something we can control and interrogate in
Line 424: our tests. I’ll cover this idea deeply later in the book. 
Line 425: 1.6
Line 426: A test from scratch
Line 427: Let’s go back to the first, simplest version of the
Line 428: code (listing 1.1) and try to test it, shall we? If we
Line 429: were to try to write a test for this, what would it
Line 430: look like? 
Line 431:  Let’s take the visual approach first with figure 1.6.
Line 432: Our entry point is sum with an input of a string called
Line 433: numbers. sum is also our exit point, since we will get a
Line 434: return value back from it and check its value.
Line 435:  It’s possible to write an automated unit test
Line 436: without using a test framework. In fact, because
Line 437: developers have gotten more into the habit of
Line 438: automating their testing, I’ve seen plenty of them
Line 439: doing this before discovering test frameworks. In
Line 440: this section, we’ll write such a test without a frame-
Line 441: work, so that you can contrast this approach with
Line 442: using a framework in chapter 2.
Line 443: Which exit points make the most problems?
Line 444: As a rule of thumb, I try to mostly use either return-value-based or state-based tests. I
Line 445: try to avoid mock-object-based tests if I can, and usually I can. As a result, I usually
Line 446: have no more than 5% of my tests using mock objects for verification. Those types of
Line 447: tests complicate things and make maintainability more difficult. Sometimes there’s no
Line 448: escape, though, and we’ll discuss them as we proceed in the next chapters.
Line 449: sum(numbers)
Line 450: Return value
Line 451: Unit
Line 452: of
Line 453: work
Line 454: Test
Line 455: Figure 1.6
Line 456: A visual view of our test
Line 457: 
Line 458: --- 페이지 41 ---
Line 459: 13
Line 460: 1.6
Line 461: A test from scratch
Line 462:  So, let’s assume test frameworks don’t exist (or that we don’t know they do). We
Line 463: have decided to write our own little automated test from scratch. The following listing
Line 464: shows a very naive example of testing our own code with plain JavaScript.
Line 465: const parserTest = () => {
Line 466:   try {
Line 467:     const result = sum('1,2');
Line 468:     if (result === 3) {
Line 469:       console.log('parserTest example 1 PASSED');
Line 470:     } else {
Line 471:       throw new Error(`parserTest: expected 3 but was ${result}`);
Line 472:     }
Line 473:   } catch (e) {
Line 474:     console.error(e.stack);
Line 475:   }
Line 476: };
Line 477: No, this code is not lovely. But it’s good enough to explain how tests work. To run this
Line 478: code, we can do the following:
Line 479: 1
Line 480: Open the command line and type an empty string.
Line 481: 2
Line 482: Add an entry under package.json’s "scripts" entry under "test" to execute
Line 483: "node mytest.js" and then execute npm test on the command line. 
Line 484: The following listing shows this.
Line 485: {
Line 486:   "name": "aout3-samples",
Line 487:   "version": "1.0.0",
Line 488:   "description": "Code Samples for Art of Unit Testing 3rd Edition",
Line 489:   "main": "index.js",
Line 490:   "scripts": {
Line 491:     "test": "node ./ch1-basics/custom-test-phase1.js",
Line 492:   }
Line 493: }
Line 494: The test method invokes the production module (the SUT) and then checks the returned
Line 495: value. If it’s not what’s expected, the test method writes to the console an error and a
Line 496: stack trace. The test method also catches any exceptions that occur and writes them to
Line 497: the console, so that they don’t interfere with the running of subsequent methods. When
Line 498: we use a test framework, that’s usually handled for us automatically.
Line 499:  Obviously, this is an ad hoc way of writing such a test. If you were to write multiple
Line 500: tests like this, you might want to have a generic test or check method that all tests
Line 501: could use, and which would format the errors consistently. You could also add special
Line 502: helper methods that would check on things like null objects, empty strings, and so on,
Line 503: so that you don’t need to write the same long lines of code in many tests. 
Line 504: Listing 1.4
Line 505: A very naive test against sum()
Line 506: Listing 1.5
Line 507: The beginning of our package.json file
Line 508: 
Line 509: --- 페이지 42 ---
Line 510: 14
Line 511: CHAPTER 1
Line 512: The basics of unit testing
Line 513:  The following listing shows what this test would look like with a slightly more
Line 514: generic check and assertEquals functions.
Line 515: const assertEquals = (expected, actual) => {
Line 516:   if (actual !== expected) {
Line 517:     throw new Error(`Expected ${expected} but was ${actual}`);
Line 518:   }
Line 519: };
Line 520: const check = (name, implementation) => {
Line 521:   try {
Line 522:     implementation();
Line 523:     console.log(`${name} passed`);
Line 524:   } catch (e) {
Line 525:     console.error(`${name} FAILED`, e.stack);
Line 526:   }
Line 527: };
Line 528: check('sum with 2 numbers should sum them up', () => {
Line 529:   const result = sum('1,2');
Line 530:   assertEquals(3, result);
Line 531: });
Line 532: check('sum with multiple digit numbers should sum them up', () => {
Line 533:   const result = sum('10,20');
Line 534:   assertEquals(30, result);
Line 535: });
Line 536: We’ve now created two helper methods: assertEquals, which removes boilerplate
Line 537: code for writing to the console or throwing errors, and check, which takes a string for
Line 538: the name of the test and a callback to the implementation. It then takes care of catch-
Line 539: ing any test errors, writing them to the console, and reporting on the status of the test.
Line 540: Notice how the tests are easier to read and faster to write with just a couple of helper
Line 541: methods. Unit testing frameworks such as Jest can provide even more generic helper
Line 542: Listing 1.6
Line 543: Using a more generic implementation of the Check method
Line 544: Built-in asserts
Line 545: It’s important to note that we don’t need to write our own asserts. We could have
Line 546: easily used Node.js’s built-in assert functions, which were originally built for internal
Line 547: use in testing Node.js itself. We could do so by importing the functions with 
Line 548: const assert = require('assert'); 
Line 549: However, I’m trying to demonstrate the underlying simplicity of the concept, so we’ll
Line 550: avoid that. You can find more info about Node.js’s assert module at https://nodejs
Line 551: .org/api/assert.html.
Line 552: 
Line 553: --- 페이지 43 ---
Line 554: 15
Line 555: 1.7
Line 556: Characteristics of a good unit test
Line 557: methods like this, so tests are even easier to write. I’ll talk about that in chapter 2.
Line 558: First, let’s talk a bit about the main subject of this book: good unit tests. 
Line 559: 1.7
Line 560: Characteristics of a good unit test
Line 561: No matter what programming language you’re using, one of the most difficult aspects
Line 562: of defining a unit test is defining what’s meant by a good one. Of course, good is rela-
Line 563: tive, and it can change whenever we learn something new about coding. That may
Line 564: seem obvious, but it really isn’t. I need to explain why we need to write better tests—
Line 565: understanding what a unit of work is isn’t enough.
Line 566:  Based on my own experience, involving many companies and teams over the years,
Line 567: most people who try to unit test their code either give up at some point or don’t actu-
Line 568: ally perform unit tests. They waste a lot of time writing problematic tests, and they give
Line 569: up when they have to spend a lot of time maintaining them, or worse, they don’t trust
Line 570: their results. 
Line 571:  There’s no point in writing a bad unit test, unless you’re in the process of learning
Line 572: how to write a good one. There are more downsides than upsides to writing bad tests,
Line 573: such as wasting time debugging buggy tests, wasting time writing tests that bring no
Line 574: benefit, wasting time trying to understand unreadable tests, and wasting time writing
Line 575: tests only to delete them a few months later. There’s also a huge issue with maintain-
Line 576: ing bad tests, and with how they affect the maintainability of production code. Bad
Line 577: tests can actually slow down your development speed, not only when writing test code,
Line 578: but also when writing production code. I’ll touch on all these things later in the book.
Line 579:  By learning what a good unit test is, you can be sure you aren’t starting off on a
Line 580: path that will be hard to fix later on, when the code becomes a nightmare. We’ll also
Line 581: define other forms of tests (component, end to end, and more) later in the book.
Line 582: 1.7.1
Line 583: What is a good unit test? 
Line 584: Every good automated test (not just unit tests) should have the following properties:
Line 585: It should be easy to understand the intent of the test author.
Line 586: It should be easy to read and write.
Line 587: It should be automated.
Line 588: It should be consistent in its results (it should always return the same result if
Line 589: you don’t change anything between runs).
Line 590: It should be useful and provide actionable results.
Line 591: Anyone should be able to run it with the push of a button.
Line 592: When it fails, it should be easy to detect what was expected and determine how
Line 593: to pinpoint the problem.
Line 594: A good unit test should also exhibit the following properties: 
Line 595: It should run quickly.
Line 596: It should have full control of the code under test (more on that in chapter 3).
Line 597: It should be fully isolated (run independently of other tests).
Line 598: 
Line 599: --- 페이지 44 ---
Line 600: 16
Line 601: CHAPTER 1
Line 602: The basics of unit testing
Line 603: It should run in memory without requiring system files, networks, or databases.
Line 604: It should be as synchronous and linear as possible when that makes sense (no
Line 605: parallel threads if we can help it).
Line 606: It’s impossible for all tests to follow the properties of a good unit test, and that’s
Line 607: fine. Such tests will simply transition to the realm of integration testing (the topic of
Line 608: section 1.8). Still, there are ways to refactor some of your tests to conform to these
Line 609: properties.
Line 610: REPLACING THE DATABASE (OR ANOTHER DEPENDENCY) WITH A STUB
Line 611: We’ll discuss stubs in later chapters, but, in short, they are fake dependencies that
Line 612: emulate the real ones. Their purpose is to simplify the process of testing because they
Line 613: are easier to set up and maintain.
Line 614:  Beware of in-memory databases, though. They can help you isolate tests from
Line 615: each other (as long as you don’t share database instances between tests) and thus
Line 616: adhere to the properties of good unit tests, but such databases lead to an awkward,
Line 617: in-between spot. In-memory databases aren’t as easy to set up as stubs. At the same
Line 618: time, they don’t provide as strong guarantees as real databases. Functionality-wise, an
Line 619: in-memory database may differ drastically from the production one, so tests that pass
Line 620: an in-memory database may fail the real one, and vice versa. You’ll often have to rerun
Line 621: the same tests manually against the production database to gain additional confi-
Line 622: dence that your code works. Unless you use a small and standardized set of SQL fea-
Line 623: tures, I recommend sticking to either stubs (for unit tests) or real databases (for
Line 624: integration testing).
Line 625:  The same is true for solutions like jsdom. You can use it to replace the real DOM,
Line 626: but make sure it supports your particular use cases. Don’t write tests that require you
Line 627: to manually recheck them.
Line 628: EMULATING ASYNCHRONOUS PROCESSING WITH LINEAR, SYNCHRONOUS TESTS
Line 629: With the advent of promises and async/await, asynchronous coding has become stan-
Line 630: dard in JavaScript. Our tests can still verify asynchronous code synchronously, though.
Line 631: Usually that means triggering callbacks directly from the test or explicitly waiting for
Line 632: an asynchronous operation to finish executing.
Line 633: 1.7.2
Line 634: A unit test checklist
Line 635: Many people confuse the act of testing their software with the concept of a unit test.
Line 636: To start off, ask yourself the following questions about the tests you’ve written and exe-
Line 637: cuted up to now:
Line 638: Can I run and get results from a test I wrote two weeks or months or years ago?
Line 639: Can any member of my team run and get results from tests I wrote two
Line 640: months ago?
Line 641: Can I run all the tests I’ve written in no more than a few minutes?
Line 642: Can I run all the tests I’ve written at the push of a button?
Line 643: 
Line 644: --- 페이지 45 ---
Line 645: 17
Line 646: 1.8
Line 647: Integration tests
Line 648: Can I write a basic test in no more than a few minutes?
Line 649: Do my tests pass when there are bugs in another team’s code?
Line 650: Do my tests show the same results when run on different machines or environ-
Line 651: ments?
Line 652: Do my tests stop working if there’s no database, network, or deployment?
Line 653: If I delete, move, or change one test, do other tests remain unaffected?
Line 654: If you answered “no” to any of these questions, there’s a high probability that what
Line 655: you’re implementing either isn’t fully automated or it isn’t a unit test. It’s definitely
Line 656: some kind of test, and it might be as important as a unit test, but it has drawbacks com-
Line 657: pared to tests that would let you answer yes to all of those questions.
Line 658:  “What was I doing until now?” you might ask. You’ve been doing integration testing. 
Line 659: 1.8
Line 660: Integration tests
Line 661: I consider integration tests to be any tests that don’t live up to one or more of the condi-
Line 662: tions outlined previously for good unit tests. For example, if the test uses the real net-
Line 663: work, the real rest APIs, the real system time, the real filesystem, or a real database, it
Line 664: has stepped into the realm of integration testing.
Line 665:  If a test doesn’t have control of the system time, for example, and it uses the cur-
Line 666: rent new Date() in the test code, then every time the test executes, it’s essentially a dif-
Line 667: ferent test because it uses a different time. It’s no longer consistent. That’s not a bad
Line 668: thing per se. I think integration tests are important counterparts to unit tests, but they
Line 669: should be separated from them to achieve a feeling of “safe green zone,” which is dis-
Line 670: cussed later in this book.
Line 671:  If a test uses the real database, it’s no longer only running in memory—its actions
Line 672: are harder to erase than when using only in-memory fake data. The test will also run
Line 673: longer, and we won’t easily be able to control how long data access takes. Unit tests
Line 674: should be fast. Integration tests are usually much slower. When you start having hun-
Line 675: dreds of tests, every half-second counts.
Line 676:  Integration tests increase the risk of another problem: testing too many things at
Line 677: once. For example, suppose your car breaks down. How do you learn what the prob-
Line 678: lem is, let alone fix it? An engine consists of many subsystems working together,
Line 679: each relying on the others to help produce the final result: a moving car. If the car
Line 680: stops moving, the fault could be with any of the subsystems—or with more than one.
Line 681: It’s the integration of those subsystems (or layers) that makes the car move. You
Line 682: could think of the car’s movement as the ultimate integration test of these parts as
Line 683: the car goes down the road. If the test fails, all the parts fail together; if it succeeds,
Line 684: all the parts succeed. 
Line 685:  The same thing happens in software. The way most developers test their function-
Line 686: ality is through the final functionality of the app or REST API or UI. Clicking some
Line 687: button triggers a series of events—functions, modules, and components working
Line 688: together to produce the final result. If the test fails, all of these software components
Line 689: 
Line 690: --- 페이지 46 ---
Line 691: 18
Line 692: CHAPTER 1
Line 693: The basics of unit testing
Line 694: fail as a team, and it can be difficult to figure out what caused the failure of the overall
Line 695: operation (see figure 1.7).
Line 696: As defined in The Complete Guide to Software Testing by Bill Hetzel (Wiley, 1988), integra-
Line 697: tion testing is “an orderly progression of testing in which software and/or hardware
Line 698: elements are combined and tested until the entire system has been integrated.”
Line 699: Here’s my own variation on defining integration testing:
Line 700: Integration testing is testing a unit of work without having full control over all of its real
Line 701: dependencies, such as other components by other teams, other services, the time, the
Line 702: network, databases, threads, random number generators, and more.
Line 703: To summarize, an integration test uses real dependencies; unit tests isolate the unit of
Line 704: work from its dependencies so that they’re easily consistent in their results and can
Line 705: easily control and simulate any aspect of the unit’s behavior.
Line 706:  Let’s apply the questions from section 1.7.2 to integration tests and consider what
Line 707: you want to achieve with real-world unit tests: 
Line 708: Can I run and get results from a test I wrote two weeks or months or years ago? 
Line 709: If you can’t, how would you know whether you broke a feature that you created
Line 710: earlier? Shared data and code changes regularly during the life of an application,
Line 711: cdn.site.com
Line 712: HAProxy
Line 713: NGINX
Line 714: foo.site.com
Line 715: bar.site.com
Line 716: Web app
Line 717: Microservice
Line 718: Queues
Line 719: List
Line 720: Golang
Line 721: Web app
Line 722: Workers
Line 723: PostgreSQL
Line 724: Books
Line 725: Failure points
Line 726: Failure points
Line 727: Some page
Line 728: Browser
Line 729: Figure 1.7
Line 730: You can have many failure points in an integration test. All the units have to work together, and each 
Line 731: could malfunction, making it harder to find the source of a bug. 
Line 732: 
Line 733: --- 페이지 47 ---
Line 734: 19
Line 735: 1.8
Line 736: Integration tests
Line 737: and if you can’t (or won’t) run tests for all the previously working features after
Line 738: changing your code, you just might break it without knowing—this is known as
Line 739: a regression. Regressions seem to occur a lot near the end of a sprint or release,
Line 740: when developers are under pressure to fix existing bugs. Sometimes they intro-
Line 741: duce new bugs inadvertently as they resolve old ones. Wouldn’t it be great to
Line 742: know that you broke something within 60 seconds of breaking it? You’ll see how
Line 743: that can be done later in this book.
Line 744: DEFINITION
Line 745: A regression is broken functionality—code that used to work. You
Line 746: can also think of it as one or more units of work that once worked and now
Line 747: don’t. 
Line 748: Can any member of my team run and get results from tests I wrote two months ago?
Line 749: This goes with the previous point but takes it up a notch. You want to make sure
Line 750: that you don’t break someone else’s code when you change something. Many
Line 751: developers fear changing legacy code in older systems for fear of not knowing
Line 752: what other code depends on what they’re changing. In essence, they risk chang-
Line 753: ing the system into an unknown state of stability.
Line 754: Few things are scarier than not knowing whether the application still works,
Line 755: especially when you didn’t write that code. If you have that safety net of unit
Line 756: tests and know you aren’t breaking anything, you’ll be much less afraid of tak-
Line 757: ing on code you’re less familiar with. 
Line 758: Good tests can be accessed and run by anyone.
Line 759: DEFINITION
Line 760: Legacy code is defined by Wikipedia as “old computer source code
Line 761: that is no longer supported on the standard hardware and environments”
Line 762: (https://en.wikipedia.org/wiki/Legacy_system), but many shops refer to any
Line 763: older version of the application currently under maintenance as legacy code.
Line 764: It often refers to code that’s hard to work with, hard to test, and usually even
Line 765: hard to read. A client once defined legacy code in a down-to-earth way: “code
Line 766: that works.” Many people like to define legacy code as “code that has no
Line 767: tests.” Working Effectively with Legacy Code by Michael Feathers (Pearson, 2004)
Line 768: uses “code that has no tests” as an official definition of legacy code, and it’s a
Line 769: definition to be considered while reading this book.
Line 770: Can I run all the tests I’ve written in no more than a few minutes?
Line 771: If you can’t run your tests quickly (seconds are better than minutes), you’ll run
Line 772: them less often (daily, or even weekly or monthly in some places). The problem
Line 773: is that when you change code, you want to get feedback as early as possible to
Line 774: see if you broke something. The more time required between running the tests,
Line 775: the more changes you make to the system, and the (many) more places you’ll
Line 776: have to search for bugs when you find that you broke something. 
Line 777: Good tests should run quickly.
Line 778: 
Line 779: --- 페이지 48 ---
Line 780: 20
Line 781: CHAPTER 1
Line 782: The basics of unit testing
Line 783: Can I run all the tests I’ve written at the push of a button?
Line 784: If you can’t, it probably means that you have to configure the machine on
Line 785: which the tests will run so that they run correctly (setting up a Docker envi-
Line 786: ronment, or setting connection strings to the database, for example), or it
Line 787: may mean that your unit tests aren’t fully automated. If you can’t fully auto-
Line 788: mate your unit tests, you’ll probably avoid running them repeatedly, as will
Line 789: everyone else on your team.
Line 790: No one likes to get bogged down with configuring details to run tests, just to
Line 791: make sure that the system still works. Developers have more important things to
Line 792: do, like writing more features into the system. But they can’t do that if they
Line 793: don’t know the state of the system.
Line 794: Good tests should be easily executed in their original form, not manually.
Line 795: Can I write a basic test in no more than a few minutes?
Line 796: One of the easiest ways to spot an integration test is that it takes time to prepare
Line 797: correctly and to implement, not just to execute. It takes time to figure out how to
Line 798: write it because of all the internal, and sometimes external, dependencies. (A
Line 799: database may be considered an external dependency.) If you’re not automating
Line 800: the test, dependencies are less of a problem, but you’re losing all the benefits of
Line 801: an automated test. The harder it is to write a test, the less likely you are to write
Line 802: more tests or to focus on anything other than the “big stuff” that you’re worried
Line 803: about. One of the strengths of unit tests is that they tend to test every little thing
Line 804: that might break, not only the big stuff. People are often surprised at how many
Line 805: bugs they can find in code they thought was simple and bug free. 
Line 806: When you concentrate only on the big tests, the overall confidence in your
Line 807: code is still very much lacking. Many parts of the code’s core logic aren’t tested
Line 808: (even though you may be covering more components), and there may be many
Line 809: bugs that you haven’t considered and might be “unofficially” worried about.
Line 810: Good tests against the system should be easy and quick to write, once you’ve
Line 811: figured out the patterns you want to use to test your specific set of objects, func-
Line 812: tions, and dependencies (the domain model). 
Line 813: Do my tests pass when there are bugs in another team’s code? Do my tests show the same
Line 814: results when run on different machines or environments? Do my tests stop working if
Line 815: there’s no database, network, or deployment?
Line 816: These three points refer to the idea that our test code is isolated from various
Line 817: dependencies. The test results are consistent because we have control over what
Line 818: those indirect inputs into our system provide. We can have fake databases, fake
Line 819: networks, fake time, and fake machine culture. In later chapters, I’ll refer to
Line 820: those points as stubs and seams in which we can inject those stubs.
Line 821: If I delete, move, or change one test, do other tests remain unaffected?
Line 822: Unit tests usually don’t need to have any shared state, but integration tests often
Line 823: do, such as an external database or service. Shared state can create a dependency
Line 824: 
Line 825: --- 페이지 49 ---
Line 826: 21
Line 827: 1.9
Line 828: Finalizing our definition
Line 829: between tests. For example, running tests in the wrong order can corrupt the
Line 830: state for future tests.
Line 831: WARNING
Line 832: Even experienced unit testers can find that it may take 30 minutes
Line 833: or more to figure out how to write the very first unit test against a domain
Line 834: model they’ve never unit tested before. This is part of the work and is to be
Line 835: expected. The second and subsequent tests on that domain model should be
Line 836: very easy to accomplish once you’ve figured out the entry and exit points of
Line 837: the unit of work. 
Line 838: We can recognize three main criteria in the previous questions and answers:
Line 839: Readability—If we can’t read it, then it’s hard to maintain, hard to debug, and
Line 840: hard to know what’s wrong.
Line 841: Maintainability—If maintaining the test or production code is painful because
Line 842: of the tests, our lives will become a living nightmare. 
Line 843: Trust—If we don’t trust the results of our tests when they fail, we’ll start manu-
Line 844: ally testing again, losing all the time benefit the tests are supposed to provide. If
Line 845: we don’t trust the tests when they pass, we’ll start debugging more, again losing
Line 846: any time benefit. 
Line 847: From what I’ve explained so far about what a unit test is not and what features need to
Line 848: be present for testing to be useful, I can now start to answer the primary question this
Line 849: chapter poses: what is a good unit test?
Line 850: 1.9
Line 851: Finalizing our definition
Line 852: Now that I’ve covered the important properties that a unit test should have, I’ll define
Line 853: unit tests once and for all:
Line 854: A unit test is an automated piece of code that invokes the unit of work through an entry
Line 855: point and then checks one of its exit points. A unit test is almost always written using a
Line 856: unit testing framework. It can be written easily and runs quickly. It’s trustworthy,
Line 857: readable, and maintainable. It is consistent as long as the production code we control has
Line 858: not changed.
Line 859: This definition certainly looks like a tall order, particularly considering how many
Line 860: developers implement unit tests poorly. It makes us take a hard look at the way we, as
Line 861: developers, have implemented testing up until now, compared to how we’d like to
Line 862: implement it. (Trustworthy, readable, and maintainable tests are discussed in depth in
Line 863: chapters 7 through 9.)
Line 864:  In the first edition of this book, my definition of a unit test was slightly different. I
Line 865: used to define a unit test as “only running against control flow code,” but I no longer
Line 866: think that’s true. Code without logic is usually used as part of a unit of work. Even
Line 867: properties with no logic will get used by a unit of work, so they don’t have to be specif-
Line 868: ically targeted by tests.
Line 869: 
Line 870: --- 페이지 50 ---
Line 871: 22
Line 872: CHAPTER 1
Line 873: The basics of unit testing
Line 874: DEFINITION
Line 875: Control flow code is any piece of code that has some sort of logic in
Line 876: it, small as it may be. It has one or more of the following: an if statement, a
Line 877: loop, calculations, or any other type of decision-making code. 
Line 878: Getters and setters are good examples of code that usually doesn’t contain any logic
Line 879: and so don’t require specific targeting by the tests. It’s code that will probably get used
Line 880: by the unit of work you’re testing, but there’s no need to test it directly. But watch out:
Line 881: once you add any logic inside a getter or setter, you’ll want to make sure that logic is
Line 882: being tested. 
Line 883:  In the next section, we’ll stop talking about what is a good test and talk about when
Line 884: you might want to write tests. I’ll discuss test-driven development, because it is often
Line 885: put in the same bucket as doing unit testing. I want to make sure we set the record
Line 886: straight on that. 
Line 887: 1.10
Line 888: Test-driven development
Line 889: Once you know how to write readable, maintainable, and trustworthy tests with a unit
Line 890: testing framework, the next question is when to write the tests. Many people feel that
Line 891: the best time to write unit tests for software is after they’ve created some functionality
Line 892: and just before they merge their code into remote source control. 
Line 893:  Also, to be a bit blunt, a lot of people don’t believe writing tests is a good idea, but
Line 894: have realized through trial and error that there are strict testing requirements in
Line 895: source control reviews, so they have to write tests to appease the code review gods and
Line 896: get their code merged into the main branch. (That kind of dynamic is a great source
Line 897: of bad tests, and I’ll address it in the third part of this book.)
Line 898:  A growing number of developers prefer writing unit tests incrementally, during the
Line 899: coding session and before each piece of very small functionality is implemented. This
Line 900: approach is called test-first or test-driven development (TDD).
Line 901: NOTE
Line 902: There are many different views on exactly what test-driven develop-
Line 903: ment means. Some say it’s test-first development, and some say it means you
Line 904: have a lot of tests. Some say it’s a way of designing, and others feel it could be
Line 905: a way to drive your code’s behavior with only some design. In this book, TDD
Line 906: means test-first development, with design taking an incremental role in the
Line 907: technique (besides this section, TDD won’t be discussed in this book).
Line 908: Figures 1.8 and 1.9 show the differences between traditional coding and TDD. TDD is
Line 909: different from traditional development, as figure 1.9 shows. You begin by writing a test
Line 910: that fails; then you move on to creating the production code, seeing the test pass, and
Line 911: continuing on to either refactor your code or create another failing test.
Line 912:  This book focuses on the technique of writing good unit tests, rather than on
Line 913: TDD, but I’m a big fan of TDD. I’ve written several major applications and frame-
Line 914: works using TDD, I’ve managed teams that utilize it, and I’ve taught hundreds of
Line 915: courses and workshops on TDD and unit testing techniques. Throughout my career,
Line 916: I’ve found TDD to be helpful in creating quality code, quality tests, and better designs
Line 917: 
Line 918: --- 페이지 51 ---
Line 919: 23
Line 920: 1.10
Line 921: Test-driven development
Line 922: Write function,
Line 923: class, or
Line 924: application
Line 925: Write tests
Line 926: (if we have
Line 927: time)
Line 928: Run tests
Line 929: (if we have
Line 930: time)
Line 931: Fix bugs
Line 932: (if we have
Line 933: time)
Line 934: Figure 1.8
Line 935: The traditional 
Line 936: way of writing unit tests
Line 937: Write a new
Line 938: test to prove the
Line 939: next small piece
Line 940: of functionality is
Line 941: missing or
Line 942: wrong.
Line 943: Simplest
Line 944: possible
Line 945: production
Line 946: code ﬁx
Line 947: Incremental
Line 948: refactoring as
Line 949: needed on test
Line 950: or production
Line 951: code
Line 952: Run all tests.
Line 953: Run all tests.
Line 954: Run all tests.
Line 955: New test
Line 956: should compile
Line 957: and fail
Line 958: All tests should
Line 959: be passing.
Line 960: All tests should
Line 961: be passing.
Line 962: Repeat until you like the code.
Line 963: Repeat until
Line 964: you have
Line 965: conﬁdence
Line 966: in the code.
Line 967: Design
Line 968: Start here.
Line 969: Think.
Line 970: Design.
Line 971: Figure 1.9
Line 972: Test-driven development—a bird’s-eye view. Notice the circular nature of the process: 
Line 973: write the test, write the code, refactor, write the next test. It shows the incremental nature of TDD: 
Line 974: small steps lead to a quality end result with confidence.
Line 975: 
Line 976: --- 페이지 52 ---
Line 977: 24
Line 978: CHAPTER 1
Line 979: The basics of unit testing
Line 980: for the code I was writing. I’m convinced that it can work to your benefit, but it’s not
Line 981: without a price (time to learn, time to implement, and more). It’s definitely worth the
Line 982: admission price, though, if you’re willing to take on the challenge of learning it. 
Line 983: 1.10.1 TDD: Not a substitute for good unit tests
Line 984: It’s important to realize that TDD doesn’t ensure project success or tests that are robust
Line 985: or maintainable. It’s quite easy to get caught up in the technique of TDD and not pay
Line 986: attention to the way unit tests are written: their naming, how maintainable or readable
Line 987: they are, and whether they test the right things or might themselves have bugs. That’s
Line 988: why I’m writing this book—because writing good tests is a separate skill from TDD. 
Line 989:  The technique of TDD is quite simple:
Line 990: 1
Line 991: Write a failing test to prove code or functionality is missing from the end product. The
Line 992: test is written as if the production code were already working, so the test failing
Line 993: means there’s a bug in the production code. How do I know? The test is written
Line 994: such that it would pass if the production code had no bugs.
Line 995: In some languages other than JavaScript, the test might not even compile at
Line 996: first, since the code doesn’t exist yet. Once it does run, it should be failing,
Line 997: because the production code is still not working. This is where a lot of the
Line 998: “design” in test-driven-design thinking happens.
Line 999: 2
Line 1000: Make the test pass by adding functionality to the production code that meets the expectations
Line 1001: of your test. The production code should be kept as simple as possible. Don’t touch
Line 1002: the test. You have to make it pass only by touching production code.
Line 1003: 3
Line 1004: Refactor your code. When the test passes, you’re free to move on to the next unit
Line 1005: test or to refactor your code (both production code and tests) to make it more
Line 1006: readable, to remove code duplication, and so on. This is another point where
Line 1007: the “design” part happens. We refactor and can even redesign our components
Line 1008: while still keeping the old functionality.
Line 1009: Refactoring steps should be very small and incremental, and we run all the
Line 1010: tests after each small step to make sure we didn’t break anything with our
Line 1011: changes. Refactoring can be done after writing several tests or after writing each
Line 1012: test. It’s an important practice, because it ensures your code gets easier to read
Line 1013: and maintain, while still passing all of the previously written tests. There’s a
Line 1014: whole section (8.3) on refactoring later in the book.
Line 1015: DEFINITION
Line 1016: Refactoring means changing a piece of code without changing its
Line 1017: functionality. If you’ve ever renamed a method, you’ve done refactoring. If
Line 1018: you’ve ever split a large method into multiple smaller method calls, you’ve
Line 1019: refactored your code. The code still does the same thing, but it becomes eas-
Line 1020: ier to maintain, read, debug, and change. 
Line 1021: The preceding steps sound technical, but there’s a lot of wisdom behind them. Done
Line 1022: correctly, TDD can make your code quality soar, decrease the number of bugs, raise
Line 1023: your confidence in the code, shorten the time it takes to find bugs, improve your code’s
Line 1024: 
Line 1025: --- 페이지 53 ---
Line 1026: 25
Line 1027: 1.10
Line 1028: Test-driven development
Line 1029: design, and keep your manager happier. If TDD is done incorrectly, it can cause your
Line 1030: project schedule to slip, waste your time, lower your motivation, and lower your code
Line 1031: quality. It’s a double-edged sword, and many people find this out the hard way. 
Line 1032:  Technically, one of the biggest benefits of TDD that nobody tells you about is that
Line 1033: by seeing a test fail, and then seeing it pass without changing the test, you’re basically
Line 1034: testing the test itself. If you expect it to fail and it passes, you might have a bug in your
Line 1035: test or you’re testing the wrong thing. If the test failed, you fixed it, and now you
Line 1036: expect it to pass, and it still fails, your test could have a bug, or maybe it’s expecting
Line 1037: the wrong thing to happen.
Line 1038:  This book deals with readable, maintainable, and trustworthy tests, but if you add
Line 1039: TDD on top, your confidence in your own tests will increase by seeing the failed, you
Line 1040: fixed it, tests failing when they should and passing when they should. In test-after style,
Line 1041: you’ll usually only see them pass when they should, and fail when they shouldn’t
Line 1042: (since the code they test should already be working). TDD helps with that a lot, and
Line 1043: it’s also one of the reasons developers do far less debugging when practicing TDD
Line 1044: than when they’re simply unit testing after the fact. If they trust the tests, they don’t
Line 1045: feel a need to debug it “just in case.” That’s the kind of trust you can only gain by see-
Line 1046: ing both sides of the test—failing when it should and passing when it should.
Line 1047: 1.10.2 Three core skills needed for successful TDD
Line 1048: To be successful in test-driven development, you need three different skill sets: know-
Line 1049: ing how to write good tests, writing them test-first, and designing the tests and the pro-
Line 1050: duction code well. Figure 1.10 shows these more clearly:
Line 1051: Just because you write your tests first doesn’t mean they’re maintainable, readable, or trust-
Line 1052: worthy. Good unit testing skills are what this book is all about.
Line 1053: Just because you write readable, maintainable tests doesn’t mean you’ll get the same bene-
Line 1054: fits as when writing them test-first. Test-first skills are what most of the TDD books
Line 1055: out there teach, without teaching the skills of good testing. I would especially
Line 1056: recommend Kent Beck’s Test-Driven Development: By Example (Addison-Wesley
Line 1057: Professional, 2002). 
Line 1058: TDD skills
Line 1059: This book
Line 1060: Other books
Line 1061: Writing
Line 1062: good tests
Line 1063: Writing
Line 1064: test-ﬁrst
Line 1065: SOLID
Line 1066: design
Line 1067: Figure 1.10
Line 1068: Three core skills 
Line 1069: of test-driven development
Line 1070: 
Line 1071: --- 페이지 54 ---
Line 1072: 26
Line 1073: CHAPTER 1
Line 1074: The basics of unit testing
Line 1075: Just because you write your tests first, and they’re readable and maintainable, doesn’t
Line 1076: mean you’ll end up with a well-designed system. Design skills are what make your
Line 1077: code beautiful and maintainable. I recommend Growing Object-Oriented Software,
Line 1078: Guided by Tests by Steve Freeman and Nat Pryce (Addison-Wesley Professional,
Line 1079: 2009) and Clean Code by Robert C. Martin (Pearson, 2008) as good books on the
Line 1080: subject.
Line 1081: A pragmatic approach to learning TDD is to learn each of these three aspects sepa-
Line 1082: rately; that is, to focus on one skill at a time, ignoring the others in the meantime. The
Line 1083: reason I recommend this approach is that I often see people trying to learn all three
Line 1084: skill sets at the same time, having a really hard time in the process, and finally giving
Line 1085: up because the wall is too high to climb. By taking a more incremental approach to
Line 1086: learning this field, you relieve yourself of the constant fear that you’re getting it wrong
Line 1087: in a different area than you’re currently focusing on.
Line 1088:  In the next chapter, you’ll start writing your first unit tests using Jest, one of the
Line 1089: most commonly used test frameworks for JavaScript.
Line 1090: Summary
Line 1091: A good unit test has these qualities:
Line 1092: – It should run quickly.
Line 1093: – It should have full control of the code under test.
Line 1094: – It should be fully isolated (it should run independently of other tests).
Line 1095: – It should run in memory without requiring filesystem files, networks, or
Line 1096: databases. 
Line 1097: – It should be as synchronous and linear as possible (no parallel threads).
Line 1098: Entry points are public functions that are the doorways into our units of work
Line 1099: and trigger the underlying logic. Exit points are the places you can inspect with
Line 1100: your test. They represent the effects of the units of work. 
Line 1101: An exit point can be a return value, a change of state, or a call to a third-party
Line 1102: dependency. Each exit point usually requires a separate test, and each type of
Line 1103: exit point requires a different testing technique.
Line 1104: A unit of work is the sum of actions that take place between the invocation of an
Line 1105: entry point up until a noticeable end result through one or more exit points. A
Line 1106: unit of work can span a function, a module, or multiple modules.
Line 1107: Integration testing is just unit testing with some or all of the dependencies
Line 1108: being real and residing outside of the current execution process. Conversely,
Line 1109: unit testing is like integration testing, but with all of the dependencies in mem-
Line 1110: ory (both real and fake), and we have control over their behavior in the test.
Line 1111: The most important attributes of any test are readability, maintainability, and
Line 1112: trust. Readability tells us how easy it is to read and understand the test. Maintain-
Line 1113: ability is the measure of how painful it is to maintain the test code. Without trust,
Line 1114: 
Line 1115: --- 페이지 55 ---
Line 1116: 27
Line 1117: Summary
Line 1118: it’s harder to introduce important changes (such as refactoring) in a codebase,
Line 1119: which leads to code deterioration.
Line 1120: Test-driven development (TDD) is a technique that advocates for writing tests
Line 1121: before the production code. This approach is also referred to as a test-first
Line 1122: approach (as opposed to code-first).
Line 1123: The main benefit of TDD is verifying the correctness of your tests. Seeing your
Line 1124: tests fail before writing production code ensures that these same tests would fail
Line 1125: if the functionality they cover stops working properly.
