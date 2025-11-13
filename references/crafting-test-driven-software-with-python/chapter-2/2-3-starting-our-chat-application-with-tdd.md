# 2.3 Starting our chat application with TDD (pp.33-38)

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


