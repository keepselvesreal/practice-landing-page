# 7.3.4 Further setup with the And step (pp.175-176)

---
**Page 175**

Fitness Function with a Contact Book Application
Chapter 7
[ 175 ]
How does pytest-bdd even know what a contact book is and how to add a contact to it?
Well, it doesn't.
Running the scenario test
If we try to run our scenario test at this point, as shown here, PyTest will just report errors
complaining that it doesn't know what to do with the first step that it encounters:
$ pytest -v -k deleting
.../test_acceptance.py::test_deleting_contacts FAILED [100%]
...
StepDefinitionNotFoundError: Step definition is not found: Given "I have a
contact book". Line 5 in scenario "Removing a Basic Contact" in the feature
"/tests/acceptance/delete_contact.feature
We have to tell pytest-bdd what to do when it faces a step. So, in our
test_acceptance.py, we must provide the code that has to be executed when a step is
met and link it to the step using the @given decorator, as shown in the following code
block:
from pytest_bdd import scenario, given
@given("I have a contact book", target_fixture="contactbook")
def contactbook():
    return contacts.Application()
Every time pytest-bdd finds"I have a contact book" as a step in a scenario, it will
invoke our contactbook function. The contactbook function doesn't just tell PyTest how
to run the step, but thanks to the target_fixture="contactbook" argument of @given,
it's also a fixture that provides the contactbook dependency every time it is requested by
another step. Any other step of the scenario that requires a contactbook can just refer to it
and they will get back the Application that was created by the "I have a contact
book" step.
Further setup with the And step
For now, the contact book is totally empty, but we know that the next step is to add a
contact named "John" to it:
And I have a "John" contact


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


