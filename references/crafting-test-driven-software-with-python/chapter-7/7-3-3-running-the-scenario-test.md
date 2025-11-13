# 7.3.3 Running the scenario test (pp.175-175)

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


