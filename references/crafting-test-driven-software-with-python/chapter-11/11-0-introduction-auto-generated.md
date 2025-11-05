# 11.0 Introduction [auto-generated] (pp.242-243)

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


---
**Page 243**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 243 ]
Technical requirements
We need a working Python interpreter with pytest, but for some sections in this chapter, we
will also have to install other libraries and frameworks. As usual, all of them can be
installed with pip:
$ pip install pytest
For the Testing HTTP section, we are going to need the requests library and the
requests-mock testing library:
$ pip install requests requests-mock
For the Testing WSGI with WebTest section, we are going to need webtest:
$ pip install webtest
And for the paragraphs regarding testing web frameworks, we are going to need the
targeted web frameworks installed, even though you aren't going to use all of them
concurrently in a real project:
$ pip install flask django pyramid turbogears2
The examples have been written on Python 3.7, pytest 6.0.2, Requests 2.24.0, Requests-Mock
1.8.0, WebTest 2.0.35, Django 3.1.4, Flask 1.1.2, Pyramid 1.10.5, and TurboGears 2.4.3, but
should work on most modern Python versions. You can find the code files present in this
chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Software-​with-​Python/​tree/​main/​Chapter11.
Testing HTTP
A frequent need when working with networking based applications is that we have to test
both the server and client. If we are writing a distributed application, we are probably
going to write both the client and the server ourselves, and that means we'll want to test
both of them just as we did with our Chat application in previous chapters.


