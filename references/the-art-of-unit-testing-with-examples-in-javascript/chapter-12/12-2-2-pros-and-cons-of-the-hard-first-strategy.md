# 12.2.2 Pros and cons of the hard-first strategy (pp.234-235)

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


