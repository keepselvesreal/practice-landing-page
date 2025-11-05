# 4.10 Summary (pp.103-104)

---
**Page 103**

103
Summary
from classes that you’re directly testing. We’ll touch more on that later in the book
when we talk about legacy code and refactoring techniques.
Summary
Interaction testing is a way to check how a unit of work interacts with its outgoing
dependencies: what calls were made and with which parameters. Interaction
testing relates to the third type of exit points: a third-party module, object, or
system. (The first two types are a return value and a state change.)
To do interaction testing, you should use mocks, which are test doubles that replace
outgoing dependencies. Stubs replace incoming dependencies. You should ver-
ify interactions with mocks in tests, but not with stubs. Unlike with mocks, inter-
actions with stubs are implementation details and shouldn't be checked.
It’s OK to have multiple stubs in a test, but you don’t usually want to have more
than a single mock per test, because that means you’re testing more than one
requirement in a single test.
Just like with stubs, there are multiple ways to inject a mock into a unit of work:
– Standard—By introducing a parameter
– Functional—Using a partial application or factory functions
– Modular—Abstracting the module dependency
– Object-oriented—Using an untyped object (in languages like JavaScript) or a
typed interface (in TypeScript)
In JavaScript, a complicated interface can be implemented partially, which
helps reduce the amount of boilerplate. There’s also the option of using partial
mocks, where you inherit from a real class and replace only some of its methods
with fakes.


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


