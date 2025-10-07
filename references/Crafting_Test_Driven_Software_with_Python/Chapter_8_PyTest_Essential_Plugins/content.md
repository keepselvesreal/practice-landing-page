Line 1: 
Line 2: --- 페이지 198 ---
Line 3: 8
Line 4: PyTest Essential Plugins
Line 5: In the previous chapter, we saw how to work with PyTest and pytest-bdd to create
Line 6: acceptance tests and verify the requirements of our software.
Line 7: However, pytest-bdd is not the only useful plugin that PyTest has. In this chapter, we are
Line 8: going to continue working on the contacts project introduced in Chapter 7, Fitness Function
Line 9: with a Contact Book Application, showing how some of the most commonly used PyTest
Line 10: plugins can help during the development of a project.
Line 11: The plugins we are going to cover in this chapter are going to help us with verifying our
Line 12: test suite coverage of the application code, checking the performance of our application,
Line 13: dealing with tests that are flaky or unstable, and optimizing our development process by
Line 14: running only the impacted tests when we change the code base or by speeding up our
Line 15: whole test suite execution.
Line 16: In this chapter, we will cover the following topics:
Line 17: Using pytest-cov for coverage reporting
Line 18: Using pytest-benchmark for benchmarking
Line 19: Using flaky to rerun unstable tests
Line 20: Using pytest-testmon to rerun tests on code changes
Line 21: Running tests in parallel with pytest-xdist
Line 22: 
Line 23: --- 페이지 199 ---
Line 24: PyTest Essential Plugins
Line 25: Chapter 8
Line 26: [ 189 ]
Line 27: Technical requirements
Line 28: We need a working Python interpreter with the PyTest framework installed with the
Line 29: pytest-bdd plugin. PyTest and pytest-bdd can be installed with the following command:
Line 30: $ pip install pytest pytest-bdd
Line 31: For each section, you will need to install the plugin discussed in the section itself. You can
Line 32: install all of them at once:
Line 33: $ pip install pytest-cov pytest-benchmark flaky pytest-testmon pytest-xdist
Line 34: The examples have been written on Python 3.7 with PyTest 6.0.2 and pytest-bdd 4.0.1, but
Line 35: should work on most modern Python versions. The versions of the plugins in use for each
Line 36: section instead are pytest-cov 2.10, pytest-benchmark 2.3.2, flaky 3.7.0, pytest-testmon 1.0.3,
Line 37: and pytest-xdist 2.1.0.
Line 38: You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
Line 39: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter08.
Line 40: Using pytest-cov for coverage reporting
Line 41: We have already seen in Chapter 1, Getting Started with Software Testing, how code
Line 42: coverage by tests is a good measure for establishing how confident you can be in your test
Line 43: suite. A test suite that only runs 10% of all our code is probably not going to be very reliable
Line 44: in finding problems, as most of the code will go unchecked. A test suite that instead verifies
Line 45: 100% of our code is certainly going to exercise every single line of code we wrote and so
Line 46: should trigger bugs more easily if there are any.
Line 47: Obviously, coverage cannot verify code that you never wrote, so it's not going to detect that
Line 48: you have a bug because you forgot to add an if check in your method, but at least it tells
Line 49: you if you forgot to write a test for that method.
Line 50: Normally, test coverage in Python is done using the coverage module, which can be
Line 51: installed from PyPI, but PyTest has a convenient pytest-cov plugin that is going to do
Line 52: that for us and make our life simpler when we want to check the coverage of our tests. Like
Line 53: any other Python distribution, we can install pytest-cov through pip:
Line 54: $ pip install pytest-cov
Line 55: 
Line 56: --- 페이지 200 ---
Line 57: PyTest Essential Plugins
Line 58: Chapter 8
Line 59: [ 190 ]
Line 60: Installing pytest-cov makes the coverage reporting available through the --cov option.
Line 61: Running PyTest with that option will immediately output the coverage at the end of the
Line 62: test suite and will save it in a .coverage file to make it available for later consultation.
Line 63: By default, running just pytest --cov will provide the coverage of every single module
Line 64: that was imported during the execution of your tests (including all libraries and
Line 65: frameworks you used in your application), which is not very helpful. As we only care about
Line 66: the coverage of our own software, it's possible to tell pytest-cov which package to report
Line 67: coverage for simply by adding it as an argument to the --cov option.
Line 68: As we care about how much of our contacts application is actually verified by our tests, we
Line 69: are going to run pytest --cov=contacts so that we get back coverage information only
Line 70: for the contacts package, which is the one we care about:
Line 71: $ pytest --cov=contacts
Line 72: ================= test session starts =================
Line 73: plugins: cov-2.10.1, bdd-4.0.1
Line 74: collected 23 items
Line 75: tests/acceptance/test_adding.py .. [ 8%]
Line 76: tests/functional/test_basic.py ... [ 21%]
Line 77: tests/unit/test_adding.py ...... [ 47%]
Line 78: tests/unit/test_application.py ....... [ 78%]
Line 79: tests/unit/test_persistence.py .. [ 86%]
Line 80: tests/acceptance/test_delete_contact.py . [ 91%]
Line 81: tests/acceptance/test_list_contacts.py .. [100%]
Line 82: ----------- coverage: platform linux, python 3.8.2-final-0 -----------
Line 83: Name                      Stmts  Miss  Cover
Line 84: ----------------------------------------------
Line 85: src/contacts/__init__.py  48     1     98%
Line 86: src/contacts/__main__.py  2      2     0%
Line 87: ----------------------------------------------
Line 88: TOTAL 50 3 94%
Line 89: Great! Our tests cover nearly all our code. The contacts/__init__.py module, which is
Line 90: the one where we have all the code that implements our contact book app, is covered at
Line 91: 98%. Out of the 48 lines of code that compose it, there is only one line that isn't covered.
Line 92: 
Line 93: --- 페이지 201 ---
Line 94: PyTest Essential Plugins
Line 95: Chapter 8
Line 96: [ 191 ]
Line 97: But how can we know which one it is? pytest-cov obviously knows; we just have to tell it to
Line 98: print it out. That's what the --cov-report option is made for. If we run pytest with the -
Line 99: -cov-report=term-missing option, it's going to tell us the lines of code that were not
Line 100: covered by tests in each Python file:
Line 101: $ pytest --cov=contacts --cov-report=term-missing
Line 102: ...
Line 103: ----------- coverage: platform linux, python 3.8.2-final-0 -----------
Line 104: Name                      Stmts Miss Cover Missing
Line 105: --------------------------------------------------------
Line 106: src/contacts/__init__.py  48    1    98%   68
Line 107: src/contacts/__main__.py  2     2    0%    1-3
Line 108: --------------------------------------------------------
Line 109: TOTAL                     50    3    94%
Line 110: Here, for example, we know that lines 1 to 3 in contacts/__main__.py are not tested.
Line 111: And that's OK, as those just import and invoke contacts.main() for the convenience of
Line 112: being able to run our contacts program with python -m contacts once installed
Line 113: (module.__main__ is what Python invokes when you pass a module to the -m option):
Line 114: from . import main
Line 115: main()
Line 116: We can easily tell pytest-cov to ignore that code by simply adding a pragma: no cover
Line 117: comment near to the lines or code block we want to exclude from coverage:
Line 118: from . import main # pragma: no cover
Line 119: main() # pragma: no cover
Line 120: Now, if we rerun our test suite, we will no longer get complaints about the __main__.py
Line 121: module:
Line 122: $ pytest --cov=contacts --cov-report=term-missing
Line 123: ...
Line 124: ----------- coverage: platform linux, python 3.8.2-final-0 -----------
Line 125: Name                      Stmts Miss Cover Missing
Line 126: --------------------------------------------------------
Line 127: src/contacts/__init__.py  48    1    98%   68
Line 128: src/contacts/__main__.py  0     0    100%
Line 129: --------------------------------------------------------
Line 130: TOTAL                     48    1    98%
Line 131: 
Line 132: --- 페이지 202 ---
Line 133: PyTest Essential Plugins
Line 134: Chapter 8
Line 135: [ 192 ]
Line 136: Only the code in contacts/__init__.py still reports uncovered code. This is the module
Line 137: that contains the real code of our application, so the uncovered line probably has to be
Line 138: tested for real. Once we check what that line refers to, we discover that we have not yet
Line 139: tested the main function:
Line 140: 67  def main():
Line 141: 68      raise NotImplementedError()
Line 142: As we haven't tested it, we never noticed that it still has to be implemented. This means
Line 143: that currently, running our contacts module will simply crash:
Line 144: $ python -m contacts
Line 145: Traceback (most recent call last):
Line 146:   ...
Line 147:   File "src/contacts/__init__.py", line 68, in main
Line 148:     raise NotImplementedError()
Line 149: NotImplementedError
Line 150: Thanks to coverage pointing, we found out that the main function didn't have a test for it.
Line 151: We notice that a piece of our application is still lacking and we can now move to provide a
Line 152: test for it and implement it.
Line 153: We are going to create a new module in tests/functional/test_main.py where we are
Line 154: going to write our test for the main function. Our test is going to provide some fake data
Line 155: pre-loaded (we are not really interested in involving I/O here, so let's replace it with a fake
Line 156: implementation) and verify that when the user runs the "contacts ls" command from
Line 157: the command line, the contacts are actually listed back:
Line 158: import sys
Line 159: from unittest import mock
Line 160: import contacts
Line 161: class TestMain:
Line 162:     def test_main(self, capsys):
Line 163:         def _stub_load(self):
Line 164:             self._contacts = [("name", "number")]
Line 165:         with mock.patch.object(contacts.Application, "load",
Line 166:                                new=_stub_load):
Line 167:             with mock.patch.object(sys, "argv", new=["contacts", "ls"]):
Line 168:                 contacts.main()
Line 169:         out, _ = capsys.readouterr()
Line 170:         assert out == "name number\n"
Line 171: 
Line 172: --- 페이지 203 ---
Line 173: PyTest Essential Plugins
Line 174: Chapter 8
Line 175: [ 193 ]
Line 176: The implementation required to pass our test is actually pretty short. We just have to create
Line 177: the application, load the stored contacts, and then run the command provided on the
Line 178: command line:
Line 179: def main():
Line 180:     import sys
Line 181:     a = Application()
Line 182:     a.load()
Line 183:     a.run(' '.join(sys.argv))
Line 184: We can then verify that we finally have 100% coverage of our code from tests and that they
Line 185: all pass by rerunning the pytest --cov=contacts command:
Line 186: $ pytest --cov=contacts
Line 187: collected 24 items
Line 188: tests/acceptance/test_adding.py .. [ 8%]
Line 189: tests/functional/test_basic.py ... [ 20%]
Line 190: tests/functional/test_main.py . [ 25%]
Line 191: tests/unit/test_adding.py ...... [ 50%]
Line 192: tests/unit/test_application.py ....... [ 79%]
Line 193: tests/unit/test_persistence.py .. [ 87%]
Line 194: tests/acceptance/test_delete_contact.py . [ 91%]
Line 195: tests/acceptance/test_list_contacts.py .. [100%]
Line 196: ----------- coverage: platform linux, python 3.8.2-final-0 -----------
Line 197: Name                      Stmts  Miss  Cover
Line 198: ----------------------------------------------
Line 199: src/contacts/__init__.py  51     0     100%
Line 200: src/contacts/__main__.py  0      0     100%
Line 201: ----------------------------------------------
Line 202: TOTAL                     51     0     100%
Line 203: If we want our coverage to be verified on every test run, we could leverage the addopts
Line 204: option in pytest.ini and make sure that coverage is performed every time we run
Line 205: PyTest:
Line 206: [pytest]
Line 207: addopts = --cov=contacts --cov-report=term-missing
Line 208: As we have already seen, using addopts ensures that some options are always provided on
Line 209: every PyTest execution. Thus, we will add coverage options every time we run PyTest.
Line 210: 
Line 211: --- 페이지 204 ---
Line 212: PyTest Essential Plugins
Line 213: Chapter 8
Line 214: [ 194 ]
Line 215: Coverage as a service
Line 216: Now that all our tests are passing and our code is fully verified, how can we make sure we
Line 217: don't forget about verifying our coverage when we extend our code base? As we have seen
Line 218: in Chapter 4, Scaling the Test Suite, there are services that enable us to run our test suite on
Line 219: every new commit we do. Can we leverage them to also make sure that our coverage didn't
Line 220: worsen?
Line 221: Strictly speaking, ensuring that the coverage doesn't decrease requires comparing the
Line 222: current coverage with the one of the previous successful run, which is something that
Line 223: services such as Travis CI are not able to do as they don't persist any information after our
Line 224: tests have run. So, the information pertaining to the previous runs is all lost.
Line 225: Luckily, there are services such as Coveralls that integrate very well with Travis CI and
Line 226: allow us to easily get our coverage in the cloud:
Line 227: Figure 8.1 – Coveralls web page
Line 228: 
Line 229: --- 페이지 205 ---
Line 230: PyTest Essential Plugins
Line 231: Chapter 8
Line 232: [ 195 ]
Line 233: As for Travis CI, we can log in with our GitHub account and add any repository that we
Line 234: had on GitHub:
Line 235: Figure 8.2 – Adding a repo on Coveralls
Line 236: Once a repository is enabled, Coveralls is ready to receive coverage data for that repository.
Line 237: But how can we get the coverage there?
Line 238: First of all, we have to tell Travis CI to install support for Coveralls, so, in the install section
Line 239: of our project, .travis.yml, we can add the relevant command:
Line 240: install:
Line 241:   - "pip install coveralls"
Line 242: Then, given that we should already be generating the coverage data by running pytest --
Line 243: cov, we have to tell Travis CI to send that data to Coveralls when the test run succeeds:
Line 244: after_success:
Line 245:   - coveralls
Line 246: Our final .travis.yml file should look like the following:
Line 247: install:
Line 248:   - "pip install coveralls"
Line 249:   - "pip install -e src"
Line 250: script:
Line 251:   - "pytest -v --cov=contacts"
Line 252: 
Line 253: --- 페이지 206 ---
Line 254: PyTest Essential Plugins
Line 255: Chapter 8
Line 256: [ 196 ]
Line 257: after_success:
Line 258:   - coveralls
Line 259: If we have done everything correctly, we should see in Coveralls the trend of our coverage
Line 260: reporting and we should be able to get notified when it lowers or goes below a certain
Line 261: threshold:
Line 262: Figure 8.3 – Coveralls coverage reporting
Line 263: Now that we have our coverage reporting in place, we can move on to taking a look at the
Line 264: other principal plugins that are available for PyTest.
Line 265: Using pytest-benchmark for benchmarking
Line 266: Another frequent need when writing applications used by many users is to make sure that
Line 267: they perform in a reasonable way and, hence, that our users don't have to wait too long for
Line 268: something to happen. This is usually achieved by benchmarking core paths of our code
Line 269: base to make sure that slowdowns aren't introduced in those functions and methods. Once
Line 270: we have a good benchmark suite, all we have to do is rerun it on every code change and
Line 271: compare the results to previous runs. If nothing got slower, we are good to go.
Line 272: 
Line 273: --- 페이지 207 ---
Line 274: PyTest Essential Plugins
Line 275: Chapter 8
Line 276: [ 197 ]
Line 277: PyTest has a pytest-benchmark plugin that makes it easy to create and run benchmarks
Line 278: as parts of our test suite. Like any other Python distribution, we can install pytest-
Line 279: benchmark through pip:
Line 280: $ pip install pytest-benchmark
Line 281: Once we have it installed, we can start organizing our benchmarks in their own dedicated
Line 282: directory. This way, they don't mix with tests, as usually we don't want to run benchmarks
Line 283: on every test run.
Line 284: For example, if we want to test how fast our app can load 1,000 contacts, we could create a
Line 285: benchmarks/test_persistence.py module as the home of a test_loading function
Line 286: meant to benchmark the loading of contacts:
Line 287: from contacts import Application
Line 288: def test_loading(benchmark):
Line 289:     app = Application()
Line 290:     app._contacts = [(f"Name {n}", "number") for n in range(1000)]
Line 291:     app.save()
Line 292:     benchmark(app.load)
Line 293: The benchmark fixture is provided automatically by pytest-benchmark and should be
Line 294: used to invoke the function we want to benchmark, in this case, the Application.load
Line 295: method. What your test does is create a new contacts application, and then populates it
Line 296: with a list of 1,000 contacts and saves those contacts on this list. This ensures that we have
Line 297: local contacts to load back.
Line 298: Then, we can benchmark how long it takes to load back those same contacts, as
Line 299: benchmark(app.load) is going to invoke app.load(), measuring how long it takes to
Line 300: run it. To run our benchmarks, we can just run them like any other PyTest suite. Running
Line 301: pytest benchmarks is enough to get our benchmarks report:
Line 302: $ pytest -v benchmarks
Line 303: ...
Line 304: benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False
Line 305: min_rounds=1 min_time=0.000005 max_time=1.0 calibration_precision=10
Line 306: warmup=False warmup_iterations=100000)
Line 307: benchmarks/test_persistence.py::test_loading PASSED [100%]
Line 308: -------------------------- benchmark: 1 tests --------------------------
Line 309: Name (time in us)   Min     Max        Mean  ...   OPS (Kops/s)   Rounds
Line 310: ------------------------------------------------------------------------
Line 311: 
Line 312: --- 페이지 208 ---
Line 313: PyTest Essential Plugins
Line 314: Chapter 8
Line 315: [ 198 ]
Line 316: test_loading        714.7   22,312.3   950.7 ...   1.0518         877
Line 317: ------------------------------------------------------------------------
Line 318: ==================== 1 passed in 1.96s ====================
Line 319: Running our benchmarks allows us to know that loading back 1,000 contacts takes a
Line 320: minimum of 0.7 milliseconds, a maximum of 22 milliseconds, and an average of 0.9
Line 321: milliseconds. In total, we can load back 1,000 contacts exactly 1,051 times in a second.
Line 322: pytest-benchmark actually provides much more information about our benchmark run, but
Line 323: for the sake of readability, some of those metrics were excluded in the previously reported
Line 324: run.
Line 325: How did pytest-benchmark know those metrics? Well, it runs our function 877 times. When
Line 326: dealing with benchmarks, running them only once is usually not enough to get a solid
Line 327: result. If the function is very fast, operative system context switches might weigh on the
Line 328: execution time significantly, and so might provide false results where the time we get is
Line 329: actually heavily influenced by the fact that our system was busy.
Line 330: pytest-benchmark will decide automatically whether it's necessary to run a benchmark
Line 331: more than once because it's too fast. This is to guarantee that we can get a fairly stable
Line 332: benchmark report even when a very fast function is under the benchmark (and so its
Line 333: execution time can be heavily influenced by system load).
Line 334: At a minimum, pytest-benchmark will run a function five times before declaring how fast it
Line 335: is. If we have very slow benchmarks and we want them to run no more than once, we can
Line 336: provide the --benchmark-min-rounds=1 option.
Line 337: Comparing benchmark runs
Line 338: Now that we know how to run benchmarks, we need to be able to understand whether
Line 339: they got slower compared with previous runs. This can be done by providing --
Line 340: benchmark-autosave --benchmark-compare options to PyTest.
Line 341: The --benchmark-autosave option will make sure that every benchmark run we perform
Line 342: gets saved in a .benchmarks directory. This way, they are all available for future reference,
Line 343: and then the --benchmark-compare option will tell pytest-benchmark to compare the
Line 344: current run to the one saved previously.
Line 345: This is a convenient built-in functionality compared to coverage reporting where, in order
Line 346: to ensure non-decreasing coverage, we had to rely on an additional service or implement
Line 347: the check ourselves.
Line 348: 
Line 349: --- 페이지 209 ---
Line 350: PyTest Essential Plugins
Line 351: Chapter 8
Line 352: [ 199 ]
Line 353: The result of running with --benchmark-compare is a report where both runs are
Line 354: provided for comparison:
Line 355: -------------------------- benchmark: 2 tests --------------------------
Line 356: Name (time in us)           Min          Max          Mean          ...
Line 357: ------------------------------------------------------------------------
Line 358: test_loading (0002_371810a) 726.9 (1.0)  23,884 (1.0)  956.7 (1.0)  ...
Line 359: test_loading (NOW)          730.1 (1.00) 24,117 (1.01) 969.6 (1.01) ...
Line 360: ------------------------------------------------------------------------
Line 361: For example, in this example, we can see that the previous run (0002_371810a) is as fast as
Line 362: the current one (NOW), so our code didn't get any slower. If our code base did get slower,
Line 363: pytest-benchmark doesn't only tell us that the performance worsened. It also allows us to
Line 364: know what the bottleneck in our code base is by using the --benchmark-
Line 365: cprofile=tottime option.
Line 366: For example, running our loading benchmark with --benchmark-cprofile=tottime
Line 367: will tell us that, as expected, the majority of the time in our Application.load function is
Line 368: actually spent reading JSON:
Line 369: test_persistence.py::test_loading (NOW)
Line 370: ncalls tottime percall cumtime percall filename:lineno(function)
Line 371: 1      0.0004  0.0004  0.0004  0.0004 .../json/decoder.py:343(raw_decode)
Line 372: 1      0.0002  0.0002  0.0002  0.0002 contacts/__init__.py:43(<listcomp>)
Line 373: 1      0.0001  0.0001  0.0009  0.0009 contacts/__init__.py:40(load)
Line 374: Thanks to the performance tests, we have a good understanding of how quick our
Line 375: application can load contacts and where the time loading contacts is spent. This should
Line 376: allow us to evolve it while making sure we don't stray too far from the current
Line 377: performance.
Line 378: Using flaky to rerun unstable tests
Line 379: A problem that developers frequently start encountering with fairly big projects that need
Line 380: to involve third-party services, networking, and concurrency is that it becomes hard to
Line 381: ensure that tests that integrate many components behave in a predictable way.
Line 382: Sometimes, tests might fail just because a component responded later than usual or a
Line 383: thread moved forward before another one. Those are things our tests should be designed to
Line 384: prevent and avoid by making sure the test execution is fully predictable, but sometimes it's
Line 385: not easy to notice that we are testing something that exhibits unstable behavior.
Line 386: 
Line 387: --- 페이지 210 ---
Line 388: PyTest Essential Plugins
Line 389: Chapter 8
Line 390: [ 200 ]
Line 391: For example, you might be writing an end-to-end test where you are loading a web page to
Line 392: click a button, but at the time you try to click the button, the button itself might not have
Line 393: appeared yet.
Line 394: Those kinds of tests that sometimes fail randomly are called "flaky" and are usually caused
Line 395: by a piece of the system that is not under the control of the test itself. When possible, it's
Line 396: usually best to put that part of the system under control of the test or replace it with a fake
Line 397: implementation that can be controlled. But when it's not possible, the best we can do is to
Line 398: retry the test.
Line 399: The flaky plugin does that for us. It will automatically retry tests that fail until they pass
Line 400: or up to a maximum number of attempts. An example of such tests is when concurrency is
Line 401: involved. For example, we might write a function that appends entries to a list using
Line 402: threading:
Line 403: def flaky_appender(l, numbers):
Line 404:     from multiprocessing.pool import ThreadPool
Line 405:     with ThreadPool(5) as pool:
Line 406:         pool.map(lambda n: l.append(n), numbers)
Line 407: The test for such a function would probably just check that all the items provided are
Line 408: correctly appended to the list:
Line 409: def test_appender():
Line 410:     l = []
Line 411:     flaky_appender(l, range(7000))
Line 412:     assert l == list(range(7000))
Line 413: Running the test would probably succeed most of the time:
Line 414: $ pytest tests/unit/test_flaky.py -q
Line 415: tests/unit/test_flaky.py::test_appender PASSED
Line 416: So we might think that our function works OK, but then we start seeing that sometimes, the
Line 417: test fails for no apparent reason.
Line 418: At this point, we can install the flaky plugin to handle our flaky test:
Line 419: $ pip install flaky
Line 420: 
Line 421: --- 페이지 211 ---
Line 422: PyTest Essential Plugins
Line 423: Chapter 8
Line 424: [ 201 ]
Line 425: The first thing we can do is to confirm whether our test is actually flaky by running it
Line 426: multiple times in a row and checking whether it always succeeds. That's something the
Line 427: flaky plugin can do for us through the --min-passes option:
Line 428: $ pytest test_flaky.py --force-flaky --min-passes=10 --max-runs=10
Line 429: test_appender failed; it passed 9 out of the required 10 times.
Line 430:         <class 'AssertionError'>
Line 431:         assert [0, 1, 2, 3, 4, 5, ...] == [0, 1, 2, 3, 4, 5, ...]
Line 432:   At index 5345 diff: 5600 != 5345
Line 433: As expected, our test succeeded on nine runs, but then failed on the 10
Line 434: th, which confirms
Line 435: that it's a flaky test.
Line 436: Every time it fails, our entire release process is blocked and we have to rerun the tests and
Line 437: wait for them to complete again. If this happens frequently, it can get frustrating. That's
Line 438: where flaky becomes handy. We can decorate the test with the @flaky decorator to mark
Line 439: it as a flaky test:
Line 440: from flaky import flaky
Line 441: @flaky
Line 442: def test_appender():
Line 443:     l = []
Line 444:     flaky_appender(l, range(7000))
Line 445:     assert l == list(range(7000))
Line 446: Now that our test is marked as a flaky one, whenever pytest fails to run it, it will simply
Line 447: retry it, twice by default, but we can control it with the --max-runs option:
Line 448: $ pytest tests/unit/test_flaky.py -v
Line 449: test_appender failed (1 runs remaining out of 2).
Line 450: ...
Line 451: test_appender passed 1 out of the required 1 times. Success!
Line 452: In the previous code snippet, our test failed the first run, but flaky noticed that it still had
Line 453: one more try to go out of the default figure of two and retried. Then, on the second try, the
Line 454: test succeeded and PyTest continued.
Line 455: This allows us to quarantine our flaky tests. We can mark them as flaky and have them not
Line 456: block our release process while we work on providing a more complete solution.
Line 457: It's usually a good idea to immediately mark as flaky any test that we see unexpectedly fail
Line 458: even just once (unless it's due to a real bug) and then have some dedicated time at which
Line 459: we go through all our flaky tests, trying to unflake them by making the tests more
Line 460: predictable.
Line 461: 
Line 462: --- 페이지 212 ---
Line 463: PyTest Essential Plugins
Line 464: Chapter 8
Line 465: [ 202 ]
Line 466: Some people prefer to skip the tests that they quarantine, but (while being more robust than
Line 467: marking them as flaky) this means that you are willing to live with the risk of introducing
Line 468: any bugs those tests were meant to catch. So, flaky is usually a safer solution and the
Line 469: important part is to have some dedicated time to go back to those quarantined tests to fix
Line 470: them.
Line 471: Using pytest-testmon to rerun tests on code
Line 472: changes
Line 473: In a fairly big project, rerunning the whole test suite can take a while, so it's not always
Line 474: feasible to rerun all tests on every code change. We might settle for rerunning all tests only
Line 475: when we commit a stable point of the code and run just a subset of them on every code
Line 476: change before we decide whether to commit our changes.
Line 477: This approach is usually naturally moved forward by developers who tend to pick a single
Line 478: test, a test case, or a subset of tests that can act as canaries for their code changes.
Line 479: For example, if I'm modifying the persistence layer of our contacts application, I would
Line 480: probably rerun all tests that involve the save or load keywords:
Line 481: $ pytest -k save -k load --ignore benchmarks -v
Line 482: ...
Line 483: tests/functional/test_basic.py::TestStorage::test_reload PASSED [ 50%]
Line 484: tests/unit/test_persistence.py::TestLoading::test_load PASSED [100%]
Line 485: Once those canary tests pass, I would rerun the whole test suite to confirm that I actually
Line 486: haven't broken anything and I can commit the relevant code. If there are issues, I would
Line 487: obviously catch them when I run the full test suite, but on a fairly big project that can take
Line 488: tens of minutes, it's not a convenient way to catch errors, and the earlier I'm able to catch
Line 489: any errors, the faster I'll be at releasing my code as I don't have to wait for the full test suite
Line 490: to run on every change.
Line 491: In our case, would just rerunning the tests that have the load and save keyword in them
Line 492: be enough to catch all possible issues and thus require us to rerun the whole test suite only
Line 493: once as we are very confident that it will pass?
Line 494: Probably not. There are quite a few more tests that invoke the persistence layer and don't
Line 495: have those keywords in their name. Also, we might not always be so lucky as to have a set
Line 496: of keywords we can use to pick a set of canary tests for every change we do. That's where
Line 497: pytest-testmon comes in handy.
Line 498: 
Line 499: --- 페이지 213 ---
Line 500: PyTest Essential Plugins
Line 501: Chapter 8
Line 502: [ 203 ]
Line 503: pytest-testmon will build a graph of relationships between all our code functions and
Line 504: then, on subsequent runs, we can tell testmon to only run the tests that are influenced by
Line 505: the code we change.
Line 506: Ensure testmon is installed, as follows:
Line 507: $ pip install pytest-testmon
Line 508: We can do the first run of our test suite to build the relationship graph between the code
Line 509: and tests:
Line 510: $ pytest --testmon --ignore=benchmarks
Line 511: ================== test session starts ===================
Line 512: ...
Line 513: testmon: new DB, environment: default
Line 514: ...
Line 515: collected 25 items
Line 516: ...
Line 517: ================== 25 passed in 2.67s ===================
Line 518: Then, we can change any function of our persistence layer (for example, let's just add
Line 519: return None at the end of the Application.save function), as follows:
Line 520:     def save(self):
Line 521:         with open("./contacts.json", "w+") as f:
Line 522:             json.dump({"_contacts": self._contacts}, f)
Line 523:         return None
Line 524: And then we can rerun all the tests that are somehow related to saving data by rerunning
Line 525: testmon again:
Line 526: $ pytest --testmon --ignore=benchmarks
Line 527: ================== test session starts ===================
Line 528: ...
Line 529: testmon: new DB, environment: default
Line 530: ...
Line 531: collected 16 items / 14 deselected / 2 selected
Line 532: tests/unit/test_persistence.py . [ 9%]
Line 533: tests/unit/test_adding.py ... [ 36%]
Line 534: tests/acceptance/test_adding.py .. [ 54%]
Line 535: tests/functional/test_basic.py .. [ 72%]
Line 536: tests/acceptance/test_list_contacts.py . [ 81%]
Line 537: tests/acceptance/test_delete_contact.py . [ 90%]
Line 538: tests/acceptance/test_list_contacts.py . [100%]
Line 539: =========== 11 passed, 14 deselected in 1.30s ============
Line 540: 
Line 541: --- 페이지 214 ---
Line 542: PyTest Essential Plugins
Line 543: Chapter 8
Line 544: [ 204 ]
Line 545: In this second run, you can see that instead of running all 25 tests that we had, testmon
Line 546: only picked 11 of them, those that somehow invoked the Application.save method
Line 547: directly or indirectly, in other words, those that might end up being broken by a change to
Line 548: the method.
Line 549: Every time we rerun pytest with the --testmon option, only the tests related to the code
Line 550: that we have changed will be rerun. If we try to run pytest --testmon again, for
Line 551: example, no tests would be run as we haven't changed anything from the previous run:
Line 552: $ pytest --testmon --ignore=benchmarks
Line 553: ================== test session starts ===================
Line 554: ...
Line 555: testmon: new DB, environment: default
Line 556: ...
Line 557: collected 0 items / 25 deselected
Line 558: ================= 25 deselected in 0.14s ==================
Line 559: This is a convenient way to pick only those tests that are related to our recent code changes
Line 560: and to verify our code on every code change without having to rerun the entire test suite or
Line 561: guess which tests might need to be checked again.
Line 562: It should be remembered, by the way, that if the behavior of the code
Line 563: depends on configuration files or data saved on disk or on a database,
Line 564: then testmon can't detect that tests have to be rerun to verify the behavior
Line 565: again when those change. In general, by the way, having your test suite
Line 566: depend on the state of external components is not a robust approach, so
Line 567: it's better to make sure that your fixtures take care of setting up a fresh
Line 568: state on every run.
Line 569: Running tests in parallel with pytest-xdist
Line 570: As your test suite gets bigger and bigger, it might start taking too long to run. Even if
Line 571: strategies to reduce the number of times you need to run the whole test suite are in place,
Line 572: there will be a time where you want all your tests to run and act as the gatekeeper of your
Line 573: releases.
Line 574: Hence, a slow test suite can actually impair the speed at which we are able to develop and
Line 575: release software.
Line 576: 
Line 577: --- 페이지 215 ---
Line 578: PyTest Essential Plugins
Line 579: Chapter 8
Line 580: [ 205 ]
Line 581: While great care must always be taken to ensure that our tests are written in the fastest
Line 582: possible way (avoid throwing time.sleep calls everywhere, they can be very good at
Line 583: hiding themselves in the most unexpected places), slow components of the software that
Line 584: we are testing should be replaced with fake implementations every time so that it is
Line 585: possible that we can get to a point where there isn't much else we can do and making our
Line 586: test suite faster would be too complex or expensive.
Line 587: When we get to that point, if we wrote our tests such that they are properly isolated (the
Line 588: state of one test doesn't influence or depend on the state of another test), a possible
Line 589: direction to pursue is to parallelize the execution of our tests.
Line 590: That's exactly what we can achieve by installing the pytest-xdist plugin:
Line 591: $ pip install pytest-xdist
Line 592: Once xdist is available, our tests can be run using multiple concurrent workers with the -
Line 593: n numprocesses option:
Line 594: $ pytest -n 2
Line 595: =========== test session starts ==========
Line 596: ...
Line 597: gw0 [26] / gw1 [26]
Line 598: .......................... [100%]
Line 599: ============ 26 passed in 2.71s ==========
Line 600: With -n 2, two workers were started for our tests (gw0 and gw1) and tests were equally
Line 601: distributed between the two. Nearly half of the tests should have gone to gw0 and the other
Line 602: half to gw1 (PyTest doesn't actually divide the tests equally; it depends on how fast they are
Line 603: to run, but in general, anticipating that tests are equally split is a good approximation).
Line 604: Note that as benchmarks can't provide reliable results when run
Line 605: concurrently, pytest-benchmark will disable benchmarking when the -n
Line 606: option is provided. The benchmarks will run as normal tests, so you
Line 607: might want to just skip them by explicitly pointing PyTest to the tests
Line 608: directory only, or by using --ignore benchmarks.
Line 609: We can see how tests are distributed simply by running pytest in verbose mode with -v.
Line 610: In verbose mode, near to every test, we will see which worker was in charge of executing
Line 611: the test:
Line 612: ...
Line 613: [gw0] [ 12%] PASSED test_adding.py::TestAddingEntries::test_basic
Line 614: [gw1] [ 16%] PASSED test_main.py::TestMain::test_main
Line 615: ...
Line 616: 
Line 617: --- 페이지 216 ---
Line 618: PyTest Essential Plugins
Line 619: Chapter 8
Line 620: [ 206 ]
Line 621: If you are unsure about how many workers to start, the -n option also accepts the value
Line 622: "auto", which will detect how many processes to start based on how many CPUs the
Line 623: system has.
Line 624: It is, by the way, important to note that if the test suite is very fast and runs in just a matter
Line 625: of seconds, running it in parallel might actually just make it slower. Distributing the tests
Line 626: across different workers and starting them involves some extra work.
Line 627: Summary
Line 628: In this chapter, we saw the most frequently used plugins that exist for PyTest, those plugins
Line 629: that can make your life easier by taking charge of some frequent needs that nearly every
Line 630: test suite will face.
Line 631: But there isn't any PyTest plugin that is able to manage the test environment itself. We are
Line 632: still forced to set up manually all dependencies that the tests have and ensure that the
Line 633: correct versions of Python are available to run the tests.
Line 634: It would be great if there was a PyTest plugin able to install everything that we need in
Line 635: order to run our test suite and just "run tests" on a new environment. Well, the good news
Line 636: is that it exists; it's not strictly a PyTest plugin, but it's what Tox, which we are going to
Line 637: introduce in the next chapter, was designed for.