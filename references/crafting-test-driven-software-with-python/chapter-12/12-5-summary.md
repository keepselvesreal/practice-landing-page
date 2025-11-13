# 12.5 Summary (pp.305-313)

---
**Page 305**

End-to-End Testing with the Robot Framework
Chapter 12
[ 305 ]
By default, a new library object is created for every test, so a new instance of our
HelloLibrary class would be made on every test. In case we needed to share a single
object across all tests, we could set the HelloLibrary.ROBOT_LIBRARY_SCOPE =
"SUITE" class attribute, which would signal to Robot to create only once instance and share
it across all tests of the same suite. Furthermore, we could set that attribute
to ROBOT_LIBRARY_SCOPE = "GLOBAL" and make the instance unique for the whole test
run. This allows us to share the internal state of our library object across multiple tests in
case we need to preserve any information.
Summary
In this chapter, we saw how we can go further and not only test the responses that our web
applications provide, but also that those responses work for real once they are handled by a
web browser.
Now that we have covered Robot, we have all the tools we need to test our web
applications across all stack levels. We know how to use PyTest for building block unit
tests, WebTest for functional and integration tests, and Robot for end-to-end tests involving
real browsers. So we are now able to write fully tested web applications, paired with the
best practices for TDD and ATDD, which we learned in earlier chapters, and we should be
able to build a solid development routine that allows us to create robust web applications
that are also safe to evolve and refactor over time.


---
**Page 306**

 
Packt.com
Subscribe to our online digital library for full access to over 7,000 books and videos, as well
as industry leading tools to help you plan your personal development and advance your
career. For more information, please visit our website.
Why subscribe?
Spend less time learning and more time coding with practical eBooks and Videos
from over 4,000 industry professionals
Improve your learning with Skill Plans built especially for you
Get a free eBook or video every month
Fully searchable for easy access to vital information
Copy and paste, print, and bookmark content
Did you know that Packt offers eBook versions of every book published, with PDF and
ePub files available? You can upgrade to the eBook version at www.packt.com and as a print
book customer, you are entitled to a discount on the eBook copy. Get in touch with us
at customercare@packtpub.com for more details.
At www.packt.com, you can also read a collection of free technical articles, sign up for a
range of free newsletters, and receive exclusive discounts and offers on Packt books and
eBooks. 


---
**Page 307**

Other Books You May Enjoy
If you enjoyed this book, you may be interested in these other books by Packt:
Django 3 By Example - Third Edition
Antonio Melé
ISBN: 978-1-83898-195-2
Build real-world web applications
Learn Django essentials, including models, views, ORM, templates, URLs, forms,
and authentication
Implement advanced features such as custom model fields, custom template tags,
cache, middleware, localization, and more
Create complex functionalities, such as AJAX interactions, social authentication, a
full-text search engine, a payment system, a CMS, a RESTful API, and more
Integrate other technologies, including Redis, Celery, RabbitMQ, PostgreSQL,
and Channels, into your projects
Deploy Django projects in production using NGINX, uWSGI, and Daphne


---
**Page 308**

Other Books You May Enjoy
[ 308 ]
40 Algorithms Every Programmer Should Know
Imran Ahmad
ISBN: 978-1-78980-121-7
Explore existing data structures and algorithms found in Python libraries
Implement graph algorithms for fraud detection using network analysis
Work with machine learning algorithms to cluster similar tweets and process
Twitter data in real time
Predict the weather using supervised learning algorithms
Use neural networks for object detection
Create a recommendation engine that suggests relevant movies to subscribers
Implement foolproof security using symmetric and asymmetric encryption on
Google Cloud Platform (GCP)


---
**Page 309**

Other Books You May Enjoy
[ 309 ]
Packt is searching for authors like you
If you're interested in becoming an author for Packt, please
visit authors.packtpub.com and apply today. We have worked with thousands of
developers and tech professionals, just like you, to help them share their insight with the
global tech community. You can make a general application, apply for a specific hot topic
that we are recruiting an author for, or submit your own idea.
Leave a review - let other readers know what
you think
Please share your thoughts on this book with others by leaving a review on the site that you
bought it from. If you purchased the book from Amazon, please leave us an honest review
on this book's Amazon page. This is vital so that other potential readers can see and use
your unbiased opinion to make purchasing decisions, we can understand what our
customers think about our products, and our authors can see your feedback on the title that
they have worked with Packt to create. It will only take a few minutes of your time, but is
valuable to other potential customers, our authors, and Packt. Thank you!


---
**Page 310**

Index
A
Acceptance Test-Driven Development (ATDD)  82
acceptance tests
   about  25
   passing  169, 170, 172
   writing  165, 166
Act phase  15
And step
   used, for creating setup  175
Arrange phase  15
Arrange, Act, Assert pattern  15
Assert phase  15
authentication  22
authorization  22
automatic tests  9, 11
B
Behavior-Driven Development (BDD)
   about  172
   actions, performing with When step  176
   conditions, assessing with Then step  177
   feature file, defining  173
   scenario test, running  175
   scenario, declaring  174
   scenario, making to pass  178, 180
   setup, creating with And step  176
   using  172
behaviors
   checking, with spies  44, 45, 46, 47, 48, 49
benchmark runs
   comparing  198
black-box tests  25
C
capsys
   IO, testing with  149
chat application
   acceptance tests  56, 57, 59
   doubles  56, 57, 59
   working, with TDD  33, 35, 36, 37, 38
code-based reference
   adding  223, 225
commit tests  126
compile suite  125
component tests  21, 25
components
   replacing, with stubs  40, 41, 42, 43, 44
construction injection  60
continuous integration (CI)
   about  131
   enabling  131, 132, 133, 134, 135
   performance tests, running in cloud  136
contract tests  25
coverage reporting
   pytest-cov, using for  189, 192, 193
coverage
   testing  29
   using, as service  194, 195
D
dependencies
   managing, with dependency injection  60, 63
   replacing, with fakes  51, 52, 53, 54, 55
dependency injection frameworks
   using  63, 65, 66
dependency injection
   dependencies, managing with  60, 63
distribution
   testing  29
Django projects
   testing, with Django's test client  277, 279
   testing, with pytest  274, 276
Django tests


---
**Page 311**

[ 311 ]
   writing, with Django's test client  271, 272, 273
Django's test client
   Django tests, writing with  271, 272, 273
   used, for testing Django projects  277, 279
documentation
   code-based reference, adding  223, 225
   testing  221, 222
   verified user guide, writing  226, 229, 231
dummy objects
   using  38, 39, 40
E
End-to-End tests
   about  25, 26
   moving, to functional tests  122, 123, 124
environments
   about  211
   using, for multiple Python versions  213, 215
F
fakes
   dependencies, replacing with  51, 52, 53, 54, 55
fixtures
   generating  156, 157, 158, 159, 160
flaky
   using, to rerun unstable tests  199, 202
functional tests
   about  21, 25, 120
   End-to-End tests, moving to  122, 123, 124
G
Gherkin  172
H
HTTP clients
   testing  247, 251
HTTP
   testing  243, 246
hypothesis  232
I
injector  60
Input/Output (I/O) queues  75
integration tests  22, 24, 26
IO
   testing, with capsys  149
M
mocks
   using  49, 50, 51
multiple test cases
   writing  11, 13
multiple test suite
   working with  125
N
narrow integration tests  122
P
parametric tests
   tests, generating with  160, 161, 162
PEP 333
   reference link  252
performance testing
   about  128, 129, 130
   in cloud  136
   strategies  136
product team
   feedback, obtaining  167, 168
property-based testing  231, 235, 237
PyTest 6  213
PyTest fixtures
   using, for dependency injection  146, 147
   writing  142, 143, 144, 145
pytest-benchmark
   used, for benchmarking  196, 198
pytest-cov
   used, for coverage reporting  189, 192, 193
pytest-testmon
   using, to rerun tests on code changes  202, 204
pytest-xdist
   used, for running tests in parallel  204
PyTest
   unittest, running with  139, 140, 141
   used, for testing Django projects  274, 276
Python 2.7  211
Python 3.7  211
Python 3.8  213
Python versions


---
**Page 312**

[ 312 ]
   testing, with Tox  211, 213
Q
quality control  7
R
Read-Eval-Print Loop (REPL)  69
regression test  105
regression
   preventing  105, 106, 107, 108, 110, 111, 112
reStructuredText format  221
Robot framework
   about  282, 283, 284, 285, 286
   custom keywords, adding  301
   extending  300
   extending, from Python  302, 303, 304, 305
   section headers  282
S
Selenium library
   reference link  286
smoke tests  127, 128
sociable unit  21
software testing  7
solitary unit  21
specifications
   embracing, by example  180, 185, 186
spies
   behaviors, checking with  44, 45, 46, 47, 48, 49
stubs
   components, replacing with  40, 41, 42, 43, 44
subsets of test suite
   running  150, 151
system tests  25
T
test case  9
test cases, test plans
   postconditions  8
   preconditions  8
   steps  8
test doubles  32, 33
test plans  8, 9
test runner  10
test suite, types
   commit tests  126
   compile suite  125
   smoke tests  127, 128
test suite
   about  9, 11
   configuring  153, 154, 155
   End-to-End tests, moving to functional tests  122,
123, 124
   scaling  115, 116, 117, 118, 119, 120, 121, 122
test units  19, 21
Test-Driven Development (TDD)
   about  68, 69, 70, 72, 73, 74, 75, 77, 78, 79,
80, 82, 116
   application, building  3, 83, 84, 85, 86, 87, 88,
89, 90, 91, 93, 94, 95, 96, 97, 98, 100, 101,
102, 103, 104
   chat application, working with  33, 35, 36, 37, 38
test-driven development
   about  15
   implementing  16, 18, 19
test-first approach  18
testing pyramid  27, 28
testing trophy  28, 29
tests
   generating, for common properties  237, 239
   generating, with parametric tests  160, 161, 162
   organizing  13, 15
Then step
   used, for assessing conditions  177
tmp_path
   temporary data, managing with  148
Tox
   about  208, 210
   used, for testing multiple Python versions  211,
213
   using, with Travis  215, 218, 219
Travis application
   reference link  133
Travis
   Tox, using with  215, 217, 219
U
unit tests  15, 26
unittest discovery mode  14


---
**Page 313**

unittest module
   about  10
   running, with PyTest  139, 140, 141
unstable tests
   rerunning, with flaky  199, 202
V
verified user guide
   writing  226, 229, 231
W
web browsers
   testing  297, 298, 299, 300
   testing with  286, 287, 288, 290, 291
   testing, with headless browsers  295, 296
   tests execution, recording  291, 292, 294
Web Server Gateway Interface (WSGI)
   testing, with WebTest  252, 255, 260
WebTest
   using, with web frameworks  261, 262, 265, 269
   WSGI, testing with  252, 255, 259, 261
When step
   used, for performing actions  176


