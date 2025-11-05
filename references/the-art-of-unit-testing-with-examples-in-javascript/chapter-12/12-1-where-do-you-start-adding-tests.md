# 12.1 Where do you start adding tests? (pp.232-234)

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


---
**Page 233**

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


---
**Page 234**

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


