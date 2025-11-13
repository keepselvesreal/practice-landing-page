# Chapter 5: Introduction to PyTest (pp.138-152)

---
**Page 138**

5
Introduction to PyTest
In the previous chapters, we saw how to approach test-driven development, how to create
a test suite with the unittest module, and how to organize it as it grows. While unittest
is a very good tool and is a reliable solution for most projects, it lacks some convenient
features that are available in more advanced testing frameworks.
PyTest is currently the most widespread testing framework in the Python community, and
it's mostly compatible with unittest. So it's easy to migrate from unittest to pytest if
you feel the need for the convenience that pytest provides.
In this chapter, we will cover the following topics:
Running tests with PyTest
Writing PyTest fixtures
Managing temporary data with tmp_path
Testing I/O with capsys
Running subsets of the test suite
Technical requirements
We need a working Python interpreter with the pytest framework installed. Pytest can be
installed with the following:
$ pip install pytest
The examples have been written on Python 3.7 and pytest 5.4.3 but should work on most
modern Python versions. You can find the code files present in this chapter on GitHub
at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-
Python/​tree/​main/​Chapter05.


---
**Page 139**

Introduction to PyTest
Chapter 5
[ 139 ]
Running tests with PyTest
PyTest is mostly compatible with the unittest module (apart from support for subtests).
Test suites written with unittest can be directly run under pytest with no modification
usually. For example, our chat application test suite can be directly run under pytest by
simply invoking pytest within the project directory:
$ pytest -v
============ test session starts ============
platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /chatapp
collected 11 items
benchmarks/test_chat.py::BenchmarkChat::test_sending_messages PASSED [ 9%]
tests/e2e/test_chat.py::TestChatAcceptance::test_message_exchange PASSED [
18%]
tests/e2e/test_chat.py::TestChatAcceptance::test_smoke_sending_message
PASSED [ 27%]
tests/functional/test_chat.py::TestChatMessageExchange::test_exchange_with_
server PASSED [ 36%]
tests/functional/test_chat.py::TestChatMessageExchange::test_many_users
PASSED [ 45%]
tests/functional/test_chat.py::TestChatMessageExchange::test_multiple_reade
rs PASSED [ 54%]
tests/unit/test_client.py::TestChatClient::test_client_connection PASSED [
63%]
tests/unit/test_client.py::TestChatClient::test_client_fetch_messages
PASSED [ 72%]
tests/unit/test_client.py::TestChatClient::test_nickname PASSED [ 81%]
tests/unit/test_client.py::TestChatClient::test_send_message PASSED [ 90%]
tests/unit/test_connection.py::TestConnection::test_broadcast PASSED [100%]
============ 11 passed in 3.63s ============
The main difference is that pytest doesn't look for classes that inherit the
unittest.TestCase class, but instead looks for anything that has test in the name, be it a
module, a class, or a function. Anything named [Tt]est* is a test... but, if needed, it's
possible to change the discovery rules by having pytest.ini inside the project directory.
This means that even a simple function can be a test as long as it's named
test_something, and as it won't inherit from TestCase, there is no need to use the
custom self.assertEqual and the related method to get meaningful information on
failed assertions. Pytest will enhance the assert statement to report as much information
as available on the asserted expression.


---
**Page 140**

Introduction to PyTest
Chapter 5
[ 140 ]
For example, we could create a very simple test suite that only has a test_simple.py
module containing a test_something function. That would be all we need to start a test
suite:
def test_something():
    a = 5
    b = 10
    assert a + b == 11
Now, if we run pytest inside the same directory, it will properly find and run our test, and
the failed assertion will also give us hints on what went wrong by telling us that a + b is
15 and not 11:
$ pytest -v
======================= test session starts =======================
platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: ~/HandsOnTestDrivenDevelopmentPython/05_pytest
collected 1 item
test_simple.py::test_something FAILED [100%]
============================ FAILURES =============================
_________________________ test_something __________________________
    def test_something():
        a = 5
        b = 10
> assert a + b == 11
E assert 15 == 11
E +15
E -11
test_simple.py:4: AssertionError
===================== short test summary info =====================
FAILED test_simple.py::test_something - assert 15 == 11
======================== 1 failed in 0.22s ========================
We can also add more complex tests that are implemented as classes collecting multiple
tests, without having to inherit from the TestCase class as we did for unittest test suites:
class TestMultiple:
    def test_first(self):
        assert 5 == 5
    def test_second(self):
        assert 10 == 10


---
**Page 141**

Introduction to PyTest
Chapter 5
[ 141 ]
As for the previous case where we only had the test_something test function, if we run
pytest, it will find all three tests and it will run them:
$ pytest -v
...
collected 3 items
test_simple.py::test_something FAILED [ 33%]
test_simple.py::TestMultiple::test_first PASSED [ 66%]
test_simple.py::TestMultiple::test_second PASSED [100%]
...
As we know that test_something always fails, we can select which tests to run by using
the -k option, as we used to do for unittest. The option is, by the way, more powerful
than the one provided by unittest.
For example, it is possible to provide the -k option to restrict the tests to a subset of them
like we already used to do:
$ pytest -v -k first
...
collected 3 items / 2 deselected / 1 selected
test_simple.py::TestMultiple::test_first PASSED [100%]
...
It's also possible to use it to exclude some specific tests:
$ pytest -v -k "not something"
...
collected 3 items / 1 deselected / 2 selected
test_simple.py::TestMultiple::test_first PASSED [ 50%]
test_simple.py::TestMultiple::test_second PASSED [100%]
...
In the first case, we ran the test_first test, but in the second, we ran all tests except
for test_something. So you could view pytest as unittest on steroids. It provides the
same features you were used to with unittest, but frequently, they are enhanced to make
them more powerful, flexible, or convenient.
If one had to choose between the two, it'd probably be a matter of preference. But it's not
uncommon to see unittest used for projects that want to keep a more lightweight test
suite that is kept stable over the course of the years (unittest, like most modules of the
Python Standard Library guarantees very long-term compatibility) and pytest for projects
that have more complex test suites or needs.


---
**Page 142**

Introduction to PyTest
Chapter 5
[ 142 ]
Writing PyTest fixtures
The primary difference between unittest and PyTest lies in how they handle fixtures.
While unittest like fixtures (setUp, tearDown, setupClass, and so on) are still
supported through the TestCase class when using pytest, pytest tries to provide
further decoupling of tests from fixtures.
In pytest, a fixture can be declared using the pytest.fixture decorator. Any function
decorated with the decorator becomes a fixture:
@pytest.fixture
def greetings():
    print("HELLO!")
    yield
    print("GOODBYE")
The code of the test is executed where we see the yield statement. yield in this context
passes execution to the test itself. So this fixture would print "HELLO" before the test starts
and then "GOODBYE" when the test finishes.
To then bind a fixture to a test, the pytest.mark.usefixtures decorator is used. So, for
example, to use our new fixture with the existing TestMultiple.test_second test, we
would have to decorate that test using the name of our new fixture:
class TestMultiple:
    def test_first(self):
        assert 5 == 5
    @pytest.mark.usefixtures("greetings")
    def test_second(self):
        assert 10 == 10
The name of a fixture is inherited by the name of the function that implements it, so by
passing "greetings" to the usefixtures decorator, we end up using our own fixture:
$ pytest -v -k "usingfixtures and second" -s
...
collected 8 items / 7 deselected / 1 selected
test_usingfixtures.py::TestMultiple::test_second HELLO!
PASSED
GOODBYE
...


---
**Page 143**

Introduction to PyTest
Chapter 5
[ 143 ]
So, the part of the fixture before the yield statement replaces the TestCase.setUp
method, while the part after yield replaces the TestCase.tearDown method.
If we want to use more than one fixture in a test, the usefixtures decorator allows us to
pass multiple arguments, one for each fixture that we want to use.
If you are wondering about the -s option, that's another difference with unittest. By
default, pytest captures all output that your code prints, while unittest, by default, didn't.
The two work in a reverse way, so in the case of pytest, we need to explicitly disable
output capturing to be able to see our prints.
Otherwise, outputs are only shown if the test fails. This has the benefit of keeping test run
output cleaner, but can leave people puzzled the first time they see it.
Pytest fixtures can be declared in the same module that uses them, or inside a
conftest.py module that will be inherited by all modules and packages in the same
directory (or subdirectories).
Think of conftest.py as being a bit like the __init__.py of test packages; it allows us to
customize tests' behavior for that package and even replace fixtures or plugins.
While the pytest fixtures mechanism is very powerful, it's usually a bad
idea to put fixtures too far away from what uses them.
It will make it hard for tests reader to understand what's going on, so
spreading tens of conftest.py files around the test suite is usually a
good way to make life hard for anyone having to understand our test
suite.
As one of the primary goals of tests is to act as references of the software
behavior, it's usually a good idea to keep them straightforward so that
anyone approaching software for the first time can learn about the
software without first having to spend days trying to understand how the
test suite works and what it does.
Obviously, pytest fixtures are not limited to functions; they can also provide a
replacement for TestCase.setUpClass and TestCase.tearDownClass. To do so, all we
have to do is to declare a fixture that has scope="class" ("function", "module",
"package", and "session" scopes are available too to define the life cycle of a fixture):
@pytest.fixture(scope="class")
def provide_current_time(request):
    import datetime


---
**Page 144**

Introduction to PyTest
Chapter 5
[ 144 ]
    request.cls.now = datetime.datetime.utcnow()
    print("ENTER CLS")
    yield
    print("EXIT CLS")
In the previous fixture, we provide a self.now attribute in the class where the test lives,
we print "ENTER CLS" before starting the tests for that class, and then we print "EXIT
CLS" once all tests for that class have finished.
If we want to use the fixture, we just have to decorate a class with mark.usefixtures and
declare we want it:
@pytest.mark.usefixtures("provide_current_time")
class TestMultiple:
    def test_first(self):
        print("RUNNING AT", self.now)
        assert 5 == 5
    @pytest.mark.usefixtures("greetings")
    def test_second(self):
        assert 10 == 10
Now, if we run our tests, we will get the messages from both the provide_current_time
fixture and from the greetings one:
$ pytest -v -k "usingfixtures" -s
collected 8 items / 6 deselected / 2 selected
test_usingfixtures.py::TestMultiple::test_first
ENTER CLS
RUNNING AT 2020-06-17 22:28:23.489433
PASSED
test_usingfixtures.py::TestMultiple::test_second
HELLO!
PASSED
GOODBYE
EXIT CLS
You can also see that our test properly printed the self.now attribute, which was injected
into the class by the fixture. The request argument to fixtures represents a request for that
fixture from a test. It provides some convenient attributes, such as the class that requested
the fixture (cls), the instance of that class that is being used to run the test, the module
where the test is contained, the tests run session, and many more, allowing us not only to
know the context of where our fixture is being used but also to modify those entities.


---
**Page 145**

Introduction to PyTest
Chapter 5
[ 145 ]
Apart from setting up tests, classes, and modules, there is usually a set of operations that
we might want to do for the whole test suite; for example, configuring pieces of our
software that we are going to need in all tests.
For that purpose, we can create a conftest.py file inside our test suite, and drop all those
fixtures there. They just need to be declared with scope="session", and the
autouse=True option can automatically enable them for all our tests:
import pytest
@pytest.fixture(scope="session", autouse=True)
def setupsuite():
    print("STARTING TESTS")
    yield
    print("FINISHED TESTS")
Now, running all our tests will be wrapped by the setupsuite fixture, which can take care
of setting up and tearing down our test suite:
$ pytest -v -s
...
test_usingfixtures.py::TestMultiple::test_first
STARTING TESTS
ENTER CLS
RUNNING AT 2020-06-17 22:29:46.108487
PASSED
test_usingfixtures.py::TestMultiple::test_second
HELLO!
PASSED
GOODBYE
EXIT CLS
FINISHED TESTS
...
We can see from the output of the command that, according to our new fixture, the tests
printed "STARTING TESTS" when they started and printed "FINISHED TESTS" at the end
of the whole suite execution. This means that we can use session-wide fixtures to prepare
and tear down resources or configurations that are necessary for the whole suite to run.


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


---
**Page 149**

Introduction to PyTest
Chapter 5
[ 149 ]
test_tmppath.py::test_tmp
FILE: /tmp/pytest-of-amol/pytest-3/test_tmp0/file.txt
PASSED
===== 1 passed in 0.03s =====
On every new run, the pytest-3 directory will be increased, so the most recent directory
will be from the most recent run and only the latest three directories will be kept.
Testing I/O with capsys
When we implemented the test suite for the TODO list application, we had to check that the
output provided by the application was the expected one. That meant that we provided a
fake implementation of the standard output, which allowed us to see what the application
was going to write.
Suppose you have a very simple app that prints something when started:
def myapp():
    print("MyApp Started")
If we wanted to test that the app actually prints what we expect when started, we could use
the capsys fixture to access the capture output from sys.stdout and sys.stderr of our
application:
def test_capsys(capsys):
    myapp()
    out, err = capsys.readouterr()
    assert out == "MyApp Started\n"
The test_capsys test just starts the application (running myapp), then through
capsys.readouterr() it retrieves the content of sys.stdout and sys.stderr
snapshotted at that moment. 
Once the standard output content is available, it can be compared to the expected one to
confirm that the application actually printed what we wanted. If the application really
printed "MyApp Started" as expected, running the test should pass and confirm that's the
content of the standard output:
$ pytest test_capsys.py -v
===== test session starts =====
...
collected 1 item


---
**Page 150**

Introduction to PyTest
Chapter 5
[ 150 ]
test_capsys.py::test_capsys PASSED
===== 1 passed in 0.03s =====
The passing test run confirms that the capsys plugin worked correctly and our test was
able to intercept the output sent by the function under test.
Running subsets of the testsuite
In the previous chapters, we saw how to divide our test suite into subsets that we can run
on demand based on their purpose and cost. The way to do so involved dividing the tests
by directory or by name, such that we could point the test runner to a specific directory or
filter for test names with the -k option.
While those strategies are available on pytest too, pytest provides more ways to
organize and divide tests; one of them being markers.
Instead of naming all our smoke tests "test_smoke_something", for example, we could
just name the test "test_something" and mark it as a smoke test. Or, we could mark slow
tests, so that we can avoid running slow ones during the most frequent runs.
Marking a test is as easy as decorating it with @pytest.mark.marker, where marker is
our custom label. For example, we could create two tests and use @pytest.mark.first to
mark the first of the two tests:
import pytest
@pytest.mark.first
def test_one():
    assert True
def test_two():
    assert True
At this point, we could select which tests to run by using pytest -m first or pytest -m
"not first":
$ pytest test_markers.py -v
...
test_markers.py::test_one PASSED [ 50%]
test_markers.py::test_two PASSED [100%]


---
**Page 151**

Introduction to PyTest
Chapter 5
[ 151 ]
pytest test_markers.py -m "first" would run only the one marked with our
custom marker:
$ pytest test_markers.py -v -m first
...
test_markers.py::test_one PASSED [100%]
This means that we can mark our tests in any way we want and run selected groups of tests
independently from the directory where they sit or how they are named.
On some versions of pytest, you might get a warning when using custom markers:
Unknown pytest.mark.first - is this a typo?  You can register custom marks
to avoid this warning
This means that the marker is unknown to pytest and must be registered in the list of
available markers to make the warning go away. The reason for this is to prevent typos that
would slip by unnoticed if markers didn't have to be registered. 
To make a marker available and make the warning disappear, the custom markers can be
set in the pytest.ini configuration file for your test suite:
[pytest]
markers =
    first: mark a test as the first one written.
If the configuration file is properly recognized and we have no typos in the "first"
marker, the previously mentioned warning will go away and we will be able to use the
"first" marker freely.
Summary
In this chapter, we saw how pytest can provide more advanced features on top of the
same functionalities we were already used to with unittest. We also saw how we can run
our existing test suite with pytest and how we can evolve it to leverage some of built-in
pytest features.
We've looked at some of the features that pytest provides out of the box, and in the next
chapter, we will introduce more advanced pytest features, such as parametric tests and
fixture generation.


---
**Page 152**

6
Dynamic and Parametric Tests
and Fixtures
In the previous chapter, we saw how pytest can be used to run our test suites, and how it
provides some more advanced features that are unavailable in unittest by default.
Python has seen multiple frameworks and libraries built on top of unittest to extend it
with various features and utilities, but pytest has surely become the most widespread
testing framework in the Python community. One of the reasons why pytest became so
popular is its flexibility and support for dynamic behaviors. Apart from this, generating
tests and fixtures dynamically or heavily changing test suite behavior are other features
supported by pytest out of the box.
In this chapter, we are going to see how to configure a test suite and generate dynamic
fixtures and dynamic or parametric tests. As your test suite grows, it will be important to be
able to know which options PyTest provides to drive the test suite execution and how we
can generate fixtures and tests dynamically instead of rewriting them over and over.
In this chapter, we will cover the following topics:
Configuring the test suite
Generating fixtures
Generating tests with parametric tests
Technical requirements
We need a working Python interpreter with the pytest framework installed. Pytest can be
installed using the following command:
$ pip install pytest


