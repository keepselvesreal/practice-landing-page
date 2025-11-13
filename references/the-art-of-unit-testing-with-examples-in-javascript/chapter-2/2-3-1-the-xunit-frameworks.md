# 2.3.1 The xUnit frameworks (pp.36-36)

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


