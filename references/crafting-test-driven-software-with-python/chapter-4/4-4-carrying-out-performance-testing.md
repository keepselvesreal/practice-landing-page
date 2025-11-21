# 4.4 Carrying out performance testing (pp.128-131)

---
**Page 128**

Scaling the Test Suite
Chapter 4
[ 128 ]
More advanced testing frameworks frequently support the concept of "tagging" tests, so
that we can run only those tests with a specific set of tags. But with unittest, it's still
possible to build our smoke test suite simply by prefixing test names with the word
smoke so that we can select them.
In this case, we would thus rename test_sending_message as
test_smoke_sending_message to make it part of our smoke tests and we would be able
to run our e2e tests as before, but also benefit from having a smoke test suite to run
beforehand as our e2e tests grow further. So we will first have our smoke test, as follows: 
$ python -m unittest discover -k smoke -v
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.334s
OK
This is then followed by our e2e test:
$ python -m unittest discover -k e2e -v
test_message_exchange (e2e.test_chat.TestChatAcceptance) ... ok
test_smoke_sending_message (e2e.test_chat.TestChatAcceptance) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.957s
OK
As for the commit suite, we were able to rely on the -k option to only execute our smoke
tests or all our e2e tests. Thus, we are able to select which kinds of tests we want to run.
Carrying out performance testing
Even though it's not related to verifying the correctness of software, a performance test
suite is part of the testing strategy for many applications. Usually, they are expected to
assess the performance of the software in terms of how fast it can do its job and how many
concurrent users it can handle.
Due to their nature, performance tests are usually very expensive as they have to repeat an
operation multiple times to get a benchmark that is able to provide a fairly stable report
and absorb outliers that could have taken too long to run just because the system was busy
doing something else.


---
**Page 129**

Scaling the Test Suite
Chapter 4
[ 129 ]
For this reason, the performance test suite is usually only executed after all other suites are
passed (also, it doesn't make much sense to assess how fast it can test the software when we
haven't checked that it actually does the right thing).
For our chat example, we could write a benchmark suite that verifies how many messages
per second we are able to handle:
To begin with, we don't want to put that into the middle of all the other tests, so
1.
we are going to put our benchmarks into a benchmarks directory, separate from
the tests directory:
.
├── benchmarks
│   ├── __init__.py
│   └── test_chat.py
├── src
│   ├── chat
│   └── setup.py
└── tests
    ├── __init__.py
    ├── e2e
    ├── functional
    └── unit
test_chat.py can then contain the benchmarks we care about. In this case, we
2.
are going to create a benchmark to report how long it takes to send 10 messages:
import unittest
import timeit
from chat.client import ChatClient
from chat.server import new_chat_server
class BenchmarkMixin:
    def bench(self, f, number):
        t = timeit.timeit(f, number=number)
        print(f"\n\ttime: {t:.2f}, iteration: {t/number:.2f}")
class BenchmarkChat(unittest.TestCase, BenchmarkMixin):
    def test_sending_messages(self):
        with new_chat_server() as srv:
            user1 = ChatClient("User1")
            self.bench(lambda: user1.send_message("Hello World"),
                       number=10)


---
**Page 130**

Scaling the Test Suite
Chapter 4
[ 130 ]
BenchmarkMixin is a utility class that is going to provide the self.bench
method we can use to report the execution time of our benchmarks. The real
benchmark is provided by BenchmarkChat.test_sending_message, which is
going to connect a client to a server and then repeat the user.send_message
call 10 times.
Then we can run our benchmarks, pointing unittest to the benchmarks
3.
directory:
$ python -m unittest discover benchmarks -v
test_sending_messages (test_chat.BenchmarkChat) ...
        time: 2.31, iteration: 0.23
ok
-------------------------------------------------------------------
---
Ran 1 test in 2.406s
If we want to only run our tests instead, we could point the unittest module to
4.
the tests directory:
$ python -m unittest discover tests
..........
-------------------------------------------------------------------
---
Ran 10 tests in 1.013s
Running just python -m unittest discover will run both the benchmarks and tests, so
make sure you point the discover process to the right directory when running your tests.
An alternative is to name your benchmark files with a different prefix (bench_*.py instead
of tests_*.py) and then use the -p option to specify the custom prefix when running
your benchmarks. But in that case, it might not be immediately obvious how to run
benchmarks for a new contributor to your project.
Our chat test suite is now fairly complete: it has e2e tests, functional tests, unit tests, smoke
tests, and benchmarks. But we still have to remember to manually run all tests every time
we do a change. Let's look at how we can tackle this. 


---
**Page 131**

Scaling the Test Suite
Chapter 4
[ 131 ]
Enabling continuous integration
Wouldn't it be convenient if someone else was in charge of running all our tests every time
we made a change to our code base? This would mean that we couldn't forget to run some
specific tests just because they were related to an area of the code that we were not directly
touching.
That's exactly the goal of Continuous Integration (CI) environments. Every time we push
our changes to the code repository, these environments will notice and rerun the tests,
usually merging our changes with the changes from our colleagues to make sure they cope
well together.
If you have a code repository on GitHub, using Travis as your CI is a fairly straightforward
process. Suppose that I made an amol-/travistest GitHub project where I pushed the
code base of our chat application; to enable Travis, the first thing that I have to do is to go
to https:/​/​travis-​ci.​com/​ and log in with my GitHub credentials:
Figure 4.1 – Travis CI Sign in page


