# 1.2.1 Effective testing in the development process (pp.12-14)

---
**Page 12**

12
CHAPTER 1
Effective and systematic software testing
she focused on the code; and through structural testing (or code coverage), she evalu-
ated whether the current test cases were sufficient. For some test cases, Eleanor wrote
example-based tests (that is, she picked a single data point for a test). For one specific
case, she used property-based testing, as it helped her better explore possible bugs in the
code. Finally, she reflected frequently about the contracts and pre- and post-conditions of
the method she was devising (although in the end, she implemented a set of valida-
tion checks and not pre-conditions per se; we discuss the differences between con-
tracts and validation in chapter 4).
 This is what I call effective and systematic software testing for developers. In the remain-
der of this chapter, I explain how software developers can perform effective testing
together with their development activities. Before we dive into the specific techniques,
I describe effective testing within the development processes and how testing tech-
niques complement each other. I discuss the different types of tests and which ones
you should focus on. Finally, I illustrate why software testing is so difficult.
1.2.1
Effective testing in the development process
In this book, I propose a straightforward flow for developers who apply effective and
systematic testing. First, we implement a feature, using tests to facilitate and guide
development. Once we are reasonably happy with the feature or small unit we’ve
coded, we dive into effective and systematic testing to ensure that it works as expected
(that is, we test to find bugs). Figure 1.4 illustrates the development workflow in more
detail; let’s walk through it:
IntelliJ indicates that these
lines are covered by adding
a color near the line. Green
indicates the line is covered;
red indicates the line is not
covered.
Here, due to the monochrome
ﬁgure, you can't see the green
color, but all lines are green.
Figure 1.3
The result of the code coverage analysis done by my IDE, IntelliJ. All lines are covered.


---
**Page 13**

13
Effective software testing for developers
1
Feature development often starts with a developer receiving some sort of require-
ment. Requirements are often in the form of natural language and may follow a
specific format, such as Unified Modeling Language (UML) use cases or agile
user stories. After building up some understanding (that is, requirement analysis),
the developer starts writing code.
2
To guide the development of the feature, the developer performs short test-
driven development (TDD) cycles. These cycles give the developer rapid feedback
about whether the code they just wrote makes sense. They also support the
developer through the many refactorings that occur when a new feature is
being implemented.
3
Requirements are often large and complex and are rarely implemented by a
single class or method. The developer creates several units (classes and methods)
with different contracts, and they collaborate and together form the required
functionality. Writing classes such that they’re easy to test is challenging, and
the developer must design with testability in mind.
4
Once the developer is satisfied with the units they’ve created and believes the
requirement is complete, they shift to testing. The first step is to exercise each
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
Here, we’ll discuss ideas
that will help us in
implementing the feature
with conﬁdence and with
testability in mind.
Here, we’ll discuss different techniques
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
Figure 1.4
The workflow of a developer who applies effective and systematic testing. The arrows indicate 
the iterative nature of the process; developers may go back and forth between the different techniques as 
they learn more about the program under development and test.


---
**Page 14**

14
CHAPTER 1
Effective and systematic software testing
new unit. Domain testing, boundary testing, and structural testing are the go-to
techniques.
5
Some parts of the system may require the developer to write larger tests (integra-
tion or system tests). To devise larger test cases, the developer uses the same
three techniques—domain testing, boundary testing, and structural testing—
but looking at larger parts of the software system.
6
When the developer has engineered test cases using the various techniques,
they apply automated, intelligent testing tools to look for tests that humans are
not good at spotting. Popular techniques include test case generation, mutation
testing, and static analysis. In this book, we cover mutation testing.
7
Finally, after this rigorous testing, the developer feels comfortable releasing
the feature. 
1.2.2
Effective testing as an iterative process
While the previous description may sound like a sequential/waterfall process, it is
more iterative. A developer may be rigorously testing a class and suddenly notice that
a coding decision they made a few hours ago was not ideal. They then go back and
redesign the code. They may be performing TDD cycles and realize the requirement
is unclear about something. The developer then goes back to the requirement analy-
sis to better grasp the expectations. Quite commonly, while testing, the developer
finds a bug. They go back to the code, fix it, and continue testing. Or the developer
may have implemented only half of the feature, but they feel it would be more pro-
ductive to rigorously test it now than to continue the implementation.
 The development workflow I propose throughout this book is not meant to
restrain you. Feel free to go back and forth between techniques or change the order
in which you apply them. In practice, you have to find what works best for you and
makes you the most productive. 
1.2.3
Focusing on development and then on testing
I find it liberating to focus separately on developing and testing. When I am coding a
feature, I do not want to be distracted by obscure corner cases. If I think of one, I take
notes so I do not forget to test it later. However, I prefer to focus all my energy on the
business rules I am implementing and, at the same time, ensure that the code is easy
for future developers to maintain.
 Once I am finished with the coding decisions, I focus on testing. First I follow the
different techniques as if I were working my way down a systematic checklist. As you
saw in the example with Eleanor, she did not have to think much about what to exer-
cise when the method received a list: she responded as if she had a checklist that said
“null, empty list, one element, many elements.” Only then do I use my creativity and
domain knowledge to exercise other cases I find relevant.


