# 9.0 Introduction [auto-generated] (pp.215-216)

---
**Page 215**

215
Writing larger tests
Most of the code we tested in previous chapters could be tested via unit tests. When
that was not possible because, say, the class depended on something else, we used
stubs and mocks to replace the dependency, and we still wrote a unit test. As I said
when we discussed the testing pyramid in chapter 1, I favor unit tests as much as
possible when testing business rules.
 But not everything in our systems can (or should) be tested via unit tests. Writ-
ing unit tests for some pieces of code is a waste of time. Forcing yourself to write
unit tests for them would result in test suites that are not good enough to find bugs,
are hard to write, or are flaky and break when you make small changes in the code.
 This chapter discusses how to identify which parts of the system should be tested
with integration or system tests. Then I will illustrate how I write these tests for three
common situations: (1) components (or sets of classes) that should be exercised
together, because otherwise, the test suite would be too weak; (2) components that
communicate with external infrastructure, such as classes that communicate with
databases and are full of SQL queries; and (3) the entire system, end to end.
This chapter covers
Deciding when to write a larger test
Engineering reliable integration and system tests


---
**Page 216**

216
CHAPTER 9
Writing larger tests
9.1
When to use larger tests
I see two situations where you should use a larger test:
You have exercised each class individually, but the overall behavior is composed
of many classes, and you want to see them work together. Think of a set of
classes that calculates the final cost of a shopping cart. You have unit-tested the
class responsible for business rule 1 and the class responsible for business rule 2.
But you still want to see the final cost of the shopping cart after all the rules
have been applied to it.
The class you want to test is a component in a larger plug-and-play architecture.
One of the main advantages of object-oriented design is that we can encapsu-
late and abstract repetitive complexity, so the user only has to implement what
matters. Think of a plugin for your favorite IDE (in my case, IntelliJ). You can
develop the logic of the plugin, but many actions will only happen when IntelliJ
calls the plugin and passes parameters to it.
The following sections show examples of both cases and will help you generalize
them.
9.1.1
Testing larger components
As always, let’s use a concrete example. Suppose we have the following requirement:
Given a shopping cart with items, quantities, and respective unit prices, the
final price of the cart is calculated as follows:
The final price of each item is calculated by multiplying its unit price by
the quantity.
The delivery costs are the following. For shopping carts with
– 1 to 3 elements (inclusive), we charge 5 dollars extra.
– 4 to 10 elements (inclusive), we charge 12.5 dollars extra.
– More than 10 elements, we charge 20 dollars extra.
If there is an electronic item in the cart, we charge 7.5 dollars extra.
NOTE
The business rule related to delivery costs is not realistic. As a devel-
oper, when you notice such inconsistencies, you should talk to the stake-
holder, product owner, or whomever is sponsoring that feature. I am keeping
this business rule simple for the sake of the example.
Before I begin coding, I think about how to approach the problem. I see how the
final price is calculated and that a list of rules is applied to the shopping cart. My
experience with software design and design for testability tells me that each rule
should be in its own class—putting everything in a single class would result in a large
class, which would require lots of tests. We prefer small classes that require only a
handful of tests.


