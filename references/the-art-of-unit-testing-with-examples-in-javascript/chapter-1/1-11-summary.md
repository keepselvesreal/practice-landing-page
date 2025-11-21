# 1.11 Summary (pp.26-28)

---
**Page 26**

26
CHAPTER 1
The basics of unit testing
Just because you write your tests first, and they’re readable and maintainable, doesn’t
mean you’ll end up with a well-designed system. Design skills are what make your
code beautiful and maintainable. I recommend Growing Object-Oriented Software,
Guided by Tests by Steve Freeman and Nat Pryce (Addison-Wesley Professional,
2009) and Clean Code by Robert C. Martin (Pearson, 2008) as good books on the
subject.
A pragmatic approach to learning TDD is to learn each of these three aspects sepa-
rately; that is, to focus on one skill at a time, ignoring the others in the meantime. The
reason I recommend this approach is that I often see people trying to learn all three
skill sets at the same time, having a really hard time in the process, and finally giving
up because the wall is too high to climb. By taking a more incremental approach to
learning this field, you relieve yourself of the constant fear that you’re getting it wrong
in a different area than you’re currently focusing on.
 In the next chapter, you’ll start writing your first unit tests using Jest, one of the
most commonly used test frameworks for JavaScript.
Summary
A good unit test has these qualities:
– It should run quickly.
– It should have full control of the code under test.
– It should be fully isolated (it should run independently of other tests).
– It should run in memory without requiring filesystem files, networks, or
databases. 
– It should be as synchronous and linear as possible (no parallel threads).
Entry points are public functions that are the doorways into our units of work
and trigger the underlying logic. Exit points are the places you can inspect with
your test. They represent the effects of the units of work. 
An exit point can be a return value, a change of state, or a call to a third-party
dependency. Each exit point usually requires a separate test, and each type of
exit point requires a different testing technique.
A unit of work is the sum of actions that take place between the invocation of an
entry point up until a noticeable end result through one or more exit points. A
unit of work can span a function, a module, or multiple modules.
Integration testing is just unit testing with some or all of the dependencies
being real and residing outside of the current execution process. Conversely,
unit testing is like integration testing, but with all of the dependencies in mem-
ory (both real and fake), and we have control over their behavior in the test.
The most important attributes of any test are readability, maintainability, and
trust. Readability tells us how easy it is to read and understand the test. Maintain-
ability is the measure of how painful it is to maintain the test code. Without trust,


---
**Page 27**

27
Summary
it’s harder to introduce important changes (such as refactoring) in a codebase,
which leads to code deterioration.
Test-driven development (TDD) is a technique that advocates for writing tests
before the production code. This approach is also referred to as a test-first
approach (as opposed to code-first).
The main benefit of TDD is verifying the correctness of your tests. Seeing your
tests fail before writing production code ensures that these same tests would fail
if the functionality they cover stops working properly.


---
**Page 28**

28
A first unit test
When I first started writing unit tests with a real unit testing framework, there was
little documentation, and the frameworks I worked with didn’t have proper exam-
ples. (I was mostly coding in VB 5 and 6 at the time.) It was a challenge learning to
work with them, and I started out writing rather poor tests. Fortunately, times have
changed. In JavaScript, and in practically any language out there, there’s a wide
range of choices and plenty of documentation and support from the community
for trying out these bundles of helpfulness.
 In the previous chapter, we wrote a very simple home-grown test framework.
In this chapter, we’ll take a look at Jest, which will be our framework of choice for
this book. 
This chapter covers
Writing your first test with Jest
Test structure and naming conventions
Working with the assertion library
Refactoring tests and reducing repetitive code


