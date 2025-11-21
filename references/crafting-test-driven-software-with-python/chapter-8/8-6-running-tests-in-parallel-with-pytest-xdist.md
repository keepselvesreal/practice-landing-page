# 8.6 Running tests in parallel with pytest-xdist (pp.204-206)

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


