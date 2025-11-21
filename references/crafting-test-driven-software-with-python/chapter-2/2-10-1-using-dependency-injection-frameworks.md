# 2.10.1 Using dependency injection frameworks (pp.63-66)

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


---
**Page 64**

Test Doubles with a Chat Application
Chapter 2
[ 64 ]
Pinject manages dependencies in a very simple and easy to understand way, based on
initializer argument names and class names.
Suppose that, like before, we had our two ChatClient and Connection classes... but in
this case, our ChatClient is just going to print which Connection it's going to use, as our
sole purpose is to showcase how Pinject can handle dependency injection for us:
class ChatClient:
    def __init__(self, connection):
        print(self, "GOT", connection)
class Connection:
    pass
Then we can use pinject to create a graph of the dependencies of our objects:
import pinject
injector = pinject.new_object_graph()
Once pinject is aware of the dependencies of our objects (which by default are built by
scanning all classes in all imported modules; you can also pass your classes explicitly
through a classes= argument), we can ask pinject to give us an instance for any class
it's aware of, resolving all class dependencies for us:
>>> cli = injector.provide(ChatClient)
<ChatClient object at 0x7fad51469610> GOT <Connection object at
0x7fad51469bd0>
What happened is that pinject detected that a Connection class existed and when we
requested a ChatClient, it saw that it depended on a Connection argument. At that
point, pinject automatically made a connection for us and provided it to the client.
What if we wanted to provide a fake Connection object for our tests? Pinject supports
providing custom binding specifications, so telling it explicitly which class solves a specific
dependency.
So if we had a FakeConnection object, we could create a pinject.BindingSpec to tell
pinject that to satisfy the "connection" dependency, it has to use the fake one:
class FakeConnection:
    pass
class FakedBindingSpec(pinject.BindingSpec):
    def provide_connection(self):
        return FakeConnection()


---
**Page 65**

Test Doubles with a Chat Application
Chapter 2
[ 65 ]
faked_injector = pinject.new_object_graph(binding_specs=[
    FakedBindingSpec()
])
At this point, if we tried to create a ChatClient through the faked_injector, we would
get back a ChatClient that uses a fake connection:
>>> cli = faked_injector.provide(ChatClient)
<ChatClient object at 0x7fad513ce350> GOT <FakeConnection object at
0x7fad513d6f90>
It must be noted that, by default, Pinjector remembers the instances it made, so if we
requested a new ChatClient, it would get the same exact connection object. That is
frequently convenient when you are building a full piece of software and you want to
replace whole components. If you wanted to replace your data abstraction layer to use a
fake database, you would probably want to get the same data abstraction layer from
everywhere so that all components see the same data.
This means that creating a new ChatClient will give us a different ChatClient but with
the same underlying Connection:
>>> cli = faked_injector.provide(ChatClient)
<ChatClient object at 0x7f9878aeb810> GOT <Connection object at
0x7f9878a58f50>
>>> cli2 = faked_injector.provide(ChatClient)
<ChatClient object at 0x7f9878a55fd0> GOT <Connection object at
0x7f9878a58f50>
In the case of our clients, we probably want each of them to have a different connection to
the server. To do so, we can use the BindingSpec and tell pinject that our returned
dependency is a prototype and not a singleton. This way, pinject won't cache the provided
dependency and will always return a new one:
class PrototypeBindingSpec(pinject.BindingSpec):
    @pinject.provides(in_scope=pinject.PROTOTYPE)
    def provide_connection(self):
        return Connection()
proto_injector = pinject.new_object_graph(binding_specs=[
    PrototypeBindingSpec()
])


---
**Page 66**

Test Doubles with a Chat Application
Chapter 2
[ 66 ]
If we were to make a ChatClient with the proto_inject, we would now see that each
client has its own Connection object:
>>> cli = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060e50> GOT <Connection object at
0x7fadab013910>
>>> cli2 = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060f10> GOT <Connection object at
0x7fadab013850>
So, dependency injection frameworks can solve many needs for you. Whether you need to
use one or not depends mostly on how complex the network of dependencies in your
software is, but having one around can usually give you a quick way to break dependencies
between your components when you need to.
Summary
Dependencies between the components that you have to test can make your life hard as a
developer. To test anything more complex than a simple utility function, you might end up
having to cope with tens of dependencies and their state.
This is why the idea of being able to provide doubles for testing in place of the real
components was quickly born once the idea of automated tests became reality. Being able
to replace the components the unit you are testing depends on with fakes, dummies, stubs,
and mocks can make your life a lot easier and keep your test suite fast and easy to maintain.
The fact that any software is, in reality, a complex network of dependencies is the reason
why many people advocate that integration tests are the most realistic and reliable form of
testing, but managing that complex network can be hard and that's where dependency
injection and dependency injection frameworks can make your life far easier.
Now that we know how to write automatic test suites and we know how to use test
doubles to verify our components in isolation and spy their state and behavior, we have all
the tools that we need to dive into test-driven development in the next chapter and see how
to write software in the TDD way.


