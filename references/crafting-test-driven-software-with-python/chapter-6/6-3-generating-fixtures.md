# 6.3 Generating fixtures (pp.156-160)

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


