# 1.3.2 Organizing tests (pp.13-15)

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


---
**Page 14**

Getting Started with Software Testing
Chapter 1
[ 14 ]
Those tests can be executed through the unittest discover mode, which will look for all
modules with names matching test*.py within a target directory and will run all the
contained test cases:
$ python -m unittest discover 02_tests -v
test_div0 (tests_div.TestDiv) ... ok
test_div1 (tests_div.TestDiv) ... ok
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok
----------------------------------------------------------------------
Ran 4 tests in 0.000s
OK
You can even pick which tests to run by filtering them with a substring with the -k
parameter; for example, -k sum will only run tests that contain "sum" in their names:
$ python -m unittest discover 02_tests -k sum -v
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.000s
OK
And yes, you can nest tests further as long as you use Python packages:
├── 02_tests
│   ├── tests_div
│   │   ├── __init__.py
│   │   └── tests_div.py
│   └── tests_sum.py
Running tests structured like the previous directory tree will properly navigate into the
subfolders and spot the nested tests.
So running unittest in discovery mode over that direction will properly find the
TestDiv and TestSum classes declared inside the files even when they are nested in
subdirectories:
$ python -m unittest discover 02_tests -v
test_div0 (tests_div.tests_div.TestDiv) ... ok
test_div1 (tests_div.tests_div.TestDiv) ... ok
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok


---
**Page 15**

Getting Started with Software Testing
Chapter 1
[ 15 ]
----------------------------------------------------------------------
Ran 4 tests in 0.000s
OK
Now that we know how to write tests, run them, and organize multiple tests in a test suite.
We can start introducing the concept of TDD and how unit tests allow us to achieve it.
Introducing test-driven development and
unit tests
Our tests in the previous section were all empty. The purpose was to showcase how a test
suite can be made, executed, and organized in test cases and individual tests, but in the
end, our tests did not test much.
Most individual tests are written following the "Arrange, Act, Assert" pattern:
First, prepare any state you will need to perform the action you want to try.
Then perform that action.
Finally, verify the consequences of the action are those that you expected.
Generally speaking, in most cases, the action you are going to test is "calling a function,"
and for code that doesn't depend on any shared state, the state is usually all contained
within the function arguments, so the Arrange phase might be omitted. Finally, the Assert
phase will verify that the called function did what you expected, which usually means
verifying the returned value and any effect at a distance that function might have:
import unittest
class SomeTestCase(unittest.TestCase):
    def test_something(self):
        # Arrange phase, nothing to prepare here.
        # Act phase, call do_something
        result = do_something()
        # Assert phase, verify do_something did what we expect.
        assert result == "did something"
The test_something test is structured as a typical test with those three phases explicitly
exposed, with the do_something call representing the Act phase and the final assert
statement representing the Assertion phase.


