# 3.2 Starting projects with TDD (pp.68-83)

---
**Page 68**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 68 ]
In this chapter, we will cover the following topics:
Starting projects with TDD
Building applications the TDD way
Preventing regressions
Technical requirements
A working Python interpreter should be all that is needed to work through the exercises in
this chapter.
The examples have been written using Python 3.7, but should work on most modern
Python versions.
You can find the code files used in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter03
Starting projects with TDD
We already know that tests are meant to verify that our software adheres to the desired
behavior. To do so means that our tests must express what that desired behavior is. They
must explicitly state, "If I do this, I expect that to happen."
For the innermost components, what happens is probably an implementation detail: "If I
commit my unit of work, data is written to the database." But the more we move to the outer
parts of our architecture, those that connect our software to the outside world, the more
these tests become expressions of business needs. The more we move from solitary units, to
sociable units, to integration and acceptance tests, the more the "desired behavior" becomes
the one that has a business value.
If we work with a test-driven approach, our first step before writing implementation code
is obviously to write a test that helps us understand what we want to build (if we are just
starting with our whole project, what we want to build is the software itself). This means
that our very first test is the one that is going to make clear what's valuable. Why are we
even writing the software in the first place?
So let's see how a test-driven approach can benefit us during the software design phase
itself. Suppose we want to start a TODO list kind of product.


---
**Page 69**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 69 ]
So let's start writing an acceptance test that will help us express explicitly what we want
our app to do.
Let's create a new todo directory where we are going to put the todo/src subdirectory
with our source code, and the todo/tests directory with our tests:
$ tree
.
├── src
└── tests
At this point, we can start by making a todo/tests/__init__.py file and a
todo/tests/test_acceptance.py module for our overall application acceptance test.
The test_acceptance.py file is going to contain our test itself:
import unittests
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        raise NotImplementedError()
We want our interactive shell application to accept commands and print outputs. So the
first thing we want the app to do is to write the output and receive commands from an
input:
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
We don't yet know what our fake_input and fake_output will be, but we will figure
that out as we reduce uncertainty about how the app should behave.
Then we said we want it to be an interactive shell, so it should be sitting there accepting
commands until we tell it to quit. To make that happen we probably want to have the main
loop for our Read-Eval-Print Loop (REPL) and we want the app to be running in the
background during our test so we can send commands to it and fetch the responses:
import unittest
import threading
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))


---
**Page 70**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 70 ]
        app_thread = threading.Thread(target=app.run, daemon=True)
        app_thread.start()
But we don't want our app to be stuck there forever until the user kills it abruptly due to
the frustration of being unable to exit it, and we surely don't want our test to be stuck there
forever either. So we want our app to support a quit command and ensure it exits when it
receives it:
import unittest
import threading
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
        app_thread = threading.Thread(target=app.run, daemon=True)
        app_thread.start()
        # ...
        self.send_input("quit")
        app_thread.join(timeout=1)
        self.assertEqual(self.get_output(), "bye!\n")
Great, now we know we want our app to sit there, accept commands, and exit on a quit
request. But how are we going to tell the user that we are accepting commands? We likely
want a prompt, so let's verify that by presenting a welcome screen with the list of the
TODO items (none at the beginning) and a "> " prompt:
import unittest
import threading
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
        app_thread = threading.Thread(target=app.run, daemon=True)
        app_thread.start()
        welcome = self.get_output()
        self.assertEqual(welcome, (
            "TODOs:\n"
            "\n"
            "\n"
            "> "


---
**Page 71**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 71 ]
        ))
        self.send_input("quit")
        app_thread.join(timeout=1)
        self.assertEqual(self.get_output(), "bye!\n")
Very well, we've already provided answers to tons of questions about how our app should
behave. We decided it's driven by commands and those commands can be provided
through a prompt on the same screen that displays the list of our items.
What primary commands do we want to provide? Surely we at least want to be able to add
new items and delete them? So let's test that we can execute those commands:
import unittest
import threading
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
        app_thread = threading.Thread(target=app.run, daemon=True)
        app_thread.start()
        welcome = self.get_output()
        self.assertEqual(welcome, (
            "TODOs:\n"
            "\n"
            "\n"
            "> "
        ))
        self.send_input("add buy milk")
        welcome = self.get_output()
        self.assertEqual(welcome, (
            "TODOs:\n"
            "1. buy milk\n"
            "\n"
            "> "
        ))
        self.send_input("add buy eggs")
        welcome = self.get_output()
        self.assertEqual(welcome, (
            "TODOs:\n"
            "1. buy milk\n"
            "2. buy eggs\n"
            "\n"


---
**Page 72**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 72 ]
            "> "
        ))
        self.send_input("del 1")
        welcome = self.get_output()
        self.assertEqual(welcome, (
            "TODOs:\n"
            "1. buy eggs\n"
            "\n"
            "> "
        ))
        self.send_input("quit")
        app_thread.join(timeout=1)
        self.assertEqual(self.get_output(), "bye!\n")
OK, we added a block where we add a note to "buy milk", one with a note to "buy eggs",
and a third where we delete the "buy milk" entry. Our acceptance test is now fairly
complete! It adds multiple todos and it removes them. We've defined everything we want
our app to do and we can now move forward to finally trying to satisfy our needs!
The test itself is going to do the next step; we simply have to run it:
$ python -m unittest discover
E
======================================================================
ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testingbook/03_specifications/01_todo/tests/test_acceptance.py",
line 20, in test_main
    app = TODOApp(io=(self.fake_input, self.fake_output))
NameError: name 'TODOApp' is not defined
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Right, we now need to make the app itself as it doesn't even exist yet as a concept.
For the sake of focusing this section on the business value of our application and thus on
the user-facing tests, we are going to diverge a bit from the correct approach and we are
going to have a single test for the whole app.


---
**Page 73**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 73 ]
So don't be surprised if we jump here from an acceptance test directly to the
implementation of the app itself. It's only for the sake of reducing the cognitive load of the
reader. In the real world, we would be writing unit tests to drive the design of our code, as
designing the app and designing its implementation are two very different things. But here
we wanted to make clear how writing tests forces us to think about the app itself, and thus
we are going to make the code design happen behind the scenes.
In the Building applications the TDD way section, we are going to see how to mix what we
learned here about acceptance tests with the more classical TDD approach regarding the
design of the code itself.
So let's create a new todo Python package inside our src directory. We are going to have a
src/todo/__init__.py file and a src/todo/app.py module for the application
implementation itself:
$ tree
.
├── src
│   ├── todo
│   │   ├── app.py
│   │   ├── __init__.py
└── tests
    ├── __init__.py
    └── test_acceptance.py
Our TODOApp can reside in src/todo/app.py for now, just as an empty class:
class TODOApp:
    pass
Is this enough to be able to use our app from the tests? Not yet, because the todo package is
not available for our tests. So before moving forward, we want to add a src/setup.py file
to make a distribution for our todo package. Our minimal setup.py file is just going to tell
the Python installer that "The application is named todo and it contains a todo package that has to
be installed":
from setuptools import setup
setup(name='todo', packages=['todo'])


---
**Page 74**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 74 ]
Then the final layout of our project directory should look pretty much like this:
$ tree
.
├── src
│   ├── setup.py
│   ├── todo
│   │   ├── app.py
│   │   ├── __init__.py
└── tests
    ├── __init__.py
    └── test_acceptance.py
At this point, we can install our application in development mode with pip install -e:
$ pip install -e src/
Obtaining file://testingbook/03_specifications/01_todo/src
Installing collected packages: todo
  Running setup.py develop for todo
Successfully installed todo
This allows us to edit our tests/test_acceptance.py file to import the application class
itself and solve the previous NameError error:
import unittest
from todo.app import TODOApp
class TestTODOAcceptance(unittest.TestCase):
    def test_main(self):
        ...
We already know that our TODOApp does nothing, so it surely won't make our test pass, but
let's see what our test suggests for the next required step that involves rerunning our test
suite:
$ python -m unittest discover
======================================================================
ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
...
    app = TODOApp(io=(self.fake_input, self.fake_output))
AttributeError: 'TestTODOAcceptance' object has no attribute 'fake_input'
Given that we've now installed the todo package, the app imports fine, but the test has no
fake_input and fake_output to provide. So those are going to be our next areas of
attention.


---
**Page 75**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 75 ]
As we want to ship input and outputs back and forth between the test and the app, wait for
the outputs to be available, and use something that works across threads, a well-fitting
solution might be to use a queue. During the application execution, our output function
will probably be the print function and our input will be the Python input function, so
let's set up something that allows us to simulate those.
In our test case setup, we are going to create the Input/Output (I/O) queues and create a
self.fake_input object that simulates the behavior of input and a self.fake_output
object that simulates the behavior of print. Also for convenience, we are going to add the
self.get_output and self.send_input methods so that our test can send and receive
text from the app:
import unittest
import threading
import queue
from todo.app import TODOApp
class TestTODOAcceptance(unittest.TestCase):
    def setUp(self):
        self.inputs = queue.Queue()
        self.outputs = queue.Queue()
        self.fake_output = lambda txt: self.outputs.put(txt)
        self.fake_input = lambda: self.inputs.get()
        self.get_output = lambda: self.outputs.get(timeout=1)
        self.send_input = lambda cmd: self.inputs.put(cmd)
    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
        ...
OK, we should have in place our I/O infrastructure for the tests. Will our test move
forward? Let's see:
$ python -m unittest discover
======================================================================
ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
...
    app = TODOApp(io=(self.fake_input, self.fake_output))
TypeError: TODOApp() takes no arguments
OK, not as much as hoped. It did move forward, but we crashed on the same exact line of
code because our TODOApp doesn't yet have any concept of I/O.


---
**Page 76**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 76 ]
So let's make our TODOApp aware of its input and output. By default, we are going to
provide the built-in Python input and print commands (without the trailing newline),
but our test will replace those with its own fake_input and fake_output:
import functools
class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
OK, we now have a TODOApp._in callable we can use to ask for inputs, and a
TODOApp._out callable we can use to write outputs. What's the next step?
$ python -m unittest discover
======================================================================
ERROR: test_main (tests.test_acceptance.TestTODOAcceptance)
...
    app_thread = threading.Thread(target=app.run)
AttributeError: 'TODOApp' object has no attribute 'run'
Right, the REPL! Our app needs to leverage those I/O functions to actually show the output
and ask for inputs. So we are going to add a TODOApp.run function that runs our REPL,
providing the prompt and accepting commands until we quit:
import functools
class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(""))
            command = self._in()
        self._out("bye!\n")
    def prompt(self, output):
        return """TODOs:
{}
> """.format(output)
For now, our interactive shell doesn't do much – it shows the prompt and does nothing
with the commands we send.


---
**Page 77**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 77 ]
If we run our acceptance test again, we are going to clearly see that our app did receive the
add command to add the buy milk entry, but it didn't execute it and so the entry isn't
there:
$ python -m unittest discover
======================================================================
...
AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
  TODOs:
-
+ 1. buy milk
Our next step is adding the command dispatching and execution functionality so that the
REPL not only receives those commands, but also executes them:
import functools
class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(""))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")
    def prompt(self, output):
        return """TODOs:
{}
> """.format(output)
    def _dispatch(self, cmd):
        cmd, *args = cmd.split(" ", 1)
        executor = getattr(self, "cmd_{}".format(cmd), None)
        if executor is None:
            self._out("Invalid command: {}\n".format(cmd))
            return
        executor(*args)


---
**Page 78**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 78 ]
The TODOApp.run method is in charge of calling TODOApp._dispatch to serve commands,
and each command will be served by running a TODOApp.cmd_COMMANDNAME method that
we will implement for each command.
If we rerun our test, we are going to get complaints about invalid commands being sent to
the application:
$ python -m unittest discover
======================================================================
FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
...
AssertionError: 'Invalid command: add\n' != 'TODOs:\n1. buy milk\n\n> '
- Invalid command: add
+ TODOs:
+ 1. buy milk
+
+ >
This is pretty much expected because we have not yet implemented any commands.
So let's provide our add command, which is simply going to get the entry to add and insert
the todo item into the list of our TODO entries:
class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
        self._entries = []
    ...
    def cmd_add(self, what):
        self._entries.append(what)


---
**Page 79**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 79 ]
Rerunning our acceptance test will confirm that the Invalid command message went
away, and thus we can now handle the command, but we still don't print back the list of
todo items. So even if the todo entry was added to our todo list, it's not displayed back to
us:
$ python -m unittest discover
======================================================================
FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
...
AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
  TODOs:
-
+ 1. buy milk
  >
Instead of showing an empty prompt, like the current self.prompt("") call is doing, we
want to actually show the list of our TODO items. So we are going to add an items_list
method to our TODOApp that returns the content we want to display in the prompt through
self.prompt(self.items_list()) during the REPL loop within TODOApp.run:
class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
        self._entries = []
    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")
    def items_list(self):
        enumerated_items = enumerate(self._entries, start=1)
        return "\n".join(
            "{}. {}".format(idx, entry) for idx, entry in enumerated_items
        )
    ...
Our application will now be able to finally serve its first complete cycle, receiving the add
command and showing us the list of items with the newly added entry.


---
**Page 80**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 80 ]
If we rerun our test, we no longer get stuck on the same issue of having an empty list of
todo items, but we are going to get complaints about the fact that the del command is not
yet implemented:
$ python -m unittest discover
======================================================================
FAIL: test_main (tests.test_acceptance.TestTODOAcceptance)
...
AssertionError: 'Invalid command: del\n' != 'TODOs:\n1. buy eggs\n\n> '
- Invalid command: del
+ TODOs:
+ 1. buy eggs
+
+ >
So let's implement the remaining two commands, del and quit, and check whether our
app is complete:
class TODOApp:
    ...
    def cmd_quit(self, *_):
        self._quit = True
    def cmd_add(self, what):
        self._entries.append(what)
    def cmd_del(self, idx):
        idx = int(idx) - 1
        if idx < 0 or idx >= len(self._entries):
            self._out("Invalid index\n")
            return
        self._entries.pop(idx)
    ...
The cmd_del function just checks whether a valid index to be removed was provided, and
then removes it from the list of todo entries. The cmd_quit command just sets a flag that
will make our REPL exit when it finds it on the next loop cycle.
Now that the functionality to add todo items, remove them, and quit the app has been
implemented, our test will finally succeed and confirm our application matches our
requirements:
$ python -m unittest discover
.
----------------------------------------------------------------------


---
**Page 81**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 81 ]
Ran 1 test in 0.001s
OK
So far, we made an entire application without launching it even once. We had the whole
implementation driven by our acceptance test. Will the app really work and do what we
wanted? Did acceptance tests really help us design the application behavior?
To check whether the experience is the one we expected, let's make our application
runnable. This can be done by adding a __main__.py file to our todo package within
src/todo. The updated result of our project layout should thus be as follows:
$ tree
.
├── src
│   ├── setup.py
│   └── todo
│       ├── app.py
│       ├── __init__.py
│       └── __main__.py
└── tests
    ├── __init__.py
    └── test_acceptance.py
3 directories, 6 files
And the content of src/todo/__main__.py will be very simple — it will just create our
TODOApp and will enter the main loop:
from .app import TODOApp
TODOApp().run()
Our app can now be started with the python -m todo command. Let's see whether the
behavior is actually what we imagined and our test-driven design approach really leads to
the app we expected:
$ python -m todo
TODOs:
> add buy some milk
TODOs:
1. buy some milk
> add buy water
TODOs:
1. buy some milk


---
**Page 82**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 82 ]
2. buy water
> add send happy birthday message
TODOs:
1. buy some milk
2. buy water
3. send happy birthday message
> del 1
TODOs:
1. buy water
2. send happy birthday message
> del 1
TODOs:
1. send happy birthday message
> quit
bye!
Definitely, the app behaves as we expected! We were welcomed by a prompt with an
empty list of todo items and as we added and removed them, our prompt updated with the
new state of our todo list. The app delivered exactly the experience we described in our test
and supports all the features we wanted, working flawlessly on the first run.
This approach of driving the whole software design and development process from
business-oriented acceptance tests usually comes under the umbrella of Acceptance Test-
Driven Development (ATDD).
We saw how tests not only verify the correctness of the software but at the outer layers, can
also explain what the primary software behaviors are and what the software's business
value is.
This means that tests can tell a story – if I read them, I'm going to know exactly how the
software behaves in that context. If the software has a good enough test coverage and I read
all the tests, then I'm going to know how the software works as a whole. Thus tests can be
used to express the software specification itself in a reliable and testable manner, which is a
concept frequently referred to as Specification by Example.
We are going to get into more details about this concept in Chapter 7, Fitness Function with
a Contact Book Application, but for now, let's focus on how to attach this concept of designing
the software through tests to the concept of designing its implementation through tests.


---
**Page 83**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 83 ]
Building applications the TDD way
In the previous section, we saw how to use tests to design our application itself, exposing
clear goals and forcing us to think about how the application should behave.
Once we start thinking a bit about what a test is actually doing, it slowly becomes clear why
that works well: the tests are going to interact with the system under test. The way they are
going to interact with the system they have to test is usually through the interface that the
system exposes.
This means that the capabilities we are going to expose to any black-box test are the same
capabilities that we are going to expose to any other user of the system under test.
If the system under test is the whole application, as in the case of the previous section, then
it means that to write the test we will be forced to reason about the capabilities and the
interface we are going to expose to our users themselves. In practice, having to write a test
for that layer forces us to make clear the UI and UX of our application.
If the system under test is instead a component of the whole application, the user of that
component will be another software component; another piece of code calling the first one.
This means that to write the test, we will be forced to define the API that our component
has to expose, and thus design the implementation of the component itself.
Thus embracing TDD helps us design code with well-thought-out APIs that the rest of the
system can depend on, but writing tests beforehand is not the sum of all TDD practices.
There are two primary rules that are part of the TDD practice: the first is obviously to write
failing tests before you write the code, but the second is that once your tests pass, you
should refactor to remove duplication.
This means that it not only forces us to think of the public interfaces that our objects and
subsystems are going to expose beforehand, but it also forces us to keep our internals in
shape through continuous refactoring.
The TODO list application we made does everything we wanted, but it lacks a fairly major
feature before it can become a valuable application we can use for real: it doesn't persist our
todo items. If we close the application and restart it, we are going to lose all our items.
We definitely want our TODO app to save and reload our todo items, so we are going to
work on a new feature to enable that behavior.


