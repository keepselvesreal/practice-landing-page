Line 1: 
Line 2: --- 페이지 56 ---
Line 3: 28
Line 4: A first unit test
Line 5: When I first started writing unit tests with a real unit testing framework, there was
Line 6: little documentation, and the frameworks I worked with didn’t have proper exam-
Line 7: ples. (I was mostly coding in VB 5 and 6 at the time.) It was a challenge learning to
Line 8: work with them, and I started out writing rather poor tests. Fortunately, times have
Line 9: changed. In JavaScript, and in practically any language out there, there’s a wide
Line 10: range of choices and plenty of documentation and support from the community
Line 11: for trying out these bundles of helpfulness.
Line 12:  In the previous chapter, we wrote a very simple home-grown test framework.
Line 13: In this chapter, we’ll take a look at Jest, which will be our framework of choice for
Line 14: this book. 
Line 15: This chapter covers
Line 16: Writing your first test with Jest
Line 17: Test structure and naming conventions
Line 18: Working with the assertion library
Line 19: Refactoring tests and reducing repetitive code
Line 20: 
Line 21: --- 페이지 57 ---
Line 22: 29
Line 23: 2.1
Line 24: Introducing Jest
Line 25: 2.1
Line 26: Introducing Jest
Line 27: Jest is an open source test framework created by Facebook. It’s easy to use, easy to
Line 28: remember, and has lots of great features. Jest was originally created for testing front-
Line 29: end React components in JavaScript. These days it’s widely used in many parts of the
Line 30: industry for both backend and frontend project testing. It supports two major flavors
Line 31: of test syntax (one that uses the word test and another that’s based on the Jasmin syn-
Line 32: tax, a framework that has inspired many of Jest’s features). We’ll try both of them to
Line 33: see which one we like better. 
Line 34:  Aside from Jest, there are many other testing frameworks in JavaScript, pretty
Line 35: much all open source as well. There are some differences between them in style and
Line 36: APIs, but for the purposes of this book, that shouldn’t matter too much. 
Line 37: 2.1.1
Line 38: Preparing our environment
Line 39: Make sure you have Node.js installed locally. You can follow the instructions at
Line 40: https://nodejs.org/en/download/ to get it up and running on your machine. The
Line 41: site will provide you with the option of either a long-term support (LTS) release or a
Line 42: current release. The LTS release is geared toward enterprises, whereas the current
Line 43: release has more frequent updates. Either will work for the purposes of this book.
Line 44:  Make sure that the node package manager (npm) is installed on your machine. It
Line 45: is included with Node.js, so run the command npm -v on the command line, and if you
Line 46: see a version of 6.10.2 or higher, you should be good to go. If not, make sure Node.js
Line 47: is installed.
Line 48: 2.1.2
Line 49: Preparing our working folder
Line 50: To get started with Jest, let’s create a new empty folder named “ch2” and initialize it
Line 51: with a package manager of your choice. I’ll use npm, since I have to choose one. Yarn
Line 52: is an alternative package manager. It shouldn’t matter, for the purposes of this book,
Line 53: which one you use. 
Line 54:  Jest expects either a jest.config.js or a package.json file. We’re going with the latter,
Line 55: and npm init will generate one for us:
Line 56: mkdir ch2
Line 57: cd ch2
Line 58: npm init --yes
Line 59: //or
Line 60: yarn init –yes 
Line 61: git init
Line 62: I’m also initializing Git in this folder. This would be recommended anyway, to track
Line 63: changes, but for Jest this file is used under the covers to track changes to files and run
Line 64: specific tests. It makes Jest’s life easier. 
Line 65:  By default, Jest will look for its configuration either in the package.json file that is
Line 66: created by this command or in a special jest.config.js file. For now, we won’t need
Line 67: 
Line 68: --- 페이지 58 ---
Line 69: 30
Line 70: CHAPTER 2
Line 71: A first unit test
Line 72: anything but the default package.json file. If you’d like to learn more about the Jest
Line 73: configuration options, refer to https://jestjs.io/docs/en/configuration.
Line 74: 2.1.3
Line 75: Installing Jest
Line 76: Next, we’ll install Jest. To install Jest as a dev dependency (which means it does not get
Line 77: distributed to production) we can use this command:
Line 78: npm install --save-dev jest
Line 79: //or
Line 80: yarn add jest –dev
Line 81: This will create a new jest.js file under our [root folder]/node_modules/bin. We can
Line 82: then execute Jest using the npx jest command.
Line 83:  We can also install Jest globally on the local machine (I recommend doing this on
Line 84: top of the save-dev installation) by executing this command:
Line 85: npm install -g jest
Line 86: This will give us the freedom to execute the jest command directly from the com-
Line 87: mand line in any folder that has tests, without going through npm to execute it.
Line 88:  In real projects, it is common to use npm commands to run tests instead of using
Line 89: the global jest. I’ll show how this is done in the next few pages. 
Line 90: 2.1.4
Line 91: Creating a test file
Line 92: Jest has a couple of default ways to find test files: 
Line 93: If there’s a __tests__ folder, it loads all the files in it as test files, regardless of
Line 94: their naming conventions. 
Line 95: It tries to find any file that ends with *.spec.js or *.test.js, in any folder under the
Line 96: root folder of your project, recursively. 
Line 97: We’ll use the first variation, but we’ll also name our files with either *test.js or *.spec.js
Line 98: to make things a bit more consistent in case we want to move them around later (and
Line 99: stop using the __tests_ folder altogether). 
Line 100:  You can also configure Jest to your heart’s content, specifying how to find which
Line 101: files where, with a jest.config.js file or through package.json. You can look up the Jest
Line 102: docs at https://jestjs.io/docs/en/configuration to find all the gory details.
Line 103:  The next step is to create a special folder under our ch2 folder called __tests__.
Line 104: Under this folder, create a file that ends with either test.js or spec.js—my-compo-
Line 105: nent.test.js, for example. Which suffix you choose is up to you—it’s about your own
Line 106: style. I’ll use them interchangeably in this book because I think of “test” as the sim-
Line 107: plest version of “spec,” so I use it when showing very simple things.
Line 108:  We don’t need require() at the top of the file to start using Jest. It automatically
Line 109: imports global functions for us to use. The main functions you should be interested
Line 110: in include test, describe, it, and expect. Listing 2.1 shows what a simple test might
Line 111: look like.
Line 112: 
Line 113: --- 페이지 59 ---
Line 114: 31
Line 115: 2.1
Line 116: Introducing Jest
Line 117: test('hello jest', () => {
Line 118:     expect('hello').toEqual('goodbye');
Line 119: });
Line 120: We haven’t used describe and it yet, but we’ll get to them soon. 
Line 121: 2.1.5
Line 122: Executing Jest
Line 123: To run this test, we need to be able to execute Jest. For Jest to be recognized from the
Line 124: command line, we need to do either of the following:
Line 125: Install Jest globally on the machine by running npm install jest -g.
Line 126: Use npx to execute Jest from the node_modules directory by typing jest in the
Line 127: root of the ch2 folder.
Line 128: If all the stars lined up correctly, you should see the results of the Jest test run and a fail-
Line 129: ure. Your first failure. Yay! Figure 2.1 shows the output on my terminal when I run the
Line 130: command. It’s pretty cool to see such lovely, colorful (if you’re reading the e-book), use-
Line 131: ful output from a test tool. It looks even cooler if your terminal is in dark mode.
Line 132:  Let’s take a closer look at the details. Figure 2.2 shows the same output, but with
Line 133: numbers to follow along. Let’s see how many pieces of information are presented
Line 134: here:
Line 135: b
Line 136: A quick list of all the failing tests (with names) with nice red Xs next to them
Line 137: c
Line 138: A detailed report on the expectation that failed (aka our assertion)
Line 139: d
Line 140: The exact difference between the actual value and expected value
Line 141: e
Line 142: The type of comparison that was executed
Line 143: f
Line 144: The code for the test
Line 145: g
Line 146: The exact line (visually) where the test failed
Line 147: h
Line 148: A report of how many tests ran, failed, and passed
Line 149: i
Line 150: The time it took
Line 151: j
Line 152: The number of snapshots (not relevant to our discussion)
Line 153: Test file locations
Line 154: There are two main patterns I see for placing test files: Some people prefer to place
Line 155: the test files directly next to the files or modules being tested. Others prefer to place
Line 156: all the files under a test directory. Which approach you choose doesn’t really matter;
Line 157: just be consistent in your choice throughout a project, so it’s easy to know where to
Line 158: find the tests for a specific item. 
Line 159: I find that placing tests in a test folder allows me to also put helper files under the
Line 160: test folder close to the tests. As for easily navigating between tests and the code
Line 161: under test, there are plugins for most IDEs today that allow you to navigate between
Line 162: code and its tests with a keyboard shortcut.
Line 163: Listing 2.1
Line 164: Hello Jest
Line 165: 
Line 166: --- 페이지 60 ---
Line 167: 32
Line 168: CHAPTER 2
Line 169: A first unit test
Line 170: Figure 2.1
Line 171: Terminal output from Jest
Line 172: 1
Line 173: 2
Line 174: 3
Line 175: 4
Line 176: 5
Line 177: 6
Line 178: 7
Line 179: 8
Line 180: 9
Line 181: Figure 2.2
Line 182: Annotated terminal output from Jest
Line 183: 
Line 184: --- 페이지 61 ---
Line 185: 33
Line 186: 2.2
Line 187: The library, the assert, the runner, and the reporter
Line 188: Imagine trying to write all this reporting functionality yourself. It’s possible, but who’s
Line 189: got the time and the inclination? Plus, you’d have to take care of any bugs in the
Line 190: reporting mechanism. 
Line 191:  If we change goodbye to hello in the test, we can see what happens when the test
Line 192: passes (figure 2.3). Nice and green, as all things should be (again, in the digital ver-
Line 193: sion—otherwise it’s nice and grey).
Line 194: You might note that it takes 1.5 seconds to run this single Hello World test. If we used
Line 195: the command jest --watch instead, we could have Jest monitor filesystem activity in
Line 196: our folder and automatically run tests for files that have changed without re-initializ-
Line 197: ing itself every time. This can save a considerable amount of time, and it really helps
Line 198: with the whole notion of continuous testing. Set a terminal in the other window of your
Line 199: workstation with jest --watch on it, and you can keep coding and getting fast feed-
Line 200: back on issues you might be creating. That’s a good way to get into the flow of things.
Line 201:  Jest also supports async-style testing and callbacks. I’ll touch on these when we get
Line 202: to those topics later in the book, but if you’d like to learn more about this style now,
Line 203: head over to the Jest documentation on the subject: https://jestjs.io/docs/en/asyn-
Line 204: chronous.
Line 205: 2.2
Line 206: The library, the assert, the runner, and the reporter
Line 207: Jest has acted in several capacities for us:
Line 208: It acted as a test library to use when writing the test.
Line 209: It acted as an assertion library for asserting inside the test (expect).
Line 210: It acted as the test runner.
Line 211: It acted as the test reporter for the test run.
Line 212: Jest also provides isolation facilities to create mocks, stubs, and spies, though we
Line 213: haven’t seen that yet. We’ll touch on these ideas in later chapters. 
Line 214:  Other than isolation facilities, it’s very common in other languages for a test frame-
Line 215: work to fill all the roles I just mentioned—library, assertions, test runner, and test
Line 216: reporter—but the JavaScript world seems a bit more fragmented. Many other test
Line 217: frameworks provide only some of these facilities. Perhaps this is because the mantra of
Line 218: Figure 2.3
Line 219: Jest terminal 
Line 220: output for a passing test 
Line 221: 
Line 222: --- 페이지 62 ---
Line 223: 34
Line 224: CHAPTER 2
Line 225: A first unit test
Line 226: “do one thing, and do it well” has been taken to heart, or perhaps it’s for other rea-
Line 227: sons. In any case, Jest stands out as one of a handful of all-in-one frameworks. It is a
Line 228: testament to the strength of the open source culture in JavaScript that for each one of
Line 229: these categories, there are multiple tools that you can mix and match to create your
Line 230: own super toolset. 
Line 231:  One of the reasons I chose Jest for this book is so we don’t have to bother too
Line 232: much with the tooling or deal with missing features—we can just focus on the pat-
Line 233: terns. That way we won’t have to use multiple frameworks in a book that is mostly con-
Line 234: cerned with patterns and antipatterns.
Line 235: 2.3
Line 236: What unit testing frameworks offer
Line 237: Let’s zoom out for a second and see where we are. What do frameworks like Jest offer
Line 238: us over creating our own framework, like we started to do in the previous chapter, or
Line 239: over manually testing things? 
Line 240: Structure—Instead of reinventing the wheel every time you want to test a fea-
Line 241: ture, when you use a test framework you always start out the same way—by writ-
Line 242: ing a test with a well-defined structure that everyone can easily recognize, read,
Line 243: and understand.
Line 244: Repeatability—When using a test framework, it’s easy to repeat the act of writing
Line 245: a new test. It’s also easy to repeat the execution of the test, using a test runner,
Line 246: and it’s easy to do this quickly and many times a day. It’s also easy to understand
Line 247: failures and their causes. Someone has already done all the hard work for us,
Line 248: instead of us having to code all that stuff into our hand-rolled framework. 
Line 249: Confidence and time savings—When we roll our own test framework, the frame-
Line 250: work is more likely to have bugs in it, since it is less battle-tested than an existing
Line 251: mature and widely used framework. On the other hand, manually testing things
Line 252: is usually very time consuming. When we’re short on time, we’ll likely focus on
Line 253: testing the things that feel the most critical and skip over things that might feel
Line 254: less important. We could be skipping small but significant bugs. By making it
Line 255: easy to write new tests, it’s more likely that we’ll also write tests for the stuff that
Line 256: feels less significant because we won’t be spending too much time writing tests
Line 257: for the big stuff.
Line 258: Shared understanding—The framework’s reporting can be helpful for managing
Line 259: tasks at the team level (when a test is passing, it means the task is done). Some
Line 260: people find this useful.
Line 261: In short, frameworks for writing, running, and reviewing unit tests and their results
Line 262: can make a huge difference in the daily lives of developers who are willing to invest
Line 263: the time in learning how to use them properly. Figure 2.4 shows the areas in software
Line 264: development in which a unit testing framework and its helper tools have influence,
Line 265: and table 2.1 lists the types of actions we usually execute with a test framework.
Line 266: 
Line 267: --- 페이지 63 ---
Line 268: 35
Line 269: 2.3
Line 270: What unit testing frameworks offer
Line 271: Table 2.1
Line 272: How testing frameworks help developers write and execute tests and review results
Line 273: Unit testing practice
Line 274: How the framework helps
Line 275: Write tests easily and in a 
Line 276: structured manner.
Line 277: A framework supplies the developer with helper functions, assertion func-
Line 278: tions, and structure-related functions.
Line 279: Execute one or all of the 
Line 280: unit tests.
Line 281: A framework provides a test runner, usually at the command line, that 
Line 282: Identifies tests in your code
Line 283: Runs tests automatically
Line 284: Indicates test status while running
Line 285: Review the results of the 
Line 286: test runs.
Line 287: A test runner will usually provide information such as 
Line 288: How many tests ran
Line 289: How many tests didn’t run
Line 290: How many tests failed 
Line 291: Which tests failed
Line 292: The reason tests failed
Line 293: The code location that failed
Line 294: Possibly provide a full stack trace for any exceptions that caused 
Line 295: the test to fail, and let you go to the various method calls inside the 
Line 296: call stack
Line 297: Unit tests
Line 298: Write
Line 299: tests
Line 300: Review
Line 301: results
Line 302: Run
Line 303: tests
Line 304: Run
Line 305: Code
Line 306: Unit testing framework
Line 307: Figure 2.4
Line 308: Unit tests are written as code, using libraries from the unit testing 
Line 309: framework. The tests are run from a test runner inside the IDE or through the 
Line 310: command line, and the results are reviewed through a test reporter (either as 
Line 311: output text or in the IDE) by the developer or an automated build process.
Line 312: 
Line 313: --- 페이지 64 ---
Line 314: 36
Line 315: CHAPTER 2
Line 316: A first unit test
Line 317: At the time of writing, there are around 900 unit testing frameworks out there, with
Line 318: more than a couple for most programming languages in public use (and a few dead
Line 319: ones). You can find a good list on Wikipedia: https://en.wikipedia.org/wiki/List_
Line 320: of_unit_testing_frameworks. 
Line 321: NOTE
Line 322: Using a unit testing framework doesn’t ensure that the tests you write
Line 323: are readable, maintainable, or trustworthy, or that they cover all the logic you’d
Line 324: like to test. We’ll look at how to ensure your unit tests have these properties in
Line 325: chapters 7 through 9 and in various other places throughout this book. 
Line 326: 2.3.1
Line 327: The xUnit frameworks
Line 328: When I started writing tests (in the Visual Basic days), the standard by which most unit
Line 329: test frameworks were measured was collectively called xUnit. The grandfather of the
Line 330: xUnit frameworks idea was SUnit, the unit testing framework for Smalltalk. 
Line 331:  These unit testing frameworks’ names usually start with the first letters of the lan-
Line 332: guage for which they were built; you might have CppUnit for C++, JUnit for Java,
Line 333: NUnit and xUnit for .NET, and HUnit for the Haskell programming language. Not all
Line 334: of them follow these naming guidelines, but most do.
Line 335: 2.3.2
Line 336: xUnit, TAP, and Jest structures
Line 337: It’s not just the names that were reasonably consistent. If you were using an xUnit
Line 338: framework, you could also expect a specific structure in which the tests were built.
Line 339: When these frameworks would run, they would output their results in the same struc-
Line 340: ture, which was usually an XML file with a specific schema.
Line 341:  This type of xUnit XML report is still prevalent today, and it’s widely used in most
Line 342: build tools, such as Jenkins, which support this format with native plugins and use it to
Line 343: report the results of test runs. Most unit test frameworks in static languages still use
Line 344: the xUnit model for structure, which means that once you’ve learned to use one of
Line 345: them, you should be able to easily use any of them (assuming you know the particular
Line 346: programming language).
Line 347:  The other interesting standard for the reporting structure of test results and more
Line 348: is called TAP, the Test Anything Protocol. TAP started life as part of the test harness for
Line 349: Perl, but now it has implementations in C, C++, Python, PHP, Perl, Java, JavaScript,
Line 350: and other languages. TAP is much more than just a reporting specification. In the
Line 351: JavaScript world, the TAP framework is the best-known test framework that natively
Line 352: supports the TAP protocol.
Line 353:  Jest is not strictly an xUnit or TAP framework. Its output is not xUnit- or TAP-
Line 354: compliant by default. However, because xUnit-style reporting still rules the build
Line 355: sphere, we’ll usually want to adapt to that protocol for our reporting on a build server.
Line 356: To get Jest test results that are easily recognized by most build tools, you can install
Line 357: npm modules such as jest-xunit (if you want TAP-specific output, use jest-tap-
Line 358: reporter) and then use a special jest.config.js file in your project to configure Jest to
Line 359: alter its reporting format. 
Line 360: 
Line 361: --- 페이지 65 ---
Line 362: 37
Line 363: 2.5
Line 364: The first Jest test for verifyPassword
Line 365:  Now let’s move on and write something that feels a bit more like a real test with
Line 366: Jest, shall we?
Line 367: 2.4
Line 368: Introducing the Password Verifier project
Line 369: The project that we’ll mostly use for testing examples in this book will start out simple,
Line 370: containing only one function. As the book moves along, we’ll extend that project with
Line 371: new features, modules, and classes to demonstrate different aspects of unit testing.
Line 372: We’ll call it the Password Verifier project.
Line 373:  The first scenario is pretty simple. We’ll be building a password verification library,
Line 374: and it will just be a function at first. The function, verifyPassword(rules), allows us
Line 375: to put in custom verification functions dubbed rules, and it outputs the list of errors,
Line 376: according to the rules that have been input. Each rule function will output two fields: 
Line 377: {
Line 378:     passed: (boolean),
Line 379:     reason: (string)
Line 380: } 
Line 381: In this book, I’ll teach you to write tests that check verifyPassword’s functionality in
Line 382: multiple ways as we add more features to it.
Line 383:  The following listing shows version 0 of this function, with a very naive implemen-
Line 384: tation.
Line 385: const verifyPassword = (input, rules) => {
Line 386:   const errors = [];
Line 387:   rules.forEach(rule => {
Line 388:     const result = rule(input);
Line 389:     if (!result.passed) {
Line 390:       errors.push(`error ${result.reason}`);
Line 391:     }
Line 392:   });
Line 393:   return errors;
Line 394: };
Line 395: Granted, this is not the most functional-style code, and we might refactor it a bit later,
Line 396: but I wanted to keep things very simple here so we can focus on the tests.
Line 397:  The function doesn’t really do much. It iterates over all the rules given and runs
Line 398: each one with the supplied input. If the rule’s result is not passed, then an error is
Line 399: added to the final errors array that is returned as the final result.
Line 400: 2.5
Line 401: The first Jest test for verifyPassword
Line 402: Assuming you have Jest installed, you can go ahead and create a new file named
Line 403: password-verifier0.spec.js under the __tests__ folder. 
Line 404:  Using the __tests__ folder is only one convention for organizing your tests, and it’s
Line 405: part of Jest’s default configuration. There are many who prefer to place the test files
Line 406: Listing 2.2
Line 407: Password Verifier version 0
Line 408: 
Line 409: --- 페이지 66 ---
Line 410: 38
Line 411: CHAPTER 2
Line 412: A first unit test
Line 413: alongside the code being tested. There are pros and cons to each approach, and we’ll
Line 414: get into that in later parts of the book. For now, we’ll go with the defaults.
Line 415:  Here’s a first version of a test against our new function.
Line 416: test('badly named test', () => {
Line 417:   const fakeRule = input =>                      
Line 418:     ({ passed: false, reason: 'fake reason' });  
Line 419:   const errors = verifyPassword('any value', [fakeRule]);   
Line 420:   expect(errors[0]).toMatch('fake reason');  
Line 421: });
Line 422: 2.5.1
Line 423: The Arrange-Act-Assert pattern
Line 424: The structure of the test in listing 2.3 is colloquially called the Arrange-Act-Assert (AAA)
Line 425: pattern. It’s quite nice! I find it very easy to reason about the parts of a test by saying
Line 426: things like “that ‘arrange’ part is too complicated” or “where is the ‘act’ part?”
Line 427:  In the arrange part, we’re creating a fake rule that always returns false, so that we
Line 428: can prove it’s actually used by asserting on its reason at the end of the test. We then
Line 429: send it to verifyPassword along with a simple input. We check in the assert section
Line 430: that the first error we get matches the fake reason we gave in the arrange part.
Line 431: .toMatch(/string/) uses a regular expression to find a part of the string. It’s the
Line 432: same as using .toContain('fake reason').
Line 433:  It’s tedious to run Jest manually after we write a test or fix something, so let’s con-
Line 434: figure npm to run Jest automatically. Go to package.json in the root folder of ch2 and
Line 435: add the following items under the scripts item:
Line 436: "scripts": {
Line 437:    "test": "jest",
Line 438:    "testw": "jest --watch" //if not using git, change to --watchAll
Line 439: },
Line 440: If you don’t have Git initialized in this folder, you can use the command --watchAll
Line 441: instead of --watch.
Line 442:  If everything went well, you can now type npm test in the command line from the
Line 443: ch2 folder, and Jest will run the tests once. If you type npm run testw, Jest will run and
Line 444: wait for changes in an endless loop, until you kill the process with Ctrl-C. (You need to
Line 445: use the word run because testw is not one of the special keywords that npm recog-
Line 446: nizes automatically.)
Line 447:  If you run the test, you can see that it passes, since the function works as expected. 
Line 448: Listing 2.3
Line 449: The first test against verifyPassword()
Line 450: Setting up inputs 
Line 451: for the test
Line 452: Invoking the 
Line 453: entry point with 
Line 454: the inputs
Line 455: Checking the exit point
Line 456: 
Line 457: --- 페이지 67 ---
Line 458: 39
Line 459: 2.5
Line 460: The first Jest test for verifyPassword
Line 461: 2.5.2
Line 462: Testing the test
Line 463: Let’s put a bug in the production code and see if the test fails when it should.
Line 464: const verifyPassword = (input, rules) => {
Line 465:   const errors = [];
Line 466:   rules.forEach(rule => {
Line 467:     const result = rule(input);
Line 468:     if (!result.passed) {
Line 469:       // errors.push(`error ${result.reason}`);  
Line 470:     }
Line 471:   });
Line 472:   return errors;
Line 473: };
Line 474: You should now see your test failing with a nice message. Let’s uncomment the line
Line 475: and see the test pass again. This is a great way to gain some confidence in your tests, if
Line 476: you’re not doing test-driven development and are writing the tests after the code.
Line 477: 2.5.3
Line 478: USE naming
Line 479: Our test has a really bad name. It doesn’t explain anything about what we’re trying to
Line 480: accomplish here. I like to put three pieces of information in test names, so that the
Line 481: reader of the test will be able to answer most of their mental questions just by looking
Line 482: at the test name. These three parts include
Line 483: The unit of work under test (the verifyPassword function, in this case)
Line 484: The scenario or inputs to the unit (the failed rule)
Line 485: The expected behavior or exit point (returns an error with a reason)
Line 486: During the review process, Tyler Lemke, a reviewer of the book, came up with a nice
Line 487: acronym for this, USE: unit under test, scenario, expectation. I like it, and it’s easy to
Line 488: remember. Thanks Tyler!
Line 489:  The following listing shows our next revision of the test with a USE name.
Line 490: test('verifyPassword, given a failing rule, returns errors', () => {
Line 491:   const fakeRule = input => ({ passed: false, reason: 'fake reason' });
Line 492:   const errors = verifyPassword('any value', [fakeRule]);
Line 493:   expect(errors[0]).toContain('fake reason');
Line 494: });
Line 495: This is a bit better. When a test fails, especially during a build process, you don’t see
Line 496: comments or the full test code. You usually only see the name of the test. The name
Line 497: should be so clear that you might not even have to look at the test code to understand
Line 498: where the production code problem might be.
Line 499: Listing 2.4
Line 500: Adding a bug
Line 501: Listing 2.5
Line 502: Naming a test with USE
Line 503: We've accidentally 
Line 504: commented out 
Line 505: this line.
Line 506: 
Line 507: --- 페이지 68 ---
Line 508: 40
Line 509: CHAPTER 2
Line 510: A first unit test
Line 511: 2.5.4
Line 512: String comparisons and maintainability
Line 513: We also made another small change in the following line:
Line 514: expect(errors[0]).toContain('fake reason');
Line 515: Instead of checking that one string is equal to another, as is very common in tests, we
Line 516: are checking that a string is contained in the output. This makes our test less brittle
Line 517: for future changes to the output. We can use .toContain or .toMatch(/fake reason/),
Line 518: which uses a regular expression to match a part of the string, to achieve this. 
Line 519:  Strings are a form of user interface. They are visible to humans, and they might
Line 520: change—especially the edges of strings. We might add whitespace, tabs, asterisks, or
Line 521: other embellishments to a string. We care that the core of the information contained in
Line 522: the string exists. We don’t want to change our test every time someone adds a new line
Line 523: to the end of a string. This is part of the thinking we want to encourage in our tests:
Line 524: test maintainability over time, and resistance to test brittleness, are of high priority. 
Line 525:  We’d ideally like the test to fail only when something is actually wrong in the pro-
Line 526: duction code. We’d like to reduce the number of false positives to a minimum. Using
Line 527: toContain() or toMatch() is a great way to move toward that goal. 
Line 528:  I’ll talk about more ways to improve test maintainability throughout the book, and
Line 529: especially in part 2 of the book.
Line 530: 2.5.5
Line 531: Using describe()
Line 532: We can use Jest’s describe() function to create a bit more structure around our test
Line 533: and to start separating the three USE pieces of information from each other. This step
Line 534: and the ones after it are completely up you—you can decide how you want to style
Line 535: your test and its readability structure. I’m showing you these steps because many peo-
Line 536: ple either don’t use describe() in an effective way, or they ignore it altogether. It can
Line 537: be quite useful.
Line 538:  The describe() functions wrap our tests with context: both logical context for the
Line 539: reader, and functional context for the test itself. The next listing shows how we can
Line 540: start using them.
Line 541: describe('verifyPassword', () => {
Line 542:   test('given a failing rule, returns errors', () => {
Line 543:     const fakeRule = input =>
Line 544:       ({ passed: false, reason: 'fake reason' });
Line 545:     const errors = verifyPassword('any value', [fakeRule]);
Line 546:     expect(errors[0]).toContain('fake reason');
Line 547:   });
Line 548: });
Line 549: Listing 2.6
Line 550: Adding a describe() block
Line 551: 
Line 552: --- 페이지 69 ---
Line 553: 41
Line 554: 2.5
Line 555: The first Jest test for verifyPassword
Line 556: I’ve made four changes here:
Line 557: I’ve added a describe() block that describes the unit of work under test. To
Line 558: me this looks clearer. It also feels like I can now add more nested tests under
Line 559: that block. This describe() block also helps the command-line reporter create
Line 560: nicer reports.
Line 561: I’ve nested the test under the new block and removed the name of the unit of
Line 562: work from the test.
Line 563: I’ve added the input into the fake rule’s reason string. 
Line 564: I’ve added an empty line between the arrange, act, and assert parts to make the
Line 565: test more readable, especially to someone new to the team.
Line 566: 2.5.6
Line 567: Structure implying context
Line 568: The nice thing about describe() is that it can be nested under itself. So we can use it
Line 569: to create another level that explains the scenario, and under that we’ll nest our test. 
Line 570: describe('verifyPassword', () => {
Line 571:   describe('with a failing rule', () => {
Line 572:     test('returns errors', () => {
Line 573:       const fakeRule = input => ({ passed: false,
Line 574:                                    reason: 'fake reason' });
Line 575:       const errors = verifyPassword('any value', [fakeRule]);
Line 576:       expect(errors[0]).toContain('fake reason');
Line 577:     });
Line 578:   });
Line 579: });
Line 580: Some people will hate it, but I think there’s a certain elegance to it. This nesting
Line 581: allows us to separate the three pieces of critical information to their own level. In
Line 582: fact, we can also extract the false rule outside of the test right under the relevant
Line 583: describe(), if we wish to.
Line 584: describe('verifyPassword', () => {
Line 585:   describe('with a failing rule', () => {
Line 586:     const fakeRule = input => ({ passed: false,
Line 587:                                  reason: 'fake reason' });
Line 588:     test('returns errors', () => {
Line 589:       const errors = verifyPassword('any value', [fakeRule]);
Line 590:       expect(errors[0]).toContain('fake reason');
Line 591:     });
Line 592:   });
Line 593: });
Line 594: Listing 2.7
Line 595: Nested describes for extra context
Line 596: Listing 2.8
Line 597: Nested describes with an extracted input
Line 598: 
Line 599: --- 페이지 70 ---
Line 600: 42
Line 601: CHAPTER 2
Line 602: A first unit test
Line 603: For the next example, I’ll move this rule back into the test (I like it when things are
Line 604: close together—more on that later).
Line 605:  This nesting structure also implies very nicely that under a specific scenario you
Line 606: could have more than one expected behavior. You could check multiple exit points
Line 607: under a scenario, with each one as a separate test, and it will still make sense from the
Line 608: reader’s point of view. 
Line 609: 2.5.7
Line 610: The it() function
Line 611: There’s one missing piece to the puzzle I’ve been building so far. Jest also exposes an
Line 612: it() function. This function is, for all intents and purposes, an alias to the test()
Line 613: function, but it fits in more nicely in terms of syntax with the describe-driven
Line 614: approach outlined so far.
Line 615:  The following listing shows what the test looks like when I replace test() with it().
Line 616: describe('verifyPassword', () => {
Line 617:   describe('with a failing rule', () => {
Line 618:     it('returns errors', () => {
Line 619:       const fakeRule = input => ({ passed: false,
Line 620:                                    reason: 'fake reason' });
Line 621:       const errors = verifyPassword('any value', [fakeRule]);
Line 622:       expect(errors[0]).toContain('fake reason');
Line 623:     });
Line 624:   });
Line 625: });
Line 626: In this test, it’s very easy to understand what it refers to. This is a natural extension of
Line 627: the previous describe() blocks. Again, it’s up to you whether you want to use this
Line 628: style. I’m showing one variation of how I like to think about it.
Line 629: 2.5.8
Line 630: Two Jest flavors
Line 631: As you’ve seen, Jest supports two main ways to write tests: a terse test syntax, and a
Line 632: more describe-driven (i.e., hierarchical) syntax. 
Line 633:  The describe-driven Jest syntax can be largely attributed to Jasmine, one of the
Line 634: oldest JavaScript test frameworks. The style itself can be traced back to Ruby-land and
Line 635: the well-known RSpec Ruby test framework. This nested style is usually called BDD
Line 636: style, referring to behavior-driven development. 
Line 637:  You can mix and match these styles as you like (I do). You can use the test syntax
Line 638: when it’s easy to understand your test target and all of its context, without going to too
Line 639: much trouble. The describe syntax can help when you’re expecting multiple results
Line 640: from the same entry point under the same scenario. I’m showing them both here
Line 641: because I sometimes use the terse test flavor and sometimes use the describe-driven
Line 642: flavor, depending on the complexity and expressiveness requirements.
Line 643: Listing 2.9
Line 644: Replacing test() with it()
Line 645: 
Line 646: --- 페이지 71 ---
Line 647: 43
Line 648: 2.5
Line 649: The first Jest test for verifyPassword
Line 650: 2.5.9
Line 651: Refactoring the production code
Line 652: Since there are many ways to build the same thing in JavaScript, I thought I’d show a
Line 653: couple of variations on our design and what happens if we change it. Suppose we’d
Line 654: like to make the password verifier an object with state.
Line 655:  One reason to change the design into a stateful one might be that I intend for dif-
Line 656: ferent parts of the application to use this object. One part will configure and add rules
Line 657: to it, and a different part will use it to do the verification. Another reason is that we
Line 658: need to know how to handle a stateful design and look at which directions it pulls our
Line 659: tests in, and what we can do about that.
Line 660:  Let’s look at the production code first.
Line 661: class PasswordVerifier1 {
Line 662:   constructor () {
Line 663:     this.rules = [];
Line 664:   }
Line 665:   addRule (rule) {
Line 666:     this.rules.push(rule);
Line 667:   }
Line 668:   verify (input) {
Line 669:     const errors = [];
Line 670:     this.rules.forEach(rule => {
Line 671:       const result = rule(input);
Line 672:       if (result.passed === false) {
Line 673:         errors.push(result.reason);
Line 674:       }
Line 675: BDD’s dark present
Line 676: BDD has quite an interesting background that might be worth talking about. BDD isn’t
Line 677: related to TDD. Dan North, the person most associated with inventing the term, refers
Line 678: to BDD as using stories and examples to describe how an application should behave.
Line 679: Mainly this is targeted at working with non-technical stakeholders—product owners,
Line 680: customers, etc. RSpec (inspired by RBehave) brought the story-driven approach to
Line 681: the masses, and in the process, many other frameworks came along, including the
Line 682: famous Cucumber.
Line 683: There is also a dark side to this story: many frameworks have been developed and
Line 684: used solely by developers without working with non-technical stakeholders, in com-
Line 685: plete opposition to the main ideas of BDD.
Line 686: Today, to me, the term BDD frameworks mainly means “test frameworks with some
Line 687: syntactic sugar,” since they are almost never used to create real conversations
Line 688: between stakeholders and are almost always used as just another shiny or pre-
Line 689: scribed tool for performing developer-based automated tests. I’ve even seen the
Line 690: mighty Cucumber fall into this pattern.
Line 691: Listing 2.10
Line 692: Refactoring a function to a stateful class
Line 693: 
Line 694: --- 페이지 72 ---
Line 695: 44
Line 696: CHAPTER 2
Line 697: A first unit test
Line 698:     });
Line 699:     return errors;
Line 700:   }
Line 701: }
Line 702: I’ve highlighted the main changes from listing 2.9. There’s nothing really special
Line 703: going on here, though this may feel more comfortable if you’re coming from an
Line 704: object-oriented background. It’s important to note that this is just one way to design
Line 705: this functionality. I’m using the class-based approach so that I can show how this
Line 706: design affects the test.
Line 707:  In this new design, where are the entry and exit points for the current scenario?
Line 708: Think about it for a second. The scope of the unit of work has increased. To test a sce-
Line 709: nario with a failing rule, we would have to invoke two functions that affect the state of
Line 710: the unit under test: addRule and verify.
Line 711:  Now let’s see what the test might look like (changes are highlighted as usual).
Line 712: describe('PasswordVerifier', () => {
Line 713:   describe('with a failing rule', () => {
Line 714:     it('has an error message based on the rule.reason', () => {
Line 715:       const verifier = new PasswordVerifier1();
Line 716:       const fakeRule = input => ({ passed: false,
Line 717:                                    reason: 'fake reason'});
Line 718:       verifier.addRule(fakeRule);
Line 719:       const errors = verifier.verify('any value');
Line 720:       expect(errors[0]).toContain('fake reason');
Line 721:     });
Line 722:   });
Line 723: });
Line 724: So far, so good; nothing fancy is happening here. Note that the surface of the unit of
Line 725: work has increased. It now spans two related functions that must work together
Line 726: (addRule and verify). There is a coupling that occurs due to the stateful nature of the
Line 727: design. We need to use two functions to test productively without exposing any inter-
Line 728: nal state from the object.
Line 729:  The test itself looks innocent enough. But what happens when we want to write sev-
Line 730: eral tests for the same scenario? That would happen if we have multiple exit points, or
Line 731: if we want to test multiple results from the same exit point. For example, let’s say we
Line 732: want to verify that we have only a single error. We could simply add a line to the test
Line 733: like this:
Line 734: verifier.addRule(fakeRule);
Line 735: const errors = verifier.verify('any value');
Line 736: expect(errors.length).toBe(1);       
Line 737: expect(errors[0]).toContain('fake reason');
Line 738: Listing 2.11
Line 739: Testing the stateful unit of work
Line 740: A new 
Line 741: assertion
Line 742: 
Line 743: --- 페이지 73 ---
Line 744: 45
Line 745: 2.6
Line 746: Trying the beforeEach() route
Line 747: What happens if the new assertion fails? The second assertion would never execute,
Line 748: because the test runner would receive an error and move on to the next test case.
Line 749:  We’d still want to know if the second assertion would have passed, right? So maybe
Line 750: we’d start commenting out the first one and rerunning the test. That’s not a healthy
Line 751: way to run your tests. In Gerard Meszaros’ book xUnit Test Patterns, this human behav-
Line 752: ior of commenting things out to test other things is called assertion roulette. It can cre-
Line 753: ate lots of confusion and false positives in your test runs (thinking that something is
Line 754: failing or passing when it isn’t).
Line 755:  I’d rather separate this extra check into its own test case with a good name, as follows.
Line 756: describe('PasswordVerifier', () => {
Line 757:   describe('with a failing rule', () => {
Line 758:     it('has an error message based on the rule.reason', () => {
Line 759:       const verifier = new PasswordVerifier1();
Line 760:       const fakeRule = input => ({ passed: false,
Line 761:                                    reason: 'fake reason'});
Line 762:       verifier.addRule(fakeRule);
Line 763:       const errors = verifier.verify('any value');
Line 764:       expect(errors[0]).toContain('fake reason');
Line 765:     });
Line 766:     it('has exactly one error', () => {
Line 767:       const verifier = new PasswordVerifier1();
Line 768:       const fakeRule = input => ({ passed: false,
Line 769:                                    reason: 'fake reason'});
Line 770:       verifier.addRule(fakeRule);
Line 771:       const errors = verifier.verify('any value');
Line 772:       expect(errors.length).toBe(1);
Line 773:     });
Line 774:   });
Line 775: });
Line 776: This is starting to look bad. Yes, we have solved the assertion roulette issue. Each it()
Line 777: can fail separately and not interfere with the results from the other test case. But what
Line 778: did it cost? Everything. Look at all the duplication we have now. At this point, those of
Line 779: you with some unit testing background will start shouting at the book: “Use a
Line 780: setup/beforeEach method!”
Line 781:  Fine!
Line 782: 2.6
Line 783: Trying the beforeEach() route
Line 784: I haven’t introduced beforeEach() yet. This function and its sibling, afterEach(),
Line 785: are used to set up and tear down a specific state required by the test cases. There’s also
Line 786: beforeAll() and afterAll(), which I try to avoid using at all costs for unit testing sce-
Line 787: narios. We’ll talk more about the siblings later in the book. 
Line 788: Listing 2.12
Line 789: Checking an extra end result from the same exit point
Line 790: 
Line 791: --- 페이지 74 ---
Line 792: 46
Line 793: CHAPTER 2
Line 794: A first unit test
Line 795:  beforeEach() can help us remove duplication in our tests because it runs once
Line 796: before each test in the describe block in which we nest it. We can also nest it multiple
Line 797: times, as the following listing demonstrates.
Line 798: describe('PasswordVerifier', () => {
Line 799:   let verifier;
Line 800:   beforeEach(() => verifier = new PasswordVerifier1());   
Line 801:   describe('with a failing rule', () => {
Line 802:     let fakeRule, errors;
Line 803:     beforeEach(() => {                             
Line 804:       fakeRule = input => ({passed: false, reason: 'fake reason'});
Line 805:       verifier.addRule(fakeRule);
Line 806:     });
Line 807:     it('has an error message based on the rule.reason', () => {
Line 808:       const errors = verifier.verify('any value');
Line 809:       expect(errors[0]).toContain('fake reason');
Line 810:     });
Line 811:     it('has exactly one error', () => {
Line 812:       const errors = verifier.verify('any value');
Line 813:       expect(errors.length).toBe(1);
Line 814:     });
Line 815:   });
Line 816: });
Line 817: Look at all that extracted code. 
Line 818:  In the first beforeEach(), we’re setting up a new PasswordVerifier1 that will be
Line 819: created for each test case. In the beforeEach() after that, we’re setting up a fake rule
Line 820: and adding it to the new verifier for every test case under that specific scenario. If we
Line 821: had other scenarios, the second beforeEach() in line 6 wouldn’t run for them, but
Line 822: the first one would.
Line 823:  The tests seem shorter now, which ideally is what you want in a test, to make it
Line 824: more readable and maintainable. We removed the creation line from each test and
Line 825: reused the same higher-level variable verifier. 
Line 826:  There are a couple of caveats:
Line 827: We forgot to reset the errors array in beforeEach() on line 6. That could bite
Line 828: us later on. 
Line 829: Jest runs unit tests in parallel by default. This means that moving the verifier to
Line 830: line 2 may cause an issue with parallel tests, where the verifier could be over-
Line 831: written by a different test on a parallel run, which would screw up the state of
Line 832: our running test. Jest is quite different from unit test frameworks in most other
Line 833: languages I know, which make a point of running tests in a single thread, not in
Line 834: parallel (at least by default), to avoid such issues. With Jest, we have to remem-
Line 835: ber that parallel tests are a reality, so stateful tests with a shared upper state, like
Line 836: Listing 2.13
Line 837: Using beforeEach() on two levels
Line 838: Setting up a new 
Line 839: verifier that will be 
Line 840: used in each test
Line 841: Setting up a fake
Line 842: rule that will be
Line 843: used within this
Line 844: describe() method
Line 845: 
Line 846: --- 페이지 75 ---
Line 847: 47
Line 848: 2.6
Line 849: Trying the beforeEach() route
Line 850: we have at line 2, can potentially be problematic and cause flaky tests that fail
Line 851: for unknown reasons.
Line 852: We’ll correct both of these issues soon.
Line 853: 2.6.1
Line 854: beforeEach() and scroll fatigue
Line 855: We lost a couple of things in the process of refactoring to beforeEach():
Line 856: If I’m trying to read only the it() parts, I can’t tell where the verifier is cre-
Line 857: ated and declared. I’d have to scroll up to understand.
Line 858: The same goes for understanding what rule was added. I’d have to look one
Line 859: level above the it() to see what rule was added, or look up the describe()
Line 860: block description. 
Line 861: Right now, this doesn’t seem so bad. But we’ll see later that this structure starts to get a
Line 862: bit hairy as the scenario list increases in size. Larger files can bring about what I like to
Line 863: call scroll fatigue, requiring the test reader to scroll up and down the test file to under-
Line 864: stand the context and state of the tests. This makes maintaining and reading the tests
Line 865: a chore instead of a simple act of reading. 
Line 866:  This nesting is great for reporting, but it sucks for humans who have to keep look-
Line 867: ing up where something came from. If you’ve ever tried to debug CSS styles in the
Line 868: browser’s inspector window, you’ll know the feeling. You’ll see that a specific cell is
Line 869: bold for some reason. Then you scroll up to see which style made that <div> inside
Line 870: nested cells in a special table under the third node bold.
Line 871:  Let’s see what happens when we take it one step further in the following listing.
Line 872: Since we’re in the process of removing duplication, we can also call verify in
Line 873: beforeEach() and remove an extra line from each it(). This is basically putting the
Line 874: arrange and act parts from the AAA pattern into the beforeEach() function.
Line 875: describe('PasswordVerifier', () => {
Line 876:   let verifier;
Line 877:   beforeEach(() => verifier = new PasswordVerifier1());
Line 878:   describe('with a failing rule', () => {
Line 879:     let fakeRule, errors;
Line 880:     beforeEach(() => {
Line 881:       fakeRule = input => ({passed: false, reason: 'fake reason'});
Line 882:       verifier.addRule(fakeRule);
Line 883:       errors = verifier.verify('any value');
Line 884:     });
Line 885:     it('has an error message based on the rule.reason', () => {
Line 886:       expect(errors[0]).toContain('fake reason');
Line 887:     });
Line 888:     it('has exactly one error', () => {
Line 889:       expect(errors.length).toBe(1);
Line 890:     });
Line 891:   });
Line 892: });
Line 893: Listing 2.14
Line 894: Pushing the arrange and act parts into beforeEach()
Line 895: 
Line 896: --- 페이지 76 ---
Line 897: 48
Line 898: CHAPTER 2
Line 899: A first unit test
Line 900: The code duplication has been reduced to a minimum, but now we also need to look
Line 901: up where and how we got the errors array if we want to understand each it(). 
Line 902:  Let’s double down and add a few more basic scenarios, and see if this approach is
Line 903: scalable as the problem space increases.
Line 904: describe('v6 PasswordVerifier', () => {
Line 905:   let verifier;
Line 906:   beforeEach(() => verifier = new PasswordVerifier1());
Line 907:   describe('with a failing rule', () => {
Line 908:     let fakeRule, errors;
Line 909:     beforeEach(() => {
Line 910:       fakeRule = input => ({passed: false, reason: 'fake reason'});
Line 911:       verifier.addRule(fakeRule);
Line 912:       errors = verifier.verify('any value');
Line 913:     });
Line 914:     it('has an error message based on the rule.reason', () => {
Line 915:       expect(errors[0]).toContain('fake reason');
Line 916:     });
Line 917:     it('has exactly one error', () => {
Line 918:       expect(errors.length).toBe(1);
Line 919:     });
Line 920:   });
Line 921:   describe('with a passing rule', () => {
Line 922:     let fakeRule, errors;
Line 923:     beforeEach(() => {
Line 924:       fakeRule = input => ({passed: true, reason: ''});
Line 925:       verifier.addRule(fakeRule);
Line 926:       errors = verifier.verify('any value');
Line 927:     });
Line 928:     it('has no errors', () => {
Line 929:       expect(errors.length).toBe(0);
Line 930:     });
Line 931:   });
Line 932:   describe('with a failing and a passing rule', () => {
Line 933:     let fakeRulePass,fakeRuleFail, errors;
Line 934:     beforeEach(() => {
Line 935:       fakeRulePass = input => ({passed: true, reason: 'fake success'});
Line 936:       fakeRuleFail = input => ({passed: false, reason: 'fake reason'});
Line 937:       verifier.addRule(fakeRulePass);
Line 938:       verifier.addRule(fakeRuleFail);
Line 939:       errors = verifier.verify('any value');
Line 940:     });
Line 941:     it('has one error', () => {
Line 942:       expect(errors.length).toBe(1);
Line 943:     });
Line 944:     it('error text belongs to failed rule', () => {
Line 945:       expect(errors[0]).toContain('fake reason');
Line 946:     });
Line 947:   });
Line 948: });
Line 949: Listing 2.15
Line 950: Adding extra scenarios
Line 951: 
Line 952: --- 페이지 77 ---
Line 953: 49
Line 954: 2.7
Line 955: Trying the factory method route
Line 956: Do we like this? I don’t. Now we’re seeing a couple of extra problems:
Line 957: I can already start to see lots of repetition in the beforeEach() parts.
Line 958: The potential for scroll fatigue has increased dramatically, with more options of
Line 959: which beforeEach() affects which it() state.
Line 960: In real projects, beforeEach() functions tend to be the garbage bin of the test file.
Line 961: People throw all kinds of test-initialized stuff in there: things that only some tests need,
Line 962: things that affect all the other tests, and things that nobody uses anymore. It’s human
Line 963: nature to put things in the easiest place possible, especially if everyone else before you
Line 964: has done so as well. 
Line 965:  I’m not crazy about the beforeEach() approach. Let’s see if we can mitigate some
Line 966: of these issues while still keeping duplication to a minimum. 
Line 967: 2.7
Line 968: Trying the factory method route
Line 969: Factory methods are simple helper functions that help us build objects or special states
Line 970: and reuse the same logic in multiple places. Perhaps we can reduce some of the dupli-
Line 971: cation and clunky-feeling code by using a couple of factory methods for the failing
Line 972: and passing rules in listing 2.16.
Line 973: describe('PasswordVerifier', () => {
Line 974:   let verifier;
Line 975:   beforeEach(() => verifier = new PasswordVerifier1());
Line 976:   describe('with a failing rule', () => {
Line 977:     let errors;
Line 978:     beforeEach(() => {
Line 979:       verifier.addRule(makeFailingRule('fake reason'));
Line 980:       errors = verifier.verify('any value');
Line 981:     });
Line 982:     it('has an error message based on the rule.reason', () => {
Line 983:       expect(errors[0]).toContain('fake reason');
Line 984:     });
Line 985:     it('has exactly one error', () => {
Line 986:       expect(errors.length).toBe(1);
Line 987:     });
Line 988:   });
Line 989:   describe('with a passing rule', () => {
Line 990:     let errors;
Line 991:     beforeEach(() => {
Line 992:       verifier.addRule(makePassingRule());
Line 993:       errors = verifier.verify('any value');
Line 994:     });
Line 995:     it('has no errors', () => {
Line 996:       expect(errors.length).toBe(0);
Line 997:     });
Line 998:   });
Line 999:   describe('with a failing and a passing rule', () => {
Line 1000:     let errors;
Line 1001: Listing 2.16
Line 1002: Adding a couple of factory methods to the mix
Line 1003: 
Line 1004: --- 페이지 78 ---
Line 1005: 50
Line 1006: CHAPTER 2
Line 1007: A first unit test
Line 1008:     beforeEach(() => {
Line 1009:       verifier.addRule(makePassingRule());
Line 1010:       verifier.addRule(makeFailingRule('fake reason'));
Line 1011:       errors = verifier.verify('any value');
Line 1012:     });
Line 1013:     it('has one error', () => {
Line 1014:       expect(errors.length).toBe(1);
Line 1015:     });
Line 1016:     it('error text belongs to failed rule', () => {
Line 1017:       expect(errors[0]).toContain('fake reason');
Line 1018:     });
Line 1019:   });
Line 1020: . . .
Line 1021:   const makeFailingRule = (reason) => {
Line 1022:     return (input) => {
Line 1023:       return { passed: false, reason: reason };
Line 1024:     };
Line 1025:   };
Line 1026:   const makePassingRule = () => (input) => {
Line 1027:     return { passed: true, reason: '' };
Line 1028:   };
Line 1029: }) 
Line 1030: The makeFailingRule() and makePassingRule() factory methods have made our
Line 1031: beforeEach() functions a little more clear.
Line 1032: 2.7.1
Line 1033: Replacing beforeEach() completely with factory methods
Line 1034: What if we don’t use beforeEach() to initialize various things at all? What if we
Line 1035: switched to using small factory methods instead? Let’s see what that looks like.
Line 1036: const makeVerifier = () => new PasswordVerifier1();
Line 1037: const passingRule = (input) => ({passed: true, reason: ''});
Line 1038: const makeVerifierWithPassingRule = () => {
Line 1039:   const verifier = makeVerifier();
Line 1040:   verifier.addRule(passingRule);
Line 1041:   return verifier;
Line 1042: };
Line 1043: const makeVerifierWithFailedRule = (reason) => {
Line 1044:   const verifier = makeVerifier();
Line 1045:   const fakeRule = input => ({passed: false, reason: reason});
Line 1046:   verifier.addRule(fakeRule);
Line 1047:   return verifier;
Line 1048: };
Line 1049: describe('PasswordVerifier', () => {
Line 1050:   describe('with a failing rule', () => {
Line 1051:     it('has an error message based on the rule.reason', () => {
Line 1052:       const verifier = makeVerifierWithFailedRule('fake reason');
Line 1053: Listing 2.17
Line 1054: Replacing beforeEach() with factory methods
Line 1055: 
Line 1056: --- 페이지 79 ---
Line 1057: 51
Line 1058: 2.7
Line 1059: Trying the factory method route
Line 1060:       const errors = verifier.verify('any input');
Line 1061:       expect(errors[0]).toContain('fake reason');
Line 1062:     });
Line 1063:     it('has exactly one error', () => {
Line 1064:       const verifier = makeVerifierWithFailedRule('fake reason');
Line 1065:       const errors = verifier.verify('any input');
Line 1066:       expect(errors.length).toBe(1);
Line 1067:     });
Line 1068:   });
Line 1069:   describe('with a passing rule', () => {
Line 1070:     it('has no errors', () => {
Line 1071:       const verifier = makeVerifierWithPassingRule();
Line 1072:       const errors = verifier.verify('any input');
Line 1073:       expect(errors.length).toBe(0);
Line 1074:     });
Line 1075:   });
Line 1076:   describe('with a failing and a passing rule', () => {
Line 1077:     it('has one error', () => {
Line 1078:       const verifier = makeVerifierWithFailedRule('fake reason');
Line 1079:       verifier.addRule(passingRule);
Line 1080:       const errors = verifier.verify('any input');
Line 1081:       expect(errors.length).toBe(1);
Line 1082:     });
Line 1083:     it('error text belongs to failed rule', () => {
Line 1084:       const verifier = makeVerifierWithFailedRule('fake reason');
Line 1085:       verifier.addRule(passingRule);
Line 1086:       const errors = verifier.verify('any input');
Line 1087:       expect(errors[0]).toContain('fake reason');
Line 1088:     });
Line 1089:   });
Line 1090: });
Line 1091: The length here is about the same as in listing 2.16, but I find the code to be more
Line 1092: readable and thus more easily maintained. We’ve eliminated the beforeEach() func-
Line 1093: tions, but we didn’t lose maintainability. The amount of repetition we’ve eliminated is
Line 1094: negligible, but the readability has improved greatly due to the removal of the nested
Line 1095: beforeEach() blocks. 
Line 1096:  Furthermore, we’ve reduced the risk of scroll fatigue. As a reader of the test, I
Line 1097: don’t have to scroll up and down the file to find out when an object is created or
Line 1098: declared. I can glean all the information from the it(). We don’t need to know how
Line 1099: something is created, but we know when it is created and what important parameters it
Line 1100: is initialized with. Everything is explicitly explained.
Line 1101:  If the need arises, I can drill into specific factory methods, and I like that each
Line 1102: it() is encapsulating its own state. The nested describe() structure is a good way to
Line 1103: know where we are, but the state is all triggered from inside the it() blocks, not out-
Line 1104: side of them.
Line 1105: 
Line 1106: --- 페이지 80 ---
Line 1107: 52
Line 1108: CHAPTER 2
Line 1109: A first unit test
Line 1110: 2.8
Line 1111: Going full circle to test()
Line 1112: The tests in listing 2.17 are self-encapsulated enough that the describe() blocks act
Line 1113: only as added sugar for understanding. They are no longer needed if we don’t want
Line 1114: them. If we wanted to, we could write the tests as in the following listing.
Line 1115: test('pass verifier, with failed rule, ' +
Line 1116:           'has an error message based on the rule.reason', () => {
Line 1117:   const verifier = makeVerifierWithFailedRule('fake reason');
Line 1118:   const errors = verifier.verify('any input');
Line 1119:   expect(errors[0]).toContain('fake reason');
Line 1120: });
Line 1121: test('pass verifier, with failed rule, has exactly one error', () => {
Line 1122:   const verifier = makeVerifierWithFailedRule('fake reason');
Line 1123:   const errors = verifier.verify('any input');
Line 1124:   expect(errors.length).toBe(1);
Line 1125: });
Line 1126: test('pass verifier, with passing rule, has no errors', () => {
Line 1127:   const verifier = makeVerifierWithPassingRule();
Line 1128:   const errors = verifier.verify('any input');
Line 1129:   expect(errors.length).toBe(0);
Line 1130: });
Line 1131: test('pass verifier, with passing  and failing rule,' +
Line 1132:           ' has one error', () => {
Line 1133:   const verifier = makeVerifierWithFailedRule('fake reason');
Line 1134:   verifier.addRule(passingRule);
Line 1135:   const errors = verifier.verify('any input');
Line 1136:   expect(errors.length).toBe(1);
Line 1137: });
Line 1138: test('pass verifier, with passing  and failing rule,' +
Line 1139:           ' error text belongs to failed rule', () => {
Line 1140:   const verifier = makeVerifierWithFailedRule('fake reason');
Line 1141:   verifier.addRule(passingRule);
Line 1142:   const errors = verifier.verify('any input');
Line 1143:   expect(errors[0]).toContain('fake reason');
Line 1144: });
Line 1145: The factory methods provide us with all the functionality we need, without losing clar-
Line 1146: ity for each specific test. 
Line 1147:  I kind of like the terseness of listing 2.18. It’s easy to understand. We might lose a
Line 1148: bit of structure clarity here, so there are instances where I go with the describe-less
Line 1149: approach, and there are places where nested describes make things more readable.
Line 1150: The sweet spot of maintainability and readability for your project is probably some-
Line 1151: where between these two points. 
Line 1152: 2.9
Line 1153: Refactoring to parameterized tests
Line 1154: Let’s move away from the verifier class to work on creating and testing a new custom
Line 1155: rule for the verifier. Listing 2.19 shows a simple rule for an uppercase letter (I realize
Line 1156: Listing 2.18
Line 1157: Removing nested describes
Line 1158: 
Line 1159: --- 페이지 81 ---
Line 1160: 53
Line 1161: 2.9
Line 1162: Refactoring to parameterized tests
Line 1163: passwords with these requirements are no longer considered a great idea, but for
Line 1164: demonstration purposes I’m okay with it).
Line 1165: const oneUpperCaseRule = (input) => {
Line 1166:   return {
Line 1167:     passed: (input.toLowerCase() !== input),
Line 1168:     reason: 'at least one upper case needed'
Line 1169:   };
Line 1170: };
Line 1171: We could write a couple of tests as in the following listing.
Line 1172: describe('one uppercase rule', function () {
Line 1173:   test('given no uppercase, it fails', () => {
Line 1174:     const result = oneUpperCaseRule('abc');
Line 1175:     expect(result.passed).toEqual(false);
Line 1176:   });
Line 1177:   test('given one uppercase, it passes', () => {
Line 1178:     const result = oneUpperCaseRule('Abc');
Line 1179:     expect(result.passed).toEqual(true);
Line 1180:   });
Line 1181:   test('given a different uppercase, it passes', () => {
Line 1182:     const result = oneUpperCaseRule('aBc');
Line 1183:     expect(result.passed).toEqual(true);
Line 1184:   });
Line 1185: });
Line 1186: In listing 2.20 I highlighted some duplication we might have if we’re trying out the
Line 1187: same scenario with small variations in the input to the unit of work. In this case, we
Line 1188: want to test that it should not matter where the uppercase letter is, as long as it’s there.
Line 1189: But this duplication will hurt us down the road if we ever want to change the upper-
Line 1190: case logic, or if we need to correct the assertions in some way for that use case.
Line 1191:  There are a few ways to create parameterized tests in JavaScript, and Jest already
Line 1192: includes one that’s built in: test.each (also aliased to it.each). The next listing
Line 1193: shows how we could use this feature to remove duplication in our tests.
Line 1194: describe('one uppercase rule', () => {
Line 1195:   test('given no uppercase, it fails', () => {
Line 1196:     const result = oneUpperCaseRule('abc');
Line 1197:     expect(result.passed).toEqual(false);
Line 1198:   });
Line 1199:   test.each(['Abc',        
Line 1200:              'aBc'])       
Line 1201:     ('given one uppercase, it passes', (input) => {    
Line 1202: Listing 2.19
Line 1203: Password rules
Line 1204: Listing 2.20
Line 1205: Testing a rule with variations
Line 1206: Listing 2.21
Line 1207: Using test.each
Line 1208: Passing in an array 
Line 1209: of values that are 
Line 1210: mapped to the 
Line 1211: input parameter
Line 1212: Using each input 
Line 1213: parameter passed 
Line 1214: in the array
Line 1215: 
Line 1216: --- 페이지 82 ---
Line 1217: 54
Line 1218: CHAPTER 2
Line 1219: A first unit test
Line 1220:       const result = oneUpperCaseRule(input);
Line 1221:       expect(result.passed).toEqual(true);
Line 1222:     });
Line 1223: });
Line 1224: In this example, the test will repeat once for each value in the array. It’s a bit of a
Line 1225: mouthful at first, but once you’ve tried this approach, it becomes easy to use. It’s also
Line 1226: pretty readable. 
Line 1227:  If we want to pass in multiple parameters, we can enclose them in an array, as in
Line 1228: the following listing.
Line 1229: describe('one uppercase rule', () => {
Line 1230:   test.each([ ['Abc', true],           
Line 1231:               ['aBc', true],
Line 1232:               ['abc', false]])           
Line 1233:     ('given %s, %s ', (input, expected) => {   
Line 1234:       const result = oneUpperCaseRule(input);
Line 1235:       expect(result.passed).toEqual(expected);
Line 1236:     });
Line 1237: });
Line 1238: We don’t have to use Jest, though. JavaScript is versatile enough to allow us to roll out
Line 1239: our own parameterized test quite easily if we want to.
Line 1240: describe('one uppercase rule, with vanilla JS for', () => {
Line 1241:   const tests = {
Line 1242:     'Abc': true,
Line 1243:     'aBc': true,
Line 1244:     'abc': false,
Line 1245:   };
Line 1246:   for (const [input, expected] of Object.entries(tests)) {
Line 1247:     test('given ${input}, ${expected}', () => {
Line 1248:       const result = oneUpperCaseRule(input);
Line 1249:       expect(result.passed).toEqual(expected);
Line 1250:     });
Line 1251:   }
Line 1252: });
Line 1253: It’s up to you which one you want to use (I like to keep it simple and use test.each).
Line 1254: The point is, Jest is just a tool. The pattern of parameterized tests can be implemented
Line 1255: in multiple ways. This pattern gives us a lot of power, but also a lot of responsibility. It’s
Line 1256: really easy to abuse this technique and create tests that are harder to understand.
Line 1257:  I usually try to make sure that the same scenario (type of input) holds for the
Line 1258: entire table. If I were reviewing this test in a code review, I would have told the person
Line 1259: Listing 2.22
Line 1260: Refactoring test.each
Line 1261: Listing 2.23
Line 1262: Using a vanilla JavaScript for
Line 1263: Providing three arrays, 
Line 1264: each with two parameters
Line 1265: A new false expectation for a 
Line 1266: missing uppercase character
Line 1267: Jest maps the array values 
Line 1268: to arguments automatically.
Line 1269: 
Line 1270: --- 페이지 83 ---
Line 1271: 55
Line 1272: 2.10
Line 1273: Checking for expected thrown errors
Line 1274: who wrote it that this test is actually testing two different scenarios: one with no upper-
Line 1275: case, and a couple with one uppercase. I would split those out into two different tests.
Line 1276:  In this example, I wanted to show that it’s very easy to get rid of many tests and put
Line 1277: them all in a big test.each—even when it hurts readability—so be careful when run-
Line 1278: ning with these specific scissors.
Line 1279: 2.10
Line 1280: Checking for expected thrown errors
Line 1281: Sometimes we need to design a piece of code that throws an error at the right time
Line 1282: with the right data. What happens if we add code to the verify function that throws
Line 1283: an error if there are no rules configured, as in the next listing?
Line 1284: verify (input) {
Line 1285:   if (this.rules.length === 0) {
Line 1286:     throw new Error('There are no rules configured');
Line 1287:   }
Line 1288:   . . .
Line 1289: We could test it the old-fashioned way by using try/catch, and failing the test if we
Line 1290: don’t get an error.
Line 1291: test('verify, with no rules, throws exception', () => {
Line 1292:     const verifier = makeVerifier();
Line 1293:     try {
Line 1294:         verifier.verify('any input');
Line 1295:         fail('error was expected but not thrown');
Line 1296:     } catch (e) {
Line 1297:         expect(e.message).toContain('no rules configured');
Line 1298:     }
Line 1299: });
Line 1300: This try/catch pattern is an effective method but very verbose and annoying to type.
Line 1301: Jest, like most other frameworks, contains a shortcut to accomplish exactly this type of
Line 1302: scenario, using expect().toThrowError().
Line 1303: Listing 2.24
Line 1304: Throwing an error
Line 1305: Listing 2.25
Line 1306: Testing exceptions with try/catch
Line 1307: Using fail()
Line 1308: Technically, fail() is a leftover API from the original fork of Jasmine, which Jest is
Line 1309: based on. It’s a way to trigger a test failure, but it’s not in the official Jest API docs,
Line 1310: and they would recommend that you use expect.assertions(1) instead. This
Line 1311: would fail the test if you never reached the catch() expectation. I find that as long
Line 1312: as fail() still works, it does the job quite nicely for my purposes, which are to
Line 1313: demonstrate why you shouldn’t use the try/catch construct in a unit test if you can
Line 1314: help it.
Line 1315: 
Line 1316: --- 페이지 84 ---
Line 1317: 56
Line 1318: CHAPTER 2
Line 1319: A first unit test
Line 1320: test('verify, with no rules, throws exception', () => {
Line 1321:     const verifier = makeVerifier();
Line 1322:     expect(() => verifier.verify('any input'))
Line 1323:         .toThrowError(/no rules configured/);   
Line 1324: });
Line 1325: Notice that I’m using a regular expression match to check that the error string con-
Line 1326: tains a specific string, and is not equal to it, so as to make the test a bit more future-
Line 1327: proof if the string changes on its sides. toThrowError has a few variations, and you can
Line 1328: go to https://jestjs.io/ find out all about them.
Line 1329: 2.11
Line 1330: Setting test categories
Line 1331: If you’d like to run only a specific category of tests, such as only unit tests, or only inte-
Line 1332: gration tests, or only tests that touch a specific part of the application, Jest currently
Line 1333: doesn’t have the ability to define test case categories.
Line 1334:  All is not lost, though. Jest has a special --testPathPattern command-line flag,
Line 1335: which allows us to define how Jest will find our tests. We can trigger this command
Line 1336: with a different path for a specific type of test we’d like to run (such as “all tests under
Line 1337: the ‘integration’ folder”). You can get the full details at https://jestjs.io/docs/en/cli.
Line 1338:  Another alternative is to create a separate jest.config.js file for each test category,
Line 1339: each with its own testRegex configuration and other properties.
Line 1340: Listing 2.26
Line 1341: Using expect().toThrowError()
Line 1342: Jest snapshots
Line 1343: Jest has a unique feature called Snapshots. It allows you to render a component
Line 1344: (when working in a framework like React) and then match the current rendering to a
Line 1345: saved snapshot of that component, including all of its properties and HTML. 
Line 1346: I won’t be touching on this too much, but from what I’ve seen, this feature tends to
Line 1347: be abused quite heavily. You can use it to create hard-to-read tests that look some-
Line 1348: thing like this:
Line 1349: it('renders',()=>{
Line 1350:     expect(<MyComponent/>).toMatchSnapshot(); 
Line 1351: });
Line 1352: This is obtuse (hard to reason about what is being tested) and it’s testing many
Line 1353: things that might not be related to one another. It will also break for many reasons
Line 1354: that you might not care about, so the maintainability cost of that test will be higher
Line 1355: over time. It’s also a great excuse not to write readable and maintainable tests,
Line 1356: because you’re on a deadline but still have to show you write tests. Yes, it does serve
Line 1357: a purpose, but it’s easy to use in places where other types of tests are more relevant. 
Line 1358: If you need a variation of this, try using toMatchInlineSnapshot() instead. You can
Line 1359: find more info at https://jestjs.io/docs/en/snapshot-testing.
Line 1360: Using a regular expression 
Line 1361: instead of looking for the 
Line 1362: exact string
Line 1363: 
Line 1364: --- 페이지 85 ---
Line 1365: 57
Line 1366: Summary
Line 1367: // jest.config.integration.js
Line 1368: var config = require('./jest.config')
Line 1369: config.testRegex = "integration\\.js$" 
Line 1370: module.exports = config
Line 1371: // jest.config.unit.js
Line 1372: var config = require('./jest.config')
Line 1373: config.testRegex = "unit\\.js$" 
Line 1374: module.exports = config
Line 1375: Then, for each category, you can create a separate npm script that invokes the Jest
Line 1376: command line with a custom config file: jest -c my.custom.jest.config.js.
Line 1377: //Package.json
Line 1378: . . .
Line 1379: "scripts": {
Line 1380:     "unit": "jest -c jest.config.unit.js",
Line 1381:     "integ": "jest -c jest.config.integration.js"
Line 1382: . . .
Line 1383: In the next chapter, we’ll look at code that has dependencies and testability problems,
Line 1384: and we’ll start discussing the idea of fakes, spies, mocks, and stubs, and how you can
Line 1385: use them to write tests against such code.
Line 1386: Summary
Line 1387: Jest is a popular, open source test framework for JavaScript applications. It
Line 1388: simultaneously acts as a test library to use when writing tests, an assertion library
Line 1389: for asserting inside the tests, a test runner, and a test reporter.
Line 1390: Arrange-Act-Assert (AAA) is a popular pattern for structuring tests. It provides a
Line 1391: simple, uniform layout for all tests. Once you get used to it, you can easily read
Line 1392: and understand any test.
Line 1393: In the AAA pattern, the arrange section is where you bring the system under test
Line 1394: and its dependencies to a desired state. In the act section, you call methods,
Line 1395: pass the prepared dependencies, and capture the output value (if any). In the
Line 1396: assert section, you verify the outcome.
Line 1397: A good pattern for naming tests is to include in the name of the test the unit
Line 1398: of work under test, the scenario or inputs to the unit, and the expected behav-
Line 1399: ior or exit point. A handy mnemonic for this pattern is USE (unit, scenario,
Line 1400: expectation).
Line 1401: Jest provides several functions that help create more structure around multiple
Line 1402: related tests. describe() is a scoping function that allows for grouping multiple
Line 1403: tests (or groups of tests) together. A good metaphor for describe() is a folder
Line 1404: Listing 2.27
Line 1405: Creating separate jest.config.js files
Line 1406: Listing 2.28
Line 1407: Using separate npm scripts
Line 1408: 
Line 1409: --- 페이지 86 ---
Line 1410: 58
Line 1411: CHAPTER 2
Line 1412: A first unit test
Line 1413: containing tests or other folders. test() is a function denoting an individual
Line 1414: test. it() is an alias for test(), but it provides better readability when used in
Line 1415: combination with describe().
Line 1416: 
Line 1417: beforeEach() helps avoid duplication by extracting code that is common for
Line 1418: the nested describe and it functions.
Line 1419: The use of beforeEach() often leads to scroll fatigue, when you have to look at
Line 1420: various places to understand what a test does.
Line 1421: Factory methods with plain tests (without any beforeEach()) improve readability
Line 1422: and help avoid scroll fatigue.
Line 1423: Parameterized tests help reduce the amount of code needed for similar tests. The
Line 1424: drawback is that the tests become less readable as you make them more generic.
Line 1425: To maintain a balance between test readability and code reuse, only parameter-
Line 1426: ize input values. Create separate tests for different output values.
Line 1427: Jest doesn’t support test categories, but you can run groups of tests using the
Line 1428: --testPathPattern flag. You can also set up testRegex in the configuration file.
