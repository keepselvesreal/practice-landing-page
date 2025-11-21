# 7.3.5 Performing actions with the When step (pp.176-177)

---
**Page 176**

Fitness Function with a Contact Book Application
Chapter 7
[ 176 ]
In this case, we have to tell pytest-bdd how to add contacts to a contact book and that
John is the name of the contact that we want to add. This can be done by using another
@given decorator (And is an alias for the previous keyword we just used):
from pytest_bdd import parsers
@given(parsers.parse("I have a \"{contactname}\" contact"))
def have_a_contact(contactbook, contactname):
    contactbook.add(contactname, "000")
We are also relying on parsers.parse provided by pytest-bdd to let the step definition
know that "John" is not part of the step itself, but that it's actually a variable. It can be
John, it can be Jane, it can be any name, and they will all go to this same step. The name of
the contact will be extracted from the step and will be passed as an argument to the
function in charge of executing the step.
Our function then only has to take that name and add it to the contact book. But where
does the contact book come from? When we declared the "I have a contact book"
step, we said that steps can also be PyTest fixtures, so when our have_a_contact function
finds the need for a contactbook argument, the PyTest dependency injection will resolve
it for us by providing what the contactbook fixture that was associated with the just
executed "I have a contact book" step returned.
Hence, to the contactbook provided by the fixture, we invoke the add method, passing
the contactname provided by the parser. In this scenario, we don't care for phone
numbers, so the contact is always added with "000" as its phone number.
Performing actions with the When step
Moving forward, our next step in the scenario is a When step. These are no longer steps
associated with preparation for testing; they are intended to perform the actions we want to
perform (remember the Arrange, Act, and Assert pattern? Well, we could consider the
Given, When, and Then steps as the three BDD counterparts to the pattern):
When I run the "contacts del John" command
Just like the previous two steps, we are going to link a function in charge of executing the
code that has to happen when this step is found, in this case using the pytest_bdd.when
decorator:
from pytest_bdd import when
@when(parsers.parse("I run the \"{command}\" command"))


---
**Page 177**

Fitness Function with a Contact Book Application
Chapter 7
[ 177 ]
def runcommand(contactbook, command):
    contactbook.run(command)
As we did for the have_a_contact function, runcommand needs the contactbook against
which it has to run the command and can rely on parsers.parse to retrieve the command
that has to be executed on the contact book.
It's not uncommon that the Given and When steps can be reused across multiple scenarios.
Making those steps parametric using parsers allows their implementation functions to be
reused more frequently. In this case, we will be able to reuse the same step definition
independently from the command we want to run, thus allowing us to implement scenarios
for other features too, and not just for deleting contacts.
In this case, as our step was I run the "contacts del John"command, the function
will run the contacts del John command as this is the one we have provided in the
step.
Our final step in the scenario is the one meant to verify that the contact was actually deleted
as we expect once the command is performed:
    Then My contacts list is now empty
Then, steps usually translate into the final assertion phase of our tests, so we are going to
verify that the contact book is really empty.
Assessing conditions with the Then step
In this case, there is no need to parse anything, but our function will still need the
contactbook for which it has to verify that it is actually empty:
from pytest_bdd import then
@then("My contacts book is now empty")
def emptylist(contactbook):
    assert contactbook._contacts == []
Now that we have provided the entry point for our scenario and the implementation of all
its steps, we can finally retry running our tests to confirm that the scenario actually gets
executed:
$ pytest -v -k deleting
.../test_acceptance.py::test_deleting_contacts FAILED [100%]
...


