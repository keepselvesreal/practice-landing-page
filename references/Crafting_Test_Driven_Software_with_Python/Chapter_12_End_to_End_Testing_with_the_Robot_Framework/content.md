Line 1: 
Line 2: --- 페이지 291 ---
Line 3: 12
Line 4: End-to-End Testing with the
Line 5: Robot Framework
Line 6: In the previous chapter, we saw how to test web applications and, in general, applications
Line 7: that rely on the HTTP protocol, both client and server side, but we were unable to test how
Line 8: they perform in a real browser. With their complex layouts, the fact that CSS and JavaScript
Line 9: are heavily involved in testing your application with WebTest or a similar solution might
Line 10: not be sufficient to guarantee users that they are actually able to work with it. What if a
Line 11: button is created by JavaScript or it's disabled by CSS? Those conditions are hard to test
Line 12: using WebTest and we might easily end up with a test that clicks that button even though
Line 13: the button wasn't actually usable by users.
Line 14: To guarantee that our applications behave properly, it is a good idea to have a few tests that
Line 15: verify at least the more important areas of the application using a real browser. As those
Line 16: kinds of tests tend to be very slow and fragile, you still want to have the majority of your
Line 17: tests written using solutions such as WebTest or even unit tests, which don't involve the
Line 18: whole application life cycle, but having the most important parts of the web application
Line 19: verified using real browsers will guarantee that at least the critical path of your web
Line 20: application works on all major browsers. 
Line 21: The Robot framework is one of the most solid solutions for writing the end-to-end tests that
Line 22: drive web browsers and mobile applications in the Python world. It was originally
Line 23: developed by Nokia and evolved under the open source community, and is a long-standing
Line 24: and solid solution with tons of documentation and plugins. It is therefore battle tested and
Line 25: ready for your daily projects.
Line 26: In this chapter, we will cover the following topics:
Line 27: Introducing the Robot framework
Line 28: Testing with web browsers
Line 29: Extending the Robot framework
Line 30: 
Line 31: --- 페이지 292 ---
Line 32: End-to-End Testing with the Robot Framework
Line 33: Chapter 12
Line 34: [ 282 ]
Line 35: Technical requirements
Line 36: We need a working Python interpreter with the Robot Framework installed. To run tests
Line 37: with real browsers, we are also going to use the robotframework-seleniumlibrary and
Line 38: the webdrivermanager utilities. To record videos of our tests, we are going to need
Line 39: the robotframework-screencaplibrary library. robotframework, robotframework-
Line 40: seleniumlibrary, robotframework-screencaplibrary, and webdrivermanager can
Line 41: be installed with pip, in the same way as all other Python dependencies:
Line 42: $ pip install robotframework robotframework-seleniumlibrary
Line 43: webdrivermanager robotframework-screencaplibrary
Line 44: The examples have been written on Python 3.7, robotframework 3.2.2, robotframework-
Line 45: seleniumlibrary 4.5.0, robotframework-screencaplibrary 1.5.0, and webdrivermanager 0.9.0,
Line 46: but should work on most modern Python versions. 
Line 47: You can find the code present in this chapter on GitHub at https:/​/​github.​com/
Line 48: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter12.
Line 49: Introducing the Robot Framework
Line 50: The Robot Framework is an automation framework mostly used to create acceptance tests
Line 51: in the Acceptance Test Driven Development (ATDD)  and Behavior Driven
Line 52: Development (BDD) styles. Tests are written in a custom, natural English-like language
Line 53: that can be easily extended in Python, so Robot can, in theory, be used to write any kind of
Line 54: acceptance tests in a format that can be shared with other stakeholders, pretty much like
Line 55: what we have seen we can do with pytest-bdd in previous chapters.
Line 56: The primary difference is that Robot is not based on PyTest, it is a replacement for PyTest,
Line 57: and is widely used to create end-to-end tests for mobile and web applications. For mobile
Line 58: applications, the Appium library allows us to write Robot Framework tests that control
Line 59: mobile applications on a real device, while the Selenium library provides a complete
Line 60: integration with web browsers, which means that the Robot Framework allows us to write
Line 61: tests that drive a real web browser and verify the results.
Line 62: Robot Framework tests are written inside .robot files, which are then divided into
Line 63: multiple sections by the section headers. The most frequently used section headers are the
Line 64: following:
Line 65: *** Settings ***: This contains options to configure Robot itself.
Line 66: *** Variables ***: This contains variables to reuse across multiple tests.
Line 67: 
Line 68: --- 페이지 293 ---
Line 69: End-to-End Testing with the Robot Framework
Line 70: Chapter 12
Line 71: [ 283 ]
Line 72: *** Test Cases ***: This contains our tests.
Line 73: *** Keywords ***: This contains our own custom commands.
Line 74: So, the minimum content of a .robot file is usually a Test Cases section with a test
Line 75: inside. Each test is then a collection of commands for the Robot Framework that are
Line 76: provided by keywords made available by libraries for the Robot Framework itself.
Line 77: The only library automatically available by default in the Robot Framework is the
Line 78: Builtin one (Builtin library reference: https:/​/​robotframework.​org/​robotframework/
Line 79: latest/​libraries/​BuiltIn.​html), which provides some generally helpful commands such
Line 80: as Should Contain to check the content of a variable, or Expression to run any Python
Line 81: expression and assign the result to a variable.
Line 82: Further libraries can be imported explicitly with the Library command in the Settings
Line 83: section. Without involving explicit libraries that add more commands, Robot itself can't do
Line 84: much. 
Line 85: For example, if we want to create a very basic test where we save the "Hello World"
Line 86: string into a file and verify its content, we would have to involve the OperatingSystem
Line 87: library (OperatingSystem library reference: https:/​/​robotframework.​org/
Line 88: robotframework/​latest/​libraries/​OperatingSystem.​html), which makes available
Line 89: commands to interact with files, directories, and the system shell.
Line 90: To create such a test, we would make a hellotest.robot file, where we can declare the
Line 91: instruction for the Robot Framework. At the beginning of the file, we would declare a
Line 92: Settings section, where we use the Library command to make the OperatingSystem
Line 93: library available:
Line 94: *** Settings ***
Line 95: Library     OperatingSystem
Line 96: In Robot, multiple spaces perform separate commands from their
Line 97: arguments.
Line 98: Through the OperatingSystem library, we will get the Run and Get File commands,
Line 99: which we need to write our actual test.
Line 100: Subsequently, we will declare the Test Cases section, where we can put all our tests. In
Line 101: this case, we are going to place only one test, entitled Hello World.
Line 102: 
Line 103: --- 페이지 294 ---
Line 104: End-to-End Testing with the Robot Framework
Line 105: Chapter 12
Line 106: [ 284 ]
Line 107: The test itself will create a new file with the "Hello World" string inside, and will then
Line 108: read it back and check that the content contains the string "Hello":
Line 109: *** Test Cases ***
Line 110: Hello World
Line 111:     Run    echo "Hello World" > hello.txt
Line 112:     ${filecontent} =    Get File    hello.txt
Line 113:     Should Contain    ${filecontent}    Hello
Line 114: The first line of our test uses the Run keyword to invoke the echo command in a shell (if
Line 115: you are on a *nix system, such as Linux or macOS X), and the echo command is invoked
Line 116: with the Hello World argument and redirection is effected to the hello.txt file so that
Line 117: the output of the command actually goes into that file.
Line 118: Once that file is created, on the second line we use the Get File keyword to read the
Line 119: content of the hello.txt file and assign what we read to the ${filecontent} variable.
Line 120: Finally, we check through the Should Contain keyword that the variable contains the
Line 121: string Hello.
Line 122: Once we have saved all this as hellotest.robot, we should be able to run it by invoking
Line 123: the robot command and see that our test is executed and passes:
Line 124: $ robot hellotest.robot
Line 125: =======================================================
Line 126: Hellotest
Line 127: =======================================================
Line 128: Hello World                                    | PASS |
Line 129: -------------------------------------------------------
Line 130: Hellotest                                      | PASS |
Line 131: 1 critical test, 1 passed, 0 failed
Line 132: 1 test total, 1 passed, 0 failed
Line 133: =======================================================
Line 134: If we wanted to see what happens when our tests fail, we could change the Should
Line 135: Contain line to a different string, for example, Should Contain    ${filecontent} 
Line 136:   Bye and see what happens when we rerun our test:
Line 137: $ robot hellotest.robot
Line 138: =======================================================
Line 139: Hellotest
Line 140: =======================================================
Line 141: Hello World                                    | FAIL |
Line 142: 'Hello World' does not contain 'Bye'
Line 143: -------------------------------------------------------
Line 144: Hellotest                                      | FAIL |
Line 145: 
Line 146: --- 페이지 295 ---
Line 147: End-to-End Testing with the Robot Framework
Line 148: Chapter 12
Line 149: [ 285 ]
Line 150: 1 critical test, 0 passed, 1 failed
Line 151: 1 test total, 0 passed, 1 failed
Line 152: =======================================================
Line 153: Details about what precisely went wrong are then made available in the log.html file,
Line 154: where each command that Robot performed is recorded with debugging information.
Line 155: Opening such a file in a browser will indicate explicitly that the command that failed is
Line 156: Builtin.Should Contain and that it failed with the 'Hello World' does not
Line 157: contain 'Bye' error:
Line 158: Figure 12.1 – Detailed log of our test execution from log.html
Line 159: 
Line 160: --- 페이지 296 ---
Line 161: End-to-End Testing with the Robot Framework
Line 162: Chapter 12
Line 163: [ 286 ]
Line 164: Now that we know how the Robot Framework works, we can move on to the next steps
Line 165: and see how we can use it to test web applications with a real browser. 
Line 166: Testing with web browsers
Line 167: We have seen how, using libraries, we can extend Robot with additional commands that
Line 168: allow us to write most different kinds of tests. One of the most frequent use cases for Robot
Line 169: is actually web development as it has a very convenient SeleniumLibrary library that
Line 170: provides many commands to control a real web browser and perform tests that can involve
Line 171: JavaScript (Selenium library reference: https:/​/​robotframework.​org/​SeleniumLibrary/
Line 172: SeleniumLibrary.​html).
Line 173: Once we have installed the robotframework and robotframework-
Line 174: seleniumlibrary Python distributions, in order to be able to write tests that involve a real
Line 175: browser, we will need to enable the web drivers for the browsers we want to use. So, we
Line 176: will need those browsers to be available and then, through the webdrivermanager utility
Line 177: that we installed previously, we can enable the drivers for all the browsers we have
Line 178: available:
Line 179: $ webdrivermanager firefox chrome
Line 180: Downloading WebDriver for browser: "firefox"
Line 181: 2588kb [00:01, 1978.35kb/s]
Line 182: Driver binary downloaded to:
Line 183: "./venv/WebDriverManager/gecko/v0.28.0/geckodriver-v0.28.0-
Line 184: linux64/geckodriver"
Line 185: Symlink created: ./venv/bin/geckodriver
Line 186: Downloading WebDriver for browser: "chrome"
Line 187: 5979kb [00:01, 3615.18kb/s]
Line 188: Driver binary downloaded to:
Line 189: "./venv/WebDriverManager/chrome/87.0.4280.88/chromedriver_linux64/chromedri
Line 190: ver"
Line 191: Symlink created: ./venv/bin/chromedriver
Line 192: Notice that the examples take for granted the fact that everything is
Line 193: happening inside a Python virtual environment, so keep in mind that
Line 194: when using a virtual environment, the drivers are only available inside
Line 195: that environment, and if you create a new one you will need to enable the
Line 196: drivers again.
Line 197: Once we have the drivers available, Robot will be able to control the browsers for which we
Line 198: provided the drivers (in this case, Chrome and Firefox), so we can go back to our editor and
Line 199: create a new test to establish how Robot works.
Line 200: 
Line 201: --- 페이지 297 ---
Line 202: End-to-End Testing with the Robot Framework
Line 203: Chapter 12
Line 204: [ 287 ]
Line 205: In this case, we are going to create a test where we search on Google for a famous person
Line 206: and verify that Wikipedia is included in the results returned. To do so, let's create a
Line 207: searchgoogle.robot file were we are going to enable the SeleniumLibrary library so
Line 208: that browser-related commands become available:
Line 209: *** Settings ***
Line 210: Library SeleniumLibrary
Line 211: The next step is then to write the test itself to open Google with Chrome, accept the privacy
Line 212: policy, perform the search, and then check that Wikipedia is included in the results:
Line 213: *** Test Cases ***
Line 214: Search On Google
Line 215:      Open Browser    http://www.google.com    Chrome
Line 216:      Wait Until Page Contains Element    cnsw
Line 217:      Select Frame    //iframe
Line 218:      Submit Form    //form
Line 219:      Input Text    name=q    Stephen\ Hawking
Line 220:      Press Keys    name=q    ENTER
Line 221:      Page Should Contain    Wikipedia
Line 222:      Close Window
Line 223: If we run our test, a Chrome window will pop up, perform the search, and then close again,
Line 224: with our test regarded as having passed if everything went right:
Line 225: $ robot searchgoogle.robot
Line 226: =======================================================
Line 227: Searchgoogle
Line 228: =======================================================
Line 229: Search On Google                               | PASS |
Line 230: -------------------------------------------------------
Line 231: Searchgoogle                                   | PASS |
Line 232: 1 critical test, 1 passed, 0 failed
Line 233: 1 test total, 1 passed, 0 failed
Line 234: =======================================================
Line 235: Our test might look a bit complex, and that's because the Google website requires us to
Line 236: accept a privacy policy before we can start searching. So, the first commands are related to
Line 237: opening Google itself using Chrome and then waiting for the privacy policy (with id=cnsw
Line 238: in HTML) to appear:
Line 239:      Open Browser    http://www.google.com    Chrome
Line 240:      Wait Until Page Contains Element    cnsw
Line 241: 
Line 242: --- 페이지 298 ---
Line 243: End-to-End Testing with the Robot Framework
Line 244: Chapter 12
Line 245: [ 288 ]
Line 246: Once the browser opens the Google website, we should be greeted by the privacy policy
Line 247: acceptance box:
Line 248: Figure 12.2 – Google website with the policy acceptance request
Line 249: In case you don't see the privacy policy when opening the Google website,
Line 250: don't worry. Google decides if to show the privacy policy or not based on
Line 251: the country and browser you are connecting from. If you country doesn't
Line 252: have any privacy policy requirement, Google might not show the policy.
Line 253: In such case you can omit the three "Wait Until Page Contains Element",
Line 254: "Select Frame" and "Submit Form" commands related to managing the
Line 255: privacy policy or just read further until we tackle headless browser later
Line 256: in the chapter and run the examples using Google Chrome browser in
Line 257: headless mode.
Line 258: Once the privacy policy is visible, we are going to pick the iframe within which it gets 
Line 259: displayed and submit the first form that exists within it:
Line 260:      Select Frame    //iframe
Line 261:      Submit Form    //form
Line 262: 
Line 263: --- 페이지 299 ---
Line 264: End-to-End Testing with the Robot Framework
Line 265: Chapter 12
Line 266: [ 289 ]
Line 267: Submitting the form will make the privacy policy alert disappear and will finally reveal the
Line 268: search box:
Line 269: Figure 12.3 – Google website once the privacy policy has been accepted
Line 270: At this point, we just have to write the name of the person we want to search for in the
Line 271: search box (which has name=q in HTML) and submit it by pressing the ENTER key:
Line 272:      Input Text    name=q    Stephen\ Hawking
Line 273:      Press Keys    name=q    ENTER
Line 274: Notice that we had to escape the space between the first name and
Line 275: surname of Stephen Hawking, and that's because spaces are used to
Line 276: separate arguments of commands in Robot, so we wanted the name and
Line 277: surname to figure together as a single argument of the Input Text
Line 278: command instead of them being treated as separate arguments.
Line 279: 
Line 280: --- 페이지 300 ---
Line 281: End-to-End Testing with the Robot Framework
Line 282: Chapter 12
Line 283: [ 290 ]
Line 284: At this point, if everything worked correctly, we should see the search results showing
Line 285: Wikipedia as one of them, if not the first:
Line 286: Figure 12.4 – Google search results for "Stephen Hawking"
Line 287: 
Line 288: --- 페이지 301 ---
Line 289: End-to-End Testing with the Robot Framework
Line 290: Chapter 12
Line 291: [ 291 ]
Line 292: As we are writing a test, the subsequent line is meant to assert the condition for our test, so
Line 293: it's going to check that Wikipedia is one of the results:
Line 294: Page Should Contain    Wikipedia
Line 295: Once we have verified that everything worked as expected, as we have nothing else to do,
Line 296: we can submit the last command to close the browser window and move forward:
Line 297: Close Window
Line 298: Recording the execution of tests
Line 299: As we have seen, while tests are running, the browser window is on screen and every
Line 300: action we perform is visible. As we obviously don't want to stare at our tests while they
Line 301: run, it would be convenient to have recordings of them available, so that we can see what
Line 302: happened during those tests in case of a failure.
Line 303: Luckily for us, the Robot Framework has a ScreenCapLibrary library that allows
Line 304: screenshots and video recordings of our tests to be made. Once the robotframework-
Line 305: screencaplibrary Python distribution is installed with pip, we will be able to use its
Line 306: commands by adding it to our test's *** Settings *** section:
Line 307: *** Settings ***
Line 308: Library    SeleniumLibrary
Line 309: Library    ScreenCapLibrary
Line 310: To record the execution of a test, we just have to begin it with a Start Video Recording
Line 311: command and then end it with a Stop Video Recording one:
Line 312: *** Test Cases ***
Line 313: Search On Google
Line 314:      Start Video Recording
Line 315:      Open Browser    http://www.google.com    Chrome
Line 316:      Wait Until Page Contains Element    cnsw
Line 317:      Select Frame    //iframe
Line 318:      Submit Form    //form
Line 319:      Input Text    name=q    Stephen\ Hawking
Line 320:      Press Keys    name=q   ENTER
Line 321:      Stop Video Recording
Line 322:      Page Should Contain    Wikipedia
Line 323:      Close Window
Line 324: 
Line 325: --- 페이지 302 ---
Line 326: End-to-End Testing with the Robot Framework
Line 327: Chapter 12
Line 328: [ 292 ]
Line 329: Screenshots and videos taken with the test are embedded within the log.html document,
Line 330: so we can see the result of our recording by looking at the log file:
Line 331: Figure 12.5 – Test execution log with video recording embedded
Line 332: ScreenCapLibrary recordings will be available only if the step that saves them succeeds.
Line 333: Therefore, we need to pay attention when writing our tests to ensure that recordings are
Line 334: saved (which means stopping the recording before any assertion). In our short test, for
Line 335: example, we placed the Stop Video Recording command before the Page Should
Line 336: Contain Wikipedia one. This ensures that even if Wikipedia is not included in the
Line 337: results, the recording will still be visible:
Line 338: 
Line 339: --- 페이지 303 ---
Line 340: End-to-End Testing with the Robot Framework
Line 341: Chapter 12
Line 342: [ 293 ]
Line 343: Figure 12.6 – Test execution log with the recording even if the test assertion failed
Line 344: 
Line 345: --- 페이지 304 ---
Line 346: End-to-End Testing with the Robot Framework
Line 347: Chapter 12
Line 348: [ 294 ]
Line 349: At the other end, in the event of any failure, the SeleniumLibrary library will make a
Line 350: screenshot of the web browser. So, even if our video doesn't get recorded, we will always
Line 351: have available screenshots of the state of the browser at the time the command failed.
Line 352: A more robust approach for handling recording is to rely on the Test Setup and Test
Line 353: Teardown phases of Robot so that we can start and stop the recording on every test
Line 354: automatically and even in case of failures. So if, for example, we move our Start Video
Line 355: Recording and Stop Video Recording commands into those two phases within the
Line 356: Settings section, we will have a reliable recording even in the event of failures:
Line 357: *** Settings ***
Line 358: Library    SeleniumLibrary
Line 359: Library    ScreenCapLibrary
Line 360: Test Setup    Start Video Recording
Line 361: Test Teardown    Stop Video Recording
Line 362: *** Test Cases ***
Line 363: Search On Google
Line 364:      Open Browser    http://www.google.com    Chrome
Line 365:      Wait Until Page Contains Element    cnsw
Line 366:      Select Frame    //iframe
Line 367:      Submit Form    //form
Line 368:      Input Text    name=q    Stephen\ Hawking
Line 369:      Press Keys    name=q    ENTER
Line 370:      Page Should Contain    Wikipedia
Line 371:      Close Window
Line 372: Now, our recording will be started automatically on all tests and stopped when they end,
Line 373: even if they fail.
Line 374: It's generally a good idea to make sure that your test suite has a Suite
Line 375: Teardown step with a Close All Browsers command in the ***
Line 376: Settings *** section. This will ensure that all browser processes and
Line 377: windows are properly destroyed when the test suite finishes running.
Line 378: Some browsers tend to leave behind running processes after the tests have
Line 379: run, and so might slow down your system if you run the test suite
Line 380: multiple times.
Line 381: 
Line 382: --- 페이지 305 ---
Line 383: End-to-End Testing with the Robot Framework
Line 384: Chapter 12
Line 385: [ 295 ]
Line 386: Testing with headless browsers
Line 387: Even if it's convenient to be able to see what's going on during tests, during our daily
Line 388: development cycle, we don't want to have browser windows popping up in the middle of
Line 389: our screen and preventing us from doing anything else apart from looking at our tests
Line 390: running.
Line 391: For this reason, it's frequently convenient to be able to run tests without real browser
Line 392: windows opening. This can be done by using a headless browser, in other words, a
Line 393: browser without a UI.
Line 394: With Chrome, for example, this can be done in the Open Browser command by
Line 395: choosing the headlesschrome browser instead of Chrome. Using headlesschrome will
Line 396: prevent browser windows from popping up, but will still retain the majority of the
Line 397: features: 
Line 398: *** Test Cases ***
Line 399: Search On Google
Line 400:      Open Browser    http://www.google.com    headlesschrome
Line 401:      Wait Until Page Contains Element    cnsw
Line 402:      Select Frame    //iframe
Line 403:      Submit Form    //form
Line 404:      Input Text    name=q    Stephen\ Hawking
Line 405:      Press Keys    name=q   ENTER
Line 406:      Page Should Contain    Wikipedia
Line 407:      Close Window
Line 408: Unfortunately, while Robot will retain the same behaviors when running with a headless
Line 409: browser, the websites themselves might not. So, for example, in our case, the test will fail
Line 410: because Google won't show up the privacy policy acceptance dialog when running with a
Line 411: headless browser:
Line 412: $ robot searchgoogle.robot
Line 413: =======================================================
Line 414: Searchgoogle
Line 415: =======================================================
Line 416: Search On Google                               | FAIL |
Line 417: Element 'cnsw' did not appear in 5 seconds.
Line 418: -------------------------------------------------------
Line 419: Searchgoogle                                   | FAIL |
Line 420: 1 critical test, 0 passed, 1 failed
Line 421: 1 test total, 0 passed, 1 failed
Line 422: =======================================================
Line 423: 
Line 424: --- 페이지 306 ---
Line 425: End-to-End Testing with the Robot Framework
Line 426: Chapter 12
Line 427: [ 296 ]
Line 428: To address this issue, we can make the commands related to the privacy policy conditional
Line 429: and only run them when a normal browser is in use. To do so, the first step is to refactor the
Line 430: selected browser into a variable so that we can more easily change which browser we are
Line 431: going to use:
Line 432: *** Variables ***
Line 433: ${BROWSER}    chrome
Line 434: *** Test Cases ***
Line 435: Search On Google
Line 436:     Open Browser    http://www.google.com    ${BROWSER}
Line 437:     ...
Line 438: Now that we can easily change which browser we use just by changing the ${BROWSER}
Line 439: variable, we can check whether that variable contains "headlesschrome" to skip the
Line 440: privacy policy part in the case of the Chrome browser in headless mode.
Line 441: To make an instruction conditional, we can use the Run Keyword If command. Tweaking
Line 442: our test that way will make sure that it succeeds both when using a real browser or a
Line 443: headless one:
Line 444: *** Settings ***
Line 445: Library    SeleniumLibrary
Line 446: Library    ScreenCapLibrary
Line 447: Test Setup Start    Video Recording
Line 448: Test Teardown Stop    Video Recording
Line 449: *** Variables ***
Line 450: ${BROWSER}    headlesschrome
Line 451: ${NOTHEADLESS}=    "headlesschrome" not in "${BROWSER}"
Line 452: *** Test Cases ***
Line 453: Search On Google
Line 454:      Open Browser    http://www.google.com    ${BROWSER}
Line 455:      Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
Line 456:          cnsw
Line 457:      Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
Line 458:      Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
Line 459:      Input Text    name=q    Stephen\ Hawking
Line 460:      Press Keys    name=q    ENTER
Line 461:      Page Should Contain    Wikipedia
Line 462:      Close Window
Line 463: To avoid repeating the condition over and over, we also refactored the "headlesschrome"
Line 464: not in "${BROWSER}" expression into a variable so that we can just check for that
Line 465: variable.
Line 466: 
Line 467: --- 페이지 307 ---
Line 468: End-to-End Testing with the Robot Framework
Line 469: Chapter 12
Line 470: [ 297 ]
Line 471: Now that we have conditional execution of the instructions that caused problems when
Line 472: using a headless browser, we can rerun our test:
Line 473: $ robot searchgoogle.robot
Line 474: =======================================================
Line 475: Searchgoogle
Line 476: =======================================================
Line 477: Search On Google                               | PASS |
Line 478: -------------------------------------------------------
Line 479: Searchgoogle                                   | PASS |
Line 480: 1 critical test, 1 passed, 0 failed
Line 481: 1 test total, 1 passed, 0 failed
Line 482: =======================================================
Line 483: Now, our tests finally passed using a headless browser and we learned how to use
Line 484: variables and conditional execution in Robot tests.
Line 485: Testing multiple browsers
Line 486: Now that we know how to run tests in Chrome, headless or not, it might be reasonable to
Line 487: feel the need to verify that our web application actually works on other browsers, too. So
Line 488: the question might be how we can also verify it on Firefox or Edge.
Line 489: Luckily for us, we just refactored the browser in use to be a variable, so we can just change
Line 490: that variable and have all our tests run on one browser or the other. 
Line 491: But if we want to make this part of our CI, it's not very convenient to change the tests file in
Line 492: the middle of our CI runs. For this reason, Robot allows the provision of variable values
Line 493: through the command line using the --variable option. For example, to use Firefox, we
Line 494: could pass --variables browser:firefox:
Line 495: $ robot --variable browser:firefox searchgoogle.robot
Line 496: =====================================================
Line 497: Searchgoogle
Line 498: =====================================================
Line 499: Search On Google                             | FAIL |
Line 500: Element with locator 'name=q' not found.
Line 501: -----------------------------------------------------
Line 502: Searchgoogle                                 | FAIL |
Line 503: 1 critical test, 0 passed, 1 failed
Line 504: 1 test total, 0 passed, 1 failed
Line 505: =====================================================
Line 506: 
Line 507: --- 페이지 308 ---
Line 508: End-to-End Testing with the Robot Framework
Line 509: Chapter 12
Line 510: [ 298 ]
Line 511: Surprisingly, when run with Firefox, our test failed. This is not only because websites might
Line 512: behave differently when using different browsers, but also because the browsers
Line 513: themselves might behave differently.
Line 514: For example, Firefox didn't select back the primary page after we accepted the privacy
Line 515: policy, so it's still trying to act inside the iframe that contained the privacy policy. This
Line 516: makes it impossible for the browser to find the input with name=q, where it's meant to
Line 517: write the query string, and so the test is failing.
Line 518: To fix this, we can modify our test slightly to Unselect Frame after we have finished with
Line 519: it:
Line 520: *** Test Cases ***
Line 521: Search On Google
Line 522:      Open Browser    http://www.google.com    ${BROWSER}
Line 523:      Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
Line 524:          cnsw
Line 525:      Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
Line 526:      Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
Line 527:      Unselect Frame
Line 528:      Input Text    name=q    Stephen\ Hawking
Line 529:      Press Keys    name=q    ENTER
Line 530:      Page Should Contain    Wikipedia
Line 531:      Close Window
Line 532: This will make sure that the test is able to accept the privacy policy and go back to the
Line 533: search field in both Chrome and Firefox, thus solving our problem. Now that we are able to
Line 534: perform the search, let's go back to our tests and see what happens when rerunning them:
Line 535: $ robot --variable browser:firefox searchgoogle.robot
Line 536: =====================================================
Line 537: Searchgoogle
Line 538: =====================================================
Line 539: Search On Google                             | FAIL |
Line 540: Page should have contained text 'Wikipedia' but did not.
Line 541: -----------------------------------------------------
Line 542: Searchgoogle                                 | FAIL |
Line 543: 1 critical test, 0 passed, 1 failed
Line 544: 1 test total, 0 passed, 1 failed
Line 545: =====================================================
Line 546: Another apparent failure is that even though the search happened correctly, the browser
Line 547: was unable to find Wikipedia in the results.
Line 548: 
Line 549: --- 페이지 309 ---
Line 550: End-to-End Testing with the Robot Framework
Line 551: Chapter 12
Line 552: [ 299 ]
Line 553: In this case, the log.html output can immediately help us understand what's going wrong.
Line 554: If we look at it, we will see that the problem is that by the time our test checks for
Line 555: "Wikipedia", the web page has not yet loaded the results themselves. The search box is
Line 556: still visible in the screenshot that the log file contains:
Line 557: Figure 12.7 – The log for our test that failed because Firefox was slower than the test itself
Line 558: 
Line 559: --- 페이지 310 ---
Line 560: End-to-End Testing with the Robot Framework
Line 561: Chapter 12
Line 562: [ 300 ]
Line 563: We can fix this by waiting for the search results to appear before performing the assertion,
Line 564: so let's tweak our search test a bit more to include an explicit wait for the results:
Line 565: *** Test Cases ***
Line 566: Search On Google
Line 567:      Open Browser    http://www.google.com    ${BROWSER}
Line 568:      Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
Line 569:          cnsw
Line 570:      Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
Line 571:      Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
Line 572:      Unselect Frame
Line 573:      Input Text    name=q    Stephen\ Hawking
Line 574:      Press Keys    name=q    SPACE
Line 575:      Press Keys    name=q    ENTER
Line 576:      Wait Until Page Contains Element    id=res
Line 577:      Page Should Contain    Wikipedia
Line 578:      Close Window
Line 579: This last version of our test is finally able to pass in connection with all the browsers we
Line 580: were concerned with, Firefox and Chrome, with both of them in headless mode too:
Line 581: $ robot --variable browser:headlessfirefox searchgoogle.robot
Line 582: =============================================================
Line 583: Searchgoogle
Line 584: =============================================================
Line 585: Search On Google                                     | PASS |
Line 586: -------------------------------------------------------------
Line 587: Searchgoogle                                         | PASS |
Line 588: 1 critical test, 1 passed, 0 failed
Line 589: 1 test total, 1 passed, 0 failed
Line 590: =============================================================
Line 591: At this point, we know how to write tests in Robot and how to write them so that we can
Line 592: verify them using multiple different browsers.
Line 593: Extending the Robot Framework
Line 594: As we have seen, Robot can be expanded with libraries that can add more keywords. That
Line 595: can be a convenient feature also for us when writing tests. If we have a set of instructions
Line 596: that we are going to repeat frequently in our tests, it would be convenient to factor them
Line 597: into a single keyword that we can reuse. Furthermore, Robot can be expanded with new
Line 598: custom commands that we can implement in Python.
Line 599: 
Line 600: --- 페이지 311 ---
Line 601: End-to-End Testing with the Robot Framework
Line 602: Chapter 12
Line 603: [ 301 ]
Line 604: Adding custom keywords
Line 605: To see how extending Robot with custom keywords works, we are going to create a very
Line 606: simple customkeywords.robot test file, where we are going to write a basic script that
Line 607: only greets us:
Line 608: *** Test Cases ***
Line 609: Use Custom Keywords
Line 610:     Echo Hello
Line 611: Running the script will fail as we have not yet implemented the Echo Hello keyword, so
Line 612: how can we provide it? For this purpose, Robot supports a *** Keywords *** section,
Line 613: where we can declare all our custom keywords, so let's declare our keyword there:
Line 614: *** Keywords ***
Line 615: Echo Hello
Line 616:     Log Hello!
Line 617: *** Test Cases ***
Line 618: Use Custom Keywords
Line 619:     Echo Hello
Line 620: The Echo Hello keyword is just going to invoke the built-in Log keyword, passing a
Line 621: hardcoded greeting string, so it's not very helpful, but we could actually list any kind or
Line 622: amount of commands within a custom keyword, so we could make it do whatever we
Line 623: needed.
Line 624: Now that we have provided a declaration for the Echo Hello command, rerunning the
Line 625: tests will succeed:
Line 626: $ robot customkeywords.robot
Line 627: ===================================================
Line 628: Customkeywords
Line 629: ===================================================
Line 630: Use Custom Keywords                        | PASS |
Line 631: ---------------------------------------------------
Line 632: Customkeywords                             | PASS |
Line 633: 1 critical test, 1 passed, 0 failed
Line 634: 1 test total, 1 passed, 0 failed
Line 635: ===================================================
Line 636: The output of our logging is not visible on the shell from which we started the Robot
Line 637: command, but if we open the log.html file, we will see that the string was correctly
Line 638: logged in that document.
Line 639: 
Line 640: --- 페이지 312 ---
Line 641: End-to-End Testing with the Robot Framework
Line 642: Chapter 12
Line 643: [ 302 ]
Line 644: Extending Robot from Python
Line 645: Going further, we can expand Robot with new libraries that we can implement in Python.
Line 646: To do so, we have to create a Python package with the name of the library and install it. All
Line 647: the non-internal functions we declare in the installed library will become available in our
Line 648: Robot scripts once we enable the library itself with the usual Library command.
Line 649: So, let's replicate what we just did using Python. The first step is to create the distribution
Line 650: for the library so that it can be installed. Therefore, we are going to create a hellolibrary
Line 651: directory where we are going to put our hellolibrary/setup.py file:
Line 652: from setuptools import setup
Line 653: setup(name='robotframework-hellolibrary', packages=['HelloLibrary'])
Line 654: Within this directory, we need to create a HelloLibrary package. This will be what gets
Line 655: installed and what gets loaded using the Library command in Robot. So let's create
Line 656: a hellolibrary/HelloLibrary/__init__.py file so that the nested directory gets
Line 657: recognized as a package by Python.
Line 658: Inside the __init__.py file, we are going to declare the HelloLibrary class with a
Line 659: say_hello method. The say_hello method, as a public method, will be automatically
Line 660: exposed in Robot as the Say Hello keyword of the library:
Line 661: class HelloLibrary:
Line 662:     def say_hello(self):
Line 663:         print("Hello from Python!")
Line 664: Now that all the pieces are in place, we can install our library so that it becomes available to
Line 665: Robot for installation using pip, as we would for any other Python distribution:
Line 666: $ pip install -e hellolibrary/
Line 667: Obtaining file://hellolibrary
Line 668: Installing collected packages: robotframework-hellolibrary
Line 669:   Running setup.py develop for robotframework-hellolibrary
Line 670: Successfully installed robotframework-hellolibrary
Line 671: 
Line 672: --- 페이지 313 ---
Line 673: End-to-End Testing with the Robot Framework
Line 674: Chapter 12
Line 675: [ 303 ]
Line 676: Once our library is installed, we can use it as we would for any other Robot library. Adding
Line 677: a Library HelloLibrary instruction to our Settings section will make the Say Hello
Line 678: keyword available for our own use:
Line 679: *** Settings ***
Line 680: Library HelloLibrary
Line 681: *** Keywords ***
Line 682: Echo Hello
Line 683:     Log Hello!
Line 684: *** Test Cases ***
Line 685: Use Custom Keywords
Line 686:     Echo Hello
Line 687:     Say Hello
Line 688: We can confirm that everything worked as expected by rerunning Robot. If we didn't make
Line 689: any error and the library was installed correctly, our tests should succeed again:
Line 690: $ robot customkeywords.robot
Line 691: ===================================================
Line 692: Customkeywords
Line 693: ===================================================
Line 694: Use Custom Keywords                        | PASS |
Line 695: ---------------------------------------------------
Line 696: Customkeywords                             | PASS |
Line 697: 1 critical test, 1 passed, 0 failed
Line 698: 1 test total, 1 passed, 0 failed
Line 699: ===================================================
Line 700: 
Line 701: --- 페이지 314 ---
Line 702: End-to-End Testing with the Robot Framework
Line 703: Chapter 12
Line 704: [ 304 ]
Line 705: Like we did for the Echo Hello keyword, we can verify that our Say Hello keyword
Line 706: worked properly and logged the "Hello from Python!" message by looking at the
Line 707: log.html file:
Line 708: Figure 12.8 – Log of the test using our custom commands
Line 709: 
Line 710: --- 페이지 315 ---
Line 711: End-to-End Testing with the Robot Framework
Line 712: Chapter 12
Line 713: [ 305 ]
Line 714: By default, a new library object is created for every test, so a new instance of our
Line 715: HelloLibrary class would be made on every test. In case we needed to share a single
Line 716: object across all tests, we could set the HelloLibrary.ROBOT_LIBRARY_SCOPE =
Line 717: "SUITE" class attribute, which would signal to Robot to create only once instance and share
Line 718: it across all tests of the same suite. Furthermore, we could set that attribute
Line 719: to ROBOT_LIBRARY_SCOPE = "GLOBAL" and make the instance unique for the whole test
Line 720: run. This allows us to share the internal state of our library object across multiple tests in
Line 721: case we need to preserve any information.
Line 722: Summary
Line 723: In this chapter, we saw how we can go further and not only test the responses that our web
Line 724: applications provide, but also that those responses work for real once they are handled by a
Line 725: web browser.
Line 726: Now that we have covered Robot, we have all the tools we need to test our web
Line 727: applications across all stack levels. We know how to use PyTest for building block unit
Line 728: tests, WebTest for functional and integration tests, and Robot for end-to-end tests involving
Line 729: real browsers. So we are now able to write fully tested web applications, paired with the
Line 730: best practices for TDD and ATDD, which we learned in earlier chapters, and we should be
Line 731: able to build a solid development routine that allows us to create robust web applications
Line 732: that are also safe to evolve and refactor over time.