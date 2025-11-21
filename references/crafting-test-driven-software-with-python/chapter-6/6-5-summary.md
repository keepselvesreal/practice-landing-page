# 6.5 Summary (pp.162-164)

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


