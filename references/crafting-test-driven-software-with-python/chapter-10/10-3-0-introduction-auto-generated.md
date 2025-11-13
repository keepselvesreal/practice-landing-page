# 10.3.0 Introduction [auto-generated] (pp.231-237)

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


