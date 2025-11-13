# 2.9 Understanding acceptance tests and doubles (pp.56-60)

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


