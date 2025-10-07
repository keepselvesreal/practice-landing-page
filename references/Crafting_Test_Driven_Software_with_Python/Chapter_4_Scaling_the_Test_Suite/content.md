Line 1: 
Line 2: --- 페이지 124 ---
Line 3: 4
Line 4: Scaling the Test Suite
Line 5: Writing one test is easy; writing thousands of tests, maintaining them, and ensuring they
Line 6: don’t become a burden for development and the team is hard. Let’s dive into some tools
Line 7: and best practices that help us define our test suite and keep it in shape.
Line 8: To support the concepts in this chapter, we are going to use the test suite written for our
Line 9: Chat application in Chapter 2, Test Doubles with a Chat Application. We are going to see how
Line 10: to scale it as the application gets bigger and the tests get slower, and how to organize it in a
Line 11: way that can serve us in the long term.
Line 12: In this chapter, we will cover the following topics:
Line 13: Scaling tests
Line 14: Working with multiple suites
Line 15: Carrying out performance testing
Line 16: Enabling continuous integration
Line 17: Technical requirements
Line 18: A working Python interpreter and a GitHub.com account are required to work through the
Line 19: examples in this chapter.
Line 20: The examples we'll work through have been written using Python 3.7, but should work
Line 21: with most modern Python versions.
Line 22: The source code for the examples in this chapter can be found on GitHub
Line 23: at https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python
Line 24: /tree/main/Chapter04
Line 25: 
Line 26: --- 페이지 125 ---
Line 27: Scaling the Test Suite
Line 28: Chapter 4
Line 29: [ 115 ]
Line 30: Scaling tests
Line 31: When we started our Chat application in Chapter 2, Test Doubles with a Chat Application, the
Line 32: whole code base was contained in a single Python module. This module mixed both the
Line 33: application itself, the test suite, and the fakes that we needed for the test suite.
Line 34: While that process fits well for the experimentation and hacking phase, it's not convenient
Line 35: for the long term. As we already saw in Chapter 3, Test-Driven Development while Creating a
Line 36: TODO List, it's possible to split tests into multiple files and directories and keep them
Line 37: separated from our application code.
Line 38: As our project grows, the first step is to split our test suite from our code base. We are going
Line 39: to use the src directory for the code base and the tests directory for the test suite. The
Line 40: src directory in this case will contain the chat package, which contains the modules for
Line 41: the client and server code:
Line 42: .
Line 43: ├── src
Line 44: │   ├── chat
Line 45: │   │   ├── client.py
Line 46: │   │   ├── __init__.py
Line 47: │   │   └── server.py
Line 48: │   └── setup.py
Line 49: The src/chat/client.py file will contain the previous Connection and ChatClient
Line 50: classes, while in src/chat/server.py we are going to put the new_chat_server
Line 51: function.
Line 52: We also provide a very minimal src/setup.py to allow installation of the chat package:
Line 53: from setuptools import setup
Line 54: setup(name='chat', packages=['chat'])
Line 55: Now that we can install the chat package through pip install -e ./src and then use
Line 56: any class within it through import chat, our tests can be moved anywhere; they no longer
Line 57: need to be in the same directory of the files they need to test. 
Line 58: 
Line 59: --- 페이지 126 ---
Line 60: Scaling the Test Suite
Line 61: Chapter 4
Line 62: [ 116 ]
Line 63: Thus we can create a tests directory and gather all our tests there. As we had three
Line 64: different test classes (TestChatAcceptance, TestChatClient, and TestConnection),
Line 65: we are going to split our tests into three dedicated files. This way, while we work, we can
Line 66: run only tests relevant to the part we are modifying:
Line 67: └── tests
Line 68:     ├── __init__.py
Line 69:     ├── test_chat.py
Line 70:     ├── test_client.py
Line 71:     └── test_connection.py
Line 72: The only required changes to the tests we made in Chapter 2, Test Doubles with a Chat
Line 73: Application, are to make sure that we add proper imports to get our classes (for
Line 74: example, from chat.client import ChatClient). Once those are in place, our test
Line 75: suite should be able to run exactly as it used to:
Line 76: $ python -m unittest discover -v
Line 77: test_message_exchange (tests.test_chat.TestChatAcceptance) ... ok
Line 78: test_client_connection (tests.test_client.TestChatClient) ... ok
Line 79: test_client_fetch_messages (tests.test_client.TestChatClient) ... ok
Line 80: test_nickname (tests.test_client.TestChatClient) ... ok
Line 81: test_send_message (tests.test_client.TestChatClient) ... ok
Line 82: test_broadcast (tests.test_connection.TestConnection) ... ok
Line 83: ----------------------------------------------------------------------
Line 84: Ran 6 tests in 0.607s
Line 85: OK
Line 86: In a Test-Driven Development (TDD) approach, the test suite is something we will be able
Line 87: to run frequently and quickly to verify the work we are doing, but in a real-world
Line 88: application, test suites tend to become big and slow and can take minutes or hours to run.
Line 89: For example, we might decide to grow our test suite further. Right now, we only have a test
Line 90: to verify that two users can exchange a message, but we have not verified that when
Line 91: multiple users are involved, we still see messages from all of them, and that each connected
Line 92: user sees the same exact messages.
Line 93: To do so, we can add a new TestChatMultiUser test case to
Line 94: our tests/test_chat.py tests to verify that we can see the messages sent by all users
Line 95: connected to the chat:
Line 96: class TestChatMultiUser(unittest.TestCase):
Line 97:     def test_many_users(self):
Line 98:         with new_chat_server() as srv:
Line 99:             firstUser = ChatClient("John Doe")
Line 100: 
Line 101: --- 페이지 127 ---
Line 102: Scaling the Test Suite
Line 103: Chapter 4
Line 104: [ 117 ]
Line 105:             for uid in range(5):
Line 106:                 moreuser = ChatClient(f"User {uid}")
Line 107:                 moreuser.send_message("Hello!")
Line 108:             messages = firstUser.fetch_messages()
Line 109:             assert len(messages) == 5
Line 110: The test_many_users test connects to the chat as firstUser and then adds five more
Line 111: users to the chat and sends a new message from each of them. At the end of the
Line 112: test, firstUser should be able to see all five messages sent by the other users.
Line 113: To go further, we could also add a test_multiple_readers test that verifies that all users
Line 114: in the chat see the same exact messages:
Line 115:    def test_multiple_readers(self):
Line 116:         with new_chat_server() as srv:
Line 117:             user1 = ChatClient("John Doe")
Line 118:             user2 = ChatClient("User 2")
Line 119:             user3 = ChatClient("User 3")
Line 120:             user1.send_message("Hi all")
Line 121:             user2.send_message("Hello World")
Line 122:             user3.send_message("Hi")
Line 123:             user1_messages = user1.fetch_messages()
Line 124:             user2_messages = user2.fetch_messages()
Line 125:             self.assertEqual(user1_messages, user2_messages)
Line 126: In this case, we have three users joining the chat, each of them sending a message, and then
Line 127: we verified that both user1 and user2 see the same exact messages.
Line 128: Through these two tests, we confirmed that our chat works as expected even when multiple
Line 129: users are inside the chat. If we receive messages from different users, we will see all
Line 130: messages, and all users will see the same exact messages. The side effect of the additional
Line 131: confidence that we now have in our chat is that our test suite has become far slower:
Line 132: $ python -m unittest discover -v -k e2e -k unit
Line 133: test_message_exchange (tests.test_chat.TestChatAcceptance) ... ok
Line 134: test_many_users (tests.test_chat.TestChatMultiUser) ... ok
Line 135: test_multiple_readers (tests.test_chat.TestChatMultiUser) ... ok
Line 136: test_client_connection (tests.test_client.TestChatClient) ... ok
Line 137: test_client_fetch_messages (tests.test_client.TestChatClient) ... ok
Line 138: test_nickname (tests.test_client.TestChatClient) ... ok
Line 139: test_send_message (tests.test_client.TestChatClient) ... ok
Line 140: test_broadcast (tests.test_connection.TestConnection) ... ok
Line 141: ----------------------------------------------------------------------
Line 142: 
Line 143: --- 페이지 128 ---
Line 144: Scaling the Test Suite
Line 145: Chapter 4
Line 146: [ 118 ]
Line 147: Ran 8 tests in 3.589s
Line 148: OK
Line 149: From less than a second that it took previously to run our tests, we went to nearly 4
Line 150: seconds. 
Line 151: As we grow our chat further, we are surely going to add more features, and more features
Line 152: will require more tests. Our test suite will become too slow and inconvenient to run as it
Line 153: will quickly reach minutes of time per run. Anything that runs in more than a few seconds
Line 154: is something that we are going to start running infrequently, thus moving further away
Line 155: from the benefits of a test-driven approach.
Line 156: But we might argue that there will be kinds of tests that are always going to take a long
Line 157: time to run because they are slow by nature due to what they do (for example, performance
Line 158: tests), so what can we do to improve the situation?
Line 159: A good first step is to make sure tests are properly spread out in groups that make their
Line 160: purpose and expected runtime clear. 
Line 161: Our test_client and test_connection modules contain pinpointed tests that aim to
Line 162: verify a single piece of our system, so we could move them into a unit package to signal
Line 163: that they are lightweight and can be run frequently. If I'm working on one of those classes,
Line 164: I'll know I'll be able to constantly run the tests related to it because they will be cheap.
Line 165: So let's move them into a tests/unit package that we can run on demand:
Line 166: └── tests
Line 167:     ├── __init__.py
Line 168:     ├── test_chat.py
Line 169:     └── unit
Line 170:         ├── __init__.py
Line 171:         ├── test_client.py
Line 172:         └── test_connection.py
Line 173: Now we know that when working on specific parts of the system, we will be able to quickly
Line 174: verify them by running only the associated test unit:
Line 175: $ python -m unittest discover tests/unit -v -k connection
Line 176: test_client_connection (test_client.TestChatClient) ... ok
Line 177: test_broadcast (test_connection.TestConnection) ... ok
Line 178: ----------------------------------------------------------------------
Line 179: Ran 2 tests in 0.006s
Line 180: OK
Line 181: 
Line 182: --- 페이지 129 ---
Line 183: Scaling the Test Suite
Line 184: Chapter 4
Line 185: [ 119 ]
Line 186: The speed is such that test units could be run every time we save the file of the class that
Line 187: the tests aim to verify.
Line 188: Our test_chat.py instead is very slow, but it verifies the system from client to server, and
Line 189: in real conditions, starts a real server over a real network. So let's make clear that its
Line 190: purpose is to verify the system end to end (e2e) by moving it into a tests/e2e package:
Line 191: └── tests
Line 192:     ├── __init__.py
Line 193:     ├── e2e
Line 194:     │   ├── __init__.py
Line 195:     │   └── test_chat.py
Line 196:     └── unit
Line 197:         ├── __init__.py
Line 198:         ├── test_client.py
Line 199:         └── test_connection.py
Line 200: There we will have the tests that run very slow and as we know this, we will probably want
Line 201: to run them only before making a new release of the software to confirm things work as
Line 202: expected on a real infrastructure:
Line 203: $ python -m unittest discover tests/e2e -v
Line 204: test_message_exchange (test_chat.TestChatAcceptance) ... ok
Line 205: test_many_users (test_chat.TestChatMultiUser) ... ok
Line 206: test_multiple_readers (test_chat.TestChatMultiUser) ... ok
Line 207: ----------------------------------------------------------------------
Line 208: Ran 3 tests in 3.568s
Line 209: OK
Line 210: OK, now we have tests that we can run when we modify a single component, and tests that
Line 211: we can run to confirm that the whole app runs correctly before making a new release.
Line 212: But during development, how are we going to work on modifying existing features and
Line 213: add more? Trying to find each unit test we need to run to verify a feature is not very
Line 214: convenient, and also doesn't give us much confidence in the fact that those units will work
Line 215: well once they are set into the whole system.
Line 216: 
Line 217: --- 페이지 130 ---
Line 218: Scaling the Test Suite
Line 219: Chapter 4
Line 220: [ 120 ]
Line 221: On the other side, the e2e tests are too slow to base our development life cycle on them. If
Line 222: we add too many of them, we will have to wait for tests to run for more time than we
Line 223: actually spend coding. What we need is a set of tests that sit in the middle ground and
Line 224: verifies a function completely, but that are still able to run quickly enough that we can run
Line 225: them constantly during our development routine.
Line 226: That goal is perfectly served by functional tests, a special set of integration tests that are
Line 227: expected to test a full feature, but are not required to reproduce the real conditions that the
Line 228: application will face out there in the wild. For example, the database can be fake, the parts
Line 229: of the system that are not involved in that feature could be disabled, or the networking
Line 230: could be replaced by the in-memory exchange of messages.
Line 231: In our case, the slowness of our chat comes from the client-server communication, and the
Line 232: fact that in the test_connection.py module, we actually have a
Line 233: test_exchange_with_server test that tries a connection against a fake server. Thus we
Line 234: should get rid of the whole networking and server startup overhead like so:
Line 235:     def test_exchange_with_server(self):
Line 236:         with unittest.mock.patch
Line 237:                     ("multiprocessing.managers.listener_client",
Line 238:                        new={"pickle": (None, FakeServer())}):
Line 239:             c1 = Connection(("localhost", 9090))
Line 240:             c2 = Connection(("localhost", 9090))
Line 241:             c1.broadcast("connected message")
Line 242:             assert c2.get_messages()[-1] == "connected message"
Line 243: In reality, that test doesn't suit the unit directory much, even if we might consider it a form
Line 244: of sociable unit test. Crossing the client-server boundary is usually a sign of a higher-level
Line 245: test, such as integration or e2e tests.
Line 246: We could use that test as a foundation for our functional tests and move it to a
Line 247: functional/test_chat.py module that tests that our chat is able to send and receive
Line 248: messages using FakeServer. Instead of using Connection, we could rewrite the same test
Line 249: to actually use ChatClient (which uses Connection underneath) so that we can test that
Line 250: the functionality of exchanging messages with a server works as expected:
Line 251: import unittest
Line 252: from unittest import mock
Line 253: from chat.client import ChatClient
Line 254: from .fakeserver import FakeServer
Line 255: 
Line 256: --- 페이지 131 ---
Line 257: Scaling the Test Suite
Line 258: Chapter 4
Line 259: [ 121 ]
Line 260: class TestChatMessageExchange(unittest.TestCase):
Line 261:     def setUp(self):
Line 262:         self.srv = mock.patch("multiprocessing.managers.listener_client",
Line 263:                               new={"pickle": (None, FakeServer())})
Line 264:         self.srv.start()
Line 265:     def tearDown(self):
Line 266:         self.srv.stop()
Line 267:     def test_exchange_with_server(self):
Line 268:         c1 = ChatClient("User1")
Line 269:         c2 = ChatClient("User2")
Line 270:         c1.send_message("connected message")
Line 271:         assert c2.fetch_messages()[-1] == "User1: connected message"
Line 272: Because we moved the test_exchange_with_server test out of our unit tests and into
Line 273: our functional tests, there is no more use for FakeServer in the unit tests, and it probably
Line 274: never really fit in there. So, we also moved the FakeServer class into
Line 275: a fakeserver.py module within the functional directory.
Line 276: Then, our TestChatMessageExchange test case provides setUp and tearDown methods
Line 277: to enable a new FakeServer for each one of the tests within the case and disables it when
Line 278: the tests are complete. This allows us to write tests as if we were using a real server,
Line 279: without having to worry about the usage of a FakeServer.
Line 280: Our functional tests are able to provide fairly good safety over the correctness of our
Line 281: features, but are going to run tens of times faster than the e2e tests. This is slower than the
Line 282: unit tests, but quick enough that we can frequently run them during our development
Line 283: routine:
Line 284: $ python -m unittest discover -k functional -v
Line 285: test_exchange_with_server
Line 286: (tests.functional.test_chat.TestChatMessageExchange) ... ok
Line 287: ----------------------------------------------------------------------
Line 288: Ran 1 test in 0.001s
Line 289: OK
Line 290: So we divided our test suite into three blocks: e2e, functional, and unit:
Line 291: └── tests
Line 292:     ├── __init__.py
Line 293:     ├── e2e
Line 294:     │   ├── __init__.py
Line 295:     │   └── test_chat.py
Line 296: 
Line 297: --- 페이지 132 ---
Line 298: Scaling the Test Suite
Line 299: Chapter 4
Line 300: [ 122 ]
Line 301:     ├── functional
Line 302:     │   ├── __init__.py
Line 303:     │   ├── fakeserver.py
Line 304:     │   └── test_chat.py
Line 305:     └── unit
Line 306:         ├── __init__.py
Line 307:         ├── test_client.py
Line 308:         └── test_connection.py
Line 309: As software grows in complexity, you might feel the need to start having more kinds of
Line 310: integration tests, and as your code grows, you might want to explore introducing narrow
Line 311: integration tests (tests where you integrate only the few components you care about)
Line 312: instead of only having functional tests where the whole system is usually started. But this
Line 313: layout has proved to be a pretty good one for small/medium-sized projects over the years
Line 314: for me. The key is making sure that writing fast tests is convenient and that e2e tests can be
Line 315: easily rewritten as functional tests so that our expensive e2e tests remain in a minority.
Line 316: Moving from e2e to functional
Line 317: Take a look at our TestChatMessageExchange.test_exchange_with_server
Line 318: functional test that we wrote in the previous section:
Line 319: class TestChatMessageExchange(unittest.TestCase):
Line 320:     ...
Line 321:     def test_exchange_with_server(self):
Line 322:         c1 = ChatClient("User1")
Line 323:         c2 = ChatClient("User2")
Line 324:         c1.send_message("connected message")
Line 325:         assert c2.fetch_messages()[-1] == "User1: connected message"
Line 326: It's probably easy to see that it looks a lot like
Line 327: our TestChatAcceptance.test_message_exchange e2e test:
Line 328: class TestChatAcceptance(unittest.TestCase):
Line 329:     def test_message_exchange(self):
Line 330:         with new_chat_server() as srv:
Line 331:             user1 = ChatClient("John Doe")
Line 332:             user2 = ChatClient("Harry Potter")
Line 333:             user1.send_message("Hello World")
Line 334:             messages = user2.fetch_messages()
Line 335:             assert messages == ["John Doe: Hello World"]
Line 336: 
Line 337: --- 페이지 133 ---
Line 338: Scaling the Test Suite
Line 339: Chapter 4
Line 340: [ 123 ]
Line 341: The first one starts a new server, while the second one doesn't. But in the end, they both
Line 342: connect two users to a server, send a message from one user, and check that the other user
Line 343: received it.
Line 344: The interesting difference, however, is that one takes nearly no time to run:
Line 345: $ python -m unittest discover -k test_exchange_with_server -v
Line 346: test_exchange_with_server
Line 347: (tests.functional.test_chat.TestChatMessageExchange) ... ok
Line 348: ----------------------------------------------------------------------
Line 349: Ran 1 test in 0.001s
Line 350: While the other takes nearly a second to run:
Line 351: $ python -m unittest discover -k test_message_exchange -v
Line 352: test_message_exchange (tests.e2e.test_chat.TestChatAcceptance) ... ok
Line 353: ----------------------------------------------------------------------
Line 354: Ran 1 test in 0.659s
Line 355: As the two tests look very similar, could we maybe leverage the same approach to make a
Line 356: faster version of our other e2e tests so that we can still be sure that our chat is able to serve
Line 357: multiple users concurrently, without having to pay the cost of running slow e2e tests?
Line 358: Yes, usually functional tests need to be able to exercise the whole system, so e2e tests can
Line 359: frequently be ported to be functional tests and benefit from their faster runtime. While we
Line 360: need a set of e2e tests to ensure that over a real network, things do work, we don't want to
Line 361: test every feature as an e2e test.
Line 362: Most tests that start as e2e could be rewritten over time as functional tests to make our test
Line 363: suite able to keep up as our tests grow, but without sacrificing too much of the safety they
Line 364: provide, and while keeping our test suite fast.
Line 365: So let's move the tests from the TestChatMultiUser e2e test case into the functional
Line 366: TestChatMessageExchange test case. The only thing we have to change in them is to
Line 367: remove the with new_chat_server() as srv: line as we no longer need to start a real
Line 368: server, but apart from that, they should be able to work as they are.
Line 369: The TestChatMessageExchange.setUp method will take care of setting up a fake server
Line 370: for the tests – we just have to use the clients:
Line 371: class TestChatMessageExchange(unittest.TestCase):
Line 372:     ...
Line 373:     def test_many_users(self):
Line 374: 
Line 375: --- 페이지 134 ---
Line 376: Scaling the Test Suite
Line 377: Chapter 4
Line 378: [ 124 ]
Line 379:         firstUser = ChatClient("John Doe")
Line 380:         for uid in range(5):
Line 381:             moreuser = ChatClient(f"User {uid}")
Line 382:             moreuser.send_message("Hello!")
Line 383:         messages = firstUser.fetch_messages()
Line 384:         assert len(messages) == 5
Line 385:     def test_multiple_readers(self):
Line 386:         user1 = ChatClient("John Doe")
Line 387:         user2 = ChatClient("User 2")
Line 388:         user3 = ChatClient("User 3")
Line 389:         user1.send_message("Hi all")
Line 390:         user2.send_message("Hello World")
Line 391:         user3.send_message("Hi")
Line 392:         user1_messages = user1.fetch_messages()
Line 393:         user2_messages = user2.fetch_messages()
Line 394:         self.assertEqual(user1_messages, user2_messages)
Line 395: Now that we have moved those tests to be functional tests, we are able to run a nearly
Line 396: complete check of our system in a few milliseconds by running the unit and functional
Line 397: tests:
Line 398: $ python -m unittest discover -k functional -k unit
Line 399: ........
Line 400: ----------------------------------------------------------------------
Line 401: Ran 8 tests in 0.007s
Line 402: OK
Line 403: Even running the whole test suite, including the e2e tests, now takes under a second, as we
Line 404: moved most of the expensive tests into lighter functional tests:
Line 405: $ python -m unittest discover
Line 406: .........
Line 407: ----------------------------------------------------------------------
Line 408: Ran 9 tests in 0.661s
Line 409: OK
Line 410: 
Line 411: --- 페이지 135 ---
Line 412: Scaling the Test Suite
Line 413: Chapter 4
Line 414: [ 125 ]
Line 415: Organizing the tests into the proper buckets is important to make sure our test suite is still
Line 416: able to run in a timeframe that can be helpful. If the test suite becomes too slow, we are just
Line 417: going to stop relying on it as working with it will become a frustrating experience.
Line 418: That's why it's important to think about how to organize the test suite for your projects and
Line 419: keep in mind the various kinds of test suites that could exist and their goals.
Line 420: Working with multiple suites
Line 421: The separation of tests we did earlier in this chapter helped us realize that there can be
Line 422: multiple test suites inside our tests directory. 
Line 423: We can then point the unittest module to some specific directories using the -k option to
Line 424: run test units on every change, and functional tests when we think we have something that
Line 425: starts looking like a full feature. Thus, we will rely on e2e tests only when making new
Line 426: releases or merging pull requests to pass the last checkpoint.
Line 427: There are a few kinds of test suites that are usually convenient to have in all our projects.
Line 428: The most common kinds of tests suites you will encounter in projects are likely the compile
Line 429: suite, commit tests, and smoke tests.
Line 430: Compile suite
Line 431: The compile suite is a set of tests that must run very fast. Historically, they were performed
Line 432: every time the code had to be recompiled. As that was a frequent action, the compile suite
Line 433: had to be very fast. They were usually static code analysis checks, and while Python doesn't
Line 434: have a proper compilation phase, it's still a good idea to have a compile suite that we can
Line 435: maybe run every time we modify a file.
Line 436: A very good tool in the Python environment to implement those kinds of checks is the
Line 437: prospector project. Once we install prospector with pip install prospector, we will be
Line 438: able to check our code for any errors simply by running it inside our project directory:
Line 439: $ prospector
Line 440: Check Information
Line 441: =================
Line 442:  Started: 2020-06-02 15:22:53.756634
Line 443:  Finished: 2020-06-02 15:22:55.614589
Line 444:  Time Taken: 1.86 seconds
Line 445:  Formatter: grouped
Line 446: 
Line 447: --- 페이지 136 ---
Line 448: Scaling the Test Suite
Line 449: Chapter 4
Line 450: [ 126 ]
Line 451:  Profiles: default, no_doc_warnings, no_test_warnings, strictness_medium,
Line 452: strictness_high, strictness_veryhigh, no_member_warnings
Line 453:  Strictness: None
Line 454:  Libraries Used:
Line 455:  Tools Run: dodgy, mccabe, pep8, profile-validator, pyflakes, pylint
Line 456:  Messages Found: 0
Line 457: Our project doesn't currently have any errors, but suppose that in
Line 458: the ChatClient.send_message method in src/chat/client.py, we mistype the
Line 459: sent_messages variable, prospector would catch the error and notify us that we have a
Line 460: bug in the code before we can run our full test suite:
Line 461: $ prospector
Line 462: Messages
Line 463: ========
Line 464: src/chat/client.py
Line 465:   Line: 23
Line 466:     pylint: Unused variable 'sen_message' (col 8)
Line 467:   Line: 24
Line 468:     pylint: Undefined variable 'sent_message' (col 34)
Line 469:   Line: 25
Line 470:     pylint: Undefined variable 'sent_message' (col 15)
Line 471: If your project relies on type hinting, prospector can also integrate mypy to verify the type
Line 472: correctness of your software before you run the code for real, just to discover it won't work.
Line 473: Commit tests
Line 474: As the name suggests, commit tests are tests you run every time you commit a new change.
Line 475: In our chat example project, the unit and functional tests would be our commit suite. 
Line 476: But as the project grows further and the functional tests start to get too slow, it's not
Line 477: uncommon to see the functional tests become "push tests" that are only run before sharing
Line 478: the code base with your colleagues, while the commit suite gets reduced to unit tests and
Line 479: lighter forms of integration tests.
Line 480: 
Line 481: --- 페이지 137 ---
Line 482: Scaling the Test Suite
Line 483: Chapter 4
Line 484: [ 127 ]
Line 485: If you properly divided your test suite, which piece consists of your commit suite is usually
Line 486: just a matter of passing the proper -k option (one or multiple) to unittest discover:
Line 487: $ python -m unittest discover -k unit -k functional
Line 488: ........
Line 489: ----------------------------------------------------------------------
Line 490: Ran 8 tests in 0.007s
Line 491: OK
Line 492: Through the -k option we can select which parts of our test suite to run and thus limit the
Line 493: execution to only those tests that are fast enough to constitute our commit suite.
Line 494: Smoke tests
Line 495: Smoke tests are a set of tests used to identify whether we broke the system in an obvious
Line 496: way and thus let us know that it doesn't make sense to proceed with further testing.
Line 497: Historically, it came from a time where test cases were manually verified, so before 
Line 498: investing hours of human effort, a set of checks was performed to ensure that the system
Line 499: did work and thus it made sense to test it.
Line 500: Nowadays, tests are far faster and cheaper as they are performed by machines, but it still
Line 501: makes sense to have a smoke test suite before running the more expensive tests. It's usually
Line 502: a good idea to select a subset of your e2e tests that constitute the smoke test suite, and run
Line 503: the complete e2e suite only if it passed the smoke tests.
Line 504: Sometimes, smoke tests are a dedicated set of tests explicitly written for that purpose, but
Line 505: an alternative is to select a set of other tests that we know exercise the most meaningful
Line 506: parts of our system and "tag" them as smoke tests.
Line 507: For example, if our e2e test suite had an extra test_sending_message test that verified
Line 508: that our ChatClient is able to connect to the server and send a message, that would be a
Line 509: fairly good candidate for our smoke test suite, as it doesn't make much sense to proceed
Line 510: with further e2e tests if we are not even able to send messages:
Line 511: class TestChatAcceptance(unittest.TestCase):
Line 512:     def test_message_exchange(self):
Line 513:         ...
Line 514:     def test_sending_message(self):
Line 515:         with new_chat_server() as srv:
Line 516:             user1 = ChatClient("User1")
Line 517:             user1.send_message("Hello World")
Line 518: 
Line 519: --- 페이지 138 ---
Line 520: Scaling the Test Suite
Line 521: Chapter 4
Line 522: [ 128 ]
Line 523: More advanced testing frameworks frequently support the concept of "tagging" tests, so
Line 524: that we can run only those tests with a specific set of tags. But with unittest, it's still
Line 525: possible to build our smoke test suite simply by prefixing test names with the word
Line 526: smoke so that we can select them.
Line 527: In this case, we would thus rename test_sending_message as
Line 528: test_smoke_sending_message to make it part of our smoke tests and we would be able
Line 529: to run our e2e tests as before, but also benefit from having a smoke test suite to run
Line 530: beforehand as our e2e tests grow further. So we will first have our smoke test, as follows: 
Line 531: $ python -m unittest discover -k smoke -v
Line 532: test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
Line 533: ----------------------------------------------------------------------
Line 534: Ran 1 test in 0.334s
Line 535: OK
Line 536: This is then followed by our e2e test:
Line 537: $ python -m unittest discover -k e2e -v
Line 538: test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
Line 539: test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
Line 540: ----------------------------------------------------------------------
Line 541: Ran 2 tests in 0.957s
Line 542: OK
Line 543: As for the commit suite, we were able to rely on the -k option to only execute our smoke
Line 544: tests or all our e2e tests. Thus, we are able to select which kinds of tests we want to run.
Line 545: Carrying out performance testing
Line 546: Even though it's not related to verifying the correctness of software, a performance test
Line 547: suite is part of the testing strategy for many applications. Usually, they are expected to
Line 548: assess the performance of the software in terms of how fast it can do its job and how many
Line 549: concurrent users it can handle.
Line 550: Due to their nature, performance tests are usually very expensive as they have to repeat an
Line 551: operation multiple times to get a benchmark that is able to provide a fairly stable report
Line 552: and absorb outliers that could have taken too long to run just because the system was busy
Line 553: doing something else.
Line 554: 
Line 555: --- 페이지 139 ---
Line 556: Scaling the Test Suite
Line 557: Chapter 4
Line 558: [ 129 ]
Line 559: For this reason, the performance test suite is usually only executed after all other suites are
Line 560: passed (also, it doesn't make much sense to assess how fast it can test the software when we
Line 561: haven't checked that it actually does the right thing).
Line 562: For our chat example, we could write a benchmark suite that verifies how many messages
Line 563: per second we are able to handle:
Line 564: To begin with, we don't want to put that into the middle of all the other tests, so
Line 565: 1.
Line 566: we are going to put our benchmarks into a benchmarks directory, separate from
Line 567: the tests directory:
Line 568: .
Line 569: ├── benchmarks
Line 570: │   ├── __init__.py
Line 571: │   └── test_chat.py
Line 572: ├── src
Line 573: │   ├── chat
Line 574: │   └── setup.py
Line 575: └── tests
Line 576:     ├── __init__.py
Line 577:     ├── e2e
Line 578:     ├── functional
Line 579:     └── unit
Line 580: test_chat.py can then contain the benchmarks we care about. In this case, we
Line 581: 2.
Line 582: are going to create a benchmark to report how long it takes to send 10 messages:
Line 583: import unittest
Line 584: import timeit
Line 585: from chat.client import ChatClient
Line 586: from chat.server import new_chat_server
Line 587: class BenchmarkMixin:
Line 588:     def bench(self, f, number):
Line 589:         t = timeit.timeit(f, number=number)
Line 590:         print(f"\n\ttime: {t:.2f}, iteration: {t/number:.2f}")
Line 591: class BenchmarkChat(unittest.TestCase, BenchmarkMixin):
Line 592:     def test_sending_messages(self):
Line 593:         with new_chat_server() as srv:
Line 594:             user1 = ChatClient("User1")
Line 595:             self.bench(lambda: user1.send_message("Hello World"),
Line 596:                        number=10)
Line 597: 
Line 598: --- 페이지 140 ---
Line 599: Scaling the Test Suite
Line 600: Chapter 4
Line 601: [ 130 ]
Line 602: BenchmarkMixin is a utility class that is going to provide the self.bench
Line 603: method we can use to report the execution time of our benchmarks. The real
Line 604: benchmark is provided by BenchmarkChat.test_sending_message, which is
Line 605: going to connect a client to a server and then repeat the user.send_message
Line 606: call 10 times.
Line 607: Then we can run our benchmarks, pointing unittest to the benchmarks
Line 608: 3.
Line 609: directory:
Line 610: $ python -m unittest discover benchmarks -v
Line 611: test_sending_messages (test_chat.BenchmarkChat) ...
Line 612:         time: 2.31, iteration: 0.23
Line 613: ok
Line 614: -------------------------------------------------------------------
Line 615: ---
Line 616: Ran 1 test in 2.406s
Line 617: If we want to only run our tests instead, we could point the unittest module to
Line 618: 4.
Line 619: the tests directory:
Line 620: $ python -m unittest discover tests
Line 621: ..........
Line 622: -------------------------------------------------------------------
Line 623: ---
Line 624: Ran 10 tests in 1.013s
Line 625: Running just python -m unittest discover will run both the benchmarks and tests, so
Line 626: make sure you point the discover process to the right directory when running your tests.
Line 627: An alternative is to name your benchmark files with a different prefix (bench_*.py instead
Line 628: of tests_*.py) and then use the -p option to specify the custom prefix when running
Line 629: your benchmarks. But in that case, it might not be immediately obvious how to run
Line 630: benchmarks for a new contributor to your project.
Line 631: Our chat test suite is now fairly complete: it has e2e tests, functional tests, unit tests, smoke
Line 632: tests, and benchmarks. But we still have to remember to manually run all tests every time
Line 633: we do a change. Let's look at how we can tackle this. 
Line 634: 
Line 635: --- 페이지 141 ---
Line 636: Scaling the Test Suite
Line 637: Chapter 4
Line 638: [ 131 ]
Line 639: Enabling continuous integration
Line 640: Wouldn't it be convenient if someone else was in charge of running all our tests every time
Line 641: we made a change to our code base? This would mean that we couldn't forget to run some
Line 642: specific tests just because they were related to an area of the code that we were not directly
Line 643: touching.
Line 644: That's exactly the goal of Continuous Integration (CI) environments. Every time we push
Line 645: our changes to the code repository, these environments will notice and rerun the tests,
Line 646: usually merging our changes with the changes from our colleagues to make sure they cope
Line 647: well together.
Line 648: If you have a code repository on GitHub, using Travis as your CI is a fairly straightforward
Line 649: process. Suppose that I made an amol-/travistest GitHub project where I pushed the
Line 650: code base of our chat application; to enable Travis, the first thing that I have to do is to go
Line 651: to https:/​/​travis-​ci.​com/​ and log in with my GitHub credentials:
Line 652: Figure 4.1 – Travis CI Sign in page
Line 653: 
Line 654: --- 페이지 142 ---
Line 655: Scaling the Test Suite
Line 656: Chapter 4
Line 657: [ 132 ]
Line 658: Once we are in, we must enable the integration with GitHub so that all our GitHub
Line 659: repositories become visible on Travis. We can do this by clicking on the top-right profile
Line 660: icon and then on the Settings option. That will show us a green Activate button that will
Line 661: allow us to enable Travis on our GitHub repositories:
Line 662: Figure 4.2 – Integrating with GitHub
Line 663: 
Line 664: --- 페이지 143 ---
Line 665: Scaling the Test Suite
Line 666: Chapter 4
Line 667: [ 133 ]
Line 668: Once we have enabled the Travis application on GitHub, we can go
Line 669: to https://travis-
Line 670: ci.com/github/{YOUR_GITHUB_USER}/{GITHUB_PROJECT} (which in my case
Line 671: is https:/​/​travis-​ci.​com/​github/​amol-​/​travistest) to confirm the repository is
Line 672: activated, but hasn't yet got any build:
Line 673: Figure 4.3 – Conﬁrming that the repository was activated
Line 674: Travis will be monitoring your repository for changes. But it won't know how to run tests
Line 675: for your project. So even if we push changes to the source code, nothing will happen.
Line 676: To tell Travis how to run our tests, we need to add to the repository a .travis.yml file
Line 677: with the following configuration: 
Line 678: language: python
Line 679: os: linux
Line 680: dist: xenial
Line 681: python:
Line 682:   - 3.7
Line 683:   - &mainstream_python 3.8
Line 684:   - nightly
Line 685: install:
Line 686:   - "pip install -e src"
Line 687: script:
Line 688: 
Line 689: --- 페이지 144 ---
Line 690: Scaling the Test Suite
Line 691: Chapter 4
Line 692: [ 134 ]
Line 693:   - "python -m unittest discover tests -v"
Line 694: after_success:
Line 695:   - "python -m unittest discover benchmarks -v"
Line 696: This configuration is going to run our tests on Python 3.7, 3.8, and the current nightly build
Line 697: of Python (3.9 at the time of writing). 
Line 698: Before running the tests (the install: section), it will install the chat distribution from
Line 699: src to make the chat package available to the tests.
Line 700: Then the tests will be performed as specified in the script: section and if they succeed,
Line 701: the benchmarks will be executed as stated in the after_success: section.
Line 702: Once we push into the repository the .travis.yml file, Travis will see it and will start
Line 703: executing the tests as specified in the configuration file. If everything worked as expected,
Line 704: by refreshing the Travis project page, we should see a successful run of our tests on the
Line 705: three versions of Python:
Line 706: Figure 4.4 – Successful run on the three versions of Python
Line 707: 
Line 708: --- 페이지 145 ---
Line 709: Scaling the Test Suite
Line 710: Chapter 4
Line 711: [ 135 ]
Line 712: If you click on any of the jobs, it will show you what happened, confirming that both the
Line 713: tests and benchmarks were run:
Line 714: Figure 4.5 – Checking the code base
Line 715: Every time we make a change to our code base, Travis will rerun all tests, guaranteeing for
Line 716: us that we haven't broken anything and allowing us to see whether the performances
Line 717: became worse with the most recent changes.
Line 718: Travis is not limited to performing a single thing such as running tests for your projects; it
Line 719: can actually perform multi-state pipelines that can be evolved to create releases of your
Line 720: packages or deploy them to a staging environment when the tests succeed. Just be aware
Line 721: that every build that you do will consume credits, and while you do have some available
Line 722: for free, you will have to switch to a paid plan if your CI needs grow beyond the amount
Line 723: covered by free credits.
Line 724: 
Line 725: --- 페이지 146 ---
Line 726: Scaling the Test Suite
Line 727: Chapter 4
Line 728: [ 136 ]
Line 729: Performance testing in the cloud
Line 730: While our CI system does most of what we need, it's important to remember that cloud
Line 731: runners are not designed for benchmarking. So our performance test suite only becomes 
Line 732: reliable when there are major slowdowns and over the course of multiple runs.
Line 733: The two most common strategies when running performance tests in the cloud are as
Line 734: follows:
Line 735: To rerun the test suite multiple times and pick the fastest run, in order to absorb
Line 736: the temporary contention of resources in the cloud
Line 737: To record the metrics into a monitoring service such as Prometheus, from which
Line 738: it becomes possible to see the trend of the metrics over the course of multiple
Line 739: runs
Line 740: Whichever direction you choose to go in, make sure you keep in mind that cloud services
Line 741: such as Travis can have random slowdowns due to the other requests they are serving, and
Line 742: thus it's usually better to make decisions over the course of multiple runs.
Line 743: Summary
Line 744: In this chapter, we saw how we can keep our test suite effective and comfortable as the
Line 745: complexity of our application and the size of our test suites grow. We saw how tests can be
Line 746: organized into different categories that could be run at different times, and also saw how
Line 747: we can have multiple different test suites in a single project, each serving its own purpose.
Line 748: In general, over the previous four chapters, we learned how to structure our testing
Line 749: strategy and how testing can help us design robust applications. We also saw how Python
Line 750: has everything we need built in already through the unittest module.
Line 751: But as our test suite grows and becomes bigger, there are utilities, patterns, and features
Line 752: that we would have to implement on our own in the unittest module. That's why, over
Line 753: the course of many years, many frameworks have been designed for testing by the Python
Line 754: community. In the next chapter, we are going to introduce pytest, the most widespread
Line 755: framework for testing Python applications.