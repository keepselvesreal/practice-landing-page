# 5.7 Summary (pp.119-121)

---
**Page 119**

119
Summary
Verifying that an internal function calls another internal function (not an
exit point).
Verifying that a stub was called (an incoming dependency should not be veri-
fied; it’s the overspecification antipattern, as we’ll discuss in section 5.6.5).
Verifying that something was called simply because someone told you to write a
test, and you’re not sure what should really be tested. (This is a good time to
verify that you’re understanding the requirements correctly.)
5.6.4
Having more than one mock per test
It’s considered good practice to test only one concern per test. Testing more than one
concern can lead to confusion and problems maintaining the test. Having two mocks
in a test is the same as testing several end results of the same unit of work (multiple
exit points).
 For each exit point, consider writing a separate test, as it could be considered a
separate requirement. Chances are that your test names will also become more focused
and readable when you only test one concern. If you can’t name your test because it
does too many things and the name becomes very generic (e.g., “XWorksOK”), it’s time
to separate it into more than one test.
5.6.5
Overspecifying the tests
If your test has too many expectations (x.received().X(), x.received().Y(), and so
on), it may become very fragile, breaking on the slightest of production code changes,
even though the overall functionality still works. Testing interactions is a double-
edged sword: test them too much, and you start to lose sight of the big picture—the
overall functionality; test them too little, and you’ll miss the important interactions
between units of work. 
 Here are some ways to balance this effect:
Use stubs instead of mocks when you can—If more than 5% of your tests use mock
objects, you might be overdoing it. Stubs can be everywhere. Mocks, not so
much. You only need to test one scenario at a time. The more mocks you
have, the more verifications will take place at the end of the test, but usually
only one will be the important one. The rest will be noise against the current
test scenario.
Avoid using stubs as mocks if possible—Use a stub only for faking simulated values
into the unit of work under test or to throw exceptions. Don’t verify that meth-
ods were called on stubs.
Summary
Isolation, or mocking, frameworks allow you to dynamically create, configure,
and verify mocks and stubs, either in object or function form. Isolation frame-
works save a lot of time compared to handwritten fakes, especially in modular
dependency situations.


---
**Page 120**

120
CHAPTER 5
Isolation frameworks
There are two flavors of isolation frameworks: loosely typed (such as Jest and
Sinon) and strongly typed (such as substitute.js). Loosely typed frameworks
require less boilerplate and are good for functional-style code; strongly typed
frameworks are useful when dealing with classes and interfaces.
Isolation frameworks can replace whole modules, but try to abstract away direct
dependencies and fake those abstractions instead. This will help you reduce the
amount of refactoring needed when the module’s API changes.
It's important to lean toward return-value or state-based testing as opposed to
interaction testing whenever you can, so that your tests assume as little as possi-
ble about internal implementation details.
Mocks should be used only when there’s no other way to test the implementa-
tion, because they eventually lead to tests that are harder to maintain if you’re
not careful.
Choose the way you work with isolation frameworks based on the codebase you
are working on. In legacy projects, you may need to fake whole modules, as it
might be the only way to add tests to such projects. In greenfield projects, try to
introduce proper abstractions on top of third-party modules. It’s all about pick-
ing the right tool for the job, so be sure to look at the big picture when consid-
ering how to approach a specific problem in testing.


---
**Page 121**

121
Unit testing
asynchronous code
When we’re dealing with regular synchronous code, waiting for actions to finish is
implicit. We don’t worry about it, and we don’t really think about it too much. When
dealing with asynchronous code, however, waiting for actions to finish becomes an
explicit activity that is under our control. Asynchronicity makes code, and the tests
for that code, potentially trickier because we have to be explicit about waiting for
actions to complete.
 Let’s start with a simple fetching example to illustrate the issue.
 
 
This chapter covers
Async, done(), and awaits
Integration and unit test levels for async
The Extract Entry Point pattern
The Extract Adapter pattern
Stubbing, advancing, and resetting timers


