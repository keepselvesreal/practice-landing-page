# Chapter 9: Managing Test Environments with Tox (pp.207-220)

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


---
**Page 212**

Managing Test Environments with Tox
Chapter 9
[ 212 ]
On Python 2.7, it failed because PyTest no longer supports Python 2.7 on versions after
4.6.11, so if we want to actually test our project on Python 2.7, we need to provide a custom
configuration for the environment and make it work against a previous PyTest version:
py27 create: ./.tox/py27
py27 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
ERROR: Could not find a version that satisfies the requirement
pytest==6.0.2 (from versions: 2.0.0, ..., 4.6.11)
ERROR: No matching distribution found for pytest==6.0.2
To fix this issue, we can simply go back and provide a custom configuration for the Python
2.7 environment where we are going to customize the deps = option, stating explicitly that
on that version of Python, we want to use a previous PyTest version:
[testenv:py27]
deps =
    pytest == 4.6.11
    pytest-bdd == 3.4.0
    flaky == 3.7.0
    pytest-benchmark == 3.2.3
    pytest-cov == 2.10.1
Options can be specialized just by creating a section named [testenv:envname], in this
case, [testenv:py27], as we want to override the options for the py27 environment.
Any option that isn't specified is inherited from the generic [testenv] configuration, so as
we haven't overridden the command = option, the configuration we provided in
[testenv] will be used for testing on Python 2.7, too.
By running Tox with this new configuration, we will finally be able to set up the
environment, install PyTest, and start our tests:
$ tox
GLOB sdist-make: ./09_tox/src/setup.py
py27 create: ./09_tox/.tox/py27
py27 installdeps: pytest == 4.6.11, pytest-bdd == 3.4.0, flaky == 3.7.0,
pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
py27 inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
py27 installed: contacts @
file://./.tox/.tmp/package/1/contacts-0.0.0.zip,pytest==4.6.11,...
py27 run-test-pre: PYTHONHASHSEED='2140925334'
py27 run-test: commands[0] | pytest --cov=contacts


---
**Page 213**

Managing Test Environments with Tox
Chapter 9
[ 213 ]
As we could have anticipated, our tests fail on Python 2.7 as our project wasn't written to
support such an old Python version:
platform linux2 -- Python 2.7.16, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py27/.pytest_cache
rootdir: .
plugins: bdd-3.4.0, flaky-3.7.0, benchmark-3.2.3, cov-2.10.1
collected 5 items / 7 errors
================ ERRORS ===================
    mod = self.fspath.pyimport(ensuresyspath=importmode)
.tox/py27/lib/python2.7/site-packages/py/_path/local.py:704: in pyimport
    __import__(modname)
E File "./benchmarks/test_persistence.py", line 5
E app._contacts = [(f"Name {n}", "number") for n in range(1000)]
E                             ^
E SyntaxError: invalid syntax
========== 7 error in 1.07 seconds ========
For example, we used f-strings, which were not supported on Python 2.7. Porting projects
to Python 2.7 is beyond the scope of this book, so we are not going to modify our project to
make it work there, but the same concepts that we have seen while using Python 2.7 do
apply to any other environment.
For example, if, instead of Python 2.7, we wanted to test our project against Python 3.8, we
could have just used py38 instead of py27 as the name of the environment. In that case, we
wouldn't even have to customize the deps = option for that environment as PyTest 6
works fine on Python 3.8.
Using environments for more than Python
versions
By default, Tox provides a few predefined environments for various Python versions, but
we can declare any kind of environment that differs for whatever reason.
Another common way to use this capability is to create various environments that differ for
the commands = option, and so do totally different things. You will probably frequently see
that this used to provide a way to build project documentation. It is not uncommon to see a
docs environment in Tox configurations that, instead of running tests, builds the project
documentation.
In our case, we might want to use this feature to disable benchmarks by default and make
them run only when a dedicated environment is used.


---
**Page 214**

Managing Test Environments with Tox
Chapter 9
[ 214 ]
To do so, we are going to disable benchmarks by default in our [testenv] configuration:
[tox]
setupdir = ./src
envlist = py27, py37
[testenv]
deps =
    pytest == 6.0.2
    pytest-bdd == 3.4.0
    flaky == 3.7.0
    pytest-benchmark == 3.2.3
    pytest-cov == 2.10.1
commands =
    pytest --cov=contacts --benchmark-skip {posargs}
[testenv:py27]
...
Then we are going to add one more [testenv:benchmarks] environment that runs only
the benchmarks:
[testenv:benchmarks]
commands =
    pytest --no-cov ./benchmarks {posargs}
This environment will inherit the configuration from our default environment, and thus
will use the same exact deps, but will provide a custom command where coverage is
disabled and only benchmarks are run.
It is important that we don't list this environment in the envlist option of the [tox]
section. Otherwise, the benchmarks would end up being run every time we invoke Tox,
which is not what we want.
To explicitly run benchmarks on demand, we can run Tox with the -e benchmarks option,
which will run Tox just for that specific environment:
$ tox -e benchmarks
GLOB sdist-make: ./src/setup.py
benchmarks create: ./.tox/benchmarks
benchmarks installdeps: pytest == 6.0.2, pytest-benchmark == 3.2.3, ...
benchmarks inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
benchmarks run-test-pre: PYTHONHASHSEED='257991845'
benchmarks run-test: commands[0] | pytest --no-cov ./benchmarks
======================= test session starts =======================
platform linux -- Python 3.7.3, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item


---
**Page 215**

Managing Test Environments with Tox
Chapter 9
[ 215 ]
benchmarks/test_persistence.py .                       [100%]
-------------------------- benchmark: 1 tests --------------------------
Name (time in us) Min Max Mean ... OPS (Kops/s) Rounds
------------------------------------------------------------------------
test_loading 714.7 22,312.3 950.7 ... 1.0518 877
------------------------------------------------------------------------
======================= 1 passed in 1.73s  =======================
We now have a configuration where running tox by default will run our tests on Python
2.7 and Python 3.7, and then running tox -e benchmarks does run benchmarks.
If we further want to specialize the behavior of our Tox configuration, we can do so by
adding more environments and customizing the options we care about. A complete
reference of all the Tox options is available on the ReadTheDocs page of Tox, so make sure
to take a look if you want to dive further into customizing Tox behavior.
Now that we have Tox working locally, we need to combine it with our CI system to ensure
that different CI processes are started for each Tox environment. As we have used Travis
for all our CI needs so far, let's see how we can integrate Tox with Travis.
Using Tox with Travis
Using Tox with a CI environment is usually fairly simple, but as both Tox and the CI will
probably end up wanting to manage the Python environment, some attention has to be
paid to enable them to exist together. To see how Travis and Tox can work together, we can
pick our chat project that we wrote in Chapter 4, Scaling the Test Suite, which we already
had on Travis-CI, and migrate it to use Tox.
We need to write a tox.ini file, which will take care of running the test suite itself:
[tox]
setupdir = ./src
envlist = py37, py38, py39
[testenv]
usedevelop = true
deps =
    coverage
commands =
    coverage run --source=src -m unittest discover tests -v
    coverage report


---
**Page 216**

Managing Test Environments with Tox
Chapter 9
[ 216 ]
[testenv:benchmarks]
commands =
    python -m unittest discover benchmarks
The commands you see in tox.ini are the same that we previously had in the
travis.yml file under the script: section. That's because, previously, Travis itself was in
charge of running our tests. Now, Tox will be in charge of doing so.
For the same reason, as the coverage reporting should happen every time we run the test
suite, we have Tox install the coverage dependency and run coverage report after the
test suite.
The main difference with tox.ini seen previously in the chapter is probably the
usedevelop = true option. That tells Tox to install our own project in editable mode
(sometimes called developer mode). Instead of making a distribution package out of our
source directory and then installing the distribution, Tox will install the source directory
itself. This is frequently convenient when coverage reporting is involved as we usually
want the coverage to be against our source code, and not against the installed distribution.
The benefit of using a Tox file is that it should work the same everywhere. So, before
moving it to Travis, we can verify that it actually does what we expect locally on our own
machine:
$ tox
py38 develop-inst-noop: travistest/src
py38 run-test: commands[0] | coverage run --source=src -m unittest discover
tests -v
test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
test_exchange_with_server (functional.test_chat.TestChatMessageExchange)
... ok
test_many_users (functional.test_chat.TestChatMessageExchange) ... ok
test_multiple_readers (functional.test_chat.TestChatMessageExchange) ... ok
test_client_connection (unit.test_client.TestChatClient) ... ok
test_client_fetch_messages (unit.test_client.TestChatClient) ... ok
test_nickname (unit.test_client.TestChatClient) ... ok
test_send_message (unit.test_client.TestChatClient) ... ok
test_broadcast (unit.test_connection.TestConnection) ... ok
----------------------------------------------------------------------
Ran 10 tests in 0.058s
OK
py38 run-test: commands[1] | coverage report
Name Stmts Miss Cover
------------------------------------------


---
**Page 217**

Managing Test Environments with Tox
Chapter 9
[ 217 ]
src/chat/__init__.py  0 0 100%
src/chat/client.py   29 0 100%
src/chat/server.py    7 0 100%
src/setup.py          2 2 0%
------------------------------------------
TOTAL                38 2 95%
As desired, it ran the test suite and then reported the code coverage. We also know, thanks
to [testenv:benchmarks], that if we want, we can run benchmarks with tox -e
benchmarks:
$ tox -e benchmarks
benchmarks develop-inst-noop: travistest/src
benchmarks run-test: commands[0] | python -m unittest discover benchmarks
  time: 0.06, iteration: 0.01
.
----------------------------------------------------------------------
Ran 1 test in 0.069s
OK
Now, the remaining element is to make Tox run inside Travis.
To do so, mostly we have to replace the script: section in our travis.yml file with a
single tox command. Then, Tox will do everything it has to do in order to make the tests
run as it did on our own PC:
script:
  - "tox"
However, Travis will also need Tox itself to run the commands. Therefore, we want to have
Travis install Tox before running the script. To do so, we are going to use a special package
named tox-travis and we are going to add it to the install: section:
install:
  - "pip install tox-travis"
You might be wondering why we used tox-travis instead of just tox. The reason is that
tox-travis takes care of that little extra work that is necessary to make Tox and Travis
collaborate. By default, Travis wants to install and set up Python, but Tox also wants to do
the same. That means that we would end up installing Python twice.


---
**Page 218**

Managing Test Environments with Tox
Chapter 9
[ 218 ]
Even worse, as we have envlist = py37, py38, py39 in our tox.ini, Tox would
actually try to run the tests against all three Python versions for each Travis Python
environment. So, suppose that we asked Travis to set up 3.7, 3.8, and 3.9. Then, Tox would
try to use 3.7, 3.8, and 3.9 inside the Travis 3.7 Python environment, and would then try to
use 3.7, 3.8, and 3.9 inside the Travis 3.8 Python environment, and so on, leading to errors
such as the following:
ERROR: py38: InterpreterNotFound: python3.8
ERROR: py39: InterpreterNotFound: python3.9
To avoid this problem, we can use tox-travis. When we use Tox-Travis, the Python
environments come from Travis only and Tox will simply use those already prepared by
Travis without trying to set up a second Python environment. At that point, our Tox
envlist is only helpful locally, and on Travis, the python: section of the travis.yml file
will dictate which Python versions get used.
Apart from making sure that we install tox-travis, the rest of our travis.yml file is
fairly similar to the original one our project had previously. We just replaced the
commands to run tests and benchmarks with those that Tox provides:
language: python
os: linux
dist: xenial
python:
  - 3.7
  - &mainstream_python 3.8
  - 3.9
  - nightly
install:
  - "pip install tox-travis"
  - "pip install coveralls"
script:
  - "tox"
after_success:
  - coveralls
  - "tox -e benchmarks"
Now that both our tox.ini and travis.yml configuration files are in place, we can just
push our repository changes and see that Travis successfully runs our tests using Tox:


---
**Page 219**

Managing Test Environments with Tox
Chapter 9
[ 219 ]
Figure 9.1 – Tox setup
It should became clear that once we have a working local Tox setup, moving on to Travis
involves very little apart from writing a travis.yml configuration file in charge of
installing tox-travis and then invoking tox.
Summary
In this chapter, we saw how Tox can take care of all the setup necessary to run our tests for
us and how it can do that on multiple target environments so that all we have to do to run
tests is just to invoke Tox itself.
This is a more convenient, but also robust, way to manage our test suite. The primary
benefit is that anyone else willing to contribute to our project won't have to learn how to set
up our projects and how to run tests. If our colleagues or project contributors are familiar
with Tox, seeing that our project includes a tox.ini file tells them all that they will need to
know—that they just have to invoke the tox command to run tests.
Now that we have seen the base plugins and tools to manage and run our test suite, in the
next chapter, we can move on to some more advanced topics that involve how to test our
documentation itself and how to use property-based testing to catch bugs in our code.


---
**Page 220**

10
Testing Documentation and
Property-Based Testing
In the previous chapter, we saw how to manage the environment where the test suite runs
through Tox. We now have a fairly good understanding of how to create a test suite, how to
set up an environment where this can be run, and how to ensure that we are able to
organize it in a way that remains effective as our software and test suite grow. We are now
going to move our attention to confirm that our tests are able to identify and cover corner
cases and make sure that our documentation is as robust and tested as our software itself.
In this chapter, we will cover the following topics:
Testing documentation
Property based-testing
Technical requirements
We need a working Python interpreter with PyTest, Sphinx for documentation testing, and
the Hypothesis framework for property-based testing. All of them can be installed through
pip with the help of the following command:
$ pip install pytest sphinx hypothesis
The examples have been written on Python 3.7, Sphinx 3.3.0, PyTest 6.0.2, and Hypothesis
5.41, but should work on most modern Python versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter10.


