# 2.3.0 Introduction [auto-generated] (pp.34-36)

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


