# 5.5 Testing I/O with capsys (pp.149-150)

---
**Page 149**

Introduction to PyTest
Chapter 5
[ 149 ]
test_tmppath.py::test_tmp
FILE: /tmp/pytest-of-amol/pytest-3/test_tmp0/file.txt
PASSED
===== 1 passed in 0.03s =====
On every new run, the pytest-3 directory will be increased, so the most recent directory
will be from the most recent run and only the latest three directories will be kept.
Testing I/O with capsys
When we implemented the test suite for the TODO list application, we had to check that the
output provided by the application was the expected one. That meant that we provided a
fake implementation of the standard output, which allowed us to see what the application
was going to write.
Suppose you have a very simple app that prints something when started:
def myapp():
    print("MyApp Started")
If we wanted to test that the app actually prints what we expect when started, we could use
the capsys fixture to access the capture output from sys.stdout and sys.stderr of our
application:
def test_capsys(capsys):
    myapp()
    out, err = capsys.readouterr()
    assert out == "MyApp Started\n"
The test_capsys test just starts the application (running myapp), then through
capsys.readouterr() it retrieves the content of sys.stdout and sys.stderr
snapshotted at that moment. 
Once the standard output content is available, it can be compared to the expected one to
confirm that the application actually printed what we wanted. If the application really
printed "MyApp Started" as expected, running the test should pass and confirm that's the
content of the standard output:
$ pytest test_capsys.py -v
===== test session starts =====
...
collected 1 item


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


