# 8.2.0 Introduction [auto-generated] (pp.189-194)

---
**Page 189**

PyTest Essential Plugins
Chapter 8
[ 189 ]
Technical requirements
We need a working Python interpreter with the PyTest framework installed with the
pytest-bdd plugin. PyTest and pytest-bdd can be installed with the following command:
$ pip install pytest pytest-bdd
For each section, you will need to install the plugin discussed in the section itself. You can
install all of them at once:
$ pip install pytest-cov pytest-benchmark flaky pytest-testmon pytest-xdist
The examples have been written on Python 3.7 with PyTest 6.0.2 and pytest-bdd 4.0.1, but
should work on most modern Python versions. The versions of the plugins in use for each
section instead are pytest-cov 2.10, pytest-benchmark 2.3.2, flaky 3.7.0, pytest-testmon 1.0.3,
and pytest-xdist 2.1.0.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter08.
Using pytest-cov for coverage reporting
We have already seen in Chapter 1, Getting Started with Software Testing, how code
coverage by tests is a good measure for establishing how confident you can be in your test
suite. A test suite that only runs 10% of all our code is probably not going to be very reliable
in finding problems, as most of the code will go unchecked. A test suite that instead verifies
100% of our code is certainly going to exercise every single line of code we wrote and so
should trigger bugs more easily if there are any.
Obviously, coverage cannot verify code that you never wrote, so it's not going to detect that
you have a bug because you forgot to add an if check in your method, but at least it tells
you if you forgot to write a test for that method.
Normally, test coverage in Python is done using the coverage module, which can be
installed from PyPI, but PyTest has a convenient pytest-cov plugin that is going to do
that for us and make our life simpler when we want to check the coverage of our tests. Like
any other Python distribution, we can install pytest-cov through pip:
$ pip install pytest-cov


---
**Page 190**

PyTest Essential Plugins
Chapter 8
[ 190 ]
Installing pytest-cov makes the coverage reporting available through the --cov option.
Running PyTest with that option will immediately output the coverage at the end of the
test suite and will save it in a .coverage file to make it available for later consultation.
By default, running just pytest --cov will provide the coverage of every single module
that was imported during the execution of your tests (including all libraries and
frameworks you used in your application), which is not very helpful. As we only care about
the coverage of our own software, it's possible to tell pytest-cov which package to report
coverage for simply by adding it as an argument to the --cov option.
As we care about how much of our contacts application is actually verified by our tests, we
are going to run pytest --cov=contacts so that we get back coverage information only
for the contacts package, which is the one we care about:
$ pytest --cov=contacts
================= test session starts =================
plugins: cov-2.10.1, bdd-4.0.1
collected 23 items
tests/acceptance/test_adding.py .. [ 8%]
tests/functional/test_basic.py ... [ 21%]
tests/unit/test_adding.py ...... [ 47%]
tests/unit/test_application.py ....... [ 78%]
tests/unit/test_persistence.py .. [ 86%]
tests/acceptance/test_delete_contact.py . [ 91%]
tests/acceptance/test_list_contacts.py .. [100%]
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts  Miss  Cover
----------------------------------------------
src/contacts/__init__.py  48     1     98%
src/contacts/__main__.py  2      2     0%
----------------------------------------------
TOTAL 50 3 94%
Great! Our tests cover nearly all our code. The contacts/__init__.py module, which is
the one where we have all the code that implements our contact book app, is covered at
98%. Out of the 48 lines of code that compose it, there is only one line that isn't covered.


---
**Page 191**

PyTest Essential Plugins
Chapter 8
[ 191 ]
But how can we know which one it is? pytest-cov obviously knows; we just have to tell it to
print it out. That's what the --cov-report option is made for. If we run pytest with the -
-cov-report=term-missing option, it's going to tell us the lines of code that were not
covered by tests in each Python file:
$ pytest --cov=contacts --cov-report=term-missing
...
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts Miss Cover Missing
--------------------------------------------------------
src/contacts/__init__.py  48    1    98%   68
src/contacts/__main__.py  2     2    0%    1-3
--------------------------------------------------------
TOTAL                     50    3    94%
Here, for example, we know that lines 1 to 3 in contacts/__main__.py are not tested.
And that's OK, as those just import and invoke contacts.main() for the convenience of
being able to run our contacts program with python -m contacts once installed
(module.__main__ is what Python invokes when you pass a module to the -m option):
from . import main
main()
We can easily tell pytest-cov to ignore that code by simply adding a pragma: no cover
comment near to the lines or code block we want to exclude from coverage:
from . import main # pragma: no cover
main() # pragma: no cover
Now, if we rerun our test suite, we will no longer get complaints about the __main__.py
module:
$ pytest --cov=contacts --cov-report=term-missing
...
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts Miss Cover Missing
--------------------------------------------------------
src/contacts/__init__.py  48    1    98%   68
src/contacts/__main__.py  0     0    100%
--------------------------------------------------------
TOTAL                     48    1    98%


---
**Page 192**

PyTest Essential Plugins
Chapter 8
[ 192 ]
Only the code in contacts/__init__.py still reports uncovered code. This is the module
that contains the real code of our application, so the uncovered line probably has to be
tested for real. Once we check what that line refers to, we discover that we have not yet
tested the main function:
67  def main():
68      raise NotImplementedError()
As we haven't tested it, we never noticed that it still has to be implemented. This means
that currently, running our contacts module will simply crash:
$ python -m contacts
Traceback (most recent call last):
  ...
  File "src/contacts/__init__.py", line 68, in main
    raise NotImplementedError()
NotImplementedError
Thanks to coverage pointing, we found out that the main function didn't have a test for it.
We notice that a piece of our application is still lacking and we can now move to provide a
test for it and implement it.
We are going to create a new module in tests/functional/test_main.py where we are
going to write our test for the main function. Our test is going to provide some fake data
pre-loaded (we are not really interested in involving I/O here, so let's replace it with a fake
implementation) and verify that when the user runs the "contacts ls" command from
the command line, the contacts are actually listed back:
import sys
from unittest import mock
import contacts
class TestMain:
    def test_main(self, capsys):
        def _stub_load(self):
            self._contacts = [("name", "number")]
        with mock.patch.object(contacts.Application, "load",
                               new=_stub_load):
            with mock.patch.object(sys, "argv", new=["contacts", "ls"]):
                contacts.main()
        out, _ = capsys.readouterr()
        assert out == "name number\n"


---
**Page 193**

PyTest Essential Plugins
Chapter 8
[ 193 ]
The implementation required to pass our test is actually pretty short. We just have to create
the application, load the stored contacts, and then run the command provided on the
command line:
def main():
    import sys
    a = Application()
    a.load()
    a.run(' '.join(sys.argv))
We can then verify that we finally have 100% coverage of our code from tests and that they
all pass by rerunning the pytest --cov=contacts command:
$ pytest --cov=contacts
collected 24 items
tests/acceptance/test_adding.py .. [ 8%]
tests/functional/test_basic.py ... [ 20%]
tests/functional/test_main.py . [ 25%]
tests/unit/test_adding.py ...... [ 50%]
tests/unit/test_application.py ....... [ 79%]
tests/unit/test_persistence.py .. [ 87%]
tests/acceptance/test_delete_contact.py . [ 91%]
tests/acceptance/test_list_contacts.py .. [100%]
----------- coverage: platform linux, python 3.8.2-final-0 -----------
Name                      Stmts  Miss  Cover
----------------------------------------------
src/contacts/__init__.py  51     0     100%
src/contacts/__main__.py  0      0     100%
----------------------------------------------
TOTAL                     51     0     100%
If we want our coverage to be verified on every test run, we could leverage the addopts
option in pytest.ini and make sure that coverage is performed every time we run
PyTest:
[pytest]
addopts = --cov=contacts --cov-report=term-missing
As we have already seen, using addopts ensures that some options are always provided on
every PyTest execution. Thus, we will add coverage options every time we run PyTest.


---
**Page 194**

PyTest Essential Plugins
Chapter 8
[ 194 ]
Coverage as a service
Now that all our tests are passing and our code is fully verified, how can we make sure we
don't forget about verifying our coverage when we extend our code base? As we have seen
in Chapter 4, Scaling the Test Suite, there are services that enable us to run our test suite on
every new commit we do. Can we leverage them to also make sure that our coverage didn't
worsen?
Strictly speaking, ensuring that the coverage doesn't decrease requires comparing the
current coverage with the one of the previous successful run, which is something that
services such as Travis CI are not able to do as they don't persist any information after our
tests have run. So, the information pertaining to the previous runs is all lost.
Luckily, there are services such as Coveralls that integrate very well with Travis CI and
allow us to easily get our coverage in the cloud:
Figure 8.1 – Coveralls web page


