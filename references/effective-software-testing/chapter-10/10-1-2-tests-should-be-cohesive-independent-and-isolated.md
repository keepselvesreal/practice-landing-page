# 10.1.2 Tests should be cohesive, independent, and isolated (pp.259-260)

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


---
**Page 260**

260
CHAPTER 10
Test code quality
up values they inserted into a database. This will force tests to set up things themselves
and not rely on data that was already there. 
10.1.3
Tests should have a reason to exist
You want tests that either help you find bugs or help you document behavior. You do
not want tests that, for example, increase code coverage. If a test does not have a good
reason to exist, it should not exist. Remember that you must maintain all your tests.
The perfect test suite is one that can detect all the bugs with the minimum number of
tests. While having such a perfect test suite is impossible, making sure you do not have
useless tests is a good start. 
10.1.4
Tests should be repeatable and not flaky
A repeatable test gives the same result no matter how many times it is executed. Devel-
opers lose their trust in tests that present flaky behavior (sometimes pass and some-
times fail, without any changes in the system or test code).
 Flaky tests hurt the productivity of software development teams. It is hard to know
whether a flaky test is failing because the behavior is buggy or because it is flaky. Little
by little, flaky tests can make us lose confidence in our test suites. Such lack of confi-
dence may lead us to deploy our systems even though the tests fail (they may be bro-
ken because of flakiness, not because the system is misbehaving).
 The prevalence and impact of flaky tests in the software development world have
increased over time (or, at least, we talk more about them now). Companies like
Google and Facebook have publicly talked about problems caused by flaky tests.
 A test can become flaky for many reasons:
Because it depends on external or shared resources—If a test depends on a database,
many things can cause flakiness. For example, the database may not be available
at the moment the test is executed, it may contain data that the test does not
expect, or two developers may be running the test suite at the same time and
sharing the same database, causing one to break the test of the other.
Due to improper time-outs—This is a common reason in web testing. Suppose a test
has to wait for something to happen in the system: for example, a request com-
ing back from a web service, which is then displayed in an HTML element. If
the web application is slower than normal, the test may fail because it did not
wait long enough.
Because of a hidden interaction between different test methods—Test A somehow influ-
ences the result of test B, possibly causing it to fail.
The work of Luo et al. (2014) also shed light on the causes of flaky tests. After analyz-
ing 201 flaky tests in open source systems, the authors noticed the following:
Async wait, concurrency, and test order dependency are the three most com-
mon causes of flakiness.
Most flaky tests are flaky from the time they are written.


