# 5.6.3 Verifying the wrong things (pp.118-119)

---
**Page 118**

118
CHAPTER 5
Isolation frameworks
can also be counted as a negative, as explained earlier, because it encourages us
to have code strongly coupled to third-party implementations.
Easier simulation of values or errors—Writing mocks manually can be difficult
across a complicated interface. Frameworks help a lot.
Easier fake creation—Isolation frameworks can be used to create both mocks and
stubs more easily. 
Although there are many advantages to using isolation frameworks, there are also pos-
sible dangers. Let’s now talk about a few things to watch out for.
5.6.1
You don’t need mock objects most of the time
The biggest trap that isolation frameworks lead you into is making it easy to fake any-
thing, and encouraging you to think you need mock objects in the first place. I’m not
saying you won’t need stubs, but mock objects shouldn’t be the standard operating
procedure for most unit tests. Remember that a unit of work can have three different
types of exit points: return values, state change, and calling a third-party dependency.
Only one of these types can benefit from a mock object in your test. The others don’t.
 I find that, in my own tests, mock objects are present in perhaps 2%–5% of my tests.
The rest of the tests are usually return-value or state-based tests. For functional designs,
the number of mock objects should be near zero, except for some corner cases.
 If you find yourself defining a test and verifying that an object or function was
called, think carefully whether you can prove the same functionality without a mock
object, but instead by verifying a return value or a change in the behavior of the over-
all unit of work from the outside (for example, verifying that a function throws an
exception when it didn’t before). Chapter 6 of Unit Testing Principles, Practices, and Pat-
terns by Vladimir Khorikov (Manning, 2020) contains a detailed description of how to
refactor interaction-based tests into simpler, more reliable tests that check a return
value instead.
5.6.2
Unreadable test code
Using a mock in a test makes the test a little less readable, but still readable enough
that an outsider can look at it and understand what’s going on. Having many mocks,
or many expectations, in a single test can ruin the readability of the test so it’s hard to
maintain, or even to understand what’s being tested.
 If you find that your test becomes unreadable or hard to follow, consider removing
some mocks or some mock expectations, or separating the test into several smaller
tests that are more readable.
5.6.3
Verifying the wrong things
Mock objects allow you to verify that methods were called on your interfaces or that
functions were called, but that doesn’t necessarily mean that you’re testing the right
thing. A lot of people new to tests end up verifying things just because they can, not
because it makes sense. Examples may include the following:


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


