# 7.3.1 Defining a feature file (pp.173-174)

---
**Page 173**

Fitness Function with a Contact Book Application
Chapter 7
[ 173 ]
Our application is able to add contacts, but it still doesn't allow us to delete or list them, so
it's not very useful. So, the next step is to implement a delete contacts feature, and we decide
to do so by using BDD.
To get started using BDD, we will create a new tests/acceptance directory, where we
are going to put all the acceptance tests for our features. Thus, the final layout of our test
suite will appear as follows:
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── acceptance
    │   └── ...
    ├── functional
    │   └── test_acceptance.py
    └── unit
        └── ...
Then we can create a tests/acceptance/delete_contact.feature file that will
contain all our acceptance scenarios for the deleting contacts feature.
Defining a feature file
We start the file by making it clear that it covers the deletion of contacts:
Feature: Deleting Contacts
    Contacts added to our contact book can be removed.
Now that we have a location where all our testing scenarios can reside, we can try to add
the first one. The basics of the Gherkin language are fairly easy to grasp. In the end, it is
meant to be readable by everyone without having to study a programming language. So,
the core words are the Given, When, Then, and And keywords that start every step in our
scenarios, and to start a new scenario we just use Scenario.


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


