# 12.3.1 Recording the execution of tests (pp.291-295)

---
**Page 291**

End-to-End Testing with the Robot Framework
Chapter 12
[ 291 ]
As we are writing a test, the subsequent line is meant to assert the condition for our test, so
it's going to check that Wikipedia is one of the results:
Page Should Contain    Wikipedia
Once we have verified that everything worked as expected, as we have nothing else to do,
we can submit the last command to close the browser window and move forward:
Close Window
Recording the execution of tests
As we have seen, while tests are running, the browser window is on screen and every
action we perform is visible. As we obviously don't want to stare at our tests while they
run, it would be convenient to have recordings of them available, so that we can see what
happened during those tests in case of a failure.
Luckily for us, the Robot Framework has a ScreenCapLibrary library that allows
screenshots and video recordings of our tests to be made. Once the robotframework-
screencaplibrary Python distribution is installed with pip, we will be able to use its
commands by adding it to our test's *** Settings *** section:
*** Settings ***
Library    SeleniumLibrary
Library    ScreenCapLibrary
To record the execution of a test, we just have to begin it with a Start Video Recording
command and then end it with a Stop Video Recording one:
*** Test Cases ***
Search On Google
     Start Video Recording
     Open Browser    http://www.google.com    Chrome
     Wait Until Page Contains Element    cnsw
     Select Frame    //iframe
     Submit Form    //form
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q   ENTER
     Stop Video Recording
     Page Should Contain    Wikipedia
     Close Window


---
**Page 292**

End-to-End Testing with the Robot Framework
Chapter 12
[ 292 ]
Screenshots and videos taken with the test are embedded within the log.html document,
so we can see the result of our recording by looking at the log file:
Figure 12.5 – Test execution log with video recording embedded
ScreenCapLibrary recordings will be available only if the step that saves them succeeds.
Therefore, we need to pay attention when writing our tests to ensure that recordings are
saved (which means stopping the recording before any assertion). In our short test, for
example, we placed the Stop Video Recording command before the Page Should
Contain Wikipedia one. This ensures that even if Wikipedia is not included in the
results, the recording will still be visible:


---
**Page 293**

End-to-End Testing with the Robot Framework
Chapter 12
[ 293 ]
Figure 12.6 – Test execution log with the recording even if the test assertion failed


---
**Page 294**

End-to-End Testing with the Robot Framework
Chapter 12
[ 294 ]
At the other end, in the event of any failure, the SeleniumLibrary library will make a
screenshot of the web browser. So, even if our video doesn't get recorded, we will always
have available screenshots of the state of the browser at the time the command failed.
A more robust approach for handling recording is to rely on the Test Setup and Test
Teardown phases of Robot so that we can start and stop the recording on every test
automatically and even in case of failures. So if, for example, we move our Start Video
Recording and Stop Video Recording commands into those two phases within the
Settings section, we will have a reliable recording even in the event of failures:
*** Settings ***
Library    SeleniumLibrary
Library    ScreenCapLibrary
Test Setup    Start Video Recording
Test Teardown    Stop Video Recording
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    Chrome
     Wait Until Page Contains Element    cnsw
     Select Frame    //iframe
     Submit Form    //form
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
     Page Should Contain    Wikipedia
     Close Window
Now, our recording will be started automatically on all tests and stopped when they end,
even if they fail.
It's generally a good idea to make sure that your test suite has a Suite
Teardown step with a Close All Browsers command in the ***
Settings *** section. This will ensure that all browser processes and
windows are properly destroyed when the test suite finishes running.
Some browsers tend to leave behind running processes after the tests have
run, and so might slow down your system if you run the test suite
multiple times.


---
**Page 295**

End-to-End Testing with the Robot Framework
Chapter 12
[ 295 ]
Testing with headless browsers
Even if it's convenient to be able to see what's going on during tests, during our daily
development cycle, we don't want to have browser windows popping up in the middle of
our screen and preventing us from doing anything else apart from looking at our tests
running.
For this reason, it's frequently convenient to be able to run tests without real browser
windows opening. This can be done by using a headless browser, in other words, a
browser without a UI.
With Chrome, for example, this can be done in the Open Browser command by
choosing the headlesschrome browser instead of Chrome. Using headlesschrome will
prevent browser windows from popping up, but will still retain the majority of the
features: 
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    headlesschrome
     Wait Until Page Contains Element    cnsw
     Select Frame    //iframe
     Submit Form    //form
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q   ENTER
     Page Should Contain    Wikipedia
     Close Window
Unfortunately, while Robot will retain the same behaviors when running with a headless
browser, the websites themselves might not. So, for example, in our case, the test will fail
because Google won't show up the privacy policy acceptance dialog when running with a
headless browser:
$ robot searchgoogle.robot
=======================================================
Searchgoogle
=======================================================
Search On Google                               | FAIL |
Element 'cnsw' did not appear in 5 seconds.
-------------------------------------------------------
Searchgoogle                                   | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=======================================================


