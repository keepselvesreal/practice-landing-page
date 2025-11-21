# 1.6 Summary (pp.18-20)

---
**Page 18**

18
CHAPTER 1
The goal of unit testing
 If you don’t have much experience with unit testing techniques and best practices,
you’ll learn a lot. In addition to the frame of reference that you can use to analyze any
test in a test suite, the book teaches
How to refactor the test suite along with the production code it covers
How to apply different styles of unit testing
Using integration tests to verify the behavior of the system as a whole
Identifying and avoiding anti-patterns in unit tests
In addition to unit tests, this book covers the entire topic of automated testing, so
you’ll also learn about integration and end-to-end tests.
 I use C# and .NET in my code samples, but you don’t have to be a C# professional
to read this book; C# is just the language that I happen to work with the most. All
the concepts I talk about are non-language-specific and can be applied to any other
object-oriented language, such as Java or C++.
Summary
Code tends to deteriorate. Each time you change something in a code base, the
amount of disorder in it, or entropy, increases. Without proper care, such as
constant cleaning and refactoring, the system becomes increasingly complex
and disorganized. Tests help overturn this tendency. They act as a safety net— a
tool that provides insurance against the vast majority of regressions.
It’s important to write unit tests. It’s equally important to write good unit tests.
The end result for projects with bad tests or no tests is the same: either stagna-
tion or a lot of regressions with every new release.
The goal of unit testing is to enable sustainable growth of the software project.
A good unit test suite helps avoid the stagnation phase and maintain the devel-
opment pace over time. With such a suite, you’re confident that your changes
won’t lead to regressions. This, in turn, makes it easier to refactor the code or
add new features.
All tests are not created equal. Each test has a cost and a benefit component,
and you need to carefully weigh one against the other. Keep only tests of posi-
tive net value in the suite, and get rid of all others. Both the application code
and the test code are liabilities, not assets.
The ability to unit test code is a good litmus test, but it only works in one direc-
tion. It’s a good negative indicator (if you can’t unit test the code, it’s of poor
quality) but a bad positive one (the ability to unit test the code doesn’t guaran-
tee its quality).
Likewise, coverage metrics are a good negative indicator but a bad positive one.
Low coverage numbers are a certain sign of trouble, but a high coverage num-
ber doesn’t automatically mean your test suite is of high quality.
Branch coverage provides better insight into the completeness of the test suite
but still can’t indicate whether the suite is good enough. It doesn’t take into


---
**Page 19**

19
Summary
account the presence of assertions, and it can’t account for code paths in third-
party libraries that your code base uses.
Imposing a particular coverage number creates a perverse incentive. It’s good
to have a high level of coverage in core parts of your system, but it’s bad to make
this high level a requirement.
A successful test suite exhibits the following attributes:
– It is integrated into the development cycle.
– It targets only the most important parts of your code base.
– It provides maximum value with minimum maintenance costs.
The only way to achieve the goal of unit testing (that is, enabling sustainable
project growth) is to
– Learn how to differentiate between a good and a bad test.
– Be able to refactor a test to make it more valuable.


---
**Page 20**

20
What is a unit test?
As mentioned in chapter 1, there are a surprising number of nuances in the defini-
tion of a unit test. Those nuances are more important than you might think—so
much so that the differences in interpreting them have led to two distinct views on
how to approach unit testing.
 These views are known as the classical and the London schools of unit testing.
The classical school is called “classical” because it’s how everyone originally
approached unit testing and test-driven development. The London school takes
root in the programming community in London. The discussion in this chapter
about the differences between the classical and London styles lays the foundation
for chapter 5, where I cover the topic of mocks and test fragility in detail.
This chapter covers
What a unit test is
The differences between shared, private, 
and volatile dependencies
The two schools of unit testing: classical 
and London
The differences between unit, integration, 
and end-to-end tests


