# 5.6 Running subsets of the testsuite (pp.150-151)

---
**Page 150**

Introduction to PyTest
Chapter 5
[ 150 ]
test_capsys.py::test_capsys PASSED
===== 1 passed in 0.03s =====
The passing test run confirms that the capsys plugin worked correctly and our test was
able to intercept the output sent by the function under test.
Running subsets of the testsuite
In the previous chapters, we saw how to divide our test suite into subsets that we can run
on demand based on their purpose and cost. The way to do so involved dividing the tests
by directory or by name, such that we could point the test runner to a specific directory or
filter for test names with the -k option.
While those strategies are available on pytest too, pytest provides more ways to
organize and divide tests; one of them being markers.
Instead of naming all our smoke tests "test_smoke_something", for example, we could
just name the test "test_something" and mark it as a smoke test. Or, we could mark slow
tests, so that we can avoid running slow ones during the most frequent runs.
Marking a test is as easy as decorating it with @pytest.mark.marker, where marker is
our custom label. For example, we could create two tests and use @pytest.mark.first to
mark the first of the two tests:
import pytest
@pytest.mark.first
def test_one():
    assert True
def test_two():
    assert True
At this point, we could select which tests to run by using pytest -m first or pytest -m
"not first":
$ pytest test_markers.py -v
...
test_markers.py::test_one PASSED [ 50%]
test_markers.py::test_two PASSED [100%]


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


