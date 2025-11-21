# 3.13 Summary (pp.96-97)

---
**Page 96**

96
CHAPTER 3
Structural testing and code coverage
C It is possible to devise a single test case that achieves 100% line coverage
and 100% decision + condition coverage.
D It is possible to devise a single test case that achieves 100% line coverage
and 100% path coverage.
3.7
Which of the following statements concerning the subsumption relations between
test adequacy criteria is true?
A MC/DC subsumes statement coverage.
B Statement coverage subsumes branch coverage.
C Branch coverage subsumes path coverage.
D Basic condition coverage subsumes branch coverage.
3.8
A test suite satisfies the loop boundary adequacy criterion if for every loop L:
A Test cases iterate L zero times, once, and more than once.
B Test cases iterate L once and more than once.
C Test cases iterate L zero times and one time.
D Test cases iterate L zero times, once, more than once, and N, where N is
the maximum number of iterations.
3.9
Which of the following statements is correct about the relationship between
specification-based testing and structural testing?
A A testing process should prioritize structural testing because it’s cheaper yet
highly effective (maybe even more effective than specification-based testing).
B Specification-based testing can only be effectively performed when we have
proper models of the program under test. A simple user story is not enough.
C Boundary analysis can only be done if testers have access to the source
code, and thus it should be considered a structural testing technique.
D None of the other answers is true.
Summary
Structural testing uses the source code to augment the test suite engineered via
specification-based testing.
The overall idea of structural testing is to analyze which parts of the code are
not yet covered and reflect on whether they should be covered or not.
Some coverage criteria are less rigorous and therefore less expensive (for exam-
ple, line coverage). Others are more rigorous but also more expensive (such as
MC/DC coverage). As a developer, you have to decide which criteria to use.
Code coverage should not be used as a number to be achieved. Rather, cover-
age tools should be used to support developers in performing structural testing
(that is, understanding what parts are not covered and why).
Mutation testing ensures that our test suite is strong enough: in other words,
that it can catch as many bugs as possible.


---
**Page 97**

97
Designing contracts
Imagine a piece of software that handles a very complex financial process. For that
big routine to happen, the software system chains calls to several subroutines (or
classes) in a complex flow of information: that is, the results of one class are passed
to the next class, whose results are again passed to the next class, and so on. As
usual, the data comes from different sources, such as databases, external web ser-
vices, and users. At some point in the routine, the class TaxCalculator (which han-
dles calculating a specific tax) is called. From the requirements of this class, the
calculation only makes sense for positive numbers.
 We need to think about how we want to model such a restriction. I see three
options when facing such a restriction:
Ensure that classes never call other classes with invalid inputs. In our exam-
ple, any other classes called TaxCalculator will ensure that they will never
pass a negative number. While this simplifies the code of the class under
This chapter covers
Designing pre-conditions, post-conditions, and 
invariants
Understanding the differences between contracts 
and validation


