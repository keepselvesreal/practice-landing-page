Line 1: 
Line 2: --- 페이지 217 ---
Line 3: 9
Line 4: Managing Test Environments
Line 5: with Tox
Line 6: In the previous chapter, we covered the most frequently used PyTest plugins. Through
Line 7: them, we are able to manage our test suite within a Python environment. We can configure
Line 8: how the test suite should work, as well as enable coverage reporting, benchmarking, and
Line 9: many more features that make it convenient to work with our tests. But what we can't do is
Line 10: manage the Python environment itself within which the test suite runs.
Line 11: Tox was invented precisely for that purpose; managing Python versions and the
Line 12: environment that we need to run our tests. Tox takes care of setting up the libraries and
Line 13: frameworks we need for our test suite to run and will check our tests on all Python versions
Line 14: that are available.
Line 15: In this chapter, we will cover the following topics:
Line 16: Introducing Tox
Line 17: Testing multiple Python versions with Tox
Line 18: Using Tox with Travis
Line 19: Technical requirements
Line 20: We need a working Python interpreter along with Tox. Tox can be installed with the
Line 21: following command:
Line 22: $ pip install tox
Line 23: Even though we are going to use the same test suite and contacts app we wrote in Chapter
Line 24: 8, PyTest Essential Plugins, we only need to install Tox 3.20.0. All other dependencies will be
Line 25: managed by Tox for us.
Line 26: 
Line 27: --- 페이지 218 ---
Line 28: Managing Test Environments with Tox
Line 29: Chapter 9
Line 30: [ 208 ]
Line 31: You can find the code files present in this chapter on GitHub at
Line 32: https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python/tr
Line 33: ee/main/Chapter09.
Line 34: Introducing Tox
Line 35: Tox is a virtual environment manager for Python. It takes care of creating the environments
Line 36: and installing our project and all its dependencies on multiple Python versions.
Line 37: It is a convenient tool that can automate the setup of our project environment and abstract
Line 38: it in a way that we can reuse the same command both locally and in our Continuous
Line 39: Integration (CI) pipeline to set up our project and run its tests. It also does that on multiple
Line 40: Python versions at the same time, so that we can check that our project works on all of
Line 41: them.
Line 42: Testing multiple Python versions can be very convenient when you need to upgrade from
Line 43: one version to the next. Before switching all your systems to the new one, you want to
Line 44: ensure that your code is still able to work on both the old and new versions, so that you can
Line 45: perform a phased rollout.
Line 46: If we take our contacts application example from Chapter 8, PyTest Essential Plugins, the
Line 47: test suite required many dependencies to run. We needed flaky to manage flaky tests,
Line 48: pytest-benchmark for the benchmarks suite, pytest-bdd for the acceptance
Line 49: tests, pytest-cov to ensure that the code coverage was verified, and obviously pytest
Line 50: itself to run the test suite.
Line 51: If we had to remember to tell all our colleagues working on the same project to install those
Line 52: packages, it would be easy to forget some of them or end up with incorrect versions
Line 53: installed. We could document our test dependencies, but even better would be to have
Line 54: them managed automatically for us.
Line 55: So, let's create a tox.ini file in our project directory, telling Tox where to find the project
Line 56: to test, which dependencies are necessary to run the test suite, and how to run it:
Line 57: [tox]
Line 58: setupdir = ./src
Line 59: [testenv]
Line 60: deps =
Line 61:     pytest == 6.0.2
Line 62:     pytest-bdd == 3.4.0
Line 63:     flaky == 3.7.0
Line 64:     pytest-benchmark == 3.2.3
Line 65: 
Line 66: --- 페이지 219 ---
Line 67: Managing Test Environments with Tox
Line 68: Chapter 9
Line 69: [ 209 ]
Line 70:     pytest-cov == 2.10.1
Line 71: commands =
Line 72:     pytest --cov=contacts
Line 73: The [tox] section configures Tox itself. In this case, it can ascertain through the setupdir
Line 74: = option where to find the project that is under test.
Line 75: The [testenv] section is instead meant to provide directives for each environment in
Line 76: which we want to test our project. In this case, through the deps = option, we are listing all
Line 77: things that need to be installed in that environment so that the project can be tested (the
Line 78: project itself is always automatically installed by Tox, so no need to list it here), and by
Line 79: using the commands = options, we are telling Tox how to test the project in the
Line 80: environments.
Line 81: Once this file is in place in the root of our project, we can prepare a fully working
Line 82: environment and test the project by simply invoking the tox command:
Line 83: $ tox
Line 84: GLOB sdist-make: ./src/setup.py
Line 85: python create: ./.tox/python
Line 86: python installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
Line 87: pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
Line 88: python inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
Line 89: python installed: ...
Line 90: python run-test: commands[0] | pytest --cov=contacts
Line 91: ====================== test session starts ======================
Line 92: ...
Line 93: collected 26 items
Line 94: tests/acceptance/test_delete_contact.py . [ 3%]
Line 95: tests/acceptance/test_list_contacts.py .. [ 11%]
Line 96: benchmarks/test_persistence.py . [ 15%]
Line 97: tests/acceptance/test_adding.py .. [ 23%]
Line 98: tests/functional/test_basic.py ... [ 34%]
Line 99: tests/functional/test_main.py . [ 38%]
Line 100: tests/unit/test_adding.py ...... [ 61%]
Line 101: tests/unit/test_application.py ....... [ 88%]
Line 102: tests/unit/test_flaky.py . [ 92%]
Line 103: tests/unit/test_persistence.py .. [100%]
Line 104: ----------- coverage: platform linux, python 3.7.3-final-0 -----------
Line 105: Name                  Stmts Miss Cover
Line 106: ----------------------------------------------------------------------
Line 107: contacts/__init__.py  51    0    100%
Line 108: contacts/__main__.py  0     0    100%
Line 109: ----------------------------------------------------------------------
Line 110: TOTAL                 51    0    100%
Line 111: 
Line 112: --- 페이지 220 ---
Line 113: Managing Test Environments with Tox
Line 114: Chapter 9
Line 115: [ 210 ]
Line 116: -------------------------- benchmark: 1 tests --------------------------
Line 117: Name (time in us) Min Max Mean ... OPS (Kops/s) Rounds
Line 118: ------------------------------------------------------------------------
Line 119: test_loading 714.7 22,312.3 950.7 ... 1.0518 877
Line 120: ------------------------------------------------------------------------
Line 121: ====================== 26 passed in 2.41s ======================
Line 122: As you can see, Tox created a new Python environment in ./tox /python, installed our
Line 123: project and all the required dependencies for us, and then started the test suite providing
Line 124: coverage and benchmarks.
Line 125: The side effect of this approach is that we lost a bit of flexibility in terms of what we can tell
Line 126: PyTest. Tox is going to run all our tests and benchmarks. If we only want to run some of
Line 127: them, there is no way of doing this.
Line 128: This flexibility can be regained by using the Tox {posargs} variable, which will proxy all
Line 129: options we provide in the command line from Tox to our test suite. So we can put
Line 130: {posargs} in our commands option in tox.ini so that any additional option we provide
Line 131: to Tox gets forwarded to our test command:
Line 132: commands =
Line 133:     pytest --cov=contacts {posargs}
Line 134: Now, if we run Tox with any additional option after --, it will be forwarded to PyTest. For
Line 135: example, to exclude benchmarks from our run, we can use tox -- ./tests to exclude
Line 136: benchmarks and only run the tests that are related to loading back our contacts. Instead, we
Line 137: can use tox -- ./tests -k load:
Line 138: $ tox -- ./tests -k load
Line 139: ...
Line 140: ============= test session starts =============
Line 141: collected 25 items / 23 deselected / 2 selected
Line 142: tests/functional/test_basic.py . [ 50%]
Line 143: tests/unit/test_persistence.py . [100%]
Line 144: ...
Line 145: ====== 2 passed, 23 deselected in 0.35s =======
Line 146: Now that we know how to use Tox to set up the testing environment without losing the
Line 147: flexibility that was afforded to us earlier when we did things manually, we can move
Line 148: forward and see how to actually set up multiple testing environments on different versions
Line 149: of Python.
Line 150: 
Line 151: --- 페이지 221 ---
Line 152: Managing Test Environments with Tox
Line 153: Chapter 9
Line 154: [ 211 ]
Line 155: Testing multiple Python versions with Tox
Line 156: Tox is based on the concept of environments. The goal of Tox is to prepare those 
Line 157: environments where it will run the commands provided. Usually, those environments are
Line 158: meant for testing (running tests in different conditions) and the most common kind of
Line 159: environments are those that use different Python versions. But in theory, it is possible to
Line 160: create a different environment for any other purpose. For example, we frequently create an
Line 161: environment where project documentation is built.
Line 162: To add further environments to Tox, it's sufficient to list them inside the envlist = option.
Line 163: To configure two environments that test our project against both Python 2.7 and Python
Line 164: 3.7, we can set envlist to both py37 and py27:
Line 165: [tox]
Line 166: setupdir = ./src
Line 167: envlist = py27, py37
Line 168: If we run tox again, we will see that it will now test our project on two different
Line 169: environments, one made for Python 2.7 and one for Python 3.7:
Line 170: $ tox
Line 171: GLOB sdist-make: ./src/setup.py
Line 172: py27 create: ./.tox/py27
Line 173: py27 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
Line 174: pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
Line 175: ...
Line 176: py37 create: ./.tox/py37
Line 177: py37 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
Line 178: pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
Line 179: We obviously need to have working executables of those two Python versions on our
Line 180: system, but as far as they are available and running the python3.7 and python2.7
Line 181: commands works, Tox will be able to leverage them.
Line 182: By default, all environments apply the same configuration, the one provided in [testenv],
Line 183: so in our case, Tox tried to install the same exact dependencies and run the same exact
Line 184: commands on both Python 2.7 and Python 3.7.
Line 185: 
Line 186: --- 페이지 222 ---
Line 187: Managing Test Environments with Tox
Line 188: Chapter 9
Line 189: [ 212 ]
Line 190: On Python 2.7, it failed because PyTest no longer supports Python 2.7 on versions after
Line 191: 4.6.11, so if we want to actually test our project on Python 2.7, we need to provide a custom
Line 192: configuration for the environment and make it work against a previous PyTest version:
Line 193: py27 create: ./.tox/py27
Line 194: py27 installdeps: pytest == 6.0.2, pytest-bdd == 3.4.0, flaky == 3.7.0,
Line 195: pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
Line 196: ERROR: Could not find a version that satisfies the requirement
Line 197: pytest==6.0.2 (from versions: 2.0.0, ..., 4.6.11)
Line 198: ERROR: No matching distribution found for pytest==6.0.2
Line 199: To fix this issue, we can simply go back and provide a custom configuration for the Python
Line 200: 2.7 environment where we are going to customize the deps = option, stating explicitly that
Line 201: on that version of Python, we want to use a previous PyTest version:
Line 202: [testenv:py27]
Line 203: deps =
Line 204:     pytest == 4.6.11
Line 205:     pytest-bdd == 3.4.0
Line 206:     flaky == 3.7.0
Line 207:     pytest-benchmark == 3.2.3
Line 208:     pytest-cov == 2.10.1
Line 209: Options can be specialized just by creating a section named [testenv:envname], in this
Line 210: case, [testenv:py27], as we want to override the options for the py27 environment.
Line 211: Any option that isn't specified is inherited from the generic [testenv] configuration, so as
Line 212: we haven't overridden the command = option, the configuration we provided in
Line 213: [testenv] will be used for testing on Python 2.7, too.
Line 214: By running Tox with this new configuration, we will finally be able to set up the
Line 215: environment, install PyTest, and start our tests:
Line 216: $ tox
Line 217: GLOB sdist-make: ./09_tox/src/setup.py
Line 218: py27 create: ./09_tox/.tox/py27
Line 219: py27 installdeps: pytest == 4.6.11, pytest-bdd == 3.4.0, flaky == 3.7.0,
Line 220: pytest-benchmark == 3.2.3, pytest-cov == 2.10.1
Line 221: py27 inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
Line 222: py27 installed: contacts @
Line 223: file://./.tox/.tmp/package/1/contacts-0.0.0.zip,pytest==4.6.11,...
Line 224: py27 run-test-pre: PYTHONHASHSEED='2140925334'
Line 225: py27 run-test: commands[0] | pytest --cov=contacts
Line 226: 
Line 227: --- 페이지 223 ---
Line 228: Managing Test Environments with Tox
Line 229: Chapter 9
Line 230: [ 213 ]
Line 231: As we could have anticipated, our tests fail on Python 2.7 as our project wasn't written to
Line 232: support such an old Python version:
Line 233: platform linux2 -- Python 2.7.16, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
Line 234: cachedir: .tox/py27/.pytest_cache
Line 235: rootdir: .
Line 236: plugins: bdd-3.4.0, flaky-3.7.0, benchmark-3.2.3, cov-2.10.1
Line 237: collected 5 items / 7 errors
Line 238: ================ ERRORS ===================
Line 239:     mod = self.fspath.pyimport(ensuresyspath=importmode)
Line 240: .tox/py27/lib/python2.7/site-packages/py/_path/local.py:704: in pyimport
Line 241:     __import__(modname)
Line 242: E File "./benchmarks/test_persistence.py", line 5
Line 243: E app._contacts = [(f"Name {n}", "number") for n in range(1000)]
Line 244: E                             ^
Line 245: E SyntaxError: invalid syntax
Line 246: ========== 7 error in 1.07 seconds ========
Line 247: For example, we used f-strings, which were not supported on Python 2.7. Porting projects
Line 248: to Python 2.7 is beyond the scope of this book, so we are not going to modify our project to
Line 249: make it work there, but the same concepts that we have seen while using Python 2.7 do
Line 250: apply to any other environment.
Line 251: For example, if, instead of Python 2.7, we wanted to test our project against Python 3.8, we
Line 252: could have just used py38 instead of py27 as the name of the environment. In that case, we
Line 253: wouldn't even have to customize the deps = option for that environment as PyTest 6
Line 254: works fine on Python 3.8.
Line 255: Using environments for more than Python
Line 256: versions
Line 257: By default, Tox provides a few predefined environments for various Python versions, but
Line 258: we can declare any kind of environment that differs for whatever reason.
Line 259: Another common way to use this capability is to create various environments that differ for
Line 260: the commands = option, and so do totally different things. You will probably frequently see
Line 261: that this used to provide a way to build project documentation. It is not uncommon to see a
Line 262: docs environment in Tox configurations that, instead of running tests, builds the project
Line 263: documentation.
Line 264: In our case, we might want to use this feature to disable benchmarks by default and make
Line 265: them run only when a dedicated environment is used.
Line 266: 
Line 267: --- 페이지 224 ---
Line 268: Managing Test Environments with Tox
Line 269: Chapter 9
Line 270: [ 214 ]
Line 271: To do so, we are going to disable benchmarks by default in our [testenv] configuration:
Line 272: [tox]
Line 273: setupdir = ./src
Line 274: envlist = py27, py37
Line 275: [testenv]
Line 276: deps =
Line 277:     pytest == 6.0.2
Line 278:     pytest-bdd == 3.4.0
Line 279:     flaky == 3.7.0
Line 280:     pytest-benchmark == 3.2.3
Line 281:     pytest-cov == 2.10.1
Line 282: commands =
Line 283:     pytest --cov=contacts --benchmark-skip {posargs}
Line 284: [testenv:py27]
Line 285: ...
Line 286: Then we are going to add one more [testenv:benchmarks] environment that runs only
Line 287: the benchmarks:
Line 288: [testenv:benchmarks]
Line 289: commands =
Line 290:     pytest --no-cov ./benchmarks {posargs}
Line 291: This environment will inherit the configuration from our default environment, and thus
Line 292: will use the same exact deps, but will provide a custom command where coverage is
Line 293: disabled and only benchmarks are run.
Line 294: It is important that we don't list this environment in the envlist option of the [tox]
Line 295: section. Otherwise, the benchmarks would end up being run every time we invoke Tox,
Line 296: which is not what we want.
Line 297: To explicitly run benchmarks on demand, we can run Tox with the -e benchmarks option,
Line 298: which will run Tox just for that specific environment:
Line 299: $ tox -e benchmarks
Line 300: GLOB sdist-make: ./src/setup.py
Line 301: benchmarks create: ./.tox/benchmarks
Line 302: benchmarks installdeps: pytest == 6.0.2, pytest-benchmark == 3.2.3, ...
Line 303: benchmarks inst: ./.tox/.tmp/package/1/contacts-0.0.0.zip
Line 304: benchmarks run-test-pre: PYTHONHASHSEED='257991845'
Line 305: benchmarks run-test: commands[0] | pytest --no-cov ./benchmarks
Line 306: ======================= test session starts =======================
Line 307: platform linux -- Python 3.7.3, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 308: collected 1 item
Line 309: 
Line 310: --- 페이지 225 ---
Line 311: Managing Test Environments with Tox
Line 312: Chapter 9
Line 313: [ 215 ]
Line 314: benchmarks/test_persistence.py .                       [100%]
Line 315: -------------------------- benchmark: 1 tests --------------------------
Line 316: Name (time in us) Min Max Mean ... OPS (Kops/s) Rounds
Line 317: ------------------------------------------------------------------------
Line 318: test_loading 714.7 22,312.3 950.7 ... 1.0518 877
Line 319: ------------------------------------------------------------------------
Line 320: ======================= 1 passed in 1.73s  =======================
Line 321: We now have a configuration where running tox by default will run our tests on Python
Line 322: 2.7 and Python 3.7, and then running tox -e benchmarks does run benchmarks.
Line 323: If we further want to specialize the behavior of our Tox configuration, we can do so by
Line 324: adding more environments and customizing the options we care about. A complete
Line 325: reference of all the Tox options is available on the ReadTheDocs page of Tox, so make sure
Line 326: to take a look if you want to dive further into customizing Tox behavior.
Line 327: Now that we have Tox working locally, we need to combine it with our CI system to ensure
Line 328: that different CI processes are started for each Tox environment. As we have used Travis
Line 329: for all our CI needs so far, let's see how we can integrate Tox with Travis.
Line 330: Using Tox with Travis
Line 331: Using Tox with a CI environment is usually fairly simple, but as both Tox and the CI will
Line 332: probably end up wanting to manage the Python environment, some attention has to be
Line 333: paid to enable them to exist together. To see how Travis and Tox can work together, we can
Line 334: pick our chat project that we wrote in Chapter 4, Scaling the Test Suite, which we already
Line 335: had on Travis-CI, and migrate it to use Tox.
Line 336: We need to write a tox.ini file, which will take care of running the test suite itself:
Line 337: [tox]
Line 338: setupdir = ./src
Line 339: envlist = py37, py38, py39
Line 340: [testenv]
Line 341: usedevelop = true
Line 342: deps =
Line 343:     coverage
Line 344: commands =
Line 345:     coverage run --source=src -m unittest discover tests -v
Line 346:     coverage report
Line 347: 
Line 348: --- 페이지 226 ---
Line 349: Managing Test Environments with Tox
Line 350: Chapter 9
Line 351: [ 216 ]
Line 352: [testenv:benchmarks]
Line 353: commands =
Line 354:     python -m unittest discover benchmarks
Line 355: The commands you see in tox.ini are the same that we previously had in the
Line 356: travis.yml file under the script: section. That's because, previously, Travis itself was in
Line 357: charge of running our tests. Now, Tox will be in charge of doing so.
Line 358: For the same reason, as the coverage reporting should happen every time we run the test
Line 359: suite, we have Tox install the coverage dependency and run coverage report after the
Line 360: test suite.
Line 361: The main difference with tox.ini seen previously in the chapter is probably the
Line 362: usedevelop = true option. That tells Tox to install our own project in editable mode
Line 363: (sometimes called developer mode). Instead of making a distribution package out of our
Line 364: source directory and then installing the distribution, Tox will install the source directory
Line 365: itself. This is frequently convenient when coverage reporting is involved as we usually
Line 366: want the coverage to be against our source code, and not against the installed distribution.
Line 367: The benefit of using a Tox file is that it should work the same everywhere. So, before
Line 368: moving it to Travis, we can verify that it actually does what we expect locally on our own
Line 369: machine:
Line 370: $ tox
Line 371: py38 develop-inst-noop: travistest/src
Line 372: py38 run-test: commands[0] | coverage run --source=src -m unittest discover
Line 373: tests -v
Line 374: test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
Line 375: test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
Line 376: test_exchange_with_server (functional.test_chat.TestChatMessageExchange)
Line 377: ... ok
Line 378: test_many_users (functional.test_chat.TestChatMessageExchange) ... ok
Line 379: test_multiple_readers (functional.test_chat.TestChatMessageExchange) ... ok
Line 380: test_client_connection (unit.test_client.TestChatClient) ... ok
Line 381: test_client_fetch_messages (unit.test_client.TestChatClient) ... ok
Line 382: test_nickname (unit.test_client.TestChatClient) ... ok
Line 383: test_send_message (unit.test_client.TestChatClient) ... ok
Line 384: test_broadcast (unit.test_connection.TestConnection) ... ok
Line 385: ----------------------------------------------------------------------
Line 386: Ran 10 tests in 0.058s
Line 387: OK
Line 388: py38 run-test: commands[1] | coverage report
Line 389: Name Stmts Miss Cover
Line 390: ------------------------------------------
Line 391: 
Line 392: --- 페이지 227 ---
Line 393: Managing Test Environments with Tox
Line 394: Chapter 9
Line 395: [ 217 ]
Line 396: src/chat/__init__.py  0 0 100%
Line 397: src/chat/client.py   29 0 100%
Line 398: src/chat/server.py    7 0 100%
Line 399: src/setup.py          2 2 0%
Line 400: ------------------------------------------
Line 401: TOTAL                38 2 95%
Line 402: As desired, it ran the test suite and then reported the code coverage. We also know, thanks
Line 403: to [testenv:benchmarks], that if we want, we can run benchmarks with tox -e
Line 404: benchmarks:
Line 405: $ tox -e benchmarks
Line 406: benchmarks develop-inst-noop: travistest/src
Line 407: benchmarks run-test: commands[0] | python -m unittest discover benchmarks
Line 408:   time: 0.06, iteration: 0.01
Line 409: .
Line 410: ----------------------------------------------------------------------
Line 411: Ran 1 test in 0.069s
Line 412: OK
Line 413: Now, the remaining element is to make Tox run inside Travis.
Line 414: To do so, mostly we have to replace the script: section in our travis.yml file with a
Line 415: single tox command. Then, Tox will do everything it has to do in order to make the tests
Line 416: run as it did on our own PC:
Line 417: script:
Line 418:   - "tox"
Line 419: However, Travis will also need Tox itself to run the commands. Therefore, we want to have
Line 420: Travis install Tox before running the script. To do so, we are going to use a special package
Line 421: named tox-travis and we are going to add it to the install: section:
Line 422: install:
Line 423:   - "pip install tox-travis"
Line 424: You might be wondering why we used tox-travis instead of just tox. The reason is that
Line 425: tox-travis takes care of that little extra work that is necessary to make Tox and Travis
Line 426: collaborate. By default, Travis wants to install and set up Python, but Tox also wants to do
Line 427: the same. That means that we would end up installing Python twice.
Line 428: 
Line 429: --- 페이지 228 ---
Line 430: Managing Test Environments with Tox
Line 431: Chapter 9
Line 432: [ 218 ]
Line 433: Even worse, as we have envlist = py37, py38, py39 in our tox.ini, Tox would
Line 434: actually try to run the tests against all three Python versions for each Travis Python
Line 435: environment. So, suppose that we asked Travis to set up 3.7, 3.8, and 3.9. Then, Tox would
Line 436: try to use 3.7, 3.8, and 3.9 inside the Travis 3.7 Python environment, and would then try to
Line 437: use 3.7, 3.8, and 3.9 inside the Travis 3.8 Python environment, and so on, leading to errors
Line 438: such as the following:
Line 439: ERROR: py38: InterpreterNotFound: python3.8
Line 440: ERROR: py39: InterpreterNotFound: python3.9
Line 441: To avoid this problem, we can use tox-travis. When we use Tox-Travis, the Python
Line 442: environments come from Travis only and Tox will simply use those already prepared by
Line 443: Travis without trying to set up a second Python environment. At that point, our Tox
Line 444: envlist is only helpful locally, and on Travis, the python: section of the travis.yml file
Line 445: will dictate which Python versions get used.
Line 446: Apart from making sure that we install tox-travis, the rest of our travis.yml file is
Line 447: fairly similar to the original one our project had previously. We just replaced the
Line 448: commands to run tests and benchmarks with those that Tox provides:
Line 449: language: python
Line 450: os: linux
Line 451: dist: xenial
Line 452: python:
Line 453:   - 3.7
Line 454:   - &mainstream_python 3.8
Line 455:   - 3.9
Line 456:   - nightly
Line 457: install:
Line 458:   - "pip install tox-travis"
Line 459:   - "pip install coveralls"
Line 460: script:
Line 461:   - "tox"
Line 462: after_success:
Line 463:   - coveralls
Line 464:   - "tox -e benchmarks"
Line 465: Now that both our tox.ini and travis.yml configuration files are in place, we can just
Line 466: push our repository changes and see that Travis successfully runs our tests using Tox:
Line 467: 
Line 468: --- 페이지 229 ---
Line 469: Managing Test Environments with Tox
Line 470: Chapter 9
Line 471: [ 219 ]
Line 472: Figure 9.1 – Tox setup
Line 473: It should became clear that once we have a working local Tox setup, moving on to Travis
Line 474: involves very little apart from writing a travis.yml configuration file in charge of
Line 475: installing tox-travis and then invoking tox.
Line 476: Summary
Line 477: In this chapter, we saw how Tox can take care of all the setup necessary to run our tests for
Line 478: us and how it can do that on multiple target environments so that all we have to do to run
Line 479: tests is just to invoke Tox itself.
Line 480: This is a more convenient, but also robust, way to manage our test suite. The primary
Line 481: benefit is that anyone else willing to contribute to our project won't have to learn how to set
Line 482: up our projects and how to run tests. If our colleagues or project contributors are familiar
Line 483: with Tox, seeing that our project includes a tox.ini file tells them all that they will need to
Line 484: know—that they just have to invoke the tox command to run tests.
Line 485: Now that we have seen the base plugins and tools to manage and run our test suite, in the
Line 486: next chapter, we can move on to some more advanced topics that involve how to test our
Line 487: documentation itself and how to use property-based testing to catch bugs in our code.