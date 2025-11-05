# 7.3.6 Assessing conditions with the Then step (pp.177-178)

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


