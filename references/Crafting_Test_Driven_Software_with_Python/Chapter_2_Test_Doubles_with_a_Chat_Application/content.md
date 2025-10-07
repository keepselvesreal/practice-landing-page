Line 1: 
Line 2: --- 페이지 41 ---
Line 3: 2
Line 4: Test Doubles with a Chat
Line 5: Application
Line 6: We have seen how a test suite, to be reasonably reliable, should include various kinds of
Line 7: tests that cover components at various levels. Usually, tests, in regard to how many
Line 8: components they involve, are categorized into at least three kinds: unit, integration, and
Line 9: end-to-end.
Line 10: Test doubles ease the implementation of tests by breaking dependencies between
Line 11: components and allowing us to simulate the behaviors we want.
Line 12: In this chapter, we will look at the most common kinds of test doubles, what their goals are,
Line 13: and how to use them in real code. By the end of this chapter, we will have covered how to
Line 14: use all those test doubles and you will be able to leverage them for your own Python
Line 15: projects.
Line 16: By adding test doubles to your toolchain, you will be able to write faster tests, decouple the
Line 17: components you want to test from the rest of the system, simulate behaviors that depend
Line 18: on other components' state, and in general move your test suite development forward with
Line 19: fewer blockers.
Line 20: In this chapter, we will learn how to move forward, in the Test-Driven Development
Line 21: (TDD) way, the development of an application that depends on other external
Line 22: dependencies such as a database management system and networking, relying on test
Line 23: doubles for the development process and replacing them in our inner test layers to ensure
Line 24: fast and consistent execution of our tests.
Line 25: In this chapter, we will cover the following topics:
Line 26: Introducing test doubles
Line 27: Starting our chat application with TDD
Line 28: Using dummy objects
Line 29: Replacing components with stubs
Line 30: 
Line 31: --- 페이지 42 ---
Line 32: Test Doubles with a Chat Application
Line 33: Chapter 2
Line 34: [ 32 ]
Line 35: Checking behaviors with spies
Line 36: Using mocks
Line 37: Replacing dependencies with fakes
Line 38: Understanding acceptance tests and doubles
Line 39: Managing dependencies with dependency injection
Line 40: Technical requirements
Line 41: A working Python interpreter should be all that is needed.
Line 42: The examples have been written on Python 3.7 but should work on most modern Python
Line 43: versions.
Line 44: You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
Line 45: PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter02.
Line 46: Introducing test doubles
Line 47: In test-driven development, the tests drive the development process and architecture. The
Line 48: software design evolves as the software changes during the development of new tests, and
Line 49: the architecture you end up with should be a consequence of the need to satisfy your tests.
Line 50: Tests are thus the arbiter that decides the future of our software and declares that the
Line 51: software is doing what it is designed for. There are specific kinds of tests that are explicitly
Line 52: designed to tell us that the software is doing what it was requested: Acceptance and
Line 53: Functional tests.
Line 54: So, while there are two possible approaches to TDD, top-down and bottom-up (one starting
Line 55: with higher-level tests first, and the other starting with unit tests first), the best way to
Line 56: avoid going in the wrong direction is to always keep in mind your acceptance rules, and
Line 57: the most effective way to do so is to write them down as tests.
Line 58: But how can we write a test that depends on the whole software existing and working if we
Line 59: haven't yet written the software at all? The key is test doubles: objects that are able to
Line 60: replace missing, incomplete, or expensive parts of our code just for the purpose of testing.
Line 61: A test double is an object that takes the place of another object, faking that it is actually able
Line 62: to do the same things as the other object, while in reality, it does nothing.
Line 63: 
Line 64: --- 페이지 43 ---
Line 65: Test Doubles with a Chat Application
Line 66: Chapter 2
Line 67: [ 33 ]
Line 68: But if we make our tests pass with test doubles, how do we avoid shipping software that is
Line 69: just a bunch of fake entities? That's why it's important to have various layers of tests – the
Line 70: more you move up through the layers, the fewer test doubles you should have, all the way
Line 71: up to end-to-end tests, which should involve no test doubles at all.
Line 72: Test-driven development also suggests that we should write the minimum amount of code
Line 73: necessary to make a test pass and it's a very important rule because, otherwise, you could
Line 74: easily end up writing code whose development has to be driven by other new tests.
Line 75: That means that to have a fairly high-level test (such as an acceptance test) pass, we are
Line 76: probably going to involve many test doubles at the beginning (as our software is still
Line 77: empty). So when are we expected to replace those test doubles with real objects?
Line 78: That's where Test-Driven Development by Example by Kent Beck suggests relying on a TODO
Line 79: list. As you write your code, you should write down anything that you think you need to
Line 80: improve/support/replace. And before moving forward to writing the next acceptance test,
Line 81: the TODO list should be completed.
Line 82: In your TODO list, you can record entries to replace the test doubles with real objects. As a
Line 83: consequence, we are going to write tests that verify the behaviors of those real objects and,
Line 84: subsequently, their implementation, finally replacing them with the real objects themselves
Line 85: in our original acceptance test to confirm it still passes.
Line 86: To showcase how test doubles can help us during TDD, we are going to build a chat
Line 87: application by relying on the most common kind of test doubles.
Line 88: Starting our chat application with TDD
Line 89: When you start the development of a new feature, the first test you might want to write is
Line 90: the primary acceptance test – the one that helps you define "this is what I want to achieve."
Line 91: Acceptance tests expose the components we need to create and the behaviors they need to
Line 92: have, allowing us to move forward by designing the development tests for those
Line 93: components and thus writing down unit and integration tests.
Line 94: In the case of the chat application, our acceptance test will probably be a test where one
Line 95: user can send a message and another user can receive it:
Line 96: import unittest
Line 97: class TestChatAcceptance(unittest.TestCase):
Line 98:     def test_message_exchange(self):
Line 99:         user1 = ChatClient("John Doe")
Line 100:         user2 = ChatClient("Harry Potter")
Line 101: 
Line 102: --- 페이지 44 ---
Line 103: Test Doubles with a Chat Application
Line 104: Chapter 2
Line 105: [ 34 ]
Line 106:         user1.send_message("Hello World")
Line 107:         messages = user2.fetch_messages()
Line 108:         assert messages == ["John Doe: Hello World"]
Line 109: if __name__ == '__main__':
Line 110:     unittest.main()
Line 111: Our test makes clear that we want two ChatClient instances that exchange a message. The
Line 112: first sends a new message and the second is able to fetch it and see it.
Line 113: Now, we made our mind up about the fact that we want two chat clients to exist: one that
Line 114: sends messages and another that can receive them. We will surely evolve this simple vision
Line 115: of our application in the future, but so far it has helped us set some clear expectations.
Line 116: The ChatClient class doesn't yet exist, by the way. We vaguely know that we want it to be
Line 117: able to send messages and fetch messages, but we still lack tons of details about what it
Line 118: should do and how it should do it. So the next step is to start clarifying what we want those
Line 119: capabilities to look like.
Line 120: If we run our acceptance test, by running the 01_chat_acceptance.py file where we
Line 121: saved the previous test case, it will fail with an error:
Line 122: $ python 01_chat_acceptance.py TestChatAcceptance
Line 123: E
Line 124: ======================================================================
Line 125: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 126: ----------------------------------------------------------------------
Line 127: Traceback (most recent call last):
Line 128:   File "01_chat_acceptance.py", line 5, in test_message_exchange
Line 129:     user1 = ChatClient("John Doe")
Line 130: NameError: global name 'ChatClient' is not defined
Line 131: ----------------------------------------------------------------------
Line 132: Ran 1 test in 0.000s
Line 133: FAILED (errors=1)
Line 134: By complaining that ChatClient is not defined, it will point out that our next step should
Line 135: probably be writing a client.
Line 136: 
Line 137: --- 페이지 45 ---
Line 138: Test Doubles with a Chat Application
Line 139: Chapter 2
Line 140: [ 35 ]
Line 141: So we know that the first thing we have to start with is creating a ChatClient and, as we
Line 142: want that client to be able to remember the nickname of the user, we need to ensure that it's
Line 143: aware of the nickname of the user. So let's start by writing a development test to ensure that
Line 144: ChatClient will able to do so:
Line 145: class TestChatClient(unittest.TestCase):
Line 146:     def test_nickname(self):
Line 147:         client = ChatClient("User 1")
Line 148:         assert client.nickname == "User 1"
Line 149: At this point, we already know that both our acceptance test and our development test will
Line 150: fail, as we haven't yet written any implementation. But let's confirm our test suite does
Line 151: what we expect:
Line 152: $ python 01_chat_acceptance.py TestChatClient
Line 153: E
Line 154: ======================================================================
Line 155: ERROR: test_nickname (__main__.TestChatClient)
Line 156: ----------------------------------------------------------------------
Line 157: Traceback (most recent call last):
Line 158:   File "01_chat_acceptance.py", line 16, in test_nickname
Line 159:     client = ChatClient("User 1")
Line 160: NameError: global name 'ChatClient' is not defined
Line 161: ----------------------------------------------------------------------
Line 162: Ran 1 test in 0.000s
Line 163: FAILED (errors=1)
Line 164: Obviously, our test is failing with the fact that ChatClient doesn't even exist, so let's 
Line 165: implement the ChatClient class itself and make it aware of the nickname used:
Line 166: class ChatClient:
Line 167:     def __init__(self, nickname):
Line 168:         self.nickname = nickname
Line 169: Now, rerunning our test unit should be successful, as we created the ChatClient and we
Line 170: made it able to keep the memory of the user's nickname that is connected to our chat
Line 171: application:
Line 172: $ python 01_dummy.py TestChatClient
Line 173: .
Line 174: ----------------------------------------------------------------------
Line 175: Ran 1 test in 0.000s
Line 176: OK
Line 177: 
Line 178: --- 페이지 46 ---
Line 179: Test Doubles with a Chat Application
Line 180: Chapter 2
Line 181: [ 36 ]
Line 182: So our unit test now passes, and we can move forward. What needs to be done next? To
Line 183: know that, we just have to go back and run our acceptance test again. Does it pass? Does it
Line 184: need any other unit to be developed?
Line 185: $ python 01_chat_acceptance.py TestChatAcceptance
Line 186: E
Line 187: ======================================================================
Line 188: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 189: ----------------------------------------------------------------------
Line 190: Traceback (most recent call last):
Line 191:   File "01_chat_acceptance.py", line 8, in test_message_exchange
Line 192:     user1.send_message("Hello World")
Line 193: AttributeError: ChatClient instance has no attribute 'send_message'
Line 194: ----------------------------------------------------------------------
Line 195: Ran 1 test in 0.000s
Line 196: FAILED (errors=1)
Line 197: Running our acceptance test again, it has now complained about the
Line 198: ChatClient.send_message method, so now we know that we need to work on that unit
Line 199: next. As is usually expected with a TDD approach, we can start the work with a unit test.
Line 200: So let's extend our TestChatClient case with one additional test_send_message test:
Line 201: class TestChatClient(unittest.TestCase):
Line 202:     def test_nickname(self):
Line 203:         client = ChatClient("User 1")
Line 204:         assert client.nickname == "User 1"
Line 205:     def test_send_message(self):
Line 206:         client = ChatClient("User 1")
Line 207:         sent_message = client.send_message("Hello World")
Line 208:         assert sent_message == "User 1: Hello World"
Line 209: The new test_send_message test creates a client for User 1 and then sends a message to
Line 210: the chat from that user, verifying that the outgoing message was actually submitted as a
Line 211: message sent by that user.
Line 212: Going back to our shell and rerunning our tests for the ChatClient component will tell us
Line 213: that we now have to write that method to satisfy the test:
Line 214: $ python 01_chat_acceptance.py TestChatClient
Line 215: .E
Line 216: ======================================================================
Line 217: ERROR: test_send_message (__main__.TestChatClient)
Line 218: 
Line 219: --- 페이지 47 ---
Line 220: Test Doubles with a Chat Application
Line 221: Chapter 2
Line 222: [ 37 ]
Line 223: ----------------------------------------------------------------------
Line 224: Traceback (most recent call last):
Line 225:   File "01_chat_acceptance.py", line 22, in test_send_message
Line 226:     sent_message = client.send_message("Hello World")
Line 227: AttributeError: ChatClient instance has no attribute 'send_message'
Line 228: ----------------------------------------------------------------------
Line 229: Ran 2 tests in 0.000s
Line 230: FAILED (errors=1)
Line 231: So let's move back to development again and add the send_message method to our
Line 232: component. We already decided that it has to accept the message, prefix it with the sender's
Line 233: nickname, and probably send it to all the other users:
Line 234: class ChatClient:
Line 235:     def __init__(self, nickname):
Line 236:         self.nickname = nickname
Line 237:     def send_message(self, message):
Line 238:         sent_message = "{}: {}".format(self.nickname, message)
Line 239:         self.connection.broadcast(message)
Line 240:         return sent_message
Line 241: Let's rerun our test case for the component to confirm that we now satisfy it:
Line 242: $ python 01_chat_acceptance.py TestChatClient
Line 243: .E
Line 244: ======================================================================
Line 245: ERROR: test_send_message (__main__.TestChatClient)
Line 246: ----------------------------------------------------------------------
Line 247: Traceback (most recent call last):
Line 248:   File "01_chat_acceptance.py", line 22, in test_send_message
Line 249:     sent_message = client.send_message("Hello World")
Line 250:   File "01_chat_acceptance.py", line 32, in send_message
Line 251:     self.connection.broadcast(message)
Line 252: AttributeError: ChatClient instance has no attribute 'connection'
Line 253: ----------------------------------------------------------------------
Line 254: Ran 2 tests in 0.000s
Line 255: FAILED (errors=1)
Line 256: 
Line 257: --- 페이지 48 ---
Line 258: Test Doubles with a Chat Application
Line 259: Chapter 2
Line 260: [ 38 ]
Line 261: Our test failed again – it told us that our ChatClient.send_message method is now
Line 262: there, and the test was able to call it, but it's not yet working.
Line 263: This is because we actually went a bit further in having the client already send the
Line 264: messages through the network before the need was exposed by our tests. But we already
Line 265: knew that's what we actually wanted to do anyway, and it actually serves the purpose of
Line 266: introducing our first test double: dummy objects.
Line 267: Using dummy objects
Line 268: A dummy is an object that does nothing. It just serves the purpose of being passed around
Line 269: as an argument and not making the code crash because we lack an object. But its
Line 270: implementation is totally empty; it does nothing.
Line 271: In our chat application, we need a connection object to be able to send messages from one
Line 272: client to the other. We have not yet implemented that connection object, and for now, we
Line 273: are focused on having the ChatClient.send_message test pass, but how can we make it
Line 274: pass if we don't yet have a working Connection object the client relies on?
Line 275: That's where dummy objects come in handy. They replace other objects, faking that they
Line 276: can do their job, but in reality, they do absolutely nothing.
Line 277: A dummy object for our Connection class would currently look like this:
Line 278: class _DummyConnection:
Line 279:     def broadcast(*args, **kwargs):
Line 280:         pass
Line 281: In practice, it's an object that provides a broadcast method but does absolutely nothing.
Line 282: Dummy objects are just fillers for the arguments of properties that another object needs.
Line 283: They are frequently not even used at all and just provide a pass-through to satisfy some
Line 284: required argument.
Line 285: Now we can adapt our previous TestChatClient.test_send_message test to use a
Line 286: dummy for the connection by setting client.connection to _DummyConnection. That
Line 287: should make our test pass as we broke the dependency over a real connection:
Line 288: class TestChatClient(unittest.TestCase):
Line 289:     ...
Line 290:     def test_send_message(self):
Line 291:         client = ChatClient("User 1")
Line 292:         client.connection = _DummyConnection()
Line 293: 
Line 294: --- 페이지 49 ---
Line 295: Test Doubles with a Chat Application
Line 296: Chapter 2
Line 297: [ 39 ]
Line 298:         sent_message = client.send_message("Hello World")
Line 299:         assert sent_message == "User 1: Hello World"
Line 300: Another convenient way to implement dummy objects is just to use the Python
Line 301: unittest.mock module. In the Using mocks section, will see that, while the name is pretty
Line 302: specific, the unittest.mock.Mock object is in practice able to serve all test doubles cases
Line 303: introduced in this chapter. It just depends on which features we use and which we ignore.
Line 304: So in our previous example, we can just replace our _DummyConnection
Line 305: with unittest.mock.Mock and avoid having to implement a dedicated class at all:
Line 306: import unittest.mock
Line 307: class TestChatClient(unittest.TestCase):
Line 308:     ...
Line 309:     def test_send_message(self):
Line 310:         client = ChatClient("User 1")
Line 311:         client.connection = unittest.mock.Mock()
Line 312:         sent_message = client.send_message("Hello World")
Line 313:         assert sent_message == "User 1: Hello World"
Line 314: If we run our tests again for TestChatClient, we should see that we finally succeeded in
Line 315: making them pass:
Line 316: $ python 02_chat_dummy.py TestChatClient
Line 317: ..
Line 318: ----------------------------------------------------------------------
Line 319: Ran 2 tests in 0.000s
Line 320: OK
Line 321: Does that mean that our work is done? Not yet, because checking our acceptance test
Line 322: (TestChatAcceptance) again will tell us that we are not yet there:
Line 323: $ python 02_chat_dummy.py TestChatAcceptance
Line 324: E
Line 325: ======================================================================
Line 326: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 327: ----------------------------------------------------------------------
Line 328: Traceback (most recent call last):
Line 329:   File "02_chat_dummy.py", line 8, in test_message_exchange
Line 330:     user1.send_message("Hello World")
Line 331:   File "02_chat_dummy.py", line 39, in send_message
Line 332:     self.connection.broadcast(message)
Line 333: 
Line 334: --- 페이지 50 ---
Line 335: Test Doubles with a Chat Application
Line 336: Chapter 2
Line 337: [ 40 ]
Line 338: AttributeError: ChatClient instance has no attribute 'connection'
Line 339: ----------------------------------------------------------------------
Line 340: Ran 1 test in 0.000s
Line 341: FAILED (errors=1)
Line 342: We implemented the ChatClient.send_message method and it passes its test, but our
Line 343: acceptance test is now reminding us that we still have to implement the Connection object
Line 344: as we just used a double for it in the send_message test.
Line 345: The connection object is the next thing we are going to implement, but the connection will
Line 346: need to be able to reach a server that can route the messages to all connected clients, and
Line 347: making our tests pass a DummyConnection won't be enough anymore. We will have to
Line 348: actually see the messages and thus using stubs will be necessary.
Line 349: Replacing components with stubs
Line 350: Our connection object will be in charge of making our message available to all the other
Line 351: clients and, probably in the near future, letting us know when there are new messages.
Line 352: The first step to drive the development of our Connection object is to start building a
Line 353: TestConnection test case and a test_broadcast test to make our expectations of the
Line 354: implementation clear:
Line 355: class TestConnection(unittest.TestCase):
Line 356:     def test_broadcast(self):
Line 357:         c = Connection(("localhost", 9090))
Line 358:         c.broadcast("some message")
Line 359:         assert c.get_messages()[-1] == "some message"
Line 360: Our test specifies that once we've sent a message in broadcast, the latest entry in the
Line 361: messages visible in the chat should be our own message (as it was the last message sent).
Line 362: Obviously, running our test now will fail because the Connection object doesn't exist at
Line 363: all, so let's make one.
Line 364: A possible idea for how to implement cross-client communication is to use a
Line 365: multiprocessing.managers.SyncManager and store the messages in a list that is
Line 366: accessible by all the clients that connect to it.
Line 367: 
Line 368: --- 페이지 51 ---
Line 369: Test Doubles with a Chat Application
Line 370: Chapter 2
Line 371: [ 41 ]
Line 372: The only thing we will have to do is register a single Connection.get_messages
Line 373: identifier in the manager. The purpose of that identifier will be to return the list of
Line 374: messages that are currently in the chat so that ChatClient can read them or append new
Line 375: messages:
Line 376: from multiprocessing.managers import SyncManager
Line 377: class Connection(SyncManager):
Line 378:     def __init__(self, address):
Line 379:         self.register("get_messages")
Line 380:         super().__init__(address=address, authkey=b'mychatsecret')
Line 381:         self.connect()
Line 382: Then the Connection.broadcast method will be as simple as just getting the messages
Line 383: through Connection.get_messages and appending a new message to them:
Line 384: from multiprocessing.managers import SyncManager
Line 385: class Connection(SyncManager):
Line 386:     def __init__(self, address):
Line 387:         self.register("get_messages")
Line 388:         super().__init__(address=address, authkey=b'mychatsecret')
Line 389:         self.connect()
Line 390:     def broadcast(self, message):
Line 391:         messages = self.get_messages()
Line 392:         messages.append(message)
Line 393: Now our connection object is done and it provides a broadcast method, so we can
Line 394: verify that it does add a new message to our chat by rerunning our test:
Line 395: $ python 03_chat_stubs.py TestConnection
Line 396: E
Line 397: ======================================================================
Line 398: ERROR: test_broadcast (__main__.TestConnection)
Line 399: ----------------------------------------------------------------------
Line 400: Traceback (most recent call last):
Line 401:   File "03_chat_stubs.py", line 33, in test_broadcast
Line 402:     c = Connection(("localhost", 9090))
Line 403:   File "03_chat_stubs.py", line 56, in __init__
Line 404:     self.connect()
Line 405:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 532, in
Line 406: connect
Line 407:     conn = Client(self._address, authkey=self._authkey)
Line 408:   File "/usr/lib/python3.7/multiprocessing/connection.py", line 492, in
Line 409: Client
Line 410:     c = SocketClient(address)
Line 411: 
Line 412: --- 페이지 52 ---
Line 413: Test Doubles with a Chat Application
Line 414: Chapter 2
Line 415: [ 42 ]
Line 416:   File "/usr/lib/python3.7/multiprocessing/connection.py", line 619, in
Line 417: SocketClient
Line 418:     s.connect(address)
Line 419: ConnectionRefusedError: [Errno 111] Connection refused
Line 420: ----------------------------------------------------------------------
Line 421: Ran 1 test in 0.003s
Line 422: FAILED (errors=1)
Line 423: Sadly, our test failed, because we still don't have a server, so the connection couldn't get
Line 424: created because there is no server it could connect to. Until we have a server, we already
Line 425: know we can replace our Connection.connect method with a dummy in our test and
Line 426: retry:
Line 427: class TestConnection(unittest.TestCase):
Line 428:     def test_broadcast(self):
Line 429:         with unittest.mock.patch.object(Connection, "connect"):
Line 430:             c = Connection(("localhost", 9090))
Line 431:         c.broadcast("some message")
Line 432:         assert c.get_messages()[-1] == "some message"
Line 433: unittest.mock.patch.object is a convenience method that allows us to replace a
Line 434: method or attribute of an object with a unittest.mock.Mock for the whole duration of the
Line 435: code block within the context. So in this case, we disabled the Connection.connect
Line 436: method so that the connection could be created without a server.
Line 437: Okay, so now we expect our test to finally pass, right? Let's try to run it once more:
Line 438: $ python 03_chat_stubs.py TestConnection
Line 439: F
Line 440: ======================================================================
Line 441: FAIL: test_broadcast (__main__.TestConnection)
Line 442: ----------------------------------------------------------------------
Line 443: Traceback (most recent call last):
Line 444:   File "03_chat_stubs.py", line 36, in test_broadcast
Line 445:     c.broadcast("some message")
Line 446:   File "03_chat_stubs.py", line 60, in broadcast
Line 447:     messages = self.get_messages()
Line 448:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 724, in temp
Line 449:     token, exp = self._create(typeid, *args, **kwds)
Line 450:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 606, in
Line 451: _create
Line 452:     assert self._state.value == State.STARTED, 'server not yet started'
Line 453: AssertionError: server not yet started
Line 454: 
Line 455: --- 페이지 53 ---
Line 456: Test Doubles with a Chat Application
Line 457: Chapter 2
Line 458: [ 43 ]
Line 459: ----------------------------------------------------------------------
Line 460: Ran 1 test in 0.001s
Line 461: FAILED (failures=1)
Line 462: Not really. The object was successfully created, but once we tried to get the chat messages
Line 463: to append the new one, it failed, as there was no server we could connect to.
Line 464: But we do really need the messages, otherwise, the whole test has no way to verify that the
Line 465: message was added to the existing messages and thus sent. So what can we do?
Line 466: Here is where stubs come in handy. Stubs provide canned answers, replacing those pieces
Line 467: of the software with the ready-made state or answer that we could have got if it had run for
Line 468: real. So we are going to replace Connection.get_messages with a stub that returns an 
Line 469: empty list and see that everything works as we expected:
Line 470: class TestConnection(unittest.TestCase):
Line 471:     def test_broadcast(self):
Line 472:         with unittest.mock.patch.object(Connection, "connect"):
Line 473:             c = Connection(("localhost", 9090))
Line 474:         with unittest.mock.patch.object(c, "get_messages",
Line 475:                                          return_value=[]):
Line 476:             c.broadcast("some message")
Line 477:             assert c.get_messages()[-1] == "some message"
Line 478: You can now see that, after the first call to unittest.mock.patch.object, where we
Line 479: replaced the connect method with a dummy one, we now have a second one. In this one,
Line 480: we replace the get_messages method of the newly made Connection instance with one
Line 481: that returns a canned response of an empty list, simulating this being the first message that
Line 482: was sent to the chat.
Line 483: Finally, running our tests again will confirm that the Connection.broadcast method is
Line 484: doing what we expected:
Line 485: $ python 03_chat_stubs.py TestConnection
Line 486: .
Line 487: ----------------------------------------------------------------------
Line 488: Ran 1 test in 0.001s
Line 489: OK
Line 490: Okay, so now we have ChatClient and Connection tests passing, so we clearly did our
Line 491: job, right?
Line 492: 
Line 493: --- 페이지 54 ---
Line 494: Test Doubles with a Chat Application
Line 495: Chapter 2
Line 496: [ 44 ]
Line 497: Let's check whether that's true by running our acceptance test:
Line 498: $ python 03_chat_stubs.py TestChatAcceptance
Line 499: E
Line 500: ======================================================================
Line 501: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 502: ----------------------------------------------------------------------
Line 503: Traceback (most recent call last):
Line 504:   File "03_chat_stubs.py", line 10, in test_message_exchange
Line 505:     user1.send_message("Hello World")
Line 506:   File "03_chat_stubs.py", line 49, in send_message
Line 507:     self.connection.broadcast(message)
Line 508: AttributeError: 'ChatClient' object has no attribute 'connection'
Line 509: ----------------------------------------------------------------------
Line 510: Ran 1 test in 0.000s
Line 511: FAILED (errors=1)
Line 512: Not yet... We made the Connection object, but we clearly forgot to bind it to our
Line 513: ChatClient.
Line 514: So let's move forward by binding ChatClient with Connection and introducing spies as
Line 515: a way to verify that the ChatClient is using the Connection the way we actually expect it
Line 516: to.
Line 517: Checking behaviors with spies
Line 518: We know that ChatClient must use a connection to send and receive the messages. So the
Line 519: next thing we have to do to make sure our test_message_exchange test passes is to make
Line 520: sure that the connection exists and is used. But we don't want to establish a connection
Line 521: every time a ChatClient is created, so the idea is to create a connection through a method
Line 522: that lazily makes them when they're needed the first time.
Line 523: We will call this method ChatClient._get_connection and we want to make sure that
Line 524: ChatClient will actually use the connection provided by that method. To verify that
Line 525: ChatClient uses the provided connection, we are going to set up a test with a spy, a kind
Line 526: of dummy object that, instead of doing nothing, actually records how it was called (if it
Line 527: was) and with which arguments.
Line 528: 
Line 529: --- 페이지 55 ---
Line 530: Test Doubles with a Chat Application
Line 531: Chapter 2
Line 532: [ 45 ]
Line 533: As we did when setting up the stub, we are going to use unittest.mock.patch to replace
Line 534: the ChatClient._get_connection method with a stub that, instead of returning the
Line 535: connection, returns the spy. Then we are going to check through the spy that the
Line 536: ChatClient.send_message method actually used the connection we returned to send the
Line 537: message:
Line 538:     def test_client_connection(self):
Line 539:         client = ChatClient("User 1")
Line 540:         connection_spy = unittest.mock.MagicMock()
Line 541:         with unittest.mock.patch.object(client, "_get_connection",
Line 542:                                         return_value=connection_spy):
Line 543:             client.send_message("Hello World")
Line 544:         # assert that the spy was called with the
Line 545:         # expected data to broadcast.
Line 546:         connection_spy.broadcast.assert_called_with(("User 1:
Line 547:                                                       Hello World"))
Line 548: Now if we call our test, it's going to fail because we never made a
Line 549: ChatClient._get_connection method and thus it can't be replaced with the stub:
Line 550: $ python 04_chat_spies.py TestChatClient
Line 551: E..
Line 552: ======================================================================
Line 553: ERROR: test_client_connection (__main__.TestChatClient)
Line 554: ----------------------------------------------------------------------
Line 555: Traceback (most recent call last):
Line 556:   File "04_chat_spies.py", line 35, in test_client_connection
Line 557:     return_value=connection_spy):
Line 558:   File "/usr/lib/python3.7/unittest/mock.py", line 1319, in __enter__
Line 559:     original, local = self.get_original()
Line 560:   File "/usr/lib/python3.7/unittest/mock.py", line 1293, in get_original
Line 561:     "%s does not have the attribute %r" % (target, name)
Line 562: AttributeError: <__main__.ChatClient object at 0x7f962dd8d050> does not
Line 563: have the attribute '_get_connection'
Line 564: ----------------------------------------------------------------------
Line 565: Ran 3 tests in 0.001s
Line 566: FAILED (errors=1)
Line 567: 
Line 568: --- 페이지 56 ---
Line 569: Test Doubles with a Chat Application
Line 570: Chapter 2
Line 571: [ 46 ]
Line 572: So let's go to our ChatClient class and let's add the _get_connection method, which is
Line 573: going to return a new Connection object against a predefined port where the server will 
Line 574: listen locally (normally, we would make the port and host for a service configurable, but
Line 575: given that it's just a simple chat application for our own use, we can take for granted that
Line 576: the server will run on a known port and host):
Line 577: class ChatClient:
Line 578:     def __init__(self, nickname):
Line 579:         self.nickname = nickname
Line 580:     def send_message(self, message):
Line 581:         sent_message = "{}: {}".format(self.nickname, message)
Line 582:         self.connection.broadcast(message)
Line 583:         return sent_message
Line 584:     def _get_connection(self):
Line 585:         return Connection(("localhost", 9090))
Line 586: Great – so our test should be happy now! The stub can be put in place, so let's see what
Line 587: happens when running our tests again:
Line 588: $ python 04_chat_spies.py TestChatClient
Line 589: E..
Line 590: ======================================================================
Line 591: ERROR: test_client_connection (__main__.TestChatClient)
Line 592: ----------------------------------------------------------------------
Line 593: Traceback (most recent call last):
Line 594:   File "04_chat_spies.py", line 36, in test_client_connection
Line 595:     client.send_message("Hello World")
Line 596:   File "04_chat_spies.py", line 83, in send_message
Line 597:     self.connection.broadcast(message)
Line 598: AttributeError: 'ChatClient' object has no attribute 'connection'
Line 599: ----------------------------------------------------------------------
Line 600: Ran 3 tests in 0.001s
Line 601: FAILED (errors=1)
Line 602: Okay, we made the _get_connection but the ChatClient never calls it... So the object is
Line 603: still missing a connection attribute.
Line 604: We know we want this attribute to lazily create the connection, so we are going to define a
Line 605: property that calls _get_connection the first time it's accessed:
Line 606: class ChatClient:
Line 607:     def __init__(self, nickname):
Line 608:         self.nickname = nickname
Line 609: 
Line 610: --- 페이지 57 ---
Line 611: Test Doubles with a Chat Application
Line 612: Chapter 2
Line 613: [ 47 ]
Line 614:         self._connection = None
Line 615:     def send_message(self, message):
Line 616:         sent_message = "{}: {}".format(self.nickname, message)
Line 617:         self.connection.broadcast(message)
Line 618:         return sent_message
Line 619:     @property
Line 620:     def connection(self):
Line 621:         if self._connection is None:
Line 622:             self._connection = self._get_connection()
Line 623:         return self._connection
Line 624:     @connection.setter
Line 625:     def connection(self, value):
Line 626:         if self._connection is not None:
Line 627:             self._connection.close()
Line 628:         self._connection = value
Line 629:     def _get_connection(self):
Line 630:         return Connection(("localhost", 9090))
Line 631: Now when ChatClient.connection is accessed, as ChatClient._connection will be
Line 632: None, the ChatClient._get_connection method will be called so that a new connection
Line 633: can be created.
Line 634: All the pieces should be in place now! So let's see if our test finally passes:
Line 635: $ python 04_chat_spies.py TestChatClient
Line 636: F..
Line 637: ======================================================================
Line 638: FAIL: test_client_connection (__main__.TestChatClient)
Line 639: ----------------------------------------------------------------------
Line 640: Traceback (most recent call last):
Line 641:   File "04_chat_spies.py", line 38, in test_client_connection
Line 642:     assert connection_spy.broadcast.assert_called_with(("User 1: Hello
Line 643: World"))
Line 644:   File "/usr/lib/python3.7/unittest/mock.py", line 873, in
Line 645: assert_called_with
Line 646:     raise AssertionError(_error_message()) from cause
Line 647: AssertionError: Expected call: broadcast('User 1: Hello World')
Line 648: Actual call: broadcast('Hello World')
Line 649: ----------------------------------------------------------------------
Line 650: Ran 3 tests in 0.001s
Line 651: FAILED (failures=1)
Line 652: 
Line 653: --- 페이지 58 ---
Line 654: Test Doubles with a Chat Application
Line 655: Chapter 2
Line 656: [ 48 ]
Line 657: Unexpectedly, our test failed. The good news is that the connection itself worked. The test
Line 658: was able to put in place the stub, and the spy was used.
Line 659: The bad news is that our test actually discovered a bug that our previous
Line 660: TestChatClient.test_send_message test was unable to spot. In the current
Line 661: implementation of ChatClient.send_message, we build the message with the name of
Line 662: the user who wrote it, but we broadcast the one without a name. So none of the other users
Line 663: reading the chat will ever know who wrote that message!
Line 664: class ChatClient:
Line 665:     ...
Line 666:     def send_message(self, message):
Line 667:         sent_message = "{}: {}".format(self.nickname, message)
Line 668:         self.connection.broadcast(message)
Line 669:         return sent_message
Line 670: What we want to do here is change the send_message method so that the message 
Line 671: broadcast is the one with the name of the author, the sent_message variable, instead of
Line 672: the message one:
Line 673: class ChatClient:
Line 674:     ...
Line 675:     def send_message(self, message):
Line 676:         sent_message = "{}: {}".format(self.nickname, message)
Line 677:         self.connection.broadcast(sent_message)
Line 678:         return sent_message
Line 679: Now that we have fixed that bug, our test can finally pass and confirm that our
Line 680: ChatClient has the connection in place and properly sends messages through it:
Line 681: $ python 04_chat_spies.py TestChatClient
Line 682: ...
Line 683: ----------------------------------------------------------------------
Line 684: Ran 3 tests in 0.001s
Line 685: OK
Line 686: The next step, as usual, is to go back to our acceptance test and ask what's left to do:
Line 687: $ python 04_chat_spies.py TestChatAcceptance
Line 688: E
Line 689: ======================================================================
Line 690: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 691: ----------------------------------------------------------------------
Line 692: Traceback (most recent call last):
Line 693: 
Line 694: --- 페이지 59 ---
Line 695: Test Doubles with a Chat Application
Line 696: Chapter 2
Line 697: [ 49 ]
Line 698:   File "04_chat_spies.py", line 10, in test_message_exchange
Line 699:     user1.send_message("Hello World")
Line 700:   File "04_chat_spies.py", line 58, in send_message
Line 701:     self.connection.broadcast(sent_message)
Line 702:   File "04_chat_spies.py", line 64, in connection
Line 703:     self._connection = self._get_connection()
Line 704:   File "04_chat_spies.py", line 74, in _get_connection
Line 705:     return Connection(("localhost", 9090))
Line 706:   File "04_chat_spies.py", line 82, in __init__
Line 707:     self.connect()
Line 708:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 532, in
Line 709: connect
Line 710:     conn = Client(self._address, authkey=self._authkey)
Line 711:   File "/usr/lib/python3.7/multiprocessing/connection.py", line 492, in
Line 712: Client
Line 713:     c = SocketClient(address)
Line 714:   File "/usr/lib/python3.7/multiprocessing/connection.py", line 619, in
Line 715: SocketClient
Line 716:     s.connect(address)
Line 717: ConnectionRefusedError: [Errno 111] Connection refused
Line 718: ----------------------------------------------------------------------
Line 719: Ran 1 test in 0.001s
Line 720: FAILED (errors=1)
Line 721: Our acceptance test proves that our client is trying to connect to the server as expected,
Line 722: which is great!
Line 723: The problem is that, as we already know, there is no such server. So our acceptance test
Line 724: cannot pass as it can't connect to a server and verify that the client is actually able to send
Line 725: and receive messages.
Line 726: But before moving forward and looking at how to implement our server, let's introduce the
Line 727: concept of mocks, which gather in themselves all the powers of the previously introduced
Line 728: test doubles.
Line 729: Using mocks
Line 730: As you've probably noticed, when we use dummy objects, stubs, or spies, we always end
Line 731: up working with the unittest.mock module. That's because mock objects could be seen
Line 732: as dummy objects that provide some stubs mixed with spies.
Line 733: 
Line 734: --- 페이지 60 ---
Line 735: Test Doubles with a Chat Application
Line 736: Chapter 2
Line 737: [ 50 ]
Line 738: Mocks are able to be passed around and they usually do nothing, behaving pretty much
Line 739: like dummy objects.
Line 740: If we had a read_file function accepting a file object with a read method, we could
Line 741: provide a Mock instead of a real file; Mock.read will just do nothing:
Line 742: >>> def read_file(f):
Line 743: ...     print("READING ALL FILE")
Line 744: ...     return f.read()
Line 745: ...
Line 746: >>> from unittest.mock import Mock
Line 747: >>> m = Mock()
Line 748: >>> read_file(m)
Line 749: READING ALL FILE
Line 750: If instead of doing nothing, we want to make it act like a stub, we can provide a canned
Line 751: response to have Mock.read return a predefined string:
Line 752: >>> m.read.return_value = "Hello World"
Line 753: >>> print(read_file(m))
Line 754: Hello World
Line 755: If we don't want to just fill in the place of other real objects by replacing them with
Line 756: dummies and stubs, we can also use mocks to track what happened to them, so they are
Line 757: able to behave like a spy too:
Line 758: >>> m.read.call_count
Line 759: 2
Line 760: But what makes them mocks is that they can test the behavior of software. Stubs, spies, and
Line 761: dummies are all about state. They provide a state for software consumption when you are
Line 762: injecting a known state into software or for test consumption when you are using a spy to
Line 763: keep the state of calls.
Line 764: Mocks are usually meant to keep track of behaviors. They usually crash when the software
Line 765: hasn't done what you expected. So they are usually meant to assert that they were used in a
Line 766: specific expected way, which confirms that the software behaved as we wished.
Line 767: For example, we can check that the read method on the Mock object was actually called:
Line 768: >>> m.read.assert_called_with()
Line 769: 
Line 770: --- 페이지 61 ---
Line 771: Test Doubles with a Chat Application
Line 772: Chapter 2
Line 773: [ 51 ]
Line 774: If we wanted to verify that read_file was calling f.read() with a specific argument, we
Line 775: could have asked the mock to verify that it was used. If the method wasn't called, the
Line 776: assertion would have failed with an AssertionError:
Line 777: >>> m.read.assert_called_with("some argument")
Line 778: Traceback (most recent call last):
Line 779:   File "<stdin>", line 1, in <module>
Line 780:   File "/usr/lib/python3.7/unittest/mock.py", line 873, in
Line 781: assert_called_with
Line 782:     raise AssertionError(_error_message()) from cause
Line 783: AssertionError: Expected call: read('some argument')
Line 784: Actual call: read()
Line 785: If it wasn't called due to a bug or incomplete implementation, the assertion would have
Line 786: detected that and we could have addressed the behavior of read_file to make it work as
Line 787: we wanted.
Line 788: Now that we know about dummies, stubs, spies, and mocks, we know that there are tons of
Line 789: ways to test our software without having to rely on complete and fully functional
Line 790: components. And we know that our test suite has to be fast, easy to debug, and must
Line 791: require minimum dependencies with minimum influence from the external system.
Line 792: So a real working server would mean having to start a separate server process every time
Line 793: we want to run our tests and would mean slowing down tests because they have to go
Line 794: through a real network connection.
Line 795: For the next step, instead of implementing a real server, we are going to introduce the
Line 796: concept of fakes and try to get a fake server that makes our acceptance test pass.
Line 797: Replacing dependencies with fakes
Line 798: Fakes are replacements for real dependencies that are good enough to fake that they are the
Line 799: real deal. Fakes are frequently involved in the goal of simplifying test suite dependencies or
Line 800: improving the performance of a test suite. For example, if your software depends on a
Line 801: third-party weather forecasting API available in the cloud, it's not very convenient to
Line 802: perform a real network connection to the remote API server. The best-case scenario is it will
Line 803: be very slow, and the worst-case scenario is you could get throttled or even banned for
Line 804: doing too many API requests in too short a time, as your test suite could easily reach
Line 805: hundreds or thousands of tests.
Line 806: The most widespread kind of fakes are usually in-memory databases as they simplify the
Line 807: need to set up and tear down a real database management system for the sole reason of
Line 808: running your tests.
Line 809: 
Line 810: --- 페이지 62 ---
Line 811: Test Doubles with a Chat Application
Line 812: Chapter 2
Line 813: [ 52 ]
Line 814: In our case, we don't want to have the need to start a chat server every time we want to run
Line 815: the test suite of our chat application, so we are going to provide a fake server and fake
Line 816: connection that will replace the real networking-based connection.
Line 817: Now that we have our TestConnection case, which verifies that the connection does what
Line 818: we want, how can we verify that it actually works when there is a server on the other side?
Line 819: We can look at how the SyncManager server works and provide a fake replacement simple
Line 820: enough to understand the basic protocol and provide the answers. Thankfully, the
Line 821: SyncManager protocol is very simple. It just receives commands with a set of arguments
Line 822: and responds with a tuple, ("RESPONSE_TYPE", RESPONSE), where RESPONSE_TYPE
Line 823: states whether the response is the returned value for that command or an error.
Line 824: So we can make a FakeServer that provides a FakeServer.send method that will trap
Line 825: the commands that the client is requesting and a FakeServer.recv method that will send
Line 826: back the response to the client:
Line 827: class FakeServer:
Line 828:     def __init__(self):
Line 829:         self.last_command = None
Line 830:         self.last_args = None
Line 831:         self.messages = []
Line 832:     def __call__(self, *args, **kwargs):
Line 833:         # Make the SyncManager think that a new connection was created.
Line 834:         return self
Line 835:     def send(self, data):
Line 836:         # Track any command that was sent to the server.
Line 837:         callid, command, args, kwargs = data
Line 838:         self.last_command = command
Line 839:         self.last_args = args
Line 840:     def recv(self, *args, **kwargs):
Line 841:         # For now we don't support any command, so just error.
Line 842:         return "#ERROR", ValueError("%s - %r" % (
Line 843:             self.last_command,self.last_args)
Line 844:         )
Line 845:     def close(self):
Line 846:         pass
Line 847: The very first basic implementation of our fake server is only going to respond to any
Line 848: command with an error, so we can track the commands that the client is trying to send to
Line 849: us.
Line 850: 
Line 851: --- 페이지 63 ---
Line 852: Test Doubles with a Chat Application
Line 853: Chapter 2
Line 854: [ 53 ]
Line 855: To test our connection with a server, we are going to add a new
Line 856: test_exchange_with_server test to the TestConnection test case, which will use the
Line 857: provided FakeServer to link two connections together:
Line 858: class TestConnection(unittest.TestCase):
Line 859:     def test_broadcast(self):
Line 860:         ...
Line 861:     def test_exchange_with_server(self):
Line 862:          with unittest.mock.patch(
Line 863:              "multiprocessing.managers.listener_client",
Line 864:              new={"pickle": (None, FakeServer())}
Line 865:          ):
Line 866:             c1 = Connection(("localhost", 9090))
Line 867:             c2 = Connection(("localhost", 9090))
Line 868:             c1.broadcast("connected message")
Line 869:             assert c2.get_messages()[-1] == "connected message"
Line 870: Our test requires some magic through unittest.mock.patch to replace the standard
Line 871: implementation of the server/client communication channel in
Line 872: multiprocessing.managers with our own custom FakeServer. In practice, what we are
Line 873: doing is replacing the "pickle" based communication channel with our own for the duration
Line 874: of the test.
Line 875: Now if we run our test, we should see that our fake server is in place and we should be able
Line 876: to start tracking which commands are exchanged:
Line 877: $ python 05_chat_fakes.py TestConnection
Line 878: .E
Line 879: ======================================================================
Line 880: ERROR: test_exchange_with_server (__main__.TestConnection)
Line 881: ----------------------------------------------------------------------
Line 882: Traceback (most recent call last):
Line 883:   File "05_chat_fakes.py", line 56, in test_exchange_with_server
Line 884:     c1 = Connection(("localhost", 9090))
Line 885:   File "05_chat_fakes.py", line 100, in __init__
Line 886:     self.connect()
Line 887:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 533, in
Line 888: connect
Line 889:     dispatch(conn, None, 'dummy')
Line 890:   File "/usr/lib/python3.7/multiprocessing/managers.py", line 82, in
Line 891: dispatch
Line 892:     raise convert_to_error(kind, result)
Line 893: ValueError: dummy - ()
Line 894: ----------------------------------------------------------------------
Line 895: 
Line 896: --- 페이지 64 ---
Line 897: Test Doubles with a Chat Application
Line 898: Chapter 2
Line 899: [ 54 ]
Line 900: Ran 2 tests in 0.001s
Line 901: FAILED (errors=1)
Line 902: Our test crashed due to an unrecognized 'dummy' command (as we currently recognize no
Line 903: commands) but it proved that our fake server is in place and being used by our
Line 904: Connection object.
Line 905: At this point, we can provide support for the dummy command (which is just used to
Line 906: establish the connection) and see what happens:
Line 907: class FakeServer:
Line 908:     ...
Line 909:     def recv(self, *args, **kwargs):
Line 910:         if self.last_command == "dummy":
Line 911:             return "#RETURN", None
Line 912:         else:
Line 913:             return "#ERROR", ValueError("%s - %r" % (
Line 914:                 self.last_command,self.last_args)
Line 915:             )
Line 916: Running again, the TestConnection test suite will invoke the next command (after the
Line 917: "dummy" one that we just implemented) and thus will complain about the next missing
Line 918: command:
Line 919: $ python 05_chat_fakes.py TestConnection
Line 920: ...
Line 921: ValueError: create - ('get_messages',)
Line 922: By rerunning our test over and over until it stops crashing, we can spot all the commands
Line 923: that our FakeServer has to support in the FakeServe.recv method, and one by one, we
Line 924: can implement enough commands to have a fairly complete implementation of our
Line 925: FakeServer:
Line 926: class FakeServer:
Line 927:     ...
Line 928:     def recv(self, *args, **kwargs):
Line 929:         if self.last_command == "dummy":
Line 930:             return "#RETURN", None
Line 931:         elif self.last_command == "create":
Line 932:             return "#RETURN", ("fakeid", tuple())
Line 933:         elif self.last_command == "append":
Line 934:             self.messages.append(self.last_args[0])
Line 935:             return "#RETURN", None
Line 936:         elif self.last_command == "__getitem__":
Line 937: 
Line 938: --- 페이지 65 ---
Line 939: Test Doubles with a Chat Application
Line 940: Chapter 2
Line 941: [ 55 ]
Line 942:             return "#RETURN", self.messages[self.last_args[0]]
Line 943:         elif self.last_command in ("incref", "decref",
Line 944:                                    "accept_connection"):
Line 945:             return "#RETURN", None
Line 946:         else:
Line 947:             return "#ERROR", ValueError("%s - %r" % (
Line 948:                 self.last_command,self.last_args)
Line 949:             )
Line 950: At this point, our TestConnection should be able to pass using our fake server to
Line 951: establish the link between the two Connection objects:
Line 952: $ python 05_chat_fakes.py TestConnection
Line 953: ..
Line 954: ----------------------------------------------------------------------
Line 955: Ran 2 tests in 0.001s
Line 956: OK
Line 957: Our FakeServer was able to confirm that the two Connection objects are able to talk to
Line 958: each other and see the messages that the other one has broadcast. And we were able to do
Line 959: so without the need to actually start a server instance, listen on the network for the chat
Line 960: connections, and handle that.
Line 961: While fakes are usually very convenient, the effort required to implement them is
Line 962: frequently pretty high. To be usable, a fake must reproduce a major chunk of the
Line 963: functionalities that the real dependency provided, and as we saw, implementing a fake
Line 964: might involve having to reverse engineer how the piece of software we are trying to replace
Line 965: works.
Line 966: Luckily, for most widespread needs, you will find fake implementations of SQL servers,
Line 967: MongoDB, S3, and so on, already available as libraries you can install.
Line 968: While the fake approach worked well, the worst part of our fake usage is probably how we
Line 969: had to patch the multiprocessing module to put it in place.
Line 970: This is a problem caused by the fact that our Connection object, being based on
Line 971: SyncManager, doesn't provide proper support for dependency injection, which would
Line 972: have allowed us to inject our own communication channel in a proper way instead of
Line 973: having to patch the "pickle" based one.
Line 974: But before moving on to see how we can handle the injection of dependencies, let's finish
Line 975: our chat application and make our acceptance test pass.
Line 976: 
Line 977: --- 페이지 66 ---
Line 978: Test Doubles with a Chat Application
Line 979: Chapter 2
Line 980: [ 56 ]
Line 981: Understanding acceptance tests and
Line 982: doubles
Line 983: We saw our Connection object works with the FakeServer but does our acceptance test
Line 984: finally pass now? Not yet. We still have to provide a server there (fake or not) and we still
Line 985: have to finish the implementation of the client.
Line 986: Acceptance tests are meant to verify that the software really does what we wanted once it's
Line 987: in the hands of our users. For this reason, it's usually a good idea to limit the usage of test
Line 988: doubles in the context of acceptance tests. They should work as much as possible by
Line 989: reproducing the real usage of the software.
Line 990: While mocks, stubs, dummies, and so on are rarely seen in acceptance tests, it's pretty
Line 991: common to see fakes in that context too. As fakes are supposed to mimic the behavior of the
Line 992: real service they replace, the software should notice no difference. But if you used fakes in
Line 993: your acceptance tests, it's a good idea to introduce a set of system tests that verify the
Line 994: software on the real services it depends on (maybe only executed at release time due to
Line 995: their cost).
Line 996: In our case, we want our acceptance test to work with a real server, thus we are going to
Line 997: tweak it a little bit to start the server and connect the clients to the newly started server. As
Line 998: our server is implemented on top of a SyncManager, like all SyncManagers it can be
Line 999: started and stopped by using it as a context manager in a with statement.
Line 1000: When we enter the with new_chat_server() context, the server will be started, and once
Line 1001: we exit it, the server will be stopped:
Line 1002: class TestChatAcceptance(unittest.TestCase):
Line 1003:     def test_message_exchange(self):
Line 1004:         with new_chat_server():
Line 1005:             user1 = ChatClient("John Doe")
Line 1006:             user2 = ChatClient("Harry Potter")
Line 1007:             user1.send_message("Hello World")
Line 1008:             messages = user2.fetch_messages()
Line 1009:             assert messages == ["John Doe: Hello World"]
Line 1010: Obviously, running the test will fail because we have not yet made the new_chat_server
Line 1011: function that is supposed to return the server in use by the test.
Line 1012: 
Line 1013: --- 페이지 67 ---
Line 1014: Test Doubles with a Chat Application
Line 1015: Chapter 2
Line 1016: [ 57 ]
Line 1017: Our server will be just a SyncManager subclass that provides the list of messages (through
Line 1018: the _srv_get_messages function) so that the clients can access them:
Line 1019: _messages = []
Line 1020: def _srv_get_messages():
Line 1021:     return _messages
Line 1022: class _ChatServerManager(SyncManager):
Line 1023:     pass
Line 1024: _ChatServerManager.register("get_messages",
Line 1025:                             callable=_srv_get_messages,
Line 1026:                             proxytype=ListProxy)
Line 1027: def new_chat_server():
Line 1028:     return _ChatServerManager(("", 9090), authkey=b'mychatsecret')
Line 1029: Now that we've created our new_chat_server, which can be used to start the server, our
Line 1030: next step is, as usual, to verify that our tests do pass to see what's the next step:
Line 1031: $ python 06_acceptance_tests.py TestChatAcceptance
Line 1032: E
Line 1033: ======================================================================
Line 1034: ERROR: test_message_exchange (__main__.TestChatAcceptance)
Line 1035: ----------------------------------------------------------------------
Line 1036: Traceback (most recent call last):
Line 1037:   File "06_dependency_injection.py", line 12, in test_message_exchange
Line 1038:     messages = user2.fetch_messages()
Line 1039: AttributeError: 'ChatClient' object has no attribute 'fetch_messages'
Line 1040: ----------------------------------------------------------------------
Line 1041: Ran 1 test in 0.011s
Line 1042: FAILED (errors=1)
Line 1043: In this case, the test doesn't yet pass because we forgot to implement the last piece of our
Line 1044: client: the part related to fetching the messages. So let's add that new fetch_messages
Line 1045: method to our client and see if things work as we want.
Line 1046: As usual, we should start with a test for the ChatClient.send_message unit, so that we
Line 1047: can verify that our implementation does what we expect:
Line 1048: class TestChatClient(unittest.TestCase):
Line 1049:     ...
Line 1050:     def test_client_fetch_messages(self):
Line 1051:         client = ChatClient("User 1")
Line 1052:         client.connection = unittest.mock.Mock()
Line 1053:         client.connection.get_messages.return_value = ["message1",
Line 1054: 
Line 1055: --- 페이지 68 ---
Line 1056: Test Doubles with a Chat Application
Line 1057: Chapter 2
Line 1058: [ 58 ]
Line 1059:                                                        "message2"]
Line 1060:         starting_messages = client.fetch_messages()
Line 1061:         client.connection.get_messages().append("message3")
Line 1062:         new_messages = client.fetch_messages()
Line 1063:         assert starting_messages == ["message1", "message2"]
Line 1064:         assert new_messages == ["message3"]
Line 1065: As our ChatClient.fetch_messages method doesn't yet exist, our test unit will
Line 1066: immediately fail:
Line 1067: $ python 06_acceptance_tests.py TestChatClient
Line 1068: .E..
Line 1069: ======================================================================
Line 1070: ERROR: test_client_fetch_messages (__main__.TestChatClient)
Line 1071: ----------------------------------------------------------------------
Line 1072: Traceback (most recent call last):
Line 1073:   File "06_dependency_injection.py", line 46, in test_client_fetch_messages
Line 1074:     starting_messages = client.fetch_messages()
Line 1075: AttributeError: 'ChatClient' object has no attribute 'fetch_messages'
Line 1076: ----------------------------------------------------------------------
Line 1077: Ran 4 tests in 0.001s
Line 1078: FAILED (errors=1)
Line 1079: So, what we can do is go back to ChatClient and implement the fetch_messages
Line 1080: method in a way that satisfies our test:
Line 1081: class ChatClient:
Line 1082:     def __init__(self, nickname):
Line 1083:         self.nickname = nickname
Line 1084:         self._connection = None
Line 1085:         self._last_msg_idx = 0
Line 1086:     def send_message(self, message):
Line 1087:         sent_message = "{}: {}".format(self.nickname, message)
Line 1088:         self.connection.broadcast(sent_message)
Line 1089:         return sent_message
Line 1090:     def fetch_messages(self):
Line 1091:         messages = list(self.connection.get_messages())
Line 1092:         new_messages = messages[self._last_msg_idx:]
Line 1093:         self._last_msg_idx = len(messages)
Line 1094:         return new_messages
Line 1095: 
Line 1096: --- 페이지 69 ---
Line 1097: Test Doubles with a Chat Application
Line 1098: Chapter 2
Line 1099: [ 59 ]
Line 1100: The new ChatClient.fetch_messages method will fetch the messages stored by the
Line 1101: server and will return any new ones since the last time they were checked.
Line 1102: If our implementation is correct, running the test again will make it pass and will confirm
Line 1103: that our method does what we wanted it to do:
Line 1104: $ python 06_acceptance_tests.py TestChatClient
Line 1105: ....
Line 1106: ----------------------------------------------------------------------
Line 1107: Ran 4 tests in 0.001s
Line 1108: OK
Line 1109: Also, as this was our last missing piece, the acceptance test should now pass, confirming
Line 1110: that our chat application does work as we wanted:
Line 1111: $ python 06_acceptance_tests.py TestChatAcceptance
Line 1112: .
Line 1113: ----------------------------------------------------------------------
Line 1114: Ran 1 test in 0.016s
Line 1115: OK
Line 1116: Hurray! We can finally declare victory. Our application works with the real client and real
Line 1117: server. They are able to connect and talk to each other, which proves we wrote the software
Line 1118: we wanted to write.
Line 1119: But our ChatClient tests have fairly complex code that has to rely on mock.patch to
Line 1120: replace pieces of it and we even had to implement a property setter for the connection for
Line 1121: the sole purpose of making it possible to replace it with a testing double.
Line 1122: Even though we achieved our goal, there should be a better way to enable test doubles in
Line 1123: code than spreading mock.patch everywhere.
Line 1124: Replacing components of a system on demand is what dependency injection was made
Line 1125: for, so let's see if it can help us to switch between using fakes and real services in our test
Line 1126: suite.
Line 1127: 
Line 1128: --- 페이지 70 ---
Line 1129: Test Doubles with a Chat Application
Line 1130: Chapter 2
Line 1131: [ 60 ]
Line 1132: Managing dependencies with dependency
Line 1133: injection
Line 1134: Our ChatClient machinery to connect to a server is rather more complex than necessary.
Line 1135: The ChatClient.get_connection and ChatClient.connection property setters are
Line 1136: there mostly to allow us to easily replace with mocks the connections that our client sets up.
Line 1137: This is because ChatClient has a dependency, a dependency on the Connection object,
Line 1138: and it tries to satisfy that dependency all by itself. It's like when you are hungry... You
Line 1139: depend on food to solve your need, so you go to the fridge, take some ingredients, turn on
Line 1140: the oven, and cook a meal yourself. Then you can eat. Or... you can call a restaurant and
Line 1141: order a meal.
Line 1142: Dependency injection gives you a way to take the restaurant path. If your ChatClient
Line 1143: needs a connection, instead of trying to get a connection itself, it can ask for a connection
Line 1144: and someone else will take care of providing it.
Line 1145: In most dependency injection systems, there is an injector that will take care of getting the
Line 1146: right object and providing it to the client. The client typically doesn't even have to know
Line 1147: about the injector. This usually involves fairly advanced frameworks that provide a services
Line 1148: registry and allow clients to register for those services, but there is a very simple form of
Line 1149: dependency injection that works very well and can be immediately achieved without any
Line 1150: external dependency or framework: construction injection.
Line 1151: Construction injection means that the service your code depends on is provided as a
Line 1152: parameter when building the class that depends on it.
Line 1153: In our case, we could easily refactor the ChatClient to accept a connection_provider
Line 1154: argument, which would allow us to simplify our ChatClient implementation and get rid
Line 1155: of entire parts of it:
Line 1156: class ChatClient:
Line 1157:     def __init__(self, nickname, connection_provider=Connection):
Line 1158:         self.nickname = nickname
Line 1159:         self._connection = None
Line 1160:         self._connection_provider = connection_provider
Line 1161:         self._last_msg_idx = 0
Line 1162:     def send_message(self, message):
Line 1163:         sent_message = "{}: {}".format(self.nickname, message)
Line 1164:         self.connection.broadcast(sent_message)
Line 1165:         return sent_message
Line 1166: 
Line 1167: --- 페이지 71 ---
Line 1168: Test Doubles with a Chat Application
Line 1169: Chapter 2
Line 1170: [ 61 ]
Line 1171:     def fetch_messages(self):
Line 1172:         messages = list(self.connection.get_messages())
Line 1173:         new_messages = messages[self._last_msg_idx:]
Line 1174:         self._last_msg_idx = len(messages)
Line 1175:         return new_messages
Line 1176:     @property
Line 1177:     def connection(self):
Line 1178:         if self._connection is None:
Line 1179:             self._connection = self._connection_provider(("localhost",
Line 1180:                                                           9090))
Line 1181:         return self._connection
Line 1182: We got rid of ChatClient.get_connection and we got rid of the connection
Line 1183: @property.setter but we haven't lost a single functionality, nor have we added any
Line 1184: additional complexity. In most cases, the ChatClient can be used exactly like before and it
Line 1185: will take care of using the right Connection by default.
Line 1186: But for the cases where we want to do something different, we can inject other kinds of
Line 1187: connections.
Line 1188: For example, in our TestChatClient.test_client_connection test, we can remove a
Line 1189: fairly hard-to-read mock.patch that was in place to set up a spy:
Line 1190: class TestChatClient(unittest.TestCase):
Line 1191:     def test_client_connection(self):
Line 1192:         client = ChatClient("User 1")
Line 1193:         connection_spy = unittest.mock.MagicMock()
Line 1194:         with unittest.mock.patch.object
Line 1195:           (client, "_get_connection",return_value=connection_spy):
Line 1196:             client.send_message("Hello World")
Line 1197:         connection_spy.broadcast.assert_called_with(("User 1:
Line 1198:                                                      Hello World"))
Line 1199: 
Line 1200: --- 페이지 72 ---
Line 1201: Test Doubles with a Chat Application
Line 1202: Chapter 2
Line 1203: [ 62 ]
Line 1204: Instead of having to patch the implementation of ChatClient, we can just provide the spy
Line 1205: to the ChatClient and have it use it:
Line 1206:     def test_client_connection(self):
Line 1207:         connection_spy = unittest.mock.MagicMock()
Line 1208:         client = ChatClient("User 1", connection_provider=lambda *args:
Line 1209:                             connection_spy)
Line 1210:         client.send_message("Hello World")
Line 1211:         connection_spy.broadcast.assert_called_with(("User 1:
Line 1212:                                                      Hello World"))
Line 1213: The code is far easier to follow and understand and doesn't rely on magic such as patching
Line 1214: objects at runtime.
Line 1215: In fact, our whole TestChatClient can be made simpler by using dependency injection
Line 1216: instead of patching:
Line 1217: class TestChatClient(unittest.TestCase):
Line 1218:     def test_nickname(self):
Line 1219:         client = ChatClient("User 1")
Line 1220:         assert client.nickname == "User 1"
Line 1221:     def test_send_message(self):
Line 1222:         client = ChatClient("User 1",
Line 1223:                             connection_provider=unittest.mock.Mock())
Line 1224:         sent_message = client.send_message("Hello World")
Line 1225:         assert sent_message == "User 1: Hello World"
Line 1226:     def test_client_connection(self):
Line 1227:         connection_spy = unittest.mock.MagicMock()
Line 1228:         client = ChatClient("User 1", connection_provider=lambda *args:
Line 1229:                             connection_spy)
Line 1230:         client.send_message("Hello World")
Line 1231:         connection_spy.broadcast.assert_called_with(("User 1: Hello
Line 1232:                                                      World"))
Line 1233:     def test_client_fetch_messages(self):
Line 1234:         connection = unittest.mock.Mock()
Line 1235:         connection.get_messages.return_value = ["message1", "message2"]
Line 1236:         client = ChatClient("User 1", connection_provider=lambda *args:
Line 1237:                             connection)
Line 1238: 
Line 1239: --- 페이지 73 ---
Line 1240: Test Doubles with a Chat Application
Line 1241: Chapter 2
Line 1242: [ 63 ]
Line 1243:         starting_messages = client.fetch_messages()
Line 1244:         client.connection.get_messages().append("message3")
Line 1245:         new_messages = client.fetch_messages()
Line 1246:         assert starting_messages == ["message1", "message2"]
Line 1247:         assert new_messages == ["message3"]
Line 1248: In all cases where we had fairly hard-to-read uses of mock.patch, we have now replaced
Line 1249: them with an explicitly provided connection_provider when the ChatClient is
Line 1250: created.
Line 1251: So dependency injection can make your life easier when testing, but actually also makes
Line 1252: your implementation far more flexible.
Line 1253: Suppose that we want to have our chat app working on something different than
Line 1254: SyncManagers; now it's a matter of just passing a different kind of
Line 1255: connection_provider to our clients.
Line 1256: Whenever your classes depend on other objects that they are going to build themselves, it's
Line 1257: usually a good idea to question whether that's a place for dependency injection and
Line 1258: whether those services could be injected from outside instead of being built within the class
Line 1259: itself.
Line 1260: Using dependency injection frameworks
Line 1261: In Python, there are many frameworks for dependency injection, and it's an easy enough
Line 1262: technique to implement yourself that you will find various variations of it in many
Line 1263: frameworks. What dependency injection frameworks will do for you is wire the objects
Line 1264: together.
Line 1265: In our previous dependency injection paragraph, we explicitly provided the dependencies
Line 1266: every time we wanted to create a new object (apart from the default dependency, which
Line 1267: was provided for us, being the default argument). A dependency injection framework
Line 1268: would instead automatically detect for us that ChatClient needs a Connection and it
Line 1269: would give the connection to the ChatClient.
Line 1270: One of the easiest-to-use dependency injection frameworks for Python is Pinject from
Line 1271: Google. It comes from the great experience Google teams have with dependency injection
Line 1272: frameworks, which is clear if you look at some of their most famous frameworks, such as
Line 1273: Angular.
Line 1274: 
Line 1275: --- 페이지 74 ---
Line 1276: Test Doubles with a Chat Application
Line 1277: Chapter 2
Line 1278: [ 64 ]
Line 1279: Pinject manages dependencies in a very simple and easy to understand way, based on
Line 1280: initializer argument names and class names.
Line 1281: Suppose that, like before, we had our two ChatClient and Connection classes... but in
Line 1282: this case, our ChatClient is just going to print which Connection it's going to use, as our
Line 1283: sole purpose is to showcase how Pinject can handle dependency injection for us:
Line 1284: class ChatClient:
Line 1285:     def __init__(self, connection):
Line 1286:         print(self, "GOT", connection)
Line 1287: class Connection:
Line 1288:     pass
Line 1289: Then we can use pinject to create a graph of the dependencies of our objects:
Line 1290: import pinject
Line 1291: injector = pinject.new_object_graph()
Line 1292: Once pinject is aware of the dependencies of our objects (which by default are built by
Line 1293: scanning all classes in all imported modules; you can also pass your classes explicitly
Line 1294: through a classes= argument), we can ask pinject to give us an instance for any class
Line 1295: it's aware of, resolving all class dependencies for us:
Line 1296: >>> cli = injector.provide(ChatClient)
Line 1297: <ChatClient object at 0x7fad51469610> GOT <Connection object at
Line 1298: 0x7fad51469bd0>
Line 1299: What happened is that pinject detected that a Connection class existed and when we
Line 1300: requested a ChatClient, it saw that it depended on a Connection argument. At that
Line 1301: point, pinject automatically made a connection for us and provided it to the client.
Line 1302: What if we wanted to provide a fake Connection object for our tests? Pinject supports
Line 1303: providing custom binding specifications, so telling it explicitly which class solves a specific
Line 1304: dependency.
Line 1305: So if we had a FakeConnection object, we could create a pinject.BindingSpec to tell
Line 1306: pinject that to satisfy the "connection" dependency, it has to use the fake one:
Line 1307: class FakeConnection:
Line 1308:     pass
Line 1309: class FakedBindingSpec(pinject.BindingSpec):
Line 1310:     def provide_connection(self):
Line 1311:         return FakeConnection()
Line 1312: 
Line 1313: --- 페이지 75 ---
Line 1314: Test Doubles with a Chat Application
Line 1315: Chapter 2
Line 1316: [ 65 ]
Line 1317: faked_injector = pinject.new_object_graph(binding_specs=[
Line 1318:     FakedBindingSpec()
Line 1319: ])
Line 1320: At this point, if we tried to create a ChatClient through the faked_injector, we would
Line 1321: get back a ChatClient that uses a fake connection:
Line 1322: >>> cli = faked_injector.provide(ChatClient)
Line 1323: <ChatClient object at 0x7fad513ce350> GOT <FakeConnection object at
Line 1324: 0x7fad513d6f90>
Line 1325: It must be noted that, by default, Pinjector remembers the instances it made, so if we
Line 1326: requested a new ChatClient, it would get the same exact connection object. That is
Line 1327: frequently convenient when you are building a full piece of software and you want to
Line 1328: replace whole components. If you wanted to replace your data abstraction layer to use a
Line 1329: fake database, you would probably want to get the same data abstraction layer from
Line 1330: everywhere so that all components see the same data.
Line 1331: This means that creating a new ChatClient will give us a different ChatClient but with
Line 1332: the same underlying Connection:
Line 1333: >>> cli = faked_injector.provide(ChatClient)
Line 1334: <ChatClient object at 0x7f9878aeb810> GOT <Connection object at
Line 1335: 0x7f9878a58f50>
Line 1336: >>> cli2 = faked_injector.provide(ChatClient)
Line 1337: <ChatClient object at 0x7f9878a55fd0> GOT <Connection object at
Line 1338: 0x7f9878a58f50>
Line 1339: In the case of our clients, we probably want each of them to have a different connection to
Line 1340: the server. To do so, we can use the BindingSpec and tell pinject that our returned
Line 1341: dependency is a prototype and not a singleton. This way, pinject won't cache the provided
Line 1342: dependency and will always return a new one:
Line 1343: class PrototypeBindingSpec(pinject.BindingSpec):
Line 1344:     @pinject.provides(in_scope=pinject.PROTOTYPE)
Line 1345:     def provide_connection(self):
Line 1346:         return Connection()
Line 1347: proto_injector = pinject.new_object_graph(binding_specs=[
Line 1348:     PrototypeBindingSpec()
Line 1349: ])
Line 1350: 
Line 1351: --- 페이지 76 ---
Line 1352: Test Doubles with a Chat Application
Line 1353: Chapter 2
Line 1354: [ 66 ]
Line 1355: If we were to make a ChatClient with the proto_inject, we would now see that each
Line 1356: client has its own Connection object:
Line 1357: >>> cli = proto_injector.provide(ChatClient)
Line 1358: <ChatClient object at 0x7fadab060e50> GOT <Connection object at
Line 1359: 0x7fadab013910>
Line 1360: >>> cli2 = proto_injector.provide(ChatClient)
Line 1361: <ChatClient object at 0x7fadab060f10> GOT <Connection object at
Line 1362: 0x7fadab013850>
Line 1363: So, dependency injection frameworks can solve many needs for you. Whether you need to
Line 1364: use one or not depends mostly on how complex the network of dependencies in your
Line 1365: software is, but having one around can usually give you a quick way to break dependencies
Line 1366: between your components when you need to.
Line 1367: Summary
Line 1368: Dependencies between the components that you have to test can make your life hard as a
Line 1369: developer. To test anything more complex than a simple utility function, you might end up
Line 1370: having to cope with tens of dependencies and their state.
Line 1371: This is why the idea of being able to provide doubles for testing in place of the real
Line 1372: components was quickly born once the idea of automated tests became reality. Being able
Line 1373: to replace the components the unit you are testing depends on with fakes, dummies, stubs,
Line 1374: and mocks can make your life a lot easier and keep your test suite fast and easy to maintain.
Line 1375: The fact that any software is, in reality, a complex network of dependencies is the reason
Line 1376: why many people advocate that integration tests are the most realistic and reliable form of
Line 1377: testing, but managing that complex network can be hard and that's where dependency
Line 1378: injection and dependency injection frameworks can make your life far easier.
Line 1379: Now that we know how to write automatic test suites and we know how to use test
Line 1380: doubles to verify our components in isolation and spy their state and behavior, we have all
Line 1381: the tools that we need to dive into test-driven development in the next chapter and see how
Line 1382: to write software in the TDD way.