# Chapter 1: Getting Started with Software Testing (pp.6-31)

---
**Page 6**

1
Getting Started with Software
Testing
Many think that the big step from "coding" to "software engineering" is made by having
elegant architectures, well-defined execution plans, and software that moves big
companies' processes. This mostly comes from our vision of the classic industrial product
development world, where planning mostly mattered more than execution, because the
execution was moved forward by an assembly line and software was an expensive internal
utility that only big companies could afford
As software development science moved forward and matured, it became clear that classic
industrial best practices weren't always a great fit for it. The reason being that every
software product was very different, due to the technologies involved, the speed at which
those technologies evolve, and in the end the fact that different software had to do totally
different things. Thus the idea developed that software development was more similar to
craftsmanship than to industry.
If you embrace that it's very hard, and not very effective, to try to eliminate uncertainty and
issues with tons of preparation work due to the very nature of software itself, it becomes
evident that the most important part of software development is detecting defects and
ensuring it achieves the expected goals. Those two things are usually mostly done by
having tests and a fitness function that can verify the software does what we really mean it
to – founding pieces of the whole Software Quality Control discipline, which is what this
chapter will introduce and, in practice, what this book is all about.
In this chapter, we will go through testing software products and the best practices in
quality control. We will also introduce automatic tests and how they are superseding
manual testing. We will take a look at what Test-Driven Development (TDD) is and how
to apply it in Python, giving some guidance on how to distinguish between the various
categories of tests, how to implement them, and how to get the right balance between test
efficacy and test cost.


---
**Page 7**

Getting Started with Software Testing
Chapter 1
[ 7 ]
In this chapter, we will cover the following:
Introducing software testing and quality control
Introducing automatic tests and test suites
Introducing test-driven development and unit tests
Understanding integration and functional tests
Understanding the testing pyramid and trophy
Technical requirements
A working Python interpreter is all that's needed.
The examples have been written in Python 3.7 but should work in most modern Python
versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter01.
Introducing software testing and quality
control
From the early days, it was clear that like any other machine, software needed a way to 
verify it was working properly and was built with no defects.
Software development processes have been heavily inspired by manufacturing industry
standards, and early on, testing and quality control were introduced into the product
development life cycle. So software companies frequently have a quality assurance team
that focuses on setting up processes to guarantee robust software and track results.
Those processes usually include a quality control process where the quality of the built
artifact is assessed before it can be considered ready for users.
The quality control process usually achieves such confidence through the execution of a test
plan. This is usually a checklist that a dedicated team goes through during the various
phases of production to ensure the software behaves as expected.


---
**Page 8**

Getting Started with Software Testing
Chapter 1
[ 8 ]
Test plans
A test plan is composed of multiple test cases, each specifying the following:
Preconditions: What's necessary to be able to verify the case
Steps: Actions that have to succeed when executed in the specified order
Postconditions: In which state the system is expected to be at the end of the steps
A sample test case of software where logging in with a username and password is
involved, and we might want to allow the user to reset those, might look like the following
table:
Test Case: 2.2 - Change User Password
Preconditions:
• A user, user1 exists
• The user is logged in as user1
• The user is at the main menu
# Action
Expected Response
Success /
Fail
1 Click the change password button. The system shows a dialog to insert a new password.
2 Enter newpass.
The dialog shows 7 asterisks in the password field.
3 Click the OK button.
The system shows a dialog with a success message.
4 Wait 2 seconds.
The success dialog goes away.
Postconditions:
• The user1 password is now newpass
These test cases are divided into cases, are manually verified by a dedicated team, and a
sample of them is usually selected to be executed during development, but most of them
are checked when the development team declared the work done.
This meant that once the team finishes its work, it takes days/weeks for the release to
happen, as the whole software has to be verified by humans clicking buttons, with all the
unpredictable results that involves, as humans can get distracted, pressing the wrong
button or receiving phone calls in the middle of a test case.
As software usage became more widespread, and business-to-consumer products became
the norm, consumers started to appreciate faster release cycles. Companies that updated
their products with new features frequently were those that ended up dominating the
market in the long term.


---
**Page 9**

Getting Started with Software Testing
Chapter 1
[ 9 ]
If you think about modern release cycles, we are now used to getting a new version of our
favorite mobile application weekly. Such applications are probably so complex that they
involve thousands of test cases. If all those cases had to be performed by a human, there
would be no way for the company to provide you with frequent releases.
The worst thing you can do, by the way, is to release a broken product. Your users will lose
confidence and will switch to other more reliable competitors if they can't get their job done
due to crashes or bugs. So how can we deliver such frequent releases without reducing our
test coverage and thus incurring more bugs?
The solution came from automating the test process. So while we learned how to detect
defects by writing and executing test plans, it's only by making them automatic that we can
scale them to the number of cases that will ensure robust software in the long term.
Instead of having humans test software, have some other software test it. What a person
does in seconds can happen in milliseconds with software and you can run thousands of
tests in a few minutes.
Introducing automatic tests and test suites
Automated testing is, in practice, the art of writing another piece of software to test an
original piece of software.
As testing a whole piece of software has to take millions of variables and possible code
paths into account, a single program trying to test another one would be very complex and
hard to maintain. For this reason, it's usually convenient to split that program into smaller
isolated programs, each being a test case.
Each test case contains all the instructions that are required to set up the target software in a
state where the parts that are the test case areas of interest can be tested, the tests can be
done, and all the conditions can be verified and reset back to the state of the target software
so a subsequent test case can find a known state from which to start.
When using the unittest module that comes with the Python Standard Library, each test
case is declared by subclassing from the unittest.TestCase class and adding a method
whose name starts with test, which will contain the test itself:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass


---
**Page 10**

Getting Started with Software Testing
Chapter 1
[ 10 ]
Trying to run our previous test will do nothing by the way:
$ python 01_automatictests.py
$
We declared our test case, but we have nothing that runs it.
As for manually executed tests, the automatic tests need someone in charge of gathering all
test cases and running them all. That's the role of a test runner.
Test runners usually involve a discovery phase (during which they detect all test cases) and
a run phase (during which they run the discovered tests).
The unittest module provides all the components necessary to build a test runner that does
both the discovery and execution of tests. For convenience, it even provides the
unittest.main() method, which configures a test runner that, by default, will run the
tests in the current module:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
if __name__ == '__main__':
    unittest.main()
By adding a call to unittest.main() at the end of our tests, Python will automatically
execute our tests when the module is invoked:
$ python 01_automatictests.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
We can confirm that the test we cared about was executed by using the -v option to print a
more verbose output:
$ python 01_automatictests.py -v
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK


---
**Page 11**

Getting Started with Software Testing
Chapter 1
[ 11 ]
During the discovery phase, unittest.main will look for all classes that inherit from
unittest.TestCase within the module that is recognized as the main Python module
(sys.modules['__main__']), and all those subclasses will be registered as test cases for
the runner.
Individual tests are then defined by having methods with names starting with test in the
test case classes. This means that if we add more methods with names that don't start with
test, they won't be treated as tests:
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
    def notatest(self):
        pass
Trying to start the test runner again will continue to run only the test_one test:
$ python 01_automatictests.py -v
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
In the previous example, only the test_one method was executed as a test, while
notatest was recognized as not being a test but instead as a method that we are going to
use ourselves in tests.
Being able to distinguish between tests (methods whose names start with test_) and other 
methods allows us to create helpers and utility methods within our test cases that the
individual tests can reuse.
Given that a test suite is a collection of multiple test cases, to grow our test suite, we need to
be able to actually write more than one single TestCase subclass and run its tests.
Multiple test cases
We already know that unittest.main is the function in charge of executing our test suite,
but how can we make it execute more than one TestCase?


---
**Page 12**

Getting Started with Software Testing
Chapter 1
[ 12 ]
The discovery phase of unittest.main (the phase during which unittest.main decides
which tests to run) looks for all subclasses or unittest.TestCase.
The same way we had MyTestCase tests executed, adding more test cases is as simple as
declaring more classes:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass
    def notatest(self):
        pass
class MySecondTestCase(unittest.TestCase):
    def test_two(self):
        pass
if __name__ == '__main__':
    unittest.main()
Running the 01_automatictests.py module again will lead to both test cases being
verified:
$ python 01_automatictests.py -v
test_two (__main__.MySecondTestCase) ... ok
test_one (__main__.MyTestCase) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.000s
OK
If a test case is particularly complex, it can even be divided into multiple individual tests,
each checking a specific subpart of it:
class MySecondTestCase(unittest.TestCase):
    def test_two(self):
        pass
    def test_two_part2(self):
        pass


---
**Page 13**

Getting Started with Software Testing
Chapter 1
[ 13 ]
This allows us to divide the test cases into smaller pieces and eventually share setup and
teardown code between the individual tests. The individual tests will be executed by the
test runner in alphabetical order, so in this case, test_two will be executed before
test_two_part2:
$ python 01_automatictests.py -v
test_two (__main__.MySecondTestCase) ... ok
test_two_part2 (__main__.MySecondTestCase) ... ok
test_one (__main__.MyTestCase) ... ok
In that run of the tests, we can see that MySecondTestCase was actually executed before
MyTestCase because "MyS" is less than "MyT".
In any case, generally, it's a good idea to consider your tests as being executed in a random
order and to not rely on any specific sequence of execution, because other developers might
add more test cases, add more individual tests to a case, or rename classes, and you want to
allow those changes with no additional issues. Especially since relying on a specific known
execution order of your tests might limit your ability to parallelize your test suite and run
test cases concurrently, which will be required as the size of your test suite grows.
Once more tests are added, adding them all into the same class or file quickly gets
confusing, so it's usually a good idea to start organizing tests.
Organizing tests
If you have more than a few tests, it's generally a good idea to group your test cases into
multiple modules and create a tests directory where you can gather the whole test plan:
├── 02_tests
│   ├── tests_div.py
│   └── tests_sum.py


---
**Page 14**

Getting Started with Software Testing
Chapter 1
[ 14 ]
Those tests can be executed through the unittest discover mode, which will look for all
modules with names matching test*.py within a target directory and will run all the
contained test cases:
$ python -m unittest discover 02_tests -v
test_div0 (tests_div.TestDiv) ... ok
test_div1 (tests_div.TestDiv) ... ok
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok
----------------------------------------------------------------------
Ran 4 tests in 0.000s
OK
You can even pick which tests to run by filtering them with a substring with the -k
parameter; for example, -k sum will only run tests that contain "sum" in their names:
$ python -m unittest discover 02_tests -k sum -v
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.000s
OK
And yes, you can nest tests further as long as you use Python packages:
├── 02_tests
│   ├── tests_div
│   │   ├── __init__.py
│   │   └── tests_div.py
│   └── tests_sum.py
Running tests structured like the previous directory tree will properly navigate into the
subfolders and spot the nested tests.
So running unittest in discovery mode over that direction will properly find the
TestDiv and TestSum classes declared inside the files even when they are nested in
subdirectories:
$ python -m unittest discover 02_tests -v
test_div0 (tests_div.tests_div.TestDiv) ... ok
test_div1 (tests_div.tests_div.TestDiv) ... ok
test_sum0 (tests_sum.TestSum) ... ok
test_sum1 (tests_sum.TestSum) ... ok


---
**Page 15**

Getting Started with Software Testing
Chapter 1
[ 15 ]
----------------------------------------------------------------------
Ran 4 tests in 0.000s
OK
Now that we know how to write tests, run them, and organize multiple tests in a test suite.
We can start introducing the concept of TDD and how unit tests allow us to achieve it.
Introducing test-driven development and
unit tests
Our tests in the previous section were all empty. The purpose was to showcase how a test
suite can be made, executed, and organized in test cases and individual tests, but in the
end, our tests did not test much.
Most individual tests are written following the "Arrange, Act, Assert" pattern:
First, prepare any state you will need to perform the action you want to try.
Then perform that action.
Finally, verify the consequences of the action are those that you expected.
Generally speaking, in most cases, the action you are going to test is "calling a function,"
and for code that doesn't depend on any shared state, the state is usually all contained
within the function arguments, so the Arrange phase might be omitted. Finally, the Assert
phase will verify that the called function did what you expected, which usually means
verifying the returned value and any effect at a distance that function might have:
import unittest
class SomeTestCase(unittest.TestCase):
    def test_something(self):
        # Arrange phase, nothing to prepare here.
        # Act phase, call do_something
        result = do_something()
        # Assert phase, verify do_something did what we expect.
        assert result == "did something"
The test_something test is structured as a typical test with those three phases explicitly
exposed, with the do_something call representing the Act phase and the final assert
statement representing the Assertion phase.


---
**Page 16**

Getting Started with Software Testing
Chapter 1
[ 16 ]
Now that we know how to structure tests properly, we can see how they are helpful in
implementing TDD and how unit tests are usually expressed.
Test-driven development
Tests can do more than just validating our code is doing what we expect. The TDD process
argues that tests are essential in designing code itself.
Writing tests before implementing the code itself forces us to reason about our
requirements. We must explicitly express requirements in a strict, well-defined way –
clearly enough that a computer itself (computers are known for not being very flexible in
understanding things) can understand them and state whether the code you will be writing
next satisfies those requirements.
First, you write a test for your primary scenario—in this case, testing that doing 3+2 does
return 5 as the result:
import unittest
class AdditionTestCase(unittest.TestCase):
    def test_main(self):
        result = addition(3, 2)
        assert result == 5
Then you make sure it fails, which proves you are really testing something:
$ python 03_tdd.py
E
======================================================================
ERROR: test_main (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 5, in test_main
    result = addition(3, 2)
NameError: name 'addition' is not defined
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
Finally, you write the real code that is expected to make the test pass:
def addition(arg1, arg2):
    return arg1 + arg2


---
**Page 17**

Getting Started with Software Testing
Chapter 1
[ 17 ]
And confirm it makes your test pass:
$ python 03_tdd.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
Once the test is done and it passes, we can revise our implementation and refactor the code.
If the test still passes, it means we haven't changed the behavior and we are still doing what
we wanted.
For example, we can change our addition function to unpack arguments instead of having
to specify the two arguments it can receive:
def addition(*args):
    a1, a2 = args
    return a1 + a2
If our test still passes, it means we haven't changed the behavior, and it's still as good as
before from that point of view:
$ python 03_tdd.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
Test-driven development is silent about when you reach a robust code base that satisfies all
your needs. Obviously, you should at least make sure there are enough tests to cover all
your requirements.
But as testing guides us in the process of development, development should guide us in the
process of testing.
Looking at the code helps us come up with more white-box tests; tests that we can think of
because we know how the code works internally. And while those tests might not
guarantee that we are satisfying more requirements, they help us guarantee that our code
is robust in most conditions, including corner cases.


---
**Page 18**

Getting Started with Software Testing
Chapter 1
[ 18 ]
While historically, test-first and test-driven were synonyms, today that's considered the one
major difference with the test-first approach. In TDD we don't have the expectation to be
able to write all tests first. Nor is it generally a good idea in the context of extreme
programming practices, because you still don't know what the resulting interface that you
want to test will be. What you want to test evolves as the code evolves, and we know that
the code will evolve after every passing test, as a passing test gives us a chance for
refactoring.
In our prior example, as we changed our addition function to accept a variable number of
arguments, a reasonable question would be, "But what happens if I pass three arguments? Or
none?" And our requirements, expressed by the tests, as a consequence, have to grow to
support a variable number of arguments:
    def test_threeargs(self):
        result = addition(3, 2, 1)
        assert result == 6
    def test_noargs(self):
        result = addition()
        assert result == 0
So, writing code helped us come up with more tests to verify the conditions that came to
mind when looking at the code like a white box:
$ python 03_tdd.py
.EE
======================================================================
ERROR: test_noargs (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 13, in test_noargs
    result = addition()
  File "03_tdd.py", line 18, in addition
    a1, a2 = args
ValueError: not enough values to unpack (expected 2, got 0)
======================================================================
ERROR: test_threeargs (__main__.AdditionTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "03_tdd.py", line 9, in test_threeargs
    result = addition(3, 2, 1)
  File "03_tdd.py", line 18, in addition
    a1, a2 = args
ValueError: too many values to unpack (expected 2)


---
**Page 19**

Getting Started with Software Testing
Chapter 1
[ 19 ]
----------------------------------------------------------------------
Ran 3 tests in 0.001s
FAILED (errors=2)
And adding those failing tests helps us come up with more, and better, code that now
properly handles the cases where any number of arguments is passed to our addition
function:
def addition(*args):
    total = 0
    for a in args:
        total += a
    return total
Our addition function will now just iterate over the provided arguments, adding them to
the total. Thus if no argument is provided, it will just return 0 because nothing was added
to it.
If we run our test suite again, we will be able to confirm that both our new tests now pass,
and thus we achieved what we wanted to:
$ python 03_tdd.py
...
----------------------------------------------------------------------
Ran 3 test in 0.001s
OK
Writing tests and writing code should interleave continuously. If you find yourself
spending all your time on one or the other, you are probably moving away from the
benefits that TDD can give you, as the two phases are meant to support each other.
There are many kinds of tests you are going to write in your test suite during your
development practice, but the most common one is probably going to be test units.
Test units
The immediate question once we know how to arrange our tests, is usually "what should I
test?". The answer to that is usually "it depends."


---
**Page 20**

Getting Started with Software Testing
Chapter 1
[ 20 ]
You usually want tests that assert that the feature you are providing to your users does
what you expect. But do tests do nothing to guarantee that, internally, the components that
collaborate with that feature behave correctly? The exposed feature might be working as a
very lucky side effect of 200 different bugs in the underlying components.
So it's generally a good idea to test those units individually and verify that they all work as
expected.
What are those units? Well, the answer is "it depends" again.
In most cases, you could discuss that in procedural programming, the units are the
individual functions, while in object-oriented programming, it might be defined as a single
class. But classes, while we usually do our best to try to isolate them to a single
responsibility, might cover multiple different behaviors based on which method you call.
So they actually act as multiple components in our system, and in such cases, they should
be considered as separate units.
In practice, a unit is the smallest testable entity that participates in your software.
If we have a piece of software that does "multiplication," we might implement it as a main
function that fetches the two provided arguments and calls a multiply function to do the
real job:
def main():
    import sys
    num1, num2 = sys.argv[1:]
    num1, num2 = int(num1), int(num2)
    print(multiply(num1, num2))
def multiply(num1, num2):
    total = 0
    for _ in range(num2):
        total = addition(total, num1)
    return total
def addition(*args):
    total = 0
    for a in args:
        total += a
    return total
In such a case, both addition and multiply are units of our software.


---
**Page 21**

Getting Started with Software Testing
Chapter 1
[ 21 ]
While addition can be tested in isolation, multiply must use addition to work.
multiply is thus defined as a sociable unit, while addition is a solitary unit.
Sociable unit tests are frequently also referred to as component tests. Your architecture 
mostly defines the distinction between a sociable unit test and a component test and it's
hard to state exactly when one name should be preferred over the other.
While sociable units usually lead to more complete testing, they are slower, require more
effort during the Arrange phase, and are less isolated. This means that a change in
addition can make a test of multiply fail, which tells us that there is a problem, but also
makes it harder to guess where the problem lies exactly.
In the subsequent chapters, we will see how sociable units can be converted into solitary
units by using test doubles. If you have complete testing coverage for the underlying units,
solitary unit tests can reach a level of guarantee that is similar to that of sociable units with
must less effort and a faster test suite.
Test units are usually great at testing software from a white-box perspective, but that's not
the sole point of view we should account for in our testing strategy. Test units guarantee
that the code does what the developer meant it to, but do little to guarantee that the code
does what the user needs. Integration and functional tests are usually more effective in
terms of testing at that level of abstraction.
Understanding integration and functional
tests
Testing all our software with solitary units can't guarantee that it's really working as
expected. Unit testing confirms that the single components are working as expected, but
doesn't give us any confidence about their effectiveness when paired together.
It's like testing an engine by itself, testing the wheels by themselves, testing the gears, and
then expecting the car to work. We wouldn't be accounting for any issues introduced in the
assembly process.
So we have a need to verify that those modules do work as expected when paired together.


---
**Page 22**

Getting Started with Software Testing
Chapter 1
[ 22 ]
That's exactly what integration tests are expected to do. They take the modules we tested
individually and test them together.
Integration tests
The scope of integration tests is blurry. They might integrate two modules, or they might
integrate tens of them. While they are more effective when integrating fewer modules, it's
also more expensive to move forward as an approach and most developers argue that the
effort of testing all possible combinations of modules in isolation isn't usually worth the
benefit.
The boundary between unit tests made of sociable units and integration tests is not easy to
explain. It usually depends on the architecture of the software itself. We could consider
sociable units tests those tests that test units together that are inside the same architectural
components, while we could consider integration tests those tests that test different
architectural components together.
In an application, two separate services will be involved: Authorization and
Authentication. Authentication takes care of letting the user in and identifying them,
while Authorization tells us what the user can do once it is authenticated. We can see
this in the following code block:
class Authentication:
    USERS = [{"username": "user1",
              "password": "pwd1"}]
    def login(self, username, password):
        u = self.fetch_user(username)
        if not u or u["password"] != password:
            return None
        return u
    def fetch_user(self, username):
        for u in self.USERS:
            if u["username"] == username:
                return u
        else:
            return None
class Authorization:
    PERMISSIONS = [{"user": "user1",
                    "permissions": {"create", "edit", "delete"}}]


---
**Page 23**

Getting Started with Software Testing
Chapter 1
[ 23 ]
    def can(self, user, action):
        for u in self.PERMISSIONS:
            if u["user"] == user["username"]:
                return action in u["permissions"]
        else:
            return False
Our classes are composed of two primary methods: Authentication.login and
Authorization.can. The first is in charge of authenticating the user with a username and
password and returning the authenticated user, while the second is in charge of verifying
that a user can do a specific action. Tests for those methods can be considered unit tests.
So TestAuthentication.test_login will be a unit test that verifies the behavior of the
Authentication.login unit, while TestAuthorization.test_can will be a unit test
that verifies the behavior of the Authorization.can unit:
class TestAuthentication(unittest.TestCase):
    def test_login(self):
        auth = Authentication()
        auth.USERS = [{"username": "testuser", "password": "testpass"}]
        resp = auth.login("testuser", "testpass")
        assert resp == {"username": "testuser", "password": "testpass"}
class TestAuthorization(unittest.TestCase):
    def test_can(self):
        authz = Authorization()
        authz.PERMISSIONS = [{"user": "testuser", "permissions":
                              {"create"}}]
        resp = authz.can({"username": "testuser"}, "create")
        assert resp is True
Here, we have the notable difference that TestAuthentication.test_login is a sociable
unit test as it depends on Authentication.fetch_user while testing
Authentication.login, and TestAuthorization.test_can is instead a solitary unit
test as it doesn't depend on any other unit.
So where is the integration test?


---
**Page 24**

Getting Started with Software Testing
Chapter 1
[ 24 ]
The integration test will happen once we join those two components of our architecture
(authorization and authentication) and test them together to confirm that we can actually
have a user log in and verify their permissions:
class TestAuthorizeAuthenticatedUser(unittest.TestCase):
    def test_auth(self):
        auth = Authentication()
        authz = Authorization()
        auth.USERS = [{"username": "testuser", "password": "testpass"}]
        authz.PERMISSIONS = [{"user": "testuser",
                              "permissions": {"create"}}]
        u = auth.login("testuser", "testpass")
        resp = authz.can(u, "create")
        assert resp is True
Generally, it's important to be able to run your integration tests independently from your
unit tests, as you will want to be able to run the unit tests continuously during development
on every change:
$ python 05_integration.py TestAuthentication TestAuthorization
........
----------------------------------------------------------------------
Ran 8 tests in 0.000s
OK
While unit tests are usually verified frequently during the development cycle, it's common
to run your integration tests only when you've reached a stable point where your unit tests
all pass:
$ python 05_integration.py TestAuthorizeAuthenticatedUser
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
As you know that the units that you wrote or modified do what you expected, running
the TestAuthorizeAuthenticatedUser case only will confirm that those entities work
together as expected.
Integration tests integrate multiple components, but they actually divide themselves into
many different kinds of tests depending on their purpose, with the most common kind
being functional tests.


---
**Page 25**

Getting Started with Software Testing
Chapter 1
[ 25 ]
Functional tests
Integration tests can be very diverse. As you start integrating more and more components,
you move toward a higher level of abstraction, and in the end, you move so far from the
underlying components that people feel the need to distinguish those kinds of tests as they
offer different benefits, complexities, and execution times.
That's why the naming of functional tests, end-to-end tests, system tests, acceptance tests,
and so on all takes place.
Overall, those are all forms of integration tests; what changes are their goal and purpose:
Functional tests tend to verify that we are exposing to our users the feature we
actually intended. They don't care about intermediate results or side-effects; they
just verify that the end result for the user is the one the specifications described,
thus they are always black-box tests.
End-to-End (E2E) tests are a specific kind of functional test that involves the
vertical integration of components. The most common E2E tests are where
technologies such as Selenium are involved in accessing a real application
instance through a web browser.
System tests are very similar to functional tests themselves, but instead of testing
a single feature, they usually test a whole journey of the user across the system.
So they usually simulate real usage patterns of the user to verify that the system
as a whole behaves as expected.
Acceptance tests are a kind of functional test that is meant to confirm that the
implementation of the feature does behave as expected. They usually express the
primary usage flow of the feature, leaving less common flows for other
integration tests, and are frequently provided by the specifications themselves to
help the developer confirm that they implemented what was expected.
But those are not the only kinds of integration that people refer to; new types are
continuously defined in the effort to distinguish the goals of tests and responsibilities.
Component tests, contract tests, and many others are kinds of tests whose goal is to verify
integration between different pieces of the software at different layers. Overall, you
shouldn't be ashamed of asking your colleagues what they mean exactly when they use
those names, because you will notice each one of them will value different properties of
those tests when classifying them into the different categories.
The general distinction to keep in mind when distinguishing between integration tests and
functional tests is that unit and integration tests aim to test the implementation, while
functional tests aim to test the behavior.


---
**Page 26**

Getting Started with Software Testing
Chapter 1
[ 26 ]
How you do that can easily involve the same exact technologies and it's just a matter of
different goals. Properly covering the behavior of your software with the right kind of tests
can be the difference between buggy software and reliable software. That's why there has
been a long debate about how to structure test suites, leading to the testing pyramid and
the testing trophy as the most widespread models of test distribution.
Understanding the testing pyramid and
trophy
Given the need to provide different kinds of tests – unit, integration, and E2E as each one of
them has different benefits and costs, the next immediate question is how do we get the
right balance?
Each kind of test comes with a benefit and a cost, so it's a matter of finding where we get
the best return on investment:
E2E tests verify the real experience of what the user faces. They are, in theory, the
most realistic kind of tests and can detect problems such as incompatibilities with
specific platforms (for example, browsers) and exercise our system as a whole.
But when something goes wrong, it is hard to spot where the problem lies. They
are very slow and tend to be flaky (failing for reasons unrelated to our software,
such as network conditions).
Integration tests usually provide a reasonable guarantee that the software is
doing what it is expected to do and are fairly robust to internal implementation
changes, requiring less frequent refactoring when the internals of the software
change. But they can still get very slow if your system involves writes to database
services, the rendering of page templates, routing HTTP requests, and generally
slow parts. And when something goes wrong, we might have to go through tens
of layers before being able to spot where the problem is.
Unit tests can be very fast (especially when talking of solitary units) and provide
very pinpointed information about where problems are. But they can't always 
guarantee that the software as a whole does what it's expected to do and can
make changing implementation details expensive because a change to internals
that don't impact the software behavior might require changing tens of unit tests.
Each of them has its own pros and cons, and the development community has long argued
how to get the right balance.
The two primary models that have emerged are the testing pyramid and the testing trophy,
named after their shapes.


---
**Page 27**

Getting Started with Software Testing
Chapter 1
[ 27 ]
The testing pyramid
The testing pyramid originates from Mike Cohn's Succeeding with Agile book, where the two
rules of thumb are "Write test with different granularities" (so you should have unit,
integration, E2E, and so on...) and "the more you get high level, the less you should test" (so you
should have tons of unit tests, and a few E2E tests).
While different people will argue about which different layers are contained within it, the
testing pyramid can be simplified to look like this:
Figure 1.1 – Testing pyramid
The tip of the pyramid is narrow, thus meaning we have fewer of those tests, while the base
is wider, meaning we should mostly cover code with those kinds of tests. So, as we move
down through the layers, the lower we get, the more tests we should have.
The idea is that as unit tests are fast to run and expose pinpointed issues early on, you
should have a lot of them and shrink the number of tests as they move to higher layers and
thus get slower and vaguer about what's broken.
The testing pyramid is probably the most widespread practice for organizing tests and
usually pairs well with test-driven development as unit tests are the founding tool for the
TDD process.


---
**Page 28**

Getting Started with Software Testing
Chapter 1
[ 28 ]
The other most widespread model is the testing trophy, which instead emphasizes
integration tests.
The testing trophy
The testing trophy originates from a phrase by Guillermo Rauch, the author of Socket.io
and many other famous JavaScript-based technologies. Guillermo stated that developers
should "Write tests. Not too many. Mostly integration."
Like Mike Cohn, he clearly states that tests are the foundation of any effective software
development practice, but he argues that they have a diminishing return and thus it's
important to find the sweet spot where you get the best return on the time spent writing
tests.
That sweet spot is expected to live in integration tests because you usually need fewer of
them to spot real problems, they are not too bound to implementation details, and they are
still fast enough that you can afford to write a few of them.
So the testing trophy will look like this:
Figure 1.2 – Testing trophy


---
**Page 29**

Getting Started with Software Testing
Chapter 1
[ 29 ]
As you probably saw, the testing trophy puts a lot of value on static tests too, because the
whole idea of the testing trophy is that what is really of value is the return on investment,
and static checks are fairly cheap, up to the point that most development environments run
them in real time. Linters, type checkers, and more advanced kinds of type analyzers are
cheap enough that it would do no good to ignore them even if they are rarely able to spot
bugs in your business logic.
Unit tests instead can cost developers time with the need to adapt them due to internal
implementation detail changes that don't impact the final behavior of the software in any
way, and thus the effort spent on them should be kept under control.
Those two models are the most common ways to distribute your tests, but more best
practices are involved when thinking of testing distribution and coverage.
Testing distribution and coverage
While the importance of testing is widely recognized, there is also general agreement that
test suites have a diminishing return.
There is little point in wasting hours on testing plain getters and setters or testing
internal/private methods. The sweet spot is said to be around 80% of code coverage, even
though I think that really depends on the language in use – the more expressive your
language is, the less code you have to write to perform complex actions. And all complex
actions should be properly tested, so in the case of Python, the sweet spots probably lies
more in the range of 90%. But there are cases, such as porting projects from Python 2 to
Python 3, where code coverage of 100% is the only way you can confirm that you haven't
changed any behavior at all in the process of porting your code base.
Last but not least, most testing practices related to test-driven development take care of the
testing practice up to the release point. It's important to keep in mind that when the
software is released, the testing process hasn't finished.
Many teams forget to set up proper system tests and don't have a way to identify and
reproduce issues that can only happen in production environments with real concurrent
users and large amounts of data. Having staging environments and a suite to simulate
incidents or real users' behaviors might be the only way to spot bugs that only happen after
days of continuous use of the system. And some companies go as far as testing the
production system with tools that inject real problems continuously for the sole purpose of
verifying that the system is solid.


---
**Page 30**

Getting Started with Software Testing
Chapter 1
[ 30 ]
Summary
As we saw in the sections about integration tests, functional tests, and the testing
pyramid/trophy models, there are many different visions about what should be tested, with
which goals in mind, and how test suites should be organized. Getting this right can impact
how much you trust your automatic test suite, and thus how much you evolve it because it
provides you with value.
Learning to do proper automated testing is the gateway to major software development
boosts, opening possibilities for practices such as continuous integration and continuous
delivery, which would otherwise be impossible without a proper test suite.
But testing isn't easy; it comes with many side-effects that are not immediately obvious, and
for which the software development industry started to provide tools and best practices
only recently. So in the next chapters, we will look at some of those best practices and tools
that can help you write a good, easily maintained test suite.


---
**Page 31**

2
Test Doubles with a Chat
Application
We have seen how a test suite, to be reasonably reliable, should include various kinds of
tests that cover components at various levels. Usually, tests, in regard to how many
components they involve, are categorized into at least three kinds: unit, integration, and
end-to-end.
Test doubles ease the implementation of tests by breaking dependencies between
components and allowing us to simulate the behaviors we want.
In this chapter, we will look at the most common kinds of test doubles, what their goals are,
and how to use them in real code. By the end of this chapter, we will have covered how to
use all those test doubles and you will be able to leverage them for your own Python
projects.
By adding test doubles to your toolchain, you will be able to write faster tests, decouple the
components you want to test from the rest of the system, simulate behaviors that depend
on other components' state, and in general move your test suite development forward with
fewer blockers.
In this chapter, we will learn how to move forward, in the Test-Driven Development
(TDD) way, the development of an application that depends on other external
dependencies such as a database management system and networking, relying on test
doubles for the development process and replacing them in our inner test layers to ensure
fast and consistent execution of our tests.
In this chapter, we will cover the following topics:
Introducing test doubles
Starting our chat application with TDD
Using dummy objects
Replacing components with stubs


