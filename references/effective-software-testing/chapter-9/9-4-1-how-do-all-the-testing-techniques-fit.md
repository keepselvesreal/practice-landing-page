# 9.4.1 How do all the testing techniques fit? (pp.254-255)

---
**Page 254**

254
CHAPTER 9
Writing larger tests
Note how long and complex the test is. We discussed a similar problem, and our
solution was to provide a web service that enabled us to skip many of the page visits.
But if visiting all these pages is part of the journey under test, the test should visit
each one. If one or two of these steps are not part of the journey, you can use the
web services. 
ASSERTIONS SHOULD USE DATA THAT COMES FROM THE POS
In the Find Owners test, our assertions focused on checking whether all the owners
were on the list. In the code, the FindOwnersPage PO provided an all() method that
returned the owners. The test code was only responsible for the assertion. This is a
good practice. Whenever your tests require information from the page for the asser-
tion, the PO provides this information. Your JUnit test should not locate HTML ele-
ments by itself. However, the assertions stay in the JUnit test code. 
PASS IMPORTANT CONFIGURATIONS TO THE TEST SUITE
The example test suite has some hard-coded details, such as the local URL of the
application (right now, it is localhost:8080) and the browser to run the tests (currently
Safari). However, you may need to change these configurations dynamically. For
example, your continuous integration may need to run the web app on a different
port, or you may want to run your test suite on Chrome.
 There are many different ways to pass configuration to Java tests, but I usually opt
for the simplest approach: everything that is a configuration is provided by a method
in  my PageObject base class. For example, a String baseUrl() method returns the
base URL of the application, and a WebDriver browser() method returns the con-
crete instance of WebDriver. These methods then read from a configuration file or an
environment variable, as those are easy to pass via build scripts. 
RUN YOUR TESTS IN MULTIPLE BROWSERS
You should run your tests in multiple browsers to be sure everything works every-
where. But I don’t do this on my machine, because it takes too much time. Instead, my
continuous integration (CI) tool has a multiple-stage process that runs the web test
suite multiple times, each time passing a different browser. If configuring such a CI is
an issue, consider using a service such as SauceLabs (https://saucelabs.com), which
automates this process for you. 
9.4
Final notes on larger tests
I close this chapter with some points I have not yet mentioned regarding larger tests.
9.4.1
How do all the testing techniques fit?
In the early chapters of this book, our goal was to explore techniques that would help
you engineer test cases systematically. In this chapter, we discuss a more orthogonal
topic: how large should our tests be? I have shown you examples of larger component
tests, integration tests, and system tests. But regardless of the test level, engineering
good test cases should still be the focus.


---
**Page 255**

255
Final notes on larger tests
 When you write a larger test, use the requirement and its boundaries, the structure
of the code, and the properties it should uphold to engineer good test cases. The chal-
lenge is that an entire component has a much larger requirement and a much larger
code base, which means many more tests to engineer.
 I follow this rule of thumb: exercise everything at the unit level (you can easily
cover entire requirements and structures at the unit level), and exercise the most
important behavior in larger tests (so you have more confidence that the program will
work when the pieces are put together). It may help to reread about the testing pyra-
mid in section 1.4 in chapter 1.
9.4.2
Perform cost/benefit analysis
One of the testing mantras is that a good test is cheap to write but can capture import-
ant bugs. Unit tests are cheap to write, so we do not have to think much about cost.
 Larger tests may not be cheap to write, run, or maintain. I have seen integration
test suites that take hours to run—and cases where developers spend hours writing a
single integration test.
 Therefore, it is fundamental to perform a simple cost/benefit analysis. Questions
like “How much will it cost me to write this test?” “How much will it cost to run?”
“What is the benefit of this test? What bugs will it catch?” and “Is this functionality
already covered by unit tests? If so, do I need to cover it via integration tests, too?” may
help you understand whether this is a fundamental test.
 The answer will be “yes” in many cases. The benefits outweigh the costs, so you
should write the test. If the cost is too high, consider simplifying your test. Can you
stub parts of the test without losing too much? Can you write a more focused test that
exercises a smaller part of the system? As always, there is no single good answer or
golden rule to follow. 
9.4.3
Be careful with methods that are covered but not tested
Larger tests exercise more classes, methods, and behaviors together. In addition to all
the trade-offs discussed in this chapter, with larger tests, the chances of covering a
method but not testing it are much higher.
 Vera-Pérez and colleagues (2019) coined the term pseudo-tested methods. These
methods are tested, but if we replace their entire implementation with a simple
return null, tests still pass. And believe it or not, Vera-Pérez and colleagues show that
pseudo-tested methods happen in the wild, even in important open source projects.
This is another reason I defend both unit tests and larger tests, used together to
ensure that everything works. 
9.4.4
Proper code infrastructure is key
Integration and system tests both require a decent infrastructure behind the scenes.
Without it, we may spend too much time setting up the environment or asserting that
behavior was as expected. My key advice here is to invest in test infrastructure. Your


