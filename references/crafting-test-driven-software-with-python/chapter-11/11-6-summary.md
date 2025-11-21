# 11.6 Summary (pp.280-281)

---
**Page 280**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 280 ]
Summary
In this chapter, we saw how we can test HTTP-based applications and how we can verify
the behavior of HTTP clients, HTTP servers, and even the two of them together. This is all
thanks to the WSGI protocol that powers the Python web ecosystem. We have also seen
how testing works in the Django world when Django's test client is used, thus we are fairly
capable of writing effective test suites for whatever web framework we are going to use.
Our testing isn't fully complete by the way. We are verifying the endpoints, checking that
the web pages contain the responses we expect, but we have no way to check that, once
those responses are read by a web browser, they actually behave as we expected. Even
worse, if there is JavaScript involved, we don't have any way to verify that the JavaScript in
those web pages is actually doing what we want.
So in the next chapter, we are going to see how we can test our web applications with a real
browser while also verifying the JavaScript that our web pages contain, thus completing the
list of skills we might need to develop a fully tested web application.


---
**Page 281**

12
End-to-End Testing with the
Robot Framework
In the previous chapter, we saw how to test web applications and, in general, applications
that rely on the HTTP protocol, both client and server side, but we were unable to test how
they perform in a real browser. With their complex layouts, the fact that CSS and JavaScript
are heavily involved in testing your application with WebTest or a similar solution might
not be sufficient to guarantee users that they are actually able to work with it. What if a
button is created by JavaScript or it's disabled by CSS? Those conditions are hard to test
using WebTest and we might easily end up with a test that clicks that button even though
the button wasn't actually usable by users.
To guarantee that our applications behave properly, it is a good idea to have a few tests that
verify at least the more important areas of the application using a real browser. As those
kinds of tests tend to be very slow and fragile, you still want to have the majority of your
tests written using solutions such as WebTest or even unit tests, which don't involve the
whole application life cycle, but having the most important parts of the web application
verified using real browsers will guarantee that at least the critical path of your web
application works on all major browsers. 
The Robot framework is one of the most solid solutions for writing the end-to-end tests that
drive web browsers and mobile applications in the Python world. It was originally
developed by Nokia and evolved under the open source community, and is a long-standing
and solid solution with tons of documentation and plugins. It is therefore battle tested and
ready for your daily projects.
In this chapter, we will cover the following topics:
Introducing the Robot framework
Testing with web browsers
Extending the Robot framework


