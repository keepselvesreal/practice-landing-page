# 9.3.0 Introduction [auto-generated] (pp.211-213)

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


