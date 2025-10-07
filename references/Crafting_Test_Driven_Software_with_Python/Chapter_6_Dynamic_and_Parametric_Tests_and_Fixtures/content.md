Line 1: 
Line 2: --- 페이지 162 ---
Line 3: 6
Line 4: Dynamic and Parametric Tests
Line 5: and Fixtures
Line 6: In the previous chapter, we saw how pytest can be used to run our test suites, and how it
Line 7: provides some more advanced features that are unavailable in unittest by default.
Line 8: Python has seen multiple frameworks and libraries built on top of unittest to extend it
Line 9: with various features and utilities, but pytest has surely become the most widespread
Line 10: testing framework in the Python community. One of the reasons why pytest became so
Line 11: popular is its flexibility and support for dynamic behaviors. Apart from this, generating
Line 12: tests and fixtures dynamically or heavily changing test suite behavior are other features
Line 13: supported by pytest out of the box.
Line 14: In this chapter, we are going to see how to configure a test suite and generate dynamic
Line 15: fixtures and dynamic or parametric tests. As your test suite grows, it will be important to be
Line 16: able to know which options PyTest provides to drive the test suite execution and how we
Line 17: can generate fixtures and tests dynamically instead of rewriting them over and over.
Line 18: In this chapter, we will cover the following topics:
Line 19: Configuring the test suite
Line 20: Generating fixtures
Line 21: Generating tests with parametric tests
Line 22: Technical requirements
Line 23: We need a working Python interpreter with the pytest framework installed. Pytest can be
Line 24: installed using the following command:
Line 25: $ pip install pytest
Line 26: 
Line 27: --- 페이지 163 ---
Line 28: Dynamic and Parametric Tests and Fixtures
Line 29: Chapter 6
Line 30: [ 153 ]
Line 31: Though the examples have been written using Python 3.7 and pytest 5.4.3, they should
Line 32: work on most modern Python versions. You can find the code files used in this chapter on
Line 33: GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-
Line 34: with-​Python/​tree/​main/​Chapter06
Line 35: Configuring the test suite
Line 36: In pytest, there are two primary configuration files that can be used to drive the behavior of
Line 37: our testing environment:
Line 38: pytest.ini takes care of configuring pytest itself, so the options we set there
Line 39: are mostly related to tweaking the behavior of the test runner and discovery.
Line 40: These options are usually available as command-line options too.
Line 41: conftest.py is aimed at configuring our tests and test suite, so it's the place
Line 42: where we can declare new fixtures, attach plugins, and change the way our tests
Line 43: should behave.
Line 44: While pytest has grown over the years, with other ways being developed to configure the
Line 45: behavior of pytest itself or of the test suite, the two aforementioned ways are probably the
Line 46: most widespread.
Line 47: For example, for a fizzbuzz project, if we have a test suite with the classical basic
Line 48: distinction between the source code, unit tests, and functional tests, then we could have a
Line 49: pytest.ini file within the project directory to drive how pytest should run:
Line 50: .
Line 51: ├── pytest.ini
Line 52: ├── src
Line 53: │   ├── fizzbuzz
Line 54: │   │   ├── __init__.py
Line 55: │   │   └── __main__.py
Line 56: │   └── setup.py
Line 57: └── tests
Line 58:     ├── conftest.py
Line 59:     ├── __init__.py
Line 60:     ├── functional
Line 61:     │   └── test_acceptance.py
Line 62:     └── unit
Line 63:         ├── test_checks.py
Line 64:         └── test_output.py
Line 65: 
Line 66: --- 페이지 164 ---
Line 67: Dynamic and Parametric Tests and Fixtures
Line 68: Chapter 6
Line 69: [ 154 ]
Line 70: The content of pytest.ini could contain any option that is also available via the
Line 71: command line, plus a bunch of extra options as described in the pytest reference for INI
Line 72: options.
Line 73: For example, to run pytest in verbose mode, without capturing the output and by
Line 74: disabling deprecation warnings, we could create a pytest.ini file that adds the following
Line 75: related configuration options:
Line 76: [pytest]
Line 77: addopts = -v -s
Line 78: filterwarnings =
Line 79:     ignore::DeprecationWarning
Line 80: In the same way, we have a conftest.py file in the tests directory. We already know
Line 81: from Chapter 5, Introduction to PyTest, that conftest.py is where we can declare our
Line 82: fixtures to make them available to the directory and all subdirectories. If set with
Line 83: autouse=True, the fixtures will also automatically apply to all tests in the same directory.
Line 84: If we want to print every time we enter and exit a test, for example, we could add a fixture
Line 85: to our conftest.py file as shown here:
Line 86: import pytest
Line 87: @pytest.fixture(scope="function", autouse=True)
Line 88: def enterexit():
Line 89:     print("ENTER")
Line 90:     yield
Line 91:     print("EXIT")
Line 92: As conftest is the entry point of our tests, the fixture would become available for all our
Line 93: tests, and as it is with autouse=True, all of them would start using it. Not only can we use
Line 94: fixtures that are declared in conftest.py itself, but we can also use fixtures that come
Line 95: from anything that was imported. We just have to declare the module as a plugin that has
Line 96: to be loaded when the tests start.
Line 97: For example, we could have a fizzbuzz.testing package in our fizzbuzz project where
Line 98: fizzbuzz.testing.fixtures provides a set of convenience fixtures for anyone willing
Line 99: to test our simple app.
Line 100: Similarly, we could have a fizzbuzz.testing.fixtures.announce fixture that
Line 101: announces every test being run:
Line 102: import pytest
Line 103: @pytest.fixture(scope="function", autouse=True)
Line 104: 
Line 105: --- 페이지 165 ---
Line 106: Dynamic and Parametric Tests and Fixtures
Line 107: Chapter 6
Line 108: [ 155 ]
Line 109: def announce(request):
Line 110:     print("RUNNING", request.function)
Line 111: To use it, we just have to add our module to pytest_plugins in the conftest.py file as
Line 112: follows:
Line 113: pytest_plugins = ["fizzbuzz.testing.fixtures"]
Line 114: Note that while conftest.py can be provided multiple times and will
Line 115: only apply to the package that contains it, pytest_plugins instead
Line 116: should only be declared in the root conftest.py file, as there is no way
Line 117: to enable/disable plugins on demand – they are always enabled for the
Line 118: whole test suite.
Line 119: But adding fixtures is not all conftest.py can do. Pytest also provides a bunch of hooks
Line 120: that can be exposed from conftest (or from a plugin declared in pytest_plugins) that
Line 121: can be used to drive the behavior of the test suite.
Line 122: The most obvious hooks are pytest_runtest_setup, which is called when preparing to
Line 123: execute a new test; pytest_runtest_call, called when executing a new test; and
Line 124: pytest_runtest_teardown, called when finalizing a test.
Line 125: For example, our previous announce fixture can be rewritten using the
Line 126: pytest_runtest_setup hook as follows:
Line 127: def pytest_runtest_setup(item):
Line 128:     print("Hook announce", item)
Line 129: Tons of additional hooks are available in pytest, such as a hook for parsing command-line
Line 130: options, a hook for generating test run reports, a hook for starting or finishing a whole test
Line 131: run, and so on.
Line 132: For a complete list of available hooks, refer to the pytest API reference at
Line 133: https:/​/​docs.​pytest.​org/​en/​stable/​reference.​html#hooks.
Line 134: We have seen how to change the behavior of our test suite by using configuration options,
Line 135: conftest, and hooks, but pytest's flexibility doesn't stop there. Not only we can change the
Line 136: behavior of the test suite itself, but we can also change the behavior of the fixtures by
Line 137: generating those fixtures on demand.
Line 138: 
Line 139: --- 페이지 166 ---
Line 140: Dynamic and Parametric Tests and Fixtures
Line 141: Chapter 6
Line 142: [ 156 ]
Line 143: Generating fixtures
Line 144: Now that we know that conftest.py allows us to customize how our test suite should
Line 145: behave, the next step is to notice that pytest allows us to also change how our fixtures
Line 146: behave as well.
Line 147: For example, the fizzbuzz program is expected to print "fizz" on every number divisible
Line 148: by 3, print "buzz" on every number divisible by 5, and print "fizzbuzz" on every
Line 149: number divisible by both.
Line 150: To implement this, we could have outfizz and outbuzz functions that print "fizz" or
Line 151: "buzz" without a newline. This allows us to call each one of them to print fizz or buzz
Line 152: and to call both functions one after the other to print fizzbuzz.
Line 153: To test this behavior, we could have a tests/unit/test_output.py module containing
Line 154: all the tests for our output utilities. For outfizz and outbuzz, we could write the tests as
Line 155: follows:
Line 156: from fizzbuzz import outfizz, outbuzz, endnum
Line 157: def test_outfizz(capsys):
Line 158:     outfizz()
Line 159:     out, _ = capsys.readouterr()
Line 160:     assert out == "fizz"
Line 161: def test_outbuzz(capsys):
Line 162:     outbuzz()
Line 163:     out, _ = capsys.readouterr()
Line 164:     assert out == "buzz"
Line 165: These are pretty simple tests that do the same thing, just over a different output. One
Line 166: invokes the outfizz function and checks whether it prints "fizz" and the other invokes
Line 167: the outbuzz function and checks whether it prints "buzz".
Line 168: We could think of having a form of dependency injection oriented toward the test itself,
Line 169: where the function to test is provided by a fixture. This would allow us to write the test
Line 170: once and provide two fixtures: one that injects "fizz" and one that injects "buzz".
Line 171: 
Line 172: --- 페이지 167 ---
Line 173: Dynamic and Parametric Tests and Fixtures
Line 174: Chapter 6
Line 175: [ 157 ]
Line 176: Going even further, we could even write the fixture only once, and dynamically generate it.
Line 177: Pytest allows us to parameterize fixtures. This means that out of a list of parameters, the
Line 178: fixture will run multiple times, once for each parameter. This will allow us to write a single
Line 179: test with a single fixture that injects the right function and the right expectation testing once
Line 180: for "fizz" and once for "buzz":
Line 181: def test_output(expected_output, capsys):
Line 182:     func, expected = expected_output
Line 183:     func()
Line 184:     out, _ = capsys.readouterr()
Line 185:     assert out == expected
Line 186: The test_output test relies on the expected_output fixture (which we will define
Line 187: shortly) and the capsys fixture that is provided by pytest itself.
Line 188: The expected_output fixture will be expected to provide the function that generates the
Line 189: output we want to test (func) and the output we expect that function to print (expected).
Line 190: Our expected_output fixture will get the function that generates the expected output
Line 191: from the fizzbuzz module through a getattr call that is meant to retrieve the outfizz
Line 192: and outbuzz functions:
Line 193: import pytest
Line 194: import fizzbuzz
Line 195: @pytest.fixture(params=["fizz", "buzz"])
Line 196: def expected_output(request):
Line 197:     yield getattr(fizzbuzz, "out{}".format(request.param)), request.param
Line 198: Thanks to @pytest.fixture(params=["fizz", "buzz"]), the expected_output
Line 199: fixture will be invoked by pytest twice, once for "fizz" and once for "buzz", leading to
Line 200: the test running twice, once for each parameter.
Line 201: Through request.param the fixtures know which one of the two parameters is running,
Line 202: and using getattr, pytest retrieves from the fizzbuzz module the outfizz and outbuzz
Line 203: output generation functions and yields to the test the function to be tested and its
Line 204: associated expected output.
Line 205: 
Line 206: --- 페이지 168 ---
Line 207: Dynamic and Parametric Tests and Fixtures
Line 208: Chapter 6
Line 209: [ 158 ]
Line 210: When the parameters are not strings, you can also use the ids argument
Line 211: to provide a text description for them. This is so that when the tests runs,
Line 212: you know which parameter is being used.
Line 213: We have seen how we can drive fixture generation from parameters and thus generate
Line 214: fixtures based on them, but pytest can go further and allow you to drive the fixture
Line 215: generation from command-line options.
Line 216: For example, imagine that you want to be able to test two possible setups: one where the
Line 217: app prints lowercase strings, and another where it prints uppercase "FIZZ" and "BUZZ".
Line 218: To do this, we could add to conftest.py a pytest_addoption hook to inject an extra --
Line 219: upper option in pytest:
Line 220: def pytest_addoption(parser):
Line 221:  parser.addoption(
Line 222:       "--upper", action="store_true",
Line 223:       help="test for uppercase behavior"
Line 224:  )
Line 225: When this option is set, the output functions will be tested for uppercase output.
Line 226: We need to slightly modify our expected_output fixture to return the right uppercase
Line 227: string that we need to check against when the --upper option is provided:
Line 228: @pytest.fixture(params=["fizz", "buzz"])
Line 229: def expected_output(request):
Line 230:     text = request.param
Line 231:     if request.config.getoption("--upper"):
Line 232:         text = text.upper()
Line 233:     yield getattr(fizzbuzz, "out{}".format(request.param)), text
Line 234: Now our tests, by default, will check against the lowercase output when run:
Line 235: $ pytest -k output
Line 236: tests/unit/test_output.py::test_output[fizz] PASSED
Line 237: tests/unit/test_output.py::test_output[buzz] PASSED
Line 238: But, if we provide --upper, we test against the uppercase output (which obviously makes
Line 239: our tests fail as the outfizz and outbuzz functions output text in lowercase):
Line 240: $ pytest --upper -k output
Line 241: tests/unit/test_output.py::test_output[fizz] FAILED
Line 242: tests/unit/test_output.py::test_output[buzz] FAILED
Line 243: ========= FAILURES ==========
Line 244: ...
Line 245: 
Line 246: --- 페이지 169 ---
Line 247: Dynamic and Parametric Tests and Fixtures
Line 248: Chapter 6
Line 249: [ 159 ]
Line 250: E AssertionError: assert 'fizz' == 'FIZZ'
Line 251: ...
Line 252: E AssertionError: assert 'buzz' == 'BUZZ'
Line 253: We have seen how to pass options to fixtures from parameters and the command line, but
Line 254: what if I want to configure fixtures from the tests themselves? That's possible thanks to
Line 255: markers. Using pytest.mark, we can add markers to our tests, and obviously, those
Line 256: markers can be read from the test suite and the fixtures. The most flexible thing about
Line 257: markers is that markers can have parameters too. So the markers can be used to set
Line 258: attributes for a specific test that will be visible to the fixture.
Line 259: For example, we could have the tests be able to force lower/upper case configuration
Line 260: instead of relying on an external command-line option. The test could add a
Line 261: pytest.mark.textcase marker to flag whether it wants upper- or lowercase text from
Line 262: the fixture:
Line 263: @pytest.mark.textcase("lower")
Line 264: def test_lowercase_output(expected_output, capsys):
Line 265:     func, expected = expected_output
Line 266:     func()
Line 267:     out, _ = capsys.readouterr()
Line 268:     assert out == expected
Line 269: Our test_lowercase_output is a perfect copy of test_output, apart from the added
Line 270: marker. The marker specifies that the test has to run with lowercase text even when the --
Line 271: upper option is provided.
Line 272: To enable such a behavior, we have to modify our expected_output fixture to read the
Line 273: marker and its arguments. After reading the command-line options, we are going to
Line 274: retrieve the marker, get its first argument, and lower/upper the text based on it:
Line 275: @pytest.fixture(params=["fizz", "buzz"])
Line 276: def expected_output(request):
Line 277:     text = request.param
Line 278:     if request.config.getoption("--upper"):
Line 279:         text = text.upper()
Line 280:     textcasemarker = request.node.get_closest_marker("textcase")
Line 281:     if textcasemarker:
Line 282:         textcase, = textcasemarker.args
Line 283:         if textcase == "upper":
Line 284:             text = text.upper()
Line 285:         elif textcase == "lower":
Line 286:             text = text.lower()
Line 287:         else:
Line 288: 
Line 289: --- 페이지 170 ---
Line 290: Dynamic and Parametric Tests and Fixtures
Line 291: Chapter 6
Line 292: [ 160 ]
Line 293:             raise ValueError("Invalid Test Marker")
Line 294:     yield getattr(fizzbuzz, "out{}".format(request.param)), text
Line 295: Now if we run our test suite, while the test_output function will fail when we provide
Line 296: the --upper option (because the output functions provide only lowercase output), the
Line 297: test_lowercase_output test instead will always succeed because the fixture is
Line 298: configured by the test to only provide lowercase text:
Line 299: $ pytest --upper -k output
Line 300: tests/unit/test_output.py::test_output[fizz] FAILED
Line 301: tests/unit/test_output.py::test_output[buzz] FAILED
Line 302: tests/unit/test_output.py::test_lowercase_output[fizz] PASSED
Line 303: tests/unit/test_output.py::test_lowercase_output[buzz] PASSED
Line 304: We have seen how we can change the behavior of fixtures based on parameters and options
Line 305: that we provide, and many of those practices work out of the box for changing the behavior
Line 306: of the tests themselves. Just as fixtures have the params option, tests support the
Line 307: @pytest.mark.parametrize decorator, which allows generating tests based on
Line 308: parameters.
Line 309: Generating tests with parametric tests
Line 310: Sometimes you find yourself writing the same check over and over for multiple
Line 311: configurations. Instead, it would be convenient if we could write the test only once and
Line 312: provide the configurations in a declarative way.
Line 313: That's exactly what @pytest.mark.parametrize allows us to do: to generate tests based
Line 314: on a template function and the various configurations that have to be provided.
Line 315: For example, in our fizzbuzz software, we could have two isbuzz and isfizz checks
Line 316: that verify whether the provided number should lead us to print the "buzz" or "fizz"
Line 317: strings. Like always, we want to write a test that drives the implementation of those two
Line 318: little blocks of our software, and the tests might look like this:
Line 319: def test_isfizz():
Line 320:     assert isfizz(1) is False
Line 321:     assert isfizz(3) is True
Line 322:     assert isfizz(4) is False
Line 323:     assert isfizz(6) is True
Line 324: def test_isbuzz():
Line 325:     assert isbuzz(1) is False
Line 326:     assert isbuzz(3) is False
Line 327: 
Line 328: --- 페이지 171 ---
Line 329: Dynamic and Parametric Tests and Fixtures
Line 330: Chapter 6
Line 331: [ 161 ]
Line 332:     assert isbuzz(5) is True
Line 333:     assert isbuzz(6) is False
Line 334:     assert isbuzz(10) is True
Line 335: The tests cover a few cases to make us feel confident that our implementation will be
Line 336: reliable, but it's very inconvenient to write the same check over and over for each possible
Line 337: number that we want to check.
Line 338: That's where parameterizing the test comes into the picture. Instead of having the
Line 339: test_isfizz function be a long list of assertions, we could rewrite it to be a single
Line 340: assertion that gets rerun by pytest multiple times, once for each parameter it receives. The
Line 341: parameters could for example be the number to check with isfizz and the expected
Line 342: outcome, so that we can compare the outcome of invoking isfizz to the expected
Line 343: outcome:
Line 344: @pytest.mark.parametrize("n,res", [
Line 345:     (1, False),
Line 346:     (3, True),
Line 347:     (4, False),
Line 348:     (6, True)
Line 349: ])
Line 350: def test_isfizz(n, res):
Line 351:     assert isfizz(n) is res
Line 352: When we run the test suite, pytest will take care of generating all tests, one for each
Line 353: parameter, to guarantee we are checking all the conditions as we were doing before:
Line 354: $ pytest -k checks
Line 355: tests/unit/test_checks.py::test_isfizz[1-False] PASSED [ 20%]
Line 356: tests/unit/test_checks.py::test_isfizz[3-True] PASSED [ 40%]
Line 357: tests/unit/test_checks.py::test_isfizz[4-False] PASSED [ 60%]
Line 358: tests/unit/test_checks.py::test_isfizz[6-True] PASSED [ 80%]
Line 359: ...
Line 360: We can even go further and mix a fixture with a parameterized test and have the fixture 
Line 361: generate one of the parameters. For the isfizz function, we explicitly provided the
Line 362: expected result; for the isbuzz test, we are going to have the fixture inject whether the
Line 363: number is divisible by 5 and thus whether it would print buzz or not.
Line 364: To do so, we are going to provide a divisible_by5 fixture that does no more than to
Line 365: return whether the number is divisible by 5 or not:
Line 366: @pytest.fixture(scope="function")
Line 367: def divisible_by5(n):
Line 368:     return n % 5 == 0
Line 369: 
Line 370: --- 페이지 172 ---
Line 371: Dynamic and Parametric Tests and Fixtures
Line 372: Chapter 6
Line 373: [ 162 ]
Line 374: Then, we can have our parameterized test accept the parameter for the number, but use the
Line 375: fixture for the expected result, as shown in the following code:
Line 376: @pytest.mark.parametrize("n", [1, 3, 5, 6, 10])
Line 377: def test_isbuzz(n, divisible_by5):
Line 378:     assert isbuzz(n) is divisible_by5
Line 379: On each one of the generated tests, the number n will be provided to both the test and the
Line 380: fixture (by virtue of the shared argument name) and our test will be able to confirm that
Line 381: isbuzz returns True only for numbers divisible by 5:
Line 382: $ pytest -k checks
Line 383: ...
Line 384: tests/unit/test_checks.py::test_isbuzz[1] PASSED [ 55%]
Line 385: tests/unit/test_checks.py::test_isbuzz[3] PASSED [ 66%]
Line 386: tests/unit/test_checks.py::test_isbuzz[5] PASSED [ 77%]
Line 387: tests/unit/test_checks.py::test_isbuzz[6] PASSED [ 88%]
Line 388: tests/unit/test_checks.py::test_isbuzz[10] PASSED [100%]
Line 389: It is also possible to provide arguments to the test through a fixture by using the indirect
Line 390: option of parametrize. In such a case, the parameter is provided to the fixture and then
Line 391: the fixture can decide what to do with it, whether to pass it to the test or change it. This
Line 392: allows us to replace test parameters, instead of injecting new ones as we did.
Line 393: Summary
Line 394: In this chapter, we saw why pytest is considered a very flexible and powerful framework
Line 395: for writing test suites. Its capabilities to automatically generate tests and fixtures on the fly
Line 396: and to change their behaviors through hooks and plugins are very helpful, allowing us to
Line 397: write smaller test suites that cover more cases.
Line 398: The problem with those techniques is that they make it less clear what's being tested and
Line 399: how, so it's always a bad idea to abuse them. It's usually better to ensure that your test is
Line 400: easy to read and clear about what's going on. That way, it can act as a form of
Line 401: documentation on the behavior of the software and allow other team members to learn
Line 402: about a new feature by reading its test suite.
Line 403: 
Line 404: --- 페이지 173 ---
Line 405: Dynamic and Parametric Tests and Fixtures
Line 406: Chapter 6
Line 407: [ 163 ]
Line 408: Only once all our test suites are written in a simple and easy-to-understand way can we
Line 409: focus on reducing the complexity of those suites by virtue of parameterization or
Line 410: dynamically generated behaviors. When dynamically generated behaviors get in the way of
Line 411: describing the behavior of software clearly, they can make the test suite unmaintainable
Line 412: and full of effects at a distance (due to the Actions at a distance anti-pattern) that make it
Line 413: hard to understand why a test fails or passes.
Line 414: Now that we have seen how to write tests in the most powerful ways, in the next chapter
Line 415: we will focus on which tests to write. We are going to focus on getting the right fitness
Line 416: functions for our software to ensure we are actually testing what we care about.