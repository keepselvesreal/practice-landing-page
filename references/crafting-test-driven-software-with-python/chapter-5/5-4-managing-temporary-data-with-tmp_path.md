# 5.4 Managing temporary data with tmp_path (pp.148-149)

---
**Page 148**

Introduction to PyTest
Chapter 5
[ 148 ]
In the upcoming sections, we are going to look at some of the built-in fixtures that pytest
provides and that are generally useful during the development of a test suite.
Managing temporary data with tmp_path
Many applications need to write data to disk. Surely we don't want data written during
tests to interfere with the data we read/write during the real program execution. Data
fixtures used in tests usually have to be predictable and we certainly don't want to corrupt
real data when we run our tests.
So it's common for a test suite to have its own read/write path where all the data is written.
If we decided the path beforehand, by the way, there would be the risk that different test
runs would read previous data and thus might not spot bugs or might fail without a
reason.
For this reason, one of the fixtures that pytest provides out of the box is tmp_path, which,
when injected into a test, provides a temporary path that is always different on every test
run. Also, it will take care of retaining the most recent temporary directories (for debugging
purposes) while deleting the oldest ones:
def test_tmp(tmp_path):
    f = tmp_path / "file.txt"
    print("FILE: ", f)
    f.write_text("Hello World")
    fread = tmp_path / "file.txt"
    assert fread.read_text() == "Hello World"
The test_tmp test creates a file.txt file in the temporary directory and writes "Hello
World" in it. Once the write is completed, it tries to access the same file again and confirm
that the expected content was written.
The tmp_path argument will be injected by pytest itself and will point to a path made by
pytest for that specific test run.
This can be seen by running our test with the -s option, which will make the "FILE: ..."
string that we printed visible:
$ pytest test_tmppath.py -v -s
===== test session starts =====
...
collected 1 item


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


