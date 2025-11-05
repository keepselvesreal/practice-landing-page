# 12.2.1 Pros and cons of the easy-first strategy (pp.234-234)

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


