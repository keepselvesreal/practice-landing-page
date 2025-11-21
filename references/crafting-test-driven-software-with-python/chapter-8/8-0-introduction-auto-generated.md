# 8.0 Introduction [auto-generated] (pp.188-189)

---
**Page 188**

8
PyTest Essential Plugins
In the previous chapter, we saw how to work with PyTest and pytest-bdd to create
acceptance tests and verify the requirements of our software.
However, pytest-bdd is not the only useful plugin that PyTest has. In this chapter, we are
going to continue working on the contacts project introduced in Chapter 7, Fitness Function
with a Contact Book Application, showing how some of the most commonly used PyTest
plugins can help during the development of a project.
The plugins we are going to cover in this chapter are going to help us with verifying our
test suite coverage of the application code, checking the performance of our application,
dealing with tests that are flaky or unstable, and optimizing our development process by
running only the impacted tests when we change the code base or by speeding up our
whole test suite execution.
In this chapter, we will cover the following topics:
Using pytest-cov for coverage reporting
Using pytest-benchmark for benchmarking
Using flaky to rerun unstable tests
Using pytest-testmon to rerun tests on code changes
Running tests in parallel with pytest-xdist


---
**Page 189**

PyTest Essential Plugins
Chapter 8
[ 189 ]
Technical requirements
We need a working Python interpreter with the PyTest framework installed with the
pytest-bdd plugin. PyTest and pytest-bdd can be installed with the following command:
$ pip install pytest pytest-bdd
For each section, you will need to install the plugin discussed in the section itself. You can
install all of them at once:
$ pip install pytest-cov pytest-benchmark flaky pytest-testmon pytest-xdist
The examples have been written on Python 3.7 with PyTest 6.0.2 and pytest-bdd 4.0.1, but
should work on most modern Python versions. The versions of the plugins in use for each
section instead are pytest-cov 2.10, pytest-benchmark 2.3.2, flaky 3.7.0, pytest-testmon 1.0.3,
and pytest-xdist 2.1.0.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter08.
Using pytest-cov for coverage reporting
We have already seen in Chapter 1, Getting Started with Software Testing, how code
coverage by tests is a good measure for establishing how confident you can be in your test
suite. A test suite that only runs 10% of all our code is probably not going to be very reliable
in finding problems, as most of the code will go unchecked. A test suite that instead verifies
100% of our code is certainly going to exercise every single line of code we wrote and so
should trigger bugs more easily if there are any.
Obviously, coverage cannot verify code that you never wrote, so it's not going to detect that
you have a bug because you forgot to add an if check in your method, but at least it tells
you if you forgot to write a test for that method.
Normally, test coverage in Python is done using the coverage module, which can be
installed from PyPI, but PyTest has a convenient pytest-cov plugin that is going to do
that for us and make our life simpler when we want to check the coverage of our tests. Like
any other Python distribution, we can install pytest-cov through pip:
$ pip install pytest-cov


