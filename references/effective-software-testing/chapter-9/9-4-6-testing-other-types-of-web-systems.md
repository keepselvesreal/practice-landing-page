# 9.4.6 Testing other types of web systems (pp.256-256)

---
**Page 256**

256
CHAPTER 9
Writing larger tests
infrastructure should help developers set up the environment, clean up the environ-
ment, retrieve complex data, assert complex data, and perform whatever other com-
plex tasks are required to write tests. 
9.4.5
DSLs and tools for stakeholders to write tests
In this chapter, we wrote the system tests ourselves with lots of Java code. At this level,
it is also common to see more automation. Some tools, such as the Robot framework
(https://robotframework.org) and Cucumber (https://cucumber.io), even allow you
to write tests in language that is almost completely natural. These tools make a lot of
sense if you want others to write tests, too, such as (non-technical) stakeholders. 
9.4.6
Testing other types of web systems
The higher we go in levels of testing, such as web testing, the more we start to think
about the frameworks and environment our application runs in. Our web application
is responsive; how do we test for that? If we use Angular or React, how do we test it?
Or, if we use a non-relational database like Mongo, how do we test it?
 Testing these specific technologies is far beyond the scope of this book. My sugges-
tion is that you visit those communities and explore their state-of-the-art tools and
bodies of knowledge. All the test case engineering techniques you learn in this book
will apply to your software, regardless of the technology.
SYSTEM TESTS IN SOFTWARE OTHER THAN WEB APPLICATIONS
I used web applications to exemplify system tests because I have a lot of experience
with them. But the idea of system testing can be applied to any type of software you
develop. If your software is a library or framework, your system tests will exercise the
entire library as the clients would. If your software is a mobile application, your system
tests will exercise the mobile app as the clients would.
 The best practices I discussed still apply. Engineering system tests will be harder
than engineering unit tests, and you may need some infrastructure code (like the POs
we created) to make you more productive. There are probably also specific best prac-
tices for your type of software—be sure to do some research. 
Exercises
9.1
Which of the following recommendations should you follow to keep a web
application testable? Select all that apply.
A Use TypeScript instead of JavaScript.
B Make sure the HTML elements can be found easily from the tests.
C Make sure requests to web servers are performed asynchronously.
D Avoid inline JavaScript in an HTML page.
9.2
Which of the following statements is true about end-to-end/system testing?
A End-to-end testing cannot be automated for web applications and there-
fore has to be performed manually.


