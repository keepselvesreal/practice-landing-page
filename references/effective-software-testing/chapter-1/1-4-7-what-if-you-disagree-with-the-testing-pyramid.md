# 1.4.7 What if you disagree with the testing pyramid? (pp.25-27)

---
**Page 25**

25
The testing pyramid, and where we should focus
under test? In other words, what parts of the system would be significantly affected by
a bug? These are the areas where I do some system testing.
 Remember the pesticide paradox: a single technique usually is not enough to iden-
tify all the bugs. Let me give you a real-world example from one of my previous proj-
ects. In developing an e-learning platform, one of our most important functionalities
was payment. The worst type of bug would prevent users from buying our product.
Therefore, we were rigorous in testing all the code related to payment. We used unit
tests for business rules related to what the user bought being converted into the right
product, access and permissions, and so on. Integration with the two payment gate-
ways we supported was tested via integration testing: the integration tests made real
HTTP calls to a sandbox web service provided by the payment gateways, and we tested
different types of users buying products with various credit cards. Finally, our system
tests represented the entire user journey in buying our product. These tests started a
Firefox browser, clicked HTML elements, submitted forms, and checked that the right
product was available after confirming payment.
 Figure 1.8 also includes manual testing. I’ve said that every test should be auto-
mated, but I see some value in manual testing when these tests focus on exploration
and validation. As a developer, it is nice to use and explore the software system you are
building from time to time, both for real and via a test script. Open the browser or the
app, and play with it—you may gain better insight into what else to test. 
1.4.7
What if you disagree with the testing pyramid?
Many people disagree about the idea of a testing pyramid and whether we should
favor unit testing. These developers argue for the testing trophy: a thinner bottom level
with unit tests, a bigger middle slice with integration tests, and a thinner top with sys-
tem tests. Clearly, these developers see the most value in writing integration tests.
 While I disagree, I see their point. In many software systems, most of the complex-
ity is in integrating components. Think of a highly distributed microservices architec-
ture: in such a scenario, the developer may feel more comfortable if the automated
tests make actual calls to other microservices instead of relying on stubs or mocks that
simulate them. Why write unit tests for something you have to test anyway via integra-
tion tests?
 In this particular case, as someone who favors unit testing, I would prefer to tackle
the microservices testing problem by first writing lots and lots of unit tests in each micro-
service to ensure that they all behaved correctly, investing heavily in contract design to
ensure that the microservices had clear pre- and post-conditions. Then, I would use
many integration tests to ensure that communication worked as expected and that the
normal variations in the distributed system did not break the system—yes, lots of them,
because their benefits would outweigh their costs in this scenario. I might even invest in
some smart (maybe AI-driven) tests to explore corner cases I could not see.
 Another common case I see in favor of integration testing rather than unit test-
ing involves database-centric information systems: that is, systems where the main


---
**Page 26**

26
CHAPTER 1
Effective and systematic software testing
responsibility is to store, retrieve, and display information. In such systems, the com-
plexity relies on ensuring that the flow of information successfully travels through the
UI to the database and back. Such applications often are not composed of complex
algorithms or business rules. In that case, integration tests to ensure that SQL queries
(which are often complex) work as expected and system tests to ensure that the over-
all application behaves as expected may be the way to go. As I said before and will say
many times in this book, context is king.
 I’ve written most of this section in the first person because it reflects my point of view
and is based on my experience as a developer. Favoring one approach over another is
largely a matter of personal taste, experience, and context. You should do the type of
testing you believe will benefit your software. I am not aware of any scientific evidence
that argues in favor of or against the testing pyramid. And in 2020, Trautsch and col-
leagues analyzed the fault detection capability of 30,000 tests (some unit tests, some
integration tests) and could not find any evidence that certain defect types are more
effectively detected by either test level. All the approaches have pros and cons, and you
will have to find what works best for you and your development team.
 I suggest that you read the opinions of others, both in favor of unit testing and in
favor of integration testing:
In Software Engineering at Google (Winters, Manshreck, and Wright, 2020), the
authors mention that Google often opts for unit tests, as they tend to be
cheaper and execute more quickly. Integration and system tests also happen,
but to a lesser extent. According to the authors, around 80% of their tests are
unit tests.
Ham Vocke (2018) defends the testing pyramid in Martin Fowler’s wiki.
Fowler himself (2021) discusses the different test shapes (testing pyramid and
testing trophy).
André Schaffer (2018) discusses how Spotify prefers integration testing over
unit testing.
Julia Zarechneva and Picnic, a scale-up Dutch company (2021), reason about
the testing pyramid.
TEST SIZES RATHER THAN THEIR SCOPE
Google also has an interesting definition of test sizes, which engineers consider when
designing test cases. A small test is a test that can be executed in a single process. Such
tests do not have access to main sources of test slowness or determinism. In other
words, they are fast and not flaky. A medium test can span multiple processes, use threads,
and make external calls (like network calls) to localhost. Medium tests tend to be
slower and flakier than small ones. Finally, large tests remove the localhost restriction
and can thus require and make calls to multiple machines. Google reserves large tests
for full end-to-end tests.
 The idea of classifying tests not in terms of their boundaries (unit, integration, sys-
tem) but in terms of how fast they run is also popular among many developers. Again,


---
**Page 27**

27
Exercises
what matters is that for each part of the system, your goal is to maximize the effective-
ness of the test. You want your test to be as cheap as possible to write and as fast as pos-
sible to run and to give you as much feedback as possible about the system’s quality.
 Most of the code examples in the remainder of this book are about methods,
classes, and unit testing, but the techniques can easily be generalized to coarse-
grained components. For example, whenever I show a method, you can think of it as a
web service. The reasoning will be the same, but you will probably have more test cases
to consider, as your component will do more things. 
1.4.8
Will this book help you find all the bugs?
I hope the answer to this question is clear from the preceding discussion: no! Never-
theless, the techniques discussed in this book will help you discover many bugs—
hopefully, all the important ones.
 In practice, many bugs are very complex. We do not even have the right tools to
search for some of them. But we know a lot about testing and how to find different
classes of bugs, and those are the ones we focus on in this book. 
Exercises
1.1
In your own words, explain what systematic testing is and how it is different
from non-systematic testing.
1.2
Kelly, a very experienced software tester, visits Books!, a social network focused
on matching people based on the books they read. Users do not report bugs
often, as the Books! developers have strong testing practices in place. However,
users say that the software is not delivering what it promises. What testing prin-
ciple applies here?
1.3
Suzanne, a junior software tester, has just joined a very large online payment
company in the Netherlands. As her first task, Suzanne analyzes the past two
years’ worth of bug reports. She observes that more than 50% of the bugs hap-
pen in the international payments module. Suzanne promises her manager that
she will design test cases that completely cover the international payments mod-
ule and thus find all the bugs.
Which of the following testing principles may explain why this is not possible?
A Pesticide paradox
B Exhaustive testing
C Test early
D Defect clustering
1.4
John strongly believes in unit testing. In fact, this is the only type of testing he does
for any project he’s part of. Which of the following testing principles will not help
convince John that he should move away from his “only unit testing” approach?
A Pesticide paradox
B Tests are context-dependent


