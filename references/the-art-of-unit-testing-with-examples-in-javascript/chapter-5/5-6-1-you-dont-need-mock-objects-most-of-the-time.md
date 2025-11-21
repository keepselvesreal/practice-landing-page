# 5.6.1 You don’t need mock objects most of the time (pp.118-118)

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


