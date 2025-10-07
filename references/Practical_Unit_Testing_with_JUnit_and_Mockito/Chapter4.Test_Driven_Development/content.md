Line 1: 
Line 2: --- 페이지 54 ---
Line 3: Chapter 4. Test Driven Development
Line 4: At the beginning of testing, things were simple. You wrote code, then you wrote tests to verify
Line 5: its validity. This seemed to be reasonable and brought good results. However after some time a
Line 6: few troublemakers ;) decided to turn things on their heads, and insisted on writing tests before
Line 7: implementation. This rather surprising idea got quite popular, and is claimed to bring even better
Line 8: results.
Line 9: Initially, writing tests before writing the actual code was a way to verify it as soon as possible. As
Line 10: more and more people started to follow the test-first approach, they soon discovered that immediate
Line 11: verification is only a part of what you gain when writing tests first (and maybe not even the most
Line 12: important part). It turned out that thinking about the tests before any implementation has actually
Line 13: been written is a powerful design technique. Code not only worked better (thanks to being thoroughly
Line 14: tested), but also "looked and felt" better, in terms of its architecture, maintainability, and API ease of
Line 15: use.
Line 16: Thus, test-first is now rather called Test Driven Development (TDD)1. There is still some discussion
Line 17: regarding the relation of TDD and test-first. However, it seems that the general understanding of these
Line 18: terms is that they really mean the same. Because of this, I will alternate between using one or other of
Line 19: the two terms throughout the book.
Line 20: This book concentrates on testing aspects, even though you will get a decent dose of the
Line 21: TDD approach here. The best book on TDD that I know of is [freeman2009]. However, I
Line 22: would suggest that you gain some experience in testing techniques before you start reading
Line 23: it. And, by the way, even though it is really great, it won’t "teach" you TDD. Practice,
Line 24: practice, practice!
Line 25: In this section we are going to take a closer look at what it means to write tests before implementation.
Line 26: Apart from giving some theoretical background, we will concentrate on practice. One important thing
Line 27: to remember is that even though the test-first approach will be demonstrated solely on unit tests, this
Line 28: does not mean that the applicability of TDD is confined to this particular kind of test! On the contrary,
Line 29: this approach can (and should) be used on every testing level.
Line 30: But first, let us consider various answers to the following question: "when to write tests?".
Line 31: 4.1. When to Write Tests?
Line 32: In the previous paragraphs, we have already mentioned two answers to this question:
Line 33: • write tests after implementation (test-last AKA code-first),
Line 34: • write tests before implementation (test-first).
Line 35: Obviously, they are contradictory. However, it is possible to use both of them for the whole coding
Line 36: process, choosing the more suitable one for each implementation task or code part.
Line 37: In spite of being a huge supporter of the TDD approach, in Section 4.7 I will discuss some
Line 38: reasons for choosing test-last over test-first.
Line 39: 1It is also called Test Driven Design, which stresses the design aspect of this technique.
Line 40: 39
Line 41: 
Line 42: --- 페이지 55 ---
Line 43: Chapter 4. Test Driven Development
Line 44: But there is yet another answer to the "when to write tests?" question, which complements the two
Line 45: given previously: "write a test every time a bug is found". Let us describe each approach in more
Line 46: detail.
Line 47: 4.1.1. Test Last (AKA Code First) Development
Line 48: In the "test last" approach, tests are written after the production code has been finished. It is
Line 49: a traditional approach to testing, predating the more recent "test first" approach.
Line 50: Writing the tests after the code has advantages and disadvantages. The main advantage is that the tests
Line 51: are written when the functionality of the tested object is well understood. The main disadvantage is
Line 52: that the developer concentrates on testing the implementation (which he/she wrote only a few minutes
Line 53: earlier) instead of testing the interface (behaviour) of the SUT. This can lead to tests which:
Line 54: • are tightly coupled to the implementation (and as such will need to be rewritten every time it
Line 55: changes),
Line 56: • encourage developers to (sub)consciously select the sort of test cases they expect to pass
Line 57: successfully.
Line 58: Additionally, when using the "test last" approach there is always a temptation to not write tests at
Line 59: all. Why bother, if you are pretty sure the code works as expected? Why bother, if you have run the
Line 60: thing and seen for yourself that the log messages are exactly as you wanted them to be? It requires a
Line 61: lot of self-discipline to write tests after you have a working code. And when the deadline comes, the
Line 62: temptation to save some time by avoiding this extra, seemingly unnecessary step, will grow. In my
Line 63: opinion, this is a serious reason to follow the test-first approach.
Line 64: In some cases, i.e. when working with legacy code, the "test last" approach is the only possible one, as
Line 65: the code already exists.
Line 66: 4.1.2. Test First Development
Line 67: This whole chapter is devoted to "test first" development, so let us start with a brief description of its
Line 68: most important characteristics.
Line 69: Writing the tests before the actual code makes developers think about the behaviour of the tested
Line 70: object as opposed to its implementation (which does not exist at this point). It cuts down the
Line 71: functionality of each implemented class to the bare minimum determined by the test cases - no
Line 72: superfluous functionalities are added. It also results in a very high (if not 100%) level of code
Line 73: coverage (see Section 12.3), which, in general, is desirable.
Line 74: This approach can be applied to any level of testing. In particular, it is very popular for and suited to
Line 75: unit tests.
Line 76: 4.1.3. Always after a Bug is Found
Line 77: The first thing you should do after a bug has been found is to restrain your natural urge to fix it right
Line 78: away. If you fix it "just like that", you lose an opportunity to get rid of it once and for all. The bug
Line 79: may reappear later (because someone reverts the changes, for example when fixing another bug). If
Line 80: you write a test before fixing it, you will strengthen your safety net of tests, and the same bug will not
Line 81: come back.
Line 82: 40
Line 83: 
Line 84: --- 페이지 56 ---
Line 85: Chapter 4. Test Driven Development
Line 86: So, no matter if you code test-first or test-last, you should write a test immediately after a bug is
Line 87: encountered. The test should expose the bug, that is, it should expect the right thing to happen, and at
Line 88: first it should fail, thus repeating the observed buggy behaviour. Later on, you should fix the code so
Line 89: the test passes.
Line 90: If you think about it, you will realize that writing a test after a bug has been found amounts to a
Line 91: test-first approach. You write a test which fails (because you want to mimic the bug), and then you
Line 92: implement the code which satisfies the failing test (which, in the case of a bug, means you fix it).
Line 93: The big issue here is to pinpoint the bug precisely, so that you are able to write a unit test which
Line 94: exposes it. This might be really tricky. It may be that multiple bugs are turning up in your business
Line 95: logic in the course of your clicking the UI of your application. It is not so easy to tell exactly which
Line 96: class is responsible for some particular bit of erroneous behaviour. This is usually solved by first
Line 97: writing a higher-level test (i.e. an end-to-end test), and then gradually gathering information on the
Line 98: cause, narrowing the search field by writing more focused tests: first integration, and then eventually
Line 99: unit, tests.
Line 100: 4.2. TDD Rhythm
Line 101: The nice thing about test-first coding is that it consists of a few very simple steps repeated over and
Line 102: over again. And – which comes as quite a surprise the first time one encounters it – these simple steps
Line 103: lead to a great coding experience and great results. Pure magic, isn’t it?
Line 104: Now, I would like you to take a look at Figure 4.1. This picture is simplified. It does not tell the whole
Line 105: truth. We will enhance it further to include some more details. Yet, this is THE picture that should
Line 106: hang over your desk2. It gives you the rhythm of your work:
Line 107: 1. Write a test that fails (RED).
Line 108: 2. Make the code work (GREEN).
Line 109: 3. Eliminate redundancy (REFACTOR).
Line 110: It also gives you a simple rule to follow: never write code without a failing test!
Line 111: Figure 4.1. The most important picture
Line 112: 2If I had to choose one thing that I would like you to remember from this book, it would be this picture!
Line 113: 41
Line 114: 
Line 115: --- 페이지 57 ---
Line 116: Chapter 4. Test Driven Development
Line 117: The next picture - Figure 4.2 - gives some more insight into the TDD rhythm. It shows how you start
Line 118: with a list of tests, choose one of them, and then follow the red-green-refactor cycle, making sure you
Line 119: end up with green.
Line 120: The whole work is finished (i.e. some particular functionality is implemented), when there are no
Line 121: more tests to be written.
Line 122: Figure 4.2. TDD rhythm explained
Line 123: In the following sections we shall discuss each element of the TDD rhythm in details.
Line 124: Baby steps
Line 125: TDD means moving in baby steps. Writing a test. Running all tests and seeing the new one
Line 126: fail. Fixing it. Rerunning all tests. Seeing the new test pass. Refactoring. Rerunning all tests.
Line 127: Seeing the new test pass. Repeating the whole cycle again, again, and again.
Line 128: Every turn of TDD circle means one more functionality is working now. Every step is a small
Line 129: accomplishment.
Line 130: Each step is small and seemingly insignificant, but they sum up to working application and
Line 131: high-quality, thoroughly tested code.
Line 132: 4.2.1. RED - Write a Test that Fails
Line 133: Think about some functionality that should be implemented and write it down in the form of a test.
Line 134: This functionality is not yet implemented, so the test will inevitably fail. At this point, failing is okay.
Line 135: More than that: it is desirable! Now you know that:
Line 136: • the functionality really does not work,
Line 137: • once it is implemented, you will see it, because test result will turn from red to green.
Line 138: At first, you might feel awkward when writing tests for something which is not even there. It requires
Line 139: a slight change to your coding habits, but after a while, you will come to see it as a great design
Line 140: opportunity. Your test is the first client of this newly born API, and this gives you a chance to create
Line 141: an API that is convenient for all clients to use.
Line 142: 42
Line 143: 
Line 144: --- 페이지 58 ---
Line 145: Chapter 4. Test Driven Development
Line 146: This is what TDD is really all about: the design of an API.
Line 147: When thinking like a client of your own soon-to-be-written code, you should concentrate on what
Line 148: is really required. You need to ask questions like: "do I really need this getter that returns this
Line 149: collection, or would it be more convenient to have a method which returns the biggest element of this
Line 150: collection?". And you need to answer such questions by writing tests. This book is not devoted to
Line 151: API design, but even if we were to just scratch the surface of this topic, it could entail a revolutionary
Line 152: change in your coding style. No more unnecessary methods, written because "they might just possibly
Line 153: be useful for someone someday", no more auto-generated getters/setters, when an immutable class is
Line 154: much more appropriate.
Line 155: Concentrate on what the client (the test code) really needs. And write tests which test
Line 156: exactly this, and nothing more.
Line 157: Writing a test first will make you think in terms of the API of the object. You won’t yet know
Line 158: what the implementation is going to look like (even if you have some vision of it). This is good: it
Line 159: means your tests will have more chances of testing the external behaviour of the object, and not its
Line 160: implementation details. This results in much more maintainable tests, which are not inseparably linked
Line 161: to the implementation.
Line 162: Always start with the failing test, and always observe it failing. Do not neglect this step! It
Line 163: is one of the few ways to learn about the quality of your test (see Chapter 12, Test Quality).
Line 164:  Of course, you cannot run the test right after having written it. Why? Because if you truly followed
Line 165: the "never write code without a failing test" rule, then your test would be using some non-existent
Line 166: classes and methods. It simply would not be able to compile. So, as part of this first step you will also
Line 167: need to make the test compile. Usually IDE will make this a breeze, by creating a default (empty)
Line 168: implementation of classes and methods which are used from the test code.
Line 169: Readable Assertion Message
Line 170: After you have a failing test and before you start implementing the code to fix it, it is advisable to
Line 171: take care of one additional detail: making sure that the message printed by the failing test indicates
Line 172: precisely what is wrong. Sometimes, in fact quite often, the default error message is good enough. If
Line 173: not, work on it (see Section 9.4 for some hints) until you are satisfied with the result. Then, move on
Line 174: to the next step.
Line 175: 4.2.2. GREEN - Write the Simplest Thing that
Line 176: Works
Line 177: Now that you have a failing test, and a clear assertion message, you need to make the test pass – by
Line 178: writing code, of course!
Line 179: The point here is not to go too far. It is to write the smallest amount of code that will satisfy the
Line 180: test. Concentrate on the task in hand. You have to make the bar green. That is it. Do not think (too
Line 181: 43
Line 182: 
Line 183: --- 페이지 59 ---
Line 184: Chapter 4. Test Driven Development
Line 185: much) about possible enhancements, do not worry about all the potential uses of your class, do not
Line 186: dwell on features that it would be "nice to have". Do not try to fulfil those requirements of the tests
Line 187: that have not yet been implemented (but which you can already envisage in your mind). The single
Line 188: failing test makes your current task clear: make it green, and nothing more.
Line 189: Remember, there will be other tests. They will cover other requirements. And when their time comes,
Line 190: you will add all those cool features that are screaming out to you in your head "implement me now!".
Line 191: Ah, just let them scream for a while. Maybe they really will be required, maybe not. Your tests will
Line 192: tell. Concentrate on the task at hand.
Line 193: On the other hand, do not fall into the opposite trap. "Simple" and "simplistic" are not synonyms! The
Line 194: "simplest thing that works" should be simple, but reasonable. Concentrating on the task at hand is not
Line 195: an excuse for writing sloppy code.
Line 196: I am not encouraging you to shut your ears to all of your experience gained from working as an
Line 197: architect or a designer. I am not saying that you should not think about the broader picture. What I
Line 198: am saying is "listen to your code". Have your own ideas, but listen to your code. It can guide your
Line 199: design. Listen to your tests also. They will tell you what is really important. They will not let you
Line 200: roam through the endless realm of exciting possibilities.
Line 201: 4.2.3. REFACTOR - Improve the Code
Line 202: The question is, won’t adding simple features one by one make your final code look like a pile of
Line 203: randomly laid elements? The code will work, but will it be easy to enhance, will it be flexible, will
Line 204: it adhere to all OO principles (KISS3, DRY, SRP4 and others)? And this is how we arrive at the next
Line 205: step of the TDD rhythm: refactoring.
Line 206: Once the test passes you can make some changes to your code. The safety net of tests gives you the
Line 207: confidence that you will not break anything as long as you "keep the bar green". Go on then, refactor!
Line 208: Remove duplicated code, change method names, update variables scope, move chunks from one place
Line 209: to another! And rerun your tests frequently. They will tell you precisely what damage, if any, your
Line 210: refactorings have caused.
Line 211:  And why is this step required? As some people say, "if it works, don’t fix it" – so why burden yourself
Line 212: with the task? The answer is that during the previous step (writing the least amount of code to satisfy a
Line 213: test) you focused on the task in hand, and the code implemented might not be clear enough. It works,
Line 214: but it might be a nightmare to maintain. And above and beyond this, when coding "only enough to
Line 215: pass the test" you were thinking only about that particular piece of code. Now is the time to look at the
Line 216: broader picture and refactor all the code you have, not just the few lines written a minute or so ago.
Line 217: Maybe there is some redundancy, maybe some functionality should be moved to a private function,
Line 218: maybe some variables should be renamed. Now is the time to do this.
Line 219: If you had "refactored", and the tests still passed, but the application is broken now, it
Line 220: means that you were not really refactoring. You were just changing your code. Refactoring
Line 221: is moving around above a safety net of tests. It means working with code which is
Line 222: thoroughly tested. You are being unfair to "refactoring" when you accuse it of having
Line 223: broken something. You had simply done it badly (i.e. not tested well enough).
Line 224: 3KISS, "Keep It Simple Stupid", see http://en.wikipedia.org/wiki/KISS_principle
Line 225: 4SRP, Single Responsibility Principle, see http://en.wikipedia.org/wiki/Single_responsibility_principle
Line 226: 44
Line 227: 
Line 228: --- 페이지 60 ---
Line 229: Chapter 4. Test Driven Development
Line 230: Last, but not least, the refactoring phase is also a good moment to add some documentation - see
Line 231: Section 4.9 for some discussion of this idea.
Line 232: Refactoring the Tests
Line 233:  Should you also refactor the tests? Yes, you should! Remember, they are a valuable asset. You
Line 234: will be executing them, reading them and updating them often. They are the foundation upon which
Line 235: your code is built and, as such, should be robust and of the highest quality. The quality of your code
Line 236: depends strongly on your tests, so you had better have confidence that they are really, really good.
Line 237: Refactoring is a way of restructuring the code without changing its functionality. In terms of tests, this
Line 238: means that the refactored tests exercise the same paths of code, call the same methods, use identical
Line 239: arguments, and verify the same assertions, as they were doing before you commenced the refactoring.
Line 240: An obvious issue with test refactoring is that there are no tests for tests themselves, so you might
Line 241: accidentally introduce some unwanted changes instead of performing a refactor. Such a danger exists,
Line 242: but is not as serious as it might at first glance seem. First of all, unit tests, if written correctly, are
Line 243: really simple (see Section 11.2). They contain no complex logic such as might be prone to breaking
Line 244: down when changes are introduced. When you refactor tests you are more involved in just moving
Line 245: things around - e.g. moving some common functionality to set-up methods5 - than you are in working
Line 246: with test logic. Also, if you do something wrong, it is very probable that the green bar will turn to red,
Line 247: warning you immediately that something has gone wrong.
Line 248: In summary, proceed with caution, but do not be afraid to refactor your tests. Make sure the number
Line 249: of executed tests has not changed, and if you do not feel confident with the changes introduced while
Line 250: refactoring, take a look at the code coverage report (see Section 12.3).
Line 251: 4.2.4. Here We Go Again
Line 252: After the code has been refactored, run the tests again to make sure that no harm has been done.
Line 253: Remember, run all the unit tests - not just the ones you have been working with recently. Unit tests
Line 254: execute fast: no time is gained by only running selected ones. Run them all, see that they pass, and so
Line 255: be confident that you can move on to the next test. Repeat the process till there are no more tests to be
Line 256: written.
Line 257: 4.3. Test First Example
Line 258: Now we are so well educated about test-first, let’s get down to business and do some coding! We shall
Line 259: code a simple class using – surprise, surprise! – the test-first approach.
Line 260: Take a look at the TDD cycle shown previously. We shall be following its phases one by one. We
Line 261: will start with a failing test. Then, after we have made sure that the error message is informative
Line 262: enough, we will move on to fixing the code. After the test passes we shall concentrate on making the
Line 263: code better by refactoring.
Line 264: Even though we shall try to follow precisely the steps described in the preceding sections, you will
Line 265: see that in real life some additional work is required. Well, moving from theory to practice is never a
Line 266: painless process.
Line 267: 5See Chapter 12, Test Quality for more information on refactoring of the test code.
Line 268: 45
Line 269: 
Line 270: --- 페이지 61 ---
Line 271: Chapter 4. Test Driven Development
Line 272: The example shown in this section is simplified – I realize that. I have made it that simple
Line 273: on purpose, so we can see test-first in practice without being distracted by the complexity
Line 274: of the domain model.
Line 275: 4.3.1. The Problem
Line 276: Let us play some football, okay? We will implement a FootballTeam class, so we can compare
Line 277: different teams and see who takes first place in the league. Each team keeps a record of the number of
Line 278: games won.
Line 279: Now we have to think about this. Let us imagine the functionalities of the class and the expected
Line 280: outcomes. All we need is a rough idea, and some guesses regarding the implementation. The details
Line 281: will come later – we do not need to think too hard right now. We should have at least some ideas
Line 282: regarding tests, so we can make the first move. Ok, let us think about this.
Line 283: So, in our example we have two teams and we need to compare them. It seems like I
Line 284: can use a Comparable interface. Yes, this is a common Java pattern for comparison…
Line 285: no need to think about anything fancy here….Good… Now, if we are to compare them,
Line 286: each team needs to remember the number of games it has won, and the comparison
Line 287: mechanism will use them. So a FootballTeam class needs a field in which to keep
Line 288: this information, and this field should somehow be accessible… Okay… and the most
Line 289: important thing is the comparison…. We need a few tests here: we need to see that
Line 290: teams with more wins are ranked first, and we need to check what happens when two
Line 291: teams have the same number of wins.
Line 292: — Tomek Dump of a Train of Thought (2011)
Line 293: As you see, some "external API" thoughts mix with "internal implementation" thoughts here. Yes, I
Line 294: guess this can’t be avoided. Anyway, this seems enough to get us started.
Line 295: 4.3.2. RED - Write a Failing Test
Line 296: In order to compare two teams, each of them has to remember its number of wins. For the sake
Line 297: of simplicity let us design a FootballTeam class that takes the number of games as a constructor
Line 298: parameter6. First things first: let us make sure that this constructor works.
Line 299: We start by creating a new class - FootballTeamTest - somewhere in the src/test/java/ directory.
Line 300: It can look like the following:
Line 301: Listing 4.1. Testing number of games won
Line 302: public class FootballTeamTest {
Line 303:     @Test
Line 304:     void constructorShouldSetGamesWon() {
Line 305:         FootballTeam team = new FootballTeam(3); 
Line 306:         assertThat(team.getGamesWon()).isEqualTo(3); 
Line 307:     }
Line 308: }
Line 309: 6In a more real-life scenario, a team would probably start with 0 games won, and then, based on the results of games played, it
Line 310: would incrementally adjust its score.
Line 311: 46
Line 312: 
Line 313: --- 페이지 62 ---
Line 314: Chapter 4. Test Driven Development
Line 315: Whoa, wait! At this point, your IDE will mark FootballTeam with a red color, as the class does
Line 316: not exist.
Line 317: Similarly, at this point your IDE will complain about the lack of a getGamesWon() method.
Line 318:  Obviously, you need to create a FootballTeam class and its getGamesWon() method before
Line 319: proceeding any further. You can let your IDE create the class, its constructor and this one method for
Line 320: you, or you can write them yourself.
Line 321: There are two things to remember when writing code that is necessary in order for a test to compile:
Line 322: • All production code should be kept in a different directory tree from the tests. I suggest following
Line 323: the previously described pattern and putting it in src/main/java.
Line 324: • Do nothing more than the minimum required for the test to compile. Create the necessary
Line 325: classes and methods, but do not fit them out with any business logic. Remember, we want to see our
Line 326: test fail now!
Line 327: It does not matter whether we created the required code ourselves or let IDE do it (which
Line 328: I recommend): either way, we will end up with an implementation of the FootballTeam class along
Line 329: similar lines to the following:
Line 330: Listing 4.2. Autogenerated FootballTeam class
Line 331: public class FootballTeam {
Line 332:     public FootballTeam(int gamesWon) {
Line 333:     }
Line 334:     public int getGamesWon() {
Line 335:         return 0;
Line 336:     }
Line 337: }
Line 338: It is quite interesting that we get this code "for free". And I am not just referring here to the IDE’s
Line 339: being able to generate it on the basis of the test. Even if we wrote it by hand, it was still hardly an
Line 340: intellectual challenge! Writing the test might have been demanding, but creating the code was very,
Line 341: very simple. That is not always the case, but it does often happen like that.
Line 342: Since the test compiles, and has an assertion which verifies an important functionality belonging to
Line 343: our class, it is worth running. Once we run it, it fails miserably, with the following message:
Line 344: Listing 4.3. Failing tests message
Line 345: org.opentest4j.AssertionFailedError:
Line 346: Expecting:
Line 347:  <0>
Line 348: to be equal to:
Line 349:  <3>
Line 350: but was not.
Line 351: Let us be clear about this – a failing test at this point is a good thing! Now we know that our test has
Line 352: been executed, and that some important functionality is not ready yet. We will implement it till we see
Line 353: the green light (that is, the test passes).
Line 354: 47
Line 355: 
Line 356: --- 페이지 63 ---
Line 357: Chapter 4. Test Driven Development
Line 358: But first, let us resist the urge to fix the code right away. Instead, we should take care of the error
Line 359: message. Does it say precisely what is wrong here? If the answer is "no", then add a custom error
Line 360: message (see Section 9.4). If you are happy with the current message, then proceed further.
Line 361: Let us say that I have decided that the test will be better if enhanced with the following custom error
Line 362: message:
Line 363: assertThat(team.getGamesWon())
Line 364:     .as("number of games won") 
Line 365:     .isEqualTo(3);
Line 366: Another neat method provided by AssertJ - as(…) - allows to enhance the error message.
Line 367: Now, after we have rerun the test, the output will be more informative:
Line 368: org.opentest4j.AssertionFailedError: [number of games won]
Line 369: Expecting:
Line 370:  <0>
Line 371: to be equal to:
Line 372:  <3>
Line 373: but was not.
Line 374: If we ever break our SUT code, so this test fails, the assertion message will tell us precisely what is
Line 375: wrong and the fix should be easy.
Line 376: All right then, it is time to move on to the next phase of TDD – we should make the test pass now – by
Line 377: fixing the code, of course.
Line 378: 4.3.3. GREEN - Fix the Code
Line 379: I know this is a really simple case. I know that you can write such code with your eyes closed, and
Line 380: you don’t need any fancy TDD techniques to do that. I know this, I really do. Still, I encourage you to
Line 381: follow the path we agreed to take: the path of baby steps.
Line 382: And walking in baby steps means that we will implement only what this first test requires us to do.
Line 383: Even if this seems outrageously unsatisfying.
Line 384: Let us take this baby step then.
Line 385: Listing 4.4. The simplest thing that satisfies the failing test
Line 386: public class FootballTeam {
Line 387:     public FootballTeam(int gamesWon) {
Line 388:     }
Line 389:     public int getGamesWon() {
Line 390:         return 3;
Line 391:     }
Line 392: }
Line 393: If we run the test now we will discover that this snippet of code really does satisfy the test. You could
Line 394: call it an absurdity, but there is wisdom in this folly. What it proves is that your test is not good
Line 395: 48
Line 396: 
Line 397: --- 페이지 64 ---
Line 398: Chapter 4. Test Driven Development
Line 399: enough to cover a certain functionality. It says, "Look, your test is so pathetic that I can make it
Line 400: pass by doing such a silly thing. You need to try harder!". It taunts us, it makes us angry, and in the
Line 401: end, it makes us write more, and better, tests.
Line 402: But before we write more tests, there is yet another phase to take care of: refactoring.
Line 403: 4.3.4. REFACTOR - Even If Only a Little Bit
Line 404:  In the case of something as simple as this FootballTeam class, I do not see anything worth
Line 405: refactoring. However, let us not forget to refactor the test! The least we should do is to get rid of the
Line 406: magic number 3 – for example, by introducing a THREE_GAMES_WON variable:
Line 407: Listing 4.5. Refactored FootballTeamTest
Line 408: public class FootballTeamTest {
Line 409:     private static final int THREE_GAMES_WON = 3;
Line 410:     @Test
Line 411:     void constructorShouldSetGamesWon() {
Line 412:         FootballTeam team = new FootballTeam(THREE_GAMES_WON);
Line 413:         assertThat(team.getGamesWon())
Line 414:             .as("number of games won")
Line 415:             .isEqualTo(THREE_GAMES_WON);
Line 416:         }
Line 417:     }
Line 418: The change was trivial, and there is no way it could break the test, right? Right! This change is trivial,
Line 419: and you probably asked your IDE to extract constant value, which further diminishes the possibility of
Line 420: any damage. True. Still, what you have to do now is to run the whole test suite.
Line 421: Still green? Great, let’s move on, then!
Line 422: No matter how insignificant the refactoring seems, always run the whole test suite. Just
Line 423: do it.
Line 424: 4.3.5. First Cycle Finished
Line 425: We have just finished the first TDD cycle. Everything started with that failed test. Then we worked on
Line 426: the error message and fixed the code. After the test passed, we refactored the code (and rerun the test),
Line 427: thus completing the cycle.
Line 428: 49
Line 429: 
Line 430: --- 페이지 65 ---
Line 431: Chapter 4. Test Driven Development
Line 432: Figure 4.3. The TDD cycle - we just completed it once
Line 433: But obviously, we haven’t finished the job yet, only the first of the probably numerous TDD cycles.
Line 434: Especially given that the first test we wrote and the first implementation of the FootballTeam class
Line 435: that we developed left us with a feeling of unfulfillment.
Line 436: 4.3.6. Fail, Pass, Refactor, …
Line 437: The constructor seems to work fine, …at least for this one value! We should add tests for more values,
Line 438: and also make the constructor throw an exception if an inappropriate number of wins is passed to the
Line 439: constructor (see Section 7.1). We will use parameterized tests (discussed in Section 3.6) in both cases.
Line 440: As you remember, the first implementation proved that our testing suite (consisting of just one test so
Line 441: far…) is not good enough. Let us now prove that we can do better. This test will surely put more strain
Line 442: on the FootballTeam class:
Line 443: Listing 4.6. Testing valid values using parameterized test
Line 444: @ParameterizedTest 
Line 445: @ValueSource(ints = { 0, 1, 3, 10 }) 
Line 446: void constructorShouldSetGamesWon(int nbOfGamesWon) { 
Line 447:         FootballTeam team = new FootballTeam(nbOfGamesWon);
Line 448:         assertThat(team.getGamesWon())
Line 449:             .as("number of games won")
Line 450:             .isEqualTo(nbOfGamesWon);
Line 451: }
Line 452: A parameterized test which expects a single integer as an input argument.
Line 453: Since values are simple integers, we can pass them using the @ValueSource annotation.
Line 454: We are in the red phase again. If we run this test, 3 out of 4 test cases will fail since getGamesWon()
Line 455: returns a canned value of 3 no matter what. There is no trick that we could use to get out of this
Line 456: situation as we did last time. Fortunately, the fix is straightforward: all we need to do is store the value
Line 457: passed as constructor parameter to some internal variable. The fixed FootballTeam class is presented
Line 458: below.
Line 459: Listing 4.7. Fixed FootballTeam class
Line 460: public class FootballTeam {
Line 461: 50
Line 462: 
Line 463: --- 페이지 66 ---
Line 464: Chapter 4. Test Driven Development
Line 465:     private int gamesWon;
Line 466:     public FootballTeam(int gamesWon) {
Line 467:         this.gamesWon = gamesWon;
Line 468:     }
Line 469:     public int getGamesWon() {
Line 470:         return gamesWon;
Line 471:     }
Line 472: }
Line 473: Rerun the test. Green? Yes, it is! Does it feel better now? Definitely!
Line 474: Time to refactor. The FootballTeam class is still so simple that there is nothing to be done. But our
Line 475: test can be cleaned: there is no need for the first test method to be there anymore. The second test
Line 476: covers the 3-games-won scenario, and also does much more. We can remove the first test now.
Line 477: After the change we rerun our test suite (is it still green?), and we can move to the red phase of TDD
Line 478: once again. This time we will take care of invalid values.
Line 479: Based on our previous experience, we can start with a parameterized test already.
Line 480: Listing 4.8. Testing invalid values using a parameterized test
Line 481: @ParameterizedTest
Line 482: @ValueSource(ints = { -10, -1 })
Line 483: void constructorShouldThrowExceptionForIllegalGamesNb(int illegalNbOfGames) {
Line 484:     assertThatExceptionOfType(IllegalArgumentException.class)
Line 485:         .isThrownBy(() -> { new FootballTeam(illegalNbOfGames); });
Line 486: }
Line 487: This test fails, as the constructor of the FootballTeam class currently accepts any value. The fix is
Line 488: straightforward:
Line 489: Listing 4.9. Constructor handles invalid values
Line 490: public FootballTeam(int gamesWon) {
Line 491:     if (gamesWon < 0) {
Line 492:         throw new IllegalArgumentException(
Line 493:             "Not possible to have less than 0 games won!
Line 494:                     (was + " + gamesWon + ")");
Line 495:     }
Line 496:     this.gamesWon = gamesWon;
Line 497: }
Line 498: The test is green now. Any refactoring required? No? Let us write another test (and see it fail).
Line 499: But is It Comparable?
Line 500:  The constructor works fine. Now we can move on to the main problem: that is, to comparing football
Line 501: teams. First of all, we have decided that we are going to use the java.lang.Comparable interface.
Line 502: This is an important decision which will influence not just the implementation of this class, but also
Line 503: its API and expected behaviour. If FootballTeam is comparable, then the client can expect that once
Line 504: he has put a few teams into a collection, he will be able to use the Collections.sort() method
Line 505: to order them. If so, then there should be a test for this behaviour. The only one I can think of is the
Line 506: following:
Line 507: 51
Line 508: 
Line 509: --- 페이지 67 ---
Line 510: Chapter 4. Test Driven Development
Line 511: Listing 4.10. Is FootballTeam comparable?
Line 512: private static final int ANY_NUMBER = 123;
Line 513: @Test
Line 514: void shouldBePossibleToCompareTeams() {
Line 515:     FootballTeam team = new FootballTeam(ANY_NUMBER);
Line 516:     assertThat(team).isInstanceOf(Comparable.class);
Line 517: }
Line 518:  This is a rather uncommon test: I rarely write tests which verify the implemented interfaces of
Line 519: the SUT. However, in this case it seems legitimate, as it covers an important characteristic of the
Line 520: FootballTeam class which is required by its clients.
Line 521: Please note the name of the static value passed to the constructor: ANY_NUMBER. That
Line 522: indicates that this argument is not important. The real value of the argument does not
Line 523: influence the test in any way. 
Line 524: The test will fail. Your IDE is surely capable of fixing the code. After the IDE has generated the
Line 525: default implementation of the required compareTo() method, the FootballTeam class will look like
Line 526: this:
Line 527: Listing 4.11. FootballTeam implements Comparable interface
Line 528: public class FootballTeam implements Comparable<FootballTeam> {
Line 529:     private int gamesWon;
Line 530:     public FootballTeam(int gamesWon) {
Line 531:         this.gamesWon = gamesWon;
Line 532:     }
Line 533:     public int getGamesWon() {
Line 534:         return gamesWon;
Line 535:     }
Line 536:     @Override
Line 537:     public int compareTo(FootballTeam otherTeam) {
Line 538:         return 0;
Line 539:     }
Line 540: }
Line 541: Rerun the test to ensure that it passes now. It does. Good.
Line 542: Before we move on to the next tests, let us make one thing clear: it is essential to run the
Line 543: whole test suite, and NOT only the last tests that failed. Make sure that while working on
Line 544: a certain feature you do not break other features. Remember, always run all unit tests you
Line 545: have. If they are really "unit" tests, they will run fast - no problem running them often,
Line 546: right? 
Line 547: Comparison Tests
Line 548: If you are not familiar with the Comparable interface, please take a look at the description
Line 549: of the Comparable.compareTo() method in Javadocs. 
Line 550: 52
Line 551: 
Line 552: --- 페이지 68 ---
Line 553: Chapter 4. Test Driven Development
Line 554: Now let us write the first comparison test. The idea is simple: take two teams with different numbers
Line 555: of wins and compare them.
Line 556: Listing 4.12. The first comparison test
Line 557: @Test
Line 558: void teamsWithMoreMatchesWonShouldBeGreater() {
Line 559:     FootballTeam team_2 = new FootballTeam(2);
Line 560:     FootballTeam team_3 = new FootballTeam(3);
Line 561:     assertThat(team_3.compareTo(team_2)).isGreaterThan(0);
Line 562: }
Line 563: When run, the test will fail. Once again, the error message is cryptic and needs to be updated. After it
Line 564: has been changed, the failed tests can print something more informative7:
Line 565: Listing 4.13. Comparison test failure
Line 566: java.lang.AssertionError:
Line 567:     team with 3 games won should be ranked before team with 2 games won
Line 568:     at com.practicalunittesting.chp04.footballteam.FootballTeamTest
Line 569:         .teamWithMoreMatchesWonShouldBeGreater(FootballTeamTest.java:77)
Line 570: The previous time in a very similar situation we returned a canned value of 3. This time, we could do
Line 571: the same with the following implementation of the compareTo() method:
Line 572: @Override
Line 573: public int compareTo(FootballTeam o) {
Line 574:         return 1;
Line 575: }
Line 576: But let us try something different this time and actually implement a more reasonable response. We
Line 577: will soon see where it takes us.
Line 578: The compareTo() method shown below looks to me like a very decent implementation which will
Line 579: make the test pass:
Line 580: Listing 4.14. compareTo() method recognises better teams
Line 581: @Override
Line 582: public int compareTo(FootballTeam o) {
Line 583:     if (gamesWon > o.getGamesWon()) {
Line 584:         return 1;
Line 585:     }
Line 586:     return 0; 
Line 587: }
Line 588: We decided to leave this branch so that our code does a little more than the test requires. In a
Line 589: few minutes, we will see what consequences this brings.
Line 590: After running all the tests and making sure they pass, we should:
Line 591: • refactor: change the o variable to something more descriptive like otherTeam,
Line 592: 7We will learn how to tweak assertion messages in Section 9.4.
Line 593: 53
Line 594: 
Line 595: --- 페이지 69 ---
Line 596: Chapter 4. Test Driven Development
Line 597: • rerun the tests so that we can be sure the refactoring was safe,
Line 598: • and, finally, proceed with the next test.
Line 599: You have probably noticed that we have just finished yet another TDD cycle - starting with
Line 600: failing test, writing code to satisfy it, and then refactoring.
Line 601: Listing 4.15. Another comparison test
Line 602: @Test
Line 603: void teamsWithLessMatchesWonShouldBeLesser() {
Line 604:     FootballTeam team_2 = new FootballTeam(2);
Line 605:     FootballTeam team_3 = new FootballTeam(3);
Line 606:     assertThat(team_2.compareTo(team_3))
Line 607:         .isLessThan(0);
Line 608: }
Line 609: Run, see it fail, then introduce changes to the FootballTeam class so the tests pass. The
Line 610: implementation which makes this test pass is, once again, trivial:
Line 611: Listing 4.16. compareTo() method recognizes team with fewer wins
Line 612: @Override
Line 613: public int compareTo(FootballTeam otherTeam) {
Line 614:     if (gamesWon > otherTeam.getGamesWon()) {
Line 615:         return 1;
Line 616:     }
Line 617:     else if (gamesWon < otherTeam.getGamesWon()) {
Line 618:         return -1;
Line 619:     }
Line 620:     return 0;
Line 621: }
Line 622: All tests pass, so we can move on to an equality test:
Line 623: Listing 4.17. Testing for equality
Line 624: @Test
Line 625: void teamsWithSameNumberOfMatchesWonShouldBeEqual() {
Line 626:     FootballTeam teamA = new FootballTeam(2);
Line 627:     FootballTeam teamB = new FootballTeam(2);
Line 628:     assertThat(teamA.compareTo(teamB))
Line 629:         .isEqualTo(0);
Line 630: }
Line 631:  Well, this test passes instantly, because our implementation has already returned 0 in cases of equality
Line 632: (see Listing 4.14).
Line 633: So, what should we do now? We have definitely skipped one step in the TDD rhythm. We have never
Line 634: seen this equality test failing, so we do not know why it passes. Is it because:
Line 635: • the FootballTeam class really implements the expected behaviour?
Line 636: 54
Line 637: 
Line 638: --- 페이지 70 ---
Line 639: Chapter 4. Test Driven Development
Line 640: • our test has been badly written and would always pass?
Line 641: • our test is not being executed at all?
Line 642: Again, with such trivial examples answers are easy to find. But in general, with a more complicated
Line 643: codebase and a plethora of tests, this might not be so. To make sure that your test really verifies the
Line 644: given scenario, and that your code really passes the test, you need to do the following:
Line 645: • introduce a change into production code that would break the test,
Line 646: • run all the tests and verify that this particular test fails,
Line 647: • revert the change,
Line 648: • run all the tests and verify that this particular test passes.
Line 649: In our case, the change to introduce would be to return some other value than 0 in the last line of the
Line 650: compareTo() method, e.g.:
Line 651: Listing 4.18. compareTo() method broken on purpose
Line 652: @Override
Line 653: public int compareTo(FootballTeam otherTeam) {
Line 654:     if (gamesWon > otherTeam.getGamesWon()) {
Line 655:         return 1;
Line 656:     }
Line 657:     else if (gamesWon < otherTeam.getGamesWon()) {
Line 658:         return -1;
Line 659:     }
Line 660:     return 23948732; 
Line 661: }
Line 662: The equality test is expected to fail now.
Line 663: So the test is red now. After reverting the line to return 0 we can see all our tests pass. Good, our
Line 664: equality test is doing what it should!
Line 665: So this was the price we paid for our initial decision to implement slightly more than the
Line 666: first test required. Not a big deal, and we made it all green in the end, but not without some
Line 667: additional struggle.
Line 668: Let us move on to refactoring. Now that we have a safety net of tests, we can really refactor the
Line 669: method being tested. After carefully thinking through the matter, we have ended up with a much
Line 670: simpler implementation:
Line 671: Listing 4.19. compareTo() method simplified
Line 672: @Override
Line 673: public int compareTo(FootballTeam otherTeam) {
Line 674:     return gamesWon - otherTeam.getGamesWon();
Line 675: }
Line 676: Rerunning the tests now tells us that this implementation satisfies all the requirements (written in the
Line 677: form of tests) so far. Hurray!
Line 678: 55
Line 679: 
Line 680: --- 페이지 71 ---
Line 681: Chapter 4. Test Driven Development
Line 682: 4.4. Benefits
Line 683: TDD helps with, but does not guarantee, good design & good code. Skill, talent, and
Line 684: expertise remain necessary.
Line 685: — Esko Luontola
Line 686: So now you have had a first-hand experience with TDD. Before I ask how you liked it, let me list the
Line 687: benefits of this approach:
Line 688: • 100% of the code we created is covered with unit tests, which allowed us to refactor the algorithm
Line 689: without the fear of breaking anything,
Line 690: • there are no superfluous parts of the code that have been written just because they "could possibly
Line 691: be useful" or "will surely be required one day" (YAGNI) - we created only what was requested by
Line 692: clients (in our case, our clients were the tests),
Line 693: • writing the smallest amount of code to make the test pass led us to simple solutions (KISS),
Line 694: • thanks to the refactoring phase, the code is clean and readable (DRY) - both the production code
Line 695: and the tests,
Line 696: • it is easy to go back to coding, even after interruptions; all you have to do is take the next test from
Line 697: the list and start the next cycle.
Line 698: 4.5. Conclusions and Comments
Line 699: The actual implementation of the test is rather a detail of TDD. Much more important
Line 700: is the mindset of practicing baby steps, the mindset of gaining insights and evolving
Line 701: through rapid feedback, the mindset of leveraging trial & error as a methodology,
Line 702: where errors are not failures but valuable insights that guide the evolution of the
Line 703: project.
Line 704: — Jonas Bandi
Line 705: So we have just implemented a class using the test-first approach. We moved in very small steps. We
Line 706: paid attention to the details. We polished the code. We even dealt with assertion messages. And all
Line 707: the time we were making sure that no functionality was broken – by rerunning the tests over and over
Line 708: again. And all the time we were moving forward… step by step… always forward.
Line 709: I have a lot of questions to ask you now. How did you like it? Did you enjoy the red-green-refactor
Line 710: rhythm? Did it help you with writing the code, or did you feel it got in the way of your style of
Line 711: thinking and coding? Are you confident that the created code really works? Would you have done it
Line 712: better or faster without testing, or – maybe – would you have preferred to have written the tests after
Line 713: the implementation had finished? Did you feel you were wasting time by writing tests even for trivial
Line 714: cases? Did you feel confident refactoring the code?
Line 715: Such a simple example might not be enough to demonstrate its usefulness. The problem was so trivial
Line 716: that you surely would have had an implementation ready in your mind from the outset, and would
Line 717: not have benefitted much from having written the tests first. However, it will be different when you
Line 718: 56
Line 719: 
Line 720: --- 페이지 72 ---
Line 721: Chapter 4. Test Driven Development
Line 722: start using test-first "in the wild". You will be writing tests for features that you have no idea how to
Line 723: implement. Then you will see how having tests helps you come up with a solution.
Line 724: Personally, I feel I owe so much to the test-first technique that I would be delighted if you also were to
Line 725: like it. However, it is up to you to decide whether test-first really suits you. Throughout the rest of this
Line 726: book I will be relying solely on the test-first technique. If you like it, great! If not, well, please do bear
Line 727: with it anyway!
Line 728: 4.6. How to Start Coding TDD
Line 729: We are all the same, under pressure we fall back on what we know; hit a few
Line 730: difficulties in TDD and developers stop writing tests.
Line 731: — Ian Cooper
Line 732: So now you have read about the wonders of the TDD approach! And you like it! It seems a little bit
Line 733: awkward, but at the same time sensible. You have heard about some great programmers writing tests
Line 734: before code. You have heard about some projects written test-first and renowned for their superior
Line 735: quality. You have spent some time reading about TDD techniques, you know the rhythm, you are
Line 736: getting more and more excited about the whole idea (up to the point of tattooing a "red-green-refactor"
Line 737: mantra on your back). Eventually… you have made up your mind about it: you want to try it… you
Line 738: want to be a step ahead of your team mates. You are eager to try it right now, with the very next job
Line 739: that you are given!
Line 740: And you do try it. And it feels like… like trying to break a wall with your own head! Databases,
Line 741: Spring context, static classes, ORM tools, JNDI calls, web services, global variables, deep inheritance
Line 742: hierarchy and console output jump out at you all at once. Nothing looks like it did in the test-first
Line 743: tutorials; none of the good advice you read seems of any help. It is just plain impossible to proceed!
Line 744: But of course you do not give up without a fight. Struggling, with gritted teeth, you somehow
Line 745: overcome one issue after another, one at a time. It takes time. You need to read some blogs, talk with
Line 746: your colleagues about the necessary design changes, but somehow it works. But at the end of the day,
Line 747: you look at the amount of written code, and you know that this is not good. You would have achieved
Line 748: 10 times more by using the code-first approach that you are accustomed with. You are not even proud
Line 749: of your tests - you know what dirty hacks you had to use to be able to write them.
Line 750: Let us stop here, before we sink into despair. Dear TDD-Wannabe-Programmer, you were simply
Line 751: trying to do too much at once! You were trying to change your habits (which is hard enough in itself)
Line 752: and, at the same time, to solve multiple problems existing in your codebase. Even if you did have
Line 753: some tests (as I hope you did), your code was probably never written with testability in mind. Trying
Line 754: to add new features in test-first manner is like challenging the old codebase: it will fight back, as you
Line 755: have just experienced. It will attempt to thwart your efforts. Those same solutions that once you were
Line 756: so proud of are now stopping you from moving forwards.
Line 757: What I would suggest is exactly what TDD itself promotes. Move in small steps. Start with the
Line 758: simplest things. Implement easy tasks using the test-first approach. Cherish every TDD success. Learn
Line 759: from every TDD failure. If you find something that you cannot tackle using the test-first approach,
Line 760: then do not worry too much about it. After a few weeks (hours, days, months?) you will be able to
Line 761: deal with such tasks. Build up your experience in small steps. Day by day… This way it will work –
Line 762: you will see!
Line 763: 57
Line 764: 
Line 765: --- 페이지 73 ---
Line 766: Chapter 4. Test Driven Development
Line 767: It will get easier and easier every day. Firstly, because you are getting better and better at coding test-
Line 768: first. You "feel the rhythm", you concentrate on the task in hand, you stop thinking about possible
Line 769: and useful issues that are merely hypothetical, etc. Secondly, because you stop doing things you were
Line 770: doing, and start thinking in terms of testing. Thirdly, your design is much more testable now, and
Line 771: the next parts of your code are easier to test. Fourthly, some colleagues have joined you and stopped
Line 772: producing tons of untestable code. …and now you can see the light at the end of the tunnel. Good. :)
Line 773: 4.7. When not To Use Test-First?
Line 774: TDD works like a charm, and it is very probable that once you get a good grip on it, you will be
Line 775: reluctant to code in any other way. However, there are some circumstances where this approach does
Line 776: not seem to be the best option. This section discusses this.
Line 777: As explained in the previous section, it is really not advisable to jump at the deep end after just
Line 778: reading a "how-to-swim” tutorial. :) I do have faith in your programming skills (and so on), but it
Line 779: might just happen to be the case that you are not yet ready to implement any real-life programming
Line 780: tasks using the test-first approach. Start with something simple, gain experience and then move on.
Line 781: This means that the first anti-test-first situation is attacking all possible problems at the same time,
Line 782: while lacking experience, skills and confidence. Do not do that.
Line 783: And even then, when you have some experience, you will still find yourself stuck with TDD. Like
Line 784: Kent Beck8, who tried to implement a new Eclipse plugin without prior knowledge of the technology:
Line 785: For six or eight hours spread over the next few weeks I struggled to get the first test
Line 786: written and running. […] If I’d just written some stuff and verified it by hand, I would
Line 787: probably have the final answer to whether my idea is actually worth money by now.
Line 788: Instead, all I have is a complicated test that doesn’t work, a pile of frustration, [and]
Line 789: eight fewer hours in my life […].
Line 790: — Kent Beck Just Ship, Baby (2009)
Line 791: Writing tests usually requires a good understanding of the technologies used, and knowledge of
Line 792: the problem domain. If you lack these, you will probably be better off starting with the code-first
Line 793: approach - especially if you lack the time to acquire the necessary knowledge and know you will
Line 794: spend time struggling with the (unknown) testing framework instead of writing real code. As usual,
Line 795: use common sense and learn from your mistakes.
Line 796: Another TDD stopper is when you apply it to some legacy code. You might not be able to go with
Line 797: TDD without some serious refactoring - thus, hitting the "chicken and egg" problem, because you
Line 798: cannot refactor for real without a safety net of tests… But then you’ll have a few dirty tricks up your
Line 799: sleeves: tools which allow you to deal with all the weirdness of your legacy code9. Sadly, there will
Line 800: be a time when you will need to use them, even if you would gladly rewrite the whole code from the
Line 801: scratch.
Line 802: However, all this applies more to integration tests than unit tests. My experience with test-first coding
Line 803: of unit tests is that it is always possible to do at least some state testing this way. As for testing of
Line 804: interactions between objects, this is sometimes significantly harder (because of some legacy non-
Line 805: easily-testable code structure).
Line 806: 8Do I really have to introduce Kent Beck? If so… see http://en.wikipedia.org/wiki/Kent_Beck
Line 807: 9This takes us back to the distinction between "tools for verification" and "tools for design" discussed in Section 1.3.
Line 808: 58
Line 809: 
Line 810: --- 페이지 74 ---
Line 811: Chapter 4. Test Driven Development
Line 812: 4.8. Should I Follow It Blindly?
Line 813: I am not apt to follow blindly the lead of other men.
Line 814: — Charles Darwin
Line 815: TDD is based on a set of very simple rules: first write a test, then see it fail, make it pass, refactor,
Line 816: check that it is still green, and then… repeat the cycle. Moreover, the beauty of these rules is
Line 817: magnified by their wide scope of applicability – you can tackle almost any programming dilemma
Line 818: with them. However, these rules are not carved in stone. You will encounter some situations where it
Line 819: make sense to omit some steps. This section gives some examples of such situations.
Line 820: 4.8.1. Write Good Assertion Messages from the
Line 821: Beginning
Line 822: After you have gained some experience with AssertJ you will just know when the default assertion
Line 823: message is good enough and when it should be corrected. I do not see any point in waiting for the test
Line 824: to fail, only to see that my hunch was correct and that I should, indeed, fix the message.
Line 825: That is why I often write good assertion messages without waiting for the test to fail.
Line 826: 4.8.2. If the Test Passes "By Default"
Line 827:   We have already witnessed the case of test passing "by default" when we rather expected it to fail as
Line 828: we just started the TDD cycle (remember the equality test discussed in Section 4.3.6?). Back then this
Line 829: was the outcome of our decision to write production code that did more than the first tests requested.
Line 830: Sometimes it also happens that it is not our fault: the IDE can interfere with our TDD habits by
Line 831: autogenerating the required functionality. Let us have a look at an example.
Line 832: Suppose you start writing a test, as shown in Listing 4.20. This might not be the best possible test, but
Line 833: it is good enough to illustrate the case in point. When writing it, your IDE will probably suggest auto-
Line 834: generating an empty implementation of the required methods in order to make the test compile.
Line 835: Listing 4.20. A simple getter/setter test
Line 836: Client client = new Client(); 
Line 837: client.setAge(20); 
Line 838: assertThat(client.getAge()).isEqualTo(20); 
Line 839: First the IDE will suggest creating a client class with a default constructor – and this is good!
Line 840: When it comes to the setAge() and getAge() methods, IntelliJ IDEA will offer two options: to
Line 841: create a method, or create a getter/setter.
Line 842: If you choose the second option – generating getters and setters – IntelliJ IDEA will generate the
Line 843: following code:
Line 844: Listing 4.21. Code autogenerated by IDE
Line 845: public class Client {
Line 846: 59
Line 847: 
Line 848: --- 페이지 75 ---
Line 849: Chapter 4. Test Driven Development
Line 850:     private int age;
Line 851:     public void setAge(int age) {
Line 852:         this.age = age;
Line 853:     }
Line 854:     public int getAge() {
Line 855:         return age;
Line 856:     }
Line 857: }
Line 858: Now, if you run the test, you will see it pass. Oops… seems like we have just skipped the first step of
Line 859: TDD! This code will not only compile, but pass the first test, so you have no chance to see the failing
Line 860: test!
Line 861: It is a reasonable assumption, that IDE is capable of generating getters/setters correctly. And I won’t
Line 862: blame you if drop your TDD habits for a minute and don’t go through the whole cycle of breaking the
Line 863: production code, witnessing test fail, fixing the code back, and witnessing test pass (as discussed in
Line 864: Section 4.3.6). However, the minimum of what should be done, is to check if the test was executed
Line 865: at all. Do it, so you are certain of this.
Line 866: 4.9. TDD & Javadocs
Line 867: During a refactoring phase I will also be taking care of Javadocs - both for production code and tests.
Line 868: This raises two issues:
Line 869: 1. First of all, your design is still not fixed. Is there a point in writing any documentation now, when
Line 870: the things may still be about to be changed?
Line 871: 2. Writing documentation now can interfere with the flow of thoughts you have. Your brain is already
Line 872: focusing on the next test to be written. Is it a good idea to interrupt this so-called "flow" and switch
Line 873: to a different activity?
Line 874: These valid questions are reinforced by the natural aversion of developers to writing
Line 875: documentation. This results in postponing the act of its creation… which, of course, leads
Line 876: to there being no documentation at all. This seems really cool in the short term, but is
Line 877: deadly in the long run.
Line 878: What I suggest is the following:
Line 879: 1. Keep it short - it will hurt less this way. Write only about the business purpose of the classes and
Line 880: methods, and about any important design decisions.
Line 881: 2. If you really, really do not want to break the coding flow, leave a note to yourself - by putting
Line 882: some TODO or FIXME marks within the code, on a scrap of paper (some kind of Post-it note on
Line 883: your monitor) or only a mental note (be careful here, they tend to vanish, you know!). Obviously,
Line 884: you’ll need to devote some time to fixing the issue after you’ve finished some larger chunks of the
Line 885: functionality.
Line 886: Do not forget that you should aim to write code that is self-documenting. Use descriptive
Line 887: method names, and write good, readable tests. This will leave you with virtually nothing to
Line 888: put into Javadocs (except for some higher-level explanations).
Line 889: 60
Line 890: 
Line 891: --- 페이지 76 ---
Line 892: Chapter 4. Test Driven Development
Line 893: 4.10. TDD is Not Only about Unit Tests
Line 894:     Even though this book is devoted to unit tests, this section is to remind you that TDD is much
Line 895: broader than this. In fact, you can, and you are encouraged to, use TDD on every level. Figure 4.4
Line 896: illustrates this idea.
Line 897: As you can see, there are two TDD loops here10. The outer loop relates to working with end-to-end
Line 898: tests in the same test-first manner as we have adopted for unit tests. For example, the outer loop could
Line 899: include tests executed against the GUI, written with the Selenium web testing tool. In order to satisfy
Line 900: such a test, many smaller functionalities must be implemented, which takes us into the inner loop.
Line 901: This, in turn, symbolizes the implementation of unit tests, and pertains to the implementation of much
Line 902: smaller functionalities.
Line 903: Figure 4.4. TDD on different levels
Line 904: There is a huge difference between the two loops. A developer will finish many cycles of the inner
Line 905: loop each day, while one cycle of the outer loop might take him even a few days. However, both are
Line 906: identical when it comes to the rhythm of work. In both cases you move from red to green, and then
Line 907: you keep it green while refactoring. This approach to development, based on the TDD method, has
Line 908: also gained a degree of popularity and even has its own name – ATDD, which stands for Acceptance
Line 909: Test Driven Development.
Line 910: We will not be spending any more time on this broader use of TDD, but after you have mastered
Line 911: TDD at the unit-testing level it is advisable to also try it with different types of tests. Once again,
Line 912: [freeman2009] is a must-read.
Line 913: 10There might be more of them - i.e. three - if other tests, like integration tests, were also to be taken into account. However, for the
Line 914: sake of simplicity I have decided to put only two of them in the picture.
Line 915: 61
Line 916: 
Line 917: --- 페이지 77 ---
Line 918: Chapter 4. Test Driven Development
Line 919: 4.11. Exercises
Line 920: You have just got acquainted with a new development method, which promotes writing tests before
Line 921: actual implementation. It is time to see, in practice, what you have learned. The exercises in this
Line 922: section are not so hard from the point of view of the complexity of the tasks. The point is to focus on
Line 923: the TDD rhythm and not on the algorythmic gotchas. When doing your homework, be extra careful
Line 924: about following the TDD, and doing everything in really small steps. Good luck!
Line 925: When working on these exercises, remember to obey the "never write code unless you have
Line 926: a failing test" rule!
Line 927: 4.11.1. Password Validator
Line 928: When creating an account, it is often required that the password should fulfil some strength
Line 929: requirements. It should be X characters long, have at least Y digits, contain underscore, hash, and
Line 930: a mixture of lower and capital letters, etc. Your task is to write a method that will validate a given
Line 931: password. The set of rules (requirements) with which you will be verifying the passwords is up to you.
Line 932: 4.11.2. Regex
Line 933: Some people, when confronted with a problem, think "I know, I’ll use regular
Line 934: expressions." Now they have two problems.
Line 935: — Jamie Zawinski
Line 936: This example requires you to write a method which, given a String, returns a list of all numbers
Line 937: taken from that String that have 3 or more digits. Table 4.1 gives some examples of expected results
Line 938: for various input strings.
Line 939: Table 4.1. Expected outputs of regex method
Line 940: input
Line 941: expected output
Line 942: abc 12
Line 943: cdefg 345 12bb23
Line 944: 345
Line 945: cdefg 345 12bbb33 678tt
Line 946: 345, 678
Line 947: 4.11.3. Booking System
Line 948: Your task is to write a (very) simplified version of a booking system. In fact, it can be written as a
Line 949: single class, which should:
Line 950: • return a list of booked hours,
Line 951: • not allow a particular hour to be double-booked,
Line 952: • deal in a sensible manner with illegal values (provided as input parameters).
Line 953: On the constraints side (to make the task more appropriate for practicing TDD), the system:
Line 954: 62
Line 955: 
Line 956: --- 페이지 78 ---
Line 957: Chapter 4. Test Driven Development
Line 958: • has only one resource that can be booked (e.g. a classroom, a lawn mower, a restaurant table, or
Line 959: anything else that makes sense to you),
Line 960: • has no notion of days, or to put it differently, it assumes all reservations are for today,
Line 961: • should only permit booking of regular whole clock-hours (e.g. it should not allow a booking from
Line 962: 4:30 pm. to 5:30 pm.),
Line 963: • is not required to remember any additional information concerning the reservation (who booked it,
Line 964: when etc.).
Line 965: 63