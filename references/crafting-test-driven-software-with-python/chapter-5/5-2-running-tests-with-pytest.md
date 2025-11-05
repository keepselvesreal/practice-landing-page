# 5.2 Running tests with PyTest (pp.139-142)

---
**Page 139**

Introduction to PyTest
Chapter 5
[ 139 ]
Running tests with PyTest
PyTest is mostly compatible with the unittest module (apart from support for subtests).
Test suites written with unittest can be directly run under pytest with no modification
usually. For example, our chat application test suite can be directly run under pytest by
simply invoking pytest within the project directory:
$ pytest -v
============ test session starts ============
platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /chatapp
collected 11 items
benchmarks/test_chat.py::BenchmarkChat::test_sending_messages PASSED [ 9%]
tests/e2e/test_chat.py::TestChatAcceptance::test_message_exchange PASSED [
18%]
tests/e2e/test_chat.py::TestChatAcceptance::test_smoke_sending_message
PASSED [ 27%]
tests/functional/test_chat.py::TestChatMessageExchange::test_exchange_with_
server PASSED [ 36%]
tests/functional/test_chat.py::TestChatMessageExchange::test_many_users
PASSED [ 45%]
tests/functional/test_chat.py::TestChatMessageExchange::test_multiple_reade
rs PASSED [ 54%]
tests/unit/test_client.py::TestChatClient::test_client_connection PASSED [
63%]
tests/unit/test_client.py::TestChatClient::test_client_fetch_messages
PASSED [ 72%]
tests/unit/test_client.py::TestChatClient::test_nickname PASSED [ 81%]
tests/unit/test_client.py::TestChatClient::test_send_message PASSED [ 90%]
tests/unit/test_connection.py::TestConnection::test_broadcast PASSED [100%]
============ 11 passed in 3.63s ============
The main difference is that pytest doesn't look for classes that inherit the
unittest.TestCase class, but instead looks for anything that has test in the name, be it a
module, a class, or a function. Anything named [Tt]est* is a test... but, if needed, it's
possible to change the discovery rules by having pytest.ini inside the project directory.
This means that even a simple function can be a test as long as it's named
test_something, and as it won't inherit from TestCase, there is no need to use the
custom self.assertEqual and the related method to get meaningful information on
failed assertions. Pytest will enhance the assert statement to report as much information
as available on the asserted expression.


---
**Page 140**

Introduction to PyTest
Chapter 5
[ 140 ]
For example, we could create a very simple test suite that only has a test_simple.py
module containing a test_something function. That would be all we need to start a test
suite:
def test_something():
    a = 5
    b = 10
    assert a + b == 11
Now, if we run pytest inside the same directory, it will properly find and run our test, and
the failed assertion will also give us hints on what went wrong by telling us that a + b is
15 and not 11:
$ pytest -v
======================= test session starts =======================
platform linux -- Python 3.7.3, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: ~/HandsOnTestDrivenDevelopmentPython/05_pytest
collected 1 item
test_simple.py::test_something FAILED [100%]
============================ FAILURES =============================
_________________________ test_something __________________________
    def test_something():
        a = 5
        b = 10
> assert a + b == 11
E assert 15 == 11
E +15
E -11
test_simple.py:4: AssertionError
===================== short test summary info =====================
FAILED test_simple.py::test_something - assert 15 == 11
======================== 1 failed in 0.22s ========================
We can also add more complex tests that are implemented as classes collecting multiple
tests, without having to inherit from the TestCase class as we did for unittest test suites:
class TestMultiple:
    def test_first(self):
        assert 5 == 5
    def test_second(self):
        assert 10 == 10


---
**Page 141**

Introduction to PyTest
Chapter 5
[ 141 ]
As for the previous case where we only had the test_something test function, if we run
pytest, it will find all three tests and it will run them:
$ pytest -v
...
collected 3 items
test_simple.py::test_something FAILED [ 33%]
test_simple.py::TestMultiple::test_first PASSED [ 66%]
test_simple.py::TestMultiple::test_second PASSED [100%]
...
As we know that test_something always fails, we can select which tests to run by using
the -k option, as we used to do for unittest. The option is, by the way, more powerful
than the one provided by unittest.
For example, it is possible to provide the -k option to restrict the tests to a subset of them
like we already used to do:
$ pytest -v -k first
...
collected 3 items / 2 deselected / 1 selected
test_simple.py::TestMultiple::test_first PASSED [100%]
...
It's also possible to use it to exclude some specific tests:
$ pytest -v -k "not something"
...
collected 3 items / 1 deselected / 2 selected
test_simple.py::TestMultiple::test_first PASSED [ 50%]
test_simple.py::TestMultiple::test_second PASSED [100%]
...
In the first case, we ran the test_first test, but in the second, we ran all tests except
for test_something. So you could view pytest as unittest on steroids. It provides the
same features you were used to with unittest, but frequently, they are enhanced to make
them more powerful, flexible, or convenient.
If one had to choose between the two, it'd probably be a matter of preference. But it's not
uncommon to see unittest used for projects that want to keep a more lightweight test
suite that is kept stable over the course of the years (unittest, like most modules of the
Python Standard Library guarantees very long-term compatibility) and pytest for projects
that have more complex test suites or needs.


---
**Page 142**

Introduction to PyTest
Chapter 5
[ 142 ]
Writing PyTest fixtures
The primary difference between unittest and PyTest lies in how they handle fixtures.
While unittest like fixtures (setUp, tearDown, setupClass, and so on) are still
supported through the TestCase class when using pytest, pytest tries to provide
further decoupling of tests from fixtures.
In pytest, a fixture can be declared using the pytest.fixture decorator. Any function
decorated with the decorator becomes a fixture:
@pytest.fixture
def greetings():
    print("HELLO!")
    yield
    print("GOODBYE")
The code of the test is executed where we see the yield statement. yield in this context
passes execution to the test itself. So this fixture would print "HELLO" before the test starts
and then "GOODBYE" when the test finishes.
To then bind a fixture to a test, the pytest.mark.usefixtures decorator is used. So, for
example, to use our new fixture with the existing TestMultiple.test_second test, we
would have to decorate that test using the name of our new fixture:
class TestMultiple:
    def test_first(self):
        assert 5 == 5
    @pytest.mark.usefixtures("greetings")
    def test_second(self):
        assert 10 == 10
The name of a fixture is inherited by the name of the function that implements it, so by
passing "greetings" to the usefixtures decorator, we end up using our own fixture:
$ pytest -v -k "usingfixtures and second" -s
...
collected 8 items / 7 deselected / 1 selected
test_usingfixtures.py::TestMultiple::test_second HELLO!
PASSED
GOODBYE
...


