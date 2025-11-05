# 3.1 Technical requirements (pp.68-68)

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


