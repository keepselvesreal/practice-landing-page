# 7.1.1 The four types of code (pp.152-155)

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


---
**Page 153**

153
Identifying the code to refactor
Domain significance shows how significant the code is for the problem domain of your
project. Normally, all code in the domain layer has a direct connection to the end
users’ goals and thus exhibits a high domain significance. On the other hand, utility
code doesn’t have such a connection.
 Complex code and code that has domain significance benefit from unit testing the
most because the corresponding tests have great protection against regressions. Note
that the domain code doesn’t have to be complex, and complex code doesn’t have to
exhibit domain significance to be test-worthy. The two components are independent
of each other. For example, a method calculating an order price can contain no con-
ditional statements and thus have the cyclomatic complexity of 1. Still, it’s important
to test such a method because it represents business-critical functionality.
 The second dimension is the number of collaborators a class or a method has. As
you may remember from chapter 2, a collaborator is a dependency that is either
mutable or out-of-process (or both). Code with a large number of collaborators is
expensive to test. That’s due to the maintainability metric, which depends on the size
of the test. It takes space to bring collaborators to an expected condition and then
check their state or interactions with them afterward. And the more collaborators
there are, the larger the test becomes.
 The type of the collaborators also matters. Out-of-process collaborators are a no-go
when it comes to the domain model. They add additional maintenance costs due to
the necessity to maintain complicated mock machinery in tests. You also have to be
extra prudent and only use mocks to verify interactions that cross the application
boundary in order to maintain proper resistance to refactoring (refer to chapter 5 for
more details). It’s better to delegate all communications with out-of-process depen-
dencies to classes outside the domain layer. The domain classes then will only work
with in-process dependencies.
 Notice that both implicit and explicit collaborators count toward this number. It
doesn’t matter if the system under test (SUT) accepts a collaborator as an argument
or refers to it implicitly via a static method, you still have to set up this collaborator in
tests. Conversely, immutable dependencies (values or value objects) don’t count. Such
dependencies are much easier to set up and assert against.
 The combination of code complexity, its domain significance, and the number of
collaborators give us the four types of code shown in figure 7.1:
Domain model and algorithms (figure 7.1, top left)—Complex code is often part of
the domain model but not in 100% of all cases. You might have a complex algo-
rithm that’s not directly related to the problem domain.
Trivial code (figure 7.1, bottom left)—Examples of such code in C# are parameter-
less constructors and one-line properties: they have few (if any) collaborators
and exhibit little complexity or domain significance.
Controllers (figure 7.1, bottom right)—This code doesn’t do complex or business-
critical work by itself but coordinates the work of other components like domain
classes and external applications.


---
**Page 154**

154
CHAPTER 7
Refactoring toward valuable unit tests
Overcomplicated code (figure 7.1, top right)—Such code scores highly on both
metrics: it has a lot of collaborators, and it’s also complex or important. An
example here are fat controllers (controllers that don’t delegate complex work
anywhere and do everything themselves).
Unit testing the top-left quadrant (domain model and algorithms) gives you the best
return for your efforts. The resulting unit tests are highly valuable and cheap. They’re
valuable because the underlying code carries out complex or important logic, thus
increasing tests’ protection against regressions. And they’re cheap because the code
has few collaborators (ideally, none), thus decreasing tests’ maintenance costs.
 Trivial code shouldn’t be tested at all; such tests have a close-to-zero value. As for
controllers, you should test them briefly as part of a much smaller set of the overarch-
ing integration tests (I cover this topic in part 3).
 The most problematic type of code is the overcomplicated quadrant. It’s hard to
unit test but too risky to leave without test coverage. Such code is one of the main rea-
sons many people struggle with unit testing. This whole chapter is primarily devoted
to how you can bypass this dilemma. The general idea is to split overcomplicated code
into two parts: algorithms and controllers (figure 7.2), although the actual implemen-
tation can be tricky at times.
TIP
The more important or complex the code, the fewer collaborators it
should have.
Getting rid of the overcomplicated code and unit testing only the domain model and
algorithms is the path to a highly valuable, easily maintainable test suite. With this
approach, you won’t have 100% test coverage, but you don’t need to—100% coverage
shouldn’t ever be your goal. Your goal is a test suite where each test adds significant
value to the project. Refactor or get rid of all other tests. Don’t allow them to inflate
the size of your test suite.
Complexity,
domain
signiﬁcance
Domain model,
algorithms
Overcomplicated
code
Trivial code
Number of
collaborators
Controllers
Figure 7.1
The four types of code, 
categorized by code complexity and 
domain significance (the vertical 
axis) and the number of collaborators 
(the horizontal axis).


---
**Page 155**

155
Identifying the code to refactor
NOTE
Remember that it’s better to not write a test at all than to write a
bad test.
Of course, getting rid of overcomplicated code is easier said than done. Still, there are
techniques that can help you do that. I’ll first explain the theory behind those tech-
niques and then demonstrate them using a close-to-real-world example. 
7.1.2
Using the Humble Object pattern to split overcomplicated code
To split overcomplicated code, you need to use the Humble Object design pattern.
This pattern was introduced by Gerard Meszaros in his book xUnit Test Patterns: Refac-
toring Test Code (Addison-Wesley, 2007) as one of the ways to battle code coupling, but
it has a much broader application. You’ll see why shortly.
 We often find that code is hard to test because it’s coupled to a framework depen-
dency (see figure 7.3). Examples include asynchronous or multi-threaded execution,
user interfaces, communication with out-of-process dependencies, and so on.
To bring the logic of this code under test, you need to extract a testable part out of it.
As a result, the code becomes a thin, humble wrapper around that testable part: it glues
Complexity,
domain
signiﬁcance
Domain model,
algorithms
Overcomplicated
code
Trivial code
Number of
collaborators
Controllers
Figure 7.2
Refactor overcomplicated 
code by splitting it into algorithms and 
controllers. Ideally, you should have no 
code in the top-right quadrant.
Overcomplicated code
Hard-to-test
dependency
Logic
Test
Figure 7.3
It’s hard to test 
code that couples to a difficult 
dependency. Tests have to deal 
with that dependency, too, which 
increases their maintenance cost.


