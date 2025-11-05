# 10.2.0 Introduction [auto-generated] (pp.221-223)

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


