# 1.3.1 Multiple test cases (pp.11-13)

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


---
**Page 12**

Getting Started with Software Testing
Chapter 1
[ 12 ]
The discovery phase of unittest.main (the phase during which unittest.main decides
which tests to run) looks for all subclasses or unittest.TestCase.
The same way we had MyTestCase tests executed, adding more test cases is as simple as
declaring more classes:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
    def notatest(self):
        pass
class MySecondTestCase(unittest.TestCase):
    def test_two(self):
        pass
if __name__ == '__main__':
    unittest.main()
Running the 01_automatictests.py module again will lead to both test cases being
verified:
$ python 01_automatictests.py -v
test_two (__main__.MySecondTestCase) ... ok
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.000s
OK
If a test case is particularly complex, it can even be divided into multiple individual tests,
each checking a specific subpart of it:
class MySecondTestCase(unittest.TestCase):
    def test_two(self):
        pass
    def test_two_part2(self):
        pass


---
**Page 13**

Getting Started with Software Testing
Chapter 1
[ 13 ]
This allows us to divide the test cases into smaller pieces and eventually share setup and
teardown code between the individual tests. The individual tests will be executed by the
test runner in alphabetical order, so in this case, test_two will be executed before
test_two_part2:
$ python 01_automatictests.py -v
test_two (__main__.MySecondTestCase) ... ok
test_two_part2 (__main__.MySecondTestCase) ... ok
test_one (__main__.MyTestCase) ... ok
In that run of the tests, we can see that MySecondTestCase was actually executed before
MyTestCase because "MyS" is less than "MyT".
In any case, generally, it's a good idea to consider your tests as being executed in a random
order and to not rely on any specific sequence of execution, because other developers might
add more test cases, add more individual tests to a case, or rename classes, and you want to
allow those changes with no additional issues. Especially since relying on a specific known
execution order of your tests might limit your ability to parallelize your test suite and run
test cases concurrently, which will be required as the size of your test suite grows.
Once more tests are added, adding them all into the same class or file quickly gets
confusing, so it's usually a good idea to start organizing tests.
Organizing tests
If you have more than a few tests, it's generally a good idea to group your test cases into
multiple modules and create a tests directory where you can gather the whole test plan:
├── 02_tests
│   ├── tests_div.py
│   └── tests_sum.py


