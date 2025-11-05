# 3.5 Summary (pp.113-114)

---
**Page 113**

Test-Driven Development while Creating a TODO List
Chapter 3
[ 113 ]
test_noloader (tests.unit.test_todoapp.TestTODOApp) ... ok
test_save (tests.unit.test_todoapp.TestTODOApp) ... ok
----------------------------------------------------------------------
Ran 9 tests in 1.015s
OK
It seems we succeeded! We identified the bug, fixed it, and now have a test preventing the
same bug from happening again.
I hope the benefit of starting any bug-and-issue resolution by first writing a test that
reproduces the issue itself is clear. Not only does it prevent the issue from happening again
in the future, but it also allows you to isolate the system where the bug is happening,
design a fix, and make sure you actually fix the right bug.
Summary
We saw how acceptance tests can be used to make clear what we want to build and guide
us step by step through what we have to build next, while lower-level tests, such as unit
and integration tests, can be used to tell us how we want to build it and how we want the
various pieces to work together.
In this case, our application was fairly small, so we used the acceptance test to verify the
integration of our pieces. However, in the real world, as we grow the various parts of our
infrastructure, we will have to introduce tests to confirm they are able to work together and
the reason is their intercommunication protocol.
Once we found a bug, we also saw how regression tests can help us design fixes and how
they can prevent the same bug from happening again in the long term.
During any stage of software development, the Design, Implementation, and Maintenance
workflow helps us better understand what we are trying to do and thus get the right
software, code, and bug fixes in place.
So far, we've worked with fairly small test suites, but the average real-world software has
thousands of tests, so particular attention to how we organize will be essential to a test suite
we feel we can rely on. In the next chapter, we are thus going to see how to scale test suites
when the number of tests becomes hard to manage and the time it takes to run the test suite
gets too long to run it all continuously.


---
**Page 114**

4
Scaling the Test Suite
Writing one test is easy; writing thousands of tests, maintaining them, and ensuring they
don’t become a burden for development and the team is hard. Let’s dive into some tools
and best practices that help us define our test suite and keep it in shape.
To support the concepts in this chapter, we are going to use the test suite written for our
Chat application in Chapter 2, Test Doubles with a Chat Application. We are going to see how
to scale it as the application gets bigger and the tests get slower, and how to organize it in a
way that can serve us in the long term.
In this chapter, we will cover the following topics:
Scaling tests
Working with multiple suites
Carrying out performance testing
Enabling continuous integration
Technical requirements
A working Python interpreter and a GitHub.com account are required to work through the
examples in this chapter.
The examples we'll work through have been written using Python 3.7, but should work
with most modern Python versions.
The source code for the examples in this chapter can be found on GitHub
at https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python
/tree/main/Chapter04


