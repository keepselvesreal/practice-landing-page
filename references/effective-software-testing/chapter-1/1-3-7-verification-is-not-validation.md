# 1.3.7 Verification is not validation (pp.18-19)

---
**Page 18**

18
CHAPTER 1
Effective and systematic software testing
other files in the system. As a software developer, you may have to watch and learn
from your software system. Data other than the source code may help you prioritize
your testing efforts. 
1.3.5
No matter what testing you do, it will never be perfect or enough
As Dijkstra used to say, “Program testing can be used to show the presence of bugs, but
never to show their absence.” In other words, while we may find more bugs by simply
testing more, our test suites, however large they may be, will never ensure that the soft-
ware system is 100% bug-free. They will only ensure that the cases we test for behave
as expected.
 This is an important principle to understand, as it will help you set your (and your
customers’) expectations. Bugs will still happen, but (hopefully) the money you pay
for testing and prevention will pay off by allowing only the less impactful bugs to go
through. “You cannot test everything” is something we must accept.
NOTE
Although monitoring is not a major topic in this book, I recommend
investing in monitoring systems. Bugs will happen, and you need to be sure
you find them the second they manifest in production. That is why tools such
as the ELK stack (Elasticsearch, Logstash, and Kibana; www.elastic.co) are
becoming so popular. This approach is sometimes called testing in production
(Wilsenach, 2017). 
1.3.6
Context is king
The context plays an important role in how we devise test cases. For example, devising
test cases for a mobile app is very different from devising test cases for a web applica-
tion or software used in a rocket. In other words, testing is context-dependent.
 Most of this book tries to be agnostic about context. The techniques I discuss
(domain testing, structural testing, property-based testing, and so on) can be applied
in any type of software system. Nevertheless, if you are working on a mobile app, I rec-
ommend reading a book dedicated to mobile testing after you read this one. I give
some context-specific tips in chapter 9, where I discuss larger tests. 
1.3.7
Verification is not validation
Finally, note that a software system that works flawlessly but is of no use to its users is
not a good software system. As a reviewer of this book said to me, “Coverage of code is
easy to measure; coverage of requirements is another matter.” Software testers face
this absence-of-errors fallacy when they focus solely on verification and not on validation.
 A popular saying that may help you remember the difference is, “Verification is
about having the system right; validation is about having the right system.” This book
primarily covers verification techniques. In other words, I do not focus on techniques
to, for example, collaborate with customers to understand their real needs; rather, I
present techniques to ensure that, given a specific requirement, the software system
implements it correctly.


---
**Page 19**

19
The testing pyramid, and where we should focus
 Verification and validation can walk hand in hand. In this chapter’s example about
the planning poker algorithm, this was what happened when Eleanor imagined all the
developers estimating the same effort. The product owner did not think of this case. A
systematic testing approach can help you identify corner cases that even the product
experts did not envision. 
1.4
The testing pyramid, and where we should focus
Whenever we talk about pragmatic testing, one of the first decisions we need to make
is the level at which to test the code. By a test level, I mean the unit, integration, or system
level. Let’s quickly look at each of them.
1.4.1
Unit testing
In some situations, the tester’s goal is to test a single feature of the software, purpose-
fully ignoring the other units of the system. This is basically what we saw in the plan-
ning poker example. The goal was to test the identifyExtremes() method and
nothing else. Of course, we cared about how this method would interact with the rest
of the system, and that is why we tested its contracts. However, we did not test it
together with the other pieces of the system.
 When we test units in isolation, we are doing unit testing. This test level offers the
following advantages:
Unit tests are fast. A unit test usually takes just a couple of milliseconds to exe-
cute. Fast tests allow us to test huge portions of the system in a small amount of
time. Fast, automated test suites give us constant feedback. This fast safety net
makes us feel more comfortable and confident in performing evolutionary
changes to the software system we are working on.
Unit tests are easy to control. A unit test tests the software by giving certain parame-
ters to a method and then comparing the return value of this method to the
expected result. These input values and the expected result value are easy to
adapt or modify in the test. Again, look at the identifyExtremes() example
and how easy it was to provide different inputs and assert its output.
Unit tests are easy to write. They do not require a complicated setup or additional
work. A single unit is also often cohesive and small, making the tester’s job eas-
ier. Tests become much more complicated when we have databases, frontends,
and web services all together.
As for disadvantages, the following should be considered:
Unit tests lack reality. A software system is rarely composed of a single class. The
large number of classes in a system and their interaction can cause the system to
behave differently in its real application than in the unit tests. Therefore, unit
tests do not perfectly represent the real execution of a software system.
Some types of bugs are not caught. Some types of bugs cannot be caught at the unit
test level; they only happen in the integration of the different components


