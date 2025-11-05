# 5.3.0 Introduction [auto-generated] (pp.142-146)

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


