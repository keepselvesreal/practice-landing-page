# 1.6 A test from scratch (pp.12-15)

---
**Page 12**

12
CHAPTER 1
The basics of unit testing
1.5
Different exit points, different techniques
Why am I spending so much time talking about types of exit points? Because not only
is it a great idea to separate the tests for each exit point, but different types of exit
points might require different techniques to test successfully:
Return-value-based exit points (direct outputs in Meszaros’ XUnit Test Patterns)
should be the easiest exit points to test. You trigger an entry point, you get
something back, and you check the value you got back.
State-based tests (indirect outputs) usually require a little more gymnastics. You
call something, and then you do another call to check something else (or you
call the previous thing again) to see if everything went according to plan. 
In a third-party situation (indirect outputs), we have the most hoops to jump through.
We haven’t discussed this yet, but that’s where we’re forced to use things like mock
objects to replace the external system with something we can control and interrogate in
our tests. I’ll cover this idea deeply later in the book. 
1.6
A test from scratch
Let’s go back to the first, simplest version of the
code (listing 1.1) and try to test it, shall we? If we
were to try to write a test for this, what would it
look like? 
 Let’s take the visual approach first with figure 1.6.
Our entry point is sum with an input of a string called
numbers. sum is also our exit point, since we will get a
return value back from it and check its value.
 It’s possible to write an automated unit test
without using a test framework. In fact, because
developers have gotten more into the habit of
automating their testing, I’ve seen plenty of them
doing this before discovering test frameworks. In
this section, we’ll write such a test without a frame-
work, so that you can contrast this approach with
using a framework in chapter 2.
Which exit points make the most problems?
As a rule of thumb, I try to mostly use either return-value-based or state-based tests. I
try to avoid mock-object-based tests if I can, and usually I can. As a result, I usually
have no more than 5% of my tests using mock objects for verification. Those types of
tests complicate things and make maintainability more difficult. Sometimes there’s no
escape, though, and we’ll discuss them as we proceed in the next chapters.
sum(numbers)
Return value
Unit
of
work
Test
Figure 1.6
A visual view of our test


---
**Page 13**

13
1.6
A test from scratch
 So, let’s assume test frameworks don’t exist (or that we don’t know they do). We
have decided to write our own little automated test from scratch. The following listing
shows a very naive example of testing our own code with plain JavaScript.
const parserTest = () => {
  try {
    const result = sum('1,2');
    if (result === 3) {
      console.log('parserTest example 1 PASSED');
    } else {
      throw new Error(`parserTest: expected 3 but was ${result}`);
    }
  } catch (e) {
    console.error(e.stack);
  }
};
No, this code is not lovely. But it’s good enough to explain how tests work. To run this
code, we can do the following:
1
Open the command line and type an empty string.
2
Add an entry under package.json’s "scripts" entry under "test" to execute
"node mytest.js" and then execute npm test on the command line. 
The following listing shows this.
{
  "name": "aout3-samples",
  "version": "1.0.0",
  "description": "Code Samples for Art of Unit Testing 3rd Edition",
  "main": "index.js",
  "scripts": {
    "test": "node ./ch1-basics/custom-test-phase1.js",
  }
}
The test method invokes the production module (the SUT) and then checks the returned
value. If it’s not what’s expected, the test method writes to the console an error and a
stack trace. The test method also catches any exceptions that occur and writes them to
the console, so that they don’t interfere with the running of subsequent methods. When
we use a test framework, that’s usually handled for us automatically.
 Obviously, this is an ad hoc way of writing such a test. If you were to write multiple
tests like this, you might want to have a generic test or check method that all tests
could use, and which would format the errors consistently. You could also add special
helper methods that would check on things like null objects, empty strings, and so on,
so that you don’t need to write the same long lines of code in many tests. 
Listing 1.4
A very naive test against sum()
Listing 1.5
The beginning of our package.json file


---
**Page 14**

14
CHAPTER 1
The basics of unit testing
 The following listing shows what this test would look like with a slightly more
generic check and assertEquals functions.
const assertEquals = (expected, actual) => {
  if (actual !== expected) {
    throw new Error(`Expected ${expected} but was ${actual}`);
  }
};
const check = (name, implementation) => {
  try {
    implementation();
    console.log(`${name} passed`);
  } catch (e) {
    console.error(`${name} FAILED`, e.stack);
  }
};
check('sum with 2 numbers should sum them up', () => {
  const result = sum('1,2');
  assertEquals(3, result);
});
check('sum with multiple digit numbers should sum them up', () => {
  const result = sum('10,20');
  assertEquals(30, result);
});
We’ve now created two helper methods: assertEquals, which removes boilerplate
code for writing to the console or throwing errors, and check, which takes a string for
the name of the test and a callback to the implementation. It then takes care of catch-
ing any test errors, writing them to the console, and reporting on the status of the test.
Notice how the tests are easier to read and faster to write with just a couple of helper
methods. Unit testing frameworks such as Jest can provide even more generic helper
Listing 1.6
Using a more generic implementation of the Check method
Built-in asserts
It’s important to note that we don’t need to write our own asserts. We could have
easily used Node.js’s built-in assert functions, which were originally built for internal
use in testing Node.js itself. We could do so by importing the functions with 
const assert = require('assert'); 
However, I’m trying to demonstrate the underlying simplicity of the concept, so we’ll
avoid that. You can find more info about Node.js’s assert module at https://nodejs
.org/api/assert.html.


---
**Page 15**

15
1.7
Characteristics of a good unit test
methods like this, so tests are even easier to write. I’ll talk about that in chapter 2.
First, let’s talk a bit about the main subject of this book: good unit tests. 
1.7
Characteristics of a good unit test
No matter what programming language you’re using, one of the most difficult aspects
of defining a unit test is defining what’s meant by a good one. Of course, good is rela-
tive, and it can change whenever we learn something new about coding. That may
seem obvious, but it really isn’t. I need to explain why we need to write better tests—
understanding what a unit of work is isn’t enough.
 Based on my own experience, involving many companies and teams over the years,
most people who try to unit test their code either give up at some point or don’t actu-
ally perform unit tests. They waste a lot of time writing problematic tests, and they give
up when they have to spend a lot of time maintaining them, or worse, they don’t trust
their results. 
 There’s no point in writing a bad unit test, unless you’re in the process of learning
how to write a good one. There are more downsides than upsides to writing bad tests,
such as wasting time debugging buggy tests, wasting time writing tests that bring no
benefit, wasting time trying to understand unreadable tests, and wasting time writing
tests only to delete them a few months later. There’s also a huge issue with maintain-
ing bad tests, and with how they affect the maintainability of production code. Bad
tests can actually slow down your development speed, not only when writing test code,
but also when writing production code. I’ll touch on all these things later in the book.
 By learning what a good unit test is, you can be sure you aren’t starting off on a
path that will be hard to fix later on, when the code becomes a nightmare. We’ll also
define other forms of tests (component, end to end, and more) later in the book.
1.7.1
What is a good unit test? 
Every good automated test (not just unit tests) should have the following properties:
It should be easy to understand the intent of the test author.
It should be easy to read and write.
It should be automated.
It should be consistent in its results (it should always return the same result if
you don’t change anything between runs).
It should be useful and provide actionable results.
Anyone should be able to run it with the push of a button.
When it fails, it should be easy to detect what was expected and determine how
to pinpoint the problem.
A good unit test should also exhibit the following properties: 
It should run quickly.
It should have full control of the code under test (more on that in chapter 3).
It should be fully isolated (run independently of other tests).


