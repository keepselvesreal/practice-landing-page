# 12.4.1 Adding custom keywords (pp.301-302)

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


