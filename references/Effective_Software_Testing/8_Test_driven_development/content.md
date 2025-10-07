Line 1: 
Line 2: --- 페이지 226 ---
Line 3: 198
Line 4: Test-driven development
Line 5: Software developers are pretty used to the traditional development process. First,
Line 6: they implement. Then, and only then, they test. But why not do it the other way
Line 7: around? In other words, why not write a test first and then implement the produc-
Line 8: tion code?
Line 9:  In this chapter, we discuss this well-known approach: test-driven development (TDD).
Line 10: In a nutshell, TDD challenges our traditional way of coding, which has always been
Line 11: “write some code and then test it.” With TDD, we start by writing a test representing
Line 12: the next small feature we want to implement. This test naturally fails, as the feature
Line 13: has not yet been implemented! We then make the test pass by writing some code.
Line 14: With the test now green, and knowing that the feature has been implemented, we
Line 15: go back to the code we wrote and refactor it.
Line 16:  TDD is a popular practice, especially among Agile practitioners. Before I dive
Line 17: into the advantages of TDD and pragmatic questions about working this way, let’s
Line 18: look at a small example.
Line 19: This chapter covers
Line 20: Understanding test-driven development
Line 21: Being productive with TDD
Line 22: When not to use TDD
Line 23: 
Line 24: --- 페이지 227 ---
Line 25: 199
Line 26: Our first TDD session
Line 27: 8.1
Line 28: Our first TDD session
Line 29: For this example, we will create a program that converts Roman numerals to integers.
Line 30: Roman numerals represent numbers with seven symbols:
Line 31: I, unus, 1, (one)
Line 32: V, quinque, 5 (five)
Line 33: X, decem, 10 (ten)
Line 34: L, quinquaginta, 50 (fifty)
Line 35: C, centum, 100 (one hundred)
Line 36: D, quingenti, 500 (five hundred)
Line 37: M, mille, 1,000 (one thousand)
Line 38: To represent all possible numbers, the Romans combined the symbols, following
Line 39: these two rules:
Line 40: Digits of lower or equal value on the right are added to the higher-value digit.
Line 41: Digits of lower value on the left are subtracted from the higher-value digit.
Line 42: For instance, the number XV represents 15 (10 + 5), and the number XXIV rep-
Line 43: resents 24 (10 + 10 – 1 + 5).
Line 44:  The goal of our TDD session is to implement the following requirement:
Line 45: Implement a program that receives a Roman numeral (as a string) and
Line 46: returns its representation in the Arabic numeral system (as an integer).
Line 47: Coming up with examples is part of TDD. So, think about different inputs you can
Line 48: give the program, and their expected outputs. For example, if we input "I" to the
Line 49: program, we expect it to return 1. If we input "XII" to the program, we expect it to
Line 50: return 12. Here are the cases I can think of:
Line 51: Simple cases, such as numbers with single characters:
Line 52: – If we input "I", the program must return 1.
Line 53: – If we input "V", the program must return 5.
Line 54: – If we input "X", the program must return 10.
Line 55: Numbers composed of more than one character (without using the subtrac-
Line 56: tive notation):
Line 57: – If we input "II", the program must return 2.
Line 58: – If we input "III", the program must return 3.
Line 59: – If we input "VI", the program must return 6.
Line 60: – If we input "XVII", the program must return 17.
Line 61: Numbers that use simple subtractive notation:
Line 62: – If we input "IV", the program must return 4.
Line 63: – If we input "IX", the program must return 9.
Line 64: 
Line 65: --- 페이지 228 ---
Line 66: 200
Line 67: CHAPTER 8
Line 68: Test-driven development
Line 69: Numbers that are composed of many characters and use subtractive notation:
Line 70: – If we input "XIV", the program must return 14.
Line 71: – If we input "XXIX", the program must return 29.
Line 72: NOTE
Line 73: You may wonder about corner cases: What about an empty string? or
Line 74: null? Those cases are worth testing. However, when doing TDD, I first focus
Line 75: on the happy path and the business rules; I consider corners and boundar-
Line 76: ies later.
Line 77: Remember, we are not in testing mode. We are in development mode, coming up with
Line 78: inputs and outputs (or test cases) that will guide us through the implementation. In
Line 79: the development flow I introduced in figure 1.4, TDD is part of “testing to guide
Line 80: development.” When we are finished with the implementation, we can dive into rigor-
Line 81: ous testing using all the techniques we have discussed.
Line 82:  Now that we have a (short) list of examples, we can write some code. Let’s do it
Line 83: this way:
Line 84: 1
Line 85: Select the simplest example from our list of examples.
Line 86: 2
Line 87: Write an automated test case that exercises the program with the given input
Line 88: and asserts its expected output. The code may not even compile at this point.
Line 89: And if it does, the test will fail, as the functionality is not implemented.
Line 90: 3
Line 91: Write as much production code as needed to make that test pass.
Line 92: 4
Line 93: Stop and reflect on what we have done so far. We may improve the production
Line 94: code. We may improve the test code. We may add more examples to our list.
Line 95: 5
Line 96: Repeat the cycle.
Line 97: The first iteration of the cycle focuses on ensuring that if we give "I" as input, the out-
Line 98: put is 1. The RomanNumeralConverterTest class contains our first test case.
Line 99: public class RomanNumberConverterTest {
Line 100:   @Test
Line 101:   void shouldUnderstandSymbolI() {
Line 102:     RomanNumeralConverter roman = new RomanNumeralConverter(); 
Line 103:     int number = roman.convert("I");
Line 104:     assertThat(number).isEqualTo(1);
Line 105:   }
Line 106: }
Line 107: At this moment, the test code does not compile, because the RomanNumberConverter
Line 108: class and its convert() method do not exist. To solve the compilation error, let’s cre-
Line 109: ate some skeleton code with no real implementation.
Line 110: public class RomanNumeralConverter {
Line 111:   public int convert(String numberInRoman) {
Line 112: Listing 8.1
Line 113: Our first test method
Line 114: Listing 8.2
Line 115: Skeleton implementation of the class
Line 116: We will get compilation errors here,
Line 117: as the RomanNumeralConverter
Line 118: class does not exist!
Line 119: 
Line 120: --- 페이지 229 ---
Line 121: 201
Line 122: Our first TDD session
Line 123:     return 0; 
Line 124:   }
Line 125: }
Line 126: The test code now compiles. When we run it, it fails: the test expected 1, but the pro-
Line 127: gram returned 0. This is not a problem, as we expected it to fail. Steps 1 and 2 of our
Line 128: cycle are finished. It is now time to write as much code as needed to make the test
Line 129: pass—and it looks weird.
Line 130: public class RomanNumeralConverter {
Line 131:   public int convert(String numberInRoman) {
Line 132:     return 1; 
Line 133:   }
Line 134: }
Line 135: The test passes, but it only works in a single case. Again, this is not a problem: we are
Line 136: still working on the implementation. We are taking baby steps.
Line 137:  Let’s move on to the next iteration of the cycle. The next-simplest example in the
Line 138: list is “If we input "V", the program must return 5.” Let’s again begin with the test.
Line 139: @Test
Line 140: void shouldUnderstandSymbolV() {
Line 141:   RomanNumeralConverter roman = new RomanNumeralConverter();
Line 142:   int number = roman.convert("V");
Line 143:   assertThat(number).isEqualTo(5);
Line 144: }
Line 145: The new test code compiles and fails. Now let’s make it pass. In the implementation,
Line 146: we can, for example, make the method convert() verify the content of the number to
Line 147: be converted. If the value is "I", the method returns 1. If the value is "V", it returns 5.
Line 148: public int convert(String numberInRoman) {
Line 149:   if(numberInRoman.equals("I")) return 1; 
Line 150:   if(numberInRoman.equals("V")) return 5;
Line 151:   return 0;
Line 152: }
Line 153: The two tests pass. We could repeat the cycle for X, L, C, M, and so on, but we already
Line 154: have a good idea about the first thing our implementation needs to generalize: when
Line 155: the Roman numeral has only one symbol, return the integer associated with it. How
Line 156: can we implement such an algorithm?
Line 157: Write a set of if statements. The number of characters we need to handle is not
Line 158: excessive.
Line 159: Listing 8.3
Line 160: Making the test pass
Line 161: Listing 8.4
Line 162: Our second test
Line 163: Listing 8.5
Line 164: Making the tests pass
Line 165: We do not want to return 0, but 
Line 166: this makes the test code compile.
Line 167: Returning 1 makes the 
Line 168: test pass. But is this the 
Line 169: implementation we want?
Line 170: Hard-coded ifs are the easiest 
Line 171: way to make both tests pass.
Line 172: 
Line 173: --- 페이지 230 ---
Line 174: 202
Line 175: CHAPTER 8
Line 176: Test-driven development
Line 177: Write a switch statement, similar to the if implementation.
Line 178: Use a map that is initialized with all the symbols and their respective integer
Line 179: values.
Line 180: The choice is a matter of taste. I will use the third option because I like it best.
Line 181: public class RomanNumeralConverter {
Line 182:   private static Map<String, Integer> table =
Line 183:       new HashMap<>() {{ 
Line 184:         put("I", 1);
Line 185:         put("V", 5);
Line 186:         put("X", 10);
Line 187:         put("L", 50);
Line 188:         put("C", 100);
Line 189:         put("D", 500);
Line 190:         put("M", 1000);
Line 191:       }};
Line 192:   public int convert(String numberInRoman) {
Line 193:     return table.get(numberInRoman); 
Line 194:   }
Line 195: }
Line 196: How do we make sure our implementation works? We have our (two) tests, and we
Line 197: can run them. Both pass. The production code is already general enough to work
Line 198: for single-character Roman numbers. But our test code is not: we have a test called
Line 199: shouldUnderstandSymbolI and another called shouldUnderstandSymbolV. This specific
Line 200: case would be better represented in a parameterized test called shouldUnderstandOne-
Line 201: CharNumbers.
Line 202: public class RomanNumeralConverterTest {
Line 203:   @ParameterizedTest
Line 204:   @CsvSource({"I,1","V,5", "X,10","L,50",
Line 205:   "C, 100", "D, 500", "M, 1000"}) 
Line 206:   void shouldUnderstandOneCharNumbers(String romanNumeral,
Line 207:     ➥ int expectedNumberAfterConversion) {
Line 208:     RomanNumeralConverter roman = new RomanNumeralConverter();
Line 209:     int convertedNumber = roman.convert(romanNumeral);
Line 210:     assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
Line 211:   }
Line 212: }
Line 213: NOTE
Line 214: The test code now has some duplicate code compared to the produc-
Line 215: tion code. The test inputs and outputs somewhat match the map in the pro-
Line 216: duction code. This is a common phenomenon when doing testing by
Line 217: example, and it will be mitigated when we write more complex tests.
Line 218: Listing 8.6
Line 219: RomanNumeralConverter for single-character numbers
Line 220: Listing 8.7
Line 221: Generalizing our first test
Line 222: Declares a conversion table that 
Line 223: contains the Roman numerals 
Line 224: and their corresponding 
Line 225: decimal numbers
Line 226: Gets the 
Line 227: number from 
Line 228: the table
Line 229: Passes the inputs as a comma-separated 
Line 230: value to the parameterized test. JUnit 
Line 231: then runs the test method for each of 
Line 232: the inputs.
Line 233: 
Line 234: --- 페이지 231 ---
Line 235: 203
Line 236: Our first TDD session
Line 237: We are finished with the first set of examples. Let’s consider the second scenario: two
Line 238: or more characters in a row, such as II or XX. Again, we start with the test code.
Line 239: @Test
Line 240: void shouldUnderstandMultipleCharNumbers() {
Line 241:   RomanNumeralConverter roman = new RomanNumeralConverter();
Line 242:   int convertedNumber = roman.convert("II");
Line 243:   assertThat(convertedNumber).isEqualTo(2);
Line 244: }
Line 245: To make the test pass in a simple way, we could add the string “II” to the map.
Line 246: private static Map<String, Integer> table =
Line 247:   new HashMap<>() {{
Line 248:     put("I", 1);
Line 249:     put("II", 2); 
Line 250:     put("V", 5);
Line 251:     put("X", 10);
Line 252:     put("L", 50);
Line 253:     put("C", 100);
Line 254:     put("D", 500);
Line 255:     put("M", 1000);
Line 256:   }};
Line 257: If we did this, the test would succeed. But it does not seem like a good idea for imple-
Line 258: mentation, because we would have to include all possible symbols in the map. It is
Line 259: time to generalize our implementation again. The first idea that comes to mind is to
Line 260: iterate over each symbol in the Roman numeral we’re converting, accumulate the
Line 261: value, and return the total value. A simple loop should do.
Line 262: public class RomanNumeralConverter {
Line 263:   private static Map<Character, Integer> table =
Line 264:       new HashMap<>() {{ 
Line 265:         put('I', 1);
Line 266:         put('V', 5);
Line 267:         put('X', 10);
Line 268:         put('L', 50);
Line 269:         put('C', 100);
Line 270:         put('D', 500);
Line 271:         put('M', 1000);
Line 272:       }};
Line 273:   public int convert(String numberInRoman) {
Line 274:     int finalNumber = 0; 
Line 275: Listing 8.8
Line 276: Tests for Roman numerals with multiple characters
Line 277: Listing 8.9
Line 278: Map with all the Roman numerals
Line 279: Listing 8.10
Line 280: Looping through each character in the Roman numeral
Line 281: Adds II. But that means 
Line 282: we would need to add III, 
Line 283: IV, and so on—not a 
Line 284: good idea!
Line 285: The conversion table 
Line 286: only contains the 
Line 287: unique Roman 
Line 288: numeral.
Line 289: Variable that aggregates 
Line 290: the value of each Roman 
Line 291: numeral
Line 292: 
Line 293: --- 페이지 232 ---
Line 294: 204
Line 295: CHAPTER 8
Line 296: Test-driven development
Line 297:     for(int i = 0; i < numberInRoman.length(); i++) { 
Line 298:       finalNumber += table.get(numberInRoman.charAt(i));
Line 299:     }
Line 300:     return finalNumber;
Line 301:   }
Line 302: }
Line 303: Note that the type of key in the map has changed from String to Character. The
Line 304: algorithm iterates over each character of the string numberInRoman using the
Line 305: charAt() method, which returns a char type. We could convert the char to String,
Line 306: but doing so would add an extra, unnecessary step.
Line 307:  The three tests continue passing. It is important to realize that our focus in this cycle
Line 308: was to make our algorithm work with Roman numerals with more than one character—
Line 309: we were not thinking about the previous examples. This is one of the main advantages
Line 310: of having the tests: we are sure that each step we take is sound. Any bugs we introduce to
Line 311: previously working behavior (regression bugs) will be captured by our tests.
Line 312:  We can now generalize the test code and exercise other examples that are similar to
Line 313: the previous one. We again use parameterized tests, as they work well for the purpose.
Line 314: @ParameterizedTest
Line 315: @CsvSource({"II,2","III,3", "VI, 6", "XVIII, 18",
Line 316: "XXIII, 23", "DCCLXVI, 766"}) 
Line 317: void shouldUnderstandMultipleCharNumbers(String romanNumeral,
Line 318:   ➥ int expectedNumberAfterConversion) {
Line 319:   RomanNumeralConverter roman = new RomanNumeralConverter();
Line 320:   int convertedNumber = roman.convert(romanNumeral);
Line 321:   assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
Line 322: }
Line 323: NOTE
Line 324: I chose the examples I passed to the test at random. Our goal is not to
Line 325: be fully systematic when coming up with examples but only to use the test
Line 326: cases as a safety net for developing the feature. When we’re finished, we will
Line 327: perform systematic testing.
Line 328: Listing 8.11
Line 329: Parameterizing the test for multiple characters
Line 330: A single test method or many?
Line 331: This test method is very similar to the previous one. We could combine them into a
Line 332: single test method, as shown here:
Line 333: @ParameterizedTest
Line 334: @CsvSource({ 
Line 335:   // single character numbers
Line 336:   "I,1","V,5", "X,10","L,50", "C, 100", "D, 500", "M, 1000",
Line 337:   // multiple character numbers
Line 338:   "II,2","III,3", "V,5","VI, 6", "XVIII, 18", "XXIII, 23", "DCCLXVI, 766"
Line 339: })
Line 340: Gets each 
Line 341: character’s 
Line 342: corresponding 
Line 343: decimal value 
Line 344: and adds it to 
Line 345: the total sum
Line 346: Tries many inputs 
Line 347: with multiple 
Line 348: characters. Again, 
Line 349: CSVSource is the 
Line 350: simplest way to 
Line 351: do this.
Line 352: All the inputs from the different tests 
Line 353: are combined into a single method.
Line 354: 
Line 355: --- 페이지 233 ---
Line 356: 205
Line 357: Our first TDD session
Line 358: Our next step is to make the subtractive notation work: for example, IV should return 4.
Line 359: As always, let’s start with the test. This time, we add multiple examples: we understand
Line 360: the problem and can take a bigger step. If things go wrong, we can take a step back.
Line 361: @ParameterizedTest
Line 362: @CsvSource({"IV,4","XIV,14", "XL, 40",
Line 363: "XLI,41", "CCXCIV, 294"}) 
Line 364: void shouldUnderstandSubtractiveNotation(String romanNumeral,
Line 365:   ➥ int expectedNumberAfterConversion) {
Line 366:   RomanNumeralConverter roman = new RomanNumeralConverter();
Line 367:   int convertedNumber = roman.convert(romanNumeral);
Line 368:   assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
Line 369: }
Line 370: Implementing this part of the algorithm requires more thought. The characters in a
Line 371: Roman numeral, from right to left, increase in terms of value. However, when a numeral
Line 372: is smaller than its neighbor on the right, it must be subtracted from instead of added to
Line 373: the accumulator. Listing 8.13 uses a trick to accomplish this: the multiplier variable
Line 374: becomes -1 if the current numeral (that is, the current character we are looking at) is
Line 375: smaller than the last neighbor (that is, the character we looked at previously). We
Line 376: then multiply the current digit by multiplier to make the digit negative.
Line 377: public int convert(String numberInRoman) {
Line 378:   int finalNumber = 0;
Line 379:   int lastNeighbor = 0; 
Line 380:   for(int i = numberInRoman.length() - 1; i >= 0; i--) { 
Line 381:    int current = table.get(numberInRoman.charAt(i)); 
Line 382:    int multiplier = 1;
Line 383:    if(current < lastNeighbor) multiplier = -1; 
Line 384: void convertRomanNumerals(String romanNumeral,
Line 385:   ➥ int expectedNumberAfterConversion) {
Line 386:   RomanNumeralConverter roman = new RomanNumeralConverter();
Line 387:   int convertedNumber = roman.convert(romanNumeral);
Line 388:   assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
Line 389: }
Line 390: This is a matter of taste and your team’s preference. For the remainder of the chap-
Line 391: ter, I keep the test methods separated.
Line 392: Listing 8.12
Line 393: Test for the subtractive notation
Line 394: Listing 8.13
Line 395: Implementation for the subtractive notation
Line 396: Provides many inputs that exercise 
Line 397: the subtractive notation rule
Line 398: Keeps the last 
Line 399: visited digit
Line 400: Loops through the 
Line 401: characters, but now 
Line 402: from right to left
Line 403: Gets the decimal value of 
Line 404: the current Roman digit
Line 405: If the previous digit was 
Line 406: higher than the current one, 
Line 407: multiplies the current digit 
Line 408: by -1 to make it negative
Line 409: 
Line 410: --- 페이지 234 ---
Line 411: 206
Line 412: CHAPTER 8
Line 413: Test-driven development
Line 414:    finalNumber +=
Line 415:      table.get(numberInRoman.charAt(i)) * multiplier; 
Line 416:    lastNeighbor = current; 
Line 417:   }
Line 418:   return finalNumber;
Line 419: }
Line 420: The tests pass. Is there anything we want to improve in the production code? We use
Line 421: numberInRoman.charAt(i) when summing the final number, but this value is already
Line 422: stored in the current variable, so we can reuse it. Also, extracting a variable to store
Line 423: the current digit after it is multiplied by 1 or -1 will help developers understand the
Line 424: algorithm. We can refactor the code, as shown in the following listing, and run the
Line 425: tests again.
Line 426: public int convert(String numberInRoman) {
Line 427:   int finalNumber = 0;
Line 428:   int lastNeighbor = 0; 
Line 429:   for(int i = numberInRoman.length() - 1; i >= 0; i--) {
Line 430:    int current = table.get(numberInRoman.charAt(i));
Line 431:    int multiplier = 1;
Line 432:    if(current < lastNeighbor) multiplier = -1;
Line 433:    int currentNumeralToBeAdded = current * multiplier; 
Line 434:    finalNumber += currentNumeralToBeAdded;
Line 435:    lastNeighbor = current;
Line 436:   }
Line 437:   return finalNumber;
Line 438: }
Line 439: Now that we have implemented all the examples in our initial list, we can think of other
Line 440: cases to handle. We are not handling invalid numbers, for example. The program must
Line 441: reject inputs such as "VXL" and "ILV". When we have new examples, we repeat the
Line 442: entire procedure until the whole program is implemented. I will leave that as an exer-
Line 443: cise for you—we have done enough that we are ready to more formally discuss TDD. 
Line 444: 8.2
Line 445: Reflecting on our first TDD experience
Line 446: Abstractly, the cycle we repeated in the previous section’s development process was
Line 447: as follows:
Line 448: 1
Line 449: We wrote a (unit) test for the next piece of functionality we wanted to imple-
Line 450: ment. The test failed.
Line 451: Listing 8.14
Line 452: Refactored version
Line 453: Adds the current digit 
Line 454: to the finalNumber 
Line 455: variable. The current 
Line 456: digit is positive or 
Line 457: negative depending on 
Line 458: whether we should 
Line 459: add or subtract it, 
Line 460: respectively.
Line 461: Updates 
Line 462: lastNeighbor 
Line 463: to be the 
Line 464: current digit
Line 465: Keeps the last 
Line 466: digit visited
Line 467: Uses the current
Line 468: variable and introduces the
Line 469: currentNumeralToBeAdded variable
Line 470: 
Line 471: --- 페이지 235 ---
Line 472: 207
Line 473: Reflecting on our first TDD experience
Line 474: 2
Line 475: We implemented the functionality. The test passed.
Line 476: 3
Line 477: We refactored our production and test code.
Line 478: This TDD process is also called the red-green-refactor cycle. Figure 8.1 shows a popular
Line 479: way to represent the TDD cycle.
Line 480: TDD practitioners say this approach can be very advantageous for the development
Line 481: process. Here are some of the advantages:
Line 482: Looking at the requirements first—In the TDD cycle, the tests we write to support
Line 483: development are basically executable requirements. Whenever we write one of
Line 484: them, we reflect on what the program should and should not do.
Line 485: This approach makes us write code for the specific problem we are supposed
Line 486: to solve, preventing us from writing unnecessary code. And exploring the
Line 487: requirement systematically forces us to think deeply about it. Developers often
Line 488: go back to the requirements engineer and ask questions about cases that are
Line 489: not explicit in the requirement.
Line 490: Full control over the pace of writing production code—If we are confident about the
Line 491: problem, we can take a big step and create a test that involves more compli-
Line 492: cated cases. However, if we are still unsure how to tackle the problem, we can
Line 493: break it into smaller parts and create tests for these simpler pieces first.
Line 494: Quick feedback—Developers who do not work in TDD cycles produce large
Line 495: chunks of production code before getting any feedback. In a TDD cycle, devel-
Line 496: opers are forced to take one step at a time. We write one test, make it pass, and
Line 497: reflect on it. These many moments of reflection make it easier to identify new
Line 498: problems as they arise, because we have only written a small amount of code
Line 499: since the last time everything was under control.
Line 500: Testable code—Creating the tests first makes us think from the beginning about a
Line 501: way to (easily) test the production code before implementing it. In the tradi-
Line 502: tional flow, developers often think about testing only in the later stages of devel-
Line 503: oping a feature. At that point, it may be expensive to change how the code
Line 504: works to facilitate testing.
Line 505: Test
Line 506: passes
Line 507: Test fails
Line 508: Refactor
Line 509: Write a
Line 510: (simple)
Line 511: test.
Line 512: Make it
Line 513: pass.
Line 514: Figure 8.1
Line 515: TDD, also known as the 
Line 516: red-green-refactor cycle
Line 517: 
Line 518: --- 페이지 236 ---
Line 519: 208
Line 520: CHAPTER 8
Line 521: Test-driven development
Line 522: Feedback about design—The test code is often the first client of the class or com-
Line 523: ponent we are developing. A test method instantiates the class under test,
Line 524: invokes a method passing all its required parameters, and asserts that the
Line 525: method produces the expected results. If this is hard to do, perhaps there is a
Line 526: better way to design the class. When doing TDD, these problems arise earlier in
Line 527: the development of the feature. And the earlier we observe such issues, the
Line 528: cheaper it is to fix them.
Line 529: NOTE
Line 530: TDD shows its advantages best in more complicated problems. I sug-
Line 531: gest watching James Shore’s YouTube playlist on TDD (2014), where he TDDs
Line 532: an entire software system. I also recommend Freeman and Pryce’s book Grow-
Line 533: ing Object-Oriented Systems Guided by Tests (2009). They also TDD an entire system,
Line 534: and they discuss in depth how they use tests to guide their design decisions.
Line 535: 8.3
Line 536: TDD in the real world
Line 537: This section discusses the most common questions and discussions around TDD.
Line 538: Some developers love TDD and defend its use fiercely; others recommend not
Line 539: using it.
Line 540:  As always, software engineering practices are not silver bullets. The reflections I
Line 541: share in this section are personal and not based on scientific evidence. The best way to
Line 542: see if TDD is beneficial for you is to try it!
Line 543: 8.3.1
Line 544: To TDD or not to TDD?
Line 545: Skeptical readers may be thinking, “I can get the same benefits without doing TDD. I
Line 546: can think more about my requirements, force myself to only implement what is
Line 547: needed, and consider the testability of my class from the beginning. I do not need to
Line 548: write tests for that!” That is true. But I appreciate TDD because it gives me a rhythm to
Line 549: follow. Finding the next-simplest feature, writing a test for it, implementing nothing
Line 550: more than what is needed, and reflecting on what I did gives me a pace that I can fully
Line 551: control. TDD helps me avoid infinite loops of confusion and frustration.
Line 552:  The more defined development cycle also reminds me to review my code often.
Line 553: The TDD cycle offers a natural moment to reflect: as soon as the test passes. When
Line 554: all my tests are green, I consider whether there is anything to improve in the cur-
Line 555: rent code.
Line 556:  Designing classes is one of the most challenging tasks of a software engineer. I
Line 557: appreciate the TDD cycle because it forces me to use the code I am developing from
Line 558: the very beginning. The perception I have about the class I am designing is often dif-
Line 559: ferent from my perception when I try to use the class. I can combine both of these
Line 560: perceptions and make the best decision about how to model the class.
Line 561:  If you write the tests after the code, and not before, as in TDD, the challenge is
Line 562: making sure the time between writing code and testing is small enough to provide
Line 563: developers with timely feedback. Don’t write code for an entire day and then start test-
Line 564: ing—that may be too late.
Line 565: 
Line 566: --- 페이지 237 ---
Line 567: 209
Line 568: TDD in the real world
Line 569: 8.3.2
Line 570: TDD 100% of the time?
Line 571: Should we always use TDD? My answer is a pragmatic “no.” I do a lot of TDD, but I do
Line 572: not use TDD 100% of the time. It depends on how much I need to learn about the
Line 573: feature I am implementing:
Line 574: I use TDD when I don’t have a clear idea of how to design, architect, or imple-
Line 575: ment a specific requirement. In such cases, I like to go slowly and use my tests
Line 576: to experiment with different possibilities. If I am working on a problem I
Line 577: know well, and I already know the best way to solve the problem, I do not
Line 578: mind skipping a few cycles.
Line 579: I use TDD when dealing with a complex problem or a problem I lack the
Line 580: expertise to solve. Whenever I face a challenging implementation, TDD helps
Line 581: me take a step back and learn about the requirements as I go by writing very
Line 582: small tests.
Line 583: I do not use TDD when there is nothing to be learned in the process. If I already
Line 584: know the problem and how to best solve it, I am comfortable coding the solu-
Line 585: tion directly. (Even if I do not use TDD, I always write tests promptly. I never
Line 586: leave it until the end of the day or the end of the sprint. I code the production
Line 587: code, and then I code the test code. And if I have trouble, I take a step back and
Line 588: slow down.)
Line 589: TDD creates opportunities for me to learn more about the code I am writing from an
Line 590: implementation point of view (does it do what it needs to do?) as well as from a design
Line 591: point of view (is it structured in a way that I want?). But for some complex features, it’s
Line 592: difficult even to determine what the first test should look like; in those cases, I do not
Line 593: use TDD.
Line 594:  We need ways to stop and think about what we are doing. TDD is a perfect
Line 595: approach for that purpose, but not the only one. Deciding when to use TDD comes
Line 596: with experience. You will quickly learn what works best for you. 
Line 597: 8.3.3
Line 598: Does TDD work for all types of applications and domains?
Line 599: TDD works for most types of applications and domains. There are even books about
Line 600: using it for embedded systems, where things are naturally more challenging, such as
Line 601: Grenning’s book Test Driven Development for Embedded C (2011). If you can write auto-
Line 602: mated tests for your application, you can do TDD. 
Line 603: 8.3.4
Line 604: What does the research say about TDD?
Line 605: TDD is such a significant part of software development that it is no wonder research-
Line 606: ers try to assess its effectiveness using scientific methods. Because so many people
Line 607: treat it as a silver bullet, I strongly believe that you should know what practitioners
Line 608: think, what I think, and what research currently knows about the subject.
Line 609:  Research has shown several situations in which TDD can improve class design:
Line 610: 
Line 611: --- 페이지 238 ---
Line 612: 210
Line 613: CHAPTER 8
Line 614: Test-driven development
Line 615: Janzen (2005) showed that TDD practitioners, compared to non-TDDers, pro-
Line 616: duced less-complex algorithms and test suites that covered more.
Line 617: Janzen and Saiedian (2006) showed that the code produced using TDD made
Line 618: better use of object-oriented concepts, and responsibilities were better distrib-
Line 619: uted into different classes. In contrast, other teams produced more proce-
Line 620: dural code.
Line 621: George and Williams (2003) showed that although TDD can initially reduce the
Line 622: productivity of inexperienced developers, 92% of the developers in a qualitative
Line 623: analysis thought that TDD helped improve code quality.
Line 624: Dogša and Baticˇ (2011) also found an improvement in class design when using
Line 625: TDD. According to the authors, the improvement resulted from the simplicity
Line 626: TDD adds to the process.
Line 627: Erdogmus et al. (2005) used an experiment with 24 undergraduate students to
Line 628: show that TDD increased their productivity but did not change the quality of
Line 629: the produced code.
Line 630: Nagappan and colleagues (2008) performed three case studies at Microsoft and
Line 631: showed that the pre-release defect density of projects that were TDD’d
Line 632: decreased 40 to 90% in comparison to projects that did not do TDD.
Line 633: Fucci et al. (2016) argue that the important aspect is writing tests (before or after).
Line 634: Gerosa and I (2015) have made similar observations after interviewing many TDD
Line 635: practitioners. This is also the perception of practitioners. To quote Michael Feathers
Line 636: (2008), “That’s the magic, and it’s why unit testing works also. When you write unit
Line 637: tests, TDD-style or after your development, you scrutinize, you think, and often you
Line 638: prevent problems without even encountering a test failure.”
Line 639:  However, other academic studies show inconclusive results for TDD:
Line 640: Müeller and Hagner (2002), after an experiment with 19 students taking a one-
Line 641: semester graduate course on extreme programming, observed that test-first did
Line 642: not accelerate implementation compared to traditional approaches. The code
Line 643: written with TDD was also not more reliable.
Line 644: Siniaalto and Abrahamsson (2007) compared five small-scale software proj-
Line 645: ects using different code metrics and showed that the benefits of TDD were
Line 646: not clear.
Line 647: Shull and colleagues (2010), after summarizing the findings of 14 papers on
Line 648: TDD, concluded that TDD shows no consistent effect on internal code quality.
Line 649: This paper is easy to read, and I recommend that you look at it.
Line 650: As an academic who has read most of the work on this topic, I find that many of these
Line 651: studies—both those that show positive effects and those that do not—are not perfect.
Line 652: Some use students, who are not experts in software development or TDD. Others use
Line 653: toy projects without specific room for TDD to demonstrate its benefits. And some use
Line 654: code metrics such as coupling and cohesion that only partially measure code quality.
Line 655: Of course, designing experiments to measure the benefits of a software engineering
Line 656: 
Line 657: --- 페이지 239 ---
Line 658: 211
Line 659: TDD in the real world
Line 660: practice is challenging, and the academic community is still trying to find the best way
Line 661: to do it.
Line 662:  More recent papers explore the idea that TDD’s effects may be due not to the
Line 663: “write the tests first” aspect but rather to taking baby steps toward the final goal. Fucci
Line 664: et al. (2016) argue that “the claimed benefits of TDD may not be due to its distinctive
Line 665: test-first dynamic, but rather due to the fact that TDD-like processes encourage fine-
Line 666: grained, steady steps that improve focus and flow.”
Line 667:  I suggest that you give TDD a chance. See if it fits your way of working and your
Line 668: programming style. You may decide to adopt it full-time (like many of my colleagues)
Line 669: or only in a few situations (like me), or you may choose never to do it (also like many
Line 670: of my colleagues). It is up to you. 
Line 671: 8.3.5
Line 672: Other schools of TDD
Line 673: TDD does not tell you how to start or what tests to write. This flexibility gave rise to
Line 674: various different schools of TDD. If you are familiar with TDD, you may have heard
Line 675: of the London school of TDD, mockist vs. classicist TDD, and outside-in TDD. This
Line 676: section summarizes their differences and points you to other material if you want to
Line 677: learn more.
Line 678:  In the classicist school of TDD (or the Detroit school of TDD, or inside-out TDD), devel-
Line 679: opers start their TDD cycles with the different units that will compose the overall fea-
Line 680: ture. More often than not, classicist TDDers begin with the entities that hold the main
Line 681: business rules; they slowly work toward the outside of the feature and connect these
Line 682: entities to, say, controllers, UIs, and web services. In other words, classicists go from
Line 683: the inside (entities and business rules) to the outside (interface with the user).
Line 684:  Classicists also avoid mocks as much as possible. For example, when implementing a
Line 685: business rule that would require the interaction of two or more other classes, classicists
Line 686: would focus on testing the entire behavior at once (all the classes working together)
Line 687: without mocking dependencies or making sure to test the units in a fully isolated man-
Line 688: ner. Classicists argue that mocks reduce the effectiveness of the test suite and make test
Line 689: suites more fragile. This is the same negative argument we discussed in chapter 6.
Line 690:  The London school of TDD (or outside-in TDD, or mockist TDD), on the other hand,
Line 691: prefers to start from the outside (such as the UI or the controller that handles the web
Line 692: service) and then slowly work toward the units that will handle the functionality. To do
Line 693: so, they focus on how the different objects will collaborate. And for that to happen in
Line 694: an outside-in manner, these developers use mocks to explore how the collaboration
Line 695: will work. They favor testing isolated units.
Line 696:  Both schools of thought use the test code to learn more about the design of the
Line 697: code being developed. I like the way Test Double (2018) puts it: “In [the] Detroit
Line 698: school, if an object is hard to test, then it’s hard to use; in [the] London school, if a
Line 699: dependency is hard to mock, then it’s hard to use for the object that’ll be using it.”
Line 700:  My style is a mixture of both schools. I start from the inside, coding entities and
Line 701: business rules, and then slowly work to the outside, making the external layers call
Line 702: 
Line 703: --- 페이지 240 ---
Line 704: 212
Line 705: CHAPTER 8
Line 706: Test-driven development
Line 707: these entities. However, I favor unit testing as much as possible: I do not like the tests
Line 708: of unit A breaking due to a bug in unit B. I use mocks for that, and I follow all the
Line 709: practices discussed in chapter 6.
Line 710:  I suggest that you learn more about both schools. Both have good points, and com-
Line 711: bining them makes sense. I recommend Mancuso’s 2018 talk, which elaborates on the
Line 712: differences between the schools and how the approaches can be used. 
Line 713: 8.3.6
Line 714: TDD and proper testing
Line 715: Some studies show that TDD practitioners write more test cases than non-TDD practi-
Line 716: tioners. However, I do not believe that the test suites generated by TDD sessions are as
Line 717: good as the strong, systematic test suites we engineered in the previous chapters after
Line 718: applying different testing practices. The reasoning is simple: when doing TDD, we are
Line 719: not focused on testing. TDD is a tool to help us develop, not to help us test.
Line 720:  Let’s revisit figure 1.4 in chapter 1. As I mentioned earlier, TDD is part of “testing
Line 721: to guide development.” In other words, you should use TDD when you want your tests
Line 722: to guide you through the development process. When you are finished with your TDD
Line 723: sessions and the code looks good, it is time to begin the effective and systematic test-
Line 724: ing part of the process I describe: change your focus to testing, and apply specifica-
Line 725: tion-based testing, structural testing, and property-based testing.
Line 726:  Can you reuse the tests you created during TDD in the effective and systematic
Line 727: part of the process? Sure. Doing so becomes natural.
Line 728:  Combining TDD and effective testing makes even more sense when both are done
Line 729: in a timely manner. You do not want to TDD something and then wait a week before
Line 730: properly testing it. Can you mix short TDD cycles with short systematic and effective
Line 731: testing cycles? Yes! Once you master all the techniques, you will begin to combine
Line 732: them. The practices I discuss in this book are not meant to be followed linearly—they
Line 733: are tools that are always at your disposal. 
Line 734: Exercises
Line 735: 8.1
Line 736: This figure illustrates the test-driven development cycle. Fill in the numbered
Line 737: gaps in the figure.
Line 738: 8.2
Line 739: Which of the following is the least important reason to do TDD?
Line 740: (5)
Line 741: (3)
Line 742: (1)
Line 743: (2)
Line 744: (4)
Line 745: 
Line 746: --- 페이지 241 ---
Line 747: 213
Line 748: Exercises
Line 749: A TDD practitioners use the feedback from the test code as a design hint.
Line 750: B The practice of TDD enables developers to have steady, incremental prog-
Line 751: ress throughout the development of a feature.
Line 752: C As a consequence of the practice of TDD, software systems are tested
Line 753: completely.
Line 754: D Using mock objects helps developers understand the relationships between
Line 755: objects.
Line 756: 8.3
Line 757: TDD has become a popular practice among developers. According to them,
Line 758: TDD has several benefits. Which of the following statements is not considered a
Line 759: benefit of TDD? (This is from the perspective of developers, which may not
Line 760: always match the results of empirical research.)
Line 761: A Baby steps. Developers can take smaller steps whenever they feel it is
Line 762: necessary.
Line 763: B Better team integration. Writing tests is a social activity and makes the
Line 764: team more aware of their code quality.
Line 765: C Refactoring. The cycle prompts developers to improve their code constantly.
Line 766: D Design for testability. Developers are forced to write testable code from
Line 767: the beginning.
Line 768: 8.4
Line 769: It is time to practice TDD. A very common practice problem is calculating the
Line 770: final score of a bowling game.
Line 771: In bowling, a game consists of 10 rounds. In each round, each player has a
Line 772: frame. In a frame, the player can make two attempts to knock over 10 pins with
Line 773: the bowling ball. The score for each frame is the number of pins knocked
Line 774: down, with a bonus for a strike or a spare.
Line 775: A strike means the player knocks over all pins with one roll. In addition to 10
Line 776: points for knocking down all 10 pins, the player receives a bonus: the total num-
Line 777: ber of pins knocked over in the next frame. Here is an example: [X] [1 2]
Line 778: (each set of [ ] is one frame, and X indicates a strike). The player has accumu-
Line 779: lated a total of 16 points in these two frames. The first frame scores 10 + 3
Line 780: points (10 for the strike, and 3 for the sum of the next two rolls, 1 + 2), and the
Line 781: second frame scores 3 (the sum of the rolls).
Line 782: A spare means the player knocks down all pins in one frame, with two rolls. As
Line 783: a bonus, the points for the next roll are added to the score of the frame. For
Line 784: example, take [4 /] [3 2] (/ represents a spare). The player scores 13 points for
Line 785: the first frame (10 pins + 3 from the next roll), plus 5 for the second frame, for
Line 786: a total of 18 points.
Line 787: If a strike or a spare is achieved in the tenth (final) frame, the player makes
Line 788: an additional one (for a spare) or two (for a strike) rolls. However, the total
Line 789: rolls for this frame cannot exceed three (that is, rolling a strike with one of the
Line 790: extra rolls does not grant more rolls).
Line 791: 
Line 792: --- 페이지 242 ---
Line 793: 214
Line 794: CHAPTER 8
Line 795: Test-driven development
Line 796: Write a program that receives the results of the 10 frames and returns the
Line 797: game’s final score. Use the TDD cycle: write a test, make it pass, and repeat.
Line 798: Summary
Line 799: Writing a test that fails, making it pass, and then refactoring is what test-driven
Line 800: development is all about.
Line 801: The red-green-refactor cycle brings different advantages to the coding process,
Line 802: such as more control over the pace of development, and quick feedback.
Line 803: All the schools of TDD make sense, and all should be used depending on the
Line 804: current context.
Line 805: Empirical research does not find clear benefits from TDD. The current consen-
Line 806: sus is that working on small parts of a feature and making steady progress makes
Line 807: developers more productive. Therefore, while TDD is a matter of taste, using
Line 808: short implementation cycles and testing is the way to go.
Line 809: Deciding whether to use TDD 100% of the time is also a personal choice. You
Line 810: should determine when TDD makes you more productive.
Line 811: Baby steps are key to TDD. Do not be afraid to go slowly when you are in doubt
Line 812: about what to do next. And do not be afraid to go faster when you feel confident!