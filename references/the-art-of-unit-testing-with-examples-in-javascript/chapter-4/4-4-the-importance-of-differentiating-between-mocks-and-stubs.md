# 4.4 The importance of differentiating between mocks and stubs (pp.88-89)

---
**Page 88**

88
CHAPTER 4
Interaction testing using mock objects
    info: (text) => {
        written = text;
    }
};
It only has one function, which mimics the signature of the logger’s info function. It
then saves the parameter being passed to it (text) so that we can assert that it was
called later in the test. If the written variable has the correct text, this proves that our
function was called, which means we have proven that the exit point is invoked cor-
rectly from our unit of work. 
 On the verifyPassword2 side, the refactoring we did is pretty common. It’s pretty
much the same as we did in the previous chapter, where we extracted a stub as a
dependency. Stubs and mocks are often treated the same way in terms of refactoring
and introducing seams in our application’s code.
 What did this simple refactoring into a parameter provide us with? 
We do not need to explicitly import (via require) the logger in our code
under test anymore. That means that if we ever change the real dependency of
the logger, the code under test will have one less reason to change. 
We now have the ability to inject any logger of our choosing into the code under
test, as long as it lives up to the same interface (or at least has the info
method). This means that we can provide a mock logger that does our bidding
for us: the mock logger helps us verify that it was called correctly. 
NOTE
The fact that our mock object only mimics a part of the logger’s inter-
face (it’s missing the debug function) is a form of duck typing. I discussed this
idea in chapter 3: if it walks like a duck, and it talks like a duck, then we can
use it as a fake object.
4.4
The importance of differentiating between mocks 
and stubs
Why do I care so much about what we name each thing? If we can’t tell the difference
between mocks and stubs, or we don’t name them correctly, we can end up with tests
that are testing multiple things and that are less readable and harder to maintain.
Naming things correctly helps us avoid these pitfalls. 
 Given that a mock represents a requirement from our unit of work (“it calls the
logger,” “it sends an email,” etc.) and that a stub represents incoming information or
behavior (“the database query returns false,” “this specific configuration throws an
error”), we can set a simple rule of thumb: It should be OK to have multiple stubs in a
test, but you don’t usually want to have more than a single mock per test, because that
would mean you’re testing more than one requirement in a single test.
 If we can’t (or won’t) differentiate between things (naming is key to that), we can
end up with multiple mocks per test or asserting our stubs, both of which can have neg-
ative effects on our tests. Keeping naming consistent gives us the following benefits:


---
**Page 89**

89
4.5
Modular-style mocks
Readability—Your test name will become much more generic and harder to
understand. You want people to be able to read the name of the test and know
everything that happens or is tested inside of it, without needing to read the
test’s code.
Maintainability—You could, without noticing or even caring, assert against stubs
if you don’t differentiate between mocks and stubs. This produces little value to
you and increases the coupling between your tests and internal production
code. Asserting that you queried a database is a good example of this. Instead of
testing that a database query returns some value, it would be much better to test
that the application’s behavior changes after we change the input from the
database. 
Trust—If you have multiple mocks (requirements) in a single test, and the first
mock verification fails the test, most test frameworks won’t execute the rest of
the test (below the failing assert line) because an exception has been thrown.
This means that the other mocks aren’t verified, and you won’t get the results
from them.
To drive the last point home, imagine a doctor who only sees 30% of their patient’s
symptoms, but still needs to make a decision—they might make the wrong decision
about treatment. If you can’t see where all the bugs are, or that two things are failing
instead of just one (because one of them is hidden after the first failure), you’re more
likely to fix the wrong thing or to fix it in the wrong place. 
 XUnit Test Patterns (Addison-Wesley, 2007), by Gerard Meszaros, calls this situation
assertion roulette (http://xunitpatterns.com/Assertion%20Roulette.html). I like this
name. It’s quite a gamble. You start commenting out lines of code in your test, and lots
of fun ensues (and possibly alcohol).
4.5
Modular-style mocks
I covered modular dependency injection in the previous chapter, but now we’re going
to look at how we can use it to inject mock objects and simulate answers on them.
Not everything is a mock
It’s unfortunate that people still tend to use the word “mock” for anything that isn’t
real, such as “mock database” or “mock service.” Most of the time they really mean
they are using a stub. 
It’s hard to blame them, though. Frameworks like Mockito, jMock, and most isolation
frameworks (I don’t call them mocking frameworks, for the same reasons I’m dis-
cussing right now), use the word “mock” to denote both mocks and stubs. 
There are newer frameworks, such as Sinon and testdouble in JavaScript, NSubsti-
tute and FakeItEasy in .NET, and others, that have helped start a change in the nam-
ing conventions. I hope this persists.


