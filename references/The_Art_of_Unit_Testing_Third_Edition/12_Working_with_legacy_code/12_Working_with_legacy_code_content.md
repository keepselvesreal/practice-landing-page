
--- 페이지 259 ---
231
Working with legacy code
I once consulted for a large development shop that produced billing software.
They had over 10,000 developers and mixed .NET, Java, and C++ in products, sub-
products, and intertwined projects. The software had existed in one form or
another for over five years, and most of the developers were tasked with maintain-
ing and building on top of existing functionality. 
 My job was to help several divisions (using all languages) learn TDD techniques.
For about 90% of the developers I worked with, this never became a reality for sev-
eral reasons, some of which were a result of legacy code:
It was difficult to write tests against existing code.
It was next to impossible to refactor the existing code (or there wasn’t
enough time to do it).
Some people didn’t want to change their designs.
Tooling (or a lack of tooling) was getting in the way.
It was difficult to determine where to begin.
This chapter covers
Examining common problems with legacy code
Deciding where to begin writing tests

--- 페이지 260 ---
232
CHAPTER 12
Working with legacy code
Anyone who’s ever tried to add tests to an existing system knows that most such sys-
tems are almost impossible to write tests for. They were usually written without proper
places (called seams) in the software to allow extensions or replacements to existing
components.
 There are two problems that need to be addressed when dealing with legacy code:
There’s so much work, where should you start to add tests? Where should you
focus your efforts?
How can you safely refactor your code if it has no tests to begin with?
This chapter will tackle these tough questions associated with approaching legacy
codebases by listing techniques, references, and tools that can help.
12.1
Where do you start adding tests?
Assuming you have existing code inside components, you’ll need to create a priority
list of components for which testing makes the most sense. There are several factors to
consider that can affect each component’s priority:
Logical complexity —This refers to the amount of logic in the component, such as
nested ifs, switch cases, or recursion. Such complexity is also called cyclomatic
complexity, and you can use various tools to check it automatically.
Dependency level—This refers to the number of dependencies in the component.
How many dependencies do you have to break in order to bring this class under
test? Does it communicate with an outside email component, perhaps, or does
it call a static log method somewhere?
Priority—This is the component’s general priority in the project.
You can give each component a rating for these factors, from 1 (low priority) to 10
(high priority). Table 12.1 shows classes with ratings for these factors. I call this a test-
feasibility table.
Table 12.1
A simple test-feasibility table
Component
Logical 
complexity
Dependency 
level
Priority
Notes
Utils
6
1
5
This utility class has few dependencies 
but contains a lot of logic. It will be easy 
to test, and it provides lots of value.
Person
2
1
1
This is a data-holder class with little 
logic and no dependencies. There’s 
little real value in testing this.
TextParser
8
4
6
This class has lots of logic and lots of 
dependencies. To top it off, it’s part of 
a high-priority task in the project. Test-
ing this will provide lots of value but 
will also be hard and time consuming.

--- 페이지 261 ---
233
12.1
Where do you start adding tests?
From the data in table 12.1, you can create a diagram like the one shown in figure 12.1,
which graphs your components by the amount of value to the project and number of
dependencies. You can safely ignore items that are below your designated threshold of
logic (which I usually set at 2 or 3), so Person and ConfigManager can be ignored.
You’re left with only the top two components in figure 12.1.
 There are two basic ways to look at the graph and decide what you’d like to test
first (see figure 12.2):
Choose the one that’s more complex and easier to test (top left).
Choose the one that’s more complex and harder to test (top right).
The question now is what path you should take. Should you start with the easy stuff or
the hard stuff?
ConfigManager
1
6
1
This class holds configuration data 
and reads files from disk. It has little 
logic but many dependencies. Testing 
it will provide little value to the proj-
ect and will also be hard and time 
consuming.
Table 12.1
A simple test-feasibility table (continued)
Component
Logical 
complexity
Dependency 
level
Priority
Notes
Utils
Person
TextParser
ConfigManager
Logic
Dependencies
Figure 12.1
Mapping components for test 
feasibility
Logic-driven
(easy to test)
Dependency-
driven
(hard to test)
Ignore
Logic
Dependencies
Figure 12.2
Easy, hard, and irrelevant 
component mapping based on logic and 
dependencies

--- 페이지 262 ---
234
CHAPTER 12
Working with legacy code
12.2
Choosing a selection strategy
As the previous section explained, you can start with the components that are easy to
test or the ones that are hard to test (because they have many dependencies). Each
strategy presents different challenges. 
12.2.1 Pros and cons of the easy-first strategy
Starting out with the components that have fewer dependencies will make writing the
tests initially much quicker and easier. But there’s a catch, as figure 12.3 demonstrates.
Figure 12.3 shows how long it takes to bring components under test during the life-
time of the project. Initially it’s easy to write tests, but as time goes by, you’re left with
components that are increasingly harder and harder to test, with the particularly
tough ones waiting for you at the end of the project cycle, just when everyone is
stressed about pushing a product out the door.
 If your team is relatively new to unit testing techniques, it’s worth starting with the
easy components. As time goes by, the team will learn the techniques needed to deal
with the more complex components and dependencies. For such a team, it may be
wise to initially avoid all components over a specific number of dependencies (with
four being a reasonable limit).
12.2.2 Pros and cons of the hard-first strategy
Starting with the more difficult components may seem like a losing proposition ini-
tially, but it has an upside as long as your team has experience with unit testing tech-
niques. Figure 12.4 shows the average time to write a test for a single component over
the lifetime of the project, if you start testing the components with the most depen-
dencies first.
 With this strategy, you could be spending a day or more to get even the simplest
tests going on the more complex components. But notice the quick decline in the
time required to write the tests relative to the slow incline in figure 12.3. Every time
you bring a component under test and refactor it to make it more testable, you may
Time to
write
test
Project lifetime
Figure 12.3
When starting with the easy 
components, the time required to test 
components increases more and more until 
the hardest components are done.

--- 페이지 263 ---
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

--- 페이지 264 ---
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

--- 페이지 265 ---
237
Summary
If your team has little or no experience in unit testing, it’s a good idea to start
with the easy components and let the team’s confidence grow as they add more
and more tests to the system.
If your team is experienced, getting the hard components under test first can
help you get through the rest of the system more quickly.
Before a large-scale refactoring, write integration tests that will sustain that
refactoring mostly unchanged. After the refactoring is completed, replace most
of these integration tests with smaller and more maintainable unit tests.
