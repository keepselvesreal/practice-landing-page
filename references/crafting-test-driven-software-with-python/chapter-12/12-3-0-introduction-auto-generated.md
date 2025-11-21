# 12.3.0 Introduction [auto-generated] (pp.286-291)

---
**Page 286**

End-to-End Testing with the Robot Framework
Chapter 12
[ 286 ]
Now that we know how the Robot Framework works, we can move on to the next steps
and see how we can use it to test web applications with a real browser. 
Testing with web browsers
We have seen how, using libraries, we can extend Robot with additional commands that
allow us to write most different kinds of tests. One of the most frequent use cases for Robot
is actually web development as it has a very convenient SeleniumLibrary library that
provides many commands to control a real web browser and perform tests that can involve
JavaScript (Selenium library reference: https:/​/​robotframework.​org/​SeleniumLibrary/
SeleniumLibrary.​html).
Once we have installed the robotframework and robotframework-
seleniumlibrary Python distributions, in order to be able to write tests that involve a real
browser, we will need to enable the web drivers for the browsers we want to use. So, we
will need those browsers to be available and then, through the webdrivermanager utility
that we installed previously, we can enable the drivers for all the browsers we have
available:
$ webdrivermanager firefox chrome
Downloading WebDriver for browser: "firefox"
2588kb [00:01, 1978.35kb/s]
Driver binary downloaded to:
"./venv/WebDriverManager/gecko/v0.28.0/geckodriver-v0.28.0-
linux64/geckodriver"
Symlink created: ./venv/bin/geckodriver
Downloading WebDriver for browser: "chrome"
5979kb [00:01, 3615.18kb/s]
Driver binary downloaded to:
"./venv/WebDriverManager/chrome/87.0.4280.88/chromedriver_linux64/chromedri
ver"
Symlink created: ./venv/bin/chromedriver
Notice that the examples take for granted the fact that everything is
happening inside a Python virtual environment, so keep in mind that
when using a virtual environment, the drivers are only available inside
that environment, and if you create a new one you will need to enable the
drivers again.
Once we have the drivers available, Robot will be able to control the browsers for which we
provided the drivers (in this case, Chrome and Firefox), so we can go back to our editor and
create a new test to establish how Robot works.


---
**Page 287**

End-to-End Testing with the Robot Framework
Chapter 12
[ 287 ]
In this case, we are going to create a test where we search on Google for a famous person
and verify that Wikipedia is included in the results returned. To do so, let's create a
searchgoogle.robot file were we are going to enable the SeleniumLibrary library so
that browser-related commands become available:
*** Settings ***
Library SeleniumLibrary
The next step is then to write the test itself to open Google with Chrome, accept the privacy
policy, perform the search, and then check that Wikipedia is included in the results:
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
If we run our test, a Chrome window will pop up, perform the search, and then close again,
with our test regarded as having passed if everything went right:
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
Our test might look a bit complex, and that's because the Google website requires us to
accept a privacy policy before we can start searching. So, the first commands are related to
opening Google itself using Chrome and then waiting for the privacy policy (with id=cnsw
in HTML) to appear:
     Open Browser    http://www.google.com    Chrome
     Wait Until Page Contains Element    cnsw


---
**Page 288**

End-to-End Testing with the Robot Framework
Chapter 12
[ 288 ]
Once the browser opens the Google website, we should be greeted by the privacy policy
acceptance box:
Figure 12.2 – Google website with the policy acceptance request
In case you don't see the privacy policy when opening the Google website,
don't worry. Google decides if to show the privacy policy or not based on
the country and browser you are connecting from. If you country doesn't
have any privacy policy requirement, Google might not show the policy.
In such case you can omit the three "Wait Until Page Contains Element",
"Select Frame" and "Submit Form" commands related to managing the
privacy policy or just read further until we tackle headless browser later
in the chapter and run the examples using Google Chrome browser in
headless mode.
Once the privacy policy is visible, we are going to pick the iframe within which it gets 
displayed and submit the first form that exists within it:
     Select Frame    //iframe
     Submit Form    //form


---
**Page 289**

End-to-End Testing with the Robot Framework
Chapter 12
[ 289 ]
Submitting the form will make the privacy policy alert disappear and will finally reveal the
search box:
Figure 12.3 – Google website once the privacy policy has been accepted
At this point, we just have to write the name of the person we want to search for in the
search box (which has name=q in HTML) and submit it by pressing the ENTER key:
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
Notice that we had to escape the space between the first name and
surname of Stephen Hawking, and that's because spaces are used to
separate arguments of commands in Robot, so we wanted the name and
surname to figure together as a single argument of the Input Text
command instead of them being treated as separate arguments.


---
**Page 290**

End-to-End Testing with the Robot Framework
Chapter 12
[ 290 ]
At this point, if everything worked correctly, we should see the search results showing
Wikipedia as one of them, if not the first:
Figure 12.4 – Google search results for "Stephen Hawking"


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


