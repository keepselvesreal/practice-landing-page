# Chapter 7: Fitness Function with a Contact Book Application (pp.164-188)

---
**Page 164**

7
Fitness Function with a Contact
Book Application
We have already seen that in test-driven development, it is common to start development
by designing and writing acceptance tests to define what the software should do and then
dive into the details of how to do it with lower-level tests. That frequently is the foundation
of Acceptance Test-Driven Development (ATDD), but more generally, what we are trying
to do is to define a Fitness Function for our whole software. A fitness function is a function
that, given any kind of solution, tells us how good it is; the better the fitness function, the
closer we get to the result.
Even though fitness functions are typically used in genetic programming to select the
solutions that should be moved forward to the next iteration, we can see our acceptance
tests as a big fitness function that takes the whole software as the input and gives us back a
value of how good the software is.
All acceptance tests passed? This is 100% what it was meant to be, while only 50% of
acceptance tests have been passed? That's half-broken... As far as our fitness function really
describes what we wanted, it can save us from shipping the wrong application.
That's why acceptance tests are one of the most important pieces of our test suite and a test
suite comprised solely of unit tests (or, more generally, technical tests) can't really
guarantee that our software is aligned with what the business really wanted. Yes, it might
do what the developer wanted, but not what the business wanted.
In this chapter, we will cover the following topics:
Writing acceptance tests
Using behavior-driven development
Embracing specifications by example


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


---
**Page 167**

Fitness Function with a Contact Book Application
Chapter 7
[ 167 ]
Satisfied with the fact that we are now clear in our mind how we want the software to
behave at a high level, we are eager to jump into the implementation. But remember that
our acceptance tests are only as good because they are a proper fitness function.
Getting feedback from the product team
Our next step is to go back to someone from our product team and share our acceptance
test with one of its members to see how good it is.
Luckily for us, our product team understands Python and they get back with a few points
as feedback:
People usually have a name and a surname and even middle names, so what
happens when NAME contains spaces?
We actually want to be able to store international numbers, so make sure you
accept a "+" at the beginning of the phone numbers, but don't accept any
random text. We don't want people wondering why their contacts don't work
after they did a typo.
These points are all new acceptance criteria. Our software is good only if it's able to satisfy
all these conditions. So, we go back to our editor and tweak our acceptance tests and we
come back with the following:
class TestAddingEntries:
    def test_basic(self):
        app = contacts.Application()
        app.run("contacts add NAME 3345554433")
        assert app._contacts == [
            ("NAME", "3345554433")
        ]
    def test_surnames(self):
        app = contacts.Application()
        app.run("contacts add Mario Mario 3345554433")
        app.run("contacts add Luigi Mario 3345554434")
        app.run("contacts add Princess Peach Toadstool 3339323323")
        assert app._contacts == [
            ("Mario Mario", "3345554433"),
            ("Luigi Mario", "3345554434"),
            ("Princess Peach Toadstool", "3339323323")


---
**Page 168**

Fitness Function with a Contact Book Application
Chapter 7
[ 168 ]
        ]
    def test_international_numbers(self):
        app = contacts.Application()
        app.run("contacts add NAME +393345554433")
        assert app._contacts == [
            ("NAME", "+393345554433")
        ]
    def test_invalid_strings(self):
        app = contacts.Application()
        app.run("contacts add NAME InvalidString")
        assert app._contacts == []
The test_surnames function now verifies that names with spaces work as expected, and
that we also support multiple spaces for middle names and multiple surnames.
The test_international_numbers function now verifies that we support international
phone numbers, while the test_invalid_strings function confirms that we don't save
invalid numbers.
This should cover a fairly comprehensive description of all the behaviors our product team
mentioned. Before declaring victory, we go back to our product people and review the
acceptance tests with them.
One of the product team members points out that a key feature for them is that contacts
have to be retained between two different runs of the application. As obvious as that might
sound, our acceptance tests don't in any way exercise that condition, and so is an
insufficient fitness function. A sub-optimal solution that lacks a major capability, such as
loading back the contacts when you run the app the second time, would still pass all our
tests and thus get the same grade as the optimal solution.
Back to our chair, we tweak our acceptance tests and add one more test that verifies that
loading back contacts leads to the same exact list of contacts that we had before:
class TestAddingEntries:
    ...
    def test_reload(self):
        app = contacts.Application()
        app.run("contacts add NAME 3345554433")


---
**Page 169**

Fitness Function with a Contact Book Application
Chapter 7
[ 169 ]
        assert app._contacts == [
            ("NAME", "3345554433")
        ]
        app._clear()
        app.load()
        assert app._contacts == [
            ("NAME", "3345554433")
        ]
The test_reload function largely behaves like our test_basic function up to the point
where it clears any list of contacts currently loaded and then loads it again.
Note that we are not testing whether Application._clear does actually
clear the list of contacts. In acceptance tests, we can take it for granted that
the functions we invoke do what they are meant to do, but what we are
interested in is testing the overall behavior and not how the
implementation works.
The functional and units tests will verify for us whether the functions
actually work as expected. From the acceptance tests, we can just use
those functions, taking it for granted that they do work.
Now it is time for one more review with someone who has the goals of the software clear in
mind and we can confirm that the acceptance tests now look good and cover what everyone
wanted. The implementation can now start!
Making the test pass
Running our current test suite obviously fails because we have not yet implemented
anything:
$ pytest -v
...
.../test_acceptance.py::TestAddingEntries::test_basic FAILED [ 25%]
.../test_acceptance.py::TestAddingEntries::test_surnames FAILED [ 50%]
.../test_acceptance.py::TestAddingEntries::test_international_numbers
FAILED [ 75%]
.../test_acceptance.py::TestAddingEntries::test_reload FAILED [100%]
...
    def test_basic(self):
> app = contacts.Application()
E AttributeError: module 'contacts' has no attribute 'Application'


---
**Page 170**

Fitness Function with a Contact Book Application
Chapter 7
[ 170 ]
The failed tests point us in the direction that we want to start by implementing the
Application itself, so we can create our tests/unit/test_application.py file and
we can start thinking about what the application is and what it should do.
As usual, we start by writing a bunch of functional and unit tests that drive our coding and
testing strategies as we also grow the implementation. We then continue to add more unit
and functional tests and implementation code until all our tests and acceptance tests pass:
$ pytest -v
functional/test_acceptance.py::TestAddingEntries::test_basic PASSED [ 5%]
functional/test_acceptance.py::TestAddingEntries::test_surnames PASSED [
10%]
functional/test_acceptance.py::TestAddingEntries::test_international_number
s PASSED [ 15%]
functional/test_acceptance.py::TestAddingEntries::test_invalid_strings
PASSED [ 20%]
functional/test_acceptance.py::TestAddingEntries::test_reload PASSED [ 25%]
unit/test_adding.py::TestAddContacts::test_basic PASSED [ 30%]
unit/test_adding.py::TestAddContacts::test_special PASSED [ 35%]
unit/test_adding.py::TestAddContacts::test_international PASSED [ 40%]
unit/test_adding.py::TestAddContacts::test_invalid PASSED [ 45%]
unit/test_adding.py::TestAddContacts::test_short PASSED [ 50%]
unit/test_adding.py::TestAddContacts::test_missing PASSED [ 55%]
unit/test_application.py::test_application PASSED [ 60%]
unit/test_application.py::test_clear PASSED [ 65%]
unit/test_application.py::TestRun::test_add PASSED [ 70%]
unit/test_application.py::TestRun::test_add_surname PASSED [ 75%]
unit/test_application.py::TestRun::test_empty PASSED [ 80%]
unit/test_application.py::TestRun::test_nocmd PASSED [ 85%]
unit/test_application.py::TestRun::test_invalid PASSED [ 90%]
unit/test_persistence.py::TestLoading::test_load PASSED [ 95%]
unit/test_persistence.py::TestSaving::test_save PASSED [100%]
For the sake of shortness, I won't report the implementation of all the tests that comprise
our test suite. You can imagine that all unit tests had the purpose of checking the overall
implementation and some specific corner cases.
The implementation of our Application class is fairly minimal. As we are going to evolve
it with more tests in the next sections, we will make the implementation available here,
allowing you to have a better understanding of the next sections:
class Application:
    PHONE_EXPR = re.compile('^[+]?[0-9]{3,}$')
    def __init__(self):
        self._clear()


---
**Page 171**

Fitness Function with a Contact Book Application
Chapter 7
[ 171 ]
    def _clear(self):
        self._contacts = []
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
        else:
            raise ValueError(f"Invalid command: {cmd}")
    def save(self):
        with open("contacts.json", "w+") as f:
            json.dump({"_contacts": self._contacts}, f)
    def load(self):
        with open("contacts.json") as f:
            self._contacts = [
                tuple(t) for t in json.load(f)["_contacts"]
            ]
    def add(self, name, phonenum):
        if not isinstance(phonenum, str):
            raise ValueError("A valid phone number is required")
        if not self.PHONE_EXPR.match(phonenum):
            raise ValueError(f"Invalid phone number: {phonenum}")
        self._contacts.append((name, phonenum))
        self.save()
The Application.add method is the one that is explicitly in charge of adding new
contacts to the contacts list, and it's what most of our tests rely on when they want to add
new contacts. The Application.save and Application.load methods are now in
charge of adding a persistence layer to the application. For the sake of simplicity, we just
store the contacts in a JSON file (in the real world, you might want to change where the
contacts are saved or make it configurable, but for our example, they will just be saved
locally where the command is invoked from).


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


---
**Page 188**

8
PyTest Essential Plugins
In the previous chapter, we saw how to work with PyTest and pytest-bdd to create
acceptance tests and verify the requirements of our software.
However, pytest-bdd is not the only useful plugin that PyTest has. In this chapter, we are
going to continue working on the contacts project introduced in Chapter 7, Fitness Function
with a Contact Book Application, showing how some of the most commonly used PyTest
plugins can help during the development of a project.
The plugins we are going to cover in this chapter are going to help us with verifying our
test suite coverage of the application code, checking the performance of our application,
dealing with tests that are flaky or unstable, and optimizing our development process by
running only the impacted tests when we change the code base or by speeding up our
whole test suite execution.
In this chapter, we will cover the following topics:
Using pytest-cov for coverage reporting
Using pytest-benchmark for benchmarking
Using flaky to rerun unstable tests
Using pytest-testmon to rerun tests on code changes
Running tests in parallel with pytest-xdist


