# 10.1.3 Tests should have a reason to exist (pp.260-260)

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


