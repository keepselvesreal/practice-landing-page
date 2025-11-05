# 6.2 Configuring the test suite (pp.153-156)

---
**Page 153**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 153 ]
Though the examples have been written using Python 3.7 and pytest 5.4.3, they should
work on most modern Python versions. You can find the code files used in this chapter on
GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-
with-​Python/​tree/​main/​Chapter06
Configuring the test suite
In pytest, there are two primary configuration files that can be used to drive the behavior of
our testing environment:
pytest.ini takes care of configuring pytest itself, so the options we set there
are mostly related to tweaking the behavior of the test runner and discovery.
These options are usually available as command-line options too.
conftest.py is aimed at configuring our tests and test suite, so it's the place
where we can declare new fixtures, attach plugins, and change the way our tests
should behave.
While pytest has grown over the years, with other ways being developed to configure the
behavior of pytest itself or of the test suite, the two aforementioned ways are probably the
most widespread.
For example, for a fizzbuzz project, if we have a test suite with the classical basic
distinction between the source code, unit tests, and functional tests, then we could have a
pytest.ini file within the project directory to drive how pytest should run:
.
├── pytest.ini
├── src
│   ├── fizzbuzz
│   │   ├── __init__.py
│   │   └── __main__.py
│   └── setup.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── functional
    │   └── test_acceptance.py
    └── unit
        ├── test_checks.py
        └── test_output.py


---
**Page 154**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 154 ]
The content of pytest.ini could contain any option that is also available via the
command line, plus a bunch of extra options as described in the pytest reference for INI
options.
For example, to run pytest in verbose mode, without capturing the output and by
disabling deprecation warnings, we could create a pytest.ini file that adds the following
related configuration options:
[pytest]
addopts = -v -s
filterwarnings =
    ignore::DeprecationWarning
In the same way, we have a conftest.py file in the tests directory. We already know
from Chapter 5, Introduction to PyTest, that conftest.py is where we can declare our
fixtures to make them available to the directory and all subdirectories. If set with
autouse=True, the fixtures will also automatically apply to all tests in the same directory.
If we want to print every time we enter and exit a test, for example, we could add a fixture
to our conftest.py file as shown here:
import pytest
@pytest.fixture(scope="function", autouse=True)
def enterexit():
    print("ENTER")
    yield
    print("EXIT")
As conftest is the entry point of our tests, the fixture would become available for all our
tests, and as it is with autouse=True, all of them would start using it. Not only can we use
fixtures that are declared in conftest.py itself, but we can also use fixtures that come
from anything that was imported. We just have to declare the module as a plugin that has
to be loaded when the tests start.
For example, we could have a fizzbuzz.testing package in our fizzbuzz project where
fizzbuzz.testing.fixtures provides a set of convenience fixtures for anyone willing
to test our simple app.
Similarly, we could have a fizzbuzz.testing.fixtures.announce fixture that
announces every test being run:
import pytest
@pytest.fixture(scope="function", autouse=True)


---
**Page 155**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 155 ]
def announce(request):
    print("RUNNING", request.function)
To use it, we just have to add our module to pytest_plugins in the conftest.py file as
follows:
pytest_plugins = ["fizzbuzz.testing.fixtures"]
Note that while conftest.py can be provided multiple times and will
only apply to the package that contains it, pytest_plugins instead
should only be declared in the root conftest.py file, as there is no way
to enable/disable plugins on demand – they are always enabled for the
whole test suite.
But adding fixtures is not all conftest.py can do. Pytest also provides a bunch of hooks
that can be exposed from conftest (or from a plugin declared in pytest_plugins) that
can be used to drive the behavior of the test suite.
The most obvious hooks are pytest_runtest_setup, which is called when preparing to
execute a new test; pytest_runtest_call, called when executing a new test; and
pytest_runtest_teardown, called when finalizing a test.
For example, our previous announce fixture can be rewritten using the
pytest_runtest_setup hook as follows:
def pytest_runtest_setup(item):
    print("Hook announce", item)
Tons of additional hooks are available in pytest, such as a hook for parsing command-line
options, a hook for generating test run reports, a hook for starting or finishing a whole test
run, and so on.
For a complete list of available hooks, refer to the pytest API reference at
https:/​/​docs.​pytest.​org/​en/​stable/​reference.​html#hooks.
We have seen how to change the behavior of our test suite by using configuration options,
conftest, and hooks, but pytest's flexibility doesn't stop there. Not only we can change the
behavior of the test suite itself, but we can also change the behavior of the fixtures by
generating those fixtures on demand.


---
**Page 156**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 156 ]
Generating fixtures
Now that we know that conftest.py allows us to customize how our test suite should
behave, the next step is to notice that pytest allows us to also change how our fixtures
behave as well.
For example, the fizzbuzz program is expected to print "fizz" on every number divisible
by 3, print "buzz" on every number divisible by 5, and print "fizzbuzz" on every
number divisible by both.
To implement this, we could have outfizz and outbuzz functions that print "fizz" or
"buzz" without a newline. This allows us to call each one of them to print fizz or buzz
and to call both functions one after the other to print fizzbuzz.
To test this behavior, we could have a tests/unit/test_output.py module containing
all the tests for our output utilities. For outfizz and outbuzz, we could write the tests as
follows:
from fizzbuzz import outfizz, outbuzz, endnum
def test_outfizz(capsys):
    outfizz()
    out, _ = capsys.readouterr()
    assert out == "fizz"
def test_outbuzz(capsys):
    outbuzz()
    out, _ = capsys.readouterr()
    assert out == "buzz"
These are pretty simple tests that do the same thing, just over a different output. One
invokes the outfizz function and checks whether it prints "fizz" and the other invokes
the outbuzz function and checks whether it prints "buzz".
We could think of having a form of dependency injection oriented toward the test itself,
where the function to test is provided by a fixture. This would allow us to write the test
once and provide two fixtures: one that injects "fizz" and one that injects "buzz".


