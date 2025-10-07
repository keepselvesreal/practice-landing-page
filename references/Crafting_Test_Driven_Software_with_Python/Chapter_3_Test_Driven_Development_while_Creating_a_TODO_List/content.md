Line 1: 
Line 2: --- 페이지 77 ---
Line 3: 3
Line 4: Test-Driven Development while
Line 5: Creating a TODO List
Line 6: No programmer ever releases a software without having tested it – even for the most basic
Line 7: proof of concept and rough hack, the developer will run it once to see that it at least starts
Line 8: and resembles what they had in mind.
Line 9: But to test, as a verb, usually ends up meaning clicking buttons here and there to get a
Line 10: vague sense of confidence that the software does what we intended. This is different from
Line 11: test as a noun, which means a set of written-out checks that our software must pass to
Line 12: confirm it does what we wanted.
Line 13: Apart from being more reliable, written-out checks force us to think about what the code
Line 14: must do. They force us to get into the details and think beforehand about what we want to
Line 15: build. Otherwise, we would just jump to building without thinking about what we are
Line 16: building. And trying to ensure that what gets built is, in every single detail, the right thing
Line 17: through a written specification is quickly going to turn into writing the software itself, just
Line 18: in plain English.
Line 19: The problem is that the more hurried, stressed, and overwhelmed developers are, the less
Line 20: they test. Tests are the first thing that get skipped when things go wrong, and by doing so
Line 21: things suddenly get even worse, as tests are what avoid errors and failures, and more errors
Line 22: and failures mean more stress and rushing through the code to fix them, making the whole
Line 23: process a loop that gets worse and worse.
Line 24: Test-Driven Development (TDD) tries to solve this problem by engendering a set of
Line 25: practices where tests become a fundamental step of your daily routine. To write more code
Line 26: you must write tests, and as you get used to TDD and it becomes natural, you will quickly
Line 27: notice that it gets hard to even think about how to get started if not by writing a test.
Line 28: That's why in this chapter, we will cover how TDD can fit into the software development
Line 29: routine and how to leverage it to keep problems under control at times of high stress.
Line 30: 
Line 31: --- 페이지 78 ---
Line 32: Test-Driven Development while Creating a TODO List
Line 33: Chapter 3
Line 34: [ 68 ]
Line 35: In this chapter, we will cover the following topics:
Line 36: Starting projects with TDD
Line 37: Building applications the TDD way
Line 38: Preventing regressions
Line 39: Technical requirements
Line 40: A working Python interpreter should be all that is needed to work through the exercises in
Line 41: this chapter.
Line 42: The examples have been written using Python 3.7, but should work on most modern
Line 43: Python versions.
Line 44: You can find the code files used in this chapter on GitHub at https:/​/​github.​com/
Line 45: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter03
Line 46: Starting projects with TDD
Line 47: We already know that tests are meant to verify that our software adheres to the desired
Line 48: behavior. To do so means that our tests must express what that desired behavior is. They
Line 49: must explicitly state, "If I do this, I expect that to happen."
Line 50: For the innermost components, what happens is probably an implementation detail: "If I
Line 51: commit my unit of work, data is written to the database." But the more we move to the outer
Line 52: parts of our architecture, those that connect our software to the outside world, the more
Line 53: these tests become expressions of business needs. The more we move from solitary units, to
Line 54: sociable units, to integration and acceptance tests, the more the "desired behavior" becomes
Line 55: the one that has a business value.
Line 56: If we work with a test-driven approach, our first step before writing implementation code
Line 57: is obviously to write a test that helps us understand what we want to build (if we are just
Line 58: starting with our whole project, what we want to build is the software itself). This means
Line 59: that our very first test is the one that is going to make clear what's valuable. Why are we
Line 60: even writing the software in the first place?
Line 61: So let's see how a test-driven approach can benefit us during the software design phase
Line 62: itself. Suppose we want to start a TODO list kind of product.
Line 63: 
Line 64: --- 페이지 79 ---
Line 65: Test-Driven Development while Creating a TODO List
Line 66: Chapter 3
Line 67: [ 69 ]
Line 68: So let's start writing an acceptance test that will help us express explicitly what we want
Line 69: our app to do.
Line 70: Let's create a new todo directory where we are going to put the todo/src subdirectory
Line 71: with our source code, and the todo/tests directory with our tests:
Line 72: $ tree
Line 73: .
Line 74: ├── src
Line 75: └── tests
Line 76: At this point, we can start by making a todo/tests/__init__.py file and a
Line 77: todo/tests/test_acceptance.py module for our overall application acceptance test.
Line 78: The test_acceptance.py file is going to contain our test itself:
Line 79: import unittests
Line 80: class TestTODOAcceptance(unittest.TestCase):
Line 81:     def test_main(self):
Line 82:         raise NotImplementedError()
Line 83: We want our interactive shell application to accept commands and print outputs. So the
Line 84: first thing we want the app to do is to write the output and receive commands from an
Line 85: input:
Line 86: class TestTODOAcceptance(unittest.TestCase):
Line 87:     def test_main(self):
Line 88:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 89: We don't yet know what our fake_input and fake_output will be, but we will figure
Line 90: that out as we reduce uncertainty about how the app should behave.
Line 91: Then we said we want it to be an interactive shell, so it should be sitting there accepting
Line 92: commands until we tell it to quit. To make that happen we probably want to have the main
Line 93: loop for our Read-Eval-Print Loop (REPL) and we want the app to be running in the
Line 94: background during our test so we can send commands to it and fetch the responses:
Line 95: import unittest
Line 96: import threading
Line 97: class TestTODOAcceptance(unittest.TestCase):
Line 98:     def test_main(self):
Line 99:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 100: 
Line 101: --- 페이지 80 ---
Line 102: Test-Driven Development while Creating a TODO List
Line 103: Chapter 3
Line 104: [ 70 ]
Line 105:         app_thread = threading.Thread(target=app.run, daemon=True)
Line 106:         app_thread.start()
Line 107: But we don't want our app to be stuck there forever until the user kills it abruptly due to
Line 108: the frustration of being unable to exit it, and we surely don't want our test to be stuck there
Line 109: forever either. So we want our app to support a quit command and ensure it exits when it
Line 110: receives it:
Line 111: import unittest
Line 112: import threading
Line 113: class TestTODOAcceptance(unittest.TestCase):
Line 114:     def test_main(self):
Line 115:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 116:         app_thread = threading.Thread(target=app.run, daemon=True)
Line 117:         app_thread.start()
Line 118:         # ...
Line 119:         self.send_input("quit")
Line 120:         app_thread.join(timeout=1)
Line 121:         self.assertEqual(self.get_output(), "bye!\n")
Line 122: Great, now we know we want our app to sit there, accept commands, and exit on a quit
Line 123: request. But how are we going to tell the user that we are accepting commands? We likely
Line 124: want a prompt, so let's verify that by presenting a welcome screen with the list of the
Line 125: TODO items (none at the beginning) and a "> " prompt:
Line 126: import unittest
Line 127: import threading
Line 128: class TestTODOAcceptance(unittest.TestCase):
Line 129:     def test_main(self):
Line 130:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 131:         app_thread = threading.Thread(target=app.run, daemon=True)
Line 132:         app_thread.start()
Line 133:         welcome = self.get_output()
Line 134:         self.assertEqual(welcome, (
Line 135:             "TODOs:\n"
Line 136:             "\n"
Line 137:             "\n"
Line 138:             "> "
Line 139: 
Line 140: --- 페이지 81 ---
Line 141: Test-Driven Development while Creating a TODO List
Line 142: Chapter 3
Line 143: [ 71 ]
Line 144:         ))
Line 145:         self.send_input("quit")
Line 146:         app_thread.join(timeout=1)
Line 147:         self.assertEqual(self.get_output(), "bye!\n")
Line 148: Very well, we've already provided answers to tons of questions about how our app should
Line 149: behave. We decided it's driven by commands and those commands can be provided
Line 150: through a prompt on the same screen that displays the list of our items.
Line 151: What primary commands do we want to provide? Surely we at least want to be able to add
Line 152: new items and delete them? So let's test that we can execute those commands:
Line 153: import unittest
Line 154: import threading
Line 155: class TestTODOAcceptance(unittest.TestCase):
Line 156:     def test_main(self):
Line 157:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 158:         app_thread = threading.Thread(target=app.run, daemon=True)
Line 159:         app_thread.start()
Line 160:         welcome = self.get_output()
Line 161:         self.assertEqual(welcome, (
Line 162:             "TODOs:\n"
Line 163:             "\n"
Line 164:             "\n"
Line 165:             "> "
Line 166:         ))
Line 167:         self.send_input("add buy milk")
Line 168:         welcome = self.get_output()
Line 169:         self.assertEqual(welcome, (
Line 170:             "TODOs:\n"
Line 171:             "1. buy milk\n"
Line 172:             "\n"
Line 173:             "> "
Line 174:         ))
Line 175:         self.send_input("add buy eggs")
Line 176:         welcome = self.get_output()
Line 177:         self.assertEqual(welcome, (
Line 178:             "TODOs:\n"
Line 179:             "1. buy milk\n"
Line 180:             "2. buy eggs\n"
Line 181:             "\n"
Line 182: 
Line 183: --- 페이지 82 ---
Line 184: Test-Driven Development while Creating a TODO List
Line 185: Chapter 3
Line 186: [ 72 ]
Line 187:             "> "
Line 188:         ))
Line 189:         self.send_input("del 1")
Line 190:         welcome = self.get_output()
Line 191:         self.assertEqual(welcome, (
Line 192:             "TODOs:\n"
Line 193:             "1. buy eggs\n"
Line 194:             "\n"
Line 195:             "> "
Line 196:         ))
Line 197:         self.send_input("quit")
Line 198:         app_thread.join(timeout=1)
Line 199:         self.assertEqual(self.get_output(), "bye!\n")
Line 200: OK, we added a block where we add a note to "buy milk", one with a note to "buy eggs",
Line 201: and a third where we delete the "buy milk" entry. Our acceptance test is now fairly
Line 202: complete! It adds multiple todos and it removes them. We've defined everything we want
Line 203: our app to do and we can now move forward to finally trying to satisfy our needs!
Line 204: The test itself is going to do the next step; we simply have to run it:
Line 205: $ python -m unittest discover
Line 206: E
Line 207: ======================================================================
Line 208: ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 209: ----------------------------------------------------------------------
Line 210: Traceback (most recent call last):
Line 211:   File "/testingbook/03_specifications/01_todo/tests/test_acceptance.py",
Line 212: line 20, in test_main
Line 213:     app = TODOApp(io=(self.fake_input, self.fake_output))
Line 214: NameError: name 'TODOApp' is not defined
Line 215: ----------------------------------------------------------------------
Line 216: Ran 1 test in 0.000s
Line 217: FAILED (errors=1)
Line 218: Right, we now need to make the app itself as it doesn't even exist yet as a concept.
Line 219: For the sake of focusing this section on the business value of our application and thus on
Line 220: the user-facing tests, we are going to diverge a bit from the correct approach and we are
Line 221: going to have a single test for the whole app.
Line 222: 
Line 223: --- 페이지 83 ---
Line 224: Test-Driven Development while Creating a TODO List
Line 225: Chapter 3
Line 226: [ 73 ]
Line 227: So don't be surprised if we jump here from an acceptance test directly to the
Line 228: implementation of the app itself. It's only for the sake of reducing the cognitive load of the
Line 229: reader. In the real world, we would be writing unit tests to drive the design of our code, as
Line 230: designing the app and designing its implementation are two very different things. But here
Line 231: we wanted to make clear how writing tests forces us to think about the app itself, and thus
Line 232: we are going to make the code design happen behind the scenes.
Line 233: In the Building applications the TDD way section, we are going to see how to mix what we
Line 234: learned here about acceptance tests with the more classical TDD approach regarding the
Line 235: design of the code itself.
Line 236: So let's create a new todo Python package inside our src directory. We are going to have a
Line 237: src/todo/__init__.py file and a src/todo/app.py module for the application
Line 238: implementation itself:
Line 239: $ tree
Line 240: .
Line 241: ├── src
Line 242: │   ├── todo
Line 243: │   │   ├── app.py
Line 244: │   │   ├── __init__.py
Line 245: └── tests
Line 246:     ├── __init__.py
Line 247:     └── test_acceptance.py
Line 248: Our TODOApp can reside in src/todo/app.py for now, just as an empty class:
Line 249: class TODOApp:
Line 250:     pass
Line 251: Is this enough to be able to use our app from the tests? Not yet, because the todo package is
Line 252: not available for our tests. So before moving forward, we want to add a src/setup.py file
Line 253: to make a distribution for our todo package. Our minimal setup.py file is just going to tell
Line 254: the Python installer that "The application is named todo and it contains a todo package that has to
Line 255: be installed":
Line 256: from setuptools import setup
Line 257: setup(name='todo', packages=['todo'])
Line 258: 
Line 259: --- 페이지 84 ---
Line 260: Test-Driven Development while Creating a TODO List
Line 261: Chapter 3
Line 262: [ 74 ]
Line 263: Then the final layout of our project directory should look pretty much like this:
Line 264: $ tree
Line 265: .
Line 266: ├── src
Line 267: │   ├── setup.py
Line 268: │   ├── todo
Line 269: │   │   ├── app.py
Line 270: │   │   ├── __init__.py
Line 271: └── tests
Line 272:     ├── __init__.py
Line 273:     └── test_acceptance.py
Line 274: At this point, we can install our application in development mode with pip install -e:
Line 275: $ pip install -e src/
Line 276: Obtaining file://testingbook/03_specifications/01_todo/src
Line 277: Installing collected packages: todo
Line 278:   Running setup.py develop for todo
Line 279: Successfully installed todo
Line 280: This allows us to edit our tests/test_acceptance.py file to import the application class
Line 281: itself and solve the previous NameError error:
Line 282: import unittest
Line 283: from todo.app import TODOApp
Line 284: class TestTODOAcceptance(unittest.TestCase):
Line 285:     def test_main(self):
Line 286:         ...
Line 287: We already know that our TODOApp does nothing, so it surely won't make our test pass, but
Line 288: let's see what our test suggests for the next required step that involves rerunning our test
Line 289: suite:
Line 290: $ python -m unittest discover
Line 291: ======================================================================
Line 292: ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 293: ...
Line 294:     app = TODOApp(io=(self.fake_input, self.fake_output))
Line 295: AttributeError: 'TestTODOAcceptance' object has no attribute 'fake_input'
Line 296: Given that we've now installed the todo package, the app imports fine, but the test has no
Line 297: fake_input and fake_output to provide. So those are going to be our next areas of
Line 298: attention.
Line 299: 
Line 300: --- 페이지 85 ---
Line 301: Test-Driven Development while Creating a TODO List
Line 302: Chapter 3
Line 303: [ 75 ]
Line 304: As we want to ship input and outputs back and forth between the test and the app, wait for
Line 305: the outputs to be available, and use something that works across threads, a well-fitting
Line 306: solution might be to use a queue. During the application execution, our output function
Line 307: will probably be the print function and our input will be the Python input function, so
Line 308: let's set up something that allows us to simulate those.
Line 309: In our test case setup, we are going to create the Input/Output (I/O) queues and create a
Line 310: self.fake_input object that simulates the behavior of input and a self.fake_output
Line 311: object that simulates the behavior of print. Also for convenience, we are going to add the
Line 312: self.get_output and self.send_input methods so that our test can send and receive
Line 313: text from the app:
Line 314: import unittest
Line 315: import threading
Line 316: import queue
Line 317: from todo.app import TODOApp
Line 318: class TestTODOAcceptance(unittest.TestCase):
Line 319:     def setUp(self):
Line 320:         self.inputs = queue.Queue()
Line 321:         self.outputs = queue.Queue()
Line 322:         self.fake_output = lambda txt: self.outputs.put(txt)
Line 323:         self.fake_input = lambda: self.inputs.get()
Line 324:         self.get_output = lambda: self.outputs.get(timeout=1)
Line 325:         self.send_input = lambda cmd: self.inputs.put(cmd)
Line 326:     def test_main(self):
Line 327:         app = TODOApp(io=(self.fake_input, self.fake_output))
Line 328:         ...
Line 329: OK, we should have in place our I/O infrastructure for the tests. Will our test move
Line 330: forward? Let's see:
Line 331: $ python -m unittest discover
Line 332: ======================================================================
Line 333: ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 334: ...
Line 335:     app = TODOApp(io=(self.fake_input, self.fake_output))
Line 336: TypeError: TODOApp() takes no arguments
Line 337: OK, not as much as hoped. It did move forward, but we crashed on the same exact line of
Line 338: code because our TODOApp doesn't yet have any concept of I/O.
Line 339: 
Line 340: --- 페이지 86 ---
Line 341: Test-Driven Development while Creating a TODO List
Line 342: Chapter 3
Line 343: [ 76 ]
Line 344: So let's make our TODOApp aware of its input and output. By default, we are going to
Line 345: provide the built-in Python input and print commands (without the trailing newline),
Line 346: but our test will replace those with its own fake_input and fake_output:
Line 347: import functools
Line 348: class TODOApp:
Line 349:     def __init__(self, io=(input, functools.partial(print, end=""))):
Line 350:         self._in, self._out = io
Line 351: OK, we now have a TODOApp._in callable we can use to ask for inputs, and a
Line 352: TODOApp._out callable we can use to write outputs. What's the next step?
Line 353: $ python -m unittest discover
Line 354: ======================================================================
Line 355: ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 356: ...
Line 357:     app_thread = threading.Thread(target=app.run)
Line 358: AttributeError: 'TODOApp' object has no attribute 'run'
Line 359: Right, the REPL! Our app needs to leverage those I/O functions to actually show the output
Line 360: and ask for inputs. So we are going to add a TODOApp.run function that runs our REPL,
Line 361: providing the prompt and accepting commands until we quit:
Line 362: import functools
Line 363: class TODOApp:
Line 364:     def __init__(self, io=(input, functools.partial(print, end=""))):
Line 365:         self._in, self._out = io
Line 366:         self._quit = False
Line 367:     def run(self):
Line 368:         self._quit = False
Line 369:         while not self._quit:
Line 370:             self._out(self.prompt(""))
Line 371:             command = self._in()
Line 372:         self._out("bye!\n")
Line 373:     def prompt(self, output):
Line 374:         return """TODOs:
Line 375: {}
Line 376: > """.format(output)
Line 377: For now, our interactive shell doesn't do much – it shows the prompt and does nothing
Line 378: with the commands we send.
Line 379: 
Line 380: --- 페이지 87 ---
Line 381: Test-Driven Development while Creating a TODO List
Line 382: Chapter 3
Line 383: [ 77 ]
Line 384: If we run our acceptance test again, we are going to clearly see that our app did receive the
Line 385: add command to add the buy milk entry, but it didn't execute it and so the entry isn't
Line 386: there:
Line 387: $ python -m unittest discover
Line 388: ======================================================================
Line 389: ...
Line 390: AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
Line 391:   TODOs:
Line 392: -
Line 393: + 1. buy milk
Line 394: Our next step is adding the command dispatching and execution functionality so that the
Line 395: REPL not only receives those commands, but also executes them:
Line 396: import functools
Line 397: class TODOApp:
Line 398:     def __init__(self, io=(input, functools.partial(print, end=""))):
Line 399:         self._in, self._out = io
Line 400:         self._quit = False
Line 401:     def run(self):
Line 402:         self._quit = False
Line 403:         while not self._quit:
Line 404:             self._out(self.prompt(""))
Line 405:             command = self._in()
Line 406:             self._dispatch(command)
Line 407:         self._out("bye!\n")
Line 408:     def prompt(self, output):
Line 409:         return """TODOs:
Line 410: {}
Line 411: > """.format(output)
Line 412:     def _dispatch(self, cmd):
Line 413:         cmd, *args = cmd.split(" ", 1)
Line 414:         executor = getattr(self, "cmd_{}".format(cmd), None)
Line 415:         if executor is None:
Line 416:             self._out("Invalid command: {}\n".format(cmd))
Line 417:             return
Line 418:         executor(*args)
Line 419: 
Line 420: --- 페이지 88 ---
Line 421: Test-Driven Development while Creating a TODO List
Line 422: Chapter 3
Line 423: [ 78 ]
Line 424: The TODOApp.run method is in charge of calling TODOApp._dispatch to serve commands,
Line 425: and each command will be served by running a TODOApp.cmd_COMMANDNAME method that
Line 426: we will implement for each command.
Line 427: If we rerun our test, we are going to get complaints about invalid commands being sent to
Line 428: the application:
Line 429: $ python -m unittest discover
Line 430: ======================================================================
Line 431: FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 432: ...
Line 433: AssertionError: 'Invalid command: add\n' != 'TODOs:\n1. buy milk\n\n> '
Line 434: - Invalid command: add
Line 435: + TODOs:
Line 436: + 1. buy milk
Line 437: +
Line 438: + >
Line 439: This is pretty much expected because we have not yet implemented any commands.
Line 440: So let's provide our add command, which is simply going to get the entry to add and insert
Line 441: the todo item into the list of our TODO entries:
Line 442: class TODOApp:
Line 443:     def __init__(self, io=(input, functools.partial(print, end=""))):
Line 444:         self._in, self._out = io
Line 445:         self._quit = False
Line 446:         self._entries = []
Line 447:     ...
Line 448:     def cmd_add(self, what):
Line 449:         self._entries.append(what)
Line 450: 
Line 451: --- 페이지 89 ---
Line 452: Test-Driven Development while Creating a TODO List
Line 453: Chapter 3
Line 454: [ 79 ]
Line 455: Rerunning our acceptance test will confirm that the Invalid command message went
Line 456: away, and thus we can now handle the command, but we still don't print back the list of
Line 457: todo items. So even if the todo entry was added to our todo list, it's not displayed back to
Line 458: us:
Line 459: $ python -m unittest discover
Line 460: ======================================================================
Line 461: FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 462: ...
Line 463: AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
Line 464:   TODOs:
Line 465: -
Line 466: + 1. buy milk
Line 467:   >
Line 468: Instead of showing an empty prompt, like the current self.prompt("") call is doing, we
Line 469: want to actually show the list of our TODO items. So we are going to add an items_list
Line 470: method to our TODOApp that returns the content we want to display in the prompt through
Line 471: self.prompt(self.items_list()) during the REPL loop within TODOApp.run:
Line 472: class TODOApp:
Line 473:     def __init__(self, io=(input, functools.partial(print, end=""))):
Line 474:         self._in, self._out = io
Line 475:         self._quit = False
Line 476:         self._entries = []
Line 477:     def run(self):
Line 478:         self._quit = False
Line 479:         while not self._quit:
Line 480:             self._out(self.prompt(self.items_list()))
Line 481:             command = self._in()
Line 482:             self._dispatch(command)
Line 483:         self._out("bye!\n")
Line 484:     def items_list(self):
Line 485:         enumerated_items = enumerate(self._entries, start=1)
Line 486:         return "\n".join(
Line 487:             "{}. {}".format(idx, entry) for idx, entry in enumerated_items
Line 488:         )
Line 489:     ...
Line 490: Our application will now be able to finally serve its first complete cycle, receiving the add
Line 491: command and showing us the list of items with the newly added entry.
Line 492: 
Line 493: --- 페이지 90 ---
Line 494: Test-Driven Development while Creating a TODO List
Line 495: Chapter 3
Line 496: [ 80 ]
Line 497: If we rerun our test, we no longer get stuck on the same issue of having an empty list of
Line 498: todo items, but we are going to get complaints about the fact that the del command is not
Line 499: yet implemented:
Line 500: $ python -m unittest discover
Line 501: ======================================================================
Line 502: FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
Line 503: ...
Line 504: AssertionError: 'Invalid command: del\n' != 'TODOs:\n1. buy eggs\n\n> '
Line 505: - Invalid command: del
Line 506: + TODOs:
Line 507: + 1. buy eggs
Line 508: +
Line 509: + >
Line 510: So let's implement the remaining two commands, del and quit, and check whether our
Line 511: app is complete:
Line 512: class TODOApp:
Line 513:     ...
Line 514:     def cmd_quit(self, *_):
Line 515:         self._quit = True
Line 516:     def cmd_add(self, what):
Line 517:         self._entries.append(what)
Line 518:     def cmd_del(self, idx):
Line 519:         idx = int(idx) - 1
Line 520:         if idx < 0 or idx >= len(self._entries):
Line 521:             self._out("Invalid index\n")
Line 522:             return
Line 523:         self._entries.pop(idx)
Line 524:     ...
Line 525: The cmd_del function just checks whether a valid index to be removed was provided, and
Line 526: then removes it from the list of todo entries. The cmd_quit command just sets a flag that
Line 527: will make our REPL exit when it finds it on the next loop cycle.
Line 528: Now that the functionality to add todo items, remove them, and quit the app has been
Line 529: implemented, our test will finally succeed and confirm our application matches our
Line 530: requirements:
Line 531: $ python -m unittest discover
Line 532: .
Line 533: ----------------------------------------------------------------------
Line 534: 
Line 535: --- 페이지 91 ---
Line 536: Test-Driven Development while Creating a TODO List
Line 537: Chapter 3
Line 538: [ 81 ]
Line 539: Ran 1 test in 0.001s
Line 540: OK
Line 541: So far, we made an entire application without launching it even once. We had the whole
Line 542: implementation driven by our acceptance test. Will the app really work and do what we
Line 543: wanted? Did acceptance tests really help us design the application behavior?
Line 544: To check whether the experience is the one we expected, let's make our application
Line 545: runnable. This can be done by adding a __main__.py file to our todo package within
Line 546: src/todo. The updated result of our project layout should thus be as follows:
Line 547: $ tree
Line 548: .
Line 549: ├── src
Line 550: │   ├── setup.py
Line 551: │   └── todo
Line 552: │       ├── app.py
Line 553: │       ├── __init__.py
Line 554: │       └── __main__.py
Line 555: └── tests
Line 556:     ├── __init__.py
Line 557:     └── test_acceptance.py
Line 558: 3 directories, 6 files
Line 559: And the content of src/todo/__main__.py will be very simple — it will just create our
Line 560: TODOApp and will enter the main loop:
Line 561: from .app import TODOApp
Line 562: TODOApp().run()
Line 563: Our app can now be started with the python -m todo command. Let's see whether the
Line 564: behavior is actually what we imagined and our test-driven design approach really leads to
Line 565: the app we expected:
Line 566: $ python -m todo
Line 567: TODOs:
Line 568: > add buy some milk
Line 569: TODOs:
Line 570: 1. buy some milk
Line 571: > add buy water
Line 572: TODOs:
Line 573: 1. buy some milk
Line 574: 
Line 575: --- 페이지 92 ---
Line 576: Test-Driven Development while Creating a TODO List
Line 577: Chapter 3
Line 578: [ 82 ]
Line 579: 2. buy water
Line 580: > add send happy birthday message
Line 581: TODOs:
Line 582: 1. buy some milk
Line 583: 2. buy water
Line 584: 3. send happy birthday message
Line 585: > del 1
Line 586: TODOs:
Line 587: 1. buy water
Line 588: 2. send happy birthday message
Line 589: > del 1
Line 590: TODOs:
Line 591: 1. send happy birthday message
Line 592: > quit
Line 593: bye!
Line 594: Definitely, the app behaves as we expected! We were welcomed by a prompt with an
Line 595: empty list of todo items and as we added and removed them, our prompt updated with the
Line 596: new state of our todo list. The app delivered exactly the experience we described in our test
Line 597: and supports all the features we wanted, working flawlessly on the first run.
Line 598: This approach of driving the whole software design and development process from
Line 599: business-oriented acceptance tests usually comes under the umbrella of Acceptance Test-
Line 600: Driven Development (ATDD).
Line 601: We saw how tests not only verify the correctness of the software but at the outer layers, can
Line 602: also explain what the primary software behaviors are and what the software's business
Line 603: value is.
Line 604: This means that tests can tell a story – if I read them, I'm going to know exactly how the
Line 605: software behaves in that context. If the software has a good enough test coverage and I read
Line 606: all the tests, then I'm going to know how the software works as a whole. Thus tests can be
Line 607: used to express the software specification itself in a reliable and testable manner, which is a
Line 608: concept frequently referred to as Specification by Example.
Line 609: We are going to get into more details about this concept in Chapter 7, Fitness Function with
Line 610: a Contact Book Application, but for now, let's focus on how to attach this concept of designing
Line 611: the software through tests to the concept of designing its implementation through tests.
Line 612: 
Line 613: --- 페이지 93 ---
Line 614: Test-Driven Development while Creating a TODO List
Line 615: Chapter 3
Line 616: [ 83 ]
Line 617: Building applications the TDD way
Line 618: In the previous section, we saw how to use tests to design our application itself, exposing
Line 619: clear goals and forcing us to think about how the application should behave.
Line 620: Once we start thinking a bit about what a test is actually doing, it slowly becomes clear why
Line 621: that works well: the tests are going to interact with the system under test. The way they are
Line 622: going to interact with the system they have to test is usually through the interface that the
Line 623: system exposes.
Line 624: This means that the capabilities we are going to expose to any black-box test are the same
Line 625: capabilities that we are going to expose to any other user of the system under test.
Line 626: If the system under test is the whole application, as in the case of the previous section, then
Line 627: it means that to write the test we will be forced to reason about the capabilities and the
Line 628: interface we are going to expose to our users themselves. In practice, having to write a test
Line 629: for that layer forces us to make clear the UI and UX of our application.
Line 630: If the system under test is instead a component of the whole application, the user of that
Line 631: component will be another software component; another piece of code calling the first one.
Line 632: This means that to write the test, we will be forced to define the API that our component
Line 633: has to expose, and thus design the implementation of the component itself.
Line 634: Thus embracing TDD helps us design code with well-thought-out APIs that the rest of the
Line 635: system can depend on, but writing tests beforehand is not the sum of all TDD practices.
Line 636: There are two primary rules that are part of the TDD practice: the first is obviously to write
Line 637: failing tests before you write the code, but the second is that once your tests pass, you
Line 638: should refactor to remove duplication.
Line 639: This means that it not only forces us to think of the public interfaces that our objects and
Line 640: subsystems are going to expose beforehand, but it also forces us to keep our internals in
Line 641: shape through continuous refactoring.
Line 642: The TODO list application we made does everything we wanted, but it lacks a fairly major
Line 643: feature before it can become a valuable application we can use for real: it doesn't persist our
Line 644: todo items. If we close the application and restart it, we are going to lose all our items.
Line 645: We definitely want our TODO app to save and reload our todo items, so we are going to
Line 646: work on a new feature to enable that behavior.
Line 647: 
Line 648: --- 페이지 94 ---
Line 649: Test-Driven Development while Creating a TODO List
Line 650: Chapter 3
Line 651: [ 84 ]
Line 652: As usual, we are going to start with a very high-level acceptance test that shows what we
Line 653: want the experience for the user to be. Our new test_persistence test is going to start a
Line 654: new todo app with an empty database, save an item, quit the app, and restart it again on
Line 655: the same database to check that the items are still there:
Line 656: ...
Line 657: import tempfile
Line 658: class TestTODOAcceptance(unittest.TestCase):
Line 659:     ...
Line 660:     def test_persistence(self):
Line 661:         with tempfile.TemporaryDirectory() as tmpdirname:
Line 662:             app_thread = threading.Thread(
Line 663:                 target=TODOApp(
Line 664:                     io=(self.fake_input, self.fake_output),
Line 665:                     dbpath=tmpdirname
Line 666:                 ).run,
Line 667:                 daemon=True
Line 668:             )
Line 669:             app_thread.start()
Line 670:             welcome = self.get_output()
Line 671:             self.assertEqual(welcome, (
Line 672:                 "TODOs:\n"
Line 673:                 "\n"
Line 674:                 "\n"
Line 675:                 "> "
Line 676:             ))
Line 677:             self.send_input("add buy milk")
Line 678:             self.send_input("quit")
Line 679:             app_thread.join(timeout=1)
Line 680:             while True:
Line 681:                 try:
Line 682:                     self.get_output()
Line 683:                 except queue.Empty:
Line 684:                     break
Line 685:             app_thread = threading.Thread(
Line 686:                 target=TODOApp(
Line 687:                     io=(self.fake_input, self.fake_output),
Line 688:                     dbpath=tmpdirname
Line 689:                 ).run,
Line 690:                 daemon=True
Line 691:             )
Line 692: 
Line 693: --- 페이지 95 ---
Line 694: Test-Driven Development while Creating a TODO List
Line 695: Chapter 3
Line 696: [ 85 ]
Line 697:             app_thread.start()
Line 698:             welcome = self.get_output()
Line 699:             self.assertEqual(welcome, (
Line 700:                 "TODOs:\n"
Line 701:                 "1. buy milk\n"
Line 702:                 "\n"
Line 703:                 "> "
Line 704:             ))
Line 705:             self.send_input("quit")
Line 706:             app_thread.join(timeout=1)
Line 707: First of all, our test makes a new temporary directory called tmpdirname, where we are
Line 708: going to save our database for the app under test. Then, as in the previous acceptance test,
Line 709: it starts the application in the background, pointing it to our fake I/O and the temporary
Line 710: path for the database. Once the app starts, we verify that, on first execution, it starts with an
Line 711: empty TODO list. Then we add one item to the app and we quit. At this point, we can
Line 712: restart the application again using the same exact database path, and check that the item we
Line 713: added is still there after the app restarts. Then we can just quit the app, as it did what we
Line 714: wanted to test.
Line 715: Obviously, if we start our test suite, we already know that our new acceptance test is not
Line 716: going to pass. We haven't implemented the persistence of our todo items at all and our app
Line 717: doesn't even accept a dbpath argument:
Line 718: $ python -m unittest discover -v
Line 719: test_main (tests.test_acceptance.TestTODOAcceptance) ... ok
Line 720: test_persistence (tests.test_acceptance.TestTODOAcceptance) ... ERROR
Line 721: ======================================================================
Line 722: ERROR: test_persistence (tests.test_acceptance.TestTODOAcceptance)
Line 723: ----------------------------------------------------------------------
Line 724: Traceback (most recent call last):
Line 725:   File "/testingbook/03_tdd/02_codedesign/tests/test_acceptance.py", line
Line 726: 72, in test_persistence
Line 727:     dbpath=tmpdirname
Line 728: TypeError: __init__() got an unexpected keyword argument 'dbpath'
Line 729: ----------------------------------------------------------------------
Line 730: Ran 2 tests in 0.004s
Line 731: FAILED (errors=1)
Line 732: Our next step is to move one layer below and start working on our implementation.
Line 733: 
Line 734: --- 페이지 96 ---
Line 735: Test-Driven Development while Creating a TODO List
Line 736: Chapter 3
Line 737: [ 86 ]
Line 738: Thus the tests that we are going to write will get further away from the end user point of
Line 739: view that we used in the acceptance tests, and move toward describing what we want our
Line 740: inner implementation to be.
Line 741: For this reason, we are going to create a separate directory for these tests so that they don't
Line 742: get confused with the higher-level tests that tell the story from the user's point of view. So
Line 743: inside our tests directory, we are going to create a subdirectory for unit tests.
Line 744: Then, inside that directory, we are going to add a test_todoapp.py file to start reasoning
Line 745: about how we want to change our TODOApp object to support persistence:
Line 746: └── tests
Line 747:     ├── __init__.py
Line 748:     ├── test_acceptance.py
Line 749:     └── unit
Line 750:         ├── __init__.py
Line 751:         └── test_todoapp.py
Line 752: Our test_todoapp.py file is going to start with a very simple test, one to verify that we
Line 753: can accept a database path for our TODO app and that if omitted, it should use the current
Line 754: directory:
Line 755: import unittest
Line 756: import tempfile
Line 757: from pathlib import Path
Line 758: from todo.app import TODOApp
Line 759: class TestTODOApp(unittest.TestCase):
Line 760:     def test_default_dbpath(self):
Line 761:         app = TODOApp()
Line 762:         assert Path(".").resolve() == Path(app._dbpath).resolve()
Line 763:     def test_accepts_dbpath(self):
Line 764:         expected_path = Path(tempfile.gettempdir(), "something")
Line 765:         app = TODOApp(dbpath=str(expected_path))
Line 766:         assert expected_path == Path(app._dbpath)
Line 767: Now we can forget for a little about our acceptance tests and focus on our unit tests. We are
Line 768: going to run them in isolation with the -k unit option to confirm that they fail as we
Line 769: expect, and we can move on to adding support for the dbpath to our object:
Line 770: $ python -m unittest discover -k unit
Line 771: EE
Line 772: ======================================================================
Line 773: 
Line 774: --- 페이지 97 ---
Line 775: Test-Driven Development while Creating a TODO List
Line 776: Chapter 3
Line 777: [ 87 ]
Line 778: ERROR: test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp)
Line 779: ----------------------------------------------------------------------
Line 780: Traceback (most recent call last):
Line 781:   File "/testingbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line
Line 782: 12, in test_accepts_dbpath
Line 783:     app = TODOApp(dbpath=str(expected_path))
Line 784: TypeError: __init__() got an unexpected keyword argument 'dbpath'
Line 785: ======================================================================
Line 786: ERROR: test_default_dbpath (tests.unit.test_todoapp.TestTODOApp)
Line 787: ----------------------------------------------------------------------
Line 788: Traceback (most recent call last):
Line 789:   File "/testingbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line
Line 790: 9, in test_default_dbpath
Line 791:     assert Path(".").resolve() == Path(app._dbpath).resolve()
Line 792: AttributeError: 'TODOApp' object has no attribute '_dbpath'
Line 793: ----------------------------------------------------------------------
Line 794: Ran 2 tests in 0.001s
Line 795: FAILED (errors=2)
Line 796: The -k option for unit tests only runs the tests that contain the provided substring, so it's
Line 797: going to identify only our tests inside the unit directory. It would obviously also run any
Line 798: tests that had unit in the name, but it's generally a convenient way to select some tests to
Line 799: run without having to remember in which exact directory they exist.
Line 800: Now the implementation is fairly easy, we just want to make TODOApp able to remember
Line 801: where it has to save the database and have it always available as TODOApp._dbpath. So we
Line 802: are going to modify our TODOApp.__init__ to accept the extra argument and put it aside:
Line 803: ...
Line 804: class TODOApp:
Line 805:     def __init__(self,
Line 806:                  io=(input, functools.partial(print, end="")),
Line 807:                  dbpath=None):
Line 808:         self._in, self._out = io
Line 809:         self._quit = False
Line 810:         self._entries = []
Line 811:         self._dbpath = dbpath or "."
Line 812:     ...
Line 813: 
Line 814: --- 페이지 98 ---
Line 815: Test-Driven Development while Creating a TODO List
Line 816: Chapter 3
Line 817: [ 88 ]
Line 818: If we did this correctly, the tests for our implementation should now pass without issue:
Line 819: $ python -m unittest discover -k unit -v
Line 820: test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 821: test_default_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 822: ----------------------------------------------------------------------
Line 823: Ran 2 tests in 0.002s
Line 824: OK
Line 825: And we can now look back to our acceptance test to find guidance about what to do next:
Line 826: $ python -m unittest discover
Line 827: .F..
Line 828: ======================================================================
Line 829: FAIL: test_persistence (tests.test_acceptance.TestTODOAcceptance)
Line 830: ----------------------------------------------------------------------
Line 831: Traceback (most recent call last):
Line 832:   File "/tddbook/03_tdd/02_codedesign/tests/test_acceptance.py", line 108,
Line 833: in test_persistence
Line 834:     "TODOs:\n"
Line 835: AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
Line 836:   TODOs:
Line 837: -
Line 838: + 1. buy milk
Line 839:   >
Line 840: ----------------------------------------------------------------------
Line 841: Ran 4 tests in 1.006s
Line 842: FAILED (failures=1)
Line 843: So, now our TODO application is able to start and accept the temporary database path. But
Line 844: it's not doing what we need. It's not saving anything into the database, so once restarted,
Line 845: the TODO list is still empty.
Line 846: At this point, we need to go back to our unit tests and come up with a set of tests to drive
Line 847: the implementation of our persistence layer so that the data can be saved and loaded back.
Line 848: Our first test should probably assess that TODOApp is able to load some save data. When we
Line 849: start thinking of our TestTODOApp.test_load test, it's easy to imagine the Act phase: it
Line 850: probably just wants to call a TODOApp.load method to load the data. The Assert phase too
Line 851: is also pretty obvious: TODOApp._entries should probably contain the same exact entries
Line 852: that we loaded.
Line 853: 
Line 854: --- 페이지 99 ---
Line 855: Test-Driven Development while Creating a TODO List
Line 856: Chapter 3
Line 857: [ 89 ]
Line 858: But what about the Arrange phase? What are we going to store in the database so that we
Line 859: can load it back? Which database system are we going to use? And after a while we will
Line 860: probably move to the "should we even care at all?" question.
Line 861: Does TODOApp have to care about how data is saved into the database?
Line 862: Probably not... We should probably delegate that whole problem to another entity, and
Line 863: only make sure that TODOApp properly invokes that entity and does the right thing with the
Line 864: data provided by that entity:
Line 865: ...
Line 866: from unittest.mock import Mock
Line 867: class TestTODOApp(unittest.TestCase):
Line 868:     ...
Line 869:     def test_load(self):
Line 870:         dbpath = Path(tempfile.gettempdir(), "something")
Line 871:         dbmanager = Mock(
Line 872:             load=Mock(return_value=["buy milk", "buy water"])
Line 873:         )
Line 874:         app = TODOApp(io=(Mock(return_value="quit"), Mock()),
Line 875:                       dbpath=dbpath, dbmanager=dbmanager)
Line 876:         app.run()
Line 877:         dbmanager.load.assert_called_with(dbpath)
Line 878:         assert app._entries == ["buy milk", "buy water"]
Line 879: Our new TestTODOApp.test_load now tests this, provided dbmanager is in charge of
Line 880: loading/saving data. Our TODOApp is going to use it when it starts, and by virtue of calling
Line 881: dbmanager, it ends up with the todo entries that dbmanager loaded.
Line 882: The test prepares a dbpath object for the sole purpose of checking that dbmanager is asked
Line 883: to load that specific path, then it makes a dbmanager that returns a canned response of two
Line 884: items when dbmanager.load(dbpath) is invoked. Once those two are in place, it
Line 885: prepares a TODOApp that has a dummy output and a stubbed input that make the app quit
Line 886: immediately.
Line 887: Then, once the app is started through app.run(), we expect it to have called dbmanager
Line 888: and have loaded the two provided entries.
Line 889: 
Line 890: --- 페이지 100 ---
Line 891: Test-Driven Development while Creating a TODO List
Line 892: Chapter 3
Line 893: [ 90 ]
Line 894: Now that we have a clearer understanding of what we want to do, we can go back to our
Line 895: TODOApp and write an implementation that satisfies our test. We are going to extend
Line 896: TODOApp to support dbmanager and we are going to modify TODOApp.run to load the
Line 897: existing data when the app is started:
Line 898: class TODOApp:
Line 899:     def __init__(self,
Line 900:                  io=(input, functools.partial(print, end="")),
Line 901:                  dbpath=None, dbmanager=None):
Line 902:         self._in, self._out = io
Line 903:         self._quit = False
Line 904:         self._entries = []
Line 905:         self._dbpath = dbpath or "."
Line 906:         self._dbmanager = dbmanager
Line 907:     def run(self):
Line 908:         if self._dbmanager is not None:
Line 909:             self._entries = self._dbmanager.load(self._dbpath)
Line 910:         self._quit = False
Line 911:         while not self._quit:
Line 912:             self._out(self.prompt(self.items_list()))
Line 913:             command = self._in()
Line 914:             self._dispatch(command)
Line 915:         self._out("bye!\n")
Line 916: Is this enough to make our test pass? Let's find out:
Line 917: $ python -m unittest discover -k unit -v
Line 918: test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 919: test_default_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 920: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 921: ----------------------------------------------------------------------
Line 922: Ran 3 tests in 0.002s
Line 923: OK
Line 924: It seems so, which means we achieved what we wanted. But there is something odd in our
Line 925: implementation. If TODOApp doesn't care about how data is loaded, why does it care where
Line 926: it is loaded from? The fact that you even need a path from which to load your data seems a
Line 927: concern of the loader. Maybe we can load data without a path? Maybe we can load things
Line 928: from remote resources that need a host and port instead of a path? That's something that
Line 929: only the loader can know.
Line 930: 
Line 931: --- 페이지 101 ---
Line 932: Test-Driven Development while Creating a TODO List
Line 933: Chapter 3
Line 934: [ 91 ]
Line 935: So let's leverage our refactoring phase, as we made the tests pass, and change everything to
Line 936: just receive dbmanager. Whether that dbmanager needs a path, and whether that path is to
Line 937: a file, a directory, or a remote resource, is not something our app should care about.
Line 938: First, we want to update the tests; instead of passing dbpath, we directly provide
Line 939: dbmanager itself. dbmanager will know the path. Let's also make a test for the case when
Line 940: no dbmanager is provided so that the app doesn't crash, but just disables persistency:
Line 941: import unittest
Line 942: from unittest.mock import Mock
Line 943: from todo.app import TODOApp
Line 944: class TestTODOApp(unittest.TestCase):
Line 945:     def test_noloader(self):
Line 946:         app = TODOApp(io=(Mock(return_value="quit"), Mock()),
Line 947:                       dbmanager=None)
Line 948:         app.run()
Line 949:         assert app._entries == []
Line 950:     def test_load(self):
Line 951:         dbmanager = Mock(
Line 952:             load=Mock(return_value=["buy milk", "buy water"])
Line 953:         )
Line 954:         app = TODOApp(io=(Mock(return_value="quit"), Mock()),
Line 955:                       dbmanager=dbmanager)
Line 956:         app.run()
Line 957:         dbmanager.load.assert_called_with()
Line 958:         assert app._entries == ["buy milk", "buy water"]
Line 959: The first test_noloader test verifies that if there is no dbmanager, the app is still able to
Line 960: start, while test_load verifies that when dbmanager is used, the data that it provides is
Line 961: properly loaded by TODOApp.
Line 962: We can now also throw away our test_accepts_dbpath and test_default_dbpath, as
Line 963: our TODOApp is no longer in charge of opening the database itself.
Line 964: Do our newly refactored tests pass? Nope, not anymore:
Line 965: $ python -m unittest discover -k unit -v
Line 966: test_load (tests.unit.test_todoapp.TestTODOApp) ... FAIL
Line 967: 
Line 968: --- 페이지 102 ---
Line 969: Test-Driven Development while Creating a TODO List
Line 970: Chapter 3
Line 971: [ 92 ]
Line 972: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 973: ======================================================================
Line 974: FAIL: test_load (tests.unit.test_todoapp.TestTODOApp)
Line 975: ----------------------------------------------------------------------
Line 976: Traceback (most recent call last):
Line 977:   File "/tddbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line 29,
Line 978: in test_load
Line 979:     dbmanager.load.assert_called_with()
Line 980:   File "/usr/lib/python3.7/unittest/mock.py", line 873, in
Line 981: assert_called_with
Line 982:     raise AssertionError(_error_message()) from cause
Line 983: AssertionError: Expected call: load()
Line 984: Actual call: load('.')
Line 985: ----------------------------------------------------------------------
Line 986: Ran 2 tests in 0.002s
Line 987: FAILED (failures=1)
Line 988: Our mock expectation was violated. We expected load to be called with no argument, as
Line 989: dbmanager should already know where to load from, but instead, we received ".", which
Line 990: is the default dbpath.
Line 991: Let's head back to our TODOApp and remove any reference to dbpath, thus removing the
Line 992: dbpath argument and the self._dbpath attribute:
Line 993: class TODOApp:
Line 994:     def __init__(self,
Line 995:                  io=(input, functools.partial(print, end="")),
Line 996:                  dbmanager=None):
Line 997:         self._in, self._out = io
Line 998:         self._quit = False
Line 999:         self._entries = []
Line 1000:         self._dbmanager = dbmanager
Line 1001:     def run(self):
Line 1002:         if self._dbmanager is not None:
Line 1003:             self._entries = self._dbmanager.load()
Line 1004:         self._quit = False
Line 1005:         while not self._quit:
Line 1006:             self._out(self.prompt(self.items_list()))
Line 1007:             command = self._in()
Line 1008:             self._dispatch(command)
Line 1009:         self._out("bye!\n")
Line 1010: 
Line 1011: --- 페이지 103 ---
Line 1012: Test-Driven Development while Creating a TODO List
Line 1013: Chapter 3
Line 1014: [ 93 ]
Line 1015: Do our tests now pass? Yes! They do:
Line 1016: $ python -m unittest discover -k unit -v
Line 1017: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1018: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1019: ----------------------------------------------------------------------
Line 1020: Ran 2 tests in 0.001s
Line 1021: OK
Line 1022: Now that we are happy with our implementation, we can go back to look for things to do.
Line 1023: When looking for things to do, guidance comes from our acceptance tests. If we run them
Line 1024: right now they will probably crash because, in the end, we settled for an interface that is
Line 1025: slightly different from the one we originally thought of:
Line 1026: $ python -m unittest discover
Line 1027: .E..
Line 1028: ======================================================================
Line 1029: ERROR: test_persistence (tests.test_acceptance.TestTODOAcceptance)
Line 1030: ----------------------------------------------------------------------
Line 1031: Traceback (most recent call last):
Line 1032:   File
Line 1033: "/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/02_codedesign/tes
Line 1034: ts/test_acceptance.py", line 74, in test_persistence
Line 1035:     dbpath=tmpdirname,
Line 1036: TypeError: __init__() got an unexpected keyword argument 'dbpath'
Line 1037: ----------------------------------------------------------------------
Line 1038: Ran 4 tests in 0.005s
Line 1039: FAILED (errors=1)
Line 1040: We don't receive dbpath anymore, but we want dbmanager. So let's update our test
Line 1041: accordingly.
Line 1042: For now, we don't want to be too refined about our storage; we are just going to store
Line 1043: things in a very simple storage system. Let's call this BasicDB and provide it to the app in
Line 1044: our acceptance tests. They will load and save data from it:
Line 1045: ...
Line 1046: import pathlib
Line 1047: ...
Line 1048: from todo.db import BasicDB
Line 1049: 
Line 1050: --- 페이지 104 ---
Line 1051: Test-Driven Development while Creating a TODO List
Line 1052: Chapter 3
Line 1053: [ 94 ]
Line 1054: class TestTODOAcceptance(unittest.TestCase):
Line 1055:     ...
Line 1056:     def test_persistence(self):
Line 1057:         with tempfile.TemporaryDirectory() as tmpdirname:
Line 1058:             app_thread = threading.Thread(
Line 1059:                 target=TODOApp(
Line 1060:                     io=(self.fake_input, self.fake_output),
Line 1061:                     dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
Line 1062:                 ).run,
Line 1063:                 daemon=True
Line 1064:             )
Line 1065:             app_thread.start()
Line 1066:             ...
Line 1067: Running our acceptance test now will tell us that the idea might look great, but we still
Line 1068: have to implement BasicDB. So let's create a tests/unit/test_basicdb.py file and
Line 1069: start reasoning how BasicDB should behave.
Line 1070: Our TestBasicDB tests are probably going to be for loading and saving data; for now, let's
Line 1071: start with the loading one as that's what we are concerned about:
Line 1072: import pathlib
Line 1073: import unittest
Line 1074: from unittest import mock
Line 1075: from todo.db import BasicDB
Line 1076: class TestBasicDB(unittest.TestCase):
Line 1077:     def test_load(self):
Line 1078:         mock_file = mock.MagicMock(
Line 1079:             read=mock.Mock(return_value='["first", "second"]')
Line 1080:         )
Line 1081:         mock_file.__enter__.return_value = mock_file
Line 1082:         mock_opener = mock.Mock(return_value=mock_file)
Line 1083:         db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
Line 1084:         loaded = db.load()
Line 1085:         self.assertEqual(loaded, ["first", "second"])
Line 1086:         self.assertEqual(
Line 1087:             mock_opener.call_args[0][0],
Line 1088:             pathlib.Path("testdb")
Line 1089:         )
Line 1090:         mock_file.read.assert_called_with()
Line 1091: 
Line 1092: --- 페이지 105 ---
Line 1093: Test-Driven Development while Creating a TODO List
Line 1094: Chapter 3
Line 1095: [ 95 ]
Line 1096: We want our BasicDB to read/write data from a file, so we are going to use a mock_file
Line 1097: object that fakes the Python behavior of a file object. When trying to read from it, it's
Line 1098: going to return the content of our BasicDB with two sample entries.
Line 1099: mock_file is going to be what our mock_opener is going to return whenever BasicDB
Line 1100: asks to open a new file. In practice, what we are trying to do is to make sure that with
Line 1101: mock_opener(ANY_PATH) as f: will return our mock_file, so that from the point of
Line 1102: view of BasicDB, there is no difference between using our mock_opener or the Python
Line 1103: open function.
Line 1104: Once our stubbed file opener is available, we are going to create an instance of BasicDB,
Line 1105: providing the stub opener as a replacement for the Python open function. The path we are
Line 1106: going to provide to BasicDB for the storage of its database doesn't really matter at this
Line 1107: point as it will always return mock_file, but we will still be checking that the opener was
Line 1108: called with the expected path.
Line 1109: The real core of our test is the call to db.load(), where we are going to ask BasicDB to
Line 1110: load the data from mock_file. Then we can confirm that the data we expected was loaded
Line 1111: and that it was loaded the way we would expect, by actually opening the file and reading
Line 1112: its content.
Line 1113: In practice, we decided that BasicDB(path).load() will be the way we plan to load the
Line 1114: data in BasicDB.
Line 1115: Now that we've set our expectations clearly and have a better idea of what we want to
Line 1116: build, we can try to work on an implementation that could satisfy the interface we
Line 1117: imagined.
Line 1118: The first step is creating our src/todo/db.py module, as that's where we imagined we
Line 1119: would be importing BasicDB from while writing our test (see the from todo.db import
Line 1120: BasicDB line at the top of our test file).
Line 1121: Then we are going to make a BasicDB class that accepts the file path to save/load data
Line 1122: to/from, and an optional opener so that we can replace the default one with other
Line 1123: alternative implementations. For the goal of making clear that the opener is mostly meant
Line 1124: for testing, we are going to flag it as an internal detail, prefixing its name with an
Line 1125: underscore:
Line 1126: class BasicDB:
Line 1127:     def __init__(self, path, _fileopener=open):
Line 1128:         self._path = path
Line 1129:         self._fileopener = _fileopener
Line 1130: 
Line 1131: --- 페이지 106 ---
Line 1132: Test-Driven Development while Creating a TODO List
Line 1133: Chapter 3
Line 1134: [ 96 ]
Line 1135: Will this make our tests pass? I doubt it will – it still does nothing, so let's cycle back to our
Line 1136: tests to see which parts of the BasicDB interface we have to implement:
Line 1137: $ python -m unittest discover -k unit -v
Line 1138: test_load (tests.unit.test_basicdb.TestBasicDB) ... ERROR
Line 1139: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1140: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1141: ======================================================================
Line 1142: ERROR: test_load (tests.unit.test_basicdb.TestBasicDB)
Line 1143: ----------------------------------------------------------------------
Line 1144: Traceback (most recent call last):
Line 1145:   File "/tddbook/03_tdd/02_codedesign/tests/unit/test_basicdb.py", line 18,
Line 1146: in test_load
Line 1147:     loaded = db.load()
Line 1148: AttributeError: 'BasicDB' object has no attribute 'load'
Line 1149: ----------------------------------------------------------------------
Line 1150: Ran 3 tests in 0.002s
Line 1151: FAILED (errors=1)
Line 1152: OK, it seems we now want to move to the implementation of BasicDB.load.
Line 1153: The implementation feels pretty straightforward: we open a file that should contain a list of
Line 1154: strings. Let's just read the file content and parse the list definition:
Line 1155: class BasicDB:
Line 1156:     def __init__(self, path, _fileopener=open):
Line 1157:         self._path = path
Line 1158:         self._fileopener = _fileopener
Line 1159:     def load(self):
Line 1160:         with self._fileopener(self._path, "r", encoding="utf-8") as f:
Line 1161:             txt = f.read()
Line 1162:         return eval(txt)
Line 1163: 
Line 1164: --- 페이지 107 ---
Line 1165: Test-Driven Development while Creating a TODO List
Line 1166: Chapter 3
Line 1167: [ 97 ]
Line 1168: Does this make our tests happy? Are we really able to load the items stored in BasicDB?
Line 1169: Let's find out:
Line 1170: $ python -m unittest discover -k unit -v
Line 1171: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1172: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1173: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1174: ----------------------------------------------------------------------
Line 1175: Ran 3 tests in 0.002s
Line 1176: OK
Line 1177: It seems so – our BasicDB test was able to load the content and fetch back the two items.
Line 1178: For anyone wondering about the usage of eval, please bear with the
Line 1179: example for a little while. We are going to replace it pretty soon and make
Line 1180: clear that using it is never a good idea. But it was a convenient way to
Line 1181: simulate the bug we are going to fix in the dedicated Preventing regressions
Line 1182: section.
Line 1183: All our unit tests now pass, so we are a bit at a loss about where we were and what we
Line 1184: wanted to do next. Whenever we are unsure about our next step, the acceptance tests
Line 1185: should guide us on how far we are from the feature we want to provide for our users. So
Line 1186: let's go back to our acceptance test and see what we still have to do:
Line 1187: $ python -m unittest discover -k acceptance
Line 1188: ...
Line 1189: FileNotFoundError: [Errno 2] No such file or directory:
Line 1190: '/tmp/tmpcug9zvsw/db'
Line 1191: Uh, we forgot that when we start the application the first time, our BasicDB is empty;
Line 1192: actually, it doesn't exist at all. So there is nothing we can load. Thus we have to go back to
Line 1193: our unit tests and write one to ensure that when the opened file doesn't exist, we do
Line 1194: actually return an empty list of todo items.
Line 1195: Back to our tests/unit/test_basicdb.py file, we are going to add a new
Line 1196: test_missing_load test:
Line 1197: ...
Line 1198: class TestBasicDB(unittest.TestCase):
Line 1199:     ...
Line 1200:     def test_missing_load(self):
Line 1201:         mock_opener = mock.Mock(side_effect=FileNotFoundError)
Line 1202: 
Line 1203: --- 페이지 108 ---
Line 1204: Test-Driven Development while Creating a TODO List
Line 1205: Chapter 3
Line 1206: [ 98 ]
Line 1207:         db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
Line 1208:         loaded = db.load()
Line 1209:         self.assertEqual(loaded, [])
Line 1210:         self.assertEqual(
Line 1211:             mock_opener.call_args[0][0],
Line 1212:             pathlib.Path("testdb")
Line 1213:         )
Line 1214: This new test is just going to throw FileNotFoundError every time BasicDB tries to read
Line 1215: the data. This simulates the case where we would try to open a nonexistent database.
Line 1216: As expected, our test is going to fail with FileNotFoundError as we haven't handled it
Line 1217: yet:
Line 1218: $ python -m unittest discover -k unit -v
Line 1219: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1220: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ERROR
Line 1221: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1222: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1223: ======================================================================
Line 1224: ERROR: test_missing_load (tests.unit.test_basicdb.TestBasicDB)
Line 1225: ----------------------------------------------------------------------
Line 1226: Traceback (most recent call last):
Line 1227:   File "/tddbook/03_tdd/02_codedesign/tests/unit/test_basicdb.py", line 31,
Line 1228: in test_missing_load
Line 1229:     loaded = db.load()
Line 1230:   File "/tddbook/03_tdd/02_codedesign/src/todo/db.py", line 9, in load
Line 1231:     with self._fileopener(self._path, "r", encoding="utf-8") as f:
Line 1232:   File "/usr/lib/python3.7/unittest/mock.py", line 1011, in __call__
Line 1233:     return _mock_self._mock_call(*args, **kwargs)
Line 1234:   File "/usr/lib/python3.7/unittest/mock.py", line 1071, in _mock_call
Line 1235:     raise effect
Line 1236: FileNotFoundError
Line 1237: ----------------------------------------------------------------------
Line 1238: Ran 4 tests in 0.003s
Line 1239: FAILED (errors=1)
Line 1240: But we can easily modify our BasicDB.load method to handle such a case and return an
Line 1241: empty list of todo items:
Line 1242: class BasicDB:
Line 1243:     def __init__(self, path, _fileopener=open):
Line 1244:         self._path = path
Line 1245:         self._fileopener = _fileopener
Line 1246: 
Line 1247: --- 페이지 109 ---
Line 1248: Test-Driven Development while Creating a TODO List
Line 1249: Chapter 3
Line 1250: [ 99 ]
Line 1251:     def load(self):
Line 1252:         try:
Line 1253:             with self._fileopener(self._path, "r",
Line 1254:                                   encoding="utf-8") as f:
Line 1255:                 txt = f.read()
Line 1256:             return eval(txt)
Line 1257:         except FileNotFoundError:
Line 1258:             return []
Line 1259: At this point, if we got it right, our unit tests should all pass:
Line 1260: $ python -m unittest discover -k unit -v
Line 1261: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1262: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1263: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1264: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1265: ----------------------------------------------------------------------
Line 1266: Ran 4 tests in 0.002s
Line 1267: OK
Line 1268: Given that we were looking for our next step a few minutes ago, we should probably head
Line 1269: back to our acceptance tests and check where we were. Running our acceptance tests again
Line 1270: will show that this time, we were able to start the application correctly (that is, it doesn't
Line 1271: crash anymore on missing files), but that on adding a new item and restarting the app, it
Line 1272: didn't persist the addition:
Line 1273: $ python -m unittest discover -k acceptance
Line 1274: .F
Line 1275: ======================================================================
Line 1276: FAIL: test_persistence (tests.test_acceptance.TestTODOAcceptance)
Line 1277: ----------------------------------------------------------------------
Line 1278: Traceback (most recent call last):
Line 1279:   File "/tddbook/03_tdd/02_codedesign/tests/test_acceptance.py", line 110,
Line 1280: in test_persistence
Line 1281:     "TODOs:\n"
Line 1282: AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
Line 1283:   TODOs:
Line 1284: -
Line 1285: + 1. buy milk
Line 1286:   >
Line 1287: ----------------------------------------------------------------------
Line 1288: Ran 2 tests in 1.006s
Line 1289: FAILED (failures=1)
Line 1290: 
Line 1291: --- 페이지 110 ---
Line 1292: Test-Driven Development while Creating a TODO List
Line 1293: Chapter 3
Line 1294: [ 100 ]
Line 1295: The buy milk item is not where we expected it to be after reloading the application, which
Line 1296: makes sense, as we never actually implemented any support for saving the current todo
Line 1297: items when we exit the application. So while we are probably able to load back a list of
Line 1298: items, we never save one.
Line 1299: This means we want to extend our TODOApp to save the current list of todo items before
Line 1300: exiting.
Line 1301: So let's add a test_save test to our tests/unit/tests_todoapp.py tests to make clear
Line 1302: what we want to achieve.
Line 1303: We just want the application to start with some entries and make sure that when it quits,
Line 1304: the app asks dbmanager to save them. This means that if there was any change made to our
Line 1305: list of TODOs, it gets recorded:
Line 1306: class TestTODOApp(unittest.TestCase):
Line 1307:     ...
Line 1308:     def test_save(self):
Line 1309:         dbmanager = Mock(
Line 1310:             load=Mock(return_value=["buy milk", "buy water"]),
Line 1311:             save=Mock()
Line 1312:         )
Line 1313:         app = TODOApp(io=(Mock(return_value="quit"), Mock()),
Line 1314:                       dbmanager=dbmanager)
Line 1315:         app.run()
Line 1316:         dbmanager.save.assert_called_with(["buy milk", "buy water"])
Line 1317: This test will obviously fail because we haven't yet used the dbmanager from TODOApp to
Line 1318: save anything:
Line 1319: $ python -m unittest discover -k unit -v
Line 1320: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1321: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1322: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1323: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1324: test_save (tests.unit.test_todoapp.TestTODOApp) ... FAIL
Line 1325: ======================================================================
Line 1326: FAIL: test_save (tests.unit.test_todoapp.TestTODOApp)
Line 1327: ----------------------------------------------------------------------
Line 1328: Traceback (most recent call last):
Line 1329:   File "/tddbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line 39,
Line 1330: in test_save
Line 1331:     dbmanager.save.assert_called_with(["buy milk", "buy water"])
Line 1332: 
Line 1333: --- 페이지 111 ---
Line 1334: Test-Driven Development while Creating a TODO List
Line 1335: Chapter 3
Line 1336: [ 101 ]
Line 1337:   File "/usr/lib/python3.7/unittest/mock.py", line 864, in
Line 1338: assert_called_with
Line 1339:     raise AssertionError('Expected call: %s\nNot called' % (expected,))
Line 1340: AssertionError: Expected call: save(['buy milk', 'buy water'])
Line 1341: Not called
Line 1342: ----------------------------------------------------------------------
Line 1343: Ran 5 tests in 0.003s
Line 1344: FAILED (failures=1)
Line 1345: So, let's go to our TODOApp.run method and extend it to call dbmanager.save() before
Line 1346: exiting:
Line 1347: class TODOApp:
Line 1348:     ...
Line 1349:     def run(self):
Line 1350:         if self._dbmanager is not None:
Line 1351:             self._entries = self._dbmanager.load()
Line 1352:         self._quit = False
Line 1353:         while not self._quit:
Line 1354:             self._out(self.prompt(self.items_list()))
Line 1355:             command = self._in()
Line 1356:             self._dispatch(command)
Line 1357:         if self._dbmanager is not None:
Line 1358:             self._dbmanager.save(self._entries)
Line 1359:         self._out("bye!\n")
Line 1360: That's all we need to make our test pass. Our TODOApp now takes care of saving the entries
Line 1361: and it's up to the provided dbmanager to do the right thing with them:
Line 1362: $ python -m unittest discover -k unit -v
Line 1363: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1364: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1365: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1366: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1367: test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1368: ----------------------------------------------------------------------
Line 1369: Ran 5 tests in 0.002s
Line 1370: OK
Line 1371: 
Line 1372: --- 페이지 112 ---
Line 1373: Test-Driven Development while Creating a TODO List
Line 1374: Chapter 3
Line 1375: [ 102 ]
Line 1376: Are we done? Not yet – TODOApp is now doing its job, but a quick run of our acceptance test
Line 1377: will point out that dbmanager doesn't know what we are talking about:
Line 1378: $ python -m unittest discover -k acceptance
Line 1379: .Exception in thread Thread-2:
Line 1380: Traceback (most recent call last):
Line 1381:   File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
Line 1382:     self.run()
Line 1383:   File "/usr/lib/python3.7/threading.py", line 870, in run
Line 1384:     self._target(*self._args, **self._kwargs)
Line 1385:   File "/tddbook/03_tdd/02_codedesign/src/todo/app.py", line 24, in run
Line 1386:     self._dbmanager.save(self._entries)
Line 1387: AttributeError: 'BasicDB' object has no attribute 'save'
Line 1388: Back to our tests/unit/test_basicdb.py file, we are going to add a test_save test to
Line 1389: confirm that BasicDB does actually want to save the list of provided items:
Line 1390: class TestBasicDB(unittest.TestCase):
Line 1391:     ...
Line 1392:     def test_save(self):
Line 1393:         mock_file = mock.MagicMock(write=mock.Mock())
Line 1394:         mock_file.__enter__.return_value = mock_file
Line 1395:         mock_opener = mock.Mock(return_value=mock_file)
Line 1396:         db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
Line 1397:         loaded = db.save(["first", "second"])
Line 1398:         self.assertEqual(
Line 1399:             mock_opener.call_args[0][0:2],
Line 1400:             (pathlib.Path("testdb"), "w+")
Line 1401:         )
Line 1402:         mock_file.write.assert_called_with('["first", "second"]')
Line 1403: The test just verifies that when BasicDB.save is called, it opens the target file in write
Line 1404: mode and it tries to write into it the list of values.
Line 1405: To satisfy our test, we are going to implement a BasicDB.save method that converts the
Line 1406: list of entries to its string representation, replaces single quotes with double quotes so that
Line 1407: we save them in a format that is compatible with JSON, and saves it back:
Line 1408: class BasicDB:
Line 1409:     ...
Line 1410:     def save(self, values):
Line 1411:         with self._fileopener(self._path, "w+", encoding="utf-8") as f:
Line 1412:             f.write(repr(values).replace("'", '"'))
Line 1413: 
Line 1414: --- 페이지 113 ---
Line 1415: Test-Driven Development while Creating a TODO List
Line 1416: Chapter 3
Line 1417: [ 103 ]
Line 1418: If we did everything correctly, our unit tests should now be able to pass:
Line 1419: $ python -m unittest discover -k unit -v
Line 1420: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1421: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1422: test_save (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1423: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1424: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1425: test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1426: ----------------------------------------------------------------------
Line 1427: Ran 6 tests in 0.003s
Line 1428: OK
Line 1429: We implemented everything that we wanted and we provided the last piece that our
Line 1430: acceptance test was complaining about, which can be easily confirmed by going back to our
Line 1431: acceptance tests and verifying that the software is now completed:
Line 1432: $ python -m unittest discover -k acceptance
Line 1433: ..
Line 1434: ----------------------------------------------------------------------
Line 1435: Ran 2 tests in 1.006s
Line 1436: OK
Line 1437: Great! Our app is now fully functional.
Line 1438: We just want to tweak our src/todo/_main__.py file so that when we start the app from
Line 1439: the command line, we start it with dbmanager and thus with persistence enabled by
Line 1440: default:
Line 1441: from .app import TODOApp
Line 1442: from .db import BasicDB
Line 1443: TODOApp(dbmanager=BasicDB("todo.data")).run()
Line 1444: Starting the application, adding an entry, and then restarting it will now properly preserve
Line 1445: the entry across the two runs:
Line 1446: $ python -m todo
Line 1447: TODOs:
Line 1448: > add buy milk
Line 1449: TODOs:
Line 1450: 1. buy milk
Line 1451: 
Line 1452: --- 페이지 114 ---
Line 1453: Test-Driven Development while Creating a TODO List
Line 1454: Chapter 3
Line 1455: [ 104 ]
Line 1456: > quit
Line 1457: bye!
Line 1458: $ python -m todo
Line 1459: TODOs:
Line 1460: 1. buy milk
Line 1461: > quit
Line 1462: bye!
Line 1463: Before ending our day with a sense of satisfaction from our newly built application, we
Line 1464: want to make sure we remember to install the new release of our favorite Linux
Line 1465: distribution.
Line 1466: As we just made a great TODO application, let's add an entry to it:
Line 1467: $ python -m todo
Line 1468: TODOs:
Line 1469: 1. buy milk
Line 1470: > add install "Focal Fossa"
Line 1471: TODOs:
Line 1472: 1. buy milk
Line 1473: 2. install "Focal Fossa"
Line 1474: > quit
Line 1475: bye!
Line 1476: Sadly, the morning after, we open our TODO application to look at what we have to do,
Line 1477: and surprise, surprise, we are welcomed by a major crash in our application:
Line 1478: $ python -m todo
Line 1479: Traceback (most recent call last):
Line 1480:   File "/usr/lib/python3.7/runpy.py", line 193, in _run_module_as_main
Line 1481:     "__main__", mod_spec)
Line 1482:   File "/usr/lib/python3.7/runpy.py", line 85, in _run_code
Line 1483:     exec(code, run_globals)
Line 1484:   File "/tddbook/03_tdd/02_codedesign/src/todo/__main__.py", line 4, in
Line 1485: <module>
Line 1486:     TODOApp(dbmanager=BasicDB("todo.data")).run()
Line 1487:   File "/tddbook/03_tdd/02_codedesign/src/todo/app.py", line 15, in run
Line 1488:     self._entries = self._dbmanager.load()
Line 1489:   File "/tddbook/03_tdd/02_codedesign/src/todo/db.py", line 12, in load
Line 1490:     return eval(txt)
Line 1491:   File "<string>", line 1
Line 1492:     ["buy milk", "install "Focal Fossa""]
Line 1493:                                ^
Line 1494: SyntaxError: invalid syntax
Line 1495: 
Line 1496: --- 페이지 115 ---
Line 1497: Test-Driven Development while Creating a TODO List
Line 1498: Chapter 3
Line 1499: [ 105 ]
Line 1500: Our data is unable to load due to an issue in the BasicDB persistence layer, and we will
Line 1501: have to fix our bug if we ever want to be able to use our TODO application. This is actually
Line 1502: great because TDD has a best practice that allows us to tackle these bugs. Let's introduce
Line 1503: regression tests.
Line 1504: Preventing regressions
Line 1505: Tests are not only used to drive our application design and our code design, but also drive
Line 1506: our research and the debugging of the issues that our application faces.
Line 1507: Whenever we face any kind of error, bug, or crash, our fixing process should start with
Line 1508: writing a regression test – a test whose purpose is to reproduce the same exact issue we are
Line 1509: facing.
Line 1510: Having a regression test in place will prevent that bug from happening again in the future,
Line 1511: even if someone refactors some of the code or replaces the implementation. That's not all a
Line 1512: test can do – once we've written a test that reproduces our issue, we will be able to more
Line 1513: easily debug the issue and see what's going on in a fully controlled and isolated
Line 1514: environment such as a test suite.
Line 1515: As our application crashed trying to load our database, we are going to write a test for it
Line 1516: and see what the problem is.
Line 1517: The first step is writing a test that reproduces the same exact steps that the user did to
Line 1518: trigger the condition, so we are going to write a test in tests/test_regressions.py that
Line 1519: is going to reproduce our most recent user sessions in the application.
Line 1520: Our first goal is to be able to reproduce the issue. To do so, we are going to use the setup
Line 1521: that is most similar to that in the real world. So we are going to reuse the setup code from
Line 1522: our acceptance tests and create a TestRegressions class:
Line 1523: import unittest
Line 1524: import threading
Line 1525: import queue
Line 1526: import tempfile
Line 1527: import pathlib
Line 1528: from todo.app import TODOApp
Line 1529: from todo.db import BasicDB
Line 1530: class TestRegressions(unittest.TestCase):
Line 1531:     def setUp(self):
Line 1532: 
Line 1533: --- 페이지 116 ---
Line 1534: Test-Driven Development while Creating a TODO List
Line 1535: Chapter 3
Line 1536: [ 106 ]
Line 1537:         self.inputs = queue.Queue()
Line 1538:         self.outputs = queue.Queue()
Line 1539:         self.fake_output = lambda txt: self.outputs.put(txt)
Line 1540:         self.fake_input = lambda: self.inputs.get()
Line 1541:         self.get_output = lambda: self.outputs.get(timeout=1)
Line 1542:         self.send_input = lambda cmd: self.inputs.put(cmd)
Line 1543: This is the same exact setUp code we had in our acceptance tests for fake I/O. We could
Line 1544: inherit from the same base class or use a mixin to provide the setup of our fake I/O, but
Line 1545: here we just copied those same few lines of code.
Line 1546: Then we are going to add a test_os_release method that reproduces exactly what
Line 1547: happened in our real usage session:
Line 1548:    def test_os_release(self):
Line 1549:         with tempfile.TemporaryDirectory() as tmpdirname:
Line 1550:             app_thread = threading.Thread(
Line 1551:                 target=TODOApp(
Line 1552:                     io=(self.fake_input, self.fake_output),
Line 1553:                     dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
Line 1554:                 ).run,
Line 1555:                 daemon=True
Line 1556:             )
Line 1557:             app_thread.start()
Line 1558:             self.get_output()
Line 1559:             self.send_input("add buy milk")
Line 1560:             self.send_input('add "Focal Fossa"')
Line 1561:             self.send_input("quit")
Line 1562:             app_thread.join(timeout=1)
Line 1563:             while True:
Line 1564:                 try:
Line 1565:                     self.get_output()
Line 1566:                 except queue.Empty:
Line 1567:                     break
Line 1568:             app_thread = threading.Thread(
Line 1569:                 target=TODOApp(
Line 1570:                     io=(self.fake_input, self.fake_output),
Line 1571:                     dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
Line 1572:                 ).run,
Line 1573:                 daemon=True
Line 1574:             )
Line 1575:             app_thread.start()
Line 1576:             self.get_output()
Line 1577: 
Line 1578: --- 페이지 117 ---
Line 1579: Test-Driven Development while Creating a TODO List
Line 1580: Chapter 3
Line 1581: [ 107 ]
Line 1582: First, we start the application, then we add a note to buy milk, install the Focal Fossa
Line 1583: release, and then we quit. Subsequently, we just restart the application.
Line 1584: If we run our test, it should reproduce the same exact steps that happened in our software
Line 1585: and thus trigger the same exact crash:
Line 1586: $ python -m unittest discover -k regression
Line 1587: Exception in thread Thread-2:
Line 1588: Traceback (most recent call last):
Line 1589:   File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
Line 1590:     self.run()
Line 1591:   File "/usr/lib/python3.8/threading.py", line 870, in run
Line 1592:     self._target(*self._args, **self._kwargs)
Line 1593:   File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
Line 1594:     self._entries = self._dbmanager.load()
Line 1595:   File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
Line 1596:     return eval(txt)
Line 1597:   File "<string>", line 1
Line 1598:     ["buy milk", "install "Focal Fossa""]
Line 1599:                            ^
Line 1600: SyntaxError: invalid syntax
Line 1601: OK, the crash is there and it's the same exact traceback. So we were able to reproduce the
Line 1602: issue! Our next step is to isolate the issue to find what really causes it and which part of our
Line 1603: system is involved in the problem itself.
Line 1604: To do so, we are going to move from a test that really runs the application to a simpler one
Line 1605: that does not involve the whole machinery and I/O support. Let's see whether we can
Line 1606: reproduce the issue by replacing our fairly long and complete TestRegressions class
Line 1607: with one that just starts the application with a stubbed set of inputs and then restarts it:
Line 1608: import unittest
Line 1609: from unittest import mock
Line 1610: import tempfile
Line 1611: import pathlib
Line 1612: from todo.app import TODOApp
Line 1613: from todo.db import BasicDB
Line 1614: class TestRegressions(unittest.TestCase):
Line 1615:     def test_os_release(self):
Line 1616:         with tempfile.TemporaryDirectory() as tmpdirname:
Line 1617:             app = TODOApp(
Line 1618:                 io=(mock.Mock(side_effect=[
Line 1619:                     "add buy milk",
Line 1620:                     'add install "Focal Fossa"',
Line 1621: 
Line 1622: --- 페이지 118 ---
Line 1623: Test-Driven Development while Creating a TODO List
Line 1624: Chapter 3
Line 1625: [ 108 ]
Line 1626:                     "quit"
Line 1627:                 ]), mock.Mock()),
Line 1628:                 dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
Line 1629:             )
Line 1630:             app.run()
Line 1631:             restarted_app = TODOApp(
Line 1632:                 io=(mock.Mock(side_effect="quit"), mock.Mock()),
Line 1633:                 dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
Line 1634:             )
Line 1635:             restarted_app.run()
Line 1636: If we rerun our regression tests, we are luckily going to see that it still fails as before:
Line 1637: $ python -m unittest discover -k regression
Line 1638: E
Line 1639: ======================================================================
Line 1640: ERROR: test_os_release (tests.test_regressions.TestRegressions)
Line 1641: ----------------------------------------------------------------------
Line 1642: Traceback (most recent call last):
Line 1643:   File "/tddbook/03_tdd/03_regression/tests/test_regressions.py", line 27,
Line 1644: in test_os_release
Line 1645:     restarted_app.run()
Line 1646:   File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
Line 1647:     self._entries = self._dbmanager.load()
Line 1648:   File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
Line 1649:     return eval(txt)
Line 1650:   File "<string>", line 1
Line 1651:     ["buy milk", "install "Focal Fossa""]
Line 1652:                            ^
Line 1653: SyntaxError: invalid syntax
Line 1654: ----------------------------------------------------------------------
Line 1655: Ran 1 test in 0.003s
Line 1656: FAILED (errors=1)
Line 1657: This helped us confirm that the I/O doesn't really matter and that running the application
Line 1658: for real is not involved in causing our bug. We greatly reduced the scope of the involved
Line 1659: entities to just TODOApp and BasicDB objects.
Line 1660: There is still the filesystem involved; does that matter? Is it a problem with the fact that we
Line 1661: are reading and writing files?
Line 1662: 
Line 1663: --- 페이지 119 ---
Line 1664: Test-Driven Development while Creating a TODO List
Line 1665: Chapter 3
Line 1666: [ 109 ]
Line 1667: To check that, let's move forward further and get rid of the filesystem too. We can use an
Line 1668: opener that provides an in-memory file instead of a real one so that where we write doesn't
Line 1669: matter anymore:
Line 1670: import unittest
Line 1671: from unittest import mock
Line 1672: import io
Line 1673: from todo.app import TODOApp
Line 1674: from todo.db import BasicDB
Line 1675: class TestRegressions(unittest.TestCase):
Line 1676:     def test_os_release(self):
Line 1677:         fakefile = io.StringIO()
Line 1678:         fakefile.close = mock.Mock()
Line 1679:         app = TODOApp(
Line 1680:             io=(mock.Mock(side_effect=[
Line 1681:                 "add buy milk",
Line 1682:                 'add install "Focal Fossa"',
Line 1683:                 "quit"
Line 1684:             ]), mock.Mock()),
Line 1685:             dbmanager=BasicDB(None, _fileopener=mock.Mock(
Line 1686:                 side_effect=[FileNotFoundError, fakefile]
Line 1687:             ))
Line 1688:         )
Line 1689:         app.run()
Line 1690:         # rollback the file. So that the application, restarting,
Line 1691:         # can read the new data that we wrote.
Line 1692:         fakefile.seek(0)
Line 1693:         restarted_app = TODOApp(
Line 1694:             io=(mock.Mock(return_value="quit"), mock.Mock()),
Line 1695:             dbmanager=BasicDB(None, _fileopener=mock.Mock(
Line 1696:                 return_value=fakefile
Line 1697:             ))
Line 1698:         )
Line 1699:         restarted_app.run()
Line 1700: Our test now creates an io.StringIO instance instead of using a real file, so it doesn't
Line 1701: depend anymore on a real disk. We replaced the standard io.StringIO.close() method
Line 1702: with a dummy one, so that the file never gets closed and we can read it again. Otherwise,
Line 1703: after it's used for the first time it will be lost forever.
Line 1704: 
Line 1705: --- 페이지 120 ---
Line 1706: Test-Driven Development while Creating a TODO List
Line 1707: Chapter 3
Line 1708: [ 110 ]
Line 1709: Then we started the application with a _fileopener that firstly triggers
Line 1710: FileNotFoundError, causing the application to start with an empty todo list, and
Line 1711: secondly returns the fake file so that the data gets saved to the fake file. The same fake file,
Line 1712: from which the application once restarted, will read the todo items.
Line 1713: Rerunning our regression test will confirm that we are still able to reproduce the same exact
Line 1714: issue, and thus our test is still valid:
Line 1715: $ python -m unittest discover -k regression
Line 1716: E
Line 1717: ======================================================================
Line 1718: ERROR: test_os_release (tests.test_regressions.TestRegressions)
Line 1719: ----------------------------------------------------------------------
Line 1720: Traceback (most recent call last):
Line 1721:   File "/tddbook/03_tdd/03_regression/tests/test_regressions.py", line 36,
Line 1722: in test_os_release
Line 1723:     restarted_app.run()
Line 1724:   File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
Line 1725:     self._entries = self._dbmanager.load()
Line 1726:   File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
Line 1727:     return eval(txt)
Line 1728:   File "<string>", line 1
Line 1729:     ["buy milk", "install "Focal Fossa""]
Line 1730:                            ^
Line 1731: SyntaxError: invalid syntax
Line 1732: ----------------------------------------------------------------------
Line 1733: Ran 1 test in 0.002s
Line 1734: FAILED (errors=1)
Line 1735: OK, we removed every interaction with the outer world. We know that our problem can be
Line 1736: reproduced solely with TODOApp and BasicDB. What else can we try to remove from the
Line 1737: equation to further reduce the area where our issue might live and identify the minimum
Line 1738: system components necessary to reproduce our issue?
Line 1739: Our issue crashes in BasicDB.load(), so there is a high chance that it's caused by loading
Line 1740: back the data that we saved. So let's get rid of TODOApp and try to directly save and load
Line 1741: back our list of two items.
Line 1742: Our final version of the test is fairly minimal and has isolated BasicDB on its own:
Line 1743: class TestRegressions(unittest.TestCase):
Line 1744:     def test_os_release(self):
Line 1745:         fakefile = io.StringIO()
Line 1746:         fakefile.close = mock.Mock()
Line 1747: 
Line 1748: --- 페이지 121 ---
Line 1749: Test-Driven Development while Creating a TODO List
Line 1750: Chapter 3
Line 1751: [ 111 ]
Line 1752:         data = ["buy milk", 'install "Focal Fossa"']
Line 1753:         dbmanager = BasicDB(None, _fileopener=mock.Mock(
Line 1754:             return_value=fakefile
Line 1755:         ))
Line 1756:         dbmanager.save(data)
Line 1757:         fakefile.seek(0)
Line 1758:         loaded_data = dbmanager.load()
Line 1759:         self.assertEqual(loaded_data, data)
Line 1760: Running our test does indeed fail with the same exact error that we had before:
Line 1761: $ python -m unittest discover -k regression
Line 1762: E
Line 1763: ======================================================================
Line 1764: ERROR: test_os_release (tests.test_regressions.TestRegressions)
Line 1765: ----------------------------------------------------------------------
Line 1766: Traceback (most recent call last):
Line 1767:   File
Line 1768: "/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/03_regression/tes
Line 1769: ts/test_regressions.py", line 22, in test_os_release
Line 1770:     loaded_data = dbmanager.load()
Line 1771:   File
Line 1772: "/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/03_regression/src
Line 1773: /todo/db.py", line 12, in load
Line 1774:     return eval(txt)
Line 1775:   File "<string>", line 1
Line 1776:     ["buy milk", "install "Focal Fossa""]
Line 1777:                            ^
Line 1778: SyntaxError: invalid syntax
Line 1779: ----------------------------------------------------------------------
Line 1780: Ran 1 test in 0.001s
Line 1781: FAILED (errors=1)
Line 1782: So we were able to get a test involving the minimum possible number of entities in isolation
Line 1783: to reproduce our issue. Only BasicDB is in use in our test, so we now know for sure that
Line 1784: that's where our issue lies.
Line 1785: Our issue is due to the fact that we tried to save and load data in JSON format, relying on
Line 1786: the fact that the Python syntax for arrays of strings is nearly the same as JSON. Thus using
Line 1787: repr and eval could work to generate the JSON and load it back.
Line 1788: Sadly, that was a pretty terrible idea that we put in place for the sole purpose of
Line 1789: reproducing this issue. Evaluating user inputs is generally a big security hole.
Line 1790: 
Line 1791: --- 페이지 122 ---
Line 1792: Test-Driven Development while Creating a TODO List
Line 1793: Chapter 3
Line 1794: [ 112 ]
Line 1795: If instead of install "Focal Fossa", we wrote "] + [print("hello")] + [" as our
Line 1796: todo item, that would have resulted in our TODOApp executing the Python print function
Line 1797: when loading back todo items (because what we saved was ["buy milk", ""] +
Line 1798: [print("hello")] + [""] ) and instead of print, we could have forced the app to do
Line 1799: anything when loading back the todo items.
Line 1800: eval should never be used with input that comes from users, so let's replace our BasicDB
Line 1801: implementation with one that uses the json module:
Line 1802: import json
Line 1803: class BasicDB:
Line 1804:     def __init__(self, path, _fileopener=open):
Line 1805:         self._path = path
Line 1806:         self._fileopener = _fileopener
Line 1807:     def load(self):
Line 1808:         try:
Line 1809:             with self._fileopener(self._path, "r",
Line 1810:                                   encoding="utf-8") as f:
Line 1811:                 return json.load(f)
Line 1812:         except FileNotFoundError:
Line 1813:             return []
Line 1814:     def save(self, values):
Line 1815:         with self._fileopener(self._path, "w+", encoding="utf-8") as f:
Line 1816:             f.write(json.dumps(values))
Line 1817: The only part we changed in BasicDB.load is that instead of using eval, we now use
Line 1818: json.load, and in BasicDB.save, instead of repr we use json.dumps.
Line 1819: This uses the JSON module to save and load our data, removing the risk of malicious code
Line 1820: execution.
Line 1821: If we did everything correctly, our test for the bug should finally pass, while our
Line 1822: application continues to pass all other existing tests as well:
Line 1823: $ python -m unittest discover -v
Line 1824: test_main (tests.test_acceptance.TestTODOAcceptance) ... ok
Line 1825: test_persistence (tests.test_acceptance.TestTODOAcceptance) ... ok
Line 1826: test_os_release (tests.test_regressions.TestRegressions) ... ok
Line 1827: test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1828: test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1829: test_save (tests.unit.test_basicdb.TestBasicDB) ... ok
Line 1830: test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1831: 
Line 1832: --- 페이지 123 ---
Line 1833: Test-Driven Development while Creating a TODO List
Line 1834: Chapter 3
Line 1835: [ 113 ]
Line 1836: test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1837: test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
Line 1838: ----------------------------------------------------------------------
Line 1839: Ran 9 tests in 1.015s
Line 1840: OK
Line 1841: It seems we succeeded! We identified the bug, fixed it, and now have a test preventing the
Line 1842: same bug from happening again.
Line 1843: I hope the benefit of starting any bug-and-issue resolution by first writing a test that
Line 1844: reproduces the issue itself is clear. Not only does it prevent the issue from happening again
Line 1845: in the future, but it also allows you to isolate the system where the bug is happening,
Line 1846: design a fix, and make sure you actually fix the right bug.
Line 1847: Summary
Line 1848: We saw how acceptance tests can be used to make clear what we want to build and guide
Line 1849: us step by step through what we have to build next, while lower-level tests, such as unit
Line 1850: and integration tests, can be used to tell us how we want to build it and how we want the
Line 1851: various pieces to work together.
Line 1852: In this case, our application was fairly small, so we used the acceptance test to verify the
Line 1853: integration of our pieces. However, in the real world, as we grow the various parts of our
Line 1854: infrastructure, we will have to introduce tests to confirm they are able to work together and
Line 1855: the reason is their intercommunication protocol.
Line 1856: Once we found a bug, we also saw how regression tests can help us design fixes and how
Line 1857: they can prevent the same bug from happening again in the long term.
Line 1858: During any stage of software development, the Design, Implementation, and Maintenance
Line 1859: workflow helps us better understand what we are trying to do and thus get the right
Line 1860: software, code, and bug fixes in place.
Line 1861: So far, we've worked with fairly small test suites, but the average real-world software has
Line 1862: thousands of tests, so particular attention to how we organize will be essential to a test suite
Line 1863: we feel we can rely on. In the next chapter, we are thus going to see how to scale test suites
Line 1864: when the number of tests becomes hard to manage and the time it takes to run the test suite
Line 1865: gets too long to run it all continuously.