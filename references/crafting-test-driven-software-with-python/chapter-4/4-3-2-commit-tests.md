# 4.3.2 Commit tests (pp.126-127)

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


