# 5.6.5 Overspecifying the tests (pp.119-119)

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


