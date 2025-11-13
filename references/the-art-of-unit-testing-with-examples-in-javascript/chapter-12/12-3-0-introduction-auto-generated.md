# 12.3.0 Introduction [auto-generated] (pp.235-236)

---
**Page 235**

235
12.3
Writing integration tests before refactoring
also be solving testability issues for the dependencies it uses or for other components.
Because that component has lots of dependencies, refactoring it can improve things
for other parts of the system. That’s the reason for the quick decline. 
 The hard-first strategy is only possible if your team has experience in unit testing
techniques, because it’s harder to implement. If your team does have experience, use
the priority aspect of components to choose whether to start with the hard or easy
components. You might want to choose a mix, but it’s important that you know in
advance how much effort will be involved and what the possible consequences are.
12.3
Writing integration tests before refactoring
If you do plan to refactor your code for testability (so you can write unit tests), a prac-
tical way to make sure you don’t break anything during the refactoring phase is to
write integration-style tests against your production system. 
 I consulted on a large legacy project, working with a developer who needed to
work on an XML configuration manager. The project had no tests and was hardly test-
able. It was also a C++ project, so we couldn’t use a tool to easily isolate components
from dependencies without refactoring the code.
 The developer needed to add another value attribute into the XML file and be
able to read and change it through the existing configuration component. We ended
up writing a couple of integration tests that used the real system to save and load con-
figuration data and that asserted on the values the configuration component was
retrieving and writing to the file. Those tests set the “original” working behavior of the
configuration manager as our base of work. 
 Next, we wrote an integration test that showed that once the component was reading
the file, it contained no attribute in memory with the name we were trying to add. We
proved that the feature was missing, and we now had a test that would pass once we
added the new attribute to the XML file and correctly wrote to it from the component.
 Once we wrote the code that saved and loaded the extra attribute, we ran the three
integration tests (two tests for the original base implementation and a new one that
tried to read the new attribute). All three passed, so we knew that we hadn’t broken
existing functionality while adding the new functionality. 
Time to
write
test
Project lifetime
Figure 12.4
When you use a hard-first 
strategy, the time required to test 
components is initially high, but then 
decreases as more dependencies are 
refactored away.


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


