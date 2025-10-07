Line 1: 
Line 2: --- 페이지 187 ---
Line 3: Chapter 9. Getting Feedback
Line 4: This report, by its very length, defends itself against the risk of being read.
Line 5: — Winston Churchill
Line 6: Writing tests, especially in a test-first manner, is all about getting rapid and precise feedback. We have
Line 7: already tackled this subject. We have discussed the green/red colors which indicate the success or
Line 8: failure of tests, and mentioned the importance of error messages. In this section we will learn what
Line 9: (detailed) information about the tests is available, and how to customize it to our liking.
Line 10: When reading about the ways of getting feedback from test tools (usually in the form of various
Line 11: reports), please bear in mind that there are two common uses for them. First of all, they are here to
Line 12: help a developer learn about the issues with his tests. Secondly, they help the whole team (or even
Line 13: some stakeholders) to get a good understanding of the situation. While your IDE can help you with
Line 14: the former, your colleagues and superiors may require something more. This section covers both
Line 15: requirements
Line 16: Is Customization Worth the Trouble? 
Line 17: This section gives a lot of information about the
Line 18: customization of existing test reports and about writing custom ones. The question is, whether such
Line 19: activities are worth the trouble. Well, I cannot answer this question for you. It is up to you to decide.
Line 20: If, like me, you like tools to behave exactly as you want them to, if you set your own keyboard
Line 21: shortcuts in MS Word, GMail or your IDE, if you believe that a one-off effort can bring everyday
Line 22: benefits for a long time to come, then you should probably read this carefully and think about how
Line 23: you would like your reports to be. But if you are usually happy with default settings (even to the
Line 24: extent of never touching the gear-system on your bike "cos it’s good the way it is right now") then
Line 25: simply read about the default reports, and do not bother with customization.
Line 26: When talking about feedback information we must mention Javadocs. In contrast to what
Line 27: we have discussed so far, they do not give us information about the execution of tests, but
Line 28: help us instead to understand their purpose and business value. Some hints about writing
Line 29: Javadocs have already been given in Section 4.2.3.
Line 30: 9.1. IDE Feedback
Line 31: If you usually run your tests via an IDE (see Appendix D, Running Unit Tests for some hints) then it
Line 32: is crucial that you know how to make the best of it. This section explains what information you can
Line 33: acquire from IntelliJ IDEA and Eclipse about the tests being executed. As both IDEs are subject to
Line 34: ongoing development, you should also check their original documentation. It is possible that some
Line 35: new helpful features will have been added after this book is written.
Line 36: All popular IDEs behave in a similar manner when it comes to running tests. They signal the fact that
Line 37: all your tests have passed with green color, and provide only the most basic information in such
Line 38: a case. In particular, they print information on how many tests were executed (it is also possible to
Line 39: check which tests exactly were executed, so you can make sure the ones you were most interested in
Line 40: were). And this should satisfy your needs in almost 100% cases as when the tests pass, you usually
Line 41: don’t need to see any diagnostic messages (it is possible to see tests output but this requires few
Line 42: additional clicks).
Line 43: Obviously, when a test fails, your expectations of support from the IDE are going to be much higher
Line 44: than if all of the tests pass. First of all, your IDE will warn you about the problem by changing the
Line 45: 172
Line 46: 
Line 47: --- 페이지 188 ---
Line 48: Chapter 9. Getting Feedback
Line 49: color from green to red. IDEs will also make it possible to navigate directly to the test code which has
Line 50: failed, so you can start fixing the bug right away. Last but not least, you will want to rerun or debug
Line 51: the tests (all of them, or maybe only the failed ones); this is also supported by IDEs.
Line 52: IDEs offer keyboard shortcuts for popular test-related tasks - in particular for running
Line 53: the tests and rerunning them. It is advisable to memorize them and to limit the number of
Line 54: clicks you need to make to perform these basic tasks.
Line 55: Let us see now how the two most popular IDEs can help with running unit tests.
Line 56: 9.1.1. Eclipse Test Reports
Line 57:  This is what Eclipse looks like when all your tests have passed:
Line 58: Figure 9.1. Eclipse: passed tests
Line 59: The green bar on top makes it clear there are no failed tests. The pane on the left provides the list
Line 60: of executed tests (in the form of a tree, so you can see which class and package they belong to).
Line 61: Information on execution time is also provided, even though this is usually not so important with
Line 62: unit tests. As Figure 9.1 shows, in cases of parameterized tests, detailed information on arguments is
Line 63: printed as well. Moreover, there is a console pane, which shows the output of each test and any other
Line 64: messages printed by the testing framework.
Line 65: In the event of test failure Eclipse also provides some additional information:
Line 66: • which test method failed and, in the case of parameterized tests, what the arguments were (in our
Line 67: case 20 and EUR),
Line 68: • a failure exception message which is "clickable", so you can easily move to the test code and start
Line 69: fixing things.
Line 70: 173
Line 71: 
Line 72: --- 페이지 189 ---
Line 73: Chapter 9. Getting Feedback
Line 74: Figure 9.2. Eclipse: failed tests
Line 75: Eclipse also makes it possible to rerun all recently executed tests, to run only the failed ones1, and to
Line 76: execute tests in debug mode.
Line 77: 9.1.2. IntelliJ IDEA Test Reports
Line 78:  When all tests pass, IntelliJ IDEA by default presents only the basic status information - a green bar
Line 79: and a printed summary message.
Line 80: Figure 9.3. IntelliJ IDEA: passed tests
Line 81: If you want to know more, you need to customize the Test Runner Tab view. IntelliJ IDEA will use
Line 82: the latest settings, so configuring it will be a one-off action. In order to see what tests have been
Line 83: run, switch off the Hide Passed button and select the Expand All button. In addition, to get the test
Line 84: execution statistics (do you really need to check the execution time of your unit tests?) select the
Line 85: Show Statistics option from the cog button menu. The resulting view is shown in Figure 9.4 (red
Line 86: rectangles mark the aforementioned options).
Line 87: The left pane lists all the test methods executed during the last run in the form of a tree (with each
Line 88: package and class as a node, and each test method as a tree leaf). The pane in the middle shows the
Line 89: console output of each of the tests (in this case the tests have not printed any messages, so it is almost
Line 90: empty). Clicking on test names (in the left panel) results in the middle pane showing the test output
Line 91: for a selected test case. The right pane shows tests execution statistics.
Line 92: 1In the moment of writing the rerun failed tests option was not available for JUnit 5 tests.
Line 93: 174
Line 94: 
Line 95: --- 페이지 190 ---
Line 96: Chapter 9. Getting Feedback
Line 97: Figure 9.4. IntelliJ IDEA: passed tests - customized view
Line 98: In the event of failure, IntelliJ IDEA will warn you about the problem by changing the bar color
Line 99: from green to red.
Line 100: Figure 9.5. IntelliJ IDEA: failed tests
Line 101: It is possible to configure the Test Runner Tab so that after having executed the tests it focuses on the
Line 102: first failed test. Figure 9.5 shows such a scenario. The assertion error is printed along with the precise
Line 103: lines of test code where the verification failed. They are clickable, so you can easily move to the test
Line 104: code and start fixing things.
Line 105: 9.1.3. Conclusion
Line 106: As we have observed in the course of this section, both IntelliJ IDEA and Eclipse provide highly
Line 107: readable test execution reports. The overall result is clearly visible in the form of a green or red bar.
Line 108: The results of each test are also shown. In cases of passed tests, only a minimal amount of information
Line 109: is printed, so the screen does not become clogged up with unimportant data. However, in the event of
Line 110: failure, both IDEs show more of the data, and this helps you fix the bug right away. They offer quick
Line 111: navigation from assertion error to test code.
Line 112: 175
Line 113: 
Line 114: --- 페이지 191 ---
Line 115: Chapter 9. Getting Feedback
Line 116: 9.2. JUnit Default Reports
Line 117:     Usually you will run your tests with an IDE. However this is not always the case, and sometimes
Line 118: you will also need to look into the report files generated by JUnit.
Line 119: JUnit generates one file per each executed test class by itself. In the case of Maven you will find two
Line 120: files for each - with .txt and .xml extensions - in the target/surefire-reports. Their content
Line 121: is equivalent, but the format differs. In the case of Gradle, you will find .xml files in the build/
Line 122: reports/tests directory. In addition, build tools generate some HTML reports, which are probably
Line 123: more agreeable to work with. Maven puts them in the target/site directory, while Gradle puts them
Line 124: in the build/reports/tests directory.
Line 125: Build tools allow you to configure the output folder for test reports. Please consult the
Line 126: documentation if you are not happy with the default settings.
Line 127: Figure 9.6 shows an overview part of the test execution report generated by Gradle.
Line 128: Figure 9.6. Test execution report - an overview
Line 129: The reports allow you to "drill down", so you can see what the number of passed and failed tests is –
Line 130: first in each of the packages, then in individual classes. It is also possible to view the log of each test
Line 131: method (so, for example, you can check what exceptions were thrown, etc.).
Line 132: 176
Line 133: 
Line 134: --- 페이지 192 ---
Line 135: Chapter 9. Getting Feedback
Line 136: Figure 9.7. Test execution report - details
Line 137: 9.3. Writing Custom Listeners
Line 138: "Getting feedback" from test execution can mean two things. We are usually interested in the details
Line 139: of test execution after they are all finished (i.e. we want to know the results they finished with), but
Line 140: sometimes we would like to have some feedback during the execution of our tests.
Line 141: There are many reasons for implementing a custom reporting mechanism - some valid for unit tests,
Line 142: some important rather for integration and end-to-end tests. You might be interested in, for example:
Line 143: • getting more detailed information printed to the console,
Line 144: • implementing a GUI progress-bar widget, which would show how the execution of the tests is
Line 145: progressing,
Line 146: • taking a screenshot after each failed Selenium test executed with the JUnit framework,
Line 147: • writing test results to a database.
Line 148: This functionality is rarely required for unit testing, so I have decided to only mention it
Line 149: very briefly. The documentation of JUnit contains a detailed example of writing an utility
Line 150: class that would log the execution time of test methods. Refer there, please, to learn how to
Line 151: do it.
Line 152: JUnit provides a few callbacks that you can hook into in order to intercept various events from
Line 153: test lifecycle2. For example, you can implement BeforeTestExecutionCallback and/or
Line 154: AfterTestExecutionCallback interfaces to execute some code right before (and right after) some
Line 155: test method is executed.
Line 156: An object of the ExtensionContext class, passed to the above methods, contains information about
Line 157: the test class and the test method. And this is exactly what is required to implement custom test
Line 158: listeners.   
Line 159: 2All extension points are grouped in the org.junit.jupiter.api.extension package.
Line 160: 177
Line 161: 
Line 162: --- 페이지 193 ---
Line 163: Chapter 9. Getting Feedback
Line 164: 9.4. Readable Assertion Messages
Line 165: An assertion message has just one purpose: to make the developer understand instantly what has gone
Line 166: wrong: no guessing, no head-scratching. You just have to look at the assertion message to know for
Line 167: sure what it is that is not working. This does not mean that you know where the bug is, but it is the
Line 168: first step on the way to finding and fixing it.
Line 169: When looking at the examples in this book, you may reach the conclusion that working on
Line 170: assertion messages is a waste of time. Well, yes, sometimes it is. However, bear in mind
Line 171: that you are now in "training mode". The examples are simple and you are focusing on
Line 172: them to the exclusion of everything else. In real life things will be different. You will be
Line 173: surprised by a not-so-clear error message of your end-to-end test when you least expect
Line 174: it, when your mind is focused on some completely different part of the system (and also,
Line 175: probably, when the deadline is near…). Doesn’t it make more sense to spend 15 seconds
Line 176: now, and maybe save a lot of grey hairs later? It is up to you to decide.
Line 177:   From time to time, you may benefit from adding a custom message to the assertion method. For
Line 178: example (going back to the Money class that we discussed earlier), consider these two messages, each
Line 179: printed by a failing test. The first one is printed by the following assertion:
Line 180: assertThat(money.getAmount()).isEqualTo(10);
Line 181: Listing 9.1. Default failure message
Line 182: org.junit.ComparisonFailure:
Line 183: Expected :10
Line 184: Actual   :15
Line 185: Let us add the as("…") method to the assertion chain and observe the result:
Line 186: assertThat(money.getAmount())
Line 187:   .as("wrong amount of money")
Line 188:   .isEqualTo(10);
Line 189: Listing 9.2. Enhanced assertion message
Line 190: org.opentest4j.AssertionFailedError: [wrong amount of money]
Line 191: Expecting:
Line 192:  <15>
Line 193: to be equal to:
Line 194:  <10>
Line 195: but was not.
Line 196: While the first version (without any message) leaves us in doubt about the nature of the problem, the
Line 197: second version states explicitly that the problem was with money3. The gain is rather minimal: usually
Line 198: all you have to do is look at the test method name (which is always included in the stack trace) to
Line 199: understand the context.
Line 200: You could also use the overridingErrorMessage() method. This one doesn’t enhance the error
Line 201: message with additional information, but rather replaces it.
Line 202: 3You could call this a ‘real-life example’, couldn’t you? ;)
Line 203: 178
Line 204: 
Line 205: --- 페이지 194 ---
Line 206: Chapter 9. Getting Feedback
Line 207: assertThat(money.getAmount())
Line 208:   .overridingErrorMessage("wrong amount of money")
Line 209:   .isEqualTo(10);
Line 210: Listing 9.3. Overriden assertion message
Line 211: java.lang.AssertionError: wrong amount of money
Line 212: And where is this kind of error message useful? I would point out to custom matchers (see Section
Line 213: 6.1). We could, for example, add the following method to the BookAssert class:
Line 214: public BookAssert isWrittenIn(String language) {
Line 215:   isNotNull();
Line 216:   String errorMessage = String.format(
Line 217:       "Expected that book was written in <%s> but was <%s>",
Line 218:         language, actual.getLanguage());
Line 219:   Assertions.assertThat(actual.getLanguage())
Line 220:     .overridingErrorMessage(errorMessage).isEqualTo(language);
Line 221:   return this;
Line 222: }
Line 223: And then, the failure message would be just perfect:
Line 224: Listing 9.4. Custom matcher assertion message
Line 225: java.lang.AssertionError:
Line 226:     Expected that book was written in <english> but was <german>
Line 227: If you name your test methods really, really well (see Section 10.2), you will rarely need
Line 228: to tweak the error messages. When they fail, you will know exactly why - just by reading
Line 229: their names.
Line 230: In other cases, all you have to do is use the right assertion! For example, if you compare two objects
Line 231: of the Client class using this isEqualTo() assertion:
Line 232: assertThat(clientA).isEqualTo(clientB);
Line 233: a failure will be reported with the following assertion message:
Line 234: Listing 9.5. A pretty cryptic assertion error message
Line 235: org.junit.ComparisonFailure:
Line 236: Expected :com.practicalunittesting.Client@71bc1ae4
Line 237: Actual   :com.practicalunittesting.Client@39a054a5
Line 238: And before you start implementing the toString() method of the Client class (which would
Line 239: improve the failure message), you might want to try another, better suited assertion provided by
Line 240: AssertJ4:
Line 241: assertThat(clientA).isEqualToComparingFieldByField(clientB);
Line 242: 4I assumed that field by field comparison is an appropriate way of comparing two Client object. Check AssertJ documentation
Line 243: for other comparison assertions.
Line 244: 179
Line 245: 
Line 246: --- 페이지 195 ---
Line 247: Chapter 9. Getting Feedback
Line 248: Listing 9.6. Fixed assertion error message
Line 249: java.lang.AssertionError:
Line 250: Expecting value <"Lois Lane"> in field <"name"> but was <"Peter Parker">
Line 251:   in <com.practicalunittesting.chp08.message.ClientTest$Client@6bc168e5>.
Line 252: Comparison was performed on all fields
Line 253: Selecting the right, the most adequate assertion, is often the key to having the best
Line 254: information on what went wrong.
Line 255: Similarly, we can get the same luxury of perfect error messages when working with mocks. Mockito
Line 256: offers the description() method, which "allows specifying a custom message to be printed if
Line 257: verification fails". The next example is taken straight from Mockito documentation:
Line 258: Listing 9.7. Fine tuning mocks error messages
Line 259: import static org.mockito.Mockito.mock;
Line 260: import static org.mockito.Mockito.description;
Line 261: import static org.mockito.Mockito.times;
Line 262: import static org.mockito.Mockito.verify;
Line 263: @Test
Line 264: void message() {
Line 265:   verify(mock(MyClass.class),
Line 266:     description("I really expected this method to be executed!")) 
Line 267:     .myMethod();
Line 268: }
Line 269: @Test
Line 270: void timesMessage() {
Line 271:   verify(mock(MyClass.class), times(2), 
Line 272:     description("I expected it to run twice!"))
Line 273:     .myMethod();
Line 274: }
Line 275: description() method can be used with any verification mode.
Line 276: As expected, when both tests fail we will see the specified messages.
Line 277: From my experience, this comes handy only in the case of few mocks of the same type when it is
Line 278: easier to distinguish between them using distinct messages. Not an everyday scenario, I have to add.
Line 279: 9.5. Logging in Tests
Line 280: The Loudmouth: A unit test (or test suite) that clutters up the console with diagnostic
Line 281: messages, logging messages, and other miscellaneous chatter, even when tests are
Line 282: passing. Sometimes during test creation there was a desire to manually see output, but
Line 283: even though it’s no longer needed, it was left behind.
Line 284: — James Carr 2006
Line 285: Let’s make it absolutely clear: you do not need logs for unit tests. They are only there because
Line 286: we are so used to the fact that we do verify our software by reading through billions of logs. This is
Line 287: 180
Line 288: 
Line 289: --- 페이지 196 ---
Line 290: Chapter 9. Getting Feedback
Line 291: unnecessary with unit tests. It may even lead to some problems, especially if you run your tests from
Line 292: the command line. 
Line 293: This section is aimed mainly at developers who use the command line for running tests.
Line 294: IDEs are quite good at only presenting users with the summary of tests execution, so even
Line 295: thousands of log lines will not be a problem for them.
Line 296: Watching screens showing logs rolling for a few seconds at the speed of light will not give you
Line 297: anything. You cannot read it, and if the test fails, it should give you exact information on what
Line 298: happened, right? I understand that for integration tests it might be worthwhile to watch Spring or
Line 299: JBoss logs getting printed and see there are no warnings there, but what is the point for unit tests?
Line 300: And the worst thing of all is when you test for expected exceptions and they are printed within the
Line 301: logs which roll over your screen at such a rapid pace. The first time you see it, you shiver, and check
Line 302: it immediately, and then you sigh with relief. And later, after n-th execution of the tests, you get used
Line 303: to exception stack traces being printed, and you start ignoring them. And then comes a day, when
Line 304: some other exception happens, and you do not react at all. You simply do not care, because "these
Line 305: exceptions were always there", and you do not try to investigate it. In fact, you are so used to the idea
Line 306: of a build’s being successful even if some exceptions have been logged, that you do not bother to get
Line 307: to see the final result of a build. You assume it passes, when in reality it has just failed. And then you
Line 308: commit the code and your information radiator goes red, and your team starts yelling at you. Uh, no
Line 309: good…
Line 310: Personally, I am perfectly happy coding with my logs turned off (by having a separate
Line 311: configuration of logging frameworks) and a custom test listener which prints single letters
Line 312: for each test - . (a dot) if it has passed, F if it has failed, and S if the test has been skipped
Line 313: (exactly as described previously in Section 9.3). In the event of test failures, I rely solely
Line 314: on the assertion messages.
Line 315: Even if you do not want to switch your logs off, the thing to remember is that you should stop relying
Line 316: on your logs. The tests should be automated – they should be precise in pointing out the problem,
Line 317: which means that no logs-hunting should be necessary to understand the cause of failure.
Line 318: 9.6. Debugging Tests
Line 319: Debugging? Haven’t we already mentioned that by testing we can save hours spent on debugging
Line 320: sessions? Well, yes. Still, sometimes you run your tests and you do not understand why they are not
Line 321: working (or why they pass!). You stare at the screen and cannot figure out what is going on. Do not
Line 322: stare any longer. Fire up a debugger and look inside.
Line 323: If you are already familiar with debugging, there will not be much that is new to learn. The same rules
Line 324: apply as when debugging a running application. This should not be a surprise, because tests run your
Line 325: application (even though they do it in some specific, strictly controlled way).
Line 326: Section 9.1 covers running a debugging session with Eclipse and IntelliJ IDEA.
Line 327: 9.7. Notifying The Team
Line 328: A common request is that you notify the team (or some superiors) about the results of your tests. The
Line 329: reason is quite sensible: there are some people who ought to know whether all the tests have passed or
Line 330: 181
Line 331: 
Line 332: --- 페이지 197 ---
Line 333: Chapter 9. Getting Feedback
Line 334: not. Perhaps because they will be able to fix it, or maybe because they need to know the status of the
Line 335: project. No matter what the reason is, such functionality can be implemented at the level of JUnit (or
Line 336: almost any other testing framework). For example, one could use the JUnit 5 Extension API5 which,
Line 337: after all tests had finished, would send an email notification using the Java Mail API6. Even so, I
Line 338: myself would argue that this is not the right approach.
Line 339: There are two main reasons for saying this. First, you should let your testing framework take care of
Line 340: executing tests and creating reports. This is what testing frameworks are for. JUnit is quite extensible,
Line 341: which means you can enhance it with almost any functionality you wish, but this does not mean you
Line 342: should do so.
Line 343:  The second reason is that there are already solutions for the notifications sending issue. I would hope
Line 344: that your team makes use of a continuous integration server, which runs all tests continually. Any
Line 345: popular CI solution will offer a notifications service, and usually much more besides. For example,
Line 346: in the case of Jenkins7, a very popular open-source CI server, there are more than 30 notification
Line 347: plugins8 which allow the sending of information about build results (including test results) by email,
Line 348: Jabber, Skype, Twitter and many more.
Line 349: To conclude, first you should "use the right tool for the job", and second, in the presence of such a
Line 350: wealth of freely available options, why bother with implementing your own solution?
Line 351: 9.8. Conclusions
Line 352: In this section we have concentrated on ways of getting feedback information about the execution
Line 353: of tests. First, we covered feedback generated by the IDE. Then we moved to the output generated
Line 354: by JUnit. We learned about the default for this, and explored options for customization. We also
Line 355: did some coding and created our own listeners. In so doing we made JUnit print information
Line 356: that was of value to us, both during the execution of the tests and after they had finished. As the
Line 357: few straightforward examples given here demonstrate, JUnit will furnish us with comprehensive
Line 358: information about the tests that have been executed, and it is up to us how we use it.
Line 359: To gather even more data on the execution of tests, we also plunged into the world of assertion
Line 360: messages, logging and debugging.
Line 361: Well, quite a lot of information. Now that you know all of this, how do you plan to use it? Will you
Line 362: rely on the default information returned by your IDE and testing framework, or do you perhaps
Line 363: feel that some customization is required? Remember, you will be running unit tests frequently and
Line 364: checking their results multiple times, so make sure you feel comfortable with the feedback you are
Line 365: getting.
Line 366: 5See https://junit.org/junit5/docs/current/user-guide/#extensions
Line 367: 6See http://www.oracle.com/technetwork/java/javamail/index.html
Line 368: 7See http://jenkins-ci.org
Line 369: 8See https://wiki.jenkins-ci.org/display/JENKINS/Plugins
Line 370: 182
Line 371: 
Line 372: --- 페이지 198 ---
Line 373: Chapter 9. Getting Feedback
Line 374: 9.9. Exercises
Line 375: The exercises presented in this section aren’t really exercises, but rather invitations for you to further
Line 376: explore the topic discussed in this secgtion.
Line 377: 9.9.1. Study Test Output
Line 378: Simply run some tests and study the output. Make sure you know where to find information on the
Line 379: cause of a failed test. Remember, there are usually several ways to obtain the required information.
Line 380: Spend some time getting to know them all, so you can choose the one which suits you best.
Line 381: 9.9.2. Debugging Session
Line 382: Make yourself comfortable with the debugging of tests. Using your favorite IDE, set some breakpoints
Line 383: (in test code and in the source code of the tested classes) and execute some tests. Practise working
Line 384: through all the typical scenarios of a debugging session:
Line 385: • setting breakpoints,
Line 386: • getting information on the values of variables,
Line 387: • various types of moving forward (step into, step over, etc.).
Line 388: 183