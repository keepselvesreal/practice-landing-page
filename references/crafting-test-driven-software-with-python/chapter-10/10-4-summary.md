# 10.4 Summary (pp.240-242)

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


