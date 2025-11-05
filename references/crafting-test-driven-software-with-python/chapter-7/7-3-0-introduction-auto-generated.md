# 7.3.0 Introduction [auto-generated] (pp.172-173)

---
**Page 172**

Fitness Function with a Contact Book Application
Chapter 7
[ 172 ]
Finally,Application.run is the user interface to our software. Given any command in the
form "executablename command arguments", it parses it and executes the correct
command. Currently, only add is implemented, but in the following sections, we will
implement the del and ls commands, too.
Now we know that acceptance tests are vital in the feedback cycle in the case of people that
understand the goals of the software well. Next, we need to focus on how to improve that
communication cycle. In this example we were lucky that our counterpart understood
Python, but what if they didn't? It's probably common that the people who understand the
business well don't know a thing about programming, and so we need a better way to set
up our communication than using Python.
Using behavior-driven development
For the first phase of our contact book application, we took it for granted that the people we
had to speak with understood the Python language well enough that we could share with
them our acceptance tests for review and confirm that we were going in the right direction.
While it's getting more and more common that people involved in product definition have
at least an entry-level knowledge of programming, we can't take it for granted that every
stakeholder we need to enter into discussions with knows Python.
So how can we keep the same kind of feedback loop and apply the strategy of reviewing all
our acceptance tests with other stakeholders without involving Python?
That's what Behavior-Driven Development (BDD) tries to solve. BDD takes some concepts
from Test-Driven Development (TDD) and Domain-Driven Design (DDD) to allow all
stakeholders to speak the same language as the technical team.
In the end, BDD tries to mediate between the two worlds. The language becomes English,
instead of Python, but a more structured form of English for which, in the end, a parser can
be written and developers embrace the business glossary (no more classes named User and
PayingUser if the business calls them Lead and Customer) so that the tests that the
developers write make sense for all other stakeholders, too.
This is usually achieved by defining the tests in a language that is commonly named
Gherkin (even though BDD doesn't strictly mandate Gherkin usage) and, luckily for us, the
pytest-bdd plugin allows us to extend our test suite with tests written in a subset of the
Gherkin language that coexists very well with all the other pytest plugins or features we
might be using.


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


