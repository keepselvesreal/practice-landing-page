# 12.3.2 Testing with headless browsers (pp.295-297)

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


---
**Page 296**

End-to-End Testing with the Robot Framework
Chapter 12
[ 296 ]
To address this issue, we can make the commands related to the privacy policy conditional
and only run them when a normal browser is in use. To do so, the first step is to refactor the
selected browser into a variable so that we can more easily change which browser we are
going to use:
*** Variables ***
${BROWSER}    chrome
*** Test Cases ***
Search On Google
    Open Browser    http://www.google.com    ${BROWSER}
    ...
Now that we can easily change which browser we use just by changing the ${BROWSER}
variable, we can check whether that variable contains "headlesschrome" to skip the
privacy policy part in the case of the Chrome browser in headless mode.
To make an instruction conditional, we can use the Run Keyword If command. Tweaking
our test that way will make sure that it succeeds both when using a real browser or a
headless one:
*** Settings ***
Library    SeleniumLibrary
Library    ScreenCapLibrary
Test Setup Start    Video Recording
Test Teardown Stop    Video Recording
*** Variables ***
${BROWSER}    headlesschrome
${NOTHEADLESS}=    "headlesschrome" not in "${BROWSER}"
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    ${BROWSER}
     Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
         cnsw
     Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
     Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
     Page Should Contain    Wikipedia
     Close Window
To avoid repeating the condition over and over, we also refactored the "headlesschrome"
not in "${BROWSER}" expression into a variable so that we can just check for that
variable.


---
**Page 297**

End-to-End Testing with the Robot Framework
Chapter 12
[ 297 ]
Now that we have conditional execution of the instructions that caused problems when
using a headless browser, we can rerun our test:
$ robot searchgoogle.robot
=======================================================
Searchgoogle
=======================================================
Search On Google                               | PASS |
-------------------------------------------------------
Searchgoogle                                   | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
=======================================================
Now, our tests finally passed using a headless browser and we learned how to use
variables and conditional execution in Robot tests.
Testing multiple browsers
Now that we know how to run tests in Chrome, headless or not, it might be reasonable to
feel the need to verify that our web application actually works on other browsers, too. So
the question might be how we can also verify it on Firefox or Edge.
Luckily for us, we just refactored the browser in use to be a variable, so we can just change
that variable and have all our tests run on one browser or the other. 
But if we want to make this part of our CI, it's not very convenient to change the tests file in
the middle of our CI runs. For this reason, Robot allows the provision of variable values
through the command line using the --variable option. For example, to use Firefox, we
could pass --variables browser:firefox:
$ robot --variable browser:firefox searchgoogle.robot
=====================================================
Searchgoogle
=====================================================
Search On Google                             | FAIL |
Element with locator 'name=q' not found.
-----------------------------------------------------
Searchgoogle                                 | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=====================================================


