# 6.5.2 Performance drawbacks (pp.148-149)

---
**Page 148**

148
CHAPTER 6
Styles of unit testing
systems fully intact: all decision-making resides in AuditManager as before. The second
approach concedes a degree of that separation for performance gains: the decision as
to whether to call the database now goes to the application service, not AuditManager.
 Note that, unlike these two options, making the domain model (AuditManager)
depend on the database isn’t a good idea. I’ll explain more about keeping the balance
between performance and separation of concerns in the next two chapters.
NOTE
A class from the functional core should work not with a collaborator,
but with the product of its work, a value. 
6.5.2
Performance drawbacks
The performance impact on the system as a whole is a common argument against
functional architecture. Note that it’s not the performance of tests that suffers. The
output-based tests we ended up with work as fast as the tests with mocks. It’s that the
system itself now has to do more calls to out-of-process dependencies and becomes
less performant. The initial version of the audit system didn’t read all files from the
working directory, and neither did the version with mocks. But the final version does
in order to comply with the read-decide-act approach.
 The choice between a functional architecture and a more traditional one is a
trade-off between performance and code maintainability (both production and test
code). In some systems where the performance impact is not as noticeable, it’s better
to go with functional architecture for additional gains in maintainability. In others,
you might need to make the opposite choice. There’s no one-size-fits-all solution. 
Collaborators vs. values
You may have noticed that AuditManager’s AddRecord() method has a dependency
that’s not present in its signature: the _maxEntriesPerFile field. The audit man-
ager refers to this field to make a decision to either append an existing audit file or
create a new one.
Although this dependency isn’t present among the method’s arguments, it’s not hid-
den. It can be derived from the class’s constructor signature. And because the _max-
EntriesPerFile field is immutable, it stays the same between the class instantiation
and the call to AddRecord(). In other words, that field is a value.
The situation with the IDatabase dependency is different because it’s a collaborator,
not a value like _maxEntriesPerFile. As you may remember from chapter 2, a col-
laborator is a dependency that is one or the other of the following:
Mutable (allows for modification of its state)
A proxy to data that is not yet in memory (a shared dependency)
The IDatabase instance falls into the second category and, therefore, is a collabo-
rator. It requires an additional call to an out-of-process dependency and thus pre-
cludes the use of output-based testing.


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


