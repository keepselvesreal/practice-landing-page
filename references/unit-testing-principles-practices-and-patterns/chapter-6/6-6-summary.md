# 6.6 Summary (pp.149-151)

---
**Page 149**

149
Summary
6.5.3
Increase in the code base size
The same is true for the size of the code base. Functional architecture requires a clear
separation between the functional (immutable) core and the mutable shell. This
necessitates additional coding initially, although it ultimately results in reduced code
complexity and gains in maintainability.
 Not all projects exhibit a high enough degree of complexity to justify such an initial
investment, though. Some code bases aren’t that significant from a business perspec-
tive or are just plain too simple. It doesn’t make sense to use functional architecture
in such projects because the initial investment will never pay off. Always apply func-
tional architecture strategically, taking into account the complexity and importance of
your system.
 Finally, don’t go for purity of the functional approach if that purity comes at too
high a cost. In most projects, you won’t be able to make the domain model fully
immutable and thus can’t rely solely on output-based tests, at least not when using an
OOP language like C# or Java. In most cases, you’ll have a combination of output-
based and state-based styles, with a small mix of communication-based tests, and that’s
fine. The goal of this chapter is not to incite you to transition all your tests toward the
output-based style; the goal is to transition as many of them as reasonably possible.
The difference is subtle but important. 
Summary
Output-based testing is a style of testing where you feed an input to the SUT and
check the output it produces. This style of testing assumes there are no hidden
inputs or outputs, and the only result of the SUT’s work is the value it returns.
State-based testing verifies the state of the system after an operation is completed.
In communication-based testing, you use mocks to verify communications between
the system under test and its collaborators.
The classical school of unit testing prefers the state-based style over the
communication-based one. The London school has the opposite preference.
Both schools use output-based testing.
Output-based testing produces tests of the highest quality. Such tests rarely cou-
ple to implementation details and thus are resistant to refactoring. They are
also small and concise and thus are more maintainable.
State-based testing requires extra prudence to avoid brittleness: you need to
make sure you don’t expose a private state to enable unit testing. Because state-
based tests tend to be larger than output-based tests, they are also less maintain-
able. Maintainability issues can sometimes be mitigated (but not eliminated)
with the use of helper methods and value objects.
Communication-based testing also requires extra prudence to avoid brittle-
ness. You should only verify communications that cross the application bound-
ary and whose side effects are visible to the external world. Maintainability of


---
**Page 150**

150
CHAPTER 6
Styles of unit testing
communication-based tests is worse compared to output-based and state-based
tests. Mocks tend to occupy a lot of space, and that makes tests less readable.
Functional programming is programming with mathematical functions.
A mathematical function is a function (or method) that doesn’t have any hidden
inputs or outputs. Side effects and exceptions are hidden outputs. A reference
to an internal or external state is a hidden input. Mathematical functions are
explicit, which makes them extremely testable.
The goal of functional programming is to introduce a separation between busi-
ness logic and side effects.
Functional architecture helps achieve that separation by pushing side effects
to the edges of a business operation. This approach maximizes the amount of
code written in a purely functional way while minimizing code that deals with
side effects.
Functional architecture divides all code into two categories: functional core
and mutable shell. The functional core makes decisions. The mutable shell supplies
input data to the functional core and converts decisions the core makes into
side effects.
The difference between functional and hexagonal architectures is in their treat-
ment of side effects. Functional architecture pushes all side effects out of the
domain layer. Conversely, hexagonal architecture is fine with side effects made
by the domain layer, as long as they are limited to that domain layer only. Func-
tional architecture is hexagonal architecture taken to an extreme.
The choice between a functional architecture and a more traditional one is a
trade-off between performance and code maintainability. Functional architec-
ture concedes performance for maintainability gains.
Not all code bases are worth converting into functional architecture. Apply
functional architecture strategically. Take into account the complexity and the
importance of your system. In code bases that are simple or not that important,
the initial investment required for functional architecture won’t pay off.


---
**Page 151**

151
Refactoring toward
valuable unit tests
In chapter 1, I defined the properties of a good unit test suite:
It is integrated into the development cycle.
It targets only the most important parts of your code base.
It provides maximum value with minimum maintenance costs. To achieve
this last attribute, you need to be able to:
– Recognize a valuable test (and, by extension, a test of low value).
– Write a valuable test.
Chapter 4 covered the topic of recognizing a valuable test using the four attributes:
protection against regressions, resistance to refactoring, fast feedback, and main-
tainability. And chapter 5 expanded on the most important one of the four: resis-
tance to refactoring.
 As I mentioned earlier, it’s not enough to recognize valuable tests, you should also
be able to write such tests. The latter skill requires the former, but it also requires
This chapter covers
Recognizing the four types of code
Understanding the Humble Object pattern
Writing valuable tests


