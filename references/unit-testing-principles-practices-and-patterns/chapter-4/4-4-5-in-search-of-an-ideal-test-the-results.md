# 4.4.5 In search of an ideal test: The results (pp.84-87)

---
**Page 84**

84
CHAPTER 4
The four pillars of a good unit test
This test makes sure the UserRepository class generates a correct SQL statement
when fetching a user from the database. Can this test catch a bug? It can. For exam-
ple, a developer can mess up the SQL code generation and mistakenly use ID instead
of UserID, and the test will point that out by raising a failure. But does this test have
good resistance to refactoring? Absolutely not. Here are different variations of the
SQL statement that lead to the same result:
SELECT * FROM dbo.[User] WHERE UserID = 5
SELECT * FROM dbo.User WHERE UserID = 5
SELECT UserID, Name, Email FROM dbo.[User] WHERE UserID = 5
SELECT * FROM dbo.[User] WHERE UserID = @UserID
The test in listing 4.6 will turn red if you change the SQL script to any of these varia-
tions, even though the functionality itself will remain operational. This is once again
an example of coupling the test to the SUT’s internal implementation details. The test
is focusing on hows instead of whats and thus ingrains the SUT’s implementation
details, preventing any further refactoring.
 Figure 4.8 shows that brittle tests fall into the third bucket. Such tests run fast and
provide good protection against regressions but have little resistance to refactoring. 
4.4.5
In search of an ideal test: The results
The first three attributes of a good unit test (protection against regressions, resistance to
refactoring, and fast feedback) are mutually exclusive. While it’s quite easy to come up
with a test that maximizes two out of these three attributes, you can only do that at the
expense of the third. Still, such a test would have a close-to-zero value due to the mul-
tiplication rule. Unfortunately, it’s impossible to create an ideal test that has a perfect
score in all three attributes (figure 4.9).
Resistance to
refactoring
Fast
feedback
Protection
against
regressions
End-to-end tests
Trivial tests
Brittle tests
Figure 4.8
Brittle tests run fast and they 
provide good protection against regressions, 
but they have little resistance to refactoring.


---
**Page 85**

85
In search of an ideal test
The fourth attribute, maintainability, is not correlated to the first three, with the excep-
tion of end-to-end tests. End-to-end tests are normally larger in size because of the
necessity to set up all the dependencies such tests reach out to. They also require addi-
tional effort to keep those dependencies operational. Hence end-to-end tests tend to
be more expensive in terms of maintenance costs.
 It’s hard to keep a balance between the attributes of a good test. A test can’t have
the maximum score in each of the first three categories, and you also have to keep an
eye on the maintainability aspect so the test remains reasonably short and simple.
Therefore, you have to make trade-offs. Moreover, you should make those trade-offs
in such a way that no particular attribute turns to zero. The sacrifices have to be par-
tial and strategic.
 What should those sacrifices look like? Because of the mutual exclusiveness of pro-
tection against regressions, resistance to refactoring, and fast feedback, you may think that the
best strategy is to concede a little bit of each: just enough to make room for all three
attributes.
 In reality, though, resistance to refactoring is non-negotiable. You should aim at gain-
ing as much of it as you can, provided that your tests remain reasonably quick and you
don’t resort to the exclusive use of end-to-end tests. The trade-off, then, comes down
to the choice between how good your tests are at pointing out bugs and how fast they
do that: that is, between protection against regressions and fast feedback. You can view this
choice as a slider that can be freely moved between protection against regressions and
fast feedback. The more you gain in one attribute, the more you lose on the other
(see figure 4.10).
 The reason resistance to refactoring is non-negotiable is that whether a test possesses
this attribute is mostly a binary choice: the test either has resistance to refactoring or it
doesn’t. There are almost no intermediate stages in between. Thus you can’t concede
Resistance to
refactoring
Fast
feedback
Protection
against
regressions
Unreachable ideal
Figure 4.9
It’s impossible to create an 
ideal test that would have a perfect score 
in all three attributes.


---
**Page 86**

86
CHAPTER 4
The four pillars of a good unit test
just a little resistance to refactoring: you’ll have to lose it all. On the other hand, the metrics
of protection against regressions and fast feedback are more malleable. You will see in the
next section what kind of trade-offs are possible when you choose one over the other.
TIP
Eradicating brittleness (false positives) in tests is the first priority on the
path to a robust test suite.
The CAP theorem
The trade-off between the first three attributes of a good unit test is similar to the
CAP theorem. The CAP theorem states that it is impossible for a distributed data
store to simultaneously provide more than two of the following three guarantees:
Consistency, which means every read receives the most recent write or an error.
Availability, which means every request receives a response (apart from out-
ages that affect all nodes in the system).
Partition tolerance, which means the system continues to operate despite
network partitioning (losing connection between network nodes).
The similarity is two-fold:
First, there is the two-out-of-three trade-off.
Second, the partition tolerance component in large-scale distributed systems is
also non-negotiable. A large application such as, for example, the Amazon web-
site can’t operate on a single machine. The option of preferring consistency and
availability at the expense of partition tolerance simply isn’t on the table—Amazon
has too much data to store on a single server, however big that server is.
refactoring
Max
out
Protection against
regressions
Fast feedback
Max
out
Maintainability
Choose between the two
Resistance to
Figure 4.10
The best tests exhibit maximum maintainability and resistance 
to refactoring; always try to max out these two attributes. The trade-off 
comes down to the choice between protection against regressions and fast 
feedback.


---
**Page 87**

87
Exploring well-known test automation concepts
4.5
Exploring well-known test automation concepts
The four attributes of a good unit test shown earlier are foundational. All existing,
well-known test automation concepts can be traced back to these four attributes. In
this section, we’ll look at two such concepts: the Test Pyramid and white-box versus
black-box testing.
4.5.1
Breaking down the Test Pyramid
The Test Pyramid is a concept that advocates for a certain ratio of different types of
tests in the test suite (figure 4.11):
Unit tests
Integration tests
End-to-end tests
The Test Pyramid is often represented visually as a pyramid with those three types of
tests in it. The width of the pyramid layers refers to the prevalence of a particular type
The choice, then, also boils down to a trade-off between consistency and availability.
In some parts of the system, it’s preferable to concede a little consistency to gain
more availability. For example, when displaying a product catalog, it’s generally fine
if some parts of the catalog are out of date. Availability is of higher priority in this sce-
nario. On the other hand, when updating a product description, consistency is more
important than availability: network nodes must have a consensus on what the most
recent version of that description is, in order to avoid merge conflicts. 
End-
to-end
Integration
tests
Unit tests
Test count
Emulating
user
Figure 4.11
The Test Pyramid advocates for a certain ratio of unit, 
integration, and end-to-end tests.


