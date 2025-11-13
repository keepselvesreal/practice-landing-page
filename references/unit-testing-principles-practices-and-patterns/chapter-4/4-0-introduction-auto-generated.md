# 4.0 Introduction [auto-generated] (pp.67-68)

---
**Page 67**

67
The four pillars
of a good unit test
Now we are getting to the heart of the matter. In chapter 1, you saw the properties
of a good unit test suite:
It is integrated into the development cycle. You only get value from tests that you
actively use; there’s no point in writing them otherwise.
It targets only the most important parts of your code base. Not all production code
deserves equal attention. It’s important to differentiate the heart of the
application (its domain model) from everything else. This topic is tackled in
chapter 7.
It provides maximum value with minimum maintenance costs. To achieve this last
attribute, you need to be able to
– Recognize a valuable test (and, by extension, a test of low value)
– Write a valuable test
This chapter covers
Exploring dichotomies between aspects of a 
good unit test
Defining an ideal test
Understanding the Test Pyramid
Using black-box and white-box testing


---
**Page 68**

68
CHAPTER 4
The four pillars of a good unit test
As we discussed in chapter 1, recognizing a valuable test and writing a valuable test are two
separate skills. The latter skill requires the former one, though; so, in this chapter, I’ll
show how to recognize a valuable test. You’ll see a universal frame of reference with
which you can analyze any test in the suite. We’ll then use this frame of reference to
go over some popular unit testing concepts: the Test Pyramid and black-box versus
white-box testing.
 Buckle up: we are starting out.
4.1
Diving into the four pillars of a good unit test
A good unit test has the following four attributes:
Protection against regressions
Resistance to refactoring
Fast feedback
Maintainability
These four attributes are foundational. You can use them to analyze any automated
test, be it unit, integration, or end-to-end. Every such test exhibits some degree of
each attribute. In this section, I define the first two attributes; and in section 4.2, I
describe the intrinsic connection between them.
4.1.1
The first pillar: Protection against regressions
Let’s start with the first attribute of a good unit test: protection against regressions. As you
know from chapter 1, a regression is a software bug. It’s when a feature stops working as
intended after some code modification, usually after you roll out new functionality.
 Such regressions are annoying (to say the least), but that’s not the worst part about
them. The worst part is that the more features you develop, the more chances there are
that you’ll break one of those features with a new release. An unfortunate fact of pro-
gramming life is that code is not an asset, it’s a liability. The larger the code base, the more
exposure it has to potential bugs. That’s why it’s crucial to develop a good protection
against regressions. Without such protection, you won’t be able to sustain the project
growth in a long run—you’ll be buried under an ever-increasing number of bugs.
 To evaluate how well a test scores on the metric of protecting against regressions,
you need to take into account the following:
The amount of code that is executed during the test
The complexity of that code
The code’s domain significance
Generally, the larger the amount of code that gets executed, the higher the chance
that the test will reveal a regression. Of course, assuming that this test has a relevant
set of assertions, you don’t want to merely execute the code. While it helps to know
that this code runs without throwing exceptions, you also need to validate the out-
come it produces.


