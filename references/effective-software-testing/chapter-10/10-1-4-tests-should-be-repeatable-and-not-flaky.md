# 10.1.4 Tests should be repeatable and not flaky (pp.260-261)

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


---
**Page 261**

261
Principles of maintainable test code
Flaky tests are rarely due to the platform-specifics (they do not fail because of
different operating systems).
Flakiness is often due to dependencies on external resources and can be fixed
by cleaning the shared state between test runs.
Detecting the cause of a flaky test is challenging. Software engineering researchers
have proposed automated tools to detect flaky tests. If you are curious about such
tools and the current state of the art, I suggest that you read the following:
The work of Bell et al. (2018), who proposed DeFlaker, a tool that monitors the
coverage of the latest code changes and marks a test as flaky if any new failing
test did not exercise any of the changed code.
The work of Lam et al. (2019), who proposed iDFlakies, a tool that executes
tests in random order, looking for flakiness.
Because these tools are not fully ready, it is up to us to find the flaky tests and fix them.
Meszaros has made a decision table that may help you with that task. You can find it in
his book (2007) or on his website (http://xunitpatterns.com/Erratic%20Test.html). 
10.1.5
Tests should have strong assertions
Tests exist to assert that the exercised code behaved as expected. Writing good asser-
tions is therefore key to a good test. An extreme example of a test with bad assertions
is one with no assertions. This seems strange, but believe it or not, it happens—not
because we do not know what we are doing, but because writing a good assertion can
be tricky. In cases where observing the outcome of behavior is not easily achievable, I
suggest refactoring the class or method under test to increase its observability. Revisit
chapter 7 if you need tips for how to do so.
 Assertions should be as strong as possible. You want your tests to fully validate the
behavior and break if there is any slight change in the output. Imagine that a method
calculateFinalPrice() in a ShoppingCart class changes two properties: finalPrice
and the taxPaid. If your tests only ensure the value of the finalPrice property, a bug
may happen in the way taxPaid is set, and your tests will not notice it. Make sure you
are asserting everything that needs to be asserted. 
10.1.6
Tests should break if the behavior changes
Tests let you know that you broke the expected behavior. If you break the behavior
and the test suite is still green, something is wrong with your tests. That may hap-
pen because of weak assertions (which we have discussed) or because the method is
covered but not tested (this happens, as discussed in chapter 9). Also recall that I
mentioned the work of Vera-Pérez and colleagues (2019) and the existence of
pseudo-tested methods.
 Whenever you write a test, make sure it will break if the behavior changes. The
TDD cycle allows developers to always see the test breaking. That happens because
the behavior is not yet implemented, but I like the idea of “let’s see if the test breaks


