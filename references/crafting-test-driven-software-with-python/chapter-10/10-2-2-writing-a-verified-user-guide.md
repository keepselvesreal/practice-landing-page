# 10.2.2 Writing a verified user guide (pp.226-231)

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


