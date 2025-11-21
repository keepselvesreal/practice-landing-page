# 2.4 Using dummy objects (pp.38-40)

---
**Page 38**

Test Doubles with a Chat Application
Chapter 2
[ 38 ]
Our test failed again – it told us that our ChatClient.send_message method is now
there, and the test was able to call it, but it's not yet working.
This is because we actually went a bit further in having the client already send the
messages through the network before the need was exposed by our tests. But we already
knew that's what we actually wanted to do anyway, and it actually serves the purpose of
introducing our first test double: dummy objects.
Using dummy objects
A dummy is an object that does nothing. It just serves the purpose of being passed around
as an argument and not making the code crash because we lack an object. But its
implementation is totally empty; it does nothing.
In our chat application, we need a connection object to be able to send messages from one
client to the other. We have not yet implemented that connection object, and for now, we
are focused on having the ChatClient.send_message test pass, but how can we make it
pass if we don't yet have a working Connection object the client relies on?
That's where dummy objects come in handy. They replace other objects, faking that they
can do their job, but in reality, they do absolutely nothing.
A dummy object for our Connection class would currently look like this:
class _DummyConnection:
    def broadcast(*args, **kwargs):
        pass
In practice, it's an object that provides a broadcast method but does absolutely nothing.
Dummy objects are just fillers for the arguments of properties that another object needs.
They are frequently not even used at all and just provide a pass-through to satisfy some
required argument.
Now we can adapt our previous TestChatClient.test_send_message test to use a
dummy for the connection by setting client.connection to _DummyConnection. That
should make our test pass as we broke the dependency over a real connection:
class TestChatClient(unittest.TestCase):
    ...
    def test_send_message(self):
        client = ChatClient("User 1")
        client.connection = _DummyConnection()


---
**Page 39**

Test Doubles with a Chat Application
Chapter 2
[ 39 ]
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
Another convenient way to implement dummy objects is just to use the Python
unittest.mock module. In the Using mocks section, will see that, while the name is pretty
specific, the unittest.mock.Mock object is in practice able to serve all test doubles cases
introduced in this chapter. It just depends on which features we use and which we ignore.
So in our previous example, we can just replace our _DummyConnection
with unittest.mock.Mock and avoid having to implement a dedicated class at all:
import unittest.mock
class TestChatClient(unittest.TestCase):
    ...
    def test_send_message(self):
        client = ChatClient("User 1")
        client.connection = unittest.mock.Mock()
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
If we run our tests again for TestChatClient, we should see that we finally succeeded in
making them pass:
$ python 02_chat_dummy.py TestChatClient
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s
OK
Does that mean that our work is done? Not yet, because checking our acceptance test
(TestChatAcceptance) again will tell us that we are not yet there:
$ python 02_chat_dummy.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "02_chat_dummy.py", line 8, in test_message_exchange
    user1.send_message("Hello World")
  File "02_chat_dummy.py", line 39, in send_message
    self.connection.broadcast(message)


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


