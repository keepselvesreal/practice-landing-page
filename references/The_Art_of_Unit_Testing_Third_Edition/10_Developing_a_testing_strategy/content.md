Line 1: 
Line 2: --- 페이지 222 ---
Line 3: 194
Line 4: Developing
Line 5: a testing strategy
Line 6: Unit tests represent just one of the types of tests you could and should write. In this
Line 7: chapter, we’ll discuss how unit testing fits into an organizational testing strategy. As
Line 8: soon as we start to look at other types of tests, we start asking some really important
Line 9: questions:
Line 10: At what level do we want to test various features? (UI, backend, API, unit,
Line 11: etc.)
Line 12: How do we decide at which level to test a feature? Do we test it multiple times
Line 13: on many levels?
Line 14: Should we have more functional end-to-end tests or more unit tests?
Line 15: This chapter covers
Line 16: Testing level pros and cons
Line 17: Common antipatterns in test levels
Line 18: The test recipe strategy
Line 19: Delivery-blocking and non-blocking tests
Line 20: Delivery vs. discovery pipelines
Line 21: Test parallelization
Line 22: 
Line 23: --- 페이지 223 ---
Line 24: 195
Line 25: 10.1
Line 26: Common test types and levels
Line 27: How can we optimize the speed of tests without sacrificing trust in them?
Line 28: Who should write each type of test? 
Line 29: The answers to these questions, and many more, are what I’d call a testing strategy. 
Line 30:  The first step in our journey is to frame the scope of the testing strategy in terms of
Line 31: test types. 
Line 32: 10.1
Line 33: Common test types and levels
Line 34: Different industries might have different test types and levels. Figure 10.1, which we
Line 35: first discussed in chapter 7, is a rather generic set of test types that I feel fits 90% of the
Line 36: organizations I consult with, if not more. The higher the level of the tests, the more
Line 37: real dependencies they use, which gives us confidence in the overall system’s correct-
Line 38: ness. The downside is that such tests are slower and flakier.
Line 39: Most speed
Line 40: • Easier to maintain
Line 41: • Easier to write
Line 42: • Faster feedback loop
Line 43: Most conﬁdence
Line 44: • Harder to maintain
Line 45: • Harder to write
Line 46: • Slower feedback loop
Line 47: Conﬁdence
Line 48: E2E/UI system tests
Line 49: E2E/UI isolated tests
Line 50: API tests (out of process)
Line 51: Integration tests (in memory)
Line 52: Component tests (in memory)
Line 53: Unit tests (in memory)
Line 54: Figure 10.1
Line 55: Common software test levels 
Line 56: 
Line 57: --- 페이지 224 ---
Line 58: 196
Line 59: CHAPTER 10
Line 60: Developing a testing strategy
Line 61: Nice diagram, but what do we do with it? We use it when we design a framework for
Line 62: decision making about which test to write. There are several criteria (things that
Line 63: make our jobs easier or harder) I like to pinpoint; these help me decide which test
Line 64: type to use.
Line 65: 10.1.1 Criteria for judging a test
Line 66: When we’re faced with more than two options to choose from, one of the best ways
Line 67: I’ve found to help me decide is to figure out what my obvious values are for the prob-
Line 68: lem at hand. These obvious values are the things we can all pretty much agree are use-
Line 69: ful or should be avoided when making the choice. Table 10.1 lists my obvious values
Line 70: for tests.
Line 71: All values are scaled from 1 to 5. As you’ll see, each level in figure 10.1 has pros and
Line 72: cons in each of these criteria. 
Line 73: 10.1.2 Unit tests and component tests
Line 74: Unit tests and component tests are the types of tests we’ve been discussing in this book
Line 75: so far. They both fit under the same category, with the only differentiation being that
Line 76: component tests might have more functions, classes, or components as part of the
Line 77: unit of work. In other words, component tests include more “stuff” between the entry
Line 78: and exit points.
Line 79:  Here are two test examples to illustrate the difference:
Line 80: Test A—A unit test of a custom UI button object in memory. You can instantiate
Line 81: it, click it, and see that it triggers some form of click event. 
Line 82: Test B—A component test that instantiates a higher-level form component and
Line 83: includes the button as part of its structure. The test verifies the higher-level
Line 84: form, with the button playing a small role as part of the higher-level scenario.
Line 85: Table 10.1
Line 86: Generic test scorecard
Line 87: Criterion
Line 88: Rating scale
Line 89: Notes
Line 90: Complexity
Line 91: 1–5
Line 92: How complicated a test is to write, read, or debug. 
Line 93: Lower is better. 
Line 94: Flakiness
Line 95: 1–5
Line 96: How likely a test is to fail because of things it does 
Line 97: not control—code from other groups, networks, data-
Line 98: bases, configuration, and more. Lower is better.
Line 99: Confidence when passes
Line 100: 1–5
Line 101: How much confidence is generated in our minds and 
Line 102: hearts when a test passes. Higher is better.  
Line 103: Maintainability
Line 104: 1–5
Line 105: How often the test needs to change, and how easy it 
Line 106: is to change. Higher is better. 
Line 107: Execution speed
Line 108: 1–5
Line 109: How quickly does the test finish? Higher is better. 
Line 110: 
Line 111: --- 페이지 225 ---
Line 112: 197
Line 113: 10.1
Line 114: Common test types and levels
Line 115: Both tests are still unit tests, in memory, and we have full control over all the things
Line 116: being used; there are no dependencies on files, databases, networks, configuration, or
Line 117: other things we don’t control. Test A is a lower-level unit test, and test B is a compo-
Line 118: nent test, or a higher-level unit test. 
Line 119:  The reason this differentiation needs to be made is because I often get asked what
Line 120: I would call a test with a different level of abstraction. The answer is that whether a test
Line 121: falls into the unit/component test category is based on the dependencies it does or
Line 122: doesn’t have, not on the abstraction level it uses. Table 10.2 shows the scorecard for
Line 123: the unit/component test layer.
Line 124: 10.1.3 Integration tests
Line 125: Integration tests look almost exactly like regular unit tests, but some of the dependen-
Line 126: cies are not stubbed out. For example, we might use a real configuration, a real data-
Line 127: base, a real filesystem, or all three. But to invoke the test, we still instantiate an object
Line 128: from our production code in memory and invoke an entry point function directly on
Line 129: that object. Table 10.3 shows the scorecard for integration tests.
Line 130: Table 10.2
Line 131: Unit/component test scorecard
Line 132: Complexity
Line 133: 1/5
Line 134: These are the least complex of all test types due to the smaller 
Line 135: scope and the fact that we can control everything in the test.
Line 136: Flakiness
Line 137: 1/5
Line 138: These are the least flaky of all test types, since we can control every-
Line 139: thing in the test. 
Line 140: Confidence when 
Line 141: passes
Line 142: 1/5
Line 143: It feels nice when a unit test passes, but we’re not really confident 
Line 144: that our application works. We just know that a small piece of it 
Line 145: does. 
Line 146: Maintainability
Line 147: 5/5
Line 148: These are the easiest to maintain out of all test types, since it’s rel-
Line 149: atively simple to read and to reason about.
Line 150: Execution speed
Line 151: 5/5
Line 152: These are the fastest of all test types, since everything runs in mem-
Line 153: ory without any hard dependencies on files, network, or databases. 
Line 154: Table 10.3
Line 155: Integration test scorecard
Line 156: Complexity
Line 157: 2/5
Line 158: These tests are slightly or greatly more complex, depending on the 
Line 159: number of dependencies that we do not fake in the test. 
Line 160: Flakiness
Line 161: 2–3/5
Line 162: These tests are slightly or much flakier depending on how many real 
Line 163: dependencies we use.
Line 164: Confidence when 
Line 165: passes
Line 166: 2–3/5
Line 167: It feels much better when an integration test passes because we are 
Line 168: verifying that the code uses something we do not control, like a data-
Line 169: base or a config file. 
Line 170: Maintainability
Line 171: 3–4/5
Line 172: These tests are more complex than a unit test because of the depen-
Line 173: dencies.
Line 174: Execution speed
Line 175: 3–4/5
Line 176: These tests are slightly or much slower than a unit test because of 
Line 177: the dependency on the filesystem, network, database, or threads.
Line 178: 
Line 179: --- 페이지 226 ---
Line 180: 198
Line 181: CHAPTER 10
Line 182: Developing a testing strategy
Line 183: 10.1.4 API tests
Line 184: In previous lower levels of tests, we haven’t needed to deploy the application under
Line 185: test or make it properly run to test it. At the API test level, we finally need to deploy, at
Line 186: least in part, the application under test and invoke it through the network. Unlike
Line 187: unit, component, and integration tests, which can be categorized as in-memory tests,
Line 188: API tests are out-of-process tests. We are no longer instantiating the unit under test
Line 189: directly in memory. This means we’re adding a new dependency into the mix: a net-
Line 190: work, as well as the deployment of some network service. Table 10.4 shows the score-
Line 191: card for API tests.
Line 192: 10.1.5 E2E/UI isolated tests
Line 193: At the level of isolated end-to-end (E2E) and user interface (UI) tests, we are testing
Line 194: our application from the point of view of a user. I use the word isolated to specify that
Line 195: we are testing only our own application or service, without deploying any dependency
Line 196: applications or services that our application might need. Such tests fake third-party
Line 197: authentication mechanisms, the APIs of other applications that are required to be
Line 198: deployed on the same server, and any code that is not specifically a part of the main
Line 199: application under test (including apps from the same organization’s other depart-
Line 200: ments—those would be faked as well). 
Line 201:  Table 10.5 shows the scorecard for E2E/UI isolated tests.
Line 202: Table 10.4
Line 203: API test scorecard
Line 204: Complexity
Line 205: 3/5
Line 206: These tests are slightly or greatly more complex, depending on the 
Line 207: deployment complexity, configuration, and API setup needed. Some-
Line 208: times we need to include the API schema in the test, which takes 
Line 209: extra work and thinking.  
Line 210: Flakiness
Line 211: 3–4/5
Line 212: The network adds more flakiness to the mix.
Line 213: Confidence when 
Line 214: passes
Line 215: 3–4/5
Line 216: It feels even better when an API test passes. We can trust that others 
Line 217: can call our API with confidence after deployment. 
Line 218: Maintainability
Line 219: 2–3/5
Line 220: The network adds more setup complexity and needs more care when 
Line 221: changing a test or adding/changing APIs.
Line 222: Execution speed
Line 223: 2–3/5
Line 224: The network slows the tests down considerably.
Line 225: Table 10.5
Line 226: E2E/UI isolated test scorecard
Line 227: Complexity
Line 228: 4/5
Line 229: These tests are much more complex than previous tests, since we are 
Line 230: dealing with user flows, UI-based changes, and capturing or scraping 
Line 231: the UI for integration and assertions. Waiting and timeouts abound.
Line 232: Flakiness
Line 233: 4/5
Line 234: There are lots of reasons the test may slow down, time out, or not 
Line 235: work due to the many dependencies involved.
Line 236: Confidence when 
Line 237: passes
Line 238: 4/5
Line 239: It’s a huge relief when this type of test passes. We gain a lot of confi-
Line 240: dence in our application.
Line 241: 
Line 242: --- 페이지 227 ---
Line 243: 199
Line 244: 10.2
Line 245: Test-level antipatterns
Line 246: 10.1.6 E2E/UI system tests
Line 247: At the level of system E2E and UI tests nothing is fake. This is as close to a production
Line 248: deployment as we can get: all dependency applications and services are real, but they
Line 249: might be differently configured to allow for our testing scenarios. Table 10.6 shows
Line 250: the scorecard for E2E/UI system tests.
Line 251: 10.2
Line 252: Test-level antipatterns
Line 253: Test-level antipatterns are not technical but organizational in nature. You’ve likely
Line 254: seen them firsthand. As a consultant, I can tell you that they are very prevalent. 
Line 255: 10.2.1 The end-to-end-only antipattern
Line 256: A very common strategy that an organization will have is using mostly, if not only, E2E
Line 257: tests (both isolated and system tests). Figure 10.2 shows what this looks like in the dia-
Line 258: gram of test levels and types.
Line 259:  Why is this an antipattern? Tests at this level are very slow, hard to maintain, hard
Line 260: to debug, and very flaky. These costs remain the same, while the value you get from
Line 261: each new E2E test diminishes.
Line 262: DIMINISHING RETURNS FROM E2E TESTS
Line 263: The first E2E test you write will bring you the most confidence because of how many
Line 264: other paths of code are included as part of that scenario, and because of the glue—
Line 265: the code orchestrating the work between your application and other systems—that
Line 266: gets invoked as part of that test. 
Line 267: Maintainability
Line 268: 1–2/5
Line 269: More dependencies add more setup complexity and require more care 
Line 270: when changing a test or adding or changing workflows. Tests are long 
Line 271: and usually have multiple steps. 
Line 272: Execution speed
Line 273: 1–2/5
Line 274: These tests can be very slow as we navigate user interfaces, some-
Line 275: times including logins, caching, multipage navigation, etc.
Line 276: Table 10.6
Line 277: E2E/UI system test scorecard
Line 278: Complexity
Line 279: 5/5
Line 280: These are the most complex tests to set up and write due to the num-
Line 281: ber of dependencies.
Line 282: Flakiness
Line 283: 5/5
Line 284: These tests can fail for any of thousands of different reasons, and 
Line 285: often for multiple reasons.
Line 286: Confidence when 
Line 287: passes
Line 288: 5/5
Line 289: These tests give us the highest confidence because of all the code 
Line 290: that gets tested when the tests execute.
Line 291: Maintainability
Line 292: 1/5
Line 293: These tests are hard to maintain, due to the many dependencies and 
Line 294: long workflows.
Line 295: Execution speed
Line 296: 1/5
Line 297: These tests are very slow because they use the UI and real depen-
Line 298: dencies. They can take minutes to hours for a single test.
Line 299: Table 10.5
Line 300: E2E/UI isolated test scorecard (continued)
Line 301: 
Line 302: --- 페이지 228 ---
Line 303: 200
Line 304: CHAPTER 10
Line 305: Developing a testing strategy
Line 306: But what about the second E2E test? It will usually be a variation on the first test,
Line 307: which means it might only bring a small fraction of the same value. Maybe there’s a
Line 308: difference in a combo box and other UI elements, but all the dependencies, such as
Line 309: the database and third-party systems, remain the same. 
Line 310:  The amount of extra confidence you get from the second E2E test is also only a
Line 311: fraction of the extra confidence you got from the first E2E test. However, the cost
Line 312: of debugging, changing, reading, and running that test is not a fraction; it is basi-
Line 313: cally the same as for the previous test. You’re incurring a lot of extra work for a very
Line 314: small bit of extra confidence, which is why I like to say that E2E tests have quickly
Line 315: diminishing returns.
Line 316:  If I want variation on the first test, it would be much more pragmatic to test at a
Line 317: lower level than the previous test. I already know most, if not all, of the glue between
Line 318: Most speed
Line 319: • Easier to maintain
Line 320: • Easier to write
Line 321: • Faster feedback loop
Line 322: Most conﬁdence
Line 323: • Harder to maintain
Line 324: • Harder to write
Line 325: • Slower feedback loop
Line 326: Conﬁdence
Line 327: E2E/UI system tests
Line 328: E2E/UI isolated tests
Line 329: API tests (out of process)
Line 330: Integration tests (in memory)
Line 331: Component tests (in memory)
Line 332: Unit tests (in memory)
Line 333: Scenario
Line 334: 1
Line 335: Scenario
Line 336: 1.1
Line 337: Scenario
Line 338: 1.2
Line 339: Scenario
Line 340: 1.3
Line 341: Scenario
Line 342: 1.4
Line 343: Scenario
Line 344: 1.5
Line 345: Figure 10.2
Line 346: End-to-end-only test antipattern
Line 347: 
Line 348: --- 페이지 229 ---
Line 349: 201
Line 350: 10.2
Line 351: Test-level antipatterns
Line 352: layers works, from the first test. There’s no need to pay the tax of another E2E test if I
Line 353: can prove the next scenario at a lower level and pay a much smaller fee for pretty
Line 354: much the same bit of confidence.
Line 355: THE BUILD WHISPERER
Line 356: With E2E tests, not only do we have diminishing returns, we create a new bottleneck
Line 357: in the organization. Because high-level tests are often flaky, they break for many differ-
Line 358: ent reasons, some of which are not relevant to the test. You then need special people
Line 359: in the organization (usually QA leads) to sit down and analyze each of the many
Line 360: failing tests, and to hunt down the cause and determine if it’s actually a problem or a
Line 361: minor issue. 
Line 362:  I call these poor souls build whisperers. When the build is red, which it is most of the
Line 363: time, build whisperers are the ones who must come in, parse the data, and knowingly
Line 364: say, after hours of inspection, “Yes, it looks red, but it’s actually green.” 
Line 365:  Usually, the organization will drive build whisperers into a corner, demanding that
Line 366: they say the build is green because “We have to get this release out the door.” They are
Line 367: the gatekeepers of the release, and that is a thankless, stressful, and often manual and
Line 368: frustrating job. Whisperers usually burn out within a year or two, and they get chewed
Line 369: up and spit out into the next organization, where they do the same thankless job all
Line 370: over again. You’ll often see build whisperers when this antipattern of many high-level
Line 371: E2E tests exists. 
Line 372: AVOIDING BUILD WHISPERERS
Line 373: There is a way to resolve this mess, and that’s to create and cultivate robust, automated
Line 374: test pipelines that can automatically judge whether a build is green or not, even if you
Line 375: have flaky tests. Netflix has openly blogged about creating their own tool for measur-
Line 376: ing how a build is doing statistically in the wild, so that it can be automatically
Line 377: approved for full release deployment (http://mng.bz/BAA1). This is doable, but it
Line 378: takes time and culture to achieve such a pipeline. I write more about these types of
Line 379: pipelines in my blog at https://pipelinedriven.org. 
Line 380: A “THROW IT OVER THE WALL” MENTALITY
Line 381: Another reason having only E2E tests hurts organizations is that the people in charge
Line 382: of maintaining and monitoring these tests are people in the QA department. This
Line 383: means that the organization’s developers might not care about or even know the results
Line 384: of these builds, and they are not invested in fixing or caring for these tests. They don’t
Line 385: own them.
Line 386:  This “throw it over the wall” mentality can cause lots of miscommunication and
Line 387: quality issues because one part of the organization is not connected to the conse-
Line 388: quences of its actions, and the other side is suffering the consequences without being
Line 389: able to control the source of the issue. Is it any wonder that, in many organizations,
Line 390: developers and QA people don’t get along? The system around them is often
Line 391: designed to make them mortal enemies instead of collaborators. 
Line 392: 
Line 393: --- 페이지 230 ---
Line 394: 202
Line 395: CHAPTER 10
Line 396: Developing a testing strategy
Line 397: WHEN THIS ANTIPATTERN HAPPENS
Line 398: These are some reasons why I see this happen:
Line 399: Separation of duties—Separate QA and development departments with separate
Line 400: pipelines (automated build jobs and dashboards) exist in many organizations.
Line 401: When a QA department has its own pipeline, it is likely to write more tests of
Line 402: the same kind. Also, a QA department tends to write only a specific type of
Line 403: test—the ones they’re used to and are expected to write (sometimes based on
Line 404: company policy).
Line 405: An “if it works, don’t change it” mentality—A group might start with E2E tests and
Line 406: see that they like the results. They continue to add all their new tests in the
Line 407: same way, because it’s what they know, and it has proven to be useful. When the
Line 408: time it takes to run tests gets too long, it’s already too late to change direction
Line 409: (which relates to the next point).
Line 410: Sunk-costs fallacy—“We have lots of these types of tests, and if we changed them
Line 411: or replaced them with lower-level tests, it would mean we’ve wasted all that time
Line 412: and effort on tests that we are removing.” This is a fallacy, because maintaining,
Line 413: debugging, and understanding test failures costs a fortune in human time. If
Line 414: anything, it costs less to delete such tests (keeping only a few basic scenarios)
Line 415: and get that time back. 
Line 416: SHOULD YOU AVOID E2E TESTS COMPLETELY?
Line 417: No, we can’t avoid E2E tests. One of the good things they offer is confidence that the
Line 418: application works. It’s a completely different level of confidence compared to unit
Line 419: tests, because they test the integration of the full system, with all of its subsystems
Line 420: and components, from the point of view of a user. When they pass, the feeling you
Line 421: get is huge relief that the major scenarios you expect your users to encounter actu-
Line 422: ally work.
Line 423:  So don’t avoid them entirely. Instead, I highly recommend minimizing the number
Line 424: of E2E tests. We’ll talk about what that minimum is in section 10.3.3.
Line 425: 10.2.2 The low-level-only test antipattern
Line 426: The opposite of having only E2E tests is to have low-level tests only. Unit tests provide
Line 427: fast feedback, but they don’t provide the amount of confidence needed to fully trust
Line 428: that your application works as a single integrated unit (see figure 10.3). 
Line 429:  In this antipattern, the organization’s automated tests are mostly or exclusively low-
Line 430: level tests, such as unit tests or component tests. There may be hints of integration
Line 431: tests, but there are no E2E tests in sight.
Line 432:  The biggest issue with this is that the confidence level you get when these types of
Line 433: tests pass is simply not enough to feel confident that your application works. That
Line 434: means people will run the tests and then continue to do manual debugging and test-
Line 435: ing to get the final sense of confidence needed to release something. Unless what
Line 436: you’re shipping is a code library that’s meant to be used in the way your unit tests are
Line 437: 
Line 438: --- 페이지 231 ---
Line 439: 203
Line 440: 10.2
Line 441: Test-level antipatterns
Line 442: using it, this won’t be enough. Yes, the tests will run quickly, but you’ll still spend lots
Line 443: of time manually testing and verifying. 
Line 444:  This antipattern often happens when your developers are only used to writing low-
Line 445: level tests, if they don’t feel comfortable writing high-level tests, or if they expect the
Line 446: QA people to write those types of tests.
Line 447:  Does that mean you should avoid unit tests? Obviously not. But I highly recom-
Line 448: mend that you have not only unit tests but also higher-level tests. We’ll discuss this rec-
Line 449: ommendation in section 10.3. 
Line 450: Conﬁdence
Line 451: E2E/UI system tests
Line 452: E2E/UI isolated tests
Line 453: API tests (out of process)
Line 454: Integration tests (in memory)
Line 455: Component tests (in memory)
Line 456: Unit tests (in memory)
Line 457: Scenario
Line 458: 1
Line 459: Scenario
Line 460: 1.6
Line 461: Scenario
Line 462: 1.2
Line 463: Scenario
Line 464: 1.10
Line 465: Scenario
Line 466: 1.4
Line 467: Scenario
Line 468: 1.5
Line 469: Scenario
Line 470: 1.9
Line 471: Figure 10.3
Line 472: Low-level-only test antipattern
Line 473: 
Line 474: --- 페이지 232 ---
Line 475: 204
Line 476: CHAPTER 10
Line 477: Developing a testing strategy
Line 478: 10.2.3 Disconnected low-level and high-level tests
Line 479: This pattern might seem healthy at first, but it really isn’t. It might look a bit like fig-
Line 480: ure 10.4.
Line 481: Yes, you want to have both low-level tests (for speed) and high-level tests (for confi-
Line 482: dence). But when you see something like this in an organization, you will likely
Line 483: encounter one or more of these anti-behaviors:
Line 484: Many of the tests repeat in multiple levels.
Line 485: The people who write the low-level tests are not the same people who write the
Line 486: high-level tests. This means they don’t care about each other’s test results, and
Line 487: Most speed
Line 488: • Easier to maintain
Line 489: • Easier to write
Line 490: • Faster feedback loop
Line 491: Most conﬁdence
Line 492: • Harder to maintain
Line 493: • Harder to write
Line 494: • Slower feedback loop
Line 495: Conﬁdence
Line 496: E2E/UI system tests
Line 497: E2E/UI isolated tests
Line 498: API tests (out of process)
Line 499: Integration tests (in memory)
Line 500: Component tests (in memory)
Line 501: Unit tests (in memory)
Line 502: Scenario
Line 503: 1
Line 504: Scenario
Line 505: 1.1
Line 506: Scenario
Line 507: 1.2
Line 508: Scenario
Line 509: 1.3
Line 510: Scenario
Line 511: 1.4
Line 512: Scenario
Line 513: 1.5
Line 514: Scenario
Line 515: 1
Line 516: Scenario
Line 517: 1.6
Line 518: Scenario
Line 519: 1.2
Line 520: Scenario
Line 521: 1.10
Line 522: Scenario
Line 523: 1.4
Line 524: Scenario
Line 525: 1.5
Line 526: Scenario
Line 527: 1.9
Line 528: Figure 10.4
Line 529: Disconnected low-level and high-level tests
Line 530: 
Line 531: --- 페이지 233 ---
Line 532: 205
Line 533: 10.3
Line 534: Test recipes as a strategy
Line 535: they’ll likely have different pipelines execute the different test types. When one
Line 536: pipeline is red, the other group might not even know nor care that those tests
Line 537: are failing.
Line 538: We suffer the worst of both worlds: at the top level, we suffer from the long test
Line 539: times, difficult maintainability, build whisperers, and flakiness; at the bottom
Line 540: level, we suffer from lack of confidence. And because there is often a lack of
Line 541: communication, we don’t get the speed benefit of the low-level tests because
Line 542: they repeat at the top anyway. We also don’t get the top-level confidence
Line 543: because of how flaky such a large number of tests is. 
Line 544: This pattern often happens when we have separate test and a development organiza-
Line 545: tions with different goals and metrics, as well as different jobs and pipelines, permis-
Line 546: sions, and even code repositories. The larger the company, the more likely this is to
Line 547: happen. 
Line 548: 10.3
Line 549: Test recipes as a strategy
Line 550: My proposed strategy to achieve balance in the types of tests used by the organization
Line 551: is to use test recipes. The idea is to have an informal plan for how a particular feature is
Line 552: going to be tested. This plan should include not only the main scenario (also known
Line 553: as the happy path), but also all its significant variations (also known as edge cases), as
Line 554: shown in figure 10.5. A well-outlined test recipe gives a clear picture of what test level
Line 555: is appropriate for each scenario.
Line 556: 10.3.1 How to write a test recipe
Line 557: It’s best to have at least two people create a test recipe—hopefully one with a devel-
Line 558: oper’s point of view and one with a tester’s point of view. If there is no test depart-
Line 559: ment, two developers, or a developer with a senior developer will suffice. Mapping
Line 560: each scenario to a specific level in the test hierarchy can be a highly subjective task, so
Line 561: two pairs of eyes will help keep each other’s implicit assumptions in check.
Line 562:  The recipes themselves can be stored as extra text in a TODO list or as part of the
Line 563: feature story on the tracking board for the task. You don’t need a separate tool for
Line 564: planning tests. 
Line 565:  The best time to create a test recipe is just before you start working on the feature.
Line 566: This way, the test recipe becomes part of the definition of “done” for the feature,
Line 567: meaning the feature is not complete until the full test recipe is passing.
Line 568:  Of course, a recipe can change as time goes by. The team can add or remove sce-
Line 569: narios from it. A recipe is not a rigid artifact but a continuous work in progress, just
Line 570: like everything else in software development.
Line 571:  A test recipe represents the list of scenarios that will give its creators “pretty good
Line 572: confidence” that the feature works. As a rule of thumb, I like to have a 1 to 5 or 1 to 10
Line 573: ratio between levels of tests. For any high-level, E2E test, I might have 5 tests at a lower
Line 574: level. Or, if you think bottom-up, say you have 100 unit tests. You usually won’t need to
Line 575: have more than 10 integration tests and 1 E2E test. 
Line 576: 
Line 577: --- 페이지 234 ---
Line 578: 206
Line 579: CHAPTER 10
Line 580: Developing a testing strategy
Line 581: Don’t treat test recipes as something formal, though. A test recipe is not a binding
Line 582: commitment or a list of test cases in a test-planning piece of software. Don’t use it as a
Line 583: public report, a user story, or any other kind of promise to a stakeholder. At its core, a
Line 584: recipe is a simple list of 5 to 20 lines of text detailing simple scenarios to be tested in
Line 585: an automated fashion and at what level. The list can be changed, added to, or sub-
Line 586: tracted from. Consider it a comment. I usually like to just put it right in the user story
Line 587: or feature in Jira or whatever program I’m using.
Line 588:  Here’s an example of what one might look like:
Line 589: User profile feature testing recipe
Line 590: E2E – Login, go to profile screen, update email, log out, log in with new 
Line 591: email, verify profile screen updated
Line 592: API – Call UpdateProfile API with more complicated data
Line 593: Conﬁdence
Line 594: E2E/UI system tests
Line 595: E2E/UI isolated tests
Line 596: API tests (out of process)
Line 597: Integration tests (in memory)
Line 598: Component tests (in memory)
Line 599: Unit tests (in memory)
Line 600: Happy
Line 601: scenario
Line 602: 1
Line 603: Feature 1
Line 604: Feature 2
Line 605: Great ROI on this test
Line 606: Scenario
Line 607: variation
Line 608: 1.1
Line 609: Scenario
Line 610: variation
Line 611: 1.2
Line 612: Scenario
Line 613: variation
Line 614: 2.1
Line 615: Scenario
Line 616: variation
Line 617: 2.1.2
Line 618: Scenario
Line 619: variation
Line 620: 2.1.1
Line 621: Scenario
Line 622: variation
Line 623: 1.1.2
Line 624: Scenario
Line 625: variation
Line 626: 1.1.1
Line 627: Scenario
Line 628: variation
Line 629: 2.1.2
Line 630: Scenario
Line 631: variation
Line 632: 2.1.1
Line 633: Figure 10.5
Line 634: A test recipe is a test plan, outlining at which level a particular feature should be tested. 
Line 635: 
Line 636: --- 페이지 235 ---
Line 637: 207
Line 638: 10.3
Line 639: Test recipes as a strategy
Line 640: Unit test – Check profile update logic with bad email
Line 641: Unit test – Profile update logic with same email
Line 642: Unit test – Profile serialization/deserialization
Line 643: 10.3.2 When do I write and use a test recipe?
Line 644: Just before you start coding a feature or a user story, sit down with another person and
Line 645: try to come up with various scenarios to be tested. Discuss at which level that scenario
Line 646: should be best tested. This meeting will usually be no longer than 5 to 15 minutes,
Line 647: and after it, coding begins, including the writing of the tests. (If you’re doing TDD,
Line 648: you’ll start with the tests.)
Line 649:  In organizations where there are automation or QA roles, the developer will write
Line 650: the lower-level tests, and the QA will focus on writing the higher-level tests, while cod-
Line 651: ing of the feature is taking place. Both people are working at the same time. One does
Line 652: not wait for the other to finish their work before starting to write their tests.
Line 653:  If you are working with feature toggles, they should also be checked as part of the
Line 654: tests, so that if a feature is off, its tests will not run.
Line 655: 10.3.3 Rules for a test recipe
Line 656: There are several rules to follow when writing a test recipe:
Line 657: Faster—Prefer writing tests at lower levels, unless a high-level test is the only way
Line 658: for you to gain confidence that the feature works.
Line 659: Confidence—The recipe is done when you can tell yourself, “If all these tests
Line 660: passed, I’ll feel pretty good about this feature working.” If you can’t say that,
Line 661: write more scenarios that will allow you to say that.
Line 662: Revise—Feel free to add or remove tests from the list as you code. Just make
Line 663: sure you notify the other person you worked with on the recipe.
Line 664: Just in time—Write this recipe just before starting to code, when you know who
Line 665: is going to code it.
Line 666: Pair—Don’t write it alone if you can help it. People think in different ways, and
Line 667: it’s important to talk through the scenarios and learn from each other about
Line 668: testing ideas and mindset.
Line 669: Don’t repeat yourself from other features—If this scenario is already covered by an
Line 670: existing test (perhaps an E2E test from a previous feature), there is no need to
Line 671: repeat this scenario at that level.
Line 672: Don’t repeat yourself from other layers—Try not to repeat the same scenario at multi-
Line 673: ple levels. If you’re checking a successful login at the E2E level, lower-level tests
Line 674: should only check variations of that scenario (logging in with different provid-
Line 675: ers, unsuccessful login results, etc.). 
Line 676: More, faster—A good rule of thumb is to end up with a ratio of at least one to
Line 677: five between levels (for one E2E test, you might end up with five or more lower-
Line 678: level tests).
Line 679: 
Line 680: --- 페이지 236 ---
Line 681: 208
Line 682: CHAPTER 10
Line 683: Developing a testing strategy
Line 684: Pragmatic—Don’t feel the need to write tests at all levels for a given feature.
Line 685: Some features or user stories might only require unit tests. Others, only API or
Line 686: E2E tests. The basic idea is that, if all the scenarios in the recipe pass, you
Line 687: should feel confidence, regardless of what level they are tested at. If that’s not
Line 688: the case, move the scenarios around to different levels until you feel more con-
Line 689: fident, without sacrificing too much speed or maintenance burden.
Line 690: By following these rules, you’ll get the benefit of fast feedback, because most of your
Line 691: tests will be low level, while not sacrificing confidence because the few most important
Line 692: scenarios are still covered by high-level tests. The test recipe approach also allows you
Line 693: to avoid most of the repetition between tests by positioning scenario variations at lev-
Line 694: els lower than the main scenario. Finally, if QA people are involved in writing test rec-
Line 695: ipes too, you’ll form a new communication channel between people within your
Line 696: organization, which helps improve mutual understanding of your software project.
Line 697: 10.4
Line 698: Managing delivery pipelines
Line 699: What about performance tests? Security tests? Load tests? What about lots of other
Line 700: tests that might take ages to run? Where and when should we run them? Which layer
Line 701: are they? Should they be part of our automated pipeline?
Line 702:  Lots of organizations run those tests as part of the integration automated pipeline
Line 703: that runs for each release or pull request. However, this causes huge delays in feed-
Line 704: back, and the feedback is often “failed,” even though the failure is not essential for a
Line 705: release to go out for these types of tests.
Line 706:  We can divide these types of tests into two main groups:
Line 707: Delivery-blocking tests—These are tests that provide a go or no-go for the change
Line 708: that is about to be released and deployed. Unit, E2E, system, and security tests
Line 709: all fall into this category. Their feedback is binary: they either pass and
Line 710: announce that the change didn’t introduce any bugs, or they fail and indicate
Line 711: that the code needs to be fixed before it’s released.
Line 712: Good-to-know tests—These are tests created for the purpose of discovery and con-
Line 713: tinuous monitoring of key performance indicator (KPI) metrics. Examples
Line 714: include code analysis and complexity scanning, high-load performance testing,
Line 715: and other long-running nonfunctional tests that provide nonbinary feedback. If
Line 716: these tests fail, we might add new work items to our next sprints, but we would
Line 717: still be OK releasing our software.
Line 718: 10.4.1 Delivery vs. discovery pipelines
Line 719: We don’t want our good-to-know tests to take valuable feedback time from our deliv-
Line 720: ery process, so we’ll also have two types of pipelines:
Line 721: Delivery pipeline—Used for delivery-blocking tests. When the pipeline is green,
Line 722: we should be confident that we can automatically release the code to produc-
Line 723: tion. Tests in this pipeline should provide relatively fast feedback.
Line 724: 
Line 725: --- 페이지 237 ---
Line 726: 209
Line 727: 10.4
Line 728: Managing delivery pipelines
Line 729: Discovery pipeline—Used for good-to-know tests. This pipeline runs in parallel
Line 730: with the delivery pipeline, but continuously, and it’s not taken into account as a
Line 731: release criterion. Since there’s no need to wait for its feedback, tests in this
Line 732: pipeline can take a long time. If errors are found, they might become new work
Line 733: items in the next sprints for the team, but releases are not blocked.
Line 734: Figure 10.6 illustrates the features of these two kinds of pipelines.
Line 735: The point of the delivery pipeline is to provide a go/no-go check that also deploys our
Line 736: code if all seems green, perhaps even to production. The point of the discovery pipe-
Line 737: line is to provide refactoring objectives for the team, such as dealing with code com-
Line 738: plexity that has become too high. It can also show whether those refactoring efforts
Line 739: are effective over time. The discovery pipeline does not deploy anything except for
Line 740: the purpose of running specialized tests or analyzing code and its various KPI metrics.
Line 741: It ends with numbers on a dashboard. 
Line 742:  Speed is a big factor in getting teams to be more engaged, and splitting tests into
Line 743: discovery and delivery pipelines is yet another technique to keep in your arsenal.
Line 744: 10.4.2 Test layer parallelization
Line 745: Since fast feedback is very important, a common pattern you can and should employ
Line 746: in many scenarios is to run different test layers in parallel to speed up the pipeline
Line 747: Auto-triggered
Line 748: per commit in
Line 749: source control
Line 750: Auto-triggered
Line 751: continuously if
Line 752: there are changes
Line 753: Deploy and
Line 754: report statuses
Line 755: to dashboards
Line 756: Report KPIs
Line 757: to dashboards
Line 758: Build
Line 759: Unit tests
Line 760: API/E2E tests
Line 761: Security tests
Line 762: Lint
Line 763: Code quality
Line 764: Performance
Line 765: Load
Line 766: Delivery
Line 767: pipeline
Line 768: Discovery
Line 769: pipeline
Line 770: Figure 10.6
Line 771: Delivery vs. discovery pipelines
Line 772: 
Line 773: --- 페이지 238 ---
Line 774: 210
Line 775: CHAPTER 10
Line 776: Developing a testing strategy
Line 777: feedback, as shown in figure 10.7. You can even use parallel environments that are cre-
Line 778: ated dynamically and destroyed at the end of the test. 
Line 779: This approach benefits greatly from having access to dynamic environments. Throw-
Line 780: ing money at environments and automated parallel tests is almost always much more
Line 781: effective than throwing money at more people to do more manual tests, or simply
Line 782: having people wait longer to get feedback because the environment is being used
Line 783: right now.
Line 784:  Manual testing is unsustainable because such manual work only increases over
Line 785: time and becomes more and more frail and error prone. At the same time, simply
Line 786: waiting longer for pipeline feedback results in a huge waste of time for everyone. The
Line 787: waiting time, multiplied by the number of people waiting and the number of builds
Line 788: per day, results in a monthly investment that can be much larger than investing in
Line 789: dynamic environments and automation. Grab an Excel file and show your manager a
Line 790: simple formula to get that budget.
Line 791:  You can parallelize not only stages inside a pipeline; you can go further and run
Line 792: individual tests in parallel too. For example, if you’re stuck with a large number of
Line 793: Delivery
Line 794: pipeline
Line 795: (parallelized)
Line 796: Discovery
Line 797: pipeline
Line 798: (parallelized)
Line 799: Auto-triggered
Line 800: per commit in
Line 801: source control
Line 802: Auto-triggered
Line 803: continuously if
Line 804: there are
Line 805: changes
Line 806: Build
Line 807: Security tests
Line 808: Unit tests
Line 809: API/E2E tests
Line 810: Wait for all
Line 811: to ﬁnish
Line 812: Deploy
Line 813: Deploy and
Line 814: report statuses
Line 815: to dashboards
Line 816: Report KPIs
Line 817: to dashboards
Line 818: Wait for all
Line 819: to ﬁnish
Line 820: Auto-triggered
Line 821: continuously if
Line 822: there are changes
Line 823: Code quality
Line 824: Build
Line 825: Lint
Line 826: Performance
Line 827: Load
Line 828: Figure 10.7
Line 829: To speed up delivery, you can run pipelines, and even stages in pipelines, in parallel.
Line 830: 
Line 831: --- 페이지 239 ---
Line 832: 211
Line 833: Summary
Line 834: E2E tests, you can break them up into parallel test suites. That shaves a lot of time off
Line 835: your feedback loop.
Line 836: Summary
Line 837: There are multiple levels of tests: unit, component, and integration tests that
Line 838: run in memory; and API, isolated end-to-end (E2E), and system E2E tests that
Line 839: run out of process.
Line 840: Each test can be judged by five criteria: complexity, flakiness, confidence when
Line 841: it passes, maintainability, and execution speed.
Line 842: Unit and component tests are best in terms of maintainability, execution speed,
Line 843: and lack of complexity and flakiness, but they’re worst in terms of the confi-
Line 844: dence they provide. Integration and API tests are the middle ground in the
Line 845: trade-off between confidence and the other metrics. E2E tests take the opposite
Line 846: approach from unit tests: they provide the best confidence but at the expense
Line 847: of maintainability, speed, complexity, and flakiness.
Line 848: The end-to-end-only antipattern is when your build consists solely of E2E tests. The
Line 849: marginal value of each additional E2E test is low, while the maintenance costs
Line 850: of all tests are the same. You’ll get the most return on your efforts if you have
Line 851: just a few E2E tests covering the most important functionality.
Line 852: The low-level-only antipattern is when your build consists solely of unit and compo-
Line 853: nent tests. Lower-level tests can’t provide enough confidence that your function-
Line 854: ality as a whole works, and they must be supplemented with higher-level tests.
Line 855: Disconnected low-level and high-level tests is an antipattern because it’s a strong sign
Line 856: that your tests are written by two groups of people who don’t communicate
Line 857: with each other. Such tests often duplicate each other and carry high mainte-
Line 858: nance costs.
Line 859: Don’t do nightly builds
Line 860: It’s best to run your delivery pipeline after every code commit, instead of at a certain
Line 861: time. Running tests with each code change gives you more granular and faster feed-
Line 862: back than the crude nightly build that simply accumulates all changes from the pre-
Line 863: vious day. But if, for some reason, you absolutely have to run your pipeline on a timely
Line 864: basis, at least run them continuously instead of once a day.
Line 865: If your delivery pipeline build takes a long time, don’t wait for a magical trigger or
Line 866: schedule to run it. Imagine, as a developer, needing to wait until tomorrow to know
Line 867: if you broke something. With tests running continuously, you would still need to wait,
Line 868: but at least it would only be a couple of hours instead of a full day. Isn’t that more
Line 869: productive?
Line 870: Also, don’t just run the build on demand. The feedback loop will be faster if you run
Line 871: the build automatically as soon as the previous one finishes, assuming there are
Line 872: code changes since the previous build, of course.
Line 873: 
Line 874: --- 페이지 240 ---
Line 875: 212
Line 876: CHAPTER 10
Line 877: Developing a testing strategy
Line 878: A test recipe is a simple list of 5 to 20 lines of text, detailing which simple scenar-
Line 879: ios should be tested in an automated fashion and at what level. A test recipe
Line 880: should give you confidence that, if all outlined tests pass, the feature works
Line 881: as intended.
Line 882: Split your build pipeline into delivery and discovery pipelines. The delivery pipe-
Line 883: line should be used for delivery-blocking tests, which, if they fail, stop delivery
Line 884: of the code under test. The discovery pipeline is used for good-to-know tests
Line 885: and runs in parallel with the delivery pipeline.
Line 886: You can parallelize not just pipelines but also stages inside those pipelines, and
Line 887: even groups of tests inside stages too.
