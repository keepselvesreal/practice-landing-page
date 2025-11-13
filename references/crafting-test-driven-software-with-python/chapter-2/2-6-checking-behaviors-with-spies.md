# 2.6 Checking behaviors with spies (pp.44-49)

---
**Page 44**

Test Doubles with a Chat Application
Chapter 2
[ 44 ]
Let's check whether that's true by running our acceptance test:
$ python 03_chat_stubs.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_chat_stubs.py", line 10, in test_message_exchange
    user1.send_message("Hello World")
  File "03_chat_stubs.py", line 49, in send_message
    self.connection.broadcast(message)
AttributeError: 'ChatClient' object has no attribute 'connection'
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Not yet... We made the Connection object, but we clearly forgot to bind it to our
ChatClient.
So let's move forward by binding ChatClient with Connection and introducing spies as
a way to verify that the ChatClient is using the Connection the way we actually expect it
to.
Checking behaviors with spies
We know that ChatClient must use a connection to send and receive the messages. So the
next thing we have to do to make sure our test_message_exchange test passes is to make
sure that the connection exists and is used. But we don't want to establish a connection
every time a ChatClient is created, so the idea is to create a connection through a method
that lazily makes them when they're needed the first time.
We will call this method ChatClient._get_connection and we want to make sure that
ChatClient will actually use the connection provided by that method. To verify that
ChatClient uses the provided connection, we are going to set up a test with a spy, a kind
of dummy object that, instead of doing nothing, actually records how it was called (if it
was) and with which arguments.


---
**Page 45**

Test Doubles with a Chat Application
Chapter 2
[ 45 ]
As we did when setting up the stub, we are going to use unittest.mock.patch to replace
the ChatClient._get_connection method with a stub that, instead of returning the
connection, returns the spy. Then we are going to check through the spy that the
ChatClient.send_message method actually used the connection we returned to send the
message:
    def test_client_connection(self):
        client = ChatClient("User 1")
        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object(client, "_get_connection",
                                        return_value=connection_spy):
            client.send_message("Hello World")
        # assert that the spy was called with the
        # expected data to broadcast.
        connection_spy.broadcast.assert_called_with(("User 1:
                                                      Hello World"))
Now if we call our test, it's going to fail because we never made a
ChatClient._get_connection method and thus it can't be replaced with the stub:
$ python 04_chat_spies.py TestChatClient
E..
======================================================================
ERROR: test_client_connection (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "04_chat_spies.py", line 35, in test_client_connection
    return_value=connection_spy):
  File "/usr/lib/python3.7/unittest/mock.py", line 1319, in __enter__
    original, local = self.get_original()
  File "/usr/lib/python3.7/unittest/mock.py", line 1293, in get_original
    "%s does not have the attribute %r" % (target, name)
AttributeError: <__main__.ChatClient object at 0x7f962dd8d050> does not
have the attribute '_get_connection'
----------------------------------------------------------------------
Ran 3 tests in 0.001s
FAILED (errors=1)


---
**Page 46**

Test Doubles with a Chat Application
Chapter 2
[ 46 ]
So let's go to our ChatClient class and let's add the _get_connection method, which is
going to return a new Connection object against a predefined port where the server will 
listen locally (normally, we would make the port and host for a service configurable, but
given that it's just a simple chat application for our own use, we can take for granted that
the server will run on a known port and host):
class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message
    def _get_connection(self):
        return Connection(("localhost", 9090))
Great – so our test should be happy now! The stub can be put in place, so let's see what
happens when running our tests again:
$ python 04_chat_spies.py TestChatClient
E..
======================================================================
ERROR: test_client_connection (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "04_chat_spies.py", line 36, in test_client_connection
    client.send_message("Hello World")
  File "04_chat_spies.py", line 83, in send_message
    self.connection.broadcast(message)
AttributeError: 'ChatClient' object has no attribute 'connection'
----------------------------------------------------------------------
Ran 3 tests in 0.001s
FAILED (errors=1)
Okay, we made the _get_connection but the ChatClient never calls it... So the object is
still missing a connection attribute.
We know we want this attribute to lazily create the connection, so we are going to define a
property that calls _get_connection the first time it's accessed:
class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname


---
**Page 47**

Test Doubles with a Chat Application
Chapter 2
[ 47 ]
        self._connection = None
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection
    @connection.setter
    def connection(self, value):
        if self._connection is not None:
            self._connection.close()
        self._connection = value
    def _get_connection(self):
        return Connection(("localhost", 9090))
Now when ChatClient.connection is accessed, as ChatClient._connection will be
None, the ChatClient._get_connection method will be called so that a new connection
can be created.
All the pieces should be in place now! So let's see if our test finally passes:
$ python 04_chat_spies.py TestChatClient
F..
======================================================================
FAIL: test_client_connection (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "04_chat_spies.py", line 38, in test_client_connection
    assert connection_spy.broadcast.assert_called_with(("User 1: Hello
World"))
  File "/usr/lib/python3.7/unittest/mock.py", line 873, in
assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: broadcast('User 1: Hello World')
Actual call: broadcast('Hello World')
----------------------------------------------------------------------
Ran 3 tests in 0.001s
FAILED (failures=1)


---
**Page 48**

Test Doubles with a Chat Application
Chapter 2
[ 48 ]
Unexpectedly, our test failed. The good news is that the connection itself worked. The test
was able to put in place the stub, and the spy was used.
The bad news is that our test actually discovered a bug that our previous
TestChatClient.test_send_message test was unable to spot. In the current
implementation of ChatClient.send_message, we build the message with the name of
the user who wrote it, but we broadcast the one without a name. So none of the other users
reading the chat will ever know who wrote that message!
class ChatClient:
    ...
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message
What we want to do here is change the send_message method so that the message 
broadcast is the one with the name of the author, the sent_message variable, instead of
the message one:
class ChatClient:
    ...
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message
Now that we have fixed that bug, our test can finally pass and confirm that our
ChatClient has the connection in place and properly sends messages through it:
$ python 04_chat_spies.py TestChatClient
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s
OK
The next step, as usual, is to go back to our acceptance test and ask what's left to do:
$ python 04_chat_spies.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):


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


