# 6.1 Technical requirements (pp.152-153)

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


---
**Page 153**

Dynamic and Parametric Tests and Fixtures
Chapter 6
[ 153 ]
Though the examples have been written using Python 3.7 and pytest 5.4.3, they should
work on most modern Python versions. You can find the code files used in this chapter on
GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-​Software-
with-​Python/​tree/​main/​Chapter06
Configuring the test suite
In pytest, there are two primary configuration files that can be used to drive the behavior of
our testing environment:
pytest.ini takes care of configuring pytest itself, so the options we set there
are mostly related to tweaking the behavior of the test runner and discovery.
These options are usually available as command-line options too.
conftest.py is aimed at configuring our tests and test suite, so it's the place
where we can declare new fixtures, attach plugins, and change the way our tests
should behave.
While pytest has grown over the years, with other ways being developed to configure the
behavior of pytest itself or of the test suite, the two aforementioned ways are probably the
most widespread.
For example, for a fizzbuzz project, if we have a test suite with the classical basic
distinction between the source code, unit tests, and functional tests, then we could have a
pytest.ini file within the project directory to drive how pytest should run:
.
├── pytest.ini
├── src
│   ├── fizzbuzz
│   │   ├── __init__.py
│   │   └── __main__.py
│   └── setup.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── functional
    │   └── test_acceptance.py
    └── unit
        ├── test_checks.py
        └── test_output.py


