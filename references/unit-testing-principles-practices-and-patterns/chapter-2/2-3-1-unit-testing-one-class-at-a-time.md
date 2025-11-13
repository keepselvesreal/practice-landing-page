# 2.3.1 Unit testing one class at a time (pp.34-35)

---
**Page 34**

34
CHAPTER 2
What is a unit test?
dependency that’s not shared. Most such dependencies are mutable and thus can be
modified by tests.
 With this foundation of definitions, let’s contrast the two schools on their merits. 
2.3
Contrasting the classical and London schools 
of unit testing
To reiterate, the main difference between the classical and London schools is in how
they treat the isolation issue in the definition of a unit test. This, in turn, spills over to
the treatment of a unit—the thing that should be put under test—and the approach
to handling dependencies.
 As I mentioned previously, I prefer the classical school of unit testing. It tends to
produce tests of higher quality and thus is better suited for achieving the ultimate goal
of unit testing, which is the sustainable growth of your project. The reason is fragility:
tests that use mocks tend to be more brittle than classical tests (more on this in chap-
ter 5). For now, let’s take the main selling points of the London school and evaluate
them one by one.
 The London school’s approach provides the following benefits:
Better granularity. The tests are fine-grained and check only one class at a time.
It’s easier to unit test a larger graph of interconnected classes. Since all collaborators
are replaced by test doubles, you don’t need to worry about them at the time of
writing the test.
If a test fails, you know for sure which functionality has failed. Without the class’s
collaborators, there could be no suspects other than the class under test itself.
Of course, there may still be situations where the system under test uses a
value object and it’s the change in this value object that makes the test fail.
But these cases aren’t that frequent because all other dependencies are elimi-
nated in tests.
2.3.1
Unit testing one class at a time
The point about better granularity relates to the discussion about what constitutes a
unit in unit testing. The London school considers a class as such a unit. Coming from
an object-oriented programming background, developers usually regard classes as the
atomic building blocks that lie at the foundation of every code base. This naturally
leads to treating classes as the atomic units to be verified in tests, too. This tendency is
understandable but misleading.
TIP
Tests shouldn’t verify units of code. Rather, they should verify units of
behavior: something that is meaningful for the problem domain and, ideally,
something that a business person can recognize as useful. The number of
classes it takes to implement such a unit of behavior is irrelevant. The unit
could span across multiple classes or only one class, or even take up just a
tiny method.


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
 


