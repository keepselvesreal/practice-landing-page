# 1.8 Integration tests (pp.17-21)

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


---
**Page 18**

18
CHAPTER 1
The basics of unit testing
fail as a team, and it can be difficult to figure out what caused the failure of the overall
operation (see figure 1.7).
As defined in The Complete Guide to Software Testing by Bill Hetzel (Wiley, 1988), integra-
tion testing is “an orderly progression of testing in which software and/or hardware
elements are combined and tested until the entire system has been integrated.”
Here’s my own variation on defining integration testing:
Integration testing is testing a unit of work without having full control over all of its real
dependencies, such as other components by other teams, other services, the time, the
network, databases, threads, random number generators, and more.
To summarize, an integration test uses real dependencies; unit tests isolate the unit of
work from its dependencies so that they’re easily consistent in their results and can
easily control and simulate any aspect of the unit’s behavior.
 Let’s apply the questions from section 1.7.2 to integration tests and consider what
you want to achieve with real-world unit tests: 
Can I run and get results from a test I wrote two weeks or months or years ago? 
If you can’t, how would you know whether you broke a feature that you created
earlier? Shared data and code changes regularly during the life of an application,
cdn.site.com
HAProxy
NGINX
foo.site.com
bar.site.com
Web app
Microservice
Queues
List
Golang
Web app
Workers
PostgreSQL
Books
Failure points
Failure points
Some page
Browser
Figure 1.7
You can have many failure points in an integration test. All the units have to work together, and each 
could malfunction, making it harder to find the source of a bug. 


---
**Page 19**

19
1.8
Integration tests
and if you can’t (or won’t) run tests for all the previously working features after
changing your code, you just might break it without knowing—this is known as
a regression. Regressions seem to occur a lot near the end of a sprint or release,
when developers are under pressure to fix existing bugs. Sometimes they intro-
duce new bugs inadvertently as they resolve old ones. Wouldn’t it be great to
know that you broke something within 60 seconds of breaking it? You’ll see how
that can be done later in this book.
DEFINITION
A regression is broken functionality—code that used to work. You
can also think of it as one or more units of work that once worked and now
don’t. 
Can any member of my team run and get results from tests I wrote two months ago?
This goes with the previous point but takes it up a notch. You want to make sure
that you don’t break someone else’s code when you change something. Many
developers fear changing legacy code in older systems for fear of not knowing
what other code depends on what they’re changing. In essence, they risk chang-
ing the system into an unknown state of stability.
Few things are scarier than not knowing whether the application still works,
especially when you didn’t write that code. If you have that safety net of unit
tests and know you aren’t breaking anything, you’ll be much less afraid of tak-
ing on code you’re less familiar with. 
Good tests can be accessed and run by anyone.
DEFINITION
Legacy code is defined by Wikipedia as “old computer source code
that is no longer supported on the standard hardware and environments”
(https://en.wikipedia.org/wiki/Legacy_system), but many shops refer to any
older version of the application currently under maintenance as legacy code.
It often refers to code that’s hard to work with, hard to test, and usually even
hard to read. A client once defined legacy code in a down-to-earth way: “code
that works.” Many people like to define legacy code as “code that has no
tests.” Working Effectively with Legacy Code by Michael Feathers (Pearson, 2004)
uses “code that has no tests” as an official definition of legacy code, and it’s a
definition to be considered while reading this book.
Can I run all the tests I’ve written in no more than a few minutes?
If you can’t run your tests quickly (seconds are better than minutes), you’ll run
them less often (daily, or even weekly or monthly in some places). The problem
is that when you change code, you want to get feedback as early as possible to
see if you broke something. The more time required between running the tests,
the more changes you make to the system, and the (many) more places you’ll
have to search for bugs when you find that you broke something. 
Good tests should run quickly.


---
**Page 20**

20
CHAPTER 1
The basics of unit testing
Can I run all the tests I’ve written at the push of a button?
If you can’t, it probably means that you have to configure the machine on
which the tests will run so that they run correctly (setting up a Docker envi-
ronment, or setting connection strings to the database, for example), or it
may mean that your unit tests aren’t fully automated. If you can’t fully auto-
mate your unit tests, you’ll probably avoid running them repeatedly, as will
everyone else on your team.
No one likes to get bogged down with configuring details to run tests, just to
make sure that the system still works. Developers have more important things to
do, like writing more features into the system. But they can’t do that if they
don’t know the state of the system.
Good tests should be easily executed in their original form, not manually.
Can I write a basic test in no more than a few minutes?
One of the easiest ways to spot an integration test is that it takes time to prepare
correctly and to implement, not just to execute. It takes time to figure out how to
write it because of all the internal, and sometimes external, dependencies. (A
database may be considered an external dependency.) If you’re not automating
the test, dependencies are less of a problem, but you’re losing all the benefits of
an automated test. The harder it is to write a test, the less likely you are to write
more tests or to focus on anything other than the “big stuff” that you’re worried
about. One of the strengths of unit tests is that they tend to test every little thing
that might break, not only the big stuff. People are often surprised at how many
bugs they can find in code they thought was simple and bug free. 
When you concentrate only on the big tests, the overall confidence in your
code is still very much lacking. Many parts of the code’s core logic aren’t tested
(even though you may be covering more components), and there may be many
bugs that you haven’t considered and might be “unofficially” worried about.
Good tests against the system should be easy and quick to write, once you’ve
figured out the patterns you want to use to test your specific set of objects, func-
tions, and dependencies (the domain model). 
Do my tests pass when there are bugs in another team’s code? Do my tests show the same
results when run on different machines or environments? Do my tests stop working if
there’s no database, network, or deployment?
These three points refer to the idea that our test code is isolated from various
dependencies. The test results are consistent because we have control over what
those indirect inputs into our system provide. We can have fake databases, fake
networks, fake time, and fake machine culture. In later chapters, I’ll refer to
those points as stubs and seams in which we can inject those stubs.
If I delete, move, or change one test, do other tests remain unaffected?
Unit tests usually don’t need to have any shared state, but integration tests often
do, such as an external database or service. Shared state can create a dependency


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


