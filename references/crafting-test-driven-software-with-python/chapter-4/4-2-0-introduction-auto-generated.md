# 4.2.0 Introduction [auto-generated] (pp.115-122)

---
**Page 115**

Scaling the Test Suite
Chapter 4
[ 115 ]
Scaling tests
When we started our Chat application in Chapter 2, Test Doubles with a Chat Application, the
whole code base was contained in a single Python module. This module mixed both the
application itself, the test suite, and the fakes that we needed for the test suite.
While that process fits well for the experimentation and hacking phase, it's not convenient
for the long term. As we already saw in Chapter 3, Test-Driven Development while Creating a
TODO List, it's possible to split tests into multiple files and directories and keep them
separated from our application code.
As our project grows, the first step is to split our test suite from our code base. We are going
to use the src directory for the code base and the tests directory for the test suite. The
src directory in this case will contain the chat package, which contains the modules for
the client and server code:
.
├── src
│   ├── chat
│   │   ├── client.py
│   │   ├── __init__.py
│   │   └── server.py
│   └── setup.py
The src/chat/client.py file will contain the previous Connection and ChatClient
classes, while in src/chat/server.py we are going to put the new_chat_server
function.
We also provide a very minimal src/setup.py to allow installation of the chat package:
from setuptools import setup
setup(name='chat', packages=['chat'])
Now that we can install the chat package through pip install -e ./src and then use
any class within it through import chat, our tests can be moved anywhere; they no longer
need to be in the same directory of the files they need to test. 


---
**Page 116**

Scaling the Test Suite
Chapter 4
[ 116 ]
Thus we can create a tests directory and gather all our tests there. As we had three
different test classes (TestChatAcceptance, TestChatClient, and TestConnection),
we are going to split our tests into three dedicated files. This way, while we work, we can
run only tests relevant to the part we are modifying:
└── tests
    ├── __init__.py
    ├── test_chat.py
    ├── test_client.py
    └── test_connection.py
The only required changes to the tests we made in Chapter 2, Test Doubles with a Chat
Application, are to make sure that we add proper imports to get our classes (for
example, from chat.client import ChatClient). Once those are in place, our test
suite should be able to run exactly as it used to:
$ python -m unittest discover -v
test_message_exchange (tests.test_chat.TestChatAcceptance) ... ok
test_client_connection (tests.test_client.TestChatClient) ... ok
test_client_fetch_messages (tests.test_client.TestChatClient) ... ok
test_nickname (tests.test_client.TestChatClient) ... ok
test_send_message (tests.test_client.TestChatClient) ... ok
test_broadcast (tests.test_connection.TestConnection) ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.607s
OK
In a Test-Driven Development (TDD) approach, the test suite is something we will be able
to run frequently and quickly to verify the work we are doing, but in a real-world
application, test suites tend to become big and slow and can take minutes or hours to run.
For example, we might decide to grow our test suite further. Right now, we only have a test
to verify that two users can exchange a message, but we have not verified that when
multiple users are involved, we still see messages from all of them, and that each connected
user sees the same exact messages.
To do so, we can add a new TestChatMultiUser test case to
our tests/test_chat.py tests to verify that we can see the messages sent by all users
connected to the chat:
class TestChatMultiUser(unittest.TestCase):
    def test_many_users(self):
        with new_chat_server() as srv:
            firstUser = ChatClient("John Doe")


---
**Page 117**

Scaling the Test Suite
Chapter 4
[ 117 ]
            for uid in range(5):
                moreuser = ChatClient(f"User {uid}")
                moreuser.send_message("Hello!")
            messages = firstUser.fetch_messages()
            assert len(messages) == 5
The test_many_users test connects to the chat as firstUser and then adds five more
users to the chat and sends a new message from each of them. At the end of the
test, firstUser should be able to see all five messages sent by the other users.
To go further, we could also add a test_multiple_readers test that verifies that all users
in the chat see the same exact messages:
   def test_multiple_readers(self):
        with new_chat_server() as srv:
            user1 = ChatClient("John Doe")
            user2 = ChatClient("User 2")
            user3 = ChatClient("User 3")
            user1.send_message("Hi all")
            user2.send_message("Hello World")
            user3.send_message("Hi")
            user1_messages = user1.fetch_messages()
            user2_messages = user2.fetch_messages()
            self.assertEqual(user1_messages, user2_messages)
In this case, we have three users joining the chat, each of them sending a message, and then
we verified that both user1 and user2 see the same exact messages.
Through these two tests, we confirmed that our chat works as expected even when multiple
users are inside the chat. If we receive messages from different users, we will see all
messages, and all users will see the same exact messages. The side effect of the additional
confidence that we now have in our chat is that our test suite has become far slower:
$ python -m unittest discover -v -k e2e -k unit
test_message_exchange (tests.test_chat.TestChatAcceptance) ... ok
test_many_users (tests.test_chat.TestChatMultiUser) ... ok
test_multiple_readers (tests.test_chat.TestChatMultiUser) ... ok
test_client_connection (tests.test_client.TestChatClient) ... ok
test_client_fetch_messages (tests.test_client.TestChatClient) ... ok
test_nickname (tests.test_client.TestChatClient) ... ok
test_send_message (tests.test_client.TestChatClient) ... ok
test_broadcast (tests.test_connection.TestConnection) ... ok
----------------------------------------------------------------------


---
**Page 118**

Scaling the Test Suite
Chapter 4
[ 118 ]
Ran 8 tests in 3.589s
OK
From less than a second that it took previously to run our tests, we went to nearly 4
seconds. 
As we grow our chat further, we are surely going to add more features, and more features
will require more tests. Our test suite will become too slow and inconvenient to run as it
will quickly reach minutes of time per run. Anything that runs in more than a few seconds
is something that we are going to start running infrequently, thus moving further away
from the benefits of a test-driven approach.
But we might argue that there will be kinds of tests that are always going to take a long
time to run because they are slow by nature due to what they do (for example, performance
tests), so what can we do to improve the situation?
A good first step is to make sure tests are properly spread out in groups that make their
purpose and expected runtime clear. 
Our test_client and test_connection modules contain pinpointed tests that aim to
verify a single piece of our system, so we could move them into a unit package to signal
that they are lightweight and can be run frequently. If I'm working on one of those classes,
I'll know I'll be able to constantly run the tests related to it because they will be cheap.
So let's move them into a tests/unit package that we can run on demand:
└── tests
    ├── __init__.py
    ├── test_chat.py
    └── unit
        ├── __init__.py
        ├── test_client.py
        └── test_connection.py
Now we know that when working on specific parts of the system, we will be able to quickly
verify them by running only the associated test unit:
$ python -m unittest discover tests/unit -v -k connection
test_client_connection (test_client.TestChatClient) ... ok
test_broadcast (test_connection.TestConnection) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.006s
OK


---
**Page 119**

Scaling the Test Suite
Chapter 4
[ 119 ]
The speed is such that test units could be run every time we save the file of the class that
the tests aim to verify.
Our test_chat.py instead is very slow, but it verifies the system from client to server, and
in real conditions, starts a real server over a real network. So let's make clear that its
purpose is to verify the system end to end (e2e) by moving it into a tests/e2e package:
└── tests
    ├── __init__.py
    ├── e2e
    │   ├── __init__.py
    │   └── test_chat.py
    └── unit
        ├── __init__.py
        ├── test_client.py
        └── test_connection.py
There we will have the tests that run very slow and as we know this, we will probably want
to run them only before making a new release of the software to confirm things work as
expected on a real infrastructure:
$ python -m unittest discover tests/e2e -v
test_message_exchange (test_chat.TestChatAcceptance) ... ok
test_many_users (test_chat.TestChatMultiUser) ... ok
test_multiple_readers (test_chat.TestChatMultiUser) ... ok
----------------------------------------------------------------------
Ran 3 tests in 3.568s
OK
OK, now we have tests that we can run when we modify a single component, and tests that
we can run to confirm that the whole app runs correctly before making a new release.
But during development, how are we going to work on modifying existing features and
add more? Trying to find each unit test we need to run to verify a feature is not very
convenient, and also doesn't give us much confidence in the fact that those units will work
well once they are set into the whole system.


---
**Page 120**

Scaling the Test Suite
Chapter 4
[ 120 ]
On the other side, the e2e tests are too slow to base our development life cycle on them. If
we add too many of them, we will have to wait for tests to run for more time than we
actually spend coding. What we need is a set of tests that sit in the middle ground and
verifies a function completely, but that are still able to run quickly enough that we can run
them constantly during our development routine.
That goal is perfectly served by functional tests, a special set of integration tests that are
expected to test a full feature, but are not required to reproduce the real conditions that the
application will face out there in the wild. For example, the database can be fake, the parts
of the system that are not involved in that feature could be disabled, or the networking
could be replaced by the in-memory exchange of messages.
In our case, the slowness of our chat comes from the client-server communication, and the
fact that in the test_connection.py module, we actually have a
test_exchange_with_server test that tries a connection against a fake server. Thus we
should get rid of the whole networking and server startup overhead like so:
    def test_exchange_with_server(self):
        with unittest.mock.patch
                    ("multiprocessing.managers.listener_client",
                       new={"pickle": (None, FakeServer())}):
            c1 = Connection(("localhost", 9090))
            c2 = Connection(("localhost", 9090))
            c1.broadcast("connected message")
            assert c2.get_messages()[-1] == "connected message"
In reality, that test doesn't suit the unit directory much, even if we might consider it a form
of sociable unit test. Crossing the client-server boundary is usually a sign of a higher-level
test, such as integration or e2e tests.
We could use that test as a foundation for our functional tests and move it to a
functional/test_chat.py module that tests that our chat is able to send and receive
messages using FakeServer. Instead of using Connection, we could rewrite the same test
to actually use ChatClient (which uses Connection underneath) so that we can test that
the functionality of exchanging messages with a server works as expected:
import unittest
from unittest import mock
from chat.client import ChatClient
from .fakeserver import FakeServer


---
**Page 121**

Scaling the Test Suite
Chapter 4
[ 121 ]
class TestChatMessageExchange(unittest.TestCase):
    def setUp(self):
        self.srv = mock.patch("multiprocessing.managers.listener_client",
                              new={"pickle": (None, FakeServer())})
        self.srv.start()
    def tearDown(self):
        self.srv.stop()
    def test_exchange_with_server(self):
        c1 = ChatClient("User1")
        c2 = ChatClient("User2")
        c1.send_message("connected message")
        assert c2.fetch_messages()[-1] == "User1: connected message"
Because we moved the test_exchange_with_server test out of our unit tests and into
our functional tests, there is no more use for FakeServer in the unit tests, and it probably
never really fit in there. So, we also moved the FakeServer class into
a fakeserver.py module within the functional directory.
Then, our TestChatMessageExchange test case provides setUp and tearDown methods
to enable a new FakeServer for each one of the tests within the case and disables it when
the tests are complete. This allows us to write tests as if we were using a real server,
without having to worry about the usage of a FakeServer.
Our functional tests are able to provide fairly good safety over the correctness of our
features, but are going to run tens of times faster than the e2e tests. This is slower than the
unit tests, but quick enough that we can frequently run them during our development
routine:
$ python -m unittest discover -k functional -v
test_exchange_with_server
(tests.functional.test_chat.TestChatMessageExchange) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK
So we divided our test suite into three blocks: e2e, functional, and unit:
└── tests
    ├── __init__.py
    ├── e2e
    │   ├── __init__.py
    │   └── test_chat.py


---
**Page 122**

Scaling the Test Suite
Chapter 4
[ 122 ]
    ├── functional
    │   ├── __init__.py
    │   ├── fakeserver.py
    │   └── test_chat.py
    └── unit
        ├── __init__.py
        ├── test_client.py
        └── test_connection.py
As software grows in complexity, you might feel the need to start having more kinds of
integration tests, and as your code grows, you might want to explore introducing narrow
integration tests (tests where you integrate only the few components you care about)
instead of only having functional tests where the whole system is usually started. But this
layout has proved to be a pretty good one for small/medium-sized projects over the years
for me. The key is making sure that writing fast tests is convenient and that e2e tests can be
easily rewritten as functional tests so that our expensive e2e tests remain in a minority.
Moving from e2e to functional
Take a look at our TestChatMessageExchange.test_exchange_with_server
functional test that we wrote in the previous section:
class TestChatMessageExchange(unittest.TestCase):
    ...
    def test_exchange_with_server(self):
        c1 = ChatClient("User1")
        c2 = ChatClient("User2")
        c1.send_message("connected message")
        assert c2.fetch_messages()[-1] == "User1: connected message"
It's probably easy to see that it looks a lot like
our TestChatAcceptance.test_message_exchange e2e test:
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        with new_chat_server() as srv:
            user1 = ChatClient("John Doe")
            user2 = ChatClient("Harry Potter")
            user1.send_message("Hello World")
            messages = user2.fetch_messages()
            assert messages == ["John Doe: Hello World"]


