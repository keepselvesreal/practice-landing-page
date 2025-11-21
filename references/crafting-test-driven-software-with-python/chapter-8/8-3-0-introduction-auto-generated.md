# 8.3.0 Introduction [auto-generated] (pp.196-198)

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


