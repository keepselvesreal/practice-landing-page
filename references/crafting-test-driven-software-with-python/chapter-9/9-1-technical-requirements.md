# 9.1 Technical requirements (pp.207-208)

---
**Page 207**

9
Managing Test Environments
with Tox
In the previous chapter, we covered the most frequently used PyTest plugins. Through
them, we are able to manage our test suite within a Python environment. We can configure
how the test suite should work, as well as enable coverage reporting, benchmarking, and
many more features that make it convenient to work with our tests. But what we can't do is
manage the Python environment itself within which the test suite runs.
Tox was invented precisely for that purpose; managing Python versions and the
environment that we need to run our tests. Tox takes care of setting up the libraries and
frameworks we need for our test suite to run and will check our tests on all Python versions
that are available.
In this chapter, we will cover the following topics:
Introducing Tox
Testing multiple Python versions with Tox
Using Tox with Travis
Technical requirements
We need a working Python interpreter along with Tox. Tox can be installed with the
following command:
$ pip install tox
Even though we are going to use the same test suite and contacts app we wrote in Chapter
8, PyTest Essential Plugins, we only need to install Tox 3.20.0. All other dependencies will be
managed by Tox for us.


---
**Page 208**

Managing Test Environments with Tox
Chapter 9
[ 208 ]
You can find the code files present in this chapter on GitHub at
https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python/tr
ee/main/Chapter09.
Introducing Tox
Tox is a virtual environment manager for Python. It takes care of creating the environments
and installing our project and all its dependencies on multiple Python versions.
It is a convenient tool that can automate the setup of our project environment and abstract
it in a way that we can reuse the same command both locally and in our Continuous
Integration (CI) pipeline to set up our project and run its tests. It also does that on multiple
Python versions at the same time, so that we can check that our project works on all of
them.
Testing multiple Python versions can be very convenient when you need to upgrade from
one version to the next. Before switching all your systems to the new one, you want to
ensure that your code is still able to work on both the old and new versions, so that you can
perform a phased rollout.
If we take our contacts application example from Chapter 8, PyTest Essential Plugins, the
test suite required many dependencies to run. We needed flaky to manage flaky tests,
pytest-benchmark for the benchmarks suite, pytest-bdd for the acceptance
tests, pytest-cov to ensure that the code coverage was verified, and obviously pytest
itself to run the test suite.
If we had to remember to tell all our colleagues working on the same project to install those
packages, it would be easy to forget some of them or end up with incorrect versions
installed. We could document our test dependencies, but even better would be to have
them managed automatically for us.
So, let's create a tox.ini file in our project directory, telling Tox where to find the project
to test, which dependencies are necessary to run the test suite, and how to run it:
[tox]
setupdir = ./src
[testenv]
deps =
    pytest == 6.0.2
    pytest-bdd == 3.4.0
    flaky == 3.7.0
    pytest-benchmark == 3.2.3


