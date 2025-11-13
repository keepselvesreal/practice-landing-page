# 5.1.1 Choosing a flavor: Loose vs. typed (pp.105-106)

---
**Page 105**

105
5.1
Defining isolation frameworks
mocks and stubs. In this chapter, we’ll take a look at a few of the JavaScript frameworks
available and how we can use them in modular, functional, and object-oriented
designs. You’ll see how you can use such frameworks to test various things and to cre-
ate stubs, mocks, and other interesting things.
 But the specific frameworks I’ll present here aren’t the point. While using them,
you’ll see the values that their APIs promote in your tests (readability, maintainability,
robust and long-lasting tests, and more), and you’ll find out what makes an isolation
framework good and, alternatively, what can make it a drawback for your tests.
5.1
Defining isolation frameworks
I’ll start with a basic definition that may sound a bit bland, but it needs to be generic
in order to include the various isolation frameworks out there: 
An isolation framework is a set of programmable APIs that allow the dynamic creation,
configuration, and verification of mocks and stubs, either in object or function form.
When using an isolation framework, these tasks are often simpler, quicker, and produce
shorter code than hand-coded mocks and stubs.
Isolation frameworks, when used properly, can save developers from the need to write
repetitive code to assert or simulate object interactions, and if applied in the right
places, they can help make tests last many years without requiring a developer to come
back and fix them after every little production code change. If they’re applied badly,
they can cause confusion and full-on abuse of these frameworks, to the point where
we either can’t read or can’t trust our own tests, so be wary. I’ll discuss some dos and
don’ts in part 3 of this book.
5.1.1
Choosing a flavor: Loose vs. typed 
Because JavaScript supports multiple paradigms of programming design, we can split
the frameworks in our world into two main flavors:
Loose JavaScript isolation frameworks—These are vanilla JavaScript-friendly loose-
typed isolation frameworks (such as Jest and Sinon). These frameworks usually
also lend themselves better to more functional styles of code because they
require less ceremony and boilerplate code to do their work.
Typed JavaScript isolation frameworks—These are more object-oriented and Type-
Script-friendly isolation frameworks (such as substitute.js). They’re very useful
when dealing with whole classes and interfaces.
Which flavor you end up choosing to use in your project will depend on a few things,
like taste, style, and readability, but the main question to start with is, what type of
dependencies will you mostly need to fake?
Module dependencies (imports, requires)—Jest and other loosely typed frameworks
should work well.
Functional (single and higher-order functions, simple parameters and values)—Jest and
other loosely typed frameworks should work well.


---
**Page 106**

106
CHAPTER 5
Isolation frameworks
Full objects, object hierarchies, and interfaces—Look into the more object-oriented
frameworks, such as substitute.js.
Let’s go back to our Password Verifier and see how we can fake the same types of
dependencies we did in previous chapters, but this time using a framework.
5.2
Faking modules dynamically
For people who are trying to test code with direct dependencies on modules using
require or import, isolation frameworks such as Jest or Sinon present the powerful
ability to fake an entire module dynamically, with very little code. Since we started with
Jest as our test framework, we’ll stick with it for the examples in this chapter.
 Figure 5.1 illustrates a Password Verifier with two dependencies:
A configuration service that helps decide what the logging level is (INFO or ERROR)
A logging service that we call as the exit point of our unit of work, whenever we
verify a password
The arrows represent the flow of behavior through the unit of work. Another way to
think about the arrows is through the terms command and query. We are querying the
configuration service (to get the log level), but we are sending commands to the log-
ger (to log).
The following listing shows a Password Verifier that has a hard dependency on a log-
ger module.
 
Command/query separation
There is a school of design that falls under the ideas of command/query separation. If
you’d like to learn more about these terms, I highly recommend reading Martin Fowler’s
2005 article on the topic, at https://martinfowler.com/bliki/CommandQuerySeparation
.html. This pattern is very beneficial as you navigate your way around different design
ideas, but we won’t be touching on this too much in this book.
Import
Import
Password
Verifier
configuration-service.js
complicated-logger.js
info()
getLogLevel(): string
Figure 5.1
Password Verifier has two dependencies: an incoming one to determine the logging level, and an 
outgoing one to create a log entry.


