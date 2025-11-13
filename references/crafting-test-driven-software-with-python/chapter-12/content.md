# Chapter 12: End-to-End Testing with the Robot Framework (pp.281-313)

---
**Page 281**

12
End-to-End Testing with the
Robot Framework
In the previous chapter, we saw how to test web applications and, in general, applications
that rely on the HTTP protocol, both client and server side, but we were unable to test how
they perform in a real browser. With their complex layouts, the fact that CSS and JavaScript
are heavily involved in testing your application with WebTest or a similar solution might
not be sufficient to guarantee users that they are actually able to work with it. What if a
button is created by JavaScript or it's disabled by CSS? Those conditions are hard to test
using WebTest and we might easily end up with a test that clicks that button even though
the button wasn't actually usable by users.
To guarantee that our applications behave properly, it is a good idea to have a few tests that
verify at least the more important areas of the application using a real browser. As those
kinds of tests tend to be very slow and fragile, you still want to have the majority of your
tests written using solutions such as WebTest or even unit tests, which don't involve the
whole application life cycle, but having the most important parts of the web application
verified using real browsers will guarantee that at least the critical path of your web
application works on all major browsers. 
The Robot framework is one of the most solid solutions for writing the end-to-end tests that
drive web browsers and mobile applications in the Python world. It was originally
developed by Nokia and evolved under the open source community, and is a long-standing
and solid solution with tons of documentation and plugins. It is therefore battle tested and
ready for your daily projects.
In this chapter, we will cover the following topics:
Introducing the Robot framework
Testing with web browsers
Extending the Robot framework


---
**Page 282**

End-to-End Testing with the Robot Framework
Chapter 12
[ 282 ]
Technical requirements
We need a working Python interpreter with the Robot Framework installed. To run tests
with real browsers, we are also going to use the robotframework-seleniumlibrary and
the webdrivermanager utilities. To record videos of our tests, we are going to need
the robotframework-screencaplibrary library. robotframework, robotframework-
seleniumlibrary, robotframework-screencaplibrary, and webdrivermanager can
be installed with pip, in the same way as all other Python dependencies:
$ pip install robotframework robotframework-seleniumlibrary
webdrivermanager robotframework-screencaplibrary
The examples have been written on Python 3.7, robotframework 3.2.2, robotframework-
seleniumlibrary 4.5.0, robotframework-screencaplibrary 1.5.0, and webdrivermanager 0.9.0,
but should work on most modern Python versions. 
You can find the code present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter12.
Introducing the Robot Framework
The Robot Framework is an automation framework mostly used to create acceptance tests
in the Acceptance Test Driven Development (ATDD)  and Behavior Driven
Development (BDD) styles. Tests are written in a custom, natural English-like language
that can be easily extended in Python, so Robot can, in theory, be used to write any kind of
acceptance tests in a format that can be shared with other stakeholders, pretty much like
what we have seen we can do with pytest-bdd in previous chapters.
The primary difference is that Robot is not based on PyTest, it is a replacement for PyTest,
and is widely used to create end-to-end tests for mobile and web applications. For mobile
applications, the Appium library allows us to write Robot Framework tests that control
mobile applications on a real device, while the Selenium library provides a complete
integration with web browsers, which means that the Robot Framework allows us to write
tests that drive a real web browser and verify the results.
Robot Framework tests are written inside .robot files, which are then divided into
multiple sections by the section headers. The most frequently used section headers are the
following:
*** Settings ***: This contains options to configure Robot itself.
*** Variables ***: This contains variables to reuse across multiple tests.


---
**Page 283**

End-to-End Testing with the Robot Framework
Chapter 12
[ 283 ]
*** Test Cases ***: This contains our tests.
*** Keywords ***: This contains our own custom commands.
So, the minimum content of a .robot file is usually a Test Cases section with a test
inside. Each test is then a collection of commands for the Robot Framework that are
provided by keywords made available by libraries for the Robot Framework itself.
The only library automatically available by default in the Robot Framework is the
Builtin one (Builtin library reference: https:/​/​robotframework.​org/​robotframework/
latest/​libraries/​BuiltIn.​html), which provides some generally helpful commands such
as Should Contain to check the content of a variable, or Expression to run any Python
expression and assign the result to a variable.
Further libraries can be imported explicitly with the Library command in the Settings
section. Without involving explicit libraries that add more commands, Robot itself can't do
much. 
For example, if we want to create a very basic test where we save the "Hello World"
string into a file and verify its content, we would have to involve the OperatingSystem
library (OperatingSystem library reference: https:/​/​robotframework.​org/
robotframework/​latest/​libraries/​OperatingSystem.​html), which makes available
commands to interact with files, directories, and the system shell.
To create such a test, we would make a hellotest.robot file, where we can declare the
instruction for the Robot Framework. At the beginning of the file, we would declare a
Settings section, where we use the Library command to make the OperatingSystem
library available:
*** Settings ***
Library     OperatingSystem
In Robot, multiple spaces perform separate commands from their
arguments.
Through the OperatingSystem library, we will get the Run and Get File commands,
which we need to write our actual test.
Subsequently, we will declare the Test Cases section, where we can put all our tests. In
this case, we are going to place only one test, entitled Hello World.


---
**Page 284**

End-to-End Testing with the Robot Framework
Chapter 12
[ 284 ]
The test itself will create a new file with the "Hello World" string inside, and will then
read it back and check that the content contains the string "Hello":
*** Test Cases ***
Hello World
    Run    echo "Hello World" > hello.txt
    ${filecontent} =    Get File    hello.txt
    Should Contain    ${filecontent}    Hello
The first line of our test uses the Run keyword to invoke the echo command in a shell (if
you are on a *nix system, such as Linux or macOS X), and the echo command is invoked
with the Hello World argument and redirection is effected to the hello.txt file so that
the output of the command actually goes into that file.
Once that file is created, on the second line we use the Get File keyword to read the
content of the hello.txt file and assign what we read to the ${filecontent} variable.
Finally, we check through the Should Contain keyword that the variable contains the
string Hello.
Once we have saved all this as hellotest.robot, we should be able to run it by invoking
the robot command and see that our test is executed and passes:
$ robot hellotest.robot
=======================================================
Hellotest
=======================================================
Hello World                                    | PASS |
-------------------------------------------------------
Hellotest                                      | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
=======================================================
If we wanted to see what happens when our tests fail, we could change the Should
Contain line to a different string, for example, Should Contain    ${filecontent} 
  Bye and see what happens when we rerun our test:
$ robot hellotest.robot
=======================================================
Hellotest
=======================================================
Hello World                                    | FAIL |
'Hello World' does not contain 'Bye'
-------------------------------------------------------
Hellotest                                      | FAIL |


---
**Page 285**

End-to-End Testing with the Robot Framework
Chapter 12
[ 285 ]
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=======================================================
Details about what precisely went wrong are then made available in the log.html file,
where each command that Robot performed is recorded with debugging information.
Opening such a file in a browser will indicate explicitly that the command that failed is
Builtin.Should Contain and that it failed with the 'Hello World' does not
contain 'Bye' error:
Figure 12.1 – Detailed log of our test execution from log.html


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


---
**Page 298**

End-to-End Testing with the Robot Framework
Chapter 12
[ 298 ]
Surprisingly, when run with Firefox, our test failed. This is not only because websites might
behave differently when using different browsers, but also because the browsers
themselves might behave differently.
For example, Firefox didn't select back the primary page after we accepted the privacy
policy, so it's still trying to act inside the iframe that contained the privacy policy. This
makes it impossible for the browser to find the input with name=q, where it's meant to
write the query string, and so the test is failing.
To fix this, we can modify our test slightly to Unselect Frame after we have finished with
it:
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    ${BROWSER}
     Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
         cnsw
     Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
     Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
     Unselect Frame
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
     Page Should Contain    Wikipedia
     Close Window
This will make sure that the test is able to accept the privacy policy and go back to the
search field in both Chrome and Firefox, thus solving our problem. Now that we are able to
perform the search, let's go back to our tests and see what happens when rerunning them:
$ robot --variable browser:firefox searchgoogle.robot
=====================================================
Searchgoogle
=====================================================
Search On Google                             | FAIL |
Page should have contained text 'Wikipedia' but did not.
-----------------------------------------------------
Searchgoogle                                 | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=====================================================
Another apparent failure is that even though the search happened correctly, the browser
was unable to find Wikipedia in the results.


---
**Page 299**

End-to-End Testing with the Robot Framework
Chapter 12
[ 299 ]
In this case, the log.html output can immediately help us understand what's going wrong.
If we look at it, we will see that the problem is that by the time our test checks for
"Wikipedia", the web page has not yet loaded the results themselves. The search box is
still visible in the screenshot that the log file contains:
Figure 12.7 – The log for our test that failed because Firefox was slower than the test itself


---
**Page 300**

End-to-End Testing with the Robot Framework
Chapter 12
[ 300 ]
We can fix this by waiting for the search results to appear before performing the assertion,
so let's tweak our search test a bit more to include an explicit wait for the results:
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    ${BROWSER}
     Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
         cnsw
     Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
     Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
     Unselect Frame
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    SPACE
     Press Keys    name=q    ENTER
     Wait Until Page Contains Element    id=res
     Page Should Contain    Wikipedia
     Close Window
This last version of our test is finally able to pass in connection with all the browsers we
were concerned with, Firefox and Chrome, with both of them in headless mode too:
$ robot --variable browser:headlessfirefox searchgoogle.robot
=============================================================
Searchgoogle
=============================================================
Search On Google                                     | PASS |
-------------------------------------------------------------
Searchgoogle                                         | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
=============================================================
At this point, we know how to write tests in Robot and how to write them so that we can
verify them using multiple different browsers.
Extending the Robot Framework
As we have seen, Robot can be expanded with libraries that can add more keywords. That
can be a convenient feature also for us when writing tests. If we have a set of instructions
that we are going to repeat frequently in our tests, it would be convenient to factor them
into a single keyword that we can reuse. Furthermore, Robot can be expanded with new
custom commands that we can implement in Python.


---
**Page 301**

End-to-End Testing with the Robot Framework
Chapter 12
[ 301 ]
Adding custom keywords
To see how extending Robot with custom keywords works, we are going to create a very
simple customkeywords.robot test file, where we are going to write a basic script that
only greets us:
*** Test Cases ***
Use Custom Keywords
    Echo Hello
Running the script will fail as we have not yet implemented the Echo Hello keyword, so
how can we provide it? For this purpose, Robot supports a *** Keywords *** section,
where we can declare all our custom keywords, so let's declare our keyword there:
*** Keywords ***
Echo Hello
    Log Hello!
*** Test Cases ***
Use Custom Keywords
    Echo Hello
The Echo Hello keyword is just going to invoke the built-in Log keyword, passing a
hardcoded greeting string, so it's not very helpful, but we could actually list any kind or
amount of commands within a custom keyword, so we could make it do whatever we
needed.
Now that we have provided a declaration for the Echo Hello command, rerunning the
tests will succeed:
$ robot customkeywords.robot
===================================================
Customkeywords
===================================================
Use Custom Keywords                        | PASS |
---------------------------------------------------
Customkeywords                             | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
===================================================
The output of our logging is not visible on the shell from which we started the Robot
command, but if we open the log.html file, we will see that the string was correctly
logged in that document.


---
**Page 302**

End-to-End Testing with the Robot Framework
Chapter 12
[ 302 ]
Extending Robot from Python
Going further, we can expand Robot with new libraries that we can implement in Python.
To do so, we have to create a Python package with the name of the library and install it. All
the non-internal functions we declare in the installed library will become available in our
Robot scripts once we enable the library itself with the usual Library command.
So, let's replicate what we just did using Python. The first step is to create the distribution
for the library so that it can be installed. Therefore, we are going to create a hellolibrary
directory where we are going to put our hellolibrary/setup.py file:
from setuptools import setup
setup(name='robotframework-hellolibrary', packages=['HelloLibrary'])
Within this directory, we need to create a HelloLibrary package. This will be what gets
installed and what gets loaded using the Library command in Robot. So let's create
a hellolibrary/HelloLibrary/__init__.py file so that the nested directory gets
recognized as a package by Python.
Inside the __init__.py file, we are going to declare the HelloLibrary class with a
say_hello method. The say_hello method, as a public method, will be automatically
exposed in Robot as the Say Hello keyword of the library:
class HelloLibrary:
    def say_hello(self):
        print("Hello from Python!")
Now that all the pieces are in place, we can install our library so that it becomes available to
Robot for installation using pip, as we would for any other Python distribution:
$ pip install -e hellolibrary/
Obtaining file://hellolibrary
Installing collected packages: robotframework-hellolibrary
  Running setup.py develop for robotframework-hellolibrary
Successfully installed robotframework-hellolibrary


---
**Page 303**

End-to-End Testing with the Robot Framework
Chapter 12
[ 303 ]
Once our library is installed, we can use it as we would for any other Robot library. Adding
a Library HelloLibrary instruction to our Settings section will make the Say Hello
keyword available for our own use:
*** Settings ***
Library HelloLibrary
*** Keywords ***
Echo Hello
    Log Hello!
*** Test Cases ***
Use Custom Keywords
    Echo Hello
    Say Hello
We can confirm that everything worked as expected by rerunning Robot. If we didn't make
any error and the library was installed correctly, our tests should succeed again:
$ robot customkeywords.robot
===================================================
Customkeywords
===================================================
Use Custom Keywords                        | PASS |
---------------------------------------------------
Customkeywords                             | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
===================================================


---
**Page 304**

End-to-End Testing with the Robot Framework
Chapter 12
[ 304 ]
Like we did for the Echo Hello keyword, we can verify that our Say Hello keyword
worked properly and logged the "Hello from Python!" message by looking at the
log.html file:
Figure 12.8 – Log of the test using our custom commands


---
**Page 305**

End-to-End Testing with the Robot Framework
Chapter 12
[ 305 ]
By default, a new library object is created for every test, so a new instance of our
HelloLibrary class would be made on every test. In case we needed to share a single
object across all tests, we could set the HelloLibrary.ROBOT_LIBRARY_SCOPE =
"SUITE" class attribute, which would signal to Robot to create only once instance and share
it across all tests of the same suite. Furthermore, we could set that attribute
to ROBOT_LIBRARY_SCOPE = "GLOBAL" and make the instance unique for the whole test
run. This allows us to share the internal state of our library object across multiple tests in
case we need to preserve any information.
Summary
In this chapter, we saw how we can go further and not only test the responses that our web
applications provide, but also that those responses work for real once they are handled by a
web browser.
Now that we have covered Robot, we have all the tools we need to test our web
applications across all stack levels. We know how to use PyTest for building block unit
tests, WebTest for functional and integration tests, and Robot for end-to-end tests involving
real browsers. So we are now able to write fully tested web applications, paired with the
best practices for TDD and ATDD, which we learned in earlier chapters, and we should be
able to build a solid development routine that allows us to create robust web applications
that are also safe to evolve and refactor over time.


---
**Page 306**

 
Packt.com
Subscribe to our online digital library for full access to over 7,000 books and videos, as well
as industry leading tools to help you plan your personal development and advance your
career. For more information, please visit our website.
Why subscribe?
Spend less time learning and more time coding with practical eBooks and Videos
from over 4,000 industry professionals
Improve your learning with Skill Plans built especially for you
Get a free eBook or video every month
Fully searchable for easy access to vital information
Copy and paste, print, and bookmark content
Did you know that Packt offers eBook versions of every book published, with PDF and
ePub files available? You can upgrade to the eBook version at www.packt.com and as a print
book customer, you are entitled to a discount on the eBook copy. Get in touch with us
at customercare@packtpub.com for more details.
At www.packt.com, you can also read a collection of free technical articles, sign up for a
range of free newsletters, and receive exclusive discounts and offers on Packt books and
eBooks. 


---
**Page 307**

Other Books You May Enjoy
If you enjoyed this book, you may be interested in these other books by Packt:
Django 3 By Example - Third Edition
Antonio Melé
ISBN: 978-1-83898-195-2
Build real-world web applications
Learn Django essentials, including models, views, ORM, templates, URLs, forms,
and authentication
Implement advanced features such as custom model fields, custom template tags,
cache, middleware, localization, and more
Create complex functionalities, such as AJAX interactions, social authentication, a
full-text search engine, a payment system, a CMS, a RESTful API, and more
Integrate other technologies, including Redis, Celery, RabbitMQ, PostgreSQL,
and Channels, into your projects
Deploy Django projects in production using NGINX, uWSGI, and Daphne


---
**Page 308**

Other Books You May Enjoy
[ 308 ]
40 Algorithms Every Programmer Should Know
Imran Ahmad
ISBN: 978-1-78980-121-7
Explore existing data structures and algorithms found in Python libraries
Implement graph algorithms for fraud detection using network analysis
Work with machine learning algorithms to cluster similar tweets and process
Twitter data in real time
Predict the weather using supervised learning algorithms
Use neural networks for object detection
Create a recommendation engine that suggests relevant movies to subscribers
Implement foolproof security using symmetric and asymmetric encryption on
Google Cloud Platform (GCP)


---
**Page 309**

Other Books You May Enjoy
[ 309 ]
Packt is searching for authors like you
If you're interested in becoming an author for Packt, please
visit authors.packtpub.com and apply today. We have worked with thousands of
developers and tech professionals, just like you, to help them share their insight with the
global tech community. You can make a general application, apply for a specific hot topic
that we are recruiting an author for, or submit your own idea.
Leave a review - let other readers know what
you think
Please share your thoughts on this book with others by leaving a review on the site that you
bought it from. If you purchased the book from Amazon, please leave us an honest review
on this book's Amazon page. This is vital so that other potential readers can see and use
your unbiased opinion to make purchasing decisions, we can understand what our
customers think about our products, and our authors can see your feedback on the title that
they have worked with Packt to create. It will only take a few minutes of your time, but is
valuable to other potential customers, our authors, and Packt. Thank you!


---
**Page 310**

Index
A
Acceptance Test-Driven Development (ATDD)  82
acceptance tests
   about  25
   passing  169, 170, 172
   writing  165, 166
Act phase  15
And step
   used, for creating setup  175
Arrange phase  15
Arrange, Act, Assert pattern  15
Assert phase  15
authentication  22
authorization  22
automatic tests  9, 11
B
Behavior-Driven Development (BDD)
   about  172
   actions, performing with When step  176
   conditions, assessing with Then step  177
   feature file, defining  173
   scenario test, running  175
   scenario, declaring  174
   scenario, making to pass  178, 180
   setup, creating with And step  176
   using  172
behaviors
   checking, with spies  44, 45, 46, 47, 48, 49
benchmark runs
   comparing  198
black-box tests  25
C
capsys
   IO, testing with  149
chat application
   acceptance tests  56, 57, 59
   doubles  56, 57, 59
   working, with TDD  33, 35, 36, 37, 38
code-based reference
   adding  223, 225
commit tests  126
compile suite  125
component tests  21, 25
components
   replacing, with stubs  40, 41, 42, 43, 44
construction injection  60
continuous integration (CI)
   about  131
   enabling  131, 132, 133, 134, 135
   performance tests, running in cloud  136
contract tests  25
coverage reporting
   pytest-cov, using for  189, 192, 193
coverage
   testing  29
   using, as service  194, 195
D
dependencies
   managing, with dependency injection  60, 63
   replacing, with fakes  51, 52, 53, 54, 55
dependency injection frameworks
   using  63, 65, 66
dependency injection
   dependencies, managing with  60, 63
distribution
   testing  29
Django projects
   testing, with Django's test client  277, 279
   testing, with pytest  274, 276
Django tests


---
**Page 311**

[ 311 ]
   writing, with Django's test client  271, 272, 273
Django's test client
   Django tests, writing with  271, 272, 273
   used, for testing Django projects  277, 279
documentation
   code-based reference, adding  223, 225
   testing  221, 222
   verified user guide, writing  226, 229, 231
dummy objects
   using  38, 39, 40
E
End-to-End tests
   about  25, 26
   moving, to functional tests  122, 123, 124
environments
   about  211
   using, for multiple Python versions  213, 215
F
fakes
   dependencies, replacing with  51, 52, 53, 54, 55
fixtures
   generating  156, 157, 158, 159, 160
flaky
   using, to rerun unstable tests  199, 202
functional tests
   about  21, 25, 120
   End-to-End tests, moving to  122, 123, 124
G
Gherkin  172
H
HTTP clients
   testing  247, 251
HTTP
   testing  243, 246
hypothesis  232
I
injector  60
Input/Output (I/O) queues  75
integration tests  22, 24, 26
IO
   testing, with capsys  149
M
mocks
   using  49, 50, 51
multiple test cases
   writing  11, 13
multiple test suite
   working with  125
N
narrow integration tests  122
P
parametric tests
   tests, generating with  160, 161, 162
PEP 333
   reference link  252
performance testing
   about  128, 129, 130
   in cloud  136
   strategies  136
product team
   feedback, obtaining  167, 168
property-based testing  231, 235, 237
PyTest 6  213
PyTest fixtures
   using, for dependency injection  146, 147
   writing  142, 143, 144, 145
pytest-benchmark
   used, for benchmarking  196, 198
pytest-cov
   used, for coverage reporting  189, 192, 193
pytest-testmon
   using, to rerun tests on code changes  202, 204
pytest-xdist
   used, for running tests in parallel  204
PyTest
   unittest, running with  139, 140, 141
   used, for testing Django projects  274, 276
Python 2.7  211
Python 3.7  211
Python 3.8  213
Python versions


---
**Page 312**

[ 312 ]
   testing, with Tox  211, 213
Q
quality control  7
R
Read-Eval-Print Loop (REPL)  69
regression test  105
regression
   preventing  105, 106, 107, 108, 110, 111, 112
reStructuredText format  221
Robot framework
   about  282, 283, 284, 285, 286
   custom keywords, adding  301
   extending  300
   extending, from Python  302, 303, 304, 305
   section headers  282
S
Selenium library
   reference link  286
smoke tests  127, 128
sociable unit  21
software testing  7
solitary unit  21
specifications
   embracing, by example  180, 185, 186
spies
   behaviors, checking with  44, 45, 46, 47, 48, 49
stubs
   components, replacing with  40, 41, 42, 43, 44
subsets of test suite
   running  150, 151
system tests  25
T
test case  9
test cases, test plans
   postconditions  8
   preconditions  8
   steps  8
test doubles  32, 33
test plans  8, 9
test runner  10
test suite, types
   commit tests  126
   compile suite  125
   smoke tests  127, 128
test suite
   about  9, 11
   configuring  153, 154, 155
   End-to-End tests, moving to functional tests  122,
123, 124
   scaling  115, 116, 117, 118, 119, 120, 121, 122
test units  19, 21
Test-Driven Development (TDD)
   about  68, 69, 70, 72, 73, 74, 75, 77, 78, 79,
80, 82, 116
   application, building  3, 83, 84, 85, 86, 87, 88,
89, 90, 91, 93, 94, 95, 96, 97, 98, 100, 101,
102, 103, 104
   chat application, working with  33, 35, 36, 37, 38
test-driven development
   about  15
   implementing  16, 18, 19
test-first approach  18
testing pyramid  27, 28
testing trophy  28, 29
tests
   generating, for common properties  237, 239
   generating, with parametric tests  160, 161, 162
   organizing  13, 15
Then step
   used, for assessing conditions  177
tmp_path
   temporary data, managing with  148
Tox
   about  208, 210
   used, for testing multiple Python versions  211,
213
   using, with Travis  215, 218, 219
Travis application
   reference link  133
Travis
   Tox, using with  215, 217, 219
U
unit tests  15, 26
unittest discovery mode  14


---
**Page 313**

unittest module
   about  10
   running, with PyTest  139, 140, 141
unstable tests
   rerunning, with flaky  199, 202
V
verified user guide
   writing  226, 229, 231
W
web browsers
   testing  297, 298, 299, 300
   testing with  286, 287, 288, 290, 291
   testing, with headless browsers  295, 296
   tests execution, recording  291, 292, 294
Web Server Gateway Interface (WSGI)
   testing, with WebTest  252, 255, 260
WebTest
   using, with web frameworks  261, 262, 265, 269
   WSGI, testing with  252, 255, 259, 261
When step
   used, for performing actions  176


