# 1.6.2 The testing trophy (pp.28-29)

---
**Page 28**

Getting Started with Software Testing
Chapter 1
[ 28 ]
The other most widespread model is the testing trophy, which instead emphasizes
integration tests.
The testing trophy
The testing trophy originates from a phrase by Guillermo Rauch, the author of Socket.io
and many other famous JavaScript-based technologies. Guillermo stated that developers
should "Write tests. Not too many. Mostly integration."
Like Mike Cohn, he clearly states that tests are the foundation of any effective software
development practice, but he argues that they have a diminishing return and thus it's
important to find the sweet spot where you get the best return on the time spent writing
tests.
That sweet spot is expected to live in integration tests because you usually need fewer of
them to spot real problems, they are not too bound to implementation details, and they are
still fast enough that you can afford to write a few of them.
So the testing trophy will look like this:
Figure 1.2 – Testing trophy


---
**Page 29**

Getting Started with Software Testing
Chapter 1
[ 29 ]
As you probably saw, the testing trophy puts a lot of value on static tests too, because the
whole idea of the testing trophy is that what is really of value is the return on investment,
and static checks are fairly cheap, up to the point that most development environments run
them in real time. Linters, type checkers, and more advanced kinds of type analyzers are
cheap enough that it would do no good to ignore them even if they are rarely able to spot
bugs in your business logic.
Unit tests instead can cost developers time with the need to adapt them due to internal
implementation detail changes that don't impact the final behavior of the software in any
way, and thus the effort spent on them should be kept under control.
Those two models are the most common ways to distribute your tests, but more best
practices are involved when thinking of testing distribution and coverage.
Testing distribution and coverage
While the importance of testing is widely recognized, there is also general agreement that
test suites have a diminishing return.
There is little point in wasting hours on testing plain getters and setters or testing
internal/private methods. The sweet spot is said to be around 80% of code coverage, even
though I think that really depends on the language in use – the more expressive your
language is, the less code you have to write to perform complex actions. And all complex
actions should be properly tested, so in the case of Python, the sweet spots probably lies
more in the range of 90%. But there are cases, such as porting projects from Python 2 to
Python 3, where code coverage of 100% is the only way you can confirm that you haven't
changed any behavior at all in the process of porting your code base.
Last but not least, most testing practices related to test-driven development take care of the
testing practice up to the release point. It's important to keep in mind that when the
software is released, the testing process hasn't finished.
Many teams forget to set up proper system tests and don't have a way to identify and
reproduce issues that can only happen in production environments with real concurrent
users and large amounts of data. Having staging environments and a suite to simulate
incidents or real users' behaviors might be the only way to spot bugs that only happen after
days of continuous use of the system. And some companies go as far as testing the
production system with tools that inject real problems continuously for the sole purpose of
verifying that the system is solid.


