# 11.1 Although the model looks linear, iterations are fundamental (pp.276-277)

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


