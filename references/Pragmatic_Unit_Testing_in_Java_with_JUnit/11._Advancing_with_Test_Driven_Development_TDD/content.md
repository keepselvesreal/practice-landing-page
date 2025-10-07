Line 1: 
Line 2: --- 페이지 225 ---
Line 3: CHAPTER 11
Line 4: Advancing with Test-Driven
Line 5: Development (TDD)
Line 6: You’re now armed with what you’ll need to know about straight-up unit
Line 7: testing in Java. In this part, you’ll learn about three significant topics:
Line 8: • Using TDD to flip the concept of unit testing from test-after to test-driven
Line 9: • Considerations for unit testing within a project team
Line 10: • Using AI tooling to drive development, assisted by unit tests
Line 11: You’ll start with a meaty example of how to practice TDD.
Line 12: It’s hard to write unit tests for some code. Such “difficult” code grows partly
Line 13: from a lack of interest in unit testing. In contrast, the more you consider how
Line 14: to unit test the code you write, the more you’ll end up with easier-to-test code.
Line 15: (“Well, duh!” responds our reluctant unit tester Joe.)
Line 16: With TDD, you think first about the outcome you expect for the code you’re
Line 17: going to write. Rather than slap out some code and then figure out how to
Line 18: test it (or even what it should do), you first capture the expected outcome in
Line 19: a test. You then code the behavior needed to meet that outcome. This reversed
Line 20: approach might seem bizarre or even impossible, but it’s the core element
Line 21: in TDD.
Line 22: With TDD, you wield unit tests as a tool to help you shape and control your
Line 23: systems. Rather than a haphazard practice where you sometimes write unit
Line 24: tests after you write code, and sometimes you don’t, describing outcomes and
Line 25: verifying code through unit tests becomes your central focus.
Line 26: You will probably find the practice of TDD dramatically different than
Line 27: anything you’ve experienced in software development. The way you build
Line 28: report erratum  •  discuss
Line 29: 
Line 30: --- 페이지 226 ---
Line 31: code and the shape that your code takes on will change considerably. You
Line 32: may well find TDD highly gratifying and ultimately liberating, strangely
Line 33: enough.
Line 34: In this chapter, you’ll test drive a small solution using TDD, unit by unit, and
Line 35: talk about the nuanced changes to the approach that TDD brings.
Line 36: The Primary Benefit of TDD
Line 37: With plain ol’ after-the-fact unit testing, the obvious, most significant benefit
Line 38: you gain is increased confidence that the code you wrote works as expected—at
Line 39: least to the coverage that your unit tests provide. With TDD, you gain that
Line 40: same benefit and many more.
Line 41: Systems degrade primarily because we don’t strive often or hard enough to
Line 42: keep the code clean. We’re good at quickly adding code into our systems, but
Line 43: on the first pass, it’s more often not-so-great code than good code. We don’t
Line 44: spend a lot of effort cleaning up that initially costly code for many reasons.
Line 45: Joe chimes in with his list:
Line 46: • “We need to move on to the next task. We don’t have time to gild the code.”
Line 47: • “I think the code reads just fine the way it is. I wrote it, I understand it.
Line 48: I can add some comments to the code if you think it’s not clear.”
Line 49: • “We can refactor the code when we need to make further changes in that
Line 50: area.”
Line 51: • “It works. Why mess with a good thing? If it ain’t broke, don’t fix it. It’s
Line 52: too easy to break something else when refactoring code.”
Line 53: Thanks, Joe, for that list of common rationalizations for letting code degrade.
Line 54: With TDD, your fear about changing code can evaporate. Indeed, refactoring is
Line 55: a risky activity, and we’ve all made plenty of mistakes when making seemingly
Line 56: innocuous changes. But if you’re following TDD well, you’re writing unit tests
Line 57: for virtually all cases you implement in the system. Those unit tests give you
Line 58: the freedom you need to continually improve the code.
Line 59: Starting Simple
Line 60: TDD is a three-part cycle:
Line 61: 1.
Line 62: Write a test that fails.
Line 63: 2.
Line 64: Get the test to pass.
Line 65: 3.
Line 66: Clean up any code added or changed in the prior two steps.
Line 67: Chapter 11. Advancing with Test-Driven Development (TDD) • 212
Line 68: report erratum  •  discuss
Line 69: 
Line 70: --- 페이지 227 ---
Line 71: The first step of the cycle tells you to write a test describing the behavior you
Line 72: want to build into the system. Seek to write a test representing the smallest
Line 73: possible—but useful—increment to the code that already exists.
Line 74: For your exercise, you’ll test-drive a small portfolio manager. Your require-
Line 75: ments will be revealed to you incrementally as well, in batches, by your
Line 76: product owner Madhu. Imagine that each requirements batch was not previ-
Line 77: ously considered. Your job is to deliver a solution for each incremental need
Line 78: to production.
Line 79: You want to ensure that you can continue to accommodate new batches of
Line 80: requirements indefinitely. To meet that ongoing demand, your focus after
Line 81: getting each new test to pass—as part of the clean-up step in TDD—will be
Line 82: to distill the solution to employ the simplest possible design. You will seek
Line 83: maximally concise, clear, and cohesive code.
Line 84: Each new TDD cycle starts with choosing the next behavior to implement.
Line 85: For the smoothest progression through building a solution, you’ll seek a
Line 86: behavior that produces the smallest possible increment from the current
Line 87: solution.
Line 88: In other words, you’re trying to ensure each TDD cycle represents a tiny little
Line 89: step that requires only a tiny bit of new code or changed code.
Line 90: You’ll step through four increments of code. You’ll be able to deliver each
Line 91: increment to production.
Line 92: Increment 1: Deferring Complexity
Line 93: For your first requirements batch, you’re tasked with delivering very simple
Line 94: rudiments of a portfolio.
Line 95: You’ll be able to make purchases for the portfolio. For now, a purchase involves
Line 96: a stock symbol, such as SONO (Sonos) or AAPL (Apple), and a number of
Line 97: shares purchased for that symbol.
Line 98: But your solution won’t need to track the actual symbols or shares of each.
Line 99: Madhu tells you that all it needs to answer are the following two things:
Line 100: • Whether or not it is empty. A portfolio is empty if no purchases have been
Line 101: made and not empty otherwise.
Line 102: • How many unique symbols have been purchased—the portfolio’s size. If
Line 103: you purchase AAPL once, you have one unique symbol. If you purchase
Line 104: AAPL a second time, you still have only the one unique symbol. If you
Line 105: purchase AAPL and then purchase SONO, you have two unique symbols.
Line 106: report erratum  •  discuss
Line 107: Increment 1: Deferring Complexity • 213
Line 108: 
Line 109: --- 페이지 228 ---
Line 110: The ZOM progression (see ZOM: Zero and One Done, Now Testing Many, on
Line 111: page 22) is a great place to start when practicing TDD. You’ll employ it fre-
Line 112: quently as you try to derive the next-smallest increment.
Line 113: You want to start with the absolute simplest requirement. Between the two
Line 114: concerns—emptiness and size—emptiness seems simplest. Your first test is
Line 115: a zero-based verification: the portfolio is empty when created (in other words,
Line 116: no purchases have been made).
Line 117: utj3-tdd/01/src/test/java/app/APortfolio.java
Line 118: import org.junit.jupiter.api.Test;
Line 119: import static org.junit.jupiter.api.Assertions.assertTrue;
Line 120: public class APortfolio {
Line 121: @Test
Line 122: void isEmptyWhenCreated() {
Line 123: var portfolio = new Portfolio();
Line 124: assertTrue(portfolio.isEmpty());
Line 125: }
Line 126: }
Line 127: In order to compile and run the test, you’ll need to supply an implementation
Line 128: for the Portfolio class. You also want a test that fails (more on that as you go).
Line 129: Returning false from isEmpty will cause the call to assertTrue to fail:
Line 130: utj3-tdd/01/src/main/java/app/Portfolio.java
Line 131: public class Portfolio {
Line 132: public boolean isEmpty() {
Line 133: return false;
Line 134: }
Line 135: }
Line 136: Now, you can run JUnit. You expect a failure and receive it:
Line 137: Expected :true
Line 138: Actual
Line 139: :false
Line 140: All is well.
Line 141: Avoid costly, poor assumptions with TDD. Ensure each new test
Line 142: fails before you write the code to make it pass.
Line 143: You seek the simplest code that will get the test to pass in order to avoid
Line 144: adding code until you have a test that demands its existence:
Line 145: Chapter 11. Advancing with Test-Driven Development (TDD) • 214
Line 146: report erratum  •  discuss
Line 147: 
Line 148: --- 페이지 229 ---
Line 149: utj3-tdd/02/src/main/java/app/Portfolio.java
Line 150: public boolean isEmpty() {
Line 151: return true;
Line 152: }
Line 153: As far as the cleanup step in the TDD cycle is concerned, that four-line
Line 154: solution is expressed about as concisely and clearly as it can get. Time to
Line 155: move on.
Line 156: If you’re using a capable source repository such as Git, now is the time to
Line 157: commit your code. Committing each new bit of behavior as you do TDD makes
Line 158: it easy to back up and change direction as needed.
Line 159: You’ve written a test for a Boolean method that demonstrates when it returns
Line 160: true. A second test, demonstrating the conditions that produce a false return, is
Line 161: required. Creating a non-empty portfolio requires test code that makes a
Line 162: purchase:
Line 163: utj3-tdd/03/src/test/java/app/APortfolio.java
Line 164: @Test
Line 165: void isNotEmptyAfterPurchase() {
Line 166: var portfolio = new Portfolio();
Line 167: portfolio.purchase("AAPL", 1);
Line 168: assertFalse(portfolio.isEmpty());
Line 169: }
Line 170: To appease the compiler, provide a purchase method:
Line 171: utj3-tdd/03/src/main/java/app/Portfolio.java
Line 172: public void purchase(String symbol, int shares) {
Line 173: }
Line 174: Run all of your Portfolio tests and ensure that (only) the newest one fails.
Line 175: To get your tests passing, you could consider storing the symbol and shares
Line 176: in some sort of data structure, such as a HashMap. And that’s probably your
Line 177: natural inclination as a developer. But it’s a lot more than you need at this
Line 178: current moment. It speculates a need to be able to return the symbol and
Line 179: shares, a need that does not exist.
Line 180: Your goal is to meet requirements and deliver. Yes, you probably will need to
Line 181: retain the symbol and shares in the portfolio. But TDD tells you to wait until
Line 182: that need exists. For now, your goal is to get the test passing in as straight-
Line 183: forward and non-speculative a manner as possible.
Line 184: report erratum  •  discuss
Line 185: Increment 1: Deferring Complexity • 215
Line 186: 
Line 187: --- 페이지 230 ---
Line 188: If you need to retain a Boolean state, a Boolean field will unsurprisingly do
Line 189: the trick. On a purchase, update the Boolean to reflect that the portfolio is
Line 190: no longer empty.
Line 191: utj3-tdd/04/src/main/java/app/Portfolio.java
Line 192: public class Portfolio {
Line 193: private boolean isEmpty = true;
Line 194: ➤
Line 195: public boolean isEmpty() {
Line 196: return isEmpty;
Line 197: ➤
Line 198: }
Line 199: public void purchase(String symbol, int shares) {
Line 200: isEmpty = false;
Line 201: ➤
Line 202: }
Line 203: }
Line 204: Your tests need love, too. They are no longer concise; both the tests you’ve
Line 205: written so far initialize a Portfolio object—a necessary thing to do, but not an
Line 206: interesting thing to do in the sense that it adds any meaning to either test.
Line 207: You can do the common initialization in a @BeforeEach method.
Line 208: utj3-tdd/05/src/test/java/app/APortfolio.java
Line 209: public class APortfolio {
Line 210: Portfolio portfolio;
Line 211: @BeforeEach
Line 212: ➤
Line 213: void create() {
Line 214: ➤
Line 215: portfolio = new Portfolio();
Line 216: ➤
Line 217: }
Line 218: ➤
Line 219: @Test
Line 220: void isEmptyWhenCreated() {
Line 221: assertTrue(portfolio.isEmpty());
Line 222: }
Line 223: @Test
Line 224: void isNotEmptyAfterPurchase() {
Line 225: portfolio.purchase("AAPL", 1);
Line 226: assertFalse(portfolio.isEmpty());
Line 227: }
Line 228: }
Line 229: For now, you’ve exhausted the Boolean. Two states/two behaviors/two tests.
Line 230: A Boolean won’t support “many.”
Line 231: Go ahead and commit your code at this point. Going forward, you won’t get
Line 232: any more reminders. Every time you get a test to pass and spend a bit of
Line 233: effort cleaning up the result, do a commit. You’ll appreciate being able to
Line 234: revert to the previous increment of code.
Line 235: Chapter 11. Advancing with Test-Driven Development (TDD) • 216
Line 236: report erratum  •  discuss
Line 237: 
Line 238: --- 페이지 231 ---
Line 239: The next of the two features to tackle for this batch is the notion of the port-
Line 240: folio’s size, and…yes, you’re right, a zero-based test.
Line 241: utj3-tdd/06/src/test/java/app/APortfolio.java
Line 242: @Test
Line 243: void hasSize0WhenCreated() {
Line 244: assertEquals(0, portfolio.size());
Line 245: }
Line 246: To get this to compile but not pass the tests, return -1 from size. After observing
Line 247: the failure, hard-code a 0 to make it pass:
Line 248: utj3-tdd/07/src/main/java/app/Portfolio.java
Line 249: public int size() {
Line 250: return 0;
Line 251: }
Line 252: Hard-coding seems silly, but it is in keeping with the test-code-and-refactor
Line 253: rhythm of the TDD cycle. Your goal is to produce the simplest possible
Line 254: implementation for the latest test. More specifically, you want to only solve
Line 255: the current set of problems. By doing so, you avoid overengineering and pre-
Line 256: mature speculation. Both will cost you in the long run.
Line 257: You are learning to design for current need so that you can more easily take
Line 258: on new, never-before-considered requirements that you could never have
Line 259: predicted (or designed for).
Line 260: Next test—make one purchase and have a portfolio with size one:
Line 261: utj3-tdd/08/src/test/java/app/APortfolio.java
Line 262: @Test
Line 263: void hasSize1OnPurchase() {
Line 264: portfolio.purchase("AAPL", 1);
Line 265: assertEquals(1, portfolio.size());
Line 266: }
Line 267: Think for just a moment. Can you solve this problem given the current “data
Line 268: structure” (a Boolean)? Of course you can:
Line 269: utj3-tdd/09/src/main/java/app/Portfolio.java
Line 270: public int size() {
Line 271: return isEmpty ? 0 : 1;
Line 272: }
Line 273: Maybe a Boolean’s two states can support more than you think.
Line 274: It’s possible that you’re thinking at this very moment that TDD might be too
Line 275: pedantic to be useful. Hang in there. You’re starting to use your brain to think
Line 276: differently about how to solve software problems. Specifically, you’re focusing
Line 277: report erratum  •  discuss
Line 278: Increment 1: Deferring Complexity • 217
Line 279: 
Line 280: --- 페이지 232 ---
Line 281: on what it means to find the next-smallest increment, probably something
Line 282: you’ve not done before.
Line 283: One key benefit you might or might not have noticed: each of these increments
Line 284: is something you could get passing in no more than a couple minutes and in
Line 285: seconds-less-than-100 in many cases (unless you’re a terrible typist, and
Line 286: that’s okay too).
Line 287: Ready for some real computing? The next test demands more than a two-state
Line 288: solution can support:
Line 289: utj3-tdd/10/src/test/java/app/APortfolio.java
Line 290: @Test
Line 291: void incrementsSizeWithEachPurchaseDifferentSymbol() {
Line 292: portfolio.purchase("AAPL", 1);
Line 293: portfolio.purchase("SONO", 1);
Line 294: assertEquals(2, portfolio.size());
Line 295: }
Line 296: Your portfolio needs to track more than 0 and 1 values; it must be able to
Line 297: answer 2, and 3, and to infinity…and beyond. The two-state Boolean solution
Line 298: has reached its predictable end and must yield to the (short-to-live) future.
Line 299: Introduce an int field named size, initialized to 0 and incremented on each
Line 300: purchase:
Line 301: utj3-tdd/11/src/main/java/app/Portfolio.java
Line 302: public class Portfolio {
Line 303: private boolean isEmpty = true;
Line 304: private int size = 0;
Line 305: ➤
Line 306: public boolean isEmpty() {
Line 307: return isEmpty;
Line 308: }
Line 309: public void purchase(String symbol, int shares) {
Line 310: isEmpty = false;
Line 311: size++;
Line 312: ➤
Line 313: }
Line 314: public int size() {
Line 315: return size;
Line 316: ➤
Line 317: }
Line 318: }
Line 319: Note that you don’t evict the Boolean-related code just yet. It can watch and
Line 320: continue to support current needs as progress, in the form of slightly more
Line 321: generalized code supporting new behavior, gets built next door.
Line 322: Chapter 11. Advancing with Test-Driven Development (TDD) • 218
Line 323: report erratum  •  discuss
Line 324: 
Line 325: --- 페이지 233 ---
Line 326: Once you demonstrate that the generalization to an int works, you can take
Line 327: advantage of a refactoring step to purge all the old, limited behaviors:
Line 328: utj3-tdd/12/src/main/java/app/Portfolio.java
Line 329: public class Portfolio {
Line 330: private int size = 0;
Line 331: public boolean isEmpty() {
Line 332: return size == 0;
Line 333: }
Line 334: public void purchase(String symbol, int shares) {
Line 335: size++;
Line 336: }
Line 337: public int size() {
Line 338: return size;
Line 339: }
Line 340: }
Line 341: Little pieces of code come and support a new initiative. Little pieces leave to
Line 342: ensure a clean, easy-to-navigate code neighborhood.
Line 343: Maybe you’re thinking, “this seems like a roundabout way to get to three lines
Line 344: of code.” Two things are important to remember, however:
Line 345: • You’ve created a handful of tests along with your solution. These tests
Line 346: will continue to provide protection.
Line 347: • You’re adopting a new mentality where someone could yell, “stop building!”
Line 348: at any time, and you’d be okay with that. With TDD, you constantly have
Line 349: the confidence to support releasing the system.
Line 350: You’ve supported Zero, One, Many cases for the portfolio’s size. Now, it’s time
Line 351: to think about the interesting cases. Hearken back to the description of the
Line 352: requirements for this batch. One of them indicated that if you purchased
Line 353: Apple stock and then purchased more of Apple stock, you still only had one
Line 354: stock symbol and thus a portfolio size of one:
Line 355: utj3-tdd/13/src/test/java/app/APortfolio.java
Line 356: @Test
Line 357: void doesNotIncrementSizeWithPurchaseSameSymbol() {
Line 358: portfolio.purchase("AAPL", 1);
Line 359: portfolio.purchase("AAPL", 1);
Line 360: assertEquals(1, portfolio.size());
Line 361: }
Line 362: “Now is it time for the HashMap?” you might ask.
Line 363: report erratum  •  discuss
Line 364: Increment 1: Deferring Complexity • 219
Line 365: 
Line 366: --- 페이지 234 ---
Line 367: Not quite yet. Maybe half a hash map: A hash map is a collection of unique
Line 368: keys, each that maps to some value. You might remember from second grade
Line 369: that a collection of unique keys is known as a set.
Line 370: Probably the easiest way to count the number of unique values is to throw
Line 371: them into a set and ask for its size.
Line 372: You introduced “real computing” a few moments back in the form of incre-
Line 373: menting an integer. Now, you’ll get to use a “real data structure” in the form
Line 374: of a Java set object.
Line 375: “Pedantic again?” you might ask. Maybe. “Why not just use a HashMap?”
Line 376: Because it’s more complex than what you need right now.
Line 377: utj3-tdd/14/src/main/java/app/Portfolio.java
Line 378: public class Portfolio {
Line 379: private int size = 0;
Line 380: private Set symbols = new HashSet<String>();
Line 381: ➤
Line 382: public boolean isEmpty() {
Line 383: return symbols.isEmpty();
Line 384: ➤
Line 385: }
Line 386: public void purchase(String symbol, int shares) {
Line 387: size++;
Line 388: symbols.add(symbol);
Line 389: ➤
Line 390: }
Line 391: public int size() {
Line 392: return symbols.size();
Line 393: ➤
Line 394: }
Line 395: }
Line 396: After verifying your updated solution, remove references to the size int:
Line 397: utj3-tdd/15/src/main/java/app/Portfolio.java
Line 398: public class Portfolio {
Line 399: private Set symbols = new HashSet<String>();
Line 400: public boolean isEmpty() {
Line 401: return symbols.isEmpty();
Line 402: }
Line 403: public void purchase(String symbol, int shares) {
Line 404: symbols.add(symbol);
Line 405: }
Line 406: public int size() {
Line 407: return symbols.size();
Line 408: }
Line 409: }
Line 410: Chapter 11. Advancing with Test-Driven Development (TDD) • 220
Line 411: report erratum  •  discuss
Line 412: 
Line 413: --- 페이지 235 ---
Line 414: And…ship it! You’ve built support for tracking the size and emptiness of the
Line 415: portfolio. It has no extraneous, speculative moving parts and is as simple a
Line 416: solution as you could ask for. It’s fully tested with six simple unit tests.
Line 417: Increment 2: Generalizing the Implementation
Line 418: Madhu’s second batch of requirements for you is a batch of one: track the
Line 419: number of shares owned for a given symbol. A happy path test case:
Line 420: utj3-tdd/16/src/test/java/app/APortfolio.java
Line 421: @Test
Line 422: void returnsSharesGivenSymbol() {
Line 423: portfolio.purchase("AAPL", 42);
Line 424: assertEquals(42, portfolio.sharesOf("AAPL"));
Line 425: }
Line 426: The tests to any point in time represent the set of assumptions you make.
Line 427: Currently, you are assuming there will only ever be a single purchase. As
Line 428: such, you can track the shares purchased using a single discrete field:
Line 429: utj3-tdd/17/src/main/java/app/Portfolio.java
Line 430: public class Portfolio {
Line 431: private Set symbols = new HashSet<String>();
Line 432: private int shares;
Line 433: ➤
Line 434: // ...
Line 435: public void purchase(String symbol, int shares) {
Line 436: symbols.add(symbol);
Line 437: this.shares = shares;
Line 438: ➤
Line 439: }
Line 440: public int sharesOf(String symbol) {
Line 441: ➤
Line 442: return shares;
Line 443: ➤
Line 444: }
Line 445: ➤
Line 446: }
Line 447: You know that using a single field won’t hold up to multiple purchases that
Line 448: are for differing symbols. That tells you that the next test you write—involve
Line 449: multiple purchases—will most certainly fail, keeping you in the TDD cycle:
Line 450: utj3-tdd/18/src/test/java/app/APortfolio.java
Line 451: @Test
Line 452: void separatesSharesBySymbol() {
Line 453: portfolio.purchase("SONO", 42);
Line 454: portfolio.purchase("AAPL", 1);
Line 455: assertEquals(42, portfolio.sharesOf("SONO"));
Line 456: }
Line 457: report erratum  •  discuss
Line 458: Increment 2: Generalizing the Implementation • 221
Line 459: 
Line 460: --- 페이지 236 ---
Line 461: “It’s time, right?” you ask. Why yes, you can finally introduce the HashMap…if
Line 462: you must. There are other ways of solving the problem, but for now, the
Line 463: HashMap is the most direct.
Line 464: utj3-tdd/19/src/main/java/app/Portfolio.java
Line 465: import java.util.HashMap;
Line 466: import java.util.HashSet;
Line 467: import java.util.Map;
Line 468: import java.util.Set;
Line 469: public class Portfolio {
Line 470: private Map<String, Integer> purchases = new HashMap<>();
Line 471: ➤
Line 472: private Set symbols = new HashSet<String>();
Line 473: private int shares;
Line 474: public boolean isEmpty() {
Line 475: return purchases.isEmpty();
Line 476: ➤
Line 477: }
Line 478: public void purchase(String symbol, int shares) {
Line 479: symbols.add(symbol);
Line 480: this.shares = shares;
Line 481: purchases.put(symbol, shares);
Line 482: ➤
Line 483: }
Line 484: public int size() {
Line 485: return purchases.size();
Line 486: ➤
Line 487: }
Line 488: public int sharesOf(String symbol) {
Line 489: return purchases.get(symbol);
Line 490: ➤
Line 491: }
Line 492: }
Line 493: With your vaunted key-value data structure and supporting code in place,
Line 494: you can make a pass that eliminates the use of both symbols and shares fields:
Line 495: utj3-tdd/20/src/main/java/app/Portfolio.java
Line 496: import java.util.HashMap;
Line 497: import java.util.Map;
Line 498: public class Portfolio {
Line 499: private Map<String, Integer> purchases = new HashMap<>();
Line 500: public boolean isEmpty() {
Line 501: return purchases.isEmpty();
Line 502: }
Line 503: public void purchase(String symbol, int shares) {
Line 504: purchases.put(symbol, shares);
Line 505: }
Line 506: public int size() {
Line 507: return purchases.size();
Line 508: }
Line 509: Chapter 11. Advancing with Test-Driven Development (TDD) • 222
Line 510: report erratum  •  discuss
Line 511: 
Line 512: --- 페이지 237 ---
Line 513: public int sharesOf(String symbol) {
Line 514: return purchases.get(symbol);
Line 515: }
Line 516: }
Line 517: Oops! You forgot about the zero-based test. Good habits take a while to
Line 518: ingrain, and it’s still possible to temporarily forget even once ingrained.
Line 519: utj3-tdd/21/src/test/java/app/APortfolio.java
Line 520: @Test
Line 521: void returns0SharesForSymbolNotPurchased() {
Line 522: assertEquals(0, portfolio.sharesOf("SONO"));
Line 523: }
Line 524: The failing test requires a single line of production code, a guard clause in
Line 525: the sharesOf method:
Line 526: utj3-tdd/22/src/main/java/app/Portfolio.java
Line 527: public int sharesOf(String symbol) {
Line 528: if (!purchases.containsKey(symbol)) return 0;
Line 529: ➤
Line 530: return purchases.get(symbol);
Line 531: }
Line 532: With a quick refactoring pass and a bit of Java knowledge, you can simplify
Line 533: the two lines into one:
Line 534: utj3-tdd/23/src/main/java/app/Portfolio.java
Line 535: public int sharesOf(String symbol) {
Line 536: return purchases.getOrDefault(symbol, 0);
Line 537: ➤
Line 538: }
Line 539: Next up—making sure that the portfolio returns the total number of shares
Line 540: across all purchases of the same symbol:
Line 541: utj3-tdd/23/src/test/java/app/APortfolio.java
Line 542: @Test
Line 543: void accumulatesSharesOfSameSymbolPurchase() {
Line 544: portfolio.purchase("SONO", 42);
Line 545: portfolio.purchase("SONO", 100);
Line 546: assertEquals(142, portfolio.sharesOf("SONO"));
Line 547: }
Line 548: A small modification on an existing line of code is all you need:
Line 549: utj3-tdd/24/src/main/java/app/Portfolio.java
Line 550: public void purchase(String symbol, int shares) {
Line 551: purchases.put(symbol, sharesOf(symbol + shares)); // OOPS!
Line 552: ➤
Line 553: }
Line 554: report erratum  •  discuss
Line 555: Increment 2: Generalizing the Implementation • 223
Line 556: 
Line 557: --- 페이지 238 ---
Line 558: Except, oops. That’s not quite the right implementation. A real mistake (by
Line 559: me), and the tests quickly caught it. The fix involves moving the parentheses:
Line 560: utj3-tdd/25/src/main/java/app/Portfolio.java
Line 561: public void purchase(String symbol, int shares) {
Line 562: purchases.put(symbol, sharesOf(symbol) + shares);
Line 563: ➤
Line 564: }
Line 565: Increment 3: Factoring Out Redundancies
Line 566: Your next challenge: support selling shares of a stock. There’s not much point
Line 567: in buying stocks in the first place if you can’t sell them.
Line 568: Madhu discusses the requirements with you:
Line 569: • Reduce shares of a holding when selling stocks.
Line 570: • Throw an exception on attempts to sell more shares of a symbol than
Line 571: what is held.
Line 572: Joe says, “okay,” then pauses a moment and asks, “what happens if you sell
Line 573: all the shares of a stock? The portfolio’s size—its count of unique symbols
Line 574: held—should come down by one, right?”
Line 575: Madhu says, “Yes, a good thought, and let’s make sure we test for that.”
Line 576: You both nod to Madhu and then turn to the monitor to code the first test:
Line 577: utj3-tdd/26/src/test/java/app/APortfolio.java
Line 578: @Test
Line 579: void reducesSharesOnSell() {
Line 580: portfolio.purchase("AAPL", 100);
Line 581: portfolio.sell("AAPL", 25);
Line 582: assertEquals(75, portfolio.sharesOf("AAPL"));
Line 583: }
Line 584: The implementation of the new sell method looks exactly like the purchase
Line 585: method, with the exception of the minus sign:
Line 586: utj3-tdd/26/src/main/java/app/Portfolio.java
Line 587: public void purchase(String symbol, int shares) {
Line 588: purchases.put(symbol, sharesOf(symbol) + shares);
Line 589: }
Line 590: public void sell(String symbol, int shares) {
Line 591: ➤
Line 592: purchases.put(symbol, sharesOf(symbol) - shares);
Line 593: ➤
Line 594: }
Line 595: ➤
Line 596: Both methods are heavy on implementation specifics and not abstractions.
Line 597: You can extract the commonality to a shared method named updateShares:
Line 598: Chapter 11. Advancing with Test-Driven Development (TDD) • 224
Line 599: report erratum  •  discuss
Line 600: 
Line 601: --- 페이지 239 ---
Line 602: utj3-tdd/27/src/main/java/app/Portfolio.java
Line 603: public void purchase(String symbol, int shares) {
Line 604: updateShares(symbol, shares);
Line 605: ➤
Line 606: }
Line 607: public void sell(String symbol, int shares) {
Line 608: updateShares(symbol, -shares);
Line 609: ➤
Line 610: }
Line 611: private void updateShares(String symbol, int shares) {
Line 612: ➤
Line 613: purchases.put(symbol, sharesOf(symbol) + shares);
Line 614: }
Line 615: Without the safety control that TDD provides, you would be less likely to
Line 616: make small improvements to the codebase. It’s part of the reason why
Line 617: most codebases steadily degrade over time with lots of crud building up
Line 618: everywhere—poorly expressed code, redundant code, overly complex solutions,
Line 619: and so on. The typical developer has little confidence to properly edit their
Line 620: code once they get their “first draft” working.
Line 621: TDD enables safe refactoring of virtually all of your code.
Line 622: A second test, for the exceptional case:
Line 623: utj3-tdd/28/src/test/java/app/APortfolio.java
Line 624: @Test
Line 625: void throwsWhenSellingMoreSharesThanHeld() {
Line 626: portfolio.purchase("AAPL", 10);
Line 627: assertThrows(InvalidTransactionException.class, () ->
Line 628: portfolio.sell("AAPL", 10 + 1));
Line 629: }
Line 630: The guard clause that gets it to pass:
Line 631: utj3-tdd/28/src/main/java/app/Portfolio.java
Line 632: public void sell(String symbol, int shares) {
Line 633: if (sharesOf(symbol) < shares)
Line 634: ➤
Line 635: throw new InvalidTransactionException();
Line 636: ➤
Line 637: updateShares(symbol, -shares);
Line 638: }
Line 639: You look at the implementation in sell, thinking it needs improvement. The
Line 640: first two lines smack of implementation specifics (even though there aren’t a
Line 641: whole lot of other ways to implement that logic). It doesn’t have the immediacy
Line 642: that the other line in sell has. You extract it to its own method:
Line 643: report erratum  •  discuss
Line 644: Increment 3: Factoring Out Redundancies • 225
Line 645: 
Line 646: --- 페이지 240 ---
Line 647: utj3-tdd/29/src/main/java/app/Portfolio.java
Line 648: public void sell(String symbol, int shares) {
Line 649: abortOnOversell(symbol, shares);
Line 650: ➤
Line 651: updateShares(symbol, -shares);
Line 652: }
Line 653: private void abortOnOversell(String symbol, int shares) {
Line 654: ➤
Line 655: if (sharesOf(symbol) < shares)
Line 656: ➤
Line 657: throw new InvalidTransactionException();
Line 658: ➤
Line 659: }
Line 660: ➤
Line 661: Time to move on to the special case: when all shares of a stock are sold,
Line 662: ensure that the size of the portfolio reduces:
Line 663: utj3-tdd/30/src/test/java/app/APortfolio.java
Line 664: @Test
Line 665: void reducesSizeWhenLiquidatingSymbol() {
Line 666: portfolio.purchase("AAPL", 50);
Line 667: portfolio.sell("AAPL", 50);
Line 668: assertEquals(0, portfolio.size());
Line 669: }
Line 670: The test fails, as expected. Your solution:
Line 671: utj3-tdd/30/src/main/java/app/Portfolio.java
Line 672: public void sell(String symbol, int shares) {
Line 673: abortOnOversell(symbol, shares);
Line 674: updateShares(symbol, -shares);
Line 675: removeSymbolIfSoldOut(symbol);
Line 676: ➤
Line 677: }
Line 678: private void removeSymbolIfSoldOut(String symbol) {
Line 679: ➤
Line 680: if (sharesOf(symbol) == 0)
Line 681: purchases.remove(symbol);
Line 682: }
Line 683: Increment 4: Introducing a Test Double
Line 684: For the final increment, Madhu tells you that you’ll need to capture and save
Line 685: a timestamp for each purchase or sale. He indicates that later requirements
Line 686: will need this information. These are the current requirements:
Line 687: • Provide details about the last transaction (purchase or sale) made,
Line 688: including the timestamp.
Line 689: • Produce a list of all transactions, ordered reverse-chronologically.
Line 690: Chapter 11. Advancing with Test-Driven Development (TDD) • 226
Line 691: report erratum  •  discuss
Line 692: 
Line 693: --- 페이지 241 ---
Line 694: You choose to start with the requirement for the last transaction. Before you
Line 695: forget, you drop a zero-based test in place:
Line 696: utj3-tdd/31/src/test/java/app/APortfolio.java
Line 697: @Test
Line 698: void returnsNullWhenNoPreviousTransactionMade() {
Line 699: assertNull(portfolio.lastTransaction());
Line 700: }
Line 701: The next test, a one-based test for the last transaction, will require you to be
Line 702: able to verify the timestamp of when the transaction was created. Time is an
Line 703: ever-changing quantity. If production code captures the instant in time when
Line 704: a transaction occurs, how can a test know what timestamp to expect?
Line 705: Your solution uses a test double (see Chapter 3, Using Test Doubles, on page
Line 706: 53) that the Java class java.time.Clock provides for just this purpose. You use
Line 707: the static method fixed on the Clock class, providing it a java.time.Instant object.
Line 708: The clock object acts like a real-world broken clock, fixed to one point in time.
Line 709: Every subsequent time inquiry will return the test instant you gave it.
Line 710: After creating a Clock object with a fixed instant, the test injects it into the
Line 711: portfolio via a setter:
Line 712: utj3-tdd/31/src/test/java/app/APortfolio.java
Line 713: @Nested
Line 714: class LastTransaction {
Line 715: Instant now = Instant.now();
Line 716: @BeforeEach
Line 717: void injectFixedClock() {
Line 718: Clock clock = Clock.fixed(now, ZoneId.systemDefault());
Line 719: portfolio.setClock(clock);
Line 720: }
Line 721: @Test
Line 722: void returnsLastTransactionAfterPurchase() {
Line 723: portfolio.purchase("SONO", 20);
Line 724: assertEquals(portfolio.lastTransaction(),
Line 725: new Transaction("SONO", 20, BUY, now));
Line 726: }
Line 727: }
Line 728: The Portfolio class initializes its clock field to a working (production) clock. When
Line 729: run in production, the clock returns the actual instant in time. When run in
Line 730: the context of a unit test, the production clock gets overwritten with the
Line 731: injected “broken” clock. Portfolio code doesn’t know or care about which context
Line 732: it’s executing in.
Line 733: report erratum  •  discuss
Line 734: Increment 4: Introducing a Test Double • 227
Line 735: 
Line 736: --- 페이지 242 ---
Line 737: The following listing introduces both the clock as well as the ability to track
Line 738: a “last transaction” object:
Line 739: utj3-tdd/31/src/main/java/app/Portfolio.java
Line 740: import java.time.Clock;
Line 741: import static app.TransactionType.BUY;
Line 742: import static java.lang.Math.abs;
Line 743: // ...
Line 744: public class Portfolio {
Line 745: private Transaction lastTransaction;
Line 746: ➤
Line 747: private Clock clock = Clock.systemUTC();
Line 748: ➤
Line 749: // ...
Line 750: public void purchase(String symbol, int shares) {
Line 751: updateShares(symbol, shares);
Line 752: }
Line 753: private void updateShares(String symbol, int shares) {
Line 754: lastTransaction =
Line 755: ➤
Line 756: new Transaction(symbol, abs(shares), BUY, clock.instant());
Line 757: ➤
Line 758: purchases.put(symbol, sharesOf(symbol) + shares);
Line 759: }
Line 760: // ...
Line 761: public void setClock(Clock clock) {
Line 762: this.clock = clock;
Line 763: }
Line 764: public Transaction lastTransaction() {
Line 765: ➤
Line 766: return lastTransaction;
Line 767: ➤
Line 768: }
Line 769: ➤
Line 770: }
Line 771: Here are declarations for the supporting types TransactionType and Transaction:
Line 772: utj3-tdd/31/src/main/java/app/TransactionType.java
Line 773: public enum TransactionType {
Line 774: BUY, SELL;
Line 775: }
Line 776: utj3-tdd/31/src/main/java/app/Transaction.java
Line 777: import java.time.Instant;
Line 778: public record Transaction(
Line 779: String symbol, int shares, TransactionType type, Instant now) {}
Line 780: In the prior increment, you factored out the redundancy between the sell and
Line 781: purchase methods, creating a new method, updateShares. It was the better design
Line 782: choice for at least a couple of reasons:
Line 783: • It increased the abstraction level and, thus, the understandability of the code.
Line 784: • It increased the conciseness of the solution, reducing future costs to
Line 785: understand both sell and update.
Line 786: Chapter 11. Advancing with Test-Driven Development (TDD) • 228
Line 787: report erratum  •  discuss
Line 788: 
Line 789: --- 페이지 243 ---
Line 790: Here, the shared method allowed you to isolate the creation of the Transaction
Line 791: to a single method.
Line 792: You add a second test so that the transaction type gets set appropriately for
Line 793: sell transactions:
Line 794: utj3-tdd/32/src/test/java/app/APortfolio.java
Line 795: @Test
Line 796: void returnsLastTransactionAfterSale() {
Line 797: portfolio.purchase("SONO", 200);
Line 798: portfolio.sell("SONO", 40);
Line 799: assertEquals(portfolio.lastTransaction(),
Line 800: new Transaction("SONO", 40, SELL, now));
Line 801: }
Line 802: utj3-tdd/32/src/main/java/app/Portfolio.java
Line 803: public void purchase(String symbol, int shares) {
Line 804: updateShares(symbol, shares, BUY);
Line 805: ➤
Line 806: }
Line 807: public void sell(String symbol, int shares) {
Line 808: abortOnOversell(symbol, shares);
Line 809: updateShares(symbol, -shares, SELL);
Line 810: ➤
Line 811: removeSymbolIfSoldOut(symbol);
Line 812: }
Line 813: private void updateShares(String symbol, int shares, TransactionType type) {
Line 814: ➤
Line 815: lastTransaction =
Line 816: new Transaction(symbol, abs(shares), type, clock.instant());
Line 817: ➤
Line 818: purchases.put(symbol, sharesOf(symbol) + shares);
Line 819: }
Line 820: Moving on to the transaction history requirement:
Line 821: utj3-tdd/33/src/test/java/app/APortfolio.java
Line 822: @Nested
Line 823: class TransactionHistory {
Line 824: Instant now = Instant.now();
Line 825: @BeforeEach
Line 826: void injectFixedClock() {
Line 827: Clock clock = Clock.fixed(now, ZoneId.systemDefault());
Line 828: portfolio.setClock(clock);
Line 829: }
Line 830: @Test
Line 831: void returnsEmptyListWhenNoTransactionsMade() {
Line 832: assertTrue(portfolio.transactions().isEmpty());
Line 833: }
Line 834: report erratum  •  discuss
Line 835: Increment 4: Introducing a Test Double • 229
Line 836: 
Line 837: --- 페이지 244 ---
Line 838: @Test
Line 839: void returnsListOfTransactionsReverseChronologically() {
Line 840: portfolio.purchase("A", 1);
Line 841: portfolio.purchase("B", 2);
Line 842: portfolio.purchase("C", 3);
Line 843: assertEquals(portfolio.transactions(), List.of(
Line 844: new Transaction("C", 3, BUY, now),
Line 845: new Transaction("B", 2, BUY, now),
Line 846: new Transaction("A", 1, BUY, now)
Line 847: ));
Line 848: }
Line 849: }
Line 850: Although two tests are shown here to simplify the presentation in this book,
Line 851: ensure you incrementally write each and develop the solution for each sepa-
Line 852: rately. Writing multiple tests at a time is improper TDD practice.
Line 853: The implementation:
Line 854: utj3-tdd/33/src/main/java/app/Portfolio.java
Line 855: import java.time.Clock;
Line 856: import java.util.LinkedList;
Line 857: import java.util.List;
Line 858: // ...
Line 859: public class Portfolio {
Line 860: private Transaction lastTransaction;
Line 861: ➤
Line 862: private LinkedList transactions = new LinkedList();
Line 863: ➤
Line 864: // ...
Line 865: private void updateShares(String symbol,
Line 866: int shares,
Line 867: TransactionType type) {
Line 868: lastTransaction =
Line 869: new Transaction(symbol, abs(shares), type, clock.instant());
Line 870: transactions.addFirst(lastTransaction);
Line 871: ➤
Line 872: purchases.put(symbol, sharesOf(symbol) + shares);
Line 873: }
Line 874: public Transaction lastTransaction() {
Line 875: return lastTransaction;
Line 876: }
Line 877: public List<Transaction> transactions() {
Line 878: ➤
Line 879: return transactions;
Line 880: ➤
Line 881: }
Line 882: ➤
Line 883: // ...
Line 884: }
Line 885: You no longer need the field lastTransaction, as you can extract the most recent
Line 886: transaction from the transaction list. You’ll want to change both the updateShares
Line 887: and lastTransaction methods. Ensure you remove the field afterward.
Line 888: Chapter 11. Advancing with Test-Driven Development (TDD) • 230
Line 889: report erratum  •  discuss
Line 890: 
Line 891: --- 페이지 245 ---
Line 892: utj3-tdd/34/src/main/java/app/Portfolio.java
Line 893: private void updateShares(String symbol,
Line 894: int shares,
Line 895: TransactionType type) {
Line 896: var transaction =
Line 897: ➤
Line 898: new Transaction(symbol, abs(shares), type, clock.instant());
Line 899: transactions.addFirst(transaction);
Line 900: ➤
Line 901: purchases.put(symbol, sharesOf(symbol) + shares);
Line 902: }
Line 903: public Transaction lastTransaction() {
Line 904: return transactions.peekFirst();
Line 905: ➤
Line 906: }
Line 907: You might consider the solution design at this point to be flawed. It uses two
Line 908: distinct data structures to manage information that could be represented
Line 909: with one. If you consider the list of transactions as the “document of record,”
Line 910: all inquiries regarding the portfolio can be calculated from it. The information
Line 911: captured in the purchases HashMap is essentially an optimized calculation.
Line 912: The dual data structure implementation is a recipe for later disaster, partic-
Line 913: ularly as the solution increases in complexity. If new behaviors are added,
Line 914: it’s possible that an oversight will lead to inconsistent data representations
Line 915: in each data structure.
Line 916: The better solution would be to eliminate the hash map, replacing all inquiries
Line 917: of it with operations on the history stream instead. If you’re curious what this
Line 918: looks like, visit versions 35 and 36 in the source distribution.
Line 919: Test-Driven Development vs. Test-After Development
Line 920: TDD centers on the simple cycle of test-code-refactor. “Significantly reduced
Line 921: defects” would seem to be the key benefit of practicing TDD, but it can accrue
Line 922: some even more valuable benefits. Most of them derive from describing every
Line 923: desired, incremental outcome before coding it into the system.
Line 924: By definition, TDD gives you near-complete unit test coverage, which in turn
Line 925: gives you the following significant benefits:
Line 926: • High confidence that the unit behaviors are correct
Line 927: • The ability to continuously retain a high-quality design
Line 928: • The ability to incorporate new changes safely and without fear
Line 929: • Clear, trustworthy documentation on all intended behaviors
Line 930: Your cost of change can reduce dramatically as a result.
Line 931: report erratum  •  discuss
Line 932: Test-Driven Development vs. Test-After Development • 231
Line 933: 
Line 934: --- 페이지 246 ---
Line 935: You’ve been learning test-after development (TAD, as in “a tad too late”) in
Line 936: this book. With TAD, testing is an afterthought—as in, “I thought about
Line 937: writing some unit tests after I developed my stellar code but decided not to.”
Line 938: You could absolutely achieve full coverage with TAD. There’s no mechanical
Line 939: reason why you couldn’t write TAD tests that cover every behavior in your
Line 940: system. The reality, though, is that almost no one ever does.
Line 941: TAD can be harder than TDD. Determining all the behavioral intents of previ-
Line 942: ously written code can be tough, even if it was written within the last hour.
Line 943: It seems simpler, in contrast, to first capture the desired outcome with a test.
Line 944: Writing tests for code with private dependencies and myriad entanglements
Line 945: is also tough. It seems simpler to shape code to align with the needs of a test
Line 946: instead of the other way around.
Line 947: Here’s a short list of reasons we don’t write enough tests when doing TAD:
Line 948: 1.
Line 949: We run out of time and are told to move on to the next thing. “We just
Line 950: need to ship.”
Line 951: 2.
Line 952: Because it’s often hard, we sometimes give up, particularly if we’re told
Line 953: to move on.
Line 954: 3.
Line 955: We think our code doesn’t stink. “I just wrote this, it looks great.”
Line 956: 4.
Line 957: We avoid it because unit testing isn’t as much fun as writing the produc-
Line 958: tion code.
Line 959: 5.
Line 960: Someone else told us we had to do it, which can be another discourage-
Line 961: ment for some of us.
Line 962: Re-read How Much Coverage Is Enough?, on page 77 if you think there’s little
Line 963: difference between 75% and 100% coverage. Minimally, remember that 75%
Line 964: coverage means that a quarter of the code in your system remains at risk.
Line 965: The Rhythm of TDD
Line 966: TDD cycles are short. Without all the chatter accompanying this chapter’s
Line 967: example, each test-code-refactor cycle takes maybe a few minutes. Increments
Line 968: of code written or changed at each step in the cycle are likewise small.
Line 969: Once you’ve established a short-cycle rhythm with TDD, it becomes obvious
Line 970: when you’re heading down a rathole. Set a regular time limit of about ten
Line 971: minutes. If you haven’t received any positive feedback (passing tests) in the
Line 972: last ten minutes, discard what you were working on and try again, taking
Line 973: Chapter 11. Advancing with Test-Driven Development (TDD) • 232
Line 974: report erratum  •  discuss
Line 975: 
Line 976: --- 페이지 247 ---
Line 977: even smaller steps. If you were committing after introducing (and cleaning)
Line 978: each new increment, reverting to the prior increment will be a trivial operation.
Line 979: Yes, you heard right—throw away costly code. Treat each cycle of TDD as a
Line 980: time-boxed experiment whose test is the hypothesis. If the experiment is going
Line 981: awry, restarting the experiment and shrinking the scope of assumptions
Line 982: (taking smaller steps) can help you pinpoint where things went wrong. The
Line 983: fresh take can often help you derive a better solution in less time than you
Line 984: would have wasted on the mess you were making.
Line 985: Summary
Line 986: In this chapter, you toured the practice of TDD, which takes all the concepts
Line 987: you’ve learned about unit testing and puts them into a simple disciplined
Line 988: cycle: write a test, get it to pass, ensure the code is clean, and repeat.
Line 989: Adopting TDD may change the way you think about design.
Line 990: Next, you’ll learn about some topics relevant to unit testing as part of a
Line 991: development team.
Line 992: report erratum  •  discuss
Line 993: Summary • 233