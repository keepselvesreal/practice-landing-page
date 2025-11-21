# 4.3.3 Smoke tests (pp.127-128)

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


