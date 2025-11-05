# 1.4.8 Will this book help you find all the bugs? (pp.27-27)

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


