Line 1: 
Line 2: --- 페이지 185 ---
Line 3: CHAPTER 9
Line 4: Refactoring Your Code’s Structure
Line 5: In the last chapter, you focused on refactoring the matches method into a
Line 6: number of more composed methods. You also focused on the clarity and
Line 7: conciseness of each method. This continual editing of small bits of code is a
Line 8: fundamental piece of design—you are making choices about how to implement
Line 9: a solution in a manner that keeps code comprehension and maintenance
Line 10: costs low.
Line 11: These are examples of “micro” design concerns:
Line 12: • How you capture state in fields
Line 13: • How you organize code into methods
Line 14: • How those methods interact with each other
Line 15: • How those methods interact with the external world
Line 16: To many developers, a software system’s design is mostly a “macro” concern:
Line 17: • How you organize classes into packages
Line 18: • How you organize methods into classes
Line 19: • How those classes interact with each other
Line 20: Both sets of concerns are relevant to the long-term maintainability of a system.
Line 21: One or both can be impacted any time you make a decision about how to
Line 22: organize and implement your code.
Line 23: A software system’s design is the combined collection of choices made at both
Line 24: macro and micro levels.
Line 25: You might be thinking, “This is a unit testing book. Why is this guy talking
Line 26: about design so much?”
Line 27: It turns out that writing unit tests isn’t an exercise that occurs in a vacuum.
Line 28: Your system’s design impacts your ability to write tests and vice versa. You
Line 29: might even consider the tests themselves a piece of the larger, continually
Line 30: report erratum  •  discuss
Line 31: 
Line 32: --- 페이지 186 ---
Line 33: shifting puzzle we call design. They provide confidence that your system’s
Line 34: design exhibits the most important aspect of design—that it supports a correct
Line 35: solution, working as intended.
Line 36: The most important aspect of a system’s design is that it works
Line 37: as intended.
Line 38: In this chapter, you’ll focus on bigger design concerns:
Line 39: • The Single Responsibility Principle (SRP) guides you to small classes that
Line 40: do one core thing to increase flexibility and ease of testing, among other
Line 41: things.
Line 42: • The command-query separation (CQS) principle says to design methods
Line 43: that do one of creating a side effect or returning a value but never both
Line 44: • Refactoring the production code toward a better design. When refactoring,
Line 45: change one of either production code or tests at a time and never both.
Line 46: Perhaps you noticed a focus on the notion of “one” in that list. It’s not a
Line 47: coincidence; it’s a core mentality in incremental software development.
Line 48: One Thing At A Time (OTAAT).
Line 49: You’ll apply these principles by refactoring code in the Profile class.
Line 50: The Profile Class and the SRP
Line 51: Take a look at the Profile class:
Line 52: utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
Line 53: import java.util.HashMap;
Line 54: import java.util.Map;
Line 55: import static iloveyouboss.Weight.REQUIRED;
Line 56: public class Profile {
Line 57: private final Map<String,Answer> answers = new HashMap<>();
Line 58: private final String name;
Line 59: private int score;
Line 60: public Profile(String name) { this.name = name; }
Line 61: public void add(Answer... newAnswers) {
Line 62: for (var answer: newAnswers)
Line 63: answers.put(answer.questionText(), answer);
Line 64: }
Line 65: Chapter 9. Refactoring Your Code’s Structure • 170
Line 66: report erratum  •  discuss
Line 67: 
Line 68: --- 페이지 187 ---
Line 69: public boolean matches(Criteria criteria) {
Line 70: calculateScore(criteria);
Line 71: if (anyRequiredCriteriaNotMet(criteria)) return false;
Line 72: return anyMatches(criteria);
Line 73: }
Line 74: private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
Line 75: return criteria.stream()
Line 76: .filter(criterion ->
Line 77: !criterion.isMatch(profileAnswerMatching(criterion)))
Line 78: .anyMatch(criterion -> criterion.weight() == REQUIRED);
Line 79: }
Line 80: private void calculateScore(Criteria criteria) {
Line 81: score = criteria.stream()
Line 82: .filter(criterion ->
Line 83: criterion.isMatch(profileAnswerMatching(criterion)))
Line 84: .mapToInt(criterion -> criterion.weight().value())
Line 85: .sum();
Line 86: }
Line 87: private boolean anyMatches(Criteria criteria) {
Line 88: return criteria.stream()
Line 89: .anyMatch(criterion ->
Line 90: criterion.isMatch(profileAnswerMatching(criterion)));
Line 91: }
Line 92: private Answer profileAnswerMatching(Criterion criterion) {
Line 93: return answers.get(criterion.questionText());
Line 94: }
Line 95: public int score() { return score; }
Line 96: @Override
Line 97: public String toString() { return name; }
Line 98: }
Line 99: At under seventy source lines, Profile doesn’t seem inordinately large or
Line 100: excessively complex. But it hints at less-than-ideal design.
Line 101: Profile tracks and manages information for a company or person, including a
Line 102: name and a collection of answers to questions. This set of information that
Line 103: Profile captures will need to change over time—more information will need to
Line 104: be added, and some might need to be removed or altered.
Line 105: As a secondary responsibility, Profile calculates a score to indicate if—and to
Line 106: what extent—a set of criteria matches the profile. With the refactoring you
Line 107: accomplished in the previous chapter, you ended up with a number of
Line 108: methods that directly support the matches method. Changes to the Profile class
Line 109: report erratum  •  discuss
Line 110: The Profile Class and the SRP • 171
Line 111: 
Line 112: --- 페이지 188 ---
Line 113: are thus probable for a second reason: you’ll undoubtedly change the
Line 114: sophistication of your matching algorithm over time.
Line 115: The Profile class violates the Single Responsibility Principle (SRP) of object-
Line 116: oriented class design, which says classes should have only one reason to change.
Line 117: (The SRP is one of a set of class design principles—see the following sidebar.)
Line 118: Focusing on the SRP decreases the risk of change. The more responsibilities a
Line 119: class has, the easier it is to break other existing behaviors when changing code
Line 120: within the class.
Line 121: SOLID Class-Design Principles
Line 122: In the mid-1990s, Robert C. Martin gathered five principles for object-oriented class
Line 123: design, presenting them as the best guidelines for building a maintainable object-
Line 124: oriented system. Michael Feathers attached the acronym SOLID to these principles
Line 125: in the early 2000s.a
Line 126: • Single Responsibility Principle (SRP). Classes should have one reason to change.
Line 127: Keep your classes small and single-purposed.
Line 128: • Open-Closed Principle (OCP). Design classes to be open for extension but closed
Line 129: for modification. Minimize the need to make changes to existing classes.
Line 130: • Liskov Substitution Principle (LSP). Subtypes should be substitutable for their
Line 131: base types. Method overrides shouldn’t break a client’s expectations for behavior.
Line 132: • Interface Segregation Principle (ISP). Clients shouldn’t have to depend on methods
Line 133: they don’t use. Split a larger interface into a number of smaller interfaces.
Line 134: • Dependency Inversion Principle (DIP). High-level modules should not depend on
Line 135: low-level modules; both should depend on abstractions. Abstractions should not
Line 136: depend on details; details should depend on abstractions.
Line 137: a.
Line 138: http://en.wikipedia.org/wiki/SOLID_(object-oriented_design)
Line 139: Smaller, more focused classes more readily provide value in another context—
Line 140: re-use! In contrast, a very large class with lots of responsibilities cannot
Line 141: possibly be used in other contexts.
Line 142: Underlying the SOLID principles are the concepts of cohesion and coupling.
Line 143: Classes in your systems should exhibit high cohesion and low coupling. Such
Line 144: systems make change easier, and they also make unit testing easier.
Line 145: The concepts of SOLID, low coupling, and high cohesion are not new, but
Line 146: they’re also not “outdated.” Despite some post-modern ideas about software
Line 147: design, these principles remain valid. They’re not absolutes: all choices in
Line 148: software systems represent tradeoffs. You must balance the principles with
Line 149: Chapter 9. Refactoring Your Code’s Structure • 172
Line 150: report erratum  •  discuss
Line 151: 
Line 152: --- 페이지 189 ---
Line 153: each other, with other considerations (like performance), and with other cir-
Line 154: cumstances or constraints of your reality.
Line 155: Extracting a New Class
Line 156: The Profile class defines two responsibilities:
Line 157: • Track information about a profile.
Line 158: • Determine whether and to what extent a set of criteria matches a profile.
Line 159: To improve your system’s design, you’ll split responsibilities into two classes,
Line 160: each small and adherent to the SRP. To do so, you’ll extract the code related
Line 161: to the profile-matching behavior to another class, Matcher. As with all refactor-
Line 162: ing, you’ll take an incremental path—make a small change and then run the
Line 163: tests to make sure they still pass.
Line 164: For your first change, move the calculateScore logic into Matcher. Start by changing
Line 165: the code in matches to declare your intent: rather than call calculateScore directly
Line 166: from matches, construct a new Matcher object with the information it needs—the
Line 167: hash map of answers and the criteria—and ask it for the score. Assign that
Line 168: returned score to the score field:
Line 169: utj3-refactor/14/src/main/java/iloveyouboss/Profile.java
Line 170: public boolean matches(Criteria criteria) {
Line 171: score = new Matcher(criteria, answers).score();
Line 172: ➤
Line 173: if (anyRequiredCriteriaNotMet(criteria)) return false;
Line 174: return anyMatches(criteria);
Line 175: }
Line 176: Copy (don’t cut it just yet) the calculateScore method from Profile into Matcher. In
Line 177: the constructor of Matcher, first, store the answers argument in a field. Then,
Line 178: call the calculateStore method, passing it the Criteria object that was passed to
Line 179: the constructor.
Line 180: Add a score field and a score() accessor method to return it.
Line 181: Compilation at this point reveals that calculateScore() needs to call profileAnswer-
Line 182: Matching(). Copy over that method.
Line 183: Your Matcher class should now look like the following:
Line 184: utj3-refactor/14/src/main/java/iloveyouboss/Matcher.java
Line 185: import java.util.Map;
Line 186: public class Matcher {
Line 187: private final Map<String, Answer> answers;
Line 188: private int score;
Line 189: report erratum  •  discuss
Line 190: Extracting a New Class • 173
Line 191: 
Line 192: --- 페이지 190 ---
Line 193: public Matcher(Criteria criteria, Map<String, Answer> answers) {
Line 194: this.answers = answers;
Line 195: calculateScore(criteria);
Line 196: }
Line 197: private void calculateScore(Criteria criteria) {
Line 198: score = criteria.stream()
Line 199: .filter(criterion ->
Line 200: criterion.isMatch(profileAnswerMatching(criterion)))
Line 201: .mapToInt(criterion -> criterion.weight().value())
Line 202: .sum();
Line 203: }
Line 204: private Answer profileAnswerMatching(Criterion criterion) {
Line 205: return answers.get(criterion.questionText());
Line 206: }
Line 207: public int score() {
Line 208: return score;
Line 209: }
Line 210: }
Line 211: Both Profile and Matcher now compile. Your tests should run successfully.
Line 212: The code in Profile no longer uses the calculateScore private method. Delete it. The
Line 213: profileAnswerMatching method is still used by code in Profile. Indicate that it’s
Line 214: duplicated elsewhere with a comment. If profileAnswerMatching is still needed by
Line 215: both classes after you finish moving code about, you’ll want to factor that
Line 216: code to a single place.
Line 217: Moving Matches Functionality to Matcher
Line 218: You’ve delegated the scoring responsibility to Matcher and invoked it from
Line 219: matches. The other code in matches represents the second goal of the method—to
Line 220: answer true or false depending on whether the criteria match the set of answers.
Line 221: Matcher represents a more appropriate home for that matches logic. Let’s simi-
Line 222: larly delegate the matching responsibility to the Matcher class.
Line 223: You can tackle this refactoring in many ways. Let’s take one small step at a
Line 224: time.
Line 225: utj3-refactor/15/src/main/java/iloveyouboss/Profile.java
Line 226: public boolean matches(Criteria criteria) {
Line 227: score = new Matcher(criteria, answers).score();
Line 228: if (anyRequiredCriteriaNotMet(criteria)) return false;
Line 229: ➤
Line 230: ➤
Line 231: return anyMatches(criteria);
Line 232: ➤
Line 233: }
Line 234: Chapter 9. Refactoring Your Code’s Structure • 174
Line 235: report erratum  •  discuss
Line 236: 
Line 237: --- 페이지 191 ---
Line 238: Extract the two highlighted lines to a method with a name other than matches,
Line 239: which is already used. How about isMatchFor?
Line 240: utj3-refactor/16/src/main/java/iloveyouboss/Profile.java
Line 241: public boolean matches(Criteria criteria) {
Line 242: score = new Matcher(criteria, answers).score();
Line 243: return isMatchFor(criteria);
Line 244: ➤
Line 245: }
Line 246: private boolean isMatchFor(Criteria criteria) {
Line 247: ➤
Line 248: if (anyRequiredCriteriaNotMet(criteria)) return false;
Line 249: return anyMatches(criteria);
Line 250: }
Line 251: Move isMatchFor to Matcher. Your IDE should let you know that the two methods
Line 252: called by isMatchFor—anyRequiredCriteriaNotMet and anyMatches—must come along
Line 253: for the ride. Move them too.
Line 254: Here is isMatchFor in its new home, along with the related methods:
Line 255: utj3-refactor/17/src/main/java/iloveyouboss/Matcher.java
Line 256: public class Matcher {
Line 257: // ...
Line 258: public boolean isMatchFor(Criteria criteria) {
Line 259: ➤
Line 260: if (anyRequiredCriteriaNotMet(criteria))
Line 261: return false;
Line 262: return anyMatches(criteria);
Line 263: }
Line 264: private boolean anyMatches(Criteria criteria) {
Line 265: ➤
Line 266: return criteria.stream()
Line 267: .anyMatch(criterion ->
Line 268: criterion.isMatch(profileAnswerMatching(criterion)));
Line 269: }
Line 270: private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
Line 271: ➤
Line 272: return criteria.stream()
Line 273: .filter(criterion ->
Line 274: !criterion.isMatch(profileAnswerMatching(criterion)))
Line 275: .anyMatch(criterion -> criterion.weight() == REQUIRED);
Line 276: }
Line 277: Answer profileAnswerMatching(Criterion criterion) {
Line 278: return answers.get(criterion.questionText());
Line 279: }
Line 280: // ...
Line 281: }
Line 282: report erratum  •  discuss
Line 283: Extracting a New Class • 175
Line 284: 
Line 285: --- 페이지 192 ---
Line 286: The matches method in Profile should be down to two statements:
Line 287: utj3-refactor/17/src/main/java/iloveyouboss/Profile.java
Line 288: public boolean matches(Criteria criteria) {
Line 289: score = new Matcher(criteria, answers).score();
Line 290: return new Matcher(criteria, answers).isMatchFor(criteria);
Line 291: }
Line 292: Tests still pass? Good. Extract the common initialization of Matcher in matches
Line 293: to a local variable:
Line 294: utj3-refactor/18/src/main/java/iloveyouboss/Profile.java
Line 295: public boolean matches(Criteria criteria) {
Line 296: var matcher = new Matcher(criteria, answers);
Line 297: score = matcher.score();
Line 298: return matcher.isMatchFor(criteria);
Line 299: }
Line 300: Moving all the matching logic into Matcher trims the Profile class nicely:
Line 301: utj3-refactor/18/src/main/java/iloveyouboss/Profile.java
Line 302: import java.util.HashMap;
Line 303: import java.util.Map;
Line 304: public class Profile {
Line 305: private final Map<String,Answer> answers = new HashMap<>();
Line 306: private final String name;
Line 307: private int score;
Line 308: public Profile(String name) {
Line 309: this.name = name;
Line 310: }
Line 311: public void add(Answer... newAnswers) {
Line 312: for (var answer: newAnswers)
Line 313: answers.put(answer.questionText(), answer);
Line 314: }
Line 315: public boolean matches(Criteria criteria) {
Line 316: var matcher = new Matcher(criteria, answers);
Line 317: score = matcher.score();
Line 318: return matcher.isMatchFor(criteria);
Line 319: }
Line 320: public int score() {
Line 321: return score;
Line 322: }
Line 323: @Override
Line 324: public String toString() {
Line 325: return name;
Line 326: }
Line 327: }
Line 328: Chapter 9. Refactoring Your Code’s Structure • 176
Line 329: report erratum  •  discuss
Line 330: 
Line 331: --- 페이지 193 ---
Line 332: The Profile class now appears to adhere to the SRP. Its methods are all small
Line 333: and straightforward—you can gather a sense of everything that’s going on in
Line 334: each of them at a glance.
Line 335: Profile is also fairly cohesive: changes to matching or scoring logic will be made
Line 336: in Matcher. Changes to the Profile class itself (for example, it needs to store
Line 337: additional attributes) will not be triggered by changes to matching/scoring
Line 338: logic and will unlikely require changes to Matcher.
Line 339: Cleaning Up After a Move
Line 340: Shift your focus back to Matcher, into which you moved a bunch of methods.
Line 341: Any time you move a method, you’ll want to determine if opportunities exist
Line 342: for improving the code in its new home.
Line 343: The moved anyRequiredCriteriaNotMet and anyMatches methods both require access
Line 344: to the criteria instance. Alter the constructor in Matcher to store criteria as a new
Line 345: field. Once criteria is available as a field, there’s no reason to pass criteria around
Line 346: to the calculateScore, anyRequiredCriteriaNotMet, and anyMatches methods.
Line 347: The removal of the criteria argument from the matches method requires you to
Line 348: change the calling code in Profile. After you make that change, note that without
Line 349: the criteria argument, return matcher.isMatchFor() reads poorly. Rename the isMatchFor
Line 350: method back to matches:
Line 351: utj3-refactor/19/src/main/java/iloveyouboss/Profile.java
Line 352: public boolean matches(Criteria criteria) {
Line 353: var matcher = new Matcher(criteria, answers);
Line 354: score = matcher.score();
Line 355: return matcher.matches();
Line 356: ➤
Line 357: }
Line 358: Here’s the cleaned-up Matcher class:
Line 359: utj3-refactor/19/src/main/java/iloveyouboss/Matcher.java
Line 360: public class Matcher {
Line 361: private final Criteria criteria;
Line 362: ➤
Line 363: private final Map<String, Answer> answers;
Line 364: private int score;
Line 365: public Matcher(Criteria criteria, Map<String, Answer> answers) {
Line 366: this.criteria = criteria;
Line 367: this.answers = answers;
Line 368: ➤
Line 369: calculateScore();
Line 370: ➤
Line 371: }
Line 372: report erratum  •  discuss
Line 373: Extracting a New Class • 177
Line 374: 
Line 375: --- 페이지 194 ---
Line 376: private void calculateScore() {
Line 377: ➤
Line 378: score = criteria.stream()
Line 379: .filter(criterion ->
Line 380: criterion.isMatch(profileAnswerMatching(criterion)))
Line 381: .mapToInt(criterion -> criterion.weight().value())
Line 382: .sum();
Line 383: }
Line 384: public boolean matches() {
Line 385: if (anyRequiredCriteriaNotMet()) return false;
Line 386: ➤
Line 387: return anyMatches();
Line 388: ➤
Line 389: }
Line 390: private boolean anyMatches() {
Line 391: ➤
Line 392: return criteria.stream()
Line 393: .anyMatch(criterion ->
Line 394: criterion.isMatch(profileAnswerMatching(criterion)));
Line 395: }
Line 396: private boolean anyRequiredCriteriaNotMet() {
Line 397: ➤
Line 398: return criteria.stream()
Line 399: .filter(criterion ->
Line 400: !criterion.isMatch(profileAnswerMatching(criterion)))
Line 401: .anyMatch(criterion -> criterion.weight() == REQUIRED);
Line 402: }
Line 403: private Answer profileAnswerMatching(Criterion criterion) {
Line 404: return answers.get(criterion.questionText());
Line 405: }
Line 406: public int score() {
Line 407: return score;
Line 408: }
Line 409: }
Line 410: A couple more tasks and then you can consider the class sufficiently cleaned
Line 411: up…for now. You can improve the matches method in Matcher, and you can
Line 412: tighten up the scoring logic.
Line 413: First, the matches method in Matcher requires three lines to express what could
Line 414: be phrased as a single complex conditional:
Line 415: utj3-refactor/19/src/main/java/iloveyouboss/Matcher.java
Line 416: public boolean matches() {
Line 417: if (anyRequiredCriteriaNotMet()) return false;
Line 418: ➤
Line 419: return anyMatches();
Line 420: ➤
Line 421: }
Line 422: As short as this method is, it remains stepwise rather than declarative. It
Line 423: requires readers to think about how to piece together three elements.
Line 424: Chapter 9. Refactoring Your Code’s Structure • 178
Line 425: report erratum  •  discuss
Line 426: 
Line 427: --- 페이지 195 ---
Line 428: Combine these separate conditionals into a single expression. Invert the result
Line 429: of anyRequiredCriteriaNotMet and combine it with the result of anyMatches using the
Line 430: and (&&) operator:
Line 431: utj3-refactor/20/src/main/java/iloveyouboss/Matcher.java
Line 432: public boolean matches() {
Line 433: return !anyRequiredCriteriaNotMet() && anyMatches();
Line 434: }
Line 435: But double-negatives read poorly. (Boolean logic, in general, is tough for many
Line 436: of us; you want to avoid making things worse.) Eliminate the double-negative
Line 437: by doing the following:
Line 438: 1.
Line 439: Flip the logic in anyRequiredCriteriaNotMet to return true if all required criteria
Line 440: are met.
Line 441: 2.
Line 442: Invert the name of anyRequiredCriteriaNotMet to allRequiredCriteriaMet.
Line 443: 3.
Line 444: Remove the not (!) operator.
Line 445: utj3-refactor/21/src/main/java/iloveyouboss/Matcher.java
Line 446: public boolean matches() {
Line 447: return allRequiredCriteriaMet() && anyMatches();
Line 448: ➤
Line 449: }
Line 450: private boolean allRequiredCriteriaMet() {
Line 451: return criteria.stream()
Line 452: .filter(criterion -> criterion.weight() == REQUIRED)
Line 453: ➤
Line 454: .allMatch(criterion ->
Line 455: ➤
Line 456: criterion.isMatch(profileAnswerMatching(criterion)));
Line 457: ➤
Line 458: }
Line 459: That should make a lot more immediate sense to virtually all readers of the
Line 460: code. You might also change the order of the expression to first ask if there
Line 461: are any matches and then ensure that all required criteria are met—it logically
Line 462: flows a little better.
Line 463: For your second final bit of cleanup, the scoring logic is unnecessarily split
Line 464: across the class. Move the calculateScore logic into the score accessor and then
Line 465: remove calculateScore and the now-unused score field. Your change also carries the
Line 466: benefit of not incurring the score calculation cost if it is not used by the client.
Line 467: utj3-refactor/21/src/main/java/iloveyouboss/Matcher.java
Line 468: public int score() {
Line 469: return criteria.stream()
Line 470: .filter(criterion ->
Line 471: criterion.isMatch(profileAnswerMatching(criterion)))
Line 472: .mapToInt(criterion -> criterion.weight().value())
Line 473: .sum();
Line 474: }
Line 475: report erratum  •  discuss
Line 476: Extracting a New Class • 179
Line 477: 
Line 478: --- 페이지 196 ---
Line 479: When you first learned about object-oriented design, you might have picked
Line 480: up a recommendation to design your classes like “the real world.” It’s an okay
Line 481: starting point, particularly for folks new to OO design, but don’t take it too
Line 482: far. Dogmatically “real-world” designs may seem appealing, but they create
Line 483: systems that are more difficult to maintain.
Line 484: The Profile class could be construed as a “real-world” entity. A simplistic real-
Line 485: world implementation would result in the Profile class containing all the logic
Line 486: related to matching on criteria. The version of Profile that you saw at the start
Line 487: of the refactoring exercises is such a real-world implementation. A system
Line 488: full of such larger, overly responsible classes will be hard to understand and
Line 489: change. It will provide virtually no opportunities for re-use and contain con-
Line 490: siderable duplication,
Line 491: Create classes that map to concepts, not concrete notions. The Matcher concept
Line 492: allows you to isolate the code related to matching, which keeps its code sim-
Line 493: pler. The Profile code from which it came gets simpler as well.
Line 494: Every code change you make alters the design of a system. Some of those
Line 495: changes can have negative impacts on behavior elsewhere in the system. So
Line 496: far, in this chapter, you’ve focused on such macro design considerations.
Line 497: As you start to correct design flaws, whether micro or macro, you’ll more readily
Line 498: spot additional problems. For example, sometimes extracting a small amount
Line 499: of code to a new method will highlight a glaringly obvious deficiency—one
Line 500: that was not so obvious when surrounded by a lot of other code.
Line 501: The methods in Profile are now all very small, and one of them indeed exposes
Line 502: a design flaw. Let’s return to the micro design space and discuss the concept
Line 503: of command-query separation.
Line 504: Command-Query Separation
Line 505: The only remaining oddity in Profile is how it handles scoring logic. Examine
Line 506: its matches method:
Line 507: utj3-refactor/21/src/main/java/iloveyouboss/Profile.java
Line 508: public boolean matches(Criteria criteria) {
Line 509: var matcher = new Matcher(criteria, answers);
Line 510: score = matcher.score();
Line 511: return matcher.matches();
Line 512: }
Line 513: As a side effect, Profile stores a score. But a profile doesn’t have a single fixed
Line 514: score. It only references a calculated score that’s associated with an attempt
Line 515: to match on criteria.
Line 516: Chapter 9. Refactoring Your Code’s Structure • 180
Line 517: report erratum  •  discuss
Line 518: 
Line 519: --- 페이지 197 ---
Line 520: The score side effect causes another problem, which is that a client can’t sep-
Line 521: arate one interest from the other. If a client wants (only) the score for a set
Line 522: of criteria, it must first call the matches() method. This sort of temporal coupling
Line 523: is not going to be immediately obvious to a developer and demands clear
Line 524: documentation. The client would ignore the boolean value returned by matches
Line 525: (awkward!) and then call the score accessor. Conversely, for a client interested
Line 526: in determining whether a set of criteria matches, the call to matches ends up
Line 527: altering the Profile’s score attribute.
Line 528: A method that both returns a value and generates a side effect (changes the
Line 529: state of the class or some other entity in the system) violates the principle
Line 530: known as command-query separation (CQS): A method should either be a
Line 531: command, creating a side effect, or a query that returns a value. It should
Line 532: not be both.
Line 533: Lack of CQS can create potential pain for client code. If a query method alters
Line 534: the state of an object, it might not work to call that method again. You might
Line 535: not get the same answer a second time, and it might cause trouble to trigger
Line 536: the side effect a second time.
Line 537: Lack of CQS also violates expectations for developers using the query method.
Line 538: Without careful reading of the code and its tests, it’s possible for a developer
Line 539: to completely overlook the side effect and thus create a problem.
Line 540: Fixing the CQS Problem in Profile
Line 541: A client of Profile should be free to call a method without having to know they
Line 542: must first call another. Make clients happy by moving all the score-related
Line 543: logic into the score accessor. It’s not much work, particularly since you’d moved
Line 544: the bulk of the logic into Matcher.
Line 545: utj3-refactor/22/src/main/java/iloveyouboss/Profile.java
Line 546: public boolean matches(Criteria criteria) {
Line 547: return new Matcher(criteria, answers).matches();
Line 548: }
Line 549: public int score(Criteria criteria) {
Line 550: ➤
Line 551: return new Matcher(criteria, answers).score();
Line 552: ➤
Line 553: }
Line 554: Most significantly, the score method is no longer a raw accessor. It now takes
Line 555: on a Criteria instance as an argument and then delegates to a new Matcher that
Line 556: calculates and retrieves the score.
Line 557: Don’t forget to delete the score field from Profile; it is no longer needed.
Line 558: report erratum  •  discuss
Line 559: Command-Query Separation • 181
Line 560: 
Line 561: --- 페이지 198 ---
Line 562: As a result of the change to Profile, three tests in AProfile no longer compile.
Line 563: Calls to the score method on a Profile instance now require a criteria object as
Line 564: an argument. Here’s an example of one fixed test showing the changed
Line 565: assertion statement:
Line 566: utj3-refactor/22/src/test/java/iloveyouboss/AProfile.java
Line 567: @Test
Line 568: void isZeroWhenThereAreNoMatches() {
Line 569: profile.add(bonusNo);
Line 570: criteria = new Criteria(
Line 571: new Criterion(bonusYes, IMPORTANT));
Line 572: var score = profile.score(criteria);
Line 573: ➤
Line 574: assertEquals(0, score);
Line 575: ➤
Line 576: }
Line 577: The Costs of Maintaining Unit Tests
Line 578: Refactoring—changing the implementation of a solution without changing
Line 579: its behavior—should not normally break tests. Here, however, you did make
Line 580: a behavioral change due to a deficiency in the Profile interface. Your updated
Line 581: design now exposes the score method’s behavior in a different manner than
Line 582: before, hence the broken tests. You might consider that your refactoring
Line 583: “pushed out a change to the interface.”
Line 584: Sure, you must spend time to fix the tests. In this case, having tests in the
Line 585: first place enabled you to recognize and fix a faulty design.
Line 586: You’ve learned throughout this book the potential benefits of unit tests:
Line 587: • Releasing fewer defects
Line 588: • Changing your code at will with high confidence
Line 589: • Knowing exactly and rapidly what behaviors the system embodies
Line 590: This book can help you attain those benefits and increase your ROI.
Line 591: The return on investment from well-designed tests outweighs
Line 592: their cost.
Line 593: Moving forward, when your tests break as you refactor, think about it as a
Line 594: design smell. The more tests that break simultaneously, the bigger the chance
Line 595: you missed an opportunity to improve the design, whether of the tests or
Line 596: production code.
Line 597: Chapter 9. Refactoring Your Code’s Structure • 182
Line 598: report erratum  •  discuss
Line 599: 
Line 600: --- 페이지 199 ---
Line 601: Refocusing Tests
Line 602: After moving behavior from Profile to Matcher, the tests in AProfile now have nothing
Line 603: to do with Profile. You’ll want to move the tests to a new class—AMatcher—and
Line 604: then adapt them to interact with Matcher, not Profile.
Line 605: Currently, Matcher’s constructor requires a Map<String,Answer> (where the String
Line 606: key represents a question’s text) as its second parameter. The tests in AProfile
Line 607: involve adding a list of Answer objects to a profile, however:
Line 608: utj3-refactor/21/src/test/java/iloveyouboss/AProfile.java
Line 609: @Test
Line 610: void whenNoneOfMultipleCriteriaMatch() {
Line 611: profile.add(bonusNo, freeLunchNo);
Line 612: ➤
Line 613: criteria = new Criteria(
Line 614: new Criterion(bonusYes, IMPORTANT),
Line 615: new Criterion(freeLunchYes, IMPORTANT));
Line 616: var matches = profile.matches(criteria);
Line 617: assertFalse(matches);
Line 618: }
Line 619: It’d be nice to only have to minimally change the tests. Right now, however,
Line 620: they’d need to convert each list of answers into a Map<String,Answer> before
Line 621: constructing the Matcher.
Line 622: Instead, think about the most concise way to express your tests. Here’s what
Line 623: you’d like Matcher’s tests to look like—very similar to the tests in AProfile:
Line 624: utj3-refactor/22/src/test/java/iloveyouboss/AMatcher.java
Line 625: @Test
Line 626: void whenNoneOfMultipleCriteriaMatch() {
Line 627: criteria = new Criteria(
Line 628: new Criterion(bonusYes, IMPORTANT),
Line 629: new Criterion(freeLunchYes, IMPORTANT));
Line 630: matcher = new Matcher(criteria, bonusNo, freeLunchNo);
Line 631: ➤
Line 632: var matches = matcher.matches();
Line 633: ➤
Line 634: assertFalse(matches);
Line 635: }
Line 636: Note that the test necessarily creates a matcher object after the criteria. Also,
Line 637: the call to matches no longer requires any arguments.
Line 638: The test assumes it can create a Matcher object using the same list of answers
Line 639: added to a profile by tests in AProfile. Make that happen by adding a constructor
Line 640: and helper method to Matcher, letting it do the dirty work:
Line 641: report erratum  •  discuss
Line 642: The Costs of Maintaining Unit Tests • 183
Line 643: 
Line 644: --- 페이지 200 ---
Line 645: utj3-refactor/22/src/main/java/iloveyouboss/Matcher.java
Line 646: public Matcher(Criteria criteria, Answer... matcherAnswers) {
Line 647: this.criteria = criteria;
Line 648: this.answers = toMap(matcherAnswers);
Line 649: }
Line 650: private Map<String, Answer> toMap(Answer[] answers) {
Line 651: return Stream.of(answers).collect(
Line 652: Collectors.toMap(Answer::questionText, answer -> answer));
Line 653: }
Line 654: Getting all of the tests to that adapted shape is maybe 15-20 minutes of work.
Line 655: You’ll need to:
Line 656: • Declare a Matcher field named matcher.
Line 657: • Eliminate the profile field.
Line 658: • For each test:
Line 659: – Assign a new Matcher instance to matcher. Create it using the test’s cri-
Line 660: teria plus the list of answers previously provided to the profile’s add
Line 661: method. Ensure this assignment statement appears after the line that
Line 662: creates the Criteria.
Line 663: – Remove the statement that adds answers to the profile (for example,
Line 664: profile.add(freeLunch, bonusYes);).
Line 665: If you get stuck—or just want to give up—go ahead and copy in the code from
Line 666: the distribution for this book.
Line 667: You can now revisit and clean up the tests in AProfile.
Line 668: Revisiting the Profile Class: Delegation Tests
Line 669: Someone created nice, exhaustive tests for the Profile class. (Hey…that was
Line 670: me. You’re welcome.) But you copied them over to AMatcher, without really
Line 671: changing the essence of the logic they verify. You also removed all that
Line 672: interesting logic from Profile.
Line 673: The Profile class still contains three methods with logic. Out of these, the
Line 674: matches and score methods do nothing but delegate to Matcher. Still, you should
Line 675: feel compelled to provide tests for these methods. They’ll probably never break,
Line 676: but would at least help describe what’s going on.
Line 677: Were you to test the score and matches methods, you’d have at least a couple
Line 678: of options. You could introduce mock objects (see Chapter 3, Using Test
Line 679: Doubles, on page 53) to verify that the work was delegated to the Matcher in
Line 680: each case. You could also choose a simple, representative case involving the
Line 681: scoring and matching. Both have their merits and demerits.
Line 682: Chapter 9. Refactoring Your Code’s Structure • 184
Line 683: report erratum  •  discuss
Line 684: 
Line 685: --- 페이지 201 ---
Line 686: Would, should, could. Maybe you’re sensing I’m not going to have you write
Line 687: tests for these methods. You’ll instead push out the work of interacting with
Line 688: the Matcher directly to the client of Profile—a service class, perhaps—as a sim-
Line 689: plifying design choice. The service class can handle the coordination between
Line 690: the profile, matcher, and criteria. That code might look like this:
Line 691: utj3-refactor/23/src/main/java/iloveyouboss/MatcherService.java
Line 692: public class MatcherService {
Line 693: public boolean matches(int profileId, int criteriaId) {
Line 694: var profile = profileData.retrieve(profileId);
Line 695: var criteria = criteriaData.retrieve(criteriaId);
Line 696: return new Matcher(criteria, profile.answers()).matches();
Line 697: }
Line 698: public int score(int profileId, int criteriaId) {
Line 699: var profile = profileData.retrieve(profileId);
Line 700: var criteria = criteriaData.retrieve(criteriaId);
Line 701: return new Matcher(criteria, profile.answers()).score();
Line 702: }
Line 703: // ...
Line 704: }
Line 705: You’ll want to (and have to) make a few more changes, but everything is now
Line 706: a little simpler in the other three classes impacted.
Line 707: After pushing out the matches and score methods, the only logic remaining in
Line 708: the Profile class appears in its add(Answer) method. Since no code in Profile cares
Line 709: about the answers, you can simplify the class to store a list of Answer objects
Line 710: rather than create a Map. Here’s the cleaned-up version of Profile:
Line 711: utj3-refactor/23/src/main/java/iloveyouboss/Profile.java
Line 712: import java.util.ArrayList;
Line 713: import java.util.List;
Line 714: public class Profile {
Line 715: private final List<Answer> answers = new ArrayList<>();
Line 716: private final String name;
Line 717: public Profile(String name) {
Line 718: this.name = name;
Line 719: }
Line 720: public void add(Answer... newAnswers) {
Line 721: for (var answer: newAnswers)
Line 722: answers.add(answer);
Line 723: }
Line 724: public List<Answer> answers() {
Line 725: return answers;
Line 726: }
Line 727: report erratum  •  discuss
Line 728: The Costs of Maintaining Unit Tests • 185
Line 729: 
Line 730: --- 페이지 202 ---
Line 731: public String name() {
Line 732: return name;
Line 733: }
Line 734: }
Line 735: And here’s a simple test to add:
Line 736: utj3-refactor/23/src/test/java/iloveyouboss/AProfile.java
Line 737: import org.junit.jupiter.api.Test;
Line 738: import java.util.List;
Line 739: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 740: class AProfile {
Line 741: Question question = new Question("?", new String[] {"Y","N"}, 1);
Line 742: Profile profile = new Profile("x");
Line 743: @Test
Line 744: void supportsAddingIndividualAnswers() {
Line 745: var answer = new Answer(question, "Y");
Line 746: profile.add(answer);
Line 747: assertEquals(List.of(answer), profile.answers());
Line 748: }
Line 749: }
Line 750: Your changes impact the constructors in Matcher again. While updating the
Line 751: class, you can also change Matcher to be a Java record instead of a class. Here’s
Line 752: the final code (minus imports):
Line 753: utj3-refactor/23/src/main/java/iloveyouboss/Matcher.java
Line 754: public record Matcher(Criteria criteria, Map<String, Answer> answers) {
Line 755: public Matcher(Criteria criteria, List<Answer> matcherAnswers) {
Line 756: this(criteria, asMap(matcherAnswers));
Line 757: }
Line 758: public Matcher(Criteria criteria, Answer... matcherAnswers) {
Line 759: this(criteria, asList(matcherAnswers));
Line 760: }
Line 761: private static Map<String, Answer> asMap(List<Answer> answers) {
Line 762: return answers.stream().collect(
Line 763: Collectors.toMap(Answer::questionText, answer -> answer));
Line 764: }
Line 765: public boolean matches() {
Line 766: return allRequiredCriteriaMet() && anyMatches();
Line 767: }
Line 768: private boolean allRequiredCriteriaMet() {
Line 769: return criteria.stream()
Line 770: .filter(criterion -> criterion.weight() == REQUIRED)
Line 771: .allMatch(criterion ->
Line 772: criterion.isMatch(profileAnswerMatching(criterion)));
Line 773: }
Line 774: Chapter 9. Refactoring Your Code’s Structure • 186
Line 775: report erratum  •  discuss
Line 776: 
Line 777: --- 페이지 203 ---
Line 778: private boolean anyMatches() {
Line 779: return criteria.stream()
Line 780: .anyMatch(criterion ->
Line 781: criterion.isMatch(profileAnswerMatching(criterion)));
Line 782: }
Line 783: private Answer profileAnswerMatching(Criterion criterion) {
Line 784: return answers.get(criterion.questionText());
Line 785: }
Line 786: public int score() {
Line 787: return criteria.stream()
Line 788: .filter(criterion ->
Line 789: criterion.isMatch(profileAnswerMatching(criterion)))
Line 790: .mapToInt(criterion -> criterion.weight().value())
Line 791: .sum();
Line 792: }
Line 793: }
Line 794: Left to you, dear reader: combining both matching logic and scoring logic in
Line 795: Matcher decreases cohesion. Your mission: split off the scoring logic into a new
Line 796: class, Scorer. It should take at most 15 minutes. Don’t forget to split off the
Line 797: tests!
Line 798: Summary
Line 799: In this chapter, you improved the design of iloveyouboss, leaning mostly on
Line 800: a couple of simple design concepts for guidance: the SRP and command-query
Line 801: separation. You owe it to yourself to know as much as possible about these
Line 802: and other concepts in design. (Take a look at Clean Code [Mar08], for example,
Line 803: but keep reading.) And don’t forget what you learned in Chapter 8, Refactoring
Line 804: to Cleaner Code, on page 147: small, continual code edits make a big difference.
Line 805: Armed with a stockpile of design smarts, your unit tests will allow you to
Line 806: reshape your system so that it more easily supports the inevitable changes
Line 807: coming.
Line 808: Your system’s design quality also inversely correlates to your pain and frus-
Line 809: tration level. The worse your design, the longer it will take to understand the
Line 810: code and make changes. Keeping the design incrementally clean will keep
Line 811: costs to a small fraction of what they’ll become otherwise.
Line 812: Be flexible. Be willing to create new, smaller classes and methods. Automated
Line 813: refactoring tools make doing so easy. Even without such tools, it takes only
Line 814: minutes. It’s worth the modest effort. Design flexibility starts with smaller,
Line 815: more composed building blocks.
Line 816: report erratum  •  discuss
Line 817: Summary • 187
Line 818: 
Line 819: --- 페이지 204 ---
Line 820: Now that you’ve learned to continually address your system’s micro and
Line 821: macro-level design because your unit tests allow you to do so with high confi-
Line 822: dence, it’s time to take a look at those tests themselves. Next up, you’ll see
Line 823: how streamlining your tests lets them pay off even more as concise, clear,
Line 824: and correct documentation on all the unit capabilities you’ve built into your
Line 825: system.
Line 826: Chapter 9. Refactoring Your Code’s Structure • 188
Line 827: report erratum  •  discuss