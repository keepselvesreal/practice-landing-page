# 1.7 Summary (pp.30-31)

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


