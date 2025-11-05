# Chapter 2: Test Doubles with a Chat Application (pp.31-67)

---
**Page 31**

2
Test Doubles with a Chat
Application
We have seen how a test suite, to be reasonably reliable, should include various kinds of
tests that cover components at various levels. Usually, tests, in regard to how many
components they involve, are categorized into at least three kinds: unit, integration, and
end-to-end.
Test doubles ease the implementation of tests by breaking dependencies between
components and allowing us to simulate the behaviors we want.
In this chapter, we will look at the most common kinds of test doubles, what their goals are,
and how to use them in real code. By the end of this chapter, we will have covered how to
use all those test doubles and you will be able to leverage them for your own Python
projects.
By adding test doubles to your toolchain, you will be able to write faster tests, decouple the
components you want to test from the rest of the system, simulate behaviors that depend
on other components' state, and in general move your test suite development forward with
fewer blockers.
In this chapter, we will learn how to move forward, in the Test-Driven Development
(TDD) way, the development of an application that depends on other external
dependencies such as a database management system and networking, relying on test
doubles for the development process and replacing them in our inner test layers to ensure
fast and consistent execution of our tests.
In this chapter, we will cover the following topics:
Introducing test doubles
Starting our chat application with TDD
Using dummy objects
Replacing components with stubs


---
**Page 32**

Test Doubles with a Chat Application
Chapter 2
[ 32 ]
Checking behaviors with spies
Using mocks
Replacing dependencies with fakes
Understanding acceptance tests and doubles
Managing dependencies with dependency injection
Technical requirements
A working Python interpreter should be all that is needed.
The examples have been written on Python 3.7 but should work on most modern Python
versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter02.
Introducing test doubles
In test-driven development, the tests drive the development process and architecture. The
software design evolves as the software changes during the development of new tests, and
the architecture you end up with should be a consequence of the need to satisfy your tests.
Tests are thus the arbiter that decides the future of our software and declares that the
software is doing what it is designed for. There are specific kinds of tests that are explicitly
designed to tell us that the software is doing what it was requested: Acceptance and
Functional tests.
So, while there are two possible approaches to TDD, top-down and bottom-up (one starting
with higher-level tests first, and the other starting with unit tests first), the best way to
avoid going in the wrong direction is to always keep in mind your acceptance rules, and
the most effective way to do so is to write them down as tests.
But how can we write a test that depends on the whole software existing and working if we
haven't yet written the software at all? The key is test doubles: objects that are able to
replace missing, incomplete, or expensive parts of our code just for the purpose of testing.
A test double is an object that takes the place of another object, faking that it is actually able
to do the same things as the other object, while in reality, it does nothing.


---
**Page 33**

Test Doubles with a Chat Application
Chapter 2
[ 33 ]
But if we make our tests pass with test doubles, how do we avoid shipping software that is
just a bunch of fake entities? That's why it's important to have various layers of tests – the
more you move up through the layers, the fewer test doubles you should have, all the way
up to end-to-end tests, which should involve no test doubles at all.
Test-driven development also suggests that we should write the minimum amount of code
necessary to make a test pass and it's a very important rule because, otherwise, you could
easily end up writing code whose development has to be driven by other new tests.
That means that to have a fairly high-level test (such as an acceptance test) pass, we are
probably going to involve many test doubles at the beginning (as our software is still
empty). So when are we expected to replace those test doubles with real objects?
That's where Test-Driven Development by Example by Kent Beck suggests relying on a TODO
list. As you write your code, you should write down anything that you think you need to
improve/support/replace. And before moving forward to writing the next acceptance test,
the TODO list should be completed.
In your TODO list, you can record entries to replace the test doubles with real objects. As a
consequence, we are going to write tests that verify the behaviors of those real objects and,
subsequently, their implementation, finally replacing them with the real objects themselves
in our original acceptance test to confirm it still passes.
To showcase how test doubles can help us during TDD, we are going to build a chat
application by relying on the most common kind of test doubles.
Starting our chat application with TDD
When you start the development of a new feature, the first test you might want to write is
the primary acceptance test – the one that helps you define "this is what I want to achieve."
Acceptance tests expose the components we need to create and the behaviors they need to
have, allowing us to move forward by designing the development tests for those
components and thus writing down unit and integration tests.
In the case of the chat application, our acceptance test will probably be a test where one
user can send a message and another user can receive it:
import unittest
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("John Doe")
        user2 = ChatClient("Harry Potter")


---
**Page 34**

Test Doubles with a Chat Application
Chapter 2
[ 34 ]
        user1.send_message("Hello World")
        messages = user2.fetch_messages()
        assert messages == ["John Doe: Hello World"]
if __name__ == '__main__':
    unittest.main()
Our test makes clear that we want two ChatClient instances that exchange a message. The
first sends a new message and the second is able to fetch it and see it.
Now, we made our mind up about the fact that we want two chat clients to exist: one that
sends messages and another that can receive them. We will surely evolve this simple vision
of our application in the future, but so far it has helped us set some clear expectations.
The ChatClient class doesn't yet exist, by the way. We vaguely know that we want it to be
able to send messages and fetch messages, but we still lack tons of details about what it
should do and how it should do it. So the next step is to start clarifying what we want those
capabilities to look like.
If we run our acceptance test, by running the 01_chat_acceptance.py file where we
saved the previous test case, it will fail with an error:
$ python 01_chat_acceptance.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "01_chat_acceptance.py", line 5, in test_message_exchange
    user1 = ChatClient("John Doe")
NameError: global name 'ChatClient' is not defined
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
By complaining that ChatClient is not defined, it will point out that our next step should
probably be writing a client.


---
**Page 35**

Test Doubles with a Chat Application
Chapter 2
[ 35 ]
So we know that the first thing we have to start with is creating a ChatClient and, as we
want that client to be able to remember the nickname of the user, we need to ensure that it's
aware of the nickname of the user. So let's start by writing a development test to ensure that
ChatClient will able to do so:
class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")
        assert client.nickname == "User 1"
At this point, we already know that both our acceptance test and our development test will
fail, as we haven't yet written any implementation. But let's confirm our test suite does
what we expect:
$ python 01_chat_acceptance.py TestChatClient
E
======================================================================
ERROR: test_nickname (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "01_chat_acceptance.py", line 16, in test_nickname
    client = ChatClient("User 1")
NameError: global name 'ChatClient' is not defined
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Obviously, our test is failing with the fact that ChatClient doesn't even exist, so let's 
implement the ChatClient class itself and make it aware of the nickname used:
class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
Now, rerunning our test unit should be successful, as we created the ChatClient and we
made it able to keep the memory of the user's nickname that is connected to our chat
application:
$ python 01_dummy.py TestChatClient
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK


---
**Page 36**

Test Doubles with a Chat Application
Chapter 2
[ 36 ]
So our unit test now passes, and we can move forward. What needs to be done next? To
know that, we just have to go back and run our acceptance test again. Does it pass? Does it
need any other unit to be developed?
$ python 01_chat_acceptance.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "01_chat_acceptance.py", line 8, in test_message_exchange
    user1.send_message("Hello World")
AttributeError: ChatClient instance has no attribute 'send_message'
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Running our acceptance test again, it has now complained about the
ChatClient.send_message method, so now we know that we need to work on that unit
next. As is usually expected with a TDD approach, we can start the work with a unit test.
So let's extend our TestChatClient case with one additional test_send_message test:
class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")
        assert client.nickname == "User 1"
    def test_send_message(self):
        client = ChatClient("User 1")
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
The new test_send_message test creates a client for User 1 and then sends a message to
the chat from that user, verifying that the outgoing message was actually submitted as a
message sent by that user.
Going back to our shell and rerunning our tests for the ChatClient component will tell us
that we now have to write that method to satisfy the test:
$ python 01_chat_acceptance.py TestChatClient
.E
======================================================================
ERROR: test_send_message (__main__.TestChatClient)


---
**Page 37**

Test Doubles with a Chat Application
Chapter 2
[ 37 ]
----------------------------------------------------------------------
Traceback (most recent call last):
  File "01_chat_acceptance.py", line 22, in test_send_message
    sent_message = client.send_message("Hello World")
AttributeError: ChatClient instance has no attribute 'send_message'
----------------------------------------------------------------------
Ran 2 tests in 0.000s
FAILED (errors=1)
So let's move back to development again and add the send_message method to our
component. We already decided that it has to accept the message, prefix it with the sender's
nickname, and probably send it to all the other users:
class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message
Let's rerun our test case for the component to confirm that we now satisfy it:
$ python 01_chat_acceptance.py TestChatClient
.E
======================================================================
ERROR: test_send_message (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "01_chat_acceptance.py", line 22, in test_send_message
    sent_message = client.send_message("Hello World")
  File "01_chat_acceptance.py", line 32, in send_message
    self.connection.broadcast(message)
AttributeError: ChatClient instance has no attribute 'connection'
----------------------------------------------------------------------
Ran 2 tests in 0.000s
FAILED (errors=1)


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


---
**Page 52**

Test Doubles with a Chat Application
Chapter 2
[ 52 ]
In our case, we don't want to have the need to start a chat server every time we want to run
the test suite of our chat application, so we are going to provide a fake server and fake
connection that will replace the real networking-based connection.
Now that we have our TestConnection case, which verifies that the connection does what
we want, how can we verify that it actually works when there is a server on the other side?
We can look at how the SyncManager server works and provide a fake replacement simple
enough to understand the basic protocol and provide the answers. Thankfully, the
SyncManager protocol is very simple. It just receives commands with a set of arguments
and responds with a tuple, ("RESPONSE_TYPE", RESPONSE), where RESPONSE_TYPE
states whether the response is the returned value for that command or an error.
So we can make a FakeServer that provides a FakeServer.send method that will trap
the commands that the client is requesting and a FakeServer.recv method that will send
back the response to the client:
class FakeServer:
    def __init__(self):
        self.last_command = None
        self.last_args = None
        self.messages = []
    def __call__(self, *args, **kwargs):
        # Make the SyncManager think that a new connection was created.
        return self
    def send(self, data):
        # Track any command that was sent to the server.
        callid, command, args, kwargs = data
        self.last_command = command
        self.last_args = args
    def recv(self, *args, **kwargs):
        # For now we don't support any command, so just error.
        return "#ERROR", ValueError("%s - %r" % (
            self.last_command,self.last_args)
        )
    def close(self):
        pass
The very first basic implementation of our fake server is only going to respond to any
command with an error, so we can track the commands that the client is trying to send to
us.


---
**Page 53**

Test Doubles with a Chat Application
Chapter 2
[ 53 ]
To test our connection with a server, we are going to add a new
test_exchange_with_server test to the TestConnection test case, which will use the
provided FakeServer to link two connections together:
class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        ...
    def test_exchange_with_server(self):
         with unittest.mock.patch(
             "multiprocessing.managers.listener_client",
             new={"pickle": (None, FakeServer())}
         ):
            c1 = Connection(("localhost", 9090))
            c2 = Connection(("localhost", 9090))
            c1.broadcast("connected message")
            assert c2.get_messages()[-1] == "connected message"
Our test requires some magic through unittest.mock.patch to replace the standard
implementation of the server/client communication channel in
multiprocessing.managers with our own custom FakeServer. In practice, what we are
doing is replacing the "pickle" based communication channel with our own for the duration
of the test.
Now if we run our test, we should see that our fake server is in place and we should be able
to start tracking which commands are exchanged:
$ python 05_chat_fakes.py TestConnection
.E
======================================================================
ERROR: test_exchange_with_server (__main__.TestConnection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "05_chat_fakes.py", line 56, in test_exchange_with_server
    c1 = Connection(("localhost", 9090))
  File "05_chat_fakes.py", line 100, in __init__
    self.connect()
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 533, in
connect
    dispatch(conn, None, 'dummy')
  File "/usr/lib/python3.7/multiprocessing/managers.py", line 82, in
dispatch
    raise convert_to_error(kind, result)
ValueError: dummy - ()
----------------------------------------------------------------------


---
**Page 54**

Test Doubles with a Chat Application
Chapter 2
[ 54 ]
Ran 2 tests in 0.001s
FAILED (errors=1)
Our test crashed due to an unrecognized 'dummy' command (as we currently recognize no
commands) but it proved that our fake server is in place and being used by our
Connection object.
At this point, we can provide support for the dummy command (which is just used to
establish the connection) and see what happens:
class FakeServer:
    ...
    def recv(self, *args, **kwargs):
        if self.last_command == "dummy":
            return "#RETURN", None
        else:
            return "#ERROR", ValueError("%s - %r" % (
                self.last_command,self.last_args)
            )
Running again, the TestConnection test suite will invoke the next command (after the
"dummy" one that we just implemented) and thus will complain about the next missing
command:
$ python 05_chat_fakes.py TestConnection
...
ValueError: create - ('get_messages',)
By rerunning our test over and over until it stops crashing, we can spot all the commands
that our FakeServer has to support in the FakeServe.recv method, and one by one, we
can implement enough commands to have a fairly complete implementation of our
FakeServer:
class FakeServer:
    ...
    def recv(self, *args, **kwargs):
        if self.last_command == "dummy":
            return "#RETURN", None
        elif self.last_command == "create":
            return "#RETURN", ("fakeid", tuple())
        elif self.last_command == "append":
            self.messages.append(self.last_args[0])
            return "#RETURN", None
        elif self.last_command == "__getitem__":


---
**Page 55**

Test Doubles with a Chat Application
Chapter 2
[ 55 ]
            return "#RETURN", self.messages[self.last_args[0]]
        elif self.last_command in ("incref", "decref",
                                   "accept_connection"):
            return "#RETURN", None
        else:
            return "#ERROR", ValueError("%s - %r" % (
                self.last_command,self.last_args)
            )
At this point, our TestConnection should be able to pass using our fake server to
establish the link between the two Connection objects:
$ python 05_chat_fakes.py TestConnection
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s
OK
Our FakeServer was able to confirm that the two Connection objects are able to talk to
each other and see the messages that the other one has broadcast. And we were able to do
so without the need to actually start a server instance, listen on the network for the chat
connections, and handle that.
While fakes are usually very convenient, the effort required to implement them is
frequently pretty high. To be usable, a fake must reproduce a major chunk of the
functionalities that the real dependency provided, and as we saw, implementing a fake
might involve having to reverse engineer how the piece of software we are trying to replace
works.
Luckily, for most widespread needs, you will find fake implementations of SQL servers,
MongoDB, S3, and so on, already available as libraries you can install.
While the fake approach worked well, the worst part of our fake usage is probably how we
had to patch the multiprocessing module to put it in place.
This is a problem caused by the fact that our Connection object, being based on
SyncManager, doesn't provide proper support for dependency injection, which would
have allowed us to inject our own communication channel in a proper way instead of
having to patch the "pickle" based one.
But before moving on to see how we can handle the injection of dependencies, let's finish
our chat application and make our acceptance test pass.


---
**Page 56**

Test Doubles with a Chat Application
Chapter 2
[ 56 ]
Understanding acceptance tests and
doubles
We saw our Connection object works with the FakeServer but does our acceptance test
finally pass now? Not yet. We still have to provide a server there (fake or not) and we still
have to finish the implementation of the client.
Acceptance tests are meant to verify that the software really does what we wanted once it's
in the hands of our users. For this reason, it's usually a good idea to limit the usage of test
doubles in the context of acceptance tests. They should work as much as possible by
reproducing the real usage of the software.
While mocks, stubs, dummies, and so on are rarely seen in acceptance tests, it's pretty
common to see fakes in that context too. As fakes are supposed to mimic the behavior of the
real service they replace, the software should notice no difference. But if you used fakes in
your acceptance tests, it's a good idea to introduce a set of system tests that verify the
software on the real services it depends on (maybe only executed at release time due to
their cost).
In our case, we want our acceptance test to work with a real server, thus we are going to
tweak it a little bit to start the server and connect the clients to the newly started server. As
our server is implemented on top of a SyncManager, like all SyncManagers it can be
started and stopped by using it as a context manager in a with statement.
When we enter the with new_chat_server() context, the server will be started, and once
we exit it, the server will be stopped:
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        with new_chat_server():
            user1 = ChatClient("John Doe")
            user2 = ChatClient("Harry Potter")
            user1.send_message("Hello World")
            messages = user2.fetch_messages()
            assert messages == ["John Doe: Hello World"]
Obviously, running the test will fail because we have not yet made the new_chat_server
function that is supposed to return the server in use by the test.


---
**Page 57**

Test Doubles with a Chat Application
Chapter 2
[ 57 ]
Our server will be just a SyncManager subclass that provides the list of messages (through
the _srv_get_messages function) so that the clients can access them:
_messages = []
def _srv_get_messages():
    return _messages
class _ChatServerManager(SyncManager):
    pass
_ChatServerManager.register("get_messages",
                            callable=_srv_get_messages,
                            proxytype=ListProxy)
def new_chat_server():
    return _ChatServerManager(("", 9090), authkey=b'mychatsecret')
Now that we've created our new_chat_server, which can be used to start the server, our
next step is, as usual, to verify that our tests do pass to see what's the next step:
$ python 06_acceptance_tests.py TestChatAcceptance
E
======================================================================
ERROR: test_message_exchange (__main__.TestChatAcceptance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "06_dependency_injection.py", line 12, in test_message_exchange
    messages = user2.fetch_messages()
AttributeError: 'ChatClient' object has no attribute 'fetch_messages'
----------------------------------------------------------------------
Ran 1 test in 0.011s
FAILED (errors=1)
In this case, the test doesn't yet pass because we forgot to implement the last piece of our
client: the part related to fetching the messages. So let's add that new fetch_messages
method to our client and see if things work as we want.
As usual, we should start with a test for the ChatClient.send_message unit, so that we
can verify that our implementation does what we expect:
class TestChatClient(unittest.TestCase):
    ...
    def test_client_fetch_messages(self):
        client = ChatClient("User 1")
        client.connection = unittest.mock.Mock()
        client.connection.get_messages.return_value = ["message1",


---
**Page 58**

Test Doubles with a Chat Application
Chapter 2
[ 58 ]
                                                       "message2"]
        starting_messages = client.fetch_messages()
        client.connection.get_messages().append("message3")
        new_messages = client.fetch_messages()
        assert starting_messages == ["message1", "message2"]
        assert new_messages == ["message3"]
As our ChatClient.fetch_messages method doesn't yet exist, our test unit will
immediately fail:
$ python 06_acceptance_tests.py TestChatClient
.E..
======================================================================
ERROR: test_client_fetch_messages (__main__.TestChatClient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "06_dependency_injection.py", line 46, in test_client_fetch_messages
    starting_messages = client.fetch_messages()
AttributeError: 'ChatClient' object has no attribute 'fetch_messages'
----------------------------------------------------------------------
Ran 4 tests in 0.001s
FAILED (errors=1)
So, what we can do is go back to ChatClient and implement the fetch_messages
method in a way that satisfies our test:
class ChatClient:
    def __init__(self, nickname):
        self.nickname = nickname
        self._connection = None
        self._last_msg_idx = 0
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message
    def fetch_messages(self):
        messages = list(self.connection.get_messages())
        new_messages = messages[self._last_msg_idx:]
        self._last_msg_idx = len(messages)
        return new_messages


---
**Page 59**

Test Doubles with a Chat Application
Chapter 2
[ 59 ]
The new ChatClient.fetch_messages method will fetch the messages stored by the
server and will return any new ones since the last time they were checked.
If our implementation is correct, running the test again will make it pass and will confirm
that our method does what we wanted it to do:
$ python 06_acceptance_tests.py TestChatClient
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s
OK
Also, as this was our last missing piece, the acceptance test should now pass, confirming
that our chat application does work as we wanted:
$ python 06_acceptance_tests.py TestChatAcceptance
.
----------------------------------------------------------------------
Ran 1 test in 0.016s
OK
Hurray! We can finally declare victory. Our application works with the real client and real
server. They are able to connect and talk to each other, which proves we wrote the software
we wanted to write.
But our ChatClient tests have fairly complex code that has to rely on mock.patch to
replace pieces of it and we even had to implement a property setter for the connection for
the sole purpose of making it possible to replace it with a testing double.
Even though we achieved our goal, there should be a better way to enable test doubles in
code than spreading mock.patch everywhere.
Replacing components of a system on demand is what dependency injection was made
for, so let's see if it can help us to switch between using fakes and real services in our test
suite.


---
**Page 60**

Test Doubles with a Chat Application
Chapter 2
[ 60 ]
Managing dependencies with dependency
injection
Our ChatClient machinery to connect to a server is rather more complex than necessary.
The ChatClient.get_connection and ChatClient.connection property setters are
there mostly to allow us to easily replace with mocks the connections that our client sets up.
This is because ChatClient has a dependency, a dependency on the Connection object,
and it tries to satisfy that dependency all by itself. It's like when you are hungry... You
depend on food to solve your need, so you go to the fridge, take some ingredients, turn on
the oven, and cook a meal yourself. Then you can eat. Or... you can call a restaurant and
order a meal.
Dependency injection gives you a way to take the restaurant path. If your ChatClient
needs a connection, instead of trying to get a connection itself, it can ask for a connection
and someone else will take care of providing it.
In most dependency injection systems, there is an injector that will take care of getting the
right object and providing it to the client. The client typically doesn't even have to know
about the injector. This usually involves fairly advanced frameworks that provide a services
registry and allow clients to register for those services, but there is a very simple form of
dependency injection that works very well and can be immediately achieved without any
external dependency or framework: construction injection.
Construction injection means that the service your code depends on is provided as a
parameter when building the class that depends on it.
In our case, we could easily refactor the ChatClient to accept a connection_provider
argument, which would allow us to simplify our ChatClient implementation and get rid
of entire parts of it:
class ChatClient:
    def __init__(self, nickname, connection_provider=Connection):
        self.nickname = nickname
        self._connection = None
        self._connection_provider = connection_provider
        self._last_msg_idx = 0
    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message


---
**Page 61**

Test Doubles with a Chat Application
Chapter 2
[ 61 ]
    def fetch_messages(self):
        messages = list(self.connection.get_messages())
        new_messages = messages[self._last_msg_idx:]
        self._last_msg_idx = len(messages)
        return new_messages
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._connection_provider(("localhost",
                                                          9090))
        return self._connection
We got rid of ChatClient.get_connection and we got rid of the connection
@property.setter but we haven't lost a single functionality, nor have we added any
additional complexity. In most cases, the ChatClient can be used exactly like before and it
will take care of using the right Connection by default.
But for the cases where we want to do something different, we can inject other kinds of
connections.
For example, in our TestChatClient.test_client_connection test, we can remove a
fairly hard-to-read mock.patch that was in place to set up a spy:
class TestChatClient(unittest.TestCase):
    def test_client_connection(self):
        client = ChatClient("User 1")
        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object
          (client, "_get_connection",return_value=connection_spy):
            client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1:
                                                     Hello World"))


---
**Page 62**

Test Doubles with a Chat Application
Chapter 2
[ 62 ]
Instead of having to patch the implementation of ChatClient, we can just provide the spy
to the ChatClient and have it use it:
    def test_client_connection(self):
        connection_spy = unittest.mock.MagicMock()
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection_spy)
        client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1:
                                                     Hello World"))
The code is far easier to follow and understand and doesn't rely on magic such as patching
objects at runtime.
In fact, our whole TestChatClient can be made simpler by using dependency injection
instead of patching:
class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")
        assert client.nickname == "User 1"
    def test_send_message(self):
        client = ChatClient("User 1",
                            connection_provider=unittest.mock.Mock())
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
    def test_client_connection(self):
        connection_spy = unittest.mock.MagicMock()
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection_spy)
        client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1: Hello
                                                     World"))
    def test_client_fetch_messages(self):
        connection = unittest.mock.Mock()
        connection.get_messages.return_value = ["message1", "message2"]
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection)


---
**Page 63**

Test Doubles with a Chat Application
Chapter 2
[ 63 ]
        starting_messages = client.fetch_messages()
        client.connection.get_messages().append("message3")
        new_messages = client.fetch_messages()
        assert starting_messages == ["message1", "message2"]
        assert new_messages == ["message3"]
In all cases where we had fairly hard-to-read uses of mock.patch, we have now replaced
them with an explicitly provided connection_provider when the ChatClient is
created.
So dependency injection can make your life easier when testing, but actually also makes
your implementation far more flexible.
Suppose that we want to have our chat app working on something different than
SyncManagers; now it's a matter of just passing a different kind of
connection_provider to our clients.
Whenever your classes depend on other objects that they are going to build themselves, it's
usually a good idea to question whether that's a place for dependency injection and
whether those services could be injected from outside instead of being built within the class
itself.
Using dependency injection frameworks
In Python, there are many frameworks for dependency injection, and it's an easy enough
technique to implement yourself that you will find various variations of it in many
frameworks. What dependency injection frameworks will do for you is wire the objects
together.
In our previous dependency injection paragraph, we explicitly provided the dependencies
every time we wanted to create a new object (apart from the default dependency, which
was provided for us, being the default argument). A dependency injection framework
would instead automatically detect for us that ChatClient needs a Connection and it
would give the connection to the ChatClient.
One of the easiest-to-use dependency injection frameworks for Python is Pinject from
Google. It comes from the great experience Google teams have with dependency injection
frameworks, which is clear if you look at some of their most famous frameworks, such as
Angular.


---
**Page 64**

Test Doubles with a Chat Application
Chapter 2
[ 64 ]
Pinject manages dependencies in a very simple and easy to understand way, based on
initializer argument names and class names.
Suppose that, like before, we had our two ChatClient and Connection classes... but in
this case, our ChatClient is just going to print which Connection it's going to use, as our
sole purpose is to showcase how Pinject can handle dependency injection for us:
class ChatClient:
    def __init__(self, connection):
        print(self, "GOT", connection)
class Connection:
    pass
Then we can use pinject to create a graph of the dependencies of our objects:
import pinject
injector = pinject.new_object_graph()
Once pinject is aware of the dependencies of our objects (which by default are built by
scanning all classes in all imported modules; you can also pass your classes explicitly
through a classes= argument), we can ask pinject to give us an instance for any class
it's aware of, resolving all class dependencies for us:
>>> cli = injector.provide(ChatClient)
<ChatClient object at 0x7fad51469610> GOT <Connection object at
0x7fad51469bd0>
What happened is that pinject detected that a Connection class existed and when we
requested a ChatClient, it saw that it depended on a Connection argument. At that
point, pinject automatically made a connection for us and provided it to the client.
What if we wanted to provide a fake Connection object for our tests? Pinject supports
providing custom binding specifications, so telling it explicitly which class solves a specific
dependency.
So if we had a FakeConnection object, we could create a pinject.BindingSpec to tell
pinject that to satisfy the "connection" dependency, it has to use the fake one:
class FakeConnection:
    pass
class FakedBindingSpec(pinject.BindingSpec):
    def provide_connection(self):
        return FakeConnection()


---
**Page 65**

Test Doubles with a Chat Application
Chapter 2
[ 65 ]
faked_injector = pinject.new_object_graph(binding_specs=[
    FakedBindingSpec()
])
At this point, if we tried to create a ChatClient through the faked_injector, we would
get back a ChatClient that uses a fake connection:
>>> cli = faked_injector.provide(ChatClient)
<ChatClient object at 0x7fad513ce350> GOT <FakeConnection object at
0x7fad513d6f90>
It must be noted that, by default, Pinjector remembers the instances it made, so if we
requested a new ChatClient, it would get the same exact connection object. That is
frequently convenient when you are building a full piece of software and you want to
replace whole components. If you wanted to replace your data abstraction layer to use a
fake database, you would probably want to get the same data abstraction layer from
everywhere so that all components see the same data.
This means that creating a new ChatClient will give us a different ChatClient but with
the same underlying Connection:
>>> cli = faked_injector.provide(ChatClient)
<ChatClient object at 0x7f9878aeb810> GOT <Connection object at
0x7f9878a58f50>
>>> cli2 = faked_injector.provide(ChatClient)
<ChatClient object at 0x7f9878a55fd0> GOT <Connection object at
0x7f9878a58f50>
In the case of our clients, we probably want each of them to have a different connection to
the server. To do so, we can use the BindingSpec and tell pinject that our returned
dependency is a prototype and not a singleton. This way, pinject won't cache the provided
dependency and will always return a new one:
class PrototypeBindingSpec(pinject.BindingSpec):
    @pinject.provides(in_scope=pinject.PROTOTYPE)
    def provide_connection(self):
        return Connection()
proto_injector = pinject.new_object_graph(binding_specs=[
    PrototypeBindingSpec()
])


---
**Page 66**

Test Doubles with a Chat Application
Chapter 2
[ 66 ]
If we were to make a ChatClient with the proto_inject, we would now see that each
client has its own Connection object:
>>> cli = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060e50> GOT <Connection object at
0x7fadab013910>
>>> cli2 = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060f10> GOT <Connection object at
0x7fadab013850>
So, dependency injection frameworks can solve many needs for you. Whether you need to
use one or not depends mostly on how complex the network of dependencies in your
software is, but having one around can usually give you a quick way to break dependencies
between your components when you need to.
Summary
Dependencies between the components that you have to test can make your life hard as a
developer. To test anything more complex than a simple utility function, you might end up
having to cope with tens of dependencies and their state.
This is why the idea of being able to provide doubles for testing in place of the real
components was quickly born once the idea of automated tests became reality. Being able
to replace the components the unit you are testing depends on with fakes, dummies, stubs,
and mocks can make your life a lot easier and keep your test suite fast and easy to maintain.
The fact that any software is, in reality, a complex network of dependencies is the reason
why many people advocate that integration tests are the most realistic and reliable form of
testing, but managing that complex network can be hard and that's where dependency
injection and dependency injection frameworks can make your life far easier.
Now that we know how to write automatic test suites and we know how to use test
doubles to verify our components in isolation and spy their state and behavior, we have all
the tools that we need to dive into test-driven development in the next chapter and see how
to write software in the TDD way.


---
**Page 67**

3
Test-Driven Development while
Creating a TODO List
No programmer ever releases a software without having tested it – even for the most basic
proof of concept and rough hack, the developer will run it once to see that it at least starts
and resembles what they had in mind.
But to test, as a verb, usually ends up meaning clicking buttons here and there to get a
vague sense of confidence that the software does what we intended. This is different from
test as a noun, which means a set of written-out checks that our software must pass to
confirm it does what we wanted.
Apart from being more reliable, written-out checks force us to think about what the code
must do. They force us to get into the details and think beforehand about what we want to
build. Otherwise, we would just jump to building without thinking about what we are
building. And trying to ensure that what gets built is, in every single detail, the right thing
through a written specification is quickly going to turn into writing the software itself, just
in plain English.
The problem is that the more hurried, stressed, and overwhelmed developers are, the less
they test. Tests are the first thing that get skipped when things go wrong, and by doing so
things suddenly get even worse, as tests are what avoid errors and failures, and more errors
and failures mean more stress and rushing through the code to fix them, making the whole
process a loop that gets worse and worse.
Test-Driven Development (TDD) tries to solve this problem by engendering a set of
practices where tests become a fundamental step of your daily routine. To write more code
you must write tests, and as you get used to TDD and it becomes natural, you will quickly
notice that it gets hard to even think about how to get started if not by writing a test.
That's why in this chapter, we will cover how TDD can fit into the software development
routine and how to leverage it to keep problems under control at times of high stress.


