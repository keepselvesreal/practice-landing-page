# 10.1.5 Tests should have strong assertions (pp.261-261)

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


