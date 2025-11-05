# A first unit test (pp.28-61)

---
**Page 28**

28
A first unit test
When I first started writing unit tests with a real unit testing framework, there was
little documentation, and the frameworks I worked with didn’t have proper exam-
ples. (I was mostly coding in VB 5 and 6 at the time.) It was a challenge learning to
work with them, and I started out writing rather poor tests. Fortunately, times have
changed. In JavaScript, and in practically any language out there, there’s a wide
range of choices and plenty of documentation and support from the community
for trying out these bundles of helpfulness.
 In the previous chapter, we wrote a very simple home-grown test framework.
In this chapter, we’ll take a look at Jest, which will be our framework of choice for
this book. 
This chapter covers
Writing your first test with Jest
Test structure and naming conventions
Working with the assertion library
Refactoring tests and reducing repetitive code


---
**Page 29**

29
2.1
Introducing Jest
2.1
Introducing Jest
Jest is an open source test framework created by Facebook. It’s easy to use, easy to
remember, and has lots of great features. Jest was originally created for testing front-
end React components in JavaScript. These days it’s widely used in many parts of the
industry for both backend and frontend project testing. It supports two major flavors
of test syntax (one that uses the word test and another that’s based on the Jasmin syn-
tax, a framework that has inspired many of Jest’s features). We’ll try both of them to
see which one we like better. 
 Aside from Jest, there are many other testing frameworks in JavaScript, pretty
much all open source as well. There are some differences between them in style and
APIs, but for the purposes of this book, that shouldn’t matter too much. 
2.1.1
Preparing our environment
Make sure you have Node.js installed locally. You can follow the instructions at
https://nodejs.org/en/download/ to get it up and running on your machine. The
site will provide you with the option of either a long-term support (LTS) release or a
current release. The LTS release is geared toward enterprises, whereas the current
release has more frequent updates. Either will work for the purposes of this book.
 Make sure that the node package manager (npm) is installed on your machine. It
is included with Node.js, so run the command npm -v on the command line, and if you
see a version of 6.10.2 or higher, you should be good to go. If not, make sure Node.js
is installed.
2.1.2
Preparing our working folder
To get started with Jest, let’s create a new empty folder named “ch2” and initialize it
with a package manager of your choice. I’ll use npm, since I have to choose one. Yarn
is an alternative package manager. It shouldn’t matter, for the purposes of this book,
which one you use. 
 Jest expects either a jest.config.js or a package.json file. We’re going with the latter,
and npm init will generate one for us:
mkdir ch2
cd ch2
npm init --yes
//or
yarn init –yes 
git init
I’m also initializing Git in this folder. This would be recommended anyway, to track
changes, but for Jest this file is used under the covers to track changes to files and run
specific tests. It makes Jest’s life easier. 
 By default, Jest will look for its configuration either in the package.json file that is
created by this command or in a special jest.config.js file. For now, we won’t need


---
**Page 30**

30
CHAPTER 2
A first unit test
anything but the default package.json file. If you’d like to learn more about the Jest
configuration options, refer to https://jestjs.io/docs/en/configuration.
2.1.3
Installing Jest
Next, we’ll install Jest. To install Jest as a dev dependency (which means it does not get
distributed to production) we can use this command:
npm install --save-dev jest
//or
yarn add jest –dev
This will create a new jest.js file under our [root folder]/node_modules/bin. We can
then execute Jest using the npx jest command.
 We can also install Jest globally on the local machine (I recommend doing this on
top of the save-dev installation) by executing this command:
npm install -g jest
This will give us the freedom to execute the jest command directly from the com-
mand line in any folder that has tests, without going through npm to execute it.
 In real projects, it is common to use npm commands to run tests instead of using
the global jest. I’ll show how this is done in the next few pages. 
2.1.4
Creating a test file
Jest has a couple of default ways to find test files: 
If there’s a __tests__ folder, it loads all the files in it as test files, regardless of
their naming conventions. 
It tries to find any file that ends with *.spec.js or *.test.js, in any folder under the
root folder of your project, recursively. 
We’ll use the first variation, but we’ll also name our files with either *test.js or *.spec.js
to make things a bit more consistent in case we want to move them around later (and
stop using the __tests_ folder altogether). 
 You can also configure Jest to your heart’s content, specifying how to find which
files where, with a jest.config.js file or through package.json. You can look up the Jest
docs at https://jestjs.io/docs/en/configuration to find all the gory details.
 The next step is to create a special folder under our ch2 folder called __tests__.
Under this folder, create a file that ends with either test.js or spec.js—my-compo-
nent.test.js, for example. Which suffix you choose is up to you—it’s about your own
style. I’ll use them interchangeably in this book because I think of “test” as the sim-
plest version of “spec,” so I use it when showing very simple things.
 We don’t need require() at the top of the file to start using Jest. It automatically
imports global functions for us to use. The main functions you should be interested
in include test, describe, it, and expect. Listing 2.1 shows what a simple test might
look like.


---
**Page 31**

31
2.1
Introducing Jest
test('hello jest', () => {
    expect('hello').toEqual('goodbye');
});
We haven’t used describe and it yet, but we’ll get to them soon. 
2.1.5
Executing Jest
To run this test, we need to be able to execute Jest. For Jest to be recognized from the
command line, we need to do either of the following:
Install Jest globally on the machine by running npm install jest -g.
Use npx to execute Jest from the node_modules directory by typing jest in the
root of the ch2 folder.
If all the stars lined up correctly, you should see the results of the Jest test run and a fail-
ure. Your first failure. Yay! Figure 2.1 shows the output on my terminal when I run the
command. It’s pretty cool to see such lovely, colorful (if you’re reading the e-book), use-
ful output from a test tool. It looks even cooler if your terminal is in dark mode.
 Let’s take a closer look at the details. Figure 2.2 shows the same output, but with
numbers to follow along. Let’s see how many pieces of information are presented
here:
b
A quick list of all the failing tests (with names) with nice red Xs next to them
c
A detailed report on the expectation that failed (aka our assertion)
d
The exact difference between the actual value and expected value
e
The type of comparison that was executed
f
The code for the test
g
The exact line (visually) where the test failed
h
A report of how many tests ran, failed, and passed
i
The time it took
j
The number of snapshots (not relevant to our discussion)
Test file locations
There are two main patterns I see for placing test files: Some people prefer to place
the test files directly next to the files or modules being tested. Others prefer to place
all the files under a test directory. Which approach you choose doesn’t really matter;
just be consistent in your choice throughout a project, so it’s easy to know where to
find the tests for a specific item. 
I find that placing tests in a test folder allows me to also put helper files under the
test folder close to the tests. As for easily navigating between tests and the code
under test, there are plugins for most IDEs today that allow you to navigate between
code and its tests with a keyboard shortcut.
Listing 2.1
Hello Jest


---
**Page 32**

32
CHAPTER 2
A first unit test
Figure 2.1
Terminal output from Jest
1
2
3
4
5
6
7
8
9
Figure 2.2
Annotated terminal output from Jest


---
**Page 33**

33
2.2
The library, the assert, the runner, and the reporter
Imagine trying to write all this reporting functionality yourself. It’s possible, but who’s
got the time and the inclination? Plus, you’d have to take care of any bugs in the
reporting mechanism. 
 If we change goodbye to hello in the test, we can see what happens when the test
passes (figure 2.3). Nice and green, as all things should be (again, in the digital ver-
sion—otherwise it’s nice and grey).
You might note that it takes 1.5 seconds to run this single Hello World test. If we used
the command jest --watch instead, we could have Jest monitor filesystem activity in
our folder and automatically run tests for files that have changed without re-initializ-
ing itself every time. This can save a considerable amount of time, and it really helps
with the whole notion of continuous testing. Set a terminal in the other window of your
workstation with jest --watch on it, and you can keep coding and getting fast feed-
back on issues you might be creating. That’s a good way to get into the flow of things.
 Jest also supports async-style testing and callbacks. I’ll touch on these when we get
to those topics later in the book, but if you’d like to learn more about this style now,
head over to the Jest documentation on the subject: https://jestjs.io/docs/en/asyn-
chronous.
2.2
The library, the assert, the runner, and the reporter
Jest has acted in several capacities for us:
It acted as a test library to use when writing the test.
It acted as an assertion library for asserting inside the test (expect).
It acted as the test runner.
It acted as the test reporter for the test run.
Jest also provides isolation facilities to create mocks, stubs, and spies, though we
haven’t seen that yet. We’ll touch on these ideas in later chapters. 
 Other than isolation facilities, it’s very common in other languages for a test frame-
work to fill all the roles I just mentioned—library, assertions, test runner, and test
reporter—but the JavaScript world seems a bit more fragmented. Many other test
frameworks provide only some of these facilities. Perhaps this is because the mantra of
Figure 2.3
Jest terminal 
output for a passing test 


---
**Page 34**

34
CHAPTER 2
A first unit test
“do one thing, and do it well” has been taken to heart, or perhaps it’s for other rea-
sons. In any case, Jest stands out as one of a handful of all-in-one frameworks. It is a
testament to the strength of the open source culture in JavaScript that for each one of
these categories, there are multiple tools that you can mix and match to create your
own super toolset. 
 One of the reasons I chose Jest for this book is so we don’t have to bother too
much with the tooling or deal with missing features—we can just focus on the pat-
terns. That way we won’t have to use multiple frameworks in a book that is mostly con-
cerned with patterns and antipatterns.
2.3
What unit testing frameworks offer
Let’s zoom out for a second and see where we are. What do frameworks like Jest offer
us over creating our own framework, like we started to do in the previous chapter, or
over manually testing things? 
Structure—Instead of reinventing the wheel every time you want to test a fea-
ture, when you use a test framework you always start out the same way—by writ-
ing a test with a well-defined structure that everyone can easily recognize, read,
and understand.
Repeatability—When using a test framework, it’s easy to repeat the act of writing
a new test. It’s also easy to repeat the execution of the test, using a test runner,
and it’s easy to do this quickly and many times a day. It’s also easy to understand
failures and their causes. Someone has already done all the hard work for us,
instead of us having to code all that stuff into our hand-rolled framework. 
Confidence and time savings—When we roll our own test framework, the frame-
work is more likely to have bugs in it, since it is less battle-tested than an existing
mature and widely used framework. On the other hand, manually testing things
is usually very time consuming. When we’re short on time, we’ll likely focus on
testing the things that feel the most critical and skip over things that might feel
less important. We could be skipping small but significant bugs. By making it
easy to write new tests, it’s more likely that we’ll also write tests for the stuff that
feels less significant because we won’t be spending too much time writing tests
for the big stuff.
Shared understanding—The framework’s reporting can be helpful for managing
tasks at the team level (when a test is passing, it means the task is done). Some
people find this useful.
In short, frameworks for writing, running, and reviewing unit tests and their results
can make a huge difference in the daily lives of developers who are willing to invest
the time in learning how to use them properly. Figure 2.4 shows the areas in software
development in which a unit testing framework and its helper tools have influence,
and table 2.1 lists the types of actions we usually execute with a test framework.


---
**Page 35**

35
2.3
What unit testing frameworks offer
Table 2.1
How testing frameworks help developers write and execute tests and review results
Unit testing practice
How the framework helps
Write tests easily and in a 
structured manner.
A framework supplies the developer with helper functions, assertion func-
tions, and structure-related functions.
Execute one or all of the 
unit tests.
A framework provides a test runner, usually at the command line, that 
Identifies tests in your code
Runs tests automatically
Indicates test status while running
Review the results of the 
test runs.
A test runner will usually provide information such as 
How many tests ran
How many tests didn’t run
How many tests failed 
Which tests failed
The reason tests failed
The code location that failed
Possibly provide a full stack trace for any exceptions that caused 
the test to fail, and let you go to the various method calls inside the 
call stack
Unit tests
Write
tests
Review
results
Run
tests
Run
Code
Unit testing framework
Figure 2.4
Unit tests are written as code, using libraries from the unit testing 
framework. The tests are run from a test runner inside the IDE or through the 
command line, and the results are reviewed through a test reporter (either as 
output text or in the IDE) by the developer or an automated build process.


---
**Page 36**

36
CHAPTER 2
A first unit test
At the time of writing, there are around 900 unit testing frameworks out there, with
more than a couple for most programming languages in public use (and a few dead
ones). You can find a good list on Wikipedia: https://en.wikipedia.org/wiki/List_
of_unit_testing_frameworks. 
NOTE
Using a unit testing framework doesn’t ensure that the tests you write
are readable, maintainable, or trustworthy, or that they cover all the logic you’d
like to test. We’ll look at how to ensure your unit tests have these properties in
chapters 7 through 9 and in various other places throughout this book. 
2.3.1
The xUnit frameworks
When I started writing tests (in the Visual Basic days), the standard by which most unit
test frameworks were measured was collectively called xUnit. The grandfather of the
xUnit frameworks idea was SUnit, the unit testing framework for Smalltalk. 
 These unit testing frameworks’ names usually start with the first letters of the lan-
guage for which they were built; you might have CppUnit for C++, JUnit for Java,
NUnit and xUnit for .NET, and HUnit for the Haskell programming language. Not all
of them follow these naming guidelines, but most do.
2.3.2
xUnit, TAP, and Jest structures
It’s not just the names that were reasonably consistent. If you were using an xUnit
framework, you could also expect a specific structure in which the tests were built.
When these frameworks would run, they would output their results in the same struc-
ture, which was usually an XML file with a specific schema.
 This type of xUnit XML report is still prevalent today, and it’s widely used in most
build tools, such as Jenkins, which support this format with native plugins and use it to
report the results of test runs. Most unit test frameworks in static languages still use
the xUnit model for structure, which means that once you’ve learned to use one of
them, you should be able to easily use any of them (assuming you know the particular
programming language).
 The other interesting standard for the reporting structure of test results and more
is called TAP, the Test Anything Protocol. TAP started life as part of the test harness for
Perl, but now it has implementations in C, C++, Python, PHP, Perl, Java, JavaScript,
and other languages. TAP is much more than just a reporting specification. In the
JavaScript world, the TAP framework is the best-known test framework that natively
supports the TAP protocol.
 Jest is not strictly an xUnit or TAP framework. Its output is not xUnit- or TAP-
compliant by default. However, because xUnit-style reporting still rules the build
sphere, we’ll usually want to adapt to that protocol for our reporting on a build server.
To get Jest test results that are easily recognized by most build tools, you can install
npm modules such as jest-xunit (if you want TAP-specific output, use jest-tap-
reporter) and then use a special jest.config.js file in your project to configure Jest to
alter its reporting format. 


---
**Page 37**

37
2.5
The first Jest test for verifyPassword
 Now let’s move on and write something that feels a bit more like a real test with
Jest, shall we?
2.4
Introducing the Password Verifier project
The project that we’ll mostly use for testing examples in this book will start out simple,
containing only one function. As the book moves along, we’ll extend that project with
new features, modules, and classes to demonstrate different aspects of unit testing.
We’ll call it the Password Verifier project.
 The first scenario is pretty simple. We’ll be building a password verification library,
and it will just be a function at first. The function, verifyPassword(rules), allows us
to put in custom verification functions dubbed rules, and it outputs the list of errors,
according to the rules that have been input. Each rule function will output two fields: 
{
    passed: (boolean),
    reason: (string)
} 
In this book, I’ll teach you to write tests that check verifyPassword’s functionality in
multiple ways as we add more features to it.
 The following listing shows version 0 of this function, with a very naive implemen-
tation.
const verifyPassword = (input, rules) => {
  const errors = [];
  rules.forEach(rule => {
    const result = rule(input);
    if (!result.passed) {
      errors.push(`error ${result.reason}`);
    }
  });
  return errors;
};
Granted, this is not the most functional-style code, and we might refactor it a bit later,
but I wanted to keep things very simple here so we can focus on the tests.
 The function doesn’t really do much. It iterates over all the rules given and runs
each one with the supplied input. If the rule’s result is not passed, then an error is
added to the final errors array that is returned as the final result.
2.5
The first Jest test for verifyPassword
Assuming you have Jest installed, you can go ahead and create a new file named
password-verifier0.spec.js under the __tests__ folder. 
 Using the __tests__ folder is only one convention for organizing your tests, and it’s
part of Jest’s default configuration. There are many who prefer to place the test files
Listing 2.2
Password Verifier version 0


---
**Page 38**

38
CHAPTER 2
A first unit test
alongside the code being tested. There are pros and cons to each approach, and we’ll
get into that in later parts of the book. For now, we’ll go with the defaults.
 Here’s a first version of a test against our new function.
test('badly named test', () => {
  const fakeRule = input =>                      
    ({ passed: false, reason: 'fake reason' });  
  const errors = verifyPassword('any value', [fakeRule]);   
  expect(errors[0]).toMatch('fake reason');  
});
2.5.1
The Arrange-Act-Assert pattern
The structure of the test in listing 2.3 is colloquially called the Arrange-Act-Assert (AAA)
pattern. It’s quite nice! I find it very easy to reason about the parts of a test by saying
things like “that ‘arrange’ part is too complicated” or “where is the ‘act’ part?”
 In the arrange part, we’re creating a fake rule that always returns false, so that we
can prove it’s actually used by asserting on its reason at the end of the test. We then
send it to verifyPassword along with a simple input. We check in the assert section
that the first error we get matches the fake reason we gave in the arrange part.
.toMatch(/string/) uses a regular expression to find a part of the string. It’s the
same as using .toContain('fake reason').
 It’s tedious to run Jest manually after we write a test or fix something, so let’s con-
figure npm to run Jest automatically. Go to package.json in the root folder of ch2 and
add the following items under the scripts item:
"scripts": {
   "test": "jest",
   "testw": "jest --watch" //if not using git, change to --watchAll
},
If you don’t have Git initialized in this folder, you can use the command --watchAll
instead of --watch.
 If everything went well, you can now type npm test in the command line from the
ch2 folder, and Jest will run the tests once. If you type npm run testw, Jest will run and
wait for changes in an endless loop, until you kill the process with Ctrl-C. (You need to
use the word run because testw is not one of the special keywords that npm recog-
nizes automatically.)
 If you run the test, you can see that it passes, since the function works as expected. 
Listing 2.3
The first test against verifyPassword()
Setting up inputs 
for the test
Invoking the 
entry point with 
the inputs
Checking the exit point


---
**Page 39**

39
2.5
The first Jest test for verifyPassword
2.5.2
Testing the test
Let’s put a bug in the production code and see if the test fails when it should.
const verifyPassword = (input, rules) => {
  const errors = [];
  rules.forEach(rule => {
    const result = rule(input);
    if (!result.passed) {
      // errors.push(`error ${result.reason}`);  
    }
  });
  return errors;
};
You should now see your test failing with a nice message. Let’s uncomment the line
and see the test pass again. This is a great way to gain some confidence in your tests, if
you’re not doing test-driven development and are writing the tests after the code.
2.5.3
USE naming
Our test has a really bad name. It doesn’t explain anything about what we’re trying to
accomplish here. I like to put three pieces of information in test names, so that the
reader of the test will be able to answer most of their mental questions just by looking
at the test name. These three parts include
The unit of work under test (the verifyPassword function, in this case)
The scenario or inputs to the unit (the failed rule)
The expected behavior or exit point (returns an error with a reason)
During the review process, Tyler Lemke, a reviewer of the book, came up with a nice
acronym for this, USE: unit under test, scenario, expectation. I like it, and it’s easy to
remember. Thanks Tyler!
 The following listing shows our next revision of the test with a USE name.
test('verifyPassword, given a failing rule, returns errors', () => {
  const fakeRule = input => ({ passed: false, reason: 'fake reason' });
  const errors = verifyPassword('any value', [fakeRule]);
  expect(errors[0]).toContain('fake reason');
});
This is a bit better. When a test fails, especially during a build process, you don’t see
comments or the full test code. You usually only see the name of the test. The name
should be so clear that you might not even have to look at the test code to understand
where the production code problem might be.
Listing 2.4
Adding a bug
Listing 2.5
Naming a test with USE
We've accidentally 
commented out 
this line.


---
**Page 40**

40
CHAPTER 2
A first unit test
2.5.4
String comparisons and maintainability
We also made another small change in the following line:
expect(errors[0]).toContain('fake reason');
Instead of checking that one string is equal to another, as is very common in tests, we
are checking that a string is contained in the output. This makes our test less brittle
for future changes to the output. We can use .toContain or .toMatch(/fake reason/),
which uses a regular expression to match a part of the string, to achieve this. 
 Strings are a form of user interface. They are visible to humans, and they might
change—especially the edges of strings. We might add whitespace, tabs, asterisks, or
other embellishments to a string. We care that the core of the information contained in
the string exists. We don’t want to change our test every time someone adds a new line
to the end of a string. This is part of the thinking we want to encourage in our tests:
test maintainability over time, and resistance to test brittleness, are of high priority. 
 We’d ideally like the test to fail only when something is actually wrong in the pro-
duction code. We’d like to reduce the number of false positives to a minimum. Using
toContain() or toMatch() is a great way to move toward that goal. 
 I’ll talk about more ways to improve test maintainability throughout the book, and
especially in part 2 of the book.
2.5.5
Using describe()
We can use Jest’s describe() function to create a bit more structure around our test
and to start separating the three USE pieces of information from each other. This step
and the ones after it are completely up you—you can decide how you want to style
your test and its readability structure. I’m showing you these steps because many peo-
ple either don’t use describe() in an effective way, or they ignore it altogether. It can
be quite useful.
 The describe() functions wrap our tests with context: both logical context for the
reader, and functional context for the test itself. The next listing shows how we can
start using them.
describe('verifyPassword', () => {
  test('given a failing rule, returns errors', () => {
    const fakeRule = input =>
      ({ passed: false, reason: 'fake reason' });
    const errors = verifyPassword('any value', [fakeRule]);
    expect(errors[0]).toContain('fake reason');
  });
});
Listing 2.6
Adding a describe() block


---
**Page 41**

41
2.5
The first Jest test for verifyPassword
I’ve made four changes here:
I’ve added a describe() block that describes the unit of work under test. To
me this looks clearer. It also feels like I can now add more nested tests under
that block. This describe() block also helps the command-line reporter create
nicer reports.
I’ve nested the test under the new block and removed the name of the unit of
work from the test.
I’ve added the input into the fake rule’s reason string. 
I’ve added an empty line between the arrange, act, and assert parts to make the
test more readable, especially to someone new to the team.
2.5.6
Structure implying context
The nice thing about describe() is that it can be nested under itself. So we can use it
to create another level that explains the scenario, and under that we’ll nest our test. 
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    test('returns errors', () => {
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason' });
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Some people will hate it, but I think there’s a certain elegance to it. This nesting
allows us to separate the three pieces of critical information to their own level. In
fact, we can also extract the false rule outside of the test right under the relevant
describe(), if we wish to.
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    const fakeRule = input => ({ passed: false,
                                 reason: 'fake reason' });
    test('returns errors', () => {
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Listing 2.7
Nested describes for extra context
Listing 2.8
Nested describes with an extracted input


---
**Page 42**

42
CHAPTER 2
A first unit test
For the next example, I’ll move this rule back into the test (I like it when things are
close together—more on that later).
 This nesting structure also implies very nicely that under a specific scenario you
could have more than one expected behavior. You could check multiple exit points
under a scenario, with each one as a separate test, and it will still make sense from the
reader’s point of view. 
2.5.7
The it() function
There’s one missing piece to the puzzle I’ve been building so far. Jest also exposes an
it() function. This function is, for all intents and purposes, an alias to the test()
function, but it fits in more nicely in terms of syntax with the describe-driven
approach outlined so far.
 The following listing shows what the test looks like when I replace test() with it().
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns errors', () => {
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason' });
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
In this test, it’s very easy to understand what it refers to. This is a natural extension of
the previous describe() blocks. Again, it’s up to you whether you want to use this
style. I’m showing one variation of how I like to think about it.
2.5.8
Two Jest flavors
As you’ve seen, Jest supports two main ways to write tests: a terse test syntax, and a
more describe-driven (i.e., hierarchical) syntax. 
 The describe-driven Jest syntax can be largely attributed to Jasmine, one of the
oldest JavaScript test frameworks. The style itself can be traced back to Ruby-land and
the well-known RSpec Ruby test framework. This nested style is usually called BDD
style, referring to behavior-driven development. 
 You can mix and match these styles as you like (I do). You can use the test syntax
when it’s easy to understand your test target and all of its context, without going to too
much trouble. The describe syntax can help when you’re expecting multiple results
from the same entry point under the same scenario. I’m showing them both here
because I sometimes use the terse test flavor and sometimes use the describe-driven
flavor, depending on the complexity and expressiveness requirements.
Listing 2.9
Replacing test() with it()


---
**Page 43**

43
2.5
The first Jest test for verifyPassword
2.5.9
Refactoring the production code
Since there are many ways to build the same thing in JavaScript, I thought I’d show a
couple of variations on our design and what happens if we change it. Suppose we’d
like to make the password verifier an object with state.
 One reason to change the design into a stateful one might be that I intend for dif-
ferent parts of the application to use this object. One part will configure and add rules
to it, and a different part will use it to do the verification. Another reason is that we
need to know how to handle a stateful design and look at which directions it pulls our
tests in, and what we can do about that.
 Let’s look at the production code first.
class PasswordVerifier1 {
  constructor () {
    this.rules = [];
  }
  addRule (rule) {
    this.rules.push(rule);
  }
  verify (input) {
    const errors = [];
    this.rules.forEach(rule => {
      const result = rule(input);
      if (result.passed === false) {
        errors.push(result.reason);
      }
BDD’s dark present
BDD has quite an interesting background that might be worth talking about. BDD isn’t
related to TDD. Dan North, the person most associated with inventing the term, refers
to BDD as using stories and examples to describe how an application should behave.
Mainly this is targeted at working with non-technical stakeholders—product owners,
customers, etc. RSpec (inspired by RBehave) brought the story-driven approach to
the masses, and in the process, many other frameworks came along, including the
famous Cucumber.
There is also a dark side to this story: many frameworks have been developed and
used solely by developers without working with non-technical stakeholders, in com-
plete opposition to the main ideas of BDD.
Today, to me, the term BDD frameworks mainly means “test frameworks with some
syntactic sugar,” since they are almost never used to create real conversations
between stakeholders and are almost always used as just another shiny or pre-
scribed tool for performing developer-based automated tests. I’ve even seen the
mighty Cucumber fall into this pattern.
Listing 2.10
Refactoring a function to a stateful class


---
**Page 44**

44
CHAPTER 2
A first unit test
    });
    return errors;
  }
}
I’ve highlighted the main changes from listing 2.9. There’s nothing really special
going on here, though this may feel more comfortable if you’re coming from an
object-oriented background. It’s important to note that this is just one way to design
this functionality. I’m using the class-based approach so that I can show how this
design affects the test.
 In this new design, where are the entry and exit points for the current scenario?
Think about it for a second. The scope of the unit of work has increased. To test a sce-
nario with a failing rule, we would have to invoke two functions that affect the state of
the unit under test: addRule and verify.
 Now let’s see what the test might look like (changes are highlighted as usual).
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = new PasswordVerifier1();
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason'});
      verifier.addRule(fakeRule);
      const errors = verifier.verify('any value');
      expect(errors[0]).toContain('fake reason');
    });
  });
});
So far, so good; nothing fancy is happening here. Note that the surface of the unit of
work has increased. It now spans two related functions that must work together
(addRule and verify). There is a coupling that occurs due to the stateful nature of the
design. We need to use two functions to test productively without exposing any inter-
nal state from the object.
 The test itself looks innocent enough. But what happens when we want to write sev-
eral tests for the same scenario? That would happen if we have multiple exit points, or
if we want to test multiple results from the same exit point. For example, let’s say we
want to verify that we have only a single error. We could simply add a line to the test
like this:
verifier.addRule(fakeRule);
const errors = verifier.verify('any value');
expect(errors.length).toBe(1);       
expect(errors[0]).toContain('fake reason');
Listing 2.11
Testing the stateful unit of work
A new 
assertion


---
**Page 45**

45
2.6
Trying the beforeEach() route
What happens if the new assertion fails? The second assertion would never execute,
because the test runner would receive an error and move on to the next test case.
 We’d still want to know if the second assertion would have passed, right? So maybe
we’d start commenting out the first one and rerunning the test. That’s not a healthy
way to run your tests. In Gerard Meszaros’ book xUnit Test Patterns, this human behav-
ior of commenting things out to test other things is called assertion roulette. It can cre-
ate lots of confusion and false positives in your test runs (thinking that something is
failing or passing when it isn’t).
 I’d rather separate this extra check into its own test case with a good name, as follows.
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = new PasswordVerifier1();
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason'});
      verifier.addRule(fakeRule);
      const errors = verifier.verify('any value');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const verifier = new PasswordVerifier1();
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason'});
      verifier.addRule(fakeRule);
      const errors = verifier.verify('any value');
      expect(errors.length).toBe(1);
    });
  });
});
This is starting to look bad. Yes, we have solved the assertion roulette issue. Each it()
can fail separately and not interfere with the results from the other test case. But what
did it cost? Everything. Look at all the duplication we have now. At this point, those of
you with some unit testing background will start shouting at the book: “Use a
setup/beforeEach method!”
 Fine!
2.6
Trying the beforeEach() route
I haven’t introduced beforeEach() yet. This function and its sibling, afterEach(),
are used to set up and tear down a specific state required by the test cases. There’s also
beforeAll() and afterAll(), which I try to avoid using at all costs for unit testing sce-
narios. We’ll talk more about the siblings later in the book. 
Listing 2.12
Checking an extra end result from the same exit point


---
**Page 46**

46
CHAPTER 2
A first unit test
 beforeEach() can help us remove duplication in our tests because it runs once
before each test in the describe block in which we nest it. We can also nest it multiple
times, as the following listing demonstrates.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());   
  describe('with a failing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {                             
      fakeRule = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRule);
    });
    it('has an error message based on the rule.reason', () => {
      const errors = verifier.verify('any value');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const errors = verifier.verify('any value');
      expect(errors.length).toBe(1);
    });
  });
});
Look at all that extracted code. 
 In the first beforeEach(), we’re setting up a new PasswordVerifier1 that will be
created for each test case. In the beforeEach() after that, we’re setting up a fake rule
and adding it to the new verifier for every test case under that specific scenario. If we
had other scenarios, the second beforeEach() in line 6 wouldn’t run for them, but
the first one would.
 The tests seem shorter now, which ideally is what you want in a test, to make it
more readable and maintainable. We removed the creation line from each test and
reused the same higher-level variable verifier. 
 There are a couple of caveats:
We forgot to reset the errors array in beforeEach() on line 6. That could bite
us later on. 
Jest runs unit tests in parallel by default. This means that moving the verifier to
line 2 may cause an issue with parallel tests, where the verifier could be over-
written by a different test on a parallel run, which would screw up the state of
our running test. Jest is quite different from unit test frameworks in most other
languages I know, which make a point of running tests in a single thread, not in
parallel (at least by default), to avoid such issues. With Jest, we have to remem-
ber that parallel tests are a reality, so stateful tests with a shared upper state, like
Listing 2.13
Using beforeEach() on two levels
Setting up a new 
verifier that will be 
used in each test
Setting up a fake
rule that will be
used within this
describe() method


---
**Page 47**

47
2.6
Trying the beforeEach() route
we have at line 2, can potentially be problematic and cause flaky tests that fail
for unknown reasons.
We’ll correct both of these issues soon.
2.6.1
beforeEach() and scroll fatigue
We lost a couple of things in the process of refactoring to beforeEach():
If I’m trying to read only the it() parts, I can’t tell where the verifier is cre-
ated and declared. I’d have to scroll up to understand.
The same goes for understanding what rule was added. I’d have to look one
level above the it() to see what rule was added, or look up the describe()
block description. 
Right now, this doesn’t seem so bad. But we’ll see later that this structure starts to get a
bit hairy as the scenario list increases in size. Larger files can bring about what I like to
call scroll fatigue, requiring the test reader to scroll up and down the test file to under-
stand the context and state of the tests. This makes maintaining and reading the tests
a chore instead of a simple act of reading. 
 This nesting is great for reporting, but it sucks for humans who have to keep look-
ing up where something came from. If you’ve ever tried to debug CSS styles in the
browser’s inspector window, you’ll know the feeling. You’ll see that a specific cell is
bold for some reason. Then you scroll up to see which style made that <div> inside
nested cells in a special table under the third node bold.
 Let’s see what happens when we take it one step further in the following listing.
Since we’re in the process of removing duplication, we can also call verify in
beforeEach() and remove an extra line from each it(). This is basically putting the
arrange and act parts from the AAA pattern into the beforeEach() function.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {
      fakeRule = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRule);
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
});
Listing 2.14
Pushing the arrange and act parts into beforeEach()


---
**Page 48**

48
CHAPTER 2
A first unit test
The code duplication has been reduced to a minimum, but now we also need to look
up where and how we got the errors array if we want to understand each it(). 
 Let’s double down and add a few more basic scenarios, and see if this approach is
scalable as the problem space increases.
describe('v6 PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {
      fakeRule = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRule);
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {
      fakeRule = input => ({passed: true, reason: ''});
      verifier.addRule(fakeRule);
      errors = verifier.verify('any value');
    });
    it('has no errors', () => {
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    let fakeRulePass,fakeRuleFail, errors;
    beforeEach(() => {
      fakeRulePass = input => ({passed: true, reason: 'fake success'});
      fakeRuleFail = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRulePass);
      verifier.addRule(fakeRuleFail);
      errors = verifier.verify('any value');
    });
    it('has one error', () => {
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Listing 2.15
Adding extra scenarios


---
**Page 49**

49
2.7
Trying the factory method route
Do we like this? I don’t. Now we’re seeing a couple of extra problems:
I can already start to see lots of repetition in the beforeEach() parts.
The potential for scroll fatigue has increased dramatically, with more options of
which beforeEach() affects which it() state.
In real projects, beforeEach() functions tend to be the garbage bin of the test file.
People throw all kinds of test-initialized stuff in there: things that only some tests need,
things that affect all the other tests, and things that nobody uses anymore. It’s human
nature to put things in the easiest place possible, especially if everyone else before you
has done so as well. 
 I’m not crazy about the beforeEach() approach. Let’s see if we can mitigate some
of these issues while still keeping duplication to a minimum. 
2.7
Trying the factory method route
Factory methods are simple helper functions that help us build objects or special states
and reuse the same logic in multiple places. Perhaps we can reduce some of the dupli-
cation and clunky-feeling code by using a couple of factory methods for the failing
and passing rules in listing 2.16.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makeFailingRule('fake reason'));
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makePassingRule());
      errors = verifier.verify('any value');
    });
    it('has no errors', () => {
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    let errors;
Listing 2.16
Adding a couple of factory methods to the mix


---
**Page 50**

50
CHAPTER 2
A first unit test
    beforeEach(() => {
      verifier.addRule(makePassingRule());
      verifier.addRule(makeFailingRule('fake reason'));
      errors = verifier.verify('any value');
    });
    it('has one error', () => {
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      expect(errors[0]).toContain('fake reason');
    });
  });
. . .
  const makeFailingRule = (reason) => {
    return (input) => {
      return { passed: false, reason: reason };
    };
  };
  const makePassingRule = () => (input) => {
    return { passed: true, reason: '' };
  };
}) 
The makeFailingRule() and makePassingRule() factory methods have made our
beforeEach() functions a little more clear.
2.7.1
Replacing beforeEach() completely with factory methods
What if we don’t use beforeEach() to initialize various things at all? What if we
switched to using small factory methods instead? Let’s see what that looks like.
const makeVerifier = () => new PasswordVerifier1();
const passingRule = (input) => ({passed: true, reason: ''});
const makeVerifierWithPassingRule = () => {
  const verifier = makeVerifier();
  verifier.addRule(passingRule);
  return verifier;
};
const makeVerifierWithFailedRule = (reason) => {
  const verifier = makeVerifier();
  const fakeRule = input => ({passed: false, reason: reason});
  verifier.addRule(fakeRule);
  return verifier;
};
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
Listing 2.17
Replacing beforeEach() with factory methods


---
**Page 51**

51
2.7
Trying the factory method route
      const errors = verifier.verify('any input');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    it('has no errors', () => {
      const verifier = makeVerifierWithPassingRule();
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    it('has one error', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      verifier.addRule(passingRule);
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      verifier.addRule(passingRule);
      const errors = verifier.verify('any input');
      expect(errors[0]).toContain('fake reason');
    });
  });
});
The length here is about the same as in listing 2.16, but I find the code to be more
readable and thus more easily maintained. We’ve eliminated the beforeEach() func-
tions, but we didn’t lose maintainability. The amount of repetition we’ve eliminated is
negligible, but the readability has improved greatly due to the removal of the nested
beforeEach() blocks. 
 Furthermore, we’ve reduced the risk of scroll fatigue. As a reader of the test, I
don’t have to scroll up and down the file to find out when an object is created or
declared. I can glean all the information from the it(). We don’t need to know how
something is created, but we know when it is created and what important parameters it
is initialized with. Everything is explicitly explained.
 If the need arises, I can drill into specific factory methods, and I like that each
it() is encapsulating its own state. The nested describe() structure is a good way to
know where we are, but the state is all triggered from inside the it() blocks, not out-
side of them.


---
**Page 52**

52
CHAPTER 2
A first unit test
2.8
Going full circle to test()
The tests in listing 2.17 are self-encapsulated enough that the describe() blocks act
only as added sugar for understanding. They are no longer needed if we don’t want
them. If we wanted to, we could write the tests as in the following listing.
test('pass verifier, with failed rule, ' +
          'has an error message based on the rule.reason', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  const errors = verifier.verify('any input');
  expect(errors[0]).toContain('fake reason');
});
test('pass verifier, with failed rule, has exactly one error', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(1);
});
test('pass verifier, with passing rule, has no errors', () => {
  const verifier = makeVerifierWithPassingRule();
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(0);
});
test('pass verifier, with passing  and failing rule,' +
          ' has one error', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  verifier.addRule(passingRule);
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(1);
});
test('pass verifier, with passing  and failing rule,' +
          ' error text belongs to failed rule', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  verifier.addRule(passingRule);
  const errors = verifier.verify('any input');
  expect(errors[0]).toContain('fake reason');
});
The factory methods provide us with all the functionality we need, without losing clar-
ity for each specific test. 
 I kind of like the terseness of listing 2.18. It’s easy to understand. We might lose a
bit of structure clarity here, so there are instances where I go with the describe-less
approach, and there are places where nested describes make things more readable.
The sweet spot of maintainability and readability for your project is probably some-
where between these two points. 
2.9
Refactoring to parameterized tests
Let’s move away from the verifier class to work on creating and testing a new custom
rule for the verifier. Listing 2.19 shows a simple rule for an uppercase letter (I realize
Listing 2.18
Removing nested describes


---
**Page 53**

53
2.9
Refactoring to parameterized tests
passwords with these requirements are no longer considered a great idea, but for
demonstration purposes I’m okay with it).
const oneUpperCaseRule = (input) => {
  return {
    passed: (input.toLowerCase() !== input),
    reason: 'at least one upper case needed'
  };
};
We could write a couple of tests as in the following listing.
describe('one uppercase rule', function () {
  test('given no uppercase, it fails', () => {
    const result = oneUpperCaseRule('abc');
    expect(result.passed).toEqual(false);
  });
  test('given one uppercase, it passes', () => {
    const result = oneUpperCaseRule('Abc');
    expect(result.passed).toEqual(true);
  });
  test('given a different uppercase, it passes', () => {
    const result = oneUpperCaseRule('aBc');
    expect(result.passed).toEqual(true);
  });
});
In listing 2.20 I highlighted some duplication we might have if we’re trying out the
same scenario with small variations in the input to the unit of work. In this case, we
want to test that it should not matter where the uppercase letter is, as long as it’s there.
But this duplication will hurt us down the road if we ever want to change the upper-
case logic, or if we need to correct the assertions in some way for that use case.
 There are a few ways to create parameterized tests in JavaScript, and Jest already
includes one that’s built in: test.each (also aliased to it.each). The next listing
shows how we could use this feature to remove duplication in our tests.
describe('one uppercase rule', () => {
  test('given no uppercase, it fails', () => {
    const result = oneUpperCaseRule('abc');
    expect(result.passed).toEqual(false);
  });
  test.each(['Abc',        
             'aBc'])       
    ('given one uppercase, it passes', (input) => {    
Listing 2.19
Password rules
Listing 2.20
Testing a rule with variations
Listing 2.21
Using test.each
Passing in an array 
of values that are 
mapped to the 
input parameter
Using each input 
parameter passed 
in the array


---
**Page 54**

54
CHAPTER 2
A first unit test
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(true);
    });
});
In this example, the test will repeat once for each value in the array. It’s a bit of a
mouthful at first, but once you’ve tried this approach, it becomes easy to use. It’s also
pretty readable. 
 If we want to pass in multiple parameters, we can enclose them in an array, as in
the following listing.
describe('one uppercase rule', () => {
  test.each([ ['Abc', true],           
              ['aBc', true],
              ['abc', false]])           
    ('given %s, %s ', (input, expected) => {   
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(expected);
    });
});
We don’t have to use Jest, though. JavaScript is versatile enough to allow us to roll out
our own parameterized test quite easily if we want to.
describe('one uppercase rule, with vanilla JS for', () => {
  const tests = {
    'Abc': true,
    'aBc': true,
    'abc': false,
  };
  for (const [input, expected] of Object.entries(tests)) {
    test('given ${input}, ${expected}', () => {
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(expected);
    });
  }
});
It’s up to you which one you want to use (I like to keep it simple and use test.each).
The point is, Jest is just a tool. The pattern of parameterized tests can be implemented
in multiple ways. This pattern gives us a lot of power, but also a lot of responsibility. It’s
really easy to abuse this technique and create tests that are harder to understand.
 I usually try to make sure that the same scenario (type of input) holds for the
entire table. If I were reviewing this test in a code review, I would have told the person
Listing 2.22
Refactoring test.each
Listing 2.23
Using a vanilla JavaScript for
Providing three arrays, 
each with two parameters
A new false expectation for a 
missing uppercase character
Jest maps the array values 
to arguments automatically.


---
**Page 55**

55
2.10
Checking for expected thrown errors
who wrote it that this test is actually testing two different scenarios: one with no upper-
case, and a couple with one uppercase. I would split those out into two different tests.
 In this example, I wanted to show that it’s very easy to get rid of many tests and put
them all in a big test.each—even when it hurts readability—so be careful when run-
ning with these specific scissors.
2.10
Checking for expected thrown errors
Sometimes we need to design a piece of code that throws an error at the right time
with the right data. What happens if we add code to the verify function that throws
an error if there are no rules configured, as in the next listing?
verify (input) {
  if (this.rules.length === 0) {
    throw new Error('There are no rules configured');
  }
  . . .
We could test it the old-fashioned way by using try/catch, and failing the test if we
don’t get an error.
test('verify, with no rules, throws exception', () => {
    const verifier = makeVerifier();
    try {
        verifier.verify('any input');
        fail('error was expected but not thrown');
    } catch (e) {
        expect(e.message).toContain('no rules configured');
    }
});
This try/catch pattern is an effective method but very verbose and annoying to type.
Jest, like most other frameworks, contains a shortcut to accomplish exactly this type of
scenario, using expect().toThrowError().
Listing 2.24
Throwing an error
Listing 2.25
Testing exceptions with try/catch
Using fail()
Technically, fail() is a leftover API from the original fork of Jasmine, which Jest is
based on. It’s a way to trigger a test failure, but it’s not in the official Jest API docs,
and they would recommend that you use expect.assertions(1) instead. This
would fail the test if you never reached the catch() expectation. I find that as long
as fail() still works, it does the job quite nicely for my purposes, which are to
demonstrate why you shouldn’t use the try/catch construct in a unit test if you can
help it.


---
**Page 56**

56
CHAPTER 2
A first unit test
test('verify, with no rules, throws exception', () => {
    const verifier = makeVerifier();
    expect(() => verifier.verify('any input'))
        .toThrowError(/no rules configured/);   
});
Notice that I’m using a regular expression match to check that the error string con-
tains a specific string, and is not equal to it, so as to make the test a bit more future-
proof if the string changes on its sides. toThrowError has a few variations, and you can
go to https://jestjs.io/ find out all about them.
2.11
Setting test categories
If you’d like to run only a specific category of tests, such as only unit tests, or only inte-
gration tests, or only tests that touch a specific part of the application, Jest currently
doesn’t have the ability to define test case categories.
 All is not lost, though. Jest has a special --testPathPattern command-line flag,
which allows us to define how Jest will find our tests. We can trigger this command
with a different path for a specific type of test we’d like to run (such as “all tests under
the ‘integration’ folder”). You can get the full details at https://jestjs.io/docs/en/cli.
 Another alternative is to create a separate jest.config.js file for each test category,
each with its own testRegex configuration and other properties.
Listing 2.26
Using expect().toThrowError()
Jest snapshots
Jest has a unique feature called Snapshots. It allows you to render a component
(when working in a framework like React) and then match the current rendering to a
saved snapshot of that component, including all of its properties and HTML. 
I won’t be touching on this too much, but from what I’ve seen, this feature tends to
be abused quite heavily. You can use it to create hard-to-read tests that look some-
thing like this:
it('renders',()=>{
    expect(<MyComponent/>).toMatchSnapshot(); 
});
This is obtuse (hard to reason about what is being tested) and it’s testing many
things that might not be related to one another. It will also break for many reasons
that you might not care about, so the maintainability cost of that test will be higher
over time. It’s also a great excuse not to write readable and maintainable tests,
because you’re on a deadline but still have to show you write tests. Yes, it does serve
a purpose, but it’s easy to use in places where other types of tests are more relevant. 
If you need a variation of this, try using toMatchInlineSnapshot() instead. You can
find more info at https://jestjs.io/docs/en/snapshot-testing.
Using a regular expression 
instead of looking for the 
exact string


---
**Page 57**

57
Summary
// jest.config.integration.js
var config = require('./jest.config')
config.testRegex = "integration\\.js$" 
module.exports = config
// jest.config.unit.js
var config = require('./jest.config')
config.testRegex = "unit\\.js$" 
module.exports = config
Then, for each category, you can create a separate npm script that invokes the Jest
command line with a custom config file: jest -c my.custom.jest.config.js.
//Package.json
. . .
"scripts": {
    "unit": "jest -c jest.config.unit.js",
    "integ": "jest -c jest.config.integration.js"
. . .
In the next chapter, we’ll look at code that has dependencies and testability problems,
and we’ll start discussing the idea of fakes, spies, mocks, and stubs, and how you can
use them to write tests against such code.
Summary
Jest is a popular, open source test framework for JavaScript applications. It
simultaneously acts as a test library to use when writing tests, an assertion library
for asserting inside the tests, a test runner, and a test reporter.
Arrange-Act-Assert (AAA) is a popular pattern for structuring tests. It provides a
simple, uniform layout for all tests. Once you get used to it, you can easily read
and understand any test.
In the AAA pattern, the arrange section is where you bring the system under test
and its dependencies to a desired state. In the act section, you call methods,
pass the prepared dependencies, and capture the output value (if any). In the
assert section, you verify the outcome.
A good pattern for naming tests is to include in the name of the test the unit
of work under test, the scenario or inputs to the unit, and the expected behav-
ior or exit point. A handy mnemonic for this pattern is USE (unit, scenario,
expectation).
Jest provides several functions that help create more structure around multiple
related tests. describe() is a scoping function that allows for grouping multiple
tests (or groups of tests) together. A good metaphor for describe() is a folder
Listing 2.27
Creating separate jest.config.js files
Listing 2.28
Using separate npm scripts


---
**Page 58**

58
CHAPTER 2
A first unit test
containing tests or other folders. test() is a function denoting an individual
test. it() is an alias for test(), but it provides better readability when used in
combination with describe().

beforeEach() helps avoid duplication by extracting code that is common for
the nested describe and it functions.
The use of beforeEach() often leads to scroll fatigue, when you have to look at
various places to understand what a test does.
Factory methods with plain tests (without any beforeEach()) improve readability
and help avoid scroll fatigue.
Parameterized tests help reduce the amount of code needed for similar tests. The
drawback is that the tests become less readable as you make them more generic.
To maintain a balance between test readability and code reuse, only parameter-
ize input values. Create separate tests for different output values.
Jest doesn’t support test categories, but you can run groups of tests using the
--testPathPattern flag. You can also set up testRegex in the configuration file.


---
**Page 59**

Part 2
Core techniques
Having covered the basics in part 1, I’ll now introduce the core testing
and refactoring techniques necessary for writing tests in the real world.
 In chapter 3, we’ll examine stubs and how they help break dependencies.
We’ll go over refactoring techniques that make code more testable, and you’ll
learn about seams in the process.
 In chapter 4, we’ll move on to mock objects and interaction testing, we’ll look
at how mock objects differ from stubs, and we’ll explore the concept of fakes.
 In chapter 5, we’ll look at isolation frameworks, also known as mocking
frameworks, and at how they solve some of the repetitive coding involved in
handwritten mocks and stubs. Chapter 6 deals with asynchronous code, such as
promises, timers, and events, and various approaches to testing such code. 


---
**Page 60**



---
**Page 61**

61
Breaking dependencies
with stubs
In the previous chapter, you wrote your first unit test using Jest, and we looked
more at the maintainability of the test itself. The scenario was pretty simple, and
more importantly, it was completely self-contained. The Password Verifier had no
reliance on outside modules, and we could focus on its functionality without worry-
ing about other things that might interfere with it. 
 In that chapter, we used the first two types of exit points for our examples:
return value exit points and state-based exit points. In this chapter, we’ll talk about
the final type—calling a third party. This chapter will also present a new require-
ment—having your code rely on time. We’ll look at two different approaches to
handling it—refactoring our code and monkey-patching it without refactoring.
 The reliance on outside modules or functions can and will make it harder to
write a test and to make the test repeatable, and it can also cause tests to be flaky.
This chapter covers
Types of dependencies—mocks, stubs, and more
Reasons to use stubs
Functional injection techniques
Modular injection techniques
Object-oriented injection techniques


