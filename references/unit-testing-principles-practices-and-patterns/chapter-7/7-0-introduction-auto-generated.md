# 7.0 Introduction [auto-generated] (pp.151-152)

---
**Page 151**

151
Refactoring toward
valuable unit tests
In chapter 1, I defined the properties of a good unit test suite:
It is integrated into the development cycle.
It targets only the most important parts of your code base.
It provides maximum value with minimum maintenance costs. To achieve
this last attribute, you need to be able to:
– Recognize a valuable test (and, by extension, a test of low value).
– Write a valuable test.
Chapter 4 covered the topic of recognizing a valuable test using the four attributes:
protection against regressions, resistance to refactoring, fast feedback, and main-
tainability. And chapter 5 expanded on the most important one of the four: resis-
tance to refactoring.
 As I mentioned earlier, it’s not enough to recognize valuable tests, you should also
be able to write such tests. The latter skill requires the former, but it also requires
This chapter covers
Recognizing the four types of code
Understanding the Humble Object pattern
Writing valuable tests


---
**Page 152**

152
CHAPTER 7
Refactoring toward valuable unit tests
that you know code design techniques. Unit tests and the underlying code are highly
intertwined, and it’s impossible to create valuable tests without putting effort into the
code base they cover.
 You saw an example of a code base transformation in chapter 6, where we refac-
tored an audit system toward a functional architecture and, as a result, were able to
apply output-based testing. This chapter generalizes this approach onto a wider spec-
trum of applications, including those that can’t use a functional architecture. You’ll
see practical guidelines on how to write valuable tests in almost any software project.
7.1
Identifying the code to refactor
It’s rarely possible to significantly improve a test suite without refactoring the underly-
ing code. There’s no way around it—test and production code are intrinsically con-
nected. In this section, you’ll see how to categorize your code into the four types in
order to outline the direction of the refactoring. The subsequent sections show a com-
prehensive example.
7.1.1
The four types of code
In this section, I describe the four types of code that serve as a foundation for the rest
of this chapter. 
 All production code can be categorized along two dimensions:
Complexity or domain significance
The number of collaborators
Code complexity is defined by the number of decision-making (branching) points in the
code. The greater that number, the higher the complexity.
How to calculate cyclomatic complexity
In computer science, there’s a special term that describes code complexity: cyclo-
matic complexity. Cyclomatic complexity indicates the number of branches in a given
program or method. This metric is calculated as
1 + <number of branching points>
Thus, a method with no control flow statements (such as if statements or condi-
tional loops) has a cyclomatic complexity of 1 + 0 = 1.
There’s another meaning to this metric. You can think of it in terms of the number of
independent paths through the method from an entry to an exit, or the number of tests
needed to get a 100% branch coverage.
Note that the number of branching points is counted as the number of simplest pred-
icates involved. For instance, a statement like IF condition1 AND condition2
THEN ... is equivalent to IF condition1 THEN IF condition2 THEN ... Therefore,
its complexity would be 1 + 2 = 3.


