# 9.4 Using Tox with Travis (pp.215-219)

---
**Page 215**

Managing Test Environments with Tox
Chapter 9
[ 215 ]
benchmarks/test_persistence.py .                       [100%]
-------------------------- benchmark: 1 tests --------------------------
Name (time in us) Min Max Mean ... OPS (Kops/s) Rounds
------------------------------------------------------------------------
test_loading 714.7 22,312.3 950.7 ... 1.0518 877
------------------------------------------------------------------------
======================= 1 passed in 1.73s  =======================
We now have a configuration where running tox by default will run our tests on Python
2.7 and Python 3.7, and then running tox -e benchmarks does run benchmarks.
If we further want to specialize the behavior of our Tox configuration, we can do so by
adding more environments and customizing the options we care about. A complete
reference of all the Tox options is available on the ReadTheDocs page of Tox, so make sure
to take a look if you want to dive further into customizing Tox behavior.
Now that we have Tox working locally, we need to combine it with our CI system to ensure
that different CI processes are started for each Tox environment. As we have used Travis
for all our CI needs so far, let's see how we can integrate Tox with Travis.
Using Tox with Travis
Using Tox with a CI environment is usually fairly simple, but as both Tox and the CI will
probably end up wanting to manage the Python environment, some attention has to be
paid to enable them to exist together. To see how Travis and Tox can work together, we can
pick our chat project that we wrote in Chapter 4, Scaling the Test Suite, which we already
had on Travis-CI, and migrate it to use Tox.
We need to write a tox.ini file, which will take care of running the test suite itself:
[tox]
setupdir = ./src
envlist = py37, py38, py39
[testenv]
usedevelop = true
deps =
    coverage
commands =
    coverage run --source=src -m unittest discover tests -v
    coverage report


---
**Page 216**

Managing Test Environments with Tox
Chapter 9
[ 216 ]
[testenv:benchmarks]
commands =
    python -m unittest discover benchmarks
The commands you see in tox.ini are the same that we previously had in the
travis.yml file under the script: section. That's because, previously, Travis itself was in
charge of running our tests. Now, Tox will be in charge of doing so.
For the same reason, as the coverage reporting should happen every time we run the test
suite, we have Tox install the coverage dependency and run coverage report after the
test suite.
The main difference with tox.ini seen previously in the chapter is probably the
usedevelop = true option. That tells Tox to install our own project in editable mode
(sometimes called developer mode). Instead of making a distribution package out of our
source directory and then installing the distribution, Tox will install the source directory
itself. This is frequently convenient when coverage reporting is involved as we usually
want the coverage to be against our source code, and not against the installed distribution.
The benefit of using a Tox file is that it should work the same everywhere. So, before
moving it to Travis, we can verify that it actually does what we expect locally on our own
machine:
$ tox
py38 develop-inst-noop: travistest/src
py38 run-test: commands[0] | coverage run --source=src -m unittest discover
tests -v
test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
test_exchange_with_server (functional.test_chat.TestChatMessageExchange)
... ok
test_many_users (functional.test_chat.TestChatMessageExchange) ... ok
test_multiple_readers (functional.test_chat.TestChatMessageExchange) ... ok
test_client_connection (unit.test_client.TestChatClient) ... ok
test_client_fetch_messages (unit.test_client.TestChatClient) ... ok
test_nickname (unit.test_client.TestChatClient) ... ok
test_send_message (unit.test_client.TestChatClient) ... ok
test_broadcast (unit.test_connection.TestConnection) ... ok
----------------------------------------------------------------------
Ran 10 tests in 0.058s
OK
py38 run-test: commands[1] | coverage report
Name Stmts Miss Cover
------------------------------------------


---
**Page 217**

Managing Test Environments with Tox
Chapter 9
[ 217 ]
src/chat/__init__.py  0 0 100%
src/chat/client.py   29 0 100%
src/chat/server.py    7 0 100%
src/setup.py          2 2 0%
------------------------------------------
TOTAL                38 2 95%
As desired, it ran the test suite and then reported the code coverage. We also know, thanks
to [testenv:benchmarks], that if we want, we can run benchmarks with tox -e
benchmarks:
$ tox -e benchmarks
benchmarks develop-inst-noop: travistest/src
benchmarks run-test: commands[0] | python -m unittest discover benchmarks
  time: 0.06, iteration: 0.01
.
----------------------------------------------------------------------
Ran 1 test in 0.069s
OK
Now, the remaining element is to make Tox run inside Travis.
To do so, mostly we have to replace the script: section in our travis.yml file with a
single tox command. Then, Tox will do everything it has to do in order to make the tests
run as it did on our own PC:
script:
  - "tox"
However, Travis will also need Tox itself to run the commands. Therefore, we want to have
Travis install Tox before running the script. To do so, we are going to use a special package
named tox-travis and we are going to add it to the install: section:
install:
  - "pip install tox-travis"
You might be wondering why we used tox-travis instead of just tox. The reason is that
tox-travis takes care of that little extra work that is necessary to make Tox and Travis
collaborate. By default, Travis wants to install and set up Python, but Tox also wants to do
the same. That means that we would end up installing Python twice.


---
**Page 218**

Managing Test Environments with Tox
Chapter 9
[ 218 ]
Even worse, as we have envlist = py37, py38, py39 in our tox.ini, Tox would
actually try to run the tests against all three Python versions for each Travis Python
environment. So, suppose that we asked Travis to set up 3.7, 3.8, and 3.9. Then, Tox would
try to use 3.7, 3.8, and 3.9 inside the Travis 3.7 Python environment, and would then try to
use 3.7, 3.8, and 3.9 inside the Travis 3.8 Python environment, and so on, leading to errors
such as the following:
ERROR: py38: InterpreterNotFound: python3.8
ERROR: py39: InterpreterNotFound: python3.9
To avoid this problem, we can use tox-travis. When we use Tox-Travis, the Python
environments come from Travis only and Tox will simply use those already prepared by
Travis without trying to set up a second Python environment. At that point, our Tox
envlist is only helpful locally, and on Travis, the python: section of the travis.yml file
will dictate which Python versions get used.
Apart from making sure that we install tox-travis, the rest of our travis.yml file is
fairly similar to the original one our project had previously. We just replaced the
commands to run tests and benchmarks with those that Tox provides:
language: python
os: linux
dist: xenial
python:
  - 3.7
  - &mainstream_python 3.8
  - 3.9
  - nightly
install:
  - "pip install tox-travis"
  - "pip install coveralls"
script:
  - "tox"
after_success:
  - coveralls
  - "tox -e benchmarks"
Now that both our tox.ini and travis.yml configuration files are in place, we can just
push our repository changes and see that Travis successfully runs our tests using Tox:


---
**Page 219**

Managing Test Environments with Tox
Chapter 9
[ 219 ]
Figure 9.1 – Tox setup
It should became clear that once we have a working local Tox setup, moving on to Travis
involves very little apart from writing a travis.yml configuration file in charge of
installing tox-travis and then invoking tox.
Summary
In this chapter, we saw how Tox can take care of all the setup necessary to run our tests for
us and how it can do that on multiple target environments so that all we have to do to run
tests is just to invoke Tox itself.
This is a more convenient, but also robust, way to manage our test suite. The primary
benefit is that anyone else willing to contribute to our project won't have to learn how to set
up our projects and how to run tests. If our colleagues or project contributors are familiar
with Tox, seeing that our project includes a tox.ini file tells them all that they will need to
know—that they just have to invoke the tox command to run tests.
Now that we have seen the base plugins and tools to manage and run our test suite, in the
next chapter, we can move on to some more advanced topics that involve how to test our
documentation itself and how to use property-based testing to catch bugs in our code.


