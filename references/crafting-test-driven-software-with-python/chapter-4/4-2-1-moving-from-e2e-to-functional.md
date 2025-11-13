# 4.2.1 Moving from e2e to functional (pp.122-125)

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


