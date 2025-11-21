# 9.5 Summary (pp.219-220)

---
**Page 219**

Managing Test Environments with Tox
Chapter 9
[ 219 ]
Figure 9.1 – Tox setup
It should became clear that once we have a working local Tox setup, moving on to Travis
involves very little apart from writing a travis.yml configuration file in charge of
installing tox-travis and then invoking tox.
Summary
In this chapter, we saw how Tox can take care of all the setup necessary to run our tests for
us and how it can do that on multiple target environments so that all we have to do to run
tests is just to invoke Tox itself.
This is a more convenient, but also robust, way to manage our test suite. The primary
benefit is that anyone else willing to contribute to our project won't have to learn how to set
up our projects and how to run tests. If our colleagues or project contributors are familiar
with Tox, seeing that our project includes a tox.ini file tells them all that they will need to
know—that they just have to invoke the tox command to run tests.
Now that we have seen the base plugins and tools to manage and run our test suite, in the
next chapter, we can move on to some more advanced topics that involve how to test our
documentation itself and how to use property-based testing to catch bugs in our code.


---
**Page 220**

10
Testing Documentation and
Property-Based Testing
In the previous chapter, we saw how to manage the environment where the test suite runs
through Tox. We now have a fairly good understanding of how to create a test suite, how to
set up an environment where this can be run, and how to ensure that we are able to
organize it in a way that remains effective as our software and test suite grow. We are now
going to move our attention to confirm that our tests are able to identify and cover corner
cases and make sure that our documentation is as robust and tested as our software itself.
In this chapter, we will cover the following topics:
Testing documentation
Property based-testing
Technical requirements
We need a working Python interpreter with PyTest, Sphinx for documentation testing, and
the Hypothesis framework for property-based testing. All of them can be installed through
pip with the help of the following command:
$ pip install pytest sphinx hypothesis
The examples have been written on Python 3.7, Sphinx 3.3.0, PyTest 6.0.2, and Hypothesis
5.41, but should work on most modern Python versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter10.


