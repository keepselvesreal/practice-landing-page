# 8.4 Using flaky to rerun unstable tests (pp.199-202)

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


