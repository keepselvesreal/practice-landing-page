# 8.7 Summary (pp.206-207)

---
**Page 206**

PyTest Essential Plugins
Chapter 8
[ 206 ]
If you are unsure about how many workers to start, the -n option also accepts the value
"auto", which will detect how many processes to start based on how many CPUs the
system has.
It is, by the way, important to note that if the test suite is very fast and runs in just a matter
of seconds, running it in parallel might actually just make it slower. Distributing the tests
across different workers and starting them involves some extra work.
Summary
In this chapter, we saw the most frequently used plugins that exist for PyTest, those plugins
that can make your life easier by taking charge of some frequent needs that nearly every
test suite will face.
But there isn't any PyTest plugin that is able to manage the test environment itself. We are
still forced to set up manually all dependencies that the tests have and ensure that the
correct versions of Python are available to run the tests.
It would be great if there was a PyTest plugin able to install everything that we need in
order to run our test suite and just "run tests" on a new environment. Well, the good news
is that it exists; it's not strictly a PyTest plugin, but it's what Tox, which we are going to
introduce in the next chapter, was designed for.


---
**Page 207**

9
Managing Test Environments
with Tox
In the previous chapter, we covered the most frequently used PyTest plugins. Through
them, we are able to manage our test suite within a Python environment. We can configure
how the test suite should work, as well as enable coverage reporting, benchmarking, and
many more features that make it convenient to work with our tests. But what we can't do is
manage the Python environment itself within which the test suite runs.
Tox was invented precisely for that purpose; managing Python versions and the
environment that we need to run our tests. Tox takes care of setting up the libraries and
frameworks we need for our test suite to run and will check our tests on all Python versions
that are available.
In this chapter, we will cover the following topics:
Introducing Tox
Testing multiple Python versions with Tox
Using Tox with Travis
Technical requirements
We need a working Python interpreter along with Tox. Tox can be installed with the
following command:
$ pip install tox
Even though we are going to use the same test suite and contacts app we wrote in Chapter
8, PyTest Essential Plugins, we only need to install Tox 3.20.0. All other dependencies will be
managed by Tox for us.


