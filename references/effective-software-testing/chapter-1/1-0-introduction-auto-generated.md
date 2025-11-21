# 1.0 Introduction [auto-generated] (pp.1-2)

---
**Page 1**

1
Effective and systematic
software testing
The developer community no longer needs to argue about the importance of soft-
ware testing. Every software developer understands that software failures may cause
severe damage to businesses, people, or even society as a whole. And although soft-
ware developers once were primarily responsible for building software systems,
today they are also responsible for the quality of the software systems they produce.
 Our community has produced several world-class tools to help developers test,
including JUnit, AssertJ, Selenium, and jqwik. We have learned to use the process
of writing tests to reflect on what programs need to do and get feedback about the
code design (or class design, if you are using an object-oriented language). We
have also learned that writing test code is challenging, and paying attention to test
code quality is fundamental for the graceful evolution of the test suite. And finally,
we know what the common bugs are and how to look for them.
This chapter covers
Understanding the importance of effective, 
systematic testing
Recognizing why testing software is difficult 
and why bug-free systems do not exist
Introducing the testing pyramid


---
**Page 2**

2
CHAPTER 1
Effective and systematic software testing
 But while developers have become very good at using testing tools, they rarely
apply systematic testing techniques to explore and find bugs. Many practitioners
argue that tests are a feedback tool and should be used mostly to help you develop.
Although this is true (and I will show throughout this book how to listen to your test
code), tests can also help you find bugs. After all, that is what software testing is all
about: finding bugs!
 Most developers do not enjoy writing tests. I have heard many reasons: writing
production code is more fun and challenging, software testing is too time-consuming,
we are paid to write production code, and so on. Developers also overestimate how
much time they spend on testing, as Beller and colleagues found in a nice empirical
study with hundreds of developers in 2019. My goal with this book is to convince you
that (1) as a developer, it is your responsibility to ensure the quality of what you pro-
duce; (2) that tests are the only tools to help you with that responsibility; and (3)
that if you follow a collection of techniques, you can test your code in an effective
and systematic way.
 Note the words I used: effective and systematic. Soon you will understand what I
mean. But first, let me convince you of the necessity of tests.
1.1
Developers who test vs. developers who do not
It is late on Friday afternoon, and John is about to implement the last feature of the
sprint. He is developing an agile software management system, and this final feature
supports developers during planning poker.
John is about to implement the feature’s core method. This method receives a list of
estimates and produces, as output, the names of the two developers who should
explain their points of view. This is what he plans to do:
 
Planning poker
Planning poker is a popular agile estimation technique. In a planning poker session,
developers estimate the effort required to build a specific feature of the backlog.
After the team discusses the feature, each developer gives an estimate: a number
ranging from one to any number the team defines. Higher numbers mean more effort
to implement the feature. For example, a developer who estimates that a feature is
worth eight points expects it to take four times more effort than a developer who esti-
mates the feature to be worth two points.
The developer with the smallest estimate and the developer with the highest esti-
mate explain their points of view to the other members of the team. After more dis-
cussion, the planning poker repeats until the team members agree about how much
effort the feature will take. You can read more about the planning poker technique in
Kanban in Action by Marcus Hammarberg and Joakim Sundén (2014).


