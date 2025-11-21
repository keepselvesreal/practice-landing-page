# 7.5 Summary (pp.187-188)

---
**Page 187**

Fitness Function with a Contact Book Application
Chapter 7
[ 187 ]
Summary
In this chapter, we saw how we can write acceptance tests that can be shared with other
stakeholders to review the behavior of the software and not just be used by developers as a
way to verify that behavior. We saw that it's possible to express the specifications of the
software itself in the form of scenarios and examples, which guarantees that our
specifications are always in sync with what the software actually does and that our
software must always match the specifications as they become the tests themselves.
Now that we know how to move a project forward in a test-driven way using PyTest, in the
next chapter we are going to see more essential PyTest plugins that can help us during our
daily development practice.


---
**Page 188**

8
PyTest Essential Plugins
In the previous chapter, we saw how to work with PyTest and pytest-bdd to create
acceptance tests and verify the requirements of our software.
However, pytest-bdd is not the only useful plugin that PyTest has. In this chapter, we are
going to continue working on the contacts project introduced in Chapter 7, Fitness Function
with a Contact Book Application, showing how some of the most commonly used PyTest
plugins can help during the development of a project.
The plugins we are going to cover in this chapter are going to help us with verifying our
test suite coverage of the application code, checking the performance of our application,
dealing with tests that are flaky or unstable, and optimizing our development process by
running only the impacted tests when we change the code base or by speeding up our
whole test suite execution.
In this chapter, we will cover the following topics:
Using pytest-cov for coverage reporting
Using pytest-benchmark for benchmarking
Using flaky to rerun unstable tests
Using pytest-testmon to rerun tests on code changes
Running tests in parallel with pytest-xdist


