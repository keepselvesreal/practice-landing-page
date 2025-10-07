Line 1: 
Line 2: --- 페이지 174 ---
Line 3: 7
Line 4: Fitness Function with a Contact
Line 5: Book Application
Line 6: We have already seen that in test-driven development, it is common to start development
Line 7: by designing and writing acceptance tests to define what the software should do and then
Line 8: dive into the details of how to do it with lower-level tests. That frequently is the foundation
Line 9: of Acceptance Test-Driven Development (ATDD), but more generally, what we are trying
Line 10: to do is to define a Fitness Function for our whole software. A fitness function is a function
Line 11: that, given any kind of solution, tells us how good it is; the better the fitness function, the
Line 12: closer we get to the result.
Line 13: Even though fitness functions are typically used in genetic programming to select the
Line 14: solutions that should be moved forward to the next iteration, we can see our acceptance
Line 15: tests as a big fitness function that takes the whole software as the input and gives us back a
Line 16: value of how good the software is.
Line 17: All acceptance tests passed? This is 100% what it was meant to be, while only 50% of
Line 18: acceptance tests have been passed? That's half-broken... As far as our fitness function really
Line 19: describes what we wanted, it can save us from shipping the wrong application.
Line 20: That's why acceptance tests are one of the most important pieces of our test suite and a test
Line 21: suite comprised solely of unit tests (or, more generally, technical tests) can't really
Line 22: guarantee that our software is aligned with what the business really wanted. Yes, it might
Line 23: do what the developer wanted, but not what the business wanted.
Line 24: In this chapter, we will cover the following topics:
Line 25: Writing acceptance tests
Line 26: Using behavior-driven development
Line 27: Embracing specifications by example
Line 28: 
Line 29: --- 페이지 175 ---
Line 30: Fitness Function with a Contact Book Application
Line 31: Chapter 7
Line 32: [ 165 ]
Line 33: Technical requirements
Line 34: We need a working Python interpreter with the PyTest framework installed. For the
Line 35: behavior-driven development part, we are going to need the pytest-bdd plugin.
Line 36: pytest and pytest-bdd can be installed using the following command:
Line 37: $ pip install pytest pytest-bdd
Line 38: The examples have been written on Python 3.7, pytest 6.0.2, and pytest-bdd 4.0.1, but
Line 39: should work on most modern Python versions. You can find the code files present in this
Line 40: chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Line 41: Software-​with-​Python/​tree/​main/​Chapter07.
Line 42: Writing acceptance tests
Line 43: Our company has just released a new product; it's a mobile phone for extreme geeks that
Line 44: will only work through a UNIX shell. All the things our users want to do will be doable via
Line 45: the command line and we are tasked with writing the contact book application. Where do
Line 46: we start?
Line 47: The usual way! First, we prepare our project skeleton. We are going to expose the contact
Line 48: book application as the contacts package, as shown here, and we are going to provide a
Line 49: main entry point. For now, we are going to invoke this with python -m contacts, but in
Line 50: the future, we will wrap this in a more convenient shortcut:
Line 51: .
Line 52: ├── src
Line 53: │   ├── contacts
Line 54: │   │   ├── __init__.py
Line 55: │   │   └── __main__.py
Line 56: │   └── setup.py
Line 57: └── tests
Line 58:     ├── conftest.py
Line 59:     ├── functional
Line 60:     │   └── test_acceptance.py
Line 61:     ├── __init__.py
Line 62:     └── unit
Line 63: For now, all our modules are empty, just placeholders are present, but the first thing we
Line 64: surely want to have is a location where we can place our acceptance tests. So, the
Line 65: test_acceptance module is born. Now, how do we populate it?
Line 66: 
Line 67: --- 페이지 176 ---
Line 68: Fitness Function with a Contact Book Application
Line 69: Chapter 7
Line 70: [ 166 ]
Line 71: Our team applies an agile approach, so we have a bunch of user stories like stickers, with
Line 72: things such as As a user, I want to have a command to add a new entry to my contact book, so that
Line 73: I can then call it without having to remember the number, or As a user, I want to have a way to
Line 74: remove contacts that I no longer require from my contact book, so that it doesn't get too hard to spot
Line 75: the contacts I care about. While they might be enough for us to start imagining what the
Line 76: application is meant to do, they are far from being something that describes its behavior
Line 77: well enough to act as a fitness function.
Line 78: So we pick one story, the one about being able to add new entries to the contact book
Line 79: application, and we start writing a set of acceptance tests for it that can describe its
Line 80: behavior in a more detailed way.
Line 81: Writing the first test
Line 82: So, we open the tests/functional/test_acceptance.py file and we write our first
Line 83: acceptance test. It has to run some kind of command line and then check that after a contact
Line 84: has been added to the list of contacts:
Line 85: import contacts
Line 86: class TestAddingEntries:
Line 87:     def test_basic(self):
Line 88:         app = contacts.Application()
Line 89:         app.run("contacts add NAME 3345554433")
Line 90:         assert app._contacts == [
Line 91:             ("NAME", "3345554433")
Line 92:         ]
Line 93: We decide that Application.run will be the entry point of our application, so we just
Line 94: pass what the user wrote on the shell and it gets parsed and executed, and also decide that
Line 95: we are going to somehow store the contacts in a _contacts list. That's an implementation
Line 96: detail that we can change later on as we dive into the details of implementation, but for
Line 97: now it is enough to state that somehow we want to be able to see the contacts that we
Line 98: stored.
Line 99: Acceptance tests are meant to exercise the system from the user point of
Line 100: view and through the interfaces provided to the user. However, it is
Line 101: generally considered acceptable if the setup and assertion parts of the test
Line 102: access internals to properly prepare the test or verify its outcome. The
Line 103: important part is that the system is used from the user point of view.
Line 104: 
Line 105: --- 페이지 177 ---
Line 106: Fitness Function with a Contact Book Application
Line 107: Chapter 7
Line 108: [ 167 ]
Line 109: Satisfied with the fact that we are now clear in our mind how we want the software to
Line 110: behave at a high level, we are eager to jump into the implementation. But remember that
Line 111: our acceptance tests are only as good because they are a proper fitness function.
Line 112: Getting feedback from the product team
Line 113: Our next step is to go back to someone from our product team and share our acceptance
Line 114: test with one of its members to see how good it is.
Line 115: Luckily for us, our product team understands Python and they get back with a few points
Line 116: as feedback:
Line 117: People usually have a name and a surname and even middle names, so what
Line 118: happens when NAME contains spaces?
Line 119: We actually want to be able to store international numbers, so make sure you
Line 120: accept a "+" at the beginning of the phone numbers, but don't accept any
Line 121: random text. We don't want people wondering why their contacts don't work
Line 122: after they did a typo.
Line 123: These points are all new acceptance criteria. Our software is good only if it's able to satisfy
Line 124: all these conditions. So, we go back to our editor and tweak our acceptance tests and we
Line 125: come back with the following:
Line 126: class TestAddingEntries:
Line 127:     def test_basic(self):
Line 128:         app = contacts.Application()
Line 129:         app.run("contacts add NAME 3345554433")
Line 130:         assert app._contacts == [
Line 131:             ("NAME", "3345554433")
Line 132:         ]
Line 133:     def test_surnames(self):
Line 134:         app = contacts.Application()
Line 135:         app.run("contacts add Mario Mario 3345554433")
Line 136:         app.run("contacts add Luigi Mario 3345554434")
Line 137:         app.run("contacts add Princess Peach Toadstool 3339323323")
Line 138:         assert app._contacts == [
Line 139:             ("Mario Mario", "3345554433"),
Line 140:             ("Luigi Mario", "3345554434"),
Line 141:             ("Princess Peach Toadstool", "3339323323")
Line 142: 
Line 143: --- 페이지 178 ---
Line 144: Fitness Function with a Contact Book Application
Line 145: Chapter 7
Line 146: [ 168 ]
Line 147:         ]
Line 148:     def test_international_numbers(self):
Line 149:         app = contacts.Application()
Line 150:         app.run("contacts add NAME +393345554433")
Line 151:         assert app._contacts == [
Line 152:             ("NAME", "+393345554433")
Line 153:         ]
Line 154:     def test_invalid_strings(self):
Line 155:         app = contacts.Application()
Line 156:         app.run("contacts add NAME InvalidString")
Line 157:         assert app._contacts == []
Line 158: The test_surnames function now verifies that names with spaces work as expected, and
Line 159: that we also support multiple spaces for middle names and multiple surnames.
Line 160: The test_international_numbers function now verifies that we support international
Line 161: phone numbers, while the test_invalid_strings function confirms that we don't save
Line 162: invalid numbers.
Line 163: This should cover a fairly comprehensive description of all the behaviors our product team
Line 164: mentioned. Before declaring victory, we go back to our product people and review the
Line 165: acceptance tests with them.
Line 166: One of the product team members points out that a key feature for them is that contacts
Line 167: have to be retained between two different runs of the application. As obvious as that might
Line 168: sound, our acceptance tests don't in any way exercise that condition, and so is an
Line 169: insufficient fitness function. A sub-optimal solution that lacks a major capability, such as
Line 170: loading back the contacts when you run the app the second time, would still pass all our
Line 171: tests and thus get the same grade as the optimal solution.
Line 172: Back to our chair, we tweak our acceptance tests and add one more test that verifies that
Line 173: loading back contacts leads to the same exact list of contacts that we had before:
Line 174: class TestAddingEntries:
Line 175:     ...
Line 176:     def test_reload(self):
Line 177:         app = contacts.Application()
Line 178:         app.run("contacts add NAME 3345554433")
Line 179: 
Line 180: --- 페이지 179 ---
Line 181: Fitness Function with a Contact Book Application
Line 182: Chapter 7
Line 183: [ 169 ]
Line 184:         assert app._contacts == [
Line 185:             ("NAME", "3345554433")
Line 186:         ]
Line 187:         app._clear()
Line 188:         app.load()
Line 189:         assert app._contacts == [
Line 190:             ("NAME", "3345554433")
Line 191:         ]
Line 192: The test_reload function largely behaves like our test_basic function up to the point
Line 193: where it clears any list of contacts currently loaded and then loads it again.
Line 194: Note that we are not testing whether Application._clear does actually
Line 195: clear the list of contacts. In acceptance tests, we can take it for granted that
Line 196: the functions we invoke do what they are meant to do, but what we are
Line 197: interested in is testing the overall behavior and not how the
Line 198: implementation works.
Line 199: The functional and units tests will verify for us whether the functions
Line 200: actually work as expected. From the acceptance tests, we can just use
Line 201: those functions, taking it for granted that they do work.
Line 202: Now it is time for one more review with someone who has the goals of the software clear in
Line 203: mind and we can confirm that the acceptance tests now look good and cover what everyone
Line 204: wanted. The implementation can now start!
Line 205: Making the test pass
Line 206: Running our current test suite obviously fails because we have not yet implemented
Line 207: anything:
Line 208: $ pytest -v
Line 209: ...
Line 210: .../test_acceptance.py::TestAddingEntries::test_basic FAILED [ 25%]
Line 211: .../test_acceptance.py::TestAddingEntries::test_surnames FAILED [ 50%]
Line 212: .../test_acceptance.py::TestAddingEntries::test_international_numbers
Line 213: FAILED [ 75%]
Line 214: .../test_acceptance.py::TestAddingEntries::test_reload FAILED [100%]
Line 215: ...
Line 216:     def test_basic(self):
Line 217: > app = contacts.Application()
Line 218: E AttributeError: module 'contacts' has no attribute 'Application'
Line 219: 
Line 220: --- 페이지 180 ---
Line 221: Fitness Function with a Contact Book Application
Line 222: Chapter 7
Line 223: [ 170 ]
Line 224: The failed tests point us in the direction that we want to start by implementing the
Line 225: Application itself, so we can create our tests/unit/test_application.py file and
Line 226: we can start thinking about what the application is and what it should do.
Line 227: As usual, we start by writing a bunch of functional and unit tests that drive our coding and
Line 228: testing strategies as we also grow the implementation. We then continue to add more unit
Line 229: and functional tests and implementation code until all our tests and acceptance tests pass:
Line 230: $ pytest -v
Line 231: functional/test_acceptance.py::TestAddingEntries::test_basic PASSED [ 5%]
Line 232: functional/test_acceptance.py::TestAddingEntries::test_surnames PASSED [
Line 233: 10%]
Line 234: functional/test_acceptance.py::TestAddingEntries::test_international_number
Line 235: s PASSED [ 15%]
Line 236: functional/test_acceptance.py::TestAddingEntries::test_invalid_strings
Line 237: PASSED [ 20%]
Line 238: functional/test_acceptance.py::TestAddingEntries::test_reload PASSED [ 25%]
Line 239: unit/test_adding.py::TestAddContacts::test_basic PASSED [ 30%]
Line 240: unit/test_adding.py::TestAddContacts::test_special PASSED [ 35%]
Line 241: unit/test_adding.py::TestAddContacts::test_international PASSED [ 40%]
Line 242: unit/test_adding.py::TestAddContacts::test_invalid PASSED [ 45%]
Line 243: unit/test_adding.py::TestAddContacts::test_short PASSED [ 50%]
Line 244: unit/test_adding.py::TestAddContacts::test_missing PASSED [ 55%]
Line 245: unit/test_application.py::test_application PASSED [ 60%]
Line 246: unit/test_application.py::test_clear PASSED [ 65%]
Line 247: unit/test_application.py::TestRun::test_add PASSED [ 70%]
Line 248: unit/test_application.py::TestRun::test_add_surname PASSED [ 75%]
Line 249: unit/test_application.py::TestRun::test_empty PASSED [ 80%]
Line 250: unit/test_application.py::TestRun::test_nocmd PASSED [ 85%]
Line 251: unit/test_application.py::TestRun::test_invalid PASSED [ 90%]
Line 252: unit/test_persistence.py::TestLoading::test_load PASSED [ 95%]
Line 253: unit/test_persistence.py::TestSaving::test_save PASSED [100%]
Line 254: For the sake of shortness, I won't report the implementation of all the tests that comprise
Line 255: our test suite. You can imagine that all unit tests had the purpose of checking the overall
Line 256: implementation and some specific corner cases.
Line 257: The implementation of our Application class is fairly minimal. As we are going to evolve
Line 258: it with more tests in the next sections, we will make the implementation available here,
Line 259: allowing you to have a better understanding of the next sections:
Line 260: class Application:
Line 261:     PHONE_EXPR = re.compile('^[+]?[0-9]{3,}$')
Line 262:     def __init__(self):
Line 263:         self._clear()
Line 264: 
Line 265: --- 페이지 181 ---
Line 266: Fitness Function with a Contact Book Application
Line 267: Chapter 7
Line 268: [ 171 ]
Line 269:     def _clear(self):
Line 270:         self._contacts = []
Line 271:     def run(self, text):
Line 272:         text = text.strip()
Line 273:         _, cmd = text.split(maxsplit=1)
Line 274:         cmd, args = cmd.split(maxsplit=1)
Line 275:         if cmd == "add":
Line 276:             name, num = args.rsplit(maxsplit=1)
Line 277:             try:
Line 278:                 self.add(name, num)
Line 279:             except ValueError as err:
Line 280:                 print(err)
Line 281:                 return
Line 282:         else:
Line 283:             raise ValueError(f"Invalid command: {cmd}")
Line 284:     def save(self):
Line 285:         with open("contacts.json", "w+") as f:
Line 286:             json.dump({"_contacts": self._contacts}, f)
Line 287:     def load(self):
Line 288:         with open("contacts.json") as f:
Line 289:             self._contacts = [
Line 290:                 tuple(t) for t in json.load(f)["_contacts"]
Line 291:             ]
Line 292:     def add(self, name, phonenum):
Line 293:         if not isinstance(phonenum, str):
Line 294:             raise ValueError("A valid phone number is required")
Line 295:         if not self.PHONE_EXPR.match(phonenum):
Line 296:             raise ValueError(f"Invalid phone number: {phonenum}")
Line 297:         self._contacts.append((name, phonenum))
Line 298:         self.save()
Line 299: The Application.add method is the one that is explicitly in charge of adding new
Line 300: contacts to the contacts list, and it's what most of our tests rely on when they want to add
Line 301: new contacts. The Application.save and Application.load methods are now in
Line 302: charge of adding a persistence layer to the application. For the sake of simplicity, we just
Line 303: store the contacts in a JSON file (in the real world, you might want to change where the
Line 304: contacts are saved or make it configurable, but for our example, they will just be saved
Line 305: locally where the command is invoked from).
Line 306: 
Line 307: --- 페이지 182 ---
Line 308: Fitness Function with a Contact Book Application
Line 309: Chapter 7
Line 310: [ 172 ]
Line 311: Finally,Application.run is the user interface to our software. Given any command in the
Line 312: form "executablename command arguments", it parses it and executes the correct
Line 313: command. Currently, only add is implemented, but in the following sections, we will
Line 314: implement the del and ls commands, too.
Line 315: Now we know that acceptance tests are vital in the feedback cycle in the case of people that
Line 316: understand the goals of the software well. Next, we need to focus on how to improve that
Line 317: communication cycle. In this example we were lucky that our counterpart understood
Line 318: Python, but what if they didn't? It's probably common that the people who understand the
Line 319: business well don't know a thing about programming, and so we need a better way to set
Line 320: up our communication than using Python.
Line 321: Using behavior-driven development
Line 322: For the first phase of our contact book application, we took it for granted that the people we
Line 323: had to speak with understood the Python language well enough that we could share with
Line 324: them our acceptance tests for review and confirm that we were going in the right direction.
Line 325: While it's getting more and more common that people involved in product definition have
Line 326: at least an entry-level knowledge of programming, we can't take it for granted that every
Line 327: stakeholder we need to enter into discussions with knows Python.
Line 328: So how can we keep the same kind of feedback loop and apply the strategy of reviewing all
Line 329: our acceptance tests with other stakeholders without involving Python?
Line 330: That's what Behavior-Driven Development (BDD) tries to solve. BDD takes some concepts
Line 331: from Test-Driven Development (TDD) and Domain-Driven Design (DDD) to allow all
Line 332: stakeholders to speak the same language as the technical team.
Line 333: In the end, BDD tries to mediate between the two worlds. The language becomes English,
Line 334: instead of Python, but a more structured form of English for which, in the end, a parser can
Line 335: be written and developers embrace the business glossary (no more classes named User and
Line 336: PayingUser if the business calls them Lead and Customer) so that the tests that the
Line 337: developers write make sense for all other stakeholders, too.
Line 338: This is usually achieved by defining the tests in a language that is commonly named
Line 339: Gherkin (even though BDD doesn't strictly mandate Gherkin usage) and, luckily for us, the
Line 340: pytest-bdd plugin allows us to extend our test suite with tests written in a subset of the
Line 341: Gherkin language that coexists very well with all the other pytest plugins or features we
Line 342: might be using.
Line 343: 
Line 344: --- 페이지 183 ---
Line 345: Fitness Function with a Contact Book Application
Line 346: Chapter 7
Line 347: [ 173 ]
Line 348: Our application is able to add contacts, but it still doesn't allow us to delete or list them, so
Line 349: it's not very useful. So, the next step is to implement a delete contacts feature, and we decide
Line 350: to do so by using BDD.
Line 351: To get started using BDD, we will create a new tests/acceptance directory, where we
Line 352: are going to put all the acceptance tests for our features. Thus, the final layout of our test
Line 353: suite will appear as follows:
Line 354: └── tests
Line 355:     ├── __init__.py
Line 356:     ├── conftest.py
Line 357:     ├── acceptance
Line 358:     │   └── ...
Line 359:     ├── functional
Line 360:     │   └── test_acceptance.py
Line 361:     └── unit
Line 362:         └── ...
Line 363: Then we can create a tests/acceptance/delete_contact.feature file that will
Line 364: contain all our acceptance scenarios for the deleting contacts feature.
Line 365: Defining a feature file
Line 366: We start the file by making it clear that it covers the deletion of contacts:
Line 367: Feature: Deleting Contacts
Line 368:     Contacts added to our contact book can be removed.
Line 369: Now that we have a location where all our testing scenarios can reside, we can try to add
Line 370: the first one. The basics of the Gherkin language are fairly easy to grasp. In the end, it is
Line 371: meant to be readable by everyone without having to study a programming language. So,
Line 372: the core words are the Given, When, Then, and And keywords that start every step in our
Line 373: scenarios, and to start a new scenario we just use Scenario.
Line 374: 
Line 375: --- 페이지 184 ---
Line 376: Fitness Function with a Contact Book Application
Line 377: Chapter 7
Line 378: [ 174 ]
Line 379: Declaring the scenario
Line 380: After the feature definition, we declare that our first scenario tries to delete a basic contact
Line 381: and see that things work as expected:
Line 382: Scenario: Removing a Basic Contact
Line 383:     Given I have a contact book
Line 384:     And I have a "John" contact
Line 385:     When I run the "contacts del John" command
Line 386:     Then My contacts list is now empty
Line 387: The scenario is written in fairly plain English so that we can review with other stakeholders
Line 388: without having to understand software development or programming languages. Once we
Line 389: agree that it represents correctly what we expect from the software, then we can turn it to
Line 390: code by using pytest-bdd.
Line 391: pytest-bdd is based on PyTest itself, so each scenario is exposed as a test function. To
Line 392: signal that it's also a scenario, we add the @scenario decorator and point it to the feature
Line 393: file.
Line 394: In our tests/functional/test_acceptance.py file, we are going to add a test for our
Line 395: Removing a Basic Contact scenario that we described in the
Line 396: tests/acceptance/delete_contact.feature file using the Gherkin language:
Line 397: from pytest_bdd import scenario
Line 398: @scenario("../acceptance/delete_contact.feature",
Line 399:             "Removing a Basic Contact")
Line 400: def test_deleting_contacts():
Line 401:     pass
Line 402: Unlike the standard PyTest test, a scenario test is usually an empty function. We can
Line 403: perform additional testing within the function, but any code that we add will run after the
Line 404: scenario has been completed.
Line 405: The test itself is loaded from the feature file looking for a scenario that has the same name
Line 406: as the one we provided in the decorator (in this case,"Removing a Basic Contact").
Line 407: Then, the scenario text is parsed and each step defined in it is executed one after the other.
Line 408: But how does PyTest know what to do in order to perform the steps? Our scenario starts by
Line 409: ensuring that we have a contact book with one contact inside named "John":
Line 410: Given I have a contact book
Line 411: And I have a "John" contact
Line 412: 
Line 413: --- 페이지 185 ---
Line 414: Fitness Function with a Contact Book Application
Line 415: Chapter 7
Line 416: [ 175 ]
Line 417: How does pytest-bdd even know what a contact book is and how to add a contact to it?
Line 418: Well, it doesn't.
Line 419: Running the scenario test
Line 420: If we try to run our scenario test at this point, as shown here, PyTest will just report errors
Line 421: complaining that it doesn't know what to do with the first step that it encounters:
Line 422: $ pytest -v -k deleting
Line 423: .../test_acceptance.py::test_deleting_contacts FAILED [100%]
Line 424: ...
Line 425: StepDefinitionNotFoundError: Step definition is not found: Given "I have a
Line 426: contact book". Line 5 in scenario "Removing a Basic Contact" in the feature
Line 427: "/tests/acceptance/delete_contact.feature
Line 428: We have to tell pytest-bdd what to do when it faces a step. So, in our
Line 429: test_acceptance.py, we must provide the code that has to be executed when a step is
Line 430: met and link it to the step using the @given decorator, as shown in the following code
Line 431: block:
Line 432: from pytest_bdd import scenario, given
Line 433: @given("I have a contact book", target_fixture="contactbook")
Line 434: def contactbook():
Line 435:     return contacts.Application()
Line 436: Every time pytest-bdd finds"I have a contact book" as a step in a scenario, it will
Line 437: invoke our contactbook function. The contactbook function doesn't just tell PyTest how
Line 438: to run the step, but thanks to the target_fixture="contactbook" argument of @given,
Line 439: it's also a fixture that provides the contactbook dependency every time it is requested by
Line 440: another step. Any other step of the scenario that requires a contactbook can just refer to it
Line 441: and they will get back the Application that was created by the "I have a contact
Line 442: book" step.
Line 443: Further setup with the And step
Line 444: For now, the contact book is totally empty, but we know that the next step is to add a
Line 445: contact named "John" to it:
Line 446: And I have a "John" contact
Line 447: 
Line 448: --- 페이지 186 ---
Line 449: Fitness Function with a Contact Book Application
Line 450: Chapter 7
Line 451: [ 176 ]
Line 452: In this case, we have to tell pytest-bdd how to add contacts to a contact book and that
Line 453: John is the name of the contact that we want to add. This can be done by using another
Line 454: @given decorator (And is an alias for the previous keyword we just used):
Line 455: from pytest_bdd import parsers
Line 456: @given(parsers.parse("I have a \"{contactname}\" contact"))
Line 457: def have_a_contact(contactbook, contactname):
Line 458:     contactbook.add(contactname, "000")
Line 459: We are also relying on parsers.parse provided by pytest-bdd to let the step definition
Line 460: know that "John" is not part of the step itself, but that it's actually a variable. It can be
Line 461: John, it can be Jane, it can be any name, and they will all go to this same step. The name of
Line 462: the contact will be extracted from the step and will be passed as an argument to the
Line 463: function in charge of executing the step.
Line 464: Our function then only has to take that name and add it to the contact book. But where
Line 465: does the contact book come from? When we declared the "I have a contact book"
Line 466: step, we said that steps can also be PyTest fixtures, so when our have_a_contact function
Line 467: finds the need for a contactbook argument, the PyTest dependency injection will resolve
Line 468: it for us by providing what the contactbook fixture that was associated with the just
Line 469: executed "I have a contact book" step returned.
Line 470: Hence, to the contactbook provided by the fixture, we invoke the add method, passing
Line 471: the contactname provided by the parser. In this scenario, we don't care for phone
Line 472: numbers, so the contact is always added with "000" as its phone number.
Line 473: Performing actions with the When step
Line 474: Moving forward, our next step in the scenario is a When step. These are no longer steps
Line 475: associated with preparation for testing; they are intended to perform the actions we want to
Line 476: perform (remember the Arrange, Act, and Assert pattern? Well, we could consider the
Line 477: Given, When, and Then steps as the three BDD counterparts to the pattern):
Line 478: When I run the "contacts del John" command
Line 479: Just like the previous two steps, we are going to link a function in charge of executing the
Line 480: code that has to happen when this step is found, in this case using the pytest_bdd.when
Line 481: decorator:
Line 482: from pytest_bdd import when
Line 483: @when(parsers.parse("I run the \"{command}\" command"))
Line 484: 
Line 485: --- 페이지 187 ---
Line 486: Fitness Function with a Contact Book Application
Line 487: Chapter 7
Line 488: [ 177 ]
Line 489: def runcommand(contactbook, command):
Line 490:     contactbook.run(command)
Line 491: As we did for the have_a_contact function, runcommand needs the contactbook against
Line 492: which it has to run the command and can rely on parsers.parse to retrieve the command
Line 493: that has to be executed on the contact book.
Line 494: It's not uncommon that the Given and When steps can be reused across multiple scenarios.
Line 495: Making those steps parametric using parsers allows their implementation functions to be
Line 496: reused more frequently. In this case, we will be able to reuse the same step definition
Line 497: independently from the command we want to run, thus allowing us to implement scenarios
Line 498: for other features too, and not just for deleting contacts.
Line 499: In this case, as our step was I run the "contacts del John"command, the function
Line 500: will run the contacts del John command as this is the one we have provided in the
Line 501: step.
Line 502: Our final step in the scenario is the one meant to verify that the contact was actually deleted
Line 503: as we expect once the command is performed:
Line 504:     Then My contacts list is now empty
Line 505: Then, steps usually translate into the final assertion phase of our tests, so we are going to
Line 506: verify that the contact book is really empty.
Line 507: Assessing conditions with the Then step
Line 508: In this case, there is no need to parse anything, but our function will still need the
Line 509: contactbook for which it has to verify that it is actually empty:
Line 510: from pytest_bdd import then
Line 511: @then("My contacts book is now empty")
Line 512: def emptylist(contactbook):
Line 513:     assert contactbook._contacts == []
Line 514: Now that we have provided the entry point for our scenario and the implementation of all
Line 515: its steps, we can finally retry running our tests to confirm that the scenario actually gets
Line 516: executed:
Line 517: $ pytest -v -k deleting
Line 518: .../test_acceptance.py::test_deleting_contacts FAILED [100%]
Line 519: ...
Line 520: 
Line 521: --- 페이지 188 ---
Line 522: Fitness Function with a Contact Book Application
Line 523: Chapter 7
Line 524: [ 178 ]
Line 525: E ValueError: Invalid command: del
Line 526: src/contacts/__init__.py:27: ValueError
Line 527: Our scenario steps were all properly executed, but, as expected, our test has not passed. It
Line 528: choked on the When I run the "contacts del John"command step because our
Line 529: contacts application doesn't yet recognize the del command.
Line 530: Making the scenario pass
Line 531: So, our next steps will involve diving into the functional and unit tests that we need to
Line 532: define how the del command has to behave while providing an implementation for it.
Line 533: As that's a part that we already know from the previous chapters of the book, we are going
Line 534: to provide the final resulting implementation here directly:
Line 535: class Application:
Line 536:     ...
Line 537:     def run(self, text):
Line 538:         text = text.strip()
Line 539:         _, cmd = text.split(maxsplit=1)
Line 540:         cmd, args = cmd.split(maxsplit=1)
Line 541:         if cmd == "add":
Line 542:             name, num = args.rsplit(maxsplit=1)
Line 543:             try:
Line 544:                 self.add(name, num)
Line 545:             except ValueError as err:
Line 546:                 print(err)
Line 547:                 return
Line 548:         elif cmd == "del":
Line 549:             self.delete(args)
Line 550:         else:
Line 551:             raise ValueError(f"Invalid command: {cmd}")
Line 552:     ...
Line 553:     def delete(self, name):
Line 554:         self._contacts = [
Line 555:             c for c in self._contacts if c[0] != name
Line 556:         ]
Line 557:         self.save()
Line 558: 
Line 559: --- 페이지 189 ---
Line 560: Fitness Function with a Contact Book Application
Line 561: Chapter 7
Line 562: [ 179 ]
Line 563: Now that our implementation is in place and the "del" command is dispatched to the
Line 564: Application.delete function, it will remove anyone matching the provided name from
Line 565: the list of contacts. We can check that our acceptance test passes and that our contacts book
Line 566: application is actually doing what we meant it to do:
Line 567: $ pytest -v -k deleting
Line 568: .../test_acceptance.py::test_deleting_contacts   PASSED [100%]
Line 569: ...
Line 570: Our scenario was executed and our implementation satisfied it. The steps were executed by
Line 571: the functions we provided in our test_acceptance.py file:
Line 572: @scenario("../acceptance/delete_contact.feature",
Line 573:             "Removing a Basic Contact")
Line 574: def test_deleting_contacts():
Line 575:     pass
Line 576: @given("I have a contact book", target_fixture="contactbook")
Line 577: def contactbook():
Line 578:     return contacts.Application()
Line 579: @given(parsers.parse("I have a \"{contactname}\" contact"))
Line 580: def have_a_contact(contactbook, contactname):
Line 581:     contactbook.add(contactname, "000")
Line 582: @when(parsers.parse("I run the \"{command}\" command"))
Line 583: def runcommand(contactbook, command):
Line 584:     contactbook.run(command)
Line 585: @then("My contacts book is now empty")
Line 586: def emptylist(contactbook):
Line 587:     assert contactbook._contacts == []
Line 588: The problem with this approach is that if we have multiple scenarios, then it can tend to get
Line 589: confusing. It's already hard to spot out of the box the order of execution of this code, or the
Line 590: relations between the functions. We would have to constantly jump back and forth to the
Line 591: .feature file in order to understand what's going on.
Line 592: This is especially the case if we have multiple different scenarios from unrelated features
Line 593: that can become hard to navigate, making it difficult to even distinguish between scenarios
Line 594: that are related to the same feature.
Line 595: 
Line 596: --- 페이지 190 ---
Line 597: Fitness Function with a Contact Book Application
Line 598: Chapter 7
Line 599: [ 180 ]
Line 600: For this reason, people tend to split the features into multiple Python modules. Each
Line 601: Python module will contain the functions implementing the scenarios and steps that are
Line 602: only related to that, usually leading to a layout that is similar to
Line 603: tests/acceptance/deleting_contacts.py,
Line 604: tests/acceptance/adding_contacts.py, and so on.
Line 605: Now that we know how to write acceptance tests in a more shareable way, we are going to
Line 606: lower the barrier of how easy they are to understand and verify for a human by introducing
Line 607: specification by example, a practice that tries to ensure that what the software has to do is
Line 608: not only expressed and verified, but that it is also expressed in a way that is less subject to
Line 609: misunderstandings.
Line 610: With BDD, we might all agree on what's written in the acceptance tests and say that it
Line 611: expresses perfectly the specifications of our software, but the translation phase from the
Line 612: Gherkin syntax to code based tests can lead to misunderstandings. Specifications by
Line 613: example try to solve these kinds of issues by relying on clear examples that should be hard
Line 614: to misunderstand and by providing multiple examples for each scenario to further reduce
Line 615: doubts.
Line 616: Embracing specifications by example
Line 617: A common problem with acceptance tests is that it takes some effort to understand what's
Line 618: going on. If you are not already familiar with the domain, it can be easy to misunderstand
Line 619: them, thus leading to the wrong checks being performed even if everyone that reviewed it
Line 620: agreed with the original acceptance tests.
Line 621: For example, if I read an acceptance test such as the following:
Line 622: Given a first number 2
Line 623: And a second number 3
Line 624: When I run the software
Line 625: Then I get 3 as the output
Line 626: I might be tempted to understand it as, Oh, ok! The test is meant to verify that given two
Line 627: numbers, we print the highest one.
Line 628: But that might not be the requirement; the requirement might actually be, Given two
Line 629: numbers, print the lowest one plus one. How can I understand which one that test was actually
Line 630: meant to verify?
Line 631: The answer is to provide more examples. The more examples we provide for our tests, the
Line 632: easier it is to understand them.
Line 633: 
Line 634: --- 페이지 191 ---
Line 635: Fitness Function with a Contact Book Application
Line 636: Chapter 7
Line 637: [ 181 ]
Line 638: Examples are provided in a table-like format, where columns are meant to show the data
Line 639: involved in our examples and the resulting outcomes. In general, we can say that the
Line 640: columns should describe the state of the system for that example:
Line 641: Number1 | Number2 | Result
Line 642:    2    |    3    |   3
Line 643: If, by having only 2 and 3 as numbers and 3 as the result, both understandings of the test
Line 644: would be acceptable, the moment I expand my examples with one more, it becomes
Line 645: immediately obvious which one of the two I meant.
Line 646: So we can add one more row to our examples table to add an example that further reduces
Line 647: the uncertainty regarding what the expected behavior is:
Line 648: Number1 | Number2 | Result
Line 649:    2    |    3    |   3
Line 650:    5    |    7    |   6
Line 651: The second example makes it possible to understand that we are not printing the highest of
Line 652: the two numbers, but that we are actually printing the lowest plus one.
Line 653: What if I have further doubts? Maybe it's not the lowest plus one; maybe it's the first of the
Line 654: two numbers plus one!
Line 655: Number1 | Number2 | Result
Line 656:    2    |    3    |   3
Line 657:    5    |    7    |   6
Line 658:    8    |    4    |   5
Line 659: With the third example, we made it clear that we actually want the lowest of the two
Line 660: numbers and not the first one. Just add more examples until the reading of the test becomes
Line 661: fairly obvious for every reader.
Line 662: That's the core idea behind specification by example: the behavior of a software can be
Line 663: described by providing enough examples that make it obvious to see what's going on.
Line 664: Instead of having to write tens of pages trying to explain what's happening, given enough
Line 665: examples, which can be automatically verified, the reader can easily see what's going on.
Line 666: Generally, there are many benefits to this approach, including the following:
Line 667: We don't have the specification and the test: the specifications are testable by
Line 668: definition.
Line 669: Tests that were easy to misunderstand can easily be made more obvious by
Line 670: adding more examples, which are cheaper to add than more tests.
Line 671: 
Line 672: --- 페이지 192 ---
Line 673: Fitness Function with a Contact Book Application
Line 674: Chapter 7
Line 675: [ 182 ]
Line 676: You can't change the behavior of the software without updating the
Line 677: specifications. The specifications are the examples used to verify the software; if
Line 678: they don't verify, then the updated tests would not pass.
Line 679: As the specifications are meant to be human-readable, the Gherkin language is a good
Line 680: foundation for writing the specifications themselves making sure that they can be verified.
Line 681: We just need to add a section where we provide a list of all the possible examples for a
Line 682: scenario.
Line 683: For example, we might write the final feature of our software: Listing the contacts using this
Line 684: model. To do so, let's write a scenario with two examples of possible contact lists to print:
Line 685: Feature: Listing Contacts
Line 686:     Contacts added to our contact book can be listed back.
Line 687: Scenario: Listing Added Contacts
Line 688:     Given I have a contact book
Line 689:     And I have a first <first> contact
Line 690:     And I have a second <second> contact
Line 691:     When I run the "contacts ls" command
Line 692:     Then the output contains <listed_contacts> contacts
Line 693:     Examples:
Line 694:     | first | second | listed_contacts |
Line 695:     | Mario | Luigi  | Mario,Luigi     |
Line 696:     | John  | Jane   | John,Jane       |
Line 697: Compared to the scenarios we wrote before, the main difference is that we used some
Line 698: placeholders contained within angular brackets (<first>, <second>, and
Line 699: <listed_contacts>), and then we have a list of examples at the end of the scenario.
Line 700: This whole feature description with its examples becomes our specification and sole
Line 701: document that we discuss with all stakeholders. If we have doubts, we add more examples
Line 702: and scenarios to the feature until it becomes obvious to everyone how the software should
Line 703: behave.
Line 704: We save our feature description as "tests/acceptance/list_contacts.feature" and,
Line 705: as we did for the previous cases, we start by adding a test for our scenario so that PyTest
Line 706: knows that we have one more test to run:
Line 707: @scenario("../acceptance/list_contacts.feature",
Line 708:             "Listing Added Contacts")
Line 709: def test_listing_added_contacts(capsys):
Line 710:     pass
Line 711: 
Line 712: --- 페이지 193 ---
Line 713: Fitness Function with a Contact Book Application
Line 714: Chapter 7
Line 715: [ 183 ]
Line 716: As we have to check the output of the command (which will print the contacts), this time,
Line 717: our test explicitly mentions the capsys fixture, so that output starts to be captured when
Line 718: the test is run.
Line 719: The first step of our scenario is "Given I have a contact book", which we had
Line 720: already implemented for our previous contacts deletion test, so in this case we have
Line 721: nothing to do. pytest-bdd will reuse the same test implementation as the step is the same.
Line 722: Going further, we have two steps in charge of adding the two contacts from the examples
Line 723: into our contact list:
Line 724:     And I have a first <first> contact
Line 725:     And I have a second <second> contact
Line 726: These translate into two new steps, and both of these are in charge of adding one contact to
Line 727: the contact book, as shown in the following code block:
Line 728: @given("I have a first <first> contact")
Line 729: def have_a_first_contact(contactbook, first):
Line 730:     contactbook.add(first, "000")
Line 731:     return first
Line 732: @given("I have a second <second> contact")
Line 733: def have_a_second_contact(contactbook, second):
Line 734:     contactbook.add(second, "000")
Line 735:     return second
Line 736: As the two tests have the same exact implementation, you might be wondering why we
Line 737: made two different Given steps instead of a single one with a parser.
Line 738: The reason is because Given steps, in BDD, are meant to represent data that is needed to
Line 739: perform the test. They state what you have in a way that should make it possible to look up
Line 740: any of the given things explicitly. If, in any other step, we want to know what's the name of
Line 741: the first person that was added to the contact book, that step would only have to refer to the
Line 742: given test by the name of the function, and the given step would behave as a fixture
Line 743: providing that specific entity.
Line 744: To make it easier to understand, if we want to get back the name of the first contact added
Line 745: to the contact book, we just have to add a have_a_first_contact argument to the
Line 746: function implementing the step that needs that name. As the have_a_first_contact
Line 747: function returns a value, that value would be associated with any have_a_first_contact
Line 748: argument name in any other step.
Line 749: In the same way, if we want to refer to the second person in our contact book, we just have
Line 750: to require the have_a_second_contact argument.
Line 751: 
Line 752: --- 페이지 194 ---
Line 753: Fitness Function with a Contact Book Application
Line 754: Chapter 7
Line 755: [ 184 ]
Line 756: If, instead of having those two separate Given steps, we had a single have_a_contact
Line 757: step that used a parser, and we used it twice to add two contacts, which one of the two
Line 758: would the have_a_contact argument refer to? It would be ambiguous, and that's why
Line 759: pytest-bdd prevents reuse of the same Given step twice in the same scenario. Each Given
Line 760: step must be unique so that the data it provides is uniquely identifiable by the step name.
Line 761: The same doesn't apply to other kinds of steps. For example, it's perfectly
Line 762: possible to reuse the same When step multiple times in a scenario. That's
Line 763: because When steps are not meant to represent data and so have no need
Line 764: to be uniquely identifiable.
Line 765: Now that we have our Given steps in place, the next step is the When step, which is meant
Line 766: to run the command that lists our contacts:
Line 767: When I run the "contacts ls" command
Line 768: This again is a step that we already implemented in our previous delete contact scenario. In
Line 769: the scenario, the When step we implemented there accepted a command to run as an
Line 770: argument, and so it's able to run any command. pytest-bdd will be able to reuse it, and
Line 771: hence we don't have to implement anything.
Line 772: The final step is the one meant to verify that the command actually did what we expect, the
Line 773: Then step:
Line 774: Then the output contains <listed_contacts> contacts
Line 775: This step will have to check the output provided by the command and ensure that the
Line 776: contacts we wrote in our example actually exist in the output:
Line 777: @then("the output contains <listed_contacts> contacts")
Line 778: def outputcontains(listed_contacts, capsys):
Line 779:     expected_list = "".join([
Line 780:         f"{c} 000\n" for c in listed_contacts.split(",")
Line 781:     ])
Line 782:     out, _ = capsys.readouterr()
Line 783:     assert expected_list == out
Line 784: We already know that we need capsys to be able to read the output of a program being
Line 785: tested. Apart from capsys, our step also requires the list of contacts that it has to check.
Line 786: Those are coming from the Examples section in the scenario.
Line 787: 
Line 788: --- 페이지 195 ---
Line 789: Fitness Function with a Contact Book Application
Line 790: Chapter 7
Line 791: [ 185 ]
Line 792: In the Examples entry, listed_contacts were provided as comma-separated
Line 793: ("Mario,Luigi"), so the first thing we do is to split them by the comma so that we can get
Line 794: back all the contacts. Then, as our program is going to print them in separate lines with
Line 795: their phone numbers, we append the phone number at the end of the line (which is
Line 796: hardcoded at "000" as that's what we had in our two have_a_first_contact and
Line 797: have_a_second_contact steps). The expected_list variable is meant to contain the list
Line 798: of contacts, one by line with their phone number. For the "Mario,Luigi" example, the
Line 799: content would thus be as follows:
Line 800: Mario 000
Line 801: Luigi 000
Line 802: Once we have the expected_list variable containing the properly formatted text, we
Line 803: only have to compare it to the actual output of the application to confirm that the
Line 804: application printed the two contacts we expected with their phone numbers.
Line 805: Now that we have translated our steps to code, we can run our test suite to confirm that the
Line 806: test is actually verifying our implementation:
Line 807: $ pytest -v
Line 808: ...
Line 809: .../test_acceptance.py::test_listing_added_contacts[Mario-Luigi-
Line 810: Mario,Luigi] FAILED
Line 811: .../test_acceptance.py::test_listing_added_contacts[John-Jane-John,Jane]
Line 812: FAILED
Line 813: ...
Line 814: E ValueError: not enough values to unpack (expected 2, got 1)
Line 815: As expected, since we haven't yet implemented any support for listing contacts, the
Line 816: software crashed, but at least we know that pytest-bdd was able to identify the code for
Line 817: all the steps, translate them, and run the scenario for both our examples (as we have the
Line 818: same test_listing_added_contacts test performed twice, one for Mario-Luigi-
Line 819: Mario,Luigi and one for John-Jane-John,Jane).
Line 820: As usual, we can jump to our functional and unit tests to drive the actual implementation,
Line 821: and a possible edit to our Application object could be to handle commands that don't
Line 822: have any args, and then call a printlist function when the command is "ls":
Line 823: class Application:
Line 824:     ...
Line 825:     def run(self, text):
Line 826:         text = text.strip()
Line 827:         _, cmd = text.split(maxsplit=1)
Line 828:         try:
Line 829: 
Line 830: --- 페이지 196 ---
Line 831: Fitness Function with a Contact Book Application
Line 832: Chapter 7
Line 833: [ 186 ]
Line 834:             cmd, args = cmd.split(maxsplit=1)
Line 835:         except ValueError:
Line 836:             args = None
Line 837:         if cmd == "add":
Line 838:             name, num = args.rsplit(maxsplit=1)
Line 839:             try:
Line 840:                 self.add(name, num)
Line 841:             except ValueError as err:
Line 842:                 print(err)
Line 843:                 return
Line 844:         elif cmd == "del":
Line 845:             self.delete(args)
Line 846:         elif cmd == "ls":
Line 847:             self.printlist()
Line 848:         else:
Line 849:             raise ValueError(f"Invalid command: {cmd}")
Line 850:     ...
Line 851:     def printlist(self):
Line 852:         for c in self._contacts:
Line 853:             print(f"{c[0]} {c[1]}")
Line 854: The printlist function simply iterates over all contacts and prints them with their phone
Line 855: numbers.
Line 856: As we have the implementation in place, our acceptance test should pass and confirm that
Line 857: it behaves like it is meant to:
Line 858: $ pytest -v
Line 859: ...
Line 860: .../test_acceptance.py::test_listing_added_contacts[Mario-Luigi-
Line 861: Mario,Luigi] PASSED
Line 862: .../test_acceptance.py::test_listing_added_contacts[John-Jane-John,Jane]
Line 863: PASSED
Line 864: ...
Line 865: Now that the acceptance tests pass for the examples we provided, we know that the 
Line 866: implementation satisfies what our team wanted so far.
Line 867: 
Line 868: --- 페이지 197 ---
Line 869: Fitness Function with a Contact Book Application
Line 870: Chapter 7
Line 871: [ 187 ]
Line 872: Summary
Line 873: In this chapter, we saw how we can write acceptance tests that can be shared with other
Line 874: stakeholders to review the behavior of the software and not just be used by developers as a
Line 875: way to verify that behavior. We saw that it's possible to express the specifications of the
Line 876: software itself in the form of scenarios and examples, which guarantees that our
Line 877: specifications are always in sync with what the software actually does and that our
Line 878: software must always match the specifications as they become the tests themselves.
Line 879: Now that we know how to move a project forward in a test-driven way using PyTest, in the
Line 880: next chapter we are going to see more essential PyTest plugins that can help us during our
Line 881: daily development practice.