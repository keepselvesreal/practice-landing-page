# 5.0 Introduction [auto-generated] (pp.104-105)

---
**Page 104**

104
Isolation frameworks
In the previous chapters, we looked at writing mocks and stubs manually and saw
the challenges involved, especially when the interface we’d like to fake requires us
to create long, error prone, repetitive code. We kept having to declare custom vari-
ables, create custom functions, or inherit from classes that use those variables and
basically make things a bit more complicated than they need to be (most of the
time).
 In this chapter, we’ll look at some elegant solutions to these problems in the
form of an isolation framework—a reusable library that can create and configure fake
objects at run time. These objects are referred to as dynamic stubs and dynamic mocks.
 I call them isolation frameworks because they allow you to isolate the unit of
work from its dependencies. You’ll find that many resources will refer to them as
“mocking frameworks,” but I try to avoid that because they can be used for both
This chapter covers
Defining isolation frameworks and how they help
Two main flavors of frameworks
Faking modules with Jest
Faking functions with Jest 
Object-oriented fakes with substitute.js


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


