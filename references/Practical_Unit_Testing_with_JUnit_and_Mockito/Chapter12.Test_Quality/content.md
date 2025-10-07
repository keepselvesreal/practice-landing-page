Line 1: 
Line 2: --- 페이지 243 ---
Line 3: Chapter 12. Test Quality
Line 4: A job worth doing is worth doing well.
Line 5: — An old saying
Line 6: Who watches the watchmen?
Line 7: — Juvenal
Line 8: Developers are obsessed with quality, and for good reasons. First of all, quality is proof of excellence
Line 9: in code writing - and we all want to be recognized as splendid coders, don’t we? Second, we have all
Line 10: heard about some spectacular catastrophes that occurred because of the poor quality of the software
Line 11: involved. Even if the software you are writing is not intended to put a man on the Moon, you still
Line 12: won’t want to disappoint your client with bugs. Third, we all know that just like a boomerang, bad
Line 13: code will one day come right back and hit us so hard that we never forget it - one more reason to write
Line 14: the best code possible!
Line 15: Since we have agreed that developers tests are important (if not crucial), we should also be concerned
Line 16: about their quality. If we cannot guarantee that the tests we have are really, really good, then all we
Line 17: have is a false sense of security.
Line 18: The topic of test quality has been implicitly present from the very beginning of this book, because we
Line 19: have cared about each test being readable, focused, concise, well-named, etc. Nevertheless, it is now
Line 20: time to investigate this in detail. In this section we shall try to answer two questions: how to measure
Line 21: test quality and how to improve it.
Line 22: In the course of our voyage into the realm of test quality, we will discover that in general it is hard
Line 23: to assess the quality of tests, at least when using certain tools. There is no tool that could verify a
Line 24: successful implementation of the "testing behaviour, not methods" rule (see Section 11.1), or that
Line 25: could make sure you "name your tests methods consistently" (see Section 10.2). This is an unhappy
Line 26: conclusion, but we should not give up hope completely. High-quality tests are hard to come by, but
Line 27: not impossible, and if we adhere to the right principles, then maybe achieving them will turn out not
Line 28: to be so very hard after all. Some tools can also help, if used right.
Line 29: 12.1. An Overview
Line 30: When talking about quality we should always ask "if" before we ask "how". Questions like "would
Line 31: I be better off writing an integration test or a unit test for this?", or "do I really need to cover this
Line 32: scenario – isn’t it perhaps already covered by another test?", should come before any pondering of
Line 33: the design and implementation of test code. A useless and/or redundant test of the highest quality is
Line 34: still, well, useless and/or redundant. Do not waste your time writing perfect tests that should not have
Line 35: been written at all!
Line 36: There is nothing so useless as doing efficiently that which should not be done at all.
Line 37: — Peter Drucker
Line 38: In the rest of this chapter we shall assume that a positive answer has been given to this first "if"
Line 39: question. This is often the case with unit tests which, in general, should be written for every piece of
Line 40: code you create.
Line 41: 228
Line 42: 
Line 43: --- 페이지 244 ---
Line 44: Chapter 12. Test Quality
Line 45: Test Smells
Line 46: When dealing with production code, we use the "code smell"1 to refer to various statements in code
Line 47: that do not look (smell) right. Such code smells have been gathered, given names and are widely
Line 48: recognized within the community. Also, there are some tools (e.g. PMD2 or Findbugs3) which are
Line 49: capable of discovering common code smells. For test code there is a similar term - "test smell" - which
Line 50: is much less commonly used. Also, there is no generally agreed on list of test code smells similar
Line 51: to that for production code4. What all of this adds up to is that the problem of various bad things in
Line 52: test code has been recognized, but not widely enough to get standardized in the sort of way that has
Line 53: happened with production code.
Line 54: Let me also mention that many of the so-called code or test smells are nothing more than catchy
Line 55: names for some manifestation of a more general rule. Take, for example, the "overriding stubbing"
Line 56: test smell, which occurs if you first describe the stubbing behaviour of one stub in a setUp()
Line 57: method, and then override it in some test methods. This is something to be avoided, as it diminishes
Line 58: readability. The thing is, if you follow a general rule of avoiding "global" objects, you will not write
Line 59: code which emits this bad smell anyway. This is why I am not inclined to ponder every possible
Line 60: existing test smell. I would rather hope that once you are following the best programming practices -
Line 61: both in production code and test code - many test smells will simply never happen in your code. So in
Line 62: this part of the book I will only be describing those bad practices which I meet with most often when
Line 63: working with code.
Line 64: Refactoring
Line 65: When talking about code smells, we can not pass over the subject of refactoring. We have already
Line 66: introduced the term and given some examples of refactoring in action, when describing the TDD
Line 67: rhythm. In this chapter we will discuss some refactorings of test code. As with production code
Line 68: refactoring, refactorings of test code help to achieve higher quality of both types: internal and
Line 69: external. Internal, because well-refactored tests are easier to understand and maintain, and external,
Line 70: because by refactoring we are making it more probable that our tests actually test something valuable.
Line 71: At this point a cautious reader will pause in their reading – feeling that something is not
Line 72: quite right here. True! Previously, I defined refactoring as moving through code "over a
Line 73: safety net of tests", whereas now I am using this term to describe an activity performed in
Line 74: the absence of tests (since we do not have tests for tests, right?). Yes, right! It is actually a
Line 75: misuse of the term "refactoring" to apply it to the activity of changing test code. However,
Line 76: the problem is that it is so commonly used this way that I dare not give it any other name.
Line 77: Code Quality Influences Tests Quality
Line 78: Another point worth remembering is that there is a strong relation between the quality of your
Line 79: production code and test code. Having good, clean, maintainable tests is definitely possible.
Line 80: The first step is to write cleaner, better designed and truly loosely-coupled production code. If the
Line 81: production code is messy, then there is a considerable likelihood that your tests will also be. If your
Line 82: production code is fine, then your tests have a chance of being good, too. The second step is to start
Line 83: treating your test code with the same respect as your production code. This means your test code
Line 84: 1http://en.wikipedia.org/wiki/Code_smell
Line 85: 2http://pmd.sourceforge.net/
Line 86: 3http://findbugs.sourceforge.net/
Line 87: 4At this point I would like to encourage you to read the list of TDD anti-patterns gathered by James Carr - [carr2006]
Line 88: 229
Line 89: 
Line 90: --- 페이지 245 ---
Line 91: Chapter 12. Test Quality
Line 92: should obey the same rules (KISS, SRP) that you apply to production code: i.e. it should avoid things
Line 93: you do not use in your code (e.g. extensive use of reflection, deep class hierarchies, etc.), and you
Line 94: should care about its quality (e.g. by having it analyzed statically, and put through a code review
Line 95: process).
Line 96: Always Observe a Failing Test
Line 97: Before we discuss ways of measuring and improving the quality of tests, let me remind you of one
Line 98: very important piece of advice, which has a lot to do with this subject. It may sound like a joke,
Line 99: but in fact observing a failing test is one way to check its quality: if it fails, then this proves that it
Line 100: really does verify some behaviour. Of course, this is not enough to mean that the test is valuable, but
Line 101: provided that you have not written the test blindfolded, it does mean something. So, make sure never
Line 102: to omit the RED phase of TDD, and always witness a failing test by actually seeing it fail.
Line 103: Obviously, this advice chiefly makes sense for TDD followers. But sometimes it could also
Line 104: be reasonable to break the production code intentionally to make sure your tests actually
Line 105: test something.
Line 106: 12.2. Static Analysis Tools
Line 107: Now that we have some basic knowledge regarding tests quality, let us look for the ways to measure
Line 108: it. Our first approach will be to use tools which perform a static code analysis in order to find some
Line 109: deficiencies. Are they helpful for test code? Let us take a look at this.
Line 110: You will surely use static code analyzers (e.g. PMD, Findbugs or what your IDE offers) to verify your
Line 111: production code. The aim of these tools is to discover various anti-patterns, and point out possible
Line 112: bugs. They are quite smart when it comes to reporting various code smells. Currently, it is normal
Line 113: engineering practice to have them as a part of a team’s Definition of Done5. Such tools are often
Line 114: integrated with IDEs, and/or are a part of the continuous integration process. A natural next step
Line 115: would be to also use them to verify your test code and reveal its dodgy parts.
Line 116: And you should use them – after all, why not? It will not cost you much, that is for sure. Simply
Line 117: include them in your build process and - voilà! - your test code is verified. But…, but the reality is
Line 118: different. In fact, you should not expect too much when performing static analysis on your test
Line 119: code. The main reason for this is, that your test code is dead simple, right? There are rarely any
Line 120: nested try-catch statements, opened streams, reused variables, deep inheritance hierarchies, multiple
Line 121: returns from methods, violations of hashCode()/equals() contracts, or other things that static code
Line 122: analyzers are so good at dealing with. In fact your tests are this simple: you just set up objects, execute
Line 123: methods and assert. Not much work for such tools.
Line 124: Another form of static analysis is calculation of various code metrics, such as number of lines per
Line 125: class or per method, and the famous cyclomatic complexity6. They will generally tell you whether
Line 126: your code is too complex or not. Obviously, test classes and methods should stick to the same (or even
Line 127: stricter) rules than your production code, so verifying this seems like a good idea. But because you
Line 128: have no logic in your tests (as discussed in Section 11.2), the complexity of your test methods should
Line 129: be very low by default. Thus, such analysis will rarely reveal any problems in your test code.
Line 130: 5See http://www.scrumalliance.org/articles/105-what-is-definition-of-done-dod and other net resources for more information on
Line 131: Defintion of Done.
Line 132: 6http://en.wikipedia.org/wiki/Cyclomatic_complexity
Line 133: 230
Line 134: 
Line 135: --- 페이지 246 ---
Line 136: Chapter 12. Test Quality
Line 137: To conclude, static analysis tools do not help much when it comes to tests code. No tool or metric
Line 138: will tell you if you have written good tests. Use them, listen to what they say, but do not expect too
Line 139: much. If you write your tests following the basic rules given in this section, then there is not much
Line 140: they can do for you.
Line 141: 12.3. Code Coverage
Line 142: If you can not measure it, you can not improve it.
Line 143: — William Thomson 1st Baron Kelvin
Line 144: Having been seriously disappointed by what static code analysis tools have to offer with regard to
Line 145: finding test code smells (see Section 12.2), let us turn towards another group of tools, which are
Line 146: commonly used to assess test quality. Are they any better at finding test smells, and weaknesses of
Line 147: any kind, in your test code?
Line 148: This section is devoted to a group of popular tools which utilize the code coverage technique7, and
Line 149: can provide a good deal of interesting information regarding your tests. We will discuss both their
Line 150: capabilities and limits. What we are really interested in is whether they can be used to measure,
Line 151: and hopefully improve, test quality. For the time being, we shall leave the technical issues relating
Line 152: to running them and concentrate solely on the usefulness of code coverage tools in the field of test
Line 153: quality measurement.
Line 154: Code coverage measures which parts of your code were executed: i.e. which parts of the production
Line 155: code were executed during tests. They work by augmenting production code with additional
Line 156: statements, which do not change the semantics of the original code. The purpose of these additional
Line 157: instructions is to record information about executed fragments (lines, methods, statements) of code
Line 158: and to present it, later, as numerical data in coverage reports.
Line 159: Code coverage tools also measure some other metrics - e.g. cyclomatic complexity8.
Line 160: However, these do not really relate to test quality, so we shall not be discussing them in
Line 161: this section.
Line 162: 12.3.1. Line and Branch Coverage
Line 163:   "Code coverage" is a broad term which denotes a number of types of coverage measurement,
Line 164: sometimes very different from one another. Wikipedia9 describes them all in details. However,
Line 165: many of them are rather theoretical, and no tool supports them (mainly because their practical use is
Line 166: limited).
Line 167: In this section I will present two types of code coverage measure provided by a popular Cobertura10
Line 168: tool: line and branch coverage:
Line 169: • Line coverage is a very simple metric. All it says is whether a particular line (or rather statement)
Line 170: of code has been exercised or not. If a line was "touched" during test execution, then it counts as
Line 171: 7See http://en.wikipedia.org/wiki/Code_coverage
Line 172: 8See http://en.wikipedia.org/wiki/Software_metric, and especially http://en.wikipedia.org/wiki/Cyclomatic_complexity, for more
Line 173: information on this topic.
Line 174: 9See http://en.wikipedia.org/wiki/Code_coverage
Line 175: 10http://cobertura.sourceforge.net/
Line 176: 231
Line 177: 
Line 178: --- 페이지 247 ---
Line 179: Chapter 12. Test Quality
Line 180: covered. Simple, yet misleading - as will be discussed further. This kind of coverage is also known
Line 181: as statement coverage.
Line 182: • Branch coverage focuses on decision points in production code, such as if or while statements
Line 183: with logical && or || operators. This is a much stronger measure than line coverage. In practice, to
Line 184: satisfy branch coverage, you must write tests such that every logical expression in your code gets to
Line 185: be evaluated to true and to false.
Line 186: The difference between the two is very significant. While getting 100% line coverage is a pretty
Line 187: straightforward affair, much more effort must be made to obtain such a value for branch coverage.
Line 188: The following snippet of code illustrates this11.
Line 189: Listing 12.1. A simple function to measure coverage
Line 190: public boolean foo(boolean a, boolean b) {
Line 191:     boolean result = false;
Line 192:     if (a && b) {
Line 193:         result = true;
Line 194:     }
Line 195:     return result;
Line 196: }
Line 197: To obtain 100% line coverage it is enough to execute foo(true, true) from the test code. For
Line 198: branch coverage we need three cases to reach 100% coverage: foo(true, false), foo(true,
Line 199: true) and foo(false, false).
Line 200: Now that we understand the types of code coverage provided by Cobertura, let us take a look at the
Line 201: results of its work.
Line 202: 12.3.2. Code Coverage Reports
Line 203: After the tests have been run, code coverage tools generate a report on coverage metrics. This is
Line 204: possible thanks to the additional information previously added to the production code.
Line 205: As we shall soon see, coverage reports can be used to gain an overall impression regarding code
Line 206: coverage, but also to scrutinize selected classes. They act as a spyglass and a microscope in one. We
Line 207: shall start with the view from 10,000 feet (i.e. project coverage), then move down to package level,
Line 208: and finally reach ground level with classes.
Line 209: Figure 12.1. Code coverage - packages overview
Line 210: Figure 12.1 presents an overview of some project coverage. For each package the following statistics
Line 211: are given:
Line 212: 11The code used to illustrate line and branch coverage is based on Wikipedia example: http://en.wikipedia.org/wiki/Code_coverage
Line 213: 232
Line 214: 
Line 215: --- 페이지 248 ---
Line 216: Chapter 12. Test Quality
Line 217: • the percentage of line coverage, along with the total number of lines and number of lines covered,
Line 218: • the percentage of branch coverage, along with the total number of branches and, for purposes of
Line 219: comparison, the number of branches covered.
Line 220: As you might guess, a red color is used for those parts of the code not executed (not "covered") during
Line 221: the tests. So - the more green, the better? Well, yes and no - we will get to this soon.
Line 222: Figure 12.2. Code coverage - single package
Line 223: The report shown in Figure 12.2 gives an overview of code coverage for the whole package, and for
Line 224: individual classes of the package. As with the previous report, it gives information on line and branch
Line 225: coverage. Figure 12.3 provides an example.
Line 226: Figure 12.3. Single class coverage
Line 227: Figure 12.3 presents code for our old friend - the Money class. This report shows precisely which parts
Line 228: of the Money class are covered by tests. The green color denotes parts that have been tested, the red
Line 229: those not executed during the tests. The first column of numbers is the line of code, while the second
Line 230: gives some additional information, about the number of times each line was "touched" during the
Line 231: testing. For example, in the case of line 12 (the if statement) the number on a red background says 1.
Line 232: 233
Line 233: 
Line 234: --- 페이지 249 ---
Line 235: Chapter 12. Test Quality
Line 236: This means that this if statement has only been executed once. We may guess that the current tests
Line 237: contain only one case, which makes this if evaluate to true. If we were to add another test which
Line 238: evaluated this Boolean expression to false, then the number 1 on a red background would change
Line 239: to 2 on a green background. Also, the coverage of line 17 would change from 0 to 1 (and from red to
Line 240: green).
Line 241: 12.3.3. The Devil is in the Details
Line 242: Let us take a closer look at this last example of detailed code coverage of the Money class. Listing 12.2
Line 243: shows tests which have been executed to obtain the following quite high level of coverage: 86% line
Line 244: coverage and 50% branch coverage.
Line 245: Listing 12.2. Tests of the Money class
Line 246:     @Test
Line 247:     void constructorShouldSetAmountAndCurrency() {
Line 248:         Money money = new Money(10, "USD");
Line 249:         assertThat(money.getAmount()).isEqualTo(10);
Line 250:         assertThat(money.getCurrency()).isEqualTo("USD");
Line 251:     }
Line 252:     @Test
Line 253:     void shouldBeAbleToAddMoney() {
Line 254:         assertThat(new Money(3, "USD").add(new Money(4, "USD"))).
Line 255:                 isEqualTo(new Money(7, "USD"));
Line 256:     }
Line 257: The tests shown in Listing 12.2 are not the best we have seen so far in terms of how they are written,
Line 258: but this is not the point. The thing is, they are highly incomplete, given the requirements that the
Line 259: Money class is supposed to fulfill. We have already discussed the notion that each feature should be
Line 260: tested with more than one test case (i.e. with many values - see Section 7.1). However, it seems that
Line 261: one can obtain quite high coverage by testing just some features with a single test case.
Line 262: This is an interesting observation. Interesting, or maybe rather ominous, considering the
Line 263: number of people who feel entitled to an opinion regarding the quality of tests based on
Line 264: code coverage measurements.
Line 265: What we could do, to achieve even higher coverage, would be to add some more tests. Listing 12.3
Line 266: shows such an attempt. This test was created only in order to make the branch code coverage higher.
Line 267: If we measure the branch coverage now, we will learn that it has gone up from 50% to 75%.
Line 268: Listing 12.3. Additional test method of the Money class
Line 269: @Test
Line 270: void differentMoneyShouldNotBeEqual() {
Line 271:         assertThat(new Money(7, "USD"))
Line 272:                 .isNotEqualTo(new Money(7, "CHF"));
Line 273:         assertThat(new Money(7, "USD"))
Line 274:                 .isNotEqualTo(new Money(8, "USD"));
Line 275:     }
Line 276: Please note that there are many important features of the Money class that we are still not verifying.
Line 277: For example, it would be nice to make sure that objects of the Money class are immutable, but if you
Line 278: 234
Line 279: 
Line 280: --- 페이지 250 ---
Line 281: Chapter 12. Test Quality
Line 282: think about such a test, it would not make the code coverage any higher. We would also like to make
Line 283: sure the addition really works, by verifying it with some more examples. But no, we have not done
Line 284: anything like this, and yet… voilà! - we already have 86% line coverage and 75% branch coverage.
Line 285: This simple example reveals a very important weakness of code coverage measures. Code coverage
Line 286: tools do not measure whether tests cover requirements! They only measure what parts of the
Line 287: production code were executed when running the tests.
Line 288: 12.3.4. How Much Code Coverage is Good
Line 289: Enough?
Line 290: You should, at least once in your lifetime, get 100% coverage – just so you know how
Line 291: it tastes. Then you can decide whether it is worth the effort.
Line 292: — Jaroslav Tulach Geecon 2011 Talk (paraphrased)
Line 293: I can get 100% code coverage and test nothing because I have no asserts. Stop making
Line 294: coverage a goal, it’s only a way!
Line 295: — Twitter @unclebobmartin 2011 Apr 8
Line 296: Since code coverage exists, there must also be a question we can ask about what is the good/
Line 297: appropriate/required amount of code coverage. The question appears in many forms, usually as a
Line 298: "should I aim at 100% coverage"? Like many other dilemmas, this one has also received some quite
Line 299: contradictory answers. Let us have a look at this.
Line 300: From the examples presented so far, we should already understand that high code coverage, even
Line 301: 100% code coverage, does not mean the tests are of high quality. You can write tests of no value at
Line 302: all (e.g. tests without assertions), whose only goal is to prop up the coverage metrics. In fact, this
Line 303: often happens when management demands that developers obtain certain, usually very high, values of
Line 304: code coverage. If the team cannot fulfil these requirements (for example because of lack of skills), the
Line 305: coverage metrics will be meaningless. Their only value will be in keeping management happy. Nice in
Line 306: the short term, but not very useful in the long run.
Line 307: The use of red and green colors makes coverage reports resemble those of tests results. On the one
Line 308: hand, this is convenient, because the "green-is-good" and "red-is-bad" associations are probably well
Line 309: entrenched in developers’ minds. On the other hand, a red color used in a test result, and the same
Line 310: red color in a coverage report, do not mean the same thing. Yet it makes developers follow a "no
Line 311: red policy" and focus on eliminating anything that shows up as red. This means they might try to get
Line 312: 100% coverage even though, as we have already noted, this might not be the most important thing
Line 313: needing to be done.
Line 314: This raises another issue. High coverage measures, together with the misguided assumption that "tests
Line 315: ensure that it works", might lead you to a (false) feeling of security. However, in the light of what was
Line 316: discussed previously, you should not feel secure, even if your code coverage does reach the 100%
Line 317: mark. "Our code is working fine because we have 100% code coverage" is a fallacy.
Line 318: Also, with regard to what was said earlier in connection with "things too simple to break" (see Section
Line 319: 11.5), there are some parts of the code which do not deserve to be tested. This makes 100% code
Line 320: coverage a goal not worth chasing, as it makes developers write tests which are not really worth the
Line 321: effort. A grotesque example might be writing a test for a private constructor in a static class, which is
Line 322: there for the sole purpose of never being called…
Line 323: 235
Line 324: 
Line 325: --- 페이지 251 ---
Line 326: Chapter 12. Test Quality
Line 327: So, what is the answer to the question which opened this section? How much coverage is desirable,
Line 328: and how much should be considered inadequate? A popular answer to this has been given by
Line 329: [savoia2007]. Basically, it suggests the following12:
Line 330: • If you begin your adventure with testing, you should not worry about code coverage. Concentrate
Line 331: on writing good tests and honing your testing skills. If you spend too much time thinking about
Line 332: coverage, you will get depressed (because it is unlikely that you will be able to achieve high values
Line 333: at this point).
Line 334: • If you are experienced, then you know that there are no simple answers, and you are able to handle
Line 335: this truth and keep on working. No threshold of required code coverage can be taken as given,
Line 336: because the desired level depends on many factors that only you, the author of the code, can
Line 337: possibly understand.
Line 338: What I, myself, would add, is that no matter what level of experience you have, you should focus on
Line 339: testing all of the important requirements of your classes, and only then check code coverage.
Line 340: 12.3.5. Conclusion
Line 341: Code coverage tells you what you definitely haven’t tested, not what you have.
Line 342: — Mark Simpson StackOverflow discussion 2009
Line 343: In this section we have seen the two faces of code coverage. The first face is friendly and helpful. It
Line 344: allows you to get a good understanding of the parts of the code which are not covered by tests and
Line 345: thus find the gaps in your safety net. However, there is also another face to code coverage. This one
Line 346: makes you worry about seeing the color red on coverage reports and waste time writing tests for lines
Line 347: that are not worth it. It also makes you feel secure, and makes you believe that your code works as
Line 348: required (when neither of these are in fact justified).
Line 349: The point is, that you should choose what is good in code coverage and ignore the rest. You should
Line 350: use it to:
Line 351: • Learn what you definitely have not tested.
Line 352: • Make sure you do not lose some tests during huge redesigns of your test code (which happens
Line 353: rarely).
Line 354: • Have a broader picture of gaps in your safety net of tests.
Line 355: Code coverage is also useful if you want to see the time trend of coverage and compare it with
Line 356: other things that happened within the team (trainings, new people joining the team, technology
Line 357: change, etc.). It is also good for seeing if there are some parts of the code which are typically being
Line 358: undertested. For example, team members might not have the skills needed for testing expected
Line 359: exceptions, thus leaving such code untested.
Line 360: But be wary, and always remember that:
Line 361: • Code coverage does not translate directly into quality. There is no simple relation here. Period.
Line 362: • "Covered" does not mean it is really "tested".
Line 363: 12I would encourage you to read the original version of the article.
Line 364: 236
Line 365: 
Line 366: --- 페이지 252 ---
Line 367: Chapter 12. Test Quality
Line 368: • Even 100% code coverage does not mean your tests cover all business requirements. They only
Line 369: signify that every statement in your production code gets executed during tests. This is not the
Line 370: same.
Line 371: • It is completely useless in cases of multithreaded testing. Imagine you run only a single test case
Line 372: against such code, using only one thread. This is obviously a nonsensical test, because it does not
Line 373: evaluate the most important feature of this code – no matter that you were able to achieve 100%
Line 374: code coverage thanks to such a useless test.
Line 375: • Never write a test just to push up code coverage. Each test should aim at covering some important
Line 376: functionality of your code
Line 377: TDD is probably the best way of achieving high "functional" code coverage. By designing your code
Line 378: with tests, you not only make code coverage reports look nice, but also the coverage values become
Line 379: meaningful. This is because they now reflect the amount of functionalities covered by tests.
Line 380: Code coverage is often used to check the quality of tests, which is not a good idea. As we have
Line 381: learned in this section, coverage measures are not credible indicators of test quality. Code coverage
Line 382: might help by showing you deficiencies in your safety net of tests, but not much more than this. In
Line 383: addition to code coverage, you should use other techniques (i.e. visual inspection - see Section 12.5)
Line 384: to supplement its indications. 
Line 385: 12.4. Mutation Testing
Line 386: High quality software cannot be done without high quality testing. Mutation testing
Line 387: measures how “good” our tests are by inserting faults into the program under test. Each
Line 388: fault generates a new program, a mutant, that is slightly different from the original. The
Line 389: idea is that the tests are adequate if they detect all mutants.
Line 390: — Mattias Bybro A Mutation Testing Tool For Java Programs (2003)
Line 391: As discussed in the previous section, code coverage is a weak indicator of test quality. Let us now take
Line 392: a look at another approach, called mutation testing, which promises to furnish us with more detailed
Line 393: information regarding the quality of tests.
Line 394: Suppose you have some classes and a suite of tests. Now imagine that you introduce a change into
Line 395: one of your classes, for example by reverting (negating) one of the if conditional expressions. In
Line 396: doing this you have created a so-called mutant of the original code. What should happen now, if you
Line 397: run all your tests once again? Provided that the suite of tests contains a test that examines this class
Line 398: thoroughly, then this test should fail. If no test fails, this means your test suite is not good enough13.
Line 399: And that is precisely the concept of mutation testing.
Line 400: 12.4.1. How does it Work?
Line 401: Mutation testing tools create a plethora of "mutants": that is, slightly changed versions of the original
Line 402: production code. Then, they run tests against each mutant. The quality of the tests is assessed by the
Line 403: number of mutants killed by the tests14. The tools differ mainly in the following respects:
Line 404: 13In fact, if all tests still pass, it can also mean that the "mutant" program is equivalent in behaviour to the original program.
Line 405: 14Okay, I admit it: this heuristic sounds like it was taken from the game series Fallout: "the more dead mutants, the better" :).
Line 406: 237
Line 407: 
Line 408: --- 페이지 253 ---
Line 409: Chapter 12. Test Quality
Line 410: • how the mutants are created (they can be brought to life by modifying source code or bytecode),
Line 411: • the set of available mutators,
Line 412: • performance (e.g. detecting equivalent mutations, so the tests are not run twice etc.).
Line 413: Mutants are created by applying various mutation operators - i.e. simple syntactic or semantic
Line 414: transformation rules - to the production code. The most basic mutation operators introduce changes
Line 415: to the various language operators - mathematical (e.g. +, -, *, /), relational (e.g. =, !=, <, >) or logical
Line 416: (e.g. &, |, !). An example of a mutation would be to switch the sign < to > within some logical
Line 417: condition. These simple mutators mimic typical sources of errors - typos or instances of the wrong
Line 418: logical operators being used. Likewise, by changing some values in the code, it is easy to simulate
Line 419: off-by-one errors. Other possible mutations are, for example, removing method calls (possible
Line 420: with void methods), changing returned values, changing constant values, etc. Some tools have also
Line 421: experimented with more Java-specific mutators, for example relating to Java collections.
Line 422: 12.4.2. Working with PIT
Line 423: PIT Mutation Testing is the Java mutation testing tool currently available. It works at the bytecode
Line 424: level, which means it creates mutants without touching the source code. After PIT’s execution has
Line 425: finished, it provides detailed information on created and killed mutants. It also creates an HTML
Line 426: report showing line coverage and a mutation coverage report. We will concentrate on the latter, as
Line 427: line coverage has already been discussed in Section 12.3.
Line 428: We will use a very simple example to demonstrate PIT in action and confront it with code coverage
Line 429: tools. Listing 12.4 shows our "production code", which will be mutated by PIT15.
Line 430: Listing 12.4. Method with two if statements
Line 431: public class TwoIfs {
Line 432:     public int twoIfs(int a, int b) {
Line 433:         if (a > 0) {
Line 434:             return 1;
Line 435:         } else {
Line 436:             System.out.println();
Line 437:         }
Line 438:         if (b > 0) {
Line 439:             return 3;
Line 440:         } else {
Line 441:             return 4;
Line 442:         }
Line 443:     }
Line 444: }
Line 445: Let us say that we also have a test class which (supposedly) verifies the correctness of the twoIfs()
Line 446: method:
Line 447: Listing 12.5. Tests for the twoIfs method
Line 448: public class TwoIfsTest {
Line 449: 15The idea of this code is taken from the StackOverflow discussion about code coverage pitfalls - http://stackoverflow.com/
Line 450: questions/695811/pitfalls-of-code-coverage.
Line 451: 238
Line 452: 
Line 453: --- 페이지 254 ---
Line 454: Chapter 12. Test Quality
Line 455:     @Test
Line 456:     void testTwoIfs() {
Line 457:         TwoIfs twoIfs = new TwoIfs();
Line 458:         assertThat(twoIfs.twoIfs(1, -1))
Line 459:             .isEqualTo(1);
Line 460:         assertThat(twoIfs.twoIfs(-1, 1))
Line 461:             .isEqualTo(3);
Line 462:         assertThat(twoIfs.twoIfs(-1, -1))
Line 463:             .isEqualTo(4);
Line 464:         }
Line 465: }
Line 466: What is really interesting is that this simple test is good enough to satisfy the code coverage tool - it
Line 467: achieves 100% in respect of both line and branch coverage! Figure 12.4 shows this:
Line 468: Figure 12.4. 100% code coverage - isn’t that great?
Line 469: When we execute a PIT analysis, it will create mutants of the production code from Listing 12.4 by
Line 470: reverting the inequality operators and fiddling with comparison values. Then it will run all tests (in
Line 471: our case only the one test shown in Listing 12.5) against each mutant and check if they failed.
Line 472:   The outcome report shows the code that was mutated together with some information about applied
Line 473: mutations. Just like with code coverage reports, the red background denotes "bad" lines of code,
Line 474: which means that some mutations performed on these lines went unnoticed when testing. Below the
Line 475: source code there is a list of applied mutations. From this list we can learn that, for example, one
Line 476: mutant survived the change of conditional boundary in line 6. The "greater than" symbol was changed
Line 477: to "greater or equal" and the tests still passed. The report informs us that such and such a mutant
Line 478: SURVIVED, which means it was not detected by our tests.
Line 479: 239
Line 480: 
Line 481: --- 페이지 255 ---
Line 482: Chapter 12. Test Quality
Line 483: Figure 12.5. Mutation testing - PIT report
Line 484: This simple example shows the difference between code coverage and mutation testing: in short, it is
Line 485: much simpler to satisfy coverage tools, whereas mutation testing tools can detect more holes within
Line 486: your tests.
Line 487: 12.4.3. Conclusions
Line 488: Mutation testing has been around since the late 1970s but is rarely used outside
Line 489: academia. Executing a huge number of mutants and finding equivalent mutants has
Line 490: been too expensive for practical use.
Line 491: — Mattias Bybro A Mutation Testing Tool For Java Programs (2003)
Line 492: Mutation testing looks interesting, but I have never met a team yet, that would use it successfully in
Line 493: a commercial project. There could be many reasons why this idea has never made it into developers'
Line 494: toolboxes, but I think the main one is that for a very long time there were no mutation testing tools
Line 495: that were production-ready. Existing tools were lagging behind relative to the progress of Java
Line 496: language (e.g. not supporting Java 5 annotations), and/or were not up to the industry standards and
Line 497: developers’ expectations in terms of reliability and ease of use. Because of this, code coverage, which
Line 498: has had decent tools for years, is today a standard part of every development process, while mutation
Line 499: testing is nowhere to be found. As for today, developers in general not only know nothing about such
Line 500: tools, but are even unaware of the very concept of mutation testing!
Line 501: This situation has improved with the rise of the PIT framework in the last years. The whole ecosystem
Line 502: of affiliated tools is slowly catching up with what code coverage already has to offer in respect of
Line 503: build tools and IDE plugins, integration with CI servers, and so on.
Line 504: 240
Line 505: 
Line 506: --- 페이지 256 ---
Line 507: Chapter 12. Test Quality
Line 508: Mutation testing tools have already made significant progress in terms of how they perform with
Line 509: regard to mutant creation (currently available tools work on the bytecode level to avoid recompilation,
Line 510: while earlier tools worked by changing the source code). The real performance issue relates to the fact
Line 511: that mutation testing tools work by executing tests many times over. Even if each execution takes only
Line 512: seconds, this can add up to a huge number, taking into consideration the number of created mutants.
Line 513: This excludes mutation testing tools from the normal TDD fast iteration cycles16. 
Line 514: 12.5. Code Reviews
Line 515: People exchange work products to review, with the expectation that as authors, they
Line 516: will produce errors, and as reviewers, they will find errors. Everyone ends up learning
Line 517: from their own mistakes and other people’s mistakes.
Line 518: — Johanna Rothman
Line 519: We have already discussed the usefulness of three kinds of tool for measuring and improving test
Line 520: quality: static code analyzers fall far short of our expectations, while both code coverage (see Section
Line 521: 12.3) and mutation testing (Section 12.4) have their uses, and it makes sense to have them in your
Line 522: toolbox. Yet they do not cover the full spectrum of test quality issues. In order to gain really insightful
Line 523: feedback on the quality of our code we need to have another developer analyze it. The process of
Line 524: working with others’ code in order to make it better is known as code review.
Line 525: A lot has been written already about code reviews, and it is not my goal to discuss their place and
Line 526: role in the software development process. Let me conclude with a short statement to the effect that
Line 527: code reviews are a must, because they help discover bugs, thus improving internal and external code
Line 528: quality, and because they spread knowledge of the code among different team members and help us
Line 529: improve by learning from each other.
Line 530: All of this is also true for code reviews performed on test code. In the absence of tools which could
Line 531: help us with validating the correctness, and assessing the quality, of our test code, code reviews are
Line 532: the only option for delivering test code of the highest quality. In this section we will discuss various
Line 533: aspects of performing code reviews of test code, and how they differ from reviews of production code.
Line 534: Before we begin, two important things to remember:
Line 535: • First of all, if your team performs code reviews (no matter if they are performed by some senior
Line 536: developer, or by your peers), it should also include test code. This code is as important as
Line 537: production code, and your prospects for a hassle-free future as a developer depend on its quality.
Line 538: • Secondly, issues discovered during reviews of test code can signify two things: that the tests are
Line 539: weak in themselves, or that the production code is of low quality. Looking into test code often
Line 540: reveals various weaknesses of the production code. This is yet another benefit of having your test
Line 541: code reviewed!
Line 542: When reading this section you might have a certain feeling of déjà vu. This is because
Line 543: many of the issues mentioned here simply invert good practices described elsewhere in the
Line 544: various chapters of this book.
Line 545: 16As far as I know, this issue is being treated very seriously by mutation testing tools authors, and a lot of improvements have
Line 546: already been made. For example, these tools can select a tiny subset of the potentially "strongest" mutants and only execute tests
Line 547: against them, thus significantly reducing the testing time.
Line 548: 241
Line 549: 
Line 550: --- 페이지 257 ---
Line 551: Chapter 12. Test Quality
Line 552: 12.5.1. A Three-Minute Test Code Review
Line 553: Code reviews take time. In an ideal world, we would have this time, but in reality things are different.
Line 554: Let us now see what can be done to perform a very quick test code review, so that next time when you
Line 555: have only three minutes and are hesitating about whether to do it at all, you will have a short checklist
Line 556: of things which could be validated, even in such a short time.
Line 557: Size Heuristics
Line 558:  Some idea of test code quality might be gained by looking at the following features of the test code:
Line 559: • the number of imported classes,
Line 560: • the number of test doubles used,
Line 561: • the length of set-up methods,
Line 562: • the length of test methods,
Line 563: • the length of test class.
Line 564: It is not possible to come up with exact numbers here - which should trigger a red light in your head.
Line 565: However, common sense is usually enough to distinguish right from wrong. For example, three test
Line 566: doubles in a test class are probably fine, but if there are eight of them, then an alarm bell should
Line 567: ring. And what about four, five, six or seven test doubles? Where is the exact border? As usual, "it
Line 568: depends", and you need some more time to decide whether or not things are fine. The same holds true
Line 569: for the number of imports (and the variety of imported classes).
Line 570: As for the length of the test methods and classes, here, again, common sense should be sufficient.
Line 571: Once again, please remember that finding weaknesses in any of the above might be
Line 572: a symptom of bad production code, which is only reflected by the test code. Violations
Line 573: of reasonable size values for test code usually indicate that the class being tested has too
Line 574: much responsibility.
Line 575: But do They Run?
Line 576: Unit tests should run in a matter of seconds, so three minutes will give you enough time to run all of
Line 577: them.
Line 578: • Is there a build script which allows anyone to execute them, or do they need some manual setup
Line 579: (e.g. running your IDE)? If the latter, then this is something to really worry about.
Line 580: • How much times does it take for tests to finish? If it is more than 20 seconds (again, this is not
Line 581: a value you should take too literally), then these are probably not unit tests but integration tests.
Line 582: • Are they really run - do they really get picked out by your build script?
Line 583: Check Code Coverage
Line 584: As we noted in Section 12.3, code coverage can inform us about areas of code that are being
Line 585: undertested. Three minutes should be enough time to run the build script and have a look at the code
Line 586: 242
Line 587: 
Line 588: --- 페이지 258 ---
Line 589: Chapter 12. Test Quality
Line 590: coverage report. What you are looking to find, in such a short period of time, are white areas of
Line 591: untested code. There is no time to ponder over each line, but it is definitely possible to see that some
Line 592: package has 20% code coverage, while the rest is close to 80%17.
Line 593: …and if there is no build script which would allow you to generate a code coverage report? Well, then
Line 594: you have one more issue to report to your colleagues.
Line 595: Conclusions
Line 596: Three minutes will not allow you to perform a real test code review, but it is enough to uncover some
Line 597: major issues with the test code. If this is all you can have at the moment, then fair enough - it is still
Line 598: much better than nothing.
Line 599: 12.5.2. Things to Look For
Line 600: Now let us assume that we are under significantly less time pressure, and so have time to really look
Line 601: into the test code. Here is the list of things we should be looking for.
Line 602: Basically, you should pay attention to the same code features as when code reviewing production
Line 603: code. Are the methods short and focused? Has the code been written at the right level of abstraction?
Line 604: Are there any global variables and magic numbers? And so on… In the subsections below, I will be
Line 605: trying to focus on test-related checks.
Line 606: Some of the hints below are written from the point of view of a technical team leader,
Line 607: responsible for ensuring the quality of all code. For example, analyzing trends in code
Line 608: coverage reports is probably not something you will be doing on a daily basis. Use
Line 609: common sense to create your own checklist of the issues to look for when code reviewing
Line 610: test code.
Line 611: Easy to Understand
Line 612:  A good unit test is easy to understand. But its readability can be spoilt by many small issues, which
Line 613: you should look out for.
Line 614:   A good test method has a content-revealing name, which gives information on the particular
Line 615: scenario implemented within it (see Section 10.2). Similarly, variables used in tests should be easy
Line 616: to understand: for example, can you tell which variable is an SUT and which are collaborators? Also,
Line 617: variables used within test code should inform you precisely about what their role is: are they here only
Line 618: to satisfy the API of the method being tested, or are they crucial to triggering some behaviour of the
Line 619: SUT or its collaborators? (see Section 12.6.3).
Line 620: Are the test methods short and focused? They should test a particular feature of the SUT (see Section
Line 621: 11.1), and nothing more. Look for anything that goes beyond just the simplest actions (arrange/act/
Line 622: assert).
Line 623: Can you find any for loops in the test methods, or instances of reflection being used to set up a test
Line 624: fixture? Both have some legitimate use, but usually cover up deficiencies in production code. Any
Line 625: violation of KISS should attract your attention.
Line 626: 17Please, do not take these values literally! They are only meant to be illustrative. See Section 12.3 for more information on desired
Line 627: code coverage levels.
Line 628: 243
Line 629: 
Line 630: --- 페이지 259 ---
Line 631: Chapter 12. Test Quality
Line 632: Look for hidden dependencies between tests - they make test code much harder to understand.
Line 633: Depending on the order of execution (which is not guaranteed by JUnit), or relying on data created by
Line 634: another test method, should both arouse your suspicions. Also global variables, reused between many
Line 635: test methods, should be treated as a code smell.
Line 636: Look for calls to some external APIs. Readability issues are often there, especially if called methods
Line 637: take many parameters. If you can not understand such code at a glance, then there is probably some
Line 638: room for improvement there (see Section 12.6.2).
Line 639: Are test classes inheriting from some parent class? How many levels of inheritance are there?
Line 640: Inheritance kills readability.
Line 641: A common issue is the mixing up of different styles within the codebase. Some developers value the
Line 642: arrange/act/assert pattern, some are more in favor of the BDD approach, some like to instantiate test
Line 643: doubles within test methods, while others prefer to rely on set-up methods for this, and so on. A good
Line 644: unit testing suite will be consistent in this respect, and while code reviewing you should also take a
Line 645: look at this. However, this is not something to be fixed easily, as it takes time for the team members to
Line 646: converge and agree on a common style, shared by all developers.
Line 647: Another thing which impacts negatively on readability is making use of custom solutions, instead of
Line 648: relying on what your own testing framework offers. If you find any non-standard approaches to setting
Line 649: up test fixtures (something different from the use of @BeforeXYZ annotations) or running test methods
Line 650: with different parameters (e.g. running tests in for loops instead of using parameterized tests - see
Line 651: Section 3.6), then by all means kick up a fuss about it.
Line 652: Similarly, you should take a look at the structure of the test classes. Does each particular part of the
Line 653: test class (e.g. data providers, private utility methods, set-up method, etc.) always appear in the same
Line 654: order? If not, this might be something to fix.
Line 655: The existence of duplicated code fragments might indicate that the "refactor" phase of the TDD cycle
Line 656: (see Section 4.2) is not being treated seriously. On the other hand, if the duplicated code helps to make
Line 657: the tests more readable, I would leave it alone. This is somewhat different from the situation with
Line 658: production code, where repeated code is almost always a code smell (see Section 12.6.6).
Line 659: Look at assertions. If a test fails, will you know exactly why? Are the right assertions being used? Are
Line 660: assertion messages clear? (see Section 9.4)
Line 661: If there is any logic involved (e.g. iteration over the collection returned by the SUT to find out if it
Line 662: contains certain values), then shouldn’t it perhaps be encapsulated within a custom matcher class?
Line 663: (See Section 6.1.)
Line 664: Test doubles are a common source of readability problems. Are the right ones being used? Are the
Line 665: expectations concerning executed methods clear? Is it clear what is verified and what is only stubbed?
Line 666: It is also common for maintainability issues to arise here. Look for overspecified tests (see Section
Line 667: 11.4.1). Are matchers used properly (see Section 7.7)?
Line 668: The creation of objects (see Section 10.6) can also be a weak point of tests. It is common to see a
Line 669: lot of copy&paste code in the test fixture setup parts of test classes, or to find many obscure private
Line 670: methods calling one another to set domain objects in certain states. Definitely something to have a
Line 671: look at.
Line 672: 244
Line 673: 
Line 674: --- 페이지 260 ---
Line 675: Chapter 12. Test Quality
Line 676: Documented
Line 677: Well-written unit tests usually do not need documentation (see Section 10.3). However, it sometimes
Line 678: transpires that you come across things which you wish had been documented, but are not. For
Line 679: example, the selection of test cases might not be obvious (e.g. "why is this method validated against
Line 680: Dubai and Sydney timezones?"). Probably there is some business explanation for this, which should
Line 681: be added as a comment (sometimes a link to bug tracker issue is all that is required). If it is not there,
Line 682: then you cannot determine whether the test cases are covering all the important scenarios.
Line 683: Are All the Important Scenarios Verified?
Line 684: The most important question to be answered is whether all the important test cases are covered by
Line 685: tests. Often you will find only single executions of tested methods, which is definitely not enough
Line 686: to verify their correctness (see Section 7.1). This is a sign of "happy path" testing, and definitely
Line 687: something to fight against.
Line 688: Another source of undertested code results from concurrency. If your code is intended to be accessed
Line 689: concurrently, then this is exactly how it should be tested. If not, then even 100% code coverage is
Line 690: nothing to be proud of.
Line 691: We have already discussed one area of code coverage usefulness for test code reviews (that is, its
Line 692: ability to uncover areas not touched by tests at all). However, more can be learned from studying the
Line 693: coverage report, even if the whole idea of measuring test code quality by looking at code coverage is
Line 694: flawed (see the discussion in Section 12.3).
Line 695: Study the coverage reports to find answers to the following questions (all of them can uncover
Line 696: potential issues):
Line 697: • Can you see a pattern of untested code across multiple classes? I often find that there are no
Line 698: tests for exceptions thrown. Usually this happens when real collaborators are used instead of test
Line 699: doubles, which makes it hard to simulate some possible paths of code execution.
Line 700: • If you happen to have historical data on executed tests (your continuous integration server should
Line 701: provide such reports), then see how the number of tests and code coverage measurements change.
Line 702: Ideally the number of tests should grow, and code coverage should at least fluctuate around the
Line 703: same values. If you see some different behaviour, you need to inspect it further.
Line 704: Additionally, you could apply mutation testing verification (see Section 12.4) to find weak spots in
Line 705: your tests.
Line 706: Run Them
Line 707: Some of the issues relating to running tests during code reviews have already been discussed.
Line 708: However, it is now time to have a closer look at them.
Line 709: Remember, always execute the tests which are under code review.
Line 710: Take a look at the build script. See if there are any conditions under which tests are not run (e.g.
Line 711: Maven profiles). Make sure the tests are not skipped.
Line 712: 245
Line 713: 
Line 714: --- 페이지 261 ---
Line 715: Chapter 12. Test Quality
Line 716: See how fast the tests run. If you find it unacceptably long, or notice some pauses during the execution
Line 717: of the tests, then look further, and answer the following questions:
Line 718: • Are these unit tests, or rather integration tests? Typically, setting up an application context or
Line 719: database connection takes time.
Line 720: • Are the setup methods used properly? Although this happens rarely with unit tests, do look to see
Line 721: whether some objects might, for example, be created before the class rather than just before each
Line 722: method (see Section 3.8.1).
Line 723: • Are there any deliberate Thread.sleep() calls? (See the next section for some discussion).
Line 724: Also, look at the messages printed during the execution of the tests (usually on the console). If you
Line 725: cannot keep up with them, it means you have a Loudmouth issue (see Section 9.5).
Line 726: Make sure the tests are repeatable. Usually they are, but in cases of multithreading tests or tests with
Line 727: random values, this might not be the case.
Line 728: Date Testing
Line 729: Experience tells me that the testing of time-dependent business logic is rarely done correctly (see
Line 730: Section 7.9). Common issues you should look for are the following:
Line 731: • Look for any Thread.sleep() code constructs which make unit tests run longer than is really
Line 732: required.
Line 733: • A common mistake is to test only the current date, which means the bug will be discovered exactly
Line 734: on the day the code fails in production. In general you need to make sure all test cases are covered.
Line 735: 12.5.3. Conclusions
Line 736: Of the many approaches to ensuring the quality of your test code, code reviews are to be
Line 737: recommended the most strongly. They help to find bugs, help your team to converge with respect
Line 738: to how they all go about coding, and serve to disseminate knowledge amongst team members about
Line 739: parts of the software being developed. Moreover, by examining the test code, a lot can be discovered
Line 740: about production code. Frankly, what more could one ask for? The only downside is that to perform a
Line 741: thorough examination of test code, a lot of time is required.
Line 742: I strongly recommend making test code reviews a part of your team’s working routine. Code reviews
Line 743: should belong to your Definition of Done, and they should embrace test code in the same manner that
Line 744: they embrace production code.
Line 745: 12.6. Refactor Your Tests
Line 746: God grant me serenity to accept the code I cannot change, courage to change the code I
Line 747: can, and wisdom to know the difference.
Line 748: — Erik Naggum
Line 749: Now that we know in what ways we can measure test quality, it is time to actually fix the deficiencies
Line 750: uncovered by code coverage (see Section 12.3), mutation testing (see Section 12.4) and code reviews
Line 751: 246
Line 752: 
Line 753: --- 페이지 262 ---
Line 754: Chapter 12. Test Quality
Line 755: (see Section 12.5). In this section we discuss the process of refactoring, which is a common way of
Line 756: altering code. We have already discussed a refactoring in Chapter 4, Test Driven Development, as one
Line 757: of the phases of the TDD rhythm. In this section we shall discuss the refactorings that are common
Line 758: when working with tests. Some of them are identical to the ones we perform on production code, but
Line 759: some are specific to test code.
Line 760: Numerous examples of making improvements to test code by introducing changes of various sorts
Line 761: have been given already in other parts of this book – or, indeed, are easily deducible from what has
Line 762: been discussed earlier. For example, we already decided to use fluent assertions instead of the ones
Line 763: provided by JUnit (for the reasons explained in Appendix B, Fluent Assertions). We also discussed
Line 764: how the use of data providers (instead of for loops), or having specialized setUp() methods, can
Line 765: also serve as a refactoring hints. This section supplements what has already been discussed with new
Line 766: examples and approaches that have yet to be examined.
Line 767: Before we see some code, let us think about the reasons for test code refactorings. The first and most
Line 768: significant one is that the test code is very important and should be cleaned so that it is easy to
Line 769: understand and maintain. Refactoring helps you achieve this. By introducing various, sometimes
Line 770: minor, changes to test code, you can make your tests convey better exactly what you are trying to test.
Line 771: If a well-written test fails, it is also easier to find out why.
Line 772: There is also a question about how to refactor test code. The situation is different from that with
Line 773: production code, because we do not have tests for our tests. However, we can deal with this issue by
Line 774: following these simple pieces of advice:
Line 775: • You should perform refactorings in small steps, and rerun tests often along the way.
Line 776: • Additional tools - code coverage and mutation testing - may help to find out if your safety net of
Line 777: tests is not getting loosened up.
Line 778: Some people say that before starting to refactor tests, you should first change the SUT’s
Line 779: implementation, so the test fails18. After refactoring tests and rerunning them, you should still see
Line 780: them failing - which is a sign that the assertions are still working. Now, when you revert the changes
Line 781: in production code, the tests should pass again. I have to admit, I have never used the last technique
Line 782: during any serious refactoring. Moving in small steps worked well enough for me.
Line 783: Another thing we should discuss is when to refactor a particular test. An obvious moment for this
Line 784: is the refactoring phase of the TDD rhythm, but this is not the only one. In fact, I would encourage
Line 785: you to do it every time you do not feel comfortable when browsing the test code. It does not matter if
Line 786: you have written that code yourself or not. Remember the Boy Scout Rule ("Leave the campground
Line 787: cleaner than you found it!") and dare to make the small changes which, added together, still make a
Line 788: big difference!
Line 789: Before we see some examples, let me inform you that all of them involve real code. Some names of
Line 790: methods and classes have been changed to "protect the innocent". :)
Line 791: The examples are only big enough to demonstrate what is to be done, and how the code changes after
Line 792: refactoring. Each of the refactorings shown addresses some real issues within the test code. Some
Line 793: of them might not seem very dangerous when looking at ten lines of test code examples, but their
Line 794: importance will grow along with the size of your test codebase. Likewise, the benefits of refactorings
Line 795: 18Please note that this approach is exactly the opposite of what you do when refactoring production code, which should be
Line 796: performed only if all tests are green.
Line 797: 247
Line 798: 
Line 799: --- 페이지 263 ---
Line 800: Chapter 12. Test Quality
Line 801: are much more clearly visible when they are introduced for real-sized test classes. Please bear this in
Line 802: mind when contemplating the examples in this section.
Line 803: 12.6.1. Use Meaningful Names - Everywhere
Line 804:   We have already discussed the importance of good naming. We have discussed various patterns for
Line 805: test class names and test method names, and pondered over the naming schema for test doubles (see
Line 806: Section 10.2). Throughout the book I have been encouraging you to rename things if you do not feel
Line 807: comfortable with the existing names. Good, meaningful names are invaluable!
Line 808: This section presents another facet of the same issue. It shows how the simple refactoring of renaming
Line 809: variables can make it easier to understand the logic of test code.
Line 810: Imagine a test of a class from a security module, which is supposed to allow or deny access to users
Line 811: based on their permissions. First the test registered users (identified by string id) and assigned them
Line 812: some permissions. Then it verified that users had only those permissions that had been assigned to
Line 813: them. Listing 12.6 shows a small part of this test.
Line 814: Listing 12.6. User_1, user_2, user_3 - who are you?
Line 815: @ParameterizedTest
Line 816:     @CsvSource({ 
Line 817:             "user_1, READ", "user_1, WRITE", "user_1, REMOVE",
Line 818:             "user_2, WRITE", "user_2, READ",
Line 819:             "user_3, READ"
Line 820:     })
Line 821:     void shouldReturnTrueIfUserHasPermission(
Line 822:             String username, Permission permission) {
Line 823:         assertThat(sut.hasPermission(username, permission)).isTrue();
Line 824:     }
Line 825: A nice example of automatic conversion performed by JUnit (see Section 7.11.3), which is smart
Line 826: enough to convert a String into enum of Permission type.
Line 827: The problem here is that this test is not obvious. For someone who looks at the test for the first time,
Line 828: it is not obvious whether user_2 should or should not have been granted the READ permission. Who
Line 829: the heck is user_2? Well, this must be checked by analyzing the data of previously registered users
Line 830: (probably in a setUp() method somewhere).
Line 831: A simple change can achieve wonders as the next listing shows.
Line 832: Listing 12.7. Admin, logged on user, guest - I know who you are!
Line 833: @ParameterizedTest
Line 834: @CsvSource({
Line 835:         "admin, READ", "admin, WRITE", "admin, REMOVE",
Line 836:         "logged, WRITE", "logged, READ",
Line 837:         "guest, READ"
Line 838: })
Line 839: void shouldReturnTrueIfUserHasPermission(
Line 840:         String username, Permission permission) {
Line 841:     assertThat(sut.hasPermission(username, permission)).isTrue();
Line 842: }
Line 843: 248
Line 844: 
Line 845: --- 페이지 264 ---
Line 846: Chapter 12. Test Quality
Line 847: Now this is clear! Admin should have all possible permissions. A "normal" logged on user should
Line 848: be able to read and write, but not to remove things. A guest user can normally only see what others
Line 849: have uploaded, but cannot change the content himself or herself. There is no need to consult any
Line 850: documentation: the code speaks for itself.
Line 851: 12.6.2. Make It Understandable at a Glance
Line 852:   The readability of tests can be improved in lots of ways. Take a look at the following snippet of test
Line 853: code, which creates an object of the MockServer class:
Line 854: Listing 12.8. Not easy to understand what type of server is created
Line 855: server = new MockServer(responseMap, true,
Line 856:         new URL(SERVER_ROOT).getPort(), false);
Line 857: What properties does a server variable have? What kind of server is created? If you do not remember
Line 858: the API of MockServer, then you need to ask your IDE for help, so it explains the meaning of true
Line 859: and false flags being passed to the MockServer constructor. Would it be possible to change this code
Line 860: so it is easier to understand? Yes, by introducing some values whose names tell a story:
Line 861: Listing 12.9. Self-explanatory values passed to the MockServer constructor
Line 862: private static final boolean NO_SSL = false;
Line 863: private static final boolean RESPONSE_IS_A_FILE = true;
Line 864: server = new MockServer(responseMap, RESPONSE_IS_A_FILE,
Line 865:         new URL(SERVER_ROOT).getPort(), NO_SSL);
Line 866: Now this makes more sense - this server responds with a file, and does not use SSL.
Line 867: Another way in which this code could be made more readable is by using the Test Data
Line 868: Builder pattern (see Section 10.6.2).
Line 869: 12.6.3. Make Irrelevant Data Clearly Visible
Line 870:   If I can change a value without changing the result of the behavior I want to check,
Line 871: then I call that irrelevant data for this test.
Line 872: — J. B. Raisenberg
Line 873: A very frequently performed refactoring consists of changing variable names, and also their values,
Line 874: so that both of these properly reflect their purpose. This is something we have already done in some
Line 875: places when discussing other unit testing issues, but now it is time to take a closer look at this.
Line 876: This section opens with a quote from J. B. Rainsberger – one that defines a heuristic for recognizing
Line 877: a certain type of (unimportant) test value which should be distinguished clearly from important ones.
Line 878: The following snippet of code illustrates this:
Line 879: Listing 12.10. Not clear what is important
Line 880: @Test
Line 881: 249
Line 882: 
Line 883: --- 페이지 265 ---
Line 884: Chapter 12. Test Quality
Line 885: void kidsNotAllowed() {
Line 886:     Person kid = new Person("Johnny", "Mnemonic");
Line 887:     kid.setAge(12);
Line 888:     assertThat(kid.isAdult())
Line 889:             .as(kid + " is a kid!")
Line 890:             .isFalse();
Line 891: }
Line 892: There is nothing wrong with this test method, except that it is not clear whether firstname and
Line 893: lastname are of any importance to the logic being tested. This can be fixed by giving them values
Line 894: which make them convey the message explicitly: "we are not important, you should not care about
Line 895: us". The code below illustrates how this can be achieved:
Line 896: Listing 12.11. Irrelevant data clearly visible
Line 897: @Test
Line 898: void kidsNotAllowed() {
Line 899:     Person kid = new Person("ANY_NAME", "ANY_SURNAME");
Line 900:     kid.setAge(12);
Line 901:     assertThat(kid.isAdult())
Line 902:             .as(kid + " is a kid!")
Line 903:             .isFalse();
Line 904: }
Line 905: I usually use an ANY_ prefix, and capital letters only - but this is just one possible instance
Line 906: of how one might do this. Find something which looks good for you.
Line 907: Apart from reading the test code more easily, another advantage is that if the test fails, the error
Line 908: message will also clearly show what is important:
Line 909: Listing 12.12. Error message shows what is irrelevant
Line 910: org.opentest4j.AssertionFailedError:
Line 911: [Person{firstname='ANY_NAME', lastname='ANY_SURNAME', age=12} is a kid!]
Line 912: In the event of a value like this being used repeatedly in multiple test methods, I would suggest
Line 913: extracting it as a constant (as you should always do), as well as naming it appropriately:
Line 914: Listing 12.13. Irrelevant data expressed by both variable names and values
Line 915: private static final String ANY_NAME = "ANY_NAME";
Line 916: private static final String ANY_SURNAME = "ANY_SURNAME";
Line 917: @Test
Line 918: void kidsNotAllowed() {
Line 919:     Person kid = new Person(ANY_NAME, ANY_SURNAME);
Line 920:     kid.setAge(12);
Line 921:     assertFalse(kid + " is a kid!", kid.isAdult());
Line 922: }
Line 923: This renaming of constants is especially important for values other than String, so you can have
Line 924: variables like: ANY_VALID_POST_CODE, ANY_NUMBER, ANY_DATE, etc.
Line 925: 250
Line 926: 
Line 927: --- 페이지 266 ---
Line 928: Chapter 12. Test Quality
Line 929: In fact, there is no need to wait for the refactoring phase to make irrelevant data clearly visible. When
Line 930: writing a test you should be clear in your mind about which data is important for the scenario you are
Line 931: covering with that test. This is probably the best time to introduce names of variables and values along
Line 932: the lines discussed in this section.
Line 933: 12.6.4. Do not Test Many Things at Once
Line 934:  The tests we have written so far have been pretty focused: they have verified only one thing.
Line 935: However, it often happens that this is not the case. An example of a test which verifies more than a
Line 936: decent test should is presented below.
Line 937: Listing 12.14. Testing two scenarios at once
Line 938: import org.junit.jupiter.params.ParameterizedTest;
Line 939: import org.junit.jupiter.params.provider.Arguments;
Line 940: import org.junit.jupiter.params.provider.MethodSource;
Line 941: import java.util.stream.Stream;
Line 942: import static org.junit.jupiter.params.provider.Arguments.of;
Line 943: public class PhoneSearchTest {
Line 944:     public static Stream<Arguments> data() {
Line 945:         return Stream.of(
Line 946:                 of("48", true), of("+48", true),
Line 947:                 of("++48", true), of("+48503", true),
Line 948:                 of("+4", false), of("++4", false),
Line 949:                 of("", false), of(null, false),
Line 950:                 of("  ", false)
Line 951:         );
Line 952:     }
Line 953:     @ParameterizedTest
Line 954:     @MethodSource(value = "data")
Line 955:     void testPrefixVerification(String prefix, boolean expected) {
Line 956:         PhoneSearch ps = new PhoneSearch(prefix);
Line 957:         assertThat(ps.isValid()).isEqualTo(expected);
Line 958:     }
Line 959: }
Line 960: The problems with this test are the following:
Line 961: • When it fails, it will not be instantly clear which feature is not working. Is the PhoneSearch class
Line 962: able to recognize valid prefixes? Is it able to reject invalid prefixes? Which one of these two works,
Line 963: and which does not?
Line 964: • The name of the test method (testPrefixVerification()) is too generic. What exactly is being
Line 965: tested? Likewise, the name of the data provider method (data()) does not reveal its intent clearly
Line 966: enough.
Line 967: • The test is more complicated than it should be: it uses a boolean flag parameter to decide whether
Line 968: the assertion should pass or fail. This amounts to introducing a form of logic into the test code -
Line 969: something which, as we discussed in Section 11.2, is very bad indeed!
Line 970: 251
Line 971: 
Line 972: --- 페이지 267 ---
Line 973: Chapter 12. Test Quality
Line 974: You can see the refactored version of this test in the next two listings:
Line 975: Listing 12.15. Refactored test - testing valid prefixes
Line 976: @ParameterizedTest
Line 977: @ValueSource(strings = { "48", "48123", "+48", "++48", "+48503" })
Line 978: void shouldRecognizeValidPrefixes(String validPrefix) {
Line 979:     PhoneSearch ps = new PhoneSearch(validPrefix);
Line 980:     assertThat(ps.isValid()).isTrue();
Line 981: }
Line 982: Listing 12.16. Refactored test - testing invalid prefixes
Line 983: public static Stream<String> invalidPrefixes() {
Line 984:     return Stream.of("+4", "++4", "", null, "  ");
Line 985: }
Line 986: @ParameterizedTest
Line 987: @MethodSource(value = "invalidPrefixes")
Line 988: void shouldRejectInvalidPrefixes(String invalidPrefix) {
Line 989:     PhoneSearch ps = new PhoneSearch(invalidPrefix);
Line 990:     assertThat(ps.isValid()).isFalse();
Line 991: }
Line 992: This version of the test differs in the following respects:
Line 993: • There are two test methods now - one verifies whether the SUT accepts valid prefixes, the other
Line 994: whether the SUT rejects invalid prefixes.
Line 995: • The boolean flag has been removed.
Line 996: • isEqualTo() assertions has been replaced with more intention-revealing ones - isTrue() and
Line 997: isFalse().
Line 998: • Each test method has its own data provider - a @ValueSource or a @MethodSource.
Line 999: • The names of all methods, including data providing method, have been updated so they are more
Line 1000: intention-revealing.
Line 1001: Even if the test has grown in length, it seems to be of higher quality now. When looking at the test
Line 1002: code it is easier to deduce "what are the prefixes that PhoneSearch accepts?", so the documentation
Line 1003: aspect has also been improved. Likewise, if this test fails, you will know which part of the SUT’s code
Line 1004: needs to be fixed.
Line 1005: 12.6.5. Change Order of Methods
Line 1006: In order to improve the readability of tests, I often rearange the order of methods so they are
Line 1007: consistent across many tests. This is a simple refactoring, which introduces no risk of breaking
Line 1008: anything. The gain is that it is much easier to browse test code, because you always know where to
Line 1009: expect certain things. In my example, all test classes have the following structure:
Line 1010: • private fields,
Line 1011: 252
Line 1012: 
Line 1013: --- 페이지 268 ---
Line 1014: Chapter 12. Test Quality
Line 1015: • data providers,
Line 1016: • set-up methods,
Line 1017: • test methods,
Line 1018: • private methods.
Line 1019: I rarely deviate from this pattern. Only occasionally do I move a data provider method next to the test
Line 1020: method which uses it (but especially if only one test method uses this data provider).
Line 1021: You can usually impose the structure you want while writing the tests. There is no need to wait for the
Line 1022: refactoring phase to do this.
Line 1023: 12.6.6. Do not Go Too Far
Line 1024: The goal of refactoring unit tests is slightly different from refactoring mainline code.
Line 1025: For the latter, your goal is to modularize the codebase and eliminate tightly coupled
Line 1026: relationships. For unit tests, those goals are secondary to creating simple, human-
Line 1027: readable tests.
Line 1028: — Keith D Gregory
Line 1029:  You might have noticed that so far we have not discussed some very popular refactorings that we use
Line 1030: quite often when working with production code. For example, we have not even mentioned Extract
Line 1031: Method19 refactoring, which seems to be the most popular (and probably the most powerful) of all.
Line 1032: There is a good reason for this, which we shall now discuss.
Line 1033: In general, code redundancy is a bad thing. In the course of the book so far, we have on several
Line 1034: occasions discussed the importance of the DRY principle (and not without good reason). However,
Line 1035: things are not so black-and-white when it comes to test code. As was discussed previously, test code
Line 1036: should be as simple as possible. It should be readable, and free of any logic, so it does not contain any
Line 1037: bugs, and can serve as a living documentation of the production code. Because of these expectations,
Line 1038: some refactorings well-suited to production code ought to be considered less useful for test code.
Line 1039: Sometimes it is very easy (and thus tempting!) to make the test code more concise by grouping things
Line 1040: within a private utility helper method20. If there are one or two methods like this in a test class,
Line 1041: it is not so bad. However, I have witnessed a lot of really unreadable test code, which required me
Line 1042: to jump through many tangled private methods to understand any one single test method. This is
Line 1043: unacceptable. What is still more horrific is the use of template methods and abstract test classes,
Line 1044: which, in conjunction with such utility methods, can make test classes completely unreadable.
Line 1045: In production code, you can almost always bet on DRY and win. In the case of test code, you need to
Line 1046: strike a balance between the DRY principle and the expressiveness of tests.
Line 1047: I have to admit that many people see it differently. I have read many blog posts which promote
Line 1048: excessive use of private helper methods, and test class hierarchies. My point of view is different, and
Line 1049: I would encourage you to follow the advice given above. However, as usual, any real knowledge will
Line 1050: only come with experience, so do not be afraid to experiment a little bit with different approaches and
Line 1051: find out what works for you.
Line 1052: 19See http://martinfowler.com/refactoring/catalog/extractMethod.html
Line 1053: 20We have already touched the topic while discussing the custom matchers in Section 6.1.1
Line 1054: 253
Line 1055: 
Line 1056: --- 페이지 269 ---
Line 1057: Chapter 12. Test Quality
Line 1058: 12.7. Conclusions
Line 1059: In this chapter we have worked hard to determine precisely how to measure and improve test
Line 1060: quality. As developers, we love tools which can do something for us, and that is why we started
Line 1061: out with a discussion of various tools - static code analyzers (see Section 12.2), code coverage (see
Line 1062: Section 12.3) and mutation testing (see Section 12.4). We discovered what, exactly, they are good at
Line 1063: when it comes to helping us achieve high-quality tests, but also realized how very inadequate they are.
Line 1064: Then we turned towards code reviews (see Section 12.5), and found these to be a great way of
Line 1065: uncovering the weak spots in our test code. Alas, code reviews take time, and what is more, not all
Line 1066: developers perform them well enough. Some developers lack knowledge about what to look for, some
Line 1067: do not treat test code with enough respect to bother analyzing it, and some are not allowed to "waste"
Line 1068: their precious time on such unproductive activities (no comment…). Finally, we discussed various
Line 1069: refactorings (see Section 12.6) that could be implemented so that our tests will be more readable and
Line 1070: more easily maintained.
Line 1071: Several times in this chapter I have sought to highlight the various issues relating to achieving high-
Line 1072: quality tests. The picture I have tried to create is one in which having really good tests is definitely
Line 1073: possible, but is also something that calls for full commitment on your part. The tools can assist you
Line 1074: with this task, but they play only a secondary role.
Line 1075: In conclusion, here is a list of "action points" which should help you achieve the goal of high-quality
Line 1076: tests:
Line 1077: • Treat test quality as the number-one issue from the very outset.
Line 1078: • Take the refactoring phase of TDD very seriously.
Line 1079: • Test code should undergo a code review in the same way that production code does. You need
Line 1080: someone other than yourself to take a critical look at your tests.
Line 1081: • "Do not live with broken windows"21 - bad things tend to get copied, and soon you will have much
Line 1082: more to clean than you can handle. Never delay fixing them.
Line 1083: • Think hard about the test cases required (see Section 7.1) and follow the TDD approach in order
Line 1084: to cover all important functionalities with tests. This is much more important than trying to satisfy
Line 1085: requirements with respect to the measuring of code coverage!
Line 1086: • Use code coverage to uncover untested areas.
Line 1087: • Adhere to the various forms of programming best practice - e.g. the SRP principle and short
Line 1088: focused methods. These apply to test code as well.
Line 1089: • Be consistent about the naming and structure of your tests.
Line 1090: 21See http://www.artima.com/intv/fixitP.html for a good explanation of this statement.
Line 1091: 254
Line 1092: 
Line 1093: --- 페이지 270 ---
Line 1094: Chapter 12. Test Quality
Line 1095: 12.8. Exercises
Line 1096: "Quality is free" they say22, but one has to work really hard to achieve it. The single exercise in this
Line 1097: section is intended to help you appreciate this simple fact.
Line 1098: 12.8.1. Clean this Mess
Line 1099: The listing below presents a naive implementation of the Fridge class. It allows one to put food into
Line 1100: the fridge, take it out, and inspect it to see whether something is in there.
Line 1101: Listing 12.17. Fridge implementation
Line 1102: public class Fridge {
Line 1103:     private Collection<String> food = new HashSet<String>();
Line 1104:     public boolean put(String item) {
Line 1105:         return food.add(item);
Line 1106:     }
Line 1107:     public boolean contains(String item) {
Line 1108:         return food.contains(item);
Line 1109:     }
Line 1110:     public void take(String item) throws NoSuchItemException {
Line 1111:         boolean result = food.remove(item);
Line 1112:         if (!result) {
Line 1113:             throw new NoSuchItemException(item
Line 1114:                 + " not found in the fridge");
Line 1115:         }
Line 1116:     }
Line 1117: }
Line 1118: The next two listings show test code of the Fridge class, which - after everything we have explored
Line 1119: up to now, and taking a mere glance at the code - we can say is a complete mess! It works, which
Line 1120: means it tests some features of the SUT, but it could have been much better written. I hope to never
Line 1121: see anything like this again in the rest of my life. Anyway, your task for now is to clean this mess!
Line 1122: Use the knowledge of high-quality testing you have gained from this chapter, but also refer to the
Line 1123: examples given previously, in order to rewrite this test! For example, you should probably take care
Line 1124: of:
Line 1125: • the proper naming of test classes, methods and variables,
Line 1126: • the use of parameterized tests,
Line 1127: • duplicated code,
Line 1128: • and many more issues that are hidden there.
Line 1129: Make sure you do not loose any test case by redesigning this test class!
Line 1130: The two test methods of the FoodTesting class are shown below:
Line 1131: 22See http://www.wppl.org/wphistory/PhilipCrosby/QualityIsFreeIfYouUnderstandIt.pdf
Line 1132: 255
Line 1133: 
Line 1134: --- 페이지 271 ---
Line 1135: Chapter 12. Test Quality
Line 1136: Listing 12.18. testFridge() method
Line 1137: @Test
Line 1138: void testFridge() {
Line 1139:     Fridge fridge = new Fridge();
Line 1140:     fridge.put("cheese");
Line 1141:     assertEquals(true, fridge.contains("cheese"));
Line 1142:     assertEquals(false, fridge.put("cheese"));
Line 1143:     assertEquals(true, fridge.contains("cheese"));
Line 1144:     assertEquals(false, fridge.contains("ham"));
Line 1145:     fridge.put("ham");
Line 1146:     assertEquals(true, fridge.contains("cheese"));
Line 1147:     assertEquals(true, fridge.contains("ham"));
Line 1148:     try {
Line 1149:         fridge.take("sausage");
Line 1150:         fail("There was no sausage in the fridge!");
Line 1151:     } catch (NoSuchItemException e) {
Line 1152:         // ok
Line 1153:     }
Line 1154: }
Line 1155: Listing 12.19. testPutTake() method
Line 1156: @Test
Line 1157: void testPutTake() throws NoSuchItemException {
Line 1158:     Fridge fridge = new Fridge();
Line 1159:     List<String> food = new ArrayList<String>();
Line 1160:     food.add("yogurt");
Line 1161:     food.add("milk");
Line 1162:     food.add("eggs");
Line 1163:     for (String item : food) {
Line 1164:         fridge.put(item);
Line 1165:         assertEquals(true, fridge.contains(item));
Line 1166:         fridge.take(item);
Line 1167:         assertEquals(false, fridge.contains(item));
Line 1168:     }
Line 1169:     for (String item : food) {
Line 1170:         try {
Line 1171:             fridge.take(item);
Line 1172:             fail("there was no " + item + " in the fridge");
Line 1173:         } catch (NoSuchItemException e) {
Line 1174:             assertEquals(true, e.getMessage().contains(item));
Line 1175:         }
Line 1176:     }
Line 1177: }
Line 1178: 256