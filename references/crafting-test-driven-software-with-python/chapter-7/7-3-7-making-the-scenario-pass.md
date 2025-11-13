# 7.3.7 Making the scenario pass (pp.178-180)

---
**Page 178**

Fitness Function with a Contact Book Application
Chapter 7
[ 178 ]
E ValueError: Invalid command: del
src/contacts/__init__.py:27: ValueError
Our scenario steps were all properly executed, but, as expected, our test has not passed. It
choked on the When I run the "contacts del John"command step because our
contacts application doesn't yet recognize the del command.
Making the scenario pass
So, our next steps will involve diving into the functional and unit tests that we need to
define how the del command has to behave while providing an implementation for it.
As that's a part that we already know from the previous chapters of the book, we are going
to provide the final resulting implementation here directly:
class Application:
    ...
    def run(self, text):
        text = text.strip()
        _, cmd = text.split(maxsplit=1)
        cmd, args = cmd.split(maxsplit=1)
        if cmd == "add":
            name, num = args.rsplit(maxsplit=1)
            try:
                self.add(name, num)
            except ValueError as err:
                print(err)
                return
        elif cmd == "del":
            self.delete(args)
        else:
            raise ValueError(f"Invalid command: {cmd}")
    ...
    def delete(self, name):
        self._contacts = [
            c for c in self._contacts if c[0] != name
        ]
        self.save()


---
**Page 179**

Fitness Function with a Contact Book Application
Chapter 7
[ 179 ]
Now that our implementation is in place and the "del" command is dispatched to the
Application.delete function, it will remove anyone matching the provided name from
the list of contacts. We can check that our acceptance test passes and that our contacts book
application is actually doing what we meant it to do:
$ pytest -v -k deleting
.../test_acceptance.py::test_deleting_contacts   PASSED [100%]
...
Our scenario was executed and our implementation satisfied it. The steps were executed by
the functions we provided in our test_acceptance.py file:
@scenario("../acceptance/delete_contact.feature",
            "Removing a Basic Contact")
def test_deleting_contacts():
    pass
@given("I have a contact book", target_fixture="contactbook")
def contactbook():
    return contacts.Application()
@given(parsers.parse("I have a \"{contactname}\" contact"))
def have_a_contact(contactbook, contactname):
    contactbook.add(contactname, "000")
@when(parsers.parse("I run the \"{command}\" command"))
def runcommand(contactbook, command):
    contactbook.run(command)
@then("My contacts book is now empty")
def emptylist(contactbook):
    assert contactbook._contacts == []
The problem with this approach is that if we have multiple scenarios, then it can tend to get
confusing. It's already hard to spot out of the box the order of execution of this code, or the
relations between the functions. We would have to constantly jump back and forth to the
.feature file in order to understand what's going on.
This is especially the case if we have multiple different scenarios from unrelated features
that can become hard to navigate, making it difficult to even distinguish between scenarios
that are related to the same feature.


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


