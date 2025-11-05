# 7.2.3 Making the test pass (pp.169-172)

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


