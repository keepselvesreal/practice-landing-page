# 12.2 Introducing the Robot Framework (pp.282-286)

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


