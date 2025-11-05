# 7.2.1 Writing the first test (pp.166-167)

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


