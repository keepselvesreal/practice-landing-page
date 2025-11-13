# 8.5 Using pytest-testmon to rerun tests on code changes (pp.202-204)

---
**Page 202**

PyTest Essential Plugins
Chapter 8
[ 202 ]
Some people prefer to skip the tests that they quarantine, but (while being more robust than
marking them as flaky) this means that you are willing to live with the risk of introducing
any bugs those tests were meant to catch. So, flaky is usually a safer solution and the
important part is to have some dedicated time to go back to those quarantined tests to fix
them.
Using pytest-testmon to rerun tests on code
changes
In a fairly big project, rerunning the whole test suite can take a while, so it's not always
feasible to rerun all tests on every code change. We might settle for rerunning all tests only
when we commit a stable point of the code and run just a subset of them on every code
change before we decide whether to commit our changes.
This approach is usually naturally moved forward by developers who tend to pick a single
test, a test case, or a subset of tests that can act as canaries for their code changes.
For example, if I'm modifying the persistence layer of our contacts application, I would
probably rerun all tests that involve the save or load keywords:
$ pytest -k save -k load --ignore benchmarks -v
...
tests/functional/test_basic.py::TestStorage::test_reload PASSED [ 50%]
tests/unit/test_persistence.py::TestLoading::test_load PASSED [100%]
Once those canary tests pass, I would rerun the whole test suite to confirm that I actually
haven't broken anything and I can commit the relevant code. If there are issues, I would
obviously catch them when I run the full test suite, but on a fairly big project that can take
tens of minutes, it's not a convenient way to catch errors, and the earlier I'm able to catch
any errors, the faster I'll be at releasing my code as I don't have to wait for the full test suite
to run on every change.
In our case, would just rerunning the tests that have the load and save keyword in them
be enough to catch all possible issues and thus require us to rerun the whole test suite only
once as we are very confident that it will pass?
Probably not. There are quite a few more tests that invoke the persistence layer and don't
have those keywords in their name. Also, we might not always be so lucky as to have a set
of keywords we can use to pick a set of canary tests for every change we do. That's where
pytest-testmon comes in handy.


---
**Page 203**

PyTest Essential Plugins
Chapter 8
[ 203 ]
pytest-testmon will build a graph of relationships between all our code functions and
then, on subsequent runs, we can tell testmon to only run the tests that are influenced by
the code we change.
Ensure testmon is installed, as follows:
$ pip install pytest-testmon
We can do the first run of our test suite to build the relationship graph between the code
and tests:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 25 items
...
================== 25 passed in 2.67s ===================
Then, we can change any function of our persistence layer (for example, let's just add
return None at the end of the Application.save function), as follows:
    def save(self):
        with open("./contacts.json", "w+") as f:
            json.dump({"_contacts": self._contacts}, f)
        return None
And then we can rerun all the tests that are somehow related to saving data by rerunning
testmon again:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 16 items / 14 deselected / 2 selected
tests/unit/test_persistence.py . [ 9%]
tests/unit/test_adding.py ... [ 36%]
tests/acceptance/test_adding.py .. [ 54%]
tests/functional/test_basic.py .. [ 72%]
tests/acceptance/test_list_contacts.py . [ 81%]
tests/acceptance/test_delete_contact.py . [ 90%]
tests/acceptance/test_list_contacts.py . [100%]
=========== 11 passed, 14 deselected in 1.30s ============


---
**Page 204**

PyTest Essential Plugins
Chapter 8
[ 204 ]
In this second run, you can see that instead of running all 25 tests that we had, testmon
only picked 11 of them, those that somehow invoked the Application.save method
directly or indirectly, in other words, those that might end up being broken by a change to
the method.
Every time we rerun pytest with the --testmon option, only the tests related to the code
that we have changed will be rerun. If we try to run pytest --testmon again, for
example, no tests would be run as we haven't changed anything from the previous run:
$ pytest --testmon --ignore=benchmarks
================== test session starts ===================
...
testmon: new DB, environment: default
...
collected 0 items / 25 deselected
================= 25 deselected in 0.14s ==================
This is a convenient way to pick only those tests that are related to our recent code changes
and to verify our code on every code change without having to rerun the entire test suite or
guess which tests might need to be checked again.
It should be remembered, by the way, that if the behavior of the code
depends on configuration files or data saved on disk or on a database,
then testmon can't detect that tests have to be rerun to verify the behavior
again when those change. In general, by the way, having your test suite
depend on the state of external components is not a robust approach, so
it's better to make sure that your fixtures take care of setting up a fresh
state on every run.
Running tests in parallel with pytest-xdist
As your test suite gets bigger and bigger, it might start taking too long to run. Even if
strategies to reduce the number of times you need to run the whole test suite are in place,
there will be a time where you want all your tests to run and act as the gatekeeper of your
releases.
Hence, a slow test suite can actually impair the speed at which we are able to develop and
release software.


