# 2.8 Replacing dependencies with fakes (pp.51-56)

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


