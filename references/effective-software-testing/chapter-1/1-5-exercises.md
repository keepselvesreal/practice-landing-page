# 1.5 Exercises (pp.27-29)

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


---
**Page 28**

28
CHAPTER 1
Effective and systematic software testing
C Absence-of-errors fallacy
D Test early
1.5
Sally just started some consultancy for a company that develops a mobile app to
help people keep up with their daily exercises. The development team mem-
bers are fans of automated software testing and, more specifically, unit tests.
They have high unit test code coverage (>95% branch coverage), but users still
report a significant number of bugs.
Sally, who is well versed in software testing, explains a testing principle to the
team. Which of the following principles did she talk about?
A Pesticide paradox
B Exhaustive testing
C Test early
D Defect clustering
1.6
Consider this requirement: “A web shop runs a batch job, once a day, to deliver all
orders that have been paid. It also sets the delivery date according to whether the
order is from an international customer. Orders are retrieved from an external
database. Orders that have been paid are then sent to an external web service.”
As a tester, you have to decide which test level (unit, integration, or system)
to apply. Which of the following statements is true?
A Integration tests, although more complicated (in terms of automation)
than unit tests, would provide more help in finding bugs in the communi-
cation with the web service and/or the communication with the database.
B Given that unit tests could be easily written (by using mocks) and would
cover as much as integration tests would, unit tests are the best option for
any situation.
C The most effective way to find bugs in this code is through system tests. In
this case, the tester should run the entire system and exercise the batch
process. Because this code can easily be mocked, system tests would also
be cheap.
D While all the test levels can be used for this problem, testers are more
likely to find more bugs if they choose one level and explore all the possi-
bilities and corner cases there.
1.7
Delft University of Technology (TU Delft) has built in-house software to handle
employee payroll. The application uses Java web technologies and stores data in
a Postgres database. The application frequently retrieves, modifies, and inserts
large amounts of data. All this communication is done by Java classes that send
(complex) SQL queries to the database.
As testers, we know that a bug can be anywhere, including in the SQL que-
ries. We also know that there are many ways to exercise our system. Which one
of the following is not a good option to detect bugs in SQL queries?


---
**Page 29**

29
Summary
A Unit testing
B Integration testing
C System testing
D Stress testing
1.8
Choosing the level of a test involves a trade-off, because each test level has
advantages and disadvantages. Which one of the following is the main advan-
tage of a test at the system level?
A The interaction with the system is much closer to reality.
B In a continuous integration environment, system tests provide real feed-
back to developers.
C Because system tests are never flaky, they provide developers with more
stable feedback.
D A system test is written by product owners, making it closer to reality.
1.9
What is the main reason the number of recommended system tests in the test-
ing pyramid is smaller than the number of unit tests?
A Unit tests are as good as system tests.
B System tests tend to be slow and are difficult to make deterministic.
C There are no good tools for system tests.
D System tests do not provide developers with enough quality feedback. 
Summary
Testing and test code can guide you through software development. But soft-
ware testing is about finding bugs, and that is what this book is primarily about.
Systematic and effective software testing helps you design test cases that exer-
cise all the corners of your code and (hopefully) leaves no space for unex-
pected behavior.
Although being systematic helps, you can never be certain that a program does
not have bugs.
Exhaustive testing is impossible. The life of a tester involves making trade-offs
about how much testing is needed.
You can test programs on different levels, ranging from testing small methods
to testing entire systems with databases and web services. Each level has advan-
tages and disadvantages.


