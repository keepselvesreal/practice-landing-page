# 7.2.2 Take 1: Making implicit dependencies explicit (pp.160-160)

---
**Page 160**

160
CHAPTER 7
Refactoring toward valuable unit tests
often fails to scale as the code base grows. The reason is precisely this lack of separa-
tion between these two responsibilities: business logic and communication with out-of-
process dependencies. 
7.2.2
Take 1: Making implicit dependencies explicit
The usual approach to improve testability is to make implicit dependencies explicit:
that is, introduce interfaces for Database and MessageBus, inject those interfaces into
User, and then mock them in tests. This approach does help, and that’s exactly what
we did in the previous chapter when we introduced the implementation with mocks
for the audit system. However, it’s not enough.
 From the perspective of the types-of-code diagram, it doesn’t matter if the domain
model refers to out-of-process dependencies directly or via an interface. Such depen-
dencies are still out-of-process; they are proxies to data that is not yet in memory. You
still need to maintain complicated mock machinery in order to test such classes,
which increases the tests’ maintenance costs. Moreover, using mocks for the database
dependency would lead to test fragility (we’ll discuss this in the next chapter).
 Overall, it’s much cleaner for the domain model not to depend on out-of-process
collaborators at all, directly or indirectly (via an interface). That’s what the hexagonal
architecture advocates as well—the domain model shouldn’t be responsible for com-
munications with external systems. 
7.2.3
Take 2: Introducing an application services layer
To overcome the problem of the domain model directly communicating with external
systems, we need to shift this responsibility to another class, a humble controller (an
application service, in the hexagonal architecture taxonomy). As a general rule, domain
classes should only depend on in-process dependencies, such as other domain classes,
or plain values. Here’s what the first version of that application service looks like.
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
User class
Figure 7.7
The initial 
implementation of the User 
class scores highly on both 
dimensions and thus falls 
into the category of 
overcomplicated code.


