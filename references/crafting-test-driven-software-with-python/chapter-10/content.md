# Chapter 10: Testing Documentation and Property-Based Testing (pp.220-242)

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


---
**Page 221**

Testing Documentation and Property-Based Testing
Chapter 10
[ 221 ]
Testing documentation
When documentation is written with the goal of teaching other developers how a system
works, providing examples on how to use its inner layers, and train them on the driving
design principles behind some complex software, it can be a very effective way to onboard
new team members in a project.
In any fairly big and complex project, documentation becomes something that is essential
for navigating the complexity of the system without having to rely on our memory to
remember how to use every single layer or class involved in the system.
But documentation is also hard. Not only is it actually hard to write, because what might
seem obvious and clear to us might sound cryptic to another reader, but also because the
code evolves quickly and documentation easily becomes outdated and inaccurate.
Thankfully, testing is a very effective way to also ensure that our documentation doesn't get
outdated and that it still applies to our system. As much as we test the application code, we
can test the documentation examples. If an example becomes outdated, it will fail and our
documentation tests won't pass.
Given that we have covered every human-readable explanation in our documentation with
a code example, we can make sure that our documentation doesn't get stale and still
describes the current state of the system by verifying those code examples. To show how
documentation can be kept in sync with the code, we are going to take our existing contacts
application we built in previous chapters and we are going to add tested documentation to
it.
Our first step will be to create the documentation itself. In Python, the most common tool
for documentation is Sphinx, which is based on the reStructuredText format.
Sphinx provides the sphinx-quickstart command to create new documentation for a
project. Running sphinx-quickstart docs will ask a few questions about the layout of
our documentation project and will create it inside the docs directory. We will also provide
the --ext-doctest --ext-autodoc options to enable the extensions to make
documentation testable and to autogenerate documentation from existing code:
$ sphinx-quickstart docs --ext-doctest --ext-autodoc
Welcome to the Sphinx 3.3.0 quickstart utility.
...
> Separate source and build directories (y/n) [n]: y
> Project name: Contacts
> Author name(s): Alessandro Molina


---
**Page 222**

Testing Documentation and Property-Based Testing
Chapter 10
[ 222 ]
> Project release []:
> Project language [en]:
Creating file docs/source/conf.py.
Creating file docs/source/index.rst.
Creating file docs/Makefile.
Creating file docs/make.bat.
Finished: An initial directory structure has been created.
Once our documentation is available in the docs directory, we can start populating it,
beginning with docs/source/index.rst, which will be the entry point for our
documentation. If we want to add further sections to it, we have to list them under the
toctree section.
In our case, we are going to create a section about how to use the software and a reference
section for the existing classes and methods. Therefore, we are going to add contacts and
reference sections to toctree in the docs/source/index.rst file:
Welcome to Contacts's documentation!
===============================
.. toctree::
   :maxdepth: 2
   :caption: Contents:
   contacts
   reference
Now, we could try to build our documentation to see whether the two new sections are
listed on the home page. But doing so would actually fail because we haven't yet created
the files for those two sections:
$ make html
Running Sphinx v3.3.0
...
docs/source/index.rst:9: WARNING: toctree contains reference to nonexisting
document 'contacts'
docs/source/index.rst:9: WARNING: toctree contains reference to nonexisting
document 'reference'
So, we are going to create docs/source/contacts.rst and
docs/source/reference.rst files to allow Sphinx to find them.


---
**Page 223**

Testing Documentation and Property-Based Testing
Chapter 10
[ 223 ]
Adding a code-based reference
First, we will add the reference section, as it's the simplest one. The
docs/source/reference.rst file will only contain the title and the directive that will tell
Sphinx to document the contacts.Application class based on the docstring we provide
in the code itself:
==============
Code Reference
==============
.. autoclass:: contacts.Application
    :members:
Recompiling our documentation with make html will now only report the missing
contacts.rst file and successfully generate the code reference section. The result will be
visible in the docs/build/ directory, hence, opening the docs/build/reference.html
file will now show our code reference.
The first time we build it, our reference will be mostly empty:
Figure 10.1 – Code reference
It has a section for the contacts.Application class, but nothing else. This is because the
content is taken directly from the code docstrings, and we haven't written any.


---
**Page 224**

Testing Documentation and Property-Based Testing
Chapter 10
[ 224 ]
Therefore, we should go back to our contacts/__init__.py file and add a docstring to
our Application class and to the Application.run method:
class Application:
    """Manages a contact book serving the provided commands.
    The contact book data is saved in a contacts.json
    file in the directory the application is
    launched from. Any contacts.json in the directory this
    is launched from will be loaded at init time.
    A contact is composed by any name followed by a valid
    phone number.
    """
    PHONE_EXPR = re.compile('^[+]?[0-9]{3,}$')
    def __init__(self):
        self._clear()
    def _clear(self):
        self._contacts = []
    def run(self, text):
        """Run a provided command.
        :param str text: The string containing the command to run.
        Takes the command to run as a string as it would
        come from the shell, parses it and runs it.
        Each command can support zero or multiple arguments
        separate by an empty space.
        Currently supported commands are:
         - add
         - del
         - ls
        """
        ...
Now that the class and the method are both documented, we can rebuild our
documentation with make html to see whether the reference has been properly generated.


---
**Page 225**

Testing Documentation and Property-Based Testing
Chapter 10
[ 225 ]
If everything works as expected, we should see in docs/build/reference.html the
documentation we wrote in the code:
Figure 10.2 – Reference generated
Mixing code and documentation in the source files is an effective technique for ensuring
that when the code changes, the documentation is updated too. For example, if we remove
a method, we would surely also remove its docstring too, and so the method would also
disappear from the documentation. Obviously, we still have to pay attention that what we
write in the docstrings makes sense, but at least the structure of our documentation would
always be in sync with the structure of our code.


---
**Page 226**

Testing Documentation and Property-Based Testing
Chapter 10
[ 226 ]
Writing a verified user guide
While it's effective for references, having a reference is usually far from being enough for
proper documentation. A usage guide and tutorials are frequently necessary to ensure that
the reader understands how the software works.
So, to make our documentation more complete, we are going to add a user guide to the
docs/source/contacts.rst file.
After a brief introduction, the docs/source/contacts.rst file will dive into some real-
world examples regarding how to add new contacts and how to list them:
===============
Manage Contacts
===============
.. contents::
Contacts can be managed through an instance of
:class:`contacts.Application`, use :meth:`contacts.Application.run`
to execute any command like you would in the shell.
Adding Contancts
================
.. code-block::
    app.run("contacts add Name 0123456789")
Listing Contacts
================
.. code-block::
    app.run("contacts ls")


---
**Page 227**

Testing Documentation and Property-Based Testing
Chapter 10
[ 227 ]
Now, if we rebuild our documentation with make html, we should no longer get any error
and opening docs/build/contacts.html should show the page we just wrote with the
two examples:
Figure 10.3 – Managing contacts
While this shows how we can use the application, it doesn't do anything to ensure that the
documentation is in sync with our code. If, for example, we ever replace the
Application.run method with Application.execute, the two examples on the page
won't even notice and will continue to say that you have to use app.run, which will be
incorrect.
How can we make sure that the examples and tutorials we write are actually always in sync
with how our application works for real? That's exactly what we can do using doctest.
Doctest is a Python module and Sphinx extension that allows us to write snippets of code
that are tested and verified in our documentation. So, we are going to use doctest to make
sure that those two examples actually run and do what we expect.
The first thing we have to do is to set up the application in the documentation file. So we
are going to add a testsetup directive to docs/source/contacts.rst with the code
that is necessary to make sure that the app object exists for real.


---
**Page 228**

Testing Documentation and Property-Based Testing
Chapter 10
[ 228 ]
For the sake of order, we are going to add this code at the end of the introductory
paragraph, right before the examples themselves:
Manage Contacts
===============
.. contents::
Contacts can be managed through an instance of
:class:`contacts.Application`, use :meth:`contacts.Application.run`
to execute any command like you would in the shell.
.. testsetup::
    from contacts import Application
    app = Application()
Then we are going to replace the two code-block directives with two testcode
directives, which means that the examples will actually be executed and checked to ensure
that they are not crashing:
Adding Contacts
================
.. testcode::
    app.run("contacts add Name 0123456789")
Listing Contacts
================
.. testcode::
    app.run("contacts ls")
code-block directives instruct Sphinx that the content should be formatted as code, but
does nothing to ensure that the content is actually valid code that does not crash. While the
testcode directive formats the code, it also ensures that it is valid code that can run.
Now we are verifying that the two commands can actually run, so if we ever renamed
Application.run to Application.execute, our testcode examples would fail to run
and so Sphinx would complain that we have to update the documentation.


---
**Page 229**

Testing Documentation and Property-Based Testing
Chapter 10
[ 229 ]
But making sure that they can run is not enough. We also want to ensure that they actually
do what we expect, that once we add a contact and list them back, we do see the new
contact. The doctest module provides us with the testoutput directive to ensure that
the previous testcode block provided the expected output. In this case, we are going to
add a testoutput directive right after the code block that lists our contacts that will
ensure that the contact we just added is listed back:
Listing Contacts
================
.. testcode::
    app.run("contacts ls")
.. testoutput::
    Name 0123456789
If we rerun make html, we are going to see that in the resulting documentation, not much
has changed. There is an extra paragraph with the output after the second example, which
is good, as it gives a hint of what the expected output of the ls command is, but apart from
that, our documentation looks the same as before:
Figure 10.4 – Manage Contacts updated


---
**Page 230**

Testing Documentation and Property-Based Testing
Chapter 10
[ 230 ]
The real difference happens when we run the make doctest command, which allows us to
verify that the examples in our documentation do work correctly:
$ make doctest
Running Sphinx v3.3.0
...
running tests...
Document: contacts
------------------
1 items passed all tests:
  2 tests in default
2 tests in 1 items.
2 passed and 0 failed.
Test passed.
Doctest summary
===============
    2 tests
    0 failures in tests
    0 failures in setup code
    0 failures in cleanup code
build succeeded.
doctest found two tests ( the two testcode blocks) within the contacts.rst document
and it confirmed that both of them work correctly.
If, as we mentioned before, we ever rename the Application.run method to
Application.execute, the doctests will immediately point out that both examples are
wrong:
Document: contacts
------------------
**********************************************************************
File "contacts.rst", line 41, in default
Failed example:
    app.run("contacts add Name 0123456789")
Exception raised:
    Traceback (most recent call last):
      File "/usr/lib/python3.8/doctest.py", line 1336, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest default[0]>", line 1, in <module>
        app.run("contacts add Name 0123456789")
    AttributeError: 'Application' object has no attribute 'run'
**********************************************************************
File "contacts.rst", line 55, in default
Failed example:


---
**Page 231**

Testing Documentation and Property-Based Testing
Chapter 10
[ 231 ]
    app.run("contacts ls")
Exception raised:
    Traceback (most recent call last):
      File "/usr/lib/python3.8/doctest.py", line 1336, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest default[0]>", line 1, in <module>
        app.run("contacts ls")
    AttributeError: 'Application' object has no attribute 'run'
**********************************************************************
1 items had failures:
   2 of 2 in default
2 tests in 1 items.
0 passed and 2 failed.
***Test Failed*** 2 failures.
Likewise, if anything goes wrong in our two examples or the contacts listed don't match
those in the testoutput section, the make doctest command would report those failures
and would inform us that our documentation is not in sync with our code.
Adding the make doctest command to our CI pipeline allows us to ensure that with
every change of code that affects the documentation, the documentation is updated too,
thereby guaranteeing that all our examples in the documentation are verified and up to
date with what our code actually does.
Property-based testing
Now that we know how to have working test suites for both our code and our
documentation, the quality of those test suites fully depends on our capability to design
and write good tests.
There is, by the way, one rule in software testing that can help us design good tests, and
this is that errors usually hide in corner cases and limit values. If we have a function that
performs division between two numbers, the bugs are probably going to be brought to the
surface when zero, the maximum integer value, or negative numbers are passed to the
function as arguments. Rarely will we see errors for most common values, such as 2, 3, 4, or
5. That's because developers usually tend to design their code with those common values in
mind. The design that comes more naturally is usually the one that works for the most
obvious cases, and corner cases rarely come to mind in the first instance.


---
**Page 232**

Testing Documentation and Property-Based Testing
Chapter 10
[ 232 ]
Property-based testing comes in handy when easily generating tests that verify those corner
cases and limit conditions by ensuring that some properties of the functions and methods
we test always hold true. Property-based testing had its origins in the Haskell community,
but libraries and frameworks to implement it are now available in most programming
languages, including Python.
Hypothesis is a library that allows us to implement property-based testing in Python.
An example of the properties of a function could be that "for any provided argument, the
function should never crash." Not crashing is the most frequently verified property, but it's
possible to check any invariant that our method should guarantee. If we have a function
such as concat(a: str, b: str, c: str)-> str, a property could be that the
returned value should always include b for any provided arguments.
Hypothesis helps us define those invariants and then takes care of generating as many tests
as possible that assert that those properties always hold true. Usually, this is done by
generating tests based on the domain of function arguments and ensuring that the
properties hold true for all values. Obviously, testing all possible values would be too
cumbersome, or even not doable at all since, for example, the values of the str domain are
infinite. For this reason, Hypothesis is smart enough to know which values most frequently
cause problems in a domain and will restrict the tests to those, also remembering which
values caused problems to our code in the past, so that our test suite remains fast but also
effective.
The most common usage of the Hypothesis testing library is as a replacement of the
pytest.mark.parametrize decorator to automatically generate tests that run for
different kinds of values based on the types of arguments.
In the case of our contacts book application, we might want to ensure that the contact book
works for any kind of name the contacts have. We don't know whether our users will be
from the USA, Europe, the Middle-East, or Asia, and so might have totally different
concepts of names.


---
**Page 233**

Testing Documentation and Property-Based Testing
Chapter 10
[ 233 ]
Using pytest.mark.parametrize, we could write a test that does that for some cases that
come to mind:
import pytest
from contacts import Application
@pytest.mark.parametrize("name",
    ["Mario Alberto Rossi", "Étienne de La Boétie", "اﻟﺰورق"]
)
def test_adding_contacts(name):
 app = Application()
 app.run(f"contacts add {name} 3456789")
 assert app._contacts == [(name, "3456789")]
The test will pass, and will try for some names and cases that come to mind:
$ pytest -v
================= test session starts =================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
...
collected 3 items
tests/test_properties.py::test_adding_contacts[Mario Alberto Rossi] PASSED
[ 33%]
tests/test_properties.py::test_adding_contacts[\xc3\x89tienne de La
Bo\xc3\xa9tie] PASSED [ 66%]
tests/test_properties.py::test_adding_contacts[\u0627\u0644\u0632\u0648\u06
31\u0642] PASSED [100%]
================= 3 passed in 0.04s =================
But is this actually a good enough test? Let's see what happens if, instead of picking the
values ourselves, we use Hypothesis to generate those tests. Implementing this change is as
easy as replacing the parametrize decorator with a hypothesis.given decorator:
import hypothesis
import hypothesis.strategies as st
from contacts import Application
@hypothesis.given(st.text())
def test_adding_contacts(name):
    app = Application()
    app.run(f"contacts add {name} 3456789")
    assert app._contacts == [(name, "3456789")]


---
**Page 234**

Testing Documentation and Property-Based Testing
Chapter 10
[ 234 ]
Now, running the Hypothesis version of the test leads to a much more interesting result
compared to the version based on @parametrize; the Hypothesis-based version of the test
actually fails:
$ pytest -v
================= test session starts =================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
...
collected 1 item
tests/test_properties.py::test_adding_contacts FAILED [100%]
====================== FAILURES ======================
________________ test_adding_contacts ________________
    @given(st.text())
> def test_adding_contacts(name):
tests/test_properties.py:8:
_ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_properties.py:11: in test_adding_contacts
    app.run(f"contacts add {name} 3456789")
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
self = <contacts.Application object at 0x7f9a71fce850>,
text = 'contacts add 3456789'
    def run(self, text):
        ...
        if cmd == "add":
>           name, num = args.rsplit(maxsplit=1)
E           ValueError: not enough values to unpack (expected 2, got 1)
src/contacts/__init__.py:48: ValueError
--------------------- Hypothesis ---------------------
Falsifying example: test_adding_contacts(
    name='',
)
================= 1 failed in 0.10s =================


---
**Page 235**

Testing Documentation and Property-Based Testing
Chapter 10
[ 235 ]
So, Hypothesis actually found a real bug in our software. If we don't provide a name at all,
the software, instead of providing an error message, just crashes. We can see that
Hypothesis tells us that the example that failed is the one where name='' and PyTest
confirms that the string that was executed as a command was text = 'contacts add
3456789'. The line that crashed is the one that splits the name and number out of the add
command arguments, so we have to handle the case where we can't split them apart
because we only have one argument.
To do so, we can go back to the Application.run method and trap the exception that can
come out of args.rsplit:
        if cmd == "add":
            try:
                name, num = args.rsplit(maxsplit=1)
            except ValueError:
                print("A contact must provide a name and phone number")
                return
            try:
                self.add(name, num)
            except ValueError as err:
                print(err)
                return
Now, if we rerun our test, we will get a slightly different kind of failure, a failure in the test
itself:
$ pytest -v
================= test session starts =================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
...
collected 1 item
tests/test_properties.py::test_adding_contacts FAILED [100%]
====================== FAILURES ======================
________________ test_adding_contacts ________________
    @given(st.text())
> def test_adding_contacts(name):
tests/test_properties.py:8:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_properties.py:11: in test_adding_contacts
    app.run(f"contacts add {name} 3456789")
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
name = ''


---
**Page 236**

Testing Documentation and Property-Based Testing
Chapter 10
[ 236 ]
    @given(st.text())
    def test_adding_contacts(name):
        app = Application()
        app.run(f"contacts add {name} 3456789")
>       assert app._contacts == [(name, "3456789")]
E       AssertionError: assert [] == [('', '3456789')]
E          Right contains one more item: ('', '3456789')
E          Full diff:
E          - [('', '3456789')]
E          + []
tests/test_properties.py:15: AssertionError
---------------- Captured stdout call ----------------
A contact must provide a name and phone number
--------------------- Hypothesis ---------------------
Falsifying example: test_adding_contacts(
    name='',
)
================= 1 failed in 0.10s =================
From Captured stdout, we can see that the error we emit when no name is provided was
properly reported, but our test failed because the assertion expects that a new contact is
always inserted while, in the case of a missing name, no contact gets added to our contact
book. So, in this case, Hypothesis found that our test itself is actually incomplete.
What we have to do is to change the assertion to ensure that the contact book actually
contains what we really expect in the case where no name is provided. In case there is no
name, the contact book should just be empty:
@given(st.text())
def test_adding_contacts(name):
    app = Application()
    app.run(f"contacts add {name} 3456789")
    name = name.strip()
    if name:
        assert app._contacts == [(name, "3456789")]
    else:
        assert app._contacts == []
At this point, rerunning the test will actually confirm that everything works as expected:
$ pytest -v
================= test session starts =================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
...


---
**Page 237**

Testing Documentation and Property-Based Testing
Chapter 10
[ 237 ]
collected 1 item
tests/test_properties.py::test_adding_contacts PASSED [100%]
================= 1 passed in 0.42s =================
We have seen how Hypothesis can help us to identify bugs and design tests, but it can
actually do much more. It can even go as far as generating some tests for the most common
properties for us.
Generating tests for common properties
Through the hypothesis write command, we can use Hypothesis to generate tests for
use based on some of the most common properties functions might have. For example, if
we want to ensure that the Python sorted method is idempotent and calling it twice leads
to the exact same result, we can use hypothesis write --idempotent sorted to
generate a test that verifies such a property:
$ hypothesis write --idempotent sorted
from hypothesis import given, strategies as st
@given(
    iterable=st.one_of(st.iterables(st.integers()),
st.iterables(st.text())),
    key=st.none(),
    reverse=st.booleans(),
)
def test_idempotent_sorted(iterable, key, reverse):
    result = sorted(iterable, key=key, reverse=reverse)
    repeat = sorted(result, key=key, reverse=reverse)
    assert result == repeat, (result, repeat)
Or, we could test that a pair of encode/decode functions leads back to the original result
when chained using the hypothesis write --roundtrip generator.
If we want to check that for json.loads and json.dumps, for example, we could use
hypothesis write --roundtrip json.dumps json.loads, which would generate the
following code block:
$ hypothesis write --roundtrip json.dumps json.loads
import json
from hypothesis import given, strategies as st


---
**Page 238**

Testing Documentation and Property-Based Testing
Chapter 10
[ 238 ]
@given(
    allow_nan=st.booleans(),
    check_circular=st.booleans(),
    cls=st.none(),
    default=st.none(),
    ensure_ascii=st.booleans(),
    indent=st.none(),
    obj=st.nothing(),
    object_hook=st.none(),
    object_pairs_hook=st.none(),
    parse_constant=st.none(),
    parse_float=st.none(),
    parse_int=st.none(),
    separators=st.none(),
    skipkeys=st.booleans(),
    sort_keys=st.booleans(),
)
def test_roundtrip_dumps_loads(
    allow_nan,
    check_circular,
    cls,
    default,
    ensure_ascii,
    indent,
    obj,
    object_hook,
    object_pairs_hook,
    parse_constant,
    parse_float,
    parse_int,
    separators,
    skipkeys,
    sort_keys,
):
    value0 = json.dumps(
        obj=obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
    value1 = json.loads(
        s=value0,


---
**Page 239**

Testing Documentation and Property-Based Testing
Chapter 10
[ 239 ]
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
    )
    assert obj == value1, (obj, value1)
When refactoring code, implementing performance optimizations, or modifying code to
port it from prior versions of Python, an essential property of the new implementation we
are going to write is that it must retain the exact same behavior of the old implementation.
The hypothesis write --equivalent command is able to do precisely this.
If, for example, we had two helper functions in contacts/utils.py, both meant to sum
two numbers, as follows:
def sum1(a: int, b: int) -> int:
    return a + b
def sum2(a: int, b: int) -> int:
    return sum((a, b))
In that case, hypothesis could generate a test that verifies the fact that both functions lead
to the exact same results:
$ hypothesis write --equivalent contacts.utils.sum1 contacts.utils.sum2
import contacts.utils
from hypothesis import given, strategies as st
@given(a=st.integers(), b=st.integers())
def test_equivalent_sum1_sum2(a, b):
    result_sum1 = contacts.utils.sum1(a=a, b=b)
    result_sum2 = contacts.utils.sum2(a=a, b=b)
    assert result_sum1 == result_sum2, (result_sum1, result_sum2)
While most of those tests could be written manually using hypothesis.given, it can be
convenient having Hypothesis inspect the functions for you and pick the right types.
Especially if you already did the effort of providing type hints for your functions,
Hypothesis will usually be able to do the right thing.
To know all the generators that are available in your version of Hypothesis, you can run
hypothesis write --help.


---
**Page 240**

Testing Documentation and Property-Based Testing
Chapter 10
[ 240 ]
Summary
In this chapter, we saw how to have tested documentation that can guarantee user guides
in sync with our code, and we saw how to make sure that our tests cover limit and corner
cases we might not have considered through property-based testing.
Hypothesis can take away from you a lot of the effort of providing all possible values to a
parameterized test, thereby making writing effective tests much faster, while doctest can
ensure that the examples we write in our user guides remain effective in the long term,
detecting whether any of them need to be updated when our code changes.
In the next chapter, we are going to shift our attention to the web development world,
where we will see how to test web applications both from the point of view of functional
tests and end-to-end tests.


---
**Page 241**

3
Section 3: Testing for the Web
In this section, we will learn how to test web applications, web services, and APIs with
Python, PyTest, and the most common testing tools available for WSGI frameworks.
This section comprises the following chapters:
Chapter 11, Testing for the Web: WSGI versus HTTP 
Chapter 12, End-to-End Testing with the Robot Framework


---
**Page 242**

11
Testing for the Web: WSGI
versus HTTP
In the previous chapter, we saw how to test documentation and implement more advanced
testing techniques in our test suites, such as property-based testing.
One of the primary use cases for Python has become web development. Python has many
very effective and powerful web development frameworks. The most famous one is surely
the Django web framework, but many more of them exist, including the Flask framework,
the Pyramid framework, TurboGears2, and more. Each web framework has its own
peculiarities and unique features that make it easy to build most of the different kinds of
web applications using Python itself, but all of them share the same need of having to
verify that the applications you built work properly and are tested. Thus in this chapter, we
are going to see how we can test HTTP-based applications on both the client and server
side, how we can do that using pytest, and how the techniques presented differ from
framework-specific tests.
In this chapter, we will cover the following topics:
Testing HTTP
Testing WSGI with WebTest
Using WebTest with web frameworks
Writing Django tests with Django's test client
In this chapter, we are going to reverse the approach a bit and we are going to violate the
Test-Driven Development (TDD) principle by implementing the code first and
introducing tests for it after. The reason for this is that by introducing the system under test
first we can illustrate more clearly some details of the tests. If you already know how the
tested software works, it's easier to understand why the tests do the things they do, so for
the purposes of this chapter we will briefly abandon our best practices and focus on the
code first, and the tests after.


