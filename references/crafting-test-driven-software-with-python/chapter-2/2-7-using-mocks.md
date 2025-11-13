# 2.7 Using mocks (pp.49-51)

---
**Page 49**

Test Doubles with a Chat Application
Chapter 2
[ 49 ]
  File "04_chat_spies.py", line 10, in test_message_exchange
    user1.send_message("Hello World")
  File "04_chat_spies.py", line 58, in send_message
    self.connection.broadcast(sent_message)
  File "04_chat_spies.py", line 64, in connection
    self._connection = self._get_connection()
  File "04_chat_spies.py", line 74, in _get_connection
    return Connection(("localhost", 9090))
  File "04_chat_spies.py", line 82, in __init__
    self.connect()
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 532, in
connect
    conn = Client(self._address, authkey=self._authkey)
  File "/usr/lib/python3.7/multiprocessing/connection.py", line 492, in
Client
    c = SocketClient(address)
  File "/usr/lib/python3.7/multiprocessing/connection.py", line 619, in
SocketClient
    s.connect(address)
ConnectionRefusedError: [Errno 111] Connection refused
----------------------------------------------------------------------
Ran 1 test in 0.001s
FAILED (errors=1)
Our acceptance test proves that our client is trying to connect to the server as expected,
which is great!
The problem is that, as we already know, there is no such server. So our acceptance test
cannot pass as it can't connect to a server and verify that the client is actually able to send
and receive messages.
But before moving forward and looking at how to implement our server, let's introduce the
concept of mocks, which gather in themselves all the powers of the previously introduced
test doubles.
Using mocks
As you've probably noticed, when we use dummy objects, stubs, or spies, we always end
up working with the unittest.mock module. That's because mock objects could be seen
as dummy objects that provide some stubs mixed with spies.


---
**Page 50**

Test Doubles with a Chat Application
Chapter 2
[ 50 ]
Mocks are able to be passed around and they usually do nothing, behaving pretty much
like dummy objects.
If we had a read_file function accepting a file object with a read method, we could
provide a Mock instead of a real file; Mock.read will just do nothing:
>>> def read_file(f):
...     print("READING ALL FILE")
...     return f.read()
...
>>> from unittest.mock import Mock
>>> m = Mock()
>>> read_file(m)
READING ALL FILE
If instead of doing nothing, we want to make it act like a stub, we can provide a canned
response to have Mock.read return a predefined string:
>>> m.read.return_value = "Hello World"
>>> print(read_file(m))
Hello World
If we don't want to just fill in the place of other real objects by replacing them with
dummies and stubs, we can also use mocks to track what happened to them, so they are
able to behave like a spy too:
>>> m.read.call_count
2
But what makes them mocks is that they can test the behavior of software. Stubs, spies, and
dummies are all about state. They provide a state for software consumption when you are
injecting a known state into software or for test consumption when you are using a spy to
keep the state of calls.
Mocks are usually meant to keep track of behaviors. They usually crash when the software
hasn't done what you expected. So they are usually meant to assert that they were used in a
specific expected way, which confirms that the software behaved as we wished.
For example, we can check that the read method on the Mock object was actually called:
>>> m.read.assert_called_with()


---
**Page 51**

Test Doubles with a Chat Application
Chapter 2
[ 51 ]
If we wanted to verify that read_file was calling f.read() with a specific argument, we
could have asked the mock to verify that it was used. If the method wasn't called, the
assertion would have failed with an AssertionError:
>>> m.read.assert_called_with("some argument")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.7/unittest/mock.py", line 873, in
assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: read('some argument')
Actual call: read()
If it wasn't called due to a bug or incomplete implementation, the assertion would have
detected that and we could have addressed the behavior of read_file to make it work as
we wanted.
Now that we know about dummies, stubs, spies, and mocks, we know that there are tons of
ways to test our software without having to rely on complete and fully functional
components. And we know that our test suite has to be fast, easy to debug, and must
require minimum dependencies with minimum influence from the external system.
So a real working server would mean having to start a separate server process every time
we want to run our tests and would mean slowing down tests because they have to go
through a real network connection.
For the next step, instead of implementing a real server, we are going to introduce the
concept of fakes and try to get a fake server that makes our acceptance test pass.
Replacing dependencies with fakes
Fakes are replacements for real dependencies that are good enough to fake that they are the
real deal. Fakes are frequently involved in the goal of simplifying test suite dependencies or
improving the performance of a test suite. For example, if your software depends on a
third-party weather forecasting API available in the cloud, it's not very convenient to
perform a real network connection to the remote API server. The best-case scenario is it will
be very slow, and the worst-case scenario is you could get throttled or even banned for
doing too many API requests in too short a time, as your test suite could easily reach
hundreds or thousands of tests.
The most widespread kind of fakes are usually in-memory databases as they simplify the
need to set up and tear down a real database management system for the sole reason of
running your tests.


