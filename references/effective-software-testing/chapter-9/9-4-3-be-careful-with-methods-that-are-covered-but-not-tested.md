# 9.4.3 Be careful with methods that are covered but not tested (pp.255-255)

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


