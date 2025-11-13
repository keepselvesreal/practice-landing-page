# 10.1 Technical requirements (pp.220-221)

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


