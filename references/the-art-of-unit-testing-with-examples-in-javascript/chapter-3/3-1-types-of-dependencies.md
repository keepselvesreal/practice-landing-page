# 3.1 Types of dependencies (pp.62-64)

---
**Page 62**

62
CHAPTER 3
Breaking dependencies with stubs
We call the external things that we rely on in our code dependencies. I’ll define them
more thoroughly later in the chapter. These dependencies could include things like
time, async execution, using the filesystem, or using the network, or they could simply
involve using something that is very difficult to configure or that may be time consum-
ing to execute.
3.1
Types of dependencies
In my experience, there are two main types of dependencies that our unit of work
can use:
Outgoing dependencies—Dependencies that represent an exit point of our unit of
work, such as calling a logger, saving something to a database, sending an email,
notifying an API or a webhook that something has happened, etc. Notice these
are all verbs: “calling,” “sending,” and “notifying.” They are flowing outward from
the unit of work in a sort of fire-and-forget scenario. Each represents an exit
point, or the end of a specific logical flow in a unit of work.
Incoming dependencies—Dependencies that are not exit points. These do not rep-
resent a requirement on the eventual behavior of the unit of work. They are
merely there to provide test-specific specialized data or behavior to the unit of
work, such as a database query’s result, the contents of a file on the filesystem, a
network response, etc. Notice that these are all passive pieces of data that flow
inward to the unit of work as the result of a previous operation. 
Figure 3.1 shows these side by side.
Test
Entry point
Exit point
Data
or behavior
Dependency
Unit
of
work
Test
Entry point
Exit point
Dependency
Unit
of
work
Outgoing dependency
Incoming dependency
Figure 3.1
On the left, an exit point is implemented as invoking a dependency. On the right, the dependency 
provides indirect input or behavior and is not an exit point.


---
**Page 63**

63
3.1
Types of dependencies
Some dependencies can be both incoming and outgoing—in some tests they will rep-
resent exit points, and in other tests they will be used to simulate data coming into the
application. These shouldn’t be very common, but they do exist, such as an external
API that returns a success/fail response for an outgoing message.
 With these types of dependencies in mind, let’s look at how the book xUnit Test Pat-
terns defines the various patterns for things that look like other things in tests.
Table 3.1 lists my thoughts about some patterns from the book’s website at http://
mng.bz/n1WK.
Here’s another way to think about this for the rest of this book:
Stubs break incoming dependencies (indirect inputs). Stubs are fake modules,
objects, or functions that provide fake behavior or data into the code under test.
We do not assert against them. We can have many stubs in a single test.
Mocks break outgoing dependencies (indirect outputs or exit points). Mocks
are fake modules, objects, or functions that we assert were called in our tests. A
mock represents an exit point in a unit test. Because of this, it is recommended
that you have no more than a single mock per test.
Unfortunately, in many shops you’ll hear the word “mock” thrown around as a catch-
all term for both stubs and mocks. Phrases like “we’ll mock this out” or “we have a
mock database” can really create confusion. There is a huge difference between stubs
Table 3.1
Clarifying terminology around stubs and mocks
Category
Pattern
Purpose
Uses
Test double
Generic name for stubs and 
mocks
I also use the term fake.
Stub
Dummy object
Used to specify the values to 
be used in tests when the only 
usage is as irrelevant argu-
ments of SUT method calls
Send as a parameter to the 
entry point or as the arrange 
part of the AAA pattern.
Test stub
Used to verify logic inde-
pendently when it depends on 
indirect inputs from other soft-
ware components
Inject as a dependency, and 
configure it to return specific 
values or behavior into the SUT.
Mock
Test spy
Used to verify logic inde-
pendently when it has indirect 
outputs to other software com-
ponents
Override a single function on a 
real object, and verify that the 
fake function was called as 
expected.
Mock object
Used to verify logic inde-
pendently when it depends on 
indirect outputs to other soft-
ware components
Inject the fake as a depen-
dency into the SUT, and verify 
that the fake was called as 
expected.


---
**Page 64**

64
CHAPTER 3
Breaking dependencies with stubs
and mocks (one should really only be used once in a test), and we should use the right
terms to ensure it’s clear what the other person is referring to. 
 When in doubt, use the term “test double” or “fake.” Often, a single fake depen-
dency can be used as a stub in one test, and it can be used as a mock in another test.
We’ll see an example of this later on. 
This might seem like a whole lot of information at once. I’ll dive deep into these defi-
nitions throughout this chapter. Let’s take a small bite and start with stubs.
3.2
Reasons to use stubs
What if we’re faced with the task of testing a piece of code like the following?
const moment = require('moment');
const SUNDAY = 0, SATURDAY = 6;
const verifyPassword = (input, rules) => {
    const dayOfWeek = moment().day();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
Our password verifier has a new dependency: it can’t work on weekends. Go figure. Spe-
cifically, the module has a direct dependency on moment.js, which is a very common
date/time wrapper for JavaScript. Working with dates directly in JavaScript is not a pleas-
ant experience, so we can assume many shops out there have something like this. 
XUnit test patterns and naming things
xUnit Test Patterns: Refactoring Test Code by Gerard Meszaros (Addison-Wesley,
2007) is a classic pattern reference book for unit testing. It defines patterns for
things you fake in your tests in at least five ways. Once you’ve gotten a feel for the
three types I mention here, I encourage you to take a look at the extra details that
book provides. 
Note that xUnit Test Patterns has a definition for the word “fake”: “Replace a compo-
nent that the system under test (SUT) depends on with a much lighter-weight imple-
mentation.” For example, you might use an in-memory database instead of a full-
fledged production instance. 
I still consider this type of test double a “stub,” and I use the word “fake” to call out
anything that isn’t real, much like the term “test double,” but “fake” is shorter and
easier on the tongue.
Listing 3.1
verifyPassword using time


