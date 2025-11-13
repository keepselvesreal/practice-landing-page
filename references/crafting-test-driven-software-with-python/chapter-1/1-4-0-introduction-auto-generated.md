# 1.4.0 Introduction [auto-generated] (pp.15-16)

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


---
**Page 16**

Getting Started with Software Testing
Chapter 1
[ 16 ]
Now that we know how to structure tests properly, we can see how they are helpful in
implementing TDD and how unit tests are usually expressed.
Test-driven development
Tests can do more than just validating our code is doing what we expect. The TDD process
argues that tests are essential in designing code itself.
Writing tests before implementing the code itself forces us to reason about our
requirements. We must explicitly express requirements in a strict, well-defined way –
clearly enough that a computer itself (computers are known for not being very flexible in
understanding things) can understand them and state whether the code you will be writing
next satisfies those requirements.
First, you write a test for your primary scenario—in this case, testing that doing 3+2 does
return 5 as the result:
import unittest
class AdditionTestCase(unittest.TestCase):
    def test_main(self):
        result = addition(3, 2)
        assert result == 5
Then you make sure it fails, which proves you are really testing something:
$ python 03_tdd.py
E
======================================================================
ERROR: test_main (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 5, in test_main
    result = addition(3, 2)
NameError: name 'addition' is not defined
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Finally, you write the real code that is expected to make the test pass:
def addition(arg1, arg2):
    return arg1 + arg2


