# Chapter 4: Scaling the Test Suite (pp.114-138)

---
**Page 114**

4
Scaling the Test Suite
Writing one test is easy; writing thousands of tests, maintaining them, and ensuring they
don’t become a burden for development and the team is hard. Let’s dive into some tools
and best practices that help us define our test suite and keep it in shape.
To support the concepts in this chapter, we are going to use the test suite written for our
Chat application in Chapter 2, Test Doubles with a Chat Application. We are going to see how
to scale it as the application gets bigger and the tests get slower, and how to organize it in a
way that can serve us in the long term.
In this chapter, we will cover the following topics:
Scaling tests
Working with multiple suites
Carrying out performance testing
Enabling continuous integration
Technical requirements
A working Python interpreter and a GitHub.com account are required to work through the
examples in this chapter.
The examples we'll work through have been written using Python 3.7, but should work
with most modern Python versions.
The source code for the examples in this chapter can be found on GitHub
at https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python
/tree/main/Chapter04


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


---
**Page 123**

Scaling the Test Suite
Chapter 4
[ 123 ]
The first one starts a new server, while the second one doesn't. But in the end, they both
connect two users to a server, send a message from one user, and check that the other user
received it.
The interesting difference, however, is that one takes nearly no time to run:
$ python -m unittest discover -k test_exchange_with_server -v
test_exchange_with_server
(tests.functional.test_chat.TestChatMessageExchange) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.001s
While the other takes nearly a second to run:
$ python -m unittest discover -k test_message_exchange -v
test_message_exchange (tests.e2e.test_chat.TestChatAcceptance) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.659s
As the two tests look very similar, could we maybe leverage the same approach to make a
faster version of our other e2e tests so that we can still be sure that our chat is able to serve
multiple users concurrently, without having to pay the cost of running slow e2e tests?
Yes, usually functional tests need to be able to exercise the whole system, so e2e tests can
frequently be ported to be functional tests and benefit from their faster runtime. While we
need a set of e2e tests to ensure that over a real network, things do work, we don't want to
test every feature as an e2e test.
Most tests that start as e2e could be rewritten over time as functional tests to make our test
suite able to keep up as our tests grow, but without sacrificing too much of the safety they
provide, and while keeping our test suite fast.
So let's move the tests from the TestChatMultiUser e2e test case into the functional
TestChatMessageExchange test case. The only thing we have to change in them is to
remove the with new_chat_server() as srv: line as we no longer need to start a real
server, but apart from that, they should be able to work as they are.
The TestChatMessageExchange.setUp method will take care of setting up a fake server
for the tests – we just have to use the clients:
class TestChatMessageExchange(unittest.TestCase):
    ...
    def test_many_users(self):


---
**Page 124**

Scaling the Test Suite
Chapter 4
[ 124 ]
        firstUser = ChatClient("John Doe")
        for uid in range(5):
            moreuser = ChatClient(f"User {uid}")
            moreuser.send_message("Hello!")
        messages = firstUser.fetch_messages()
        assert len(messages) == 5
    def test_multiple_readers(self):
        user1 = ChatClient("John Doe")
        user2 = ChatClient("User 2")
        user3 = ChatClient("User 3")
        user1.send_message("Hi all")
        user2.send_message("Hello World")
        user3.send_message("Hi")
        user1_messages = user1.fetch_messages()
        user2_messages = user2.fetch_messages()
        self.assertEqual(user1_messages, user2_messages)
Now that we have moved those tests to be functional tests, we are able to run a nearly
complete check of our system in a few milliseconds by running the unit and functional
tests:
$ python -m unittest discover -k functional -k unit
........
----------------------------------------------------------------------
Ran 8 tests in 0.007s
OK
Even running the whole test suite, including the e2e tests, now takes under a second, as we
moved most of the expensive tests into lighter functional tests:
$ python -m unittest discover
.........
----------------------------------------------------------------------
Ran 9 tests in 0.661s
OK


---
**Page 125**

Scaling the Test Suite
Chapter 4
[ 125 ]
Organizing the tests into the proper buckets is important to make sure our test suite is still
able to run in a timeframe that can be helpful. If the test suite becomes too slow, we are just
going to stop relying on it as working with it will become a frustrating experience.
That's why it's important to think about how to organize the test suite for your projects and
keep in mind the various kinds of test suites that could exist and their goals.
Working with multiple suites
The separation of tests we did earlier in this chapter helped us realize that there can be
multiple test suites inside our tests directory. 
We can then point the unittest module to some specific directories using the -k option to
run test units on every change, and functional tests when we think we have something that
starts looking like a full feature. Thus, we will rely on e2e tests only when making new
releases or merging pull requests to pass the last checkpoint.
There are a few kinds of test suites that are usually convenient to have in all our projects.
The most common kinds of tests suites you will encounter in projects are likely the compile
suite, commit tests, and smoke tests.
Compile suite
The compile suite is a set of tests that must run very fast. Historically, they were performed
every time the code had to be recompiled. As that was a frequent action, the compile suite
had to be very fast. They were usually static code analysis checks, and while Python doesn't
have a proper compilation phase, it's still a good idea to have a compile suite that we can
maybe run every time we modify a file.
A very good tool in the Python environment to implement those kinds of checks is the
prospector project. Once we install prospector with pip install prospector, we will be
able to check our code for any errors simply by running it inside our project directory:
$ prospector
Check Information
=================
 Started: 2020-06-02 15:22:53.756634
 Finished: 2020-06-02 15:22:55.614589
 Time Taken: 1.86 seconds
 Formatter: grouped


---
**Page 126**

Scaling the Test Suite
Chapter 4
[ 126 ]
 Profiles: default, no_doc_warnings, no_test_warnings, strictness_medium,
strictness_high, strictness_veryhigh, no_member_warnings
 Strictness: None
 Libraries Used:
 Tools Run: dodgy, mccabe, pep8, profile-validator, pyflakes, pylint
 Messages Found: 0
Our project doesn't currently have any errors, but suppose that in
the ChatClient.send_message method in src/chat/client.py, we mistype the
sent_messages variable, prospector would catch the error and notify us that we have a
bug in the code before we can run our full test suite:
$ prospector
Messages
========
src/chat/client.py
  Line: 23
    pylint: Unused variable 'sen_message' (col 8)
  Line: 24
    pylint: Undefined variable 'sent_message' (col 34)
  Line: 25
    pylint: Undefined variable 'sent_message' (col 15)
If your project relies on type hinting, prospector can also integrate mypy to verify the type
correctness of your software before you run the code for real, just to discover it won't work.
Commit tests
As the name suggests, commit tests are tests you run every time you commit a new change.
In our chat example project, the unit and functional tests would be our commit suite. 
But as the project grows further and the functional tests start to get too slow, it's not
uncommon to see the functional tests become "push tests" that are only run before sharing
the code base with your colleagues, while the commit suite gets reduced to unit tests and
lighter forms of integration tests.


---
**Page 127**

Scaling the Test Suite
Chapter 4
[ 127 ]
If you properly divided your test suite, which piece consists of your commit suite is usually
just a matter of passing the proper -k option (one or multiple) to unittest discover:
$ python -m unittest discover -k unit -k functional
........
----------------------------------------------------------------------
Ran 8 tests in 0.007s
OK
Through the -k option we can select which parts of our test suite to run and thus limit the
execution to only those tests that are fast enough to constitute our commit suite.
Smoke tests
Smoke tests are a set of tests used to identify whether we broke the system in an obvious
way and thus let us know that it doesn't make sense to proceed with further testing.
Historically, it came from a time where test cases were manually verified, so before 
investing hours of human effort, a set of checks was performed to ensure that the system
did work and thus it made sense to test it.
Nowadays, tests are far faster and cheaper as they are performed by machines, but it still
makes sense to have a smoke test suite before running the more expensive tests. It's usually
a good idea to select a subset of your e2e tests that constitute the smoke test suite, and run
the complete e2e suite only if it passed the smoke tests.
Sometimes, smoke tests are a dedicated set of tests explicitly written for that purpose, but
an alternative is to select a set of other tests that we know exercise the most meaningful
parts of our system and "tag" them as smoke tests.
For example, if our e2e test suite had an extra test_sending_message test that verified
that our ChatClient is able to connect to the server and send a message, that would be a
fairly good candidate for our smoke test suite, as it doesn't make much sense to proceed
with further e2e tests if we are not even able to send messages:
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        ...
    def test_sending_message(self):
        with new_chat_server() as srv:
            user1 = ChatClient("User1")
            user1.send_message("Hello World")


---
**Page 128**

Scaling the Test Suite
Chapter 4
[ 128 ]
More advanced testing frameworks frequently support the concept of "tagging" tests, so
that we can run only those tests with a specific set of tags. But with unittest, it's still
possible to build our smoke test suite simply by prefixing test names with the word
smoke so that we can select them.
In this case, we would thus rename test_sending_message as
test_smoke_sending_message to make it part of our smoke tests and we would be able
to run our e2e tests as before, but also benefit from having a smoke test suite to run
beforehand as our e2e tests grow further. So we will first have our smoke test, as follows: 
$ python -m unittest discover -k smoke -v
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.334s
OK
This is then followed by our e2e test:
$ python -m unittest discover -k e2e -v
test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.957s
OK
As for the commit suite, we were able to rely on the -k option to only execute our smoke
tests or all our e2e tests. Thus, we are able to select which kinds of tests we want to run.
Carrying out performance testing
Even though it's not related to verifying the correctness of software, a performance test
suite is part of the testing strategy for many applications. Usually, they are expected to
assess the performance of the software in terms of how fast it can do its job and how many
concurrent users it can handle.
Due to their nature, performance tests are usually very expensive as they have to repeat an
operation multiple times to get a benchmark that is able to provide a fairly stable report
and absorb outliers that could have taken too long to run just because the system was busy
doing something else.


---
**Page 129**

Scaling the Test Suite
Chapter 4
[ 129 ]
For this reason, the performance test suite is usually only executed after all other suites are
passed (also, it doesn't make much sense to assess how fast it can test the software when we
haven't checked that it actually does the right thing).
For our chat example, we could write a benchmark suite that verifies how many messages
per second we are able to handle:
To begin with, we don't want to put that into the middle of all the other tests, so
1.
we are going to put our benchmarks into a benchmarks directory, separate from
the tests directory:
.
├── benchmarks
│   ├── __init__.py
│   └── test_chat.py
├── src
│   ├── chat
│   └── setup.py
└── tests
    ├── __init__.py
    ├── e2e
    ├── functional
    └── unit
test_chat.py can then contain the benchmarks we care about. In this case, we
2.
are going to create a benchmark to report how long it takes to send 10 messages:
import unittest
import timeit
from chat.client import ChatClient
from chat.server import new_chat_server
class BenchmarkMixin:
    def bench(self, f, number):
        t = timeit.timeit(f, number=number)
        print(f"\n\ttime: {t:.2f}, iteration: {t/number:.2f}")
class BenchmarkChat(unittest.TestCase, BenchmarkMixin):
    def test_sending_messages(self):
        with new_chat_server() as srv:
            user1 = ChatClient("User1")
            self.bench(lambda: user1.send_message("Hello World"),
                       number=10)


---
**Page 130**

Scaling the Test Suite
Chapter 4
[ 130 ]
BenchmarkMixin is a utility class that is going to provide the self.bench
method we can use to report the execution time of our benchmarks. The real
benchmark is provided by BenchmarkChat.test_sending_message, which is
going to connect a client to a server and then repeat the user.send_message
call 10 times.
Then we can run our benchmarks, pointing unittest to the benchmarks
3.
directory:
$ python -m unittest discover benchmarks -v
test_sending_messages (test_chat.BenchmarkChat) ...
        time: 2.31, iteration: 0.23
ok
-------------------------------------------------------------------
---
Ran 1 test in 2.406s
If we want to only run our tests instead, we could point the unittest module to
4.
the tests directory:
$ python -m unittest discover tests
..........
-------------------------------------------------------------------
---
Ran 10 tests in 1.013s
Running just python -m unittest discover will run both the benchmarks and tests, so
make sure you point the discover process to the right directory when running your tests.
An alternative is to name your benchmark files with a different prefix (bench_*.py instead
of tests_*.py) and then use the -p option to specify the custom prefix when running
your benchmarks. But in that case, it might not be immediately obvious how to run
benchmarks for a new contributor to your project.
Our chat test suite is now fairly complete: it has e2e tests, functional tests, unit tests, smoke
tests, and benchmarks. But we still have to remember to manually run all tests every time
we do a change. Let's look at how we can tackle this. 


---
**Page 131**

Scaling the Test Suite
Chapter 4
[ 131 ]
Enabling continuous integration
Wouldn't it be convenient if someone else was in charge of running all our tests every time
we made a change to our code base? This would mean that we couldn't forget to run some
specific tests just because they were related to an area of the code that we were not directly
touching.
That's exactly the goal of Continuous Integration (CI) environments. Every time we push
our changes to the code repository, these environments will notice and rerun the tests,
usually merging our changes with the changes from our colleagues to make sure they cope
well together.
If you have a code repository on GitHub, using Travis as your CI is a fairly straightforward
process. Suppose that I made an amol-/travistest GitHub project where I pushed the
code base of our chat application; to enable Travis, the first thing that I have to do is to go
to https:/​/​travis-​ci.​com/​ and log in with my GitHub credentials:
Figure 4.1 – Travis CI Sign in page


---
**Page 132**

Scaling the Test Suite
Chapter 4
[ 132 ]
Once we are in, we must enable the integration with GitHub so that all our GitHub
repositories become visible on Travis. We can do this by clicking on the top-right profile
icon and then on the Settings option. That will show us a green Activate button that will
allow us to enable Travis on our GitHub repositories:
Figure 4.2 – Integrating with GitHub


---
**Page 133**

Scaling the Test Suite
Chapter 4
[ 133 ]
Once we have enabled the Travis application on GitHub, we can go
to https://travis-
ci.com/github/{YOUR_GITHUB_USER}/{GITHUB_PROJECT} (which in my case
is https:/​/​travis-​ci.​com/​github/​amol-​/​travistest) to confirm the repository is
activated, but hasn't yet got any build:
Figure 4.3 – Conﬁrming that the repository was activated
Travis will be monitoring your repository for changes. But it won't know how to run tests
for your project. So even if we push changes to the source code, nothing will happen.
To tell Travis how to run our tests, we need to add to the repository a .travis.yml file
with the following configuration: 
language: python
os: linux
dist: xenial
python:
  - 3.7
  - &mainstream_python 3.8
  - nightly
install:
  - "pip install -e src"
script:


---
**Page 134**

Scaling the Test Suite
Chapter 4
[ 134 ]
  - "python -m unittest discover tests -v"
after_success:
  - "python -m unittest discover benchmarks -v"
This configuration is going to run our tests on Python 3.7, 3.8, and the current nightly build
of Python (3.9 at the time of writing). 
Before running the tests (the install: section), it will install the chat distribution from
src to make the chat package available to the tests.
Then the tests will be performed as specified in the script: section and if they succeed,
the benchmarks will be executed as stated in the after_success: section.
Once we push into the repository the .travis.yml file, Travis will see it and will start
executing the tests as specified in the configuration file. If everything worked as expected,
by refreshing the Travis project page, we should see a successful run of our tests on the
three versions of Python:
Figure 4.4 – Successful run on the three versions of Python


---
**Page 135**

Scaling the Test Suite
Chapter 4
[ 135 ]
If you click on any of the jobs, it will show you what happened, confirming that both the
tests and benchmarks were run:
Figure 4.5 – Checking the code base
Every time we make a change to our code base, Travis will rerun all tests, guaranteeing for
us that we haven't broken anything and allowing us to see whether the performances
became worse with the most recent changes.
Travis is not limited to performing a single thing such as running tests for your projects; it
can actually perform multi-state pipelines that can be evolved to create releases of your
packages or deploy them to a staging environment when the tests succeed. Just be aware
that every build that you do will consume credits, and while you do have some available
for free, you will have to switch to a paid plan if your CI needs grow beyond the amount
covered by free credits.


---
**Page 136**

Scaling the Test Suite
Chapter 4
[ 136 ]
Performance testing in the cloud
While our CI system does most of what we need, it's important to remember that cloud
runners are not designed for benchmarking. So our performance test suite only becomes 
reliable when there are major slowdowns and over the course of multiple runs.
The two most common strategies when running performance tests in the cloud are as
follows:
To rerun the test suite multiple times and pick the fastest run, in order to absorb
the temporary contention of resources in the cloud
To record the metrics into a monitoring service such as Prometheus, from which
it becomes possible to see the trend of the metrics over the course of multiple
runs
Whichever direction you choose to go in, make sure you keep in mind that cloud services
such as Travis can have random slowdowns due to the other requests they are serving, and
thus it's usually better to make decisions over the course of multiple runs.
Summary
In this chapter, we saw how we can keep our test suite effective and comfortable as the
complexity of our application and the size of our test suites grow. We saw how tests can be
organized into different categories that could be run at different times, and also saw how
we can have multiple different test suites in a single project, each serving its own purpose.
In general, over the previous four chapters, we learned how to structure our testing
strategy and how testing can help us design robust applications. We also saw how Python
has everything we need built in already through the unittest module.
But as our test suite grows and becomes bigger, there are utilities, patterns, and features
that we would have to implement on our own in the unittest module. That's why, over
the course of many years, many frameworks have been designed for testing by the Python
community. In the next chapter, we are going to introduce pytest, the most widespread
framework for testing Python applications.


---
**Page 137**

2
Section 2: PyTest for Python
Testing
In this section, we will learn how PyTest, the most widespread Python testing framework,
can be applied to the concepts we learned in Section 1, Software Testing and Test-Driven
Development, regarding plain Python. We will also learn how to set up fixtures and which
plugins exist to make our lives easier when we're maintaining a test suite.
This section comprises the following chapters:
Chapter 5, Introduction to PyTest
Chapter 6, Dynamic and Parametric Tests and Fixtures 
Chapter 7, Fitness Function with a Contact Book Application 
Chapter 8, PyTest Essential Plugins 
Chapter 9, Managing Test Environments with Tox
Chapter 10, Testing Documentation and Property-Based Testing


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


