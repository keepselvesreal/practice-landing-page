# 12.0 Introduction [auto-generated] (pp.281-282)

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


---
**Page 282**

End-to-End Testing with the Robot Framework
Chapter 12
[ 282 ]
Technical requirements
We need a working Python interpreter with the Robot Framework installed. To run tests
with real browsers, we are also going to use the robotframework-seleniumlibrary and
the webdrivermanager utilities. To record videos of our tests, we are going to need
the robotframework-screencaplibrary library. robotframework, robotframework-
seleniumlibrary, robotframework-screencaplibrary, and webdrivermanager can
be installed with pip, in the same way as all other Python dependencies:
$ pip install robotframework robotframework-seleniumlibrary
webdrivermanager robotframework-screencaplibrary
The examples have been written on Python 3.7, robotframework 3.2.2, robotframework-
seleniumlibrary 4.5.0, robotframework-screencaplibrary 1.5.0, and webdrivermanager 0.9.0,
but should work on most modern Python versions. 
You can find the code present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter12.
Introducing the Robot Framework
The Robot Framework is an automation framework mostly used to create acceptance tests
in the Acceptance Test Driven Development (ATDD)  and Behavior Driven
Development (BDD) styles. Tests are written in a custom, natural English-like language
that can be easily extended in Python, so Robot can, in theory, be used to write any kind of
acceptance tests in a format that can be shared with other stakeholders, pretty much like
what we have seen we can do with pytest-bdd in previous chapters.
The primary difference is that Robot is not based on PyTest, it is a replacement for PyTest,
and is widely used to create end-to-end tests for mobile and web applications. For mobile
applications, the Appium library allows us to write Robot Framework tests that control
mobile applications on a real device, while the Selenium library provides a complete
integration with web browsers, which means that the Robot Framework allows us to write
tests that drive a real web browser and verify the results.
Robot Framework tests are written inside .robot files, which are then divided into
multiple sections by the section headers. The most frequently used section headers are the
following:
*** Settings ***: This contains options to configure Robot itself.
*** Variables ***: This contains variables to reuse across multiple tests.


