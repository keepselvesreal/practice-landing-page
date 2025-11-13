# 1.7.1 What is a good unit test? (pp.15-16)

---
**Page 15**

15
1.7
Characteristics of a good unit test
methods like this, so tests are even easier to write. I’ll talk about that in chapter 2.
First, let’s talk a bit about the main subject of this book: good unit tests. 
1.7
Characteristics of a good unit test
No matter what programming language you’re using, one of the most difficult aspects
of defining a unit test is defining what’s meant by a good one. Of course, good is rela-
tive, and it can change whenever we learn something new about coding. That may
seem obvious, but it really isn’t. I need to explain why we need to write better tests—
understanding what a unit of work is isn’t enough.
 Based on my own experience, involving many companies and teams over the years,
most people who try to unit test their code either give up at some point or don’t actu-
ally perform unit tests. They waste a lot of time writing problematic tests, and they give
up when they have to spend a lot of time maintaining them, or worse, they don’t trust
their results. 
 There’s no point in writing a bad unit test, unless you’re in the process of learning
how to write a good one. There are more downsides than upsides to writing bad tests,
such as wasting time debugging buggy tests, wasting time writing tests that bring no
benefit, wasting time trying to understand unreadable tests, and wasting time writing
tests only to delete them a few months later. There’s also a huge issue with maintain-
ing bad tests, and with how they affect the maintainability of production code. Bad
tests can actually slow down your development speed, not only when writing test code,
but also when writing production code. I’ll touch on all these things later in the book.
 By learning what a good unit test is, you can be sure you aren’t starting off on a
path that will be hard to fix later on, when the code becomes a nightmare. We’ll also
define other forms of tests (component, end to end, and more) later in the book.
1.7.1
What is a good unit test? 
Every good automated test (not just unit tests) should have the following properties:
It should be easy to understand the intent of the test author.
It should be easy to read and write.
It should be automated.
It should be consistent in its results (it should always return the same result if
you don’t change anything between runs).
It should be useful and provide actionable results.
Anyone should be able to run it with the push of a button.
When it fails, it should be easy to detect what was expected and determine how
to pinpoint the problem.
A good unit test should also exhibit the following properties: 
It should run quickly.
It should have full control of the code under test (more on that in chapter 3).
It should be fully isolated (run independently of other tests).


---
**Page 16**

16
CHAPTER 1
The basics of unit testing
It should run in memory without requiring system files, networks, or databases.
It should be as synchronous and linear as possible when that makes sense (no
parallel threads if we can help it).
It’s impossible for all tests to follow the properties of a good unit test, and that’s
fine. Such tests will simply transition to the realm of integration testing (the topic of
section 1.8). Still, there are ways to refactor some of your tests to conform to these
properties.
REPLACING THE DATABASE (OR ANOTHER DEPENDENCY) WITH A STUB
We’ll discuss stubs in later chapters, but, in short, they are fake dependencies that
emulate the real ones. Their purpose is to simplify the process of testing because they
are easier to set up and maintain.
 Beware of in-memory databases, though. They can help you isolate tests from
each other (as long as you don’t share database instances between tests) and thus
adhere to the properties of good unit tests, but such databases lead to an awkward,
in-between spot. In-memory databases aren’t as easy to set up as stubs. At the same
time, they don’t provide as strong guarantees as real databases. Functionality-wise, an
in-memory database may differ drastically from the production one, so tests that pass
an in-memory database may fail the real one, and vice versa. You’ll often have to rerun
the same tests manually against the production database to gain additional confi-
dence that your code works. Unless you use a small and standardized set of SQL fea-
tures, I recommend sticking to either stubs (for unit tests) or real databases (for
integration testing).
 The same is true for solutions like jsdom. You can use it to replace the real DOM,
but make sure it supports your particular use cases. Don’t write tests that require you
to manually recheck them.
EMULATING ASYNCHRONOUS PROCESSING WITH LINEAR, SYNCHRONOUS TESTS
With the advent of promises and async/await, asynchronous coding has become stan-
dard in JavaScript. Our tests can still verify asynchronous code synchronously, though.
Usually that means triggering callbacks directly from the test or explicitly waiting for
an asynchronous operation to finish executing.
1.7.2
A unit test checklist
Many people confuse the act of testing their software with the concept of a unit test.
To start off, ask yourself the following questions about the tests you’ve written and exe-
cuted up to now:
Can I run and get results from a test I wrote two weeks or months or years ago?
Can any member of my team run and get results from tests I wrote two
months ago?
Can I run all the tests I’ve written in no more than a few minutes?
Can I run all the tests I’ve written at the push of a button?


