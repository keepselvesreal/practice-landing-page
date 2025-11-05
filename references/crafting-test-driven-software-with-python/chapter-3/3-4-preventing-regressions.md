# 3.4 Preventing regressions (pp.105-113)

---
**Page 105**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 105 ]
Our data is unable to load due to an issue in the BasicDB persistence layer, and we will
have to fix our bug if we ever want to be able to use our TODO application. This is actually
great because TDD has a best practice that allows us to tackle these bugs. Let's introduce
regression tests.
Preventing regressions
Tests are not only used to drive our application design and our code design, but also drive
our research and the debugging of the issues that our application faces.
Whenever we face any kind of error, bug, or crash, our fixing process should start with
writing a regression test – a test whose purpose is to reproduce the same exact issue we are
facing.
Having a regression test in place will prevent that bug from happening again in the future,
even if someone refactors some of the code or replaces the implementation. That's not all a
test can do – once we've written a test that reproduces our issue, we will be able to more
easily debug the issue and see what's going on in a fully controlled and isolated
environment such as a test suite.
As our application crashed trying to load our database, we are going to write a test for it
and see what the problem is.
The first step is writing a test that reproduces the same exact steps that the user did to
trigger the condition, so we are going to write a test in tests/test_regressions.py that
is going to reproduce our most recent user sessions in the application.
Our first goal is to be able to reproduce the issue. To do so, we are going to use the setup
that is most similar to that in the real world. So we are going to reuse the setup code from
our acceptance tests and create a TestRegressions class:
import unittest
import threading
import queue
import tempfile
import pathlib
from todo.app import TODOApp
from todo.db import BasicDB
class TestRegressions(unittest.TestCase):
    def setUp(self):


---
**Page 106**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 106 ]
        self.inputs = queue.Queue()
        self.outputs = queue.Queue()
        self.fake_output = lambda txt: self.outputs.put(txt)
        self.fake_input = lambda: self.inputs.get()
        self.get_output = lambda: self.outputs.get(timeout=1)
        self.send_input = lambda cmd: self.inputs.put(cmd)
This is the same exact setUp code we had in our acceptance tests for fake I/O. We could
inherit from the same base class or use a mixin to provide the setup of our fake I/O, but
here we just copied those same few lines of code.
Then we are going to add a test_os_release method that reproduces exactly what
happened in our real usage session:
   def test_os_release(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            app_thread = threading.Thread(
                target=TODOApp(
                    io=(self.fake_input, self.fake_output),
                    dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
                ).run,
                daemon=True
            )
            app_thread.start()
            self.get_output()
            self.send_input("add buy milk")
            self.send_input('add "Focal Fossa"')
            self.send_input("quit")
            app_thread.join(timeout=1)
            while True:
                try:
                    self.get_output()
                except queue.Empty:
                    break
            app_thread = threading.Thread(
                target=TODOApp(
                    io=(self.fake_input, self.fake_output),
                    dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
                ).run,
                daemon=True
            )
            app_thread.start()
            self.get_output()


---
**Page 107**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 107 ]
First, we start the application, then we add a note to buy milk, install the Focal Fossa
release, and then we quit. Subsequently, we just restart the application.
If we run our test, it should reproduce the same exact steps that happened in our software
and thus trigger the same exact crash:
$ python -m unittest discover -k regression
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
    self._entries = self._dbmanager.load()
  File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
    return eval(txt)
  File "<string>", line 1
    ["buy milk", "install "Focal Fossa""]
                           ^
SyntaxError: invalid syntax
OK, the crash is there and it's the same exact traceback. So we were able to reproduce the
issue! Our next step is to isolate the issue to find what really causes it and which part of our
system is involved in the problem itself.
To do so, we are going to move from a test that really runs the application to a simpler one
that does not involve the whole machinery and I/O support. Let's see whether we can
reproduce the issue by replacing our fairly long and complete TestRegressions class
with one that just starts the application with a stubbed set of inputs and then restarts it:
import unittest
from unittest import mock
import tempfile
import pathlib
from todo.app import TODOApp
from todo.db import BasicDB
class TestRegressions(unittest.TestCase):
    def test_os_release(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            app = TODOApp(
                io=(mock.Mock(side_effect=[
                    "add buy milk",
                    'add install "Focal Fossa"',


---
**Page 108**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 108 ]
                    "quit"
                ]), mock.Mock()),
                dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
            )
            app.run()
            restarted_app = TODOApp(
                io=(mock.Mock(side_effect="quit"), mock.Mock()),
                dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
            )
            restarted_app.run()
If we rerun our regression tests, we are luckily going to see that it still fails as before:
$ python -m unittest discover -k regression
E
======================================================================
ERROR: test_os_release (tests.test_regressions.TestRegressions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/03_regression/tests/test_regressions.py", line 27,
in test_os_release
    restarted_app.run()
  File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
    self._entries = self._dbmanager.load()
  File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
    return eval(txt)
  File "<string>", line 1
    ["buy milk", "install "Focal Fossa""]
                           ^
SyntaxError: invalid syntax
----------------------------------------------------------------------
Ran 1 test in 0.003s
FAILED (errors=1)
This helped us confirm that the I/O doesn't really matter and that running the application
for real is not involved in causing our bug. We greatly reduced the scope of the involved
entities to just TODOApp and BasicDB objects.
There is still the filesystem involved; does that matter? Is it a problem with the fact that we
are reading and writing files?


---
**Page 109**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 109 ]
To check that, let's move forward further and get rid of the filesystem too. We can use an
opener that provides an in-memory file instead of a real one so that where we write doesn't
matter anymore:
import unittest
from unittest import mock
import io
from todo.app import TODOApp
from todo.db import BasicDB
class TestRegressions(unittest.TestCase):
    def test_os_release(self):
        fakefile = io.StringIO()
        fakefile.close = mock.Mock()
        app = TODOApp(
            io=(mock.Mock(side_effect=[
                "add buy milk",
                'add install "Focal Fossa"',
                "quit"
            ]), mock.Mock()),
            dbmanager=BasicDB(None, _fileopener=mock.Mock(
                side_effect=[FileNotFoundError, fakefile]
            ))
        )
        app.run()
        # rollback the file. So that the application, restarting,
        # can read the new data that we wrote.
        fakefile.seek(0)
        restarted_app = TODOApp(
            io=(mock.Mock(return_value="quit"), mock.Mock()),
            dbmanager=BasicDB(None, _fileopener=mock.Mock(
                return_value=fakefile
            ))
        )
        restarted_app.run()
Our test now creates an io.StringIO instance instead of using a real file, so it doesn't
depend anymore on a real disk. We replaced the standard io.StringIO.close() method
with a dummy one, so that the file never gets closed and we can read it again. Otherwise,
after it's used for the first time it will be lost forever.


---
**Page 110**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 110 ]
Then we started the application with a _fileopener that firstly triggers
FileNotFoundError, causing the application to start with an empty todo list, and
secondly returns the fake file so that the data gets saved to the fake file. The same fake file,
from which the application once restarted, will read the todo items.
Rerunning our regression test will confirm that we are still able to reproduce the same exact
issue, and thus our test is still valid:
$ python -m unittest discover -k regression
E
======================================================================
ERROR: test_os_release (tests.test_regressions.TestRegressions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/03_regression/tests/test_regressions.py", line 36,
in test_os_release
    restarted_app.run()
  File "/tddbook/03_tdd/03_regression/src/todo/app.py", line 15, in run
    self._entries = self._dbmanager.load()
  File "/tddbook/03_tdd/03_regression/src/todo/db.py", line 12, in load
    return eval(txt)
  File "<string>", line 1
    ["buy milk", "install "Focal Fossa""]
                           ^
SyntaxError: invalid syntax
----------------------------------------------------------------------
Ran 1 test in 0.002s
FAILED (errors=1)
OK, we removed every interaction with the outer world. We know that our problem can be
reproduced solely with TODOApp and BasicDB. What else can we try to remove from the
equation to further reduce the area where our issue might live and identify the minimum
system components necessary to reproduce our issue?
Our issue crashes in BasicDB.load(), so there is a high chance that it's caused by loading
back the data that we saved. So let's get rid of TODOApp and try to directly save and load
back our list of two items.
Our final version of the test is fairly minimal and has isolated BasicDB on its own:
class TestRegressions(unittest.TestCase):
    def test_os_release(self):
        fakefile = io.StringIO()
        fakefile.close = mock.Mock()


---
**Page 111**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 111 ]
        data = ["buy milk", 'install "Focal Fossa"']
        dbmanager = BasicDB(None, _fileopener=mock.Mock(
            return_value=fakefile
        ))
        dbmanager.save(data)
        fakefile.seek(0)
        loaded_data = dbmanager.load()
        self.assertEqual(loaded_data, data)
Running our test does indeed fail with the same exact error that we had before:
$ python -m unittest discover -k regression
E
======================================================================
ERROR: test_os_release (tests.test_regressions.TestRegressions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File
"/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/03_regression/tes
ts/test_regressions.py", line 22, in test_os_release
    loaded_data = dbmanager.load()
  File
"/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/03_regression/src
/todo/db.py", line 12, in load
    return eval(txt)
  File "<string>", line 1
    ["buy milk", "install "Focal Fossa""]
                           ^
SyntaxError: invalid syntax
----------------------------------------------------------------------
Ran 1 test in 0.001s
FAILED (errors=1)
So we were able to get a test involving the minimum possible number of entities in isolation
to reproduce our issue. Only BasicDB is in use in our test, so we now know for sure that
that's where our issue lies.
Our issue is due to the fact that we tried to save and load data in JSON format, relying on
the fact that the Python syntax for arrays of strings is nearly the same as JSON. Thus using
repr and eval could work to generate the JSON and load it back.
Sadly, that was a pretty terrible idea that we put in place for the sole purpose of
reproducing this issue. Evaluating user inputs is generally a big security hole.


---
**Page 112**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 112 ]
If instead of install "Focal Fossa", we wrote "] + [print("hello")] + [" as our
todo item, that would have resulted in our TODOApp executing the Python print function
when loading back todo items (because what we saved was ["buy milk", ""] +
[print("hello")] + [""] ) and instead of print, we could have forced the app to do
anything when loading back the todo items.
eval should never be used with input that comes from users, so let's replace our BasicDB
implementation with one that uses the json module:
import json
class BasicDB:
    def __init__(self, path, _fileopener=open):
        self._path = path
        self._fileopener = _fileopener
    def load(self):
        try:
            with self._fileopener(self._path, "r",
                                  encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    def save(self, values):
        with self._fileopener(self._path, "w+", encoding="utf-8") as f:
            f.write(json.dumps(values))
The only part we changed in BasicDB.load is that instead of using eval, we now use
json.load, and in BasicDB.save, instead of repr we use json.dumps.
This uses the JSON module to save and load our data, removing the risk of malicious code
execution.
If we did everything correctly, our test for the bug should finally pass, while our
application continues to pass all other existing tests as well:
$ python -m unittest discover -v
test_main (tests.test_acceptance.TestTODOAcceptance) ... ok
test_persistence (tests.test_acceptance.TestTODOAcceptance) ... ok
test_os_release (tests.test_regressions.TestRegressions) ... ok
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_save (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok


---
**Page 113**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 113 ]
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 9 tests in 1.015s
OK
It seems we succeeded! We identified the bug, fixed it, and now have a test preventing the
same bug from happening again.
I hope the benefit of starting any bug-and-issue resolution by first writing a test that
reproduces the issue itself is clear. Not only does it prevent the issue from happening again
in the future, but it also allows you to isolate the system where the bug is happening,
design a fix, and make sure you actually fix the right bug.
Summary
We saw how acceptance tests can be used to make clear what we want to build and guide
us step by step through what we have to build next, while lower-level tests, such as unit
and integration tests, can be used to tell us how we want to build it and how we want the
various pieces to work together.
In this case, our application was fairly small, so we used the acceptance test to verify the
integration of our pieces. However, in the real world, as we grow the various parts of our
infrastructure, we will have to introduce tests to confirm they are able to work together and
the reason is their intercommunication protocol.
Once we found a bug, we also saw how regression tests can help us design fixes and how
they can prevent the same bug from happening again in the long term.
During any stage of software development, the Design, Implementation, and Maintenance
workflow helps us better understand what we are trying to do and thus get the right
software, code, and bug fixes in place.
So far, we've worked with fairly small test suites, but the average real-world software has
thousands of tests, so particular attention to how we organize will be essential to a test suite
we feel we can rely on. In the next chapter, we are thus going to see how to scale test suites
when the number of tests becomes hard to manage and the time it takes to run the test suite
gets too long to run it all continuously.


