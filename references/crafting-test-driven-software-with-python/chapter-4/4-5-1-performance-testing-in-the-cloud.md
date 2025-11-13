# 4.5.1 Performance testing in the cloud (pp.136-136)

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


