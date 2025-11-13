# 6.4 Generating tests with parametric tests (pp.160-162)

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


