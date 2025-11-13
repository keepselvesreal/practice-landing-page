# 12.0 Introduction [auto-generated] (pp.231-232)

---
**Page 231**

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


---
**Page 232**

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


