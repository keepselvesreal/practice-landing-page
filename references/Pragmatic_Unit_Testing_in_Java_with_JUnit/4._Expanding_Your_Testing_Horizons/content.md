Line 1: 
Line 2: --- 페이지 91 ---
Line 3: CHAPTER 4
Line 4: Expanding Your Testing Horizons
Line 5: At this point, you’ve worked through the core topics in unit testing, including
Line 6: JUnit and unit testing fundamentals, how to test various scenarios, and how
Line 7: to use test doubles to deal with dependencies.
Line 8: In this chapter, you’ll review a few topics that begin to move outside the sphere
Line 9: of “doing unit testing”:
Line 10: • Code coverage and how it can help (or hurt)
Line 11: • Challenges with writing tests for multithreaded code
Line 12: • Writing integration tests
Line 13: Improving Unit Testing Skills Using Code Coverage
Line 14: Code coverage metrics measure the percentage of code that your unit tests
Line 15: execute (exercise) when run. Ostensibly, code that is covered is working, and
Line 16: code that is not covered represents the risk of breakage.
Line 17: From a high level, tests that exhaust all relevant pieces of code provide 100
Line 18: percent coverage. Code with no tests whatsoever has 0 percent coverage. Most
Line 19: code lies somewhere in between.
Line 20: Many tools exist that will calculate coverage metrics for Java code, including
Line 21: JaCoCo, OpenClover, SonarQube, and Cobertura. IntelliJ IDEA ships with a
Line 22: coverage tool built into the IDE.
Line 23: Numerous coverage metrics exist to measure various code aspects. Function
Line 24: coverage, for example, measures the percentage of functions (methods) exer-
Line 25: cised by tests. Some of the other metrics include line, statement, branch,
Line 26: condition, and path coverage.
Line 27: report erratum  •  discuss
Line 28: 
Line 29: --- 페이지 92 ---
Line 30: Line and statement coverage metrics are similar. Line coverage measures
Line 31: source lines exercised. Since a line can consist of multiple statements, some
Line 32: tools measure statement coverage.
Line 33: Branch, condition, and path coverage metrics are similarly related. Branch
Line 34: coverage measures whether all branches of a conditional statement (for
Line 35: example, both true and false branches of an if statement) are executed. Condition
Line 36: coverage measures whether all conditionals (including each in a complex
Line 37: conditional) have evaluated to both true and false. Path coverage measures
Line 38: whether every possible route through the code has been executed.
Line 39: Most of the popular Java coverage tools support calculating line and branch
Line 40: coverage. You’ll learn about these in this section.
Line 41: Understanding Statement Coverage
Line 42: Consider a Batter class that tracks a baseball batter’s strike count. A batter is
Line 43: out after three strikes. A swing-and-a-miss with the bat—a strike—increments
Line 44: the strike count. A foul ball (a ball hit out of play) also increments the strike
Line 45: count unless the batter already has two strikes.
Line 46: utj3-coverage/01/src/main/java/util/Batter.java
Line 47: public class Batter {
Line 48: private int strikeCount = 0;
Line 49: public void foul() {
Line 50: if (strikeCount < 2)
Line 51: strikeCount++;
Line 52: }
Line 53: public void strike() {
Line 54: strikeCount++;
Line 55: }
Line 56: public int strikeCount() {
Line 57: return strikeCount;
Line 58: }
Line 59: }
Line 60: Note the strike method. If none of your tests trigger its execution, its coverage
Line 61: is 0 percent. If your tests do result in a call to strike, its whopping one line of
Line 62: code gets exercised, and thus the recorded coverage is 100 percent.
Line 63: The foul method contains a conditional. It increments strikeCount only if there
Line 64: are fewer than two strikes. A conditional, implemented in Java with an if
Line 65: statement, demands at least two tests—one that forces the conditional block
Line 66: to execute (because the conditional expression resolved to true) and one that
Line 67: bypasses the if block code.
Line 68: Chapter 4. Expanding Your Testing Horizons • 72
Line 69: report erratum  •  discuss
Line 70: 
Line 71: --- 페이지 93 ---
Line 72: The following test covers the special case—when two strikes already exist.
Line 73: utj3-coverage/01/src/test/java/util/ABatter.java
Line 74: @Test
Line 75: void doesNotIncrementStrikesWhenAtTwo() {
Line 76: batter.strike();
Line 77: batter.strike();
Line 78: batter.foul();
Line 79: assertEquals(2, batter.strikeCount());
Line 80: }
Line 81: If you run this test “with coverage” (that’s the actual text on an IDEA menu
Line 82: item), the if statement conditional evaluates to false because strikeCount is not
Line 83: less than two. As a result, the if-statement body doesn’t execute, and strikeCount
Line 84: is not incremented.
Line 85: Here’s a tool window showing the summary coverage metrics:
Line 86: Method coverage shows that three of three possible methods defined on the
Line 87: Batter class were exercised. That’s not terribly interesting or useful.
Line 88: Line coverage shows that three of four lines were exercised across those three
Line 89: methods—one of the lines didn’t get covered when the test ran. In this case,
Line 90: it’s because you only ran one test in ABatter. Run them all to attain 100 percent
Line 91: line coverage.
Line 92: The real value of a coverage tool is that it shows exactly what lines are exer-
Line 93: cised and what lines are not. IDEA’s coverage tool window shows colored
Line 94: markers in the gutter (the gray strip left of the source code) to the immediate
Line 95: right of the line numbers. It marks executed lines as green, lines not executed
Line 96: as red, and lines partially covered (read on) as yellow as shown in the figure
Line 97: on page 74.
Line 98: The increment operation (strikeCount++) is marked red because it is never
Line 99: executed.
Line 100: Uncovered code is one of two things: dead or risky.
Line 101: It can be near-impossible to determine whether code is ever needed or used.
Line 102: “All dead” code (as opposed to mostly dead code, which might have some
Line 103: report erratum  •  discuss
Line 104: Improving Unit Testing Skills Using Code Coverage • 73
Line 105: 
Line 106: --- 페이지 94 ---
Line 107: future resurrected purpose) can waste time in many ways. Like a vampire,
Line 108: dead code sucks time: when you read it, when it shows up in search results,
Line 109: and when you mistakenly start making changes (true stories here) to it.
Line 110: When you encounter uncovered, mostly dead code, bring it into the sunlight
Line 111: of your whole team. If it doesn’t shrivel away under their scrutiny, cover the
Line 112: code with tests. Otherwise, delete it.
Line 113: Unit tests declare intent. If you test every intent, you can safely
Line 114: delete untested code.
Line 115: Add a second test involving only a single strike to get 100 percent coverage
Line 116: in foul:
Line 117: utj3-coverage/01/src/test/java/util/ABatter.java
Line 118: @Test
Line 119: void incrementsStrikesWhenLessThan2() {
Line 120: batter.strike();
Line 121: batter.foul();
Line 122: assertEquals(2, batter.strikeCount());
Line 123: }
Line 124: Conditionals and Code Coverage
Line 125: Line coverage is an unsophisticated metric that tells you only whether a line
Line 126: of code was executed or not. It doesn’t tell you if you’ve explored different
Line 127: Chapter 4. Expanding Your Testing Horizons • 74
Line 128: report erratum  •  discuss
Line 129: 
Line 130: --- 페이지 95 ---
Line 131: data cases. For example, if a method accepts an int, did you test it with 0?
Line 132: With negative numbers and very large numbers? A coverage tool doesn’t even
Line 133: tell you if the tests contain any assertions. (Yes, some clever developers do
Line 134: that to make their coverage numbers look better.)
Line 135: Complex conditionals often represent insufficiently covered paths through
Line 136: your code. You create complex conditionals when you produce Boolean
Line 137: expressions involving the logical operators OR (||) and AND (&&).
Line 138: Suppose you write one test that exercises a complex conditional using only
Line 139: the OR operator. The line coverage metric will credit your tests for the entire
Line 140: line containing the complex conditional as long as any one of its Boolean
Line 141: expressions resolves to true. But you won’t have ensured that all the other
Line 142: Boolean expressions behave as expected.
Line 143: Conditional coverage tools can help you pinpoint deficiencies in your coverage
Line 144: of conditionals.
Line 145: Take a look at the next intended increment of the Batter code, which supports
Line 146: tracking balls and walks. It introduces the notion of whether or not a batter’s
Line 147: turn at home plate is “done,” meaning that they either struck out or walked
Line 148: (hits and fielding outs would come later). The method isDone implements that
Line 149: complex conditional.
Line 150: utj3-coverage/02/src/main/java/util/Batter.java
Line 151: public class Batter {
Line 152: private int strikeCount = 0;
Line 153: private int ballCount = 0;
Line 154: public void foul() {
Line 155: if (strikeCount < 2)
Line 156: strikeCount++;
Line 157: }
Line 158: public void ball() {
Line 159: ballCount++;
Line 160: }
Line 161: public void strike() {
Line 162: strikeCount++;
Line 163: }
Line 164: public int strikeCount() {
Line 165: return strikeCount;
Line 166: }
Line 167: public boolean isDone() {
Line 168: ➤
Line 169: return struckOut() || walked();
Line 170: ➤
Line 171: }
Line 172: ➤
Line 173: report erratum  •  discuss
Line 174: Improving Unit Testing Skills Using Code Coverage • 75
Line 175: 
Line 176: --- 페이지 96 ---
Line 177: private boolean walked() {
Line 178: return ballCount == 4;
Line 179: }
Line 180: private boolean struckOut() {
Line 181: return strikeCount == 3;
Line 182: }
Line 183: }
Line 184: A new test is added to the test class to cover a strikeout case:
Line 185: utj3-coverage/02/src/test/java/util/ABatter.java
Line 186: @Test
Line 187: void whenStruckOut() {
Line 188: batter.strike();
Line 189: batter.strike();
Line 190: batter.strike();
Line 191: assertTrue(batter.isDone());
Line 192: }
Line 193: IDEA supports the branch coverage metric, but it is turned off by default.
Line 194: Turn it on and run all the tests in ABatter. Your code coverage summary now
Line 195: includes a column for Branch Coverage %:
Line 196: The summary pane shows that you have a branch coverage deficiency; cur-
Line 197: rently, it measures only 50 percent. Again, the more revealing aspect is how
Line 198: the coverage tool marks code within the editor for Batter. The isDone method is
Line 199: marked with yellow to indicate that not all branches of the complex conditional
Line 200: are covered. A call to struckOut occurs, but not to walked.
Line 201: Chapter 4. Expanding Your Testing Horizons • 76
Line 202: report erratum  •  discuss
Line 203: 
Line 204: --- 페이지 97 ---
Line 205: The struckOut method is also marked as partially covered. If you click on the
Line 206: yellow marker, IDEA reveals the coverage data:
Line 207: Hits: 1
Line 208: Covered 1/2 branches
Line 209: In other words, the method was invoked (“hit”) one time. Full branch coverage
Line 210: of a simple Boolean conditional would require getting hit twice—once where
Line 211: it evaluates to true and once where it gets evaluated to false.
Line 212: To garner full coverage for ABatter, you’ll need to add a couple of tests to not
Line 213: only exercise the walked method but to also ensure that you have a test in
Line 214: which the entire expression in isDone returns false.
Line 215: utj3-coverage/03/src/test/java/util/ABatter.java
Line 216: @Test
Line 217: void isDoneWithWalk() {
Line 218: for (var i = 0; i < 4; i++)
Line 219: batter.ball();
Line 220: assertTrue(batter.isDone());
Line 221: }
Line 222: @Test
Line 223: void isNotDoneWhenNeitherWalkNorStrikeout() {
Line 224: assertFalse(batter.isDone());
Line 225: }
Line 226: How Much Coverage Is Enough?
Line 227: Any one of your unit tests will exercise only a very small percentage of code—a
Line 228: unit’s worth. If you want 100 percent coverage, write unit tests for every unit
Line 229: you add to your system. Emphasize testing the behaviors, not the methods.
Line 230: Use tools like ZOM to help you think through the different cases and their
Line 231: outcomes.
Line 232: On the surface, it would seem that higher code coverage is good and lower
Line 233: coverage is not so good. But your manager craves a single number that says,
Line 234: “Yup, we’re doing well on our unit testing practice,” or “No, we’re not writing
Line 235: enough unit tests.”
Line 236: To satisfy your manager, you’d unfortunately need to first determine what
Line 237: enough means. Obviously, 0 percent is not enough. And 100 percent would
Line 238: be great, but is it realistic? The use of certain frameworks can make it nearly
Line 239: impossible to hit 100 percent without some trickery.
Line 240: Most folks out there (the purveyors of Emma included) suggest that coverage
Line 241: under 70 percent is insufficient. I agree.
Line 242: report erratum  •  discuss
Line 243: Improving Unit Testing Skills Using Code Coverage • 77
Line 244: 
Line 245: --- 페이지 98 ---
Line 246: Many developers also claim that attempts to increase coverage represent
Line 247: diminishing returns on value. I disagree. Teams that habitually write unit tests
Line 248: after they write code achieve coverage levels of 70 percent with relative ease.
Line 249: Unfortunately, that means the remaining 30 percent of their code remains
Line 250: untested, often because it’s difficult, hard-to-test code. Difficult code hides more
Line 251: defects, so at least a third of your defects will probably lie in this untested code.
Line 252: Jeff’s Theory of Code Coverage: the amount of costly code
Line 253: increases in the areas of least coverage.
Line 254: The better your design, the easier it is to write tests. Revisit Chapter 8, Refactor-
Line 255: ing to Cleaner Code, on page 147 and Chapter 9, Refactoring Your Code’s
Line 256: Structure, on page 169 to understand how to better structure your code. A
Line 257: good design coupled with the will to increase coverage will move you in the
Line 258: direction of 100 percent, which should lead to fewer defects. You might not
Line 259: reach 100 percent, and that’s okay.
Line 260: Developers practicing TDD (see Chapter 11, Advancing with Test-Driven Devel-
Line 261: opment (TDD), on page 211) achieve percentages well over 90 percent, largely by
Line 262: definition. They write a test for each new behavior they’re about to code. Those
Line 263: who do TDD, myself included, rarely look at the coverage numbers. TDD makes
Line 264: coverage a self-fulfilling prophecy.
Line 265: Coverage percentages can mislead. You can easily write a few tests that blast
Line 266: through a large percentage of code yet assert little of use. Most tools don’t
Line 267: even care if your tests have no assertions (which means they’re not really
Line 268: tests). The tools certainly don’t care if your tests are cryptic or prolix or if they
Line 269: assert nothing useful. Too many teams spend a fortune writing unit tests
Line 270: with decent coverage numbers but little value.
Line 271: Unfortunately, managers always want a single number they can use to mea-
Line 272: sure success. The code-coverage number is but a surface-level metric that
Line 273: means little if the tests stink. And if someone tells the team that the metric
Line 274: goal matters most, the tests will stink.
Line 275: A downward code coverage trend is probably useful information, however.
Line 276: Your coverage percentage should either increase or become stable over time
Line 277: as you add behavior.
Line 278: The Value in Code Coverage
Line 279: If you write your tests after you write the corresponding code, you’ll miss
Line 280: numerous test cases until you improve your skills and habits. Even if you
Line 281: Chapter 4. Expanding Your Testing Horizons • 78
Line 282: report erratum  •  discuss
Line 283: 
Line 284: --- 페이지 99 ---
Line 285: try TDD and write tests first for all unit behaviors, you’ll still find yourself
Line 286: sneaking in untested logic over time.
Line 287: As you’re learning, lean on the visual red-yellow-and-green annotations that
Line 288: the tools produce.
Line 289: Use code-coverage tools to help you understand where your code
Line 290: lacks coverage or where your team is trending downward.
Line 291: Do your best to avoid the code coverage metric debate and convince your
Line 292: leadership that the metric is not for them. It will ultimately create problems
Line 293: when used for anything but educational purposes.
Line 294: Testing Multithreaded Code
Line 295: It’s hard enough to write code that works as expected. That’s one reason to
Line 296: write unit tests. It’s dramatically harder to write concurrent code that works
Line 297: and even harder to verify that it’s safe enough to ship.
Line 298: In one sense, testing application code that requires concurrent processing is
Line 299: technically out of the realm of unit testing. It’s better classified as integration
Line 300: testing. You’re verifying that you can integrate the notion of your application-
Line 301: specific logic with the ability to execute portions of it concurrently.
Line 302: Tests for threaded code tend to be slower because you must expand the scope
Line 303: of execution time to ensure that you have no concurrency issues. Threading
Line 304: defects sometimes sneakily lie in wait, surfacing long after you thought you’d
Line 305: stomped them all out.
Line 306: There are piles of ways to approach multithreading in Java and, similarly,
Line 307: piles of ways for your implementation to go wrong: deadlock, race conditions,
Line 308: livelock, starvation, and thread interference, to name a few. One could fill a
Line 309: book (or at least several chapters) covering how to test for and correct all of
Line 310: these policies. I’m not allowed to fill that much paper, so you’ll see only a
Line 311: short example that highlights a couple of key thoughts.
Line 312: Tips for Testing Multithreaded Code
Line 313: Here’s a short list of techniques for designing and analyzing multithreaded
Line 314: code that minimizes concurrency issues:
Line 315: • Minimize the overlap between threading controls and application code.
Line 316: Rework your design so that you can unit test the bulk of application
Line 317: report erratum  •  discuss
Line 318: Testing Multithreaded Code • 79
Line 319: 
Line 320: --- 페이지 100 ---
Line 321: code in the absence of threads. Write thread-focused tests for the small
Line 322: remainder of the code.
Line 323: • Trust the work of others. Java incorporates Doug Lea’s set of concurrency
Line 324: utility classes in java.util.concurrent. Don’t code producer/consumer yourself
Line 325: by hand, for example; it’s too easy to get wrong. Do take advantage of
Line 326: Lea’s BlockingQueue implementations, and capitalize on his painstaking
Line 327: efforts to get them right.
Line 328: • Avoid and isolate concurrent updates, which cause most problems.
Line 329: • Profile the codebase using static concurrency analysis tools, which can
Line 330: identify potential problems (including deadlocks) based on coded interac-
Line 331: tions between threads.
Line 332: • Profile the runtime behavior of your system using dynamic analysis tooling
Line 333: such as VisualVM or YourKit. These tools can monitor thread state, ana-
Line 334: lyze thread dumps, detect deadlocks, and more.
Line 335: • Write a test that demonstrates a potential concurrency problem, then
Line 336: exacerbate it to the point where the test always fails. You might reduce
Line 337: the number of threads, increase the number of requests being tested, or
Line 338: temporarily introduce sleep to expose timing issues. Tools like Thread
Line 339: Weaver can also help you force and test different thread interleavings.
Line 340: – Add only the concurrency control that makes the test pass. Syn-
Line 341: chronization blocks and locks may be necessary, but using them
Line 342: inappropriately can degrade performance (while still not solving
Line 343: the real concurrency problems).
Line 344: – When your fix consistently passes, remove any artificialities like sleep.
Line 345: • Don’t introduce concurrency controls like locks, synchronized blocks, or
Line 346: atomic variables until you’ve actually demonstrated a concurrency problem
Line 347: (hopefully with a failing test).
Line 348: Let’s take a quick look at one example of fixing a concurrency issue.
Line 349: Exacerbating a Threading Issue
Line 350: You’ll work on a bit of code from iloveyouboss, a job-search website designed
Line 351: to compete with sites like Indeed and Monster. It takes a different approach to
Line 352: the typical job posting site: It attempts to match prospective employees with
Line 353: potential employers and vice versa, much as a dating site would. Employers
Line 354: and employees both create profiles by answering a series of multiple-choice or
Line 355: yes-no questions. The site scores profiles based on criteria from the other party
Line 356: Chapter 4. Expanding Your Testing Horizons • 80
Line 357: report erratum  •  discuss
Line 358: 
Line 359: --- 페이지 101 ---
Line 360: and shows the best potential matches from the perspective of both the employee
Line 361: and employer. (The author reserves the right to monetize the site, make a
Line 362: fortune, retire, and do nothing but support the kind readers of this book.)
Line 363: The ProfileMatcher class, a core piece of iloveyouboss, collects all of the relevant
Line 364: profiles. Provided with a set of criteria (essentially the preferred answers to
Line 365: relevant questions), the ProfileMatcher method scoreProfiles iterates all profiles
Line 366: added. For each profile matching the criteria, ProfileMatcher collects both the
Line 367: profile and its score—zero if the profile is not a match for the criteria and a
Line 368: positive value otherwise.
Line 369: utj3-iloveyouboss2/01/src/main/java/iloveyouboss/domain/ProfileMatcher.java
Line 370: import java.util.*;
Line 371: import java.util.concurrent.*;
Line 372: public class ProfileMatcher {
Line 373: private List<Profile> profiles = new ArrayList<>();
Line 374: public void addProfile(Profile profile) {
Line 375: profiles.add(profile);
Line 376: }
Line 377: ExecutorService executorService =
Line 378: Executors.newFixedThreadPool(8);
Line 379: public Map<Profile, Integer> scoreProfiles(Criteria criteria)
Line 380: throws ExecutionException, InterruptedException {
Line 381: var profiles = new HashMap<Profile, Integer>();
Line 382: ➤
Line 383: var futures = new ArrayList<Future<Void>>();
Line 384: for (var profile: this.profiles) {
Line 385: futures.add(executorService.submit(() -> {
Line 386: profiles.put(profile,
Line 387: profile.matches(criteria) ? profile.score(criteria) : 0);
Line 388: return null;
Line 389: }));
Line 390: }
Line 391: for (var future: futures)
Line 392: future.get();
Line 393: executorService.shutdown();
Line 394: return profiles;
Line 395: }
Line 396: }
Line 397: To be responsive, scoreProfiles calculates matches in the context of separate
Line 398: threads, implemented using futures. Each profile iterated gets managed by
Line 399: a single future. That future is responsible for adding the profile and score to
Line 400: the profiles variable, initialized to an empty HashMap. That concurrent update
Line 401: is the source of the problem your test will uncover.
Line 402: report erratum  •  discuss
Line 403: Testing Multithreaded Code • 81
Line 404: 
Line 405: --- 페이지 102 ---
Line 406: utj3-iloveyouboss2/01/src/test/java/iloveyouboss/domain/AProfileMatcher.java
Line 407: import org.junit.jupiter.api.Test;
Line 408: import org.junit.jupiter.api.extension.ExtendWith;
Line 409: import org.mockito.junit.jupiter.MockitoExtension;
Line 410: import java.util.List;
Line 411: import java.util.function.Function;
Line 412: import static iloveyouboss.domain.Weight.REQUIRED;
Line 413: import static iloveyouboss.domain.Weight.WOULD_PREFER;
Line 414: import static java.util.stream.IntStream.range;
Line 415: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 416: @ExtendWith(MockitoExtension.class)
Line 417: class AProfileMatcher {
Line 418: ProfileMatcher matcher = new ProfileMatcher();
Line 419: @Test
Line 420: void returnsScoreForAllProfiles() throws Exception {
Line 421: var questions = createQuestions(50);
Line 422: int profileCount = 500;
Line 423: var half = profileCount / 2;
Line 424: range(0, half).forEach(id ->
Line 425: matcher.addProfile(createProfile(
Line 426: questions, id, i -> nonMatchingAnswer(questions.get(i)))));
Line 427: range(half, profileCount).forEach(id ->
Line 428: matcher.addProfile(createProfile(
Line 429: questions, id, i -> matchingAnswer(questions.get(i)))));
Line 430: var criteria = createCriteria(questions);
Line 431: var results = matcher.scoreProfiles(criteria);
Line 432: assertEquals(half,
Line 433: results.values().stream().filter(score -> score == 0).count());
Line 434: assertEquals(half,
Line 435: results.values().stream().filter(score -> score > 0).count());
Line 436: }
Line 437: private Profile createProfile(
Line 438: List<BooleanQuestion> questions,
Line 439: int id,
Line 440: Function<Integer, Answer> answerFunction) {
Line 441: var profile = new Profile(String.valueOf(id));
Line 442: range(0, questions.size()).forEach(i ->
Line 443: profile.add(answerFunction.apply(i)));
Line 444: return profile;
Line 445: }
Line 446: private Criteria createCriteria(List<BooleanQuestion> questions) {
Line 447: var questionCount = questions.size();
Line 448: var criteria = new Criteria();
Line 449: range(0, 5).forEach(i ->
Line 450: criteria.add(new Criterion(
Line 451: matchingAnswer(questions.get(i)), REQUIRED)));
Line 452: Chapter 4. Expanding Your Testing Horizons • 82
Line 453: report erratum  •  discuss
Line 454: 
Line 455: --- 페이지 103 ---
Line 456: range(5, questionCount).forEach(i ->
Line 457: criteria.add(new Criterion(
Line 458: matchingAnswer(questions.get(i)), WOULD_PREFER)));
Line 459: return criteria;
Line 460: }
Line 461: private List<BooleanQuestion> createQuestions(int questionCount) {
Line 462: return range(0, questionCount)
Line 463: .mapToObj(i -> new BooleanQuestion("question " + i))
Line 464: .toList();
Line 465: }
Line 466: Answer matchingAnswer(Question question) {
Line 467: return new Answer(question, Bool.TRUE);
Line 468: }
Line 469: Answer nonMatchingAnswer(Question question) {
Line 470: return new Answer(question, Bool.FALSE);
Line 471: }
Line 472: }
Line 473: The test returnsScoreForAllProfiles should fail most of the time and occasionally
Line 474: pass. If you have difficulty getting it to fail, alter the size of the thread pool,
Line 475: the number of questions (currently 50), and/or the number of profiles (500).
Line 476: Try to get it to fail at least 9 out of 10 times. I got it to consistently fail with
Line 477: 200 questions and 2000 profiles.
Line 478: A simple solution is to wrap the shared HashMap in a synchronized map, which
Line 479: makes it a thread-safe Java construct:
Line 480: utj3-iloveyouboss2/02/src/main/java/iloveyouboss/domain/ProfileMatcher.java
Line 481: public class ProfileMatcher {
Line 482: private List<Profile> profiles = new ArrayList<>();
Line 483: public void addProfile(Profile profile) {
Line 484: profiles.add(profile);
Line 485: }
Line 486: ExecutorService executorService =
Line 487: Executors.newFixedThreadPool(8);
Line 488: public Map<Profile, Integer> scoreProfiles(Criteria criteria)
Line 489: throws ExecutionException, InterruptedException {
Line 490: var profiles =
Line 491: ➤
Line 492: Collections.synchronizedMap(new HashMap<Profile, Integer>());
Line 493: ➤
Line 494: var futures = new ArrayList<Future<Void>>();
Line 495: for (var profile: this.profiles) {
Line 496: futures.add(executorService.submit(() -> {
Line 497: profiles.put(profile,
Line 498: profile.matches(criteria) ? profile.score(criteria) : 0);
Line 499: report erratum  •  discuss
Line 500: Testing Multithreaded Code • 83
Line 501: 
Line 502: --- 페이지 104 ---
Line 503: return null;
Line 504: }));
Line 505: }
Line 506: for (var future: futures)
Line 507: future.get();
Line 508: executorService.shutdown();
Line 509: return profiles;
Line 510: }
Line 511: Ensure that your test passes consistently—with the same numbers as it was
Line 512: consistently failing with—after making this small change.
Line 513: Perhaps the better approach, however, is to have each future return a map
Line 514: with a single key-value pair of profile and score. This avoids the modification
Line 515: to a shared data store. The individual-key maps can all be aggregated into a
Line 516: single HashMap as part of a loop that blocks on future.get for all futures:
Line 517: utj3-iloveyouboss2/03/src/main/java/iloveyouboss/domain/ProfileMatcher.java
Line 518: public Map<Profile, Integer> scoreProfiles(Criteria criteria)
Line 519: throws ExecutionException, InterruptedException {
Line 520: var futures = new ArrayList<Future<Map<Profile, Integer>>>();
Line 521: ➤
Line 522: for (var profile : profiles)
Line 523: futures.add(executorService.submit(() ->
Line 524: Map.of(profile,
Line 525: ➤
Line 526: profile.matches(criteria) ? profile.score(criteria) : 0)));
Line 527: ➤
Line 528: var finalScores = new HashMap<Profile, Integer>();
Line 529: ➤
Line 530: for (var future: futures)
Line 531: ➤
Line 532: finalScores.putAll(future.get());
Line 533: ➤
Line 534: executorService.shutdown();
Line 535: return finalScores;
Line 536: }
Line 537: Any exacerbation aside, the performance test will be slow due to the numerous
Line 538: iterations and larger data volumes typically wanted for such a test. It takes
Line 539: several hundred milliseconds on my machine, far too much for a single test.
Line 540: Mark it as “slow,” and run it separately from your suite of fast unit tests. See
Line 541: Creating Arbitrary Test Groups Using Tags, on page 137.
Line 542: Writing Integration Tests
Line 543: The QuestionRepository class talks to an H2 database using the Java Persistence
Line 544: API (JPA). You might correctly guess that this data class is used in many
Line 545: places throughout the application and that testing each of those places will
Line 546: require the use of a test double.
Line 547: Chapter 4. Expanding Your Testing Horizons • 84
Line 548: report erratum  •  discuss
Line 549: 
Line 550: --- 페이지 105 ---
Line 551: Here’s the code for the class:
Line 552: utj3-iloveyouboss2/01/src/main/java/iloveyouboss/persistence/QuestionRepository.java
Line 553: import iloveyouboss.domain.BooleanQuestion;
Line 554: import iloveyouboss.domain.PercentileQuestion;
Line 555: import iloveyouboss.domain.Persistable;
Line 556: import iloveyouboss.domain.Question;
Line 557: import jakarta.persistence.EntityManager;
Line 558: import jakarta.persistence.EntityManagerFactory;
Line 559: import jakarta.persistence.Persistence;
Line 560: import java.time.Clock;
Line 561: import java.util.List;
Line 562: import java.util.function.Consumer;
Line 563: public class QuestionRepository {
Line 564: private Clock clock = Clock.systemUTC();
Line 565: private static EntityManagerFactory getEntityManagerFactory() {
Line 566: return Persistence.createEntityManagerFactory("h2-ds");
Line 567: }
Line 568: public Question find(Long id) {
Line 569: try (var em = em()) {
Line 570: return em.find(Question.class, id);
Line 571: }
Line 572: }
Line 573: public List<Question> getAll() {
Line 574: try (var em = em()) {
Line 575: return em.createQuery("select q from Question q",
Line 576: Question.class).getResultList();
Line 577: }
Line 578: }
Line 579: public List<Question> findWithMatchingText(String text) {
Line 580: try (var em = em()) {
Line 581: var queryString =
Line 582: "select q from Question q where q.text like :searchText";
Line 583: var query = em.createQuery(queryString, Question.class);
Line 584: query.setParameter("searchText", "%" + text + "%");
Line 585: return query.getResultList();
Line 586: }
Line 587: }
Line 588: public long addPercentileQuestion(String text, String... answerChoices) {
Line 589: return persist(new PercentileQuestion(text, answerChoices));
Line 590: }
Line 591: public long addBooleanQuestion(String text) {
Line 592: return persist(new BooleanQuestion(text));
Line 593: }
Line 594: report erratum  •  discuss
Line 595: Writing Integration Tests • 85
Line 596: 
Line 597: --- 페이지 106 ---
Line 598: void setClock(Clock clock) {
Line 599: this.clock = clock;
Line 600: }
Line 601: void deleteAll() {
Line 602: executeInTransaction(em ->
Line 603: em.createNativeQuery("delete from Question").executeUpdate());
Line 604: }
Line 605: private EntityManager em() {
Line 606: return getEntityManagerFactory().createEntityManager();
Line 607: }
Line 608: private void executeInTransaction(Consumer<EntityManager> func) {
Line 609: try (var em = em()) {
Line 610: var transaction = em.getTransaction();
Line 611: try {
Line 612: transaction.begin();
Line 613: func.accept(em);
Line 614: transaction.commit();
Line 615: } catch (Exception t) {
Line 616: if (transaction.isActive()) transaction.rollback();
Line 617: }
Line 618: }
Line 619: }
Line 620: private long persist(Persistable object) {
Line 621: object.setCreateTimestamp(clock.instant());
Line 622: executeInTransaction(em -> em.persist(object));
Line 623: return object.getId();
Line 624: }
Line 625: }
Line 626: Most of the code in QuestionRepository is simple delegation to the JPA. The class
Line 627: contains little in the way of interesting logic. That’s good design. QuestionRepository
Line 628: isolates the dependency on JPA from the rest of the system.
Line 629: From a testing stance, does it make sense to write a unit test against Question-
Line 630: Repository? You could write unit tests in which you stub all of the relevant
Line 631: interfaces, but it would take a good amount of effort, the tests would be diffi-
Line 632: cult, and in the end, you wouldn’t have proven much. Particularly, unit testing
Line 633: QuestionRepository won’t prove that you’re using JPA correctly. Defects are fairly
Line 634: common in dealings with JPA because three different pieces of detail must
Line 635: all work correctly in concert: the Java code, the mapping configuration
Line 636: (located in src/META-INF/persistence.xml in your codebase), and the database itself.
Line 637: The only real way to know if QuestionRepository works is to have it interact with
Line 638: a real database. You can write tests to do so, but they’ll be integration tests,
Line 639: not unit tests. They’ll also be one to two orders of magnitude slower than unit
Line 640: tests.
Line 641: Chapter 4. Expanding Your Testing Horizons • 86
Line 642: report erratum  •  discuss
Line 643: 
Line 644: --- 페이지 107 ---
Line 645: The world of integration testing is huge, and this section is tiny, but hopefully,
Line 646: it provides a few ideas on when you’ll want integration tests and how you
Line 647: might approach crafting them.
Line 648: The Data Problem
Line 649: You want the vast majority of your JUnit tests to be fast. No worries—if you
Line 650: isolate all of your persistence interaction to one place in the system, you’ll
Line 651: have a reasonably small amount of code that must be integration tested.
Line 652: When you write integration tests for code that interacts with the real database,
Line 653: the data in the database and how it gets there are important considerations.
Line 654: To verify that database query operations return expected results, for example,
Line 655: you must either insert appropriate data or assume it already exists.
Line 656: Assuming that data is already in the database will create problems. Over
Line 657: time, the data will change without your knowledge, breaking tests. Also,
Line 658: divorcing the data from the test code makes it a lot harder to understand why
Line 659: a particular test passes or not. The meaning of the data with respect to the
Line 660: tests is lost by dumping it all into the database.
Line 661: As much as possible, integration tests should create and manage
Line 662: their own data.
Line 663: If your tests will be running against your database on your own machine, the
Line 664: simplest route might be for each test to start with a clean database (or one pre-
Line 665: populated with necessary reference data). Each test then becomes responsible
Line 666: for adding and working with its own data. This minimizes intertest dependency
Line 667: issues, where one test breaks because of data that another test left lying
Line 668: around. (Those can be a headache to debug!)
Line 669: If you can only interact with a shared database for your testing, then you’ll
Line 670: need a less intrusive solution. One option: if your database supports it, you
Line 671: can initiate a transaction in the context of each test and then roll it back.
Line 672: (The transaction handling is usually relegated to @BeforeEach and @AfterEach
Line 673: methods.)
Line 674: You’ll also want your integration tests to execute as part of your build process.
Line 675: Whatever solution you derive for the tests must work both on your machine
Line 676: as well as in the build server’s environment.
Line 677: Ultimately, integration tests are harder to write, execute, and maintain. They
Line 678: tend to break more often, and when they do break, debugging the problem
Line 679: report erratum  •  discuss
Line 680: Writing Integration Tests • 87
Line 681: 
Line 682: --- 페이지 108 ---
Line 683: can take considerably longer. But a dependable testing strategy demands you
Line 684: include some.
Line 685: If you find yourself adding interesting logic either before or after interaction
Line 686: with the live interactions (to the database in this example), find a way to
Line 687: extract that logic to another class. Write unit tests against it there.
Line 688: Integration tests are essential but challenging to design and
Line 689: maintain. Minimize their number and complexity by maximizing
Line 690: the logic you verify in unit tests.
Line 691: Clean-Room Database Tests
Line 692: Your tests for the repository empty the database both before and after each
Line 693: test method’s execution:
Line 694: utj3-iloveyouboss2/01/src/test/java/iloveyouboss/persistence/AQuestionRepository.java
Line 695: import iloveyouboss.domain.Question;
Line 696: import org.junit.jupiter.api.AfterEach;
Line 697: import org.junit.jupiter.api.BeforeEach;
Line 698: import org.junit.jupiter.api.Test;
Line 699: import java.time.ZoneId;
Line 700: import java.util.Date;
Line 701: import java.util.List;
Line 702: import static java.time.Clock.fixed;
Line 703: import static java.util.Arrays.asList;
Line 704: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 705: class AQuestionRepository {
Line 706: QuestionRepository repository = new QuestionRepository();
Line 707: @BeforeEach
Line 708: void setUp() {
Line 709: repository.deleteAll();
Line 710: }
Line 711: @AfterEach
Line 712: void tearDown() {
Line 713: repository.deleteAll();
Line 714: }
Line 715: @Test
Line 716: void findsPersistedQuestionById() {
Line 717: var id = repository.addBooleanQuestion("question text");
Line 718: var question = repository.find(id);
Line 719: assertEquals("question text", question.getText());
Line 720: }
Line 721: Chapter 4. Expanding Your Testing Horizons • 88
Line 722: report erratum  •  discuss
Line 723: 
Line 724: --- 페이지 109 ---
Line 725: @Test
Line 726: void storesDateAddedForPersistedQuestion() {
Line 727: var now = new Date().toInstant();
Line 728: repository.setClock(fixed(now, ZoneId.systemDefault()));
Line 729: var id = repository.addBooleanQuestion("text");
Line 730: var question = repository.find(id);
Line 731: assertEquals(now, question.getCreateTimestamp());
Line 732: }
Line 733: @Test
Line 734: void answersMultiplePersistedQuestions() {
Line 735: repository.addBooleanQuestion("q1");
Line 736: repository.addBooleanQuestion("q2");
Line 737: repository.addPercentileQuestion("q3", "a1", "a2");
Line 738: var questions = repository.getAll();
Line 739: assertEquals(asList("q1", "q2", "q3"), extractText(questions));
Line 740: }
Line 741: @Test
Line 742: void findsMatchingEntries() {
Line 743: repository.addBooleanQuestion("alpha 1");
Line 744: repository.addBooleanQuestion("alpha 2");
Line 745: repository.addBooleanQuestion("beta 1");
Line 746: var questions = repository.findWithMatchingText("alpha");
Line 747: assertEquals(asList("alpha 1", "alpha 2"), extractText(questions));
Line 748: }
Line 749: private List<String> extractText(List<Question> questions) {
Line 750: return questions.stream().map(Question::getText).toList();
Line 751: }
Line 752: }
Line 753: Clearing the data before gives your tests the advantage of working with a clean
Line 754: slate.
Line 755: Clearing the data after each test runs is just being nice, not leaving data
Line 756: around cluttering shared databases.
Line 757: When trying to figure out a problem, you might want to take a look at the
Line 758: data after a test completes. To do so, comment out the call to clearData call in
Line 759: the @AfterEach method.
Line 760: Your tests aren’t focused on individual methods; instead, they’re verifying
Line 761: behaviors that are inextricably linked. To verify that you can retrieve or find
Line 762: elements, you must first insert them. To verify that you’ve inserted elements,
Line 763: you retrieve them.
Line 764: report erratum  •  discuss
Line 765: Writing Integration Tests • 89
Line 766: 
Line 767: --- 페이지 110 ---
Line 768: Ensure you run coverage tools to verify that all the code is getting tested. The
Line 769: tests for QuestionRepository show that it’s completely covered with tests. Also, if
Line 770: you use integration tests to cover some small portions of code rather than
Line 771: unit tests, your system-wide unit test code coverage numbers will suffer a
Line 772: little. If that concerns you, you might be able to merge the numbers properly
Line 773: (the tool jacoco:merge
Line 774: 1 works for JaCoCo).
Line 775: Exploratory Unit Testing
Line 776: The unit tests you’ve learned to build capture your best understanding of the
Line 777: intents in the code. They cover known edge cases and typical use cases.
Line 778: Some code may demand further exploration. For example, complex code, code
Line 779: that seems to keep breaking as you uncover more nuances about the input
Line 780: data, or code that incurs a high cost if it were to fail. Systems requiring high
Line 781: reliability or security might incur significant costs from unit-level failures.
Line 782: Numerous kinds of developer-focused tests exist to help you with such
Line 783: exploratory testing. Many of them verify at the integration level—load tests,
Line 784: failover tests, performance tests, and contract tests, to name a few. You can
Line 785: learn about some of these in Alexander Tarlinder’s book Developer Testing.
Line 786: 2
Line 787: Following is an overview of two unit-level testing tactics: fuzz testing and
Line 788: property testing, which can be considered forms of what’s known as generative
Line 789: testing. These sorts of tests require additional tooling above and beyond JUnit,
Line 790: and thus, you’re only getting an introduction to them in this book. (That’s
Line 791: one excuse among a few, and I’m sticking with it.)
Line 792: Not covered at all: mutation testing, which involves tools that make small
Line 793: changes to your production code to see if such changes break your tests. If
Line 794: your tests don’t break, the mutation tests suggest you might have insufficient
Line 795: test coverage.
Line 796: Fuzz Testing
Line 797: With fuzz testing, you use a tool to provide a wide range of random, unexpected,
Line 798: or invalid inputs to your code. It can help you identify edge cases in your
Line 799: code that you’re otherwise unlikely to think of when doing traditional unit
Line 800: testing.
Line 801: 1.
Line 802: https://www.jacoco.org/jacoco/trunk/doc/merge-mojo.html
Line 803: 2.
Line 804: https://www.informit.com/store/developer-testing-building-quality-into-software-9780134431802
Line 805: Chapter 4. Expanding Your Testing Horizons • 90
Line 806: report erratum  •  discuss
Line 807: 
Line 808: --- 페이지 111 ---
Line 809: This URL creator code combines server and document strings into a valid
Line 810: URL string:
Line 811: utj3-iloveyouboss2/03/src/main/java/util/URLCreator.java
Line 812: import java.net.MalformedURLException;
Line 813: import java.net.URL;
Line 814: import static java.lang.String.format;
Line 815: public class URLCreator {
Line 816: public String create(String server, String document)
Line 817: throws MalformedURLException {
Line 818: if (isEmpty(document))
Line 819: return new URL(format("https://%s", server)).toString();
Line 820: return new URL(
Line 821: format("https://%s/%s", server, clean(document))).toString();
Line 822: }
Line 823: private boolean isEmpty(String document) {
Line 824: return document == null || document.trim().equals("");
Line 825: }
Line 826: private String clean(String document) {
Line 827: return document.charAt(0) == '/'
Line 828: ? document.substring(1)
Line 829: : document;
Line 830: }
Line 831: }
Line 832: Here are the tests:
Line 833: utj3-iloveyouboss2/03/src/test/java/util/AURLCreator.java
Line 834: import org.junit.jupiter.api.Test;
Line 835: import org.junit.jupiter.params.ParameterizedTest;
Line 836: import org.junit.jupiter.params.provider.NullSource;
Line 837: import org.junit.jupiter.params.provider.ValueSource;
Line 838: import java.net.MalformedURLException;
Line 839: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 840: class AURLCreator {
Line 841: URLCreator urlCreator = new URLCreator();
Line 842: @Test
Line 843: void returnsCombinedURLStringGivenServerAndDocument()
Line 844: throws MalformedURLException {
Line 845: assertEquals(
Line 846: "https://example.com/customer?id=123",
Line 847: urlCreator.create("example.com", "customer?id=123"));
Line 848: }
Line 849: @ParameterizedTest
Line 850: @NullSource
Line 851: report erratum  •  discuss
Line 852: Exploratory Unit Testing • 91
Line 853: 
Line 854: --- 페이지 112 ---
Line 855: @ValueSource(strings = { "", " \n\t\r " })
Line 856: void buildsURLGivenServerOnly(String document)
Line 857: throws MalformedURLException {
Line 858: assertEquals(
Line 859: "https://example.com",
Line 860: urlCreator.create("example.com", document));
Line 861: }
Line 862: @Test
Line 863: void eliminatesRedundantLeadingSlash() throws MalformedURLException {
Line 864: assertEquals(
Line 865: "https://example.com/customer?id=123",
Line 866: urlCreator.create("example.com", "/customer?id=123"));
Line 867: }
Line 868: }
Line 869: Code like this tends to grow over time as you think of additional protections
Line 870: to add. The third test deals with the case where the caller of the create method
Line 871: prepends the document with a forward slash—"/employee?id=42", for example.
Line 872: Someone likely wasn’t sure if the slash needed to be provided or not. The
Line 873: developer, as a result, updated the code to allow either circumstance.
Line 874: With fuzz testing, you’ll likely add more protections and corresponding tests
Line 875: as the fuzzing effort uncovers additional problems.
Line 876: You can write fuzz tests using the tool Jazzer:
Line 877: 3
Line 878: utj3-iloveyouboss2/03/src/test/java/util/AURLCreatorFuzzer.java
Line 879: import com.code_intelligence.jazzer.api.FuzzedDataProvider;
Line 880: import com.code_intelligence.jazzer.junit.FuzzTest;
Line 881: import java.net.MalformedURLException;
Line 882: public class AURLCreatorFuzzer {
Line 883: @FuzzTest
Line 884: public void fuzzTestIsValidURL(FuzzedDataProvider data)
Line 885: throws MalformedURLException {
Line 886: var server = data.consumeString(32);
Line 887: var document = data.consumeRemainingAsString();
Line 888: new URLCreator().create(server, document);
Line 889: }
Line 890: }
Line 891: Fuzz test methods are annotated with @FuzzTest, and passed a data provider.
Line 892: From this data provider (a wrapper around some random stream of data),
Line 893: you can extract the data you need. The test fuzzTestIsValidUrl first extracts a 32-
Line 894: character string to be passed as the server, then uses the remaining incoming
Line 895: data as the document.
Line 896: 3.
Line 897: https://github.com/CodeIntelligenceTesting/jazzer
Line 898: Chapter 4. Expanding Your Testing Horizons • 92
Line 899: report erratum  •  discuss
Line 900: 
Line 901: --- 페이지 113 ---
Line 902: To run fuzzing with Jazzer, first create a directory in your project’s test
Line 903: resources. Derive its name from your fuzzer class’s package plus the fuzzer
Line 904: class name plus the word Inputs:
Line 905: utj3-iloveyouboss2/src/test/resources/util/AURLCreatorFuzzerInputs
Line 906: Then run your tests with the environment variable setting JAZZER_FUZZ=1. The
Line 907: fuzzing tool will display failures and add the inputs causing the failures to
Line 908: files within the resource directory you created.
Line 909: The fuzzer should report that an input containing an LF (line feed character;
Line 910: ASCII value 10) represents an invalid character for a URL. You, as the devel-
Line 911: oper, get to decide how you want the code to deal with that, if at all.
Line 912: You can also collect a number of inputs in the test resources directory. With
Line 913: the JAZZER_FUZZ environment variable turned off, Jazzer will use these inputs
Line 914: to run what effectively become regression test inputs.
Line 915: Property Testing
Line 916: Another form of unit testing is property testing, where your tests describe
Line 917: invariants and postconditions, or properties, about the expected behavior of
Line 918: code. Property testing tools, such as jqwik,
Line 919: 4 will test these invariants using
Line 920: a wide range of automatically generated inputs.
Line 921: Your primary reason for using property tests is to uncover edge cases and
Line 922: unexpected behaviors by virtue of exploring a broader range of inputs.
Line 923: Here’s an implementation for the insertion sort algorithm, which performs
Line 924: terribly but is a reasonable choice if your input array is small (or if your inputs
Line 925: are generally almost sorted already):
Line 926: utj3-iloveyouboss2/03/src/main/java/util/ArraySorter.java
Line 927: public class ArraySorter {
Line 928: public void inPlaceInsertionSort(int[] arr) {
Line 929: for (var i = 1; i < arr.length - 1; i++) {
Line 930: var key = arr[i];
Line 931: var j = i - 1;
Line 932: while (j >= 0 && arr[j] > key) {
Line 933: arr[j + 1] = arr[j];
Line 934: j = j - 1;
Line 935: }
Line 936: arr[j + 1] = key;
Line 937: }
Line 938: }
Line 939: }
Line 940: 4.
Line 941: https://jqwik.net
Line 942: report erratum  •  discuss
Line 943: Exploratory Unit Testing • 93
Line 944: 
Line 945: --- 페이지 114 ---
Line 946: Using jqwik, you define @Property methods that get executed by the JUnit test
Line 947: runner. The following set of properties for ArraySorter describes three properties:
Line 948: an already-sorted array should remain sorted, an array with all the same
Line 949: elements should remain unchanged, and a random array should be sorted
Line 950: in ascending order:
Line 951: utj3-iloveyouboss2/03/src/test/java/util/ArraySorterProperties.java
Line 952: import static java.util.Arrays.fill;
Line 953: import static java.util.Arrays.sort;
Line 954: import net.jqwik.api.*;
Line 955: import java.util.Arrays;
Line 956: public class ArraySorterProperties {
Line 957: ArraySorter arraySorter = new ArraySorter();
Line 958: @Property
Line 959: boolean returnsSameArrayWhenAlreadySorted(@ForAll int[] array) {
Line 960: sort(array);
Line 961: var expected = array.clone();
Line 962: arraySorter.inPlaceInsertionSort(array);
Line 963: return Arrays.equals(expected, array);
Line 964: }
Line 965: @Property
Line 966: boolean returnsSameArrayWhenAllSameElements(@ForAll int element) {
Line 967: var array = new int[12];
Line 968: fill(array, element);
Line 969: var expected = array.clone();
Line 970: arraySorter.inPlaceInsertionSort(array);
Line 971: return Arrays.equals(expected, array);
Line 972: }
Line 973: @Property
Line 974: boolean sortsAscendingWhenRandomUnsortedArray(@ForAll int[] array) {
Line 975: var expected = array.clone();
Line 976: sort(expected);
Line 977: arraySorter.inPlaceInsertionSort(array);
Line 978: return Arrays.equals(expected, array);
Line 979: }
Line 980: }
Line 981: Taking the last method as an example: sortsAscendingForRandomUnsortedArray rep-
Line 982: resents a postcondition that should hold true for all (@ForAll) input arrays (array).
Line 983: The property implementation clones the incoming array and sorts it using
Line 984: Java’s built-in sort, capturing the result as expected. It sorts the incoming
Line 985: array, then returns the result of comparing that sort to expected.
Line 986: Chapter 4. Expanding Your Testing Horizons • 94
Line 987: report erratum  •  discuss
Line 988: 
Line 989: --- 페이지 115 ---
Line 990: Jqwik, a sophisticated and highly flexible tool, calls the property one thousand
Line 991: times by default. And, beauty! The last property fails, and consistently so,
Line 992: given those thousand inputs.
Line 993: The array sort code represents a good fit for property testing. You might think
Line 994: to write a handful of test cases (ZOM, certainly). But there are some cases
Line 995: that can be hard to think of. Property testing can help uncover those cases.
Line 996: Yes, there’s a defect in the insertion sort. The jqwik tool should identify the
Line 997: problem. See if you can figure out and fix the defective code.
Line 998: Summary
Line 999: In this chapter, you rounded out your knowledge of core unit testing concepts
Line 1000: with a few (mostly unrelated) topics that look at bigger concerns surrounding
Line 1001: unit testing:
Line 1002: • Code coverage, a concept that can help you learn where your unit testing
Line 1003: is deficient
Line 1004: • Testing multithreaded code, a tricky and sophisticated challenge
Line 1005: • Integration tests, which verify code and its interaction with external
Line 1006: dependencies that might be out of your control
Line 1007: Now that you’ve worked through foundational concepts regarding unit testing,
Line 1008: you’ll take a deeper look into the preferred tool for Java unit testing, JUnit.
Line 1009: The next three chapters will explore JUnit in-depth, providing useful insights
Line 1010: and nuggets on how to best take advantage of its wealth of features.
Line 1011: report erratum  •  discuss
Line 1012: Summary • 95