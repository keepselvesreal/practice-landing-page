# 4.6 Summary (pp.136-138)

---
**Page 136**

Scaling the Test Suite
Chapter 4
[ 136 ]
Performance testing in the cloud
While our CI system does most of what we need, it's important to remember that cloud
runners are not designed for benchmarking. So our performance test suite only becomes 
reliable when there are major slowdowns and over the course of multiple runs.
The two most common strategies when running performance tests in the cloud are as
follows:
To rerun the test suite multiple times and pick the fastest run, in order to absorb
the temporary contention of resources in the cloud
To record the metrics into a monitoring service such as Prometheus, from which
it becomes possible to see the trend of the metrics over the course of multiple
runs
Whichever direction you choose to go in, make sure you keep in mind that cloud services
such as Travis can have random slowdowns due to the other requests they are serving, and
thus it's usually better to make decisions over the course of multiple runs.
Summary
In this chapter, we saw how we can keep our test suite effective and comfortable as the
complexity of our application and the size of our test suites grow. We saw how tests can be
organized into different categories that could be run at different times, and also saw how
we can have multiple different test suites in a single project, each serving its own purpose.
In general, over the previous four chapters, we learned how to structure our testing
strategy and how testing can help us design robust applications. We also saw how Python
has everything we need built in already through the unittest module.
But as our test suite grows and becomes bigger, there are utilities, patterns, and features
that we would have to implement on our own in the unittest module. That's why, over
the course of many years, many frameworks have been designed for testing by the Python
community. In the next chapter, we are going to introduce pytest, the most widespread
framework for testing Python applications.


---
**Page 137**

2
Section 2: PyTest for Python
Testing
In this section, we will learn how PyTest, the most widespread Python testing framework,
can be applied to the concepts we learned in Section 1, Software Testing and Test-Driven
Development, regarding plain Python. We will also learn how to set up fixtures and which
plugins exist to make our lives easier when we're maintaining a test suite.
This section comprises the following chapters:
Chapter 5, Introduction to PyTest
Chapter 6, Dynamic and Parametric Tests and Fixtures 
Chapter 7, Fitness Function with a Contact Book Application 
Chapter 8, PyTest Essential Plugins 
Chapter 9, Managing Test Environments with Tox
Chapter 10, Testing Documentation and Property-Based Testing


---
**Page 138**

5
Introduction to PyTest
In the previous chapters, we saw how to approach test-driven development, how to create
a test suite with the unittest module, and how to organize it as it grows. While unittest
is a very good tool and is a reliable solution for most projects, it lacks some convenient
features that are available in more advanced testing frameworks.
PyTest is currently the most widespread testing framework in the Python community, and
it's mostly compatible with unittest. So it's easy to migrate from unittest to pytest if
you feel the need for the convenience that pytest provides.
In this chapter, we will cover the following topics:
Running tests with PyTest
Writing PyTest fixtures
Managing temporary data with tmp_path
Testing I/O with capsys
Running subsets of the test suite
Technical requirements
We need a working Python interpreter with the pytest framework installed. Pytest can be
installed with the following:
$ pip install pytest
The examples have been written on Python 3.7 and pytest 5.4.3 but should work on most
modern Python versions. You can find the code files present in this chapter on GitHub
at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-
Python/​tree/​main/​Chapter05.


