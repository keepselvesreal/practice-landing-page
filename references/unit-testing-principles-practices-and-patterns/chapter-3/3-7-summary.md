# 3.7 Summary (pp.63-67)

---
**Page 63**

63
Summary
result) precisely because it follows the story pattern. It’s a simple story in which
result is a subject, should be is an action, and 30 is an object.
NOTE
The paradigm of object-oriented programming (OOP) has become a
success partly because of this readability benefit. With OOP, you, too, can
structure the code in a way that reads like a story.
The Fluent Assertions library also provides numerous helper methods to assert against
numbers, strings, collections, dates and times, and much more. The only drawback is
that such a library is an additional dependency you may not want to introduce to your
project (although it’s for development only and won’t be shipped to production). 
Summary
All unit tests should follow the AAA pattern: arrange, act, assert. If a test has mul-
tiple arrange, act, or assert sections, that’s a sign that the test verifies multiple
units of behavior at once. If this test is meant to be a unit test, split it into several
tests—one per each action.
More than one line in the act section is a sign of a problem with the SUT’s API.
It requires the client to remember to always perform these actions together,
which can potentially lead to inconsistencies. Such inconsistencies are called
invariant violations. The act of protecting your code against potential invariant
violations is called encapsulation.
Distinguish the SUT in tests by naming it sut. Differentiate the three test sec-
tions either by putting Arrange, Act, and Assert comments before them or by
introducing empty lines between these sections.
Reuse test fixture initialization code by introducing factory methods, not by
putting this initialization code to the constructor. Such reuse helps maintain a
high degree of decoupling between tests and also provides better readability.
Don’t use a rigid test naming policy. Name each test as if you were describing
the scenario in it to a non-programmer who is familiar with the problem
domain. Separate words in the test name by underscores, and don’t include the
name of the method under test in the test name.
Parameterized tests help reduce the amount of code needed for similar tests.
The drawback is that the test names become less readable as you make them
more generic.
Assertion libraries help you further improve test readability by restructuring the
word order in assertions so that they read like plain English. 


---
**Page 64**



---
**Page 65**

Part 2
Making your tests
work for you
Now that you’re armed with the knowledge of what unit testing is for,
you’re ready to dive into the very crux of what makes a good test and learn how
to refactor your tests toward being more valuable. In chapter 4, you’ll learn
about the four pillars that make up a good unit test. These four pillars set a foun-
dation, a common frame of reference, which we’ll use to analyze unit tests and
testing approaches moving forward.
 Chapter 5 takes the frame of reference established in chapter 4 and builds
the case for mocks and their relation to test fragility.
 Chapter 6 uses the same the frame of reference to examine the three styles of
unit testing. It shows which of those styles tends to produce tests of the best qual-
ity, and why.
 Chapter 7 puts the knowledge from chapters 4 to 6 into practice and teaches
you how to refactor away from bloated, overcomplicated tests to tests that pro-
vide as much value with as little maintenance cost as possible.


---
**Page 66**



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


