# 1.9 Finalizing our definition (pp.21-22)

---
**Page 21**

21
1.9
Finalizing our definition
between tests. For example, running tests in the wrong order can corrupt the
state for future tests.
WARNING
Even experienced unit testers can find that it may take 30 minutes
or more to figure out how to write the very first unit test against a domain
model they’ve never unit tested before. This is part of the work and is to be
expected. The second and subsequent tests on that domain model should be
very easy to accomplish once you’ve figured out the entry and exit points of
the unit of work. 
We can recognize three main criteria in the previous questions and answers:
Readability—If we can’t read it, then it’s hard to maintain, hard to debug, and
hard to know what’s wrong.
Maintainability—If maintaining the test or production code is painful because
of the tests, our lives will become a living nightmare. 
Trust—If we don’t trust the results of our tests when they fail, we’ll start manu-
ally testing again, losing all the time benefit the tests are supposed to provide. If
we don’t trust the tests when they pass, we’ll start debugging more, again losing
any time benefit. 
From what I’ve explained so far about what a unit test is not and what features need to
be present for testing to be useful, I can now start to answer the primary question this
chapter poses: what is a good unit test?
1.9
Finalizing our definition
Now that I’ve covered the important properties that a unit test should have, I’ll define
unit tests once and for all:
A unit test is an automated piece of code that invokes the unit of work through an entry
point and then checks one of its exit points. A unit test is almost always written using a
unit testing framework. It can be written easily and runs quickly. It’s trustworthy,
readable, and maintainable. It is consistent as long as the production code we control has
not changed.
This definition certainly looks like a tall order, particularly considering how many
developers implement unit tests poorly. It makes us take a hard look at the way we, as
developers, have implemented testing up until now, compared to how we’d like to
implement it. (Trustworthy, readable, and maintainable tests are discussed in depth in
chapters 7 through 9.)
 In the first edition of this book, my definition of a unit test was slightly different. I
used to define a unit test as “only running against control flow code,” but I no longer
think that’s true. Code without logic is usually used as part of a unit of work. Even
properties with no logic will get used by a unit of work, so they don’t have to be specif-
ically targeted by tests.


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


