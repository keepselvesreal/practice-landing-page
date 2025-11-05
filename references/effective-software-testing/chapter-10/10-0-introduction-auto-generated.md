# 10.0 Introduction [auto-generated] (pp.258-259)

---
**Page 258**

258
Test code quality
You have probably noticed that once test infected, the number of JUnit tests a soft-
ware development team writes and maintains can become significant. In practice,
test code bases grow quickly. Moreover, we have observed that Lehman’s law of evo-
lution, “Code tends to rot, unless one actively works against it” (1980), also applies
to test code. A 2018 literature review by Garousi and Küçük shows that our body of
knowledge about things that can go wrong with test code is already comprehensive.
 As with production code, we must put extra effort into writing high-quality test code
bases so they can be maintained and developed sustainably. In this chapter, I discuss two
opposite perspectives of writing test code. First, we examine what constitutes good
and maintainable test code, and best practices that can help you keep complexity
under control. Then we look at what constitutes problematic test code. We focus on
key test smells that hinder test code comprehension and evolution.
 I have discussed some of this material informally in previous chapters. This
chapter consolidates that knowledge.
This chapter covers
Principles and best practices of good and 
maintainable test code
Avoiding test smells that hinder the 
comprehension and evolution of test code


---
**Page 259**

259
Principles of maintainable test code
10.1
Principles of maintainable test code
What does good test code look like? There is a great deal of literature about test code
quality, which I rely on in this section. Much of what I say here can be found in the
works of Langr, Hunt, and Thomas (2015); Meszaros (2007); and Beck (2019)—as
always, with my own twist.
10.1.1
Tests should be fast
Tests are a developer’s safety net. Whenever we perform maintenance or evolution in
source code, we use the feedback from the test suite to understand whether the system
is working as expected. The faster we get feedback from the test code, the better.
Slower test suites force us to run the tests less often, making them less effective. There-
fore, good tests are fast. There is no hard line that separates slow from fast tests. You
should apply common sense.
 If you are facing a slow test, consider the following:
Using mocks or stubs to replace slower components that are part of the test
Redesigning the production code so slower pieces of code can be tested sepa-
rately from fast pieces of code
Moving slower tests to a different test suite that you can run less often
Sometimes you cannot avoid slow tests. Think of SQL tests: they are much slower than
unit tests, but there is not much you can do about it. I separate slow tests from fast
ones: this way, I can run my fast tests all the time and the slow tests when I modify the
production code that has a slow test tied to it. I also run the slow tests before commit-
ting my code and in continuous integration. 
10.1.2
Tests should be cohesive, independent, and isolated
Tests should be as cohesive, independent, and isolated as possible. Ideally, a single test
method should test a single functionality or behavior of the system. Fat tests (or, as the
test smells community calls them, eager tests) exercise multiple functionalities and are
often complex in terms of implementation. Complex test code reduces our ability to
understand what is being tested at a glance and makes future maintenance more diffi-
cult. If you face such a test, break it into multiple smaller tests. Simpler and shorter
tests are better.
 Moreover, tests should not depend on other tests to succeed. The test result should
be the same whether the test is executed in isolation or together with the rest of the
test suite. It is not uncommon to see cases where test B only works if test A is executed
first. This is often the case when test B relies on the work of test A to set up the envi-
ronment for it. Such tests become highly unreliable.
 If you have a test that is somewhat dependent on another test, refactor the test
suite so each test is responsible for setting up the whole environment it needs.
Another tip that helps make tests independent is to make sure your tests clean up
their messes: for example, by deleting any files they created on the disk and cleaning


