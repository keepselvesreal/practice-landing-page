# 3.0 Introduction [auto-generated] (pp.67-68)

---
**Page 67**

3
Test-Driven Development while
Creating a TODO List
No programmer ever releases a software without having tested it – even for the most basic
proof of concept and rough hack, the developer will run it once to see that it at least starts
and resembles what they had in mind.
But to test, as a verb, usually ends up meaning clicking buttons here and there to get a
vague sense of confidence that the software does what we intended. This is different from
test as a noun, which means a set of written-out checks that our software must pass to
confirm it does what we wanted.
Apart from being more reliable, written-out checks force us to think about what the code
must do. They force us to get into the details and think beforehand about what we want to
build. Otherwise, we would just jump to building without thinking about what we are
building. And trying to ensure that what gets built is, in every single detail, the right thing
through a written specification is quickly going to turn into writing the software itself, just
in plain English.
The problem is that the more hurried, stressed, and overwhelmed developers are, the less
they test. Tests are the first thing that get skipped when things go wrong, and by doing so
things suddenly get even worse, as tests are what avoid errors and failures, and more errors
and failures mean more stress and rushing through the code to fix them, making the whole
process a loop that gets worse and worse.
Test-Driven Development (TDD) tries to solve this problem by engendering a set of
practices where tests become a fundamental step of your daily routine. To write more code
you must write tests, and as you get used to TDD and it becomes natural, you will quickly
notice that it gets hard to even think about how to get started if not by writing a test.
That's why in this chapter, we will cover how TDD can fit into the software development
routine and how to leverage it to keep problems under control at times of high stress.


---
**Page 68**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 68 ]
In this chapter, we will cover the following topics:
Starting projects with TDD
Building applications the TDD way
Preventing regressions
Technical requirements
A working Python interpreter should be all that is needed to work through the exercises in
this chapter.
The examples have been written using Python 3.7, but should work on most modern
Python versions.
You can find the code files used in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter03
Starting projects with TDD
We already know that tests are meant to verify that our software adheres to the desired
behavior. To do so means that our tests must express what that desired behavior is. They
must explicitly state, "If I do this, I expect that to happen."
For the innermost components, what happens is probably an implementation detail: "If I
commit my unit of work, data is written to the database." But the more we move to the outer
parts of our architecture, those that connect our software to the outside world, the more
these tests become expressions of business needs. The more we move from solitary units, to
sociable units, to integration and acceptance tests, the more the "desired behavior" becomes
the one that has a business value.
If we work with a test-driven approach, our first step before writing implementation code
is obviously to write a test that helps us understand what we want to build (if we are just
starting with our whole project, what we want to build is the software itself). This means
that our very first test is the one that is going to make clear what's valuable. Why are we
even writing the software in the first place?
So let's see how a test-driven approach can benefit us during the software design phase
itself. Suppose we want to start a TODO list kind of product.


