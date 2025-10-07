Line 1: 
Line 2: --- 페이지 35 ---
Line 3: Chapter 3. Unit Tests with no
Line 4: Collaborators
Line 5: It is really fun to understand the types of interaction and parts of unit tests, but since "practice
Line 6: makes perfect" it is high time to put this knowledge to use. Just for now, we will be concentrating
Line 7: on a subset of testing issues, assuming as we shall that our SUT does not need any collaborators.
Line 8: This assumption – even if it does not hold for the majority of real-life classes – will permit us
Line 9: to demonstrate some important concepts, ideas and techniques. They will be much easier to
Line 10: explain under such conditions, even though their use is by no means limited to a no-collaborators
Line 11: environment. In fact some of them – e.g. the TDD approach – are not even confined to unit testing
Line 12: itself.
Line 13: In later sections (starting with Chapter 5, Mocks, Stubs, and Dummies) we drop this unrealistic
Line 14: assumption and discuss techniques for testing an SUT which cooperates with collaborators in
Line 15: various ways. But for now, let us pretend that our SUT is all alone.
Line 16: After reading the tools introduction you will already know that JUnit is the most popular Java testing
Line 17: framework aimed especially at unit tests. In this section we will learn to write and execute JUnit tests,
Line 18: and also learn some JUnit features that will be reused throughout the book. Some of them will only be
Line 19: briefly mentioned here, prior to being discussed in more detail in subsequent chapters.
Line 20: This book is not an all-embracing JUnit tutorial, even though it contains everything
Line 21: you should know if you want to write high-quality unit tests. JUnit offers more than is
Line 22: described here, including some features useful for integration and end-to-end tests. To truly
Line 23: master this tool, you should refer to other resources, i.e. JUnit documentation.
Line 24: 3.1. Project Structure and Naming
Line 25: Conventions
Line 26: Java developers tend to use similar layout for their projects these days. All sources of production code
Line 27: commonly reside in the src/main/java directory, while all test source files are kept at src/test/
Line 28: java.
Line 29: Below, you can see an example of a typical project layout:
Line 30: Listing 3.1. Typical project layout
Line 31: `-- src
Line 32:     |-- main
Line 33:     |   `-- java 
Line 34:     |       `-- com
Line 35:     |           `-- practicalunittesting
Line 36:     |               `-- Money.java 
Line 37:     `-- test
Line 38:         `-- java 
Line 39:         |   `-- com
Line 40:         |      `-- practicalunittesting
Line 41: 20
Line 42: 
Line 43: --- 페이지 36 ---
Line 44: Chapter 3. Unit Tests with no Collaborators
Line 45:         |            |-- MoneyTest.java 
Line 46:         `-- resources 
Line 47: src/main/java is where all your production code is located,
Line 48: an exemplary production class - Money,
Line 49: src/test/java is where all your test code resides,
Line 50: an exemplary test class - MoneyTest,
Line 51: there is also a general consensus that all test resources (e.g. files containing test data) should be
Line 52: put into subdirectories of the src/test/resources folder.
Line 53: The main thing to notice is that code and tests reside in different subtrees. This way your production
Line 54: JARs will not be polluted with unnecessary test classes. Most tools recognize this layout, and will
Line 55: treat both subtrees accordingly.
Line 56:  You probably have also noticed that test classes follow the SomethingTest name format (in our case,
Line 57: here, it is MoneyTest). The Something prefix will usually be the name of a class being tested by this
Line 58: particular test. This is a very common pattern, definitely worth following, as it enables developers to
Line 59: understand at once which class is being tested. Some tools also take advantage of this naming format1.
Line 60: We will be following this layout and naming format throughout the book.
Line 61: 3.2. Class To Test
Line 62: For our first unit-testing experience we will use a Money class, almost identical to the one used in a
Line 63: popular unit testing tutorial from JUnit2. For unit testing, the Money class plays a similar role to that
Line 64: played for any programming language by the famous HelloWorld example: it just has to be there3.
Line 65: We will begin with a very simple (and, to be honest, quite useless) class. Later on it will be extended.
Line 66: Listing 3.2. Money class to be tested
Line 67: public class Money {
Line 68:     private final int amount;
Line 69:     private final String currency;
Line 70:     public Money(int amount, String currency) {
Line 71:         this.amount = amount;
Line 72:         this.currency = currency;
Line 73:     }
Line 74:     public int getAmount() {
Line 75:         return amount;
Line 76:     }
Line 77:     public String getCurrency() {
Line 78:         return currency;
Line 79:     }
Line 80:     public boolean equals(Object anObject) {
Line 81: 1For some discussion of test-naming approaches, please refer to Section 10.2
Line 82: 2See http://junit.sourceforge.net/doc/testinfected/testing.htm
Line 83: 3This reminds me of the first time I put to the test the examples from this tutorial. It took me a few weeks to really digest these
Line 84: ideas about unit testing, which were completely new to me back then.
Line 85: 21
Line 86: 
Line 87: --- 페이지 37 ---
Line 88: Chapter 3. Unit Tests with no Collaborators
Line 89:         if (anObject instanceof Money) {
Line 90:             Money money = (Money) anObject;
Line 91:             return getCurrency().equals(money.getCurrency())
Line 92:                     && getAmount() == money.getAmount();
Line 93:         }
Line 94:         return false;
Line 95:     }
Line 96: }
Line 97: As you can see, the Money class is immutable. It has two final fields set by the constructor. The only
Line 98: method with some logic is the implementation of equals().
Line 99: 3.3. Your First JUnit Test
Line 100: Before you write a test, you need to think about test cases. You can write them down somewhere, if
Line 101: you feel it helps, but keeping them in your head will usually be enough.
Line 102: Looking at the code of the Money class you will probably notice two things that can be tested:
Line 103: • the constructor,
Line 104: • the equals() method.
Line 105: Testing of the constructor seems like a trivial matter, and this is exactly why we will start with it. The
Line 106: only thing we can check here is if amount and currency have been properly set4.   
Line 107: Listing 3.3. First JUnit unit test
Line 108: import org.junit.jupiter.api.Test; 
Line 109: import static org.assertj.core.api.Assertions.assertThat; 
Line 110: public class MoneyTest { 
Line 111:     @Test 
Line 112:     void constructorShouldSetAmountAndCurrency() { 
Line 113:         Money money = new Money(10, "USD"); 
Line 114:     assertThat(money.getAmount()).isEqualTo(10); 
Line 115:     assertThat(money.getCurrency()).isEqualTo("USD"); 
Line 116:     }
Line 117: }
Line 118: @Test annotation is required, so JUnit (and other tools) will recognize this method as a test
Line 119: method.
Line 120: The static import of the AssertJ Assertions class assertThat method makes assertion
Line 121: checking more concise.
Line 122: The test class does not have to extend any base class or implement any interfaces. Its name is
Line 123: also not important, though using the Test suffix leaves no doubt as to its purpose.
Line 124: The test method can take any name. It also doesn’t have to be public (which was required by
Line 125: previous versions of JUnit).
Line 126: 4It is questionable whether such code is worth testing in code-first manner. Please see the discussion in Section 11.5.
Line 127: 22
Line 128: 
Line 129: --- 페이지 38 ---
Line 130: Chapter 3. Unit Tests with no Collaborators
Line 131: An SUT is created.
Line 132: The SUT is put to the test and the results are verified using the static assertThat() method of
Line 133: the Assertions class.
Line 134: That is quite a lot of information for such a simple class! Much more could be written about each line
Line 135: of this code, but that is enough for now. We will discuss it step by step in the course of considering
Line 136: subsequent examples. Let us run the test now.
Line 137: There are many ways to run tests written with JUnit. Please consult Appendix D, Running
Line 138: Unit Tests, which contains detailed description of how to run tests with Eclipse, IntelliJ
Line 139: IDEA, Gradle and Maven.
Line 140: After you have run this first test, JUnit will print a short summary. It might vary, depending on the
Line 141: way you run it (in particular, your IDE will probably present it in some nicer way), but it will always
Line 142: contain information about executed, passed and failed tests. An example is shown below:
Line 143: Listing 3.4. JUnit summary test result
Line 144: Running com.practicalunittesting.MoneyTest
Line 145: Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.059 sec
Line 146: Remember to always look at the status line and react immediately if you see failed or skipped tests.
Line 147: Also, take note of the number of tests executed. It can happen, especially at the beginning of your
Line 148: testing journey, that your test will not run at all!
Line 149: 3.3.1. Test Results
Line 150: Tests executed by hand (see Section A.1 for some discussion of this) can end up with a plethora of
Line 151: results, ranging from "it works for me", through "I am not sure, but I do not have time to investigate it
Line 152: any further", to "it works… and this exception has always been there". In the case of automated tests
Line 153: things look different. There are only a few possible outcomes. Let us take a closer look at them.
Line 154: An automated test ends up in one of two states: as passed or failed. Two other outcomes are less
Line 155: frequent - a test can be skipped or finish with error. There is no place for "I think it should work
Line 156: now" in automated tests!
Line 157:  If all assertions of a test are met, and no unexpected exceptions are thrown, then that test passes. A
Line 158: passed test is usually marked with a green color by IDEs and test reports.
Line 159:  If an unexpected exception is thrown then the test fails. This happens if some assertion is unmet, or
Line 160: you have a bug in your code which results in, for example ArraysOutOfBoundsException. Your IDE
Line 161: and test reports will mark such a failed test with a red color.
Line 162:  A test can be skipped (which means it was not run at all) if some of its assumptions were not met
Line 163: (see Section 7.3), or if the user decided explicitly that it should be skipped. Such a test is usually
Line 164: marked with a yellow color.
Line 165:  Finally, a test can end up as an error, if some unexpected condition occurred that interrupted its
Line 166: execution. This is rather an uncommon situation and usually indicates that something is wrong with
Line 167: 23
Line 168: 
Line 169: --- 페이지 39 ---
Line 170: Chapter 3. Unit Tests with no Collaborators
Line 171: your test code. It can happen, for example, if a test method expects some parameters but they were
Line 172: not provided (see Section 3.6). Just like failed tests, tests which have ended in an error state are also
Line 173: marked with a red color. They are usually grouped with failed tests on reports.
Line 174: 3.4. Assertions
Line 175:  We have already encountered an assertion of the org.assertj.core.api.Assertions class. Let me
Line 176: remind you what it looked like:
Line 177: Listing 3.5. assertThat() in action
Line 178: assertThat(money.getAmount()).isEqualTo(10);
Line 179: assertThat(money.getCurrency()).isEqualTo("USD");
Line 180: As you can see, assertions written using AssertJ are quite readable. You could read the first one as
Line 181: "assert that money.getAmount() is equal to 10".
Line 182:  You will see many more assertions in this book, and you will soon notice they all start with the
Line 183: assertThat() method (a static method of the org.assertj.core.api.Assertions class). It takes
Line 184: one argument: the thing being tested. No matter if the tested object is a String, or a List<Integer>,
Line 185: or even an object of your own design, the assertion will always start with the assertThat() method.
Line 186: Another thing worth mentioning is that the assertThat() method does nothing valuable on its own.
Line 187: It only sets the stage for the methods that follow it to perform some real verification. In our case,
Line 188: the real work is performed by the isEqualTo() method, which verifies whether the argument of
Line 189: assertThat() is equal to the argument of the isEqualTo().
Line 190: Depending on the type of the object tested, the assertThat() method can be followed by different
Line 191: methods. Let me give you some examples of assertions performed on some basic Java types:
Line 192: Listing 3.6. Examples of assertions
Line 193: assertThat("some string").isNotEmpty()
Line 194: assertThat(1).isLessThan(2)
Line 195: assertThat(1).isGreaterThanOrEqualTo(0)
Line 196: assertThat(true).isTrue();
Line 197: assertThat(Arrays.asList(1, 2, 3)).contains(1);
Line 198: Another neat feature of AssertJ assertions is that you can chain them together to test various aspects of
Line 199: one object. For example, the following is possible:
Line 200: Listing 3.7. Assertions chaining
Line 201: assertThat("some string")
Line 202:     .isNotEmpty()
Line 203:     .hasSize(10)
Line 204:     .matches("some.*");
Line 205: I explain the reasons for using AssertJ assertions instead of those provided by JUnit in
Line 206: Appendix B, Fluent Assertions.
Line 207: 24
Line 208: 
Line 209: --- 페이지 40 ---
Line 210: Chapter 3. Unit Tests with no Collaborators
Line 211: 3.5. Failing Test
Line 212:  Let us see what happens when a test fails. Inevitably, tests will fail, so we had better get acquainted
Line 213: with it.
Line 214: To make our test fail, we need to introduce a small change into the constructor of the Money class.
Line 215: Listing 3.8. Breaking the code so the test fails
Line 216: public Money(int amount, String currency) {
Line 217:     this.amount = 15; 
Line 218:     this.currency = currency;
Line 219: }
Line 220: No matter what was passed by argument, amount will be set to 15.
Line 221: Of course, this change will make one of the assertions in our test
Line 222: (assertThat(money.getAmount()).isEqualTo(10)) fail. After rerunning the test, the following
Line 223: message and stack trace will appear:
Line 224: Listing 3.9. Failing test output
Line 225: org.junit.ComparisonFailure: 
Line 226: Expected :10 
Line 227: Actual   :15
Line 228:     at sun.reflect.NativeConstructorAccessorImpl
Line 229:       .newInstance0(Native Method)
Line 230:     at sun.reflect.NativeConstructorAccessorImpl
Line 231:       .newInstance(NativeConstructorAccessorImpl.java:57)
Line 232:     at sun.reflect.DelegatingConstructorAccessorImpl
Line 233:       .newInstance(DelegatingConstructorAccessorImpl.java:45)
Line 234:     at com.practicalunittesting.chp03.money.MoneyTest 
Line 235:         .constructorShouldSetAmountAndCurrency(MoneyTest.java:24)
Line 236: This line tells us that an assertion has failed.
Line 237: Both the expected and the actual value are used, and we can clearly see the reason for test
Line 238: failure.
Line 239: The first line of the stack trace to mention classes from your code points to the offending line in
Line 240: your test. In this case, it is the line which ends up with:
Line 241: assertThat(money.getAmount()).isEqualTo(10);
Line 242: One thing to notice is that the IDE was able to figure out the expected and actual values and print
Line 243: them accordingly. The information printed about the reason for the test failure is based on the
Line 244: assumption that we have kept the default order (actual values put into the assertThat() method,
Line 245: expected values put into the methods which follow next). In any other circumstances, the information
Line 246: printed would have been misleading.
Line 247: We will discuss the assertions' messages in details in Section 9.4.
Line 248: 25
Line 249: 
Line 250: --- 페이지 41 ---
Line 251: Chapter 3. Unit Tests with no Collaborators
Line 252: 3.6. Parameterized Tests
Line 253:  When you look for your cat it is not enough to check whether it occupies your her sofa (as usual).
Line 254: If she is not there, then you have to check under the desk, and in a few other places before you can
Line 255: declare "she is not here!" (and you can still be gravely mistaken). It’s the same with the tests of our
Line 256: Money class. Checking it with a single test case of $10 is not enough to declare "it works!". In this
Line 257: section, we will find out how to enhance our tests so that we can declare with more certainty that
Line 258: "there are no bugs!" (hmm… well, the cat can hide in your wardrobe without your knowing anything
Line 259: about it - and so can the bugs).
Line 260: Let us leave the cat example (but I can’t promise it won’t come back) and see how we could go about
Line 261: it. We start with a naive - but working! - approach of simply repeating similar checks for different
Line 262: values.
Line 263: Listing 3.10. Testing the Money class with more than one value
Line 264: import org.junit.jupiter.api.Test;
Line 265: import static org.assertj.core.api.Assertions.assertThat;
Line 266: public class MoneyManyValuesTest {
Line 267:     public static final String USD = "USD";
Line 268:     @Test
Line 269:     void constructorShouldSetAmountAndCurrency() {
Line 270:         Money money = new Money(10, USD);
Line 271:         assertThat(money.getAmount()).isEqualTo(10);
Line 272:         assertThat(money.getCurrency()).isEqualTo(USD);
Line 273:         money = new Money(20, USD);
Line 274:         assertThat(money.getAmount()).isEqualTo(20);
Line 275:         assertThat(money.getCurrency()).isEqualTo(USD);
Line 276:     // ... and so on - e.g. for 100, 999 and 23908423 USD
Line 277:     }
Line 278: }
Line 279: This approach will work, but its drawbacks are clearly visible. First of all, there is a lot of repetition
Line 280: and a clear violation of the DRY5 principle. Secondly, such code is usually created using the
Line 281: "copy&paste" technique, and that’s a sure recipe for getting into trouble (when you copy a whole
Line 282: section but only change a part of it). Thirdly, the test class will grow with every new set of arguments.
Line 283: Enough! There must be a better way!
Line 284: A different variation of this technique would be to introduce a for loop and iterate over the collection
Line 285: of inputs and expected outputs. This isn’t advisable either, as it introduces some logic into your test
Line 286: code (albeit of a very basic kind) - something we will further discuss in Section 11.2.
Line 287: Fortunately, you do not need to invent your own solution here. This requirement is so common that
Line 288: testing frameworks offer support for exactly these sorts of cases. It is called "parameterized tests". Let
Line 289: us see how JUnit can help us here.
Line 290: 5See http://en.wikipedia.org/wiki/Don’t_repeat_yourself.
Line 291: 26
Line 292: 
Line 293: --- 페이지 42 ---
Line 294: Chapter 3. Unit Tests with no Collaborators
Line 295: 3.6.1. The idea
Line 296: No matter which tool for parameterized tests you decide to use6, the general idea is always the same.
Line 297: The test method gets split into two parts. The first part acts as a source of arguments that will be
Line 298: passed to the second part (the actual test method), which, in turn, is responsible for the actual testing.
Line 299: And both are linked together using some special annotation.
Line 300: 3.6.2. One parameter only
Line 301: Let’s start with a super-simplified example in which only one argument (amount of USD) changes.
Line 302: This code illustrates how to leverage JUnit support for parameterized tests to achieve this.  
Line 303: Listing 3.11. Single parameter passed to test method
Line 304: import org.junit.jupiter.params.ParameterizedTest; 
Line 305: import org.junit.jupiter.params.provider.ValueSource;
Line 306: public class MoneyOneParamAnnotationTest {
Line 307:     @ParameterizedTest 
Line 308:     @ValueSource(ints = { 10, 15, 50 }) 
Line 309:     void constructorShouldSetAmountAndCurrency(int amount) { 
Line 310:         Money money = new Money(amount, "USD");
Line 311:         assertThat(money.getAmount()).isEqualTo(amount);
Line 312:     }
Line 313: }
Line 314: We have to use @ParameterizedTest annotation instead of @Test to inform JUnit that this test
Line 315: method will accept some input parameters.
Line 316: The @ValueSource annotation is the simplest way to provide a single parameter to a test method
Line 317: (more about this soon).
Line 318: …which our test method accepts, now expecting a single amount parameter.
Line 319: And if we run this code, we would see something similar to this output:
Line 320: [root]
Line 321: MoneyOneParamAnnotationTest
Line 322:   constructorShouldSetAmountAndCurrency(int)
Line 323:     [1] 10
Line 324:     [2] 15
Line 325:     [3] 50
Line 326: A lot happens in these few lines of code, so let us discuss it a little bit. Firstly, it seems that
Line 327: JUnit executed each test case (each set of parameters) separately. Secondly, this new annotation
Line 328: @ValueSource acts as a provider of test data. Thirdly, our IDE was able to nicely present the result of
Line 329: test execution.
Line 330: We can see now that all we need to test our classes with many input values is to combine the
Line 331: @ParameterizedTest annotation with @ValueSource annotation, and add a relevant parameter to the
Line 332: test method signature.
Line 333: 6For example, there is a very nice JUnitParams library [http://pragmatists.github.io/JUnitParams/] that was commonly used for
Line 334: JUnit4 which didn’t provide good support for parameterized tests.
Line 335: 27
Line 336: 
Line 337: --- 페이지 43 ---
Line 338: Chapter 3. Unit Tests with no Collaborators
Line 339: What are we gaining by this compared to our naive approach shown in Listing 3.10? Definitely
Line 340: the DRY principle is not violated. We have also clearly separated the part that provides the data
Line 341: (in this case, the @ValueSource annotation) from the testing algorithm (in this case the body of
Line 342: constructorShouldSetAmountAndCurrency) method. Also, the code is concise and everything is
Line 343: based on what JUnit provides, with no additional coding required on our side.
Line 344: 3.6.3. More than one parameter
Line 345: But we need more than just passing amount of USD to our test method. What if wanted to verify the
Line 346: combinations of amount and currency? The following code proves it is possible with the use of the
Line 347: @CsvSource annotation. 
Line 348: Listing 3.12. Many parameters passed to test method
Line 349: import org.junit.jupiter.params.ParameterizedTest; 
Line 350: import org.junit.jupiter.params.provider.CsvSource; 
Line 351: public class MoneyManyParamsAnnotationTest {
Line 352:   @ParameterizedTest 
Line 353:   @CsvSource({ 
Line 354:       "10, USD", // first set of arguments
Line 355:       "15, EUR", // second set of arguments
Line 356:       "50, CHF" // third set of arguments
Line 357:   })
Line 358:   void constructorShouldSetAmountAndCurrency(int amount, String currency) { 
Line 359:       Money money = new Money(amount, currency);
Line 360:       assertThat(money.getAmount()).isEqualTo(amount);
Line 361:       assertThat(money.getCurrency()).isEqualTo(currency);
Line 362:   }
Line 363: }
Line 364: Again, we use the @ParameterizedTest instead of the @Test annotation.
Line 365: The @CsvSource annotation allows us to specify many values per each test case (in our case
Line 366: two).
Line 367: The method signature has changed - it now accepts both amount and currency.
Line 368: As you can see, there is a perfect match between the number of values provided by the @CSVSource
Line 369: annotation and our test method (and if there weren’t, JUnit would have complained loudly about it!).
Line 370: The execution output presented by IDE assures us that JUnit has in fact executed three separate test
Line 371: cases:
Line 372: MoneyManyParamsAnnotationTest
Line 373:   constructorShouldSetAmountAndCurrency(int, String)
Line 374:     [1] 10, USD
Line 375:     [2] 15, EUR
Line 376:     [3] 50, CHF
Line 377: And, by the way, have you noticed that JUnit silently converted our String parameters into Integer
Line 378: when we weren’t looking? Well done, JUnit!7
Line 379: 7We will discuss this miracle further in Section 7.11.3.
Line 380: 28
Line 381: 
Line 382: --- 페이지 44 ---
Line 383: Chapter 3. Unit Tests with no Collaborators
Line 384: 3.6.4. Conclusions
Line 385:   We will revisit the parameterized tests in Section 7.11 but as for now we have seen enough.
Line 386: Summing up, the advantages of using parameterized tests over any custom code are the following:
Line 387: • none of our own, potentially flawed, logic is introduced (e.g. for loop),
Line 388: • adding another set of arguments is very easy, and does not make the code grow,
Line 389: • there is no copy&paste coding and the DRY principle is faithfully honored,
Line 390: • there is a clear separation between test logic (how the code is expected to work) and test data (what
Line 391: values are tested),
Line 392: • we get detailed results of test execution.
Line 393: …and what about the downsides? Surely parameterized tests have some of these! Yes they do, but
Line 394: they are of less importance (wait till Section 7.11 to learn about them.).
Line 395: 3.7. Checking Expected Exceptions
Line 396: From time to time your code needs to throw an exception. Perhaps a method received an unexpected
Line 397: (illegal) value as an argument. Perhaps a third-party component that it cooperates with has thrown
Line 398: an exception. Perhaps… Anyway, exceptions are a vital part of how your methods behave. They are
Line 399: equally important for the results that are returned. They belong to the interface of your class, and
Line 400: therefore should be tested.
Line 401: Fortunately, checking for expected exceptions is very easy, these days. The following code snippet
Line 402: illustrates this: 
Line 403: Listing 3.13. Expected exceptions testing pattern
Line 404: import static org.assertj.core.api.Assertions.assertThatExceptionOfType; 
Line 405: @Test
Line 406: void testException() {
Line 407:   assertThatExceptionOfType(MyException.class)
Line 408:     .isThrownBy(() -> {  
Line 409:         SUT.someMethod(); 
Line 410:     });
Line 411: }
Line 412: Yet another static method of AssertJ Assertions class.
Line 413: An exception of the MyException class is expected to be thrown by a lambda expression.
Line 414: The code that we expect to throw an exception of the given class.
Line 415: Think of it as about another way of writing a try-catch statement, and apply the same
Line 416: rules. In particular do not catch exceptions of the class Exception when something much
Line 417: more specific (e.g. an exception of type the IllegalArgumentException) is expected.
Line 418: And if the exception is not thrown, the test will fail and JUnit will inform us about the reason:
Line 419: java.lang.AssertionError:
Line 420: 29
Line 421: 
Line 422: --- 페이지 45 ---
Line 423: Chapter 3. Unit Tests with no Collaborators
Line 424:   Expecting code to raise a throwable.
Line 425: Let us have a look at an example now. We will introduce a change to the Money class. Let its
Line 426: constructor throw an IllegalArgumentException if amount is less than 0.
Line 427: Listing 3.14. Money class constructor with arguments checking
Line 428: public Money(int amount, String currency) {
Line 429:     if (amount < 0) {
Line 430:         throw new IllegalArgumentException(
Line 431:             "illegal amount: [" + amount + "]");
Line 432:     }
Line 433:     this.amount = amount;
Line 434:     this.currency = currency;
Line 435: }
Line 436: Now, we would like to test it8. The test can look as shown in Listing 3.15. It is a parameterized test
Line 437: that you are already familiar with. We pass a few negative values via the @ValueSource annotation
Line 438: which makes the code very concise and allows for multiple values to be tested with a minimal amount
Line 439: of test code.
Line 440: Listing 3.15. Money class constructor expected exceptions test
Line 441: import org.junit.jupiter.params.ParameterizedTest; 
Line 442: import org.junit.jupiter.params.provider.ValueSource; 
Line 443: import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
Line 444: public class MoneyIAETest {
Line 445:     private final static String VALID_CURRENCY = "USD";
Line 446:     @ParameterizedTest 
Line 447:     @ValueSource(ints = { -12387, -5, -1 }) 
Line 448:     void constructorShouldThrowIAEForInvalidAmount(int invalidAmount) { 
Line 449:         assertThatExceptionOfType(IllegalArgumentException.class)
Line 450:                 .isThrownBy(() -> { 
Line 451:             new Money(invalidAmount, VALID_CURRENCY); 
Line 452:         });
Line 453:     }
Line 454: }
Line 455: Yes, this is a parameterized test.
Line 456: These integers seem like reasonable values to check the non-negative scenario.
Line 457: Our test method expects an integer argument.
Line 458: Expecting exception…
Line 459: …thrown by this constructor call.
Line 460: And voilà! This test verifies that an exception of the IllegalArgumentException class is thrown
Line 461: when an unwanted amount value is passed to the constructor of the Money class.
Line 462: Armed with this knowledge, we will leave the topic of the verification of expected exceptions for
Line 463: now. There is more to say, and we will do this in Section 7.4.
Line 464: 8Personally, I feel slightly uneasy about this code-first approach. We shall soon be introducing the test-first technique, and will be
Line 465: adhering to it throughout the rest of the book.
Line 466: 30
Line 467: 
Line 468: --- 페이지 46 ---
Line 469: Chapter 3. Unit Tests with no Collaborators
Line 470: Naming
Line 471:   What I would like to stress here is the importance of giving meaningful names to methods
Line 472: and variables9. They make the test readable and leave no room for doubt as to the role played
Line 473: by each method or variable. Let’s take a look at this statement:
Line 474: new Money(invalidAmount, VALID_CURRENCY);
Line 475: By using meaningful names for variables, we have achieved a highly readable test. Just read it
Line 476: as follows: "this line of code creates a new object of the class Money, using an invalid amount
Line 477: and a valid currency". All perfectly clear.
Line 478: 3.8. Test Fixture Setting
Line 479: A software test fixture sets up the system for the testing process by providing it with
Line 480: all the necessary code to initialize it, thereby satisfying whatever preconditions there
Line 481: may be. […] This allows for tests to be repeatable, which is one of the key features of
Line 482: an effective test framework.
Line 483: — Wikipedia Test fixture
Line 484:  Have you ever seen a kid trying to measure the length of his bed with a tape measure for the first
Line 485: time? It usually results in tape measure moving to and fro and the final measurement is nowhere near
Line 486: the real values. This can also happen in a test if we don’t make sure that the object we want to verify
Line 487: is in a known state.
Line 488: To give you a better understanding of what this test fixture thing is all about, the following table
Line 489: provides examples of test fixtures for different types of test. As you can imagine, the steps required to
Line 490: set up such an environment differ, depending on the types of tests and tools used, but the basic idea is
Line 491: always the same.
Line 492: Table 3.1. Test fixture examples
Line 493: Type of test
Line 494: Test fixture example
Line 495: unit test
Line 496: • creation of new objects (SUT and test doubles),
Line 497: • preparation of input data,
Line 498: integration
Line 499: test
Line 500: • resetting the database to the initial state (e.g. so it contains one user with
Line 501: required privileges whose account can be used to perform tests),
Line 502: • copying of files that will be used during tests,
Line 503: end-to-end
Line 504: test
Line 505: • installation of a virtual machine that provides the runtime environment for the
Line 506: application,
Line 507: • installation (or cleaning to some initial state) of the web server and database
Line 508: used by the application.
Line 509: The automation of the environment setup process is often the most challenging part of
Line 510: testing. This is especially true for integration and end-to-end tests. In the case of unit tests
Line 511: things are usually much simpler, but there are still some issues which should be taken care
Line 512: of.
Line 513: 9This issue is further discussed in Section 10.2 and Section 12.6.1
Line 514: 31
Line 515: 
Line 516: --- 페이지 47 ---
Line 517: Chapter 3. Unit Tests with no Collaborators
Line 518: It is time to make sure that all the elements are in place before an SUT’s method is executed in our
Line 519: unit tests.
Line 520: 3.8.1. @BeforeEach
Line 521: We will use a mechanism offered by JUnit to have the required objects fresh & ready for use before
Line 522: each test method. Hmm…. I just wrote "before each test method", which leads us straight to the
Line 523: JUnit5 @BeforeEach annotation. Its usage is straightforward: a method marked with this annotation
Line 524: will be executed before each test method is executed.
Line 525: Later on (see Section 8.3) we will discuss other approaches to test fixture creation.
Line 526: We will demonstrate the use of @BeforeEach annotation using two simple Client and Address
Line 527: classes. Suppose we want to verify that the objects of the Client class are able to store a collection of
Line 528: addresses. Listing 3.16 shows what such a test could look like. 
Line 529: Listing 3.16. ClientTest with @BeforeEach annotation
Line 530: import org.junit.jupiter.api.BeforeEach; 
Line 531: public class ClientTest {
Line 532:   private Address address = new Address("street A"); 
Line 533:   private Address secondAddress = new Address("street B"); 
Line 534:   private Client client;
Line 535:   @BeforeEach 
Line 536:   void setUp() {
Line 537:     client = new Client(); 
Line 538:     // client.setSomePropertiesIfNeeded(); 
Line 539:   }
Line 540:   @Test
Line 541:   void afterCreationShouldHaveNoAddress() {
Line 542:     // ... assert that client has no addresses 
Line 543:   }
Line 544:   @Test
Line 545:   void shouldAllowToAddAddress() {
Line 546:     client.addAddress(address);
Line 547:     // ... assert that client has this one address 
Line 548:   }
Line 549:   @Test
Line 550:   void shouldAllowToAddManyAddresses() {
Line 551:     client.addAddress(address);
Line 552:     client.addAddress(secondAddress);
Line 553:     // ... assert that client has two addresses 
Line 554:   }
Line 555: }
Line 556: 32
Line 557: 
Line 558: --- 페이지 48 ---
Line 559: Chapter 3. Unit Tests with no Collaborators
Line 560: The @BeforeEach annotation makes JUnit execute this method before each test method is
Line 561: executed.
Line 562: We don’t care much about the state of these objects, so there is no real difference as to where we
Line 563: create them.
Line 564: SUT is created and set into desired state for testing.
Line 565: In Section 7.10 we will learn classy ways to test collections, but for now let us just skip this part
Line 566: and concentrate on the test fixture issues.
Line 567:  The order of method execution of the code from Listing 3.16 is the following10:
Line 568: setUp()
Line 569: afterCreationShouldHaveNoAddress()
Line 570: setUp()
Line 571: shouldAllowToAddManyAddresses()
Line 572: setUp()
Line 573: shouldAllowToAddAddress()
Line 574: JUnit lifecycle
Line 575: To fully understand the code you should know that JUnit creates a new instance of a test
Line 576: class before executing each test method marked with the @Test annotation. This means that
Line 577: instance variables (like address and secondAddress) are created anew before the execution
Line 578: of each test method.
Line 579: 3.8.2. Other test fixture annotations
Line 580:    JUnit offers three more similar annotations with meaningful names: @AfterEach, @BeforeAll and
Line 581: @AfterAll. As you probably guessed:
Line 582: • @AfterEach is the counterpart of @BeforeEach as it is executed after each test method,
Line 583: • @BeforeAll and @AfterAll follow the logic of @BeforeEach and @AfterEach, but on the class
Line 584: level (that is, before/after any test of a test class is/was executed)
Line 585: I will not discuss them any further as their use in unit tests is rather limited. They are pretty handy for
Line 586: higher level tests and you will surely use them there to create some costly resources and to clean them
Line 587: afterwards. For unit tests, you will rarely need them11, so there is no point in focusing on them now.
Line 588: Set-up method
Line 589: I use the setUp() name for a good reason and I encourage you to do the same. JUnit version
Line 590: 3.x had a special method, called setUp(), responsible for setting up the test fixture. It had
Line 591: to be named exactly this so that JUnit could recognize it and execute it at the right moments.
Line 592: JUnit 5 ignores method names, but responds to method annotations, so you are free to name
Line 593: such methods as you wish. But if you continue using setUp(), it will make the purpose of the
Line 594: method obvious to many developers who used to work with older versions of JUnit.
Line 595: In addition, you will from time to time hear people talking about "set-up methods". And now
Line 596: you know what they mean by this.
Line 597: 10In fact, the order of execution of the test methods is not guaranteed. What is guaranteed is that methods annotated with
Line 598: @BeforeEach will be invoked before each of the test methods.
Line 599: 11See Section 8.9 for some discussion.
Line 600: 33
Line 601: 
Line 602: --- 페이지 49 ---
Line 603: Chapter 3. Unit Tests with no Collaborators
Line 604: 3.9. Phases of a Unit Test
Line 605: Now that we have encountered some unit tests we may take a closer look at their structure. As you
Line 606: will probably have noticed, a unit test takes care of three things: firstly, it creates an object to be
Line 607: tested (the SUT) along with other required objects (the SUT’s collaborators), then it executes the
Line 608: SUT’s methods, and finally it verifies the results. This pattern is so common for unit tests that such
Line 609: tests are often described as Arrange / Act / Assert tests.
Line 610: The first phase - arrange - relates to the preparation of a test fixture (see Section 3.8). As we have
Line 611: already discussed, this functionality is often (at least partially) contained within instance variables
Line 612: or utility methods shared by many tests, to avoid duplication of such set-up code across multiple test
Line 613: classes. You might noticed that there is no "cleaning" phase (or, to use JUnit nomenclature, tear-down
Line 614: method). Such a step is rarely used in unit tests where fresh objects are created at the beginning of
Line 615: every test method and no persisting storages (e.g. databases) are used.
Line 616: Let us now analyze the ClientTest class which we have been discussing in the previous section.
Line 617: Arrange
Line 618: We need to arrange all the necessary actors of our tests, which usually boils down to:
Line 619: • creation of all the objects that are necessary for test execution (i.e. test collaborators),
Line 620: • creation of the SUT - the object whose functionality will be tested,
Line 621: • setting the collaborators and the SUT in some initial state.
Line 622: An example of this phase could look like this:
Line 623: Address address = new Address("street A");
Line 624: Address secondAddress = new Address("street B");
Line 625: Client client = new Client();
Line 626: Act
Line 627: This phase is all about the execution of SUT method(s) to be tested. This is often the shortest phase of
Line 628: all three, for example:
Line 629: client.addAddress(address);
Line 630: client.addAddress(secondAddress);
Line 631: Assert
Line 632: This is where we verify the results.
Line 633: assertThat(client.getAddresses()).hasSize(2));
Line 634: assertThat(client.getAddresses()).contains(address);
Line 635: assertThat(client.getAddresses()).contains(secondAddress);
Line 636: As we have seen in the previous examples, not all of the phases will necessarily be contained within a
Line 637: test method. For example, in the last version of the ClientTest class that we discussed (see Section
Line 638: 3.8.1), both instances of the Address class were created as private fields, and the SUT (an object of
Line 639: 34
Line 640: 
Line 641: --- 페이지 50 ---
Line 642: Chapter 3. Unit Tests with no Collaborators
Line 643: the Client class) was created within a setUp() method. However, this does not alter the fact that
Line 644: during test execution, the order of their creation was exactly as presented above.
Line 645:  Opinions are divided within the testing community as to what constitutes an adequate
Line 646: number of assertions per test method (see Section 8.4 for some discussion of this topic).
Line 647: However, it is recommended that all assertions within a single test method verify
Line 648: properties of a single object: the SUT. Asserting on many objects within a single test
Line 649: method is considered bad practice, and should be avoided!
Line 650: 3.10. Conclusions
Line 651: In this section you have met JUnit and AssertJ and learned:
Line 652: • about the default project structure that will be used throughout the book,
Line 653: • how to write test classes and test methods,
Line 654: • how to run tests,
Line 655: • what assertions AssertJ provides,
Line 656: • how to use parameterized tests,
Line 657: • how to verify expected exceptions,
Line 658: • how to use annotations for test fixture management.
Line 659: What we have discussed in this section is good enough if you want to write really nice and useful
Line 660: unit tests. We have not gone into greater detail concerning these features, however, for two reasons:
Line 661: firstly, in many cases there are no more details, because testing frameworks (JUnit included) are rather
Line 662: simple, and secondly, we shall be adding a thing or two in subsequent parts of the book to what you
Line 663: have already learned about JUnit, and this will make more sense in the specific contexts that arise.
Line 664: As you might expect, JUnit offers many other features which we have not yet covered. Some of them
Line 665: will be discussed in the ensuing sections, while others lie beyond the scope of this book, inasmuch as
Line 666: they have no real use in connection with unit tests. Once again, please make sure you at least browse
Line 667: the JUnit documentation, so that you know about its various capabilities.
Line 668: In the following sections we will be making use of the knowledge you have acquired here, so please
Line 669: make sure to practice it a little bit, before reading further.
Line 670: 35
Line 671: 
Line 672: --- 페이지 51 ---
Line 673: Chapter 3. Unit Tests with no Collaborators
Line 674: 3.11. Exercises
Line 675: The goal of the exercises presented below is twofold: firstly, they are here to help you get used to the
Line 676: idea of unit testing your code, and secondly, by carrying them out, you will preserve your knowledge
Line 677: of JUnit features.
Line 678: 3.11.1. JUnit Run
Line 679: This exercise will help you get up and running with JUnit.
Line 680: 1. Create a new empty project using the build tool of your choice (Maven, Gradle). Add required
Line 681: JUnit dependencies. Create a simple test class with a single test method containing some assertions.
Line 682: 2. Compile and run the test using your build tool.
Line 683: 3. Compile and run the test using your IDE.
Line 684: 4. Browse the test results.
Line 685: 3.11.2. Learn About AssertJ
Line 686: The simplest way to learn about assertions provided by AssertJ is the following. Open your IDE and
Line 687: create a new test class. Then create a test method like this:
Line 688: @Test
Line 689: void learnAssertJ() {
Line 690:     double var = 2.5;
Line 691:     assertThat(var). 
Line 692: }
Line 693: Unfinished line with hanging dot at the end.
Line 694: If you set the cursor after the hanging dot and ask your IDE for autocompletion then it will provide
Line 695: you with the list of available methods. All you have to do now is to change the type of variable var to
Line 696: String, BigDecimal or List<Object> and see what assertions are available.
Line 697: 3.11.3. String Reverse
Line 698: A developer attempted to write a utility String reversing method. The outcome of his attempts is
Line 699: displayed below:
Line 700: Listing 3.17. String reverse
Line 701: public static String reverse(String s) {
Line 702:     List<String> tempArray = new ArrayList<String>(s.length());
Line 703:     for (int i = 0; i < s.length(); i++) {
Line 704:         tempArray.add(s.substring(i, i+1));
Line 705:     }
Line 706:     StringBuilder reversedString = new StringBuilder(s.length());
Line 707:     for (int i = tempArray.size() -1; i >= 0; i--) {
Line 708:         reversedString.append(tempArray.get(i));
Line 709: 36
Line 710: 
Line 711: --- 페이지 52 ---
Line 712: Chapter 3. Unit Tests with no Collaborators
Line 713:     }
Line 714:     return reversedString.toString();
Line 715: }
Line 716: Now go ahead and write unit tests (using JUnit framework) which will verify that the method works
Line 717: properly!
Line 718: Additional requirements and hints:
Line 719: • think about the possible input parameters (see Section 7.1),
Line 720: • use parameterized tests (see Section 3.6) to make the test code concise,
Line 721: • write tests for expected exceptions (see Section 3.7),
Line 722: • if the method on Listing 3.17 does not work properly, then fix it,
Line 723: • refactor (after all the tests pass).
Line 724: 3.11.4. HashMap
Line 725: Write unit tests which will verify the following properties of the java.util.HashMap class:
Line 726: • an object stored with the put() method can be retrieved with the get() method,
Line 727: • adding a second object with the same key results in the old value being replaced ,
Line 728: • the clear() method removes all its content,
Line 729: • the null value can be used as a key,
Line 730: Additional requirement:
Line 731: • use the appropariate JUnit annotations to create a fresh, empty map before each test method is
Line 732: called (see Section 3.8)
Line 733: 3.11.5. Fahrenheits to Celcius with Parameterized
Line 734: Tests
Line 735: A simple test class is shown in Listing 3.18. Your task is to introduce parameterized tests, so there
Line 736: will be no repetition in the test code.
Line 737: Listing 3.18. Fahrenheit to Celcius conversion test
Line 738: public class FahrenheitCelciusConverterTest {
Line 739:     @Test
Line 740:     void shouldConvertCelciusToFahrenheit() {
Line 741:         assertThat(FahrToCelcConverter.toFahrenheit(0)).isEqualTo(32);
Line 742:         assertThat(FahrToCelcConverter.toFahrenheit(37)).isEqualTo(98);
Line 743:         assertThat(FahrToCelcConverter.toFahrenheit(100)).isEqualTo(212);
Line 744:     }
Line 745: 37
Line 746: 
Line 747: --- 페이지 53 ---
Line 748: Chapter 3. Unit Tests with no Collaborators
Line 749:     @Test
Line 750:     void shouldConvertFahrenheitToCelcius() {
Line 751:         assertThat(FahrToCelcConverter.toCelcius(32)).isEqualTo(0);
Line 752:         assertThat(FahrToCelcConverter.toCelcius(100)).isEqualTo(37);
Line 753:         assertThat(FahrToCelcConverter.toCelcius(212)).isEqualTo(100);
Line 754:     }
Line 755: }
Line 756: 3.11.6. Master Your IDE
Line 757: Make sure you spend some time learning about the support your IDE can give you in terms of
Line 758: effective unit testing. In particular, there are two features you should get accustomed with.
Line 759: Templates
Line 760: Every decent IDE allows you to create custom templates for quickly creating larger code structures.
Line 761: For the sake of efficient unit testing, you should at least learn how to:
Line 762: • create a test class template (so, for example, you have all the required imports already included),
Line 763: • create some typical code constructs - i.e. parameterized tests and set-up methods.
Line 764: Quick Navigation
Line 765: It is very handy to able to quickly navigate between the production class (e.g. Money) and the
Line 766: corresponding test classes (e.g. MoneyTest). Find out the proper keyboard shortcut for doing this.
Line 767: 38