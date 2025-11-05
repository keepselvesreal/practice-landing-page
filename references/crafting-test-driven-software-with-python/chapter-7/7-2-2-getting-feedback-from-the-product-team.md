# 7.2.2 Getting feedback from the product team (pp.167-169)

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


