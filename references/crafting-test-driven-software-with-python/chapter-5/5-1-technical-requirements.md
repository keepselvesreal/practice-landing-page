# 5.1 Technical requirements (pp.138-139)

---
**Page 138**

5
Introduction to PyTest
In the previous chapters, we saw how to approach test-driven development, how to create
a test suite with the unittest module, and how to organize it as it grows. While unittest
is a very good tool and is a reliable solution for most projects, it lacks some convenient
features that are available in more advanced testing frameworks.
PyTest is currently the most widespread testing framework in the Python community, and
it's mostly compatible with unittest. So it's easy to migrate from unittest to pytest if
you feel the need for the convenience that pytest provides.
In this chapter, we will cover the following topics:
Running tests with PyTest
Writing PyTest fixtures
Managing temporary data with tmp_path
Testing I/O with capsys
Running subsets of the test suite
Technical requirements
We need a working Python interpreter with the pytest framework installed. Pytest can be
installed with the following:
$ pip install pytest
The examples have been written on Python 3.7 and pytest 5.4.3 but should work on most
modern Python versions. You can find the code files present in this chapter on GitHub
at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-
Python/​tree/​main/​Chapter05.


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


