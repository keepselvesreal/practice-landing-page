# 2.10.0 Introduction [auto-generated] (pp.60-63)

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


---
**Page 61**

Test Doubles with a Chat Application
Chapter 2
[ 61 ]
    def fetch_messages(self):
        messages = list(self.connection.get_messages())
        new_messages = messages[self._last_msg_idx:]
        self._last_msg_idx = len(messages)
        return new_messages
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._connection_provider(("localhost",
                                                          9090))
        return self._connection
We got rid of ChatClient.get_connection and we got rid of the connection
@property.setter but we haven't lost a single functionality, nor have we added any
additional complexity. In most cases, the ChatClient can be used exactly like before and it
will take care of using the right Connection by default.
But for the cases where we want to do something different, we can inject other kinds of
connections.
For example, in our TestChatClient.test_client_connection test, we can remove a
fairly hard-to-read mock.patch that was in place to set up a spy:
class TestChatClient(unittest.TestCase):
    def test_client_connection(self):
        client = ChatClient("User 1")
        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object
          (client, "_get_connection",return_value=connection_spy):
            client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1:
                                                     Hello World"))


---
**Page 62**

Test Doubles with a Chat Application
Chapter 2
[ 62 ]
Instead of having to patch the implementation of ChatClient, we can just provide the spy
to the ChatClient and have it use it:
    def test_client_connection(self):
        connection_spy = unittest.mock.MagicMock()
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection_spy)
        client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1:
                                                     Hello World"))
The code is far easier to follow and understand and doesn't rely on magic such as patching
objects at runtime.
In fact, our whole TestChatClient can be made simpler by using dependency injection
instead of patching:
class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")
        assert client.nickname == "User 1"
    def test_send_message(self):
        client = ChatClient("User 1",
                            connection_provider=unittest.mock.Mock())
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"
    def test_client_connection(self):
        connection_spy = unittest.mock.MagicMock()
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection_spy)
        client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with(("User 1: Hello
                                                     World"))
    def test_client_fetch_messages(self):
        connection = unittest.mock.Mock()
        connection.get_messages.return_value = ["message1", "message2"]
        client = ChatClient("User 1", connection_provider=lambda *args:
                            connection)


---
**Page 63**

Test Doubles with a Chat Application
Chapter 2
[ 63 ]
        starting_messages = client.fetch_messages()
        client.connection.get_messages().append("message3")
        new_messages = client.fetch_messages()
        assert starting_messages == ["message1", "message2"]
        assert new_messages == ["message3"]
In all cases where we had fairly hard-to-read uses of mock.patch, we have now replaced
them with an explicitly provided connection_provider when the ChatClient is
created.
So dependency injection can make your life easier when testing, but actually also makes
your implementation far more flexible.
Suppose that we want to have our chat app working on something different than
SyncManagers; now it's a matter of just passing a different kind of
connection_provider to our clients.
Whenever your classes depend on other objects that they are going to build themselves, it's
usually a good idea to question whether that's a place for dependency injection and
whether those services could be injected from outside instead of being built within the class
itself.
Using dependency injection frameworks
In Python, there are many frameworks for dependency injection, and it's an easy enough
technique to implement yourself that you will find various variations of it in many
frameworks. What dependency injection frameworks will do for you is wire the objects
together.
In our previous dependency injection paragraph, we explicitly provided the dependencies
every time we wanted to create a new object (apart from the default dependency, which
was provided for us, being the default argument). A dependency injection framework
would instead automatically detect for us that ChatClient needs a Connection and it
would give the connection to the ChatClient.
One of the easiest-to-use dependency injection frameworks for Python is Pinject from
Google. It comes from the great experience Google teams have with dependency injection
frameworks, which is clear if you look at some of their most famous frameworks, such as
Angular.


