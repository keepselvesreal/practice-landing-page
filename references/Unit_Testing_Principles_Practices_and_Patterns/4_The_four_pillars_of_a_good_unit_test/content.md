Line 1: 
Line 2: --- 페이지 89 ---
Line 3: 67
Line 4: The four pillars
Line 5: of a good unit test
Line 6: Now we are getting to the heart of the matter. In chapter 1, you saw the properties
Line 7: of a good unit test suite:
Line 8: It is integrated into the development cycle. You only get value from tests that you
Line 9: actively use; there’s no point in writing them otherwise.
Line 10: It targets only the most important parts of your code base. Not all production code
Line 11: deserves equal attention. It’s important to differentiate the heart of the
Line 12: application (its domain model) from everything else. This topic is tackled in
Line 13: chapter 7.
Line 14: It provides maximum value with minimum maintenance costs. To achieve this last
Line 15: attribute, you need to be able to
Line 16: – Recognize a valuable test (and, by extension, a test of low value)
Line 17: – Write a valuable test
Line 18: This chapter covers
Line 19: Exploring dichotomies between aspects of a 
Line 20: good unit test
Line 21: Defining an ideal test
Line 22: Understanding the Test Pyramid
Line 23: Using black-box and white-box testing
Line 24: 
Line 25: --- 페이지 90 ---
Line 26: 68
Line 27: CHAPTER 4
Line 28: The four pillars of a good unit test
Line 29: As we discussed in chapter 1, recognizing a valuable test and writing a valuable test are two
Line 30: separate skills. The latter skill requires the former one, though; so, in this chapter, I’ll
Line 31: show how to recognize a valuable test. You’ll see a universal frame of reference with
Line 32: which you can analyze any test in the suite. We’ll then use this frame of reference to
Line 33: go over some popular unit testing concepts: the Test Pyramid and black-box versus
Line 34: white-box testing.
Line 35:  Buckle up: we are starting out.
Line 36: 4.1
Line 37: Diving into the four pillars of a good unit test
Line 38: A good unit test has the following four attributes:
Line 39: Protection against regressions
Line 40: Resistance to refactoring
Line 41: Fast feedback
Line 42: Maintainability
Line 43: These four attributes are foundational. You can use them to analyze any automated
Line 44: test, be it unit, integration, or end-to-end. Every such test exhibits some degree of
Line 45: each attribute. In this section, I define the first two attributes; and in section 4.2, I
Line 46: describe the intrinsic connection between them.
Line 47: 4.1.1
Line 48: The first pillar: Protection against regressions
Line 49: Let’s start with the first attribute of a good unit test: protection against regressions. As you
Line 50: know from chapter 1, a regression is a software bug. It’s when a feature stops working as
Line 51: intended after some code modification, usually after you roll out new functionality.
Line 52:  Such regressions are annoying (to say the least), but that’s not the worst part about
Line 53: them. The worst part is that the more features you develop, the more chances there are
Line 54: that you’ll break one of those features with a new release. An unfortunate fact of pro-
Line 55: gramming life is that code is not an asset, it’s a liability. The larger the code base, the more
Line 56: exposure it has to potential bugs. That’s why it’s crucial to develop a good protection
Line 57: against regressions. Without such protection, you won’t be able to sustain the project
Line 58: growth in a long run—you’ll be buried under an ever-increasing number of bugs.
Line 59:  To evaluate how well a test scores on the metric of protecting against regressions,
Line 60: you need to take into account the following:
Line 61: The amount of code that is executed during the test
Line 62: The complexity of that code
Line 63: The code’s domain significance
Line 64: Generally, the larger the amount of code that gets executed, the higher the chance
Line 65: that the test will reveal a regression. Of course, assuming that this test has a relevant
Line 66: set of assertions, you don’t want to merely execute the code. While it helps to know
Line 67: that this code runs without throwing exceptions, you also need to validate the out-
Line 68: come it produces.
Line 69: 
Line 70: --- 페이지 91 ---
Line 71: 69
Line 72: Diving into the four pillars of a good unit test
Line 73:  Note that it’s not only the amount of code that matters, but also its complexity and
Line 74: domain significance. Code that represents complex business logic is more important
Line 75: than boilerplate code—bugs in business-critical functionality are the most damaging.
Line 76:  On the other hand, it’s rarely worthwhile to test trivial code. Such code is short and
Line 77: doesn’t contain a substantial amount of business logic. Tests that cover trivial code
Line 78: don’t have much of a chance of finding a regression error, because there’s not a lot of
Line 79: room for a mistake. An example of trivial code is a single-line property like this:
Line 80: public class User
Line 81: {
Line 82: public string Name { get; set; }
Line 83: }
Line 84: Furthermore, in addition to your code, the code you didn’t write also counts: for
Line 85: example, libraries, frameworks, and any external systems used in the project. That
Line 86: code influences the working of your software almost as much as your own code. For
Line 87: the best protection, the test must include those libraries, frameworks, and external sys-
Line 88: tems in the testing scope, in order to check that the assumptions your software makes
Line 89: about these dependencies are correct.
Line 90: TIP
Line 91: To maximize the metric of protection against regressions, the test needs
Line 92: to aim at exercising as much code as possible. 
Line 93: 4.1.2
Line 94: The second pillar: Resistance to refactoring
Line 95: The second attribute of a good unit test is resistance to refactoring—the degree to which
Line 96: a test can sustain a refactoring of the underlying application code without turning red
Line 97: (failing).
Line 98: DEFINITION
Line 99: Refactoring means changing existing code without modifying its
Line 100: observable behavior. The intention is usually to improve the code’s nonfunc-
Line 101: tional characteristics: increase readability and reduce complexity. Some exam-
Line 102: ples of refactoring are renaming a method and extracting a piece of code into
Line 103: a new class.
Line 104: Picture this situation. You developed a new feature, and everything works great. The
Line 105: feature itself is doing its job, and all the tests are passing. Now you decide to clean up
Line 106: the code. You do some refactoring here, a little bit of modification there, and every-
Line 107: thing looks even better than before. Except one thing—the tests are failing. You look
Line 108: more closely to see exactly what you broke with the refactoring, but it turns out that
Line 109: you didn’t break anything. The feature works perfectly, just as before. The problem is
Line 110: that the tests are written in such a way that they turn red with any modification of the
Line 111: underlying code. And they do that regardless of whether you actually break the func-
Line 112: tionality itself.
Line 113:  This situation is called a false positive. A false positive is a false alarm. It’s a result
Line 114: indicating that the test fails, although in reality, the functionality it covers works as
Line 115: 
Line 116: --- 페이지 92 ---
Line 117: 70
Line 118: CHAPTER 4
Line 119: The four pillars of a good unit test
Line 120: intended. Such false positives usually take place when you refactor the code—when
Line 121: you modify the implementation but keep the observable behavior intact. Hence the
Line 122: name for this attribute of a good unit test: resistance to refactoring.
Line 123:  To evaluate how well a test scores on the metric of resisting to refactoring, you
Line 124: need to look at how many false positives the test generates. The fewer, the better.
Line 125:  Why so much attention on false positives? Because they can have a devastating
Line 126: effect on your entire test suite. As you may recall from chapter 1, the goal of unit test-
Line 127: ing is to enable sustainable project growth. The mechanism by which the tests enable
Line 128: sustainable growth is that they allow you to add new features and conduct regular
Line 129: refactorings without introducing regressions. There are two specific benefits here:
Line 130: Tests provide an early warning when you break existing functionality. Thanks to such
Line 131: early warnings, you can fix an issue long before the faulty code is deployed to
Line 132: production, where dealing with it would require a significantly larger amount
Line 133: of effort.
Line 134: You become confident that your code changes won’t lead to regressions. Without such
Line 135: confidence, you will be much more hesitant to refactor and much more likely
Line 136: to leave the code base to deteriorate.
Line 137: False positives interfere with both of these benefits:
Line 138: If tests fail with no good reason, they dilute your ability and willingness to react
Line 139: to problems in code. Over time, you get accustomed to such failures and stop
Line 140: paying as much attention. After a while, you start ignoring legitimate failures,
Line 141: too, allowing them to slip into production.
Line 142: On the other hand, when false positives are frequent, you slowly lose trust in the
Line 143: test suite. You no longer perceive it as a reliable safety net—the perception is
Line 144: diminished by false alarms. This lack of trust leads to fewer refactorings,
Line 145: because you try to reduce code changes to a minimum in order to avoid regres-
Line 146: sions.
Line 147: A story from the trenches
Line 148: I once worked on a project with a rich history. The project wasn’t too old, maybe two
Line 149: or three years; but during that period of time, management significantly shifted the
Line 150: direction they wanted to go with the project, and development changed direction
Line 151: accordingly. During this change, a problem emerged: the code base accumulated
Line 152: large chunks of leftover code that no one dared to delete or refactor. The company
Line 153: no longer needed the features that code provided, but some parts of it were used in
Line 154: new functionality, so it was impossible to get rid of the old code completely.
Line 155: The project had good test coverage. But every time someone tried to refactor the old
Line 156: features and separate the bits that were still in use from everything else, the tests
Line 157: failed. And not just the old tests—they had been disabled long ago—but the new
Line 158: tests, too. Some of the failures were legitimate, but most were not—they were false
Line 159: positives.
Line 160: 
Line 161: --- 페이지 93 ---
Line 162: 71
Line 163: Diving into the four pillars of a good unit test
Line 164: This story is typical of most projects with brittle tests. First, developers take test failures
Line 165: at face value and deal with them accordingly. After a while, people get tired of tests
Line 166: crying “wolf” all the time and start to ignore them more and more. Eventually, there
Line 167: comes a moment when a bunch of real bugs are released to production because devel-
Line 168: opers ignored the failures along with all the false positives.
Line 169:  You don’t want to react to such a situation by ceasing all refactorings, though. The
Line 170: correct response is to re-evaluate the test suite and start reducing its brittleness. I
Line 171: cover this topic in chapter 7. 
Line 172: 4.1.3
Line 173: What causes false positives?
Line 174: So, what causes false positives? And how can you avoid them?
Line 175:  The number of false positives a test produces is directly related to the way the test
Line 176: is structured. The more the test is coupled to the implementation details of the system
Line 177: under test (SUT), the more false alarms it generates. The only way to reduce the
Line 178: chance of getting a false positive is to decouple the test from those implementation
Line 179: details. You need to make sure the test verifies the end result the SUT delivers: its
Line 180: observable behavior, not the steps it takes to do that. Tests should approach SUT veri-
Line 181: fication from the end user’s point of view and check only the outcome meaningful to
Line 182: that end user. Everything else must be disregarded (more on this topic in chapter 5).
Line 183:  The best way to structure a test is to make it tell a story about the problem domain.
Line 184: Should such a test fail, that failure would mean there’s a disconnect between the story
Line 185: and the actual application behavior. It’s the only type of test failure that benefits you—
Line 186: such failures are always on point and help you quickly understand what went wrong.
Line 187: All other failures are just noise that steer your attention away from things that matter.
Line 188:  Take a look at the following example. In it, the MessageRenderer class generates
Line 189: an HTML representation of a message containing a header, a body, and a footer.
Line 190: public class Message
Line 191: {
Line 192: public string Header { get; set; }
Line 193: public string Body { get; set; }
Line 194: public string Footer { get; set; }
Line 195: }
Line 196: At first, the developers tried to deal with the test failures. However, since the vast
Line 197: majority of them were false alarms, the situation got to the point where the develop-
Line 198: ers ignored such failures and disabled the failing tests. The prevailing attitude was,
Line 199: “If it’s because of that old chunk of code, just disable the test; we’ll look at it later.”
Line 200: Everything worked fine for a while—until a major bug slipped into production. One of
Line 201: the tests correctly identified the bug, but no one listened; the test was disabled along
Line 202: with all the others. After that accident, the developers stopped touching the old code
Line 203: entirely.
Line 204: Listing 4.1
Line 205: Generating an HTML representation of a message
Line 206: 
Line 207: --- 페이지 94 ---
Line 208: 72
Line 209: CHAPTER 4
Line 210: The four pillars of a good unit test
Line 211: public interface IRenderer
Line 212: {
Line 213: string Render(Message message);
Line 214: }
Line 215: public class MessageRenderer : IRenderer
Line 216: {
Line 217: public IReadOnlyList<IRenderer> SubRenderers { get; }
Line 218: public MessageRenderer()
Line 219: {
Line 220: SubRenderers = new List<IRenderer>
Line 221: {
Line 222: new HeaderRenderer(),
Line 223: new BodyRenderer(),
Line 224: new FooterRenderer()
Line 225: };
Line 226: }
Line 227: public string Render(Message message)
Line 228: {
Line 229: return SubRenderers
Line 230: .Select(x => x.Render(message))
Line 231: .Aggregate("", (str1, str2) => str1 + str2);
Line 232: }
Line 233: }
Line 234: The MessageRenderer class contains several sub-renderers to which it delegates the
Line 235: actual work on parts of the message. It then combines the result into an HTML docu-
Line 236: ment. The sub-renderers orchestrate the raw text with HTML tags. For example:
Line 237: public class BodyRenderer : IRenderer
Line 238: {
Line 239: public string Render(Message message)
Line 240: {
Line 241: return $"<b>{message.Body}</b>";
Line 242: }
Line 243: }
Line 244: How can MessageRenderer be tested? One possible approach is to analyze the algo-
Line 245: rithm this class follows.
Line 246: [Fact]
Line 247: public void MessageRenderer_uses_correct_sub_renderers()
Line 248: {
Line 249: var sut = new MessageRenderer();
Line 250: IReadOnlyList<IRenderer> renderers = sut.SubRenderers;
Line 251: Listing 4.2
Line 252: Verifying that MessageRenderer has the correct structure
Line 253: 
Line 254: --- 페이지 95 ---
Line 255: 73
Line 256: Diving into the four pillars of a good unit test
Line 257: Assert.Equal(3, renderers.Count);
Line 258: Assert.IsAssignableFrom<HeaderRenderer>(renderers[0]);
Line 259: Assert.IsAssignableFrom<BodyRenderer>(renderers[1]);
Line 260: Assert.IsAssignableFrom<FooterRenderer>(renderers[2]);
Line 261: }
Line 262: This test checks to see if the sub-renderers are all of the expected types and appear in
Line 263: the correct order, which presumes that the way MessageRenderer processes messages
Line 264: must also be correct. The test might look good at first, but does it really verify Message-
Line 265: Renderer’s observable behavior? What if you rearrange the sub-renderers, or replace
Line 266: one of them with a new one? Will that lead to a bug?
Line 267:  Not necessarily. You could change a sub-renderer’s composition in such a way that
Line 268: the resulting HTML document remains the same. For example, you could replace
Line 269: BodyRenderer with a BoldRenderer, which does the same job as BodyRenderer. Or you
Line 270: could get rid of all the sub-renderers and implement the rendering directly in Message-
Line 271: Renderer.
Line 272:  Still, the test will turn red if you do any of that, even though the end result won’t
Line 273: change. That’s because the test couples to the SUT’s implementation details and not
Line 274: the outcome the SUT produces. This test inspects the algorithm and expects to see
Line 275: one particular implementation, without any consideration for equally applicable alter-
Line 276: native implementations (see figure 4.1).
Line 277: Any substantial refactoring of the MessageRenderer class would lead to a test failure.
Line 278: Mind you, the process of refactoring is changing the implementation without affecting
Line 279: the application’s observable behavior. And it’s precisely because the test is concerned
Line 280: with the implementation details that it turns red every time you change those details.
Line 281: Step 1
Line 282: Step 2
Line 283: Step 3
Line 284: Client
Line 285: System under test
Line 286: Test: “Are
Line 287: these steps
Line 288: correct?”
Line 289: Figure 4.1
Line 290: A test that couples to the SUT’s algorithm. Such a test expects to see one particular 
Line 291: implementation (the specific steps the SUT must take to deliver the result) and therefore is 
Line 292: brittle. Any refactoring of the SUT’s implementation would lead to a test failure.
Line 293: 
Line 294: --- 페이지 96 ---
Line 295: 74
Line 296: CHAPTER 4
Line 297: The four pillars of a good unit test
Line 298: Therefore, tests that couple to the SUT’s implementation details are not resistant to refactoring.
Line 299: Such tests exhibit all the shortcomings I described previously:
Line 300: They don’t provide an early warning in the event of regressions—you simply
Line 301: ignore those warnings due to little relevance.
Line 302: They hinder your ability and willingness to refactor. It’s no wonder—who would
Line 303: like to refactor, knowing that the tests can’t tell which way is up when it comes
Line 304: to finding bugs?
Line 305: The next listing shows the most egregious example of brittleness in tests that I’ve ever
Line 306: encountered, in which the test reads the source code of the MessageRenderer class
Line 307: and compares it to the “correct” implementation.
Line 308: [Fact]
Line 309: public void MessageRenderer_is_implemented_correctly()
Line 310: {
Line 311: string sourceCode = File.ReadAllText(@"[path]\MessageRenderer.cs");
Line 312: Assert.Equal(@"
Line 313: public class MessageRenderer : IRenderer
Line 314: {
Line 315: public IReadOnlyList<<IRenderer> SubRenderers { get; }
Line 316: public MessageRenderer()
Line 317: {
Line 318: SubRenderers = new List<<IRenderer>
Line 319: {
Line 320: new HeaderRenderer(),
Line 321: new BodyRenderer(),
Line 322: new FooterRenderer()
Line 323: };
Line 324: }
Line 325: public string Render(Message message) { /* ... */ }
Line 326: }", sourceCode);
Line 327: }
Line 328: Of course, this test is just plain ridiculous; it will fail should you modify even the slight-
Line 329: est detail in the MessageRenderer class. At the same time, it’s not that different from
Line 330: the test I brought up earlier. Both insist on a particular implementation without tak-
Line 331: ing into consideration the SUT’s observable behavior. And both will turn red each
Line 332: time you change that implementation. Admittedly, though, the test in listing 4.3 will
Line 333: break more often than the one in listing 4.2. 
Line 334: 4.1.4
Line 335: Aim at the end result instead of implementation details
Line 336: As I mentioned earlier, the only way to avoid brittleness in tests and increase their resis-
Line 337: tance to refactoring is to decouple them from the SUT’s implementation details—keep
Line 338: as much distance as possible between the test and the code’s inner workings, and
Line 339: Listing 4.3
Line 340: Verifying the source code of the MessageRenderer class
Line 341: 
Line 342: --- 페이지 97 ---
Line 343: 75
Line 344: Diving into the four pillars of a good unit test
Line 345: instead aim at verifying the end result. Let’s do that: let’s refactor the test from list-
Line 346: ing 4.2 into something much less brittle.
Line 347:  To start off, you need to ask yourself the following question: What is the final out-
Line 348: come you get from MessageRenderer? Well, it’s the HTML representation of a mes-
Line 349: sage. And it’s the only thing that makes sense to check, since it’s the only observable
Line 350: result you get out of the class. As long as this HTML representation stays the same,
Line 351: there’s no need to worry about exactly how it’s generated. Such implementation
Line 352: details are irrelevant. The following code is the new version of the test.
Line 353: [Fact]
Line 354: public void Rendering_a_message()
Line 355: {
Line 356: var sut = new MessageRenderer();
Line 357: var message = new Message
Line 358: {
Line 359: Header = "h",
Line 360: Body = "b",
Line 361: Footer = "f"
Line 362: };
Line 363: string html = sut.Render(message);
Line 364: Assert.Equal("<h1>h</h1><b>b</b><i>f</i>", html);
Line 365: }
Line 366: This test treats MessageRenderer as a black box and is only interested in its observable
Line 367: behavior. As a result, the test is much more resistant to refactoring—it doesn’t care
Line 368: what changes you make to the SUT as long as the HTML output remains the same
Line 369: (figure 4.2).
Line 370:  Notice the profound improvement in this test over the original version. It aligns
Line 371: itself with the business needs by verifying the only outcome meaningful to end users—
Line 372: Listing 4.4
Line 373: Verifying the outcome that MessageRenderer produces
Line 374: Step 1
Line 375: Step 2
Line 376: Step 3
Line 377: Client
Line 378: System under test
Line 379: Good test: “Is
Line 380: the end result
Line 381: correct?”
Line 382: Step 1
Line 383: Step 2
Line 384: Step 3
Line 385: Client
Line 386: System under test
Line 387: Bad test: “Are
Line 388: these steps
Line 389: correct?”
Line 390: Figure 4.2
Line 391: The test on the left couples to the SUT’s observable behavior as opposed to implementation 
Line 392: details. Such a test is resistant to refactoring—it will trigger few, if any, false positives.
Line 393: 
Line 394: --- 페이지 98 ---
Line 395: 76
Line 396: CHAPTER 4
Line 397: The four pillars of a good unit test
Line 398: how a message is displayed in the browser. Failures of such a test are always on point:
Line 399: they communicate a change in the application behavior that can affect the customer
Line 400: and thus should be brought to the developer’s attention. This test will produce few, if
Line 401: any, false positives.
Line 402:  Why few and not none at all? Because there could still be changes in Message-
Line 403: Renderer that would break the test. For example, you could introduce a new parame-
Line 404: ter in the Render() method, causing a compilation error. And technically, such an
Line 405: error counts as a false positive, too. After all, the test isn’t failing because of a change
Line 406: in the application’s behavior.
Line 407:  But this kind of false positive is easy to fix. Just follow the compiler and add a new
Line 408: parameter to all tests that invoke the Render() method. The worse false positives are
Line 409: those that don’t lead to compilation errors. Such false positives are the hardest to deal
Line 410: with—they seem as though they point to a legitimate bug and require much more
Line 411: time to investigate.
Line 412: 4.2
Line 413: The intrinsic connection between the first 
Line 414: two attributes
Line 415: As I mentioned earlier, there’s an intrinsic connection between the first two pillars of
Line 416: a good unit test—protection against regressions and resistance to refactoring. They both con-
Line 417: tribute to the accuracy of the test suite, though from opposite perspectives. These two
Line 418: attributes also tend to influence the project differently over time: while it’s important
Line 419: to have good protection against regressions very soon after the project’s initiation, the
Line 420: need for resistance to refactoring is not immediate.
Line 421:  In this section, I talk about
Line 422: Maximizing test accuracy
Line 423: The importance of false positives and false negatives
Line 424: 4.2.1
Line 425: Maximizing test accuracy
Line 426: Let’s step back for a second and look at the broader picture with regard to test results.
Line 427: When it comes to code correctness and test results, there are four possible outcomes,
Line 428: as shown in figure 4.3. The test can either pass or fail (the rows of the table). And the
Line 429: functionality itself can be either correct or broken (the table’s columns).
Line 430:  The situation when the test passes and the underlying functionality works as
Line 431: intended is a correct inference: the test correctly inferred the state of the system (there
Line 432: are no bugs in it). Another term for this combination of working functionality and a
Line 433: passing test is true negative.
Line 434:  Similarly, when the functionality is broken and the test fails, it’s also a correct infer-
Line 435: ence. That’s because you expect to see the test fail when the functionality is not work-
Line 436: ing properly. That’s the whole point of unit testing. The corresponding term for this
Line 437: situation is true positive.
Line 438:  But when the test doesn’t catch an error, that’s a problem. This is the upper-right
Line 439: quadrant, a false negative. And this is what the first attribute of a good test—protection
Line 440: 
Line 441: --- 페이지 99 ---
Line 442: 77
Line 443: The intrinsic connection between the first two attributes
Line 444: against regressions—helps you avoid. Tests with a good protection against regressions
Line 445: help you to minimize the number of false negatives—type II errors.
Line 446:  On the other hand, there’s a symmetric situation when the functionality is correct
Line 447: but the test still shows a failure. This is a false positive, a false alarm. And this is what the
Line 448: second attribute—resistance to refactoring—helps you with.
Line 449:  All these terms (false positive, type I error and so on) have roots in statistics, but can
Line 450: also be applied to analyzing a test suite. The best way to wrap your head around them
Line 451: is to think of a flu test. A flu test is positive when the person taking the test has the flu.
Line 452: The term positive is a bit confusing because there’s nothing positive about having the
Line 453: flu. But the test doesn’t evaluate the situation as a whole. In the context of testing,
Line 454: positive means that some set of conditions is now true. Those are the conditions the
Line 455: creators of the test have set it to react to. In this particular example, it’s the presence
Line 456: of the flu. Conversely, the lack of flu renders the flu test negative.
Line 457:  Now, when you evaluate how accurate the flu test is, you bring up terms such as
Line 458: false positive or false negative. The probability of false positives and false negatives tells
Line 459: you how good the flu test is: the lower that probability, the more accurate the test.
Line 460:  This accuracy is what the first two pillars of a good unit test are all about. Protection
Line 461: against regressions and resistance to refactoring aim at maximizing the accuracy of the test
Line 462: suite. The accuracy metric itself consists of two components:
Line 463: How good the test is at indicating the presence of bugs (lack of false negatives,
Line 464: the sphere of protection against regressions)
Line 465: How good the test is at indicating the absence of bugs (lack of false positives,
Line 466: the sphere of resistance to refactoring)
Line 467: Another way to think of false positives and false negatives is in terms of signal-to-noise
Line 468: ratio. As you can see from the formula in figure 4.4, there are two ways to improve test
Line 469: Table of error types
Line 470: Type II error
Line 471: (false negative)
Line 472: Correct inference
Line 473: (true positives)
Line 474: Type I error
Line 475: (false positive)
Line 476: Correct inference
Line 477: (true negatives)
Line 478: Resistance to
Line 479: refactoring
Line 480: Test
Line 481: result
Line 482: Test fails
Line 483: Test passes
Line 484: Correct
Line 485: Functionality is
Line 486: Broken
Line 487: Protection
Line 488: against
Line 489: regressions
Line 490: Figure 4.3
Line 491: The relationship between protection against regressions and resistance to 
Line 492: refactoring. Protection against regressions guards against false negatives (type II errors). 
Line 493: Resistance to refactoring minimizes the number of false positives (type I errors).
Line 494: 
Line 495: --- 페이지 100 ---
Line 496: 78
Line 497: CHAPTER 4
Line 498: The four pillars of a good unit test
Line 499: accuracy. The first is to increase the numerator, signal: that is, make the test better at
Line 500: finding regressions. The second is to reduce the denominator, noise: make the test bet-
Line 501: ter at not raising false alarms.
Line 502:  Both are critically important. There’s no use for a test that isn’t capable of finding
Line 503: any bugs, even if it doesn’t raise false alarms. Similarly, the test’s accuracy goes to zero
Line 504: when it generates a lot of noise, even if it’s capable of finding all the bugs in code.
Line 505: These findings are simply lost in the sea of irrelevant information. 
Line 506: 4.2.2
Line 507: The importance of false positives and false negatives: 
Line 508: The dynamics
Line 509: In the short term, false positives are not as bad as false negatives. In the beginning of a
Line 510: project, receiving a wrong warning is not that big a deal as opposed to not being
Line 511: warned at all and running the risk of a bug slipping into production. But as the proj-
Line 512: ect grows, false positives start to have an increasingly large effect on the test suite
Line 513: (figure 4.5).
Line 514: Test accuracy =
Line 515: Noise (number of false alarms raised)
Line 516: Signal (number of bugs found)
Line 517: Figure 4.4
Line 518: A test is accurate insofar as it generates a 
Line 519: strong signal (is capable of finding bugs) with as little 
Line 520: noise (false alarms) as possible.
Line 521: Eﬀect on the
Line 522: test suite
Line 523: Project duration
Line 524: False negatives
Line 525: False positives
Line 526: Figure 4.5
Line 527: False positives (false alarms) don’t have as much of a 
Line 528: negative effect in the beginning. But they become increasingly 
Line 529: important as the project grows—as important as false negatives 
Line 530: (unnoticed bugs).
Line 531: 
Line 532: --- 페이지 101 ---
Line 533: 79
Line 534: The third and fourth pillars: Fast feedback and maintainability
Line 535: Why are false positives not as important initially? Because the importance of refactor-
Line 536: ing is also not immediate; it increases gradually over time. You don’t need to conduct
Line 537: many code clean-ups in the beginning of the project. Newly written code is often shiny
Line 538: and flawless. It’s also still fresh in your memory, so you can easily refactor it even if
Line 539: tests raise false alarms.
Line 540:  But as time goes on, the code base deteriorates. It becomes increasingly complex
Line 541: and disorganized. Thus you have to start conducting regular refactorings in order to
Line 542: mitigate this tendency. Otherwise, the cost of introducing new features eventually
Line 543: becomes prohibitive.
Line 544:  As the need for refactoring increases, the importance of resistance to refactoring in
Line 545: tests increases with it. As I explained earlier, you can’t refactor when the tests keep cry-
Line 546: ing “wolf” and you keep getting warnings about bugs that don’t exist. You quickly lose
Line 547: trust in such tests and stop viewing them as a reliable source of feedback.
Line 548:  Despite the importance of protecting your code against false positives, especially in
Line 549: the later project stages, few developers perceive false positives this way. Most people
Line 550: tend to focus solely on improving the first attribute of a good unit test—protection
Line 551: against regressions, which is not enough to build a valuable, highly accurate test suite
Line 552: that helps sustain project growth.
Line 553:  The reason, of course, is that far fewer projects get to those later stages, mostly
Line 554: because they are small and the development finishes before the project becomes too
Line 555: big. Thus developers face the problem of unnoticed bugs more often than false
Line 556: alarms that swarm the project and hinder all refactoring undertakings. And so, people
Line 557: optimize accordingly. Nevertheless, if you work on a medium to large project, you
Line 558: have to pay equal attention to both false negatives (unnoticed bugs) and false posi-
Line 559: tives (false alarms). 
Line 560: 4.3
Line 561: The third and fourth pillars: Fast feedback 
Line 562: and maintainability
Line 563: In this section, I talk about the two remaining pillars of a good unit test:
Line 564: Fast feedback
Line 565: Maintainability
Line 566: As you may remember from chapter 2, fast feedback is an essential property of a unit
Line 567: test. The faster the tests, the more of them you can have in the suite and the more
Line 568: often you can run them.
Line 569:  With tests that run quickly, you can drastically shorten the feedback loop, to the
Line 570: point where the tests begin to warn you about bugs as soon as you break the code, thus
Line 571: reducing the cost of fixing those bugs almost to zero. On the other hand, slow tests
Line 572: delay the feedback and potentially prolong the period during which the bugs remain
Line 573: unnoticed, thus increasing the cost of fixing them. That’s because slow tests discour-
Line 574: age you from running them often, and therefore lead to wasting more time moving in
Line 575: a wrong direction.
Line 576: 
Line 577: --- 페이지 102 ---
Line 578: 80
Line 579: CHAPTER 4
Line 580: The four pillars of a good unit test
Line 581:  Finally, the fourth pillar of good units tests, the maintainability metric, evaluates
Line 582: maintenance costs. This metric consists of two major components:
Line 583: How hard it is to understand the test—This component is related to the size of the
Line 584: test. The fewer lines of code in the test, the more readable the test is. It’s also
Line 585: easier to change a small test when needed. Of course, that’s assuming you don’t
Line 586: try to compress the test code artificially just to reduce the line count. The qual-
Line 587: ity of the test code matters as much as the production code. Don’t cut corners
Line 588: when writing tests; treat the test code as a first-class citizen.
Line 589: How hard it is to run the test—If the test works with out-of-process dependencies,
Line 590: you have to spend time keeping those dependencies operational: reboot the
Line 591: database server, resolve network connectivity issues, and so on. 
Line 592: 4.4
Line 593: In search of an ideal test
Line 594: Here are the four attributes of a good unit test once again:
Line 595: Protection against regressions
Line 596: Resistance to refactoring
Line 597: Fast feedback
Line 598: Maintainability
Line 599: These four attributes, when multiplied together, determine the value of a test. And by
Line 600: multiplied, I mean in a mathematical sense; that is, if a test gets zero in one of the attri-
Line 601: butes, its value turns to zero as well:
Line 602: Value estimate = [0..1] * [0..1] * [0..1] * [0..1]
Line 603: TIP
Line 604: In order to be valuable, the test needs to score at least something in all
Line 605: four categories.
Line 606: Of course, it’s impossible to measure these attributes precisely. There’s no code analy-
Line 607: sis tool you can plug a test into and get the exact numbers. But you can still evaluate
Line 608: the test pretty accurately to see where a test stands with regard to the four attributes.
Line 609: This evaluation, in turn, gives you the test’s value estimate, which you can use to
Line 610: decide whether to keep the test in the suite.
Line 611:  Remember, all code, including test code, is a liability. Set a fairly high threshold
Line 612: for the minimum required value, and only allow tests in the suite if they meet this
Line 613: threshold. A small number of highly valuable tests will do a much better job sustain-
Line 614: ing project growth than a large number of mediocre tests.
Line 615:  I’ll show some examples shortly. For now, let’s examine whether it’s possible to cre-
Line 616: ate an ideal test.
Line 617: 
Line 618: --- 페이지 103 ---
Line 619: 81
Line 620: In search of an ideal test
Line 621: 4.4.1
Line 622: Is it possible to create an ideal test?
Line 623: An ideal test is a test that scores the maximum in all four attributes. If you take the
Line 624: minimum and maximum values as 0 and 1 for each of the attributes, an ideal test must
Line 625: get 1 in all of them.
Line 626:  Unfortunately, it’s impossible to create such an ideal test. The reason is that the
Line 627: first three attributes—protection against regressions, resistance to refactoring, and fast feedback—
Line 628: are mutually exclusive. It’s impossible to maximize them all: you have to sacrifice one
Line 629: of the three in order to max out the remaining two.
Line 630:  Moreover, because of the multiplication principle (see the calculation of the value
Line 631: estimate in the previous section), it’s even trickier to keep the balance. You can’t just
Line 632: forgo one of the attributes in order to focus on the others. As I mentioned previously,
Line 633: a test that scores zero in one of the four categories is worthless. Therefore, you have to
Line 634: maximize these attributes in such a way that none of them is diminished too much.
Line 635: Let’s look at some examples of tests that aim at maximizing two out of three attributes
Line 636: at the expense of the third and, as a result, have a value that’s close to zero. 
Line 637: 4.4.2
Line 638: Extreme case #1: End-to-end tests
Line 639: The first example is end-to-end tests. As you may remember from chapter 2, end-to-end
Line 640: tests look at the system from the end user’s perspective. They normally go through all of
Line 641: the system’s components, including the UI, database, and external applications.
Line 642:  Since end-to-end tests exercise a lot of code, they provide the best protection
Line 643: against regressions. In fact, of all types of tests, end-to-end tests exercise the most
Line 644: code—both your code and the code you didn’t write but use in the project, such as
Line 645: external libraries, frameworks, and third-party applications.
Line 646:  End-to-end tests are also immune to false positives and thus have a good resistance
Line 647: to refactoring. A refactoring, if done correctly, doesn’t change the system’s observable
Line 648: behavior and therefore doesn’t affect the end-to-end tests. That’s another advantage
Line 649: of such tests: they don’t impose any particular implementation. The only thing end-to-
Line 650: end tests look at is how a feature behaves from the end user’s point of view. They are
Line 651: as removed from implementation details as tests could possibly be.
Line 652:  However, despite these benefits, end-to-end tests have a major drawback: they are
Line 653: slow. Any system that relies solely on such tests would have a hard time getting rapid
Line 654: feedback. And that is a deal-breaker for many development teams. This is why it’s
Line 655: pretty much impossible to cover your code base with only end-to-end tests.
Line 656:  Figure 4.6 shows where end-to-end tests stand with regard to the first three unit
Line 657: testing metrics. Such tests provide great protection against both regression errors and
Line 658: false positives, but lack speed. 
Line 659: 
Line 660: --- 페이지 104 ---
Line 661: 82
Line 662: CHAPTER 4
Line 663: The four pillars of a good unit test
Line 664: 4.4.3
Line 665: Extreme case #2: Trivial tests
Line 666: Another example of maximizing two out of three attributes at the expense of the third
Line 667: is a trivial test. Such tests cover a simple piece of code, something that is unlikely to
Line 668: break because it’s too trivial, as shown in the following listing.
Line 669: public class User
Line 670: {
Line 671: public string Name { get; set; }    
Line 672: }
Line 673: [Fact]
Line 674: public void Test()
Line 675: {
Line 676: var sut = new User();
Line 677: sut.Name = "John Smith";
Line 678: Assert.Equal("John Smith", sut.Name);
Line 679: }
Line 680: Unlike end-to-end tests, trivial tests do provide fast feedback—they run very quickly.
Line 681: They also have a fairly low chance of producing a false positive, so they have good
Line 682: resistance to refactoring. Trivial tests are unlikely to reveal any regressions, though,
Line 683: because there’s not much room for a mistake in the underlying code.
Line 684:  Trivial tests taken to an extreme result in tautology tests. They don’t test anything
Line 685: because they are set up in such a way that they always pass or contain semantically
Line 686: meaningless assertions.
Line 687: Listing 4.5
Line 688: Trivial test covering a simple piece of code
Line 689: Resistance to
Line 690: refactoring
Line 691: Fast
Line 692: feedback
Line 693: Protection
Line 694: against
Line 695: regressions
Line 696: End-to-end tests
Line 697: Figure 4.6
Line 698: End-to-end tests 
Line 699: provide great protection against 
Line 700: both regression errors and false 
Line 701: positives, but they fail at the 
Line 702: metric of fast feedback.
Line 703: One-liners like 
Line 704: this are unlikely 
Line 705: to contain bugs.
Line 706: 
Line 707: --- 페이지 105 ---
Line 708: 83
Line 709: In search of an ideal test
Line 710: Figure 4.7 shows where trivial tests stand. They have good resistance to refactoring
Line 711: and provide fast feedback, but they don’t protect you from regressions. 
Line 712: 4.4.4
Line 713: Extreme case #3: Brittle tests
Line 714: Similarly, it’s pretty easy to write a test that runs fast and has a good chance of catching
Line 715: a regression but does so with a lot of false positives. Such a test is called a brittle test: it
Line 716: can’t withstand a refactoring and will turn red regardless of whether the underlying
Line 717: functionality is broken.
Line 718:  You already saw an example of a brittle test in listing 4.2. Here’s another one.
Line 719: public class UserRepository
Line 720: {
Line 721: public User GetById(int id)
Line 722: {
Line 723: /* ... */
Line 724: }
Line 725: public string LastExecutedSqlStatement { get; set; }
Line 726: }
Line 727: [Fact]
Line 728: public void GetById_executes_correct_SQL_code()
Line 729: {
Line 730: var sut = new UserRepository();
Line 731: User user = sut.GetById(5);
Line 732: Assert.Equal(
Line 733: "SELECT * FROM dbo.[User] WHERE UserID = 5",
Line 734: sut.LastExecutedSqlStatement);
Line 735: }
Line 736: Listing 4.6
Line 737: Test verifying which SQL statement is executed
Line 738: Resistance to
Line 739: refactoring
Line 740: Fast
Line 741: feedback
Line 742: Protection
Line 743: against
Line 744: regressions
Line 745: End-to-end tests
Line 746: Trivial tests
Line 747: Figure 4.7
Line 748: Trivial tests have good 
Line 749: resistance to refactoring, and they 
Line 750: provide fast feedback, but such tests 
Line 751: don’t protect you from regressions.
Line 752: 
Line 753: --- 페이지 106 ---
Line 754: 84
Line 755: CHAPTER 4
Line 756: The four pillars of a good unit test
Line 757: This test makes sure the UserRepository class generates a correct SQL statement
Line 758: when fetching a user from the database. Can this test catch a bug? It can. For exam-
Line 759: ple, a developer can mess up the SQL code generation and mistakenly use ID instead
Line 760: of UserID, and the test will point that out by raising a failure. But does this test have
Line 761: good resistance to refactoring? Absolutely not. Here are different variations of the
Line 762: SQL statement that lead to the same result:
Line 763: SELECT * FROM dbo.[User] WHERE UserID = 5
Line 764: SELECT * FROM dbo.User WHERE UserID = 5
Line 765: SELECT UserID, Name, Email FROM dbo.[User] WHERE UserID = 5
Line 766: SELECT * FROM dbo.[User] WHERE UserID = @UserID
Line 767: The test in listing 4.6 will turn red if you change the SQL script to any of these varia-
Line 768: tions, even though the functionality itself will remain operational. This is once again
Line 769: an example of coupling the test to the SUT’s internal implementation details. The test
Line 770: is focusing on hows instead of whats and thus ingrains the SUT’s implementation
Line 771: details, preventing any further refactoring.
Line 772:  Figure 4.8 shows that brittle tests fall into the third bucket. Such tests run fast and
Line 773: provide good protection against regressions but have little resistance to refactoring. 
Line 774: 4.4.5
Line 775: In search of an ideal test: The results
Line 776: The first three attributes of a good unit test (protection against regressions, resistance to
Line 777: refactoring, and fast feedback) are mutually exclusive. While it’s quite easy to come up
Line 778: with a test that maximizes two out of these three attributes, you can only do that at the
Line 779: expense of the third. Still, such a test would have a close-to-zero value due to the mul-
Line 780: tiplication rule. Unfortunately, it’s impossible to create an ideal test that has a perfect
Line 781: score in all three attributes (figure 4.9).
Line 782: Resistance to
Line 783: refactoring
Line 784: Fast
Line 785: feedback
Line 786: Protection
Line 787: against
Line 788: regressions
Line 789: End-to-end tests
Line 790: Trivial tests
Line 791: Brittle tests
Line 792: Figure 4.8
Line 793: Brittle tests run fast and they 
Line 794: provide good protection against regressions, 
Line 795: but they have little resistance to refactoring.
Line 796: 
Line 797: --- 페이지 107 ---
Line 798: 85
Line 799: In search of an ideal test
Line 800: The fourth attribute, maintainability, is not correlated to the first three, with the excep-
Line 801: tion of end-to-end tests. End-to-end tests are normally larger in size because of the
Line 802: necessity to set up all the dependencies such tests reach out to. They also require addi-
Line 803: tional effort to keep those dependencies operational. Hence end-to-end tests tend to
Line 804: be more expensive in terms of maintenance costs.
Line 805:  It’s hard to keep a balance between the attributes of a good test. A test can’t have
Line 806: the maximum score in each of the first three categories, and you also have to keep an
Line 807: eye on the maintainability aspect so the test remains reasonably short and simple.
Line 808: Therefore, you have to make trade-offs. Moreover, you should make those trade-offs
Line 809: in such a way that no particular attribute turns to zero. The sacrifices have to be par-
Line 810: tial and strategic.
Line 811:  What should those sacrifices look like? Because of the mutual exclusiveness of pro-
Line 812: tection against regressions, resistance to refactoring, and fast feedback, you may think that the
Line 813: best strategy is to concede a little bit of each: just enough to make room for all three
Line 814: attributes.
Line 815:  In reality, though, resistance to refactoring is non-negotiable. You should aim at gain-
Line 816: ing as much of it as you can, provided that your tests remain reasonably quick and you
Line 817: don’t resort to the exclusive use of end-to-end tests. The trade-off, then, comes down
Line 818: to the choice between how good your tests are at pointing out bugs and how fast they
Line 819: do that: that is, between protection against regressions and fast feedback. You can view this
Line 820: choice as a slider that can be freely moved between protection against regressions and
Line 821: fast feedback. The more you gain in one attribute, the more you lose on the other
Line 822: (see figure 4.10).
Line 823:  The reason resistance to refactoring is non-negotiable is that whether a test possesses
Line 824: this attribute is mostly a binary choice: the test either has resistance to refactoring or it
Line 825: doesn’t. There are almost no intermediate stages in between. Thus you can’t concede
Line 826: Resistance to
Line 827: refactoring
Line 828: Fast
Line 829: feedback
Line 830: Protection
Line 831: against
Line 832: regressions
Line 833: Unreachable ideal
Line 834: Figure 4.9
Line 835: It’s impossible to create an 
Line 836: ideal test that would have a perfect score 
Line 837: in all three attributes.
Line 838: 
Line 839: --- 페이지 108 ---
Line 840: 86
Line 841: CHAPTER 4
Line 842: The four pillars of a good unit test
Line 843: just a little resistance to refactoring: you’ll have to lose it all. On the other hand, the metrics
Line 844: of protection against regressions and fast feedback are more malleable. You will see in the
Line 845: next section what kind of trade-offs are possible when you choose one over the other.
Line 846: TIP
Line 847: Eradicating brittleness (false positives) in tests is the first priority on the
Line 848: path to a robust test suite.
Line 849: The CAP theorem
Line 850: The trade-off between the first three attributes of a good unit test is similar to the
Line 851: CAP theorem. The CAP theorem states that it is impossible for a distributed data
Line 852: store to simultaneously provide more than two of the following three guarantees:
Line 853: Consistency, which means every read receives the most recent write or an error.
Line 854: Availability, which means every request receives a response (apart from out-
Line 855: ages that affect all nodes in the system).
Line 856: Partition tolerance, which means the system continues to operate despite
Line 857: network partitioning (losing connection between network nodes).
Line 858: The similarity is two-fold:
Line 859: First, there is the two-out-of-three trade-off.
Line 860: Second, the partition tolerance component in large-scale distributed systems is
Line 861: also non-negotiable. A large application such as, for example, the Amazon web-
Line 862: site can’t operate on a single machine. The option of preferring consistency and
Line 863: availability at the expense of partition tolerance simply isn’t on the table—Amazon
Line 864: has too much data to store on a single server, however big that server is.
Line 865: refactoring
Line 866: Max
Line 867: out
Line 868: Protection against
Line 869: regressions
Line 870: Fast feedback
Line 871: Max
Line 872: out
Line 873: Maintainability
Line 874: Choose between the two
Line 875: Resistance to
Line 876: Figure 4.10
Line 877: The best tests exhibit maximum maintainability and resistance 
Line 878: to refactoring; always try to max out these two attributes. The trade-off 
Line 879: comes down to the choice between protection against regressions and fast 
Line 880: feedback.
Line 881: 
Line 882: --- 페이지 109 ---
Line 883: 87
Line 884: Exploring well-known test automation concepts
Line 885: 4.5
Line 886: Exploring well-known test automation concepts
Line 887: The four attributes of a good unit test shown earlier are foundational. All existing,
Line 888: well-known test automation concepts can be traced back to these four attributes. In
Line 889: this section, we’ll look at two such concepts: the Test Pyramid and white-box versus
Line 890: black-box testing.
Line 891: 4.5.1
Line 892: Breaking down the Test Pyramid
Line 893: The Test Pyramid is a concept that advocates for a certain ratio of different types of
Line 894: tests in the test suite (figure 4.11):
Line 895: Unit tests
Line 896: Integration tests
Line 897: End-to-end tests
Line 898: The Test Pyramid is often represented visually as a pyramid with those three types of
Line 899: tests in it. The width of the pyramid layers refers to the prevalence of a particular type
Line 900: The choice, then, also boils down to a trade-off between consistency and availability.
Line 901: In some parts of the system, it’s preferable to concede a little consistency to gain
Line 902: more availability. For example, when displaying a product catalog, it’s generally fine
Line 903: if some parts of the catalog are out of date. Availability is of higher priority in this sce-
Line 904: nario. On the other hand, when updating a product description, consistency is more
Line 905: important than availability: network nodes must have a consensus on what the most
Line 906: recent version of that description is, in order to avoid merge conflicts. 
Line 907: End-
Line 908: to-end
Line 909: Integration
Line 910: tests
Line 911: Unit tests
Line 912: Test count
Line 913: Emulating
Line 914: user
Line 915: Figure 4.11
Line 916: The Test Pyramid advocates for a certain ratio of unit, 
Line 917: integration, and end-to-end tests.
Line 918: 
Line 919: --- 페이지 110 ---
Line 920: 88
Line 921: CHAPTER 4
Line 922: The four pillars of a good unit test
Line 923: of test in the suite. The wider the layer, the greater the test count. The height of the
Line 924: layer is a measure of how close these tests are to emulating the end user’s behavior.
Line 925: End-to-end tests are at the top—they are the closest to imitating the user experience.
Line 926: Different types of tests in the pyramid make different choices in the trade-off between
Line 927: fast feedback and protection against regressions. Tests in higher pyramid layers favor protec-
Line 928: tion against regressions, while lower layers emphasize execution speed (figure 4.12).
Line 929: Notice that neither layer gives up resistance to refactoring. Naturally, end-to-end and inte-
Line 930: gration tests score higher on this metric than unit tests, but only as a side effect of
Line 931: being more detached from the production code. Still, even unit tests should not con-
Line 932: cede resistance to refactoring. All tests should aim at producing as few false positives as
Line 933: possible, even when working directly with the production code. (How to do that is the
Line 934: topic of the next chapter.)
Line 935:  The exact mix between types of tests will be different for each team and project.
Line 936: But in general, it should retain the pyramid shape: end-to-end tests should be the
Line 937: minority; unit tests, the majority; and integration tests somewhere in the middle.
Line 938:  The reason end-to-end tests are the minority is, again, the multiplication rule
Line 939: described in section 4.4. End-to-end tests score extremely low on the metric of fast feed-
Line 940: back. They also lack maintainability: they tend to be larger in size and require addi-
Line 941: tional effort to maintain the involved out-of-process dependencies. Thus, end-to-end
Line 942: tests only make sense when applied to the most critical functionality—features in
Line 943: refactoring
Line 944: Max
Line 945: out
Line 946: Protection against
Line 947: regressions
Line 948: Fast feedback
Line 949: End-to-end
Line 950: Integration
Line 951: Unit tests
Line 952: Resistance to
Line 953: Figure 4.12
Line 954: Different types of tests in the pyramid make different choices 
Line 955: between fast feedback and protection against regressions. End-to-end tests 
Line 956: favor protection against regressions, unit tests emphasize fast feedback, and 
Line 957: integration tests lie in the middle.
Line 958: 
Line 959: --- 페이지 111 ---
Line 960: 89
Line 961: Exploring well-known test automation concepts
Line 962: which you don’t ever want to see any bugs—and only when you can’t get the same
Line 963: degree of protection with unit or integration tests. The use of end-to-end tests for any-
Line 964: thing else shouldn’t pass your minimum required value threshold. Unit tests are usu-
Line 965: ally more balanced, and hence you normally have many more of them.
Line 966:  There are exceptions to the Test Pyramid. For example, if all your application does
Line 967: is basic create, read, update, and delete (CRUD) operations with very few business
Line 968: rules or any other complexity, your test “pyramid” will most likely look like a rectangle
Line 969: with an equal number of unit and integration tests and no end-to-end tests.
Line 970:  Unit tests are less useful in a setting without algorithmic or business complexity—
Line 971: they quickly descend into trivial tests. At the same time, integration tests retain their
Line 972: value—it’s still important to verify how code, however simple it is, works in integration
Line 973: with other subsystems, such as the database. As a result, you may end up with fewer
Line 974: unit tests and more integration tests. In the most trivial examples, the number of inte-
Line 975: gration tests may even be greater than the number of unit tests.
Line 976:  Another exception to the Test Pyramid is an API that reaches out to a single out-of-
Line 977: process dependency—say, a database. Having more end-to-end tests may be a viable
Line 978: option for such an application. Since there’s no user interface, end-to-end tests will
Line 979: run reasonably fast. The maintenance costs won’t be too high, either, because you
Line 980: only work with the single external dependency, the database. Basically, end-to-end
Line 981: tests are indistinguishable from integration tests in this environment. The only thing
Line 982: that differs is the entry point: end-to-end tests require the application to be hosted
Line 983: somewhere to fully emulate the end user, while integration tests normally host the
Line 984: application in the same process. We’ll get back to the Test Pyramid in chapter 8, when
Line 985: we’ll be talking about integration testing. 
Line 986: 4.5.2
Line 987: Choosing between black-box and white-box testing
Line 988: The other well-known test automation concept is black-box versus white-box testing.
Line 989: In this section, I show when to use each of the two approaches:
Line 990: Black-box testing is a method of software testing that examines the functionality
Line 991: of a system without knowing its internal structure. Such testing is normally built
Line 992: around specifications and requirements: what the application is supposed to do,
Line 993: rather than how it does it.
Line 994: White-box testing is the opposite of that. It’s a method of testing that verifies the
Line 995: application’s inner workings. The tests are derived from the source code, not
Line 996: requirements or specifications.
Line 997: There are pros and cons to both of these methods. White-box testing tends to be more
Line 998: thorough. By analyzing the source code, you can uncover a lot of errors that you may
Line 999: miss when relying solely on external specifications. On the other hand, tests resulting
Line 1000: from white-box testing are often brittle, as they tend to tightly couple to the specific
Line 1001: implementation of the code under test. Such tests produce many false positives and
Line 1002: thus fall short on the metric of resistance to refactoring. They also often can’t be traced
Line 1003: 
Line 1004: --- 페이지 112 ---
Line 1005: 90
Line 1006: CHAPTER 4
Line 1007: The four pillars of a good unit test
Line 1008: back to a behavior that is meaningful to a business person, which is a strong sign that
Line 1009: these tests are fragile and don’t add much value. Black-box testing provides the oppo-
Line 1010: site set of pros and cons (table 4.1).
Line 1011: As you may remember from section 4.4.5, you can’t compromise on resistance to refac-
Line 1012: toring: a test either possesses resistance to refactoring or it doesn’t. Therefore, choose black-
Line 1013: box testing over white-box testing by default. Make all tests—be they unit, integration, or
Line 1014: end-to-end—view the system as a black box and verify behavior meaningful to the
Line 1015: problem domain. If you can’t trace a test back to a business requirement, it’s an indi-
Line 1016: cation of the test’s brittleness. Either restructure or delete this test; don’t let it into the
Line 1017: suite as-is. The only exception is when the test covers utility code with high algorith-
Line 1018: mic complexity (more on this in chapter 7).
Line 1019:  Note that even though black-box testing is preferable when writing tests, you can
Line 1020: still use the white-box method when analyzing the tests. Use code coverage tools to see which
Line 1021: code branches are not exercised, but then turn around and test them as if you know nothing about
Line 1022: the code’s internal structure. Such a combination of the white-box and black-box meth-
Line 1023: ods works best. 
Line 1024: Summary
Line 1025: A good unit test has four foundational attributes that you can use to analyze any
Line 1026: automated test, whether unit, integration, or end-to-end:
Line 1027: – Protection against regressions
Line 1028: – Resistance to refactoring
Line 1029: – Fast feedback
Line 1030: – Maintainability
Line 1031: Protection against regressions is a measure of how good the test is at indicating the
Line 1032: presence of bugs (regressions). The more code the test executes (both your
Line 1033: code and the code of libraries and frameworks used in the project), the higher
Line 1034: the chance this test will reveal a bug.
Line 1035: Resistance to refactoring is the degree to which a test can sustain application code
Line 1036: refactoring without producing a false positive.
Line 1037: A false positive is a false alarm—a result indicating that the test fails, whereas
Line 1038: the functionality it covers works as intended. False positives can have a devastat-
Line 1039: ing effect on the test suite:
Line 1040: – They dilute your ability and willingness to react to problems in code, because
Line 1041: you get accustomed to false alarms and stop paying attention to them.
Line 1042: Table 4.1
Line 1043: The pros and cons of white-box and black-box testing
Line 1044: Protection against regressions
Line 1045: Resistance to refactoring
Line 1046: White-box testing
Line 1047: Good
Line 1048: Bad
Line 1049: Black-box testing
Line 1050: Bad
Line 1051: Good
Line 1052: 
Line 1053: --- 페이지 113 ---
Line 1054: 91
Line 1055: Summary
Line 1056: – They diminish your perception of tests as a reliable safety net and lead to los-
Line 1057: ing trust in the test suite.
Line 1058: False positives are a result of tight coupling between tests and the internal imple-
Line 1059: mentation details of the system under test. To avoid such coupling, the test
Line 1060: must verify the end result the SUT produces, not the steps it took to do that.
Line 1061: Protection against regressions and resistance to refactoring contribute to test accuracy.
Line 1062: A test is accurate insofar as it generates a strong signal (is capable of finding
Line 1063: bugs, the sphere of protection against regressions) with as little noise (false posi-
Line 1064: tives) as possible (the sphere of resistance to refactoring).
Line 1065: False positives don’t have as much of a negative effect in the beginning of the
Line 1066: project, but they become increasingly important as the project grows: as import-
Line 1067: ant as false negatives (unnoticed bugs).
Line 1068: Fast feedback is a measure of how quickly the test executes.
Line 1069: Maintainability consists of two components:
Line 1070: – How hard it is to understand the test. The smaller the test, the more read-
Line 1071: able it is.
Line 1072: – How hard it is to run the test. The fewer out-of-process dependencies the test
Line 1073: reaches out to, the easier it is to keep them operational.
Line 1074: A test’s value estimate is the product of scores the test gets in each of the four attri-
Line 1075: butes. If the test gets zero in one of the attributes, its value turns to zero as well.
Line 1076: It’s impossible to create a test that gets the maximum score in all four attri-
Line 1077: butes, because the first three—protection against regressions, resistance to refactor-
Line 1078: ing, and fast feedback—are mutually exclusive. The test can only maximize two
Line 1079: out of the three.
Line 1080: Resistance to refactoring is non-negotiable because whether a test possess this attri-
Line 1081: bute is mostly a binary choice: the test either has resistance to refactoring or it
Line 1082: doesn’t. The trade-off between the attributes comes down to the choice
Line 1083: between protection against regressions and fast feedback.
Line 1084: The Test Pyramid advocates for a certain ratio of unit, integration, and end-to-
Line 1085: end tests: end-to-end tests should be in the minority, unit tests in the majority,
Line 1086: and integration tests somewhere in the middle.
Line 1087: Different types of tests in the pyramid make different choices between fast feed-
Line 1088: back and protection against regressions. End-to-end tests favor protection against
Line 1089: regressions, while unit tests favor fast feedback.
Line 1090: Use the black-box testing method when writing tests. Use the white-box method
Line 1091: when analyzing the tests.