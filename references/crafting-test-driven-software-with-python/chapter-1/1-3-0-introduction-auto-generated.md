# 1.3.0 Introduction [auto-generated] (pp.9-11)

---
**Page 9**

Getting Started with Software Testing
Chapter 1
[ 9 ]
If you think about modern release cycles, we are now used to getting a new version of our
favorite mobile application weekly. Such applications are probably so complex that they
involve thousands of test cases. If all those cases had to be performed by a human, there
would be no way for the company to provide you with frequent releases.
The worst thing you can do, by the way, is to release a broken product. Your users will lose
confidence and will switch to other more reliable competitors if they can't get their job done
due to crashes or bugs. So how can we deliver such frequent releases without reducing our
test coverage and thus incurring more bugs?
The solution came from automating the test process. So while we learned how to detect
defects by writing and executing test plans, it's only by making them automatic that we can
scale them to the number of cases that will ensure robust software in the long term.
Instead of having humans test software, have some other software test it. What a person
does in seconds can happen in milliseconds with software and you can run thousands of
tests in a few minutes.
Introducing automatic tests and test suites
Automated testing is, in practice, the art of writing another piece of software to test an
original piece of software.
As testing a whole piece of software has to take millions of variables and possible code
paths into account, a single program trying to test another one would be very complex and
hard to maintain. For this reason, it's usually convenient to split that program into smaller
isolated programs, each being a test case.
Each test case contains all the instructions that are required to set up the target software in a
state where the parts that are the test case areas of interest can be tested, the tests can be
done, and all the conditions can be verified and reset back to the state of the target software
so a subsequent test case can find a known state from which to start.
When using the unittest module that comes with the Python Standard Library, each test
case is declared by subclassing from the unittest.TestCase class and adding a method
whose name starts with test, which will contain the test itself:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass


---
**Page 10**

Getting Started with Software Testing
Chapter 1
[ 10 ]
Trying to run our previous test will do nothing by the way:
$ python 01_automatictests.py
$
We declared our test case, but we have nothing that runs it.
As for manually executed tests, the automatic tests need someone in charge of gathering all
test cases and running them all. That's the role of a test runner.
Test runners usually involve a discovery phase (during which they detect all test cases) and
a run phase (during which they run the discovered tests).
The unittest module provides all the components necessary to build a test runner that does
both the discovery and execution of tests. For convenience, it even provides the
unittest.main() method, which configures a test runner that, by default, will run the
tests in the current module:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
if __name__ == '__main__':
    unittest.main()
By adding a call to unittest.main() at the end of our tests, Python will automatically
execute our tests when the module is invoked:
$ python 01_automatictests.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
We can confirm that the test we cared about was executed by using the -v option to print a
more verbose output:
$ python 01_automatictests.py -v
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK


---
**Page 11**

Getting Started with Software Testing
Chapter 1
[ 11 ]
During the discovery phase, unittest.main will look for all classes that inherit from
unittest.TestCase within the module that is recognized as the main Python module
(sys.modules['__main__']), and all those subclasses will be registered as test cases for
the runner.
Individual tests are then defined by having methods with names starting with test in the
test case classes. This means that if we add more methods with names that don't start with
test, they won't be treated as tests:
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
    def notatest(self):
        pass
Trying to start the test runner again will continue to run only the test_one test:
$ python 01_automatictests.py -v
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
In the previous example, only the test_one method was executed as a test, while
notatest was recognized as not being a test but instead as a method that we are going to
use ourselves in tests.
Being able to distinguish between tests (methods whose names start with test_) and other 
methods allows us to create helpers and utility methods within our test cases that the
individual tests can reuse.
Given that a test suite is a collection of multiple test cases, to grow our test suite, we need to
be able to actually write more than one single TestCase subclass and run its tests.
Multiple test cases
We already know that unittest.main is the function in charge of executing our test suite,
but how can we make it execute more than one TestCase?


