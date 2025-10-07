Line 1: 
Line 2: --- 페이지 148 ---
Line 3: 5
Line 4: Introduction to PyTest
Line 5: In the previous chapters, we saw how to approach test-driven development, how to create
Line 6: a test suite with the unittest module, and how to organize it as it grows. While unittest
Line 7: is a very good tool and is a reliable solution for most projects, it lacks some convenient
Line 8: features that are available in more advanced testing frameworks.
Line 9: PyTest is currently the most widespread testing framework in the Python community, and
Line 10: it's mostly compatible with unittest. So it's easy to migrate from unittest to pytest if
Line 11: you feel the need for the convenience that pytest provides.
Line 12: In this chapter, we will cover the following topics:
Line 13: Running tests with PyTest
Line 14: Writing PyTest fixtures
Line 15: Managing temporary data with tmp_path
Line 16: Testing I/O with capsys
Line 17: Running subsets of the test suite
Line 18: Technical requirements
Line 19: We need a working Python interpreter with the pytest framework installed. Pytest can be
Line 20: installed with the following:
Line 21: $ pip install pytest
Line 22: The examples have been written on Python 3.7 and pytest 5.4.3 but should work on most
Line 23: modern Python versions. You can find the code files present in this chapter on GitHub
Line 24: at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-
Line 25: Python/​tree/​main/​Chapter05.
Line 26: 
Line 27: --- 페이지 149 ---
Line 28: Introduction to PyTest
Line 29: Chapter 5
Line 30: [ 139 ]
Line 31: Running tests with PyTest
Line 32: PyTest is mostly compatible with the unittest module (apart from support for subtests).
Line 33: Test suites written with unittest can be directly run under pytest with no modification
Line 34: usually. For example, our chat application test suite can be directly run under pytest by
Line 35: simply invoking pytest within the project directory:
Line 36: $ pytest -v
Line 37: ============ test session starts ============
Line 38: platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
Line 39: cachedir: .pytest_cache
Line 40: rootdir: /chatapp
Line 41: collected 11 items
Line 42: benchmarks/test_chat.py::BenchmarkChat::test_sending_messages PASSED [ 9%]
Line 43: tests/e2e/test_chat.py::TestChatAcceptance::test_message_exchange PASSED [
Line 44: 18%]
Line 45: tests/e2e/test_chat.py::TestChatAcceptance::test_smoke_sending_message
Line 46: PASSED [ 27%]
Line 47: tests/functional/test_chat.py::TestChatMessageExchange::test_exchange_with_
Line 48: server PASSED [ 36%]
Line 49: tests/functional/test_chat.py::TestChatMessageExchange::test_many_users
Line 50: PASSED [ 45%]
Line 51: tests/functional/test_chat.py::TestChatMessageExchange::test_multiple_reade
Line 52: rs PASSED [ 54%]
Line 53: tests/unit/test_client.py::TestChatClient::test_client_connection PASSED [
Line 54: 63%]
Line 55: tests/unit/test_client.py::TestChatClient::test_client_fetch_messages
Line 56: PASSED [ 72%]
Line 57: tests/unit/test_client.py::TestChatClient::test_nickname PASSED [ 81%]
Line 58: tests/unit/test_client.py::TestChatClient::test_send_message PASSED [ 90%]
Line 59: tests/unit/test_connection.py::TestConnection::test_broadcast PASSED [100%]
Line 60: ============ 11 passed in 3.63s ============
Line 61: The main difference is that pytest doesn't look for classes that inherit the
Line 62: unittest.TestCase class, but instead looks for anything that has test in the name, be it a
Line 63: module, a class, or a function. Anything named [Tt]est* is a test... but, if needed, it's
Line 64: possible to change the discovery rules by having pytest.ini inside the project directory.
Line 65: This means that even a simple function can be a test as long as it's named
Line 66: test_something, and as it won't inherit from TestCase, there is no need to use the
Line 67: custom self.assertEqual and the related method to get meaningful information on
Line 68: failed assertions. Pytest will enhance the assert statement to report as much information
Line 69: as available on the asserted expression.
Line 70: 
Line 71: --- 페이지 150 ---
Line 72: Introduction to PyTest
Line 73: Chapter 5
Line 74: [ 140 ]
Line 75: For example, we could create a very simple test suite that only has a test_simple.py
Line 76: module containing a test_something function. That would be all we need to start a test
Line 77: suite:
Line 78: def test_something():
Line 79:     a = 5
Line 80:     b = 10
Line 81:     assert a + b == 11
Line 82: Now, if we run pytest inside the same directory, it will properly find and run our test, and
Line 83: the failed assertion will also give us hints on what went wrong by telling us that a + b is
Line 84: 15 and not 11:
Line 85: $ pytest -v
Line 86: ======================= test session starts =======================
Line 87: platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
Line 88: cachedir: .pytest_cache
Line 89: rootdir: ~/HandsOnTestDrivenDevelopmentPython/05_pytest
Line 90: collected 1 item
Line 91: test_simple.py::test_something FAILED [100%]
Line 92: ============================ FAILURES =============================
Line 93: _________________________ test_something __________________________
Line 94:     def test_something():
Line 95:         a = 5
Line 96:         b = 10
Line 97: > assert a + b == 11
Line 98: E assert 15 == 11
Line 99: E +15
Line 100: E -11
Line 101: test_simple.py:4: AssertionError
Line 102: ===================== short test summary info =====================
Line 103: FAILED test_simple.py::test_something - assert 15 == 11
Line 104: ======================== 1 failed in 0.22s ========================
Line 105: We can also add more complex tests that are implemented as classes collecting multiple
Line 106: tests, without having to inherit from the TestCase class as we did for unittest test suites:
Line 107: class TestMultiple:
Line 108:     def test_first(self):
Line 109:         assert 5 == 5
Line 110:     def test_second(self):
Line 111:         assert 10 == 10
Line 112: 
Line 113: --- 페이지 151 ---
Line 114: Introduction to PyTest
Line 115: Chapter 5
Line 116: [ 141 ]
Line 117: As for the previous case where we only had the test_something test function, if we run
Line 118: pytest, it will find all three tests and it will run them:
Line 119: $ pytest -v
Line 120: ...
Line 121: collected 3 items
Line 122: test_simple.py::test_something FAILED [ 33%]
Line 123: test_simple.py::TestMultiple::test_first PASSED [ 66%]
Line 124: test_simple.py::TestMultiple::test_second PASSED [100%]
Line 125: ...
Line 126: As we know that test_something always fails, we can select which tests to run by using
Line 127: the -k option, as we used to do for unittest. The option is, by the way, more powerful
Line 128: than the one provided by unittest.
Line 129: For example, it is possible to provide the -k option to restrict the tests to a subset of them
Line 130: like we already used to do:
Line 131: $ pytest -v -k first
Line 132: ...
Line 133: collected 3 items / 2 deselected / 1 selected
Line 134: test_simple.py::TestMultiple::test_first PASSED [100%]
Line 135: ...
Line 136: It's also possible to use it to exclude some specific tests:
Line 137: $ pytest -v -k "not something"
Line 138: ...
Line 139: collected 3 items / 1 deselected / 2 selected
Line 140: test_simple.py::TestMultiple::test_first PASSED [ 50%]
Line 141: test_simple.py::TestMultiple::test_second PASSED [100%]
Line 142: ...
Line 143: In the first case, we ran the test_first test, but in the second, we ran all tests except
Line 144: for test_something. So you could view pytest as unittest on steroids. It provides the
Line 145: same features you were used to with unittest, but frequently, they are enhanced to make
Line 146: them more powerful, flexible, or convenient.
Line 147: If one had to choose between the two, it'd probably be a matter of preference. But it's not
Line 148: uncommon to see unittest used for projects that want to keep a more lightweight test
Line 149: suite that is kept stable over the course of the years (unittest, like most modules of the
Line 150: Python Standard Library guarantees very long-term compatibility) and pytest for projects
Line 151: that have more complex test suites or needs.
Line 152: 
Line 153: --- 페이지 152 ---
Line 154: Introduction to PyTest
Line 155: Chapter 5
Line 156: [ 142 ]
Line 157: Writing PyTest fixtures
Line 158: The primary difference between unittest and PyTest lies in how they handle fixtures.
Line 159: While unittest like fixtures (setUp, tearDown, setupClass, and so on) are still
Line 160: supported through the TestCase class when using pytest, pytest tries to provide
Line 161: further decoupling of tests from fixtures.
Line 162: In pytest, a fixture can be declared using the pytest.fixture decorator. Any function
Line 163: decorated with the decorator becomes a fixture:
Line 164: @pytest.fixture
Line 165: def greetings():
Line 166:     print("HELLO!")
Line 167:     yield
Line 168:     print("GOODBYE")
Line 169: The code of the test is executed where we see the yield statement. yield in this context
Line 170: passes execution to the test itself. So this fixture would print "HELLO" before the test starts
Line 171: and then "GOODBYE" when the test finishes.
Line 172: To then bind a fixture to a test, the pytest.mark.usefixtures decorator is used. So, for
Line 173: example, to use our new fixture with the existing TestMultiple.test_second test, we
Line 174: would have to decorate that test using the name of our new fixture:
Line 175: class TestMultiple:
Line 176:     def test_first(self):
Line 177:         assert 5 == 5
Line 178:     @pytest.mark.usefixtures("greetings")
Line 179:     def test_second(self):
Line 180:         assert 10 == 10
Line 181: The name of a fixture is inherited by the name of the function that implements it, so by
Line 182: passing "greetings" to the usefixtures decorator, we end up using our own fixture:
Line 183: $ pytest -v -k "usingfixtures and second" -s
Line 184: ...
Line 185: collected 8 items / 7 deselected / 1 selected
Line 186: test_usingfixtures.py::TestMultiple::test_second HELLO!
Line 187: PASSED
Line 188: GOODBYE
Line 189: ...
Line 190: 
Line 191: --- 페이지 153 ---
Line 192: Introduction to PyTest
Line 193: Chapter 5
Line 194: [ 143 ]
Line 195: So, the part of the fixture before the yield statement replaces the TestCase.setUp
Line 196: method, while the part after yield replaces the TestCase.tearDown method.
Line 197: If we want to use more than one fixture in a test, the usefixtures decorator allows us to
Line 198: pass multiple arguments, one for each fixture that we want to use.
Line 199: If you are wondering about the -s option, that's another difference with unittest. By
Line 200: default, pytest captures all output that your code prints, while unittest, by default, didn't.
Line 201: The two work in a reverse way, so in the case of pytest, we need to explicitly disable
Line 202: output capturing to be able to see our prints.
Line 203: Otherwise, outputs are only shown if the test fails. This has the benefit of keeping test run
Line 204: output cleaner, but can leave people puzzled the first time they see it.
Line 205: Pytest fixtures can be declared in the same module that uses them, or inside a
Line 206: conftest.py module that will be inherited by all modules and packages in the same
Line 207: directory (or subdirectories).
Line 208: Think of conftest.py as being a bit like the __init__.py of test packages; it allows us to
Line 209: customize tests' behavior for that package and even replace fixtures or plugins.
Line 210: While the pytest fixtures mechanism is very powerful, it's usually a bad
Line 211: idea to put fixtures too far away from what uses them.
Line 212: It will make it hard for tests reader to understand what's going on, so
Line 213: spreading tens of conftest.py files around the test suite is usually a
Line 214: good way to make life hard for anyone having to understand our test
Line 215: suite.
Line 216: As one of the primary goals of tests is to act as references of the software
Line 217: behavior, it's usually a good idea to keep them straightforward so that
Line 218: anyone approaching software for the first time can learn about the
Line 219: software without first having to spend days trying to understand how the
Line 220: test suite works and what it does.
Line 221: Obviously, pytest fixtures are not limited to functions; they can also provide a
Line 222: replacement for TestCase.setUpClass and TestCase.tearDownClass. To do so, all we
Line 223: have to do is to declare a fixture that has scope="class" ("function", "module",
Line 224: "package", and "session" scopes are available too to define the life cycle of a fixture):
Line 225: @pytest.fixture(scope="class")
Line 226: def provide_current_time(request):
Line 227:     import datetime
Line 228: 
Line 229: --- 페이지 154 ---
Line 230: Introduction to PyTest
Line 231: Chapter 5
Line 232: [ 144 ]
Line 233:     request.cls.now = datetime.datetime.utcnow()
Line 234:     print("ENTER CLS")
Line 235:     yield
Line 236:     print("EXIT CLS")
Line 237: In the previous fixture, we provide a self.now attribute in the class where the test lives,
Line 238: we print "ENTER CLS" before starting the tests for that class, and then we print "EXIT
Line 239: CLS" once all tests for that class have finished.
Line 240: If we want to use the fixture, we just have to decorate a class with mark.usefixtures and
Line 241: declare we want it:
Line 242: @pytest.mark.usefixtures("provide_current_time")
Line 243: class TestMultiple:
Line 244:     def test_first(self):
Line 245:         print("RUNNING AT", self.now)
Line 246:         assert 5 == 5
Line 247:     @pytest.mark.usefixtures("greetings")
Line 248:     def test_second(self):
Line 249:         assert 10 == 10
Line 250: Now, if we run our tests, we will get the messages from both the provide_current_time
Line 251: fixture and from the greetings one:
Line 252: $ pytest -v -k "usingfixtures" -s
Line 253: collected 8 items / 6 deselected / 2 selected
Line 254: test_usingfixtures.py::TestMultiple::test_first
Line 255: ENTER CLS
Line 256: RUNNING AT 2020-06-17 22:28:23.489433
Line 257: PASSED
Line 258: test_usingfixtures.py::TestMultiple::test_second
Line 259: HELLO!
Line 260: PASSED
Line 261: GOODBYE
Line 262: EXIT CLS
Line 263: You can also see that our test properly printed the self.now attribute, which was injected
Line 264: into the class by the fixture. The request argument to fixtures represents a request for that
Line 265: fixture from a test. It provides some convenient attributes, such as the class that requested
Line 266: the fixture (cls), the instance of that class that is being used to run the test, the module
Line 267: where the test is contained, the tests run session, and many more, allowing us not only to
Line 268: know the context of where our fixture is being used but also to modify those entities.
Line 269: 
Line 270: --- 페이지 155 ---
Line 271: Introduction to PyTest
Line 272: Chapter 5
Line 273: [ 145 ]
Line 274: Apart from setting up tests, classes, and modules, there is usually a set of operations that
Line 275: we might want to do for the whole test suite; for example, configuring pieces of our
Line 276: software that we are going to need in all tests.
Line 277: For that purpose, we can create a conftest.py file inside our test suite, and drop all those
Line 278: fixtures there. They just need to be declared with scope="session", and the
Line 279: autouse=True option can automatically enable them for all our tests:
Line 280: import pytest
Line 281: @pytest.fixture(scope="session", autouse=True)
Line 282: def setupsuite():
Line 283:     print("STARTING TESTS")
Line 284:     yield
Line 285:     print("FINISHED TESTS")
Line 286: Now, running all our tests will be wrapped by the setupsuite fixture, which can take care
Line 287: of setting up and tearing down our test suite:
Line 288: $ pytest -v -s
Line 289: ...
Line 290: test_usingfixtures.py::TestMultiple::test_first
Line 291: STARTING TESTS
Line 292: ENTER CLS
Line 293: RUNNING AT 2020-06-17 22:29:46.108487
Line 294: PASSED
Line 295: test_usingfixtures.py::TestMultiple::test_second
Line 296: HELLO!
Line 297: PASSED
Line 298: GOODBYE
Line 299: EXIT CLS
Line 300: FINISHED TESTS
Line 301: ...
Line 302: We can see from the output of the command that, according to our new fixture, the tests
Line 303: printed "STARTING TESTS" when they started and printed "FINISHED TESTS" at the end
Line 304: of the whole suite execution. This means that we can use session-wide fixtures to prepare
Line 305: and tear down resources or configurations that are necessary for the whole suite to run.
Line 306: 
Line 307: --- 페이지 156 ---
Line 308: Introduction to PyTest
Line 309: Chapter 5
Line 310: [ 146 ]
Line 311: Using fixtures for dependency injection
Line 312: Another good property of pytest fixtures is that they can also provide some kind of
Line 313: dependency injection management. For example, your software might use a remote
Line 314: random number generator. Whenever a new random number is needed, an HTTP request
Line 315: to a remote service is made that will return the number.
Line 316:  Inside our conftest.py file, we could provide a fixture that builds a fake random number
Line 317: generator that by default is going to generate random numbers (to test the software still
Line 318: works when the provided values are random) but without doing any remote calls to ensure
Line 319: the test suite is able to run quickly:
Line 320: $ cat conftest.py
Line 321: import pytest
Line 322: @pytest.fixture
Line 323: def random_number_generator():
Line 324:     import random
Line 325:     def _number_provider():
Line 326:         return random.choice(range(10))
Line 327:     yield _number_provider
Line 328: Then, we could have any number of tests that use our random number generator (for the
Line 329: sake of simplicity, we are going to make a test_randomness.py file with a single test
Line 330: using it):
Line 331: def test_something(random_number_generator):
Line 332:     a = random_number_generator()
Line 333:     b = 10
Line 334:     assert a + b >= 10
Line 335: If a test has an argument, pytest will automatically consider that dependency injection
Line 336: and will invoke the fixture with the same name of the argument to provide the object that
Line 337: should satisfy that dependency.
Line 338: So, for our test_something function, the random_number_generator object is the one
Line 339: returned by our random_number_generator fixture, which returns numbers from 0 to 9.
Line 340: 
Line 341: --- 페이지 157 ---
Line 342: Introduction to PyTest
Line 343: Chapter 5
Line 344: [ 147 ]
Line 345: As fixtures can be overridden inside modules or packages, if for some of our tests we
Line 346: wanted to replace the random number generator with a fairly predictable one (that always
Line 347: returns 1, all we would have to do is, again, declare a fixture with the same exact name
Line 348: inside the other module. Let's look at an example:
Line 349: We would make a test_fixturesinj.py test module where we provide a new
Line 350: 1.
Line 351: random_number_generator that is not random at all and we have a test that
Line 352: relies on that feature:
Line 353: def test_something(random_number_generator):
Line 354:     a = random_number_generator()
Line 355:     b = 10
Line 356:     assert a + b == 11
Line 357: @pytest.fixture
Line 358: def random_number_generator():
Line 359:     def _number_provider():
Line 360:         return 1
Line 361:     yield _number_provider
Line 362: If we run our two test_something tests, from the two modules, they will both
Line 363: 2.
Line 364: pass, because one will be using a random number generator that builds random
Line 365: numbers, while the other will use one that always returns the number 1:
Line 366: $ pytest -v -k "something and not simple"
Line 367: ...
Line 368: collected 7 items / 5 deselected / 2 selected
Line 369: test_fixturesinj.py::test_something PASSED [ 50%]
Line 370: test_randomness.py::test_something PASSED [100%]
Line 371: ...
Line 372: So we saw that pytest fixtures are much more flexible than unittest ones and that due
Line 373: to that greater decoupling and flexibility, great care has to be put into making sure it's clear
Line 374: which fixture implementations we end up using in our tests.
Line 375: 
Line 376: --- 페이지 158 ---
Line 377: Introduction to PyTest
Line 378: Chapter 5
Line 379: [ 148 ]
Line 380: In the upcoming sections, we are going to look at some of the built-in fixtures that pytest
Line 381: provides and that are generally useful during the development of a test suite.
Line 382: Managing temporary data with tmp_path
Line 383: Many applications need to write data to disk. Surely we don't want data written during
Line 384: tests to interfere with the data we read/write during the real program execution. Data
Line 385: fixtures used in tests usually have to be predictable and we certainly don't want to corrupt
Line 386: real data when we run our tests.
Line 387: So it's common for a test suite to have its own read/write path where all the data is written.
Line 388: If we decided the path beforehand, by the way, there would be the risk that different test
Line 389: runs would read previous data and thus might not spot bugs or might fail without a
Line 390: reason.
Line 391: For this reason, one of the fixtures that pytest provides out of the box is tmp_path, which,
Line 392: when injected into a test, provides a temporary path that is always different on every test
Line 393: run. Also, it will take care of retaining the most recent temporary directories (for debugging
Line 394: purposes) while deleting the oldest ones:
Line 395: def test_tmp(tmp_path):
Line 396:     f = tmp_path / "file.txt"
Line 397:     print("FILE: ", f)
Line 398:     f.write_text("Hello World")
Line 399:     fread = tmp_path / "file.txt"
Line 400:     assert fread.read_text() == "Hello World"
Line 401: The test_tmp test creates a file.txt file in the temporary directory and writes "Hello
Line 402: World" in it. Once the write is completed, it tries to access the same file again and confirm
Line 403: that the expected content was written.
Line 404: The tmp_path argument will be injected by pytest itself and will point to a path made by
Line 405: pytest for that specific test run.
Line 406: This can be seen by running our test with the -s option, which will make the "FILE: ..."
Line 407: string that we printed visible:
Line 408: $ pytest test_tmppath.py -v -s
Line 409: ===== test session starts =====
Line 410: ...
Line 411: collected 1 item
Line 412: 
Line 413: --- 페이지 159 ---
Line 414: Introduction to PyTest
Line 415: Chapter 5
Line 416: [ 149 ]
Line 417: test_tmppath.py::test_tmp
Line 418: FILE: /tmp/pytest-of-amol/pytest-3/test_tmp0/file.txt
Line 419: PASSED
Line 420: ===== 1 passed in 0.03s =====
Line 421: On every new run, the pytest-3 directory will be increased, so the most recent directory
Line 422: will be from the most recent run and only the latest three directories will be kept.
Line 423: Testing I/O with capsys
Line 424: When we implemented the test suite for the TODO list application, we had to check that the
Line 425: output provided by the application was the expected one. That meant that we provided a
Line 426: fake implementation of the standard output, which allowed us to see what the application
Line 427: was going to write.
Line 428: Suppose you have a very simple app that prints something when started:
Line 429: def myapp():
Line 430:     print("MyApp Started")
Line 431: If we wanted to test that the app actually prints what we expect when started, we could use
Line 432: the capsys fixture to access the capture output from sys.stdout and sys.stderr of our
Line 433: application:
Line 434: def test_capsys(capsys):
Line 435:     myapp()
Line 436:     out, err = capsys.readouterr()
Line 437:     assert out == "MyApp Started\n"
Line 438: The test_capsys test just starts the application (running myapp), then through
Line 439: capsys.readouterr() it retrieves the content of sys.stdout and sys.stderr
Line 440: snapshotted at that moment. 
Line 441: Once the standard output content is available, it can be compared to the expected one to
Line 442: confirm that the application actually printed what we wanted. If the application really
Line 443: printed "MyApp Started" as expected, running the test should pass and confirm that's the
Line 444: content of the standard output:
Line 445: $ pytest test_capsys.py -v
Line 446: ===== test session starts =====
Line 447: ...
Line 448: collected 1 item
Line 449: 
Line 450: --- 페이지 160 ---
Line 451: Introduction to PyTest
Line 452: Chapter 5
Line 453: [ 150 ]
Line 454: test_capsys.py::test_capsys PASSED
Line 455: ===== 1 passed in 0.03s =====
Line 456: The passing test run confirms that the capsys plugin worked correctly and our test was
Line 457: able to intercept the output sent by the function under test.
Line 458: Running subsets of the testsuite
Line 459: In the previous chapters, we saw how to divide our test suite into subsets that we can run
Line 460: on demand based on their purpose and cost. The way to do so involved dividing the tests
Line 461: by directory or by name, such that we could point the test runner to a specific directory or
Line 462: filter for test names with the -k option.
Line 463: While those strategies are available on pytest too, pytest provides more ways to
Line 464: organize and divide tests; one of them being markers.
Line 465: Instead of naming all our smoke tests "test_smoke_something", for example, we could
Line 466: just name the test "test_something" and mark it as a smoke test. Or, we could mark slow
Line 467: tests, so that we can avoid running slow ones during the most frequent runs.
Line 468: Marking a test is as easy as decorating it with @pytest.mark.marker, where marker is
Line 469: our custom label. For example, we could create two tests and use @pytest.mark.first to
Line 470: mark the first of the two tests:
Line 471: import pytest
Line 472: @pytest.mark.first
Line 473: def test_one():
Line 474:     assert True
Line 475: def test_two():
Line 476:     assert True
Line 477: At this point, we could select which tests to run by using pytest -m first or pytest -m
Line 478: "not first":
Line 479: $ pytest test_markers.py -v
Line 480: ...
Line 481: test_markers.py::test_one PASSED [ 50%]
Line 482: test_markers.py::test_two PASSED [100%]
Line 483: 
Line 484: --- 페이지 161 ---
Line 485: Introduction to PyTest
Line 486: Chapter 5
Line 487: [ 151 ]
Line 488: pytest test_markers.py -m "first" would run only the one marked with our
Line 489: custom marker:
Line 490: $ pytest test_markers.py -v -m first
Line 491: ...
Line 492: test_markers.py::test_one PASSED [100%]
Line 493: This means that we can mark our tests in any way we want and run selected groups of tests
Line 494: independently from the directory where they sit or how they are named.
Line 495: On some versions of pytest, you might get a warning when using custom markers:
Line 496: Unknown pytest.mark.first - is this a typo?  You can register custom marks
Line 497: to avoid this warning
Line 498: This means that the marker is unknown to pytest and must be registered in the list of
Line 499: available markers to make the warning go away. The reason for this is to prevent typos that
Line 500: would slip by unnoticed if markers didn't have to be registered. 
Line 501: To make a marker available and make the warning disappear, the custom markers can be
Line 502: set in the pytest.ini configuration file for your test suite:
Line 503: [pytest]
Line 504: markers =
Line 505:     first: mark a test as the first one written.
Line 506: If the configuration file is properly recognized and we have no typos in the "first"
Line 507: marker, the previously mentioned warning will go away and we will be able to use the
Line 508: "first" marker freely.
Line 509: Summary
Line 510: In this chapter, we saw how pytest can provide more advanced features on top of the
Line 511: same functionalities we were already used to with unittest. We also saw how we can run
Line 512: our existing test suite with pytest and how we can evolve it to leverage some of built-in
Line 513: pytest features.
Line 514: We've looked at some of the features that pytest provides out of the box, and in the next
Line 515: chapter, we will introduce more advanced pytest features, such as parametric tests and
Line 516: fixture generation.