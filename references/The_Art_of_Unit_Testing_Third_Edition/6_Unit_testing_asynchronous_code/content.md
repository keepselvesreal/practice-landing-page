Line 1: 
Line 2: --- 페이지 149 ---
Line 3: 121
Line 4: Unit testing
Line 5: asynchronous code
Line 6: When we’re dealing with regular synchronous code, waiting for actions to finish is
Line 7: implicit. We don’t worry about it, and we don’t really think about it too much. When
Line 8: dealing with asynchronous code, however, waiting for actions to finish becomes an
Line 9: explicit activity that is under our control. Asynchronicity makes code, and the tests
Line 10: for that code, potentially trickier because we have to be explicit about waiting for
Line 11: actions to complete.
Line 12:  Let’s start with a simple fetching example to illustrate the issue.
Line 13:  
Line 14:  
Line 15: This chapter covers
Line 16: Async, done(), and awaits
Line 17: Integration and unit test levels for async
Line 18: The Extract Entry Point pattern
Line 19: The Extract Adapter pattern
Line 20: Stubbing, advancing, and resetting timers
Line 21: 
Line 22: --- 페이지 150 ---
Line 23: 122
Line 24: CHAPTER 6
Line 25: Unit testing asynchronous code
Line 26: 6.1
Line 27: Dealing with async data fetching
Line 28: Let’s say we have a module that checks whether our website at example.com is alive. It
Line 29: does this by fetching the context from the main URL and checking for a specific
Line 30: word, “illustrative,” to determine if the website is up. We’ll look at two different and
Line 31: very simple implementations of this functionality. The first uses a callback mecha-
Line 32: nism, and the second uses an async/await mechanism.
Line 33:  Figure 6.1 illustrates their entry and exit points for our purposes. Note that the
Line 34: callback arrow is pointed differently, to make it more obvious that it’s a different type
Line 35: of exit point.
Line 36: The initial code is shown in the following listing. We’re using node-fetch to get the
Line 37: URL’s content.
Line 38: //Callback version
Line 39: const fetch = require("node-fetch");
Line 40: const isWebsiteAliveWithCallback = (callback) => {
Line 41:   const website = "http://example.com";
Line 42:   fetch(website)
Line 43:     .then((response) => {
Line 44:       if (!response.ok) {
Line 45:         //how can we simulate this network issue?
Line 46:         throw Error(response.statusText);      
Line 47:       }
Line 48:       return response;
Line 49:     })
Line 50:     .then((response) => response.text())
Line 51:     .then((text) => {
Line 52:       if (text.includes("illustrative")) {
Line 53:         callback({ success: true, status: "ok" });
Line 54:       } else {
Line 55:         //how can we test this path?
Line 56: Listing 6.1
Line 57: IsWebsiteAlive() callback and await versions
Line 58: Callback version
Line 59: Async/await version
Line 60: Website
Line 61: checkup
Line 62: isWebsiteAlive()
Line 63: Return
Line 64: value/error
Line 65: isWebsiteAlive(callback)
Line 66: Callback
Line 67: Website
Line 68: checkup
Line 69: Figure 6.1
Line 70: IsWebsiteAlive() callback vs. the async/await version
Line 71: Throwing a custom 
Line 72: error to handle 
Line 73: problems in our code
Line 74: 
Line 75: --- 페이지 151 ---
Line 76: 123
Line 77: 6.1
Line 78: Dealing with async data fetching
Line 79:         callback({ success: false, status: "text missing" });
Line 80:       }
Line 81:     })
Line 82:     .catch((err) => {
Line 83:       //how can we test this exit point?
Line 84:       callback({ success: false, status: err });
Line 85:     });
Line 86: };
Line 87: // Await version
Line 88: const isWebsiteAliveWithAsyncAwait = async () => {
Line 89:   try {
Line 90:     const resp = await fetch("http://example.com");
Line 91:     if (!resp.ok) {
Line 92:       //how can we simulate a non ok response?
Line 93:       throw resp.statusText;                     
Line 94:     }
Line 95:     const text = await resp.text();
Line 96:     const included = text.includes("illustrative");
Line 97:     if (included) {
Line 98:       return { success: true, status: "ok" };
Line 99:     }
Line 100:     // how can we simulate different website content?
Line 101:     throw "text missing";
Line 102:   } catch (err) {
Line 103:     return { success: false, status: err };  
Line 104:   }
Line 105: };
Line 106: NOTE
Line 107: In the preceding code, I’m assuming you know how promises work in
Line 108: JavaScript. If you need more information, I recommend reading the Mozilla
Line 109: documentation on promises at http://mng.bz/W11a.
Line 110: In this example, we are converting any errors from connectivity failures or missing
Line 111: text on the web page to either a callback or a return value to denote a failure to the
Line 112: user of our function. 
Line 113: 6.1.1
Line 114: An initial attempt with an integration test
Line 115: Since everything is hardcoded in listing 6.1, how would you test this? Your initial reac-
Line 116: tion might involve writing an integration test. The following listing shows how we
Line 117: could write an integration test for the callback version.
Line 118: test("NETWORK REQUIRED (callback): correct content, true", (done) => {
Line 119:   samples.isWebsiteAliveWithCallback((result) => {
Line 120:     expect(result.success).toBe(true);
Line 121:     expect(result.status).toBe("ok");
Line 122:     done();
Line 123:   });
Line 124: });
Line 125: Listing 6.2
Line 126: An initial integration test
Line 127: Throwing a custom 
Line 128: error to handle 
Line 129: problems in our code
Line 130: Wrapping the error 
Line 131: into a response
Line 132: 
Line 133: --- 페이지 152 ---
Line 134: 124
Line 135: CHAPTER 6
Line 136: Unit testing asynchronous code
Line 137: To test a function whose exit point is a callback function, we pass it our own callback
Line 138: function in which we can
Line 139: Check the correctness of the passed-in values
Line 140: Tell the test runner to stop waiting through whatever mechanism is given to us
Line 141: by the test framework (in this case, that’s the done() function)
Line 142: 6.1.2
Line 143: Waiting for the act
Line 144: Because we’re using callbacks as exit points, our test has to explicitly wait until the par-
Line 145: allel execution completes. That parallel execution could be on the JavaScript event
Line 146: loop or it could be in a separate thread, or even in a separate process if you’re using
Line 147: another language.
Line 148:  In the Arrange-Act-Assert pattern, the act part is the thing we need to wait out.
Line 149: Most test frameworks will allow us to do so with special helper functions. In this case,
Line 150: we can use the optional done callback that Jest provides to signal that the test needs to
Line 151: wait until we explicitly call done(). If done() isn’t called, our test will time out and fail
Line 152: after the default 5 seconds (which is configurable, of course).
Line 153:  Jest has other means for testing asynchronous code, a couple of which we’ll cover
Line 154: later in the chapter.
Line 155: 6.1.3
Line 156: Integration testing of async/await
Line 157: What about the async/await version? We could technically write a test that looks almost
Line 158: exactly like the previous one, since async/await is just syntactic sugar over promises.
Line 159: test("NETWORK REQUIRED (await): correct content, true", (done) => {
Line 160:   samples.isWebsiteAliveWithAsyncAwait().then((result) => {
Line 161:     expect(result.success).toBe(true);
Line 162:     expect(result.status).toBe("ok");
Line 163:     done();
Line 164:   });
Line 165: });
Line 166: However, a test that uses callbacks such as done() and then() is much less readable
Line 167: than one using the Arrange-Act-Assert pattern. The good news is there’s no need to
Line 168: complicate our lives by forcing ourselves to use callbacks. We can use the await syntax
Line 169: in our test as well. This will force us to put the async keyword in front of the test func-
Line 170: tion, but, overall, our test becomes simpler and more readable, as you can see here.
Line 171: test("NETWORK REQUIRED2 (await): correct content, true", async () => {
Line 172:   const result = await samples.isWebsiteAliveWithAsyncAwait();
Line 173:   expect(result.success).toBe(true);
Line 174:   expect(result.status).toBe("ok");
Line 175: });
Line 176: Listing 6.3
Line 177: Integration test with callbacks and .then()
Line 178: Listing 6.4
Line 179: Integration test with async/await
Line 180: 
Line 181: --- 페이지 153 ---
Line 182: 125
Line 183: 6.2
Line 184: Making our code unit-test friendly
Line 185: Having asynchronous code that allows us to use the async/await syntax turns our test
Line 186: into almost a run-of-the-mill value-based test. The entry point is also the exit point, as
Line 187: we saw in figure 6.1. 
Line 188:  Even though the call is simplified, the call is still asynchronous underneath,
Line 189: which is why I still call this an integration test. What are the caveats for this type of
Line 190: test? Let’s discuss.
Line 191: 6.1.4
Line 192: Challenges with integration tests
Line 193: The tests we’ve just written aren’t horrible as far as integration tests go. They’re rela-
Line 194: tively short and readable, but they still suffer from what any integration test suffers from:
Line 195: Lengthy run time—Compared to unit tests, integration tests are orders of magni-
Line 196: tude slower, sometimes taking seconds or even minutes.
Line 197: Flaky—Integration tests can present inconsistent results (different timings
Line 198: based on where they run, inconsistent failures or successes, etc.)
Line 199: Tests possibly irrelevant code and environment conditions—Integration tests test mul-
Line 200: tiple pieces of code that might be unrelated to what we care about. (In our case,
Line 201: it’s the node-fetch library, network conditions, firewall, external website func-
Line 202: tionality, etc.)
Line 203: Longer investigations—When an integration test fails, it requires more time for
Line 204: investigation and debugging because there are many possible reasons for a failure.
Line 205: Simulation is harder—It is harder than it needs to be to simulate a negative test
Line 206: with an integration test (simulating wrong website content, website down, net-
Line 207: work down, etc.)
Line 208: Harder to trust results—We might believe the failure of an integration test is due
Line 209: to an external issue when in fact it’s a bug in our code. I’ll talk about trust more
Line 210: in the next chapter.
Line 211: Does all this mean you shouldn’t write integration tests? No, I believe you should abso-
Line 212: lutely have integration tests, but you don’t need to have that many of them to get
Line 213: enough confidence in your code. Whatever integration tests don’t cover should be
Line 214: covered by lower-level tests, such as unit, API, or component tests. I’ll discuss this strat-
Line 215: egy at length in chapter 10, which focuses on testing strategies.
Line 216: 6.2
Line 217: Making our code unit-test friendly
Line 218: How can we test the code with a unit test? I’ll show you some patterns that I use to
Line 219: make the code more unit testable (i.e., to more easily inject or avoid dependencies,
Line 220: and to check exit points): 
Line 221: Extract Entry Point pattern—Extracting the parts of the production code that are
Line 222: pure logic into their own functions, and treating those functions as entry points
Line 223: for our tests
Line 224: Extract Adapter pattern—Extracting the thing that is inherently asynchronous and
Line 225: abstracting it away so that we can replace it with something that is synchronous
Line 226: 
Line 227: --- 페이지 154 ---
Line 228: 126
Line 229: CHAPTER 6
Line 230: Unit testing asynchronous code
Line 231: 6.2.1
Line 232: Extracting an entry point
Line 233: In this pattern, we take a specific unit of async work and split it into two pieces:
Line 234: The async part (which stays intact).
Line 235: The callbacks that are invoked when the async execution finishes. These are
Line 236: extracted as new functions, which eventually become entry points for a purely
Line 237: logical unit of work that we can invoke with pure unit tests.
Line 238: Figure 6.2 depicts this idea: In the before diagram, we have a single unit of work that
Line 239: contains asynchronous code mixed with logic that processes the async results inter-
Line 240: nally and returns a result via a callback or promise mechanism. In step 1, we extract
Line 241: the logic into its own function (or functions) that contains only the results of the
Line 242: async work as inputs. In step 2, we externalize those functions so that we can use them
Line 243: as entry points for our unit tests.
Line 244: This provides us with the important ability to test the logical processing of the async
Line 245: callbacks (and to simulate inputs easily). At the same time, we can choose to write a
Line 246: higher-level integration test against the original unit of work to gain confidence that
Line 247: the async orchestration works correctly as well. 
Line 248:  If we do integration tests only for all our scenarios, we would end up in a world of
Line 249: many long-running and flaky tests. In the new world, we’re able to have most of our
Line 250: tests be fast and consistent, and to have a small layer of integration tests on top to
Line 251: make sure all the orchestration works in between. This way we don’t sacrifice speed
Line 252: and maintainability for confidence.
Line 253: Before
Line 254: Step 1
Line 255: Step 2
Line 256: Callback/async result
Line 257: Logic
Line 258: processing
Line 259: Entry point
Line 260: Callback
Line 261: Async code
Line 262: Entry point
Line 263: Callback/async result
Line 264: Unit of work
Line 265: Logic
Line 266: processing
Line 267: Unit of work
Line 268: Entry point
Line 269: Callback/async result
Line 270: Async
Line 271: code
Line 272: Logic
Line 273: processing
Line 274: Callback
Line 275: Figure 6.2
Line 276: Extracting the internal processing logic into a separate unit of work helps simplify the tests, because 
Line 277: we are able to verify the new unit of work synchronously and without involving external dependencies.
Line 278: 
Line 279: --- 페이지 155 ---
Line 280: 127
Line 281: 6.2
Line 282: Making our code unit-test friendly
Line 283: EXAMPLE OF EXTRACTING A UNIT OF WORK
Line 284: Let’s apply this pattern to the code from listing 6.1. Figure 6.3 shows the steps we’ll
Line 285: follow:
Line 286: b
Line 287: The before state contains processing logic that is baked into the isWebsite-
Line 288: Alive() function.
Line 289: c
Line 290: We’ll extract any logical code that happens at the edge of the fetch results
Line 291: and put it in two separate functions: one for handling the success case, and
Line 292: the other for the error case.
Line 293: d
Line 294: We’ll then externalize these two functions so that we can invoke them directly
Line 295: from unit tests.
Line 296: The following listing shows the refactored code.
Line 297: //Entry Point
Line 298: const isWebsiteAlive = (callback) => {
Line 299:   fetch("http://example.com")
Line 300:     .then(throwOnInvalidResponse)
Line 301:     .then((resp) => resp.text())
Line 302:     .then((text) => {
Line 303:       processFetchSuccess(text, callback);
Line 304:     })
Line 305:     .catch((err) => {
Line 306:       processFetchError(err, callback);
Line 307:     });
Line 308: };
Line 309: Listing 6.5
Line 310: Extracting entry points with callback
Line 311: Before
Line 312: Extract logic
Line 313: Externalize entry points
Line 314: Callback/async result
Line 315: Pure logic
Line 316: processFetchSuccess(vars)
Line 317: Callback
Line 318: Call fetch(url)
Line 319: isWebsiteAlive(callback)Callback
Line 320: Unit of work
Line 321: Pure logic
Line 322: Unit of work
Line 323: isWebsiteAlive(callback)
Line 324: Callback
Line 325: Call
Line 326: fetch(url)
Line 327: processFetchSuccess(vars)
Line 328: processFetchError(vars)
Line 329: Callback
Line 330: New
Line 331: unit of work
Line 332: Pure logic
Line 333: processFetchError(vars)
Line 334: 1
Line 335: 2
Line 336: 3
Line 337: (Unit of work logic testable directly)
Line 338: (Async decoupled from logic)
Line 339: (Async coupled with logic)
Line 340: Figure 6.3
Line 341: Extracting the success and error-handling logic from isWebsiteAlive() to test that logic 
Line 342: separately
Line 343: 
Line 344: --- 페이지 156 ---
Line 345: 128
Line 346: CHAPTER 6
Line 347: Unit testing asynchronous code
Line 348: const throwOnInvalidResponse = (resp) => {
Line 349:   if (!resp.ok) {
Line 350:     throw Error(resp.statusText);
Line 351:   }
Line 352:   return resp;
Line 353: };
Line 354: //Entry Point
Line 355: const processFetchSuccess = (text, callback) => {         
Line 356:   if (text.includes("illustrative")) {
Line 357:     callback({ success: true, status: "ok" });
Line 358:   } else {
Line 359:     callback({ success: false, status: "missing text" });
Line 360:   }
Line 361: };
Line 362: //Entry Point
Line 363: const processFetchError = (err, callback) => {            
Line 364:   callback({ success: false, status: err });
Line 365: };
Line 366: As you can see, the original unit we started with now has three entry points instead of
Line 367: the single one we started with. The new entry points can be used for unit testing, while
Line 368: the original one can still be used for integration testing, as shown in figure 6.4.
Line 369: We’d still want an integration test for the original entry point, but not more than one
Line 370: or two of those. Any other scenario can be simulated using the purely logical entry
Line 371: points, quickly and painlessly. 
Line 372:  
Line 373: New entry 
Line 374: points (units 
Line 375: of work)
Line 376: isWebsiteAlive(callback)
Line 377: Callback version
Line 378: Callback
Line 379: Website
Line 380: checkup
Line 381: Before
Line 382: isWebsiteAlive(callback)
Line 383: Callback version
Line 384: Website
Line 385: checkup
Line 386: Callback
Line 387: After
Line 388: processFetchSuccess(text, callback)
Line 389: processFetchError(err, callback)
Line 390: Figure 6.4
Line 391: New entry points introduced after extracting the two new functions. The new functions can now be 
Line 392: tested with simpler unit tests instead of the integration tests that were required before the refactoring.
Line 393: 
Line 394: --- 페이지 157 ---
Line 395: 129
Line 396: 6.2
Line 397: Making our code unit-test friendly
Line 398:  Now we’re free to write unit tests that invoke the new entry points, like this.
Line 399: describe("Website alive checking", () => {
Line 400:   test("content matches, returns true", (done) => {
Line 401:     samples.processFetchSuccess("illustrative", (err, result) => {  
Line 402:       expect(err).toBeNull();
Line 403:       expect(result.success).toBe(true);
Line 404:       expect(result.status).toBe("ok");
Line 405:       done();
Line 406:     });
Line 407:   });
Line 408:   test("website content does not match, returns false", (done) => {
Line 409:     samples.processFetchSuccess("bad content", (err, result) => {   
Line 410:       expect(err.message).toBe("missing text");
Line 411:       done();
Line 412:     });
Line 413:   });
Line 414:   test("When fetch fails, returns false", (done) => {
Line 415:    samples.processFetchError("error text", (err,result) => {        
Line 416:       expect(err.message).toBe("error text");
Line 417:       done();
Line 418:     });
Line 419:   });
Line 420: });
Line 421: Notice that we are invoking the new entry points directly, and we’re able to simulate
Line 422: various conditions easily. Nothing is asynchronous in these tests, but we still need
Line 423: the done() function, since the callbacks might not be invoked at all, and we’ll want
Line 424: to catch that.
Line 425:  We still need at least one integration test that gives us confidence that the asyn-
Line 426: chronous orchestration works between our entry points. That’s where the original
Line 427: integration test can help, but we don’t need to write all our test scenarios as integra-
Line 428: tion tests anymore (more on this in chapter 10).
Line 429: EXTRACTING AN ENTRY POINT WITH AWAIT
Line 430: The same pattern we just applied can work well for standard async/await function
Line 431: structures. Figure 6.5 illustrates that refactoring.
Line 432:  By providing the async/await syntax, we can go back to writing code in a linear
Line 433: fashion, without using callback arguments. The isWebsiteAlive() function starts
Line 434: looking almost exactly the same as regular synchronous code, only returning values
Line 435: and throwing errors when needed. 
Line 436:  Listing 6.7 shows how that looks in our production code.
Line 437:  
Line 438:  
Line 439:  
Line 440:  
Line 441:  
Line 442: Listing 6.6
Line 443: Unit tests with extracted entry points
Line 444: Invoking 
Line 445: the new 
Line 446: entry 
Line 447: points
Line 448: 
Line 449: --- 페이지 158 ---
Line 450: 130
Line 451: CHAPTER 6
Line 452: Unit testing asynchronous code
Line 453: //Entry Point
Line 454: const isWebsiteAlive = async () => {
Line 455:   try {
Line 456:     const resp = await fetch("http://example.com");
Line 457:     throwIfResponseNotOK(resp);
Line 458:     const text = await resp.text();
Line 459:     return processFetchContent(text);
Line 460:   } catch (err) {
Line 461:     return processFetchError(err);
Line 462:   }
Line 463: };
Line 464: const throwIfResponseNotOK = (resp) => {
Line 465:   if (!resp.ok) {
Line 466:     throw resp.statusText;
Line 467:   }
Line 468: };
Line 469: //Entry Point
Line 470: const processFetchContent = (text) => {
Line 471:   const included = text.includes("illustrative");
Line 472:   if (included) {
Line 473:     return { success: true, status: "ok" };          
Line 474:   }
Line 475:   return { success: false, status: "missing text" }; 
Line 476: };
Line 477: //Entry Point
Line 478: const processFetchError = (err) => {
Line 479:   return { success: false, status: err };            
Line 480: };
Line 481: Listing 6.7
Line 482: The function written with async/await instead of callbacks
Line 483: Async/await version
Line 484: Before
Line 485: Async/await version
Line 486: After
Line 487: processFetchSuccess(text)
Line 488: processFetchError(err)
Line 489: isWebsiteAlive()
Line 490: Return
Line 491: value/error
Line 492: isWebsiteAlive()
Line 493: Return
Line 494: value/error
Line 495: Website
Line 496: checkup
Line 497: Website
Line 498: checkup
Line 499: Figure 6.5
Line 500: Extracting entry points with async/await
Line 501: Returning a 
Line 502: value instead 
Line 503: of calling a 
Line 504: callback
Line 505: 
Line 506: --- 페이지 159 ---
Line 507: 131
Line 508: 6.2
Line 509: Making our code unit-test friendly
Line 510: Notice that, unlike the callback examples, we’re using return or throw to denote suc-
Line 511: cess or failure. This is a common pattern of writing code using async/await.
Line 512:  Our tests are simplified as well, as shown in the following listing.
Line 513: describe("website up check", () => {
Line 514:   test("on fetch success with good content, returns true", () => {
Line 515:     const result = samples.processFetchContent("illustrative");
Line 516:     expect(result.success).toBe(true);
Line 517:     expect(result.status).toBe("ok");
Line 518:   });
Line 519:   test("on fetch success with bad content, returns false", () => {
Line 520:     const result = samples.processFetchContent("text not on site");
Line 521:     expect(result.success).toBe(false);
Line 522:     expect(result.status).toBe("missing text");
Line 523:   });
Line 524:   test("on fetch fail, throws ", () => {
Line 525:     expect(() => samples.processFetchError("error text"))
Line 526:       .toThrowError("error text");
Line 527:   });
Line 528: });
Line 529: Again, notice that we don’t need to add any kind of async/await-related keywords or
Line 530: to be explicit about waiting for execution, because we’ve separated the logical unit of
Line 531: work from the asynchronous pieces that make our lives more complicated.
Line 532: 6.2.2
Line 533: The Extract Adapter pattern
Line 534: The Extract Adapter pattern takes the opposite view from the previous pattern. We
Line 535: look at the asynchronous piece of code just like we look at any dependency we’ve dis-
Line 536: cussed in the previous chapters—as something we’d like to replace in our tests to
Line 537: gain more control. Instead of extracting the logical code into its own set of entry
Line 538: points, we’ll extract the asynchronous code (our dependency) and abstract it away
Line 539: under an adapter, which we can later inject, just like any other dependency. Figure 6.6
Line 540: shows this.
Line 541:  It’s also common to create a special interface for the adapter that is simplified for
Line 542: the needs of the consumer of the dependency. Another name for this approach is the
Line 543: interface segregation principle. In this case, we’ll create a network-adapter module that
Line 544: hides the real fetching functionality and has its own custom functions, as shown in fig-
Line 545: ure 6.7.
Line 546: Listing 6.8
Line 547: Testing entry points extracted from async/await
Line 548: 
Line 549: --- 페이지 160 ---
Line 550: 132
Line 551: CHAPTER 6
Line 552: Unit testing asynchronous code
Line 553: Before
Line 554: After
Line 555: Entry point
Line 556: Exit point
Line 557: Unit of work
Line 558: Dependency
Line 559: Logic
Line 560: processing
Line 561: Inject adapter
Line 562: Entry point
Line 563: Exit point
Line 564: Adapter
Line 565: Dependency
Line 566: Figure 6.6
Line 567: Extracting a dependency and wrapping it with an adapter helps us simplify that 
Line 568: dependency and replace it with a fake in tests.
Line 569: Before
Line 570: After
Line 571: Entry point
Line 572: Exit point
Line 573: website-verifier
Line 574: node-fetch
Line 575: Logic
Line 576: Logic
Line 577: Inject/import
Line 578: network-adapter
Line 579: website-verifier
Line 580: network-adapter
Line 581: fetchUrlText(url)
Line 582: async
Line 583: isWebsiteAlive()
Line 584: async
Line 585: node-fetch
Line 586: Figure 6.7
Line 587: Wrapping the node-fetch module with our own network-adapter module helps us expose only 
Line 588: the functionality our application needs, expressed in the language most suitable for the problem at hand.
Line 589: 
Line 590: --- 페이지 161 ---
Line 591: 133
Line 592: 6.2
Line 593: Making our code unit-test friendly
Line 594: The following listing shows what the network-adapter module looks like.
Line 595: const fetch = require("node-fetch");
Line 596: const fetchUrlText = async (url) => {
Line 597:   const resp = await fetch(url);
Line 598:   if (resp.ok) {
Line 599:     const text = await resp.text();
Line 600:     return { ok: true, text: text };
Line 601:   }
Line 602:   return { ok: false, text: resp.statusText };
Line 603: };   
Line 604: Note that the network-adapter module is the only module in the project that imports
Line 605: node-fetch. If that dependency changes at some point in the future, this increases
Line 606: the chances that only the current file would need to change. We’ve also simplified the
Line 607: function both by name and by functionality. We’re hiding the need to fetch the status
Line 608: and the text from the URL, and we’re abstracting them both under a single easier-to-
Line 609: use function.
Line 610:  Now we get to choose how to use the adapter. First, we can use it in the modular
Line 611: style. Then we’ll use a functional approach and an object-oriented one with a strongly
Line 612: typed interface.
Line 613: MODULAR ADAPTER
Line 614: The following listing shows a modular use of network-adapter by our initial isWebsite-
Line 615: Alive() function.
Line 616: const network = require("./network-adapter");
Line 617: const isWebsiteAlive = async () => {
Line 618:   try {
Line 619:     const result = await network.fetchUrlText("http://example.com");
Line 620:     if (!result.ok) {
Line 621:       throw result.text;
Line 622:     }
Line 623: Interface segregation principle
Line 624: The term interface segregation principle was coined by Robert Martin. Imagine a data-
Line 625: base dependency with dozens of functions hidden behind an adapter whose interface
Line 626: might only contain a couple of functions with custom names and parameters. The
Line 627: adapter serves to hide the complexity and simplify both the consumer’s code and the
Line 628: tests that simulate it. For more information on interface segregation, see the Wikipe-
Line 629: dia article about it: https://en.wikipedia.org/wiki/Interface_segregation_principle.
Line 630: Listing 6.9
Line 631: The network-adapter code
Line 632: Listing 6.10
Line 633: isWebsiteAlive() using the network-adapter module
Line 634: 
Line 635: --- 페이지 162 ---
Line 636: 134
Line 637: CHAPTER 6
Line 638: Unit testing asynchronous code
Line 639:     const text = result.text;
Line 640:     return processFetchSuccess(text);
Line 641:   } catch (err) {
Line 642:     throw processFetchFail(err);
Line 643:   }
Line 644: };
Line 645: In this version, we are directly importing the network-adapter module, which we’ll
Line 646: fake in our tests later on. 
Line 647:  The unit tests for this module are shown in the following listing. Because we’re
Line 648: using a modular design, we can fake the module using jest.mock() in our tests. We’ll
Line 649: also inject the module in later examples, don’t worry.
Line 650: jest.mock("./network-adapter");    
Line 651: const stubSyncNetwork = require("./network-adapter");   
Line 652: const webverifier = require("./website-verifier");
Line 653: describe("unit test website verifier", () => {
Line 654:   beforeEach(jest.resetAllMocks);              
Line 655:   test("with good content, returns true", async () => {
Line 656:     stubSyncNetwork.fetchUrlText.mockReturnValue({     
Line 657:       ok: true,
Line 658:       text: "illustrative",
Line 659:     });
Line 660:     const result = await webverifier.isWebsiteAlive();    
Line 661:     expect(result.success).toBe(true);
Line 662:     expect(result.status).toBe("ok");
Line 663:   });
Line 664:   test("with bad content, returns false", async () => {
Line 665:     stubSyncNetwork.fetchUrlText.mockReturnValue({
Line 666:       ok: true,
Line 667:       text: "<span>hello world</span>",
Line 668:     });
Line 669:     const result = await webverifier.isWebsiteAlive();    
Line 670:     expect(result.success).toBe(false);
Line 671:     expect(result.status).toBe("missing text");
Line 672:   });
Line 673: Notice that we are using async/await again, because we are back to using the original
Line 674: entry point we started with at the beginning of the chapter. But just because we’re
Line 675: using await doesn’t mean our tests are running asynchronously. Our test code, and
Line 676: the production code it invokes, actually runs linearly, with an async-friendly signature.
Line 677: We’ll need to use async/await for the functional and object-oriented designs as well,
Line 678: because the entry point requires it.
Line 679:  I’ve named our fake network stubSyncNetwork to make the synchronous nature of
Line 680: the test clearer. Otherwise, it’s hard to tell just by looking at the test whether the code
Line 681: it invokes runs linearly or asynchronously.
Line 682: Listing 6.11
Line 683: Faking network-adapter with jest.mock
Line 684: Faking the network-adapter module
Line 685: Importing the 
Line 686: fake module
Line 687: Resetting all the stubs to avoid 
Line 688: any potential issues in other tests
Line 689: Simulating a 
Line 690: return value from 
Line 691: the stub module
Line 692: Using 
Line 693: await in 
Line 694: our tests
Line 695: 
Line 696: --- 페이지 163 ---
Line 697: 135
Line 698: 6.2
Line 699: Making our code unit-test friendly
Line 700: FUNCTIONAL ADAPTER
Line 701: In the functional design pattern, the design of the network-adapter module stays the
Line 702: same, but we enable its injection into our website-verifier differently. As you can
Line 703: see in the next listing, we add a new parameter to our entry point.
Line 704: const isWebsiteAlive = async (network) => {
Line 705:   const result = await network.fetchUrlText("http://example.com");
Line 706:   if (result.ok) {
Line 707:     const text = result.text;
Line 708:     return onFetchSuccess(text);
Line 709:   }
Line 710:   return onFetchError(result.text);
Line 711: };
Line 712: In this version, we’re expecting the network-adapter module to be injected through
Line 713: a common parameter to our function. In a functional design, we can use higher-order
Line 714: functions and currying to configure a pre-injected function with our own network
Line 715: dependency. In our tests, we can simply send in a fake network via this parameter. As
Line 716: far as the design of the injection goes, almost nothing else has changed from previous
Line 717: samples, other than the fact that we don’t import the network-adapter module any-
Line 718: more. Reducing the amount of imports and requires can help maintainability in the
Line 719: long run. 
Line 720:  Our tests are simpler in the following listing, with less boilerplate code.
Line 721: const webverifier = require("./website-verifier");
Line 722: const makeStubNetworkWithResult = (fakeResult) => {   
Line 723:   return {
Line 724:     fetchUrlText: () => {
Line 725:       return fakeResult;
Line 726:     },
Line 727:   };
Line 728: };
Line 729: describe("unit test website verifier", () => {
Line 730:   test("with good content, returns true", async () => {
Line 731:     const stubSyncNetwork = makeStubNetworkWithResult({
Line 732:       ok: true,
Line 733:       text: "illustrative",
Line 734:     });
Line 735:     const result = await webverifier.isWebsiteAlive(stubSyncNetwork);   
Line 736:     expect(result.success).toBe(true);
Line 737:     expect(result.status).toBe("ok");
Line 738:   });
Line 739:   test("with bad content, returns false", async () => {
Line 740:     const stubSyncNetwork = makeStubNetworkWithResult({
Line 741: Listing 6.12
Line 742: A functional injection design for isWebsiteAlive() 
Line 743: Listing 6.13
Line 744: Unit test with functional injection of network-adapter
Line 745: A new helper function 
Line 746: to create a custom 
Line 747: object that matches 
Line 748: the important parts of 
Line 749: the network-adapter’s 
Line 750: interface
Line 751: Injecting the
Line 752: custom object
Line 753: 
Line 754: --- 페이지 164 ---
Line 755: 136
Line 756: CHAPTER 6
Line 757: Unit testing asynchronous code
Line 758:       ok: true,
Line 759:       text: "unexpected content",
Line 760:     });
Line 761:     const result = await webverifier.isWebsiteAlive(stubSyncNetwork);   
Line 762:     expect(result.success).toBe(false);
Line 763:     expect(result.status).toBe("missing text");
Line 764:   });
Line 765:   …   
Line 766: Notice that we don’t need a lot of the boilerplate at the top of the file, as we did in the
Line 767: modular design. We don’t need to fake the module indirectly (via jest.mock), we
Line 768: don’t need to re-import it for our tests (via require), and we don’t need to reset Jest’s
Line 769: state using jest.resetAllMocks. All we need to do is call our new makeStubNetwork-
Line 770: WithResult helper function from each test to generate a new fake network adapter,
Line 771: and then inject the fake network by sending it as a parameter to our entry point.
Line 772: OBJECT-ORIENTED, INTERFACE-BASED ADAPTER
Line 773: We’ve taken a look at the modular and functional designs. Let’s now turn our atten-
Line 774: tion to the object-oriented side of the equation. In the object-oriented paradigm, we
Line 775: can take the parameter injection we’ve done before and promote it into a constructor
Line 776: injection pattern. We’ll start with the network adapter and its interfaces (public API
Line 777: and results signature) in the following listing.
Line 778: export interface INetworkAdapter {
Line 779:   fetchUrlText(url: string): Promise<NetworkAdapterFetchResults>;
Line 780: }
Line 781: export interface NetworkAdapterFetchResults {
Line 782:   ok: boolean;
Line 783:   text: string;
Line 784: }
Line 785: ch6-async/6-fetch-adapter-interface-oo/network-adapter.ts
Line 786:     
Line 787: export class NetworkAdapter implements INetworkAdapter {
Line 788:   async fetchUrlText(url: string): 
Line 789:         Promise<NetworkAdapterFetchResults> {
Line 790:     const resp = await fetch(url);
Line 791:     if (resp.ok) {
Line 792:       const text = await resp.text();
Line 793:       return Promise.resolve({ ok: true, text: text });
Line 794:     }
Line 795:     return Promise.reject({ ok: false, text: resp.statusText });
Line 796:   }
Line 797: }
Line 798: In the next listing, we create a WebsiteVerifier class that has a constructor that
Line 799: receives an INetworkAdapter parameter.
Line 800:  
Line 801: Listing 6.14
Line 802: NetworkAdapter and its interfaces
Line 803: Injecting the
Line 804: custom object
Line 805: 
Line 806: --- 페이지 165 ---
Line 807: 137
Line 808: 6.2
Line 809: Making our code unit-test friendly
Line 810: export interface WebsiteAliveResult {
Line 811:   success: boolean;
Line 812:   status: string;
Line 813: }
Line 814: export class WebsiteVerifier {
Line 815:   constructor(private network: INetworkAdapter) {}
Line 816:   isWebsiteAlive = async (): Promise<WebsiteAliveResult> => {
Line 817:     let netResult: NetworkAdapterFetchResults;
Line 818:     try {
Line 819:     netResult = await this.network.fetchUrlText("http://example.com");
Line 820:       if (!netResult.ok) {
Line 821:         throw netResult.text;
Line 822:       }
Line 823:       const text = netResult.text;
Line 824:       return this.processNetSuccess(text);
Line 825:     } catch (err) {
Line 826:       throw this.processNetFail(err);
Line 827:     }
Line 828:   };
Line 829:   processNetSuccess = (text): WebsiteAliveResult => {
Line 830:     const included = text.includes("illustrative");
Line 831:     if (included) {
Line 832:       return { success: true, status: "ok" };
Line 833:     }
Line 834:     return { success: false, status: "missing text" };
Line 835:   };
Line 836:   processNetFail = (err): WebsiteAliveResult => {
Line 837:     return { success: false, status: err };
Line 838:   };
Line 839: }
Line 840: The unit tests for this class can instantiate a fake network adapter and inject it through
Line 841: a constructor. In the following listing, we’ll use substitute.js to create a fake object that
Line 842: fits the new interface.
Line 843: const makeStubNetworkWithResult = (    
Line 844:   fakeResult: NetworkAdapterFetchResults
Line 845: ): INetworkAdapter => {
Line 846:   const stubNetwork = Substitute.for<INetworkAdapter>();   
Line 847:   stubNetwork.fetchUrlText(Arg.any()) 
Line 848:     .returns(Promise.resolve(fakeResult));   
Line 849:   return stubNetwork;
Line 850: };
Line 851: Listing 6.15
Line 852: WebsiteVerifier class with constructor injection
Line 853: Listing 6.16
Line 854: Unit tests for the object-oriented WebsiteVerifier
Line 855: Helper function to simulate 
Line 856: the network adapter
Line 857: Generating the 
Line 858: fake object
Line 859: Making the fake 
Line 860: object return what 
Line 861: the test requires
Line 862: 
Line 863: --- 페이지 166 ---
Line 864: 138
Line 865: CHAPTER 6
Line 866: Unit testing asynchronous code
Line 867: describe("unit test website verifier", () => {
Line 868:   test("with good content, returns true", async () => {
Line 869:     const stubSyncNetwork = makeStubNetworkWithResult({
Line 870:       ok: true,
Line 871:       text: "illustrative",
Line 872:     });
Line 873:     const webVerifier = new WebsiteVerifier(stubSyncNetwork);
Line 874:     const result = await webVerifier.isWebsiteAlive();
Line 875:     expect(result.success).toBe(true);
Line 876:     expect(result.status).toBe("ok");
Line 877:   });
Line 878:   test("with bad content, returns false", async () => {
Line 879:     const stubSyncNetwork = makeStubNetworkWithResult({
Line 880:       ok: true,
Line 881:       text: "unexpected content",
Line 882:     });
Line 883:     const webVerifier = new WebsiteVerifier(stubSyncNetwork);
Line 884:     const result = await webVerifier.isWebsiteAlive();
Line 885:     expect(result.success).toBe(false);
Line 886:     expect(result.status).toBe("missing text");
Line 887:   });    
Line 888: This type of Inversion of Control (IOC) and Dependency Injection (DI) works well. In
Line 889: the object-oriented world, constructor injection with interfaces is very common and
Line 890: can, in many instances, provide a valid and maintainable solution for separating your
Line 891: dependencies from your logic. 
Line 892: 6.3
Line 893: Dealing with timers
Line 894: Timers, such as setTimeout, represent a very JavaScript-specific problem. They are
Line 895: part of the domain and are used, for better or worse, in many pieces of code. Instead
Line 896: of extracting adapters and entry points, sometimes it’s just as useful to disable these
Line 897: functions and work around them. We’ll look at two patterns for getting around timers:
Line 898: Directly monkey-patching the function
Line 899: Using Jest and other frameworks to disable and control them
Line 900: 6.3.1
Line 901: Stubbing timers out with monkey-patching
Line 902: Monkey-patching is a way for a program to extend or modify supporting system soft-
Line 903: ware locally (affecting only the running instance of the program). Programming lan-
Line 904: guages and runtimes such as JavaScript, Ruby, and Python can accommodate monkey-
Line 905: patching pretty easily. It’s much more difficult to do with more strongly typed and
Line 906: compile-time languages such as C# and Java. I discuss monkey-patching in more detail
Line 907: in the appendix.
Line 908:  Here’s one way to do it in JavaScript. We’ll start with the following piece of code
Line 909: that uses the setTimeout method.
Line 910: 
Line 911: --- 페이지 167 ---
Line 912: 139
Line 913: 6.3
Line 914: Dealing with timers
Line 915: const calculate1 = (x, y, resultCallback) => {
Line 916:   setTimeout(() => { resultCallback(x + y); },
Line 917:     5000);
Line 918: };
Line 919: We can monkey-patch the setTimeout function to be synchronous by literally setting
Line 920: that function’s prototype in memory, as follows.
Line 921: const Samples = require("./timing-samples");
Line 922: describe("monkey patching ", () => {
Line 923:   let originalTimeOut;
Line 924:   beforeEach(() => (originalTimeOut = setTimeout));    
Line 925:   afterEach(() => (setTimeout = originalTimeOut));    
Line 926:   test("calculate1", () => {
Line 927:     setTimeout = (callback, ms) => callback();    
Line 928:     Samples.calculate1(1, 2, (result) => {
Line 929:         expect(result).toBe(3);
Line 930:     });
Line 931:   });
Line 932: });
Line 933: Since everything is synchronous, we don’t need to use done() to wait for a callback
Line 934: invocation. We are replacing setTimeout with a purely synchronous implementation
Line 935: that invokes the received callback immediately.
Line 936:  The only downside to this approach is that it requires a bunch of boilerplate code
Line 937: and is generally more error prone, since we need to remember to clean up correctly.
Line 938: Let’s look at what frameworks like Jest provide us with to handle these situations.
Line 939: 6.3.2
Line 940: Faking setTimeout with Jest
Line 941: Jest provides us with three major functions for handling most types of timers in
Line 942: JavaScript:
Line 943: 
Line 944: jest.useFakeTimers—Stubs out all the various timer functions, such as
Line 945: setTimetout
Line 946: 
Line 947: jest.resetAllTimers—Resets all fake timers to the real ones
Line 948: 
Line 949: jest.advanceTimersToNextTimer—Triggers any fake timer so that any callbacks
Line 950: are triggered
Line 951: Together, these functions take care of most of the boilerplate code for us.
Line 952:  Here’s the same test we just did in listing 6.18, this time using Jest’s helper functions.
Line 953:  
Line 954:  
Line 955: Listing 6.17
Line 956: Code with setTimeout we’d like to monkey-patch 
Line 957: Listing 6.18
Line 958: A simple monkey-patching pattern
Line 959: Saving the 
Line 960: original 
Line 961: setTimeout
Line 962: Restoring the 
Line 963: original setTimeout
Line 964: Monkey-patching 
Line 965: the setTimeout
Line 966: 
Line 967: --- 페이지 168 ---
Line 968: 140
Line 969: CHAPTER 6
Line 970: Unit testing asynchronous code
Line 971: describe("calculate1 - with jest", () => {
Line 972:   beforeEach(jest.clearAllTimers);
Line 973:   beforeEach(jest.useFakeTimers);
Line 974:   test("fake timeout with callback", () => {
Line 975:     Samples.calculate1(1, 2, (result) => {
Line 976:       expect(result).toBe(3);
Line 977:     });
Line 978:     jest.advanceTimersToNextTimer();
Line 979:   });
Line 980: });
Line 981: Notice that, once again, we don’t need to call done(), since everything is synchronous.
Line 982: At the same time, we have to use advanceTimersToNextTimer because, without it, our
Line 983: fake setTimeout would be stuck forever. advanceTimersToNextTimer is also useful for
Line 984: scenarios such as when the module being tested schedules a setTimeout whose call-
Line 985: back schedules another setTimeout recursively (meaning the scheduling never
Line 986: stops). In these scenarios, it’s useful to be able to run forward in time, step by step. 
Line 987:  With advanceTimersToNextTimer, you could potentially advance all timers by a
Line 988: specified number of steps to simulate the passage of steps that will trigger the next
Line 989: timer callback waiting in line.
Line 990:  The same pattern also works well with setInterval, as shown next.
Line 991: const calculate4 = (getInputsFn, resultFn) => {
Line 992:   setInterval(() => {
Line 993:     const { x, y } = getInputsFn();
Line 994:     resultFn(x + y);
Line 995:   }, 1000);
Line 996: };
Line 997: In this case, our function takes in two callbacks as parameters: one to provide the
Line 998: inputs to calculate, and the other to call back with the calculation result. It uses set-
Line 999: Interval to continuously get more inputs and calculate their results.
Line 1000:  The following listing shows a test that will advance our timer, trigger the interval
Line 1001: twice, and expect the same result from both invocations.
Line 1002: describe("calculate with intervals", () => {
Line 1003:   beforeEach(jest.clearAllTimers);
Line 1004:   beforeEach(jest.useFakeTimers);
Line 1005:   test("calculate, incr input/output, calculates correctly", () => {
Line 1006:     let xInput = 1;
Line 1007:     let yInput = 2;
Line 1008:     const inputFn = () => ({ x: xInput++, y: yInput++ });      
Line 1009: Listing 6.19
Line 1010: Faking setTimeout with Jest
Line 1011: Listing 6.20
Line 1012: A function that uses setInterval
Line 1013: Listing 6.21
Line 1014: Advancing fake timers in a unit test
Line 1015: Incrementing a
Line 1016: variable to verify the
Line 1017: number of callbacks
Line 1018: 
Line 1019: --- 페이지 169 ---
Line 1020: 141
Line 1021: 6.4
Line 1022: Dealing with common events
Line 1023:     const results = [];
Line 1024:     Samples.calculate4(inputFn, (result) => results.push(result));
Line 1025:     jest.advanceTimersToNextTimer();   
Line 1026:     jest.advanceTimersToNextTimer();   
Line 1027:     expect(results[0]).toBe(3);
Line 1028:     expect(results[1]).toBe(5);
Line 1029:   });
Line 1030: });
Line 1031: In this example, we verify that the new values are being calculated and stored cor-
Line 1032: rectly. Notice that we could have written the same test with only a single invocation
Line 1033: and a single expect, and we would have gotten close to the same amount of confi-
Line 1034: dence that this more elaborate test provides, but I like to put in additional validation
Line 1035: when I need more confidence. 
Line 1036: 6.4
Line 1037: Dealing with common events
Line 1038: I can’t talk about async unit testing and not discuss the basic events flow. Hopefully
Line 1039: the topic of async unit testing now seems relatively straightforward, but I want to go
Line 1040: over the events part explicitly.
Line 1041: 6.4.1
Line 1042: Dealing with event emitters
Line 1043: To make sure we’re all on the same page, here’s a clear and concise definition of event
Line 1044: emitters from DigitalOcean’s “Using Event Emitters in Node.js” tutorial (http://mng
Line 1045: .bz/844z):
Line 1046: Event emitters are objects in Node.js that trigger an event by sending a message to signal
Line 1047: that an action was completed. JavaScript developers can write code that listens to events
Line 1048: from an event emitter, allowing them to execute functions every time those events are
Line 1049: triggered. In this context, events are composed of an identifying string and any data that
Line 1050: needs to be passed to the listeners.
Line 1051: Consider the Adder class in the following listing, which emits an event every time it
Line 1052: adds something.
Line 1053: const EventEmitter = require("events");
Line 1054: class Adder extends EventEmitter {
Line 1055:   constructor() {
Line 1056:     super();
Line 1057:   }
Line 1058:   add(x, y) {
Line 1059:     const result = x + y;
Line 1060:     this.emit("added", result);
Line 1061:     return result;
Line 1062: Listing 6.22
Line 1063: A simple event-emitter-based Adder
Line 1064: Invoking 
Line 1065: setInterval twice
Line 1066: 
Line 1067: --- 페이지 170 ---
Line 1068: 142
Line 1069: CHAPTER 6
Line 1070: Unit testing asynchronous code
Line 1071:   }
Line 1072: }
Line 1073: The simplest way to write a unit test that verifies that the event is emitted is to liter-
Line 1074: ally subscribe to the event in our test and verify that it triggers when we call the add
Line 1075: function.
Line 1076: describe("events based module", () => {
Line 1077:   describe("add", () => {
Line 1078:     it("generates addition event when called", (done) => {
Line 1079:       const adder = new Adder();
Line 1080:       adder.on("added", (result) => {
Line 1081:         expect(result).toBe(3);
Line 1082:         done();
Line 1083:       });
Line 1084:       adder.add(1, 2);
Line 1085:     });
Line 1086:   });
Line 1087: });
Line 1088: By using done(), we are verifying that the event actually was emitted. If we didn’t use
Line 1089: done(), and the event wasn’t emitted, our test would pass because the subscribed code
Line 1090: never executed. By adding expect(x).toBe(y), we are also verifying the values sent in
Line 1091: the event parameters, as well as implicitly testing that the event was triggered. 
Line 1092: 6.4.2
Line 1093: Dealing with click events
Line 1094: What about those pesky UI events, such as click? How can we test that we have bound
Line 1095: them correctly via our scripts? Consider the simple web page and associated logic in
Line 1096: listings 6.24 and 6.25.
Line 1097: <!DOCTYPE html>
Line 1098: <html lang="en">
Line 1099: <head>
Line 1100:     <meta charset="UTF-8">
Line 1101:     <title>File to Be Tested</title>
Line 1102:     <script src="index-helper.js"></script>
Line 1103: </head>
Line 1104: <body>
Line 1105:     <div>
Line 1106:         <div>A simple button</div>
Line 1107:         <Button data-testid="myButton" id="myButton">Click Me</Button>
Line 1108:         <div data-testid="myResult" id="myResult">Waiting...</div>
Line 1109:     </div>
Line 1110: </body>
Line 1111: </html> 
Line 1112: Listing 6.23
Line 1113: Testing an event emitter by subscribing to it
Line 1114: Listing 6.24
Line 1115: A simple web page with JavaScript click functionality
Line 1116: 
Line 1117: --- 페이지 171 ---
Line 1118: 143
Line 1119: 6.4
Line 1120: Dealing with common events
Line 1121: window.addEventListener("load", () => {
Line 1122:   document
Line 1123:     .getElementById("myButton")
Line 1124:     .addEventListener("click", onMyButtonClick);
Line 1125:   const resultDiv = document.getElementById("myResult");
Line 1126:   resultDiv.innerText = "Document Loaded";
Line 1127: });
Line 1128: function onMyButtonClick() {
Line 1129:   const resultDiv = document.getElementById("myResult");
Line 1130:   resultDiv.innerText = "Clicked!";
Line 1131: }
Line 1132: We have a very simple piece of logic that makes sure our button sets a special message
Line 1133: when clicked. How can we test this?
Line 1134:  Here’s an antipattern: we could subscribe to the click event in our tests and make
Line 1135: sure it is triggered, but this would provide no value to us. What we care about is that
Line 1136: the click has actually done something useful, other than triggering. 
Line 1137:  Here’s a better way: we can trigger the click event and make sure it has changed
Line 1138: the correct value inside the page—this will provide real value. Figure 6.8 shows this.
Line 1139: The following listing shows what our test might look like.
Line 1140: /**
Line 1141:  * @jest-environment jsdom    
Line 1142:  */
Line 1143: //(the above is required for window events)
Line 1144: const fs = require("fs");
Line 1145: const path = require("path");
Line 1146: require("./index-helper.js");
Line 1147: Listing 6.25
Line 1148: The logic for the web page in JavaScript
Line 1149: Listing 6.26
Line 1150: Triggering a click event, and testing an element’s text
Line 1151: Trigger
Line 1152: event
Line 1153: document.load()
Line 1154: Trigger
Line 1155: event
Line 1156: click()
Line 1157: Verify text
Line 1158: in page element
Line 1159: Web page
Line 1160: Figure 6.8
Line 1161: Click as an entry point, 
Line 1162: and element as an exit point
Line 1163: Applying the browser-simulating 
Line 1164: jsdom environment just for this file 
Line 1165: 
Line 1166: --- 페이지 172 ---
Line 1167: 144
Line 1168: CHAPTER 6
Line 1169: Unit testing asynchronous code
Line 1170: const loadHtml = (fileRelativePath) => {
Line 1171:   const filePath = path.join(__dirname, "index.html");
Line 1172:   const innerHTML = fs.readFileSync(filePath);
Line 1173:   document.documentElement.innerHTML = innerHTML;
Line 1174: };
Line 1175: const loadHtmlAndGetUIElements = () => {
Line 1176:   loadHtml("index.html");
Line 1177:   const button = document.getElementById("myButton");
Line 1178:   const resultDiv = document.getElementById("myResult");
Line 1179:   return { window, button, resultDiv };
Line 1180: };
Line 1181: describe("index helper", () => {
Line 1182:   test("vanilla button click triggers change in result div", () => {
Line 1183:     const { window, button, resultDiv } = loadHtmlAndGetUIElements();
Line 1184:     window.dispatchEvent(new Event("load"));    
Line 1185:     button.click();   
Line 1186:     expect(resultDiv.innerText).toBe("Clicked!");   
Line 1187:   });
Line 1188: });   
Line 1189: In this example, I’ve extracted two utility methods, loadHtml and loadHtmlAndGetUI-
Line 1190: Elements, so that I can write cleaner, more readable tests, and so I’ll have fewer issues
Line 1191: changing my tests if UI item locations or IDs change in the future.
Line 1192:  In the test itself, we’re simulating the document.load event, so that our custom
Line 1193: script under test can start running and then triggering the click, as if the user had
Line 1194: clicked the button. Finally, the test verifies that an element in our document has
Line 1195: actually changed, which means our code successfully subscribed to the event and
Line 1196: did its work.
Line 1197:  Notice that we don’t actually care about the underlying logic inside the index
Line 1198: helper file. We just rely on observed state changes in the UI, which acts as our final
Line 1199: exit point. This allows less coupling in our tests, so that if our code under test changes,
Line 1200: we are less likely to need to change the test, unless the observable (publicly notice-
Line 1201: able) functionality has truly changed.
Line 1202: 6.5
Line 1203: Bringing in the DOM testing library
Line 1204: Our test has a lot of boilerplate code, mostly for finding elements and verifying their
Line 1205: contents. I recommend looking into the open source DOM Testing Library written by
Line 1206: Kent C. Dodds (https://github.com/kentcdodds/dom-testing-library-with-anything).
Line 1207: This library has variants applicable to most frontend JavaScript frameworks today,
Line 1208: such as React, Angular, and Vue.js. We’ll be using the vanilla version of it named DOM
Line 1209: Testing Library. 
Line 1210:  What I like about this library is that it aims to allow us to write tests closer to the
Line 1211: point of view of the user interacting with our web page. Instead of using IDs for ele-
Line 1212: ments, we query by element text; firing events is a bit cleaner; and querying and
Line 1213: Simulating the 
Line 1214: document.load event
Line 1215: Triggering
Line 1216: the click
Line 1217: Verifying that an element 
Line 1218: in our document has 
Line 1219: actually changed
Line 1220: 
Line 1221: --- 페이지 173 ---
Line 1222: 145
Line 1223: Summary
Line 1224: waiting for elements to appear or disappear is cleaner and hidden under syntactic
Line 1225: sugar. It’s quite useful once you use it in multiple tests. 
Line 1226:  Here’s what our test looks like with this library.
Line 1227: const { fireEvent, findByText, getByText }  
Line 1228:     = require("@testing-library/dom");      
Line 1229: const loadHtml = (fileRelativePath) => {
Line 1230:   const filePath = path.join(__dirname, "index.html");
Line 1231:   const innerHTML = fs.readFileSync(filePath);
Line 1232:   document.documentElement.innerHTML = innerHTML;
Line 1233:   return document.documentElement;        
Line 1234: };
Line 1235: const loadHtmlAndGetUIElements = () => {
Line 1236:   const docElem = loadHtml("index.html");
Line 1237:   const button = getByText(docElem, "click me", { exact: false });
Line 1238:   return { window, docElem, button };
Line 1239: };
Line 1240: describe("index helper", () => {
Line 1241:   test("dom test lib button click triggers change in page", () => {
Line 1242:     const { window, docElem, button } = loadHtmlAndGetUIElements();
Line 1243:     fireEvent.load(window);        
Line 1244:     fireEvent.click(button);       
Line 1245:     //wait until true or timeout in 1 sec
Line 1246:     expect(findByText(docElem,"clicked", { exact: false })).toBeTruthy();  
Line 1247:   });
Line 1248: });
Line 1249: Notice how the library allows us to use the regular text of the page items to get the
Line 1250: items, instead of their IDs or test IDs. This is part of the way the library pushes us to
Line 1251: work so things feel more natural and from the user’s point of view. To make the test
Line 1252: more sustainable over time, we’re using the exact: false flag so that we don’t have to
Line 1253: worry about uppercasing issues or missing letters at the start or end of strings. This
Line 1254: removes the need to change the test for small text changes that are less important.
Line 1255: Summary
Line 1256: Testing asynchronous code directly results in flaky tests that take a long time to
Line 1257: execute. To fix these issues, you can take two approaches: extract an entry point
Line 1258: or extract an adapter.
Line 1259: Extracting an entry point is when you extract the pure logic into separate func-
Line 1260: tions and treat those functions as entry points for your tests. The extracted
Line 1261: entry point can either accept a callback as an argument or return a value. Prefer
Line 1262: return values over callbacks for simplicity.
Line 1263: Listing 6.27
Line 1264: Using the DOM Testing Library in a simple test
Line 1265: Importing some of the 
Line 1266: library APIs to be used
Line 1267: Library APIs require 
Line 1268: the document element 
Line 1269: as the basis for most 
Line 1270: of the work.
Line 1271: Using the library’s fireEvent API 
Line 1272: to simplify event dispatching
Line 1273: This query will wait until the item is
Line 1274: found or will timeout within 1 second.
Line 1275: 
Line 1276: --- 페이지 174 ---
Line 1277: 146
Line 1278: CHAPTER 6
Line 1279: Unit testing asynchronous code
Line 1280: Extracting an adapter involves extracting a dependency that is inherently asyn-
Line 1281: chronous and abstracting it away so that you can replace it with something that
Line 1282: is synchronous. The adapter may be of different types:
Line 1283: – Modular—When you stub the whole module (file) and replace specific func-
Line 1284: tions in it.
Line 1285: – Functional—When you inject a function or value into the system under test.
Line 1286: You can replace the injected value with a stub in tests.
Line 1287: – Object-oriented—When you use an interface in the production code and cre-
Line 1288: ate a stub that implements that interface in the test code.
Line 1289: Timers (such as setTimeout and setInterval) can be replaced either directly
Line 1290: with monkey-patching or by using Jest or another framework to disable and
Line 1291: control them.
Line 1292: Events are best tested by verifying the end result they produce—changes in the
Line 1293: HTML document the user can see. You can do this either directly or by using
Line 1294: libraries such as the DOM Testing Library. 
