Line 1: 
Line 2: --- 페이지 118 ---
Line 3: Chapter 7. Things You Should Know
Line 4: You have learned much, young one.
Line 5: — Darth Vader The Empire Strikes Back (1980)
Line 6: After having read the previous parts of this book, you should now be capable of writing unit tests.
Line 7: In fact, you should know a lot about things which some people would regard as "advanced" - for
Line 8: example parameterized tests and test doubles. Still, there are a great many other things you should
Line 9: also know, that will make your tasks easier to complete. You could probably figure them out yourself,
Line 10: using your existing knowledge and your general programming experience, but I would encourage you
Line 11: to continue your education here, and to read about custom patterns, frequently arising problems and
Line 12: various aspects of unit testing. There is still so much for you to learn!
Line 13: In this section we will first discuss a few general aspects of writing tests (namely, advanced expected
Line 14: exceptions handling and the use of matchers), before proceeding with some how-to subsections
Line 15: devoted to such extremely common problems as testing collections, testing time-dependent methods,
Line 16: and the like.
Line 17: 7.1. What Values To Check?
Line 18: […] even for a small program, with a relatively simple set of variables and relatively
Line 19: few possible states per variable, the total number of possible valid states in
Line 20: combination is intractably large.
Line 21: — Michael Bolton DevelopSense
Line 22: This section discusses a common problem related to the number of tests that should be written for a
Line 23: given function. It does not give an ultimate answer, but definitely sheds some light on this topic.
Line 24: To test functionality you need to decide what arguments will be passed to methods. In general it is
Line 25: impossible to tests every combination of input arguments (for obvious reasons). This forces us to
Line 26: choose a subset of arguments, that will represent all possible cases. This might sound hard, but is
Line 27: usually quite simple. Let us discuss some tips for selecting the right arguments.
Line 28: My general advice is as follows. You should select arguments that belong to these three groups:
Line 29: expected values (AKA happy path), boundary values, and strange values (AKA validity or
Line 30: domain).
Line 31: 7.1.1. Expected Values
Line 32:  This is how you expect a reasonable client1 will use your code. You expect that he will pass "John"
Line 33: as his name, "52" as his age and "yellow" as his favorite color. You expect him to pass values from
Line 34: 1 to 12 to the function that takes month as an input. You expect that he will pass a positive value to a
Line 35: constructor of Circle class that takes radius parameter. You expect that if he asks you to parse an
Line 36: XML file, to find all products with price greater than 30, then the file will at least be a valid XML.
Line 37: And so on…
Line 38: 1In this case client is someone or something that calls your code, not necessarily a person.
Line 39: 103
Line 40: 
Line 41: --- 페이지 119 ---
Line 42: Chapter 7. Things You Should Know
Line 43: This is something you absolutely need to check. Call your code with normal, reasonable, sensible,
Line 44: expected values, and make sure that it behaves properly, i.e. that it gives good answers. This is crucial.
Line 45: If your code does not work properly for such decent input arguments, it is useless.
Line 46: 7.1.2. Boundary Values
Line 47:  After you have checked that your code works fine for "normal" values, it is time to look for boundary
Line 48: values. Such values are a typical source of errors. You need to be especially inquisitive when checking
Line 49: for boundary values2.
Line 50: In the previous section we chose arguments that represented expected values. It was always clear
Line 51: what your code should do when asked to work on them. In short, it should do its job. Now we choose
Line 52: arguments that are on the borderline. Sometimes we choose those that live inside a box labeled
Line 53: "reasonable arguments", sometimes we choose them from a box labeled "out of scope". When writing
Line 54: tests we need to decide which value belongs to which group3. This is when we decide whether,
Line 55: for example, -1 should result in an IllegalArgumentException or should cause a normal flow of
Line 56: calculations to ensue.
Line 57: Let us discuss an example. Imagine a method that takes a single integer parameter and returns the
Line 58: number of days in a month. You assume that:
Line 59: • 1 symbolizes January, 2 means February, …, 11 - November and 12 - December.
Line 60: Now, let us test the boundary values. What we surely need to check is whether our counter really
Line 61: starts with 1 and not with 0. So we need to check that:
Line 62: • 0 fails with an error, while 1 returns a value for January.
Line 63: And similarly, we also need to check "the other end":
Line 64: • 12 returns a value for December, while 13 fails with an error.
Line 65: Analysis of the values that should be checked can lead you to some interesting findings.
Line 66: For example, it seems that the function that takes an integer representing a month could be
Line 67: improved by the introduction of enum Month. That way, passing of bad values will not be a
Line 68: problem anymore. This is an example of what happens when you start thinking about tests,
Line 69: and you consider boundary values. Redesign happens, and better design emerges. And that
Line 70: is a good thing!
Line 71: 7.1.3. Strange Values
Line 72:  So your code is almost bulletproof. It is verified to work well with expected values, and has some
Line 73: border checking capabilities. That is good, but not enough. The code is not yet ready to deal with
Line 74: values that are completely out of order.
Line 75: No matter what values you expect, you can always meet with something unexpected. So, expect the
Line 76: unexpected, likely one of the following:
Line 77: 2See http://en.wikipedia.org/wiki/Boundary-value_analysis and http://en.wikipedia.org/wiki/Off-by-one_error for more
Line 78: information.
Line 79: 3This is true, when working in test-first manner, see Chapter 4, Test Driven Development.
Line 80: 104
Line 81: 
Line 82: --- 페이지 120 ---
Line 83: Chapter 7. Things You Should Know
Line 84: • negative values, when only positive ones make sense (e.g. age),
Line 85: • null or empty values (e.g. empty Strings, empty collections),
Line 86: • data structures not conforming to some expectations, e.g. unsorted (when sorting is assumed) or
Line 87: with duplicates (when no duplicates are expected),
Line 88: • corrupted files (another mime-type than expected, not-valid XML, a binary file instead of text, etc.),
Line 89: • objects of a different type than expected (possible in weakly typed languages).
Line 90: This kind of testing is especially important if your code deals with values entered by
Line 91: the user – be it directly via some WWW form, or by reading information from a file
Line 92: uploaded from the user. When receiving data directly from users be prepared to expect
Line 93: every possible value!
Line 94: Let us consider dates for example. Dates are a common source of confusion and error, because:
Line 95: • they are intrinsically complicated (e.g. leap years, different numbers of days in months),
Line 96: • we use them differently (i.e. various data formats – e.g. YYYY-MM-DD vs. YYYY-DD-MM).
Line 97: So let us say that the function we are testing takes date as String. We expect it to be in YYYY-MM-
Line 98: DD format. The code is already tested to deal with:
Line 99: • normal values - 2011-01-18, 1956-07-14, 2015-12-23, …
Line 100: • boundary values - 2011-02-28 and 2011-02-29, …
Line 101: Now, it should be hardened against unexpected dates. For example, a date entered by a user might be
Line 102: one of the following:
Line 103: • 2011-28-03 - which is YYYY-DD-MM, instead of the required YYYY-MM-DD,
Line 104: • 2011/04/18 - which uses a different group separator,
Line 105: • tomorrow - which is a nice date, but not really what was expected,
Line 106: • null or empty String - this happens all the time,
Line 107: • http://some.address/, I love you Mom or blah (*&$ - it can also happen.
Line 108: 7.1.4. Should You Always Care?
Line 109: "I will spend my life writing tests for this simple function…" If a dreadful thought like this crossed
Line 110: your mind while you were reading the previous section, maybe the next few paragraphs will cheer you
Line 111: up.
Line 112: Let us say you write tests for AgeValidator class. Your web-based application will use it to check
Line 113: the validity of arguments passed from a web form (probably HTML). You know that this form will
Line 114: allow you to input only two digits in the age field. The question is, should you use this knowledge
Line 115: to limit the set of tested values to [0..99]? Does it make sense to write tests that pass 100 or -1 to
Line 116: validateAge() method?4
Line 117: 4Let us assume that tampering with POST data is not possible…
Line 118: 105
Line 119: 
Line 120: --- 페이지 121 ---
Line 121: Chapter 7. Things You Should Know
Line 122: If you were to design all your classes and methods so that they did not depend on the context of your
Line 123: application, they would definitely be more robust and reusable, which in turn would certainly be a
Line 124: good thing. But should you strive for this? This is a common problem you will face. Let us discuss it.
Line 125: In general, you will probably not be expected to write all the code keeping reusability in mind. This
Line 126: would only be the case in some rare situations – i.e. when writing a "library", whose purpose is,
Line 127: precisely, to be reusable. What you are going to be paid for is to build this particular application – not
Line 128: to prepare your code so you can build any application with it. Of course, thinking about reusability
Line 129: is valuable, as it make you code much clean and easier to maintain, so not only your company, but
Line 130: also your own team will surely benefit from the lower maintenance effort. On the other hand, thinking
Line 131: about possible future use breaches the You Ain’t Gonna Need It (YAGNI) principle5. Try to be
Line 132: pragmatic about it.
Line 133: And if you code every component with reusability in mind, your integrated application may perform
Line 134: suboptimally. For example, each component would repeat the same checks (e.g. null values
Line 135: checking). Does it really makes sense to check arguments for being null in the web layer, then pass
Line 136: them to the services layer and repeat the same checks, then pass them further to the DAO layer and
Line 137: perform the same checks? I don’t think so.
Line 138: It is a different case with all "utility" classes. They should be context-free, because the chances of
Line 139: reusing them are much higher than for any other code you write. You should test them with special
Line 140: care, knowing that you cannot assume much about the context they will be used in.
Line 141: As a case in point, the validator class, mentioned previously, falls into the "utility classes" category.
Line 142: As such, I would recommend preparing it for work in any context, without any assumptions about the
Line 143: arguments. That would mean it should be tested taking into account values not from 0 to 9 but from
Line 144: Integer.MIN_VALUE to Integer.MAX_VALUE. I guess that for this validator that would not mean a lot
Line 145: more work. In other cases, though, it might be different.
Line 146:  There are some ways to deal with methods which require many different sets of arguments
Line 147: in order to be properly tested. See Section 3.6 for what JUnit can offer in this respect. If
Line 148: this is something of great importance, you should also look for information on "pairwise
Line 149: testing"6 and tools like quickcheck7.
Line 150: 7.1.5. Not Only Input Parameters
Line 151:  So far, we have only discussed those sorts of case that have allowed us to freely set input parameters.
Line 152: However, in the real world not every input is passed as a method argument. We have already
Line 153: discussed the issues related to indirect inputs provided by DOCs. In case of such interactions of an
Line 154: SUT with DOCs, the same rules apply as were discussed previously. That is, we should write test
Line 155: cases for:
Line 156: • the normal behaviour of the DOC (i.e. that it returns reasonable values or throws reasonable
Line 157: exceptions),
Line 158: • the DOC returning boundary values,
Line 159: 5http://en.wikipedia.org/wiki/You_ain%27t_gonna_need_it
Line 160: 6See http://en.wikipedia.org/wiki/All-pairs_testing
Line 161: 7http://java.net/projects/quickcheck/pages/Home
Line 162: 106
Line 163: 
Line 164: --- 페이지 122 ---
Line 165: Chapter 7. Things You Should Know
Line 166: • the DOC returning unexpected values, i.e. throwing exceptions, that are unlikely to happen.
Line 167: 7.2. How To Choose the Next Test To
Line 168: Write
Line 169:  In section Section 4.2 we skipped over the problem of selecting the next test to implement. In fact,
Line 170: telling you to simply go and write a failing test "just like that" is kind of unfair. It sounds easy, but
Line 171: how should one go about it? Say we have a list of functionalities to be implemented, and a list of tests
Line 172: which cover them. The question we have to deal with right now is how to choose the first test. And
Line 173: then, after you implement it, and finish the TDD circle by implementing the code and refactoring, how
Line 174: to go about the next test? And the next one?
Line 175: This is a standard problem and, as far as I know, no standard answer exists. There is no heuristic that
Line 176: is commonly recognized as the right way to determine the next test to be implemented. However,
Line 177: amongst the community there are some rules of thumb that might be helpful. Let us have a look at
Line 178: them.
Line 179: The Low-Hanging Fruit. 
Line 180: This rule says: "Start with something really simple. Implement an
Line 181: obvious test case."
Line 182: This technique is especially useful if you are stuck. Writing something, even something trivial or
Line 183: of only minimal importance, might be helpful to overcome this sort of "writer’s block". When you
Line 184: have doubts about what tests to write and how the tested method should behave, then making the
Line 185: first step might be the best thing you can do. Even if the functionality implemented in this way is not
Line 186: so important, you will at least get some of the pieces of the puzzle (the SUT class and some of its
Line 187: methods) in place. It might help you to move forward.
Line 188: An example of writing a simple test case just to get you started would be:
Line 189: • writing a parameter-checking test for a function (no matter what the purpose of the function in
Line 190: question might be),
Line 191: • or, when writing a parser, starting with the test case of passing an empty String to the parsing
Line 192: method and receiving null in return8.
Line 193: In neither case would you touch the (probably quite complex) main logic which is to be tested and
Line 194: implemented. However, you would end up with some classes and methods that might give you some
Line 195: insight into the real task ahead. This could be really handy if you are feeling lost and do not know how
Line 196: to proceed.
Line 197: The Most Informative One. 
Line 198: Another approach is to start with the test which gives you the most
Line 199: information about the implemented functionality. This is like striking the ball with the sweet spot: it
Line 200: yields the maximum possible return in terms of knowledge.
Line 201: However, this usually means facing up to the most difficult dilemmas. Well, you are going to have
Line 202: to deal with them anyway, so maybe instead of circling around, why not simply jump right into the
Line 203: action?
Line 204: 8This example is taken from Ash Kim’s discussion of TDD techniques on StackOverflow http://stackoverflow.com/
Line 205: questions/3922258/when-applying-tdd-what-heuristics-do-you-use-to-select-which-test-to-write-next
Line 206: 107
Line 207: 
Line 208: --- 페이지 123 ---
Line 209: Chapter 7. Things You Should Know
Line 210: This approach is like saying "it does not matter that my first match is against the world
Line 211: champion - if I am going to win the whole tournament, I will have to beat him anyway".
Line 212: Some people like this kind of motivation.
Line 213: All good and well, but haven’t we just answered a riddle with another riddle? The question, now,
Line 214: is how to know which test will furnish you with the most knowledge about the implemented
Line 215: functionality? Well, this is not so hard to answer. This is probably the test which you know you still
Line 216: do not know how to make pass. You will simply know which one it is.
Line 217: In the case of the preceding parser example, if you adopted this approach, you will probably start
Line 218: by parsing a full sentence. This would definitely teach you a lot about the functionality being
Line 219: implemented.
Line 220: First The Typical Case, Then Corner Cases. 
Line 221: It seems quite reasonable to start with a "typical
Line 222: case". Think about how you would expect this function to be most frequently used. When writing
Line 223: a tokenizer, start with a valid sentence as an input. When implementing a vending machine, begin
Line 224: with a client inserting a $1 coin and selecting a product which the machine has. Later on, you will
Line 225: implement corner cases.
Line 226: Also, this approach guarantees that you have something valuable working from the very beginning.
Line 227: Even if you get dragged away from your computer (e.g. to some very urgent meeting of the highest
Line 228: importance) you will have already implemented something which is useful for the clients of the SUT.
Line 229: This will be nice.
Line 230: This approach represents a "natural" order of testing, as discussed in (see Section 7.1).
Line 231: Listen To Your Experience. 
Line 232: Probably the most valuable way to deal with the "next test" dilemma
Line 233: is to listen to your experience. It should tell you which one of the above approaches is the most
Line 234: suitable for this particular case. Personally, I like to go with the typical cases first, but it happens that I
Line 235: use other approaches as well.
Line 236: 7.3. How to skip a test?
Line 237: Disclaimer 
Line 238: I debated with myself whether I should include this section in the book at all. There aren’t
Line 239: many legitimate reasons not to run a certain test. In fact, I can remember doing it only a
Line 240: few times in my whole career, and not even once for unit tests. However, your working
Line 241: environment might differ, so I eventually I decided, with considerable hesitation, to devote a
Line 242: few paragraphs to this topic.
Line 243: Bear in mind, please, that skipping tests isn’t what you should do often. And if you do, then
Line 244: maybe your unit tests aren’t so very much unit after all?
Line 245:  Assuming that you have good reasons to skip a test, let us see how you could do that. There is no
Line 246: need for any hand-crafted solutions, as JUnit provides a bunch of annotations exactly for this purpose.
Line 247: The first one of them is named @Disabled. JUnit will ignore any test method marked with this
Line 248: 108
Line 249: 
Line 250: --- 페이지 124 ---
Line 251: Chapter 7. Things You Should Know
Line 252: annotation. Which means, these test methods won’t be executed and they will be marked as ignored in
Line 253: test execution report.
Line 254: Listing 7.1. Skipping a test
Line 255: import org.junit.jupiter.api.Disabled; 
Line 256: public class SkipTest {
Line 257:     @Test
Line 258:     void shouldBeRun() {
Line 259:         System.out.println("running!");
Line 260:     }
Line 261:     @Disabled 
Line 262:     @Test
Line 263:     void shouldBeSkipped() {
Line 264:         System.out.println("huh, not skipped?!"); 
Line 265:     }
Line 266: }
Line 267: The test runner will skip all tests marked with the @Disabled annotation.
Line 268: This message will not be printed.
Line 269: After running, the following output should be printed:
Line 270: running!
Line 271: void com.practicalunittesting
Line 272:   .SkipTest.shouldBeSkipped() is @Disabled
Line 273: In other cases you might want to achieve the same effect, but with the decision postponed until
Line 274: runtime. JUnit provides some out-of-the-box annotations for two typical situations that might make
Line 275: a test irrelevant: differences in operating systems (@EnabledOnOs and @DisabledOnOS annotation)
Line 276: and differences in runtime environments (@EnabledOnJre and @DisabledOnJre). Their use is pretty
Line 277: straightforward as the following code shows:     
Line 278: Listing 7.2. Skipping a test
Line 279: import org.junit.jupiter.api.condition.DisabledOnJre;
Line 280: import org.junit.jupiter.api.condition.DisabledOnOs;
Line 281: import org.junit.jupiter.api.condition.JRE;
Line 282: import org.junit.jupiter.api.condition.OS;
Line 283: public class AssumptionsTest {
Line 284:     @DisabledOnOs(OS.WINDOWS) 
Line 285:     @Test
Line 286:     void dontRunOnWindows() { 
Line 287:         System.out.println("OS name: "
Line 288:             + System.getProperty("os.name"));
Line 289:     }
Line 290:     @DisabledOnJre(JRE.JAVA_11) 
Line 291:     @Test
Line 292:     void weAintReadyForJava11Yet() { 
Line 293:         System.out.println("JAVA version: "
Line 294: 109
Line 295: 
Line 296: --- 페이지 125 ---
Line 297: Chapter 7. Things You Should Know
Line 298:             + System.getProperty("java.version"));
Line 299:     }
Line 300: }
Line 301: JUnit will skip this test method on Windows machine.
Line 302: JUnit will skip this test method on Java 11.
Line 303: There is also a possibility to skip test based on JVM system properties (@EnabledIfSystemProperty)
Line 304: or values of operating system environment variables (@EnabledIfEnvironmentVariable). In both
Line 305: cases their counterparts - @DisabledIfSystemProperty and @EnabledIfEnvironmentVariable -
Line 306: are also available.    
Line 307: To make the picture complete, you should also know that there is an Assumptions class of JUnit
Line 308: that allows you to write any conditions in the form of assumeThat(condition) expressions. If the
Line 309: condition fails, the rest of test method is not executed and the method is marked as ignored. 
Line 310: There is also an Assumptions class provided by AssertJ. Its purpose, however, is different
Line 311: and the semantics differ: test methods that don’t pass the AssertJ assumptions are marked
Line 312: as failed and not as ignored. Don’t confuse it with the Assumptions class of JUnit! 
Line 313: You should only very rarely either ignore tests or just run them under certain conditions.
Line 314: Make sure you have a good reason before doing so!
Line 315: 7.4. More about Expected Exceptions
Line 316: In Section 3.7, we learned almost everything there is to know about testing expected exceptions with
Line 317: JUnit. Still, there is always something more to learn, and this is exactly the moment to discuss it.
Line 318: On some rare occasions it is important to verify whether the exception has been thrown with a proper
Line 319: message or not. This is rarely the case, because the exception message is usually an implementation
Line 320: detail and not something your clients would care about. However, if such a need arises, then the
Line 321: verification of the exception message is pretty straightforward. The following listing illustrates this.
Line 322: Listing 7.3. Verifying an exception
Line 323: import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
Line 324: @Test
Line 325: void testException() {
Line 326:     assertThatExceptionOfType(Exception.class)
Line 327:         .isThrownBy(() -> { 
Line 328:             // SUT.someMethod();
Line 329:         }).withMessageContaining("expected message") 
Line 330:         .withNoCause(); 
Line 331: }
Line 332: The same technique for intercepting exceptions that we learned in Section 3.7.
Line 333: Verification of exception message. Other methods - e.g. withMessageEnding() or
Line 334: withMessage() - also available.
Line 335: Additionally, we can also check the cause of the exceptions. There are a few
Line 336: methods available (e.g. withCauseInstanceOf(), withRootCauseInstanceOf(),
Line 337: withStackTraceContaining()).
Line 338: 110
Line 339: 
Line 340: --- 페이지 126 ---
Line 341: Chapter 7. Things You Should Know
Line 342: AssertJ provides also few dedicated methods that replace the generic method
Line 343: assertThatExceptionOfType() for some quite popular exceptions (NullPointerException,
Line 344: IllegalArgumentException, IOException, IllegalStateException). You can write, for example:
Line 345: assertThatIllegalStateException()
Line 346:   .isThrownBy(() -> {
Line 347:         //SUT.someMethod()
Line 348:   });
Line 349: But if get used to starting verification with assertThat() and dislike the idea of having a different
Line 350: assertion method for exceptions, you can do this as well. This will also please all those who follow the
Line 351: BDD approach to testing (see Section 10.4): 
Line 352: Listing 7.4. Expected exception - BDD style
Line 353: import static org.assertj.core.api.Assertions.*;
Line 354: @Test
Line 355: void testExceptionBDDStyle() {
Line 356:     // given
Line 357:     ...
Line 358:     // when
Line 359:     Throwable thrown = catchThrowable(() -> { 
Line 360:         //SUT.someMethod();
Line 361:     });
Line 362:     // then
Line 363:     assertThat(thrown)
Line 364:         .isInstanceOf(MyException.class) 
Line 365:         .hasMessageContaining("boom")
Line 366:         .hasCause(IOException.class);
Line 367: }
Line 368: We catch Throwable here…
Line 369: …to verify it at the end of test method.
Line 370: 7.5. Mockito Exceptions
Line 371: Using a similar syntax, we can also instruct test doubles to throw exceptions. This is shown in Listing
Line 372: 7.5.
Line 373: This feature of mocking frameworks - throwing exceptions on demand - is extremely
Line 374: useful for simulating all kinds of errors that can happen during the execution of your
Line 375: application. It is especially important when testing possible scenarios involving
Line 376: cooperation with some third-party components - e.g. databases or web services. 
Line 377: Listing 7.5. myFerrari throws an exception
Line 378: public class MockitoThrowingExceptionsTest {
Line 379:     private Car myFerrari = mock(Car.class);
Line 380: 111
Line 381: 
Line 382: --- 페이지 127 ---
Line 383: Chapter 7. Things You Should Know
Line 384:     @Test(expected = RuntimeException.class) 
Line 385:     void throwException() {
Line 386:         when(myFerrari.needsFuel())
Line 387:             .thenThrow(new RuntimeException()); 
Line 388:         myFerrari.needsFuel(); 
Line 389:     }
Line 390: }
Line 391: The test passes because myFerrari throws the expected exception as instructed.
Line 392: Expectations set.
Line 393: This test also passes, as myFerrari obediently throws an exception when its needsFuel() method is
Line 394: executed.
Line 395: You need to use a different syntax when setting expectations on void methods. This is
Line 396: discussed in Section 7.6.
Line 397: 7.6. Stubbing Void Methods
Line 398:  Sometimes it is required to stub void methods. Mockito allows to do it, but there is a small catch: the
Line 399: syntax differs substantially from what we have learned so far. For example, to stub the behaviour of
Line 400: someMethod() method you would usually write the following:
Line 401: Listing 7.6. Stubbing a non-void method
Line 402: when(someObject.someMethod()).thenReturn("some value");
Line 403: However, if a method returns void, then the syntax differs (obviously it does not make sens to return
Line 404: anything from void method, so in the example below we instruct the voidMethod() to throw an
Line 405: exception):
Line 406: Listing 7.7. Stubbing a void method
Line 407: doThrow(new IllegalArgumentException("bad argument!"))
Line 408:     .when(someObject).voidMethod();
Line 409: As the original Mockito’s documentation states, this different syntax is required, because: "Stubbing
Line 410: voids requires different approach from when(Object) because the compiler does not like void
Line 411: methods inside brackets…".
Line 412: Apart from the doThrow() method, there are two other methods which may help when
Line 413: working with void methods: doNothing() and doAnswer(). Mockito documentation
Line 414: discusses them in detail, giving very good examples for both.
Line 415: 7.7. Mockito Matchers
Line 416:  Continuing our discussion on matchers, let us take a look at their use in specific, test-double related
Line 417: cases. So far we have been very specific as to the arguments of methods that we have been instructing
Line 418: Mockito to return when stubbing. Similarly, when verifying test doubles’ behaviour, we have
Line 419: 112
Line 420: 
Line 421: --- 페이지 128 ---
Line 422: Chapter 7. Things You Should Know
Line 423: expected certain methods to be called with certain values. For example, in Section 5.4.5 we verified
Line 424: whether client had received a specific message object or not. This makes sense, but sometimes
Line 425: expressing the arguments of calls in such detail is too rigid, as well as being simply unnecessary. In
Line 426: this section we will learn how to make our tests more relaxed by using argument matchers provided
Line 427: by Mockito.
Line 428: But first things first, why bother at all with such a feature? Basically, there are two good reasons for
Line 429: doing so:
Line 430: • improved readability coming from the fact that code with matchers can be read like natural
Line 431: language (well, almost…),
Line 432: • improved maintainability thanks to the omitting of some unimportant details within the test code
Line 433: by means of more relaxed matchers.
Line 434: Mockito offers a variety of predefined matchers which can be used for verification or stubbing.
Line 435: There are a great many of them, some being just aliases of others, simply for the sake of ensuring
Line 436: the readability of your tests. The list below gives only a subset of all of the matchers offered by
Line 437: org.mockito.ArgumentMatchers class:       
Line 438: • any() matches any object (or null),
Line 439: • anyVararg() matches any number and values of arguments,
Line 440: • isNull(), isNotNull() match null and not-null values respectively,
Line 441: • anyBoolean(), anyByte(), anyChar(), anyDouble(), anyFloat(), anyInt(), anyLong(),
Line 442: anyShort(), anyString() match these Java types (or null),
Line 443: • isA(Class<T> clazz) matches any object of a given class,
Line 444: • same(T value) matches an object which is the same (==) to a given object,
Line 445: • anyCollection(), anyList(), anyMap(), anySet() matches any kind of instance of each sort of
Line 446: collection (or null),
Line 447: • refEq(T value, String… excludeFields) matches an object that is reflection-equal to the
Line 448: given value; allows us to specify excluded fields, not to be taken into account,
Line 449: • eq(boolean value), eq(byte value), eq(char value), eq(double value), eq(float
Line 450: value), eq(int value), eq(long value), eq(short value), eq(T value) - matches values
Line 451: which are equal to given arguments.
Line 452: Many of the above methods also exists with additional arguments (of the java.lang.Class type) to
Line 453: make them generics-friendly: i.e. to avoid compiler warnings.
Line 454: There are also some utility matchers for working with String arguments:    
Line 455: • startsWith(String prefix), endsWith(String suffix) match a string that starts/ends with
Line 456: the prefix/suffix that is given,
Line 457: • contains(String substring) matches a string that contains a given substring,
Line 458: 113
Line 459: 
Line 460: --- 페이지 129 ---
Line 461: Chapter 7. Things You Should Know
Line 462: • matches(String regex) matches a string that matches a given regular expression.
Line 463: Such matchers are useful for specifying some "generic" stubbing behaviour or expectations. For
Line 464: example, such code will make the userDAO stub return the object user every time its getUser()
Line 465: method is called, regardless of what ID parameter is passed there.
Line 466: Listing 7.8. Use of the anyInt() matcher
Line 467: import static org.mockito.ArgumentMatchers.anyInt;
Line 468: UserDAO userDAO = mock(UserDAO.class);
Line 469: User user = new User();
Line 470: when(userDAO.getUser(anyInt())).thenReturn(user); 
Line 471: assertEquals(user, userDAO.getUser(1));
Line 472: assertEquals(user, userDAO.getUser(2));
Line 473: assertEquals(user, userDAO.getUser(3));
Line 474: verify(userDAO, times(3)).getUser(anyInt()); 
Line 475: Stubbing of userDAO using an anyInt() matcher.
Line 476: Verification that getUser() was called three times with some int argument.
Line 477: The listing above shows you how to get rid of specific values and use more relaxed arguments when
Line 478: stubbing or verifying your code. This feature of Mockito is highly compatible with the approach that
Line 479: Mockito itself promotes – namely, only specifying in your tests what actually needs to be specified.
Line 480: So, if it is not crucial for your test logic that getUser() gets an argument equal to 789, then maybe
Line 481: anyInt() would be good enough? If so, do not hesitate. Work at the right abstraction level, hiding the
Line 482: unimportant details beneath the handy matchers we have just been learning about.
Line 483: 7.7.1. Hamcrest Matchers Integration
Line 484:  Last but not least, the Matchers class also provides a set of methods that will facilitate using custom
Line 485: Hamcrest matchers within your Mockito-based test code:   
Line 486: • argThat(org.hamcrest.Matcher<T> matcher), which uses a given matcher,
Line 487: • booleanThat(Matcher<Boolean> matcher), byteThat(Matcher<Byte> matcher),
Line 488: charThat(Matcher<Character> matcher), doubleThat(Matcher<Double> matcher),
Line 489: floatThat(Matcher<Float> matcher), intThat(Matcher<Integer> matcher),
Line 490: longThat(Matcher<Long> matcher), shortThat(Matcher<Short> matcher), all of which will
Line 491: match on the basis of matchers of the specified type.
Line 492: By allowing any custom Hamcrest matcher to pass, we gain limitless possibilities for writing highly
Line 493: readable testing code. The use of matcher libraries in test code is discussed in Appendix B, Fluent
Line 494: Assertions, so right now let us conclude with just one example: 
Line 495: Listing 7.9. Use of Hamcrest matchers with Mockito
Line 496: import static org.mockito.hamcrest.MockitoHamcrest.argThat; 
Line 497: import static org.hamcrest.Matchers.hasEntry;
Line 498: 114
Line 499: 
Line 500: --- 페이지 130 ---
Line 501: Chapter 7. Things You Should Know
Line 502: User user = new User();
Line 503: UserDAO userDAO = mock(UserDAO.class);
Line 504: when(userDAO.getUserByProperties((Map<String, String>)
Line 505:     argThat(hasEntry("id", "2")))).thenReturn(user); 
Line 506:   Map<String, String> emptyProperties = new HashMap<String, String>();
Line 507:   assertThat(userDAO.getUserByProperties(emptyProperties))
Line 508:                   .isNull();  
Line 509:   Map<String, String> properties = new HashMap<String, String>();
Line 510:   properties.put("id", "2");
Line 511:   assertThat(userDAO.getUserByProperties(properties))
Line 512:     .isEqualTo(user); 
Line 513: The necessary static methods are imported.
Line 514: Our use of the Hamcrest matcher hasEntry() must be wrapped in the argThat() method of
Line 515: Mockito9.
Line 516: This map does not fulfill the requirement - no user will be returned (as discussed previously,
Line 517: Mockito returns null in such cases).
Line 518: Now the map contains the entry required by the matcher, so a real user will be returned.
Line 519: "Limitless possibilities" are opened up, in that it is possible to write custom Hamcrest matchers
Line 520: that can then be used within the argThat() method in just the same way as the original Hamcrest
Line 521: matchers are used.
Line 522: I bet that you will only rarely find a real need for such sophisticated argument matching.
Line 523: 7.7.2. Matchers Warning
Line 524: One thing to remember is that if you are using argument matchers, all arguments have to be
Line 525: provided by matchers. This is shown with the following snippet of code (an example copied directly
Line 526: from Mockito documentation):
Line 527: Listing 7.10. The requirement to use matchers for all arguments
Line 528: verify(mock).someMethod(anyInt(), anyString(), eq("third argument")); 
Line 529: verify(mock).someMethod(anyInt(), anyString(), "third argument"); 
Line 530: This is correct: all argument are matchers.
Line 531: This is incorrect: the third argument is not a matcher and will result in an exception being
Line 532: thrown.
Line 533: 7.8. Unit Testing Asynchronous Code
Line 534: Chuck Norris can test multi-threaded applications with a single thread.
Line 535: 9This is because all Hamcrest matcher methods return objects of the org.hamcrest.Matcher<T> type, while Mockito
Line 536: matchers return objects of the T type.
Line 537: 115
Line 538: 
Line 539: --- 페이지 131 ---
Line 540: Chapter 7. Things You Should Know
Line 541: — Wisdom of the Internet ;)
Line 542: Often we write code which delegates some task to be run "in the background", so the caller of our
Line 543: code will not have to wait for it to finish. This very popular scenario is usually handled with the
Line 544: java.util.concurrent.ExecutorService10.
Line 545: I do not plan to go into details concerning writing asynchronous Java code. For the purpose of
Line 546: this discussion it will suffice to say that the implementation of the ExecutorService interface is
Line 547: capable of running tasks (Runnable and Callable) asynchronously. The submit() method of the
Line 548: ExecutorService interface returns immediately, even if the execution of the task passed to it lasts for
Line 549: some time. 
Line 550: An example of such an approach is shown in Listing 7.11. A server receives a request and handles all
Line 551: the tasks of this request. The tasks are handled asynchronously.
Line 552: Listing 7.11. Starting tasks asynchronously with ExecutorService
Line 553: public class Server {
Line 554:     private final ExecutorService executorService;
Line 555:     private final TaskService taskService;
Line 556:     public Server(ExecutorService executorService, TaskService taskService) { 
Line 557:         this.executorService = executorService;
Line 558:         this.taskService = taskService;
Line 559:     }
Line 560:     public void serve(Collection<Task> tasks) {
Line 561:         for (Task task : tasks) {
Line 562:             executorService.submit(new TaskHandler(taskService, task)); 
Line 563:         }
Line 564:     }
Line 565:     private class TaskHandler implements Runnable { 
Line 566:         private final TaskService taskService;
Line 567:         private final Task task;
Line 568:         public TaskHandler(TaskService taskService, Task task) {
Line 569:             this.taskService = taskService;
Line 570:             this.task = task;
Line 571:         }
Line 572:         public void run() {
Line 573:             ... 
Line 574:             taskService.handle(task); 
Line 575:         }
Line 576:     }
Line 577: }
Line 578: Collaborators of the Server class are injected via a constructor.
Line 579: The submit() method of the ExecutorService returns immediately, even if the execution of
Line 580: the Runnable that was passed to it takes some time.
Line 581: The TaskHandler class implements the Runnable interface.
Line 582: 10See http://docs.oracle.com/javase/6/docs/api/java/util/concurrent/ExecutorService.html
Line 583: 116
Line 584: 
Line 585: --- 페이지 132 ---
Line 586: Chapter 7. Things You Should Know
Line 587: The run() method is responsible for "doing the real work". We need not concern ourselves with
Line 588: what it does, but let us assume that its execution takes a significant amount of time.
Line 589: Here the handle() method of the TaskService class is invoked, which finishes the execution of
Line 590: the run() method.
Line 591: Now let us test the following scenario: We will send a request to the server and verify whether the
Line 592: handle() method of the TaskService class has been executed.
Line 593: Hmm…. It seems that to have real unit tests we should write tests for two classes:
Line 594: • for the Server class to verify whether it submits all tasks to its executorService collaborator,
Line 595: • and for the TaskHandler class to verify whether its run() method invokes the handle() method of
Line 596: the taskService collaborator.
Line 597: But this is not possible, because the TaskHandler class is private (and we would like to keep it that
Line 598: way). So the other option we have is to test the two classes - Server and TaskHandler - together, in
Line 599: this way stretching our notion of what constitutes a "unit". This hardly seems terrible, given that the
Line 600: two classes are coupled together so very tightly.
Line 601: Sounds simple, so let’s go ahead and do it, based on what we already know about mocks. The
Line 602: only question we should answer is what to do with ExecutorService. Should we use its real
Line 603: implementation or replace it with a test double? The first option seems better to me. First of all,
Line 604: the functionality we are testing is contained within two types (Server and ExecutorService),
Line 605: so mocking just one of them would be awkward. Secondly, there are many definitely valid
Line 606: implementations of the ExecutorService interface provided by the mighty Java itself, so we need
Line 607: not worry about bugs within this collaborator of the ExecutorService class. Last but not least, we
Line 608: should stick to the good old rule which says "mock only types that you own"11: this tells us that since
Line 609: we don’t own the ExecutorService (in that we haven’t written it and have no control over its further
Line 610: development) we should not mock it. In sum, then, our decision is that we should use some real
Line 611: implementation of this interface.
Line 612: Listing 7.12. Testing asynchronous code - a naive approach
Line 613: @Test
Line 614: void shouldSaveTasks() throws InterruptedException {
Line 615:     ExecutorService executorService = Executors.newCachedThreadPool(); 
Line 616:     TaskService taskService = mock(TaskService.class); 
Line 617:     Task task = mock(Task.class);
Line 618:     Collection<Task> listOfTasks = Arrays.asList(task);
Line 619:     Server server = new Server(executorService, taskService);
Line 620:     server.serve(listOfTasks); 
Line 621:     verify(taskService).handle(task); 
Line 622: }
Line 623: Collaborators of the SUT. As was previously decided, we mock an object of the TaskService
Line 624: class and use a real implementation of the ExecutorService interface.
Line 625: The execution of the serve() method initiates the asynchronous task.
Line 626: 11See http://stevef.truemesh.com/archives/000194.html
Line 627: 117
Line 628: 
Line 629: --- 페이지 133 ---
Line 630: Chapter 7. Things You Should Know
Line 631: Verification occurs of whether the handle() method of the taskService collaborator is
Line 632: invoked at the end of the execution.
Line 633: Will it work? Unfortunately not. At the time when Mockito runs the verification part of the test, the
Line 634: asynchronously invoked operations are still in progress, and the handle() method has not yet been
Line 635: invoked.
Line 636: 7.8.1. Waiting for the Asynchronous Task to Finish
Line 637: It seems that we need to wait for the asynchronous task to finish. Let’s suppose that the first idea we
Line 638: come up with is to put a Thread.sleep() into our test code, like this: 
Line 639: Listing 7.13. Testing asynchronous code - with Thread.sleep()
Line 640: @Test
Line 641: void shouldSaveTasks() throws InterruptedException {
Line 642:     ...
Line 643:     server.serve(listOfTasks);
Line 644:     Thread.sleep(1000);
Line 645:     verify(taskService).handle(task);
Line 646: }
Line 647: Now the test is green and… slow! Every time we run it we lose 1 second. This does not seem to be a
Line 648: lot, but if you think about it you will come to the conclusion that it is a bad situation. What if we have
Line 649: more tests like this and the waiting time grows to 15 seconds, or maybe a minute? This would not be
Line 650: acceptable, as it would eventually lead to developers not running tests.
Line 651: Of course, we could perform some fine-tuning and make the sleep shorter, but this is a risky business.
Line 652: There is a risk that under some circumstances (on a different machine, or when garbage collection
Line 653: interferes) the waiting time will be too short, and the test will fail. False alarms are an awful thing –
Line 654: they make people indifferent to tests turning red!
Line 655: Pursuing the direction we have already gone in (i.e. waiting till the asynchronous task is finished), we
Line 656: could do a little better if we repeatedly execute the verification until it succeeds, or until the execution
Line 657: time exceeds some reasonable value. This could be done with the try-catch statement, or with some
Line 658: fancy framework like Awaitility12. Both solutions are presented in the next two listings.
Line 659: Listing 7.14. Testing asynchronous code - with Thread.sleep() within a for loop
Line 660: @Test
Line 661: void shouldSaveTasksUsingTryCatch() throws InterruptedException {
Line 662:     final TaskService taskService = mock(TaskService.class);
Line 663:     ExecutorService executorService = Executors.newCachedThreadPool();
Line 664:     final Task task = mock(Task.class);
Line 665:     Collection<Task> listOfTasks = Arrays.asList(task);
Line 666:     Server server = new Server(executorService, taskService);
Line 667:     server.serve(listOfTasks);
Line 668:     boolean handleMethodInvoked = false; 
Line 669: 12See http://www.awaitility.org/.
Line 670: 118
Line 671: 
Line 672: --- 페이지 134 ---
Line 673: Chapter 7. Things You Should Know
Line 674:     for (int i = 0; i < 10 && !handleMethodInvoked ; i++) { 
Line 675:         try {
Line 676:             verify(taskService).handle(task); 
Line 677:             handleMethodInvoked = true; 
Line 678:         }
Line 679:         catch (AssertionError e) { 
Line 680:             // no need to do anything
Line 681:         }
Line 682:         Thread.sleep(100); 
Line 683:     }
Line 684:     assertThat(handleMethodInvoked).isTrue(); 
Line 685: }
Line 686: This flag will allow us to verify whether the expected handle() method has really been
Line 687: executed.
Line 688: The maximum waiting time is 1 second (100 milliseconds multiplied by 10).
Line 689: If the verification fails, then an AssertionError will be thrown. There is nothing we need do
Line 690: within the catch clause, because we will want to try again after some time.
Line 691: If we get there, it means the verification has succeeded.
Line 692: Let us see whether, during the (maximum) time of 1 second, the expected method was invoked.
Line 693: Is it better than the previous version? Yes, because it is guaranteed that we will wait, at the very most,
Line 694: 100 milliseconds longer after the task finished, and at the same time we will never wait longer than 1
Line 695: second. However, the code gets complicated. To enhance its readability, we could extract the for loop
Line 696: into some private utility method or create a custom assertion (see Section 6.1).
Line 697: Another way we could improve the situation is to replace the for loop with some nice DSL offered by
Line 698: the Awaitility framework. This is presented in the next listing.
Line 699: Listing 7.15. Testing asynchronous code - with Awaitility
Line 700: Awaitility.await()
Line 701:     .atMost(1, SECONDS)
Line 702:     .with().pollInterval(100, MILLISECONDS)
Line 703:     .until(new Callable<Boolean>() {
Line 704:         @Override
Line 705:         public Boolean call() throws Exception {
Line 706:             try {
Line 707:                 verify(taskService).handle(task);
Line 708:                 return true;
Line 709:             } catch(AssertionError ae) {
Line 710:                 return false;
Line 711:             }
Line 712:         }
Line 713:     });
Line 714: Personally I do not like the try-catch version of this test. It is much more complicated than the usual
Line 715: tests. The second version - which uses Awaitility - is more readable, but even so, it also requires us to
Line 716: catch a class of the Error type, which goes against the common rules of Java coding.
Line 717: Spend some time learning about the Awaitility framework. You won’t use it a lot in
Line 718: unit tests, but it can do wonders to your test code in your integration or end-to-end tests,
Line 719: making it much more readable.
Line 720: 119
Line 721: 
Line 722: --- 페이지 135 ---
Line 723: Chapter 7. Things You Should Know
Line 724: 7.8.2. Making Asynchronous Synchronous
Line 725: So far we have been concentrating on waiting for the asynchronous code. This is possible, but not
Line 726: without some drawbacks. Let us try a different approach now.
Line 727: Let us take a look again at the code in Listing 7.11. Can you see anything which makes it
Line 728: asynchronous? No, there is nothing of that sort there. The asynchronous nature of this code is
Line 729: "injected" by a concrete implementation of the ExecutorService, which means, in turn, that if we
Line 730: provide a synchronous implementation of this interface, it will make our situation much simpler. At
Line 731: the same time, by doing this we won’t breach the contract of the ExecutorService. Even if it was
Line 732: designed with asynchronicity in mind, it does not demand implementations to provide such a feature.
Line 733: Listing 7.16 presents such a sample implementation.
Line 734: Listing 7.16. SynchronousExecutorService
Line 735: public class SynchronousExecutorService extends AbstractExecutorService { 
Line 736:     private boolean shutdown;
Line 737:     public void shutdown() {
Line 738:         shutdown = true;
Line 739:     }
Line 740:     public List<Runnable> shutdownNow() {
Line 741:         shutdown = true;
Line 742:         return Collections.emptyList();
Line 743:     }
Line 744:     public boolean isShutdown() {
Line 745:         shutdown = true;
Line 746:         return shutdown;
Line 747:     }
Line 748:     public boolean isTerminated() {
Line 749:         return shutdown;
Line 750:     }
Line 751:     public boolean awaitTermination(
Line 752:                         final long timeout,
Line 753:                         final TimeUnit unit) {
Line 754:         return true;
Line 755:     }
Line 756:     public void execute(final Runnable command) { 
Line 757:         command.run();
Line 758:     }
Line 759: }
Line 760: This implementation extends the java.util.concurrent.AbstractExecutorService class,
Line 761: which allows us to implement only selected methods of the ExecutorService interface.
Line 762: This is the most important part of this class: instead of executing the command in a separate
Line 763: thread we simply run it synchronously.
Line 764: If we inject this synchronous implementation into the tested instance of the Server class, we discover
Line 765: that the test is now trivial. By removing the asynchronicity we have simplified this case, turning it into
Line 766: a normal one. There is no need for any waiting within the test code.
Line 767: 120
Line 768: 
Line 769: --- 페이지 136 ---
Line 770: Chapter 7. Things You Should Know
Line 771: Listing 7.17. Testing asynchronous code - using SynchronousExecutorService
Line 772: @Test
Line 773: void shouldSaveTasks() {
Line 774:     TaskService taskService = mock(TaskService.class);
Line 775:     ExecutorService executorService = new SynchronousExecutorService();
Line 776:     Server server = new Server(executorService, taskService);
Line 777:     Task task = mock(Task.class);
Line 778:     Collection<Task> listOfTasks = Arrays.asList(task);
Line 779:     server.serve(listOfTasks);
Line 780:     verify(taskService).handle(task);
Line 781: }
Line 782: 7.8.3. Conclusions
Line 783: In this section we have learned how to write unit tests for code which spawns new threads. We have
Line 784: learned two ways of doing this. The first option is to wait (preferably by constant polling) for the
Line 785: desired thing to happen. The second option is to reduce the asynchronous code to its synchronous
Line 786: counterpart and then solve it using a standard approach.
Line 787: If you are interested in testing asynchronous and concurrent code then [goetz2006] is
Line 788: probably the book for you to read.
Line 789: 7.9. Time is not on Your Side
Line 790: Time is making fools of us again.
Line 791: — J.K. Rowling Harry Potter and the Half-Blood Prince (2005)
Line 792: Alas, after all the years of software development we still cannot get it right! The number of bugs
Line 793: related to time formatting and storage is horrifying. Wikipedia gives a lot of examples of such issues,
Line 794: with the famous Y2K problem among them13. There is definitely something complicated connected
Line 795: with time – something which makes us write code not in conformity with its quirky and unpredictable
Line 796: nature. In this section we will see how to deal with classes whose behaviour is determined by time.
Line 797:  A typical example of a time-dependent class is shown in Listing 7.18. The code itself is trivial, but
Line 798: testing such code is not.
Line 799: Listing 7.18. Time-dependent code
Line 800: public class Hello {
Line 801:     public String sayHello() {
Line 802:         Calendar current = Calendar.getInstance(); 
Line 803:         if (current.get(Calendar.HOUR_OF_DAY) < 12) {
Line 804:             return "Good Morning!";
Line 805:         } else {
Line 806:             return "Good Afternoon!";
Line 807:         }
Line 808: 13See http://en.wikipedia.org/wiki/Time_formatting_and_storage_bugs
Line 809: 121
Line 810: 
Line 811: --- 페이지 137 ---
Line 812: Chapter 7. Things You Should Know
Line 813:     }
Line 814: }
Line 815: Returns the current date (at the time of the test’s execution).
Line 816: Please do not be offended by this "HelloWorld" style example. Its point is that it
Line 817: encapsulates everything problematic about the unit testing of time-dependent code. I have
Line 818: seen complicated business code with exactly the same issue as is shown in Listing 7.18. If
Line 819: you learn to solve the problem of Hello class, you will also know how to deal with much
Line 820: more complicated logic.
Line 821: Whatever test we write in connection with this simple Hello class, its result will depend on the time
Line 822: of execution. An example is shown in Listing 7.19. After execution, one of the tests will fail. This is
Line 823: something we cannot accept. What is expected of unit tests is that they abstract from the environment
Line 824: and make sure that a given class always works.
Line 825: Listing 7.19. Time-dependent code - a failing test
Line 826: public class HelloTest {
Line 827:     @Test
Line 828:     void shouldSayGoodMorningInTheMorning() {
Line 829:         Hello hello = new Hello();
Line 830:         assertEquals("Good Morning!", hello.sayHello()); 
Line 831:     }
Line 832:     @Test
Line 833:     void shouldSayGoodAfternoonInTheAfternoon() {
Line 834:         Hello hello = new Hello();
Line 835:         assertEquals("Good Afternoon!", hello.sayHello()); 
Line 836:     }
Line 837: }
Line 838: One of these assertions will fail.
Line 839: We need to think of something different… But what on Earth could help us to win a fight against the
Line 840: tyranny of time? Hmm…
Line 841: Chuck to the rescue
Line 842: Now this book will suddenly turn intimate as I have a little secret of mine to share. Read
Line 843: carefully, ‘cause it can do wonders for you, as it did for me. So, whenever I’m in doubt,
Line 844: whenever I see no clear path to follow, whenever I feel I’m not up to the job… Then I ask
Line 845: myself: "What would Chuck Norris do?". And the enlightenment comes almost instantly! Try
Line 846: it and you will see.
Line 847: Take this "time problem" we have right now. You might feel lost and don’t know what to do.
Line 848: But read this sentence and everything will get clear:
Line 849: When Chuck Norris sets his watch, he sets time itself.
Line 850: — Wisdom of the Internet ;)
Line 851: 122
Line 852: 
Line 853: --- 페이지 138 ---
Line 854: Chapter 7. Things You Should Know
Line 855: …Eureka! Let us be like Chuck, and control the time itself! Speaking in programming terms, the trick
Line 856: is to make time a collaborator of the Hello class. In order to do this, we need to:
Line 857: • create a new interface of TimeProvider that would encapsulate all operations related to time,
Line 858: • redesign Hello class a little bit, so it uses this TimeProvider instead of using the Calendar class
Line 859: directly.
Line 860: If you just had an "aha!" moment and the term dependency injection sprang up in your
Line 861: head then you are on the right track!
Line 862: Listing 7.20. The TimeProvider interface
Line 863: /**
Line 864:  * Allows for taking control over time in unit tests.
Line 865:  */
Line 866: public interface TimeProvider {
Line 867:     Calendar getTime();
Line 868: }
Line 869: A default implementation of this TimeProvider interface would probably reuse the system calendar
Line 870: (Calendar.getInstance()). But we wouldn’t use it for testing purposes.
Line 871: Now let us see what the redesigned Hello class would look like:
Line 872: Listing 7.21. Time as a collaborator
Line 873: public class HelloRedesigned {
Line 874:     private TimeProvider timeProvider;
Line 875:     public HelloRedesigned(TimeProvider timeProvider) { 
Line 876:         this.timeProvider = timeProvider;
Line 877:     }
Line 878:     public String sayHello() {
Line 879:         Calendar current = timeProvider.getTime(); 
Line 880:         if (current.get(Calendar.HOUR_OF_DAY) < 12) {
Line 881:             return "Good Morning!";
Line 882:         } else {
Line 883:             return "Good Afternoon!";
Line 884:         }
Line 885:     }
Line 886: }
Line 887: The TimeProvider collaborator has been injected as a constructor parameter, which means it is
Line 888: easily replaceable with a test double.
Line 889: timeProvider.getTime() is used instead of Calendar.getInstance().
Line 890: An inquisitive reader may notice that the design of our HelloRedesigned class can still be
Line 891: improved by moving more functionality into the TimeProvider class. We will address this
Line 892: in one of the exercises at the end of this chapter (see Section 7.13).
Line 893: Suddenly, the tests of the redesigned Hello class have become trivial.
Line 894: 123
Line 895: 
Line 896: --- 페이지 139 ---
Line 897: Chapter 7. Things You Should Know
Line 898: Listing 7.22. Testing time - setting the stage
Line 899: public class HelloRedesignedTest {
Line 900:     private HelloRedesigned hello;
Line 901:     private TimeProvider timeProvider;
Line 902:     @BeforeEach
Line 903:     void setUp() { 
Line 904:         timeProvider = mock(TimeProvider.class);
Line 905:         hello = new HelloRedesigned(timeProvider);
Line 906:     }
Line 907:     ...
Line 908: }
Line 909: Here a mock of TimeProvider has been created and injected into the SUT14.
Line 910: Listing 7.23. Testing time - morning
Line 911:     ...
Line 912:     private static final Object[] morningHours() {
Line 913:         return $(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);
Line 914:     }
Line 915:     @Test
Line 916:     @Parameters(method = "morningHours") 
Line 917:     void shouldSayGoodMorningInTheMorning(int morningHour) {
Line 918:         when(timeProvider.getTime())
Line 919:             .thenReturn(getCalendar(morningHour)); 
Line 920:         assertEquals("Good Morning!", hello.sayHello());
Line 921:     }
Line 922: Test methods takes parameters provided by data provider.
Line 923: Here we have stubbing of the timeProvider test double.
Line 924: Listing 7.24. Testing time - afternoon
Line 925:     ...
Line 926:     private static final Object[] afternoonHours() {
Line 927:         return $(12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23);
Line 928:     }
Line 929:     @Test
Line 930:     @Parameters(method = "afternoonHours") 
Line 931:     void shouldSayGoodAfternoonInTheAfternoon(int afternoonHour) {
Line 932:         when(timeProvider.getTime())
Line 933:             .thenReturn(getCalendar(afternoonHour)); 
Line 934:         assertEquals("Good Afternoon!", hello.sayHello());
Line 935:     }
Line 936:     private Calendar getCalendar(int hour) {
Line 937: 14Because the test-fixture setting code grew, I decided to put it into a separate method. See Section 8.3 for some discussion.
Line 938: 124
Line 939: 
Line 940: --- 페이지 140 ---
Line 941: Chapter 7. Things You Should Know
Line 942:         Calendar cal = Calendar.getInstance();
Line 943:         cal.set(Calendar.HOUR_OF_DAY, hour);
Line 944:         return cal;
Line 945:     }
Line 946: }
Line 947: Test methods takes parameters provided by data provider.
Line 948: Here we have stubbing of the timeProvider test double.
Line 949: If you run this new test it should pass. No matter if it is 3 am or 6 pm, it will pass. Apparently, time is
Line 950: not a issue anymore. :)
Line 951: Redesign Is Not The Only Way. 
Line 952: This redesign trick (i.e. implementing time provider as a separate
Line 953: entity) is not the only way of dealing with such time-dependent code. Using tools like PowerMock
Line 954: or JMockit it is possible to convince the Calendar class to return whatever value we want. I do not
Line 955: recommend such solutions, because they do not make the SUT’s code any better. Instead they make
Line 956: its current implementation fixed, by repeating some of its implementation details within the test code
Line 957: (see Section 8.7 for a discussion of the trade-offs between the redesign option and its alternatives).
Line 958: Nevertheless, I do believe you should know about the different options – which is why I mention
Line 959: them. 
Line 960: 7.9.1. Test Every Date (Within Reason)
Line 961: Now that we know how to deal with time-dependent code - it really is that simple! - it is time for some
Line 962: general, but nevertheless very important, remarks. 
Line 963: Numerous bugs relate to undertested code, which depends on time. Developers seem to share a naive
Line 964: faith that "if it works today, then it should also work tomorrow". Well, not necessarily. The point I
Line 965: want to make is that you should be really, really cautious when dealing with time, which in essence
Line 966: means the following:
Line 967: • be pedantic when writing unit tests for such code,
Line 968: • run your tests with at least a few subsequent years in mind.
Line 969: With unit tests, there really is no excuse for not running tests for all possible dates or hours. Why not
Line 970: run tests for 5 years in advance, if your tests are ultra-fast? Just do it and then you can rest confident
Line 971: that for the next five years you will not encounter any time-related issue in that particular piece of
Line 972: code.
Line 973: Date assertions
Line 974: And since we are talking of time. If you were to perform assertions on dates, then
Line 975: you should definitely check out what AssertJ offers. All you have to do is it call the
Line 976: assertThat(someDate) method and it gives you access to all the assertions provided by
Line 977: DateAssert. For example:
Line 978: assertThat(date)
Line 979:     .isAfterYear(1999)
Line 980:     .isInSameMonthAs(anotherDate)
Line 981:     .isEqualToIgnoringMinutes(anotherDateAsString)
Line 982: 125
Line 983: 
Line 984: --- 페이지 141 ---
Line 985: Chapter 7. Things You Should Know
Line 986: 7.9.2. Conclusions
Line 987: In this section we have discussed how to deal with time-dependent SUTs. The solution is quite
Line 988: simple: make time one of the SUT’s collaborators, and then do exactly what you would with other
Line 989: collaborators: replace it with a test double. Once you have done this, your design will be improved
Line 990: (the SUT is freed from time-management knowledge and can focus on business logic), and you can
Line 991: then proceed with a standard approach to all collaborators. Yes, this is enough to triumph over time (at
Line 992: least in unit tests). :)
Line 993: The technique presented in this section is sufficient to deal with the time problem at the unit-testing
Line 994: level. However, it does not solve many problems related to time that you will encounter when testing
Line 995: applications on a higher level. The different time-zones of servers and databases, triggers in databases,
Line 996: or external processes running only during certain hours of the night, as well as security certificates
Line 997: whose viability expires, will all give you a good deal of trouble. Fortunately, though, none of these
Line 998: affect unit tests!
Line 999: 7.10. Testing Collections
Line 1000: Sometimes the methods of SUTs return collections whose content is the outcome of an SUT’s
Line 1001: business logic: of course, this is something to be tested. This section provides some information on
Line 1002: testing collections and their content.
Line 1003: 7.10.1. Specialised Assertions
Line 1004: AssertJ offers a bunch of interesting assertions that make verification of collections and arrays quite
Line 1005: simple. I would strongly encourage you to browse the project’s Javadocs to learn about them. Below,
Line 1006: you will find a short summary of what you can expect there. 
Line 1007: • all kinds of empty / not empty assertions, e.g. isNull(), isEmpty() and their isNot…()
Line 1008: counterparts,
Line 1009: • size checks: e.g. hasSize(int expected) and hasSameSizeAs(Iterable<?> other),
Line 1010: • contains(), doesNotContains(), and isIn(Iterable<?> values), also with popular data
Line 1011: structures e.g. contains(double[] values, Offset<Double> precision) for array of double
Line 1012: values,
Line 1013: • even more contains-related methods that allow you to check whether there are some duplicates
Line 1014: (doesNotHaveDuplicates()), or how many times the element in question appears in a given array
Line 1015: of the collection (containsOnly(), containsExactlyOnce())
Line 1016: • support for map verification, e.g. containsKeys(…), containsValues(…) and
Line 1017: contains(Map.Entry entry),
Line 1018: • sorting verification: isSorted() and isSortedAccordingTo(Comparator<> comparator)
Line 1019: • and many more…
Line 1020: This abundance of verification methods mean that you rarely (if ever) need to iterate over collection or
Line 1021: array in order to discover something about its content. And this is actually a very good thing, at least
Line 1022: for two reasons:
Line 1023: 126
Line 1024: 
Line 1025: --- 페이지 142 ---
Line 1026: Chapter 7. Things You Should Know
Line 1027: • the verification code is concise,
Line 1028: • there is no need to introduce logic (for loops and if constructs) into your testing code (which
Line 1029: happens in the case of arrays).
Line 1030: Usage of these specialised verification methods results in conciseness that is demonstrated by the
Line 1031: following snippet:
Line 1032: Listing 7.25. Checking if set contains only elements e1 and e2
Line 1033: assertThat(set.contains(e1)).isTrue();
Line 1034: assertThat(set.contains(e2)).isTrue();
Line 1035: assertThat(set.size()).isEqualTo(2);
Line 1036: // vs.
Line 1037: assertThat(set)
Line 1038:   .containsOnly(e1, e2);
Line 1039: Also, these specialised methods offer very clear failure messages. Continuing with the example above,
Line 1040: if set contained only e1, the containsOnly() assertion would fail with the following message:
Line 1041: java.lang.AssertionError:
Line 1042: Expecting:
Line 1043:   <["e1"]>
Line 1044: to contain only:
Line 1045:   <["e1", "e2"]>
Line 1046: but could not find the following elements:
Line 1047:   <["e2"]>
Line 1048: In addition, AssertJ offers also some utility classes that make it possible to avoid tedious creation of
Line 1049: objects within your test code, e.g.:
Line 1050: Listing 7.26. MapEntry and Sets utility class
Line 1051: import static org.assertj.core.data.MapEntry.*; 
Line 1052: import static org.assertj.core.util.Sets.*; 
Line 1053: assertThat(map)
Line 1054:   .contains(entry("a", 2), entry("b", 3)) 
Line 1055:   .doesNotContain(entry("c", 1)); 
Line 1056: Set<String> set = Sets.newTreeSet("a", "b", "c"); 
Line 1057: Usage of an utility static method entry() of MapEntry class.
Line 1058: Sets.newTreeSet() method allows us to create an instance of TreeSet and fill it with testing
Line 1059: data in one line.
Line 1060: While writing this section I realised that even though I had been testing exhaustively for
Line 1061: years, I hadn’t needed to use even 10% of all collections-related methods that AssertJ
Line 1062: offers!
Line 1063: Testing collections by property
Line 1064: AssertJ offer an interesting feature for searching objects within collections based on their properties. 
Line 1065: 127
Line 1066: 
Line 1067: --- 페이지 143 ---
Line 1068: Chapter 7. Things You Should Know
Line 1069: Listing 7.27. Testing collections objects by properties
Line 1070: Collection<Book> books = Sets.newLinkedHashSet(
Line 1071:   new Book("Homer", "Odyssey"), 
Line 1072:   new Book("J.R.R. Tolkien", "Hobbit")
Line 1073: );
Line 1074: assertThat(books).extracting(Book::getAuthor) 
Line 1075:   .contains("J.R.R. Tolkien") 
Line 1076:     .doesNotContain("J.K. Rowling"); 
Line 1077: A constructor of the Book class sets its two fields - author and title.
Line 1078: Using Java 8 method reference to fetch the values we are investigating.
Line 1079: Verification methods.
Line 1080: Conditions and collections
Line 1081: Let me also remind you that custom conditions could be used to verify the content of
Line 1082: collections. Refer to Section 6.2 for an example.
Line 1083: 7.10.2. The TDD Approach - Step by Step
Line 1084: We know that AssertJ can help with collections testing. Now, let us combine this knowledge with the
Line 1085: TDD approach. 
Line 1086: First of all, it is advisable to do this step by step. Start with a simple assertion which verifies that a
Line 1087: returned collection is not null. Watch the test fail (as a default implementation created by your IDE
Line 1088: will probably return null). Make the test pass by returning a new collection. Add another assertion
Line 1089: verifying whether or not the returned collection has the expected number of elements. Now start
Line 1090: verifying the content.
Line 1091: An example of the resulting test code is shown in Listing 7.28. It contains many assertions, each
Line 1092: progressively more restrictive than the previous one. 
Line 1093: Listing 7.28. TDD collection content testing
Line 1094: @Test
Line 1095: void shouldReturnUsersPhone() {
Line 1096:     User user = new User();
Line 1097:     user.addPhone("123 456 789");
Line 1098:     List<String> phones = user.getPhones();
Line 1099:     assertThat(phones)
Line 1100:         .isNotNull()
Line 1101:         .isNotEmpty()
Line 1102:         .hasSize(1)
Line 1103:         .contains("123 456 789");
Line 1104: }
Line 1105: Even though this pattern might seem unnatural at first, the benefit is that if anything goes wrong
Line 1106: during development, you can pinpoint bugs with 100% accuracy. But of course, you do not have to be
Line 1107: so meticulous - if you feel like moving in larger steps, then by all means do so.
Line 1108: 128
Line 1109: 
Line 1110: --- 페이지 144 ---
Line 1111: Chapter 7. Things You Should Know
Line 1112: Refactor?
Line 1113: As you remember, during the third step of the TDD cycle ("refactor") you should clean both your
Line 1114: production code and your test code. If the only reason for writing these progressively more restrictive
Line 1115: assertions was to write some complex code by taking small steps, then it might be a good idea right
Line 1116: now to refactor the assertion as well. For example, you could achieve the same verification with this
Line 1117: single assertion:
Line 1118: Listing 7.29. One assertion to rule them all
Line 1119: assertThat(phones).containsExactly("123 456 789");
Line 1120: Interestingly, AssertJ assertions are so smart that if phones variable happens to be null you will still
Line 1121: get a reasonable error message (the same you would get if using the isNotNull() method):
Line 1122: java.lang.AssertionError:
Line 1123: Expecting actual not to be null
Line 1124: 7.11. Parameterized tests revisited
Line 1125: You have already learned a lot about parameterized tests in Section 3.6. Now we will go a little bit
Line 1126: deeper into the topic.
Line 1127: 7.11.1. Data Provider Method
Line 1128: In Section 3.6 we have learned to provide test data using @ValueSource annotation, like this:
Line 1129: @ValueSource(ints = { -12387, -5, -1 })
Line 1130: or using the @CsvSource annotation:
Line 1131: @CsvSource({ "10, USD", "15, EUR", "50, CHF" })
Line 1132: This works for the majority of cases, but not all of them. Firstly, there are some limitations with
Line 1133: regard to values you can pass using annotations - i.e. null value is not treated as constant expression.
Line 1134: In some other scenarios values you want to pass need to be created during runtime (i.e. you need to
Line 1135: compute them or fetch them from some external source).
Line 1136: To satisfy such needs JUnit allows for the use of other methods as data providers.
Line 1137: Remember the Money class constructor we tested for invalid amount values (see Listing 3.15)? Let us
Line 1138: exercise a similar scenario, this time trying to pass invalid currencies, and using a separate method as
Line 1139: data provider.
Line 1140: Just in case you forgot, this is what our test looked like:
Line 1141: Listing 7.30. Parameterized test uses annotation
Line 1142: @ParameterizedTest
Line 1143: @ValueSource(ints = { -12387, -5, -1 })
Line 1144: void constructorShouldThrowIAEForInvalidAmount(int invalidAmount) {
Line 1145:     assertThatExceptionOfType(IllegalArgumentException.class)
Line 1146: 129
Line 1147: 
Line 1148: --- 페이지 145 ---
Line 1149: Chapter 7. Things You Should Know
Line 1150:             .isThrownBy(() -> {
Line 1151:                 new Money(invalidAmount, VALID_CURRENCY);
Line 1152:             });
Line 1153: }
Line 1154: As promised, this time we will use a separate data providing method to feed our test method with data.
Line 1155: The following listing illustrates this:
Line 1156: Listing 7.31. Parameterized tests uses a data providing method
Line 1157: import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
Line 1158: import java.util.stream.Stream;
Line 1159: import org.junit.jupiter.params.provider.MethodSource; 
Line 1160: public class MoneyTest {
Line 1161:     private static final int VALID_AMOUNT = 7;
Line 1162:     public static Stream<String> invalidCurrency() { 
Line 1163:         return Stream.of(null, "", " ", "\t"); 
Line 1164:     }
Line 1165:     @ParameterizedTest
Line 1166:     @MethodSource(value = "invalidCurrency") 
Line 1167:     void constructorShouldThrowIAEForInvalidCurrency(String invalidCurrency) {
Line 1168:         assertThatExceptionOfType(IllegalArgumentException.class)
Line 1169:             .isThrownBy(() -> {
Line 1170:                 new Money(VALID_AMOUNT, invalidCurrency);
Line 1171:       });
Line 1172:   }
Line 1173: }
Line 1174: This is our data providing method. It is static and returns a Stream<String>.
Line 1175: Indeed, it does return a Stream of String objects: in our case these are invalid currency values
Line 1176: (null and various empty values).
Line 1177: The @MethodSource annotation tells JUnit to ask the invalidCurrency() method for input
Line 1178: arguments.
Line 1179: In the case whe multiple arguments are expected by the test method, our data providing method would
Line 1180: need to return the Stream<Argument> as the following listing shows:
Line 1181: Listing 7.32. Parameterized tests - data providing method with multiple
Line 1182: arguments
Line 1183: import org.junit.jupiter.params.provider.Arguments; 
Line 1184: import org.junit.jupiter.params.provider.MethodSource; 
Line 1185: public static Stream<Arguments> dataProvider() { 
Line 1186:     return Stream.of(
Line 1187:             Arguments.of("a", 1), 
Line 1188:             Arguments.of("b", 2));
Line 1189: }
Line 1190: @ParameterizedTest
Line 1191: @MethodSource(value = "dataProvider") 
Line 1192: void expectsStringAndInt(String x, int y) {
Line 1193: 130
Line 1194: 
Line 1195: --- 페이지 146 ---
Line 1196: Chapter 7. Things You Should Know
Line 1197:     // test code here
Line 1198: }
Line 1199: All arguments of different types are wrapped into Stream<Arguments>.
Line 1200: @MethodSource annotation used, same as previously.
Line 1201: In fact, there are many more details to the @MethodSource annotation (all nicely described by JUnit
Line 1202: documentation), but what you saw already is good enough for 99% of cases. The pattern is quite
Line 1203: simple:
Line 1204: • create a static method returning a Stream of whatever arguments are needed,
Line 1205: • mark your test method with the @MethodSource pointing to the data providing method.
Line 1206: 7.11.2. Reading Test Data From CSV File
Line 1207: A commonly arising issue is reading data for tests from CSV files. Of course, it is possible to come up
Line 1208: with a custom solution leveraging libraries like OpenCSV15 or SuperCSV16. This is neither hard, nor
Line 1209: time consuming, but since this scenario is very common, there are ready-to-use solutions we should
Line 1210: look at first. 
Line 1211: For the rest of this section we will use the following case: verifying whether our software calculates
Line 1212: valid discounts based on the total value of a purchase made by a client.
Line 1213: The test data file looks the following:
Line 1214: financial.csv. 
Line 1215: value,      discount 
Line 1216: 0.00,       0
Line 1217: 999.99,     0
Line 1218: 1000.00,    0.01
Line 1219: 1999.99,    0.01
Line 1220: 2000.00,    0.02
Line 1221: 4999.99,    0.02
Line 1222: 5000.00,    0.03 
Line 1223: 10000.00,   0.03
Line 1224: 378433.00,  0.03
Line 1225: A header which we should ignore.
Line 1226: For each value in the first column, a certain discount is expected. Our test will verify if the
Line 1227: DiscountCalculator class calculates the discount properly. For example, for values of 5k and
Line 1228: more, a discount of 3% is expected.
Line 1229: Listing 7.33. Reading Test Data from CSV FIle
Line 1230: import org.junit.jupiter.params.ParameterizedTest; 
Line 1231: import org.junit.jupiter.params.provider.CsvFileSource; 
Line 1232: import org.assertj.core.data.Offset; 
Line 1233: public class ReadCSVDataForTest {
Line 1234: 15http://opencsv.sourceforge.net/
Line 1235: 16http://super-csv.github.io/super-csv/
Line 1236: 131
Line 1237: 
Line 1238: --- 페이지 147 ---
Line 1239: Chapter 7. Things You Should Know
Line 1240:     @ParameterizedTest 
Line 1241:     @CsvFileSource(resources = "financial_data.csv", numLinesToSkip = 1) 
Line 1242:     void shouldCalculateDiscount(double value, double discount) { 
Line 1243:         assertThat(DiscountCalculator.calculateDiscount(value))
Line 1244:                 .isEqualTo(discount, Offset.offset(0.0001)); 
Line 1245:     }
Line 1246: }
Line 1247: Test methods which take parameters need to be marked with @ParameterizedTest annotation.
Line 1248: @CsvFileSource points to the data file financial_data.csv. The file is kept in the same
Line 1249: package in the src/test/resources subfolder, so the test class can access it with ease. The
Line 1250: numLinesToSkip parameter instructs JUnit to ignore the first line of data file (a header, that the
Line 1251: test should not care about).
Line 1252: The test method expects two arguments which, by pure chance of course, is exactly the number
Line 1253: of datapoints in each row of the financial_data.csv file.
Line 1254: I took an opportunity to present one more interesting feature of AssertJ assertions: double values
Line 1255: can be compared with some offset.
Line 1256: 7.11.3. Converters
Line 1257: In Section 3.6 we have seen how JUnit behind our backs silently converted a few String values into
Line 1258: Integers. In fact, JUnit does a very nice job when converting values to required types. It does all the
Line 1259: obvious things (e.g. if your test method requires a long argument, JUnit will conveniently convert int
Line 1260: values passed with @ValueSource annotation). 
Line 1261: It also does the not-so-obvious things. For example, it will turn String values into enums, booleans,
Line 1262: dates, big decimals and many more whenever appropriate. This means that for commonly used types
Line 1263: you can try to write them as strings instead of creating fully fledged objects of certain types, having
Line 1264: pretty good confidence JUnit will figure out the rest.
Line 1265: Let me present a short example of what you can expect:
Line 1266: Listing 7.34. JUnit automatic conversion of test method parameters
Line 1267: @ParameterizedTest
Line 1268: @CsvSource({ 
Line 1269:         "http://valid.url, 123.456e789",
Line 1270:         "http://whatever.com, -987.653e321"})
Line 1271: void expectsURLsAndBigDecimals(URL url, BigDecimal bigDec) {
Line 1272:         System.out.println("url: " + url + ", bigDec: " + bigDec);
Line 1273: }
Line 1274: @ParameterizedTest
Line 1275: @CsvSource({ 
Line 1276:         "/path/to/file, 15:24:38",
Line 1277:         "/usr/local/file.txt, 11:11:11"})
Line 1278: void expectsPathAndTime(Path path, LocalTime time) {
Line 1279:         System.out.println("path: " + path + ", time: " + time);
Line 1280: }
Line 1281: I have used @CsvSource annotation, but same conversions are possible with @ValueSource.
Line 1282: If we run this test, the output will prove that JUnit converted strings into expected types:
Line 1283: 132
Line 1284: 
Line 1285: --- 페이지 148 ---
Line 1286: Chapter 7. Things You Should Know
Line 1287: url: http://valid.url, bigDec: 1.23456E+791
Line 1288: url: http://whatever.com, bigDec: -9.87653E+323
Line 1289: path: /path/to/file, time: 15:24:38
Line 1290: path: /usr/local/file.txt, time: 11:11:11
Line 1291: Please check JUnit parameterized tests documentation [https://junit.org/junit5/docs/current/
Line 1292: user-guide/#writing-tests-parameterized-tests] to learn about all possible conversions.
Line 1293: 7.12. Conclusions
Line 1294: We started this section by discussing a few techniques that should definitely be in your testing
Line 1295: toolbox. In particular, we took a detailed look at expected exceptions testing, and learned what
Line 1296: matchers are good for.
Line 1297: In the earlier parts of this book, we discussed some artificial situations in order to demonstrate the
Line 1298: basics of unit testing. This part has been different. We have tackled some real-life problems: "how to
Line 1299: test collections?", "how to beat time in time-dependent methods?" or "how to use test data that my
Line 1300: business analytics gave me?". We have learned how to deal with each of them, so they are no longer
Line 1301: scary, but just another thing we have to deal with in order to achieve our ultimate goal of high-quality,
Line 1302: flawless code.
Line 1303: 133
Line 1304: 
Line 1305: --- 페이지 149 ---
Line 1306: Chapter 7. Things You Should Know
Line 1307: 7.13. Exercises
Line 1308: In this section we have been discussing a number of aspects of advanced unit testing. Now it is time to
Line 1309: practice some of these freshly acquired skills.
Line 1310: 7.13.1. Design Test Cases: State Testing
Line 1311: A StringUtils class contains a reverse() method, with a signature as presented below. List test
Line 1312: cases, which would verify that this method really reverses the input String!
Line 1313: Listing 7.35. Signature of reverse Method
Line 1314: public String reverse(String s) { ... }
Line 1315: 7.13.2. Design Test Cases: Interactions Testing
Line 1316: UserServiceImpl class contains the assignPassword() method, as presented on Listing 7.36. The
Line 1317: method uses two collaborators to successfully perform its task: userDAO and securityService.
Line 1318: Listing 7.36. assignPassword() method
Line 1319: private UserDAO userDAO;
Line 1320: private SecurityService securityService;
Line 1321: public void assignPassword(User user) throws Exception {
Line 1322:     String passwordMd5 = securityService.md5(user.getPassword());
Line 1323:     user.setPassword(passwordMd5);
Line 1324:     userDAO.updateUser(user);
Line 1325: }
Line 1326: Design the test cases for this method! Please note that this time you will have to think not only
Line 1327: about the input parameters (user), but also about the values returned (or exceptions thrown!) by
Line 1328: securityService and userDAO.
Line 1329: 7.13.3. Test Collections
Line 1330: Write a test for the trivial UserList class (shown in Listing 7.37), which will verify that:
Line 1331: • an empty list of users is returned if no users have been added,
Line 1332: • exactly one user is returned if only one has been added,
Line 1333: • two users are returned if two have been added.
Line 1334: Listing 7.37. Testing collections - exercise
Line 1335: public class UserList {
Line 1336:     private List<User> users = new ArrayList<User>();
Line 1337:     public List<User> getUsers() {
Line 1338: 134
Line 1339: 
Line 1340: --- 페이지 150 ---
Line 1341: Chapter 7. Things You Should Know
Line 1342:         return users;
Line 1343:     }
Line 1344:     public void addUser(User user) {
Line 1345:         users.add(user);
Line 1346:     }
Line 1347: }
Line 1348: 7.13.4. Time Testing
Line 1349: Listing 7.38 presents a single test-dependent method. Use the method described in Section 7.9 to test
Line 1350: its business logic.
Line 1351: Listing 7.38. Time-dependent method - exercise
Line 1352: public class HelpDesk {
Line 1353:     public final static int EOB_HOUR = 17;
Line 1354:     public boolean willHandleIssue(Issue issue) {
Line 1355:         Calendar cal = Calendar.getInstance();
Line 1356:         int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);
Line 1357:         if (Calendar.SUNDAY == dayOfWeek || Calendar.SATURDAY == dayOfWeek) {
Line 1358:             return false;
Line 1359:         }
Line 1360:         if (Calendar.FRIDAY == dayOfWeek) {
Line 1361:             int hour = cal.get(Calendar.HOUR_OF_DAY);
Line 1362:             if (hour > EOB_HOUR) {
Line 1363:                 return false;
Line 1364:             }
Line 1365:         }
Line 1366:         return true;
Line 1367:     }
Line 1368: }
Line 1369: 7.13.5. Redesign of the TimeProvider class
Line 1370: Let’s recall the Hello class after we had introduced a timeProvider collaborator to it (see the Listing
Line 1371: 7.21 in the Section 7.9). The current version of this class fetches some data from the timeProvider
Line 1372: (i.e. the current hour) and then makes some decision based on this returned data. This is not such a
Line 1373: terrible thing, but it does break one important rule of good design: that we should preferably ask for
Line 1374: results of calculations rather than data. We can fix it by changing the TimeProvider interface so that
Line 1375: it answers the "is it morning?" question. After this, rewrite the test for the Hello class, and see if that
Line 1376: has become any simpler!
Line 1377: In addition, write the implementation (with tests, of course!) of the TimeProvider interface! See
Line 1378: how the test cases originally aimed at the Hello class now relate to the class implementing the
Line 1379: TimeProvider interface!
Line 1380: 7.13.6. Write a Custom Matcher
Line 1381: Write an AssertJ custom matcher so that you can write nicely readable assertions for the given
Line 1382: OperatingSystem class:
Line 1383: 135
Line 1384: 
Line 1385: --- 페이지 151 ---
Line 1386: Chapter 7. Things You Should Know
Line 1387: Listing 7.39. The OperatingSystem class
Line 1388: public class OperatingSystem {
Line 1389:     private int nbOfBits;
Line 1390:     private String name;
Line 1391:     private String version;
Line 1392:     private int releaseYear;
Line 1393:     // getters and setters omitted
Line 1394: }
Line 1395: An example of what you should achieve is presented below:
Line 1396: Listing 7.40. Test of the OperatingSystem class
Line 1397: public class OperatingSystemTest {
Line 1398:     private OperatingSystem os;
Line 1399:     @Test
Line 1400:     void testUsingMatcher() {
Line 1401:         OperatingSystem min9 = new Mindows9();
Line 1402:         assertThat(min9)
Line 1403:             .is128bit()
Line 1404:             .wasReleasedIn(2019)
Line 1405:             .hasVersion(9);
Line 1406:     }
Line 1407: }
Line 1408: Make sure you take care of any failed assertion messages in such a way that the cause of a failure is
Line 1409: explicitly given.
Line 1410: Write some tests using your matcher, and decide whether it was worth the trouble of implementing it.
Line 1411: 136