# 1.6.3 Testing distribution and coverage (pp.29-30)

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


---
**Page 30**

Getting Started with Software Testing
Chapter 1
[ 30 ]
Summary
As we saw in the sections about integration tests, functional tests, and the testing
pyramid/trophy models, there are many different visions about what should be tested, with
which goals in mind, and how test suites should be organized. Getting this right can impact
how much you trust your automatic test suite, and thus how much you evolve it because it
provides you with value.
Learning to do proper automated testing is the gateway to major software development
boosts, opening possibilities for practices such as continuous integration and continuous
delivery, which would otherwise be impossible without a proper test suite.
But testing isn't easy; it comes with many side-effects that are not immediately obvious, and
for which the software development industry started to provide tools and best practices
only recently. So in the next chapters, we will look at some of those best practices and tools
that can help you write a good, easily maintained test suite.


