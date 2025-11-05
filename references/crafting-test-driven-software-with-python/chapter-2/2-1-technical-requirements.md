# 2.1 Technical requirements (pp.32-32)

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


