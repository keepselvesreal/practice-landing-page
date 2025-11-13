# 1.7.2 A unit test checklist (pp.16-17)

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


---
**Page 17**

17
1.8
Integration tests
Can I write a basic test in no more than a few minutes?
Do my tests pass when there are bugs in another team’s code?
Do my tests show the same results when run on different machines or environ-
ments?
Do my tests stop working if there’s no database, network, or deployment?
If I delete, move, or change one test, do other tests remain unaffected?
If you answered “no” to any of these questions, there’s a high probability that what
you’re implementing either isn’t fully automated or it isn’t a unit test. It’s definitely
some kind of test, and it might be as important as a unit test, but it has drawbacks com-
pared to tests that would let you answer yes to all of those questions.
 “What was I doing until now?” you might ask. You’ve been doing integration testing. 
1.8
Integration tests
I consider integration tests to be any tests that don’t live up to one or more of the condi-
tions outlined previously for good unit tests. For example, if the test uses the real net-
work, the real rest APIs, the real system time, the real filesystem, or a real database, it
has stepped into the realm of integration testing.
 If a test doesn’t have control of the system time, for example, and it uses the cur-
rent new Date() in the test code, then every time the test executes, it’s essentially a dif-
ferent test because it uses a different time. It’s no longer consistent. That’s not a bad
thing per se. I think integration tests are important counterparts to unit tests, but they
should be separated from them to achieve a feeling of “safe green zone,” which is dis-
cussed later in this book.
 If a test uses the real database, it’s no longer only running in memory—its actions
are harder to erase than when using only in-memory fake data. The test will also run
longer, and we won’t easily be able to control how long data access takes. Unit tests
should be fast. Integration tests are usually much slower. When you start having hun-
dreds of tests, every half-second counts.
 Integration tests increase the risk of another problem: testing too many things at
once. For example, suppose your car breaks down. How do you learn what the prob-
lem is, let alone fix it? An engine consists of many subsystems working together,
each relying on the others to help produce the final result: a moving car. If the car
stops moving, the fault could be with any of the subsystems—or with more than one.
It’s the integration of those subsystems (or layers) that makes the car move. You
could think of the car’s movement as the ultimate integration test of these parts as
the car goes down the road. If the test fails, all the parts fail together; if it succeeds,
all the parts succeed. 
 The same thing happens in software. The way most developers test their function-
ality is through the final functionality of the app or REST API or UI. Clicking some
button triggers a series of events—functions, modules, and components working
together to produce the final result. If the test fails, all of these software components


