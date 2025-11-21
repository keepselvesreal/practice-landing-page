# Chapter 8: PyTest Essential Plugins (pp.188-207)

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


---
**Page 190**

PyTest Essential Plugins
Chapter 8
[ 190 ]
Installing pytest-cov makes the coverage reporting available through the --cov option.
Running PyTest with that option will immediately output the coverage at the end of the
test suite and will save it in a .coverage file to make it available for later consultation.
By default, running just pytest --cov will provide the coverage of every single module
that was imported during the execution of your tests (including all libraries and
frameworks you used in your application), which is not very helpful. As we only care about
the coverage of our own software, it's possible to tell pytest-cov which package to report
coverage for simply by adding it as an argument to the --cov option.
As we care about how much of our contacts application is actually verified by our tests, we
are going to run pytest --cov=contacts so that we get back coverage information only
for the contacts package, which is the one we care about:
$ pytest --cov=contacts
================= test session starts =================
plugins: cov-2.10.1, bdd-4.0.1
collected 23 items
tests/acceptance/test_adding.py .. [ 8%]
tests/functional/test_basic.py ... [ 21%]
tests/unit/test_adding.py ...... [ 47%]
tests/unit/test_application.py ....... [ 78%]
tests/unit/test_persistence.py .. [ 86%]
tests/acceptance/test_delete_contact.py . [ 91%]
tests/acceptance/test_list_contacts.py .. [100%]
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts  Miss  Cover
----------------------------------------------
src/contacts/__init__.py  48     1     98%
src/contacts/__main__.py  2      2     0%
----------------------------------------------
TOTAL 50 3 94%
Great! Our tests cover nearly all our code. The contacts/__init__.py module, which is
the one where we have all the code that implements our contact book app, is covered at
98%. Out of the 48 lines of code that compose it, there is only one line that isn't covered.


---
**Page 191**

PyTest Essential Plugins
Chapter 8
[ 191 ]
But how can we know which one it is? pytest-cov obviously knows; we just have to tell it to
print it out. That's what the --cov-report option is made for. If we run pytest with the -
-cov-report=term-missing option, it's going to tell us the lines of code that were not
covered by tests in each Python file:
$ pytest --cov=contacts --cov-report=term-missing
...
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts Miss Cover Missing
--------------------------------------------------------
src/contacts/__init__.py  48    1    98%   68
src/contacts/__main__.py  2     2    0%    1-3
--------------------------------------------------------
TOTAL                     50    3    94%
Here, for example, we know that lines 1 to 3 in contacts/__main__.py are not tested.
And that's OK, as those just import and invoke contacts.main() for the convenience of
being able to run our contacts program with python -m contacts once installed
(module.__main__ is what Python invokes when you pass a module to the -m option):
from . import main
main()
We can easily tell pytest-cov to ignore that code by simply adding a pragma: no cover
comment near to the lines or code block we want to exclude from coverage:
from . import main # pragma: no cover
main() # pragma: no cover
Now, if we rerun our test suite, we will no longer get complaints about the __main__.py
module:
$ pytest --cov=contacts --cov-report=term-missing
...
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts Miss Cover Missing
--------------------------------------------------------
src/contacts/__init__.py  48    1    98%   68
src/contacts/__main__.py  0     0    100%
--------------------------------------------------------
TOTAL                     48    1    98%


---
**Page 192**

PyTest Essential Plugins
Chapter 8
[ 192 ]
Only the code in contacts/__init__.py still reports uncovered code. This is the module
that contains the real code of our application, so the uncovered line probably has to be
tested for real. Once we check what that line refers to, we discover that we have not yet
tested the main function:
67  def main():
68      raise NotImplementedError()
As we haven't tested it, we never noticed that it still has to be implemented. This means
that currently, running our contacts module will simply crash:
$ python -m contacts
Traceback (most recent call last):
  ...
  File "src/contacts/__init__.py", line 68, in main
    raise NotImplementedError()
NotImplementedError
Thanks to coverage pointing, we found out that the main function didn't have a test for it.
We notice that a piece of our application is still lacking and we can now move to provide a
test for it and implement it.
We are going to create a new module in tests/functional/test_main.py where we are
going to write our test for the main function. Our test is going to provide some fake data
pre-loaded (we are not really interested in involving I/O here, so let's replace it with a fake
implementation) and verify that when the user runs the "contacts ls" command from
the command line, the contacts are actually listed back:
import sys
from unittest import mock
import contacts
class TestMain:
    def test_main(self, capsys):
        def _stub_load(self):
            self._contacts = [("name", "number")]
        with mock.patch.object(contacts.Application, "load",
                               new=_stub_load):
            with mock.patch.object(sys, "argv", new=["contacts", "ls"]):
                contacts.main()
        out, _ = capsys.readouterr()
        assert out == "name number\n"


---
**Page 193**

PyTest Essential Plugins
Chapter 8
[ 193 ]
The implementation required to pass our test is actually pretty short. We just have to create
the application, load the stored contacts, and then run the command provided on the
command line:
def main():
    import sys
    a = Application()
    a.load()
    a.run(' '.join(sys.argv))
We can then verify that we finally have 100% coverage of our code from tests and that they
all pass by rerunning the pytest --cov=contacts command:
$ pytest --cov=contacts
collected 24 items
tests/acceptance/test_adding.py .. [ 8%]
tests/functional/test_basic.py ... [ 20%]
tests/functional/test_main.py . [ 25%]
tests/unit/test_adding.py ...... [ 50%]
tests/unit/test_application.py ....... [ 79%]
tests/unit/test_persistence.py .. [ 87%]
tests/acceptance/test_delete_contact.py . [ 91%]
tests/acceptance/test_list_contacts.py .. [100%]
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts  Miss  Cover
----------------------------------------------
src/contacts/__init__.py  51     0     100%
src/contacts/__main__.py  0      0     100%
----------------------------------------------
TOTAL                     51     0     100%
If we want our coverage to be verified on every test run, we could leverage the addopts
option in pytest.ini and make sure that coverage is performed every time we run
PyTest:
[pytest]
addopts = --cov=contacts --cov-report=term-missing
As we have already seen, using addopts ensures that some options are always provided on
every PyTest execution. Thus, we will add coverage options every time we run PyTest.


---
**Page 194**

PyTest Essential Plugins
Chapter 8
[ 194 ]
Coverage as a service
Now that all our tests are passing and our code is fully verified, how can we make sure we
don't forget about verifying our coverage when we extend our code base? As we have seen
in Chapter 4, Scaling the Test Suite, there are services that enable us to run our test suite on
every new commit we do. Can we leverage them to also make sure that our coverage didn't
worsen?
Strictly speaking, ensuring that the coverage doesn't decrease requires comparing the
current coverage with the one of the previous successful run, which is something that
services such as Travis CI are not able to do as they don't persist any information after our
tests have run. So, the information pertaining to the previous runs is all lost.
Luckily, there are services such as Coveralls that integrate very well with Travis CI and
allow us to easily get our coverage in the cloud:
Figure 8.1 – Coveralls web page


---
**Page 195**

PyTest Essential Plugins
Chapter 8
[ 195 ]
As for Travis CI, we can log in with our GitHub account and add any repository that we
had on GitHub:
Figure 8.2 – Adding a repo on Coveralls
Once a repository is enabled, Coveralls is ready to receive coverage data for that repository.
But how can we get the coverage there?
First of all, we have to tell Travis CI to install support for Coveralls, so, in the install section
of our project, .travis.yml, we can add the relevant command:
install:
  - "pip install coveralls"
Then, given that we should already be generating the coverage data by running pytest --
cov, we have to tell Travis CI to send that data to Coveralls when the test run succeeds:
after_success:
  - coveralls
Our final .travis.yml file should look like the following:
install:
  - "pip install coveralls"
  - "pip install -e src"
script:
  - "pytest -v --cov=contacts"


---
**Page 196**

PyTest Essential Plugins
Chapter 8
[ 196 ]
after_success:
  - coveralls
If we have done everything correctly, we should see in Coveralls the trend of our coverage
reporting and we should be able to get notified when it lowers or goes below a certain
threshold:
Figure 8.3 – Coveralls coverage reporting
Now that we have our coverage reporting in place, we can move on to taking a look at the
other principal plugins that are available for PyTest.
Using pytest-benchmark for benchmarking
Another frequent need when writing applications used by many users is to make sure that
they perform in a reasonable way and, hence, that our users don't have to wait too long for
something to happen. This is usually achieved by benchmarking core paths of our code
base to make sure that slowdowns aren't introduced in those functions and methods. Once
we have a good benchmark suite, all we have to do is rerun it on every code change and
compare the results to previous runs. If nothing got slower, we are good to go.


---
**Page 197**

PyTest Essential Plugins
Chapter 8
[ 197 ]
PyTest has a pytest-benchmark plugin that makes it easy to create and run benchmarks
as parts of our test suite. Like any other Python distribution, we can install pytest-
benchmark through pip:
$ pip install pytest-benchmark
Once we have it installed, we can start organizing our benchmarks in their own dedicated
directory. This way, they don't mix with tests, as usually we don't want to run benchmarks
on every test run.
For example, if we want to test how fast our app can load 1,000 contacts, we could create a
benchmarks/test_persistence.py module as the home of a test_loading function
meant to benchmark the loading of contacts:
from contacts import Application
def test_loading(benchmark):
    app = Application()
    app._contacts = [(f"Name {n}", "number") for n in range(1000)]
    app.save()
    benchmark(app.load)
The benchmark fixture is provided automatically by pytest-benchmark and should be
used to invoke the function we want to benchmark, in this case, the Application.load
method. What your test does is create a new contacts application, and then populates it
with a list of 1,000 contacts and saves those contacts on this list. This ensures that we have
local contacts to load back.
Then, we can benchmark how long it takes to load back those same contacts, as
benchmark(app.load) is going to invoke app.load(), measuring how long it takes to
run it. To run our benchmarks, we can just run them like any other PyTest suite. Running
pytest benchmarks is enough to get our benchmarks report:
$ pytest -v benchmarks
...
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False
min_rounds=1 min_time=0.000005 max_time=1.0 calibration_precision=10
warmup=False warmup_iterations=100000)
benchmarks/test_persistence.py::test_loading PASSED [100%]
-------------------------- benchmark: 1 tests --------------------------
Name (time in us)   Min     Max        Mean  ...   OPS (Kops/s)   Rounds
------------------------------------------------------------------------


---
**Page 198**

PyTest Essential Plugins
Chapter 8
[ 198 ]
test_loading        714.7   22,312.3   950.7 ...   1.0518         877
------------------------------------------------------------------------
==================== 1 passed in 1.96s ====================
Running our benchmarks allows us to know that loading back 1,000 contacts takes a
minimum of 0.7 milliseconds, a maximum of 22 milliseconds, and an average of 0.9
milliseconds. In total, we can load back 1,000 contacts exactly 1,051 times in a second.
pytest-benchmark actually provides much more information about our benchmark run, but
for the sake of readability, some of those metrics were excluded in the previously reported
run.
How did pytest-benchmark know those metrics? Well, it runs our function 877 times. When
dealing with benchmarks, running them only once is usually not enough to get a solid
result. If the function is very fast, operative system context switches might weigh on the
execution time significantly, and so might provide false results where the time we get is
actually heavily influenced by the fact that our system was busy.
pytest-benchmark will decide automatically whether it's necessary to run a benchmark
more than once because it's too fast. This is to guarantee that we can get a fairly stable
benchmark report even when a very fast function is under the benchmark (and so its
execution time can be heavily influenced by system load).
At a minimum, pytest-benchmark will run a function five times before declaring how fast it
is. If we have very slow benchmarks and we want them to run no more than once, we can
provide the --benchmark-min-rounds=1 option.
Comparing benchmark runs
Now that we know how to run benchmarks, we need to be able to understand whether
they got slower compared with previous runs. This can be done by providing --
benchmark-autosave --benchmark-compare options to PyTest.
The --benchmark-autosave option will make sure that every benchmark run we perform
gets saved in a .benchmarks directory. This way, they are all available for future reference,
and then the --benchmark-compare option will tell pytest-benchmark to compare the
current run to the one saved previously.
This is a convenient built-in functionality compared to coverage reporting where, in order
to ensure non-decreasing coverage, we had to rely on an additional service or implement
the check ourselves.


---
**Page 199**

PyTest Essential Plugins
Chapter 8
[ 199 ]
The result of running with --benchmark-compare is a report where both runs are
provided for comparison:
-------------------------- benchmark: 2 tests --------------------------
Name (time in us)           Min          Max          Mean          ...
------------------------------------------------------------------------
test_loading (0002_371810a) 726.9 (1.0)  23,884 (1.0)  956.7 (1.0)  ...
test_loading (NOW)          730.1 (1.00) 24,117 (1.01) 969.6 (1.01) ...
------------------------------------------------------------------------
For example, in this example, we can see that the previous run (0002_371810a) is as fast as
the current one (NOW), so our code didn't get any slower. If our code base did get slower,
pytest-benchmark doesn't only tell us that the performance worsened. It also allows us to
know what the bottleneck in our code base is by using the --benchmark-
cprofile=tottime option.
For example, running our loading benchmark with --benchmark-cprofile=tottime
will tell us that, as expected, the majority of the time in our Application.load function is
actually spent reading JSON:
test_persistence.py::test_loading (NOW)
ncalls tottime percall cumtime percall filename:lineno(function)
1      0.0004  0.0004  0.0004  0.0004 .../json/decoder.py:343(raw_decode)
1      0.0002  0.0002  0.0002  0.0002 contacts/__init__.py:43(<listcomp>)
1      0.0001  0.0001  0.0009  0.0009 contacts/__init__.py:40(load)
Thanks to the performance tests, we have a good understanding of how quick our
application can load contacts and where the time loading contacts is spent. This should
allow us to evolve it while making sure we don't stray too far from the current
performance.
Using flaky to rerun unstable tests
A problem that developers frequently start encountering with fairly big projects that need
to involve third-party services, networking, and concurrency is that it becomes hard to
ensure that tests that integrate many components behave in a predictable way.
Sometimes, tests might fail just because a component responded later than usual or a
thread moved forward before another one. Those are things our tests should be designed to
prevent and avoid by making sure the test execution is fully predictable, but sometimes it's
not easy to notice that we are testing something that exhibits unstable behavior.


---
**Page 200**

PyTest Essential Plugins
Chapter 8
[ 200 ]
For example, you might be writing an end-to-end test where you are loading a web page to
click a button, but at the time you try to click the button, the button itself might not have
appeared yet.
Those kinds of tests that sometimes fail randomly are called "flaky" and are usually caused
by a piece of the system that is not under the control of the test itself. When possible, it's
usually best to put that part of the system under control of the test or replace it with a fake
implementation that can be controlled. But when it's not possible, the best we can do is to
retry the test.
The flaky plugin does that for us. It will automatically retry tests that fail until they pass
or up to a maximum number of attempts. An example of such tests is when concurrency is
involved. For example, we might write a function that appends entries to a list using
threading:
def flaky_appender(l, numbers):
    from multiprocessing.pool import ThreadPool
    with ThreadPool(5) as pool:
        pool.map(lambda n: l.append(n), numbers)
The test for such a function would probably just check that all the items provided are
correctly appended to the list:
def test_appender():
    l = []
    flaky_appender(l, range(7000))
    assert l == list(range(7000))
Running the test would probably succeed most of the time:
$ pytest tests/unit/test_flaky.py -q
tests/unit/test_flaky.py::test_appender PASSED
So we might think that our function works OK, but then we start seeing that sometimes, the
test fails for no apparent reason.
At this point, we can install the flaky plugin to handle our flaky test:
$ pip install flaky


---
**Page 201**

PyTest Essential Plugins
Chapter 8
[ 201 ]
The first thing we can do is to confirm whether our test is actually flaky by running it
multiple times in a row and checking whether it always succeeds. That's something the
flaky plugin can do for us through the --min-passes option:
$ pytest test_flaky.py --force-flaky --min-passes=10 --max-runs=10
test_appender failed; it passed 9 out of the required 10 times.
        <class 'AssertionError'>
        assert [0, 1, 2, 3, 4, 5, ...] == [0, 1, 2, 3, 4, 5, ...]
  At index 5345 diff: 5600 != 5345
As expected, our test succeeded on nine runs, but then failed on the 10
th, which confirms
that it's a flaky test.
Every time it fails, our entire release process is blocked and we have to rerun the tests and
wait for them to complete again. If this happens frequently, it can get frustrating. That's
where flaky becomes handy. We can decorate the test with the @flaky decorator to mark
it as a flaky test:
from flaky import flaky
@flaky
def test_appender():
    l = []
    flaky_appender(l, range(7000))
    assert l == list(range(7000))
Now that our test is marked as a flaky one, whenever pytest fails to run it, it will simply
retry it, twice by default, but we can control it with the --max-runs option:
$ pytest tests/unit/test_flaky.py -v
test_appender failed (1 runs remaining out of 2).
...
test_appender passed 1 out of the required 1 times. Success!
In the previous code snippet, our test failed the first run, but flaky noticed that it still had
one more try to go out of the default figure of two and retried. Then, on the second try, the
test succeeded and PyTest continued.
This allows us to quarantine our flaky tests. We can mark them as flaky and have them not
block our release process while we work on providing a more complete solution.
It's usually a good idea to immediately mark as flaky any test that we see unexpectedly fail
even just once (unless it's due to a real bug) and then have some dedicated time at which
we go through all our flaky tests, trying to unflake them by making the tests more
predictable.


---
**Page 202**

PyTest Essential Plugins
Chapter 8
[ 202 ]
Some people prefer to skip the tests that they quarantine, but (while being more robust than
marking them as flaky) this means that you are willing to live with the risk of introducing
any bugs those tests were meant to catch. So, flaky is usually a safer solution and the
important part is to have some dedicated time to go back to those quarantined tests to fix
them.
Using pytest-testmon to rerun tests on code
changes
In a fairly big project, rerunning the whole test suite can take a while, so it's not always
feasible to rerun all tests on every code change. We might settle for rerunning all tests only
when we commit a stable point of the code and run just a subset of them on every code
change before we decide whether to commit our changes.
This approach is usually naturally moved forward by developers who tend to pick a single
test, a test case, or a subset of tests that can act as canaries for their code changes.
For example, if I'm modifying the persistence layer of our contacts application, I would
probably rerun all tests that involve the save or load keywords:
$ pytest -k save -k load --ignore benchmarks -v
...
tests/functional/test_basic.py::TestStorage::test_reload PASSED [ 50%]
tests/unit/test_persistence.py::TestLoading::test_load PASSED [100%]
Once those canary tests pass, I would rerun the whole test suite to confirm that I actually
haven't broken anything and I can commit the relevant code. If there are issues, I would
obviously catch them when I run the full test suite, but on a fairly big project that can take
tens of minutes, it's not a convenient way to catch errors, and the earlier I'm able to catch
any errors, the faster I'll be at releasing my code as I don't have to wait for the full test suite
to run on every change.
In our case, would just rerunning the tests that have the load and save keyword in them
be enough to catch all possible issues and thus require us to rerun the whole test suite only
once as we are very confident that it will pass?
Probably not. There are quite a few more tests that invoke the persistence layer and don't
have those keywords in their name. Also, we might not always be so lucky as to have a set
of keywords we can use to pick a set of canary tests for every change we do. That's where
pytest-testmon comes in handy.


---
**Page 203**

PyTest Essential Plugins
Chapter 8
[ 203 ]
pytest-testmon will build a graph of relationships between all our code functions and
then, on subsequent runs, we can tell testmon to only run the tests that are influenced by
the code we change.
Ensure testmon is installed, as follows:
$ pip install pytest-testmon
We can do the first run of our test suite to build the relationship graph between the code
and tests:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 25 items
...
================== 25 passed in 2.67s ===================
Then, we can change any function of our persistence layer (for example, let's just add
return None at the end of the Application.save function), as follows:
    def save(self):
        with open("./contacts.json", "w+") as f:
            json.dump({"_contacts": self._contacts}, f)
        return None
And then we can rerun all the tests that are somehow related to saving data by rerunning
testmon again:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 16 items / 14 deselected / 2 selected
tests/unit/test_persistence.py . [ 9%]
tests/unit/test_adding.py ... [ 36%]
tests/acceptance/test_adding.py .. [ 54%]
tests/functional/test_basic.py .. [ 72%]
tests/acceptance/test_list_contacts.py . [ 81%]
tests/acceptance/test_delete_contact.py . [ 90%]
tests/acceptance/test_list_contacts.py . [100%]
=========== 11 passed, 14 deselected in 1.30s ============


---
**Page 204**

PyTest Essential Plugins
Chapter 8
[ 204 ]
In this second run, you can see that instead of running all 25 tests that we had, testmon
only picked 11 of them, those that somehow invoked the Application.save method
directly or indirectly, in other words, those that might end up being broken by a change to
the method.
Every time we rerun pytest with the --testmon option, only the tests related to the code
that we have changed will be rerun. If we try to run pytest --testmon again, for
example, no tests would be run as we haven't changed anything from the previous run:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 0 items / 25 deselected
================= 25 deselected in 0.14s ==================
This is a convenient way to pick only those tests that are related to our recent code changes
and to verify our code on every code change without having to rerun the entire test suite or
guess which tests might need to be checked again.
It should be remembered, by the way, that if the behavior of the code
depends on configuration files or data saved on disk or on a database,
then testmon can't detect that tests have to be rerun to verify the behavior
again when those change. In general, by the way, having your test suite
depend on the state of external components is not a robust approach, so
it's better to make sure that your fixtures take care of setting up a fresh
state on every run.
Running tests in parallel with pytest-xdist
As your test suite gets bigger and bigger, it might start taking too long to run. Even if
strategies to reduce the number of times you need to run the whole test suite are in place,
there will be a time where you want all your tests to run and act as the gatekeeper of your
releases.
Hence, a slow test suite can actually impair the speed at which we are able to develop and
release software.


---
**Page 205**

PyTest Essential Plugins
Chapter 8
[ 205 ]
While great care must always be taken to ensure that our tests are written in the fastest
possible way (avoid throwing time.sleep calls everywhere, they can be very good at
hiding themselves in the most unexpected places), slow components of the software that
we are testing should be replaced with fake implementations every time so that it is
possible that we can get to a point where there isn't much else we can do and making our
test suite faster would be too complex or expensive.
When we get to that point, if we wrote our tests such that they are properly isolated (the
state of one test doesn't influence or depend on the state of another test), a possible
direction to pursue is to parallelize the execution of our tests.
That's exactly what we can achieve by installing the pytest-xdist plugin:
$ pip install pytest-xdist
Once xdist is available, our tests can be run using multiple concurrent workers with the -
n numprocesses option:
$ pytest -n 2
=========== test session starts ==========
...
gw0 [26] / gw1 [26]
.......................... [100%]
============ 26 passed in 2.71s ==========
With -n 2, two workers were started for our tests (gw0 and gw1) and tests were equally
distributed between the two. Nearly half of the tests should have gone to gw0 and the other
half to gw1 (PyTest doesn't actually divide the tests equally; it depends on how fast they are
to run, but in general, anticipating that tests are equally split is a good approximation).
Note that as benchmarks can't provide reliable results when run
concurrently, pytest-benchmark will disable benchmarking when the -n
option is provided. The benchmarks will run as normal tests, so you
might want to just skip them by explicitly pointing PyTest to the tests
directory only, or by using --ignore benchmarks.
We can see how tests are distributed simply by running pytest in verbose mode with -v.
In verbose mode, near to every test, we will see which worker was in charge of executing
the test:
...
[gw0] [ 12%] PASSED test_adding.py::TestAddingEntries::test_basic
[gw1] [ 16%] PASSED test_main.py::TestMain::test_main
...


---
**Page 206**

PyTest Essential Plugins
Chapter 8
[ 206 ]
If you are unsure about how many workers to start, the -n option also accepts the value
"auto", which will detect how many processes to start based on how many CPUs the
system has.
It is, by the way, important to note that if the test suite is very fast and runs in just a matter
of seconds, running it in parallel might actually just make it slower. Distributing the tests
across different workers and starting them involves some extra work.
Summary
In this chapter, we saw the most frequently used plugins that exist for PyTest, those plugins
that can make your life easier by taking charge of some frequent needs that nearly every
test suite will face.
But there isn't any PyTest plugin that is able to manage the test environment itself. We are
still forced to set up manually all dependencies that the tests have and ensure that the
correct versions of Python are available to run the tests.
It would be great if there was a PyTest plugin able to install everything that we need in
order to run our test suite and just "run tests" on a new environment. Well, the good news
is that it exists; it's not strictly a PyTest plugin, but it's what Tox, which we are going to
introduce in the next chapter, was designed for.


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


