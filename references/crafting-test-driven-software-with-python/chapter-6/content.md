# Chapter 6: Dynamic and Parametric Tests and Fixtures (pp.152-164)

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


---
**Page 157**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 157 ]
Going even further, we could even write the fixture only once, and dynamically generate it.
Pytest allows us to parameterize fixtures. This means that out of a list of parameters, the
fixture will run multiple times, once for each parameter. This will allow us to write a single
test with a single fixture that injects the right function and the right expectation testing once
for "fizz" and once for "buzz":
def test_output(expected_output, capsys):
    func, expected = expected_output
    func()
    out, _ = capsys.readouterr()
    assert out == expected
The test_output test relies on the expected_output fixture (which we will define
shortly) and the capsys fixture that is provided by pytest itself.
The expected_output fixture will be expected to provide the function that generates the
output we want to test (func) and the output we expect that function to print (expected).
Our expected_output fixture will get the function that generates the expected output
from the fizzbuzz module through a getattr call that is meant to retrieve the outfizz
and outbuzz functions:
import pytest
import fizzbuzz
@pytest.fixture(params=["fizz", "buzz"])
def expected_output(request):
    yield getattr(fizzbuzz, "out{}".format(request.param)), request.param
Thanks to @pytest.fixture(params=["fizz", "buzz"]), the expected_output
fixture will be invoked by pytest twice, once for "fizz" and once for "buzz", leading to
the test running twice, once for each parameter.
Through request.param the fixtures know which one of the two parameters is running,
and using getattr, pytest retrieves from the fizzbuzz module the outfizz and outbuzz
output generation functions and yields to the test the function to be tested and its
associated expected output.


---
**Page 158**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 158 ]
When the parameters are not strings, you can also use the ids argument
to provide a text description for them. This is so that when the tests runs,
you know which parameter is being used.
We have seen how we can drive fixture generation from parameters and thus generate
fixtures based on them, but pytest can go further and allow you to drive the fixture
generation from command-line options.
For example, imagine that you want to be able to test two possible setups: one where the
app prints lowercase strings, and another where it prints uppercase "FIZZ" and "BUZZ".
To do this, we could add to conftest.py a pytest_addoption hook to inject an extra --
upper option in pytest:
def pytest_addoption(parser):
 parser.addoption(
      "--upper", action="store_true",
      help="test for uppercase behavior"
 )
When this option is set, the output functions will be tested for uppercase output.
We need to slightly modify our expected_output fixture to return the right uppercase
string that we need to check against when the --upper option is provided:
@pytest.fixture(params=["fizz", "buzz"])
def expected_output(request):
    text = request.param
    if request.config.getoption("--upper"):
        text = text.upper()
    yield getattr(fizzbuzz, "out{}".format(request.param)), text
Now our tests, by default, will check against the lowercase output when run:
$ pytest -k output
tests/unit/test_output.py::test_output[fizz] PASSED
tests/unit/test_output.py::test_output[buzz] PASSED
But, if we provide --upper, we test against the uppercase output (which obviously makes
our tests fail as the outfizz and outbuzz functions output text in lowercase):
$ pytest --upper -k output
tests/unit/test_output.py::test_output[fizz] FAILED
tests/unit/test_output.py::test_output[buzz] FAILED
========= FAILURES ==========
...


---
**Page 159**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 159 ]
E AssertionError: assert 'fizz' == 'FIZZ'
...
E AssertionError: assert 'buzz' == 'BUZZ'
We have seen how to pass options to fixtures from parameters and the command line, but
what if I want to configure fixtures from the tests themselves? That's possible thanks to
markers. Using pytest.mark, we can add markers to our tests, and obviously, those
markers can be read from the test suite and the fixtures. The most flexible thing about
markers is that markers can have parameters too. So the markers can be used to set
attributes for a specific test that will be visible to the fixture.
For example, we could have the tests be able to force lower/upper case configuration
instead of relying on an external command-line option. The test could add a
pytest.mark.textcase marker to flag whether it wants upper- or lowercase text from
the fixture:
@pytest.mark.textcase("lower")
def test_lowercase_output(expected_output, capsys):
    func, expected = expected_output
    func()
    out, _ = capsys.readouterr()
    assert out == expected
Our test_lowercase_output is a perfect copy of test_output, apart from the added
marker. The marker specifies that the test has to run with lowercase text even when the --
upper option is provided.
To enable such a behavior, we have to modify our expected_output fixture to read the
marker and its arguments. After reading the command-line options, we are going to
retrieve the marker, get its first argument, and lower/upper the text based on it:
@pytest.fixture(params=["fizz", "buzz"])
def expected_output(request):
    text = request.param
    if request.config.getoption("--upper"):
        text = text.upper()
    textcasemarker = request.node.get_closest_marker("textcase")
    if textcasemarker:
        textcase, = textcasemarker.args
        if textcase == "upper":
            text = text.upper()
        elif textcase == "lower":
            text = text.lower()
        else:


---
**Page 160**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 160 ]
            raise ValueError("Invalid Test Marker")
    yield getattr(fizzbuzz, "out{}".format(request.param)), text
Now if we run our test suite, while the test_output function will fail when we provide
the --upper option (because the output functions provide only lowercase output), the
test_lowercase_output test instead will always succeed because the fixture is
configured by the test to only provide lowercase text:
$ pytest --upper -k output
tests/unit/test_output.py::test_output[fizz] FAILED
tests/unit/test_output.py::test_output[buzz] FAILED
tests/unit/test_output.py::test_lowercase_output[fizz] PASSED
tests/unit/test_output.py::test_lowercase_output[buzz] PASSED
We have seen how we can change the behavior of fixtures based on parameters and options
that we provide, and many of those practices work out of the box for changing the behavior
of the tests themselves. Just as fixtures have the params option, tests support the
@pytest.mark.parametrize decorator, which allows generating tests based on
parameters.
Generating tests with parametric tests
Sometimes you find yourself writing the same check over and over for multiple
configurations. Instead, it would be convenient if we could write the test only once and
provide the configurations in a declarative way.
That's exactly what @pytest.mark.parametrize allows us to do: to generate tests based
on a template function and the various configurations that have to be provided.
For example, in our fizzbuzz software, we could have two isbuzz and isfizz checks
that verify whether the provided number should lead us to print the "buzz" or "fizz"
strings. Like always, we want to write a test that drives the implementation of those two
little blocks of our software, and the tests might look like this:
def test_isfizz():
    assert isfizz(1) is False
    assert isfizz(3) is True
    assert isfizz(4) is False
    assert isfizz(6) is True
def test_isbuzz():
    assert isbuzz(1) is False
    assert isbuzz(3) is False


---
**Page 161**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 161 ]
    assert isbuzz(5) is True
    assert isbuzz(6) is False
    assert isbuzz(10) is True
The tests cover a few cases to make us feel confident that our implementation will be
reliable, but it's very inconvenient to write the same check over and over for each possible
number that we want to check.
That's where parameterizing the test comes into the picture. Instead of having the
test_isfizz function be a long list of assertions, we could rewrite it to be a single
assertion that gets rerun by pytest multiple times, once for each parameter it receives. The
parameters could for example be the number to check with isfizz and the expected
outcome, so that we can compare the outcome of invoking isfizz to the expected
outcome:
@pytest.mark.parametrize("n,res", [
    (1, False),
    (3, True),
    (4, False),
    (6, True)
])
def test_isfizz(n, res):
    assert isfizz(n) is res
When we run the test suite, pytest will take care of generating all tests, one for each
parameter, to guarantee we are checking all the conditions as we were doing before:
$ pytest -k checks
tests/unit/test_checks.py::test_isfizz[1-False] PASSED [ 20%]
tests/unit/test_checks.py::test_isfizz[3-True] PASSED [ 40%]
tests/unit/test_checks.py::test_isfizz[4-False] PASSED [ 60%]
tests/unit/test_checks.py::test_isfizz[6-True] PASSED [ 80%]
...
We can even go further and mix a fixture with a parameterized test and have the fixture 
generate one of the parameters. For the isfizz function, we explicitly provided the
expected result; for the isbuzz test, we are going to have the fixture inject whether the
number is divisible by 5 and thus whether it would print buzz or not.
To do so, we are going to provide a divisible_by5 fixture that does no more than to
return whether the number is divisible by 5 or not:
@pytest.fixture(scope="function")
def divisible_by5(n):
    return n % 5 == 0


---
**Page 162**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 162 ]
Then, we can have our parameterized test accept the parameter for the number, but use the
fixture for the expected result, as shown in the following code:
@pytest.mark.parametrize("n", [1, 3, 5, 6, 10])
def test_isbuzz(n, divisible_by5):
    assert isbuzz(n) is divisible_by5
On each one of the generated tests, the number n will be provided to both the test and the
fixture (by virtue of the shared argument name) and our test will be able to confirm that
isbuzz returns True only for numbers divisible by 5:
$ pytest -k checks
...
tests/unit/test_checks.py::test_isbuzz[1] PASSED [ 55%]
tests/unit/test_checks.py::test_isbuzz[3] PASSED [ 66%]
tests/unit/test_checks.py::test_isbuzz[5] PASSED [ 77%]
tests/unit/test_checks.py::test_isbuzz[6] PASSED [ 88%]
tests/unit/test_checks.py::test_isbuzz[10] PASSED [100%]
It is also possible to provide arguments to the test through a fixture by using the indirect
option of parametrize. In such a case, the parameter is provided to the fixture and then
the fixture can decide what to do with it, whether to pass it to the test or change it. This
allows us to replace test parameters, instead of injecting new ones as we did.
Summary
In this chapter, we saw why pytest is considered a very flexible and powerful framework
for writing test suites. Its capabilities to automatically generate tests and fixtures on the fly
and to change their behaviors through hooks and plugins are very helpful, allowing us to
write smaller test suites that cover more cases.
The problem with those techniques is that they make it less clear what's being tested and
how, so it's always a bad idea to abuse them. It's usually better to ensure that your test is
easy to read and clear about what's going on. That way, it can act as a form of
documentation on the behavior of the software and allow other team members to learn
about a new feature by reading its test suite.


---
**Page 163**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 163 ]
Only once all our test suites are written in a simple and easy-to-understand way can we
focus on reducing the complexity of those suites by virtue of parameterization or
dynamically generated behaviors. When dynamically generated behaviors get in the way of
describing the behavior of software clearly, they can make the test suite unmaintainable
and full of effects at a distance (due to the Actions at a distance anti-pattern) that make it
hard to understand why a test fails or passes.
Now that we have seen how to write tests in the most powerful ways, in the next chapter
we will focus on which tests to write. We are going to focus on getting the right fitness
functions for our software to ensure we are actually testing what we care about.


---
**Page 164**

7
Fitness Function with a Contact
Book Application
We have already seen that in test-driven development, it is common to start development
by designing and writing acceptance tests to define what the software should do and then
dive into the details of how to do it with lower-level tests. That frequently is the foundation
of Acceptance Test-Driven Development (ATDD), but more generally, what we are trying
to do is to define a Fitness Function for our whole software. A fitness function is a function
that, given any kind of solution, tells us how good it is; the better the fitness function, the
closer we get to the result.
Even though fitness functions are typically used in genetic programming to select the
solutions that should be moved forward to the next iteration, we can see our acceptance
tests as a big fitness function that takes the whole software as the input and gives us back a
value of how good the software is.
All acceptance tests passed? This is 100% what it was meant to be, while only 50% of
acceptance tests have been passed? That's half-broken... As far as our fitness function really
describes what we wanted, it can save us from shipping the wrong application.
That's why acceptance tests are one of the most important pieces of our test suite and a test
suite comprised solely of unit tests (or, more generally, technical tests) can't really
guarantee that our software is aligned with what the business really wanted. Yes, it might
do what the developer wanted, but not what the business wanted.
In this chapter, we will cover the following topics:
Writing acceptance tests
Using behavior-driven development
Embracing specifications by example


