# 9.2 Introducing Tox (pp.208-211)

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


---
**Page 209**

Managing Test Environments with Tox
Chapter 9
[ 209 ]
    pytest-cov == 2.10.1
commands =
    pytest --cov=contacts
The [tox] section configures Tox itself. In this case, it can ascertain through the setupdir
= option where to find the project that is under test.
The [testenv] section is instead meant to provide directives for each environment in
which we want to test our project. In this case, through the deps = option, we are listing all
things that need to be installed in that environment so that the project can be tested (the
project itself is always automatically installed by Tox, so no need to list it here), and by
using the commands = options, we are telling Tox how to test the project in the
environments.
Once this file is in place in the root of our project, we can prepare a fully working
environment and test the project by simply invoking the tox command:
$ tox
GLOB sdist-make: ./src/setup.py
python create: ./.tox/python
python installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
python inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
python installed: ...
python run-test: commands[0] | pytest --cov=contacts
====================== test session starts ======================
...
collected 26 items
tests/acceptance/test_delete_contact.py . [ 3%]
tests/acceptance/test_list_contacts.py .. [ 11%]
benchmarks/test_persistence.py . [ 15%]
tests/acceptance/test_adding.py .. [ 23%]
tests/functional/test_basic.py ... [ 34%]
tests/functional/test_main.py . [ 38%]
tests/unit/test_adding.py ...... [ 61%]
tests/unit/test_application.py ....... [ 88%]
tests/unit/test_flaky.py . [ 92%]
tests/unit/test_persistence.py .. [100%]
----------- coverage: platform linux, python 3.7.3-final-0 -----------
Name                  Stmts Miss Cover
----------------------------------------------------------------------
contacts/__init__.py  51    0    100%
contacts/__main__.py  0     0    100%
----------------------------------------------------------------------
TOTAL                 51    0    100%


---
**Page 210**

Managing Test Environments with Tox
Chapter 9
[ 210 ]
-------------------------- benchmark: 1 tests --------------------------
Name (time in us) Min Max Mean ... OPS (Kops/s) Rounds
------------------------------------------------------------------------
test_loading 714.7 22,312.3 950.7 ... 1.0518 877
------------------------------------------------------------------------
====================== 26 passed in 2.41s ======================
As you can see, Tox created a new Python environment in ./tox /python, installed our
project and all the required dependencies for us, and then started the test suite providing
coverage and benchmarks.
The side effect of this approach is that we lost a bit of flexibility in terms of what we can tell
PyTest. Tox is going to run all our tests and benchmarks. If we only want to run some of
them, there is no way of doing this.
This flexibility can be regained by using the Tox {posargs} variable, which will proxy all
options we provide in the command line from Tox to our test suite. So we can put
{posargs} in our commands option in tox.ini so that any additional option we provide
to Tox gets forwarded to our test command:
commands =
    pytest --cov=contacts {posargs}
Now, if we run Tox with any additional option after --, it will be forwarded to PyTest. For
example, to exclude benchmarks from our run, we can use tox -- ./tests to exclude
benchmarks and only run the tests that are related to loading back our contacts. Instead, we
can use tox -- ./tests -k load:
$ tox -- ./tests -k load
...
============= test session starts =============
collected 25 items / 23 deselected / 2 selected
tests/functional/test_basic.py . [ 50%]
tests/unit/test_persistence.py . [100%]
...
====== 2 passed, 23 deselected in 0.35s =======
Now that we know how to use Tox to set up the testing environment without losing the
flexibility that was afforded to us earlier when we did things manually, we can move
forward and see how to actually set up multiple testing environments on different versions
of Python.


---
**Page 211**

Managing Test Environments with Tox
Chapter 9
[ 211 ]
Testing multiple Python versions with Tox
Tox is based on the concept of environments. The goal of Tox is to prepare those 
environments where it will run the commands provided. Usually, those environments are
meant for testing (running tests in different conditions) and the most common kind of
environments are those that use different Python versions. But in theory, it is possible to
create a different environment for any other purpose. For example, we frequently create an
environment where project documentation is built.
To add further environments to Tox, it's sufficient to list them inside the envlist = option.
To configure two environments that test our project against both Python 2.7 and Python
3.7, we can set envlist to both py37 and py27:
[tox]
setupdir = ./src
envlist = py27, py37
If we run tox again, we will see that it will now test our project on two different
environments, one made for Python 2.7 and one for Python 3.7:
$ tox
GLOB sdist-make: ./src/setup.py
py27 create: ./.tox/py27
py27 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
...
py37 create: ./.tox/py37
py37 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
We obviously need to have working executables of those two Python versions on our
system, but as far as they are available and running the python3.7 and python2.7
commands works, Tox will be able to leverage them.
By default, all environments apply the same configuration, the one provided in [testenv],
so in our case, Tox tried to install the same exact dependencies and run the same exact
commands on both Python 2.7 and Python 3.7.


