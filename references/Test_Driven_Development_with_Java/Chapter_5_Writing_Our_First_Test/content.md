Line 1: 
Line 2: --- 페이지 78 ---
Line 3: 5
Line 4: Writing Our First Test
Line 5: It’s time for us to dive in and write our first TDD unit test in this chapter. To help us do this, we will 
Line 6: learn about a simple template that helps us organize each test into a logical, readable piece of code. 
Line 7: Along the way, we will learn some key principles we can use to make our tests effective. We will see 
Line 8: how writing the test first forces us to make decisions about the design of our code and its ease of use, 
Line 9: before needing to think about implementation details.
Line 10: After some examples covering those techniques, we will make a start on our Wordz application, writing 
Line 11: a test first before adding production code to make that test pass. We will use the popular Java unit 
Line 12: testing libraries JUnit5 and AssertJ to help us write easy-to-read tests.
Line 13: In this chapter, we will cover the following main principles behind writing effective unit tests:
Line 14: •	 Starting TDD: Arrange-Act-Assert
Line 15: •	 Defining a good test
Line 16: •	 Catching common errors
Line 17: •	 Asserting exceptions
Line 18: •	 Only testing public methods
Line 19: •	 Learning from our tests
Line 20: •	 Beginning Wordz – our first test
Line 21: Technical requirements
Line 22: The final code in this chapter can be found at https://github.com/PacktPublishing/
Line 23: Test-Driven-Development-with-Java/tree/main/chapter05.
Line 24: 
Line 25: --- 페이지 79 ---
Line 26: Writing Our First Test
Line 27: 56
Line 28: Starting TDD: Arrange-Act-Assert
Line 29: Unit tests are nothing mysterious. They’re just code, executable code written in the same language 
Line 30: that you write your application in. Each unit test forms the first use of the code you want to write. It 
Line 31: calls the code just as it will be called in the real application. The test executes that code, captures all 
Line 32: the outputs that we care about, and checks that they are what we expected them to be. Because the 
Line 33: test uses our code in the exact same way that the real application will, we get instant feedback on 
Line 34: how easy or difficult our code is to use. This might sound obvious, and it is, but it is a powerful tool 
Line 35: to help us write clean and correct code. Let’s take a look at an example of a unit test and learn how 
Line 36: to define its structure.
Line 37: Defining the test structure
Line 38: It’s always helpful to have templates to follow when we do things and unit tests are no exception. 
Line 39: Based on commercial work done on the Chrysler Comprehensive Compensation Project, TDD 
Line 40: inventor Kent Beck found that unit tests had certain features in common. This became summarized 
Line 41: as a recommended structure for test code, called Arrange-Act-Assert or AAA.
Line 42: The original definition of AAA
Line 43: The original description of AAA can be found here, in the C2 wiki: http://wiki.
Line 44: c2.com/?ArrangeActAssert.
Line 45: To explain what each section does, let’s walk through a completed unit test for a piece of code where 
Line 46: we want to ensure that a username is displayed in lowercase:
Line 47: import org.junit.jupiter.api.Test;
Line 48: import static org.assertj.core.api.Assertions.*;
Line 49: public class UsernameTest {
Line 50:     @Test
Line 51:     public void convertsToLowerCase() {
Line 52:         var username = new Username("SirJakington35179");
Line 53:         String actual = username.asLowerCase();
Line 54:         assertThat(actual).isEqualTo("sirjakington35179");
Line 55:     }
Line 56: }
Line 57: 
Line 58: --- 페이지 80 ---
Line 59: Starting TDD: Arrange-Act-Assert
Line 60: 57
Line 61: The first thing to notice is the class name for our test: UsernameTest. This is the first piece of 
Line 62: storytelling for readers of our code. We are describing the behavioral area we are testing, in this case, 
Line 63: usernames. All our tests, and indeed all our code, should follow this storytelling approach: what do 
Line 64: we want the readers of our code to understand? We want them to clearly see what the problem that 
Line 65: we are solving is and how the code that solves it should be used. We want to demonstrate to them 
Line 66: that the code works correctly.
Line 67: The unit test itself is the convertsToLowerCase() method. Again, the name describes what 
Line 68: we expect to happen. When the code runs successfully, the username will be converted to lowercase. 
Line 69: The names are intentionally simple, clear, and descriptive. This method has the @Test annotation 
Line 70: from the JUnit5 test framework. The annotation tells JUnit that this is a test that it can run for us.
Line 71: Inside the @Test method, we can see our Arrange-Act-Assert structure. We first arrange for our 
Line 72: code to be able to run. This involves creating any objects required, supplying any configuration 
Line 73: needed, and connecting any dependent objects and functions. Sometimes, we do not need this step, 
Line 74: for example, if we are testing a simple standalone function. In our example code, the Arrange step is 
Line 75: the line that creates the username object and supplies a name to the constructor. It then stores that 
Line 76: object ready to use in the local username variable. It is the first line of the var username = 
Line 77: new Username("SirJakington35179"); test method body.
Line 78: The Act step follows. This is the part where we cause our code under test to act – we run that code. This 
Line 79: is always a call to the code under test, supplying any necessary parameters, and arranging to capture 
Line 80: the results. In the example, the String actual = username.asLowerCase(); line is the 
Line 81: Act step. We call the asLowerCase() method on our username object. It takes no parameters and 
Line 82: returns a simple String object containing the lowercase text sirjakington35179 as a result.
Line 83: Completing our test is the final Assert step. The a s s e r t T h a t ( a c t u a l ) .
Line 84: isEqualTo("sirjakington35179"); line is our Assert step here. It uses the assertThat() 
Line 85: method and the isEqualTo() method from the AssertJ fluent assertions library. Its job is to 
Line 86: check whether the result we returned from the Act step matches our expectations or not. Here, we 
Line 87: are testing whether all the uppercase letters in the original name have been converted to lowercase.
Line 88: Unit tests like this are easy to write, easy to read, and they run very quickly. Many such tests can run 
Line 89: in under 1 second.
Line 90: The JUnit library is the industry-standard unit test framework for Java. It provides us with a means 
Line 91: to annotate Java methods as unit tests, lets us run all our tests, and visually displays the results, as 
Line 92: shown here in the IntelliJ IDE window:
Line 93: 
Line 94: --- 페이지 81 ---
Line 95: Writing Our First Test
Line 96: 58
Line 97: Figure 5.1 – Output from the JUnit test runner
Line 98: We see here that the unit test failed. The test expected the result to be the sirjakington35179 
Line 99: text string but instead, we received null. Using TDD, we would complete just enough code to make 
Line 100: that test pass:
Line 101: Figure 5.2 – A JUnit test pass
Line 102: We can see that our change to the production code has made this test pass. It has gone green, to use 
Line 103: the popular term. Tests that fail are described as red tests and those that pass are green. This is based 
Line 104: on the colors shown in popular IDEs, which are based on traffic signals in turn. Seeing all these short 
Line 105: iterations of red tests turning to green is surprisingly satisfying, as well as building confidence in our 
Line 106: work. The tests help us focus on the design of our code by forcing us to work backward from outcomes. 
Line 107: Let’s look at what this means.
Line 108: Working backward from outcomes
Line 109: One thing we notice right away is just how unimportant the actual code that makes this test pass is. 
Line 110: Everything in this test is about defining the expectations of that code. We are setting boundaries around 
Line 111: why our code is useful and what we expect it to do. We are not constraining how it does it in any way. 
Line 112: We are taking an outside-in view of code. Any implementation that makes our test pass is acceptable.
Line 113: 
Line 114: --- 페이지 82 ---
Line 115: Defining a good test
Line 116: 59
Line 117: This seems to be a transition point in learning to use TDD. Many of us learned to program by writing 
Line 118: implementations first. We thought about how the code would work. We went deep into the algorithms 
Line 119: and data structures behind a specific implementation. Then, as a last thought, we wrapped it all up 
Line 120: in some kind of callable interface.
Line 121: TDD turns this on its head. We intentionally design our callable interface first, as this is what the users 
Line 122: of that code will see. We use the test to precisely describe how the code will be set up, how it will be 
Line 123: called, and what we can expect it to do for us. Once we get used to doing this outside-in design first, 
Line 124: TDD follows very naturally and improves our workflow efficiency in several important ways. Let’s 
Line 125: review what these improvements are.
Line 126: Increasing workflow efficiency
Line 127: Unit tests like these increase our efficiency as developers in several ways. The most obvious is that the 
Line 128: code we write has passed a test: we know it works. We are not waiting around for a manual QA process 
Line 129: to find a defect and then raise a bug report for rework in the future. We find and fix bugs now, before 
Line 130: ever releasing them into the main source trunk, let alone to users. We have documented our intentions 
Line 131: for our colleagues. If anyone wants to know how our Username class works, it is right there in the 
Line 132: test – how you create the object, which methods you can call, and what we expect the outcomes to be.
Line 133: Unit tests give us a way to run code in isolation. We are no longer forced to rebuild a whole application, 
Line 134: run it, set up test data entries in our database, log in to the user interface, navigate to the correct screen, 
Line 135: and then visually inspect the output of our code. We run the test. That’s it. This allows us to execute 
Line 136: code that is not yet fully integrated into our application’s main trunk. This speeds up our work. We 
Line 137: can get started more quickly, spend more time on developing the code at hand, and spend less time 
Line 138: on cumbersome manual testing and deployment processes.
Line 139: A further benefit is that this act of design improves the modularity of our code. By designing code that 
Line 140: can be tested in small pieces, we remind ourselves to write code that can execute in small pieces. That 
Line 141: has been the basic approach to design since the 1960s and remains as effective today as it ever was.
Line 142: This section has covered the standard structure that we use to organize every unit test but it doesn’t 
Line 143: guarantee that we will write a good test. To achieve this, each test needs to have particular properties. 
Line 144: The FIRST principles describe the properties of a good test. Let’s learn how to apply these next.
Line 145: Defining a good test
Line 146: Like all code, unit test code can be written in better or worse ways. We’ve seen how AAA helps us 
Line 147: structure a test correctly and how accurate, descriptive names tell the story of what we intend our code 
Line 148: to do. The most useful tests also follow the FIRST principles and use one assert per test.
Line 149: 
Line 150: --- 페이지 83 ---
Line 151: Writing Our First Test
Line 152: 60
Line 153: Applying the FIRST principles
Line 154: These are a set of five principles that make tests more effective:
Line 155: •	 Fast
Line 156: •	 Isolated
Line 157: •	 Repeatable
Line 158: •	 Self-verifying
Line 159: •	 Timely
Line 160: Unit tests need to be fast, just as our earlier example was. This is especially important for test-first 
Line 161: TDD, as we want that immediate feedback while we explore our design and implementation. If we 
Line 162: run a unit test, and it takes even as little as 15 seconds to complete, we will soon stop running tests as 
Line 163: often. We will degenerate into writing big chunks of production code without tests so that we spend 
Line 164: less time waiting for slow tests to finish. This is the exact opposite of what we want from TDD, so we 
Line 165: work hard to keep tests fast. We need unit tests to run in 2 seconds or less, ideally milliseconds. Even 
Line 166: two seconds is really quite a high number.
Line 167: Tests need to be isolated from one another. This means that we can pick any test or any combination 
Line 168: of tests and run them in any order we like and always get the same result. One test must not depend 
Line 169: on another test having been run before it. This is often a symptom of failing to write fast tests, so we 
Line 170: compensate by caching results or arranging step setups. This is a mistake, as it slows down development, 
Line 171: especially for our colleagues. The reason is that we don’t know the special order in which the tests 
Line 172: must run. When we run any test on its own, and if it has not been properly isolated, it will fail as a 
Line 173: false negative. That test no longer tells us anything about our code under test. It only tells us that we 
Line 174: have not run some other test before it, without telling us which test that might be. Isolation is critical 
Line 175: to a healthy TDD workflow.
Line 176: Repeatable tests are vital to TDD. Whenever we run a test with the same production code, that test 
Line 177: must always return the same pass or fail result. This might sound obvious but care needs to be taken 
Line 178: to achieve this. Think about a test that checks a function that returns a random number between 1 
Line 179: and 10. If we assert that the number seven is returned, this test will only pass occasionally, even if we 
Line 180: have correctly coded the function. In this regard, three popular sources of misery are tests involving 
Line 181: the database, tests against time, and tests through the user interface. We will explore techniques to 
Line 182: handle these situations in Chapter 8, Test Doubles –Stubs and Mocks.
Line 183: All tests must be self-verifying. This means we need executable code to run and check whether the 
Line 184: outputs are as expected. This step must be automated. We must not leave this check to manual inspection, 
Line 185: perhaps by writing the output to a console and having a human check it against a test plan. Unit tests 
Line 186: derive huge value from being automated. The computer checks the production code, freeing us from 
Line 187: the tedium of following a test plan, the slowness of human activities, and the likelihood of human error.
Line 188: 
Line 189: --- 페이지 84 ---
Line 190: Defining a good test
Line 191: 61
Line 192: Timely tests are tests written at just the right time to be most useful. The ideal time to write a test is 
Line 193: just before writing the code that makes that test pass. It’s not unusual to see teams use less beneficial 
Line 194: approaches. The worst one, of course, is to never write any unit tests and rely on manual QA to find 
Line 195: bugs. With this approach, we get none of the design feedback available. The other extreme is to have an 
Line 196: analyst write every test for the component – or even the whole system – upfront, leaving the coding as 
Line 197: a mechanical exercise. This also fails to learn from design feedback. It can also result in overspecified 
Line 198: tests that lock in poor design and implementation choices. Many teams start by writing some code 
Line 199: and then go on to write a unit test, thereby missing out on an opportunity for early design feedback. 
Line 200: It can also lead to untested code and faulty edge case handling.
Line 201: We’ve seen how the FIRST principles help us focus on crafting a good test. Another important principle 
Line 202: is not to try to test too much all at once. If we do, the test becomes very difficult to understand. A 
Line 203: simple solution to this is to write a single assert per test, which we will cover next.
Line 204: Using one assert per test
Line 205: Tests provide the most useful feedback when they are short and specific. They act as a microscope 
Line 206: working on the code, each test highlighting one small aspect of our code. The best way to ensure this 
Line 207: happens is by writing one assertion per test. This prevents us from tackling too much in one test. This 
Line 208: focuses on the error messages we get during test failures and helps us control the complexity of our 
Line 209: code. It forces us to break things down a little further.
Line 210: Deciding on the scope of a unit test
Line 211: Another common misunderstanding is what a unit means in a unit test. The unit refers to the test 
Line 212: isolation itself – each test can be considered a standalone unit. As a result, the size of the code under 
Line 213: test can vary a lot, as long as that test can run in isolation.
Line 214: Thinking of the test itself as the unit unifies several popular opinions about what the scope of a 
Line 215: unit test should be. Often, it is said that the unit is the smallest piece of testable code – a function, 
Line 216: method, class, or package. All of these are valid options. Another common argument is that a unit 
Line 217: test should be a class test – one unit test class per production code class, with one unit test method 
Line 218: per production method. While common, this isn’t usually the best approach. It unnecessarily couples 
Line 219: the structure of the test to the structure of the implementation, making the code harder to change in 
Line 220: the future, not easier.
Line 221: The ideal goal of a unit test is to cover one externally visible behavior. This applies at several different 
Line 222: scales in the code base. We can unit test an entire user story across multiple packages of classes, 
Line 223: provided we can avoid manipulating external systems such as a database or the user interface. We’ll 
Line 224: look into techniques for doing that in Chapter 9, Hexagonal Architecture – Decoupling External Systems. 
Line 225: We often also use unit tests that are closer to the details of the code, testing only the public methods 
Line 226: of a single class.
Line 227: 
Line 228: --- 페이지 85 ---
Line 229: Writing Our First Test
Line 230: 62
Line 231: Once we have written our test based on the design that we would like our code to have, we can 
Line 232: concentrate on the more obvious aspect of testing: verifying that our code is correct.
Line 233: Catching common errors
Line 234: The traditional view of testing is of it as a process to check that code works as it is intended to work. 
Line 235: Unit tests excel at this and automate the process of running the code with known inputs and checking 
Line 236: for expected outputs. As we are human, all of us make mistakes from time to time as we write code 
Line 237: and some of these can have significant impacts. There are several common simple mistakes we can 
Line 238: make and unit tests excel at catching them all. The most likely errors are the following:
Line 239: •	 Off-by-one errors
Line 240: •	 Inverted conditional logic
Line 241: •	 Missing conditions
Line 242: •	 Uninitialized data
Line 243: •	 The wrong algorithm
Line 244: •	 Broken equality checks
Line 245: As an example, going back to our earlier test for a lowercase username, suppose we decided not to 
Line 246: implement this using the String built-in .toLowerCase() method, but instead tried to roll 
Line 247: our own loop code, like this:
Line 248: public class Username {
Line 249:     private final String name;
Line 250:     public Username(String username) {
Line 251:         name = username;
Line 252:     }
Line 253:     public String asLowerCase() {
Line 254:         var result = new StringBuilder();
Line 255:         for (int i=1; i < name.length(); i++) {
Line 256:             char current = name.charAt(i);
Line 257:             if (current > 'A' && current < 'Z') {
Line 258:                 result.append(current + 'a' - 'A');
Line 259:             } else {
Line 260:                 result.append( current );
Line 261: 
Line 262: --- 페이지 86 ---
Line 263: Asserting exceptions
Line 264: 63
Line 265:             }
Line 266:         }
Line 267:         return result.toString() ;
Line 268:     }
Line 269: }
Line 270: We would see right away that this code isn’t correct. The test fails, as shown in the following figure:
Line 271: Figure 5.3 – A common coding error
Line 272: The first error in this code is a simple off-by-one error – the first letter is missing from the output. 
Line 273: That points to an error in initializing our loop index but there are other errors in this code as well. 
Line 274: This test reveals two defects. Further tests would reveal two more. Can you see what they are by visual 
Line 275: inspection alone? How much more time and effort is it to analyze code like this in our heads, rather 
Line 276: than using automated tests?
Line 277: Asserting exceptions
Line 278: One area where unit tests excel is in testing error handling code. As an example of testing exception 
Line 279: throwing, let’s add a business requirement that our usernames must be at least four characters long. 
Line 280: We think about the design we want and decide to throw a custom exception if the name is too short. 
Line 281: We decide to represent this custom exception as class InvalidNameException. Here’s what 
Line 282: the test looks like, using AssertJ:
Line 283: @Test
Line 284: public void rejectsShortName() {
Line 285:     assertThatExceptionOfType(InvalidNameException.class)
Line 286:             .isThrownBy(()->new Username("Abc"));
Line 287: }
Line 288: 
Line 289: --- 페이지 87 ---
Line 290: Writing Our First Test
Line 291: 64
Line 292: We can consider adding another test specifically aimed at proving that a name of four characters is 
Line 293: accepted and no exception is thrown:
Line 294: @Test
Line 295: public void acceptsMinimumLengthName() {
Line 296:     assertThatNoException()
Line 297:             .isThrownBy(()->new Username("Abcd"));
Line 298: }
Line 299: Alternatively, we may simply decide that this explicit test is not needed. We may cover it implicitly 
Line 300: with other tests. It is a good practice to add both tests to make our intentions clear.
Line 301: The test names are fairly general, starting with either rejects or accepts. They describe the 
Line 302: outcome that the code is being tested for. This allows us to change our minds about the error handling 
Line 303: mechanics later, perhaps switching to something other than exceptions to signal the error.
Line 304: Unit tests can catch common programming errors and verify error handling logic. Let’s look at a major 
Line 305: principle of writing our unit tests to give us maximum flexibility when implementing our methods.
Line 306: Only testing public methods
Line 307: TDD is all about testing the behaviors of components, not their implementations. As we have seen 
Line 308: in our test in the previous section, having a test for the behavior we want enables us to choose any 
Line 309: implementation that will do the job. We focus on what’s important – what a component does – not 
Line 310: on the less important details – how it does it.
Line 311: Inside a test, this appears as calling public methods or functions on public classes and packages. The 
Line 312: public methods are the behaviors we choose to expose to the wider application. Any private data or 
Line 313: supporting code in classes, methods, or functions remain hidden.
Line 314: A common mistake that developers make when learning TDD is that they make things public just 
Line 315: to simplify testing. Resist the temptation. A typical mistake here is to take a private data field and 
Line 316: expose it for testing using a public getter method. This weakens the encapsulation of that class. It is 
Line 317: now more likely that the getter will be misused. Future developers may add methods to other classes 
Line 318: that really belong in this one. The design of our production code is important. Fortunately, there is a 
Line 319: simple way of preserving encapsulation without compromising testing.
Line 320: Preserving encapsulation
Line 321: If we feel we need to add getters to all our private data so that the test can check that each one is as 
Line 322: expected, it is often better to treat this as a value object. A value object is an object that lacks identity. 
Line 323: Any two value objects that contain the same data are considered to be equal. Using value objects, we 
Line 324: can make another object containing the same private data and then test that the two objects are equal.
Line 325: 
Line 326: --- 페이지 88 ---
Line 327: Learning from our tests
Line 328: 65
Line 329: In Java, this requires us to code a custom equals() method for our class. If we do this, we should also 
Line 330: code a hashcode() method, as the two go hand in hand. Any implementation that works will do. I 
Line 331: recommend using the Apache commons3 library, which uses Java reflection capabilities to do this:
Line 332: @Override
Line 333: public boolean equals(Object other) {
Line 334:     return EqualsBuilder.reflectionEquals(this, other);
Line 335: }
Line 336: @Override
Line 337: public int hashCode() {
Line 338:     return HashCodeBuilder.reflectionHashCode(this);
Line 339: }
Line 340: You can find out more about these library methods at https://commons.apache.org/
Line 341: proper/commons-lang/.
Line 342: Simply adding those two methods (and the Apache commons3 library) to our class means that we 
Line 343: can keep all our data fields private and still check that all the fields have the expected data in them. 
Line 344: We simply create a new object with all the expected fields, then assert that it is equal to the object we 
Line 345: are testing.
Line 346: As we write each test, we are using the code under test for the first time. This allows us to learn a lot 
Line 347: about how easy our code is to use, allowing us to make changes if we need to.
Line 348: Learning from our tests
Line 349: Our tests are a rich source of feedback on our design. As we make decisions, we write them as test 
Line 350: code. Seeing this code – the first usage of our production code – brings into sharp focus how good 
Line 351: our proposed design is. When our design isn’t good, the AAA sections of our test will reveal those 
Line 352: design issues as code smells in the test. Let’s try to understand in detail how each of these can help 
Line 353: identify a faulty design.
Line 354: A messy Arrange step
Line 355: If the code in our Arrange step is messy, our object may be difficult to create and configure. It may 
Line 356: need too many parameters in a constructor or too many optional parameters left as null in the 
Line 357: test. It may be that the object needs too many dependencies injected, indicating that it has too many 
Line 358: responsibilities or it might need too many primitive data parameters to pass in a lot of configuration 
Line 359: items. These are signals that the way we create our object might benefit from a redesign.
Line 360: 
Line 361: --- 페이지 89 ---
Line 362: Writing Our First Test
Line 363: 66
Line 364: A messy Act step
Line 365: Calling the main part of the code in the Act step is usually straightforward but it can reveal some 
Line 366: basic design errors. For example, we might have unclear parameters that we pass in, signatures such 
Line 367: as a list of Boolean or String objects. It is very hard to know what each one means. We could 
Line 368: redesign this by wrapping those difficult parameters in an easy-to-understand new class, called a 
Line 369: configuration object. Another possible problem is if the Act step requires multiple calls to be made 
Line 370: in a specific order. That is error-prone. It is easy to call them in the wrong order or forget one of the 
Line 371: calls. We could redesign to use a single method that wraps all of this detail.
Line 372: A messy Assert step
Line 373: The Assert step will reveal whether the results of our code are difficult to use. Problem areas might 
Line 374: include having to call accessors in a specific order or perhaps returning some conventional code 
Line 375: smells, such as an array of results where every index has a different meaning. We can redesign to use 
Line 376: safer constructs in either case.
Line 377: In each of these cases, one of the sections of code in our unit test looks wrong – it has a code smell. 
Line 378: That is because the design of the code we are testing has the same code smell. This is what is meant 
Line 379: by unit tests giving fast feedback on design. They are the first user of the code we are writing, so we 
Line 380: can identify problem areas early on.
Line 381: We now have all the techniques we need to start writing our first test for our example application. 
Line 382: Let’s make a start.
Line 383: Limitations of unit tests
Line 384: One very important idea is that an automated test can only prove the presence of a defect, not the 
Line 385: absence. What this means is that if we think of a boundary condition, write a test for that, and the test 
Line 386: fails, we know we have a defect in our logic. However, if all our tests pass, that does not and cannot mean 
Line 387: our code is free of defects. It only means that our code is free of all the defects that we have thought 
Line 388: to test for. There simply is no magic solution that can ensure our code is defect-free. TDD gives us 
Line 389: a significant boost in that direction but we must never claim our code is defect-free just because all 
Line 390: our tests pass. This is simply untrue.
Line 391: One important consequence of this is that our QA engineering colleagues remain as important as they 
Line 392: ever were,  although we now help them start from an easier standing point. We can deliver TDD-tested 
Line 393: code to our manual QA colleagues, and they can be assured that many defects have been prevented 
Line 394: and proven to be absent. This means that they can start work on manual exploratory testing, finding 
Line 395: all the things we never thought to test. Working together, we can use their defect reports to write 
Line 396: further unit tests to rectify what they find. The contribution of QA engineers remains vital, even with 
Line 397: TDD. We need all the help our team can get in our efforts to write high-quality software.
Line 398: 
Line 399: --- 페이지 90 ---
Line 400: Beginning Wordz
Line 401: 67
Line 402: Code coverage – an often-meaningless metric
Line 403: Code coverage is a measure of how many lines of code have been executed in a given run. It is 
Line 404: measured by instrumenting the code and this is something that a code coverage tool will do for us. 
Line 405: It is often used in conjunction with unit testing to measure how many lines of code were executed 
Line 406: while running the test suite.
Line 407: In theory, you can see how this might mean that missing tests can be discovered in a scientific way. If 
Line 408: we see that a line of code was not run, we must have a missing test somewhere. That is both true and 
Line 409: helpful but the converse is not true. Suppose we get 100% code coverage during our test run. Does 
Line 410: that mean the software is now completely tested and correct? No.
Line 411: Consider having a single test for an if (x < 2) statement. We can write a test that will cause this 
Line 412: line to execute and be included in code coverage reports. However, a single test is not enough to cover 
Line 413: all the possibilities of behavior. The conditional statement might have the wrong operator – less than 
Line 414: instead of less than or equal to. It might have the incorrect limit of 2 when it should be 20. Any single 
Line 415: test cannot fully explore the combinations of behavior in that statement. We can have code coverage 
Line 416: tell us that the line has been run and that our single test passed but we can still have several logic 
Line 417: errors remaining. We can have 100% code coverage and still have missing tests.
Line 418: Writing the wrong tests
Line 419: Time for a short personal story about how my best attempt at TDD went spectacularly wrong. In a 
Line 420: mobile application that calculated personal tax reports, there was a particular yes/no checkbox in 
Line 421: the app to indicate whether you had a student loan or not, since this affects the tax you pay. It had six 
Line 422: consequences in our application and I thoroughly TDD tested each one, carefully writing my tests first.
Line 423: Sadly, I had misread the user story. I had inverted every single test. Where the checkbox should apply 
Line 424: the relevant tax, it now did not apply it, and vice versa.
Line 425: This was thankfully picked up by our QA engineer. Her only comment was that she could find absolutely 
Line 426: no workaround in the system for this defect. We concluded that TDD had done an excellent job of 
Line 427: making the code do what I wanted it to do but I had done a rather less excellent job of figuring out 
Line 428: what that should be. At least it was a very quick fix and retest.
Line 429: Beginning Wordz
Line 430: Let’s apply these ideas to our Wordz application. We’re going to start with a class that will contain 
Line 431: the core of our application logic, one that represents a word to guess and that can work out the score 
Line 432: for a guess.
Line 433: We begin by creating a unit test class and this immediately puts us into software design mode: what 
Line 434: should we call the test? We’ll go with WordTest, as that outlines the area we want to cover – the 
Line 435: word to be guessed.
Line 436: 
Line 437: --- 페이지 91 ---
Line 438: Writing Our First Test
Line 439: 68
Line 440: Typical Java project structures are divided into packages. The production code lives under src/main/
Line 441: java and the test code is located under src/test/java. This structure describes how production 
Line 442: and test code are equally important parts of the source code, while giving us a way to compile and 
Line 443: deploy only the production code. We always ship test code with the production code when we are 
Line 444: dealing with source code, but for deployed executables, we only omit the tests. We will also follow the 
Line 445: basic Java package convention of having a unique name for our company or project at the top level. 
Line 446: This helps avoid clashes with library code. We’ll call ours com.wordz, named after the application.
Line 447: The next design step is to decide which behavior to drive out and test first. We always want a simple 
Line 448: version of a happy path, something that will help drive out the normal logic that will most commonly 
Line 449: execute. We can cover edge cases and error conditions later. To begin with, let’s write a test that will 
Line 450: return the score for a single letter that is incorrect:
Line 451: 1.	
Line 452: Write the following code to begin our test:
Line 453: public class WordTest {
Line 454:     @Test
Line 455:     public void oneIncorrectLetter() {
Line 456:     }
Line 457: }
Line 458: The name of the test gives us an overview of what the test is doing.
Line 459: 2.	
Line 460: To start our design, we decide to use a class called Word to represent our word. We also decide 
Line 461: to supply the word to guess as a constructor parameter to our object instance of class Word we 
Line 462: want to create. We code these design decisions into the test:
Line 463: @Test
Line 464: public void oneIncorrectLetter () {
Line 465:     new Word("A");
Line 466: }
Line 467: 3.	
Line 468: We use autocomplete at this point to create a new Word class in its own file. Double-check in 
Line 469: src/main folder tree and not src/test:
Line 470: 
Line 471: --- 페이지 92 ---
Line 472: Beginning Wordz
Line 473: 69
Line 474: Figure 5.4 – Creating a class dialog
Line 475: 4.	
Line 476: Click OK to create the file in the source tree inside the right package.
Line 477: 5.	
Line 478: Now, we rename the Word constructor parameter:
Line 479: public class Word {
Line 480:     public Word(String correctWord) {
Line 481:   // No Action
Line 482:     }
Line 483: }
Line 484: 6.	
Line 485: Next, we return to the test. We capture the new object as a local variable so that we can test it:
Line 486: @Test
Line 487: public void oneIncorrectLetter () {
Line 488:     var word = new Word("A");
Line 489: }
Line 490: The next design step is to think of a way to pass a guess into the Word class and return a score.
Line 491: 7.	
Line 492: Passing the guess in is an easy decision – we’ll use a method that we’ll call guess(). We can 
Line 493: code these decisions into the test:
Line 494: @Test
Line 495: public void oneIncorrectLetter () {
Line 496:     var word = new Word("A");
Line 497:     word.guess("Z");
Line 498: }
Line 499: 
Line 500: --- 페이지 93 ---
Line 501: Writing Our First Test
Line 502: 70
Line 503: 8.	
Line 504: Use autocomplete to add the guess() method to the Word class:
Line 505: Figure 5.5 – Creating the Word class
Line 506: 9.	
Line 507: Click Enter to add the method, then change the parameter name to a descriptive name:
Line 508: public void guess(String attempt) {
Line 509: }
Line 510: 10.	 Next, let’s add a way to get the resulting score from that guess. Start with the test:
Line 511: @Test
Line 512: public void oneIncorrectLetter () {
Line 513:     var word = new Word("A");
Line 514:     var score = word.guess("Z");
Line 515: }
Line 516: Then, we need a little think about what to return from the production code.
Line 517: We probably want an object of some sort. This object must represent the score from that guess. Because 
Line 518: our current user story is about the scores for a five-letter word and the details of each letter, we must 
Line 519: return one of exactly right, right letter, wrong place, or letter not present.
Line 520: There are several ways to do this and now is the time to stop and think about them. Here are some 
Line 521: viable approaches:
Line 522: •	 A class with five getters, each one returning an enum.
Line 523: •	 A Java 17 record type with the same getters.
Line 524: •	 A class with an iterator method, which iterates over five enum constants.
Line 525: 
Line 526: --- 페이지 94 ---
Line 527: Beginning Wordz
Line 528: 71
Line 529: •	 A class with an iterator method that returns one interface for each letter score. The scoring 
Line 530: code would implement a concrete class for each type of score. This would be a purely object-
Line 531: oriented way of adding a callback for each possible outcome.
Line 532: •	 A class that iterated over results for each letter and you passed in a Java 8 lambda function 
Line 533: for each of the outcomes. The correct one would be called as a callback for each letter.
Line 534: That’s already a lot of design options. The key part of TDD is that we are considering this now before 
Line 535: we write any production code. To help us decide, let’s sketch out what the calling code will look like. 
Line 536: We need to consider plausible extensions to the code – will we need more or fewer than five letters 
Line 537: in a word? Would the scoring rules ever change? Should we care about any of those things right 
Line 538: now? Would the people reading this code in the future more easily grasp any one of these ideas than 
Line 539: the others? TDD gives us fast feedback on our design decisions and that forces us to take a design 
Line 540: workout right now.
Line 541: One overriding decision is that we will not return the colors that each letter should have. That will be 
Line 542: a UI code decision. For this core domain logic, we will return only the fact that the letter is correct, 
Line 543: in the wrong position, or not present.
Line 544: It’s easy enough with TDD to sketch out the calling code because it is the test code itself. After about 
Line 545: 15 minutes of pondering what to do, here are the three design decisions we will use in this code:
Line 546: •	 Supporting a variable number of letters in a word
Line 547: •	 Representing the score using a simple enum of INCORRECT, PART_CORRECT, or CORRECT
Line 548: •	 Accessing each score by its position in the word, zero-based
Line 549: These decisions support the KISS principle, usually termed keep it simple, stupid. The decision to 
Line 550: support a variable number of letters does make me wonder whether I’ve overstepped another principle 
Line 551: – YAGNI – or you ain’t gonna need it. In this case, I’m convincing myself that it’s not too much of 
Line 552: a speculative design and that the readability of the score object will make up for that. Let’s move 
Line 553: on to the design:
Line 554: 1.	
Line 555: Capture these decisions in the test:
Line 556: @Test
Line 557: public void oneIncorrectLetter() {
Line 558:     var word = new Word("A");
Line 559:     var score = word.guess("Z");
Line 560:     var result = score.letter(0);
Line 561:     assertThat(result).isEqualTo(Letter.INCORRECT);
Line 562: }
Line 563: 
Line 564: --- 페이지 95 ---
Line 565: Writing Our First Test
Line 566: 72
Line 567: We can see how this test has locked in those design decisions about how we will use our objects. 
Line 568: It says nothing at all about how we will implement those methods internally. This is critical 
Line 569: to effective TDD. We have also captured and documented all the design decisions in this test. 
Line 570: Creating an executable specification such as this is an important benefit of TDD.
Line 571: 2.	
Line 572: Now, run this test. Watch it fail. This is a surprisingly important step.
Line 573: We might think at first that we only ever want to see passing tests. This is not totally true. Part 
Line 574: of the work in TDD is having confidence that your tests are working. Seeing a test fail when 
Line 575: we know we have not written the code to make it pass yet gives us confidence that our test is 
Line 576: probably checking the right things.
Line 577: 3.	
Line 578: Let’s make that test pass, by adding code to class Word:
Line 579: public class Word {
Line 580:     public Word(String correctWord) {
Line 581:         // Not Implemented
Line 582:     }
Line 583:     public Score guess(String attempt) {
Line 584:         var score = new Score();
Line 585:         return score;
Line 586:     }
Line 587: }
Line 588: 4.	
Line 589: Next, create class Score:
Line 590: public class Score {
Line 591:     public Letter letter(int position) {
Line 592:         return Letter.INCORRECT;
Line 593:     }
Line 594: }
Line 595: Again, we used IDE shortcuts to do most of the work in writing that code for us. The test passes:
Line 596: Figure 5.6 – A test passing in IntelliJ
Line 597: 
Line 598: --- 페이지 96 ---
Line 599: Summary
Line 600: 73
Line 601: We can see that the test passed and that it took 0.139 seconds to run. That certainly beats any 
Line 602: manual test.
Line 603: We also have a repeatable test, which we can run for the remainder of the project life cycle. The time 
Line 604: saving compared to manual testing will add up every time we run the test suite.
Line 605: You will notice that although the test passes, the code seems like it is cheating. The test only ever expects 
Line 606: Letter.INCORRECT and the code is hardcoded to always return that. It clearly could never possibly 
Line 607: work for any other values! This is expected at this stage. Our first test has set out a rough design for 
Line 608: the interface of our code. It has not yet begun to drive out the full implementation. We will do that 
Line 609: with our subsequent tests. This process is called triangulation, where we rely on adding tests to drive 
Line 610: out the missing implementation details. By doing this, all our code is covered by tests. We get 100% 
Line 611: meaningful code coverage for free. More importantly, it breaks our work down into smaller chunks, 
Line 612: creates progress with frequent deliverables, and can lead to some interesting solutions.
Line 613: Another thing to notice is that our one test led us to create two classes, covered by that one test. This is 
Line 614: highly recommended. Remember that our unit test covers a behavior, not any specific implementation 
Line 615: of that behavior.
Line 616: Summary
Line 617: We’ve taken our first steps into TDD and learned about the AAA structure of each test. We’ve seen 
Line 618: how it is possible to design our software and write our test before our production code and get cleaner, 
Line 619: more modular designs as a result. We learned what makes for a good test and learned some common 
Line 620: techniques used to catch common programming errors and test code that throws exceptions.
Line 621: It is important to understand the flow of using AAA sections inside our FIRST tests, as this gives us 
Line 622: a template we can reliably follow. It is also important to understand the flow of design ideas, as used 
Line 623: in the previous Wordz example. Writing our tests is literally taking the design decisions we make and 
Line 624: capturing them in unit test code. This provides fast feedback on how clean our design is, as well as 
Line 625: providing an executable specification for future readers of our code.
Line 626: In the next chapter, we will add tests and drive out a complete implementation for our word-scoring 
Line 627: object. We will see how TDD has a rhythm that drives work forward. We will use the Red, Green, Refactor 
Line 628: approach to keep refining our code and keep both code and tests clean without overengineering them.
Line 629: Questions and answers
Line 630: 1.	
Line 631: How do we know what test to write if we have no code to test?
Line 632: We reframe this thinking. Tests help us design a small section of code upfront. We decide what 
Line 633: interface we want for this code and then capture these decisions in the AAA steps of a unit 
Line 634: test. We write just enough code to make the test compile, and then just enough to make the 
Line 635: test run and fail. At this point, we have an executable specification for our code to guide us as 
Line 636: we go on to write the production code.
Line 637: 
Line 638: --- 페이지 97 ---
Line 639: Writing Our First Test
Line 640: 74
Line 641: 2.	
Line 642: Must we stick to one test class per production class?
Line 643: No, and this is a common misunderstanding when using unit tests. The goal of each test is 
Line 644: to specify and run a behavior. This behavior will be implemented in some way using code – 
Line 645: functions, classes, objects, library calls, and the like – but this test in no way constrains how 
Line 646: the behavior is implemented. Some unit tests test only one function. Some have one test per 
Line 647: public method per class. Others, like in our worked example, give rise to more than one class 
Line 648: to satisfy the test.
Line 649: 3.	
Line 650: Do we always use the AAA structure?
Line 651: It’s a useful recommendation to start out that way but we sometimes find that we can omit or 
Line 652: collapse a step and improve the readability of a test. We might omit the Arrange step, if we had 
Line 653: nothing to create for, say, a static method. We may collapse the Act step into the Assert step 
Line 654: for a simple method call to make the test more readable. We can factor our common Arrange 
Line 655: step code into a JUnit @BeforeEach annotate method.
Line 656: 4.	
Line 657: Are tests throwaway code?
Line 658: No. They are treated with the same importance and care as production code. The test code is kept 
Line 659: clean just as the production code is kept clean. The readability of our test code is paramount. 
Line 660: We must be able to skim-read a test and quickly see why it exists and what it does. The test code 
Line 661: is not deployed in production but that does not make it any less important.