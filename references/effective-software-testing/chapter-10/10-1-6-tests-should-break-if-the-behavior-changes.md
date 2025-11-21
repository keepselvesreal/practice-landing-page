# 10.1.6 Tests should break if the behavior changes (pp.261-262)

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


---
**Page 262**

262
CHAPTER 10
Test code quality
if the behavior does not exist or is incorrect.” I am not afraid of purposefully intro-
ducing a bug in the code, running the tests, and seeing them red (and then revert-
ing the bug). 
10.1.7
Tests should have a single and clear reason to fail
We love tests that fail. They indicate problems in our code, usually long before the
code is deployed. But the test failure is the first step toward understanding and fixing
the bug. Your test code should help you understand what caused the bug.
 There are many ways you can do that. If your test follows the earlier principles, the
test is cohesive and exercises only one (hopefully small) behavior of the software sys-
tem. Give your test a name that indicates its intention and the behavior it exercises.
Make sure anyone can understand the input values passed to the method under test.
If the input values are complex, use good variable names that explain what they are
about and code comments in natural language. Finally, make sure the assertions are
clear, and explain why a value is expected. 
10.1.8
Tests should be easy to write
There should be no friction when it comes to writing tests. If it is hard to do so (per-
haps writing an integration test requires you to set up the database, create complex
objects one by one, and so on), it is too easy for you to give up and not do it.
 Writing unit tests tends to be easy most of the time, but it may get complicated
when the class under test requires too much setup or depends on too many other
classes. Integration and system tests also require each test to set up and tear down the
(external) infrastructure.
 Make sure tests are always easy to write. Give developers all the tools to do that. If
tests require a database to be set up, provide developers with an API that requires one
or two method calls and voilà—the database is ready for tests.
 Investing time in writing good test infrastructure is fundamental and pays off in
the long term. Remember the test base classes we created to facilitate SQL integra-
tion tests and all the POs we created to facilitate web testing in chapter 9? This is the
type of infrastructure I am talking about. After the test infrastructure was in place,
the rest was easy. 
10.1.9
Tests should be easy to read
I touched on this point when I said that tests should have a clear reason to fail. I will
reinforce it now. Your test code base will grow significantly. But you probably will not
read it until there is a bug or you add another test to the suite.
 It is well known that developers spend more time reading than writing code. There-
fore, saving reading time will make you more productive. All the things you know about
code readability and use in your production code apply to test code, as well. Do not be
afraid to invest some time in refactoring it. The next developer will thank you.


