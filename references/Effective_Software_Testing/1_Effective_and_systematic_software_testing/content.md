Line 1: 
Line 2: --- 페이지 29 ---
Line 3: 1
Line 4: Effective and systematic
Line 5: software testing
Line 6: The developer community no longer needs to argue about the importance of soft-
Line 7: ware testing. Every software developer understands that software failures may cause
Line 8: severe damage to businesses, people, or even society as a whole. And although soft-
Line 9: ware developers once were primarily responsible for building software systems,
Line 10: today they are also responsible for the quality of the software systems they produce.
Line 11:  Our community has produced several world-class tools to help developers test,
Line 12: including JUnit, AssertJ, Selenium, and jqwik. We have learned to use the process
Line 13: of writing tests to reflect on what programs need to do and get feedback about the
Line 14: code design (or class design, if you are using an object-oriented language). We
Line 15: have also learned that writing test code is challenging, and paying attention to test
Line 16: code quality is fundamental for the graceful evolution of the test suite. And finally,
Line 17: we know what the common bugs are and how to look for them.
Line 18: This chapter covers
Line 19: Understanding the importance of effective, 
Line 20: systematic testing
Line 21: Recognizing why testing software is difficult 
Line 22: and why bug-free systems do not exist
Line 23: Introducing the testing pyramid
Line 24: 
Line 25: --- 페이지 30 ---
Line 26: 2
Line 27: CHAPTER 1
Line 28: Effective and systematic software testing
Line 29:  But while developers have become very good at using testing tools, they rarely
Line 30: apply systematic testing techniques to explore and find bugs. Many practitioners
Line 31: argue that tests are a feedback tool and should be used mostly to help you develop.
Line 32: Although this is true (and I will show throughout this book how to listen to your test
Line 33: code), tests can also help you find bugs. After all, that is what software testing is all
Line 34: about: finding bugs!
Line 35:  Most developers do not enjoy writing tests. I have heard many reasons: writing
Line 36: production code is more fun and challenging, software testing is too time-consuming,
Line 37: we are paid to write production code, and so on. Developers also overestimate how
Line 38: much time they spend on testing, as Beller and colleagues found in a nice empirical
Line 39: study with hundreds of developers in 2019. My goal with this book is to convince you
Line 40: that (1) as a developer, it is your responsibility to ensure the quality of what you pro-
Line 41: duce; (2) that tests are the only tools to help you with that responsibility; and (3)
Line 42: that if you follow a collection of techniques, you can test your code in an effective
Line 43: and systematic way.
Line 44:  Note the words I used: effective and systematic. Soon you will understand what I
Line 45: mean. But first, let me convince you of the necessity of tests.
Line 46: 1.1
Line 47: Developers who test vs. developers who do not
Line 48: It is late on Friday afternoon, and John is about to implement the last feature of the
Line 49: sprint. He is developing an agile software management system, and this final feature
Line 50: supports developers during planning poker.
Line 51: John is about to implement the feature’s core method. This method receives a list of
Line 52: estimates and produces, as output, the names of the two developers who should
Line 53: explain their points of view. This is what he plans to do:
Line 54:  
Line 55: Planning poker
Line 56: Planning poker is a popular agile estimation technique. In a planning poker session,
Line 57: developers estimate the effort required to build a specific feature of the backlog.
Line 58: After the team discusses the feature, each developer gives an estimate: a number
Line 59: ranging from one to any number the team defines. Higher numbers mean more effort
Line 60: to implement the feature. For example, a developer who estimates that a feature is
Line 61: worth eight points expects it to take four times more effort than a developer who esti-
Line 62: mates the feature to be worth two points.
Line 63: The developer with the smallest estimate and the developer with the highest esti-
Line 64: mate explain their points of view to the other members of the team. After more dis-
Line 65: cussion, the planning poker repeats until the team members agree about how much
Line 66: effort the feature will take. You can read more about the planning poker technique in
Line 67: Kanban in Action by Marcus Hammarberg and Joakim Sundén (2014).
Line 68: 
Line 69: --- 페이지 31 ---
Line 70: 3
Line 71: Developers who test vs. developers who do not
Line 72: Method: identifyExtremes
Line 73: The method should receive a list of developers and their respective estimates
Line 74: and return the two developers with the most extreme estimates.
Line 75: Input: A list of Estimates, each containing the name of the developer and
Line 76: their estimate 
Line 77: Output: A list of Strings containing the name of the developer with the lowest
Line 78: estimate and the name of the developer with the highest estimate
Line 79: After a few minutes, John ends up with the code in the following listing.
Line 80: public class PlanningPoker {
Line 81:   public List<String> identifyExtremes(List<Estimate> estimates) {
Line 82:     Estimate lowestEstimate = null;   
Line 83:     Estimate highestEstimate = null;  
Line 84:     for(Estimate estimate: estimates) {
Line 85:       if(highestEstimate == null ||
Line 86:        estimate.getEstimate() > highestEstimate.getEstimate()) {   
Line 87:         highestEstimate = estimate;
Line 88:       }
Line 89:       else if(lowestEstimate == null ||
Line 90:        estimate.getEstimate() < lowestEstimate.getEstimate()) {     
Line 91:         lowestEstimate = estimate;
Line 92:       }
Line 93:     }
Line 94:     return Arrays.asList(         
Line 95:         lowestEstimate.getDeveloper(),
Line 96:         highestEstimate.getDeveloper()
Line 97:     );
Line 98:   }
Line 99: }
Line 100: The logic is straightforward: the algorithm loops through all the developers in the list
Line 101: and keeps track of the highest and lowest estimates. It returns the names of the develop-
Line 102: ers with the lowest and highest estimates. Both lowestEstimate and highestEstimate
Line 103: are initialized with null and later replaced by the first estimate within the for loop.
Line 104: Listing 1.1
Line 105: The first PlanningPoker implementation
Line 106: Generalizing from the code examples
Line 107: Experienced developers may question some of my coding decisions. Maybe this
Line 108: Estimate class is not the best way to represent developers and their estimates.
Line 109: Maybe the logic to find the smallest and highest estimates is not the best. Maybe
Line 110: Defines placeholder variables for 
Line 111: the lowest and highest estimates
Line 112: If the current estimate is higher than the
Line 113: highest estimate seen so far, we replace the
Line 114: previous highest estimate with the current one.
Line 115: If the current estimate is lower than the
Line 116: lowest estimate seen so far, we replace the
Line 117: previous lowest estimate with the current one.
Line 118: Returns the developers 
Line 119: with the lowest and the 
Line 120: highest estimates
Line 121: 
Line 122: --- 페이지 32 ---
Line 123: 4
Line 124: CHAPTER 1
Line 125: Effective and systematic software testing
Line 126: John is not a fan of (automated) software testing. As is commonly done by developers
Line 127: who do not automate their tests, John runs the finished application and tries a few
Line 128: inputs. You can see one of these trials in figure 1.1. John sees that given the input in
Line 129: the figure (the estimates of Ted, Barney, Lily, and Robin), the program produces the
Line 130: correct output.
Line 131: John is happy with the results: his implementation worked from the beginning. He
Line 132: pushes his code, and the new feature is deployed automatically to customers. John
Line 133: goes home, ready for the weekend—but not even an hour later, the help desk starts to
Line 134: get e-mails from furious customers. The software is producing incorrect outputs!
Line 135:  John goes back to work, looks at the logs, and quickly identifies a case where the
Line 136: code fails. Can you find the input that makes the program crash? As illustrated in fig-
Line 137: ure 1.2, if the developers’ estimates are (by chance) in ascending order, the program
Line 138: throws a null pointer exception.
Line 139: (continued)
Line 140: the if statements could be simpler. I agree. But my focus in this book is not object-
Line 141: oriented design or the best ways to write code: rather, I want to focus on how to test
Line 142: the code once it’s written.
Line 143: The techniques I show you throughout this book will work regardless of how you imple-
Line 144: ment your code. So, bear with me when you see a piece of code that you think you
Line 145: could do better. Try to generalize from my examples to your own code. In terms of
Line 146: complexity, I am sure you have encountered code like that in listing 1.1.
Line 147: Calculate
Line 148: Lily and Ted
Line 149: should
Line 150: u
Line 151: speak
Line 152: p!
Line 153: Ted
Line 154: Barn y
Line 155: e
Line 156: Lily
Line 157: Robin
Line 158: 16
Line 159: 8
Line 160: 2
Line 161: 4
Line 162: Figure 1.1
Line 163: John does some manual 
Line 164: testing before releasing the application.
Line 165: Ross
Line 166: Phoebe
Line 167: Monica
Line 168: Chandler
Line 169: 2
Line 170: 4
Line 171: 8
Line 172: 16
Line 173: Calculate
Line 174: NullPointer
Line 175: exception
Line 176: Figure 1.2
Line 177: John finds a case where 
Line 178: his implementation crashes.
Line 179: 
Line 180: --- 페이지 33 ---
Line 181: 5
Line 182: Developers who test vs. developers who do not
Line 183: It does not take John long to find the bug in his code: the extra else in listing 1.1. In
Line 184: the case of ascending estimates, that innocent else causes the program to never
Line 185: replace the lowestEstimate variable with the lowest estimate in the list, because the
Line 186: previous if is always evaluated to true.
Line 187:  John changes the else if to an if, as shown in listing 1.2. He then runs the pro-
Line 188: gram and tries it with the same inputs. Everything seems to work. The software is
Line 189: deployed again, and John returns home, finally ready to start the weekend.
Line 190: if(highestEstimate == null ||
Line 191:     estimate.getEstimate() > highestEstimate.getEstimate()) {
Line 192:   highestEstimate = estimate;
Line 193: }
Line 194: if(lowestEstimate == null ||    
Line 195:     estimate.getEstimate() < lowestEstimate.getEstimate()) {
Line 196:   lowestEstimate = estimate;
Line 197: }
Line 198: You may be thinking, “This was a very easy bug to spot! I would never make such a mis-
Line 199: take!” That may be true. But in practice, it is hard to keep tabs on everything that may
Line 200: happen in our code. And, of course, it is even more difficult when the code is com-
Line 201: plex. Bugs happen not because we are bad programmers but because we program
Line 202: complicated things (and because computers are more precise than humans can be).
Line 203:  Let’s generalize from John’s case. John is a very good and experienced developer.
Line 204: But as a human, he makes mistakes. John performed some manual testing before releas-
Line 205: ing his code, but manual testing can only go so far, and it takes too long if we need to
Line 206: explore many cases. Also, John did not follow a systematic approach to testing—he just
Line 207: tried the first few inputs that came to mind. Ad hoc methods like “follow your instincts”
Line 208: may lead us to forget corner cases. John would greatly benefit from (1) a more systematic
Line 209: approach for deriving tests, to reduce the chances of forgetting a case; and (2) test auto-
Line 210: mation, so he does not have to spend time running tests manually.
Line 211:  Now, let’s replay the same story, but with Eleanor instead of John. Eleanor is also a
Line 212: very good and experienced software developer. She is highly skilled in software testing
Line 213: and only deploys once she has developed a strong test suite for all the code she
Line 214: writes.
Line 215:  Suppose Eleanor writes the same code as John (listing 1.1). She does not do test-
Line 216: driven development (TDD), but she does proper testing after writing her code.
Line 217: NOTE
Line 218: In a nutshell, TDD means writing the tests before the implementation.
Line 219: Not using TDD is not a problem, as we discuss in chapter 8.
Line 220: Eleanor thinks about what the identifyExtremes method does. Let’s say her reasoning
Line 221: is the same as John’s. She first focuses on the inputs of this method: a list of Estimates.
Line 222: She knows that whenever a method receives a list, there are several cases to try: a null
Line 223: Listing 1.2
Line 224: The bug fix in the PlanningPoker implementation
Line 225: We fixed the bug here 
Line 226: by replacing the “else 
Line 227: if” with an “if”.
Line 228: 
Line 229: --- 페이지 34 ---
Line 230: 6
Line 231: CHAPTER 1
Line 232: Effective and systematic software testing
Line 233: list, an empty list, a list with one element, and a list with multiple elements. How does
Line 234: she know that? She read this book!
Line 235:  Eleanor reflects on the first three cases (null, empty, single element), considering
Line 236: how this method will fit in with the rest of the system. The current implementation
Line 237: would crash in these cases! So, she decides the method should reject such inputs. She
Line 238: goes back to the production code and adds some validation code as follows.
Line 239: public List<String> identifyExtremes(List<Estimate> estimates) {
Line 240:   if(estimates == null) {   
Line 241:     throw new IllegalArgumentException("estimates cannot be null");
Line 242:   }
Line 243:   if(estimates.size() <= 1) {    
Line 244:     throw new IllegalArgumentException("there has to be more than 1
Line 245:     ➥ estimate in the list");
Line 246:   }
Line 247:   // continues here...
Line 248: }
Line 249: Although Eleanor is sure that the method now handles these invalid inputs correctly
Line 250: (it is clear in the code), she decides to write an automated test that formalizes the test
Line 251: case. This test will also prevent future regressions: later, if another developer does not
Line 252: understand why the assertions are in the code and removes them, the test will ensure
Line 253: that the mistake is noticed. The following listing shows the three test cases (note that,
Line 254: for now, I am making the tests verbose so they are easy to understand).
Line 255: public class PlanningPokerTest {
Line 256:   @Test
Line 257:   void rejectNullInput() {
Line 258:     assertThatThrownBy(     
Line 259:       () -> new PlanningPoker().identifyExtremes(null)
Line 260:     ).isInstanceOf(IllegalArgumentException.class);     
Line 261:   }
Line 262:   @Test
Line 263:   void rejectEmptyList() {
Line 264:     assertThatThrownBy(() -> {                              
Line 265:       List<Estimate> emptyList = Collections.emptyList();   
Line 266:       new PlanningPoker().identifyExtremes(emptyList);      
Line 267:     }).isInstanceOf(IllegalArgumentException.class);        
Line 268:   }
Line 269:   @Test
Line 270:   void rejectSingleEstimate() {
Line 271: Listing 1.3
Line 272: Adding validation to prevent invalid inputs
Line 273: Listing 1.4
Line 274: Test cases for null, an empty list, and a one-element list
Line 275: The list of estimates cannot be null.
Line 276: The list of estimates should
Line 277: contain more than one element.
Line 278: Asserts that an exception 
Line 279: happens when we call 
Line 280: the method
Line 281: Asserts that this 
Line 282: assertion is an 
Line 283: IllegalArgumentException
Line 284: Similar to the earlier 
Line 285: test, ensures that the 
Line 286: program throws an 
Line 287: exception if an empty 
Line 288: list of estimates is 
Line 289: passed as input
Line 290: 
Line 291: --- 페이지 35 ---
Line 292: 7
Line 293: Developers who test vs. developers who do not
Line 294:     assertThatThrownBy(() -> {                                          
Line 295:       List<Estimate> list = Arrays.asList(new Estimate("Eleanor", 1));  
Line 296:       new PlanningPoker().identifyExtremes(list);                       
Line 297:     }).isInstanceOf(IllegalArgumentException.class);                    
Line 298:   }
Line 299: }
Line 300: The three test cases have the same structure. They all invoke the method under test with
Line 301: an invalid input and check that the method throws an IllegalArgumentException.
Line 302: This is common assertion behavior in Java. The assertThatThrownBy method pro-
Line 303: vided by the AssertJ library (https://assertj.github.io/doc/) enables us to assert that
Line 304: the method throws an exception. Also note the isInstanceOf method, which allows
Line 305: us to assert that a specific type of exception is thrown.
Line 306:  If you are not familiar with Java, the lambda syntax () -> is basically an inline code
Line 307: block. This may be clearer in the second test, rejectEmptyList(), where { and }
Line 308: delimit the block. The testing framework will run this block of code and, if an excep-
Line 309: tion happens, will check the type of the exception. If the exception type matches, the
Line 310: test will pass. Note that this test fails if the exception is not thrown—after all, having
Line 311: an exception is the behavior we expect in this case.
Line 312: NOTE
Line 313: If you are new to automated tests, this code may make you nervous.
Line 314: Testing exceptions involves some extra code, and it is also an “upside-down”
Line 315: test that passes if the exception is thrown! Don’t worry—the more you see test
Line 316: methods, the better you will understand them.
Line 317: With the invalid inputs handled, Eleanor now focuses on the good weather tests: that is,
Line 318: tests that exercise the valid behavior of the program. Looking back at Eleanor’s test
Line 319: cases, this means passing lists of estimates with more than one element. Deciding how
Line 320: many elements to pass is always challenging, but Eleanor sees at least two cases: a list
Line 321: with exactly two elements and a list with more than two elements. Why two? A list with
Line 322: two elements is the smallest for which the method should work. There is a boundary
Line 323: between a list with one element (which does not work) and two elements (which does
Line 324: work). Eleanor knows that bugs love boundaries, so she decides to also have a dedicated
Line 325: test for it, illustrated in listing 1.5.
Line 326:  This resembles a more traditional test case. We define the input value we want to
Line 327: pass to the method under test (in this case, a list with two estimates); we invoke the
Line 328: method under test with that input; and, finally, we assert that the list returns the two
Line 329: developers we expect.
Line 330: @Test
Line 331: void twoEstimates() {
Line 332:   List<Estimate> list = Arrays.asList(    
Line 333:       new Estimate("Mauricio", 10),
Line 334:       new Estimate("Frank", 5)
Line 335:   );
Line 336: Listing 1.5
Line 337: Test case for a list with two elements
Line 338: Ensures that the program throws an exception
Line 339: if a list with a single estimate is passed
Line 340: Declares a 
Line 341: list with two 
Line 342: estimates
Line 343: 
Line 344: --- 페이지 36 ---
Line 345: 8
Line 346: CHAPTER 1
Line 347: Effective and systematic software testing
Line 348:   List<String> devs = new PlanningPoker()     
Line 349:     .identifyExtremes(list);
Line 350:   assertThat(devs)                         
Line 351:       .containsExactlyInAnyOrder("Mauricio", "Frank");
Line 352: }
Line 353: @Test
Line 354: void manyEstimates() {
Line 355:   List<Estimate> list = Arrays.asList(   
Line 356:       new Estimate("Mauricio", 10),
Line 357:       new Estimate("Arie", 5),
Line 358:       new Estimate("Frank", 7)
Line 359:   );
Line 360:   List<String> devs = new PlanningPoker()
Line 361:     .identifyExtremes(list);      
Line 362:   assertThat(devs)                               
Line 363:       .containsExactlyInAnyOrder("Mauricio", "Arie");
Line 364: }
Line 365: Before we continue, I want to highlight that Eleanor has five passing tests, but the
Line 366: else if bug is still there. Eleanor does not know about it yet (or, rather, has not found
Line 367: it). However, she knows that whenever lists are given as input, the order of the elements
Line 368: may affect the algorithm. Therefore, she decides to write a test that provides the
Line 369: method with estimates in random order. For this test, Eleanor does not use example-
Line 370: based testing (tests that pick one specific input out of many possible inputs). Rather,
Line 371: she goes for a property-based test, as shown in the following listing.
Line 372: @Property   
Line 373: void inAnyOrder(@ForAll("estimates") List<Estimate> estimates) {   
Line 374:   estimates.add(new Estimate("MrLowEstimate", 1));     
Line 375:   estimates.add(new Estimate("MsHighEstimate", 100));  
Line 376:   Collections.shuffle(estimates);  
Line 377:   List<String> dev = new PlanningPoker().identifyExtremes(estimates);
Line 378:   assertThat(dev)  
Line 379:       .containsExactlyInAnyOrder("MrLowEstimate", "MsHighEstimate");
Line 380: }
Line 381: @Provide       
Line 382: Arbitrary<List<Estimate>> estimates() {
Line 383: Listing 1.6
Line 384: Property-based testing for multiple estimates
Line 385: Calls the method 
Line 386: we want to test: 
Line 387: identifyExtremes
Line 388: Asserts that the method 
Line 389: correctly returns the 
Line 390: two developers
Line 391: Declares another list 
Line 392: of estimates, now with 
Line 393: three developers
Line 394: Again calls
Line 395: the method
Line 396: under test
Line 397: Asserts that it returns the 
Line 398: two correct developers: 
Line 399: Mauricio and Arie
Line 400: Makes this method a property-based 
Line 401: test instead of a traditional JUnit test
Line 402: The list that the framework provides will contain
Line 403: randomly generated estimates. This list is generated
Line 404: by the method with the name that matches the
Line 405: string "estimates" (declared later in the code).
Line 406: Ensures that the 
Line 407: generated list contains 
Line 408: the known lowest and 
Line 409: highest estimates
Line 410: Shuffles
Line 411: the list to
Line 412: ensure that
Line 413: the order
Line 414: does not
Line 415: matter
Line 416: Asserts that regardless of the list of estimates, the 
Line 417: outcome is always MrLowEstimate and MsHighEstimate
Line 418: Method that provides a random list of 
Line 419: estimates for the property-based test
Line 420: 
Line 421: --- 페이지 37 ---
Line 422: 9
Line 423: Developers who test vs. developers who do not
Line 424:   Arbitrary<String> names = Arbitraries.strings()
Line 425:       .withCharRange('a', 'z').ofLength(5);    
Line 426:   Arbitrary<Integer> values = Arbitraries.integers().between(2, 99);  
Line 427:   Arbitrary<Estimate> estimates = Combinators.combine(names, values)
Line 428:       .as((name, value) -> new Estimate(name, value));  
Line 429:   return estimates.list().ofMinSize(1);  
Line 430: }
Line 431: In property-based testing, our goal is to assert a specific property. We discuss this in
Line 432: more detail later in chapter 5, but here is a short explanation. The estimates()
Line 433: method returns random Estimates. We define that an estimate has a random name
Line 434: (for simplicity, of length five) and a random estimate that varies from 2 to 99. The
Line 435: method feeds lists of Estimates back to the test method. The lists all have at least one
Line 436: element. The test method then adds two more estimates: the lowest and the highest.
Line 437: Since our list only has values between 2 and 99, we ensure the lowest and highest by
Line 438: using the values 1 and 100, respectively. We then shuffle the list so order does not mat-
Line 439: ter. Finally, we assert that no matter what the list of estimates contains, MrLowEstimate
Line 440: and MsHighEstimate are always returned.
Line 441:  The property-based testing framework runs the same test 100 times, each time with
Line 442: a different combination of estimates. If the test fails for one of the random inputs, the
Line 443: framework stops the test and reports the input that broke the code. In this book, we
Line 444: use the jqwik library (https://jqwik.net), but you can easily find a property-based test-
Line 445: ing framework for your language.
Line 446:  To Eleanor’s surprise, when she runs this property-based test, it fails! Based on the
Line 447: example provided by the test, she finds that the else if is wrong and replaces it with a
Line 448: simple if. The test now passes.
Line 449:  Eleanor decides to delete the manyEstimates test, as the new property-based testing
Line 450: replaces it. Whether to delete a duplicate test is a personal decision; you could argue
Line 451: that the simple example-based test is easier to understand than the property-based test.
Line 452: And having simple tests that quickly explain the behavior of the production code is
Line 453: always beneficial, even if it means having a little duplication in your test suite.
Line 454:  Next, Eleanor remembers that in lists, duplicate elements can also break the code.
Line 455: In this case, this would mean developers with the same estimate. She did not consider
Line 456: this case in her implementation. She reflects on how this will affect the method, con-
Line 457: sults with the product owner, and decides that the program should return the dupli-
Line 458: cate developer who appears first in the list.
Line 459:  Eleanor notices that the program already has this behavior. Still, she decides to
Line 460: formalize it in the test shown in listing 1.7. The test is straightforward: it creates a list
Line 461: of estimates in which two developers give the same lowest estimate and two other
Line 462: Generates random names of length five, 
Line 463: composed of only lowercase letters
Line 464: Generates random values for the
Line 465: estimates, ranging from 2 to 99
Line 466: Combines them, thus
Line 467: generating random estimates
Line 468: Returns a list of estimates 
Line 469: with a minimum size of 1 (and no 
Line 470: constraint for how big the list can be)
Line 471: 
Line 472: --- 페이지 38 ---
Line 473: 10
Line 474: CHAPTER 1
Line 475: Effective and systematic software testing
Line 476: developers give the same highest estimate. The test then calls the method under test
Line 477: and ensures that the two developers who appear earlier in the list are returned.
Line 478: @Test
Line 479: void developersWithSameEstimates() {
Line 480:   List<Estimate> list = Arrays.asList(   
Line 481:       new Estimate("Mauricio", 10),
Line 482:       new Estimate("Arie", 5),
Line 483:       new Estimate("Andy", 10),
Line 484:       new Estimate("Frank", 7),
Line 485:       new Estimate("Annibale", 5)
Line 486:   );
Line 487:   List<String> devs = new PlanningPoker().identifyExtremes(list);
Line 488:   assertThat(devs)             
Line 489:     .containsExactlyInAnyOrder("Mauricio", "Arie");
Line 490: }
Line 491: But, Eleanor thinks, what if the list only contains developers with the same estimates?
Line 492: This is another corner case that emerges when we systematically reflect on inputs
Line 493: that are lists. Lists with zero elements, one element, many elements, different values,
Line 494: and identical values are all common test cases to engineer whenever lists are used
Line 495: as inputs.
Line 496:  She talks to the product owner again. They are surprised that they did not see this
Line 497: corner case coming, and they request that in this case, the code should return an
Line 498: empty list. Eleanor changes the implementation to reflect the new expected behavior
Line 499: by adding an if statement near the end of the method, as in the following listing.
Line 500: public List<String> identifyExtremes(List<Estimate> estimates) {
Line 501:   if(estimates == null) {
Line 502:     throw new IllegalArgumentException("Estimates
Line 503:     ➥ cannot be null");
Line 504:   }
Line 505:   if(estimates.size() <= 1) {
Line 506:     throw new IllegalArgumentException("There has to be
Line 507:     ➥ more than 1 estimate in the list");
Line 508:   }
Line 509:   Estimate lowestEstimate = null;
Line 510:   Estimate highestEstimate = null;
Line 511:   for(Estimate estimate: estimates) {
Line 512:     if(highestEstimate == null ||
Line 513:         estimate.getEstimate() > highestEstimate.getEstimate()) {
Line 514:       highestEstimate = estimate;
Line 515:     }
Line 516: Listing 1.7
Line 517: Ensuring that the first duplicate developer is returned
Line 518: Listing 1.8
Line 519: Returning an empty list if all estimates are the same
Line 520: Declares a list of estimates 
Line 521: with repeated estimate 
Line 522: values
Line 523: Asserts that whenever there are 
Line 524: repeated estimates, the developer 
Line 525: who appears earlier in the list is 
Line 526: returned by the method
Line 527: 
Line 528: --- 페이지 39 ---
Line 529: 11
Line 530: Effective software testing for developers
Line 531:     if(lowestEstimate == null ||
Line 532:         estimate.getEstimate() < lowestEstimate.getEstimate()) {
Line 533:       lowestEstimate = estimate;
Line 534:     }
Line 535:   }
Line 536:   if(lowestEstimate.equals(highestEstimate))  
Line 537:     return Collections.emptyList();
Line 538:   return Arrays.asList(
Line 539:       lowestEstimate.getDeveloper(),
Line 540:       highestEstimate.getDeveloper()
Line 541:   );
Line 542: }
Line 543: Eleanor then writes a test to ensure that her implementation is correct.
Line 544: @Test
Line 545: void allDevelopersWithTheSameEstimate() {
Line 546:   List<Estimate> list = Arrays.asList(  
Line 547:       new Estimate("Mauricio", 10),
Line 548:       new Estimate("Arie", 10),
Line 549:       new Estimate("Andy", 10),
Line 550:       new Estimate("Frank", 10),
Line 551:       new Estimate("Annibale", 10)
Line 552:   );
Line 553:   List<String> devs = new PlanningPoker().identifyExtremes(list);
Line 554:   assertThat(devs).isEmpty();  
Line 555: }
Line 556: Eleanor is now satisfied with the test suite she has engineered from the requirements.
Line 557: As a next step, she decides to focus on the code itself. Maybe there is something that
Line 558: no tests are exercising. To help her in this analysis, she runs the code coverage tool
Line 559: that comes with her IDE (figure 1.3).
Line 560:  All the lines and branches of the code are covered. Eleanor knows that tools are
Line 561: not perfect, so she examines the code for other cases. She cannot find any, so she con-
Line 562: cludes that the code is tested enough. She pushes the code and goes home for the
Line 563: weekend. The code goes directly to the customers. On Monday morning, Eleanor is
Line 564: happy to see that monitoring does not report a single crash.
Line 565: 1.2
Line 566: Effective software testing for developers
Line 567: I hope the difference is clear between the two developers in the previous section. Elea-
Line 568: nor used automated tests and systematically and effectively engineered test cases. She
Line 569: broke down the requirements into small parts and used them to derive test cases,
Line 570: applying a technique called domain testing. When she was done with the specification,
Line 571: Listing 1.9
Line 572: Testing for an empty list if the estimates are all the same
Line 573: If the lowest and highest 
Line 574: estimate objects are the same, 
Line 575: all developers have the same 
Line 576: estimate, and therefore we 
Line 577: return an empty list.
Line 578: Declares a list of estimates, 
Line 579: this time with all the 
Line 580: developers having the 
Line 581: same estimate
Line 582: Asserts that the 
Line 583: resulting list is empty
Line 584: 
Line 585: --- 페이지 40 ---
Line 586: 12
Line 587: CHAPTER 1
Line 588: Effective and systematic software testing
Line 589: she focused on the code; and through structural testing (or code coverage), she evalu-
Line 590: ated whether the current test cases were sufficient. For some test cases, Eleanor wrote
Line 591: example-based tests (that is, she picked a single data point for a test). For one specific
Line 592: case, she used property-based testing, as it helped her better explore possible bugs in the
Line 593: code. Finally, she reflected frequently about the contracts and pre- and post-conditions of
Line 594: the method she was devising (although in the end, she implemented a set of valida-
Line 595: tion checks and not pre-conditions per se; we discuss the differences between con-
Line 596: tracts and validation in chapter 4).
Line 597:  This is what I call effective and systematic software testing for developers. In the remain-
Line 598: der of this chapter, I explain how software developers can perform effective testing
Line 599: together with their development activities. Before we dive into the specific techniques,
Line 600: I describe effective testing within the development processes and how testing tech-
Line 601: niques complement each other. I discuss the different types of tests and which ones
Line 602: you should focus on. Finally, I illustrate why software testing is so difficult.
Line 603: 1.2.1
Line 604: Effective testing in the development process
Line 605: In this book, I propose a straightforward flow for developers who apply effective and
Line 606: systematic testing. First, we implement a feature, using tests to facilitate and guide
Line 607: development. Once we are reasonably happy with the feature or small unit we’ve
Line 608: coded, we dive into effective and systematic testing to ensure that it works as expected
Line 609: (that is, we test to find bugs). Figure 1.4 illustrates the development workflow in more
Line 610: detail; let’s walk through it:
Line 611: IntelliJ indicates that these
Line 612: lines are covered by adding
Line 613: a color near the line. Green
Line 614: indicates the line is covered;
Line 615: red indicates the line is not
Line 616: covered.
Line 617: Here, due to the monochrome
Line 618: ﬁgure, you can't see the green
Line 619: color, but all lines are green.
Line 620: Figure 1.3
Line 621: The result of the code coverage analysis done by my IDE, IntelliJ. All lines are covered.
Line 622: 
Line 623: --- 페이지 41 ---
Line 624: 13
Line 625: Effective software testing for developers
Line 626: 1
Line 627: Feature development often starts with a developer receiving some sort of require-
Line 628: ment. Requirements are often in the form of natural language and may follow a
Line 629: specific format, such as Unified Modeling Language (UML) use cases or agile
Line 630: user stories. After building up some understanding (that is, requirement analysis),
Line 631: the developer starts writing code.
Line 632: 2
Line 633: To guide the development of the feature, the developer performs short test-
Line 634: driven development (TDD) cycles. These cycles give the developer rapid feedback
Line 635: about whether the code they just wrote makes sense. They also support the
Line 636: developer through the many refactorings that occur when a new feature is
Line 637: being implemented.
Line 638: 3
Line 639: Requirements are often large and complex and are rarely implemented by a
Line 640: single class or method. The developer creates several units (classes and methods)
Line 641: with different contracts, and they collaborate and together form the required
Line 642: functionality. Writing classes such that they’re easy to test is challenging, and
Line 643: the developer must design with testability in mind.
Line 644: 4
Line 645: Once the developer is satisfied with the units they’ve created and believes the
Line 646: requirement is complete, they shift to testing. The first step is to exercise each
Line 647: Developer
Line 648: Builds a
Line 649: feature
Line 650: T
Line 651: o guide
Line 652: e
Line 653: esting t
Line 654: d velopment
Line 655: Requirement
Line 656: analysis
Line 657: Test-driven
Line 658: development
Line 659: Design for
Line 660: testability
Line 661: Design by
Line 662: contracts
Line 663: Eﬀective and systematic testing
Line 664: Speciﬁcation
Line 665: testing
Line 666: Bound
Line 667: y
Line 668: ar
Line 669: testing
Line 670: Structural
Line 671: testing
Line 672: Intelligent testing
Line 673: Mutation
Line 674: testing
Line 675: Larger tests
Line 676: Integration
Line 677: testing
Line 678: System
Line 679: testing
Line 680: Unit w h d
Line 681: s
Line 682: it
Line 683: iﬀerent roles
Line 684: and
Line 685: iliti
Line 686: responsib
Line 687: es
Line 688: Unit testing
Line 689: Property-
Line 690: based testing
Line 691: Here, we’ll discuss ideas
Line 692: that will help us in
Line 693: implementing the feature
Line 694: with conﬁdence and with
Line 695: testability in mind.
Line 696: Here, we’ll discuss different techniques
Line 697: that will exercise our implementation
Line 698: from many different angles and help us
Line 699: to identify possible bugs in our code.
Line 700: Mocks,
Line 701: stubs, and
Line 702: fakes
Line 703: Automated test
Line 704: suite
Line 705: T
Line 706: ode
Line 707: est c
Line 708: quality
Line 709: Figure 1.4
Line 710: The workflow of a developer who applies effective and systematic testing. The arrows indicate 
Line 711: the iterative nature of the process; developers may go back and forth between the different techniques as 
Line 712: they learn more about the program under development and test.
Line 713: 
Line 714: --- 페이지 42 ---
Line 715: 14
Line 716: CHAPTER 1
Line 717: Effective and systematic software testing
Line 718: new unit. Domain testing, boundary testing, and structural testing are the go-to
Line 719: techniques.
Line 720: 5
Line 721: Some parts of the system may require the developer to write larger tests (integra-
Line 722: tion or system tests). To devise larger test cases, the developer uses the same
Line 723: three techniques—domain testing, boundary testing, and structural testing—
Line 724: but looking at larger parts of the software system.
Line 725: 6
Line 726: When the developer has engineered test cases using the various techniques,
Line 727: they apply automated, intelligent testing tools to look for tests that humans are
Line 728: not good at spotting. Popular techniques include test case generation, mutation
Line 729: testing, and static analysis. In this book, we cover mutation testing.
Line 730: 7
Line 731: Finally, after this rigorous testing, the developer feels comfortable releasing
Line 732: the feature. 
Line 733: 1.2.2
Line 734: Effective testing as an iterative process
Line 735: While the previous description may sound like a sequential/waterfall process, it is
Line 736: more iterative. A developer may be rigorously testing a class and suddenly notice that
Line 737: a coding decision they made a few hours ago was not ideal. They then go back and
Line 738: redesign the code. They may be performing TDD cycles and realize the requirement
Line 739: is unclear about something. The developer then goes back to the requirement analy-
Line 740: sis to better grasp the expectations. Quite commonly, while testing, the developer
Line 741: finds a bug. They go back to the code, fix it, and continue testing. Or the developer
Line 742: may have implemented only half of the feature, but they feel it would be more pro-
Line 743: ductive to rigorously test it now than to continue the implementation.
Line 744:  The development workflow I propose throughout this book is not meant to
Line 745: restrain you. Feel free to go back and forth between techniques or change the order
Line 746: in which you apply them. In practice, you have to find what works best for you and
Line 747: makes you the most productive. 
Line 748: 1.2.3
Line 749: Focusing on development and then on testing
Line 750: I find it liberating to focus separately on developing and testing. When I am coding a
Line 751: feature, I do not want to be distracted by obscure corner cases. If I think of one, I take
Line 752: notes so I do not forget to test it later. However, I prefer to focus all my energy on the
Line 753: business rules I am implementing and, at the same time, ensure that the code is easy
Line 754: for future developers to maintain.
Line 755:  Once I am finished with the coding decisions, I focus on testing. First I follow the
Line 756: different techniques as if I were working my way down a systematic checklist. As you
Line 757: saw in the example with Eleanor, she did not have to think much about what to exer-
Line 758: cise when the method received a list: she responded as if she had a checklist that said
Line 759: “null, empty list, one element, many elements.” Only then do I use my creativity and
Line 760: domain knowledge to exercise other cases I find relevant.
Line 761: 
Line 762: --- 페이지 43 ---
Line 763: 15
Line 764: Effective software testing for developers
Line 765: 1.2.4
Line 766: The myth of “correctness by design”
Line 767: Now that you have a clearer picture of what I mean by effective and systematic soft-
Line 768: ware testing, let me debunk a myth. There is a perception among software developers
Line 769: that if you design code in a simple way, it will not have bugs, as if the secret of bug-free
Line 770: code is simplicity.
Line 771:  Empirical research in software engineering has repeatedly shown that simple,
Line 772: non-smelly code is less prone to defects than complex code (see, for example, the
Line 773: 2006 paper by Shatnawi and Li). However, simplicity is far from enough. It is naive
Line 774: to believe that testing can be fully replaced by simplicity. The same is true for
Line 775: “correctness by design”: designing your code well does not mean you avoid all pos-
Line 776: sible bugs.
Line 777: 1.2.5
Line 778: The cost of testing
Line 779: You may be thinking that forcing developers to apply rigorous testing may be too
Line 780: costly. Figure 1.4 shows the many techniques developers have to apply if they follow
Line 781: the flow I am proposing. It is true: testing software properly is more work than not
Line 782: doing so. Let me convince you why it is worth it:
Line 783: The cost of bugs that happen in production often outweighs the cost of preven-
Line 784: tion (as shown by Boehm and Papaccio, 1988). Think of a popular web shop
Line 785: and how much it would cost the shop if the payment application goes down for
Line 786: 30 minutes due to a bug that could have been easily prevented via testing.
Line 787: Teams that produce many bugs tend to waste time in an eternal loop where
Line 788: developers write bugs, customers (or dedicated QAs) find the bugs, developers
Line 789: fix the bugs, customers find a different set of bugs, and so on.
Line 790: Practice is key. Once developers are used to engineering test cases, they can do
Line 791: it much faster. 
Line 792: 1.2.6
Line 793: The meaning of effective and systematic
Line 794: I have been using two words to describe how I expect a developer to test: effectively and
Line 795: systematically. Being effective means we focus on writing the right tests. Software testing
Line 796: is all about trade-offs. Testers want to maximize the number of bugs they find while
Line 797: minimizing the effort required to find the bugs. How do we achieve this? By knowing
Line 798: what to test.
Line 799:  All the techniques I present in this book have a clear beginning (what to test) and
Line 800: a clear end (when to stop). Of course, I do not mean your systems will be bug-free if you
Line 801: follow these techniques. As a community, we still do not know how to build bug-free
Line 802: systems. But I can confidently say that the number of bugs will be reduced, hopefully
Line 803: to tolerable levels.
Line 804:  Being systematic means that for a given piece of code, any developer should come
Line 805: up with the same test suite. Testing often happens in an ad hoc manner. Developers
Line 806: engineer the test cases that come to mind. It is common to see two developers devel-
Line 807: 
Line 808: --- 페이지 44 ---
Line 809: 16
Line 810: CHAPTER 1
Line 811: Effective and systematic software testing
Line 812: oping different test suites for the same program. We should be able to systematize our
Line 813: processes to reduce the dependency on the developer who is doing the job.
Line 814:  I understand and agree with the argument that software development is a creative
Line 815: process that cannot be executed by robots. I believe that humans will always be in the
Line 816: loop when it comes to building software; but why not let developers focus on what
Line 817: requires creativity? A lot of software testing can be systematized, and that is what you
Line 818: will see throughout this book. 
Line 819: 1.2.7
Line 820: The role of test automation
Line 821: Automation is key for an effective testing process. Every test case we devise here is
Line 822: later automated via a testing framework such as JUnit. Let me clearly distinguish
Line 823: between test case design and test case execution. Once a test case is written, a framework
Line 824: runs it and shows reports, failures, and so on. This is all that these frameworks do.
Line 825: Their role is very important, but the real challenge in software testing is not writing
Line 826: JUnit code but designing decent test cases that may reveal bugs. Designing test cases is
Line 827: mostly a human activity and is what this book primarily focuses on.
Line 828: NOTE
Line 829: If you are not familiar with JUnit, it should not be a problem, because
Line 830: the examples in the book are easy to read. But as I mention throughout the
Line 831: book, the more familiar you are with the testing framework, the better.
Line 832: In the chapters where I discuss testing techniques, we first engineer the test cases and
Line 833: only later automate them with JUnit code. In real life, you may mingle both activities;
Line 834: but in this book, I decided to keep them separate so you can see the difference. This
Line 835: also means the book does not talk much about tooling. JUnit and other testing frame-
Line 836: works are powerful tools, and I recommend reading the manuals and books that focus
Line 837: on them. 
Line 838: 1.3
Line 839: Principles of software testing 
Line 840: (or, why testing is so difficult)
Line 841: A simplistic view of software testing is that if we want our systems to be well tested, we
Line 842: must keep adding tests until we have enough. I wish it were that simple. Ensuring that
Line 843: programs have no bugs is virtually impossible, and developers should understand why
Line 844: that is the case.
Line 845:  In this section, I discuss some principles that make our lives as software testers
Line 846: more difficult and what we can do to mitigate them. These principles were inspired by
Line 847: those presented in the International Software Testing Qualifications Board (ISTQB)
Line 848: book by Black, Veenendaal, and Graham (2012).
Line 849: 1.3.1
Line 850: Exhaustive testing is impossible
Line 851: We do not have the resources to completely test our programs. Testing all possible sit-
Line 852: uations in a software system might be impossible even if we had unlimited resources.
Line 853: Imagine a software system with “only” 300 different flags or configuration settings
Line 854: 
Line 855: --- 페이지 45 ---
Line 856: 17
Line 857: Principles of software testing (or, why testing is so difficult)
Line 858: (such as the Linux operating system). Each flag can be set to true or false (Boolean)
Line 859: and can be set independently from the others. The software system behaves differ-
Line 860: ently according to the configured combination of flags. Having two possible values for
Line 861: each of the 300 flags gives 2300 combinations that need to be tested. For comparison,
Line 862: the number of atoms in the universe is estimated to be 1080. In other words, this soft-
Line 863: ware system has more possible combinations to be tested than the universe has atoms.
Line 864:  Knowing that testing everything is not possible, we have to choose (or prioritize)
Line 865: what to test. This is why I emphasize the need for effective tests. The book discusses tech-
Line 866: niques that will help you identify the relevant test cases. 
Line 867: 1.3.2
Line 868: Knowing when to stop testing
Line 869: Prioritizing which tests to engineer is difficult. Creating too few tests may leave us with
Line 870: a software system that does not behave as intended (that is, it’s full of bugs). On the
Line 871: other hand, creating test after test without proper consideration can lead to ineffec-
Line 872: tive tests (and cost time and money). As I said before, our goal should always be to
Line 873: maximize the number of bugs found while minimizing the resources we spend on
Line 874: finding those bugs. To that aim, I will discuss different adequacy criteria that will help
Line 875: you decide when to stop testing. 
Line 876: 1.3.3
Line 877: Variability is important (the pesticide paradox)
Line 878: There is no silver bullet in software testing. In other words, there is no single testing
Line 879: technique that you can always apply to find all possible bugs. Different testing tech-
Line 880: niques help reveal different bugs. If you use only a single technique, you may find all
Line 881: the bugs you can with that technique and no more.
Line 882:  A more concrete example is a team that relies solely on unit testing techniques.
Line 883: The team may find all the bugs that can be captured at the unit test level, but they may
Line 884: miss bugs that only occur at the integration level.
Line 885:  This is known as the pesticide paradox: every method you use to prevent or find bugs
Line 886: leaves a residue of subtler bugs against which those methods are ineffectual. Testers
Line 887: must use different testing strategies to minimize the number of bugs left in the soft-
Line 888: ware. When studying the various testing strategies presented in this book, keep in
Line 889: mind that combining them all is probably a wise decision. 
Line 890: 1.3.4
Line 891: Bugs happen in some places more than others
Line 892: As I said earlier, given that exhaustive testing is impossible, software testers have to pri-
Line 893: oritize the tests they perform. When prioritizing test cases, note that bugs are not uni-
Line 894: formly distributed. Empirically, our community has observed that some components
Line 895: present more bugs than others. For example, a Payment module may require more
Line 896: rigorous testing than a Marketing module.
Line 897:  As a real-world example, take Schröter and colleagues (2006), who studied bugs in
Line 898: the Eclipse projects. They observed that 71% of files that imported compiler packages
Line 899: had to be fixed later. In other words, such files were more prone to defects than the
Line 900: 
Line 901: --- 페이지 46 ---
Line 902: 18
Line 903: CHAPTER 1
Line 904: Effective and systematic software testing
Line 905: other files in the system. As a software developer, you may have to watch and learn
Line 906: from your software system. Data other than the source code may help you prioritize
Line 907: your testing efforts. 
Line 908: 1.3.5
Line 909: No matter what testing you do, it will never be perfect or enough
Line 910: As Dijkstra used to say, “Program testing can be used to show the presence of bugs, but
Line 911: never to show their absence.” In other words, while we may find more bugs by simply
Line 912: testing more, our test suites, however large they may be, will never ensure that the soft-
Line 913: ware system is 100% bug-free. They will only ensure that the cases we test for behave
Line 914: as expected.
Line 915:  This is an important principle to understand, as it will help you set your (and your
Line 916: customers’) expectations. Bugs will still happen, but (hopefully) the money you pay
Line 917: for testing and prevention will pay off by allowing only the less impactful bugs to go
Line 918: through. “You cannot test everything” is something we must accept.
Line 919: NOTE
Line 920: Although monitoring is not a major topic in this book, I recommend
Line 921: investing in monitoring systems. Bugs will happen, and you need to be sure
Line 922: you find them the second they manifest in production. That is why tools such
Line 923: as the ELK stack (Elasticsearch, Logstash, and Kibana; www.elastic.co) are
Line 924: becoming so popular. This approach is sometimes called testing in production
Line 925: (Wilsenach, 2017). 
Line 926: 1.3.6
Line 927: Context is king
Line 928: The context plays an important role in how we devise test cases. For example, devising
Line 929: test cases for a mobile app is very different from devising test cases for a web applica-
Line 930: tion or software used in a rocket. In other words, testing is context-dependent.
Line 931:  Most of this book tries to be agnostic about context. The techniques I discuss
Line 932: (domain testing, structural testing, property-based testing, and so on) can be applied
Line 933: in any type of software system. Nevertheless, if you are working on a mobile app, I rec-
Line 934: ommend reading a book dedicated to mobile testing after you read this one. I give
Line 935: some context-specific tips in chapter 9, where I discuss larger tests. 
Line 936: 1.3.7
Line 937: Verification is not validation
Line 938: Finally, note that a software system that works flawlessly but is of no use to its users is
Line 939: not a good software system. As a reviewer of this book said to me, “Coverage of code is
Line 940: easy to measure; coverage of requirements is another matter.” Software testers face
Line 941: this absence-of-errors fallacy when they focus solely on verification and not on validation.
Line 942:  A popular saying that may help you remember the difference is, “Verification is
Line 943: about having the system right; validation is about having the right system.” This book
Line 944: primarily covers verification techniques. In other words, I do not focus on techniques
Line 945: to, for example, collaborate with customers to understand their real needs; rather, I
Line 946: present techniques to ensure that, given a specific requirement, the software system
Line 947: implements it correctly.
Line 948: 
Line 949: --- 페이지 47 ---
Line 950: 19
Line 951: The testing pyramid, and where we should focus
Line 952:  Verification and validation can walk hand in hand. In this chapter’s example about
Line 953: the planning poker algorithm, this was what happened when Eleanor imagined all the
Line 954: developers estimating the same effort. The product owner did not think of this case. A
Line 955: systematic testing approach can help you identify corner cases that even the product
Line 956: experts did not envision. 
Line 957: 1.4
Line 958: The testing pyramid, and where we should focus
Line 959: Whenever we talk about pragmatic testing, one of the first decisions we need to make
Line 960: is the level at which to test the code. By a test level, I mean the unit, integration, or system
Line 961: level. Let’s quickly look at each of them.
Line 962: 1.4.1
Line 963: Unit testing
Line 964: In some situations, the tester’s goal is to test a single feature of the software, purpose-
Line 965: fully ignoring the other units of the system. This is basically what we saw in the plan-
Line 966: ning poker example. The goal was to test the identifyExtremes() method and
Line 967: nothing else. Of course, we cared about how this method would interact with the rest
Line 968: of the system, and that is why we tested its contracts. However, we did not test it
Line 969: together with the other pieces of the system.
Line 970:  When we test units in isolation, we are doing unit testing. This test level offers the
Line 971: following advantages:
Line 972: Unit tests are fast. A unit test usually takes just a couple of milliseconds to exe-
Line 973: cute. Fast tests allow us to test huge portions of the system in a small amount of
Line 974: time. Fast, automated test suites give us constant feedback. This fast safety net
Line 975: makes us feel more comfortable and confident in performing evolutionary
Line 976: changes to the software system we are working on.
Line 977: Unit tests are easy to control. A unit test tests the software by giving certain parame-
Line 978: ters to a method and then comparing the return value of this method to the
Line 979: expected result. These input values and the expected result value are easy to
Line 980: adapt or modify in the test. Again, look at the identifyExtremes() example
Line 981: and how easy it was to provide different inputs and assert its output.
Line 982: Unit tests are easy to write. They do not require a complicated setup or additional
Line 983: work. A single unit is also often cohesive and small, making the tester’s job eas-
Line 984: ier. Tests become much more complicated when we have databases, frontends,
Line 985: and web services all together.
Line 986: As for disadvantages, the following should be considered:
Line 987: Unit tests lack reality. A software system is rarely composed of a single class. The
Line 988: large number of classes in a system and their interaction can cause the system to
Line 989: behave differently in its real application than in the unit tests. Therefore, unit
Line 990: tests do not perfectly represent the real execution of a software system.
Line 991: Some types of bugs are not caught. Some types of bugs cannot be caught at the unit
Line 992: test level; they only happen in the integration of the different components
Line 993: 
Line 994: --- 페이지 48 ---
Line 995: 20
Line 996: CHAPTER 1
Line 997: Effective and systematic software testing
Line 998: (which are not exercised in a pure unit test). Think of a web application that
Line 999: has a complex UI: you may have tested the backend and the frontend thor-
Line 1000: oughly, but a bug may only reveal itself when the backend and frontend are put
Line 1001: together. Or imagine multithreaded code: everything may work at the unit
Line 1002: level, but bugs may appear once threads are running together.
Line 1003: Interestingly, one of the hardest challenges in unit testing is to define what constitutes
Line 1004: a unit. A unit can be one method or multiple classes. Here is a definition for unit test-
Line 1005: ing that I like, given by Roy Osherove (2009): “A unit test is an automated piece of
Line 1006: code that invokes a unit of work in the system. And a unit of work can span a single
Line 1007: method, a whole class or multiple classes working together to achieve one single logi-
Line 1008: cal purpose that can be verified.”
Line 1009:  For me, unit testing means testing a (small) set of classes that have no dependency
Line 1010: on external systems (such as databases or web services) or anything else I do not fully
Line 1011: control. When I unit-test a set of classes together, the number of classes tends to be
Line 1012: small. This is primarily because testing many classes together may be too difficult, not
Line 1013: because this isn’t a unit test.
Line 1014:  But what if a class I want to test depends on another class that talks to, for example,
Line 1015: a database (figure 1.5)? This is where unit testing becomes more complicated. Here is
Line 1016: a short answer: if I want to test a class, and this class depends on another class that
Line 1017: depends on a database, I will simulate the database class. In other words, I will create a
Line 1018: stub that acts like the original class but is much simpler and easier to use during test-
Line 1019: ing. We will dive into this specific problem in chapter 6, where we discuss mocks. 
Line 1020: 1.4.2
Line 1021: Integration testing
Line 1022: Unit tests focus on the smallest parts of the system. However, testing components in
Line 1023: isolation sometimes is not enough. This is especially true when the code under test
Line 1024: goes beyond the system’s borders and uses other (often external) components. Inte-
Line 1025: gration testing is the test level we use to test the integration between our code and
Line 1026: external parties.
Line 1027:  Let’s consider a real-world example. Software systems commonly rely on database
Line 1028: systems. To communicate with the database, developers often create a class whose
Line 1029: Class
Line 1030: A
Line 1031: Class
Line 1032: B
Line 1033: Class
Line 1034: C
Line 1035: Depends
Line 1036: ATest
Line 1037: DB
Line 1038: C
Line 1039: sume
Line 1040: on
Line 1041: s
Line 1042: When unit testing class A, our focus is on testing A,
Line 1043: as isolated as possible from the rest! If A depends
Line 1044: on other classes, we have to decide whether to
Line 1045: simulate them or to make our unit test a bit bigger.
Line 1046: Unit test
Line 1047: Figure 1.5
Line 1048: Unit testing. Our goal is 
Line 1049: to test one unit of the system that is 
Line 1050: as isolated as possible from the rest 
Line 1051: of the system.
Line 1052: 
Line 1053: --- 페이지 49 ---
Line 1054: 21
Line 1055: The testing pyramid, and where we should focus
Line 1056: only responsibility is to interact with this external component (think of Data Access
Line 1057: Object [DAO] classes). These DAOs may contain complicated SQL code. Thus, a tes-
Line 1058: ter feels the need to test the SQL queries. The tester does not want to test the entire
Line 1059: system, only the integration between the DAO class and the database. The tester also
Line 1060: does not want to test the DAO class in complete isolation. After all, the best way to
Line 1061: know whether a SQL query works is to submit it to the database and see what the
Line 1062: database returns.
Line 1063:  This is an example of an integration test. Integration testing aims to test multiple
Line 1064: components of a system together, focusing on the interactions between them instead
Line 1065: of testing the system as a whole (see figure 1.6). Are they communicating correctly?
Line 1066: What happens if component A sends message X to component B? Do they still present
Line 1067: correct behavior?
Line 1068: Integration testing focuses on two parts: our component and the external component.
Line 1069: Writing such a test is less complicated than writing a test that goes through the entire
Line 1070: system and includes components we do not care about.
Line 1071:  Compared to unit testing, integration tests are more difficult to write. In the exam-
Line 1072: ple, setting up a database for the test requires effort. Tests that involve databases gen-
Line 1073: erally need to use an isolated instance of the database just for testing purposes, update
Line 1074: the database schema, put the database into a state expected by the test by adding or
Line 1075: removing rows, and clean everything afterward. The same effort is involved in other
Line 1076: types of integration tests: web services, file reads and writes, and so on. We will discuss
Line 1077: writing integration tests effectively in chapter 9. 
Line 1078: 1.4.3
Line 1079: System testing
Line 1080: To get a more realistic view of the software and thus perform more realistic tests, we
Line 1081: should run the entire software system with all its databases, frontend apps, and other
Line 1082: components. When we test the system in its entirety, instead of testing small parts of
Line 1083: the system in isolation, we are doing system testing (see figure 1.7). We do not care
Line 1084: how the system works from the inside; we do not care if it was developed in Java or
Line 1085: Class
Line 1086: A
Line 1087: Class
Line 1088: B
Line 1089: Class
Line 1090: C
Line 1091: Depends
Line 1092: DB
Line 1093: C
Line 1094: sume
Line 1095: on
Line 1096: s
Line 1097: Integration testing exercises the
Line 1098: integration between a component
Line 1099: of your system and some external
Line 1100: component (e.g., a database).
Line 1101: CTest
Line 1102: Figure 1.6
Line 1103: Integration testing. Our goal is 
Line 1104: to test whether our component integrates 
Line 1105: well with an external component.
Line 1106: 
Line 1107: --- 페이지 50 ---
Line 1108: 22
Line 1109: CHAPTER 1
Line 1110: Effective and systematic software testing
Line 1111: Ruby, or whether it uses a relational database. We only care that, given input X, the
Line 1112: system will provide output Y.
Line 1113: The obvious advantage of system testing is how realistic the tests are. Our final customers
Line 1114: will not run the identifyExtremes() method in isolation. Rather, they will visit a web
Line 1115: page, submit a form, and see the results. System tests exercise the system in that pre-
Line 1116: cise manner. The more realistic the tests are (that is, when the tests perform actions
Line 1117: similar to the final user), the more confident we can be about the whole system.
Line 1118:  System testing does, however, have its downsides:
Line 1119: System tests are often slow compared to unit tests. Imagine everything a system
Line 1120: test has to do, including starting and running the entire system with all its com-
Line 1121: ponents. The test also has to interact with the real application, and actions may
Line 1122: take a few seconds. Imagine a test that starts a container with a web application
Line 1123: and another container with a database. It then submits an HTTP request to a
Line 1124: web service exposed by this web app. This web service retrieves data from the
Line 1125: database and writes a JSON response to the test. This obviously takes more time
Line 1126: than running a simple unit test, which has virtually no dependencies.
Line 1127: System tests are also harder to write. Some of the components (such as data-
Line 1128: bases) may require a complex setup before they can be used in a testing sce-
Line 1129: nario. Think of connecting, authenticating, and making sure the database has
Line 1130: all the data required by that test case. Additional code is required just to auto-
Line 1131: mate the tests.
Line 1132: System tests are more prone to flakiness. A flaky test presents erratic behavior: if
Line 1133: you run it, it may pass or fail for the same configuration. Flaky tests are an
Line 1134: important problem for software development teams, and we discuss this issue in
Line 1135: chapter 10. Imagine a system test that exercises a web app. After the tester clicks
Line 1136: a button, the HTTP POST request to the web app takes half a second longer
Line 1137: Class
Line 1138: Class
Line 1139: Class
Line 1140: Depends
Line 1141: System
Line 1142: test
Line 1143: DB
Line 1144: C
Line 1145: mes
Line 1146: onsu
Line 1147: When system testing, you
Line 1148: want to exercise the entire
Line 1149: system together, including
Line 1150: all of its classes, dependencies,
Line 1151: database , web services, and
Line 1152: s
Line 1153: whatever other components it
Line 1154: may have.
Line 1155: Controller
Line 1156: Web
Line 1157: ser
Line 1158: e
Line 1159: vic
Line 1160: The entire software system
Line 1161: Request
Line 1162: Response
Line 1163: Figure 1.7
Line 1164: System testing. Our goal is to test the entire system and its components.
Line 1165: 
Line 1166: --- 페이지 51 ---
Line 1167: 23
Line 1168: The testing pyramid, and where we should focus
Line 1169: than usual (due to small variations we often do not control in real-life scenar-
Line 1170: ios). The test does not expect this and thus fails. The test is executed again, the
Line 1171: web app takes the usual time to respond, and the test passes. Many uncertain-
Line 1172: ties in a system test can lead to unexpected behavior. 
Line 1173: 1.4.4
Line 1174: When to use each test level
Line 1175: With a clear understanding of the different test levels and their benefits, we have to
Line 1176: decide whether to invest more in unit testing or system testing and determine which
Line 1177: components should be tested via unit testing and which components should be tested
Line 1178: via system testing. A wrong decision may have a considerable impact on the system’s
Line 1179: quality: a wrong level may cost too many resources and may not find sufficient bugs.
Line 1180: As you may have guessed, the best answer here is, “It depends.”
Line 1181:  Some developers—including me—favor unit testing over other test levels. This
Line 1182: does not mean such developers do not do integration or system testing; but whenever
Line 1183: possible, they push testing toward the unit test level. A pyramid is often used to illus-
Line 1184: trate this idea, as shown in figure 1.8. The size of the slice in the pyramid represents
Line 1185: the relative number of tests to carry out at each test level.
Line 1186: Unit testing is at the bottom of the pyramid and has the largest area. This means
Line 1187: developers who follow this scheme favor unit testing (that is, write more unit tests).
Line 1188: Climbing up in the diagram, the next level is integration testing. The area is smaller,
Line 1189: indicating that, in practice, these developers write fewer integration tests than unit
Line 1190: tests. Given the extra effort that integration tests require, the developers write tests
Line 1191: only for the integrations they need. The diagram shows that these developers favor
Line 1192: system tests less than integration tests and have even fewer manual tests. 
Line 1193: 1.4.5
Line 1194: Why do I favor unit tests?
Line 1195: As I said, I tend to favor unit testing. I appreciate the advantages that unit tests give
Line 1196: me. They are easy to write, they are fast, I can write them intertwined with production
Line 1197: code, and so on. I also believe that unit testing fits very well with the way software
Line 1198: Unit tests
Line 1199: Integration tests
Line 1200: System tests
Line 1201: Manual
Line 1202: More real
Line 1203: More complex
Line 1204: All business rules
Line 1205: should be tested here.
Line 1206: Exploratory tests
Line 1207: Complex integrations
Line 1208: with external services
Line 1209: Tests the main/risky
Line 1210: ﬂow of the app
Line 1211: Figure 1.8
Line 1212: My version of the testing pyramid. The closer a test is to the 
Line 1213: top, the more real and complex the test becomes. At the right part you see 
Line 1214: what I test at each test level.
Line 1215: 
Line 1216: --- 페이지 52 ---
Line 1217: 24
Line 1218: CHAPTER 1
Line 1219: Effective and systematic software testing
Line 1220: developers work. When developers implement a new feature, they write separate units
Line 1221: that will eventually work together to deliver larger functionality. While developing
Line 1222: each unit, it is easy to ensure that it works as expected. Testing small units rigorously
Line 1223: and effectively is much easier than testing a larger piece of functionality.
Line 1224:  Because I am also aware of the disadvantages of unit testing, I think carefully about
Line 1225: how the unit under development will be used by the other units of the system. Enforc-
Line 1226: ing clear contracts and systematically testing them gives me more certainty that things
Line 1227: will work out when they are put together.
Line 1228:  Finally, given the intensity with which I test my code using (simple and cheap)
Line 1229: unit tests, I can use integration and system tests for the parts that really matter. I do
Line 1230: not have to retest all the functionalities again at these levels. I use integration or sys-
Line 1231: tem testing to test specific parts of the code that I believe may cause problems
Line 1232: during integration.
Line 1233: 1.4.6
Line 1234: What do I test at the different levels?
Line 1235: I use unit tests for units that are concerned with an algorithm or a single piece of busi-
Line 1236: ness logic of the software system. Most enterprise/business systems are used to trans-
Line 1237: form data. Such business logic is often expressed by using entity classes (for example,
Line 1238: an Invoice class and an Order class) to exchange messages. Business logic often does
Line 1239: not depend on external services, so it can easily be tested and fully controlled through
Line 1240: unit tests. Unit tests give us full control over the input data as well as full observability
Line 1241: in terms of asserting that the behavior is as expected.
Line 1242: NOTE
Line 1243: If a piece of code deals with specific business logic but cannot be
Line 1244: tested via unit tests (for example, the business logic can only be tested with
Line 1245: the full system running), previous design or architectural decisions are proba-
Line 1246: bly preventing you from writing unit tests. How you design your classes has a
Line 1247: significant impact on how easy it is to write unit tests for your code. We discuss
Line 1248: design for testability in chapter 7.
Line 1249: I use integration tests whenever the component under test interacts with an external
Line 1250: component (such as a database or web service). A DAO, whose sole responsibility is to
Line 1251: communicate with a database, is better tested at the integration level: you want to
Line 1252: ensure that communication with the database works, the SQL query returns what you
Line 1253: want it to, and transactions are committed to the database. Again, note that integration
Line 1254: tests are more expensive and harder to set up than unit tests, and I use them only
Line 1255: because they are the only way to test a particular part of the system. Chapter 7 discusses
Line 1256: how having a clear separation between business rules and infrastructure code will help
Line 1257: you test business rules with unit tests and integration code with integration tests.
Line 1258:  As we know already, system tests are very costly (they are difficult to write and slow
Line 1259: to run) and, thus, at the top of the pyramid. It is impossible to retest the entire system
Line 1260: at the system level. Therefore, I have to prioritize what to test at this level, and I per-
Line 1261: form a simple risk analysis to decide. What are the critical parts of the software system
Line 1262: 
Line 1263: --- 페이지 53 ---
Line 1264: 25
Line 1265: The testing pyramid, and where we should focus
Line 1266: under test? In other words, what parts of the system would be significantly affected by
Line 1267: a bug? These are the areas where I do some system testing.
Line 1268:  Remember the pesticide paradox: a single technique usually is not enough to iden-
Line 1269: tify all the bugs. Let me give you a real-world example from one of my previous proj-
Line 1270: ects. In developing an e-learning platform, one of our most important functionalities
Line 1271: was payment. The worst type of bug would prevent users from buying our product.
Line 1272: Therefore, we were rigorous in testing all the code related to payment. We used unit
Line 1273: tests for business rules related to what the user bought being converted into the right
Line 1274: product, access and permissions, and so on. Integration with the two payment gate-
Line 1275: ways we supported was tested via integration testing: the integration tests made real
Line 1276: HTTP calls to a sandbox web service provided by the payment gateways, and we tested
Line 1277: different types of users buying products with various credit cards. Finally, our system
Line 1278: tests represented the entire user journey in buying our product. These tests started a
Line 1279: Firefox browser, clicked HTML elements, submitted forms, and checked that the right
Line 1280: product was available after confirming payment.
Line 1281:  Figure 1.8 also includes manual testing. I’ve said that every test should be auto-
Line 1282: mated, but I see some value in manual testing when these tests focus on exploration
Line 1283: and validation. As a developer, it is nice to use and explore the software system you are
Line 1284: building from time to time, both for real and via a test script. Open the browser or the
Line 1285: app, and play with it—you may gain better insight into what else to test. 
Line 1286: 1.4.7
Line 1287: What if you disagree with the testing pyramid?
Line 1288: Many people disagree about the idea of a testing pyramid and whether we should
Line 1289: favor unit testing. These developers argue for the testing trophy: a thinner bottom level
Line 1290: with unit tests, a bigger middle slice with integration tests, and a thinner top with sys-
Line 1291: tem tests. Clearly, these developers see the most value in writing integration tests.
Line 1292:  While I disagree, I see their point. In many software systems, most of the complex-
Line 1293: ity is in integrating components. Think of a highly distributed microservices architec-
Line 1294: ture: in such a scenario, the developer may feel more comfortable if the automated
Line 1295: tests make actual calls to other microservices instead of relying on stubs or mocks that
Line 1296: simulate them. Why write unit tests for something you have to test anyway via integra-
Line 1297: tion tests?
Line 1298:  In this particular case, as someone who favors unit testing, I would prefer to tackle
Line 1299: the microservices testing problem by first writing lots and lots of unit tests in each micro-
Line 1300: service to ensure that they all behaved correctly, investing heavily in contract design to
Line 1301: ensure that the microservices had clear pre- and post-conditions. Then, I would use
Line 1302: many integration tests to ensure that communication worked as expected and that the
Line 1303: normal variations in the distributed system did not break the system—yes, lots of them,
Line 1304: because their benefits would outweigh their costs in this scenario. I might even invest in
Line 1305: some smart (maybe AI-driven) tests to explore corner cases I could not see.
Line 1306:  Another common case I see in favor of integration testing rather than unit test-
Line 1307: ing involves database-centric information systems: that is, systems where the main
Line 1308: 
Line 1309: --- 페이지 54 ---
Line 1310: 26
Line 1311: CHAPTER 1
Line 1312: Effective and systematic software testing
Line 1313: responsibility is to store, retrieve, and display information. In such systems, the com-
Line 1314: plexity relies on ensuring that the flow of information successfully travels through the
Line 1315: UI to the database and back. Such applications often are not composed of complex
Line 1316: algorithms or business rules. In that case, integration tests to ensure that SQL queries
Line 1317: (which are often complex) work as expected and system tests to ensure that the over-
Line 1318: all application behaves as expected may be the way to go. As I said before and will say
Line 1319: many times in this book, context is king.
Line 1320:  I’ve written most of this section in the first person because it reflects my point of view
Line 1321: and is based on my experience as a developer. Favoring one approach over another is
Line 1322: largely a matter of personal taste, experience, and context. You should do the type of
Line 1323: testing you believe will benefit your software. I am not aware of any scientific evidence
Line 1324: that argues in favor of or against the testing pyramid. And in 2020, Trautsch and col-
Line 1325: leagues analyzed the fault detection capability of 30,000 tests (some unit tests, some
Line 1326: integration tests) and could not find any evidence that certain defect types are more
Line 1327: effectively detected by either test level. All the approaches have pros and cons, and you
Line 1328: will have to find what works best for you and your development team.
Line 1329:  I suggest that you read the opinions of others, both in favor of unit testing and in
Line 1330: favor of integration testing:
Line 1331: In Software Engineering at Google (Winters, Manshreck, and Wright, 2020), the
Line 1332: authors mention that Google often opts for unit tests, as they tend to be
Line 1333: cheaper and execute more quickly. Integration and system tests also happen,
Line 1334: but to a lesser extent. According to the authors, around 80% of their tests are
Line 1335: unit tests.
Line 1336: Ham Vocke (2018) defends the testing pyramid in Martin Fowler’s wiki.
Line 1337: Fowler himself (2021) discusses the different test shapes (testing pyramid and
Line 1338: testing trophy).
Line 1339: André Schaffer (2018) discusses how Spotify prefers integration testing over
Line 1340: unit testing.
Line 1341: Julia Zarechneva and Picnic, a scale-up Dutch company (2021), reason about
Line 1342: the testing pyramid.
Line 1343: TEST SIZES RATHER THAN THEIR SCOPE
Line 1344: Google also has an interesting definition of test sizes, which engineers consider when
Line 1345: designing test cases. A small test is a test that can be executed in a single process. Such
Line 1346: tests do not have access to main sources of test slowness or determinism. In other
Line 1347: words, they are fast and not flaky. A medium test can span multiple processes, use threads,
Line 1348: and make external calls (like network calls) to localhost. Medium tests tend to be
Line 1349: slower and flakier than small ones. Finally, large tests remove the localhost restriction
Line 1350: and can thus require and make calls to multiple machines. Google reserves large tests
Line 1351: for full end-to-end tests.
Line 1352:  The idea of classifying tests not in terms of their boundaries (unit, integration, sys-
Line 1353: tem) but in terms of how fast they run is also popular among many developers. Again,
Line 1354: 
Line 1355: --- 페이지 55 ---
Line 1356: 27
Line 1357: Exercises
Line 1358: what matters is that for each part of the system, your goal is to maximize the effective-
Line 1359: ness of the test. You want your test to be as cheap as possible to write and as fast as pos-
Line 1360: sible to run and to give you as much feedback as possible about the system’s quality.
Line 1361:  Most of the code examples in the remainder of this book are about methods,
Line 1362: classes, and unit testing, but the techniques can easily be generalized to coarse-
Line 1363: grained components. For example, whenever I show a method, you can think of it as a
Line 1364: web service. The reasoning will be the same, but you will probably have more test cases
Line 1365: to consider, as your component will do more things. 
Line 1366: 1.4.8
Line 1367: Will this book help you find all the bugs?
Line 1368: I hope the answer to this question is clear from the preceding discussion: no! Never-
Line 1369: theless, the techniques discussed in this book will help you discover many bugs—
Line 1370: hopefully, all the important ones.
Line 1371:  In practice, many bugs are very complex. We do not even have the right tools to
Line 1372: search for some of them. But we know a lot about testing and how to find different
Line 1373: classes of bugs, and those are the ones we focus on in this book. 
Line 1374: Exercises
Line 1375: 1.1
Line 1376: In your own words, explain what systematic testing is and how it is different
Line 1377: from non-systematic testing.
Line 1378: 1.2
Line 1379: Kelly, a very experienced software tester, visits Books!, a social network focused
Line 1380: on matching people based on the books they read. Users do not report bugs
Line 1381: often, as the Books! developers have strong testing practices in place. However,
Line 1382: users say that the software is not delivering what it promises. What testing prin-
Line 1383: ciple applies here?
Line 1384: 1.3
Line 1385: Suzanne, a junior software tester, has just joined a very large online payment
Line 1386: company in the Netherlands. As her first task, Suzanne analyzes the past two
Line 1387: years’ worth of bug reports. She observes that more than 50% of the bugs hap-
Line 1388: pen in the international payments module. Suzanne promises her manager that
Line 1389: she will design test cases that completely cover the international payments mod-
Line 1390: ule and thus find all the bugs.
Line 1391: Which of the following testing principles may explain why this is not possible?
Line 1392: A Pesticide paradox
Line 1393: B Exhaustive testing
Line 1394: C Test early
Line 1395: D Defect clustering
Line 1396: 1.4
Line 1397: John strongly believes in unit testing. In fact, this is the only type of testing he does
Line 1398: for any project he’s part of. Which of the following testing principles will not help
Line 1399: convince John that he should move away from his “only unit testing” approach?
Line 1400: A Pesticide paradox
Line 1401: B Tests are context-dependent
Line 1402: 
Line 1403: --- 페이지 56 ---
Line 1404: 28
Line 1405: CHAPTER 1
Line 1406: Effective and systematic software testing
Line 1407: C Absence-of-errors fallacy
Line 1408: D Test early
Line 1409: 1.5
Line 1410: Sally just started some consultancy for a company that develops a mobile app to
Line 1411: help people keep up with their daily exercises. The development team mem-
Line 1412: bers are fans of automated software testing and, more specifically, unit tests.
Line 1413: They have high unit test code coverage (>95% branch coverage), but users still
Line 1414: report a significant number of bugs.
Line 1415: Sally, who is well versed in software testing, explains a testing principle to the
Line 1416: team. Which of the following principles did she talk about?
Line 1417: A Pesticide paradox
Line 1418: B Exhaustive testing
Line 1419: C Test early
Line 1420: D Defect clustering
Line 1421: 1.6
Line 1422: Consider this requirement: “A web shop runs a batch job, once a day, to deliver all
Line 1423: orders that have been paid. It also sets the delivery date according to whether the
Line 1424: order is from an international customer. Orders are retrieved from an external
Line 1425: database. Orders that have been paid are then sent to an external web service.”
Line 1426: As a tester, you have to decide which test level (unit, integration, or system)
Line 1427: to apply. Which of the following statements is true?
Line 1428: A Integration tests, although more complicated (in terms of automation)
Line 1429: than unit tests, would provide more help in finding bugs in the communi-
Line 1430: cation with the web service and/or the communication with the database.
Line 1431: B Given that unit tests could be easily written (by using mocks) and would
Line 1432: cover as much as integration tests would, unit tests are the best option for
Line 1433: any situation.
Line 1434: C The most effective way to find bugs in this code is through system tests. In
Line 1435: this case, the tester should run the entire system and exercise the batch
Line 1436: process. Because this code can easily be mocked, system tests would also
Line 1437: be cheap.
Line 1438: D While all the test levels can be used for this problem, testers are more
Line 1439: likely to find more bugs if they choose one level and explore all the possi-
Line 1440: bilities and corner cases there.
Line 1441: 1.7
Line 1442: Delft University of Technology (TU Delft) has built in-house software to handle
Line 1443: employee payroll. The application uses Java web technologies and stores data in
Line 1444: a Postgres database. The application frequently retrieves, modifies, and inserts
Line 1445: large amounts of data. All this communication is done by Java classes that send
Line 1446: (complex) SQL queries to the database.
Line 1447: As testers, we know that a bug can be anywhere, including in the SQL que-
Line 1448: ries. We also know that there are many ways to exercise our system. Which one
Line 1449: of the following is not a good option to detect bugs in SQL queries?
Line 1450: 
Line 1451: --- 페이지 57 ---
Line 1452: 29
Line 1453: Summary
Line 1454: A Unit testing
Line 1455: B Integration testing
Line 1456: C System testing
Line 1457: D Stress testing
Line 1458: 1.8
Line 1459: Choosing the level of a test involves a trade-off, because each test level has
Line 1460: advantages and disadvantages. Which one of the following is the main advan-
Line 1461: tage of a test at the system level?
Line 1462: A The interaction with the system is much closer to reality.
Line 1463: B In a continuous integration environment, system tests provide real feed-
Line 1464: back to developers.
Line 1465: C Because system tests are never flaky, they provide developers with more
Line 1466: stable feedback.
Line 1467: D A system test is written by product owners, making it closer to reality.
Line 1468: 1.9
Line 1469: What is the main reason the number of recommended system tests in the test-
Line 1470: ing pyramid is smaller than the number of unit tests?
Line 1471: A Unit tests are as good as system tests.
Line 1472: B System tests tend to be slow and are difficult to make deterministic.
Line 1473: C There are no good tools for system tests.
Line 1474: D System tests do not provide developers with enough quality feedback. 
Line 1475: Summary
Line 1476: Testing and test code can guide you through software development. But soft-
Line 1477: ware testing is about finding bugs, and that is what this book is primarily about.
Line 1478: Systematic and effective software testing helps you design test cases that exer-
Line 1479: cise all the corners of your code and (hopefully) leaves no space for unex-
Line 1480: pected behavior.
Line 1481: Although being systematic helps, you can never be certain that a program does
Line 1482: not have bugs.
Line 1483: Exhaustive testing is impossible. The life of a tester involves making trade-offs
Line 1484: about how much testing is needed.
Line 1485: You can test programs on different levels, ranging from testing small methods
Line 1486: to testing entire systems with databases and web services. Each level has advan-
Line 1487: tages and disadvantages.