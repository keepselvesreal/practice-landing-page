# 5.7 Summary (pp.151-152)

---
**Page 151**

Introduction to PyTest
Chapter 5
[ 151 ]
pytest test_markers.py -m "first" would run only the one marked with our
custom marker:
$ pytest test_markers.py -v -m first
...
test_markers.py::test_one PASSED [100%]
This means that we can mark our tests in any way we want and run selected groups of tests
independently from the directory where they sit or how they are named.
On some versions of pytest, you might get a warning when using custom markers:
Unknown pytest.mark.first - is this a typo?  You can register custom marks
to avoid this warning
This means that the marker is unknown to pytest and must be registered in the list of
available markers to make the warning go away. The reason for this is to prevent typos that
would slip by unnoticed if markers didn't have to be registered. 
To make a marker available and make the warning disappear, the custom markers can be
set in the pytest.ini configuration file for your test suite:
[pytest]
markers =
    first: mark a test as the first one written.
If the configuration file is properly recognized and we have no typos in the "first"
marker, the previously mentioned warning will go away and we will be able to use the
"first" marker freely.
Summary
In this chapter, we saw how pytest can provide more advanced features on top of the
same functionalities we were already used to with unittest. We also saw how we can run
our existing test suite with pytest and how we can evolve it to leverage some of built-in
pytest features.
We've looked at some of the features that pytest provides out of the box, and in the next
chapter, we will introduce more advanced pytest features, such as parametric tests and
fixture generation.


---
**Page 152**

6
Dynamic and Parametric Tests
and Fixtures
In the previous chapter, we saw how pytest can be used to run our test suites, and how it
provides some more advanced features that are unavailable in unittest by default.
Python has seen multiple frameworks and libraries built on top of unittest to extend it
with various features and utilities, but pytest has surely become the most widespread
testing framework in the Python community. One of the reasons why pytest became so
popular is its flexibility and support for dynamic behaviors. Apart from this, generating
tests and fixtures dynamically or heavily changing test suite behavior are other features
supported by pytest out of the box.
In this chapter, we are going to see how to configure a test suite and generate dynamic
fixtures and dynamic or parametric tests. As your test suite grows, it will be important to be
able to know which options PyTest provides to drive the test suite execution and how we
can generate fixtures and tests dynamically instead of rewriting them over and over.
In this chapter, we will cover the following topics:
Configuring the test suite
Generating fixtures
Generating tests with parametric tests
Technical requirements
We need a working Python interpreter with the pytest framework installed. Pytest can be
installed using the following command:
$ pip install pytest


