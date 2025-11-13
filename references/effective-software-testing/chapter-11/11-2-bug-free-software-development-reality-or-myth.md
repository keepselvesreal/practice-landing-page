# 11.2 Bug-free software development: Reality or myth? (pp.277-278)

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
 
 


