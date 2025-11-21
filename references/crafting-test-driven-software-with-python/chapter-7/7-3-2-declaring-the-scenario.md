# 7.3.2 Declaring the scenario (pp.174-175)

---
**Page 174**

Fitness Function with a Contact Book Application
Chapter 7
[ 174 ]
Declaring the scenario
After the feature definition, we declare that our first scenario tries to delete a basic contact
and see that things work as expected:
Scenario: Removing a Basic Contact
    Given I have a contact book
    And I have a "John" contact
    When I run the "contacts del John" command
    Then My contacts list is now empty
The scenario is written in fairly plain English so that we can review with other stakeholders
without having to understand software development or programming languages. Once we
agree that it represents correctly what we expect from the software, then we can turn it to
code by using pytest-bdd.
pytest-bdd is based on PyTest itself, so each scenario is exposed as a test function. To
signal that it's also a scenario, we add the @scenario decorator and point it to the feature
file.
In our tests/functional/test_acceptance.py file, we are going to add a test for our
Removing a Basic Contact scenario that we described in the
tests/acceptance/delete_contact.feature file using the Gherkin language:
from pytest_bdd import scenario
@scenario("../acceptance/delete_contact.feature",
            "Removing a Basic Contact")
def test_deleting_contacts():
    pass
Unlike the standard PyTest test, a scenario test is usually an empty function. We can
perform additional testing within the function, but any code that we add will run after the
scenario has been completed.
The test itself is loaded from the feature file looking for a scenario that has the same name
as the one we provided in the decorator (in this case,"Removing a Basic Contact").
Then, the scenario text is parsed and each step defined in it is executed one after the other.
But how does PyTest know what to do in order to perform the steps? Our scenario starts by
ensuring that we have a contact book with one contact inside named "John":
Given I have a contact book
And I have a "John" contact


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


