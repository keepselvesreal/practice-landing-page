# 12.3.1 Read Michael Feathers’ book on legacy code (pp.236-236)

---
**Page 236**

236
CHAPTER 12
Working with legacy code
 As you can see, the process is relatively simple:
Add one or more integration tests (no mocks or stubs) to the system to prove
the original system works as needed.
Refactor or add a failing test for the feature you’re trying to add to the system.
Refactor and change the system in small chunks, and run the integration tests
as often as you can, to see if you break something.
Sometimes, integration tests may seem easier to write than unit tests, because you
don’t need to understand the internal structure of the code or where to inject various
dependencies. But making those tests run on your local system may prove annoying or
time consuming because you have to make sure every little thing the system needs is
in place.
 The trick is to work on the parts of the system that you need to fix or add features
to. Don’t focus on the other parts. That way, the system grows in the right places, leav-
ing other bridges to be crossed when you get to them.
 As you continue adding more and more tests, you can refactor the system and add
more unit tests to it, growing it into a more maintainable and testable system. This
takes time (sometimes months and months), but it’s worth it.
 Chapter 7 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov
(Manning, 2020) contains an in-depth example of such refactoring. Refer to that
book for more details.
12.3.1 Read Michael Feathers’ book on legacy code
Working Effectively with Legacy Code by Michael Feathers (Pearson, 2004) is another valu-
able source that deals with the issues you’ll encounter with legacy code. It shows many
refactoring techniques and gotchas in depth that this book doesn’t attempt to cover.
It’s worth its weight in gold. Get it. 
12.3.2 Use CodeScene to investigate your production code
Another tool called CodeScene allows you to discover lots of technical debt and hid-
den issues in legacy code, among many other things. It is a commercial tool, and while
I have not personally used it, I've heard great things. You can learn more about it at
https://codescene.com/. 
Summary
Before starting to write tests for legacy code, it’s important to map out the vari-
ous components according to their number of dependencies, their amount of
logic, and each component’s general priority in the project. A component’s log-
ical complexity (or cyclomatic complexity) refers to the amount of logic in the
component, such as nested ifs, switch cases, or recursion. 
Once you have that information, you can choose the components to work on
based on how easy or how hard it will be to get them under test.


