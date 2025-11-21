# 10.2.1 Adding a code-based reference (pp.223-226)

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


