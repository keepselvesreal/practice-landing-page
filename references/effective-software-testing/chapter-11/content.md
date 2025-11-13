# Wrapping up the book (pp.276-281)

---
**Page 276**

276
Wrapping up the book
We are now at the end of this book. The book comprises a lot of my knowledge
about practical software testing, and I hope you now understand the testing tech-
niques that have supported me throughout the years. In this chapter, I will say some
final words about how I see effective testing in practice and reinforce points that I
feel should be uppermost in your mind.
11.1
Although the model looks linear, iterations 
are fundamental
Figure 11.1 (which you saw for the first time back in chapter 1) illustrates what I
call effective software testing. Although this figure and the order of the chapters in this
book may give you a sense of linearity (that is, you first do specification-based test-
ing and then move on to structural testing), this is not the case. You should not
view the proposed flow as a sort of testing waterfall.
 Software development is an iterative process. You may start with specification-
based testing, then go to structural testing, and then feel you need to go back to
specification-based testing. Or you may begin with structural testing because the
This chapter covers
Revisiting what was discussed in this book


---
**Page 277**

277
Bug-free software development: Reality or myth?
tests that emerged from your TDD sessions are good enough. There is nothing wrong
with customizing the process to specific cases.
 As you become more experienced with testing, you will develop a feeling for the
best order in which to apply the techniques. As long as you master them all and
understand the goals and outputs of each, that will come naturally. 
11.2
Bug-free software development: Reality or myth?
The techniques explore the source code from many different perspectives. That may
give you the impression that if you apply them all, no bugs will ever happen. Unfortu-
nately, this is not the case.
 The more you test your code from different angles, the greater the chances of
revealing bugs you did not see previously. But the software systems we work with today
are very complex, and bugs may happen in corner cases that involve dozens of differ-
ent components working together. Domain knowledge may help you see such cases.
So, deeply understanding the business behind the software systems you test is funda-
mental in foreseeing complex interactions between systems that may lead to crashes
or bugs.
Developer
Builds a
feature
T
o guide
e
esting t
d velopment
Requirement
analysis
Test-driven
development
Design for
testability
Design by
contracts
Eﬀective and systematic testing
Speciﬁcation
testing
Bound
y
ar
testing
Structural
testing
Intelligent testing
Mutation
testing
Larger tests
Integration
testing
System
testing
Unit w h d
s
it
iﬀerent roles
and
iliti
responsib
es
Unit testing
Property-
based testing
Here, we discussed ideas
that will help us in
implementing the feature
with conﬁdence and with
testability in mind.
Here, we discussed different techniques
that will exercise our implementation
from many different angles and help us
to identify possible bugs in our code.
Mocks,
stubs, and
fakes
Automated test
suite
T
ode
est c
quality
Figure 11.1
Flow of a developer who applies effective and systematic testing. The arrows indicate the 
iterative nature of the process; we may go back and forth between techniques as we learn more about the 
program under development and test.


---
**Page 278**

278
CHAPTER 11
Wrapping up the book
 I am betting all my chips on intelligent testing. I do not talk much about it in this
book, although it appears in figure 11.1. Intelligent testing is all about having comput-
ers explore software systems for us. In this book, we automated the process of test exe-
cution. Test case engineering—that is, thinking of good tests—was a human activity.
Intelligent testing systems propose test cases for us.
 The idea is no longer novel among academics. There are many interesting intelli-
gent testing techniques, some of which are mature enough to be deployed into pro-
duction. Facebook, for example, has deployed Sapienz, a tool that uses search-based
algorithms that automatically explore mobile apps, looking for crashes. And Google
deploys fuzz testing (generating unexpected inputs to programs to see if they crash)
on a large scale to identify bugs in open source systems. And the beauty of the
research is that these tools are not randomly generating input data: they are getting
smarter and smarter.
 If you want to play with automated test case generation, try EvoSuite for Java
(www.evosuite.org). EvoSuite receives a class as input and produces a set of JUnit tests
that often achieve 100% branch coverage. It is awe-inspiring. I am hoping the big soft-
ware development companies of this world will catch up with this idea and build more
production-ready tools. 
11.3
Involve your final user
This book focuses on verification. Verification ensures that the code works as we
expect. Another angle to consider is validation: whether the software does what the
user wants or needs. Delivering software that brings the most value is as essential as
delivering software that works. Be sure you have mechanisms to ensure that you are
building the right software in your pipeline. 
11.4
Unit testing is hard in practice
I have a clear position regarding unit testing versus integration testing: you should do
as much unit testing as possible and leave integration testing for the parts of the sys-
tem that need it. For that to happen, you need code that is easily tested and designed
with testability in mind. However, most readers of this book are not in such a situation.
Software systems are rarely designed this way.
 When you write new pieces of code that you have more control over, be sure you
code in a unit-testable way. This means integrating the new code with hard-to-test
legacy code. I have a very simple suggestion that works in most cases. Imagine that
you need to add new behavior to a legacy class. Instead of coding the behavior in
this class, create a new class, put the new behavior in it, and unit-test it. Then, in the
legacy class, instantiate the new class and call the method. This way, you avoid the
hassle of writing a test for a class that is impossible to test. The following listing
shows an example.
 
 


---
**Page 279**

279
Invest in monitoring
class LegacyClass {
  public void complexMethod() {
    // ...
    // lots of code here...
    // ...
    new BeautifullyDesignedClass().cleanMethod();  
    // ...
    // lots of code here...
    // ...
  }
}
class BeautifullyDesignedClass {
  public void cleanMethod() {  
    // ...
    // lots of code here...
    // ...
  }
}
You may, of course, need to do things differently for your specific case, but the idea
is the same. For more information on handling legacy systems, I suggest Feather’s
book (2004). I also suggest reading about the anti-corruption layer idea proposed by
Evans (2004). 
11.5
Invest in monitoring
You do your best to catch all the bugs before we deploy. But in practice, you know that
is impossible. What can you do? Make sure that you detect the bugs as soon as they
happen in production.
 Software monitoring is as important as testing. Be sure your team invests in decent
monitoring systems. This is more complicated than you may think. First, developers need
to know what to log. This may be a tricky decision, as you do not want to log too much (to
avoid overloading your infrastructure), and you do not want to log too little (because you
will not have enough information to debug the problem). Make sure your team has good
guidelines for what should be logged, what log level to use, and so on. If you are curious,
we wrote a paper showing that machine learning can recommend logs to developers
(Cândido et al., 2021). We hope to have more concrete tooling in the future.
 It is also difficult for developers to identify anomalies when the system logs mil-
lions or even billions of log lines each month. Sometimes exceptions happen, and the
software is resilient enough to know what to do with them. Developers log these
exceptions anyway, but often the exceptions are not important. Therefore, investing
in ways to identify exceptions that matter is a pragmatic challenge, and you and your
team should invest in it. 
Listing 11.1
Handling legacy code
In the legacy class, 
we call the behavior 
that is now in the 
new class.
This class is also 
complex, but it is 
testable.


---
**Page 280**

280
CHAPTER 11
Wrapping up the book
11.6
What’s next?
There is still much to learn about software testing! This book did not have space to
cover these important topics:
Non-functional testing—If you have non-functional requirements such as perfor-
mance, scalability, or security, you may want to write tests for them as well. A
2022 book by Gayathri Mohan, Full Stack Testing (https://learning.oreilly.com/
library/view/full-stack-testing/9781098108120) has good coverage of these
type of tests.
Testing for specific architectures and contexts—As you saw in chapter 9, different
technologies may require different testing patterns. If you are building an API,
it is wise to write API tests for it. If you are building a VueJS application, it is wise
to write VueJS tests. Manning has several interesting books on the topic, includ-
ing Testing Web APIs by Mark Winteringham (www.manning.com/books/testing
-web-apis); Exploring Testing Java Microservices, with chapters selected by Alex
Soto Bueno and Jason Porter (www.manning.com/books/exploring-testing
-java-microservices), and Testing Vue.js Applications by Edd Yerburgh (www.manning
.com/books/testing-vue-js-applications).
Design for testability principles for your programming language—I mostly discussed
principles that make sense for object-oriented languages in general. If you are
working with, for example, functional languages, the principles may be some-
what different. If we pick Clojure as an example, Phil Calçado has a nice blog
post on his experiences with TDD in that language (http://mng.bz/g40x), and
Manning’s book Clojure in Action (www.manning.com/books/clojure-in-action
-second-edition) by Amit Rathore and Francis Avila has an entire chapter dedi-
cated to TDD.
Static analysis tools—Tools such as SonarQube (www.sonarqube.org) and Spot-
Bugs (https://spotbugs.github.io/) are interesting ways to look for quality
issues in code bases. These tools mostly rely on static analysis and look for spe-
cific buggy code patterns. Their main advantage is that they are very fast and
can be executed in continuous integration. I strongly suggest that you become
familiar with these tools.
Software monitoring—I said you should invest in monitoring, which means you
also need to learn how to do proper monitoring. Techniques such as A/B test-
ing, blue-green deployment, and others will help you ensure that bugs have a
harder time getting to production even if they made it through your thor-
ough testing process. The blog post “QA in Production” by Rouan Wilsenach
is a good introduction to the subject (https://martinfowler.com/articles/qa-in
-production.html).
Have fun testing!


---
**Page 281**

281
appendix
Answers to exercises
Chapter 1
1.1 The goal of systematic testing, as its name says, is to engineer test cases in a
more systematic way, rather than simply following gut feelings. Systematic testing
gives engineers sound techniques to engineer test cases out of requirements,
boundaries, and source code.
1.2 The absence-of-errors fallacy. While the software does not have many bugs, it does
not give users what they want. In this case, the verification is good, but the develop-
ers need to work on the validation.
1.3 B. Exhaustive testing is impossible in most cases.
1.4 D. Test early is an important principle, but it is definitely not related to the
problem of only doing unit tests. All the other principles can help developers
understand that using different types of testing is important.
1.5 A. The pesticide paradox fits the discussion best. The development team has
high code coverage, but they need to apply different techniques.
1.6 A. The primary use of integration tests is to find mistakes in the communication
between a system and its external dependencies.
1.7 A.
1.8 A.
1.9 B.


