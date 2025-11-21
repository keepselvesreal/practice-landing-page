# 5.3.1 Using fixtures for dependency injection (pp.146-148)

---
**Page 146**

Introduction to PyTest
Chapter 5
[ 146 ]
Using fixtures for dependency injection
Another good property of pytest fixtures is that they can also provide some kind of
dependency injection management. For example, your software might use a remote
random number generator. Whenever a new random number is needed, an HTTP request
to a remote service is made that will return the number.
 Inside our conftest.py file, we could provide a fixture that builds a fake random number
generator that by default is going to generate random numbers (to test the software still
works when the provided values are random) but without doing any remote calls to ensure
the test suite is able to run quickly:
$ cat conftest.py
import pytest
@pytest.fixture
def random_number_generator():
    import random
    def _number_provider():
        return random.choice(range(10))
    yield _number_provider
Then, we could have any number of tests that use our random number generator (for the
sake of simplicity, we are going to make a test_randomness.py file with a single test
using it):
def test_something(random_number_generator):
    a = random_number_generator()
    b = 10
    assert a + b >= 10
If a test has an argument, pytest will automatically consider that dependency injection
and will invoke the fixture with the same name of the argument to provide the object that
should satisfy that dependency.
So, for our test_something function, the random_number_generator object is the one
returned by our random_number_generator fixture, which returns numbers from 0 to 9.


---
**Page 147**

Introduction to PyTest
Chapter 5
[ 147 ]
As fixtures can be overridden inside modules or packages, if for some of our tests we
wanted to replace the random number generator with a fairly predictable one (that always
returns 1, all we would have to do is, again, declare a fixture with the same exact name
inside the other module. Let's look at an example:
We would make a test_fixturesinj.py test module where we provide a new
1.
random_number_generator that is not random at all and we have a test that
relies on that feature:
def test_something(random_number_generator):
    a = random_number_generator()
    b = 10
    assert a + b == 11
@pytest.fixture
def random_number_generator():
    def _number_provider():
        return 1
    yield _number_provider
If we run our two test_something tests, from the two modules, they will both
2.
pass, because one will be using a random number generator that builds random
numbers, while the other will use one that always returns the number 1:
$ pytest -v -k "something and not simple"
...
collected 7 items / 5 deselected / 2 selected
test_fixturesinj.py::test_something PASSED [ 50%]
test_randomness.py::test_something PASSED [100%]
...
So we saw that pytest fixtures are much more flexible than unittest ones and that due
to that greater decoupling and flexibility, great care has to be put into making sure it's clear
which fixture implementations we end up using in our tests.


---
**Page 148**

Introduction to PyTest
Chapter 5
[ 148 ]
In the upcoming sections, we are going to look at some of the built-in fixtures that pytest
provides and that are generally useful during the development of a test suite.
Managing temporary data with tmp_path
Many applications need to write data to disk. Surely we don't want data written during
tests to interfere with the data we read/write during the real program execution. Data
fixtures used in tests usually have to be predictable and we certainly don't want to corrupt
real data when we run our tests.
So it's common for a test suite to have its own read/write path where all the data is written.
If we decided the path beforehand, by the way, there would be the risk that different test
runs would read previous data and thus might not spot bugs or might fail without a
reason.
For this reason, one of the fixtures that pytest provides out of the box is tmp_path, which,
when injected into a test, provides a temporary path that is always different on every test
run. Also, it will take care of retaining the most recent temporary directories (for debugging
purposes) while deleting the oldest ones:
def test_tmp(tmp_path):
    f = tmp_path / "file.txt"
    print("FILE: ", f)
    f.write_text("Hello World")
    fread = tmp_path / "file.txt"
    assert fread.read_text() == "Hello World"
The test_tmp test creates a file.txt file in the temporary directory and writes "Hello
World" in it. Once the write is completed, it tries to access the same file again and confirm
that the expected content was written.
The tmp_path argument will be injected by pytest itself and will point to a path made by
pytest for that specific test run.
This can be seen by running our test with the -s option, which will make the "FILE: ..."
string that we printed visible:
$ pytest test_tmppath.py -v -s
===== test session starts =====
...
collected 1 item


