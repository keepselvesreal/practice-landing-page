Line 1: 
Line 2: --- 페이지 25 ---
Line 3: 3
Line 4: The goal of unit testing
Line 5: Learning unit testing doesn’t stop at mastering the technical bits of it, such as
Line 6: your favorite test framework, mocking library, and so on. There’s much more to
Line 7: unit testing than the act of writing tests. You always have to strive to achieve the
Line 8: best return on the time you invest in unit testing, minimizing the effort you put
Line 9: into tests and maximizing the benefits they provide. Achieving both things isn’t
Line 10: an easy task.
Line 11:  It’s fascinating to watch projects that have achieved this balance: they grow
Line 12: effortlessly, don’t require much maintenance, and can quickly adapt to their cus-
Line 13: tomers’ ever-changing needs. It’s equally frustrating to see projects that failed to do
Line 14: so. Despite all the effort and an impressive number of unit tests, such projects drag
Line 15: on slowly, with lots of bugs and upkeep costs.
Line 16: This chapter covers
Line 17: The state of unit testing
Line 18: The goal of unit testing
Line 19: Consequences of having a bad test suite
Line 20: Using coverage metrics to measure test 
Line 21: suite quality
Line 22: Attributes of a successful test suite
Line 23: 
Line 24: --- 페이지 26 ---
Line 25: 4
Line 26: CHAPTER 1
Line 27: The goal of unit testing
Line 28:  That’s the difference between various unit testing techniques. Some yield great
Line 29: outcomes and help maintain software quality. Others don’t: they result in tests that
Line 30: don’t contribute much, break often, and require a lot of maintenance in general.
Line 31:  What you learn in this book will help you differentiate between good and bad unit
Line 32: testing techniques. You’ll learn how to do a cost-benefit analysis of your tests and apply
Line 33: proper testing techniques in your particular situation. You’ll also learn how to avoid
Line 34: common anti-patterns—patterns that may make sense at first but lead to trouble down
Line 35: the road.
Line 36:  But let’s start with the basics. This chapter gives a quick overview of the state of
Line 37: unit testing in the software industry, describes the goal behind writing and maintain-
Line 38: ing tests, and provides you with the idea of what makes a test suite successful.
Line 39: 1.1
Line 40: The current state of unit testing
Line 41: For the past two decades, there’s been a push toward adopting unit testing. The push
Line 42: has been so successful that unit testing is now considered mandatory in most compa-
Line 43: nies. Most programmers practice unit testing and understand its importance. There’s
Line 44: no longer any dispute as to whether you should do it. Unless you’re working on a
Line 45: throwaway project, the answer is, yes, you do.
Line 46:  When it comes to enterprise application development, almost every project
Line 47: includes at least some unit tests. A significant percentage of such projects go far
Line 48: beyond that: they achieve good code coverage with lots and lots of unit and integra-
Line 49: tion tests. The ratio between the production code and the test code could be any-
Line 50: where between 1:1 and 1:3 (for each line of production code, there are one to
Line 51: three lines of test code). Sometimes, this ratio goes much higher than that, to a
Line 52: whopping 1:10.
Line 53:  But as with all new technologies, unit testing continues to evolve. The discussion
Line 54: has shifted from “Should we write unit tests?” to “What does it mean to write good unit
Line 55: tests?” This is where the main confusion still lies.
Line 56:  You can see the results of this confusion in software projects. Many projects have
Line 57: automated tests; they may even have a lot of them. But the existence of those tests
Line 58: often doesn’t provide the results the developers hope for. It can still take program-
Line 59: mers a lot of effort to make progress in such projects. New features take forever to
Line 60: implement, new bugs constantly appear in the already implemented and accepted
Line 61: functionality, and the unit tests that are supposed to help don’t seem to mitigate this
Line 62: situation at all. They can even make it worse.
Line 63:  It’s a horrible situation for anyone to be in—and it’s the result of having unit tests
Line 64: that don’t do their job properly. The difference between good and bad tests is not
Line 65: merely a matter of taste or personal preference, it’s a matter of succeeding or failing
Line 66: at this critical project you’re working on.
Line 67:  It’s hard to overestimate the importance of the discussion of what makes a good
Line 68: unit test. Still, this discussion isn’t occurring much in the software development industry
Line 69: 
Line 70: --- 페이지 27 ---
Line 71: 5
Line 72: The goal of unit testing
Line 73: today. You’ll find a few articles and conference talks online, but I’ve yet to see any
Line 74: comprehensive material on this topic.
Line 75:  The situation in books isn’t any better; most of them focus on the basics of unit
Line 76: testing but don’t go much beyond that. Don’t get me wrong. There’s a lot of value in
Line 77: such books, especially when you are just starting out with unit testing. However, the
Line 78: learning doesn’t end with the basics. There’s a next level: not just writing tests, but
Line 79: doing unit testing in a way that provides you with the best return on your efforts.
Line 80: When you reach this point, most books pretty much leave you to your own devices to
Line 81: figure out how to get to that next level.
Line 82:  This book takes you there. It teaches a precise, scientific definition of the ideal
Line 83: unit test. You’ll see how this definition can be applied to practical, real-world exam-
Line 84: ples. My hope is that this book will help you understand why your particular project
Line 85: may have gone sideways despite having a good number of tests, and how to correct its
Line 86: course for the better.
Line 87:  You’ll get the most value out of this book if you work in enterprise application
Line 88: development, but the core ideas are applicable to any software project.
Line 89: 1.2
Line 90: The goal of unit testing
Line 91: Before taking a deep dive into the topic of unit testing, let’s step back and consider
Line 92: the goal that unit testing helps you to achieve. It’s often said that unit testing practices
Line 93: lead to a better design. And it’s true: the necessity to write unit tests for a code base
Line 94: normally leads to a better design. But that’s not the main goal of unit testing; it’s
Line 95: merely a pleasant side effect.
Line 96: What is an enterprise application?
Line 97: An enterprise application is an application that aims at automating or assisting an
Line 98: organization’s inner processes. It can take many forms, but usually the characteris-
Line 99: tics of an enterprise software are
Line 100: High business logic complexity
Line 101: Long project lifespan
Line 102: Moderate amounts of data
Line 103: Low or moderate performance requirements 
Line 104: The relationship between unit testing and code design
Line 105: The ability to unit test a piece of code is a nice litmus test, but it only works in one
Line 106: direction. It’s a good negative indicator—it points out poor-quality code with relatively
Line 107: high accuracy. If you find that code is hard to unit test, it’s a strong sign that the code
Line 108: needs improvement. The poor quality usually manifests itself in tight coupling, which
Line 109: means different pieces of production code are not decoupled from each other
Line 110: enough, and it’s hard to test them separately.
Line 111: 
Line 112: --- 페이지 28 ---
Line 113: 6
Line 114: CHAPTER 1
Line 115: The goal of unit testing
Line 116: What is the goal of unit testing, then? The goal is to enable sustainable growth of the
Line 117: software project. The term sustainable is key. It’s quite easy to grow a project, especially
Line 118: when you start from scratch. It’s much harder to sustain this growth over time.
Line 119:  Figure 1.1 shows the growth dynamic of a typical project without tests. You start
Line 120: off quickly because there’s nothing dragging you down. No bad architectural deci-
Line 121: sions have been made yet, and there isn’t any existing code to worry about. As time
Line 122: goes by, however, you have to put in more and more hours to make the same amount
Line 123: of progress you showed at the beginning. Eventually, the development speed slows
Line 124: down significantly, sometimes even to the point where you can’t make any progress
Line 125: whatsoever.
Line 126: This phenomenon of quickly decreasing development speed is also known as software
Line 127: entropy. Entropy (the amount of disorder in a system) is a mathematical and scientific
Line 128: concept that can also apply to software systems. (If you’re interested in the math and
Line 129: science of entropy, look up the second law of thermodynamics.)
Line 130:  In software, entropy manifests in the form of code that tends to deteriorate. Each
Line 131: time you change something in a code base, the amount of disorder in it, or entropy,
Line 132: increases. If left without proper care, such as constant cleaning and refactoring, the
Line 133: system becomes increasingly complex and disorganized. Fixing one bug introduces
Line 134: more bugs, and modifying one part of the software breaks several others—it’s like a
Line 135: (continued)
Line 136: Unfortunately, the ability to unit test a piece of code is a bad positive indicator. The
Line 137: fact that you can easily unit test your code base doesn’t necessarily mean it’s of
Line 138: good quality. The project can be a disaster even when it exhibits a high degree of
Line 139: decoupling.
Line 140: Without tests
Line 141: With tests
Line 142: Progress
Line 143: hours
Line 144: spent
Line 145: Work
Line 146: Figure 1.1
Line 147: The difference in growth 
Line 148: dynamics between projects with and 
Line 149: without tests. A project without tests 
Line 150: has a head start but quickly slows down 
Line 151: to the point that it’s hard to make any 
Line 152: progress.
Line 153: 
Line 154: --- 페이지 29 ---
Line 155: 7
Line 156: The goal of unit testing
Line 157: domino effect. Eventually, the code base becomes unreliable. And worst of all, it’s
Line 158: hard to bring it back to stability.
Line 159:  Tests help overturn this tendency. They act as a safety net—a tool that provides
Line 160: insurance against a vast majority of regressions. Tests help make sure the existing
Line 161: functionality works, even after you introduce new features or refactor the code to bet-
Line 162: ter fit new requirements.
Line 163: DEFINITION
Line 164: A regression is when a feature stops working as intended after a cer-
Line 165: tain event (usually, a code modification). The terms regression and software bug
Line 166: are synonyms and can be used interchangeably.
Line 167: The downside here is that tests require initial—sometimes significant—effort. But they
Line 168: pay for themselves in the long run by helping the project to grow in the later stages.
Line 169: Software development without the help of tests that constantly verify the code base
Line 170: simply doesn’t scale.
Line 171:  Sustainability and scalability are the keys. They allow you to maintain development
Line 172: speed in the long run.
Line 173: 1.2.1
Line 174: What makes a good or bad test?
Line 175: Although unit testing helps maintain project growth, it’s not enough to just write tests.
Line 176: Badly written tests still result in the same picture.
Line 177:  As shown in figure 1.2, bad tests do help to slow down code deterioration at the
Line 178: beginning: the decline in development speed is less prominent compared to the situa-
Line 179: tion with no tests at all. But nothing really changes in the grand scheme of things. It
Line 180: might take longer for such a project to enter the stagnation phase, but stagnation is
Line 181: still inevitable.
Line 182: Without tests
Line 183: With good tests
Line 184: With bad tests
Line 185: Progress
Line 186: Work
Line 187: hours
Line 188: spent
Line 189: Figure 1.2
Line 190: The difference in 
Line 191: growth dynamics between 
Line 192: projects with good and bad 
Line 193: tests. A project with badly 
Line 194: written tests exhibits the 
Line 195: properties of a project with 
Line 196: good tests at the beginning, 
Line 197: but it eventually falls into 
Line 198: the stagnation phase.
Line 199: 
Line 200: --- 페이지 30 ---
Line 201: 8
Line 202: CHAPTER 1
Line 203: The goal of unit testing
Line 204: Remember, not all tests are created equal. Some of them are valuable and contribute a lot
Line 205: to overall software quality. Others don’t. They raise false alarms, don’t help you catch
Line 206: regression errors, and are slow and difficult to maintain. It’s easy to fall into the trap
Line 207: of writing unit tests for the sake of unit testing without a clear picture of whether it
Line 208: helps the project.
Line 209:  You can’t achieve the goal of unit testing by just throwing more tests at the project.
Line 210: You need to consider both the test’s value and its upkeep cost. The cost component is
Line 211: determined by the amount of time spent on various activities:
Line 212: Refactoring the test when you refactor the underlying code
Line 213: Running the test on each code change
Line 214: Dealing with false alarms raised by the test
Line 215: Spending time reading the test when you’re trying to understand how the
Line 216: underlying code behaves
Line 217: It’s easy to create tests whose net value is close to zero or even is negative due to high
Line 218: maintenance costs. To enable sustainable project growth, you have to exclusively
Line 219: focus on high-quality tests—those are the only type of tests that are worth keeping in
Line 220: the test suite.
Line 221: It’s crucial to learn how to differentiate between good and bad unit tests. I cover this
Line 222: topic in chapter 4. 
Line 223: 1.3
Line 224: Using coverage metrics to measure test suite quality
Line 225: In this section, I talk about the two most popular coverage metrics—code coverage
Line 226: and branch coverage—how to calculate them, how they’re used, and problems with
Line 227: them. I’ll show why it’s detrimental for programmers to aim at a particular coverage
Line 228: number and why you can’t just rely on coverage metrics to determine the quality of
Line 229: your test suite.
Line 230: DEFINITION
Line 231: A coverage metric shows how much source code a test suite exe-
Line 232: cutes, from none to 100%.
Line 233: Production code vs. test code 
Line 234: People often think production code and test code are different. Tests are assumed
Line 235: to be an addition to production code and have no cost of ownership. By extension,
Line 236: people often believe that the more tests, the better. This isn’t the case. Code is a
Line 237: liability, not an asset. The more code you introduce, the more you extend the surface
Line 238: area for potential bugs in your software, and the higher the project’s upkeep cost. It’s
Line 239: always better to solve problems with as little code as possible.
Line 240: Tests are code, too. You should view them as the part of your code base that aims at
Line 241: solving a particular problem: ensuring the application’s correctness. Unit tests, just
Line 242: like any other code, are also vulnerable to bugs and require maintenance.
Line 243: 
Line 244: --- 페이지 31 ---
Line 245: 9
Line 246: Using coverage metrics to measure test suite quality
Line 247: There are different types of coverage metrics, and they’re often used to assess the
Line 248: quality of a test suite. The common belief is that the higher the coverage number,
Line 249: the better.
Line 250:  Unfortunately, it’s not that simple, and coverage metrics, while providing valuable
Line 251: feedback, can’t be used to effectively measure the quality of a test suite. It’s the same
Line 252: situation as with the ability to unit test the code: coverage metrics are a good negative
Line 253: indicator but a bad positive one.
Line 254:  If a metric shows that there’s too little coverage in your code base—say, only 10%—
Line 255: that’s a good indication that you are not testing enough. But the reverse isn’t true:
Line 256: even 100% coverage isn’t a guarantee that you have a good-quality test suite. A test
Line 257: suite that provides high coverage can still be of poor quality.
Line 258:  I already touched on why this is so—you can’t just throw random tests at your
Line 259: project with the hope those tests will improve the situation. But let’s discuss this
Line 260: problem in detail with respect to the code coverage metric.
Line 261: 1.3.1
Line 262: Understanding the code coverage metric
Line 263: The first and most-used coverage metric is code coverage, also known as test coverage; see
Line 264: figure 1.3. This metric shows the ratio of the number of code lines executed by at least
Line 265: one test and the total number of lines in the production code base.
Line 266: Let’s see an example to better understand how this works. Listing 1.1 shows an
Line 267: IsStringLong method and a test that covers it. The method determines whether a
Line 268: string provided to it as an input parameter is long (here, the definition of long is any
Line 269: string with the length greater than five characters). The test exercises the method
Line 270: using "abc" and checks that this string is not considered long.
Line 271: public static bool IsStringLong(string input)
Line 272: {
Line 273:            
Line 274: if (input.Length > 5)          
Line 275: return true;
Line 276:     
Line 277: return false;
Line 278:            
Line 279: }
Line 280:           
Line 281: Listing 1.1
Line 282: A sample method partially covered by a test
Line 283: Code coverage (test coverage) =
Line 284: Total number of lines
Line 285: Lines of code executed
Line 286: Figure 1.3
Line 287: The code coverage (test coverage) metric is 
Line 288: calculated as the ratio between the number of code lines 
Line 289: executed by the test suite and the total number of lines in 
Line 290: the production code base.
Line 291: Covered 
Line 292: by the 
Line 293: test
Line 294: Not
Line 295: covered
Line 296: by the
Line 297: test
Line 298: 
Line 299: --- 페이지 32 ---
Line 300: 10
Line 301: CHAPTER 1
Line 302: The goal of unit testing
Line 303: public void Test()
Line 304: {
Line 305: bool result = IsStringLong("abc");
Line 306: Assert.Equal(false, result);
Line 307: }
Line 308: It’s easy to calculate the code coverage here. The total number of lines in the method
Line 309: is five (curly braces count, too). The number of lines executed by the test is four—the
Line 310: test goes through all the code lines except for the return true; statement. This gives
Line 311: us 4/5 = 0.8 = 80% code coverage.
Line 312:  Now, what if I refactor the method and inline the unnecessary if statement, like this?
Line 313: public static bool IsStringLong(string input)
Line 314: {
Line 315: return input.Length > 5;
Line 316: }
Line 317: public void Test()
Line 318: {
Line 319: bool result = IsStringLong("abc");
Line 320: Assert.Equal(false, result);
Line 321: }
Line 322: Does the code coverage number change? Yes, it does. Because the test now exercises
Line 323: all three lines of code (the return statement plus two curly braces), the code coverage
Line 324: increases to 100%.
Line 325:  But did I improve the test suite with this refactoring? Of course not. I just shuffled the
Line 326: code inside the method. The test still verifies the same number of possible outcomes.
Line 327:  This simple example shows how easy it is to game the coverage numbers. The more
Line 328: compact your code is, the better the test coverage metric becomes, because it only
Line 329: accounts for the raw line numbers. At the same time, squashing more code into less
Line 330: space doesn’t (and shouldn’t) change the value of the test suite or the maintainability
Line 331: of the underlying code base. 
Line 332: 1.3.2
Line 333: Understanding the branch coverage metric
Line 334: Another coverage metric is called branch coverage. Branch coverage provides more pre-
Line 335: cise results than code coverage because it helps cope with code coverage’s shortcom-
Line 336: ings. Instead of using the raw number of code lines, this metric focuses on control
Line 337: structures, such as if and switch statements. It shows how many of such control struc-
Line 338: tures are traversed by at least one test in the suite, as shown in figure 1.4.
Line 339: Branch coverage = Total number of branches
Line 340: Branches traversed
Line 341: Figure 1.4
Line 342: The branch metric is calculated as the ratio of the 
Line 343: number of code branches exercised by the test suite and the 
Line 344: total number of branches in the production code base.
Line 345: 
Line 346: --- 페이지 33 ---
Line 347: 11
Line 348: Using coverage metrics to measure test suite quality
Line 349: To calculate the branch coverage metric, you need to sum up all possible branches in
Line 350: your code base and see how many of them are visited by tests. Let’s take our previous
Line 351: example again:
Line 352: public static bool IsStringLong(string input)
Line 353: {
Line 354: return input.Length > 5;
Line 355: }
Line 356: public void Test()
Line 357: {
Line 358: bool result = IsStringLong("abc");
Line 359: Assert.Equal(false, result);
Line 360: }
Line 361: There are two branches in the IsStringLong method: one for the situation when the
Line 362: length of the string argument is greater than five characters, and the other one when
Line 363: it’s not. The test covers only one of these branches, so the branch coverage metric is
Line 364: 1/2 = 0.5 = 50%. And it doesn’t matter how we represent the code under test—
Line 365: whether we use an if statement as before or use the shorter notation. The branch cov-
Line 366: erage metric only accounts for the number of branches; it doesn’t take into consider-
Line 367: ation how many lines of code it took to implement those branches.
Line 368:  Figure 1.5 shows a helpful way to visualize this metric. You can represent all pos-
Line 369: sible paths the code under test can take as a graph and see how many of them have
Line 370: been traversed. IsStringLong has two such paths, and the test exercises only one
Line 371: of them.
Line 372: Start
Line 373: Length <= 5
Line 374: End
Line 375: Length > 5
Line 376: Figure 1.5
Line 377: The method IsStringLong represented as a graph of possible 
Line 378: code paths. Test covers only one of the two code paths, thus providing 50% 
Line 379: branch coverage.
Line 380: 
Line 381: --- 페이지 34 ---
Line 382: 12
Line 383: CHAPTER 1
Line 384: The goal of unit testing
Line 385: 1.3.3
Line 386: Problems with coverage metrics
Line 387: Although the branch coverage metric yields better results than code coverage, you still
Line 388: can’t rely on either of them to determine the quality of your test suite, for two reasons:
Line 389: You can’t guarantee that the test verifies all the possible outcomes of the system
Line 390: under test.
Line 391: No coverage metric can take into account code paths in external libraries.
Line 392: Let’s look more closely at each of these reasons.
Line 393: YOU CAN’T GUARANTEE THAT THE TEST VERIFIES ALL THE POSSIBLE OUTCOMES
Line 394: For the code paths to be actually tested and not just exercised, your unit tests must
Line 395: have appropriate assertions. In other words, you need to check that the outcome the
Line 396: system under test produces is the exact outcome you expect it to produce. Moreover,
Line 397: this outcome may have several components; and for the coverage metrics to be mean-
Line 398: ingful, you need to verify all of them.
Line 399:  The next listing shows another version of the IsStringLong method. It records the
Line 400: last result into a public WasLastStringLong property.
Line 401: public static bool WasLastStringLong { get; private set; }
Line 402: public static bool IsStringLong(string input)
Line 403: {
Line 404: bool result = input.Length > 5;
Line 405: WasLastStringLong = result;         
Line 406: return result;
Line 407:      
Line 408: }
Line 409: public void Test()
Line 410: {
Line 411: bool result = IsStringLong("abc");
Line 412: Assert.Equal(false, result);   
Line 413: }
Line 414: The IsStringLong method now has two outcomes: an explicit one, which is encoded
Line 415: by the return value; and an implicit one, which is the new value of the property. And
Line 416: in spite of not verifying the second, implicit outcome, the coverage metrics would still
Line 417: show the same results: 100% for the code coverage and 50% for the branch coverage.
Line 418: As you can see, the coverage metrics don’t guarantee that the underlying code is
Line 419: tested, only that it has been executed at some point.
Line 420:  An extreme version of this situation with partially tested outcomes is assertion-free
Line 421: testing, which is when you write tests that don’t have any assertion statements in them
Line 422: whatsoever. Here’s an example of assertion-free testing.
Line 423:  
Line 424:  
Line 425: Listing 1.2
Line 426: Version of IsStringLong that records the last result
Line 427: First 
Line 428: outcome
Line 429: Second 
Line 430: outcome
Line 431: The test verifies only 
Line 432: the second outcome.
Line 433: 
Line 434: --- 페이지 35 ---
Line 435: 13
Line 436: Using coverage metrics to measure test suite quality
Line 437: public void Test()
Line 438: {
Line 439: bool result1 = IsStringLong("abc");   
Line 440: bool result2 = IsStringLong("abcdef");   
Line 441: }
Line 442: This test has both code and branch coverage metrics showing 100%. But at the same
Line 443: time, it is completely useless because it doesn’t verify anything.
Line 444: But let’s say that you thoroughly verify each outcome of the code under test. Does this,
Line 445: in combination with the branch coverage metric, provide a reliable mechanism, which
Line 446: you can use to determine the quality of your test suite? Unfortunately, no. 
Line 447: Listing 1.3
Line 448: A test with no assertions always passes.
Line 449: A story from the trenches
Line 450: The concept of assertion-free testing might look like a dumb idea, but it does happen
Line 451: in the wild.
Line 452: Years ago, I worked on a project where management imposed a strict requirement of
Line 453: having 100% code coverage for every project under development. This initiative had
Line 454: noble intentions. It was during the time when unit testing wasn’t as prevalent as it is
Line 455: today. Few people in the organization practiced it, and even fewer did unit testing
Line 456: consistently.
Line 457: A group of developers had gone to a conference where many talks were devoted to
Line 458: unit testing. After returning, they decided to put their new knowledge into practice.
Line 459: Upper management supported them, and the great conversion to better programming
Line 460: techniques began. Internal presentations were given. New tools were installed. And,
Line 461: more importantly, a new company-wide rule was imposed: all development teams had
Line 462: to focus on writing tests exclusively until they reached the 100% code coverage mark.
Line 463: After they reached this goal, any code check-in that lowered the metric had to be
Line 464: rejected by the build systems.
Line 465: As you might guess, this didn’t play out well. Crushed by this severe limitation, devel-
Line 466: opers started to seek ways to game the system. Naturally, many of them came to the
Line 467: same realization: if you wrap all tests with try/catch blocks and don’t introduce any
Line 468: assertions in them, those tests are guaranteed to pass. People started to mindlessly
Line 469: create tests for the sake of meeting the mandatory 100% coverage requirement.
Line 470: Needless to say, those tests didn’t add any value to the projects. Moreover, they
Line 471: damaged the projects because of all the effort and time they steered away from pro-
Line 472: ductive activities, and because of the upkeep costs required to maintain the tests
Line 473: moving forward.
Line 474: Eventually, the requirement was lowered to 90% and then to 80%; after some period
Line 475: of time, it was retracted altogether (for the better!).
Line 476: Returns true
Line 477: Returns false
Line 478: 
Line 479: --- 페이지 36 ---
Line 480: 14
Line 481: CHAPTER 1
Line 482: The goal of unit testing
Line 483: NO COVERAGE METRIC CAN TAKE INTO ACCOUNT CODE PATHS IN EXTERNAL LIBRARIES
Line 484: The second problem with all coverage metrics is that they don’t take into account
Line 485: code paths that external libraries go through when the system under test calls meth-
Line 486: ods on them. Let’s take the following example:
Line 487: public static int Parse(string input)
Line 488: {
Line 489: return int.Parse(input);
Line 490: }
Line 491: public void Test()
Line 492: {
Line 493: int result = Parse("5");
Line 494: Assert.Equal(5, result);
Line 495: }
Line 496: The branch coverage metric shows 100%, and the test verifies all components of the
Line 497: method’s outcome. It has a single such component anyway—the return value. At the
Line 498: same time, this test is nowhere near being exhaustive. It doesn’t take into account
Line 499: the code paths the .NET Framework’s int.Parse method may go through. And
Line 500: there are quite a number of code paths, even in this simple method, as you can see
Line 501: in figure 1.6.
Line 502: The built-in integer type has plenty of branches that are hidden from the test and
Line 503: that might lead to different results, should you change the method’s input parameter.
Line 504: Here are just a few possible arguments that can’t be transformed into an integer:
Line 505: Null value
Line 506: An empty string
Line 507: “Not an int”
Line 508: A string that’s too large
Line 509: Hidden
Line 510: part
Line 511: Start
Line 512: int.Parse
Line 513: null
Line 514: “ ”
Line 515: “5”
Line 516: “not an int”
Line 517: End
Line 518: Figure 1.6
Line 519: Hidden code paths of external libraries. Coverage metrics have no way to see how 
Line 520: many of them there are and how many of them your tests exercise.
Line 521: 
Line 522: --- 페이지 37 ---
Line 523: 15
Line 524: What makes a successful test suite?
Line 525: You can fall into numerous edge cases, and there’s no way to see if your tests account
Line 526: for all of them.
Line 527:  This is not to say that coverage metrics should take into account code paths in
Line 528: external libraries (they shouldn’t), but rather to show you that you can’t rely on
Line 529: those metrics to see how good or bad your unit tests are. Coverage metrics can’t
Line 530: possibly tell whether your tests are exhaustive; nor can they say if you have enough
Line 531: tests. 
Line 532: 1.3.4
Line 533: Aiming at a particular coverage number
Line 534: At this point, I hope you can see that relying on coverage metrics to determine the
Line 535: quality of your test suite is not enough. It can also lead to dangerous territory if you
Line 536: start making a specific coverage number a target, be it 100%, 90%, or even a moder-
Line 537: ate 70%. The best way to view a coverage metric is as an indicator, not a goal in and
Line 538: of itself.
Line 539:  Think of a patient in a hospital. Their high temperature might indicate a fever and
Line 540: is a helpful observation. But the hospital shouldn’t make the proper temperature of
Line 541: this patient a goal to target by any means necessary. Otherwise, the hospital might end
Line 542: up with the quick and “efficient” solution of installing an air conditioner next to the
Line 543: patient and regulating their temperature by adjusting the amount of cold air flowing
Line 544: onto their skin. Of course, this approach doesn’t make any sense.
Line 545:  Likewise, targeting a specific coverage number creates a perverse incentive that
Line 546: goes against the goal of unit testing. Instead of focusing on testing the things that
Line 547: matter, people start to seek ways to attain this artificial target. Proper unit testing is dif-
Line 548: ficult enough already. Imposing a mandatory coverage number only distracts develop-
Line 549: ers from being mindful about what they test, and makes proper unit testing even
Line 550: harder to achieve.
Line 551: TIP
Line 552: It’s good to have a high level of coverage in core parts of your system.
Line 553: It’s bad to make this high level a requirement. The difference is subtle but
Line 554: critical.
Line 555: Let me repeat myself: coverage metrics are a good negative indicator, but a bad posi-
Line 556: tive one. Low coverage numbers—say, below 60%—are a certain sign of trouble. They
Line 557: mean there’s a lot of untested code in your code base. But high numbers don’t mean
Line 558: anything. Thus, measuring the code coverage should be only a first step on the way to
Line 559: a quality test suite. 
Line 560: 1.4
Line 561: What makes a successful test suite?
Line 562: I’ve spent most of this chapter discussing improper ways to measure the quality of a
Line 563: test suite: using coverage metrics. What about a proper way? How should you mea-
Line 564: sure your test suite’s quality? The only reliable way is to evaluate each test in the
Line 565: suite individually, one by one. Of course, you don’t have to evaluate all of them at
Line 566: 
Line 567: --- 페이지 38 ---
Line 568: 16
Line 569: CHAPTER 1
Line 570: The goal of unit testing
Line 571: once; that could be quite a large undertaking and require significant upfront effort.
Line 572: You can perform this evaluation gradually. The point is that there’s no automated
Line 573: way to see how good your test suite is. You have to apply your personal judgment.
Line 574:  Let’s look at a broader picture of what makes a test suite successful as a whole.
Line 575: (We’ll dive into the specifics of differentiating between good and bad tests in chapter 4.)
Line 576: A successful test suite has the following properties:
Line 577: It’s integrated into the development cycle.
Line 578: It targets only the most important parts of your code base.
Line 579: It provides maximum value with minimum maintenance costs.
Line 580: 1.4.1
Line 581: It’s integrated into the development cycle
Line 582: The only point in having automated tests is if you constantly use them. All tests should
Line 583: be integrated into the development cycle. Ideally, you should execute them on every
Line 584: code change, even the smallest one. 
Line 585: 1.4.2
Line 586: It targets only the most important parts of your code base
Line 587: Just as all tests are not created equal, not all parts of your code base are worth the
Line 588: same attention in terms of unit testing. The value the tests provide is not only in how
Line 589: those tests themselves are structured, but also in the code they verify.
Line 590:  It’s important to direct your unit testing efforts to the most critical parts of the sys-
Line 591: tem and verify the others only briefly or indirectly. In most applications, the most
Line 592: important part is the part that contains business logic—the domain model.1 Testing
Line 593: business logic gives you the best return on your time investment.
Line 594:  All other parts can be divided into three categories:
Line 595: Infrastructure code
Line 596: External services and dependencies, such as the database and third-party systems
Line 597: Code that glues everything together
Line 598: Some of these other parts may still need thorough unit testing, though. For example,
Line 599: the infrastructure code may contain complex and important algorithms, so it would
Line 600: make sense to cover them with a lot of tests, too. But in general, most of your attention
Line 601: should be spent on the domain model.
Line 602:  Some of your tests, such as integration tests, can go beyond the domain model and
Line 603: verify how the system works as a whole, including the noncritical parts of the code
Line 604: base. And that’s fine. But the focus should remain on the domain model.
Line 605:  Note that in order to follow this guideline, you should isolate the domain model
Line 606: from the non-essential parts of the code base. You have to keep the domain model
Line 607: separated from all other application concerns so you can focus your unit testing
Line 608: 1 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).
Line 609: 
Line 610: --- 페이지 39 ---
Line 611: 17
Line 612: What you will learn in this book
Line 613: efforts on that domain model exclusively. We talk about all this in detail in part 2 of
Line 614: the book. 
Line 615: 1.4.3
Line 616: It provides maximum value with minimum maintenance costs
Line 617: The most difficult part of unit testing is achieving maximum value with minimum
Line 618: maintenance costs. That’s the main focus of this book.
Line 619:  It’s not enough to incorporate tests into a build system, and it’s not enough to
Line 620: maintain high test coverage of the domain model. It’s also crucial to keep in the suite
Line 621: only the tests whose value exceeds their upkeep costs by a good margin.
Line 622:  This last attribute can be divided in two:
Line 623: Recognizing a valuable test (and, by extension, a test of low value)
Line 624: Writing a valuable test
Line 625: Although these skills may seem similar, they’re different by nature. To recognize a test
Line 626: of high value, you need a frame of reference. On the other hand, writing a valuable
Line 627: test requires you to also know code design techniques. Unit tests and the underlying
Line 628: code are highly intertwined, and it’s impossible to create valuable tests without put-
Line 629: ting significant effort into the code base they cover.
Line 630:  You can view it as the difference between recognizing a good song and being able
Line 631: to compose one. The amount of effort required to become a composer is asymmetri-
Line 632: cally larger than the effort required to differentiate between good and bad music. The
Line 633: same is true for unit tests. Writing a new test requires more effort than examining an
Line 634: existing one, mostly because you don’t write tests in a vacuum: you have to take into
Line 635: account the underlying code. And so although I focus on unit tests, I also devote a sig-
Line 636: nificant portion of this book to discussing code design. 
Line 637: 1.5
Line 638: What you will learn in this book
Line 639: This book teaches a frame of reference that you can use to analyze any test in your test
Line 640: suite. This frame of reference is foundational. After learning it, you’ll be able to look
Line 641: at many of your tests in a new light and see which of them contribute to the project
Line 642: and which must be refactored or gotten rid of altogether.
Line 643:  After setting this stage (chapter 4), the book analyzes the existing unit testing tech-
Line 644: niques and practices (chapters 4–6, and part of 7). It doesn’t matter whether you’re
Line 645: familiar with those techniques and practices. If you are familiar with them, you’ll see
Line 646: them from a new angle. Most likely, you already get them at the intuitive level. This
Line 647: book can help you articulate why the techniques and best practices you’ve been using
Line 648: all along are so helpful.
Line 649:  Don’t underestimate this skill. The ability to clearly communicate your ideas to col-
Line 650: leagues is priceless. A software developer—even a great one—rarely gets full credit for
Line 651: a design decision if they can’t explain why, exactly, that decision was made. This book
Line 652: can help you transform your knowledge from the realm of the unconscious to some-
Line 653: thing you are able to talk about with anyone.
Line 654: 
Line 655: --- 페이지 40 ---
Line 656: 18
Line 657: CHAPTER 1
Line 658: The goal of unit testing
Line 659:  If you don’t have much experience with unit testing techniques and best practices,
Line 660: you’ll learn a lot. In addition to the frame of reference that you can use to analyze any
Line 661: test in a test suite, the book teaches
Line 662: How to refactor the test suite along with the production code it covers
Line 663: How to apply different styles of unit testing
Line 664: Using integration tests to verify the behavior of the system as a whole
Line 665: Identifying and avoiding anti-patterns in unit tests
Line 666: In addition to unit tests, this book covers the entire topic of automated testing, so
Line 667: you’ll also learn about integration and end-to-end tests.
Line 668:  I use C# and .NET in my code samples, but you don’t have to be a C# professional
Line 669: to read this book; C# is just the language that I happen to work with the most. All
Line 670: the concepts I talk about are non-language-specific and can be applied to any other
Line 671: object-oriented language, such as Java or C++.
Line 672: Summary
Line 673: Code tends to deteriorate. Each time you change something in a code base, the
Line 674: amount of disorder in it, or entropy, increases. Without proper care, such as
Line 675: constant cleaning and refactoring, the system becomes increasingly complex
Line 676: and disorganized. Tests help overturn this tendency. They act as a safety net— a
Line 677: tool that provides insurance against the vast majority of regressions.
Line 678: It’s important to write unit tests. It’s equally important to write good unit tests.
Line 679: The end result for projects with bad tests or no tests is the same: either stagna-
Line 680: tion or a lot of regressions with every new release.
Line 681: The goal of unit testing is to enable sustainable growth of the software project.
Line 682: A good unit test suite helps avoid the stagnation phase and maintain the devel-
Line 683: opment pace over time. With such a suite, you’re confident that your changes
Line 684: won’t lead to regressions. This, in turn, makes it easier to refactor the code or
Line 685: add new features.
Line 686: All tests are not created equal. Each test has a cost and a benefit component,
Line 687: and you need to carefully weigh one against the other. Keep only tests of posi-
Line 688: tive net value in the suite, and get rid of all others. Both the application code
Line 689: and the test code are liabilities, not assets.
Line 690: The ability to unit test code is a good litmus test, but it only works in one direc-
Line 691: tion. It’s a good negative indicator (if you can’t unit test the code, it’s of poor
Line 692: quality) but a bad positive one (the ability to unit test the code doesn’t guaran-
Line 693: tee its quality).
Line 694: Likewise, coverage metrics are a good negative indicator but a bad positive one.
Line 695: Low coverage numbers are a certain sign of trouble, but a high coverage num-
Line 696: ber doesn’t automatically mean your test suite is of high quality.
Line 697: Branch coverage provides better insight into the completeness of the test suite
Line 698: but still can’t indicate whether the suite is good enough. It doesn’t take into
Line 699: 
Line 700: --- 페이지 41 ---
Line 701: 19
Line 702: Summary
Line 703: account the presence of assertions, and it can’t account for code paths in third-
Line 704: party libraries that your code base uses.
Line 705: Imposing a particular coverage number creates a perverse incentive. It’s good
Line 706: to have a high level of coverage in core parts of your system, but it’s bad to make
Line 707: this high level a requirement.
Line 708: A successful test suite exhibits the following attributes:
Line 709: – It is integrated into the development cycle.
Line 710: – It targets only the most important parts of your code base.
Line 711: – It provides maximum value with minimum maintenance costs.
Line 712: The only way to achieve the goal of unit testing (that is, enabling sustainable
Line 713: project growth) is to
Line 714: – Learn how to differentiate between a good and a bad test.
Line 715: – Be able to refactor a test to make it more valuable.