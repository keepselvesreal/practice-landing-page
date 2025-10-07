Line 1: 
Line 2: --- 페이지 163 ---
Line 3: CHAPTER 8
Line 4: Refactoring to Cleaner Code
Line 5: In Parts I and II, you dug deep into how to write unit tests and take advantage
Line 6: of JUnit. In this part, you’ll learn to take advantage of unit tests to help shape
Line 7: the design of your system, as well as document the numerous unit-level
Line 8: behavioral choices you’ve made. Your ability to keep your system simpler and
Line 9: your tests clearer can reduce your development costs considerably.
Line 10: You’ll start by focusing on design “in the small,” addressing the lack of clarity
Line 11: and excessive complexity that’s commonplace in most systems. You’ll
Line 12: accomplish this by learning to refactor—making small, frequent edits to the
Line 13: code you write. Your design improvements will help reduce the cost of change.
Line 14: In a clear, well-designed system, it might take seconds to locate a point of
Line 15: change and understand the surrounding code. In a more typically convoluted
Line 16: system, the navigation and comprehension tasks often require minutes
Line 17: instead. Once you’ve understood the code well enough to change it, a well-
Line 18: designed system might accommodate your change readily. In the convoluted
Line 19: system, weaving in your changes might take hours.
Line 20: Convoluted systems can increase your maintenance costs by an
Line 21: order of magnitude or more.
Line 22: You can, with relative ease, create systems that embody clean code. In brief,
Line 23: this describes clean code:
Line 24: • Concise: It imparts the solution without unnecessary code.
Line 25: • Clear: It can be directly understood.
Line 26: report erratum  •  discuss
Line 27: 
Line 28: --- 페이지 164 ---
Line 29: • Cohesive: It groups related concepts together and apart from unrelated
Line 30: concepts.
Line 31: • Confirmable: It can be easily verified with tests.
Line 32: Your unit tests provide you with that last facet of clean code.
Line 33: A Little Bit o’ Refactor
Line 34: Refactoring is a fancy way to indicate that you’re transforming the underlying
Line 35: structure of your code—its implementation details—while retaining its existing
Line 36: functional behavior. Since refactoring involves reshaping and moving code,
Line 37: you must ensure your system still works after such manipulations. Unit tests
Line 38: are the cheapest, fastest way to do so.
Line 39: Refactoring is to coding as editing is to writing. Even the best (expository)
Line 40: writers edit most sentences they write to make them immediately clear to
Line 41: readers. Coding is no different. Once you capture a solution in an editor, your
Line 42: code is often harder to follow than necessary.
Line 43: Writers follow the mindset to write first for themselves and then for others.
Line 44: To do so as a programmer, first, code your solution in a way that makes sense to
Line 45: you. Then, consider your teammates who must revisit your code at some
Line 46: point in the future. Rework your code to provide a clearer solution now while
Line 47: it still makes sense to you.
Line 48: Code in two steps: first, capture your thoughts in a correct solu-
Line 49: tion. Second, clarify your solution for others.
Line 50: Confidence is the key consideration when it comes to refactoring. Without
Line 51: the confidence that good unit tests provide, you’d want to be extremely cau-
Line 52: tious about “fixing” code that’s already working. In fact, without unit tests,
Line 53: you might think, “it ain’t broke. Don’t fix it.” Your code would start its life
Line 54: unedited—with deficiencies—and would get a little worse with each change.
Line 55: If you’ve followed the recommendations in this book, however, you can make
Line 56: changes willy-nilly. Did you think of a new name for a method, one that makes
Line 57: more sense? Rename it (ten seconds in a good IDE; perhaps minutes other-
Line 58: wise), run your tests, and know seconds later that nothing broke. Method too
Line 59: long and hard to follow? Extract a chunk of it to a new method, and run your
Line 60: tests. Method in the wrong place? Move it, run tests. You can make small
Line 61: improvements to your codebase all day long, each making it incrementally
Line 62: easier (cheaper) to work with.
Line 63: Chapter 8. Refactoring to Cleaner Code • 148
Line 64: report erratum  •  discuss
Line 65: 
Line 66: --- 페이지 165 ---
Line 67: An Opportunity for Refactoring
Line 68: The code you’ll clean up comes from iloveyouboss (albeit a different version
Line 69: of it). See Exacerbating a Threading Issue, on page 80 for an overview of the
Line 70: application. Take a look at the Profile class in iloveyouboss:
Line 71: utj3-refactor/01/src/main/java/iloveyouboss/Profile.java
Line 72: import java.util.*;
Line 73: import static iloveyouboss.Weight.*;
Line 74: public class Profile {
Line 75: private final Map<String,Answer> answers = new HashMap<>();
Line 76: private final String name;
Line 77: private int score;
Line 78: public Profile(String name) { this.name = name; }
Line 79: public void add(Answer... newAnswers) {
Line 80: for (var answer: newAnswers)
Line 81: answers.put(answer.questionText(), answer);
Line 82: }
Line 83: public boolean matches(Criteria criteria) {
Line 84: score = 0;
Line 85: var kill = false;
Line 86: var anyMatches = false;
Line 87: for (var criterion: criteria) {
Line 88: var answer = answers.get(criterion.answer().questionText());
Line 89: var match = criterion.weight() == IRRELEVANT ||
Line 90: ➤
Line 91: answer.match(criterion.answer());
Line 92: ➤
Line 93: if (!match && criterion.weight() == REQUIRED) {
Line 94: kill = true;
Line 95: }
Line 96: if (match) {
Line 97: score += criterion.weight().value();
Line 98: }
Line 99: anyMatches |= match;
Line 100: }
Line 101: if (kill) {
Line 102: return false;
Line 103: }
Line 104: return anyMatches;
Line 105: }
Line 106: public int score() { return score; }
Line 107: @Override
Line 108: public String toString() { return name; }
Line 109: }
Line 110: report erratum  •  discuss
Line 111: A Little Bit o’ Refactor • 149
Line 112: 
Line 113: --- 페이지 166 ---
Line 114: This class provides the beginnings of the core matching functionality. A Profile
Line 115: is comprised of answers to questions that prospective employees might ask
Line 116: about a company: Do you provide bonuses? Do you hire remote workers? Will
Line 117: you wash my dog for me? It exposes the core matching functionality through
Line 118: its matches method. The matches method takes on a Criteria object containing the
Line 119: preferred answers that a would-be employee has specified.
Line 120: The matches method isn’t particularly long, weighing in at around a dozen total
Line 121: lines of expressions and/or statements. Yet it’s reasonably dense, requiring
Line 122: attentive, stepwise reading. Spend a little time looking at matches to see if you
Line 123: can pin down what it does.
Line 124: Testing the class’s behavior sufficiently required seven unit tests:
Line 125: utj3-refactor/01/src/test/java/iloveyouboss/AProfile.java
Line 126: import org.junit.jupiter.api.*;
Line 127: import static iloveyouboss.Weight.*;
Line 128: import static iloveyouboss.YesNo.*;
Line 129: import static org.junit.jupiter.api.Assertions.*;
Line 130: class AProfile {
Line 131: Profile profile = new Profile("Geeks Inc.");
Line 132: Criteria criteria;
Line 133: Question freeLunch;
Line 134: Answer freeLunchYes;
Line 135: Answer freeLunchNo;
Line 136: Question bonus;
Line 137: Answer bonusYes;
Line 138: Answer bonusNo;
Line 139: Question hasGym;
Line 140: Answer hasGymNo;
Line 141: Answer hasGymYes;
Line 142: String[] NO_YES = {NO.toString(), YES.toString()};
Line 143: @BeforeEach
Line 144: void createQuestionsAndAnswers() {
Line 145: bonus = new Question("Bonus?", NO_YES, 1);
Line 146: bonusYes = new Answer(bonus, YES);
Line 147: bonusNo = new Answer(bonus, NO);
Line 148: freeLunch = new Question("Free lunch?", NO_YES, 1);
Line 149: freeLunchYes = new Answer(freeLunch, YES);
Line 150: freeLunchNo = new Answer(freeLunch, NO);
Line 151: hasGym = new Question("Gym?", NO_YES, 1);
Line 152: hasGymYes = new Answer(hasGym, YES);
Line 153: hasGymNo = new Answer(hasGym, NO);
Line 154: }
Line 155: Chapter 8. Refactoring to Cleaner Code • 150
Line 156: report erratum  •  discuss
Line 157: 
Line 158: --- 페이지 167 ---
Line 159: @Nested
Line 160: class DoesNotMatch {
Line 161: @Test
Line 162: void whenAnyRequiredCriteriaNotMet() {
Line 163: profile.add(freeLunchNo, bonusYes);
Line 164: criteria = new Criteria(
Line 165: new Criterion(freeLunchYes, REQUIRED),
Line 166: new Criterion(bonusYes, IMPORTANT));
Line 167: var matches = profile.matches(criteria);
Line 168: assertFalse(matches);
Line 169: }
Line 170: @Test
Line 171: void whenNoneOfMultipleCriteriaMatch() {
Line 172: profile.add(bonusNo, freeLunchNo);
Line 173: criteria = new Criteria(
Line 174: new Criterion(bonusYes, IMPORTANT),
Line 175: new Criterion(freeLunchYes, IMPORTANT));
Line 176: var matches = profile.matches(criteria);
Line 177: assertFalse(matches);
Line 178: }
Line 179: }
Line 180: @Nested
Line 181: class Matches {
Line 182: @Test
Line 183: void whenCriteriaIrrelevant() {
Line 184: profile.add(freeLunchNo);
Line 185: criteria = new Criteria(
Line 186: new Criterion(freeLunchYes, IRRELEVANT));
Line 187: var matches = profile.matches(criteria);
Line 188: assertTrue(matches);
Line 189: }
Line 190: @Test
Line 191: void whenAnyOfMultipleCriteriaMatch() {
Line 192: profile.add(bonusYes, freeLunchNo);
Line 193: criteria = new Criteria(
Line 194: new Criterion(bonusYes, IMPORTANT),
Line 195: new Criterion(freeLunchYes, IMPORTANT));
Line 196: var matches = profile.matches(criteria);
Line 197: assertTrue(matches);
Line 198: }
Line 199: }
Line 200: report erratum  •  discuss
Line 201: A Little Bit o’ Refactor • 151
Line 202: 
Line 203: --- 페이지 168 ---
Line 204: @Nested
Line 205: class Score {
Line 206: @Test
Line 207: void isZeroWhenThereAreNoMatches() {
Line 208: profile.add(bonusNo);
Line 209: criteria = new Criteria(
Line 210: new Criterion(bonusYes, IMPORTANT));
Line 211: profile.matches(criteria);
Line 212: assertEquals(0, profile.score());
Line 213: }
Line 214: @Test
Line 215: void doesNotIncludeUnmetRequiredCriteria() {
Line 216: profile.add(bonusNo, freeLunchYes);
Line 217: criteria = new Criteria(
Line 218: new Criterion(bonusYes, REQUIRED),
Line 219: new Criterion(freeLunchYes, IMPORTANT));
Line 220: profile.matches(criteria);
Line 221: assertEquals(IMPORTANT.value(), profile.score());
Line 222: }
Line 223: @Test
Line 224: void equalsCriterionValueForSingleMatch() {
Line 225: profile.add(bonusYes);
Line 226: criteria = new Criteria(
Line 227: new Criterion(bonusYes, IMPORTANT));
Line 228: profile.matches(criteria);
Line 229: assertEquals(IMPORTANT.value(), profile.score());
Line 230: }
Line 231: @Test
Line 232: void sumsCriterionValuesForMatches() {
Line 233: profile.add(bonusYes, freeLunchYes, hasGymNo);
Line 234: criteria = new Criteria(
Line 235: new Criterion(bonusYes, IMPORTANT),
Line 236: new Criterion(freeLunchYes, NICE_TO_HAVE),
Line 237: new Criterion(hasGymYes, VERY_IMPORTANT));
Line 238: profile.matches(criteria);
Line 239: assertEquals(IMPORTANT.value() + NICE_TO_HAVE.value(),
Line 240: profile.score());
Line 241: }
Line 242: }
Line 243: }
Line 244: The tests’ examples should help you understand the Profile class.
Line 245: Chapter 8. Refactoring to Cleaner Code • 152
Line 246: report erratum  •  discuss
Line 247: 
Line 248: --- 페이지 169 ---
Line 249: Extract Method: Your Second-Best Refactoring Friend
Line 250: Before this section’s heading sends you digging in the index, your best
Line 251: refactoring friend is rename, whether it be a class, method, or variable of any
Line 252: sort. Clarity is largely about declaration of intent, and good names are what
Line 253: impart clarity best in code.
Line 254: Your goal: reduce complexity in matches so you can readily understand what
Line 255: it’s responsible for. The method is currently a jumble of code that obscures
Line 256: the overall set of steps required—its algorithm or policy. You’ll shift the code
Line 257: from “implementation detail” to “clear declarations” by extracting detailed bits
Line 258: of logic to new, separate methods.
Line 259: Conditional expressions often read poorly, particularly when they are com-
Line 260: plex. An example is the assignment to match that appears atop the for loop
Line 261: in matches:
Line 262: utj3-refactor/01/src/main/java/iloveyouboss/Profile.java
Line 263: public boolean matches(Criteria criteria) {
Line 264: // ...
Line 265: for (var criterion: criteria) {
Line 266: var answer = answers.get(criterion.answer().questionText());
Line 267: var match = criterion.weight() == IRRELEVANT ||
Line 268: ➤
Line 269: answer.match(criterion.answer());
Line 270: ➤
Line 271: // ...
Line 272: }
Line 273: }
Line 274: The right-hand side of the assignment seemingly defines when there’s a match.
Line 275: Specifically, it says there’s a match either when the criterion is irrelevant or
Line 276: when the criterion’s answer matches the corresponding answer in the profile.
Line 277: Isolate this complexity by extracting it to a separate method named isMatch.
Line 278: In IntelliJ IDEA, extract methods by following these mouse-heavy steps:
Line 279: 1.
Line 280: Highlight the appropriate code.
Line 281: 2.
Line 282: Open the context menu (via right-click).
Line 283: 3.
Line 284: Select Refactor ▶ Extract Method from the menu.
Line 285: 4.
Line 286: Type a name for the new method (or accept the one suggested).
Line 287: 5.
Line 288: Press Enter.
Line 289: IntelliJ creates a method containing the highlighted code and then replaces
Line 290: the highlighted code with a call to the new method.
Line 291: report erratum  •  discuss
Line 292: A Little Bit o’ Refactor • 153
Line 293: 
Line 294: --- 페이지 170 ---
Line 295: After extracting isMatches, you’re left with a simple declaration in matches and
Line 296: a short helper method in the Profile class:
Line 297: utj3-refactor/02/src/main/java/iloveyouboss/Profile.java
Line 298: for (var criterion: criteria) {
Line 299: var answer = answers.get(criterion.answer().questionText());
Line 300: var match = isMatch(criterion, answer);
Line 301: ➤
Line 302: // ...
Line 303: }
Line 304: utj3-refactor/02/src/main/java/iloveyouboss/Profile.java
Line 305: private boolean isMatch(Criterion criterion, Answer answer) {
Line 306: return criterion.weight() == IRRELEVANT ||
Line 307: answer.match(criterion.answer());
Line 308: }
Line 309: The loop’s code is one step closer to showing only high-level policy and de-
Line 310: emphasizing lower-level details. The isMatch method provides the specifics
Line 311: about whether an individual criterion is a match for an answer.
Line 312: It’s too easy to break behavior when moving code about, sometimes, even
Line 313: when your IDE moves it for you. After making this change, run all the tests
Line 314: to ensure they still pass. Good tests provide confidence to make countless
Line 315: small changes. You’ll know the moment you introduce a sneaky little defect.
Line 316: With each small change, run your fast set of tests for confidence.
Line 317: It’s cheap, easy, and gratifying.
Line 318: The ability to move code about safely is one of the most important benefits
Line 319: of unit testing. You can add new features safely as well as shape the code
Line 320: toward a better design. In the absence of sufficient tests, you’ll tend to make
Line 321: fewer changes or changes that are highly risky.
Line 322: Finding Better Homes for Your Methods
Line 323: Your loop is a bit easier to read—great! But code in the newly extracted isMatch
Line 324: method has nothing to do with the Profile object itself—it interacts with Answer
Line 325: and Criterion objects. One of those two classes is probably a better place for
Line 326: the isMatch behavior.
Line 327: Criterion objects already know about Answer objects, but Answer isn’t dependent
Line 328: on Criterion. As such, move the newly extracted matches method to the Criterion
Line 329: record. Moving it to Answer would create a bidirectional dependency with Answer
Line 330: and Criterion objects depending on each other. Such a tight coupling would
Line 331: Chapter 8. Refactoring to Cleaner Code • 154
Line 332: report erratum  •  discuss
Line 333: 
Line 334: --- 페이지 171 ---
Line 335: mean that changes to either type could propagate to the other, which in turn
Line 336: could create other problems.
Line 337: In IntelliJ IDEA, move the method by following these steps:
Line 338: 1.
Line 339: Click its name.
Line 340: 2.
Line 341: Open the context menu (via right-click).
Line 342: 3.
Line 343: Select Refactor ▶ Move Instance Method from the menu.
Line 344: 4.
Line 345: Select the instance expression Criterion criterion.
Line 346: 5.
Line 347: Press Enter.
Line 348: Here’s isMatch in its new home:
Line 349: utj3-refactor/03/src/main/java/iloveyouboss/Criterion.java
Line 350: import static iloveyouboss.Weight.IRRELEVANT;
Line 351: public record Criterion(Answer answer, Weight weight) {
Line 352: boolean isMatch(Answer answer) {
Line 353: ➤
Line 354: return weight() == IRRELEVANT || answer.match(answer());
Line 355: }
Line 356: }
Line 357: And here’s what the loop looks like after the move:
Line 358: utj3-refactor/03/src/main/java/iloveyouboss/Profile.java
Line 359: for (var criterion: criteria) {
Line 360: var answer = answers.get(criterion.answer().questionText());
Line 361: var match = criterion.isMatch(answer);
Line 362: ➤
Line 363: if (!match && criterion.weight() == REQUIRED) {
Line 364: kill = true;
Line 365: }
Line 366: if (match) {
Line 367: score += criterion.weight().value();
Line 368: }
Line 369: anyMatches |= match;
Line 370: }
Line 371: The expression assigned to the answer local variable is hard to read because
Line 372: of the method chaining:
Line 373: utj3-refactor/03/src/main/java/iloveyouboss/Profile.java
Line 374: var answer = answers.get(criterion.answer().questionText());
Line 375: The code asks criterion for its answer object and then asks the answer for its
Line 376: question text. Better: ask the criterion to directly return the question text. As
Line 377: the first step toward that goal, extract the expression criterion.answer().questionText()
Line 378: to a new method named questionText:
Line 379: utj3-refactor/04/src/main/java/iloveyouboss/Profile.java
Line 380: public boolean matches(Criteria criteria) {
Line 381: // ...
Line 382: report erratum  •  discuss
Line 383: Finding Better Homes for Your Methods • 155
Line 384: 
Line 385: --- 페이지 172 ---
Line 386: for (var criterion: criteria) {
Line 387: var answer = answers.get(questionText(criterion));
Line 388: ➤
Line 389: // ...
Line 390: }
Line 391: // ...
Line 392: }
Line 393: private String questionText(Criterion criterion) {
Line 394: ➤
Line 395: return criterion.answer().questionText();
Line 396: }
Line 397: Now move questionText to the Criterion class. If you move it via IDEA’s automated
Line 398: refactoring support, select Criterion criterion as the instance expression.
Line 399: The method disappears from Profile. The expression assigned to the answer local
Line 400: variable no longer involves method chaining:
Line 401: utj3-refactor/05/src/main/java/iloveyouboss/Profile.java
Line 402: public boolean matches(Criteria criteria) {
Line 403: // ...
Line 404: for (var criterion: criteria) {
Line 405: var answer = answers.get(criterion.questionText());
Line 406: ➤
Line 407: // ...
Line 408: }
Line 409: // ...
Line 410: }
Line 411: Criterion is now responsible for retrieving and returning the question text:
Line 412: utj3-refactor/05/src/main/java/iloveyouboss/Criterion.java
Line 413: import static iloveyouboss.Weight.IRRELEVANT;
Line 414: public record Criterion(Answer answer, Weight weight) {
Line 415: // ...
Line 416: String questionText() {
Line 417: return answer().questionText();
Line 418: }
Line 419: }
Line 420: Next, extract the whole right-hand side of the answer assignment to a method
Line 421: that helps explain what the answer represents:
Line 422: utj3-refactor/06/src/main/java/iloveyouboss/Profile.java
Line 423: public boolean matches(Criteria criteria) {
Line 424: // ...
Line 425: for (var criterion: criteria) {
Line 426: var answer = profileAnswerMatching(criterion);
Line 427: ➤
Line 428: var match = criterion.isMatch(answer);
Line 429: // ...
Line 430: }
Line 431: // ...
Line 432: }
Line 433: Chapter 8. Refactoring to Cleaner Code • 156
Line 434: report erratum  •  discuss
Line 435: 
Line 436: --- 페이지 173 ---
Line 437: private Answer profileAnswerMatching(Criterion criterion) {
Line 438: ➤
Line 439: return answers.get(criterion.questionText());
Line 440: }
Line 441: Each extract method you do increases the conciseness of matches bit by bit.
Line 442: Using intention-revealing names for the new methods also increases the
Line 443: clarity of matches. The new methods also represent opportunities to move
Line 444: responsibilities to where they belong. Profile gets simpler while the previously
Line 445: barren Criterion builds up its usefulness.
Line 446: Removing Temporaries of Little Value
Line 447: Temporary variables (“temps”) have a number of uses. They can cache the
Line 448: value of an expensive computation or collect things that change throughout
Line 449: the body of a method. A temp can also clarify the intent of code—a valid choice
Line 450: even if it’s used only once.
Line 451: In matches, the answer local variable provides none of those three benefits. You
Line 452: can inline such a pointless variable by replacing any occurrences of it with
Line 453: the answerMatching(criterion) expression. In IntelliJ IDEA, inline a variable by fol-
Line 454: lowing these steps:
Line 455: 1.
Line 456: Click its name.
Line 457: 2.
Line 458: Open the context menu (via right-click).
Line 459: 3.
Line 460: Select Refactor ▶ Inline Variable from the menu.
Line 461: Any references to the variable are replaced with the right-hand side of the
Line 462: assignment. The assignment statement disappears:
Line 463: utj3-refactor/07/src/main/java/iloveyouboss/Profile.java
Line 464: public boolean matches(Criteria criteria) {
Line 465: // ...
Line 466: for (var criterion: criteria) {
Line 467: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 468: ➤
Line 469: // ...
Line 470: }
Line 471: // ...
Line 472: }
Line 473: The true intent for match can be understood directly. Paraphrasing: a match
Line 474: exists when the criterion is a match for the corresponding profile answer.
Line 475: Speeding Up with Automated Refactoring
Line 476: You can, of course, do this or any other refactoring manually, cutting and
Line 477: pasting little bits of code until you reach the same outcome. But once you’ve
Line 478: report erratum  •  discuss
Line 479: Removing Temporaries of Little Value • 157
Line 480: 
Line 481: --- 페이지 174 ---
Line 482: learned that a good IDE can do the job at least ten times as fast, it makes
Line 483: little sense not to take advantage of that power.
Line 484: More importantly, you can trust that (in Java, at least) an automated refac-
Line 485: toring generally will not break code. You’re far more likely to mess up along
Line 486: the way through a manual refactoring. Java automated refactorings are code
Line 487: transformations that have been proven in all senses of the word.
Line 488: You can further speed up by using the keyboard shortcuts for each automated
Line 489: refactoring rather than click through menus and dialogs. Throughout your
Line 490: development day, you’ll find heavy use for a small number of core automated
Line 491: refactorings: introduce variable/constant/field/parameter, extract method,
Line 492: inline method, inline variable, move method, and change signature. It won’t
Line 493: take long to ingrain the corresponding shortcuts. You can reduce most
Line 494: refactoring operations to about three to four seconds from 10 seconds or more
Line 495: (clicking through the UI) or from several minutes (manually).
Line 496: Lucky you: 20 years ago, most Java programmers manually moved code about
Line 497: in highly unsafe ways. Thirty years ago, automated refactoring tools didn’t
Line 498: exist. Today, the power and speed they grant can’t be overstated. You can
Line 499: watch the computer do the dirty work and know that your code still works.
Line 500: Amplifying the Core Intent of Code
Line 501: Let’s re-examine the slightly improved matches method:
Line 502: utj3-refactor/07/src/main/java/iloveyouboss/Profile.java
Line 503: public boolean matches(Criteria criteria) {
Line 504: score = 0;
Line 505: var kill = false;
Line 506: var anyMatches = false;
Line 507: for (var criterion: criteria) {
Line 508: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 509: if (!match && criterion.weight() == REQUIRED) {
Line 510: kill = true;
Line 511: }
Line 512: if (match) {
Line 513: score += criterion.weight().value();
Line 514: }
Line 515: anyMatches |= match;
Line 516: }
Line 517: if (kill)
Line 518: return false;
Line 519: return anyMatches;
Line 520: }
Line 521: Chapter 8. Refactoring to Cleaner Code • 158
Line 522: report erratum  •  discuss
Line 523: 
Line 524: --- 페이지 175 ---
Line 525: Careful reading reveals the following outcomes:
Line 526: • Return true if any criterion matches, false if none do.
Line 527: • Calculate the score by summing the weights of matching criteria.
Line 528: • Return false when any required criterion does not match the corresponding
Line 529: profile answer.
Line 530: Let’s restructure matches to directly emphasize these three core concepts.
Line 531: Extract Concept: Any Matches Exist?
Line 532: The determination of whether any matches exist is scattered through the
Line 533: method. It involves both the anyMatches and matches local variables:
Line 534: utj3-refactor/08/src/main/java/iloveyouboss/Profile.java
Line 535: public boolean matches(Criteria criteria) {
Line 536: score = 0;
Line 537: var kill = false;
Line 538: var anyMatches = false;
Line 539: ➤
Line 540: for (var criterion: criteria) {
Line 541: ➤
Line 542: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 543: ➤
Line 544: if (!match && criterion.weight() == REQUIRED) {
Line 545: kill = true;
Line 546: }
Line 547: if (match) {
Line 548: score += criterion.weight().value();
Line 549: }
Line 550: anyMatches |= match;
Line 551: ➤
Line 552: }
Line 553: if (kill)
Line 554: return false;
Line 555: return anyMatches;
Line 556: ➤
Line 557: }
Line 558: Your goal: move all the logic related to making that determination to its own
Line 559: method. Here are the steps:
Line 560: 1.
Line 561: Change the return statement to return the result of calling a new method,
Line 562: anyMatches().
Line 563: 2.
Line 564: Create a new method, anyMatches, that returns a Boolean value.
Line 565: 3.
Line 566: Copy (don’t cut) the relevant logic into the new method.
Line 567: The result:
Line 568: utj3-refactor/09/src/main/java/iloveyouboss/Profile.java
Line 569: public boolean matches(Criteria criteria) {
Line 570: score = 0;
Line 571: report erratum  •  discuss
Line 572: Amplifying the Core Intent of Code • 159
Line 573: 
Line 574: --- 페이지 176 ---
Line 575: var kill = false;
Line 576: var anyMatches = false;
Line 577: for (var criterion: criteria) {
Line 578: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 579: if (!match && criterion.weight() == REQUIRED) {
Line 580: kill = true;
Line 581: }
Line 582: if (match) {
Line 583: score += criterion.weight().value();
Line 584: }
Line 585: anyMatches |= match;
Line 586: }
Line 587: if (kill)
Line 588: return false;
Line 589: return anyMatches(criteria);
Line 590: ➤
Line 591: }
Line 592: private boolean anyMatches(Criteria criteria) {
Line 593: ➤
Line 594: var anyMatches = false;
Line 595: for (var criterion: criteria) {
Line 596: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 597: anyMatches |= match;
Line 598: }
Line 599: return anyMatches;
Line 600: }
Line 601: There’s no automated refactoring for this change. You’re making riskier
Line 602: manual changes, so run your tests! Once they pass, remove the two lines of
Line 603: code in matches that reference the anyMatches variable:
Line 604: utj3-refactor/10/src/main/java/iloveyouboss/Profile.java
Line 605: public boolean matches(Criteria criteria) {
Line 606: score = 0;
Line 607: var kill = false;
Line 608: for (var criterion: criteria) {
Line 609: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 610: if (!match && criterion.weight() == REQUIRED) {
Line 611: kill = true;
Line 612: }
Line 613: if (match) {
Line 614: score += criterion.weight().value();
Line 615: }
Line 616: }
Line 617: if (kill)
Line 618: return false;
Line 619: return anyMatches(criteria);
Line 620: }
Line 621: Chapter 8. Refactoring to Cleaner Code • 160
Line 622: report erratum  •  discuss
Line 623: 
Line 624: --- 페이지 177 ---
Line 625: The loop, of course, must remain and so must the line of code that assigns
Line 626: to the match variable.
Line 627: You might be concerned about that method extraction and its performance
Line 628: implications. We’ll discuss.
Line 629: Extract Concept: Calculate Score for Matches
Line 630: Now that you’ve isolated the anyMatches logic by extracting it to a new method,
Line 631: you can do the same for the code that calculates the score. If you put the call
Line 632: to calculateScore below if (kill) return false, however, the tests break. (The score
Line 633: needs to be calculated before any unmet required criterion results in an
Line 634: aborted method.)
Line 635: utj3-refactor/11/src/main/java/iloveyouboss/Profile.java
Line 636: public boolean matches(Criteria criteria) {
Line 637: calculateScore(criteria);
Line 638: ➤
Line 639: var kill = false;
Line 640: for (var criterion: criteria) {
Line 641: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 642: if (!match && criterion.weight() == REQUIRED) {
Line 643: kill = true;
Line 644: }
Line 645: }
Line 646: if (kill)
Line 647: return false;
Line 648: return anyMatches(criteria);
Line 649: }
Line 650: private void calculateScore(Criteria criteria) {
Line 651: ➤
Line 652: score = 0;
Line 653: for (var criterion: criteria) {
Line 654: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 655: if (match) {
Line 656: score += criterion.weight().value();
Line 657: }
Line 658: }
Line 659: }
Line 660: Hmmm. You might be wondering if you’re creating performance problems.
Line 661: Extract Concept: Return False When Required Criterion Not Met
Line 662: The code remaining in the loop aborts method execution if the profile doesn’t
Line 663: match a required criterion, returning false. Similarly, extract this logic to a
Line 664: new method, anyRequiredCriteriaNotMet:
Line 665: report erratum  •  discuss
Line 666: Amplifying the Core Intent of Code • 161
Line 667: 
Line 668: --- 페이지 178 ---
Line 669: utj3-refactor/12/src/main/java/iloveyouboss/Profile.java
Line 670: public boolean matches(Criteria criteria) {
Line 671: calculateScore(criteria);
Line 672: var kill = anyRequiredCriteriaNotMet(criteria);
Line 673: ➤
Line 674: if (kill)
Line 675: return false;
Line 676: return anyMatches(criteria);
Line 677: }
Line 678: private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
Line 679: ➤
Line 680: var kill = false;
Line 681: for (var criterion: criteria) {
Line 682: var match = criterion.isMatch(profileAnswerMatching(criterion));
Line 683: if (!match && criterion.weight() == REQUIRED) {
Line 684: kill = true;
Line 685: }
Line 686: }
Line 687: return kill;
Line 688: }
Line 689: Matches is now five lines of code and fairly easy to follow! But some cleanup
Line 690: work remains, particularly in the three newly extracted methods. For one,
Line 691: the loops are all old-school for-each loops. You’ll clean up these problems
Line 692: after we address the performance elephant in the room.
Line 693: The implementation for matches now involves three loops spread across three
Line 694: methods instead of a single loop through the criteria. That might seem horri-
Line 695: fying to you. We’ll come back to discuss the performance implications; for
Line 696: now, let’s talk about the benefits you gain with the new design.
Line 697: Earlier, you invested some time in carefully reading the original code in order
Line 698: to glean its three intents. The Boolean logic throughout created opportunities
Line 699: for confusion along the way. Now, matches (almost) directly states the method’s
Line 700: high-level goals.
Line 701: The implementation details for each of the three steps in the algorithm are
Line 702: hidden in the corresponding helper methods calculateScore, anyRequiredCriteriaNotMet,
Line 703: and anyMatches. Each helper method allows the necessary behavior to be
Line 704: expressed in a concise, isolated fashion, not cluttered with other concerns.
Line 705: Are You Kidding Me? Addressing Concerns
Line 706: over Performance
Line 707: At this point, you might be feeling a little perturbed. After refactoring the
Line 708: matches method, each of anyMatches, calculateScore, and anyRequiredCriteriaNotMet
Line 709: Chapter 8. Refactoring to Cleaner Code • 162
Line 710: report erratum  •  discuss
Line 711: 
Line 712: --- 페이지 179 ---
Line 713: iterates through the criterion collection. Your code now loops three times instead
Line 714: of one. You’ve potentially tripled the time to execute matches.
Line 715: Do you have a real performance problem relevant to the real requirements,
Line 716: or do you only suspect one exists? Many programmers speculate about where
Line 717: performance problems might lie and about what the best resolution might
Line 718: be. Unfortunately, such speculations can be quite wrong.
Line 719: Base all performance optimization attempts on real data, not
Line 720: speculation.
Line 721: The first answer to any potential performance problem is to measure. If under-
Line 722: standing performance characteristics is a pervasive and critical application
Line 723: concern, you want to do that analysis from the perspective of end-to-end
Line 724: functionality—more holistically—rather than at the level of individual unit or
Line 725: method performance. (You’ll still ultimately be narrowing down to a hopefully
Line 726: small number of methods that need to be fixed.) For such needs, you’ll want
Line 727: a tool like JMeter.
Line 728: 1 You can also incorporate JUnitPerf,
Line 729: 2 which allows you to
Line 730: write performance tests using JUnit.
Line 731: If you have an occasional concern about the performance of an individual
Line 732: unit, you can create a few “roll your own” performance probes. As long as
Line 733: you’re careful with your conclusions, they’ll be adequate for your needs.
Line 734: The following code runs in the context of a JUnit test (though it has no assertions
Line 735: and is currently not a test) and displays the number of milliseconds elapsed. The
Line 736: probe code creates a Criteria object with answers to 20 questions. It then loops a
Line 737: million times. Each loop creates a new Profile, adds randomized answers to the 20
Line 738: questions, and then determines whether or not the profile matches the criteria.
Line 739: utj3-refactor/12/src/test/java/iloveyouboss/AProfilePerformance.java
Line 740: import org.junit.jupiter.api.Test;
Line 741: import java.util.List;
Line 742: import java.util.Random;
Line 743: import java.util.concurrent.atomic.AtomicInteger;
Line 744: import java.util.function.Consumer;
Line 745: import static iloveyouboss.YesNo.*;
Line 746: import static java.util.stream.IntStream.range;
Line 747: class AProfilePerformance {
Line 748: int questionCount = 20;
Line 749: Random random = new Random();
Line 750: 1.
Line 751: http://jmeter.apache.org/
Line 752: 2.
Line 753: https://github.com/noconnor/JUnitPerf
Line 754: report erratum  •  discuss
Line 755: Are You Kidding Me? Addressing Concerns over Performance • 163
Line 756: 
Line 757: --- 페이지 180 ---
Line 758: @Test
Line 759: void executionTime() {
Line 760: ➤
Line 761: var questions = createQuestions();
Line 762: var criteria = new Criteria(createCriteria(questions));
Line 763: var iterations = 1_000_000;
Line 764: var matchCount = new AtomicInteger(0);
Line 765: var elapsedMs = time(iterations, i -> {
Line 766: var profile = new Profile("");
Line 767: profile.add(createAnswers(questions));
Line 768: if (profile.matches(criteria))
Line 769: matchCount.incrementAndGet();
Line 770: });
Line 771: System.out.println("elapsed: " + elapsedMs);
Line 772: System.out.println("matches: " + matchCount.get());
Line 773: }
Line 774: long time(int times, Consumer<Integer> func) {
Line 775: var start = System.nanoTime();
Line 776: range(0, times).forEach(i -> func.accept(i + 1));
Line 777: return (System.nanoTime() - start) / 1_000_000;
Line 778: }
Line 779: int numberOfWeights = Weight.values().length;
Line 780: Weight randomWeight() {
Line 781: if (isOneInTenTimesRandomly()) return Weight.REQUIRED;
Line 782: var nonRequiredWeightIndex =
Line 783: random.nextInt(numberOfWeights - 1) + 1;
Line 784: return Weight.values()[nonRequiredWeightIndex];
Line 785: }
Line 786: private boolean isOneInTenTimesRandomly() {
Line 787: return random.nextInt(10) == 0;
Line 788: }
Line 789: YesNo randomAnswer() {
Line 790: return random.nextInt() % 2 == 0 ? NO : YES;
Line 791: }
Line 792: Answer[] createAnswers(List<Question> questions) {
Line 793: return range(0, questionCount)
Line 794: .mapToObj(i -> new Answer(questions.get(i), randomAnswer()))
Line 795: .toArray(Answer[]::new);
Line 796: }
Line 797: List<Question> createQuestions() {
Line 798: String[] noYes = {NO.toString(), YES.toString()};
Line 799: return range(0, questionCount)
Line 800: .mapToObj(i -> new Question("" + i, noYes, i))
Line 801: .toList();
Line 802: }
Line 803: Chapter 8. Refactoring to Cleaner Code • 164
Line 804: report erratum  •  discuss
Line 805: 
Line 806: --- 페이지 181 ---
Line 807: List<Criterion> createCriteria(List<Question> questions) {
Line 808: return range(0, questionCount)
Line 809: .mapToObj(i -> new Criterion(new Answer(
Line 810: questions.get(i), randomAnswer()), randomWeight()))
Line 811: .toList();
Line 812: }
Line 813: }
Line 814: I ran the probe on an old laptop five times to shake out any issues around
Line 815: timing and the clock cycle. Execution time averaged at 1470ms.
Line 816: The iterations (1,000,000) and data size (20 questions) are arbitrary choices.
Line 817: You might choose numbers with some real-world credibility using actual
Line 818: production characteristics, but that’s not critical. Mostly, you want a sense
Line 819: of whether or not the degradation is significant enough to be concerned
Line 820: about.
Line 821: I also ran the probe against version 8 of the profile, which represents the code
Line 822: right before you started factoring into multiple loops. Execution time averaged
Line 823: at 1318ms (with a low standard deviation, under 3 percent).
Line 824: Execution time for the cleaner design represents an 11.5 percent increase for
Line 825: the new solution. It’s a sizeable amount, percentage-wise, but it’s not anywhere
Line 826: near three times worse due to the triple looping. For most people, it’s a non-
Line 827: issue, but you must decide if the degradation will create a real problem
Line 828: regarding end-user impact.
Line 829: Take care when doing this kind of probe. It’s possible to craft a probe that
Line 830: mischaracterizes reality. For example, Java can, at times, optimize out parts
Line 831: of the code you’re profiling.
Line 832: If you process very high volumes, performance may indeed be critical to the
Line 833: point where the degradation is too much. Ensure you measure after each
Line 834: optimization attempt and validate whether or not the optimization made
Line 835: enough of a difference.
Line 836: Optimized code can easily increase the cost of both understanding and
Line 837: changing a solution by an order of magnitude. A clean design can reveal intent
Line 838: in a handful of seconds, as opposed to a minute or more with an optimized
Line 839: design. Always derive a clean design and then optimize your code only if
Line 840: necessary.
Line 841: A clean design can provide more flexibility and opportunities for optimizing
Line 842: the code. Caching, for example, is a lot easier if the things being cached are
Line 843: isolated from other bits of code.
Line 844: report erratum  •  discuss
Line 845: Are You Kidding Me? Addressing Concerns over Performance • 165
Line 846: 
Line 847: --- 페이지 182 ---
Line 848: A clean design is your best starting point for optimization.
Line 849: Note: this probe is intended to be throw-away code. However, you might need
Line 850: to elevate it to your integration test suite, where it would fail if someone
Line 851: pushed a solution that violated the execution time threshold. To do so, you’d
Line 852: add an assertion that the probe finished in under x milliseconds. The challenge
Line 853: is determining what x should be, given likely varying execution contexts (dif-
Line 854: fering machines and differing loads, for example). One approach would involve
Line 855: calculating the threshold dynamically as part of test execution, using a
Line 856: baseline measurement of a simple, stable operation.
Line 857: Next up, you’ll change the for-each loops to use the Java streams interface.
Line 858: This refactoring, afforded by the tests, would allow you to parallelize the
Line 859: execution of a stream as one way to improve performance.
Line 860: Final Cleanup
Line 861: Let’s return to the fun and see how tight you can make the code.
Line 862: First, replace the old-school loops with Java streams. Start with anyMatches:
Line 863: utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
Line 864: private boolean anyMatches(Criteria criteria) {
Line 865: return criteria.stream()
Line 866: .anyMatch(criterion ->
Line 867: criterion.isMatch(profileAnswerMatching(criterion)));
Line 868: }
Line 869: To get that compiling and passing, you’ll need to add a stream method to the
Line 870: Criteria record:
Line 871: utj3-refactor/13/src/main/java/iloveyouboss/Criteria.java
Line 872: public Stream<Criterion> stream() {
Line 873: return criteria.stream();
Line 874: }
Line 875: Next, rework the calculateScore method:
Line 876: utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
Line 877: private void calculateScore(Criteria criteria) {
Line 878: score = criteria.stream()
Line 879: .filter(criterion ->
Line 880: criterion.isMatch(profileAnswerMatching(criterion)))
Line 881: .mapToInt(criterion -> criterion.weight().value())
Line 882: .sum();
Line 883: }
Line 884: Chapter 8. Refactoring to Cleaner Code • 166
Line 885: report erratum  •  discuss
Line 886: 
Line 887: --- 페이지 183 ---
Line 888: After cleaning up anyRequiredCriteriaNotMet similarly, it’s much simpler to follow
Line 889: without the (horribly named) kill temporary variable:
Line 890: utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
Line 891: private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
Line 892: return criteria.stream()
Line 893: .filter(criterion ->
Line 894: !criterion.isMatch(profileAnswerMatching(criterion)))
Line 895: .anyMatch(criterion -> criterion.weight() == REQUIRED);
Line 896: }
Line 897: You’ve supplanted all three loops. Delete the iterator method in the Criteria
Line 898: record.
Line 899: Finally, inline kill in the core matches method:
Line 900: utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
Line 901: public boolean matches(Criteria criteria) {
Line 902: calculateScore(criteria);
Line 903: if (anyRequiredCriteriaNotMet(criteria)) return false;
Line 904: return anyMatches(criteria);
Line 905: }
Line 906: You can capture that core four-line policy in a few other ways, but this
Line 907: approach reads fine.
Line 908: Summary
Line 909: It’s easy to write a lot of code quickly. It’s just as easy to let that code get dirty
Line 910: to the point where it becomes difficult to comprehend and navigate. Unit tests
Line 911: provide the safeguards you need to clean up messy code without breaking
Line 912: things.
Line 913: In this chapter, you learned techniques for keeping your system clean contin-
Line 914: ually to help you keep your system from degrading into a frustrating mess.
Line 915: You renamed variables and methods, you extracted smaller methods, you in-
Line 916: lined variables, and you replaced older Java constructs with newer ones. You
Line 917: might call this very incremental method-level cleanup “micro” refactoring—a
Line 918: programmer’s version of the continuous editing that a writer performs.
Line 919: Don’t let your code get to the point of the convoluted matches methods. Do
Line 920: recognize that difficult code like matches is rampant in most systems, and it
Line 921: doesn’t take long for developers to create it.
Line 922: As you begin to sweep away the small bits of dust in your system, you’ll start
Line 923: to see larger design concerns—problems related to the overall structure of
Line 924: the system and how its responsibilities are organized. Next up, you’ll learn
Line 925: report erratum  •  discuss
Line 926: Summary • 167
Line 927: 
Line 928: --- 페이지 184 ---
Line 929: how to lean on unit tests again to address these larger design concerns
Line 930: through “macro” refactoring.
Line 931: Right now, the code you refactored in matches clearly states what’s going on.
Line 932: But it also poses some concerns about the bigger design picture. The Profile
Line 933: class, for example, might be doing too much.
Line 934: In the next chapter, you’ll explore where your design falls flat. You’ll take
Line 935: advantage of your tests to support getting things back on track.
Line 936: Chapter 8. Refactoring to Cleaner Code • 168
Line 937: report erratum  •  discuss