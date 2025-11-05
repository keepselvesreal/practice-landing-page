# 4.3.1 Compile suite (pp.125-126)

---
**Page 125**

Scaling the Test Suite
Chapter 4
[ 125 ]
Organizing the tests into the proper buckets is important to make sure our test suite is still
able to run in a timeframe that can be helpful. If the test suite becomes too slow, we are just
going to stop relying on it as working with it will become a frustrating experience.
That's why it's important to think about how to organize the test suite for your projects and
keep in mind the various kinds of test suites that could exist and their goals.
Working with multiple suites
The separation of tests we did earlier in this chapter helped us realize that there can be
multiple test suites inside our tests directory. 
We can then point the unittest module to some specific directories using the -k option to
run test units on every change, and functional tests when we think we have something that
starts looking like a full feature. Thus, we will rely on e2e tests only when making new
releases or merging pull requests to pass the last checkpoint.
There are a few kinds of test suites that are usually convenient to have in all our projects.
The most common kinds of tests suites you will encounter in projects are likely the compile
suite, commit tests, and smoke tests.
Compile suite
The compile suite is a set of tests that must run very fast. Historically, they were performed
every time the code had to be recompiled. As that was a frequent action, the compile suite
had to be very fast. They were usually static code analysis checks, and while Python doesn't
have a proper compilation phase, it's still a good idea to have a compile suite that we can
maybe run every time we modify a file.
A very good tool in the Python environment to implement those kinds of checks is the
prospector project. Once we install prospector with pip install prospector, we will be
able to check our code for any errors simply by running it inside our project directory:
$ prospector
Check Information
=================
 Started: 2020-06-02 15:22:53.756634
 Finished: 2020-06-02 15:22:55.614589
 Time Taken: 1.86 seconds
 Formatter: grouped


---
**Page 126**

Scaling the Test Suite
Chapter 4
[ 126 ]
 Profiles: default, no_doc_warnings, no_test_warnings, strictness_medium,
strictness_high, strictness_veryhigh, no_member_warnings
 Strictness: None
 Libraries Used:
 Tools Run: dodgy, mccabe, pep8, profile-validator, pyflakes, pylint
 Messages Found: 0
Our project doesn't currently have any errors, but suppose that in
the ChatClient.send_message method in src/chat/client.py, we mistype the
sent_messages variable, prospector would catch the error and notify us that we have a
bug in the code before we can run our full test suite:
$ prospector
Messages
========
src/chat/client.py
  Line: 23
    pylint: Unused variable 'sen_message' (col 8)
  Line: 24
    pylint: Undefined variable 'sent_message' (col 34)
  Line: 25
    pylint: Undefined variable 'sent_message' (col 15)
If your project relies on type hinting, prospector can also integrate mypy to verify the type
correctness of your software before you run the code for real, just to discover it won't work.
Commit tests
As the name suggests, commit tests are tests you run every time you commit a new change.
In our chat example project, the unit and functional tests would be our commit suite. 
But as the project grows further and the functional tests start to get too slow, it's not
uncommon to see the functional tests become "push tests" that are only run before sharing
the code base with your colleagues, while the commit suite gets reduced to unit tests and
lighter forms of integration tests.


