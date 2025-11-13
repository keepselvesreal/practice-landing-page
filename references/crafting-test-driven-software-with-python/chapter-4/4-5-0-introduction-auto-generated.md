# 4.5.0 Introduction [auto-generated] (pp.131-136)

---
**Page 131**

Scaling the Test Suite
Chapter 4
[ 131 ]
Enabling continuous integration
Wouldn't it be convenient if someone else was in charge of running all our tests every time
we made a change to our code base? This would mean that we couldn't forget to run some
specific tests just because they were related to an area of the code that we were not directly
touching.
That's exactly the goal of Continuous Integration (CI) environments. Every time we push
our changes to the code repository, these environments will notice and rerun the tests,
usually merging our changes with the changes from our colleagues to make sure they cope
well together.
If you have a code repository on GitHub, using Travis as your CI is a fairly straightforward
process. Suppose that I made an amol-/travistest GitHub project where I pushed the
code base of our chat application; to enable Travis, the first thing that I have to do is to go
to https:/​/​travis-​ci.​com/​ and log in with my GitHub credentials:
Figure 4.1 – Travis CI Sign in page


---
**Page 132**

Scaling the Test Suite
Chapter 4
[ 132 ]
Once we are in, we must enable the integration with GitHub so that all our GitHub
repositories become visible on Travis. We can do this by clicking on the top-right profile
icon and then on the Settings option. That will show us a green Activate button that will
allow us to enable Travis on our GitHub repositories:
Figure 4.2 – Integrating with GitHub


---
**Page 133**

Scaling the Test Suite
Chapter 4
[ 133 ]
Once we have enabled the Travis application on GitHub, we can go
to https://travis-
ci.com/github/{YOUR_GITHUB_USER}/{GITHUB_PROJECT} (which in my case
is https:/​/​travis-​ci.​com/​github/​amol-​/​travistest) to confirm the repository is
activated, but hasn't yet got any build:
Figure 4.3 – Conﬁrming that the repository was activated
Travis will be monitoring your repository for changes. But it won't know how to run tests
for your project. So even if we push changes to the source code, nothing will happen.
To tell Travis how to run our tests, we need to add to the repository a .travis.yml file
with the following configuration: 
language: python
os: linux
dist: xenial
python:
  - 3.7
  - &mainstream_python 3.8
  - nightly
install:
  - "pip install -e src"
script:


---
**Page 134**

Scaling the Test Suite
Chapter 4
[ 134 ]
  - "python -m unittest discover tests -v"
after_success:
  - "python -m unittest discover benchmarks -v"
This configuration is going to run our tests on Python 3.7, 3.8, and the current nightly build
of Python (3.9 at the time of writing). 
Before running the tests (the install: section), it will install the chat distribution from
src to make the chat package available to the tests.
Then the tests will be performed as specified in the script: section and if they succeed,
the benchmarks will be executed as stated in the after_success: section.
Once we push into the repository the .travis.yml file, Travis will see it and will start
executing the tests as specified in the configuration file. If everything worked as expected,
by refreshing the Travis project page, we should see a successful run of our tests on the
three versions of Python:
Figure 4.4 – Successful run on the three versions of Python


---
**Page 135**

Scaling the Test Suite
Chapter 4
[ 135 ]
If you click on any of the jobs, it will show you what happened, confirming that both the
tests and benchmarks were run:
Figure 4.5 – Checking the code base
Every time we make a change to our code base, Travis will rerun all tests, guaranteeing for
us that we haven't broken anything and allowing us to see whether the performances
became worse with the most recent changes.
Travis is not limited to performing a single thing such as running tests for your projects; it
can actually perform multi-state pipelines that can be evolved to create releases of your
packages or deploy them to a staging environment when the tests succeed. Just be aware
that every build that you do will consume credits, and while you do have some available
for free, you will have to switch to a paid plan if your CI needs grow beyond the amount
covered by free credits.


---
**Page 136**

Scaling the Test Suite
Chapter 4
[ 136 ]
Performance testing in the cloud
While our CI system does most of what we need, it's important to remember that cloud
runners are not designed for benchmarking. So our performance test suite only becomes 
reliable when there are major slowdowns and over the course of multiple runs.
The two most common strategies when running performance tests in the cloud are as
follows:
To rerun the test suite multiple times and pick the fastest run, in order to absorb
the temporary contention of resources in the cloud
To record the metrics into a monitoring service such as Prometheus, from which
it becomes possible to see the trend of the metrics over the course of multiple
runs
Whichever direction you choose to go in, make sure you keep in mind that cloud services
such as Travis can have random slowdowns due to the other requests they are serving, and
thus it's usually better to make decisions over the course of multiple runs.
Summary
In this chapter, we saw how we can keep our test suite effective and comfortable as the
complexity of our application and the size of our test suites grow. We saw how tests can be
organized into different categories that could be run at different times, and also saw how
we can have multiple different test suites in a single project, each serving its own purpose.
In general, over the previous four chapters, we learned how to structure our testing
strategy and how testing can help us design robust applications. We also saw how Python
has everything we need built in already through the unittest module.
But as our test suite grows and becomes bigger, there are utilities, patterns, and features
that we would have to implement on our own in the unittest module. That's why, over
the course of many years, many frameworks have been designed for testing by the Python
community. In the next chapter, we are going to introduce pytest, the most widespread
framework for testing Python applications.


