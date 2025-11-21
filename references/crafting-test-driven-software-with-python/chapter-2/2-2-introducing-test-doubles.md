# 2.2 Introducing test doubles (pp.32-33)

---
**Page 32**

Test Doubles with a Chat Application
Chapter 2
[ 32 ]
Checking behaviors with spies
Using mocks
Replacing dependencies with fakes
Understanding acceptance tests and doubles
Managing dependencies with dependency injection
Technical requirements
A working Python interpreter should be all that is needed.
The examples have been written on Python 3.7 but should work on most modern Python
versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter02.
Introducing test doubles
In test-driven development, the tests drive the development process and architecture. The
software design evolves as the software changes during the development of new tests, and
the architecture you end up with should be a consequence of the need to satisfy your tests.
Tests are thus the arbiter that decides the future of our software and declares that the
software is doing what it is designed for. There are specific kinds of tests that are explicitly
designed to tell us that the software is doing what it was requested: Acceptance and
Functional tests.
So, while there are two possible approaches to TDD, top-down and bottom-up (one starting
with higher-level tests first, and the other starting with unit tests first), the best way to
avoid going in the wrong direction is to always keep in mind your acceptance rules, and
the most effective way to do so is to write them down as tests.
But how can we write a test that depends on the whole software existing and working if we
haven't yet written the software at all? The key is test doubles: objects that are able to
replace missing, incomplete, or expensive parts of our code just for the purpose of testing.
A test double is an object that takes the place of another object, faking that it is actually able
to do the same things as the other object, while in reality, it does nothing.


---
**Page 33**

Test Doubles with a Chat Application
Chapter 2
[ 33 ]
But if we make our tests pass with test doubles, how do we avoid shipping software that is
just a bunch of fake entities? That's why it's important to have various layers of tests – the
more you move up through the layers, the fewer test doubles you should have, all the way
up to end-to-end tests, which should involve no test doubles at all.
Test-driven development also suggests that we should write the minimum amount of code
necessary to make a test pass and it's a very important rule because, otherwise, you could
easily end up writing code whose development has to be driven by other new tests.
That means that to have a fairly high-level test (such as an acceptance test) pass, we are
probably going to involve many test doubles at the beginning (as our software is still
empty). So when are we expected to replace those test doubles with real objects?
That's where Test-Driven Development by Example by Kent Beck suggests relying on a TODO
list. As you write your code, you should write down anything that you think you need to
improve/support/replace. And before moving forward to writing the next acceptance test,
the TODO list should be completed.
In your TODO list, you can record entries to replace the test doubles with real objects. As a
consequence, we are going to write tests that verify the behaviors of those real objects and,
subsequently, their implementation, finally replacing them with the real objects themselves
in our original acceptance test to confirm it still passes.
To showcase how test doubles can help us during TDD, we are going to build a chat
application by relying on the most common kind of test doubles.
Starting our chat application with TDD
When you start the development of a new feature, the first test you might want to write is
the primary acceptance test – the one that helps you define "this is what I want to achieve."
Acceptance tests expose the components we need to create and the behaviors they need to
have, allowing us to move forward by designing the development tests for those
components and thus writing down unit and integration tests.
In the case of the chat application, our acceptance test will probably be a test where one
user can send a message and another user can receive it:
import unittest
class TestChatAcceptance(unittest.TestCase):
    def test_message_exchange(self):
        user1 = ChatClient("John Doe")
        user2 = ChatClient("Harry Potter")


