# 2.5 Replacing components with stubs (pp.40-44)

---
**Page 40**

Test Doubles with a Chat Application
Chapter 2
[ 40 ]
AttributeError: ChatClient instance has no attribute 'connection'
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
We implemented the ChatClient.send_message method and it passes its test, but our
acceptance test is now reminding us that we still have to implement the Connection object
as we just used a double for it in the send_message test.
The connection object is the next thing we are going to implement, but the connection will
need to be able to reach a server that can route the messages to all connected clients, and
making our tests pass a DummyConnection won't be enough anymore. We will have to
actually see the messages and thus using stubs will be necessary.
Replacing components with stubs
Our connection object will be in charge of making our message available to all the other
clients and, probably in the near future, letting us know when there are new messages.
The first step to drive the development of our Connection object is to start building a
TestConnection test case and a test_broadcast test to make our expectations of the
implementation clear:
class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        c = Connection(("localhost", 9090))
        c.broadcast("some message")
        assert c.get_messages()[-1] == "some message"
Our test specifies that once we've sent a message in broadcast, the latest entry in the
messages visible in the chat should be our own message (as it was the last message sent).
Obviously, running our test now will fail because the Connection object doesn't exist at
all, so let's make one.
A possible idea for how to implement cross-client communication is to use a
multiprocessing.managers.SyncManager and store the messages in a list that is
accessible by all the clients that connect to it.


---
**Page 41**

Test Doubles with a Chat Application
Chapter 2
[ 41 ]
The only thing we will have to do is register a single Connection.get_messages
identifier in the manager. The purpose of that identifier will be to return the list of
messages that are currently in the chat so that ChatClient can read them or append new
messages:
from multiprocessing.managers import SyncManager
class Connection(SyncManager):
    def __init__(self, address):
        self.register("get_messages")
        super().__init__(address=address, authkey=b'mychatsecret')
        self.connect()
Then the Connection.broadcast method will be as simple as just getting the messages
through Connection.get_messages and appending a new message to them:
from multiprocessing.managers import SyncManager
class Connection(SyncManager):
    def __init__(self, address):
        self.register("get_messages")
        super().__init__(address=address, authkey=b'mychatsecret')
        self.connect()
    def broadcast(self, message):
        messages = self.get_messages()
        messages.append(message)
Now our connection object is done and it provides a broadcast method, so we can
verify that it does add a new message to our chat by rerunning our test:
$ python 03_chat_stubs.py TestConnection
E
======================================================================
ERROR: test_broadcast (__main__.TestConnection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_chat_stubs.py", line 33, in test_broadcast
    c = Connection(("localhost", 9090))
  File "03_chat_stubs.py", line 56, in __init__
    self.connect()
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 532, in
connect
    conn = Client(self._address, authkey=self._authkey)
  File "/usr/lib/python3.7/multiprocessing/connection.py", line 492, in
Client
    c = SocketClient(address)


---
**Page 42**

Test Doubles with a Chat Application
Chapter 2
[ 42 ]
  File "/usr/lib/python3.7/multiprocessing/connection.py", line 619, in
SocketClient
    s.connect(address)
ConnectionRefusedError: [Errno 111] Connection refused
----------------------------------------------------------------------
Ran 1 test in 0.003s
FAILED (errors=1)
Sadly, our test failed, because we still don't have a server, so the connection couldn't get
created because there is no server it could connect to. Until we have a server, we already
know we can replace our Connection.connect method with a dummy in our test and
retry:
class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        with unittest.mock.patch.object(Connection, "connect"):
            c = Connection(("localhost", 9090))
        c.broadcast("some message")
        assert c.get_messages()[-1] == "some message"
unittest.mock.patch.object is a convenience method that allows us to replace a
method or attribute of an object with a unittest.mock.Mock for the whole duration of the
code block within the context. So in this case, we disabled the Connection.connect
method so that the connection could be created without a server.
Okay, so now we expect our test to finally pass, right? Let's try to run it once more:
$ python 03_chat_stubs.py TestConnection
F
======================================================================
FAIL: test_broadcast (__main__.TestConnection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_chat_stubs.py", line 36, in test_broadcast
    c.broadcast("some message")
  File "03_chat_stubs.py", line 60, in broadcast
    messages = self.get_messages()
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 724, in temp
    token, exp = self._create(typeid, *args, **kwds)
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 606, in
_create
    assert self._state.value == State.STARTED, 'server not yet started'
AssertionError: server not yet started


---
**Page 43**

Test Doubles with a Chat Application
Chapter 2
[ 43 ]
----------------------------------------------------------------------
Ran 1 test in 0.001s
FAILED (failures=1)
Not really. The object was successfully created, but once we tried to get the chat messages
to append the new one, it failed, as there was no server we could connect to.
But we do really need the messages, otherwise, the whole test has no way to verify that the
message was added to the existing messages and thus sent. So what can we do?
Here is where stubs come in handy. Stubs provide canned answers, replacing those pieces
of the software with the ready-made state or answer that we could have got if it had run for
real. So we are going to replace Connection.get_messages with a stub that returns an 
empty list and see that everything works as we expected:
class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        with unittest.mock.patch.object(Connection, "connect"):
            c = Connection(("localhost", 9090))
        with unittest.mock.patch.object(c, "get_messages",
                                         return_value=[]):
            c.broadcast("some message")
            assert c.get_messages()[-1] == "some message"
You can now see that, after the first call to unittest.mock.patch.object, where we
replaced the connect method with a dummy one, we now have a second one. In this one,
we replace the get_messages method of the newly made Connection instance with one
that returns a canned response of an empty list, simulating this being the first message that
was sent to the chat.
Finally, running our tests again will confirm that the Connection.broadcast method is
doing what we expected:
$ python 03_chat_stubs.py TestConnection
.
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK
Okay, so now we have ChatClient and Connection tests passing, so we clearly did our
job, right?


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


