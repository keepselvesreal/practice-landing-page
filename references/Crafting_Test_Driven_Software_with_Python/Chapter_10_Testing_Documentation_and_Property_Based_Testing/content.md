Line 1: 
Line 2: --- 페이지 230 ---
Line 3: 10
Line 4: Testing Documentation and
Line 5: Property-Based Testing
Line 6: In the previous chapter, we saw how to manage the environment where the test suite runs
Line 7: through Tox. We now have a fairly good understanding of how to create a test suite, how to
Line 8: set up an environment where this can be run, and how to ensure that we are able to
Line 9: organize it in a way that remains effective as our software and test suite grow. We are now
Line 10: going to move our attention to confirm that our tests are able to identify and cover corner
Line 11: cases and make sure that our documentation is as robust and tested as our software itself.
Line 12: In this chapter, we will cover the following topics:
Line 13: Testing documentation
Line 14: Property based-testing
Line 15: Technical requirements
Line 16: We need a working Python interpreter with PyTest, Sphinx for documentation testing, and
Line 17: the Hypothesis framework for property-based testing. All of them can be installed through
Line 18: pip with the help of the following command:
Line 19: $ pip install pytest sphinx hypothesis
Line 20: The examples have been written on Python 3.7, Sphinx 3.3.0, PyTest 6.0.2, and Hypothesis
Line 21: 5.41, but should work on most modern Python versions.
Line 22: You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
Line 23: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter10.
Line 24: 
Line 25: --- 페이지 231 ---
Line 26: Testing Documentation and Property-Based Testing
Line 27: Chapter 10
Line 28: [ 221 ]
Line 29: Testing documentation
Line 30: When documentation is written with the goal of teaching other developers how a system
Line 31: works, providing examples on how to use its inner layers, and train them on the driving
Line 32: design principles behind some complex software, it can be a very effective way to onboard
Line 33: new team members in a project.
Line 34: In any fairly big and complex project, documentation becomes something that is essential
Line 35: for navigating the complexity of the system without having to rely on our memory to
Line 36: remember how to use every single layer or class involved in the system.
Line 37: But documentation is also hard. Not only is it actually hard to write, because what might
Line 38: seem obvious and clear to us might sound cryptic to another reader, but also because the
Line 39: code evolves quickly and documentation easily becomes outdated and inaccurate.
Line 40: Thankfully, testing is a very effective way to also ensure that our documentation doesn't get
Line 41: outdated and that it still applies to our system. As much as we test the application code, we
Line 42: can test the documentation examples. If an example becomes outdated, it will fail and our
Line 43: documentation tests won't pass.
Line 44: Given that we have covered every human-readable explanation in our documentation with
Line 45: a code example, we can make sure that our documentation doesn't get stale and still
Line 46: describes the current state of the system by verifying those code examples. To show how
Line 47: documentation can be kept in sync with the code, we are going to take our existing contacts
Line 48: application we built in previous chapters and we are going to add tested documentation to
Line 49: it.
Line 50: Our first step will be to create the documentation itself. In Python, the most common tool
Line 51: for documentation is Sphinx, which is based on the reStructuredText format.
Line 52: Sphinx provides the sphinx-quickstart command to create new documentation for a
Line 53: project. Running sphinx-quickstart docs will ask a few questions about the layout of
Line 54: our documentation project and will create it inside the docs directory. We will also provide
Line 55: the --ext-doctest --ext-autodoc options to enable the extensions to make
Line 56: documentation testable and to autogenerate documentation from existing code:
Line 57: $ sphinx-quickstart docs --ext-doctest --ext-autodoc
Line 58: Welcome to the Sphinx 3.3.0 quickstart utility.
Line 59: ...
Line 60: > Separate source and build directories (y/n) [n]: y
Line 61: > Project name: Contacts
Line 62: > Author name(s): Alessandro Molina
Line 63: 
Line 64: --- 페이지 232 ---
Line 65: Testing Documentation and Property-Based Testing
Line 66: Chapter 10
Line 67: [ 222 ]
Line 68: > Project release []:
Line 69: > Project language [en]:
Line 70: Creating file docs/source/conf.py.
Line 71: Creating file docs/source/index.rst.
Line 72: Creating file docs/Makefile.
Line 73: Creating file docs/make.bat.
Line 74: Finished: An initial directory structure has been created.
Line 75: Once our documentation is available in the docs directory, we can start populating it,
Line 76: beginning with docs/source/index.rst, which will be the entry point for our
Line 77: documentation. If we want to add further sections to it, we have to list them under the
Line 78: toctree section.
Line 79: In our case, we are going to create a section about how to use the software and a reference
Line 80: section for the existing classes and methods. Therefore, we are going to add contacts and
Line 81: reference sections to toctree in the docs/source/index.rst file:
Line 82: Welcome to Contacts's documentation!
Line 83: ===============================
Line 84: .. toctree::
Line 85:    :maxdepth: 2
Line 86:    :caption: Contents:
Line 87:    contacts
Line 88:    reference
Line 89: Now, we could try to build our documentation to see whether the two new sections are
Line 90: listed on the home page. But doing so would actually fail because we haven't yet created
Line 91: the files for those two sections:
Line 92: $ make html
Line 93: Running Sphinx v3.3.0
Line 94: ...
Line 95: docs/source/index.rst:9: WARNING: toctree contains reference to nonexisting
Line 96: document 'contacts'
Line 97: docs/source/index.rst:9: WARNING: toctree contains reference to nonexisting
Line 98: document 'reference'
Line 99: So, we are going to create docs/source/contacts.rst and
Line 100: docs/source/reference.rst files to allow Sphinx to find them.
Line 101: 
Line 102: --- 페이지 233 ---
Line 103: Testing Documentation and Property-Based Testing
Line 104: Chapter 10
Line 105: [ 223 ]
Line 106: Adding a code-based reference
Line 107: First, we will add the reference section, as it's the simplest one. The
Line 108: docs/source/reference.rst file will only contain the title and the directive that will tell
Line 109: Sphinx to document the contacts.Application class based on the docstring we provide
Line 110: in the code itself:
Line 111: ==============
Line 112: Code Reference
Line 113: ==============
Line 114: .. autoclass:: contacts.Application
Line 115:     :members:
Line 116: Recompiling our documentation with make html will now only report the missing
Line 117: contacts.rst file and successfully generate the code reference section. The result will be
Line 118: visible in the docs/build/ directory, hence, opening the docs/build/reference.html
Line 119: file will now show our code reference.
Line 120: The first time we build it, our reference will be mostly empty:
Line 121: Figure 10.1 – Code reference
Line 122: It has a section for the contacts.Application class, but nothing else. This is because the
Line 123: content is taken directly from the code docstrings, and we haven't written any.
Line 124: 
Line 125: --- 페이지 234 ---
Line 126: Testing Documentation and Property-Based Testing
Line 127: Chapter 10
Line 128: [ 224 ]
Line 129: Therefore, we should go back to our contacts/__init__.py file and add a docstring to
Line 130: our Application class and to the Application.run method:
Line 131: class Application:
Line 132:     """Manages a contact book serving the provided commands.
Line 133:     The contact book data is saved in a contacts.json
Line 134:     file in the directory the application is
Line 135:     launched from. Any contacts.json in the directory this
Line 136:     is launched from will be loaded at init time.
Line 137:     A contact is composed by any name followed by a valid
Line 138:     phone number.
Line 139:     """
Line 140:     PHONE_EXPR = re.compile('^[+]?[0-9]{3,}$')
Line 141:     def __init__(self):
Line 142:         self._clear()
Line 143:     def _clear(self):
Line 144:         self._contacts = []
Line 145:     def run(self, text):
Line 146:         """Run a provided command.
Line 147:         :param str text: The string containing the command to run.
Line 148:         Takes the command to run as a string as it would
Line 149:         come from the shell, parses it and runs it.
Line 150:         Each command can support zero or multiple arguments
Line 151:         separate by an empty space.
Line 152:         Currently supported commands are:
Line 153:          - add
Line 154:          - del
Line 155:          - ls
Line 156:         """
Line 157:         ...
Line 158: Now that the class and the method are both documented, we can rebuild our
Line 159: documentation with make html to see whether the reference has been properly generated.
Line 160: 
Line 161: --- 페이지 235 ---
Line 162: Testing Documentation and Property-Based Testing
Line 163: Chapter 10
Line 164: [ 225 ]
Line 165: If everything works as expected, we should see in docs/build/reference.html the
Line 166: documentation we wrote in the code:
Line 167: Figure 10.2 – Reference generated
Line 168: Mixing code and documentation in the source files is an effective technique for ensuring
Line 169: that when the code changes, the documentation is updated too. For example, if we remove
Line 170: a method, we would surely also remove its docstring too, and so the method would also
Line 171: disappear from the documentation. Obviously, we still have to pay attention that what we
Line 172: write in the docstrings makes sense, but at least the structure of our documentation would
Line 173: always be in sync with the structure of our code.
Line 174: 
Line 175: --- 페이지 236 ---
Line 176: Testing Documentation and Property-Based Testing
Line 177: Chapter 10
Line 178: [ 226 ]
Line 179: Writing a verified user guide
Line 180: While it's effective for references, having a reference is usually far from being enough for
Line 181: proper documentation. A usage guide and tutorials are frequently necessary to ensure that
Line 182: the reader understands how the software works.
Line 183: So, to make our documentation more complete, we are going to add a user guide to the
Line 184: docs/source/contacts.rst file.
Line 185: After a brief introduction, the docs/source/contacts.rst file will dive into some real-
Line 186: world examples regarding how to add new contacts and how to list them:
Line 187: ===============
Line 188: Manage Contacts
Line 189: ===============
Line 190: .. contents::
Line 191: Contacts can be managed through an instance of
Line 192: :class:`contacts.Application`, use :meth:`contacts.Application.run`
Line 193: to execute any command like you would in the shell.
Line 194: Adding Contancts
Line 195: ================
Line 196: .. code-block::
Line 197:     app.run("contacts add Name 0123456789")
Line 198: Listing Contacts
Line 199: ================
Line 200: .. code-block::
Line 201:     app.run("contacts ls")
Line 202: 
Line 203: --- 페이지 237 ---
Line 204: Testing Documentation and Property-Based Testing
Line 205: Chapter 10
Line 206: [ 227 ]
Line 207: Now, if we rebuild our documentation with make html, we should no longer get any error
Line 208: and opening docs/build/contacts.html should show the page we just wrote with the
Line 209: two examples:
Line 210: Figure 10.3 – Managing contacts
Line 211: While this shows how we can use the application, it doesn't do anything to ensure that the
Line 212: documentation is in sync with our code. If, for example, we ever replace the
Line 213: Application.run method with Application.execute, the two examples on the page
Line 214: won't even notice and will continue to say that you have to use app.run, which will be
Line 215: incorrect.
Line 216: How can we make sure that the examples and tutorials we write are actually always in sync
Line 217: with how our application works for real? That's exactly what we can do using doctest.
Line 218: Doctest is a Python module and Sphinx extension that allows us to write snippets of code
Line 219: that are tested and verified in our documentation. So, we are going to use doctest to make
Line 220: sure that those two examples actually run and do what we expect.
Line 221: The first thing we have to do is to set up the application in the documentation file. So we
Line 222: are going to add a testsetup directive to docs/source/contacts.rst with the code
Line 223: that is necessary to make sure that the app object exists for real.
Line 224: 
Line 225: --- 페이지 238 ---
Line 226: Testing Documentation and Property-Based Testing
Line 227: Chapter 10
Line 228: [ 228 ]
Line 229: For the sake of order, we are going to add this code at the end of the introductory
Line 230: paragraph, right before the examples themselves:
Line 231: Manage Contacts
Line 232: ===============
Line 233: .. contents::
Line 234: Contacts can be managed through an instance of
Line 235: :class:`contacts.Application`, use :meth:`contacts.Application.run`
Line 236: to execute any command like you would in the shell.
Line 237: .. testsetup::
Line 238:     from contacts import Application
Line 239:     app = Application()
Line 240: Then we are going to replace the two code-block directives with two testcode
Line 241: directives, which means that the examples will actually be executed and checked to ensure
Line 242: that they are not crashing:
Line 243: Adding Contacts
Line 244: ================
Line 245: .. testcode::
Line 246:     app.run("contacts add Name 0123456789")
Line 247: Listing Contacts
Line 248: ================
Line 249: .. testcode::
Line 250:     app.run("contacts ls")
Line 251: code-block directives instruct Sphinx that the content should be formatted as code, but
Line 252: does nothing to ensure that the content is actually valid code that does not crash. While the
Line 253: testcode directive formats the code, it also ensures that it is valid code that can run.
Line 254: Now we are verifying that the two commands can actually run, so if we ever renamed
Line 255: Application.run to Application.execute, our testcode examples would fail to run
Line 256: and so Sphinx would complain that we have to update the documentation.
Line 257: 
Line 258: --- 페이지 239 ---
Line 259: Testing Documentation and Property-Based Testing
Line 260: Chapter 10
Line 261: [ 229 ]
Line 262: But making sure that they can run is not enough. We also want to ensure that they actually
Line 263: do what we expect, that once we add a contact and list them back, we do see the new
Line 264: contact. The doctest module provides us with the testoutput directive to ensure that
Line 265: the previous testcode block provided the expected output. In this case, we are going to
Line 266: add a testoutput directive right after the code block that lists our contacts that will
Line 267: ensure that the contact we just added is listed back:
Line 268: Listing Contacts
Line 269: ================
Line 270: .. testcode::
Line 271:     app.run("contacts ls")
Line 272: .. testoutput::
Line 273:     Name 0123456789
Line 274: If we rerun make html, we are going to see that in the resulting documentation, not much
Line 275: has changed. There is an extra paragraph with the output after the second example, which
Line 276: is good, as it gives a hint of what the expected output of the ls command is, but apart from
Line 277: that, our documentation looks the same as before:
Line 278: Figure 10.4 – Manage Contacts updated
Line 279: 
Line 280: --- 페이지 240 ---
Line 281: Testing Documentation and Property-Based Testing
Line 282: Chapter 10
Line 283: [ 230 ]
Line 284: The real difference happens when we run the make doctest command, which allows us to
Line 285: verify that the examples in our documentation do work correctly:
Line 286: $ make doctest
Line 287: Running Sphinx v3.3.0
Line 288: ...
Line 289: running tests...
Line 290: Document: contacts
Line 291: ------------------
Line 292: 1 items passed all tests:
Line 293:   2 tests in default
Line 294: 2 tests in 1 items.
Line 295: 2 passed and 0 failed.
Line 296: Test passed.
Line 297: Doctest summary
Line 298: ===============
Line 299:     2 tests
Line 300:     0 failures in tests
Line 301:     0 failures in setup code
Line 302:     0 failures in cleanup code
Line 303: build succeeded.
Line 304: doctest found two tests ( the two testcode blocks) within the contacts.rst document
Line 305: and it confirmed that both of them work correctly.
Line 306: If, as we mentioned before, we ever rename the Application.run method to
Line 307: Application.execute, the doctests will immediately point out that both examples are
Line 308: wrong:
Line 309: Document: contacts
Line 310: ------------------
Line 311: **********************************************************************
Line 312: File "contacts.rst", line 41, in default
Line 313: Failed example:
Line 314:     app.run("contacts add Name 0123456789")
Line 315: Exception raised:
Line 316:     Traceback (most recent call last):
Line 317:       File "/usr/lib/python3.8/doctest.py", line 1336, in __run
Line 318:         exec(compile(example.source, filename, "single",
Line 319:       File "<doctest default[0]>", line 1, in <module>
Line 320:         app.run("contacts add Name 0123456789")
Line 321:     AttributeError: 'Application' object has no attribute 'run'
Line 322: **********************************************************************
Line 323: File "contacts.rst", line 55, in default
Line 324: Failed example:
Line 325: 
Line 326: --- 페이지 241 ---
Line 327: Testing Documentation and Property-Based Testing
Line 328: Chapter 10
Line 329: [ 231 ]
Line 330:     app.run("contacts ls")
Line 331: Exception raised:
Line 332:     Traceback (most recent call last):
Line 333:       File "/usr/lib/python3.8/doctest.py", line 1336, in __run
Line 334:         exec(compile(example.source, filename, "single",
Line 335:       File "<doctest default[0]>", line 1, in <module>
Line 336:         app.run("contacts ls")
Line 337:     AttributeError: 'Application' object has no attribute 'run'
Line 338: **********************************************************************
Line 339: 1 items had failures:
Line 340:    2 of 2 in default
Line 341: 2 tests in 1 items.
Line 342: 0 passed and 2 failed.
Line 343: ***Test Failed*** 2 failures.
Line 344: Likewise, if anything goes wrong in our two examples or the contacts listed don't match
Line 345: those in the testoutput section, the make doctest command would report those failures
Line 346: and would inform us that our documentation is not in sync with our code.
Line 347: Adding the make doctest command to our CI pipeline allows us to ensure that with
Line 348: every change of code that affects the documentation, the documentation is updated too,
Line 349: thereby guaranteeing that all our examples in the documentation are verified and up to
Line 350: date with what our code actually does.
Line 351: Property-based testing
Line 352: Now that we know how to have working test suites for both our code and our
Line 353: documentation, the quality of those test suites fully depends on our capability to design
Line 354: and write good tests.
Line 355: There is, by the way, one rule in software testing that can help us design good tests, and
Line 356: this is that errors usually hide in corner cases and limit values. If we have a function that
Line 357: performs division between two numbers, the bugs are probably going to be brought to the
Line 358: surface when zero, the maximum integer value, or negative numbers are passed to the
Line 359: function as arguments. Rarely will we see errors for most common values, such as 2, 3, 4, or
Line 360: 5. That's because developers usually tend to design their code with those common values in
Line 361: mind. The design that comes more naturally is usually the one that works for the most
Line 362: obvious cases, and corner cases rarely come to mind in the first instance.
Line 363: 
Line 364: --- 페이지 242 ---
Line 365: Testing Documentation and Property-Based Testing
Line 366: Chapter 10
Line 367: [ 232 ]
Line 368: Property-based testing comes in handy when easily generating tests that verify those corner
Line 369: cases and limit conditions by ensuring that some properties of the functions and methods
Line 370: we test always hold true. Property-based testing had its origins in the Haskell community,
Line 371: but libraries and frameworks to implement it are now available in most programming
Line 372: languages, including Python.
Line 373: Hypothesis is a library that allows us to implement property-based testing in Python.
Line 374: An example of the properties of a function could be that "for any provided argument, the
Line 375: function should never crash." Not crashing is the most frequently verified property, but it's
Line 376: possible to check any invariant that our method should guarantee. If we have a function
Line 377: such as concat(a: str, b: str, c: str)-> str, a property could be that the
Line 378: returned value should always include b for any provided arguments.
Line 379: Hypothesis helps us define those invariants and then takes care of generating as many tests
Line 380: as possible that assert that those properties always hold true. Usually, this is done by
Line 381: generating tests based on the domain of function arguments and ensuring that the
Line 382: properties hold true for all values. Obviously, testing all possible values would be too
Line 383: cumbersome, or even not doable at all since, for example, the values of the str domain are
Line 384: infinite. For this reason, Hypothesis is smart enough to know which values most frequently
Line 385: cause problems in a domain and will restrict the tests to those, also remembering which
Line 386: values caused problems to our code in the past, so that our test suite remains fast but also
Line 387: effective.
Line 388: The most common usage of the Hypothesis testing library is as a replacement of the
Line 389: pytest.mark.parametrize decorator to automatically generate tests that run for
Line 390: different kinds of values based on the types of arguments.
Line 391: In the case of our contacts book application, we might want to ensure that the contact book
Line 392: works for any kind of name the contacts have. We don't know whether our users will be
Line 393: from the USA, Europe, the Middle-East, or Asia, and so might have totally different
Line 394: concepts of names.
Line 395: 
Line 396: --- 페이지 243 ---
Line 397: Testing Documentation and Property-Based Testing
Line 398: Chapter 10
Line 399: [ 233 ]
Line 400: Using pytest.mark.parametrize, we could write a test that does that for some cases that
Line 401: come to mind:
Line 402: import pytest
Line 403: from contacts import Application
Line 404: @pytest.mark.parametrize("name",
Line 405:     ["Mario Alberto Rossi", "Étienne de La Boétie", "اﻟﺰورق"]
Line 406: )
Line 407: def test_adding_contacts(name):
Line 408:  app = Application()
Line 409:  app.run(f"contacts add {name} 3456789")
Line 410:  assert app._contacts == [(name, "3456789")]
Line 411: The test will pass, and will try for some names and cases that come to mind:
Line 412: $ pytest -v
Line 413: ================= test session starts =================
Line 414: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
Line 415: ...
Line 416: collected 3 items
Line 417: tests/test_properties.py::test_adding_contacts[Mario Alberto Rossi] PASSED
Line 418: [ 33%]
Line 419: tests/test_properties.py::test_adding_contacts[\xc3\x89tienne de La
Line 420: Bo\xc3\xa9tie] PASSED [ 66%]
Line 421: tests/test_properties.py::test_adding_contacts[\u0627\u0644\u0632\u0648\u06
Line 422: 31\u0642] PASSED [100%]
Line 423: ================= 3 passed in 0.04s =================
Line 424: But is this actually a good enough test? Let's see what happens if, instead of picking the
Line 425: values ourselves, we use Hypothesis to generate those tests. Implementing this change is as
Line 426: easy as replacing the parametrize decorator with a hypothesis.given decorator:
Line 427: import hypothesis
Line 428: import hypothesis.strategies as st
Line 429: from contacts import Application
Line 430: @hypothesis.given(st.text())
Line 431: def test_adding_contacts(name):
Line 432:     app = Application()
Line 433:     app.run(f"contacts add {name} 3456789")
Line 434:     assert app._contacts == [(name, "3456789")]
Line 435: 
Line 436: --- 페이지 244 ---
Line 437: Testing Documentation and Property-Based Testing
Line 438: Chapter 10
Line 439: [ 234 ]
Line 440: Now, running the Hypothesis version of the test leads to a much more interesting result
Line 441: compared to the version based on @parametrize; the Hypothesis-based version of the test
Line 442: actually fails:
Line 443: $ pytest -v
Line 444: ================= test session starts =================
Line 445: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
Line 446: ...
Line 447: collected 1 item
Line 448: tests/test_properties.py::test_adding_contacts FAILED [100%]
Line 449: ====================== FAILURES ======================
Line 450: ________________ test_adding_contacts ________________
Line 451:     @given(st.text())
Line 452: > def test_adding_contacts(name):
Line 453: tests/test_properties.py:8:
Line 454: _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
Line 455: tests/test_properties.py:11: in test_adding_contacts
Line 456:     app.run(f"contacts add {name} 3456789")
Line 457: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
Line 458: self = <contacts.Application object at 0x7f9a71fce850>,
Line 459: text = 'contacts add 3456789'
Line 460:     def run(self, text):
Line 461:         ...
Line 462:         if cmd == "add":
Line 463: >           name, num = args.rsplit(maxsplit=1)
Line 464: E           ValueError: not enough values to unpack (expected 2, got 1)
Line 465: src/contacts/__init__.py:48: ValueError
Line 466: --------------------- Hypothesis ---------------------
Line 467: Falsifying example: test_adding_contacts(
Line 468:     name='',
Line 469: )
Line 470: ================= 1 failed in 0.10s =================
Line 471: 
Line 472: --- 페이지 245 ---
Line 473: Testing Documentation and Property-Based Testing
Line 474: Chapter 10
Line 475: [ 235 ]
Line 476: So, Hypothesis actually found a real bug in our software. If we don't provide a name at all,
Line 477: the software, instead of providing an error message, just crashes. We can see that
Line 478: Hypothesis tells us that the example that failed is the one where name='' and PyTest
Line 479: confirms that the string that was executed as a command was text = 'contacts add
Line 480: 3456789'. The line that crashed is the one that splits the name and number out of the add
Line 481: command arguments, so we have to handle the case where we can't split them apart
Line 482: because we only have one argument.
Line 483: To do so, we can go back to the Application.run method and trap the exception that can
Line 484: come out of args.rsplit:
Line 485:         if cmd == "add":
Line 486:             try:
Line 487:                 name, num = args.rsplit(maxsplit=1)
Line 488:             except ValueError:
Line 489:                 print("A contact must provide a name and phone number")
Line 490:                 return
Line 491:             try:
Line 492:                 self.add(name, num)
Line 493:             except ValueError as err:
Line 494:                 print(err)
Line 495:                 return
Line 496: Now, if we rerun our test, we will get a slightly different kind of failure, a failure in the test
Line 497: itself:
Line 498: $ pytest -v
Line 499: ================= test session starts =================
Line 500: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
Line 501: ...
Line 502: collected 1 item
Line 503: tests/test_properties.py::test_adding_contacts FAILED [100%]
Line 504: ====================== FAILURES ======================
Line 505: ________________ test_adding_contacts ________________
Line 506:     @given(st.text())
Line 507: > def test_adding_contacts(name):
Line 508: tests/test_properties.py:8:
Line 509: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
Line 510: tests/test_properties.py:11: in test_adding_contacts
Line 511:     app.run(f"contacts add {name} 3456789")
Line 512: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
Line 513: name = ''
Line 514: 
Line 515: --- 페이지 246 ---
Line 516: Testing Documentation and Property-Based Testing
Line 517: Chapter 10
Line 518: [ 236 ]
Line 519:     @given(st.text())
Line 520:     def test_adding_contacts(name):
Line 521:         app = Application()
Line 522:         app.run(f"contacts add {name} 3456789")
Line 523: >       assert app._contacts == [(name, "3456789")]
Line 524: E       AssertionError: assert [] == [('', '3456789')]
Line 525: E          Right contains one more item: ('', '3456789')
Line 526: E          Full diff:
Line 527: E          - [('', '3456789')]
Line 528: E          + []
Line 529: tests/test_properties.py:15: AssertionError
Line 530: ---------------- Captured stdout call ----------------
Line 531: A contact must provide a name and phone number
Line 532: --------------------- Hypothesis ---------------------
Line 533: Falsifying example: test_adding_contacts(
Line 534:     name='',
Line 535: )
Line 536: ================= 1 failed in 0.10s =================
Line 537: From Captured stdout, we can see that the error we emit when no name is provided was
Line 538: properly reported, but our test failed because the assertion expects that a new contact is
Line 539: always inserted while, in the case of a missing name, no contact gets added to our contact
Line 540: book. So, in this case, Hypothesis found that our test itself is actually incomplete.
Line 541: What we have to do is to change the assertion to ensure that the contact book actually
Line 542: contains what we really expect in the case where no name is provided. In case there is no
Line 543: name, the contact book should just be empty:
Line 544: @given(st.text())
Line 545: def test_adding_contacts(name):
Line 546:     app = Application()
Line 547:     app.run(f"contacts add {name} 3456789")
Line 548:     name = name.strip()
Line 549:     if name:
Line 550:         assert app._contacts == [(name, "3456789")]
Line 551:     else:
Line 552:         assert app._contacts == []
Line 553: At this point, rerunning the test will actually confirm that everything works as expected:
Line 554: $ pytest -v
Line 555: ================= test session starts =================
Line 556: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
Line 557: ...
Line 558: 
Line 559: --- 페이지 247 ---
Line 560: Testing Documentation and Property-Based Testing
Line 561: Chapter 10
Line 562: [ 237 ]
Line 563: collected 1 item
Line 564: tests/test_properties.py::test_adding_contacts PASSED [100%]
Line 565: ================= 1 passed in 0.42s =================
Line 566: We have seen how Hypothesis can help us to identify bugs and design tests, but it can
Line 567: actually do much more. It can even go as far as generating some tests for the most common
Line 568: properties for us.
Line 569: Generating tests for common properties
Line 570: Through the hypothesis write command, we can use Hypothesis to generate tests for
Line 571: use based on some of the most common properties functions might have. For example, if
Line 572: we want to ensure that the Python sorted method is idempotent and calling it twice leads
Line 573: to the exact same result, we can use hypothesis write --idempotent sorted to
Line 574: generate a test that verifies such a property:
Line 575: $ hypothesis write --idempotent sorted
Line 576: from hypothesis import given, strategies as st
Line 577: @given(
Line 578:     iterable=st.one_of(st.iterables(st.integers()),
Line 579: st.iterables(st.text())),
Line 580:     key=st.none(),
Line 581:     reverse=st.booleans(),
Line 582: )
Line 583: def test_idempotent_sorted(iterable, key, reverse):
Line 584:     result = sorted(iterable, key=key, reverse=reverse)
Line 585:     repeat = sorted(result, key=key, reverse=reverse)
Line 586:     assert result == repeat, (result, repeat)
Line 587: Or, we could test that a pair of encode/decode functions leads back to the original result
Line 588: when chained using the hypothesis write --roundtrip generator.
Line 589: If we want to check that for json.loads and json.dumps, for example, we could use
Line 590: hypothesis write --roundtrip json.dumps json.loads, which would generate the
Line 591: following code block:
Line 592: $ hypothesis write --roundtrip json.dumps json.loads
Line 593: import json
Line 594: from hypothesis import given, strategies as st
Line 595: 
Line 596: --- 페이지 248 ---
Line 597: Testing Documentation and Property-Based Testing
Line 598: Chapter 10
Line 599: [ 238 ]
Line 600: @given(
Line 601:     allow_nan=st.booleans(),
Line 602:     check_circular=st.booleans(),
Line 603:     cls=st.none(),
Line 604:     default=st.none(),
Line 605:     ensure_ascii=st.booleans(),
Line 606:     indent=st.none(),
Line 607:     obj=st.nothing(),
Line 608:     object_hook=st.none(),
Line 609:     object_pairs_hook=st.none(),
Line 610:     parse_constant=st.none(),
Line 611:     parse_float=st.none(),
Line 612:     parse_int=st.none(),
Line 613:     separators=st.none(),
Line 614:     skipkeys=st.booleans(),
Line 615:     sort_keys=st.booleans(),
Line 616: )
Line 617: def test_roundtrip_dumps_loads(
Line 618:     allow_nan,
Line 619:     check_circular,
Line 620:     cls,
Line 621:     default,
Line 622:     ensure_ascii,
Line 623:     indent,
Line 624:     obj,
Line 625:     object_hook,
Line 626:     object_pairs_hook,
Line 627:     parse_constant,
Line 628:     parse_float,
Line 629:     parse_int,
Line 630:     separators,
Line 631:     skipkeys,
Line 632:     sort_keys,
Line 633: ):
Line 634:     value0 = json.dumps(
Line 635:         obj=obj,
Line 636:         skipkeys=skipkeys,
Line 637:         ensure_ascii=ensure_ascii,
Line 638:         check_circular=check_circular,
Line 639:         allow_nan=allow_nan,
Line 640:         cls=cls,
Line 641:         indent=indent,
Line 642:         separators=separators,
Line 643:         default=default,
Line 644:         sort_keys=sort_keys,
Line 645:     )
Line 646:     value1 = json.loads(
Line 647:         s=value0,
Line 648: 
Line 649: --- 페이지 249 ---
Line 650: Testing Documentation and Property-Based Testing
Line 651: Chapter 10
Line 652: [ 239 ]
Line 653:         cls=cls,
Line 654:         object_hook=object_hook,
Line 655:         parse_float=parse_float,
Line 656:         parse_int=parse_int,
Line 657:         parse_constant=parse_constant,
Line 658:         object_pairs_hook=object_pairs_hook,
Line 659:     )
Line 660:     assert obj == value1, (obj, value1)
Line 661: When refactoring code, implementing performance optimizations, or modifying code to
Line 662: port it from prior versions of Python, an essential property of the new implementation we
Line 663: are going to write is that it must retain the exact same behavior of the old implementation.
Line 664: The hypothesis write --equivalent command is able to do precisely this.
Line 665: If, for example, we had two helper functions in contacts/utils.py, both meant to sum
Line 666: two numbers, as follows:
Line 667: def sum1(a: int, b: int) -> int:
Line 668:     return a + b
Line 669: def sum2(a: int, b: int) -> int:
Line 670:     return sum((a, b))
Line 671: In that case, hypothesis could generate a test that verifies the fact that both functions lead
Line 672: to the exact same results:
Line 673: $ hypothesis write --equivalent contacts.utils.sum1 contacts.utils.sum2
Line 674: import contacts.utils
Line 675: from hypothesis import given, strategies as st
Line 676: @given(a=st.integers(), b=st.integers())
Line 677: def test_equivalent_sum1_sum2(a, b):
Line 678:     result_sum1 = contacts.utils.sum1(a=a, b=b)
Line 679:     result_sum2 = contacts.utils.sum2(a=a, b=b)
Line 680:     assert result_sum1 == result_sum2, (result_sum1, result_sum2)
Line 681: While most of those tests could be written manually using hypothesis.given, it can be
Line 682: convenient having Hypothesis inspect the functions for you and pick the right types.
Line 683: Especially if you already did the effort of providing type hints for your functions,
Line 684: Hypothesis will usually be able to do the right thing.
Line 685: To know all the generators that are available in your version of Hypothesis, you can run
Line 686: hypothesis write --help.
Line 687: 
Line 688: --- 페이지 250 ---
Line 689: Testing Documentation and Property-Based Testing
Line 690: Chapter 10
Line 691: [ 240 ]
Line 692: Summary
Line 693: In this chapter, we saw how to have tested documentation that can guarantee user guides
Line 694: in sync with our code, and we saw how to make sure that our tests cover limit and corner
Line 695: cases we might not have considered through property-based testing.
Line 696: Hypothesis can take away from you a lot of the effort of providing all possible values to a
Line 697: parameterized test, thereby making writing effective tests much faster, while doctest can
Line 698: ensure that the examples we write in our user guides remain effective in the long term,
Line 699: detecting whether any of them need to be updated when our code changes.
Line 700: In the next chapter, we are going to shift our attention to the web development world,
Line 701: where we will see how to test web applications both from the point of view of functional
Line 702: tests and end-to-end tests.