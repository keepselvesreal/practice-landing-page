# 7.2.0 Introduction [auto-generated] (pp.165-166)

---
**Page 165**

Fitness Function with a Contact Book Application
Chapter 7
[ 165 ]
Technical requirements
We need a working Python interpreter with the PyTest framework installed. For the
behavior-driven development part, we are going to need the pytest-bdd plugin.
pytest and pytest-bdd can be installed using the following command:
$ pip install pytest pytest-bdd
The examples have been written on Python 3.7, pytest 6.0.2, and pytest-bdd 4.0.1, but
should work on most modern Python versions. You can find the code files present in this
chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Software-​with-​Python/​tree/​main/​Chapter07.
Writing acceptance tests
Our company has just released a new product; it's a mobile phone for extreme geeks that
will only work through a UNIX shell. All the things our users want to do will be doable via
the command line and we are tasked with writing the contact book application. Where do
we start?
The usual way! First, we prepare our project skeleton. We are going to expose the contact
book application as the contacts package, as shown here, and we are going to provide a
main entry point. For now, we are going to invoke this with python -m contacts, but in
the future, we will wrap this in a more convenient shortcut:
.
├── src
│   ├── contacts
│   │   ├── __init__.py
│   │   └── __main__.py
│   └── setup.py
└── tests
    ├── conftest.py
    ├── functional
    │   └── test_acceptance.py
    ├── __init__.py
    └── unit
For now, all our modules are empty, just placeholders are present, but the first thing we
surely want to have is a location where we can place our acceptance tests. So, the
test_acceptance module is born. Now, how do we populate it?


---
**Page 166**

Fitness Function with a Contact Book Application
Chapter 7
[ 166 ]
Our team applies an agile approach, so we have a bunch of user stories like stickers, with
things such as As a user, I want to have a command to add a new entry to my contact book, so that
I can then call it without having to remember the number, or As a user, I want to have a way to
remove contacts that I no longer require from my contact book, so that it doesn't get too hard to spot
the contacts I care about. While they might be enough for us to start imagining what the
application is meant to do, they are far from being something that describes its behavior
well enough to act as a fitness function.
So we pick one story, the one about being able to add new entries to the contact book
application, and we start writing a set of acceptance tests for it that can describe its
behavior in a more detailed way.
Writing the first test
So, we open the tests/functional/test_acceptance.py file and we write our first
acceptance test. It has to run some kind of command line and then check that after a contact
has been added to the list of contacts:
import contacts
class TestAddingEntries:
    def test_basic(self):
        app = contacts.Application()
        app.run("contacts add NAME 3345554433")
        assert app._contacts == [
            ("NAME", "3345554433")
        ]
We decide that Application.run will be the entry point of our application, so we just
pass what the user wrote on the shell and it gets parsed and executed, and also decide that
we are going to somehow store the contacts in a _contacts list. That's an implementation
detail that we can change later on as we dive into the details of implementation, but for
now it is enough to state that somehow we want to be able to see the contacts that we
stored.
Acceptance tests are meant to exercise the system from the user point of
view and through the interfaces provided to the user. However, it is
generally considered acceptable if the setup and assertion parts of the test
access internals to properly prepare the test or verify its outcome. The
important part is that the system is used from the user point of view.


