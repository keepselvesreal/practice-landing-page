Line 1: 
Line 2: --- 페이지 98 ---
Line 3: 6
Line 4: Following the Rhythms of TDD
Line 5: We’ve seen how individual unit tests help us explore and capture design decisions about our code and 
Line 6: keep our code defect-free and simple to use, but that’s not all they can do. TDD has rhythms that help 
Line 7: us with the whole development cycle. By following the rhythms, we have a guide on what to do next at 
Line 8: each step. It is helpful to have this technical structure that allows us to think deeply about engineering 
Line 9: good code and then capture the results.
Line 10: The first rhythm was covered in the last chapter. Inside each test, we have a rhythm of writing the 
Line 11: Arrange, Act, and Assert sections. We’ll add some detailed observations on succeeding with this next. 
Line 12: We’ll go on to cover the larger rhythm that guides us as we refine our code, known as the red, green, 
Line 13: refactor (RGR) cycle. Together, they help us craft our code to be easy to integrate into the broader 
Line 14: application and made of clean, simple-to-understand code. Applying these two rhythms ensures that 
Line 15: we deliver high-quality code at pace. It provides us with several small milestones to hit during each 
Line 16: coding session. This is highly motivating, as we gain a sense of steady progress toward our goal of 
Line 17: building our application.
Line 18: In this chapter, we’re going to cover the following topics:
Line 19: •	 Following the RGR cycle
Line 20: •	 Writing our next tests for Wordz
Line 21: Technical requirements
Line 22: The final code in this chapter can be found at https://github.com/PacktPublishing/
Line 23: Test-Driven-Development-with-Java/tree/main/chapter06. It is recommended 
Line 24: to follow along with the exercise by typing the code in yourself – and thinking about all the decisions 
Line 25: we will be making as we go.
Line 26: Following the RGR cycle
Line 27: We saw in the previous chapter how a single unit test is split into three parts, known as the Arrange, 
Line 28: Act, and Assert sections. This forms a simple rhythm of work that guides us through writing every 
Line 29: 
Line 30: --- 페이지 99 ---
Line 31: Following the Rhythms of TDD
Line 32: 76
Line 33: test. It forces us to design how our code is going to be used – the outside of our code. If we think of 
Line 34: an object as being an encapsulation boundary, it makes sense to talk about what is inside and outside 
Line 35: that boundary. The public methods form the outside of our object. The Arrange, Act and Assert 
Line 36: rhythm helps us design those.
Line 37: We’re using the word rhythm here in an almost musical sense. It’s a constant, repeating theme that 
Line 38: holds our work together. There is a regular flow of work in writing tests, writing code, improving that 
Line 39: code, and then deciding which test to write next. Every test and piece of code will be different, but the 
Line 40: rhythm of work is the same, as though it were a steady beat in an ever-changing song.
Line 41: Once we have written our test, we turn to creating the code that is inside our object – the private fields 
Line 42: and methods. For this, we make use of another rhythm called RGR. This is a three-step process that helps 
Line 43: us to build confidence in our test, create a basic implementation of our code, and then refine it safely.
Line 44: In this section, we will learn what work needs to be done in each of the three phases.
Line 45: Starting on red
Line 46: Figure 6.1 – The red phase
Line 47: We always start with the first phase called the red phase. The goal of this phase is to use the Arrange, 
Line 48: Act and Assert template to get our test up and running and ready to test the code we will write next. 
Line 49: The most important part of this phase is to make sure that the test does not pass. We call this a failing 
Line 50: test, or a red test, due to the color that most graphical test tools use to indicate a failing test.
Line 51: That’s rather counter-intuitive, isn’t it? We normally aim to make things work right the first time in 
Line 52: development. However, we want our test to fail at this stage to give us confidence that it is working 
Line 53: correctly. If the test passes at this point, it’s a concern. Why does it pass? We know that we have not 
Line 54: yet written any of the code we are testing. If the test passes now, that means we either do not need to 
Line 55: write any new code or we have made a mistake in the test. The Further reading section has a link to 
Line 56: eight reasons why a test might not be running correctly.
Line 57: The most common mistake here is getting the assertion wrong. Identify the error and fix it before 
Line 58: moving on. We must have that red test in place so that we can see it change from failing to passing 
Line 59: as we correctly add code.
Line 60: 
Line 61: --- 페이지 100 ---
Line 62: Following the RGR cycle
Line 63: 77
Line 64: Keep it simple – moving to green
Line 65: Figure 6.2 – The green phase
Line 66: Once we have our failing test, we are free to write the code that will make it pass. We call this the 
Line 67: production code – the code that will form part of our production system. We treat our production 
Line 68: code as a black-box component. Think of an integrated circuit in electronics, or perhaps some kind 
Line 69: of mechanical sealed unit. The component has an inside and an outside. The inside is where we write 
Line 70: our production code. It is where we hide the data and algorithms of our implementation. We can do 
Line 71: this using any approach we choose – object-oriented, functional, declarative, or procedural. Anything 
Line 72: we fancy. The outside is the Application Programming Interface (API). This is the part we use to 
Line 73: connect to our component and use it to build bigger pieces of software. If we choose an object-oriented 
Line 74: approach, this API will be made of public methods on an object. With TDD, the first piece we connect 
Line 75: to is our test, and that gives us fast feedback on how easy the connection is to use.
Line 76: The following diagram shows the different pieces – the inside, outside, test code, and other users of 
Line 77: our component:
Line 78: Figure 6.3 – The inside and outside a black-box component
Line 79: 
Line 80: --- 페이지 101 ---
Line 81: Following the Rhythms of TDD
Line 82: 78
Line 83: Because our implementation is encapsulated, we can change our minds about it later as we learn more 
Line 84: without breaking the test.
Line 85: There are two guidelines for this phase:
Line 86: •	 Use the simplest code that could possibly work: Using the simplest code is important. There 
Line 87: can be a temptation to use over-engineered algorithms, or perhaps use the latest language 
Line 88: feature just for an excuse to use it. Resist this temptation. At this stage, our goal is to get the 
Line 89: test to pass and nothing more.
Line 90: •	 Don’t overthink the implementation details: We don’t need to overthink this. We don’t need 
Line 91: to write the perfect code on our first attempt. We can write a single line, a method, several 
Line 92: methods, or entirely new classes. We will improve this code in the next step. Just remember 
Line 93: to make the test pass and not go beyond what this test is covering in terms of functionality.
Line 94: Refactoring to clean code
Line 95: Figure 6.4 – The refactor phase
Line 96: This is the phase where we go into software engineering mode. We have some working, simple code 
Line 97: with a test that passes. Now is the time to refine that into clean code – meaning code that will be 
Line 98: easy to read later. With the confidence that a passing test provides, we are free to apply any valid 
Line 99: refactoring technique to our code. Some examples of refactoring techniques we can use during this 
Line 100: phase include the following:
Line 101: •	 Extracting a method to remove duplicated code
Line 102: •	 Renaming a method to express what it does better
Line 103: •	 Renaming a variable to express what it contains better
Line 104: •	 Splitting a long method into several smaller ones
Line 105: •	 Extracting a smaller class
Line 106: •	 Combining a long parameter list into its own class
Line 107: 
Line 108: --- 페이지 102 ---
Line 109: Writing our next tests for Wordz
Line 110: 79
Line 111: All these techniques have one goal: to make our code easier to understand. This will make it easier 
Line 112: to maintain. Remember to keep that green test passing throughout these changes. By the end of this 
Line 113: phase, we will have a unit test covering a piece of production code that we have engineered to be easy 
Line 114: to work with in the future. That’s a good place to be.
Line 115: Now we’re familiar with what to do in each phase of the RGR cycle, let’s apply that to our Wordz application.
Line 116: Writing our next tests for Wordz
Line 117: So, what should we write for our next tests? What would be a useful and small-enough step so that we 
Line 118: do not fall into the trap of writing beyond what our tests can support? In this section, we will continue 
Line 119: building out the Wordz application scoring system using TDD. We will discuss how we choose to 
Line 120: move forward at each step.
Line 121: For the next test, a good choice is to play it safe and move only a small step further. We will add a test 
Line 122: for a single correct letter. This will drive out our first piece of genuine application logic:
Line 123: 1.	
Line 124: Let’s start on red. Write a failing test for a single, correct letter:
Line 125: @Test
Line 126: public void oneCorrectLetter() {
Line 127:    var word = new Word("A");
Line 128:    var score = word.guess("A");
Line 129:    assertThat(score.letter(0))
Line 130:       .isEqualTo(Letter.CORRECT);
Line 131: }
Line 132: This test is intentionally similar to the one before. The difference is that it tests for a letter 
Line 133: being correct, rather than being incorrect. We have used the same word – a single letter, "A" 
Line 134: – intentionally. This is important when writing tests – use test data that helps to tell the story 
Line 135: of what we are testing and why. The story here is that the same word with a different guess 
Line 136: will lead to a different score – obviously key to the problem we are solving. Our two test cases 
Line 137: completely cover both possible outcomes of any guess of a single-letter word.
Line 138: Using our IDE auto-completion features, we quickly arrive at changes to class Word.
Line 139: 2.	
Line 140: Now let’s move to green by adding the production code to make the test pass:
Line 141: public class Word {
Line 142:     private final String word;
Line 143:     public Word(String correctWord) {
Line 144: 
Line 145: --- 페이지 103 ---
Line 146: Following the Rhythms of TDD
Line 147: 80
Line 148:         this.word = correctWord;
Line 149:     }
Line 150:     public Score guess(String attempt) {
Line 151:         var score = new Score(word);
Line 152:         score.assess( 0, attempt );
Line 153:         return score;
Line 154:     }
Line 155: }
Line 156: The goal here is to get the new test to pass while keeping the existing test passing. We don’t 
Line 157: want to break any existing code. We’ve added a field called word, which will store the word 
Line 158: we are supposed to be guessing. We’ve added a public constructor to initialize this field. We 
Line 159: have added code into the guess() method to create a new Score object. We decide to add a 
Line 160: method to this Score class called assess(). This method has the responsibility of assessing 
Line 161: what our guess should score. We decide that assess() should have two parameters. The 
Line 162: first parameter is a zero-based index for which letter of the word we wish to assess a score. The 
Line 163: second parameter is our guess at what the word might be.
Line 164: We use the IDE to help us write class Score:
Line 165: public class Score {
Line 166:     private final String correct;
Line 167:     private Letter result = Letter.INCORRECT ;
Line 168:     public Score(String correct) {
Line 169:         this.correct = correct;
Line 170:     }
Line 171:     public Letter letter(int position) {
Line 172:         return result;
Line 173:     }
Line 174:     public void assess(int position, String attempt) {
Line 175:         if ( correct.charAt(position) == attempt.
Line 176:             charAt(position)){
Line 177:             result = Letter.CORRECT;
Line 178:         }
Line 179: 
Line 180: --- 페이지 104 ---
Line 181: Writing our next tests for Wordz
Line 182: 81
Line 183:     }
Line 184: }
Line 185: To cover the new behavior tested by the oneCorrectLetter() test, we add the preceding 
Line 186: code. Instead of the assess() method always returning Letter.INCORRECT as it did 
Line 187: previously, the new test has forced a new direction. The assess() method must now be able 
Line 188: to return the correct score when a guessed letter is correct.
Line 189: To achieve this, we added a field called result to hold the latest score, code to return that 
Line 190: result from the letter() method, and code into the assess() method to check whether 
Line 191: the first letter of our guess matches the first letter of our word. If we have got this right, both 
Line 192: of our tests should now pass.
Line 193: Run all the tests to see how we are doing:
Line 194: Figure 6.5 – Two tests passing
Line 195: There’s a lot to review here. Notice how both of our tests are passing. By running all the tests 
Line 196: so far, we have proven that we have not broken anything. The changes we made to our code 
Line 197: added the new feature and did not break any existing features. That’s powerful. Take note of 
Line 198: another obvious aspect – we know our code works. We do not have to wait until a manual test 
Line 199: phase, wait until some integration point, or wait until the user interface is ready. We know our 
Line 200: code works now. As a minor point, note the time duration of 0.103 seconds. The two tests were 
Line 201: completed in one-tenth of one second, much faster than testing this manually. Not bad at all.
Line 202: Design-wise, we have moved on. We have moved past the hard-coded Letter.INCORRECT 
Line 203: result with code that can detect both correct and incorrect guesses. We have added the important 
Line 204: design concept of an assess() method into class Score. This is significant. Our code 
Line 205: now reveals a design; the Score object will know the correct word and will be able to use the 
Line 206: assess() method against the guess, attempt. The terminology used here forms a good 
Line 207: description of the problem we are solving. We want to assess a guess to return a word score.
Line 208: Now that the test passes, we can move on – but an important part of TDD is continuously 
Line 209: improving our code and working toward a better design, guided by tests. We now enter the 
Line 210: refactor phase of the RGR cycle. Once again, TDD hands control back to us. Do we want to 
Line 211: refactor? What things should we refactor? Why? Is it worth doing this right now or can we 
Line 212: defer this until a later step?
Line 213: 
Line 214: --- 페이지 105 ---
Line 215: Following the Rhythms of TDD
Line 216: 82
Line 217: Let’s review the code and look for code smells. A code smell is an indication that the implementation 
Line 218: may need improving. The name comes from the idea of the smell that food has once it starts 
Line 219: to go off.
Line 220: One code smell is duplicated code. Alone, a little duplicated code might be okay. But it is an 
Line 221: early warning that perhaps too much copy-and-paste has been used, and that we have failed 
Line 222: to capture an important concept more directly. Let’s review our code to eliminate duplication. 
Line 223: We can also look for two other common code smells – unclear naming, and blocks of code 
Line 224: that would be easier to read if they were extracted out into their own method. Obviously, this 
Line 225: is subjective, and we will all have different views on what to change.
Line 226: Defining code smells
Line 227: The term code smell originally appeared on the C2 wiki. It’s worth a read to see the given 
Line 228: examples of code smells. It has a helpful definition that notes a code smell is something that 
Line 229: needs review but may not necessarily need to be changed: 
Line 230: https://wiki.c2.com/?CodeSmell.
Line 231: Let’s reflect on the inside of the assess() method. It just seems cluttered with too much 
Line 232: code. Let’s extract a helper method to add some clarity. We can always revert the change if we 
Line 233: feel it doesn’t help.
Line 234: 3.	
Line 235: Let’s refactor. Extract an isCorrectLetter() method for clarity:
Line 236: public void assess(int position, String attempt) {
Line 237:     if (isCorrectLetter(position, attempt)){
Line 238:         result = Letter.CORRECT;
Line 239:     }
Line 240: }
Line 241: private boolean isCorrectLetter(int position,
Line 242:                                 String attempt) {
Line 243:     return correct.charAt(position) ==
Line 244:            attempt.charAt(position);
Line 245: }
Line 246: Once more, we run all the tests to prove this refactoring has not broken anything. The tests 
Line 247: pass. In the preceding code, we have split out a complex conditional statement into its own 
Line 248: private method. The motivation was to get a method name into the code. This is an effective 
Line 249: way of commenting on our code – in a way that the compiler helps us keep up to date. It helps 
Line 250: the calling code in the assess() method tell a better story. The if statement now says “if 
Line 251: this is a correct letter” more or less in English. That is a powerful aid to readability.
Line 252: 
Line 253: --- 페이지 106 ---
Line 254: Writing our next tests for Wordz
Line 255: 83
Line 256: Readability happens during writing not reading
Line 257: A common question from coding beginners is “How can I improve my ability to read code?”
Line 258: This is a valid question, as any line of code will be read by human programmers many more 
Line 259: times than it was written. Readability is won or lost when you write the code. Any line of code 
Line 260: can be written either to be easy to read or hard to read. We get to choose as writers. If we 
Line 261: consistently choose ease of reading over anything else, others will find our code easy to read.
Line 262: Badly written code is hard to read. Sadly, it is easy to write.
Line 263: There are two more areas I want to refactor at this stage. The first is a simple method to improve 
Line 264: test readability.
Line 265: Let’s refactor the test code to improve its clarity. We will add a custom assert method:
Line 266: @Test
Line 267: public void oneCorrectLetter() {
Line 268:     var word = new Word("A");
Line 269:     var score = word.guess("A");
Line 270:     assertScoreForLetter(score, 0, Letter.CORRECT);
Line 271: }
Line 272: private void assertScoreForLetter(Score score,
Line 273:                   int position, Letter expected) {
Line 274:     assertThat(score.letter(position))
Line 275:           .isEqualTo(expected);
Line 276: }
Line 277: The preceding code has taken the assertThat() assertion and moved it into its own private 
Line 278: method. We have called this method assertScoreForLetter() and given it a signature 
Line 279: that describes what information is needed. This change provides a more direct description of 
Line 280: what the test is doing while reducing some duplicated code. It also protects us against changes 
Line 281: in the implementation of the assertion. This seems to be a step toward a more comprehensive 
Line 282: assertion, which we will need once we support guesses with more letters. Once again, instead 
Line 283: of adding a comment to the source code, we have used a method name to capture the intent 
Line 284: of the assertThat() code. Writing AssertJ custom matchers are another way of doing this.
Line 285: The next refactoring we may want to do is a little more controversial, as it is a design change. 
Line 286: Let’s do the refactoring, discuss it, then possibly revert the code if we don’t like it. That will save 
Line 287: hours of wondering about what the change would look like.
Line 288: 
Line 289: --- 페이지 107 ---
Line 290: Following the Rhythms of TDD
Line 291: 84
Line 292: 4.	
Line 293: Let’s change how we specify the letter position to check in the assess() method:
Line 294: public class Score {
Line 295:     private final String correct;
Line 296:     private Letter result = Letter.INCORRECT ;
Line 297:     private int position;
Line 298:     public Score(String correct) {
Line 299:         this.correct = correct;
Line 300:     }
Line 301:     public Letter letter(int position) {
Line 302:         return result;
Line 303:     }
Line 304:     public void assess(String attempt) {
Line 305:         if (isCorrectLetter(attempt)){
Line 306:             result = Letter.CORRECT;
Line 307:         }
Line 308:     }
Line 309:     private boolean isCorrectLetter(String attempt) {
Line 310:         return correct.charAt(position) == attempt.
Line 311:         charAt(position);
Line 312:     }
Line 313: }
Line 314: We’ve removed the position parameter from the assess() method and converted it into 
Line 315: a field called position. The intention is to simplify the usage of the assess() method. It 
Line 316: no longer needs to explicitly state which position is being assessed. That makes the code easier 
Line 317: to call. The code we have just added will only work in the case where the position is zero. This 
Line 318: is fine, as this is the only thing required by our tests at this stage. We will make this code work 
Line 319: for non-zero values later.
Line 320: The reason this is a controversial change is that it requires us to change the test code to reflect 
Line 321: that change in the method signature. I am prepared to accept this, knowing that I can use my 
Line 322: IDE-automated refactoring support to do this safely. It also introduces a risk: we must ensure 
Line 323: that position is set to the correct value before we call isCorrectLetter(). We’ll see 
Line 324: how this develops. This may make the code more difficult to understand, in which case the 
Line 325: simplified assess() method probably will not be worth it. We can change our approach if 
Line 326: we find this to be the case.
Line 327: 
Line 328: --- 페이지 108 ---
Line 329: Writing our next tests for Wordz
Line 330: 85
Line 331: We are now at a point where the code is complete for any single-letter word. What should we 
Line 332: attempt next? It seems as though we should move on to two-letter words and see how that 
Line 333: changes our tests and logic.
Line 334: Advancing the design with two-letter combinations
Line 335: We can proceed to add tests aimed at getting the code to handle two-letter combinations. This is an 
Line 336: obvious step to take after getting the code to work with a single letter. To do this, we will need to 
Line 337: introduce a new concept into the code: a letter can be present in the word, but not in the position we 
Line 338: guessed it to be:
Line 339: 1.	
Line 340: Let’s begin by writing a test for a second letter that is in the wrong position:
Line 341: @Test
Line 342: void secondLetterWrongPosition() {
Line 343:     var word = new Word("AR");
Line 344:     var score = word.guess("ZA");
Line 345:     assertScoreForLetter(score, 1,
Line 346:                          Letter.PART_CORRECT);
Line 347: }
Line 348: Let’s change the code inside the assess() method to make this pass and keep the existing 
Line 349: tests passing.
Line 350: 2.	
Line 351: Let’s add initial code to check all the letters in our guess:
Line 352: public void assess(String attempt) {
Line 353:     for (char current: attempt.toCharArray()) {
Line 354:         if (isCorrectLetter(current)) {
Line 355:             result = Letter.CORRECT;
Line 356:         }
Line 357:     }
Line 358: }
Line 359: private boolean isCorrectLetter(char currentLetter) {
Line 360:     return correct.charAt(position) == currentLetter;
Line 361: }
Line 362: The main change here is to assess all of the letters in attempt and not assume it only has one 
Line 363: letter in it. That, of course, was the purpose of this test – to drive out this behavior. By choosing 
Line 364: to convert the attempt string into an array of char, the code seems to read quite well. This 
Line 365: simple algorithm iterates over each char, using the current variable to represent the current 
Line 366: 
Line 367: --- 페이지 109 ---
Line 368: Following the Rhythms of TDD
Line 369: 86
Line 370: letter to be assessed. This requires the isCorrectLetter() method to be refactored for it 
Line 371: to accept and work with the char input – well, either that or converting char to a String, 
Line 372: and that looks ugly.
Line 373: The original tests for single-letter behaviors still pass, as they must. We know the logic inside 
Line 374: our loop cannot possibly be correct – we are simply overwriting the result field, which can 
Line 375: only store a result for one letter at most. We need to improve that logic, but we won’t do that 
Line 376: until we have added a test for that. Working this way is known as triangulation – we make the 
Line 377: code more general-purpose as we add more specific tests. For our next step, we will add code 
Line 378: to detect when our attempted letter occurs in the word in some other position.
Line 379: 3.	
Line 380: Let’s add code to detect when a correct letter is in the wrong position:
Line 381: public void assess(String attempt) {
Line 382:     for (char current: attempt.toCharArray()) {
Line 383:         if (isCorrectLetter(current)) {
Line 384:             result = Letter.CORRECT;
Line 385:         } else if (occursInWord(current)) {
Line 386:             result = Letter.PART_CORRECT;
Line 387:         }
Line 388:     }
Line 389: }
Line 390:     private boolean occursInWord(char current) {
Line 391:         return
Line 392:           correct.contains(String.valueOf(current));
Line 393:     }
Line 394: We’ve added a call to a new private method, occursInWord(), which will return true if 
Line 395: the current letter occurs anywhere in the word. We have already established that this current 
Line 396: letter is not in the right place. This should give us a clear result for a correct letter not in the 
Line 397: correct position.
Line 398: This code makes all three tests pass. Immediately, this is suspicious, as it shouldn’t happen. 
Line 399: We already know that our logic overwrites the single result field and this means that many 
Line 400: combinations will fail. What has happened is that our latest test is fairly weak. We could go 
Line 401: back and strengthen that test, by adding an extra assertion. Alternatively, we can leave it as 
Line 402: it is and write another test. Dilemmas such as this are common in development and it’s not 
Line 403: usually worth spending too much time thinking about them. Either way will move us forward.
Line 404: Let’s add another test to completely exercise the behavior around the second letter being in 
Line 405: the wrong position.
Line 406: 
Line 407: --- 페이지 110 ---
Line 408: Writing our next tests for Wordz
Line 409: 87
Line 410: 4.	
Line 411: Add a new test exercising all three scoring possibilities:
Line 412: @Test
Line 413: void allScoreCombinations() {
Line 414:     var word = new Word("ARI");
Line 415:     var score = word.guess("ZAI");
Line 416:     assertScoreForLetter(score, 0, Letter.INCORRECT);
Line 417:     assertScoreForLetter(score, 1,
Line 418:                          Letter.PART_CORRECT);
Line 419:     assertScoreForLetter(score, 2, Letter.CORRECT);
Line 420: }
Line 421: As expected, this test fails. The reason is obvious upon inspecting the production code. It’s 
Line 422: because we were storing results in the same single-valued field. Now that we have a failing test 
Line 423: for that, we can correct the scoring logic.
Line 424: 5.	
Line 425: Add a List of results to store the result for each letter position separately:
Line 426: public class Score {
Line 427:     private final String correct;
Line 428:     private final List<Letter> results =
Line 429:                              new ArrayList<>();
Line 430:     private int position;
Line 431:     public Score(String correct) {
Line 432:         this.correct = correct;
Line 433:     }
Line 434:     public Letter letter(int position) {
Line 435:         return results.get(position);
Line 436:     }
Line 437:     public void assess(String attempt) {
Line 438:         for (char current: attempt.toCharArray()) {
Line 439:             if (isCorrectLetter(current)) {
Line 440:                 results.add(Letter.CORRECT);
Line 441:             } else if (occursInWord(current)) {
Line 442:                 results.add(Letter.PART_CORRECT);
Line 443:             } else {
Line 444: 
Line 445: --- 페이지 111 ---
Line 446: Following the Rhythms of TDD
Line 447: 88
Line 448:                 results.add(Letter.INCORRECT);
Line 449:             }
Line 450:             position++;
Line 451:         }
Line 452:     }
Line 453:     private boolean occursInWord(char current) {
Line 454:         return
Line 455:          correct.contains(String.valueOf(current));
Line 456:     }
Line 457:     private boolean isCorrectLetter(char
Line 458:       currentLetter) {
Line 459:         return correct.charAt(position) ==
Line 460:                  currentLetter;
Line 461:     }
Line 462: }
Line 463: This took a couple of attempts to get right, driven by failures in the test we just added. The 
Line 464: preceding end result passes all four tests, proving it can correctly score all combinations in 
Line 465: a three-letter word. The main change was to replace the single-valued result field with an 
Line 466: ArrayList of results and change the letter(position) implementation method 
Line 467: to use this new collection of results. Running that change caused a failure, as the code could 
Line 468: no longer detect an incorrect letter. Previously, that had been handled by the default value of 
Line 469: the result field. Now, we must do that explicitly for each letter. We then need to update the 
Line 470: position within the loop to track which letter position we are assessing.
Line 471: We’ve added a test, watched it go red and fail, then added code to make the test go green and 
Line 472: pass, so now it is time to refactor. There are things about both the test and the production code 
Line 473: that don’t seem quite right.
Line 474: In the production code class Score, it is the loop body of the assess() method that 
Line 475: seems unwieldy. It has a long loop body with logic in it and a set of if-else-if blocks. It 
Line 476: feels as though the code could be made clearer. We can extract the loop body into a method. 
Line 477: The method name then gives us a place to describe what is happening to each thing. The loop 
Line 478: then becomes shorter and simpler to grasp. We can also replace the if-else-if ladders with 
Line 479: a simpler construct.
Line 480: 
Line 481: --- 페이지 112 ---
Line 482: Writing our next tests for Wordz
Line 483: 89
Line 484: 6.	
Line 485: Let’s extract the logic inside the loop body into a scoreFor() method:
Line 486: public void assess(String attempt) {
Line 487:     for (char current: attempt.toCharArray()) {
Line 488:         results.add( scoreFor(current) );
Line 489:         position++;
Line 490:     }
Line 491: }
Line 492: private Letter scoreFor(char current) {
Line 493:     if (isCorrectLetter(current)) {
Line 494:         return Letter.CORRECT;
Line 495:     }
Line 496:     if (occursInWord(current)) {
Line 497:         return Letter.PART_CORRECT;
Line 498:     }
Line 499:     return Letter.INCORRECT;
Line 500: }
Line 501: This reads far more clearly. The body of the scoreFor() method is now a concise description 
Line 502: of the rules for scoring each letter. We replaced the if-else-if construction with a simpler 
Line 503: if-return construction. We work out what the score is, then exit the method immediately.
Line 504: The next job is to clean up the test code. In TDD, test code is given equal priority to production 
Line 505: code. It forms part of the documentation about the system. It needs to be maintained and 
Line 506: extended alongside the production code. We treat test code readability with the same importance 
Line 507: as production code.
Line 508: The code smell with the test code is around the asserts. Two things could be improved. There 
Line 509: is an obvious duplication in the code that we could eliminate. There is also a question about 
Line 510: how many assertions should be made in one test.
Line 511: 7.	
Line 512: Let’s remove the duplicated assertion code by extracting a method:
Line 513: @Test
Line 514: void allScoreCombinations() {
Line 515:     var word = new Word("ARI");
Line 516:     var score = word.guess("ZAI");
Line 517:     assertScoreForGuess(score, INCORRECT,
Line 518: 
Line 519: --- 페이지 113 ---
Line 520: Following the Rhythms of TDD
Line 521: 90
Line 522:                                PART_CORRECT,
Line 523:                                CORRECT);
Line 524: }
Line 525: private void assertScoreForGuess(Score score, Letter…
Line 526:     for (int position=0;
Line 527:              position < expectedScores.length;
Line 528:              position++){
Line 529:         Letter expected = expectedScores[position];
Line 530:         assertThat(score.letter(position))
Line 531:             .isEqualTo(expected);
Line 532:     }
Line 533: }
Line 534: By extracting the assertScoreForGuess() method, we create a way to check the scores 
Line 535: for a variable number of letters. This eliminates those copy-pasted assert lines that we had 
Line 536: and raises the level of abstraction. The test code reads more clearly as we now describe tests in 
Line 537: terms of the order of INCORRECT, PART_CORRECT, CORRECT that we expect the score 
Line 538: to be in. By adding a static import to those enums, syntax clutter is also beneficially reduced.
Line 539: The earlier tests can now be manually modified to make use of this new assertion helper. This 
Line 540: allows us to inline the original assertScoreForLetter() method, as it no longer adds value.
Line 541: 8.	
Line 542: Now, let’s take a look at the final set of tests following our refactoring:
Line 543: package com.wordz.domain;
Line 544: import org.junit.jupiter.api.Test;
Line 545: import static com.wordz.domain.Letter.*;
Line 546: import static org.assertj.core.api.Assertions.assertThat;
Line 547: public class WordTest {
Line 548:     @Test
Line 549:     public void oneIncorrectLetter() {
Line 550:         var word = new Word("A");
Line 551:         var score = word.guess("Z");
Line 552:         assertScoreForGuess(score, INCORRECT);
Line 553:     }
Line 554:     @Test
Line 555: 
Line 556: --- 페이지 114 ---
Line 557: Writing our next tests for Wordz
Line 558: 91
Line 559:     public void oneCorrectLetter() {
Line 560:         var word = new Word("A");
Line 561:         var score = word.guess("A");
Line 562:         assertScoreForGuess(score, CORRECT);
Line 563:     }
Line 564:     @Test
Line 565:     public void secondLetterWrongPosition() {
Line 566:         var word = new Word("AR");
Line 567:         var score = word.guess("ZA");
Line 568:         assertScoreForGuess(score,  INCORRECT,
Line 569:                                     PART_CORRECT);
Line 570:     }
Line 571:     @Test
Line 572:     public void allScoreCombinations() {
Line 573:         var word = new Word("ARI");
Line 574:         var score = word.guess("ZAI");
Line 575:         assertScoreForGuess(score,  INCORRECT,
Line 576:                                     PART_CORRECT,
Line 577:                                     CORRECT);
Line 578:     }
Line 579:     private void assertScoreForGuess(Score score,
Line 580:         Letter... expectedScores) {
Line 581:         for (int position = 0;
Line 582:               position < expectedScores.length;
Line 583:               position++) {
Line 584:             Letter expected =
Line 585:                     expectedScores[position];
Line 586:             assertThat(score.letter(position))
Line 587:                     .isEqualTo(expected);
Line 588:         }
Line 589:     }
Line 590: }
Line 591: 
Line 592: --- 페이지 115 ---
Line 593: Following the Rhythms of TDD
Line 594: 92
Line 595: This appears to be a comprehensive set of test cases. Every line of production code has been 
Line 596: driven out as a direct result of adding a new test to explore a new aspect of behavior. The test 
Line 597: code seems easy to read and the production code also seems clearly implemented and simple 
Line 598: to call. The test forms an executable specification of the rules for scoring a guess at a word.
Line 599: That’s achieved everything we set out to at the start of this coding session. We have grown the 
Line 600: capability of our Score class using TDD. We have followed the RGR cycle to keep both our 
Line 601: test code and production code following good engineering practices. We have robust code, 
Line 602: validated by unit tests, and a design that makes this code easy to call from our wider application.
Line 603: Summary
Line 604: In this chapter, we have applied the RGR cycle to our code. We’ve seen how this splits the work into 
Line 605: separate tasks, which results in confidence in our test, a rapid path to simple production code, and 
Line 606: less time spent to improve the maintainability of our code. We’ve looked at removing code smells 
Line 607: from both the production code and the test code. As part of our work in this chapter, we’ve used ideas 
Line 608: that help us move ahead and decide what tests we should write next. The techniques in this chapter 
Line 609: enable us to write multiple tests and incrementally drive out the detailed logic in our production code.
Line 610: In the next chapter, we’re going to learn about some object-oriented design ideas known as the SOLID 
Line 611: principles, enabling us to use TDD to grow our application still further.
Line 612: Questions and answers
Line 613: 1.	
Line 614: What are the two key rhythms of TDD?
Line 615: Arrange, Act, Assert, and RGR. The first rhythm helps us write the body of the test while 
Line 616: designing the interface to our production code. The second rhythm works to help us create 
Line 617: and then refine the implementation of that production code.
Line 618: 2.	
Line 619: How can we write tests before code?
Line 620: Instead of thinking about how we are going to implement some code, we think about how we 
Line 621: are going to call that code. We capture those design decisions inside a unit test.
Line 622: 3.	
Line 623: Should tests be throwaway code?
Line 624: No. In TDD, unit tests are given equal weight to the production code. They are written with 
Line 625: the same care and are stored in the same code repository. The only difference is that the test 
Line 626: code itself will not be present in the delivered executable.
Line 627: 4.	
Line 628: Do we need to refactor after every test pass?
Line 629: No. Use this time as an opportunity to decide what refactoring is needed. This applies to both 
Line 630: the production code and the test code. Sometimes, none is needed and we move on. Other 
Line 631: times, we sense that a larger change would be beneficial. We might choose to defer that larger 
Line 632: change until later once we have more code in place.
Line 633: 
Line 634: --- 페이지 116 ---
Line 635: Further reading
Line 636: 93
Line 637: Further reading
Line 638: •	 Getting Green on Red
Line 639: An article by Jeff Langr describing eight different ways a test can pass for the wrong reasons. 
Line 640: If we’re aware of these issues, we can avoid them as we work.
Line 641: https://medium.com/pragmatic-programmers/3-5-getting-green-on-
Line 642: red-d189240b1c87
Line 643: •	 Refactoring: Improving the design of existing code, Martin Fowler (ISBN 978-0134757599)
Line 644: The definitive guide to refactoring code. The book describes step-by-step transformations of 
Line 645: code that preserve its behavior but improve clarity. Interestingly, most transformations come in 
Line 646: pairs, such as the pair of techniques known as Extract Method and Inline Method. This reflects 
Line 647: the trade-offs involved.
Line 648: •	 AssertJ documentation for custom matchers
Line 649: This chapter briefly mentioned AssertJ custom matchers. These are very useful ways of creating 
Line 650: reusable customized assertions for your code. These assertion classes are themselves unit-testable 
Line 651: and can be written using test-first TDD. For that reason alone, they are superior to adding a 
Line 652: private method to handle a customized assertion.
Line 653: The following link provides many examples provided by the AssertJ distribution on github.
Line 654: https://github.com/assertj/assertj-examples/tree/main/assertions-
Line 655: examples/src/test/java/org/assertj/examples/custom
Line 656: 
Line 657: --- 페이지 117 ---