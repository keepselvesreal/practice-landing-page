# 1.4.1 Test-driven development (pp.16-19)

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


---
**Page 17**

Getting Started with Software Testing
Chapter 1
[ 17 ]
And confirm it makes your test pass:
$ python 03_tdd.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
Once the test is done and it passes, we can revise our implementation and refactor the code.
If the test still passes, it means we haven't changed the behavior and we are still doing what
we wanted.
For example, we can change our addition function to unpack arguments instead of having
to specify the two arguments it can receive:
def addition(*args):
    a1, a2 = args
    return a1 + a2
If our test still passes, it means we haven't changed the behavior, and it's still as good as
before from that point of view:
$ python 03_tdd.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
Test-driven development is silent about when you reach a robust code base that satisfies all
your needs. Obviously, you should at least make sure there are enough tests to cover all
your requirements.
But as testing guides us in the process of development, development should guide us in the
process of testing.
Looking at the code helps us come up with more white-box tests; tests that we can think of
because we know how the code works internally. And while those tests might not
guarantee that we are satisfying more requirements, they help us guarantee that our code
is robust in most conditions, including corner cases.


---
**Page 18**

Getting Started with Software Testing
Chapter 1
[ 18 ]
While historically, test-first and test-driven were synonyms, today that's considered the one
major difference with the test-first approach. In TDD we don't have the expectation to be
able to write all tests first. Nor is it generally a good idea in the context of extreme
programming practices, because you still don't know what the resulting interface that you
want to test will be. What you want to test evolves as the code evolves, and we know that
the code will evolve after every passing test, as a passing test gives us a chance for
refactoring.
In our prior example, as we changed our addition function to accept a variable number of
arguments, a reasonable question would be, "But what happens if I pass three arguments? Or
none?" And our requirements, expressed by the tests, as a consequence, have to grow to
support a variable number of arguments:
    def test_threeargs(self):
        result = addition(3, 2, 1)
        assert result == 6
    def test_noargs(self):
        result = addition()
        assert result == 0
So, writing code helped us come up with more tests to verify the conditions that came to
mind when looking at the code like a white box:
$ python 03_tdd.py
.EE
======================================================================
ERROR: test_noargs (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 13, in test_noargs
    result = addition()
  File "03_tdd.py", line 18, in addition
    a1, a2 = args
ValueError: not enough values to unpack (expected 2, got 0)
======================================================================
ERROR: test_threeargs (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 9, in test_threeargs
    result = addition(3, 2, 1)
  File "03_tdd.py", line 18, in addition
    a1, a2 = args
ValueError: too many values to unpack (expected 2)


---
**Page 19**

Getting Started with Software Testing
Chapter 1
[ 19 ]
----------------------------------------------------------------------
Ran 3 tests in 0.001s
FAILED (errors=2)
And adding those failing tests helps us come up with more, and better, code that now
properly handles the cases where any number of arguments is passed to our addition
function:
def addition(*args):
    total = 0
    for a in args:
        total += a
    return total
Our addition function will now just iterate over the provided arguments, adding them to
the total. Thus if no argument is provided, it will just return 0 because nothing was added
to it.
If we run our test suite again, we will be able to confirm that both our new tests now pass,
and thus we achieved what we wanted to:
$ python 03_tdd.py
...
----------------------------------------------------------------------
Ran 3 test in 0.001s
OK
Writing tests and writing code should interleave continuously. If you find yourself
spending all your time on one or the other, you are probably moving away from the
benefits that TDD can give you, as the two phases are meant to support each other.
There are many kinds of tests you are going to write in your test suite during your
development practice, but the most common one is probably going to be test units.
Test units
The immediate question once we know how to arrange our tests, is usually "what should I
test?". The answer to that is usually "it depends."


