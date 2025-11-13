# 11.1 Technical requirements (pp.243-243)

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


