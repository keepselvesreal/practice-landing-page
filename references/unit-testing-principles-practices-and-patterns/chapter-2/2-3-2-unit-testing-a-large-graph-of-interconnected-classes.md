# 2.3.2 Unit testing a large graph of interconnected classes (pp.35-36)

---
**Page 35**

35
Contrasting the classical and London schools of unit testing
And so, aiming at better code granularity isn’t helpful. As long as the test checks a sin-
gle unit of behavior, it’s a good test. Targeting something less than that can in fact
damage your unit tests, as it becomes harder to understand exactly what these tests
verify. A test should tell a story about the problem your code helps to solve, and this story should
be cohesive and meaningful to a non-programmer.
 For instance, this is an example of a cohesive story:
When I call my dog, he comes right to me.
Now compare it to the following:
When I call my dog, he moves his front left leg first, then the front right 
leg, his head turns, the tail start wagging...
The second story makes much less sense. What’s the purpose of all those movements?
Is the dog coming to me? Or is he running away? You can’t tell. This is what your tests
start to look like when you target individual classes (the dog’s legs, head, and tail)
instead of the actual behavior (the dog coming to his master). I talk more about this
topic of observable behavior and how to differentiate it from internal implementation
details in chapter 5. 
2.3.2
Unit testing a large graph of interconnected classes
The use of mocks in place of real collaborators can make it easier to test a class—
especially when there’s a complicated dependency graph, where the class under test
has dependencies, each of which relies on dependencies of its own, and so on, several
layers deep. With test doubles, you can substitute the class’s immediate dependencies
and thus break up the graph, which can significantly reduce the amount of prepara-
tion you have to do in a unit test. If you follow the classical school, you have to re-create
the full object graph (with the exception of shared dependencies) just for the sake of
setting up the system under test, which can be a lot of work.
 Although this is all true, this line of reasoning focuses on the wrong problem.
Instead of finding ways to test a large, complicated graph of interconnected classes,
you should focus on not having such a graph of classes in the first place. More often
than not, a large class graph is a result of a code design problem.
 It’s actually a good thing that the tests point out this problem. As we discussed in
chapter 1, the ability to unit test a piece of code is a good negative indicator—it pre-
dicts poor code quality with a relatively high precision. If you see that to unit test a
class, you need to extend the test’s arrange phase beyond all reasonable limits, it’s a
certain sign of trouble. The use of mocks only hides this problem; it doesn’t tackle the
root cause. I talk about how to fix the underlying code design problem in part 2. 
 


---
**Page 36**

36
CHAPTER 2
What is a unit test?
2.3.3
Revealing the precise bug location
If you introduce a bug to a system with London-style tests, it normally causes only tests
whose SUT contains the bug to fail. However, with the classical approach, tests that
target the clients of the malfunctioning class can also fail. This leads to a ripple effect
where a single bug can cause test failures across the whole system. As a result, it
becomes harder to find the root of the issue. You might need to spend some time
debugging the tests to figure it out.
 It’s a valid concern, but I don’t see it as a big problem. If you run your tests regu-
larly (ideally, after each source code change), then you know what caused the bug—
it’s what you edited last, so it’s not that difficult to find the issue. Also, you don’t have
to look at all the failing tests. Fixing one automatically fixes all the others.
 Furthermore, there’s some value in failures cascading all over the test suite. If a
bug leads to a fault in not only one test but a whole lot of them, it shows that the piece
of code you have just broken is of great value—the entire system depends on it. That’s
useful information to keep in mind when working with the code. 
2.3.4
Other differences between the classical and London schools
Two remaining differences between the classical and London schools are
Their approach to system design with test-driven development (TDD)
The issue of over-specification
The London style of unit testing leads to outside-in TDD, where you start from the
higher-level tests that set expectations for the whole system. By using mocks, you spec-
ify which collaborators the system should communicate with to achieve the expected
result. You then work your way through the graph of classes until you implement every
one of them. Mocks make this design process possible because you can focus on one
Test-driven development
Test-driven development is a software development process that relies on tests to
drive the project development. The process consists of three (some authors specify
four) stages, which you repeat for every test case:
1
Write a failing test to indicate which functionality needs to be added and how
it should behave.
2
Write just enough code to make the test pass. At this stage, the code doesn’t
have to be elegant or clean.
3
Refactor the code. Under the protection of the passing test, you can safely
clean up the code to make it more readable and maintainable.
Good sources on this topic are the two books I recommended earlier: Kent Beck’s
Test-Driven Development: By Example, and Growing Object-Oriented Software, Guided
by Tests by Steve Freeman and Nat Pryce.


