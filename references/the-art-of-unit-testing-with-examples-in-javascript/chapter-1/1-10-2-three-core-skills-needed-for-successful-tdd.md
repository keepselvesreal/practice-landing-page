# 1.10.2 Three core skills needed for successful TDD (pp.25-26)

---
**Page 25**

25
1.10
Test-driven development
design, and keep your manager happier. If TDD is done incorrectly, it can cause your
project schedule to slip, waste your time, lower your motivation, and lower your code
quality. It’s a double-edged sword, and many people find this out the hard way. 
 Technically, one of the biggest benefits of TDD that nobody tells you about is that
by seeing a test fail, and then seeing it pass without changing the test, you’re basically
testing the test itself. If you expect it to fail and it passes, you might have a bug in your
test or you’re testing the wrong thing. If the test failed, you fixed it, and now you
expect it to pass, and it still fails, your test could have a bug, or maybe it’s expecting
the wrong thing to happen.
 This book deals with readable, maintainable, and trustworthy tests, but if you add
TDD on top, your confidence in your own tests will increase by seeing the failed, you
fixed it, tests failing when they should and passing when they should. In test-after style,
you’ll usually only see them pass when they should, and fail when they shouldn’t
(since the code they test should already be working). TDD helps with that a lot, and
it’s also one of the reasons developers do far less debugging when practicing TDD
than when they’re simply unit testing after the fact. If they trust the tests, they don’t
feel a need to debug it “just in case.” That’s the kind of trust you can only gain by see-
ing both sides of the test—failing when it should and passing when it should.
1.10.2 Three core skills needed for successful TDD
To be successful in test-driven development, you need three different skill sets: know-
ing how to write good tests, writing them test-first, and designing the tests and the pro-
duction code well. Figure 1.10 shows these more clearly:
Just because you write your tests first doesn’t mean they’re maintainable, readable, or trust-
worthy. Good unit testing skills are what this book is all about.
Just because you write readable, maintainable tests doesn’t mean you’ll get the same bene-
fits as when writing them test-first. Test-first skills are what most of the TDD books
out there teach, without teaching the skills of good testing. I would especially
recommend Kent Beck’s Test-Driven Development: By Example (Addison-Wesley
Professional, 2002). 
TDD skills
This book
Other books
Writing
good tests
Writing
test-ﬁrst
SOLID
design
Figure 1.10
Three core skills 
of test-driven development


---
**Page 26**

26
CHAPTER 1
The basics of unit testing
Just because you write your tests first, and they’re readable and maintainable, doesn’t
mean you’ll end up with a well-designed system. Design skills are what make your
code beautiful and maintainable. I recommend Growing Object-Oriented Software,
Guided by Tests by Steve Freeman and Nat Pryce (Addison-Wesley Professional,
2009) and Clean Code by Robert C. Martin (Pearson, 2008) as good books on the
subject.
A pragmatic approach to learning TDD is to learn each of these three aspects sepa-
rately; that is, to focus on one skill at a time, ignoring the others in the meantime. The
reason I recommend this approach is that I often see people trying to learn all three
skill sets at the same time, having a really hard time in the process, and finally giving
up because the wall is too high to climb. By taking a more incremental approach to
learning this field, you relieve yourself of the constant fear that you’re getting it wrong
in a different area than you’re currently focusing on.
 In the next chapter, you’ll start writing your first unit tests using Jest, one of the
most commonly used test frameworks for JavaScript.
Summary
A good unit test has these qualities:
– It should run quickly.
– It should have full control of the code under test.
– It should be fully isolated (it should run independently of other tests).
– It should run in memory without requiring filesystem files, networks, or
databases. 
– It should be as synchronous and linear as possible (no parallel threads).
Entry points are public functions that are the doorways into our units of work
and trigger the underlying logic. Exit points are the places you can inspect with
your test. They represent the effects of the units of work. 
An exit point can be a return value, a change of state, or a call to a third-party
dependency. Each exit point usually requires a separate test, and each type of
exit point requires a different testing technique.
A unit of work is the sum of actions that take place between the invocation of an
entry point up until a noticeable end result through one or more exit points. A
unit of work can span a function, a module, or multiple modules.
Integration testing is just unit testing with some or all of the dependencies
being real and residing outside of the current execution process. Conversely,
unit testing is like integration testing, but with all of the dependencies in mem-
ory (both real and fake), and we have control over their behavior in the test.
The most important attributes of any test are readability, maintainability, and
trust. Readability tells us how easy it is to read and understand the test. Maintain-
ability is the measure of how painful it is to maintain the test code. Without trust,


