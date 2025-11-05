# 2.0 Introduction [auto-generated] (pp.31-32)

---
**Page 31**

2
Test Doubles with a Chat
Application
We have seen how a test suite, to be reasonably reliable, should include various kinds of
tests that cover components at various levels. Usually, tests, in regard to how many
components they involve, are categorized into at least three kinds: unit, integration, and
end-to-end.
Test doubles ease the implementation of tests by breaking dependencies between
components and allowing us to simulate the behaviors we want.
In this chapter, we will look at the most common kinds of test doubles, what their goals are,
and how to use them in real code. By the end of this chapter, we will have covered how to
use all those test doubles and you will be able to leverage them for your own Python
projects.
By adding test doubles to your toolchain, you will be able to write faster tests, decouple the
components you want to test from the rest of the system, simulate behaviors that depend
on other components' state, and in general move your test suite development forward with
fewer blockers.
In this chapter, we will learn how to move forward, in the Test-Driven Development
(TDD) way, the development of an application that depends on other external
dependencies such as a database management system and networking, relying on test
doubles for the development process and replacing them in our inner test layers to ensure
fast and consistent execution of our tests.
In this chapter, we will cover the following topics:
Introducing test doubles
Starting our chat application with TDD
Using dummy objects
Replacing components with stubs


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


