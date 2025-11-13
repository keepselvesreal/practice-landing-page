# 1.10.1 TDD: Not a substitute for good unit tests (pp.24-25)

---
**Page 24**

24
CHAPTER 1
The basics of unit testing
for the code I was writing. I’m convinced that it can work to your benefit, but it’s not
without a price (time to learn, time to implement, and more). It’s definitely worth the
admission price, though, if you’re willing to take on the challenge of learning it. 
1.10.1 TDD: Not a substitute for good unit tests
It’s important to realize that TDD doesn’t ensure project success or tests that are robust
or maintainable. It’s quite easy to get caught up in the technique of TDD and not pay
attention to the way unit tests are written: their naming, how maintainable or readable
they are, and whether they test the right things or might themselves have bugs. That’s
why I’m writing this book—because writing good tests is a separate skill from TDD. 
 The technique of TDD is quite simple:
1
Write a failing test to prove code or functionality is missing from the end product. The
test is written as if the production code were already working, so the test failing
means there’s a bug in the production code. How do I know? The test is written
such that it would pass if the production code had no bugs.
In some languages other than JavaScript, the test might not even compile at
first, since the code doesn’t exist yet. Once it does run, it should be failing,
because the production code is still not working. This is where a lot of the
“design” in test-driven-design thinking happens.
2
Make the test pass by adding functionality to the production code that meets the expectations
of your test. The production code should be kept as simple as possible. Don’t touch
the test. You have to make it pass only by touching production code.
3
Refactor your code. When the test passes, you’re free to move on to the next unit
test or to refactor your code (both production code and tests) to make it more
readable, to remove code duplication, and so on. This is another point where
the “design” part happens. We refactor and can even redesign our components
while still keeping the old functionality.
Refactoring steps should be very small and incremental, and we run all the
tests after each small step to make sure we didn’t break anything with our
changes. Refactoring can be done after writing several tests or after writing each
test. It’s an important practice, because it ensures your code gets easier to read
and maintain, while still passing all of the previously written tests. There’s a
whole section (8.3) on refactoring later in the book.
DEFINITION
Refactoring means changing a piece of code without changing its
functionality. If you’ve ever renamed a method, you’ve done refactoring. If
you’ve ever split a large method into multiple smaller method calls, you’ve
refactored your code. The code still does the same thing, but it becomes eas-
ier to maintain, read, debug, and change. 
The preceding steps sound technical, but there’s a lot of wisdom behind them. Done
correctly, TDD can make your code quality soar, decrease the number of bugs, raise
your confidence in the code, shorten the time it takes to find bugs, improve your code’s


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


