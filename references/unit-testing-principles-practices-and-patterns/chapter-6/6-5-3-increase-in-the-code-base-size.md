# 6.5.3 Increase in the code base size (pp.149-149)

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


