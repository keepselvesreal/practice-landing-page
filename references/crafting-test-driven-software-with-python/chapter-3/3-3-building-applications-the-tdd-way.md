# 3.3 Building applications the TDD way (pp.83-105)

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


---
**Page 84**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 84 ]
As usual, we are going to start with a very high-level acceptance test that shows what we
want the experience for the user to be. Our new test_persistence test is going to start a
new todo app with an empty database, save an item, quit the app, and restart it again on
the same database to check that the items are still there:
...
import tempfile
class TestTODOAcceptance(unittest.TestCase):
    ...
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            app_thread = threading.Thread(
                target=TODOApp(
                    io=(self.fake_input, self.fake_output),
                    dbpath=tmpdirname
                ).run,
                daemon=True
            )
            app_thread.start()
            welcome = self.get_output()
            self.assertEqual(welcome, (
                "TODOs:\n"
                "\n"
                "\n"
                "> "
            ))
            self.send_input("add buy milk")
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
                    dbpath=tmpdirname
                ).run,
                daemon=True
            )


---
**Page 85**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 85 ]
            app_thread.start()
            welcome = self.get_output()
            self.assertEqual(welcome, (
                "TODOs:\n"
                "1. buy milk\n"
                "\n"
                "> "
            ))
            self.send_input("quit")
            app_thread.join(timeout=1)
First of all, our test makes a new temporary directory called tmpdirname, where we are
going to save our database for the app under test. Then, as in the previous acceptance test,
it starts the application in the background, pointing it to our fake I/O and the temporary
path for the database. Once the app starts, we verify that, on first execution, it starts with an
empty TODO list. Then we add one item to the app and we quit. At this point, we can
restart the application again using the same exact database path, and check that the item we
added is still there after the app restarts. Then we can just quit the app, as it did what we
wanted to test.
Obviously, if we start our test suite, we already know that our new acceptance test is not
going to pass. We haven't implemented the persistence of our todo items at all and our app
doesn't even accept a dbpath argument:
$ python -m unittest discover -v
test_main (tests.test_acceptance.TestTODOAcceptance) ... ok
test_persistence (tests.test_acceptance.TestTODOAcceptance) ... ERROR
======================================================================
ERROR: test_persistence (tests.test_acceptance.TestTODOAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testingbook/03_tdd/02_codedesign/tests/test_acceptance.py", line
72, in test_persistence
    dbpath=tmpdirname
TypeError: __init__() got an unexpected keyword argument 'dbpath'
----------------------------------------------------------------------
Ran 2 tests in 0.004s
FAILED (errors=1)
Our next step is to move one layer below and start working on our implementation.


---
**Page 86**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 86 ]
Thus the tests that we are going to write will get further away from the end user point of
view that we used in the acceptance tests, and move toward describing what we want our
inner implementation to be.
For this reason, we are going to create a separate directory for these tests so that they don't
get confused with the higher-level tests that tell the story from the user's point of view. So
inside our tests directory, we are going to create a subdirectory for unit tests.
Then, inside that directory, we are going to add a test_todoapp.py file to start reasoning
about how we want to change our TODOApp object to support persistence:
└── tests
    ├── __init__.py
    ├── test_acceptance.py
    └── unit
        ├── __init__.py
        └── test_todoapp.py
Our test_todoapp.py file is going to start with a very simple test, one to verify that we
can accept a database path for our TODO app and that if omitted, it should use the current
directory:
import unittest
import tempfile
from pathlib import Path
from todo.app import TODOApp
class TestTODOApp(unittest.TestCase):
    def test_default_dbpath(self):
        app = TODOApp()
        assert Path(".").resolve() == Path(app._dbpath).resolve()
    def test_accepts_dbpath(self):
        expected_path = Path(tempfile.gettempdir(), "something")
        app = TODOApp(dbpath=str(expected_path))
        assert expected_path == Path(app._dbpath)
Now we can forget for a little about our acceptance tests and focus on our unit tests. We are
going to run them in isolation with the -k unit option to confirm that they fail as we
expect, and we can move on to adding support for the dbpath to our object:
$ python -m unittest discover -k unit
EE
======================================================================


---
**Page 87**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 87 ]
ERROR: test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testingbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line
12, in test_accepts_dbpath
    app = TODOApp(dbpath=str(expected_path))
TypeError: __init__() got an unexpected keyword argument 'dbpath'
======================================================================
ERROR: test_default_dbpath (tests.unit.test_todoapp.TestTODOApp)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testingbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line
9, in test_default_dbpath
    assert Path(".").resolve() == Path(app._dbpath).resolve()
AttributeError: 'TODOApp' object has no attribute '_dbpath'
----------------------------------------------------------------------
Ran 2 tests in 0.001s
FAILED (errors=2)
The -k option for unit tests only runs the tests that contain the provided substring, so it's
going to identify only our tests inside the unit directory. It would obviously also run any
tests that had unit in the name, but it's generally a convenient way to select some tests to
run without having to remember in which exact directory they exist.
Now the implementation is fairly easy, we just want to make TODOApp able to remember
where it has to save the database and have it always available as TODOApp._dbpath. So we
are going to modify our TODOApp.__init__ to accept the extra argument and put it aside:
...
class TODOApp:
    def __init__(self,
                 io=(input, functools.partial(print, end="")),
                 dbpath=None):
        self._in, self._out = io
        self._quit = False
        self._entries = []
        self._dbpath = dbpath or "."
    ...


---
**Page 88**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 88 ]
If we did this correctly, the tests for our implementation should now pass without issue:
$ python -m unittest discover -k unit -v
test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
test_default_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.002s
OK
And we can now look back to our acceptance test to find guidance about what to do next:
$ python -m unittest discover
.F..
======================================================================
FAIL: test_persistence (tests.test_acceptance.TestTODOAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/test_acceptance.py", line 108,
in test_persistence
    "TODOs:\n"
AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
  TODOs:
-
+ 1. buy milk
  >
----------------------------------------------------------------------
Ran 4 tests in 1.006s
FAILED (failures=1)
So, now our TODO application is able to start and accept the temporary database path. But
it's not doing what we need. It's not saving anything into the database, so once restarted,
the TODO list is still empty.
At this point, we need to go back to our unit tests and come up with a set of tests to drive
the implementation of our persistence layer so that the data can be saved and loaded back.
Our first test should probably assess that TODOApp is able to load some save data. When we
start thinking of our TestTODOApp.test_load test, it's easy to imagine the Act phase: it
probably just wants to call a TODOApp.load method to load the data. The Assert phase too
is also pretty obvious: TODOApp._entries should probably contain the same exact entries
that we loaded.


---
**Page 89**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 89 ]
But what about the Arrange phase? What are we going to store in the database so that we
can load it back? Which database system are we going to use? And after a while we will
probably move to the "should we even care at all?" question.
Does TODOApp have to care about how data is saved into the database?
Probably not... We should probably delegate that whole problem to another entity, and
only make sure that TODOApp properly invokes that entity and does the right thing with the
data provided by that entity:
...
from unittest.mock import Mock
class TestTODOApp(unittest.TestCase):
    ...
    def test_load(self):
        dbpath = Path(tempfile.gettempdir(), "something")
        dbmanager = Mock(
            load=Mock(return_value=["buy milk", "buy water"])
        )
        app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                      dbpath=dbpath, dbmanager=dbmanager)
        app.run()
        dbmanager.load.assert_called_with(dbpath)
        assert app._entries == ["buy milk", "buy water"]
Our new TestTODOApp.test_load now tests this, provided dbmanager is in charge of
loading/saving data. Our TODOApp is going to use it when it starts, and by virtue of calling
dbmanager, it ends up with the todo entries that dbmanager loaded.
The test prepares a dbpath object for the sole purpose of checking that dbmanager is asked
to load that specific path, then it makes a dbmanager that returns a canned response of two
items when dbmanager.load(dbpath) is invoked. Once those two are in place, it
prepares a TODOApp that has a dummy output and a stubbed input that make the app quit
immediately.
Then, once the app is started through app.run(), we expect it to have called dbmanager
and have loaded the two provided entries.


---
**Page 90**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 90 ]
Now that we have a clearer understanding of what we want to do, we can go back to our
TODOApp and write an implementation that satisfies our test. We are going to extend
TODOApp to support dbmanager and we are going to modify TODOApp.run to load the
existing data when the app is started:
class TODOApp:
    def __init__(self,
                 io=(input, functools.partial(print, end="")),
                 dbpath=None, dbmanager=None):
        self._in, self._out = io
        self._quit = False
        self._entries = []
        self._dbpath = dbpath or "."
        self._dbmanager = dbmanager
    def run(self):
        if self._dbmanager is not None:
            self._entries = self._dbmanager.load(self._dbpath)
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")
Is this enough to make our test pass? Let's find out:
$ python -m unittest discover -k unit -v
test_accepts_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
test_default_dbpath (tests.unit.test_todoapp.TestTODOApp) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.002s
OK
It seems so, which means we achieved what we wanted. But there is something odd in our
implementation. If TODOApp doesn't care about how data is loaded, why does it care where
it is loaded from? The fact that you even need a path from which to load your data seems a
concern of the loader. Maybe we can load data without a path? Maybe we can load things
from remote resources that need a host and port instead of a path? That's something that
only the loader can know.


---
**Page 91**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 91 ]
So let's leverage our refactoring phase, as we made the tests pass, and change everything to
just receive dbmanager. Whether that dbmanager needs a path, and whether that path is to
a file, a directory, or a remote resource, is not something our app should care about.
First, we want to update the tests; instead of passing dbpath, we directly provide
dbmanager itself. dbmanager will know the path. Let's also make a test for the case when
no dbmanager is provided so that the app doesn't crash, but just disables persistency:
import unittest
from unittest.mock import Mock
from todo.app import TODOApp
class TestTODOApp(unittest.TestCase):
    def test_noloader(self):
        app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                      dbmanager=None)
        app.run()
        assert app._entries == []
    def test_load(self):
        dbmanager = Mock(
            load=Mock(return_value=["buy milk", "buy water"])
        )
        app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                      dbmanager=dbmanager)
        app.run()
        dbmanager.load.assert_called_with()
        assert app._entries == ["buy milk", "buy water"]
The first test_noloader test verifies that if there is no dbmanager, the app is still able to
start, while test_load verifies that when dbmanager is used, the data that it provides is
properly loaded by TODOApp.
We can now also throw away our test_accepts_dbpath and test_default_dbpath, as
our TODOApp is no longer in charge of opening the database itself.
Do our newly refactored tests pass? Nope, not anymore:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_todoapp.TestTODOApp) ... FAIL


---
**Page 92**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 92 ]
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
======================================================================
FAIL: test_load (tests.unit.test_todoapp.TestTODOApp)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line 29,
in test_load
    dbmanager.load.assert_called_with()
  File "/usr/lib/python3.7/unittest/mock.py", line 873, in
assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: load()
Actual call: load('.')
----------------------------------------------------------------------
Ran 2 tests in 0.002s
FAILED (failures=1)
Our mock expectation was violated. We expected load to be called with no argument, as
dbmanager should already know where to load from, but instead, we received ".", which
is the default dbpath.
Let's head back to our TODOApp and remove any reference to dbpath, thus removing the
dbpath argument and the self._dbpath attribute:
class TODOApp:
    def __init__(self,
                 io=(input, functools.partial(print, end="")),
                 dbmanager=None):
        self._in, self._out = io
        self._quit = False
        self._entries = []
        self._dbmanager = dbmanager
    def run(self):
        if self._dbmanager is not None:
            self._entries = self._dbmanager.load()
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")


---
**Page 93**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 93 ]
Do our tests now pass? Yes! They do:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.001s
OK
Now that we are happy with our implementation, we can go back to look for things to do.
When looking for things to do, guidance comes from our acceptance tests. If we run them
right now they will probably crash because, in the end, we settled for an interface that is
slightly different from the one we originally thought of:
$ python -m unittest discover
.E..
======================================================================
ERROR: test_persistence (tests.test_acceptance.TestTODOAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File
"/home/amol/wrk/HandsOnTestDrivenDevelopmentPython/03_tdd/02_codedesign/tes
ts/test_acceptance.py", line 74, in test_persistence
    dbpath=tmpdirname,
TypeError: __init__() got an unexpected keyword argument 'dbpath'
----------------------------------------------------------------------
Ran 4 tests in 0.005s
FAILED (errors=1)
We don't receive dbpath anymore, but we want dbmanager. So let's update our test
accordingly.
For now, we don't want to be too refined about our storage; we are just going to store
things in a very simple storage system. Let's call this BasicDB and provide it to the app in
our acceptance tests. They will load and save data from it:
...
import pathlib
...
from todo.db import BasicDB


---
**Page 94**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 94 ]
class TestTODOAcceptance(unittest.TestCase):
    ...
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            app_thread = threading.Thread(
                target=TODOApp(
                    io=(self.fake_input, self.fake_output),
                    dbmanager=BasicDB(pathlib.Path(tmpdirname, "db"))
                ).run,
                daemon=True
            )
            app_thread.start()
            ...
Running our acceptance test now will tell us that the idea might look great, but we still
have to implement BasicDB. So let's create a tests/unit/test_basicdb.py file and
start reasoning how BasicDB should behave.
Our TestBasicDB tests are probably going to be for loading and saving data; for now, let's
start with the loading one as that's what we are concerned about:
import pathlib
import unittest
from unittest import mock
from todo.db import BasicDB
class TestBasicDB(unittest.TestCase):
    def test_load(self):
        mock_file = mock.MagicMock(
            read=mock.Mock(return_value='["first", "second"]')
        )
        mock_file.__enter__.return_value = mock_file
        mock_opener = mock.Mock(return_value=mock_file)
        db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
        loaded = db.load()
        self.assertEqual(loaded, ["first", "second"])
        self.assertEqual(
            mock_opener.call_args[0][0],
            pathlib.Path("testdb")
        )
        mock_file.read.assert_called_with()


---
**Page 95**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 95 ]
We want our BasicDB to read/write data from a file, so we are going to use a mock_file
object that fakes the Python behavior of a file object. When trying to read from it, it's
going to return the content of our BasicDB with two sample entries.
mock_file is going to be what our mock_opener is going to return whenever BasicDB
asks to open a new file. In practice, what we are trying to do is to make sure that with
mock_opener(ANY_PATH) as f: will return our mock_file, so that from the point of
view of BasicDB, there is no difference between using our mock_opener or the Python
open function.
Once our stubbed file opener is available, we are going to create an instance of BasicDB,
providing the stub opener as a replacement for the Python open function. The path we are
going to provide to BasicDB for the storage of its database doesn't really matter at this
point as it will always return mock_file, but we will still be checking that the opener was
called with the expected path.
The real core of our test is the call to db.load(), where we are going to ask BasicDB to
load the data from mock_file. Then we can confirm that the data we expected was loaded
and that it was loaded the way we would expect, by actually opening the file and reading
its content.
In practice, we decided that BasicDB(path).load() will be the way we plan to load the
data in BasicDB.
Now that we've set our expectations clearly and have a better idea of what we want to
build, we can try to work on an implementation that could satisfy the interface we
imagined.
The first step is creating our src/todo/db.py module, as that's where we imagined we
would be importing BasicDB from while writing our test (see the from todo.db import
BasicDB line at the top of our test file).
Then we are going to make a BasicDB class that accepts the file path to save/load data
to/from, and an optional opener so that we can replace the default one with other
alternative implementations. For the goal of making clear that the opener is mostly meant
for testing, we are going to flag it as an internal detail, prefixing its name with an
underscore:
class BasicDB:
    def __init__(self, path, _fileopener=open):
        self._path = path
        self._fileopener = _fileopener


---
**Page 96**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 96 ]
Will this make our tests pass? I doubt it will – it still does nothing, so let's cycle back to our
tests to see which parts of the BasicDB interface we have to implement:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ERROR
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
======================================================================
ERROR: test_load (tests.unit.test_basicdb.TestBasicDB)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/unit/test_basicdb.py", line 18,
in test_load
    loaded = db.load()
AttributeError: 'BasicDB' object has no attribute 'load'
----------------------------------------------------------------------
Ran 3 tests in 0.002s
FAILED (errors=1)
OK, it seems we now want to move to the implementation of BasicDB.load.
The implementation feels pretty straightforward: we open a file that should contain a list of
strings. Let's just read the file content and parse the list definition:
class BasicDB:
    def __init__(self, path, _fileopener=open):
        self._path = path
        self._fileopener = _fileopener
    def load(self):
        with self._fileopener(self._path, "r", encoding="utf-8") as f:
            txt = f.read()
        return eval(txt)


---
**Page 97**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 97 ]
Does this make our tests happy? Are we really able to load the items stored in BasicDB?
Let's find out:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.002s
OK
It seems so – our BasicDB test was able to load the content and fetch back the two items.
For anyone wondering about the usage of eval, please bear with the
example for a little while. We are going to replace it pretty soon and make
clear that using it is never a good idea. But it was a convenient way to
simulate the bug we are going to fix in the dedicated Preventing regressions
section.
All our unit tests now pass, so we are a bit at a loss about where we were and what we
wanted to do next. Whenever we are unsure about our next step, the acceptance tests
should guide us on how far we are from the feature we want to provide for our users. So
let's go back to our acceptance test and see what we still have to do:
$ python -m unittest discover -k acceptance
...
FileNotFoundError: [Errno 2] No such file or directory:
'/tmp/tmpcug9zvsw/db'
Uh, we forgot that when we start the application the first time, our BasicDB is empty;
actually, it doesn't exist at all. So there is nothing we can load. Thus we have to go back to
our unit tests and write one to ensure that when the opened file doesn't exist, we do
actually return an empty list of todo items.
Back to our tests/unit/test_basicdb.py file, we are going to add a new
test_missing_load test:
...
class TestBasicDB(unittest.TestCase):
    ...
    def test_missing_load(self):
        mock_opener = mock.Mock(side_effect=FileNotFoundError)


---
**Page 98**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 98 ]
        db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
        loaded = db.load()
        self.assertEqual(loaded, [])
        self.assertEqual(
            mock_opener.call_args[0][0],
            pathlib.Path("testdb")
        )
This new test is just going to throw FileNotFoundError every time BasicDB tries to read
the data. This simulates the case where we would try to open a nonexistent database.
As expected, our test is going to fail with FileNotFoundError as we haven't handled it
yet:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ERROR
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
======================================================================
ERROR: test_missing_load (tests.unit.test_basicdb.TestBasicDB)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/unit/test_basicdb.py", line 31,
in test_missing_load
    loaded = db.load()
  File "/tddbook/03_tdd/02_codedesign/src/todo/db.py", line 9, in load
    with self._fileopener(self._path, "r", encoding="utf-8") as f:
  File "/usr/lib/python3.7/unittest/mock.py", line 1011, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.7/unittest/mock.py", line 1071, in _mock_call
    raise effect
FileNotFoundError
----------------------------------------------------------------------
Ran 4 tests in 0.003s
FAILED (errors=1)
But we can easily modify our BasicDB.load method to handle such a case and return an
empty list of todo items:
class BasicDB:
    def __init__(self, path, _fileopener=open):
        self._path = path
        self._fileopener = _fileopener


---
**Page 99**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 99 ]
    def load(self):
        try:
            with self._fileopener(self._path, "r",
                                  encoding="utf-8") as f:
                txt = f.read()
            return eval(txt)
        except FileNotFoundError:
            return []
At this point, if we got it right, our unit tests should all pass:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 4 tests in 0.002s
OK
Given that we were looking for our next step a few minutes ago, we should probably head
back to our acceptance tests and check where we were. Running our acceptance tests again
will show that this time, we were able to start the application correctly (that is, it doesn't
crash anymore on missing files), but that on adding a new item and restarting the app, it
didn't persist the addition:
$ python -m unittest discover -k acceptance
.F
======================================================================
FAIL: test_persistence (tests.test_acceptance.TestTODOAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/test_acceptance.py", line 110,
in test_persistence
    "TODOs:\n"
AssertionError: 'TODOs:\n\n\n> ' != 'TODOs:\n1. buy milk\n\n> '
  TODOs:
-
+ 1. buy milk
  >
----------------------------------------------------------------------
Ran 2 tests in 1.006s
FAILED (failures=1)


---
**Page 100**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 100 ]
The buy milk item is not where we expected it to be after reloading the application, which
makes sense, as we never actually implemented any support for saving the current todo
items when we exit the application. So while we are probably able to load back a list of
items, we never save one.
This means we want to extend our TODOApp to save the current list of todo items before
exiting.
So let's add a test_save test to our tests/unit/tests_todoapp.py tests to make clear
what we want to achieve.
We just want the application to start with some entries and make sure that when it quits,
the app asks dbmanager to save them. This means that if there was any change made to our
list of TODOs, it gets recorded:
class TestTODOApp(unittest.TestCase):
    ...
    def test_save(self):
        dbmanager = Mock(
            load=Mock(return_value=["buy milk", "buy water"]),
            save=Mock()
        )
        app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                      dbmanager=dbmanager)
        app.run()
        dbmanager.save.assert_called_with(["buy milk", "buy water"])
This test will obviously fail because we haven't yet used the dbmanager from TODOApp to
save anything:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
test_save (tests.unit.test_todoapp.TestTODOApp) ... FAIL
======================================================================
FAIL: test_save (tests.unit.test_todoapp.TestTODOApp)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tddbook/03_tdd/02_codedesign/tests/unit/test_todoapp.py", line 39,
in test_save
    dbmanager.save.assert_called_with(["buy milk", "buy water"])


---
**Page 101**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 101 ]
  File "/usr/lib/python3.7/unittest/mock.py", line 864, in
assert_called_with
    raise AssertionError('Expected call: %s\nNot called' % (expected,))
AssertionError: Expected call: save(['buy milk', 'buy water'])
Not called
----------------------------------------------------------------------
Ran 5 tests in 0.003s
FAILED (failures=1)
So, let's go to our TODOApp.run method and extend it to call dbmanager.save() before
exiting:
class TODOApp:
    ...
    def run(self):
        if self._dbmanager is not None:
            self._entries = self._dbmanager.load()
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        if self._dbmanager is not None:
            self._dbmanager.save(self._entries)
        self._out("bye!\n")
That's all we need to make our test pass. Our TODOApp now takes care of saving the entries
and it's up to the provided dbmanager to do the right thing with them:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 5 tests in 0.002s
OK


---
**Page 102**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 102 ]
Are we done? Not yet – TODOApp is now doing its job, but a quick run of our acceptance test
will point out that dbmanager doesn't know what we are talking about:
$ python -m unittest discover -k acceptance
.Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "/tddbook/03_tdd/02_codedesign/src/todo/app.py", line 24, in run
    self._dbmanager.save(self._entries)
AttributeError: 'BasicDB' object has no attribute 'save'
Back to our tests/unit/test_basicdb.py file, we are going to add a test_save test to
confirm that BasicDB does actually want to save the list of provided items:
class TestBasicDB(unittest.TestCase):
    ...
    def test_save(self):
        mock_file = mock.MagicMock(write=mock.Mock())
        mock_file.__enter__.return_value = mock_file
        mock_opener = mock.Mock(return_value=mock_file)
        db = BasicDB(pathlib.Path("testdb"), _fileopener=mock_opener)
        loaded = db.save(["first", "second"])
        self.assertEqual(
            mock_opener.call_args[0][0:2],
            (pathlib.Path("testdb"), "w+")
        )
        mock_file.write.assert_called_with('["first", "second"]')
The test just verifies that when BasicDB.save is called, it opens the target file in write
mode and it tries to write into it the list of values.
To satisfy our test, we are going to implement a BasicDB.save method that converts the
list of entries to its string representation, replaces single quotes with double quotes so that
we save them in a format that is compatible with JSON, and saves it back:
class BasicDB:
    ...
    def save(self, values):
        with self._fileopener(self._path, "w+", encoding="utf-8") as f:
            f.write(repr(values).replace("'", '"'))


---
**Page 103**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 103 ]
If we did everything correctly, our unit tests should now be able to pass:
$ python -m unittest discover -k unit -v
test_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_missing_load (tests.unit.test_basicdb.TestBasicDB) ... ok
test_save (tests.unit.test_basicdb.TestBasicDB) ... ok
test_load (tests.unit.test_todoapp.TestTODOApp) ... ok
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.003s
OK
We implemented everything that we wanted and we provided the last piece that our
acceptance test was complaining about, which can be easily confirmed by going back to our
acceptance tests and verifying that the software is now completed:
$ python -m unittest discover -k acceptance
..
----------------------------------------------------------------------
Ran 2 tests in 1.006s
OK
Great! Our app is now fully functional.
We just want to tweak our src/todo/_main__.py file so that when we start the app from
the command line, we start it with dbmanager and thus with persistence enabled by
default:
from .app import TODOApp
from .db import BasicDB
TODOApp(dbmanager=BasicDB("todo.data")).run()
Starting the application, adding an entry, and then restarting it will now properly preserve
the entry across the two runs:
$ python -m todo
TODOs:
> add buy milk
TODOs:
1. buy milk


---
**Page 104**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 104 ]
> quit
bye!
$ python -m todo
TODOs:
1. buy milk
> quit
bye!
Before ending our day with a sense of satisfaction from our newly built application, we
want to make sure we remember to install the new release of our favorite Linux
distribution.
As we just made a great TODO application, let's add an entry to it:
$ python -m todo
TODOs:
1. buy milk
> add install "Focal Fossa"
TODOs:
1. buy milk
2. install "Focal Fossa"
> quit
bye!
Sadly, the morning after, we open our TODO application to look at what we have to do,
and surprise, surprise, we are welcomed by a major crash in our application:
$ python -m todo
Traceback (most recent call last):
  File "/usr/lib/python3.7/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/lib/python3.7/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/tddbook/03_tdd/02_codedesign/src/todo/__main__.py", line 4, in
<module>
    TODOApp(dbmanager=BasicDB("todo.data")).run()
  File "/tddbook/03_tdd/02_codedesign/src/todo/app.py", line 15, in run
    self._entries = self._dbmanager.load()
  File "/tddbook/03_tdd/02_codedesign/src/todo/db.py", line 12, in load
    return eval(txt)
  File "<string>", line 1
    ["buy milk", "install "Focal Fossa""]
                               ^
SyntaxError: invalid syntax


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


