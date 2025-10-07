Line 1: 
Line 2: --- 페이지 177 ---
Line 3: 149
Line 4: Trustworthy tests
Line 5: No matter how you organize your tests, or how many you have, they’re worth very
Line 6: little if you can’t trust them, maintain them, or read them. The tests that you write
Line 7: should have three properties that together make them good:
Line 8: Trustworthiness—Developers will want to run trustworthy tests, and they’ll
Line 9: accept the test results with confidence. Trustworthy tests don’t have bugs,
Line 10: and they test the right things. 
Line 11: Maintainability—Unmaintainable tests are nightmares because they can ruin
Line 12: project schedules, or they may be sidelined when the project is put on a
Line 13: more aggressive schedule. Developers will simply stop maintaining and fix-
Line 14: ing tests that take too long to change or that need to change often on very
Line 15: minor production code changes.
Line 16: Readability—This refers not only to being able to read a test but also figuring
Line 17: out the problem if the test seems to be wrong. Without readability, the other
Line 18: This chapter covers
Line 19: How to know you trust a test
Line 20: Detecting untrustworthy failing tests
Line 21: Detecting untrustworthy passing tests
Line 22: Dealing with flaky tests
Line 23: 
Line 24: --- 페이지 178 ---
Line 25: 150
Line 26: CHAPTER 7
Line 27: Trustworthy tests
Line 28: two pillars fall pretty quickly. Maintaining tests becomes harder, and you can’t
Line 29: trust them anymore because you don’t understand them.
Line 30: This chapter and the next two present a series of practices related to each of these pil-
Line 31: lars that you can use when doing test reviews. Together, the three pillars ensure your
Line 32: time is well used. Drop one of them, and you run the risk of wasting everyone’s time.
Line 33:  Trust is the first of the three pillars that I like to evaluate good unit tests on, so it’s
Line 34: fitting that we start with it. If we don’t trust the tests, what’s the point in running
Line 35: them? What’s the point in fixing them or fixing the code if they fail? What’s the point
Line 36: of maintaining them? 
Line 37: 7.1
Line 38: How to know you trust a test
Line 39: What does “trust” mean for a software developer in the context of a test? Perhaps it’s
Line 40: easier to explain based on what we do or don’t do when a test fails or passes. 
Line 41:  You might not trust a test if
Line 42: It fails and you’re not worried (you believe it’s a false positive).
Line 43: You feel like it’s fine to ignore the results of this test, either because it passes
Line 44: every once in a while or because you feel it’s not relevant or buggy. 
Line 45: It passes and you are worried (you believe it’s a false negative).
Line 46: You still feel the need to manually debug or test the software “just in case.”
Line 47: You might trust the test if
Line 48: The test fails and you’re genuinely worried that something broke. You don’t
Line 49: move on, assuming the test is wrong.
Line 50: The test passes and you feel relaxed, not feeling the need to test or debug
Line 51: manually.
Line 52: In the next few sections, we’ll look at test failures as a way to identify untrustworthy tests,
Line 53: and we’ll look at passing tests’ code and see how to detect untrustworthy test code.
Line 54: Finally, we’ll cover a few generic practices that can enhance trustworthiness in tests.
Line 55: 7.2
Line 56: Why tests fail
Line 57: Ideally, your tests (any tests, not just unit tests) should only be failing for a good reason.
Line 58: That good reason is, of course, that a real bug was uncovered in the underlying pro-
Line 59: duction code. 
Line 60:  Unfortunately, tests can fail for a multitude of reasons. We can assume that a test
Line 61: failing for any reason other than that one good reason should trigger an “untrust-
Line 62: worthy” warning, but not all tests fail the same way, and recognizing the reasons tests
Line 63: may fail can help us build a roadmap for what we’d like to do in each case.
Line 64:  Here are some reasons that tests fail:
Line 65: A real bug has been uncovered in the production code
Line 66: A buggy test gives a false failure
Line 67: The test is out of date due to a change in functionality
Line 68: 
Line 69: --- 페이지 179 ---
Line 70: 151
Line 71: 7.2
Line 72: Why tests fail
Line 73: The test conflicts with another test
Line 74: The test is flaky
Line 75: Except for the first point here, all these reasons are the test telling you it should not
Line 76: be trusted in its current form. Let’s go through them.
Line 77: 7.2.1
Line 78: A real bug has been uncovered in the production code
Line 79: The first reason a test will fail is when there is a bug in the production code. That’s
Line 80: good! That’s why we have tests. Let’s move on to the other reasons tests fail.
Line 81: 7.2.2
Line 82: A buggy test gives a false failure
Line 83: A test will fail if the test is buggy. The production code might be correct, but that
Line 84: doesn’t matter if the test itself has a bug that causes the test to fail. It could be that
Line 85: you’re asserting on the wrong expected result of an exit point, or that you’re using the
Line 86: system under test incorrectly. It could be that you’re setting up the context for the test
Line 87: wrong or that you misunderstand what you were supposed to test. 
Line 88:  Either way, a buggy test can be quite dangerous, because a bug in a test can also
Line 89: cause it to pass and leave you unsuspecting of what’s really going on. We’ll talk more
Line 90: about tests that don’t fail but should later in the chapter.
Line 91: HOW TO RECOGNIZE A BUGGY TEST
Line 92: You have a failing test, but you might have already debugged the production code and
Line 93: couldn’t find any bug there. This is when you should start suspecting the failing test.
Line 94: There’s no way around it. You’re going to have to slowly debug the test code. 
Line 95:  Here are some potential causes of false failures:
Line 96: Asserting on the wrong thing or on the wrong exit point
Line 97: Injecting a wrong value into the entry point
Line 98: Invoking the entry point incorrectly
Line 99: It could also be some other small mistake that happens when you write code at 2 A.M.
Line 100: (That’s not a sustainable coding strategy, by the way. Stop doing that.)
Line 101: WHAT DO YOU DO ONCE YOU’VE FOUND A BUGGY TEST?
Line 102: When you find a buggy test, don’t panic. This might be the millionth time you’ve
Line 103: found one, so you might be panicking and thinking “our tests suck.” You might also be
Line 104: right about that. But that doesn’t mean you should panic. Fix the bug, and run the
Line 105: test to see if it now passes.
Line 106:  If the test passes, don’t be happy too soon! Go to the production code and place an
Line 107: obvious bug that should be caught by the newly fixed test. For example, change a
Line 108: Boolean to always be true. Or false. Then run the test again, and make sure it fails. If
Line 109: it doesn’t, you might still have a bug in your test. Fix the test until it can find the pro-
Line 110: duction bug and you can see it fail.
Line 111:  Once you are sure the test is failing for an obvious production code issue, fix the
Line 112: production code issue you just made and run the test again. It should pass. If the test
Line 113: 
Line 114: --- 페이지 180 ---
Line 115: 152
Line 116: CHAPTER 7
Line 117: Trustworthy tests
Line 118: is now passing, you’re done. You’ve now seen the test passing when it should and fail-
Line 119: ing when it should. Commit the code and move on.
Line 120:  If the test is still failing, it might have another bug. Repeat the whole process again
Line 121: until you verify that the test fails and passes when it should. If the test is still failing, you
Line 122: might have come across a real bug in production code. In which case, good for you!
Line 123: HOW TO AVOID BUGGY TESTS IN THE FUTURE
Line 124: One of the best ways I know to detect and prevent buggy tests is to write your code in a
Line 125: test-driven manner. I explained a bit about this technique in chapter 1 of this book. I
Line 126: also practice this technique in real life.
Line 127:  Test-driven development (TDD) allows us to see both states of a test: both that it
Line 128: fails when it should (that’s the initial state we start in) and that it passes when it should
Line 129: (when the production code under test is written to make the test pass). If the test con-
Line 130: tinues to fail, we’ve found a bug in the production code. If the test starts out passing,
Line 131: we have a bug in the test. 
Line 132:  Another great way to reduce the likelihood of bugs in tests is to remove logic from
Line 133: them. More on this in section 7.3.
Line 134: 7.2.3
Line 135: The test is out of date due to a change in functionality
Line 136: A test can fail if it’s no longer compatible with the current feature that’s being tested.
Line 137: Say you have a login feature, and in an earlier version, you needed to provide a user-
Line 138: name and a password to log in. In the new version, a two-factor authentication scheme
Line 139: replaced the old login. The existing test will start failing because it’s not providing the
Line 140: right parameters to the login functions.
Line 141: WHAT CAN YOU DO NOW?
Line 142: You now have two options:
Line 143: Adapt the test to the new functionality.
Line 144: Write a new test for the new functionality, and remove the old test because it has
Line 145: now become irrelevant.
Line 146: AVOIDING OR PREVENTING THIS IN THE FUTURE
Line 147: Things change. I don’t think it’s possible to not have out-of-date tests at some point in
Line 148: time. We’ll deal with change in the next chapter, relating to the maintainability of
Line 149: tests and how well tests can handle changes in the application. 
Line 150: 7.2.4
Line 151: The test conflicts with another test
Line 152: Let’s say you have two tests: one of them is failing and one is passing. Let’s also say they
Line 153: cannot pass together. You’ll usually only see the failing test, because the passing one is,
Line 154: well, passing.
Line 155:  For instance, a test may fail because it suddenly conflicts with a new behavior. On
Line 156: the other hand, a conflicting test may expect a new behavior but doesn’t find it. The
Line 157: simplest example is when the first test verifies that calling a function with two parame-
Line 158: ters produces “3,” whereas the second test expects the same function to produce “4.”
Line 159: 
Line 160: --- 페이지 181 ---
Line 161: 153
Line 162: 7.3
Line 163: Avoiding logic in unit tests
Line 164: WHAT CAN YOU DO NOW?
Line 165: The root cause is that one of the tests has become irrelevant, which means it needs to
Line 166: be removed. Which one should be removed? That’s a question we’d need to ask a
Line 167: product owner, because the answer is related to which behavior is correct and
Line 168: expected from the application. 
Line 169: AVOIDING THIS IN THE FUTURE
Line 170: I feel this is a healthy dynamic, and I’m fine with not avoiding it. 
Line 171: 7.2.5
Line 172: The test is flaky
Line 173: A test can fail inconsistently. Even if the production code under test hasn’t changed, a
Line 174: test can suddenly fail without any apparent reason, then pass again, then fail again.
Line 175: We call a test like that “flaky.” 
Line 176:  Flaky tests are a special beast, and I’ll deal with them in section 7.5.
Line 177: 7.3
Line 178: Avoiding logic in unit tests
Line 179: The chances of having bugs in your tests increase almost exponentially as you include
Line 180: more and more logic in them. I’ve seen plenty of tests that should have been simple
Line 181: become dynamic, random-number-generating, thread-creating, file-writing monsters
Line 182: that are little test engines in their own right. Sadly, because they were “tests,” the
Line 183: writer didn’t consider that they might have bugs or didn’t write them in a maintain-
Line 184: able manner. Those test monsters take more time to debug and verify than they save. 
Line 185:  But all monsters start out small. Often, an experienced developer in the company
Line 186: will look at a test and start thinking, “What if we made the function loop and create
Line 187: random numbers as input? We’d surely find lots more bugs that way!” And you will,
Line 188: especially in your tests. 
Line 189:  Test bugs are one of the most annoying things for developers, because you’ll
Line 190: almost never search for the cause of a failing test in the test itself. I’m not saying that
Line 191: tests with logic don’t have any value. In fact, I’m likely to write such tests myself in
Line 192: some special situations. But I try to avoid this practice as much as possible. 
Line 193:  If you have any of the following inside a unit test, your test contains logic that I usu-
Line 194: ally recommend be reduced or removed completely:
Line 195: 
Line 196: switch, if, or else statements
Line 197: 
Line 198: foreach, for, or while loops
Line 199: Concatenations (+ sign, etc.)
Line 200: 
Line 201: try, catch
Line 202: 7.3.1
Line 203: Logic in asserts: Creating dynamic expected values
Line 204: Here’s a quick example of a concatenation to start us off.
Line 205: describe("makeGreeting", () => {
Line 206:   it("returns correct greeting for name", () => {
Line 207: Listing 7.1
Line 208: A test with logic in it
Line 209: 
Line 210: --- 페이지 182 ---
Line 211: 154
Line 212: CHAPTER 7
Line 213: Trustworthy tests
Line 214:     const name = "abc";
Line 215:     const result = trust.makeGreeting(name);
Line 216:     expect(result).toBe("hello" + name);    
Line 217:   });
Line 218: To understand the problem with this test, the following listing shows the code being
Line 219: tested. Notice that the + sign makes an appearance in both. 
Line 220: const makeGreeting = (name) => {
Line 221:   return "hello" + name;      
Line 222: };
Line 223: Notice how the algorithm (very simple, but still an algorithm) of connecting a name
Line 224: with a "hello" string is repeated in both the test and the code under test:
Line 225: expect(result).toBe("hello" + name);   
Line 226: return "hello" + name;   
Line 227: My issue with this test is that the algorithm under test is repeated in the test itself. This
Line 228: means that if there is a bug in the algorithm, the test also contains the same bug. The
Line 229: test will not catch the bug, but instead will expect the incorrect result from the code
Line 230: under test. 
Line 231:  In this case, the incorrect result is that we’re missing a space character between the
Line 232: concatenated words, but hopefully you can see how the same issue could become
Line 233: much more complex with a more complex algorithm.
Line 234:  This is a trust issue. We can’t trust this test to tell us the truth, since its logic is a
Line 235: repeat of the logic being tested. The test might pass when the bug exists in the code,
Line 236: so we can’t trust the test’s result.
Line 237: WARNING
Line 238: Avoid dynamically creating the expected value in your asserts; use
Line 239: hardcoded values when possible. 
Line 240: A more trustworthy version of this test can be rewritten as follows.
Line 241: it("returns correct greeting for name 2", () => {
Line 242:   const result = trust.makeGreeting("abc");
Line 243:   expect(result).toBe("hello abc");    
Line 244: });
Line 245: Because the inputs in this test are so simple, it’s easy to write a hardcoded expected
Line 246: value. This is what I usually recommend—make the test inputs so simple that it is triv-
Line 247: ial to create a hardcoded version of the expected value. Note that this is mostly true of
Line 248: unit tests. For higher-level tests, this is a bit harder to do, which is another reason why
Line 249: Listing 7.2
Line 250: Code under test
Line 251: Listing 7.3
Line 252: A more trustworthy test
Line 253: Logic in the 
Line 254: assertion part
Line 255: The same logic as in 
Line 256: the production code
Line 257: Our test
Line 258: The code under test
Line 259: Using a hardcoded value
Line 260: 
Line 261: --- 페이지 183 ---
Line 262: 155
Line 263: 7.3
Line 264: Avoiding logic in unit tests
Line 265: higher-level tests should be considered a bit riskier; they often create expected results
Line 266: dynamically, which you should try to avoid any time you can.
Line 267:  “But Roy,” you might say, “Now we are repeating ourselves—the string "abc" is
Line 268: repeated twice. We were able to avoid this in the previous test.” When push comes to
Line 269: shove, trust should trump maintainability. What good is a highly maintainable test that
Line 270: I cannot trust? You can read more about code duplication in tests in Vladimir
Line 271: Khorikov’s article, “DRY vs. DAMP in Unit Tests,” (https://enterprisecraftsmanship
Line 272: .com/posts/dry-damp-unit-tests/).
Line 273: 7.3.2
Line 274: Other forms of logic
Line 275: Here’s the opposite case: creating the inputs dynamically (using a loop) forces us to
Line 276: dynamically decide what the expected output should be. Suppose we have the follow-
Line 277: ing code to test.
Line 278: const isName = (input) => {
Line 279:   return input.split(" ").length === 2;
Line 280: };
Line 281: The following listing shows a clear antipattern for a test.
Line 282: describe("isName", () => {
Line 283:   const namesToTest = ["firstOnly", "first second", ""];   
Line 284:   it("correctly finds out if it is a name", () => {
Line 285:     namesToTest.forEach((name) => {
Line 286:       const result = trust.isName(name);
Line 287:       if (name.includes(" ")) {       
Line 288:         expect(result).toBe(true);    
Line 289:       } else {                        
Line 290:         expect(result).toBe(false);   
Line 291:       }
Line 292:     });
Line 293:   });
Line 294: });
Line 295: Notice how we’re using multiple inputs for the test. This forces us to loop over those
Line 296: inputs, which in itself complicates the test. Remember, loops can have bugs too. 
Line 297:  Additionally, because we have different scenarios for the values (with and without
Line 298: spaces) we need an if/else to know what the assertion is expecting, and the if/else
Line 299: can have bugs too. We are also repeating a part of the production algorithm, which
Line 300: brings us back to the previous concatenation example and its problems.
Line 301:  Finally, our test name is too generic. We can only title it as “it works” because we have
Line 302: to account for multiple scenarios and expected outcomes. That’s bad for readability.
Line 303: Listing 7.4
Line 304: A name-finding function
Line 305: Listing 7.5
Line 306: Loops and ifs in a test
Line 307: Declaring 
Line 308: multiple inputs
Line 309: Production code 
Line 310: logic leaking into 
Line 311: the test
Line 312: 
Line 313: --- 페이지 184 ---
Line 314: 156
Line 315: CHAPTER 7
Line 316: Trustworthy tests
Line 317:  This is an all-around bad test. It’s better to separate this into two or three tests,
Line 318: each with its own scenario and name. This would allow us to use hardcoded inputs
Line 319: and assertions and to remove any loops and if/else logic from the code. Anything
Line 320: more complex causes the following problems:
Line 321: The test is harder to read and understand.
Line 322: The test is hard to recreate. For example, imagine a multithreaded test or a test
Line 323: with random numbers that suddenly fails.
Line 324: The test is more likely to have a bug or to verify the wrong thing.
Line 325: Naming the test may be harder because it does multiple things.
Line 326: Generally, monster tests replace original simpler tests, and that makes it harder to find
Line 327: bugs in the production code. If you must create a monster test, it should be added as a
Line 328: new test and not be a replacement for existing tests. Also, it should reside in a project
Line 329: or folder explicitly titled to hold tests other than unit tests. I call these “integration
Line 330: tests” or “complex tests” and try to keep their number to an acceptable minimum.
Line 331: 7.3.3
Line 332: Even more logic
Line 333: Logic can be found not only in tests but also in test helper methods, handwritten
Line 334: fakes, and test utility classes. Remember, every piece of logic you add in these places
Line 335: makes the code that much harder to read and increases the chances of a bug in a util-
Line 336: ity method that your tests use. 
Line 337:  If you find that you need to have complicated logic in your test suite for some rea-
Line 338: son (though that’s generally something I do with integration tests, not unit tests), at
Line 339: least make sure you have a couple of tests against the logic of your utility methods in
Line 340: the test project. This will save you many tears down the road.
Line 341: 7.4
Line 342: Smelling a false sense of trust in passing tests
Line 343: We’ve now covered failed tests as a means of detecting tests we shouldn’t trust. What
Line 344: about all those quiet, green tests we have lying all over the place? Should we trust
Line 345: them? What about a test that we need to do a code review for, before it’s pushed into a
Line 346: main branch? What should we look for?
Line 347:  Let’s use the term “false-trust” to describe trusting a test that you really shouldn’t,
Line 348: but you don’t know it yet. Being able to review tests and find possible false-trust issues
Line 349: has immense value because, not only can you fix those tests yourself, you’re affecting
Line 350: the trust of everyone else who’s ever going to read or run those tests. Here are some
Line 351: reasons I reduce my trust in tests, even if they are passing:
Line 352: The test contains no asserts.
Line 353: I can’t understand the test.
Line 354: Unit tests are mixed with flaky integration tests.
Line 355: The test verifies multiple concerns or exit points.
Line 356: The test keeps changing.
Line 357: 
Line 358: --- 페이지 185 ---
Line 359: 157
Line 360: 7.4
Line 361: Smelling a false sense of trust in passing tests
Line 362: 7.4.1
Line 363: Tests that don’t assert anything
Line 364: We all agree that a test that doesn’t actually verify that something is true or false is less
Line 365: than helpful, right? Less than helpful because it also costs in maintenance time, refac-
Line 366: toring, and reading time, and sometimes unnecessary noise if it needs changing due
Line 367: to API changes in production code. 
Line 368:  If you see a test with no asserts, consider that there may be hidden asserts in a func-
Line 369: tion call. This causes a readability problem if the function is not named to explain
Line 370: this. Sometimes people also write a test that exercises a piece of code simply to make
Line 371: sure that the code does not throw an exception. This does have some value, and if
Line 372: that’s the test you choose to write, make sure that the name of the test indicates this
Line 373: with a term such as “does not throw.” To be even more specific, many test APIs support
Line 374: the ability to specify that something does not throw an exception. This is how you can
Line 375: do this in Jest:
Line 376: expect(() => someFunction()).not.toThrow(error)
Line 377: If you do have such tests, make sure there’s a very small number of them. I don’t rec-
Line 378: ommend it as a standard, but only for really special cases.
Line 379:  Sometimes people simply forget to write an assert due to lack of experience. Con-
Line 380: sider adding the missing assert or removing the test if it brings no value. People may
Line 381: also actively write tests to achieve some imagined test coverage goal set by manage-
Line 382: ment. Those tests usually serve no real value except to get management off people’s
Line 383: backs so they can do real work.
Line 384: TIP
Line 385: Code coverage shouldn’t ever be a goal on its own. It doesn’t mean
Line 386: “code quality.” In fact, it often causes developers to write meaningless tests
Line 387: that will cost even more time to maintain. Instead, measure “escaped bugs,”
Line 388: “time to fix,” and other metrics that we’ll discuss in chapter 11.
Line 389: 7.4.2
Line 390: Not understanding the tests
Line 391: This is a huge issue, and I’ll deal with it in depth in chapter 9. There are several possi-
Line 392: ble issues:
Line 393: Tests with bad names
Line 394: Tests that are too long or have convoluted code
Line 395: Tests containing confusing variable names
Line 396: Tests containing hidden logic or assumptions that cannot be understood easily
Line 397: Test results that are inconclusive (neither failed nor passed)
Line 398: Test messages that don’t provide enough information
Line 399: If you don’t understand the test that’s failing or passing, you don’t know if you should
Line 400: be worried or not.
Line 401: 
Line 402: --- 페이지 186 ---
Line 403: 158
Line 404: CHAPTER 7
Line 405: Trustworthy tests
Line 406: 7.4.3
Line 407: Mixing unit tests and flaky integration tests
Line 408: They say that one rotten apple spoils the bunch. The same is true for flaky tests
Line 409: mixed in with nonflaky tests. Integration tests are much more likely to be flaky than
Line 410: unit tests because they have more dependencies. If you find that you have a mix of
Line 411: integration and unit tests in the same folder or test execution command, you should
Line 412: be suspicious.
Line 413:  Humans like to take the path of least resistance, and it’s no different when it comes
Line 414: to coding. Suppose that a developer runs all the tests and one of them fails—if there’s
Line 415: a way to blame a missing configuration or a network issue instead of spending time
Line 416: investigating and fixing a real problem, they will. That’s especially true if they’re under
Line 417: serious time pressure or they’re overcommitted to delivering things they’re already
Line 418: late on.
Line 419:  The easiest thing is to accuse any failing test of being a flaky test. Because flaky and
Line 420: nonflaky tests are mixed up with each other, that’s a simple thing to do, and it’s a good
Line 421: way to ignore the issue and work on something more fun. Because of this human fac-
Line 422: tor, it’s best to remove the option to blame a test for being flaky. What should you do
Line 423: to prevent this? Aim to have a safe green zone by keeping your integration and unit tests
Line 424: in separate places.
Line 425:  A safe green test area should contain only nonflaky, fast tests, where developers
Line 426: know that they can get the latest code version, they can run all the tests in that name-
Line 427: space or folder, and the tests should all be green (given no changes to production
Line 428: code). If some tests in the safe green zone don’t pass, a developer is much more likely
Line 429: to be concerned.
Line 430:  An added benefit to this separation is that developers are more likely to run the
Line 431: unit tests more often, now that the run time is faster without the integration tests. It’s
Line 432: better to have some feedback than no feedback, right? The automated build pipeline
Line 433: should take care of running any of the “missing” feedback tests that developers can’t
Line 434: or won’t run on their local machines.
Line 435: 7.4.4
Line 436: Testing multiple exit points
Line 437: An exit point (I’ll also refer to it as a concern) is explained in chapter 1. It’s a single end
Line 438: result from a unit of work: a return value, a change to system state, or a call to a third-
Line 439: party object.
Line 440:  Here’s a simple example of a function that has two exit points, or two concerns. It
Line 441: both returns a value and triggers a passed-in callback function:
Line 442: const trigger = (x, y, callback) => {
Line 443:   callback("I'm triggered");
Line 444:   return x + y;
Line 445: };
Line 446: We could write a test that checks both of these exit points at the same time.
Line 447:  
Line 448: 
Line 449: --- 페이지 187 ---
Line 450: 159
Line 451: 7.4
Line 452: Smelling a false sense of trust in passing tests
Line 453: describe("trigger", () => {
Line 454:   it("works", () => {
Line 455:     const callback = jest.fn();
Line 456:     const result = trigger(1, 2, callback);
Line 457:     expect(result).toBe(3);
Line 458:     expect(callback).toHaveBeenCalledWith("I'm triggered");
Line 459:   });
Line 460: });
Line 461: The first reason testing more than one concern in a test can backfire is that your test
Line 462: name suffers. I’ll discuss readability in chapter 9, but here’s a quick note on naming:
Line 463: naming tests is hugely important for both debugging and documentation purposes. I
Line 464: spend a lot of time thinking about good names for tests, and I’m not ashamed to admit it. 
Line 465:  Naming a test may seem like a simple task, but if you’re testing more than one
Line 466: thing, giving the test a good name that indicates what’s being tested is difficult. Often
Line 467: you end up with a very generic test name that forces the reader to read the test code.
Line 468: When you test just one concern, naming the test is easy. But wait, there’s more. 
Line 469:  More disturbingly, in most unit test frameworks, a failed assert throws a special type
Line 470: of exception that’s caught by the test framework runner. When the test framework
Line 471: catches that exception, it means the test has failed. Most exceptions in most lan-
Line 472: guages, by design, don’t let the code continue. So if this line,
Line 473: expect(result).toBe(3);
Line 474: fails the assert, this line will not execute at all:
Line 475: expect(callback).toHaveBeenCalledWith("I'm triggered");
Line 476: The test method exits on the same line where the exception is thrown. Each of these
Line 477: asserts can and should be considered different requirements, and they can also, and in
Line 478: this case likely should, be implemented separately and incrementally, one after the other.
Line 479:  Consider assert failures as symptoms of a disease. The more symptoms you can
Line 480: find, the easier the disease will be to diagnose. After a failure, subsequent asserts
Line 481: aren’t executed, and you’ll miss seeing other possible symptoms that could provide
Line 482: valuable data (symptoms) that would help you narrow your focus and discover the
Line 483: underlying problem. Checking multiple concerns in a single unit test adds complexity
Line 484: with little value. You should run additional concern checks in separate, self-contained
Line 485: unit tests so that you can see what really fails.
Line 486:  Let’s break it up into two separate tests.
Line 487: describe("trigger", () => {
Line 488:   it("triggers a given callback", () => {
Line 489:     const callback = jest.fn();
Line 490: Listing 7.6
Line 491: Checking two exit points in the same test
Line 492: Listing 7.7
Line 493: Checking the two exit points in separate tests
Line 494: 
Line 495: --- 페이지 188 ---
Line 496: 160
Line 497: CHAPTER 7
Line 498: Trustworthy tests
Line 499:     trigger(1, 2, callback);
Line 500:     expect(callback).toHaveBeenCalledWith("I'm triggered");
Line 501:   });
Line 502:   it("sums up given values", () => {
Line 503:     const result = trigger(1, 2, jest.fn());
Line 504:     expect(result).toBe(3);
Line 505:   });
Line 506: });
Line 507: Now we can clearly separate the concerns, and each one can fail separately.
Line 508:  Sometimes it’s perfectly okay to assert multiple things in the same test, as long as
Line 509: they are not multiple concerns. Take the following function and its associated test as an
Line 510: example. makePerson is designed to build a new person object with some properties. 
Line 511: const makePerson = (x, y) => {
Line 512:   return {
Line 513:     name: x,
Line 514:     age: y,
Line 515:     type: "person",
Line 516:   };
Line 517: };
Line 518: describe("makePerson", () => {
Line 519:   it("creates person given passed in values", () => {
Line 520:     const result = makePerson("name", 1);
Line 521:     expect(result.name).toBe("name");
Line 522:     expect(result.age).toBe(1);
Line 523:   });
Line 524: });
Line 525: In our test, we are asserting on both name and age together, because they are part of
Line 526: the same concern (building the person object). If the first assert fails, we likely don’t
Line 527: care about the second assert because something might have gone terribly wrong while
Line 528: building the object in the first place.
Line 529: TIP
Line 530: Here’s a test break-up hint: If the first assert fails, do you still care what
Line 531: the result of the next assert is? If you do, you should probably separate the test
Line 532: into two tests.
Line 533: 7.4.5
Line 534: Tests that keep changing
Line 535: If a test is using the current date and time as part of its execution or assertions, then we
Line 536: can claim that every time the test runs, it’s a different test. The same can be said of tests
Line 537: that use random numbers, machine names, or anything that depends on grabbing a
Line 538: current value from outside the test’s environment. There’s a big chance its results won’t
Line 539: be consistent, and that means they can be flaky. For us, as developers, flaky tests reduce
Line 540: our trust in the failed results of the test (as I’ll discuss in the next section). 
Line 541: Listing 7.8
Line 542: Using multiple asserts to verify a single exit point
Line 543: 
Line 544: --- 페이지 189 ---
Line 545: 161
Line 546: 7.5
Line 547: Dealing with flaky tests
Line 548:  Another huge potential issue with dynamically generated values is that if we don’t
Line 549: know ahead of time what the input into the system might be, we also have to compute
Line 550: the expected output of the system, and that can lead to a buggy test that depends on
Line 551: repeating production logic, as mentioned in section 7.3. 
Line 552: 7.5
Line 553: Dealing with flaky tests
Line 554: I’m not sure who came up with the term flaky tests, but it does fit the bill. It’s used to
Line 555: describe tests that, given no changes to the code, return inconsistent results. This
Line 556: might happen frequently or very rarely, but it does happen. 
Line 557:  Figure 7.1 illustrates where flakiness comes from. The figure is based on the num-
Line 558: ber of real dependencies the tests have. Another way to think about this is how many
Line 559: moving parts the tests have. For this book, we’re mostly concerning ourselves with the
Line 560: Flakiness caused by
Line 561: • Shared memory resources
Line 562: • Threads
Line 563: • Random values
Line 564: • Dynamically generated inputs/outputs
Line 565: • Time
Line 566: • Logic bugs
Line 567: Flakiness also caused by
Line 568: • Shared resources
Line 569: • Network issues
Line 570: • Conﬁguration issues
Line 571: • Permission issues
Line 572: • Load issues
Line 573: • Security issues
Line 574: • Other systems are down
Line 575: • And more...
Line 576: Conﬁdence/Flakiness
Line 577: E2E/UI system tests
Line 578: E2E/UI isolated tests
Line 579: API tests (out of process)
Line 580: Integration tests (in memory)
Line 581: Component tests (in memory)
Line 582: Unit tests (in memory)
Line 583: Figure 7.1
Line 584: The higher the level of the tests, the more real dependencies they use, which 
Line 585: gives us confidence in the overall system correctness but results in more flakiness.
Line 586: 
Line 587: --- 페이지 190 ---
Line 588: 162
Line 589: CHAPTER 7
Line 590: Trustworthy tests
Line 591: bottom third of this diagram: unit and component tests. However, I want to touch on
Line 592: the higher-level flakiness so I can give you some pointers on what to research.
Line 593:  At the lowest level, our tests have full control over all of their dependencies and
Line 594: therefore have no moving parts, either because they’re faking them or because they
Line 595: run purely in memory and can be configured. We did this in chapters 3 and 4. Execu-
Line 596: tion paths in the code are fully deterministic because all the initial states and expected
Line 597: return values from various dependencies have been predetermined. The code path is
Line 598: almost static—if it returns the wrong expected result, then something important
Line 599: might have changed in the production code’s execution path or logic. 
Line 600:  As we go up the levels, our tests shed more and more stubs and mocks and start
Line 601: using more and more real dependencies, such as databases, networks, configura-
Line 602: tion, and more. This, in turn, means more moving parts that we have less control
Line 603: over and that might change our execution path, return unexpected values, or fail to
Line 604: execute at all. 
Line 605:  At the highest level, there are no fake dependencies. Everything our tests rely on
Line 606: is real, including any third-party services, security and network layers, and configura-
Line 607: tion. These types of tests usually require us to set up an environment that is as close
Line 608: to a production scenario as possible, if they’re not running right on the production
Line 609: environments.
Line 610:  The higher up we go in the test diagram, we should get higher confidence that our
Line 611: code works, unless we don’t trust the tests’ results. Unfortunately, the higher up we go
Line 612: in the diagram, the more chances there are for our tests to become flaky because of
Line 613: how many moving parts are involved.
Line 614:  We might assume that tests at the lowest level shouldn’t have any flakiness issues
Line 615: because there shouldn’t be any moving parts that cause flakiness. That’s theoretically
Line 616: true, but in reality people still manage to add moving parts in lower-level tests: using
Line 617: the current date and time, the machine name, the network, the filesystem, and more
Line 618: can cause a test to be flaky.
Line 619:  A test fails sometimes without us touching production code. For example:
Line 620: A test fails every third run.
Line 621: A test fails once every unknown number of times.
Line 622: A test fails when various external conditions fail, such as network or database
Line 623: availability, other APIs not being available, environment configuration, and more.
Line 624: To add to that salad of pain, each dependency the test uses (network, filesystem,
Line 625: threads, etc.) usually adds time to the test run. Calls to the network and the database
Line 626: take time. The same goes for waiting for threads to finish, reading configurations, and
Line 627: waiting for asynchronous tasks.
Line 628:  It also takes longer to figure out why a test is failing. Debugging a test or reading
Line 629: through huge amounts of logs is heartbreakingly time consuming and will drain your
Line 630: soul slowly into the abyss of “time to update my resume” land.
Line 631: 
Line 632: --- 페이지 191 ---
Line 633: 163
Line 634: 7.5
Line 635: Dealing with flaky tests
Line 636: 7.5.1
Line 637: What can you do once you’ve found a flaky test?
Line 638: It’s important to realize that flaky tests can be costly to an organization. You should
Line 639: aim to have zero flaky tests as a long-term goal. Here are some ways to reduce the costs
Line 640: associated with handling flaky tests:
Line 641: Define—Agree on what “flaky” means to your organization. For example, run
Line 642: your test suite 10 times without any production code changes, and count all the
Line 643: tests that were not consistent in their results (i.e., ones that did not fail all 10
Line 644: times or did not pass all 10 times).
Line 645: Place any test deemed flaky in a special category or folder of tests that can be
Line 646: run separately. I recommend removing all flaky tests from the regular delivery
Line 647: build so they do not create noise, and quarantining them in their own little
Line 648: pipeline temporarily. Then, go over each of the flaky tests and play my favorite
Line 649: flaky game, “fix, convert, or kill”:
Line 650: – Fix—Make the test not flaky by controlling its dependencies, if possible. For
Line 651: example, if it requires data in the database, insert the data into the database
Line 652: as part of the test. 
Line 653: – Convert—Remove flakiness by converting the test into a lower-level test by
Line 654: removing and controlling one or more of its dependencies. For example,
Line 655: simulate a network endpoint with a stub instead of using a real one. 
Line 656: – Kill—Seriously consider whether the value the test brings is enough to con-
Line 657: tinue to run it and pay the maintenance costs it creates. Sometimes old flaky
Line 658: tests are better off dead and buried. Sometimes they are already covered by
Line 659: newer, better tests, and the old tests are pure technical debt that we can get
Line 660: rid of. Sadly, many engineering managers are reluctant to remove these old
Line 661: tests because of the sunken cost fallacy—there was so much effort put into
Line 662: them that it would be a waste to delete them. However, at this point, it might
Line 663: cost you more to keep the test than to delete it, so I recommend seriously
Line 664: considering this option for many of your flaky tests. 
Line 665: 7.5.2
Line 666: Preventing flakiness in higher-level tests
Line 667: If you’re interested in preventing flakiness in higher-level tests, your best bet is to
Line 668: make sure that your tests are repeatable on any environment after any deployment.
Line 669: That could involve the following:
Line 670: Roll back any changes your tests have made to external shared resources.
Line 671: Do not depend on other tests changing external state.
Line 672: Gain some control over external systems and dependencies by ensuring you
Line 673: have the ability to recreate them at will (do an internet search on “infrastruc-
Line 674: ture as code”), creating dummies of them that you can control, or creating spe-
Line 675: cial test accounts on them and pray that they stay safe.
Line 676: 
Line 677: --- 페이지 192 ---
Line 678: 164
Line 679: CHAPTER 7
Line 680: Trustworthy tests
Line 681: On this last point, controlling external dependencies can be difficult or impossible
Line 682: when using external systems managed by other companies. When that’s true, it’s
Line 683: worth considering these options:
Line 684: Remove some of the higher-level tests if some low-level tests already cover those
Line 685: scenarios.
Line 686: Convert some of the higher-level tests to a set of lower-level tests.
Line 687: If you’re writing new tests, consider a pipeline-friendly testing strategy with test
Line 688: recipes (such as the one I’ll explain in chapter 10).
Line 689: Summary
Line 690: If you don’t trust a test when it’s failing, you might ignore a real bug, and if you
Line 691: don’t trust a test when it’s passing, you’ll end up doing lots of manual debug-
Line 692: ging and testing. Both of these outcomes are supposed to be reduced by having
Line 693: good tests, but if we don’t reduce them, and we spend all this time writing tests
Line 694: that we don’t trust, what’s the point in writing them in the first place? 
Line 695: Tests might fail for multiple reasons: a real bug found in production code, a bug
Line 696: in the test resulting in a false failure, a test being out of date due to a change in
Line 697: functionality, a test conflicting with another test, or test flakiness. Only the first
Line 698: reason is a valid one. All the others tell us the test shouldn’t be trusted.
Line 699: Avoid complexity in tests, such as creating dynamic expected values or duplicat-
Line 700: ing logic from the underlying production code. Such complexity increases the
Line 701: chances of introducing bugs in tests and the time it takes to understand them.
Line 702: If a test doesn’t have any asserts, you can’t understand what's it’s doing, it runs
Line 703: alongside flaky tests (even if this test itself isn’t flaky), it verifies multiple exit
Line 704: points, or it keeps changing, it can’t be fully trusted.
Line 705: Flaky tests are tests that fail unpredictably. The higher the level of the test, the
Line 706: more real dependencies it uses, which gives us confidence in the overall sys-
Line 707: tem’s correctness but results in more flakiness. To better identify flaky tests, put
Line 708: them in a special category or folder that can be run separately.
Line 709: To reduce test flakiness, either fix the tests, convert flaky higher-level tests into
Line 710: less flaky lower-level ones, or delete them.
