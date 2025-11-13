# 9.3.1 Using environments for more than Python versions (pp.213-215)

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


