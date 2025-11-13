# 8.3.1 Comparing benchmark runs (pp.198-199)

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


