# 12.4.2 Extending Robot from Python (pp.302-305)

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


