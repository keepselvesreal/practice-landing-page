# 1.4.2 Test units (pp.19-21)

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


