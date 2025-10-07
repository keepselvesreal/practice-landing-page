Line 1: 
Line 2: --- 페이지 16 ---
Line 3: 1
Line 4: Getting Started with Software
Line 5: Testing
Line 6: Many think that the big step from "coding" to "software engineering" is made by having
Line 7: elegant architectures, well-defined execution plans, and software that moves big
Line 8: companies' processes. This mostly comes from our vision of the classic industrial product
Line 9: development world, where planning mostly mattered more than execution, because the
Line 10: execution was moved forward by an assembly line and software was an expensive internal
Line 11: utility that only big companies could afford
Line 12: As software development science moved forward and matured, it became clear that classic
Line 13: industrial best practices weren't always a great fit for it. The reason being that every
Line 14: software product was very different, due to the technologies involved, the speed at which
Line 15: those technologies evolve, and in the end the fact that different software had to do totally
Line 16: different things. Thus the idea developed that software development was more similar to
Line 17: craftsmanship than to industry.
Line 18: If you embrace that it's very hard, and not very effective, to try to eliminate uncertainty and
Line 19: issues with tons of preparation work due to the very nature of software itself, it becomes
Line 20: evident that the most important part of software development is detecting defects and
Line 21: ensuring it achieves the expected goals. Those two things are usually mostly done by
Line 22: having tests and a fitness function that can verify the software does what we really mean it
Line 23: to – founding pieces of the whole Software Quality Control discipline, which is what this
Line 24: chapter will introduce and, in practice, what this book is all about.
Line 25: In this chapter, we will go through testing software products and the best practices in
Line 26: quality control. We will also introduce automatic tests and how they are superseding
Line 27: manual testing. We will take a look at what Test-Driven Development (TDD) is and how
Line 28: to apply it in Python, giving some guidance on how to distinguish between the various
Line 29: categories of tests, how to implement them, and how to get the right balance between test
Line 30: efficacy and test cost.
Line 31: 
Line 32: --- 페이지 17 ---
Line 33: Getting Started with Software Testing
Line 34: Chapter 1
Line 35: [ 7 ]
Line 36: In this chapter, we will cover the following:
Line 37: Introducing software testing and quality control
Line 38: Introducing automatic tests and test suites
Line 39: Introducing test-driven development and unit tests
Line 40: Understanding integration and functional tests
Line 41: Understanding the testing pyramid and trophy
Line 42: Technical requirements
Line 43: A working Python interpreter is all that's needed.
Line 44: The examples have been written in Python 3.7 but should work in most modern Python
Line 45: versions.
Line 46: You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
Line 47: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter01.
Line 48: Introducing software testing and quality
Line 49: control
Line 50: From the early days, it was clear that like any other machine, software needed a way to 
Line 51: verify it was working properly and was built with no defects.
Line 52: Software development processes have been heavily inspired by manufacturing industry
Line 53: standards, and early on, testing and quality control were introduced into the product
Line 54: development life cycle. So software companies frequently have a quality assurance team
Line 55: that focuses on setting up processes to guarantee robust software and track results.
Line 56: Those processes usually include a quality control process where the quality of the built
Line 57: artifact is assessed before it can be considered ready for users.
Line 58: The quality control process usually achieves such confidence through the execution of a test
Line 59: plan. This is usually a checklist that a dedicated team goes through during the various
Line 60: phases of production to ensure the software behaves as expected.
Line 61: 
Line 62: --- 페이지 18 ---
Line 63: Getting Started with Software Testing
Line 64: Chapter 1
Line 65: [ 8 ]
Line 66: Test plans
Line 67: A test plan is composed of multiple test cases, each specifying the following:
Line 68: Preconditions: What's necessary to be able to verify the case
Line 69: Steps: Actions that have to succeed when executed in the specified order
Line 70: Postconditions: In which state the system is expected to be at the end of the steps
Line 71: A sample test case of software where logging in with a username and password is
Line 72: involved, and we might want to allow the user to reset those, might look like the following
Line 73: table:
Line 74: Test Case: 2.2 - Change User Password
Line 75: Preconditions:
Line 76: • A user, user1 exists
Line 77: • The user is logged in as user1
Line 78: • The user is at the main menu
Line 79: # Action
Line 80: Expected Response
Line 81: Success /
Line 82: Fail
Line 83: 1 Click the change password button. The system shows a dialog to insert a new password.
Line 84: 2 Enter newpass.
Line 85: The dialog shows 7 asterisks in the password field.
Line 86: 3 Click the OK button.
Line 87: The system shows a dialog with a success message.
Line 88: 4 Wait 2 seconds.
Line 89: The success dialog goes away.
Line 90: Postconditions:
Line 91: • The user1 password is now newpass
Line 92: These test cases are divided into cases, are manually verified by a dedicated team, and a
Line 93: sample of them is usually selected to be executed during development, but most of them
Line 94: are checked when the development team declared the work done.
Line 95: This meant that once the team finishes its work, it takes days/weeks for the release to
Line 96: happen, as the whole software has to be verified by humans clicking buttons, with all the
Line 97: unpredictable results that involves, as humans can get distracted, pressing the wrong
Line 98: button or receiving phone calls in the middle of a test case.
Line 99: As software usage became more widespread, and business-to-consumer products became
Line 100: the norm, consumers started to appreciate faster release cycles. Companies that updated
Line 101: their products with new features frequently were those that ended up dominating the
Line 102: market in the long term.
Line 103: 
Line 104: --- 페이지 19 ---
Line 105: Getting Started with Software Testing
Line 106: Chapter 1
Line 107: [ 9 ]
Line 108: If you think about modern release cycles, we are now used to getting a new version of our
Line 109: favorite mobile application weekly. Such applications are probably so complex that they
Line 110: involve thousands of test cases. If all those cases had to be performed by a human, there
Line 111: would be no way for the company to provide you with frequent releases.
Line 112: The worst thing you can do, by the way, is to release a broken product. Your users will lose
Line 113: confidence and will switch to other more reliable competitors if they can't get their job done
Line 114: due to crashes or bugs. So how can we deliver such frequent releases without reducing our
Line 115: test coverage and thus incurring more bugs?
Line 116: The solution came from automating the test process. So while we learned how to detect
Line 117: defects by writing and executing test plans, it's only by making them automatic that we can
Line 118: scale them to the number of cases that will ensure robust software in the long term.
Line 119: Instead of having humans test software, have some other software test it. What a person
Line 120: does in seconds can happen in milliseconds with software and you can run thousands of
Line 121: tests in a few minutes.
Line 122: Introducing automatic tests and test suites
Line 123: Automated testing is, in practice, the art of writing another piece of software to test an
Line 124: original piece of software.
Line 125: As testing a whole piece of software has to take millions of variables and possible code
Line 126: paths into account, a single program trying to test another one would be very complex and
Line 127: hard to maintain. For this reason, it's usually convenient to split that program into smaller
Line 128: isolated programs, each being a test case.
Line 129: Each test case contains all the instructions that are required to set up the target software in a
Line 130: state where the parts that are the test case areas of interest can be tested, the tests can be
Line 131: done, and all the conditions can be verified and reset back to the state of the target software
Line 132: so a subsequent test case can find a known state from which to start.
Line 133: When using the unittest module that comes with the Python Standard Library, each test
Line 134: case is declared by subclassing from the unittest.TestCase class and adding a method
Line 135: whose name starts with test, which will contain the test itself:
Line 136: import unittest
Line 137: class MyTestCase(unittest.TestCase):
Line 138:     def test_one(self):
Line 139:         pass
Line 140: 
Line 141: --- 페이지 20 ---
Line 142: Getting Started with Software Testing
Line 143: Chapter 1
Line 144: [ 10 ]
Line 145: Trying to run our previous test will do nothing by the way:
Line 146: $ python 01_automatictests.py
Line 147: $
Line 148: We declared our test case, but we have nothing that runs it.
Line 149: As for manually executed tests, the automatic tests need someone in charge of gathering all
Line 150: test cases and running them all. That's the role of a test runner.
Line 151: Test runners usually involve a discovery phase (during which they detect all test cases) and
Line 152: a run phase (during which they run the discovered tests).
Line 153: The unittest module provides all the components necessary to build a test runner that does
Line 154: both the discovery and execution of tests. For convenience, it even provides the
Line 155: unittest.main() method, which configures a test runner that, by default, will run the
Line 156: tests in the current module:
Line 157: import unittest
Line 158: class MyTestCase(unittest.TestCase):
Line 159:     def test_one(self):
Line 160:         pass
Line 161: if __name__ == '__main__':
Line 162:     unittest.main()
Line 163: By adding a call to unittest.main() at the end of our tests, Python will automatically
Line 164: execute our tests when the module is invoked:
Line 165: $ python 01_automatictests.py
Line 166: .
Line 167: ----------------------------------------------------------------------
Line 168: Ran 1 test in 0.000s
Line 169: OK
Line 170: We can confirm that the test we cared about was executed by using the -v option to print a
Line 171: more verbose output:
Line 172: $ python 01_automatictests.py -v
Line 173: test_one (__main__.MyTestCase) ... ok
Line 174: ----------------------------------------------------------------------
Line 175: Ran 1 test in 0.000s
Line 176: OK
Line 177: 
Line 178: --- 페이지 21 ---
Line 179: Getting Started with Software Testing
Line 180: Chapter 1
Line 181: [ 11 ]
Line 182: During the discovery phase, unittest.main will look for all classes that inherit from
Line 183: unittest.TestCase within the module that is recognized as the main Python module
Line 184: (sys.modules['__main__']), and all those subclasses will be registered as test cases for
Line 185: the runner.
Line 186: Individual tests are then defined by having methods with names starting with test in the
Line 187: test case classes. This means that if we add more methods with names that don't start with
Line 188: test, they won't be treated as tests:
Line 189: class MyTestCase(unittest.TestCase):
Line 190:     def test_one(self):
Line 191:         pass
Line 192:     def notatest(self):
Line 193:         pass
Line 194: Trying to start the test runner again will continue to run only the test_one test:
Line 195: $ python 01_automatictests.py -v
Line 196: test_one (__main__.MyTestCase) ... ok
Line 197: ----------------------------------------------------------------------
Line 198: Ran 1 test in 0.000s
Line 199: OK
Line 200: In the previous example, only the test_one method was executed as a test, while
Line 201: notatest was recognized as not being a test but instead as a method that we are going to
Line 202: use ourselves in tests.
Line 203: Being able to distinguish between tests (methods whose names start with test_) and other 
Line 204: methods allows us to create helpers and utility methods within our test cases that the
Line 205: individual tests can reuse.
Line 206: Given that a test suite is a collection of multiple test cases, to grow our test suite, we need to
Line 207: be able to actually write more than one single TestCase subclass and run its tests.
Line 208: Multiple test cases
Line 209: We already know that unittest.main is the function in charge of executing our test suite,
Line 210: but how can we make it execute more than one TestCase?
Line 211: 
Line 212: --- 페이지 22 ---
Line 213: Getting Started with Software Testing
Line 214: Chapter 1
Line 215: [ 12 ]
Line 216: The discovery phase of unittest.main (the phase during which unittest.main decides
Line 217: which tests to run) looks for all subclasses or unittest.TestCase.
Line 218: The same way we had MyTestCase tests executed, adding more test cases is as simple as
Line 219: declaring more classes:
Line 220: import unittest
Line 221: class MyTestCase(unittest.TestCase):
Line 222:     def test_one(self):
Line 223:         pass
Line 224:     def notatest(self):
Line 225:         pass
Line 226: class MySecondTestCase(unittest.TestCase):
Line 227:     def test_two(self):
Line 228:         pass
Line 229: if __name__ == '__main__':
Line 230:     unittest.main()
Line 231: Running the 01_automatictests.py module again will lead to both test cases being
Line 232: verified:
Line 233: $ python 01_automatictests.py -v
Line 234: test_two (__main__.MySecondTestCase) ... ok
Line 235: test_one (__main__.MyTestCase) ... ok
Line 236: ----------------------------------------------------------------------
Line 237: Ran 2 tests in 0.000s
Line 238: OK
Line 239: If a test case is particularly complex, it can even be divided into multiple individual tests,
Line 240: each checking a specific subpart of it:
Line 241: class MySecondTestCase(unittest.TestCase):
Line 242:     def test_two(self):
Line 243:         pass
Line 244:     def test_two_part2(self):
Line 245:         pass
Line 246: 
Line 247: --- 페이지 23 ---
Line 248: Getting Started with Software Testing
Line 249: Chapter 1
Line 250: [ 13 ]
Line 251: This allows us to divide the test cases into smaller pieces and eventually share setup and
Line 252: teardown code between the individual tests. The individual tests will be executed by the
Line 253: test runner in alphabetical order, so in this case, test_two will be executed before
Line 254: test_two_part2:
Line 255: $ python 01_automatictests.py -v
Line 256: test_two (__main__.MySecondTestCase) ... ok
Line 257: test_two_part2 (__main__.MySecondTestCase) ... ok
Line 258: test_one (__main__.MyTestCase) ... ok
Line 259: In that run of the tests, we can see that MySecondTestCase was actually executed before
Line 260: MyTestCase because "MyS" is less than "MyT".
Line 261: In any case, generally, it's a good idea to consider your tests as being executed in a random
Line 262: order and to not rely on any specific sequence of execution, because other developers might
Line 263: add more test cases, add more individual tests to a case, or rename classes, and you want to
Line 264: allow those changes with no additional issues. Especially since relying on a specific known
Line 265: execution order of your tests might limit your ability to parallelize your test suite and run
Line 266: test cases concurrently, which will be required as the size of your test suite grows.
Line 267: Once more tests are added, adding them all into the same class or file quickly gets
Line 268: confusing, so it's usually a good idea to start organizing tests.
Line 269: Organizing tests
Line 270: If you have more than a few tests, it's generally a good idea to group your test cases into
Line 271: multiple modules and create a tests directory where you can gather the whole test plan:
Line 272: ├── 02_tests
Line 273: │   ├── tests_div.py
Line 274: │   └── tests_sum.py
Line 275: 
Line 276: --- 페이지 24 ---
Line 277: Getting Started with Software Testing
Line 278: Chapter 1
Line 279: [ 14 ]
Line 280: Those tests can be executed through the unittest discover mode, which will look for all
Line 281: modules with names matching test*.py within a target directory and will run all the
Line 282: contained test cases:
Line 283: $ python -m unittest discover 02_tests -v
Line 284: test_div0 (tests_div.TestDiv) ... ok
Line 285: test_div1 (tests_div.TestDiv) ... ok
Line 286: test_sum0 (tests_sum.TestSum) ... ok
Line 287: test_sum1 (tests_sum.TestSum) ... ok
Line 288: ----------------------------------------------------------------------
Line 289: Ran 4 tests in 0.000s
Line 290: OK
Line 291: You can even pick which tests to run by filtering them with a substring with the -k
Line 292: parameter; for example, -k sum will only run tests that contain "sum" in their names:
Line 293: $ python -m unittest discover 02_tests -k sum -v
Line 294: test_sum0 (tests_sum.TestSum) ... ok
Line 295: test_sum1 (tests_sum.TestSum) ... ok
Line 296: ----------------------------------------------------------------------
Line 297: Ran 2 tests in 0.000s
Line 298: OK
Line 299: And yes, you can nest tests further as long as you use Python packages:
Line 300: ├── 02_tests
Line 301: │   ├── tests_div
Line 302: │   │   ├── __init__.py
Line 303: │   │   └── tests_div.py
Line 304: │   └── tests_sum.py
Line 305: Running tests structured like the previous directory tree will properly navigate into the
Line 306: subfolders and spot the nested tests.
Line 307: So running unittest in discovery mode over that direction will properly find the
Line 308: TestDiv and TestSum classes declared inside the files even when they are nested in
Line 309: subdirectories:
Line 310: $ python -m unittest discover 02_tests -v
Line 311: test_div0 (tests_div.tests_div.TestDiv) ... ok
Line 312: test_div1 (tests_div.tests_div.TestDiv) ... ok
Line 313: test_sum0 (tests_sum.TestSum) ... ok
Line 314: test_sum1 (tests_sum.TestSum) ... ok
Line 315: 
Line 316: --- 페이지 25 ---
Line 317: Getting Started with Software Testing
Line 318: Chapter 1
Line 319: [ 15 ]
Line 320: ----------------------------------------------------------------------
Line 321: Ran 4 tests in 0.000s
Line 322: OK
Line 323: Now that we know how to write tests, run them, and organize multiple tests in a test suite.
Line 324: We can start introducing the concept of TDD and how unit tests allow us to achieve it.
Line 325: Introducing test-driven development and
Line 326: unit tests
Line 327: Our tests in the previous section were all empty. The purpose was to showcase how a test
Line 328: suite can be made, executed, and organized in test cases and individual tests, but in the
Line 329: end, our tests did not test much.
Line 330: Most individual tests are written following the "Arrange, Act, Assert" pattern:
Line 331: First, prepare any state you will need to perform the action you want to try.
Line 332: Then perform that action.
Line 333: Finally, verify the consequences of the action are those that you expected.
Line 334: Generally speaking, in most cases, the action you are going to test is "calling a function,"
Line 335: and for code that doesn't depend on any shared state, the state is usually all contained
Line 336: within the function arguments, so the Arrange phase might be omitted. Finally, the Assert
Line 337: phase will verify that the called function did what you expected, which usually means
Line 338: verifying the returned value and any effect at a distance that function might have:
Line 339: import unittest
Line 340: class SomeTestCase(unittest.TestCase):
Line 341:     def test_something(self):
Line 342:         # Arrange phase, nothing to prepare here.
Line 343:         # Act phase, call do_something
Line 344:         result = do_something()
Line 345:         # Assert phase, verify do_something did what we expect.
Line 346:         assert result == "did something"
Line 347: The test_something test is structured as a typical test with those three phases explicitly
Line 348: exposed, with the do_something call representing the Act phase and the final assert
Line 349: statement representing the Assertion phase.
Line 350: 
Line 351: --- 페이지 26 ---
Line 352: Getting Started with Software Testing
Line 353: Chapter 1
Line 354: [ 16 ]
Line 355: Now that we know how to structure tests properly, we can see how they are helpful in
Line 356: implementing TDD and how unit tests are usually expressed.
Line 357: Test-driven development
Line 358: Tests can do more than just validating our code is doing what we expect. The TDD process
Line 359: argues that tests are essential in designing code itself.
Line 360: Writing tests before implementing the code itself forces us to reason about our
Line 361: requirements. We must explicitly express requirements in a strict, well-defined way –
Line 362: clearly enough that a computer itself (computers are known for not being very flexible in
Line 363: understanding things) can understand them and state whether the code you will be writing
Line 364: next satisfies those requirements.
Line 365: First, you write a test for your primary scenario—in this case, testing that doing 3+2 does
Line 366: return 5 as the result:
Line 367: import unittest
Line 368: class AdditionTestCase(unittest.TestCase):
Line 369:     def test_main(self):
Line 370:         result = addition(3, 2)
Line 371:         assert result == 5
Line 372: Then you make sure it fails, which proves you are really testing something:
Line 373: $ python 03_tdd.py
Line 374: E
Line 375: ======================================================================
Line 376: ERROR: test_main (__main__.AdditionTestCase)
Line 377: ----------------------------------------------------------------------
Line 378: Traceback (most recent call last):
Line 379:   File "03_tdd.py", line 5, in test_main
Line 380:     result = addition(3, 2)
Line 381: NameError: name 'addition' is not defined
Line 382: ----------------------------------------------------------------------
Line 383: Ran 1 test in 0.000s
Line 384: FAILED (errors=1)
Line 385: Finally, you write the real code that is expected to make the test pass:
Line 386: def addition(arg1, arg2):
Line 387:     return arg1 + arg2
Line 388: 
Line 389: --- 페이지 27 ---
Line 390: Getting Started with Software Testing
Line 391: Chapter 1
Line 392: [ 17 ]
Line 393: And confirm it makes your test pass:
Line 394: $ python 03_tdd.py
Line 395: .
Line 396: ----------------------------------------------------------------------
Line 397: Ran 1 test in 0.000s
Line 398: OK
Line 399: Once the test is done and it passes, we can revise our implementation and refactor the code.
Line 400: If the test still passes, it means we haven't changed the behavior and we are still doing what
Line 401: we wanted.
Line 402: For example, we can change our addition function to unpack arguments instead of having
Line 403: to specify the two arguments it can receive:
Line 404: def addition(*args):
Line 405:     a1, a2 = args
Line 406:     return a1 + a2
Line 407: If our test still passes, it means we haven't changed the behavior, and it's still as good as
Line 408: before from that point of view:
Line 409: $ python 03_tdd.py
Line 410: .
Line 411: ----------------------------------------------------------------------
Line 412: Ran 1 test in 0.000s
Line 413: OK
Line 414: Test-driven development is silent about when you reach a robust code base that satisfies all
Line 415: your needs. Obviously, you should at least make sure there are enough tests to cover all
Line 416: your requirements.
Line 417: But as testing guides us in the process of development, development should guide us in the
Line 418: process of testing.
Line 419: Looking at the code helps us come up with more white-box tests; tests that we can think of
Line 420: because we know how the code works internally. And while those tests might not
Line 421: guarantee that we are satisfying more requirements, they help us guarantee that our code
Line 422: is robust in most conditions, including corner cases.
Line 423: 
Line 424: --- 페이지 28 ---
Line 425: Getting Started with Software Testing
Line 426: Chapter 1
Line 427: [ 18 ]
Line 428: While historically, test-first and test-driven were synonyms, today that's considered the one
Line 429: major difference with the test-first approach. In TDD we don't have the expectation to be
Line 430: able to write all tests first. Nor is it generally a good idea in the context of extreme
Line 431: programming practices, because you still don't know what the resulting interface that you
Line 432: want to test will be. What you want to test evolves as the code evolves, and we know that
Line 433: the code will evolve after every passing test, as a passing test gives us a chance for
Line 434: refactoring.
Line 435: In our prior example, as we changed our addition function to accept a variable number of
Line 436: arguments, a reasonable question would be, "But what happens if I pass three arguments? Or
Line 437: none?" And our requirements, expressed by the tests, as a consequence, have to grow to
Line 438: support a variable number of arguments:
Line 439:     def test_threeargs(self):
Line 440:         result = addition(3, 2, 1)
Line 441:         assert result == 6
Line 442:     def test_noargs(self):
Line 443:         result = addition()
Line 444:         assert result == 0
Line 445: So, writing code helped us come up with more tests to verify the conditions that came to
Line 446: mind when looking at the code like a white box:
Line 447: $ python 03_tdd.py
Line 448: .EE
Line 449: ======================================================================
Line 450: ERROR: test_noargs (__main__.AdditionTestCase)
Line 451: ----------------------------------------------------------------------
Line 452: Traceback (most recent call last):
Line 453:   File "03_tdd.py", line 13, in test_noargs
Line 454:     result = addition()
Line 455:   File "03_tdd.py", line 18, in addition
Line 456:     a1, a2 = args
Line 457: ValueError: not enough values to unpack (expected 2, got 0)
Line 458: ======================================================================
Line 459: ERROR: test_threeargs (__main__.AdditionTestCase)
Line 460: ----------------------------------------------------------------------
Line 461: Traceback (most recent call last):
Line 462:   File "03_tdd.py", line 9, in test_threeargs
Line 463:     result = addition(3, 2, 1)
Line 464:   File "03_tdd.py", line 18, in addition
Line 465:     a1, a2 = args
Line 466: ValueError: too many values to unpack (expected 2)
Line 467: 
Line 468: --- 페이지 29 ---
Line 469: Getting Started with Software Testing
Line 470: Chapter 1
Line 471: [ 19 ]
Line 472: ----------------------------------------------------------------------
Line 473: Ran 3 tests in 0.001s
Line 474: FAILED (errors=2)
Line 475: And adding those failing tests helps us come up with more, and better, code that now
Line 476: properly handles the cases where any number of arguments is passed to our addition
Line 477: function:
Line 478: def addition(*args):
Line 479:     total = 0
Line 480:     for a in args:
Line 481:         total += a
Line 482:     return total
Line 483: Our addition function will now just iterate over the provided arguments, adding them to
Line 484: the total. Thus if no argument is provided, it will just return 0 because nothing was added
Line 485: to it.
Line 486: If we run our test suite again, we will be able to confirm that both our new tests now pass,
Line 487: and thus we achieved what we wanted to:
Line 488: $ python 03_tdd.py
Line 489: ...
Line 490: ----------------------------------------------------------------------
Line 491: Ran 3 test in 0.001s
Line 492: OK
Line 493: Writing tests and writing code should interleave continuously. If you find yourself
Line 494: spending all your time on one or the other, you are probably moving away from the
Line 495: benefits that TDD can give you, as the two phases are meant to support each other.
Line 496: There are many kinds of tests you are going to write in your test suite during your
Line 497: development practice, but the most common one is probably going to be test units.
Line 498: Test units
Line 499: The immediate question once we know how to arrange our tests, is usually "what should I
Line 500: test?". The answer to that is usually "it depends."
Line 501: 
Line 502: --- 페이지 30 ---
Line 503: Getting Started with Software Testing
Line 504: Chapter 1
Line 505: [ 20 ]
Line 506: You usually want tests that assert that the feature you are providing to your users does
Line 507: what you expect. But do tests do nothing to guarantee that, internally, the components that
Line 508: collaborate with that feature behave correctly? The exposed feature might be working as a
Line 509: very lucky side effect of 200 different bugs in the underlying components.
Line 510: So it's generally a good idea to test those units individually and verify that they all work as
Line 511: expected.
Line 512: What are those units? Well, the answer is "it depends" again.
Line 513: In most cases, you could discuss that in procedural programming, the units are the
Line 514: individual functions, while in object-oriented programming, it might be defined as a single
Line 515: class. But classes, while we usually do our best to try to isolate them to a single
Line 516: responsibility, might cover multiple different behaviors based on which method you call.
Line 517: So they actually act as multiple components in our system, and in such cases, they should
Line 518: be considered as separate units.
Line 519: In practice, a unit is the smallest testable entity that participates in your software.
Line 520: If we have a piece of software that does "multiplication," we might implement it as a main
Line 521: function that fetches the two provided arguments and calls a multiply function to do the
Line 522: real job:
Line 523: def main():
Line 524:     import sys
Line 525:     num1, num2 = sys.argv[1:]
Line 526:     num1, num2 = int(num1), int(num2)
Line 527:     print(multiply(num1, num2))
Line 528: def multiply(num1, num2):
Line 529:     total = 0
Line 530:     for _ in range(num2):
Line 531:         total = addition(total, num1)
Line 532:     return total
Line 533: def addition(*args):
Line 534:     total = 0
Line 535:     for a in args:
Line 536:         total += a
Line 537:     return total
Line 538: In such a case, both addition and multiply are units of our software.
Line 539: 
Line 540: --- 페이지 31 ---
Line 541: Getting Started with Software Testing
Line 542: Chapter 1
Line 543: [ 21 ]
Line 544: While addition can be tested in isolation, multiply must use addition to work.
Line 545: multiply is thus defined as a sociable unit, while addition is a solitary unit.
Line 546: Sociable unit tests are frequently also referred to as component tests. Your architecture 
Line 547: mostly defines the distinction between a sociable unit test and a component test and it's
Line 548: hard to state exactly when one name should be preferred over the other.
Line 549: While sociable units usually lead to more complete testing, they are slower, require more
Line 550: effort during the Arrange phase, and are less isolated. This means that a change in
Line 551: addition can make a test of multiply fail, which tells us that there is a problem, but also
Line 552: makes it harder to guess where the problem lies exactly.
Line 553: In the subsequent chapters, we will see how sociable units can be converted into solitary
Line 554: units by using test doubles. If you have complete testing coverage for the underlying units,
Line 555: solitary unit tests can reach a level of guarantee that is similar to that of sociable units with
Line 556: must less effort and a faster test suite.
Line 557: Test units are usually great at testing software from a white-box perspective, but that's not
Line 558: the sole point of view we should account for in our testing strategy. Test units guarantee
Line 559: that the code does what the developer meant it to, but do little to guarantee that the code
Line 560: does what the user needs. Integration and functional tests are usually more effective in
Line 561: terms of testing at that level of abstraction.
Line 562: Understanding integration and functional
Line 563: tests
Line 564: Testing all our software with solitary units can't guarantee that it's really working as
Line 565: expected. Unit testing confirms that the single components are working as expected, but
Line 566: doesn't give us any confidence about their effectiveness when paired together.
Line 567: It's like testing an engine by itself, testing the wheels by themselves, testing the gears, and
Line 568: then expecting the car to work. We wouldn't be accounting for any issues introduced in the
Line 569: assembly process.
Line 570: So we have a need to verify that those modules do work as expected when paired together.
Line 571: 
Line 572: --- 페이지 32 ---
Line 573: Getting Started with Software Testing
Line 574: Chapter 1
Line 575: [ 22 ]
Line 576: That's exactly what integration tests are expected to do. They take the modules we tested
Line 577: individually and test them together.
Line 578: Integration tests
Line 579: The scope of integration tests is blurry. They might integrate two modules, or they might
Line 580: integrate tens of them. While they are more effective when integrating fewer modules, it's
Line 581: also more expensive to move forward as an approach and most developers argue that the
Line 582: effort of testing all possible combinations of modules in isolation isn't usually worth the
Line 583: benefit.
Line 584: The boundary between unit tests made of sociable units and integration tests is not easy to
Line 585: explain. It usually depends on the architecture of the software itself. We could consider
Line 586: sociable units tests those tests that test units together that are inside the same architectural
Line 587: components, while we could consider integration tests those tests that test different
Line 588: architectural components together.
Line 589: In an application, two separate services will be involved: Authorization and
Line 590: Authentication. Authentication takes care of letting the user in and identifying them,
Line 591: while Authorization tells us what the user can do once it is authenticated. We can see
Line 592: this in the following code block:
Line 593: class Authentication:
Line 594:     USERS = [{"username": "user1",
Line 595:               "password": "pwd1"}]
Line 596:     def login(self, username, password):
Line 597:         u = self.fetch_user(username)
Line 598:         if not u or u["password"] != password:
Line 599:             return None
Line 600:         return u
Line 601:     def fetch_user(self, username):
Line 602:         for u in self.USERS:
Line 603:             if u["username"] == username:
Line 604:                 return u
Line 605:         else:
Line 606:             return None
Line 607: class Authorization:
Line 608:     PERMISSIONS = [{"user": "user1",
Line 609:                     "permissions": {"create", "edit", "delete"}}]
Line 610: 
Line 611: --- 페이지 33 ---
Line 612: Getting Started with Software Testing
Line 613: Chapter 1
Line 614: [ 23 ]
Line 615:     def can(self, user, action):
Line 616:         for u in self.PERMISSIONS:
Line 617:             if u["user"] == user["username"]:
Line 618:                 return action in u["permissions"]
Line 619:         else:
Line 620:             return False
Line 621: Our classes are composed of two primary methods: Authentication.login and
Line 622: Authorization.can. The first is in charge of authenticating the user with a username and
Line 623: password and returning the authenticated user, while the second is in charge of verifying
Line 624: that a user can do a specific action. Tests for those methods can be considered unit tests.
Line 625: So TestAuthentication.test_login will be a unit test that verifies the behavior of the
Line 626: Authentication.login unit, while TestAuthorization.test_can will be a unit test
Line 627: that verifies the behavior of the Authorization.can unit:
Line 628: class TestAuthentication(unittest.TestCase):
Line 629:     def test_login(self):
Line 630:         auth = Authentication()
Line 631:         auth.USERS = [{"username": "testuser", "password": "testpass"}]
Line 632:         resp = auth.login("testuser", "testpass")
Line 633:         assert resp == {"username": "testuser", "password": "testpass"}
Line 634: class TestAuthorization(unittest.TestCase):
Line 635:     def test_can(self):
Line 636:         authz = Authorization()
Line 637:         authz.PERMISSIONS = [{"user": "testuser", "permissions":
Line 638:                               {"create"}}]
Line 639:         resp = authz.can({"username": "testuser"}, "create")
Line 640:         assert resp is True
Line 641: Here, we have the notable difference that TestAuthentication.test_login is a sociable
Line 642: unit test as it depends on Authentication.fetch_user while testing
Line 643: Authentication.login, and TestAuthorization.test_can is instead a solitary unit
Line 644: test as it doesn't depend on any other unit.
Line 645: So where is the integration test?
Line 646: 
Line 647: --- 페이지 34 ---
Line 648: Getting Started with Software Testing
Line 649: Chapter 1
Line 650: [ 24 ]
Line 651: The integration test will happen once we join those two components of our architecture
Line 652: (authorization and authentication) and test them together to confirm that we can actually
Line 653: have a user log in and verify their permissions:
Line 654: class TestAuthorizeAuthenticatedUser(unittest.TestCase):
Line 655:     def test_auth(self):
Line 656:         auth = Authentication()
Line 657:         authz = Authorization()
Line 658:         auth.USERS = [{"username": "testuser", "password": "testpass"}]
Line 659:         authz.PERMISSIONS = [{"user": "testuser",
Line 660:                               "permissions": {"create"}}]
Line 661:         u = auth.login("testuser", "testpass")
Line 662:         resp = authz.can(u, "create")
Line 663:         assert resp is True
Line 664: Generally, it's important to be able to run your integration tests independently from your
Line 665: unit tests, as you will want to be able to run the unit tests continuously during development
Line 666: on every change:
Line 667: $ python 05_integration.py TestAuthentication TestAuthorization
Line 668: ........
Line 669: ----------------------------------------------------------------------
Line 670: Ran 8 tests in 0.000s
Line 671: OK
Line 672: While unit tests are usually verified frequently during the development cycle, it's common
Line 673: to run your integration tests only when you've reached a stable point where your unit tests
Line 674: all pass:
Line 675: $ python 05_integration.py TestAuthorizeAuthenticatedUser
Line 676: .
Line 677: ----------------------------------------------------------------------
Line 678: Ran 1 test in 0.000s
Line 679: OK
Line 680: As you know that the units that you wrote or modified do what you expected, running
Line 681: the TestAuthorizeAuthenticatedUser case only will confirm that those entities work
Line 682: together as expected.
Line 683: Integration tests integrate multiple components, but they actually divide themselves into
Line 684: many different kinds of tests depending on their purpose, with the most common kind
Line 685: being functional tests.
Line 686: 
Line 687: --- 페이지 35 ---
Line 688: Getting Started with Software Testing
Line 689: Chapter 1
Line 690: [ 25 ]
Line 691: Functional tests
Line 692: Integration tests can be very diverse. As you start integrating more and more components,
Line 693: you move toward a higher level of abstraction, and in the end, you move so far from the
Line 694: underlying components that people feel the need to distinguish those kinds of tests as they
Line 695: offer different benefits, complexities, and execution times.
Line 696: That's why the naming of functional tests, end-to-end tests, system tests, acceptance tests,
Line 697: and so on all takes place.
Line 698: Overall, those are all forms of integration tests; what changes are their goal and purpose:
Line 699: Functional tests tend to verify that we are exposing to our users the feature we
Line 700: actually intended. They don't care about intermediate results or side-effects; they
Line 701: just verify that the end result for the user is the one the specifications described,
Line 702: thus they are always black-box tests.
Line 703: End-to-End (E2E) tests are a specific kind of functional test that involves the
Line 704: vertical integration of components. The most common E2E tests are where
Line 705: technologies such as Selenium are involved in accessing a real application
Line 706: instance through a web browser.
Line 707: System tests are very similar to functional tests themselves, but instead of testing
Line 708: a single feature, they usually test a whole journey of the user across the system.
Line 709: So they usually simulate real usage patterns of the user to verify that the system
Line 710: as a whole behaves as expected.
Line 711: Acceptance tests are a kind of functional test that is meant to confirm that the
Line 712: implementation of the feature does behave as expected. They usually express the
Line 713: primary usage flow of the feature, leaving less common flows for other
Line 714: integration tests, and are frequently provided by the specifications themselves to
Line 715: help the developer confirm that they implemented what was expected.
Line 716: But those are not the only kinds of integration that people refer to; new types are
Line 717: continuously defined in the effort to distinguish the goals of tests and responsibilities.
Line 718: Component tests, contract tests, and many others are kinds of tests whose goal is to verify
Line 719: integration between different pieces of the software at different layers. Overall, you
Line 720: shouldn't be ashamed of asking your colleagues what they mean exactly when they use
Line 721: those names, because you will notice each one of them will value different properties of
Line 722: those tests when classifying them into the different categories.
Line 723: The general distinction to keep in mind when distinguishing between integration tests and
Line 724: functional tests is that unit and integration tests aim to test the implementation, while
Line 725: functional tests aim to test the behavior.
Line 726: 
Line 727: --- 페이지 36 ---
Line 728: Getting Started with Software Testing
Line 729: Chapter 1
Line 730: [ 26 ]
Line 731: How you do that can easily involve the same exact technologies and it's just a matter of
Line 732: different goals. Properly covering the behavior of your software with the right kind of tests
Line 733: can be the difference between buggy software and reliable software. That's why there has
Line 734: been a long debate about how to structure test suites, leading to the testing pyramid and
Line 735: the testing trophy as the most widespread models of test distribution.
Line 736: Understanding the testing pyramid and
Line 737: trophy
Line 738: Given the need to provide different kinds of tests – unit, integration, and E2E as each one of
Line 739: them has different benefits and costs, the next immediate question is how do we get the
Line 740: right balance?
Line 741: Each kind of test comes with a benefit and a cost, so it's a matter of finding where we get
Line 742: the best return on investment:
Line 743: E2E tests verify the real experience of what the user faces. They are, in theory, the
Line 744: most realistic kind of tests and can detect problems such as incompatibilities with
Line 745: specific platforms (for example, browsers) and exercise our system as a whole.
Line 746: But when something goes wrong, it is hard to spot where the problem lies. They
Line 747: are very slow and tend to be flaky (failing for reasons unrelated to our software,
Line 748: such as network conditions).
Line 749: Integration tests usually provide a reasonable guarantee that the software is
Line 750: doing what it is expected to do and are fairly robust to internal implementation
Line 751: changes, requiring less frequent refactoring when the internals of the software
Line 752: change. But they can still get very slow if your system involves writes to database
Line 753: services, the rendering of page templates, routing HTTP requests, and generally
Line 754: slow parts. And when something goes wrong, we might have to go through tens
Line 755: of layers before being able to spot where the problem is.
Line 756: Unit tests can be very fast (especially when talking of solitary units) and provide
Line 757: very pinpointed information about where problems are. But they can't always 
Line 758: guarantee that the software as a whole does what it's expected to do and can
Line 759: make changing implementation details expensive because a change to internals
Line 760: that don't impact the software behavior might require changing tens of unit tests.
Line 761: Each of them has its own pros and cons, and the development community has long argued
Line 762: how to get the right balance.
Line 763: The two primary models that have emerged are the testing pyramid and the testing trophy,
Line 764: named after their shapes.
Line 765: 
Line 766: --- 페이지 37 ---
Line 767: Getting Started with Software Testing
Line 768: Chapter 1
Line 769: [ 27 ]
Line 770: The testing pyramid
Line 771: The testing pyramid originates from Mike Cohn's Succeeding with Agile book, where the two
Line 772: rules of thumb are "Write test with different granularities" (so you should have unit,
Line 773: integration, E2E, and so on...) and "the more you get high level, the less you should test" (so you
Line 774: should have tons of unit tests, and a few E2E tests).
Line 775: While different people will argue about which different layers are contained within it, the
Line 776: testing pyramid can be simplified to look like this:
Line 777: Figure 1.1 – Testing pyramid
Line 778: The tip of the pyramid is narrow, thus meaning we have fewer of those tests, while the base
Line 779: is wider, meaning we should mostly cover code with those kinds of tests. So, as we move
Line 780: down through the layers, the lower we get, the more tests we should have.
Line 781: The idea is that as unit tests are fast to run and expose pinpointed issues early on, you
Line 782: should have a lot of them and shrink the number of tests as they move to higher layers and
Line 783: thus get slower and vaguer about what's broken.
Line 784: The testing pyramid is probably the most widespread practice for organizing tests and
Line 785: usually pairs well with test-driven development as unit tests are the founding tool for the
Line 786: TDD process.
Line 787: 
Line 788: --- 페이지 38 ---
Line 789: Getting Started with Software Testing
Line 790: Chapter 1
Line 791: [ 28 ]
Line 792: The other most widespread model is the testing trophy, which instead emphasizes
Line 793: integration tests.
Line 794: The testing trophy
Line 795: The testing trophy originates from a phrase by Guillermo Rauch, the author of Socket.io
Line 796: and many other famous JavaScript-based technologies. Guillermo stated that developers
Line 797: should "Write tests. Not too many. Mostly integration."
Line 798: Like Mike Cohn, he clearly states that tests are the foundation of any effective software
Line 799: development practice, but he argues that they have a diminishing return and thus it's
Line 800: important to find the sweet spot where you get the best return on the time spent writing
Line 801: tests.
Line 802: That sweet spot is expected to live in integration tests because you usually need fewer of
Line 803: them to spot real problems, they are not too bound to implementation details, and they are
Line 804: still fast enough that you can afford to write a few of them.
Line 805: So the testing trophy will look like this:
Line 806: Figure 1.2 – Testing trophy
Line 807: 
Line 808: --- 페이지 39 ---
Line 809: Getting Started with Software Testing
Line 810: Chapter 1
Line 811: [ 29 ]
Line 812: As you probably saw, the testing trophy puts a lot of value on static tests too, because the
Line 813: whole idea of the testing trophy is that what is really of value is the return on investment,
Line 814: and static checks are fairly cheap, up to the point that most development environments run
Line 815: them in real time. Linters, type checkers, and more advanced kinds of type analyzers are
Line 816: cheap enough that it would do no good to ignore them even if they are rarely able to spot
Line 817: bugs in your business logic.
Line 818: Unit tests instead can cost developers time with the need to adapt them due to internal
Line 819: implementation detail changes that don't impact the final behavior of the software in any
Line 820: way, and thus the effort spent on them should be kept under control.
Line 821: Those two models are the most common ways to distribute your tests, but more best
Line 822: practices are involved when thinking of testing distribution and coverage.
Line 823: Testing distribution and coverage
Line 824: While the importance of testing is widely recognized, there is also general agreement that
Line 825: test suites have a diminishing return.
Line 826: There is little point in wasting hours on testing plain getters and setters or testing
Line 827: internal/private methods. The sweet spot is said to be around 80% of code coverage, even
Line 828: though I think that really depends on the language in use – the more expressive your
Line 829: language is, the less code you have to write to perform complex actions. And all complex
Line 830: actions should be properly tested, so in the case of Python, the sweet spots probably lies
Line 831: more in the range of 90%. But there are cases, such as porting projects from Python 2 to
Line 832: Python 3, where code coverage of 100% is the only way you can confirm that you haven't
Line 833: changed any behavior at all in the process of porting your code base.
Line 834: Last but not least, most testing practices related to test-driven development take care of the
Line 835: testing practice up to the release point. It's important to keep in mind that when the
Line 836: software is released, the testing process hasn't finished.
Line 837: Many teams forget to set up proper system tests and don't have a way to identify and
Line 838: reproduce issues that can only happen in production environments with real concurrent
Line 839: users and large amounts of data. Having staging environments and a suite to simulate
Line 840: incidents or real users' behaviors might be the only way to spot bugs that only happen after
Line 841: days of continuous use of the system. And some companies go as far as testing the
Line 842: production system with tools that inject real problems continuously for the sole purpose of
Line 843: verifying that the system is solid.
Line 844: 
Line 845: --- 페이지 40 ---
Line 846: Getting Started with Software Testing
Line 847: Chapter 1
Line 848: [ 30 ]
Line 849: Summary
Line 850: As we saw in the sections about integration tests, functional tests, and the testing
Line 851: pyramid/trophy models, there are many different visions about what should be tested, with
Line 852: which goals in mind, and how test suites should be organized. Getting this right can impact
Line 853: how much you trust your automatic test suite, and thus how much you evolve it because it
Line 854: provides you with value.
Line 855: Learning to do proper automated testing is the gateway to major software development
Line 856: boosts, opening possibilities for practices such as continuous integration and continuous
Line 857: delivery, which would otherwise be impossible without a proper test suite.
Line 858: But testing isn't easy; it comes with many side-effects that are not immediately obvious, and
Line 859: for which the software development industry started to provide tools and best practices
Line 860: only recently. So in the next chapters, we will look at some of those best practices and tools
Line 861: that can help you write a good, easily maintained test suite.