# 1.10.0 Introduction [auto-generated] (pp.22-24)

---
**Page 22**

22
CHAPTER 1
The basics of unit testing
DEFINITION
Control flow code is any piece of code that has some sort of logic in
it, small as it may be. It has one or more of the following: an if statement, a
loop, calculations, or any other type of decision-making code. 
Getters and setters are good examples of code that usually doesn’t contain any logic
and so don’t require specific targeting by the tests. It’s code that will probably get used
by the unit of work you’re testing, but there’s no need to test it directly. But watch out:
once you add any logic inside a getter or setter, you’ll want to make sure that logic is
being tested. 
 In the next section, we’ll stop talking about what is a good test and talk about when
you might want to write tests. I’ll discuss test-driven development, because it is often
put in the same bucket as doing unit testing. I want to make sure we set the record
straight on that. 
1.10
Test-driven development
Once you know how to write readable, maintainable, and trustworthy tests with a unit
testing framework, the next question is when to write the tests. Many people feel that
the best time to write unit tests for software is after they’ve created some functionality
and just before they merge their code into remote source control. 
 Also, to be a bit blunt, a lot of people don’t believe writing tests is a good idea, but
have realized through trial and error that there are strict testing requirements in
source control reviews, so they have to write tests to appease the code review gods and
get their code merged into the main branch. (That kind of dynamic is a great source
of bad tests, and I’ll address it in the third part of this book.)
 A growing number of developers prefer writing unit tests incrementally, during the
coding session and before each piece of very small functionality is implemented. This
approach is called test-first or test-driven development (TDD).
NOTE
There are many different views on exactly what test-driven develop-
ment means. Some say it’s test-first development, and some say it means you
have a lot of tests. Some say it’s a way of designing, and others feel it could be
a way to drive your code’s behavior with only some design. In this book, TDD
means test-first development, with design taking an incremental role in the
technique (besides this section, TDD won’t be discussed in this book).
Figures 1.8 and 1.9 show the differences between traditional coding and TDD. TDD is
different from traditional development, as figure 1.9 shows. You begin by writing a test
that fails; then you move on to creating the production code, seeing the test pass, and
continuing on to either refactor your code or create another failing test.
 This book focuses on the technique of writing good unit tests, rather than on
TDD, but I’m a big fan of TDD. I’ve written several major applications and frame-
works using TDD, I’ve managed teams that utilize it, and I’ve taught hundreds of
courses and workshops on TDD and unit testing techniques. Throughout my career,
I’ve found TDD to be helpful in creating quality code, quality tests, and better designs


---
**Page 23**

23
1.10
Test-driven development
Write function,
class, or
application
Write tests
(if we have
time)
Run tests
(if we have
time)
Fix bugs
(if we have
time)
Figure 1.8
The traditional 
way of writing unit tests
Write a new
test to prove the
next small piece
of functionality is
missing or
wrong.
Simplest
possible
production
code ﬁx
Incremental
refactoring as
needed on test
or production
code
Run all tests.
Run all tests.
Run all tests.
New test
should compile
and fail
All tests should
be passing.
All tests should
be passing.
Repeat until you like the code.
Repeat until
you have
conﬁdence
in the code.
Design
Start here.
Think.
Design.
Figure 1.9
Test-driven development—a bird’s-eye view. Notice the circular nature of the process: 
write the test, write the code, refactor, write the next test. It shows the incremental nature of TDD: 
small steps lead to a quality end result with confidence.


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


