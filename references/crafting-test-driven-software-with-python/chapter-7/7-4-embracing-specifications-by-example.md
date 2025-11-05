# 7.4 Embracing specifications by example (pp.180-187)

---
**Page 180**

Fitness Function with a Contact Book Application
Chapter 7
[ 180 ]
For this reason, people tend to split the features into multiple Python modules. Each
Python module will contain the functions implementing the scenarios and steps that are
only related to that, usually leading to a layout that is similar to
tests/acceptance/deleting_contacts.py,
tests/acceptance/adding_contacts.py, and so on.
Now that we know how to write acceptance tests in a more shareable way, we are going to
lower the barrier of how easy they are to understand and verify for a human by introducing
specification by example, a practice that tries to ensure that what the software has to do is
not only expressed and verified, but that it is also expressed in a way that is less subject to
misunderstandings.
With BDD, we might all agree on what's written in the acceptance tests and say that it
expresses perfectly the specifications of our software, but the translation phase from the
Gherkin syntax to code based tests can lead to misunderstandings. Specifications by
example try to solve these kinds of issues by relying on clear examples that should be hard
to misunderstand and by providing multiple examples for each scenario to further reduce
doubts.
Embracing specifications by example
A common problem with acceptance tests is that it takes some effort to understand what's
going on. If you are not already familiar with the domain, it can be easy to misunderstand
them, thus leading to the wrong checks being performed even if everyone that reviewed it
agreed with the original acceptance tests.
For example, if I read an acceptance test such as the following:
Given a first number 2
And a second number 3
When I run the software
Then I get 3 as the output
I might be tempted to understand it as, Oh, ok! The test is meant to verify that given two
numbers, we print the highest one.
But that might not be the requirement; the requirement might actually be, Given two
numbers, print the lowest one plus one. How can I understand which one that test was actually
meant to verify?
The answer is to provide more examples. The more examples we provide for our tests, the
easier it is to understand them.


---
**Page 181**

Fitness Function with a Contact Book Application
Chapter 7
[ 181 ]
Examples are provided in a table-like format, where columns are meant to show the data
involved in our examples and the resulting outcomes. In general, we can say that the
columns should describe the state of the system for that example:
Number1 | Number2 | Result
   2    |    3    |   3
If, by having only 2 and 3 as numbers and 3 as the result, both understandings of the test
would be acceptable, the moment I expand my examples with one more, it becomes
immediately obvious which one of the two I meant.
So we can add one more row to our examples table to add an example that further reduces
the uncertainty regarding what the expected behavior is:
Number1 | Number2 | Result
   2    |    3    |   3
   5    |    7    |   6
The second example makes it possible to understand that we are not printing the highest of
the two numbers, but that we are actually printing the lowest plus one.
What if I have further doubts? Maybe it's not the lowest plus one; maybe it's the first of the
two numbers plus one!
Number1 | Number2 | Result
   2    |    3    |   3
   5    |    7    |   6
   8    |    4    |   5
With the third example, we made it clear that we actually want the lowest of the two
numbers and not the first one. Just add more examples until the reading of the test becomes
fairly obvious for every reader.
That's the core idea behind specification by example: the behavior of a software can be
described by providing enough examples that make it obvious to see what's going on.
Instead of having to write tens of pages trying to explain what's happening, given enough
examples, which can be automatically verified, the reader can easily see what's going on.
Generally, there are many benefits to this approach, including the following:
We don't have the specification and the test: the specifications are testable by
definition.
Tests that were easy to misunderstand can easily be made more obvious by
adding more examples, which are cheaper to add than more tests.


---
**Page 182**

Fitness Function with a Contact Book Application
Chapter 7
[ 182 ]
You can't change the behavior of the software without updating the
specifications. The specifications are the examples used to verify the software; if
they don't verify, then the updated tests would not pass.
As the specifications are meant to be human-readable, the Gherkin language is a good
foundation for writing the specifications themselves making sure that they can be verified.
We just need to add a section where we provide a list of all the possible examples for a
scenario.
For example, we might write the final feature of our software: Listing the contacts using this
model. To do so, let's write a scenario with two examples of possible contact lists to print:
Feature: Listing Contacts
    Contacts added to our contact book can be listed back.
Scenario: Listing Added Contacts
    Given I have a contact book
    And I have a first <first> contact
    And I have a second <second> contact
    When I run the "contacts ls" command
    Then the output contains <listed_contacts> contacts
    Examples:
    | first | second | listed_contacts |
    | Mario | Luigi  | Mario,Luigi     |
    | John  | Jane   | John,Jane       |
Compared to the scenarios we wrote before, the main difference is that we used some
placeholders contained within angular brackets (<first>, <second>, and
<listed_contacts>), and then we have a list of examples at the end of the scenario.
This whole feature description with its examples becomes our specification and sole
document that we discuss with all stakeholders. If we have doubts, we add more examples
and scenarios to the feature until it becomes obvious to everyone how the software should
behave.
We save our feature description as "tests/acceptance/list_contacts.feature" and,
as we did for the previous cases, we start by adding a test for our scenario so that PyTest
knows that we have one more test to run:
@scenario("../acceptance/list_contacts.feature",
            "Listing Added Contacts")
def test_listing_added_contacts(capsys):
    pass


---
**Page 183**

Fitness Function with a Contact Book Application
Chapter 7
[ 183 ]
As we have to check the output of the command (which will print the contacts), this time,
our test explicitly mentions the capsys fixture, so that output starts to be captured when
the test is run.
The first step of our scenario is "Given I have a contact book", which we had
already implemented for our previous contacts deletion test, so in this case we have
nothing to do. pytest-bdd will reuse the same test implementation as the step is the same.
Going further, we have two steps in charge of adding the two contacts from the examples
into our contact list:
    And I have a first <first> contact
    And I have a second <second> contact
These translate into two new steps, and both of these are in charge of adding one contact to
the contact book, as shown in the following code block:
@given("I have a first <first> contact")
def have_a_first_contact(contactbook, first):
    contactbook.add(first, "000")
    return first
@given("I have a second <second> contact")
def have_a_second_contact(contactbook, second):
    contactbook.add(second, "000")
    return second
As the two tests have the same exact implementation, you might be wondering why we
made two different Given steps instead of a single one with a parser.
The reason is because Given steps, in BDD, are meant to represent data that is needed to
perform the test. They state what you have in a way that should make it possible to look up
any of the given things explicitly. If, in any other step, we want to know what's the name of
the first person that was added to the contact book, that step would only have to refer to the
given test by the name of the function, and the given step would behave as a fixture
providing that specific entity.
To make it easier to understand, if we want to get back the name of the first contact added
to the contact book, we just have to add a have_a_first_contact argument to the
function implementing the step that needs that name. As the have_a_first_contact
function returns a value, that value would be associated with any have_a_first_contact
argument name in any other step.
In the same way, if we want to refer to the second person in our contact book, we just have
to require the have_a_second_contact argument.


---
**Page 184**

Fitness Function with a Contact Book Application
Chapter 7
[ 184 ]
If, instead of having those two separate Given steps, we had a single have_a_contact
step that used a parser, and we used it twice to add two contacts, which one of the two
would the have_a_contact argument refer to? It would be ambiguous, and that's why
pytest-bdd prevents reuse of the same Given step twice in the same scenario. Each Given
step must be unique so that the data it provides is uniquely identifiable by the step name.
The same doesn't apply to other kinds of steps. For example, it's perfectly
possible to reuse the same When step multiple times in a scenario. That's
because When steps are not meant to represent data and so have no need
to be uniquely identifiable.
Now that we have our Given steps in place, the next step is the When step, which is meant
to run the command that lists our contacts:
When I run the "contacts ls" command
This again is a step that we already implemented in our previous delete contact scenario. In
the scenario, the When step we implemented there accepted a command to run as an
argument, and so it's able to run any command. pytest-bdd will be able to reuse it, and
hence we don't have to implement anything.
The final step is the one meant to verify that the command actually did what we expect, the
Then step:
Then the output contains <listed_contacts> contacts
This step will have to check the output provided by the command and ensure that the
contacts we wrote in our example actually exist in the output:
@then("the output contains <listed_contacts> contacts")
def outputcontains(listed_contacts, capsys):
    expected_list = "".join([
        f"{c} 000\n" for c in listed_contacts.split(",")
    ])
    out, _ = capsys.readouterr()
    assert expected_list == out
We already know that we need capsys to be able to read the output of a program being
tested. Apart from capsys, our step also requires the list of contacts that it has to check.
Those are coming from the Examples section in the scenario.


---
**Page 185**

Fitness Function with a Contact Book Application
Chapter 7
[ 185 ]
In the Examples entry, listed_contacts were provided as comma-separated
("Mario,Luigi"), so the first thing we do is to split them by the comma so that we can get
back all the contacts. Then, as our program is going to print them in separate lines with
their phone numbers, we append the phone number at the end of the line (which is
hardcoded at "000" as that's what we had in our two have_a_first_contact and
have_a_second_contact steps). The expected_list variable is meant to contain the list
of contacts, one by line with their phone number. For the "Mario,Luigi" example, the
content would thus be as follows:
Mario 000
Luigi 000
Once we have the expected_list variable containing the properly formatted text, we
only have to compare it to the actual output of the application to confirm that the
application printed the two contacts we expected with their phone numbers.
Now that we have translated our steps to code, we can run our test suite to confirm that the
test is actually verifying our implementation:
$ pytest -v
...
.../test_acceptance.py::test_listing_added_contacts[Mario-Luigi-
Mario,Luigi] FAILED
.../test_acceptance.py::test_listing_added_contacts[John-Jane-John,Jane]
FAILED
...
E ValueError: not enough values to unpack (expected 2, got 1)
As expected, since we haven't yet implemented any support for listing contacts, the
software crashed, but at least we know that pytest-bdd was able to identify the code for
all the steps, translate them, and run the scenario for both our examples (as we have the
same test_listing_added_contacts test performed twice, one for Mario-Luigi-
Mario,Luigi and one for John-Jane-John,Jane).
As usual, we can jump to our functional and unit tests to drive the actual implementation,
and a possible edit to our Application object could be to handle commands that don't
have any args, and then call a printlist function when the command is "ls":
class Application:
    ...
    def run(self, text):
        text = text.strip()
        _, cmd = text.split(maxsplit=1)
        try:


---
**Page 186**

Fitness Function with a Contact Book Application
Chapter 7
[ 186 ]
            cmd, args = cmd.split(maxsplit=1)
        except ValueError:
            args = None
        if cmd == "add":
            name, num = args.rsplit(maxsplit=1)
            try:
                self.add(name, num)
            except ValueError as err:
                print(err)
                return
        elif cmd == "del":
            self.delete(args)
        elif cmd == "ls":
            self.printlist()
        else:
            raise ValueError(f"Invalid command: {cmd}")
    ...
    def printlist(self):
        for c in self._contacts:
            print(f"{c[0]} {c[1]}")
The printlist function simply iterates over all contacts and prints them with their phone
numbers.
As we have the implementation in place, our acceptance test should pass and confirm that
it behaves like it is meant to:
$ pytest -v
...
.../test_acceptance.py::test_listing_added_contacts[Mario-Luigi-
Mario,Luigi] PASSED
.../test_acceptance.py::test_listing_added_contacts[John-Jane-John,Jane]
PASSED
...
Now that the acceptance tests pass for the examples we provided, we know that the 
implementation satisfies what our team wanted so far.


---
**Page 187**

Fitness Function with a Contact Book Application
Chapter 7
[ 187 ]
Summary
In this chapter, we saw how we can write acceptance tests that can be shared with other
stakeholders to review the behavior of the software and not just be used by developers as a
way to verify that behavior. We saw that it's possible to express the specifications of the
software itself in the form of scenarios and examples, which guarantees that our
specifications are always in sync with what the software actually does and that our
software must always match the specifications as they become the tests themselves.
Now that we know how to move a project forward in a test-driven way using PyTest, in the
next chapter we are going to see more essential PyTest plugins that can help us during our
daily development practice.


